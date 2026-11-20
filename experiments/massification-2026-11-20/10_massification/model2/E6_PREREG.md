# PRE-REGISTRATION — E6 independent timing comparison (observed estimation; NO direction claim)

**Written before running.** E6 owner pair: deepseek-exp2 + pattern-scout (brief-013 slate #2, D34–D37/Amendment A4).
**Timing is the outcome for near-universal systems** (JPN/KOR/HKG); crossing years are HOLDOUT outcomes, never
fitted (R4/R5). No direction claim (R13/EQUIVALENT). Observed cells only; reconstructed rows are sensitivity only,
never primary. No git writes.

**Data.** `10_massification/relations/data/UNIVERSALIZATION_TIMING.csv` (63 rows: crossing bands, status, flags) and
`10_massification/data/UNIVERSALIZATION_SERIES.csv` (observed GER/NER/completion/OOS series). Primary timing row per
country×milestone = lowest-`priority`, non-`reconstructed` row with status ∈ {`crossed`,
`censored_above_at_first_obs`, `not_crossed_by_last_obs`}; reconstructed rows and other measures are sensitivity.
`in_school_*` series = 100 − OOS (derived from observed OOS, labelled derived); GER/NER/completion used as labelled.

**Estimator (independent of scout's E6 run).** For each scored milestone: fit four single-curve forms (logistic,
Gompertz, linear, exponential) by nonlinear least squares **only on observed years strictly before `crossing_lo`**
(the crossing band is holdout; minimum 8 pre-crossing observations, else UNABLE). Predict the crossing year as the
first integer year the fitted curve reaches the milestone threshold; require a predicted crossing within 300 years of
the last fit year, else "no predicted crossing".

**Tolerances (A4/D37).** |predicted − observed band midpoint| ≤ **5 years**; ≤ **3 years** where the band width ≤2y.
`censored_above_at_first_obs` = **LEFT-CENSORED** (boundary constraint only: no point timing credit; report whether a
fit from the observed window would cross at/before the first observed year — descriptive, not scored).
`not_crossed_by_last_obs` = **false-positive test**: a fitted form must not predict a crossing at/before the last
observed year.

**Verdicts.** PASS (within tolerance) / PARTIAL (within 2× tolerance) / FAIL (outside 2×) / LEFT-CENSORED /
FALSE-CROSSING / UNABLE (insufficient pre-crossing observations).
**Decision rule (predeclared).** E6 timing is **reproduced by bounded single-curve forms** iff, across all scored
crossed milestones, **≥2/3 are PASS for at least one bounded form (logistic or Gompertz)** **and** that form produces
**0 false crossings** on the right-censored milestones. Otherwise **FAIL = structural timing miss (R19)**: the cycle
closes with PARTIAL + EQUIVALENT + explicit timing miss (D36).
**Sensitivity.** (i) reconstructed rows; (ii) fitting window = first 70% of pre-crossing observations; (iii) all
measures per milestone; (iv) comparison with scout's `e6_timing_comparison.csv` (cell-level agreement).
**Failure rule.** A form that fails to converge is logged, not dropped silently; a milestone with <8 pre-crossing
observations is UNABLE, not imputed. No threshold changed after results. **Stop-rule links:** R4/R5 (supplying/
fitting timing invalid), R19 (timing structural miss), R13 (no direction claim), R3 (equivalence report).
