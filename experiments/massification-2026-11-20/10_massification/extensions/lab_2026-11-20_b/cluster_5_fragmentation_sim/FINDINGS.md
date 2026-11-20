# Cluster 5 — Geographic Fragmentation (SIMULATED) — FINDINGS

**STATUS: SIMULATED.** This cluster is a toy simulation with **stipulated parameters** only. Nothing is
calibrated to data. **Not evidence.** No historical test was performed and no observed data was read.
No claim is made about any real-world direction of effect. A "SIMULATED-THRESHOLD-MET" verdict would
mean only that the stipulated rules generate the predeclared pattern **within the simulation**.

## Structural note on the stipulated demand path (reported, not a threshold change)

The stipulated recursion d_{t+1} = d_t * r * (1 - d_t/dmax) with **r = 0.08 (< 1)** is contractive:
starting at d_0 = 0.10, d_t decays monotonically toward 0 and remains **below 0.50 at every t = 0..79**.
Consequently no ceiling can ever be crossed under the frozen parameters: **every cell in every
experiment is fully right-censored (100% >80)**, and median crossing years are undefined
(reported as `nan` in the CSVs; **not imputed**, per the never-impute rule). Thresholds were not changed;
verdicts follow mechanically from the frozen thresholds applied to undefined/absent effects.

## X13 — Does splitting delay the ceiling crossing?

All K in {1,2,4,8,16,32}: pct_censored = 100.0, n_seeds = 200; median/q25/q75 all `nan` (no crossings).
Delta = median(K=32) − median(K=1) = `nan` (undefined, not imputed).
**Verdict: SIMULATED-THRESHOLD-MISSED** (Delta is not ≥ 1 year; it is undefined).

## X14 — Does splitting smooth the approach?

No ceiling binds below the decaying demand path, so aggregate participation equals d_t in every cell;
median volatility = 0.0103840502383539 at every K (IQR degenerate: q25 = q75 = 0.0103840502383539),
with pct_censored = 100.0, n_seeds = 200 per K.
V = median volatility(K=1) / median volatility(K=32) = **1.0000** (bootstrap 95% CI 1.0000–1.0000, SE 0.0000).
**Verdict: SIMULATED-THRESHOLD-MISSED** (V = 1.0000 < 1.1).

## X15 — Heterogeneity dose (K = 8, binding ceil_k = 0.40)

All f in {0.0, 0.25, 0.50, 0.75, 1.0}: pct_censored = 100.0, n_seeds = 200; median/q25/q75 all `nan`
(the stipulated 0.40 ceiling never binds below the demand path, which starts at 0.10 and decays).
Spearman rho(crossing year, f) = `nan` (all cells all-censored; excluded, not imputed).
Delay f=0→f=1.0 = `nan`; delay(f=0→0.5) = `nan`; delay(f=0.5→1.0) = `nan`; the comparison
f=0→0.5 vs f=0.5→1.0 is **undefined** (first_half_bigger = False by default, not an observed ordering).
**Verdict: SIMULATED-THRESHOLD-MISSED** (rho is not ≥ 0.90; it is undefined).

## Determinism

Two consecutive runs produced byte-identical results CSVs (fixed seeds, PCG64):
see `hashes_run1.txt` / `hashes_run2.txt` (identical SHA-256 sets), and `RUN_MANIFEST.json` for the
RNG call pattern, code SHA-256, Python 3.11.17 / NumPy 2.4.6.

---

# AMENDMENT B1 — POST-HOC DISCLOSED (Lead predeclaration defect), thresholds unchanged

**Status: SIMULATED — stipulated toy, not evidence; POST-HOC, not predeclared.** The predeclared verdicts above
**stand as the formal predeclared result** and are not replaced. Amendment B1 exists because the frozen demand
recursion `d_{t+1}=d_t·r·(1−d_t/dmax)` with `r=0.08<1` is **contractive** — a defect in the Lead's predeclaration,
not in the worker's execution. Amendment B1 keeps **every frozen threshold, the K grid, the f grid, the 200-seed
cells and the estimator identical** and changes **only** the demand rule to a genuinely growing logistic form
`d_{t+1}=d_t·(1+g·(1−d_t/dmax))`, `g=0.08` (same numerical `r`, corrected sign). Rule before/after is recorded in
`code/amendment_b1.py` and `RUN_MANIFEST.json`. Outputs are under `results/AMENDMENT_B1/` and
`CLUSTER_RESULTS_AMENDMENT_B1.csv` (rows carry `run_tag=amendment_B1`).

**AMENDMENT-B1 RESULTS (all `SIMULATED-THRESHOLD-*`, no observed data):**

| exp | estimand | estimate | 95% CI | verdict (same frozen thresholds) |
|---|---|---|---|---|
| X13 | Δ = median crossing year K=32 − K=1 | **+1.00 y** | [0.00, 1.00] | **PARTIAL** (1 ≤ Δ < 3) |
| X14 | V = median volatility K=1 / K=32 | **1.231** | [1.201, 1.251] | **PARTIAL** (1.1 ≤ V < 1.5) |
| X15 | Spearman ρ(crossing year, f) | **1.000** (finite cells f = 0, 0.25, 0.50, 0.75) | — | **PARTIAL** (ρ ≥ 0.90 but delay f=0→1.0 undefined: f=1.0 cell is 100% censored) |

**Exploratory secondary read (NO threshold, reported because it is the largest effect):** the share of seeds that
ever cross rises from **77.0% at K=1 to 100.0% at K=8/16/32**, i.e. fragmentation in this toy moves the
**extensive margin** (probability of universalizing at all) far more than the **timing** (+1 year) or the
smoothness (V = 1.23). Median crossing years in B1: K=1 28, K=2 28, K=4 28, K=8 28, K=16 28, K=32 29 (IQR 28–29).
Binding-market dose delays the median crossing monotonically across the finite cells (f=0: 29 y; 0.25: 31 y;
0.50: 35 y; 0.75: 43 y; 1.0: >80, 100% censored).

**Reading guard:** none of this is evidence about any real system. It says only that *in this stipulated toy* a
system split into more markets crosses at nearly the same time but is **more likely to cross at all**; whether that
is a "delay" or a "smoothing" phenomenon is parameter-dependent and was not predeclared.

