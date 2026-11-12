/* Cambodia child labour simulator: two linked regions (Phnom Penh, countryside).
   Built on the Atlas childlabour.js mechanics, extended with migration, remittances, left-behind children,
   factory-only ban enforcement, microfinance debt, teacher-sold tutoring and a credential floor by region.
   Money is in units of one adult informal annual wage (= 1). Every constant is an assumption unless noted. */
(function (root) {
'use strict';
const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));
const sum = a => a.reduce((s, x) => s + x, 0);
function rng(seed) { let n = seed >>> 0; return () => ((n = (n * 1664525 + 1013904223) >>> 0) / 2 ** 32); }
function normal(r) { let u = 0; while (u === 0) u = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * r()); }
const STATES = ['school', 'both', 'work', 'neither'];
const HAZ = .35;   // A: share of full-time 15-17 workers in hazardous work or over 48 hours

const REGIONS = {
  pp: {label: 'Phnom Penh', khmer: 'ភ្នំពេញ', share: .22, yMedian: 1.55, ySigma: .6, shockP: .08, shockSize: .35, borrow: .22,
    debt: .07, distance: 0, quality: .62, safety: .66, localPull: 1.25, enterprise: .18, leftBehind: .05, formalJobs: .40,
    tutoring: .06, credFloor: .55, migrate: false, vPrim: 3.391, vLow: 2.162, vUp: .886},
  rural: {label: 'Countryside', khmer: 'ជនបទ', share: .78, yMedian: .9, ySigma: .6, shockP: .16, shockSize: .45, borrow: .12,
    debt: .12, distance: .45, quality: .50, safety: .64, localPull: .80, enterprise: .55, leftBehind: .20, formalJobs: .05,
    tutoring: .025, credFloor: .25, migrate: true, vPrim: 3.506, vLow: 5.657, vUp: 2.199},
};

const POLICY0 = {
  cashU: 0,         // unconditional transfer to the same households, paid whatever the child does (income effect only)
  cash: 0,          // transfer to IDPoor households (bottom two quintiles) with a child enrolled, adult-wage units per child-year
  feeding: 0,       // school meals coverage 0-1
  protection: 0,    // schools as protection: safety, care, counselling 0-1 (Nordtveit)
  leftSupport: 0,   // support for children whose parents migrated 0-1 (Nordtveit: orphans and vulnerable children analogue)
  harvest: 0,       // flexible timetable around rice planting and harvest 0-1
  bridging: 0,      // re-entry and bridging classes for dropouts 0-1
  tutorFix: 0,      // end teacher-sold extra classes (teacher pay instead) 0-1 (Bray)
  ban: 0,           // enforcement of minimum working age 0-1; inspectors reach factories only (Better Factories Cambodia)
  debtRelief: 0,    // microfinance debt restructuring 0-1
  garmentBoom: 0,   // rise in teen wages in Phnom Penh factories and construction, share
  thaiOpen: 1,      // Thailand route for migrant parents and teens: 1 open, 0 closed (July 2025 border conflict)
  floorRise: 0,     // more formal jobs read the Grade 12 diploma (the relational floor binds) 0-1
};

