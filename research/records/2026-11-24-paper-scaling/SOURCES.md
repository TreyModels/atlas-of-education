# Sources map — every number in the Paper M section draft

**Section author:** cuda-scale (task-33, folded into Paper M / task-37, led by panel-matrix).
**Draft file:** `SECTION-M-scaling-and-drivers.md`. Every number in it appears below with the
branch, commit, file and JSON key or line it came from. Nothing is quoted from memory.

## Scaling claims

| number in draft | value | source branch @ commit | file and location |
|---|---|---|---|
| rarefied Heaps exponent | 0.333 (SE 0.011), 151 countries, 11,712 points | `research/scaling-2026-11-23` @ `fd691a6` | `research/records/2026-11-23-scaling/results/scaling_results.json` → `sections.heaps` (`heaps_exponent`, `se`, `ncountries`, `npoints`) |
| raw distinct-category slope vs workforce | −0.002 | same | `scaling_results.json` → `sections.heaps.raw_count_vs_workforce_exponent`; also `README.md` §2 |
| z against literature 0.4 | −5.9 | same | `scaling_results.json` → `sections.heaps.test_vs_literature.z_0_4` |
| per-country Heaps median / IQR | 0.374 [0.319, 0.468] | same | `sections.heaps.per_country_median`, `per_country_iqr` |
| bootstrap Heaps (one curve/country, latest year) | 0.349, 95% CI 0.331–0.368, 151 countries, 1,208 points | same | `results/heaps_groups.json` → `overall` |
| θ/γ proxy groups (income) | 0.343–0.355, Kruskal H = 1.22, p = 0.75 | same | `results/heaps_groups.json` → `groups.income`, `heterogeneity.income_kruskal` |
| θ/γ proxy groups (region) | 0.281–0.400, H = 6.48, p = 0.26 | same | `results/heaps_groups.json` → `groups.region`, `heterogeneity.region_kruskal` |
| high-vs-low income difference | 0.010, 95% CI −0.043 to 0.062 | same | `results/heaps_groups.json` → `heterogeneity.high_vs_low_income` |
| curvature of accumulation curve | −0.0583 (SE 0.0018) | same | `results/regime_break.json` → `curvature.squared_coef`, `squared_se` |
| threshold split by attainment | 0.360 / 0.403 / 0.387; Welch t = −1.25, p = 0.22 | same | `results/regime_break.json` → `threshold_split` |
| within/between education exponents (table) | e.g. secondary GER 0.090 (0.124) within vs 0.215 (0.035) between | same | `results/consolidated_verdicts.csv`; local source table quoted in `research/records/2026-11-23-scaling/data/scaling_laws.csv` (copied from `/root/work/local_data/10_massification/relations/data/` at 23 Nov) |
| urbanisation–income logistic slope; n | 0.572 (SE 0.030), 10,986 country-years, 208 countries, midpoint $3,647 | same | `results/scaling_results.json` → `sections.urban_income` |
| out-of-sample RMSE (logistic/log-linear/power) | 0.1523 / 0.1532 / 0.1598 | same | `sections.urban_income.out_of_sample_rmse_share` |
| fertility–income power exponent | −0.263 (SE 0.013), n = 11,345, 213 countries; squared term +0.0178 (0.008) | same | `sections.fertility_income` |
| Wagner elasticity | 0.103 (SE 0.030), n = 4,699, 161 countries | same | `sections.wagner` |
| weak Mincer proxy elasticity | 0.378 (SE 0.027), n = 5,925, 202 countries | same | `sections.schooling_income` |
| collapse-curve fits and collapse metrics | 4,394 points / 158 countries; exponential a = 1.13 (0.26), b = 5.97 (0.23), decay 0.0197 (0.0025), R² = 0.78; country intercepts R² = 0.914; slopes R² = 0.955; F = 46.4 (313, 3,717 df); residual SD 0.847 (11.2% of range); 0.434 after rescale (R² = 0.942); country variance share 71.6%; low-income +0.40, high −0.11; 1950s +0.29, 1970s −0.17 | same | `results/scaling_results.json` → `sections.collapse` (all keys); values cross-checked in `README.md` §(1) Fertility |
| levels vs changes | between −0.479; within levels −0.299 (SE 0.026, t = −11.7); ten-year changes −0.056; 4,394 levels, 2,064 changes, 201 countries | same | `results/consolidated_verdicts.json` → `levels_vs_changes` |
| Zipf median exponent | 0.859, bootstrap 95% CI 0.746–0.978; 55 countries, 22,465 cities; Wilcoxon vs 1 p = 0.23; 27% within 0.8–1.2; pooled FE 0.386 (CI 0.293–0.677) | `research/scaling-data-hunt-2026-11-23` @ `9e15b6d` | `research/records/2026-11-23-scaling-data-hunt/results/zipf.json` |
| gravity PPML / OLS estimates | PPML FE distance −0.970 (SE 0.076); PPML no-FE distance −0.622 (0.149), sizes +0.456 (0.057) / +0.533 (0.114); OLS FE −1.306 (0.053); n = 8,020 pairs, 195 origins × 187 destinations | same | `results/gravity.json` → `ppml_fe`, `ppml_no_fe`, `ols_fe` |
| gravity integrity | pair matrix 282 million vs published 281 million; spot checks in `gravity.json` | same | `results/gravity.json` → `integrity` |
| blocked data sources and exact errors | WUP 404; UN Data Portal no city rows; BLS 403; Credential Engine 403; BEA 000 | same | `results/pull_log.json` → `attempts`; `README.md` data-availability table |
| data-availability verdicts for city output / credential counts | blocked | same | `results/pull_log.json`; `research/records/2026-11-23-scaling/README.md` §"What we could not test" |

