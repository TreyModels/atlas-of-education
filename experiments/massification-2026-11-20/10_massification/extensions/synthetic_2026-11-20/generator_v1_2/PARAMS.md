# PARAMS — every declared parameter of the SYNTHETIC generator v1.2, with provenance

**`LABEL: SYNTHETIC.`** This file documents a declared-assumption simulator. Nothing here is estimated,
nothing here is evidence about any country, and no number below licenses a causal or direction claim. No
real country is modelled. The observed numbers that appear are either (i) **declared input paths** (the
PHL demographic path, explicitly allowed by the frozen spec) or (ii) **benchmarks reported for context**,
never encoded as targets. The only fitted object anywhere is a design-phase choice of declared
parameter values, disclosed in [`TUNE_LOG.md`](TUNE_LOG.md).

Files: [`code/sim_v1_2.py`](code/sim_v1_2.py) · [`RUN_MANIFEST.json`](RUN_MANIFEST.json) ·
[`TUNE_LOG.md`](TUNE_LOG.md) · [`FINDINGS.md`](FINDINGS.md) · [`results/`](results/)

> **Authoritative copy.** `RUN_MANIFEST.json → params` is written by the generator from the module-level
> `P` block in `code/sim_v1_2.py`. This file is the human-readable mirror plus material the manifest
> cannot carry: units, provenance, the supply-rule statement, the code-inspection statement and the
> frozen scoring rules. **Frozen before the scored run**; this file's sha256 is recorded in the manifest.

Source vocabulary (one token per row):

| token | meaning |
|---|---|
| `OBSERVED-INPUT` | an observed series enters the simulation numerically as a **declared input path** (never fitted at runtime) |
| `DECLARED` | chosen for v1.2 by design; no estimate exists. **The majority.** |
| `BORROWED-FROM-ATLAS-STRUCTURAL` | structure / parameter name only, from `engine/childworld.py`; **no value** is imported |
| `CONVENTION` | accounting identity, definitional constant or measurement convention |

---

## 1. Panel, seed, determinism

| item | value | unit | source |
|---|---|---|---|
| seed | `20261120` | — | DECLARED (single numpy PCG64 stream) |
| countries | 30 synthetic (`SYN00_PHL_LIKE`, `SYN01_TWIN_MFG`, `SYN02_TWIN_OFFICE`, `SYN10_BOOM`, `SYN11_FLAT`, `SYN12_DECLINE`, `SYN03…SYN29`) | count | DECLARED |
| years | 1970–2025 | year | DECLARED |
| levels | primary, lower_secondary, upper_secondary, tertiary | — | DECLARED |
| panel rows | 30 × 56 × 4 = **6 720** | rows | CONVENTION |
| label | `SYNTHETIC` in every row and every results file | — | CONVENTION |
| floats | written at `%.10g` | — | CONVENTION |
| runtime | ≈0.6 s per run (measured; < 5 min contract) | s | measured |

The generator **refuses to run** if `v1_2/PRE_DECLARATIONS.md` sha256 ≠
`fde18d405d875167977b350a925c28248c3007d2813dcdb29219d3baf0b95f16` (the frozen value embedded in the code).

---

## 2. Declared inputs (OBSERVED-INPUT; never fitted at runtime)

| input | file | how it enters | source |
|---|---|---|---|
| PHL annual school-age cohort path | `10_massification/data/UNIVERSALIZATION_SERIES.csv`, `cohort_population_0_14` (PHL, 1995–2024) | used **directly** as `S(t)` for `SYN00_PHL_LIKE`; 1970–1994 extrapolated at a declared 2.45 %/yr backwards, 2025 at a declared −0.8 %/yr | OBSERVED-INPUT (shape) + DECLARED (extrapolation) |
| PHL population path | same file, `population_total` (1995–2024) | used directly for the population/labour-force stock; 1970–1994 at a declared 2.5 %/yr backwards, 2025 at +1.0 %/yr | OBSERVED-INPUT (shape) + DECLARED (extrapolation) |
| PHL cohort/pop levels for the other synthetics | — | 27 countries: `S(t)=S0·Π(1+g_phase)`, three declared growth phases (breaks 1985, 2005); `SYN10/11/12` share one base country and differ only in the declared cohort path (boom = PHL shape scaled; flat; decline −0.9 %/yr) | DECLARED |

**Read, hashed, and used only as rationale/benchmark — never encoded numerically:**

