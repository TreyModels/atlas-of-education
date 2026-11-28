'use strict';

(function () {
  const TEAL = '#07665e';
  const TEAL_GLOW = 'rgba(7, 102, 94, 0.22)';
  const AMBER = '#aa4c28';
  const AMBER_GLOW = 'rgba(170, 76, 40, 0.22)';
  const SLATE = '#102f35';
  const GRID = '#d8e5e4';
  const MUTED = '#4b6064';

  let rafId = null;
  let progress = 0;
  let paused = false;
  let lastTs = 0;
  let currentCfg = null;

  const prefersReduced = () =>
    window.matchMedia && window.matchMedia('(prefers-reduced-motion: reduce)').matches;

  function renderFrame(canvas, cfg, t) {
    const w = Math.round(canvas.getBoundingClientRect().width);
    if (!w) return;
    const h = 265;
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    canvas.style.height = h + 'px';
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    const cx = canvas.getContext('2d');
    cx.scale(dpr, dpr);
    cx.fillStyle = '#fff';
    cx.fillRect(0, 0, w, h);
    const zh = cfg.lang === 'zh';
    const d = cfg.storyPaths.example_cohort_profiles;
    const compKey = cfg.compareMode === 'rich10_top10' ? 'rich10_top10' : 'rich10_p60';
    const rows = [[d.poor10_top10, zh ? '能力前10% · 财富后10%' : 'Top 10% ability · Bottom 10% wealth', TEAL]];
    if (cfg.showCompare) rows.push([d[compKey], compKey === 'rich10_top10'
      ? (zh ? '能力前10% · 财富前10%' : 'Top 10% ability · Top 10% wealth')
      : (zh ? '能力约第60百分位 · 财富前10%' : 'Around 60th percentile ability · Top 10% wealth'), AMBER]);
    const description = rows.map(([r,label]) => label + ': ' + r.selective_uni_pct + '% (n=' + r.n + ')');
    canvas.setAttribute('role', 'img');
    canvas.setAttribute('aria-label', description.join('. '));
    const pad = 18, width = w - 2 * pad;
    const progress = 1 - Math.pow(1 - t, 3);
    cx.fillStyle = SLATE;
    cx.font = '600 14px system-ui';
    cx.fillText(zh ? '一个保存队列中的模拟重点大学录取率' : 'Selective university proxy rate in one saved cohort', pad, 24, width);
    rows.forEach(([r,label,color], i) => {
      const y = 56 + i * 86;
      cx.fillStyle = SLATE;
      cx.font = '600 12px system-ui';
      cx.fillText(label, pad, y, width);
      cx.fillStyle = GRID;
      cx.fillRect(pad, y+8, width, 15);
      cx.fillStyle = color;
      cx.fillRect(pad, y+8, width * r.selective_uni_pct / 100 * progress, 15);
      cx.font = '600 13px system-ui';
      cx.fillText(r.selective_uni_pct.toFixed(1) + '%  ·  n = ' + r.n, pad, y+42, width);
    });
    cx.fillStyle = MUTED;
    cx.font = '12px system-ui';
    cx.fillText(zh ? '横条显示已保存的比例。动画仅逐步显示其长度。'
      : 'Bars reveal saved rates on a 0–100% scale.', pad, h-28, width);
  }

  function stepAnim(ts) {
    if (!currentCfg) return;
    if (!lastTs) lastTs = ts;
    const dt = (ts - lastTs) / 1000;
    lastTs = ts;
    if (!paused) {
      progress = Math.min(1, progress + dt / 1.25);
    }
    renderFrame(currentCfg.canvas, currentCfg, progress);
    if (progress < 1 && !paused) {
      rafId = requestAnimationFrame(stepAnim);
    } else {
      rafId = null;
    }
  }

  window.GZ_MC_CANVAS = {
    mount(canvas, cfg) {
      if (rafId) cancelAnimationFrame(rafId);
      currentCfg = { canvas, ...cfg };
      paused = false;
      lastTs = 0;
      progress = prefersReduced() ? 1 : 0.02;
      renderFrame(canvas, currentCfg, progress);
      if (progress < 1) rafId = requestAnimationFrame(stepAnim);
    },
    replay() {
      if (!currentCfg) return;
      if (rafId) cancelAnimationFrame(rafId);
      paused = false;
      lastTs = 0;
      progress = prefersReduced() ? 1 : 0.02;
      renderFrame(currentCfg.canvas, currentCfg, progress);
      if (progress < 1) rafId = requestAnimationFrame(stepAnim);
    },
    togglePause() {
      if (!currentCfg) return false;
      paused = !paused;
      if (!paused && progress < 1) {
        lastTs = 0;
        rafId = requestAnimationFrame(stepAnim);
      }
      return paused;
    },
    redraw() {
      if (currentCfg) renderFrame(currentCfg.canvas, currentCfg, progress);
    },
    stop() {
      if (rafId) cancelAnimationFrame(rafId);
      rafId = null;
    }
  };
})();
