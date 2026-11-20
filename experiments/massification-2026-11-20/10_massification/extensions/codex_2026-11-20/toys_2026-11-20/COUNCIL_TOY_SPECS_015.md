# 15 NEW TOY-MODEL EXPERIMENTS — Council specification (brief 014 follow-on)

**Status: toy/illustrative only.** These are specifications for small, standard-library, seeded toy models — not
estimates, not calibrations, not evidence, and not a reopening of the closed massification phase. The phase stays
CLOSED (closeout `787f1792…`): direction unidentifiable (R13), income-scaling sign wrong (R27/C1), ceiling residual
14.97 pp UNABLE, capacity floor-not-ceiling (A10/R29), timing censored. These toys are for **mechanism pedagogy and
hypothesis generation**; none may be cited as a finding. Build under `extensions_archive/`; every output labelled
`ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence`.

**Protocol (applies to all 15).** Python 3 stdlib; fixed seeds; **paired** counterfactuals with identical latent
draws; matched starting conditions; one-factor shocks; ≥100 seeds per cell (≥200 where cheap); predeclared threshold
and falsifier written before the run; report all cells including failures; distinguish applications vs admissions,
readiness vs completion, jobs vs output; record the imposed parameter vector in each output. All models are
illustrative; if a toy “confirms” a theory, that is a property of its stipulated rules, not evidence about the world.

---

## Cluster A — Provider entry / supply response (touches C1/R27)

### 1. Entry-threshold hysteresis
**Question:** does private provider entry/exit create asymmetric supply response (fast exit, slow entry) after demand
shocks? **Model change:** in `model.py`, make entry a fixed-cost threshold (`qty·(tuition−varcost) ≥ F`) and let
providers **exit** when the threshold is not met; demand shock ±20% in two periods. **Arms:** F low vs high × shock up
vs down (4 cells). **Estimand:** net private seats and admissions path; entry/exit asymmetry (exit response vs entry
response). **Threshold:** high-F arm shows exit faster/stronger than entry by ≥ a declared margin. **Falsifier:** no
asymmetry (symmetric response) → the fixed-cost story adds nothing. **Link:** C1 supply channel; net≠gross.

### 2. Public expansion with private exit (net vs gross)
**Question:** how much of a public seat expansion survives provider exit? **Model change:** `model.py` with public
seats 30→50 and 38→39; private fixed cost and capacity varied. **Arms:** F low/high × expansion size (2 sizes);
paired. **Estimand:** gross vs net admissions, private exit count. **Threshold:** high-F arm's net gain < 50% of gross
gain (mirror of the 30→50 ~5-net-admissions result). **Falsifier:** no offsetting exit (net ≈ gross). **Link:** the
one toy result most worth generalising; still illustrative.

### 3. Provider entry lag and overshoot
**Question:** does entry lag produce enrolment overshoot/deficit after a demand shock? **Model change:** entry lag
L ∈ {0, 2, 4} cohorts; temporary vs permanent demand shock. **Arms:** L × shock duration (6 cells). **Estimand:**
peak enrolment gap, seats vacancy/backlog, time-to-steady-state. **Threshold:** L=4 overshoots by more than a declared
percentage with the temporary shock. **Falsifier:** lag has no overshoot effect → no dynamic supply story.
**Link:** C1; also explains why capacity-timing tests may fail (A10/R29).

## Cluster B — Rival discrimination (touches C3)

### 4. Visibility × mechanism (HC vs signalling)
**Question:** does employer **skill visibility** separate human-capital from signalling signatures? **Model change:**
`model.py`: HC adds one skill unit per graduate; signalling premium shrinks with visibility v ∈ {0, .5, 1};
employer ranking by visible skill vs credential. **Arms:** 2 mechanisms × 3 visibility levels. **Estimand:** output
among hires, skill of rejected applicants, applications, graduate hires. **Threshold:** predeclared sign pattern: HC
output rises and signalling output falls as v rises; rejected-skill composition differs. **Falsifier:** the two
mechanisms' signatures coincide at all v → no discriminating toy. **Link:** C3; the toy cannot test the world, only
show whether a discriminator is *conceptually* possible.

