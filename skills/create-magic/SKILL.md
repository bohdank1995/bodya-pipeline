---
name: "create-magic"
description: "Run when Bodya says \"let's create magic\", starts a new project, or wants to formulate a vision, a target audience, desired outcomes, what to validate, or hypotheses with success bars. Guides one project through his validation pipeline step by step, using the notes in My Brain/Rules and templates, and saves each result as a note in the project folder. This version covers all of layer 1, from the vision to the gate."
---

# Create magic

Guides one project through the first part of Bodya's validation pipeline. It knows which stage the project is at, asks the questions for that stage, formulates his answers with the rules and templates he built, and saves the result.

Trigger: "let's create magic", "I'm starting a project", or a request to work on one of the stages below. If he names a project, use only that project. If the name matches more than one folder, ask which.

## The two diagrams (context)

**Validation pipeline (layer 1).** Proves that the audience has the problem.
Vision + Target audience (starting assumptions) → Desired outcomes → 1. Choose what to validate → 2. Hypotheses + bar → 3. Choose how to validate → 4. Validate (validation profile, then the evidence log) → 5. Result + decision → Gate → pass: Validated outcome, the start of layer 2. Not yet or fail: next lap.

**Solution validation (layer 2).** Used after the outcomes are validated.
Validated outcome → Explore ways to achieve it → Pick one way → Hypotheses + bar → Choose how to validate → Minimal requirements → Build → Validate → Document + decide → Share → Next lap or layer.

Source files: GitHub repo `bodya-pipeline`, folder `diagrams/` (`idea-validation` and `solution-validation`).

**This version covers all of layer 1, up to and including the gate.** Layer 2 is context only.

## Where things live

Vault root: `My Brain/`.

Rules and templates, in `My Brain/Rules and templates/`:
- `Vision statement rules`, `Vision questions`
- `Target audience rules`, `Target audience questions`
- `Desired outcomes rules`
- `Choose what to validate rules`
- `Hypothesis rules`
- `Choose how to validate rules`
- `Validation profile rules`
- `Evidence log rules`
- `Result and decision rules`
- `Gate rules`

Project notes, in `My Brain/<Project>/`:
- `Vision.md`, `Target Audience.md`, `Desired Outcomes.md`, `Validation Plan.md`, `Evidence Log.md`

Before each stage, read that stage's notes again. Do not work from memory of the rules. If a rules note is missing, say so and ask what to do.

## Find the stage

Read the project folder. Take the first row that matches.

| State of the project folder | Stage |
|---|---|
| No `Vision.md`, or it is empty | 1. Vision |
| `Vision.md` exists, no `Target Audience.md` | 2. Target audience |
| Audience exists, no `Desired Outcomes.md` | 3. Desired outcomes |
| Outcomes exist, no `Validation Plan.md`, or the last entry has no "What we validate" | 4. Choose what to validate |
| The last entry has "What we validate" but no hypotheses table | 5. Hypotheses + bar |
| The last entry has a hypotheses table but no methods table | 6. Choose how to validate |
| The last entry has a methods table but no next steps table | 6. Choose how to validate, part 2: next steps |
| The last entry has a next steps table but no validation profile | 7. Validate, part 1: validation profile |
| The profile exists, and `Evidence Log.md` has fewer people than the sample size for this entry | 7. Validate, part 2: evidence log |
| The evidence log reaches the sample size, and "Result and decision" is empty | 8. Result + decision |
| The result is written, and the gate has not run | 9. Gate |
| The gate result is "Pass" | Stop. Layer 2 is not built yet |
| The gate result is "Not yet" | Back to stage 7, part 2, for more evidence |
| The gate result is "Fail" | A new entry, starting at stage 4 |

If he asks for the result before the sample size is reached, do stage 8 and use "Not enough data" where the rules say so.

If he says he is starting a project, begin at stage 1. If he names a stage whose earlier stage is missing, say what is missing and offer to do it first.

Say the stage in one line.

## Ask before every stage

