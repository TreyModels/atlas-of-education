# External audit — GPU ABC bundle @ `045a63e` (recorded 2026-11-25)

**Status: P0 FINDINGS ACCEPTED; scientific conclusions of the GPU bundle are QUARANTINED.**
**Auditor:** independent external review (ChatGPT), with its own NumPy reimplementation of the E1/Q3 synthetic
regression and wild-cluster bootstrap. **Lead verification:** every claim below that can be checked from the
committed code was checked and **confirmed** (evidence column). The auditor did not rerun CUDA jobs and neither
did we; the GPU hardware computed what it was told to compute — the defects are in the **specification and
inference**, not the arithmetic.

This document is the authoritative record. It supersedes any implication in
`docs/audit/GPU_ABC_AUDITOR_PACKET.md` that the ABC or E1/Q3 work is merely "pre-repair": the two mathematical
defects below are *structural*, not calibration choices.

---

## 1. Verified P0 findings

### P0-01 — The ABC has only FOUR independent moments, not five (verified)

The five advertised moments are overall participation 0.73, G9 0.67, G12 0.85, urban−rural gap 0.14, own share
0.68. The synthetic population is **420 G9 + 210 G12**, so for *every* parameter vector

```
M_overall = (2/3)·M_G9 + (1/3)·M_G12
```

and the targets satisfy the same identity exactly: `(2/3)(0.67) + (1/3)(0.85) = 0.73`. **Overall participation is
redundant.** Verified arithmetic; population constructed at
`gpu_abc_bundle/gpu_bray_abc_and_contest_surface_6param.py:50-52`, moments at `:82-90`.

Consequence: **5 advertised moments have maximum rank 4**. The corrected model has **6 active parameters**
(θ0–θ4, θ6) → **maximum Jacobian rank 4/6**, i.e. **at least two locally unidentified directions** at regular
interior points. The original 7-parameter model has at least three. The internal audit's "5 moments vs 6
parameters" understated this. Also: the "posterior correlation condition number" (25.96 → 21.03) does **not**
measure moment-Jacobian rank and must not be cited as identification evidence.

### P0-02 — The provider-choice parameter is analytic (verified)

With `V_none = 0`, `V_own = B_i`, `V_other = B_i + δ`, the conditional own-teacher share is

```
P(own | tutoring) = 1 / (1 + exp(δ))
```

independent of income, school quality, grade and urban residence. The 0.68 target therefore pins
`δ = ln(0.32/0.68) = −0.7537718023763802` exactly — no 200,000-draw ABC is needed for it. Archived estimates imply
69.51 % (7-param, δ = −0.8241) and 66.11 % (6-param, δ = −0.6682), both off the exact target. Verified arithmetic;
utilities at `gpu_bray_abc_and_contest_surface_6param.py:73-84`.

Reduced problem after substitution: **5 parameters** (θ0–θ4) against **3 independent participation moments**
(G9, G12, urban−rural gap) → **two further independent moments are required** for full local rank. This does not
validate Paper A's Jacobian proposition; the rank **must be recomputed** with whatever micro-moments Paper A
proposes.

### P0-03 — Synthetic population is degenerate (verified)

`is_g12 = [0]×420 + [1]×210`, `is_urban = [1]×210 + [0]×420` → **every Grade 12 pupil is rural; there are zero
urban Grade 12 pupils**, so the G12×urban cell is empty. There are **no school identifiers**; `school_gap ~ U(0,1)`
is drawn independently per pupil. Any claim about school-level remediation, urban differences, or distinguishing
tutoring motives is unsupported by this design.
Evidence: `gpu_bray_abc_and_contest_surface_6param.py:50-54`.

### P0-04 — The E1/Q3 selftest conflates minority-effect leakage with omitted-country-effect bias (verified DGP)

The selftest DGP (`gpu_e1_q3_wild_cluster_ri.py:172-185`) is:

```python
c_eff = rng.normal(0, 1.0, size=G)[cl]
x1    = rng.normal(0, 1.0, size=N) + 0.5 * c_eff     # country effect enters the regressor
y     = 0.2 + 0.8 * active_c * x1 + 0.3 * x2 + c_eff + noise   # ... and the outcome
```

The pooled regression omits `c_eff`, so it carries **omitted-variable bias**; clustered SEs do not address
omitted-variable bias. The auditor's independent NumPy negative control (true effect **zero in every country**)
found pooled β = 0.3054, t = 4.975, wild-cluster p = 0.0005 — i.e. **the procedure is "significant" when the true
effect is null**. Country FE moved the original estimate from 0.4447 to 0.1053 (p ≈ 0.076). Therefore the shipped
selftest **cannot** attribute its result to minority-effect leakage. The auditor's reproduction of the reported
pooled numbers (β = 0.4447407388610451, SE = 0.08291358451449393, t = 5.363906788800103) is consistent with the
committed code.

### P0-05 — The country-block permutation cannot test the within-country FE estimand (verified algebra)

The permutation (`gpu_e1_q3_wild_cluster_ri.py:144-160`) sets `x*_it = x̄_{π(i)} + (x_it − x̄_i)`. After country FE,

```
x*_it − x̄*_i = x_it − x̄_i
```

**identically, for every permutation.** The within-country regressor is invariant, so every permutation yields the
same within coefficient (up to rounding) — adding the missing FE to the existing permutation **cannot repair it**.
This is an algebraic identity, not a finite-sample issue. A different resampling scheme must be justified against
the actual estimand (restricted wild-cluster bootstrap, a justified whole-trajectory permutation, or a
null-DGP simulation that preserves temporal dependence), and country exchangeability must itself be defended.

### P0-06 — The contest solver is the r = 1 first-order condition with r inserted as a multiplier (verified)

