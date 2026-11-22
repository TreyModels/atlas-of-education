// dump_facts.js v2 — everything check_claims.js v2 asserts on, including the
// falsification tests MODEL_CARD promises. Node 12 compatible.
'use strict';
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const ROOT = path.resolve(__dirname, '..');
const M = require(path.join(ROOT, 'model.js'));
const appSrc = fs.readFileSync(path.join(ROOT, 'app.js'), 'utf8');
const modelSrc = fs.readFileSync(path.join(ROOT, 'model.js'), 'utf8');
const D = M.DEFAULTS;

// --- source-level facts (the prose lives in three files; record what each one says) ---
const ui = [];
let m; const uiRe = /\['([A-Za-z0-9_]+)','([^']*)',(-?[\d.]+),(-?[\d.]+),(-?[\d.]+)/g;
while ((m = uiRe.exec(appSrc))) ui.push({ key: m[1], min: +m[3], max: +m[4] });
const sweepBounds = {};
const bb = modelSrc.match(/const bounds=\{([^}]+)\};/);
if (bb) { const r = /([A-Za-z0-9_]+):\[([\d.]+),([\d.]+)\]/g; let b; while ((b = r.exec(bb[1]))) sweepBounds[b[1]] = [+b[2], +b[3]]; }
const claims = {
  sweepDescribedAs: /randomi[sz]ed/.test(modelSrc) ? 'randomized' : 'deterministic',
  sweepUsesRng: /10000\+i\*101/.test(modelSrc) === false,
  sweepR2OnNoiseCovered: false
};

// --- run diagnostics ---
function diagnose(p, seed) {
  const x = M.simulate(Object.assign({}, D, p, { seed: seed || 42 }), { cadence: 1 });
  const t = x.timeline;
  let seen = false, armyDied = -1, peak = 0, noArmy = 0, noSurplus = 0, legitFloor = 0;
  for (const r of t) {
    if (r.soldiers > peak) peak = r.soldiers;
    if (r.soldiers > 0) seen = true; else { noArmy++; if (seen && armyDied < 0) armyDied = r.year; }
    if (r.surplus <= 0) noSurplus++;
    if (r.legitimacy <= 0.0355) legitFloor++;
  }
  return {
    pop: Math.round(x.final.pop), soldiers: x.final.soldiers, peakSoldiers: peak,
    armyDied: armyDied, firstZeroSoldiers: (function () { const r = t.find(function (q) { return q.soldiers <= 0; }); return r ? r.year : null; })(),
    firstZeroSurplus: (function () { const r = t.find(function (q) { return q.surplus <= 0; }); return r ? r.year : null; })(),
    fracYearsNoArmy: +(noArmy / t.length).toFixed(3), fracYearsNoSurplus: +(noSurplus / t.length).toFixed(3),
    fracLegitimacyAtFloor: +(legitFloor / t.length).toFixed(3),
    grainBalance: Math.round(x.final.grainBalance), foodRatio: +x.final.foodRatio.toFixed(3),
    bonded: Math.round(x.final.bonded), sacks: x.events.sacks, wars: x.events.wars,
    legitimacy: +x.final.legitimacy.toFixed(3), gunIndex: +x.final.ornamentalIndex.toFixed(4)
  };
}

const diag = { reference: diagnose({}) };
const presetRuns = {};
Object.keys(M.PRESETS).forEach(function (k) {
  const p = Object.assign({}, M.PRESETS[k].patch);
  presetRuns[k] = diagnose(p);
  diag[k] = presetRuns[k];
});

const raidCounterfactual = {
  reference: diagnose({}), noRaid: diagnose({ raidIntensity: 0 }), maxRaid: diagnose({ raidIntensity: 0.94 })
};

const seeds = [42, 7, 1234, 999, 2026, 11, 2024, 31337];
const referenceAcrossSeeds = seeds.map(function (s) { return Object.assign({ seed: s }, diagnose({}, s)); });

const facts = {
  modelVersion: '1.0',
  generator: 'scripts/dump_facts.js',
  modelHash: crypto.createHash('sha256').update(modelSrc).digest('hex'),
  appHash: crypto.createHash('sha256').update(appSrc).digest('hex'),
  gridCells: (function () { const x = M.simulate(D); return x.snapshots[x.snapshots.length - 1].cells.length; })(),
  defaults: D, uiParams: ui, sweepBounds: sweepBounds,
  presets: Object.keys(M.PRESETS),
  claims: claims,
  defaultSweepUnused: Object.keys(D).filter(function (k) {
    return ['start', 'end', 'seed', 'population', 'regionKm2'].indexOf(k) < 0 && !sweepBounds[k];
  }),
  reference: {
    pop: diag.reference.pop, soldiers: diag.reference.soldiers,
    grainBalance: diag.reference.grainBalance, foodRatio: diag.reference.foodRatio
  },
  diag: diag, presetRuns: presetRuns, raidCounterfactual: raidCounterfactual,
  referenceAcrossSeeds: referenceAcrossSeeds
};
fs.mkdirSync(path.join(ROOT, 'out'), { recursive: true });
fs.writeFileSync(path.join(ROOT, 'out', 'facts.json'), JSON.stringify(facts, null, 2) + '\n');
console.log('facts.json written; model sha256 ' + facts.modelHash.slice(0, 12));