Before starting any stage, including the first one, ask one yes or no question that names it, and wait for his answer. For example: "Should we now choose how to validate?" Do not start the stage until he says yes. Ask again before part 2 of a stage.

## Chat first, file second

Show everything in the chat: the options, the drafts, the questions and the tables. Write to the project file only the result he agreed to, after his OK. Show every table in the chat even though the same table is also saved in Obsidian.

## How to work every stage

- Ask **one question at a time**.
- Every question can be answered with **"unknown"**. Record it as an assumption. Never fill it with a guess.
- Do not suggest answers. Give examples only if he asks.
- If he says he does not understand, rephrase the question with his earlier answers filled in.
- If he gives more than one answer to a question that asks for one, record all of them.
- Each question has one idea, states its scope, can be answered from what he knows, and has options that do not overlap.
- Use his own words. Do not add items he did not give. If you think something is missing, ask.
- When the draft is ready, check it against the stage's rules, show it, and let him correct it.
- Before writing, say which file will change and wait for his OK.

## Stage 1. Vision

Read `Vision statement rules` and `Vision questions`. Run the question set. Draft three versions, check them against the rules, and let him pick. Save only the chosen sentence in `Vision.md`, with nothing else in the file.

## Stage 2. Target audience

Read `Target audience rules`, `Target audience questions` and `Vision.md`. Run the question set. Draft the statement and the fields with an evidence status for each (known, assumed, unknown). Fewer than 5 people spoken with means the whole statement is marked a hypothesis. Save `Target Audience.md` with the statement, the fields, the research tasks and the first problem hypotheses.

## Stage 3. Desired outcomes

Read `Desired outcomes rules`, `Vision.md` and `Target Audience.md`.

1. Ask him to list what the audience wants, in his own words.
2. For each trigger in the audience note that has no outcome, ask what the audience wants instead.
3. For each item, ask why it matters to the audience role, until the answer reaches the vision. Ask what would have to be true first, to find missing steps.
4. Label each item with one of three words: **Job**, **Outcome** or **Consequence**. Keep his wording. Do not write measurable statements yet.
5. Show the sorted list and the chain. Save `Desired Outcomes.md` in the structure he already uses.

## Stage 4. Choose what to validate

Read `Choose what to validate rules`, `Vision.md`, `Target Audience.md` and `Desired Outcomes.md`.

1. He picks one outcome.
2. Turn it into the statement: "We validate that [audience] [feel / experience / do this] when [situation]". Take the audience from the audience note exactly as written. Ask for the situation if the notes do not give it.
3. Fix anything that breaks the rules: two feelings in one statement, a wish instead of the present, a solution word, a number. Explain each fix in one line.
4. Show the statement and the checklist result. After his OK, add a new entry to `Validation Plan.md` with the outcome, a status, and the statement. Leave the hypotheses and the method as placeholders.

## Stage 5. Hypotheses + bar

Read `Hypothesis rules` and the entry in `Validation Plan.md`.

1. Ask him to write his hypotheses plainly, in any form.
2. For each one, ask only the questions needed to fill the template: who exactly, what they do or feel, how often or how many, the number, the sample size, the kind of evidence, and the deadline.
3. Put each in the template: "We believe that [audience] [does or experiences X] [how often, or how many]", with the success bar "We are right if [number] of [sample size] [show this] by [deadline]".
4. Check: 3 to 5 hypotheses, one behaviour each, about today, observable, different aspects (frequency, feeling, cost, workaround), a bar on every one. If an aspect is missing, say so and ask whether to add one.
5. If he gives no number, propose one and label it "proposed". Ask him to confirm or change it. Leave a missing deadline as "Not set".
6. Ask for the rule for the whole claim, and propose one if he has none (for example, at least 3 of 4 reach their bar).
7. Show the table. After his OK, write it into the entry in `Validation Plan.md` with every status "Not tested".

When showing hypotheses for the first time, say that H means hypothesis and that later tables refer to them by number.

