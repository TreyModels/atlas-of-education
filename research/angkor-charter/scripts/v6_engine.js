// v6_engine.js — Angkor fiscal-charter model with switchable mechanisms.
// Built for experiment design, not for realism: every rival hypothesis is a switch,
// so a 2^5 factorial can ask which combination produces a rise, a peak and a relocation.
//
// Stocks: cultivators (pop), cultivated land (A), endowment share (e), elite households (E),
//         charter (legitimacy), water network (km), grain store.
//
// Mechanisms (all switchable):
//   ratchet   — temple endowments permanently alienate land from the taxable base
//   charter   — legitimacy is a stock that can be lost and relocated (capital cycle)
//   climate   — drought shrinks the harvest from a given year
//   raid      — war captures labour (the "Rome" channel)
//   transport — tribute attenuates with distance from the capital
//
// Node 12 compatible.
'use strict';

var DEFAULTS = {
  start: 800, end: 1600, seed: 42,
  // land / yield
  A0: 400, Amax: 1110, y: 1.5, lossPct: 16, expandRate: 0.010,
  // demography
  pop0: 150000, riceKg: 200, growRate: 0.006,
  // endowment ratchet
  e0: 0.02, endowRate: 0.0016, endowMax: 0.90,
  // elite
  elite0: 6000, stipendT: 0.25, eliteGrow: 0.002,
  // crown
  taxRate: 0.10,
  // network
  km0: 40, kmPer1000T: 14, pdPerKm: 3000, pdToT: 1 / 180,
  // defence
  defShare: 0.12,
  // charter
  charter0: 0.60, charterGain: 0.0025, charterLoss: 0.004,
  // transport attenuation of tribute
  decayKm: 120,
  // raiding
  raidRate: 0.45, captureRate: 0.006,
  // climate
  climateVol: 0.11, droughtYear: 1300, droughtSlope: 0.0,
  // relocation
  relocCharter: 0.25, relocCover: 0.60, relocHold: 12,
  // switches
  swRatchet: 1, swCharter: 1, swClimate: 1, swRaid: 1, swTransport: 1
};

