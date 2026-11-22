// charter4.js — Angkor "charter state" model v4.
//
// The v3 lesson (kept here in code, not in a comment thread): a water network whose
// per-km upkeep is a constant can always be paid for once the polity has any spare
// labour, so the model has no interior peak. An interior peak requires the per-km
// cost to rise with the length of the network faster than the population does.
//
// So the network has one parameter that matters: `costExp` (the exponent on length).
//   costExp = 1   -> linear: no interior peak, the state plateaus (E3 predicts this)
//   costExp = 1.5 -> interior peak + endogenous relocation (the observed pattern)
//   costExp = 2   -> the state never consolidates (a smallholding equilibrium)
//
// Units: tonnes, person-days, km, people, years.
'use strict';
const fs = require('fs');

const DEFAULTS = {
  pop0: 250000, growRate: 0.0075, maxGrow: 0.02,
  riceKg: 200, yieldT: 1.6, lossPct: 16, importsT: 6000,
  area: 3000, arableFrac: 0.37, storeYears: 1.5,
  // network
  kmWanted0: 40, kmPerReach: 1.6, pdPerKm: 3000, costExp: 1.5, kmRef: 300,
  levyDays: 9, infraDecay: 0.010, hEffOnInfra: 0.45,
  // state
  reachMax: 220, reach0: 40, charter0: 0.45,
  taxRate: 0.10, extractionShare: 0.55,
  charterBuild: 0.010, charterDecay: 0.012,
  // war
  raidRate: 0.45, captureRate: 0.006, warShare: 0.22,
  // climate
  climateVol: 0.11, droughtYear: 1300, droughtSlope: 0.0,
  // class mobility (the elite-leaves-first dial)
  mobilityElite: 0.55, mobilitySpecialist: 0.35, mobilityFarmer: 0.05,
  // run
  start: 850, end: 1500, seed: 42
};

