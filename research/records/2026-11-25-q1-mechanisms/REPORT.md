# Q1 — Can genuinely different mechanisms fit the same aggregate history, and which measurements tell them apart?

**Bounded known-truth pilot plus GPU engine gate.** Branch `research/q1-mechanisms-2026-11-25`. Everything here is
synthetic: no historical data are fitted, and no real-world mechanism is claimed.
Pre-registration `PRE_REGISTRATION.md` was committed as the branch's first commit (`0f176a0`) before any run.
Sources under examination: the Codex handoff (branch `research/codex-handoff-run-2026-11-24`,
`LETTER_FOR_DEEPSEEK.md` and `SYNTHETIC.md`) and the Codex review (`REVIEW.md`, `findings.csv`).

## What was asked
1. Can three *genuinely different* mechanisms generate the same aggregate history?
2. Which independent measurements, if any, recover the true mechanism?
3. Where do they fail, and is the failure a property of the world (observational equivalence) or of the pilot?

## The three worlds (distinct kernels, fixed before runs)
All three generate the same observables: country-cohort mean schooling, mean births, income, a price shifter, a
wealth proxy and age at first birth, for 24 countries x 8 five-year cohorts.

- **W1 direct schooling.** S assigned by background; F falls with S (`F = FE - tau S + e`). Intervention: an
  exogenous schooling increase reduces births by tau. tau varies by strength (0.10, 0.25, 0.45).
- **W2 common-development selection.** A latent development level D drives both S and F; schooling has **zero**
  causal effect. Intervention: shifting S with D fixed changes no births. Calibrated so its F|S gradient matches
  W1's, i.e. the same conditional means.
- **W3 joint fertility-education choice.** A price shifter moves S and F jointly, with correlated residuals
  (rho = 0.5). Intervention: a price change moves both; the schooling-only response differs from W1's direct
  effect and from W2's null.

## Rivals, budgets, sample flow
Three rivals with **different kernels**, fitted to the *same* training block (16 countries, first 6 cohorts):
- **R1**: F ~ S + income + country and cohort FE (the direct kernel).
- **R2**: two-equation selection system, F ~ income + FE and S ~ income + FE; no S in the births equation.
- **R3**: bivariate (S, F) with price and price-squared regressors plus residual correlation, scored with a joint
  likelihood.
All are closed-form Gaussian MLE, so the search budget is *identical by construction* (no convergence failures,
no unequal optimiser calls): 40 replications per truth x strength cell; data-generation seeds and fitting-order
seeds are independent streams (`seed_dgp=20261125`, `seed_fit=777001`, both recorded in the script and JSON).
Held out before fitting: 8 countries and the last 2 cohorts of every country (preregistered split, seed fixed).

## Result 1 — a control the machinery failed, and why that matters
The pre-registered zero-signal control sets strength = 0, which makes the three worlds equivalent in their effect
content. A valid discriminator must then be at chance (~33 per cent). **It is not.**

| criterion | zero-signal recovery (strength 0, 40 reps) |
|---|---|
| raw held-out MSE | picks **R3 in 97 per cent** of W1 and W2 runs, 33 per cent for W3 |
| BIC-penalised held-out score | picks **R1 in 100 per cent** of every world |

Both criteria are degenerate, and in opposite directions: raw MSE rewards the most flexible kernel (R3 has two
extra regressors plus a correlation parameter), BIC rewards the most parsimonious (R1). Neither measures
mechanism. **Per the pre-registration this invalidates the ladder as a discrimination test**, and it is the
pilot's main result: a "model winner" from either criterion is an artefact of specification and complexity, not
evidence about the mechanism. That is exactly the failure the Codex letter warned about, reproduced in a fitted
(rather than oracle-supplied) setting.

## Result 2 — the recovery tables, reported as they came out
Because the criteria are invalid, the tables below are reported for completeness and are **not** evidence that any
world is identifiable.

Held-out MSE, share of 40 reps where the winner equals the truth:

| truth \ strength | R1 | R2 | R3 |
|---|---|---|---|
| W1 direct, 0.10 | 0.00 | 0.00 | 1.00 |
| W1 direct, 0.45 | 0.00 | 0.00 | 1.00 |
| W2 selection, 0.10 | 0.00 | 0.00 | 1.00 |
| W2 selection, 0.45 | 0.00 | 0.03 | 0.97 |
| W3 joint, 0.10 | 0.80 | 0.00 | 0.20 |
| W3 joint, 0.45 | 0.55 | 0.00 | 0.45 |