| file | why it is in the manifest |
|---|---|
| `10_massification/data/SCHOOL_EXPANSION.csv` | teacher/classroom/PTR context for the declared build-out story |
| `10_massification/data/STATE_CAPACITY.csv` | observed PHL primary PTR (35.07 in 2005 → 29.08 in 2017) and education spending (2.33 → 3.96 % GDP) are reported **as the benchmark in check (c)** and as the rationale for the declared build-out timing. They set no parameter. |
| `data/gmr_observed_6countries_1970_2024.csv` | declared reference series for the programme; not encoded |
| `09_relations/data/economic_complexity_panel_30ctys.csv` | declared ECI reference; **no panel value is copied into the synthetic `X`** |

No observed PHL completion, GER or OOS value is encoded anywhere. There is **no** per-level anchor array,
no interpolation through observed completion years, and no PHL-specific supply branch.

---

## 3. Layer 1b — demographics

| parameter | value | unit | source |
|---|---|---|---|
| `band_share` | (0.42, 0.21, 0.20, 0.17) | split of the school-age cohort across levels | DECLARED |
| level duration `dur` | (6, 3, 3, 4) | years | CONVENTION |
| annual cohort | `C_L(t) = band_share_L · S(t) / dur_L` | persons/yr | CONVENTION |

`S(t)` is the declared school-age cohort index (the observed PHL `cohort_population_0_14` shape for
`SYN00`). The baby boom is a property of this **input**, not of the model: no fertility model, no fitting.

---

## 4. Layer 1c — capacity with a lag, congestion, quality

### 4.1 The single supply rule (applied to every country and level)

```
B_L(t)       = 1 / (1 + exp(-(t - (seat_t50_L + dshift_c)) / seat_width_L))     build-out level
cover_L(t)   = cover_lo_L + (cover_hi_L - cover_lo_L) · B_L(t)                   declared coverage path
desired_L(t) = cap0_c · cover_L(t) · C_L(t - seat_lag_L)                         desired places
seats_L(t)   = max(0, seats_L(t-1) + seat_resp_L · (desired_L(t) - seats_L(t-1))) seats adjust with lag
q_L(t)       = C_L(t) / seats_L(t)                                               congestion (frozen spec)
Q_L(t)       = exp(-gamma · max(0, q_L(t) - 1))                                  quality (frozen spec)
class_L(t)   = class_target_L · max(1, q_L(t))                                   class size
surv_L(t)    = clip(surv_max_L · Q_L(t)^surv_theta_L, 0.02, 0.995)               quality feeds survival
```

`seats` are **adequate single-shift places**; enrolment may exceed them up to `phys_cap` through double
shifts, which is why a system can have high GER and congested quality at the same time. Completion is a
cohort-flow object (`adm_off/C` at entry × survival now), never a product of fitted probabilities.

| parameter | value | unit | source |
|---|---|---|---|
| `init_cover` | (0.90, 0.55, 0.30, 0.08) | 1970 adequate places / cohort | DECLARED |
| `seat_lag` | (4, 5, 5, 6) | years | DECLARED |
| `seat_resp` | (0.45, 0.40, 0.35, 0.30) | annual convergence | DECLARED |
| `cover_lo` | (0.72, 0.55, 0.45, 0.10) | places / cohort, early | DECLARED |
| `cover_hi` | (0.90, 1.25, 1.00, 0.85) | places / cohort, late | DECLARED |
| `seat_t50` | (2003, 2024, 2010, 2000) | build-out centre by level (years) | DECLARED |
| `seat_width` | (12, 5, 10, 12) | build-out width (years) | DECLARED |
| `phys_cap` | 1.15 | max pupils per adequate place | DECLARED |
| `overage_cap` | 1.05 | GER hard cap | CONVENTION (Z1 gate) |
| `oa_rate` | (0.08, 0.06, 0.05, 0.04) | over-age applicants / cohort | DECLARED |
| `gamma` | 0.55 | quality decay on congestion | DECLARED |
| `surv_max` | (0.96, 0.91, 0.90, 0.90) | survival at zero congestion | DECLARED |
| `surv_theta` | (1.0, 1.0, 1.0, 0.80) | survival elasticity to Q | DECLARED |
| `learn_theta` | (1.0, 1.0, 1.0, 0.80) | learning elasticity to Q | DECLARED |
| `class_target` | (40, 42, 42, 30) | class size at q ≤ 1 | DECLARED |

