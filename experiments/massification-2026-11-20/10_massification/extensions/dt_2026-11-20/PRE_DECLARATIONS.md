# PRE-DECLARATIONS — DT1–DT5 test battery (brief 020)

**Worker:** DT (DT1–DT5 battery)
**Programme root:** `/Users/treymenefee/massification_live/experiments/massification-2026-11-20`
**Write scope:** `10_massification/extensions/dt_2026-11-20/` only. All inputs are read-only.
**Authority:** D102 (paper-status ruling), D103 (DT1–DT5 slate adopted), D104 (integration ruling + binding
conditional gate), D105 (falsification reach), D89 (standing order: 5 anchored experiments, 7-field blocks,
drop-first named). Anchoring blocks: `08_council/brief_020/SYNTHESIS_020.md` §C.
**Status: FROZEN — written before any run. No threshold changes after results.**

> **Predeclaration discipline.** This file was written before `code/run_dt.py` was executed on any test. Its
> sha256 is recorded in `RUN_MANIFEST.json`. The five anchoring blocks in §1 are copied **verbatim** from
> `SYNTHESIS_020.md` §C (programmatic line-slice, not retyped). §3 adds only the **operationalizations** the
> blocks leave implicit (estimator, aggregation, eligibility, missing-data rule); it does **not** change any
> threshold, discriminating action, or falsifier. Every operationalization below was fixed before the first run.
> Where a test cannot be reached on disk, the frozen rule is DATA LIMITED / UNABLE — never a fabricated number.

---

## 0. Scope, labels, and closed claims

- **Labels only:** `OBSERVED` (raw on-disk observed series), `DERIVED` (a statistic computed from observed series),
  `HELD` (named series that does not exist on disk — never fabricated). **No toy, no simulated, no synthetic.**
- **No causal claim, no direction claim (R13-safe).** Every DT statistic is associational/descriptive. A DT PASS is
  a descriptive association; it is **not** validation of either paper and **not** evidence that the model
  "reproduces induction" or "reproduces hysteresis".
- **No C1–C4 reopening.** Nothing here reopens the closed claims; DT5 explicitly does **not** re-score WT2/WT4.
- **No external data, no web, no external message, no writes outside this directory, no touch of the running server.**
- **No HELD series is read, imputed, proxied, or fabricated.** DT3 is design-only (see §3.4) and its behavioural
  outcomes are recorded as UNABLE. Anthropometric series, adoption/migrant panels, and reform/behavioural data are
  HELD and are not touched by `run_dt.py`.

### Inputs (observed only; read-only)

| path | used by | status |
|---|---|---|
| `09_relations/data/panel_wdi_long.csv` (long: `iso3,country,indicator,year,value`) | DT1, DT2, DT4, DT5 | OBSERVED |
| `09_relations/data/literacy_cohort_decomposition.csv` (`iso3,y0,y1,dt,lit0,lit1,dlit,youth0,gap0,entrant_share,exit_share,E_entrant,X_exit_lo,X_exit_hi,replacement_lo,replacement_hi,resid_lo,resid_hi`) | DT2 | DERIVED on-disk decomposition (built from observed WDI series by `09_relations/scripts/analyze_literacy_eci.py`) |
| `09_relations/data/literacy_decomposition_regressions.csv` (`test,dep,driver,coef,se,t,p,n,n_cty,within_r2`) | DT2 (on-disk anchor D1/D2a/D2b; not re-used as a result) | DERIVED on-disk regressions |
| `10_massification/data/UNIVERSALIZATION_SERIES.csv` (PHL `completion_upper_secondary`, `CR.3`) | DT5 (PHL ceiling descriptive corroboration only) | OBSERVED (source-reported) |
| `09_relations/data/economic_complexity_panel_30ctys.csv` | **not named by any DT block — not used by any test** | OBSERVED (unused here) |
| `10_massification/data/JOBS_AND_MARKETS_PANEL.csv` | **not named by any DT block — not used by any test** | OBSERVED (unused here) |
| DT3 behavioural/reform data; anthropometric series; adoption/migrant panel | DT3 | **HELD — absent; never fabricated** |

