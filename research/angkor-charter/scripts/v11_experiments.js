// v11_experiments.js — round 2: ten experiments attacking the budget-degeneracy weakness.
// Round 1 showed only the ratio upkeepShare/monumentShare was identified; v11 makes each level
// enter separately, and these experiments test whether they now do.
// Usage: node v11_experiments.js <lo> <hi> <outfile>
// Usage: node v10_experiments.js <lo> <hi> <outfile>
'use strict';
var fs = require('fs');
var A = require('/root/angkor/scripts/v11_abm.js');

var EXPS = [
  { name: 'Y1_obligations', variants: [
    { upkeepShare: 0.55, tag: 'u55' }, { upkeepShare: 0.85, tag: 'u85' },
    { upkeepShare: 1.00, tag: 'u100' }, { upkeepShare: 1.00, monumentShare: 0.0, tag: 'u100m0' }] },
  { name: 'Y2_temple', variants: [0.0, 0.12, 0.25, 0.40].map(function (v) { return { monumentShare: v, upkeepShare: 1.0, tag: 'm' + v }; }) },
  { name: 'Y3_garrison', variants: [0.10, 0.35, 0.70, 1.40].map(function (v) { return { armyPerKm: v, upkeepShare: 1.0, tag: 'a' + v }; }) },
  { name: 'Y4_timing', variants: [1500, 2400, 3300, 4300].map(function (v) { return { pdPerKm: v, upkeepShare: 1.0, tag: 'pd' + v }; }) },
  { name: 'Y5_demog', variants: [0.001, 0.0025, 0.005, 0.008].map(function (v) { return { growRate: v, upkeepShare: 1.0, tag: 'g' + v }; }) },
  { name: 'Y6_arrears', variants: [
    { debtLimit: 6, sellFrac: 0.05, tag: 'd6' }, { debtLimit: 15, sellFrac: 0.05, tag: 'd15' },
    { debtLimit: 30, sellFrac: 0.05, tag: 'd30' }, { debtLimit: 15, sellFrac: 0.12, tag: 'd15s12' },
    { debtLimit: 15, sellFrac: 0.02, tag: 'd15s02' }, { debtLimit: 15, sellFrac: 0.05, minLand: 10, tag: 'floor10' }] },
  { name: 'Y7_frontier', variants: [1.02, 1.35, 2.0, 3.0].map(function (v) { return { zoneHeadroom: v, upkeepShare: 1.0, tag: 'zh' + v }; }) },
  { name: 'Y8_monument_decay', variants: [
    { monDep: 0.0, tag: 'dep0' }, { monDep: 0.02, tag: 'dep02' }, { monDep: 0.05, tag: 'dep05' },
    { prestigeMax: 0.004, tag: 'prest4' }, { prestigeMax: 0.0005, tag: 'prest05' }] },
  { name: 'Y9_rules', variants: [
    { rentOnSurplus: 1, tag: 'rentSurplus' }, { eliteFrac: 0.015, tag: 'elite15p' },
    { eliteFrac: 0.06, tag: 'elite6p' }, { mortSlope: 0.25, mortMax: 0.10, tag: 'harddeath' },
    { swMigrate: 0, tag: 'nomigrate' }, { raidRate: 0.3, tag: 'raid30' }] },
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
    for (var s = 0; s < reps; s++) WORK.push({ exp: ex.name, v: v, seed: 2400 + s * 37 });
  });
});

var LO = +(process.argv[2] || 0), HI = Math.min(WORK.length, +(process.argv[3] || WORK.length));
var OUT = process.argv[4] || '/tmp/v10.csv';

// Monte Carlo space: the fiscal loop parameters plus the classic social ones.
var MCSPACE = {
  rentRate: [0.18, 0.45], eliteFrac: [0.005, 0.08], migrateProb: [0.0, 0.08],
  monumentShare: [0.0, 0.45], upkeepShare: [0.4, 1.0], crownShare: [0.25, 0.65],
  clearProb: [0.01, 0.10], raidRate: [0.0, 0.30], zoneHeadroom: [1.02, 2.5],
  droughtSlope: [0.0, 0.5], pdPerKm: [2800, 12000], growRate: [0.0008, 0.008],
  debtLimit: [3, 45], hEffFloor: [0.30, 0.85], netUp: [0.008, 0.05], armyPerKm: [0.05, 1.5],
  monDep: [0.0, 0.04], sellFrac: [0.01, 0.15], kmPer1000T: [8, 70]};
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
    var r = rng(31000 + w.v.idx * 31 + w.seed);
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
