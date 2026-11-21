#!/usr/bin/env python3
"""Rebuild a project's pipeline diagram from its vault notes.

Reads the project's notes, works out which pipeline steps are done and which one is
current, then writes the Archify candidate and renders it with Archify:

  - done steps are grayed out (Archify's gray `external` type, so hover and the
    click popover with the description still work),
  - the current step is enlarged and framed with a red "You are here" group,
  - the edges between done steps are gray,
  - the note "0 Plan" is rewritten as a checklist of what to do in the current step
    (ticks are kept, and so are items you add yourself).

Usage:
  python3 scripts/build_project_diagram.py delivery-crm \
      --vault "~/Documents/My Brain/Delivery CRM (new pipeline test)" --title "Delivery CRM"

Run it again whenever the notes change. Add --plan-only to skip the diagram and refresh just the
checklist and the step column (instant).
"""
import argparse
import copy
import json
import os
import re
import shutil
import subprocess
import sys
from urllib.parse import quote

REPO = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE = os.path.join(REPO, "diagrams", "pipeline", "candidate.json")
ARCHIFY = os.environ.get("ARCHIFY_BIN", os.path.expanduser("~/.claude/skills/archify/bin/archify.mjs"))

# Pipeline order. Done = every step before the current one.
ORDER = [
    "vision", "audience", "outcomes", "choose", "formulate", "how", "validate", "evidence",
    "result", "share1", "gate", "validated",
    "list", "pick", "hypothesis", "how2", "requirements", "build", "validate2", "document", "share", "next",
]

# In the base diagram these three are gray (`external`) as plain waypoints. In a project
# diagram gray means "done", so a step that is not done yet gets a different colour.
NOT_DONE_TYPE = {"vision": "frontend", "audience": "frontend", "validated": "frontend"}


def find_note(vault, name):
    """The note called `name`, ignoring a leading number: '1 Vision.md' matches 'Vision.md'."""
    if not os.path.isdir(vault):
        return None
    for f in sorted(os.listdir(vault)):
        if re.sub(r"^\d+\s+", "", f).lower() == name.lower():
            return os.path.join(vault, f)
    return None


def read(vault, name):
    path = find_note(vault, name)
    return open(path, encoding="utf-8").read() if path else ""


def section(text, heading):
    """Body of a section, up to the next heading of the same or a higher level (sub-headings stay inside)."""
    m = re.search(r"^(#{2,4})\s+" + re.escape(heading) + r"\s*$", text, re.M)
    if not m:
        return ""
    level = len(m.group(1))
    rest = text[m.end():]
    end = re.search(r"^#{1," + str(level) + r"}\s", rest, re.M)
    return (rest[: end.start()] if end else rest).strip()


def table_rows(block):
    rows = []
    for line in block.splitlines():
        line = line.strip()
        if line.startswith("|") and not re.match(r"^\|[\s:|-]+\|?$", line):
            rows.append([c.strip() for c in line.strip("|").split("|")])
    return rows


def lap_folder(vault):
    """The latest 'Validation' folder (numbered or not): one folder holds one lap, one note per pipeline step."""
    dirs = [d for d in sorted(os.listdir(vault))
            if os.path.isdir(os.path.join(vault, d)) and re.sub(r"^\d+\s+", "", d).lower().startswith("validation")]
    return os.path.join(vault, dirs[-1]) if dirs else vault


