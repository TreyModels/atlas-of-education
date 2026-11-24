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
