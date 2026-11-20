# MODEL_PLUG_MAP — where each candidate relation plugs into the model

**Author:** `pattern-scout` · 2026-11-20 · task-21. Target code: `05b_experiments/loop2/code/twoway.py` (the loop-2 two-way module) and
`01_sources/massification_project/code/massabm/massabm/{model.py,params.py}` (the case model). Parameter names below are the **actual names in
those files**, read this session — not invented.

**Escalation rule.** A row marked `correlational` may only be used as (a) a *sensitivity range* in an MC, or (b) a *pattern to reproduce*, never as a
calibrated value. A row marked `not identifiable` must stay a declared prior and be reported as such.

## A. `twoway.py` — the loop-2 module

| Relation | Plug point (exact) | Functional form | In-model validation experiment | Grade |
|---|---|---|---|---|
| R01 spending→secondary enrolment | *no state-budget block exists*. Add: `s_t` logit intercept += `b_spend * log(SPEND_t/SPEND_0)`; the budget itself must come from R12 (tax→spend) | logit-linear in log spending, lag 5y (spending at `t-d_spend`, `d_spend=5`) | set `b_spend=0.111` for PH-like/KHM-like, 0.010 for HK-like; raise spend 20% at t=10; require +2.0pp completion; **fail if channel is switched on in HK-like** (R01 heterogeneity) | correlational |
| R02 spending→primary (null) | do **not** add a primary spending channel | — | if the model's primary completion responds >2pp to doubled spend, the spending block is mis-specified | correlational (null) |
| R04 income→tertiary | already in: `feasible_share(cost_col, inc_sig)` and `c_t` | `c_t = sig(logit(c0) + 2.5*(ret_C-ret_Cref)/ANN + ...) * feasible_share(cost_col, inc_sig)` — income acts through the liquidity filter | raise `g` by 1pp/yr for 20y in PH-like; model must deliver ≈+17% tertiary entry (0.848·ln(1.22)); fail if <5% | correlational |
| R05 income→secondary | `s_t` logit, via `fea`/cost, plus the returns term | `s_t = sig(logit(s0) + 2.5*(ret_S-ret_Sref)/ANN + 0.8*prev_take_S + noise)` | +1pp/yr growth for 15y in KHM-like → +5–8pp completion | correlational |
| R07 fertility/cohort size→completion | `births` (country dict) and the pipeline lags (`t-16`, `t-20`) | `S_t = s_t * N*(1+births)^(t-16)` — cohort size enters the denominator directly | lower `births` from 3.0 to 2.0 over 20y; require +7–10pp primary completion (−0.189·ln(3/2)=−7.7%); fail if <2pp | plausibly-causal |
| R09 private provision→enrolment | `n_cm` entry equation (`e_cm`, `F_cm`) | `n_cm ← n_cm*(1 + e_cm*tanh(pi_cm/F_cm))` — entry on profit sign | switch `e_cm` to 0 (R6-style fixed supply) and compare KHM-like vs HK-like fit; the relation predicts a **larger** GER gain from private entry in KHM-like | correlational |
| R13 education→growth (`eps_ec`) | `REGIMES[*]['eps_ec']`, `d_ec` | `Vc_t = Vc0*B0*(1+g)^t*(H_{t-d_ec}/H0)^eps_ec` | run `eps_ec ∈ {0, 0.3, 0.6}`; the FE estimate is −1.035 (R13). Report which arms the PH/KHM 2000–2024 data rejects; do **not** keep 0.6 unexamined | correlational / contrary evidence |
| R21 gate proximity→tutoring | `T_S`, `T_C` positional terms: `+0.7*log(R_S)`, `+0.8*log(R_C)` | `T_S = sig(-1 + shift + 0.9*log1p(ret_S) + 0.7*log(R_S) - 1.1*p/(ret_S+2))` | move a cohort one stage (R_gate ×2); require ≈+35pp take-up (HK 2003 gradient); fail if <10pp | correlational |
| R22 income elasticity of tutoring spend | `inc_sig` (demand dispersion) + price term | income regime shift; the model has no direct income term in `T_S/T_C` — **candidate addition**: `+ b_inc*log(income)` with `b_inc≈0.5–0.7` (spend elasticity 1.33 ⇒ participation elasticity lower) | widen `inc_sig`; top-quintile spend must rise super-proportionally (≈1.3) | correlational |
| R23 extensive vs intensive margin | needs a **second margin**: `quality` and `cap_*` are the only intensive margins today | add `spend_per_user = p_tut * hours` and let `hours` rise with gate proximity while participation falls (Korea fact) | require 86→66% participation *and* +23% spend across levels; a one-margin block cannot | correlational |
| R24 urban→tutoring | **absent** in `twoway.py`; `massabm` has `urban_path`, `q_urban` | add `+b_urb*urban_t` to the `T_S` index (b_urb from JPN 2.62× / KHM 2.29× gradients) | require 2× urban/rural take-up ratio | correlational |
| R25 Double Reduction | `n_cm` collapse (`F_cm` → prohibitive, or `shadow='fixed_supply'` with a ban) | shock `n_cm→0.2` at 2021 | model predicts rerouting into `n_tt` (teacher-tutors); no data confirm yet — flag as P4-pending | not identifiable |
| R26 returns→tutoring | `+0.9*log1p(ret_S)` in `T_S` — **currently a prior with no estimate behind it** | as coded | sensitivity on the 0.9 coefficient {0.4, 0.9, 1.4}; this is the model's weakest link (R26) | not identifiable |
| R29 tutoring price elasticity | `-1.1*(p_tut/max(ret+2,0.5))` — **a declared prior** | as coded | arms at {−0.5, −1.1, −2.0}; report survival | not identifiable |

