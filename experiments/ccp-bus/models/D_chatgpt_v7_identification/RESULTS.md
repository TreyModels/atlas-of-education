# V7: fitted competing mechanisms and temporal test

The available original model's social feedback and reporting congestion were restored in the V6 person/organization and case-pipeline kernel. New Tilly effects were switched off for the primary comparison. A shared case scale was profiled separately for each fit using 2013–2019 disciplinary filings; 2020–2025 case observations were excluded from fitting and candidate selection. The outcome is disciplinary cases, not corruption prevalence.

The 64-draw search and three families generated 192 candidate evaluations, each with two screening seeds; the best four per family were re-ranked with eight independent training seeds. Five parameter dimensions were sampled, with peer gain and reporting capture inactive in the current-incentives family. Seven annual targets cannot identify all behavioral and observation parameters. The fitted case scale is an unknown observation coefficient. These are simulated minimum-distance fits, not posterior estimates.

## Retrospective holdout

| Model | Agents | Input scenario | Log RMSE |
|---|---:|---|---:|
| last_value | N/A | strict | 0.247 |
| log_linear | N/A | strict | 0.885 |
| current_incentives | 12500 | strict | 0.205 |
| current_incentives | 12500 | conditional | 0.218 |
| current_incentives | 50000 | strict | 0.195 |
| current_incentives | 50000 | conditional | 0.206 |
| social_trap | 12500 | strict | 0.219 |
| social_trap | 12500 | conditional | 0.219 |
| social_trap | 50000 | strict | 0.190 |
| social_trap | 50000 | conditional | 0.190 |
| bus | 12500 | strict | 0.220 |
| bus | 12500 | conditional | 0.220 |
| bus | 50000 | strict | 0.190 |
| bus | 50000 | conditional | 0.190 |

Strict forecasts hold land receipts at their 2019 level. Conditional hindcasts use realized land receipts. The 2019 land figure was published in May 2020, so the information cutoff is 24 May 2020. These annual outcomes were already known when this exercise was designed; an independent future period or organizational holdout is needed for an untouched test. The six yearly errors are highly correlated and too few for a reliable model ranking. The last-value benchmark has lower absolute error than some ABM forecasts even when its log RMSE is higher.

## Memory test

Four matched seeds per family began at 5% and 95% misconduct with identical external conditions and identical initial traits. The table shows mean high-minus-low misconduct at selected steps. It is a state-initialization test; no historical pulse, head replacement, debt wipe or full-state reset was executed here.

| Family | Step 1 | Step 10 | Step 30 | Step 60 |
|---|---:|---:|---:|---:|
| bus | +0.8332 | +0.0000 | +0.0001 | +0.0000 |
| current_incentives | +0.0000 | +0.0000 | +0.0000 | +0.0000 |
| social_trap | +0.8332 | +0.0000 | +0.0000 | +0.0000 |

The fitted social and bus families show a large initial response to state differences, followed by rapid convergence in this test. This provides no evidence of lasting memory at the fitted settings. It does not establish that other parameter regions or interventions lack memory. The experiment does not implement the replacement and full-reset tests described in SPEC.md; those remain outstanding.

## Limits and files

The simplified intervention tests are incomplete. The available original model supplied the memory mechanisms; an updated Opus codebase was not present in the workspace. Existing V6 accounting, personnel identity and case-queue code is retained, but a full V6 test suite was not rerun against every V7 family. The model retains assumptions about enforcement ramp, capacity, temperature and reporting. It does not demonstrate that a Chinese official was corrupt or selected personally by Xi. CCPORG has not been ingested.

- `fit.py`, `common.py`, `model.py`, `memory.py`: model and fitting.
- `evaluate.py`: forecasts and held-out scores.
- `memory_test.py`: matched initial-state experiment.
- `results/fit_candidates/`: every sampled fit.
- `results/frozen_fits.json`: selected training fits.
- `results/holdout_runs.json`, `results/holdout_scores.csv`, `results/memory_runs.json`: full outputs.
- `data/`: separate training and holdout files with sources.
