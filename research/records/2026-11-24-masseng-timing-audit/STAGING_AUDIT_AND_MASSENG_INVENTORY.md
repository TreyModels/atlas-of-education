# STAGING AUDIT AND MASSENG INVENTORY (task-26)

**Status: read-only independent audit + inventory, 2026-11-24. SIMULATION ONLY. No causal
claims. No Codex branch was rewritten; no staging run was re-executed; the engine was not
edited. The only server interaction was read-only provenance verification (SHA-256 of files
already on region-42) and a status snapshot of the active Bayesian screens — no compute was
launched by this audit.**

Machine-readable tables: `audit_tables/` —
`staging_audit.json` (independent recomputation from the committed `full.json`),
`engine_inventory.json`, `dataset_catalog.csv`, `runner_catalog.csv`,
`next_experiments.json`, `verification.json`.
Audited branch: `research/codex-masseng-staging-2026-11-24` @ **`bac3a7c`**.

---

## 0. Provenance verified before reading results

| item | evidence |
|---|---|
| audited branch / commit | `research/codex-masseng-staging-2026-11-24` @ `bac3a7c` |
| DESIGN recorded before results | `git` history: `c435fa2` (2026-11-24 20:46:01 +0800) adds **DESIGN.md + run_staging.py**; `bac3a7c` (20:48:13) adds **results/full.json + Bayesian pilots**. Design precedes results in the record. |
| committed == server SHA-256 | `results/full.json` `69129f47…` (both); `DESIGN.md` `7d9ad7b8…`; `engine/worlds.py` `2e9ec71a…`; `engine/eduengine/core.py` `2b7484a9…`; `codex_bayes/run_screen.py` `48dec650…`; `model/masseng/engine5.py` `e01bd543…` — **all match** between the committed branch and `/root/work/masseng-staging-codex-20261124/`. |
| claimed design | 160 runs, 400 children/cohort, 70 years, 10 seeds, 16.5 s — **verified against `full.json`** below |

---

# PART A — AUDIT OF THE STAGING EXPERIMENT

## A1. Design/config verification (all claimed values confirmed)

| claim | actual in `full.json` | verdict |
|---|---|---|
| 160 runs | `len(rows) = 160`; grid = 4 schedules × 2 feedback × 2 gates × 10 seeds; every cell has seeds 0–9 | **PASS** |
| 400 children/cohort | `config.cohort_N = 400` | **PASS** |
| 70 years | `config.years = 70`; annual series length 70 | **PASS** |
| 10 seeds | `config.seeds = [0..9]` | **PASS** |
| 16.5 s | `elapsed_s = 16.499` | **PASS** |
| schedules/interventions | `none`; `school_first` (edu @15, jobs @30); `jobs_first` (jobs @15, edu @30); `simultaneous` (@15/15); values edu_share 0.18→0.30 and vac0 0.08→0.16 | **PASS (160/160 row event logs match the declared schedules and values)** |
| measurement | code: `T=70, N=400, measure_from=35`; engine SDG4 scores cohorts `measure_from … T−26`, i.e. cohorts 35–44 ("cohorts 35–44") | **PASS (verified from code)** |
| no country enrolment anchors | `run_staging.py` passes no `enrol_targets`; engine default `{}` | **PASS** |
| summary reproduces | recomputed all 4 conditions × 4 schedules × 13 scalars from raw rows: **max abs difference from stored summary = 0.0**, 0/208 mismatches | **PASS** |
| data hygiene | annual series: 70-length, keys `year,formal_share_gdp,edu_budget,q_pub,tut_rate`, **0 missing entries**; metrics: **0 None**; no non-finite values retained as None | **PASS** |

**Gaps in the record (not errors, but reproducibility limits):** no worker count, machine,
package/library versions or code hashes inside `full.json` (the 16.5 s is not reproducible from
the JSON alone); the engine's internal `event_log` is not exported beyond the per-row `events`;
the stored summary computes **only two contrasts** (school_first−jobs_first; simultaneous−none)
with bootstrap CIs — the DESIGN-requested **quota-vs-bar** comparison and the feedback
comparison are only present as separate group means, with **no contrast or CI**. This audit
recomputed them (below).

