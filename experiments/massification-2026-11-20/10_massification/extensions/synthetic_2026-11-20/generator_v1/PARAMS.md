# PARAMS — declared parameters of the SYNTHETIC generator v1 (`code/sim_v1.py`)

**SYNTHETIC. Declared assumptions only — not estimates, not fitted values, not evidence.**

This file is a readable mirror of the parameter block actually recorded by the generator in
`results/RUN_MANIFEST.json` (key `params`) at run time. The authoritative copy is that JSON;
the code copies are the module-level constants in `code/sim_v1.py`. Nothing here is fitted to the
observed panel; the only observed numbers encoded are the declared PHL targets listed under
`targets_encoded` in the manifest.

Two notes for reviewers: (i) the `sim_v1.py` docstring says parameters are declared in
`../../PARAMS.md` — that path is stale; the v1 parameter block lives here and in the manifest
(the `../generator_v0/PARAMS.md` file covers v0 only). (ii) Parameter names are the code's own;
see `code/sim_v1.py` for each one's use site.

| parameter | declared value |
|---|---|
| `accel_div` | [1.0, 1.0, 1.3, 1.5] |
| `accel_ind` | [1.0, 1.0, 1.6, 1.3] |
| `adj_speed` | [0.5, 0.5, 0.35, 0.35] |
| `age_share_base` | 0.16 |
| `age_share_max` | 0.42 |
| `age_share_min` | 0.13 |
| `age_share_tfr_slope` | 0.045 |
| `band_share` | [0.42, 0.21, 0.2, 0.17] |
| `comp_step` | [0.1, 0.18, 0.32, 0.5] |
| `cred_prem` | 0.1 |
| `div_income` | 6000.0 |
| `div_x` | 0.95 |
| `g_cap` | 0.09 |
| `g_floor` | 0.0 |
| `g_noise_sd` | 0.006 |
| `ger_cap` | 105.0 |
| `gp` | [0.012, 0.008, 0.03, 0.022] |
| `lf_share_of_pop` | 0.52 |
| `lit_lag` | 12 |
| `lit_learn` | 0.05 |
| `mfg_u_coef` | [0.0, -0.1, 0.3, 0.1] |
| `office_u_coef` | [0.0, 0.35, 0.0, -0.2] |
| `overage_cap` | 1.05 |
| `phi_formal` | 0.82 |
| `psi_div` | 0.12 |
| `psi_ind` | 0.22 |
| `psi_pre` | 0.02 |
| `queue_max_lf` | 0.2 |
| `queue_retain` | 0.5 |
| `rank_gain` | 0.2 |
| `rung_a` | [0.9, 0.4, -0.3, -1.3] |
| `rung_b` | [-0.65, 0.2, 1.0, 2.2] |
| `rung_mult` | [2.2, 3.2, 4.6, 6.4] |
| `seat_hi` | [1.05, 0.985, 0.8, 0.78] |
| `seat_lo` | [1.02, 0.28, 0.14, 0.05] |
| `sec_ag_base` | 0.5 |
| `sec_ag_x` | -0.45 |
| `sec_floors` | [0.02, 0.05, 0.03, 0.05] |
| `sec_inf_base` | 0.24 |
| `sec_inf_x` | -0.08 |
| `sec_man_base` | 0.13 |
| `sec_man_x` | 0.09 |
| `seek` | [0.15, 0.35, 0.6, 0.8] |
| `sep` | [0.1, 0.07, 0.05, 0.04] |
| `star_c1` | [0.3, 1.0, 1.45, 1.2] |
| `star_c3` | [0.25, 0.8, 1.1, 0.9] |
| `surv_min` | [0.62, 0.55, 0.6, 0.7] |
| `takeoff_income` | 1500.0 |
| `takeoff_lit` | 0.6 |
| `ter_pool_retain` | 0.35 |
| `ter_trans_cap` | 0.65 |
| `x_income_coef` | 0.55 |
| `x_max` | 1.8 |
| `x_min` | 0.0 |
| `x_open` | [0.0, 0.08, 0.26, 0.48] |
| `x_urban_coef` | 0.55 |
| `x_urban_ref` | 0.4 |

Recorded seed: **20261120**; numpy 2.4.6; python 3.11.17.  
Code sha256: `a95fd6b3e81dfb8801774d7ad5ecd4b7722c72c737d3f436f7d176987b276aa4`  
Checks summary at delivery: A=FAIL, B=FAIL, C=FAIL, D=FAIL, E=PASS, F=PASS  
Determinism: two fresh runs write byte-identical results CSVs (verified by the controller, 2026-11-20).
