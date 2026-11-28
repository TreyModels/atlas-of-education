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
let tab = 'findings';
let current = 'access';
let index = 0;
let activeCategory = 'all';
let focusedAssumption = '';

const params = new URLSearchParams(location.search);
let lang = (params.get('lang') || localStorage.getItem('gz_lang') || 'en') === 'zh' ? 'zh' : 'en';

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

const option = (value, label) => {
  const item = make('option', label);
  item.value = value;
  return item;
};

function updateURL() {
  const q = new URLSearchParams();
  if (lang !== 'en') q.set('lang', lang);
  if (tab !== 'findings') q.set('tab', tab);
  q.set('topic', current);
  q.set('case', String(index));
  if (tab === 'assumptions' && focusedAssumption) q.set('assumption', focusedAssumption);
  history.replaceState(null, '', '?' + q.toString());
}

function ensureLangSwitch() {
  if (document.querySelector('.lang-switch')) return;
  const links = document.querySelector('.masthead-links');
  if (!links) return;
  const wrap = make('div', undefined, 'lang-switch');
  wrap.setAttribute('role', 'group');
  wrap.setAttribute('aria-label', 'Language');
  [['en', 'EN'], ['zh', '中文']].forEach(([code, label]) => {
    const b = make('button', label);
    b.type = 'button';
    b.dataset.lang = code;
    b.setAttribute('aria-pressed', String(code === lang));
    b.addEventListener('click', () => setLanguage(code));
    wrap.append(b);
  });
  links.append(wrap);
}

function applyStaticLocalization() {
  ensureLangSwitch();
  const dict = T();
  document.documentElement.lang = dict.htmlLang;
  document.title = dict.pageTitle;
  document.querySelectorAll('[data-i18n]').forEach((el) => {
    const key = el.dataset.i18n;
    if (typeof dict[key] === 'string') el.textContent = dict[key];
  });
  const selMap = [
    ['.atlas span:last-child', 'brandTitle'],
    ['.masthead .source-link', 'githubRepo'],
    ['.kicker', 'kicker'],
    ['.intro h1', 'heroTitle'],
    ['.intro .lead', 'heroLead'],
    ['.badge-precomputed', 'badgePrecomputed'],
    ['.intro-stats .stat:not(.rich) span', 'statPoor'],
    ['.intro-stats .stat.rich span', 'statRich'],
    ['.ratio-label', 'ratioLabel'],
    ['.stat-note', 'statNote'],
    ['#highlights-heading', 'highlightsHeading'],
    ['.strip-head .fine', 'highlightsSub'],
    ['label[for="topic"]', 'lblTopic'],
    ['label[for="case-select"]', 'lblCase'],
    ['#reset-case', 'btnReset'],
    ['#copy', 'btnCopyLink'],
    ['.guardrail-note', 'guardrail'],
    ['#sweep-heading', 'sweepHeading'],
    ['#assumption-title', 'assumpTitle'],
    ['.assumption-head p', 'assumpLead'],
    ['label[for="search"]', 'lblSearch'],
    ['label[for="group"]', 'lblGroup'],
    ['label[for="version"]', 'lblModel'],
    ['.toggle-check span', 'lblTinkerableOnly'],
    ['#source-title', 'srcTitle'],
    ['#sources > p', 'srcLead'],
    ['footer > span:first-child', 'footerLeft'],
    ['footer a:last-child', 'footerRepo']
  ];
  selMap.forEach(([sel, key]) => {
    const el = document.querySelector(sel);
    if (el && typeof dict[key] === 'string') el.textContent = dict[key];
  });
  const tabMap = [['findings', 'tabFindings'], ['assumptions', 'tabAssumptions'], ['sources', 'tabSources']];
  tabMap.forEach(([tId, key]) => {
    const btn = document.querySelector(`[data-tab="${tId}"]`);
    if (btn && btn.firstChild && btn.firstChild.nodeType === Node.TEXT_NODE) {
      btn.firstChild.textContent = dict[key] + ' ';
    }
  });
  $('search').placeholder = dict.phSearch;
  document.querySelectorAll('[data-lang]').forEach((btn) => {
    btn.setAttribute('aria-pressed', String(btn.dataset.lang === lang));
  });
}

function setLanguage(nextLang) {
  lang = nextLang === 'zh' ? 'zh' : 'en';
  try { localStorage.setItem('gz_lang', lang); } catch {}
  applyStaticLocalization();
  if (topics) {
    renderStoryCards();
    renderCategoryBar();
    populateTopicSelect();
    populateAssumptionFilters();
    display(false);
    showAssumptions();
    renderProvenanceTable();
  }
  updateURL();
}

function goTab(name, setURL = true) {
  tab = ['findings', 'assumptions', 'sources'].includes(name) ? name : 'findings';
  document.querySelectorAll('[data-tab]').forEach((button) => {
    const panel = button.dataset.tab;
    $(panel).hidden = panel !== tab;
    button.setAttribute('aria-pressed', String(panel === tab));
  });
  if (tab === 'findings' && topics) plot();
  if (setURL) updateURL();
}