def completed(vault):
    """Return {step id: done?} for every step the notes can tell us about."""
    lap = lap_folder(vault)
    choose = read(lap, "Choose what to validate.md")
    hypotheses = read(lap, "Hypotheses and bar.md")
    how = read(lap, "Choose how to validate.md")
    profile = read(lap, "Validate.md")
    evidence = read(lap, "Evidence log.md")
    result = read(lap, "Result and decision.md")
    gate_note = read(lap, "Gate.md")

    sample = 5
    m = re.search(r"Sample size\s*\|\s*(\d+)", profile)
    if m:
        sample = int(m.group(1))

    # Evidence rows: a row counts when the Person column is filled.
    people = set()
    for row in table_rows(section(evidence, "From people") or evidence):  # public sources do not count as people
        if len(row) > 2 and row[0].isdigit() and row[2]:
            people.add(row[2].lower())

    decision_rows = table_rows(result.split("**Decision**")[-1]) if "**Decision**" in result else []
    decision_filled = len(decision_rows) >= 2 and bool(decision_rows[1][0])

    gate = re.search(r"\*\*Gate result:\*\*\s*(.+)", gate_note)
    gate_text = gate.group(1).strip() if gate else ""
    gate_ran = bool(gate_text) and not gate_text.lower().startswith("not run")

    profile_ready = bool(re.search(r"Ready to start\s*\|\s*Yes", profile))
    validate_done = profile_ready and len(people) >= sample

    return {
        "vision": bool(read(vault, "Vision.md").strip()),
        "audience": bool(section(read(vault, "Target Audience.md"), "Statement")),
        "outcomes": bool(section(read(vault, "Desired Outcomes.md"), "Outcomes")),
        "choose": bool(re.search(r"^We validate\b.+", choose, re.M)),
        "formulate": bool(re.search(r"^\|\s*H\d+\s*\|", hypotheses, re.M)),
        "how": "| **" in how,
        "validate": validate_done,
        "evidence": validate_done,
        "result": decision_filled,
        "share1": gate_ran,  # the gate comes after sharing
        "gate": gate_ran,
        "validated": gate_ran and gate_text.lower().startswith("pass"),
    }


def build(candidate, done_map, title, output):
    d = copy.deepcopy(candidate)
    d["meta"]["title"] = title
    d["meta"]["output"] = output
    d["groups"] = [g for g in d["groups"] if g["id"] != "g-now"]

    current = next((s for s in ORDER if not done_map.get(s, False)), None)
    done = set(ORDER[: ORDER.index(current)]) if current else set(ORDER)

    for n in d["nodes"]:
        if n["id"] in done:
            n["type"] = "external"  # gray
        elif n["id"] in NOT_DONE_TYPE:
            n["type"] = NOT_DONE_TYPE[n["id"]]
        if n["id"] == current:
            n["height"] = 104  # taller, not wider: a wider node can push the canvas past Archify's readable width
            n["tag"] = "you are here"

    for e in d["edges"]:
        if e["from"] in done and e["to"] in done and e.get("variant") != "dashed":
            e["variant"] = "default"

    legend = d["meta"]["legend"]["entries"]
    legend["external"] = {"label": "Done", "visible": bool(done)}

    group = None
    if current:
        node = next(n for n in d["nodes"] if n["id"] == current)
        group = {"id": "g-now", "label": "You are here", "lane": node["lane"],
                 "fromCol": node["col"], "toCol": node["col"], "variant": "security"}
    return d, current, done, group


def write_steps(base, built, current, done, folder, slug):
    """Write steps.js: the same steps, sections and status, for the column view in the tab.
    The column view is plain HTML (Archify's canvas cannot reflow into a narrow column)."""
    lane_label = {l["id"]: l["label"] for l in base["lanes"]}
    node = {n["id"]: n for n in base["nodes"]}  # base nodes keep their natural type
    label_of = {n["id"]: n["label"] for n in base["nodes"]}
    steps = []
    for sid in ORDER:
        n = node[sid]
        incoming = next((e for e in base["edges"] if e["to"] == sid and e.get("role") != "return"
                         and e["from"] in ORDER[: ORDER.index(sid)]), None)
        returns = [{"label": e.get("label", ""), "to": label_of[e["to"]]}
                   for e in base["edges"] if e["from"] == sid and e.get("role") == "return"]
        steps.append({
            "id": sid,
            "label": n["label"],
            "sublabel": n.get("sublabel", ""),
            "description": n.get("description", ""),
            "section": lane_label[n["lane"]],
            "type": NOT_DONE_TYPE.get(sid, n["type"]),
            "state": "current" if sid == current else ("done" if sid in done else "todo"),
            "via": (incoming or {}).get("label", ""),
            "returns": returns,
        })
    data = {"title": built["meta"]["title"], "current": current, "steps": steps}
    path = os.path.join(REPO, folder, "steps.js")
    with open(path, "w", encoding="utf-8") as f:
        f.write("// Generated by scripts/build_project_diagram.py. Do not edit.\n")
        f.write("window.PIPELINE_STEPS = window.PIPELINE_STEPS || {};\n")
        f.write("window.PIPELINE_STEPS[%s] = %s;\n" % (json.dumps(slug), json.dumps(data, indent=1, ensure_ascii=False)))


