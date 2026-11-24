# PRE-REGISTRATION — X2 gate/tutoring inequality factorial + X4 honest-split aggregate test (task-28)

**Status: committed BEFORE code and before any run.** EXPLORATORY. X2 is SIMULATION ONLY on the
existing `eduengine` toy worlds (no engine edits, no country fit, no causal language; **rural
migration is not simulated** — rural is a household attribute + `rural_cost` + lower tutoring-firm
access). X4 uses **committed observed aggregates only, no simulation**; it is an aggregate,
exploratory prediction test, and must be allowed to return **INSUFFICIENT EVIDENCE** rather than
force a model–data match. Branch `research/masseng-staging-x2-2026-11-24`, additive from
`fef7428`. Engine (`engine/eduengine/`, `engine/worlds.py`) used unmodified.

Authorisation: task-28; experiments X2 and X4 from `research/records/2026-11-24-masseng-timing-audit/
audit_tables/next_experiments.json` (audit head `ff84e75`). Context from the audit: the original
staging experiment's quota−none lower/upper completion was ~0 pp vs bar +5.2/+6.2 pp (gate
arithmetic), and quota raised tutoring +21…+27 pp; X2 asks whether that is gate arithmetic or
inequality-relevant, and whether it is uniform across tutoring access/ban environments.

---

## 1. X2 — gate/quota × tutoring inequality factorial

**Engine/baseline (declared).** `worlds.make('formal_loop', seed=s, N=400, T=70, measure_from=35,
job_elasticity=0.0, gates=<bar|quota>, events=[], rural_firm_access=<a>, own_ban=<b>)`.
No sequenced interventions (stationary baseline); `job_elasticity=0` fixed to isolate the
gate/tutoring channel. Gates exactly as before:
`bar = [bar3.0, bar5.5, bar8.0, bar11.5]`;
`quota = [bar3.0, quota(share=.55,cut0=7.0), quota(share=.45,cut0=10.0), bar11.5]`.

**Factors.** gates {bar, quota} (2) × `rural_firm_access` {0.2, 0.4, 0.8} (3) × `own_ban`
{0.0 (off), 1.0 (full ban)} (2) × seeds 0–19 (2 × 3 × 2 × 20 = **240 runs**, ≈200 CPU-s).

**Metrics recorded per run.** All 13 standard scalars plus arrays; additionally
`tut_own_by_grade`, `tut_firm_by_grade`, `own_share`, `firm_price` (engine already reports them).
Derived, pre-declared:
- **gate-adjacent grades** = grades 6, 9, 12 (1-based; engine `ends=[6,9,12,16]`, gates at end of
  grades 6, 9, 12) → `tut_by_grade` indices 5, 8, 11 (0-based);
- **non-gate grades** = grades 4, 7, 10, 13 → indices 3, 6, 9, 12 (declared now; not re-selected);
- **wealth tutoring gap** = `tut_by_q[4] − tut_by_q[0]` (top minus bottom income quintile);
- **wealth completion gaps** for lower/upper/tertiary from the `completion_*_q` arrays (top−bottom);
- `parity_location_lower/upper` (rural/urban adjusted parity indices) as already reported.

**Pre-declared hypotheses, material thresholds, falsifiers (all paired by seed).**
Material threshold: **1 pp (0.01)** for tutoring levels/gaps; **1 pp** for completion/parity
differences; 90 % seed-bootstrap CI (4,000 draws) must exclude 0.
- **H1 (gate-prep):** at `own_ban=0`, quota gates raise tutoring relative to bar gates — overall
  `tut_rate` and the mean gate-adjacent grade tutoring. *Supported* if both are material-positive
  in **≥2 of 3** access levels. **Falsifier = quota does not raise gate-prep tutoring** (either
  quantity material-positive in ≤1/3 access levels, or material-negative anywhere).
- **H1b (ban):** `own_ban=1` reduces tutoring relative to `own_ban=0` (same gate/access; paired by
  seed), material-negative in ≥2/3 access levels for both gates. Falsifier otherwise.
- **H2 (inequality):** at `own_ban=0`, quota gates widen the top-vs-bottom tutoring gap relative to
  bar gates (material-positive quota−bar, ≥2/3 access levels). **Falsifier = quota does not widen
  the gap** (material-positive in ≤1/3 levels, or material-negative anywhere).