## Massification-driver claims

| number in draft | value | source branch @ commit | file and location |
|---|---|---|---|
| links × groupings | 272 links; 50 real groupings in 8 families; 400 random re-partitions | `research/grouping-multiverse-400-2026-11-23` @ `1152cec` | `research/records/2026-11-23-grouping-multiverse-400/README.md` ("What was run"); `results/headline.json` |
| class counts | 5 robust everywhere; 76 group-specific; 30 beat random no clear group; 161 no better than random | same | README §Main results; `results/edge_table400.csv` |
| main-tier tests | 46 of 272 beat random with trends; 20 worse; 32 flips | same | README ¶"Bottom line"; `results/summary400.txt` |
| strict tier | 35 up and 19 down certified; 30 at the descriptive ceiling | same | README §RESOLUTION ANALYSIS; `results/headline.json` |
| resolution floor | 1/401; lone link needs 5,440 draws; cluster of 30 needs ≈182 | same | README §1–3 |
| electricity | zero whole-sample with trends; 11 of 32 links sign-flip more than random | same | README §(2) Massification "Electricity" |
| paid employment | no wage-employment link to a schooling outcome beats random in any group | same | README §(2) Massification "Paid jobs" |
| robust fertility links | child mortality → birth rate 95% of real groups vs random median 93%; life expectancy → 81% vs 93%; 2 links robust everywhere | same | README §(1) Fertility "Robust everywhere" |
| falsifiers | determinism bit-identical (3 replicates + real pass); 74-draw reproduction exact; halves p rank correlation 0.994; normal vs t 42 vs 46 | same | README §"Tests designed to kill these findings"; `results/determinism.txt`, `halves.csv` |

## Literature benchmarks

`claims-prior-art.md` lists the closest prior work per claim with Crossref verification status.
Crossref checks were run from the local clone on 24 Nov 2026 against `api.crossref.org`; raw responses
are in `results/doi_verified.json`, `results/doi_verified2.json`, `results/doi_batch3.json`. Books and
arXiv preprints have no Crossref DOI and are marked as such — they are not claimed as verified DOIs.
