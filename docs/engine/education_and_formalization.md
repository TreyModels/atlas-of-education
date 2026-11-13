# What does education do for industrialisation? China, Vietnam, the Philippines, Cambodia

Results note, 5 November 2026. Model: `engine/floorworld.py`. Experiment: `engine/floorworld_mc.py` → `engine/results/floorworld_mc.md`. Aggregate toy, not an agent-based model. Policy schedules are stylised inputs; the tests are qualitative patterns.

## The question

Does expanding education create a formal, taxable, complex economy? Or does it pay off only where investment and industrial policy are building one? And which layer of schooling matters: the floor (lower secondary, literacy and numeracy), vocational schools, or universities? Cambodia's version of the question: what did education actually do in China and Vietnam?

## Theories tested (each a separate model structure)

| | Theory | Economists behind it |
|---|---|---|
| S1 | Human-capital-led: formal and complex jobs grow with productive human capital; schooling makes activity legible and taxable | Becker, Mincer; Lucas; James C. Scott on legibility |
| S2 | Demand-led: investment and industrial policy create formal jobs; education fills them | Foster's vocational school fallacy; Pritchett |
| S3 | Complexity: complex jobs need capabilities built by doing, plus enough graduates to staff teams | Hausmann & Hidalgo (personbytes) |
| S4 | Adoption: factory investment locates where the productive floor is; complex jobs as in S3 | Nelson & Phelps (1966) |
| S5 | Hybrid: the floor attracts factories (as S4), but complex jobs follow demand (as S2) | the hypothesis argued in conversation |

Under every theory:
- Each credential has a **signalling share** (Caplan): the part of its value that only reorders who gets which job.
- **Vocational schooling** has four weighted roles: skills, pipeline to employers, protection (Nordtveit), and parking.
- **Learning quality** scales what a year of school teaches (Hanushek & Woessmann).

## Tests: eight patterns that must hold together

| Test | Pattern | Source |
|---|---|---|
| T1 | Complexity, 2018: China above Vietnam and the Philippines, both above Cambodia | Harvard Atlas ECI ranks 18, 52, 35, 90 |
| T2 | Cambodia informal employment 80–95%, 2019 | ILO, 89.4% |
| T3 | Vietnam informal employment 55–80%, 2023 | ILO, 67.7% |
| T4 | Philippine graduates abroad, 1–8% of the workforce, 2023 | PSA, 2.16m overseas Filipino workers |
| T5 | China's graduate surplus rises at least 10 points, 1998→2019 | — |
| T6 | Philippine K-12 adds under 3 points of formal employment, 2015→2023 | PIDS 2023: no effect on the probability of wage work |
| T7 | Undereducation in formal work: Cambodia above Vietnam, 2013 | ILO school-to-work surveys |
| T8 | Overeducation: Vietnam above Cambodia, 2013 | ILO: 23.5% of young Vietnamese workers overeducated |

## Results (6,000 parameter draws, all four countries, each theory)

| Theory | All eight pass | All but one |
|---|---:|---:|
| S2 demand-led | **14.7%** | 1,574 |
| S1 human-capital-led | **10.3%** | 1,316 |
| S5 floor attracts factories, complex jobs follow demand | **0.7%** | 1,817 |
| S3 complexity | 0.03% | 63 |
| S4 adoption | 0% | 9 |

1. **Demand-led explains the four countries most easily.** Formal jobs come from investment and industrial policy; education fills them.
2. **Human-capital-led also fits, but only with its signature mechanism weak.** Where it passes, the "schooling creates formal jobs" effect sits near 0.13 on a 0–0.6 range, so the fit comes from the parts it shares with demand-led. The Philippine K-12 test is the hardest single test for it.
3. **Theories where complex jobs grow with the number of graduates fail.** They cannot produce China's graduate surplus after 1999 (0% pass on T5). Graduates do not create their own complex jobs.
4. **The hybrid fits only in a narrow form.** The floor attracts factory investment only modestly: the attraction strength is tightly constrained at about 0.5–0.65. A strong "educate them and the factories will come" version is ruled out. A moderate one is allowed, and it passes the K-12 test most often (54%).
5. **Caplan is not settled by these patterns.** The tertiary signalling share comes out at about 0.5 with a 0.1–0.8 range under every surviving theory. Country-level patterns cannot separate signalling from productivity. Micro tests can:
   - Philippine Grade 10 leavers' job quality before and after K-12 (bumping down);
   - Chinese non-graduates' absolute incomes during the expansion.
