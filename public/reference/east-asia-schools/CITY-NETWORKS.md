# School Networks · Hong Kong and Guangzhou

Extract the ZIP and open **city-networks.html**. All data and code are embedded. No server is required. Both cities run through 2050/51, and the dashboard opens at that year. The year selector also covers every school year from 2026/27. Use the stage and metric controls to inspect schools, teachers and enrollment. The scenario CSV button exports the current assumptions' output.

## Hong Kong

The **published-policy reference** combines the Education Bureau's population projections and existing class rules with announced school plans. It is a reproducible reconstruction based on public material. EDB has not supplied a territory-wide schedule for the modeled school and teacher totals.

The 448 matched public primary profiles report 1,564 P1 classes in 2025/26 and 1,438 approved for 2026/27. The latest disposition record used here describes eight merger approvals in principle, two private P1 approvals, four wind-downs and one exemption among the 15 newly zero-intake schools. The model treats Fresh Fish Traders' 2026/27 merger as one fewer standalone school. Three reported 2029/30 exits are incorporated. The other plans appear in a separate ledger with their reported status and no assumed exit date. The named subset is applied as a floor on net reductions. Its effects are already included in the simulated school totals. Reprovisioning and continuing campuses can change physical access independently of registered school operations.

The **selective retention** variant begins in 2027/28. It protects up to five additional operations per stage in the default, while preserving explicitly dated exits, and targets a 10% reduction in primary and secondary average class size relative to the reference, subject to room capacity. The room limit is a proxy based on 2025/26 classes per retained operation and 5% slack. Kindergarten protects at least 90% of baseline staffing when the retention rule applies. **Faster consolidation** responds sooner to spare capacity, operates with fewer classes, and permits forced separations when normal departures are insufficient.

All cases age the same cohorts through school. EDB age-six and age-twelve population inputs end in 2035. From 2036 onward, the age-six path moves over four years from the final official point toward the selected birth path. The default path assumes 30,000 births per year. The annual-change control can compound a sustained decline or recovery in future birth cohorts. The age-twelve path ages the earlier primary cohorts forward six years. The published district inputs end in 2031; intake shares remain fixed from that point. Grade-level primary approval differences in the matched public sample are applied to the 2025 all-sector anchor, holding other classes fixed at the 2026/27 anchor, and then followed with those cohorts. The model approximates the public secondary calculation basis increasing from 27 to 29 by cohort. Regular class-based staffing uses 1.6 posts per primary class and 1.8/2.1 for junior/senior secondary. Additional staffing is anchored to the observed all-sector 2025 headcount and scaled with enrollment and sites. The funding rules cover public schools. Their use as marginal ratios across sectors is a modeling approximation. Individual merger teacher protections, redeployment, vacancies by subject, age-specific retirement and class eligibility exceptions require finer data.

### Default results

Observed 2025/26 operations were **958 kindergartens, 591 primaries and 513 secondaries**, with **67,315 teachers** across the three stages. Kindergarten and ordinary day schools are covered. The same building can contain more than one stage, so summed operations are not unique physical campuses.

| Year and policy | Kindergartens | Primaries | Secondaries | Teachers employed | Change vs. 2025/26 |
|---|---:|---:|---:|---:|---:|
| 2031/32 published-policy reference | 887 | 587 | 512 | 58,671 | −8,644 |
| 2031/32 selective retention | 892 | 587 | 513 | 64,061 | −3,254 |
| 2031/32 faster consolidation | 800 | 550 | 511 | 56,203 | −11,112 |
| 2035/36 published-policy reference | 887 | 582 | 508 | 56,479 | −10,836 |
| 2035/36 selective retention | 892 | 587 | 513 | 61,555 | −5,760 |
| 2035/36 faster consolidation | 797 | 498 | 485 | 53,844 | −13,471 |
| 2040/41 published-policy reference | 887 | 565 | 480 | 53,060 | −14,255 |
| 2040/41 selective retention | 892 | 570 | 485 | 57,853 | −9,462 |
| 2040/41 faster consolidation | 797 | 464 | 410 | 50,320 | −16,995 |
| 2050/51 published-policy reference | 887 | 479 | 415 | 49,476 | −17,839 |
| 2050/51 selective retention | 892 | 484 | 420 | 54,013 | −13,302 |
| 2050/51 faster consolidation | 797 | 385 | 334 | 46,845 | −20,470 |

