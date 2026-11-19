// Angkor journey: the narrated family page.
// Content only. Presentation lives in src/components/AngkorJourney.tsx (Kimi restyles it).
// Every number here is copied from a cited source or a stored Atlas result; the check
// script scripts/check-angkor-journey.mjs guards structure, labels and links.

/** Why a model exists. Separate from how far it has been checked. */
export type Purpose = 'published' | 'mechanism' | 'teaching' | 'accounting'
/** How far a model has been checked. "checked" means the code and ledgers were verified, not the history. */
export type DevState = 'checked' | 'developing' | 'historical' | 'evaluated'
/** What kind of claim a paragraph makes. */
export type Claim = 'published' | 'data' | 'sim' | 'open' | 'method'

export interface Para { claim?: Claim; text: string }
export interface ModelCard { id: string; title: string; purpose: Purpose; state: DevState; note: string; engine?: string; route?: string; research?: string }
export interface Maths { plain: string; formula?: string; symbols?: [string, string][]; example?: string }
export interface Source { label: string; href: string }
export interface Chapter {
  id: string; kicker: string; title: string; question: string
  evidence: Para[]; rule: Para[]; result: Para[]; limitation: Para[]
  maths?: Maths; sources: Source[]; models: string[]; interactive?: 'beta'
}
export interface Journey { kicker: string; title: string; lede: string; why: Para[]; chapters: Chapter[]; deeper: string[]; models: Record<string, ModelCard>; bottomLine: string; repo: string; family: string }

export const purposeLabel: Record<Purpose, { label: string; help: string }> = {
  published: { label: 'Published foundation', help: 'Implements relationships reported in a peer-reviewed study.' },
  mechanism: { label: 'Mechanism exploration', help: 'Asks what follows if these rules held. Not a reconstruction of what happened.' },
  teaching: { label: 'Teaching', help: 'Built to show an idea clearly. Complete for that purpose.' },
  accounting: { label: 'Description and accounting', help: 'Keeps food, labour and people consistent so other rules can be examined.' },
}
export const stateLabel: Record<DevState, { label: string; help: string }> = {
  checked: { label: 'Implementation checked', help: 'Code, ledgers and stored results verified. Not validated against history.' },
  developing: { label: 'In development', help: 'Known gaps remain in the rules or inputs; listed on the card.' },
  historical: { label: 'Historical result', help: 'Kept as a record. Its findings are superseded or limited.' },
  evaluated: { label: 'Empirically evaluated', help: 'Tested against observations it was not built from.' },
}
export const claimLabel: Record<Claim, string> = {
  published: 'From the published study',
  data: 'Observed data',
  sim: 'Produced by an Atlas simulation',
  open: 'Still unsettled',
  method: 'How the model works',
}

const KLASSEN = 'https://doi.org/10.1007/s10816-021-09535-5'

