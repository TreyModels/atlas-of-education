// check_claims.js v2 — the gate for the Angkor Atlas model.
// Covers both the original 1.0 claims and the five falsification tests MODEL_CARD
// promises for the next version (tests 1, 3 are now machine-checked).
'use strict';
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
const F = JSON.parse(fs.readFileSync(path.join(ROOT, 'out', 'facts.json'), 'utf8'));

let passes = 0; const fails = [];
// hold(id, cond, msg): PASS when cond true, FAIL when false
function hold(id, cond, msg) { if (cond) passes++; else fails.push(id + ': ' + msg); }
// reject(id, cond, msg): FAIL when cond true (use for claims the model currently breaks)
function reject(id, cond, msg) { if (cond) fails.push(id + ': ' + msg); else passes++; }

// ---------------- structural ----------------
hold('S1-grid', F.gridCells === 140, 'MODEL_CARD: 140 spatial cells; found ' + F.gridCells);
hold('S2-presets', Object.keys(F.presets).length === 9, '9 presets expected; found ' + Object.keys(F.presets).length);
hold('S3-span', F.defaults.start === 850 && F.defaults.end === 1450, 'span ' + F.defaults.start + '-' + F.defaults.end);

// ---------------- the headline claim ----------------
hold('C1-soldiers-0-at-1450', F.reference.soldiers === 0,
  'RESULTS_README: reference ends with zero soldiers in 1450 — held (' + F.reference.soldiers + ')');

// ---------------- falsification test 1: food balance ----------------
// A plausible 12th-13th c. population within supported cultivated area and feasible transport.
// We can only check the model's own claim of internal consistency: grain balance should not be
// structurally negative in the reference preset.
const dref = F.diag.reference;
reject('F1-food-balance', F.reference.grainBalance < 0,
  'TEST 1 (food balance) FAILS: reference grain balance ' + F.reference.grainBalance + ' t/yr, foodRatio ' +
  F.reference.foodRatio + '; deficit starts in ' + dref.firstZeroSurplus + ' and never recovers (' +
  (100 * dref.fracYearsNoSurplus).toFixed(0) + '% of years have zero surplus). The model card asks this test of v2, ' +
  'but the engine cannot even satisfy it with the reference preset, so no plausible population is reachable.');

// ---------------- falsification test 3: raiding independence ----------------
const cf = F.raidCounterfactual;
reject('F3-raiding-independence', true,
  'TEST 3 (raiding independence) is UNFALSIFIABLE as built: raidIntensity 0.45->0 changes final population by ' +
  ((100 * cf.noRaid.pop / cf.reference.pop) - 100).toFixed(1) + '% (' + cf.reference.pop + ' -> ' + cf.noRaid.pop + '), and ' +
  '0.94 gives ' + cf.maxRaid.pop + '. The captive channel carries ' + cf.noRaid.bonded + ' -> ' + cf.maxRaid.bonded +
  ' bonded people, i.e. <0.4% of a 780k population. A test the engine cannot fail is not a test.');

// ---------------- army dynamics ----------------
hold('A1-army-zero-not-late', dref.firstZeroSoldiers > 1200,
  'army hits zero in ' + dref.firstZeroSoldiers + '; deficit from ' + dref.firstZeroSurplus + '. Since Angkor Wat is 1113, the ' +
  'reference world has no army for the entire monumental period and ' + (100 * dref.fracYearsNoArmy).toFixed(0) +
  '% of simulated years. RESULTS_README calls this a 1450 end-point artefact; it is a 930s collapse.');
const zeroArmy = Object.keys(F.presetRuns).filter(function (k) { return F.presetRuns[k].soldiers === 0; });
hold('A2-presets-keep-an-army', zeroArmy.length < 9,
  zeroArmy.length + '/9 presets end with no soldiers (' + zeroArmy.join(', ') + '), including raiding and mandala ' +
  'whose subject is the army. Comparing them compares two zeros.');
hold('A3-legitimacy-alive', dref.fracLegitimacyAtFloor < 0.5,
  'courtLegitimacy on its 0.035 floor in ' + (100 * dref.fracLegitimacyAtFloor).toFixed(0) +
  '% of years; ends at ' + cf.reference.legitimacy + ' for every raid level. Narratives keyed to court strength ride a dead variable.');

// ---------------- experimentation honesty ----------------
const pops = F.referenceAcrossSeeds.map(function (r) { return r.pop; });
const spread = 100 * (Math.max.apply(null, pops) - Math.min.apply(null, pops)) / Math.min.apply(null, pops);
reject('E1-seed-noise-quantified', spread > 5,
  'reference final population spans ' + Math.min.apply(null, pops) + '-' + Math.max.apply(null, pops) + ' across 5 seeds (' +
  spread.toFixed(1) + '%). The result must be reported with the seed distribution, not as a point; ' +
  'the reported estates effect (~90k) is the same order as this noise.');
hold('E2-sweep-coverage', F.defaultSweepUnused.length < 8,
  F.defaultSweepUnused.length + '/28 substantive defaults never perturbed, including buildShare, warExpense, ' +
  'monumentSkill, templeAutonomy, defenseSpend — the variables the monument/army stories are made of.');
reject('E3-sweep-not-randomised', /randomi[sz]ed/.test(F.claims.sweepDescribedAs) && !F.claims.sweepUsesRng,
  'MODEL_CARD says "randomized parameter-sweep OLS"; sweep() sets seed=10000+i*101 with no RNG, so reruns are ' +
  'bit-identical. Replace the word or add a real design (LHS / Sobol).');
hold('E4-ols-r2-interpretable', F.claims.sweepR2OnNoiseCovered,
  'R2 0.99/0.95 with 5 free parameters is the simulator\'s determinism, not a finding; only the sacks regression (R2~0.24) carries noise.');

// ---------------- report ----------------
const lines = ['PASS ' + passes];
lines.push('FAIL ' + fails.length);
fails.forEach(function (f) { lines.push('  FAIL ' + f); });
console.log(lines.join('\n'));
process.exit(fails.length ? 1 : 0);
