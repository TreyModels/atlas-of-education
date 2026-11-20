# PARAMS — EXP-18 **PART-REPAIR** (v1.7)

**`LABEL: DECLARED` for every behavioural parameter; `LABEL: DERIVED` only for the EXP-17
target (cited, not used); `LABEL: CONVENTION` for `m`; `LABEL: SUBSTITUTION` for the one change.
`FITTED`: none. No value is introduced by this cell.**

The repaired arm A17 is the **frozen v1.6 generator** (`code/frozen/sim_v1_6_repair.py`,
sha256 `9c0e7998…`, an unedited copy) with **one** module-level function lookup replaced: the
participation decision is taken from the **frozen v1.3 four-state block**
(`code/frozen/sim_v1_3.py`, sha256 `70ae8f0e…`, unedited), called unchanged. Nothing else is
touched: the tier menu, the tier capacity split, the admission ranking, the survival law, the
capacity build-out and the economy block are the frozen v1.6 ones.

## 1. The one change, and its parameter ledger

| object | before (v1.6 / A10) | after (v1.7 / A17) | status |
|---|---|---|---|
| participation mass | the tier block's own `max(U_work, U_neither)` refusal set over `S01` cell weights | `w_school[k] = w[k] · ds13`, `ds13 = Pr[school] + Pr[both]` from `sim_v1_3.state_shares(cp, L, y_shock)` | **SUBSTITUTION** — a frozen *function*, no number |
| out-of-school composition | tier block's `mW/mB/mN` | the same block's `(Pr[work], Pr[neither], 0)` | **REPORTING ONLY** (declared; no effect on demand, admission, capacity, verdict) |
| H/O split | tier block `U_H` vs `U_O` | **unchanged** (frozen `U_H`, `U_O`, frozen menu) | held |
| O-vs-outside refusal margin `acc` | `U_O > max(U_work, U_neither)` | **unchanged** | held |
| tier capacity | `K_H = h_share·seats`, `K_O = seats − K_H` | **unchanged** | held (the structural part; §4.1 of the predeclaration) |
| survival | `surv_max·Q^θ`, no tier multiplier | **unchanged** | held |

## 2. Parameter count — non-increasing by construction

| pool | count | source |
|---|---:|---|
| `P` declared parameters | 82 | `generator_v1_3/PARAMS.md` (inherited unchanged by v1.5/v1.6) |
| tier-block parameters (`TIER16`: T01–T14, S01–S08) | 21 | `generator_v1_5_bimodal/PARAMETERS.csv` |
| borrowed geometry constants (`NEED`, `UTIL_SCALE`, `GIRL_SHARE`, `TASTE`, `ABILITY`, `OUT_YEARS`, `AGE_W`) | 7 | frozen v1.3 code, identical values in v1.6 |
| **v1.6 total** | **110** | |
| **v1.7 total** | **110** | |
| **introduced by this cell** | **0** | |

