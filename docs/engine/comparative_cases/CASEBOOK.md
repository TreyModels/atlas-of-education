# Reconstructing education and economic change across cases

Research assembly, 3 November 2026. Based on the supplied Atlas v0.4/v0.4.2 archives, their historical paper and specifications, and the primary sources linked below. Model designs and proposed tests are our deductions from those sources. This assembly adds a runnable institutional-timing benchmark; the remaining behavioural modules are specifications awaiting implementation and estimation.

## What these cases contribute

The cases suggest a shared system in which households choose education, institutions decide which programmes to offer, employers change hiring requirements, and governments finance and regulate access. Migration connects this system to foreign labour demand. Each country's history supplies particular interventions, institutional rules and initial conditions. We should estimate the responses and retain failures when a mechanism cannot reproduce them.

| Case | Historical change | Mechanism to test | Outcomes that discriminate between explanations |
|---|---|---|---|
| Philippines, nursing | Changes in access to US employment | Migration expectations, programme entry, licensing | Programmes, enrolment, pass rates, licensed stock, emigrants |
| Philippines, K12 | Two additional school years and later college entry | Cohort timing, grandfathering, credential recognition | First-time college entrants, total enrolment, work transitions |
| Hong Kong, 334 | Shorter school cycle and longer university cycle | Overlapping cohorts, separate admission tracks | Entrants and occupied university places by track |
| Kenya, free primary | Public fee abolition in 2003 | Affordability, congestion, household sorting, private entry | Completion, sector enrolment, fees, achievement conditional on composition |
| Indonesia, INPRES | School construction in 1973–78 | Distance/capacity constraints and later earnings | Cohort-by-region schooling and adult wages |
| Mexico, PROGRESA | Conditional schooling transfers | Dynamic household choices and opportunity costs | Experimental schooling responses by age and sex |
| Pakistan, report cards | Information about child and school achievement | Beliefs, school pricing and quality response | Fees, scores, enrolment at village level |
| China, graduate expansion | Larger graduate cohorts alongside changing demand | Skilled production, job queues, participation | Wages, unemployment, inactivity and underemployment separately |
| Cambodia, upgrading | Education expansion in a changing sector structure | Complementarity of skills, investment and productive jobs | Sector employment, productivity, task demand, learning and earnings |

## Philippines: nursing and the institutions supplying qualifications

Abarcar and Theoharides exploit changes in US nurse migration opportunities and differences in Philippine provinces' historical migration networks. Their published study reports roughly nine additional licensed nurses for each additional emigrant. Expansion included nursing programmes at existing private institutions; pass rates declined. The estimate concerns additional licensing relative to additional migration. Domestic employment and patient outcomes require further evidence. [1]

The archived massification paper reports that its nursing simulation produces approximately 0.25 additional licensed nurses per emigrant. That is a recorded model failure. Re-estimation must first establish that both calculations use comparable time windows and denominators.

Implement programme-specific capacity, institutional entry costs, instructor availability and licensing. A school's programme decision could follow expected discounted fee revenue less instruction, accreditation and setup costs. Expected migration income belongs in households' programme choices, with visa probabilities and recruitment costs explicitly represented. Courses take time to complete; visas can tighten while students remain enrolled.

A useful capacity law is

    K[p,t+1] = (1-depreciation[p]) K[p,t] + new_seats[p,t]
    new_seats[p,t] = entry_response(expected_profit[p,t], instructors[p,t], accreditation[p,t]).

This is a proposed behavioural relationship. Its slope requires evidence. Licensing should depend on student preparation, instruction and the exam threshold. Falling pass rates could arise from changes in entrants' preparation, deterioration in instruction, or both. Record those channels separately.

Fit the pre-expansion institutional distribution. Predict the expansion and subsequent contraction with the same response rules. Score programme counts and pass rates alongside licensing and migration. A fitted nine-to-one ratio alone leaves most of the mechanism unidentified.

## Philippines: K12, recognition and the college-enrolment dip

DepEd's 2015 eligibility order explicitly accommodates old-curriculum graduates and early SHS adopters in 2016–17. Consequently, a rule requiring every applicant to complete twelve years on the reform date misstates transition eligibility. [2] CHED's published series records 4,104,841 higher-education students in 2015–16, 2,981,803 in 2017–18 and 3,408,425 in 2019–20. These are enrolment stocks across disciplines, compiled from institutional submissions. [3]

The accompanying cohort script implements two extra school years for cohorts whose old-system college entry would occur from 2016 onward. With 100 students per cohort and four-year degrees, new entrants fall to zero in 2016 and 2017 and resume in 2018. Enrolled students fall from 400 to 200 and remain at 200 through 2019 before recovering. Real entrants include grandfathered applicants, returners and early adopters. The synthetic trough therefore provides an accounting reference with deliberately restrictive assumptions.

