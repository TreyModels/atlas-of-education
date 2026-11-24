# Pre-registration — Q2: country pathway comparisons

**Task:** Q2 of the Codex handoff ("Do similar starting countries take different educational, labour and
fertility pathways?"). **Owner:** panel-matrix. **Branch:** `research/q2-pathways-2026-11-25`.
**Record:** `research/records/2026-11-25-q2-pathways/`. **Status:** committed before any analysis was run (the
smoke test below had not been run in this record when this file was committed).

## 1. Question and claim discipline

This is a **descriptive path-comparison exercise**, not a causal design. The question: among countries with
similar starting conditions in 1980, do subsequent 1990-2010 education, fertility and (where dated) labour
pathways diverge, and can a small number of matched pairs/triads be checked against independent historical
sources? The unit is the country pair or triad. The output is a description of paths plus a documented selection
process. **No causal inference will be drawn from time ordering, matching similarity, or outcome gaps.** Every
statement of the form "X led Y" is banned from the report; the report will say "the recorded series move in this
order", not "X caused Y". Ties, counterexamples and failed cases are published.

## 2. Inputs and provenance (fixed before analysis)

- **Panel:** `data/long_run_panel.csv`, copied verbatim from the Codex handoff bundle
  (`research/codex-handoff-run-2026-11-24`, record `research/records/2026-11-24-next-tests/data/`).
  **SHA-256 `cd30d7ea7beb77b63de092c53f9b143065b94651f1ac95535ac70eebb3280f2d`** (verified against the handoff
  letter's expected hash; 42,959 data rows, 180 countries, annual 1800-2023 with gaps).
  Columns: `iso3, year, child_mortality_per100, life_expectancy_years, effective_fertility,
  tfr_observed_1950plus, tfr_implied_derived, mean_years_schooling, gdp_pc_maddison_1990int, urban_share_pct,
  cm_source`.
- **Pair benchmark script:** `scripts/country_pairs.py`, copied verbatim from
  `research/records/2026-11-24-codex-handoff/scripts/`, SHA-256
  `fbc4fda4e7a82fe5d7740f3409f39ae2d2d310baae5e9e1ddf155433f6a2d51b`. Baseline features:
  `mean_years_schooling, tfr_observed_1950plus, gdp_pc_maddison_1990int (logged), urban_share_pct`; greedy
  disjoint Euclidean matching on baseline z-scores; baseline 1980, outcomes 1990-2010 changes.
- **Environment:** box `autodl3` (region-9), repo `/root/work/repo`, Python `/root/miniconda3/bin/python`
  (pandas 2.3.3, numpy 1.24.1), `OPENBLAS_NUM_THREADS=1`, deterministic. Local Python 3.12 with pandas 3.0.1 /
  numpy 2.3.5 used only for cross-checks; box is the reported environment.

## 3. Smoke test (reproduction check, run immediately after this commit)

Command (on box): `OPENBLAS_NUM_THREADS=1 /root/miniconda3/bin/python scripts/country_pairs.py --panel
data/long_run_panel.csv --baseline 1980 --start 1990 --end 2010 --out results/smoke`.

**Expected metadata (from the handoff letter): 105 baseline-complete countries, 52 disjoint pairs, 1 unpaired
country, 52 pairs with both 1990-2010 schooling and TFR changes.** We record the input SHA-256, script SHA-256,
raw meta JSON, pair list, stdout/stderr, run time and environment. Any deviation is reported, not patched to
match; if the numbers differ, the smoke test failed and the reason is investigated before any audit.

## 4. Audit plan (fixed before looking at outcomes)

### A. Baseline coverage and missingness
Table of 1980 baseline availability by feature (n present/absent, by region and income group), the four
complete-case counts at each filter step, the list of countries dropped and why (missing feature, GDP ≤ 0,
duplicate year), and a check that pair selection uses only 1980 features (no outcome information). Report the
selected 105 countries against the 180-country panel (what the selection over-represents); no reweighting claim.

### B. Distance metric and matching sensitivity (pre-specified alternatives)
Primary: greedy Euclidean on baseline z-scores (all four features), as in the benchmark.
Alternatives, all fixed here before results:
1. **Mahalanobis** distance (baseline covariance, regularised if singular).
2. **Manhattan** distance on baseline z-scores.
3. **Three-feature match** dropping `tfr_observed_1950plus` (to separate fertility-level matching from the
   other three features) - because the outcome includes TFR change.
4. **Optimal assignment**: Hungarian algorithm (`scipy.optimize.linear_sum_assignment`) on the full pairwise
   distance matrix with dummy columns at a large fixed cost, so all countries are matched or left unpaired;
   minimises total distance rather than greedy order.
For each: number of pairs, median baseline distance, overlap with the primary pair set, median absolute 1990-2010
schooling and TFR gaps, and Spearman correlation of gaps across matchings. **Descriptive only; no p-values used
to rank matchings.**

### C. Farming employment where dated
No invented earlier values. The panel has no agricultural employment column; we will use the project's dated
series only: `agricultural_employment_share` from the project panel if present in the local data on the box
(`/root/work/data`, WDI/ILO-modelled, usually 1960+ and often 1990+), joined by `iso3, year` with **no
backcasting, interpolation or extrapolation**. Report: year coverage per country; for pairs/triads where both
members have a 1990 and 2010 value, the change; otherwise mark **not dated** and do not estimate. Document
source file, hash, first/last year and missingness. If the local series cannot be found, the labour dimension is
reported as **not available** and no substitute is silently used.

### D. Random-matching comparison
1,000 random disjoint pairings of the same 105 baseline-complete countries (seed 71201), stratified only by the
primary greedy structure (same number of pairs, one unpaired). Compare the observed distribution of
(a) baseline distance and (b) absolute 1990-2010 schooling/TFR gaps with the random distribution: observed median
vs random median and 2.5-97.5 percentiles, and the share of random draws whose median is at least as large as
observed. This is a **yardstick**, not a significance test; no p-values claimed.

### E. Selection flow and holdout
A CONSORT-style flow: 180 panel countries → 1980 complete cases → GDP>0 → matched sample (105, 52 pairs,
1 unpaired) → pairs with both outcomes. For case checks, split the matched countries into two halves by baseline
distance rank (pairs alternating) and use hypotheses generated from half A only; choose case countries from half
B where they satisfy the case criteria. If a half-B case cannot be checked with independent sources, it is
reported as unattempted rather than replaced by a half-A case. The split is fixed here: even-ranked pairs = A,
odd-ranked = B (rank by primary baseline distance, ascending).

### F. Case selection (3-5 pairs/triads, criteria fixed before looking at outcomes)
From the matched pairs, choose, in this order:
1. **Divergent close pair**: among pairs with baseline distance below the median, the largest absolute summed
   outcome gap (schooling + TFR, standardised by the matched-sample SDs). Purpose: the clearest "similar start,
   different path".
2. **Convergent close pair**: among the same close pairs, the smallest summed gap. Purpose: a control against
   cherry-picking divergence.
3. **Divergent distant pair**: among pairs above the median baseline distance, the largest summed gap (a pair
   that is *not* closely matched) - published as a counterexample to the "similar start" frame.
4. **Triad**: one pair from (1) plus the nearest baseline neighbour of either member that is not already paired
   (or an existing pair whose four members form a triad); add only if all members are in the same half for the
   holdout rule; otherwise report as a pair.
5. **Counterexample/negative case**: a pair that the criteria predict should diverge (close baseline) but does
   not, or a case where the independent sources contradict the panel values; publish it with the contradiction.
Every selected case is reported, including failures; no case is dropped after inspection. Case checks against
independent historical sources: national statistical sources, World Bank/WDI, UNESCO, Maddison, and historical
literature fetched in-session; every number is labelled (panel value vs independent source value vs estimate),
with year, definition and source. If a source cannot be obtained, the case is labelled **unverified** and kept.

## 5. Outputs
`results/smoke/` (pairs, metadata, stdout), `results/audit_*.csv/json` (coverage, matching, random, farming),
`results/cases.csv` (selected cases and criteria values), `REPORT.md` (question, provenance, matching rules,
selection flow, case table, limitations, what this can/cannot support). All scripts and logs committed.

## 6. Pre-specified falsifiers / honest-null conditions
- **Smoke mismatch**: expected 105/52/1/52 not reproduced → report the deviation and stop interpreting benchmark
  numbers until explained.
- **Selection dominance**: if the 105 baseline-complete countries differ from the full panel by more than
  0.5 SD on any baseline feature (compared on the matched feature scales), the report says the sample is
  selected and does not generalise.
- **Matching fragility**: if the primary pair set overlaps <50% with at least two of the pre-specified
  alternatives, the report says the specific pairs are matching-dependent and only the audit is interpretable.
- **Random yardstick**: if random pairings have median outcome gaps at least as large as the observed matched
  pairs, the report says the matched sample does not show unusually large divergence.
- **Case contradiction**: if independent sources contradict the panel for any selected case, the contradiction is
  published and the panel value is not defended.
- **No causal inference**: any sentence in the report that implies causation from the ordering is a falsifier of
  this pre-registration; the report is revised before push.


## 8. Series labels (fixed before analysis)

The panel is a **reconstruction**, not a set of directly observed national series. Every series used will be
labelled in the report and case table:
- `tfr_observed_1950plus` - **observed** births-based total fertility where available for 1950 onward (UN/WPP
  vintage in the handoff); used as the benchmark TFR outcome, with gaps left missing.
- `effective_fertility` - **reconstructed/modelled** expected surviving children per woman; not a birth-based
  TFR and **not used as either outcome** in this exercise (Codex F01/F03).
- `mean_years_schooling` - **reconstructed** attainment stock (Barro-Lee/Wittgenstein-type series in the
  handoff), not observed enrolment.
- `gdp_pc_maddison_1990int` - **reconstructed** historical national-accounts estimate (Maddison), not observed
  income.
- `urban_share_pct` - **reconstructed** urban population share (WUP-type series), not observed.
- `child_mortality_per100`, `life_expectancy_years` - reconstructed historical series; not used as outcomes here.
- agricultural employment share (if found) - **model-identified** (ILO/WDI-modelled) series; recorded with its first
  and last dated year, never backcast.
Matching uses only baseline 1980 values of these reconstructed series; "similar baseline" means similar on these
reconstructions, not causal or historical identity, and matched pairs are not independent observations.

## 7. Deviations
Any deviation from this plan is recorded in `REPORT.md` under "Deviations" with the reason and the date, not
silently applied.
