// v10_experiments.js — round 1: ten experiments attacking the fiscal->water->harvest coupling.
// Usage: node v10_experiments.js <lo> <hi> <outfile>
'use strict';
var fs = require('fs');
var A = require('/root/angkor/scripts/v10_abm.js');

var EXPS = [
  // X1: the two parameters that were bit-identical in v9. Now they share one budget.
  { name: 'X1_budget_split', variants: [
    { upkeepShare: 0.30, monumentShare: 0.05, tag: 'u30m05' },
    { upkeepShare: 0.30, monumentShare: 0.18, tag: 'u30m18' },
    { upkeepShare: 0.30, monumentShare: 0.45, tag: 'u30m45' },
    { upkeepShare: 0.12, monumentShare: 0.18, tag: 'u12m18' }] },
  // X2: how heavily the water network is loaded -> how fast the fiscal loop closes
  { name: 'X2_fiscal_load', variants: [3000, 5000, 8000, 12000].map(function (v) { return { pdPerKm: v, tag: 'pd' + v }; }) },
  // X3: network growth rate and how fast abandoned canals leave the maintenance bill
  { name: 'X3_network_dyn', variants: [
    { kmPer1000T: 10, netDown: 0.03, tag: 'k10' },
    { kmPer1000T: 30, netDown: 0.03, tag: 'k30' },
    { kmPer1000T: 60, netDown: 0.03, tag: 'k60' },
    { kmPer1000T: 30, netDown: 0.005, tag: 'k30sticky' }] },
  // X4: demographic rate -> peak timing (ablation on the new food-driven demography)
  { name: 'X4_demog', variants: [0.001, 0.0025, 0.005, 0.008].map(function (v) { return { growRate: v, tag: 'g' + v }; }) },
  // X5: the ablation that decides whether the fix matters at all
  { name: 'X5_coupling_off', variants: [
    { swCouple: 0, tag: 'nofix' },
    { swCouple: 1, tag: 'fix' }] },
  // X6: arrears -> dispossession -> elite share of land
  { name: 'X6_arrears', variants: [
    { debtLimit: 4, sellFrac: 0.02, tag: 'd4s02' }, { debtLimit: 4, sellFrac: 0.12, tag: 'd4s12' },
    { debtLimit: 15, sellFrac: 0.05, tag: 'd15s05' }, { debtLimit: 40, sellFrac: 0.05, tag: 'd40s05' },
    { debtLimit: 15, sellFrac: 0.05, minLand: 15, tag: 'floor15' }, { debtLimit: 15, sellFrac: 0.05, minLand: 90, tag: 'floor90' }] },
  // X7: the land ceiling, now per zone
  { name: 'X7_frontier', variants: [1.02, 1.35, 2.0, 3.0].map(function (v) { return { zoneHeadroom: v, tag: 'zh' + v }; }) },
  // X8: network condition parameters
  { name: 'X8_infra', variants: [
    { infraDecay: 0.03, infraRepair: 0.04, tag: 'soft' },
    { infraDecay: 0.05, infraRepair: 0.03, tag: 'base' },
    { infraDecay: 0.08, infraRepair: 0.02, tag: 'hard' },
    { infraDecay: 0.05, infraRepair: 0.03, hEffFloor: 0.30, tag: 'floor30' },
    { infraDecay: 0.05, infraRepair: 0.03, hEffFloor: 0.80, tag: 'floor80' }] },
  // X9: ABM rule variants (rent form, mortality cap, elite rent routing)
  { name: 'X9_rules', variants: [
    { rentOnSurplus: 0, tag: 'rentGross' },
    { rentOnSurplus: 1, tag: 'rentSurplus' },
    { mortMax: 0.03, mortSlope: 0.06, tag: 'slowdeath' },
    { mortMax: 0.12, mortSlope: 0.30, tag: 'fastdeath' },
    { eliteFrac: 0.01, tag: 'elite1pct' },
    { eliteFrac: 0.08, tag: 'elite8pct' }] },
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
    for (var s = 0; s < reps; s++) WORK.push({ exp: ex.name, v: v, seed: 1300 + s * 37 });
  });
});

var LO = +(process.argv[2] || 0), HI = Math.min(WORK.length, +(process.argv[3] || WORK.length));
var OUT = process.argv[4] || '/tmp/v10.csv';

// Monte Carlo space: the fiscal loop parameters plus the classic social ones.
var MCSPACE = {
  rentRate: [0.18, 0.45], eliteFrac: [0.005, 0.08], migrateProb: [0.0, 0.08],
  monumentShare: [0.0, 0.45], upkeepShare: [0.08, 0.45], crownShare: [0.25, 0.65],
  clearProb: [0.01, 0.10], raidRate: [0.0, 0.30], zoneHeadroom: [1.02, 2.5],
  droughtSlope: [0.0, 0.5], pdPerKm: [2500, 12000], growRate: [0.0008, 0.008],
  debtLimit: [3, 45], hEffFloor: [0.30, 0.85], netUp: [0.008, 0.05], kmPer1000T: [8, 70]
};
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
    var r = rng(91000 + w.v.idx * 31 + w.seed);
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
