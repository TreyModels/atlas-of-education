# PRE-REGISTRATION — corrected small experiment (task-22; committed BEFORE code fixes and run)

Approved by Trey. **SIMULATION only; no causal language; no scaling.** Old exploratory results (v2/v2b/Phase B) stay labelled exploratory; this is the first corrected confirmatory run.

## Declared grid (fixed)
- **Worlds:** P, S, C, R (literature parameterisation, Phase A) + **s=0** zero-signal world **included** in the matrix; misspecified Rm retained as a secondary diagnostic only (not in the primary decision).
- **N = 10,000 households/country; 64 countries; 25 years.**
- **10 independent country blocks**: fresh country parameter draws per block (no reuse of the same 512/64 draws across blocks).
- **6 specifications as declared:** S1 10y differences + decade FE; S2 **true 5-year windows** + bin FE (no reuse of 10y logic); S3 levels + country + year FE; S4 10y + income control; S5 5y + region-style control; S6 first differences.
- **Links:** 7 kernel-generated variables (child employment, study+work, visible work, hidden work, tutoring, learning, income); fertility/CEB deferred (declared).
- **Uncertainty:** **cluster-robust CIs over countries** (no binomial-over-cells).
- **Measurement-error dose:** 0×, 1× (σ=0.05) only (keep the run feasible); dose 2× dropped and declared.
- **Decision criterion:** effect sizes + **TOST equivalence with pre-declared margin** (margin: |slope difference| ≤ 0.05 in absolute slope units; equivalence declared only if the 90 % CI of the difference lies wholly within ±0.05) **and/or predictive discrimination** (out-of-block cross-validated separation of worlds; report AUC/accuracy with CIs). **"Non-significant" alone is not equivalence.**
- Expected cells: 7 links × 6 specs × 2 doses × 10 blocks × (1 grouping dimension: full sample + 4 declared types) ≈ 3,360 cells; 5 worlds → ≤16,800 fitted regressions; 64×5 kernel runs per block = 3,200 runs at N=10k (~1–2 min on 96 cores).

## Corrections applied before this run (must be smoke-tested first)
1. Phase B: `WOMEN 400 → 4000`; corrected B1 within-mother spacing definition with explicit denominators; **feature-specific admissibility gates**; **clean independent s=0 draws** (no duplicated observations across labels).
2. Matrix driver: all 6 specs; s=0 present; true 5-year windows; **independent block country draws**; **cluster-robust CIs**; departure log.
3. 2-seed smoke test on the hash-verified files before the full run; hashes recorded.

## Failure/stop rules
If the smoke test fails, stop and report the traceback from the verified copy; do not launch the full run. Old outputs preserved; no deletion.

## Deviations log
- (to be filled)
