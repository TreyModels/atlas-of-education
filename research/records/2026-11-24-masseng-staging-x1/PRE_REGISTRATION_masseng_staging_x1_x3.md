# PRE-REGISTRATION — X1 exposure-matched sequencing + X3 feedback-elasticity surface (task-27)

**Status: committed BEFORE the pilot code and before any run.** EXPLORATORY. SIMULATION ONLY.
No causal language. No confirmatory claim. These are stipulated toy worlds from the existing
`eduengine`; nothing is fitted to a country. **Rural migration remains not simulated** (rural is
a household attribute plus an extra schooling cost and lower tutoring-firm access; no migration
flows). Branch `research/masseng-staging-x1-2026-11-24`, additive from the audit branch head
`ff84e75`. The engine (`engine/eduengine/`, `engine/worlds.py`) is used unmodified — no engine
rewrite, no Codex-branch rewrite.

Authorisation: task-27 (Trey's server-heavy directive; the two follow-ups proposed in
`research/records/2026-11-24-masseng-timing-audit/audit_tables/next_experiments.json` X1 and X3,
audit commit `ff84e75`). The audit found that the original `school_first − jobs_first`
contrast was **not exposure-matched** (+1.8 education-share-years vs −1.2 vacancy-years), that
the fiscal loop gave `jobs_first` ~9.5 % higher cumulative education budget, and that the
one-year fiscal lag made "simultaneous" non-simultaneous. X1 tests whether anything survives
exposure matching; X3 tests robustness to the assumed education-to-jobs feedback.

**Server constraint.** Two 4,096-draw Bayesian screens are active on region-42 (48 workers).
They are not to be killed. X1/X3 run with a bounded pool (**≤20 workers**, declared below) and
are cheap (~1,500 runs total ≈ 1,260 CPU-s by the audited ~0.83 CPU-s/run). If load/contention
makes either run exceed 15 minutes wall, stop and report the log/traceback; do not silently
retry with a larger pool.

---

## 1. X1 — exposure-matched sequencing test

**Question.** After equalising cumulative exposure to the education-share and vacancy-rate
changes, does any `school_first − jobs_first` difference in the pre-declared metrics persist, or
was the original contrast cumulative exposure/revenue rather than order?

**Engine settings (declared, same as the audited staging experiment).** `worlds.make('formal_loop',
seed=s, N=400, T=70, measure_from=35, job_elasticity=feedback, gates=<bar|quota>, events=<arm>)`.
Cohorts 35–44 measured. Gates exactly as in the audited experiment:
`bar = [bar3.0, bar5.5, bar8.0, bar11.5]`;
`quota = [bar3.0, quota(share=.55,cut0=7.0), quota(share=.45,cut0=10.0), bar11.5]`.
Events set `edu_share` from 0.18 to 0.30 and/or `vac0` from 0.08 to 0.16.

**Factors.** 9 arms × 2 feedback (0, 1) × 2 gates (bar, quota) × 20 seeds (0–19) = **720 runs**
(≈600 CPU-s). *Arithmetic reconciliation with task-27's "6 arms × 2 × 2 × 20 = 480":* the
declared **primary 6-arm set** is `none, school_first, jobs_first, simultaneous,
matched_school_first, matched_jobs_first` = 480 runs; the **supplementary 3 arms**
(`matched_simultaneous`, `shifted_school_first`, `shifted_jobs_first`) add 240 runs. Primary and
supplementary arms are fixed here, before any run; no arm will be added or dropped after seeing
results.

**Arms (events).**

| arm | events | cumulative education-share-years | cumulative vacancy-years | role |
|---|---|---|---|---|
| `none` | none | 12.6 | 5.6 | baseline |
| `school_first` (unmatched) | edu@15, jobs@30 | 19.2 | 8.8 | original confounded contrast |
| `jobs_first` (unmatched) | jobs@15, edu@30 | 17.4 | 10.0 | original confounded contrast |
| `simultaneous` (unmatched) | both@15 | 19.2 | 10.0 | original both-early |
| `matched_school_first` | edu@0 (years 0–47), jobs@22 (22–69) | **18.36** | **9.44** | primary matched arm |
| `matched_jobs_first` | jobs@0 (0–47), edu@22 (22–69) | **18.36** | **9.44** | primary matched arm |
| `matched_simultaneous` | both@22 (22–69) | 18.36 | 9.44 | supplementary reference |
| `shifted_school_first` (placebo) | edu@25, jobs@40 | 18.0 | 8.0 | calendar-shift placebo |
| `shifted_jobs_first` (placebo) | jobs@25, edu@40 | 16.2 | 9.2 | calendar-shift placebo |

