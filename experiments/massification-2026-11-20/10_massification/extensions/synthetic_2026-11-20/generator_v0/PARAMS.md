# PARAMS — SYNTHETIC education-system generator, v0

> **SYNTHETIC. This file documents a seeded computer model. Everything it produces is
> generated data from declared equations. It is not calibrated evidence about the world,
> not a forecast, and not a fit to any observed country series. No observed data file is
> read at runtime.** The only observed numbers that enter are the declared targets in §3.
> Label carried in every output: `SYNTHETIC`.

**Run identity**

| item | value |
|---|---|
| generator | `code/sim.py` |
| seed | `20261120` (PCG64, fixed draw order) |
| panel | 32 countries × 55 years (1970–2024) × 4 levels = **7,040 rows** |
| levels | `primary`, `lower_secondary`, `upper_secondary`, `tertiary` |
| special country | `PHL_like` (index 0), declared pattern-matched, **not fitted to observed PHL** |
| runtime | ≈0.2 s (well under the 60 s limit) |
| outputs | `results/synthetic_panel.csv`, `results/reproduction_checks.csv`, `results/calibration_log.csv`, `results/capacity_counterfactual.csv`, `results/run_summary.json` |

---

## 1. Declared equations (verbatim)

Let `t = year − 1970`, `x = log(GDPpc/1000)`, and `L ∈ {primary, lower_secondary, upper_secondary, tertiary}`.

**1. Cohorts / demography.**
```
N_{c,t}      = N0_c · exp(n_c · t)
f_{c,t}      = max(1.3, f0_c − fdec_c · t)                      # fertility proxy
share014_c,t = clip(0.13 + 0.062·(f_{c,t} − 1.3), 0.12, 0.48)
C_{c,t}      = N_{c,t} · share014_c,t                            # 0–14 base cohort
cohort_{L,c,t} = C_{c,t} · ω_L                                   # official-age population
ω = (6/15, 3/15, 3/15, 5/15)
```

**2. Demand ceiling.**
```
d_{L,c,t} = logistic( a_L + b_L·x_{c,t} + g_L·urban_{c,t} + h_L·services_{c,t} + e_{L,c} )
a_L       = logit(C_MEAN_L) − b_L·X_REF − g_L·URBAN_REF − h_L·SERVICES_REF
e_{L,c}  ~ Normal(0, σ_L)                                        # country fixed effect
```
The intercept is written through `C_MEAN_L`, the ceiling at the declared reference point
(GDPpc 3,000; urban 0.50; services 0.42; e=0). This keeps the central ceiling fixed when `b_L`
changes, so the income-scaling calibration does not drift into saturation. `X_REF = log(3.0)`.

**3. Supply / capacity gate.**
```
spend_{c,t} = clip(sp0_c + spg_c·t, 1, 9)
K_{c,t}     = clip(K0_c + 0.30·(log y_{c,t} − log y_{c,0}) + 0.05·(spend_{c,t} − spend_{c,0}), 0.05, 1)
gate_{c,t}  = K_{c,t}^0.75
```

**4. State push.**
```
law_{L,c,t}  = 1[ year ≥ law_year_{L,c} ]                        # 0/1 declared event
push_{L,c,t} = δ_L · law_{L,c,t} · gate_{c,t}
eff_{L,c,t}  = min(1.04, d_{L,c,t}·gate_{c,t} + push_{L,c,t})     # effective ceiling
```

**5. Flow / stock identity (the old-model fix).**
```
p_{L,c,1970} = eff_{L,c,1970}
p_{L,c,t}    = clip( p_{L,c,t−1} + r_L·(eff_{L,c,t} − p_{L,c,t−1}), 0, 1.04 )
E_{L,c,t}    = cohort_{L,c,t} · p_{L,c,t}
GER_{L,c,t}  = 100 · E_{L,c,t} / cohort_{L,c,t} = 100·p_{L,c,t}    ∈ [0,104]
comp_{L,c,t} = 100 · p_{L,c,t} · s_L
```
`ω_L` is applied **once**, to define the official-age denominator. There is no second
cycle-length factor anywhere: enrolment is `cohort × p`, and completion is `s_L × p`. Cross-level
transition is embedded in `p_L` (participation among the official-age population), **not**
multiplied again by the previous level's completion — that is the double-counting failure this
identity is designed to avoid.

