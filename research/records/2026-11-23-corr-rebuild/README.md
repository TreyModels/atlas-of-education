# Rebuilding the schooling–fertility correlation at the right level of analysis

Worker `un-data`, branch `research/corr-rebuild-2026-11-23`, 23 Nov 2026. Box2 only (`autodl2`),
`/root/work/corr_rebuild`, 4 cores. Pre-registration: `PRE_REGISTRATION.md`, commit **c077672**, written
and pushed **before any analysis code**; results are the second commit. Scripts in `scripts/`, results in
`data/`, figures in `figures/`.

**Short answer.** Dr. Menefee is right about the level of analysis: in **levels**, more schooling goes with
fewer births, strongly and everywhere (female attainment: −0.13 births per woman per year of schooling;
total attainment −0.23; secondary enrolment −0.021 per percentage point; all significant, 190+ countries).
In **decade changes** the same measures are weak or go the **opposite way** (+0.12 for female attainment,
+0.008 for secondary enrolment, both significant), which is exactly how our previous null was produced.
But the level correlation is a **development-gradient association, not an identified schooling effect**: a
placebo where *future* schooling predicts *current* fertility is just as strong (median −0.68), so the level
relation cannot be read causally. The honest bottom line: the correlation is real and was mis-tested before;
it is not evidence that more schooling causes fewer births.

## (1) Fertility

**Levels versus decade changes, same measures, same period.** Levels spec: fertility level on schooling
level, decade + region effects, income logged, urbanisation, country-clustered SEs, no country effects.
Changes spec: ten-year change in fertility on the starting schooling level, country effects + decade effects
+ country trends, income logged, urbanisation (the project matrix). Coefficient (clustered SE).

| measure | levels | decade changes (trends) | n / countries (levels) |
|---|---|---|---|
| mean years of schooling, women | **−0.129** (0.029) | **+0.111** (0.045) | 5,915 / 192 |
| mean years of schooling, total | **−0.228** (0.042) | **+0.190** (0.055) | 1,394 / 144 |
| secondary enrolment (%) | **−0.0213** (0.0037) | +0.0030 (0.0026) | 5,927 / 202 |
| lower-secondary completion (%) | **−0.0224** (0.0035) | **+0.0066** (0.0031) | 4,106 / 193 |
| primary completion (%) | **−0.0239** (0.0033) | −0.0003 (0.0019) | 4,878 / 193 |
| tertiary enrolment (%) | **−0.0040** (0.0020) | −0.0044 (0.0026) | 5,126 / 198 |
| gender parity index, tertiary | **−1.27** (0.20) | +0.0006 (0.207) | 4,455 / 198 |

In plain words: a country where women have five more years of schooling has about 0.65 fewer births per
woman (level relation), other things equal; one more percentage point of secondary enrolment goes with 0.02
fewer births. The change relation is not merely absent — for half the measures it is significantly
**positive**: within a country, decades when schooling expanded fastest are not decades when fertility fell
fastest (they are often the opposite; this is a within-country association and no causal reading is offered).

**Income does not explain it.** In the same level specification, adding income log: female schooling
−0.129 (0.029) with income −0.231 (0.063); total schooling −0.228 (0.042) with income −0.142 (0.087, not
significant). Income alone gives −0.318 (0.066), so both predict the level; schooling is not a proxy for
income in this comparison.

**Specification curve (pre-registered grid, all 336 specs reported).** Of 288 period-TFR specs (4 lags ×
3 control sets × 2 fixed-effect sets × 4 functional forms × 3 measures): **99.7% negative, 91.3% negative
and significant, 0% positive and significant**, median coefficient −0.475. All 336 including 48 cohort cells:
96.1% negative, 81.8% negative-significant, 3.6% positive-significant. Pre-registered P5 (≥80% negative, ≥50%
significant-negative) is **confirmed** for the period specs. The cohort cells are mixed (75% negative, 25%
negative-significant, 25% positive-significant) on only 24–27 countries — inconclusive.

**Transportability (pre-registered analysis 2).** In real groupings the negative-significant share is:
region 50% (6 groups), income group 75% (4), decade 100% (4), region × decade 43% (21) — **pooled 54%**, which
**fails** the pre-registered ≥70% threshold. But the random-yardstick comparison is the informative part:
across 400 random repartitions of countries into 6 groups, the level relation is negative and significant in
**90%** of groups (5th–95th percentile 67–100%), versus **1%** for the change relation (0–17%). So the level
relation is a *global* property that shows up in almost any arbitrary subset of countries, while the change
relation is essentially absent from arbitrary subsets. The real-group shortfall comes from small, homogeneous
cells (a region × decade cell has little schooling variation left), not from absence of the relation.

