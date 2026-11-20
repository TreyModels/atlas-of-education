# PRE-DECLARATION — income-scaling channel repair (STRUCTURAL CHANGE, new cell)

**Owner:** experiment-runner (`deepseek-exp1`). **Status:** predeclared, **NOT run**; submitted to Council intake
(repo-auditor instruction 2). **Type: structural change, not parameter tuning.** Authority: Council brief 013,
Amendment **A1** (directive 68e9dfe6), repo-auditor GO; STOP RULES **R4** (supplied law), **R5** (no new moment /
re-parameterisation), **R12** (no retro-fits).

## Why this cell exists (the failure it must repair, recorded before writing any code)
The PHL smoke fit (cell hash `13c93588…`) generated **wrong-sign** OOS income-scaling exponents:
secondary GER~income −1.89 / −0.38 / −0.74 (demand / education / complementary) against the A1 target
**+0.286 (se 0.045)**; tertiary −1.23 / −0.14 / −0.35 against **+0.776 (se 0.086)**. The model would need those
exponents supplied to match them, which R4 forbids. The cause is structural, not numerical: in `pushpull.py`
enrolment is a **cohort-flow stock** (intake × progression × cycle length) while income only enters the
*progression rates*; as simulated GDP grows, the cohort-based stock cannot grow as fast as income, so the ratio turns
negative. Completion calibration cannot repair this (the Lead's instruction: do not tune completion to rescue the
fit).

## The structural change (declared mechanism, one change)
Add an explicit **income-facing participation margin** to the schooling block so that the demand-led and
education-led channels can operate on *entry and continuation* (the observed margins) rather than only on
progression probabilities:
1. **Intake margin:** age-6 intake responds to expected returns / income with elasticity `eta_in` and lag `lag_in`:
   `intake_t = intake_base · (Y_{t-lag_in}/Y_ref)^{eta_in}` (declared reduced form; demand-led channel).
2. **Continuation margin:** progression at each transition responds to the *level* of income, not only its growth
   (already present), with the exponent scaled by the channel:
   `p_k = logistic(a_k + g_k·ln Y + u_k·urban + m_k·ln(1+E_{t-lag}))`, `E` educated share.
3. **Education-led feedback** is unchanged in form but now acts on income growth through the *stock* of education
   (`Δln Y = g0 + e_s·(S_{t-lag_s} − S_ref)`), so the scaling exponents can be positive without imposing them.
No target enters as a parameter. The A1 exponents are **checks**, computed as OOS log–log slopes, never fitted.

## Parameterisation (declared; all free params ranges, never targets)
New parameters: `eta_in ∈ [0,1.5]`, `lag_in ∈ [0,6]`, `m_k ∈ [0,1.5]` for k∈{primary,lower,upper,tertiary};
existing `e_s`, `e_d`, lags retained. Total free parameters: 14 existing + 6 new = 20. They are fitted **only** on the
brief-013 FIT cells (completion, PHL+CHN, 1980–2010 observed years), never on the scaling exponents.

## Roles that remain unchanged (brief 013 §2 / A1 — reproduced)
FIT: completion primary/lower/upper, PHL+CHN, observed years 1980–2010. HOLDOUT PERIOD: 2011–2024 (untouched by the
repair). HOLDOUT COUNTRY: **KHM, all observed years, never fitted**. CHECK only: KOR/HKG/JPN completion, GER/flow
proxies all countries, sector shares (WDI/ILO modelled; CHECK-only per Amendment §I), and the **A1 scaling
exponents** (secondary +0.286, tertiary +0.776, completion logit law) which must be **generated**, not supplied.
**The scaling exponents are never fit; the holdout period and KHM are never used in the repair fit.**

## What counts as PASS / PARTIAL / FAIL (predeclared)
- **PASS (repair works):** the repaired structural version (i) keeps completion fit/holdout inside brief-013 §3
  tolerances; (ii) **generates** secondary and tertiary income exponents within **±1 se of the A1 values**
  (|e_gen − e_A1| ≤ 1·se) out of sample; (iii) keeps cohort-flow conservation exact; (iv) KHM held-out completion
  within the §3 out-of-sample tolerance; (v) no target was coded as a parameter. Only then may scaling be described
  as *generated*.
- **PARTIAL:** (i) and (iii)–(v) hold but one or both exponents differ by 1–3 se, or the sign is now right but the
  magnitude is outside 1 se → scaling is *partially generated*; descriptive only.
- **FAIL:** exponent still wrong-signed, or any conservation violation, or completion/holdout tolerances broken by the
  change, or the repair requires the exponent as an input (R4 violation).
- **EQUIVALENT:** if the repair improves scaling only because it adds a free channel with no new discriminating
  moment (R5), report EQUIVALENT to the unrepaired model and do **not** claim a repair.

## R4 / R5 / R12 links
- **R4:** the A1 exponents are checks; if the repaired model cannot generate them, report the failure and do not
  insert them. A model that "matches" only because the relation is an input schedule gets FAIL, not PASS.
- **R5:** the repair must add a *new discriminating moment*, not just parameters. The predeclared discriminator is the
  **OOS income-scaling exponent set** (two exponents + the completion logit slope) evaluated on 2011–2024 — a moment
  not used in fitting. If the repair only improves the fit of the same completion moments, it is EQUIVALENT.
- **R12:** no retro-fit. The unrepaired results (PHL smoke fit hash `13c93588…`, PHL+CHN batch) remain in the record
  and are not re-labelled; the repaired cell is reported alongside with its own hash and verdict.

## Data and cost
No new data required: uses the same observed completion target rows (`04_data/TARGETS_FLOW.csv`, `status==target`)
and the same model. Cost ≈ 1 calibration run (pooled PHL+CHN, 3 rivals) + 1 OOS scaling evaluation per rival;
≤ ~10 minutes compute at workers≤2. **Submitted to Council intake; do not run until accepted.**
