# G2-A/G2-B identifiability — MULTI-SEED Jacobian (frozen V540-FREEZE calibration map)

**Status: multi-seed local identifiability estimate — rank 4/4 at both starts, null_dim 0, but the Jacobian remains
materially start-dependent. LOCAL identification only; no global-identifiability claim; no condition-number
identification claim.** Artefact `results/audit/newgen/identifiability_multiseed_846c9e0_pin.json`;
runner `identify_multiseed3.py` (strictly **max 2 concurrent eval columns**, sequential seeds); evaluator
`eval_one.py` (per-seed `G2A_SEED`, isolated subprocess); engine `/tmp/gate1-540/engine` = clean `98baf6b` (numerics
unchanged vs `846c9e0`; pre-fix pin recorded); frozen spec, 5 matched seeds per finite-difference column, declared
steps 5 %/3 %/5 %/4 %, central differences, 2 starting points; 90 evaluations; host run 1,361 s (~1.2 min/eval,
2 columns concurrent).

## Result

| start | rank | singular values | null dim |
|---|---|---|---|
| (1.0, 1.0, 1.0, 1.0) | **4/4** | 50.030, 32.596, 1.907, **0.341** | 0 |
| (1.5, 0.8, 1.5, 0.95) | **4/4** | 46.916, 17.058, 6.801, **0.128** | 0 |

**Stability:** max |ΔJ| = **11.476**, relative **0.287** (one-seed forward-difference run was max|ΔJ| 26.5, rel 0.52).
Multi-seed averaging roughly halves the start-to-start Jacobian drift but does **not** eliminate it; the smallest
singular value still moves 0.341 → 0.128 across starts.

## Interpretation (binding for Gate 2)

1. The 4-moment calibration map is **locally full-rank** at both tested points on the frozen spec; there is no null
   direction at this parameterisation.
2. **Local full rank is not global identification**, and the start-dependence of the Jacobian/SVs means the
   conditioning of the fourth direction is not settled. Gate-2 must (i) use multi-seed Jacobians with declared
   perturbation sizes (done here), (ii) report rank/SV/null space across ≥3 starts, and (iii) not infer identification
   from condition numbers.
3. The v1 one-seed run had a hidden single-seed defect (all columns seed 0) — fixed before this run; this artefact is the
   authoritative multi-seed result.
