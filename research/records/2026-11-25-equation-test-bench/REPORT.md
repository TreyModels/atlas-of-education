# One-page report — equation test bench (cached-data attempt, corrected 25 Nov 2026)

**Outcome after the join/estimator fixes: one family is now REJECTED, one construct check is supported as a
construct check, the permutation control PASSES, and the rest remains UNTESTABLE for lack of cached data.**
No effect size or benchmark comparison is claimed beyond the OOS prediction comparison below.

> **Correction notice.** The first version of this report said F9 was "NOT IDENTIFIED because the lagged
> design returned n=0" and that Q1 "failed to run" with `LinAlgError: Singular matrix`. Both were
> implementation bugs, not data limits, and are now fixed (`DIAGNOSTICS_2026-11-25.md` had already flagged
> them): (a) the panel's schooling series is populated every 5 years, so `lag=1` produced an empty join —
> with the data's native lag the join has **n = 1,495**; (b) `np.linalg.inv(X.T @ X)` blew up on a collinear
> control — now an SVD rank guard drops collinear controls and records them.

## Result

| family | data | what was run | result | verdict |
|---|---|---|---|---|
| **F9 fertility/health** (lagged OOS) | `data/long_run_panel.csv` (sha256 `cd30d7ea…`, 42,959 rows, 197 countries, schooling spacing 5 y) | Δschooling(y−5→y) → ΔTFR, urban/GDP controls, 5-fold by country, train ≤2000 → test >2000, cluster SE; 8-variant spec curve | n = 1,495 (135 countries), 5/5 folds eligible. Model RMSE **0.2381** vs persistence **0.2855** vs training-mean null **0.2311**; folds beating both = **2/5**; β = **−0.2531** (SE 0.0322), CI excludes 0, spec sign share 1.00 | **REJECTED (does not beat both benchmarks)** — the lagged model beats persistence but not the training mean out of sample |
| **F10 measurement** | same panel | observed TFR vs reconstructed effective fertility | n = 14,578; median \|Δ\| = **0.284**, mean Δ = 0.703 | **SUPPORTED_CONSTRUCT_DIVERGENCE** — they are different constructs; this is not a validation of either |
| **Q1 zero-signal control** | permuted outcomes within country | 20 permutations of the observed outcome values, same spec | the model beat both benchmarks in **3/20 = 0.15** permuted runs (≤0.5 = pass) | **PASS** — no runaway false-positive selection |
| E8 fee-abolition gate | fee dates exist on `research/e6e8-sequencing-2026-11-25` and `research/paper-massification-2026-11-25` | not run (needs `--e8-dir` with SHA-256 provenance) | data located, not on this branch | **UNTESTABLE on this branch** (runner now supports it) |
| E8 PHL K–12 gate | PHL 2013 K–12 series | not run | series not located in the searched branches | **UNTESTABLE** |
| F1–F8, shared-code ablation, multiverse swap | — | — | no micro affordability/fees, no PTR/teacher/finance panel, no learning panel, no exam data, no wage panel, `x4` is a wide cross-section, no equation model code in this branch | **UNTESTABLE** |

## What this does and does not say

- F9 is a **descriptive out-of-sample prediction exercise on reconstructed/observed aggregate panels**. Its
  REJECTED verdict means: the lagged schooling→TFR specification does not beat a training-mean benchmark out
  of sample, even though its coefficient is stable and precisely estimated in-sample. It is **not** a causal
  test of schooling on fertility.
- F10 says only that observed TFR and reconstructed effective fertility diverge — as expected from their
  definitions. It is not evidence about skill or attainment.
- The permutation control passing means the benchmark comparison is not trivially won by a saturated search.

## Reproduction

```
python3 test_bench2.py --out results2.json        # from this directory; needs numpy only
python3 test_bench_guards.py                      # guard suite; ALL PASS
```
Data are committed under `data/` with `PROVENANCE.json` + `MANIFEST.sha256` (all four files verify). Lag is
derived from the panel (5 y), not assumed. `results2.json` carries script/source hashes, numpy/python
versions and the lag.

## Required next

Copy the E8 fee-date files in with `--e8-dir` (hashes recorded) and run the naive gate; find or transcribe the
PHL K–12 series (else it stays UNTESTABLE); wire the equation model code before the ablation and multiverse
swap can be tested.
