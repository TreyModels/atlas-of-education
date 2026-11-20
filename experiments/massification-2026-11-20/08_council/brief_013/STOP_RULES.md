> **SYNTHETIC EXERCISE — DESIGN DOCUMENT.** Panelists are AI-constructed composite personas; nothing here is a
> statement by, or endorsed by, the named individuals.

# STOP RULES — massification-first phase (declared before fitting)

**Status:** binding alongside `SUCCESS_CRITERIA.md`; declared 2026-11-20 before any fit. Programme starts from the
prior phase's identification limits (`06_report/LOOP_CLOSEOUT.md`, brief 008); no prior shadow-education rule is
reopened.

| # | Rule (condition → action) | Evidence cell / trigger |
|---|---|---|
| **R1** | **Out-of-sample failure:** held-out MAE > 8 pp, or worse than naive persistence/trend → no country/general claim; report failure | `SUCCESS_CRITERIA.md` §3–§4 |
| **R2** | **Cohort conservation:** any stock-identity or cohort-conservation residual ≠ 0, or any transition rate outside [0,1], or negative stocks → model invalid; stop and fix; no results from the run | runner's balance checks |
| **R3** | **Equivalence:** push and pull rivals fit the same moments equally (no predeclared discriminating test survives) → report **observational equivalence**, do not claim a direction | two-shock design / recovery test |
| **R4** | **Supplied law:** if the model reproduces a scaling relation only because that relation enters as an input schedule/parameter → not a finding; model must generate the relation as output | scaling check design |
| **R5** | **No new moment:** if an "improvement" comes only from adding/tuning parameters without a new discriminating moment → stop; that is re-parameterisation | fit/check table |
| **R6** | **Universalization false positive:** model generates universalization where observed series did not → structural failure; no claim until fixed | false-positive test |
| **R7** | **Measurement/definition break:** series definitions change across the window without harmonisation, or only imputed/modelled cells exist → exclude the series; no claim from it | data ledger |
| **R8** | **Sector heterogeneity unresolved:** if sector patterns cannot be reconciled by the model (and no data explain the misfit) → descriptive only | sector fit |
| **R9** | **Iteration budget:** two consecutive iterations without an **identification gain** (defined: a predeclared threshold passed on a moment *not used in fitting*) → stop claiming the mechanism; publish the equivalence/negative map | iteration log |
| **R10** | **Pre-trend failure:** in event-study designs, if pre-trends reject at the predeclared level → no causal claim; downgrade to correlational/descriptive | event-study diagnostics |
| **R11** | **Rival exclusion:** if any fair rival is structurally barred (different population, information, shock, or outcome) → the comparison is void; re-specify before reporting | rival-matching audit |
| **R12** | **No retro-fits:** no target may become a parameter; no post-hoc change of the fit/holdout split; no quiet re-labelling of an out-of-sample miss as a "calibration issue" | predeclaration hashes |

## Publishable results — positive

1. An **identified** push or pull effect with pre-trends passing, placebo outcomes clean, and a predeclared
   falsifier — e.g., an exogenous demand shock raising schooling in exposed cohorts/regions, or a supply shock raising
   completions and (or not) employment.
2. A **scaling regularity validated out of sample** (e.g., logistic shape with country-specific timing beating
   linear/exponential on held-out countries), reported with its heterogeneity.
3. A **universalization timing result**: which state-capacity/income/demand conditions predict the crossing year,
   tested out of country.
4. A **two-shock interaction** showing complementarity (demand response larger where supply expanded) with the
   interaction sign predeclared.

## Publishable results — negative

