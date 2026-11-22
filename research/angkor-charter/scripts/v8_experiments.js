// v8_experiments.js — ten experiments designed from the v7 results.
// Usage: node v8_experiments.js <lo> <hi> <outfile>
// Each index i maps to (experiment, variant, seed) so shards are disjoint.
'use strict';
var fs = require('fs');
var E = require('/root/angkor/scripts/v8_engine.js');

// fixed base: charter on, raid off, climate off unless the experiment says otherwise
var BASE = { swCharter: 1, swRaid: 0, swClimate: 0, swTransport: 1, swRatchet: 1 };

// each experiment: name, list of variant objects
var EXPS = [];

// E1: where does the endowment land?  existing taxable / frontier-cleared / labour
EXPS.push({ name: 'E1_endowTarget', variants: [0, 1, 2].map(function (v) { return { endowTarget: v, tag: 'target' + v }; }) });
// E2: what is taxed?  land / head / mixed
EXPS.push({ name: 'E2_taxBase', variants: [0, 1, 2].map(function (v) { return { taxBase: v, tag: 'tax' + v }; }) });
// E3: ratchet x elite-overproduction surface -> where does the peak land?
(function () {
  var vars = [], rs = [0.0002, 0.0006, 0.0012, 0.0020, 0.0032, 0.0050], es = [0, 0.001, 0.002, 0.004, 0.006];
  rs.forEach(function (r) { es.forEach(function (e) { vars.push({ endowRate: r, eliteGrow: e, tag: 'r' + r + '_e' + e }); }); });
  EXPS.push({ name: 'E3_ratchet_x_elite', variants: vars });
})();
// E4: charter resilience — how fast can legitimacy erode before relocation becomes collapse?
EXPS.push({ name: 'E4_charterLoss', variants: [0.001, 0.002, 0.004, 0.007, 0.012, 0.020].map(function (v) { return { charterLoss: v, tag: 'cl' + v }; }) });
// E5: cost of moving the capital — phase change or terminal decline?
EXPS.push({ name: 'E5_relocCost', variants: [0.05, 0.10, 0.20, 0.35, 0.50].map(function (v) { return { relocPopLoss: v, tag: 'loss' + v }; }) });
// E6: rival polities competing for the same hinterland
EXPS.push({ name: 'E6_rivals', variants: [0, 1, 2, 3, 5, 8].map(function (v) { return { nRivals: v, tag: 'n' + v }; }) });
// E7: drought timing — before vs after the peak
(function () {
  var vars = [];
  [950, 1050, 1150, 1250, 1350].forEach(function (yr) {
    [0, 0.3, 0.6].forEach(function (sl) { vars.push({ swClimate: 1, droughtYear: yr, droughtSlope: sl, tag: 'y' + yr + '_s' + sl }); });
  });
  EXPS.push({ name: 'E7_droughtTiming', variants: vars });
})();
// E8: yield regime as a SCALE test — does chasing yield change the dynamics at all?
(function () {
  var vars = [];
  [1.0, 1.5, 2.2].forEach(function (y) { [150, 200, 250].forEach(function (kg) { vars.push({ y: y, riceKg: kg, tag: 'y' + y + '_kg' + kg }); }); });
  EXPS.push({ name: 'E8_yieldScale', variants: vars });
})();
// E9: coercion cost curve — is over-extension (the Rome channel) real once reach is endogenous?
EXPS.push({ name: 'E9_garrison', variants: [0.4, 0.8, 1.2, 1.6, 2.4].map(function (v) { return { garrisonExp: v, tag: 'g' + v }; }) });
// E10: calibration — what endowment rate puts the peak at 1150?
EXPS.push({ name: 'E10_calibratePeak', variants: [0.0002, 0.0004, 0.0006, 0.0008, 0.0010, 0.0013, 0.0016].map(function (v) { return { endowRate: v, tag: 'er' + v }; }) });

// flatten to a work list
var WORK = [];
EXPS.forEach(function (ex) {
  ex.variants.forEach(function (v) {
    for (var s = 0; s < 24; s++) WORK.push({ exp: ex.name, v: v, seed: 500 + s * 37 });
  });
});

var LO = +(process.argv[2] || 0), HI = Math.min(WORK.length, +(process.argv[3] || WORK.length));
var OUT = process.argv[4] || '/tmp/v8.csv';

var rows = [];
for (var i = LO; i < HI; i++) {
  var w = WORK[i];
  var over = {}, k;
  for (k in BASE) over[k] = BASE[k];
  for (k in w.v) if (k !== 'tag') over[k] = w.v[k];
  over.seed = w.seed;
  var x = E.simulate(over);
  rows.push({ exp: w.exp, variant: w.v.tag, seed: w.seed,
    yrPopPeak: x.yrPopPeak, peakPop: Math.round(x.peakPop),
    yrRevPeak: x.yrRevPeak, peakRev: Math.round(x.peakRev),
    relocations: x.relocations, firstReloc: x.firstReloc, relocLag: x.relocLag,
    revenueDecline: x.revenueDecline, endReach: x.endReach, peakReach: x.peakReach,
    endE: x.endE, endCharter: x.endCharter });
}

var cols = Object.keys(rows[0]);
var lines = [cols.join(',')];
rows.forEach(function (r) {
  lines.push(cols.map(function (c) { return typeof r[c] === 'number' ? +r[c].toPrecision(8) : r[c]; }).join(','));
});
fs.writeFileSync(OUT, lines.join('\n') + '\n');
if (LO === 0) console.log('total work items: ' + WORK.length);