function rng(seed) {
  var a = (seed >>> 0) || 1;
  return function () {
    a += 0x6D2B79F5;
    var t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function normRand(r) {
  var u = 1 - r(), v = 1 - r();
  return Math.sqrt(-2 * Math.log(Math.max(1e-9, u))) * Math.cos(2 * Math.PI * v);
}
function clamp(x, a, b) { if (!isFinite(x)) return a; return Math.max(a, Math.min(b, x)); }

function simulate(over) {
  var p = {}, k;
  for (k in DEFAULTS) p[k] = DEFAULTS[k];
  if (over) for (k in over) if (over[k] !== undefined) p[k] = over[k];

  var r = rng(p.seed);
  var A = p.A0, e = p.e0, E = p.elite0, pop = p.pop0, km = p.km0;
  var charter = p.charter0, grain = 0;
  var badYears = 0, relocations = 0, firstReloc = 0, lastReloc = 0;
  var peakRev = 0, yrRevPeak = 0, peakPop = 0, yrPopPeak = 0, crossYear = 0;
  var endowAtCross = null, captured = 0, sacks = 0;
  var rows = [];

  for (var yr = p.start; yr <= p.end; yr++) {
    // ---------- climate ----------
    var season = clamp((yr - p.droughtYear) / 150, 0, 1);
    var shock = p.swClimate ? clamp(normRand(r) * p.climateVol - p.droughtSlope * season * 0.42, -0.72, 0.55) : 0;

    // ---------- production ----------
    var prod = A * 100 * p.y * (1 - p.lossPct / 100) * (1 + shock);
    var demand = pop * p.riceKg / 1000;
    var balance = prod - demand;
    var cap = demand * 1.5;
    grain = clamp(grain + balance, -cap * 0.4, cap);

    // ---------- land expansion ----------
    var rentShare = clamp(0.12 + 0.55 * e + 0.000018 * E, 0.10, 0.78);
    var available = prod * (1 - rentShare);
    var carrying = available / (p.riceKg / 1000) / 1000 * 1000 / 1000;
    carrying = available / (p.riceKg / 1000);
    var pressure = pop / Math.max(1, carrying);
    if (A < p.Amax && pressure > 0.25) A = Math.min(p.Amax, A * (1 + p.expandRate * (1 - pressure)));

    // ---------- the endowment ratchet ----------
    if (p.swRatchet) e = Math.min(p.endowMax, e + p.endowRate * (0.4 + charter));

    // ---------- crown revenue, attenuated by distance ----------
    var taxable = A * (1 - e);
    var grossRev = taxable * 100 * p.y * (1 - p.lossPct / 100) * (1 + shock) * p.taxRate;
    // reach grows with solvency; tribute from a wider ring is discounted
    var reachKm = 40 + 320 * charter;
    var atten = p.swTransport ? Math.exp(-Math.max(0, reachKm - 60) / p.decayKm) : 1;
    var revenue = grossRev * (0.55 + 0.45 * atten);

    // ---------- obligations ----------
    var stipends = E * p.stipendT;
    var network = km * p.pdPerKm * p.pdToT;
    var defence = revenue * p.defShare;
    var obligations = stipends + network + defence;
    var cover = revenue / Math.max(1, obligations);

    // ---------- network follows revenue ----------
    km += (p.km0 + revenue * p.kmPer1000T / 1000 - km) * 0.03;

    // ---------- elite overproduction ----------
    if (revenue / Math.max(1, E) > p.stipendT * 1.25) E *= (1 + p.eliteGrow);

    // ---------- raiding ----------
    if (p.swRaid && r() < p.raidRate * 0.5) {
      var c = p.captureRate * 700 * (0.5 + revenue / 5000);
      pop += c; captured += c;
    }
    if (p.swRaid && r() < p.raidRate * 0.05) { sacks++; pop *= 0.99; }

    // ---------- charter ----------
    if (p.swCharter) charter = clamp(charter + (cover > 1 ? p.charterGain : -p.charterLoss), 0, 1);

    // ---------- population ----------
    var g;
    if (pressure <= 1) g = p.growRate * (1 - pressure);
    else g = -0.030 * (pressure - 1) - 0.004;   // overshoot above carrying capacity
    if (balance < 0) g -= 0.008 * Math.min(1, -balance / Math.max(1, demand));
    pop = Math.max(30000, pop * (1 + g));

    // ---------- relocation (the capital-cycle mechanism) ----------
    if (p.swCharter) {
      if (cover < 0.45) badYears++; else badYears = 0;
      var charterCollapse = charter < p.relocCharter;
      if (charterCollapse || badYears >= p.relocHold) {
        relocations++;
        if (!firstReloc) firstReloc = yr;
        lastReloc = yr;
        // a new capital means a new catchment: smaller cultivated area, fresh endowment base
        A = Math.max(p.A0 * 0.6, A * 0.35);
        e = 0.05; km = p.km0; charter = 0.45; badYears = 0;
        pop *= 0.80; E *= 0.5;
      }
    }

    if (revenue > peakRev) { peakRev = revenue; yrRevPeak = yr; }
    if (pop > peakPop) { peakPop = pop; yrPopPeak = yr; }
    if (!crossYear && yr > p.start + 60 && cover < 1) { crossYear = yr; endowAtCross = e; }

    rows.push({ yr: yr, pop: pop, A: A, e: e, E: E, revenue: revenue, obligations: obligations,
      cover: cover, km: km, charter: charter, grain: grain, relocations: relocations });
  }

  var last = rows[rows.length - 1];
  return {
    peakRev: Math.round(peakRev), yrRevPeak: yrRevPeak,
    peakPop: Math.round(peakPop), yrPopPeak: yrPopPeak,
    crossYear: crossYear || 0, endowAtCross: endowAtCross === null ? -1 : +endowAtCross.toFixed(3),
    relocations: relocations, firstReloc: firstReloc, lastReloc: lastReloc,
    endPop: Math.round(last.pop), endRev: Math.round(last.revenue),
    endCharter: +last.charter.toFixed(3), endE: +last.e.toFixed(3),
    captured: Math.round(captured), sacks: sacks,
    // the discriminating statistic: does the capital move AFTER the population peak?
    relocLag: (firstReloc && yrPopPeak) ? firstReloc - yrPopPeak : -999,
    revenueDecline: peakRev > 0 ? +(1 - last.revenue / peakRev).toFixed(3) : 0,
    rows: rows
  };
}

module.exports = { simulate: simulate, DEFAULTS: DEFAULTS };