**6. PHL-like country.** Uses the same structural parameters (`b_L, g_L, h_L, κ, r_L, s_L, δ_L`);
only country-specific draws are overridden and four fixed effects are solved to the declared
milestone pattern (§5.2–5.3).

---

## 2. Parameter table

Every row states value, source, and whether it is an assumption. "Declared" = chosen by design,
not estimated from data. "Target" = encoded from the brief / cited scaling table. "Derived" =
solved deterministically by the declared calibration.

### 2.1 Structural parameters

| symbol | value | source | assumption? | note |
|---|---|---|---|---|
| `SEED` | 20261120 | declared | — | PCG64; fixed draw order |
| `N_COUNTRIES` | 32 | declared | — | 31 generic + 1 `PHL_like` |
| years | 1970–2024 (55) | declared | — | synthetic window |
| `C_MEAN` | (0.92, 0.72, 0.50, 0.32) | declared design anchor | **yes** | demand ceiling at reference point |
| `B_PRIM` | 0.05 | declared (saturated primary) | **yes** | primary income slope not calibrated |
| `B_SEC` | **1.055144** | derived by bisection to target +0.29 | **target-driven** | common lower+upper slope |
| `B_TER` | **1.108998** | derived by bisection to target +0.78 | **target-driven** | tertiary slope |
| `G` | (0.30, 0.55, 0.75, 0.60) | declared | **yes** | urban-share loadings |
| `H` | (0.20, 0.35, 0.45, 0.40) | declared | **yes** | services-share loadings |
| `SIGMA_E` | (0.30, 0.50, 0.60, 0.70) | declared | **yes** | SD of country fixed effects |
| `SURVIVAL` | (0.95, 0.95, 0.92, 0.88) | declared | **yes** | within-level survival to completion |
| `ADJUST` | (0.20, 0.18, 0.15, 0.12) | declared | **yes** | annual adjustment speed `r_L` |
| `PUSH` | (0.06, 0.05, 0.06, 0.08) | declared | **yes** | `δ_L` push size (pp/100) |
| `KAPPA` | 0.75 | declared (brief) | **yes** | gate exponent |
| `K_Y`, `K_S` | 0.30, 0.05 | declared | **yes** | capacity loadings on income growth / spending |
| `K_MIN`, `K_MAX` | 0.05, 1.0 | declared | **yes** | capacity normalisation |
| `EFF_CAP` | 1.04 | declared | **yes** | numerical cap ⇒ GER ≤104 |
| `OMEGA` | (0.40, 0.20, 0.20, 0.3333) | declared | **yes** | age-band weights (6/15, 3/15, 3/15, 5/15) |
| `X_REF` | log(3.0) | declared reference | **yes** | GDPpc $3,000 anchor |
| `URBAN_REF` | 0.50 | declared reference | **yes** | urban anchor |
| `SERVICES_REF` | 0.42 | declared reference | **yes** | services anchor |
| `F_MIN` | 1.3 | declared | **yes** | fertility floor |
| `SHARE_INTERCEPT/SLOPE` | 0.13 / 0.062 | declared | **yes** | 0–14 share mapping |
| `SHARE_MIN/MAX` | 0.12 / 0.48 | declared | **yes** | share bounds |
| `LAW_NEVER_PROB` | 0.15 | declared | **yes** | probability a level never gets a law |
| `LAW_RANGES` | (1972–98, 1975–2005, 1980–2015, 1985–2020) | declared | **yes** | synthetic law dates |

**Timing / start dates.** The panel is balanced (every country is observed 1970–2024). The brief's
"varying start dates" is operationalised as country-and-level-specific `law_year` draws
(1972–2020, 15% never) plus the PHL-like synthetic law years — i.e. policy timing, not an
unbalanced entry panel. This is declared, not an oversight.

### 2.2 Country draw distributions (independent; fixed order)

