'use strict';

const $ = (id) => document.getElementById(id);
const make = (tag, text, className) => {
  const el = document.createElement(tag);
  if (text !== undefined) el.textContent = text;
  if (className) el.className = className;
  return el;
};

const colors = ['#07665e', '#aa4c28', '#3f5d96'];
const fmt = (x) => Intl.NumberFormat('en', { maximumFractionDigits: 2 }).format(x);
const fmtSigned = (x) => (x > 0 ? '+' : '') + fmt(x);

const TOPIC_GROUP_DEFS = [
  { id: 'all', topics: null },
  { id: 'core', topics: ['access', 'fairness', 'fade', 'hukou'] },
  { id: 'mech', topics: ['inputs', 'restriction', 'ranks', 'ranks-legacy'] },
  { id: 'choice', topics: ['grade', 'calendar', 'wealth', 'fulltime'] },
  { id: 'sens', topics: ['schools', 'skills'] }
];

const topicsFor = {
  SCHOOLS: 'schools', N_WEIGHT: 'skills', NONHUKOU: 'hukou', QUOTA: 'hukou',
  DECAY: 'fade', HOME: 'inputs', TEACH_ZONE: 'inputs', PRE_EFF: 'restriction',
  POST_EFF: 'restriction', REBAND: 'inputs', BAN_GRAD: 'restriction', BAN_RED: 'restriction',
  gain: 'ranks', signal: 'grade', budget_share: 'fulltime', force_none: 'grade', board_term: 'calendar',
  board_rule: 'calendar', boarding_rule: 'calendar', ses_coef: 'wealth', access: 'grade', hours: 'calendar',
  part_price: 'grade', full_group_price: 'fulltime', premium_price: 'fulltime', premium_quality: 'fulltime'
};

const exactCasesFor = {
  HOME: ['inputs', 1], TEACH_ZONE: ['inputs', 2], REBAND: ['inputs', 6], gain: ['ranks', 2],
  signal: ['grade', 'g11_belief_only_039'], force_none: ['grade', 'no_tutoring'],
  board_term: ['calendar', 'board_longer_term'], boarding_rule: ['calendar', 'senior_board_rank'],
  ses_coef: ['wealth', 'ses_neutral'], access: ['grade', 'access_low'],
  hours: ['calendar', 'higher_hours'], part_price: ['grade', 'part_price_high'],
  full_group_price: ['fulltime', 1], premium_price: ['fulltime', 6], premium_quality: ['fulltime', 8]
};

let topics = null;
let assumptions = [];
let provenance = null;
let storyPaths = null;

const params = new URLSearchParams(location.search);
let savedLanguage;
try { savedLanguage = localStorage.getItem('gz_lang'); } catch {}
let lang = (params.get('lang') || savedLanguage || 'en') === 'zh' ? 'zh' : 'en';
let mode = (params.get('mode') === 'explorer' || params.get('tab') || params.get('topic') || params.get('assumption')) ? 'explorer' : 'storyboard';
let storyStep = Math.max(0, Math.min(5, Math.trunc(Number(params.get('step')) || 0)));

let beat2Compare = 'rich10_p60';
let beat3Opt = 0;
let beat4Math = 'choice'; // 'choice' | 'legacy'
let beat4Idx = 2;         // 0.18 SD central in ranks
let beat4LegacyIdx = 1;   // 16.2% strong in ranks-legacy
let beat5Idx = 3;         // 45-60% fade

let tab = 'findings';
let current = 'access';
let index = 0;
let activeCategory = 'all';
let focusedAssumption = '';

const T = () => (window.GZ_I18N && window.GZ_I18N[lang]) || window.GZ_I18N.en;
const locTopic = (id) => {
  const raw = topics[id];
  const ov = T().topics[id];
  if (!ov) return raw;
  return {
    ...raw,
    label: ov.label || raw.label,
    description: ov.description || raw.description,
    metric: ov.metric || raw.metric,
    series: ov.series || raw.series,
    interval: ov.interval || raw.interval
  };
};
const locGroup = (g) => T().groups[g] || g;
const locModel = (m) => T().models[m] || m;
const option = (value, label) => { const el = make('option', label); el.value = value; return el; };

function updateURL() {
  const q = new URLSearchParams();
  if (lang !== 'en') q.set('lang', lang);
  if (mode === 'explorer') {
    q.set('mode', 'explorer');
    if (tab !== 'findings') q.set('tab', tab);
    q.set('topic', current);
    q.set('case', String(index));
    if (tab === 'assumptions' && focusedAssumption) q.set('assumption', focusedAssumption);
  } else if (storyStep > 0) {
    q.set('step', String(storyStep));
  }
  const qs = q.toString();
  history.replaceState(null, '', qs ? '?' + qs : location.pathname);
}

function applyStaticLocalization() {
  const dict = T();
  document.documentElement.lang = dict.htmlLang;
  document.title = dict.pageTitle;
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.dataset.i18n;
    if (typeof dict[key] === 'string') el.textContent = dict[key];
  });
  $('search').placeholder = dict.phSearch;
  document.querySelectorAll('[data-lang]').forEach((btn) => {
    btn.setAttribute('aria-pressed', String(btn.dataset.lang === lang));
  });
}

