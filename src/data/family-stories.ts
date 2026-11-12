import type { ModelFamily } from './model-catalogue'

// Evidence labels follow the fertility-research convention:
// [data] measured from real data · [sim] produced by a simulation ·
// [ruled out] a claim we tested and rejected · [open] still unsettled · [method] a computational tool.
export type ClaimTag = 'data' | 'sim' | 'ruled-out' | 'open' | 'method'
export type StoryBlock =
  | { kind: 'para'; tag?: ClaimTag; text: string }
  | { kind: 'list'; tag?: ClaimTag; items: string[] }
  | { kind: 'table'; tag?: ClaimTag; caption?: string; head: string[]; rows: string[][] }
export type StorySection = { heading: string; blocks: StoryBlock[] }
export type FamilyStory = {
  kicker: string
  title: string
  lede: string
  sections: StorySection[]
  bottomLine?: string
  cta?: { label: string; route: string }
}

export const familyStories: Record<ModelFamily, FamilyStory> = {
  fertility: {
    kicker: 'What our models support',
    title: 'Why fertility fell, and what can still move it',
    lede: 'The full story the fertility models support, each part labelled by the kind of evidence behind it.',
    sections: [
      {
        heading: 'Survival sets the floor',
        blocks: [
          { kind: 'para', tag: 'data', text: 'When children survive and people live long lives, large families stop being necessary. Life expectancy alone predicts each country’s decline down to about 1.3–1.5 children per woman.' },
          { kind: 'para', tag: 'data', text: 'Income is the wrong yardstick. Our six places reached replacement at incomes 16 times apart ($990 to $16,000), but all at life expectancies of 67–75 years. The fertility-to-income curve shifted over time; the fertility-to-survival curve held steady.' },
        ],
      },
      {
        heading: 'Education turns children and marriage into credential contests',
        blocks: [
          { kind: 'para', tag: 'sim', text: 'Children cost more. Each child needs heavy investment to compete, lowering births everywhere by roughly 0.4 children, mostly second births.' },
          { kind: 'para', tag: 'sim', text: 'The marriage market jams. In Korea, the “credential floor plus women marrying up” combination was the only one that reproduced all five Korean facts — unmarried educated women alongside unmarried less-educated men.' },
          { kind: 'para', tag: 'sim', text: 'Marriage gets later. Years establishing a career, housing costs and slower job prospects for men together reproduce China’s 4.7-year rise in women’s marriage age.' },
          { kind: 'para', tag: 'sim', text: 'The jam matters only where births need marriage. It is large in East Asia and shrinks by about 70% where births outside marriage are common, as in the Philippines.' },
        ],
      },
      {
        heading: 'Late marriage meets the biological clock',
        blocks: [
          { kind: 'para', tag: 'sim', text: 'Every year of delay costs more than the last, and the cost gets steep after 33–35. The curve is calibrated to medical fecundity data.' },
          { kind: 'table', tag: 'sim', caption: 'Share of the fertility fall explained by late marriage', head: ['Place', 'Share explained'], rows: [
            ['Hong Kong', '26%'], ['Korea', '21%'], ['China', '18%'], ['Thailand, Philippines', '1–2% (still marrying in their mid-20s)'],
          ] },
          { kind: 'para', tag: 'sim', text: 'IVF recovers only about a sixth of this loss — validated against Korea’s 15% of births from fertility treatment.' },
        ],
      },
      {
        heading: 'A shared shock after 2015',
        blocks: [
          { kind: 'list', tag: 'data', items: [
            'All six places fell below their development path at once, by about 0.46 children on average — 0.71 against their own earlier, recovering trends.',
            'The drop was the same whether or not births require marriage, so it is not the marriage jam. It cut births across the board.',
            'Nothing in pre-2015 trends predicted it. Models trained up to 2014 forecast 1.86 for China in 2024; the actual figure was 1.01.',
          ] },
          { kind: 'para', tag: 'ruled-out', text: 'Country-to-country spread is ruled out; microplastics are ruled out as the main cause — the pattern is wrong. The cause is still open: smartphones, COVID and economic shocks all fit the timing.' },
        ],
      },
      {
        heading: 'Can it bounce back?',
        blocks: [
          { kind: 'para', tag: 'sim', text: 'In uniform, peer-driven societies a temporary shock can tip fertility into a lasting low. Reversing it then costs about 8 times what preventing it would have.' },
          { kind: 'para', tag: 'data', text: 'Japan and Hong Kong show a pull back toward their path; Japan recovered from 1.26 to 1.45. Korea and China show none. The data did not confirm a clean tipping cliff, though.' },
        ],
      },
      {
        heading: 'What policy can do',
        blocks: [
          { kind: 'table', tag: 'sim', caption: 'Simulated effect on births per woman', head: ['Policy', 'Effect'], rows: [
            ['Accepting births outside marriage', '+0.37 children'],
            ['More people marrying (+10 points)', '+0.12'],
            ['Support for second births', '+0.13'],
            ['Marrying 2 years earlier', '+0.04'],
            ['IVF for everyone who needs it', '+0.02'],
            ['Cash (+30%)', '+0.08'],
            ['Best four combined', '+0.35'],
          ] },
          { kind: 'para', tag: 'sim', text: 'Even the combined package leaves Korea far below replacement.' },
        ],
      },
      {
        heading: 'Ruled out along the way',
        blocks: [
          { kind: 'list', tag: 'ruled-out', items: [
            'A 15–20 year lag from education to fertility (the effect is immediate)',
            'An age-29 trap below 1.3 (Japan is a counterexample)',
            'National enrolment ratios as evidence for the marriage jam (failed the placebo test)',
            'Competition within marriage as the main driver in Korea',
            'Educated Chinese women wanting fewer children (surveys show about 1.7, the same as others)',
            'Diet and stress as a major factor',
          ] },
        ],
      },
    ],
    bottomLine: 'Survival brings every society down to about 1.4. Mass education then turns children into expensive projects and marriage into a credential match. Where births need marriage, that jams the marriage market and pushes weddings into the 30s, where the biological clock turns delay into permanent loss. Since 2015, a still-unexplained shock has pushed every country lower at once. Money alone can’t fix it; what helps most is decoupling births from marriage, helping people marry, and supporting second children — ideally before the fall rather than after.',
  },

  education: {
    kicker: 'What our models support',
    title: 'Who stays in school, and what the diploma is worth',
    lede: 'Household choices, graduate queues and credential dynamics — behaviour is modelled, not treated as an accounting identity.',
    sections: [
      {
        heading: 'What keeps students in school',
        blocks: [
          { kind: 'para', tag: 'sim', text: 'Human-capital, positional and relational bundles were each drawn 24,000 times against country targets. Where a wealth gradient exists, adding the relational floor sharply narrows which parameter draws fit.' },
          { kind: 'para', tag: 'open', text: 'Cambodia and China lack wealth gradients in this comparison, so acceptance rates cannot rank the theories across countries.' },
        ],
      },
      {
        heading: 'The graduate queue',
        blocks: [
          { kind: 'para', tag: 'data', text: 'The fitted labour-market model reproduces the supplied NBS graduate series, and the app compares model and record directly. An earlier 2018–22 fit missed the later unemployment bulge.' },
          { kind: 'para', tag: 'open', text: 'Matching the displayed record leaves the mechanisms open. The reporting definition changes in 2024, and several labour-market responses remain assumptions.' },
        ],
      },
      {
        heading: 'School versus child labour',
        blocks: [
          { kind: 'para', tag: 'sim', text: 'In the Cambodia household simulation, policy and reference runs share matched seeds across 12 simulated years, so the interface exposes the difference each policy makes.' },
          { kind: 'para', tag: 'ruled-out', text: 'Causal policy effects are not yet established: programme effect sizes are stylised, and the rural school-retention fit needs a large unexplained adjustment.' },
        ],
      },
    ],
    bottomLine: 'Credentials are positional as much as productive. When everyone invests more, the queue lengthens rather than the payoff rising — which is why the same models feed the fertility story.',
  },

  systems: {
    kicker: 'What our models support',
    title: 'What happens when a cohort moves through the system',
    lede: 'Country cases, synthetic cities and East Asian forecasts follow pupils, teachers, classrooms and budgets through demographic change.',
    sections: [
      {
        heading: 'Demography drives everything',
        blocks: [
          { kind: 'para', tag: 'data', text: 'The East Asian dashboards index observed births — Hong Kong’s 2025 count of about 31,100 is the 100 baseline — and follow the shrinking cohort into classrooms, teacher demand and budgets.' },
          { kind: 'para', tag: 'sim', text: 'In the toy worlds, births growing 3% a year (Riverton) or falling 4% a year (Stillwater) let you watch the wave move through the system and see when spare capacity appears.' },
        ],
      },
      {
        heading: 'Teacher supply responds with a lag',
        blocks: [
          { kind: 'para', tag: 'sim', text: 'An age-structured accounting model follows intake, graduation, hiring and retirement through 2050. A lag between training decisions and hiring changes the projected gap — training pipelines cannot turn on a dime.' },
          { kind: 'para', tag: 'ruled-out', text: 'This is not a country forecast: starting counts and completion rates are synthetic, and the demonstration carries no prediction for any real system.' },
        ],
      },
      {
        heading: 'Policy shocks travel for years',
        blocks: [
          { kind: 'para', tag: 'sim', text: 'Free primary education during a hiring freeze (Kenya), a K-to-12 expansion (Philippines) and a post-conflict birth boom (Cambodia) each show how a single policy or demographic shock keeps moving through classrooms long after it lands.' },
        ],
      },
    ],
    bottomLine: 'A school system is a pipeline with memory: you cannot hire teachers you did not train, or fill classrooms for children who were never born.',
  },

  planning: {
    kicker: 'How the toolkit works',
    title: 'The planner’s arithmetic, showing its work',
    lede: 'Twelve independent implementations in the IIEP, UIS and education-sector-analysis tradition. Methodological tools, not official UNESCO software.',
    sections: [
      {
        heading: 'Indicators from raw counts',
        blocks: [
          { kind: 'para', tag: 'method', text: 'The indicator calculator derives GER, NER, GIR, adjusted gender parity and teacher ratios from raw enrolment and population counts, using the standard definitions.' },
          { kind: 'para', tag: 'method', text: 'Cohort-component projection shows who will be of school age and when; the flows model tracks promotion, repetition and dropout through the grades.' },
        ],
      },
      {
        heading: 'Money and equity',
        blocks: [
          { kind: 'para', tag: 'method', text: 'Benefit-incidence analysis traces public education resources across a cohort with a Lorenz curve; the grant-formula tool combines per-pupil, poverty and remoteness weights and shows the allocation per child.' },
          { kind: 'para', tag: 'data', text: 'The deployment tool applies the education-sector-analysis R² diagnostic to test whether teacher allocations actually follow pupils.' },
        ],
      },
      {
        heading: 'Targets, honestly checked',
        blocks: [
          { kind: 'para', tag: 'sim', text: 'The logistic tool compares the S-curve speed a coverage target requires with the speeds countries have historically achieved — a feasibility check, not a forecast.' },
          { kind: 'para', tag: 'open', text: 'These tools compute; they do not judge. The values they return are only as good as the counts and assumptions fed into them.' },
        ],
      },
    ],
  },

  shadow: {
    kicker: 'What our models support',
    title: 'Why do pupils pay their own teachers?',
    lede: 'In Cambodia, about four in five secondary pupils buy private tutoring, and most of it comes from their own teachers. An agent-based model of 72 teachers and 1,260 pupils tests three rival explanations against seven published patterns.',
    sections: [
      {
        heading: 'Three rival explanations, one calibration',
        blocks: [
          { kind: 'para', tag: 'sim', text: 'The thin timetable (the curriculum does not fit the official hours), diversion (teachers hold content back for paid sessions) and favour (paying buys goodwill) each fit the seven published patterns about equally well after ABC-SMC calibration. The data cannot tell them apart.' },
          { kind: 'para', tag: 'sim', text: 'But all three agree on what policies would do — and that agreement, not the verdict between theories, is the useful result.' },
        ],
      },
      {
        heading: 'What the calibrated worlds say',
        blocks: [
          { kind: 'para', tag: 'sim', text: 'Even under the diversion explanation, calibrated teachers withhold almost nothing — median 0% of content held back.' },
          { kind: 'para', tag: 'open', text: 'The evidence ratios are too sparse to rank the explanations, and only 11–18% of calibrated settings still fit in fresh random school systems. Treat the policy effects as model-conditional, not as evidence of real-world effects.' },
        ],
      },
      {
        heading: 'Who leaves school: the credential-floor test',
        blocks: [
          { kind: 'para', tag: 'data', text: 'A separate model offers three explanations for who leaves secondary school, each predicting a different share of leavers from the poorest 40% of households. The Cambodia DHS 2021–22 (Table 2.12) puts that share at 47–58%.' },
          { kind: 'para', tag: 'open', text: 'The published table counts all secondary-age children not in school, ages 12–18 — not exits from lower secondary. A matched test needs the DHS microdata.' },
        ],
      },
    ],
    bottomLine: 'Shadow education is not one disease with one cause. The model cannot crown a single explanation, but every surviving explanation points at the same policy levers — so act on the agreement, and keep measuring to break the tie.',
  },

  angkor: {
    kicker: 'What our models support',
    title: 'How food, labour, authority and climate interact',
    lede: 'A guided reconstruction followed by separate experiments on institutions, flight, relocation and uncertainty.',
    cta: { label: 'Start the guided reconstruction', route: 'angkor-guide' },
    sections: [
      {
        heading: 'Climate and the timing of decline',
        blocks: [
          { kind: 'para', tag: 'sim', text: 'We ran 2,000 matched parameter draws at each of three crop responses, plus a neutral-climate comparison. At the middle response, 1,260 of 2,000 runs decline; their median onset is 1362. Changing crop sensitivity shifts the timing.' },
          { kind: 'para', tag: 'ruled-out', text: 'The synthetic petri economy is a mechanism test only: it has no historical fit score and makes no claim to identify the cause of Angkor’s decline.' },
        ],
      },
      {
        heading: 'Distance, campaigns and the harvest',
        blocks: [
          { kind: 'para', tag: 'sim', text: 'Across six scenarios with 32 matched seeds each, moving the frontier from 180 to 540 km adds 40 campaign days and creates harvest overlap in every modelled year.' },
          { kind: 'para', tag: 'open', text: 'Unbounded stores mask food pressure in the default setup; historical quantities still need review.' },
        ],
      },
      {
        heading: 'Stone, pledges and who pays when the court leaves',
        blocks: [
          { kind: 'para', tag: 'sim', text: 'Default suppliers pledge during failed defence for 7.28 of 12 years on average; lowering trust reduces that to 2.34.' },
          { kind: 'para', tag: 'sim', text: 'With the same interruption, 21 of 32 courts exit. Allowing a funded return brings all 21 back.' },
          { kind: 'para', tag: 'open', text: 'These results test our belief rules. The numerical relationships have yet to be established historically.' },
        ],
      },
      {
        heading: 'Maintenance is the quiet variable',
        blocks: [
          { kind: 'para', tag: 'sim', text: 'The corrected maintenance-only drought median is 6,209 state-linked people, against an unchanged stable reference of 6,958.' },
        ],
      },
    ],
    bottomLine: 'No single mechanism carries the story: climate sets the timing, distance strains the army, and trust decides whether the centre holds. The models test mechanisms, not verdicts.',
  },
}
