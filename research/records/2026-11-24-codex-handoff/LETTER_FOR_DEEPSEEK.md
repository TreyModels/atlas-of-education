# Trey’s next Atlas experiments — handoff from Codex

DeepSeek: Trey asked for executable research work, not another unbounded regression sweep. This package contains the review since Sonnet’s handoff, the work Gemini contributed, and three new, tested scripts. Start here; do not assume any previously stated result is independently verified unless identified as such below. The three questions at the end are my priorities, in order. The first supplied benchmark is intentionally simple and CPU-only; it is **not** the Atlas GPU model. You have a server: adapt the real engine only after the checks below, record the difference, and run bounded pilots before scaling.

## Read first

1. `research/records/2026-11-24-codex-review/REVIEW.md` and `findings.csv` in this bundle. Review branch locally at Codex commit `8b48e61` (not necessarily present on GitHub).
2. Sonnet: GitHub branch `research/assessment-and-next-experiments-2026-11-24`, records `research/records/2026-11-24-assessment-and-next-experiments/` and `research/records/2026-11-24-next-tests/`. Start with `PAPER_PLAN.md`, `CLAIMS_LEDGER.md`, `NEXT_EXPERIMENTS.md`, `LETTER_FOR_DEEPSEEK.md` and `gemini/REVIEW.md`; inspect Gemini’s unchanged `gemini/Next_Tests_Runbook.md` too. These are useful but contain superseded statements. Do not execute the old letter blindly.
3. GPU records on branches `research/cuda-scale-2026-11-23`, `research/dose-gpu-2026-11-23`, `research/transition-gpu-2026-11-23`, `research/dose-tolerance-2026-11-23`; start with each record’s README, `scripts/`, and results. Read `cuda-scale/results/determinism_v2.json` and dose `results/PORT_NOTES.md`. These GPU findings are reported in repo records; Codex did not independently run the GPU.

## What changed after Sonnet and Gemini

- Codex ran all nine scripts from the two new records in clean copies with Python 3.10, NumPy 2.2.6, pandas 2.3.3, SciPy 1.15.3, statsmodels 0.15.0. Their generated committed outputs matched byte-for-byte. Reproducible does not mean correct interpretation.
- Crucial correction: `effective_fertility` means expected surviving children per woman, not total births. The transition source script defines it and writes it separately from UN TFR. Hence Q2 outcomes need not agree, and Q3’s nine-country “TFR” race actually models effective fertility. Do not extend that benchmark as TFR without replacing the input and redoing the analysis.
- Sequencing default reproduces 31 forward / 3 reverse-or-tie / 30 undetermined, with 18-year median in 18 both-dated countries. It is not an estimate that 91% of all 64 countries are forward. A threshold sweep changes the sample as well as the rule. The 7% labour-demand figure is not sound evidence against a demand mechanism; its original input identity and same-sample upper bound are not yet established. Source script bins 1991 paid-employment data into 1990 and builds a premium from multiple WDI series.
- Gemini’s runbook is useful but its lead/lag starter drops incomplete rows before shifting, and its residualized regression omits a necessary control for equivalence. Country fixed effects are compatible with “no country trends.” Its numerical claims remain unverified unless the review says otherwise.
- In the stylized known-truth simulation, the original robust rule fires 85/100 times for one minority-effect scenario; that is not general error calibration. Simulation choices were revised after inspecting results. The methods paper cannot infer that BY finds zero from floor counts alone; run the full sorted p-value calculation. Valid p-values and an appropriate test family are prerequisites.
- Q5’s donor backcast uses donor data from the years hidden in the target; this is conditional on such donor histories existing. Its so-called naive baseline is a transformed three-point anchor-period mean, not simply the 1990 value.
- The two tracks Trey wants are simulated competing mechanisms and country pathway comparisons. Do not promise that descriptive correlations or simulations alone identify a real mechanism.

## Immediate reproducible commands

From the root of the extracted bundle, create/use an environment containing NumPy and pandas. Work in a new directory or branch; preserve inputs. For a clean Linux Python 3.10+ environment, install packages from your existing trusted environment or use a new virtualenv. Record `python -V`, versions, input SHA-256, platform, seeds and all stdout/stderr. No secrets in logs or bridge messages.

```bash
R=research/records/2026-11-24-codex-handoff
P=research/records/2026-11-24-next-tests/data/long_run_panel.csv
export OPENBLAS_NUM_THREADS=1
python3 -I "$R/scripts/test_checks.py"
python3 -I "$R/scripts/competing_worlds.py" --seed 71201 --reps 200 --n-per-cell 400 --out run-codex/synthetic
python3 -I "$R/scripts/country_pairs.py" --panel "$P" --baseline 1980 --start 1990 --end 2010 --out run-codex/pairs
```

Expected local smoke: five tests pass; pair metadata reports **105** baseline-complete countries, **52** disjoint pairs, **1** unpaired, **52** pairs with both 1990–2010 schooling and TFR changes. Input SHA-256: `cd30d7ea7beb77b63de092c53f9b143065b94651f1ac95535ac70eebb3280f2d`. These are exploratory outputs, not a preregistered finding. Synthetic benchmark default (oracle-known parameters): structured micro likelihood wins 200/200 in effect and selection worlds, 0/200 in common-trend world. It deliberately makes effect and selection observationally identical; this is a constructed demonstration, not estimated power or evidence that real microdata distinguish the theories. See `SYNTHETIC.md`.

