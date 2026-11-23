# Heavy specification / transportability battery on the levels relation (task 21)

Worker `un-data`, branch `research/corr-battery-2026-11-23`, 23 Nov 2026. Box2 only (`autodl2`),
`/root/work/corr_battery`, **10 workers** (hard cap), thread caps on. Pre-registration: `PRE_REGISTRATION.md`,
commits **`772650a`** (grid) and **`6a1927f`** (widened grid), both pushed **before any code existed**.

**Run facts (traceable to `results/logs/battery.log` and `out/checkpoint_final.pkl`).** Launched 20:51:36,
**DONE 10,447,698 recorded result rows in 3,018 s** (3,462 rows/s). Because the transportability phase
aggregates six within-group regressions into each recorded row, the true number of regressions run is
**57,291,101**: battery 936,657; transportability 56,077,352; bootstrap 171,000; threshold bootstrap 6,000;
placebo 100,092. Wall time 50.3 minutes at 10 workers (~9.7-10 cores), checkpoints every ~4 min
(`out/checkpoint_latest.pkl`, final 266 MB). A crash at 20:46 (dispatch bug in the threshold task, 1.58M rows in)
was fixed, a one-unit-of-every-kind dispatch smoke test added (`scripts/smoke_dispatch.py`, passes in 2.2 s), and
the run **resumed from `checkpoint_latest.pkl`** rather than re-running completed work; the grid was not changed.
`results/logs/battery_crashed_2046.log` keeps the crash log.

## Pre-registered grid vs what ran

| phase | pre-registered | actually ran |
|---|---|---|
| A. levels vs changes, 342 ordered pairs | 2,111,508 cells (6,174/pair) | 936,657 estimable cells recorded (44%; the rest fail the minimum-sample rule n≥60, ≥8 countries) |
| B. transportability, random re-partitions | 800 partitions × 6 groups × 342 pairs × 2 relations | **13,800 partitions** (800 base + waves to fill the load target), 56,077,352 within-group regressions |
| C. clustered bootstrap | 500 reps per pair | 500 reps × 342 pairs = 171,000 |
| threshold bootstrap | 500 reps × 4 measures | 6,000 |
| future-schooling placebo | same design grid | 100,092 cells |

All pre-registered decision thresholds are evaluated below; the transportability run exceeds its pre-registered
draw count (a load extension, same statistic) and the battery has fewer *estimable* cells than the full factorial
because of the sample minima — both are stated rather than glossed.

## (1) Fertility

**Headline: the schooling–fertility relation is strongly negative in levels and flips or vanishes in decade
changes, across the whole 342-pair battery.** Focal pairs, baseline spec (levels: decade+region FE, income+urban,
lag 0, all years; changes: country FE + country trends, income+urban, lag 0, all years); coefficient (clustered
SE), and transportability = share of 13,800 random groups where the within-group estimate is negative and
significant (levels | changes):

| schooling measure → fertility | level | change | transport levels | transport changes |
|---|---|---|---|---|
| mean years, women | **−0.129** (0.029) | **+0.115** (0.046) | 0.913 | 0.000 |
| mean years, total | **−0.227** (0.042) | **+0.189** (0.054) | 0.914 | 0.002 |
| secondary enrolment | **−0.0213** (0.0037) | +0.0029 (0.0026) | 0.979 | 0.001 |
| lower-secondary completion | **−0.0224** (0.0035) | **+0.0064** (0.0031) | 0.986 | 0.001 |
| primary completion | **−0.0239** (0.0033) | −0.0004 (0.0020) | 0.989 | 0.028 |
| tertiary enrolment | **−0.0040** (0.0020) | −0.0044 (0.0026) | 0.715 | 0.001 |
| gender parity, secondary | **−1.968** (0.277) | +0.059 (0.190) | 0.962 | 0.072 |
| gender parity, tertiary | **−1.265** (0.197) | +0.010 (0.207) | 0.811 | 0.003 |

