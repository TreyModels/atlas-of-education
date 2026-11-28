/* Heatmap of the 1,024-setting sweep over two chosen parameters.
 * Expects data.json to hold per-setting results as data.sweep: an array of
 * objects, one per saved setting, whose keys other than "value" are parameter
 * values and whose "value" is the saved outcome (percent).
 * Each cell is the mean of the saved outcome across all other parameters.
 * data.json currently holds only band summaries for this sweep, so the module
 * shows a "not available" note rather than inventing a grid.
 * Clicking a cell dispatches CustomEvent 'gz:select-setting' on document with
 * detail {params, value}. */
(function () {
  'use strict';

  /* Viridis-like stops: colour-blind safe, perceptually ordered. */
  var PALETTE = [
    [68, 1, 84], [59, 82, 139], [33, 145, 140], [94, 201, 98], [253, 231, 37]
  ];

  var STR = {
    en: {
      heading: 'Whole-sweep heatmap',
      intro: 'Pick two parameters. Each square is the average saved outcome across all other settings. Select a square to load that setting into the sorter above.',
      rows: 'Rows',
      cols: 'Columns',
      noSweep: 'Not available in saved results. data.json holds band summaries for the 1,024-setting sweep, not a saved outcome for each setting. A two-parameter grid would need invented values, so none is drawn.',
      noParams: 'Fewer than two saved parameters are available, so a two-parameter grid cannot be drawn.',
      noCell: 'No saved setting for this combination',
      cellLabel: '{a}: {av}, {b}: {bv}. Mean saved outcome {v}% across {n} settings. Select to load.',
      selected: 'Selected {a} = {av}, {b} = {bv}. Mean {v}%.',
      legend: 'Mean saved outcome (%)',
      low: 'Lower',
      high: 'Higher',
      loadFail: 'Saved results could not be loaded. Open this page over http(s), not as a local file.',
      scrollHint: 'Swipe sideways to see every column.'
    },
    'zh-Hans': {
      heading: '全部设定的热力图',
      intro: '选择两个参数。每个方格是其他所有设定上已保存结果的平均值。点击方格，即可将该设定载入上方的分流模拟。',
      rows: '行',
      cols: '列',
      noSweep: '已保存结果中没有此项数据。data.json 只保存了 1,024 组设定的区间汇总，没有每组设定各自的结果。若要画两参数网格，就必须编造数字，因此不绘制。',
      noParams: '可用的已保存参数不足两个，无法绘制两参数网格。',
      noCell: '此参数组合没有已保存的设定',
      cellLabel: '{a}：{av}，{b}：{bv}。已保存结果均值 {v}%，基于 {n} 组设定。选择即可载入。',
      selected: '已选择 {a} = {av}，{b} = {bv}。均值 {v}%。',
      legend: '已保存结果均值（%）',
      low: '低',
      high: '高',
      loadFail: '无法加载已保存的结果。请通过 http(s) 打开此页面，而非直接以本地文件打开。',
      scrollHint: '左右滑动可查看所有列。'
    }
  };

  var state = { data: null, failed: false, rowParam: null, colParam: null, status: '' };

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

  function loadData() {
    return fetch('data.json').then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    });
  }

  function sweepRows() {
    var rows = state.data && Array.isArray(state.data.sweep) ? state.data.sweep : [];
    return rows.filter(function (r) { return r && typeof r.value === 'number' && isFinite(r.value); });
  }

  function paramNames(rows) {
    var names = [];
    rows.forEach(function (r) {
      Object.keys(r).forEach(function (k) { if (k !== 'value' && names.indexOf(k) < 0) names.push(k); });
    });
    return names;
  }

  function uniqueValues(rows, name) {
    var vals = [];
    rows.forEach(function (r) {
      if (r[name] !== undefined && vals.indexOf(r[name]) < 0) vals.push(r[name]);
    });
    return vals.sort(function (a, b) { return a < b ? -1 : a > b ? 1 : 0; });
  }

  function colourFor(t) {
    t = Math.max(0, Math.min(1, t));
    var seg = t * (PALETTE.length - 1);
    var i = Math.min(PALETTE.length - 2, Math.floor(seg));
    var f = seg - i;
    var a = PALETTE[i], b = PALETTE[i + 1];
    var rgb = [0, 1, 2].map(function (k) { return Math.round(a[k] + (b[k] - a[k]) * f); });
    return rgb;
  }

  function luminance(rgb) {
    var c = rgb.map(function (v) {
      var x = v / 255;
      return x <= 0.03928 ? x / 12.92 : Math.pow((x + 0.055) / 1.055, 2.4);
    });
    return 0.2126 * c[0] + 0.7152 * c[1] + 0.0722 * c[2];
  }

  function textOn(rgb) {
    var L = luminance(rgb);
    var white = 1.05 / (L + 0.05);
    var ink = (L + 0.05) / (luminance([21, 36, 39]) + 0.05);
    return white >= ink ? '#ffffff' : '#152427';
  }

  function selectParam(labelText, names, current, onChange) {
    var wrap = el('label', 'viz-label', labelText + ' ');
    var sel = el('select', 'viz-select hm-select');
    names.forEach(function (n) {
      var o = el('option', null, n);
      o.value = n;
      if (n === current) o.selected = true;
      sel.appendChild(o);
    });
    sel.addEventListener('change', function () { onChange(sel.value); });
    wrap.appendChild(sel);
    return wrap;
  }

  function render() {
    var root = document.getElementById('heatmap-root');
    if (!root) return;
    var s = S();
    root.replaceChildren();

    var card = el('section', 'viz-card hm-card');
    card.setAttribute('aria-labelledby', 'hm-heading');
    var h = el('h3', null, s.heading); h.id = 'hm-heading';
    card.appendChild(h);
    card.appendChild(el('p', 'viz-lead', s.intro));

    if (state.failed || !state.data) {
      card.appendChild(el('p', 'viz-note', s.loadFail));
      root.appendChild(card);
      return;
    }

    var rows = sweepRows();
    if (!rows.length) {
      card.appendChild(el('p', 'viz-note', s.noSweep));
      root.appendChild(card);
      return;
    }
    var names = paramNames(rows);
    if (names.length < 2) {
      card.appendChild(el('p', 'viz-note', s.noParams));
      root.appendChild(card);
      return;
    }

    if (names.indexOf(state.rowParam) < 0) state.rowParam = names[0];
    if (names.indexOf(state.colParam) < 0 || state.colParam === state.rowParam) {
      state.colParam = names[0] === state.rowParam ? names[1] : names[0];
    }

    var controls = el('div', 'hm-controls');
    controls.appendChild(selectParam(s.rows, names, state.rowParam, function (v) {
      state.rowParam = v; state.status = ''; render();
    }));
    controls.appendChild(selectParam(s.cols, names, state.colParam, function (v) {
      state.colParam = v; state.status = ''; render();
    }));
    card.appendChild(controls);

    var rVals = uniqueValues(rows, state.rowParam);
    var cVals = uniqueValues(rows, state.colParam);

    /* Cell = mean of saved outcome over all other parameters. */
    var acc = {};
    var lo = Infinity, hi = -Infinity;
    rows.forEach(function (r) {
      var key = r[state.rowParam] + '\u0001' + r[state.colParam];
      if (!acc[key]) acc[key] = { sum: 0, n: 0 };
      acc[key].sum += r.value; acc[key].n += 1;
    });
    Object.keys(acc).forEach(function (k) {
      acc[k].mean = acc[k].sum / acc[k].n;
      lo = Math.min(lo, acc[k].mean); hi = Math.max(hi, acc[k].mean);
    });

    var scroll = el('div', 'hm-scroll');
    scroll.setAttribute('tabindex', '0');
    scroll.appendChild(el('p', 'hm-hint', s.scrollHint));
    var grid = el('div', 'hm-grid');
    grid.setAttribute('role', 'group');
    grid.setAttribute('aria-label', fill('{r} × {c}', { r: state.rowParam, c: state.colParam }));
    grid.style.gridTemplateColumns = 'max-content repeat(' + cVals.length + ', minmax(44px, 1fr))';

    grid.appendChild(el('span', 'hm-corner', state.rowParam + ' \\ ' + state.colParam));
    cVals.forEach(function (c) { grid.appendChild(el('span', 'hm-head', String(c))); });

    rVals.forEach(function (r) {
      grid.appendChild(el('span', 'hm-rowhead', String(r)));
      cVals.forEach(function (c) {
        var a = acc[r + '\u0001' + c];
        if (!a) {
          var empty = el('span', 'hm-cell hm-empty', '–');
          empty.setAttribute('aria-label', s.noCell + ': ' + state.rowParam + ' ' + r + ', ' + state.colParam + ' ' + c);
          grid.appendChild(empty);
          return;
        }
        var t = hi > lo ? (a.mean - lo) / (hi - lo) : 0.5;
        var rgb = colourFor(t);
        var btn = el('button', 'hm-cell', a.mean.toFixed(1));
        btn.type = 'button';
        btn.style.background = 'rgb(' + rgb.join(',') + ')';
        btn.style.color = textOn(rgb);
        btn.setAttribute('aria-label', fill(s.cellLabel, {
          a: state.rowParam, av: r, b: state.colParam, bv: c, v: a.mean.toFixed(1), n: a.n
        }));
        btn.addEventListener('click', function () {
          var params = {};
          params[state.rowParam] = r;
          params[state.colParam] = c;
          state.status = fill(s.selected, { a: state.rowParam, av: r, b: state.colParam, bv: c, v: a.mean.toFixed(1) });
          document.dispatchEvent(new CustomEvent('gz:select-setting', {
            detail: { params: params, value: a.mean }
          }));
          var st = document.getElementById('hm-status');
          if (st) st.textContent = state.status;
        });
        grid.appendChild(btn);
      });
    });
    scroll.appendChild(grid);
    card.appendChild(scroll);

    /* Legend: gradient plus text end labels (colour is not the only cue). */
    var legend = el('div', 'hm-legend');
    legend.appendChild(el('p', 'hm-legend-title', s.legend));
    var bar = el('div', 'hm-bar');
    bar.setAttribute('aria-hidden', 'true');
    bar.style.background = 'linear-gradient(to right, ' + PALETTE.map(function (p) {
      return 'rgb(' + p.join(',') + ')';
    }).join(', ') + ')';
    legend.appendChild(bar);
    var ends = el('div', 'hm-ends');
    ends.appendChild(el('span', null, s.low + ' ' + (isFinite(lo) ? lo.toFixed(1) : '')));
    ends.appendChild(el('span', null, s.high + ' ' + (isFinite(hi) ? hi.toFixed(1) : '')));
    legend.appendChild(ends);
    card.appendChild(legend);

    var status = el('p', 'hm-status', state.status);
    status.id = 'hm-status';
    status.setAttribute('role', 'status');
    card.appendChild(status);

    root.appendChild(card);
  }

  function init() {
    var root = document.getElementById('heatmap-root');
    if (!root) return;
    if (!state.data && !state.failed) {
      loadData().then(function (d) {
        state.data = d;
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