## B. `massabm` — the Philippines case model

| Relation | Plug point (exact) | Functional form | Validation experiment | Grade |
|---|---|---|---|---|
| R01/R12 fiscal space | `fiscal.py`: `tax_income`, `tax_consumption`, plus `params['cost_jhs']`, `cost_shs`, `cap_cost` | state capacity `K` raises unit cost: `1 + cap_cost*(1-K)`; spending path feeds `cct_path`/`tuition_path` analogues | tax take +3pp in a KHM-like preset (KHM has no preset — requires building one) → +1.2% education spend; fiscal NPV must stay coherent | correlational |
| R07 cohort size | `N` (children entering each year), `births` analogue in the pipeline | cohort size scales the denominator of completion | births −1.0 over 20y → +7.7pp primary completion | plausibly-causal |
| R18 K-12 (RA 10533) | `params` K-12 rule + `cost_shs`; `round3_mechanisms` already has a "surge" arm | two extra years for the SHS tier; GER denominator changes | the model must reproduce **no total-GER jump** (observed −2.4%, ns) with an upper-secondary level shift; if it produces a total-GER surge, the accounting is wrong | plausibly-causal (null) |
| R19 free SUC tuition | `tuition_path=[(2017,1.0),(2018,0.5),(2035,0.5)]` | college-cost multiplier | the model must show a **dip then recovery** in tertiary entry because of the K-12 cohort delay (observed −28.9% at 2018); an immediate jump is falsified by the data | correlational |
| R28 nurse licensing→migration | `os_prof` vacancy pool + board exam supply (`bar_board`, `lic_bonus`) | `lic_bonus` and the licensing pass route | the existing `nurse_check` fails (0.25 vs 9 licensed per migrant). This is the model's **largest documented miss** and remains open | plausibly-causal |
| R30 school construction | capacity/`places` and `rural_cost` | places constraint per level | build schools at t=5 in a KHM-like preset; expect +0.1–0.2 years of schooling | unverified (R30) |
| R10 teacher supply | **absent as a separate stock**; capacity is implicit in `places` | candidate: add `teacher_stock_t` and a capacity constraint `min(places, teacher_stock/max_ptr)` | binding only where income/tax capacity is low (R10 heterogeneity) | correlational |

## C. What should NOT be plugged in, and why

1. **`eps_ec = 0.6` as a calibrated value.** The 30-country FE estimate is −1.035 (se 0.240) at a 15-year lag (R13). The model may keep
   `eps_ec>0` as a theoretical regime, but it must also report the demand-led arm (`R1_demand_led`, `eps_ec=0`) as an equal candidate — the
   panel does not support a positive education→growth elasticity in this specification.
