# External review of the China youth-unemployment model: items 1.1 to 1.8

Scope: the review points in the task brief. "Before" is the engine on disk (`engine/firms/results/china_fit.json`,
`tilly_fit.json`), which a refit with the old bounds reproduces exactly (cost 244.858, identical parameters). "After" is the
widened-bound, pinned or variant refit. All scores use the engine's own residuals (`calibrate_china.pairs_for`). Costs are
half the sum of squared residuals; MAE is in percentage points. The site's `public/engines/atlas_data.js` is an older
export and differs from the engine files; it has not been regenerated (see "Not done").

## Summary

| Item | Status | Headline changes? |
|---|---|---|
| 1.1 Aug-2021 step | Relabelled everywhere in the engine and in `youth.js`. Sourced data give a data-sized step of about 0.02 to 0.07. Fixed-step variants fit worse in sample and do not fix the vacancy check. | Rise stays about 5 pp, but the Shapley share attributed to the step is unexplained, not demand. |
| 1.2 Bounds | Seven parameters sat on bounds, not four. Two of the stuck ones are structural limits, so "double the range" is infeasible for them. Widened and refit. | Rise 5.18 to 5.06. Fit cost improves 244.9 to 227.3. Parameters move a lot. |
| 1.3 lam_g | Data-derived lam_g of 0.012 to 0.016 per month. The review's 0.0025 is not the on-disk headline (which has lam_g = 1.0). Pinned refits done. | Rise stays 5 to 6 pp with pinned lam_g. Without refit, the on-disk fit collapses at any lam_g below 0.06. |
| 1.4 Waiting counterfactual | The +22.8 pp is not reproduced. Current file gives +12.2. Explanation and broad metric added. | Explanation changes; the waiting effect is about 7 pp on the measured rate. |
| 1.5 Tilly mechanisms | Mechanisms presented as supported are relabelled as built in and untested. 22 text proposals in `TEXT_CHANGES.json`. | Wording only. |
| 1.6 Shapley label | Renamed to "Aug-2021 step (unexplained)" in `calibrate_china.py` and `youth.js`. | Label only. |
| 1.7 Holdout and naive | Benchmark rows added to `youth.js` (`AtlasYouth.benchmarks`). Naive beats the early fit on both out-of-sample windows. | Shows the fit fails out of sample. |
| 1.8 Lake null | Plain four-parameter constant-rate lake model run on the same series. | The categorical model is not shown to beat it out of sample. |

## 1.1 Aug-2021 step (dr_drop)

Mapping from sourced data (`derive_inputs.py`, `results/derived_inputs.json`):

- Real-estate development employment fell 27.0% from 2018 to 2023. This is one segment only: total real-estate
  employment rose 14.0% over the same years. The review's "real-estate employment -27%" should be qualified.
- Tutoring: about 3 million jobs lost within four months (Huang et al. 2025), against about 11 million pre-policy
  employees (secondary), so 0.27. The source says job losses, not openings.
- Graduate-accessible shares of these sectors are not sourced. They are assumptions: real estate 5 / 10 / 15%,
  tutoring 2.5 / 5 / 10%.
- Resulting step: dr = 0.020 (low), 0.041 (central), 0.068 (high). Fitted step: 0.30 (old full window), 0.32 (widened
  full window), 0.079 (early window only).

Fixed-step refits (other parameters free, widened bounds, warm start from the on-disk optimum):

| dr_drop | Window | Cost | Whole-record MAE | Holdout 2023H1 MAE | Verified new MAE | Rise (pp) | Vacancies 2025H1 y/y |
|---|---|---:|---:|---:|---:|---:|---:|
| fitted 0.32 (widened) | full | 227.25 | 1.76 | 3.16 (in sample) | 1.13 (in sample) | +5.06 | +8.3% |
| 0.020 (low) | full | 277.41 | 1.95 | 3.70 | 1.33 | +5.00 | +27.4% |
| 0.041 (central) | full | 255.71 | 1.88 | 3.51 | 1.27 | +5.11 | +19.6% |
| 0.068 (high) | full | 244.24 | 1.84 | 3.38 | 1.22 | +5.13 | +15.1% |
| fitted 0.079 | early (2018-22) | 78.95 | n/a | 7.13 | 5.54 | +0.09 | +44.1% |
| 0.041 | early | 81.04 | n/a | 7.04 | 4.91 | +0.66 | +29.0% |

