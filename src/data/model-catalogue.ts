import { worlds } from '../models'
import { schoolFutures } from '../components/SchoolFutures'

export type ModelFamily = 'education' | 'systems' | 'planning' | 'angkor' | 'fertility' | 'shadow' | 'deephistory'
export type CatalogueItem = {
  id: string
  family: ModelFamily
  title: string
  question: string
  method: string
  format: 'Atlas workbench' | 'Classic workbench'
  route?: string
  href?: string
  keywords?: string
}

const atlas = 'reference/education/index.html'
const external = (id: string, family: ModelFamily, title: string, question: string, method: string, target: string, keywords = ''): CatalogueItem => ({
  id, family, title, question, method, format: 'Classic workbench', href: `${atlas}#${target}`, keywords,
})
const internal = (id: string, family: ModelFamily, method: string): CatalogueItem => {
  const model = worlds.find(item => item.id === id)!
  return { id, family, title: model.nav, question: model.question, method, format: 'Atlas workbench', route: id }
}

const education: CatalogueItem[] = [
  internal('china', 'education', 'Fitted labour-market model'),
  internal('cambodia', 'education', 'Household simulation'),
  internal('credentials', 'education', 'Credential dynamics'),
  { id: 'massification-parents', family: 'education', title: 'Massification · Parents & peers', question: 'Can the pressure to keep up raise aspirations faster than completion?', method: 'Stored experiment · household emulation', format: 'Classic workbench', href: 'research/massification/index.html#parents', keywords: 'massification family parents emulation credit' },
  { id: 'massification-actors', family: 'education', title: 'Massification · Three actors', question: 'How do households, employers and the state reinforce a credential pipeline?', method: 'Stored experiment · actor interactions', format: 'Classic workbench', href: 'research/massification/index.html#actors', keywords: 'massification household employer state' },
  { id: 'massification-access', family: 'education', title: 'Massification · Unequal access', question: 'Who gets into credential-screened jobs when access is restricted?', method: 'Stored experiment · durable inequality', format: 'Classic workbench', href: 'research/massification/index.html#access', keywords: 'massification Tilly hoarding exclusion access inequality' },
  { id: 'massification-persistence', family: 'education', title: 'Massification · Persistence', question: 'Can credential screening persist after referral networks return?', method: 'Stored experiment · institutional adaptation', format: 'Classic workbench', href: 'research/massification/index.html#persistence', keywords: 'massification imitation adaptation inertia networks' },
]

const systems: CatalogueItem[] = [
  ...Object.entries(schoolFutures).map(([route, dashboard]): CatalogueItem => ({
    id: route, family: 'systems', title: dashboard.title, question: dashboard.description,
    method: 'School-system forecasting', format: 'Atlas workbench', route,
  })),
  external('city-system', 'systems', 'The six-district city', 'Children move through a synthetic city. Which staffing and school-consolidation strategy keeps provision resilient?', 'Synthetic city · cohort flow', 'world=city', 'districts migration school places'),
  external('cambodia-system', 'systems', 'Cambodia · cohort echo', 'How does the post-conflict birth boom travel through classrooms, teachers and budgets?', 'Country case · cohort flow', 'world=cambodia', 'Cambodia demographics enrolment'),
  external('china-system', 'systems', 'China · demographic contraction', 'What happens when the baby bust reaches the classroom and teacher training responds with a lag?', 'Country case · cohort flow', 'world=china', 'China demographics enrolment'),
  external('philippines-system', 'systems', 'Philippines · K to 12 expansion', 'How does a large cohort interact with the K to 12 transition, teacher supply and classrooms?', 'Country case · cohort flow', 'world=philippines', 'Philippines K12 expansion'),
  external('kenya-system', 'systems', 'Kenya · free primary education', 'What follows when free primary education arrives during a teacher hiring freeze?', 'Country case · policy shock', 'world=kenya', 'Kenya free primary hiring freeze'),
  external('riverton-system', 'systems', 'Riverton · growing population', 'A transparent toy world: births grow three percent a year. Watch the wave move through the system.', 'Toy world · growth', 'world=rising', 'synthetic growing births'),
  external('stillwater-system', 'systems', 'Stillwater · declining population', 'A transparent toy world: births fall four percent a year. When does spare capacity appear?', 'Toy world · decline', 'world=falling', 'synthetic declining births'),
]

