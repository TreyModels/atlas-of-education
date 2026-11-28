/* Guangzhou explorer: hero "sorting machine".
 * Illustrative replay of SAVED aggregate results (data.json). No per-pupil
 * outcomes exist in the saved file, so every dot is a sampled stand-in.
 * Dots are assigned to baskets so that the shares match the saved rates.
 * Plain JS, no build step. Mounts into #sorter-root.
 */
(function () {
  'use strict';

  // Saved headline numbers (data.json):
  //  poorRate / richRate: access.cases[2] (top 10% starting ability, local pupils,
  //  bottom 40% vs top 40% of wealth), selective-university proxy, in percent / 100.
  //  ratios: fairness.cases[0..2].values[0] (standardized richer-to-poorer rate ratios).
  var SAVED = {
    poorRate: 0.658117,
    richRate: 0.818206,
    ratios: [0.912502, 1.166706, 1.369075]
  };

  var MODES = [
    { ratio: SAVED.ratios[0], label: 'modeEntrance', cap: 'cap0' },
    { ratio: SAVED.ratios[1], label: 'modeJoint', cap: 'cap1' },
    { ratio: SAVED.ratios[2], label: 'modeAbility', cap: 'cap2', raw: true }
  ];

  // Group indices: 0 poorer, 1 middle, 2 richer.
  var GROUPS = [
    { key: 'gPoor', color: '#13857a' },
    { key: 'gMid', color: '#9aa3ab' },
    { key: 'gRich', color: '#e8793a' }
  ];
  var BASKET_COUNT = 4;
  var BX = [0.125, 0.375, 0.625, 0.875];
  var GATE_Y = [0.18, 0.36, 0.54];
  var GATE_LABEL = ['bandTutoring', 'bandSchool', 'bandScore'];
  var LANE_Y = 0.66;
  var BASKET_TOP = 0.8;
  var BASKET_BOTTOM = 0.96;
  // Split of NON-selective pupils across the other baskets. Not in the saved
  // file; illustrative only.
  var OTHER_SPLIT = 0.35;
  var VOC_SPLIT = 0.30;
  var DR_SHIFT = 0.02; // illustrative double-reduction shift on selective shares
  var SEED = 2201;
  var SHARE = 0.4; // poorer and richer groups are each 40% of the sample

  var STR = {
    en: {
      badge: 'Illustrative replay of saved results (each dot is a sample pupil; shares match saved rates, not individual pupil records)',
      sample: 'Sample note: the saved file gives raw rates only for starting ability (65.8% poorer, 81.8% richer). For the other two views, dot rates are matched to the saved ratios on the same poorer base. The split of non-selective pupils is illustrative.',
      sortBy: 'Sort by',
      dr: 'Double reduction',
      drOff: 'Off',
      drOn: 'On',
      drNote: 'Illustrative only, not a saved run: On moves selective shares 2 points toward parity (poorer up, richer down).',
      play: 'Play',
      pause: 'Pause',
      replay: 'Replay',
      modeEntrance: 'Entrance score',
      modeJoint: 'Score + ability',
      modeAbility: 'Starting ability',
      bandTutoring: 'Tutoring',
      bandSchool: 'School type',
      bandScore: 'Entrance score',
      bName0: 'Selective university',
      bName1: 'Other university',
      bName2: 'Vocational',
      bName3: 'Out of track',
      gPoor: 'Poorer 40%',
      gMid: 'Middle 20%',
      gRich: 'Richer 40%',
      cap0: 'Similar entrance scores: richer-to-poorer ratio {r} (saved, standardized). Family advantage is largely already in the exam score.',
      cap1: 'Similar scores and starting ability: ratio {r} (saved, standardized).',
      cap2: 'Similar starting ability: ratio {r} (saved, standardized). The raw rates behind this view are 65.8% poorer and 81.8% richer, a smaller raw gap than the standardized ratio.',
      ratioLabel: 'Ratio sequence',
      canvasLabel: 'Animated sorting of simulated pupils into four baskets: selective university, other university, vocational and out of track. The shares are given in the text below.',
      summaryLine: '{b}: poorer {p}, middle {m}, richer {r}.'
    },
    'zh-Hans': {
      badge: '已保存结果的示意回放（每个点是一名抽样学生；比例与已保存结果一致，并非个体学生记录）',
      sample: '说明：已保存文件中，仅“初始能力”视图给出原始比率（贫困 65.8%，富裕 81.8%）。另外两个视图的点按已保存的比值，在同一贫困基数上匹配。非重点去向的划分仅为示意。',
      sortBy: '排序依据',
      dr: '双减',
      drOff: '关',
      drOn: '开',
      drNote: '仅为示意，并非已保存的运行结果：“开”会使重点大学比率向均等方向移动 2 个百分点（贫困组上升，富裕组下降）。',
      play: '播放',
      pause: '暂停',
      replay: '重播',
      modeEntrance: '中考成绩',
      modeJoint: '成绩 + 能力',
      modeAbility: '初始能力',
      bandTutoring: '课外辅导',
      bandSchool: '学校类型',
      bandScore: '中考成绩',
      bName0: '重点大学',
      bName1: '其他大学',
      bName2: '职业教育',
      bName3: '脱离升学轨道',
      gPoor: '贫困 40%',
      gMid: '中间 20%',
      gRich: '富裕 40%',
      cap0: '中考成绩相近：富裕与贫困家庭的比值为 {r}（已保存，标准化）。家庭优势大多已体现在考试成绩中。',
      cap1: '成绩与初始能力相近：比值为 {r}（已保存，标准化）。',
      cap2: '初始能力相近：比值为 {r}（已保存，标准化）。该视图的原始比率为贫困 65.8%、富裕 81.8%，原始差距小于标准化比值。',
      ratioLabel: '比值序列',
      canvasLabel: '模拟学生被分流到四个去向的动画：重点大学、其他大学、职业教育和脱离升学轨道。具体比例见下方文字。',
      summaryLine: '{b}：贫困 {p}，中间 {m}，富裕 {r}。'
    }
  };

  var state = {
    lang: 'en',
    mode: 0,
    dr: false,
    dots: [],
    N: 0,
    T: 0,
    running: false,
    reduced: false,
    allDone: false,
    inView: true,
    lastNow: 0,
    rafId: 0,
    frames: 0,
    W: 0,
    H: 0,
    ctx: null,
    canvas: null,
    root: null,
    ink: '#1c2430',
    font: 'system-ui, sans-serif',
    cntDone: [],
    groupDone: [0, 0, 0],
    refs: null
  };

  function normLang(l) {
    return /^zh/i.test(l || '') ? 'zh-Hans' : 'en';
  }

  function S() {
    return STR[state.lang];
  }

  function pct(x) {
    return (x * 100).toFixed(1) + '%';
  }

  function fmt(tpl, vars) {
    return tpl.replace(/\{(\w+)\}/g, function (_, k) {
      return vars[k] !== undefined ? vars[k] : '';
    });
  }

  function seeded(seed) {
    return function () {
      seed = (seed + 0x6d2b79f5) | 0;
      var t = Math.imul(seed ^ (seed >>> 15), 1 | seed);
      t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
      return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
    };
  }

  // Rates per group [poorer, middle, richer] for a mode and double-reduction setting.
  function rates(mode, dr) {
    var poor = SAVED.poorRate;
    var rich = MODES[mode].raw ? SAVED.richRate : MODES[mode].ratio * SAVED.poorRate;
    if (dr) {
      poor = Math.min(1, poor + DR_SHIFT);
      rich = Math.max(0, rich - DR_SHIFT);
    }
    return [poor, (poor + rich) / 2, rich];
  }

  function makeDots(n) {
    var rnd = seeded(SEED);
    var nPoor = Math.round(SHARE * n);
    var nRich = Math.round(SHARE * n);
    var nMid = n - nPoor - nRich;
    var groups = [];
    var i;
    for (i = 0; i < nPoor; i++) groups.push(0);
    for (i = 0; i < nMid; i++) groups.push(1);
    for (i = 0; i < nRich; i++) groups.push(2);
    for (i = groups.length - 1; i > 0; i--) {
      var k = Math.floor(rnd() * (i + 1));
      var tmp = groups[i];
      groups[i] = groups[k];
      groups[k] = tmp;
    }
    var dots = [];
    for (i = 0; i < n; i++) {
      dots.push({
        g: groups[i],
        u: rnd(),
        v: rnd(),
        d: rnd() * 2.4,
        bits: [rnd() < 0.5, rnd() < 0.5, rnd() < 0.5],
        j: [rnd(), rnd(), rnd(), rnd()],
        b: 0,
        x: 0.5,
        y: -0.04,
        active: false,
        wp: []
      });
    }
    return dots;
  }

  // Basket assignment: selective shares are the first nSel dots by u (nested
  // across settings); the rest are split by v. Counts are exact per group.
  function assignBaskets() {
    var r = rates(state.mode, state.dr);
    for (var g = 0; g < 3; g++) {
      var m = state.dots.filter(function (d) { return d.g === g; });
      m.sort(function (a, b) { return a.u - b.u; });
      var nSel = Math.round(r[g] * m.length);
      for (var i = 0; i < nSel; i++) m[i].b = 0;
      var rest = m.slice(nSel).sort(function (a, b) { return a.v - b.v; });
      var nOther = Math.round(OTHER_SPLIT * rest.length);
      var nVoc = Math.round(VOC_SPLIT * rest.length);
      for (var k = 0; k < rest.length; k++) {
        rest[k].b = k < nOther ? 1 : (k < nOther + nVoc ? 2 : 3);
      }
    }
  }

  function side(d, k) {
    return (d.bits[k] ? 0.34 : 0.66) + (d.j[k] - 0.5) * 0.12;
  }

  function finalPos(d) {
    return { x: BX[d.b] + (d.j[3] - 0.5) * 0.16, y: 0.84 + d.j[2] * 0.1 };
  }

  function spawnX(d) {
    return 0.5 + (d.j[0] - 0.5) * 0.1;
  }

  function pathFor(d, resort) {
    var fin = finalPos(d);
    if (resort) {
      return [{ x: 0.5 + (d.j[1] - 0.5) * 0.3, y: LANE_Y }, fin];
    }
    return [
      { x: side(d, 0), y: GATE_Y[0] },
      { x: side(d, 1), y: GATE_Y[1] },
      { x: side(d, 2), y: GATE_Y[2] },
      fin
    ];
  }

  function resetDots() {
    state.T = 0;
    state.allDone = false;
    state.dots.forEach(function (d) {
      d.active = false;
      d.x = spawnX(d);
      d.y = -0.04;
      d.wp = pathFor(d, false);
    });
  }

  function settleAll() {
    state.allDone = true;
    state.running = false;
    state.dots.forEach(function (d) {
      var f = finalPos(d);
      d.active = true;
      d.x = f.x;
      d.y = f.y;
      d.wp = [];
    });
    updateCounters();
    announce();
    draw();
  }

  // Advance physics by dt seconds. Returns true when every dot has arrived.
  function tick(dt) {
    state.T += dt;
    var pending = false;
    var a = 1 - Math.exp(-6 * dt);
    state.dots.forEach(function (d) {
      if (!d.active) {
        if (state.T >= d.d) {
          d.active = true;
          d.x = spawnX(d);
          d.y = -0.04;
        } else {
          pending = true;
          return;
        }
      }
      if (d.wp.length) {
        var tg = d.wp[0];
        d.x += (tg.x - d.x) * a;
        d.y += (tg.y - d.y) * a;
        if (Math.abs(tg.x - d.x) < 0.003 && Math.abs(tg.y - d.y) < 0.003) {
          d.wp.shift();
        }
        if (d.wp.length) pending = true;
      }
    });
    return !pending;
  }

  function computeCounts() {
    var cnt = [];
    for (var b = 0; b < BASKET_COUNT; b++) cnt.push([0, 0, 0]);
    var gDone = [0, 0, 0];
    state.dots.forEach(function (d) {
      if (d.active && !d.wp.length) {
        cnt[d.b][d.g]++;
        gDone[d.g]++;
      }
    });
    state.cntDone = cnt;
    state.groupDone = gDone;
  }

  // Expected final shares (complete sample, not only arrived dots).
  function finalShares() {
    var cnt = [];
    var tot = [0, 0, 0];
    var b;
    for (b = 0; b < BASKET_COUNT; b++) cnt.push([0, 0, 0]);
    state.dots.forEach(function (d) {
      cnt[d.b][d.g]++;
      tot[d.g]++;
    });
    var out = [];
    for (b = 0; b < BASKET_COUNT; b++) {
      out.push([0, 1, 2].map(function (g) {
        return tot[g] ? cnt[b][g] / tot[g] : 0;
      }));
    }
    return out;
  }

  function updateCounters() {
    if (!state.refs) return;
    computeCounts();
    var cnt = state.cntDone;
    var gDone = state.groupDone;
    for (var b = 0; b < BASKET_COUNT; b++) {
      for (var g = 0; g < 3; g++) {
        var el = state.refs.vals[b][g];
        el.textContent = gDone[g] ? pct(cnt[b][g] / gDone[g]) : '—';
      }
    }
  }

  function wrapLines(ctx, text, maxW) {
    if (ctx.measureText(text).width <= maxW) return [text];
    var words = text.split(' ');
    if (words.length < 2) return [text];
    var mid = Math.ceil(words.length / 2);
    return [words.slice(0, mid).join(' '), words.slice(mid).join(' ')];
  }

  function draw() {
    var ctx = state.ctx;
    if (!ctx) return;
    var W = state.W;
    var H = state.H;
    var s = S();
    ctx.clearRect(0, 0, W, H);
    ctx.font = '12px ' + state.font;
    ctx.textBaseline = 'middle';
    ctx.fillStyle = state.ink;
    ctx.strokeStyle = state.ink;

    // Stage gates and re-sort lane.
    ctx.save();
    ctx.setLineDash([4, 4]);
    ctx.globalAlpha = 0.28;
    GATE_Y.forEach(function (gy) {
      ctx.beginPath();
      ctx.moveTo(0, gy * H);
      ctx.lineTo(W, gy * H);
      ctx.stroke();
    });
    ctx.beginPath();
    ctx.moveTo(0, LANE_Y * H);
    ctx.lineTo(W, LANE_Y * H);
    ctx.stroke();
    ctx.restore();

    ctx.save();
    ctx.globalAlpha = 0.75;
    ctx.textAlign = 'left';
    GATE_Y.forEach(function (gy, k) {
      ctx.fillText(s[GATE_LABEL[k]], 6, gy * H - 9);
    });
    ctx.restore();

    // Baskets and names.
    ctx.save();
    ctx.globalAlpha = 0.5;
    ctx.lineWidth = 1;
    for (var b = 0; b < BASKET_COUNT; b++) {
      ctx.strokeRect((BX[b] - 0.1) * W, BASKET_TOP * H, 0.2 * W, (BASKET_BOTTOM - BASKET_TOP) * H);
    }
    ctx.restore();

    ctx.save();
    ctx.globalAlpha = 0.85;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'bottom';
    for (b = 0; b < BASKET_COUNT; b++) {
      var lines = wrapLines(ctx, s['bName' + b], 0.2 * W - 4);
      for (var i = 0; i < lines.length; i++) {
        ctx.fillText(lines[i], BX[b] * W, BASKET_TOP * H - 4 - (lines.length - 1 - i) * 14);
      }
    }
    ctx.restore();

    // Dots.
    var r = W < 700 ? 2.4 : 2.8;
    ctx.save();
    ctx.globalAlpha = 0.88;
    state.dots.forEach(function (d) {
      if (!d.active) return;
      ctx.fillStyle = GROUPS[d.g].color;
      ctx.beginPath();
      ctx.arc(d.x * W, d.y * H, r, 0, Math.PI * 2);
      ctx.fill();
    });
    ctx.restore();
  }

  function canRun() {
    return state.running && !state.reduced && !state.allDone && state.inView && !document.hidden;
  }

  function syncLoop() {
    if (canRun() && !state.rafId) {
      state.lastNow = 0;
      state.rafId = requestAnimationFrame(frame);
    }
  }

  function frame(now) {
    state.rafId = 0;
    if (!canRun()) return;
    // Cap work at about 60 fps.
    if (state.lastNow && now - state.lastNow < 15) {
      state.rafId = requestAnimationFrame(frame);
      return;
    }
    var dt = state.lastNow ? Math.min(0.05, (now - state.lastNow) / 1000) : 0.016;
    state.lastNow = now;
    var done = tick(dt);
    state.frames++;
    if (state.frames % 6 === 0 || done) updateCounters();
    draw();
    if (done) {
      state.running = false;
      state.allDone = true;
      updateCounters();
      announce();
      renderControls();
      return;
    }
    state.rafId = requestAnimationFrame(frame);
  }

  function announce() {
    if (!state.refs) return;
    var s = S();
    var shares = finalShares();
    var parts = [];
    for (var b = 0; b < BASKET_COUNT; b++) {
      parts.push(fmt(s.summaryLine, {
        b: s['bName' + b],
        p: pct(shares[b][0]),
        m: pct(shares[b][1]),
        r: pct(shares[b][2])
      }));
    }
    state.refs.summary.textContent = parts.join(' ');
  }

  function renderControls() {
    if (!state.refs) return;
    var s = S();
    var R = state.refs;
    R.toggle.textContent = state.running ? s.pause : s.play;
    R.replay.textContent = s.replay;
    R.modeBtns.forEach(function (btn, i) {
      btn.textContent = s[MODES[i].label];
      btn.setAttribute('aria-pressed', state.mode === i ? 'true' : 'false');
    });
    R.drBtns.forEach(function (btn, i) {
      btn.textContent = i === 0 ? s.drOff : s.drOn;
      btn.setAttribute('aria-pressed', (state.dr === (i === 1)) ? 'true' : 'false');
    });
  }

  function renderText() {
    if (!state.refs) return;
    var s = S();
    var R = state.refs;
    R.root.querySelectorAll('[data-s]').forEach(function (el) {
      el.textContent = s[el.getAttribute('data-s')];
    });
    R.canvas.setAttribute('aria-label', s.canvasLabel);
    var m = MODES[state.mode];
    R.caption.textContent = fmt(s[m.cap], { r: m.ratio.toFixed(2) });
    R.ratioVals.forEach(function (el, i) {
      el.textContent = MODES[i].ratio.toFixed(2);
      el.classList.toggle('is-on', i === state.mode);
    });
    R.drNote.hidden = !state.dr;
    R.drNote.textContent = state.dr ? s.drNote : '';
    for (var b = 0; b < BASKET_COUNT; b++) {
      R.bnames[b].textContent = s['bName' + b];
    }
    for (var g = 0; g < 3; g++) {
      R.gnames[g].forEach(function (el) { el.textContent = s[GROUPS[g].key]; });
    }
    renderControls();
  }

  function renderAll() {
    renderText();
    updateCounters();
    draw();
  }

  function onLang(e) {
    var l = (e && e.detail && e.detail.lang) || document.documentElement.lang;
    state.lang = normLang(l);
    renderAll();
    announce();
  }

  function setMode(m) {
    state.mode = m;
    afterChange();
  }

  function setDr(on) {
    state.dr = on;
    afterChange();
  }

  function afterChange() {
    assignBaskets();
    if (state.reduced) {
      settleAll();
    } else {
      state.dots.forEach(function (d) {
        if (!d.active) {
          d.active = true;
          d.x = spawnX(d);
          d.y = -0.04;
        }
        d.wp = pathFor(d, true);
      });
      state.allDone = false;
      state.running = true;
      syncLoop();
    }
    renderAll();
  }

  function replay() {
    if (state.reduced) {
      settleAll();
    } else {
      resetDots();
      state.running = true;
      syncLoop();
    }
    renderAll();
  }

  function togglePlay() {
    if (state.allDone) {
      replay();
      return;
    }
    state.running = !state.running;
    syncLoop();
    renderControls();
  }

  function resizeCanvas() {
    var c = state.canvas;
    var root = state.root;
    var W = c.clientWidth;
    var H = c.clientHeight;
    if (!W || !H) return;
    var dpr = Math.min(window.devicePixelRatio || 1, 2);
    c.width = Math.round(W * dpr);
    c.height = Math.round(H * dpr);
    state.ctx = c.getContext('2d');
    state.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    state.W = W;
    state.H = H;
    var cs = window.getComputedStyle(root);
    state.ink = cs.color || state.ink;
    state.font = cs.fontFamily || state.font;
    draw();
  }

  function buildDots() {
    var n = window.innerWidth < 700 ? 600 : 1500;
    state.N = n;
    state.dots = makeDots(n);
    assignBaskets();
  }

  function el(tag, cls, text) {
    var e = document.createElement(tag);
    if (cls) e.className = cls;
    if (text !== undefined) e.textContent = text;
    return e;
  }

  function buildDOM(root) {
    var refs = {};
    var section = el('section', 'sorter');
    section.setAttribute('aria-label', 'Sorting machine');

    var badge = el('p', 'sorter-badge');
    badge.setAttribute('data-s', 'badge');
    section.appendChild(badge);

    var stage = el('div', 'sorter-stage');
    var canvas = el('canvas', 'sorter-canvas');
    canvas.setAttribute('role', 'img');
    stage.appendChild(canvas);
    section.appendChild(stage);

    var baskets = el('div', 'sorter-baskets');
    refs.bnames = [];
    refs.vals = [];
    refs.gnames = [[], [], []];
    for (var b = 0; b < BASKET_COUNT; b++) {
      var card = el('div', 'sorter-basket');
      card.setAttribute('data-b', String(b));
      var h = el('h3', 'sorter-bname');
      refs.bnames.push(h);
      card.appendChild(h);
      var ul = el('ul', 'sorter-counts');
      refs.vals.push([]);
      for (var g = 0; g < 3; g++) {
        var li = el('li', 'sorter-row');
        var sw = el('span', 'sorter-sw');
        sw.style.background = GROUPS[g].color;
        var gn = el('span', 'sorter-gname');
        refs.gnames[g].push(gn);
        var val = el('span', 'sorter-val', '—');
        refs.vals[b].push(val);
        li.appendChild(sw);
        li.appendChild(gn);
        li.appendChild(val);
        ul.appendChild(li);
      }
      card.appendChild(ul);
      baskets.appendChild(card);
    }
    section.appendChild(baskets);

    var controls = el('div', 'sorter-controls');
    var row = el('div', 'sorter-actions');
    refs.toggle = el('button', 'sorter-btn sorter-btn--primary');
    refs.toggle.type = 'button';
    refs.replay = el('button', 'sorter-btn');
    refs.replay.type = 'button';
    row.appendChild(refs.toggle);
    row.appendChild(refs.replay);
    controls.appendChild(row);

    var sortGroup = el('div', 'sorter-group');
    var sortLabel = el('span', 'sorter-label');
    sortLabel.setAttribute('data-s', 'sortBy');
    sortGroup.appendChild(sortLabel);
    var seg1 = el('div', 'sorter-seg');
    seg1.setAttribute('role', 'group');
    refs.modeBtns = [];
    for (var m = 0; m < MODES.length; m++) {
      var mb = el('button', 'sorter-chip');
      mb.type = 'button';
      mb.setAttribute('data-mode', String(m));
      refs.modeBtns.push(mb);
      seg1.appendChild(mb);
    }
    sortGroup.appendChild(seg1);
    controls.appendChild(sortGroup);

    var drGroup = el('div', 'sorter-group');
    var drLabel = el('span', 'sorter-label');
    drLabel.setAttribute('data-s', 'dr');
    drGroup.appendChild(drLabel);
    var seg2 = el('div', 'sorter-seg');
    seg2.setAttribute('role', 'group');
    refs.drBtns = [];
    for (var k = 0; k < 2; k++) {
      var db = el('button', 'sorter-chip');
      db.type = 'button';
      db.setAttribute('data-dr', String(k));
      refs.drBtns.push(db);
      seg2.appendChild(db);
    }
    drGroup.appendChild(seg2);
    controls.appendChild(drGroup);
    section.appendChild(controls);

    var ratio = el('p', 'sorter-ratio');
    var rl = el('span', 'sorter-ratio-label');
    rl.setAttribute('data-s', 'ratioLabel');
    ratio.appendChild(rl);
    refs.ratioVals = [];
    for (var r = 0; r < MODES.length; r++) {
      if (r > 0) ratio.appendChild(el('span', 'sorter-arrow', ' → '));
      var rv = el('span', 'sorter-rv', '');
      refs.ratioVals.push(rv);
      ratio.appendChild(rv);
    }
    section.appendChild(ratio);

    refs.caption = el('p', 'sorter-caption');
    section.appendChild(refs.caption);

    refs.drNote = el('p', 'sorter-drnote');
    refs.drNote.hidden = true;
    section.appendChild(refs.drNote);

    refs.summary = el('p', 'sorter-summary');
    refs.summary.setAttribute('aria-live', 'polite');
    section.appendChild(refs.summary);

    var note = el('p', 'sorter-note');
    note.setAttribute('data-s', 'sample');
    section.appendChild(note);

    root.appendChild(section);
    refs.root = section;
    refs.canvas = canvas;
    return refs;
  }

  function mount() {
    var root = document.getElementById('sorter-root');
    if (!root) {
      var main = document.querySelector('main');
      root = el('div');
      root.id = 'sorter-root';
      if (main) main.insertBefore(root, main.firstChild);
      else document.body.appendChild(root);
    }
    state.root = root;
    state.lang = normLang(document.documentElement.lang);
    var mq = window.matchMedia ? window.matchMedia('(prefers-reduced-motion: reduce)') : null;
    state.reduced = !!(mq && mq.matches);

    state.refs = buildDOM(root);
    state.canvas = state.refs.canvas;
    buildDots();

    var R = state.refs;
    R.toggle.addEventListener('click', togglePlay);
    R.replay.addEventListener('click', replay);
    R.modeBtns.forEach(function (btn, i) {
      btn.addEventListener('click', function () { setMode(i); });
    });
    R.drBtns.forEach(function (btn, i) {
      btn.addEventListener('click', function () { setDr(i === 1); });
    });

    resizeCanvas();
    if (state.reduced) {
      state.dots.forEach(function (d) { d.active = true; });
      settleAll();
    } else {
      resetDots();
      state.running = true;
    }
    renderAll();
    syncLoop();

    var resizeTimer = 0;
    function onResize() {
      clearTimeout(resizeTimer);
      resizeTimer = setTimeout(function () {
        var n = window.innerWidth < 700 ? 600 : 1500;
        resizeCanvas();
        if (n !== state.N) {
          buildDots();
          if (state.reduced) settleAll();
          else replay();
        }
        renderAll();
      }, 150);
    }
    if (typeof ResizeObserver !== 'undefined') {
      new ResizeObserver(onResize).observe(R.canvas.parentNode);
    } else {
      window.addEventListener('resize', onResize);
    }

    if (mq) {
      var onMotion = function () {
        state.reduced = mq.matches;
        if (state.reduced) {
          settleAll();
        } else {
          replay();
        }
        renderAll();
      };
      if (mq.addEventListener) mq.addEventListener('change', onMotion);
      else if (mq.addListener) mq.addListener(onMotion);
    }

    document.addEventListener('visibilitychange', syncLoop);
    if (typeof IntersectionObserver !== 'undefined') {
      new IntersectionObserver(function (entries) {
        state.inView = entries[0].isIntersecting;
        syncLoop();
      }).observe(root);
    }

    window.addEventListener('languagechange', onLang);
    document.addEventListener('languagechange', onLang);
    if (typeof MutationObserver !== 'undefined') {
      new MutationObserver(function () { onLang(); })
        .observe(document.documentElement, { attributes: true, attributeFilter: ['lang'] });
    }
  }

  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', mount);
  } else {
    mount();
  }
})();
