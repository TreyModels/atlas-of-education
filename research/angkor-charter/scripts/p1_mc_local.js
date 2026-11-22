// p1_mc_local.js — prior-predictive simulation, local (iSH) build.
// Server is down; this runs single-core. v8 stock model is cheap; the agent model is not,
// so ABM draws are capped and reported separately.
//
// Usage: node p1_mc_local.js <nStock> <nAgent>
'use strict';
var fs = require('fs');
var path = require('path');
var ROOT = path.resolve(__dirname, '..');
var P = require(path.join(ROOT, 'scripts/p1_priors.js'));
var V8 = require(path.join(ROOT, 'scripts/v8_engine.js'));

var NS = +(process.argv[2] || 200);
var NA = +(process.argv[3] || 0);

function rng(seed) { var a = (seed >>> 0) || 1; return function () { a += 0x6D2B79F5; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
function flags(x) {
  var p = (x.yrPopPeak >= 1000 && x.yrPopPeak <= 1300) ? 1 : 0;
  var l = (x.relocLag >= 20 && x.relocLag <= 300) ? 1 : 0;
  var d = x.revenueDecline >= 0.20 ? 1 : 0;
  return { p: p, l: l, d: d, all: (p && l && d) ? 1 : 0 };
}
function q(a, p2) { var s = a.slice().sort(function (x, y) { return x - y; }); return s[Math.floor((s.length - 1) * p2)]; }
function mean(a) { return a.reduce(function (x, y) { return x + y; }, 0) / a.length; }

var rows = [];
for (var i = 0; i < NS; i++) {
  var r = rng(123400 + i * 7919);
  var p = P.sample(r);
  var x = V8.simulate({
    y: p.y, riceKg: p.riceKg, Amax: p.Amax, A0: Math.min(600, p.Amax * 0.4),
    endowRate: p.endowRate, eliteGrow: p.eliteGrow, taxRate: p.taxRate,
    droughtSlope: p.droughtSlope, seed: 1000 + i
  });
  var f = flags(x);
  rows.push({ draw: i, y: p.y, riceKg: p.riceKg, Amax: p.Amax, endowRate: p.endowRate,
    taxRate: p.taxRate, eliteGrow: p.eliteGrow, peopleFed: p.meta.peopleFed,
    peakYr: x.yrPopPeak, lag: x.relocLag, decl: x.revenueDecline,
    hitPeak: f.p, hitLag: f.l, hitDecl: f.d, pattern: f.all });
}

var cols = Object.keys(rows[0]);
var out = [cols.join(',')];
rows.forEach(function (rr) {
  out.push(cols.map(function (c) { var v = rr[c]; return typeof v === 'number' ? +v.toPrecision(8) : v; }).join(','));
});
fs.mkdirSync(path.join(ROOT, 'results'), { recursive: true });
fs.writeFileSync(path.join(ROOT, 'results/p1_local.csv'), out.join('\n') + '\n');

var pk = rows.map(function (x) { return x.peakYr; });
console.log('STOCK MODEL v8, prior predictive, n=' + NS);
console.log('  peak year      median ' + q(pk, 0.5) + '   [5% ' + q(pk, 0.05) + '  95% ' + q(pk, 0.95) + ']');
console.log('  reloc lag      median ' + q(rows.map(function (x) { return x.lag; }), 0.5));
console.log('  revenue decline median ' + (100 * q(rows.map(function (x) { return x.decl; }), 0.5)).toFixed(0) + '%');
console.log('  P(peak 1000-1300) ' + (100 * mean(rows.map(function (x) { return x.hitPeak; }))).toFixed(0) + '%');
console.log('  P(lag 20-300)     ' + (100 * mean(rows.map(function (x) { return x.hitLag; }))).toFixed(0) + '%');
console.log('  P(decline >20%)   ' + (100 * mean(rows.map(function (x) { return x.hitDecl; }))).toFixed(0) + '%');
console.log('  P(full pattern)   ' + (100 * mean(rows.map(function (x) { return x.pattern; }))).toFixed(0) + '%');
console.log('  people fed by drawn land: median ' + Math.round(q(rows.map(function (x) { return x.peopleFed; }), 0.5)));

// how often does the drawn land actually feed the implied population?
var split = rows.filter(function (x) { return x.peopleFed >= 700000; }).length;
console.log('  share of draws whose land feeds >=700k (Carter lower bound): ' + (100 * split / rows.length).toFixed(0) + '%');

if (NA > 0) {
  var V12 = require(path.join(ROOT, 'scripts/v12_abm.js'));
  var ab = [];
  for (var j = 0; j < NA; j++) {
    var r2 = rng(550000 + j * 6151);
    var p2 = P.sample(r2);
    var lpa = (p2.Amax * 100) / 400;
    var t0 = Date.now();
    var x2 = V12.simulate({ y: p2.y, riceKg: p2.riceKg, landPerAgent0: lpa,
      rentRate: p2.rentRate, crownShare: p2.crownShare,
      sellFrac: Math.min(0.25, 0.02 + p2.endowRate * 12),
      droughtSlope: p2.droughtSlope, seed: 3000 + j });
    ab.push({ peakYr: x2.yrPopPeak, lag: x2.relocLag, decl: x2.revenueDecline, ms: Date.now() - t0 });
  }
  console.log('\nAGENT MODEL v12, prior predictive, n=' + NA);
  console.log('  peak year median ' + q(ab.map(function (x) { return x.peakYr; }), 0.5));
  console.log('  revenue decline median ' + (100 * q(ab.map(function (x) { return x.decl; }), 0.5)).toFixed(0) + '%');
  console.log('  ms per run (emulated): ' + Math.round(mean(ab.map(function (x) { return x.ms; }))));
  fs.writeFileSync(path.join(ROOT, 'results/p2_local.csv'),
    'peakYr,lag,decl\n' + ab.map(function (x) { return [x.peakYr, x.lag, x.decl].join(','); }).join('\n') + '\n');
}
