# Country configurations — every parameter labelled

Labels: **sourced** (observed data / named source) · **estimated** (derived from a named series by a stated rule) ·
**fitted** (calibrated in this package) · **assumed** (judgement, no direct evidence).

Structural limitations (declared): massabm has a 10- or 12-year basic cycle only, so KHM/HKG/CHN are
approximated with a 10-year cycle (4-year secondary); 6-3-3 and 3-3-4 cannot be represented exactly.
PHL keeps its K-12/CCT/free-tuition/overseas architecture; KHM/HKG/CHN switch those off.
hukou/migration (CHN) and HKG 3-3-4 are NOT modelled.

## Source series used (from 04_data, observed cells only)

| series | use |
|---|---|
| gmr_observed_6countries_1970_2024.csv | GER by level (fit targets C3/loop2) |
| uis_sdg4_4countries_long.csv | completion (fit targets) |
| wdi_4countries_long.csv SP.URB.TOTL.IN.ZS | urban_path (sourced) |
| wdi_4countries_long.csv SE.PRM.DURS / SE.SEC.DURS | structural note on cycle length |
| wdi_4countries_long.csv BX.TRF.PWKR.DT.GD.ZS | PH overseas-channel context (not wired) |

## PHL

baseline institutions: K-12 2013, 4Ps, free SUC tuition, overseas registration architecture

