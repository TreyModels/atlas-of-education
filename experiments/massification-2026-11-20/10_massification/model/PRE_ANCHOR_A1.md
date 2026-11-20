# PRE-DECLARATION — A1: PHILIPPINES anchor model (mechanisms + calibration + rivals)

**Owner:** experiment-runner (`deepseek-exp1`). **Status:** predeclared before fitting. **Authority:** Council
`08_council/brief_013/ANCHOR_SYSTEM.md` (D38–D42, Amendment **A5**, **R20–R22**), `08_council/ANCHOR_SLATE.csv` A1,
brief 013 §2–§4, Amendment A1 (scaling) and A4 (milestone timing). Anchor system = **PHILIPPINES** (Council D38).

## Scope
One PHL model that reproduces the trajectory, the A1/A3 scaling exponents (generated, not supplied), the A4 milestone
timing, and the **A5 mechanism event breaks**; compared against at least three fair rival models fitted on the same
record. Portability (A6 CHN, A7 HKG) is a separate later checkpoint and is not scored here.

## Mechanisms and exogenous events (never fitted — R12/R4)
All dates are exogenous inputs from the record; effects may not be calibrated to outcomes.
| id | type | event | date (exogenous) | model switch | what the model must generate |
|---|---|---|---|---|---|
| M1 | state push | K-12 extension (RA 10533; SHS rollout) | 2013 law, 2016–17 SHS | cycle-length switch + cohort exposure | break in upper-secondary completion for exposed cohorts; JHS-holder definition shift; placebo pre-2013 cohorts null |
| M2 | state push | free SHS | 2016 | cost/fee path for upper secondary | intake/continuation rise, concentrated in Q1–Q2 |
| M3 | state push | free tertiary (RA 10931) | 2018 | tertiary cost path | tertiary intake/transition rise, concentrated in Q1–Q2 |
| M4 | state push | places/teacher supply expansion | dated capacity/teacher series (data-first A8) | capacity/teacher path feeding intake | capacity leads intake with a declared lag (2–4 y); unmet demand before, absorbed after |
| M5 | demand pull (foreign) | US nurse visa expansion | 2005–06 | expected-return/field-specific channel | nursing field response; placebo fields null (E3 series DATA BLOCKED → simulated only, labelled) |
| M6 | demand pull (domestic) | BPO/IT growth; remittances | series-driven | regional/sectoral exposure channel | regional transition/enrolment gradient; placebo sectors/regions null |
| M7 | supply push | HEI/teacher expansion; educated-cohort growth | series-driven | education-led feedback (e_s) | schooling expansion leads formal jobs (positive) vs absorbed in informality/queue (~0/negative → queue; R13) |

## Event-break estimand (predeclared)
For each event: **pre-trend** over the pre-event observed window; **break sign** and **magnitude band** predeclared per
event (e.g. M1: upper-secondary completion falls then rises, net band declared; M2/M3: rise in the treated level,
concentrated Q1–Q2 with a declared minimum differential); **placebo checks**: pre-event cohorts, unaffected levels,
unaffected fields/regions. A break that appears only arithmetically (definition change) is reported as such.
Band values are declared in the A2 predeclaration for state pushes and in the demand-pull cell for M5–M6.

## Rival set — "different researchers' models" fitted on the same PHL record
| rival | core mechanism | what it predicts for PHL | discriminating implication |
|---|---|---|---|
| HC (Becker/Mincer) | returns-driven investment | expansion tracks returns; event breaks follow expected earnings | if expansion continues while returns fall, HC needs a residual |
| world society (Meyer/Schofer) | global norms/legitimacy | expansion decoupled from jobs/returns; timing follows norm diffusion | predicts no event-break at domestic policy dates |
| labour queue (Thurow/Collins) | credential queue, jobs fixed | education expands regardless of jobs; educated absorption in lower jobs/informality | predicts informality/queue absorption (R13 ~0/negative education→jobs) |
| state-building (Paglayan) | state capacity/order motive | state pushes drive expansion at fiscal/political events | predicts event breaks at state-push dates, not at demand dates |
| sectoral demand (Lewis/Kuznets) | sectoral shift pulls schooling | expansion follows agri→industry→services | predicts sectoral links dominate policy events |
Each rival is fitted identically on the PHL pre-2013 record with the same exogenous events, then predicts 2013–2024
and the event breaks out of sample. **Anchor must beat them on the predeclared event-break estimand AND on
out-of-sample trajectory; otherwise report EQUIVALENT (R3/R13) — no winner chosen.**

