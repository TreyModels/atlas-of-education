# TEST MATRIX — equation test bench (cached-data attempt, 25 Nov 2026)

**Branch** `research/equation-test-bench-2026-11-25`. **No causal claims; no invented targets.** Status reflects the
**actual execution attempt** on committed cached inputs, including failures. Script hash deployed to region-42:
`b8d099ad4fdb0391ef779607d3b70e687d7a4b1a915cb71a94bc2475eaff70f5` (`test_bench2.py`; local == remote).
Data: `/root/work/testbench/data/` = `long_run_panel.csv` (Q2 `9a4f586`, sha256 `cd30d7ea…`),
`x4_panel.csv` (masseng-x2 `f592bae`, sha256 `01590120…`), `bray_targets.json` (literature targets,
sha256 `15ebc84e…`), manifest `MANIFEST.sha256`. **No live World Bank pulls.**

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
| F9 fertility/health (lagged OOS) | A | long_run_panel | lagged Δschooling→ΔTFR, LCO + time split, persistence/trend/null benchmarks, cluster SE, 12-variant spec curve | **estimator returned n=0** — panel join degenerate on cached columns (schooling/TFR/control vintages do not overlap under the lag+control requirement); no OOS metrics | **NOT IDENTIFIED** |
| F10 measurement/attainment | A | long_run_panel | observed TFR vs effective-fertility construct check | not reached (script aborted at F9/Q1 stage; see failure below) | **NOT IDENTIFIED** |
| Q1 zero-signal control | — | long_run_panel (permuted) | 40 permuted trials of the selection metric | **could not complete:** `numpy.linalg.LinAlgError: Singular matrix` in `ols()` when a folded control block was collinear (need `pinv`/rank guard) | **UNTESTABLE until fixed** |
| shared-code ablation | — | — | — | no equation/eduengine model code in this branch | **UNTESTABLE (this branch)** |
| multiverse structural swap | — | — | — | no equation/eduengine model code in this branch | **UNTESTABLE (this branch)** |

## Exact failures (from the verified remote copy)
1. **F9:** `build()` filters leave `n=0` — the lagged Δschooling→ΔTFR design with urban/GDP controls does not find
   overlapping rows in the cached `long_run_panel` (columns present: schooling, tfr_observed, effective_fertility,
   urban_share_pct, gdp_pc_maddison). No model fit was produced; verdict NOT IDENTIFIED (data/join), not REJECTED.
2. **Q1 control:** `numpy.linalg.LinAlgError: Singular matrix` at
   `test_bench2.py:41` `np.linalg.inv(X.T@X)` — a dropped/collinear control inside a fold; fix is `pinv` + rank check
   **before** any Q1 pass/fail can be reported.
3. Earlier network-dependent version killed (PID 10206) per instruction; no WB calls in this attempt.

## What is required before any SUPPORTED/REJECTED verdict
- Fix F9 join (inspect overlaps: which years/countries have all required columns; relax control requirement or use
  available controls only) and `pinv` rank guards; rerun Q1 permutation control and F9/F10.
- E8 fee-abolition panels and PHL 2013 series are **not in the cached inputs**, so the naive benchmark gate as
  specified (E8 +22–29 pp, PHL K–12) remains **UNTESTABLE** here — do not fabricate.
- (d) shared-code ablation and (e) multiverse structural swap need the equation model code; UNTESTABLE in this branch.

## Hash / command record
- script `b8d099ad…` (local == remote), run `timeout 300 /root/miniconda3/bin/python -u test_bench2.py` on region-42
  (`ssh -p 45973`, ≤8 workers; single process), log `/root/work/testbench/` — **aborted at the F9/Q1 stage**;
  `results2.json` not produced. No shutdown.