`country_pairs.py` locks pairs using 1980 GDP, urbanisation, schooling and TFR before examining 1990–2010 changes. It greedily matches disjoint cases on standardized baseline distance. It is deterministic but neither globally optimal nor representative of all countries; it does not prove causal similarity. All pairs are retained, not cherry-picked; incomplete future outcomes stay missing. Treat the 1990–2010 comparison as exploratory because we have already run it. Before any inferential test freeze a new hypothesis and use a genuinely untouched sample/period where feasible. Do not fit multi-parameter clustered regressions to two countries or call overlapping cases independent. Add a triad algorithm and uncertainty only after defining the target question; keep all attempted matches and disclose outcome-driven selection.

The BH/BY checker takes **actual complete** p-value families, CSV columns `family,link,p`, one row per link. It does not create valid p-values or recover missing null draws:

```bash
python3 -I "$R/scripts/fdr_check.py" --input YOUR_VALID_COMPLETE_PVALUES.csv --output run-codex/fdr_checked.csv
```

The test suite includes a constructed 272-p-value example where no p-values are at the floor but 168 still pass BY: it checks the entire ordered list, not just floor counts. Do not apply it to the robust-everywhere verdict as if that rule were a p-value. Audit all four actual families separately; a joint collection of claims has a different multiplicity question.

## Three questions to answer, not just three batches to run

### 1. Can genuinely different mechanisms fit the same aggregate history, and which independent measurements discriminate them?

Use the synthetic script as a unit check, not a demographic model. Design at least three genuinely distinct, plausible worlds: direct schooling mechanism, common-development/selection, and a defensible alternative such as fertility/education joint choice. Make intervention semantics explicit; do not simply relabel the same kernel. Generate repeated known-truth data with independently seeded data-generation and fitting. Fit each rival using the same historical aggregate training information and comparable search budgets, with uncertainty and diagnostics; check parameter and model recovery over multiple parameter strengths, seeds and realistic sample sizes. Freeze target countries/time windows and data transforms before looking at evaluation results. Evaluate on independent held-out country/cohort/time and, where available, independently sourced age-at-first-birth, education-by-cohort, births by wealth and residence—not the same observations used to calibrate. Report model fit, predictive errors and uncertainty, and the cases where rival mechanisms remain observationally indistinguishable. Do not call a model winner an established cause. Preserve negative and failed runs.

Implement this against the real GPU engine only after verifying its API and baseline. Existing record’s two rivals already showed no clear out-of-sample individuation advantage and broad parameter intervals; neither a near-prior posterior nor a small uncertainty interval from an implausible model settles the true mechanism. The old mortality-freeze counterfactual is model-conditional, with schooling/income paths still following history; it is not a real-world attribution of the fertility fall.

### 2. Do similar starting countries take different educational, labor and fertility pathways?

Run the baseline pair script as a smoke test; retain raw lists and diagnostics. Improve by auditing baseline sources and missingness, distances and alternative pre-specified matching choices; include farming employment where dated coverage permits without inventing earlier values. Select contrasting as well as similar paths using explicit documented criteria, then examine a small number of matched pairs or triads against independent historical sources. Label the data series and how estimated. Avoid inferring a causal mechanism from time ordering. Where feasible, hold out countries for checking hypotheses generated by other countries and publish all selected cases, including counterexamples. Evaluate selection sensitivity and compare against random matching; this is descriptive, not a p-value factory.

### 3. When does the grouping multiverse get fooled, and can it say what differs rather than merely assign a verdict?

Use the original estimator and fixed code versions when available. First establish panel provenance/hashes and run the small known-truth study with independent seeds, including null, uniform, minority-only, varying-strength same-sign and shared-trend worlds. Separate Monte Carlo uncertainty from uncertainty about mechanisms and sample size. Report false positive/negative and group-localisation rates with intervals, not just “travels everywhere”. Validate empirical random-partition p-values and exchangeability before interpreting BH/BY. Recompute actual BH/BY with all 272 ordered p-values for each family, if the inputs exist. Do not infer BY zero just from the number at the minimum p-value.

## GPU safety and validation gate

Before scaling, run a small, fixed-seed baseline against the documented reference, inspect `scripts/run_determinism2.py` and its dependencies, and reproduce the existing batch-layout diagnostic. The repo record reports that fixed seed + fixed layout is repeatable but changing batch layout changes random streams, with notable output differences. Pin and log batch layout for an initial reproduction. If implementing a fix, use stable identifiers keyed by experiment/replicate/country/person, create it in a copy, and demonstrate that identical units get identical draws across batching/reordering without accidentally sharing streams. Compare independent-seed distributions and reference outputs; distinguish harmless floating-point reduction differences from changes in individual states. Check the GPU port’s marriage-market deviation explicitly. Do not claim bit identity across architectures without testing it. Maintain before/after outputs and code, and run a representative pilot with finite resource bounds before scaling. No GPU benchmark or causal claim is accepted until these checks pass.

## Deliverables and operating rules

Return one concise `REPORT.md` with questions, hypotheses, input hashes, exact commands, source commit, seeds, sample-selection flow, actual GPU/CPU time, failures, deviations, comparisons, uncertainty and output paths; separate fact, model result, inference and unverified claim. Save scripts/configs, full logs and machine-readable tables, including null/failed results. Use a new branch or output directory; never rewrite existing branches, open PRs or publish on Trey’s behalf. Do not send passwords, tokens, SSH keys or private connection details through the bridge. If a required input or GPU is missing, run the self-contained checks and report the blocker rather than silently substituting data. Start with a small bounded pilot; do not run the old 1,200-draw or 100-million-agent scale job simply because the server is on. Tell Trey when finished so he can shut down billed resources.

Plain-language bottom line: we are trying to learn whether different stories produce the same observed transitions, which additional evidence can distinguish them, and whether countries follow more than one pathway. A fast computer helps explore those questions; it does not make an assumption into a historical fact.
