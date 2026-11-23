# Claims → source map

Every number in `paper-f-section.md`, `paper-f-claims-prior-art.md`, `paper-m-section-drivers.md`,
`paper-m-section-credential.md` and `paper-m-claims-prior-art.md`. "Record" is the verified branch
and commit; all four are in the shared repository and were verified by run-lead.

## Paper F section — fertility mechanism

| # | claim / number | record | file | evidence field |
|---|---|---|---|---|
| F1 | care share of female employment by attainment tercile 8.1% / 19.0% / 28.4%, n = 47 per tercile, 148 countries | care-credential @ e626cb8 | `results/results_care_cred.json`, `README.md` (1) | A1 tercile means in results JSON / README |
| F2 | female care share mean 18.3% (sd 12.1, range 1.2–52.1); male 5.9%; manufacturing 9.8%, n = 148/147 | care-credential @ e626cb8 | `README.md` (data section) | descriptive means |
| F3 | A1 absorption: attainment +0.009 (t 0.17, n 140); log GDP +0.242 (t 2.47); urban +0.42 (t 3.38) | care-credential @ e626cb8 | `results/results_care_cred.json` | `A1_*` blocks |
| F4 | A3 interaction −0.131 (t −1.38, n 141) → +0.128 (t 1.53) | care-credential @ e626cb8 | `results/results_care_cred.json` | `A3_*` blocks |
| F5 | placebos male care +0.179 (t 2.10); manufacturing −0.189 (t −3.47) | care-credential @ e626cb8 | `results/results_care_cred.json` | `A3_placebo_*` |
| F6 | A2 pairs +0.199 (t 2.14) → −0.045 (t −0.41), 119 country pairs | care-credential @ e626cb8 | `results/results_care_cred.json` | `A2_*` |
| F7 | 36-specification curve, care coefficient −0.57 to +0.27, both signs | care-credential @ e626cb8 | `results/results_care_cred.json` | `spec_curve` |
| F8 | 38 introductions, 25 countries, all TFR < 1.6 at introduction | policy-foreclosure @ 63691a2 | `data/events.json`, `results/A_results.txt` | events list; "events..." line |
| F9 | bound test 34/396 = 8.6%, one-sided 95% upper 11.3% | policy-foreclosure @ 63691a2 | `results/A_results.txt` | BOUND TEST line |
| F10 | 10/38 any year >1.6 within 10y; 5/38 with 3+ consecutive years (RUS 2007/2011, CZE 2008, EST 2004, BLR 2007) | policy-foreclosure @ 63691a2 | `results/A_results.txt` | "events where TFR exceeds"; "3+ CONSECUTIVE" line |
| F11 | long-run 9/38; BGR 10y (2014–2023, 1.81 in 2023), ROU 8, CZE 7, RUS 6, EST 5, BLR 5, LVA 4 | policy-foreclosure @ 63691a2 | `results/A2_longrun.json` | `longest_run` per event |
| F12 | highest TFR after any introduction 1.83 (CZE) | policy-foreclosure @ 63691a2 | `results/A_results.txt`, `A2_longrun.json` | "highest TFR reached" |
| F13 | event study +0.035 (SE 0.025; CI −0.014 to +0.083), 467 country-years, 25 countries; MDE 0.070 | policy-foreclosure @ 63691a2 | `results/A_results.txt` | EVENT STUDY line; POWER line |
| F14 | rivals: no controls +0.028 (SE 0.028); income+urban+migration +0.028 (SE 0.028); country trends +0.017 (SE 0.010) | policy-foreclosure @ 63691a2 | `results/A_results.txt` | RIVALS lines |
| F15 | pre/post: max post-10y minus pre-5y mean, median +0.151, mean +0.177 | policy-foreclosure @ 63691a2 | `results/A_results.txt` | PRE/POST line |
| F16 | Thailand TFR 1.84 (1997) → 1.73 (2000) → 1.56 (2010) → 1.21 (2023) | policy-foreclosure @ 63691a2 | `results/A_results.txt` | THAILAND line |
| F17 | early warning: 184 events, 80 usable; autocorr trend −0.025 (SE 0.008, t −3.3); variance +0.079 (SE 0.034, t 2.3) | early-warning @ 7e64f61 | `results/ews_results.json` | `ews` block |
| F18 | surrogate shares 0.57 (autocorr), 0.42 (variance), 16,000 surrogates | early-warning @ 7e64f61 | `results/ews_results.json` | `surrogate` block |
| F19 | MDE 0.095 (variance), 0.021 (autocorrelation) | early-warning @ 7e64f61 | `results/ews_results.json` | `mde` |
| F20 | diminishing returns: 3,865 country-years, 238 countries; quadratic +0.00019 (t 18.2); marginals −0.0099 / +0.0064 / +0.0214 with bootstrap CIs; turning point ≈ 39 | early-warning @ 7e64f61 | `results/ews_results.json` | `diminishing` block |
| F21 | scaling discipline: secondary enrolment exponent 0.215 (SE 0.035) between vs 0.090 (SE 0.124) within; attainment 0.312 (0.052) vs 0.072 (0.167); fertility between −0.479 vs change −0.056 | scaling @ fd691a6 | `results/consolidated_verdicts.csv`, `README.md` | verdict table; levels-vs-changes paragraph |

