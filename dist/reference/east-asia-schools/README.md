# School and teacher futures, 2025–2050

Unzip and double-click **index.html** in a current browser on Windows or Mac. The page runs offline without installation. To put it on an existing site, copy **index.html** and **city-networks.html** into the same directory on that site and link to the first file. The second file contains the Hong Kong and Guangzhou district, cohort and school-plan views. The source and CSV files are for audit and replication.

## What to try

- Pick **South Korea → Primary**. The latest approved training intake is 3,390 places. At a four-year lag, the lower intake reaches the qualifying pool in 2029. With the default 85% qualification rate and 80% application rate, that is about 2,306 new applicants against 2,500–2,800 planned public appointments per year in 2029 and 2030. The appointment process also draws on previous cohorts. Published appointment ranges are separate columns in the table and CSV.
- Choose **Enrollment-only reference** for Korean primary. Directly scaling teacher posts with enrollment produces zero openings in years covered by the published plan. The regular reference instead uses a minimum number of entrant openings based on the 2026 and 2027 recruitment announcements and the midpoint of each 2028–30 planned range. The minimum tapers to zero by 2034. That transition is an assumption. The first gap in 2031 depends on it. It disappears in 2031 if the published 2030 range continues, given the same training assumptions.
- Pick **Hong Kong → Primary + secondary**. Using the observed departure rates, the default reference has about 40,800 teachers in 2050/51 and zero modeled layoffs. Selective retention has about 44,500. These scenarios use the same projected pupils. EDB provisionally reports 461 full-time and 1,439 part-time subsidized PGDE admissions for primary and secondary combined in 2025/26. The default pipeline models the full-time group alone. BEd and other routes are outside that series. EDB says its part-time expansion helps already-employed teachers qualify. The chart separately marks 2,136 provisional first-time primary and secondary hires in 2025/26. The model cannot infer total new supply from that evidence.
- Pick **Taiwan → Primary**. Training inputs use roughly 2,300 regular approved places annually plus about 168 additional approvals for 2025/26. Targeted post-baccalaureate routes are separate. The ministry reported 3,108 public regular primary openings in 2025/26, with 2,833 candidates selected by late July. The nationwide applicant scenario pools vacancies across locations and subjects. Use the official recruitment benchmark when interpreting the first simulated gap.
- Use **Cut remaining posts to target** and vary exits to see when the scenario produces involuntary separations. The annual difference between employed staff and the target with cuts off indicates pressure on incumbents. A gap for new applicants is a different measure. The model does not carry unmatched applicants into the next year.
- The country birth slider shifts births relative to the UN medium projection from the 2027 birth cohort. The first effect appears at preschool ages in 2030, primary in 2033, lower secondary in 2039 and upper secondary in 2042. Hong Kong instead uses a count of annual births after the near-term EDB anchors. Guangzhou uses a long-run preschool demand growth assumption that also includes participation and migration.

## Model scope

| System | Enrollment and workforce | Training |
|---|---|---|
| Hong Kong | Kindergarten, primary and secondary, with combined primary plus secondary view | Partial combined full-time PGDE route, with custom input for other stages |
| Japan | Ordinary primary and lower secondary | Custom intake, plus published public appointments as historical context |
| South Korea | Primary and lower secondary | Approved primary places, published primary recruitment announcements and plan |
| Taiwan | Primary operations and dedicated lower secondary schools | Approximate regular primary approvals |
| Thailand | Primary and all secondary, with lower and upper secondary populations shown separately | Custom intake |
| Guangzhou | Kindergarten, primary, junior secondary and general senior high | Custom intake |

The four national models use actual 2025 education counts and UN age bands. Age-based enrollment paths hold relative participation and coverage constant. Their enrollment checks roll a one-year projection from the preceding observed year and compare it with persistence. For primary, the age method had 0.36% error in Japan, 0.47% in Korea, 0.11% in Taiwan and 0.91% in Thailand, using one, one, four and three holdout years respectively. These are retrospective checks against one UN release. Teacher hiring and layoffs need separate validation. The published Korean plan provides a near-term policy benchmark. For Taiwan and Japan, recent public recruitment provides historical context.

Country school operations are capacity scenarios and need district data to predict closures. Thailand has no matched national operations series in the dashboard. A teacher headcount and a class count are different measures. The optional cost input gives modeled payroll in local currency. Estimates of learning and student sorting would need additional data. The city network document gives the geography, class rules and validation behind those two models.

## Rebuild and check

Run these from the extracted directory if you want to rebuild the page.

```sh
python3 source/build.py index.html
node source/check.cjs index.html
node source/city/check.cjs city-networks.html
```

The WPP age slice is included. To reproduce it from the two official single-age medium CSV files, pass their directory and the desired output file to `python3 source/prepare_population.py`. The filename periods are 1950–2023 and 2024–2100. Sources for school records and training parameters are linked in the dashboard and recorded in `source/systems.json`. The current page uses deterministic scenarios.