For a single-prize Tullock contest `P_i = x_i^r / (x_i^r + A)`,
`∂P_i/∂e_i = r·A·x_i^{r−1} / (x_i^r + A)^2`. The implemented closed form

```
e_i = sqrt(r · ΔV · A · y_i / p) − A − x0
```

is the **r = 1** solution with `r` multiplied into the prize. Changing `r` therefore changes the *incentive scale*,
not the discrimination exponent. The solver also depends only on the combination `r·ΔV/p`, so distinct
`(r, ΔV, p)` produce identical cells — the 2,000-point grid carries far less independent structure than its size
suggests. Additional gaps: no convergence diagnostics after 30 fixed-point iterations, no admission-probability
distribution, no capacity-clearing check, no fee-abolition parameter despite the H2 docstring, and seat shares stop
at 50 % so the descending arm of any inverted-U cannot be observed. **The "100 % paradox" result is a toy-model
result and is quarantined.**
Evidence: `gpu_bray_abc_and_contest_surface_6param.py:151-169`.

### P0-07 — Execution-integrity defects (verified)

- `run_gpu_jobs.sh` uses `set -u` only; `run()` captures `PIPESTATUS[0]` but only **echoes** it — no `set -e` /
  `pipefail` — so a failed job does not stop the sequence and the run ends with `DONE`. (The deposited logs do show
  `EXIT 0` per job, so this run was clean, but the harness cannot detect failure.)
- The **6-parameter run is absent from the runner**; it cannot reproduce the deposited bundle.
- `gpu_bray_abc_and_contest_surface_6param.py` retains the original `--out-dir` default
  (`./results_rtx3080ti/bray_and_contest`), so a default run would **overwrite** the 7-parameter output.
- **Accepted draws are discarded** (only `n_accepted`, `best_theta`, condition number are returned) → no posterior
  diagnostics, predictive checks, or uncertainty are possible from the deposit.
- The docstring advertises a **"100-Fresh-Seed Stability Bank"** that is **not implemented** anywhere.
- Targets are hardcoded; there is only one synthetic population per run; survey measurement uncertainty is absent.

### Corrections to our own audit documentation (accepted)

1. `docs/audit/GPU_ABC_AUDITOR_PACKET.md` and `gpu_abc_bundle/README.md` called the unused parameter "the **7th**
   coordinate"; it is the **6th coordinate, θ5 (0-indexed 5)**. Corrected.
2. `gpu_abc_bundle/RUN_REPORT.md` says "5 active parameters and 5 moments"; it is **6 active parameters and
   5 advertised / 4 independent moments**. Correction appended to the bundle copy (the legacy record is preserved).
3. `MANIFEST.sha256` appended `<- original:` annotations to checksum lines, so it was not usable with
   `sha256sum -c`. Now split into a **canonical** `MANIFEST.sha256` plus `MANIFEST_ORIGINS.csv`.

---

## 2. Quarantine

From this commit, **no output of the GPU ABC / contest-surface / E1-Q3 bundle may be cited** as a calibration, a
contest boundary map, or an E1/Q3 reconstruction. Evidence labels remain `AUTHOR-REPORTED` / `PRE-REPAIR` /
`UNRESOLVED`. GPU-vs-CPU numerical agreement (8.9e-15) validates **arithmetic only** and does **not** promote any
claim to `VALIDATED`.

## 3. Dispositions and required deliverables

| P0 | work | owner | deliverable |
|---|---|---|---|
| 01 | analytic AD Jacobian of the 5-moment/6-param map: singular values, numerical rank, null-space directions, scaling sensitivity; repeat with Paper A's proposed micro-moments | contest-math | `ABC_IDENTIFICATION_AUDIT.md` |
| 02 | analytic δ substitution; reparameterized participation model; survey-uncertainty propagation | contest-math | part of the same report |
| 03 | realistic crossed grade×urban population, school identifiers, within-school dependence, empirical covariate distributions; parameter-recovery on 100 independent populations; save accepted draws + posterior predictive | qa-verifier | `SYNTHETIC_DGP_VALIDATION.md` |
| 04 | factorial simulation: minority-effect share {0, 5, 15, 50, 100 %} × confounding {0, .25, .5, 1} × estimator {pooled, FE, FE+year}; type-I error, power, bias, CI coverage; 2,000 datasets/scenario | qa-verifier | `BOOTSTRAP_SIZE_POWER_RESULTS.parquet` + report |
| 05 | replace the within-invariant permutation with a scheme justified for the actual estimand; identical pre-generated weights for GPU-vs-CPU; independent reference implementation | qa-verifier | part of the bootstrap report |
| 06 | independently derived general-r Tullock optimum; exact small contests; capacity clearing; convergence diagnostics; seat shares to universal admission; benchmark vs engine PL | contest-math | `CONTEST_MATH_VALIDATION.md` |
| 07 | failure propagation, unique output dirs, atomic/hashed artifacts, 6-param in runner; corrected experiment manifest + claim ledger | atlas-commander | `CORRECTED_GPU_EXPERIMENT_MANIFEST.json`, `SCIENTIFIC_CLAIM_LEDGER.md` |

**Sequencing (binding):** stages 1–2 (rank audit, analytic δ, DGP validation) and the bootstrap **size** test come
before any full-scale experiment. No GPU campaign; all of the above is CPU-cheap (≤8 workers on the 10-CPU box or
the Mac). "Begin with the mathematical corrections and negative controls."

**Also preserved from the auditor:** retain the identification defect and the regression negative control as the
core of the proposed AI-assisted-research failure paper; do not use the existing ABC outputs to support the
manuscript's Jacobian theorem.
