import type { CatalogueItem } from './model-catalogue'

/**
 * Curated hashtag vocabulary for the Atlas Worlds catalogue.
 *
 * Two audiences, one index (Trey, 19 November 2026): a non-specialist should be able
 * to search #economics, #education, #history, #jobs or #families; a specialist
 * can still use #credential-floor, #massification or #monte-carlo.
 *
 * Layers:
 * - broad:    plain-language disciplines and everyday topics (what most people type)
 * - specific: jargon and named mechanisms (a second way in, never the only way)
 * - type:     how the entry is delivered (workbench, classic lab, download, …)
 * - status:   how far the entry can be trusted (historical, mechanism, developing, evaluated)
 *
 * Honesty rules: every broad tag covers at least three models, every non-family
 * specific tag at least two; every model gets a broad tag, and none is
 * jargon-only. Tags are lowercase ASCII: letters, digits and hyphens.
 */

export const DISCIPLINES = [
  'economics',
  'education',
  'sociology',
  'political-science',
  'history',
  'archaeology',
  'demography',
  'anthropology',
  'geography',
  'environmental-studies',
  'agriculture',
  'public-health',
  'statistics',
  'complexity',
  'public-policy',
  'development',
] as const

export const PLAIN_TOPICS = [
  'schools',
  'teachers',
  'students',
  'jobs',
  'families',
  'marriage',
  'births',
  'water',
  'food',
  'farming',
  'money',
  'budgets',
  'government',
  'corruption',
  'climate',
  'cities',
  'migration',
  'skills',
  'credentials',
  'tutoring',
  'land',
  'taxes',
  'inequality',
  'networks',
  'simulation',
] as const

/** Broad = the plain-language layer: disciplines plus everyday topics. */
export const BROAD_TAGS: string[] = [...DISCIPLINES, ...PLAIN_TOPICS]

export const STATUS_TAGS = ['historical', 'mechanism', 'developing', 'evaluated'] as const

export const TYPE_TAGS = ['workbench', 'classic-lab', 'download', 'write-up', 'narrated', 'experimental', 'stored-experiment'] as const

export const FAMILY_TAGS: Record<CatalogueItem['family'], string> = {
  education: 'education',
  systems: 'school-systems',
  planning: 'planning',
  angkor: 'angkor',
  fertility: 'fertility',
  shadow: 'shadow-education',
  deephistory: 'deep-history',
  politics: 'political-economy',
  extension: 'field-schools',
}

export const KIND_TAGS: Record<CatalogueItem['format'], string> = {
  'Atlas workbench': 'workbench',
  'Classic workbench': 'classic-lab',
  'Write-up': 'write-up',
  'Code & data download': 'download',
  'Narrated journey': 'narrated',
  'Experimental interface': 'experimental',
}

export type ModelTagSet = {
  /** 1-4 plain-language tags. At least one discipline; topics where sensible. */
  broad: string[]
  /** Jargon / named mechanisms. Secondary, never the only way in. */
  specific?: string[]
  /** How far the entry can be trusted. */
  status?: string[]
}

const d = (tag: (typeof DISCIPLINES)[number]) => tag
const t = (tag: (typeof PLAIN_TOPICS)[number]) => tag

