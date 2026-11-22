// v6_analyze.js — reduce the recombined shard CSVs to the tables the paper needs.
'use strict';
var fs = require('fs');
var path = require('path');
var R = '/root/angkor/results';

function readCSV(f) {
  var txt = fs.readFileSync(f, 'utf8').trim().split('\n');
  var cols = txt[0].split(',');
  return txt.slice(1).map(function (line) {
    var v = line.split(','), o = {};
    cols.forEach(function (c, i) { var x = v[i]; o[c] = (x === '' ? NaN : (isNaN(+x) ? x : +x)); });
    return o;
  });
}
function q(a, p) {
  var s = a.filter(Number.isFinite).sort(function (x, y) { return x - y; });
  if (!s.length) return NaN;
  var pos = (s.length - 1) * p, lo = Math.floor(pos), hi = Math.ceil(pos);
  return s[lo] + (s[hi] - s[lo]) * (pos - lo);
}

var out = {};

// ---------- factorial: which switch combinations produce the pattern ----------
if (fs.existsSync(path.join(R, 'v7fact_all.csv'))) {
  var f = readCSV(path.join(R, 'v7fact_all.csv'));
  var cells = {};
  f.forEach(function (r) {
    var c = r.cell;
    cells[c] = cells[c] || { n: 0, pattern: 0, peak: 0, lag: 0, decl: 0, sw: {
      ratchet: r.ratchet, charter: r.charter, climate: r.climate, raid: r.raid, transport: r.transport } };
    cells[c].n++;
    cells[c].pattern += r.pattern; cells[c].peak += r.hitPeak;
    cells[c].lag += r.hitLag; cells[c].decl += r.hitDecl;
  });
  var tab = Object.keys(cells).map(function (c) {
    var o = cells[c];
    return { cell: +c, sw: o.sw, n: o.n, pPattern: +(o.pattern / o.n).toFixed(3),
      pPeak: +(o.peak / o.n).toFixed(3), pLag: +(o.lag / o.n).toFixed(3), pDecl: +(o.decl / o.n).toFixed(3) };
  }).sort(function (a, b) { return b.pPattern - a.pPattern; });

  // main effect of each switch on P(pattern)
  var switches = ['ratchet', 'charter', 'climate', 'raid', 'transport'];
  var main = {};
  switches.forEach(function (s) {
    var on = tab.filter(function (t) { return t.sw[s] === 1; });
    var off = tab.filter(function (t) { return t.sw[s] === 0; });
    var m = function (a) { return a.reduce(function (x, y) { return x + y.pPattern; }, 0) / a.length; };
    main[s] = +(m(on) - m(off)).toFixed(3);
  });
  out.factorial = { n: f.length, topCells: tab.slice(0, 10), mainEffectOnPattern: main };
}

// ---------- morris: parameter sensitivity ----------
if (fs.existsSync(path.join(R, 'v7mor_all.csv'))) {
  var m2 = readCSV(path.join(R, 'v7mor_all.csv'));
  var metrics = ['dPopPeak', 'dYrPopPeak', 'dYrRevPeak', 'dRelocLag', 'dRelocations', 'dDecline', 'dEndowCross'];
  var byKey = {};
  m2.forEach(function (r) { (byKey[r.key] = byKey[r.key] || []).push(r); });
  var rank = Object.keys(byKey).map(function (k) {
    var rs = byKey[k], o = { key: k, mu: {}, sigma: {}, score: 0 };
    metrics.forEach(function (mt) {
      var v = rs.map(function (r) { return r[mt]; }).filter(Number.isFinite);
      var mean = v.reduce(function (a, b) { return a + b; }, 0) / (v.length || 1);
      var sd = Math.sqrt(v.reduce(function (a, b) { return a + (b - mean) * (b - mean); }, 0) / (v.length || 1));
      o.mu[mt] = mean; o.sigma[mt] = sd;
    });
    // normalise each metric by its cross-parameter scale so the composite is comparable
    return o;
  });
  // scale-normalise then composite
  var scales = {};
  metrics.forEach(function (mt) {
    var vals = rank.map(function (r) { return Math.abs(r.mu[mt]); }).filter(Number.isFinite);
    scales[mt] = Math.max.apply(null, vals) || 1;
  });
  rank.forEach(function (r) {
    metrics.forEach(function (mt) { r.score += Math.abs(r.mu[mt]) / scales[mt]; });
    r.score = +r.score.toFixed(3);
  });
  rank.sort(function (a, b) { return b.score - a.score; });
  out.morris = { n: m2.length, repsPerParam: m2.length / Object.keys(byKey).length,
    ranking: rank.map(function (r) {
      var o = { key: r.key, score: r.score };
      metrics.forEach(function (mt) { o[mt] = +r.mu[mt].toPrecision(4); });
      return o;
    }) };
}

