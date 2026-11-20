# PRE-DECLARATION — A2: state-push event battery (PHL anchor)

**Owner:** experiment-runner (`deepseek-exp1`). **Status:** predeclared before running. **Authority:**
`ANCHOR_SYSTEM.md` §C and `ANCHOR_SLATE.csv` A2 (D38–D42, A5, R20–R22), brief 013 §2–§4, A1/A3/A4. E2 (K-12 cohort
exposure) **folds into A2** per repo-auditor; its claim cap and MDE ruling carry over unchanged.

## Events and arms (all dates exogenous, never fitted — R12/R4)
| test | event (date) | arms | estimand | predeclared sign + band | placebo |
|---|---|---|---|---|---|
| A2a cycle extension | K-12 RA 10533 (2013), SHS 2016–17 | exposed vs unexposed cohorts by birth year (born ≥2000 exposed; ≤1997 unexposed; 1998–99 excluded/placebo) | upper-secondary completion; transition to tertiary | completion falls then rises (definition change), net ≥ MDE 4 pp; tertiary transition falls then recovers | pre-2013 cohorts; lower-secondary completion (mechanically unaffected) |
| A2b fee abolition (SHS) | free SHS (2016) | exposed cohorts vs pre-2016; income quartile differential | upper-secondary intake/completion | rise concentrated in Q1–Q2; declared minimum differential **≥3 pp** between Q1–Q2 and Q4–Q5 | unaffected levels (primary); high-remittance households less responsive |
| A2c fee abolition (tertiary) | free tertiary RA 10931 (2018) | exposed cohorts vs pre-2018; income quartile differential | tertiary intake/transition | rise concentrated in Q1–Q2; minimum differential ≥3 pp | unaffected levels; private-provider share |
| A2d places/teachers | capacity/teacher expansion (dated series) | capacity leads intake with declared lag 2–4 y | enrolment response to capacity | positive lead relation; unmet-demand indicator before, absorbed after | reverse ordering (intake leads capacity) reported as failure |

## Thresholds (predeclared)
- Pre-trends pass: |pre-event slope| < 1 pp/yr over the observed pre-window, or placebo cohort break null
  (|effect| < 2 pp).
- Break sign and magnitude inside the predeclared band above; **MDE claim cap**: PASS only at ≥ MDE ≈4 pp (from the
  E2 power calculation: s=2.5 pp, n_pre≈6, n_post≈6 → SE≈1.44 pp, MDE≈4.0 pp); below = **INCONCLUSIVE** (not support,
  not null).
- Fee effects must be **concentrated** (Q1–Q2 differential ≥3 pp); a uniform rise is reported as consistent with a
  demand trend, not with fee abolition.
- COVID sensitivity (2020–21 overlaps the first full SHS cohort): exclude 2020–2022 and include a COVID indicator;
  a sign flip between the two makes the test **INCONCLUSIVE/COVID-CONFOUNDED**. No re-specification after results.
- **Cohort conservation exact** (zero tolerance); no target coded as a parameter; crossing years never fitted.

## Data and DATA BLOCKED rules
Observed completion 1999–2024 (`TARGETS_FLOW.csv`, status==target) and GMR observed cells are the backbone. DepEd/DPWH
places and teacher series are **not yet on disk** (A8 data-first): A2d is **DATA BLOCKED** until they land; if only
partial, the covered sub-period is reported and the gap declared. No imputation; no modelled series as observations.
Unresolved rows stay excluded (brief 013 §6).

## Rival-comparison link (R3/R13)
A2's event breaks are also the A5 discriminator: the same exogenous events are imposed on the five rival models (HC,
world society, labour queue, state-building, sectoral demand); the anchor must beat them on the event-break estimand
or the result is **EQUIVALENT** — a state-push date coincidence is not identification, and no direction claim is made.

## Roles, tolerances, vocabulary
As reproduced verbatim in `PRE_ANCHOR_A1.md` (brief 013 §2 table + §3 tolerances + A1/A4/A5 additions). Verdicts
PASS / PARTIAL / FAIL / EQUIVALENT (+ PASS-CONDITIONAL / IDENTIFIED); STOP RULES R1–R12, R20–R22.

## AMENDMENT A6 (Council D47–D49) — cohort exposure, not level breaks; null results allowed
Per R23/A6 and scout's event_windows: state-push tests are scored on **cohort exposure** (exposed vs unexposed
cohorts by birth year / stage) and on **crossing years/ordering**, not on level shifts at law dates. Window shifts
computed by scout are recorded as context only (+0.42 pp t=0.50 for K-12 secondary GER; −5.39 pp t=−3.0 for free
tuition, confounded by the K-12 transition; −2.49 pp t=−1.27 for 4Ps). Each event test **predeclares that a null is a
valid result** and carries the MDE power statement (PASS at ≥4 pp, else INCONCLUSIVE). A2a (K-12 cohort exposure) is
the primary state-push test; A2b/A2c (fee abolition) keep the Q1–Q2 concentration rule; A2d (places/teachers) remains
DATA BLOCKED until DepEd/DPWH series land. No test may add the law date as a fitted parameter (R12/R4).