export const journey: Journey = {
  kicker: 'Historical systems · Angkor',
  title: 'How did a medieval city feed itself, and what could break it?',
  lede: 'Angkor, in today’s Cambodia, was one of the largest pre-industrial cities ever mapped: an urban landscape of at least 1,500 km² and up to 900,000 people between the 9th and 14th centuries. This page starts from a peer-reviewed study of how its food economy was organised, then follows the Atlas models built on top of it, one assumption at a time.',
  repo: 'https://github.com/TreyModels/atlas-of-education',
  family: 'angkor',
  why: [
    { text: 'Cities need farmers to feed people who do not farm. A common view in economic anthropology is that farming more intensively brings diminishing returns: each extra hour of work yields less. Angkor is hard to square with that view. Its core alone held more than 150,000 people.' },
    { text: 'So we ask two questions in order. First, what does the archaeological record say about how production was organised? That part is a published result. Second, if those relationships held, how would food, labour, authority and climate interact over time? That part is ours: a set of experiments, each labelled with its purpose and how far it has been checked.' },
    { claim: 'method', text: 'We follow a descriptive approach (Edmonds and Moss, “From KISS to KIDS”): add detail where the evidence supports it, and say plainly where a rule is assumed. The models do not compete to explain Angkor’s decline. They show which assumptions carry which results.' },
  ],
  chapters: [
    {
      id: 'klassen', kicker: 'Chapter 1 · The published foundation', interactive: 'beta',
      title: 'Temple communities and the provisioning of a city',
      question: 'How was agricultural production organised so that farmers could feed a city?',
      evidence: [
        { claim: 'published', text: 'Sarah Klassen, Scott Ortman, José Lobo and Damian Evans (2022) used extensive documentation of the Greater Angkor Region: temple communities, their fields, ponds, reservoirs and routes. A temple community was a productive and institutional unit, not only a stone shrine. Local communities coordinated production, often under elite ownership, and contributed to state resources.' },
        { claim: 'published', text: 'They report two patterns. Larger communities had more land and reservoir capacity per person, which points to organisation above the household that raised the returns to farm labour. And land use changed with distance from the urban core, consistent with farmers taking transport costs into account. Their conclusion: Angkor’s farming was organised more like other urban production than like a scatter of independent smallholders.' },
        { claim: 'published', text: 'Table 4B traces the build-up of the complete-data sample: 93 inhabited communities in 770–906, then 192, 380, 511 and 568, reaching 571 in 1181–1308. These are period summaries of an archaeological sample, not censuses of the whole city.' },
      ],
      rule: [
        { claim: 'published', text: 'Community output follows Y = Y₀N^β with β = 1.227 (standard error 0.023). Settlement scaling theory predicts 7/6 ≈ 1.167. Constant productivity would be β = 1. The Atlas plots the per-person index 100 × (N/100)^(β−1).' },
        { claim: 'published', text: 'Separate distance relationships, normalised to 100 at 10 km from the Bayon: output per hectare falls with slope −0.846, reservoir volume per hectare with −0.409, and land per person rises with +0.521. Temple-platform volume has an elasticity of 0.085 with respect to the production index.' },
      ],
      result: [
        { claim: 'published', text: 'Because β exceeds 1, a community of 500 has a per-person index about 44% higher than one of 100 (5^0.227 ≈ 1.44). The paper puts the index of a 500-person temple community at 4.18 times that of a farmer working alone, “more than adequate to feed a growing population of non-food producers.”' },
        { claim: 'method', text: 'Try it below: move community size and compare the published exponent with the theoretical 7/6 and with constant returns.' },
      ],
      limitation: [
        { claim: 'open', text: 'The production index is the product of archaeological proxies for labour, land and irrigation water. It is not measured tonnes of rice. Because population is one of the three factors, β > 1 means larger communities were assigned more land and water per person; it is not a direct measure of output per farmer.' },
        { claim: 'open', text: 'The distance slopes are separate associations, not coefficients of one production function, and they explain only 2.6–5.1% of variance. The 0.085 temple elasticity is not a constant surplus share or tax rate.' },
        { claim: 'open', text: 'The paper leaves open who received the gains: coercive elite capture and more communal sharing could both produce these aggregate patterns. Using β as a year-by-year harvest multiplier, as some later chapters can, is our hypothesis, not the paper’s finding.' },
      ],
      maths: {
        plain: 'A scaling law says how a total grows with size. If β = 1, doubling a community doubles its output: output per person stays flat. If β > 1, output grows faster than population, so each person’s share of the index rises with community size.',
        formula: 'Y = Y₀ · N^β     per-person index = 100 × (N / 100)^(β − 1)',
        symbols: [['Y', 'production index of a community (proxy: labour × land × water)'], ['N', 'people in the community'], ['Y₀', 'a constant that sets the units'], ['β', 'scaling exponent; 1.227 ± 0.023 (Table 5)']],
        example: 'For N = 500: (500/100)^(1.227 − 1) = 5^0.227. ln 5 ≈ 1.609; × 0.227 ≈ 0.365; e^0.365 ≈ 1.44. So the index per person is 144 against 100 for a community of 100. With β = 7/6 it would be 5^(1/6) ≈ 1.31; with β = 1, exactly 1.',
      },
      sources: [
        { label: 'Klassen, Ortman, Lobo & Evans (2022), Journal of Archaeological Method and Theory 29: 763–794', href: KLASSEN },
        { label: 'Atlas notes on the paper and its boundaries', href: 'research/provisioning.html' },
        { label: 'Table 4B transcription (CSV)', href: 'research/provisioning-periods.csv' },
        { label: 'The paper (PDF)', href: 'research/provisioning-paper.pdf' },
      ],
      models: ['provisioning'],
    },
    {
      id: 'campaign', kicker: 'Chapter 2 · Atlas extension',
      title: 'Feeding the people who build and fight',
      question: 'What happens to the harvest when the court sends workers on campaign?',
      evidence: [
        { claim: 'published', text: 'Chapter 1 shows a landscape organised to deliver surplus to the core. Builders, soldiers and ritual specialists ate from that surplus. Rice and fish fed households; grain and working time also paid for campaigns, canals and construction.' },
      ],
      rule: [
        { claim: 'method', text: 'A seasonal model of an illustrative provisioning area. Rice, fish, farm work and construction compete across the seasons. A campaign takes workers away from farming and needs food on the road. The court collects its share after the village reserve.' },
      ],
      result: [
        { claim: 'sim', text: 'Across six scenarios with 32 matched seeds each, moving the frontier from 180 to 540 km adds 40 campaign days and creates overlap with the harvest in every modelled year.' },
      ],
      limitation: [
        { claim: 'open', text: 'Routes, transport performance and capture rates are illustrative. Stores have no physical cap, which can hide food pressure in the default setup. The grain totals are kept separate from the other experiments.' },
      ],
      maths: {
        plain: 'A first-principles check on scale: 1,000 km² of paddy at 1.5 tonnes per hectare, with 16% losses, yields about 126,000 tonnes. At 200 kg per person per year that is about 630,000 annual rations.',
        example: '1,000 km² = 100,000 ha. 100,000 × 1.5 t = 150,000 t. × (1 − 0.16) = 126,000 t. 126,000,000 kg ÷ 200 kg = 630,000 people. The area, yield and ration are illustrative inputs; fish, staggered harvests and imports change the budget.',
      },
      sources: [{ label: 'The three-experiment sequence', href: 'research/angkor-sequence.html' }],
      models: ['campaign'],
    },
    {
      id: 'growth', kicker: 'Chapter 3 · Atlas extension',
      title: 'Growth, waterworks and upkeep',
      question: 'Can production support a larger settlement over generations, and what does upkeep cost?',
      evidence: [
        { claim: 'published', text: 'Angkor’s reservoirs and canals were central to its farming, and they needed continuing work. Chapter 1’s distance pattern in reservoir volume is one trace of that investment.' },
      ],
      rule: [
        { claim: 'method', text: 'A long-run water-and-rice model follows a synthetic regional population. Harvests depend on yield and the condition of the waterworks; population responds to harvests. Maintenance intensity and dependence on waterworks are the levers.' },
      ],
      result: [
        { claim: 'sim', text: 'In the separate maintenance experiment, cutting upkeep to 35% of its reference level from year 55 leaves a median of 6,209 state-linked people under drought, against 6,958 in the stable reference.' },
      ],
      limitation: [
        { claim: 'open', text: 'The geography and population are synthetic. The older growth engine has no annual grain ledger, and its military and monument spending can exceed its budget. Use it to inspect the growth rules, not as a reconstruction.' },
      ],
      sources: [{ label: 'Angkor model review: before and after', href: 'https://github.com/TreyModels/atlas-of-education/blob/main/experiments/angkor-review/README.md' }],
      models: ['angkor', 'maintenance'],
    },
    {
      id: 'signalling', kicker: 'Chapter 4 · Atlas extension',
      title: 'Turning stone into authority',
      question: 'What does visible construction tell a tributary deciding whether to pay?',
      evidence: [
        { claim: 'published', text: 'Chapter 1’s temple elasticity links monument volume to production. Monuments were also political statements, legible to neighbours and suppliers.' },
      ],
      rule: [
        { claim: 'method', text: 'A successor court inherits monuments and elephants. A supplier decides whether to pledge tribute. In one world it judges readiness from the visible display; in a paired world it can see the defence the court can actually provision. Both worlds face identical harvests and frontier challenges.' },
      ],
      result: [
        { claim: 'sim', text: 'With the default mixed display, suppliers pledge during failed defence for 7.28 of 12 years on average (32 paired seeds). Lowering trust in the display to 80% cuts that to 2.34 years. Tribute paid on a false signal can then build real capacity.' },
      ],
      limitation: [
        { claim: 'open', text: 'The magnitudes follow from the belief rule, which is assumed. The numerical relationships have not been established historically.' },
      ],
      sources: [{ label: 'Signalling experiment and results', href: 'research/signalling.html' }],
      models: ['signalling'],
    },
    {
      id: 'obligations', kicker: 'Chapter 5 · Atlas extension',
      title: 'Can the court afford to stay, leave or come back?',
      question: 'Who pays when the court leaves, and what brings it back?',
      evidence: [
        { claim: 'published', text: 'Victor Lieberman calls Angkor a “charter state”: an early polity whose political template outlasted it. Courts moved; farming landscapes often stayed.' },
      ],
      rule: [
        { claim: 'method', text: 'Local food and pledged outside deliveries must cover ritual and court bills. Two consecutive unpaid court bills trigger departure, by assumption. A separate rule allows a funded return. Pledges come from the signalling model with the same seeds; the food ledgers stay separate to avoid double counting.' },
      ],
      result: [
        { claim: 'sim', text: 'With the same interruption, 21 of 32 courts leave. Allowing a funded return brings all 21 back.' },
        { claim: 'sim', text: 'In the separate two-centre relocation experiment, an earlier result had the court leave in every drought run. That depended on the coordination multiplier from Chapter 1 applied as a causal boost. With the multiplier off by default, the court left in none of the 32 default drought runs.' },
      ],
      limitation: [
        { claim: 'open', text: 'The exit threshold is an assumption. The relocation result shows how much one borrowed coefficient can carry: a size association used as a causal effect decided the outcome.' },
      ],
      sources: [{ label: 'Relocation experiment and the multiplier finding', href: 'research/relocation.html' }],
      models: ['obligations', 'relocation'],
    },
    {
      id: 'climate', kicker: 'Chapter 6 · Atlas extension',
      title: 'Applying the documented climate',
      question: 'What changes when the reconstructed drought record is applied?',
      evidence: [
        { claim: 'published', text: 'Lieberman and Buckley (2012) connect monsoon variation to the rise and fragmentation of mainland Southeast Asian kingdoms. Buckley and colleagues (2010) reconstructed annual drought from tree rings, including severe droughts in the 14th and early 15th centuries.' },
      ],
      rule: [
        { claim: 'method', text: 'From 1250 to 1450 the long-run engine uses the reconstructed March–May drought index (PDSI). We translate it into a crop factor: clamp(1 + response × PDSI, 0.4, 1.15). Three response values test how much the result depends on that translation. The same society with neutral climate is the comparison.' },
      ],
      result: [
        { claim: 'sim', text: 'This is the clearest decline result in the Atlas. With neutral climate after 1250, none of 2,000 matched parameter draws declines. With the reconstructed drought record applied to the same societies, 217, 1,260 or 1,657 of 2,000 decline, depending on the crop response (0.04, 0.07 or 0.10 per index unit), with median onsets of 1402, 1362 and 1338.' },
        { claim: 'sim', text: 'So the documented droughts are enough to produce decline in this society model, and the timing falls in the late 14th century. How often and how early depends on a crop response nobody has measured. At the middle response, the median core-activity index in 1450 is 89.4, against 100 in 1300: a sustained fall, not a collapse.' },
      ],
      limitation: [
        { claim: 'open', text: 'A literature search (November 2026) found no published rice-yield response per PDSI unit for mainland Southeast Asia. The reconstruction reaches −7.2 in 1403, far outside the modern instrumental range, so any modern yield response is an extrapolation. Weather before 1250 is synthetic.' },
      ],
      maths: {
        plain: 'The crop factor multiplies the harvest. A drought index of −2 with a response of 0.05 gives 1 + 0.05 × (−2) = 0.9: a 10% shortfall. The clamp stops the factor going below 0.4 or above 1.15.',
        formula: 'crop factor = clamp(1 + r × PDSI, 0.4, 1.15)',
        symbols: [['PDSI', 'Palmer Drought Severity Index; negative is dry'], ['r', 'assumed crop response per index unit (three values tested)']],
        example: 'In 1403, PDSI = −7.2. With r = 0.05: 1 − 0.36 = 0.64. With r = 0.1: 1 − 0.72 = 0.28, clamped to 0.4. The choice of r, which no source pins down, decides how hard that year bites.',
      },
      sources: [
        { label: 'Monsoon account and results', href: 'research/monsoon.html' },
        { label: 'Lieberman (2011), Charter State Collapse in Southeast Asia', href: 'https://doi.org/10.1086/ahr.116.4.937' },
      ],
      models: ['monsoon'],
    },
  ],
  deeper: ['petri', 'institutions', 'flight', 'accounts', 'mandala'],
  models: {
    provisioning: { id: 'provisioning', title: 'Temple communities and provisioning', purpose: 'published', state: 'checked', note: 'Reproduces the paper’s scaling and distance relationships as normalised indices. No re-estimation from the archaeological records.', engine: 'engines/provisioning.js', route: 'provisioning', research: 'research/provisioning.html' },
    campaign: { id: 'campaign', title: 'Seasonal campaign logistics', purpose: 'mechanism', state: 'developing', note: 'Illustrative routes and transport rates; stores are uncapped, which can hide food pressure.', engine: 'engines/campaign.js', route: 'campaign' },
    angkor: { id: 'angkor', title: 'Water, rice and growth', purpose: 'mechanism', state: 'developing', note: 'Older engine: no annual grain ledger; military and monument spending can exceed budget.', engine: 'reference/angkor/model.js', route: 'angkor' },
    signalling: { id: 'signalling', title: 'Monument signalling and tribute', purpose: 'mechanism', state: 'checked', note: 'Paired worlds with identical shocks. Magnitudes follow from an assumed belief rule.', engine: 'engines/signalling.js', route: 'signalling', research: 'research/signalling.html' },
    obligations: { id: 'obligations', title: 'Court obligations, exit and return', purpose: 'mechanism', state: 'checked', note: 'Linked to signalling by seed; separate food ledgers. Exit threshold assumed.', engine: 'engines/obligations.js', route: 'obligations' },
    monsoon: { id: 'monsoon', title: 'Monsoon and state growth', purpose: 'mechanism', state: 'developing', note: 'Real drought record; the crop response to it is unsourced and tested at three values.', engine: 'engines/monsoon.js', route: 'monsoon', research: 'research/monsoon.html' },
    petri: { id: 'petri', title: 'Dynamic temple economy (Petri lab)', purpose: 'mechanism', state: 'checked', note: 'Every annual grain ledger balances. Results before the November 2026 review used a coordination multiplier and water floor now off by default; those are kept as a historical run.', engine: 'engines/petri.js', route: 'petri', research: 'research/provisioning.html' },
    relocation: { id: 'relocation', title: 'Two-centre elite relocation', purpose: 'mechanism', state: 'checked', note: 'The court’s departure depended on a borrowed multiplier; with it off, no default drought run exits.', engine: 'engines/relocation.js', route: 'relocation', research: 'research/relocation.html' },
    maintenance: { id: 'maintenance', title: 'Canal maintenance', purpose: 'accounting', state: 'checked', note: 'Maintenance-only and reshuffle cases separated after review; harvest still ignores remaining farm workforce.', engine: 'engines/lab_models.js', route: 'maintenance' },
    institutions: { id: 'institutions', title: 'Shares of the harvest', purpose: 'teaching', state: 'developing', note: 'One trial per scenario; land rights recorded without changing harvest.', engine: 'engines/lab_models.js', route: 'institutions' },
    flight: { id: 'flight', title: 'Flight to a refuge', purpose: 'teaching', state: 'developing', note: 'People move to a refuge rather than vanishing; refuge food production not tracked in this version.', engine: 'engines/lab_models.js', route: 'flight' },
    accounts: { id: 'accounts', title: 'Balanced food and labour accounts', purpose: 'accounting', state: 'checked', note: 'Every year balances food, labour and population. Rates hypothetical; no battles.', engine: 'engines/lab_models.js', route: 'accounts' },
    mandala: { id: 'mandala', title: 'Mandala spatial lab (stored runs)', purpose: 'mechanism', state: 'historical', note: 'The reference run fails to make Angkor the leading centre and overshoots population. Kept for diagnosis.', route: 'mandala' },
  },
  bottomLine: 'The published study tells us how Angkor’s food economy was organised. Our experiments ask what would follow if those relationships and our added rules held. In the reviewed runs, climate shifts the timing, distance strains the army, and belief decides whether the centre holds. And one borrowed coefficient, used as a cause, was enough to decide whether a court left. The models test assumptions. They do not deliver a verdict on Angkor’s decline.',
}