## A2. Recomputed headline comparisons (independent implementation; seed-level paired differences, 4,000-draw seed bootstrap, seed 20261125)

### (i) Early school-funding vs early jobs (`school_first − jobs_first`)

| condition | completion_lower | completion_upper | completion_tertiary | formal_share_gdp | tut_rate | q_pub |
|---|---|---|---|---|---|---|
| feedback 0, bar | **−0.56 pp** [−1.36, +0.21], 6/10 seeds negative, not sign-stable | −0.20 pp [−0.77, +0.38] | −0.53 pp [−1.30, +0.18] | **−5.37 pp** [−5.68, −5.05] sign-stable | +0.46 pp [0.32, 0.60] sign-stable | −2.11 pp sign-stable |
| feedback 0, quota | +0.035 pp [−0.005, +0.078] | +0.023 pp [0.000, 0.050] | +0.045 pp [−0.24, +0.36] | **−5.18 pp** sign-stable | −0.32 pp [−0.68, +0.02] | −1.58 pp sign-stable |
| feedback 1, bar | −0.13 pp [−0.83, +0.60] | +0.39 pp [−0.22, +0.96] | +0.52 pp [0.08, 1.00] | **−5.44 pp** sign-stable | +0.49 pp sign-stable | −1.60 pp sign-stable |
| feedback 1, quota | +0.002 pp [−0.010, +0.015] | −0.007 pp [−0.025, +0.005] | +0.14 pp [−0.33, +0.62] | **−4.84 pp** sign-stable | +0.05 pp [−0.19, +0.31] | −1.34 pp sign-stable |

- Completion differences are **small (|Δ| ≤ 0.6 pp) and not sign-stable across seeds** (only
  3–4 of 13 metrics are sign-stable in each condition; per-seed signs flip). The statistically
  stable quantities are the **mechanical/engine-identity** ones: `formal_share_gdp`,
  `q_pub`, `edu_gdp`.
- **Why this contrast cannot be read as "timing": the arms are not exposure-matched.**
  Cumulative exposure arithmetic (70 years, declared events): `school_first` = +6.6
  education-share-years and +3.2 vacancy-years vs `none`; `jobs_first` = +4.8 education-share-years
  and +4.4 vacancy-years. So relative to `jobs_first`, `school_first` has **+1.8 education-share-years
  and −1.2 vacancy-years by construction**. In addition the fiscal loop endogenises education
  spending: because earlier formal jobs raise tax revenue earlier, mean total education budget is
  **higher** under `jobs_first` (mean-seed sum 41,818) than `school_first` (38,183; +9.5%), and
  43,363 under `simultaneous`. The contrast therefore mixes order, cumulative dose and
  endogenous revenue feedback.
- The engine also lags the fiscal channel: fiscal revenue is turned into the school budget in the
  **next** model year, while vacancies act in the **event year** (verified in `eduengine/core.py`:
  labour market → `FiscalState.after` → budget used by `PublicSchools` next year). So even
  "simultaneous" is **not simultaneous in effect**. DESIGN states the lag; it does not remove it.

### (ii) Quota gates vs absolute bar gates (`quota − bar`, paired by seed)

| metric (across schedules/feedback) | mean difference | seed-stability |
|---|---|---|
| completion_lower | **−0.171 to −0.201** (≈ −17 to −20 pp) | sign-stable in all displayed cells |
| completion_upper | strongly negative in most cells | sign-stable |
| tut_rate | **+0.21 to +0.27** (≈ +21 to +27 pp) | sign-stable |
| q_pub | negative | sign-stable |
| parity_wealth_lower | mixed sign | **not sign-stable** (5/10 each side in several cells) |