## Stage 6. Choose how to validate

Read `Choose how to validate rules` and the entry in `Validation Plan.md`.

**Part 1: methods**
1. Show the list of methods from the rules, as a table, in the chat.
2. Suggest methods for the entry's hypotheses, following the rules for choosing: match each method to its success bar, cheapest honest method, "do" over "say", at most two methods per lap.
3. Show the suggestion as the methods table from the rules: grouped by method, the method named once, one row per hypothesis, columns in this order: Method, Tests, How, Success bar, Sample, Needed first. Copy each success bar from the hypotheses table without changing it.
4. He chooses. After his OK, write the methods table under "How to validate" in the entry, and update the entry's status.

**Part 2: next steps**
1. Ask: "Should we now write the next steps?" Wait for yes.
2. Draft 3 to 7 next steps as the next steps table from the rules: Step, Produces, Needs, Time box, Needs other people. Each step starts with a verb, holds one action and produces something visible. The first step can start today. Steps end where "Validate + collect insights" starts. Mark time boxes as rough estimates.
3. Show the table in the chat. After his OK, write it into the entry and update the entry's status.

## Stage 7. Validate

Read `Validation profile rules`, `Evidence log rules`, `Target Audience.md` and the entry.

**Part 1: validation profile**
1. Fill the profile table from the audience note and the entry. Copy every value. Write "Missing" for any required field that is empty.
2. Show the profile in the chat. If a required field is missing, say which and ask for it.
3. After his OK, write the profile under "Validation profile" in the entry.

**Part 2: evidence log**
1. Ask: "Should we log evidence from a conversation?" Wait for yes.
2. He tells or pastes what happened in one conversation, in any form.
3. Split it into rows, one per piece of evidence, with the exact words. For each column the notes do not give (date, person label, hypothesis, for or against, unprompted, level), ask one question at a time. Never guess.
4. Show the rows in the chat. After his OK, add them under the entry's section in `Evidence Log.md`.
5. Say how many people are logged so far, out of the sample size.

## Stage 8. Result + decision

Read `Result and decision rules`, the entry and the entry's evidence log.

1. Count the people for and against each hypothesis, following the rules: people not rows, only what the bar counts.
2. Show the results table, the claim result from the verdict rule, and the strongest evidence against.
3. Ask him to decide: keep, narrow, change or stop. You may say which one the rules point to, but he decides.
4. Ask what he learned and what surprised him, then the next step.
5. After his OK, write everything under "Result and decision" in the entry.

## Stage 9. Gate

Read `Gate rules`, the entry, the evidence log and `Target Audience.md`.

1. Go through the six checks. For each, write what you found in the notes and whether it passes.
2. Show the checklist and the gate result it points to: pass, not yet or fail.
3. He makes the final call.
4. On pass, fill the validated outcome template with up to 3 rows of strongest evidence by number. After his OK, write the checklist, the result and the validated outcome under "Gate" in the entry.
5. On not yet, go back to stage 7, part 2. On fail, offer a new entry at stage 4.

## After each stage

Show one progress line, then the next step:

`Vision ✓ → Audience ✓ → Outcomes ✓ → Choose what ✓ → Hypotheses + bar ✓ → Choose how ✓ → Validate ✓ → Result ✓ → Gate ✓ → Layer 2 (not built yet)`

## Not built yet

Layer 2 (solution validation), the X post and the portfolio page. When the gate passes, say that this version stops here, and leave the plan as it is.

## Rules

- Say which files will change and wait for his OK before writing anything.
- Change only the stage's own file, `Validation Plan.md` and `Evidence Log.md`.
- Never invent facts, numbers or quotes. Unknown stays unknown.
- Keep prose plain: no inflated words, no rule-of-three padding, no em dashes.
- Keep answers short. He is easily overwhelmed, so show one stage at a time.
- If the vault cannot be reached, say so and tell him to open the Claude desktop app on his Mac and add the My Brain folder from the + menu. Continue by asking for the content and giving him the text to paste.