- **H3 (access gradient):** at `own_ban=0`, raising `rural_firm_access` from 0.2 to 0.8 reduces the
  wealth tutoring gap (material-negative in **both** gates). Falsifier otherwise; also report the
  three-level surface for non-monotonicity.
- **Gate-specificity (gate arithmetic vs broad):** difference-in-differences
  (quota−bar) on gate-adjacent minus non-gate grade tutoring, at `own_ban=0`, per access. If material
  positive, the quota effect is gate-concentrated (gate arithmetic); if not, it is broader — both
  outcomes reported, neither is a "win".
**Reporting:** full 2×3×2×metric surface with means and 90 % CIs, seed counts (+/−), and
leave-one-seed-out sign stability. **No selected cell is reported as "the" answer**; hypotheses are
judged only by the pre-declared multi-cell rules above. This answers the audit's question (is the
quota tutoring jump gate arithmetic or inequality-relevant?) on the declared metrics.

## 2. X4 — honest-split aggregate observed-data staging test (no simulation)

**Question.** Does a pre-registered, model-implied **education-vs-jobs ordering score** predict
subsequent lower-secondary completion gains out of sample, better than persistence and a pooled
trend? (The staging account implies education-led expansion should raise later completion more than
jobs-led expansion. This is an aggregate exploratory test of that implication — not a fit, not
causal evidence.)

**Data (committed only, no new pulls, no imputation).** `origin/research/massification-panel-2026-11-22`
@ **`7d25322e…`**: `sources/wdi_sweep/{prm_ner.json, wage_emp.json.gz, lsc.json, sec_ner.json,
emp_agri.json.gz, meta.json}`. National countries only (`meta.json` region ≠ "Aggregates",
3-letter ISO3). Unit: country × year; complete-case only.
- education expansion: **primary net enrolment rate** (`prm_ner`, UIS/WDI %);
- jobs/formalisation expansion: **wage-and-salaried employment share** (`wage_emp`, ILO-modelled %;
  declared structural-transformation proxy);
- outcome (primary): **lower-secondary completion** (`lsc`, %);
- robustness only: `sec_ner` (secondary net enrolment), `emp_agri` (agricultural employment share,
  used as −Δ as the alternative structural-transformation proxy);
- transition onset dates (`origin/research/transition-2026-11-23` @ `b13fde86…`) are **not** used
  in the ordering score — they date demographic (mortality/fertility) transitions, not
  education-vs-jobs ordering (declared construct mismatch); only descriptive correlation is reported.

**Windows and split (frozen now, before analysis).**
- Primary predictor window **1991–2004** with midpoint **1998**; primary outcome window **2004–2018**
  (14 years). Values matched with a maximum ±2-year tolerance; complete-case only.
- **Honest country split (deterministic, no outcome peeking):** the 197 national ISO3 codes with any
  `lsc` observation are sorted alphabetically; **every third (rank % 3 == 0) is validation**, the
  rest training. This gives **61 complete-case countries = 40 training / 21 validation** for the
  primary windows (declared from coverage before any outcome analysis; thresholds ≥20 train / ≥10
  validation are met). The split lists are written to the run manifest and hashed; no country is in
  both splits; no observations are reused.
- **Insufficient-evidence rule (binding, evaluated before modelling):** if complete-case counts were
  <20 training or <10 validation for the declared windows, X4 would **stop** and report
  INSUFFICIENT EVIDENCE; windows/split would **not** be re-chosen to force a match. (Coverage was
  checked to fix this design; outcomes were not examined.)

**Scores (pre-declared).**
- **Primary — timing-order score:** `ΔE_early = prm_ner(1998)−prm_ner(1991)`,
  `ΔE_late = prm_ner(2004)−prm_ner(1998)`; `ΔJ_early`, `ΔJ_late` analogously for `wage_emp`;
  `S_order = z(ΔE_early − ΔE_late) − z(ΔJ_early − ΔJ_late)`, where z-standardisation uses
  **training-country mean/SD only** (applied to validation). Positive = education expanded
  relatively earlier (education-led ordering).
- **Secondary — net-change score:** `S_net = z(ΔE_total) − z(ΔJ_total)` with Δ over 1991–2004,
  same training-only standardisation.

