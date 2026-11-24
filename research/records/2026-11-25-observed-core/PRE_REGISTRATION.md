# PRE-REGISTRATION — observed-core full-system model (task-42)

**Branch:** `research/observed-core-2026-11-25` (created from `origin/research/full-system-data-2026-11-25`
@ `34fd7c9`, the task-41 data-readiness map). **Record:** `research/records/2026-11-25-observed-core/`.
**Written before any model code was written and before any model was run.** The only prior step is reading
the task-41 data map. Owner: lit-verifier (repurposed; literature work stopped).

**What this is.** A bounded, honest *observed-core* model of the education/development system at country-year
level, built only from panels that actually exist, with every non-observed block declared as an assumption and
excluded from fitting. It is not a structural model of schooling, and no coefficient here is causal.

## 1. Why the core is what it is (from task-41 @ `34fd7c9`)

Task-41 established that of the seven system modules, only **macro/development** and **state/school supply**
are observed well enough to use without inventing a target. **Household demand/affordability, learning/quality,
gates/admissions, jobs/credentials and rural-urban migration** cannot be fitted from public data: the data are
gated (DHS IR), proxy-only (completion/transition for gates), or missing (migration flows, credential
requirements). The observed core is therefore:

- **observed and used**: enrolment, completion, pupil–teacher ratios, teachers, education spending (% GDP and
  per student), private-enrolment share, children in employment, urban share, GDP per capita, employment
  shares (structural change);
- **declared assumptions, not fitted**: learning/quality (latent), admissions gates (proxy only), jobs and
  credential requirements, internal migration flows, household borrowing/forgone earnings, school capacity
  (latent). Nothing in this record estimates these blocks or claims their parameters.

Shadow education gets **one short subsection of context in the report only**; it is not modelled.

## 2. Data, tiering and licences

All series are public World Bank WDI/EdStats API series (observed tier), retrieved by a committed script
(`scripts/fetch_wdi.py`) with retrieval timestamp, API URL, and `sha256` of every raw download and tidy file
in `data/MANIFEST.json`. No imputation, no interpolation, no back-casting. Missing cells stay missing and
reduce the estimation sample row-wise (availability reported).

Indicators (WDI codes; construct caveats from task-41 carried):
| role | series |
|---|---|
| outcomes | `SE.PRM.ENRR`, `SE.SEC.ENRR` (gross enrolment ratios; can exceed 100), `SE.PRM.CMPT.ZS` (primary completion; model-based), `SE.SEC.CMPT.LO.ZS` (lower-secondary completion; model-based) |
| supply | `SE.PRM.ENRL.TC.ZS` (primary pupil–teacher ratio), `SE.SEC.ENRL.LO.TC.ZS` (lower-secondary PTR), `SE.PRM.TCHR` (teachers), `SE.XPD.TOTL.GD.ZS` (education spending % GDP), `SE.XPD.PRIM.PC.ZS`, `SE.XPD.SECO.PC.ZS` (per-student spending, % GDP pc) |
| sector mix | `SE.PRM.PRIV.ZS`, `SE.SEC.PRIV.ZS` (private share) |
| demand/structural | `SL.TLF.0714.ZS` (children in employment — **not** child labour), `SL.AGR.EMPL.ZS` (agriculture employment share; ILO **modelled**, labelled), `SP.URB.TOTL.IN.ZS` (urban share — level, not migration) |
| macro | `NY.GDP.PCAP.KD`, `SP.POP.TOTL` |

Aggregates (regions, income groups) are excluded using the World Bank country endpoint (`region.value ==
"Aggregates"`). The country list and its vintage are saved with the data.

Known construct limits, stated up front and repeated in the report: GER ≠ net attendance ≠ completion;
completion is model-based, not exam pass; PTR is a headcount ratio, not effective teacher supply; children
in employment ≠ child labour; urban share is not migration; per-student spending has serious coverage gaps.

## 3. Model class (pre-declared)

A **reduced-form predictive panel system** at country-year level, not a structural model. Two horizons:

