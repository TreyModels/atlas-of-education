// p1_mc.js — prior predictive simulation.
//
// Draws parameter sets from p1_priors.js and runs BOTH architectures (v8 stock model,
// v9 agent model) on the same draws. This is the honest question: given only the
// educated guesses we can defend, what does each model predict, and do they agree?
//
// Usage: node p1_mc.js <lo> <hi> <outfile>
'use strict';
var fs = require('fs');
var P = require('/root/angkor/scripts/p1_priors.js');
var V8 = require('/root/angkor/scripts/v8_engine.js');
var V9 = require('/root/angkor/scripts/v9_abm.js');

var LO = +(process.argv[2] || 0), HI = +(process.argv[3] || 200), OUT = process.argv[4] || '/tmp/p1.csv';

function rng(seed) { var a = (seed >>> 0) || 1; return function () { a += 0x6D2B79F5; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

function pattern(x) {
  var hitPeak = (x.yrPopPeak >= 1000 && x.yrPopPeak <= 1400) ? 1 : 0;
  var hitLag = (x.relocLag >= 20 && x.relocLag <= 300) ? 1 : 0;
  var hitDecl = x.revenueDecline >= 0.20 ? 1 : 0;
  return { peak: hitPeak, lag: hitLag, decl: hitDecl, all: (hitPeak && hitLag && hitDecl) ? 1 : 0 };
}

var rows = [];
for (var i = LO; i < HI; i++) {
  var r = rng(123400 + i * 7919);
  var p = P.sample(r);

  // ---- stock model (v8): fiscal mechanisms explicit, no agents ----
  var x8 = V8.simulate({
    y: p.y, riceKg: p.riceKg, Amax: p.Amax, A0: Math.min(600, p.Amax * 0.4),
    endowRate: p.endowRate, eliteGrow: p.eliteGrow, taxRate: p.taxRate,
    droughtSlope: p.droughtSlope, seed: 1000 + i
  });
  var s8 = pattern(x8);

  // ---- agent model (v9): the same priors, different architecture ----
  // land per settlement and the ceiling follow from Amax; 400 settlements
  var lpa = (p.Amax * 100) / 400;
  var x9 = V9.simulate({
    y: Math.max(0.9, p.y), riceKg: p.riceKg, rentRate: p.rentRate,
    landCap: p.Amax * 100, landPerAgent0: lpa,
    droughtSlope: p.droughtSlope, seed: 2000 + i
  });
  var s9 = pattern(x9);

  rows.push({
    draw: i, y: +p.y.toFixed(3), riceKg: Math.round(p.riceKg), Amax: Math.round(p.Amax),
    endowRate: +p.endowRate.toFixed(6), eliteGrow: +p.eliteGrow.toFixed(5),
    taxRate: +p.taxRate.toFixed(3), rentRate: +p.rentRate.toFixed(3),
    peopleFed: p.meta.peopleFed,
    v8_peakYr: x8.yrPopPeak, v8_lag: x8.relocLag, v8_decl: +x8.revenueDecline.toFixed(3),
    v8_pattern: s8.all, v8_peak8: s8.peak, v8_lag8: s8.lag, v8_decl8: s8.decl,
    v9_peakYr: x9.yrPopPeak, v9_lag: x9.relocLag, v9_decl: +x9.revenueDecline.toFixed(3),
    v9_eliteLand: +x9.eliteShareOfLand.toFixed(2),
    v9_pattern: s9.all, v9_peak8: s9.peak, v9_lag8: s9.lag, v9_decl8: s9.decl
  });
}

var cols = Object.keys(rows[0]);
var lines = [cols.join(',')];
rows.forEach(function (rr) {
  lines.push(cols.map(function (c) {
    var v = rr[c];
    return typeof v === 'number' ? +v.toPrecision(8) : v;
  }).join(','));
});
fs.writeFileSync(OUT, lines.join('\n') + '\n');