function setMode(nextMode, targetTab = null, setURL = true) {
  mode = nextMode === 'explorer' ? 'explorer' : 'storyboard';
  $('storyboard-shell').hidden = mode !== 'storyboard';
  $('explorer-shell').hidden = mode !== 'explorer';
  document.querySelectorAll('[data-mode]').forEach((b) => {
    if (b.tagName === 'A') {
      if (b.dataset.mode === mode) b.setAttribute('aria-current', 'location');
      else b.removeAttribute('aria-current');
    } else b.setAttribute('aria-pressed', String(b.dataset.mode === mode));
  });
  if (mode === 'explorer') {
    if (window.GZ_MC_CANVAS) window.GZ_MC_CANVAS.stop();
    if (targetTab) goTab(targetTab, false);
    if (topics && tab === 'findings') plotTopicToCanvas('chart', current, index);
  } else if (topics) {
    renderStoryStep();
  }
  if (setURL) updateURL();
}

function navigateMode(nextMode, targetTab = null) {
  setMode(nextMode, targetTab);
  const panel = $(mode === 'storyboard' ? 'storyboard-shell' : 'explorer-shell');
  const target = panel.querySelector('h2[tabindex="-1"]');
  target?.focus({ preventScroll: true });
  panel.scrollIntoView({ block: 'start' });
}

function setLanguage(nextLang) {
  lang = nextLang === 'zh' ? 'zh' : 'en';
  try { localStorage.setItem('gz_lang', lang); } catch {}
  applyStaticLocalization();
  if (topics) {
    renderStoryStep();
    renderCategoryBar();
    populateTopicSelect();
    populateAssumptionFilters();
    display(false);
    showAssumptions();
    renderProvenanceTable();
  }
  updateURL();
}

/* ==================== SHARED CHART PLOTTER ==================== */
function plotTopicToCanvas(canvasId, topicId, caseIdx) {
  const c = $(canvasId);
  if (!c || !topics || !topics[topicId]) return;
  const w = Math.round(c.getBoundingClientRect().width);
  if (!w) return;
  const t = locTopic(topicId);
  const s = t.cases[caseIdx];
  const ref = t.cases[t.default];
  const dpr = Math.min(2, window.devicePixelRatio || 1);
  const h = 104 + 54 * s.values.length;
  c.style.height = h + 'px';
  c.width = w * dpr;
  c.height = h * dpr;
  const cx = c.getContext('2d');
  cx.scale(dpr, dpr);

  cx.fillStyle = '#ffffff';
  cx.fillRect(0, 0, w, h);

  const [min, max] = t.domain;
  const left = 26, right = w - 26, top = 18, bottom = h - 46;
  const x = (v) => left + ((v - min) / (max - min)) * (right - left);

  const ticks = topicId === 'restriction'
    ? [0, 0.5, 1, 1.5, 2]
    : Array.from({ length: 5 }, (_, i) => min + ((max - min) * i) / 4);

  cx.font = '12px Inter, system-ui, sans-serif';
  cx.textAlign = 'center';
  for (const value of ticks) {
    const px = x(value);
    cx.beginPath();
    cx.moveTo(px, top);
    cx.lineTo(px, bottom);
    cx.strokeStyle = '#dde8e7';
    cx.lineWidth = 1;
    cx.stroke();
    cx.fillStyle = '#4b6064';
    cx.fillText(fmt(value), px, bottom + 19);
  }

  if (t.line !== null) {
    const lx = x(t.line);
    cx.beginPath();
    cx.moveTo(lx, top);
    cx.lineTo(lx, bottom);
    cx.setLineDash([4, 4]);
    cx.strokeStyle = '#5a7275';
    cx.lineWidth = 1.5;
    cx.stroke();
    cx.setLineDash([]);
  }

  s.values.forEach(([v, lo, hi], i) => {
    const y = top + 34 + i * 54;
    const px = x(v);
    const col = colors[i % colors.length];

    if (caseIdx !== t.default && ref && ref.values[i]) {
      const rx = x(ref.values[i][0]);
      cx.beginPath();
      cx.arc(rx, y, 5, 0, Math.PI * 2);
      cx.strokeStyle = '#9bb2b0';
      cx.lineWidth = 1.8;
      cx.stroke();
    }

    cx.strokeStyle = cx.fillStyle = col;
    if (lo !== null) {
      cx.lineWidth = 3.5;
      cx.beginPath();
      cx.moveTo(x(lo), y);
      cx.lineTo(x(hi), y);
      cx.stroke();
      [lo, hi].forEach((end) => {
        cx.beginPath();
        cx.moveTo(x(end), y - 6);
        cx.lineTo(x(end), y + 6);
        cx.stroke();
      });
    } else {
      const base = x(t.line ?? min);
      cx.globalAlpha = 0.25;
      cx.fillRect(Math.min(base, px), y - 7, Math.max(2, Math.abs(px - base)), 14);
      cx.globalAlpha = 1;
    }

    cx.beginPath();
    cx.arc(px, y, 6.5, 0, Math.PI * 2);
    cx.fill();
    cx.strokeStyle = '#fff';
    cx.lineWidth = 1.5;
    cx.stroke();

    cx.fillStyle = col;
    cx.font = 'bold 12.5px Inter, system-ui, sans-serif';
    cx.fillText(fmt(v), Math.max(left + 14, Math.min(right - 14, px)), y - 12);
  });
}

