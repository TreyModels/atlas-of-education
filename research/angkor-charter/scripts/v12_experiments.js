// v12_experiments.js — round 3: ten experiments attacking the dead-shock weakness.
// In v11 raidRate and droughtSlope were dead (a raid was a 1 t wealth shock that the next
// harvest erased). v12 routes shocks through infrastructure damage and field loss, the same
// condition variable the fiscal loop uses.
// Usage: node v12_experiments.js <lo> <hi> <outfile>
'use strict';
var fs = require('fs');
var A = require('/root/angkor/scripts/v12_abm.js');

var EXPS = [
  { name: 'Z1_raid_rate', variants: [0.0, 0.10, 0.30, 0.60].map(function (v) { return { raidRate: v, upkeepShare: 0.85, tag: 'x' + v }; }) },
  { name: 'Z2_raid_damage', variants: [0.0, 0.05, 0.15, 0.35].map(function (v) { return { raidRate: 0.30, raidInfraDamage: v, upkeepShare: 0.85, tag: 'dmg' + v }; }) },
  { name: 'Z3_drought_damage', variants: [0.0, 0.02, 0.05, 0.10].map(function (v) { return { droughtDamage: v, upkeepShare: 0.85, tag: 'dd' + v }; }) },
  { name: 'Z4_climate', variants: [0.05, 0.10, 0.18, 0.28].map(function (v) { return { climateVol: v, upkeepShare: 0.85, tag: 'cv' + v }; }) },
  { name: 'Z5_timing', variants: [2500, 3500, 4500, 6000].map(function (v) { return { pdPerKm: v, upkeepShare: 0.85, tag: 'pd' + v }; }) },
  { name: 'Z6_frontier', variants: [1.05, 1.20, 1.35, 1.60].map(function (v) { return { zoneHeadroom: v, upkeepShare: 0.85, tag: 'zh' + v }; }) },
  { name: 'Z7_elite', variants: [
    { eliteFrac: 0.01, upkeepShare: 0.85, tag: 'e1' }, { eliteFrac: 0.02, upkeepShare: 0.85, tag: 'e2' },
    { eliteFrac: 0.05, upkeepShare: 0.85, tag: 'e5' }, { eliteFrac: 0.02, crownShare: 0.30, upkeepShare: 0.85, tag: 'e2c30' },
    { eliteFrac: 0.02, crownShare: 0.60, upkeepShare: 0.85, tag: 'e2c60' }] },
  { name: 'Z8_infra_floor', variants: [0.35, 0.50, 0.65, 0.80].map(function (v) { return { hEffFloor: v, upkeepShare: 0.85, tag: 'hf' + v }; }) },
  { name: 'Z9_rules', variants: [
    { monDep: 0.04, upkeepShare: 0.85, tag: 'monDep04' }, { prestigeMax: 0.0004, upkeepShare: 0.85, tag: 'prest04' },
    { rentOnSurplus: 1, upkeepShare: 0.85, tag: 'rentSurplus' }, { minLand: 10, upkeepShare: 0.85, tag: 'floor10' },
    { zoneHeadroom: 1.2, pdPerKm: 3500, raidRate: 0.3, upkeepShare: 0.85, tag: 'combined' },
    { debtLimit: 8, upkeepShare: 0.85, tag: 'debt8' }] },
  (function () {
    var vs = [];
    for (var i = 0; i < 60; i++) vs.push({ _mc: true, idx: i, tag: 'mc' + i });
    return { name: 'X10_montecarlo', variants: vs };
  })()
];

var WORK = [];
EXPS.forEach(function (ex) {
  ex.variants.forEach(function (v) {
    var reps = v._mc ? 6 : 8;
    for (var s = 0; s < reps; s++) WORK.push({ exp: ex.name, v: v, seed: 5100 + s * 37 });
  });
});

var LO = +(process.argv[2] || 0), HI = Math.min(WORK.length, +(process.argv[3] || WORK.length));
var OUT = process.argv[4] || '/tmp/v10.csv';

// Monte Carlo space: the fiscal loop parameters plus the classic social ones.
var MCSPACE = {
  rentRate: [0.18, 0.45], eliteFrac: [0.005, 0.08], migrateProb: [0.0, 0.08],
  monumentShare: [0.0, 0.45], upkeepShare: [0.4, 1.0], crownShare: [0.25, 0.65],
  clearProb: [0.01, 0.10], raidRate: [0.0, 0.60], zoneHeadroom: [1.02, 2.0],
  droughtSlope: [0.0, 0.5], pdPerKm: [2000, 9000], growRate: [0.0008, 0.008],
  debtLimit: [3, 45], hEffFloor: [0.30, 0.85], netUp: [0.008, 0.05], armyPerKm: [0.05, 1.5],
  raidInfraDamage: [0.0, 0.35], droughtDamage: [0.0, 0.08], climateVol: [0.04, 0.28]};
var MCKEYS = Object.keys(MCSPACE);
function rng(seed) { var a = (seed >>> 0) || 1; return function () { a += 0x6D2B79F5; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

var rows = [];
for (var i = LO; i < HI; i++) {
  var w = WORK[i];
  var over = {}, k;
  for (k in w.v) if (k !== 'tag' && k !== '_mc' && k !== 'idx') over[k] = w.v[k];
  over.seed = w.seed;
  var mcParams = '';
  if (w.v._mc) {
    var r = rng(61000 + w.v.idx * 31 + w.seed);
    var parts = [];
    MCKEYS.forEach(function (kk) {
      var lo = MCSPACE[kk][0], hi = MCSPACE[kk][1];
      var val = lo + (hi - lo) * r();
      over[kk] = val; parts.push(kk + '=' + val.toFixed(4));
    });
    mcParams = parts.join(';');
  }
  var x = A.simulate(over);
  var hitPeak = (x.yrPopPeak >= 1100 && x.yrPopPeak <= 1250) ? 1 : 0;
  var hitLag = (x.relocLag >= 50 && x.relocLag <= 250) ? 1 : 0;
  var hitDecl = x.revenueDecline >= 0.30 ? 1 : 0;
  var hitElite = (x.eliteShareOfLand >= 0.30 && x.eliteShareOfLand <= 0.60) ? 1 : 0;
  rows.push({ exp: w.exp, variant: w.v.tag, seed: w.seed,
    yrPopPeak: x.yrPopPeak, peakPop: x.peakPop, endPop: x.endPop,
    relocations: x.relocations, relocLag: x.relocLag,
    revenueDecline: x.revenueDecline, popDecline: x.popDecline,
    eliteShareOfLand: x.eliteShareOfLand, endCharter: x.endCharter,
    endInfra: x.endInfra, minInfra: x.minInfra, meanFunded: x.meanFunded,
    interiorPeak: x.interiorPeak, yrCapBound: x.yrCapBound, abandoned: x.abandoned,
    hitPeak: hitPeak, hitLag: hitLag, hitDecl: hitDecl, hitElite: hitElite,
    pattern: (hitPeak && hitLag && hitDecl) ? 1 : 0, mc: mcParams });
}
if (!rows.length) { fs.writeFileSync(OUT, ''); process.exit(0); }
var cols = Object.keys(rows[0]);
var lines = [cols.join(',')];
rows.forEach(function (rr) {
  lines.push(cols.map(function (c) {
    var v = rr[c];
    if (typeof v === 'number') return +v.toPrecision(8);
    return String(v).indexOf(',') >= 0 ? '"' + String(v).replace(/"/g, "'") + '"' : v;
  }).join(','));
});
fs.writeFileSync(OUT, lines.join('\n') + '\n');
if (LO === 0) console.log('work items: ' + WORK.length);
