// p2_mc.js — the decisive test: run the AGENT's v12 engine under the DERIVED priors.
//
// The agent's round-3 best (Z5 pd4500) hits peak 1099 / lag 142 / decline 0.80. That was
// found by choosing parameters. This script asks whether the same engine, given only the
// priors we can defend, still lands there - or whether 1099 was a tuning artefact.
//
// Usage: node p2_mc.js <lo> <hi> <outfile>
'use strict';
var fs = require('fs');
var P = require('/root/angkor/scripts/p1_priors.js');
var V12 = require('/root/angkor/scripts/v12_abm.js');

var LO = +(process.argv[2] || 0), HI = +(process.argv[3] || 200), OUT = process.argv[4] || '/tmp/p2.csv';

function rng(seed) { var a = (seed >>> 0) || 1; return function () { a += 0x6D2B79F5; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

function flags(x) {
  var p = (x.yrPopPeak >= 1000 && x.yrPopPeak <= 1300) ? 1 : 0;
  var l = (x.relocLag >= 20 && x.relocLag <= 300) ? 1 : 0;
  var d = x.revenueDecline >= 0.20 ? 1 : 0;
  return { p: p, l: l, d: d, all: (p && l && d) ? 1 : 0 };
}

var rows = [];
for (var i = LO; i < HI; i++) {
  var r = rng(550000 + i * 6151);
  var p = P.sample(r);

  // map the priors onto v12's parameter names.
  // Amax governs both the land ceiling and the starting endowment (400 settlements).
  var lpa = (p.Amax * 100) / 400;
  var x = V12.simulate({
    y: p.y,
    riceKg: p.riceKg,
    landPerAgent0: lpa,
    zoneHeadroom: 1.35,
    rentRate: p.rentRate,
    crownShare: p.crownShare,
    // the endowment ratchet in v12 lives in the elite land market; its rate is proxied by
    // sellFrac (share of a distressed holding that changes hands per event)
    sellFrac: Math.min(0.25, 0.02 + p.endowRate * 12),
    droughtSlope: p.droughtSlope,
    seed: 3000 + i
  });
  var f = flags(x);

  rows.push({
    draw: i, y: +p.y.toFixed(3), riceKg: Math.round(p.riceKg), Amax: Math.round(p.Amax),
    endowRate: +p.endowRate.toFixed(6), rentRate: +p.rentRate.toFixed(3),
    peopleFed: p.meta.peopleFed,
    peakYr: x.yrPopPeak, lag: x.relocLag, decl: +x.revenueDecline.toFixed(3),
    popDecl: +x.popDecline.toFixed(3), eliteLand: +x.eliteShareOfLand.toFixed(2),
    interior: x.interiorPeak ? 1 : 0, relocs: x.relocations,
    hitPeak: f.p, hitLag: f.l, hitDecl: f.d, pattern: f.all
  });
}
var cols = Object.keys(rows[0]);
var lines = [cols.join(',')];
rows.forEach(function (rr) {
  lines.push(cols.map(function (c) { var v = rr[c]; return typeof v === 'number' ? +v.toPrecision(8) : v; }).join(','));
});
fs.writeFileSync(OUT, lines.join('\n') + '\n');
