# Claims to source: every number in Paper N1

Format: claim → branch @ hash → record path → field or derivation. All files verified present at the hash.

| claim in the paper | source | field / derivation |
|---|---|---|
| 64 countries with all three dates | `research/subsistence-v2-2026-11-23` @ `ce66cfc` | `results/sequencing.json`, field `countries_with_all_events`; reproduced in `results/sequencing_stats.json` (`all_three.n`) |
| schooling first in 31 of the 34 identified countries (91.2%); 30 undetermined; overall bounds 48.4%–95.3% | `results/event_dates.csv` (copy of `research/subsistence-v2-2026-11-23` @ `ce66cfc`) | recomputed in `results/sequencing_stats.json` (`all_three.identified_forward`, `.identified_reverse`, `.undetermined`, `.categories`) with boundary dates (schooling = 1965, release = 1991) treated as censored. The earlier "61 of 64" (`results/sequencing.json`, `results/sequencing.txt`) treated them as exact and is kept only in `naive_uncensored_for_reference` |
| median lead 18 years (18 countries with both dates exact; range −12 to +34) | same | `all_three.both_exact_median_lead`, `.both_exact_leads_sorted`; the 26-year median in the first draft is withdrawn |
| IQR 8.0–30.8 (both-exact pairs) | same | `all_three.both_exact_lead_q1`, `.both_exact_lead_q3` |
| (93.4% >10 years in first draft) withdrawn | same | not computable on censored pairs; see `naive_uncensored_for_reference` |
| 26 of 34 identified (76.5%) still forward after a +15-year error on schooling dates | same | `all_three.identified_forward_after_plus15_error`, `.identified_forward_after_plus15_share_of_identified_pct` |
| wider 81-country sample: 44 identified, 39 forward (88.6%), 37 undetermined; both-exact median 18 (n=21) | same | `schooling_and_release` block |
| supply onset before schooling 28% (CI 19-37) | `research/supply-demand-2026-11-23` @ `963e5e5` | `results/supply_demand.txt` section C1 |
| demand onset before schooling 73% (CI 64-82) | same | C1 |
| fair sample of 33: supply 76%, demand 79%, supply-before-demand 39% | same | C1b |
| labour-market-only demand precedes schooling in 7% of 58 countries | same | C1b |
| 61 of 108 schooling take-offs on the 1965 boundary and 65 of 134 release dates on the 1991 boundary; supply series start median 1975 | C1b; boundary counts recomputed from `results/event_dates.csv` | |
| horse race supply +0.456 (0.174) vs demand +0.006 (0.203), n=78, 51 countries | same | C2; also `results/supply_demand.json` (fields `composite z-scores`) |
| individual coefficients (enrolment +0.307 (0.146), spending +0.125 (0.058), demand measures null) | same | C2 |
| demand alone: no significant measure (n=300, 103 countries) | same | C2 |
| Prussia 1763 supply-led 80-120 years; France 1833/Ferry 1881-82; Britain 1870, 40-90 years; US common schools 1830-60, high schools 1910-40 | `research/historical-sequence-2026-11-23` @ `ab658c7` | `README.md` sections 2-6 and the sequence table; definitions fixed at `74e0fe2` |
| US order 1910 -> 1955 -> 1957 (farm, schooling, fertility) | `research/subsistence-v2-2026-11-23` @ `ce66cfc` | `results/sequencing.txt` section C5; `results/sequencing.json` field `us` |
| the project's own long-run panel cannot date these cases (schooling series starts 1870, urban share 1950) | `research/historical-sequence-2026-11-23` @ `ab658c7` | `results/sequence_from_panel.json`; script `scripts/hist.py` |
| fertility ordering: 68.75% = schooling ≤ fertility (20 ties, 18 both-at-1965); strict schooling-first 24, fertility-first 20; both-exact 11 vs 10 | same | `schooling_vs_fertility_all_three`; resolves the 68.75% vs 35.8% discrepancy; not used in claims |
