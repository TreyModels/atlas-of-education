# PRE-REGISTRATION — rebuilding the schooling–fertility correlation at the right level

Record: `research/records/2026-11-23-corr-rebuild/`. Branch `research/corr-rebuild-2026-11-23`.
Written and committed **before any analysis code is run** (this file is the first commit on the branch).
Author: `un-data`, 23 Nov 2026.

## The claim we are testing

Dr. Menefee's reading: "more schooling, fewer births" is real, and our previous null is an artefact of the
level of analysis. The matrix regressed the **ten-year change** in fertility on the **starting level** of
schooling with **country fixed effects and country-specific trends**, which absorbs the between-country and
long-run (between-cohort) variation that carries the relationship. We will test the relation in **levels**
(between-country) and compare it, side by side, with the **decade-change** estimator.

## Pre-registered expected pattern (stated before results)

**P1. Levels are strong.** The schooling coefficient in the levels specification should be **negative and
statistically significant** (|t| > 1.96) for the schooling measures based on attainment, and larger in
magnitude than in the change specification. Pre-registered expectation: roughly −0.2 to −0.5 fewer births per
woman per additional year of schooling (or the equivalent in per-cent terms for completion/enrolment measures).

**P2. Changes are weak.** The same schooling measure in the decade-change matrix (country FE, decade effects,
country trends, income logged, urbanisation) should be **small and not significant** — as found before
(secondary enrolment → fertility −0.0015 ± 0.0016 with trends).

**P3. The level relation is transportable.** Running the grouping-multiverse logic on the level relation (real
groupings: region, income group, decade, region × decade; plus 400 random re-partitions as the yardstick)
should show the level coefficient **negative and significant in the large majority of groupings** (pre-
registered threshold: **≥ 70%** of real groupings negative and significant), whereas the change relation is
expected to be patchy (pre-registered threshold: **< 50%**).

**P4. Cohort female attainment, lagged.** Female mean years of schooling lagged 15–25 years should predict
lower period fertility and lower cohort fertility; the association should be **stronger when lagged 15–25
years than contemporaneously** (pre-registered directional prediction), and should show **diminishing
returns / a threshold around secondary completion** (a knot at 6 years of schooling and another at 9 years;
pre-registered expectation: the steepest fall in fertility between about 4 and 8 years of female schooling).

**P5. Specification curve.** Across the pre-registered grid of defensible specifications (below), **≥ 80%**
should have a negative schooling coefficient and **≥ 50%** a negative-and-significant one. If the shares are
near 50% and 5% (a coin flip and a nominal-size tail), that is a null result and will be reported as such.

**P6. Placebo.** Schooling measured **after** the fertility outcome (schooling at t+10 predicting fertility at
t) must be null or smaller than the correct-time relation; large "future schooling" effects would indicate
that the level relation is a common trend, not schooling.

## What would falsify the thesis's core relation (stated in advance)

If the level relation is **null or positive** (P1 fails), or if it is negative only for enrolment measures and
not for attainment, or if it disappears once income and urbanisation are controlled and never shows up in the
cohort/lag specifications, then the claim "more schooling, fewer births" is **not supported by these data at
the country level**, and we will say so plainly: that is a serious problem for the thesis, not a small
adjustment. If the level relation is strong while the change relation is weak, that is the expected pattern
and we will report the contrast as the result (with the caveat that levels are between-country and cannot be
given a causal reading without the shocks/micro work).

## Pre-registered designs and decision rules

**Data (fixed in advance).** Observed panel `/root/work/data` (income in levels → natural log; never use the
gap-filled panel for headline numbers; report the imputed panel only as a robustness check if at all). Annual
country-year data 1960–2024. Sources: project panel for completion/enrolment (primary completion, secondary
enrolment, tertiary enrolment, plus the gender parity indices) and barro-lee/owid female and total mean years
of schooling (downloaded from Our World in Data; citation recorded). Cohort fertility from UN WPP cohort
fertility via OWID.

**Analysis 1 — levels vs changes matrix (same estimator, two levels of analysis).**
- Changes (the existing matrix): Δ10 fertility_t on schooling_t, country FE + decade FE + country trends,
  income logged, urbanisation, clustered by country.
- Levels: fertility_t on schooling_t, decade FE (then decade + region FE), income logged, urbanisation,
  clustered by country, no country FE.
- Also report the pure between-country cross-section (country means over the whole period) as a third panel.
- Estimand: births per woman associated with one more year of schooling (attainment measures) or one
  percentage point of completion/enrolment (rate measures).
- Report coefficient, clustered SE, n, countries, and the levels-versus-changes ratio.

**Analysis 2 — transportability of the level relation.**
- Real groupings: region (project regions), income group, mortality/fertility transition stage, decade,
  region × decade; at least 40 real groups in total.
- Yardstick: 400 random re-partitions with the same group sizes and nesting rule.
- Statistic: share of groups with a negative and significant level coefficient; compare real vs random, and
  the same statistic for the change relation.
- Pre-registered: level ≥ 70% vs change < 50%.

**Analysis 3 — cohort female attainment, lagged.**
- Measures: female mean years of schooling (lag 0, 10, 15, 20, 25 years); total mean years; secondary
  completion/enrolment; tertiary; gender parity index in tertiary (inversion = index > 1).
- Outcomes: period TFR, cohort fertility (birth-cohort based).
- Functional form: linear, log, quadratic, and a restricted cubic spline with knots at 6 and 9 years.
- Pre-registered threshold test: coefficient on years of schooling above 6 years versus below.
- Female vs total comparison; attainment vs enrolment comparison.

**Analysis 4 — specification curve (pre-registered grid).**
Systematic grid: lags {0, 10, 15, 20} × control sets {none; income; income+urban} × FE {decade; decade+region}
× forms {linear; log; quadratic; spline(6,9)} × outcomes {period TFR; cohort fertility} × measures {female
attainment; total attainment; secondary completion} = **576 specifications** (all reported, no selection).
For each: coefficient, clustered SE, sign, |t| > 1.96. Report: share negative; share negative-and-significant;
median coefficient; the specification-curve figure; and which design choices flip the sign.
Placebos: (a) future schooling (t+10) predicting current fertility; (b) schooling at t predicting fertility
change over the **previous** ten years.

**Uncertainty and inference.** Country-clustered standard errors throughout; report n and number of countries
for every headline; for the specification curve report the distribution, not a selected spec; for the
transportability test use the pre-registered share thresholds, not a post-hoc one. Any deviation from this
document will be listed in the results commit and explained.

## Why pre-register this

The expected answer is known to the requester and the previous result is known to us: the risk is that the
analysis is steered towards the expected contrast. Freezing the predictions, the exact specification grid, the
transportability thresholds and the falsification conditions before touching the data means the report can be
checked against this file. If the data contradict the expectation, P1/P3/P5 fail visibly against this
document.
