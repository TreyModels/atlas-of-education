// Population and school systems journey: the narrated family page.
// Content only. Presentation lives in the family journey components.
// Every number here is copied from a cited source or a stored Atlas result.

import type { Journey } from './angkor-journey'

export const systemsJourney: Journey = {
  kicker: 'Population & school systems · cohorts',
  title: 'What happens when a birth wave reaches school?',
  lede: 'A school system is a pipeline with memory. Children born this year become pupils years later, and the teachers they need must have been trained before the wave arrives. This page follows cohorts through schools, teachers, classrooms and budgets in East Asian forecasts, country cases and synthetic teaching worlds. It separates country projections from published inputs, transparent toy worlds, and the limited retrospective checks that actually exist.',
  repo: 'https://github.com/TreyModels/atlas-of-education',
  family: 'systems',
  why: [
    { text: 'Most arguments about schools are arguments about now: class sizes this year, teacher vacancies this term, a budget line in the current plan. But a school system is also a queue. A birth enters at the bottom and moves upward. A teacher enters through training and moves into a classroom after a delay. A classroom built for one cohort can sit empty when a smaller cohort arrives.' },
    { text: 'That is why a birth wave can look harmless in the year it happens and then appear, stage by stage, as a primary shortage, a secondary bulge, a teacher-hiring gap or an empty building. The question is not only “how many children?” but “when does this cohort reach which part of the system, and what has to be in place by then?”' },
    { claim: 'method', text: 'We follow a descriptive approach: say what is observed, what is projected from published inputs, what is synthetic, and what has actually been checked against data. A country-shaped example is not a country forecast. A transparent toy world is not evidence about any real system. An implementation check is not empirical validation.' },
  ],
  chapters: [
    {
      id: 'cohorts', kicker: 'Chapter 1 · Why cohorts matter',
      title: 'A birth is a school place years later',
      question: 'Why does a change in births matter long before it reaches a classroom?',
      evidence: [
        { claim: 'data', text: 'The East Asian dashboards index observed births — Hong Kong’s 2025 count of about 31,100 is the 100 baseline — and follow the shrinking cohort into classrooms, teacher demand and budgets. These are observed starting counts and UN age bands, not a claim that the future path is known.' },
        { claim: 'method', text: 'The school-futures README describes the timing convention: a country birth slider shifts births relative to the UN medium projection from the 2027 birth cohort. The first effect appears at preschool ages in 2030, primary in 2033, lower secondary in 2039 and upper secondary in 2042.' },
        { claim: 'sim', text: 'The toy worlds make the same logic visible without country data: in Riverton births grow 3% a year, and in Stillwater births fall 4% a year. The point is to watch the wave move through the system and to see when spare capacity appears.' },
      ],
      rule: [
        { claim: 'method', text: 'A cohort-flow model carries a group of children forward stage by stage. Enrolment at a stage depends on the cohort reaching that age, on participation, repetition, dropout and migration. Teacher demand depends on the resulting classes and staffing rules. Budgets depend on staffing and enrolment.' },
        { claim: 'method', text: 'The East Asian dashboards add an age-structured teacher pipeline: intake, training completion, hiring and retirement happen with lags. The country cases and toy worlds use the same broad logic in a simpler teaching form.' },
      ],
      result: [
        { claim: 'sim', text: 'In the toy worlds the direction of the wave is built in: 3% annual growth in Riverton, 4% annual decline in Stillwater. The teaching result is not a country forecast; it is a demonstration of how a sustained birth trend accumulates through grades.' },
      ],
      limitation: [
        { claim: 'open', text: 'The toy-world percentages are assumptions, not observations. The country cases are illustrative cohort flows, and the context does not record an empirical evaluation or holdout window for them.' },
        { claim: 'open', text: 'Even a detailed dashboard is conditional on its inputs. Observed 2025 counts and UN age bands anchor the East Asian models, but teacher hiring, layoffs, school closures and budgets need separate validation.' },
      ],
      sources: [
        { label: 'School and teacher futures README', href: 'reference/east-asia-schools/README.md' },
        { label: 'East Asia school and teacher futures dashboard', href: 'reference/east-asia-schools/index.html' },
        { label: 'Research library', href: 'research/index.html' },
      ],
      models: ['school-futures', 'riverton-system', 'stillwater-system'],
    },
    {
      id: 'mechanism', kicker: 'Chapter 2 · How a cohort-flow model works',
      title: 'A birth wave moving through the grades',
      question: 'How does a model turn a birth cohort into classrooms, teachers and budgets?',
      evidence: [
        { claim: 'method', text: 'The basic object is a grade cohort. A group of pupils in one grade this year becomes next year’s higher grade, minus those who leave, plus those who repeat, adjusted for migration. The model does not need individual children to make the arithmetic visible.' },
        { claim: 'method', text: 'The school-futures README gives a concrete timing example. A change from the 2027 birth cohort reaches preschool ages in 2030, primary in 2033, lower secondary in 2039 and upper secondary in 2042. That sequence is the worked example: one birth wave, four stage dates.' },
      ],
      rule: [
        { claim: 'method', text: 'In words: next year’s grade is this year’s lower grade, reduced by dropout and migration, plus repeaters. The model then divides pupils by class-size rules to get classes, and classes by staffing rules to get teachers. A teacher pipeline adds training and hiring lags.' },
      ],
      result: [
        { claim: 'method', text: 'The worked example is a timing result, not an empirical finding. If a birth change enters in 2027, the model shows it at preschool in 2030, primary in 2033, lower secondary in 2039 and upper secondary in 2042. A system that responds only when the pupils arrive is already late.' },
      ],
      limitation: [
        { claim: 'open', text: 'The dates are model stage conventions. Real systems have repetition, dropout, migration, late entry, private schooling and cross-border pupils. The model can represent some of these, but the context does not provide a validated country fit for every stage.' },
        { claim: 'open', text: 'A cohort-flow model is an accounting device. It can keep pupils, classes and teachers consistent. It cannot tell you whether a country will actually hire the teachers its arithmetic requires.' },
      ],
      maths: {
        plain: 'A cohort is carried forward one grade at a time. The pupils in a grade next year are the pupils from the grade below this year, after subtracting those who leave and adding those who repeat. Class counts then follow from a class-size rule, and teacher counts from a staffing rule.',
        formula: 'N_(g+1,t+1) = N_(g,t) × (1 − d_g − m_g) + R_(g+1,t+1)',
        symbols: [
          ['N_(g,t)', 'pupils in grade g in year t'],
          ['d_g', 'dropout rate from grade g'],
          ['m_g', 'net migration rate out of grade g'],
          ['R_(g+1,t+1)', 'repeaters in the next grade next year'],
        ],
        example: 'The README timing example is the worked case: a change from the 2027 birth cohort first appears at preschool ages in 2030, primary in 2033, lower secondary in 2039 and upper secondary in 2042. These are illustrative model dates, not observations of a particular country.',
      },
      sources: [
        { label: 'School and teacher futures README: birth-slider timing', href: 'reference/east-asia-schools/README.md' },
        { label: 'School and teacher futures dashboard', href: 'reference/east-asia-schools/index.html' },
      ],
      models: ['school-futures'],
    },
    {
      id: 'countries', kicker: 'Chapter 3 · Country cohort cases',
      title: 'Cambodia, China, the Philippines and Kenya',
      question: 'What does a demographic or policy shock look like when it travels through a country-shaped system?',
      evidence: [
        { claim: 'method', text: 'The catalogue describes four country cases. Cambodia asks how a post-conflict birth boom travels through classrooms, teachers and budgets. China asks what happens when the baby bust reaches the classroom and teacher training responds with a lag. The Philippines asks how a large cohort interacts with the K to 12 transition, teacher supply and classrooms. Kenya asks what follows when free primary education arrives during a teacher hiring freeze.' },
        { claim: 'open', text: 'The context gives the questions and the broad mechanism, but it does not list a stored forecast evaluation, a holdout window or an accuracy score for these four worlds. They are country-shaped teaching and mechanism examples, not validated country forecasts.' },
      ],
      rule: [
        { claim: 'method', text: 'Each case is a cohort flow with a shock attached. A birth boom adds pupils at the bottom. A baby bust removes them. A K to 12 expansion changes the number of grades and the teacher requirement. A hiring freeze holds teacher supply fixed while pupils arrive. The model follows the consequence through classrooms and budgets.' },
      ],
      result: [
        { claim: 'sim', text: 'The teaching result is qualitative and visible: a shock at one point in the system keeps moving after the year it lands. A birth boom becomes a primary wave, then a secondary wave. A hiring freeze during rising enrolment becomes a staffing gap. A contraction becomes spare capacity later.' },
        { claim: 'open', text: 'Because no evaluation window is recorded in the context, these runs cannot be read as current fits to Cambodia, China, the Philippines or Kenya. A historical run would not fix that: a run through past years is not a test against held-out outcomes unless it was actually compared with them.' },
      ],
      limitation: [
        { claim: 'open', text: 'Country cases need country data to become forecasts: annual enrolment by grade, repetition and dropout, teacher hiring and retirement, class-size rules and budget lines. The context does not provide a validation table for these four cases.' },
        { claim: 'open', text: 'The cases are useful for asking “what would follow if these cohort and policy rules held?” They are not evidence that those rules are the ones operating in any named country.' },
      ],
      sources: [
        { label: 'Country and toy systems in the catalogue', href: 'reference/education/index.html#world=cambodia' },
        { label: 'China demographic-contraction case', href: 'reference/education/index.html#world=china' },
        { label: 'Philippines K to 12 case', href: 'reference/education/index.html#world=philippines' },
        { label: 'Kenya free-primary case', href: 'reference/education/index.html#world=kenya' },
      ],
      models: ['cambodia-system', 'china-system', 'philippines-system', 'kenya-system'],
    },
    {
      id: 'east-asia', kicker: 'Chapter 4 · East Asian contraction forecasts',
      title: 'Teacher pipelines, shrinking cohorts and school networks',
      question: 'What do the East Asian dashboards actually project, and what has been checked?',
      evidence: [
        { claim: 'data', text: 'The school-futures dashboard uses actual 2025 education counts and UN age bands for Hong Kong, Japan, South Korea, Taiwan, Thailand and Guangzhou. The four national models use age-based enrolment paths that hold relative participation and coverage constant.' },
        { claim: 'method', text: 'The teacher pipeline is explicit about lags. In the Korean primary example, the latest approved training intake is 3,390 places. With a four-year lag, the lower intake reaches the qualifying pool in 2029. At an 85% qualification rate and an 80% application rate, that is about 2,306 new applicants against 2,500–2,800 planned public appointments per year in 2029 and 2030. The appointment process also draws on earlier cohorts.' },
        { claim: 'data', text: 'The city-networks dashboard reconstructs Hong Kong and Guangzhou from published school, population and policy material. Hong Kong’s observed 2025/26 operations were 958 kindergartens, 591 primaries and 513 secondaries, with 67,315 teachers across the three stages. The published-policy reference is a reproducible reconstruction, not an EDB territory-wide schedule.' },
      ],
      rule: [
        { claim: 'method', text: 'Enrolment is aged forward from observed cohorts. Teacher posts follow class rules and staffing ratios. Hiring, training and retirement are separate flows. Scenarios vary births, retention, consolidation and class size. The Hong Kong cases include published-policy reference, selective retention and faster consolidation. Guangzhou uses local education bulletins and a separate school structure.' },
      ],
      result: [
        { claim: 'sim', text: 'In the Hong Kong reference, teachers fall from 67,315 in 2025/26 to 49,476 in 2050/51, a change of −17,839. Selective retention gives 54,013, and faster consolidation gives 46,845. The default reference still requires 3,459 hires in 2031/32, including replacement hiring; headcount reductions are absorbed through departures and lower replacement hiring. The model contains no evidence of an EDB layoff plan.' },
        { claim: 'sim', text: 'The retrospective enrolment checks are modest. For primary, the age method had 0.36% error in Japan, 0.47% in Korea, 0.11% in Taiwan and 0.91% in Thailand, using one, one, four and three holdout years respectively. In Hong Kong the rolling historical enrolment model achieved 2.20% weighted error versus 3.16% for holding enrolment flat, and the workforce arithmetic achieved 1.04% versus 1.80% for a fixed pupil–teacher ratio. Historical school-count changes had 3.44 operations mean absolute error versus 6.22 for assuming no change.' },
        { claim: 'sim', text: 'For Guangzhou, rolling enrolment forecasts for 2023–2025 produced 4.08% weighted error versus 5.70% for persistence. The school-count rule performed slightly worse than persistence, 1.51% versus 1.45%. The teacher-count rule reached 3.06% versus 4.47% on the same short test.' },
      ],
      limitation: [
        { claim: 'open', text: 'These are retrospective checks against one UN release and short historical windows, not evaluations of forecasts made before the outcomes were known. The Hong Kong backtest window is not stated in the context. No test of the latest published merger rules over a completed period was possible.' },
        { claim: 'open', text: 'Country school operations are capacity scenarios and need district data to predict closures. Teacher hiring and layoffs need separate validation. The model does not carry unmatched applicants into the next year. Cost input gives modelled payroll in local currency, not a validated budget forecast.' },
        { claim: 'open', text: 'The dashboard, its README and CITY-NETWORKS.md are one workbench and its documentation, not separate models. Implementation checks and retrospective backtests are not empirical validation of a current country forecast.' },
      ],
      sources: [
        { label: 'School and teacher futures README', href: 'reference/east-asia-schools/README.md' },
        { label: 'Hong Kong and Guangzhou school networks: methods and results', href: 'reference/east-asia-schools/CITY-NETWORKS.md' },
        { label: 'City-networks dashboard', href: 'reference/east-asia-schools/city-networks.html' },
        { label: 'School-futures dashboard', href: 'reference/east-asia-schools/index.html' },
      ],
      models: ['school-futures', 'city-networks'],
    },
    {
      id: 'synthetic', kicker: 'Chapter 5 · Synthetic city and toy worlds',
      title: 'Teaching tools, not country forecasts',
      question: 'What can a synthetic city or a toy world show that a country case cannot?',
      evidence: [
        { claim: 'method', text: 'The six-district city is a synthetic city with cohort flow. The catalogue asks which staffing and school-consolidation strategy keeps provision resilient while children move through it. Its value is transparency: the districts, flows and rules are visible enough to inspect.' },
        { claim: 'method', text: 'Riverton and Stillwater are deliberately simple toy worlds. In Riverton births grow 3% a year; in Stillwater they fall 4% a year. The catalogue uses them to show the wave moving through the system and to ask when spare capacity appears.' },
      ],
      rule: [
        { claim: 'method', text: 'The synthetic city adds spatial structure to the cohort flow: children are in districts, and provision can be consolidated or staffed in different ways. The toy worlds remove most of that detail and keep one trend, so the user can see the arithmetic without a country story attached.' },
      ],
      result: [
        { claim: 'sim', text: 'The teaching result is the shape of the wave: sustained growth fills grades and then strains staffing; sustained decline leaves spare capacity later. Because Riverton and Stillwater use 3% growth and 4% decline by construction, their paths demonstrate the rule rather than estimate a real place.' },
        { claim: 'open', text: 'The context records no empirical evaluation for the six-district city, Riverton or Stillwater. They are teaching and mechanism tools. They should not be cited as evidence about a real city or country.' },
      ],
      limitation: [
        { claim: 'open', text: 'Synthetic does not mean arbitrary, but it does mean unvalidated. A toy world can make a mechanism clear and still be wrong about the magnitude, timing or direction in any real system.' },
        { claim: 'open', text: 'The six-district city is not the same object as the Hong Kong and Guangzhou city networks. The latter reconstructs published inputs; the former is a synthetic teaching city.' },
      ],
      sources: [
        { label: 'The six-district city in the catalogue', href: 'reference/education/index.html#world=city' },
        { label: 'Riverton growing-population toy world', href: 'reference/education/index.html#world=rising' },
        { label: 'Stillwater declining-population toy world', href: 'reference/education/index.html#world=falling' },
      ],
      models: ['city-system', 'riverton-system', 'stillwater-system'],
    },
    {
      id: 'limits', kicker: 'Chapter 6 · Limits and what would test them',
      title: 'What would make these models forecasts?',
      question: 'What evidence would turn a cohort-flow scenario into a tested forecast?',
      evidence: [
        { claim: 'open', text: 'The East Asian dashboards have retrospective enrolment and workforce checks against published counts and one UN release. Those checks are useful, but they are not a current forecast evaluation. The country cases and toy worlds have no recorded evaluation window in the context.' },
        { claim: 'open', text: 'A historical run is not a current fit. A model run through past years proves only that the code can produce a path; it becomes evidence only when its outputs are compared with observations that were not used to set it up.' },
      ],
      rule: [
        { claim: 'method', text: 'A proper test would hold out annual district or national counts: enrolment by grade, classes, teachers, hiring, retirement and budget lines. The model would be fitted on earlier years and scored on later ones. For school closure, the outcome would need the actual closure and merger decisions, not only capacity arithmetic.' },
        { claim: 'method', text: 'For the country cases, the same test would need the country’s own grade-level enrolment, repetition, dropout, migration and teacher records. For the toy worlds, no such test is appropriate: they are teaching tools and should stay labelled as such.' },
      ],
      result: [
        { claim: 'open', text: 'The context does not record a completed forecast evaluation for the systems family as a whole. The East Asian models come closest: they use observed 2025 counts, UN age bands and published policy benchmarks, and they report retrospective errors. Even there, teacher hiring and layoffs need separate validation, and the latest merger rules could not be tested over a completed period.' },
      ],
      limitation: [
        { claim: 'open', text: 'The main risk is category confusion. A country-shaped teaching case can look like a forecast. A synthetic city can look like a real district. A retrospective check can look like a validated forecast. The labels on this page are there to keep those apart.' },
        { claim: 'open', text: 'Until held-out outcome data are named and scored, the right reading is conditional: if these cohort, staffing and budget rules held, this is what would follow. That is a useful question. It is not a prediction.' },
      ],
      sources: [
        { label: 'School and teacher futures README: scope and checks', href: 'reference/east-asia-schools/README.md' },
        { label: 'City networks: backtests and limits', href: 'reference/east-asia-schools/CITY-NETWORKS.md' },
        { label: 'Research library', href: 'research/index.html' },
      ],
      models: ['school-futures', 'city-networks', 'city-system'],
    },
  ],
  deeper: [],
  models: {
    'school-futures': {
      id: 'school-futures',
      title: 'East Asia school and teacher futures',
      purpose: 'accounting',
      state: 'developing',
      note: 'Uses observed 2025 education counts and UN age bands; deterministic scenarios. Retrospective enrolment checks beat persistence in Japan, Korea, Taiwan and Thailand, but teacher hiring and layoffs need separate validation. Not a current country forecast.',
      engine: 'reference/east-asia-schools/index.html',
      route: 'school-futures',
      research: 'reference/east-asia-schools/README.md',
    },
    'city-networks': {
      id: 'city-networks',
      title: 'Hong Kong and Guangzhou school networks',
      purpose: 'accounting',
      state: 'developing',
      note: 'Published-policy reconstruction from EDB and Guangzhou bulletin material, with separate selective-retention and faster-consolidation variants. Retrospective backtests are reported, but the latest merger rules could not be tested over a completed period. District data are still needed for closure prediction.',
      engine: 'reference/east-asia-schools/city-networks.html',
      route: 'city-networks',
      research: 'reference/east-asia-schools/CITY-NETWORKS.md',
    },
    'city-system': {
      id: 'city-system',
      title: 'The six-district city',
      purpose: 'teaching',
      state: 'developing',
      note: 'Synthetic city and cohort flow for comparing staffing and school-consolidation strategies. Useful for inspecting the rules; the context records no empirical evaluation or holdout window.',
      engine: 'reference/education/index.html#world=city',
    },
    'cambodia-system': {
      id: 'cambodia-system',
      title: 'Cambodia · cohort echo',
      purpose: 'accounting',
      state: 'developing',
      note: 'Country-shaped cohort-flow case asking how a post-conflict birth boom travels through classrooms, teachers and budgets. No evaluation data or window is recorded in the context; treat it as a conditional teaching case, not a current forecast.',
      engine: 'reference/education/index.html#world=cambodia',
    },
    'china-system': {
      id: 'china-system',
      title: 'China · demographic contraction',
      purpose: 'accounting',
      state: 'developing',
      note: 'Country-shaped case following the baby bust into classrooms while teacher training responds with a lag. The context gives no stored evaluation, holdout window or accuracy score for this world.',
      engine: 'reference/education/index.html#world=china',
    },
    'philippines-system': {
      id: 'philippines-system',
      title: 'Philippines · K to 12 expansion',
      purpose: 'accounting',
      state: 'developing',
      note: 'Country-shaped case combining a large cohort with the K to 12 transition, teacher supply and classrooms. It is a mechanism and teaching world, not a validated forecast; no evaluation window is recorded in the context.',
      engine: 'reference/education/index.html#world=philippines',
    },
    'kenya-system': {
      id: 'kenya-system',
      title: 'Kenya · free primary education',
      purpose: 'accounting',
      state: 'developing',
      note: 'Country-shaped policy-shock case: free primary education arrives during a teacher hiring freeze. Shows how a fixed teacher pipeline strains provision; no empirical evaluation or holdout window is recorded in the context.',
      engine: 'reference/education/index.html#world=kenya',
    },
    'riverton-system': {
      id: 'riverton-system',
      title: 'Riverton · growing population',
      purpose: 'teaching',
      state: 'developing',
      note: 'Transparent toy world with births growing 3% a year by construction. Built to show a birth wave moving through the grades. Not a country forecast and not empirically evaluated in the context.',
      engine: 'reference/education/index.html#world=rising',
    },
    'stillwater-system': {
      id: 'stillwater-system',
      title: 'Stillwater · declining population',
      purpose: 'teaching',
      state: 'developing',
      note: 'Transparent toy world with births falling 4% a year by construction. Built to show when spare capacity appears as a cohort shrinks. Not a country forecast and not empirically evaluated in the context.',
      engine: 'reference/education/index.html#world=falling',
    },
  },
  bottomLine: 'A school system is a pipeline with memory: births today set class sizes years later, and teachers take time to train. The East Asian dashboards make that arithmetic transparent and report retrospective checks against published counts and one UN release; the country cases and toy worlds show the same logic but are teaching and mechanism tools, not validated forecasts. Read the numbers as conditional on their inputs, not as predictions.',
}
