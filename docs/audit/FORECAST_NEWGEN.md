# Paper A (e) — NEW-GENERATION fee-abolition forecast with genuine held-out horizons (engine pin 846c9e0)

**Label: NEW GENERATION — REPRODUCED SIMULATION forecast.** Empirical target = **REPRODUCED EMPIRICAL ANALYSIS**
(fresh-WDI CS-style event path). The manuscript's 78.6–80.5 % RMSE-reduction claim stays **AUTHOR-REPORTED baseline**
and is not re-derived as a reproduction.
Artefact `results/audit/newgen/forecast_holdout_fixed_846c9e0.json`; engine pin `846c9e0` (core `e111397b…`); runner
`forecast_holdout_v2.py` v4; fixed-engine event key `year_t=T0` with **`assert E.unfired_events == []`** in every arm;
40 matched seeds; held-out horizons e=+5,+6.

## Design (training-only calibration, declared fallback)

Repaired engine, declared NEW SSA-like world (N=300, T=24, entry_age=6, subsist=.60, borrow=0, y_median=.8, open
gates), fee_public fixed at the manuscript value **0.15**; abolition event (`year_t=T0`, fee_public → 0) vs
persistence; outcome = mean primary attendance across the 6 primary grades / cohort, change vs the pre-abolition year.
**Calibration:** attempted training-only bisection on the pre-abolition year only against the manuscript's 74.88 %
level anchor → **CALIBRATION_FAILED: the anchor is infeasible in this NEW world** (max pre-attendance 71.0 % at fee 0),
so the documented fallback is: manuscript fee 0.15, engine's own pre-abolition level as baseline, **no post-abolition
horizon used for any tuning**. Held-out e=+5,+6 are reported separately.

## Result

| horizon e | 0 | 1 | 2 | 3 | 4 | 5 | 6 |
|---|---|---|---|---|---|---|---|
| simulated abolition − persistence (pp) | +17.19 | +20.97 | +23.37 | +25.03 | +26.14 | +26.18 | +25.35 |
| empirical CS-style path (fresh WDI) | 12.32 | 23.66 | 25.79 | 21.88 | 24.94 | 28.45 | 25.78 |

* **Full-7 RMSE 2.764 / MAE 2.432** vs **persistence baseline RMSE 23.759 / MAE 23.260** → RMSE reduction **88.4 %**
  (author-reported baseline 78.6–80.5 %, different world/estimator — indicative comparison only).
* **Held-out e=+5,+6: RMSE 1.637 / MAE 1.350** vs persistence → the forecast beats carry-forward on the genuinely
  held-out horizons.
* The engine-core expectation (+17 pp at e=+1 → ≈+25 pp by e=+6) is confirmed; the earlier zero-effect artefact was
  the runner's simulation-index-vs-calendar-year bug (engine-core `846c9e0` fixed the silent no-op; this run asserts
  `unfired_events == []`).

## Caveats

* NEW world (declared, not a reconstruction of Gemini's parameters); level anchor infeasible → fallback declared; do not
  describe this as reproducing the author's calibration.
* Empirical target is our fresh-WDI CS-style path with its own declared deviations (equal weights, no DR covariates).
* 40 matched seeds; no parameter uncertainty (frozen); seed MC uncertainty is reported in the JSON stats.
* No causal claim beyond the author's design; the paper's RMSE number remains AUTHOR-REPORTED baseline.
