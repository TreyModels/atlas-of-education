import { worlds } from '../models'
import { schoolFutures } from '../components/SchoolFutures'
import { tagGroup, tagsFor } from './model-tags'

export type ModelFamily = 'education' | 'systems' | 'planning' | 'angkor' | 'fertility' | 'shadow' | 'deephistory' | 'politics' | 'extension'
export type CatalogueItem = {
  id: string
  family: ModelFamily
  title: string
  question: string
  method: string
  format: 'Atlas workbench' | 'Classic workbench' | 'Write-up' | 'Code & data download' | 'Narrated journey' | 'Experimental interface'
  route?: string
  href?: string
  /** Optional file download offered as a separate secondary action; never the primary click. */
  downloadHref?: string
  keywords?: string
  /** Curated hashtags, e.g. ['angkor','workbench','water']. Family and kind tags are automatic. */
  tags: string[]
}

/** Entries as authored: tags are derived once, centrally, in `catalogue` below. */
type CatalogueItemInput = Omit<CatalogueItem, 'tags'>

const atlas = 'reference/education/index.html'
const external = (id: string, family: ModelFamily, title: string, question: string, method: string, target: string, keywords = ''): CatalogueItemInput => ({
  id, family, title, question, method, format: 'Classic workbench', href: `${atlas}#${target}`, keywords,
})
const internal = (id: string, family: ModelFamily, method: string): CatalogueItemInput => {
  const model = worlds.find(item => item.id === id)!
  return { id, family, title: model.nav, question: model.question, method, format: 'Atlas workbench', route: id }
}

const education: CatalogueItemInput[] = [
  internal('china', 'education', 'Fitted labour-market model'),
  internal('cambodia', 'education', 'Household simulation'),
  internal('credentials', 'education', 'Credential dynamics'),
  { id: 'massification-parents', family: 'education', title: 'Massification · Parents & peers', question: 'Can the pressure to keep up raise aspirations faster than completion?', method: 'Stored experiment · household emulation', format: 'Classic workbench', href: 'research/massification/index.html#parents', keywords: 'massification family parents emulation credit' },
  { id: 'massification-actors', family: 'education', title: 'Massification · Three actors', question: 'How do households, employers and the state reinforce a credential pipeline?', method: 'Stored experiment · actor interactions', format: 'Classic workbench', href: 'research/massification/index.html#actors', keywords: 'massification household employer state' },
  { id: 'massification-access', family: 'education', title: 'Massification · Unequal access', question: 'Who gets into credential-screened jobs when access is restricted?', method: 'Stored experiment · durable inequality', format: 'Classic workbench', href: 'research/massification/index.html#access', keywords: 'massification Tilly hoarding exclusion access inequality' },
  { id: 'massification-persistence', family: 'education', title: 'Massification · Persistence', question: 'Can credential screening persist after referral networks return?', method: 'Stored experiment · institutional adaptation', format: 'Classic workbench', href: 'research/massification/index.html#persistence', keywords: 'massification imitation adaptation inertia networks' },
]

