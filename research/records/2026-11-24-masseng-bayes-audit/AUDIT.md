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
