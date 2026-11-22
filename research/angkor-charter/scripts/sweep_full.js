// sweep_full.js — full-parameter sensitivity study of the Angkor model.
// Fits the "850 assertions / build.py" idea from simgrammar to *experiment design*:
// all 33 parameters get a design matrix instead of 5 hard-coded ones.
//
// Usage:  node scripts/sweep_full.js <mode>
//   mode = morris | mc     (default morris)
// Writes results/<mode>.csv (+ .meta.json). One row per model evaluation.
'use strict';
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
const M = require(path.join(ROOT, 'model.js'));
const D = M.DEFAULTS;

const MODE = process.argv[2] || 'morris';

// Every switch the UI exposes, i.e. everything a user can actually change.
const PARAMS = {
  population: [250000, 500000], regionKm2: [1500, 5000], coreShare: [0.05, 0.30],
  riceKm2: [400, 1800], yieldT: [0.9, 2.6], lossPct: [5, 35], riceKg: [140, 320],
  importsT: [0, 40000], localShare: [0.05, 0.90], estateShare: [0.05, 0.80],
  hydraulicDependency: [0.10, 0.85], maintenanceIntensity: [0.05, 0.85],
  climateVolatility: [0.04, 0.28], lateDrought: [0.0, 0.50], growthPct: [0.2, 1.2],
  corveeDays: [4, 80], bonded: [2000, 45000], bondedBirthPct: [0.3, 2.0],
  ritualMobilityPct: [2, 16], raidIntensity: [0.0, 0.94], diplomacy: [0.10, 0.90],
  warExpense: [0.05, 0.60], buildShare: [0.05, 0.65], monumentSkill: [0.35, 0.90],
  defenseSpend: [0.02, 0.55], conquestDamage: [0.1, 0.8], sackShock: [0.0, 0.8],
  tradeIntegration: [0.08, 0.92], templeAutonomy: [0.10, 0.90], marketElasticity: [0.10, 0.80]
};
const KEYS = Object.keys(PARAMS);

// deterministic RNG so the design is reproducible by seed
function rng(seed) { let a = (seed >>> 0) || 1; return () => { a += 0x6D2B79F5; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

const END = 1450;

function run(p) {
  const x = M.simulate(Object.assign({}, D, p, { end: END }), { cadence: 1000 });
  const t = x.timeline;
  let peakSoldiers = 0, yrsArmy = 0, firstArmyZero = null, sMin = Infinity, sMax = -Infinity;
  for (const r of t) {
    if (r.soldiers > peakSoldiers) peakSoldiers = r.soldiers;
    if (r.soldiers > 0) { yrsArmy++; if (firstArmyZero === null) firstArmyZero = r.year; }
    if (r.surplus < sMin) sMin = r.surplus; if (r.surplus > sMax) sMax = r.surplus;
  }
  // first year the army goes to zero after having been positive
  let seenArmy = false, armyDied = null;
  for (const r of t) { if (r.soldiers > 0) seenArmy = true; else if (seenArmy && armyDied === null) armyDied = r.year; }
  return {
    pop: x.final.pop, soldiers: x.final.soldiers, peakSoldiers: peakSoldiers,
    armyDied: armyDied === null ? END : armyDied, yrsArmy: yrsArmy,
    grain: x.final.grainBalance, gunIndex: x.final.ornamentalIndex,
    bonded: x.final.bonded, sacks: x.events.sacks, wars: x.events.wars,
    legitimacy: x.final.legitimacy, surplusMin: sMin, surplusMax: sMax,
    popAt1113: (t.find(r => r.year >= 1113) || t[t.length - 1]).pop,
    popAt1300: (t.find(r => r.year >= 1300) || t[t.length - 1]).pop
  };
}

// ---- Morris: elementary-effects screening over all 30 parameters ----
// r trajectories, (k+1) points each; base points from a fractional-factorial free start.
function morris(r, seed, delta) {
  const k = KEYS.length, d = delta || 0.2, res = rng(seed);
  const rows = [];
  for (let i = 0; i < r; i++) {
    const base = {};
    // random start: each parameter on a random grid level
    const levels = new Array(k).fill(0).map(() => Math.round(res() * 2) / (d > 0.25 ? 1 : 1));
    const jitter = KEYS.map(() => res());
    KEYS.forEach((key, j) => {
      const L = Math.max(2, Math.round(1 / d));
      const lvl = Math.floor(res() * (L - 1) + 1) / L;
      const v = PARAMS[key][0] + (PARAMS[key][1] - PARAMS[key][0]) * lvl;
      base[key] = v;
    });
    const card = KEYS.map((_, j) => j).sort(() => res() - 0.5);
    let cur = Object.assign({}, base);
    const y0 = run(cur);
    let prev = y0;
    for (const j of card) {
      const key = KEYS[j], span = PARAMS[key][1] - PARAMS[key][0];
      cur = Object.assign({}, cur);
      cur[key] = Math.min(PARAMS[key][1], cur[key] + d * span);
      const y = run(Object.assign({}, cur, { seed: 1000 + i }));
      // elementary effects, standardised by the actual step taken
      const step = (cur[key] - base[key]) || 1e-9;
      const dPop = (y.pop - prev.pop) / step;
      const dArmy = (y.peakSoldiers - prev.peakSoldiers) / step / 1000; // soldiers per 1000
      const dGun = (y.gunIndex - prev.gunIndex) / step;
      const dArmyDied = (y.armyDied - prev.armyDied) / step;
      const dGrain = (y.grain - prev.grain) / step;
      const dSacks = (y.sacks - prev.sacks) / step;
      rows.push({ traj: i, key: key, dPop: dPop, dArmy: dArmy, dGun: dGun, dArmyDied: dArmyDied, dGrain: dGrain, dSacks: dSacks,
        from: prev[key], to: cur[key], seedUsed: 1000 + i, base: prev });
      prev = y;
    }
  }
  return rows;
}

// ---- plain Monte Carlo for the KPI distribution ----
function mc(n, seed) {
  const res = rng(seed), rows = [];
  for (let i = 0; i < n; i++) {
    const p = {};
    KEYS.forEach(k => { p[k] = PARAMS[k][0] + (PARAMS[k][1] - PARAMS[k][0]) * res(); });
    const y = run(Object.assign({}, p, { seed: 5000 + i }));
    rows.push(Object.assign({ run: i }, y, p));
  }
  return rows;
}

function toCSV(rows) {
  if (!rows.length) return '';
  const cols = Object.keys(rows[0]).filter(c => typeof rows[0][c] !== 'object');
  return [cols.join(',')].concat(rows.map(r => cols.map(c => r[c] === null || r[c] === undefined ? '' : r[c]).join(','))).join('\n') + '\n';
}

const outDir = path.join(ROOT, 'results');
fs.mkdirSync(outDir, { recursive: true });
const t0 = Date.now();
let rows, name;
if (MODE === 'morris') { rows = morris(48, 2026); name = 'morris'; }
else { rows = mc(parseInt(process.argv[3] || '4000', 10), 777); name = 'mc'; }
fs.writeFileSync(path.join(outDir, name + '.csv'), toCSV(rows));
const meta = { mode: name, rows: rows.length, params: KEYS.length, end: END, seconds: (Date.now() - t0) / 1000,
  model: require('crypto').createHash('sha256').update(fs.readFileSync(path.join(ROOT, 'model.js'))).digest('hex'),
  ranges: PARAMS };
fs.writeFileSync(path.join(outDir, name + '.meta.json'), JSON.stringify(meta, null, 2) + '\n');
console.log(name + ': ' + rows.length + ' evaluations in ' + meta.seconds.toFixed(1) + 's');
