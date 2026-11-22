// v11_abm.js — v10 + F8: the crown budget is a set of COMMITTED OBLIGATIONS, not a
// normalised share of a residual.  Round 1 showed x1_budget_split collapsing: (u30,m45) and
// (u12,m18) gave bit-identical output because only the ratio u/(u+m) entered.  Now:
//   army   = armyPerKm * netKm          (garrison scales with the network it guards)
//   temple = monumentShare * (revenue - army)   (a programme that cannot be deferred)
//   upkeep = upkeepShare * (revenue - army - temple)   (slack is elite consumption)
// Each level is separately identified.
//
// Fixes over v9_abm.js:
//  F1  crown upkeep need is now ENDOGENOUS: the water network has a length that grows with
//      the peak revenue ever collected (canals, once dug, stay to be maintained) and shrinks
//      only slowly.  upkeepNeed = netKm * pdPerKm * pdToT.  So a fiscal squeeze is possible.
//  F2  the crown budget is a real BUDGET: army first, then upkeep and monument compete for
//      the same residual by normalised shares, so raising monumentShare directly starves the
//      network (v9 added them independently, which is why the two were bit-identical).
//  F3  network condition feeds each AGENT's harvest: hEff = floor + (1-floor)*infra.
//  F4  demography is food-driven, not threshold-driven: per-capita food ratio drives
//      household growth / excess mortality.  (v9's wealth < -6 && r() < 0.05 almost never fired,
//      and a settlement whose households were half-starved kept growing anyway.)
//  F5  the land ceiling is PER ZONE (zone arable endowment = zoneHeadroom x initial zone land),
//      so the frontier closes when it should instead of being inert.
//  F6  rent accrues to the nearest elite (same zone first), not a random one.
//  F7  charter no longer pinned at 1: prestige has diminishing returns and monScale is finite.
//
// Node 12.  ES5 only.
'use strict';

var D = {
  start: 800, end: 1600, seed: 42,
  nAgents: 400, nZones: 8, maxDist: 150,
  // agronomy
  y: 1.5, lossPct: 16, riceKg: 200, haPerKm2: 100,
  // land
  landPerAgent0: 150, clearProb: 0.05, clearCost: 8, maxLand: 220, peoplePerHH: 5,
  zoneHeadroom: 1.35,      // zone arable endowment = zoneHeadroom x land initially farmed in that zone
  // demography (F4)
  growRate: 0.0025,        // household growth per year at full food security
  mortSlope: 0.12,         // excess-mortality response to the food deficit ratio
  mortMax: 0.06,           // cap on annual household loss
  maxHH: 400,
  minHH: 3,                // below this a settlement is abandoned
  // rent
  rentRate: 0.28, distPenalty: 0.003, crownShare: 0.45,
  rentOnSurplus: 0,        // 1 = rent is a tithe on the surplus above subsistence
  // elites
  eliteFrac: 0.03, distressThreshold: -1.5, sellFrac: 0.05, sellPrice: 1.0,
  normMul: 0.80, debtLimit: 15.0, minLand: 40,
  // crown budget (F2)
  upkeepShare: 0.30, armyShare: 0.10, armyPerKm: 0.35, upkeepSpend: 0.85, monumentShare: 0.18,
  // network (F1)
  km0: 40, kmPer1000T: 30, pdPerKm: 5000, pdToT: 1 / 180,
  infra0: 0.85, infraRepair: 0.030, infraDecay: 0.050, hEffFloor: 0.55,
  netUp: 0.020, netDown: 0.030,
  // charter (F7)
  charter0: 0.60, legitGain: 0.010, legitLoss: 0.005,
  prestigeMax: 0.0015, monScale: 20000, monDep: 0.01,
  // mobility
  migrateThreshold: -0.25, migrateProb: 0.02,
  // shocks
  climateVol: 0.10, droughtYear: 1300, droughtSlope: 0, raidRate: 0.10,
  // relocation
  relocCharter: 0.25, relocCooldown: 60, relocPopLoss: 0.12,
  // switches
  swMigrate: 1, swElite: 1, swMonument: 1, swClimate: 1, swRaid: 1, swUpkeep: 1, swCouple: 1
};

function rng(seed) { var a = (seed >>> 0) || 1; return function () { a += 0x6D2B79F5; var t = a; t = Math.imul(t ^ (t >>> 15), t | 1); t ^= t + Math.imul(t ^ (t >>> 7), t | 61); return ((t ^ (t >>> 14)) >>> 0) / 4294967296; }; }
function normRand(r) { var u = 1 - r(), v = 1 - r(); return Math.sqrt(-2 * Math.log(Math.max(1e-9, u))) * Math.cos(2 * Math.PI * v); }
function clamp(x, a, b) { if (!isFinite(x)) return a; return Math.max(a, Math.min(b, x)); }

