# Blocker and acquisition needs — fitted-worlds feasibility pilot (task-24)

**The blocker is data/construct availability, NOT compute.** Stage 1 of the pre-registered
fitted-worlds pilot failed with **"insufficient evidence"** (`STAGE1_CONSTRUCT_AUDIT.md`,
`RUN_REPORT.md`; pre-registration `953a382`; audit commit `155bc0a`). The four literature
worlds differ mainly in the **school / work / tutoring decomposition** of the child state
(school only; school+work; work only; hidden work). The committed observed data contain
**no series for study-and-work, work-only or hidden work**, have **no age/grade dimension** to
match the age-specific observed constructs, and provide no **learning scale** or harmonised
**tutoring** panel. More CPU cannot fix this: the question has no measurement-compatible
target in the current panels.

No fitting, synthetic-recovery, rejection-ABC, model-free benchmark, timing pilot or server
run was executed (region-42 was not used; 0 s; nothing server-only exists).

## Acquisition needs (ordered by leverage for the fitted-worlds question)

1. **Age/grade-structured model output** (or a declared, testable age-aggregation rule) so
   UCW **7–14** child-labour states and primary/secondary enrolment can be mapped to model
   states without inventing an age rule.
2. **ILO-UCW study-and-work and work-only shares** as a harmonised country-year panel — the
   decomposition that distinguishes the four worlds. The committed cache has only **total**
   child employment (ILO/UCW via WDI: 100 countries, 281 observations, 1994–2016, median 2
   obs/country).
3. **A learning-scale anchor**: an explicit, out-of-sample-validated mapping between model
   grade-equivalents and an observed learning measure (WDI harmonized test scores / HCI /
   LAYS).
4. **A harmonised cross-country tutoring / shadow-education panel** (current data are 6
   countries/sites of hand-collected case studies).
5. **DHS birth-interval microdata (IR/BH files) for Phase B B1** — **already pending** as a
   separate DHS microdata request; this is the real path for the birth-history observables,
   not more compute. Until it arrives, B1 remains unmatched and B2/B3 remain partial
   (PPR not published; mean CEB by education is a different quantity).
6. **Consistent data vintages/periods across constructs** so a frozen, non-overlapping
   train/validation split (≥20 training, ≥10 independent validation countries) can be defined.

Only after (1)–(6) are available should a new pre-registration be written for any fitting
stage; the current five-stage design must not be launched against invented targets.

## Status of the rest of the pilot

| stage | status |
|---|---|
| 1 construct/feasibility audit | **FAIL — insufficient evidence** |
| 2 frozen split | not launched |
| 3 synthetic-recovery challenge | not launched |
| 4 bounded equal-budget rejection-ABC | not launched |
| 5 model-free benchmark | not launched |
| timing pilot / server draws | not run (no draw/cores commitment) |

Labels: EXPLORATORY. No confirmatory claim, no causal claim, no E1 1.8% comparison, no theory
ranking. Region-42 remains idle and can be stopped (关机, not 释放) by Trey; no server-side
artefact is needed for any of the above.