## Paper M sections — massification

| # | claim / number | record | file | evidence field |
|---|---|---|---|---|
| M1 | 50 real groupings / 8 families / 179 groups; 400 random re-partitions; 272 links; BH 5%; floor 1/401; single link needs 5,440 draws; 30 at ceiling → k* = 35 certified | grouping-multiverse-400 @ 1152cec | `results/headline.json`, `results/summary400.txt` | `R`, `floor`, `draws_needed_for_BH`, `empirical_floor_check` |
| M2 | 46 of 272 beat random with trends; 42 of old 43 survive, 1 dies (farm employment→gender parity higher ed), 4 new; 20 worse; 32 flips; 5 robust everywhere | grouping-multiverse-400 @ 1152cec | `results/summary400.txt`, `results/edge_table400.csv` | headline lines; `verdict_400` |
| M3 | 5 robust links: child mortality→life expectancy 62.7% vs 48.5% (above all 400 draws); child mortality→fertility 95.0% vs 93.0%; income→urbanisation 52% vs 49%; farm share→income 53% vs 37%; life expectancy→fertility 80.9% vs 93.0% | grouping-multiverse-400 @ 1152cec | `results/edge_table400.csv` | `share_TR`, `null_TR_mean`, `ceil_up` for the five rows |
| M4 | electricity: FE t 4.12/4.40/3.85/3.57/6.02; trends 0.53/−0.26/0.02/−0.77/−1.94; real shares 15.6/6.0/8.0/7.4/36.0% vs random 2.5/5.1/5.6/6.1/28.0%; 11 of 32 electricity links flip more than random | grouping-multiverse-400 @ 1152cec | `results/edge_table400.csv` | `pooled_FE_t`, `pooled_TR_t`, `share_TR`, `null_TR_mean`, `flips_more_tier2` |
| M5 | paid employment: wage_emp→lsc 8.9% vs 16.7% (q≈1); →sec 5.6% vs 2.7%; →prm_cmp 13.9% vs 11.6%; →gpi_sec 5.7% vs 5.3%; →ter 21.0% vs 20.5% (q 0.99); no wage-employment link beats random | grouping-multiverse-400 @ 1152cec | `results/edge_table400.csv` | same fields for wage_emp rows |
| M6 | 30 links above all 400 draws vs 0.68 expected (Poisson p ≈ 2e-38); binomial se on a share from 400 draws worst case ±4.9 points | grouping-multiverse-400 @ 1152cec | `results/headline.json`, `results/summary400.txt` | `ceiling_up`, `expected_ceiling_by_chance`, `share_summary` |
| M7 | credential gap: fertility correlation −0.15 (2% variance) vs attainment −0.62, credentialed jobs −0.65; horse race attainment −0.81 (t −4.6), gap +0.33 (t 1.9); with controls attainment −0.80 (t −2.85), gap +0.32 (t 1.61), log GDP −0.035 (t −0.30), urban +0.036 (t 0.19) | care-credential @ e626cb8 | `results/results_B_clean.json` | `B1_gap_only`, `B1_attainment_only`, `B1_race`, `B1_race_ctrl` |
| M8 | saturation: high-attainment R² 0.17 vs low-attainment R² 0.50 (23 vs 23 countries) | care-credential @ e626cb8 | `results/results_B_clean.json` | `B2_high*`, `B2_low*` |
| M9 | attainment vs credentialed-jobs share correlation +0.81 → re-verified for this draft at r = 0.807, n = 46 | care-credential @ e626cb8 | `results/panel_cross_section.csv` | columns `edu_ter_f`, `isco12_f`, finite n = 46 |
| M10 | care context: same numbers as F1–F6 (reported briefly in M) | care-credential @ e626cb8 | as above | as above |

## Notes on traceability
- All four records were pushed and their pre-registrations were the first commit on their branch (care-credential 7356e76, policy-foreclosure 7ad44d5, early-warning e12249b, scaling f8f782f).
- Paper-F and Paper-M numbers were not re-estimated for this draft. The only new computation in this record is the M9 re-verification of the +0.81 correlation from the committed panel (r = 0.807, n = 46), which is reported as a re-verification, not as a new result.
- No box compute was used for this draft (server was unavailable for part of the task window); everything is derived from committed files.
