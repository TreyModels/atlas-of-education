/* Heatmap of the 1,024-setting principal sweep over two chosen inputs.
 * Source: sweep.json, exported from research/guangzhou-working-paper/draws.csv.
 * Each setting's outcome is T (equal-talent richer-to-poorer rate ratio).
 * Each input is binned into four equal-width quartiles of its sampled range.
 * Each cell is the mean T across the settings in that pair of bins.
 * If sweep.json cannot be loaded, or holds no usable rows, the whole panel
 * stays hidden: no heading, no grid, and no notice. */
(function () {
  'use strict';

  /* Viridis-like stops: colour-blind safe, perceptually ordered. */
  var PALETTE = [
    [68, 1, 84], [59, 82, 139], [33, 145, 140], [94, 201, 98], [253, 231, 37]
  ];

  var STR = {
    en: {
      heading: 'Whole-sweep heatmap',
      intro: 'Pick two inputs. Each square is the mean equal-talent ratio T across the simulated settings in that pair of quartile bins. Bin 1 is the lowest quarter of an input’s sampled range.',
      rows: 'Rows',
      cols: 'Columns',
      noCell: 'No saved setting for this combination',
      cellLabel: '{a}: bin {av}, {b}: bin {bv}. Mean T {v} across {n} settings.',
      legend: 'Mean T (equal-talent richer-to-poorer ratio, 1,024 settings)',
      low: 'Lower',
      high: 'Higher',
      scrollHint: 'Swipe sideways to see every column.',
      source: 'Source: sweep.json (principal sweep, 1,024 independent settings, 40,000 synthetic pupils each).'
    },
    'zh-Hans': {
      heading: '全部设定的热力图',
      intro: '选择两个输入参数。每个方格是这一对四分位分段内的各组模拟设定的平均等能力比值 T。第 1 段为该输入抽样范围的最低四分之一。',
      rows: '行',
      cols: '列',
      noCell: '此参数组合没有已保存的设定',
      cellLabel: '{a}：第 {av} 段，{b}：第 {bv} 段。平均 T 为 {v}，基于 {n} 组设定。',
      legend: '平均 T（等能力富裕与贫困家庭比值，1,024 组设定）',
      low: '低',
      high: '高',
      scrollHint: '左右滑动可查看所有列。',
      source: '来源：sweep.json（主要模拟，1,024 组独立设定，每组 40,000 名模拟学生）。'
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
    return fetch('sweep.json').then(function (r) {
      if (!r.ok) throw new Error('HTTP ' + r.status);
      return r.json();
    });
  }

  /* Convert the compact [bin..., T] rows into one object per setting. */
  function sweepRows() {
    var d = state.data;
    if (!d || !Array.isArray(d.params) || !Array.isArray(d.rows)) return [];
    return d.rows.map(function (row) {
      var o = {};
      d.params.forEach(function (p, i) { o[p] = row[i]; });
      o.value = row[d.params.length];
      return o;
    }).filter(function (r) { return typeof r.value === 'number' && isFinite(r.value); });
  }

  function paramNames() {
    return state.data.params.slice();
  }

  function uniqueValues(rows, name) {
    var vals = [];
    rows.forEach(function (r) {
      if (r[name] !== undefined && vals.indexOf(r[name]) < 0) vals.push(r[name]);
    });
    return vals.sort(function (a, b) { return a - b; });
  }

  function colourFor(t) {
    t = Math.max(0, Math.min(1, t));
    var seg = t * (PALETTE.length - 1);
    var i = Math.min(PALETTE.length - 2, Math.floor(seg));
    var f = seg - i;
    var a = PALETTE[i], b = PALETTE[i + 1];
    return [0, 1, 2].map(function (k) { return Math.round(a[k] + (b[k] - a[k]) * f); });
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

  function hidePanel(root) {
    root.replaceChildren();
    root.hidden = true;
  }

  function render() {
    var root = document.getElementById('heatmap-root');
    if (!root) return;
    var s = S();
    var rows = (state.data && !state.failed) ? sweepRows() : [];
    if (!rows.length) {
      hidePanel(root);
      return;
    }
    root.hidden = false;
    root.replaceChildren();

    var card = el('section', 'viz-card hm-card');
    card.setAttribute('aria-labelledby', 'hm-heading');
    var h = el('h3', null, s.heading); h.id = 'hm-heading';
    card.appendChild(h);
    card.appendChild(el('p', 'viz-lead', s.intro));

    var names = paramNames();
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

    /* Cell = mean T over all settings in that pair of bins. */
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
        var btn = el('button', 'hm-cell', a.mean.toFixed(2));
        btn.type = 'button';
        btn.style.background = 'rgb(' + rgb.join(',') + ')';
        btn.style.color = textOn(rgb);
        btn.setAttribute('aria-label', fill(s.cellLabel, {
          a: state.rowParam, av: r, b: state.colParam, bv: c, v: a.mean.toFixed(2), n: a.n
        }));
        btn.addEventListener('click', function () {
          state.status = fill(s.cellLabel, {
            a: state.rowParam, av: r, b: state.colParam, bv: c, v: a.mean.toFixed(2), n: a.n
          });
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
    ends.appendChild(el('span', null, s.low + ' ' + lo.toFixed(2)));
    ends.appendChild(el('span', null, s.high + ' ' + hi.toFixed(2)));
    legend.appendChild(ends);
    card.appendChild(legend);

    card.appendChild(el('p', 'viz-note', s.source));

    var status = el('p', 'hm-status', state.status);
    status.id = 'hm-status';
    status.setAttribute('role', 'status');
    card.appendChild(status);

    root.appendChild(card);
  }

  function init() {
    var root = document.getElementById('heatmap-root');
    if (!root) return;
    root.hidden = true;
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
