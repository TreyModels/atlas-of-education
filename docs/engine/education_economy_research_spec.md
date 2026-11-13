# Education, economic transformation and diploma disease

Research and model specification for Education Atlas v0.4.2. Prepared 3 November 2026.

## The question to model

Under what conditions does expanding education change what an economy produces, how firms produce it, and who receives its income? When do employers absorb new skills through investment and new work? When does expansion increase competition for an existing set of positions, displace less educated workers, or send graduates into migration and further study?

Cambodia and China provide different historical settings in which to test these mechanisms. Each country also changes regime over time. China's industrial expansion and its recent graduate employment problems require different periods and sectoral shocks within the same accounting system. Cambodia's rapid growth and its difficulties raising productivity must both appear in the evidence.

This specification combines an inspection of both uploaded Atlas archives, the supplied Opus memo, official reporting frameworks, and a broad search of primary research and model documentation. It is a first research specification. Searches located many candidate models; several papers were accessible only through abstracts. An exhaustive systematic review, parameter extraction and replication of the economic studies remain to be completed. Equations below are proposed benchmark representations unless explicitly described as existing code.

## What the current code establishes

Paths below are relative to `merged/` inside the v0.4.2 archive. Both archives were extracted and their engine directories compared. The newer archive adds the China page and coverage inventory, plus changes in the labour module and tests. This inspection does not establish the validity of every archived result.

| Component | Evidence in the code | Consequence for the research claim |
|---|---|---|
| Household resources | `engine/eduengine/core.py` assigns entering cohorts lognormal household incomes around `y_median`; country files provide income paths | Labour earnings affect beliefs about schooling, but the next generation's household resources are assigned separately. Intergenerational income feedback needs an explicit link. |
| Cambodia and China public finance | Both country files set `fiscal_budget=False` | Their school budget paths are imposed. Having a fiscal module in the engine does not make the country runs fiscally endogenous. |
| Fiscal aggregate | `modules/state.py` sets `gdp=f+i`, the modelled formal and informal earnings bills | This measures an earnings aggregate. Full GDP requires value added and a national-accounts reconciliation, including capital income and the relevant taxes. |
| Formal labour demand | Country paths supply `vac0`; `QueueLabour` can apply a chosen elasticity to educated supply | Firms do not choose vacancies from expected operating surplus and investment costs. The elasticity is a hypothesis about job creation. |
| Competitive alternative | `CompetitiveLabour` computes a wage premium from demand relative to a smoothed share of educated leavers | A useful reduced-form rival exists. It is short of a full CES equilibrium using workforce stocks and production-derived labour demand. |
| Employment stock | `_Stock` retains entry earnings for a fixed work life | Workers lack a complete lifecycle of wage changes, layoffs, retraining and occupational transitions. |
| School supply | Salary budget divided by pay determines teachers; capacity and class quality follow. A second staffing rule hires to a norm and adjusts effective pay | This is a useful fiscal tradeoff. Qualified teacher supply, recruitment delays and retention need separate stocks. |
| Private supply | Fees respond to past demand/capacity; capacity adjusts gradually; oversubscribed private seats go to richer applicants | Private provision includes price adjustment and rationing. Immediate market clearing should not be claimed. |
| China queue | `china_page.py` reports degree-holder queuing per cohort size | Its outcome differs from NBS unemployment among the economically active, non-student urban population in specified age bands. |
| Attribution | The China page computes Shapley contributions of four chosen switches | Additivity is a mathematical property of that attribution. Empirical causal shares depend on identifying the mechanisms and counterfactuals. |
| China labour shock | The tutoring module can affect graduate employment; displaced tutors are represented by synthetic queue records | A future person-level ledger must reconcile worker identities, prior jobs and earnings when tutors are displaced. This is an audit requirement before population accounting claims. |
| Reporting | Sex, preschool and adult education are absent from the current cohort model; several learning outcomes are generated without assessment calibration | Full EFA, MDG 3 and SDG 4 coverage requires additional populations, institutions and measurement. |

The stored `results/TUNING_REPORT.md` reports Cambodia completion MAE after 2015 of 4.3 percentage points for the original anchored configuration and 11.7 for the original mechanism-only configuration. These figures come from the archive, not a fresh replication. The report explicitly says that later outcomes had previously been inspected and later country paths/events remained coded. It calls the exercise a retrospective temporal check. The older `engine/results/cambodia_fit.txt` is a separate historical result and must retain that status.

