// v7_engine.js — space-explicit tribute model.
//
// Replaces v6's single scalar attenuation `exp(-d/decayKm)` with an actual ring geometry:
// the polity is a centre surrounded by annuli, each with its own cultivable area, its own
// haul cost to the centre, and its own garrison cost. Revenue is the sum over the rings the
// state can actually hold, and REACH IS AN OUTPUT, not a parameter.
//
// This is the model that can resolve the v6 disagreement: Morris said transport attenuation
// barely matters, the factorial said it can substitute for the endowment ratchet. With rings,
// transport does two things at once — it discounts distant revenue AND it sets the optimal
// reach — which a single scalar multiplier cannot do.
//
// Units: km, km2, t (paddy), people, years.
'use strict';

var DEFAULTS = {
  start: 800, end: 1600, seed: 42,
  // geometry
  ringD: [10,30,50,70,90,110,130,150],
  ringArea: [280,200,170,140,110,90,70,50],
  // yield / diet
  y: 1.5, lossPct: 16, riceKg: 200,
  // haul: fraction of a load that survives `haulHalf` km
  haulHalf: 100,
  // garrison cost per km2 cultivated, at distance d: base * (d/50)^garrisonExp
  holdFrac: 0.05, garrisonExp: 1.2,
  // demography
  pop0: 330000, growRate: 0.006,
  // endowment ratchet (per ring, uniform)
  e0: 0.02, endowRate: 0.0016, endowMax: 0.90,
  // elite
  elite0: 5000, stipendT: 0.25, eliteGrow: 0.002,
  // crown
  taxRate: 0.10,
  // network
  km0: 40, kmPer1000T: 14, pdPerKm: 3000, pdToT: 1 / 180,
  defShare: 0.12,
  // charter
  charter0: 0.60, charterGain: 0.0025, charterLoss: 0.004,
  // raiding
  raidRate: 0.45, captureRate: 0.006,
  // climate
  climateVol: 0.11, droughtYear: 1300, droughtSlope: 0.0,
  // relocation
  relocCharter: 0.25, relocHold: 12, relocCooldown: 60,
  // switches
  swRatchet: 1, swCharter: 1, swClimate: 1, swRaid: 1, swTransport: 1
};