These are **structural by construction**, not estimated effects: the quota gates define seats as
a planned share of the cohort (0.55 at the lower gate, 0.45 at the upper gate), so measured
lower/upper completion is mechanically capped; and gate-prep tutoring demand is a built-in
tutoring motive. Evidence: under quota gates `simultaneous − none` is **−0.008 pp
(completion_lower), −0.010 pp (completion_upper)** — essentially zero — whereas under bar gates
it is **+5.2 pp / +6.2 pp**. The "quota vs bar" result is therefore a statement about the gate
rules' arithmetic, not an empirical finding.

### (iii) Education-to-jobs feedback (`job_elasticity 1 − 0`, paired by seed)

- `formal_share_gdp` rises **+0.033 to +0.084** (3.3–8.4 pp), sign-stable in every cell.
  This is the assumed functional form: vacancies are multiplied by
  `(educated share / reference)^elasticity` (verified in `eduengine/modules/labour.py`). It is
  **not an estimate of jobs created by education**; it is the model's assumption.
- Completion effects are small (+0.000 to +0.029 depending on gates/schedule) and are
  sign-stable under bar gates but ~0 under quota gates.
- Conclusion: feedback results are **conditional on the assumed elasticity form and value**;
  they cannot be read as evidence about real economies.

### (iv) Jointly early vs neither (`simultaneous − none`)

Sign-stable and CI-excluding-zero in almost all cells: bar gates +5.2 pp lower / +6.2 pp upper /
+1.1 pp tertiary completion; formal GDP share +16.7 to +17.6 pp; tutoring −3.2 pp (bar) but
+4.2 pp (quota); wealth parity +3.1 to +4.4 pp. This is the cleanest contrast in the experiment
(both interventions vs neither), but it is still a synthetic model contrast, not a historical
or causal statement.

## A3. Seed-level uncertainty and seed sensitivity

- Within-cell between-seed SD is small for levels (e.g. completion_lower CV ≈ 1.0–1.6%;
  formal_share_gdp CV ≈ 1.6%; q_pub CV ≈ 0.3%), but much larger for equity ratios
  (parity_wealth_lower CV ≈ 16%).
- **Schedule ranking on completion is seed-sensitive**: across the 10 seeds there are **5–7
  distinct orderings** of the four schedules for `completion_lower` (7 under quota gates),
  4–6 for `completion_upper`, 5–7 for `completion_tertiary`. The ordering of
  `formal_share_gdp` is stable (1–2 distinct orderings; jobs-first/simultaneous above
  school-first/none) and `q_pub` is essentially fixed (1 ordering in most cells) — again
  mechanical/engine-identity quantities.
- Contrast sign-stability counts (13 metrics): `school_first−jobs_first` **3–4/13**;
  `simultaneous−none` **9–13/13**; quota−bar **8–11/13**; feedback **3–8/13**.
- Conclusion: **the headline "which sequence is better" comparisons on completion are not
  robust to the 10-seed Monte Carlo**; the robust differences are the mechanical ones. The
  DESIGN's instruction to report seed bootstrap uncertainty is satisfied, but the two
  reproduced contrasts are not described as seed-sensitive anywhere in `full.json`.

## A4. What is mechanical by construction / not causal (explicit)

1. **Early jobs mechanically raises cumulative job opportunities**: vacancies are
   `vac0 × (1+vac_growth)^t` with `vac_growth=0`; an earlier `vac0` event yields +1.2 vacancy-years
   in `jobs_first` relative to `school_first` over 70 years. Any formal-share/jobs difference
   from the order contrast includes this dose.
2. **Early school funding mechanically raises cumulative education-share exposure** (+1.8
   share-years for `school_first` vs `jobs_first`), and the **fiscal feedback** more than offsets
   it in budget terms (jobs-first has the higher cumulative budget).
3. **One-year fiscal lag** makes "simultaneous" asymmetric (education effective next year,
   vacancies same year).
4. **Quota gates mechanically cap completion** (planned seat shares) and mechanically create
   gate-prep tutoring demand; bar-vs-quota differences are the gate arithmetic.
