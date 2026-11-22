// charter3.js — Angkor "charter state" model, v3 (calibrated units).
//
// Purpose: can a low-density agrarian polity rise, peak and fall from endogenous
// mechanisms, with no scripted 1431?
//
// Calibration anchors (all changeable; see research/litreview.md once it lands):
//   - population 250k -> ~750k, plateau ~1100-1300, decline after
//   - paddy yield 1.5-1.8 t/ha (pre-Green Revolution regional baseline)
//   - planted area ~1,000-1,200 km2 of a 3,000 km2 complex
//   - rice demand 200 kg paddy/person/yr
//   - maintenance: a km of canal needs a fixed person-days/yr, rising with network length
//
// Units: tonnes (t), person-days (pd), km, people, years.
'use strict';
const fs = require('fs');

const DEFAULTS = {
  // demography and food
  pop0: 250000, growRate: 0.0075, maxGrow: 0.020,
  riceKg: 200, yieldT: 1.6, lossPct: 16, importsT: 6000,
  area: 3000, arableFrac: 0.37,          // 1,110 km2 of rice
  storeYears: 1.5,
  // water network: person-days per km per year, and the length the state is trying to hold
  pdPerKm: 1200, infraKm0: 40, maintDuty: 0.55,   // 25% of the non-farming labour pool may be mobilised
  infraDecay: 0.010, hEffOnInfra: 0.45, pdShape: 0.6, pdPerKm: 4800, costPerKm: 1,
  // state: revenue and reach
  reachMax: 220, reach0: 40, charter0: 0.45,
  taxRate: 0.10, extractionShare: 0.55,   // share of the surplus the court can actually tap
  patronShare: 0.15, charterBuild: 0.010, charterDecay: 0.012,
  // war
  raidRate: 0.45, captureRate: 0.006, warShare: 0.22,
  // climate
  climateVol: 0.11, droughtYear: 1300, droughtSlope: 0.0,
  // run
  start: 850, end: 1500, seed: 42
};

