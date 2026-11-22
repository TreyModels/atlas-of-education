// v8_report.js — aggregate the ten experiments into one readable table.
'use strict';
var fs = require('fs');
var R = '/root/angkor/results';

function readCSV(f) {
  var txt = fs.readFileSync(f, 'utf8').trim().split('\n');
  var cols = txt[0].split(',');
  return txt.slice(1).map(function (line) {
    var v = line.split(','), o = {};
    cols.forEach(function (c, i) { var x = v[i]; o[c] = isNaN(+x) ? x : +x; });
    return o;
  });
}
function med(a) { var s = a.filter(Number.isFinite).sort(function (x, y) { return x - y; }); return s.length ? s[Math.floor(s.length / 2)] : NaN; }
function mean(a) { var s = a.filter(Number.isFinite); return s.length ? s.reduce(function (x, y) { return x + y; }, 0) / s.length : NaN; }

var rows = readCSV(R + '/v8_all.csv');
var byExp = {};
rows.forEach(function (r) {
  byExp[r.exp] = byExp[r.exp] || {};
  byExp[r.exp][r.variant] = byExp[r.exp][r.variant] || [];
  byExp[r.exp][r.variant].push(r);
});

var order = ['E1_endowTarget', 'E2_taxBase', 'E3_ratchet_x_elite', 'E4_charterLoss', 'E5_relocCost',
  'E6_rivals', 'E7_droughtTiming', 'E8_yieldScale', 'E9_garrison', 'E10_calibratePeak'];

var out = {};
order.forEach(function (name) {
  if (!byExp[name]) return;
  var variants = Object.keys(byExp[name]);
  var tab = variants.map(function (v) {
    var rs = byExp[name][v];
    return { variant: v, n: rs.length,
      peakYr: med(rs.map(function (r) { return r.yrPopPeak; })),
      peakPop: Math.round(med(rs.map(function (r) { return r.peakPop; }))),
      relocLag: med(rs.map(function (r) { return r.relocLag; })),
      decl: +mean(rs.map(function (r) { return r.revenueDecline; })).toFixed(2),
      relocs: +mean(rs.map(function (r) { return r.relocations; })).toFixed(1),
      reach: med(rs.map(function (r) { return r.endReach; })) };
  });
  tab.sort(function (a, b) { return a.peakYr - b.peakYr; });
  out[name] = tab;
  console.log('\n=== ' + name + ' ===');
  console.log('  variant            peakYr  peakPop  lag  decline relocs reach');
  tab.forEach(function (t) {
    console.log('  ' + String(t.variant).padEnd(18) +
      String(t.peakYr).padStart(6) + String(t.peakPop).padStart(9) +
      String(t.relocLag).padStart(5) + String(t.decl).padStart(9) +
      String(t.relocs).padStart(7) + String(t.reach).padStart(6));
  });
});
fs.writeFileSync(R + '/analysis_v8.json', JSON.stringify(out, null, 2) + '\n');
console.log('\nwrote results/analysis_v8.json');