Fresh verification in this session: `python -m unittest test_validation test_planning` passed all nine tests. Small test worlds emitted empty-slice warnings for unsupported summary groups. These checks cover selected validation and planning behaviour; they do not validate the macroeconomic explanation.

## What changes in the Opus memo

The memo correctly identifies imposed macroeconomic paths and recommends a people-and-money ledger. Several claims need sharper conditions:

* Higher income can reduce child labour and raise schooling demand under the luxury axiom. The table's sentence saying demand falls with income reverses that channel if read as education demand. Rising child wages can separately raise the opportunity cost of school.
* The engine has learning-to-earnings and earnings-to-beliefs channels, alongside its competitive wage rival. The missing mechanism is a consistent joint determination of production, employment, wages and household budgets.
* A public queue and a competitive skill market should be retained as competing or segmented mechanisms. Substituting one wage rule throughout the economy would assume away part of diploma disease.
* SDG 4.7 concerns curriculum, institutions and social outcomes. It belongs in the reporting system even when its implementation uses public decisions rather than a price-clearing market.
* Familiar textbook results need their exact assumptions attached. A general dynamic queue need not satisfy the static Harris–Todaro migration condition. Equality of private and planner choices also requires all other relevant wedges to be removed.
* Indicator definitions need a versioned dictionary. Thematic indicators in a 2021 list and the current global indicator framework have different scope; labels alone cannot establish comparability.

## The economic literature that answers the central question

The following are research roles, not a claim that one model dominates every economy. Linked pages were retrieved in this session. Where full text was unavailable, findings remain at abstract/documentation level.

