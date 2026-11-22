// p1_report.js — prior predictive summary: what do the models say, given only defensible guesses?
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
function q(a, p) { var s = a.filter(Number.isFinite).sort(function (x, y) { return x - y; }); if (!s.length) return NaN; var i = Math.floor((s.length - 1) * p); return s[i]; }
function mean(a) { var s = a.filter(Number.isFinite); return s.length ? s.reduce(function (x, y) { return x + y; }, 0) / s.length : NaN; }
function corr(a, b) {
  var n = Math.min(a.length, b.length), ma = 0, mb = 0, i;
  for (i = 0; i < n; i++) { ma += a[i]; mb += b[i]; } ma /= n; mb /= n;
  var num = 0, da = 0, db = 0;
  for (i = 0; i < n; i++) { var u = a[i] - ma, w = b[i] - mb; num += u * w; da += u * u; db += w * w; }
  return (da > 0 && db > 0) ? num / Math.sqrt(da * db) : NaN;
}

var rows = readCSV(R + '/p1_all.csv');
console.log('draws: ' + rows.length);
console.log('\nIDENTITY CHECK: people fed by the drawn land area');
console.log('  median ' + Math.round(q(rows.map(function (r) { return r.peopleFed; }), 0.5)) +
  '   [5%: ' + Math.round(q(rows.map(function (r) { return r.peopleFed; }), 0.05)) +
  '   95%: ' + Math.round(q(rows.map(function (r) { return r.peopleFed; }), 0.95)) + ']');

['v8', 'v9'].forEach(function (m) {
  var pk = rows.map(function (r) { return r[m + '_peakYr']; });
  var lg = rows.map(function (r) { return r[m + '_lag']; });
  var dc = rows.map(function (r) { return r[m + '_decl']; });
  var ok = rows.map(function (r) { return r[m + '_pattern']; });
  var hitP = rows.map(function (r) { return r[m + '_peak8']; });
  var hitL = rows.map(function (r) { return r[m + '_lag8']; });
  var hitD = rows.map(function (r) { return r[m + '_decl8']; });
  console.log('\n=== ' + (m === 'v8' ? 'STOCK MODEL (v8)' : 'AGENT MODEL (v9)') + ' — prior predictive ===');
  console.log('  peak year   median ' + q(pk, 0.5) + '   [5%: ' + q(pk, 0.05) + '  95%: ' + q(pk, 0.95) + ']');
  console.log('  reloc lag   median ' + q(lg, 0.5) + '   [5%: ' + q(lg, 0.05) + '  95%: ' + q(lg, 0.95) + ']');
  console.log('  revenue decline median ' + (100 * q(dc, 0.5)).toFixed(0) + '%');
  console.log('  P(peak in 1000-1400) ' + (100 * mean(hitP)).toFixed(0) + '%');
  console.log('  P(lag 20-300)        ' + (100 * mean(hitL)).toFixed(0) + '%');
  console.log('  P(decline > 20%)     ' + (100 * mean(hitD)).toFixed(0) + '%');
  console.log('  P(full pattern)      ' + (100 * mean(ok)).toFixed(0) + '%');
});

console.log('\n=== what moves the stock model peak year ===');
[['endowRate', 'endowRate'], ['y', 'y'], ['Amax', 'Amax'], ['taxRate', 'taxRate'], ['eliteGrow', 'eliteGrow']].forEach(function (p) {
  var c = corr(rows.map(function (r) { return r[p[0]]; }), rows.map(function (r) { return r.p1; }));
  var c2 = corr(rows.map(function (r) { return r[p[0]]; }), rows.map(function (r) { return r.v8_peakYr; }));
  var c3 = corr(rows.map(function (r) { return r[p[0]]; }), rows.map(function (r) { return r.v9_peakYr; }));
  console.log('  ' + p[1].padEnd(12) + '  vs v8 peakYr ' + (isNaN(c2) ? 'n/a' : (c2 >= 0 ? ' ' : '') + c2.toFixed(2)) +
    '   vs v9 peakYr ' + (isNaN(c3) ? 'n/a' : (c3 >= 0 ? ' ' : '') + c3.toFixed(2)));
});

// the headline: where does the peak land at the derived endowment rate?
var near = rows.filter(function (r) { return r.endowRate > 0.0008 && r.endowRate < 0.0015; });
if (near.length) {
  console.log('\n=== at the DERIVED endowment rate (0.0008-0.0015/yr, n=' + near.length + ') ===');
  console.log('  v8 peak year median ' + q(near.map(function (r) { return r.v8_peakYr; }), 0.5));
  console.log('  v9 peak year median ' + q(near.map(function (r) { return r.v9_peakYr; }), 0.5));
  console.log('  historical apogee ~1100-1200');
}
var out = { draws: rows.length };
fs.writeFileSync(R + '/analysis_p1.json', JSON.stringify(out, null, 2) + '\n');
