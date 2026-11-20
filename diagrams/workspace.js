/* Project workspace: the "0 Plan" checklist (left, about 75%) beside the pipeline steps column (right, about 25%).
 *
 * Both are read from files that scripts/build_project_diagram.py writes from the project's notes:
 *   plan.js   the checklist from the note "0 Plan" (not committed)
 *   steps.js  the pipeline steps and where you are
 * The checkboxes here only show the note. Tick them in Obsidian, then run the script to refresh.
 */
(function () {
  function h(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text != null) e.textContent = text;
    return e;
  }
  function loadScript(src) {
    return new Promise(function (resolve, reject) {
      var s = document.createElement('script');
      s.src = src; s.onload = resolve; s.onerror = function () { reject(new Error('Could not load ' + src)); };
      document.head.appendChild(s);
    });
  }

  // An earlier version let you choose a notes folder and remembered it. That choice is not used any more: clear it.
  try { indexedDB.deleteDatabase('pipeline-workspace'); } catch (e) { /* nothing to clear */ }

  // Text with [[wiki links]]. A link opens its note in Obsidian when the script could find the note, and the
  // number in front of the note's name is not shown.
  function richText(el, text, links) {
    var re = /\[\[([^\]|#]+)(#[^\]|]*)?(?:\|([^\]]*))?\]\]/g, last = 0, m;
    while ((m = re.exec(text))) {
      if (m.index > last) el.appendChild(document.createTextNode(text.slice(last, m.index)));
      var target = m[1] + (m[2] || '');
      var shown = (m[3] || m[1].replace(/^\d+\s+/, '')).trim();
      var href = links && links[target];
      var a = h(href ? 'a' : 'span', 'ws-link', shown);
      if (href) a.href = href;
      el.appendChild(a);
      last = re.lastIndex;
    }
    if (last < text.length) el.appendChild(document.createTextNode(text.slice(last)));
  }

  function mount(root, project) {
    root.classList.add('workspace');

    // =============== Plan (left) ===============
    var plan = h('section', 'ws-plan'); plan.setAttribute('aria-label', 'Plan');
    var planInner = h('div', 'ws-plan-inner');
    plan.appendChild(planInner);

    function renderPlan(data) {
      planInner.innerHTML = '';
      planInner.appendChild(h('h1', null, data.title || 'Plan'));
      var any = data.groups.some(function (g) { return g.items.length; });
      if (!any) { planInner.appendChild(h('p', 'ws-muted', 'Nothing to do right now.')); return; }
      data.groups.forEach(function (g) {
        if (!g.items.length) return;
        var sec = h('section', 'ws-group');
        if (g.title) {
          var head = h('h2', 'ws-group-title');
          if (g.href) { var a = h('a', null, g.title); a.href = g.href; head.appendChild(a); } else head.textContent = g.title;
          sec.appendChild(head);
        }
        var ul = h('ul', 'ws-todo');
        g.items.forEach(function (it) {
          var li = h('li', it.done ? 'done' : '');
          var box = h('span', 'ws-box', it.done ? '✓' : ''); box.setAttribute('role', 'img'); box.setAttribute('aria-label', it.done ? 'Done' : 'Not done');
          var txt = h('span', 'ws-todo-text'); richText(txt, it.text, data.links);
          li.appendChild(box); li.appendChild(txt); ul.appendChild(li);
        });
        sec.appendChild(ul); planInner.appendChild(sec);
      });
    }
    function planFailed() {
      planInner.innerHTML = '';
      planInner.appendChild(h('h1', null, 'Plan'));
      planInner.appendChild(h('p', 'ws-muted', 'The plan is not built yet. Run scripts/build_project_diagram.py.'));
    }

    // =============== Steps column (right, 25%) ===============
    var steps = h('aside', 'ws-steps'); steps.setAttribute('aria-label', 'Pipeline steps');
    var head = h('div', 'ws-steps-head');
    var title = h('h2', null, project.name + ' pipeline');
    var meta = h('div', 'ws-meta');
    head.appendChild(title); head.appendChild(meta);
    var scroll = h('div', 'ws-scroll');
    steps.appendChild(head); steps.appendChild(scroll);

    function key(color, text) {
      var k = h('span', 'ws-key'); var i = h('i'); i.style.background = color; k.appendChild(i); k.appendChild(document.createTextNode(text)); return k;
    }
    function renderSteps(data) {
      title.textContent = data.title + ' pipeline';
      meta.innerHTML = '';
      meta.appendChild(key('var(--ws-done)', 'Done'));
      meta.appendChild(key('var(--ws-now)', 'You are here'));
      if (project.diagram) {
        var a = h('a', null, 'Full diagram ↗'); a.href = project.diagram; a.target = '_blank'; a.rel = 'noopener'; meta.appendChild(a);
      }
      scroll.innerHTML = '';
      var list = null, currentEl = null, lastSection = null;
      data.steps.forEach(function (s) {
        if (s.section !== lastSection) {
          lastSection = s.section; var sec = h('section', 'ws-sec');
          sec.appendChild(h('h3', 'ws-sec-title', s.section)); list = h('ol', 'ws-list'); sec.appendChild(list); scroll.appendChild(sec);
        }
        var li = h('li', 'ws-step ' + s.state); li.dataset.type = s.type;
        li.appendChild(h('span', 'pin'));
        if (s.via) li.appendChild(h('span', 'ws-via', s.via));
        var btn = h('button', 'ws-btn-step'); btn.type = 'button'; btn.setAttribute('aria-expanded', 'false');
        var txt = h('span', 'txt'); txt.appendChild(h('b', null, s.label)); if (s.sublabel) txt.appendChild(h('small', null, s.sublabel));
        btn.appendChild(txt);
        if (s.state === 'current') btn.appendChild(h('span', 'ws-badge', 'You are here'));
        var detail = h('div', 'ws-detail'); detail.hidden = true;
        if (s.description) detail.appendChild(h('p', null, s.description));
        s.returns.forEach(function (r) { detail.appendChild(h('p', 'ret', (r.label || 'Return') + ' → back to "' + r.to + '"')); });
        if (!detail.children.length) detail.appendChild(h('p', null, s.sublabel || s.label));
        btn.addEventListener('click', function () { var open = detail.hidden; detail.hidden = !open; btn.setAttribute('aria-expanded', String(open)); });
        li.appendChild(btn); li.appendChild(detail); list.appendChild(li);
        if (s.state === 'current') currentEl = li;
      });
      if (currentEl) setTimeout(function () { currentEl.scrollIntoView({ block: 'center' }); }, 0);
    }

    root.appendChild(plan); root.appendChild(steps);

    function load(globalName, src, ok, fail) {
      var have = window[globalName] && window[globalName][project.id];
      if (have) return ok(have);
      loadScript(src).then(function () { ok(window[globalName][project.id]); }).catch(fail);
    }
    load('PIPELINE_PLAN', project.plan, renderPlan, planFailed);
    load('PIPELINE_STEPS', project.steps, renderSteps, function () { scroll.textContent = 'Steps are not built yet. Run scripts/build_project_diagram.py.'; });
  }

  window.Workspace = { mount: mount };
})();
