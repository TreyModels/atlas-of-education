# PRE-REGISTRATION — M2c-2: conforming E1-design recovery test (SIMULATED; submit for acceptance BEFORE any run)

**Written 2026-11-20 after Council D32 (14:13 M2c = pre-standard/provisional; conforming M2c-2 required under a new
predeclaration). NOT RUN. This predeclaration is submitted for Council intake acceptance under
`08_council/brief_013/INTAKE_ACCEPTANCE.md` (M2c bullets) and must be ACCEPTED before any execution.** All content
is simulated; no observed data; no direction claim (R13/EQUIVALENT); no model fitting; no closed-claim content.

## Common gate bullets
- **Gate copy:** `GATE_ACK_BRIEF013.md` (SUCCESS_CRITERIA §2–§4 + both Amendment A1 texts, verbatim) is in this
  directory; M2c-2 is bounded by it.
- **Data provenance:** simulated only; no observed series used; no target used as a parameter; no imputed cell.
- **Labels:** all cells SIMULATED; recovery/failure results are design properties, not evidence about the world;
  no direction claim; conditional reproduction would be labelled PASS-CONDITIONAL (A1 §3).
- **Rivals:** four candidate configurations (demand-led, supply-led, complementary, outside/cohort-fertility) are
  fitted to the same simulated data with the same information set; the outside configuration is included so the
  estimator can reject direction rather than force it.
- **Deliverables:** `NEW:` with path, commit/hash, one-line finding, what it changes; `OP:` milestone; all cells
  reported including failures.

## DGP (four truths, declared)
Panel of N = 60 regions × T = 20 years (fixed; also N=30×T=10 as a low-power stress cell). Two shocks:
`S` = supply expansion (region×post-2 timing), `D` = demand expansion (region×post-3 timing), each with
overlap allowed; `Y_it = α_i + λ_t + βs S_it + βd D_it + γ S_it·D_it + ε_it`, ε ~ N(0, σ²).
Truths and parameters (declared grid, fixed seeds 0–99; 100 reps per truth; no post-hoc changes):
1. **DEMAND_LED:** data generated with D → schooling only (`βd>0`, no S feedback, γ=0) and structural path as
   declared in the simulation script.
2. **SUPPLY_LED:** S drives Y only (`βs>0`, no D response, γ=0).
3. **COMPLEMENTARY:** both effects and γ ∈ {0.30 (detectability cell), 0.0 (null cell)}.
4. **OUTSIDE (cohort/fertility):** Y driven only by a nuisance cohort/fertility path; no S/D effects, γ=0.
Effect sizes: βs=βd=0.5 (baseline), γ=+0.30 (predeclared detectable size) and γ=0.0; noise σ ∈ {0.5 (power cell),
1.0 (stress)}; shock timing/overlap declared in the script; seeds fixed.

## Exact E1 estimator (the one to be fielded)
Two-shock interaction DiD/event study: `Y_it = α_i + λ_t + βs S_it + βd D_it + γ S_it·D_it + X'δ + ε_it` with unit
and year fixed effects, equally weighted observations, CR1 cluster SE by region; placebo estimator: (a) pre-period
placebo timing (S,D shifted 3 years earlier; must be null), (b) null-γ placebo. Channel selection: the four
configurations are fitted to the same data and selected by AIC (predeclared); a predeclared rejection rule allows
"outside" (no direction) to be selected.

## Estimands and predeclared thresholds (no post-hoc change)
- **Recovery rate** (correct configuration selected) — **≥ 0.80**.
- **Forced-ID rate** (outside truth assigned to any candidate D/S/C) — **= 0.00**.
- **False-positive complementarity** (γ=0 truth classified complementarity) — **≤ 0.10**.
- **Complementarity detection rate** at γ=0.30, σ=0.5 — **≥ 0.80**.
- **Sign accuracy** of γ̂ when a direction configuration is selected — **≥ 0.80**.
- **Power** at the predeclared size (γ=0.30, σ=0.5) — reported; if power < 0.80, E1 cannot be fielded as-is.
**Failure rule (abandon-E1):** if ANY threshold fails → **E1 is not sufficient; do not field it**; report the failure
and either redesign E1 (new arms/estimator, new predeclaration) or abandon the direction claim (programme reduces to
conditional reproduction + equivalence). This is an **R3/R13 event**. No silent dropping; all cells reported.

## Non-conformance note
This document supersedes only the pre-standard M2c (`M2C_PREREG.md`, 14:13) for acceptance purposes; that run remains
labelled provisional/internal and is not cited as the accepted M2c cell (D32). **No run will occur until this
predeclaration is accepted.** No git writes (executor commits).