5. **`job_elasticity` feedback is an assumption**, not an estimated jobs-creation effect.
6. **Time order is not causal evidence**: the schedules are stipulated changes in a synthetic
   model; there is no identification, no exogenous variation, no empirical fit, and the DESIGN
   says so explicitly ("stipulated changes, not observed dates or plausible real-world effect
   sizes").
7. **Rural migration is not simulated.** Rurality is a household attribute (`urban` flag) plus
   an extra schooling cost (`rural_cost=0.03` beyond primary) and lower tutoring-firm access
   (`rural_firm_access=0.4`); **no migration, remittances, spatial job access, or rural-urban
   composition change is modelled.** What this omits: urbanisation as a massification channel,
   rural–urban sorting, migrant networks, remittance-financed schooling, and the changing
   returns to education across locations. Any rural/urban result is a within-fixed-population
   comparison.

## A5. DESIGN vs code vs JSON — consistency summary

**Consistent:** design question/status labels; grid; interventions and values; gate sets;
measurement cohorts; no anchors; bootstrap over seed-level differences; matched-seed caveat;
"no causal/historical claim"; "not fitted to a country"; "migration is not simulated";
"tutoring spike conditional on rules"; failures/None policy (none occurred).
**Inconsistent/incomplete (flagged):** (i) quota-vs-bar and feedback comparisons are asked for
in DESIGN but no contrast/CIs are stored (only group means) — recomputed here; (ii) no
worker/machine/version/hash provenance in the result JSON; (iii) no seed-sensitivity summary
(the completion rankings are seed-sensitive — see A3); (iv) single 160-run record, no
independent replication; (v) `event_log` minimal; (vi) the fiscal-lag asymmetry, while stated,
means "simultaneous" is mislabelled; (vii) the run's timing claim (16.5 s) is machine-dependent
and not reproducible from the JSON.

## A6. What the experiment does **not** implement (per DESIGN, confirmed in code)

No fit to a country; no observed dates or effect sizes; no migration; no tutoring costs or
distribution data; no employer credential-requirement data; no school-quality measurement; no
DHS/observed matching; no cross-country place comparison. These are appropriate limitations for
a mechanism-timing **illustration**; they are not a historical account.

---

# PART B — MASSENG / TIMING INVENTORY

## B1. Which engine is which (paths and status)

| engine | path | what it is | status |
|---|---|---|---|
| **eduengine** modular ABM | `engine/eduengine/` + `engine/worlds.py` | children/households/schools/labour/fiscal/tutoring ABM with gates, quality, shadow education, queues, SDG4 measurement layer; used by the audited staging experiment (`worlds.formal_loop`) | **toy/uncalibrated** ("worlds are abstractions, not countries") |
| **MASSENG v5** portable national cohort model ("v5 R1" = `model/outputs/PHL/v5/fit_R1.json`) | `research/masseng-v6/model/` (`masseng/engine.py`, `engine5.py`, `calibrate.py`, `calibrate5.py`, `targets.py`, `data.py`, `readiness5.py`; `PROTOCOL*.md`; `countries/{HKG,KHM,PHL}`; `outputs/PHL/v1..v5`, `outputs/KHM/v3`) | deterministic cohort-flow/demand model fitted to country data: births→Grade1→primary(6)→secondary(3)→upper-secondary(3)→tertiary(4), income deciles, public/private, demand engine (b_h premium, b_p positional, b_r formal/relational floor, lam), supply/financing inputs | **fitted for PHL (v1–v5) and KHM (v3)**; retrospective/inspected; the model the active Bayesian screens use |
| **MASSENG v6 Phase 1** prototype | `research/masseng-v6/masseng_v6/` (`core/state.py`, `core/ledger.py`, `core/runner.py`, `education/admissions.py`, `education/institutions.py`) | conserved probability-mass cohorts with orthogonal education/work status, EntryFunnel Q≥L≥E≥R, joint admission markets | **accounting prototype only**; not calibrated; not full country-year simulation |
| legacy `engine/` worlds | `engine/{childworld.py,camchild.py,floorworld.py,impute/,experiments.py,mc.py,...}` | childworld (school-and-work cross-country MC), camchild (Cambodia two-region child labour), floorworld (education→industrialisation), imputation system | auxiliary/archived; not the current MASSENG line |
| staging experiment | `engine/experiments_codex_sequence/` | eduengine scenario grid, 160 runs | audited here |
| Bayesian screen | `research/masseng-v6/experiments/codex_bayes/` | importance screen on v5 R1 (4 mechanism parameters) | pilots committed; 4,096-draw runs active on region-42 |

## B2. State variables and stage transitions

- **v5 R1:** cohorts × income decile × public/private; 16 grades across primary/secondary/
  upper-secondary/tertiary; statuses: new entrant, enrolled, repeater, deferred/qualified-
  waiting (tertiary deferral), completer, out-of-school; demand utility with 4 fitted mechanism
  parameters; supply/financing (capacity, vouchers, fees, subsidies, free tuition, cycle rules)
  as inputs; drivers: cohort size, age/cycle rules, wage premiums, formal employment share,
  dated policies. **No region/rural dimension, no migration, no learning/quality, no tutoring;
  employer credential queues are proxied by a formal-share relational driver.**
- **eduengine:** child-level state (cohort, grade 1–16, learning in grade-equivalents,
  credential, attendance, ability, home, income, urban); gates bar/quota; public/private
  schools; fiscal state (tax→education share); labour queue with credential floors, vacancies,
  informality, optional education→jobs feedback; tutoring market (own-teacher buy-back, gate
  prep, remedial; rural firm access); SDG4 measurement layer. **No migration.**
- **v6 Phase 1:** typed probability mass by cohort/decile/region/stage/grade/sector with
  orthogonal education status (attending/repeating/qualified_waiting/out_of_school_reenterable/
  completed/exit_terminal/alternative) and work status (none/part-time/full-time/seasonal);
  conserved entries/exits; joint admissions with capacity reservations. Behaviour, quality,
  tutoring, migration not yet implemented.

## B3. Feature coverage against the full-MASSENG agenda

| agenda component | v5 R1 | eduengine | v6 Phase-1 |
|---|---|---|---|
| all levels (primary→tertiary) | yes | yes | yes (stages) |
| state supply vs household demand | supply/financing inputs; demand fitted | yes (modules) | admissions funnel only |
| rural out-migration | **no** | **no** (rural attribute/cost only) | region field only, no flows |
| formalisation/jobs vs credential competition | formal-share driver; no employer queue | yes (queues, credential floors) | not yet |
| quality & shadow tutoring at gates | **no** | yes | **no** |
| heterogeneity over time | cohorts × deciles | cohorts × income/urban/ability | cohort×decile×region×status |

## B4. Datasets (full catalog in `audit_tables/dataset_catalog.csv`)

Highlights (path, coverage, vintage, limitation):
- **WDI/UIS/ILO sweep** (`origin/research/massification-panel-2026-11-22`): 60+ country-year
  series; primary GER 207 countries 1970–2022; net enrolment 197/188; lower-secondary
  completion 197; harmonized test scores 172 countries **2010–2020 only**; ILO/UCW child
  employment **100 countries, 281 obs, 1994–2016, median 2 obs/country**. Vintages mixed.
- **E1 multiverse**: derived 272-link outputs only; raw WDI panel not committed; 179 countries,
  1940–2025.
- **Q2 / Transition long-run panel**: 197 countries, 1750–2024, 42,959 rows (mortality, life
  expectancy, fertility, schooling attainment, Maddison GDP, urban share); reconstruction/
  splice caveats; onset dates for mortality/fertility decline.
- **DHS API cache**: 76–87 countries, 1985–2025, 369 surveys (fertility, women's education,
  median age at first birth, mean CEB by education); no microdata; no child-labour/enrolment/
  tutoring cells.
- **DHS CEB by education**: 14 countries, 318 rows.
- **Shadow-education hand collection**: 6 countries/sites, 38+20 rows, case studies.
- **asia_school_work**: 21-country cross-section, mixed years.
- **Staging results** (160 runs) and **Bayesian pilots** (2×256 draws) as above.
- **MASSENG v5 fits/protocols** and **massification-panel sweeps** (takeoff, sweep, lead-lag,
  fee-abolition event study, Bayesian model averaging; child-work B3).

## B5. Runners (full catalog in `audit_tables/runner_catalog.csv`)

Measured costs where available: staging **160 runs / 16.499 s** (~0.83 CPU-s/run; workers not
recorded); E1 **5,426.8 s on 8 workers** for 1,200 draws (4.52 s/draw effective); Bayesian 256-
draw pilots at 4 workers (elapsed not recorded); **4,096-draw main+expanded screens active on
region-42 at audit time** (see B7). Others: v5 least-squares calibration, Q2 pair audit,
massification-panel scripts, engine5 array runner, v6 Phase-1 tests, transition onsets, GPU-suite
ABC.

## B6. Known construct mismatches (consistent with the earlier fitted-worlds Stage-1 audit)

The observed panels do **not** contain the model's school/work/tutoring/quality decomposition:
GER (gross) vs the model's participation share; net enrolment is age-specific while the models
have no age variable; ILO/UCW child employment is 7–14 (and only the total is committed — no
study-and-work/work-only split; hidden work is unobservable); test scores (0–625/HCI) vs the
models' internal learning scale (assumed for eduengine SDG4); tutoring only as 6-country case
studies; income as country GDP vs model units; migration absent in models **and** panels; employer
credential requirements not measured. These are why the earlier fitted-worlds pilot stopped with
"insufficient evidence" and why any observed-data staging test here must be labelled exploratory
and aggregate-only.

## B7. Verification and active-run status (read-only snapshot, 2026-11-24T12:55:31Z)

- All committed staging code/results and the server copies match SHA-256 exactly (see §0).
- **Active Bayesian screens (owned by Lead/Codex; not touched):** main 4,096 draws (seed
  20261125, prior main) shells 18115/18116 and expanded 4,096 draws (seed 20261126, prior
  expanded) shell 18162, 24 workers each, launched 12:49Z; both were **running** at the snapshot
  (~6 min elapsed; 53 `run_screen` processes observed). Output JSONs are written only at
  completion and were absent. `server_expanded_4096.log` shows repeated
  `RuntimeWarning: overflow encountered in exp` in `engine5.py:63` (the logistic overflow Codex
  flagged) — extreme-draw numerical behaviour must be inspected before interpreting expanded-
  prior weights. Committed 256-draw pilots: ESS **5.94** (main) / **1.77** (expanded), holdout
  GER RMSE **9.645 / 7.065** vs persistence **6.600** — under-resolved and worse than the naive
  benchmark; they are conditional importance weights, **not a posterior**.
- **Do not shut region-42 down while these are active.** This audit launched nothing and
  overwrote nothing.

---

# PART C — FIVE HIGHEST-VALUE EXECUTABLE NEXT EXPERIMENTS (proposals; none run)

Full machine-readable detail in `audit_tables/next_experiments.json`. Cost estimates use the
measured eduengine throughput (~0.83 CPU-s/run) and the staging grid.

| # | experiment | design in one line | pre-declared falsifier | cost estimate |
|---|---|---|---|---|
| **X1** | **Exposure-matched sequencing test** | 6 arms: none / school-first / jobs-first / simultaneous + two **dose-matched** arms (equal total education-share-years and vacancy-years, order only differs) + calendar-shift placebo; 6×2 feedback×2 gates×20 seeds = 480 runs | if the matched order contrast ≈0 while unmatched is large → the staging "timing effect" is cumulative exposure, not sequencing | ~400 CPU-s; **<1–5 min** wall on 24–48 workers |
| **X2** | **Gate/quota × tutoring inequality factorial** | bar vs quota gates × tutoring access (rural_firm_access 0.2/0.4/0.8) × own-teacher ban; outcomes by level, wealth quintile, rural/urban; 240 runs | if quota gates do not raise gate-prep tutoring and widen the top-vs-bottom gap (sign+CI) → the gate/tutoring channel does not reproduce the claim | ~200 CPU-s; **<1 min** |
| **X3** | **Feedback-elasticity robustness surface** | job_elasticity ∈ {0,.25,.5,.75,1} × 4 schedules × 2 gates × 20 seeds = 800 runs; full contrast surface | any order conclusion that reverses across the elasticity grid is not robust; no post-hoc selection | ~660 CPU-s; **1–2 min** |
| **X4** | **Observed-data staging/ordering test with honest splits (aggregate only)** | pre-register a model-implied ordering score on WDI/UIS + transition onsets; leave-country-out + time-block validation; paired losses vs persistence/trend with country-cluster bootstrap CIs | if the ordering score does not beat both benchmarks on held-out countries → no aggregate support; report as such | panel regressions only; **minutes**; no simulation |
| **X5** | **Bayesian screen validation + synthetic parameter recovery** (coordinate with Lead; do not duplicate active runs) | synthetic recovery of known b_h,b_p,b_r,lam, ESS/max-weight diagnostics, ≥2 seeds, prior/tolerance sensitivity, posterior-predictive coverage; no posterior claims | if recovery fails or ESS stays very low at the declared budget → screens unusable; no mechanism claim | needs one measured 4,096-draw screen wall first; budget **≤1 h server time** at 24 workers; do not promise draw counts before the timing measure |

**Why these five.** X1 fixes the audit's central confound (exposure vs order) at negligible
cost; X2 addresses the gate/tutoring/inequality mechanism the full-MASSENG agenda names; X3
tests whether any timing conclusion survives the most arbitrary structural assumption; X4 is
the only honest path to observed data and is deliberately aggregate-only; X5 is the
prerequisite for any Bayesian claim and is already partially in flight. All are bounded,
pre-declarable, falsifiable, report every cell, and use honest splits (X4) or synthetic
known-answer designs (X1–X3, X5). None treats association or fitted trajectories as causal
proof.

---

# PART D — Caveats

1. **Simulation only.** The audited experiment is a synthetic mechanism illustration; no result
   here is empirical evidence about any country.
2. **No causal language.** Time order in a stipulated synthetic scenario is not causal evidence;
   the experiment's own DESIGN says this.
3. **No branch rewrites, no re-runs, no engine edits.** The audit recomputed from the committed
   `full.json`; the only server actions were read-only hashes and a process/status snapshot.
4. **Seed sensitivity is material** for completion-based conclusions (5–7 distinct schedule
   orderings across 10 seeds; only 3–4/13 metrics sign-stable for the order contrast).
5. **The Bayesian screens are not a posterior** and are currently under-resolved (ESS 5.94/1.77
   at 256 draws; 4,096-draw runs in flight); overflow warnings on the expanded prior must be
   inspected.
6. **Construct mismatches** remain the binding constraint on any observed-data MASSENG test
   (see B6 and the earlier fitted-worlds Stage-1 audit).
7. **Preserve everything.** No committed file was modified; no existing output was overwritten;
   active jobs were not touched.

## Files and hashes (this record)

- `STAGING_AUDIT_AND_MASSENG_INVENTORY.md` (this file)
- `staging_audit.py` → `audit_tables/staging_audit.json`
- `build_inventory.py` → `audit_tables/{engine_inventory.json, dataset_catalog.csv, runner_catalog.csv, next_experiments.json, verification.json}`
- audited commit `bac3a7c` on `research/codex-masseng-staging-2026-11-24`; audit branch
  `research/masseng-timing-audit-2026-11-24`.