function rng(seed) {
  let a = (seed >>> 0) || 1;
  return function () {
    a += 0x6D2B79F5; let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function normRand(r) { const u = 1 - r(), v = 1 - r(); return Math.sqrt(-2 * Math.log(Math.max(1e-9, u))) * Math.cos(2 * Math.PI * v); }
function clamp(x, a, b) { if (!isFinite(x)) return a; return Math.max(a, Math.min(b, x)); }

function simulate(over) {
  const p = Object.assign({}, DEFAULTS, over || {});
  const r = rng(p.seed);
  let pop = p.pop0, charter = p.charter0, reach = p.reach0, grain = 0, infra = p.infraKm0 / 90;
  let infraKm = p.infraKm0, capitalAlive = 1, sacks = 0, captured = 0;
  let peakPop = 0, yrPeak = p.start, exitYear = 0, exitKind = 'none';
  const series = [];
  const carryArea = p.area * p.arableFrac;

  for (let year = p.start; year <= p.end; year++) {
    // ---- climate ----
    const seasonal = clamp((year - p.droughtYear) / 150, 0, 1);
    const shock = clamp(normRand(r) * p.climateVol - p.droughtSlope * seasonal * 0.42, -0.72, 0.55);

    // ---- labour ----
    const adults = pop * 0.45;
    const workDays = adults * 180;                 // total adult work-days/yr
    // farming need is capped by what the fields require, so a bigger population frees labour
    const fieldNeed = Math.min(workDays * 0.85, carryArea * 100 * 26); // ~26 pd/ha/yr
    const spare = Math.max(0, workDays - fieldNeed);
    const avail = spare * p.maintDuty;

    // ---- water network ----
    // need = length x per-km cost, and per-km cost rises with length (scale diseconomy)
    const pdPerKmNow = p.pdPerKm * (1 + p.pdShape * (infraKm / 300)) * (1 + 2.0 * (1 - infra));
    const need = infraKm * pdPerKmNow;
    const sat = clamp(avail / Math.max(1, need), 0, 1.2);
    // network length the court is trying to hold, gated by reach
    const wantedKm = p.infraKm0 + reach * 1.6;
    if (sat > 0.6) infraKm += (wantedKm - infraKm) * 0.02;   // a funded state extends
    infra = clamp(infra + 0.030 * sat - p.infraDecay * (1 - sat) - clamp(-shock * 0.030, 0, 0.06), 0.02, 1.2);

    // ---- harvest ----
    const hEff = clamp(1 - p.hEffOnInfra * (1 - clamp(infra, 0, 1)), 0.5, 1.0);
    const weather = clamp(1 + shock, 0.2, 1.5);
    const gross = carryArea * 100 * p.yieldT * weather * hEff * (1 - p.lossPct / 100);
    const demand = pop * p.riceKg / 1000;
    const balance = gross + p.importsT - demand;
    const cap = demand * p.storeYears;
    grain = clamp(grain + balance, -cap * 0.4, cap);

    // ---- state revenue: a fraction of the household surplus, gated by reach and charter ----
    const surplus = Math.max(0, gross - demand * 0.75);
    const reachFrac = clamp(reach / p.reachMax, 0, 1.2);
    const revenue = surplus * p.taxRate * p.extractionShare * reachFrac * clamp(0.45 + charter, 0.3, 1.6);

    // ---- war: capture as the payoff ----
    const army = Math.min(pop * 0.03, revenue * p.warShare / 0.12);
    const rival = Math.max(1, (9.5 + 5 * Math.sin((year - 842) / 67) + 0.014 * (year - 850)) * (0.72 + 0.48 * p.raidRate));
    const court = (army / 2500) * (0.45 + 0.85 * charter) + charter * 7 + clamp(surplus / 16000, 0, 7);
    const winP = clamp(court / (court + rival), 0, 1);
    if (winP > 0.60 && r() < winP * p.raidRate) {
      const c = p.captureRate * rival * 700;
      pop += c; captured += c; charter = clamp(charter + 0.015, 0, 1);
    } else if (winP < 0.45 && r() < (1 - winP) * p.raidRate * 0.22) {
      sacks++; pop *= 0.975;
    }

    // ---- charter: patronage builds, contraction erodes ----
    const patron = clamp(revenue / Math.max(1, p.reachMax * 400) * 0.02, 0, 0.012);
    const legit = clamp(balance / Math.max(1, demand), -1, 1);
    charter = clamp(charter + patron + p.charterBuild * winP + 0.003 * legit
      - p.charterDecay * (1 - reachFrac) - 0.004 * (capitalAlive ? 0 : 1), 0, 1);

    // ---- reach ----
    const reachTarget = p.reach0 + (p.reachMax - p.reach0) * charter * clamp(infra, 0.2, 1.1);
    reach = clamp(reach + (reachTarget - reach) * 0.05, 8, p.reachMax * 1.1);

    // ---- population ----
    const pressure = pop / Math.max(1, (carryArea * 100 * p.yieldT * (1 - p.lossPct / 100) * clamp(infra, 0.3, 1.1)) / (p.riceKg / 1000));
    let g = p.growRate * (1 - pressure) + 0.002 * legit;
    // a food deficit is a mortality event, and the store cannot mask it indefinitely
    if (balance < 0 || grain < -cap * 0.25) g -= 0.02 + 0.03 * clamp(-balance / Math.max(1, demand), 0, 1);
    g = clamp(g, -0.06, p.maxGrow);
    pop = Math.max(20000, pop * (1 + g));

    // ---- endogenous exit ----
    if (year - p.start >= 80 && capitalAlive &&
        (reach < p.reachMax * 0.30 || charter < 0.24 || infra < 0.30)) {
      capitalAlive = 0; exitYear = year; exitKind = 'relocation';
    }
    if (pop > peakPop) { peakPop = pop; yrPeak = year; }
    series.push({ year, pop, charter, reach, infra, infraKm, grain, sacks, captured, capitalAlive });
  }
  const last = series[series.length - 1];
  return {
    peakPop, yrPeak, endPop: last.pop, endCharter: last.charter, endReach: last.reach,
    endInfra: last.infra, sacks, captured: Math.round(captured), exitYear, exitKind,
    riseYears: yrPeak - p.start, fallYears: exitYear ? exitYear - yrPeak : p.end - yrPeak, series
  };
}

// ---------------- experiments ----------------
const EXPS = {
  baseline: () => ({}),
  noCapture: () => ({ captureRate: 0 }),
  noCharter: () => ({ charterBuild: 0, charter0: 0.05 }),
  // no scale diseconomy in the network: per-km cost constant
  flatMaint: () => ({ pdPerKm: 1200 }),
  // flatMaint needs a distinct knob: we add one in simulate via pdPerKmShape
  flatMaintTrue: () => ({ _flat: true }),
  eliteFirst: () => ({ _mob: 'first' }),
  eliteLast: () => ({ _mob: 'last' }),
  flatMobility: () => ({ _mob: 'flat' }),
  climateOnly: () => ({ _flat: true, droughtSlope: 0.35 })
};

function runExp(name, seed) {
  const over = Object.assign({}, (EXPS[name] ? EXPS[name]() : {}), { seed });
  if (over._flat) { over.pdShape = 0; delete over._flat; }
  if (over._mob) { over._mobility = over._mob; delete over._mob; }
  return simulate(over);
}

module.exports = { simulate, runExp, EXPS, DEFAULTS };
