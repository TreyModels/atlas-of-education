/* Guangzhou explorer: hero "sorting machine".
 * Stylized replay of SAVED aggregate results (data.json). No per-pupil
 * outcomes exist in the saved file, so every dot is a sampled stand-in whose
 * group shares match the saved rates.
 * Plain JS, no build step. Mounts into #sorter-root.
 */
(function () {
  'use strict';

  // Saved headline numbers (data.json):
  //  poorRate / richRate: access.cases[2] ("Top 10% ability · bottom and top 40%
  //  of wealth", local-hukou pupils), selective-university proxy, in percent / 100.
  //  ratios: fairness.cases[0..2].values[0] (standardized richer-to-poorer ratios).
  //  drShift: restriction.cases[2] (default case, junior 0.075 · senior 0.05 score
  //  gain), mean paired change for poorer local pupils in the top ability tenth,
  //  in percentage points (converted to a fraction here, / 100).
  //  [0] uniform cut ("Cut equally borne"), [1] richer families mostly evade.
  var SAVED = {
    poorRate: 0.658117,
    richRate: 0.818206,
    ratios: [0.912502, 1.166706, 1.369075],
    drShift: [0.25244 / 100, 0.02126 / 100]
  };

  var MODES = [
    { ratio: SAVED.ratios[0], label: 'modeEntrance', cap: 'cap0' },
    { ratio: SAVED.ratios[1], label: 'modeJoint', cap: 'cap1' },
    { ratio: SAVED.ratios[2], label: 'modeAbility', cap: 'cap2', raw: true }
  ];

  // Double-reduction states: 0 off, 1 uniform cut, 2 richer families evade.
  var DR_COUNT = 3;

  // Two groups only: poorer 40% and richer 40% of local pupils (the middle 20%
  // is outside the rich-to-poor contrast in the paper).
  var GROUPS = [
    { key: 'gPoor', color: '#13857a' },
    { key: 'gRich', color: '#e8793a' }
  ];
  // Two baskets: the saved selective-university proxy share, and everyone else.
  var BASKET_COUNT = 2;
  var BX = [0.3, 0.7];
  var BASKET_HALF = 0.19;
  var GATE_Y = [0.18, 0.36, 0.54];
  var GATE_LABEL = ['bandTutoring', 'bandSchool', 'bandScore'];
  var LANE_Y = 0.66;
  var BASKET_TOP = 0.8;
  var BASKET_BOTTOM = 0.96;
  var SEED = 2201;

  var STR = {
    en: {
      badge: 'Stylized replay of saved results. Each dot is a sample pupil; group shares match saved rates, not individual pupil records.',
      sample: 'Source: data.json. The saved file gives raw rates only for starting ability (65.8% poorer, 81.8% richer, top 10% ability). For the entrance-score and joint views, the dots are matched to the saved standardized ratios applied to the poorer rate. The sample is drawn from these rates.',
      sortBy: 'Sort by',
      dr: 'Double reduction',
      drOff: 'Off',
      drUni: 'Uniform cut',
      drEvade: 'Richer families evade',
      drNote1: 'Stylized mechanism, not an estimate of the real policy effect. Saved paired change in the poorer group’s selective-university proxy rate under a 40% pre-gate cut, uniform enforcement: +0.25 percentage points (data.json, restriction, default case). The richer group is not changed because no saved richer-group change exists.',
      drNote2: 'Stylized mechanism, not an estimate of the real policy effect. Saved paired change in the poorer group’s selective-university proxy rate under a 40% pre-gate cut, wealthier families mostly evading: +0.02 percentage points (data.json, restriction, default case). The richer group is not changed because no saved richer-group change exists.',
      play: 'Play',
      pause: 'Pause',
      replay: 'Replay',
      modeEntrance: 'Entrance score',
      modeJoint: 'Score + ability',
      modeAbility: 'Starting ability',
      bandTutoring: 'Tutoring',
      bandSchool: 'School type',
      bandScore: 'Entrance score',
      bName0: 'Selective university (proxy)',
      bName1: 'Not selective',
      gPoor: 'Poorer 40%',
      gRich: 'Richer 40%',
      cap0: 'Similar entrance scores: richer-to-poorer ratio {r} (saved, standardized). Family advantage is largely already in the exam score.',
      cap1: 'Similar scores and starting ability: ratio {r} (saved, standardized).',
      cap2: 'Similar starting ability: ratio {r} (saved, standardized). The raw rates behind this view are 65.8% poorer and 81.8% richer, a smaller raw gap than the standardized ratio.',
      ratioLabel: 'Ratio sequence',
      canvasLabel: 'Animated sorting of simulated pupils into two baskets: selective university proxy and not selective. The shares are given in the text below.',
      summaryLine: '{b}: poorer {p}, richer {r}.'
    },
    'zh-Hans': {
      badge: '已保存结果的程式化回放。每个点是一名抽样学生；群体比例与已保存比率一致，并非个体学生记录。',
      sample: '来源：data.json。已保存文件仅在“初始能力”视图给出原始比率（前 10% 能力，贫困 65.8%，富裕 81.8%）。中考成绩与综合视图中，各点按已保存的标准化比值，在贫困组比率上匹配。抽样依据这些比率。',
      sortBy: '排序依据',
      dr: '双减',
      drOff: '关',
      drUni: '平等削减',
      drEvade: '富裕家庭规避',
      drNote1: '程式化机制，并非对真实政策效果的估计。已保存的配对变化：在升学前削减 40% 的情形下，贫困组重点大学代理比率上升 0.25 个百分点（平等执行；data.json，restriction，默认情形）。富裕组未作改动，因已保存结果中没有富裕组的变化。',
      drNote2: '程式化机制，并非对真实政策效果的估计。已保存的配对变化：在升学前削减 40% 的情形下，富裕家庭大多规避时，贫困组重点大学代理比率上升 0.02 个百分点（data.json，restriction，默认情形）。富裕组未作改动，因已保存结果中没有富裕组的变化。',
      play: '播放',
      pause: '暂停',
      replay: '重播',
      modeEntrance: '中考成绩',
      modeJoint: '成绩 + 能力',
      modeAbility: '初始能力',
      bandTutoring: '课外辅导',
      bandSchool: '学校类型',
      bandScore: '中考成绩',
      bName0: '重点大学（代理）',
      bName1: '非重点',
      gPoor: '贫困 40%',
      gRich: '富裕 40%',
      cap0: '中考成绩相近：富裕与贫困家庭的比值为 {r}（已保存，标准化）。家庭优势大多已体现在考试成绩中。',
      cap1: '成绩与初始能力相近：比值为 {r}（已保存，标准化）。',
      cap2: '初始能力相近：比值为 {r}（已保存，标准化）。该视图的原始比率为贫困 65.8%、富裕 81.8%，原始差距小于标准化比值。',
      ratioLabel: '比值序列',
      canvasLabel: '模拟学生被分流到两个去向的动画：重点大学代理与非重点。具体比例见下方文字。',
      summaryLine: '{b}：贫困 {p}，富裕 {r}。'
    }
  };

  var state = {
    lang: 'en',
    mode: 0,
    dr: 0,
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
    groupDone: [0, 0],
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

  // Selective-university shares per group [poorer, richer] for a mode and
  // double-reduction state. The saved shift applies to the poorer group only;
  // the richer group keeps its saved or saved-ratio value.
  function rates(mode, dr) {
    var poorBase = SAVED.poorRate;
    var rich = MODES[mode].raw ? SAVED.richRate : MODES[mode].ratio * SAVED.poorRate;
    var poor = poorBase;
    if (dr > 0) poor = Math.min(1, poorBase + SAVED.drShift[dr - 1]);
    return [poor, rich];
  }

  function makeDots(n) {
    var rnd = seeded(SEED);
    var nPoor = Math.floor(n / 2);
    var groups = [];
    var i;
    for (i = 0; i < nPoor; i++) groups.push(0);
    for (i = nPoor; i < n; i++) groups.push(1);
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
  // across settings); the rest go to the not-selective basket. Counts are exact
  // per group.
  function assignBaskets() {
    var r = rates(state.mode, state.dr);
    for (var g = 0; g < 2; g++) {
      var m = state.dots.filter(function (d) { return d.g === g; });
      m.sort(function (a, b) { return a.u - b.u; });
      var nSel = Math.round(r[g] * m.length);
      for (var i = 0; i < m.length; i++) m[i].b = i < nSel ? 0 : 1;
    }
  }

  function side(d, k) {
    return (d.bits[k] ? 0.34 : 0.66) + (d.j[k] - 0.5) * 0.12;
  }

  function finalPos(d) {
    return { x: BX[d.b] + (d.j[3] - 0.5) * 0.2, y: 0.84 + d.j[2] * 0.1 };
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
    for (var b = 0; b < BASKET_COUNT; b++) cnt.push([0, 0]);
    var gDone = [0, 0];
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
    var tot = [0, 0];
    var b;
    for (b = 0; b < BASKET_COUNT; b++) cnt.push([0, 0]);
    state.dots.forEach(function (d) {
      cnt[d.b][d.g]++;
      tot[d.g]++;
    });
    var out = [];
    for (b = 0; b < BASKET_COUNT; b++) {
      out.push([0, 1].map(function (g) {
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
      for (var g = 0; g < 2; g++) {
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
      ctx.strokeRect((BX[b] - BASKET_HALF) * W, BASKET_TOP * H, 2 * BASKET_HALF * W, (BASKET_BOTTOM - BASKET_TOP) * H);
    }
    ctx.restore();

    ctx.save();
    ctx.globalAlpha = 0.85;
    ctx.textAlign = 'center';
    ctx.textBaseline = 'bottom';
    for (b = 0; b < BASKET_COUNT; b++) {
      var lines = wrapLines(ctx, s['bName' + b], 2 * BASKET_HALF * W - 4);
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
        r: pct(shares[b][1])
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
    var drLabels = [s.drOff, s.drUni, s.drEvade];
    R.drBtns.forEach(function (btn, i) {
      btn.textContent = drLabels[i];
      btn.setAttribute('aria-pressed', state.dr === i ? 'true' : 'false');
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
    R.drNote.hidden = state.dr === 0;
    R.drNote.textContent = state.dr === 1 ? s.drNote1 : (state.dr === 2 ? s.drNote2 : '');
    for (var b = 0; b < BASKET_COUNT; b++) {
      R.bnames[b].textContent = s['bName' + b];
    }
    for (var g = 0; g < 2; g++) {
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

  function setDr(k) {
    state.dr = k;
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
    refs.gnames = [[], []];
    for (var b = 0; b < BASKET_COUNT; b++) {
      var card = el('div', 'sorter-basket');
      card.setAttribute('data-b', String(b));
      var h = el('h3', 'sorter-bname');
      refs.bnames.push(h);
      card.appendChild(h);
      var ul = el('ul', 'sorter-counts');
      refs.vals.push([]);
      for (var g = 0; g < 2; g++) {
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
    for (var k = 0; k < DR_COUNT; k++) {
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
      btn.addEventListener('click', function () { setDr(i); });
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
