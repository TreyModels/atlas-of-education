// v2.1 — Yang-mapped factory/credential toy. ILLUSTRATIVE; no country claims.
// Run: node pathways_yang.cjs [--seeds N] [--out FILE] [--log FILE]
// Predeclaration: ../PRE_DECLARATIONS.md (frozen design); v2.1 applies the declared cleanups only:
//   explicit worker classification, fixed unfilled-post count, pre-shock y=20-22 match check,
//   saved grid output, byte-identical two-run determinism. No parameter or threshold changed.
const fs = require('fs');
const PARAMS = {
  b: 128.0, anchorD: 500.0, beta: 0.5,
  pDipInt: 0.70, pDipSlope: 0.20,
  travelBase: 0.10, travelSpread: 0.25,
  wageFactory: 2.3, wageFormal: 2.0, wageInformal: 1.4, farmValue: 1.0,
  gateMapping: 'linear', convexScale: 200.0,
  endogHigh: 3.0, endogLow: 1.0,
  promoteBase: 0.78, promoteSlope: 0.18
};
const NLO = 50000, NHI = 2000000;
const SIZES = [50000, 100000, 200000, 500000, 1000000, 2000000];
const DESIGNS = ['none', 'all', 'yang', 'yang_endog'];
const YEARS = 36, OPEN = 23, POSTS = 12;

function yangD(N, p) { return p.b * Math.log(N) + (p.anchorD - p.b * Math.log(1e6)); }
function gateShare(N, p) {
  const D = yangD(N, p);
  const Dlo = yangD(NLO, p), Dhi = yangD(NHI, p);
  let g;
  if (p.gateMapping === 'linear') g = (D - Dlo) / (Dhi - Dlo);
  else if (p.gateMapping === 'proportional') g = D / Dhi;
  else if (p.gateMapping === 'convex') g = 1 - Math.exp(-(D - Dlo) / p.convexScale);
  else throw new Error('unknown gateMapping ' + p.gateMapping);
  return Math.max(0, Math.min(1, g));
}
// CRN: the arrival noise depends only on (seed, cohort, individual, year, channel) — never on the
// design or the parameter draw — so the same seed gives the same arrivals across designs (common
// random numbers) and across parameter draws.
function noise(seed, c, i, y, k) {
  let x = seed + 1009;
  for (const n of [c, i, y, k]) { x = Math.imul(x ^ n, 0x45d9f3b); x ^= x >>> 16; }
  return (x >>> 0) / 4294967296;
}

function run(seed, design, N, P) {
  const p = P || PARAMS;
  const rows = [], people = [];
  const gs = gateShare(N, p);
  let q = design === 'none' ? 0 : design === 'all' ? POSTS : Math.round(POSTS * gs);
  for (let y = 0; y < YEARS; y++) {
    for (let i = 0; i < 64; i++) people.push({
      c: y, i, r: i % 2, skill: noise(seed, y, i, 0, 2), school: noise(seed, y, i, 0, 3),
      g: 0, left: false, completed: false, factoryOffer: false
    });
    const row = { seed, design, N, y, leaving: 0, secondaryComplete: 0, factoryJobs: 0,
      farmWorkers: 0, informalWorkers: 0, formalWorkers: 0, students: 0, householdIncome: 0,
      q, gs, unfilled: 0, applicantsPerGated: null };
    if (y >= OPEN) {
      const elig = people.filter(p2 => !p2.left && 6 + y - p2.c >= 16 && 6 + y - p2.c <= 24);
      if (design === 'yang_endog') {
        const appPerPost = elig.length / POSTS;
        if (appPerPost > p.endogHigh) q = Math.min(POSTS, q + 1);
        else if (appPerPost < p.endogLow) q = Math.max(0, q - 1);
      }
      row.q = q;
      row.applicantsPerGated = q > 0 ? +(elig.length / q).toFixed(3) : null;
      const ranked = elig.slice().sort((a, b2) =>
        noise(seed, a.c, a.i, y, 8) - noise(seed, b2.c, b2.i, y, 8));
      const selected = new Set();
      for (let slot = 0; slot < POSTS; slot++) {
        const needsDiploma = slot < q;
        const cand = ranked.find(p2 => !selected.has(p2) && (!needsDiploma || p2.g >= 12));
        if (cand) selected.add(cand);
      }
      for (const p2 of people) if (selected.has(p2) && !p2.left) p2.factoryOffer = true;
    }
    for (const p2 of people) {
      const age = 6 + y - p2.c;
      if (age < 6 || age > 24 || p2.left) continue;
      const inSchool = p2.g < 16;
      const travel = p2.r === 1 ? p.travelBase + p.travelSpread * noise(seed, p2.c, p2.i, 1, 5) : 0;
      const pDip = Math.min(0.98, p.pDipInt + p.pDipSlope * p2.skill);
      const future = pDip * (gs * p.wageFactory + (1 - gs) * p.wageFormal) + (1 - pDip) * p.wageInformal;
      const dynamic = p.beta * (future - p.wageInformal);
      const studyValue = 0.9 + 0.8 * p2.school + 0.5 * p2.skill + (p2.g < 12 ? 0.45 : 0)
        + dynamic - travel;
      const wage = p2.factoryOffer ? p.wageFactory : 0;
      const alternative = age >= 18 ? p.wageFormal : p.wageInformal;
      const workValue = Math.max(p.farmValue, alternative, wage);
      const work = age >= 16 && workValue > studyValue;
      if (work) {
        p2.left = true; row.leaving++; row.householdIncome += workValue;
        // explicit classification (replaces the ambiguous formal() helper)
        if (wage === workValue) row.factoryJobs++;
        else if (age >= 18 && alternative === p.wageFormal && workValue === p.wageFormal) row.formalWorkers++;
        else if (alternative === p.wageInformal && workValue === p.wageInformal) row.informalWorkers++;
        else row.farmWorkers++;
        continue;
      }
      if (inSchool) {
        row.students++; row.householdIncome += p.farmValue;
        if (noise(seed, p2.c, p2.i, y, 7) < p.promoteBase + p.promoteSlope * p2.skill) {
          p2.g++; if (p2.g === 12) { p2.completed = true; row.secondaryComplete++; }
        }
      }
    }
    row.unfilled = Math.max(0, POSTS - row.factoryJobs);
    for (const p2 of people) p2.factoryOffer = false;
    rows.push(row);
  }
  return rows;
}

