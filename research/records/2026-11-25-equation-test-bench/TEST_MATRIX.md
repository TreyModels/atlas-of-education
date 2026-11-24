# TEST MATRIX — equation test bench (cached-data attempt, CORRECTED 25 Nov 2026)

**Branch** `research/equation-test-bench-2026-11-25`. **No causal claims; no invented targets.** This table now
reflects the **fixed** runner (`test_bench2.py`, rewritten after the line audit); the first version's failures are
recorded at the bottom and in git history. Data are committed under `data/` with `PROVENANCE.json` +
`MANIFEST.sha256` (all four entries verify; `long_run_panel.csv` sha256 `cd30d7ea…`, 42,959 rows, 197 countries,
schooling spacing **5 years**). No live World Bank pulls.

| family | tier | data | test attempted | result | verdict |
|---|---|---|---|---|---|
| F1 household demand/affordability | C | none | — | no public micro affordability/fees in cache | **UNTESTABLE** |
| F2 state supply/finance | C | none | — | no PTR/teacher/private/finance panel in cached inputs | **UNTESTABLE** |
| F3 learning production | C | none | — | no learning panels in cache | **UNTESTABLE** |
| F4 stage gates | C | none | — | no exam/admission data | **UNTESTABLE** |
| F5 returns/credentials | C | none | — | no wage/returns panel in cache | **UNTESTABLE** |
| F6 structural change/growth | C | x4 (wide cross-section only) | not run | x4 is a wide cross-section, no lagged growth panel with controls | **UNTESTABLE** |
| F7 inequality/mobility | C | none | — | no Gini/SWIID in cache | **UNTESTABLE** |
| F8 tutoring/shadow | C | bray targets only | not run | literature targets, not a panel | **UNTESTABLE** |
| F9 fertility/health (lagged OOS) | A | `data/long_run_panel.csv`, lag 5 | Δschooling(y−5→y) → ΔTFR, urban/GDP controls, 5-fold by country, train ≤2000 / test >2000, cluster SE, 8-variant spec curve | n = **1,495** (135 countries), 5/5 folds; model RMSE **0.2381** vs persistence **0.2855** vs null **0.2311**; folds beating both **2/5**; β = **−0.2531** (SE 0.0322), CI excludes 0, spec sign share 1.00 | **REJECTED (does not beat both benchmarks)** |
| F10 measurement/attainment | A | `data/long_run_panel.csv` | observed TFR vs reconstructed effective fertility | n = 14,578; median \|Δ\| **0.284**, mean Δ 0.703 | **SUPPORTED_CONSTRUCT_DIVERGENCE** (construct check only) |
| Q1 zero-signal control | — | permuted outcomes within country | 20 permutations, same spec | model beat both benchmarks in **3/20 = 0.15** (< 0.5 = pass) | **PASS** |
| E8 fee-abolition gate | B | fee dates on `research/e6e8-sequencing-2026-11-25`, `research/paper-massification-2026-11-25` | not run (runner supports `--e8-dir` + SHA-256) | data located but not on this branch | **UNTESTABLE on this branch** |
| E8 PHL K–12 gate | B | PHL 2013 K–12 series | not run | series not located in searched branches | **UNTESTABLE** |
| shared-code ablation | — | — | — | no equation/eduengine model code in this branch | **UNTESTABLE (this branch)** |
| multiverse structural swap | — | — | — | no equation/eduengine model code in this branch | **UNTESTABLE (this branch)** |

## Failures in the FIRST version (kept as record; both fixed)

1. **F9 join:** v1 used `lag=1`, but `mean_years_schooling` is only populated every 5 years, so the join asked
   for schooling in `y−1` and got **n = 0** — a verdict computed from nothing. Confirmed by counting: lag=1 →
   0 usable rows, lag=5 → 1,560 rows (1,495 with controls). Fixed: the lag is derived from the schooling
   spacing (`native_lag`), an empty/insufficient join returns NOT IDENTIFIED with a reason, and the old failure
   is pinned by a guard test.
2. **Q1 control:** `np.linalg.inv(X.T @ X)` raised `LinAlgError: Singular matrix` on a collinear control inside a
   fold. Fixed: SVD rank guard drops collinear controls (never intercept/schooling), records
   `dropped_controls`, and reports `not identifiable` if the design is still deficient. Q1 now runs and passes.

## What is required before more verdicts

- E8 fee-abolition gate: copy the fee-date files with `--e8-dir` (hashes recorded in `results2.json`).
- PHL 2013 K–12 series: find/transcribe it, or leave UNTESTABLE.
- (d) shared-code ablation and (e) multiverse structural swap need the equation model code wired in.

## Hash / command record

- Runner: `test_bench2.py` (rewritten 25 Nov; `results2.json` records the source sha256, `long_run_panel.csv`
  sha256 `cd30d7ea…`, numpy 1.24.3, python 3.10.2, derived lag 5).
- Local run (Mac, numpy only, ~1 s): `python3 test_bench2.py --out results2.json`; guards
  `python3 test_bench_guards.py` → ALL PASS. No server compute for the corrected run (the box was powered off
  mid-session; the corrected run needs none).
- No live network pulls. `results2.json` committed next to this file.