| Research family and anchor | Mechanism and maintained conditions | Observable that separates it from alternatives | Atlas role |
|---|---|---|---|
| Human-capital investment; Mincer, *Schooling, Experience, and Earnings* (1974), [NBER book](https://www.nber.org/books-and-chapters/schooling-experience-and-earnings) | People acquire productive capabilities; schooling has direct and opportunity costs | Measured skills, output and earnings changes following exogenous schooling variation | Benchmark household valuation and lifecycle wage profiles; a Mincer coefficient alone does not identify productivity |
| Dynamic schooling choice; Todd and Wolpin (2006), [AER](https://www.aeaweb.org/articles/pdf/doi/10.1257/aer.96.5.1384) | Families choose schooling under resource constraints and expectations about future opportunities | Policy responses predicted using pre-intervention data and tested against an experiment | Main template for validating household policy counterfactuals |
| Skill formation; Cunha and Heckman (2007), [research paper](https://docs.iza.org/dp2550.pdf) | Existing capability and investment at different ages interact | Age-specific learning gains and persistence of early disadvantages | Preschool, foundations and adult retraining; estimate transfer rather than equating years and skills |
| Child labour; Basu and Van (1998), [authors' publication record](https://basu.economics.cornell.edu/publications.html) | Subsistence-related child labour and substitution between adult and child labour can create multiple equilibria | School attendance and adult/child wages after income or employment changes | Joint school, work and household time decisions |
| Credit and inequality; Galor and Zeira (1993), [REStud](https://academic.oup.com/restud/article-abstract/60/1/35/1576085) | Credit frictions and indivisible human-capital investment make wealth distribution affect aggregate outcomes | Qualified poor students excluded despite high expected returns | Financing constraints and intergenerational persistence |
| Skill supply and demand; Katz and Murphy (1992), [NBER](https://www.nber.org/papers/w3927) | Relative wages respond to relative skill supplies and demand shifts, conditional on substitution technology | Relative wages and employment measured in comparable skill units | Competitive benchmark with a complete workforce stock |
| Skills and tasks; Acemoglu and Autor (2011 chapter), [NBER working paper](https://www.nber.org/papers/w16082) | Workers and machines are assigned to tasks; technology can replace or complement particular tasks | Occupational changes within sectors, changing task content and wage polarization | Field-specific retraining, automation and occupational demand |
| Directed technology; Acemoglu (1998), [QJE](https://doi.org/10.1162/003355398555838) | Market size and profitability affect the technologies firms develop or adopt | Skill supply followed by investment and changes in production technology | A candidate explanation for skill-demand feedback, with adoption costs and delays |
| Complementary capabilities; Kremer (1993), [O-ring paper](https://academic.oup.com/qje/article-abstract/108/3/551/1881767) | Production tasks require complementary capabilities; failure at one task reduces the value of the others | Skilled workers cluster in capable firms; returns vary with team and firm capability | Why isolated graduates may have limited productive opportunities |
| Coordination; Murphy, Shleifer and Vishny (1989), [NBER](https://www.nber.org/papers/w2708) | Fixed costs and demand spillovers can sustain multiple industrialization equilibria | Joint investment succeeds where isolated investments fail | Conditional takeoff experiments; determine whether export access relaxes domestic-market limits |
| Growth diagnostics; Hausmann, Rodrik and Velasco (2005), [authors' institution](https://growthlab.hks.harvard.edu/publication/growth-diagnostics/) | Diagnose the binding constraint through its shadow price and responses to relaxation | High scarcity rents, costly circumvention and strong responses when a constraint eases | Choose among skill, finance, infrastructure and appropriability explanations for Cambodia |
| Structural transformation; Herrendorf, Rogerson and Valentinyi, [NBER](https://www.nber.org/papers/w18996) | Sectoral productivity, income elasticities and relative prices move labour across sectors | Sectoral employment and value added, expenditure shares and relative prices | Backbone connecting education to what the economy produces |
| Chinese firm reallocation; Song, Storesletten and Zilibotti (2011), [authors' institutional page](https://research-center.econ.cuhk.edu.hk/en-gb/research/research-papers/281-growing-like-china) | Heterogeneous firms and financing conditions generate reallocation and growth | Ownership-specific productivity, investment, capital returns and employment shares | China takeoff comparator; historical fit remains distinct from recent graduate unemployment |
| Misallocation; Hsieh and Klenow (2009), [NBER](https://www.nber.org/papers/w13290) | Distortions keep factors from their most productive uses under a specified production framework | Dispersion of revenue products and allocation across firms | Separate capability scarcity from restrictions on productive firms |
| Education and sectoral growth; Coelli, Zi, Ouyang and Yuan (2026), [CEPR DP21895](https://cepr.org/publications/dp21895) | Higher-education expansion can shift labour into sectors with different productivity growth | In the paper's abstract, more exposed Chinese prefectures shifted toward services without faster growth | Very close contemporary research lead; full model, identification and replication still need review |
| Screening and employer learning; Aryal, Bhuller and Lange (2022), [AER](https://swlb2.aeaweb.org/articles?id=10.1257%2Faer.20200146) | Credentials convey information while productive effects and employer learning coexist | Returns differ with employer information and experience | Separate credential value, task capability and employer knowledge; country estimates do not transfer automatically |
| Job competition and diploma disease; Dore, Thurow and Fields in Atlas bibliography | Employers ration desirable positions using credentials; households respond to exclusion risk | Credential requirements rise within stable tasks, with displacement of less credentialed workers | Retain as a rival mechanism; formalize screening costs and test changing task requirements |
| Expected-income migration; Harris–Todaro, [original MIT working-paper record](https://dspace.mit.edu/entities/publication/7c461c5e-0027-449c-8bbd-bd9e41dfc2d9) | Migration responds to expected urban earnings when access to jobs is uncertain | Migration alongside urban unemployment, rural wages and job-finding probabilities | Rural–urban and international opportunities, separately specified |
| Search and matching; Mortensen and Pissarides (1994), [REStud](https://academic.oup.com/restud/article-abstract/61/3/397/1589192?login=false) | Matching frictions and vacancy costs connect unemployment to firms' expected surplus | Vacancy–unemployment patterns, duration and job-finding rates | Endogenous vacancy creation and transitions out of unemployment |
| State capacity; Besley and Persson, [NBER](https://www.nber.org/papers/w13028) | Past investment in fiscal/legal capacity limits current policy | Tax collection and enforcement conditional on the tax base | Fiscal feedback with capacity costs and financing constraints |
| Teacher incentives; Jayachandran (2014), [author's institutional record](https://collaborate.princeton.edu/en/publications/incentives-to-teach-badly-after-school-tutoring-in-developing-cou/) | Teachers who sell tutoring may change classroom instruction | Learning and tutoring after restrictions on own-pupil tutoring | Keep incentives separate from a mechanical salary-gap rule |
| Teacher salary evidence; de Ree et al. (2018), [QJE](https://doi.org/10.1093/qje/qjx040) | Indonesia's salary experiment tests an effort response among existing teachers | Higher pay improved teacher welfare; learning did not improve over the measured period | Allow a weak short-run effort response while separately testing recruitment and retention |

Dore, Thurow and Fields are central inherited literature leads in the Atlas and uploaded manuscript; this session has not verified their complete original texts. The other rows also need equation-level extraction before implementation is described as a replication.

### Cambodia evidence with direct model implications

[Barrera-Osorio, de Barros and Filmer's scholarship experiment](https://onlinelibrary.wiley.com/doi/full/10.1002/pam.22533), published in a 2024 journal issue, reports higher long-run attainment, cognitive gains concentrated in merit-targeted recipients, and no systematic labour-outcome improvement in the studied follow-up. Attrition and the authors' treatment of it belong in the evidence card. These results give distinct tests of progression, learning and labour-market transmission. They do not establish that future schooling gains have zero economic value.

The [World Bank's Cambodia SCD update](https://www.worldbank.org/en/country/cambodia/publication/cambodia-systematic-country-diagnostic-update) describes strong growth with limited productivity contributions, and identifies infrastructure, the business environment and skills among the priorities. This supports testing several complementary constraints. It does not identify their separate causal contributions.

[CDRI Working Paper 111](https://cdri.org.kh/publication/cambodia-macroeconomic-impacts-of-public-consumption-on-education-a-computable-general-equilibrium-approach), by Ear Sothy, Sim Sokcheng and Khiev Pirom, is an existing country-specific education CGE comparator. The publisher describes using a social accounting matrix, budget data, CSES and the economic census. Its publisher PDF link retrieved here contains a one-page description rather than the full study. Full labour and fiscal closures therefore remain an extraction task.

Sakellariou's 2008 study, highlighted in the Opus memo, uses 1997 and 2003–04 surveys. The publisher's original PDF was inaccessible in this session. Its indexed abstract reports changing tertiary returns and sector/sex selection effects. Keep it as a historical lead; current skill scarcity requires newer survey estimates and occupation-specific analysis.

### China evidence and the graduate bulge

The [IMF's 2023 consultation, published in 2024](https://www.elibrary.imf.org/abstract/journals/002/2024/038/article-A001-en.xml), discusses graduate supply, weak demand in graduate-absorbing services, regulatory changes and graduation-season effects together. It provides competing mechanisms to test. Its descriptive attribution is not a structural decomposition.

The [2025 consultation, published in 2026](https://www.elibrary.imf.org/view/journals/002/2026/044/article-A001-en.xml), reports a 16.5% youth unemployment rate in December 2025 and discusses weak demand, labour mobility and skill mismatch. This is a dated observation, not a claim about today's rate. Official youth unemployment is broader than graduate unemployment. China's revised series excludes students and needs a separate observation equation from the earlier series.

For diploma disease, observe degree requirements within occupations and firms over time, job tasks, wages and output. The joint presence of more graduates and more unemployment alone leaves several explanations open. Growing task complexity can also raise degree requirements; demand weakness can generate queues without credential inflation.

## The proposed mathematical core

Start with a small open economy divided into agriculture, export manufacturing, construction, consumer services and producer services. Public education is a separately accounted activity. Add industry detail where the research question and data distinguish its consequences. Cambodia and China need different sectoral weights, institutional constraints and external exposure; the identities and measurement contracts should be shared.

### 1. Goods demand and supply

For domestic households, begin with a transparent non-homothetic demand system. A Stone–Geary benchmark is:

\[
c_{ih}=\bar c_i+\frac{\beta_{ih}}{p_i}\left(x_h-\sum_jp_j\bar c_j\right),\qquad \sum_i\beta_{ih}=1.
\]

This applies when expenditure covers the specified subsistence bundle. Poorer households below that threshold require an explicit alternative allocation rule. Estimate expenditure and price responses from household data; compare with a richer demand system when supported. As income grows, expenditure shares change and alter sectoral labour demand.

Exports require foreign demand with finite elasticity, or an explicitly stated price-taking limit. Imports require a declared domestic–import substitution rule. Public services have budgeted demand and capacity constraints. Construction depends on investment and financing; treating it as ordinary household consumption would lose a major Chinese cyclical channel.

Firms choose inputs to maximize expected profit:

\[
\pi_j=p_jF_j(K_j,H_j,L_j,M_j;A_j)-r_jK_j-w_{Hj}H_j-w_{Lj}L_j-p_M M_j-\text{fixed and adjustment costs}.
\]

Here `H` measures effective task capability, which must be linked to learning and experience. Degree possession is recorded separately. Capital accumulation follows:

\[
K_{j,t+1}=(1-\delta_j)K_{jt}+I_{jt}.
\]

Investment follows an estimated or bounded profitability rule with financing constraints. Technology adoption needs a cost and an expected payoff. This creates an explicit route from additional skills to firms' demand for skills, subject to market access and complementary inputs.

### 2. Competitive benchmark and its deductions

A two-skill CES value-added benchmark is:

\[
Y=A K^\alpha[\omega H^\rho+(1-\omega)L^\rho]^{(1-\alpha)/\rho},\qquad \rho=(\sigma-1)/\sigma.
\]

With competitive marginal-product wages and common output prices:

\[
\frac{w_H}{w_L}=\frac{\omega}{1-\omega}\left(\frac HL\right)^{-1/\sigma}.
\]

The premium falls with relative skill supply holding technology and other stated conditions fixed. Endogenous technology, investment, task reassignment and trade can change the total response. Calibrate `H/L` from the employed workforce and relevant unemployment stocks, with efficiency units declared. The current educated-leaver share is a different object.

### 3. Vacancies, queues and hiring standards

For sector and occupation `j`, a matching benchmark is:

\[
m_j=\mu_j U_j^{\eta_j}V_j^{1-\eta_j},\qquad \theta_j=V_j/U_j.
\]

The job-filling rate is `q_j=m_j/V_j`, and job-finding is `f_j=m_j/U_j`. With free vacancy entry and the chosen timing convention, expected posting cost equals expected discounted vacancy surplus. A simple stationary statement is:

\[
\kappa_j=q_j(\theta_j)J_j.
\]

Specify wage bargaining, separation risk and financing before solving this condition. Vacancy subsidies, retraining and demand stimulus enter different parts of the model and should produce distinct predictions.

Within jobs where employers use credentials to screen, choose a credential threshold by expected profit net of screening cost, subject to applicant availability. Hold task requirements explicit. Dore's mechanism then has a test: requirements can rise when applicants become more credentialed even with unchanged tasks. Compare that response with employers learning more about actual capability.

Workers choose among accepting available work, searching, studying and migrating using expected lifetime value and household support. Support must be financed by another household member or assets. Reservation wages, search costs and perceptions are estimated or bounded. Graduate status cannot mechanically put everyone into a queue.

### 4. Education, work and retraining

Represent a worker by age, sex, location, household membership, education, a vector of skills and employment history. Learning evolves through a bounded transition:

\[
\mathbf h_{t+1}=(1-\boldsymbol\delta_h)\odot\mathbf h_t+\mathbf G(\mathbf h_t,\text{instruction},\text{effort},\text{practice},\text{health}).
\]

Estimate which skills transfer to each occupation. Adult retraining changes a subset of that vector and consumes time, training resources and forgone earnings. Include employer training, worker mobility and the possibility that trained workers move abroad. Programme placement is measured over a specified follow-up; fiscal returns depend on durable additional employment and wages.

### 5. Accounting and feedback

Every person occupies one defined state at each observation time. States include employment, unemployment with active search, education and inactivity; combinations such as student employment require an explicit underlying activity representation and a survey classification rule.

\[
N_{a+1,s,e,t+1}=\sum_{e'}N_{a,s,e',t}P_{e'e,t}(1-d_{a,s,e',t})+\text{net migration}_{a+1,s,e,t}.
\]

Births come from fertility schedules conditional on the chosen demographic state. Education-related fertility differences can be incorporated using [IIASA's multistate approach](https://iiasa.ac.at/models-tools-data/sub-national-population-and-human-capital-projections); causal effects of education require separate evidence.

Government must satisfy:

\[
T+\text{grants}+\text{new borrowing}=G_{edu}+G_{other}+\text{transfers}+\text{interest}+\text{debt repayment}+\Delta\text{cash}.
\]

Households receive wages, capital income, transfers and remittances, and pay taxes and consumption costs. School and tutoring payments have institutional recipients. National accounts reconcile expenditure and value added at stated prices; external accounts reconcile trade, remittances, investment flows and external borrowing. A fiscal floor needs a financing source.

Choose whether a policy is financed by taxes, borrowing, grants or reductions elsewhere. Describe the exchange-rate/external financing rule and savings–investment rule. Report alternate plausible closures when they change the policy result. An employment model with queues needs an unemployment closure compatible with its hiring process.

## Weather, shocks and inference

Weather enters agricultural yields, health, access to school, infrastructure damage and electricity costs through specified channels. Rainfall variation can help identify effects when exclusion assumptions hold. Rainfall can also affect several outcomes directly, which complicates instrumental-variable claims.

External demand changes export orders; tourism depends partly on foreign incomes and travel conditions. Energy prices alter real household resources and firms' input costs. Financial shocks affect construction and investment. Public policy alters returns, costs and access. These processes require dated series, with information availability distinguished from retrospective historical knowledge.

Deduction supplies conditional implications of the model. Estimation uses evidence to learn parameters; causal inference addresses a specified treatment and identification problem. Calibration chooses values to match named moments. None makes a broad behavioural assumption a mathematical identity. Forecast errors must include measurement, parameter and structural uncertainty alongside simulation noise.

## Goal-by-goal economic contracts

Goal labels below summarize the [EFA framework](https://www.unesco.at/en/education/education-2030/agenda-2030/education-for-all), [MDG 2](https://www.un.org/millenniumgoals/education.shtml), [MDG 3](https://www.un.org/millenniumgoals/gender.shtml) and [current SDG 4 framework](https://sdgs.un.org/goals/goal4). The proposed economics and Atlas status are this audit's judgments. A reporting target defines an outcome; economic demand concerns decisions and willingness or ability to pay for services.

| Reporting target | Who demands and supplies the relevant service | Allocation mechanism and principal conditions | Existing Atlas coverage |
|---|---|---|---|
| EFA 1: early childhood | Households seek care and development; public, community and private providers supply staff and places | Fees, proximity and admission; parental employment, care time and early skill formation interact | Absent |
| EFA 2: universal primary | Children/households seek schooling; state and private schools supply places and teaching | Effective cost, attendance choice and rationing; transport, work opportunities and liquidity matter | Core mechanisms; imposed completion anchors in replay |
| EFA 3: youth/adult learning | Workers and employers seek capabilities; providers supply education and training | Fees, employer contracts and programme places; portability and expected job demand matter | Some youth tracks; adult learning absent |
| EFA 4: adult literacy | Adults seek functional capability; public, NGO and private programmes supply instruction | Programme access and time costs; learning must persist and be used | Absent for the adult stock |
| EFA 5: gender equality | Household members and public institutions decide access; schools supply safe, accessible education | Bargaining, expected returns, care obligations and institutional exclusion | Wealth/location measures; sex absent |
| EFA 6: quality | Learners seek learning; teachers and institutions supply instruction | Public budgets, effort contracts, tutoring and school choice; measured learning needs a calibrated scale | Learning generated; empirical calibration incomplete |
| MDG 2: primary completion | Same primary service chain | Intake, progression and completion; measure age windows and denominators consistently | Partial mechanisms and historical observations |
| MDG 3: gender parity | Sex-specific household choices and institutional access | Parity across education levels; employment and political components require their own outcomes | Sex absent |
| SDG 4.1: school completion/learning | Households and public planners; schools and teachers | Capacity plus learning, with dropout, repetition and unequal resources | Partial; assessment outcomes unscored |
| SDG 4.2: early development | Parents and care institutions | Care/work decisions, developmental inputs and local access | Absent |
| SDG 4.3: further education/training | Youth/adults and employers; TVET and tertiary institutions | Fees, financing, admissions and relevant training capacity | Tertiary/track choice; adult participation incomplete |
| SDG 4.4: relevant capabilities | Workers and firms; education and workplace training | Task demand, technology and skill transfer | One broad learning scale cannot represent ICT/task skill types |
| SDG 4.5: equitable access | Diverse households and learners; institutions | Group-specific resources, discrimination and accessibility | Wealth/location partial; other groups absent |
| SDG 4.6: literacy/numeracy | Youth and adults; schools and adult programmes | Entry, instruction, practice and depreciation | Youth proxies; adult stock absent |
| SDG 4.7: citizenship/sustainability | Learners, communities and public authorities; curriculum and teacher institutions | Policy implementation and curriculum decisions; outcomes can have public benefits | Absent |
| SDG 4.a: safe facilities | Communities and education authorities; construction and service providers | Capital budgets, procurement, maintenance and geography | Capacity proxy; facilities/services absent |
| SDG 4.b: scholarships | Eligible international students and funders | Donor budgets, admissions, migration and return decisions | Domestic transfers differ from scholarship ODA |
| SDG 4.c: qualified teachers | Schools/public authorities; training institutions and potential teachers | Training places, wages, hiring constraints and location preferences | Teacher count and pay; qualification stock absent |

Current global indicator 4.b.1 measures scholarship ODA flows; the target's stated deadline is 2020. A domestic scholarship does not automatically measure that indicator. Current global 4.c.1 concerns minimum qualifications, which pupil–teacher ratios alone cannot measure. Preserve historical and thematic indicator vintages in the reporting dictionary.

## Which integrated model to use

| Candidate | Best use here | Required qualification |
|---|---|---|
| [MAMS](https://www.worldbank.org/en/research/brief/MAMS) | Closest reference architecture for government finance, education transitions, workforce composition and economy-wide outcomes | Reproduce a specified version with explicit social accounting data and closures; performance in another country is not Cambodia validation |
| [MANAGE-WB](https://www.worldbank.org/en/programs/economicpolicy-macro-modeling/overview) | Modern recursive CGE comparator for sectoral shocks, trade and investment | Detailed schooling and credential queues require additions |
| [International Futures education](https://pardeewiki.du.edu/index.php?title=Education) | Long-run cross-country comparison linking demographic and economic conditions | Retrieved documentation describes important omissions, including private education spending and explicit cognitive quality; inspect version-specific scope |
| [UNESCO EPSSim and its successor](https://www.unesco.org/en/articles/unesco-launches-new-simulation-model-education) | Independently verify pupil flows, staffing, classroom needs and financing | Resource requirements alone do not explain household or employer behaviour |
| [IIASA/Wittgenstein multistate demography](https://iiasa.ac.at/models-tools-data/sub-national-population-and-human-capital-projections) | Consistent age/sex/education populations and demographic scenarios | Education-specific schedules need separate causal interpretation |
| [IMF DIG/DIGNAR](https://www.imf.org/en/capacity-development/training/icdtc/schedule/ol/2025/digxol25-145) | Compare debt-financed public investment and fiscal risks | Resource-sector features of DIGNAR are not an automatic Cambodia baseline; education needs its own production and timing |
| Heterogeneous-household lifecycle/OLG model | Distribution, household finance, retraining and intergenerational feedback | Large data and identification burden; simplify only after defining the question |
| Task/search model coupled to Atlas | Chinese graduate employment, mismatch, credentials and retraining | Requires unemployment, inactivity, vacancies and wage observations; school outcomes alone cannot identify it |

Recommendation: keep Atlas as the detailed education and household-choice component. Build a modest multisector production and hiring model under shared accounting, with competitive and queue/search variants. Use MAMS for architectural comparison and planning models for independent resource arithmetic. Add complexity when independent evidence distinguishes its implications.

## Country experiments and evidence gates

### Cambodia: can skills unlock upgrading?

First compare four interventions of equal stated public cost: foundational learning, targeted technical/retraining programmes, tertiary expansion, and a complementary package that changes firm investment constraints. The package must specify what is financed, such as power reliability or a credit intervention, and allow its independent effect to be measured.

Estimate wage and job-finding patterns by occupation, sector, education, sex, location and experience. Combine [CSES](https://nis.gov.kh/en/cambodia-socio-economic-survey/) with the [2019 Labour Force Survey](https://www.ilo.org/publications/report-cambodia-labour-force-survey-2019), education administration, learning assessments, fiscal accounts and enterprise data. Survey access and comparable variables still need checking. The 2019 LFS reports approximately 88% informal employment; that is employment status, not an unqualified measure of informal firms or the untaxed economy.

Discriminating predictions:

* A binding skill constraint produces costly hard-to-fill vacancies for specific capabilities and strong firm responses when those capabilities become available.
* Weak output demand limits job creation even after training. Workers may gain through mobility or occupational substitution without large aggregate employment gains.
* Missing complementary inputs concentrate returns in capable firms and locations; combined investment can have a larger payoff than isolated training.
* Credential screening raises qualification thresholds within comparable work, with displacement visible farther down the education distribution.

National graduate supply and particular skill shortages can coexist. Test the matching of capabilities, industries and locations before assigning one national diagnosis.

### China: reproduce the youth bulge

Use monthly labour transitions or an explicit seasonal observation model; an annual school engine alone cannot reproduce the graduation-season pattern. Track cohorts produced by the expansion of higher education with the actual completion lag. Distinguish higher education type and field, as data allow.

Outcomes: unemployment for each official age band; graduate job-finding duration; participation/inactivity; further study; underemployment; wages; occupations and sectoral absorption. Construct the official observation equation from the survey definition, including student status and the statistical break. Retain a separate graduate queue measure for mechanism diagnosis.

Compare a common observed education expansion under alternative mechanisms: demand weakness by sector, task mismatch, screening competition, mobility restrictions, and household-supported waiting. Shocks to property, services and tutoring require dated sector exposure. Economic takeoff and current employment stress should use a common stock history without presuming one parameter regime throughout.

Shapley decomposition may summarize a validated model's counterfactuals. Every contribution must be labelled conditional on its baseline, selected mechanisms and intervention definitions. Report unexplained error alongside the decomposition.

### Retraining: capacity, access and displacement

For a defined displaced group, report programme uptake, completion, skill gains, time to employment and earnings after costs. Compare employer-linked training with classroom-only training under the same demand path. Include the jobs lost by workers displaced from the destination occupation and the possibility of programme gains without net job creation. Evaluate time horizons long enough to separate temporary placement from durable returns.

## The mathematical assurance system

| Layer | Required record/check | Claim it supports |
|---|---|---|
| Units and ownership | Every variable has units, price basis, frequency and one state owner | Components exchange compatible quantities |
| Population conservation | Reconcile births, deaths, migration, school transitions and labour states, including displaced tutors | Recorded people are conserved |
| Double-entry money | Each payment has payer/recipient; reconcile household, provider, government and external balances | Policy costs and incomes are jointly feasible |
| Mathematical specification | Domain restrictions, existence conditions, uniqueness where available, and alternate equilibria when relevant | The stated mathematical problem is well defined |
| Numerical solution | Residuals, tolerance, convergence and sensitivity to update order | The program solves the specified problem accurately |
| Limiting cases | CES premium, vacancy free entry, zero-policy effects and frictionless cases under their exact assumptions | Code agrees with conditional deductions |
| Empirical identification | Data sources, estimands, exclusion restrictions and sensitivity | Parameter interpretation is warranted to the stated extent |
| Historical evaluation | Separate imposed paths, calibrated moments and genuinely withheld outcomes | Fit is classified correctly |
| Structural uncertainty | Compare competing production, hiring, learning and fiscal rules | Policy conclusions are tested across credible alternatives |
| Reproduction | Frozen code/data hashes, environment, seeds and an executable run manifest | Another researcher can regenerate the stated result |

Do not describe finite hand-chosen parameter ranges as confidence intervals. Monte Carlo seed bands describe simulation variation; posterior or sampling uncertainty requires a separate estimation procedure. New independent observations are needed for a fresh forecast test once historical outcomes have already shaped model design.

## Build sequence with acceptance criteria

1. **Audit the current national-accounts and people ledgers.** Reconcile tutoring payments, displaced tutor identities, household support and the earnings aggregate. Acceptance: balances and population stocks reconcile in each year and policy arm, with residuals visible.
2. **Create versioned observation contracts.** Define China unemployment and Cambodia education/labour outcomes before fitting. Acceptance: known survey examples can be reconstructed from microdata or documented aggregates.
3. **Implement competing labour benchmarks.** Keep the existing queue, add a full workforce CES benchmark, then a search variant with profit-sensitive vacancies. Acceptance: each reproduces its limiting cases and reports the same defined labour outcomes.
4. **Introduce sectoral production, investment and household budgets.** Connect skills to firms and earned income to household resources. Acceptance: the baseline reconciles sectoral output, wage bills, employment, investment and external accounts.
5. **Close public finance in an explicit variant.** Finance teacher recruitment, transfers and policy costs under stated taxes/debt/grants. Acceptance: all fiscal constraints hold without an unfinanced budget floor.
6. **Estimate and compare mechanisms.** Use completion and learning alongside labour-market and enterprise observations. Acceptance: rejection criteria set before the next evaluation, with weak identification reported.
7. **Run the Cambodia upgrading and China graduate-bulge experiments.** Acceptance: results include distribution, displacement, timing, costs, model discrepancies and structural sensitivity.
8. **Expand reporting coverage.** Add sex, preschool, adult learning and qualified teacher stocks, then facilities and curriculum implementation as supported. Acceptance: every claimed indicator maps to the relevant population and metadata vintage.

## Search coverage and remaining work

Searches in this session covered official EFA/MDG/SDG frameworks; MAMS, IFs, EPSSim, MANAGE and DIG/DIGNAR; skill formation and schooling choice; labour demand and task assignment; child labour and credit constraints; migration and search; firm reallocation, coordination and technical change; fiscal capacity; Cambodia surveys and experiments; and Chinese youth employment and higher-education expansion. Both available search systems were used, with targeted primary-source searches and direct page retrieval.

The next literature pass should extract equations and parameter provenance from full texts, follow backward and forward citations, check replication packages, and record exclusions. Several relevant areas need a dedicated pass: trade/FDI and firm technology transfer, spatial equilibrium and housing/hukou constraints, informal enterprise entry, household bargaining and care work, macro stabilization in a dollarized economy, and rigorous adult-training impact evidence. Source completeness cannot yet be claimed.

For each candidate, record the version, geography, period, population, outcome, equations, identification design, closure, parameter sources, code/data availability and known failure cases. Rank candidates by fit to a specified question, attainable evidence and performance against rival mechanisms. Mathematical consistency is a necessary acceptance gate; the explanation of a real economy remains open to empirical rejection.
