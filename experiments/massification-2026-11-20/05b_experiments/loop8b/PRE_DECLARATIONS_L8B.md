# PRE-DECLARATIONS — Loop 8b: ECI-inclusive frontier re-run (wiring correction)

**SYNTHETIC / POSSIBILITY-ONLY. Programme stays CLOSED; brief-008 identification limits stand; not evidence.**
Wiring correction to loop 8 (which marked ECI PENDING on a false absence check): `04_data/complexity/
ECONOMIC_COMPLEXITY.csv` and `09_relations/data/economic_complexity_panel.csv` exist and are used here.
Same LHS design: **256 draws × 5 matched seeds**, same targets/bands as loop 6, no tuning, no fitting.

**Process note (honest):** the wired frontier run was launched before this file was committed (the wiring
and distributions had been fixed in the code from the task specification, and results were not read until
after writing this file). Recorded as deviation L8B-1 in ERROR_LOG_L8B.md; the predeclaration contents below
match exactly what was executed.

## ECI metric and country values (observed, not fitted)
- Metric: **`eci_hs92`** (full 30/30 coverage; strongest GDP fit per R49). **`eci_sitc` robustness only — never
  scored**. Ranks, `growth_proj`, and spliced HS12 are **never used**.
- Country values (mean `eci_hs92`, 2015–2024, 10 obs each): **KOR 1.754, HKG 1.218, PHL 0.718, KHM −0.281**;
  reference (mean of the four) = **0.852**. ECI enters as a country-level state/type variable, z-like scale.

## ECI conditioning — exactly which parameters (literature-grounded distributions; "assumed" where noted)
| # | Model object (file/parameter) | ECI conditioning | Distribution |
|---|---|---|---|
| E1 | shadow demand, **terminal-stage gate stakes** (loop-8 `make_cfg`: `cfg['stakes'][last]`) | `stakes_last *= (1 + b_eci_stake·(eci−0.852))` | b_eci_stake ~ LHS[0.05, 0.25]; mapping assumed from R41–R43 positive ECI elasticities (0.165–0.306) |
| E2 | shadow demand, terminal-stage **credential returns** (`cfg['returns'][last]`) | `returns_last *= (1 + b_eci_ret·(eci−0.852))` | b_eci_ret ~ LHS[0.05, 0.20]; sign uncertain in R44/R48 → mapping **assumed** |
| E3 | twoway cohort flows, **completion & tertiary transition** (`s0`, `c0`) | `s0,c0 *= (1 + b_eci_comp·(eci−0.852))` | b_eci_comp ~ LHS[0.05, 0.20]; assumed from R42/R43 (0.165–0.202) |
| E4 | twoway **formal-job creation elasticity** (`eps_ec`) | `eps_ec_eff = eps_ec + b_eci_formal·(eci−0.852)` | b_eci_formal ~ LHS[0.05, 0.20]; assumed (R41/R47 positive but ns; R48 negative) |
Unchanged: all other loop-8 wired relations and declared priors; demand-level intercept fixed A0 = −1.5.

## Unscoreable ECI rows (direction-only; NEVER scored as inside/outside)
R44 wage-and-salaried share (**not significant**), R45 cumulative-growth/ECI premium (**fails to replicate;
negative ns**), R46 youth literacy (jointly produced with ECI — auxiliary, not a mechanism test), R47
spending×ECI interaction (**not significant**), R48 schooling×ECI interaction (**negative — opposite the
prior**), R49 metric choice (**methodological recommendation, not an estimate**), CX-01…CX-04 (direction-only
by construction). `eci_sitc` values are carried as robustness only and are not used in any scored target.

## Delta rule (predeclared, same as loop 8)
- **Shrink** = a target that was **0/256 in loop 6** becomes **≥1/256 in loop 8b**; also report a **material
  change** as ≥+10 inside/256 for a target that was non-zero. Report ONLY the five targets: KOR stage
  gradient, HKG stage gradient, KOR fee, KOR income-gradient, KOR two-margin joint (R23: participation
  falling 86/75.4/66.4 ±5pp AND intensity margin ≥+15%; joint = both).
- If empty support persists (KOR gradient still 0/256), say so plainly. No threshold changed after results.