function renderValueRows(containerId, topicId, caseIdx) {
  const t = locTopic(topicId);
  const s = t.cases[caseIdx];
  const rows = s.values.map(([value, low, high], i) => {
    const row = make('div', undefined, 'value-row');
    const name = make('span');
    const dot = make('i', undefined, 'dot');
    dot.setAttribute('aria-hidden', 'true');
    dot.style.background = colors[i % colors.length];
    name.append(dot, t.series[i]);
    const valStr = low === null ? fmt(value) : `${fmt(value)}  [${fmt(low)}–${fmt(high)}]`;
    row.append(name, make('b', valStr));
    return row;
  });
  $(containerId).replaceChildren(...rows);
}

/* ==================== 6-BEAT STORYBOARD ==================== */
function renderStoryDataChart(topicId, caseIdxOrId) {
  if (window.GZ_MC_CANVAS) window.GZ_MC_CANVAS.stop();
  const t = locTopic(topicId);
  let idx = t.default;
  if (typeof caseIdxOrId === 'string') {
    const found = t.cases.findIndex((c) => c.id === caseIdxOrId);
    if (found >= 0) idx = found;
  } else if (Number.isInteger(caseIdxOrId)) {
    idx = Math.max(0, Math.min(caseIdxOrId, t.cases.length - 1));
  }
  const s = t.cases[idx];
  $('story-metric').textContent = t.metric;
  $('story-interval').textContent = t.interval;
  $('story-pill').textContent = s.label;
  $('story-caption').textContent = s.caption;
  renderValueRows('story-values', topicId, idx);
  requestAnimationFrame(() => plotTopicToCanvas('story-chart', topicId, idx));
}

function renderStoryMonteCarlo(showCompare) {
  if (!storyPaths || !window.GZ_MC_CANVAS) return;
  const p = storyPaths.example_cohort_profiles;
  const m = storyPaths.principal_medians;
  $('story-metric').textContent = lang === 'zh'
    ? '一个保存队列中的模拟升学结果'
    : 'Selective university outcomes in one saved cohort';
  $('story-interval').textContent = lang === 'zh'
    ? '显示各组获得模拟重点大学名额的比例'
    : 'Share of each group securing a simulated selective university place';
  $('story-pill').textContent = showCompare
    ? (beat2Compare === 'rich10_p60' ? (lang === 'zh' ? '天赋 vs 财富' : 'Talent vs Wealth') : (lang === 'zh' ? '同天赋财富差距' : 'Equal Talent, Wealth Gap'))
    : (lang === 'zh' ? '示例队列' : 'Example cohort');

  const rows = [];
  const addRow = (col, label, val) => {
    const r = make('div', undefined, 'value-row');
    const sp = make('span');
    const d = make('i', undefined, 'dot');
    d.style.background = col;
    sp.append(d, label);
    r.append(sp, make('b', val));
    rows.push(r);
  };
  addRow(colors[0],
    lang === 'zh' ? '能力前10% · 财富后10%（本地生）' : 'Top 10% ability · Bottom 10% wealth (local)',
    lang === 'zh' ? `示例队列 ${p.poor10_top10.selective_uni_pct}% · 全1,024组中位数 ${m.poor10_top10_uni_pct}%` : `${p.poor10_top10.selective_uni_pct}% cohort · ${m.poor10_top10_uni_pct}% median (1,024 worlds)`
  );
  if (showCompare) {
    if (beat2Compare === 'rich10_p60') {
      addRow(colors[1],
        lang === 'zh' ? '能力第60百分位 · 财富前10%（本地生）' : '60th-pct ability · Top 10% wealth (local)',
        lang === 'zh' ? `普高 ${p.rich10_p60.academic_pct}% · 重点大学通道 ${p.rich10_p60.selective_uni_pct}%` : `${p.rich10_p60.academic_pct}% academic · ${p.rich10_p60.selective_uni_pct}% selective uni`
      );
    } else {
      addRow(colors[1],
        lang === 'zh' ? '能力前10% · 财富前10%（本地生）' : 'Top 10% ability · Top 10% wealth (local)',
        lang === 'zh' ? `示例队列 ${p.rich10_top10.selective_uni_pct}% · 全1,024组中位数 ${m.rich10_top10_uni_pct}%` : `${p.rich10_top10.selective_uni_pct}% cohort · ${m.rich10_top10_uni_pct}% median (1,024 worlds)`
      );
    }
  }
  $('story-values').replaceChildren(...rows);
  $('story-caption').textContent = lang === 'zh'
    ? '横条显示一个已保存的 40,000 人合成队列中的比例。文字另列 1,024 组设定的中位数。'
    : 'Bars show rates from one saved 40,000-pupil cohort. The text also reports the median across 1,024 settings where available.';

  requestAnimationFrame(() => {
    window.GZ_MC_CANVAS.mount($('story-chart'), {
      storyPaths,
      lang,
      showCompare,
      compareMode: beat2Compare
    });
  });
}

