# WHERE TO LOOK — code review index (25 Nov 2026)

Repo: **https://github.com/TreyModels/atlas-of-education**

This index is for an external reviewer (Gemini Neon). **Review the scripts and their logic, not the results** —
several branches contain exploratory or in-progress runs. Every script is labelled simulation/synthetic where
relevant; no causal claims are intended unless explicitly stated.

## Core full-system / massification work

| what | branch (head) | script paths |
|---|---|---|
| Full-system multiverse (144 equation-choice combinations × seeds; eduengine) | `research/masseng-edsystem-2026-11-25` (`b7108da`) | `research/records/2026-11-25-masseng-edsystem/run_edsystem_multiverse.py`, `analyze_edsystem_multiverse.py` |
| Statistical tests of that multiverse (cluster-robust OLS + seed FE + Holm + stratum checks) | `research/edsystem-tests-2026-11-25` (`aadbbb4`) | `research/records/2026-11-25-edsystem-tests/test_full_system.py` |
| 10-script Master Equation Inventory suite (massification; tutoring one module) | `research/equation-suite-2026-11-25` (`a7fcfb9`) | `research/records/2026-11-25-equation-suite/scripts/eq01_family_demand.py` … `eq10_tutoring_shadow.py`, `eq_common.py` |
| Observed-core model (state supply + demand + attainment + structural change from panels) | `research/observed-core-2026-11-25` (`cfb9418`) | `research/records/2026-11-25-observed-core/scripts/` |
| Equation test bench (pre-registered plan + partial data-level bench) | `research/equation-test-bench-2026-11-25` (`3451693`) | `research/records/2026-11-25-equation-test-bench/test_bench.py`, `TEST_PLAN.md` |

## MASSENG coupling / engine boundaries

| what | branch (head) | script paths |
|---|---|---|
| MASSENG v5 switchable tutoring subclass (bit-identical switch-off) | `research/masseng-tutoring-2026-11-25` (`b9d68c1`) | `research/masseng-v6/model/masseng/tutoring.py`, `research/records/2026-11-25-masseng-tutoring/scripts/` |
| v6 prototype: score/quota gate + labour/earnings module | `research/masseng-gate-jobs-2026-11-25` (`6728494`) | `research/masseng-v6/masseng_v6/education/gate.py`, `research/masseng-v6/masseng_v6/labour.py`, `research/records/2026-11-25-masseng-gate-jobs/scripts/` |
| Rural–urban migration extension of the eduengine multiverse | `research/masseng-edsystem-migration-2026-11-25` (`d57d126`) | `research/records/2026-11-25-masseng-edsystem-migration/` scripts |
| MASSENG v5 claim-layer audit (what the engine actually estimates) | `research/masseng-audit-2026-11-25` (`8429422`) | `research/records/2026-11-25-masseng-audit/scripts/audit_claims.py` |
| Audit of the equation suite + full-system claims (critiques, false positives, buried FAILs) | `research/edsystem-audit-2026-11-25` (`fe9c6ee`) | `research/records/2026-11-25-suite-audit/scripts/audit_claims.py` |

## Shadow-education demand + reality check (one corner, not the centre)

| what | branch (head) | script paths |
|---|---|---|
| First-pass demand/learning/gate/earnings model + Bray reality check + multiverse | `research/shadow-equations-review-2026-11-25` (`264c059`) | `research/records/2026-11-25-shadow-equations/shadow_model.py`, `run_shadow_scenarios.py`, `bray_reality_check.py`, `bray_parallel.py`, `multiverse_run.py`, `test_shadow_model.py` |
| Simplified v5 coupling (superseded by branch above) | `research/synthetic-corrected-2026-11-24` (`26d9b27`) | `research/records/2026-11-24-synthetic-corrected/synth_loop/` |

## Data / DHS / port

| what | branch (head) | script paths |
|---|---|---|
| DHS public-API ecological estimation (corrected FE parameterisation) | `research/dhs-api-ecological-2026-11-24` (`fe762b9`) | `scripts/estimate.py` |
| DHS IR pipeline + verification gate (no microdata yet) | `research/dhs-acquisition-2026-11-24` (`f4a7f65`) | `scripts/ir_pipeline.py`, `EXECUTION_READY.md` |
| Apple Silicon port: CuPy shim, MLX/NumPy kernels, equivalence tests | `research/apple-silicon-gpu-2026-11-24` (`52d74ec`) | `gpu_compat.py`, `kernels_np_mlx.py`, `shim/cupy/__init__.py`, `tests/`, `run_apple.sh` |
| Full-system data readiness matrix (what is observed vs assumed) | `research/full-system-data-2026-11-25` (`34fd7c9`) | `research/records/2026-11-25-full-system-data/` |

## Older synthetic / matrix / Phase B records (context)

- `research/synthetic-matrix-2026-11-24` (`77d6f23`) — `run_matrix_v2b.py`, matrix results (exploratory pending audit).
- `research/synthetic-phaseb-2026-11-24` (`2b1a160`) — `synth_loop/run_phaseb.py`, `fertility.py`.
- `research/synthetic-loop-2026-11-24` (`394fb32`), `research/suite-redesign-2026-11-24` (`1de7d33`).
- `research/handoff-2026-11-24` (`0bbfc65`) — HANDOFF + dashboard pointers; start here for narrative context.

## What to review, concretely

1. **Correctness of the estimators/simulators**: seed handling, cluster-robust SEs, fixed effects, Holm correction, identifiability guards, empty-stratum handling, zero-variance outcomes.
2. **Identification claims**: does a script claim more than the data/design can identify? Are "supported" verdicts actually pre-registered?
3. **Pre-registration discipline**: rules declared before runs vs rules changed after; FAILs not buried; deviations logged.
4. **Boundaries**: no invented learning/score/jobs/rural/migration mechanics; `MASSENG v5` labels must not be applied to standalone simulations.
5. **Labels**: SIMULATION / OBSERVED / RECONSTRUCTED / LITERATURE_TARGETS correctly attached; no causal language.

Known open critiques (already recorded, not hidden): the suite audit at `research/edsystem-audit-2026-11-25` lists 17 claims to downgrade/withdraw, including the "3 pre-declared FAILs" framing, buried FAILs, p-values introduced against a "no p-values" prereg, empty-stratum false positives, and incorrect overlap/η² prose. Review against that audit too.