The observed headcount decline is about 27.4%, followed by approximately 14.3% recovery through 2019–20. Explaining that path requires first-time entrants by prior curriculum, progression, programme duration and returners. Population changes and reporting coverage also enter. Free-tertiary policy must apply to eligible institutions and students; a generic fee reduction across all colleges distorts incidence.

Recognition needs a matrix indexed by credential vintage, employer or admitting institution, occupation and year. The Civil Service Commission's 2025 revision explicitly changes qualification equivalences for specified posts. [4] Use the circular's effective date and exclusions when encoding it. A national credential floor cannot capture grandfathering or regulated-profession requirements.

PIDS research using eight Labour Force Survey rounds from July 2018 to April 2020 finds over 70% of SHS graduates continued education and only just over 20% entered the labour force; comparative employment results were mixed. Its weighting/regression approach depends on selection assumptions. [5] The model should reproduce continued study, employment and inactivity with their respective denominators before interpreting SHS as a terminal labour qualification.

## Hong Kong: the paired timing experiment and examination competition

The government's transition plan provided separate pools of 14,500 first-year first-degree places for old Form 7 and new Senior Secondary 3 leavers entering in 2012/13. Total planned places doubled to 29,000. [6] The new senior-secondary structure began in 2009, followed by the first HKDSE in 2012. [7]

Represent the last old school cohort and first new cohort as distinct tracks. Old university programmes last three years; new programmes last four. The supplied script conserves cohort membership and checks the simultaneous intake. It also demonstrates how separate admission quotas leave some capacity unfilled when one track has fewer applicants, even if the other is oversubscribed. A pooled allocation would produce a different result.

For the older tutoring case, Bray and Kwok's survey documents paid supplementary academic tutoring and its variation across school stages. [8] It supports a descriptive benchmark with the survey's own sample and definitions. Causal effects on learning require additional identification. The archived grade mapping needs reconciliation with the old system's S6–S7 stage: compressing it into one upper-secondary year changes exposure and examination timing.

Model examination preparation as increasing a score through learning and exam-specific preparation. Admission depends on a gate-specific ranking or threshold. Track the gain in learning independently from the change in admission probability. Government-aided and Direct Subsidy Scheme schools also need their own funding and admissions rules before being mapped into a generic public/private choice model.

## Kenya: fee abolition, sorting and provider entry

Lucas and Mbiti find that the 2003 free-primary reform increased completion and access for disadvantaged students and encouraged private-school entry, exploiting district differences in pre-reform dropout. [9] Bold and colleagues examine public/private enrolment and fees and find patterns consistent with household sorting after fee abolition. [10] Completion and public net enrolment describe different margins; a model must retain both.

Set the abolished fee to zero while recording other household costs. Track public resources per pupil as entry changes. Let families value distance, expected instruction and peer composition, with capacity limiting feasible choices. Private providers may adjust fees, seats and entry in response to residual demand. Government grants need actual funding and timing rules.

Prespecify tests for public entry by poorer children, movement to private provision, primary completion and achievement among comparable pupils. An aggregate mean score can change when newly included students differ in preparation. Decompose changes within comparable groups and changes in group weights.

The existing Kenya-like tutoring configuration is a starting point for institutional rules. A reconstruction of the 2003 intervention needs dated fee, funding and cohort data. Its eight-year primary cycle places the secondary transition after grade 8.

## Indonesia: school access with later labour-market consequences

Duflo's INPRES study combines regional construction intensity with cohort exposure. Each school constructed per 1,000 children is associated with an estimated 0.12–0.19 additional years of education and 1.5–2.7% higher wages across specifications. These ranges describe reported estimates across specifications. [11]

Model the geographic supply constraint using school distance, places, teachers and construction dates. Households respond to travel costs and access. Later wage outcomes should follow the affected cohorts into labour markets. A generic education-to-wage coefficient can reproduce a mean while missing the programme's differential effect by age at construction and region.

Reproduce the study's exposure comparison, including cohorts too old to benefit. Estimate the schooling response first, then use the wage response as a further test under explicitly stated assumptions about migration, selection into paid work and local economic trends. Scaling these local effects to national growth requires a labour-demand response and other equilibrium adjustments.

## Mexico: PROGRESA as a model-validation template

Todd and Wolpin estimate a dynamic schooling/fertility model without post-programme outcomes and compare its predicted subsidy impacts with experimental estimates. [12] This provides a practical validation design for the Atlas.

