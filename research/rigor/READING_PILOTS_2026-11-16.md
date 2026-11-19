# Reading the 16 November pilot runs

Source: the local run bundle `atlas_local_run_results_2026-11-16` (workbench runner, DeepSeek-executed, audited for
execution integrity). That audit covers hashes, plan identity and failure accounting. It establishes that the runs
are what they claim to be. It establishes nothing about the social theories. These notes say what the pilot
numbers show, at pilot budgets, and what they do not show.

## China youth unemployment (384 fits, 48 cells)

- **No fit beats the naive benchmark, in any cell.** With a 2024 cutoff the best test MAE across all restarts is
  1.48 against 0.89 for the same month a year earlier. With a 2022 cutoff the best cell mean on verified
  new-method months is 3.05 against 1.61.
- **The forecast is not pinned down by the training data.** Within one cell, restarts with almost the same training
  error (e.g. 1.81–2.05) give test errors from 1.6 to 3.9. Many parameter sets fit the past equally well and
  disagree about the future: the "sloppy" pattern of Gutenkunst et al. (2007). The categorical mechanisms (waiting,
  insider protection, credential ranking) are not identified by this series.
- Pinning the step at its data-sized values (0.041, 0.068), or at zero, worsens the out-of-sample fit in most cells.
  The fitted step is doing real work, and that work is unexplained. `youth_placebo` tests whether August 2021 is
  special.

## Credential floor (1,152 trials)

- The paired premium effect (2035, falling minus baseline premium, Q3+) differs by structure and hardly at all by
  country or financing rule: HC −0.11 to −0.13, POS −0.05 to −0.06, REL −0.02. So the structures differ in their
  *response to a premium change*, not in their wealth profiles. That is the identification route
  `credential_recovery` tests (design D1).
- Caveats: every draw fails the profile screens (median profile errors 0.22–0.46), so these are prior-predictive
  magnitudes, not Cambodian ones. The sign is built in. The ordering HC > POS > REL is partly built in too, because
  positional and relational terms add value that does not move with the premium. The recovery study asks whether the
  ordering survives measurement error and the profile constraint.

## Shadow education (960 trials, prior draws)

- 0/960 prior draws meet the published patterns, as expected.
- The response to a ban on own-pupil tutoring separates **favour** (participation −0.24 on average) from **thin** and
  **diversion** (−0.04 to −0.05). Thin and diversion are almost indistinguishable in every policy response, and
  withholding is tiny (mean 0.007 of the curriculum). Within these priors, diversion behaves like thin.
  `shadow_recovery` design S4 tests whether a ban response would discriminate near the data.
- 15 non-convergences, all in `full` with four subjects; 15 more in the conditional-pay counterfactual.

## Cambodia child labour (128 trials)

- No lever's effect changes sign across nuisance draws. The ranking is stable: cash > feeding > protection > cashU >
  tutorFix > debtRelief > the rest.
- But the nuisance draws vary incomes, debt and school values. They do not vary the lever effect constants
  (feeding 0.07/0.05, protection +0.15 quality, the left-behind penalty −0.45, and so on), which are invented. The
  ranking is stable against things that are not the levers' effect sizes. `camchild_validation` checks the one
  lever with Cambodian experimental evidence.

## Angkor (1,280 trials)

- The pilots confirm the review. Drought retention is 0.53 with multiplier 1 and 0.98 with 1.44. The water floor
  moves drought retention by up to 0.47. Without independent historical targets, more draws refine only the
  model's conditional behaviour.

## School futures (deterministic)

- Hong Kong one-step forecasts beat the flat benchmark on most outputs (pupils 5.9k vs 8.5k MAE; classes 38 vs
  118; staff 215 vs 413). Multi-year margins are small (pupils 23.8k vs 26.7k; sites 15.6 vs 16.4).
- National series have 1–4 forecasts each: anecdotes, not evidence.
- The flat benchmark is weak for enrolment, because the cohorts entering school are already born. The fair
  benchmark is a cohort-progression naive forecast: last observed grade-to-grade ratios applied to known cohorts.
  Add it before claiming the model adds skill. `analyze.py` now gives DM tests against the existing benchmark and
  flags rows that carry a `conditional` field. Confirm none of those forecasts uses data dated after its origin.

## Out of Africa (640 trials)

- Mixed reaches Sahul most often (77% vs 72% terrestrial vs 63% coastal). Only 17–20% pass the site gates, and
  chronology S passes none by construction. Rankings are conditional on the model family and the sensitivity bracket.