Reading: a data-sized step fits worse in sample (cost up by 10 to 50). The observed graduate-vacancy fall (Caixin, about
-22% y/y in H1 2025) is not reproduced by any variant; the sign is wrong in all of them. The fitted step size is unstable
across windows (0.08 on 2018-22, 0.30 on the full record). Shapley, on-disk headline: supply +1.47, composition -0.10,
demand -0.04, Aug-2021 step +3.84, of a total +5.18 pp. Widened headline: supply +1.91, composition -0.18, demand 0.00,
step +3.33, of +5.06 pp. These shares hold the other parameters fixed; with the step at its data size and the others
refitted, the rise stays about 5 pp, so the rise is not identified as step-driven.

Changes made: the label is "Aug-2021 step (unexplained residual, fitted)" in `worlds.js` and the reference page (proposed),
the docstrings in `engine/firms/model.py` and `calibrate_china.py`, and in `youth.js`. The docs claim that the tutoring
ban "lost 3m openings" is corrected to job losses.

## 1.2 Bounds

Code: `engine/firms/calibrate_china.py`, `FREE`.

Seven parameters sat on a bound in the on-disk full fit: m_g (0.03, lower), m_n (0.42, upper), f_n_ref (0.38, upper),
lam_g (1.0, upper), m_a (0.02, lower), e_prop (0, lower), dr_drop (0.30, upper). The early fit has four: m_n, f_g_ref,
f_n_ref, e_prop.

Two of the stuck parameters are structural limits, so doubling the range is not possible without a model change:

- m_n: the non-graduate wage w_n0 = p_n0(1 - m_n) must stay above the flow value z_n = 0.55, so m_n < 0.45. The old upper
  bound 0.42 sat just below that ceiling. The upper bound is now 0.449, not 0.84. (A first attempt with 0.84 hit this
  constraint and wasted starts.)
- f_n_ref: the urn-ball matching needs f < a = 0.40. The upper bound is now 0.399, not 0.76. A doubled range needs a
  larger application rate, so a variant with a = 0.80 and f_n_ref up to 0.76 was run separately.

Changes: m_g lower 0.03 to 0.00; m_n upper 0.42 to 0.449; f_n_ref upper 0.38 to 0.399; m_a lower 0.02 to 0.00; dr_drop upper
0.30 to 0.60. lam_g stays capped at 1 and e_prop at 0. The fit penalises infeasible points rather than aborting.

| Fit (full window unless stated) | Cost | Early MAE | Holdout 2023H1 MAE | New MAE | Whole MAE | Rise (pp) | At bounds |
|---|---:|---:|---:|---:|---:|---:|---|
| On disk (= old bounds, reproduced) | 244.86 | 2.05 | 3.17 (in sample) | 1.27 | 1.86 | +5.18 | m_g, m_n, f_n_ref, lam_g, m_a, e_prop, dr_drop |
| Widened bounds | 227.25 | 1.95 | 3.16 | 1.13 | 1.76 | +5.06 | f_n_ref, m_a, e_prop |
| Widened, a = 0.80 | 241.52 | 1.86 | 2.88 | 1.69 | 1.87 | +4.80 | m_g, f_g_ref, lam_g, m_a, sep_scale, e_prop |
| Early window, on disk | 79.01 | 1.19 | 7.14 (true holdout) | 5.54 | n/a | +0.08 | m_n, f_g_ref, f_n_ref, e_prop |
| Early window, widened | 78.95 | 1.20 | 7.13 | 5.54 | n/a | +0.09 | f_g_ref, e_prop |

Parameters, on disk to widened: m_g 0.030 to 0.361; m_n 0.42 to 0.332; f_g_ref 0.323 to 0.380; f_n_ref 0.380 to 0.399;
lam_g 1.00 to 0.004; zeta 0.277 to 0.263; m_a 0.02 to 0.00; sep_scale 1.32 to 1.51; july_g 0.56 to 0.58; e_prop 0.00 to
0.00; dr_drop 0.30 to 0.32.

Verdict: the headline rise does not change (5.2 to 5.1 pp). The parameter values do change a lot, and the cost surface is
flat: several different parameter sets fit within a few cost units. The on-disk optimum was reached by a warm start; a
multistart with the new bounds alone did not reach it, so the warm-started result is the one reported.

## 1.3 lam_g (graduate wage speed)

Derivation (`derive_inputs.py`): ratio r_y = 12 x MyCOS starting pay / NBS urban non-private wage. r = 0.782 (2015),
0.777 (2016), 0.747 (2018), 0.721 (2019), 0.674 (2020), 0.655 (2021), 0.630 (2022), 0.602 (2023). Half of the 2015-23 decline
is reached after 4.63 years (origin 2015) or 3.68 years (origin 2016). Formula: lam = 1 - 2^(-1/H), with H the half-life
in months. Central lam = 0.0124 (origin 2015) or 0.0156 (origin 2016); a fast variant with a 12-month half-life gives
0.0561.

