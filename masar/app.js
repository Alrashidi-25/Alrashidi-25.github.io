/**
 * مسار — Masar GPA Planner
 * Client-side only. Nothing is uploaded; state lives in localStorage.
 */
(() => {
  'use strict';

  /* ================= Grade scales (Saudi universities) ================= */
  const SCALES = {
    5: {
      max: 5,
      grades: [
        { code: 'A+', label: 'ممتاز مرتفع', range: '95 – 100', points: 5.00 },
        { code: 'A',  label: 'ممتاز',       range: '90 – 94',  points: 4.75 },
        { code: 'B+', label: 'جيد جداً مرتفع', range: '85 – 89', points: 4.50 },
        { code: 'B',  label: 'جيد جداً',    range: '80 – 84',  points: 4.00 },
        { code: 'C+', label: 'جيد مرتفع',   range: '75 – 79',  points: 3.50 },
        { code: 'C',  label: 'جيد',         range: '70 – 74',  points: 3.00 },
        { code: 'D+', label: 'مقبول مرتفع', range: '65 – 69',  points: 2.50 },
        { code: 'D',  label: 'مقبول',       range: '60 – 64',  points: 2.00 },
        { code: 'F',  label: 'راسب',        range: 'أقل من 60', points: 1.00 }
      ],
      standing: [
        { min: 4.50, label: 'ممتاز' },
        { min: 3.75, label: 'جيد جداً' },
        { min: 2.75, label: 'جيد' },
        { min: 2.00, label: 'مقبول' },
        { min: 0,    label: 'ضعيف' }
      ]
    },
    4: {
      max: 4,
      grades: [
        { code: 'A+', label: 'ممتاز مرتفع', range: '95 – 100', points: 4.00 },
        { code: 'A',  label: 'ممتاز',       range: '90 – 94',  points: 3.75 },
        { code: 'B+', label: 'جيد جداً مرتفع', range: '85 – 89', points: 3.50 },
        { code: 'B',  label: 'جيد جداً',    range: '80 – 84',  points: 3.00 },
        { code: 'C+', label: 'جيد مرتفع',   range: '75 – 79',  points: 2.50 },
        { code: 'C',  label: 'جيد',         range: '70 – 74',  points: 2.00 },
        { code: 'D+', label: 'مقبول مرتفع', range: '65 – 69',  points: 1.50 },
        { code: 'D',  label: 'مقبول',       range: '60 – 64',  points: 1.00 },
        { code: 'F',  label: 'راسب',        range: 'أقل من 60', points: 0.00 }
      ],
      standing: [
        { min: 3.50, label: 'ممتاز' },
        { min: 3.00, label: 'جيد جداً' },
        { min: 2.25, label: 'جيد' },
        { min: 1.50, label: 'مقبول' },
        { min: 0,    label: 'ضعيف' }
      ]
    }
  };

  const STORAGE_KEY = 'masar.v1';
  // Blank so a fresh row doesn't quietly count toward the GPA before it's filled in
  const DEFAULT_HOURS = '';

  /* ================= State ================= */
  let state = {
    scale: 5,
    courses: [],
    prior: { gpa: '', hours: '' },
    target: { gpa: '', hours: '' },
    terms: []
  };

  const load = () => {
    try {
      const raw = localStorage.getItem(STORAGE_KEY);
      if (raw) state = Object.assign(state, JSON.parse(raw));
    } catch { /* storage unavailable or corrupt — start fresh */ }
    if (!state.courses.length) state.courses = [newCourse(), newCourse(), newCourse()];
  };
  const save = () => {
    try { localStorage.setItem(STORAGE_KEY, JSON.stringify(state)); } catch { /* ignore */ }
  };

  let seq = 0;
  const newCourse = () => ({ id: `c${Date.now()}${seq++}`, name: '', hours: DEFAULT_HOURS, code: 'A' });

  /* ================= Helpers ================= */
  const $ = (id) => document.getElementById(id);
  const scale = () => SCALES[state.scale];
  const pointsFor = (code) => scale().grades.find(g => g.code === code)?.points ?? 0;
  const fmt = (n) => (Math.round(n * 100) / 100).toFixed(2);
  const num = (v) => { const n = parseFloat(v); return Number.isFinite(n) ? n : 0; };

  const standingFor = (gpa, hours) => {
    if (!hours) return '—';
    return scale().standing.find(s => gpa >= s.min)?.label ?? '—';
  };

  /** Term totals from the current course rows. Courses with 0 hours are ignored. */
  const termTotals = () => {
    let hours = 0, points = 0;
    state.courses.forEach(c => {
      const h = num(c.hours);
      if (h <= 0) return;
      hours += h;
      points += h * pointsFor(c.code);
    });
    return { hours, points, gpa: hours ? points / hours : 0 };
  };

  /** Prior record — saved terms take priority, manual inputs are the fallback. */
  const priorRecord = () => {
    if (state.terms.length) {
      const hours = state.terms.reduce((s, t) => s + t.hours, 0);
      const points = state.terms.reduce((s, t) => s + t.points, 0);
      return { hours, points, gpa: hours ? points / hours : 0, fromSaved: true };
    }
    const hours = num(state.prior.hours);
    const gpa = num(state.prior.gpa);
    return { hours, points: gpa * hours, gpa, fromSaved: false };
  };

  /* ================= Rendering ================= */

  function renderCourses() {
    const tbody = $('courseRows');
    tbody.textContent = '';

    state.courses.forEach((course) => {
      const tr = document.createElement('tr');

      // name
      const tdName = document.createElement('td');
      const name = document.createElement('input');
      name.type = 'text';
      name.value = course.name;
      name.placeholder = 'مثال: تحليل وتصميم النظم';
      name.setAttribute('aria-label', 'اسم المادة');
      name.addEventListener('input', () => { course.name = name.value; save(); });
      tdName.appendChild(name);

      // hours
      const tdHours = document.createElement('td');
      const hours = document.createElement('input');
      hours.type = 'number';
      hours.min = '0';
      hours.max = '12';
      hours.step = '1';
      hours.inputMode = 'numeric';
      hours.placeholder = '3';
      hours.value = course.hours;
      hours.setAttribute('aria-label', 'عدد الساعات');
      hours.addEventListener('input', () => { course.hours = hours.value; update(); });
      tdHours.appendChild(hours);

      // grade
      const tdGrade = document.createElement('td');
      const sel = document.createElement('select');
      sel.setAttribute('aria-label', 'التقدير');
      scale().grades.forEach(g => {
        const opt = document.createElement('option');
        opt.value = g.code;
        // LRI/PDI isolate the Latin grade code so "A+" doesn't render as "+A" in RTL
        opt.textContent = `⁦${g.code}⁩ · ${g.label}`;
        sel.appendChild(opt);
      });
      sel.value = course.code;
      sel.addEventListener('change', () => { course.code = sel.value; update(); });
      tdGrade.appendChild(sel);

      // points
      const tdPts = document.createElement('td');
      tdPts.className = 'pts';
      tdPts.textContent = fmt(num(course.hours) * pointsFor(course.code));

      // delete
      const tdAct = document.createElement('td');
      const del = document.createElement('button');
      del.type = 'button';
      del.className = 'row-del';
      del.setAttribute('aria-label', 'حذف المادة');
      del.innerHTML = '<svg class="ic"><use href="#i-trash"/></svg>';
      del.addEventListener('click', () => {
        state.courses = state.courses.filter(c => c.id !== course.id);
        renderCourses();
        update();
      });
      tdAct.appendChild(del);

      tr.append(tdName, tdHours, tdGrade, tdPts, tdAct);
      tbody.appendChild(tr);
    });

    $('emptyNote').hidden = state.courses.length > 0;
  }

  function renderRefTable() {
    const tbody = $('refTable').querySelector('tbody');
    tbody.textContent = '';
    scale().grades.forEach(g => {
      const tr = document.createElement('tr');
      [g.label, g.code, g.range, fmt(g.points)].forEach((val, i) => {
        const td = document.createElement('td');
        td.textContent = val;
        if (i === 1) td.className = 'code';
        // "A+" and "95 – 100" both flip under an RTL base direction
        if (i === 1 || i === 3 || (i === 2 && !/[؀-ۿ]/.test(val))) td.dir = 'ltr';
        tr.appendChild(td);
      });
      tbody.appendChild(tr);
    });
  }

  function renderSummary() {
    const term = termTotals();
    const prior = priorRecord();
    const totalHours = prior.hours + term.hours;
    const cumGpa = totalHours ? (prior.points + term.points) / totalHours : 0;

    $('termGpa').textContent = fmt(term.gpa);
    $('termGrade').textContent = standingFor(term.gpa, term.hours);
    $('termHours').textContent = term.hours;
    $('termPoints').textContent = `${fmt(term.points)} نقطة`;
    $('cumGpa').textContent = fmt(cumGpa);
    $('cumGrade').textContent = standingFor(cumGpa, totalHours);
    $('totalHours').textContent = totalHours;

    const note = $('autoNote');
    if (prior.fromSaved) {
      note.hidden = false;
      note.querySelector('span').textContent =
        `محسوب تلقائياً من ${state.terms.length} فصل محفوظ: ${fmt(prior.gpa)} على ${prior.hours} ساعة. احذف الفصول المحفوظة إذا تبي تدخل الأرقام يدوياً.`;
      $('priorGpa').disabled = true;
      $('priorHours').disabled = true;
    } else {
      note.hidden = true;
      $('priorGpa').disabled = false;
      $('priorHours').disabled = false;
    }
  }

  function renderTarget() {
    const out = $('targetOut');
    const targetGpa = num(state.target.gpa);
    const prior = priorRecord();
    const term = termTotals();
    const hours = num(state.target.hours) || term.hours;

    if (!targetGpa || !hours) { out.hidden = true; return; }
    out.hidden = false;

    const max = scale().max;
    // required = (target × totalHours − priorPoints) / termHours
    const required = (targetGpa * (prior.hours + hours) - prior.points) / hours;
    const msg = $('targetMsg');

    if (targetGpa > max) {
      $('targetResult').textContent = '—';
      msg.className = 'target-msg bad';
      msg.textContent = `المعدل المستهدف لازم يكون ${max} أو أقل على هذا النظام.`;
      return;
    }

    $('targetResult').textContent = required <= 0 ? '0.00' : fmt(Math.min(required, max));

    if (required > max) {
      msg.className = 'target-msg bad';
      const needed = fmt(required);
      msg.textContent = `صعب هذا الفصل — تحتاج ${needed} وهو أعلى من سقف النظام (${max}). وسّع الخطة على أكثر من فصل أو زد عدد الساعات.`;
    } else if (required <= 0) {
      msg.className = 'target-msg ok';
      msg.textContent = 'أنت فوق هدفك أصلاً — حتى لو كان أداء الفصل ضعيف بتظل عند المستهدف.';
    } else if (required > max * 0.9) {
      msg.className = 'target-msg warn';
      msg.textContent = `ممكن بس يبي له انضباط — تحتاج ${fmt(required)} في ${hours} ساعة، يعني أغلب موادك لازم تكون تقدير عالي.`;
    } else {
      msg.className = 'target-msg ok';
      msg.textContent = `في المتناول — تحتاج معدل ${fmt(required)} في ${hours} ساعة هذا الفصل.`;
    }
  }

  function renderHistory() {
    const card = $('historyCard');
    card.hidden = state.terms.length === 0;
    if (card.hidden) return;

    const list = $('termList');
    list.textContent = '';
    state.terms.forEach(t => {
      const li = document.createElement('li');
      li.className = 'term-item';

      const name = document.createElement('span');
      name.className = 'term-name';
      name.textContent = t.name;

      const hours = document.createElement('span');
      hours.className = 'term-stat';
      hours.textContent = `${t.hours} ساعة`;

      const pts = document.createElement('span');
      pts.className = 'term-stat';
      pts.textContent = `${fmt(t.points)} نقطة`;

      const gpa = document.createElement('span');
      gpa.className = 'term-gpa';
      gpa.textContent = fmt(t.gpa);

      const del = document.createElement('button');
      del.type = 'button';
      del.className = 'term-del';
      del.setAttribute('aria-label', `حذف ${t.name}`);
      del.innerHTML = '<svg class="ic"><use href="#i-trash"/></svg>';
      del.addEventListener('click', () => {
        state.terms = state.terms.filter(x => x.id !== t.id);
        update();
      });

      li.append(name, hours, pts, gpa, del);
      list.appendChild(li);
    });

    const trend = $('trend');
    trend.textContent = '';
    const max = scale().max;
    state.terms.forEach(t => {
      const bar = document.createElement('div');
      bar.className = 'trend-bar';

      const val = document.createElement('span');
      val.className = 'trend-val';
      val.textContent = fmt(t.gpa);

      const fill = document.createElement('div');
      fill.className = 'trend-fill';
      fill.style.height = `${Math.max((t.gpa / max) * 100, 3)}%`;

      const label = document.createElement('span');
      label.className = 'trend-name';
      label.textContent = t.name;

      bar.append(val, fill, label);
      trend.appendChild(bar);
    });
  }

  function renderDistribution() {
    const counts = new Map();
    state.courses.forEach(c => {
      if (num(c.hours) <= 0) return;
      counts.set(c.code, (counts.get(c.code) || 0) + 1);
    });
    state.terms.forEach(t => {
      Object.entries(t.dist || {}).forEach(([code, n]) => counts.set(code, (counts.get(code) || 0) + n));
    });

    const total = [...counts.values()].reduce((a, b) => a + b, 0);
    const card = $('distCard');
    card.hidden = total === 0;
    if (card.hidden) return;

    const box = $('dist');
    box.textContent = '';
    scale().grades.forEach(g => {
      const n = counts.get(g.code) || 0;
      if (!n) return;
      const row = document.createElement('div');
      row.className = 'dist-row';

      const code = document.createElement('span');
      code.className = 'dist-code';
      code.textContent = g.code;

      const track = document.createElement('div');
      track.className = 'dist-track';
      const fill = document.createElement('div');
      fill.className = 'dist-fill';
      fill.style.width = `${(n / total) * 100}%`;
      track.appendChild(fill);

      const count = document.createElement('span');
      count.className = 'dist-count';
      count.textContent = `${n} مادة`;

      row.append(code, track, count);
      box.appendChild(row);
    });
  }

  const update = () => {
    // Keep the points column in sync without rebuilding inputs (would drop focus)
    state.courses.forEach((c, i) => {
      const cell = $('courseRows').children[i]?.querySelector('.pts');
      if (cell) cell.textContent = fmt(num(c.hours) * pointsFor(c.code));
    });
    renderSummary();
    renderTarget();
    renderHistory();
    renderDistribution();
    save();
  };

  /* ================= Actions ================= */

  function saveTerm() {
    const term = termTotals();
    if (!term.hours) {
      alert('أضف مواد بساعات معتمدة قبل حفظ الفصل.');
      return;
    }
    const name = prompt('اسم الفصل:', `الفصل ${state.terms.length + 1}`);
    if (name === null) return;

    const dist = {};
    state.courses.forEach(c => {
      if (num(c.hours) <= 0) return;
      dist[c.code] = (dist[c.code] || 0) + 1;
    });

    state.terms.push({
      id: `t${Date.now()}`,
      name: name.trim() || `الفصل ${state.terms.length + 1}`,
      hours: term.hours,
      points: term.points,
      gpa: term.gpa,
      dist
    });

    state.courses = [newCourse(), newCourse(), newCourse()];
    renderCourses();
    update();
  }

  function exportCsv() {
    const rows = [['اسم المادة', 'الساعات', 'التقدير', 'النقاط']];
    state.courses.forEach(c => {
      if (num(c.hours) <= 0) return;
      rows.push([c.name || 'بدون اسم', c.hours, c.code, fmt(num(c.hours) * pointsFor(c.code))]);
    });
    if (rows.length === 1) { alert('ما فيه مواد للتصدير.'); return; }

    const term = termTotals();
    rows.push([]);
    rows.push(['المعدل الفصلي', fmt(term.gpa)]);
    rows.push(['مجموع الساعات', term.hours]);
    rows.push(['مجموع النقاط', fmt(term.points)]);
    rows.push(['النظام', `من ${scale().max}`]);

    // Escape quotes, and prefix BOM so Excel reads Arabic correctly
    const csv = rows.map(r => r.map(cell => `"${String(cell).replace(/"/g, '""')}"`).join(',')).join('\r\n');
    const blob = new Blob(['﻿' + csv], { type: 'text/csv;charset=utf-8' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'masar-gpa.csv';
    a.click();
    URL.revokeObjectURL(url);
  }

  /* ================= Wiring ================= */

  function init() {
    load();
    renderCourses();
    renderRefTable();

    $('priorGpa').value = state.prior.gpa;
    $('priorHours').value = state.prior.hours;
    $('targetGpa').value = state.target.gpa;
    $('targetHours').value = state.target.hours;

    document.querySelectorAll('.scale-btn').forEach(btn => {
      btn.classList.toggle('is-active', Number(btn.dataset.scale) === state.scale);
      btn.addEventListener('click', () => {
        state.scale = Number(btn.dataset.scale);
        document.querySelectorAll('.scale-btn').forEach(b => b.classList.toggle('is-active', b === btn));
        renderCourses();
        renderRefTable();
        update();
      });
    });

    $('addCourse').addEventListener('click', () => {
      state.courses.push(newCourse());
      renderCourses();
      update();
      $('courseRows').lastElementChild?.querySelector('input')?.focus();
    });

    $('clearCourses').addEventListener('click', () => {
      if (!confirm('تبي تمسح كل مواد هذا الفصل؟')) return;
      state.courses = [newCourse()];
      renderCourses();
      update();
    });

    $('saveTerm').addEventListener('click', saveTerm);
    $('exportCsv').addEventListener('click', exportCsv);

    $('clearHistory').addEventListener('click', () => {
      if (!confirm('تبي تمسح كل الفصول المحفوظة؟ ما يمكن التراجع.')) return;
      state.terms = [];
      update();
    });

    ['priorGpa', 'priorHours'].forEach(id => {
      $(id).addEventListener('input', e => {
        state.prior[id === 'priorGpa' ? 'gpa' : 'hours'] = e.target.value;
        update();
      });
    });
    ['targetGpa', 'targetHours'].forEach(id => {
      $(id).addEventListener('input', e => {
        state.target[id === 'targetGpa' ? 'gpa' : 'hours'] = e.target.value;
        update();
      });
    });

    update();
  }

  document.addEventListener('DOMContentLoaded', init);
})();