**Structural constants vs anchor arrays.** `cover_lo/hi`, `seat_t50`, `seat_width`, `seat_lag`, `seat_resp`,
`surv_max`, `surv_theta` are **level-specific constants of one rule**, the same for all 30 countries. They
encode a declared *expansion sequencing* (primary capacity first, lower secondary later, upper secondary
later still, tertiary earlier than upper in this parameterisation). They are **not** interpolated through
observed PHL completion years and are **not** country-specific. Country heterogeneity enters the supply
rule only through two declared traits that exist for every country: `cap0_c` (state-capacity scalar) and
`dshift_c` (delivery-timing shift).

**Code-inspection statement (check a).** The supply rule is implemented in three functions —
`coverage_target`, `desired_capacity`, `update_seats`. None of them receives or references a country name;
none contains a year-indexed array or an anchor interpolation; there is no `if country == "SYN00"` or any
PHL-only supply variable anywhere. The audit is executed at run time (`supply_code_audit`), written to
`results/reproduction_checks_detail_v1_2.csv` and recorded in the manifest. The only PHL-specific objects
in the whole code are (i) the declared **demographic path** in §2 and (ii) the declared country traits in
§9, which pass through the same functions as every other country.

### 4.2 Teachers and PTR

```
teachers_L(t) = max(1, teachers_L(t-1) + teach_resp_L · (teach_delivery_base + teach_delivery_gain·B_L(t))
                    · (enrol_L(t - teach_lag_L)/ptr_target_L - teachers_L(t-1)))
PTR_L(t)      = enrol_L(t) / teachers_L(t)
```

| parameter | value | unit | source |
|---|---|---|---|
| `ptr0` | (24, 26, 26, 18) | 1970 pupils per teacher | DECLARED |
| `ptr_target` | (33, 35, 34, 24) | planning norm | DECLARED |
| `teach_resp` | (0.35, 0.30, 0.25, 0.20) | annual convergence | DECLARED |
| `teach_lag` | (4, 5, 5, 6) | years | DECLARED |
| `teach_delivery_base`, `teach_delivery_gain` | 0.35, 0.65 | hiring effort | DECLARED |

PTR is a genuine stock ratio, not a direct function of `q`. The observed PHL primary PTR series is read
only as the declared benchmark in check (c) and is never encoded.

---

## 5. Layer 2b — borrowed four-state household block (structure only)

### 5.1 Borrow ledger

| element | source (read-only) | sha256 | status |
|---|---|---|---|
| four states `school` / `both` / `work` / `neither`; household utility comparison; parameter **names** `y_med`, `w_child`, `farm`, `compat`, `v0`, `decay`, `cost`, `neither`, `girl_care`, `haz` | `engine/childworld.py` at parent-repo HEAD (`git -C /Users/treymenefee/massification_live show HEAD:engine/childworld.py`) | `ae73adb2a6d9c75d59966390e4304437479ff310a8724093e9108e9d26a23cab` (**verified at retrieval**) | **BORROWED-FROM-ATLAS-STRUCTURAL** |

**What is not taken:** no childworld prior, posterior, calibrated value, country target or output number
enters as a parameter. Its observation equation is **not** the ILO child-labour definition; its values are
stylised; `childworld_mc` v1 failed the India composition test; its baseline "neither" share (0.421) was
flagged for validation. Those caveats travel with the code.

### 5.2 Declared utility form (childworld structure, our values)

```
util(c) = log(c - 0.6·need)                      if c - 0.6·need > 0.05
        = log(0.05) + (c - 0.6·need - 0.05)/0.05 otherwise        need = 0.85
earn_L  = 0.32 · ageW_L · max(w_child/0.32, 0.55·farm)
cost_L  = cost · cost_base_L
v_L     = v0 · decay^L + 0.25·ability − 1.3·min(out_years,3)/3
U_school  = util(y − cost_L) + v_L
U_both    = util(y − cost_L + 0.5·(1+compat)·earn_L) + v_L·(0.72+0.2·compat) + 0.4·compat − 0.25
U_work    = util(y + earn_L) − 0.2·taste
U_neither = util(y) + neither + girl_care·girl
P(state) ∝ exp(U_state / 0.3)
```

Aggregation is a **declared representative household**: `ability = 0`, `taste = 0`, half girls
(`GIRL_SHARE = 0.5`), no out-of-school years at the decision point. `y = y_med · exp(shock)`, with a
declared country-year shock sd of 1.5 %.

### 5.3 Declared parameter ranges (drawn per country, uniform unless stated)

