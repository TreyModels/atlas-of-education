# Claims-to-source map — Paper N3

Every number in `paper.md` that comes from a record is mapped here to **branch @ commit hash → file → field or line**. The source branches are pushed to the repository; the hashes are the commits named in the task. A reader who checks out a branch at the hash finds the file exactly. Numbers not listed here are qualitative statements or definitions.

Source key:
- **S1** = `research/subsistence-2026-11-23` @ `41f6429`
- **S2** = `research/subsistence-v2-2026-11-23` @ `ce66cfc`
- **S3** = `research/supply-demand-2026-11-23` @ `963e5e5`

Paths below are relative to each branch root.

## Section 2 — replication

| Paper statement | Source | File | Field / location |
|---|---|---|---|
| Elasticity capital-labour 2005 = 1.24 (SE 0.08) | S1 | `research/records/2026-11-23-subsistence/results/replication.json` | `sigma_k_l_2005` = [1.2354, 0.0773] |
| Elasticity intermediates-labour 2005 = 1.11 (0.08) | S1 | same | `sigma_m_l_2005` = [1.1138, 0.0840] |
| Elasticity capital-labour 2015 = 1.40 (0.07) | S1 | same | `sigma_k_l_2015` = [1.3981, 0.0737] |
| Elasticity intermediates-labour 2015 = 1.27 (0.07) | S1 | same | `sigma_m_l_2015` = [1.2698, 0.0733] |
| Extremes 1.73 / 1.76 (2005); 1.73 / 1.64 (2015) | S1 | `.../results/replication.txt` | "same elasticity from the development extremes" lines |
| 570× / 637× (2005); 557× / 394× (2015) | S1 | same | "observed intensification" lines |
| Input share 55-69% | S1 | `.../results/replication.json` and `replication.txt` | `usda_input_share_2005` 0.5499; `input_share_2005_paper-` 0.6945; 2015 0.6137 / 0.6860; decomposition lines in txt (3.32 log points = 69%, USDA 2.63 = 55%) |
| Gap 4.78 log points, ratio 118.8× (2005); 4.80, 121.8× (2015) | S1 | `.../results/replication.txt` | "log agricultural labour-productivity gap" lines |
| T2a: −1.13 (0.15), n=126; −1.28 (0.11), n=128 | S1 | `.../results/corrected_test.txt` | "T2a cross-section 2005/2015" lines (not in the JSON) |
| T2a2: intensity −4.71 (0.89), price +1.11 (2.23), income −7.32 (2.07), n=126 | S1 | `.../results/corrected_test.txt` | "T2a2 cross-section 2005" line |
| T2a2: intensity −4.38 (1.15), price +4.02 (3.40), income −4.12 (2.31), n=128 | S1 | same | "T2a2 cross-section 2015" line |
| Panel: 507 country-year observations, 128 countries, 1995-2010 | S1 | same | "panel for the ten-year changes" line |
| T2b: +1.7471 (0.7082), price +0.8155 (0.3220), n=503 | S1 | `.../results/corrected_test.json` | `"T2b: change in ag employment share t->t+10..."` → `log_intensity`, `relprice`, `n` |
| Reverse check: intensity −3.320 (0.702), price −1.092 (0.374), n=383 | S1 | `.../results/corrected_test.txt` | "reverse check" line (not in the JSON) |
| T2b(a): −0.0022 (0.0636), n=503 | S1 | `.../results/corrected_test.json` | `"T2b(a): change in intensity t->t+10 on relative input price(t)"` → `relprice`, `n` |
| T2b(b): +0.0122 (0.0348), n=376 | S1 | same | `"T2b(b)..."` → `d_relprice_f10`, `n` |
| T2b(c): −0.0440 (0.3778), +0.3549 (0.3856), −0.5298 (0.1006), n=472 | S1 | same | `"T2b(c)..."` → `d_logint_past`, `d_relprice_past`, `ag_share`, `n` |
| Long difference 1995-2015: −0.757 (0.871), +0.181 (0.897), −0.193 (0.052), +0.305 (0.748), n=124 | S1 | `.../results/corrected_test.txt` | "T2b long difference 1995->2015" lines |
| T2c secondary: −0.1621 (0.2454), −1.1842 (3.1981), n=278 | S1 | `.../results/corrected_test.json` | `"T2c: change in secondary completion..."` → `d_ag_f10`, `log_intensity`, `n` |
| T2c fertility: −0.0003 (0.0058), −0.0047 (0.0500), n=503 | S1 | same | `"T2c: change in fertility..."` → `d_ag_f10`, `log_intensity`, `n` |
| MDE about 0.016 births | S1 | `research/records/2026-11-23-subsistence/README.md` | §3 T2c paragraph ("a fertility change of ~0.016 births would have been detected") |
| USDA panel: 182 countries, 1961-2023; WDI 207,622 rows | S1 | same README | §1 "Data question" paragraph |

## Section 4 — sequencing

