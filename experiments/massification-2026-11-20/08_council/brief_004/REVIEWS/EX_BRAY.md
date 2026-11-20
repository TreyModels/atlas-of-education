> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# REVIEW — BRAY composite (drawing on Bray & Lykins 2012; Bray's comparative work; Bray & Zhang) — brief_004

**G. GROUNDING.** Literature basis: shadow education is stage-specific, gate-anchored, supplied by commercial firms
and teacher-tutors, culturally embedded, and it expands as an industry; take-up rates vary widely by country and
stage and are measured inconsistently. **COUNCIL EXTRAPOLATION:** the assessment of the loop's shadow-incidence
criterion is the composite's.

**M. MODEL RENDERING.** To say "shadow education appears where the literature says", the model needs: M1 stage- and
country-specific take-up (who tutors, at which gate), M2 provider mix as an outcome of demand and capacity
(commercial entry, teacher-tutor time, informal), M3 spending and hours that scale with income and stakes, M4 gate
position (upper-secondary/tertiary entrance vs basic completion), M5 the sector's own expansion (entry), M6 a
predeclared literature range per cell and a miss report, M7 KIDS: the country card describes the tutoring market
before it is modelled.

**A. VERDICTS.** (a) The operationalisation in `RESEARCH_LOOP.md` §2 is **sound and unusually well specified** — it
is the first place in the programme where shadow education is treated as an *outcome* rather than a coded response.
But it has an empirical soft spot: the "literature range" is a range of survey estimates with different definitions
(tutoring type, subject, hours vs spend, stage). If the country cards do not fix the definition per cell, the model
can land inside a range by definitional drift. (b) Iteration 2's anti-re-parameterisation test for tutoring is stop
rule 5 ("the target was coded as a parameter") — that is the right rule, and the loop should add: provider mix and
take-up are *checks*, never fit parameters; the fitted parameters are household demand, supplier entry cost and
teacher-tutor capacity, not the shares themselves. (c) On China: the substitution elasticity remains the
unidentified object; the loop must not reintroduce the Double Reduction claim as a target. Mark it "needs data", not
"to be calibrated".

**B. WHAT IS IMPOSED.** "Shadow education appears" is easy to impose: a demand function with a gate-anchored price
will produce clustering by construction (that was iteration 1). The discovery would be the *level* and *provider
composition* by stage and country, generated without setting the shares. If take-up ranges are met only by tuning
the tutoring-cost function, that is re-parameterisation; report it as such.

**C. ESTIMAND.** Take-up share of gate-takers, by stage and provider type; spending and hours; provider entry. Units
must be stated (share of age cohort vs share of enrolled vs share of examinees) — the literature mixes them.

**D. TYPE.** The country cards are measurement; the take-up match is a model check, not evidence about a country
unless the moment is a real-data target excluded from the fit.

**E. STRONGEST DEFENSIBLE SENTENCE.** "Given a predeclared national range for take-up by stage, the model generates
take-up inside it with provider composition as an outcome of demand and capacity, not as a fitted share; where it
misses, the miss is reported."

**F. NEGATIVE.** The provider side is the weak link: teacher-tutoring is a large share of the market in Cambodia and
the Philippines, and the iteration-1 model has no teacher-tutor channel. A model that hits take-up with commercial
firms only will be wrong about who supplies the shadow — which is exactly what the comparative literature documents.

**G2. STEEL-MAN.** The strongest defence of targeting incidence: it is the one place where the programme can be
falsified by real data rather than by internal consistency; that is why it is worth doing even with soft ranges.

**H. ALTERNATIVE.** Tutoring may be driven more by school quality and social competition than by gate position
(Bray's comparative record); the model should be able to miss the gate-position check and say so.

**I. WHAT WOULD CHANGE MY MIND.** Country cards with stage × provider take-up series and a predeclared range per
cell; a model that hits the range without fitting the share; a disclosed miss in at least one country.