- **h = 1** (short-run): each outcome at year *t* predicted from the observed state at *t−1*.
- **h = 5** (massification horizon): each outcome at *t* predicted from the observed state at *t−5*
  (long differences of the same definitions).

Outcomes (6): primary GER, secondary GER, primary completion, lower-secondary completion, primary PTR,
lower-secondary PTR.

Each outcome has one equation, with predictors pre-declared in three nested sets:

- **Base:** outcome lag + ln GDP pc lag.
- **Supply:** Base + education spending (% GDP) + per-student spending at the matching level.
- **Full:** Supply + urban share + children in employment + agriculture employment share + (for completion
  equations) the corresponding enrolment lag; (for PTR equations) the corresponding enrolment lag.

Equations are estimated by country fixed effects + decade fixed effects on the pooled panel (within
transformation), OLS. A country's observations enter only where outcome and every predictor are observed;
no imputation. Estimation sample sizes and country coverage are reported per outcome and specification.

**Declared assumption block (never fitted):** learning/quality, gates/admissions, jobs/credentials,
migration flows, borrowing/forgone earnings, and latent school capacity are not estimated. Where the report
mentions them it says "assumed, not estimated".

## 4. Evaluation design (pre-declared before any run)

**Splits.**
1. **Leave-country-out, 5 folds.** Countries are assigned to folds by a fixed seeded permutation
   (`seed = 20261125`), stratified so that each fold has the same country count (±1); all years of a country
   are in one fold. A second country split, **leave-region-out** (6 World Bank regions), is run as a
   robustness split but is not used for the PASS/FAIL rule.
2. **Time blocks.** Train on years ≤ 2000, test on 2001–2012; and train on years ≤ 2010, test on 2011–2023.
   Test rows must have both the outcome at *t* and all predictors at *t−h* observed.

**Benchmarks** (each computed on the same test rows):
- **Persistence:** predict the outcome at *t* by its value at *t−h*.
- **Country trend:** per-country OLS linear trend fitted on the outcome over the last 10 observed years of
  the *training* period (minimum 3 points); if unavailable, falls back to persistence.
- **Pooled mean:** training-sample mean of the outcome at *t* (no country information).

**Metrics:** RMSE, MAE, and skill score `1 − MSE_model / MSE_benchmark` for both persistence and trend.
Uncertainty for the transmission regressions: country-clustered standard errors. For predictive comparisons
we report fold-level results and the share of folds in which the model wins; no significance testing of
forecast superiority is claimed.

**PASS/FAIL rule (pre-declared, applied per outcome × horizon).**
- **PASS** if skill vs persistence > 0 in **≥ 60% of leave-country-out folds** *and* overall skill vs
  persistence ≥ 0.05 *and* overall skill vs country trend ≥ 0.
- **WEAK** if it beats persistence by overall skill ≥ 0 but fails the trend condition or the fold-share
  condition.
- **FAIL** otherwise (at or below persistence on the pooled test rows).
Nulls and FAILs are reported; no outcome is dropped for failing.

## 5. Transmission (association) estimates

Separately from prediction, six pre-declared 5-year long-difference associations are estimated with country
FE and decade FE, country-clustered SEs, and labelled **associations, not effects**:

- T1 Δln GDP pc → Δ primary GER; T2 Δln GDP pc → Δ secondary GER;
- T3 Δ child employment → Δ primary GER; T4 Δ agriculture employment share → Δ secondary GER;
- T5 Δ education spending (% GDP) → Δ primary PTR; T6 Δ per-student primary spending → Δ primary completion;
- T7 Δ primary completion → Δ agriculture employment share (direction reported, not causal).

## 6. Multiverse over defensible specifications

For every prediction and transmission result, the following choices are varied **exhaustively** and all
results reported (no selection, no dropping inconvenient specs):

- fixed-effects structure: country only; country + decade; country + year; country + region×decade;
- lag/long-difference horizon: h = 1 and h = 5 (for transmission: 5-year differences and 10-year differences);
- functional form: levels; log outcome (where strictly positive); logit-transformed share (where within (0,1));
- controls: Base / Supply / Full nested sets above;
- benchmark set as in §4.

