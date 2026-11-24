# PRE-REGISTRATION — fitted-worlds feasibility pilot (task-24)

**Status: committed BEFORE any pilot code and before any fitting run.** This is a **small,
staged, EXPLORATORY feasibility pilot**, not a confirmatory run and not a calibration
campaign. Branch `research/fitted-worlds-pilot-2026-11-24`, additive from the corrected
branch head `7f0221bd`. The audited corrected-experiment code `a12d357` is **not edited** by
this pilot. All model/fitting compute runs on region-42; no model compute on the Mac;
existing outputs are preserved and never overwritten.

**Question.** Once each of the four literature worlds (P, S, C, R) is fitted to observed
aggregate moments, do the worlds still separate at the macro level, or do they converge?
**First question (gate):** is that even answerable with the constructs the project actually
holds? If the constructs do not line up, the pilot stops and reports **"insufficient
evidence"**; no target is invented.

**Authorisation and gate.** Codex approved this design in principle (Bridge
`1028340e`, 2026-11-24T12:26:59Z) subject to a five-stage gate. The programme Lead launched
the pilot under that gate (Bridge `2026-11-24T12:44Z`). Every stage may stop the pilot; a
stage failure is a reportable result, not something to work around.

**Labels.** EXPLORATORY throughout. No confirmatory claim. No causal claim. No comparison
with E1's 1.8% real-data robustness figure. No theory ranking from ABC acceptance counts.
No identification claim from prior width or posterior overlap.

---

## 0. Evidence base — committed repo data only

Only data already committed in this repository is used. **No new external pulls, no DHS
microdata acquisition, no imputation of missing observations, no synthetic "targets".**

| # | source (branch / path) | content | unit and period | the audit must record |
|---|---|---|---|---|
| D1 | `origin/research/massification-panel-2026-11-22` → `research/records/2026-11-22-massification-panel/sources/wdi_sweep/` | WDI/UIS/ILO-modelled series as `[iso3, year, value]` JSON (uncompressed or `.json.gz`). Relevant: `child_work` (ILO/UCW children 7–14 in employment), `pre_ger` (primary GER), `prm_ner`, `sec_ner` (net enrolment), `lsc` (lower-secondary completion), `test_scores` (harmonized test scores), `hci` (learning index), `gdppc_log`, `fertility`, `repeat_prm`, etc. | country × calendar year; mixed vintages (`child_work` 1994–2016; `pre_ger` 1970–2022; `test_scores` 2010–2020) | countries, years, observations, overlap between series |
| D2 | `engine/data/asia_school_work.json` (on the handoff/massification branches) | 21-country cross-section: `oos_lower` (adolescents out of school, lower-secondary age; UIS via WDI) and `child_labour` (% children 5–17; ILO/UNICEF estimates as tabulated on Wikipedia), plus 3 survey composition facts used by their record as tests, never matching | one row per country; **years differ by row** (2010–2023) | exact row coverage, year heterogeneity, the file's own caveats |
| D3 | `experiments/massification-2026-11-20/04_data/shadow_round2/data/shadow_incidence_round2.csv` / `shadow_fees_round2.csv` | hand-collected shadow-education (tutoring) incidence/fees; 38 and 20 rows; several are case studies, not national | country/site × year; no harmonised panel | row coverage, definitions, confidence labels |
| D4 | E1 record `research/records/2026-11-25-e1-multiverse/` | **derived outputs only** (272 WDI links, 179 countries, 1940–2025; 17 WDI variables). The raw WDI panel is **not committed** (it lived at `/root/work/data` on a different host) | derived link statistics | that raw E1 panel is unavailable from the repo; no re-pull allowed |
| D5 | Q2 record `research/records/2026-11-25-q2-pathways/data/long_run_panel.csv` | 197 countries, 1750–2024: child mortality, life expectancy, effective/TFR fertility, mean years of schooling, Maddison GDP pc, urban share | country × year | variable availability by year; age/definition of schooling variable |
| D6 | DHS API cache `research/records/2026-11-24-dhs-api-ecological/data/` | published DHS **API cells** (no microdata): fertility (TFR/GFR/wanted fertility), age at first birth, women's education, mean CEB by education; 370 surveys | survey round × country × background category | indicator list, countries/surveys, education categories, denominators |
| D7 | `research/records/2026-11-24-dhs-acquisition/data/ceb_education_cells.csv` | published DHS API cells: mean children ever born (women 40–49) by education | survey × country × education | rows, countries, years, definitions |
| D8 | `docs/engine/comparative_cases/philippines_enrolment.json` | one-country higher-education headcount series, 5 academic years 2015–2020 | student headcount × academic year | irrelevant to the ABM kernel (no tertiary layer); marked unmatched |