// ---------- grid: yield x ratchet x land ceiling ----------
if (fs.existsSync(path.join(R, 'v7grid_all.csv'))) {
  var g = readCSV(path.join(R, 'v7grid_all.csv'));
  var cells2 = {};
  g.forEach(function (r) {
    var k = r.haulHalf + '|' + r.holdFrac + '|' + r.endowRate;
    cells2[k] = cells2[k] || { n: 0, pattern: 0, peaks: [], lags: [], decl: [], reach: [] };
    cells2[k].n++; cells2[k].pattern += r.pattern;
    cells2[k].peaks.push(r.yrPopPeak); cells2[k].lags.push(r.relocLag); cells2[k].decl.push(r.revenueDecline); cells2[k].reach.push(r.reachMedian);
  });
  out.grid = Object.keys(cells2).map(function (k) {
    var o = cells2[k], parts = k.split('|');
    return { haulHalf: +parts[0], holdFrac: +parts[1], endowRate: +parts[2], n: o.n,
      pPattern: +(o.pattern / o.n).toFixed(3),
      yrPopPeakMedian: q(o.peaks, 0.5), relocLagMedian: q(o.lags, 0.5),
      declineMedian: +q(o.decl, 0.5).toFixed(3), reachMedian: q(o.reach, 0.5) };
  }).sort(function (a, b) { return b.pPattern - a.pPattern; });
}

fs.writeFileSync(path.join(R, 'analysis_v7.json'), JSON.stringify(out, null, 2) + '\n');

if (out.factorial) {
  console.log('=== FACTORIAL (n=' + out.factorial.n + ') ===');
  console.log('main effects on P(pattern):');
  Object.keys(out.factorial.mainEffectOnPattern).forEach(function (k) {
    console.log('  ' + k.padEnd(10) + (out.factorial.mainEffectOnPattern[k] > 0 ? '+' : '') + out.factorial.mainEffectOnPattern[k]);
  });
  console.log('top cells:');
  out.factorial.topCells.forEach(function (t) {
    var s = t.sw;
    console.log('  cell' + String(t.cell).padStart(3) + ' rat' + s.ratchet + ' chr' + s.charter + ' cli' + s.climate + ' rai' + s.raid + ' tra' + s.transport +
      '  P=' + t.pPattern + '  peak=' + t.pPeak + ' lag=' + t.pLag + ' decl=' + t.pDecl);
  });
}
if (out.morris) {
  console.log('\n=== MORRIS (n=' + out.morris.n + ', ' + out.morris.repsPerParam + ' reps/param) ===');
  out.morris.ranking.forEach(function (r) {
    console.log('  ' + r.key.padEnd(16) + 'score ' + String(r.score).padStart(6) +
      '  yrPopPeak ' + String(r.dYrPopPeak).padStart(8) + '  relocLag ' + String(r.dRelocLag).padStart(9) +
      '  decline ' + String(r.dDecline).padStart(7));
  });
}
if (out.grid) {
  console.log('\n=== GRID top ===');
  out.grid.slice(0, 12).forEach(function (r) {
    console.log('  haulHalf=' + String(r.haulHalf).padStart(3) + ' hold=' + String(r.holdFrac).padEnd(5) + ' ratchet=' + String(r.endowRate).padEnd(6) +
      ' P=' + String(r.pPattern).padEnd(5) + ' peakYr=' + String(r.yrPopPeakMedian).padStart(4) + ' lag=' + String(r.relocLagMedian).padStart(5) + ' decl=' + String(r.declineMedian).padEnd(5) + ' reach=' + r.reachMedian);
  });
}
console.log('\nwrote results/analysis_v7.json');
