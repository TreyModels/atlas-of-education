'use strict';

(function () {
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
    const h = w < 450 ? 240 : 310;
    const dpr = Math.min(2, window.devicePixelRatio || 1);
    canvas.style.height = h + 'px';
    if (canvas.width !== w*dpr || canvas.height !== h*dpr) {
      canvas.width = w*dpr;
      canvas.height = h*dpr;
    }
    const cx = canvas.getContext('2d');
    cx.setTransform(dpr,0,0,dpr,0,0);
    const zh = cfg.lang === 'zh';
    const data = cfg.storyPaths;
    const rows = data.points.poor10_top10;
    const lead = rows[1];
    canvas.setAttribute('aria-label', zh
      ? '一名模拟学生及其同组学生的起始与最终排名。'
      : 'Starting and final ranks of one simulated pupil and others in the same group.');
    const x0=28, x1=w-27, y0=36, y1=h-46;
    const y=p=>y1-(y1-y0)*p/100;
    const end=p=>x0+(x1-x0)*p;
    const bg=cx.createLinearGradient(0,0,w,h);
    bg.addColorStop(0,'#0c2a36');bg.addColorStop(1,'#132d48');
    cx.fillStyle=bg;cx.fillRect(0,0,w,h);
    cx.fillStyle='#1a4251';cx.fillRect(x0,y(100),x1-x0,y(90)-y(100));
    cx.font='600 11px system-ui';cx.fillStyle='#d5f5ed';cx.textAlign='right';
    cx.fillText(zh?'前10%模拟录取线':'Top 10% university proxy',x1-5,y(90)-5,x1-x0-10);
    cx.textAlign='left';cx.fillStyle='#ecf5f5';
    cx.fillText(zh?'初始能力排名':'Starting ability rank',x0,h-23);
    cx.textAlign='right';cx.fillText(zh?'最终录取排名':'Final placement rank',x1,h-23);
    cx.strokeStyle='#53717c';cx.lineWidth=1;
    for(const x of [x0,x1]){cx.beginPath();cx.moveTo(x,y0);cx.lineTo(x,y1);cx.stroke();}
    const drawPath = ([from, to], u, featured) => {
      const bend = v => y(from + (to - from) * (v * v * (3 - 2 * v)));
      const trail = cx.createLinearGradient(x0, 0, Math.max(x0 + 1, end(u)), 0);
      trail.addColorStop(0, 'rgba(85, 176, 232, .04)');
      trail.addColorStop(1, featured ? '#92dbff' : 'rgba(85, 176, 232, .34)');
      cx.strokeStyle = trail;
      cx.lineWidth = featured ? 2.6 : .85;
      cx.beginPath();
      cx.moveTo(x0, bend(0));
      for (let j = 1; j <= 20; j++) {
        const v = u * j / 20;
        cx.lineTo(end(v), bend(v));
      }
      cx.stroke();
      cx.fillStyle = featured ? '#dbf9ff' : 'rgba(110, 196, 244, .55)';
      if (featured) {
        cx.shadowColor = '#58bbff';
        cx.shadowBlur = 14;
      }
      cx.beginPath();
      cx.arc(end(u), bend(u), featured ? 4.9 : 1.25, 0, Math.PI * 2);
      cx.fill();
      cx.shadowBlur = 0;
    };
    const pack = Math.max(0, (t - .39) / .61);
    if (pack > 0) {
      rows.forEach((point, i) => {
        if (point !== lead && i % 3 === 0) {
          const distance = Math.max(0, Math.min(1, pack * 1.26 - (i % 13) / 52));
          if (distance > 0) drawPath(point, distance, false);
        }
      });
    }
    drawPath(lead, Math.min(1, t / .40), true);
    cfg.onProgress?.(t);
  }

  function stepAnim(ts) {
    if (!currentCfg) return;
    if (!lastTs) lastTs = ts;
    const dt = (ts - lastTs) / 1000;
    lastTs = ts;
    if (!paused) {
      progress = Math.min(1, progress + dt / 7.2);
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
    seek(value) {
      if (!currentCfg) return;
      if (rafId) cancelAnimationFrame(rafId);
      rafId = null;
      paused = true;
      progress = value;
      renderFrame(currentCfg.canvas, currentCfg, progress);
    },
    togglePause() {
      if (!currentCfg) return false;
      if (!paused && progress >= 1) {
        this.replay();
        return false;
      }
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
