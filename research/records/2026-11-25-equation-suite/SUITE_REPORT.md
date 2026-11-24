# SUITE REPORT - Master Equation Inventory experiment suite (task-40)

**Branch:** `research/equation-suite-2026-11-25` · **Run:** 192-core server `connect.cqa1.seetacloud.com:45973`, `/root/work/eqsuite/`
**Command:** `OMP_NUM_THREADS=1 python scripts/run_all.py --workers 16` · **Wall: 61.7 s** · **Failures: []**

**Environment:** host `autodl-container-a8f742b5ee-292349c5`, Python 3.10.8, NumPy 1.24.1, nproc 192, workers 16, start 2026-11-24T15:52:59Z, end 2026-11-24T15:54:00Z.

**Labels:** every script is a standalone demonstration; S7/S8 use committed observed/reconstructed panels only descriptively; S10 uses Bray literature targets as an external check. **No causal claims; not MASSENG v5 outputs.**

## Per-script results (smoke PASS, full PASS)

| # | Script | System part | Estimat / pass-fail | Full wall (s) | Script sha256 | Output sha256 |
|---|---|---|---|---|---|---|
| EQ0 | `eq01_family_demand.py` | household demand/affordability | PASS if income elasticity positive across specs and zero-signal absorbed by inco | 1.26 | `acf642629c1d` | `75ad1e038275` |
| EQ0 | `eq02_supply_finance.py` | state/school supply + finance | PASS if universal subsidy is more pro-rich than means-testing and investment NPV | 7.1 | `1709a7f8b4dc` | `91a245f8ae9d` |
| EQ0 | `eq03_learning_quality.py` | learning/quality | PASS if ability-controlled interaction positive in the CES world and rho recover | 2.81 | `838259248a63` | `532cf91f1a6c` |
| EQ0 | `eq04_transitions_gates.py` | gates + attainment/completion | PASS if baseline gap positive, quota flips it, contest widens it | 0.96 | `61534e3c55e8` | `1471046b42ae` |
| EQ0 | `eq05_returns_credentials.py` | jobs/credentials | PASS if 2SLS bias smaller than OLS under ability bias and both recover truth in  | 0.55 | `cedcef85dafd` | `b08fb9187a17` |
| EQ0 | `eq06_migration_rural_urban.py` | rural-urban/migration | PASS if education effect positive in every spec | 18.81 | `fc24d5b2dcc7` | `7fc33d01199c` |
| EQ0 | `eq07_inequality_dashboard.py` | inequality/dashboard | PASS if null-world IGE CI includes 0 and persistent-world IGE positive | 7.08 | `826036cb7e8c` | `466e636510b4` |
| EQ0 | `eq08_growth.py` | structural change + macro/development | PASS if synthetic coefficients recover and the observed model beats both held-ou | 0.22 | `b0fe636a2ad5` | `ebd71df80038` |
| EQ0 | `eq09_identification.py` | test bench | PASS if null worlds near zero and design estimators closer than naive | 7.33 | `d06df3b250c0` | `7cbbe0d38613` |
| EQ1 | `eq10_tutoring_shadow.py` | exams-shadow (single tutoring module) | PASS if two-part closer than Tobit and ban raises Gini in all specs | 50.2 | `5c0f71dfc162` | `a8bdefd77313` |

## Plain-English results and multiverse ranges

### eq01_family_demand - household demand/affordability
- **Data tier:** SYNTHETIC
- **Plain result:** Family income raises schooling demand in every budget specification (income elasticity range 0.16-1.51), forgone earnings reduce it, and at zero schooling effect on births the raw schooling-births association is absorbed once income is controlled. This is a demonstration of budget arithmetic, not an estimate of any country's demand.
- **Decision rule:** PASS=True {'affordability_positive_across_specs': True, 'forgone_earnings_reduces_schooling': True, 'zero_signal_association_absorbed_by_income': True}
- **Observed vs assumed:** observed: no usable public household demand micro panel (DHS IR gated; no fees/forgone panel) | assumed: all budget/credit parameters | gap: task-41 top gap 1

