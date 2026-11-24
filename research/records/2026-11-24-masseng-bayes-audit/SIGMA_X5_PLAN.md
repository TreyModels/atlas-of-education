# PLAN — Bayesian-audit addendum: σ-sensitivity + X5 synthetic recovery (task-29)

**Committed BEFORE the new code and before any run.** Additive to
`research/masseng-bayes-audit-2026-11-24` @ `1e406fb` (branch ancestry caveat already in AUDIT.md;
no rewrite). The originals — `run_screen.py`, the two 4,096-draw screens and all audit results — are
**not modified**. All compute on region-42; fresh output directories only; no secrets.

**Context.** The audited screens are conditional importance weights, not posteriors (AUDIT.md):
main ESS 88.75/4096 (2.17 %), expanded 20.64/4096 (0.50 %, max weight 10.63 %); N=1,024 Monte
Carlo probes give ESS fractions 1.74–1.90 %; the screen is prior-dominated and worse than
persistence on every holdout series. Two items were explicitly PENDING: (1) σ-sensitivity of the
three pseudo-likelihood scales; (2) synthetic recovery (X5). These are the decisive usability
tests.

## 1. σ-sensitivity (bounded copy, original untouched)

- `run_screen_sigma.py` is a *copy* of `run_screen.py` with one addition: `--sigma <multiplier>`,
  applied to all three declared likelihood scales (primary 4 pp, secondary 4 pp, tertiary 5 pp).
  Everything else (priors, R1 baseline file, target construction, weighting, holdout scoring,
  non-overwriting outputs) is unchanged; the original file is not edited.
- **Declared grid:** σ multiplier ∈ {0.5, 1.0, 2.0}; N = 1,024 draws; seed 20261125 (same as the
  main 4,096 screen); prior `main`; workers = 32. New output dirs only.
- **Reported per run:** ESS, ESS fraction, max weight share, weighted parameter means/q05/q95,
  per-series and pooled holdout RMSE vs persistence. **No "best σ" is selected**: the grid is a
  sensitivity display; and because the holdout years were previously inspected, none of the RMSEs
  is a blind benchmark.

## 2. X5 — synthetic parameter recovery (decisive usability test)

**Generator.** Use the same v5 R1 model and fixed nuisance block as the audited screen
(`model/outputs/PHL/v5/fit_R1.json`, all non-varied parameters fixed). For each known setting of
`(b_h, b_p, b_r, lam)`, run `Model5(Country("PHL"), p, spec="R1")` to get the model's GER series,
then form a synthetic observed training block 1971–1995 and holdout 1996–2024 by adding
**Gaussian observation noise with the screen's own declared scales (σ = 4/4/5 pp)**, using a
declared generation seed. This makes the synthetic data correctly specified for the screen's
pseudo-likelihood, so recovery is a fair test.

**Declared known settings (6, spanning the main prior):**
`(0.5, 2.0, 2.0, 1.0)`, `(3.0, 5.0, 5.0, 4.0)`, `(6.0, 8.0, 10.0, 6.0)`, `(-1.0, 1.0, 0.0, 0.5)`,
`(7.0, 9.0, 11.0, 7.0)`, `(1.0, 4.0, 7.0, 3.0)`. **2 generation seeds** each
(20261201, 20261202) = 12 synthetic datasets. Each is screened with the **main prior**, the
**same prior draws** (N = 256, screen seed 20261125) for paired comparability, workers = 32; the
screen-on-synthetic path is `run_x5_recovery.py`.

**Reported per dataset:** truth; weighted posterior mean/q05/q95 of each parameter; absolute
recovery error (and error as a fraction of the prior range); **coverage** = truth inside the
weighted 90 % interval; **confusion** = nearest declared setting to the recovered weighted-mean
vector (prior-range-normalised Euclidean); ESS, ESS fraction, max weight share; synthetic-holdout
RMSE (model vs persistence on the synthetic test block).

**Pre-declared usability criteria (fixed now, before running).** "Screens recover when the
generating model is true" requires **all** of:
(a) median ESS fraction across the 12 synthetic screens **≥ 2 %** of draws;
(b) truth covered by the weighted 90 % interval in **≥ 60 %** of parameter×dataset cases;
(c) weighted-mean absolute error **≤ 15 % of the prior range** in **≥ 60 %** of cases;
(d) nearest-setting confusion diagonal **≥ 60 %** (the recovered vector is closest to its own
generating setting).
**Decisive verdicts:**
- If (a) fails, or median ESS fraction stays below 2 % and max weight share exceeds 10 % even
  when the generating model is true → state plainly **"screens unusable"** (under-resolved
  regardless of correctness of the real data).
- If (a)–(d) hold → state **"recovery works under the true model"**, and state what that does
  **not** license: it does not make the real-data screens a calibrated posterior, does not validate
  the pseudo-likelihood scales, does not fix prior sensitivity, and does not provide real-data
  posterior/mechanism claims.
- Any mixed outcome is reported exactly, with the failing criteria named; no post-hoc criterion
  changes.

## 3. Deliverables and preservation

- `run_screen_sigma.py` (copy), `run_x5_recovery.py` (new), σ-grid and X5 results (new dirs/files),
  a short addendum section appended to `AUDIT.md`, and this plan; all committed and pushed to
  `research/masseng-bayes-audit-2026-11-24` (additive commit on top of `1e406fb`).
- Exact commands, start/end times, code hashes, worker counts, logs and seed-level outputs are
  preserved; existing results/logs are never overwritten.
- Labels: conditional importance weights, not posteriors; no causal claims; no E1 comparison.