A qualitative conclusion (sign of a transmission coefficient; model-beats-persistence) is reported
**robust** only if it holds in ≥ 90% of the specification cells; 75–90% = **fragile**; below 75% =
**specification-dependent**. The report gives the full distribution and the median magnitude, not a single
chosen estimate.

## 7. Server, determinism, preservation

- Compute: `ssh -p 45973 root@connect.cqa1.seetacloud.com` (key only; **instance must not be shut down**),
  `/root/work/observed-core/`, `≤ 12` worker processes with `OMP_NUM_THREADS=1`; shared box, no other jobs
  touched.
- Determinism: fixed seeds (`20261125` for fold assignment; no stochastic estimator otherwise). Scripts write
  `results/*.json` and CSV tables with per-fold, per-spec rows.
- Provenance: `sha256` of every script, data file and result file in `results/MANIFEST.json`; exact commands
  and wall time in `results/RUN_LOG.txt`.
- Local smoke (`--smoke`, tiny sample) runs before the server run; failures are preserved and reported.

## 8. Honesty rules

- No causal claims, no "effect" language for any coefficient, no policy recommendation.
- No invented target; no fit to learning, gates, jobs, migration or borrowing blocks.
- Where the data cannot identify a mechanism, the report says so explicitly.
- Every model choice that is not observed is labelled a declared assumption.
- If the model fails the pre-declared benchmarks, that is the result.
- Shadow education is at most one contextual subsection; it is not modelled here.

## Amendment log

- No amendment yet. Any change after this commit is appended here with a date and the reason, and the run
  log records it.

---

## Amendment 01 — evaluation mechanics fixed before any model code or run (dated 2026-11-25)

Written before `scripts/observed_core.py` existed and before any model run. It fixes four mechanical
ambiguities in §3–§4; it does not change any PASS/FAIL rule, data source, or the declared-assumption block.

1. **Leave-country-out cannot use country intercepts.** For an unseen country there is no estimated country
   fixed effect, so LOO predictions use the same nested predictor sets estimated with **year and/or decade
   fixed effects but no country fixed effects** (pooled slopes). Country fixed effects are used in the
   time-block evaluation (countries are seen in training) and in the transmission regressions. This is the
   reason the prereg's FE multiverse is split by split type.
2. **Benchmarks by split.** Persistence, pooled-mean and country-trend are used everywhere the information
   exists. The country-trend benchmark is fitted per country on the last ≤10 observed training years
   (minimum 3 points) and is therefore available only for time-block splits; for LOO folds the trend
   benchmark is a **global linear year trend** fitted on the training sample. The pre-declared PASS rule
   "skill vs country trend ≥ 0" is read as "skill vs the available trend benchmark".
3. **Horizons.** h = 1 is one step ahead: each test year t is predicted from state t−1. h = 5 is one
   five-year step per training endpoint: T ∈ {2000, 2010}, predicting the outcome at T+5 from state at T,
   using training years ≤ T only. No recursive multi-step simulation is attempted (it would require
   imputing unobserved intermediate years, which §2 forbids).
4. **Time blocks.** h = 1: train ≤ 2000 → test 2001–2012; train ≤ 2010 → test 2011–2023. h = 5: the two
   single steps 2000→2005 and 2010→2015. h = 1 test years with unobserved t−1 predictors are dropped
   row-wise and counted.
5. **FE multiverse cells.** LOO: year FE / decade FE / region×decade FE. Time-block: country FE /
   country+year FE / country+decade FE. Transmission: country+decade FE (baseline) and country+year FE
   (robustness).

No other change.

---

## Amendment 02 — identified fixed-effect cells and transform details (dated 2026-11-25, before any model run)

Written before `scripts/observed_core.py` was executed. No PASS/FAIL rule or data source changes.

