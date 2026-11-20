> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# COUNCIL DELIBERATION 013 — design review, massification-first programme

**Panel (AI composites):** LUTZ (demography/education statistics), PATRINOS (identification; steel-man), PAGE
(scaling/model), CARTWRIGHT (falsifiability/definitions).
**Input:** `10_massification/README.md`; `06_report/LOOP_CLOSEOUT.md`; briefs 003–012; on-disk intake
(`10_massification/relations/data/universalization_fits.csv`, `universalization_common_shape.csv`;
`10_massification/model2/PRE_DECLARATIONS_M2.md`) — provisional, no `NEW:` post yet; `04_data/` targets/economy
series; `09_relations/RELATION_CANDIDATES.csv`.

## Agreed

1. **The gate is the right instrument and is binding.** `SUCCESS_CRITERIA.md` + `STOP_RULES.md` are declared before
   fitting; task-37/38 are cleared only on ACK, and the runners must copy the fit/check/holdout table and tolerances
   into their own predeclaration verbatim.
2. **What must differ from the previous phase:** identification before calibration; within-country/cohort/sector
   variation rather than more national aggregates; predeclared fit/check/holdout; scaling as constraint not input;
   equivalence publishable; model must beat naive benchmarks and the false-positive test.
3. **Push-pull identification:** the two-shock design (E1) is the only configuration that identifies both directions
   against each other; E2 (K-12 supply) and E3 (nurse-visa demand) are the cheap single-direction tests that must be
   predeclared as a pair if E1 is delayed. Fair rivals (human capital, world culture, labour queue, sectoral demand,
   migration) are listed and may not be structurally barred (R11).
4. **Scaling:** bounded diffusion is a candidate form, not a law; the on-disk fits show form fragility (PHL
   secondary prefers Gompertz, primary logistic, tertiary unstable) and country-specific slopes are rejected for
   secondary/tertiary but not for upper-secondary/NER (low power). Relations constrain as excluded moments, sign
   constraints (R13 negative education→growth; R04 positive; R02 null) and out-of-sample targets — never as inputs.
5. **Completion is primary, GER is a check** (LUTZ) — GER denominators are the recurring trap; KHM holdout is right
   but its series breaks need verification before use.
6. **Equivalence is publishable** (R3), and "reproduces" is not "explains".

## Disagreements preserved

**D1. PATRINOS vs the E1-first ranking.** PATRINOS: E1 is underpowered at national scale and data assembly may slip;
run E2+E3 first as the identification pair and E1 as integration with a power calculation. Council/PAGE: E1 remains
the flagship in the slate; the resolution is to predeclare E2+E3 as the fallback pair with the joint interpretation,
and to require E1's power calculation before it is fielded.

**D2. LUTZ vs CARTWRIGHT on thresholds.** LUTZ: completion thresholds (95/90/90) are defensible conventions but must
be stated as declared; CARTWRIGHT: add a sensitivity run (90/85/85) as a precondition for any "reproduces
universalization" sentence. Resolution: thresholds declared as conventions; sensitivity required in the results
table, not necessarily as a separate experiment.

**D3. PAGE vs the slate's size.** PAGE: eight experiments overreach the fleet; sequence them (E2+E3 → E1 → E6 → E4)
rather than parallelising. Others concur; Lead assigns with sequence.

**D4. CARTWRIGHT on rules.** No dissent on substance; add the threshold-sensitivity precondition to the stop-rule
table (recorded; Lead may implement as an OP requirement).

## Resolution

The gate stands as written (`SUCCESS_CRITERIA.md`, `STOP_RULES.md`); the slate in `EXPERIMENT_SLATE.csv` stands with
E1 as the single most important test and E2+E3 as the predeclared pair if E1 is delayed. New Lead executor
(`deepseek-audit`) is directed to assign, post `OP:` milestones, and enforce the `NEW:`/`ACK:` loop; pattern-scout and
exp2 must post `NEW:` for the universalization fits and scaling predeclaration before those numbers are used as
targets.
