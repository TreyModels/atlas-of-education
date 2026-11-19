// CCP bus journey: the narrated family page for the politics family.
// Content only. Presentation lives in src/components/AngkorJourney.tsx (reused unchanged).
// Every number here is copied from a stored Atlas result or the briefing; the check
// script guards structure, labels and links. All agents are synthetic.

import type { Journey, ModelCard } from './angkor-journey'

const REPO = 'https://github.com/TreyModels/atlas-of-education'
const COMMIT = '2e19f07'
const MODELS = `${REPO}/blob/${COMMIT}/experiments/ccp-bus/models`
const BRIEFING = `${REPO}/blob/${COMMIT}/experiments/ccp-bus/BRIEFING.md`

const V1_RESULTS = `${REPO}/tree/${COMMIT}/experiments/ccp-bus/models/A_claude_v1_three_models`
const V3_RESULTS = `${MODELS}/B_claude_v3_economy_factions/README.md`
const V6_RESULTS = `${MODELS}/C_chatgpt_v6_tilly/RESULTS.md`
const V7_RESULTS = `${MODELS}/D_chatgpt_v7_identification/RESULTS.md`

const V1_ZIP = 'research/ccp-bus/ccp-bus-v1.zip'
const V3_ZIP = 'research/ccp-bus/ccp-bus-v3.zip'
const V6_ZIP = 'research/ccp-bus/ccp-bus-v6.zip'
const V7_ZIP = 'research/ccp-bus/ccp-bus-v7.zip'

const models: Record<string, ModelCard> = {
  'ccp-v1': {
    id: 'ccp-v1',
    title: 'CCP bus · Rival mechanisms',
    purpose: 'mechanism',
    state: 'checked',
    note: 'Three small rival families (current incentives, social trap, bus) set to the same 30% snapshot. Only models with complementarities show hysteresis; the memoryless model never kept a campaign effect (0 of 96 runs).',
    engine: V1_ZIP,
    research: V1_RESULTS,
  },
  'ccp-v3': {
    id: 'ccp-v3',
    title: 'CCP bus · Economy and factions',
    purpose: 'mechanism',
    state: 'developing',
    note: 'Adds land revenue, credit, PLA procurement, four sectors and faction dynamics. Pattern-oriented ABC against CCDI cases plus six qualitative patterns; 17 accepted fits. Not tested out of sample.',
    engine: V3_ZIP,
    research: V3_RESULTS,
  },
  'ccp-v6': {
    id: 'ccp-v6',
    title: 'CCP bus · Tilly mechanisms',
    purpose: 'mechanism',
    state: 'developing',
    note: '50,000 agents, 64 organisations, 5 ranks, Tilly-labelled mechanisms. Well engineered (14 passing checks, exact accounting) but uncalibrated: 42 hand-set parameters, several mechanisms inert, little memory.',
    engine: V6_ZIP,
    research: V6_RESULTS,
  },
  'ccp-v7': {
    id: 'ccp-v7',
    title: 'CCP bus · Identification comparison',
    purpose: 'mechanism',
    state: 'evaluated',
    note: 'The three rival families on the v6 kernel, fitted to 2013–19 filings and scored on 2020–25. Retrospective: outcomes were known when the exercise was designed. Bus and social trap are indistinguishable on case counts.',
    engine: V7_ZIP,
    research: V7_RESULTS,
  },
}

