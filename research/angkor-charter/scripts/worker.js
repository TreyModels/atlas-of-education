// worker.js — one shard of the sensitivity study. Same parameter space as sweep_full.js,
// but with disjoint sampling so N shards are independent and recombine exactly.
// Usage: node scripts/worker.js <mc|morris> <lo> <hi> <outfile>
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const ROOT = path.resolve(__dirname, '..');
const M = require(path.join(ROOT, 'model.js'));
const D = M.DEFAULTS;

const MODE = process.argv[2] || 'mc';
const LO = parseInt(process.argv[3] || '0', 10);
const HI = parseInt(process.argv[4] || '1000', 10);
const OUT = process.argv[5] || path.join(ROOT, 'results', 'part.csv');
const END = parseInt(process.env.ANGKOR_END || '1450', 10);

// identical space to sweep_full.js: every switch the UI exposes
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

function rng(seed) { let a = (seed >>> 0) || 1; return () => { a += 0x6D2B79F5; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

function run(p) {
  const x = M.simulate(Object.assign({}, D, p, { end: END }), { cadence: 1000 });
  const t = x.timeline;
  let peakSoldiers = 0, yrsArmy = 0, seenArmy = false, armyDied = -1;
  let sMin = Infinity, sMax = -Infinity, gunMax = 0;
  for (const r of t) {
    if (r.soldiers > peakSoldiers) peakSoldiers = r.soldiers;
    if (r.soldiers > 0) { yrsArmy++; seenArmy = true; } else if (seenArmy && armyDied < 0) armyDied = r.year;
    if (r.surplus < sMin) sMin = r.surplus;
    if (r.surplus > sMax) sMax = r.surplus;
    if (r.ornamentalIndex > gunMax) gunMax = r.ornamentalIndex;
  }
  const at = yr => { for (const r of t) if (r.year >= yr) return r; return t[t.length - 1]; };
  const r1113 = at(1113), r1300 = at(1300);
  return {
    pop: x.final.pop, popAt1113: r1113.pop, popAt1300: r1300.pop,
    soldiers: x.final.soldiers, peakSoldiers: peakSoldiers,
    armyDied: armyDied < 0 ? END : armyDied, fracYrsNoArmy: 1 - yrsArmy / t.length,
    gunIndex: x.final.ornamentalIndex, gunMax: gunMax,
    grain: x.final.grainBalance, surplusMin: sMin, surplusMax: sMax,
    bonded: x.final.bonded, sacks: x.events.sacks, wars: x.events.wars,
    legitimacy: x.final.legitimacy, foodRatio: x.final.foodRatio
  };
}

const rows = [];
if (MODE === 'mc') {
  const res = rng(12345);
  for (let i = LO; i < HI; i++) {
    // skip-ahead so each shard's stream is independent of the others
    const p = {};
    KEYS.forEach((k, j) => {
      // cheap decorrelation: hash (i,j) into [0,1)
      const h = (Math.imul(i + 0x9E3779B9, 0x85EBCA6B) ^ Math.imul(j + 1, 0xC2B2AE35)) >>> 0;
      p[k] = PARAMS[k][0] + (PARAMS[k][1] - PARAMS[k][0]) * (h / 4294967296);
    });
    const y = run(Object.assign({}, p, { seed: 5000 + i }));
    rows.push(Object.assign({ run: i }, y, p));
  }
} else {
  // Morris elementary effects, replication index = run index
  const DELTA = 0.2;
  for (let rep = LO; rep < HI; rep++) {
    const res = rng(31337 + rep);
    const L = Math.max(2, Math.round(1 / DELTA));
    const base = {};
    KEYS.forEach(k => {
      const lvl = Math.floor(res() * (L - 1) + 1) / L;
      base[k] = PARAMS[k][0] + (PARAMS[k][1] - PARAMS[k][0]) * lvl;
    });
    // random permutation of parameters (Fisher-Yates with seeded rng)
    const order = KEYS.map((k, j) => j);
    for (let a = order.length - 1; a > 0; a--) { const b = Math.floor(res() * (a + 1)); const tmp = order[a]; order[a] = order[b]; order[b] = tmp; }
    let cur = Object.assign({}, base);
    let prev = run(Object.assign({}, cur, { seed: 1000 + rep }));
    for (const j of order) {
      const key = KEYS[j];
      const before = cur[key];
      cur[key] = Math.min(PARAMS[key][1], before + DELTA * (PARAMS[key][1] - PARAMS[key][0]));
      const step = cur[key] - before;
      const y = run(Object.assign({}, cur, { seed: 1000 + rep }));
      if (Math.abs(step) > 1e-12) {
        rows.push({
          rep: rep, key: key, from: before, to: cur[key],
          dPop: (y.pop - prev.pop) / step, dPop1113: (y.popAt1113 - prev.popAt1113) / step,
          dPeakSoldiers: (y.peakSoldiers - prev.peakSoldiers) / step,
          dArmyDied: (y.armyDied - prev.armyDied) / step,
          dGun: (y.gunIndex - prev.gunIndex) / step, dGrain: (y.grain - prev.grain) / step,
          dSacks: (y.sacks - prev.sacks) / step, dBonded: (y.bonded - prev.bonded) / step,
          dLegit: (y.legitimacy - prev.legitimacy) / step
        });
      }
      prev = y;
    }
  }
}

function toCSV(rs) {
  if (!rs.length) return '';
  const cols = Object.keys(rs[0]);
  return [cols.join(',')].concat(rs.map(r => cols.map(c => {
    const v = r[c];
    return v === null || v === undefined ? '' : (typeof v === 'number' ? +v.toPrecision(12) : v);
  }).join(','))).join('\n') + '\n';
}
fs.writeFileSync(OUT, toCSV(rows));