function renderStoryStep() {
  if (!topics) return;
  const dict = T();
  const beat = dict.storyBeats[storyStep];

  const dots = dict.storyBeats.map((_, i) => {
    const b = make('button', `${i + 1}`, 'story-dot');
    b.type = 'button';
    b.setAttribute('role', 'tab');
    b.setAttribute('aria-selected', String(i === storyStep));
    b.addEventListener('click', () => { storyStep = i; renderStoryStep(); updateURL(); });
    return b;
  });
  $('story-dots').replaceChildren(...dots);
  const stepStr = dict.storyStepOf(storyStep + 1, dict.storyBeats.length);
  $('story-step-counter').textContent = stepStr;
  $('story-nav-counter').textContent = stepStr;

  $('story-tag').textContent = beat.tag;
  $('story-title').textContent = beat.title;
  $('story-lead').textContent = beat.lead;
  $('story-sub').textContent = beat.subNote;

  $('story-prev').disabled = storyStep === 0;
  $('story-next').hidden = storyStep === dict.storyBeats.length - 1;

  const controls = $('story-controls');
  const callout = $('story-callout');
  const bullets = $('story-bullets');
  const ctas = $('story-ctas');
  const stage = document.querySelector('.story-stage');
  controls.replaceChildren();
  callout.hidden = true;
  bullets.hidden = true;
  ctas.hidden = true;

  if (storyStep === 0) {
    $('story-visual-wrap').hidden = false;
    stage.classList.remove('single-col');
    controls.append(make('label', beat.controlLabel));
    const pg = make('div', undefined, 'pill-group');
    const replay = make('button', dict.btnReplay, 'ghost');
    replay.type = 'button';
    replay.addEventListener('click', () => window.GZ_MC_CANVAS?.replay());
    const pause = make('button', dict.btnPause, 'ghost');
    pause.type = 'button';
    pause.addEventListener('click', () => {
      const isPaused = window.GZ_MC_CANVAS?.togglePause();
      pause.textContent = isPaused ? dict.btnResume : dict.btnPause;
    });
    pg.append(replay, pause);
    controls.append(pg);
    renderStoryMonteCarlo(false);
  } else if (storyStep === 1) {
    $('story-visual-wrap').hidden = false;
    stage.classList.remove('single-col');
    controls.append(make('label', beat.controlLabel));
    const pg = make('div', undefined, 'pill-group');
    dict.beat2CompareOptions.forEach((opt) => {
      const b = make('button', opt.label, 'choice-pill');
      b.type = 'button';
      b.setAttribute('aria-pressed', String(beat2Compare === opt.id));
      b.addEventListener('click', () => { beat2Compare = opt.id; renderStoryStep(); });
      pg.append(b);
    });
    controls.append(pg);
    callout.hidden = false;
    callout.textContent = dict.beat2RebandCallout;
    renderStoryMonteCarlo(true);
  } else if (storyStep === 2) {
    $('story-visual-wrap').hidden = false;
    stage.classList.remove('single-col');
    controls.append(make('label', beat.controlLabel));
    const pg = make('div', undefined, 'pill-group');
    dict.beat3Options.forEach((opt, i) => {
      const b = make('button', opt.label, 'choice-pill');
      b.type = 'button';
      b.setAttribute('aria-pressed', String(i === beat3Opt));
      b.addEventListener('click', () => { beat3Opt = i; renderStoryStep(); });
      pg.append(b);
    });
    controls.append(pg);
    const chosen = dict.beat3Options[beat3Opt];
    renderStoryDataChart(chosen.topic, chosen.caseId);
  } else if (storyStep === 3) {
    $('story-visual-wrap').hidden = false;
    stage.classList.remove('single-col');
    controls.append(make('label', beat.controlLabel));
    const pg = make('div', undefined, 'pill-group');
    dict.beat4MathModes.forEach((m) => {
      const b = make('button', m.label, 'choice-pill');
      b.type = 'button';
      b.setAttribute('aria-pressed', String(beat4Math === m.id));
      b.addEventListener('click', () => { beat4Math = m.id; renderStoryStep(); });
      pg.append(b);
    });
    controls.append(pg);

    const activeTopic = beat4Math === 'legacy' ? 'ranks-legacy' : 'ranks';
    const curVal = beat4Math === 'legacy' ? beat4LegacyIdx : beat4Idx;
    const sliderRow = make('div', undefined, 'slider-controls');
    const slider = document.createElement('input');
    slider.type = 'range';
    slider.min = '0';
    slider.max = String(topics[activeTopic].cases.length - 1);
    slider.step = '1';
    slider.value = String(curVal);
    slider.addEventListener('input', () => {
      if (beat4Math === 'legacy') beat4LegacyIdx = Number(slider.value);
      else beat4Idx = Number(slider.value);
      lbl.textContent = topics[activeTopic].cases[Number(slider.value)].label;
      renderStoryDataChart(activeTopic, Number(slider.value));
    });
    slider.setAttribute('aria-label', beat.controlLabel);
    sliderRow.append(slider);
    const lbl = make('span', topics[activeTopic].cases[curVal].label, 'fine');
    controls.append(sliderRow, lbl);
    callout.hidden = false;
    callout.textContent = dict.beat4RestrictionNote;
    renderStoryDataChart(activeTopic, curVal);
  } else if (storyStep === 4) {
    $('story-visual-wrap').hidden = false;
    stage.classList.remove('single-col');
    controls.append(make('label', beat.controlLabel));
    const sliderRow = make('div', undefined, 'slider-controls');
    const slider = document.createElement('input');
    slider.type = 'range';
    slider.min = '0';
    slider.max = String(topics.fade.cases.length - 1);
    slider.step = '1';
    slider.value = String(beat5Idx);
    slider.setAttribute('aria-label', beat.controlLabel);
    slider.addEventListener('input', () => {
      beat5Idx = Number(slider.value);
      lbl.textContent = topics.fade.cases[beat5Idx].label;
      renderStoryDataChart('fade', beat5Idx);
    });
    sliderRow.append(slider);
    const lbl = make('span', topics.fade.cases[beat5Idx].label, 'fine');
    controls.append(sliderRow, lbl);
    callout.hidden = false;
    callout.textContent = dict.beat5AblationNote;
    renderStoryDataChart('fade', beat5Idx);
  } else {
    if (window.GZ_MC_CANVAS) window.GZ_MC_CANVAS.stop();
    $('story-visual-wrap').hidden = true;
    stage.classList.add('single-col');
    bullets.hidden = false;
    bullets.replaceChildren(...beat.bullets.map((b) => make('li', b)));
    ctas.hidden = false;
    const b1 = make('button', beat.ctaExplorer, 'secondary');
    b1.type = 'button';
    b1.addEventListener('click', () => navigateMode('explorer', 'findings'));
    const b2 = make('button', beat.ctaAssumptions, 'ghost');
    b2.type = 'button';
    b2.addEventListener('click', () => navigateMode('explorer', 'assumptions'));
    const b3 = make('button', beat.ctaSources, 'ghost');
    b3.type = 'button';
    b3.addEventListener('click', () => navigateMode('explorer', 'sources'));
    ctas.replaceChildren(b1, b2, b3);
  }
}