| variable | distribution | clip | source | assumption? |
|---|---|---|---|---|
| `gdp0` | lognormal(median 2,500; σ_log 0.9) | [400, 20,000] | declared | **yes** |
| `growth` | Normal(0.018, 0.008) | [0, 0.045] | declared | **yes** |
| `N0` | lognormal(median 12e6; σ_log 1.0) | [3e5, 3e8] | declared | **yes** |
| `npop` | Normal(0.014, 0.006) | [0, 0.035] | declared | **yes** |
| `f0` | Uniform(1.8, 6.0) | — | declared | **yes** |
| `fdec` | Uniform(0.005, 0.045) | — | declared | **yes** |
| `u0` | Uniform(0.15, 0.75) | — | declared | **yes** |
| `ug` | Uniform(0.001, 0.008) | clip [0.05,0.95] | declared | **yes** |
| `sv0` | Uniform(0.25, 0.55) | — | declared | **yes** |
| `svg` | Uniform(0.001, 0.006) | clip [0.15,0.85] | declared | **yes** |
| `sp0` | Uniform(2, 6) | — | declared | **yes** |
| `spg` | Uniform(0, 0.03) | — | declared | **yes** |
| `K0` | Uniform(0.30, 0.65) | — | declared | **yes** |
| `e_{L,c}` | Normal(0, σ_L), independent across levels | — | declared | **yes** |
| `law_year` | Uniform(range_L), 15% never | — | declared | **yes** |

### 2.3 PHL-like overrides (index 0)

| parameter | value | source | assumption? |
|---|---|---|---|
| `gdp0` | 2,200 | declared synthetic | **yes** |
| `growth` | 0.020 | declared design (tuned to 15→50 grid, §5.3) | **yes** |
| `N0` | 50e6 | declared synthetic | **yes** |
| `npop` | 0.019 | declared synthetic | **yes** |
| `f0`, `fdec` | 5.5, 0.05 | declared synthetic | **yes** |
| `u0`, `ug` | 0.33, 0.006 | declared synthetic | **yes** |
| `sv0`, `svg` | 0.42, 0.004 | declared synthetic | **yes** |
| `sp0`, `spg` | 3.0, 0.02 | declared synthetic | **yes** |
| `K0` | 0.75 | declared design (tuned to 15→50 grid) | **yes** |
| law years | 1990, 1995, 2005, 2015 | **synthetic**, not the observed PHL statutory dates | **yes** |
| `p0_ter` | 0.15 | declared target (tertiary 1970 GER ≈15) | target |

### 2.4 Solved PHL fixed effects (declared calibration, not fitted to observed PHL)

| level | `e_{L,PHL}` | z = e/σ | realized 2024 target | target source |
|---|---|---|---|---|
| primary | **0.028647** | 0.10 | completion 94.00 | brief pattern (cross 90) |
| lower_secondary | **0.638445** | 1.28 | completion 92.00 | brief pattern (cross 90 later) |
| upper_secondary | **0.470322** | 0.78 | completion 78.00 | brief pattern (stall <90) |
| tertiary | **−0.275682** | −0.39 | GER 15.00 in 1970 → 50.83 in 2024 | brief pattern (~15→~50) |

The four fixed effects are **mild** (all |z| ≤ 1.3). The PHL-like pattern is therefore produced
mainly by the declared structural parameters, the synthetic growth path, the capacity path and
the synthetic law dates — not by extreme country effects.

---

## 3. Observed numbers encoded as targets (complete list)

The hard rule is that no observed series is read; only declared target numbers are transcribed.
**These are the only observed numbers in the generator:**

| # | number | meaning | source | how used |
|---|---|---|---|---|
| 1 | **+0.29** | secondary GER–income exponent | **brief** (which cites `10_massification/relations/data/scaling_laws.csv`) | `b_sec` bisection target |
| 2 | **+0.78** | tertiary GER–income exponent | **brief** (same citation) | `b_ter` bisection target |
| 3 | **90** | primary completion crossing | brief C3 | PHL-like primary solve |
| 4 | **90** | lower-secondary completion crossing, later | brief C3 | PHL-like lower solve |
| 5 | **<90** | upper-secondary must stay below | brief C3 | PHL-like upper solve (78) |
| 6 | **~15** | tertiary GER at start | brief C3 | `p0_ter = 0.15` |
| 7 | **~50** | tertiary GER at end | brief C3 | PHL-like growth/K0 design |
| 8 | +0.2154 | on-disk between-country secondary exponent | `scaling_laws.csv` S1-between | **note only** (mismatch check) |
| 9 | +0.5666 | on-disk between-country tertiary exponent | `scaling_laws.csv` S2-between | **note only** (mismatch check) |
| 10 | +0.0904 | on-disk within-country secondary exponent | `scaling_laws.csv` S1-within | **C2b diagnostic target only** |
| 11 | +0.8482 | on-disk within-country tertiary exponent | `scaling_laws.csv` S2-within | **C2b diagnostic target only** |