export const MODEL_TAGS: Record<string, ModelTagSet> = {
  // ── Education, work & credentials ────────────────────────────────────────
  china: { broad: [d('economics'), d('education'), t('jobs'), t('skills')], specific: ['china', 'graduate-jobs', 'credential-floor'] },
  cambodia: { broad: [d('economics'), d('education'), t('families'), t('tutoring')], specific: ['cambodia', 'labour', 'households'] },
  credentials: { broad: [d('economics'), d('education'), t('credentials'), t('jobs')], specific: ['credential-floor', 'graduate-jobs'], status: ['mechanism'] },
  'massification-parents': { broad: [d('education'), d('sociology'), t('families')], specific: ['massification', 'credential-floor', 'households'] },
  'massification-actors': { broad: [d('education'), d('sociology'), t('government')], specific: ['massification', 'credential-floor', 'institutions'] },
  'massification-access': { broad: [d('education'), d('sociology'), t('inequality')], specific: ['massification', 'credential-floor', 'access'] },
  'massification-persistence': { broad: [d('education'), d('sociology'), t('credentials'), t('networks')], specific: ['massification', 'credential-floor'], status: ['mechanism'] },

  // ── Population & school systems ──────────────────────────────────────────
  'school-futures': { broad: [d('education'), d('demography'), t('schools'), t('teachers')], specific: ['east-asia', 'forecasting', 'enrolment'] },
  'city-networks': { broad: [d('education'), d('geography'), t('cities')], specific: ['east-asia', 'forecasting', 'networks'] },
  'city-system': { broad: [d('education'), d('demography'), t('cities'), t('migration')], specific: ['synthetic', 'forecasting'] },
  'cambodia-system': { broad: [d('education'), d('demography'), t('schools')], specific: ['cambodia', 'forecasting', 'enrolment'] },
  'china-system': { broad: [d('education'), d('demography'), t('schools')], specific: ['china', 'east-asia', 'forecasting', 'enrolment'] },
  'philippines-system': { broad: [d('education'), d('demography'), t('schools')], specific: ['enrolment', 'policy'] },
  'kenya-system': { broad: [d('education'), d('demography'), d('development')], specific: ['enrolment', 'policy'] },
  'riverton-system': { broad: [d('education'), d('demography'), t('cities')], specific: ['synthetic', 'forecasting'] },
  'stillwater-system': { broad: [d('education'), d('demography'), t('cities')], specific: ['synthetic', 'forecasting'] },

  // ── Education Planning Toolkit ───────────────────────────────────────────
  cohort: { broad: [d('education'), d('demography'), t('students')], specific: ['cohort-flow', 'enrolment', 'completion', 'accounting'] },
  indicators: { broad: [d('education'), d('statistics'), t('schools')], specific: ['enrolment'] },
  sector: { broad: [d('education'), t('budgets'), t('taxes')], specific: ['financing', 'forecasting', 'enrolment'] },
  population: { broad: [d('demography'), d('education'), t('schools')], specific: ['forecasting', 'enrolment', 'cohort-flow'] },
  teachers: { broad: [d('education'), d('demography'), t('teachers'), t('students')], specific: ['forecasting', 'deployment'] },
  deployment: { broad: [d('education'), d('public-policy'), t('teachers')], specific: ['deployment'] },
  equity: { broad: [d('economics'), d('education'), t('budgets'), t('money')], specific: ['financing', 'inequality'] },
  grants: { broad: [d('education'), d('public-policy'), t('budgets'), t('money')], specific: ['financing', 'inequality'] },
  schoolmap: { broad: [d('education'), d('geography'), t('schools'), t('land')], specific: ['access', 'facilities'] },
  lays: { broad: [d('education'), t('students'), t('skills')], specific: ['targets'] },
  logistic: { broad: [d('education'), d('statistics'), d('public-policy')], specific: ['targets', 'forecasting'] },
  absorption: { broad: [d('economics'), d('education'), t('jobs'), t('skills')], specific: ['completion', 'labour', 'accounting'] },

  // ── Historical systems · Angkor ──────────────────────────────────────────
  provisioning: { broad: [d('archaeology'), d('history'), t('water'), t('food')], specific: ['provisioning', 'tithes', 'labour'] },
  campaign: { broad: [d('archaeology'), d('history'), d('political-science'), t('government')], specific: ['authority', 'temples', 'labour'] },
  angkor: { broad: [d('archaeology'), d('anthropology'), d('history'), t('land')], specific: ['temples', 'authority', 'monuments'] },
  signalling: { broad: [d('archaeology'), d('history'), t('networks')], specific: ['authority', 'monuments'] },
  obligations: { broad: [d('archaeology'), d('history'), d('political-science'), t('taxes')], specific: ['tithes', 'authority', 'labour'] },
  monsoon: { broad: [d('environmental-studies'), t('climate'), t('water'), t('food')], specific: ['uncertainty', 'provisioning'] },
  mandala: { broad: [d('archaeology'), d('complexity'), t('networks'), t('simulation')], specific: ['authority'], status: ['historical'] },
  accounts: { broad: [d('archaeology'), d('history'), t('taxes')], specific: ['accounting', 'temples', 'tithes'], status: ['historical'] },
  institutions: { broad: [d('archaeology'), d('history'), t('government'), t('simulation')], specific: ['authority', 'institutions'], status: ['historical'] },
  flight: { broad: [d('archaeology'), d('history'), t('migration'), t('inequality')], specific: ['authority', 'households'] },
  maintenance: { broad: [d('archaeology'), d('environmental-studies'), t('water'), t('simulation')], specific: ['facilities', 'labour'] },
  relocation: { broad: [d('archaeology'), d('geography'), t('migration'), t('inequality')], specific: ['access', 'households'] },
  petri: { broad: [d('complexity'), d('sociology'), t('networks'), t('inequality')], status: ['mechanism'] },

  // ── Fertility & family formation ─────────────────────────────────────────
  'fertility-collapse': { broad: [d('demography'), d('sociology'), t('families'), t('marriage')], specific: ['fecundity', 'east-asia'] },
  'development-survival': { broad: [d('demography'), d('statistics'), d('development')], specific: ['calibration'] },
  'matching-dummy': { broad: [d('demography'), d('sociology'), t('marriage')], specific: ['assortative-matching', 'calibration'] },
  'credential-cohort': { broad: [d('demography'), d('education'), t('credentials')], specific: ['credential-floor', 'massification', 'households'] },
  'mechanism-assortative': { broad: [d('demography'), d('sociology'), t('marriage')], specific: ['credential-floor', 'assortative-matching'], status: ['mechanism'] },
  'fecundity-age': { broad: [d('demography'), d('public-health'), t('births')], specific: ['fecundity', 'marriage'] },
  'ivf-policy': { broad: [d('demography'), d('public-health'), d('public-policy')], specific: ['fecundity'] },
  'shock-suite': { broad: [d('demography'), d('statistics'), t('births')], specific: ['shocks'] },
  'microplastics-test': { broad: [d('demography'), d('public-health'), d('environmental-studies')], specific: ['shocks'] },
  'momentum-test': { broad: [d('demography'), d('complexity'), t('networks'), t('births')], status: ['mechanism'] },
  'fertility-bundle': { broad: [d('demography'), d('development'), t('families'), t('births')], specific: ['calibration'] },

  // ── Shadow education ─────────────────────────────────────────────────────
  'shadow-education': { broad: [d('education'), d('sociology'), t('tutoring')], specific: ['agent-based'], status: ['developing'] },
  'shadow-abm': { broad: [d('education'), d('sociology'), t('tutoring')], specific: ['agent-based', 'calibration'], status: ['developing'] },
  'shadow-dhs': { broad: [d('education'), d('statistics'), t('inequality')], specific: ['credential-floor', 'households'] },

  // ── Deep history ─────────────────────────────────────────────────────────
  'out-of-africa': { broad: [d('anthropology'), d('archaeology'), t('climate'), t('land')], specific: ['monte-carlo', 'uncertainty'], status: ['evaluated'] },
  'out-of-africa-bundle': { broad: [d('anthropology'), d('archaeology'), t('climate')], specific: ['monte-carlo'] },

  // ── Political economy ────────────────────────────────────────────────────
  'ccp-v1': { broad: [d('political-science'), d('sociology'), t('government'), t('corruption')], specific: ['enforcement'], status: ['mechanism'] },
  'ccp-v3': { broad: [d('political-science'), d('sociology'), t('government'), t('corruption')], specific: ['enforcement', 'factions'] },
  'ccp-v6': { broad: [d('political-science'), d('history'), t('government'), t('corruption')], specific: ['enforcement'], status: ['historical'] },
  'ccp-v7': { broad: [d('political-science'), d('statistics'), t('corruption')], specific: ['enforcement', 'factions'], status: ['evaluated'] },

  // ── Farmer field schools ─────────────────────────────────────────────────
  'fs-diffusion': { broad: [d('agriculture'), t('farming'), d('sociology')], specific: ['adoption'] },
  'fs-foodprice': { broad: [d('agriculture'), t('farming'), t('food')], specific: ['adoption', 'prices'] },
  'fs-treadmill': { broad: [d('agriculture'), t('farming')], specific: ['adoption'], status: ['historical'] },
  'fs-pricetag': { broad: [d('agriculture'), t('farming'), t('money')], specific: ['adoption', 'prices'], status: ['historical'] },
}

