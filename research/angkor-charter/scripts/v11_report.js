// v10_report.js — reduce results/vN_all.csv. usage: node v10_report.js <N>
'use strict';
var fs = require('fs');
var V = process.argv[2] || '11';
var R = '/root/angkor/results';
var rows = fs.readFileSync(R + '/v' + V + '_all.csv', 'utf8').trim().split('\n');
var cols = rows[0].split(',');
var data = rows.slice(1).map(function (line) {
  var v = line.match(/("([^"]|"")*"|[^,]*)(,|$)/g).map(function (s) { return s.replace(/,$/, ''); });
  var o = {};
  cols.forEach(function (c, i) { var x = (v[i] || '').replace(/^"|"$/g, ''); o[c] = (x !== '' && !isNaN(+x)) ? +x : x; });
  return o;
});
function med(a) { var s = a.filter(Number.isFinite).sort(function (x, y) { return x - y; }); return s.length ? s[Math.floor(s.length / 2)] : NaN; }
function mean(a) { var s = a.filter(Number.isFinite); return s.length ? s.reduce(function (x, y) { return x + y; }, 0) / s.length : NaN; }
function f(x, d) { return isNaN(x) ? '  n/a' : x.toFixed(d === undefined ? 2 : d); }

var byExp = {};
data.forEach(function (r) { (byExp[r.exp] = byExp[r.exp] || {}); (byExp[r.exp][r.variant] = byExp[r.exp][r.variant] || []).push(r); });

var out = {};
Object.keys(byExp).forEach(function (name) {
  var tab = Object.keys(byExp[name]).map(function (v) {
    var rs = byExp[name][v];
    return { variant: v, n: rs.length,
      peakYr: med(rs.map(function (r) { return r.yrPopPeak; })),
      peakPop: Math.round(med(rs.map(function (r) { return r.peakPop; }))),
      endPop: Math.round(med(rs.map(function (r) { return r.endPop; }))),
      lag: med(rs.map(function (r) { return r.relocLag; })),
      decl: +mean(rs.map(function (r) { return r.revenueDecline; })).toFixed(2),
      popDecl: +mean(rs.map(function (r) { return r.popDecline; })).toFixed(2),
      eliteLand: +mean(rs.map(function (r) { return r.eliteShareOfLand; })).toFixed(2),
      relocs: +mean(rs.map(function (r) { return r.relocations; })).toFixed(1),
      fund: +mean(rs.map(function (r) { return r.meanFunded; })).toFixed(2),
      minInfra: +mean(rs.map(function (r) { return r.minInfra; })).toFixed(2),
      interior: +mean(rs.map(function (r) { return r.interiorPeak; })).toFixed(2),
      capYr: med(rs.map(function (r) { return r.yrCapBound; })),
      pPattern: +mean(rs.map(function (r) { return r.pattern; })).toFixed(2),
      pElite: +mean(rs.map(function (r) { return r.hitElite; })).toFixed(2) };
  });
  out[name] = tab;
  console.log('\n=== ' + name + ' ===');
  console.log('  variant      peakYr  peakPop   endPop    lag   decl popD elite reloc fund mnInf int capYr  P  E');
  tab.forEach(function (t) {
    console.log('  ' + String(t.variant).padEnd(12) + String(t.peakYr).padStart(7) + String(t.peakPop).padStart(9) +
      String(t.endPop).padStart(8) + String(t.lag).padStart(7) + String(t.decl).padStart(7) + String(t.popDecl).padStart(5) +
      String(t.eliteLand).padStart(6) + String(t.relocs).padStart(6) + String(t.fund).padStart(5) +
      String(t.minInfra).padStart(6) + String(t.interior).padStart(4) + String(t.capYr).padStart(7) +
      String(t.pPattern).padStart(4) + String(t.pElite).padStart(4));
  });
});