No raw PHL panel, no WDI series, no `UNIVERSALIZATION_SERIES.csv`, and no observed capacity
series are read or used. `data_files_read = []` in `RUN_MANIFEST.json`.

---

## 4. The target mismatch (load-bearing; read this before quoting C2)

The brief says the targets are secondary ≈ **+0.29** and tertiary ≈ **+0.78**, and says to cite
`scaling_laws.csv`. The on-disk file does **not** contain those numbers:

| object | secondary | tertiary |
|---|---|---|
| brief target (encoded) | **+0.29** | **+0.78** |
| `scaling_laws.csv` **between** (year FE only) | +0.2154 | +0.5666 |
| `scaling_laws.csv` **within** (country+year FE) | +0.0904 (ns) | +0.8482 |

The brief's tertiary target is **+0.213** above the on-disk between estimate. The generator encodes
the brief's numbers, as instructed. Consequences:

- **C2 vs the brief**: pass (synthetic +0.2819 / +0.7757, both within ±0.15).
- **C2 vs the on-disk between estimate**: tertiary is off by **+0.209**, outside ±0.15 → would be
  "off"; secondary is within tolerance (+0.067).
- **C2b vs the on-disk within estimate**: secondary fails badly (+0.4607 vs +0.0904, diff +0.370);
  tertiary passes (+0.7489 vs +0.8482, diff −0.099).

This is a provenance finding, not a modelling error. It is reported in `reproduction_checks.csv`
(C2 note, C2b) and in `FINDINGS.md` §4. The generator does not silently reconcile the brief with
the file.

---

## 5. Calibration and tune log

### 5.1 Income-scaling slopes `b_sec`, `b_ter`

Both are solved by **deterministic bisection** on the 31 generic countries only (`PHL_like`
excluded), so the special country cannot drive the scaling target. The bisection count is fixed
at 50; the full per-iteration trace is in `results/calibration_log.csv` (281 rows, label
`SYNTHETIC`).

| parameter | bounds | iterations | converged value | realized non-PHL slope | target |
|---|---|---|---|---|---|
| `b_sec` | [0.05, 3.0] | 50 | **1.0551444716918654** | 0.2900000000 | 0.29 |
| `b_ter` | [0.05, 4.0] | 50 | **1.1089977188459499** | 0.7800000000 | 0.78 |

Selected trace (first three iterations, showing the search bracketed the target):

| stage | it | candidate | realized | target |
|---|---|---|---|---|
| b_sec | 1 | 1.525000 | 0.392671 | 0.29 |
| b_sec | 2 | 0.787500 | 0.226660 | 0.29 |
| b_sec | 3 | 1.156250 | 0.312889 | 0.29 |
| b_ter | 1 | 2.025000 | 1.118903 | 0.78 |
| b_ter | 2 | 1.037500 | 0.748202 | 0.78 |
| b_ter | 3 | 1.531250 | 0.950092 | 0.78 |

The final all-country slopes are slightly lower (secondary +0.2819, tertiary +0.7757) because the
calibrated `PHL_like` point is included. Both remain inside ±0.15 of the brief targets. This is
**target encoding**, not independent validation: the generator is designed to embody the assumed
relations, which is the point of the exercise.

### 5.2 PHL-like growth / capacity grid (the 15→50 tune log)

The tertiary 15→50 path needs a growth/capacity combination that does not overshoot. I explored
the declared grid below (each cell: `e_ter` re-solved so the 1970 capacity-gated ceiling is exactly
0.15; reported number is 2024 tertiary GER). The chosen cell is **K0 = 0.75, growth = 0.020**
(interpolating between the 0.019 and 0.022 grid rows), giving **15.00 → 50.83**.

