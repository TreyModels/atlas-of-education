# Claims to source: every number in Paper N1

Format: claim → branch @ hash → record path → field or derivation. All files verified present at the hash.

| claim in the paper | source | field / derivation |
|---|---|---|
| 64 countries with all three dates | `research/subsistence-v2-2026-11-23` @ `ce66cfc` | `results/sequencing.json`, field `countries_with_all_events`; reproduced in `results/sequencing_stats.json` (`all_three.n`) |
| 61 of 64 schooling first (95.3%) | same | `results/sequencing.json` (`pct_release_before_schooling` = 4.6875 → 3 reverse, 61 forward); `results/sequencing.txt` line "countries where schooling precedes release: 61 of 64"; recomputed in `results/sequencing_stats.json` (`all_three.forward`, `.forward_pct`) |
| median lead 26 years | same | `results/sequencing.txt` ("median gap release->schooling: -26 years" under its schooling-minus-release convention); recomputed as `all_three.median_lead` = 26.0 |
| IQR 16.5-29.5 (17-29 rounded) | same | recomputed `all_three.q1`, `all_three.q3` from `results/event_dates.csv` |
| 93.4% of forward cases >10 years | same | recomputed `all_three.share_gt10` |
| 85.2% >15 years; 81.3% of the panel still forward after a +15-year error | same | recomputed `all_three.share_gt15`, `all_three.still_forward_after_plus15_*` |
| wider 81-country sample: 26-year median, 93.8% forward | same | recomputed `schooling_and_release` block |
| supply onset before schooling 28% (CI 19-37) | `research/supply-demand-2026-11-23` @ `963e5e5` | `results/supply_demand.txt` section C1 |
| demand onset before schooling 73% (CI 64-82) | same | C1 |
| fair sample of 33: supply 76%, demand 79%, supply-before-demand 39% | same | C1b |
| labour-market-only demand precedes schooling in 7% of 58 countries | same | C1b |
| 61 of 108 take-offs on the 1965 boundary; supply series start median 1975 | same | C1b |
| horse race supply +0.456 (0.174) vs demand +0.006 (0.203), n=78, 51 countries | same | C2; also `results/supply_demand.json` (fields `composite z-scores`) |
| individual coefficients (enrolment +0.307 (0.146), spending +0.125 (0.058), demand measures null) | same | C2 |
| demand alone: no significant measure (n=300, 103 countries) | same | C2 |
| Prussia 1763 supply-led 80-120 years; France 1833/Ferry 1881-82; Britain 1870, 40-90 years; US common schools 1830-60, high schools 1910-40 | `research/historical-sequence-2026-11-23` @ `ab658c7` | `README.md` sections 2-6 and the sequence table; definitions fixed at `74e0fe2` |
| US order 1910 -> 1955 -> 1957 (farm, schooling, fertility) | `research/subsistence-v2-2026-11-23` @ `ce66cfc` | `results/sequencing.txt` section C5; `results/sequencing.json` field `us` |
| the project's own long-run panel cannot date these cases (schooling series starts 1870, urban share 1950) | `research/historical-sequence-2026-11-23` @ `ab658c7` | `results/sequence_from_panel.json`; script `scripts/hist.py` |
| fertility ordering discrepancy (68.75% JSON vs 35.8% recomputed) | `research/subsistence-v2-2026-11-23` @ `ce66cfc` | `results/sequencing.json` field `pct_schooling_before_fertility` versus recomputation from `results/event_dates.csv`; flagged in Section 9, not used in claims |