function renderStoryCards() {
  const cards = T().storyCards.map((card, i) => {
    const btn = make('button', undefined, 'story-card');
    btn.type = 'button';
    btn.dataset.story = String(i);
    btn.append(
      make('span', card.metric, 'story-metric'),
      make('h3', card.title),
      make('p', card.summary)
    );
    btn.addEventListener('click', () => {
      activeCategory = 'all';
      renderCategoryBar();
      populateTopicSelect();
      goTab('findings', false);
      pick(card.topic, card.caseId !== undefined ? card.caseId : card.caseIdx);
      $('findings').scrollIntoView({ behavior: 'smooth', block: 'start' });
    });
    return btn;
  });
  $('story-grid').replaceChildren(...cards);
}

function highlightActiveStory() {
  const t = topics[current];
  const curId = t.cases[index]?.id;
  const cards = T().storyCards;
  document.querySelectorAll('.story-card').forEach((el, i) => {
    const c = cards[i];
    const match = c && c.topic === current && (c.caseId ? c.caseId === curId : c.caseIdx === index);
    el.classList.toggle('active', Boolean(match));
  });
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
  $('result-values').replaceChildren(...rows);

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

  plot();
  renderSweepOverview();
  highlightActiveStory();
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

    const valText = c.values.length > 1
      ? `${fmt(c.values[0][0])} / ${fmt(c.values[1][0])}`
      : fmt(c.values[0][0]);
    const val = make('span', valText, 'sweep-val');

    btn.append(name, track, val);
    btn.addEventListener('click', () => {
      index = i;
      display();
    });
    return btn;
  });

  $('sweep-list').replaceChildren(...rows);
  const activeEl = $('sweep-list').querySelector('.sweep-row.active');
  if (activeEl && t.cases.length > 10) activeEl.scrollIntoView({ block: 'nearest' });
}

function plot() {
  if (!topics || $('findings').hidden) return;
  const t = locTopic(current);
  const s = t.cases[index];
  const c = $('chart');
  const w = Math.round(c.getBoundingClientRect().width);
  if (!w) return;
  const dpr = Math.min(2, window.devicePixelRatio || 1);
  const h = 104 + 54 * s.values.length;
  c.style.height = h + 'px';
  c.width = w * dpr;
  c.height = h * dpr;
  const cx = c.getContext('2d');
  cx.scale(dpr, dpr);

  const [min, max] = t.domain;
  const left = 26, right = w - 26, top = 18, bottom = h - 46;
  const x = (v) => left + ((v - min) / (max - min)) * (right - left);

  const ticks = current === 'restriction'
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

  const ref = t.cases[t.default];
  s.values.forEach(([v, lo, hi], i) => {
    const y = top + 34 + i * 54;
    const px = x(v);
    const col = colors[i % colors.length];

    if (index !== t.default && ref && ref.values[i]) {
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
  slider.setAttribute('aria-label', `${r.name}`);

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
    if (topicsFor[r.id]) {
      title.append(make('span', dict.pillTinker, 'pill-tinker'));
    }

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
        goTab('findings', false);
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
        lang === 'zh' ? `广州教育模型假设反馈（修订版 1.4）` : `Guangzhou Model Assumption Note (Rev 1.4)`,
        `${r.name} [${r.id}]`,
        `${locModel(r.model)} · ${locGroup(r.group)}`,
        `Default: ${r.value} | Range: ${r.range}`,
        `Suggested: ${propInput.value.trim() || '(not specified)'}`,
        `Rationale: ${noteArea.value.trim() || '(not specified)'}`,
        `Link: ${location.origin}${location.pathname}?lang=${lang}&tab=assumptions&assumption=${encodeURIComponent(r.id)}`
      ].join('\n');
      try {
        await navigator.clipboard.writeText(text);
        statusSpan.textContent = dict.noteCopied;
      } catch {
        window.prompt('Copy:', text);
      }
    });

    challengeBox.append(
      make('strong', dict.challengeTitle(r.id)),
      propInput,
      noteArea,
      (() => { const row = make('div', undefined, 'cite-actions'); row.append(copyNoteBtn, statusSpan); return row; })()
    );

    challengeBtn.addEventListener('click', () => {
      challengeBox.hidden = !challengeBox.hidden;
    });

    const linkEl = make('a', dict.permalink);
    const q = new URLSearchParams();
    if (lang !== 'en') q.set('lang', lang);
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

  try {
    const [topicRes, assumpRes, provRes] = await Promise.all([
      fetch('data.json'),
      fetch('assumptions.json'),
      fetch('provenance.json')
    ]);
    if (!topicRes.ok || !assumpRes.ok) throw new Error('Saved data request failed');
    topics = await topicRes.json();
    assumptions = await assumpRes.json();
    provenance = provRes.ok ? await provRes.json() : null;

    $('topic-count-badge').textContent = String(Object.keys(topics).length);
    $('assumption-count-badge').textContent = String(assumptions.length);

    renderStoryCards();
    renderCategoryBar();
    populateTopicSelect();
    populateAssumptionFilters();

    focusedAssumption = params.get('assumption') || '';
    showAssumptions();
    renderProvenanceTable();

    const rawCase = params.get('case');
    goTab(params.get('tab') || 'findings', false);
    pick(params.get('topic') || 'access', rawCase === null ? undefined : Number(rawCase), false);

    if (focusedAssumption) {
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
      } catch {
        window.prompt('Copy:', location.href);
      }
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

    new ResizeObserver(plot).observe($('chart').parentElement);
  } catch (error) {
    $('load-error').hidden = false;
    $('load-error').textContent = T().loadError;
    console.error(error);
  }
}

start();
