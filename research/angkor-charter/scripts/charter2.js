// charter.js — Angkor v2.0 "charter state" engine (clean rewrite).
// Question: can a low-density agrarian polity rise, peak and fall from endogenous
// mechanisms alone, with no scripted 1431?
//
// State: pop, charter (portable legitimacy), reach (administrative km), grain (store),
//        infra (water network condition), capitalAlive, class stocks (elite/specialist/farmer).
//
// Endogenous "fall": reach shrinks below the cost of holding the network -> the court relocates.
//
// Usage: node scripts/charter.js <experiment> <lo> <hi> <outfile>
'use strict';
const fs = require('fs');

function rng(seed) {
  let a = (seed >>> 0) || 1;
  return function () {
    a += 0x6D2B79F5;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}
function normRand(r) {
  const u = 1 - r(), v = 1 - r();
  return Math.sqrt(-2 * Math.log(Math.max(1e-9, u))) * Math.cos(2 * Math.PI * v);
}
function clamp(x, a, b) {
  if (!isFinite(x)) return a;
  return Math.max(a, Math.min(b, x));
}

var P = {
  cells: 60, area: 3000, arableFrac: 0.37,
  yieldT: 1.6, lossPct: 16, riceKg: 200, importsT: 6000,
  pop0: 250000, growth: 0.0065,
  householdTax: 0.11, reachMax: 220, reach0: 40,
  charter0: 0.45, charterGain: 0.008, charterDecay: 0.0045, captureCharterBoost: 0.02,
  patronageShare: 0.18,
  infraKm: 340, maintBase: 0.30, maintShape: 0.85, maintainerShare: 0.22,
  mobilityElite: 0.55, mobilitySpecialist: 0.35, mobilityFarmer: 0.05,
  relocateThreshold: 0.62,
  raidRate: 0.45, captureRate: 0.020, warShare: 0.28,
  climateVol: 0.11, drought0: 0.0, droughtYear: 1300, droughtSlope: 0.0,
  start: 850, end: 1500, seed: 42, storeYears: 1.5
};

function simulate(over) {
  var p = {};
  for (var k in P) p[k] = P[k];
  if (over) for (var k2 in over) if (over[k2] !== undefined) p[k2] = over[k2];

  var r = rng(p.seed);
  var pop = p.pop0;
  var charter = p.charter0;
  var reach = p.reach0;
  var grain = 0;
  var infra = 0.8;
  var capitalAlive = 1;
  var warCapture = 0, sacks = 0;
  var peakPop = 0, yrPeak = p.start, exitYear = 0, exitKind = 'none';
  var popElite = p.pop0 * 0.02, popSpec = p.pop0 * 0.08;
  var series = [];

  var arable = p.area * p.arableFrac;
  var carry = (arable * 100 * p.yieldT * (1 - p.lossPct / 100)) / (p.riceKg / 1000);

  for (var year = p.start; year <= p.end; year++) {
    // climate
    var seasonal = clamp((year - p.droughtYear) / 150, 0, 1);
    var shock = clamp(normRand(r) * p.climateVol - (p.drought0 + p.droughtSlope * seasonal) * 0.42, -0.72, 0.55);

    // water network: maintenance need rises faster than the served area
    // maintenance burden scales with the network a state tries to hold: per-km cost rises
    // with network length (maintShape) and rises again as condition decays (maintBase+(1-infra))
    var netKm = p.infraKm + reach * 1.4;
    // per-km burden is a multiple of a base that is set relative to the labour available per km;
    // it rises with network length (shape) and with decay (condition term)
    var labPerKm = (pop * 0.45 * 180 * 0.25) / Math.max(1, netKm);
    var perKm = p.maintBase * labPerKm * (1 + p.maintShape * (netKm / 400)) * (1 + 3.0 * (1 - infra));
    var maintNeed = netKm * 1000 * perKm;
    var laborPool = pop * 0.45 * 180 * 0.25;
    var maintLabor = Math.min(maintNeed, laborPool * p.maintainerShare);
    var sat = clamp(maintLabor / Math.max(1, maintNeed), 0, 1.2);
    // repair is proportional to what was actually done; decay is proportional to what was needed
    infra = clamp(infra + 0.028 * sat - 0.024 * (1 - sat) - 0.0010 - clamp(-shock * 0.038, 0, 0.075), 0.02, 1);

    // harvest and store
    var hEff = clamp(1 - 0.45 * (1 - infra), 0.46, 1.12);
    var weather = clamp(1 + shock, 0.16, 1.55);
    var gross = arable * 100 * p.yieldT * weather * hEff * (1 - p.lossPct / 100);
    var imports = p.importsT * 0.8;
    var demand = pop * p.riceKg / 1000;
    var balance = gross + imports - demand;
    var cap = demand * clamp(p.storeYears, 0.5, 4);
    grain = clamp(grain + balance, -cap * 0.4, cap);

    // court revenue: a function of reach and charter, not of headcount
    var reachFrac = clamp(reach / p.reachMax, 0, 1.2);
    var surplusHousehold = Math.max(0, gross - demand * 0.72);
    var revenue = surplusHousehold * p.householdTax * reachFrac * clamp(0.4 + charter, 0.3, 1.6);

    // war: capture is the payoff
    var warBudget = revenue * p.warShare;
    var army = Math.min(pop * 0.035, warBudget / 0.12);
    var rivalPower = Math.max(1, (9.5 + 5 * Math.sin((year - 842) / 67) + 0.014 * (year - 850)) * (0.72 + 0.48 * p.raidRate));
    var courtPower = (army / 2500) * (0.45 + 0.85 * charter) + charter * 7 + clamp(surplusHousehold / 16000, 0, 7);
    var winP = clamp(courtPower / (courtPower + rivalPower), 0, 1);
    if (winP > 0.62 && r() < winP * p.raidRate) {
      var captives = p.captureRate * rivalPower * 900;
      pop += captives; warCapture += captives;
      charter = clamp(charter + p.captureCharterBoost, 0, 1);
    } else if (winP < 0.45 && r() < (1 - winP) * p.raidRate * 0.25) {
      sacks++; pop *= 0.97;
    }

    // charter: patronage builds it, a shrinking reach erodes it
    var patronDays = revenue * p.patronageShare * 1000 / 0.45;
    var patronEffect = clamp(Math.log(1 + patronDays / 800000) * 0.006, 0, 0.008);
    var legit = clamp(balance / Math.max(1, demand), -1, 1);
    charter = clamp(charter + patronEffect + p.charterGain * winP + 0.004 * legit
      - p.charterDecay * (1 - reachFrac) - 0.004 * (capitalAlive ? 0 : 1), 0, 1);

    // reach follows charter x network condition
    var reachTarget = p.reach0 + (p.reachMax - p.reach0) * charter * clamp(infra, 0.2, 1.1);
    reach = clamp(reach + (reachTarget - reach) * 0.06, 8, p.reachMax * 1.1);

    // population
    var pressure = pop / Math.max(1, carry);
    var netGrowth = p.growth * (1 - pressure) + 0.004 * legit;
    if (balance < 0) pop *= (1 - clamp(-balance / Math.max(1, demand), 0, 1) * 0.02);
    pop = Math.max(20000, pop * (1 + netGrowth));

    // class mobility: the elite leave first when the charter weakens
    if (charter < p.relocateThreshold * 0.55 || infra < 0.35) {
      var weakness = clamp(1 - charter / p.relocateThreshold, 0, 1);
      popElite *= (1 - clamp(p.mobilityElite * weakness, 0, 0.08));
      popSpec *= (1 - clamp(p.mobilitySpecialist * weakness, 0, 0.06));
    }

    // endogenous exit
    var testable = (year - p.start) >= 60;
    if (testable && capitalAlive && (reach < p.reachMax * 0.30 || grain < -cap * 0.35 || charter < 0.25 || infra < 0.30)) {
      capitalAlive = 0; exitYear = year; exitKind = 'relocation';
    }
    if (pop > peakPop) { peakPop = pop; yrPeak = year; }

    series.push({ year: year, pop: pop, charter: charter, reach: reach, grain: grain, infra: infra,
      capitalAlive: capitalAlive, sacks: sacks, capture: warCapture, elite: popElite, spec: popSpec });
  }

  var lastS = series[series.length - 1];
  return {
    peakPop: peakPop, yrPeak: yrPeak, endPop: lastS.pop, endCharter: lastS.charter,
    endReach: lastS.reach, endInfra: lastS.infra, sacks: sacks, capture: warCapture,
    exitYear: exitYear, exitKind: exitKind,
    riseYears: yrPeak - p.start, fallYears: exitYear ? exitYear - yrPeak : p.end - yrPeak,
    series: series
  };
}

var EXPS = {
  baseline: function () { return {}; },
  noCapture: function () { return { captureRate: 0 }; },
  noCharter: function () { return { charterGain: 0, captureCharterBoost: 0, charter0: 0.05 }; },
  flatMaint: function () { return { maintShape: 0.0, infraKm: 60 }; },
  flatMobility: function () { return { mobilityElite: P.mobilityFarmer, mobilitySpecialist: P.mobilityFarmer }; },
  eliteFirst: function () { return { mobilityElite: P.mobilityElite, mobilityFarmer: P.mobilityFarmer * 0.2 }; },
  eliteLast: function () { return { mobilityElite: P.mobilityFarmer, mobilityFarmer: P.mobilityElite }; },
  climateOnly: function () { return { drought0: 0.0, droughtYear: 1300, droughtSlope: 0.35, maintShape: 0, infraKm: 60 }; },
  granary: function (v) { return { storeYears: v }; },
  reach: function (v) { return { reachMax: v }; }
};

if (require.main === module) {
  var EXP = process.argv[2] || 'baseline';
  var LO = parseInt(process.argv[3] || '0', 10);
  var HI = parseInt(process.argv[4] || '50', 10);
  var OUT = process.argv[5] || '/tmp/charter.csv';
  var rows = [];
  for (var i = LO; i < HI; i++) {
    var seed = 2000 + i * 17;
    var over = {}, variant = 'base';
    if (EXP === 'granary') { variant = (0.5 + 0.5 * (i % 8)).toFixed(1); over = EXPS.granary(+variant); }
    else if (EXP === 'reach') { variant = String(60 + 40 * (i % 9)); over = EXPS.reach(+variant); }
    else if (EXPS[EXP]) { over = EXPS[EXP](); variant = EXP; }
    var x = simulate(Object.assign({}, over, { seed: seed }));
    rows.push({ exp: EXP, variant: variant, seed: seed,
      peakPop: Math.round(x.peakPop), yrPeak: x.yrPeak, endPop: Math.round(x.endPop),
      endCharter: +x.endCharter.toFixed(3), endReach: +x.endReach.toFixed(1),
      endInfra: +x.endInfra.toFixed(3), sacks: x.sacks, capture: Math.round(x.capture),
      exitYear: x.exitYear, exitKind: x.exitKind, riseYears: x.riseYears, fallYears: x.fallYears });
  }
  var cols = Object.keys(rows[0]);
  var lines = [cols.join(',')];
  rows.forEach(function (row) {
    lines.push(cols.map(function (c) { return typeof row[c] === 'number' ? +row[c].toPrecision(10) : row[c]; }).join(','));
  });
  fs.writeFileSync(OUT, lines.join('\n') + '\n');
}

module.exports = { simulate: simulate, P: P, EXPS: EXPS };