function simulate(over) {
  var p = {}, k;
  for (k in D) p[k] = D[k];
  if (over) for (k in over) if (over[k] !== undefined) p[k] = over[k];
  var r = rng(p.seed);
  var N = p.nAgents, Z = p.nZones;

  // ---- agents ----
  var land = new Float64Array(N), hh = new Float64Array(N), wealth = new Float64Array(N);
  var loyalty = new Float64Array(N), zone = new Int8Array(N), elite = new Uint8Array(N);
  var alive = new Uint8Array(N);
  for (var i = 0; i < N; i++) {
    land[i] = p.landPerAgent0 * (0.7 + 0.6 * r());
    hh[i] = 55 + Math.floor(r() * 15);
    wealth[i] = 2 + r() * 2;
    loyalty[i] = 0.5 + r() * 0.3;
    zone[i] = Math.min(Z - 1, Math.floor(r() * Z));
    elite[i] = r() < p.eliteFrac ? 1 : 0;
    alive[i] = 1;
  }
  var zd = [], haul = [];
  for (var z = 0; z < Z; z++) { zd.push((z + 0.5) * p.maxDist / Z); haul.push(Math.pow(0.5, zd[z] / 100)); }

  // ---- F5: per-zone arable endowment ----
  var zoneLand = new Float64Array(Z), zoneCap = new Float64Array(Z);
  var totalLand = 0;
  for (var a0 = 0; a0 < N; a0++) { zoneLand[zone[a0]] += land[a0]; totalLand += land[a0]; }
  var capSum = 0;
  for (var zc = 0; zc < Z; zc++) {
    zoneCap[zc] = Math.max(1, zoneLand[zc]) * p.zoneHeadroom;
    capSum += zoneCap[zc];
  }

  var eliteIdx = [];
  for (var ei = 0; ei < N; ei++) if (elite[ei]) eliteIdx.push(ei);
  // F6: elites of each zone, for nearest-elite rent routing
  var zoneElite = [];
  for (var ze = 0; ze < Z; ze++) {
    zoneElite.push([]);
    for (var ee = 0; ee < N; ee++) if (elite[ee] && zone[ee] === ze) zoneElite[ze].push(ee);
  }
  function nearestElite(z) {
    var d, zz;
    for (d = 0; d < Z; d++) {
      for (var s = -1; s <= 1; s += 2) {
        zz = z + s * d;
        if (zz >= 0 && zz < Z && zoneElite[zz].length) {
          var lst = zoneElite[zz];
          return lst[Math.floor(r() * lst.length)];
        }
      }
      if (d === 0 && zoneElite[z].length) return zoneElite[z][Math.floor(r() * zoneElite[z].length)];
    }
    return eliteIdx.length ? eliteIdx[Math.floor(r() * eliteIdx.length)] : -1;
  }

  var infra = p.infra0, charter = p.charter0, monument = 0;
  var netKm = p.km0, peakRevEver = 0;
  var peakPop = 0, yrPeak = p.start, peakRev = 0, yrRevPeak = 0;
  var relocations = 0, firstReloc = 0, prevReloc = 0;
  var yrCapBound = 0, abandonedTotal = 0;
  var prevRevenue = 0, fundSum = 0, fundYrs = 0, solvSum = 0;
  var rows = [];

  for (var yr = p.start; yr <= p.end; yr++) {
    var season = clamp((yr - p.droughtYear) / 150, 0, 1);
    var shock = p.swClimate ? clamp(normRand(r) * p.climateVol - p.droughtSlope * season * 0.4, -0.6, 0.4) : 0;
    var hEff = p.swCouple ? (p.hEffFloor + (1 - p.hEffFloor) * infra) : 1;

    // ---- harvest, needs, rent (F3: harvest depends on network condition) ----
    var totalRent = 0, totalHarvest = 0, starving = 0, defectors = 0, foodSum = 0, popNow = 0;
    var eliteRent = new Float64Array(N); var shortf = new Float64Array(N); var debt = new Float64Array(N);
    for (var a = 0; a < N; a++) {
      if (!alive[a]) continue;
      var zoneHaul = 1 - 0.5 * (1 - haul[zone[a]]);
      var eff = (1 - p.lossPct / 100) * (1 + shock) * hEff * (0.6 + 0.4 * zoneHaul);
      var harvest = land[a] * p.y * eff;
      var need = hh[a] * p.peoplePerHH * p.riceKg / 1000;
      var rentRate = p.rentRate * (1 + p.distPenalty * zd[zone[a]]);
      // assessed obligation (fixed on normal yield, not on this year's crop) -> arrears in bad years
      // rent is PAID as a share of the actual crop (so crown revenue is elastic) but it is
      // ASSESSED on a normal-year yield, and the shortfall becomes arrears -> dispossession.
      var normHarvest = land[a] * p.y * (1 - p.lossPct / 100) * p.normMul;
      var rent = p.rentOnSurplus ? Math.max(0, harvest - need) * rentRate : harvest * rentRate;
      if (elite[a]) rent = 0; else debt[a] += Math.max(0, (normHarvest - harvest) * rentRate);
      var rentDue = normHarvest * rentRate;
      totalHarvest += harvest; totalRent += rent;
      var net = harvest - need - rent;
      wealth[a] += net;
      // F4: food-driven demography
      var foodPC = (harvest - rent) / Math.max(1e-6, hh[a] * p.peoplePerHH);
      var ratio = foodPC / (p.riceKg / 1000);
      foodSum += ratio * hh[a] * p.peoplePerHH;
      shortf[a] = net / Math.max(1e-6, need);
      if (ratio < 1) {
        starving++;
        hh[a] *= (1 - Math.min(p.mortMax, p.mortSlope * (1 - ratio)));
        loyalty[a] = clamp(loyalty[a] - 0.03 * (1 - ratio), 0, 1);
      } else {
        hh[a] = Math.min(p.maxHH, hh[a] * (1 + p.growRate * Math.min(1.5, ratio - 1)));
        loyalty[a] = clamp(loyalty[a] + 0.004 * Math.min(2, ratio - 1), 0, 1);
      }
      if (hh[a] < p.minHH) { alive[a] = 0; abandonedTotal++; }
      popNow += hh[a] * p.peoplePerHH;
      if (loyalty[a] < 0.25) defectors++;
      if (!elite[a]) { var ne = nearestElite(zone[a]); if (ne >= 0) eliteRent[ne] += rent; }
    }

    // ---- elites buy land from distressed cultivators ----
    for (var c = 0; c < N; c++) {
      if (elite[c] || !alive[c]) continue;
      var dstress = (debt[c] > p.debtLimit) || (wealth[c] < p.distressThreshold);
      if (dstress && p.swElite && eliteIdx.length) {
        var e2 = nearestElite(zone[c]);
        if (e2 < 0) continue;
        var owed = Math.max(debt[c], -wealth[c]);
        var want = Math.min(land[c] * p.sellFrac, Math.max(0, land[c] - p.minLand), owed / p.sellPrice);
        if (want > 0.01) {
          land[c] -= want; land[e2] += want;
          wealth[c] += want * p.sellPrice; debt[c] = 0;
          zoneElite[zone[c]] = zoneElite[zone[c]]; // no-op, keeps shapes
        }
      } else if (wealth[c] > p.clearCost * 2 && land[c] < p.maxLand && r() < p.clearProb) {
        // F5: clearing only into the zone's remaining arable endowment
        var zz2 = zone[c];
        if (zoneLand[zz2] + p.clearCost <= zoneCap[zz2]) {
          land[c] += p.clearCost; zoneLand[zz2] += p.clearCost; totalLand += p.clearCost;
          wealth[c] -= p.clearCost * 1.0;
        } else if (!yrCapBound) yrCapBound = yr;
      }
    }

    // ---- migration ----
    var migrated = 0;
    if (p.swMigrate) {
      for (var m = 0; m < N; m++) {
        if (!alive[m] || elite[m]) continue;
        if (wealth[m] < p.migrateThreshold && r() < p.migrateProb * 8) {
          var up = zone[m] - 1, dn = zone[m] + 1, dir = 0;
          var roomUp = up >= 0 ? (zoneCap[up] - zoneLand[up]) : -1;
          var roomDn = dn < Z ? (zoneCap[dn] - zoneLand[dn]) : -1;
          if (roomUp < 0 && roomDn < 0) dir = 0;
          else if (roomDn > roomUp) dir = 1;
          else dir = -1;
          var nz = clamp(zone[m] + dir, 0, Z - 1);
          zone[m] = nz; migrated++;
        }
      }
    }
    var aliveN = 0;
    for (var q = 0; q < N; q++) if (alive[q]) aliveN++;

    // ---- crown revenue ----
    var eliteLiquid = 0;
    for (var b = 0; b < N; b++) if (elite[b] && alive[b]) eliteLiquid += eliteRent[b];
    var crownRevenue = eliteLiquid * p.crownShare * (0.4 + 0.6 * charter);

    // ---- F1: endogenous network length, F2: budget split ----
    if (crownRevenue > peakRevEver) peakRevEver = crownRevenue;
    var netTarget = p.km0 + peakRevEver * p.kmPer1000T / 1000;
    netKm += (netTarget - netKm) * (netTarget > netKm ? p.netUp : p.netDown);
    var upkeepNeed = netKm * p.pdPerKm * p.pdToT;
    var armyCost = p.armyPerKm * netKm * (0.6 + 0.4 * charter);
    var monBudget = p.swMonument ? Math.max(0, crownRevenue - armyCost) * p.monumentShare : 0;
    var residual = Math.max(0, crownRevenue - armyCost - monBudget);
    var upkeepBudget = residual * p.upkeepShare;
    var upkeepPaid = Math.min(upkeepNeed, upkeepBudget);
    var fundedFrac = upkeepNeed > 0 ? upkeepPaid / upkeepNeed : 1;
    if (p.swUpkeep) infra = clamp(infra + p.infraRepair * fundedFrac - p.infraDecay * (1 - fundedFrac), 0.05, 1);
    monument += monBudget * (1 - p.monDep);

    // ---- charter (F7) ----
    var solvency = crownRevenue / Math.max(1, upkeepNeed);
    var prestige = p.prestigeMax * (monument / (monument + p.monScale));
    charter = clamp(charter + prestige + p.legitGain * clamp(solvency - 1, -1, 1)
      - p.legitLoss * (defectors / Math.max(1, aliveN)), 0, 1);

    // ---- raids ----
    if (p.swRaid && r() < p.raidRate * 0.06) {
      for (var rr = 0; rr < Math.floor(N * 0.02); rr++) { var v = Math.floor(r() * N); if (alive[v]) wealth[v] -= 1.0; }
    }

    // ---- relocation ----
    if (charter < p.relocCharter && (yr - prevReloc > p.relocCooldown || !prevReloc)) {
      relocations++; if (!firstReloc) firstReloc = yr;
      prevReloc = yr; charter = 0.45; monument = 0;
      infra = Math.max(0.55, infra * 0.85); netKm = p.km0 * 1.5; peakRevEver = 0;
      for (var z3 = 0; z3 < Z; z3++) haul[z3] = Math.pow(0.5, zd[z3] / 100);
      for (var q2 = 0; q2 < N; q2++) if (alive[q2]) hh[q2] *= (1 - p.relocPopLoss);
    }

    if (popNow > peakPop) { peakPop = popNow; yrPeak = yr; }
    if (crownRevenue > peakRev) { peakRev = crownRevenue; yrRevPeak = yr; }
    fundSum += fundedFrac; solvSum += solvency; fundYrs++;
    prevRevenue = crownRevenue;

    rows.push({ yr: yr, pop: popNow, popN: aliveN, revenue: crownRevenue, charter: charter,
      infra: infra, hEff: hEff, netKm: netKm, upkeepNeed: upkeepNeed, fundedFrac: fundedFrac,
      solvency: solvency, monument: monument, rent: totalRent, defectors: defectors,
      migrated: migrated, starving: starving, eliteShare: landShare(elite, land, alive, N) });
  }

  var last = rows[rows.length - 1];
  var landByElite = 0, landByFarm = 0, nE = 0, nF = 0;
  for (var w = 0; w < N; w++) if (alive[w]) { if (elite[w]) { landByElite += land[w]; nE++; } else { landByFarm += land[w]; nF++; } }

  // discount the peak year if population never actually fell (flat-monotone = no peak)
  var interior = yrPeak < p.end - 5 ? 1 : 0;
  return {
    peakPop: Math.round(peakPop), yrPopPeak: yrPeak, peakRev: Math.round(peakRev), yrRevPeak: yrRevPeak,
    endPop: Math.round(last.pop), endRev: Math.round(last.revenue), endCharter: +last.charter.toFixed(3),
    endInfra: +last.infra.toFixed(3), endMonument: Math.round(last.monument), endNetKm: +last.netKm.toFixed(1),
    minInfra: +Math.min.apply(null, rows.map(function (x) { return x.infra; })).toFixed(3),
    meanFunded: +(fundSum / Math.max(1, fundYrs)).toFixed(3),
    relocations: relocations, firstReloc: firstReloc, residentsLast: last.popN,
    abandoned: abandonedTotal, yrCapBound: yrCapBound, interiorPeak: interior,
    eliteShareOfLand: +(landByElite / Math.max(1e-9, landByElite + landByFarm)).toFixed(3),
    nElite: nE, nFarmer: nF,
    relocLag: (firstReloc && yrPeak) ? firstReloc - yrPeak : -999,
    revenueDecline: peakRev > 0 ? +(1 - last.revenue / peakRev).toFixed(3) : 0,
    popDecline: peakPop > 0 ? +(1 - last.pop / peakPop).toFixed(3) : 0,
    rows: rows
  };
}
function landShare(elite, land, alive, N) {
  var e = 0, f = 0;
  for (var i = 0; i < N; i++) if (alive[i]) { if (elite[i]) e += land[i]; else f += land[i]; }
  return e / Math.max(1e-9, e + f);
}

module.exports = { simulate: simulate, DEFAULTS: D };