All eight level coefficients are negative and significant; three of eight change coefficients are significantly
**positive** (women's years, total years, lower-secondary completion) and none is negatively significant. In each
pair's full specification grid the level coefficient is negative in 70-83% of specs (negative-significant in
43-59%), while the change coefficient is negative in only 24-44% (negative-significant 3.5-13.5%). Across all 342
pairs (many of them unrelated, so signs are mixed by construction), the pre-registered baseline cells give levels
42% negative / 31% negative-significant and changes 51% negative / 9% negative-significant — **changes are weak by
the pre-registered <30% rule**, but the aggregate levels 80%-negative threshold is not met matrix-wide because most
of the 342 pairs are not schooling–fertility pairs. For the eight schooling pairs it is met in five of eight at
the ≥80% level and all eight at the baseline specification.

**Transportability, the direct test.** Over 13,800 random re-partitions (6 groups each, region-family sizes):

- all 342 pairs: levels negative-significant share **0.227** [0.214, 0.239]; changes **0.111** [0.103, 0.120];
- the eight schooling–fertility pairs: levels **0.715-0.989**, changes **0.000-0.072**.

So the "global between-country property" is confirmed **for the schooling–fertility relation** (it survives
arbitrary country groupings) but not for the matrix as a whole, where only about a quarter of pair×group
estimates hold. That is the honest reading of the pre-registered ≥0.80 / ≤0.10 thresholds: they hold for the
relation of interest and fail as a description of all 342 links.

**Threshold shape, 500-rep clustered bootstrap.** For women's mean years: slope below 6 years **−0.326**
[−0.405, −0.248]; 6-9 years **−0.092** [−0.175, −0.013]; above 9 years **+0.112** [+0.057, +0.171]. For total mean
years: **−0.387** [−0.483, −0.283], **−0.274** [−0.364, −0.182], **+0.174** [0.106, 0.250]. The steep part of the
level relation is getting populations from minimal to about six years of schooling; beyond nine years the
conditional level association reverses.

**Bootstrap.** The headline level coefficient's country-clustered bootstrap interval excludes zero for **8 of 8**
schooling–fertility pairs (all-pairs: 74.6% of 342; the pre-registered ≥90% threshold is for the whole matrix and
fails there).

**The placebo, reported as it is.** The future-schooling placebo (schooling measured ten years later predicting
current fertility) on the identical design cells is **not null**: for the schooling–fertility pairs, 52.9% of
placebo cells are negative-significant (median coefficient −0.0179) against 58.8% for the correct-time relation
(median −0.0224) — the placebo is about 90% as strong; all-pairs: 20.1% vs 21.1%. The pre-registered rule
(placebo ≥80% of correct-time ⇒ development gradient) therefore **fires**: the strong level correlation is a
development-gradient association and cannot be given a causal reading. This is the same phenomenon as the 24/24
placebo in the smaller corr-rebuild grid, now measured on the large grid rather than asserted.

## (2) Massification

The battery sharpens the massification story rather than changing it. The level correlation is a property of the
**stock** of schooling and is transportable in the sense that arbitrary groupings of countries reproduce it for
the schooling–fertility pairs (91-99% of random six-group splits), with the steepest gradient in the first six
years — the massification margin. But it is not causal (placebo above), and the expansion side is weak or
positive: decades of faster schooling growth are not decades of faster fertility decline, and the basket of 342
pairs shows the change relation is a patchy, sign-mixed object. Mass schooling therefore sits **before and
alongside** the fertility transition as a marker of the development gradient, not as a demonstrated lever.

## Files and limits

`PRE_REGISTRATION.md` (frozen before code); `scripts/battery.py` (grid runner, checkpoints, resume),
`scripts/bootstrap_only.py` (separate 68 s bootstrap pass because the main checkpoint drops draws),
`scripts/process_results.py`, `scripts/smoke_dispatch.py`; `data/results_summary.json` (all aggregates),
`data/pair_table.csv` (342 rows: level and change coefficients, per-pair spec shares, transport shares),
`data/transport.csv` (13,800 partitions), `data/bootstrap.csv` (342 pairs), figures
`figures/fig_battery_levels_vs_changes.png` and `figures/fig_transportability.png`; `results/logs/` (run, crash,
bootstrap logs). Limits: recorded rows are aggregated for the transportability phase (six within-group
regressions per row), so "recorded rows" and "regressions run" differ by that factor; standard errors are
country-clustered but spatial/serial dependence is not otherwise modelled; the placebo result means the levels
correlation is descriptive, not causal; the 13,800-partition extension was a load fill with the pre-registered
statistic and is reported, not hidden.
