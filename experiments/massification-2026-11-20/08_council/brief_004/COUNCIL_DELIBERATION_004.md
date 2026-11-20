> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# COUNCIL DELIBERATION 004 — iteration-2 design review

**Panel (AI composites, literature-based):** PAGE (model reasoning), BRAY (shadow education, mandatory), PATRINOS
(education economics; steel-man), CARTWRIGHT (philosophy of social science).
**Input:** `brief_004/BRIEF.md`; `06_report/RESEARCH_LOOP.md` (120 lines, present at 13:07 after a brief absence);
`05_experiments/runs/C1/findings.txt`; `C2/findings.txt`; `C_STATUS.md`; `OPEN_QUESTIONS.md`. No iteration-2
artifacts exist yet.

## Agreed

1. **The loop's architecture is right; its sequencing is fit-first.** A→B→C→D→E is sound, but calibration (C)
   precedes falsification (D) and the Council gate (E) is last. C1 shows why that matters: on six aggregate moments
   the surplus and competitive worlds are equidistant (0.012–0.023), and a truth outside the set is confidently
   assigned to the surplus world (2/2). The target set must label every moment **fit** or **check** *before*
   calibration, with a predicted sign for each candidate world.
2. **C1's forced identification is the programme's most important negative result** and must be a regression test in
   every iteration: include a truth outside the candidate set and report the forced-ID rate.
3. **C2 forces symmetric freezing.** "Supplied attainment, not-from-schooling jobs" is a one-way model. The two-way
   requirement is satisfied only if both freezes are tested: freeze schooling (does the job path still rise?) *and*
   freeze wages/jobs (does attainment still rise?). If either side needs its schedule, call it supplied.
4. **"Change one variable" must mean a structural rule change, not a parameter value.** Otherwise the loop is
   re-parameterisation with a new label.
5. **Shadow incidence is the one place real data can falsify the model.** `RESEARCH_LOOP.md` §2 is well specified,
   but literature ranges are definition-dependent; each target cell needs a source, date, stage/provider definition,
   and a predeclared range. Provider mix and take-up are *checks*, never fit parameters; the fitted objects are
   household demand, supplier entry cost and teacher-tutor capacity.

## Disagreements preserved

**D1. PAGE vs PATRINOS — where identification comes from.**
PAGE: identification is a property of the moment vector; iteration 2 can improve it by adding new moments even before
new data exist (simulated checks can show the contrast). PATRINOS: simulated moments cannot identify a model; at least
two new moments must be real-data and excluded from the fit. *What turns on it:* whether iteration 2 is permitted to
declare "identification gain" from internal simulations. *Resolution:* both — the moment vector must carry real-data
counterparts; simulated moments are labelled "simulation-only check" and cannot support an identification claim.

**D2. BRAY vs PAGE — the softness of literature ranges.**
BRAY: comparative tutoring ranges are survey estimates with inconsistent definitions; a model can land inside a range
by definitional drift. PAGE: still the best available external check; the alternative is no check at all.
*Resolution:* predeclare per-cell definition and range with sources; report the miss; no range may be revised after
seeing the model output.

**D3. PATRINOS vs CARTWRIGHT — the one variable.**
PATRINOS: the single most important change is the **moment set** (new data/moments); more structure without new
moments is re-fitting. CARTWRIGHT: the single most important change is a **structural rule** (the symmetric freeze
test), because a moment set that is still one-way cannot show two-way feedback. BRAY: the provider side is the
missing structural actor — it is both a moment (who supplies the shadow) and a mechanism (entry, teacher-tutor
capacity), and it addresses the paper's own nursing failure. *Resolution:* the single variable = **provider
supply/entry with teacher-tutor capacity** (BRAY's structural candidate, supported by CARTWRIGHT's rule-change
criterion), conditional on PATRINOS's requirement that the country cards deliver provider data; otherwise the
identification question is `UNABLE TO ASSESS` and the loop must report that.

**D4. All — the Council gate should occur twice.** A design gate (this brief) before calibration, and a results gate
after (brief 005). A council that only sees finished runs can audit but cannot prevent manufactured identification.

## Model contest (design-level)

| Question | PAGE | PATRINOS | BRAY | CARTWRIGHT |
|---|---|---|---|---|
| Can iteration 2 identify the worlds? | only with new moments with different predictions | only with real-data moments + holdout | the shadow incidence moment is real but soft | not from one-way schedules; needs symmetric freeze |
| What is the one changed variable? | provider supply/entry | new moment set (data) | provider supply + teacher-tutor capacity | structural rule change, measured by freeze-both |
| What must be predeclared? | moment-to-rival prediction table | fit/check labels, holdout, confusion matrix | ranges/definitions per cell | stop rules (6)–(9), hashed before runs |
| What is publishable now? | design + negative map | measurement/identification note | country cards as comparative measurement | executed cells + identification map |

**Intake note.** `06_report/RESEARCH_LOOP.md` was absent when the task arrived and appeared minutes later; this review
is of its 13:07 state. If it changes, brief 004 is superseded — the amendments are specific enough to apply to a
revised version.