Indicators used from `panel_wdi_long.csv`:
`SE.ADT.1524.LT.ZS` (youth literacy), `SE.ADT.LITR.ZS` (adult literacy), `SE.PRM.CMPT.ZS` (primary completion),
`SE.PRM.CUAT.ZS` (primary attainment), `NY.GDP.PCAP.KD` (income), `SP.URB.TOTL.IN.ZS` (urbanization),
`SE.SEC.CUAT.UP.ZS` (upper-secondary attainment), `SE.TER.ENRR` (tertiary GER), `SE.PRM.DURS` and `SE.SEC.DURS`
(declared durations).

---

## 1. The five anchoring blocks (VERBATIM — `SYNTHESIS_020.md` §C, lines 113–251)

### DT1 — Induction of literacy: exposure dominates income/time (assembly §3.2 + §8 Prediction 2)
1. **Paper claim / section.** "In induction … a coordinated competence is assembled from conserved components by a
   practice that has no ancestral counterpart" (§3.2); Prediction 2: "induction traits track input intensity and depend
   on the practice … should scale with the duration and intensity of the installed input" (§8).
2. **First-order link (channel).** **schooling + cohort flows** — this is the micro-foundation of the programme's
   "primary graduate is installed with literacy" (A1's takeoff prerequisite). It asks whether literacy (the induced
   competence) is exposure-driven rather than income-modernized.
3. **Discriminating action.** *positive* (literacy scales with lagged schooling exposure **after** income/urbanization
   control) → the induction reading has a descriptive footprint; the "installed, not modernized" assumption is
   *named-grounded* in the model. *negative* (income absorbs the association) → literacy is consistent with a
   modernization/release secular trend, and the induction grounding is parked.
4. **Why not a niche.** It is the single cheapest test of the paper's defining claim, and it targets the assumption
   that is load-bearing for the takeoff channel (a reader of the first-order question cares directly).
5. **Data on disk.** `09_relations/data/panel_wdi_long.csv` — `SE.ADT.1524.LT.ZS` (youth literacy, the induced-competence
   tracer), `SE.ADT.LITR.ZS` (adult literacy), `SE.PRM.CMPT.ZS` / `SE.PRM.CUAT.ZS` (primary completion/attainment =
   exposure), `NY.GDP.PCAP.KD` (income), `SP.URB.TOTL.IN.ZS` (urbanization). Builds on (does **not** re-derive) the
   existing `09_relations/data/eci_literacy_results.csv` E9 (`lit_youth ~ log_cmpt_p` +29.9, within-R² 0.55, n=222).
6. **Threshold + falsifier (fixed).** Per country with ≥12 y of both series: income-partial **Spearman ρ(youth literacy,
   primary completion lagged 5 y | log income + urban) ≥ +0.40**, sign retained after control. **Falsifier** = |ρ| < 0.40
   or sign flip on income control → record "literacy orderable by income alone; induction has no footprint at this
   granularity."
7. **Closed-claim / label check.** No C1–C4 reopening; descriptive partial correlation; no causal/direction claim
   (R13-safe). **Caveat recorded:** literacy is definitionally taught in school, so a positive is *weak* evidence for
   "induction vs delivery" — DT1 is **partially diagnostic**; DT2 is the discriminating version.
8. **Cost / rank:** **small.** **Rank #1.**

### DT2 — The release-vs-induction discriminating test as a measurement design (assembly §3.3)
1. **Paper claim / section.** §3.3: "A release trait changes when nutrition, disease burden, or loading changes,
   regardless of instruction. An induced competence fails to appear when the practice is absent, regardless of how
   favorable the physiological conditions are." The discriminator is **secular-trend (release) vs input-driven
   (induction)** change.
2. **First-order link (channel).** **schooling + cohort flows** — converts the paper's own claimed linchpin into a
   measurement design on the literacy record; a null here would demote the whole release/induction distinction from
   theory to vocabulary for our purposes.