const planning: CatalogueItem[] = [
  internal('cohort', 'planning', 'Flows and internal efficiency'),
  external('indicators', 'planning', 'Indicator calculator', 'Calculate GER, NER, GIR, adjusted gender parity and teacher ratios from raw counts.', 'Flows and internal efficiency', 'tool=indicators', 'IIEP UIS enrollment indicators parity'),
  internal('sector', 'planning', 'Population and enrolment'),
  external('population', 'planning', 'School-age population', 'Use cohort-component projection to see who will be of school age, and when.', 'Population and enrolment', 'tool=population', 'IIEP UIS demographics projection'),
  internal('teachers', 'planning', 'Teachers'),
  external('deployment', 'planning', 'Teacher deployment', 'Test whether teacher allocations follow pupils using the education-sector-analysis R² diagnostic.', 'Teachers', 'tool=deployment', 'IIEP UIS allocation R squared'),
  external('equity', 'planning', 'Who gets public spending', 'Trace public education resources across a cohort with a Lorenz curve and benefit-incidence analysis.', 'Money and equity', 'tool=equity', 'IIEP UIS Lorenz benefit incidence'),
  external('grants', 'planning', 'School grant formula', 'Combine per-pupil, poverty and remoteness weights and inspect the resulting allocation per child.', 'Money and equity', 'tool=grants', 'IIEP UIS funding formula'),
  internal('schoolmap', 'planning', 'Access and places'),
  internal('lays', 'planning', 'Learning and targets'),
  external('logistic', 'planning', 'Is the deadline realistic?', 'Compare the S-curve speed required by a coverage target with speeds countries have achieved.', 'Learning and targets', 'tool=logistic', 'IIEP UIS logistic target feasibility'),
  internal('absorption', 'planning', 'Work and external efficiency'),
]

const guided = ['provisioning', 'campaign', 'angkor', 'signalling', 'obligations', 'monsoon']
const further = ['mandala', 'accounts', 'institutions', 'flight', 'maintenance', 'relocation', 'petri']
const angkor: CatalogueItem[] = [
  ...guided.map(id => internal(id, 'angkor', 'Guided sequence')),
  ...further.map(id => internal(id, 'angkor', 'Further experiment')),
]

const fertility: CatalogueItem[] = [
  { id: 'fertility-collapse', family: 'fertility', title: 'Fertility collapse lab', question: 'Six economies fell below their development path at once after 2015. Explore the survival floor, the marriage jam, the biological clock and the policy levers.', method: 'Findings lab · six economies', format: 'Classic workbench', href: 'research/fertility.html', keywords: 'fertility TFR marriage East Asia IVF shock 2015 fecundity' },
  { id: 'fertility-bundle', family: 'fertility', title: 'Fertility research bundle', question: 'The full codebase and findings: survival floor, credential contest, fecundity clock, shock tests and policy suites.', method: 'Code, data & findings · download', format: 'Classic workbench', href: 'research/fertility/fertility-research-full.zip', keywords: 'fertility code data findings zip download' },
]

const shadow: CatalogueItem[] = [
  { id: 'shadow-education', family: 'shadow', title: 'Shadow education lab', question: 'Why do pupils pay their own teachers? Three rival explanations tested against seven published patterns.', method: 'Agent-based model · Cambodia', format: 'Classic workbench', href: 'research/shadow-education.html', keywords: 'shadow education private tutoring Cambodia Bray diversion favour' },
  { id: 'shadow-abm', family: 'shadow', title: 'Tutoring ABM bundle', question: 'The calibrated agent-based model: 72 teachers and 1,260 pupils, fitted by ABC-SMC against published targets.', method: 'Code & data · download', format: 'Classic workbench', href: 'research/shadow/tutoring_abm.zip', keywords: 'tutoring agent based model code download' },
  { id: 'shadow-dhs', family: 'shadow', title: 'Credential-floor DHS test', question: 'Who leaves school? Three structures predict different shares of leavers from the poorest 40% of households, checked against the Cambodia DHS.', method: 'Code & data · download', format: 'Classic workbench', href: 'research/shadow/credential_floor_dhs.zip', keywords: 'credential floor DHS Cambodia poorest households download' },
]

const deephistory: CatalogueItem[] = [
  { id: 'out-of-africa', family: 'deephistory', title: 'Coast or herds? The route out of Africa', question: 'Did the first people to reach Australia follow the shoreline or the big game? 800 simulated dispersals across a drowned Ice Age landscape.', method: 'Monte Carlo · least-cost dispersal', format: 'Classic workbench', href: 'research/out-of-africa.html', keywords: 'out of Africa dispersal coast megafauna Sahul Arabia sea level Monte Carlo ice age prehistory human evolution' },
  { id: 'out-of-africa-bundle', family: 'deephistory', title: 'Out of Africa model bundle', question: 'The Python model, the 800-run Monte Carlo results, the landscape grid and the static maps.', method: 'Code & data · download', format: 'Classic workbench', href: 'research/out-of-africa/coast-or-herds-model.zip', keywords: 'out of Africa code data download python' },
]

