# AMENDMENT 013 — predeclaration aligned to Council brief 013 (task-39)

**Dated:** 2026-11-20, before any massification-phase fit. **Status:** binding; supersedes the calibration sections
of `PREDECLARATION.md` where they differ. Nothing has been fitted (the gate was respected); no already-run cell is
changed. Brief 013 §2–§4 are reproduced here **verbatim in substance** as required by §7.

## A. Fit / check / holdout table (brief 013 §2 — copied role-for-role)

| Domain | Series (unit) | Role | Countries |
|---|---|---|---|
| Education levels | Primary / lower-sec / upper-sec **completion** (%, cohort; UIS CR.1/2/3 observed years) | **FIT** | PHL (1980–2010), CHN (1980–2010) |
| Education levels | Same series | **HOLDOUT PERIOD (2011–2024)** | PHL, CHN |
| Education levels | Same series | **HOLDOUT COUNTRY (all years; never fitted)** | KHM (1980–2023 observed) |
| Education levels | Same series | **CHECK only** | KOR (2012 point), HKG (no UIS completion), JPN (no UIS completion) |
| Education flows | GER, out-of-school rate, transition proxies (UIS; `TARGETS_FLOW.csv`; proxies labelled) | **CHECK (shape only; no fitting)** | all six |
| Attainment | Mean years / attainment distribution (HK EDB 2025; KHM CLFS 2019; WDI modelled = benchmark only) | **CHECK** | HKG, KHM |
| Jobs/markets | Employment shares agri/industry/services (WDI/ILO modelled; `ECONOMY_SERIES.csv`) | **FIT (cohort-sector link); holdout 2011–2024** | PHL, CHN |
| Jobs/markets | Status employment (wage/vulnerable), GDP pc, urbanisation, remittances | **CHECK / constraints (sign expectations)** | all six |
| Jobs/markets | Formal/informal share (CLFS 2019 KHM only; ILOSTAT blocked) | **CHECK (single cell)** | KHM |
| Sectors | Agri/industry/services shares; formal/informal where measured | **FIT in PHL/CHN; check elsewhere; never extrapolate missing sectors** | PHL, CHN (+KHM informal cell) |
| Universalization timing | Crossing year derived from the FIT/CHECK series; never fitted | **HOLDOUT OUTCOME** | PHL, CHN, KHM; KOR/HKG/JPN as checks |

Excluded from fitting and targets (brief 013 §2): HKG 85% shadow-education figure (prior phase; shadow secondary now),
modelled attainment series, imputed/environment cells, any series with an un-harmonised definition change.

## B. Tolerances (brief 013 §3 — reproduced)
- In-sample **level** fit (completion, each level): MAE ≤ **5 pp**.
- Out-of-sample **level** (2011–2024; and held-out KHM): MAE ≤ **8 pp** AND strictly better than **both** naive
  benchmarks (last-value persistence; linear trend).
- Shape: correlation ≥ **0.6** in-sample, ≥ **0.5** out-of-sample; sign of net change correct at each level.
- Turning point / universalization midpoint: within **±5 years**.
- Cohort-flow consistency: exact conservation (B1 stock identity, B2 cohort conservation, B3 all rates in [0,1],
  no negative stocks) — **zero tolerance**.
- Sector shares: MAE ≤ **5 pp** in-sample; ≤ **8 pp** out-of-sample; sign of change correct.
- Universalization **false-positive** test: no simulated crossing where the observed series did not cross.
- Sign constraints from the relations register (checks, not fits): R13 panel education→growth **negative**;
  R04 income→tertiary **positive**; R02 spending→primary **null**. Violations reported as failures, never tuned away.

## C. Verdict vocabulary (brief 013 §4)
**PASS** = all domain checks within tolerance + exact cohort conservation + timing within ±5y on held-out country
(KHM) and period (2011–2024) + false-positive test passed + naive benchmarks beaten. **PARTIAL** = levels and
conservation pass but out-of-sample or false-positive checks fail → descriptive only. **FAIL** = any conservation
violation, impossible transitions, or out-of-sample miss beyond tolerance → no claim. **EQUIVALENT** = rivals fit the
same moments within tolerance and no predeclared discriminating test separates them → report equivalence, no winner.

## D. Naive benchmarks (brief 013 §5)
Persistence (last observed value), linear trend, constant-transition cohort progression; UIS/WDI modelled series are
description only. Losing to any of these is not a result.

## E. Stop rules adopted (brief 013 STOP_RULES R1–R12)
Out-of-sample failure (R1), conservation (R2), equivalence (R3), supplied-law (R4), no-new-moment (R5), false-positive
universalization (R6), definition break (R7), sector heterogeneity (R8), iteration budget/no identification gain (R9),
pre-trend failure (R10), rival exclusion (R11), no retro-fits (R12). R2 and R12 have already applied: the model's
accounting checks are exact and no target is coded as a parameter (automated B4 check in `pushpull.py`).

## F. Literature targets now registered as declared rival predictions (ACK of lit `PUSH_PULL_TARGETS.csv`)
`10_massification/lit/PUSH_PULL_TARGETS.csv` supplies rival predictions, not parameters. Adopted as declared
sign/ordering checks (never fitted): demand-led predicts a foreign-demand shock produces an origin training boom
(9 licensed nurses per additional migrant; pass rate 38.4%); demand-led predicts a large place premium (3.99) makes
household response rational; both predict expansion tracking returns (8.8%/yr); the lead–lag Granger direction and the
elasticity of formal employment to educated labour supply are **NOT FOUND** in the literature and are therefore
**not available as checks** — that absence is itself a data gap to report, not something to fill with a model value.

## G. Model changes made to satisfy §2 (declared, before fitting)
`pushpull.py` now emits **completion** series (primary/lower/upper) generated from the same cohort flow
(completion_primary = p_pri; lower = p_pri·p_low; upper = p_pri·p_low·p_up) — because brief 013 makes completion the
FIT series and GER a CHECK. The structure smoke was re-run after this change: 0 accounting failures.

## H. What is still blocked / open
1. `04_data/TARGETS_FLOW.csv` and `ECONOMY_SERIES.csv` must be confirmed on disk before the sector-link fit; if
   absent, sector shares fall back to CHECK-only and that is reported.
2. The Council's fit/check table is now registered; **fitting may begin** on the §2 FIT cells only, with KHM held out
   and 2011–2024 held out. Ordering: (i) one-country (PHL) smoke fit to confirm the calibration machinery and
   out-of-sample machinery, (ii) PHL+CHN fit, (iii) rival comparison + equivalence/recovery, (iv) scaling exponents
   (generated vs supplied), (v) push-pull decomposition with the two-shock discriminating design.
