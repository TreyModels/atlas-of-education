# REPORT — synthetic diagnostic loop v2, Phase A

**Task-18** · branch `research/synthetic-loop-2026-11-24` · base `fc96f84` · run **135.9 s** on the Apple M1,
port NumPy backend (NumPy/MLX kernel bit-identical; batch layout `N=10,000, threads=256, blocks=40`).
**SIMULATION — diagnostic and trap-setter, not evidence about real economies. No causal language.**

**Phase A delivered** (schooling/child-labour/tutoring worlds, macro wall, static micro tie-breakers,
construct-correct ABC pre-audit, DHS day-one signature in `PRE_REGISTRATION.md` §6). **Phase B** (fertility /
birth-history dynamics: death-spacing, parity progression, age at first birth) is **pre-registered but not
run** — it requires integrating the dose-model fertility engine and is specified in `PRE_REGISTRATION.md` §4.

## 1. Worlds (non-degenerate; parameterisation committed before any test)

Four literature worlds + `s=0` null (identical across labels): Basu–Van (P), Nordtveit (S), Bray/Jayachandran
(C), Pritchett (R). The shipped degeneracy (GER 0.000 for two worlds; visible work 0.87–1.00) was fixed before
the run; a first Nordtveit design (`w_push=1.5, psi=0.55`) remained structurally unable to enrol (GER 0.00) and
is documented as a design finding in `PRE_REGISTRATION.md` §1. All four worlds calibrated to the declared target
`M*=[0.60,0.55,0.27,0.77,0.47,0.50]` within ±0.10: max |residual| **P 0.030, S 0.029, C 0.080, R 0.097**
(records in `results/calibration.json`). `s=0` identity: **max abs difference 0.0** (exact).

## 2. Macro-wall verdict: **separable** (the wall is NOT reproduced)

Exact 10-year country-decade FE regression (`D_cl_observed` on `D_GER`, decade FE, 24 country clusters, 24
synthetic countries per world, paired nuisance):

| world | macro slope | 95% bootstrap CI |
|---|---|---|
| P Basu–Van | **−0.234** | see `results/h1_macro_wall.json` |
| S Nordtveit | **−0.346** | " |
| C Bray/Jayachandran | **−0.370** | " |
| R Pritchett | **−0.150** | " |

Joint interaction test **Wald χ²(3), p ≈ 0** (p < 1e-20); pairwise slope-CI overlaps below the 0.75 wall
threshold. Under a real FE test the four literature worlds **separate**; we report that and do not tune for a
wall. Implication (simulation-conditional): the "macro wall" is an **empirical** finding about country panels
(E1/Q2/Q3), not a generic consequence of distinct micro mechanisms — this parameterisation does not generate it.

## 3. Micro tie-breaker panel (Phase A): **cannot test (F3)** — the trap is caught, again

Measured-variable panel (survey layer; hidden work unmeasured): held-out accuracies T1 0.846, T2 0.887,
T3 0.804, T4 0.642; but the pre-registered **admissibility gate rejects every one as a transform of the DGP
weights**: R² = **T1 0.981, T2 0.990, T3 0.996, T4 0.934** (> 0.90). s=0 control and the algebraic-equivalence
placebo are at chance; label permutation is clean. **Verdict: cannot test (F3).** The static observables cannot
serve as a tie-breaker even in non-degenerate, literature-anchored worlds — which is precisely why Phase B needs
*non-transform dynamic* observables (birth spacing after child death; parity progression / age at first birth)
and why the DHS day-one signature is built on **design-based** identification, not on simulation screening.

## 4. Identifiability pre-audit — equal-weight rejection ABC (5,000 draws, top 10 % = 500 accepted)

Construct-correct targets: WDI `SL.TLF.0714.ZS` **children in employment** (E8 mean 31.4 % of children; **not**
child labour), model-scale GER target 0.80, study+work share of employed children 0.70. All nuisances logged
(`results/abc_preaudit.json`). 0.80 prior-width gate:

| parameter | width ratio | verdict |
|---|---|---|
| `w_push` | 0.376 | **identified** |
| `w_tutor` | 0.378 | **identified** |
| `div` | 0.837 | **UNIDENTIFIED** |
| `w_pov` | 0.872 | **UNIDENTIFIED** |

Aggregate data pin down the school-push and tutoring dimensions but **cannot** pin subsistence intensity or
teacher diversion — the pre-audit's justified finding, not a failure. The crashed exp3 path is not reused; the
`region/SSF` query bug is bypassed by explicit E8 country lists, and every nuisance is logged.

## 5. DHS day-one micro signature (deliverable)

Pre-registered in `PRE_REGISTRATION.md` §6: individual-level `CEB ~ education` with cohort FE + round FE +
pre-declared controls, DHS weights and clustered SE; EFR vs CEB construct split (never "TFR"); Phase A/B
tie-breaker panel computed on DHS IR/child modules where available; transport decision rule (DHS estimate inside
the simulation's pre-registered interval with same sign/ordering, else non-transport). It is a signature to
**test**, not an inference from this simulation.

## 6. Limitations

Model-conditional only; four stylised worlds; one design point; ±0.10 calibration tolerance (wide because the
model's work attractor limits attainable employment shares — a model limitation, declared); Phase B not run;
the ABC target GER is a declared model-scale value (WDI gross primary enrolment is not comparable to the model
share); synthetic aggregates are not country data.

## 7. Files

`PRE_REGISTRATION.md`, `synth_loop/{port_backend,model,calibrate,macro,measure,tiebreak,run_phase_a}.py`,
`results/{calibration,h1_macro_wall,h4_tiebreakers,abc_preaudit,run_manifest}.json`.

## 8. Declared deviations log

- Literature parameterisation fixed after a non-confirmatory design probe; the first Nordtveit parameterisation
  was degenerate (GER 0.00) and is documented (PRE_REGISTRATION §1) — a design finding, not a result.
- Verdict logic reuses the redesign's corrected rule (rejected-by-gate tie-breakers are ineligible; F3).
- `cl_target` pulled live from the World Bank API at run time (E8, SL.TLF.0714.ZS, 1990–2023); fallback
  constant 0.314 if the API fails.