**Model and benchmarks (frozen specifications, no tuning).**
- Model: OLS on training countries: `Δlsc(2004→2018) = a + b1·S_order + b2·lsc(2004)`; pre-declared
  single specification; predictions on validation countries.
- Benchmarks: **persistence** (predicted Δlsc = 0); **pooled trend** (predicted Δlsc = training mean
  Δlsc). A country-specific prior trend is **infeasible on this honest split** (only 5 validation
  countries have `lsc(1991)`); this is declared and the pooled-trend benchmark is used instead.
- Losses: **MAE** primary, RMSE secondary, per validation country; paired differences
  model − benchmark; 4,000-draw bootstrap over validation countries (seed 20261125); 90 % CIs;
  report absolute losses, paired differences, and the training coefficient.

**Pre-declared decision rule.**
- **PASS (aggregate evidence for the staging implication):** model beats **both** benchmarks on
  validation MAE — mean paired difference <0 with 90 % CI upper bound <0 for persistence **and**
  pooled trend — **and** `b1 > 0` with 90 % CI excluding 0 in the expected direction.
- **FAIL / NO EVIDENCE:** any part of that criterion is unmet; report which and all losses.
- **INSUFFICIENT EVIDENCE:** the split/coverage rule above fails (it does not), or the declared
  windows cannot be formed completely; no window hunting.
**Robustness (reported, no decision authority):** `S_net` instead of `S_order`; window C
(predictor 1995–2005, outcome 2005–2019; 74 complete = 50/24); outcome `sec_ner` (41 = 23/18);
`emp_agri` job proxy (61 = 40/21). All reported with the same losses/CIs; none can flip the primary
verdict.

**Caveats (binding).** Aggregates only: no child-work 4-state decomposition, no tutoring/learning
measures, no age-specific enrolment, no mechanism identification; PHL-style post-1995 data were
inspected in earlier records, so this is retrospective and exploratory; no causal or confirmatory
claim; no E1 comparison.

## 3. Execution, preservation, analysis

- Region-42 only for model runs (X2) and for the X4 statistical analysis; X4 input is a committed,
  deterministic derived panel extracted from the committed WDI/UIS cache (extraction script and
  provenance committed).
- Commands, start/end times, host, worker count (≤20), code hashes (driver, `engine/worlds.py`,
  `engine/eduengine/*.py`), input-data hashes, split lists and seed-level rows are preserved.
  Fresh output files only (exclusive creation); never overwrite.
- Analysis scripts are committed with the results; all outputs and a `RUN_REPORT.md` are committed
  and pushed. No causal language; no p-value-based claims; no ranking of theories.
- Stop rules: engine import failure or >2 % non-finite metrics → stop and report traceback; X2 wall
  >15 min → preserve log and report; X4 fires the insufficient-evidence rule if counts fall below the
  declared minimum (checked before modelling).

## Deviations log
- 2026-11-24 (X2): ran once as declared: 240 runs, `elapsed_s=24.549`, results hash preserved.
- 2026-11-24 (X4 robustness-count clarification, BEFORE the successful run): the pre-registered
  robustness note for window C quoted 74 complete = 50/24 from a coverage check that did not yet
  require the 1998 midpoint that the declared S_order formula needs; with the declared timing
  score the window-C robustness sample is 72 complete = 49/23. Primary windows/split/scores/
  decision rule are unchanged; window C is robustness-only (no decision authority). The S_net
  robustness spec uses endpoint years only (1991 and 2004), as declared (63 complete = 41/22).
- 2026-11-24 (X4 run 1, NO RESULTS): the first X4 execution failed immediately with
  `KeyError: 'lsc_2004'` because the analysis code looked up panel keys named after the outcome
  variable label (`lsc_*`) while the committed extraction names outcome columns `out_*` /
  `out_alt_*`. This is a column-name bug in the analysis code, not a design/coverage failure: no
  model was fitted, no loss was computed, no result exists. The traceback is preserved in
  `x4_v1_failure.log`. Fix: analysis now refers to the panel's outcome columns (`out_*` for the
  lsc primary outcome, `out_alt_*` for the sec_ner robustness outcome); windows, split, scores,
  benchmarks, thresholds and decision rules are unchanged. X4 rerun as `results_x4.json` with the
  failure log kept.
