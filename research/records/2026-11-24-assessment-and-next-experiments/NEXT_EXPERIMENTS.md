# Next experiments (for DeepSeek, and anyone else, to run)

Rules for every experiment (see also README.md):
1. Write `PRE_REGISTRATION.md` (question, data, specification, decision rule) in the new record directory **before** running; commit it first.
2. Put work in `research/records/<date>-<topic>/{scripts,results,data}` on a **new branch** `research/<topic>-<date>`. Never push to, force-push, or rewrite an existing branch.
3. Report every outcome, including nulls and failures. Save raw outputs and logs. Record the git commit of the code and the sha256 of inputs.
4. Recompute any number you quote from a paper or review before using it; cite the file it came from.
5. `python3 -I`, pinned versions in `requirements.txt`; seed every random draw; write the seed in the output.
6. Estimates are associations unless the design is an event study with checked pre-trends; say so.

Priority: **P1** decides whether a paper is submittable; **P2** strengthens; **P3** new ideas. "Runtime" is for 8 CPU cores unless stated.

---
## Methods paper (Paper 4)

### E1 [P1] Push the grouping multiverse to >= 1,200 random draws
- Why: the Benjamini-Yekutieli threshold for the cluster of ~30 links needs ~1,120 draws; the paper certifies at 400 under BH only.
- Code: `research/records/2026-11-23-grouping-multiverse-400/scripts/{gm_core.py,run_multiverse400.py,analyse400.py,determinism_check.py}` (branch `research/grouping-multiverse-400-2026-11-23`). Data directory set by env var `GM_DATA`.
- **Prerequisite E0:** confirm the panel for `GM_DATA` exists (the methods paper says the panel is not in the repo). The 22 Nov series in `data/` of this record are a subset (10 series) and are *not* enough. Rebuild from `research/records/2026-11-23-corr-rebuild/data/RAW_SOURCES.md` + `scripts/download_raw.sh`, or ask the owner for the panel. Record which.
- Run: replicates seeded 1000+r (r = 0..1199 so the first 400 reproduce the existing run exactly); run `determinism_check.py` first; keep per-replicate wall times.
- Decision rule: report, for every one of the 272 links, the verdict at R = 74, 400, 800, 1,200 under BH and BY. A link "survives" if its verdict is unchanged at 1,200 under BY. Report the split-halves agreement at 1,200 (two disjoint 600s).
- Runtime: ~3 h on 16 cores (about 6 h on 8). Output: `results/summary1200.txt`, `verdict_by_R.csv`.

### E2 [P1] Known-truth simulation with the real estimator
- Why: the simplified simulation in this record (`scripts/known_truth_sim.py`) uses per-country sufficient statistics, 8 groupings, 150 countries, 50 years. The paper needs it with the real code, 50 groupings, the real panel's missingness.
- Method: generate panels with the regimes in `known_truth_sim.py` (A uniform, W weak uniform, B planted in one tercile of one grouping family, C null, D null with shared trends, S sign-split), but with the real panel's country set, missingness mask and grouping variables; run `gm_core` verdicts at R = 74, 400, 1,200; 200 replicates per regime.
- Decision rule: report type-I error per verdict (target <= 5%), power for A/B/S, and the share of regime-B replicates labelled "robust everywhere". Freeze the design before running; do not tune effect sizes after seeing verdicts.
- Benchmarks from this record (v2 rules, simplified estimator, 100 replicates): A robust 100% at every R; B labelled robust 85%; planted tag detected 0/6/49% at R = 25/100/400; null false positives 0-2%; S detected 0/99/100%.

### E3 [P1] Heterogeneity condition on the real verdicts
- Add to the robust-everywhere rule: the real heterogeneity rate (share of groupings whose group-specific estimates are jointly heterogeneous at 5%, already computed) must not exceed the 95th percentile of the random-draw heterogeneity rate. Re-label the 272 links.
- Decision rule: if >= 2 of the 5 links that "travel" lose the label, rewrite Section 5.3; otherwise report the count and keep it.
- Also run the "always report group-specific tags even when robust" variant and count links that are both.
- Runtime: minutes (post-processing of E1 outputs).

