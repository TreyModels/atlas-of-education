# Pre-registration — scaling-law tests (The Networked Domus, Appendix A)

Written before any results file was created, and committed before analysis code produced output.
Task `task-19`, branch `research/scaling-2026-11-23`, record `research/records/2026-11-23-scaling/`.

## Claim under test

Appendix A proposes that low-inhibition (low-θ) kin networks diversify functionally as they scale
(Heaps-type sublinear growth of functional categories), while high-inhibition/high-γ systems shift to
a logarithmic/saturating regime in which scale yields diminishing functional diversity and credential
categories proliferate without new functions. A scaling regularity of this kind is **not a causal
identification**: it constrains functional form, not mechanism. No causal claim will be made.

## Expected patterns (stated before looking at the data)

1. **Occupational category accumulation.** The number of distinct functional (occupational) categories
   grows **sublinearly** with the number of people observed: in `log(distinct categories) = a + b·log(n)`
   the Heaps exponent **b < 1** (expected roughly 0.3–0.8), where the curve is the *accumulation /
   rarefaction* curve (expected distinct categories as a function of sample size), not the raw
   country-level count.
2. **Regime change at universalization.** Adding a squared log-size term gives a **negative** coefficient
   (diminishing returns), or a broken-stick regression finds a **break** in slope, located near the
   universalization threshold (operationalised as the country's attainment level; exact proxy declared
   in the analysis when data are fixed). Countries above the threshold should show a flatter or
   saturating exponent.
3. **Credential inflation.** The US count of credential categories grows **faster than** the count of
   detailed occupations, so the credential:occupation ratio rises over time and is not proportional.
   This is a time-series with few points; power will be reported honestly.
4. **Universal collapse curve.** Fertility (total or cohort) plotted against female attainment falls on
   **one common curve across countries and cohorts** — i.e. a single functional form, rescaled only by
   a country/cohort level factor, describes the data; residuals should not carry strong country or
   cohort structure and should not depend on pipeline stage.

## Falsifiers (stated before the data)

- (1) b ≈ 1 (proportional growth) or b > 1 — no sublinearity; or sublinearity that disappears once
  rarefaction is applied (i.e. raw-count sublinearity is a sampling artefact).
- (2) No significant curvature (squared term indistinguishable from zero) and no broken-stick break
  better than a single line by an out-of-sample or information criterion.
- (3) A constant or proportionally growing credential:occupation ratio.
- (4) No collapse: country-specific curves differ significantly from the pooled curve, or residual
  scatter is large relative to the fitted range, or residuals retain country/cohort structure.

A null will be reported as prominently as a positive result. If a test lacks power (e.g. the US
credential series with a handful of years), it will be labelled as such rather than presented as
evidence for or against.

## Measurement decisions fixed in advance

- **Rarefaction first.** Category counts mechanically depend on sampling effort, so the primary
  quantity is the accumulation/rarefaction curve: for each country, expected distinct categories at
  common sample sizes (analytical rarefaction, E[S_n] = Σ_i [1 − C(N−n_i, n)/C(N,n)]), with
  bootstrap uncertainty. Raw counts are reported only as a descriptive comparison and as a secondary
  regression with an explicit sampling-effort control.
- **Common sample size.** Countries are compared on the rarefied curve at equal n, not on raw counts.
- **Regression.** OLS of log categories on log size (and squared term), standard errors clustered by
  country where the unit of observation is country; for accumulation curves the unit is the country's
  curve, with country-clustered SEs. Every exponent reported with SE and n.
- **Break test.** Broken-stick (piecewise-linear, continuous) regression with a grid search over the
  breakpoint; compare with a single line by BIC and by a sup-F-type statistic; declare a regime change
  only if the break beats the single line in both.
- **Data collapse.** Fit one common functional form to all country/cohort points; quantify overlay by
  (i) the residual scatter around the pooled curve, (ii) the extra variance explained by country or
  cohort identifiers over the pooled fit, and (iii) a comparison of pooled versus country-specific
  fitted curves. Collapse requires that country/cohort structure adds little and residual scatter is
  small relative to the fitted range.
- **Multiple comparisons.** The four tests are treated as four separate pre-registered tests; no
  correction is applied across them, and each is reported on its own.

## Data priorities (fixed)

Priority order: (A) occupational diversity scaling and (C) the fertility–female-attainment collapse
curve are the core tests. (B) the US credential-versus-occupation time series is included if clean
sources are on the machine, otherwise reported as a documented gap. (D) urban fertility scaling is
included only if city-level data exist; otherwise reported as unavailable. A data-availability table
will be published with the results, naming the source, coverage and exclusions for every series used.

## Analysis code

All analysis code and the small inputs/results needed to reproduce every number are committed in
`research/records/2026-11-23-scaling/`. Numbers in the report must be traceable to a results file.

## Addendum (same day, before any results): canonical urbanisation/development scaling laws

Added scope from the Lead: test the standard laws against our data where the data exist, reporting
each estimated exponent side by side with its literature benchmark. Literature benchmarks are fixed
here before fitting:

| law | benchmark being tested | expected / literature value | test |
|---|---|---|---|
| Urban output scaling (Bettencourt) | city output ~ city population^β, socioeconomic | β ≈ 1.15 (superlinear) | needs city-level output/GDP/wages/patents; if absent, documented as data-limited |
| Urban infrastructure scaling | infrastructure ~ population^β | β ≈ 0.85 (sublinear) | same data constraint |
| Zipf / rank-size (city populations) | Pareto tail exponent of city sizes | ≈ 1 | needs WUP city population list; estimate tail index and compare to 1 |
| Gibrat's law | city growth independent of initial size | slope of growth on log initial size ≈ 0 | needs two WUP waves; report slope with SE |
| Heaps' law (occupational/category diversity) | distinct categories ~ sample^b | b ≈ 0.4–0.6 in the literature | rarefaction-corrected accumulation curve (core task) |
| Urbanisation vs income | S-curve, not a power law | logistic fits better than a power law | logistic vs power-law comparison (R² / residual scatter, AIC) |
| Schooling vs income | log-linear (Mincer), not a power law | log years of schooling on log income, slope ≈ 0.05–0.15 | log-log fit with clustered SEs |
| Fertility vs income / urbanisation | nonlinear declining relationship | no single power-law exponent expected | logistic/exponential vs power-law comparison; curvature |
| Teacher–student ratio vs school size | class-size scaling | — | only if clean data exist; otherwise documented gap |

Falsifiers for this addendum: an estimated exponent whose confidence interval excludes the literature
value; a logistic that does not beat a power law for urbanisation–income; a size–growth slope
significantly different from zero (Gibrat fails); a Zipf exponent significantly different from 1.
Any law that fails to replicate is reported plainly as a result, not explained away. Data-limited
laws are declared unavailable rather than replaced with weaker proxies.