Cumulative exposure = Σ_t value(t) over the 70 model years (base value before the event, treated
value from the event year). The three matched arms therefore have **identical total
education-share-years and identical vacancy-years**; only their timing differs. The placebo arms
keep the unmatched order structure but shift the calendar by +10 years (their exposure differs
between each other by exactly the unmatched +1.8 edu-share-years / −1.2 vacancy-years).
The fiscal channel lags one year (budget from this year's revenue is spent next year) while
vacancies act in the event year; exposure totals above ignore that lag, and the matched arms also
have equal *lag-adjusted* education years (48 treated years each).

**Pre-declared contrasts (seed-level paired differences; 4,000-draw seed bootstrap; 90 % and
95 % CIs; sign counts and leave-one-seed-out sign stability).**
- **Primary target:** `matched_school_first − matched_jobs_first` (equal total exposure, opposite
  order).
- Reference decomposition: (`matched_school_first − matched_simultaneous`) and
  (`matched_jobs_first − matched_simultaneous`), whose difference equals the primary contrast.
- Confounded comparator (reported, not the target): `school_first − jobs_first`.
- Placebo: `shifted_school_first − shifted_jobs_first` vs the confounded comparator.
- Metrics (all 13): completion_primary/lower/upper/tertiary; tut_rate; mpl_primary; q_pub;
  formal_share_gdp; edu_gdp; parity_location_lower; parity_wealth_lower; parity_location_upper;
  parity_wealth_upper.

**Pre-declared material thresholds and falsifier (fixed now).**
- A contrast is **material** on a metric if |mean| ≥ **0.005 (0.5 pp)** for the four completion
  metrics or ≥ **0.02 (2 pp)** for `formal_share_gdp`/`edu_gdp`/`q_pub`/`parity_*`/`tut_rate`,
  **and** its 90 % seed-bootstrap CI excludes 0.
- **Metric families:** (i) **exposure-sensitive/mechanical** = `formal_share_gdp`, `edu_gdp`,
  `q_pub` (the audit found these material and sign-stable for the unmatched contrast);
  (ii) **completion/equity** = the four completion metrics, `tut_rate`, `parity_*` (the audit
  found these small and not sign-stable for the unmatched contrast).
- The matched contrast is **≈0** for a metric if its 90 % CI includes 0 **and**
  |mean_matched| ≤ **0.25 × |mean_unmatched|** for that metric (unmatched material).
- **Decision categories (pre-declared; reported per condition and overall):**
  - **A — FALSIFIER CONFIRMED (exposure/revenue, not order):** on family (i) and/or on any
    family-(ii) metric where the unmatched contrast is material, the unmatched contrast is
    material **and** the matched contrast is ≈0.
  - **B — ORDER EFFECT IN THE MODEL:** on at least one family-(ii) metric the matched contrast is
    material with the **same sign** as the unmatched contrast (report as a toy-model timing
    effect, still not causal evidence).
  - **C — NO MATERIAL UNMATCHED EFFECT:** the unmatched contrast is not material on any metric
    (audit-consistent: no sequencing effect to interpret).
  - **D — MIXED/OTHER:** anything else (e.g. matched material with the opposite sign, or
    conditions disagree). Report all cells; no headline.
- **Overall rule:** a category is assigned only if it holds in **≥3 of the 4 feedback×gate
  conditions**; otherwise report per-condition categories and "inconsistent". If several
  categories hold by metric family, report them side by side (e.g. "A on family (i); C on
  family (ii)") — this is expected by the audit and is the primary anticipated outcome.
- **Placebo interpretation:** if the shifted placebo contrast differs from the unmatched
  contrast by more than its 90 % CI width on a material metric, calendar/cohort-window position
  is a plausible driver and is reported; otherwise no evidence of calendar-position sensitivity.

**Anticipated outcome (declared before running, not a claim).** The audit predicts the unmatched
family-(i) contrasts are exposure-driven and the family-(ii) contrasts are not material; X1
therefore most likely yields **A on family (i) and C on family (ii)** — i.e. the sequencing
"effect" does not survive exposure matching. Any other pattern is reported as such.

## 2. X3 — feedback-elasticity robustness surface

**Question.** Are sequencing conclusions robust to the assumed education-to-jobs feedback?

**Design.** `job_elasticity ∈ {0, 0.25, 0.5, 0.75, 1.0}` × 4 schedules
(`none, school_first, jobs_first, simultaneous`, the original unmatched arms) × 2 gates
(bar, quota) × 20 seeds (0–19) = **800 runs** (≈660 CPU-s). N=400, T=70, measure_from=35,
same gates/events as X1's unmatched arms.

**Contrasts:** `school_first − jobs_first` and `simultaneous − none`, per elasticity × gate, with
seed-level paired differences, 4,000-draw seed bootstrap 90 %/95 % CIs, sign counts and
leave-one-seed-out stability; report the **full surface** (no point selection).

**Pre-declared falsifier / verdict:**
- **ROBUST** for a metric if its contrast is material (thresholds in §1) with the **same sign at
  every elasticity**, in ≥3 of the 4 (schedule-pair × gate) cells.
- **REVERSAL** if the sign changes across the elasticity grid with material CIs at both ends.
- **NULL** if the contrast is not material at any elasticity.
- Report the surface for all 13 metrics; no conclusion may be based on a single elasticity; do
  not choose an elasticity post hoc.

## 3. Execution, preservation, analysis

- Region-42 only (`/root/miniconda3/bin/python`, `PYTHONPATH=/root/work/masseng-codex-deps` for
  scipy, numpy 2.2.6, scipy 1.15.3 verified); **bounded pool ≤20 workers** because 48 Bayesian
  workers are active. Do not kill those screens.
- Exact commands, start/end timestamps, host, worker count, code hashes (driver, `engine/worlds.py`,
  `engine/eduengine/*.py`), and seed-level rows are written to fresh files only; **no file may be
  overwritten** (open with exclusive creation). Failures keep their log/traceback; no silent retry.
- Both experiments write one JSON each: rows (arm/elasticity × feedback × gate × seed), metrics,
  annual series, event logs, config, elapsed, hashes. Analysis is a separate script committed with
  the results; all outputs and the analysis script are committed and pushed with `RUN_REPORT.md`.
- No causal language; no p-values are used as evidence of effects; all uncertainty is seed-level
  Monte Carlo; worlds are stipulated; migration is not simulated.

## 4. Stop rules

- If the engine cannot import on the server (e.g. scipy path) → preserve traceback, report, stop.
- If >2 % of runs raise or return non-finite metrics → stop and report; no silent retry.
- If either experiment exceeds 15 min wall due to host contention → preserve log and report.
- If the primary matched contrast is undefined (missing arms) → report as failure.

## Deviations log
- 2026-11-24 (X1 run 1, INVALID for the primary analysis): the first implementation of the two
  dose-matched arms used one-way step events without end events, so the early intervention stayed on
  for all 70 years: the emitted exposure check gave `matched_school_first` 21.0 edu-share-years /
  9.44 vacancy-years and `matched_jobs_first` 18.36 / 11.2 — **not** the declared 18.36 / 9.44 for
  both. The primary matched contrast from run 1 is therefore not exposure-matched and is reported as
  **INVALID**, not interpreted. Run 1 is preserved under
  `results_x1_v1_INVALID_matched_arms_not_exposure_matched.json` (never overwritten);
  `results_x1_EXPLORATORY.json` is its untouched original.
- 2026-11-24 (fix, before the corrected run): the two matched arms now add end events at year 48
  (`education_revert` to 0.18 / `vacancy_revert` to 0.08) so each intervention is treated for exactly
  48 years, matching the declared arm table; the driver's exposure function now re-simulates the
  parameter path and verifies 18.36 / 9.44 for all three matched arms. Only the pre-declared arms and
  seeds are rerun (`results_x1_EXPLORATORY_corrected.json`); no arms/seeds/thresholds were changed.
- X3 was unaffected by this bug (it uses only the four original schedules) and ran once, as declared.
