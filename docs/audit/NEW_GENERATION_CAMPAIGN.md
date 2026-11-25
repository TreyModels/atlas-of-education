# NEW-GENERATION CAMPAIGN — status ledger (repaired engine, frozen spec)

**Framing (operator, 2026-11-25):** Gemini-era docx numbers are the **AUTHOR-REPORTED baseline**; the repaired-engine
runs are a **NEW GENERATION** (not reproductions, not validations). Preregistration
`docs/audit/GATE2_PREREGISTRATION.md` (commit `dba0ecc`, frozen before launch) + addendum A1.

## 1. Frozen base

* Engine clean `git archive 98baf6b` (core `72cbddf7…`, contest_math `23a01730…`, tutoring `7a6fd4c3…`, labour
  `0ccfb3ce…`); spec `docs/audit/canonical_spec.json` (content sha `c5f9e2de…`, file `35576fed…`), V540-FREEZE,
  N=300, T=46, measure_from=18; KR primary = `GATE_SPECS['KR-TRACKED']`, KR sensitivity = `KR-SINGLE`.
* Box: 10-CPU cgroup, declared venv py3.10.8/numpy 2.2.6/scipy 1.15.3, nice 10, BLAS/OMP=1, ≤10 workers, per-job
  dirs, hashes/logs/exit codes, no silent partials.

## 2. Paper B — 18 arms × 100 matched seeds (1,800) + KR-SINGLE sensitivity (900)

Runner `papers/shadow-education-contest/code/run_new_generation.py` (sha `a84132ae…`), PID 24480, 8 workers, per-seed
atomic checkpoints. **Result:** see `PAPER_B_NEWGEN.md` / `results/audit/newgen/paperB_newgen_tables.csv` after
completion. Pre-stated primary contrast CF4a (spend index < 80 AND elite-Q5 below Baseline in both jurisdictions);
secondary CF4b/CF1b/CF3b; all arms × 4 headline outcomes reported; seed/MC uncertainty (100 seeds) vs
calibrated-parameter uncertainty (**zero by construction** — frozen parameters) stated separately.

## 3. Paper A — five intended computations (new generation)

| # | computation | status | artefact |
|---|---|---|---|
| a1 | E8 empirical event study, simple DiD, fresh hashed WDI | **DONE** — impact +12.322 pp (author +12.44); post +2.54 vs +25.26 (estimator-dependent) | `E8_BULGE_NEWGEN.md`, `results/audit/newgen/e8_bulge_fresh_wdi_2026-11-25.json` |
| a2 | E8 CS-style group-time ATT, fresh WDI | **DONE — REPLICATES** impact +12.322, post **+25.083** (author +25.26), Fisher p .0044/.0040, bootstrap CI impact [4.48, 22.64] | `CS_ESTIMATOR_NEWGEN.md`, `results/audit/newgen/cs_estimator_fresh_wdi_2026-11-25.json` |
| b | delayed secondary-bulge t* (fresh WDI) | **DONE** — ATT −0.956 pp, post +0.30, Fisher p .251/.384 → no detectable jump (consistent with HONEST_NULL) | `results/audit/newgen/e8_bulge_fresh_wdi_2026-11-25.json` |
| c | gate-architecture ≥5,000 runs | runner committed (`run_gate_architecture.py`, 5,120 runs); **launch after Paper B full**; fee-arm caveat from the mid-run fee-event finding | pending |
| d | multi-seed Jacobian (≥5 seeds/column, ≥3 starts) | running, PID 27382, cap-1 sequential; slow under Paper B contention (ETA may be ~20:40) | pending |
| e | forecast with held-out | **BLOCKED** — engine calendar fee change logged but not propagated to attendance (engine-core repro); no numbers cited (A-37) | `forecast_holdout*.py` |

## 4. Evidence labels (mandatory)

AUTHOR-REPORTED baseline · REPRODUCED EMPIRICAL ANALYSIS (fresh WDI) · NEW GENERATION — REPRODUCED SIMULATION
(repaired engine, frozen spec) · QUARANTINED (GPU/ABC pre-repair). Never "VALIDATED"; never "reproduces Gemini".