Use pre-intervention data to estimate schooling costs, household resources, preferences and relevant expectations. Implement the transfer's actual eligibility, attendance conditions and grade/sex schedule. Freeze parameters before predicting post-treatment schooling. Score responses across age and sex, along with programme cost. Preserve discrepancy rather than adjusting preferences to reproduce the held-out result.

For the Philippine 4Ps module, the archived uniform transfer event needs comparison with programme-specific rules and evaluations. The official DSWD repository contains experimental and subsequent evaluation materials. [13] A detailed 4Ps replication remains a separate extraction task; this assembly does not transfer Mexico's response coefficients to Philippine households.

## Pakistan: information changes the education market

Andrabi, Das and Khwaja's randomized village-level report-card intervention increased achievement by 0.11 standard deviations and reduced private fees by 17%; the reported primary-enrolment increase was 4.5%. [14] Preserve the paper's outcome definitions when extracting regression-level targets.

Add imperfect information about school quality. Parents update beliefs when report cards arrive; schools respond through price and instructional choices. Freeze physical capacity initially to test whether information alone generates the correct direction of household sorting and prices. Then permit entry and expansion with implementation lags.

Use village-level treatment assignment as the simulation unit and allow responses by untreated schools within treated markets. A household-by-household treatment model would miss market interactions. The simultaneous achievement and fee results constrain explanations: an arbitrary fixed quality premium for private schooling cannot by itself explain their joint movement after information changes.

## Bringing China and Cambodia into the same system

The earlier China diagnostic already shows that the integrated engine's queue and competitive-wage options generate different outcomes from a graduate supply shock. Current reduced-form vacancy paths cannot explain the creation of skilled work. The comparative cases add institutional supply responses, geographic access and credible policy-validation designs.

For China, distinguish productive skills from credentials and track employment, search, inactivity and further study by cohort and region. Licensing in nursing illustrates an occupation-specific eligibility gate. Hong Kong illustrates an admissions gate. Their rules should remain institution-specific when constructing the Chinese employer-screening mechanism.

For Cambodia, production and investment must create labour demand. A candidate sector model is

    Y[s,t] = A[s,t] * F_s(capital[s,t], skilled_labour[s,t], other_labour[s,t], intermediates[s,t]).

Choose technology by sector and test substitutions using evidence. Firms' hiring follows expected sales, wages, capital and financing conditions. Training can change task capability, but adopting skill-intensive production may also require capital, management and market access. Represent those complements explicitly before drawing a conclusion about an education trap.

A weather shock can affect agricultural output, household income, food prices and government revenue. Export demand, construction finance and migration opportunities require distinct shocks and transmission paths. Estimate the channels using observed sector and household outcomes where possible. Imported scenario paths must be labelled as imposed inputs when interpreting counterfactuals.

## Shared mathematical and empirical contract

A cohort accounting identity governs every country:

    enrolled[g,t+1] = promoted_into[g,t] + repeaters[g,t] + returning[g,t]
                       - exits_before_next_census[g,t].

Specify the census timing so flows are mutually exclusive. Skills and credentials need separate states. Labour-force membership determines the unemployment denominator; a graduate waiting queue may include people who fail the survey's active-search criterion.

Each historical intervention should have a versioned record: announcement, legal start, implementation, affected cohorts, eligibility exceptions, financing, and measured outcomes. Household income and public revenue need feedback from production and work if the model claims to explain the two-way economy–education relationship.

A benchmark record should contain source, table or page, sample, period, unit, denominator, estimator, uncertainty and whether it was used for calibration. Missing standard errors prevent a formal statistical pass/fail claim. Literature point estimates can still guide directional diagnostics. The code must distinguish accounting assertions from empirical validation.

Evaluate mechanisms against multiple outcomes, hold out intervention periods where possible, and report which relationships were imposed. Cross-country tests should change measured institutions and initial conditions before permitting country-specific behavioural parameters. If parameters must differ, document the evidence supporting that change.

## What to build next, in order

1. Integrate the cohort calendar and credential-vintage matrix. Use the Philippine/Hong Kong timing checks supplied here as regression tests. Extract college entrants and progression to explain the observed Philippine stock path.
2. Add programme entry, instructor constraints and licensing. Re-run the archived Philippine nursing failure with both migration episodes held out in turn.
3. Implement Kenya's fee/funding intervention and Pakistan's information intervention in a shared school-choice/provider module. Test fees and composition jointly with attendance and learning.
4. Adopt PROGRESA's pre-intervention estimation/held-out-policy validation discipline. Use INPRES to test geographic capacity constraints and longer-run consequences.
5. Connect sector production, investment and labour demand to the education system for China and Cambodia. Preserve a transparent reduced-form baseline for comparison.

