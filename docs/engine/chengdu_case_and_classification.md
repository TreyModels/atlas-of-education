# Chengdu as the architecture test, and one classification for China and Cambodia

5 November 2026. Design note, not results. Built from Trey's dictated notes of 5 Nov and two documents read in full from his Drive: *Confronting a Durable Educational Inequality* (the 2014 baseline draft, last saved Oct 2016, with several empty sections) and *Huizhi Preliminary Report2* (June 2016, 2014 vs 2016 TOEFL Junior). Claims about Cambodia are Trey's propositions to document, not findings; no citation has been checked.

## 1. The classification: where a child can get to, not who the child is

Two things get conflated. **Categories** are what the boundary rules read: registration (hukou), urban/rural, income quintile, sex, ethnicity (the Tilly vector, TODO §9). **Tracks** are the farthest gate a child is likely to clear. Tracks are an output of the model, defined the same way in every country:

| Track | Clears | Typical China content | Typical Cambodia content |
|---|---|---|---|
| T4 | the scarce selective gate (top university, overseas) | key-school academic route, very small share | Phnom Penh private/foreign route |
| T3 | the mass academic gate | ordinary academic upper secondary, gaokao | Bac II, public university |
| T2 | the short vocational/tertiary gate | secondary vocational (about six in ten upper-secondary students), two-year colleges | technical/TVET, garment and construction ladders |
| T1 | none, but stays enrolled to the gate | at-risk, Lewin's zone 6 | at-risk, lower-secondary repeaters |
| T0 | left before the gate | Lewin zones 4 and 5 | the dropout and child-labour class |

Lewin's zones are positions along the path; the four states A-D (school, both, work, neither) are what a child does with a year. Track is the forward-looking summary of both. "The bar has moved" then has a precise form: the share of each cohort in T2 and T3 changes when a country adds seats, relabels vocational schools, or raises the floor. China's move of the T0/T1 group into vocational schools and two-year colleges is a change in the T2 gate's capacity and rule, not in those children.

## 2. Shadow education as one continuous variable

Let **p** be the share of the curriculum a child can only get by paying: withheld by the teacher and sold back (Cambodia, as Trey describes it), sold by firms (China before the 2021 double reduction), or supplied at home by parent time and money (China after it). The second variable is the **payee**: teacher, firm, or household. Double reduction moved payee, not p.

Two testable links, both missing from the Atlas now (`camchild` treats tutoring only as a cost, `tutorFix` only as removing it):

- **Supply side:** p rises as the teacher's budget gap rises (official pay minus living cost minus the school's ability to meet payroll). Cambodia's 2014-18 teacher pay changes, already listed in TODO §6, are the natural test: p should fall where pay rose most.
- **Demand side:** demand for the private portion rises with the stakes of the next gate and with the share of the gate exam that depends on content delivered privately.

A child who cannot buy the private part has a lower effective quality of free schooling. That lowers the value of school for the poorest and is a channel from fee-free policy to dropout that a fee-only model misses.

## 3. Out-of-school time and what prohibition acts on

Out-of-school hours go to market work, family enterprise, domestic care or nothing. A ban closes the market-work margin only where inspectors reach, and never touches domestic care. The model has the first part (`ban`, `formalJobs`) and hides the second inside state D. Adding an hours margin (already a TODO §10 item) makes the cross-country question sharp: where the legal system keeps children in a school or vocational slot until 15 or 16, out-of-school time is near zero and exit shows up as unmeasured idleness or domestic care, not child labour. The Sobol run (`results/childworld_sobol.md`) found the value of state D is the stiffest parameter for three of the four outcomes (not for the share of child labourers who are also in school), which says the same thing from the other side.

## 4. The Chengdu chain, and what it must reproduce first

Starting position (registration, income, prior learning, school access, cost) -> school and teaching (turnover, preparation, curriculum level, remedial help) -> assessment (learning to reported score, with a floor) -> next gate (Zhongkao, seats by route, cost of each) -> later outcome. The model should reproduce these documented facts before any intervention is compared; each is a target with a source:

| Fact | Source | Value |
|---|---|---|
| Below-A2 share at baseline | draft | 32% (+/-5%) of 253; 44% at Zhongke Yucai, 22% at Jitou |
| Class-size loss grade 6 to 7 | draft | 28% Xingguang, 36% Zhongke Yucai, +3% Jitou; mean 20% |
| Loss grade 6 to 9 (max to min) | draft | 60% Zhongke Yucai, 49% Xingguang, mean 37% |
| Zhongkao English expectation | draft | 29% think they will not pass, 31% unsure; one pilot school mean 60/150, pass mark 90 |
| Household cost | draft | about 14% of migrant household income (one child), double with two |
| Mean score change 2014 to 2016 | report | total 674 to 667 (-1%); price-sorting of pupils and teachers across schools given as the explanation |
| Teacher turnover | draft/report | every sampled Zhongke Yucai teacher under two years' tenure in 2014 |

The assessment layer needs its own observation equation (TODO §3). From the draft: a 42-item short form (10 listening, 12 form and meaning, 20 reading) rather than the 126-item standard test; guessers not removed, and a 25% chance floor on four-option items; the school means for three of five schools sat below what random guessing would give; the CEFR mapping starts at A2, so "below A2" is the lowest band reported and cannot separate pupils beneath it. A score cannot distinguish learning beneath the floor, so an intervention that moves pupils from nothing to a little is invisible to the instrument. That is Trey's 2014 point, and it becomes a testable property: the model should say how large a true gain is needed before the reported score moves.

## 5. Ledgers

A school account (government transfer, local revenue, household payments, donors in; payroll, buildings, utilities, materials out) and a household account (fees, transport, tutoring, forgone earnings, borrowing). Without them neither "who pays" for the Chengdu or Cambodian schools nor the payroll point (a building funded, no one to pay the teacher) can be asked. This is the school-level half of TODO §0 "one ledger" and §6 "financing closure".

## 6. Items in the two documents to reconcile before they become calibration targets

- The school lists differ: the 2014 draft names Jitou, Shuhui, Xingguang, Zhongke Yucai and Chongyiqiao; the 2016 report names Xishu, Xingguang, Yangfan, Shuhui and Zhongke Yucai. Check whether these are spelling variants, replacements or different samples.
- The report gives declines in counts of over 100% (for example "decrease by 128%"), which is impossible for a count; the measure needs redefining before use.
- The draft's fee line adds a tuition of 1,200 "every semester" to meals, transport and uniform and calls the total (2,260) yearly. If the 1,200 is per semester the annual figure is higher.
- The bottom-quartile education spending of "371%" of income needs its definition checked against the CHFS source.
- The draft's By School, Teachers, Beliefs, and Interpretation sections are empty or stubs; the figures behind them are not in the document.
- The draft describes migrants as "overwhelmingly white collar workers", which reads as a slip for blue collar.
- The note that the full TOEFL Junior test "would imply about a 10% margin of error" is an assertion, not a computed interval.

## 7. What this does to the plan

Nothing here needs a new engine. It needs: one gate-reach classification used by `childworld`, `camchild` and the Chengdu case; the variable p with a payee; an hours margin; two ledgers; and an assessment observation equation. Chengdu is built as a small case (one city, one grade band, a handful of schools) and must pass its reproduction table before any intervention is run. The first phase stays the cross-country question of school exit without child labour against overlap; Chengdu is the second, smaller case that tests the same architecture on documented fieldwork.