# ---------------------------------------------------------------------------------------------
# "0 Plan": a checklist for the current step
# ---------------------------------------------------------------------------------------------

def first_table(text):
    """Rows of the first Markdown table in `text` (a table ends at the first line that is not part of it)."""
    block, started = [], False
    for line in text.splitlines():
        if line.strip().startswith("|"):
            started = True
            block.append(line)
        elif started:
            break
    return table_rows("\n".join(block))


def methods(vault):
    """The methods chosen in '3 Choose how to validate': one dict per method, in table order."""
    rows = first_table(read(lap_folder(vault), "Choose how to validate.md"))
    if not rows or rows[0][0].lower() != "method":
        return []
    head = [c.lower() for c in rows[0]]
    col = {n: head.index(n) for n in ("method", "people", "how", "sample", "needs") if n in head}
    out, cur = [], None
    for r in rows[1:]:
        cell = lambda n: r[col[n]].replace("**", "").strip() if n in col and col[n] < len(r) else ""
        if cell("method"):
            cur = {"method": cell("method"), "people": cell("people").lower().startswith("y"), "how": cell("how"), "sample": "", "needs": ""}
            out.append(cur)
        if cur:
            cur["sample"] = cur["sample"] or cell("sample")
            cur["needs"] = cur["needs"] or cell("needs")
    return out


def lower_first(s):
    return s[:1].lower() + s[1:] if s and not s[:2].isupper() else s


def plain_action(how):
    """The first sentence of a method's "How", as a plain instruction ('Open each business's public pages ...')."""
    first = re.split(r"(?<=[.!?])\s", how.strip())[0].rstrip(".")
    first = re.sub(r"^[^:]{1,60}:\s*", "", first)  # drop a label such as "Last part of the same conversation:"
    return first[:1].upper() + first[1:]


def validate_groups(vault):
    """Tasks for the Validate step, grouped by method, then one group for the evidence log.
    Each group says where it belongs: its heading links to the note that holds it.
    Each task says what to do in plain words, taken from the method's own "How"."""
    ms = methods(vault)
    if not ms:
        return [{"title": None, "link": None, "items": ["Choose the methods in [[3 Choose how to validate]]"]}]
    groups, seen = [], set()
    for m in ms:
        if m["people"]:
            continue
        items = []
        need = re.split(r"[.;]", m["needs"])[0].strip()
        if (need and need.lower() != "nothing extra" and not need.lower().startswith("the same")
                and need.lower() not in seen):
            seen.add(need.lower())
            items.append("Prepare: " + lower_first(need))
        action = plain_action(m["how"]) if m["how"] else "Do " + m["method"]
        if m["sample"][:1].isdigit():
            action += ". Do it for " + lower_first(m["sample"])
        items.append(action)
        groups.append({"title": m["method"], "link": "3 Choose how to validate", "items": items})
    people = [m for m in ms if m["people"]]
    if people:
        sample = people[0]["sample"]
        items = ["Book conversations" + (" with " + sample if sample else "")]
        items += [plain_action(m["how"]) if m["how"] else "Do " + m["method"] for m in people]
        groups.append({"title": " + ".join(m["method"] for m in people), "link": "3 Choose how to validate", "items": items})
    log = []
    if any(not m["people"] for m in ms):
        log.append("Log each public-source finding in [[5 Evidence log#From public sources]] within 24 hours")
    if people:
        log.append("Log each conversation in [[5 Evidence log#From people]] within 24 hours")
    groups.append({"title": "Evidence log", "link": "5 Evidence log", "items": log})
    return groups