/* ==================== FULL EXPLORER ==================== */
function goTab(name, setURL = true) {
  tab = ['findings', 'assumptions', 'sources'].includes(name) ? name : 'findings';
  document.querySelectorAll('[data-tab]').forEach((button) => {
    const panel = button.dataset.tab;
    $(panel).hidden = panel !== tab;
    button.setAttribute('aria-pressed', String(panel === tab));
  });
  if (tab === 'findings' && topics && mode === 'explorer') plotTopicToCanvas('chart', current, index);
  if (setURL) updateURL();
}

function renderCategoryBar() {
  const labels = T().topicGroups;
  const buttons = TOPIC_GROUP_DEFS.map((g) => {
    const b = make('button', labels[g.id] || g.id, 'cat-pill' + (g.id === activeCategory ? ' active' : ''));
    b.type = 'button';
    b.setAttribute('aria-pressed', String(g.id === activeCategory));
    b.addEventListener('click', () => {
      activeCategory = g.id;
      renderCategoryBar();
      populateTopicSelect();
      const allowed = g.topics || Object.keys(topics);
      if (!allowed.includes(current)) pick(allowed[0]);
    });
    return b;
  });
  $('category-bar').replaceChildren(...buttons);
}

function populateTopicSelect() {
  const grp = TOPIC_GROUP_DEFS.find((g) => g.id === activeCategory);
  const allowed = grp && grp.topics ? grp.topics : Object.keys(topics);
  $('topic').replaceChildren(
    ...allowed.filter((id) => Object.hasOwn(topics, id)).map((id) => option(id, locTopic(id).label))
  );
  if (allowed.includes(current)) $('topic').value = current;
}

function populateAssumptionFilters() {
  const prevGroup = $('group').value;
  const prevModel = $('version').value;
  const groups = Array.from(new Set(assumptions.map((r) => r.group))).sort();
  const models = Array.from(new Set(assumptions.map((r) => r.model))).sort();
  $('group').replaceChildren(option('', T().optAllGroups), ...groups.map((x) => option(x, locGroup(x))));
  $('version').replaceChildren(option('', T().optAllModels), ...models.map((x) => option(x, locModel(x))));
  $('group').value = prevGroup;
  $('version').value = prevModel;
}

function pick(topicID, chosen, setURL = true) {
  current = Object.hasOwn(topics, topicID) ? topicID : 'access';
  const t = topics[current];
  if (typeof chosen === 'string') {
    const found = t.cases.findIndex((r) => r.id === chosen);
    chosen = found >= 0 ? found : t.default;
  }
  index = Number.isInteger(chosen) && chosen >= 0 ? Math.min(chosen, t.cases.length - 1) : t.default;

  const grp = TOPIC_GROUP_DEFS.find((g) => g.id === activeCategory);
  if (grp && grp.topics && !grp.topics.includes(current)) {
    activeCategory = 'all';
    renderCategoryBar();
    populateTopicSelect();
  }
  $('topic').value = current;
  $('case-select').replaceChildren(...t.cases.map((r, i) => option(String(i), r.label)));
  $('case-slider').max = String(t.cases.length - 1);
  display(setURL);
}