function meanOver(arr, keys) {
  const out = {};
  for (const k of keys) {
    let s = 0, n = 0;
    for (const r of arr) if (r[k] !== null && r[k] !== undefined) { s += r[k]; n++; }
    out[k] = n ? s / n : null;
  }
  return out;
}

function grid(seeds, P) {
  const p = P || PARAMS;
  const keys = ['leaving', 'secondaryComplete', 'factoryJobs', 'farmWorkers', 'informalWorkers',
    'formalWorkers', 'householdIncome', 'q', 'unfilled', 'applicantsPerGated'];
  const post = [], pre = {};
  for (const N of SIZES) for (const d of DESIGNS) {
    let rows = [];
    for (let seed = 0; seed < seeds; seed++) rows = rows.concat(run(seed, d, N, p));
    // pre-shock match check: y=20..22 means must be equal across designs for the same size
    const preRows = rows.filter(r => r.y >= 20 && r.y <= 22);
    const preMean = meanOver(preRows, ['leaving', 'secondaryComplete', 'students']);
    const key = N + '|' + d;
    pre[key] = preMean;
    const postRows = rows.filter(r => r.y >= OPEN);
    post.push({ N, design: d, gs: +gateShare(N, p).toFixed(4), D: +yangD(N, p).toFixed(1), ...meanOver(postRows, keys) });
  }
  // pre-shock check: for each size, all four designs must agree on leaving/secondaryComplete/students
  const preShock = [];
  for (const N of SIZES) {
    const vals = DESIGNS.map(d => pre[N + '|' + d]);
    const maxDiff = (k) => Math.max(...vals.map(v => v[k])) - Math.min(...vals.map(v => v[k]));
    preShock.push({ N, designs: vals, max_diff_leaving: maxDiff('leaving'), max_diff_secondary: maxDiff('secondaryComplete'), max_diff_students: maxDiff('students') });
  }
  const preOk = preShock.every(x => x.max_diff_leaving === 0 && x.max_diff_secondary === 0 && x.max_diff_students === 0);
  return { post, preShock, preOk };
}

function fmtGrid(res) {
  const lines = [];
  lines.push('city,design,gate_share,YangD,q_mean,leaving,secondary_completion,factory_hires,unfilled,applicants_per_gated,formal_workers,informal_workers,household_income');
  for (const r of res.post) lines.push([
    r.N, r.design, r.gs, r.D, r.q === null ? '' : r.q.toFixed(2),
    r.leaving.toFixed(3), r.secondaryComplete.toFixed(3), r.factoryJobs.toFixed(3),
    r.unfilled === null ? '' : r.unfilled.toFixed(3),
    r.applicantsPerGated === null ? '' : r.applicantsPerGated,
    r.formalWorkers.toFixed(3), r.informalWorkers.toFixed(3), r.householdIncome.toFixed(1)
  ].join(','));
  return lines.join('\n') + '\n';
}

function parseArgs(argv) {
  const o = {};
  for (let i = 0; i < argv.length; i++) {
    const t = argv[i];
    if (t === '--seeds') o.seeds = Number(argv[++i]);
    else if (t === '--out') o.out = argv[++i];
    else if (t === '--log') o.log = argv[++i];
  }
  return o;
}

if (require.main === module) {
  const o = parseArgs(process.argv.slice(2));
  const seeds = o.seeds || 200;
  const t0 = Date.now();
  const res = grid(seeds);
  const csv = fmtGrid(res);
  if (o.out) fs.writeFileSync(o.out, csv);
  const logLines = [];
  logLines.push(`v2.1 grid: ${SIZES.length} sizes x ${DESIGNS.length} designs x ${seeds} seeds`);
  logLines.push(`pre-shock match (y=20-22): ${res.preOk ? 'PASS' : 'FAIL'}`);
  for (const x of res.preShock) logLines.push(`  N=${x.N} maxDiff leaving=${x.max_diff_leaving} secondary=${x.max_diff_secondary} students=${x.max_diff_students}`);
  logLines.push(`runtime_ms=${Date.now() - t0}`);
  logLines.push(csv.trimEnd());
  const log = logLines.join('\n') + '\n';
  if (o.log) fs.writeFileSync(o.log, log);
  console.log(log);
}
module.exports = { PARAMS, SIZES, DESIGNS, YEARS, OPEN, POSTS, yangD, gateShare, noise, run, grid, meanOver };