### 5. Queue vs human capital under fixed jobs
**Question:** with fixed jobs, does upgrading 20 people separate rank-based from skill-based allocation? **Model
change:** `experiments.py` fixed-job check; skill-upgrade vs rank-upgrade; jobs fixed at 35–40, then a responsive-jobs
arm. **Arms:** skill/rank × fixed/responsive (4). **Estimand:** hires of the fixed older-diploma group, output among
hires. **Threshold:** rank lowers older-group hires and output; skill raises output; fixed-jobs output separation
disappears under responsive jobs. **Falsifier:** no separation. **Link:** C3/queue theory.

### 6. Eligibility repeal vs blind ranking
**Question:** is the queue reading sensitive to the gate or to credential visibility? **Model change:** Luna item 5
toy: credential visible at ranking × gate repealed; blind ranking × gate retained; both. **Arms:** 2×2. **Estimand:**
offer rate among uncredentialed applicants; callback/offer counts. **Threshold:** gate repeal raises the
uncredentialed offer rate to the declared high level; blind ranking alone leaves it at the low level. **Falsifier:**
no effect of either → no credential-signalling channel in the toy. **Link:** C3; explicitly a staged screening toy,
not an equilibrium vacancy test.

## Cluster C — Capacity: floor vs ceiling (touches A10/R29, C4)

### 7. Capacity by level (floor/ceiling split)
**Question:** can capacity alone universalize the ceiling, or only the floor? **Model change:** `takeoff.py` capacity
shock applied to primary only / secondary only / tertiary only / all levels. **Arms:** 4 + control. **Estimand:**
cohort-30 counts per level, crossing years/order. **Threshold:** capacity at a level raises that level's completion;
secondary-only capacity does **not** make upper-secondary universal (predeclared: no ceiling universalization from
capacity alone). **Falsifier:** capacity alone universalizes the top level → contradicts A10 (and would reopen the
capacity question). **Link:** A10/R29.

### 8. Enforcement × compulsory law
**Question:** does a compulsory-schooling law bind without enforcement? **Model change:** `takeoff.py`: law 0/1 ×
enforcement e ∈ {0, .5, 1} (probability/capacity of inspection and sanctions); attendance/completion mapping.
**Arms:** 6 cells. **Estimand:** registration, attendance, completion, household work. **Threshold:** law with e=0
≈ no-law; law with e=1 raises attendance/completion by the declared margin. **Falsifier:** law alone binds → enforcement
leg is redundant. **Link:** C4/A9; PHL de jure vs de facto problem.

### 9. Buildings vs teachers under equal budget
**Question:** do physical seats without staff produce usable places? **Model change:** Luna item 4 toy: equal budget
for rooms-only, salaries-only, split; rural retention parameter varied. **Arms:** 3 × retention low/high. **Estimand:**
physical places, staffed places, completion. **Threshold:** rooms-only creates physical seats but no staffed-place or
completion gain; split with better retention dominates. **Falsifier:** rooms alone raise completion. **Link:** A9
delivery dimension; DATA ASK for real construction cost (toy cannot settle it).

## Cluster D — Timing, cohorts, temporary expansion (touches A6/A7/A10)

### 10. Level-first roll-out and crossing order
**Question:** does the *order* in which levels expand change crossing years and the floor/ceiling asymmetry? **Model
change:** `takeoff.py`: primary-first, secondary-first, simultaneous expansions of equal present value. **Arms:** 3.
**Estimand:** M0–M3 crossing years, completion gaps, floor/ceiling ratio. **Threshold:** ordering changes crossing
years by more than a declared band. **Falsifier:** identical crossings → order is not a mechanism. **Link:** A6/A7;
PHL asymmetry.

### 11. Cohort-size shock × capacity
**Question:** does a demographic shock change completion timing only when capacity is frozen? **Model change:**
`takeoff.py`: cohort ±20% × capacity frozen/responsive. **Arms:** 2×2. **Estimand:** completion per child, crossing
years. **Threshold:** demographic effect under frozen capacity, not under responsive. **Falsifier:** no interaction.
**Link:** C2 (timing), A10.

