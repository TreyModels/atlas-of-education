// Sweep of the coordination multiplier (review 5.1) and the water floor (review 5.4)
// for the Petri and relocation engines. Usage:
//   NEW=public/engines ORIG=experiments/angkor-review/original/engines node experiments/angkor-review/sweep-engines.cjs
'use strict';
const fs = require('fs'), vm = require('vm'), path = require('path');
const root = path.join(__dirname, '..', '..');
const NEW = process.env.NEW || path.join(root, 'public/engines');
const ORIG = process.env.ORIG || path.join(__dirname, 'original/engines');
const OUT = path.join(__dirname, 'results');
fs.mkdirSync(OUT, {recursive: true});

const load = (dir, file) => {
  const c = vm.createContext({});
  vm.runInContext(fs.readFileSync(path.join(dir, file), 'utf8'), c);
  return c;
};
const stats = xs => {
  const n = xs.length, mean = xs.reduce((a, b) => a + b, 0) / n;
  const sd = Math.sqrt(xs.reduce((a, b) => a + (b - mean) ** 2, 0) / (n - 1));
  const s = [...xs].sort((a, b) => a - b);
  const q = p => s[Math.min(n - 1, Math.floor(p * (n - 1) + 0.5))];
  return {n, mean, sd, p10: q(0.1), p90: q(0.9)};
};
const f = (x, d = 3) => (x === null || x === undefined ? 'n/a' : Number(x).toFixed(d));
const ms = (st, d = 3) => `${f(st.mean, d)} ± ${f(st.sd, d)} [${f(st.p10, d)}, ${f(st.p90, d)}]`;

const OLD_COORD = 5 ** 0.227;           // old: 1.4410
const MID_COORD = 5 ** (0.227 / 2);     // one value in between (geometric midpoint): ~1.2003
const COORDS = [['no effect (new default)', 1], ['midpoint', MID_COORD], ['old 5^0.227', OLD_COORD]];
const FLOORS = [['0 (new default)', 0], ['0.1 (old)', 0.1]];
const SEEDS_PETRI = 256, SEEDS_REL = 32;

const md = [];
// ---------- Verification: new engine with old parameters must equal the original engine ----------
const newP = load(NEW, 'petri.js').AngkorPetri, oldP = load(ORIG, 'petri.js').AngkorPetri;
let petriMaxDiff = 0;
for (const scenario of ['stable', 'drought']) for (const knockout of ['none', 'coordination', 'water', 'transport', 'relief', 'temple'])
  for (let seed = 1; seed <= SEEDS_PETRI; seed++) {
    const a = oldP.run({scenario, knockout, seed}), b = newP.run({scenario, knockout, seed, coordination: OLD_COORD, waterFloor: 0.1});
    for (let i = 0; i < a.rows.length; i++) for (const k of ['population', 'core', 'store', 'water', 'harvest', 'gap'])
      petriMaxDiff = Math.max(petriMaxDiff, Math.abs(a.rows[i][k] - b.rows[i][k]));
  }
const newR = load(NEW, 'relocation.js').AngkorRelocation, oldR = load(ORIG, 'relocation.js').AngkorRelocation;
let relocMaxDiff = 0;
for (const climate of ['stable', 'drought']) for (let seed = 1; seed <= SEEDS_REL; seed++) {
  const a = oldR.run({climate, seed, outside: 1.2}), b = newR.run({climate, seed, outside: 1.2, coordination: OLD_COORD, waterFloor: 0.1});
  for (let i = 0; i < a.rows.length; i++) for (const k of ['oldRural', 'oldCore', 'oldWater', 'oldHarvest', 'southHarvest', 'oldUtility'])
    relocMaxDiff = Math.max(relocMaxDiff, Math.abs(a.rows[i][k] - b.rows[i][k]));
}
md.push(`Reproduction check (new engine with coordination=5^0.227 and waterFloor=0.1 against the original engine): Petri max abs difference ${petriMaxDiff}, relocation max abs difference ${relocMaxDiff}.`);

// ---------- Petri sweep ----------
md.push('\n## Petri sweep (256 seeds per cell; mean ± SD [p10, p90])\n');
md.push('| Scenario | Coordination multiplier | Water floor | Peak population | Final/peak retained | Accumulated food gap |');
md.push('|---|---|---|---|---|---|');
const petriSummary = {};
for (const scenario of ['stable', 'drought']) for (const [cl, cv] of COORDS) for (const [fl, fv] of FLOORS) {
  const runs = Array.from({length: SEEDS_PETRI}, (_, i) => newP.run({scenario, seed: i + 1, coordination: cv, waterFloor: fv}));
  const peak = stats(runs.map(r => r.peak)), ret = stats(runs.map(r => r.retained)), gap = stats(runs.map(r => r.gap));
  petriSummary[`${scenario}|${cv}|${fv}`] = {peak, ret, gap};
  md.push(`| ${scenario} | ${cl} (${cv.toFixed(3)}) | ${fl} | ${ms(peak)} | ${ms(ret)} | ${ms(gap)} |`);
}

// ---------- Relocation sweep ----------
md.push('\n## Relocation sweep (32 seeds per cell; outside 1.2, moving cost 0.25, portability 0.75, local repair 0.5, open mobility)\n');
md.push('| Climate | Coordination multiplier | Water floor | Elite exit share (runs with exit) | Final elite share (old centre) | Old-centre rural retained | Old-centre core retained | Old-centre water (final) |');
md.push('|---|---|---|---|---|---|---|---|');
const relocSummary = {};
for (const climate of ['stable', 'drought']) for (const [cl, cv] of COORDS) for (const [fl, fv] of FLOORS) {
  const runs = Array.from({length: SEEDS_REL}, (_, i) => newR.run({climate, seed: i + 1, outside: 1.2, movingCost: 0.25, portability: 0.75, localRepair: 0.5, coordination: cv, waterFloor: fv}));
  const exits = runs.filter(r => r.exitYear !== null).length;
  const st = {
    exit: exits / runs.length,
    elite: stats(runs.map(r => r.finalEliteShare)), rural: stats(runs.map(r => r.oldRuralRetained)),
    core: stats(runs.map(r => r.oldCoreRetained)), water: stats(runs.map(r => r.oldWater))
  };
  relocSummary[`${climate}|${cv}|${fv}`] = st;
  md.push(`| ${climate} | ${cl} (${cv.toFixed(3)}) | ${fl} | ${exits}/${runs.length} | ${ms(st.elite)} | ${ms(st.rural)} | ${ms(st.core)} | ${ms(st.water)} |`);
}

fs.writeFileSync(path.join(OUT, 'sweep-engines.md'), md.join('\n') + '\n');
fs.writeFileSync(path.join(OUT, 'sweep-engines.json'), JSON.stringify({petriMaxDiff, relocMaxDiff, petri: petriSummary, relocation: relocSummary}, null, 2));
console.log(md.join('\n'));