const TAG_PATTERN = /^[a-z0-9][a-z0-9-]*$/
const BROAD_SET: Set<string> = new Set(BROAD_TAGS)
const TYPE_SET: Set<string> = new Set(TYPE_TAGS)
const STATUS_SET: Set<string> = new Set(STATUS_TAGS)

/** Which layer a tag belongs to, so the UI can group the cloud. */
export function tagGroup(tag: string): 'broad' | 'specific' | 'type' | 'status' {
  if (BROAD_SET.has(tag)) return 'broad'
  if (TYPE_SET.has(tag)) return 'type'
  if (STATUS_SET.has(tag)) return 'status'
  return 'specific'
}

/** Broad tags first, then family/collection, specifics, delivery type and status. */
export function tagsFor(item: Pick<CatalogueItem, 'id' | 'family' | 'format' | 'method'>): string[] {
  const curated = MODEL_TAGS[item.id]
  const tags = [
    ...(curated?.broad ?? []),
    FAMILY_TAGS[item.family],
    ...(curated?.specific ?? []),
    KIND_TAGS[item.format],
    ...(curated?.status ?? []),
    ...(/^stored experiment/i.test(item.method) ? ['stored-experiment'] : []),
  ]
  return [...new Set(tags)].filter(tag => TAG_PATTERN.test(tag))
}

export { TAG_PATTERN }