2. **The pupil-teacher ratio**, in either direction (R11): levels and first differences disagree in sign. Use it only as a capacity constraint.
3. **The spending elasticity as a single number**: it is 0.189 in Asia, 0.010 outside, and ~0 above near-universal enrolment. Wire the
   **country-type switch**, not the pooled value.
4. **Returns→tutoring coefficient (0.9)** and **price elasticity (−1.1)**: both are priors with no identified estimate. Declare them as priors.

## D. Priority order for the modellers

1. **R13** (test `eps_ec` honestly) — it changes the model's central claim, and the panel points the other way.
2. **R18/R19** (K-12 and free tuition as *confounded* events) — the Philippines case rests on them.
3. **R21/R23** (gate gradient + two-margin tutoring) — the shadow sector's demand side.
4. **R09/R01 conditional on country type** — the heteronomy the Council asked for.
5. Everything else: sensitivity range or pattern to reproduce.

## E. Economic complexity (task-28) — a country index, not a mechanism

**What is on disk:** `data/economic_complexity_panel.csv` (6 ctys x 1995-2024, 27 columns, ready to ingest: `eci_hs92` primary + `eci_sitc` robustness + derived `eci_pctile`, `eci_z_year`, `eci_growth_5y`, `complexity_gap`, `complexity_quadrant`, merged education/economy columns).

| Relation (register id) | Plug point (exact) | Functional form | In-model validation | Grade |
|---|---|---|---|---|
| R41 ECI -> tertiary GER | `twoway.py`: `Vc0` (complex vacancies) and the `c_t` logit. Complexity shifts the *level* of complex demand, not the elasticity | `Vc += b_eci * (ECI_t - ECI_1995)`, b_eci calibrated from 0.23-0.31 log points per ECI point, **but** the income control absorbs it, so prefer `Vc0` scaling by country | raise ECI alone with income fixed; tertiary entry should barely move (data: 0.120, ns) | correlational |
| R42 ECI -> completion | `massabm` `bar_basic` / completion floor; `twoway` `s_t` intercept | level shift in the completion logit: `+0.139*(ECI_t-ECI_1995)` | hold income fixed, raise ECI 1 point -> +14% completion; if the model's ECI term is a relabelled income term it double-counts | correlational |
| R43 ECI -> secondary GER | `twoway` `s_t` intercept | as above, lower-secondary margin only (upper-secondary ns) | separate lower and senior gates in the response | correlational |
| R44 ECI -> formal share | `twoway` complex-vs-routine job split; `massabm` formal/informal shares | `formal_share += b*(ECI)` with b≈+0.03/point, **not significant** — treat as a sign prior, not a parameter | the model must not make complexity the formalisation driver; the income->formal channel is far stronger (6.11, se 1.54) | low |
| R45 ECI -> growth | **do not plug** | the Growth Lab premium does not replicate (-0.142, se 0.105) | run the same 10y regression on model output; a positive premium the data lack = over-fit to literature | null |
| R47 ECI x spending | **do not add** | the interaction is a clean null (0.081, se 0.080) | spending shocks in high- vs low-ECI presets must differ only via income/tax capacity | null |
| R48 ECI x schooling -> growth | `twoway` `eps_ec` / `ret_S`, `ret_C`; `massabm` `wage_hc` | if returns are made complexity-dependent: `eps_ec(ECI) = eps0 - 0.077*ECI` (the data sign), **not** `eps0 + k*ECI` | run rising vs falling returns-in-complexity; the data favour falling. If the model needs rising to fit the four countries, report that as a finding | low-medium |

**Hard caveats from `04_data/complexity/COMPLEXITY_MAP.md`, restated because they matter:** complexity is a *country-level index*, not a mechanism; it may condition or proxy latent capability, never identify a causal effect. Do not treat ECI as schooling or education quality; do not use rank changes as level changes; do not splice SITC/HS92/HS12; do not claim complexity causes education demand (it is endogenous to income, schooling and industrial policy); do not use `growth_proj` as evidence for an education->growth effect.