export const catalogue: CatalogueItem[] = [...education, ...systems, ...planning, ...angkor, ...fertility, ...shadow, ...deephistory]
export const modelFamilies: ModelFamily[] = ['education', 'systems', 'planning', 'angkor', 'fertility', 'shadow', 'deephistory']
export const familyItems = (family: ModelFamily) => catalogue.filter(item => item.family === family)
export const familyCounts = Object.fromEntries(modelFamilies.map(id => [id, familyItems(id).length])) as Record<ModelFamily, number>
export const totalModels = catalogue.length

export const familyInfo: Record<ModelFamily, { title: string; short: string; question: string; description: string }> = {
  education: {
    title: 'Education, work & credentials', short: 'Education & work',
    question: 'Who stays in school, and what is the diploma worth?',
    description: 'Household choices, child labour, graduate queues and credential dynamics. Behaviour is modelled, not treated as an accounting identity.',
  },
  systems: {
    title: 'Population & school systems', short: 'School systems',
    question: 'What happens when a cohort moves through the system?',
    description: 'Country cases, synthetic cities and East Asian forecasts follow pupils, teachers, classrooms and budgets through demographic change.',
  },
  planning: {
    title: 'IIEP / UIS planning methods', short: 'IIEP / UIS methods',
    question: 'The planner’s toolkit, with its arithmetic showing.',
    description: 'Twelve independent implementations in the IIEP, UIS and education-sector-analysis tradition. These are methodological tools, not official UNESCO software.',
  },
  angkor: {
    title: 'Historical systems · Angkor', short: 'Angkor',
    question: 'How do food, labour, authority and climate interact?',
    description: 'A guided reconstruction followed by separate experiments on institutions, flight, relocation and uncertainty.',
  },
  fertility: {
    title: 'Fertility & family formation', short: 'Fertility',
    question: 'Why did fertility fall off its path, and what can still move it?',
    description: 'The six-economy fertility programme: survival floor, credential contest, marriage jam, biological clock and the unexplained post-2015 shock.',
  },
  shadow: {
    title: 'Shadow education', short: 'Shadow ed',
    question: 'Why do pupils pay their own teachers?',
    description: 'Private tutoring in Cambodia as a system: three rival explanations calibrated against published patterns, and the policies they agree on.',
  },
  deephistory: {
    title: 'Deep history · Human dispersal', short: 'Deep history',
    question: 'How did people get from Africa to Australia?',
    description: 'A paleo-landscape model of the exit from Africa 85,000–65,000 years ago: coast-huggers, big-game hunters and mixed foragers raced across shifting sea levels and Green Arabia.',
  },
}

export const familyResearch: Record<ModelFamily, { label: string; href: string }[]> = {
  education: [
    { label: 'Full Education Atlas', href: 'reference/education/index.html' },
    { label: 'Research library', href: 'research/index.html' },
  ],
  systems: [
    { label: 'Research library', href: 'research/index.html' },
  ],
  planning: [
    { label: 'Full Education Atlas', href: 'reference/education/index.html' },
  ],
  angkor: [
    { label: 'Original Angkor Atlas', href: 'reference/angkor/index.html' },
    { label: 'Angkor Mandala Lab', href: 'reference/mandala/index.html' },
    { label: 'Monte Carlo Methods Studio', href: 'reference/monte-carlo/index.html' },
    { label: 'Research library', href: 'research/index.html' },
  ],
  fertility: [
    { label: 'Fertility collapse lab', href: 'research/fertility.html' },
    { label: 'Research bundle · code, data & findings', href: 'research/fertility/fertility-research-full.zip' },
  ],
  shadow: [
    { label: 'Shadow education lab', href: 'research/shadow-education.html' },
    { label: 'Tutoring ABM bundle', href: 'research/shadow/tutoring_abm.zip' },
    { label: 'Credential-floor DHS test', href: 'research/shadow/credential_floor_dhs.zip' },
  ],
  deephistory: [
    { label: 'Coast or herds? Full write-up', href: 'research/out-of-africa.html' },
    { label: 'Model bundle · code, data & maps', href: 'research/out-of-africa/coast-or-herds-model.zip' },
  ],
}

export const classicLabs = [
  { title: 'Original Angkor Atlas', description: 'The unified offline experiment in rice, population, temples, labour and regional competition.', href: 'reference/angkor/index.html', label: 'Classic integrated lab' },
  { title: 'Angkor Mandala Lab', description: 'The original spatial implementation of pledges, population and political reach.', href: 'reference/mandala/index.html', label: 'Classic spatial lab' },
  { title: 'Monte Carlo Methods Studio', description: 'Run historical scenarios repeatedly and inspect distributions rather than a single trajectory.', href: 'reference/monte-carlo/index.html', label: 'Methods classroom' },
]