1. **FE cells must be identified on the test rows.** Some cells named in Amendment 01 cannot be estimated
   for out-of-period test rows (year/decade dummies for years not in the training block). The pre-declared
   FE multiverse is therefore:
   - LOO and leave-region-out folds (all years present in training): **no FE**, **year FE**, **decade FE**,
     **region×decade FE**.
   - Time blocks (future test years): **country FE**, **country FE + region FE**, **country FE + linear
     year trend**, **country FE + region-specific linear year trends**. (Continuous trends extrapolate;
     year/decade dummies would require an unseen level.)
   - Transmission: **country + decade FE** (baseline) and **country + region×decade FE** (robustness).
2. **Forms.** For every cell, three transforms are run and reported separately: (a) **level**; (b) **log**
   of the outcome (only cells where every training outcome > 0); (c) **logit** of the outcome/100 for
   share outcomes (clipped to (0.001, 0.999) on the training data; cells with no rows strictly inside the
   open interval are skipped and counted). Predicted values are back-transformed and clipped to the
   indicator's admissible range before scoring: enrolment ratios to [0, 150]; completion and PTR to
   [0, 100].
3. **Fold aggregation.** Fold-level and pooled-test results are both written. The pre-declared PASS rule is
   applied to the pooled test rows across the 5 LOO folds, together with the share of folds won; leave-
   region-out and time-block results are reported as robustness, not used for PASS/FAIL.
4. **Multiverse aggregation.** Robustness shares are computed over all *identified* cells for the outcome
   (any split, FE, controls, form) that produced a finite prediction, with N and skipped cells reported.

No other change.

---

## Amendment 03 — verdict aggregation and transmission details (dated 2026-11-25, before any model run)

Written before `scripts/observed_core.py` was executed.

1. **Aggregating the PASS/FAIL rule over the multiverse.** The §4 rule ("skill vs persistence > 0 in ≥60%
   of LOO folds, overall skill vs persistence ≥ 0.05, overall skill vs trend ≥ 0") is applied **per
   specification cell** (FE × controls × form) on the 5 LOO folds. The outcome×horizon verdict is then
   **PASS if ≥ 50% of LOO cells meet all three conditions**; **WEAK if 20–50%**; **FAIL if < 20%** (or if
   the pooled test skill is negative in the median cell). The cell distribution and median skill are always
   reported alongside the verdict, so the verdict never hides a fragile result.
2. **Transmission variables.** T1–T7 use 5-year and 10-year long differences of the named series, country FE
   plus decade FE (baseline) or country FE plus region×decade FE (robustness). T3–T7 additionally report a
   version controlling for Δln GDP per capita. Standard errors are clustered by country with the standard
   small-sample correction `G/(G−1) · (N−1)/(N−K)`; dummy coefficients are not reported, only the driver.
   A transmission sign is **robust** only if the pre-declared expected sign holds in ≥ 90% of cells with
   p < 0.05 in at least half of those; otherwise it is reported as fragile/uncertain. Expected signs:
   T1 +, T2 +, T3 −, T4 −, T5 −, T6 +, T7 − (T7 is reported as an association; no direction is claimed as
   causal and its sign is not used for PASS/FAIL).
3. **Skipped cells.** Cells with fewer than 200 training rows or fewer than 30 test rows are marked
   `skipped` with the reason and counted; they are not silently dropped. All cells, including skipped ones,
   appear in `results/predictive.csv`.

No other change.

---

## Amendment 04 — stronger trend benchmark for the LOO folds (dated 2026-11-25, before the full run)

Written after the local smoke run (2 cells, ger_primary/ger_secondary h=1) and before the full server
run. The smoke showed that a pooled global linear year trend is such a weak cross-country benchmark
(RMSE ≈ 19–24 vs model ≈ 4) that "skill vs trend ≥ 0" would be trivially satisfied, making the PASS rule
uninformative. The trend benchmark for LOO and leave-region-out folds becomes:

- **region-specific linear year trend**: pooled OLS of the outcome on year within the test country's World
  Bank region, fitted on the training rows only; fallback to the global pooled trend if the region has < 30
  training rows. Time-block folds keep the per-country trend (last ≤ 10 training observations, min 3,
  fallback persistence).

This makes the trend comparison harder, not easier, and it does not change the PASS thresholds (§4) or any
data source. It is the only change in this amendment.