| name | declared range | unit / meaning | source |
|---|---|---|---|
| `y_med` | U(0.90, 1.80) | household income, adult informal-wage units | BORROWED-FROM-ATLAS-STRUCTURAL (name) + DECLARED (range) |
| `w_child` | U(0.10, 0.35) | child market wage, relative | same |
| `farm` | U(0.10, 0.60) | share with farm/family business | same |
| `compat` | U(0.25, 0.75) | work–school compatibility | same |
| `v0` | U(1.20, 2.20) | value of schooling at primary | same |
| `decay` | U(0.62, 0.80) | decline of schooling value by level | same |
| `cost` | U(0.80, 1.80) | school cost multiplier | same |
| `neither` | U(−1.20, −0.60) | baseline value of not in school/market work | same |
| `girl_care` | U(0.05, 0.35) | extra "neither" value for girls | same |
| `haz` | U(0.10, 0.40) | hazardous share of 15–17 work | same |
| `cost_base` | (0.05, 0.14, 0.22) | level cost weights | DECLARED |
| `ration_work_share` | 0.90 | share of **rationed** children defaulting to work | DECLARED |
| `hh_noise_sd` | 0.015 | log household-income shock | DECLARED |

### 5.4 Rationing (declared)

For each level-year, the capacity is `min(phys_cap·seats, overage_cap·C)`. **Official-age applicants are
admitted first, then over-age applicants, until capacity fills.** The remainder are out of school and
**default to work**: `ration_work_share = 0.90` of rationed children go to work and 0.10 to the bounded
"neither" category. The decision uses no RNG (there are no ties in a representative-household block); the
seeded stream is used only for country draws and the declared shocks. "Neither" is reported separately, is
bounded by the declared utility value and the 0.10 rationed share, and never absorbs a residual.

### 5.5 Declared deviations from childworld (frozen spec §2)

1. **No free "neither" sink** — out-of-school children default to work/child labour; "neither" is bounded
   and reported.
2. **Rationing is added** — childworld is demand-only; v1.2 has a supply cap per level and a declared
   admission order.
3. **Child-labour definition** — declared as "any market work under 15; work at 15–17 in a declared
   hazardous share; and school-plus-work under 12". This is the childworld/camchild definition, explicitly
   **not** claimed to be the ILO statistical definition. It is reported as a separate series from model
   "work".
4. **Time structure** — one-year cohort ageing; cohort inflow from the declared path, not a fertility
   model.

---

## 6. Layer 3 — growth/composition (v1, retained) and education → complexity (Amendment A1)

### 6.1 Education → X

```
xbase_t = x_income_coef·ln(Y_t/1000) + x_urban_coef·(U_t − 0.40) + xoff_c
X_t     = clip( xbase_t + x_edu_level·flow_{t−L} + x_edu_delta·(flow_{t−L} − flow_{t−L−1})
                + x_persist·(X_{t−1} − xbase_{t−1}), 0, 2.40 )
flow_t  = cohort-flow primary completion rate (the FLOW object; not the literacy stock)
```

| parameter | value | unit | source |
|---|---|---|---|
| `x_income_coef` | 0.55 | X per ln(GDPpc/1000) | DECLARED |
| `x_urban_coef` | 0.55 | X per urban share | DECLARED |
| `x_urban_ref` | 0.40 | urban reference | DECLARED |
| `x_edu_level` | 0.40 | X per unit lagged completion (level term) | DECLARED (order of magnitude of the observed E5 association 0.593, **not** that estimate and not causal) |
| `x_edu_delta` | 0.15 | X per unit change in completion (flow term) | DECLARED |
| `x_persist` | 0.50 | persistence of X around the income/urban base | DECLARED |
| `edu_lag` L | 10 | years | DECLARED (within the frozen 5–10) |
| `x_min`, `x_max` | 0.0, 2.40 | index bounds | DECLARED |

`X` continues to open rungs and raise rung demand (v1 block), so the loop is two-way, as Amendment A1
requires.

### 6.2 v1 economy block (retained)