**Lags, thresholds, cohort attainment (analysis 3).** Female attainment lagged 0/10/15/20/25 years:
−0.129, −0.090, −0.075, −0.062, −0.055 — the association is **strongest contemporaneously and decays** with
the lag, so the pre-registered directional prediction (stronger at 15–25 years) **failed**. The threshold
shape is clear for female attainment: below 6 years the slope is −0.33 (0.05), between 6 and 9 years −0.09
(0.05), above 9 years +0.11 (0.03) — most of the level association sits in the move from very low to
lower-secondary schooling. Cohort fertility with attainment measured at cohort age 25: total attainment
−0.001 (0.028; 202 observations, 24 countries), female +0.051 (0.019; 223 observations, 27 countries) — too
thin a sample to settle anything.

**The falsifier that fails, and it matters.** Pre-registered placebo P6: *future* schooling (measured ten
years later) predicting current fertility. Result: **24 of 24 specs negative and significant, median
coefficient −0.68** — as large as the correct-time relation. Countries whose schooling will be high in ten
years already have low fertility today; education and fertility are both persistent development outcomes.
This is not a small caveat: it means the strong level correlation **cannot** be given a causal reading, and
the pre-registered P6 is **failed**. The backward-change placebo is null (0 of 12 specs negative-significant),
so the change relation is not an artefact of reverse timing.

## (2) Massification

The level association is with the **stock** of schooling a country carries, not with measured expansions.
Adding one more year of schooling to the average woman in a country is associated with about 0.13 fewer
births in the cross-section, and most of the association is concentrated between roughly zero and six years —
so "massification" in the sense of getting populations from minimal to lower-secondary schooling is where the
level correlation lives. But the expansion (change) side is null-to-positive: decades of rapid schooling
growth are not decades of faster fertility decline, which is consistent with the project's previous matrix
null. Both can be true at once: schooling stock marks where a country is in its development; schooling
*expansion* is not observed to pull fertility down within a decade. Massification therefore sits **before and
alongside** the fertility transition as a marker of the development gradient, not as a demonstrated lever.

## Pre-registered expectations versus results (frozen in c077672)

| # | pre-registered expectation | result |
|---|---|---|
| P1 | levels strong negative and significant | **confirmed** (all attainment/completion measures, survives income) |
| P2 | changes weak/insignificant | **partly failed**: null for primary completion and GPI-secondary, but significantly *positive* for secondary/lower-secondary/tertiary enrolment and mean years |
| P3 | level relation transportable: ≥70% of real groupings | **failed as written** (54% pooled); random-yardstick benchmark 90% vs 1% for changes reframes it as a global property |
| P4 | stronger at 15–25-year lags; threshold at secondary completion | lag direction **failed** (contemporaneous strongest); threshold shape **confirmed** (steepest below 6 years) |
| P5 | ≥80% of specs negative, ≥50% significant | **confirmed** for period specs (99.7% / 91.3%) |
| P6 | future-schooling placebo null | **failed** (24/24 negative significant, median −0.68) — the level relation is a development gradient |

**What would kill the thesis's claim, and what happened.** The pre-registration said: if the level relation is
null or positive, say plainly that the thesis's core relation is in trouble. It is **not** null — it is strong,
robust across measures and specifications, and survives income. What the data do not support is the causal
reading: the future-schooling placebo is as strong as the real thing. So the correct statement is "more
schooling and fewer births are tightly linked across countries and across cohorts of development, but this
design cannot show that schooling causes the fewer births".

## Deviations from the pre-registration (with reasons)

1. Barro-Lee female tables could not be downloaded directly (barrolee.com unreachable from box2: SSL error /
   timeout). Used OWID's Barro-Lee-based female and total mean-years series instead: female 1990–2023 (204
   countries), total 1870–2020. This is why the female long-lag cells are limited.
2. The pre-registered 576-cell grid was **implemented as 336**: the 288 period cells exactly as specified;
   the 288 cohort cells reduced to 48 because the cohort-fertility series covers only 33 countries (cohorts
   1876–1975) and the four-lag dimension cannot be aligned to a cohort outcome, so cohort cells use a fixed
   attainment-at-age-25 alignment.
3. The spline form is summarised by its below-6-years hinge coefficient (the pre-registration did not specify
   how to summarise a spline coefficient for the spec curve).
4. Transportability was pooled across grouping families (region, income, decade, region × decade) and the
   random yardstick uses 6 groups to match the region family; the pre-registration named the families but not
   the pooling rule.

## Files

`PRE_REGISTRATION.md` (commit c077672, before code); `scripts/corr_rebuild_part1.py` (levels vs changes,
lags, thresholds, cohort), `scripts/corr_rebuild_part2.py` (transportability, spec curve, placebos,
income rival, figures); `data/results_part1.json`, `data/results_part2.json`, `data/spec_curve.csv` (all 336
specs); `figures/fig_levels_vs_changes.png`, `figures/fig_spec_curve.png`; `results/logs/`.
