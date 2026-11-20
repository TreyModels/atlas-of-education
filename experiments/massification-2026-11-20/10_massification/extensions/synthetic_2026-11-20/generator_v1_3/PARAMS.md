# PARAMS — declared parameters of the v1.3 shadow-education-at-the-gates module

**LABEL: SYNTHETIC / DECLARED.** This is a declared-assumption parameter table. It contains no result, no estimate, no fit, and nothing about any real country. `SYN_HKG_LIKE`, `SYN_PHL_LIKE` and `SYN_KHM_LIKE` are synthetic country types, not Hong Kong, the Philippines or Cambodia.

Generated from the frozen `shadow_module/PARAMETERS.csv` by `_scratch/build_params.py`; the table below is that file's 42 rows, reproduced mechanically, so there is one source of truth. `code/sim_v1_3.py` refuses to run unless this file's sha256 matches the value frozen in its header.

## 0. Frozen identities

| object | sha256 |
|---|---|
| `shadow_module/PRE_DECLARATIONS.md` (frozen v1.3 spec) | `cf8c61cb818cd63acfb2ada594bc9541bfcb0711f801e13b7eee3b86508f94f2` |
| `shadow_module/PRE_DECLARATIONS_S1_NOTE.md` (binding controller note) | `af49a616a7b57c4ef23a693c155d022cd17817f66f5acafba4dc6798dedb65eb` |
| `shadow_module/PARAMETERS.csv` (this table's source) | `cb49d3197b911451f8b1e32080fbe6d095f181440572e1a2b72005dc4302703a` |
| `generator_v1_2/code/sim_v1_2.py` (inherited code) | `61123aa9370a407487407bf3ff4b97287aea67cac5f90629e540a6e8cc855e7c` |
| `generator_v1_2/results/synthetic_panel_v1_2.csv` (c6 reference) | `14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac` |
| `IMPLEMENTATION_NOTE.md` (spec-gap resolutions, pre-run) | `b367b7daa85f126f359b2c9bd2c3fff37e20361700502241402bc2bcee16153a` |

## 1. The demand equation (frozen, PRE_DECLARATIONS.md §4)

```
p_{i,c,g,q,t} = sigma( a_g + b_Z ln R_{c,g,t} + b_V ln(1+V_{c,g}) + b_D ln(1+Delta-pi_{c,g,t})
                       + b_y ln(y_{c,q,t}/ybar_{c,t}) - b_F ln(1 + s_{c,g}/(y_{c,q,t}/ybar_{c,t})) )
D_{c,g,t}   = sum_q omega_q p_{c,g,q,t}          omega_q = 0.2 (equal quintile weights)
S_{c,g,t}   = D_{c,g,t} * s_c                     (declared fee units = shares of mean monthly
                                                   household income; no currency conversion exists)
D*_{c,t}    = sum_{g in g1,g2,g3} nu_{c,g} D_{c,g,t}   (cohort incidence; g0 never enters)
Pi_{c,g,t}  = (1-D) pi0 + D pi1                   |Pi - pi0| <= delta_g (1 - pi0)
R_{c,g,t}   = (1+Q)^0.40 (1/pi0)^0.40 kappa^0.20   clipped [1,20]
V_{c,g}     = phi_c r_EAP DeltaS_g H  (g1-g3);  V_{c,g4} = phi_c G_c H;  V_{c,g0} = 0
Delta-pi    = pi1 - pi0 = delta_g (1 - pi0),  pi1 = min(0.999, pi0 + delta_g (1-pi0))
```

**One behavioural rule for every country.** There is no country-specific value of `a_g, b_Z, b_V, b_D, b_y, b_F, delta_g` anywhere in the code; `c4c` audits the behavioural functions for exactly that. Country variation enters only through `phi, s, sigma, nu` (§3 below).

## 2. The 42 declared rows (verbatim from `PARAMETERS.csv`)

| id | symbol | meaning | value / range | unit | provenance | evidence file:line | enters | notes |
|---|---|---|---|---|---|---|---|---|
| B01 | `a_0` | pre-gate intercept (no positional good) | -4.80 (fixed) | logit | DECLARED |  | Theta intercept, g0 only | Sets the non-positional baseline: with R=1.02, V=0, Delta-pi=0.0006 at mean income this gives ~1% participation. Never enters D* scoring. |
| B02 | `a_g` | gate intercepts g1-g4 (one shared value, no country variation) | -2.80 (fixed) | logit | DECLARED |  | Theta intercept, g1-g4 | Identical for all four gates and all three country types. c4c voids the run if any country-specific value exists. |
| B03 | `b_Z` | coefficient on ln R (gate pressure) | 2.00; sensitivity {1.2, 2.0, 2.8} | logit per ln unit | DECLARED | 09_relations/RELATION_CANDIDATES.csv R21 (shape and calibration test only) | b_Z * ln R | R21 supplies the gate-gradient structure and its implied test (R doubled -> +35 pp at p~0.40 implies b_Z ~ 2.0 on ln R); R21's own stated coefficient (+0.7*log R_S) cannot deliver its own test, which is why the value is declared from the test, not the stated coefficient. |
| B04 | `b_V` | coefficient on ln(1+V) (credential return) | 1.00; sensitivity {0.5, 1.0, 1.5} | logit per ln unit | DECLARED | 09_relations/RELATION_CANDIDATES.csv R26 | b_V * ln(1+V) | R26 records returns->tutoring demand as NOT IDENTIFIABLE and requires the coefficient to stay a prior; its stated prior (0.9) is on log1p(ret) in a different model and is not numerically transferable, so 1.0 is declared and sensitivity-tested. |
| B05 | `b_Delta` | coefficient on ln(1+Delta-pi) (tutoring lift) | 2.00; sensitivity {1.0, 2.0, 3.0} | logit per ln unit | DECLARED |  | b_Delta * ln(1+Delta-pi) | Delta-pi is small in magnitude (0.01-0.2), so this term contributes <=0.4 logit; it is the gate-stakes channel but NOT the dominant one. |
| B06 | `b_y` | coefficient on household income position | 0.60; sensitivity {0.3, 0.6, 0.9} | logit per ln unit | DECLARED | 09_relations/data/shadow_gradients.csv:8 (direction only) | b_y * ln(y_q / ybar) | KOR income elasticity of tutoring EXPENDITURE is 1.33 (R22); that is a spend elasticity, not a participation coefficient, so only the direction is borrowed. |
| B07 | `b_F` | coefficient on fee burden | 0.80; sensitivity {0.4, 0.8, 1.2} | logit per ln unit | DECLARED | 04_data/shadow_round2/SHADOW_DATA.md sec.6 (HKG 1.1-5.0% of income) | -b_F * ln(1 + s/(y_q/ybar)) | No tutoring price elasticity is identified anywhere in the package (R29); this is a burden coefficient, not a price elasticity. |
| B08 | `delta_g1` | tutoring lift fraction at GATE-LS | 0.30; sensitivity {0.15, 0.30, 0.45} | share of failure gap | DECLARED |  | Delta-pi = delta*(1-pi0) at g1 | MOST EXPOSED DECLARED PARAMETER: no estimate of tutoring's effect on transition probability exists in this package. Sensitivity is mandatory. |
| B09 | `delta_g2` | tutoring lift fraction at GATE-US | 0.30; sensitivity {0.15, 0.30, 0.45} | share of failure gap | DECLARED |  | Delta-pi at g2 |  |
| B10 | `delta_g3` | tutoring lift fraction at GATE-TER | 0.25; sensitivity {0.15, 0.30, 0.45} | share of failure gap | DECLARED |  | Delta-pi at g3 |  |
| B11 | `delta_g4` | tutoring lift fraction at GATE-JOB | 0.20; sensitivity {0.15, 0.30, 0.45} | share of failure gap | DECLARED |  | Delta-pi at g4 |  |
| B12 | `delta_g0` | tutoring lift fraction at PRE-GATE | 0.02 (fixed) | share of failure gap | DECLARED |  | Delta-pi at g0 | Declared as negligible because a non-gate does not screen; this is what makes c3 a consistency check rather than a prediction. |
| B13 | `w_Q` | weight on queue-per-place in R | 0.40 (fixed) | weight | DECLARED |  | R = (1+Q)^w_Q * (1/pi0)^w_pi * kappa^w_kappa |  |
| B14 | `w_pi` | weight on 1/pi0 in R | 0.40 (fixed) | weight | DECLARED |  | same |  |
| B15 | `w_kappa` | weight on credential rank in R | 0.20 (fixed) | weight | DECLARED |  | same | Smaller because kappa is the least reliably measured of the three components. |
| B16 | `r_EAP` | East Asia & Pacific private Mincer return | 0.087 (fixed) | per year of schooling | OBSERVED (compiled; calibration-only) | 02_lit/ECON_TARGETS.csv:3 | V = phi * r_EAP * DeltaS * H | Psacharopoulos & Patrinos 2018 (WB PRWP 8402), regional table; a compilation of Mincer cross-sections, explicitly NOT causal. ECON_LIT sec.1.2 warns no country return is available on disk. |
| B17 | `H` | present-value-equivalent working years used to capitalise the credential | 20; sensitivity {10, 20, 30} | years | DECLARED |  | V = phi * r_EAP * DeltaS * H | Undiscounted capitalisation would overstate; 20 is a declared mid-point and is sensitivity-tested. |
| B18 | `DeltaS_g1` | declared years added by the lower-secondary credential | 3 | years | DERIVED |  | V at g1 | Standard level durations in the v1.2 cohort flow (primary 6, lower-sec 3, upper-sec 3, tertiary 4). |
| B19 | `DeltaS_g2` | declared years added by the upper-secondary credential | 3 | years | DERIVED |  | V at g2 |  |
| B20 | `DeltaS_g3` | declared years added by the tertiary credential | 4 | years | DERIVED |  | V at g3 |  |
| B21 | `G_c` | formal-rung log-wage gap used for g4 (placeholder for the v1.2 wage block) | 0.55; sensitivity {0.35, 0.55, 0.75} | log points | DECLARED |  | V at g4 (V = phi * G_c * H) | Replaced in v1.3 by the model's own ln(w_for[rung 2]/w_inf). No on-disk wage-premium series exists (PARAMETER_MAP: 'wage premium by education level' = not observable). |
| B22 | `omega_q` | quintile weights for aggregating p to D | 0.20 x 5 (fixed) | share | DECLARED |  | D = sum_q omega_q * p_q | Equal weights; no on-disk income-share data for these three systems. |
| B23 | `z_q` | quintile midpoints of the standard normal used to lay out the income distribution | -1.2816, -0.5244, 0, 0.5244, 1.2816 (fixed) | z | DECLARED |  | y_q/ybar = exp(sigma_c*z_q) normalised to mean 1 |  |
| B24 | `seed` | PCG64 seed for any stochastic element | 20261120 | integer | BORROWED-FROM-SHADOW-RECORD (v1.2 convention) | 10_massification/extensions/synthetic_2026-11-20/v1_2/PRE_DECLARATIONS.md sec.6 | RNG | Two clean runs must be byte-identical. The module is deterministic conditional on inputs; the seed is inherited, not new. |
| C01 | `phi_HKG` | 1 - vulnerable employment share, HKG 2019 | 0.940 | probability | OBSERVED (DECLARED interpretation) | 04_data/ECONOMY_SERIES.csv (Vulnerable employment 6.007% in 2019; WDI/ILO modelled) | V = phi * ... | Proxy for 'probability a credential is rewarded in wage work'. PARAMETER_MAP warns status of employment is NOT formality, so the interpretation is declared. |
| C02 | `phi_PHL` | 1 - vulnerable employment share, PHL 2019 | 0.677 | probability | OBSERVED (DECLARED interpretation) | 04_data/ECONOMY_SERIES.csv (Vulnerable employment 32.298% in 2019) | V = phi * ... | same |
| C03 | `phi_KHM` | 1 - vulnerable employment share, KHM 2019 | 0.464 | probability | OBSERVED (DECLARED interpretation) | 04_data/ECONOMY_SERIES.csv (Vulnerable employment 53.634% in 2019) | V = phi * ... | Also on disk: KHM formal share 11.7% (CLFS 2019, ILO definition; 04_data/econ_round2/PARAMETER_MAP.csv) - used as a SENSITIVITY for KHM only, not as the primary value, because no equivalent formal-share series exists for HKG/PHL. |
| C04 | `s_HKG` | fee as share of mean monthly household income | 0.0305 | share of income | DERIVED | 04_data/shadow_round2/SHADOW_DATA.md sec.6 ("fees consumed 1.1-5.0% of monthly household income") | -b_F * ln(1 + s/(y_q/ybar)) | Midpoint of the observed 1.1-5.0% band (Bray & Kwok 2003, n=630, six schools). |
| C05 | `s_PHL` | fee as share of mean monthly household income | 0.0400; sensitivity {0.02, 0.04, 0.07} | share of income | DECLARED | 04_data/shadow_round2/SHADOW_DATA.md sec.3 and sec.7 ("no PH fee number is asserted"; "no PH fee series exist") | same | FLAGGED: no Philippine fee series is on disk. This is the module's second most exposed country input. |
| C06 | `s_KHM` | fee as share of mean monthly household income | 0.0210; sensitivity {0.01, 0.021, 0.04} | share of income | DERIVED (fee level) + DECLARED (income share) | 04_data/shadow_round2/SHADOW_DATA.md sec.5 (500-1,000 Riel per session, approx US$0.13-0.25) | same | Arithmetic: 750 Riel/session (midpoint) x 16 declared sessions/month = 12,000 Riel = US$2.96/month (4,050 Riel/US$). The conversion to an income SHARE is declared: no KHM household-income series is on disk. |
| C07 | `sigma_HKG` | income dispersion (lognormal sd of ln household income) | 0.55; sensitivity {0.40, 0.55, 0.70} | log units | DECLARED |  | y_q/ybar lay-out | FLAGGED: no Gini or income-share series exists on disk for any of the three systems (04_data/ECONOMY_SERIES.csv carries vulnerable/wage employment and GDP pc only). |
| C08 | `sigma_PHL` | income dispersion | 0.80; sensitivity {0.60, 0.80, 1.00} | log units | DECLARED |  | same | Declared higher than HKG; cannot be grounded on disk. |
| C09 | `sigma_KHM` | income dispersion | 0.75; sensitivity {0.55, 0.75, 0.95} | log units | DECLARED |  | same |  |
| C10 | `nu_HKG` | declared cohort-exposure weights across g1,g2,g3 | 0.10, 0.62, 0.22 (sum 0.94) | share of cohort | DERIVED from OBSERVED + DECLARED split | 10_massification/data/UNIVERSALIZATION_SERIES.csv (oos_upper_secondary HKG 2020 = 5.428%); split across gates DECLARED | D* = sum_g nu_g * D_g | Sum = 1 - oos_upper. The split of in-school youth across the three gates is declared, constrained to that sum. |
| C11 | `nu_PHL` | declared cohort-exposure weights across g1,g2,g3 | 0.30, 0.35, 0.10 (sum 0.75) | share of cohort | DERIVED from OBSERVED + DECLARED split | UNIVERSALIZATION_SERIES.csv (oos_upper_secondary PHL 2020 = 24.737%) | same |  |
| C12 | `nu_KHM` | declared cohort-exposure weights across g1,g2,g3 | 0.28, 0.13, 0.02 (sum 0.43) | share of cohort | DERIVED from OBSERVED + DECLARED split | UNIVERSALIZATION_SERIES.csv (oos_upper_secondary KHM 2020 = 56.987%); also oos_lower_secondary 20.29%, completion_upper_secondary 22.03% | same | This is the input that carries 'KHM low' on the national statistic: only ~43% of the cohort is in school at gate age. It does NOT make KHM's gate-conditional demand low. |
| C13 | `oos_upper` | observed upper-secondary-age out-of-school rate (2020) | HKG 5.428; PHL 24.737; KHM 56.987 | percent | OBSERVED | 10_massification/data/UNIVERSALIZATION_SERIES.csv (indicator oos_upper_secondary; UIS SDG4 release 2026-11) | constrains nu | UIS SDG4 definition; not the same object as tutoring participation and never used as one. |
| T01 | `c1_threshold_pp` | R-doubling experiment at g2 must raise D by at least this much | 10.0 | percentage points | THRESHOLD (not a parameter) | PRE_DECLARATIONS.md sec.8 c1 | scored | Weaker than R21's implied +35 pp because the module's households also respond to V and the fee; declared before any run. |
| T02 | `c2_threshold_pp` | +25% on phi at g2 must raise D by at least this much | 2.0 | percentage points | THRESHOLD | PRE_DECLARATIONS.md sec.8 c2 | scored |  |
| T03 | `c3_threshold_share` | pre-gate participation ceiling | 0.025 | share | THRESHOLD | PRE_DECLARATIONS.md sec.8 c3 | scored | Plus D_g0 <= 0.20 * D_g1 in every country-year. |
| T04 | `c4a_band` | HKG g2 participation band | [0.75, 0.95] | share | THRESHOLD | PRE_DECLARATIONS.md sec.8 c4a | scored | 85% +/- 10 pp, widened for the source's low/medium confidence and disputed denominator. |
| T05 | `c4b_gaps` | required D* ordering gaps | HKG-PHL >= 0.10; PHL-KHM >= 0.05 | share | THRESHOLD | PRE_DECLARATIONS.md sec.8 c4b | scored |  |

## 3. Country input bundles (the ONLY country-varying quantities)

| input | SYN_HKG_LIKE | SYN_PHL_LIKE | SYN_KHM_LIKE | label |
|---|---|---|---|---|
| `phi_c` = 1 − vulnerable employment (2019) | 0.940 | 0.677 | 0.464 | OBSERVED (WDI/ILO), DECLARED interpretation |
| fee share `s_c` of mean monthly household income | 0.0305 | 0.0400 | 0.0210 | DERIVED / DECLARED / DERIVED |
| income dispersion `sigma_c` | 0.55 | 0.80 | 0.75 | DECLARED (no Gini series on disk) |
| cohort weights `nu_{c,1}, nu_{c,2}, nu_{c,3}` | 0.10, 0.62, 0.22 (0.94) | 0.30, 0.35, 0.10 (0.75) | 0.28, 0.13, 0.02 (0.43) | DERIVED from observed UIS out-of-school + DECLARED split |
| observed out-of-school at upper-secondary age (2020) | 5.428% | 24.737% | 56.987% | OBSERVED (UIS SDG4) |

## 4. Host mapping (which v1.2 country carries which declared bundle)

The frozen v1.2 generator contains no HKG-like and no KHM-like country, so the shadow block is layered on the gate state of three designated v1.2 countries. The rule is **shadow-blind** (it reads 2020 GDP per capita, which is not an argument of the demand equation) and is fixed in `IMPLEMENTATION_NOTE.md` §1 before any shadow output exists:

| declared type | host | rule |
|---|---|---|
| `SYN_PHL_LIKE` | `SYN00_PHL_LIKE` | v1.2's own declared PHL-informed country |
| `SYN_HKG_LIKE` | the country with the highest 2020 `gdppc` | HKG is the high-income system |
| `SYN_KHM_LIKE` | the country with the lowest 2020 `gdppc` | KHM is the poorest system |

Resolved names are written to `results/shadow_country_inputs_audit.csv` and `RUN_MANIFEST.json`. No v1.2 parameter, path, draw or arithmetic is altered by this mapping; the host country is generated by the frozen v1.2 code exactly as delivered.

## 5. Inherited v1.2 parameters read by the gate-state extractor (unchanged)

Read-only, never re-fitted: `phys_cap = 1.15`, `overage_cap = 1.05`, `rank_gain = 0.20`, `seek = (0.15,0.35,0.60,0.80)`, `queue_retain = 0.50`, `sep = (0.10,0.07,0.05,0.04)`, `rung_mult = (2.20,3.20,4.60,6.40)`, `cred_prem = 0.10`, `psi = (0.02,0.22,0.12)`. The gate contract is `IMPLEMENTATION_NOTE.md` §2; `generator_v1_2/PARAMS.md` is the authoritative v1.2 table and is not reproduced here.

## 6. Freeze declaration

These values were frozen by `shadow_module/PRE_DECLARATIONS.md` before any v1.3 run. This worker changed none of them. The central-value run is the scored run; the pre-declared one-at-a-time sensitivity grid is reported beside it and cannot replace it. A FAIL is reported as a FAIL and is never rescued by re-parameterising.

Seed `20261120` (PCG64, inherited from v1.2); floats `%.10g`; two clean runs byte-identical.

