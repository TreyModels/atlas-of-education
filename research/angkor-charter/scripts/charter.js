// charter.js — Angkor v2.0 "charter state" engine.
// A separate, minimal engine built to answer ONE question: can a low-density agrarian
// polity rise, peak and fall from endogenous mechanisms, with no imposed 1431 script?
//
// Four state variables:
//   charter  — portable legitimacy (0..1). Survives the loss of a capital, decays when
//              the revenue base contracts, is rebuilt by patronage.
//   reach    — administrative radius (km). What the court can actually tax.
//   grain    — granary stock (t). Draws down in deficit years.
//   pop      — aggregate regional population, distributed over N cells by suitability.
//
// Three endogenous exits (the "fall" is a RESULT, not a parameter):
//   E1 revenue collapse   (reach shrinks below the cost of the water network)
//   E2 capital relocation (court moves to the trade geography, as Lovek/Oudong)
//   E3 dispersal          (population thins; no capital left to lose)
//
// Usage: node scripts/charter.js <experiment> <lo> <hi> <outfile>
'use strict';
const fs = require('fs');

function rng(seed) { let a = (seed >>> 0) || 1; return function () { a += 0x6D2B79F5; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
function normal(r) { const u = 1 - r(), v = 1 - r(); return Math.sqrt(-2 * Math.log(Math.max(1e-9, u))) * Math.cos(2 * Math.PI * v); }
const clamp = (x, a, b) => Math.max(a, Math.min(b, x));

const P = {
  // landscape
  cells: 60, area: 3000,      // km2 of the settlement complex
  arableFrac: 0.37,
  yieldT: 1.6, lossPct: 16, riceKg: 200, importsT: 6000,
  // demography
  pop0: 250000, growth: 0.0065, carryMult: 1.0,
  // economy
  householdTax: 0.11,          // share of household surplus the court extracts when reach is max
  reachMax: 220, reach0: 40,   // km
  // charter
  charter0: 0.45, charterGain: 0.012, charterDecay: 0.004, charterOnCapture: 0.5,
  patronageShare: 0.18,
  // water network: maintenance cost scales superlinearly with the network a state must hold
  infraKm: 90, maintBase: 0.9, maintShape: 1.0, maintainerShare: 0.36,
  // class mobility (the elite-leaves-first test lives here)
  mobilityElite: 0.55, mobilitySpecialist: 0.35, mobilityFarmer: 0.05,
  relocateThreshold: 0.62,
  // war / capture
  raidRate: 0.45, captureRate: 0.020, warShare: 0.28,
  // climate
  climateVol: 0.11, drought0: 0.0, droughtYear: 1300, droughtSlope: 0.0,
  // horizon
  start: 850, end: 1500, seed: 42, storeYears: 1.5
};

function simulate(over) {
  const p = Object.assign({}, P, over || {});
  const r = rng(p.seed);
  const s = {
    pop: p.pop0, charter: p.charter0, reach: p.reach0, grain: 0, infra: 0.8,
    capitalAlive: 1, capitalLatent: 1, patronDays: 0, warCapture: 0, sacks: 0,
    relocations: 0, yrPeak: p.start, peakPop: 0, exitYear: null, exitKind: null,
    popElite: p.pop0 * 0.02, popSpec: p.pop0 * 0.08,  // shares of the mobile classes
    thin: 0
  };
  const out = [];
  const arable = p.cells * (p.area / p.cells) * p.arableFrac; // km2 of rice
  const carry = (arable * 100 * p.yieldT * (1 - p.lossPct / 100)) / (p.riceKg / 1000); // people fed (t -> kg -> persons)
  for (let year = p.start; year <= p.end; year++) {
    // --- climate ---
    const seasonal = clamp((year - p.droughtYear) / 150, 0, 1);
    const shock = clamp(normal(r) * p.climateVol - (p.drought0 + p.droughtSlope * seasonal) * 0.42, -0.72, 0.55);
    // --- infrastructure maintenance: cost rises faster than area as reach grows ---
    const netDemand = (p.infraKm + p.reach * 1.4) * (1 + p.reach / 600);
    const maintNeed = netDemand * 1000 * (p.maintBase + 4 * p.maintShape * (1 - s.infra)); // person-days
    const adults = s.pop * 0.45;
    const laborPool = adults * 180 * 0.25; // available non-farming person-days
    const maintLabor = Math.min(maintNeed, laborPool * p.maintainerShare);
    const sat = clamp(maintLabor / Math.max(1, maintNeed), 0, 1.2);
    s.infra = clamp(s.infra + 0.006 * sat - 0.0055 * (p.maintBase) - clamp(-shock * 0.038, 0, 0.075), 0.03, 1);
    // --- harvest ---
    const hEff = clamp(1 - 0.45 * (1 - s.infra), 0.46, 1.12);
    const weather = clamp(1 + shock, 0.16, 1.55);
    const gross = arable * 100 * p.yieldT * weather * hEff * p.carryMult * (1 - p.lossPct / 100);
    const imports = p.importsT * 0.8;
    const demand = s.pop * p.riceKg / 1000;
    const balance = gross + imports - demand;
    const cap = demand * clamp(p.storeYears, 0.5, 4);
    s.grain = clamp(s.grain + balance, -cap * 0.4, cap);
    // --- court revenue: proportional to reach and charter, not to total population ---
    const reachFrac = clamp(s.reach / p.reachMax, 0, 1.2);
    const surplusHousehold = Math.max(0, gross - demand * 0.72);
    const revenue = surplusHousehold * p.householdTax * reachFrac * clamp(0.4 + s.charter, 0.3, 1.6);
    // --- war: capture is the payoff (charter-state behaviour 2) ---
    const warBudget = revenue * p.warShare;
    const army = Math.min(s.pop * 0.035, warBudget / 0.12);
    const rivalPower = Math.max(1, (9.5 + 5 * Math.sin((year - 842) / 67) + 0.014 * (year - 850)) * (0.72 + 0.48 * p.raidRate));
    const courtPower = (army / 2500) * (0.45 + 0.85 * s.charter) + s.charter * 7 + clamp(surplusHousehold / 16000, 0, 7);
    const winP = clamp(courtPower / (courtPower + rivalPower), 0, 1);
    if (winP > 0.62) {
      const captives = Math.max(0, r() < winP * p.raidRate ? p.captureRate * rivalPower * 900 : 0);
      s.pop += captives; s.warCapture += captives; s.charter = clamp(s.charter + p.charterOnCapture * 0.05, 0, 1);
    } else if (winP < 0.45 && r() < (1 - winP) * p.raidRate * 0.25) {
      s.sacks++; s.capitalLatent = clamp(s.capitalLatent - 0.30, 0, 1); s.pop *= 0.97;
    }
    // --- charter dynamics: patronage when rich, decay when poor ---
    s.patronDays = revenue * p.patronageShare * 1000 / 0.45;
    const patronEffect = clamp(Math.log1p(s.patronDays / 500000) * 0.010, 0, 0.014);
    const legitSignal = clamp(balance / Math.max(1, demand), -1, 1);
    s.charter = clamp(s.charter + patronEffect + p.charterGain * winP * 0.5 + 0.004 * legitSignal
      - p.charterDecay * (1 - reachFrac) - 0.004 * (s.capitalAlive ? 0 : 1), 0.0, 1);
    // --- administrative reach: grows with charter, shrinks when the network fails ---
    const reachTarget = p.reach0 + (p.reachMax - p.reach0) * s.charter * clamp(s.infra, 0.2, 1.1);
    s.reach = clamp(s.reach + (reachTarget - s.reach) * 0.06, 8, p.reachMax * 1.1);
    // --- population: logistic with a mobile-class gradient (elite leaves first) ---
    const pressure = s.pop / (carry * p.carryMult);
    const netGrowth = p.growth * (1 - pressure) + 0.004 * clamp(balance / Math.max(1, demand), -1, 1);
    // mortality phase: a sustained deficit kills faster than mobility removes
    if (balance < 0) s.pop *= (1 - clamp(-balance / Math.max(1, demand), 0, 1) * 0.02);
    s.pop = Math.max(20000, s.pop * (1 + netGrowth));
    // dispersal of the mobile classes when the court's reach fails
    if (s.charter < p.relocateThreshold * 0.55 || s.infra < 0.35) {
      const eliteExit = p.mobilityElite * (1 - s.charter / p.relocateThreshold);
      const specExit = p.mobilitySpecialist * (1 - s.charter / p.relocateThreshold);
      s.popElite *= (1 - clamp(eliteExit, 0, 0.08));
      s.popSpec *= (1 - clamp(specExit, 0, 0.06));
    }
    // --- exit detection (endogenous, no scripted 1431) ---
    if (s.capitalAlive && (s.reach < p.reachMax * 0.30 || s.grain < -cap * 0.35)) {
      s.capitalAlive = 0; s.relocations++; s.exitYear = year; s.exitKind = 'relocation';
    }
    if (s.pop > s.peakPop) { s.peakPop = s.pop; s.yrPeak = year; }
    out.push({ year, pop: s.pop, charter: s.charter, reach: s.reach, grain: s.grain, infra: s.infra,
      capitalAlive: s.capitalAlive, sacks: s.sacks, capture: s.warCapture, elite: s.popElite, spec: s.popSpec });
  }
  const last = out[out.length - 1];
  // "fall" = peak-to-end decline and whether a relocation happened
  return {
    peakPop: s.peakPop, yrPeak: s.yrPeak, endPop: last.pop, endCharter: last.charter,
    endReach: last.reach, endInfra: last.infra, sacks: s.sacks, capture: s.warCapture,
    exitYear: s.exitYear || 0, exitKind: s.exitKind || 'none',
    riseYears: s.yrPeak - p.start, fallYears: (s.exitYear ? s.exitYear - s.yrPeak : p.end - s.yrPeak),
    series: out
  };
}

// ---------------- experiments ----------------
const EXPS = {
  // E0: the plain charter-state run, no scripted decline
  baseline: () => ({}),
  // E1: kill the capture channel -> does the polity still rise?
  noCapture: () => ({ captureRate: 0 }),
  // E2: kill the charter (no portable legitimacy) -> does it consolidate at all?
  noCharter: () => ({ charterGain: 0, charterOnCapture: 0, charter0: 0.05 }),
  // E3: flat maintenance cost (no scale diseconomy) -> does the network still fail?
  flatMaint: () => ({ maintShape: 0.0, infraKm: 60 }),
  // E4: no elite mobility gradient (all classes leave together)
  flatMobility: (sp) => ({ mobilityElite: sp.mobilityFarmer, mobilitySpecialist: sp.mobilityFarmer }),
  // E5: elite leave FIRST vs LAST (the user's hypothesis as a dial)
  eliteFirst: (sp) => ({ mobilityElite: sp.mobilityElite, mobilityFarmer: sp.mobilityFarmer * 0.2 }),
  eliteLast: (sp) => ({ mobilityElite: sp.mobilityFarmer, mobilityFarmer: sp.mobilityElite }),
  // E6: climate as the trigger instead of structure
  climateOnly: (sp) => ({ drought0: 0.0, droughtYear: 1300, droughtSlope: 0.35, maintShape: 0, infraKm: 60 }),
  // E7: granary size sweep -> how much storage is needed for a peak to exist?
  granary: (sp, v) => ({ storeYears: v }),
  // E8: reach ceiling sweep -> how large can a charter state get?
  reach: (sp, v) => ({ reachMax: v })
};

const EXP = process.argv[2] || 'baseline';
const LO = parseInt(process.argv[3] || '0', 10);
const HI = parseInt(process.argv[4] || '50', 10);
const OUT = process.argv[5] || '/tmp/charter.csv';

function summarise(x) {
  return {
    peakPop: Math.round(x.peakPop), yrPeak: x.yrPeak, endPop: Math.round(x.endPop),
    endCharter: +x.endCharter.toFixed(3), endReach: +x.endReach.toFixed(1),
    endInfra: +x.endInfra.toFixed(3), sacks: x.sacks, capture: Math.round(x.capture),
    exitYear: x.exitYear, exitKind: x.exitKind, riseYears: x.riseYears, fallYears: x.fallYears
  };
}

const rows = [];
for (let i = LO; i < HI; i++) {
  const seed = 2000 + i * 17;
  let over = {};
  let variant = 'base';
  if (EXP === 'granary') { variant = (0.5 + 0.5 * (i % 8)).toFixed(1); over = EXPS.granary(P, +variant); }
  else if (EXP === 'reach') { variant = String(60 + 40 * (i % 9)); over = EXPS.reach(P, +variant); }
  else if (EXP === 'eliteFirst' || EXP === 'eliteLast' || EXP === 'flatMobility') { over = EXPS[EXP](P); variant = EXP; }
  else if (EXPS[EXP]) { over = EXPS[EXP](P); variant = EXP; }
  const x = simulate(Object.assign({}, over, { seed: seed }));
  rows.push(Object.assign({ exp: EXP, variant: variant, seed: seed }, summarise(x)));
}

const cols = Object.keys(rows[0]);
fs.writeFileSync(OUT, [cols.join(',')].concat(rows.map(function (r) {
  return cols.map(function (c) { return typeof r[c] === 'number' ? +(+r[c]).toPrecision(10) : r[c]; }).join(',');
})).join('\n') + '\n');
