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

  function stageLabels(lang) {
    return lang === 'zh'
      ? ['初始能力', '中考分流', '高一分班', '高考录取']
      : ['Start', 'Zhongkao', 'Senior-1\nReband', 'Gaokao'];
  }

  function zoneLabels(lang) {
    return lang === 'zh'
      ? { top: '重点大学通道 (前10%)', mid: '普通高中 / 学术轨', low: '职高 / 分流' }
      : { top: 'Selective Uni (Top 10%)', mid: 'Academic Track', low: 'Vocational / Exit' };
  }

  function drawSpline(cx, pts, t, color, width, alpha) {
    const segs = pts.length - 1;
    const total = Math.max(0, Math.min(1, t)) * segs;
    const full = Math.floor(total);
    const frac = total - full;
    if (total <= 0) return;

    cx.save();
    cx.globalAlpha = alpha;
    cx.strokeStyle = color;
    cx.lineWidth = width;
    cx.lineCap = 'round';
    cx.lineJoin = 'round';
    cx.beginPath();
    cx.moveTo(pts[0][0], pts[0][1]);

    for (let i = 0; i < full; i++) {
      const [x0, y0] = pts[i];
      const [x1, y1] = pts[i + 1];
      const mx = (x0 + x1) / 2;
      cx.bezierCurveTo(mx, y0, mx, y1, x1, y1);
    }
    if (full < segs && frac > 0) {
      const [x0, y0] = pts[full];
      const [x1, y1] = pts[full + 1];
      const mx = (x0 + x1) / 2;
      // Subdivide cubic bezier at frac via de Casteljau
      const ax = x0 + (mx - x0) * frac;
      const ay = y0;
      const bx = mx;
      const by = y0 + (y1 - y0) * frac;
      const cxp = mx + (x1 - mx) * frac;
      const cyp = y1;
      const dx = ax + (bx - ax) * frac;
      const dy = ay + (by - ay) * frac;
      const ex = bx + (cxp - bx) * frac;
      const ey = by + (cyp - by) * frac;
      const fx = dx + (ex - dx) * frac;
      const fy = dy + (ey - dy) * frac;
      cx.bezierCurveTo(ax, ay, dx, dy, fx, fy);
    }
    cx.stroke();
    cx.restore();
    return { x: pts[Math.min(segs, full)][0], y: pts[Math.min(segs, full)][1] };
  }

  function evalPoint(pts, t) {
    const segs = pts.length - 1;
    const total = Math.max(0, Math.min(1, t)) * segs;
    const i = Math.min(segs - 1, Math.floor(total));
    const u = total - i;
    const [x0, y0] = pts[i];
    const [x1, y1] = pts[i + 1];
    const mx = (x0 + x1) / 2;
    const inv = 1 - u;
    const x = inv * inv * inv * x0 + 3 * inv * inv * u * mx + 3 * inv * u * u * mx + u * u * u * x1;
    const y = inv * inv * inv * y0 + 3 * inv * inv * u * y0 + 3 * inv * u * u * y1 + u * u * u * y1;
    return [x, y];
  }

  function renderFrame(canvas, cfg, t) {
    const w = Math.round(canvas.getBoundingClientRect().width);
    if (!w) return;
    const isNarrow = w < 460;
    const h = isNarrow ? 245 : 295;
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    canvas.style.height = h + 'px';
    canvas.width = w * dpr;
    canvas.height = h * dpr;
    const cx = canvas.getContext('2d');
    cx.scale(dpr, dpr);

    // Crisp white canvas background
    cx.fillStyle = '#ffffff';
    cx.fillRect(0, 0, w, h);

    const padL = isNarrow ? 22 : 34;
    const padR = isNarrow ? 22 : 34;
    const padT = 38;
    const padB = 34;
    const plotW = w - padL - padR;
    const plotH = h - padT - padB;

    const sx = (i) => padL + (plotW * i) / 3;
    const sy = (rank01) => padT + plotH * (1 - Math.max(0.04, Math.min(0.98, rank01)));

    // Selective University top-10% shaded band
    const uniTopY = sy(0.90);
    cx.fillStyle = 'rgba(7, 102, 94, 0.08)';
    cx.fillRect(padL, padT, plotW, uniTopY - padT);
    cx.strokeStyle = 'rgba(7, 102, 94, 0.35)';
    cx.setLineDash([4, 4]);
    cx.beginPath();
    cx.moveTo(padL, uniTopY);
    cx.lineTo(w - padR, uniTopY);
    cx.stroke();
    cx.setLineDash([]);

    // Vocational band at bottom
    const vocY = sy(0.34);
    cx.fillStyle = 'rgba(16, 47, 53, 0.04)';
    cx.fillRect(padL, vocY, plotW, padT + plotH - vocY);

    // Zone labels
    const zl = zoneLabels(cfg.lang);
    cx.font = `${isNarrow ? 10 : 11}px Inter, "PingFang SC", system-ui, sans-serif`;
    cx.textAlign = 'right';
    cx.fillStyle = TEAL;
    cx.fillText(zl.top, w - padR - 4, padT + 13);
    cx.fillStyle = MUTED;
    cx.fillText(zl.low, w - padR - 4, padT + plotH - 6);

    // 4 vertical stage gates
    const labels = stageLabels(cfg.lang);
    labels.forEach((lbl, i) => {
      const gx = sx(i);
      cx.beginPath();
      cx.moveTo(gx, padT);
      cx.lineTo(gx, padT + plotH);
      cx.strokeStyle = i === 1 || i === 3 ? '#9dbab7' : GRID;
      cx.lineWidth = i === 1 || i === 3 ? 1.5 : 1;
      cx.stroke();

      cx.fillStyle = SLATE;
      cx.font = `600 ${isNarrow ? 10.5 : 11.5}px Inter, "PingFang SC", system-ui, sans-serif`;
      cx.textAlign = 'center';
      const lines = lbl.split('\n');
      lines.forEach((line, li) => {
        cx.fillText(line, gx, 16 + li * 13);
      });
    });

    const toPts = (p) => [
      [sx(0), sy(p.start)],
      [sx(1), sy(p.zhongkao)],
      [sx(2), sy(p.reband)],
      [sx(3), sy(p.gaokao)]
    ];

    const poorTraj = cfg.storyPaths.trajectories.poor10_top10 || [];
    const compKey = cfg.compareMode === 'rich10_top10' ? 'rich10_top10' : 'rich10_p60';
    const compTraj = cfg.storyPaths.trajectories[compKey] || [];

    // 1. Draw faded Monte Carlo ghost cohort trails for Poor Top-10%
    if (t > 0.15) {
      const ghostT = Math.min(1, (t - 0.15) / 0.85);
      poorTraj.slice(1).forEach((p, idx) => {
        const stagger = Math.max(0, Math.min(1, ghostT * 1.15 - (idx % 6) * 0.04));
        drawSpline(cx, toPts(p), stagger, TEAL, 1.35, 0.19);
      });
    }

    // 2. If Beat 2 (or compare enabled), draw faded ghost trails + glowing lead path for comparison student
    if (cfg.showCompare && compTraj.length) {
      if (t > 0.15) {
        const ghostT = Math.min(1, (t - 0.15) / 0.85);
        compTraj.slice(1).forEach((p, idx) => {
          const stagger = Math.max(0, Math.min(1, ghostT * 1.15 - (idx % 6) * 0.04));
          drawSpline(cx, toPts(p), stagger, AMBER, 1.35, 0.18);
        });
      }
      const leadComp = toPts(compTraj[0]);
      drawSpline(cx, leadComp, t, AMBER_GLOW, 9, 1);
      drawSpline(cx, leadComp, t, AMBER, 3.2, 1);
      const [hx, hy] = evalPoint(leadComp, t);
      cx.beginPath();
      cx.arc(hx, hy, 5.5, 0, Math.PI * 2);
      cx.fillStyle = AMBER;
      cx.fill();
      cx.strokeStyle = '#fff';
      cx.lineWidth = 1.8;
      cx.stroke();
    }

    // 3. Draw glowing lead path for Student A (Top-10% ability, bottom-10% wealth)
    if (poorTraj.length) {
      const leadPoor = toPts(poorTraj[0]);
      drawSpline(cx, leadPoor, t, TEAL_GLOW, 10, 1);
      drawSpline(cx, leadPoor, t, TEAL, 3.4, 1);
      const [hx, hy] = evalPoint(leadPoor, t);
      cx.beginPath();
      cx.arc(hx, hy, 6, 0, Math.PI * 2);
      cx.fillStyle = TEAL;
      cx.fill();
      cx.strokeStyle = '#fff';
      cx.lineWidth = 2;
      cx.stroke();
    }

    // Footer legend inside canvas
    cx.font = `${isNarrow ? 10 : 11}px Inter, "PingFang SC", system-ui, sans-serif`;
    cx.textAlign = 'left';
    cx.fillStyle = TEAL;
    const poorLbl = cfg.lang === 'zh'
      ? '● 能力前10% · 财富后10%（实线=单名学生，浅线=蒙特卡洛影子队列）'
      : '● Top 10% ability · Bottom 10% wealth (lead + ghost cohorts)';
    cx.fillText(poorLbl, padL, h - 10);
  }

  function stepAnim(ts) {
    if (!currentCfg) return;
    if (!lastTs) lastTs = ts;
    const dt = (ts - lastTs) / 1000;
    lastTs = ts;
    if (!paused) {
      progress = Math.min(1, progress + dt / 3.4);
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