BIC-penalised: R1 wins 100 per cent in every cell. Implied-gradient recovery (the micro measurement's statistic)
is the only criterion with any structure: W3 is recovered by R3 in 42 / 62 / 62 per cent of reps at strengths
0.10 / 0.25 / 0.45, W2 is misattributed to R1 (65-68 per cent), and W1 is misattributed to R2 (45-55 per cent).
It separates W3 from the other two at moderate strength but does not identify W1 or W2.

## Result 3 — the observations and the world are not distinguishable here
Two of the three worlds (W1 and W2) generate **the same conditional distributions** of the observables (the
shared-mean construction from SYNTHETIC.md, now with fitting rather than oracle rates). The gradient criterion
sometimes separates them, but not reliably, and no criterion above separates them at weak strength. The honest
statement is the Codex one: **if the mechanisms imply identical distributions of the measured variables, more
observations of the same variables do not identify them; only different measurements or interventions can.**

## GPU engine gate (real engine, synthetic panel)
Box `ssh autodl3` (Tesla T4 16 GB, CUDA 11.8, 8-CPU cgroup). The calibration panel lived on the retired box2 and
is **not** on box3, so the gate uses a **synthetic 2-country panel** built from the engine's own parameter ranges:
this checks the API and the harness, not the published calibration, and it is labelled so throughout.
`cupy-cuda11x` 13.6.0 had to be installed and `CUDA_PATH=/usr/local/cuda-11.8` set (the pre-installed
cupy-cuda12x could not find `libnvrtc.so.12`); both are recorded as environment deviations.

| check | result |
|---|---|
| API: documented entry point `abm_dose.simulate` | returns the documented keys (`tfr, asfr1519, smam, m18, afb, coh, years`); first call 5.02 s including NVRTC compile |
| repeatability, same seed same layout | tfr max abs diff **8.9e-16**, smam **0.0**, asfr1519 **6.9e-17** — repeatable at floating-point noise |
| batch layout: nW=12 vs nW=6, same seed | tfr max abs diff **1.907** — a real change in the random streams, not floating-point noise; the documented caveat reproduces |
| layout pinned | **nW = 12**, seed 7; all numbers in this record use it and the pin is logged in `results/engine_check.json` |
| one small adaptation | 50,000 women, 1 parameter vector, 1 country: **2.99 s** (~16,700 women/s, overhead-dominated at this size). The CPU numpy reference at nW = 2,000 took **250.1 s** (~8 women/s): the reference is a slow pure-Python loop, so the ratio is a harness fact, not a performance claim about the published model |

Caveats to keep: the synthetic panel produces undefined (NaN) cells in the 1980-2010 target window, so the layout
comparison uses `nanmax` and the *levels* in this record are not meaningful — only the differences are. The
throughput here is **not** comparable to the earlier record's 3.3 million women/s, which was measured on batched
launches of 210,000 women per run; a single 50k run is dominated by fixed overhead.

## What this pilot does and does not establish
**Establishes:** (i) three distinct kernels were built and generated data; (ii) with the same aggregate training
information, two standard selection criteria are dominated by model complexity and fail a pre-registered
zero-signal control, so a model winner from them is not evidence; (iii) a micro-gradient measurement has partial
and asymmetric discriminating power; (iv) the GPU engine's API, same-seed repeatability, batch-layout sensitivity
and layout pinning are all verified on box3 with a synthetic panel.
**Does not establish:** any real-world mechanism; any causal claim; that the synthetic panel reproduces the
published calibration; any claim of observational equivalence among the three worlds beyond the shared-mean
construction. **No model winner is an established cause**, and the pilot is synthetic throughout.

## Failures and deviations preserved
1. Raw-MSE and BIC criteria fail the zero-signal control (the pilot's central negative result). No post-hoc
   criterion was substituted and called success; the BIC variant was added *after* seeing the MSE control fail,
   and it also failed, which is reported as such.
2. The gradient statistic's mapping from each rival to "dF/dS" is an approximation (R2 and R3 are read through
   their income and price coefficients); its misattributions are reported, not hidden.
3. The engine gate ran on a synthetic panel because the calibration panel is not on box3; NaN targets appear.
4. `cupy-cuda12x` was pre-installed but unusable (no CUDA 12 NVRTC); `cupy-cuda11x` was installed and
   `CUDA_PATH` set. An SSH session dropped once after the engine results were written; no results were lost.
5. No large run was attempted: 40 reps x 3 strengths x 3 worlds plus controls, and a single 50k-woman adaptation.

## Claims to source
| claim | file | field |
|---|---|---|
| 40 reps, strengths 0.10/0.25/0.45, recovery tables | `results/pilot_recovery_bic.json` | `reps`, `strengths`, `main.<strength>.mse_recovery`, `.bic_recovery`, `.gradient_recovery` |
| zero-signal control | same | `zero_signal_control.0.0.*` |
| seeds, split, worlds | `scripts/q1_pilot.py` | `make_world`, `TRAIN`, `--seed-dgp`, `--seed-fit` |
| engine API, repeatability, layout, adaptation | `results/engine_check.json` | `engine_api`, `baseline.repeat`, `layout`, `adaptation` |
| raw engine stdout | `results/engine_run.log` | provenance of the engine run |

## Commands
```
python3 scripts/q1_pilot.py --reps 40 --out results            # Mac; identical run on box3 at /root/work/q1
CUDA_PATH=/usr/local/cuda-11.8 python engine_check.py          # box3, T4, synthetic panel
```