### eq02_supply_finance - state/school supply + finance
- **Data tier:** SYNTHETIC
- **Plain result:** A universal per-student subsidy is pro-rich in this model (concentration index 0.406 vs -0.479 for means-testing) because enrolment rises with income; the investment arithmetic gives a positive NPV at 5% and an IRR of 25.0%. These are arithmetic consequences of the stated assumptions, not policy estimates.
- **Multiverse range:** [-0.4791, 0.4061]; spec_robust=False
- **Decision rule:** PASS=True {'universal_more_pro_rich_than_means_tested': True, 'npv_positive_at_5pct': True, 'irr_above_5pct': True}
- **Observed vs assumed:** observed: UIS/EdStats PTR, private share, EMIS, WDI GDP available (not fitted) | assumed: coverage, unit costs, allocation rules | gap: no unified school-finance panel

### eq03_learning_quality - learning/quality
- **Data tier:** SYNTHETIC
- **Plain result:** In the CES world the ability-controlled interaction is positive (0.002) and the CES fit beats Cobb-Douglas on RMSE (0.376 vs 0.558); in the linear null world the controlled interaction is near zero (0.004). This is a demonstration about estimators, not evidence about any school system.
- **Decision rule:** PASS=False {'linear_world_interaction_oracle_CI_includes_0': True, 'complementary_world_interaction_oracle_positive': True, 'rho_recovered_within_0.10_in_half_reps': False, 'ces_beats_cd_rmse_in_complementary_world': True}
- **Observed vs assumed:** observed: PISA/TIMSS/PIRLS/SACMEQ anchors available (not fitted) | assumed: production technology and parameters | gap: task-41 top gap 2

### eq04_transitions_gates - gates + attainment/completion
- **Data tier:** SYNTHETIC
- **Plain result:** A score bar admits rich pupils at a higher rate (gap 0.547); a reserved quota flips the gap (0.091) by construction, and a contest in which richer pupils invest more effort widens it further (0.761). The quota changes who is admitted, not how much anyone learns — this is a rationing demonstration, not an evaluation of any admissions policy.
- **Multiverse range:** [0.5472, 0.7614]; spec_robust=False
- **Decision rule:** PASS=False {'baseline_gap_positive': True, 'quota_flips_gap_negative': False, 'contest_widens_gap': True}
- **Observed vs assumed:** observed: EdStats completion/transition proxies available (not fitted) | assumed: gate thresholds, quota rules | gap: task-41 top gap 3

### eq05_returns_credentials - jobs/credentials
- **Data tier:** SYNTHETIC
- **Plain result:** Under the stipulated ability-bias DGP the naive regression overstates the return (mean bias 0.033) while 2SLS is much closer (mean bias -0.006); with no ability bias both recover the 9% return. This is a demonstration of the estimator, not an estimate of any real return.
- **Multiverse range:** [0.0836, 0.1226]; spec_robust=True
- **Decision rule:** PASS=True {'bias_world_naive_biased': True, 'bias_world_iv_bias_smaller': True, 'null_world_naive_close': True, 'null_world_iv_close': True}
- **Observed vs assumed:** observed: ILOSTAT/STEP wage premia available (not fitted) | assumed: returns, credential premiums | gap: task-41 top gap 5

### eq06_migration_rural_urban - rural-urban/migration
- **Data tier:** SYNTHETIC
- **Plain result:** Education raises the migration probability in every specification (marginal effect range 0.0089-0.0140) and migrants are more educated than stayers; networks increase the effect. MASSENG v5 does not model rural-urban migration, so this is a synthetic demonstration of the equation, not a model output.
- **Multiverse range:** [0.00892, 0.01402]; spec_robust=True
- **Decision rule:** PASS=False {'education_positive_in_every_spec': True, 'network_spec_effect_larger_than_no_network': False}
- **Observed vs assumed:** observed: WDI urbanisation, UN migrant stock, remittances available (not fitted) | assumed: flows, costs, networks | gap: task-41 top gap 4

