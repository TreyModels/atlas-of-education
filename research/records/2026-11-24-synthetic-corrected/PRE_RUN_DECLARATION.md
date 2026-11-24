# PRE-RUN DECLARATION — corrected matrix core (task-23) — committed BEFORE the run

**SIMULATION only. Not evidence. No causal language.** The approved pre-registration is
`research/records/2026-11-24-synthetic-matrix-v2/PRE_REGISTRATION_corrected.md` at commit
`77d6f23` (blob `618f4d1c…`, sha256 `eab63120…`), committed before this code and before any
run. Code hashes are recorded in the run manifest produced by `synth_loop/run_corrected.py`.

Scope of this driver: the **matrix core** of the pre-registration (worlds, blocks, specs,
uncertainty, TOST/effect-size decision, out-of-block predictive discrimination). The
corrected Phase B birth-history layer runs as a separate self-contained driver
(`run_corrected_phaseb.py`) after this matrix run is committed (Lead sequencing; the matrix
must not block on Phase B).

## Declared grid (frozen before the run; no tuning)

- **Worlds (5):** P, S, C, R (literature parameterisations, Phase A) + **s0** = the declared
  s=0 zero-signal world, included in the matrix. Rm is a secondary diagnostic only, not run
  here (not in the primary decision).
- **N = 10,000 households/country; 64 countries; 25 years.**
- **10 independent country blocks:** fresh country parameter draws per block;
  `default_rng(SEED+1000+block)`, `SEED=20261124`. Block sha256 hashes must be pairwise
  distinct (self-check aborts otherwise).
- **4 declared country types** (prereg says "4 declared types" without enumerating them):
  declared HERE before the run as the first four rows of the v2 eight-type table, 16
  countries per type, 64 total. Within-type jitter `N(0, 0.05)` clipped to the declared
  ranges.
- **6 specifications:** S1 10y differences + decade FE; **S2 true 5y windows (Δ5) + bin FE**;
  S3 levels + country + year FE; S4 10y differences + income control; **S5 true 5y windows
  (Δ5) + region-style control + bin FE**; S6 first differences (Δ1) + year FE.
- **Links (7):** child employment, study+work, visible work, hidden work, tutoring, learning,
  income; fertility/CEB deferred (declared).
- **Measurement-error doses:** 0× and 1× (σ = 0.05 lognormal on each link series and on GER).
  2× dropped as declared.
- **Groupings (5):** full sample + the 4 declared types.
- **Uncertainty:** cluster-robust CR1 sandwich over countries inside each independent block;
  cross-block inference from the 10 independent blocks as paired replicates (Student t,
  df = 9). **No binomial-over-cells uncertainty anywhere.**
- **Decision:** effect sizes + **TOST** with pre-declared margin `|Δslope| ≤ 0.05`
  (equivalence only if the 90 % CI of the paired difference lies wholly within ±0.05) and
  **out-of-block predictive discrimination** (train blocks 0–4, test blocks 5–9; 5-class
  nearest-centroid accuracy/AUC with CIs). "Non-significant" alone is **not** equivalence.
- **Cell arithmetic:** 41 link×spec combinations (S4 × income is undefined: the declared
  control is the outcome) × 2 doses × 5 groupings = **410 cells**; ×5 worlds = 2,050 fitted
  regressions per block, 20,500 in total; 4,100 pairwise world contrasts. The prereg's
  "≈3,360 cells / ≤16,800 regressions" assumed 4 groupings; the declared grouping dimension
  ("full sample + 4 declared types") gives 5. This is an arithmetic clarification only —
  no declared design element was changed (recorded in the departures log).

## Declared exclusions (recorded before the run)

- **S4 × income** is not defined (income is both outcome and the declared control). Excluded
  and counted, never silently replaced by S1 (the audited v2 behaviour).
- **Country-level classifier features** use S1, S2, S4 only. S3 (country FE) and S6
  (24 first differences with year FE) are not identified at the individual-country level and
  S5's region control is absorbed within a country; those specs are excluded from the
  predictive-discrimination step.

## Smoke rule

`--smoke` (2 blocks, 8 countries, N=1,000) exists only to exercise every code path on
hash-verified files. If the smoke fails, the verified-copy traceback is reported and the full
run is not launched. Smoke output is `results_smoke/` and is never quoted as a result.
