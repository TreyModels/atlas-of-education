# PARAMS — V16-REPAIR (EXP-14)

**`LABEL: DECLARED` for every behavioural parameter; `LABEL: DERIVED` where a value is an observed median used as
an input; `LABEL: CONVENTION` for `m`. `FITTED`: none. Values are fixed before the run and hashed with the
predeclaration. The machine-readable copy is the `json` block in `PRE_DECLARATIONS.md` §5, which the code parses and
compares against its own constants (`verify_predecl()`); a mismatch refuses to run.**

Base instrument: `code/base_v1_3_sim.py`, a byte-for-byte copy of `generator_v1_3/code/sim_v1_3.py`
(sha256 `70ae8f0e…`). All v1.3 parameters are inherited unchanged from `generator_v1_3/PARAMS.md` — they are not
restated here except where V16 touches them.

## 1. V16 switches (one boolean read per insertion point)

| switch | values | default (scored arm) | identity when OFF? |
|---|---|---|---|
| `bimodal` | ON/OFF | **ON** in A10 | yes — the frozen single gate |
| `kappa_link` | ON/OFF | **OFF** (D138, Rule R6) | yes |
| `tier_surv` | ON/OFF | **OFF** (Rule R4c) | yes |
| `inject_upper` | vector/None | None | yes — only used by the guard arm A00CF |

## 2. Tier block (A5), carried from `generator_v1_5_bimodal/PARAMETERS.csv` T/S rows

| id | parameter | value | status | provenance (v1.5) | V16 change |
|---|---|---|---|---|---|
| T01 | `h_share` (Tier H share of adequate places, by level) | (0.15, 0.28, 0.40, 0.50) | DECLARED | v1.5 T01, declared before any v1.5 run | none |
| T05 | `q_O` Tier O quality multiplier | **0.55** | DECLARED | v1.5 T05 | **margin moved**: now multiplies `v_O` in `U_O` (return/take-up), not `Q_O` in survival (R4a) |
| T06 | `cost_H_mult` | 1.60 | DECLARED | v1.5 T06 | none |
| T07 | `cost_O_mult` | 0.03 | DECLARED | v1.5 T07 | none |
| T10 | `v_tier_scale` (`v_O = 0.45 v_H`) | **retired** | DECLARED, RETIRED | v1.5 T10 | retired for this cell: one discount, one place (R4b). Retained in reconstruction arm A11V15 and in `S_dual` |
| T11 | `w_work_free` | 0.0 | DECLARED | v1.5 T11 | none (audited: no free taste) |
| T12 | `a_gate` | 0.40 | DECLARED | v1.5 T12 | none |
| T13 | `risk_pen` | 0.20 | DECLARED | v1.5 T13 | none |
| T14 | `H_h` (gate-payoff scale, shadow_module B17) | 20.0 | DECLARED | v1.5 T14 | none |
| S01 | `cell_weight` (5×3 joint weights) | see predecl §5 | DECLARED | v1.5 S01 | none |
| S02 | `z_q` (quintile income points) | (−1.2816, −0.5244, 0, 0.5244, 1.2816) | DECLARED | v1.5 S02 (shadow_module B23) | none |
| S03 | `sigma_tier` | 0.80 | DECLARED | v1.5 S03 | none |
| S04 | `ability_grid` | (0.25, 0.50, 0.75) | DECLARED | v1.5 S04 | none |
| S06 | `rank_w_income`, `rank_w_ability` | 0.30, 0.70 | DECLARED | v1.5 S06 | none |
| S08 | `padv_clip` | (0.01, 0.999) | DECLARED | v1.5 S08 | none |
| — | `cred_prem_H`, `cred_prem_O` | 0.18, 0.03 | DECLARED | v1.5 T08/T09 | reported wage objects only; not in the choice block |
| — | `q_H_mult`, `q_O_mult` (survival) | **1.00, 1.00** | DECLARED | v1.5 had 1.25 / 0.55 | **removed from survival** (R4c): no tier survival penalty |
| — | `surv_pen_H`, `surv_pen_O` | **1.000, 1.000** | DECLARED | new | **no retained survival penalty.** Justification: A5 places the defect in the return; no measured tier-conditional survival differential is on disk (capacity utilisation HELD). Own sensitivity: `surv_pen_O ∈ {1.00, 0.95, 0.90}` in arms `S_survpen_*` |

**The parameter-fixing rule, stated before the run.** Every value above is fixed by the frozen v1.3/v1.5
declarations; `q_O = 0.55` is the v1.5 declared value, unchanged, at a different margin. No value was chosen by
reference to any level, any observed cell, the 17/33 bar or the `[55,85]` band. **A grid search that lands on a
passing cell would be `FAIL-RE-FIT`**, and the declared grids are reported as sensitivities only.

## 3. κ and the completion-unit bound

| id | parameter | value | status | provenance |
|---|---|---|---|---|
| K01 | `kappa` | 0.949 | **DERIVED** | observed PHL median of 8 pairs (`kappa_fwd_2026-11-20`, D133/D138). **DIAGNOSTIC ONLY** — not a forward constraint (D138/R6); not used in the scored arm |
| K03 | `kappa_lag` | 3 | DERIVED | exact 3-year lag (D118; `repro_path_2026-11-20`) |
| — | register | **admission rate (dimensionless), one unit** | DECLARED | R1: `e(s) = m·a_upper(s)·surv_upper(s) ≤ κ·comp_uis_lower(s−3)`; enforced object = audited object |

## 4. Measurement convention and scoring constants

| id | parameter | value | status |
|---|---|---|---|
| — | `m` = `meas_completion_factor` | **1.10** | **CONVENTION** (frozen; not a conversion) |
| — | observed bar | ≥ **17 / 33** cells within **± 5.0 pp** inclusive | copied from EXP-7, unchanged |
| — | crossing tolerance | **± 5 y** (D34/A6), thresholds 90/90/90 pp | D34 |
| — | `phys_cap` baseline | **1.15** | DECLARED (v1.3 P), **not re-chosen**; sensitivity grid {1.00, 1.05, 1.08, 1.15, 1.22, 1.30} |
| — | child-wage shock | × **1.10** | D134(2) |
| — | lower target | **80.896** pp observed (2021) / **80.76** pp internal-consistency | D140; both reported |
| — | survival ceiling | `surv_max` = (0.96, 0.91, 0.90, 0.90); lower ceiling at 2021 = **0.784589** | DERIVED from the declared law |
| — | clip boundaries | survival [0.02, 0.995]; completion and completion_uis [0, 1]; admission rate [0, 1] | DECLARED |

## 5. Determinism

One `numpy.random.default_rng(20261120)` PCG64 stream, the frozen v1.2 draw order and draw count; the V16 blocks draw
**nothing**; floats written `%.10g`; no wall-clock, hostname, PID or iteration order enters any output. Two complete
runs are byte-identical (guard G5).