export const ccpJourney: Journey = {
  kicker: 'Political systems · CCP bus',
  title: 'Does a sponsored entry route keep corruption going after a campaign?',
  lede: 'This project’s user manuscript, The Priest and the Bandit, argues that Chinese Communist Party (CCP) corruption is the payroll of a clergy, not deviance: entry by sponsorship creates obligations and shared exposure that keep corruption going after enforcement changes. The manuscript is not peer reviewed, and nothing here treats its claims as established fact. In modelling terms, the claim is path dependence. This page follows four stored model versions that ask whether that claim can be told apart from simpler mechanisms in the data we have. All agents are synthetic.',
  repo: REPO,
  family: 'politics',
  why: [
    { text: 'If this year’s incentives fully determine this year’s corruption, then a campaign that changes incentives should change corruption, and history should not matter. If entry is sponsored, and sponsors and clients share exposure, then inherited networks can keep corruption high, or bring it back, after a campaign. The two views make different predictions about what happens after enforcement changes.' },
    { claim: 'method', text: 'We follow a modular “model of models” design (Page, The Model Thinker): a broad framework whose pieces switch on and off, each tested against the pattern it bears on. Each added mechanism must earn its place against a pattern in data (Grimm et al. 2005, pattern-oriented modelling).' },
    { claim: 'open', text: 'The user manuscript The Priest and the Bandit is the source of the hypothesis. It is not peer reviewed. Nothing on this page treats its claims as established fact, and nothing here estimates the actual prevalence of corruption in China, identifies any real official as corrupt, or describes anyone’s personal motives.' },
  ],
  chapters: [
    {
      id: 'hypothesis',
      kicker: 'Chapter 1 · The hypothesis and the filings',
      title: 'Path dependence, and what the data can see',
      question: 'If sponsored entry keeps corruption going after a campaign, what should we see, and what do the filings actually record?',
      evidence: [
        { claim: 'data', text: 'The observable outcome is disciplinary cases filed by the Central Commission for Discipline Inspection (CCDI), reported annually. Cases are not corruption prevalence: they mix detection, reporting, enforcement capacity and the underlying behaviour. The v7 training window is 2013–2019; the evaluation window is 2020–2025.' },
        { claim: 'data', text: 'Annual cases filed (thousands): 618 in 2020, 631 in 2021, 596 in 2022, 626 in 2023, 877 in 2024, 1,012 in 2025. The 2024–25 surge is the pattern any mechanism has to explain.' },
        { claim: 'method', text: 'The 2019 land figure was published in May 2020, so the information cutoff for the v7 exercise is 24 May 2020. The 2020–25 outcomes were already known when the exercise was designed; this is a retrospective holdout, not an untouched forecast.' },
      ],
      rule: [
        { claim: 'method', text: 'The hypothesis is stated as a mechanism: entry by sponsorship selects pliable clients and wires them into a sponsor’s circle; shared exposure keeps the network together after enforcement changes. The rival view is that current incentives alone determine current behaviour, so history cannot matter in the long run.' },
        { claim: 'method', text: 'The models are synthetic. Agents are not real officials. The models do not claim that any real person was corrupt, was selected personally, or had any particular motive.' },
      ],
      result: [
        { claim: 'open', text: 'The hypothesis is testable in principle. Whether the available data can distinguish it from simpler mechanisms is the question the four model versions address.' },
      ],
      limitation: [
        { claim: 'open', text: 'National case counts are a coarse outcome. They cannot separate detection from behaviour, and seven annual training points cannot identify many behavioural parameters.' },
      ],
      sources: [
        { label: 'Briefing for review (19 November 2026)', href: BRIEFING },
        { label: 'v7 results and holdout scores', href: V7_RESULTS },
      ],
      models: [],
    },
    {
      id: 'v1',
      kicker: 'Chapter 2 · v1 rival mechanisms',
      title: 'Three small families on the same snapshot',
      question: 'Can a memoryless model ever keep a campaign effect?',
      evidence: [
        { claim: 'method', text: 'v1 sets three small rival families to the same 30% corruption snapshot: current incentives (principal–agent, Markov), social trap (peer norms, detection that depends on honest peers, finite enforcement capacity), and bus (social trap plus sponsored entry and threat-driven rewiring).' },
      ],
      rule: [
        { claim: 'method', text: 'Current incentives: an official’s choice depends only on current deterrence. Social trap: strategic complementarities can produce multiple equilibria and hysteresis. Bus: adds sponsored entry that selects pliable clients and wires them into the sponsor’s circle, plus rewiring of corrupt officials toward each other.' },
      ],
      result: [
        { claim: 'sim', text: 'Only models with complementarities (finite investigators, peer reporting) show hysteresis. The memoryless model never kept a campaign effect: 0 of 96 runs.' },
      ],
      limitation: [
        { claim: 'open', text: 'v1 is a small mechanism demonstration, not a calibrated model of China. The parameters are hypotheses to be estimated, not facts.' },
      ],
      sources: [
        { label: 'v1 model source and experiments', href: V1_RESULTS },
        { label: 'v1 code (zip)', href: V1_ZIP },
      ],
      models: ['ccp-v1'],
    },
    {
      id: 'v3',
      kicker: 'Chapter 3 · v3 economy and factions',
      title: 'Adding land, credit and factions',
      question: 'Does a richer political economy change what the bus predicts?',
      evidence: [
        { claim: 'method', text: 'v3 adds land revenue, credit, PLA procurement, four sectors and faction dynamics: patron protection, encirclement, hiding, bandwagoning and succession.' },
      ],
      rule: [
        { claim: 'method', text: 'Pattern-oriented approximate Bayesian computation (ABC) against CCDI cases plus six qualitative patterns. The model is fitted to the patterns it is asked to reproduce.' },
      ],
      result: [
        { claim: 'sim', text: '17 accepted fits. Within the simulation, modeled faction status predicts simulated removal about as well as modeled corruption (AUC 0.67 vs 0.66). This is a within-simulation discrimination, not an empirical finding about real officials.' },
      ],
      limitation: [
        { claim: 'open', text: 'The 17 accepted fits are exploratory and fitted. They are not tested out of sample. The AUC comparison is a fitted association, not a causal claim about faction or corruption.' },
      ],
      sources: [
        { label: 'v3 README', href: V3_RESULTS },
        { label: 'v3 code (zip)', href: V3_ZIP },
      ],
      models: ['ccp-v3'],
    },
    {
      id: 'v6',
      kicker: 'Chapter 4 · v6 institutional kernel',
      title: 'A larger kernel, uncalibrated',
      question: 'What does a large Tilly-style kernel add, and what does it not yet show?',
      evidence: [
        { claim: 'method', text: 'v6 is a 50,000-agent, 64-organisation, 5-rank kernel with Tilly-labelled mechanisms. It is the shared kernel on which v7 compares the three rival families.' },
      ],
      rule: [
        { claim: 'method', text: 'The kernel is engineered for accounting and personnel identity. Mechanisms are labelled with Tilly’s vocabulary so that each can be switched on and off.' },
      ],
      result: [
        { claim: 'method', text: 'Well engineered: 14 passing checks and exact accounting. These checks are implementation verification, not a scientific result. Uncalibrated: 42 hand-set parameters, several mechanisms inert, little memory.' },
      ],
      limitation: [
        { claim: 'open', text: 'v6 is illustrative and uncalibrated. Its outputs are not evidence about China; they are a platform for the v7 comparison.' },
      ],
      sources: [
        { label: 'v6 results', href: V6_RESULTS },
        { label: 'v6 code (zip)', href: V6_ZIP },
      ],
      models: ['ccp-v6'],
    },
    {
      id: 'v7',
      kicker: 'Chapter 5 · v7 retrospective comparison',
      title: 'Three families on a common kernel',
      question: 'On a common kernel, can the bus be told apart from simpler mechanisms?',
      evidence: [
        { claim: 'method', text: 'v7 compares the three rival families (current incentives, social trap, bus) on the v6 kernel. It is not a comparison across version numbers. Fitted on 2013–2019 filings; scored on 2020–2025. The outcome is disciplinary cases, not corruption prevalence.' },
        { claim: 'method', text: 'Strict forecasts hold land receipts at their 2019 level. Conditional hindcasts use realized land receipts. The 2019 land figure was published in May 2020, so the information cutoff is 24 May 2020.' },
      ],
      rule: [
        { claim: 'method', text: 'A shared case scale is profiled separately for each fit. The 64-draw search and three families generated 192 candidate evaluations, each with two screening seeds; the best four per family were re-ranked with eight independent training seeds. Five parameter dimensions were sampled, with peer gain and reporting capture inactive in the current-incentives family.' },
      ],
      result: [
        { claim: 'sim', text: 'Log RMSE at 50,000 agents, strict: current incentives 0.195, social trap 0.190, bus 0.190. Bus and social trap are indistinguishable (0.1898 vs 0.1896). At the fitted settings the extra bus mechanisms do nothing for case counts.' },
        { claim: 'sim', text: 'All three miss the 2024–25 surge. They beat a last-value forecast on log RMSE (0.19 vs 0.25) mainly because last-value misses the surge by even more. On absolute error, last-value MAE is 115,667 against bus 118,066: there is no universal benchmark win.' },
        { claim: 'sim', text: 'Memory test: four matched seeds per family began at 5% and 95% misconduct with identical external conditions. The fitted social and bus families show a large initial response (bus +0.8332 at step 1) followed by rapid convergence (≈0 by step 10). This is a state-initialization test only; head replacement and full network reset were not run.' },
      ],
      limitation: [
        { claim: 'open', text: 'Retrospective: the 2020–25 outcomes were already known when the exercise was designed. An independent future period or organisational holdout is needed for an untouched test. The six yearly errors are highly correlated and too few for a reliable model ranking.' },
        { claim: 'open', text: 'These fits leave parameters weakly constrained; seven annual training targets provide little leverage for discriminating these mechanisms. Fitted values swing widely (rent −0.67 to 0.84, peer effect 0.17 to 4.0) with near-identical fit. The fitted case scale is an unknown observation coefficient; these are simulated minimum-distance fits, not posterior estimates.' },
        { claim: 'open', text: 'The memory test does not establish that other parameter regions or interventions lack memory. The replacement and full-reset tests described in the spec remain outstanding.' },
        { claim: 'open', text: 'Room for improvement: compare provincial land receipts and fines/fees, add organisational or faction evidence, and run head-replacement and full-reset experiments. A future forecast must state its information cutoff and score only outcomes not already seen. These proposed checks are not completed findings.' },
      ],
      maths: {
        plain: 'Log RMSE compares forecasts with observations on a log scale, so a miss on a small number counts as much as the same proportional miss on a large one. It is the square root of the mean squared difference between the log of the forecast and the log of the observation.',
        formula: 'logRMSE = sqrt( (1/n) · Σ (ln ŷₜ − ln yₜ)² )',
        symbols: [['n', 'number of forecast years (6 in v7)'], ['ŷₜ', 'forecast cases filed in year t'], ['yₜ', 'observed cases filed in year t'], ['ln', 'natural logarithm']],
        example: 'A forecast of 700 against an observation of 1,000 gives ln 700 − ln 1,000 ≈ −0.357; squared ≈ 0.127. Averaging over years and taking the square root gives the reported log RMSE.',
      },
      sources: [
        { label: 'v7 results and holdout scores', href: V7_RESULTS },
        { label: 'v7 code (zip)', href: V7_ZIP },
        { label: 'Briefing for review', href: BRIEFING },
      ],
      models: ['ccp-v7'],
    },
  ],
  deeper: [],
  models,
  bottomLine: 'On national case counts, the bus cannot yet be told apart from simpler mechanisms. Bus and social trap are indistinguishable (log RMSE 0.1898 vs 0.1896), all three families miss the 2024–25 surge, and the memory test finds no lasting memory at the fitted settings. The bus is a coherent, testable theory instrument, not yet evidence for itself. All agents are synthetic. Nothing here estimates the actual prevalence of corruption in China, identifies any real official as corrupt, or describes anyone’s personal motives.',
}

export default ccpJourney
