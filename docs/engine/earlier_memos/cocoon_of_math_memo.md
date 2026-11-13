# The cocoon of math: economic models around the Education Atlas

Nov 3, 2026 · @James W. Menefee III

## The two-way loop

&#91;embedded content: economy and schools loop · 7 links, 1 computed\]

The lines run both ways because you asked for both: Cambodia's economy should explain its schools, and the schools should explain part of the economy. Reading the drawing top to bottom, the economy reaches the schools through four links, all of which the engine takes as coded inputs. The one link it computes is the return path from skill to wages.

## Goal by goal: who demands, who supplies, what clears

Of ten areas in the EFA, MDG and SDG 4 frames, the Atlas has demand, supply and a clearing rule for two, part of the loop for four, and none for four. "Clearing" means what equalises want and availability: a price, a queue, or a quota.

The goals are the six Dakar EFA goals (2000, due 2015), MDG 2 and 3 as I remember them (not re-checked here), and the SDG 4 targets as listed in the [official indicator list](https://apa.sdg4education2030.org/sites/apa.sdg4education2030.org/files/2021-07/SDG4_indicator_list.pdf). The demand and supply columns are standard economic reasoning, not quotations.

| Goal | Demand: who wants it, what moves it | Supply: who provides it, what limits it | What clears it | Model that supplies the curve | Atlas today |
| --- | --- | --- | --- | --- | --- |
| Early childhood (EFA 1; SDG 4.2) | Parents: income, mother's job options, belief in school readiness | Community, NGO and private centres; thin state provision | Fees and rationing by distance | Household childcare-and-work choice; early-skill complementarity (not sourced here) | **No**: engine starts at primary entry |
| Primary and secondary completion (EFA 2; MDG 2; SDG 4.1.2) | Households: out-of-pocket cost against expected earnings, and the child's own earnings. Falls as income rises (child labour is a luxury-axiom problem) | State seats, teachers, distance; fee-charging by schools | Mostly **quantity rationing** on the supply side, plus household cost on the demand side | Becker-Mincer investment; Lucas 1988 (skills have external effects, so households under-invest); child-labour models | **Mostly**: household backward induction, public seats, fees, gates. Missing: wage feedback from the labour market |
| Youth and adult skills, TVET, tertiary (EFA 3; SDG 4.3, 4.4) | Employers: skill-biased demand. Youth: the pay-off and job odds | Institutions and quotas (China's gaokao quota is the clear case) | **Relative wage** (skill premium) and **queue** | Katz-Murphy supply-and-demand for skill; Harris-Todaro queue; search and matching | **Partly**: quotas, tracks, a graduate queue. Wages are fixed ratios, so no price clears |
| Adult literacy (EFA 4; SDG 4.6) | Adults: low return, high time cost | Programmes, usually donor or NGO funded | Programme availability | Adult-learning cost-benefit (not sourced here) | **No**: engine follows youth cohorts |
| Gender and equity (EFA 5; MDG 3; SDG 4.5) | Household preferences by sex; marriage-market and wage returns by sex; wealth | Distance, safety, toilets, teachers | Household cost against returns by group | Intra-household bargaining and returns-by-sex models (not sourced here) | **Partly**: wealth parity yes; **no sex** in the model |
| Quality and learning (EFA 6; SDG 4.1.1) | Parents buy extra quality: private schools, tutoring | Teacher effort, class size, peers | **Price** in private schooling and tutoring; peers sort | Epple-Romano school competition; tutoring and teacher-incentive models (Biswal, Jayachandran) | **Mostly**: learning accumulates, tutoring and private schools clear by price |
| Qualified teachers (SDG 4.c; indicator 4.c.5 is teacher pay relative to comparable professions) | Schools: staffing norm, pupils per teacher | Graduates choosing teaching against outside wages; training capacity | **Relative wage**, with recruitment delay | Teacher labour-market models; EPSSim staffing rule | **Partly**: pay gap and budget set teachers. No teacher stock or recruitment delay yet |
| Public financing (SDG 4.5.4) | Ministry claims on revenue; aid | Tax capacity, which depends on the formal economy | Budget constraint | Fiscal capacity (Besley-Persson); CGE government closure | **Partly**: the fiscal loop exists, but the country packs use a coded budget path |
| Facilities and safe schools (SDG 4.a) | Communities | Capital spending, construction | Budget and queue for classrooms | EPSSim classroom requirements | **No** |
| Scholarships and aid (SDG 4.b, 4.5.5) | Students abroad; donors' priorities | Donor budgets | Aid allocation | Aid-allocation models | **No** |

Target 4.7 (education for sustainable development) is not an economic market and is left out.

## The models that supply those curves

Three families fill the Atlas's gaps: skill prices (who gets paid what as supply changes), vacancy creation (where jobs come from), and the macro closure that ties incomes, taxes and budgets together. Each row says what the model assumes about supply and demand, and what it would add.

| Model | What it assumes | What it would add to the Atlas |
| --- | --- | --- |
| Becker-Mincer human-capital investment (standard; not re-fetched) | A person invests in schooling until the marginal return equals the marginal cost, including forgone earnings | Already the core of household demand; needs a wage that responds to supply |
| [Lucas 1988](https://users.ssc.wisc.edu/~cengel/Econ702/LucasDevelopment.pdf) | Each worker splits time between producing and building skill; skill grows at a rate proportional to time spent; average skill raises everyone's productivity | A test of under-investment: with the external effect, households choose less schooling than a planner would. His U.S. calibration put the external elasticity near 0.4 |
| [Katz-Murphy and Goldin-Katz](https://www.nber.org/papers/w26705) | Relative demand for educated labour grows with skill-biased technology; relative supply grows with schooling; the wage premium is the price that reconciles them | An endogenous graduate premium instead of fixed wage ratios; the "race" is the supply-demand mechanism behind the premium |
| [Heckman-Lochner-Taber 1998](https://www.nber.org/papers/w6384) | Schooling choice, skill supply and skill prices are determined together; skill prices and measured wages can move in opposite directions | The feedback you asked for: more graduates change the price of graduate skill, which changes who studies |
| [Harris-Todaro](https://dev-ii-seminar.readthedocs.io/en/latest/notebooks/HarrisTodaro.html) | The formal wage is held above the market-clearing level, jobs are allocated by lottery, and entrants keep coming until the expected formal wage equals the alternative | The Atlas's graduate queue is this logic; the formal equilibrium condition would become a test it must satisfy |
| [Search and matching](https://m.nber.org/conferences/2007/si2007/EFRSW/mortenson.pdf) (Diamond-Mortensen-Pissarides) | Unemployed workers and vacancies meet through a matching function; firms post vacancies until expected profit is zero; the wage splits the surplus | Vacancies that respond to profitability instead of the Atlas's coded vacancy path |
| [Epple-Romano 1998](https://ideas.repec.org/a/aea/aecrev/v88y1998i1p33-62.html) | Public schools are free and tax-financed; private schools are tuition-financed; achievement depends on own ability and peers | A prediction to test: vouchers enlarge the private sector and increase sorting |
| [MAMS](https://isap.iges.or.jp/2009/en/pdf/day1/26s105_Lofgren.pdf) (World Bank) | A dynamic-recursive general-equilibrium model: students stay, pass, repeat or drop out depending on services per student, private consumption, infrastructure and wage incentives; labour-force composition feeds productivity; closures are chosen by the modeller | The reference design for "economy drives education and back"; its closure options are the template |
| [IFs education](https://ifs.du.edu/ifs/help/understand/education/equations.html) (Pardee) | Flow rates, as shares of the age-appropriate population, follow per-capita income, budget allocation and cohort size along S-curves; schooling feeds fertility, mortality, productivity and governance | A second reference run: if the Atlas and IFs disagree on Cambodia, that disagreement is informative |
| [EPSSim](https://unesdoc.unesco.org/ark:/48223/pf0000214778) (UNESCO) | Pupil flows from intake and flow rates; teachers, rooms and materials from norms; unit costs give financing needs and gaps | Already built as the planning kernel; the Atlas is the behavioural layer it lacks |
| [Cohort-component with education](https://www.demographic-research.org/volumes/vol22/15/default.htm) (Wittgenstein/IIASA) | Population by age, sex and education level; fertility and mortality vary by education | The population denominator and the education-fertility link; the abstract does not say whether it includes economic feedback |
| CGE closures ([overview](https://www.open.edu/openlearncreate/mod/page/view.php?id=214558)) | Savings-driven or investment-driven investment; government balance either fixed or accommodating; fixed trade balance or fixed exchange rate | The rule for what gives when the budget, savings or trade do not balance; without a closure the model has no solution |

Two cautions. The [Cambodia CGE study at CDRI](https://cdri.org.kh/publication/cambodia-macroeconomic-impacts-of-public-consumption-on-education-a-computable-general-equilibrium-approach) uses a social accounting matrix, the household survey and the economic census, but I could read only its abstract, so I cannot say how it treats the labour market. And none of these models claims its behavioural assumptions are beyond dispute; what they share is an accounting closure that holds by construction.

## Cambodia: what the economy is doing, and what the engine takes as given

The engine explains Cambodia's schools from household choices, but every main economic driver is a coded path, so it cannot yet explain schooling "from what the economy is doing" or the reverse. The [World Bank's Cambodia page](https://www.worldbank.org/kh) gives the facts below; the right-hand column is from the Atlas code.

| What the economy is doing | Source fact | In the engine today |
| --- | --- | --- |
| Income growth | Real GDP growth averaged 8.2% a year in 2000-2019; lower-middle income since 2015; 2026 growth projected near 3.5% | A coded path for median household income (`y_median`), an assumption |
| Garment, footwear and travel-goods jobs | More than one million direct workers in 2025, over three-quarters women: the backbone of formal work | Formal vacancies are a coded path (`vac0`); jobs do not respond to the skills supplied, and there is no sex |
| Informality | 88.3% of employed informal in the 2019 Labour Force Survey, which I sourced earlier; the Cambodia pack's comment assumes about 77% | A fixed informal wage; the pack's formal share assumes 77%, which needs reconciling with the survey figure |
| Graduate demand | 6.6% of employed hold a university degree (same survey) | Graduate queuing is switched off in the Cambodia pack; no observations to score it |
| Returns to schooling | An older study using 1997 and 2003-04 surveys found the tertiary return fell as supply outgrew demand, with the secondary return stable ([Demand for Skills, Supply of Skills and Returns to Schooling in Cambodia](https://ideas.repec.org/p/nan/wpaper/0805.html)) | Fixed wage ratios by credential, not a market price |
| Tourism and remittances | Tourism revenue fell in 2026; remittances are falling as migrants return | Not in the engine: no migration, no remittances |
| Fiscal capacity | Education spending near 2% of GDP in the pack's own notes | The fiscal loop (formal wage bill to tax to budget) exists, but the pack switches it off and codes a budget-per-child path |
| Population | Cohort sizes drive intake | One cohort size, `N`, per year; no fertility link |

The return to education is the clearest test. The older Cambodia study says tertiary returns fell because supply outgrew demand. If the Atlas had a graduate wage that responds to the number of graduates, it should reproduce that fall from the same enrolment path. Today it cannot, because the premium is an input.

Three economy-to-school channels would carry most of the weight for Cambodia: formal-job creation (garments, construction), the informal wage that sets what a child's time is worth, and household income. Three school-to-economy channels matter back: the skill mix of new workers, the tax base from formal wages, and the cost to firms of unskilled labour. The Atlas has the second only in outline.

## The cocoon: what can be beyond dispute, and the order to build it

Two tiers of the math can be beyond dispute, and the third cannot; the Atlas should say which tier each result sits in. Behavioural assumptions, such as how a household weighs a child's wage, are disputed by nature, and no economic model, including MAMS and IFs, claims otherwise.

| Tier | What it is | Why it can be trusted | Test in the Atlas |
| --- | --- | --- | --- |
| 1. Identities | Cohort flows add up; every person is in exactly one state; every payment has a sender and receiver; budget identities hold | True by construction, so any violation is a bug | Run-time assertions; the planning kernel's conservation tests already do this for pupils and teachers |
| 2. Limiting cases | Switch off the frictions and the engine must reproduce the textbook result: Lucas with no external effect gives the planner's schooling; Harris-Todaro's expected-wage equilibrium; search-model free entry; Katz-Murphy's "more graduates, lower premium" | Theorems given their assumptions, so a mismatch means the code is wrong | A stripped-down test world per theory card |
| 3. Calibrated behaviour | Elasticities, beliefs, how households respond | Disputable; credible only with a declared evidence class and a range | The struts register and Monte Carlo bands, with each parameter's source labelled |

The order to build, each step testable on its own:

1. **A money-and-people ledger.** Every fee, informal levy, tutoring payment, salary and tax recorded with payer and receiver, and checked each year. This is the tier-1 core and the answer to "who pays for expansion".
2. **Theory cards as limiting-case tests.** One stripped test world each for Becker-Mincer, Lucas, Katz-Murphy, Harris-Todaro, search and matching, and Epple-Romano; the engine passes them or the failure is logged.
3. **A graduate wage that clears.** Replace the fixed wage ratios with a supply-and-demand price for each skill, in the Katz-Murphy form. Check: from the same enrolment path, Cambodia's tertiary return should fall as the older study found.
4. **Vacancies and the informal wage that respond.** Free entry for formal vacancies, and an informal wage tied to labour supply, so jobs are an outcome and not a coded path.
5. **A declared macro closure.** Choose and document the savings, government and external rules, then turn the fiscal loop on in a Cambodia variant, so the budget comes from the economy.
6. **Teacher stock and recruitment delay.** Already planned; it makes teacher pay, the pay gap and the gate respond to massification.
7. **Benchmarks against MAMS and IFs.** Run the same Cambodia question and compare published results; where they differ, trace which assumption does the work.
8. **Data to close the unscored indicators,** and sex, so that the reporting goals can be checked.

Steps 1 and 2 can be promised as beyond dispute, within their stated assumptions. Steps 3 to 5 are where the real disputes will be, and the point of the cocoon is to make each dispute visible and testable.

## Sources

Pages opened on 3 November 2026. Where a page gave only an abstract, the text says so.

- Goals: [Dakar Framework for Action (EFA goals)](https://healtheducationresources.unesco.org/sites/default/files/resources/Framework%20for%20Action_Dakar.pdf); [Official SDG 4 indicator list](https://apa.sdg4education2030.org/sites/apa.sdg4education2030.org/files/2021-07/SDG4_indicator_list.pdf)
- Macro and planning models: [World Bank MAMS](https://worldbank.org/en/research/brief/MAMS) and [Löfgren's MAMS slides](https://isap.iges.or.jp/2009/en/pdf/day1/26s105_Lofgren.pdf); [IFs education model](https://ifs.du.edu/ifs/help/understand/education/equations.html); [EPSSim](https://unesdoc.unesco.org/ark:/48223/pf0000214778); [Wittgenstein cohort-component projections](https://www.demographic-research.org/volumes/vol22/15/default.htm); [CGE closure rules](https://www.open.edu/openlearncreate/mod/page/view.php?id=214558)
- Theory: [Lucas 1988](https://users.ssc.wisc.edu/~cengel/Econ702/LucasDevelopment.pdf); [Goldin-Katz, extending the race between education and technology](https://www.nber.org/papers/w26705) (abstract only); [Heckman-Lochner-Taber](https://www.nber.org/papers/w6384) (abstract only); [search and matching](https://m.nber.org/conferences/2007/si2007/EFRSW/mortenson.pdf); [Harris-Todaro](https://dev-ii-seminar.readthedocs.io/en/latest/notebooks/HarrisTodaro.html); [Epple-Romano](https://ideas.repec.org/a/aea/aecrev/v88y1998i1p33-62.html) (abstract only)
- Cambodia: [World Bank country page](https://www.worldbank.org/kh); [Demand for Skills, Supply of Skills and Returns to Schooling in Cambodia](https://ideas.repec.org/p/nan/wpaper/0805.html) (abstract only); [CDRI education CGE study](https://cdri.org.kh/publication/cambodia-macroeconomic-impacts-of-public-consumption-on-education-a-computable-general-equilibrium-approach) (abstract only)

Not opened today, so treat as from memory: Becker-Mincer, child-labour and early-childhood models, the MDG 2 and 3 wording, and the Cambodia Labour Force Survey 2019 figures (6.6% degree holders, 88.3% informal), which were sourced earlier in this project. The Atlas column describes the code as read today.
