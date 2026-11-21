// v2 — Yang-mapped factory/credential toy. ILLUSTRATIVE; no packages.
// Run: node pathways_yang.cjs [seeds] [--grid]      (default: grid mode)
// Predeclaration: ../PRE_DECLARATIONS.md (frozen before first run).
const B = 128.0;
const C = 500.0 - B * Math.log(1e6);          // anchor D(1e6)=500 (declared)
const NLO = 50000, NHI = 2000000;
const SIZES = [50000, 100000, 200000, 500000, 1000000, 2000000];
const DESIGNS = ['none', 'all', 'yang', 'yang_endog'];
const YEARS = 36, OPEN = 23, POSTS = 12;
const FARM = 1.0, INFORMAL = 1.4, FORMAL = 2.0, FACTORY = 2.3;
const BETA = 0.5;

function yangD(N) { return B * Math.log(N) + C; }
function gateShare(N) {
  const lo = yangD(NLO), hi = yangD(NHI);
  return Math.max(0, Math.min(1, (yangD(N) - lo) / (hi - lo)));
}
function noise(seed, c, i, y, k) {
  let x = seed + 1009;
  for (const n of [c, i, y, k]) { x = Math.imul(x ^ n, 0x45d9f3b); x ^= x >>> 16; }
  return (x >>> 0) / 4294967296;
}

function run(seed, design, N) {
  const years = YEARS, rows = [], people = [];
  const gs = gateShare(N);
  let q = design === 'none' ? 0 : design === 'all' ? POSTS : Math.round(POSTS * gs);
  for (let y = 0; y < years; y++) {
    for (let i = 0; i < 64; i++) people.push({
      c: y, i, r: i % 2, skill: noise(seed, y, i, 0, 2), school: noise(seed, y, i, 0, 3),
      g: 0, left: false, completed: false
    });
    const row = { seed, design, N, y, leaving: 0, secondaryComplete: 0, factoryJobs: 0,
      farmWorkers: 0, informalWorkers: 0, formalWorkers: 0, students: 0, householdIncome: 0,
      q, gs, unfilled: 0, applicantsPerGated: null };
    if (y >= OPEN) {
      const elig = people.filter(p => !p.left && 6 + y - p.c >= 16 && 6 + y - p.c <= 24);
      if (design === 'yang_endog') {
        const appPerPost = elig.length / POSTS;
        if (appPerPost > 3) q = Math.min(POSTS, q + 1);
        else if (appPerPost < 1) q = Math.max(0, q - 1);
      }
      row.q = q;
      row.applicantsPerGated = q > 0 ? +(elig.length / q).toFixed(3) : null;
      const ranked = elig.slice().sort((a, b) =>
        noise(seed, a.c, a.i, y, 8) - noise(seed, b.c, b.i, y, 8));
      const selected = new Set();
      for (let slot = 0; slot < POSTS; slot++) {
        const needsDiploma = slot < q;
        const cand = ranked.find(p => !selected.has(p) && (!needsDiploma || p.g >= 12));
        if (cand) selected.add(cand);
      }
      for (const p of people) {
        if (!selected.has(p) || p.left) continue;
        p.factoryOffer = true;
      }
    }
    for (const p of people) {
      const age = 6 + y - p.c;
      if (age < 6 || age > 24 || p.left) continue;
      const inSchool = p.g < 16;
      const travel = p.r === 1 ? 0.10 + 0.25 * noise(seed, p.c, p.i, 1, 5) : 0;
      const pDip = Math.min(0.98, 0.70 + 0.20 * p.skill);
      const future = pDip * (gs * FACTORY + (1 - gs) * FORMAL) + (1 - pDip) * INFORMAL;
      const dynamic = BETA * (future - INFORMAL);
      const studyValue = 0.9 + 0.8 * p.school + 0.5 * p.skill + (p.g < 12 ? 0.45 : 0)
        + dynamic - travel;
      const wage = p.factoryOffer ? FACTORY : 0;
      const alternative = age >= 18 ? FORMAL : INFORMAL;
      const workValue = Math.max(FARM, alternative, wage);
      const work = age >= 16 && workValue > studyValue;
      if (work) {
        p.left = true; row.leaving++; row.householdIncome += workValue;
        if (wage === workValue) row.factoryJobs++;
        else if (age >= 18 && formal(wage, alternative, workValue)) row.formalWorkers++;
        else if (alternative === INFORMAL && workValue === INFORMAL) row.informalWorkers++;
        else row.farmWorkers++;
        continue;
      }
      if (inSchool) {
        row.students++; row.householdIncome += FARM;
        if (noise(seed, p.c, p.i, y, 7) < 0.78 + 0.18 * p.skill) {
          p.g++; if (p.g === 12) { p.completed = true; row.secondaryComplete++; }
        }
      }
    }
    row.unfilled = Math.max(0, POSTS - row.factoryJobs - (design === 'none' ? 0 : 0));
    for (const p of people) delete p.factoryOffer;
    rows.push(row);
  }
  return rows;
}
function formal(wage, alternative, workValue) {
  return alternative === FORMAL && workValue === FORMAL && wage !== workValue;
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

function grid(seeds) {
  const keys = ['leaving', 'secondaryComplete', 'factoryJobs', 'farmWorkers', 'informalWorkers',
    'formalWorkers', 'householdIncome', 'q', 'unfilled', 'applicantsPerGated'];
  const post = [];
  console.error(`grid: ${SIZES.length} sizes x ${DESIGNS.length} designs x ${seeds} seeds`);
  for (const N of SIZES) for (const d of DESIGNS) {
    let rows = [];
    for (let seed = 0; seed < seeds; seed++) rows = rows.concat(run(seed, d, N).filter(r => r.y >= OPEN));
    const m = meanOver(rows, keys);
    post.push({ N, design: d, gs: +gateShare(N).toFixed(4), D: +yangD(N).toFixed(1), ...m });
  }
  return post;
}

if (require.main === module) {
  const arg = process.argv[2];
  const seeds = Number(arg) || 200;
  const res = grid(seeds);
  console.log('city,design,gate_share,YangD,q_mean,leaving,secondary_completion,factory_hires,unfilled,applicants_per_gated,formal_workers,informal_workers,household_income');
  for (const r of res) console.log([
    r.N, r.design, r.gs, r.D, r.q === null ? '' : r.q.toFixed(2),
    r.leaving.toFixed(3), r.secondaryComplete.toFixed(3), r.factoryJobs.toFixed(3),
    r.unfilled === null ? '' : r.unfilled.toFixed(3),
    r.applicantsPerGated === null ? '' : r.applicantsPerGated,
    r.formalWorkers.toFixed(3), r.informalWorkers.toFixed(3), r.householdIncome.toFixed(1)
  ].join(','));
}