## Roles (brief 013 §2 reproduced verbatim; A4/A5 additions)
| Domain | Series (unit) | Role | Countries |
|---|---|---|---|
| Education levels | Primary / lower-sec / upper-sec completion (%, cohort; UIS CR.1/2/3 observed years) | **FIT** | PHL (1980–2010), CHN (1980–2010) |
| Education levels | Same series | **HOLDOUT PERIOD (2011–2024)** | PHL, CHN |
| Education levels | Same series | **HOLDOUT COUNTRY (all years; KHM never fitted)** | KHM (1980–2023 observed) |
| Education levels | Same series | **CHECK only** | KOR (2012 point), HKG (no UIS completion), JPN (no UIS completion) |
| Education flows | GER, out-of-school rate, transition proxies (UIS; TARGETS_FLOW.csv; proxies labelled) | **CHECK (shape only; no fitting)** | all six |
| Attainment | Mean years / attainment distribution (HK EDB 2025; KHM CLFS 2019; WDI modelled = benchmark only) | **CHECK** | HKG, KHM |
| Jobs/markets | Employment shares agri/industry/services (WDI/ILO modelled; ECONOMY_SERIES.csv) | **CHECK in task-37** (deviation from the brief-013 "FIT" row recorded in Amendment §I: modelled series excluded per §6 + Lead resolution) | PHL, CHN |
| Jobs/markets | Status employment (wage/vulnerable), GDP pc, urbanisation, remittances | **CHECK / constraints (sign expectations)** | all six |
| Jobs/markets | Formal/informal share (CLFS 2019 KHM only; ILOSTAT blocked) | **CHECK (single cell)** | KHM |
| Sectors | Agri/industry/services shares; formal/informal where measured | **CHECK (see row above); never extrapolate missing sectors** | PHL, CHN (+KHM cell) |
| Universalization timing | **A4 milestones M0–M4 crossing years** derived from the series; **never fitted — HOLDOUT OUTCOME** | **HOLDOUT OUTCOME** | PHL (A1); JPN/KOR/HKG as timing checks once A4 data lands |

## Tolerances (brief 013 §3 reproduced verbatim) and A1/A4/A5 additions
In-sample level MAE ≤ 5 pp; out-of-sample level (2011–2024; held-out KHM) MAE ≤ 8 pp AND strictly better than **both**
naive benchmarks (persistence; linear trend); shape corr ≥ 0.6 in-sample, ≥ 0.5 out-of-sample, sign of net change
correct; midpoint within ±5 years; cohort-flow consistency exact (B1–B3, zero tolerance); sector shares MAE ≤ 5 pp
in-sample / ≤ 8 pp out-of-sample, sign correct; universalization false-positive test; relation-sign constraints
R13/R04/R02 reported as failures if violated. **A1/A3 scaling:** generated OOS exponents correct sign for all three
classified laws and inside the A3 estimator range for ≥2 of 3; ±1 se of A1 values = stricter descriptive only.
**A4 timing:** M0 massification crossing ≥50% and M2/M3 universalization crossings within ±5 y (±3 narrow); primary is
near-universal → timing/boundary regime. **A5 mechanisms:** each event break with clean pre-trend, sign and magnitude
inside the predeclared band, placebo null. **Verdict vocabulary:** PASS / PARTIAL / FAIL / EQUIVALENT, plus
PASS-CONDITIONAL vs IDENTIFIED (A1). Stop rules R1–R12 + R20–R22 adopted.

## Known data limits (declared before fitting; ANCHOR fit window superseded to 1999–2013 by Amendment A6 below)
Pre-1999 completion is missing (A8 data-first pending); the anchor FIT window is **1999–2013** (Amendment A6), holdout 2014–2024; the earlier smoke window 1999–2010 remains only for the pre-anchor diagnostic cells
(≈6–7 observed points per level) and 2013+ events fall inside the HOLDOUT window, so event-break tests for K-12/free
SHS/free tertiary have limited pre-period support. DepEd/DPWH places/teacher series are not yet on disk (A8/A2
data-first); where absent, the affected test is **DATA BLOCKED**, never imputed. E3 nurse series remain DATA BLOCKED
(simulated-only). MDE claim cap applies: PASS at ≥ MDE ≈4 pp; below = INCONCLUSIVE (not support, not null).

