# MODEL ZOO — scope and test protocol (design-only; no compute yet)

**Status: SCOPED, NOT YET PREREGISTERED, NOT RUN.** Operator direction 2026-11-25: test *competing education models*
(not only audit equations). Decision outcomes are **holds / fails / indeterminate-by-context**, never "the model is
wrong". Sequencing: Paper C Pilot-0 → grid/G2-B → Paper C confirmatory → Model Zoo (reusing pilot cells).
Codex has been asked to identify "Kaplan" (test-prep/for-profit supply form vs a named academic model vs
Kaplan–Meier attrition) and to propose the canonical model list + test protocol; this document is our draft scope
until that reply lands. **No Model Zoo computation will run before the preregistration is drafted and Codex replies.**

## 1. Candidate models (declared predictions, discriminating moments, data needs)

| # | model | core claim / prediction set | discriminating moment(s) | data need | planned decision rule |
|---|---|---|---|---|---|
| 1 | **Becker human capital** | schooling/tutoring raises skills and earnings; investment responds to returns | learning/mpl/earnings gradient; completion vs spending | PISA/CEPS learning + earnings returns | fails if learning response absent where spending rises |
| 2 | **Mincer returns** | log earnings linear in schooling/experience | returns coefficient stability across contexts | household survey earnings | indeterminate if no earnings data |
| 3 | **Spence signalling/screening** | credentials matter beyond skills; gate pressure raises investment without learning | elite/track share vs L, contest effort vs L, learning flat | gate + learning data | holds if effort rises with L but learning does not |
| 4 | **Hanushek production function** | school inputs → achievement with diminishing returns | q0/S variation → learning; teacher pay/PTR | PISA school inputs | fails if S variation leaves learning flat |
| 5 | **Hirsch positional competition** | demand driven by relative rank / seats, not absolute skill | gap/spend vs gate share; positional-vs-learning decomposition | contest gate data | holds if spend tracks L, not q |
| 6 | **Bray shadow-education demand** | tutoring demand responds to high-stakes exams + household capacity | own_share/spend vs L and income | HK/PH/KH tutoring data | holds if participation rises with L |
| 7 | **Biswal/Jayachandran withholding** | public teachers withhold lessons when pay gap + sellable | withheld, own_share, q_pub under pay_ratio/own_ban | teacher-pay + tutoring data (thin) | holds if h>0 and own_share rises when sellable |
| 8 | **Kaplan-type test-prep supply** | commercial supply form (for-profit prep) scales with exam stakes and ability to pay | firm_price/firm share vs L and income | prep-market data (thin) | TBD after Codex identification |
| 9 | **China state-provision (DL) model** | state supply crowds out private tutoring | firm/own share vs q0/S, private share | China data (CEPS) | holds if S crowds out private demand |
| 10 | **Household time allocation** | student time is the binding constraint; tutoring trades off work/leisure | time-use vs participation (no current data) | time-use survey | indeterminate (data gap) |

## 2. Test protocol (draft)

1. **Declared prediction set** per model (sign/magnitude on named moments), registered before runs.
2. **Common engine runs** (Pilot-0 cells, grid cells, G2-B runs) as the test bed; no bespoke runs unless registered.
3. **Discriminating moments**: a moment is usable only if two models predict different signs/magnitudes for the same
   parameter change (e.g. L↑: positional → spend↑; human capital → spend flat unless learning returns change).
4. **Evidence layering**: engine simulation (mechanism plausibility), DHS/ILSA evidence (empirical pattern), and
   published estimates (baseline) kept separate; no model "wins" on simulation alone.
5. **Decision rule**: holds / fails / indeterminate-by-context, with the context variables (L, S, supply form) named;
   a fail must be a pre-declared falsification test, not a post-hoc story.
6. **Data-need matrix**: every model marked observed / proxy / theory-only before any claim.
7. **Multiplicity**: family-wise reporting of all models × moments; no selective model reporting.
8. **Paper D** (equation audit) is the *methodological companion*: classify standard equations as identity / stylized
   theory / empirical spec / incomplete-for-mechanism, with divergence tests; the Zoo supplies the competing
   predictions that make those divergences testable.

## 3. What exists vs missing (per the engine-core mapping)

* Engine supports: human-capital learning response, positional contest, own-teacher vs firm supply, withholding
  (pay-gap/incentive), gate pressure, school-quality proxy q0.
* Missing (blocks full Zoo testing): positive school-supply lever S (homework/feedback/supervision/teacher effort),
  student/teacher time budgets, own-vs-firm spend split, teacher hours/workload, clean identification data for
  HK/PH/Cambodia/China (see `TUTORING_DATA_INVENTORY.md`), earnings returns data in-scope.
* Therefore **Pilot-0 is hypothesis-generating only**; Zoo tests requiring missing levers must be marked
  indeterminate/data-blocked until the levers/data exist.
