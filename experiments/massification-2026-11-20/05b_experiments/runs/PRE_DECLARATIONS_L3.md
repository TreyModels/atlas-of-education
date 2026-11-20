# PRE-DECLARATIONS — Loop 3 (S1 stage-matched checks, S2 non-universality, S3 price/entry)

Written BEFORE any loop-3 run. **NEW module, clearly named:** `loop3/code/shadow3.py` — a declared
structural shadow-incidence model (demand by stage/location + provider market with commercial firms and
teacher-tutors, entry costs, capacity, price tatonnement). It extends the loop-2 design with explicit
stages; it is NOT massabm, NOT floorworld, NOT triad, NOT a reproduction. Timebox ~35 min,
workers ≤ 2 (numpy-only), `PYTHONDONTWRITEBYTECODE=1`, matched seeds 0..4.

## Intake discrepancies corrected from loop 2 (Council brief 005)

1. `02_lit/SHADOW_TARGETS.csv` contains **11 `use_as_model_target=YES` rows**, not 6: KOR all-levels
   78.5, KOR elementary 90, JPN grade-6 41.8, HKG senior 85, KHM grade-9 68.4, KHM primary 41.3,
   KHM primary-urban 60.5, KHM primary-rural 26.4, PHL all-basic 46.5, PHL elementary 23.8,
   PHL upper-sec 28.1. All 11 are reported in S1.
2. The loop-2 provider-entry effect is **54–67 pp** (PH 66.5, HK 53.8, KHM 62.9), not 46–66 pp; the
   loop-2 uncalibrated run produced 46–66 and is superseded. This is corrected here and in the loop-3
   record; no loop-2 file is edited.

## S1 — stage-matched shadow check table (all 11 YES rows + HKG 13-row gradient)

**Question.** Does the model reproduce the literature's stage/provider-matched shadow-education rates?
**Estimand.** Model take-up at the stage/provider the literature row specifies, at the literature year
where the model has a dated equivalent, versus rate_pct; outside/inside the literature low-high range;
`UNABLE TO ASSESS` where no stage-matched model object exists.
**Mapping rules (declared before running).**
- KHM grade-9 → lower-secondary stage; KHM primary / primary-urban / primary-rural → primary stage
  (urban/rural split).
- PHL elementary → primary; PHL upper-secondary → upper-secondary; PHL all-basic → pupil-weighted
  aggregate of primary+lower+upper (model enrolment weights).
- HKG senior-secondary → senior stage. **HK 0.85 is a CALIBRATION, never incidence evidence**; it is
  reported in the table but excluded from the pass/fail count.
- HKG 2010 lower/middle/senior (72/82/85) from `04_data/TARGETS_SHADOW.csv` are checks (the 85 row is
  the calibration). The 1996 HKG rows (45 primary, 26 lower, 34 middle, 40 senior) have **no dated
  model equivalent** (steady-state model) → `UNABLE TO ASSESS`.
- KOR and JPN rows: **no KOR-like or JPN-like structural variant** exists; transferring PH/HK/KHM
  parameters would be an untested transfer → `UNABLE TO ASSESS`.
**Threshold (predeclared).** Assessable countries = HKG, KHM, PHL (3); KOR/JPN `UNABLE`. If **≥2 of the
3 assessable countries** have ≥1 stage-matched row outside its literature range (excluding the HK
calibration), the incidence claim FAILS. (The brief's "≥2 of 4" cannot be applied: only 3 countries
have a stage-matched model variant; KOR/JPN are marked UNABLE, not counted as outside.)
**Prediction before running.** Hopes are low: loop-2 made incidence near-universal, so PHL and KHM
should come out above their ranges → S1 FLAG (fail). Prediction recorded in advance.

## S2 — what makes tutoring non-universal? (structural parameters, no direct take-up setting)

**Question.** Can independently justified country-specific structural parameters reproduce PHL 46.5,
KHM 68.4 and the HKG 72/82/85 gradient **without setting a take-up rate directly**?
**Structural parameters (declared ranges; justified independently of the target).**
gate stakes by stage (0.2–1.5), public-school substitute quality (0–1), household income level and
urban/rural premium (declared from GDP/urbanisation orders), provider entry cost multiplier (0.3–3),
teacher-tutor capacity share (0–1), credential returns by stage (0.1–1.5), plus the demand-elasticity
coefficients (fixed at declared values, not fitted). No parameter is a take-up rate.
**Method.** (a) baseline run per country → miss; (b) one-parameter-at-a-time re-optimisation (grid over
the declared range of each parameter, holding others at baseline) to see which single parameter moves
the model toward the targets and how much; (c) a 600-draw Latin-hypercube-style random search over all
parameters within ranges (declared seed) to find the best joint fit. Targets: PHL {46.5, 23.8, 28.1},
KHM {68.4, 41.3, 60.5, 26.4}, HKG {72, 82} (85 excluded as calibration). Weighted squared error in
percentage points.
**Threshold.** `reproduces` if a structural combination brings every country's target vector to within
**±5 pp** simultaneously; `partial` if within ±10 pp; `none works` otherwise. Report which parameter
does the work and the defensible ordering (stakes/returns must rise with stage; no fitted ordering).
**Prediction before running.** Gate stakes + income + public-school substitute will do most of the work;
PHL is reachable, KHM's teacher-sold 68.4 lower-secondary rate and the HKG gradient are unlikely to be
matched simultaneously → likely `partial` or `none works`.

## S3 — price / provider-entry calibration

**Question.** Can the provider market be made structural (finite price, non-exploding provider count,
sensible teacher share) with entry-cost/capacity parameters, and is the price inside an observed range?
**Grid (declared).** entry-cost multipliers F_cm × F_tt ∈ {0.5, 1, 2, 5, 10}²; capacities cap_cm ∈
{0.5, 1, 2}×, cap_tt ∈ {0.5, 1, 2}×, teacher-capacity multiplier ∈ {0.5, 1, 2}; each country baseline
demand. Estimands at convergence: tutoring price relative to declared income, provider count per 1000
pupils, teacher-tutor share of capacity.
**Observed fee moments.** The only verified fee moments in the target files are Korean (KOR
434k won/month per student; 553k per participant). There is **no verified fee moment for PH, HK or KHM**
and **no KOR model variant**. Therefore the fee comparison is `UNABLE TO ASSESS` unless a grid point
produces a price/income ratio inside a declared plausible band [1%, 15%]; report the grid, the price/
income ratio, and mark `UNABLE` where no observed moment exists. Threshold: price inside observed range
→ pass; no observed moment → `UNABLE` (never called a pass).
**Prediction before running.** The loop-2 block collapsed to the price floor because entry costs were
too low relative to demand; with F multipliers up to 10× the price should stay finite for at least part
of the grid, but provider counts will remain high (tens per 1000 pupils) → the credible-price region
will be narrow and the fee comparison UNABLE.

## Pending loop-2 tests (L2-4 recovery/forced-ID, L2-5 holdout)

Run only if S1–S3 finish inside the timebox. If not run: recorded as pending, not claimed.

## General rules

Matched seeds; sd across replications; failures logged and not dropped; all numbers simulated model
output; no imputed cell used; only observed target cells are compared; every unrun cell is marked
`not run`.