| K0 \ growth | 0.010 | 0.013 | 0.016 | 0.019 | 0.022 |
|---|---|---|---|---|---|
| 0.55 | 36.5 | 41.2 | 46.2 | 51.5 | 57.0 |
| 0.65 | 36.8 | 41.6 | 46.6 | 51.9 | 56.4 |
| **0.75** | 37.2 | 41.8 | 45.9 | **49.8** | 53.7 |

This is a **declared design search**, not a fit to observed PHL data. The brief's own target
(~50) is the only thing being matched. The grid is the full tune log for this choice; no other
PHL parameters were tuned to rescue a check.

### 5.3 PHL-like fixed-effect solve

| level | method | target | iterations | converged `e` | realized |
|---|---|---|---|---|---|
| tertiary | analytic (set 1970 gated ceiling = 0.15) | start 15.0 | 1 | −0.275682 | 15.00 |
| primary | bisection on 2024 completion | 94.0 | 60 | 0.028647 | 94.00 |
| lower_secondary | bisection on 2024 completion | 92.0 | 60 | 0.638445 | 92.00 |
| upper_secondary | bisection on 2024 completion | 78.0 | 60 | 0.470322 | 78.00 |

Full trace: `results/calibration_log.csv`, stages `phl_e_*`.

---

## 6. Declared assumptions (load-bearing)

| id | assumption | why it matters |
|---|---|---|
| **A1** | One logistic demand ceiling per level; one common `b_L` across countries. | Forces the between and within income margins to share a slope; this is why C2b fails. |
| **A2** | Country fixed effects are independent across levels. | Produces the C5b ladder violations (tertiary can exceed upper-secondary). |
| **A3** | Official-age population = base 0–14 cohort × fixed `ω_L`; applied once. | The anti-double-count identity. If applied twice, GER would be badly wrong. |
| **A4** | Completion = survival × participation; cross-level transition embedded in `p`. | Avoids a second cycle-length/transition multiplication. |
| **A5** | Capacity gate multiplies the demand ceiling; `κ=0.75`; `K ∈ [0,1]`. | The gate is the supply mechanism; C4's floor>ceiling follows from it + ceiling ordering. |
| **A6** | Push is additive, proportional to gate; `δ_L` declared. | The law event is a level shift, not a trend break with enforcement. |
| **A7** | Country draws are independent; no diffusion/spillovers. | No cross-country convergence or neighbourhood effects. |
| **A8** | Adjustment speed `r_L` is constant; over 55 years the system is near equilibrium. | The panel is mostly a ceiling panel; initial conditions wash out (except PHL tertiary). |
| **A9** | All drivers are monotone non-decreasing; no crises/reversals. | Every synthetic GER/completion series is monotone non-decreasing; stagnation/collapse cannot be reproduced. |
| **A10** | `PHL_like` parameters are design choices matched to the declared pattern, not observed PHL. | The "PHL-like" label is a pattern target, not a calibration to the Philippines. |
| **A11** | The reference point (GDPpc 3,000; urban .50; services .42) is a declared anchor, not an observed mean. | `C_MEAN` is interpretable but not estimated. |
| **A12** | Education spending is a synthetic series; `K_Y`, `K_S` are arbitrary declared loadings. | Capacity is not measured, only generated. |

---

## 7. What is deliberately not in the model

No teacher/classroom production function; no labour-market returns; no migration or foreign
students; no repetition/over-age mechanism beyond the 1.04 cap (so GER barely exceeds 100); no
cross-level transition coupling (the ladder); no conflict, crisis, or reversal; no observed
calibration of any kind. These omissions are limitations, not hidden assumptions.

---

## 8. Reproducibility

- PCG64 seed `20261120`; draws in a fixed order; bisection counts fixed at 50 (b) and 60 (PHL e);
  float output formatted with `%.6f`.
- `results/reproduction_checks.csv` uses the column name **`verdict`** for the
  pass/fail/inconclusive field; values are exactly `pass` or `fail` (no `inconclusive` arose).
- `code/verify_and_manifest.py` runs `sim.py` twice and compares every `results/*.csv` byte for
  byte. `RUN_MANIFEST.json` records both hash sets, `byte_identical: true`, code SHA-256, Python
  and NumPy versions, parameters, and `data_files_read: []`.
- Re-running twice on this machine produced byte-identical CSVs; the manifest records the exact
  SHA-256 pairs.