| Paper statement | Source | File | Field / location |
|---|---|---|---|
| 64 countries with all three events | S2 | `research/records/2026-11-23-subsistence-v2/results/sequencing.json` | `countries_with_all_events` = 64 |
| Schooling before release 61/64 = 95% | S2 | `.../results/sequencing.txt` | "countries where schooling precedes release: 61 of 64" + country list |
| Release before schooling 5% (3/64), CI [0,11] | S2 | `.../results/sequencing.json`; `sequencing.txt` | `pct_release_before_schooling` = 4.6875; bootstrap lines |
| Schooling before fertility 69%, CI [58,80] | S2 | same | `pct_schooling_before_fertility` = 68.75; bootstrap lines |
| Release before fertility 6%, CI [0,11] | S2 | same | `pct_release_before_fertility` = 6.25 |
| Median gap release→schooling −26 years, CI [−26,−22] | S2 | `.../results/sequencing.txt` | "median gap release->schooling: -26 years" + bootstrap line |
| 180 countries with data | S2 | `.../results/sequencing.txt` | "countries with data: 180" |
| US order 1910 / 1955 / 1957 | S2 | `.../results/sequencing.json` | `us.farm_onset`=1910, `us.schooling_onset`=1955, `us.fertility_onset`=1957 |
| Supply before schooling 28.09%, CI [19,37] | S3 | `research/records/2026-11-23-supply-demand/results/supply_demand.json`; `supply_demand.txt` | `supply_before_schooling_pct` = 28.0899; bootstrap line |
| Demand before schooling 73.03%, CI [64,82] | S3 | same | `demand_before_schooling_pct` = 73.0337; bootstrap line |
| Supply-before-demand CI [19,38] | S3 | `.../results/supply_demand.txt` | C1 bootstrap line |
| 108 schooling dates, 97 demand onsets, 89 both | S3 | `.../results/supply_demand.txt` | C1 first line |
| 61 of 108 schooling take-offs at the 1965 boundary; supply data start 1975 | S3 | `.../results/supply_demand.txt` | C1b lines |
| Fair sample 33 countries: supply 76%, demand 79%, supply-before-demand 39%, median gaps −5 / −10 | S3 | `.../results/supply_demand.txt` | C1b "fair-comparison sample" lines |
| Labour-market-only demand precedes schooling in 7% of 58 countries | S3 | `.../results/supply_demand.txt` | C1b line "demand measured only by wage-premium and paid-employment..." |
| Composite supply +0.4563 (0.1739), demand +0.0065 (0.2033), n=78, 51 countries | S3 | `.../results/supply_demand.json` | `event_ordering.composite.supply/demand/n` |
| Education spending +0.1250 (0.0583); enrolment +0.3071 (0.1459); pupil-teacher +0.0981 (0.1016) | S3 | same | `event_ordering["horse race"].d_supply_spend`, `d_supply_ger`, `d_supply_ptr` |
| Wage premium −0.2088 (0.1143); paid employment +0.0509 (0.1167); urbanisation −0.0486 (0.0962); income +0.1398 (0.1358) | S3 | same | `event_ordering["horse race"].d_demand_prem`, `d_demand_wage`, `d_demand_urban`, `d_demand_gdp` |
| Supply-only n=116, 62 countries; demand-only n=300, 103 countries | S3 | same; `supply_demand.txt` | `event_ordering["supply only"].n`, `["demand only"].n`; C2 lines |
| Cross-tab 3 / 43 / 22 / 21 | S3 | `.../results/supply_demand.txt` | C1 "cross-tab" line |

## Section 5 — model

| Paper statement | Source | File | Field / location |
|---|---|---|---|
| Five free parameters 4.8666 / 0.0209 / 0.0452 / 0.4091 / 28.8340 | S2 | `research/records/2026-11-23-subsistence-v2/results/model_v2_params.json`; `model_v2_summary.txt` | `params.lam_q`, `gJ`, `gA`, `eps_food`, `mort`; summary parameter block |
| N0 = 3.18, kappa = 0.124, sigma = 1.5 | S2 | same | `calibrated.N0`, `calibrated.kappa`, `estimated.sigma` |
| Fit 1960/2000/2020 (ag share, TFR, schooling, population) | S2 | `.../results/model_v2_summary.txt` | "repair check" table rows 1960, 2000, 2020 |
| Recovery errors 2.500 / 0.016 / 0.000 / 0.002 / 2.543 | S2 | `.../results/model_v2_summary.txt` | "parameter recovery test" block |
| Counterfactuals 2020: baseline 17.6 / 7.5 / 2.35 / 1.58; freeze mechanisation 39.9 / 0.2 / 3.29 / 2.19; freeze pipeline 18.0 / 3.0 / 2.94 / 1.90; freeze mortality 18.4 / 7.2 / 3.96 / 0.39 | S2 | `.../results/model_v2_summary.txt`; frozen-mechanisation path in `.../results/model_v2_counterfactual.csv` | "counterfactuals in 2020" block; CSV 2020 row (`cf_ag_share` 0.3990, `cf_school` 0.2400, `cf_tfr` 3.2931, `cf_pop` 1.1031) |
| v1 values: 2020 ag share 8.1 vs 19.44; population 4.43 vs 2.92; v1 freeze-mechanisation 17.9 / 5.6 / 2.52 | S1 | `research/records/2026-11-23-subsistence/results/model_summary.txt` | "model vs data" table and counterfactual block |
| v1 parameters 3.605 / 0.00 / 0.017; v1 constants | S1 | `.../results/model_params.json`; `model_summary.txt` | `params.lam_q`, `lam_r`, `gJ`; `constants` block |

## Statements that are not numbers

- The BKKM mechanism description, the Lewis-Kuznets narrative, the world-polity and human-capital-before-industry literature, the policy implications, and the future-research designs are qualitative and cited to `refs.md`.
- "We are not aware" statements and the closest-competitor naming are in `claims-prior-art.md`, with the search strategy recorded there.
- The earlier project proxy test is described qualitatively in `paper.md` §2.4; the numbers behind it are in the project's handoff record (not restated here).
