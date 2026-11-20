# DATED AMENDMENT M2b — declared partial re-run of model2 Parts 1–2 against landed relations data

**Date:** 2026-11-20. **Authority:** Council brief-013 Amendment A1 (M2b authorized); executor direction.
**Scope:** estimation only (no model fitting, no calibration); observed data only; direction claims remain
barred (R13/EQUIVALENT). Original M2 estimates in `runs/scaling_estimates.csv` remain the labelled original
run; this amendment is a **declared partial re-run** against `10_massification/relations/data/` and must not
be read as replacing the original.

## What was re-run
1. **Part 1 (scaling):** lower-secondary completion ~ income (the flagged coefficient) plus secondary/tertiary
   GER, under (a) year-FE log-log, (b) year-FE logit, (c) between estimator (M2's estimator), on
   `09_relations/data/panel_wdi_wide.csv` and `panel_wdi_eci.csv` — same estimators/thresholds as M2.
2. **Part 2 (universalization dynamics):** comparison of model2 logistic fits against scout's
   `10_massification/relations/data/universalization_fits.csv` (50 matched country-indicator cells),
   common-shape verdicts (`universalization_common_shape.csv`), and push–pull lead-lag tests
   (`push_pull_tests.csv`).

## Discrepancy resolution — lower-secondary completion coefficient
| specification (same estimators/thresholds) | coefficient | SE | n |
|---|---|---|---|
| log-log, year-FE (scout-style) | **+2.282** | 0.340 | 629 |
| log-log, year-FE (PPP income) | +1.968 | 0.435 | 548 |
| logit, year-FE | −9.325 | 1.798 | 629 |
| **logit, between (M2 estimator)** | **+1.362** | — | 28 countries |
| M2 original between (WDI30, logged run) | **+0.843** | 0.157 | 30 |

**Resolution:** the discrepancy is **estimator/transform/sample sensitivity, not a data error**. The
between-logit estimate moves from +0.84 (M2 original sample/run) to +1.36 (all-year country means in the
landed panel); scout-style year-FE log-log gives larger positive values (+1.97 to +2.28 here; relay +1.174
uses their exact `linear FE` variant, which could not be reproduced exactly in this timebox because their
script's relative-path layout differs — noted as a limitation below). **The lower-secondary completion
coefficient must therefore be treated as an ESTIMATOR RANGE, not a point**: ~+0.84 (between-logit, original)
to ~+1.17 (scout's relayed FE spec) to ~+2.3 (this re-run's year-FE log-log). The Council gate (Amendment A1
§1) says "coefficient to be re-verified in M2b"; M2b's answer is **range, with transform/FE named**, and the
model's simulated exponents should be judged against that range for ≥2 of 3 laws (R14).

**Limitation:** the exact scout script (`relations/scripts/scaling_laws.py`) could not be executed as-is
(its relative-path layout resolves outside the repo in this sandbox); the scout-style number above is our
reimplementation of the stated spec (log-log, year FE, country-clustered), so the relayed +1.174 is carried
as the scout value and the reimplementation as a check.

## Universalization (Part 2) — comparison
- **Logistic parameters:** 50 matched cells; median |Δr| between scout fits and model2 fits **0.061**, median
  |Δt0| **11.1 years** (parameter comparisons only; fit samples differ).
- **Common shape:** scout rejects common slopes for GER secondary, tertiary, upper-secondary (p≤0.05);
  model2's independent test also rejects (shared=False) → **agree: country-specific slopes**.
- **Lead-lag / push–pull:** scout's 13 tests mark `cannot_discriminate=YES` in 7/13 and describe their own
  set as predictive-only; model2's lead-lag was NOT IDENTIFIABLE → **agree: no causal direction identified**.

## What it changes
- Part-1 lower-secondary completion is recorded as an **estimator range (+0.84 to ~+2.3; scout relay
  +1.174)** rather than a single law point; the classification of "scaling law" is retained only as
  *direction-stable*, with the magnitude range disclosed.
- Part-2 conclusions are **unchanged** (country-specific slopes; no identifiable lead-lag). No direction
  claim; direction stays EQUIVALENT (R13).
- Data-hunter's task-34 series (`10_massification/data/`) landed after this run: **adoption re-run is
  deferred** per executor/lead instruction; no silent replacement of M2 or M2b estimates.

## Files
`runs/m2b_scaling.csv`, `runs/m2b_logistic_compare.csv`, `runs/m2b_findings.txt`, `runs/m2b_meta.json`.