# What to do in each step. Anything project-specific comes from the notes.
STAGE_TASKS = {
    "vision": ["Answer the vision questions with Claude", "Pick one version", "Save it as [[1 Vision]]"],
    "audience": ["Answer the audience questions with Claude", "Write the audience statement", "Fill in the fields in [[2 Target Audience]]"],
    "outcomes": ["List the outcomes people want", "Sort them and write the chain", "Save it as [[3 Desired Outcomes]]"],
    "choose": ["Pick one outcome from [[3 Desired Outcomes]]", "Write the claim in [[1 Choose what to validate]]"],
    "formulate": ["Write 3 to 5 hypotheses in [[2 Hypotheses and bar]]", "Give each one a success bar with a number", "Write the rule for the whole claim"],
    "how": ["Choose a method for each hypothesis in [[3 Choose how to validate]]", "Write the next steps"],
    "result": ["Count the people for and against each hypothesis in [[6 Result and decision]]",
               "Compare with the success bars and the verdict rule", "Decide: keep, narrow, change or stop",
               "Write what you learned and the next step"],
    "share1": ["Write the post or the portfolio case in [[7 Share]]"],
    "gate": ["Run the six checks in [[8 Gate]]", "If it passes, write [[5 Validated opportunity]]"],
    "validated": ["Write [[5 Validated opportunity]]"],
}


def plan_groups(current, vault, node_by_id):
    """The checklist for the current step, as groups: [{title, link, items}]. A group without a title is a plain list."""
    if current is None:
        return []
    if current in ("validate", "evidence"):
        return validate_groups(vault)
    if current in STAGE_TASKS:
        return [{"title": None, "link": None, "items": STAGE_TASKS[current]}]
    n = node_by_id[current]
    return [{"title": None, "link": None, "items": [n["label"] + (": " + n["sublabel"] if n.get("sublabel") else "")]}]


TASK_LINE = re.compile(r"^- \[( |x|X)\] (.+?)\s*$")
WIKILINK = re.compile(r"\[\[([^\]|#]+)(#[^\]|]*)?(?:\|([^\]]*))?\]\]")
MINE = "Mine"  # heading for items added by hand


def obsidian_root(vault):
    d = os.path.abspath(vault)
    while d != os.path.dirname(d):
        if os.path.isdir(os.path.join(d, ".obsidian")):
            return d
        d = os.path.dirname(d)
    return None


def obsidian_url(vault, target):
    """obsidian:// link that opens `target` ('Note' or 'Note#Heading') from anywhere, or None if it is not found."""
    root = obsidian_root(vault)
    if not root:
        return None
    name, _, heading = target.partition("#")
    for dirpath, dirnames, filenames in os.walk(vault):
        dirnames[:] = [d for d in dirnames if not d.startswith(".")]
        for f in filenames:
            if f.lower() == name.strip().lower() + ".md":
                rel = os.path.relpath(os.path.join(dirpath, f), root)[:-3]
                file = rel + ("#" + heading if heading else "")
                return "obsidian://open?vault=%s&file=%s" % (quote(os.path.basename(root), safe=""), quote(file, safe=""))
    return None


def sync_plan(vault, groups, folder, slug, stage_label):
    """Write '0 Plan.md' as grouped checklists. Keeps ticks, keeps items the user added (under "Mine"),
    drops stale generated ones. A hidden file in the project folder remembers what was generated last time."""
    path = find_note(vault, "Plan.md") or os.path.join(vault, "0 Plan.md")
    state_path = os.path.join(vault, ".plan-state.json")
    try:
        last = set(json.load(open(state_path, encoding="utf-8")).get("generated", []))
    except (OSError, ValueError):
        last = set()

    existing = []  # (done, text), in file order
    if os.path.exists(path):
        for line in open(path, encoding="utf-8").read().splitlines():
            m = TASK_LINE.match(line)
            if m:
                existing.append((m.group(1) != " ", m.group(2)))
    ticked = {text: done for done, text in existing}
    generated = [tx for g in groups for tx in g["items"]]
    mine = [(d, tx) for d, tx in existing if tx not in last and tx not in generated]  # added by hand

    def box(d, tx):
        return "- [%s] %s\n" % ("x" if d else " ", tx)

    out, plan_groups_out = "# Plan\n", []
    for g in groups + ([{"title": MINE, "link": None, "items": [tx for _, tx in mine]}] if mine else []):
        items = [(ticked.get(tx, False) if g["title"] != MINE else dict((tx2, d2) for d2, tx2 in mine)[tx], tx) for tx in g["items"]]
        if g["title"]:
            out += "\n### " + ("[[%s|%s]]" % (g["link"], g["title"]) if g["link"] else g["title"]) + "\n"
        out += "\n" + "".join(box(d, tx) for d, tx in items)
        plan_groups_out.append({"title": g["title"], "link": g["link"], "items": items})
    with open(path, "w", encoding="utf-8") as f:
        f.write(out)
    with open(state_path, "w", encoding="utf-8") as f:
        json.dump({"generated": generated}, f, ensure_ascii=False, indent=1)

    # the page: every [[link]] becomes an obsidian:// link
    links = {}
    def collect(text):
        for m in WIKILINK.finditer(text):
            target = m.group(1) + (m.group(2) or "")
            url = obsidian_url(vault, target)
            if url:
                links[target] = url
    data_groups = []
    for g in plan_groups_out:
        if g["link"]:
            collect("[[%s]]" % g["link"])
        data_groups.append({"title": g["title"], "href": links.get(g["link"]) if g["link"] else None,
                            "items": [{"text": tx, "done": d} for d, tx in g["items"]]})
        for _, tx in g["items"]:
            collect(tx)
    data = {"title": "Plan", "stage": stage_label, "groups": data_groups, "links": links}
    with open(os.path.join(REPO, folder, "plan.js"), "w", encoding="utf-8") as f:
        f.write("// Generated by scripts/build_project_diagram.py from the note '0 Plan'. Do not edit. Not committed.\n")
        f.write("window.PIPELINE_PLAN = window.PIPELINE_PLAN || {};\n")
        f.write("window.PIPELINE_PLAN[%s] = %s;\n" % (json.dumps(slug), json.dumps(data, indent=1, ensure_ascii=False)))
    return [it for g in plan_groups_out for it in g["items"]]


