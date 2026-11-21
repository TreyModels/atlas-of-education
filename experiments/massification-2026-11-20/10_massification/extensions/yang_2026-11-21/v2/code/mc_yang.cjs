// MC — parameter Monte Carlo with paired seeds (CRN) for the Yang-mapped factory toy.
// ILLUSTRATIVE / EXPLORATORY. Contract: ../MC_PRE_DECLARATIONS.md (sha256 6f9d8c35...).
// Run: node mc_yang.cjs --draws 1000 --outdir ../results --tag mc
const fs = require('fs');
const path = require('path');
const sim = require('./pathways_yang.cjs');
const { PARAMS, DESIGNS, YEARS, OPEN, POSTS } = sim;

const MC_SIZES = [50000, 200000, 500000, 1000000, 2000000];
const PAIRED_SEEDS = [0, 1, 2];
const DRAWS = 1000;
const DRAW_SEED = 20261121;
const LABEL = 'SIMULATED';

// deterministic PRNG for parameter draws (mulberry32)
function mulberry32(a) {
  return function () {
    a |= 0; a = (a + 0x6D2B79F5) | 0;
    let t = Math.imul(a ^ (a >>> 15), 1 | a);
    t = (t + Math.imul(t ^ (t >>> 7), 61 | t)) ^ t;
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

function draws(n, seed) {
  const rnd = mulberry32(seed);
  const out = [];
  for (let k = 0; k < n; k++) {
    const u = () => rnd();
    const variant = Math.min(2, Math.floor(u() * 3));
    const d = {
      draw: k,
      b: 100 + 60 * u(),
      anchorD: 400 + 200 * u(),
      beta: 0.3 + 0.4 * u(),
      pDipInt: 0.60 + 0.20 * u(),
      pDipSlope: 0.10 + 0.20 * u(),
      travelBase: 0.05 + 0.15 * u(),
      travelSpread: 0.15 + 0.20 * u(),
      wageFactory: 2.3 * (0.85 + 0.30 * u()),
      wageFormal: 2.0 * (0.85 + 0.30 * u()),
      wageInformal: 1.4 * (0.85 + 0.30 * u()),
      gateMapping: ['linear', 'proportional', 'convex'][variant],
      gateVariant: variant,
      convexScale: 100 + 300 * u(),
      endogHigh: 2 + 2 * u(),
      endogLow: 0.5 + 1.0 * u()
    };
    out.push(d);
  }
  return out;
}

function meanPost(rows, key) {
  let s = 0, n = 0;
  for (const r of rows) { if (r.y >= OPEN) { s += r[key]; n++; } }
  return n ? s / n : null;
}

function quantile(sorted, q) {
  if (!sorted.length) return null;
  const pos = (sorted.length - 1) * q;
  const lo = Math.floor(pos), hi = Math.ceil(pos);
  if (lo === hi) return sorted[lo];
  return sorted[lo] + (sorted[hi] - sorted[lo]) * (pos - lo);
}

function pearson(x, y) {
  const n = x.length;
  if (n < 2) return null;
  const mx = x.reduce((a, b) => a + b, 0) / n, my = y.reduce((a, b) => a + b, 0) / n;
  let sx = 0, sy = 0, sxy = 0;
  for (let i = 0; i < n; i++) { const dx = x[i] - mx, dy = y[i] - my; sx += dx * dx; sy += dy * dy; sxy += dx * dy; }
  if (sx === 0 || sy === 0) return null;
  return sxy / Math.sqrt(sx * sy);
}

function ranks(values) {
  const idx = values.map((v, i) => [v, i]).sort((a, b) => a[0] - b[0]);
  const r = new Array(values.length);
  let i = 0;
  while (i < idx.length) {
    let j = i;
    while (j + 1 < idx.length && idx[j + 1][0] === idx[i][0]) j++;
    const avg = (i + j) / 2 + 1;
    for (let k = i; k <= j; k++) r[idx[k][1]] = avg;
    i = j + 1;
  }
  return r;
}
function spearman(x, y) { return pearson(ranks(x), ranks(y)); }

function runMC(drawsList, outdir, tag) {
  const perDraw = [];
  const preChecks = [];
  for (const d of drawsList) {
    const P = Object.assign({}, PARAMS, {
      b: d.b, anchorD: d.anchorD, beta: d.beta,
      pDipInt: d.pDipInt, pDipSlope: d.pDipSlope,
      travelBase: d.travelBase, travelSpread: d.travelSpread,
      wageFactory: d.wageFactory, wageFormal: d.wageFormal, wageInformal: d.wageInformal,
      gateMapping: d.gateMapping, convexScale: d.convexScale,
      endogHigh: d.endogHigh, endogLow: d.endogLow
    });
    const rec = Object.assign({}, d, { sizes: {} });
    let preOk = true;
    for (const N of MC_SIZES) {
      const cell = { completion: {}, leaving: {} };
      for (const s of PAIRED_SEEDS) {
        const runs = {};
        for (const design of DESIGNS) runs[design] = sim.run(s, design, N, P);
        // pre-shock check: y=20..22 means identical across designs
        for (const key of ['leaving', 'secondaryComplete']) {
          const means = DESIGNS.map(dz => {
            const rs = runs[dz].filter(r => r.y >= 20 && r.y <= 22);
            return rs.reduce((a, r) => a + r[key], 0) / rs.length;
          });
          const md = Math.max(...means) - Math.min(...means);
          if (!(md === 0)) { preOk = false; preChecks.push({ draw: d.draw, seed: s, N, key, maxDiff: md }); }
        }
        cell.completion[s] = meanPost(runs['yang'], 'secondaryComplete') - meanPost(runs['none'], 'secondaryComplete');
        cell.leaving[s] = meanPost(runs['yang'], 'leaving') - meanPost(runs['none'], 'leaving');
        cell.completion_endog = cell.completion_endog || {};
        cell.leaving_endog = cell.leaving_endog || {};
        cell.completion_endog[s] = meanPost(runs['yang_endog'], 'secondaryComplete') - meanPost(runs['none'], 'secondaryComplete');
        cell.leaving_endog[s] = meanPost(runs['yang_endog'], 'leaving') - meanPost(runs['none'], 'leaving');
      }
      const avg = (o) => Object.values(o).reduce((a, b) => a + b, 0) / Object.values(o).length;
      rec.sizes[N] = {
        completion_gap: avg(cell.completion), leaving_gap: avg(cell.leaving),
        completion_gap_endog: avg(cell.completion_endog), leaving_gap_endog: avg(cell.leaving_endog)
      };
    }
    const counts = (field) => MC_SIZES.filter(N => Math.abs(rec.sizes[N][field]) >= 0.5).length;
    const counts_leaving = (field) => MC_SIZES.filter(N => Math.abs(rec.sizes[N][field]) >= 0.5).length;
    rec.count_completion = counts('completion_gap');
    rec.count_leaving = counts_leaving('leaving_gap');
    rec.count_any = MC_SIZES.filter(N => Math.abs(rec.sizes[N].completion_gap) >= 0.5 || Math.abs(rec.sizes[N].leaving_gap) >= 0.5).length;
    rec.count_any_endog = MC_SIZES.filter(N => Math.abs(rec.sizes[N].completion_gap_endog) >= 0.5 || Math.abs(rec.sizes[N].leaving_gap_endog) >= 0.5).length;
    rec.gap_bar_completion = MC_SIZES.reduce((a, N) => a + rec.sizes[N].completion_gap, 0) / MC_SIZES.length;
    rec.gap_bar_leaving = MC_SIZES.reduce((a, N) => a + rec.sizes[N].leaving_gap, 0) / MC_SIZES.length;
    rec.gap_bar_completion_endog = MC_SIZES.reduce((a, N) => a + rec.sizes[N].completion_gap_endog, 0) / MC_SIZES.length;
    rec.gap_bar_leaving_endog = MC_SIZES.reduce((a, N) => a + rec.sizes[N].leaving_gap_endog, 0) / MC_SIZES.length;
    rec.robust_active = rec.count_any >= 3;
    rec.robust_active_endog = rec.count_any_endog >= 3;
    rec.yang_inert = rec.count_any === 0;
    rec.pre_ok = preOk;
    perDraw.push(rec);
  }
  return { perDraw, preChecks };
}

function summarise(perDraw) {
  const out = { label: LABEL, n_draws: perDraw.length, sizes: {}, sensitivity: {}, inert: {}, pre_shock: {} };
  const q = (arr, p) => quantile(arr.slice().sort((a, b) => a - b), p);
  const stats = (arr) => ({ mean: arr.reduce((a, b) => a + b, 0) / arr.length, p5: q(arr, 0.05), p50: q(arr, 0.5), p95: q(arr, 0.95), min: Math.min(...arr), max: Math.max(...arr) });
  for (const N of MC_SIZES) {
    out.sizes[N] = {
      completion_gap: stats(perDraw.map(r => r.sizes[N].completion_gap)),
      leaving_gap: stats(perDraw.map(r => r.sizes[N].leaving_gap)),
      completion_gap_endog: stats(perDraw.map(r => r.sizes[N].completion_gap_endog)),
      leaving_gap_endog: stats(perDraw.map(r => r.sizes[N].leaving_gap_endog))
    };
  }
  out.pooled = {
    gap_completion: stats(perDraw.map(r => r.gap_bar_completion)),
    gap_leaving: stats(perDraw.map(r => r.gap_bar_leaving)),
    gap_completion_endog: stats(perDraw.map(r => r.gap_bar_completion_endog)),
    gap_leaving_endog: stats(perDraw.map(r => r.gap_bar_leaving_endog))
  };
  out.robust_active_share = perDraw.filter(r => r.robust_active).length / perDraw.length;
  out.robust_active_share_endog = perDraw.filter(r => r.robust_active_endog).length / perDraw.length;
  out.inert_share = perDraw.filter(r => r.yang_inert).length / perDraw.length;
  out.inert_draws = perDraw.filter(r => r.yang_inert).slice(0, 5).map(r => ({ draw: r.draw, b: r.b, anchorD: r.anchorD, gateMapping: r.gateMapping, beta: r.beta }));
  // sensitivity: Spearman of gap_bar with drawn parameters
  const params = ['b', 'anchorD', 'beta', 'pDipInt', 'pDipSlope', 'travelBase', 'travelSpread', 'wageFactory', 'wageFormal', 'wageInformal', 'gateVariant', 'convexScale', 'endogHigh', 'endogLow'];
  const gapC = perDraw.map(r => r.gap_bar_completion), gapL = perDraw.map(r => r.gap_bar_leaving);
  const gapCE = perDraw.map(r => r.gap_bar_completion_endog), gapLE = perDraw.map(r => r.gap_bar_leaving_endog);
  const rows = [];
  for (const k of params) {
    const x = perDraw.map(r => r[k]);
    const rC = spearman(x, gapC), rL = spearman(x, gapL), rCE = spearman(x, gapCE), rLE = spearman(x, gapLE);
    // univariate OLS R^2 on standardised parameter (Pearson r squared) for completion gap
    const rC2 = pearson(x, gapC);
    rows.push({ param: k, spearman_completion: rC, spearman_leaving: rL, spearman_completion_endog: rCE, spearman_leaving_endog: rLE, r2_completion: rC2 === null ? null : rC2 * rC2 });
  }
  out.sensitivity.table = rows;
  const rank = rows.slice().sort((a, b) => Math.abs(b.spearman_completion || 0) - Math.abs(a.spearman_completion || 0));
  out.sensitivity.top3 = rank.slice(0, 3).map(r => ({ param: r.param, rho: r.spearman_completion }));
  const r2sum = rows.reduce((a, r) => a + (r.r2_completion || 0), 0);
  const vd = rows.map(r => ({ param: r.param, r2: r.r2_completion, share: r2sum > 0 ? (r.r2_completion || 0) / r2sum : null }));
  out.sensitivity.variance_decomposition = vd.sort((a, b) => (b.r2 || 0) - (a.r2 || 0)).slice(0, 5);
  out.pre_shock = { pass: perDraw.every(r => r.pre_ok), failures: [] };
  return out;
}

function writePerDrawCSV(perDraw, file) {
  const params = ['draw', 'b', 'anchorD', 'beta', 'pDipInt', 'pDipSlope', 'travelBase', 'travelSpread', 'wageFactory', 'wageFormal', 'wageInformal', 'gateMapping', 'convexScale', 'endogHigh', 'endogLow'];
  const heads = params.slice();
  for (const N of MC_SIZES) heads.push(`comp_gap_${N}`, `leav_gap_${N}`);
  heads.push('count_any', 'count_any_endog', 'robust_active', 'robust_active_endog', 'yang_inert');
  const lines = [heads.join(',')];
  for (const r of perDraw) {
    const vals = params.map(k => typeof r[k] === 'number' ? r[k].toPrecision(10) : r[k]);
    for (const N of MC_SIZES) vals.push(r.sizes[N].completion_gap.toPrecision(10), r.sizes[N].leaving_gap.toPrecision(10));
    vals.push(r.count_any, r.count_any_endog, r.robust_active, r.robust_active_endog, r.yang_inert);
    lines.push(vals.join(','));
  }
  fs.writeFileSync(file, lines.join('\n') + '\n');
}

function parseArgs(argv) {
  const o = {};
  for (let i = 0; i < argv.length; i++) {
    const t = argv[i];
    if (t === '--draws') o.draws = Number(argv[++i]);
    else if (t === '--outdir') o.outdir = argv[++i];
    else if (t === '--tag') o.tag = argv[++i];
  }
  return o;
}

if (require.main === module) {
  const o = parseArgs(process.argv.slice(2));
  const n = o.draws || DRAWS;
  const outdir = o.outdir || path.join(__dirname, '..', 'results');
  const tag = o.tag || 'mc';
  fs.mkdirSync(outdir, { recursive: true });
  const t0 = Date.now();
  const dl = draws(n, DRAW_SEED);
  const { perDraw, preChecks } = runMC(dl, outdir, tag);
  const summary = summarise(perDraw);
  summary.pre_shock.failures = preChecks.slice(0, 5);
  summary.pre_shock.n_failures = preChecks.length;
  const runtime_ms = Date.now() - t0;
  summary.draw_seed = DRAW_SEED;
  summary.paired_seeds = PAIRED_SEEDS;
  summary.sizes_tested = MC_SIZES;
  summary.designs = ['none', 'yang', 'yang_endog'];
  fs.writeFileSync(path.join(outdir, `${tag}_results.json`), JSON.stringify(summary, null, 2) + '\n');
  writePerDrawCSV(perDraw, path.join(outdir, `${tag}_per_draw.csv`));
  const consoleLines = [];
  consoleLines.push(`MC: ${n} draws x ${PAIRED_SEEDS.length} paired seeds x ${MC_SIZES.length} sizes x 3 designs = ${n * PAIRED_SEEDS.length * MC_SIZES.length * 3} runs`);
  consoleLines.push(`pre-shock match: ${summary.pre_shock.pass ? 'PASS' : 'FAIL'} (n_failures=${summary.pre_shock.n_failures})`);
  consoleLines.push(`robust-ACTIVE share (yang): ${summary.robust_active_share.toFixed(4)}`);
  consoleLines.push(`robust-ACTIVE share (yang_endog): ${summary.robust_active_share_endog.toFixed(4)}`);
  consoleLines.push(`inert-draw share: ${summary.inert_share.toFixed(4)}`);
  consoleLines.push(`pooled completion gap: mean ${summary.pooled.gap_completion.mean.toFixed(4)} p5 ${summary.pooled.gap_completion.p5.toFixed(4)} p95 ${summary.pooled.gap_completion.p95.toFixed(4)}`);
  consoleLines.push(`pooled leaving gap: mean ${summary.pooled.gap_leaving.mean.toFixed(4)} p5 ${summary.pooled.gap_leaving.p5.toFixed(4)} p95 ${summary.pooled.gap_leaving.p95.toFixed(4)}`);
  consoleLines.push(`top3 params (completion Spearman): ${JSON.stringify(summary.sensitivity.top3)}`);
  consoleLines.push(`runtime_ms=${runtime_ms}`);
  const log = consoleLines.join('\n') + '\n';
  fs.writeFileSync(path.join(outdir, `${tag}_console.log`), log);
  console.log(log);
}
module.exports = { draws, runMC, summarise, spearman, pearson, ranks, quantile };
