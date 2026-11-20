# ERROR LOG — Loop 2 (`05b_experiments/loop2/`)

## Run-level
- Final calibrated run: 3 countries × 10 regimes × 5 seeds = **150 trajectories, 0 failures**.
- Final uncalibrated sensitivity run: **150 trajectories, 0 failures**.
- No per-run timeouts (the module is numpy-only, no multiprocessing; completed in seconds).

## Defects found and fixed before any result was recorded
1. **Deterministic first pass (major).** The first execution drew no random numbers: all five "seeds"
   were identical and seed sd was exactly 0, making every 2sd test vacuous. Fix: declared stochastic
   terms were added — multiplicative formal-demand shocks (lognormal sd 0.06) on Vc/Vr and household
   decision taste noise (logit sd 0.15) — and the module re-run. The first-pass output was deleted and
   is not reported.
2. **`UnboundLocalError` on `qc_ref` in the frozen-returns arm (R5).** 15 of 135 first-pass trajectories
   failed. Fixed by binding the reference beliefs in the enclosing function and declaring them
   `nonlocal`. The final run has 0 failures.
3. **Undefined `clip` in the wage calculation** (would have raised NameError); replaced with `np.clip`.
4. **Syntax error from an over-broad text patch** (unmatched parenthesis in `summarise`) fixed before
   execution.

## Interpretation issues / caveats (recorded, not hidden)
1. **KHM-like "education-led" classification is driven by a tiny effect.** The predeclared rule fires
   because Ed_dir = +0.0008 exceeds 2sd = 0.0001, but that is +0.08 percentage points of complex-job
   share — economically nil. Reported as `education-led by rule, but effect ≈0 → treat as weak/nil`,
   not as evidence.
2. **The price/entry block overshoots.** With endogenous entry, prices fall to the declared floor and
   provider counts grow 5–90×; with fixed supply prices hit the ceiling. Neither price level is
   credible economics yet — the entry-cost/capacity parameters need calibration against price moments
   (Council brief 004 says provider supply is the structural variable; this is the next fit).
3. **The single-moment shadow calibration is underdetermined.** Fitting the common household-demand
   intercept to HK 0.85 forces PH/KHM to ~0.88–0.89 take-up with no literature target to check. This is
   reported as non-identification of the cross-country shadow pattern, not as a fit.
4. **Frozen-economy arm is a first-order counterfactual.** R10 holds vacancies and beliefs at their t=0
   values; a fully consistent counterfactual would re-solve steady states. The residual attainment rise
   under R10 (+0.022–0.028 over 40y) should be read as an upper bound on the non-economy channel.
5. **Positional channel null.** Take-up does not respond detectably to gate competition in this
   specification; this is a null result for the module, not evidence against the paper's positional
   claim (which needs a separate, better-identified test).
6. **Targets are observed cells only.** GMR observed panel and national headline figures; no imputed
   cell is cited as observed. Where no target exists (PH/KHM tutoring; HK completion) the table says so.
7. **Council tests 4–5 not run.** Recovery with truths outside the candidate set / forced-identification
   rate, and the 1980–2010 fit / 2011–2024 held-out test, were specified (Amendment L2-4/L2-5) but not
   executed in this timebox. No claim from them is made.