def finalize(candidate_path, html_path, out_dir):
    shutil.rmtree(out_dir, ignore_errors=True)  # receipts are generated; start clean each run
    cmd = ["node", ARCHIFY, "finalize", "workflow", candidate_path, html_path,
           "--quality", "showcase", "--out-dir", out_dir, "--json"]
    r = subprocess.run(cmd, cwd=REPO, capture_output=True, text=True)
    try:
        return json.loads(r.stdout)
    except ValueError:
        return {"status": "fail", "diagnostics": [{"code": "no-json", "message": (r.stdout + r.stderr)[-400:]}]}


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("slug", help="project folder name under diagrams/, e.g. delivery-crm")
    ap.add_argument("--vault", required=True, help="the project's notes folder")
    ap.add_argument("--title", required=True)
    ap.add_argument("--plan-only", action="store_true", help="skip the Archify diagram; refresh only the checklist and the step column")
    a = ap.parse_args()

    vault = os.path.expanduser(a.vault)
    folder = os.path.join("diagrams", a.slug)
    os.makedirs(os.path.join(REPO, folder), exist_ok=True)
    cand_rel = os.path.join(folder, "candidate.json")
    html_rel = os.path.join(folder, a.slug + ".html")

    base = json.load(open(BASE, encoding="utf-8"))
    d, current, done, group = build(base, completed(vault), a.title, html_rel)

    if not a.plan_only:
        attempts = [("with the You are here frame", d["groups"] + ([group] if group else []))]
        if group:
            attempts.append(("without the frame (it blocked a route)", d["groups"]))
        result = None
        for label, groups in attempts:
            d["groups"] = groups
            json.dump(d, open(os.path.join(REPO, cand_rel), "w", encoding="utf-8"), indent=2, ensure_ascii=False)
            result = finalize(cand_rel, html_rel, os.path.join(folder, "review"))
            if result.get("status") == "pass":
                print("Rendered", label)
                break
        if result.get("status") != "pass":
            print("FAILED:", json.dumps(result.get("diagnostics", [])[:3], indent=1)[:1500])
            sys.exit(1)

    write_steps(base, d, current, done, folder, a.slug)
    node_by_id = {n["id"]: n for n in base["nodes"]}
    groups = plan_groups(current, vault, node_by_id)
    items = sync_plan(vault, groups, folder, a.slug, node_by_id[current]["label"] if current else "")
    print("Plan:", len(items), "items,", sum(1 for d_, _ in items if d_), "ticked")
    print("Current step:", current or "(all done)")
    print("Done:", ", ".join(s for s in ORDER if s in done) or "(none)")
    if not a.plan_only:
        print("Output:", os.path.join(REPO, html_rel))


if __name__ == "__main__":
    main()
