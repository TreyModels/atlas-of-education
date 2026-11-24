# Claims to source: every number in Paper N1

Format: claim → branch @ hash → record path → field or derivation. All files verified present at the hash.
**Revision of 25 November 2026:** the retracted "7 per cent" labour-demand figure was removed (see row 4);
E6, E8 and N3 rows added; every number quoted in the revised passages is recomputed by
`scripts/verify_revision_numbers.py`, output `results/revision_verification.json` (28/28 checks pass), from
verbatim copies of the source records in `data/`.

| claim in the paper | source | field / derivation |
|---|---|---|
| 64 countries with all three dates | `research/subsistence-v2-2026-11-23` @ `ce66cfc` | `results/sequencing.json`, field `countries_with_all_events`; reproduced in `results/sequencing_stats.json` (`all_three.n`) and `results/revision_verification.json` |
| 61 of 64 schooling first (95.3%) | same | `results/sequencing.json` (`pct_release_before_schooling` = 4.6875 → 3 reverse, 61 forward); recomputed in `results/sequencing_stats.json` (`all_three.forward`) and `results/revision_verification.json` |
| median lead 26 years | same | `results/sequencing.txt` ("median gap release->schooling: -26 years" under its schooling-minus-release convention); recomputed as `all_three.median_lead` = 26.0 |
| IQR 16.5-29.5 (17-29 rounded) among forward cases; all-64 gap IQR 16-29 | same | recomputed `all_three.q1`, `all_three.q3` from `results/event_dates.csv` (`scripts/sequencing_stats.py`); all-64 IQR in `revision_verification.json` |
| 93.4% of forward cases >10 years | same | recomputed `all_three.share_gt10` |
| 85.2% >15 years; 81.25% of the panel still forward after a +15-year error (52/64) | same | recomputed `all_three.share_gt15`, `all_three.still_forward_after_plus15_pct` |
| wider 81-country sample: 26-year median, 93.8% forward | same | recomputed `schooling_and_release` block |
| **RETRACTED — DO NOT USE**: labour-market-only demand precedes schooling in 7% of 58 countries | `research/supply-demand-2026-11-23` @ `963e5e5` | `results/supply_demand.txt` C1b. A 1991+ data-start artefact (Codex F02/F12); replaced by the E6 row below. The paper cites it only as retracted |
| E6 demand-first shares: 10.0% GGDC non-agricultural employment, 15.4% urbanisation, 24.1% industry VA, 18.8% agricultural VA (1900-2012, identifiable countries); all-country bounds 6.7-53.0%; weak forward-or-tie / left-censored 21-43%; N3 54-definition strict range 0.0-30.8% (median 10.45%), q1 default 6.2% strict / 70.6% weak tie / 17.6% schooling-first | `research/e6e8-sequencing-2026-11-25` @ `2d19da7` | `results/e6_summary.json`, `results/n3_recommendation.json` (copies in `data/`); fields `forward_share_identified`, `forward_lower/upper_bound_all`, `forward_or_tie`/`n_in_window`, `q1_default`; recomputed in `results/revision_verification.json` |
| E8 fee-abolition event study: 8 verified dates MWI 1994, ETH 1995, UGA 1997, LSO 2000, TZA 2001, KEN 2003, MOZ 2004, GHA 2005; 4 unresolved excluded from main; CS post ATT +22.1 to +28.6 at +1..+6; on-impact +12.4 [-2.4, 27.2]; pre-trends -2 -0.03 [-3.43, 3.38], -3 -0.13 [-7.23, 6.98], -4 1.35 [-6.35, 9.04]; placebo -0.39; LOO 18.17-26.16; 7 treated countries with primary-GER coverage | `research/e6e8-sequencing-2026-11-25` @ `2d19da7`; dates `research/codex-source-verification-2026-11-25` @ `9a0fd69` | `results/e8_results.json`, `fee_dates.csv` (copies in `data/`); `event_table`, `pre_trend_rows`, `sensitivity`; `preferred_year`/`status`; recomputed in `results/revision_verification.json` |
| 61 of 108 take-offs on the 1965 boundary; supply series start median 1975 | `research/supply-demand-2026-11-23` @ `963e5e5` | `results/supply_demand.txt` C1b |
| fair sample of 33: supply 76%, demand 79%, supply-before-demand 39% | same | C1b |
| horse race supply +0.456 (0.174) vs demand +0.006 (0.203), n=78, 51 countries | same | C2; also `results/supply_demand.json` (composite fields); recomputed in `results/revision_verification.json` |
| individual coefficients (enrolment +0.307 (0.146), spending +0.125 (0.058); demand measures null) | same | C2 |
| demand alone: no significant measure (n=300, 103 countries) | same | C2 |
| Prussia 1763 state supply 80-120 years; France 1833/Ferry 1881-82; Britain 1870, 40-90 years; US common schools 1830-60, high schools 1910-40 — **all UNVERIFIED literature standard** | `research/historical-sequence-2026-11-23` @ `ab658c7` | `README.md` sections 2-6 and the sequence table; definitions fixed at `74e0fe2` |
| US order 1910 -> 1955 -> 1957 (farm, schooling, fertility) | `research/subsistence-v2-2026-11-23` @ `ce66cfc` | `results/sequencing.txt` section C5; `results/sequencing.json` field `us` |
| the project's own long-run panel cannot date these cases (schooling series starts 1870, urban share 1950) | `research/historical-sequence-2026-11-23` @ `ab658c7` | `results/sequence_from_panel.json`; script `scripts/hist.py` |
| fertility ordering: strict schooling-first 37.5% (24/64, 95% interval 26.6-50.0), 31.25% simultaneous, 31.25% fertility-first; all 81 with both dates 35.8%. The record JSON's 68.75% counts ties as schooling-first and is not used | `research/subsistence-v2-2026-11-23` @ `ce66cfc` | `results/event_dates.csv`; recomputed in `results/revision_verification.json` and `research/paper-massification-2026-11-25` `scripts/recompute_fertility_ordering.py` |
| data tiers (observed / reconstructed / literature-standard) and the TFR-vs-effective-fertility construct note | this branch; E6/E8 record §0 | `PAPER.md` abstract, §3, §3.1; `research/e6e8-sequencing-2026-11-25` @ `2d19da7` `REPORT.md` §0; construct difference from `research/e11-fertility-audit-2026-11-25` @ `e926575` (median 0.3042, max 4.2677) |

**Recomputation:** `scripts/verify_revision_numbers.py` (requires pandas; run with the project's bundled runtime
python) reads `results/event_dates.csv` and the `data/` copies and writes `results/revision_verification.json`
(28/28 checks pass).

**UNVERIFIED numbers:** the only quoted numbers not recomputable in this pass are the four historical sequences'
literature dates/percentages, labelled **UNVERIFIED literature standard** in the paper (§5). All
E6/E8/N3/sequencing/fertility/supply-demand numbers quoted in the revision are recomputed.