### E4 [P2] Imputed-panel sensitivity
- Branches `research/imputed-matrix-2026-11-23`, `research/imputed-panel-2026-11-23`. Re-run the 74-draw verdicts on the imputed panel; report verdict agreement (Cohen's kappa) with the observed panel and list links whose verdict changes.
- Decision rule: kappa >= 0.8 -> the 161-link null remainder is not a missingness artefact; below that, report it as a limitation.

### E5 [P2] Minimum detectable effects for every null in the project
- For each reported null compute the smallest effect detectable at 80% power and 5% (2.8 x SE for a two-sided test with the reported clustered SE), in the outcome's natural units; build one table (farm decline -> fertility 0.016 births; care work; credential gap; marriage; mortality volatility; pronatalist policy).
- Decision rule: a null is "power-calibrated" only if the MDE is smaller than the smallest effect the theory in question would call substantively relevant; state that threshold in advance.

---
## Sequencing paper (Paper 1)

### E6 [P1] Redesign the demand-timing test
- Why: the "7%" statistic is an artefact of 1991 start dates (CLAIMS_LEDGER B6).
- Use demand proxies that exist before 1990: non-agricultural employment share and sectoral value added from the GGDC 10-Sector Database / Penn World Table (1950+, ~40 countries), urbanisation (WDI, 1960+), industry value-added share (WDI, ~1960+), agricultural value-added share (WDI 1960+, median start 1981).
- Method: date a demand take-off for each proxy with a stated threshold (e.g., +3 percentage points in 10 years), compare with the schooling take-off date as in `research/records/2026-11-25-paper-sequencing-novel/scripts/sequencing_stats.py` (branch `fix/sequencing-censoring-2026-11-24`) (classify both-exact / censored), and report the full classification table, not a single percentage.
- Decision rule: if demand precedes schooling in more than a third of identifiable countries, soften Paper 1's supply-led framing to "schooling and structural change move together"; if fewer than 15%, the claim can be restated with the new numbers.

### E7 [P1] Threshold and window sweep for the 31/34 result
- Vary the schooling take-off threshold (three levels), the agricultural-release threshold (2, 3, 5 percentage points), the smoothing window (3, 5, 7 years) and the common window (1960-2010, 1965-2010, 1970-2015). Recompute classify() each time.
- Output: a 3x3x3x3 table of (forward, reverse, undetermined). Decision rule: report the range of the forward share among identifiable countries; if it falls below 75% in any cell with >= 20 identifiable countries, flag it as threshold-sensitive in the abstract.

### E8 [P1] Fee-abolition event study, verified and robust to staggered timing
- Dates: verify the 12 in `research/records/2026-11-22-massification-panel/scripts/final_tests.py` against primary sources (ministry decrees, World Bank/UNICEF 2009 *Abolishing School Fees in Africa*, SFAI country notes). Conflicts to resolve: Cameroon 1999/2000, Ghana 1997/2005, Ethiopia 1994/1995, Tanzania 2001/2003, Malawi 1994/1995, Mozambique 2004/2005. Store a table `fee_dates.csv` with source and page for each.
- Estimator: replace two-way fixed effects with a heterogeneity-robust estimator (Callaway-Sant'Anna with not-yet-treated controls, and Sun-Abraham); keep TWFE as the comparison.
- Outcomes: primary GER (SE.PRM.ENRR), then lower-secondary GER and primary completion at t+5..t+10 (does primary expansion feed later secondary take-off? this is the sequencing link).
- Sensitivity: +/-1 year on every date; leave-one-country-out; placebo dates 6 years earlier.
- Decision rule: the first-stage claim (+20 points, no pre-trend) is kept only if it survives the robust estimator and +/-1-year shifts.

### E9 [P2] Historical sequence cases with reproducible series
- Replace literature-standard dates for Prussia/Germany, France, Britain, Sweden, the US and Japan with series from Clio Infra (literacy, enrolment), Lee & Lee (2016) enrolment, GGDC / Maddison sectoral shares. Report schooling and agricultural-release dates with the series used.
- Decision rule: the 40-90-year British demand-led gap is kept only if both dates come from a stated series.

### E10 [P2] Reconcile "schooling follows fertility by 18 years" with schooling-first (B9)
- Compute, on one event table, the lag between schooling take-off, 6-year-schooling attainment milestone, and fertility decline onset, for the same 64 countries. Explain the sign difference between take-off timing and attainment timing.
- Output: one table and a paragraph for Paper 1 and Paper 2.

---
## Fertility audit (Paper 2)

### E11 [P1] Change-on-change placebo ladder on the battery panel
- Panel from `research/records/2026-11-23-corr-battery` (raw data via `corr-rebuild/scripts/download_raw.sh`). For each of the 8 schooling indicators run, in one table: F(t) on S(t); on S(t+10); on both; and dF(t,t+10) on dS(t-10,t), dS(t,t+10), dS(t+10,t+20), with and without country trends, with country-clustered SEs. The 22 Nov quick version is `scripts/placebo_orthogonal.py`.
- Decision rule (pre-register): if the lead term (S(t+10) or dS(t+10,t+20)) is at least 80% of the lag term in more than half of indicators, the paper says "development gradient / co-trending"; if the lag term is at least twice the lead term in more than half, say "temporal asymmetry present, causal reading still untested".

### E12 [P2] Stratified DHS check (public API, no login)
- Use the DHS STATcompiler / API to pull TFR by woman's education x residence x wealth quintile for all surveys 1990-2022. Test whether the education gradient and its cohort attenuation survive within urban/rural and wealth strata.
- Decision rule: if the gradient halves or more within strata, composition (who is educated) explains much of the macro gradient; report both.

### E13 [P3] Direction test
- Granger-type test with 5- and 10-year lags in a dynamic panel (Arellano-Bond or long-difference): does lagged schooling change predict fertility change better than lagged fertility change predicts schooling change? Report both directions and the difference in explained variance.

---
## Shape paper (Paper 3)

### E14 [P1] Complete pre-1960 transitions
- Public long-run TFR (Human Fertility Database, Our World in Data, Chesnais 1992; Sweden, France, England & Wales, US, Japan, Denmark, Netherlands, plus any with plateaus before onset). Fit the parametric forms used in `research/records/2026-11-25-paper-shape/scripts/analysis.py` (branch `fix/n4-shape-2026-11-24`; includes logistic, Gompertz and exponential-to-floor) on full transitions; rank by BIC and rolling-origin hold-out RMSE.
- Decision rule: if logistic still loses on full transitions, the paper's functional-form claim extends beyond the censored window; if it wins or ties, the paper must say the 1960-2023 result is a property of the window.

### E15 [P1] The real rival: double-logistic
- Add the Alkema et al. (2011) double-logistic form (UN WPP) as a fifth model, on the same 105 countries and on UN WPP 2024 TFR for out-of-sample 2023-2024. Decision rule as above.

### E16 [P2] Does starting mortality survive controls?
- Add region fixed effects and the starting TFR level (1960) to `scripts/n4_gdp_mortality.py`; use leave-one-region-out. Decision rule: if starting mortality's coefficient on onset falls below twice its SE, describe it as a proxy for initial development, not a mortality effect.

---
## New experiments (open; take any)

### N1 Negative-control links in the multiverse
Add 30 links with no plausible mechanism (e.g., an outcome from one domain regressed on an unrelated driver) to the 272-link matrix; report their verdict distribution. Calibrates the false-positive rate of the verdict taxonomy on real data, not simulated data.

### N2 Time-shift luck test for mortality and income
The 22 Nov time-shift permutation test (20,000 worlds) was run for schooling -> fertility only. Run it for u5mr -> fertility, life expectancy -> fertility and gdppc -> urbanisation (the links that "travel"). Does shifting break them? If not, they are trends.

### N3 Hazard model for schooling take-off with censoring built in
Replace the 1965/1991 boundary rule by a survival model with left truncation: P(take-off in year t | not yet), covariates lagged. Compares with the event-date comparison and removes the "30 undetermined".

### N4 Event study around agricultural-price shocks
Use the fertiliser/relative-price series (`subsistence-v1/v2`) as a shock; estimate farm exit, wage jobs, births and *schooling* with lags (0-10 years). The existing result stops at fertility; does it reach schooling? This tests the only partial mechanism the project has.

### N5 Cohort-level check of the placebo
Use birth-cohort schooling (Barro-Lee, Lee-Lee) instead of period stocks so that "future schooling" is a different cohort, not the same cohort aged ten years. This removes much of the serial correlation.

### N6 Specification curve for Paper 1
Cross all choices (thresholds, windows, smoothers, country sets, series sources) in one specification curve for the forward share; report the median and the share of specifications above 75%.

### N7 Hold-out replication
Freeze all Paper 1 and Paper 2 specifications and run them on a country set that was never used (e.g., microstates and countries dropped for population < 1M, or post-2010 data) as a true out-of-sample check.

### N8 Reverse-case audit
Study the 3 countries where agricultural release came before the schooling take-off (AFG, KHM, SEN; MLI and MOZ in the 81-country sample) and, separately, the 4 release-before-fertility cases (AFG, LBR, MWI, ZMB): are they data errors, conflict, or a genuinely different path? A short country appendix.