Anything not in this table is out of scope. If a needed construct is absent, it is reported
as absent — not inferred.

## 1. STAGE 1 — construct/feasibility audit (before any fitting)

**Outputs to map (all model observables in this programme):**
1. `ger` — share of households with a child in school (states 0 or 1; no age, no grade);
2. `cl` — observed child employment (states 1,2);
3. `sw` — study-and-work share (state 1);
4. `wo` — visible-work-only share (state 2);
5. `hw` — hidden work (state 3; unobserved by construction);
6. `tut` — tutoring share;
7. `learn` — mean learning in model grade-equivalents;
8. `inc` — mean household income in model units;
9. Phase B `B1` — within-mother post-death birth-spacing contrast;
10. Phase B `B2` — parity-progression gradient by education;
11. Phase B `B3` — age-at-first-birth gradient by education.

For **each** output the audit records, in a table: the candidate observed series (IDs D1–D8),
**age/sex target population, unit, definition, period**, source, coverage
(countries/years/observations), and one of:

- **compatible** — same target population (or the model output is genuinely age-unspecified
  and the observed series can be aggregated with **no invented age rule**), same unit (or an
  exact declared transformation), same period definition (calendar or a declared event-time
  alignment), and a defensible data vintage;
- **partial** — same broad construct but a mismatch in age, unit, definition or period that
  would require a declared and testable approximation;
- **unmatched** — no observed series in the repo, or only a construct that is conceptually
  different (e.g. attainment stock vs participation flow, test-score scale vs model
  grade-equivalents, country GDP pc vs household income in arbitrary units, hidden work that
  surveys do not observe).

The audit also reports **joint coverage**: for every pair/triple of model outputs that must
be fitted *jointly* (the four worlds differ mainly in the school/work/tutoring decomposition),
the countries × years where all of them are observed together, and how many non-overlapping
train/validation units that leaves.

**Stage 1 pass rule (declared now).** Stage 1 passes only if **all** of the following hold:
(a) at least **two** model outputs are *compatible* (not partial) with observed series;
(b) those outputs jointly constrain the four worlds' distinguishing parameters (the school/
work/tutoring utility weights and the fixed parameters they differ in) — a single aggregate
moment cannot do this;
(c) a frozen training panel and a genuinely independent validation set can be formed from the
same compatible constructs (rules in §2) with at least **20 training countries** and **10
independent validation countries** after all overlap/missingness exclusions.

Otherwise the pilot **STOPS**, reports **"insufficient evidence"**, and no fitting,
synthetic-recovery, ABC or server draw is run. Partial/unmatched constructs are reported with
the exact data gap and what would be needed to close it; no proxy target is invented and the
pilot does not relabel a weak holdout as validation.

## 2. STAGE 2 — frozen split (only if Stage 1 passes)

- Freeze **before** seeing any comparative fit: the training panel (documented
  countries × period × construct set) and a **genuinely independent** validation set —
  disjoint countries, or later time blocks for the same constructs, declared in the run
  manifest and hashed.
- No observation, country or time block may be reused across train/validation. E1/Q2-derived
  observations must not be reused across splits; a Q2 pair may not be used for validation if
  either country was used in training.
- If the freeze leaves fewer than 20 training countries or fewer than 10 independent
  validation countries, report **insufficient evidence**; do not relabel a weak holdout.

## 3. STAGE 3 — synthetic-recovery challenge (only if Stages 1–2 pass)

- Generate pseudo-observed data from known worlds across multiple declared parameter/nuisance
  draws (minimum 8 nuisance draws/config), with a declared realistic noise/missingness model
  calibrated from the observed panel (never fitted to make recovery pass).
- Include the **shared-baseline/null** world and at least **one misspecified generating
  scenario**.
- Run the **entire frozen fitting + held-out decision** for every candidate world.
- Report: world-selection confusion matrix, false-distinction rate, false-equivalence rate,
  parameter coverage, and Monte Carlo uncertainty.
- **Declared pass rule:** recovery is adequate only if held-out world selection hits the
  correct world in ≥80% of simulated replicates with the diagonal dominating each row, and
  the false-equivalence rate is ≤0.10. If recovery fails, **STOP** before claiming any
  real-world discrimination.

## 4. STAGE 4 — bounded equal-budget rejection-ABC reconnaissance (only if Stage 3 passes)

