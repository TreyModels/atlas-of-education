// v10_probe.js — trace one run. usage: node v10_probe.js [json overrides]
'use strict';
var A = require('/root/angkor/scripts/v10_abm.js');
var over = process.argv[2] ? JSON.parse(process.argv[2]) : {};
var x = A.simulate(over);
console.log('peakPop=' + x.peakPop + ' yr=' + x.yrPopPeak + ' endPop=' + x.endPop + ' popDecl=' + x.popDecline +
  ' relocs=' + x.relocations + ' first=' + x.firstReloc + ' lag=' + x.relocLag +
  ' revDecl=' + x.revenueDecline + ' eliteLand=' + x.eliteShareOfLand + ' infraEnd=' + x.endInfra +
  ' minInfra=' + x.minInfra + ' fund=' + x.meanFunded + ' capBoundYr=' + x.yrCapBound + ' aband=' + x.abandoned);
console.log('   yr     pop  popN    rev  chart  infra   hEff  netKm fundF solv  eShare  starv');
x.rows.forEach(function (r) {
  if (r.yr % 20 !== 0 && r.yr !== 800 && r.yr !== 1600) return;
  console.log('  ' + r.yr + String(Math.round(r.pop)).padStart(8) + String(r.popN).padStart(6) +
    String(Math.round(r.revenue)).padStart(7) + r.charter.toFixed(2).padStart(7) + r.infra.toFixed(2).padStart(7) +
    r.hEff.toFixed(2).padStart(7) + r.netKm.toFixed(0).padStart(7) + r.fundedFrac.toFixed(2).padStart(6) +
    r.solvency.toFixed(2).padStart(5) + r.eliteShare.toFixed(3).padStart(8) + String(r.starving).padStart(7));
});
