'use strict';
// Seed spread for the Cambodia child labour engine (public/engines/camchild.js).
// Loads the browser engine the way test-worlds.cjs does (vm context, no module system), runs the reference and each
// policy scenario over the same seeds, and writes results.json next to this script.
// Run: node experiments/camchild-seeds/run.cjs [seeds]        (default 50 seeds, seeds 1..50)

const fs = require('fs');
const path = require('path');
const vm = require('vm');
const crypto = require('crypto');

const ROOT = path.join(__dirname, '..', '..');
const ENGINE = path.join(ROOT, 'public', 'engines', 'camchild.js');
const SEEDS = +(process.argv[2] || 50);
const N = 6000;          // households per simulated history, as in the Cambodia world
const HORIZON = 'last';  // headline year is the final simulated year (2036)

const src = fs.readFileSync(ENGINE, 'utf8');
const ctx = vm.createContext({});
vm.runInContext(src, ctx, {filename: 'camchild.js'});
const E = ctx.CamChild;
if (!E || typeof E.simulate !== 'function') throw new Error('CamChild.simulate not found after loading ' + ENGINE);

// Reference: every lever at zero, Thailand route open (the engine default).
// Policy scenarios: each of the Cambodia world's levers on its own, at half of its slider maximum (garmentBoom max .5,
// cash max .15). Context levers (floorRise, garmentBoom, thaiOpen) are not programmes, so no cost index is computed.
const LEVERS = [
  ['cash', .075, 'programme'], ['cashU', .075, 'programme'], ['tutorFix', .5, 'programme'],
  ['debtRelief', .5, 'programme'], ['protection', .5, 'programme'], ['feeding', .5, 'programme'],
  ['leftSupport', .5, 'programme'], ['harvest', .5, 'programme'], ['bridging', .5, 'programme'],
  ['ban', .5, 'programme'], ['floorRise', .5, 'context'], ['garmentBoom', .25, 'context'], ['thaiOpen', 0, 'context'],
];
const SCENARIOS = [{id: 'reference', label: 'Reference: no programmes, Thailand route open', kind: 'reference', policy: {}}]
  .concat(LEVERS.map(([k, v, kind]) => ({
    id: k + '_' + String(v).replace('.', 'p'), label: `${k} = ${v}`, kind, policy: {[k]: v},
  })));

// Headline outputs, read from one simulated history against the reference history with the same seed.
const HEADLINE = [
  ['working2036', 'Child labour rate, national, 2036'],
  ['changeVsReference_pp', 'Change vs reference, national child labour, 2036 (percentage points)'],
  ['childYearsAvoided', 'Child-years of labour avoided over 12 years (vs reference)'],
  ['attend2036', 'Attending school (school only or school and work), 2036'],
  ['clPoor2036', 'Child labour, poorest fifth, 2036'],
  ['clRich2036', 'Child labour, richest fifth, 2036'],
  ['clCountryside2036', 'Child labour, countryside, 2036'],
  ['clPhnomPenh2036', 'Child labour, Phnom Penh, 2036'],
  ['clLeftBehind2036', 'Child labour, children of migrant parents, 2036'],
  ['migrantTeens2036', 'Teens working away from home, share of all children, 2036'],
  ['costIndexIllustrative', 'ILLUSTRATIVE cost index per child-year avoided (invented unit costs), per-seed ratio'],
];

function headline(R, B) {
  const last = R.rows.length - 1;
  const avoided = R.rows.reduce((s, x, i) => s + (B.rows[i].all.cl - x.all.cl), 0) * N;
  return {
    working2036: R.rows[last].all.cl,
    changeVsReference_pp: 100 * (R.rows[last].all.cl - B.rows[last].all.cl),
    childYearsAvoided: avoided,
    attend2036: R.rows[last].all.attend,
    clPoor2036: R.rows[last].all.clPoor,
    clRich2036: R.rows[last].all.clRich,
    clCountryside2036: R.rows[last].rural.cl,
    clPhnomPenh2036: R.rows[last].pp.cl,
    clLeftBehind2036: R.rows[last].all.clLeft,
    migrantTeens2036: R.rows[last].all.migrant,
    costIndexIllustrative: null, // filled by the caller for programme scenarios only
    _spent: R.spent.total,
  };
}

const q = (a, p) => {
  const s = a.slice().sort((x, y) => x - y);
  const i = (s.length - 1) * p, lo = Math.floor(i), hi = Math.ceil(i);
  return s[lo] + (s[hi] - s[lo]) * (i - lo);
};
function stats(xs) {
  const v = xs.filter(x => x !== null && Number.isFinite(x));
  const n = v.length;
  const mean = v.reduce((a, b) => a + b, 0) / n;
  const sd = n > 1 ? Math.sqrt(v.reduce((a, b) => a + (b - mean) ** 2, 0) / (n - 1)) : 0;
  return {n, mean, sd, p5: q(v, .05), p50: q(v, .5), p95: q(v, .95)};
}