The v1.3 four-state block's primitives are **the same declared values** already counted in the
110 (its `cost_base`, `P` and the seven geometry constants are v1.6's own); the substitution
adds no entry, retires none, and renames none. **Every value the repaired arm uses is cited by
name and file in §3–§5.** A number not already declared would be `FAIL-RE-FIT`.

## 3. Tier block (A5) — held exactly as built (not touched by this cell)

| id | parameter | value | status | provenance |
|---|---|---|---|---|
| T01 | `h_share` (Tier H share of adequate places) | (0.15, 0.28, 0.40, 0.50) | DECLARED | v1.5 `PARAMETERS.csv` T01 |
| T05 | `q_O` (Tier O quality multiplier, return/take-up margin) | **0.55** | DECLARED | v1.5 T05 — **not moved**; the menu route is CLOSED (D144(5)) |
| T06 | `cost_H_mult` | 1.60 | DECLARED | v1.5 T06 |
| T07 | `cost_O_mult` | 0.03 | DECLARED | v1.5 T07 |
| T10 | `v_tier_scale` | **retired** | RETIRED | v1.5 T10 (R4b) — not used |
| T12 | `a_gate` | 0.40 | DECLARED | v1.5 T12 |
| T13 | `risk_pen` | 0.20 | DECLARED | v1.5 T13 |
| T14 | `H_h` | 20.0 | DECLARED | v1.5 T14 |
| S01 | `cell_weight` (5×3) | see predecl §11 of the v1.6 file | DECLARED | v1.5 S01 |
| S02 | `z_q` | (−1.2816, −0.5244, 0, 0.5244, 1.2816) | DECLARED | v1.5 S02 |
| S03 | `sigma_tier` | 0.80 | DECLARED | v1.5 S03 |
| S04 | `ability_grid` | (0.25, 0.50, 0.75) | DECLARED | v1.5 S04 |
| S06 | `rank_w_income`, `rank_w_ability` | 0.30, 0.70 | DECLARED | v1.5 S06 |
| S08 | `padv_clip` | (0.01, 0.999) | DECLARED | v1.5 S08 |
| — | `q_H_mult`, `q_O_mult` (survival) | 1.00, 1.00 | DECLARED | v1.6 R4c (no tier survival penalty) |
| — | `surv_pen_H`, `surv_pen_O` | 1.000, 1.000 | DECLARED | v1.6 R4c |
| — | `cred_prem_H`, `cred_prem_O` | 0.18, 0.03 | DECLARED | v1.5 T08/T09 (reported wage objects) |

## 4. The substituted primitive — the frozen v1.3 four-state block (called, never re-implemented)

| object | value | status | file |
|---|---|---|---|
| `state_shares(cp, level, y_shock)` | multinomial logit over `{school, both, work, neither}` | DECLARED | `generator_v1_3/code/sim_v1_3.py` |
| `NEED` | 0.85 | DECLARED (geometry) | `sim_v1_3.py` |
| `UTIL_SCALE` | 0.30 | DECLARED (geometry) | `sim_v1_3.py` |
| `GIRL_SHARE` | 0.50 | DECLARED (geometry) | `sim_v1_3.py` |
| `TASTE`, `ABILITY`, `OUT_YEARS` | 0.0, 0.0, 0.0 | DECLARED (geometry) | `sim_v1_3.py` |
| `AGE_W` | (0.25, 0.70, 1.00) | DECLARED (geometry) | `sim_v1_3.py` |
| `cost_base` | (0.05, 0.14, 0.22) | DECLARED | `generator_v1_3/PARAMS.md` (`P`) |
| `y_med, w_child, farm, cost, v0, decay, compat, neither, girl_care` | drawn country traits | DECLARED | `sim_v1_3.py` (`draw_countries`) / `apply_declared` |

## 5. Measurement, capacity and scoring constants (unchanged)

| object | value | status | note |
|---|---|---|---|
| `m` = `meas_completion_factor` | **1.10** | CONVENTION | frozen; not a conversion |
| `phys_cap` | **1.15** | DECLARED | not re-chosen; **no grid is run** in this cell |
| `overage_cap` | 1.05 | DECLARED | GER hard cap |
| `seed` | 20261120 | DECLARED | one PCG64 stream, frozen draw order |
| observed bar | **≥ 17 / 33** within **±5.0 pp** inclusive | THRESHOLD | copied from EXP-7, unchanged |
| crossing tolerance | **±5 y**, thresholds 90/90/90 pp | THRESHOLD | D34/A6 |
| representation | unfilled ≥ 0.10 (≥15/30), queue ≥ 1.10 (≥15/30), coexistence ≥ 8/15 | THRESHOLD | Council block 024 §5.3, copied |
| A00 construction check | 9/33; medians −4.3008 / −29.4351 / −27.5857 pp | CHECK | EXP-7's V1 construction |
| EXP-17 λ\* | 1.11465019198434 | **REQUIRED-STATE (EXP-17) — NOT ADOPTED** | cited only; the DERIVED target 0.8076 is attached; no λ enters the model |

## 6. What is *not* a parameter here

The **upper structural part** (the tier menu's consequence at upper-secondary) is **declared and
reported as a sensitivity** (`results/upper_structural_sensitivity.csv`), never tuned: no menu
value is moved and no menu arm is run. The **capacity decomposition**
(`results/capacity_decomposition.csv`) is **report-only arithmetic on A17's own panel** — no
alternative arm, no alternative capacity value, no alternative count.