| parameter | value | unit | source |
|---|---|---|---|
| `lf_share_of_pop` | 0.52 | labour force / population | DECLARED |
| `sec_ag_base`, `sec_ag_x` | 0.500, −0.450 | ag share at X=0.6 and slope | DECLARED |
| `sec_inf_base`, `sec_inf_x` | 0.240, −0.080 | informal share | DECLARED |
| `sec_man_base`, `sec_man_x` | 0.130, 0.090 | industry share | DECLARED |
| `sec_floors` | (0.02, 0.05, 0.03, 0.05) | minimum shares; services is the water-filled residual | CONVENTION |
| `rung_a` / `rung_b` | (0.90, 0.40, −0.30, −1.30) / (−0.65, 0.20, 1.00, 2.20) | rung utility intercept/slope | DECLARED |
| `x_open` | (0.00, 0.08, 0.26, 0.48) | X threshold for each rung | DECLARED |
| `office_u_coef` / `mfg_u_coef` | (0, 0.35, 0, −0.20) / (0, −0.10, 0.30, 0.10) | sector bias on rung utility | DECLARED |
| `phi_formal` | 0.82 | formal share of industry+services | DECLARED |
| `sep` | (0.10, 0.07, 0.05, 0.04) | separation rate | DECLARED |
| `seek` | (0.15, 0.35, 0.60, 0.80) | share of graduates seeking a rung | DECLARED |
| `queue_retain`, `queue_max_lf`, `rank_gain` | 0.50, 0.20, 0.20 | queue/rank parameters | DECLARED |
| `rung_mult` | (2.20, 3.20, 4.60, 6.40) | rung wage ladder × GDPpc/1000 | DECLARED |
| `cred_prem` | 0.10 | credential premium per level | DECLARED |
| `psi_pre/ind/div` | 0.02 / 0.22 / 0.12 | informal wage literacy slope by regime | DECLARED |
| `gp` | (0.012, 0.008, 0.030, 0.022) | sector productivity growth | DECLARED |
| `accel_ind` / `accel_div` | (1,1,1.6,1.3) / (1,1,1.3,1.5) | sector growth multipliers | DECLARED |
| `comp_step` | (0.10, 0.18, 0.32, 0.50) | growth step per Δ(employment/LF) by rung | DECLARED |
| `lit_ag_growth` | 0.010 | literacy × ag/informal productivity, post-takeoff only | DECLARED |
| `g_floor`, `g_cap`, `g_noise_sd` | 0.0, 0.090, 0.006 | growth clip and noise | DECLARED |

Takeoff: `pre→industrializing` iff literacy ≥ 0.60 and GDPpc ≥ 1500; `industrializing→diversified` iff
X ≥ 0.95 and GDPpc ≥ 6000. Literacy is a lagged (12-year) function of primary completion, as in v1.

### 6.3 Pipeline and tertiary demand

| parameter | value | unit | source |
|---|---|---|---|
| `pool_retain` | 0.50 | annual carry-over of the completed/over-age pool | DECLARED |
| `init_pipe` | (0.95, 0.75, 0.50, 0.15) | 1970 eligible pool / cohort | DECLARED |
| `init_comp` | (0.55, 0.35, 0.15, 0.05) | burn-in completion | DECLARED |
| `t3_a`, `t3_b`, `t3_c` | −2.02, 0.45, 0.60 | tertiary participation logit on income and X | DECLARED |
| `ter_pool_retain` | 0.35 | tertiary eligible-pool memory | DECLARED |

Levels 0–2 use the four-state block; tertiary is an **adult** decision (no child states, no child labour)
driven by the declared participation logit applied to the eligible pool. The panel's `demand_share` column
is the four-state demand share for levels 0–2 and the participation rate for tertiary.

---

## 7. Measurement convention (check d)

| parameter | value | unit | source |
|---|---|---|---|
| `meas_completion_factor` m | **1.10** | single constant, all levels and countries | CONVENTION / measurement choice |

The model reports a **cohort-flow completion** (identity-bound, used for check d) and a **UIS-convention
completion** = m × cohort-flow (both written to the panel). m is a single declared constant; there is no
per-level or per-country factor. The observed PHL 2024 ratios (primary ≈ 1.05, lower ≈ 1.05, upper ≈ 1.14)
are the declared rationale; they are **not** used to set m numerically beyond the single declared 1.10.

**Scoring choice, declared before the run.** Check (a) is scored on the **UIS-convention** series, because
the frozen on-disk targets are UIS completion rates; the cohort-flow crossing dates are reported alongside
in the check note and detail file. Check (d) is scored on the **cohort-flow** series. Both series are in
the panel. This is the disclosed measurement issue; it is not a rescue factor tuned per level.

---

## 8. Frozen scoring rules (checks a–e)

The exact thresholds are in `v1_2/PRE_DECLARATIONS.md` §5. The implementation:

| check | pass rule |
|---|---|
| **a** | UIS completion: primary first ≥90 in **2014–2020**; lower first ≥90 in **2021–2027** with 2023 < 90; upper never ≥90 for years ≤2024 and 2024 ∈ **[73.0, 77.0]**; tertiary GER 2025 ∈ **[48.1, 54.1]**; **and** the run-time code audit finds no country branch, no per-level anchor array, no override token. |
| **b** | PHL primary OOS 2005–2015 mean ∈ **[5 %, 20 %]**; work share of OOS ≥ **0.50** in every country-year (levels 0–2); boom mean OOS − max(flat, decline) ≥ **2 pp** over 1990–2015 (primary+lower-secondary, cohort-weighted). |
| **c** | PHL primary PTR peak year ∈ **[1990, 2010]**, peak ≥ **1.10 ×** 2024, and 2024 < peak. |
| **d** | cohort-flow completion ≤ GER × (1 + 1e−9) in every country-year-level; m single and declared. |
| **e** | two-way FE (country + year) coefficient of lagged primary completion flow on X **> 0** with **p < 0.05** at lag 10; same sign in the 5-year-block FE spec. |

A FAIL is reported, not rescued. No parameter is changed after the freeze to flip a check.

---

## 9. Declared country parameterisation

| | `SYN00_PHL_LIKE` | `SYN01_TWIN_MFG` / `SYN02_TWIN_OFFICE` | `SYN10_BOOM` / `SYN11_FLAT` / `SYN12_DECLINE` | `SYN03…SYN29` |
|---|---|---|---|---|
| y0 (1970 GDPpc) | 2000 | 2600 | 2200 | LN(ln 2500, 0.80) |
| pop0 / npop | observed path / 0.0173 | 20e6 / 0.014 | 20e6 / 0.014 | LN(ln 18e6, 0.70) / N(0.016, 0.005) |
| cohort path | **observed PHL path** (1995–2024) + declared extrapolation | one common path (S0 18e6; g 1.8/1.4/0.9 %) | **differ only here**: boom = PHL shape × S0 20e6; flat = S0; decline = −0.9 %/yr | 3-phase growth |
| urban 1970 / growth | 0.33 / 0.0045 | 0.42 / 0.004 | 0.35 / 0.004 | U(0.12, 0.78) / U(0.001, 0.007) |
| literacy 1970 | 0.83 | 0.72 | 0.70 | 0.10 + 0.60·ln(y0/1000)/1.6 + N(0, 0.08) |
| sector offsets ag/inf/man | −0.03 / +0.08 / −0.03 | 0 / −0.03 / **+0.07** vs 0 / +0.02 / **−0.06** | 0 / 0 / 0 | N(0, 0.06/0.05/0.04) |
| office / mfg bias | **−1.20** / −0.80 | **−0.30 / +0.80** vs **+0.80 / −0.30** | 0 / 0 | N(0, 0.55) |
| `cap0` / `dshift` | 1.00 / 0 | 1.00 / 0 | 1.00 / 0 | N(1, 0.08) clip [0.80,1.20] / N(0, 6) |
| household block | (y_med 1.30, w_child 0.28, farm 0.25, compat 0.50, v0 1.70, decay 0.68, cost 1.00, neither −0.90, girl_care 0.20, haz 0.25) | common draw (1.35, 0.28, 0.30, 0.50, 1.70, 0.68, 1.00, −0.90, 0.20, 0.25) | same common draw | declared ranges in §5.3 |

**The twins** share cohort, income, urban, literacy, household block and **shock realisations**; they differ
**only** in sector offsets and office/mfg rung loadings. **The three cohort variants** share everything
except the declared cohort path (and their shock realisations). These are controlled comparisons, not
cross-country evidence.

---

## 10. What v1.2 does **not** contain

- No estimate, fit, calibration run or likelihood. No observed PHL completion/GER/OOS value is encoded.
- No per-level anchor interpolation, no PHL-specific supply branch, no per-country supply override.
- No causal claim, no direction-of-causation claim, no policy claim, no forecast.
- No fertility model, no NER object, no enforcement series, no regional layer.
- No childworld value, prior or posterior; only structure and parameter names are borrowed.
- No claim that the synthetic `SYN00_PHL_LIKE` is the Philippines or any real country.

---

## 11. Freeze declaration

This parameter block was frozen **before the scored run** on 2026-11-20 (Asia/Shanghai). Its sha256, the
code sha256, the predeclaration sha256 and the input-data sha256 values are recorded in
`RUN_MANIFEST.json`. The design-phase changes that led to these values are disclosed in
[`TUNE_LOG.md`](TUNE_LOG.md); the scored run is the one whose artifacts are in `results/`.