6. **The vocational roles are not identified either.** Their posteriors look like the priors.

## Cambodia to 2035 (change against its own path; surviving theories)

| Policy | Informal employment | Undereducated in factories | Lower-secondary completion |
|---|---|---|---|
| Finish the floor (Vietnam-like) | about −0.5 pts (0 under demand-led) | −2.5 to −3.2 pts | +25 pts |
| Expand universities to 35% | about 0 | 0 | 0 |
| Double zone investment | −4.9 to −9.4 pts | 0 | small |
| Floor + zone investment | **−6 to −9.4 pts** | −2.8 to −3.2 pts | +25 pts |
| Vocational at 30% as parking | 0 | 0 | 0 |
| Vocational at 30% as pipeline + protection | about −0.6 pts | about −0.6 pts | **+6.5 pts** |

Reading:
- **Investment moves formal employment within a decade; the floor does not.** Finishing lower secondary changes only new cohorts entering a 40-year workforce, so its effect on the stock is slow. It is a 20–30-year bet. A planner judging it by 2035 will undervalue it.
- **Universities do nothing for formality or complexity** in any surviving theory, unless complex demand is built separately.
- **Vocational schooling as parking does nothing.** Designed as protection plus pipeline, it raises floor completion by 6.5 points: Nordtveit's protection role doing industrial work.

## Limits

- Aggregate cohorts, not agents.
- The country schedules (floors, investment, emigration) are stylised from documented policy history, not estimated.
- The tests are orderings and ranges, and three of them are qualitative.
- Output per worker barely moves in any experiment: the output block is too crude to be read.
- The 2035 horizon understates floor effects.
- Next refinement: put learning quality and the floor into the investment decision with firm-level evidence, such as investment surveys of SEZ firms in Cambodia and Vietnam.

## Sources

- Harvard Growth Lab ECI rankings via https://wiki.riteme.site/wiki/List_of_countries_by_economic_complexity
- ILO informal employment via https://en.wikipedia.org/wiki/List_of_countries_by_informal_employment_rate
- ILO school-to-work transition surveys (2014 release): https://www.ilo.org/resource/news/young-workers-asia-face-instability-and-vulnerability
- PSA, 2023 overseas Filipino workers: https://psa.gov.ph/content/2023-overseas-filipino-workers-final-results
- PIDS on Philippine senior high school (Philstar, 2023): https://www.philstar.com/headlines/2023/07/12/2280536/senior-high-graduates-more-likely-earn-higher-wages-junior-high-graduates-study
- World Bank on Vietnam's PISA 2012: https://blogs.worldbank.org/en/eastasiapacific/what-explains-vietnam-s-stunning-performance-pisa-2012
- Tertiary enrolment: https://www.indexmundi.com/facts/indicators/SE.TER.ENRR/rankings/asia
- Hanushek, Schwerdt, Woessmann & Zhang (2017): https://hanushek.stanford.edu/publications/general-education-vocational-education-and-labor-market-outcomes-over-life-cycle
- Foster's vocational school fallacy: https://education.stateuniversity.com/pages/2537/Vocational-School-Fallacy.html
- Pritchett (2001): https://ideas.repec.org/a/oup/wbecrv/2001153367--391.html
- Paglayan (2021): https://cambridge.org/core/services/aop-cambridge-core/content/view/8C8C594AA07996A00ED4BEFC66B133B7/S0003055420000647a.pdf/nondemocratic_roots_of_mass_education_evidence_from_200_years.pdf
- Hidalgo on personbytes: https://ethanzuckerman.com/2011/10/12/cesar-hidalgo-on-personbytes-and-knowledge-networks/
- Nordtveit, UMass profile: https://www.umass.edu/education/about/directory/bjorn-h-nordtveit