### 12. Temporary expansion with expectations
**Question:** does temporary capacity change applications/hires through expectations even after it ends? **Model
change:** Luna item 7 toy: 12 leased seats for cohorts 2–4; arms supply-only, fee waiver, placement information;
employer responsive vs fixed. **Arms:** 3 × 2. **Estimand:** cohort 5–7 applications, hires, decay to cohorts 16–20.
**Threshold:** information arm raises applications but not hires under fixed jobs; responsive employers raise hires
temporarily. **Falsifier:** no expectation/decay effect. **Link:** A7 (candidate markers need not be laws); the
“temporary push” question.

## Cluster E — Market pull / information / geography

### 13. Migration and remittance route
**Question:** can an external credentialed job route pull schooling while local jobs stay flat? **Model change:**
`diffusion.py`/`takeoff.py`: external route open/closed × remittances on/off. **Arms:** 2×2. **Estimand:** origin
schooling, local output, migrant count (counted once), household resources. **Threshold:** schooling rises with the
route even when local employment is flat; remittances add a smaller, declared effect. **Falsifier:** no schooling
response to the route. **Link:** demand-pull hypothesis; C3-adjacent.

### 14. Sector-demand shock × field access
**Question:** does a demand shock reallocate cohorts to a targeted field, or just raise overall enrolment? **Model
change:** `takeoff.py` with two fields; shock to one occupation; field access/tracking varied. **Arms:** targeted vs
placebo field × open/closed field access. **Estimand:** applications, seats, licensed completers, vacancies proxy.
**Threshold:** field-specific response only when field access is open. **Falsifier:** no field specificity → the shock
is general demand, not a sectoral pull. **Link:** market pull; C3.

### 15. Neighbour information and roads (diffusion)
**Question:** do prestigious-neighbour information, road access and teacher supply have separable effects on
applications? **Model change:** `diffusion.py`: independently vary a prestigious neighbouring school, road access,
teacher supply; tied vs untied villages. **Arms:** 2×2×2 or one-factor at a time. **Estimand:** applications per
household, admissions, completion by distance/kin. **Threshold:** independent effects of the declared signs; kin
transmission is a stipulated assumption and must be labelled. **Falsifier:** no independent effect → diffusion story
collapses to capacity. **Link:** A7/A10; geography of expansion.

---

## Build order (recommended)

1. **#1 entry hysteresis, #2 net vs gross, #7 capacity by level** — cheapest, closest to the two live questions
   (C1 provider supply; A10 floor/ceiling), and they reuse existing scripts.
2. **#4 visibility × mechanism, #5 queue vs HC, #6 eligibility/blind** — the only realistic route to a *conceptual*
   rival discriminator; do them together as one battery.
3. **#10 level-first, #11 cohort shock, #12 temporary expansion** — timing/asymmetry toys.
4. **#3 lags, #8 enforcement, #9 buildings vs teachers, #13 migration, #14 sector, #15 diffusion** — fill out the menu.

## What these toys can and cannot do

- **Can:** show whether a proposed mechanism *could* produce a pattern (net vs gross, floor vs ceiling, visibility
  signatures); generate predeclared predictions for real-data tests; teach the difference between an assumption and a
  result.
- **Cannot:** test any historical claim, calibrate a parameter, or reopen C1–C4. If the user wants to reopen the phase,
  the only admissible next cell is still the **observed provider-entry supply-response test** from brief 014
  (`COUNCIL_REVIEW_014.md` §3.1): entry elasticity first, sign flip second, or a recorded negative. These 15 toys are
  the design space around that cell, not a substitute for it.

**Labelling (mandatory on every output):** `ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence; no
historical test; phase closed; do not cite numbers as estimates.` Build under `extensions_archive/`, never in results
tables, never pushed to the closed branch.

— Council, follow-on to brief 014 (design specification only).