3. **Discriminating action.** *positive* (adult-literacy change is driven by the **schooling-exposed entrant share**
   — `E_entrant` — and that driver survives income control while the within-cohort secular drift and the initial gap do
   not dominate) → the induced-competence causal structure (§3.3) is the right description. *negative* (the secular
   time/cohort drift or the initial gap dominates, or `E_entrant` is absorbed by income) → literacy looks
   release-like/modernization, and the distinction does not earn model status.
4. **Why not a niche.** It is the paper's self-declared discriminating test (§3.3), run on data we already hold; it is
   the test that most directly separates the assembly account from "standard modernization descriptions" (the paper's
   own rival, §8 pred 5).
5. **Data on disk.** `09_relations/data/literacy_cohort_decomposition.csv` (columns `iso3,y0,y1,dt,lit0,lit1,dlit,
   youth0,gap0,entrant_share,exit_share,E_entrant,X_exit_lo,X_exit_hi,replacement_lo,replacement_hi,resid_lo,resid_hi`),
   `09_relations/data/literacy_decomposition_regressions.csv` (D1/D2a: `dlit ~ E_entrant` +1.65/1.64, p<0.001, n=241/25;
   D2b: `dlit ~ gap0` +0.32, p=0.009 — existing, **without** income control). Add income from `panel_wdi_long.csv`
   `NY.GDP.PCAP.KD`.
6. **Threshold + falsifier (fixed).** Re-derive the decomposition with **income added**: support iff (a) the `E_entrant`
   coefficient on `dlit` remains **≥ +1.0** and p<0.05 after log-income control, **and** (b) the `gap0` coefficient is
   **≤ 0.5 × the `E_entrant` coefficient**. **Falsifier** = `E_entrant` < +0.5 or loses significance on income control,
   or `gap0` ≥ `E_entrant` → record "secular/gap channel dominates; no exposure-driven (induction) signature survives
   income."
7. **Closed-claim / label check.** No C1–C4 reopening; descriptive decomposition, no direction claim. **Caveat
   recorded:** cohort replacement is partly arithmetic (entrants mechanically replace exits), so `E_entrant` dominance is
   *partly mechanical*; the discriminating part is **income-controlled survival + gap0 subordination**, not the raw
   coefficient.
8. **Cost / rank:** **small–medium.** **Rank #2.**

### DT3 — Schedule-discipline as an induced competence (assembly §3.2 + §8 Prediction 3) — DESIGN-ONLY / HELD
1. **Paper claim / section.** "Time discipline, punctuality, tolerance of deferred reward, and performance under
   continuous evaluation are properties of persons produced by the institution's routine" (§3.2); Prediction 3:
   "reform designs should show behavioral as well as cognitive effects … Reform effects confined to measured cognition,
   with no movement in the behavioral syndrome, would damage the formatting claim" (§8).
2. **First-order link (channel).** **government (policy) + schooling** — the formatting/behavioural channel is the A3
   "school formats persons" assumption, but the model has **no behavioural output**, so this is a *micro-validity* test
   rather than a model lever.
3. **Discriminating action.** *positive* (a reform/grade-discontinuity moves a behavioural outcome — punctuality,
   schedule compliance, arrest/incarceration, evaluative orientation — alongside or beyond measured cognition) → the
   formatting claim has an identification route. *negative / unavailable* → the formatting claim stays a **declared
   assumption** with no on-disk behavioural footing.
4. **Why not a niche.** It is the paper's most distinctive claim (the person, not the curriculum) — but it is **not on
   the current critical path**: the model does not emit behaviour, so this cannot change the PHL ceiling or the crossings.
5. **Data on disk.** **None.** HELD (named, never fabricated): a compulsory-schooling reform / grade-level discontinuity
   for PHL (or a comparable system) matched to a behavioural outcome — time-discipline/punctuality survey, arrest/
   incarceration counts (Lochner–Moretti design), or evaluative-orientation survey. The paper's own behavioural citations
   (Lochner–Moretti 2004; Paglayan 2024; Bowles–Gintis 1976) are **external, cited not measured** (D49).
