# PRE-DECLARATION — push-pull cohort-flow massification model (task-37)

Status: **scaffold + predeclaration only. NOTHING HAS BEEN FITTED.** Calibration is gated on Council brief 013
(task-39), which must define what "reproducing universalization" means (series, countries, tolerance, holdout)
before any parameter is estimated. This file is written before that gate lands so the design cannot drift.

## Model (declared)

New module `pushpull.py` (no atlas engine reused; `twoway.py` was **not found in this checkout**, so nothing is
reused from it — recorded rather than guessed). Six single-year cohorts countries: PHL, KHM, HKG, CHN, KOR, JPN;
years 1960–2040 (reporting 1980–2040).

**Cohorts and fertility.** Ages 0–84, single-year. Births from a declared TFR path (sourced from WDI where on
disk: PHL/KHM/HKG/CHN; KOR/JPN assumed and labelled). Age-band survival, declared approximation.
**School flow.** Intake at age 6; progression primary→lower→upper→tertiary with country cycle lengths; annual
progression rates depend on income, urbanisation and (demand-led channel only) lagged job opportunities.
Enrolment stocks are constructed from the cohort flow, not supplied.
**Sectors.** Agriculture share declines with log GDP per capita; non-agriculture splits into industry/services;
formal share of non-agriculture rises with the educated labour share and income.
**Two channels, stated elasticities and lags.**
- *education-led* `e_s ∈ [0, 0.6]`, lag `lag_s ∈ [1, 8]`: educated-labour share → GDP growth / formal-sector growth.
- *demand-led* `e_d ∈ [0, 0.8]`, lag `lag_d ∈ [0, 5]`: job opportunities → intake and progression.
**Rivals (same code, switches).** R1 demand-led (`e_s = 0`); R2 education-led (`e_d = 0`); R3 complementary (both).
Same countries, same exogenous paths, same outcomes. Observational equivalence will be reported explicitly.

## Labels
Every config value is labelled S (sourced) / E (estimated) / A (assumed) / F (to be fitted). The F slots are
**ranges**, never target values. No observed target (GER, completion, sector share) is coded as a parameter; an
automated check in the smoke run asserts the config contains no target-series key.

## Calibration design (executed ONLY after the gate)
- **Fit window 1980–2010; holdout 2011–2024.** Split declared here, before data contact.
- **Fit/check labels.** Every target row is labelled `fit` or `check` before estimation, with the predicted sign
  per rival. Education targets (GER by level, completion by level) are `fit`; sectoral-employment shares
  (agri/industry/services) and the formal-share proxy are `check` (excluded from the fit); holdout years of the
  education targets are `check`.
- **Objective.** Equal-weight mean absolute error in percentage points over the fit targets, plus a declared
  share-metric term for sector shares. Pareto/fit surface reported, never only the argmin.
- **No target coded as a parameter.** Progression/intake/elasticity parameters are free; targets are never read
  into the config.
- **Seeds/workers.** Matched seeds across rivals; workers ≤ 2; every run labelled *simulated*.

## Scaling checks (generated vs supplied)
The model must be asked to produce, not be given, the exponents in `../relations/` (task-36) and `../model2/`
(task-38): log–log slopes of GER secondary and tertiary on GDP per capita, and of agri/services shares on GDP per
capita. Report **generated exponents vs the relations/ estimates** and state which had to be supplied. The
`relation` estimates are checks/constraints, not parameters unless explicitly declared.

## Push-pull decomposition and the discriminating test
- **Decomposition.** For each country, the share of the 1980→2024 change in attainment attributable to demand
  pull vs supply push, by a Shapley decomposition over {`e_s`, `e_d`} (average marginal contribution over both
  orderings), with uncertainty from parameter draws. Reported as a share with an interval, never as a point.
- **Discriminating experiment.** (i) a GDP shock only (e.g. a 2-year −10% GDP shock around a crisis year):
  demand-led predicts an immediate enrolment fall; education-led predicts no immediate enrolment response and a
  slower subsequent GDP path. (ii) a schooling-supply shock only (intake +10 pp): education-led predicts a
  delayed GDP/formal-share rise; demand-led predicts no GDP response. The discriminating statistic is the sign
  and timing of the cross-response (enrolment→shock and GDP→schooling shock).
- **Recovery / forced-ID.** Simulate from each rival, fit all three to the same moments, report the confusion
  matrix and a forced-identification rate against a truth outside the model set. "Both directions matter" is not
  reported as a result unless the channels are separable or the equivalence is demonstrated.

## What is blocked on brief 013 (task-39)
1. The exact operational definition of "reproducing universalization": which series, which countries, what
   tolerance, which holdout, and what counts as a fail.
2. Whether the model is scored on GER, completion, transition, sector shares, or a declared composite.
3. The stop rule and the ranking of the three rivals.
Until these land, only `--structure-smoke` may run (accounting identities, declared priors, no fit).