function rng(seed) { let a = (seed >>> 0) || 1; return function () { a += 0x6D2B79F5; let t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
function normRand(r) { const u = 1 - r(), v = 1 - r(); return Math.sqrt(-2 * Math.log(Math.max(1e-9, u))) * Math.cos(2 * Math.PI * v); }
function clamp(x, a, b) { if (!isFinite(x)) return a; return Math.max(a, Math.min(b, x)); }

function simulate(over) {
  const p = Object.assign({}, DEFAULTS, over || {});
  const r = rng(p.seed);
  let pop = p.pop0, charter = p.charter0, reach = p.reach0, grain = 0;
  let km = p.kmWanted0, infra = clamp(km / 90, 0, 1.2);
  let capitalAlive = 1, sacks = 0, captured = 0;
  let peakPop = 0, yrPeak = p.start, exitYear = 0, exitKind = 'none';
  const series = [];
  const carryArea = p.area * p.arableFrac;

  // class stocks
  let elite = pop * 0.02, spec = pop * 0.08, farmer = pop * 0.90;
  let tEliteExit = 0, tSpecExit = 0, tFarmerExit = 0;
  const startPop = pop;

  for (let year = p.start; year <= p.end; year++) {
    const season = clamp((year - p.droughtYear) / 150, 0, 1);
    const shock = clamp(normRand(r) * p.climateVol - p.droughtSlope * season * 0.42, -0.72, 0.55);

    // ---- labour available for public works ----
    const workDays = pop * 0.45 * 180;
    // upkeep is a levy ON THE POPULATION, not a share of a free labour pool: it competes with farming
    const levy = pop * p.levyDays;
    const fieldNeed = Math.min(workDays * 0.85, carryArea * 100 * 26);
    const avail = levy;

    // ---- the network: upkeep cost per km rises with length (costExp) and with decay ----
    const perKm = p.pdPerKm * Math.pow(Math.max(1, km) / p.kmRef, p.costExp - 1) * (1 + 2.0 * (1 - clamp(infra, 0, 1)));
    const need = km * perKm;
    const sat = clamp(avail / Math.max(1, need), 0, 1.2);

    // length the court is trying to hold
    const wantedKm = p.kmWanted0 + reach * p.kmPerReach;
    if (sat > 0.95) km += (wantedKm - km) * 0.015;
    else km += (p.kmWanted0 + reach * 0.3 - km) * 0.02;   // an unfunded state abandons its extensions
    km = Math.max(p.kmWanted0, km);

    infra = clamp(infra + 0.030 * Math.min(sat, 1) - p.infraDecay * clamp(1 - sat, 0, 1) - clamp(-shock * 0.030, 0, 0.06), 0.02, 1.2);

    // ---- harvest ----
    const hEff = clamp(1 - p.hEffOnInfra * (1 - clamp(infra, 0, 1)), 0.5, 1.0);
    const weather = clamp(1 + shock, 0.2, 1.5);
    const gross = carryArea * 100 * p.yieldT * weather * hEff * (1 - p.lossPct / 100);
    const demand = pop * p.riceKg / 1000;
    const balance = gross + p.importsT - demand;
    const cap = demand * p.storeYears;
    grain = clamp(grain + balance, -cap * 0.4, cap);

    // ---- revenue ----
    const surplus = Math.max(0, gross - demand * 0.75);
    const reachFrac = clamp(reach / p.reachMax, 0, 1.2);
    const revenue = surplus * p.taxRate * p.extractionShare * reachFrac * clamp(0.45 + charter, 0.3, 1.6);

    // ---- war ----
    const army = Math.min(pop * 0.03, revenue * p.warShare / 0.12);
    const rival = Math.max(1, (9.5 + 5 * Math.sin((year - 842) / 67) + 0.014 * (year - 850)) * (0.72 + 0.48 * p.raidRate));
    const court = (army / 2500) * (0.45 + 0.85 * charter) + charter * 7 + clamp(surplus / 16000, 0, 7);
    const winP = clamp(court / (court + rival), 0, 1);
    if (winP > 0.60 && r() < winP * p.raidRate) {
      const c = p.captureRate * rival * 700;
      pop += c; captured += c; farmer += c * 0.9;
      charter = clamp(charter + 0.015, 0, 1);
    } else if (winP < 0.45 && r() < (1 - winP) * p.raidRate * 0.22) {
      sacks++; pop *= 0.975; farmer *= 0.975;
    }

    // ---- charter ----
    const patron = clamp(revenue / Math.max(1, p.reachMax * 400) * 0.02, 0, 0.012);
    const legit = clamp(balance / Math.max(1, demand), -1, 1);
    charter = clamp(charter + patron + p.charterBuild * winP + 0.003 * legit
      - p.charterDecay * (1 - reachFrac) - 0.004 * (capitalAlive ? 0 : 1), 0, 1);

    // ---- reach ----
    const reachTarget = p.reach0 + (p.reachMax - p.reach0) * charter * clamp(infra, 0.2, 1.1);
    reach = clamp(reach + (reachTarget - reach) * 0.05, 8, p.reachMax * 1.1);

    // ---- population ----
    const supported = (carryArea * 100 * p.yieldT * (1 - p.lossPct / 100) * clamp(infra, 0.3, 1.1)) / (p.riceKg / 1000);
    const pressure = pop / Math.max(1, supported);
    let g = p.growRate * (1 - pressure) + 0.002 * legit;
    if (balance < 0 || grain < -cap * 0.25) g -= 0.02 + 0.03 * clamp(-balance / Math.max(1, demand), 0, 1);
    g = clamp(g, -0.06, p.maxGrow);
    pop = Math.max(20000, pop * (1 + g));

    // keep class stocks in step, then let them exit by their own mobility
    const scaleIn = pop * (1 + g) / Math.max(1, elite + spec + farmer);
    elite *= scaleIn; spec *= scaleIn; farmer *= scaleIn;
    const weakness = clamp(1 - charter / 0.62, 0, 1);
    if (weakness > 0.05) {
      const eExit = clamp(p.mobilityElite * weakness, 0, 0.06);
      const sExit = clamp(p.mobilitySpecialist * weakness, 0, 0.05);
      const fExit = clamp(p.mobilityFarmer * weakness, 0, 0.04);
      if (eExit > 0 && !tEliteExit) tEliteExit = year;
      if (sExit > 0 && !tSpecExit) tSpecExit = year;
      if (fExit > 0 && !tFarmerExit) tFarmerExit = year;
      elite *= (1 - eExit); spec *= (1 - sExit); farmer *= (1 - fExit);
    }

    // ---- endogenous exit ----
    if (year - p.start >= 80 && capitalAlive && (reach < p.reachMax * 0.30 || charter < 0.24 || infra < 0.30)) {
      capitalAlive = 0; exitYear = year; exitKind = 'relocation';
    }
    if (pop > peakPop) { peakPop = pop; yrPeak = year; }
    series.push({ year, pop, charter, reach, infra, km, grain, sacks, captured,
      elite: elite / Math.max(1, elite + spec + farmer) , capitalAlive });
  }
  const last = series[series.length - 1];
  return {
    peakPop, yrPeak, endPop: last.pop, endCharter: last.charter, endReach: last.reach,
    endInfra: last.infra, endKm: last.km, sacks, captured: Math.round(captured),
    exitYear, exitKind, tEliteExit, tSpecExit, tFarmerExit,
    riseYears: yrPeak - p.start, fallYears: exitYear ? exitYear - yrPeak : p.end - yrPeak,
    finalEliteShare: last.elite, series
  };
}

if (require.main === module) {
  const fs2 = fs;
  const out = {};
  ['baseline'].forEach(function (n) { out[n] = simulate({}); });
  console.log(JSON.stringify({ peak: Math.round(out.baseline.peakPop), yrPeak: out.baseline.yrPeak,
    end: Math.round(out.baseline.endPop), exit: out.baseline.exitYear, km: Math.round(out.baseline.endKm) }));
}

module.exports = { simulate, DEFAULTS };
