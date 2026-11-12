/* Shared by the offline browser and the reproducible Node checks. */
(function (root) {
  "use strict";

  const START = 2015;
  const BASE = 2025;
  const END = 2050;
  const NAMES = ["Kindergarten", "Primary", "Secondary"];
  const GRADES = [
    ["K1", "K2", "K3"],
    ["P1", "P2", "P3", "P4", "P5", "P6"],
    ["S1", "S2", "S3", "S4", "S5", "S6", "S7"],
  ];
  const ENTRY_AGE = [3, 6, 12];
  const POLICIES = [
    { name: "Consolidate", campuses: 0, staffing: 0 },
    { name: "Keep campuses", campuses: 1, staffing: 0 },
    { name: "Keep teachers", campuses: 0, staffing: 1 },
    { name: "Keep both", campuses: 1, staffing: 1 },
  ];
  const DEFAULTS = {
    births: 31100,
    birthGrowth: 0,
    demandShift: 0,
    exitScale: 1,
    retention: 1,
    closureScale: 1,
    minimumLoad: 0.72,
    payroll: [360000, 740000, 850000],
    campusCost: [1000000, 4500000, 5500000],
    unitBenchmark: [54488, 86333, 99041],
    transitionCost: [300000, 1000000, 1500000],
    travelCost: 0,
    readingEffect: 0.05,
    disruptionEffect: 0.05,
  };

  const sum = xs => xs.reduce((a, b) => a + b, 0);
  const mean = xs => sum(xs) / xs.length;
  const clamp = (value, lo, hi) => Math.max(lo, Math.min(hi, value));
  const sequence = (first, last) => Array.from({ length: Math.max(0, last - first + 1) }, (_, i) => first + i);
  const median = xs => {
    const sorted = [...xs].sort((a, b) => a - b);
    return (sorted[Math.floor((sorted.length - 1) / 2)] + sorted[Math.ceil((sorted.length - 1) / 2)]) / 2;
  };

  function allocate(total, weights) {
    if (total === 0) return weights.map(() => 0);
    const weightTotal = sum(weights);
    if (weightTotal <= 0) throw new RangeError("Positive allocation requires a positive weight");
    const scale = total / weightTotal;
    const scaled = weights.map(w => w * scale);
    const result = scaled.map(Math.floor);
    const ranking = scaled.map((x, i) => [i, x - result[i]]).sort((a, b) => b[1] - a[1]);
    for (const [i] of ranking.slice(0, total - sum(result))) result[i]++;
    return result;
  }

  function fitSlope(samples, prior, penalty, low, high) {
    const xy = sum(samples.map(([x, y]) => x * y));
    const xx = sum(samples.map(([x]) => x * x));
    return clamp((xy + prior * penalty) / (xx + penalty), low, high);
  }

  function observed(data, year, stage) {
    return data.history[year - START][stage];
  }

  function enrollment(data, year, stage) {
    return sum(observed(data, year, stage).pupils);
  }

  function fit(data, origin) {
    const years = sequence(Math.max(START, origin - 3), origin);
    const changes = sequence(Math.max(START + 1, origin - 5), origin);
    return NAMES.map((_, s) => {
      const latest = observed(data, origin, s);
      const age = ENTRY_AGE[s];
      const conversion = median(years.map(y => observed(data, y, s).pupils[0] / data.population[y][age]));
      const aging = median(changes.slice(-4).map(y => data.population[y][age] / data.population[y - 1][age - 1]));
      const progression = latest.pupils.map((_, g) => {
        if (!g) return null;
        // S7 is a small separate, largely non-local provision. Keep its recent level.
        if (s === 2 && g === 6) return null;
        return median(changes.slice(-4).map(y => observed(data, y, s).pupils[g] / observed(data, y - 1, s).pupils[g - 1]));
      });
      const feeder = s === 2 ? median(changes.slice(-4).map(y =>
        observed(data, y, s).pupils[0] / observed(data, y - 1, 1).pupils[5])) : null;
      const anchor = enrollment(data, origin, s);
      const siteResponse = fitSlope(changes.map(y => [
        Math.log(enrollment(data, y, s) / enrollment(data, y - 1, s)),
        Math.log(observed(data, y, s).sites / observed(data, y - 1, s).sites),
      ]), [0.25, 0.04, 0.04][s], 0.006, 0, 1);
      const classResponse = latest.classes ? latest.classes.map((_, g) => fitSlope(changes.map(y => {
        const current = observed(data, y, s);
        const prior = observed(data, y - 1, s);
        return [Math.log(current.pupils[g] / prior.pupils[g]), Math.log(current.classes[g] / prior.classes[g])];
      }), 0.55, 0.008, 0.05, 1)) : null;
      const workforce = origin >= 2020 ? latest.staff : null;
      const staffResponse = workforce === null ? null : fitSlope(changes.filter(y => y > 2020).map(y => {
        const current = observed(data, y, s);
        const prior = observed(data, y - 1, s);
        const driver = s === 0 ? enrollment(data, y, s) : sum(current.classes);
        const previousDriver = s === 0 ? enrollment(data, y - 1, s) : sum(prior.classes);
        return [Math.log(driver / previousDriver), Math.log(current.staff / prior.staff)];
      }), [0.7, 0.75, 0.6][s], 0.004, 0, 1.2);
      return {
        conversion, aging, progression, feeder, anchor, siteResponse, classResponse, staffResponse,
        staff: workforce, sites: latest.sites, classes: latest.classes, pupils: latest.pupils,
        exitRate: latest.exitRate, classTotal: latest.classTotal, s7: latest.pupils.at(-1),
      };
    });
  }

  function populationPaths(data, origin, end, calibration, settings, official) {
    const paths = {};
    const ageThree = {};
    const lastEDB = official ? Math.max(...Object.keys(data.projected).map(Number)) : null;
    const ages = data.population[origin];
    const birthLevel = official ? settings.births
      : mean(sequence(origin - 2, origin - 1).map(y => data.births[y]));
    for (const year of sequence(origin + 1, end)) {
      const horizon = year - origin;
      const sourceYear = official ? 2026 : origin;
      ageThree[year] = (year - sourceYear <= 3
        ? data.population[sourceYear][3 - (year - sourceYear)]
        : birthLevel * (1 + settings.birthGrowth) ** (year - sourceYear - 4));
      if (official && year === 2026) {
        paths[year] = ENTRY_AGE.map(age => data.population[2026][age]);
      } else if (official) {
        const edb = data.projected[year];
        if (edb) {
          paths[year] = [ageThree[year], ...edb];
        } else {
          // Blend off the last official age-six input so a change in source
          // does not itself introduce a sudden enrollment drop.
          const excessAtAnchor = data.projected[lastEDB][0] - ageThree[lastEDB - 3];
          const remainingBridge = Math.max(0, 1 - (year - lastEDB) / 4);
          const primary = ageThree[year - 3] + remainingBridge * excessAtAnchor;
          const secondaryRatio = data.projected[lastEDB][1] / paths[lastEDB - 6][1];
          const secondary = paths[year - 6][1] * secondaryRatio;
          paths[year] = [ageThree[year], primary, secondary];
        }
      } else {
        paths[year] = ENTRY_AGE.map((age, s) => {
          const startSize = horizon <= age ? ages[age - horizon] : birthLevel;
          return startSize * calibration[s].aging;
        });
      }
    }
    return paths;
  }

  function nextPupils(stage, previous, fitted, agePopulation, shift, primarySix) {
    const demographic = agePopulation * fitted.conversion * (1 + shift);
    const entry = stage === 2 ? 0.5 * (demographic + primarySix * fitted.feeder) : demographic;
    return previous.pupils.map((_, g) => {
      if (!g) return Math.round(entry);
      if (stage === 2 && g === 6) return fitted.s7;
      return Math.round(previous.pupils[g - 1] * fitted.progression[g]);
    });
  }

  function costFor(stage, row, fitted, settings) {
    const payroll = settings.payroll[stage];
    const siteCost = settings.campusCost[stage];
    const perPupil = Math.max(0, settings.unitBenchmark[stage] - (fitted.staff * payroll + fitted.sites * siteCost) / fitted.anchor);
    const exposed = row.siteReductions * fitted.anchor / fitted.sites;
    return {
      payroll: row.staff * payroll,
      premises: row.sites * siteCost,
      variable: sum(row.pupils) * perPupil,
      transition: row.siteReductions * settings.transitionCost[stage],
      travel: Math.max(0, fitted.sites - row.sites) * (fitted.anchor / fitted.sites) * settings.travelCost,
      exposed,
    };
  }

  function structure(stage, year, pupils, previous, fitted, trend, settings, policy, official) {
    const count = sum(pupils);
    // Retain fractional carry so gradual adjustment can still yield whole site counts.
    const contraction = trend < 0;
    const useOriginalCapacity = settings.capacityStart != null && year < settings.capacityStart;
    const closureScale = useOriginalCapacity ? 1 : settings.closureScale;
    const siteDelta = trend * fitted.siteResponse * (contraction ? closureScale : 1);
    let projectedSites = clamp(previous.siteStock * Math.exp(siteDelta), 1, 10000);
    if (official) {
      // Stress beyond the historical range. A site count is the unit here,
      // so closure pressure works on average load rather than named campuses.
      const typicalSize = fitted.anchor / fitted.sites;
      const averageEnrollment = 0.7 * count + 0.3 * sum(previous.pupils);
      const load = useOriginalCapacity ? DEFAULTS.minimumLoad : settings.minimumLoad;
      const supportedSites = averageEnrollment / (typicalSize * load);
      const phasedReduction = clamp((previous.siteStock - supportedSites) / [2, 5, 5][stage], 0, previous.siteStock * 0.05);
      projectedSites = Math.max(1, Math.min(projectedSites, previous.siteStock - phasedReduction));
    }
    const siteStock = policy.campuses ? Math.max(fitted.sites, projectedSites) : projectedSites;
    const sites = Math.round(siteStock);
    const siteReductions = Math.max(0, previous.sites - sites);
    const row = { pupils, sites, siteStock, siteReductions };

    if (fitted.classes) {
      const minimum = stage === 2 ? 2 : 1;
      // Non-local S7 provision is kept at its observed level.
      const target = pupils.map((n, g) => {
        if (stage === 2 && g === 6) return fitted.classes[g];
        const ratio = n / fitted.pupils[g];
        let target = fitted.classes[g] * ratio ** fitted.classResponse[g];
        if (official && stage === 2) {
          // 29 vs 27 applies by entry cohort. Weight by public-sector share to
          // approximate the all-sector total. It is an approval basis, not a cap.
          if (year - g >= 2026) target *= (1 - 0.76) + 0.76 * (27 / 29);
        }
        return Math.max(Math.ceil(sites * minimum), Math.round(target));
      });
      row.baseClasses = target;
      row.classes = [...target];
      row.classTotal = sum(target);
    }

    if (fitted.staff !== null) {
      const driver = row.classTotal ?? count;
      const anchorDriver = fitted.classes ? sum(fitted.classes) : fitted.anchor;
      const required = Math.max(1, Math.round(fitted.staff * (driver / anchorDriver) ** fitted.staffResponse));
      const exits = Math.round(previous.staff * clamp(fitted.exitRate * settings.exitScale, 0, 0.8));
      const survivors = previous.staff - exits;
      const target = Math.max(required, policy.staffing ? Math.round(fitted.staff * settings.retention) : 0);
      const hires = Math.max(0, target - survivors);
      const staff = survivors + hires;
      Object.assign(row, {
        required, staff, exits, hires, surplus: staff - required,
        replacementHires: Math.min(exits, hires),
      });

      if (fitted.classes && policy.staffing && row.surplus > 0) {
        // Allocate extra teacher capacity to additional whole classes, holding
        // historical teachers per class fixed on this margin. Cap at one per pupil.
        const extraTeachers = Math.floor(row.surplus / (fitted.staff / anchorDriver));
        const extraRooms = Math.max(0, Math.round(anchorDriver * sites / fitted.sites) - row.classTotal);
        const extra = Math.min(extraTeachers, extraRooms);
        const eligible = row.classes.map((c, g) => stage === 2 && g === 6 ? 0 : Math.max(0, pupils[g] - c));
        const additions = allocate(Math.min(extra, sum(eligible)), eligible);
        row.classes = row.classes.map((c, g) => c + (additions[g] || 0));
        row.classTotal = sum(row.classes);
      }
      if (official) {
        row.cost = costFor(stage, row, fitted, settings);
        row.totalCost = sum([row.cost.payroll, row.cost.premises, row.cost.variable, row.cost.transition, row.cost.travel]);
      }
    }
    return row;
  }

  function simulate(data, origin, end, options = {}) {
    const { official = false, policy = POLICIES[0], actualEnrollment = false } = options;
    const settings = { ...DEFAULTS, ...options.settings };
    const calibration = fit(data, origin);
    const paths = populationPaths(data, origin, end, calibration, settings, official);
    const records = {};
    records[origin] = NAMES.map((_, s) => {
      const actual = observed(data, origin, s);
      return { ...actual, siteStock: actual.sites, siteReductions: 0 };
    });

    for (const year of sequence(origin + 1, end)) {
      records[year] = NAMES.map((_, s) => {
        const previous = records[year - 1][s];
        const a = calibration[s];
        const shift = official ? settings.demandShift * Math.min(1, (year - origin) / 5) : 0;
        const pupils = actualEnrollment
          ? observed(data, year, s).pupils
          : nextPupils(s, previous, a, paths[year][s], shift, records[year - 1][1].pupils[5]);
        const growth = Math.log(sum(pupils) / sum(previous.pupils));
        const prior = records[year - 2]?.[s]?.pupils ?? observed(data, origin - 1, s).pupils;
        // Blend this year's total change with the prior year's change to model delayed site adjustment.
        const trend = 0.7 * growth + 0.3 * Math.log(sum(previous.pupils) / sum(prior));
        return structure(s, year, pupils, previous, a, trend, settings, policy, official);
      });
    }
    return { records, paths, calibration, settings, origin, end };
  }

  function districtPaths(data, run) {
    const result = { [BASE]: data.districtObserved[BASE] };
    const base = result[BASE];
    for (const year of sequence(BASE + 1, run.end)) {
      result[year] = NAMES.map((_, s) => {
        const last = result[year - 1][s];
        const ref = s > 0 ? data.districtProjected[s - 1] : null;
        const weights = ref ? ref.map((district, d) => {
          const i = clamp(year - 2027, 0, 4);
          const fraction = year === 2026 ? 0 : 1;
          const baseEnrollment = base[s][d][0];
          const meanGrowth = sum(ref.map(x => x[i])) / sum(ref.map(x => x[0]));
          const relative = (district[i] / district[0]) / meanGrowth;
          return baseEnrollment * (1 + fraction * (relative - 1));
        }) : base[s].map(district => district[0]);
        const columns = run.records[year][s].pupils.map((n, g) => {
          if (!g) return allocate(n, weights);
          if (s === 2 && g === 6) return allocate(n, base[s].map(d => d[g]));
          // Keep the observed geographic differences in grade progression, with modest shrinkage.
          return allocate(n, last.map((d, i) => d[g - 1] * (0.7 + 0.3 * base[s][i][g] / base[s][i][g - 1])));
        });
        return base[s].map((_, d) => columns.map(column => column[d]));
      });
    }
    return result;
  }

  function historicalDistrictTest(data, rows) {
    const outcomes = [];
    for (const year of sequence(2021, BASE)) {
      const prev = data.districtObserved[year - 1];
      const actual = data.districtObserved[year];
      for (const s of [0, 1, 2]) {
        const forecast = rows.find(row => row.year === year && row.stage === s && row.metric === "entry").model;
        const estimates = allocate(forecast, prev[s].map(d => d[0]));
        outcomes.push(...actual[s].map((d, i) => ({
          year, stage: s, district: data.districts[i], actual: d[0], model: estimates[i], naive: prev[s][i][0],
        })));
      }
    }
    return outcomes;
  }

  function metrics(rows) {
    const n = rows.length;
    const actual = sum(rows.map(r => Math.abs(r.actual)));
    const mae = key => n ? sum(rows.map(r => Math.abs(r[key] - r.actual))) / n : null;
    const wape = key => actual ? mae(key) * n / actual : null;
    return { n, mae: mae("model"), naiveMae: mae("naive"), conditionalMae: mae("conditional"),
      wape: wape("model"), naiveWape: wape("naive"), conditionalWape: wape("conditional") };
  }

  function backtest(data, rolling = true) {
    const rows = [];
    const origins = rolling ? sequence(2019, 2024) : [2019];
    for (const origin of origins) {
      const end = rolling ? origin + 1 : BASE;
      const free = simulate(data, origin, end);
      const conditional = simulate(data, origin, end, { actualEnrollment: true });
      for (const year of sequence(origin + 1, end)) {
        NAMES.forEach((_, s) => {
          const model = free.records[year][s];
          const actual = observed(data, year, s);
          const known = observed(data, origin, s);
          const withActual = conditional.records[year][s];
          const prior = observed(data, year - 1, s);
          const add = (metric, a, m, n, c = m) => rows.push({ origin, year, stage: s, metric, actual: a, model: m, naive: n, conditional: c });
          add("entry", actual.pupils[0], model.pupils[0], known.pupils[0]);
          add("pupils", sum(actual.pupils), sum(model.pupils), sum(known.pupils));
          add("sites", actual.sites, model.sites, known.sites, withActual.sites);
          if (rolling) add("siteChange", actual.sites - prior.sites, model.sites - prior.sites, 0, withActual.sites - prior.sites);
          if (actual.classTotal) add("classes", actual.classTotal, model.classTotal, known.classTotal, withActual.classTotal);
          if (model.staff !== undefined) {
            const ratioNaive = Math.round(sum(model.pupils) * known.staff / sum(known.pupils));
            add("staff", actual.staff, model.staff, ratioNaive, withActual.staff);
            // Estimated gross entrants derived from two stock observations and the
            // EDB exit rate. EDB separately publishes first-time entrants on a narrower scope.
            const implied = Math.max(0, actual.staff - prior.staff + Math.round(prior.staff * actual.exitRate));
            const fixedStockReplacement = Math.round(known.staff * known.exitRate);
            add("hires", implied, model.hires, fixedStockReplacement, withActual.hires);
          }
        });
      }
    }
    return rows;
  }

  function learning(stage, row, baseline, settings) {
    if (stage === 0) return null;
    const relativeLosses = baseline.cost.exposed - row.cost.exposed;
    const transition = settings.disruptionEffect * relativeLosses / sum(row.pupils);
    const reduction = sum(row.pupils) * (1 / baseline.classTotal - 1 / row.classTotal);
    const classEffect = clamp(reduction / 10, -2, 2) * settings.readingEffect;
    return { low: Math.min(0, classEffect, transition, classEffect + transition),
      high: Math.max(0, classEffect, transition, classEffect + transition), reduction };
  }

  const api = { START, BASE, END, NAMES, GRADES, POLICIES, DEFAULTS, sum, metrics, backtest, simulate, districtPaths, historicalDistrictTest, learning, allocate };
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.HKModel = api;
})(globalThis);
