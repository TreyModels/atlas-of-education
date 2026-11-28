/* Download buttons for the saved data and the sorter chart image.
 * - JSON and CSV export the saved summaries from data.json (every section
 *   shown on the page: centre, low and high per series, with the interval
 *   basis stated). If data.sweep exists (the heatmap source), the JSON also
 *   includes it.
 * - PNG exports the sorter canvas, if one is on the page. */
(function () {
  'use strict';

  var STR = {
    en: {
      heading: 'Download',
      intro: 'Saved numbers only, exactly as stored in data.json. Nothing is recalculated or simulated in your browser.',
      json: 'Download data (JSON)',
      csv: 'Download data (CSV)',
      png: 'Download chart image (PNG)',
      noCanvas: 'No chart image is on this page to save.',
      pngFail: 'The chart image could not be created in this browser.',
      loadFail: 'Saved results could not be loaded. Open this page over http(s), not as a local file.',
      ready: 'Preparing file…',
      done: 'Download started.'
    },
    'zh-Hans': {
      heading: '下载',
      intro: '仅为已保存的数字，与 data.json 中存储的内容一致。浏览器中不会重新计算或模拟。',
      json: '下载数据（JSON）',
      csv: '下载数据（CSV）',
      png: '下载图表图片（PNG）',
      noCanvas: '此页面上没有可保存的图表图片。',
      pngFail: '此浏览器无法生成图表图片。',
      loadFail: '无法加载已保存的结果。请通过 http(s) 打开此页面，而非直接以本地文件打开。',
      ready: '正在准备文件…',
      done: '下载已开始。'
    }
  };

  var SECTION_KEYS = ['access', 'fairness', 'fade', 'inputs', 'restriction', 'ranks', 'grade', 'calendar',
    'wealth', 'fulltime', 'schools', 'skills', 'hukou', 'ranks-legacy'];

  var state = { data: null, failed: false, status: '' };

  function lang() {
    return /^zh/i.test(document.documentElement.lang || '') ? 'zh-Hans' : 'en';
  }
  function S() { return STR[lang()]; }

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

  /* Flat rows: one per case and series. Values are [centre, low, high] as saved. */
  function flatRows(data) {
    var rows = [];
    SECTION_KEYS.forEach(function (sk) {
      var sec = data[sk];
      if (!sec || !Array.isArray(sec.cases)) return;
      sec.cases.forEach(function (c, ci) {
        (c.values || []).forEach(function (v, si) {
          rows.push({
            section: sk,
            section_label: sec.label,
            metric: sec.metric,
            interval_basis: sec.interval,
            case_id: c.id || String(ci),
            case_label: c.label,
            series: (sec.series && sec.series[si]) || '',
            centre: v[0],
            low: v[1],
            high: v[2],
            caption: c.caption || ''
          });
        });
      });
    });
    return rows;
  }

  function csvCell(v) {
    if (v === null || v === undefined) return '';
    var s = String(v);
    return /[",\n\r]/.test(s) ? '"' + s.replace(/"/g, '""') + '"' : s;
  }

  function toCSV(rows) {
    var cols = ['section', 'section_label', 'metric', 'interval_basis', 'case_id', 'case_label', 'series', 'centre', 'low', 'high', 'caption'];
    var lines = [cols.join(',')];
    rows.forEach(function (r) {
      lines.push(cols.map(function (c) { return csvCell(r[c]); }).join(','));
    });
    return lines.join('\r\n') + '\r\n';
  }

  function toJSON(data) {
    var out = { source: 'data.json', sections: {} };
    SECTION_KEYS.forEach(function (sk) {
      if (data[sk]) out.sections[sk] = data[sk];
    });
    if (data.sweep) out.sweep = data.sweep;
    return JSON.stringify(out, null, 2) + '\n';
  }

  function save(name, blob) {
    var url = URL.createObjectURL(blob);
    var a = document.createElement('a');
    a.href = url;
    a.download = name;
    document.body.appendChild(a);
    a.click();
    a.remove();
    setTimeout(function () { URL.revokeObjectURL(url); }, 1000);
  }

  function setStatus(text) {
    state.status = text;
    var st = document.getElementById('dl-status');
    if (st) st.textContent = text;
  }

  function downloadJSON() {
    save('gz-saved-data.json', new Blob([toJSON(state.data)], { type: 'application/json' }));
    setStatus(S().done);
  }

  function downloadCSV() {
    save('gz-saved-data.csv', new Blob([toCSV(flatRows(state.data))], { type: 'text/csv;charset=utf-8' }));
    setStatus(S().done);
  }

  function downloadPNG() {
    var canvas = document.querySelector('#sorter-root canvas');
    if (!canvas) { setStatus(S().noCanvas); return; }
    try {
      canvas.toBlob(function (blob) {
        if (!blob) { setStatus(S().pngFail); return; }
        save('gz-sorter-chart.png', blob);
        setStatus(S().done);
      }, 'image/png');
    } catch (e) {
      setStatus(S().pngFail);
    }
  }

  function render() {
    var root = document.getElementById('download-root');
    if (!root) return;
    var s = S();
    root.replaceChildren();

    var card = el('section', 'viz-card dl-card');
    card.setAttribute('aria-labelledby', 'dl-heading');
    var h = el('h3', null, s.heading); h.id = 'dl-heading';
    card.appendChild(h);
    card.appendChild(el('p', 'viz-lead', s.intro));

    var bar = el('div', 'dl-buttons');
    var disabled = !state.data;
    [['json', downloadJSON], ['csv', downloadCSV], ['png', downloadPNG]].forEach(function (pair) {
      var b = el('button', 'viz-button dl-button', s[pair[0]]);
      b.type = 'button';
      b.disabled = disabled;
      b.addEventListener('click', pair[1]);
      bar.appendChild(b);
    });
    card.appendChild(bar);

    if (state.failed) card.appendChild(el('p', 'viz-note', s.loadFail));
    var st = el('p', 'dl-status', state.status);
    st.id = 'dl-status';
    st.setAttribute('role', 'status');
    card.appendChild(st);

    root.appendChild(card);
  }

  function init() {
    var root = document.getElementById('download-root');
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
      new MutationObserver(function () { state.status = ''; render(); })
        .observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', init);
  } else {
    init();
  }
})();