6. **Threshold + falsifier (fixed).** Design-only: support iff a reform-associated behavioural shift is **≥ 5% of a
   within-series SD** and survives a pre-declared parallel-trends check. No run until the data ask is approved; **no
   number may be fabricated**.
7. **Closed-claim / label check.** Does **not** reopen C1–C4 or the closed shadow/mechanism claims; design-only; no
   direction claim. The *discriminating* formatting test is genuinely open but **data-blocked**.
8. **Cost / rank:** **large (HELD data).** **Rank #5 → DROP-FIRST.**

### DT4 — Constructed-niche intensity → persistence (assembly §8 Prediction 5 + hysteresis Prediction 4)
1. **Paper claim / section.** Assembly §8 pred 5: "Installation depth … should order populations and cohorts on the
   tracers of Table 1, and should do so after income is controlled … A tracer set that ordered on income alone, with
   installation depth adding nothing, would reduce the account to standard modernization descriptions." Hysteresis
   Prediction 4: "Scaffolds surrounded by dense complementary investment should display greater persistence following
   deterioration of their original adoption advantage" (§492–494).
2. **First-order link (channel).** **markets + schooling** — the combined comparative claim that *niche depth*
   (schooling exposure) both orders the induced tracer (literacy) and predicts its *persistence* (no reversal), the
   developmental counterpart of the WT3 complementarity test.
