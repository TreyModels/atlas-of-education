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
    const other = !cfg.showCompare || cfg.compareMode === 'rich10_top10' ? 'rich10_top10' : 'rich10_p60';
    const groups = [
      ['poor10_top10', zh ? '较贫困的高能力学生' : 'High ability, poorer families', '#176b78', '#39acba'],
      [other, other === 'rich10_top10' ? (zh ? '较富裕的高能力学生' : 'High ability, richer families')
        : (zh ? '较富裕的中等能力学生' : 'Middle ability, richer families'), '#9a4d24', '#ea9860']
    ];
    canvas.setAttribute('aria-label', groups.map(([key,label]) => {
      const group = data.example_cohort_profiles[key];
      return label + ': ' + group.selective_uni_pct + '% (n=' + group.n + ')';
    }).join('. '));
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
    const pace=Math.min(1,t*1.2);
    for(const [key,label,trail,head] of groups){
      const rows=data.points[key];
      const skip=Math.max(1,Math.ceil(rows.length/120));
      rows.forEach(([from,to],i)=>{
        if(i%skip) return;
        const u=Math.max(0,Math.min(1,pace-(i%13)/65));
        if(u<=0) return;
        const bend=v=>y(from+(to-from)*(v*v*(3-2*v)));
        cx.strokeStyle=trail;
        cx.globalAlpha=.30;cx.lineWidth=.8;
        cx.beginPath();cx.moveTo(x0,bend(0));
        for(let j=1;j<=10;j++){const v=u*j/10;cx.lineTo(end(v),bend(v));}
        cx.stroke();
        cx.globalAlpha=.82;cx.fillStyle=head;
        cx.beginPath();cx.arc(end(u),bend(u),1.7,0,Math.PI*2);cx.fill();
        cx.globalAlpha=1;
      });
    }
  }

  function stepAnim(ts) {
    if (!currentCfg) return;
    if (!lastTs) lastTs = ts;
    const dt = (ts - lastTs) / 1000;
    lastTs = ts;
    if (!paused) {
      progress = Math.min(1, progress + dt / 2.55);
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
