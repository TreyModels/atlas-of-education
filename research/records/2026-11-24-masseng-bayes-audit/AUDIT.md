# MASSENG Bayesian importance screens — audit record (24 Nov 2026)

**Branch:** `research/masseng-bayes-audit-2026-11-24` (additive; Codex's branch untouched). **SIMULATION / conditional importance weights — NOT calibrated posteriors.** No causal claims; no E1 comparison.

## Runs audited (region-42, PIDs preserved)
- main: `run_screen.py --n-draws 4096 --seed 20261125 --workers 24 --prior main --out server_main_4096` (PIDs 18115/18116, 24 workers; wall ≈11 min)
- expanded: `--seed 20261126 --prior expanded --out server_expanded_4096` (PIDs 18162/18163, 24 workers; wall ≈11 min)
- MC: N=1,024, prior main, seeds 20261127 / 20261128 (smaller-N stability probe, not a replication)
- env: `PYTHONPATH=/root/work/masseng-codex-deps`, OPENBLAS/OMP/MKL_NUM_THREADS=1, `/root/miniconda3/bin/python`

## Code hashes (live server copies)
- `run_screen.py` **48dec650d5d77a54a8cc99840e3e27bc3c0dd65961695e29f5e74b35ce7fcc52**
- `model/masseng/engine5.py` **e01bd54383a7215503c3caff50212c5fcf16312aca9531e10ad810c7a3a5c17c**
- `calibrate5.py` 074657dde0a7afac9b94d706f03e1fff8a3b29731d37c329cd917a66c99dabca
- `engine.py` 9c8ccb6a74c7a3074f2b3858de071b445bbbdac861163c24c35e49853759a07c
- `data.py` 34f47a17401430d69493f38bb531dec9622f6a73c7d9a25a6c837d921d22cf01
- expanded log sha256 **49528337fb14c91f47099489c2c069a938c43de174a865e525ef32765a460bd0**

## ESS / weight diagnostics
| screen | N | ESS | ESS fraction | max weight share | non-finite | zero/neg |
|---|---|---|---|---|---|---|
| main | 4,096 | **88.75** | 2.17 % | 0.0227 | 0 | 0/0 |
| expanded | 4,096 | **20.64** | 0.50 % | **0.1063** | 0 | 0/0 |
| MC 20261127 | 1,024 | 19.48 | 1.90 % | 0.0948 | — | — |
| MC 20261128 | 1,024 | 17.83 | 1.74 % | 0.0986 | — | — |

The 46 logistic-overflow warnings (`engine5.py:63`) did **not** produce Inf/NaN weights — all 4,096 finite positive; failure mode is **weight concentration**, not numerical corruption.

## Holdout benchmark (retrospective, previously inspected — not blind)
| screen | per-series model RMSE (primary/secondary/tertiary) | persistence | pooled model | pooled persistence |
|---|---|---|---|---|
| main | 7.231 / 10.569 / 6.873 | 4.737 / 7.793 / 6.930 | 8.225 | 6.487 |
| expanded | 7.030 / 7.593 / 4.509 | 4.737 / 7.793 / 6.930 | 6.377 | 6.487 |
| MC 20261127 | — | — | 10.02 | 6.487 |
| MC 20261128 | — | — | 10.44 | 6.487 |

MC noise (10.0–10.4 at N=1,024 vs 8.2 at N=4,096) exceeds any apparent edge over persistence; main is worse than persistence on every series.

## Prior sensitivity (matched N=4,096)
Posterior means: main `b_h 3.02, b_p 5.03, b_r 5.13, lam 3.99`; expanded `b_h 3.02, b_p 2.99, b_r 6.06, lam 2.92`. Changing only the prior bounds moves means by ~30–60 % of their own scale while ESS collapses 88.7 → 20.6 and max weight share rises 2.27 % → 10.63 %. **Prior-dominated, not data-dominated.**

## Limitations (as the screen's own summary states)
No causal interpretation; deterministic model/targets conditional on inputs; weights reflect a chosen pseudo-likelihood (equal series weights, σ = 4/4/5 pp), not a validated observation model; R1 baseline fit reuses data beyond the GER training block; holdout years previously inspected; persistence is not a blind benchmark; no adaptive resampling/MCMC.

## σ-sensitivity and X5 synthetic recovery — PENDING
Not run at the time of this record: (a) a `run_screen_sigma.py` copy with a three-scale `--sigma` flag and a ×0.5/×1/×2 grid at N=1,024; (b) an X5 generator (known `b_h,b_p,b_r,lam` → synthetic GER) + screen-on-synthetic path with recovery/coverage/confusion. **No recovery verdict is claimed.** These are the next bounded items; the record will be amended.

## Compute cost
Two 4,096-draw screens × 24 workers ≈ 11 min each (≈22 core-minutes at 48 workers); two 1,024-draw MC probes ≈ 3 min each. Box: 96 cores, RTX 2080 Ti (GPU unused — no CuPy backend/equivalence for this model).


---

# ADDENDUM — σ-sensitivity + X5 synthetic recovery (task-29, 24 Nov 2026)

**Branch additive on `1e406fb`; original `run_screen.py`, the two 4,096-draw screens and all prior
audit results are untouched. SIMULATION / conditional importance weights — NOT posteriors. No causal
claims; no E1 comparison. New code: `run_screen_sigma.py` (copy of `run_screen.py` + `--sigma`),
`run_x5_recovery.py`; plan committed before runs (`SIGMA_X5_PLAN.md`).**

## Execution (region-42; exact logs committed)

- Command wrapper: `nohup bash run_addendum.sh > addendum_run.log 2>&1` in
  `/root/work/masseng-staging-codex-20261124/masseng-v6/experiments/codex_bayes/`; env
  `PYTHONPATH=/root/work/masseng-codex-deps OPENBLAS_NUM_THREADS=1 OMP_NUM_THREADS=1 MKL_NUM_THREADS=1`;
  `/root/miniconda3/bin/python` 3.10.8, NumPy 2.2.6; 32 workers.
- σ grid: σ multipliers {0.5, 1.0, 2.0} × N=1,024 draws, seed 20261125, prior `main`; new output dirs
  `sigma_main_x<mult>_1024/`. Each run finished in ~1 min; new files only.
- X5: 6 declared settings × 2 generation seeds × N=256 main-prior draws (identical prior draws across
  datasets; screen seed 20261125), 32 workers; **wall 229.18 s**; `results_x5_recovery.json`.
- Smoke tests first: `run_screen_sigma.py --n-draws 8 --workers 2 --sigma 1.0` (parsed/ran) and
  `run_x5_recovery.py --n-draws 8 --truth 3,5,5,4` (parsed/ran). No failures in the full runs.
- Code hashes: `run_screen_sigma.py` **bd8a6c1a…**; `run_x5_recovery.py` **dc284eac…**;
  `run_screen.py` **48dec650…**; `model/masseng/engine5.py` **e01bd543…**; `model/masseng/data.py`
  **34f47a17…**. Result hashes: `sigma_grid/sigma_x*_1024_summary.json` (see `MANIFEST` update) and
  `results_x5_recovery.json` **12046f3d…**.

## 1. σ-sensitivity of the three pseudo-likelihood scales (N=1,024, same seed/prior)

| σ multiplier | ESS / 1,024 | ESS % | max weight | pooled holdout RMSE model | persistence | per-series model / persistence (prim., sec., tert.) | weighted means b_h / b_p / b_r / lam |
|---|---|---|---|---|---|---|---|
| ×0.5 | **7.47** | 0.73 % | **18.70 %** | 9.203 | 6.600 | 7.53/4.74, 12.34/7.79, 7.02/6.93 | 1.04 / 6.70 / 4.07 / 1.70 |
| ×1.0 | **23.78** | 2.32 % | 7.15 % | 7.442 | 6.600 | 7.17/4.74, 9.80/7.79, 4.65/6.93 | 1.03 / 6.09 / 4.86 / 1.49 |
| ×2.0 | **74.87** | 7.31 % | 2.34 % | 6.553 | 6.600 | 6.78/4.74, 7.16/7.79, 5.69/6.93 | 1.40 / 5.38 / 4.99 / 1.78 |

- ESS rises monotonically with the assumed scale (7.5 → 23.8 → 74.9), max single-draw weight falls
  (18.7 % → 2.3 %), and **the weighted parameter means move materially with σ** (b_h +35 %, b_p
  −20 %, b_r +23 %, lam +19 % from ×0.5 to ×2). The "posterior" summary is therefore set largely by
  the arbitrary working scale, not by the data.
- The pooled holdout RMSE only edges below persistence at σ×2 (6.553 vs 6.600) and is worse at ×0.5/×1;
  per-series, primary and secondary remain worse than persistence at every σ. The holdout is previously
  inspected and is not a blind benchmark. **No σ is selected as "best"**; the grid is a sensitivity
  display, and it shows the inference is scale/prior dominated.

## 2. X5 — synthetic parameter recovery (decisive usability test)

Generator: same v5 R1 model + same fixed nuisance block as the screen; synthetic GER training
1971–1995 and holdout 1996–2024 with Gaussian noise at the screen's own 4/4/5 pp scales; screenshot
via the unchanged `run_screen` likelihood. 6 declared truth settings × 2 generation seeds = 12
synthetic datasets, N=256 main-prior draws each.

**Aggregate (pre-declared criteria):**

| statistic | value | criterion | met? |
|---|---|---|---|
| median ESS fraction | **12.79 %** | ≥ 2 % | **YES** |
| min ESS fraction | 1.37 % | — | — |
| max single-draw weight | 37.46 % | — | — |
| truth coverage by weighted 90 % interval | **91.67 %** | ≥ 60 % | **YES** |
| median absolute error | 12.76 % of prior range | — | — |
| cases with error ≤15 % of prior range | **56.25 %** | ≥ 60 % | **NO** |
| confusion diagonal (recovered vector nearest its own setting) | **50.0 %** | ≥ 60 % | **NO** |
| synthetic-holdout RMSE, median model vs persistence | 4.71 vs 9.77 | — | (model true by construction) |

**Per-setting pattern (both generation seeds agree):** S1 `(3,5,5,4)` and S2 `(6,8,10,6)` recover well
(ESS 18–31 %, coverage 100 %, correct nearest setting); S0 `(0.5,2,2,1)` and S3 `(-1,1,0,0.5)` show
low ESS (1.4–4.3 %), max weight up to 37 %, and S3 is confused with S1/S0; **S4 `(7,9,11,7)` is
confused with S2** (identical ESS 31.1 % and holdout RMSE to two decimals — the two settings are
nearly non-identifiable under the R1 GER likelihood); S5 `(1,4,7,3)` recovers coverage but maps to S1.
So some parameter settings are recoverable when the generating model is true, while others are not
identified by the GER likelihood at this draw count.

**Plain usability verdict: MIXED → the real-data screens are NOT usable as posterior-style
inference.** The pre-declared "screens unusable" trigger (degenerate ESS under a true model) is not
met — under the true model ESS improves about six-fold vs the real-data N=1,024 screens (median
12.8 % vs 1.7–2.3 %) and coverage is high — so the real-data weight degeneracy is largely
**model-misspecification/prior conflict, not merely too few draws**. But recovery is **not**
established by the pre-declared criteria (error criterion missed at 56 % vs 60 %; confusion diagonal
50 % vs 60 %; two truth settings confused, one pair effectively non-identifiable), so the screens
cannot support parameter or mechanism claims on real data at these draw counts.

**What this does and does not license.** It licenses the narrow statement that the importance
machinery can concentrate weights and achieve interval coverage when the generating model is exactly
the screen's model, for *some* settings. It does **not** license any real-data posterior, mechanism,
or causal claim; it does not validate the arbitrary pseudo-likelihood scales (see §1: σ drives ESS
and parameter means); it does not resolve the prior sensitivity documented above; and it does not
establish that the v5 R1 GER likelihood identifies the four mechanism parameters in general.

**Shutdown advice:** all addendum runs completed; no jobs of ours remain on region-42; every output,
log and result is pulled and committed. Nothing server-only remains for this audit; stopping (关机,
not 释放) region-42 is safe once Trey/Codex confirm no further Bayesian work is needed.
