import type { CatalogueItem } from './model-catalogue'

/**
 * Curated hashtag vocabulary for the Atlas Worlds catalogue (Trey, 22 Nov 2026).
 *
 * Tags are lowercase ASCII: letters, digits and hyphens only. Each model gets
 * three to seven tags. Family and kind tags are derived automatically from the
 * entry, so only themes and a few documented maturity labels live here.
 *
 * Honesty rule: a theme tag must describe at least two entries, or be a family
 * tag (one per collection). No tag is decoration: every tag in this file is a
 * real axis you can filter on. Models are not tagged with everything.
 */
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

/** Explicit theme and maturity tags. Family and kind tags are added automatically. */
export const MODEL_TAGS: Record<string, string[]> = {
  // Education, work & credentials
  china: ['china', 'graduate-jobs', 'wages', 'labour', 'credential-floor'],
  cambodia: ['cambodia', 'labour', 'households', 'policy'],
  credentials: ['credential-floor', 'graduate-jobs', 'inequality', 'networks', 'stored-experiment'],
  'massification-parents': ['massification', 'credential-floor', 'households', 'inequality'],
  'massification-actors': ['massification', 'credential-floor', 'networks', 'institutions'],
  'massification-access': ['massification', 'credential-floor', 'inequality', 'access'],
  'massification-persistence': ['massification', 'credential-floor', 'networks', 'inequality', 'mechanism'],

  // Population & school systems
  'school-futures': ['east-asia', 'teachers', 'forecasting', 'enrolment', 'demographics'],
  'city-networks': ['east-asia', 'networks', 'teachers', 'forecasting'],
  'city-system': ['migration', 'teachers', 'demographics', 'synthetic', 'forecasting'],
  'cambodia-system': ['cambodia', 'demographics', 'enrolment', 'teachers'],
  'china-system': ['china', 'east-asia', 'demographics', 'teachers', 'enrolment'],
  'philippines-system': ['enrolment', 'teachers', 'policy', 'demographics', 'forecasting'],
  'kenya-system': ['enrolment', 'teachers', 'policy', 'demographics'],
  'riverton-system': ['synthetic', 'demographics', 'teachers', 'forecasting'],
  'stillwater-system': ['synthetic', 'demographics', 'teachers', 'forecasting'],

  // Education Planning Toolkit
  cohort: ['demographics', 'enrolment', 'completion', 'accounting'],
  indicators: ['enrolment', 'teachers', 'accounting'],
  sector: ['budgets', 'teachers', 'enrolment', 'financing', 'forecasting'],
  population: ['demographics', 'forecasting', 'enrolment', 'completion'],
  teachers: ['teachers', 'forecasting', 'deployment', 'demographics'],
  deployment: ['teachers', 'deployment', 'inequality'],
  equity: ['budgets', 'financing', 'inequality', 'accounting'],
  grants: ['budgets', 'financing', 'inequality', 'policy'],
  schoolmap: ['access', 'facilities', 'policy'],
  lays: ['learning', 'targets', 'enrolment'],
  logistic: ['targets', 'forecasting', 'learning'],
  absorption: ['completion', 'labour', 'wages', 'accounting'],

  // Historical systems · Angkor
  provisioning: ['water', 'food', 'agriculture', 'labour', 'tithes'],
  campaign: ['authority', 'labour', 'temples', 'monuments'],
  angkor: ['temples', 'monuments', 'authority', 'simulation'],
  signalling: ['authority', 'networks', 'monuments'],
  obligations: ['tithes', 'authority', 'labour'],
  monsoon: ['climate', 'water', 'agriculture', 'food', 'uncertainty'],
  mandala: ['authority', 'networks', 'simulation', 'historical', 'stored-experiment'],
  accounts: ['accounting', 'temples', 'tithes', 'historical'],
  institutions: ['institutions', 'authority', 'historical', 'simulation'],
  flight: ['migration', 'inequality', 'authority', 'simulation'],
  maintenance: ['water', 'facilities', 'labour', 'simulation'],
  relocation: ['migration', 'inequality', 'access', 'simulation'],
  petri: ['networks', 'inequality', 'simulation', 'mechanism'],

  // Fertility & family formation
  'fertility-collapse': ['fertility', 'marriage', 'korea', 'east-asia', 'fecundity'],
  'development-survival': ['fertility', 'development', 'regression', 'calibration'],
  'matching-dummy': ['fertility', 'marriage', 'regression', 'korea'],
  'credential-cohort': ['fertility', 'credential-floor', 'massification', 'households'],
  'mechanism-assortative': ['fertility', 'marriage', 'korea', 'credential-floor', 'mechanism'],
  'fecundity-age': ['fertility', 'fecundity', 'marriage', 'regression'],
  'ivf-policy': ['fertility', 'policy', 'korea', 'fecundity'],
  'shock-suite': ['fertility', 'shocks', 'regression', 'policy'],
  'microplastics-test': ['fertility', 'shocks', 'regression', 'policy'],
  'momentum-test': ['fertility', 'networks', 'mechanism', 'simulation'],
  'fertility-bundle': ['fertility', 'development', 'marriage'],

  // Shadow education
  'shadow-education': ['tutoring', 'cambodia', 'agent-based', 'mechanism', 'developing'],
  'shadow-abm': ['tutoring', 'agent-based', 'calibration', 'developing'],
  'shadow-dhs': ['credential-floor', 'cambodia', 'inequality', 'regression'],

  // Deep history
  'out-of-africa': ['migration', 'africa', 'monte-carlo', 'climate', 'uncertainty', 'simulation'],
  'out-of-africa-bundle': ['migration', 'africa', 'monte-carlo', 'simulation'],

  // Political economy
  'ccp-v1': ['ccp', 'corruption', 'enforcement', 'mechanism'],
  'ccp-v3': ['ccp', 'corruption', 'factions', 'simulation'],
  'ccp-v6': ['ccp', 'corruption', 'enforcement', 'institutions', 'historical'],
  'ccp-v7': ['ccp', 'corruption', 'enforcement', 'factions', 'regression'],

  // Farmer field schools
  'fs-diffusion': ['adoption', 'agriculture', 'networks', 'simulation'],
  'fs-foodprice': ['adoption', 'food', 'prices', 'agriculture'],
  'fs-treadmill': ['adoption', 'agriculture', 'historical', 'mechanism'],
  'fs-pricetag': ['adoption', 'prices', 'historical', 'mechanism'],
}

const TAG_PATTERN = /^[a-z0-9][a-z0-9-]*$/

/** Family tag + kind tag + curated tags, de-duplicated in that order. */
export function tagsFor(item: Pick<CatalogueItem, 'id' | 'family' | 'format' | 'method'>): string[] {
  const tags = [FAMILY_TAGS[item.family], KIND_TAGS[item.format], ...(MODEL_TAGS[item.id] ?? [])]
  if (/^stored experiment/i.test(item.method)) tags.push('stored-experiment')
  return [...new Set(tags)].filter(tag => TAG_PATTERN.test(tag))
}

export { TAG_PATTERN }
