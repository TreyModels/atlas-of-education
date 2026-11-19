// Site-wide status overview and call to action, shown at the top of the homepage.
// Content owned by Claude; Kimi renders it. Purpose and state words match angkor-journey.ts.
import type { ModelFamily } from './model-catalogue'
import type { DevState, Purpose } from './angkor-journey'

export interface FamilyStatus { family: ModelFamily | 'politics'; route: string; line: string; purposes: Purpose[]; states: DevState[]; narrated: boolean }

export const statusIntro = {
  kicker: 'Read this first',
  title: 'Models you can inspect, with their code and limits',
  text: 'Some models implement findings from peer-reviewed studies. Some explore what would follow if a mechanism held. Some exist to teach an idea, and some are still being built. Each model page says which, and how far it has been checked. A label is a limit on what the model can claim, not a grade.',
}

export const familyStatus: FamilyStatus[] = [
  { family: 'angkor', route: 'story-angkor', narrated: true, purposes: ['published', 'mechanism', 'teaching', 'accounting'], states: ['checked', 'developing', 'historical'], line: 'Built on a peer-reviewed study (Klassen et al. 2022); the extensions are mechanism explorations, labelled one by one.' },
  { family: 'shadow', route: 'story-shadow', narrated: true, purposes: ['mechanism'], states: ['historical', 'developing'], line: 'Three explanations of tutoring fit the published patterns equally well; the archived calibration predates later corrections.' },
  { family: 'politics', route: 'story-politics', narrated: true, purposes: ['mechanism'], states: ['checked', 'developing', 'evaluated'], line: 'Four versions of a path-dependence model; a holdout test cannot yet tell it apart from simpler mechanisms. Synthetic agents only.' },
  { family: 'extension', route: 'story-extension', narrated: true, purposes: ['mechanism'], states: ['developing', 'historical'], line: 'Farmer field schools and food politics: two developing mechanism models and two historical mechanism cards. Observational motivation is not calibrated validation.' },
  { family: 'planning', route: 'story-planning', narrated: true, purposes: ['teaching', 'accounting'], states: ['checked', 'developing'], line: 'Planning methods in the UN education-planning tradition, with the arithmetic shown. Not official UNESCO software.' },
  { family: 'fertility', route: 'story-fertility', narrated: true, purposes: ['mechanism', 'teaching'], states: ['developing'], line: 'Exploratory models of six economies; the levels link to survival does not survive differencing.' },
  { family: 'education', route: 'story-education', narrated: true, purposes: ['mechanism', 'teaching'], states: ['developing', 'checked', 'evaluated'], line: 'Credentials, schooling and work, including the China youth-unemployment model (fitted with an unexplained residual).' },
  { family: 'systems', route: 'story-systems', narrated: true, purposes: ['accounting', 'teaching'], states: ['checked', 'developing'], line: 'Cohorts, teachers, classrooms and budgets followed through demographic change.' },
  { family: 'deephistory', route: 'story-deephistory', narrated: true, purposes: ['mechanism'], states: ['developing'], line: 'Routes out of Africa: rankings depend on stated constraints and priors, which the page shows.' },
]

export const callToAction = {
  title: 'Think a model is missing something? Change it.',
  text: 'Every model can be downloaded, run on your own machine and modified. If you change an assumption, add data or find a mistake, propose your version. Proposals are reviewed by Dr. Trey Menefee before anything is listed here.',
  actions: [
    { label: 'Download all the code', href: 'https://github.com/TreyModels/atlas-of-education/archive/refs/heads/main.zip' },
    { label: 'Propose a version', href: 'https://github.com/TreyModels/atlas-of-education/issues/new?template=propose-a-version.yml' },
    { label: 'Challenge a claim', href: 'https://github.com/TreyModels/atlas-of-education/issues/new?template=model-challenge.yml' },
    { label: 'How to cite (CC BY-NC 4.0)', href: 'https://github.com/TreyModels/atlas-of-education/blob/main/CITATION.cff' },
  ],
  licence: 'Licensed CC BY-NC 4.0: reuse and adapt with credit to Dr. Trey Menefee, for noncommercial purposes. Versioned releases support citation; DOI details appear when available.',
}