function display(setURL = true) {
  const dict = T();
  const t = locTopic(current);
  const s = t.cases[index];
  const ref = t.cases[t.default];

  $('case-select').value = String(index);
  $('case-slider').value = String(index);
  $('case-slider').setAttribute('aria-valuetext', s.label);
  $('prev').disabled = index === 0;
  $('next').disabled = index === t.cases.length - 1;
  $('reset-case').disabled = index === t.default;
  $('case-position').textContent = dict.casePos(index + 1, t.cases.length);
  $('explorer-title').textContent = t.label;
  $('explanation').textContent = t.description;
  $('metric').textContent = t.metric;
  $('interval').textContent = t.interval;
  $('active-case-pill').textContent = s.label;
  $('case-caption').textContent = s.caption;
  $('chart').setAttribute('aria-label', `${s.label}. ${t.metric}`);

  renderValueRows('result-values', current, index);

  const deltaBox = $('delta-box');
  if (index !== t.default && ref) {
    deltaBox.hidden = false;
    const parts = s.values.map(([v], i) => {
      const diff = v - ref.values[i][0];
      const cls = diff > 0.005 ? 'delta-pos' : diff < -0.005 ? 'delta-neg' : '';
      return `<span>${t.series[i]}: <span class="${cls}">${fmtSigned(diff)}</span></span>`;
    });
    deltaBox.innerHTML = `<strong>${dict.deltaTitle(ref.label)}</strong><br>${parts.join(' · ')}`;
  } else {
    deltaBox.hidden = true;
  }

  if (mode === 'explorer' && tab === 'findings') plotTopicToCanvas('chart', current, index);
  renderSweepOverview();
  if (setURL) updateURL();
}

function renderSweepOverview() {
  const t = locTopic(current);
  const [min, max] = t.domain;
  const span = max - min || 1;
  $('sweep-subtitle').textContent = T().sweepSub(t.cases.length);

  const rows = t.cases.map((c, i) => {
    const btn = make('button', undefined, 'sweep-row' + (i === index ? ' active' : ''));
    btn.type = 'button';
    const primary = c.values[0][0];
    const pct = Math.max(2, Math.min(100, ((primary - min) / span) * 100));
    const name = make('span', c.label, 'sweep-name');
    name.title = c.label;
    const track = make('span', undefined, 'sweep-track');
    track.setAttribute('aria-hidden', 'true');
    const bar = make('span', undefined, 'sweep-bar');
    bar.style.left = '0%';
    bar.style.width = `${pct}%`;
    bar.style.background = i === index ? '#07665e' : '#7ba6a2';
    track.append(bar);
    const valText = c.values.length > 1 ? `${fmt(c.values[0][0])} / ${fmt(c.values[1][0])}` : fmt(c.values[0][0]);
    btn.append(name, track, make('span', valText, 'sweep-val'));
    btn.addEventListener('click', () => { index = i; display(); });
    return btn;
  });

  $('sweep-list').replaceChildren(...rows);
  const activeEl = $('sweep-list').querySelector('.sweep-row.active');
  if (activeEl && t.cases.length > 10) activeEl.scrollIntoView({ block: 'nearest' });
}

function buildInlineTinker(r) {
  const topicId = topicsFor[r.id];
  if (!topicId || !topics[topicId]) return null;
  const dict = T();
  const t = locTopic(topicId);
  let localIdx = t.default;
  if (exactCasesFor[r.id]) {
    const [, step] = exactCasesFor[r.id];
    if (typeof step === 'string') {
      const found = t.cases.findIndex((c) => c.id === step);
      if (found >= 0) localIdx = found;
    } else if (Number.isInteger(step)) {
      localIdx = Math.min(step, t.cases.length - 1);
    }
  }

  const wrap = make('div', undefined, 'inline-tinker');
  const head = make('div', undefined, 'inline-tinker-head');
  const title = make('strong', dict.inlineTinkerTitle(t.label));
  const caseLbl = make('span', t.cases[localIdx].label, 'fine');
  head.append(title, caseLbl);

  const sliderRow = make('div', undefined, 'inline-tinker-slider');
  const slider = document.createElement('input');
  slider.type = 'range';
  slider.min = '0';
  slider.max = String(t.cases.length - 1);
  slider.step = '1';
  slider.value = String(localIdx);
  slider.setAttribute('aria-label', r.name);

  const readout = make('div', undefined, 'inline-tinker-readout');
  function updateReadout(idx) {
    const c = t.cases[idx];
    const ref = t.cases[t.default];
    caseLbl.textContent = `${c.label} (${idx + 1}/${t.cases.length})`;
    readout.innerHTML = c.values.map(([v, lo, hi], i) => {
      const diff = v - ref.values[i][0];
      const diffTag = idx !== t.default ? ` (${fmtSigned(diff)} ${dict.vsBaseline})` : ` (${dict.baselineTag})`;
      const rangeTag = lo !== null ? ` [${fmt(lo)}–${fmt(hi)}]` : '';
      return `<span><strong>${t.series[i]}:</strong> ${fmt(v)}${rangeTag}<span class="fine">${diffTag}</span></span>`;
    }).join('');
  }
  slider.addEventListener('input', () => updateReadout(Number(slider.value)));
  updateReadout(localIdx);

  sliderRow.append(make('span', dict.inlineSavedSetting, 'fine'), slider);
  wrap.append(head, sliderRow, readout);
  return wrap;
}