Myanmar, Angola and Djibouti remain documentary comparators for changes in school-cycle length. The supplied paper mentions them, but this research pass has not verified their complete legislative and implementation sequences. Nigeria's demographic and measurement questions also need a distinct evidence packet. These cases should enter the scored benchmark registry after those gaps are resolved.

## Sources and access notes

1. Abarcar and Theoharides, *Medical Worker Migration and Origin-Country Human Capital: Evidence from U.S. Visa Policy*, Review of Economics and Statistics 106(1), 2024, 20–35. [Author manuscript, September 2021, opened](https://www.amherst.edu/system/files/2021_09_12_draft_FINAL_submit.pdf). Version-specific numerical extraction should use the published paper when available.
2. [DepEd Order 42, s.2015, official eligibility order](https://www.deped.gov.ph/2015/09/11/do-42-s-2015-high-school-graduates-who-are-eligible-to-enrol-in-higher-education-institutions-in-school-year-sy-2016-2017/). Official indexed text consulted.
3. [CHED, Higher Education Data and Indicators AY2009–10 to AY2019–20](https://legacy.ched.gov.ph/wp-content/uploads/Higher-Education-Data-and-Indicators-AY-2009-10-to-AY-2019-20.pdf). PDF table opened; five years transcribed in accompanying JSON.
4. [Civil Service Commission, revised qualification standards](https://www.csc.gov.ph/csc-revises-qualification-standards-to-allow-senior-high-school-graduates-entry-into-government-service). [2025 memorandum circulars](https://www.csc.gov.ph/phocadownload/userupload/irmo/mc/2025/2025%20CSC%20Memorandum%20Circulars.pdf). Official indexed text consulted; full occupation-by-occupation coding pending.
5. Orbeta and Potestad, *On the Employability of Senior High School Graduates in the Philippines*, 2025. [PIDS article abstract opened](https://www.pids.gov.ph/publication/philippine-journal-of-development/on-the-employability-of-senior-high-school-graduates-in-the-philippines-evidence-from-the-labor-force-survey).
6. [Hong Kong Legislative Council paper CB(2)665/09–10(01), paragraph 26](https://www.legco.gov.hk/yr09-10/english/panels/ed/papers/ed0111cb2-665-1-e.pdf). Official indexed passage retrieved; direct PDF fetch failed. Planned quotas, not measured realised admissions.
7. [Hong Kong government, 3 July 2009](https://www.info.gov.hk/gia/general/200907/03/P200907030255.htm). Official indexed text consulted.
8. Bray and Kwok (2003), *Demand for Private Supplementary Tutoring: Conceptual Considerations, and Socio-Economic Patterns in Hong Kong*, Economics of Education Review 22, 611–620. [Author-hosted PDF opened](https://web.edu.hku.hk/f/staff/376/Bray_&_Kwok_Tutoring_EER_1.pdf).
9. Lucas and Mbiti (2012), *Access, Sorting, and Achievement*. [AEA abstract retrieved](https://www.aeaweb.org/articles?id=10.1257/app.4.4.226).
10. Bold, Kimenyi, Mwabu and Sandefur (2015), *Can Free Provision Reduce Demand for Public Services? Evidence from Kenyan Education*. [Publisher abstract](https://doi.org/10.1093/wber/lht038); [authors' working-paper page](https://www.cgdev.org/publication/why-did-abolishing-fees-not-increase-public-school-enrollment-kenya-working-paper-271). Indexed summaries consulted.
11. Duflo (2001), *Schooling and Labor Market Consequences of School Construction in Indonesia*. [AEA abstract retrieved](https://www.aeaweb.org/articles?id=10.1257/aer.91.4.795). Exact regression table and standard-error extraction pending.
12. Todd and Wolpin (2006), *Assessing the Impact of a School Subsidy Program in Mexico*. [AEA abstract retrieved](https://www.aeaweb.org/articles?id=10.1257/aer.96.5.1384). Full replication/data audit pending.
13. [DSWD Pantawid evaluation repository](https://pantawid.dswd.gov.ph/downloadables-3/). Located; evaluations not reviewed in depth in this assembly.
14. Andrabi, Das and Khwaja (2017), *Report Cards: The Impact of Providing School and Child Test Scores on Educational Markets*. [Authors' institutional abstract retrieved](https://www.hks.harvard.edu/publications/report-cards-impact-providing-school-and-child-test-scores-educational-markets-0); [AEA](https://www.aeaweb.org/articles?id=10.1257/aer.20140774).