- **Fitted parameterisation (declared now):** for candidate world `w`, parameters are (i) the
  eight nuisance parameters (`sigma_y, sigma_a, mu_y, mu_a, w_child, shadow_cost, f_pub_pre,
  y_sub0`) with priors uniform over the same ranges used by the corrected experiment's
  calibration record, and (ii) the world-strength `s ∈ [0.5, 2.0]` (uniform prior), with
  `theta_w(s) = theta_0 + s·Δ_w` exactly as in the audited model. The four worlds differ only
  in the direction `Δ_w`. No other parameters are fitted.
- **Discrepancy (declared):** weighted squared distance on the frozen, standardised moments
  (each moment divided by its observed cross-unit SD); equal weights unless the Stage 2
  freeze declares otherwise. All moments, weights and signs are frozen before any simulation.
- **Equal budget:** the **same number of simulated draws per world** (set only after the
  timing pilot in §6; never chosen per world). The tolerance is fixed by that budget — not
  tuned per world.
- Report: prior predictive checks, posterior predictive checks, prior-width sensitivity (two
  declared prior scales), tolerance sensitivity (two declared tolerance levels), Monte Carlo
  uncertainty, absolute discrepancy vs the pre-declared adequacy benchmark, and an explicit
  **cannot-fit** outcome. An adequacy benchmark is declared before the run (the absolute
  discrepancy level a model-free benchmark achieves on the same held-out moments, or a
  declared absolute RMSE-z threshold — whichever is declared in the Stage 2 freeze file).
- **No** ranking of theories from acceptance counts; **no** probabilities from acceptance
  proportions; **no** identification claims from prior width or posterior overlap.

## 5. STAGE 5 — model-free benchmark and paired predictive losses (only if Stage 4 runs)

- Frozen model-free benchmark: last-observation persistence and a regularised pooled
  predictor (ridge, tuning inside training only), declared before fits.
- Evaluate exact per-country / out-of-time predictive losses for each world and the benchmark
  on the validation set; report **absolute held-out fit** and **paired predictive-performance
  differences** with country-cluster-respecting bootstrap uncertainty (≥1,000 draws).
- Margins for any equivalence statement are declared in meaningful outcome units (percentage
  points of school/child-work shares) before seeing results; distinguish statistical
  indistinguishability from demonstrated equivalence. "Non-significant" alone is not
  equivalence.
- Allowed outcomes: a world fails adequacy; several fit comparably within the declared
  tolerance; one predicts better; insufficient power. All are reported, including poor fits.

## 6. Timing pilot (before any draw/cores commitment, only if Stage 1 passes)

A tiny kernel-through-moment timing pilot on region-42: run the audited model for one
representative country-slice, compute the frozen-moment pipeline, measure wall time, memory
and cores. Extrapolate the cost of the declared equal-budget ABC per world and report it
**before** committing draws/cores. **Stop and report** if the projected wall exceeds 60
minute-equivalents or requires more than 96 cores; do not promise a draw count in advance.

## 7. Compute, preservation and reporting

- All model/fitting compute on region-42 (`/root/miniconda3/bin/python`, NumPy backend,
  `REDESIGN_BACKEND=numpy`); no model compute on the Mac; no GPU number counts.
- Exact commands, start/end timestamps, code hashes, calibration/data hashes and logs are
  preserved; outputs written to fresh filenames only (never overwritten); failures preserved.
- Deliverables: this pre-registration (committed first), the audit code and a Stage 1 audit
  report, then — only if the gate passes — pilot code, a small region-42 run, results and a
  `RUN_REPORT.md` with per-stage pass/fail, numbers, cost and honest caveats.
- The pilot may stop at any stage; a stop is reported as the result. No confirmatory claims;
  no E1 comparison; no theory ranking.

## 8. Declared stop rules (summary)

| stage | stop condition |
|---|---|
| 1 | fewer than 2 compatible constructs, or no joint moment that constrains the four worlds, or fewer than 20 train / 10 validation units → **insufficient evidence**, stop |
| 2 | split too small or not genuinely independent → **insufficient evidence**, stop |
| 3 | recovery/confusion fails the declared criteria → stop |
| 4 | no fit below the declared adequacy benchmark at the equal budget → **cannot fit**, stop |
| 6 | projected cost above the declared budget → stop, report cost |

## Deviations log
- 2026-11-24: Stage 1 audit executed as a read-only inventory of committed repo data
  (`construct_audit.py`, file reading only). No model/fitting compute ran anywhere; the
  pre-registration's region-42 compute rule was therefore not engaged.
- 2026-11-24: **Stage 1 FAILED** (0 compatible, 4 partial, 7 unmatched model observables;
  no joint moment observing the school/work decomposition; no frozen split feasible).
  Per §8 stop rules, Stages 2–5 and the §6 timing pilot were **not launched**; no draws or
  cores were committed and region-42 was not used.