const t0 = Date.now();
const perSeed = {};           // scenario id -> seed -> headline row
const spentBySeed = {};       // scenario id -> seed -> total programme spend (adult-wage units)
for (const sc of SCENARIOS) { perSeed[sc.id] = {}; spentBySeed[sc.id] = {}; }
for (let s = 1; s <= SEEDS; s++) {
  const Ref = E.simulate({seed: s, policy: {}});
  for (const sc of SCENARIOS) {
    const R = sc.id === 'reference' ? Ref : E.simulate({seed: s, policy: sc.policy});
    const h = headline(R, Ref);
    spentBySeed[sc.id][s] = h._spent;
    if (sc.kind === 'programme') h.costIndexIllustrative = h.childYearsAvoided > 0 ? h._spent / h.childYearsAvoided : null;
    delete h._spent;
    h.seed = s;
    perSeed[sc.id][s] = h;
  }
  if (s % 10 === 0) process.stderr.write(`seed ${s}/${SEEDS} (${Math.round((Date.now() - t0) / 1000)}s)\n`);
}

// Pooled cost index as the Cambodia world computes it: mean spend over seeds / mean child-years avoided over seeds.
const pooledCostIndex = {};
for (const sc of SCENARIOS.filter(x => x.kind === 'programme')) {
  const rows = Object.values(perSeed[sc.id]);
  const meanSpent = rows.reduce((a, h) => a + spentBySeed[sc.id][h.seed], 0) / rows.length;
  const meanAvoided = rows.reduce((a, h) => a + h.childYearsAvoided, 0) / rows.length;
  pooledCostIndex[sc.id] = meanAvoided > 0 ? meanSpent / meanAvoided : null;
}

const summary = {reference: {}, scenarios: {}};
for (const [key] of HEADLINE) summary.reference[key] = stats(Object.values(perSeed.reference).map(h => h[key]));
const comparisons = {};
for (const sc of SCENARIOS.filter(x => x.id !== 'reference')) {
  summary.scenarios[sc.id] = {};
  comparisons[sc.id] = {};
  for (const [key] of HEADLINE) {
    summary.scenarios[sc.id][key] = stats(Object.values(perSeed[sc.id]).map(h => h[key]));
    if (key === 'costIndexIllustrative') continue; // reported only as an illustrative ratio, not compared
    const d = SEEDS ? Object.keys(perSeed[sc.id]).map(s => perSeed[sc.id][s][key] - perSeed.reference[s][key]) : [];
    const dStat = stats(d);
    const refSd = summary.reference[key].sd;
    comparisons[sc.id][key] = {
      meanDifference: dStat.mean,
      sdOfPairedDifference: dStat.sd,
      referenceSeedSd: refSd,
      absMeanDiffOverReferenceSd: refSd > 0 ? Math.abs(dStat.mean) / refSd : null,
      smallerThanSeedSpread: Math.abs(dStat.mean) < refSd,
      pairedT: dStat.sd > 0 ? dStat.mean / (dStat.sd / Math.sqrt(dStat.n)) : null,
      shareSeedsSameSign: d.filter(x => Math.sign(x) === Math.sign(dStat.mean)).length / d.length,
    };
  }
}

const engineSha = crypto.createHash('sha256').update(src).digest('hex');
const out = {
  meta: {
    engine: 'public/engines/camchild.js',
    engineSha256: engineSha,
    seeds: SEEDS, seedValues: `1..${SEEDS}`, households: N, years: 12, headlineYear: 2036,
    node: process.version, made: new Date().toISOString().slice(0, 10),
    scenarioLevels: 'each lever alone at half its Cambodia-world slider maximum (garmentBoom .25, cash .075, thaiOpen 0); reference = engine defaults',
    spreadDefinition: 'referenceSeedSd = standard deviation across seeds of the reference headline (sample SD, n-1); a policy difference is smaller than the seed spread when |mean paired difference| < referenceSeedSd',
    costIndexNote: 'ILLUSTRATIVE only: unit costs in the engine are UNSOURCED (invented). Not a programme cost estimate.',
  },
  headline: HEADLINE.map(([key, label]) => ({key, label})),
  scenarios: SCENARIOS.map(({id, label, kind, policy}) => ({id, label, kind, policy})),
  reference: summary.reference,
  scenarioStats: summary.scenarios,
  pooledCostIndexIllustrative: pooledCostIndex,
  comparisons,
  perSeed,
};
const outFile = path.join(__dirname, 'results.json');
fs.writeFileSync(outFile, JSON.stringify(out, null, 2) + '\n');
process.stderr.write(`wrote ${outFile} in ${Math.round((Date.now() - t0) / 1000)}s\n`);
