(function (root) {
  "use strict";
  const C = typeof module === "object" && module.exports ? require("./model.js") : root.HKModel;
  const END = 2050;
  const CASES = [
    { key: "policy", label: "Published-policy reference", load: 0.72, speed: 1, protect: false, size: 1, force: false },
    { key: "retention", label: "Selective retention + smaller classes", load: 0.72, speed: 1, protect: true, size: 0.9, force: false },
    { key: "rapid", label: "Faster consolidation", load: 0.9, speed: 1.4, protect: false, size: 1.06, force: true },
  ];
  const DEFAULTS = { savedSites: 5, exitScale: 1, demandShift: 0, births: 31100, birthGrowth: 0 };
  const sum = C.sum;
  const range = (start, end) => Array.from({ length: end - start + 1 }, (_, i) => start + i);
  const stages = C.NAMES;
  const allYears = range(C.BASE + 1, END);
  const weights = [[1], [1.6, 1.6, 1.6, 1.6, 1.6, 1.6], [1.8, 1.8, 1.8, 2.1, 2.1, 2.1, 2.1]];
  const weightsFor = (classes, stage) => sum(classes.map((n, g) => n * weights[stage][g]));

  function staffTarget(base, stage, pupils, classes, sites) {
    const enrollment = sum(pupils);
    const populationRatio = enrollment / sum(base.pupils);
    const siteRatio = sites / base.sites;
    if (stage === 0) return Math.max(1, Math.round(base.staff * populationRatio ** 0.65 * siteRatio ** 0.12));
    const regular = weightsFor(base.classes, stage);
    // Regular ratios come from EDB. Additional staff is calibrated to the
    // all-sector starting headcount and split between enrollment and sites.
    const residual = base.staff - regular;
    const other = residual * (0.65 * populationRatio + 0.35 * siteRatio);
    return Math.max(1, Math.round(weightsFor(classes, stage) + other));
  }

  function workforce(previous, target, rate, force) {
    const departures = Math.round(previous * Math.min(0.95, rate));
    const survivors = previous - departures;
    const involuntary = force ? Math.max(0, survivors - target) : 0;
    const hires = Math.max(0, target - survivors);
    return { departures, hires, involuntary, staff: survivors + hires - involuntary };
  }

  function districtApprovals(profiles, districts) {
    return districts.map(name => {
      const rows = profiles.schools.filter(s => s.district === name);
      return {
        name, schools: rows.length, previous: sum(rows.map(s => s.previousP1 || 0)),
        approved: sum(rows.map(s => s.classes[0] || 0)),
        zero: rows.filter(s => s.previousP1 > 0 && s.classes[0] === 0).length,
      };
    });
  }

  function run(data, approvals, plans, input = {}) {
    const settings = { ...DEFAULTS, ...input };
    const base = data.history.at(-1);
    const cohort = C.simulate(data, C.BASE, END, { official: true, settings: { demandShift: settings.demandShift, births: settings.births, birthGrowth: settings.birthGrowth } });
    const baseline = cohort.records;
    const district = C.districtPaths(data, cohort);
    const rawRapid = C.simulate(data, C.BASE, END, { official: true, settings: {
      demandShift: settings.demandShift, births: settings.births, birthGrowth: settings.birthGrowth, minimumLoad: CASES[2].load, closureScale: CASES[2].speed, capacityStart: 2027,
    } }).records;

    // Carry the observed change among matched public primary profiles into
    // the all-sector forecast. The residual outside the matched sample is held
    // fixed in 2026/27; each grade-level correction then follows that cohort.
    const correction = base[1].classes.map((n, g) =>
      n + approvals.approved[g] - approvals.previous[g] - baseline[2026][1].classes[g]);
    const confirmed = year => plans.schools.filter(x => x[4] != null && x[4] <= year).length;

    const records = {};
    for (const policy of CASES) {
      const rows = {};
      rows[C.BASE] = base.map((b, stage) => ({
        year: C.BASE, stage, enrollment: sum(b.pupils), entry: b.pupils[0], sites: b.sites, staff: b.staff,
        classes: b.classTotal, classSize: b.classTotal ? sum(b.pupils) / b.classTotal : null,
        ratio: sum(b.pupils) / b.staff, planned: 0,
      }));
      for (const year of allYears) {
        rows[year] = stages.map((_, s) => {
          const b = base[s];
          const p = rows[year - 1][s];
          const d = baseline[year][s];
          const raw = policy.key === "rapid" && year >= 2027 ? rawRapid[year][s] : d;
          const planned = s === 1 ? confirmed(year) : 0;
          const knownCap = b.sites - planned;
          // The dated subset is already part of net contraction. Apply it as a
          // ceiling on operations so a modeled reduction cannot count it twice.
          let sites = planned ? Math.min(raw.sites, knownCap) : raw.sites;
          if (policy.protect && year >= 2027) {
            sites += Math.min(settings.savedSites, Math.max(0, knownCap - sites));
          }

          let classes = raw.classes?.map((n, g) => {
            const previousGrade = g - (year - 2026);
            const offset = s === 1 && previousGrade >= 0 ? correction[previousGrade] : 0;
            return Math.max(1, n + offset);
          });
          if (classes && year >= 2027 && policy.size !== 1) {
            const total = sum(classes);
            if (policy.size < 1) {
              const roomProxy = Math.max(total, Math.round(sum(b.classes) / b.sites * sites * 1.05));
              const extra = Math.min(roomProxy - total, Math.round(total / policy.size) - total);
              const allocation = C.allocate(extra, classes.map((n, g) => s === 2 && g === 6 ? 0 : n));
              classes = classes.map((n, g) => n + allocation[g]);
            } else {
              classes = classes.map((n, g) => s === 2 && g === 6 ? n :
                Math.max(sites * (s === 2 ? 2 : 1), Math.round(n / policy.size)));
            }
          }

          const count = sum(d.pupils);
          let required = staffTarget(b, s, d.pupils, classes, sites);
          if (s === 0 && policy.protect && year >= 2027) required = Math.max(required, Math.round(b.staff * 0.9));
          const flow = workforce(p.staff, required, b.exitRate * settings.exitScale, policy.force && year >= 2027);
          const classTotal = classes ? sum(classes) : null;
          return { year, stage: s, enrollment: count, entry: d.pupils[0], sites, required, ...flow,
            cutsFrom2025: b.staff - flow.staff, netTeacherChange: flow.staff - p.staff,
            sitesFrom2025: sites - b.sites, planned, classes: classTotal,
            classSize: classTotal ? count / classTotal : null, ratio: count / flow.staff };
        });
      }
      records[policy.key] = rows;
    }
    return { settings, records, cohort, district };
  }

  function testHistory(data) {
    const historical = C.backtest(data);
    const workforceRows = [];
    for (const origin of range(2020, 2024)) {
      const year = origin + 1;
      const free = C.simulate(data, origin, year).records[year];
      const base = data.history[origin - C.START];
      const actual = data.history[year - C.START];
      for (const [s, f] of free.entries()) {
        const required = staffTarget(base[s], s, f.pupils, f.classes, f.sites);
        const predicted = workforce(base[s].staff, required, base[s].exitRate, false).staff;
        const ratio = Math.round(sum(f.pupils) * base[s].staff / sum(base[s].pupils));
        workforceRows.push({ origin, year, stage: s, metric: "network_staff", actual: actual[s].staff, model: predicted, naive: ratio });
      }
    }
    return { historical, workforceRows };
  }

  const api = { END, CASES, DEFAULTS, allYears, stages, run, districtApprovals, testHistory, staffTarget, workforce };
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.HKNetwork = api;
})(globalThis);
