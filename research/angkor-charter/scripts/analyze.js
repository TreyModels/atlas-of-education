// analyze.js — reduces the recombined Monte Carlo / Morris CSVs to the numbers a paper needs.
// Node 12 compatible. Reads results/mc_all.csv and results/morris_all.csv if present.
'use strict';
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
const R = path.join(ROOT, 'results');

function readCSV(file) {
  const txt = fs.readFileSync(file, 'utf8').trim().split('\n');
  const cols = txt[0].split(',');
  return txt.slice(1).map(line => {
    const v = line.split(',');
    const o = {};
    cols.forEach((c, i) => { const x = v[i]; o[c] = (x === '' ? NaN : (isNaN(+x) ? x : +x)); });
    return o;
  });
}
function q(a, p) {
  const s = a.filter(Number.isFinite).sort((x, y) => x - y);
  if (!s.length) return NaN;
  const pos = (s.length - 1) * p, lo = Math.floor(pos), hi = Math.ceil(pos);
  return s[lo] + (s[hi] - s[lo]) * (pos - lo);
}

const out = {};
if (fs.existsSync(path.join(R, 'mc_all.csv'))) {
  const rows = readCSV(path.join(R, 'mc_all.csv'));
  const f = k => rows.map(r => r[k]).filter(Number.isFinite);
  const pop = f('pop'), died = f('armyDied'), peak = f('peakSoldiers');
  out.mc = {
    n: rows.length,
    fracRunsWithNoArmyAt1450: rows.filter(r => r.soldiers <= 0).length / rows.length,
    armyDiedQuantiles: { q05: q(died, 0.05), q25: q(died, 0.25), median: q(died, 0.5), q75: q(died, 0.75), q95: q(died, 0.95) },
    armyDiedBefore1113: rows.filter(r => r.armyDied < 1113).length / rows.length,
    armyDiedBefore1300: rows.filter(r => r.armyDied < 1300).length / rows.length,
    peakSoldiersQuantiles: { q05: q(peak, 0.05), median: q(peak, 0.5), q95: q(peak, 0.95) },
    popQuantiles: { q05: q(pop, 0.05), median: q(pop, 0.5), q95: q(pop, 0.95) },
    grainNegativeShare: rows.filter(r => r.grain < 0).length / rows.length,
    legitimacyAtFloorShare: rows.filter(r => r.legitimacy <= 0.036).length / rows.length,
    sacksPerRun: { mean: f('sacks').reduce((a, b) => a + b, 0) / rows.length, p50: q(f('sacks'), 0.5), p95: q(f('sacks'), 0.95) }
  };
}

if (fs.existsSync(path.join(R, 'morris_all.csv'))) {
  const rows = readCSV(path.join(R, 'morris_all.csv'));
  const metrics = ['dPop', 'dPop1113', 'dPeakSoldiers', 'dArmyDied', 'dGun', 'dGrain', 'dSacks', 'dBonded', 'dLegit'];
  const byKey = {};
  rows.forEach(r => { (byKey[r.key] = byKey[r.key] || []).push(r); });
  const tab = Object.keys(byKey).map(k => {
    const rs = byKey[k], o = { key: k, mu: {}, sigma: {} };
    metrics.forEach(m => {
      const v = rs.map(r => r[m]).filter(Number.isFinite);
      o.mu[m] = v.reduce((a, b) => a + b, 0) / (v.length || 1);
      const s = Math.sqrt(v.reduce((a, b) => a + (b - o.mu[m]) ** 2, 0) / (v.length || 1));
      o.sigma[m] = s;
    });
    // composite influence: normalised |mu|*sigma across population, army, monuments
    o.score = Math.abs(o.mu.dPop) / 1e5 + Math.abs(o.mu.dPeakSoldiers) * 10 + Math.abs(o.mu.dGun) * 100;
    return o;
  }).sort((a, b) => b.score - a.score);
  out.morris = {
    replicationsPerParam: rows.length / Object.keys(byKey).length,
    rankingByCompositeInfluence: tab.map(t => ({
      key: t.key, score: +t.score.toFixed(4),
      mu_pop: Math.round(t.mu.dPop), sd_pop: Math.round(t.sigma.dPop),
      mu_peakSoldiers: Math.round(t.mu.dPeakSoldiers), sd_peakSoldiers: Math.round(t.sigma.dPeakSoldiers),
      mu_armyDied: Math.round(t.mu.dArmyDied), sd_armyDied: Math.round(t.sigma.dArmyDied),
      mu_gun: +t.mu.dGun.toFixed(4), sd_gun: +t.sigma.dGun.toFixed(4)
    }))
  };
}
fs.writeFileSync(path.join(R, 'analysis.json'), JSON.stringify(out, null, 2) + '\n');
if (out.mc) {
  console.log('MC n=' + out.mc.n);
  console.log('  no army at 1450: ' + (100 * out.mc.fracRunsWithNoArmyAt1450).toFixed(1) + '%');
  console.log('  army died before 1113: ' + (100 * out.mc.armyDiedBefore1113).toFixed(1) + '%   before 1300: ' + (100 * out.mc.armyDiedBefore1300).toFixed(1) + '%');
  console.log('  armyDied median ' + out.mc.armyDiedQuantiles.median + '  [' + out.mc.armyDiedQuantiles.q05 + ', ' + out.mc.armyDiedQuantiles.q95 + ']');
  console.log('  final grain negative: ' + (100 * out.mc.grainNegativeShare).toFixed(1) + '%   legitimacy at floor: ' + (100 * out.mc.legitimacyAtFloorShare).toFixed(1) + '%');
}
if (out.morris) {
  console.log('Morris reps=' + out.morris.replicationsPerParam + '  top parameters:');
  out.morris.rankingByCompositeInfluence.slice(0, 10).forEach(t => console.log('  ' + t.key.padEnd(22) + ' pop ' + String(t.mu_pop).padStart(9) + '  peakSoldiers ' + String(t.mu_peakSoldiers).padStart(7) + '  armyDied ' + String(t.mu_armyDied).padStart(6)));
}
console.log('wrote results/analysis.json');