function rng(seed) { var a = (seed >>> 0) || 1; return function () { a += 0x6D2B79F5; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
function normRand(r) { var u = 1 - r(), v = 1 - r(); return Math.sqrt(-2 * Math.log(Math.max(1e-9, u))) * Math.cos(2 * Math.PI * v); }
function clamp(x, a, b) { if (!isFinite(x)) return a; return Math.max(a, Math.min(b, x)); }

function buildRings(p) {
  var rings = [];
  for (var j = 0; j < p.ringD.length; j++) {
    var d = p.ringD[j];
    rings.push({ j: j, d: d, area: p.ringArea[j], arable: p.ringArea[j],
      haul: Math.pow(0.5, d / p.haulHalf), cult: 0, e: p.e0 });
  }
  return rings;
}

function simulate(over) {
  var p = {}, k;
  for (k in DEFAULTS) p[k] = DEFAULTS[k];
  if (over) for (k in over) if (over[k] !== undefined) p[k] = over[k];

  var r = rng(p.seed);
  var rings = buildRings(p);
  var pop = p.pop0, E = p.elite0, km = p.km0, charter = p.charter0;
  var badYears = 0, relocations = 0, firstReloc = 0;
  var peakRev = 0, yrRevPeak = 0, peakPop = 0, yrPopPeak = 0, crossYear = 0, endowAtCross = -1;
  var reachYears = [], heldYears = [];
  var rows = [];

  for (var yr = p.start; yr <= p.end; yr++) {
    var season = clamp((yr - p.droughtYear) / 150, 0, 1);
    var shock = p.swClimate ? clamp(normRand(r) * p.climateVol - p.droughtSlope * season * 0.42, -0.72, 0.55) : 0;

    // ---- how much land must be cultivated to feed the population ----
    var need = pop * p.riceKg / 1000;                        // t
    var perKm2 = 100 * p.y * (1 - p.lossPct / 100) * (1 + shock); // t per km2
    var landNeeded = need * 1.32 / Math.max(0.2, perKm2);    // km2, plus a margin

    // ---- fill rings from the centre outward (von Thunen: nearest land is cultivated first) ----
    var remaining = landNeeded, totalCult = 0, grossProd = 0;
    for (var j = 0; j < rings.length; j++) {
      var rg = rings[j];
      rg.cult = Math.min(rg.arable, Math.max(0, remaining));
      remaining -= rg.cult;
      totalCult += rg.cult;
      grossProd += rg.cult * perKm2;
    }
    // slow adjustment toward the target (land cannot be cleared instantly)
    if (yr > p.start) {
      // (cells are recomputed each year from `need`; the smoothing is implicit in pop's own rate)
    }

    // ---- the endowment ratchet, applied to every ring ----
    if (p.swRatchet) for (var j2 = 0; j2 < rings.length; j2++) {
      rings[j2].e = Math.min(p.endowMax, rings[j2].e + p.endowRate * (0.4 + charter));
    }

    // ---- revenue and holding cost, ring by ring ----
    var revenue = 0, holdCost = 0, outermostHeld = 0, ringsHeld = 0;
    for (var j3 = 0; j3 < rings.length; j3++) {
      var rg3 = rings[j3];
      if (rg3.cult <= 0) continue;
      var haul = p.swTransport ? rg3.haul : 1;
      var prodJ = rg3.cult * perKm2;
      var rev = prodJ * (1 - rg3.e) * p.taxRate * haul;
      var cost = prodJ * p.holdFrac * Math.pow(Math.max(1, rg3.d) / 50, p.garrisonExp);
      if (rev > cost || rg3.d <= 60) {   // the inner rings are held even at a loss (they are the polity)
        revenue += rev - cost;
        outermostHeld = rg3.d; ringsHeld++;
      }
    }
    var obligations = E * p.stipendT + km * p.pdPerKm * p.pdToT + Math.max(0, revenue) * p.defShare;
    var cover = revenue / Math.max(1, obligations);

    // ---- network ----
    km += (p.km0 + Math.max(0, revenue) * p.kmPer1000T / 1000 - km) * 0.03;

    // ---- elite overproduction ----
    if (revenue / Math.max(1, E) > p.stipendT * 1.25) E *= (1 + p.eliteGrow);

    // ---- raiding ----
    if (p.swRaid && r() < p.raidRate * 0.5) pop += p.captureRate * 700 * (0.5 + revenue / 5000);
    if (p.swRaid && r() < p.raidRate * 0.05) pop *= 0.99;

    // ---- charter ----
    if (p.swCharter) charter = clamp(charter + (cover > 1 ? p.charterGain : -p.charterLoss), 0, 1);

    // ---- population: food-limited, with rent extraction ----
    var rentShare = clamp(0.10 + 0.35 * rings[0].e + 0.000010 * E, 0.08, 0.70);
    var available = grossProd * (1 - rentShare);
    var carrying = available / (p.riceKg / 1000);
    var pressure = pop / Math.max(1, carrying);
    var g = (pressure <= 1) ? p.growRate * (1 - pressure) : -0.030 * (pressure - 1) - 0.004;
    pop = Math.max(30000, pop * (1 + g));

    // ---- relocation ----
    if (p.swCharter) {
      if (cover < 0.45) badYears++; else badYears = 0;
      if ((charter < p.relocCharter || badYears >= p.relocHold) && (yr - firstReloc > p.relocCooldown || !firstReloc)) {
        relocations++; if (!firstReloc) firstReloc = yr;
        // new capital: nearer rings only, fresh endowment base
        for (var j4 = 0; j4 < rings.length; j4++) rings[j4].e = 0.05;
        km = p.km0; charter = 0.45; badYears = 0; pop *= 0.80; E *= 0.5;
      }
    }

    if (revenue > peakRev) { peakRev = revenue; yrRevPeak = yr; }
    if (pop > peakPop) { peakPop = pop; yrPopPeak = yr; }
    if (!crossYear && yr > p.start + 60 && cover < 1) { crossYear = yr; endowAtCross = rings[0].e; }
    reachYears.push(outermostHeld); heldYears.push(ringsHeld);

    rows.push({ yr: yr, pop: pop, revenue: revenue, obligations: obligations, cover: cover,
      cult: totalCult, reach: outermostHeld, ringsHeld: ringsHeld, e: rings[0].e, charter: charter });
  }

  var last = rows[rows.length - 1];
  var reachMedian = reachYears.slice().sort(function (a, b) { return a - b; })[Math.floor(reachYears.length / 2)];
  return {
    peakRev: Math.round(peakRev), yrRevPeak: yrRevPeak,
    peakPop: Math.round(peakPop), yrPopPeak: yrPopPeak,
    crossYear: crossYear, endowAtCross: +endowAtCross.toFixed(3),
    relocations: relocations, firstReloc: firstReloc,
    endPop: Math.round(last.pop), endRev: Math.round(last.revenue),
    endCharter: +last.charter.toFixed(3), endE: +last.e.toFixed(3),
    endReach: last.reach, peakReach: Math.max.apply(null, reachYears), reachMedian: reachMedian,
    relocLag: (firstReloc && yrPopPeak) ? firstReloc - yrPopPeak : -999,
    revenueDecline: peakRev > 0 ? +(1 - last.revenue / peakRev).toFixed(3) : 0,
    rows: rows
  };
}

module.exports = { simulate: simulate, DEFAULTS: DEFAULTS };
