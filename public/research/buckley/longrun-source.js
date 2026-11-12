/* Angkor 802-1450: the standard explanations as switchable mechanisms. One step per year.
 * Background in every run: kings die (mean reign 20 years); some successions are contested,
 * and a contest cuts the labour the court can command (waxing and waning).
 * Mechanisms and the dates they take from outside evidence:
 *   war       Ayutthaya attacks 1353, 1370, 1431 (chronicle dates): people carried off, court flees.
 *   orgy      Jayavarman VII's building 1181-1218 takes labour first, and every temple built
 *             carries endowed upkeep forever after (temples were assigned villages and workers).
 *   theravada royal temple-labour claims fade: monks at Angkor 1296 (Zhou Daguan), royal Pali
 *             inscription 1308/09. Ramp centre drawn 1290-1320.
 *   trade     an outside option pulls the court south. Date NOT fixed by evidence (1150-1450).
 *   drought   dry 1335-1365 and 1400-1425 (Buckley et al. 2010).
 *   hydraulic upkeep per unit of network rises as channels silt (Groslier, Fletcher).
 * Population is a share of food-limited capacity (~590k people in the seasonal model). */
'use strict';
globalThis.AngkorStandard = (() => {
  const FIRST = 802, LAST = 1450;
  const MECH = ['war', 'orgy', 'theravada', 'trade', 'drought', 'hydraulic'];
  const fixed = Object.freeze({droughts: [[1335, 1365], [1400, 1425]], attacks: [1353, 1370, 1431],
    orgy: [1181, 1218], fieldLabour: .26});
  const rngFrom = seed => { let s = seed >>> 0; return () => ((s = (Math.imul(1664525, s) + 1013904223) >>> 0) / 4294967296); };
  const logistic = (t, mid, width) => 1 / (1 + Math.exp(-(t - mid) / width));

  function run(p, on) {
    const wr = rngFrom(p.seed), kr = rngFrom(p.seed ^ 0x9e3779b9);   // separate streams: weather, kings
    const b = p.bondedShare;
    const pool0 = p.bondedWork * b + p.corvee * (1 - b);              // court labour at baseline
    const unitNeed = pool0 / p.slack;                                  // upkeep per unit of network at baseline
    let N = .08, B = .08 * b, C = .3, E = 1, S = .088, M = 0;
    let reignLeft = 1 + Math.floor(-20 * Math.log(1 - kr())), contest = 0;
    const rows = [];
    for (let year = FIRST; year <= LAST; year++) {
      // kings: succession contests are the background waxing and waning
      if (--reignLeft <= 0) {
        reignLeft = 1 + Math.floor(-20 * Math.log(1 - kr()));
        if (kr() < p.contestProb) contest = 2 + Math.floor(kr() * 14);
      }
      const cohesion = contest > 0 ? p.contestCut : 1;
      if (contest > 0) contest--;
      // weather
      const dry = on.drought && fixed.droughts.some(([a, z]) => year >= a && year <= z);
      const w = Math.min(1.15, (dry ? p.droughtMean : 1) + p.noise * (wr() + wr() + wr() - 1.5));
      const buffered = w < 1 ? w + C * p.buffer * (1 - w) : w;
      const capacity = buffered * (1 + p.channelGain * C) / (1 + p.channelGain);
      const P0 = N + B;
      const harvest = capacity * Math.min(1, (N + .75 * B) / fixed.fieldLabour);
      const shortfall = Math.max(0, 1 - harvest / P0);
      const follow = p.follow * (1 - E);
      const growth = shortfall > 0 ? -p.famine * shortfall : p.growth * (1 - P0 / harvest);
      N = Math.max(0, N * (1 + growth - follow));
      const captives = p.attrition * b * N / (1 - b);                  // steady inflow keeps B/P ~ b
      B = Math.max(0, B * (1 - p.attrition - (shortfall > 0 ? p.famine * shortfall : 0) - follow) + captives);
      // war: attacks carry people off and drive the court out for a while
      if (on.war && fixed.attacks.includes(year)) { N *= 1 - p.warLoss; B *= 1 - 2 * p.warLoss; E *= 1 - p.warFlight; }
      // labour the court commands; Theravada erodes temple-labour claims
      const devotion = on.theravada ? 1 - (1 - p.theravadaFloor) * logistic(year, p.theravadaYear, 10) : 1;
      const pool = (p.bondedWork * B + p.corvee * E * N) * devotion * cohesion;
      // upkeep: network built for the peak, silting, and endowed temples
      S = Math.max(S, N + B);
      const silt = on.hydraulic ? 1 + p.silt * Math.max(0, year - 1000) / 100 : 1;
      const need = unitNeed * S * silt + (on.orgy ? p.templeUpkeep * M : 0);
      const inOrgy = on.orgy && year >= fixed.orgy[0] && year <= fixed.orgy[1];
      let build, upkeep;
      if (inOrgy) { build = pool * p.orgyShare; upkeep = Math.min(need, pool - build); }
      else { upkeep = Math.min(need, pool); build = pool - upkeep; }
      M += build;
      const maintained = need > 0 ? upkeep / need : 1;
      C = C * (1 - p.decay) + p.decay * Math.min(1, maintained);
      // court presence: per-head revenue against an outside option
      const Pn = Math.max(1e-9, N + B);
      const revenue = .5 * Math.min(1.5, harvest / Pn) + .5 * (B / Pn) / b;
      const outside = on.trade ? p.outside0 + (p.outside1 - p.outside0) * logistic(year, p.tradeYear, 20) : p.outside0;
      const gap = revenue - outside;
      E = Math.min(1, Math.max(0, E + p.court * (gap > 0 ? (1 - E) * gap : E * gap)));
      rows.push({year, P: N + B, C, E, build, maintained, core: E * (N + B), moat: E * Math.min(1, maintained),
        devotion, cohesion});
    }
    return rows;
  }

  function score(rows) {
    const at = y => rows[y - FIRST];
    const mean = (a, z, k) => { let s = 0; for (let y = a; y <= z; y++) s += at(y)[k]; return s / (z - a + 1); };
    const sustained = (test, from, span) => {
      for (let y = from; y <= LAST - span; y++) {
        let ok = true;
        for (let k = 0; k < span; k++) if (!test(at(y + k))) { ok = false; break; }
        if (ok) return y;
      }
      return null;
    };
    const coreRef = mean(1250, 1290, 'core'), buildRef = mean(1100, 1220, 'build');
    const onset = sustained(r => r.core < .85 * coreRef, 1250, 15);
    const deep = sustained(r => r.core < .4 * coreRef, 1250, 15);
    const moatLost = sustained(r => r.moat < .3, 1250, 10);
    let peak = 0, peakYear = FIRST; rows.forEach(r => { if (r.P > peak) { peak = r.P; peakYear = r.year; } });
    return {onset, deep, moatLost, peakYear,
      build1230_90: buildRef > 0 ? mean(1230, 1290, 'build') / buildRef : 0,
      build1300_50: buildRef > 0 ? mean(1300, 1350, 'build') / buildRef : 0,
      pop1431: at(1431).P / peak};
  }

  // Observations, each from a dated source (see RESULTS2.txt)
  function tests(s) {
    return {
      buildingFalls: s.build1230_90 < .35,                                  // few monuments after ~1220
      buildingStops: s.build1300_50 < .1,                                   // last major temple 1295
      coreOnset: s.onset != null && s.onset >= 1300 && s.onset <= (+process.env.ONSET_END || 1340),  // moat cores
      moatBy1400: s.moatLost != null && s.moatLost <= 1400,                 // moat cores
      gradual: s.onset != null && ((s.deep ?? 1451) - s.onset) >= 40,       // moat cores
      notEmpty: s.pop1431 > .25,                                            // reoccupation, Angkor Wat used on
      apogee: s.peakYear >= 1150 && s.peakYear <= 1340};                    // lidar population study
  }

  function drawPriors(rnd, seed) {
    const u = (a, z) => a + (z - a) * rnd();
    const attrition = u(.02, .06);
    return {seed, attrition, bondedShare: Math.min(.4, u(.0028, .0038) / attrition),
      growth: u(.01, .025), famine: u(.3, 1), follow: u(.005, .04), decay: u(.03, .1), slack: u(1.1, 1.6),
      bondedWork: u(.3, .7), corvee: u(.03, .08),
      buffer: u(.3, .8), channelGain: u(.12, .4), droughtMean: u(.65, .85), noise: u(.05, .12),
      contestProb: u(.2, .6), contestCut: u(.2, .6),
      warLoss: u(.05, .2), warFlight: u(.3, .8),
      orgyShare: u(.5, .9), templeUpkeep: u(.002, .02),
      theravadaYear: u(1290, 1320), theravadaFloor: u(.2, .6),
      silt: u(.02, .15), court: u(.05, .3), outside0: u(.5, .8), outside1: u(1, 1.6), tradeYear: u(1150, 1450)};
  }
  return {run, score, tests, drawPriors, rngFrom, MECH, fixed, FIRST, LAST};
})();
