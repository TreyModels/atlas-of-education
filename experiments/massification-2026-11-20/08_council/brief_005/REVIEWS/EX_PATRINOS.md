> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# REVIEW — PATRINOS composite (drawing on Psacharopoulos & Patrinos 2018; Becker 1964; steel-man seat) — brief_005

**G. GROUNDING.** Literature basis: identification is a property of the contrast; a parameter fitted to a target and
then reported as a match is a restatement; external validity needs a holdout. **COUNCIL EXTRAPOLATION:** the
restatement audit below is the composite's.

**M. MODEL RENDERING.** M1 fitted parameters must be listed with the moment each was solved against; M2 every
literature target must be labelled fit or check *before* the run; M3 checks are compared stage-by-stage with
predeclared tolerances; M4 a holdout (fit 1980–2010, test 2011–2024) and a recovery test with a truth outside the
candidate set are required before any identification claim; M5 the cohort ledger must conserve persons and match the
flow targets. Any of these absent → the corresponding claim is UNABLE TO ASSESS.

**A. RESTATEMENT TEST — the answer is yes, at one cell, and only one cell is even tested.**
- `SHADOW_TARGETS.csv` has **11** rows with `use_as_model_target=YES`, not 6 (verified count). The Lead's signal
  understates the register.
- `twoway.py` wires exactly **one** literature shadow rate into the model: the HK senior-secondary 0.85
  (`targets=dict(tutoring_senior_sec=0.85)`; bisection in Amendment L2-3). It is the **calibration target**, so the
  match is by construction. **Restated, not generated.**
- The other ten YES rows (KOR 78.5/90; JPN 41.8; KHM 68.4/41.3/60.5/26.4; PHL 46.5/23.8/28.1) appear in **no**
  model target dictionary (`COUNTRIES` configs carry completion/tertiary/GER/formal share/attainment only) and are
  **not reported as checks**. So the restatement test is worse than "one fitted": ten of eleven literature shadow
  rates are unused, and the model's generated PH/KHM take-up (0.884/0.887) is never compared with them. Stage-matched,
  that comparison is a miss by tens of points (PH college-gate 0.899 vs review-centre 28.1%; KHM senior 0.887 vs
  Grade-9 68.4% and primary 41.3%).
- KOR and JPN have cards but no simulation run, so their targets cannot be checked at all.

**B. FIT/CHECK DISCIPLINE.** The brief-004 requirement (label targets before calibration; report checks) is **not
met** in this artifact. `TARGETS_SHADOW.csv` carries status labels (target/check/unresolved) but the module ignores
them except for HK 0.85. `TARGETS_FLOW.csv` is mostly `unresolved` or `proxy — do not calibrate`, so flow checks are
absent. The GMR completion misses are reported (PH −0.089; KHM +0.099) — good — but the shadow checks are not.

**C. COHORT FLOWS.** UNABLE TO ASSESS: the longitudinal cohort ledger is in the pending runner-1 layer. Internally,
the module's completion paths miss observed GMR (PH 0.661 vs 0.750; KHM 0.378 vs 0.279), and the flow targets are
proxies or unresolved, so no conservation/consistency judgment is possible yet.

**D. TYPE.** The direction decomposition and take-up levels are within-model; no identification from them. The HK
"demand-led" label is a one-country classifier outcome, not an estimate.

**E. STRONGEST DEFENSIBLE SENTENCE.** "In this module, take-up can be calibrated to one verified HK rate by a single
common intercept; the other ten literature shadow targets are unused, the PH/KHM take-up levels are contradicted by
the stage-matched literature, and the two-way and identification claims are pending the holdout and recovery runs."

**F. NEGATIVE.** The 54–67 pp entry effect (not 46–66 as signalled) is the largest behavioural number in the batch,
and it coincides with prices at their floor and provider counts up to 90× — a parameter block that cannot be read as
economics until calibrated.

**G2. STEEL-MAN.** The country cards and target register are serious measurement work: sourced, dated, with
provenance and NOT-FOUND flags. The failure is in the model's use of them, not in the cards.

**H. ALTERNATIVE.** The model may simply be unable to represent stage-specific take-up without a second moment
(provider mix); adding a check on teacher share would make the shadow pattern an outcome rather than a correlate of
the intercept.

**I. WHAT WOULD CHANGE MY MIND.** A check table with all 11 rows, stage-matched, plus the holdout and recovery runs;
a predeclared tolerance for each check.