// ranking against the historical targets
function dist(t) {
  var dp = t.peakYr >= 1100 && t.peakYr <= 1250 ? 0 : Math.min(Math.abs(t.peakYr - 1100), Math.abs(t.peakYr - 1250));
  var dl = (t.lag >= 50 && t.lag <= 250) ? 0 : (t.lag < 0 ? 400 : Math.min(Math.abs(t.lag - 50), Math.abs(t.lag - 250)));
  var dd = t.decl >= 0.30 ? 0 : (0.30 - t.decl) * 200;
  var de = (t.eliteLand >= 0.30 && t.eliteLand <= 0.60) ? 0 : Math.min(Math.abs(t.eliteLand - 0.30), Math.abs(t.eliteLand - 0.60)) * 100;
  return +(dp + dl + dd + de).toFixed(1);
}
var all = [];
Object.keys(out).forEach(function (k) { if (k.indexOf('X10') < 0) out[k].forEach(function (t) { t.exp = k; t.dist = dist(t); all.push(t); }); });
all.sort(function (a, b) { return a.dist - b.dist; });
console.log('\n=== closest to the historical target (peak 1100-1250, lag 50-250, decline>0.30, elite 0.3-0.6) ===');
console.log('  rank exp                variant      peakYr    lag  decl elite  P  dist');
all.slice(0, 12).forEach(function (t, i) {
  console.log('  ' + String(i + 1).padStart(4) + ' ' + t.exp.padEnd(18) + String(t.variant).padEnd(12) +
    String(t.peakYr).padStart(7) + String(t.lag).padStart(7) + String(t.decl).padStart(6) +
    String(t.eliteLand).padStart(6) + String(t.pPattern).padStart(4) + String(t.dist).padStart(6));
});

if (byExp.X10_montecarlo) {
  var mc = [];
  Object.keys(byExp.X10_montecarlo).forEach(function (v) {
    byExp.X10_montecarlo[v].forEach(function (r) {
      if (!r.mc) return;
      var o = { y: r.pattern, peak: r.yrPopPeak, decl: r.revenueDecline, lag: r.relocLag, el: r.eliteShareOfLand, pd: r.popDecline };
      String(r.mc).split(';').forEach(function (kv) { var p = kv.split('='); o[p[0]] = +p[1]; });
      mc.push(o);
    });
  });
  function corr(a, b) {
    var n = Math.min(a.length, b.length), ma = 0, mb = 0, i;
    if (n < 6) return NaN;
    for (i = 0; i < n; i++) { ma += a[i]; mb += b[i]; }
    ma /= n; mb /= n;
    var num = 0, da = 0, db = 0;
    for (i = 0; i < n; i++) { var u = a[i] - ma, w = b[i] - mb; num += u * w; da += u * u; db += w * w; }
    return (da > 1e-12 && db > 1e-12) ? num / Math.sqrt(da * db) : NaN;
  }
  var keys = Object.keys(mc[0]).filter(function (k) { return ['y', 'peak', 'decl', 'lag', 'el', 'pd'].indexOf(k) < 0; });
  console.log('\n=== X10 Monte Carlo (n=' + mc.length + '): correlation with outcome ===');
  console.log('  parameter        pattern   peakYr    decl     lag  elite popDecl');
  keys.map(function (k) {
    return { k: k, cp: corr(mc.map(function (r) { return r[k]; }), mc.map(function (r) { return r.y; })),
      ck: corr(mc.map(function (r) { return r[k]; }), mc.map(function (r) { return r.peak; })),
      cd: corr(mc.map(function (r) { return r[k]; }), mc.map(function (r) { return r.decl; })),
      cl: corr(mc.map(function (r) { return r[k]; }), mc.map(function (r) { return r.lag; })),
      ce: corr(mc.map(function (r) { return r[k]; }), mc.map(function (r) { return r.el; })),
      cpd: corr(mc.map(function (r) { return r[k]; }), mc.map(function (r) { return r.pd; })) };
  }).sort(function (a, b) { return Math.abs(b.cp) - Math.abs(a.cp); }).forEach(function (r) {
    console.log('  ' + r.k.padEnd(16) + f(r.cp) + f(r.ck, 1).padStart(9) + f(r.cd, 1).padStart(8) +
      f(r.cl, 0).padStart(7) + f(r.ce, 1).padStart(7) + f(r.cpd, 1).padStart(8));
  });
  var pat = mean(mc.map(function (r) { return r.y; }));
  var inter = mean(data.filter(function (r) { return r.exp === 'X10_montecarlo'; }).map(function (r) { return r.interiorPeak; }));
  console.log('  MC: pattern hit rate=' + pat.toFixed(2) + '  interior-peak rate=' + inter.toFixed(2));
}

fs.writeFileSync(R + '/analysis_v' + V + '.json', JSON.stringify(out, null, 2) + '\n');
console.log('\nwrote results/analysis_v' + V + '.json');