Assumptions: the observed decline is one monotone adjustment; the series alone does not identify the target, so this is
an order of magnitude, not a regression estimate.

The review's 0.0025 implies a half-life of 277 months (23 years), which cannot match a 23% fall in relative pay over
eight years. The on-disk full headline has lam_g = 1.0 (the flexible benchmark), not 0.0025. The 0.0025 belongs to the
Tilly parameter set in `public/engines/atlas_data.js` (lam_g 0.0025); the site headline there has lam_g 0.0035.

No-refit sensitivity (on-disk parameters, only lam_g changed; `lam_sensitivity.py`):

| lam_g | Rise (pp) | Whole MAE |
|---|---:|---:|
| 1.0 (on disk) | +5.18 | 1.86 |
| 0.0561 | +36.9 | 14.1 |
| 0.0156 | +36.9 | 14.1 |
| 0.0124 | +36.9 | 14.1 |
| 0.0025 | +36.9 | 14.1 |

The on-disk fit is only valid near flexible wages. Pinned refits (other parameters free, widened bounds):

| lam_g pinned | Cost | Whole MAE | Holdout 2023H1 | New MAE | Rise (pp) | At bounds |
|---|---:|---:|---:|---:|---:|---|
| 0.0025 (review) | 230.91 | 1.79 | 3.27 | 1.14 | +5.07 | m_n, f_n_ref, m_a, e_prop |
| 0.0124 (data, central) | 278.39 | 1.95 | 3.11 | 2.21 | +5.82 | m_g, m_n, f_n_ref, e_prop |
| 0.0561 (data, fast) | 268.50 | 1.96 | 2.85 | 2.24 | +5.97 | m_n |
| Free (widened) | 227.25 | 1.76 | 3.16 | 1.13 | +5.06 | f_n_ref, m_a, e_prop |

Verdict: lam_g is weakly identified. The free fit moves it between 0.004 and 1.0 across local optima, and the early fit
gives 0.15. Pinning it at a data-derived value makes the fit worse in sample (cost 230 to 278 against 227), and the rise
stays at 5 to 6 pp. The result does not depend on lam_g as strongly as the on-disk no-refit test suggests, but it is not
pinned by the data either.

## 1.4 Waiting and the "no waiting" counterfactual

Before: `docs/engine/facts_register.md` cites +22.8 pp for "no waiting". The current `tilly_fit.json` gives +12.17 pp (rate
and slack, parameters held fixed). The +22.8 comes from an earlier run and is not reproduced. The facts-register sentence
is proposed for correction in `TEXT_CHANGES.json`.

With waiting (same parameters): measured rate +5.07 pp; broad unemployment (unemployed plus waiting, over the labour force
plus waiting) +9.47 pp; about 2.0 million graduates are waiting in 2024 to 2026.

Why the measured rate rises less: graduates waiting are removed from both the numerator and the denominator of the
measured rate, so the rate falls when people move to waiting. The no-waiting counterfactual also changes flows (no exits to
waiting, more search and hires), so it is not pure accounting. The broad measure is the honest comparison for the
accounting channel.

Metric: `youth.js` now outputs `broad_u` (unemployed plus waiting, over labour force plus waiting). It equals the existing
`slack` series.

## 1.5 Tilly mechanisms presented as supported

Set, not estimated (`tilly_fit.FIXED`): secure posts 10% of entry, hoarding 40%, wage wedge 20%, insider split 50%. No
hukou, party-membership or parental-sector data exists in the inputs, so the insider line and the wedges are untested.
Waiting family support and emulation rates are untested as well.

Places that present the mechanisms as supported (all proposed in `TEXT_CHANGES.json`, not applied):

- `public/worlds.js`: the evidence entry on the reference, the hoarding control note, the waiting control note.
- `public/reference/education/index.html`: the world pitch ("act at those boundaries"), the youth-labour-market card, the
  preset label, the parameter note, the insider-share sentence in the refit note, the "adaptation hides slack" sentence.
- `src/data/model-catalogue.md` (and the zh-Hans and vi versions, not yet edited): "earn their place".
- `engine/firms/categorical.py` docstring: "Four mechanisms do the work".
- `docs/engine/facts_register.md`: the +22.8 sentence.

## 1.6 Shapley label