Form 1 intake climbs from **32,370 in 2035/36 to 40,181 in 2040/41** in the reference. Total secondary enrollment still falls from **257,295 to 224,576** while earlier cohorts leave. At 20,000 versus 40,000 annual births, modeled primary enrollment in 2040/41 ranges from roughly 166,000 to 236,000. Those younger cohorts have yet to reach secondary school by the horizon, so the corresponding secondary path is the same.

From 2040/41 to 2050/51, Hong Kong's default primary enrollment falls from **201,022 to 180,288** and secondary enrollment falls from **224,576 to 182,767**. Primary enrollment settles by the mid-2040s at constant births. Secondary enrollment still falls in the last year of the run. In the scenario where annual births keep falling 3% from the same starting level, 2050/51 secondary enrollment is **141,680**.

The default reference still requires **3,459 hires in 2031/32**, including replacement hiring. Headcount reductions in the default run are absorbed through departures and lower replacement hiring. In a stress test with 35% of the observed 2025/26 departure rates, faster consolidation produces 311 simulated forced secondary separations in 2035/36. That is a stress case. The model contains no evidence of an EDB layoff plan.

The rolling historical enrollment model achieved 2.20% weighted error versus 3.16% for holding enrollment flat. The new workforce arithmetic achieved 1.04% versus 1.80% for a fixed pupil–teacher ratio using the same forecast enrollment. Historical school-count changes had 3.44 operations mean absolute error versus 6.22 for assuming no change. Those closure scores come from the earlier model under historical conditions. No test of the latest published merger rules over a completed period was possible.

## Guangzhou

The first pass uses six local education bulletins and a different school structure. It reconstructs the primary, junior secondary and general senior-high cohorts from local intakes. Kindergarten follows a separately adjustable growth path. From 2032 to 2036 its growth rate moves toward the chosen long-run value, which defaults to zero. The reference maps demand into school operations and teacher requirements. Retention protects 2025 sites and staffing, and faster adjustment scales these stocks more strongly. No Hong Kong staffing, admissions or departure parameters are carried over.

In the default reference, primary enrollment goes from **1.34m in 2025 to 1.06m in 2031**, while junior secondary enrollment rises from **542,000 to 712,000**. The junior increase is particularly sensitive to the larger 2023 primary intake moving into junior secondary around 2029. Guangzhou's published 2026 work plan calls for 50,000 additional public basic-education places, including 15,000 general senior-high places, and at least 10,000 additional senior-high admissions. That plan is displayed alongside the results and is not converted into site or teacher totals.

Looking further, the default run peaks at **about 712,000 junior secondary pupils in 2031 and 365,000 general senior-high pupils in 2034**. By 2040 those levels fall to **438,000 and 247,000**, respectively. The model's primary, junior and senior peak years match those reported by Guangzhou’s chief education inspector in 2025. The agreement concerns timing; post-peak levels come from the scenario. A long-run preschool growth assumption of −3% versus +2% a year changes 2040 primary enrollment from roughly 774,000 to 925,000. [Published Guangzhou peak-year estimates](https://www.cse.edu.cn/index/detail.html?category=179&id=4485).

In 2050/51 the default run has **861,000 primary, 425,000 junior secondary and 218,000 general senior-high pupils**, rounded to the nearest thousand. Those stages level off by the late 2040s because preschool enrollment stabilizes in the default. With sustained 3% annual preschool shrinkage, modeled 2050/51 enrollment is about **571,000, 323,000 and 182,000**, respectively.

Across the four stages, rolling enrollment forecasts for 2023–2025 produced 4.08% weighted error versus 5.70% for persistence. The school-count rule performed slightly worse than persistence, 1.51% versus 1.45%. The teacher-count rule reached 3.06% versus 4.47% on the same short test. The model is suitable for comparing pressure across stages. District school capacity, staffing departures, the split between public and private providers, and future plans at individual schools need additional data. Many bulletin counts are reported in units of 10,000 to two decimals, so the derived estimates are approximate.

## Reproduce and audit

From the extracted folder:

- `node source/city/check.cjs city-networks.html` checks school-plan reconciliation, scenario invariants, workforce flows and interface logic.
- `node source/city/results.cjs city-results` recreates the scenario, approval and backtest CSVs.
- `python3 source/city/build.py city-networks.html` rebuilds the offline dashboard.

The bundled `city-results/2050_demand_sensitivities.csv` records the alternative 2050 birth and preschool-demand runs. These runs vary demographic inputs and provide sensitivity estimates.

The normalized data are included in `source/city/`. The interface and `plans.json` and `guangzhou.json` link to the specific official bulletins and reported decisions used. References reflect material available by 9 November 2026. Historical rows use the latest source vintages available when assembled.
