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

## Known data limits (declared before fitting)
Pre-1999 completion is missing (A8 data-first pending); the FIT window for PHL is therefore effectively 1999–2010
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
