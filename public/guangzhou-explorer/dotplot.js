/* Quantile dotplot of seed-to-seed variation for the 8-seed tutoring-choice runs.
 * Reads saved results from data.json. Dots are drawn only when a case carries
 * per-seed values (case.seeds: array of numbers). data.json stores mean, lowest
 * and highest seed per series, so otherwise a "not available" note is shown and
 * the saved figures are listed as text. No values are invented. */
(function () {
  'use strict';

  var SECTIONS = ['grade', 'calendar', 'wealth', 'fulltime', 'ranks'];
  var DOTS = 20;

  var STR = {
    en: {
      heading: 'How much does one result move from seed to seed?',
      intro: 'The tutoring-choice runs were repeated on eight matched cohorts (seeds 2201–2208), each with 40,000 simulated pupils. Only the random draw changes between seeds.',
      pick: 'Saved result',
      caption: 'Each dot is a 5% chance. Twenty dots stack from the lowest to the highest value. A taller stack means that value is more likely across the eight seeds.',
      noSeeds: 'Not available in saved results. The saved file keeps the mean, the lowest seed and the highest seed for each series, but not each seed’s own value. Dots would need invented values, so none are drawn. The saved figures are listed below.',
      expert: 'Exact saved figures (for experts)',
      mean: 'Mean of eight seeds',
      low: 'Lowest seed',
      high: 'Highest seed',
      axisNote: 'Scale runs from {d0} to {d1}.',
      svgLabel: 'Quantile dotplot of seed-to-seed variation: {s}',
      loadFail: 'Saved results could not be loaded. Open this page over http(s), not as a local file.',
      seriesNone: 'No series saved for this result.'
    },
    'zh-Hans': {
      heading: '同一设定在不同随机种子下波动多大？',
      intro: '补习选择实验在 8 组配对队列（种子 2201–2208）上重复运行，每组 40,000 名模拟学生。种子之间只有随机抽样不同。',
      pick: '已保存结果',
      caption: '每个点代表 5% 的可能性。20 个点从最低值排到最高值，堆叠越高，说明该值在 8 个种子中越常见。',
      noSeeds: '已保存结果中没有此项数据。文件只保存了每个序列的均值、最低种子值和最高种子值，没有每个种子各自的数值。若要画点，就必须编造数字，因此不绘制。已保存的数字列在下方。',
      expert: '已保存的精确数值（供专家查看）',
      mean: '八个种子的均值',
      low: '最低种子',
      high: '最高种子',
      axisNote: '刻度范围为 {d0} 至 {d1}。',
      svgLabel: '种子间波动的分位数点图：{s}',
      loadFail: '无法加载已保存的结果。请通过 http(s) 打开此页面，而非直接以本地文件打开。',
      seriesNone: '此结果没有保存的序列。'
    }
  };

  var state = { data: null, key: null, failed: false };

  function lang() {
    return /^zh/i.test(document.documentElement.lang || '') ? 'zh-Hans' : 'en';
  }
  function S() { return STR[lang()]; }

  function fill(tpl, vars) {
    return String(tpl).replace(/\{(\w+)\}/g, function (_, k) { return vars[k] != null ? vars[k] : ''; });
  }

  function el(tag, cls, text) {
    var n = document.createElement(tag);
    if (cls) n.className = cls;
    if (text != null) n.textContent = text;
    return n;
  }

  function svgEl(tag, attrs) {
    var n = document.createElementNS('http://www.w3.org/2000/svg', tag);
    Object.keys(attrs || {}).forEach(function (k) { n.setAttribute(k, attrs[k]); });
    return n;
  }

  function fmt(v) {
    if (v == null || isNaN(v)) return '—';
    return Number(v).toFixed(1);
  }

  function loadData() {
    return fetch('data.json').then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    });
  }

  /* Candidate results: every case in the 8-seed sections. */
  function options(data) {
    var out = [];
    SECTIONS.forEach(function (sk) {
      var sec = data[sk];
      if (!sec || !sec.cases) return;
      sec.cases.forEach(function (c, i) {
        out.push({ key: sk + '|' + i, section: sec, sectionKey: sk, c: c, label: sec.label + ' · ' + c.label });
      });
    });
    return out;
  }

  function quantile(sorted, p) {
    var h = (sorted.length - 1) * p;
    var lo = Math.floor(h), hi = Math.ceil(h);
    return sorted[lo] + (sorted[hi] - sorted[lo]) * (h - lo);
  }

  /* Quantile dotplot for one series: 20 dots, each the (i+0.5)/20 quantile. */
  function drawDots(seeds, dom, label) {
    var W = 320, R = 6, STEP = 2 * R + 2, BASE = 22;
    var d0 = dom[0], d1 = dom[1];
    var sorted = seeds.slice().sort(function (a, b) { return a - b; });
    var bins = {};
    var maxStack = 0;
    for (var i = 0; i < DOTS; i++) {
      var v = quantile(sorted, (i + 0.5) / DOTS);
      var px = Math.max(R, Math.min(W - R, ((v - d0) / (d1 - d0)) * (W - 2 * R) + R));
      var b = Math.round(px / STEP);
      bins[b] = (bins[b] || 0) + 1;
      maxStack = Math.max(maxStack, bins[b]);
    }
    var H = BASE + maxStack * STEP + 8;
    var svg = svgEl('svg', { viewBox: '0 0 ' + W + ' ' + H, class: 'dp-svg', role: 'img', preserveAspectRatio: 'xMidYMid meet' });
    svg.setAttribute('aria-label', fill(S().svgLabel, { s: label }));
    var seen = {};
    for (var j = 0; j < DOTS; j++) {
      var vj = quantile(sorted, (j + 0.5) / DOTS);
      var pxj = Math.max(R, Math.min(W - R, ((vj - d0) / (d1 - d0)) * (W - 2 * R) + R));
      var bj = Math.round(pxj / STEP);
      seen[bj] = (seen[bj] || 0) + 1;
      var cy = H - BASE - R - (seen[bj] - 1) * STEP;
      svg.appendChild(svgEl('circle', { cx: bj * STEP + R, cy: cy, r: R, class: 'dp-dot' }));
    }
    svg.appendChild(svgEl('line', { x1: 0, x2: W, y1: H - BASE + 4, y2: H - BASE + 4, class: 'dp-axis' }));
    var t0 = svgEl('text', { x: 0, y: H - 4, class: 'dp-tick' }); t0.textContent = fmt(d0);
    var t1 = svgEl('text', { x: W, y: H - 4, class: 'dp-tick', 'text-anchor': 'end' }); t1.textContent = fmt(d1);
    svg.appendChild(t0); svg.appendChild(t1);
    return svg;
  }

  function render() {
    var root = document.getElementById('dotplot-root');
    if (!root) return;
    var s = S();
    root.replaceChildren();

    var card = el('section', 'viz-card dp-card');
    card.setAttribute('aria-labelledby', 'dp-heading');
    var h = el('h3', null, s.heading); h.id = 'dp-heading';
    card.appendChild(h);
    card.appendChild(el('p', 'viz-lead', s.intro));

    if (state.failed || !state.data) {
      card.appendChild(el('p', 'viz-note', s.loadFail));
      root.appendChild(card);
      return;
    }

    var opts = options(state.data);
    var label = el('label', 'viz-label', s.pick + ' ');
    var sel = el('select', 'viz-select dp-select');
    sel.id = 'dp-select';
    opts.forEach(function (o) {
      var op = el('option', null, o.label);
      op.value = o.key;
      if (o.key === state.key) op.selected = true;
      sel.appendChild(op);
    });
    sel.addEventListener('change', function () { state.key = sel.value; render(); });
    label.appendChild(sel);
    card.appendChild(label);

    var cur = opts.filter(function (o) { return o.key === state.key; })[0] || opts[0];
    if (!cur) { card.appendChild(el('p', 'viz-note', s.noSeeds)); root.appendChild(card); return; }
    state.key = cur.key;

    var fig = el('figure', 'dp-figure');
    var plot = el('div', 'dp-plot');
    var seriesList = cur.section.series || [];
    var values = cur.c.values || [];
    var dom = cur.section.domain || [0, 100];

    /* seeds: flat array of per-seed values (one series) or an array of such arrays (one per series). */
    var seeds = cur.c.seeds;
    var perSeries = Array.isArray(seeds) && Array.isArray(seeds[0]) ? seeds : [seeds];
    if (Array.isArray(seeds) && seeds.length >= 2 && perSeries.every(function (a) { return a.length >= 2; })) {
      var rows = seriesList.length ? seriesList : [cur.c.label];
      rows.forEach(function (name, idx) {
        if (!perSeries[idx]) return;
        var row = el('div', 'dp-row');
        row.appendChild(el('p', 'dp-series', name));
        row.appendChild(drawDots(perSeries[idx], dom, name));
        plot.appendChild(row);
      });
    } else {
      plot.appendChild(el('p', 'viz-note', s.noSeeds));
    }
    fig.appendChild(plot);
    fig.appendChild(el('figcaption', 'dp-caption', s.caption));
    fig.appendChild(el('p', 'dp-scale', fill(s.axisNote, { d0: fmt(dom[0]), d1: fmt(dom[1]) })));
    card.appendChild(fig);

    var ex = el('details', 'viz-expert');
    ex.appendChild(el('summary', null, s.expert));
    if (!values.length) {
      ex.appendChild(el('p', null, s.seriesNone));
    } else {
      var dl = el('dl', 'dp-figures');
      values.forEach(function (v, i) {
        var block = el('div', 'dp-fig');
        block.appendChild(el('dt', null, seriesList[i] || cur.c.label));
        var dd = el('dd', null, s.mean + ': ' + fmt(v[0]) + ' · ' + s.low + ': ' + fmt(v[1]) + ' · ' + s.high + ': ' + fmt(v[2]));
        block.appendChild(dd);
        dl.appendChild(block);
      });
      ex.appendChild(dl);
    }
    card.appendChild(ex);
    root.appendChild(card);
  }

  function init() {
    var root = document.getElementById('dotplot-root');
    if (!root) return;
    if (!state.data && !state.failed) {
      loadData().then(function (d) {
        state.data = d;
        var first = options(d)[0];
        state.key = first ? first.key : null;
        render();
      }).catch(function () {
        state.failed = true;
        render();
      });
    }
    render();
    window.addEventListener('languagechange', render);
    if (typeof MutationObserver !== 'undefined') {
      new MutationObserver(render).observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