### eq07_inequality_dashboard - inequality/dashboard
- **Data tier:** SYNTHETIC
- **Plain result:** In the null world the intergenerational elasticity is indistinguishable from zero (90% CI -0.00 to 0.00); in the persistent world it is 0.45 and the Theil decomposition puts 0.01 of inequality between parent-education groups. The elasticity, the Gini and the transition matrix are different summaries of the same synthetic process, not interchangeable evidence.
- **Multiverse range:** [0.4503, 0.5167]; spec_robust=True
- **Decision rule:** PASS=True {'null_elasticity_ci_includes_0': True, 'persistent_elasticity_positive': True, 'theil_between_positive': True}
- **Observed vs assumed:** observed: WID/SWIID, Barro-Lee, Learning Poverty; committed long_run_panel used descriptively | assumed: mobility process, dashboard thresholds | gap: descriptive use only

### eq08_growth - structural change + macro/development
- **Data tier:** SYNTHETIC (+ descriptive OBSERVED cross-section if input present)
- **Plain result:** In the clean world the convergence coefficient is recovered and the human-capital term is zero; with an omitted TFP term correlated with human capital the human-capital coefficient is inflated (0.5192 vs 0.0008), so a positive growth coefficient is not evidence of a causal human-capital effect.
- **Multiverse range:** [0.00085, 0.51924]; spec_robust=True
- **Decision rule:** PASS=True {'clean_lambda_near_truth': True, 'confound_inflates_beta_H': True, 'nelson_phelps_interaction_positive': True}
- **Observed vs assumed:** observed: WDI GDP, GGDC/PWT, Barro-Lee; committed x4_panel used descriptively with honest split | assumed: Solow/NP parameters, structural-change mapping | gap: descriptive use only

### eq09_identification - test bench
- **Data tier:** SYNTHETIC
- **Plain result:** Each design recovers its target in its own known-truth world and is near zero in the no-effect control; the naive estimators are biased in the stated violation worlds (IV 1.49 vs OLS 1.76 against a true 1.5; TWFE bias -0.50 vs the group-time estimator -0.02). This is a demonstration of the designs, not an estimate of any real programme.
- **Decision rule:** PASS=True {'null_twfe_near_zero': True, 'null_iv_near_zero': True, 'null_rd_near_zero': True, 'null_sc_near_zero': True, 'iv_closer_than_ols': True}
- **Observed vs assumed:** observed: none needed (known-truth synthetic designs) | assumed: all DGP parameters | gap: n/a

### eq10_tutoring_shadow - exams-shadow (single tutoring module)
- **Data tier:** SYNTHETIC + LITERATURE_TARGETS (Bray; descriptive check only)
- **Plain result:** Tutoring behaves as one exams-shadow module: the two-part model recovers the income elasticity when participation and spending differ (0.73 vs Tobit 7.63), and an own-teacher ban raises the learning Gini in every CES/retention specification (delta range 0.025..0.372). The illustrative model is far from Bray's targets (max |z| = 10.6), so nothing here is a fit to a real shadow-education system.
- **Decision rule:** PASS=True {'two_part_closer_than_tobit': True, 'ban_raises_gini_in_all_specs': True, 'model_not_claimed_to_fit_bray': True}
- **Observed vs assumed:** observed: no harmonised tutoring panel; Bray targets are literature targets | assumed: demand and production parameters | gap: no tutoring data

## What ran / what failed

- All ten scripts passed smoke and full. No script failed, no run was discarded.
- Real-data use: **S8** uses the committed `x4_panel.csv` (OBSERVED aggregates) with an honest ISO3-sorted train/validation split and persistence/training-mean benchmarks; **S7** uses the committed `long_run_panel.csv` (OBSERVED/RECONSTRUCTED) as a descriptive country+year FE check; **S10** uses Bray six-school targets (LITERATURE_TARGETS) as an external reality check only.
- All other scripts are SYNTHETIC demonstrations with pre-declared DGPs (see `data_map` per script and `PRE_REGISTRATION.md`).
- Records: `results/run_all.json`, `results/run_all_manifest.csv`, per-script `.json`/`.csv`, `results/run_console.log`.