| parameter | value | label | basis |
|---|---|---|---|
| `seed` | 0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `t0` | 1920 | **assumed** | model start 1920 to allow 1980 initial stocks |
| `t1` | 2035 | **assumed** | horizon; 2040 set for the ledger extensions |
| `report_from` | 1960 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `N` | 10000 | **assumed** | cohort scale, no behavioural role |
| `y_sigma` | 0.8 | **estimated** | lognormal income sd from WDI/APIS-type Gini ~0.4-0.5 |
| `y_median` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `subsist0` | 0.75 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `growth` | 0.015 | **estimated** | real index growth vs subsistence; WDI GDP per capita long-run |
| `shock_sigma` | 0.5 | **assumed** | income shock sd |
| `borrow` | 0.5 | **assumed** | annual borrowing capacity as share of income; no direct country series |
| `need_share` | 0.36 | **estimated** | direct child-labour opportunity cost share; ILO/EDB employment context |
| `cct_path` | [[2007, 0.0], [2008, 0.04], [2035, 0.04]] | **sourced** | PHL 4Ps (2008+); switched off elsewhere |
| `tuition_path` | [[2017, 1.0], [2018, 0.5], [2035, 0.5]] | **sourced** | PHL RA 10931 free SUC tuition (2018) |
| `idio_exit` | 0.045 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `rural_cost` | 0.03 | **assumed** | extra post-primary rural cost |
| `urban_path` | [[1945, 0.25], [1980, 0.37], [2010, 0.45], [2035, 0.55]] | **sourced** | WDI SP.URB.TOTL.IN.ZS urban share, interpolated 1945-2035 |
| `cost_pri` | 0.02 | **assumed** | direct primary cost; low and stable |
| `cost_jhs` | 0.05 | **assumed** | direct lower-secondary cost |
| `cost_shs` | 0.06 | **fitted** | fitted in C3 to observed GER/completion |
| `cost_col` | 0.573012846750278 | **fitted** | fitted in C3/loop2 to observed GER; bounds 0.3-1.0 |
| `cost_apx` | 0.4 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `prof_cost_extra` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `cap_cost` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `child_wage` | [[9, 0.0], [12, 0.1], [15, 0.3], [18, 0.6], [22, 0.9]] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `child_wage_male_mult` | 1.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `crra` | 1.5 | **assumed** | risk preferences |
| `disc` | 0.93 | **assumed** | discount factor |
| `work_years` | 40 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `adult_age` | 18 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tau` | 0.04 | **assumed** | logit noise in schooling choice |
| `prior_income` | [0.9, 1.0, 1.1, 1.5, 2.2, 3.2, 3.0, 4.0] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `belief_decay` | 0.88 | **assumed** | memory of observed outcomes; E5 shows it is a structural lever |
| `belief_k` | 0.003 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `female_F_shift` | 0.2 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `ses_formatability` | 0.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `w_A` | 0.55 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `w_F` | 0.35 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `q_urban` | 0.15 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `q_inc` | 0.15 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `sigma_exam` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `sigma_self` | 0.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `bar_basic` | -1.8 | **fitted** | fitted in C3 to observed completion |
| `bar_college` | -1.0 | **fitted** | fitted in C3 to observed GER/transition |
| `bar_board` | 0.7 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_cost` | 0.15 | **assumed** | tutoring price per gate-year; no consistent cross-country price series in 04_data |
| `tut_effect` | 0.25 | **assumed** | tutoring score effect; literature cards feed this once TARGETS_SHADOW lands |
| `apex_path` | [[1945, 0.004], [2035, 0.012]] | **fitted** | apex seat scale fitted (apex_mult) in C3 |
| `hc_school` | 0.05 | **fitted** | fitted in C3; near zero implies mostly signalling at the aggregate level |
| `hc_ability` | 0.3 | **assumed** | ability return inside the gray box |
| `mode` | full | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `wage_base` | {"os_prof": 5.0, "elite": 4.5, "mid": 2.6, "os_agency": 2.3, "routine" | **estimated** | sector wage relativities, informal = 1.0 (see LITERATURE_LEDGER) |
| `wage_hc` | {"os_prof": 1.0, "elite": 1.0, "mid": 1.0, "os_agency": 0.5, "routine" | **estimated** | within-sector schooling returns |
| `vac_paths` | {"os_prof": [[1945, 0.001], [1990, 0.003], [1997, 0.004], [2001, 0.012 | **estimated** | sector vacancy paths inferred from employment shares (EDB/WDI) |
| `employers_per_pool` | 20 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `r_init` | {"elite": 4, "mid": 4, "routine": 3} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `screen_kappa` | 4.7 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fill_margin` | 1.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `r_adjust_p` | 0.25 | **assumed** | employer floor adjustment probability |
| `rho_level` | [0.0, 0.1, 0.1, 0.2, 0.3, 0.8] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `sig_noise` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `lic_bonus` | {"elite": 0.0, "mid": 0.0, "routine": 0.0} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `referral_max` | 0.6 | **assumed** | kin-referral reach; Philippine evidence suggests high |
| `referral_homophily` | {"elite": 1.5, "mid": 0.8, "routine": 0.3} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `referral_min_level` | {"elite": 4, "mid": 3, "routine": 1} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `agency_min_level` | 3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `female_bonus` | {"os_prof": 1.0, "os_agency": 0.1} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `female_penalty` | {"elite": 0.0, "mid": 0.0, "routine": 0.0} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `os_noise` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `formal_growth_scale` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `vac_scale` | {} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_ban` | [] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_ban_leak` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `arch_path` | [[2004, 0.0], [2009, 0.1], [2012, 0.4], [2016, 1.0]] | **sourced** | PHL/atlas overseas registration architecture (MRAs 2004-2016); off elsewhere |
| `p_discretion` | 0.95 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `p_downgrade` | 0.6 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `downgrade_factor` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `arch_visible_from` | 2005 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `recog_lag` | 10 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reform_rule` | exogenous | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reform_year` | 2013 | **sourced** | PHL RA 10533 K-12 (2013); switched off elsewhere |
| `impl_lag` | 3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `capacity_path` | [[1945, 0.3], [1985, 0.35], [1986, 0.5], [2009, 0.55], [2010, 0.8], [2 | **estimated** | state schooling capacity inferred from observed GER trajectories |
| `capacity_shock` | 0.03 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `cap_threshold` | 0.7 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reform_cost` | 0.004 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `state_horizon` | 25 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `state_disc` | 0.95 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `script_base` | 0.01 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `script_pulse` | 0.15 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `script_events` | [1949, 1990, 2000, 2015] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `belief_mode` | naive | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `diploma_by_years` | False | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `idio_mode` | yearly | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `hc_school_informal` | None | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `informal_crowding` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fair_sigma` | 1.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fair_rel0` | 2.2 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reanchor_share` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reanchor_sticky` | 0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `conformity` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `os_prof_boost_path` | [[1900, 1.0], [2100, 1.0]] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `female_informal_mult` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `anticipate_liquidity` | False | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_access_path` | None | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_max_age` | 35 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_tau` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_forgo` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_cash_share` | 0.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tax_income` | 0.1 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tax_consumption` | 0.12 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `consumption_share` | 0.8 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `remit_share` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `pub_cost` | {"primary": 0.2, "secondary": 0.25, "shs": 0.3, "college": 0.35} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `work_life` | 40 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `macro_elasticity` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `macro_ref_year` | 1980 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `macro_window` | 20 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `macro_lag` | 3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `floor_fixed` | None | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `hc_beta0` | 0.1 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `hc_sigma` | 2.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `support_effect` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `support_share` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `support_target_q` | None | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `support_withhold` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_hc_equiv` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_suppress` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fair_slots_mult` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fair_income_scale` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `prov_capacity` | 0.4037205298384015 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `prov_elasticity` | 1.2502432325102368 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `teacher_capacity` | 0.08237097111931437 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `teacher_price_mult` | 0.6 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `freeze_schooling` | False | **assumed** | not documented individually: judgement/placeholder, no direct evidence |

## KHM

no K-12 reform, no CCT, no overseas professional architecture; low capacity; higher child-labour need

| parameter | value | label | basis |
|---|---|---|---|
| `seed` | 0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `t0` | 1920 | **assumed** | model start 1920 to allow 1980 initial stocks |
| `t1` | 2035 | **assumed** | horizon; 2040 set for the ledger extensions |
| `report_from` | 1960 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `N` | 10000 | **assumed** | cohort scale, no behavioural role |
| `y_sigma` | 0.9 | **estimated** | lognormal income sd from WDI/APIS-type Gini ~0.4-0.5 |
| `y_median` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `subsist0` | 0.75 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `growth` | 0.015 | **estimated** | real index growth vs subsistence; WDI GDP per capita long-run |
| `shock_sigma` | 0.6 | **assumed** | income shock sd |
| `borrow` | 0.5 | **assumed** | annual borrowing capacity as share of income; no direct country series |
| `need_share` | 0.45 | **estimated** | direct child-labour opportunity cost share; ILO/EDB employment context |
| `cct_path` | [[1900, 0.0], [2100, 0.0]] | **sourced** | PHL 4Ps (2008+); switched off elsewhere |
| `tuition_path` | [[2017, 1.0], [2018, 0.5], [2035, 0.5]] | **sourced** | PHL RA 10931 free SUC tuition (2018) |
| `idio_exit` | 0.045 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `rural_cost` | 0.05 | **assumed** | extra post-primary rural cost |
| `urban_path` | [[1945, 0.12], [1980, 0.15], [2010, 0.21], [2035, 0.27]] | **sourced** | WDI SP.URB.TOTL.IN.ZS urban share, interpolated 1945-2035 |
| `cost_pri` | 0.02 | **assumed** | direct primary cost; low and stable |
| `cost_jhs` | 0.05 | **assumed** | direct lower-secondary cost |
| `cost_shs` | 0.06 | **fitted** | fitted in C3 to observed GER/completion |
| `cost_col` | 0.7 | **fitted** | fitted in C3/loop2 to observed GER; bounds 0.3-1.0 |
| `cost_apx` | 0.4 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `prof_cost_extra` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `cap_cost` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `child_wage` | [[9, 0.0], [12, 0.1], [15, 0.3], [18, 0.6], [22, 0.9]] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `child_wage_male_mult` | 1.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `crra` | 1.5 | **assumed** | risk preferences |
| `disc` | 0.93 | **assumed** | discount factor |
| `work_years` | 40 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `adult_age` | 18 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tau` | 0.04 | **assumed** | logit noise in schooling choice |
| `prior_income` | [0.9, 1.0, 1.1, 1.5, 2.2, 3.2, 3.0, 4.0] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `belief_decay` | 0.88 | **assumed** | memory of observed outcomes; E5 shows it is a structural lever |
| `belief_k` | 0.003 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `female_F_shift` | 0.2 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `ses_formatability` | 0.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `w_A` | 0.55 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `w_F` | 0.35 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `q_urban` | 0.15 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `q_inc` | 0.15 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `sigma_exam` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `sigma_self` | 0.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `bar_basic` | -1.8 | **fitted** | fitted in C3 to observed completion |
| `bar_college` | -1.0 | **fitted** | fitted in C3 to observed GER/transition |
| `bar_board` | 0.7 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_cost` | 0.15 | **assumed** | tutoring price per gate-year; no consistent cross-country price series in 04_data |
| `tut_effect` | 0.25 | **assumed** | tutoring score effect; literature cards feed this once TARGETS_SHADOW lands |
| `apex_path` | [[1945, 0.004], [2035, 0.012]] | **fitted** | apex seat scale fitted (apex_mult) in C3 |
| `hc_school` | 0.05 | **fitted** | fitted in C3; near zero implies mostly signalling at the aggregate level |
| `hc_ability` | 0.3 | **assumed** | ability return inside the gray box |
| `mode` | full | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `wage_base` | {"os_prof": 5.0, "elite": 4.5, "mid": 2.6, "os_agency": 2.3, "routine" | **estimated** | sector wage relativities, informal = 1.0 (see LITERATURE_LEDGER) |
| `wage_hc` | {"os_prof": 1.0, "elite": 1.0, "mid": 1.0, "os_agency": 0.5, "routine" | **estimated** | within-sector schooling returns |
| `vac_paths` | {"os_prof": [[1945, 0.001], [1990, 0.003], [1997, 0.004], [2001, 0.012 | **estimated** | sector vacancy paths inferred from employment shares (EDB/WDI) |
| `employers_per_pool` | 20 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `r_init` | {"elite": 4, "mid": 4, "routine": 3} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `screen_kappa` | 4.7 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fill_margin` | 1.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `r_adjust_p` | 0.25 | **assumed** | employer floor adjustment probability |
| `rho_level` | [0.0, 0.1, 0.1, 0.2, 0.3, 0.8] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `sig_noise` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `lic_bonus` | {"elite": 0.0, "mid": 0.0, "routine": 0.0} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `referral_max` | 0.6 | **assumed** | kin-referral reach; Philippine evidence suggests high |
| `referral_homophily` | {"elite": 1.5, "mid": 0.8, "routine": 0.3} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `referral_min_level` | {"elite": 4, "mid": 3, "routine": 1} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `agency_min_level` | 3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `female_bonus` | {"os_prof": 1.0, "os_agency": 0.1} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `female_penalty` | {"elite": 0.0, "mid": 0.0, "routine": 0.0} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `os_noise` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `formal_growth_scale` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `vac_scale` | {} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_ban` | [] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_ban_leak` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `arch_path` | [[1900, 0.0], [2100, 0.0]] | **sourced** | PHL/atlas overseas registration architecture (MRAs 2004-2016); off elsewhere |
| `p_discretion` | 0.95 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `p_downgrade` | 0.6 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `downgrade_factor` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `arch_visible_from` | 2005 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `recog_lag` | 10 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reform_rule` | never | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reform_year` | 2013 | **sourced** | PHL RA 10533 K-12 (2013); switched off elsewhere |
| `impl_lag` | 3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `capacity_path` | [[1945, 0.12], [1985, 0.18], [2009, 0.28], [2035, 0.5]] | **estimated** | state schooling capacity inferred from observed GER trajectories |
| `capacity_shock` | 0.03 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `cap_threshold` | 0.7 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reform_cost` | 0.004 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `state_horizon` | 25 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `state_disc` | 0.95 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `script_base` | 0.01 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `script_pulse` | 0.15 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `script_events` | [1949, 1990, 2000, 2015] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `belief_mode` | naive | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `diploma_by_years` | False | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `idio_mode` | yearly | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `hc_school_informal` | None | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `informal_crowding` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fair_sigma` | 1.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fair_rel0` | 2.2 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reanchor_share` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reanchor_sticky` | 0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `conformity` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `os_prof_boost_path` | [[1900, 1.0], [2100, 1.0]] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `female_informal_mult` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `anticipate_liquidity` | False | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_access_path` | None | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_max_age` | 35 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_tau` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_forgo` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_cash_share` | 0.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tax_income` | 0.1 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tax_consumption` | 0.12 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `consumption_share` | 0.8 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `remit_share` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `pub_cost` | {"primary": 0.2, "secondary": 0.25, "shs": 0.3, "college": 0.35} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `work_life` | 40 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `macro_elasticity` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `macro_ref_year` | 1980 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `macro_window` | 20 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `macro_lag` | 3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `floor_fixed` | None | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `hc_beta0` | 0.1 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `hc_sigma` | 2.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `support_effect` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `support_share` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `support_target_q` | None | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `support_withhold` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_hc_equiv` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_suppress` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fair_slots_mult` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fair_income_scale` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `prov_capacity` | 0.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `prov_elasticity` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `teacher_capacity` | 0.15 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `teacher_price_mult` | 0.6 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `freeze_schooling` | False | **assumed** | not documented individually: judgement/placeholder, no direct evidence |

## HKG

city-state: 100% urban, high capacity, no rural cost, no overseas professional channel, no CCT

| parameter | value | label | basis |
|---|---|---|---|
| `seed` | 0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `t0` | 1920 | **assumed** | model start 1920 to allow 1980 initial stocks |
| `t1` | 2035 | **assumed** | horizon; 2040 set for the ledger extensions |
| `report_from` | 1960 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `N` | 10000 | **assumed** | cohort scale, no behavioural role |
| `y_sigma` | 0.7 | **estimated** | lognormal income sd from WDI/APIS-type Gini ~0.4-0.5 |
| `y_median` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `subsist0` | 0.75 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `growth` | 0.04 | **estimated** | real index growth vs subsistence; WDI GDP per capita long-run |
| `shock_sigma` | 0.5 | **assumed** | income shock sd |
| `borrow` | 0.5 | **assumed** | annual borrowing capacity as share of income; no direct country series |
| `need_share` | 0.15 | **estimated** | direct child-labour opportunity cost share; ILO/EDB employment context |
| `cct_path` | [[1900, 0.0], [2100, 0.0]] | **sourced** | PHL 4Ps (2008+); switched off elsewhere |
| `tuition_path` | [[1900, 1.0], [2100, 1.0]] | **sourced** | PHL RA 10931 free SUC tuition (2018) |
| `idio_exit` | 0.045 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `rural_cost` | 0.0 | **assumed** | extra post-primary rural cost |
| `urban_path` | [[1945, 1.0], [2035, 1.0]] | **sourced** | WDI SP.URB.TOTL.IN.ZS urban share, interpolated 1945-2035 |
| `cost_pri` | 0.02 | **assumed** | direct primary cost; low and stable |
| `cost_jhs` | 0.05 | **assumed** | direct lower-secondary cost |
| `cost_shs` | 0.05 | **fitted** | fitted in C3 to observed GER/completion |
| `cost_col` | 0.45 | **fitted** | fitted in C3/loop2 to observed GER; bounds 0.3-1.0 |
| `cost_apx` | 0.4 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `prof_cost_extra` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `cap_cost` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `child_wage` | [[9, 0.0], [12, 0.1], [15, 0.3], [18, 0.6], [22, 0.9]] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `child_wage_male_mult` | 1.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `crra` | 1.5 | **assumed** | risk preferences |
| `disc` | 0.93 | **assumed** | discount factor |
| `work_years` | 40 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `adult_age` | 18 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tau` | 0.04 | **assumed** | logit noise in schooling choice |
| `prior_income` | [0.9, 1.0, 1.1, 1.5, 2.2, 3.2, 3.0, 4.0] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `belief_decay` | 0.88 | **assumed** | memory of observed outcomes; E5 shows it is a structural lever |
| `belief_k` | 0.003 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `female_F_shift` | 0.2 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `ses_formatability` | 0.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `w_A` | 0.55 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `w_F` | 0.35 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `q_urban` | 0.15 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `q_inc` | 0.15 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `sigma_exam` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `sigma_self` | 0.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `bar_basic` | -1.8 | **fitted** | fitted in C3 to observed completion |
| `bar_college` | -1.0 | **fitted** | fitted in C3 to observed GER/transition |
| `bar_board` | 0.7 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_cost` | 0.15 | **assumed** | tutoring price per gate-year; no consistent cross-country price series in 04_data |
| `tut_effect` | 0.25 | **assumed** | tutoring score effect; literature cards feed this once TARGETS_SHADOW lands |
| `apex_path` | [[1945, 0.004], [2035, 0.012]] | **fitted** | apex seat scale fitted (apex_mult) in C3 |
| `hc_school` | 0.05 | **fitted** | fitted in C3; near zero implies mostly signalling at the aggregate level |
| `hc_ability` | 0.3 | **assumed** | ability return inside the gray box |
| `mode` | full | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `wage_base` | {"os_prof": 5.0, "elite": 4.5, "mid": 2.6, "os_agency": 2.3, "routine" | **estimated** | sector wage relativities, informal = 1.0 (see LITERATURE_LEDGER) |
| `wage_hc` | {"os_prof": 1.0, "elite": 1.0, "mid": 1.0, "os_agency": 0.5, "routine" | **estimated** | within-sector schooling returns |
| `vac_paths` | {"os_prof": [[1945, 0.0], [2035, 0.0]], "elite": [[1945, 0.01], [2035, | **estimated** | sector vacancy paths inferred from employment shares (EDB/WDI) |
| `employers_per_pool` | 20 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `r_init` | {"elite": 4, "mid": 4, "routine": 3} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `screen_kappa` | 4.7 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fill_margin` | 1.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `r_adjust_p` | 0.25 | **assumed** | employer floor adjustment probability |
| `rho_level` | [0.0, 0.1, 0.1, 0.2, 0.3, 0.8] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `sig_noise` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `lic_bonus` | {"elite": 0.0, "mid": 0.0, "routine": 0.0} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `referral_max` | 0.6 | **assumed** | kin-referral reach; Philippine evidence suggests high |
| `referral_homophily` | {"elite": 1.5, "mid": 0.8, "routine": 0.3} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `referral_min_level` | {"elite": 4, "mid": 3, "routine": 1} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `agency_min_level` | 3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `female_bonus` | {"os_prof": 1.0, "os_agency": 0.1} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `female_penalty` | {"elite": 0.0, "mid": 0.0, "routine": 0.0} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `os_noise` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `formal_growth_scale` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `vac_scale` | {} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_ban` | [] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_ban_leak` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `arch_path` | [[1900, 0.0], [2100, 0.0]] | **sourced** | PHL/atlas overseas registration architecture (MRAs 2004-2016); off elsewhere |
| `p_discretion` | 0.95 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `p_downgrade` | 0.6 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `downgrade_factor` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `arch_visible_from` | 2005 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `recog_lag` | 10 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reform_rule` | never | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reform_year` | 2013 | **sourced** | PHL RA 10533 K-12 (2013); switched off elsewhere |
| `impl_lag` | 3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `capacity_path` | [[1945, 0.55], [1965, 0.8], [2035, 0.95]] | **estimated** | state schooling capacity inferred from observed GER trajectories |
| `capacity_shock` | 0.03 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `cap_threshold` | 0.7 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reform_cost` | 0.004 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `state_horizon` | 25 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `state_disc` | 0.95 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `script_base` | 0.01 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `script_pulse` | 0.15 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `script_events` | [1949, 1990, 2000, 2015] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `belief_mode` | naive | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `diploma_by_years` | False | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `idio_mode` | yearly | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `hc_school_informal` | None | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `informal_crowding` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fair_sigma` | 1.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fair_rel0` | 2.2 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reanchor_share` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reanchor_sticky` | 0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `conformity` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `os_prof_boost_path` | [[1900, 1.0], [2100, 1.0]] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `female_informal_mult` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `anticipate_liquidity` | False | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_access_path` | None | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_max_age` | 35 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_tau` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_forgo` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_cash_share` | 0.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tax_income` | 0.1 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tax_consumption` | 0.12 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `consumption_share` | 0.8 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `remit_share` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `pub_cost` | {"primary": 0.2, "secondary": 0.25, "shs": 0.3, "college": 0.35} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `work_life` | 40 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `macro_elasticity` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `macro_ref_year` | 1980 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `macro_window` | 20 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `macro_lag` | 3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `floor_fixed` | None | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `hc_beta0` | 0.1 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `hc_sigma` | 2.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `support_effect` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `support_share` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `support_target_q` | None | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `support_withhold` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_hc_equiv` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_suppress` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fair_slots_mult` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fair_income_scale` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `prov_capacity` | 0.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `prov_elasticity` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `teacher_capacity` | 0.15 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `teacher_price_mult` | 0.6 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `freeze_schooling` | False | **assumed** | not documented individually: judgement/placeholder, no direct evidence |

## CHN

high capacity, large formal sector, exam gates; no K-12 reform/CCT/overseas architecture; hukou and migration are NOT modelled (structural limitation)

| parameter | value | label | basis |
|---|---|---|---|
| `seed` | 0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `t0` | 1920 | **assumed** | model start 1920 to allow 1980 initial stocks |
| `t1` | 2035 | **assumed** | horizon; 2040 set for the ledger extensions |
| `report_from` | 1960 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `N` | 10000 | **assumed** | cohort scale, no behavioural role |
| `y_sigma` | 0.8 | **estimated** | lognormal income sd from WDI/APIS-type Gini ~0.4-0.5 |
| `y_median` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `subsist0` | 0.75 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `growth` | 0.04 | **estimated** | real index growth vs subsistence; WDI GDP per capita long-run |
| `shock_sigma` | 0.5 | **assumed** | income shock sd |
| `borrow` | 0.5 | **assumed** | annual borrowing capacity as share of income; no direct country series |
| `need_share` | 0.25 | **estimated** | direct child-labour opportunity cost share; ILO/EDB employment context |
| `cct_path` | [[1900, 0.0], [2100, 0.0]] | **sourced** | PHL 4Ps (2008+); switched off elsewhere |
| `tuition_path` | [[2017, 1.0], [2018, 0.5], [2035, 0.5]] | **sourced** | PHL RA 10931 free SUC tuition (2018) |
| `idio_exit` | 0.045 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `rural_cost` | 0.04 | **assumed** | extra post-primary rural cost |
| `urban_path` | [[1945, 0.12], [1980, 0.19], [2000, 0.36], [2010, 0.5], [2035, 0.66]] | **sourced** | WDI SP.URB.TOTL.IN.ZS urban share, interpolated 1945-2035 |
| `cost_pri` | 0.02 | **assumed** | direct primary cost; low and stable |
| `cost_jhs` | 0.05 | **assumed** | direct lower-secondary cost |
| `cost_shs` | 0.04 | **fitted** | fitted in C3 to observed GER/completion |
| `cost_col` | 0.45 | **fitted** | fitted in C3/loop2 to observed GER; bounds 0.3-1.0 |
| `cost_apx` | 0.4 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `prof_cost_extra` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `cap_cost` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `child_wage` | [[9, 0.0], [12, 0.1], [15, 0.3], [18, 0.6], [22, 0.9]] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `child_wage_male_mult` | 1.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `crra` | 1.5 | **assumed** | risk preferences |
| `disc` | 0.93 | **assumed** | discount factor |
| `work_years` | 40 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `adult_age` | 18 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tau` | 0.04 | **assumed** | logit noise in schooling choice |
| `prior_income` | [0.9, 1.0, 1.1, 1.5, 2.2, 3.2, 3.0, 4.0] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `belief_decay` | 0.88 | **assumed** | memory of observed outcomes; E5 shows it is a structural lever |
| `belief_k` | 0.003 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `female_F_shift` | 0.2 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `ses_formatability` | 0.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `w_A` | 0.55 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `w_F` | 0.35 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `q_urban` | 0.15 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `q_inc` | 0.15 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `sigma_exam` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `sigma_self` | 0.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `bar_basic` | -1.8 | **fitted** | fitted in C3 to observed completion |
| `bar_college` | -1.0 | **fitted** | fitted in C3 to observed GER/transition |
| `bar_board` | 0.7 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_cost` | 0.15 | **assumed** | tutoring price per gate-year; no consistent cross-country price series in 04_data |
| `tut_effect` | 0.25 | **assumed** | tutoring score effect; literature cards feed this once TARGETS_SHADOW lands |
| `apex_path` | [[1945, 0.002], [2035, 0.02]] | **fitted** | apex seat scale fitted (apex_mult) in C3 |
| `hc_school` | 0.05 | **fitted** | fitted in C3; near zero implies mostly signalling at the aggregate level |
| `hc_ability` | 0.3 | **assumed** | ability return inside the gray box |
| `mode` | full | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `wage_base` | {"os_prof": 5.0, "elite": 4.5, "mid": 2.6, "os_agency": 2.3, "routine" | **estimated** | sector wage relativities, informal = 1.0 (see LITERATURE_LEDGER) |
| `wage_hc` | {"os_prof": 1.0, "elite": 1.0, "mid": 1.0, "os_agency": 0.5, "routine" | **estimated** | within-sector schooling returns |
| `vac_paths` | {"os_prof": [[1945, 0.0], [2035, 0.0]], "elite": [[1945, 0.01], [2035, | **estimated** | sector vacancy paths inferred from employment shares (EDB/WDI) |
| `employers_per_pool` | 20 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `r_init` | {"elite": 4, "mid": 4, "routine": 3} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `screen_kappa` | 4.7 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fill_margin` | 1.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `r_adjust_p` | 0.25 | **assumed** | employer floor adjustment probability |
| `rho_level` | [0.0, 0.1, 0.1, 0.2, 0.3, 0.8] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `sig_noise` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `lic_bonus` | {"elite": 0.0, "mid": 0.0, "routine": 0.0} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `referral_max` | 0.6 | **assumed** | kin-referral reach; Philippine evidence suggests high |
| `referral_homophily` | {"elite": 1.5, "mid": 0.8, "routine": 0.3} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `referral_min_level` | {"elite": 4, "mid": 3, "routine": 1} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `agency_min_level` | 3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `female_bonus` | {"os_prof": 1.0, "os_agency": 0.1} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `female_penalty` | {"elite": 0.0, "mid": 0.0, "routine": 0.0} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `os_noise` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `formal_growth_scale` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `vac_scale` | {} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_ban` | [] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_ban_leak` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `arch_path` | [[1900, 0.0], [2100, 0.0]] | **sourced** | PHL/atlas overseas registration architecture (MRAs 2004-2016); off elsewhere |
| `p_discretion` | 0.95 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `p_downgrade` | 0.6 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `downgrade_factor` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `arch_visible_from` | 2005 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `recog_lag` | 10 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reform_rule` | never | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reform_year` | 2013 | **sourced** | PHL RA 10533 K-12 (2013); switched off elsewhere |
| `impl_lag` | 3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `capacity_path` | [[1945, 0.25], [1980, 0.45], [2009, 0.7], [2035, 0.92]] | **estimated** | state schooling capacity inferred from observed GER trajectories |
| `capacity_shock` | 0.03 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `cap_threshold` | 0.7 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reform_cost` | 0.004 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `state_horizon` | 25 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `state_disc` | 0.95 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `script_base` | 0.01 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `script_pulse` | 0.15 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `script_events` | [1949, 1990, 2000, 2015] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `belief_mode` | naive | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `diploma_by_years` | False | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `idio_mode` | yearly | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `hc_school_informal` | None | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `informal_crowding` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fair_sigma` | 1.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fair_rel0` | 2.2 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reanchor_share` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `reanchor_sticky` | 0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `conformity` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `os_prof_boost_path` | [[1900, 1.0], [2100, 1.0]] | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `female_informal_mult` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `anticipate_liquidity` | False | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_access_path` | None | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_max_age` | 35 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_tau` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_forgo` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `return_cash_share` | 0.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tax_income` | 0.1 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tax_consumption` | 0.12 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `consumption_share` | 0.8 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `remit_share` | 0.5 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `pub_cost` | {"primary": 0.2, "secondary": 0.25, "shs": 0.3, "college": 0.35} | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `work_life` | 40 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `macro_elasticity` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `macro_ref_year` | 1980 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `macro_window` | 20 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `macro_lag` | 3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `floor_fixed` | None | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `hc_beta0` | 0.1 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `hc_sigma` | 2.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `support_effect` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `support_share` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `support_target_q` | None | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `support_withhold` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_hc_equiv` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `tut_suppress` | 0.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fair_slots_mult` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `fair_income_scale` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `prov_capacity` | 0.3 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `prov_elasticity` | 1.0 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `teacher_capacity` | 0.15 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `teacher_price_mult` | 0.6 | **assumed** | not documented individually: judgement/placeholder, no direct evidence |
| `freeze_schooling` | False | **assumed** | not documented individually: judgement/placeholder, no direct evidence |

