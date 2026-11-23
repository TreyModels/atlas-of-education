# PRE-REGISTRATION — heavy specification/transportability battery on the levels relation

Record `research/records/2026-11-23-corr-battery/`, branch `research/corr-battery-2026-11-23`.
Written and committed **before the battery code is run** (first commit on the branch). Author `un-data`,
23 Nov 2026. Box2 only, working directory `/root/work/corr_battery`, 10 workers.

## Purpose

The corr-rebuild result (record `2026-11-23-corr-rebuild`) found schooling → fertility strongly negative in
**levels** and null-to-positive in **decade changes**, but the pre-registered future-schooling placebo also
"worked", suggesting a development gradient rather than a causal effect. This battery quantifies both: a large
specification grid over every ordered pair of measures, a proper random-repartition transportability test, a
country-clustered bootstrap, and the placebo measured on the same grid.

## Data (fixed)

Project panel `/root/work/data` (observed annual country-year 1960–2024; income file holds LEVELS → natural
log taken in code; no imputation; no interpolation). Plus OWID series already downloaded for corr-rebuild:
total mean years of schooling (1870–2020), female and male mean years of schooling (1990–2023), adjusted
gender parity index (1970–2024). No new network data are needed.

**Measures (19).** The 17 project measures (electricity, wage employment, lower-secondary completion,
secondary enrolment, tertiary enrolment, primary completion, income, urbanisation, tax, agricultural value
added, agricultural employment, female labour-force participation, life expectancy, under-5 mortality,
secondary gender-parity index, tertiary gender-parity index, fertility) plus total mean years of schooling
and female mean years of schooling. **342 ordered pairs** (19 × 18; a measure never predicts itself).

## Grid A — levels vs changes battery (fixed)

For each ordered pair: outcome y, predictor x, lag L ∈ {0, 5, 10, 15, 20, 25} (years between x at t and y at
t+L), controls C ∈ {none; income; income + urbanisation}, sample S ∈ {all years; 1960–1990; 1990–2024;
7 regions; 4 income groups} (14 samples), and fixed-effect designs:
- LEVELS (outcome = y level): (i) decade FE; (ii) decade + region FE; (iii) country FE (within); (iv) country
  FE + country-specific linear trends.
- CHANGES (outcome = ten-year change in y): (i) country FE (within); (ii) country FE + country trends;
  (iii) decade + region FE.
Spec count per pair: levels 4 × 3 × 6 × 14 = 1,008; changes 3 × 3 × 6 × 14 = 756; **1,764 per pair**;
**603,288 total regressions**. Country-clustered standard errors throughout. Estimates are recorded for every
specification, no selection.

## Grid B — transportability (fixed)

Random re-partitions of countries: **400 partitions**, each into **6 groups** with the region-family group
sizes (the same kind of nesting/size matching used in the earlier multiverse work; every country appears in
exactly one group per partition). Within every (partition, group): the levels relation and the changes
relation for **all 342 pairs**, baseline design (decade FE for levels, country FE for changes; controls income
+ urbanisation; lag 0). That is 400 × 6 × 342 × 2 = **1,641,600 regressions**. Real-group comparison: the same
statistic computed within the 6 real regions, the 4 income groups, and the 7 regions × 6 decade cells.
Statistic: share of group × pair estimates that are negative and significant (|t| > 1.96), and the same for
changes. Checkpoint partial pickles every ~2 minutes.

## Grid C — bootstrap and placebo (fixed)

- **Country-clustered bootstrap, 500 reps** for every pair's headline levels relation (outcome y level,
  predictor x, lag 0, decade + region FE, income + urbanisation, all years): 342 × 500 = **171,000
  regressions**; report bootstrap 5th–95th percentile of the coefficient and the share of pairs whose bootstrap
  interval excludes zero.
- **Threshold-shape bootstrap, 500 reps** for the four schooling measures (total mean years, female mean years,
  secondary enrolment, lower-secondary completion) on the spline with knots at 6 and 9 years: **2,000
  regressions**; report bootstrap intervals for the below-6, 6–9 and above-9 slopes.
- **Future-schooling placebo on the same grid**: x measured at **t + 10** predicting y at t, across the levels
  design grid restricted to lags {0,10} (the lag is set by the placebo construction), 4 FE × 3 controls × 14
  samples: 342 × 4 × 3 × 2 × 14 = **114,912 regressions**. The same battery is run with the correct-time x for
  the identical design cells, so the placebo is compared like-for-like, not asserted.

**Planned total: about 2.53 million regressions.** (If the actual runtime is below the 45–60 minute target
after Grid A+B+C, Grid B partitions are increased from 400 towards 800 with the same pre-registered statistic;
if it is above, checkpoint at 45 minutes and report what completed — the target is load, not a number.)

## Decision thresholds (fixed in advance)

1. **Levels are strong** if, over the 288 baseline levels cells (4 FE × 3 controls × 6 lags × 4 whole-sample/
   period settings) **≥ 80% of estimates are negative and ≥ 50% are negative-significant** at |t| > 1.96,
   and the schooling → fertility pairs are negative-significant in at least 6 of the 8 schooling measures.
2. **Changes are weak** if **< 30%** of change-cell estimates are negative-significant.
3. **Transportability**: the level relation is a *global between-country property* if the random-repartition
   share of negative-significant group-pairs is **≥ 0.80** and the change share is **≤ 0.10**; it is "patchy"
   if the real-group share differs from the random share by more than 2 random SDs. The earlier corr-rebuild
   figure of 54% real-group vs 90% random is the hypothesis to be re-measured, not assumed.
4. **Placebo / development gradient**: if the future-schooling placebo's negative-significant share is
   **≥ 80% of the correct-time share** in the identical design cells, the levels correlation is declared a
   development-gradient association and **not** an identified effect of schooling at time t. If the placebo
   share is below half the correct-time share, the level relation is more credible as a timing-specific
   association.
5. **Bootstrap**: a headline level relation is "robust" if the country-clustered bootstrap interval excludes
   zero for ***at least 90% of the 342 pairs*** (the battery asks about the whole matrix, not one pair).

## Machinery and honesty rules

- 10 worker processes on box2 (12-core quota; 2 cores left for other agents' downloads); thread caps set to 1
  per worker.
- Progress log every ~15 seconds with specifications completed and specifications/second; partial pickles
  every ~2 minutes so a crash loses at most two minutes.
- No selection: every pre-registered cell is recorded; the report will state the exact number of regressions
  actually run and the wall time.
- Standard errors clustered by country for every specification; no causal language where the design does not
  identify causation; the placebo is part of the headline, not an appendix.
- Any deviation from this document (grid sizes, worker count, runtime cut-offs) will be listed in the results
  commit with the reason.
