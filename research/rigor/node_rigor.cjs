/* Rigor families on the shipped browser engines. Input/output: one JSON object (see research/rigor/adapters_rigor.py).

camchild_validation: an external check of the `cash` lever against a published Cambodian result.

  Filmer & Schady (2011, J. Dev. Econ. 96(1):150-157) evaluate the CESSP scholarship by regression discontinuity:
  poor children finishing Grade 6 received US$45 or US$60 a year conditional on enrolment and attendance in lower
  secondary. Their headline: attendance and enrolment rose by roughly 25 percentage points, and the larger award had
  no detectable additional effect. VERIFY both numbers and their intervals against the paper's tables before treating
  the check as pass/fail (research/rigor/protocols_rigor.json records them as "to verify").

  The engine's `cash` lever pays households in the bottom two quintiles per enrolled child, in units of one adult
  informal annual wage. A US$ award becomes cash = USD / W, where W (an adult informal annual wage in US$ at the time
  of the programme) is unsourced here and drawn from a declared range. The engine has one child per household, so a
  per-child award is a per-household award.

  Outcome: attendance (school, or school and work) among bottom-two-quintile children aged 12-13 in the first simulated
  year, cash arm minus no-cash arm with common random numbers. The first year avoids re-entry dynamics. Paying all ages
  (the lever cannot target Grade 7) changes child wages slightly through the market-clearing loop; that attenuation is
  reported as a limitation, not corrected.

  Era matching: the engine is calibrated to 2024; the CESSP cohort (2005-08) had much lower baseline attendance, and a
  logit response is largest near 50%. With targetBaseline set, an additive shift to vLow in both regions moves the
  baseline attendance of the eligible group to that value before the award is applied (bisection on the same seeds).
*/
'use strict';
const fs = require('node:fs'), path = require('node:path'), vm = require('node:vm');
const root = path.resolve(__dirname, '..', '..');
const load = name => { const ctx = vm.createContext({}); vm.runInContext(fs.readFileSync(path.join(root, 'public/engines', name), 'utf8'), ctx); return ctx; };
const seeded = seed => { let s = seed >>> 0; return () => ((s = (Math.imul(s, 1664525) + 1013904223) >>> 0) + .5) / 2 ** 32; };
const QCUT = [-.8416, -.2533, .2533, .8416];

function eligibleAttendance(res) {
  const row = res.rows[0];
  let n = 0, a = 0;
  res.H.forEach((h, i) => {
    const q = QCUT.filter(c => h.z > c).length, age = row.age[i];
    if (q <= 1 && (age === 12 || age === 13)) { n++; const c = row.choice[i]; if (c === 'school' || c === 'both') a++; }
  });
  return {n, attend: n ? a / n : NaN};
}

function camchild_validation(t) {
  const M = load('camchild.js').CamChild, s = t.settings, r = seeded(t.parameter_seed), u = (a, b) => a + (b - a) * r();
  const W = u(s.wageRangeUSD[0], s.wageRangeUSD[1]);
  const over = {};
  for (const reg of ['pp', 'rural']) {
    const b = M.REGIONS[reg];
    over[reg] = {yMedian: b.yMedian * u(.75, 1.25), debt: b.debt * u(.5, 1.5)};
  }
  const base = {N: s.n, years: 1, seed: t.seed, randomMode: 'indexed', wealthDefinition: 'within_region_rank'};
  const withShift = d => { const o = {}; for (const reg of ['pp', 'rural']) o[reg] = {...over[reg], vLow: M.REGIONS[reg].vLow + d}; return o; };
  let shift = 0;
  if (s.targetBaseline !== null) {
    let lo = -8, hi = 4;
    for (let it = 0; it < 22; it++) {
      const mid = (lo + hi) / 2;
      const att = eligibleAttendance(M.simulate({...base, over: withShift(mid)})).attend;
      if (att > s.targetBaseline) hi = mid; else lo = mid;
    }
    shift = (lo + hi) / 2;
  }
  const o = withShift(shift);
  const b0 = eligibleAttendance(M.simulate({...base, over: o}));
  const metrics = {wage_usd: W, vlow_shift: shift, baseline_attend_eligible: b0.attend, n_eligible: b0.n};
  for (const usd of s.amountsUSD) {
    const res = M.simulate({...base, over: o, policy: {cash: usd / W}});
    const e = eligibleAttendance(res);
    metrics['cash_units_' + usd] = usd / W;
    metrics['effect_attend_' + usd] = e.attend - b0.attend;
  }
  if (s.amountsUSD.length >= 2) {
    const [a, b] = s.amountsUSD;
    metrics['effect_diff_' + b + '_minus_' + a] = metrics['effect_attend_' + b] - metrics['effect_attend_' + a];
  }
  return {metrics, parameters: {W, over: o, targetBaseline: s.targetBaseline},
    evidence_role: 'external pattern check against a published regression-discontinuity estimate (to verify)',
    limitation: 'W unsourced; lever pays all ages, not only Grade 7 entrants; RD estimates are local to the poverty cutoff while the model averages the bottom two quintiles'};
}

const task = JSON.parse(fs.readFileSync(0, 'utf8'));
const result = {camchild_validation}[task.family](task);
result.nonfinite_metrics = Object.entries(result.metrics).filter(([, v]) => typeof v === 'number' && !Number.isFinite(v)).map(([k]) => k);
process.stdout.write(JSON.stringify(result));