1. **Equivalence**: push and pull are observationally equivalent on all available moments; the honest product is an
   equivalence/identification-limits map (the prior phase's main output, now for massification).
2. **Null**: no detectable demand→schooling (or schooling→jobs) response in a well-powered design.
3. **Model failure**: model loses to naive benchmarks or fails universalization timing out of country.
4. **Scaling failure**: the logistic/candidate law fails out of sample, or exponents are not stable across
   countries/sectors → report regularity, not law.
5. **Data limits**: the needed series do not exist in usable form (definitions, coverage) → publish the measurement
   gap and the design that would close it.

## Gate

task-37 cannot fit before `SUCCESS_CRITERIA.md` is registered and acknowledged; the runner must copy §2–§4 of that
file into its own predeclaration and report every R1–R12 trigger in its results table, including the ones that did not
fire.


## Amendment A1 (2026-11-20 14:34) — R13–R14 (forced-ID intake)

| # | Rule | Trigger |
|---|---|---|
| **R13** | **Direction claims from cross-country/panel moments are barred:** if a recovery/forced-ID test shows the estimator assigns channels confidently without identification (forced-ID > 0), no push/pull/complementarity claim may be made from those moments; report EQUIVALENT and require E1 (or the predeclared E2+E3 pair) | model2 recovery: forced-ID 1.00, recovery complementary 0.00 |
| **R14** | **Scaling-exponent reproduction is a gate, not decoration:** if the model cannot generate the classified scaling laws (secondary GER ~ income +0.286; tertiary +0.776; lower-sec completion law) within the estimator range and with country-specific timing, the universalization reproduction claim is capped at PARTIAL | `scaling_classification.csv` |
| **R15** | **Conditional-labelling:** any reproduction claim made under a declared channel mixture must be labelled PASS-CONDITIONAL; presenting it as identified is a rule violation | A1 §3 |


## Amendment A2 (2026-11-20 14:52) — R16–R18 (loop-5 outcomes)

| # | Rule | Trigger |
|---|---|---|
| **R16** | **Interaction-estimator sufficiency:** a two-shock design may be fielded as an identification gate only if its predeclared recovery test passes sign accuracy, median bias, coverage and null-FP thresholds. Failure = do not field; a redesigned estimator requires a NEW predeclaration and its own recovery test, and the current reduction (conditional reproduction + equivalence) stands until it passes | M2c: median abs bias 0.55 > 0.50 (predeclared); sigma=1.0 sign accuracy 0.74/0.68 |
| **R17** | **Scaling repair must be structural:** if generated OOS exponents have the wrong sign, the reproduction claim is capped at PARTIAL; only a new predeclared structural channel may repair it — never exponent fitting, never target-to-parameter, holdout untouched | task-37 scaling_check FAILED: secondary -1.89/-0.38/-0.74 vs +0.286; tertiary -1.23/-0.14/-0.35 vs +0.776 |
| **R18** | **Smoke-fit status:** a fit that loses to the linear-trend benchmark on holdout is PARTIAL at best, regardless of in-sample fit; no PASS, no direction claim | task-37: holdout MAE 4.84/5.40/6.08 vs linear-trend 4.35 (persistence 8.60) |


## Amendment A3 (2026-11-20 15:02) — R19 (timing regime)

| # | Rule | Trigger |
|---|---|---|
| **R19** | **Timing miss is a structural miss:** for near-universal systems, if the model does not reproduce the observed universalization crossing years within the declared timing tolerances (or violates a left-censored boundary / produces a false crossing), the reproduction claim is FAIL for that country/milestone; report the timing miss explicitly. No level-only victory may be reported as reproducing universalization in a near-universal system. | `UNIVERSALIZATION_MILESTONES.md`; A4 |


## Amendment A4 (2026-11-20 15:20) — R20–R22 (anchor/portability)

| # | Rule | Trigger |
|---|---|---|
| **R20** | **Portability requires fixed behaviour:** if the transferred model needs behavioural re-fitting, extra free parameters, or target fitting to match HKG/CHN, portability FAILS; report which parameter had to move. Only declared country inputs may re-set | A5 §3 |
| **R21** | **Mechanism events are exogenous, predeclared and falsifiable:** state-push/demand-pull dates enter as inputs; the model's event break must be predeclared (sign, band, placebo); fitting an event's effect to the outcome is a rule violation (R4/R12); a trajectory match without event breaks is not "mechanisms shown" | A5 §2 |
| **R22** | **Anchor-first:** no portability claim before the anchor (PHL) passes its trajectory, scaling, timing and mechanism-event criteria; E1-class identification stays secondary until then | user directive; A5 §1 |


## Amendment A5 (2026-11-20 15:40) — R23 (anchor asymmetry)

| # | Rule | Trigger |
|---|---|---|
| **R23** | **Single-curve / symmetric-universalization failure:** for the anchor, if the model cannot reproduce the milestone **ordering and gaps** (primary ~2017, lower-secondary ~2024, upper-secondary never by 2024, tertiary GER ~2024–25), the anchor reproduction claim is at most PARTIAL; a single shared curve/timing is a structural miss, and generating upper-secondary universalization the record does not show is a false-positive failure (R6) | A6; verified PHL completion series |


## Amendment A6 (2026-11-20 15:50) — R24–R25 (timing alignment; event-window evidence)

| # | Rule | Trigger |
|---|---|---|
| **R24** | **Timing-alignment rule:** a state-push law may be presented as a mechanism only if its event window is computable on the affected level's observed series, the shift sign matches the prediction, and the event-to-crossing gap is within ±5 y (or the crossing is inside the post window), with affected cohorts declared. Otherwise it is a candidate marker/context, not a mechanism; the anchor's state push must be justified this way or abandoned (A7) | event_windows.csv: PHL 1987 (−31 y), PHL K-12 (mass ≤1999), PHL 2018 (negative, confounded), CHN 1986 (−27 y) |
| **R25** | **Event-window evidence is descriptive:** naive SEs ignore serial correlation; no control groups; quality A/B/C. No causal claim (R13), never supplied as model schedules (R4/R14). Quality C inferred episodes (SCHOOL_EXPANSION missing) may not serve as event evidence | EVENT_WINDOWS.md §1/§6 |


## Amendment A7 (2026-11-20 16:00) — R26 (capacity channel)

| # | Rule | Trigger |
|---|---|---|
| **R26** | **Capacity channel (teacher supply/PTR) is provisional and level-specific:** it may be a R24 candidate only where the affected level's observed series and a computable capacity path align with that level's crossing; it is an **expansion marker** (not a universalization mechanism) where the level never crossed the universalization threshold; approximate hiring counts must be labelled `check`/medium and never treated as exact policy events; school/classroom counts remain UNABLE (DATA ASK) | SCHOOL_EXPANSION.csv batch-1: HS PTR 37→27→24; ~200k/40k hires; DepEd 403 |