function showAssumptions() {
  const dict = T();
  const words = $('search').value.toLowerCase().trim().split(/\s+/).filter(Boolean);
  const wantedGroup = $('group').value;
  const wantedModel = $('version').value;
  const onlyTinkerable = $('tinkerable-only').checked;

  const rows = assumptions.filter((r) => {
    if (onlyTinkerable && !topicsFor[r.id]) return false;
    return (!wantedGroup || r.group === wantedGroup) &&
      (!wantedModel || r.model === wantedModel) &&
      words.every((w) =>
        Object.values(r).some((val) => String(val).toLowerCase().includes(w)) ||
        locGroup(r.group).toLowerCase().includes(w) ||
        locModel(r.model).toLowerCase().includes(w)
      );
  });

  $('assumption-count').textContent = dict.assumpCount(rows.length, assumptions.length);
  $('register').replaceChildren(...rows.map((r) => {
    const box = make('details', undefined, 'entry');
    box.id = 'assumption-' + r.id;
    const title = make('summary');
    title.append(make('span', r.name), make('code', r.id));
    if (topicsFor[r.id]) title.append(make('span', dict.pillTinker, 'pill-tinker'));

    const body = make('div', undefined, 'entry-body');
    const meta = make('dl', undefined, 'register-meta');
    [
      [dict.metaModelCat, `${locModel(r.model)} · ${locGroup(r.group)}`],
      [dict.metaDefault, r.value],
      [dict.metaRange, r.range]
    ].forEach(([label, value]) => {
      const item = make('div');
      item.append(make('dt', label), make('dd', value));
      meta.append(item);
    });
    body.append(meta, make('p', r.description), make('p', dict.basisPrefix + r.basis, 'fine'));

    const tinkerEl = buildInlineTinker(r);
    if (tinkerEl) body.append(tinkerEl);

    const actions = make('div', undefined, 'entry-actions');
    if (topicsFor[r.id]) {
      const jumpBtn = make('button', dict.btnOpenChart, 'jump');
      jumpBtn.type = 'button';
      jumpBtn.addEventListener('click', () => {
        const [target, step] = exactCasesFor[r.id] ?? [topicsFor[r.id], undefined];
        setMode('explorer', 'findings', false);
        pick(target, step);
        $('findings').scrollIntoView({ behavior: 'smooth', block: 'start' });
      });
      actions.append(jumpBtn);
    }

    const challengeBtn = make('button', dict.btnChallenge, 'ghost');
    challengeBtn.type = 'button';
    const challengeBox = make('div', undefined, 'challenge-form');
    challengeBox.hidden = true;
    const propInput = document.createElement('input');
    propInput.type = 'text';
    propInput.placeholder = dict.phSuggested(r.value);
    const noteArea = document.createElement('textarea');
    noteArea.placeholder = dict.phNote;
    const copyNoteBtn = make('button', dict.btnCopyNote, 'secondary');
    copyNoteBtn.type = 'button';
    const statusSpan = make('span', '', 'fine');

    copyNoteBtn.addEventListener('click', async () => {
      const text = [
        lang === 'zh' ? '广州教育模型假设反馈（修订版 1.4 · Dr. Trey Menefee）' : 'Guangzhou Model Assumption Note (Rev 1.4 · Dr. Trey Menefee)',
        `${r.name} [${r.id}]`,
        `${locModel(r.model)} · ${locGroup(r.group)}`,
        `Default: ${r.value} | Range: ${r.range}`,
        `Suggested: ${propInput.value.trim() || '(not specified)'}`,
        `Rationale: ${noteArea.value.trim() || '(not specified)'}`,
        `Link: ${location.origin}${location.pathname}?lang=${lang}&mode=explorer&tab=assumptions&assumption=${encodeURIComponent(r.id)}`
      ].join('\n');
      try {
        await navigator.clipboard.writeText(text);
        statusSpan.textContent = dict.noteCopied;
      } catch { window.prompt('Copy:', text); }
    });

    challengeBox.append(
      make('strong', dict.challengeTitle(r.id)),
      propInput,
      noteArea,
      (() => { const row = make('div', undefined, 'cite-actions'); row.append(copyNoteBtn, statusSpan); return row; })()
    );
    challengeBtn.addEventListener('click', () => { challengeBox.hidden = !challengeBox.hidden; });

    const linkEl = make('a', dict.permalink);
    const q = new URLSearchParams();
    if (lang !== 'en') q.set('lang', lang);
    q.set('mode', 'explorer');
    q.set('tab', 'assumptions');
    q.set('assumption', r.id);
    linkEl.href = '?' + q.toString();

    actions.append(challengeBtn, linkEl);
    body.append(actions, challengeBox);
    box.append(title, body);
    if (r.id === focusedAssumption) box.open = true;
    return box;
  }));
}

function renderProvenanceTable() {
  if (!provenance) return;
  const dict = T();
  const rows = [
    ...Object.entries(provenance.served_hashes || {}).map(([k, v]) => [dict.layerServed, k, v]),
    ...Object.entries(provenance.source_hashes || {}).map(([k, v]) => [dict.layerSource, k, v])
  ];
  const table = make('table', undefined, 'prov-table');
  table.innerHTML = `<thead><tr><th>${dict.provColLayer}</th><th>${dict.provColFile}</th><th>${dict.provColHash}</th></tr></thead>`;
  const tbody = make('tbody');
  rows.forEach(([layer, file, hash]) => {
    const tr = make('tr');
    tr.append(make('td', layer), make('td', file), (() => { const td = make('td'); td.append(make('code', hash)); return td; })());
    tbody.append(tr);
  });
  table.append(tbody);
  $('provenance-table-wrap').replaceChildren(table);
}

