// v6_worker.js — one shard of the mechanism experiment suite.
// Usage: node v6_worker.js <mode> <lo> <hi> <outfile>
//   mode = factorial | morris | grid
// Writes CSV; shards are disjoint by index range.
'use strict';
var fs = require('fs');
var E = require(__dirname + '/v7_engine.js');
var simulate = E.simulate, DEFAULTS = E.DEFAULTS;
var path = process.argv[2], LO = +process.argv[3], HI = +process.argv[4], OUT = process.argv[5];

// the parameter space for Morris screening (literature-plausible ranges)
var SPACE = {
  haulHalf: [50, 220], holdFrac: [0.015, 0.12], garrisonExp: [0.6, 2.2],
  y: [1.0, 2.2], endowRate: [0.0004, 0.0040], eliteGrow: [0.0005, 0.0060],
  pop0: [200000, 480000], riceKg: [150, 250], growRate: [0.003, 0.010],
  taxRate: [0.05, 0.18], stipendT: [0.15, 0.40], defShare: [0.05, 0.30],
  droughtSlope: [0.0, 0.6], captureRate: [0.0, 0.02], kmPer1000T: [4, 28]
};
var KEYS = Object.keys(SPACE);

function score(x) {
  var hitPeak = (x.yrPopPeak >= 900 && x.yrPopPeak <= 1400) ? 1 : 0;
  var hitLag = (x.relocLag >= 20 && x.relocLag <= 300) ? 1 : 0;
  var hitDecl = x.revenueDecline >= 0.20 ? 1 : 0;
  return { hitPeak: hitPeak, hitLag: hitLag, hitDecl: hitDecl,
    pattern: (hitPeak && hitLag && hitDecl) ? 1 : 0 };
}

function rng(seed) { var a = (seed >>> 0) || 1; return function () { a += 0x6D2B79F5; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }

var rows = [];

if (path === 'factorial') {
  // all 32 switch combinations, replicated
  for (var i = LO; i < HI; i++) {
    var cell = i % 32, rep = Math.floor(i / 32);
    var sw = { swRatchet: cell & 1 ? 1 : 0, swCharter: cell & 2 ? 1 : 0,
      swClimate: cell & 4 ? 1 : 0, swRaid: cell & 8 ? 1 : 0, swTransport: cell & 16 ? 1 : 0 };
    var o = { seed: 4000 + rep * 7 }; for (var k in sw) o[k] = sw[k];
    var x = simulate(o), s = score(x);
    rows.push({ cell: cell, rep: rep, ratchet: sw.swRatchet, charter: sw.swCharter,
      climate: sw.swClimate, raid: sw.swRaid, transport: sw.swTransport,
      yrPopPeak: x.yrPopPeak, peakPop: x.peakPop, yrRevPeak: x.yrRevPeak, peakRev: x.peakRev,
      relocations: x.relocations, firstReloc: x.firstReloc, relocLag: x.relocLag,
      revenueDecline: x.revenueDecline, endowAtCross: x.endowAtCross,
      endPop: x.endPop, hitPeak: s.hitPeak, hitLag: s.hitLag, hitDecl: s.hitDecl, pattern: s.pattern });
  }
} else if (path === 'morris') {
  // elementary effects over the continuous space, switches all ON
  var DELTA = 0.15;
  for (var rep2 = LO; rep2 < HI; rep2++) {
    var r = rng(90000 + rep2 * 13);
    var base = {};
    KEYS.forEach(function (k) { base[k] = SPACE[k][0] + (SPACE[k][1] - SPACE[k][0]) * r(); });
    var order = KEYS.map(function (k, j) { return j; });
    for (var a = order.length - 1; a > 0; a--) { var b = Math.floor(r() * (a + 1)); var tmp = order[a]; order[a] = order[b]; order[b] = tmp; }
    var cur = {}, kk;
    for (kk in base) cur[kk] = base[kk];
    var prev = simulate(Object.assign({ seed: 20000 + rep2 }, cur));
    for (var j2 = 0; j2 < order.length; j2++) {
      var key = KEYS[order[j2]];
      var before = cur[key];
      cur[key] = Math.min(SPACE[key][1], before + DELTA * (SPACE[key][1] - SPACE[key][0]));
      var step = cur[key] - before;
      var y = simulate(Object.assign({ seed: 20000 + rep2 }, cur));
      if (Math.abs(step) > 1e-9) {
        rows.push({ key: key, rep: rep2, step: step,
          dPopPeak: (y.peakPop - prev.peakPop) / step,
          dYrPopPeak: (y.yrPopPeak - prev.yrPopPeak) / step,
          dYrRevPeak: (y.yrRevPeak - prev.yrRevPeak) / step,
          dRelocLag: (y.relocLag - prev.relocLag) / step,
          dRelocations: (y.relocations - prev.relocations) / step,
          dDecline: (y.revenueDecline - prev.revenueDecline) / step,
          dEndowCross: (y.endowAtCross - prev.endowAtCross) / step });
      }
      prev = y;
    }
  }
} else {
  // grid: does transport geometry substitute for the endowment ratchet?
  var hs = [60, 100, 180], hf = [0.02, 0.05, 0.10], ers = [0.0004, 0.0016, 0.0040];
  var n = hs.length * hf.length * ers.length;
  for (var i3 = LO; i3 < HI; i3++) {
    var idx = i3 % n, rep3 = Math.floor(i3 / n);
    var ih = Math.floor(idx / (hf.length * ers.length));
    var if_ = Math.floor((idx % (hf.length * ers.length)) / ers.length);
    var ie3 = idx % ers.length;
    var x3 = simulate({ haulHalf: hs[ih], holdFrac: hf[if_], endowRate: ers[ie3],
      seed: 7000 + rep3 * 11 });
    var s3 = score(x3);
    rows.push({ haulHalf: hs[ih], holdFrac: hf[if_], endowRate: ers[ie3], rep: rep3,
      yrPopPeak: x3.yrPopPeak, peakPop: x3.peakPop, yrRevPeak: x3.yrRevPeak,
      relocations: x3.relocations, firstReloc: x3.firstReloc, relocLag: x3.relocLag,
      revenueDecline: x3.revenueDecline, endowAtCross: x3.endowAtCross,
      peakReach: x3.peakReach, reachMedian: x3.reachMedian,
      hitPeak: s3.hitPeak, hitLag: s3.hitLag, hitDecl: s3.hitDecl, pattern: s3.pattern });
  }
}

function toCSV(rs) {
  if (!rs.length) { fs.writeFileSync(OUT, ''); return; }
  var cols = Object.keys(rs[0]);
  var lines = [cols.join(',')];
  rs.forEach(function (row) {
    lines.push(cols.map(function (c) {
      var v = row[c];
      return (typeof v === 'number') ? +v.toPrecision(10) : v;
    }).join(','));
  });
  fs.writeFileSync(OUT, lines.join('\n') + '\n');
}
toCSV(rows);