`sector` is the Aug-2021 step (`dr_drop`); `e_prop` is fitted to about 0, so the component is not real estate. Relabelled
"Aug-2021 step (unexplained)" in `calibrate_china.py` (`LABEL`) and in `youth.js` (`shapleyLabels`). The stored
`ATLAS_DATA.shapley.label` in the site file still carries the old label until the file is regenerated.

## 1.7 Holdout and naive benchmark

Only `early|sigma_A=5.0` is a true holdout (fitted 2018-22). `full|sigma_A=5.0` is in sample, including its "2023H1 holdout"
and "new method" numbers.

| Window | Model (early fit) | Naive (same month of 2022) |
|---|---:|---:|
| Holdout, 2023 H1 (old method), MAE | 7.14 (engine), 6.83 (site file) | 2.50 |
| Forecast, Dec 2023 to Sep 2026 (verified), MAE | 5.54 (engine, n=32), 5.50 (site, n=24) | 1.61 (engine), 1.71 (site) |
| Fit, 2018-22 (in sample) | 1.19 | n/a |

The naive benchmark beats the early fit on both out-of-sample windows. `youth.js` exports `benchmarks(DATA)` for these rows.
Wiring into the China world's metrics is in `proposed_worlds_wiring.js` and is not applied, because `public/worlds.js` is
outside this review's edit list.

## 1.8 Lake null

`lake_null.py` (results in `results/lake_null.json`): one pool, constant job-finding f and separation s per month, exit
1/27 per month, observed entrant flows (the engine's psi values), a fitted July share q, and a fitted method offset delta.
Four free parameters, against 11 in the headline. An entrant-scale parameter was dropped because the system is linear in
the inflow, so the scale is not identified.

| | Lake null | Categorical model (early fit) | Naive |
|---|---:|---:|---:|
| Fit 2018-22 MAE | 2.66 | 1.19 | n/a |
| Holdout 2023H1 MAE | 8.45 | 7.14 | 2.50 |
| Verified Dec 2023 to Sep 2026 MAE | 2.88 | 5.54 | 1.61 |
| Whole-record MAE (full fit) | 2.88 | 1.86 (in sample) | n/a |

Lake on the full window: f = 0.962 (at its structural cap) and delta = -2.06; early: f at the cap and delta at -5 (its bound).
Out of sample, the lake beats the categorical model on the verified new-method months and loses on 2023 H1. Both lose to
the naive benchmark. On the full window, the categorical model has the smaller AIC, but it has 11 parameters against 4.
Verdict: the categorical model is not shown to beat the plain null out of sample. The July spike, waiting and insider
protection remain untested.

## Other findings

- The site `atlas_data.js` is an older export. Its profiles differ from the engine (full|5 rise 4.99 against 5.18; site
  headline lam_g 0.0035 and m_g 0.35), and its verified new-method count is 24 against 32 in the engine. It has not been
  regenerated; that is the owner's call.
- The "+22.8 pp" and the "real-estate -27%" figures in the review and docs are corrected above.

## Not done, and why

- DeepSeek-exec launch was denied by the permission classifier, so the refits were run directly with the local Python
  (`run_fits.py`), not through DeepSeek. A later request to draft this README through the flash model was also denied.
- `public/evidence.js` pins the `youth.js` SHA-256. The hash edit was denied as an integrity change, so `test-worlds.cjs`
  fails the `china` world on that hash. Updating the pin, or regenerating `evidence.js` with `prepare-evidence.py`, needs
  your approval.
- `public/worlds.js`, `public/reference/education/index.html`, `src/data/*`, and `docs/*` are not edited. Proposals are in
  `TEXT_CHANGES.json`.
- New strings in the proposals need zh-Hans and vi entries when applied. Entries already added to `public/languages.js`
  cover the strings `youth.js` now outputs and the two relabel strings in the proposals. The `check-translations` run
  passes.
- The site `atlas_data.js` was not regenerated, so the site still shows the older fit.

## How to rerun

From `experiments/youth-review` with `./.venv/bin/python` (numpy 2.2, scipy 1.15):

- `python derive_inputs.py` (inputs for 1.1 and 1.3)
- `python run_fits.py baseline` and `python run_fits.py one <name>` for the bounds, step and lam fits
- `python lake_null.py`, `python lam_sensitivity.py`, `python shapley_check.py`
- `python make_text_changes.py` (checks every quoted string occurs exactly once before writing `TEXT_CHANGES.json`)

Node checks (Node 18; the default Node 16 lacks `node:test`): `node test-worlds.cjs` and `node check-translations.cjs`.
Current result: `check-translations` passes; `test-worlds` runs 52 tests, with one failure (`china`, pinned hash).