3. **Discriminating action.** *positive* (installation depth orders the literacy tracer after income control **and**
   high-depth countries show zero literacy reversal) → the assembled-niche reading survives the modernization rival and
   the combined persistence claim gains footing. *negative* (income absorbs the ordering, or reversals are uncorrelated
   with depth) → the account reduces to modernization (the paper's own rival) and is parked.
4. **Why not a niche.** It is the paper's explicitly-named **principal rival** test ("the design must beat" modernization),
   extended by the hysteresis persistence corollary; it is comparative and uses our 30-country panel.
5. **Data on disk.** `09_relations/data/panel_wdi_long.csv` — `SE.ADT.LITR.ZS` / `SE.ADT.1524.LT.ZS` (tracer),
   `SE.PRM.CMPT.ZS` + `SE.PRM.DURS` / `SE.SEC.DURS` (installation-depth proxy = completion level + schooling duration),
   `NY.GDP.PCAP.KD` (income). No DATA ASK.
6. **Threshold + falsifier (fixed).** Installation-depth proxy = primary-completion level × declared schooling duration
   (both standardized). Persistence = **zero** ≥3 pp negative literacy Δ over 1995–2024. Support iff (a) income-partial
   **Spearman ρ(literacy level, depth | log income) ≥ +0.40**, **and** (b) in the top-half depth countries **≥ 80%**
   show zero reversal while the bottom half shows ≥ 1 reversal in **≥ 40%** of countries. **Falsifier** = |income-partial
   ρ| < 0.40 or sign flip, or no depth gradient in reversal incidence.
7. **Closed-claim / label check.** No C1–C4 reopening; cross-sectional descriptive association, no direction claim (R13);
   **n=30, low power, income-confounded** (the Y1 lesson: raw agri association was absorbed by income) — reported as
   descriptive, never as a law.
8. **Cost / rank:** **medium.** **Rank #3.**

### DT5 — The credential as the junction of both papers (induced competence + asymmetric exit) — assembly §9 + hysteresis credential §321–331
1. **Paper claim / section.** Assembly §9: "the school's largest product is the person rather than the curriculum, and
   the productivity of the credential system should be evaluated with the formatting included in the accounting."
   Hysteresis credential: "The resulting equilibrium can persist even if the credential becomes only weakly related to
   job-specific competence" (§321–331). Joint prediction: the credential is **both** an installed (induced) competence
   **and** a scaffold whose exit is asymmetric.
2. **First-order link (channel).** **markets + schooling** — the PHL upper-secondary ceiling residual (D63, 15.0 pp,
   UNABLE) is the single object where the two papers meet; this asks whether the *joint* signature (induction happened at
   the floor + asymmetric exit at the ceiling) is a PHL-specific coincidence or a general decomposable pattern.
3. **Discriminating action.** *positive* (in the panel, literacy universalizes everywhere — the induction side — while
   the upper-secondary credential ceiling persists only where the credential gate is load-bearing — the exit side) → the
   two papers decompose the record into distinct mechanisms. *negative* (literacy universalization and the ceiling
   residual are uncorrelated across countries, or the PHL ceiling is not a gate phenomenon) → the junction reading has no
   comparative footing and the ceiling stays UNABLE.
4. **Why not a niche.** It targets the phase's single open object (the ceiling) and tests whether the two papers'
   *joint* vocabulary is more than a re-description. **Honest caveat:** at n=30 and with the PHL ceiling already known, a
   positive is **near-circular** — this is the weakest diagnostic of the five.
5. **Data on disk.** `09_relations/data/panel_wdi_long.csv` — `SE.ADT.LITR.ZS` (induction tracer),
   `SE.SEC.CUAT.UP.ZS` (upper-secondary attainment = the credential gate), `SE.TER.ENRR` (tertiary GER);
   `10_massification/data/UNIVERSALIZATION_SERIES.csv` (PHL `CR.3` upper-secondary completion never ≥90, peak 76.43).
6. **Threshold + falsifier (fixed).** Define "literacy-universalized" = adult literacy ≥ 90 by 2024; "ceiling-persistent"
   = upper-secondary attainment **never** ≥ 90 and no ≥5 pp sustained reversal. Support iff, across the panel, literacy
   universalization and ceiling-persistence are **both present in ≥ 50% of countries** (joint signature), **and** the PHL
   ceiling is **not** explained by the same observables that explain its literacy (income/completion). **Falsifier** =
   the joint signature holds in < 50% of countries, or the PHL ceiling is absorbed by the same observables as its floor.
7. **Closed-claim / label check.** Does **not** reopen C1–C4 (the *discriminating* queue test remains C3/HELD); does **not**
   re-score WT2/WT4 — this is the *joint-presence* version, flagged near-circular. No direction claim.
8. **Cost / rank:** **small.** **Rank #4.**

---

## 2. Diagnostic-vs-circular labels (VERBATIM — `SYNTHESIS_020.md` §F, table)

| test | what it tests | diagnostic value | circularity / confound |
|---|---|---|---|
| **DT1** induction dose-response | literacy scales with exposure after income | **partially diagnostic** — a null weakens the induction-as-niche claim | literacy is definitionally taught in school ⇒ positive is weak evidence |
| **DT2** release-vs-induction (§3.3) | secular-trend vs exposure-driven change, income-controlled | **most diagnostic** — the paper's own discriminator | cohort replacement is partly arithmetic; income-control survival is the real test |
| **DT3** schedule-discipline (§8 #3) | reform → behavioural | diagnostic in principle, **not runnable (HELD)** | none on disk; design-only |
| **DT4** niche-intensity → persistence (pred 5 + hysteresis P4) | installation depth orders tracer + persistence after income | **partially diagnostic** | income-confounded (Y1 lesson); n=30 |
| **DT5** credential junction | joint induced-competence + asymmetric-exit signature | **near-circular** | re-tabulates known literacy-universalization + PHL ceiling under new vocabulary |

---

## 3. Operationalizations fixed before run

These fill in estimator/aggregation/eligibility details the blocks leave implicit. **They are not threshold
changes.** No threshold, discriminating action, or falsifier below differs from §1.

### 3.0 Verdict vocabulary (used in `results/RESULTS.csv`)

| verdict value | block term it copies | meaning |
|---|---|---|
| `NON-NULL` | DT1 "**positive**"; DT2/DT4/DT5 "**support**" | the block's fixed support condition is met |
| `NULL` | DT1 "**negative**"; DT2/DT4/DT5 "**falsifier**" | the block's fixed falsifier condition is met |
| `INDETERMINATE` | — (block's own gap) | only where the block's support and falsifier regions leave an uncovered interval and the estimate falls in it; reported, never counted as support |
| `DATA LIMITED` | frozen rule | the block's eligibility/denominator floor is not met; no verdict on the claim |
| `UNABLE` | DT3 "**UNABLE (HELD)**" | the series is absent/HELD; no number is reported |

`RESULTS.csv` carries both `verdict` (the table above) and `block_term` (the block's own word, verbatim:
`positive`/`negative` or `support`/`falsifier` or `UNABLE`).

### 3.1 Common rules

1. **Missing data:** listwise deletion within each test; **no imputation**, no interpolation, no proxy substitution.
2. **Observed cells only.** HELD series are not proxied. A test whose inputs are absent is DATA LIMITED/UNABLE.
3. **Eligibility:** exactly the block's rule (e.g., DT1 `≥12` overlapping years per country). Added floors, fixed
   now, for "too small to reach the fixed test": DT1 `<2` eligible countries; DT2 either model `n<40` or
   `n_cty<8` (the on-disk pipeline's own floor, on which D1/D2a rely); DT4 cross-section `n<10` or either depth
   half `<5`; DT5 denominator `<10`. Below a floor: `DATA LIMITED`, statistic reported as the raw eligible count,
   no verdict.
4. **Two-way FE estimator (DT2 only):** country and `y1` fixed effects via alternating projections (country-demean,
   time-demean; 200 iterations, tol `1e-12`), country-clustered CR1 standard errors, normal two-sided p — the same
   specification used by `09_relations/scripts/panel_lib.py:27–82`, which produced the on-disk D1/D2a/D2b. DT2
   re-reports D1 (`dlit ~ E_entrant`) as a specification cross-check; the cross-check is **not** a DT2 result.
5. **Partial Spearman (DT1, DT4a):** average-rank transform each variable, OLS-residualize the ranks of the
   outcome and the exposure on the ranks of the controls (plus intercept), then Pearson-correlate the residuals.
   Controls: DT1 = `log(NY.GDP.PCAP.KD)` and `SP.URB.TOTL.IN.ZS`; DT4a = `log(NY.GDP.PCAP.KD)`.
6. **Aggregation across countries (DT1):** the block states the threshold **per country**. Headline statistic =
   **median** country-level income-partial ρ across eligible countries (fixed before run); per-country ρ are all
   reported in `DETAIL.csv`. Sign retention = median raw ρ > 0 and median partial ρ has the same sign.
7. **Rows:** `RESULTS.csv` = exactly one row per test (5 rows), including nulls and UNABLE. `DETAIL.csv` = the
   underlying per-country / per-model numbers behind every row.
8. **Rounding:** results are written at full float precision to CSV; prose may round for reading. No rounding
   before a threshold comparison.

### 3.2 DT1 — induction of literacy, exposure dominates income/time

- **Sample (per country):** years `t` with `SE.ADT.1524.LT.ZS(t)`, `SE.PRM.CMPT.ZS(t−5)` (primary completion
  lagged 5 years), `NY.GDP.PCAP.KD(t)`, `SP.URB.TOTL.IN.ZS(t)` all observed. Eligibility: `n_t ≥ 12` (block rule).
- **Statistic:** per-country income-partial Spearman ρ(youth literacy, primary completion lagged 5y | log income +
  urban) by §3.1(5); plus raw Spearman ρ for the sign-retention check.
- **Headline:** median partial ρ across eligible countries; `n` = eligible country-years; `n_countries` = eligible
  countries. Secondary (reported, non-verdict): number/share of countries with ρ ≥ +0.40.
- **Support (block):** median partial ρ ≥ **+0.40**, sign retained after control.
- **Falsifier (block):** `|ρ| < 0.40` or sign flip on income control → record "literacy orderable by income alone;
  induction has no footprint at this granularity."
- **Label:** DERIVED. **Diagnostic value:** partially diagnostic; a positive is weak evidence (literacy is
  definitionally taught in school).

### 3.3 DT2 — release-vs-induction discriminating test (income added)

- **Sample:** all `literacy_cohort_decomposition.csv` rows (241 country-periods, 25 countries) merged to
  `log(NY.GDP.PCAP.KD)` at `y1`. All 241 rows have income on disk; no imputation.
- **Models (two-way FE + country-clustered CR1, §3.1(4)):**
  - `M1`: `dlit ~ E_entrant + log_gdp` (income-controlled discriminating driver alone)
  - `M2`: `dlit ~ E_entrant + gap0 + log_gdp` (joint model: entrant driver + initial gap, income-controlled)
  - Cross-check only: `D1`: `dlit ~ E_entrant` (must reproduce the on-disk +1.65).
- **Support (block):** (a) the `E_entrant` coefficient on `dlit` remains **≥ +1.0** and **p<0.05** after
  log-income control — tested in the joint model `M2` (and reported in `M1`) — **and** (b) the `gap0` coefficient
  is **≤ 0.5 × the `E_entrant` coefficient** (both from `M2`).
- **Falsifier (block):** `E_entrant < +0.5` or loses significance on income control (p≥0.05), or
  `gap0 ≥ E_entrant` → "secular/gap channel dominates; no exposure-driven (induction) signature survives income."
- **INDETERMINATE:** if `+0.5 ≤ E_entrant < +1.0` with p<0.05 and (b) holds — the block's own uncovered interval.
- **Label:** DERIVED. **Caveat:** cohort replacement is partly arithmetic; the discriminating part is
  income-controlled survival + `gap0` subordination, not the raw coefficient.

### 3.4 DT3 — schedule-discipline as an induced competence (DESIGN-ONLY / HELD)

- **No run.** No data on disk. No number is produced anywhere in this battery.
- **Design (recorded, not executed):** a difference-in-differences / regression-discontinuity design on a
  compulsory-schooling reform or a grade-level discontinuity (e.g., a leaving-age change in the Lochner–Moretti
  tradition), with the treated cohort compared to adjacent untreated cohorts; outcome = a behavioural syndrome
  measure (time-discipline/punctuality survey, arrest/incarceration counts, or evaluative-orientation survey);
  a **pre-declared parallel-trends check** on pre-reform cohorts must pass; support iff the reform-associated
  behavioural shift is **≥ 5% of a within-series SD** and survives that check.
- **Data status:** **HELD** — named, never fabricated: reform/grade-discontinuity microdata matched to behavioural
  outcomes. The paper's behavioural citations (Lochner–Moretti 2004; Paglayan 2024; Bowles–Gintis 1976) are
  external, cited not measured (D49).
- **Verdict:** `UNABLE (HELD, design-only)`; drop-first per D103.

### 3.5 DT4 — constructed-niche intensity → persistence

- **Depth proxy (block: primary-completion level × declared schooling duration, both standardized):**
  country means over 1995–2024 of `SE.PRM.CMPT.ZS` and of total declared duration
  `SE.PRM.DURS + SE.SEC.DURS`; each z-scored across countries (sample SD, ddof=1); `depth = z(completion) ×
  z(duration)`. (The block's data line names both `SE.PRM.DURS` and `SE.SEC.DURS`; total declared duration is the
  primary spec, primary-only duration is a reported sensitivity, never verdict-changing.)
- **(a) Ordering:** cross-section of the 30 countries; country mean adult literacy (`SE.ADT.LITR.ZS`, 1995–2024)
  vs `depth`, income-partial Spearman | log mean income (1995–2024). Support: ρ ≥ **+0.40**, sign positive.
- **(b) Persistence:** consecutive-year Δ in adult literacy, 1995–2024 (only exactly 1-year gaps); reversal event
  = Δ ≤ **−3.0 pp**. Top half = `depth ≥ median` (15 countries), bottom half = the rest.
  Support: top-half **zero-reversal share ≥ 80%** **and** bottom-half **≥1-reversal share ≥ 40%**.
- **Support:** (a) **and** (b). **Falsifier:** (a) fails (`|ρ| < 0.40` or sign flip) **or** there is no depth
  gradient in reversal incidence (the (b) shares fail).
- **Label:** DERIVED. **Caveat:** n=30, low power, income-confounded (Y1 lesson); descriptive, never a law.

### 3.6 DT5 — the credential as the junction of both papers

- **Denominator:** countries with an adult-literacy (`SE.ADT.LITR.ZS`) observation in 2015–2024 (latest used) and
  an upper-secondary-attainment (`SE.SEC.CUAT.UP.ZS`) observation in 1995–2024.
- **"Literacy-universalized" (block):** latest adult literacy **≥ 90** by 2024.
- **"Ceiling-persistent" (block):** upper-secondary attainment **never ≥ 90** over 1995–2024 **and** no **≥5 pp
  sustained reversal** (operationalized: no episode in which the series falls ≥5 pp below its prior running maximum
  and remains ≥5 pp below it for at least two consecutive observations).
- **Joint signature:** both present, as a share of the denominator. Support requires **≥ 50% of countries**.
- **PHL ceiling check (block: "not explained by the same observables that explain its literacy (income/completion)"):**
  cross-country OLS of latest upper-secondary attainment on latest `log(NY.GDP.PCAP.KD)` and latest
  `SE.PRM.CMPT.ZS`; `z_PHL` = PHL residual / SD of residuals. Fixed operational cut: the ceiling counts as **not
  explained** iff `z_PHL ≤ −1.0` (PHL at least 1 residual SD below what its income/completion predict). Sensitivity
  cuts (−0.5, bottom quartile) are reported in `DETAIL.csv`, never verdict-changing.
- **Support:** joint share **≥ 50%** **and** `z_PHL ≤ −1.0`. **Falsifier:** joint share < 50% **or** `z_PHL > −1.0`.
- **Label:** DERIVED. **Caveat:** near-circular at n≈24–30 with the PHL ceiling already known (D63); weakest
  diagnostic of the five. Does **not** re-score WT2/WT4.

---

## 4. Binding conditional gate (VERBATIM — `SYNTHESIS_020.md` §D, item 3)

3. **A conditional, binding addition (mirroring D101):** **if DT1 AND DT2 both return non-null**, the generator may
   *name* the induction mechanism in its declared-assumption provenance (still a declared assumption, **never** a fitted
   "induction parameter" — R4/R27). If either returns null, the induction grounding is **PARKED** and the two assumptions
   keep their current "declared" label with no theory citation.

**Reading fixed now:** induction naming is allowed **only if BOTH DT1 and DT2 return NON-NULL**. If either is NULL,
DATA LIMITED, INDETERMINATE, or UNABLE, the induction grounding is **PARKED**. A DT PASS is descriptive only: it
does not validate the paper, does not create an "induction parameter", and does not reopen C1–C4.

---

## 5. What this battery cannot claim (fixed before results)

1. No causal claim and no direction claim: every DT statistic is a descriptive association.
2. A DT PASS is **not** validation of the assembly paper or the hysteresis paper; neither paper is evidence.
3. No C1–C4 reopening; no re-scoring of WT1–WT5; no relabelling of the closed D63 ceiling residual as "explained".
4. No model change follows from any DT: D104 permits only declared-assumption provenance naming, gated on DT1 **and**
   DT2, and never a fitted "induction" parameter or a new layer.
5. DT3 cannot be run (HELD) and its absence is not evidence for or against the formatting claim.
6. DT1 is partially diagnostic (literacy is definitionally taught in school); DT5 is near-circular; DT4 is
   income-confounded at n=30; DT2 is the only strongly discriminating test, and even it is descriptive.

---

## 6. Determinism and manifest

- `code/run_dt.py` is deterministic: no RNG, no sampling, no seed (seed = `null`; recorded in `RUN_MANIFEST.json`).
- The battery is run **twice** into separate output directories (`results/run1/`, `results/run2/`); the two
  `RESULTS.csv` and `DETAIL.csv` must be **byte-identical** (sha256 equality). Only then are they promoted to
  `results/RESULTS.csv` and `results/DETAIL.csv`.
- `RUN_MANIFEST.json` records: sha256 of this file, of the code, of every input, of every result; the run
  timestamps; and the determinism evidence (per-file sha256 of run1 vs run2).

---

## 7. Change log

**None.** This predeclaration is frozen at the sha256 recorded in `RUN_MANIFEST.json`. No threshold, discriminating
action, or falsifier was changed after any result was seen.
