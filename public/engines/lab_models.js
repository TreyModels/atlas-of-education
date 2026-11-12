/* Education Atlas Planning Lab — models in the IIEP / UIS / education-sector-analysis tradition.
   Independent implementations of published methods. They are not official UNESCO, IIEP, UIS or World Bank software,
   and no workbook equivalence is claimed. Pure functions; CommonJS in Node (tests/test_lab.cjs), AtlasLab in a browser. */
(function (root) {
'use strict';
const sum = a => a.reduce((s, x) => s + x, 0);
const clamp = (x, lo, hi) => Math.max(lo, Math.min(hi, x));
const lerp = (a, b, w) => a + (b - a) * w;
function rng(seed) { let n = seed >>> 0; return () => ((n = (n * 1664525 + 1013904223) >>> 0) / 2 ** 32); }
function normal(r) { let u = 0, v = 0; while (u === 0) u = r(); v = r(); return Math.sqrt(-2 * Math.log(u)) * Math.cos(2 * Math.PI * v); }

/* 1. Flow rates from two years of grade enrolment (UIS reconstructed cohort method).
   E0[g], E1[g]: enrolment in grade g in years t and t+1; R1[g]: repeaters in grade g in t+1; G0: graduates of the last
   grade in year t (optional; otherwise promotion from the last grade is the remainder after repetition and an assumed
   last-grade dropout rate d_last). r = R1/E0; p = (E1[g+1] - R1[g+1]) / E0[g]; d = 1 - p - r. */
function flowRates(E0, E1, R1, opts) {
  const n = E0.length, o = opts || {};
  const r = E0.map((e, g) => R1[g] / e);
  const p = E0.map((e, g) => g < n - 1 ? (E1[g + 1] - R1[g + 1]) / e : (o.G0 !== undefined ? o.G0 / e : 1 - r[g] - (o.d_last || 0)));
  const d = p.map((pp, g) => 1 - pp - r[g]);
  return {p, r, d};
}

/* 2. Reconstructed cohort: follow a cohort of `size` entrants through grades with constant flow rates, allowing up to
   `maxRep` repetitions per grade (UIS convention). Outputs survival by grade, graduates, pupil-years, years input per
   graduate and the coefficient of efficiency (graduates x duration / pupil-years). */
function cohort(p, r, opts) {
  const o = Object.assign({size: 1000, maxRep: 3}, opts || {});
  const n = p.length;
  const reach = [], pupilYears = [], dropByGrade = [];
  let graduates = 0, gradYears = 0, totalYears = 0, dropouts = 0;
  // track (repeats used, years spent) as a distribution: state[k] = mass that has used k repeats in total
  let state = [{k: 0, years: 0, mass: o.size}];
  for (let g = 0; g < n; g++) {
    reach.push(sum(state.map(s => s.mass)));
    let py = 0; const next = []; let drop = 0;
    for (const s of state) {
      let mass = s.mass, k = s.k, years = s.years;
      while (mass > 1e-12) {
        py += mass; years += 1;
        const prom = mass * p[g], rep = k < o.maxRep ? mass * r[g] : 0, dr = mass - prom - rep;
        drop += dr; totalYears += dr * years;
        if (prom > 0) next.push({k, years, mass: prom});
        mass = rep; k += 1;
      }
    }
    pupilYears.push(py); dropByGrade.push(drop); dropouts += drop;
    // merge identical (k, years) states to keep the list small
    const m = new Map(); for (const s of next) { const key = s.k + ':' + s.years; m.set(key, (m.get(key) || 0) + s.mass); }
    state = [...m].map(([key, mass]) => ({k: +key.split(':')[0], years: +key.split(':')[1], mass}));
  }
  for (const s of state) { graduates += s.mass; gradYears += s.mass * s.years; totalYears += s.mass * s.years; }
  const PY = sum(pupilYears);
  const yearsPerGraduate = graduates > 0 ? PY / graduates : Infinity;
  return {reach, survival: reach.map(x => x / o.size), pupilYears, dropByGrade, graduates, dropouts, totalPupilYears: PY,
    yearsPerGraduate, coefficientOfEfficiency: graduates > 0 ? graduates * n / PY : 0,
    wastedShare: PY > 0 ? 1 - graduates * n / PY : 0, avgYearsGraduates: graduates > 0 ? gradYears / graduates : 0,
    balance: o.size - graduates - dropouts};
}

/* 3. Cohort-component projection of the school-age population by single year of age (0..A-1).
   pop[a][t+1] = pop[a-1][t] * surv[a-1] + mig[a]; age 0 = births(t). Mass balance is returned. */
function populationProjection(o) {
  const A = o.ages || 25, T = o.years, surv = o.survival, out = [];
  let pop = o.initial.slice();
  const balance = [];
  for (let t = 0; t < T; t++) {
    out.push(pop.slice());
    const next = new Array(A).fill(0);
    const B = o.births(t);
    next[0] = B;
    let deaths = 0;
    for (let a = 1; a < A; a++) { const s = surv(a - 1); next[a] = pop[a - 1] * s + (o.migration ? o.migration(a, t) : 0); deaths += pop[a - 1] * (1 - s); }
    const aged = pop[A - 1];
    const mig = o.migration ? sum(Array.from({length: A - 1}, (_, i) => o.migration(i + 1, t))) : 0;
    balance.push(sum(next) - (sum(pop) + B - deaths - aged + mig));
    pop = next;
  }
  return {pop: out, balance};
}

/* 4. Enrolment, resource and financing projection by flow-rate targets (EPSSim-style sector simulation).
   Rates move linearly from base-year values to target-year values. Intake = intake rate x population at entry age.
   Teachers = enrolment / PTR; classrooms = enrolment / (class size x shifts); recurrent cost = teachers x salary
   (multiple of GDP per capita) x GDPpc + non-salary share; capital = new classrooms x room cost; resources = GDP x
   revenue ratio x education share x primary share. Financing gap = cost - resources (never clipped). */
function sectorSimulation(o) {
  const n = o.grades, Y = o.years, out = [];
  let E = o.E0.slice();
  let rooms = o.rooms0, gdp = o.gdp0, popAge = o.popAge;   // popAge(t, age) -> population
  const pupilBalance = [];
  for (let t = 0; t < Y; t++) {
    const w = clamp(t / Math.max(1, o.targetYear), 0, 1);
    const intakeRate = lerp(o.intake0, o.intakeT, w), rep = lerp(o.rep0, o.repT, w), drop = lerp(o.drop0, o.dropT, w);
    const ptr = lerp(o.ptr0, o.ptrT, w), salary = lerp(o.salary0, o.salaryT, w), nonsal = lerp(o.nonsal0, o.nonsalT, w);
    const pupils = sum(E), school = sum(Array.from({length: n}, (_, g) => popAge(t, o.entryAge + g)));
    const teachers = pupils / ptr;
    const roomsNeeded = pupils / (o.classSize * o.shifts);
    const newRooms = Math.max(0, roomsNeeded - rooms);
    const gdppc = gdp / o.population(t);
    const salaryBill = teachers * salary * gdppc;
    const recurrent = salaryBill / (1 - nonsal);
    const capital = newRooms * o.roomCost * gdppc;
    const resources = gdp * o.revenue * o.eduShare * o.primaryShare;
    const completers = E[n - 1] * Math.max(0, 1 - rep - drop);
    out.push({t, year: o.startYear + t, enrolment: E.slice(), pupils, ger: pupils / school, intakeRate, teachers, rooms: Math.max(rooms, roomsNeeded),
      newRooms, recurrent, capital, cost: recurrent + capital, resources, gap: recurrent + capital - resources,
      completionRate: completers / popAge(t, o.entryAge + n), unitCostShareGDPpc: recurrent / pupils / gdppc, gdp});
    // flows to next year
    const promote = 1 - rep - drop;
    const entrants = intakeRate * popAge(t + 1, o.entryAge);
    const next = E.map((e, g) => e * rep + (g ? E[g - 1] * promote : entrants));
    pupilBalance.push(sum(next) - (pupils + entrants - pupils * drop - E[n - 1] * promote));
    E = next; rooms = Math.max(rooms, roomsNeeded); gdp *= 1 + o.growth;
  }
  return {rows: out, pupilBalance};
}

/* 5. Teacher demand and supply, age-structured. Stock by single age 22..64; exit rates by age (quits young,
   retirement at `retire`). Requirement path given. New requirement = growth + replacement. Supply = trainees graduating
   after `lag` years (intake capacity can grow at most `capGrowth` a year toward the need) times the absorption rate. */
function teacherProjection(o) {
  const A0 = 22, A1 = o.retire, ages = A1 - A0, out = [];
  let stock = o.initialByAge.slice(0, ages);
  const pipe = new Array(o.lag).fill(o.intake0 * o.completion);
  let intake = o.intake0;
  for (let t = 0; t < o.years; t++) {
    const total = sum(stock), req = o.required(t);
    const exitsByAge = stock.map((s, i) => s * o.exitRate(A0 + i));
    const exits = sum(exitsByAge) + stock[ages - 1] * (1 - o.exitRate(A1 - 1));   // last age retires
    const graduates = pipe.shift();
    const hires = Math.min(graduates * o.absorption, Math.max(0, o.required(t + 1) - (total - exits)));
    const unemployedGrads = graduates * o.absorption - hires;
    // ageing
    const next = new Array(ages).fill(0);
    for (let i = 0; i < ages - 1; i++) next[i + 1] = stock[i] - exitsByAge[i];
    next[0] += hires * 0.6; next[1] += hires * 0.4;                                      // new teachers aged 22-23
    // next intake toward expected need `lag` years ahead, bounded by capacity growth
    const futureNeed = Math.max(0, o.required(t + o.lag) - o.required(t + o.lag - 1)) + exits;
    const wanted = futureNeed / Math.max(o.completion * o.absorption, 1e-9);
    intake = clamp(wanted, intake * (1 - o.capGrowth), intake * (1 + o.capGrowth));
    pipe.push(intake * o.completion);
    const balance = sum(next) - (total - exits + hires);
    out.push({t, year: o.startYear + t, required: req, stock: total, gap: req - total, exits, hires, graduates, unemployedGrads, balance,
      intake, attritionRate: exits / Math.max(total, 1e-9), over50: sum(stock.slice(50 - A0)) / Math.max(total, 1e-9)});
    stock = next;
  }
  return {rows: out, finalByAge: stock};
}

/* 6. Teacher deployment consistency (education sector analysis guidelines): across schools, regress teachers on
   pupils; R^2 measures how consistently teachers follow pupils, 1 - R^2 the share of allocation unrelated to enrolment.
   A reallocation moves a share k of each school's deviation from the proportional norm, keeping the total fixed. */
function deployment(o) {
  const r = rng(o.seed || 7), N = o.schools || 200, out = {pupils: [], teachers: []};
  for (let i = 0; i < N; i++) {
    const p = Math.round(Math.exp(Math.log(o.meanPupils || 260) + (o.spread || 0.6) * normal(r)));
    const ideal = p / o.ptr;
    // a share `randomness` of each school's staffing is unrelated to its enrolment (an average post, scaled by noise)
    const t = ideal * (1 - o.randomness) + o.randomness * ((o.meanPupils || 260) / o.ptr) * Math.exp(0.6 * normal(r));
    out.pupils.push(p); out.teachers.push(t);
  }
  const before = fitR2(out.pupils, out.teachers);
  const T = sum(out.teachers), P = sum(out.pupils);
  const norm = out.pupils.map(p => p * T / P);
  const after = out.teachers.map((t, i) => t + (o.reallocate || 0) * (norm[i] - t));
  const moved = 0.5 * sum(out.teachers.map((t, i) => Math.abs(after[i] - t)));
  return {pupils: out.pupils, teachers: out.teachers, after, r2Before: before.r2, r2After: fitR2(out.pupils, after).r2, slope: before.b, intercept: before.a,
    moved, totalBefore: T, totalAfter: sum(after),
    shareOverPTR: out.pupils.filter((p, i) => p / out.teachers[i] > o.ptr * 1.25).length / N,
    shareOverPTRAfter: out.pupils.filter((p, i) => p / after[i] > o.ptr * 1.25).length / N};
}
function fitR2(x, y) {
  const n = x.length, mx = sum(x) / n, my = sum(y) / n;
  let sxy = 0, sxx = 0, syy = 0;
  for (let i = 0; i < n; i++) { sxy += (x[i] - mx) * (y[i] - my); sxx += (x[i] - mx) ** 2; syy += (y[i] - my) ** 2; }
  const b = sxy / sxx, a = my - b * mx;
  return {a, b, r2: syy > 0 ? (sxy * sxy) / (sxx * syy) : 1};
}

/* 7. Distribution of public education resources across a cohort (education sector analysis, equity chapter).
   Each person's cumulative public spending = sum over levels attended of years x unit cost. Lorenz curve over people
   ordered by spending; Gini; share appropriated by the 10% most educated. */
function resourceDistribution(o) {
  // o.levels: [{name, years, unitCost}] in order; o.terminal: share whose highest level is each level (plus `none`)
  const groups = [{name: 'Never enrolled', share: o.none, spend: 0}];
  let cum = 0;
  o.levels.forEach((l, i) => { cum += l.years * l.unitCost; groups.push({name: l.name, share: o.terminal[i], spend: cum}); });
  const tot = sum(groups.map(g => g.share));
  groups.forEach(g => { g.share /= tot; });
  const total = sum(groups.map(g => g.share * g.spend));
  const lorenz = [[0, 0]]; let cp = 0, cs = 0;
  for (const g of groups) { cp += g.share; cs += g.share * g.spend / total; lorenz.push([cp, cs]); }
  let area = 0; for (let i = 1; i < lorenz.length; i++) area += (lorenz[i][0] - lorenz[i - 1][0]) * (lorenz[i][1] + lorenz[i - 1][1]) / 2;
  // share held by the top 10% (from the top of the distribution down)
  let need = 0.10, top = 0;
  for (let i = groups.length - 1; i >= 0 && need > 1e-12; i--) { const take = Math.min(need, groups[i].share); top += take * groups[i].spend / total; need -= take; }
  return {groups, lorenz, gini: 1 - 2 * area, top10: top, totalPerPerson: total};
}

/* 8. School mapping / micro-planning: villages on a plane; each child attends the nearest school. Greedy p-median adds
   one school at a time at the candidate site that most reduces total child-km (Teitz-Bart style). Never increases any
   child's distance. */
function schoolMap(o) {
  const r = rng(o.seed || 11), V = [];
  for (let i = 0; i < (o.villages || 60); i++) {
    const cl = i % 4, cx = [25, 70, 40, 80][cl], cy = [30, 25, 70, 75][cl];
    V.push({x: clamp(cx + 14 * normal(r), 2, 98), y: clamp(cy + 14 * normal(r), 2, 98), kids: Math.round(Math.exp(3.6 + 0.8 * normal(r)))});
  }
  const schools = (o.existing || [[50, 50]]).map(([x, y]) => ({x, y, built: false}));
  const dist = (a, b) => Math.hypot(a.x - b.x, a.y - b.y) * (o.kmPerUnit || 0.3);
  const assign = S => V.map(v => Math.min(...S.map(s => dist(v, s))));
  const stats = S => { const d = assign(S), kids = sum(V.map(v => v.kids));
    return {mean: sum(d.map((x, i) => x * V[i].kids)) / kids, beyond: sum(d.map((x, i) => x > o.maxKm ? V[i].kids : 0)) / kids, d}; };
  const history = [stats(schools)];
  for (let k = 0; k < (o.add || 0); k++) {
    let best = null, bestVal = Infinity;
    const cands = o.rule === 'largest' ? V.slice().sort((a, b) => b.kids - a.kids).filter(v => !schools.some(s => s.x === v.x && s.y === v.y)).slice(0, 1) : V;
    for (const c of cands) {
      const S = schools.concat([{x: c.x, y: c.y}]);
      const d = assign(S); const val = sum(d.map((x, i) => x * V[i].kids));
      if (val < bestVal) { bestVal = val; best = c; }
    }
    schools.push({x: best.x, y: best.y, built: true});
    history.push(stats(schools));
  }
  return {villages: V, schools, history};
}

/* 9. Learning-adjusted years of schooling (World Bank HCI): LAYS = EYS x HLO / 625. Learning poverty: share of
   children at the end-primary age who cannot read with comprehension, counting out-of-school children as not
   proficient: LP = OOS + (1 - OOS) x (1 - BMP). */
function learningAdjusted(o) {
  const lays = o.eys * o.hlo / 625;
  return {lays, lostYears: o.eys - lays, learningPoverty: o.oos + (1 - o.oos) * (1 - o.bmp)};
}

/* 10. Feasibility of a target on a logistic S-curve (Clemens 2004, The long walk to school): coverage x(t) follows
   logistic growth with speed beta. Given today's x0 and a speed, when is the target reached? What speed would the
   deadline need? */
function logisticTarget(o) {
  const L = o.ceiling || 1, x0 = clamp(o.x0, 1e-4, L - 1e-4), xt = clamp(o.target, 1e-4, L - 1e-4);
  const logit = x => Math.log(x / (L - x));
  const yearsNeeded = (logit(xt) - logit(x0)) / o.beta;
  const betaNeeded = (logit(xt) - logit(x0)) / Math.max(o.deadline - o.startYear, 1e-9);
  const path = []; for (let t = 0; t <= (o.horizon || 40); t++) path.push([o.startYear + t, L / (1 + Math.exp(-(logit(x0) + o.beta * t)))]);
  return {yearsNeeded, yearReached: o.startYear + yearsNeeded, betaNeeded, path};
}

/* 11. External efficiency: graduate output against graduate-job openings. Openings grow with output growth x the
   employment elasticity x the growth of the skilled share; unabsorbed graduates join a queue that clears at `clear`
   a year (to other work, migration, or leaving the labour force). */
function absorption(o) {
  const rows = []; let jobs = o.jobs0, queue = o.queue0 || 0, grads = o.grads0;
  for (let t = 0; t < o.years; t++) {
    const openings = jobs * o.replacement + (t ? jobs - rows[t - 1].jobs : 0);
    const hired = Math.min(openings, grads + queue);
    const unabsorbed = grads + queue - hired;
    rows.push({year: o.startYear + t, grads, jobs, openings, hired, queue, ratio: openings / grads});
    queue = unabsorbed * (1 - o.clear);
    jobs *= 1 + o.gdpGrowth * o.elasticity + o.skillShift;
    grads *= 1 + o.gradGrowth;
  }
  return rows;
}

/* 12. UIS indicator calculator: GER, NER, GIR, adjusted gender parity index (UIS: F/M if F <= M, else 2 - M/F),
   pupil-teacher ratio, percentage of trained teachers. */
function indicators(o) {
  const gpi = (f, m) => f <= m ? f / m : 2 - m / f;
  const gerF = o.enrolF / o.popF, gerM = o.enrolM / o.popM;
  return {ger: (o.enrolF + o.enrolM) / (o.popF + o.popM), gerF, gerM, ner: (o.ofAgeF + o.ofAgeM) / (o.popF + o.popM),
    gpiRaw: gerF / gerM, gpiAdj: gpi(gerF, gerM), gir: o.newEntrants / o.popEntry, ptr: (o.enrolF + o.enrolM) / o.teachers,
    trained: o.trained / o.teachers, pqtr: (o.enrolF + o.enrolM) / o.trained, overAge: 1 - (o.ofAgeF + o.ofAgeM) / (o.enrolF + o.enrolM)};
}

/* 13. School grant formula: allocate a budget across schools by per-pupil weight plus equity weights (poverty,
   remoteness) and a fixed base per school. Every unit of budget is allocated (identity). */
function grantFormula(o) {
  const r = rng(o.seed || 5), S = [];
  for (let i = 0; i < (o.schools || 120); i++) S.push({pupils: Math.round(Math.exp(5.3 + 0.7 * normal(r))), poverty: clamp(0.4 + 0.25 * normal(r), 0, 1), remote: r() < 0.3 ? 1 : 0});
  const base = o.baseShare * o.budget / S.length;
  const pts = S.map(s => s.pupils * (1 + o.wPoverty * s.poverty + o.wRemote * s.remote));
  const pool = o.budget * (1 - o.baseShare), P = sum(pts);
  S.forEach((s, i) => { s.grant = base + pool * pts[i] / P; s.perPupil = s.grant / s.pupils; });
  const sorted = S.slice().sort((a, b) => a.poverty - b.poverty), q = Math.floor(S.length / 5);
  const pp = arr => sum(arr.map(s => s.grant)) / sum(arr.map(s => s.pupils));
  return {schools: S, allocated: sum(S.map(s => s.grant)), poorestQuintilePerPupil: pp(sorted.slice(-q)), richestQuintilePerPupil: pp(sorted.slice(0, q)),
    smallSchoolPerPupil: pp(S.filter(s => s.pupils < 120)), largeSchoolPerPupil: pp(S.filter(s => s.pupils >= 400))};
}

const api = {flowRates, cohort, populationProjection, sectorSimulation, teacherProjection, deployment, fitR2, resourceDistribution,
  schoolMap, learningAdjusted, logisticTarget, absorption, indicators, grantFormula};
if (typeof module !== 'undefined') module.exports = api;
root.AtlasLab = api;
})(typeof window !== 'undefined' ? window : globalThis);
