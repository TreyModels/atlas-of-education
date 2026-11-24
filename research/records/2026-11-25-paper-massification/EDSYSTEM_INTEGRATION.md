# Full-system multiverse integration — Paper M (25 November 2026, task-45)

**Branch:** new additive branch `research/paper-massification-edsystem-2026-11-25` from
`research/paper-massification-negatives-2026-11-24` @ `142ef49`; no old head rewritten. **Draft after integration:**
19,898 words (was 18,809; README flags the ~10.5% overage against the 12,000–18,000 target for a trim pass).

**Sources**

| source | branch @ commit | record file(s) |
|---|---|---|
| full-system multiverse (1,440 runs; pre-registration `3679f2d`) | `research/masseng-edsystem-2026-11-25` @ `b7108da` | `research/records/2026-11-25-masseng-edsystem/RUN_REPORT.md`, `results_multiverse.json`, `summary_multiverse.json` |
| independent tests (cluster-robust OLS + seed FE + Holm + stratum sign checks) | `research/edsystem-tests-2026-11-25` @ `aadbbb4` | `research/records/2026-11-25-edsystem-tests/MULTIVERSE_TESTS.md`, `full_system_tests.json` |

**Design:** 144 equation-choice combinations (3 affordability × 2 supply/funding × 3 learning/supply
configurations × 2 gates × 2 labour regimes × 2 rural structures) × 10 seeds = 1,440 `eduengine` runs; N=400
children/cohort, T=70 years, cohorts measured from year 35. **Toy, uncalibrated simulation; no causal or empirical
claims.**

**Exact numbers used in §7.9 (all from the two sources above; 10-seed means with 90% ranges, or test 95% CIs):**

| result | label | numbers |
|---|---|---|
| gates dominate lower/upper completion | simulation | lower: bar **.720** [.592, .849] vs quota **.550** [.549, .550]; upper: bar **.609** [.493, .746] vs quota **.449** [.446, .450]; quota−bar **−17.0pp** [−18.4, −15.7] / **−16.0pp**; tertiary −9.9pp |
| bar screens the poorest hardest | simulation | lower completion by wealth quintile under bar **.174** (q1) vs **.966** (q5), absolute gap .792; under quota **.121** / **.767**, gap .646 (quota narrows the absolute gap but caps completion for all) |
| affordability dominates primary/tertiary completion and the poverty margin | simulation | primary: cash-only **.797** [.746, .852] vs credit **.929** [.865, .977] / credit+poverty **.910** [.831, .968]; tertiary: **.296** [.245, .392] vs **.362** [.283, .497] / **.428** [.340, .569]; credit effects +13.2 [12.6, 13.9] / +11.3 [10.6, 12.0] (primary) and +6.6 [5.6, 7.7] / +13.2 [12.1, 14.4] (tertiary); q1 lower completion **.091→.195** |
| jobs regime dominates formal share | simulation | queue-with-floors **.293** [.275, .331] vs competitive **.627** [.556, .707]; η² **.96**; competitive−queue **+33.4pp** [32.4, 34.4] |
| rural structure dominates wealth parity | simulation | low penalty **.245** [.124, .393] vs high penalty **.100** [.043, .180]; **−14.6pp**; attainment costs −3.2/−5.0/−4.4/−5.3pp across levels |
| supply/funding moves public quality but is not identifiable from attainment | simulation | q_pub **0.99** vs **1.12**; supported test effect **+0.132** [0.115, 0.149]; completion effects not supported, variant ranges overlap 1.00 |
| tutoring is gate-driven and second-order for attainment | simulation | tutoring rate bar **.273** vs quota **.499** (gate-adjacent .320 vs .604); quota−bar **+22.6pp** [21.3, 23.9]; η² ≈ 0 for completion; learning arm +3.5pp primary, −0.09 skill premium; quota reallocates prep from tertiary (.145→.078) to lower/primary |

**Engine boundaries (stated in §7.9 and the record):** toy/uncalibrated `eduengine`; no persistent learning state; no
exam-score gate (bar-vs-quota seat rules, not score cut-offs); stylised labour market (queue floors vs competitive
skill premium) and rural/urban block (distance cost/urban share), not estimated; no migration, rural–urban sorting,
remittances, coupled income growth or country calibration; push-out decomposition by liquidity vs choice unusable
(engine overwrites exit-reason codes); PHL level check construct-limited (simulated lower completion .635
[.550, .833] vs observed 84.8% in 2024; no calibration).

**Disposition:** new §7.9; abstract sentence; §14.1 point 8; §14.2 box bullet; §15 objection 14; §16 conclusion
sentence; §12.3 cross-reference. All labelled simulation; no causal/empirical claim; no server compute.