const systems: CatalogueItemInput[] = [
  ...Object.entries(schoolFutures).map(([route, dashboard]): CatalogueItemInput => ({
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

const planning: CatalogueItemInput[] = [
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
const angkor: CatalogueItemInput[] = [
  ...guided.map(id => internal(id, 'angkor', 'Guided sequence')),
  ...further.map(id => internal(id, 'angkor', 'Further experiment')),
]

const fertility: CatalogueItemInput[] = [
  { id: 'fertility-collapse', family: 'fertility', title: 'Fertility collapse lab', question: 'Explore development, family formation and birth timing across six economies. Compare the assumptions behind the fertility scenarios.', method: 'Exploratory lab · six economies', format: 'Write-up', href: 'research/fertility.html', keywords: 'fertility TFR marriage East Asia IVF shock 2015 fecundity' },
  { id: 'development-survival', family: 'fertility', title: 'Development (survival) model', question: 'Does life expectancy predict fertility levels, and does that link survive differencing?', method: 'Exploratory model · Python bundle', format: 'Code & data download', route: 'story-fertility', downloadHref: 'research/fertility/fertility-research-full.zip', keywords: 'fertility TFR life expectancy levels first differences cointegration six economies' },
  { id: 'matching-dummy', family: 'fertility', title: 'Development + matching + post-2015 period dummy', question: 'What does adding marriage matching and a post-2015 period dummy change?', method: 'Exploratory model · Python bundle', format: 'Code & data download', route: 'story-fertility', downloadHref: 'research/fertility/fertility-research-full.zip', keywords: 'fertility marriage matching period dummy post-2015 held-out fit' },
  { id: 'credential-cohort', family: 'fertility', title: 'Credential cohort model', question: 'Can mass education raising the cost of each child generate a fertility floor?', method: 'Exploratory model · Python bundle', format: 'Code & data download', route: 'story-fertility', downloadHref: 'research/fertility/fertility-research-full.zip', keywords: 'fertility credential cohort mass education child cost synthetic' },
  { id: 'mechanism-assortative', family: 'fertility', title: 'Assortative matching mechanism lab', question: 'Can a credential floor with women marrying up reproduce Korean marriage facts?', method: 'Exploratory model · Python bundle', format: 'Code & data download', route: 'story-fertility', downloadHref: 'research/fertility/fertility-research-full.zip', keywords: 'fertility assortative matching marriage Korea credential floor synthetic cohort' },
  { id: 'fecundity-age', family: 'fertility', title: 'Fecundity-age model', question: 'How much do delayed marriages cut births under an age-specific fecundity curve?', method: 'Exploratory model · Python bundle', format: 'Code & data download', route: 'story-fertility', downloadHref: 'research/fertility/fertility-research-full.zip', keywords: 'fertility fecundity age marriage delay births calibration' },
  { id: 'ivf-policy', family: 'fertility', title: 'IVF and policy suite', question: 'What do IVF and policy levers do to completed fertility in a synthetic Korea-like cohort?', method: 'Exploratory model · Python bundle', format: 'Code & data download', route: 'story-fertility', downloadHref: 'research/fertility/fertility-research-full.zip', keywords: 'fertility IVF policy completed fertility Korea synthetic cohort' },
  { id: 'shock-suite', family: 'fertility', title: 'Post-2015 shock suite', question: 'Can a post-2015 shock explain the timing, and which shocks does it separate?', method: 'Exploratory model · Python bundle', format: 'Code & data download', route: 'story-fertility', downloadHref: 'research/fertility/fertility-research-full.zip', keywords: 'fertility post-2015 shock timing period dummy country spread' },
  { id: 'microplastics-test', family: 'fertility', title: 'Microplastics test', question: 'Do microplastics fit the post-2015 fertility pattern?', method: 'Exploratory model · Python bundle', format: 'Code & data download', route: 'story-fertility', downloadHref: 'research/fertility/fertility-research-full.zip', keywords: 'fertility microplastics post-2015 pattern timing test' },
  { id: 'momentum-test', family: 'fertility', title: 'Tipping / momentum lab', question: 'Can peer-driven thresholds tip fertility into a lasting low?', method: 'Exploratory model · Python bundle', format: 'Code & data download', route: 'story-fertility', downloadHref: 'research/fertility/fertility-research-full.zip', keywords: 'fertility tipping momentum peer thresholds social norms low fertility' },
  { id: 'fertility-bundle', family: 'fertility', title: 'Fertility research bundle', question: 'Historical code and results for exploratory fertility scenarios. Read the research protocols before interpreting fitted relationships or policy effects.', method: 'Code, data & findings · download', format: 'Code & data download', href: 'research/fertility.html', downloadHref: 'research/fertility/fertility-research-full.zip', keywords: 'fertility code data findings zip download' },
]

const shadow: CatalogueItemInput[] = [
  { id: 'shadow-education', family: 'shadow', title: 'Shadow education lab', question: 'Why do pupils pay their own teachers? Three rival explanations tested against seven published patterns.', method: 'Agent-based model · Cambodia', format: 'Write-up', href: 'research/shadow-education.html', keywords: 'shadow education private tutoring Cambodia Bray diversion favour' },
  { id: 'shadow-abm', family: 'shadow', title: 'Tutoring ABM bundle', question: 'Historical calibration bundle. Provider observation equations and the SMC evidence estimator were subsequently corrected; new calibration runs are required.', method: 'Code & data · download', format: 'Code & data download', route: 'story-shadow', downloadHref: 'research/shadow/tutoring_abm.zip', keywords: 'tutoring agent based model code download' },
  { id: 'shadow-dhs', family: 'education', title: 'Credential-floor DHS test', question: 'Who leaves school? Three structures predict different shares of leavers from the poorest 40% of households, checked against the Cambodia DHS.', method: 'Code & data · download', format: 'Code & data download', route: 'story-shadow', downloadHref: 'research/shadow/credential_floor_dhs.zip', keywords: 'credential floor DHS Cambodia poorest households download' },
]

const deephistory: CatalogueItemInput[] = [
  { id: 'out-of-africa', family: 'deephistory', title: 'Coast or herds? The route out of Africa', question: 'Did the first people to reach Australia follow the shoreline or the big game? 800 simulated dispersals across a drowned Ice Age landscape.', method: 'Monte Carlo · least-cost dispersal', format: 'Write-up', href: 'research/out-of-africa.html', keywords: 'out of Africa dispersal coast megafauna Sahul Arabia sea level Monte Carlo ice age prehistory human evolution' },
  { id: 'out-of-africa-bundle', family: 'deephistory', title: 'Out of Africa model bundle', question: 'The Python model, the 800-run Monte Carlo results, the landscape grid and the static maps.', method: 'Code & data · download', format: 'Code & data download', route: 'story-deephistory', downloadHref: 'research/out-of-africa/coast-or-herds-model.zip', keywords: 'out of Africa code data download python' },
]

const politics: CatalogueItemInput[] = [
  { id: 'ccp-v1', family: 'politics', title: 'CCP bus · Rival mechanisms', question: 'Which rival mechanism — enforcement, social trap or bus — best reproduces the observed pattern of disciplinary filings?', method: 'Stored experiment · Mechanism comparison', format: 'Code & data download', route: 'story-politics', downloadHref: 'research/ccp-bus/ccp-bus-v1.zip', keywords: 'CCP corruption enforcement social trap bus mechanism comparison' },
  { id: 'ccp-v3', family: 'politics', title: 'CCP bus · Economy and factions', question: 'How do economic conditions and factional competition interact to shape enforcement outcomes in the stored exploratory fit?', method: 'Stored experiment · Exploratory fit', format: 'Code & data download', route: 'story-politics', downloadHref: 'research/ccp-bus/ccp-bus-v3.zip', keywords: 'CCP economy factions exploratory fit enforcement' },
  { id: 'ccp-v6', family: 'politics', title: 'CCP bus · Tilly mechanisms', question: 'Can Tilly-style state-making mechanisms — extraction, coercion and capital — illustrate how enforcement obligations outlast a campaign?', method: 'Stored experiment · Illustrative kernel', format: 'Code & data download', route: 'story-politics', downloadHref: 'research/ccp-bus/ccp-bus-v6.zip', keywords: 'CCP Tilly state making extraction coercion capital illustrative kernel' },
  { id: 'ccp-v7', family: 'politics', title: 'CCP bus · Identification comparison', question: 'How do three mechanism families compare on identification in a common kernel — what each can and cannot distinguish given the observed disciplinary filings?', method: 'Stored experiment · Retrospective evaluation', format: 'Code & data download', route: 'story-politics', downloadHref: 'research/ccp-bus/ccp-bus-v7.zip', keywords: 'CCP identification comparison retrospective evaluation disciplinary filings mechanism families common kernel' },
]

const extension: CatalogueItemInput[] = [
  { id: 'fs-diffusion', family: 'extension', title: 'Farmer field schools · Diffusion', question: 'How does adoption spread through a finite horizon when existing adopters mediate it after an initial seed?', method: 'Stored experiment · diffusion grid', format: 'Code & data download', route: 'story-extension', downloadHref: 'research/field-schools/field-schools-models.zip', keywords: 'extension diffusion adoption finite horizon adopter mediated seed' },
  { id: 'fs-foodprice', family: 'extension', title: 'Farmer field schools · Food-price politics', question: 'What does the food-price model show on its endogenous simulated path, and what can it not show?', method: 'Stored experiment · annual periods 2004–2024', format: 'Code & data download', route: 'story-extension', downloadHref: 'research/field-schools/field-schools-models.zip', keywords: 'extension food price politics OLS endogenous simulated path' },
  { id: 'fs-treadmill', family: 'extension', title: 'Farmer field schools · Treadmill economy', question: 'What did the earlier treadmill mechanism story propose, and how should it be read now?', method: 'Historical mechanism card', format: 'Narrated journey', route: 'story-extension', keywords: 'extension treadmill economy historical mechanism card superseded' },
  { id: 'fs-pricetag', family: 'extension', title: 'Farmer field schools · Price-tag advice market', question: 'What did the earlier price-tag advice story propose about ambiguity and willingness to pay for private advice?', method: 'Historical mechanism card', format: 'Narrated journey', route: 'story-extension', keywords: 'extension price tag advice market historical unverified ambiguity willingness to pay' },
]

const catalogueInput: CatalogueItemInput[] = [...education, ...systems, ...planning, ...angkor, ...fertility, ...shadow, ...deephistory, ...politics, ...extension]
export const catalogue: CatalogueItem[] = catalogueInput.map(item => ({ ...item, tags: tagsFor(item) }))

/** Reverse index: tag -> entries. Family and kind tags included. */
export const tagIndex: Record<string, CatalogueItem[]> = {}
for (const item of catalogue) for (const tag of item.tags) (tagIndex[tag] ??= []).push(item)
export const tagCounts: Record<string, number> = Object.fromEntries(Object.entries(tagIndex).map(([tag, items]) => [tag, items.length]))
/** Every tag, most used first, then alphabetical. */
const byUsage = (a: string, b: string) => tagCounts[b] - tagCounts[a] || a.localeCompare(b)
export const allTags: string[] = Object.keys(tagIndex).sort(byUsage)
/** Grouped layers for the browse cloud: plain language first, then specifics, type and status. */
export const broadTags: string[] = allTags.filter(tag => tagGroup(tag) === 'broad').sort(byUsage)
export const specificTags: string[] = allTags.filter(tag => tagGroup(tag) === 'specific').sort(byUsage)
export const typeTags: string[] = allTags.filter(tag => tagGroup(tag) === 'type').sort(byUsage)
export const statusTags: string[] = allTags.filter(tag => tagGroup(tag) === 'status').sort(byUsage)
export const tagStats = { total: allTags.length, broad: broadTags.length, specific: specificTags.length, type: typeTags.length, status: statusTags.length }
export { tagGroup, tagsFor }
export const modelFamilies: ModelFamily[] = ['education', 'systems', 'planning', 'angkor', 'fertility', 'shadow', 'deephistory', 'politics', 'extension']

/** Menu and homepage grouping (Trey, 19 Nov 2026). Families are research areas; the toolkit is methods, not models. */
export const familyGroups: { id: string; title: string; families: ModelFamily[] }[] = [
  { id: 'education', title: 'Education and schooling', families: ['education', 'shadow', 'systems', 'extension'] },
  { id: 'society', title: 'Societies, history and evolution', families: ['angkor', 'deephistory', 'fertility', 'politics'] },
  { id: 'tools', title: 'Planning toolkit', families: ['planning'] },
]
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
    title: 'Education Planning Toolkit · UN methods', short: 'Ed planning toolkit',
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
    description: 'Exploratory fertility models across six economies, with explicit assumptions about development, family formation, birth timing and period effects.',
  },
  shadow: {
    title: 'Shadow education', short: 'Shadow ed',
    question: 'Why do pupils pay their own teachers?',
    description: 'Explore rival mechanisms for private tutoring in Cambodia. Corrected provider measurements require recalibration; policy comparisons depend on shared rules.',
  },
  deephistory: {
    title: 'Deep history · Human dispersal', short: 'Deep history',
    question: 'How did people get from Africa to Australia?',
    description: 'A paleo-landscape model of the exit from Africa 85,000–65,000 years ago: coast-huggers, big-game hunters and mixed foragers raced across shifting sea levels and Green Arabia.',
  },
  politics: {
    title: 'Political economy', short: 'Political economy',
    question: 'Can enforcement change corruption when obligations outlast a campaign?',
    description: 'Four stored model versions compare competing synthetic mechanisms against observed disciplinary filings. The models describe mechanisms, not the prevalence of corruption.',
  },
  extension: {
    title: 'Farmer field schools & food politics', short: 'Field schools',
    question: 'Can training farmers change what they know without making adoption pay?',
    description: 'A narrated extension story with two current mechanism models and two historical mechanism cards. Observational motivation is not calibrated validation: training may change knowledge without making adoption pay.',
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
  politics: [
    { label: 'CCP bus · Rival mechanisms (v1)', href: 'research/ccp-bus/ccp-bus-v1.zip' },
    { label: 'CCP bus · Economy and factions (v3)', href: 'research/ccp-bus/ccp-bus-v3.zip' },
    { label: 'CCP bus · Tilly mechanisms (v6)', href: 'research/ccp-bus/ccp-bus-v6.zip' },
    { label: 'CCP bus · Identification comparison (v7)', href: 'research/ccp-bus/ccp-bus-v7.zip' },
    { label: 'Source · experiments/ccp-bus/models/', href: 'https://github.com/TreyModels/atlas-of-education/tree/2e19f07/experiments/ccp-bus/models/' },
  ],
  extension: [
    { label: 'Model bundle · code, data & README', href: 'research/field-schools/field-schools-models.zip' },
    { label: 'README', href: 'research/field-schools/README.md' },
    { label: 'Validation notes', href: 'research/field-schools/VALIDATION.md' },
  ],
}

/** Experimental interfaces deliberately sit outside `catalogue`, so they never inflate totalModels or familyCounts. */
const experimentalInput: CatalogueItemInput[] = [
  {
    id: 'scenario-theatre', family: 'planning', title: 'Scenario Theatre',
    question: 'How does the current plan compare with a pinned run on cost, the unfunded share and completion?',
    method: 'Prototype · pinned-versus-current model runs', format: 'Experimental interface', route: 'sector',
    keywords: 'scenario theatre pinned comparison experimental planning sector',
  },
]
export const experimentalInterfaces: CatalogueItem[] = experimentalInput.map(item => ({ ...item, tags: tagsFor(item) }))

export const classicLabs = [
  { title: 'Original Angkor Atlas', description: 'The unified offline experiment in rice, population, temples, labour and regional competition.', href: 'reference/angkor/index.html', label: 'Classic integrated lab' },
  { title: 'Angkor Mandala Lab', description: 'The original spatial implementation of pledges, population and political reach.', href: 'reference/mandala/index.html', label: 'Classic spatial lab' },
  { title: 'Monte Carlo Methods Studio', description: 'Run historical scenarios repeatedly and inspect distributions rather than a single trajectory.', href: 'reference/monte-carlo/index.html', label: 'Methods classroom' },
]
