# PRE-DECLARATION — pivot to ONE anchor education system, with switchable state-push mechanisms

**Owner:** experiment-runner (`deepseek-exp1`). **Status:** predeclared architecture, **NOT run**. **Origin:** user
directive (logged 2026-11-20): pivot to one anchor education system first — stand it up, show the mechanisms, then
test whether it works for Hong Kong and China. The Council is to name the anchor and the single-system success
criteria; nothing is fitted until both land. This file predeclares the architecture so the build cannot drift while
the Council decides.

## What changes from the current task-37 cells
Current model has two continuous channels (education-led `e_s`, demand-led `e_d`) plus fertility/cohort flow and
declared reduced-form sector equations. The pivot adds **explicit, switchable state-push mechanisms** so that each
mechanism's *contribution and activation timing* can be shown rather than absorbed into a fitted curve, and
restructures the work around one anchor system + two portability checks.

## Anchor system
**TBD by Council** (Lead has asked the Council to name it and set the single-system success criteria). Candidate
logics to be recorded by the Council, not presumed here: PHL has the densest observed target coverage in
`04_data/TARGETS_FLOW.csv` and a dated policy record (RA 10533, 2013); KHM carries the held-out-country role from
brief 013; HKG/CHN are the mandated portability checks. The anchor is *not* chosen by the runner.

## Mechanism set (each declared, switchable, with an activation year from the policy record)
| id | mechanism | switch | activation input | declared parameter(s) |
|---|---|---|---|---|
| M1 | compulsory-law change (e.g. lengthening/compulsory schooling law) | on/off + year | policy date (sourced) | affected cohort cut, compliance rate |
| M2 | school/place expansion (capacity) | on/off + path | capacity path (sourced/estimated) | expansion rate, crowding |
| M3 | teacher supply | on/off + path | teacher stock / PTR path | teacher elasticity of progression |
| M4 | fee abolition / cost change | on/off + path | fee/cost path (sourced) | cost elasticity of intake/continuation |
| M5 | demand pull | on/off (elasticity) | income/jobs path | `e_d`, `lag_d` |
| M6 | supply push (education-led feedback) | on/off (elasticity) | educated stock | `e_s`, `lag_s` |
M1–M4 are **state push**; M5 demand pull; M6 supply push. Each is a separate switch in the code, so any subset can be
activated; no mechanism is hard-wired on. Activation years come from the policy record (declared, sourced), never
fitted. **No target is coded as a parameter.**

## What "show the mechanisms" means (predeclared estimands)
1. **Activation-timing match.** For each mechanism, the model's generated acceleration/crossing response to switching
   it on at its *policy-record* activation year is compared with the observed crossing years / expansion episodes.
   Report per mechanism: whether its activation year is the one that reproduces the observed timing (a within-model
   timing comparison), and its marginal contribution (switch-on minus switch-off) over the observed window.
2. **Decomposition.** Shapley decomposition over the switch set (M1–M6) for the anchor's expansion: share of the
   1980–2020 (or Council-specified window) attainment/enrolment change attributable to state push vs demand pull vs
   supply push, with uncertainty across parameter draws and seeds. Declared weights/contributions only; **no direction
   claim unless identified** (R13/E1; the panel cannot identify direction, so the decomposition is a model
   decomposition, labelled as such).
3. **Identification honesty.** If two mechanisms' activation timings produce indistinguishable paths at the observed
   data, report **EQUIVALENT** for that pair — a timing coincidence is not identification.

## Portability checkpoint (HKG, CHN)
Freeze the anchor's mechanism set and fitted parameters; re-parameterise only the **minimal country-specific inputs**
declared in `configs.py` (TFR path, urbanisation path, cycle lengths, policy activation years where the record
differs). Test HKG and CHN as **checks**, not fits: report what transfers, what fails, and the failure mode. A
portability result that requires re-fitting country-specific mechanism strengths is reported as **not portable**,
not as a success.

## Roles that remain (brief 013 + A1/A4)
FIT: completion PHL+CHN 1980–2010 observed years (unless the Council's anchor criteria change this). HOLDOUT PERIOD:
2011–2024. HOLDOUT COUNTRY: KHM. CHECK-ONLY: KOR/HKG/JPN completion (and, once A4 lands, levels for JPN/KOR/HKG
become check-only with the **timing of universalization** as the holdout outcome, predeclared separately in
`PRE_TIMING_JPN_KOR_HKG.md`); sector shares (WDI/ILO modelled, Amendment §I); A1 scaling exponents (generated, never
supplied — R4). The income-scaling repair (`PRE_SCALING_REPAIR.md`) stays in the plan and remains **not run pending
Council intake acceptance** (D21).

## Success criteria (provisional; Council to set the single-system criteria)
- **PASS (single system):** all of (i) cohort conservation exact; (ii) completion fit/holdout inside brief-013 §3
  tolerances and beating BOTH naive benchmarks; (iii) mechanism decomposition reported with at least one mechanism
  whose activation timing is *required* to reproduce the observed expansion (i.e. switching it off breaks the
  predeclared timing threshold); (iv) no target coded as a parameter, crossing years never fitted. Portability then
  reported separately (does not gate the single-system PASS).
- **PARTIAL:** (i)+(iv) hold but completion/holdout fails a benchmark, or the mechanism-timing test is satisfied by
  more than one mechanism (EQUIVALENT).
- **FAIL:** conservation violation, target-as-parameter, crossing year in fitting, or no mechanism timing matches the
  observed episodes.
- Verdict vocabulary keeps **PASS-CONDITIONAL** (declared mixture, weights declared not fitted) vs **IDENTIFIED**
  (E1 or predeclared E2+E3 pair) from A1.

## Gate and sequencing
1. Council names the anchor system and posts the single-system success criteria (Lead has requested this).
2. Council confirms/amends the mechanism list and activation years.
3. THEN: build the anchor model with switchable M1–M6, run the single-system cells, then portability.
Until (1)–(2) land: nothing is fitted; existing completed cells (PHL smoke `13c93588…`, PHL+CHN batch, scaling-repair
predecl under intake) are not re-labelled (R12).