async function start() {
  applyStaticLocalization();
  document.querySelectorAll('[data-lang]').forEach((btn) => {
    btn.addEventListener('click', () => setLanguage(btn.dataset.lang));
  });
  document.querySelectorAll('[data-mode]').forEach((btn) => {
    btn.addEventListener('click', (event) => {
      if (btn.tagName === 'A' && (event.ctrlKey || event.metaKey || event.shiftKey || event.altKey)) return;
      event.preventDefault();
      if (btn.dataset.mode === 'storyboard') storyStep = 0;
      navigateMode(btn.dataset.mode);
    });
  });
  $('btn-skip-explorer').addEventListener('click', () => navigateMode('explorer', 'findings'));
  $('btn-back-story').addEventListener('click', () => navigateMode('storyboard'));
  $('story-prev').addEventListener('click', () => { if (storyStep > 0) { storyStep -= 1; renderStoryStep(); updateURL(); } });
  $('story-next').addEventListener('click', () => { if (storyStep < 5) { storyStep += 1; renderStoryStep(); updateURL(); } });

  window.addEventListener('keydown', (e) => {
    if (mode !== 'storyboard' || ['INPUT', 'TEXTAREA', 'SELECT'].includes(document.activeElement?.tagName)) return;
    if (e.key === 'ArrowRight' && storyStep < 5) { storyStep += 1; renderStoryStep(); updateURL(); }
    if (e.key === 'ArrowLeft' && storyStep > 0) { storyStep -= 1; renderStoryStep(); updateURL(); }
  });

  try {
    const [topicRes, assumpRes, provRes, storyRes] = await Promise.all([
      fetch('data.json'),
      fetch('assumptions.json'),
      fetch('provenance.json'),
      fetch('story_paths.json')
    ]);
    if (!topicRes.ok || !assumpRes.ok) throw new Error('Saved data request failed');
    topics = await topicRes.json();
    assumptions = await assumpRes.json();
    provenance = provRes.ok ? await provRes.json() : null;
    storyPaths = storyRes.ok ? await storyRes.json() : null;

    $('topic-count-badge').textContent = String(Object.keys(topics).length);
    $('assumption-count-badge').textContent = String(assumptions.length);

    renderCategoryBar();
    populateTopicSelect();
    populateAssumptionFilters();

    focusedAssumption = params.get('assumption') || '';
    showAssumptions();
    renderProvenanceTable();

    const rawCase = params.get('case');
    goTab(params.get('tab') || 'findings', false);
    pick(params.get('topic') || 'access', rawCase === null ? undefined : Number(rawCase), false);
    setMode(mode, null, false);

    if (focusedAssumption && mode === 'explorer') {
      document.getElementById('assumption-' + focusedAssumption)?.scrollIntoView({ behavior: 'smooth' });
    }

    document.querySelectorAll('[data-tab]').forEach((button) => {
      button.addEventListener('click', () => goTab(button.dataset.tab));
    });
    $('topic').addEventListener('change', (e) => pick(e.target.value));
    for (const id of ['case-select', 'case-slider']) {
      $(id).addEventListener('input', (e) => { index = Number(e.target.value); display(); });
    }
    $('prev').addEventListener('click', () => { if (index > 0) { index -= 1; display(); } });
    $('next').addEventListener('click', () => { if (index < topics[current].cases.length - 1) { index += 1; display(); } });
    $('reset-case').addEventListener('click', () => { index = topics[current].default; display(); });
    for (const id of ['search', 'group', 'version', 'tinkerable-only']) {
      $(id).addEventListener('input', showAssumptions);
      $(id).addEventListener('change', showAssumptions);
    }

    $('copy').addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(location.href);
        $('copy').textContent = T().btnCopied;
        $('copy-status').textContent = T().btnCopied;
        setTimeout(() => { $('copy').textContent = T().btnCopyLink; }, 1600);
      } catch { window.prompt('Copy:', location.href); }
    });

    $('download-png').addEventListener('click', () => {
      const c = $('chart');
      const a = document.createElement('a');
      a.download = `guangzhou-${current}-case-${index + 1}.png`;
      a.href = c.toDataURL('image/png');
      a.click();
    });

    $('copy-apa').addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText($('apa-cite').textContent.trim());
        $('cite-status').textContent = T().apaCopied;
      } catch { window.prompt('Copy APA:', $('apa-cite').textContent.trim()); }
    });

    $('copy-bib').addEventListener('click', async () => {
      const bib = `@misc{menefee2026guangzhou,\n  author = {Menefee, Trey},\n  title = {Educational Opportunity and Private Tutoring in Guangzhou},\n  year = {2026},\n  note = {Working paper, Revision 1.4, Atlas of Education},\n  doi = {10.5281/zenodo.24369167}\n}`;
      try {
        await navigator.clipboard.writeText(bib);
        $('cite-status').textContent = T().bibCopied;
      } catch { window.prompt('Copy BibTeX:', bib); }
    });

    new ResizeObserver(() => {
      if (mode === 'explorer' && tab === 'findings') plotTopicToCanvas('chart', current, index);
    }).observe($('chart').parentElement);
    const frame = $('story-chart').parentElement;
    let frameWidth = frame.clientWidth;
    new ResizeObserver(() => {
      const width = frame.clientWidth;
      if (!width || width === frameWidth) return;
      frameWidth = width;
      if (mode !== 'storyboard') return;
      if (storyStep <= 1) window.GZ_MC_CANVAS?.redraw();
      else if (storyStep < 5) renderStoryStep();
    }).observe(frame);
  } catch (error) {
    $('load-error').hidden = false;
    $('load-error').textContent = T().loadError;
    console.error(error);
  }
}

start();