function simulate(opts) {
  const o = Object.assign({years: 12, N: 6000, seed: 7, policy: {}, over: {}}, opts || {});
  const P = Object.assign({}, POLICY0, o.policy);
  const R = {pp: Object.assign({}, REGIONS.pp, (o.over.pp || {})), rural: Object.assign({}, REGIONS.rural, (o.over.rural || {}))};
  const r = rng(o.seed);
  const H = [];
  for (let i = 0; i < o.N; i++) {
    const reg = r() < R.pp.share ? 'pp' : 'rural', C = R[reg];
    const z = normal(r);
    H.push({reg, z, y0: C.yMedian * Math.exp(C.ySigma * z), age: 6 + Math.floor(r() * 12), girl: r() < .5,
      left: r() < C.leftBehind * (1.3 - .5 * (z > 0)), thai: r() < .65, ability: normal(r),
      enterprise: r() < C.enterprise, outYears: 0, everOut: false, taste: normal(r)});
  }
  const qcut = [-.8416, -.2533, .2533, .8416];
  const quint = h => qcut.filter(c => h.z > c).length;
  const wChild = {pp: 1, rural: 1};
  let L0 = null;
  const rows = [];
  let spent = {cash: 0, other: 0};
  for (let t = 0; t < o.years; t++) {
    const decide = () => {
      const S = {pp: mk(), rural: mk(), all: mk()};
      function mk() { return {n: 0, school: 0, both: 0, work: 0, neither: 0, cl: 0, migrant: 0, lab: 0,
        lvl: [[0, 0], [0, 0], [0, 0]], q: [0, 1, 2, 3, 4].map(() => ({n: 0, cl: 0})), girls: [0, 0], boys: [0, 0], left: [0, 0]}; }
      const choice = [], migr = [];
      let cash = 0;
      for (const h of H) {
        const C = R[h.reg], q = quint(h), a = h.age, rural = h.reg === 'rural';
        // household income: wage, shocks buffered by credit, microfinance repayments, remittances
        const shocked = r() < C.shockP;
        let y = h.y0 * (shocked ? 1 - C.shockSize : 1);
        if (shocked) y += Math.min(C.shockSize * h.y0, (C.borrow + P.debtRelief * .1) * h.y0);
        y -= C.debt * h.y0 * (1 - P.debtRelief * .7);
        let left = h.left;
        if (h.left) {
          if (h.thai && P.thaiOpen < 1) { y += .6 * .63 * (1 - P.thaiOpen); left = r() < P.thaiOpen; y += .45 * P.thaiOpen; }
          else y += .45;                                                        // remittance from a parent working away
        }
        if (q <= 1) y += P.cashU;                                               // unconditional transfer: income effect only
        const need = .85;
        // child earnings: local market (ban bites only on the formal, inspected share), family farm or stall, migration
        const ageW = a < 10 ? .25 : a < 12 ? .45 : a < 15 ? .7 : 1;
        const visible = P.ban * C.formalJobs;
        const pull = C.localPull * (h.reg === 'pp' && a >= 14 ? 1 + P.garmentBoom : 1);
        const famRet = h.enterprise ? .55 : 0;
        let earn = .32 * ageW * Math.max(wChild[h.reg] * pull * (1 - visible), famRet);
        let mig = false;
        if (C.migrate && a >= 15) {
          const toPP = .32 * R.pp.localPull * (1 + P.garmentBoom) * wChild.pp * (1 - P.ban * R.pp.formalJobs) - .10;
          const toTH = .32 * 1.9 * P.thaiOpen - .14;
          const best = Math.max(toPP, toTH) * .8;                               // share sent home
          if (best > earn) { earn = best; mig = true; }
        }
        // school: costs, value by level, protection, the credential floor
        const lvl = a <= 11 ? 0 : a <= 14 ? 1 : 2;
        const fee = [.03, .08, .13][lvl];
        const tut = C.tutoring * [.6, 1, 1.4][lvl] * (1 - P.tutorFix);
        const dist = C.distance * [.03, .14, .22][lvl];
        const cost = fee + tut + dist;
        const feed = P.feeding * (lvl === 0 ? .07 : .05);
        const cashAmt = q <= 1 ? P.cash : 0;
        const quality = clamp(C.quality + .15 * P.protection + .05 * P.tutorFix + (h.outYears > 0 ? .2 * P.bridging : 0), 0, 1.2);
        const safety = clamp(C.safety + P.protection * (1 - C.safety), 0, 1);
        const leftPen = left ? -.45 * (1 - P.leftSupport) : 0;
        const reentry = h.outYears > 0 ? -1.3 * (1 - .7 * P.bridging) * Math.min(h.outYears, 3) / 3 : 0;
        const floor = lvl === 2 ? 1.1 * (clamp(C.credFloor + P.floorRise * (1 - C.credFloor), 0, 1) - .4) : 0;
        const vLvl = [C.vPrim, C.vLow, C.vUp][lvl];
        const valueSchool = vLvl + 1.1 * (quality - .55) + 1.2 * (safety - .65) + leftPen + reentry + floor + .25 * h.ability;
        const harvestWork = rural && a >= 12 ? .5 * P.harvest : 0;               // adolescents: school and seasonal work fit together
        const util = c => { const x = c - .6 * need, x0 = .05; return x > x0 ? Math.log(x) : Math.log(x0) + (x - x0) / x0; };
        const U = {
          school: util(y - cost + feed + cashAmt) + valueSchool,
          both: util(y - cost + feed + cashAmt + .5 * earn) + valueSchool * .72 + harvestWork - .25,
          work: util(y + earn) - .2 * h.taste,
          neither: util(y) - .6 + (h.girl ? .25 : 0),
        };
        const m = Math.max(U.school, U.both, U.work, U.neither);
        const ex = STATES.map(s => Math.exp((U[s] - m) / .3)); const Z = sum(ex);
        let u = r() * Z, k = 0; while (u > ex[k] && k < 3) { u -= ex[k]; k++; }
        const s = STATES[k];
        choice.push(s); migr.push(s === 'work' && mig);
        if (s === 'school' || s === 'both') cash += cashAmt;
        if (q <= 1) cash += P.cashU;
        const isCL = (s === 'work' && (a < 15 || r() < HAZ)) || (s === 'both' && a < 12);   // ILO: 15-17 only if hazardous or over 48 hours
        for (const G of [S[h.reg], S.all]) {
          G.n++; G[s]++; if (isCL) G.cl++; if (s === 'work' && mig) G.migrant++;
          if (s === 'work' && !mig) G.lab += ageW; if (s === 'both') G.lab += .5 * ageW;
          G.lvl[lvl][1]++; if (s === 'work' || s === 'neither') G.lvl[lvl][0]++;
          G.q[q].n++; if (isCL) G.q[q].cl++;
          const g = h.girl ? G.girls : G.boys; g[1]++; if (isCL) g[0]++;
          if (left) { G.left[1]++; if (isCL) G.left[0]++; }
        }
      }
      return {S, choice, migr, cash};
    };
    let D = decide();
    if (L0 === null) L0 = {pp: Math.max(D.S.pp.lab, 1), rural: Math.max(D.S.rural.lab, 1)};
    for (let it = 0; it < 3; it++) {                                            // child wages clear in each region
      for (const k of ['pp', 'rural']) wChild[k] = clamp(Math.pow(Math.max(D.S[k].lab, 1) / L0[k], -1 / 2.5), .4, 2.2);
      D = decide();
    }
    spent.cash += D.cash;
    const nPP = D.S.pp.n, nR = D.S.rural.n;
    spent.other += nPP * cst(P, 'pp') + nR * cst(P, 'rural');
    const pack = G => ({n: G.n, school: G.school / G.n, both: G.both / G.n, work: G.work / G.n, neither: G.neither / G.n,
      attend: (G.school + G.both) / G.n, cl: G.cl / G.n, migrant: G.migrant / G.n,
      oos: G.lvl.map(x => x[1] ? x[0] / x[1] : 0), clPoor: G.q[0].cl / Math.max(G.q[0].n, 1), clRich: G.q[4].cl / Math.max(G.q[4].n, 1),
      clGirls: G.girls[0] / Math.max(G.girls[1], 1), clBoys: G.boys[0] / Math.max(G.boys[1], 1), clLeft: G.left[0] / Math.max(G.left[1], 1),
      balance: G.school + G.both + G.work + G.neither - G.n});
    rows.push({t, year: 2025 + t, pp: pack(D.S.pp), rural: pack(D.S.rural), all: pack(D.S.all), wChild: Object.assign({}, wChild),
      choice: D.choice.slice(), migr: D.migr.slice(), age: H.map(h => h.age), left: H.map(h => h.left)});
    H.forEach((h, i) => {
      const s = D.choice[i];
      if (s === 'work' || s === 'neither') { h.outYears++; h.everOut = true; } else h.outYears = 0;
      h.age++;
      if (h.age > 17) { h.age = 6; h.outYears = 0; h.everOut = false; h.ability = normal(r); h.girl = r() < .5; }
    });
  }
  return {rows, spent: {cash: spent.cash, other: spent.other, total: spent.cash + spent.other}, N: o.N, H, P};
}
function cst(P, reg) {   // per child per year, adult-wage units (assumed unit costs)
  return P.feeding * .05 + P.protection * .03 + (reg === 'rural' ? P.leftSupport * REGIONS.rural.leftBehind * .08 + P.harvest * .005 : P.leftSupport * .004)
    + P.bridging * .01 + P.tutorFix * .03 + P.ban * .004 + P.debtRelief * .02;
}
function compare(opts) {
  const base = simulate(Object.assign({}, opts, {policy: {thaiOpen: (opts.policy || {}).thaiOpen ?? 1}}));
  const pol = simulate(opts);
  const yearsAvoided = sum(base.rows.map((x, i) => x.all.cl - pol.rows[i].all.cl)) * base.N;
  return {base, pol, yearsAvoided, costPer: yearsAvoided > 0 ? pol.spent.total / yearsAvoided : null};
}
const api = {simulate, compare, REGIONS, POLICY0};
if (typeof module !== 'undefined') module.exports = api;
root.CamChild = api;
})(typeof window !== 'undefined' ? window : globalThis);
