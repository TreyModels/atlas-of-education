(function (root) {
  "use strict";
  const BASE = 2025;
  const END = 2050;
  const years = Array.from({length: END - BASE + 1}, (_, i) => BASE + i);
  const sum = list => list.reduce((total, value) => total + value, 0);
  const defaults = {policy:"reference", births:0, exits:null, firstShare:null, override:null,
    lag:null, qualify:0.85, seek:0.8, force:false, cost:null};
  const policies = {
    reference: {staff:1, sites:0.45, hk:"policy", gz:"reference"},
    retain: {staff:1, sites:0.45, floor:true, hk:"retention", gz:"retain"},
    rapid: {staff:1.2, sites:0.85, hk:"rapid", gz:"rapid"},
    enrollment: {staff:1, sites:0.45, hk:"policy", gz:"reference"}
  };

  function ageCount(data, system, stage, year, birthChange = 0) {
    const [first, last] = stage.ages;
    return Math.round(sum(data.population[system][year].slice(first, last + 1).map((n, i) => {
      const birthYear = year - first - i;
      return n * (birthYear >= 2027 ? 1 + birthChange : 1);
    })));
  }

  function nationalRows(data, system, stage, config, policy) {
    const base = stage.history?.[BASE];
    const baseAge = ageCount(data, system, stage, BASE);
    return years.map(year => {
      const age = ageCount(data, system, stage, year, config.births);
      const ratio = age / baseAge;
      const scale = (value, elasticity) => value == null ? null :
        Math.max(policy.floor ? value : 1, Math.round(value * ratio ** elasticity));
      return [{year, age, enrollment:scale(base?.[1], 1), sites:scale(base?.[0], policy.sites),
        required:scale(base?.[2], policy.staff), exitRate:config.exits ?? 0.04, classSize:null}];
    });
  }

  function cityRows(data, system, stage, config, policy) {
    if (system.family === "hk") {
      const city = data.cities;
      const path = root.HKNetwork.run(city.hk, city.approvals, city.plans,
        {births:Math.round(31100 * (1 + config.births))}).records[policy.hk];
      return years.map(year => stage.city.map(s => {
        const row = path[year][s];
        return {year, age:null, enrollment:row.enrollment, sites:row.sites,
          required:row.required ?? row.staff, classSize:row.classSize,
          exitRate:(s === 2 && stage.city.length > 1 ? config.secondaryExits : config.exits) ?? city.hk.history.at(-1)[s].exitRate};
      }));
    }
    const path = root.Guangzhou.simulate(data.cities.gz, {longKgGrowth:config.births})[policy.gz];
    return years.map(year => stage.city.map(s => {
      const row = path[year][s];
      return {year, age:null, enrollment:row.enrollment, sites:row.sites, required:row.staff,
        classSize:null, exitRate:config.exits ?? 0.04};
    }));
  }

  function workforce(previous, required, exitRate, force, entryFloor = 0) {
    const departures = Math.round(previous * exitRate);
    const survivors = previous - departures;
    const target = entryFloor ? Math.max(required, survivors + entryFloor) : required;
    const excess = Math.max(0, survivors - target);
    const openings = Math.max(0, target - survivors);
    const layoffs = force ? excess : 0;
    return {departures, excess, openings, layoffs, target, employed:survivors + openings - layoffs};
  }

  function intake(stage, config, year) {
    const training = stage.training;
    if (config.override != null && year >= 2027) return config.override;
    if (training) return training.years[year] ?? (year >= BASE ? training.future : training.before);
    return config.override;
  }

  function plannedFloor(stage, policy, year) {
    if (!stage.hiring || policy !== "reference") return 0;
    const midpoint = range => Math.round(sum(range) / range.length);
    if (stage.hiring[year]) return midpoint(stage.hiring[year]);
    return year > 2030 ? Math.round(midpoint(stage.hiring[2030]) * Math.max(0, (2034 - year) / 4)) : 0;
  }

  function simulate(data, name, key, input = {}) {
    const system = data.systems[name];
    const stage = system.stages[key];
    const config = {...defaults, ...input};
    const policy = policies[config.policy];
    const demand = system.family ? cityRows(data, system, stage, config, policy) : nationalRows(data, name, stage, config, policy);
    const base = demand[0].map(row => row.required);
    let employed = [...base];
    const lag = config.lag ?? stage.lag ?? 4;
    const firstShare = config.firstShare ?? stage.firstShare ?? 0.5;
    const aggregate = values => values.some(value => value == null) ? null : sum(values);
    return demand.map((parts, index) => {
      const year = years[index];
      const floor = plannedFloor(stage, config.policy, year);
      const flows = parts.map((row, i) => !index || row.required == null ? null :
        workforce(employed[i], row.required, row.exitRate, config.force, floor));
      employed = flows.map((flow, i) => flow?.employed ?? employed[i]);
      const row = {year};
      for (const field of ["age","enrollment","sites","required"]) row[field] = aggregate(parts.map(part => part[field]));
      for (const field of ["departures","excess","openings","layoffs"]) row[field] = aggregate(flows.map(flow => flow?.[field]));
      row.demographicTarget = stage.hiring ? row.required : null;
      row.required = index && row.required != null ? aggregate(flows.map(flow => flow?.target)) : row.required;
      row.planLow = stage.hiring?.[year]?.[0] ?? null;
      row.planHigh = stage.hiring?.[year]?.[1] ?? null;
      row.planFloor = floor || null;
      row.historicalEntrants = stage.historicalEntrants?.[year] ?? null;
      row.historicalRecruitment = stage.historicalRecruitment?.[year] ?? null;
      row.employed = aggregate(employed);
      row.classSize = parts.length === 1 ? parts[0].classSize : null;
      row.pupilTeacherRatio = row.employed ? row.enrollment / row.employed : null;
      row.starts = intake(stage, config, year);
      row.feederIntake = index ? intake(stage, config, year - lag) : null;
      row.qualified = row.feederIntake == null ? null : Math.round(row.feederIntake * config.qualify);
      row.applicants = row.qualified == null ? null : Math.round(row.qualified * config.seek);
      row.firstOpenings = row.openings == null ? null : Math.max(floor, Math.round(row.openings * firstShare));
      row.unmatched = row.applicants == null || row.firstOpenings == null ? null :
        Math.max(0, row.applicants - row.firstOpenings);
      row.payroll = row.employed == null || config.cost == null ? null : row.employed * config.cost;
      return row;
    });
  }

  function historicalCheck(data, system, key) {
    const stage = data.systems[system].stages[key];
    const observed = stage.history ?? {};
    return Object.keys(observed).map(Number).filter(y => observed[y - 1]).map(year => {
      const actual = observed[year][1], flat = observed[year - 1][1];
      const expected = Math.round(flat * ageCount(data, system, stage, year) / ageCount(data, system, stage, year - 1));
      return {year, actual, expected, flat};
    });
  }

  const api = {BASE, END, years, simulate, workforce, historicalCheck, ageCount};
  if (typeof module === "object" && module.exports) module.exports = api;
  else root.Pipeline = api;
})(globalThis);