## Sequencing
1. A1 fit only after this predeclaration is posted (done).
2. Then A2 state-push battery (own predeclaration), then demand-pull battery (A3/A5).
3. Portability A6 (CHN) then A7 (HKG) only after A1/A2, with **fixed behaviour + PHL parameter values**; only declared
   country inputs re-set; behavioural re-fit = **FAIL** (R20). No direction claims anywhere (R13); label
   observed/simulated; no git writes.

## AMENDMENT A6 (Council D47–D49 / R23; applied before anchor fitting)
**The anchor's discriminating signal is the verified ASYMMETRY of the PHL record, not a single universalization
curve.** Observed (on-disk, `status==target`; A6 text): primary completion 83.16 (1999) → 91.92 in **2017** (first
≥90) → 98.30 (2024); lower-secondary 58.86 (1999) → 92.41 in **2024** (first ≥90); upper-secondary 59.70 (1999) →
75.03 (2024) and **never ≥90**; tertiary GER 16.34 (1971) → 52.99 (2026), first ≥50 in the **2024–2025** band.

**1. Fit/holdout supersession (binding).** For the ANCHOR model: **FIT window 1999–2013; HOLDOUT 2014–2024.** This
supersedes the earlier 1999–2010 smoke window for the anchor (the smoke/PHL+CHN cells are retained as pre-anchor
diagnostics, R12). CHN/KHM roles are unchanged; KHM stays the held-out country.

**2. Milestone set M0–M4 (declared; crossing years are HOLDOUT OUTCOMES, never fitted).**
| id | milestone (PHL) | observed crossing | status of the crossing |
|---|---|---|---|
| M0 | primary completion ≥90% | **2017** | observed |
| M1 | lower-secondary completion ≥90% | **2024** | observed (at edge of holdout) |
| M2 | upper-secondary completion ≥90% | **none by 2024** (75.03 last) | **right-censored / never observed** |
| M3 | tertiary GER ≥50% | **2024–2025 band** | observed band, not a point |
| M4 | upper-secondary completion ≥75% | **~2023–24** (75.03 in 2024) | observed (level unsaturated) |
**Estimand:** the vector of generated crossing years/intervals, their **ordering**, and the **gaps** between them.
**Tolerances:** ±5 y (±3 y narrow band) per A4; a crossing reported as an interval when the observed bracket is wider
than one year.
**Asymmetry test (predeclared):** a model that fits one shared universalization curve/timing to all levels is
**PARTIAL at most (R23)**. PASS requires the model to reproduce *which* milestones moved and *when* — i.e. the
ordering (M0 ≺ M1/M3/M4, with M3 as a band) and the gaps — not merely the overall level.
**False-positive check (R6, predeclared):** generating upper-secondary completion reaching ≥90 by 2024 is a
**structural failure** (the record never shows it), regardless of how well the trajectory otherwise fits. Model
crossings for M2 must be absent or right-censored consistently.
**No shared-curve shortcut:** the model may not be given the crossing years, ceilings, or a logistic schedule as
inputs (R4). Generated paths only.

**3. Events vs crossings (evidence recorded before fitting).** Scout's `relations/data/event_windows.csv` shows PHL
policy dates do **not** align with crossing years: 1987 Constitution → primary ≥90 crossing 2017–21 (gap **31 y**);
RA 10533 (2016 effective) → secondary GER window shift **+0.42 pp (t=0.50)**, i.e. null; RA 10931 free tuition (2018) →
tertiary window shift **−5.39 pp (t=−3.0)** but confounded with the K-12 transition cohorts; 4Ps CCT → secondary
−2.49 pp (t=−1.27, n_post=3). Therefore: (a) the anchor is scored primarily on **crossing years/ordering/gaps**, not
on law-date breaks; (b) event-break tests are predeclared to **allow a null result** and must carry a declared power
statement (the E2 power/MDE rule: PASS at ≥MDE ≈4 pp, else INCONCLUSIVE — not support, not null); (c) a state-push
event that shows no break is reported as such, not tuned until it appears (R12).

**4. Rivals scored on ordering/gaps, not levels.** The five rival models (HC, world society, labour queue,
state-building, sectoral demand) are fitted on the **same PHL 1999–2013 record with the same exogenous events** and
scored on (i) the milestone ordering/gap vector and (ii) out-of-sample trajectory 2014–2024; a rival that matches the
same moments is **EQUIVALENT** (R3/R13), no winner chosen. Anchor PASS requires beating them on the predeclared
ordering/gap estimand AND on out-of-sample trajectory.
