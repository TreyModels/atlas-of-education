import type { Journey } from './angkor-journey'

export const shadowJourney: Journey = {
  kicker: 'Education and work · Shadow education · Cambodia',
  title: 'Why do pupils pay their own teachers?',
  lede: 'In six Siem Reap schools, about four in five secondary pupils bought private lessons, and more than half of those lessons came from the teacher who already taught them (Bray and colleagues, 2016 and 2018). This page follows one question through the Atlas models: can those published patterns tell three rival explanations apart — a timetable too short, content held back and sold, or goodwill bought from your own teacher? The short answer is no. The way the models fail is more useful than a tidy verdict would have been.',
  repo: 'https://github.com/TreyModels/atlas-of-education',
  family: 'shadow',
  why: [
    { text: 'A tutoring market is common. A tutoring market that runs through the classroom itself is less so. When a pupil pays the person who sets and marks their work, three ordinary stories compete: the school day is too short, the teacher is selling back what was withheld, or the pupil is buying goodwill. Each story is plausible on its own. The question is whether evidence can choose between them.' },
    { claim: 'method', text: 'So we ask two things in order. First, what do the published patterns say, and what happens when a model of pupils and teachers is fitted to them? That part is described in Chapters 1 to 3. Second, can those patterns separate the explanations at all? That part is ours, and it is where the answer turned out to be uncomfortable.' },
    { claim: 'method', text: 'We follow a descriptive approach (Edmonds and Moss, “From KISS to KIDS”): add detail where the evidence supports it, and label every paragraph as published, observed, simulated or still unsettled. Where a result has been superseded by a correction, we say so rather than quietly replacing it.' },
  ],
  chapters: [
    {
      id: 'puzzle', kicker: 'Chapter 1 · The published pattern',
      title: 'Pupils pay the teacher in front of them',
      question: 'Why do pupils buy extra lessons, and what do the surveys actually report?',
      evidence: [
        { claim: 'published', text: 'Bray, Kobakhidze, Liu and Zhang (2016) and Bray, Kobakhidze, Zhang and Liu (2018) report the pattern that starts this page: in six Siem Reap schools, tutoring participation is 81.9% overall, 74.7% in Grade 9 and 89.8% in Grade 12. Of the lessons bought, 57.7% come from the pupil’s own teacher and 40.9% from a parallel-class teacher. About half of teachers tutor (13 of 24), commercial providers hold a small share, and the urban–rural gap is only 2.6 percentage points.' },
        { claim: 'published', text: 'The puzzle is in the middle of that list. A pupil who wants more teaching has other places to go: the parallel-class teacher, a commercial centre. Buying from the person who already teaches you is a different act, and the literature asks why it is so common.' },
        { claim: 'data', text: 'These patterns come from one study of six schools. The repository holds no second independent survey of the same schools and no pupil-level records, so its own fact check scores the first gate as only half met.' },
      ],
      rule: [
        { claim: 'method', text: 'The model holds 72 teachers and 1,260 pupils in six Siem Reap–style schools, Grades 9 and 12, four subjects. Each teacher decides whether to tutor. Each pupil chooses, subject by subject, between their own teacher, the parallel-class teacher, a commercial provider, or nobody.' },
        { claim: 'method', text: 'The seven published patterns — overall, Grade 9 and Grade 12 participation, the urban–rural gap, the own-teacher and other-teacher shares, and the share of teachers who tutor — plus a small commercial share, are the targets the model is fitted to.' },
      ],
      result: [
        { claim: 'data', text: 'So the question is narrow on purpose. It is not “why does Cambodia tutor?” but “why, in these six schools, do so many pupils buy from the teacher in front of them?” A model that answers the second question says nothing directly about the first.' },
      ],
      limitation: [
        { claim: 'open', text: 'One study, six schools, seven aggregate patterns, no pupil-level data. Everything later on this page inherits that base. Seven summary numbers leave little room for a model to be wrong in an interesting way: many different rules can pass through the same seven points.' },
      ],
      sources: [
        { label: 'Bray et al. (2016, 2018): citations and the seven patterns, on the shadow-education lab page', href: 'research/shadow-education.html' },
        { label: 'Shadow education research folder and README', href: 'https://github.com/TreyModels/atlas-of-education/tree/main/research/shadow-education' },
      ],
      models: ['shadow-lab'],
    },
    {
      id: 'rivals', kicker: 'Chapter 2 · Three rival explanations',
      title: 'Thin hours, held-back content, or goodwill',
      question: 'What could make a pupil pay the teacher who already teaches them?',
      evidence: [
        { claim: 'published', text: 'Thin. The official timetable is too short for the curriculum, so pupils need more hours from somebody. On this explanation a teacher gains nothing by holding content back.' },
        { claim: 'published', text: 'Diversion. A teacher covers less of the curriculum in the regular lesson and covers the missing part in paid sessions.' },
        { claim: 'published', text: 'Favour. Paying your own teacher brings a benefit of its own — better treatment, marks or goodwill — whatever is covered in class.' },
      ],
      rule: [
        { claim: 'method', text: 'Thin becomes one rule: a single curriculum requirement sits above the timetabled hours, and every pupil is short of the same hours, whoever they buy from.' },
        { claim: 'method', text: 'Diversion becomes two: the teacher chooses how much of the regular lesson to withhold, and withholding costs the teacher something (a cost term and a convexity term).' },
        { claim: 'method', text: 'Favour becomes one number: the own-teacher option carries an extra value f. Nothing about hours or coverage changes.' },
      ],
      result: [
        { claim: 'method', text: 'Each explanation is a different lever on the same logit choice model, not a different world. That is convenient for side-by-side comparison, and — as Chapter 4 shows — risky for it.' },
      ],
      limitation: [
        { claim: 'open', text: 'None of the three rules has a measured magnitude. The coverage requirement, the withholding cost and the value of favour are fitted or assumed, so the model can rank explanations only through the seven patterns it was fitted to.' },
      ],
      sources: [
        { label: 'The three explanations, described on the lab page', href: 'research/shadow-education.html' },
        { label: 'Tutoring ABM review reruns (14 November 2026)', href: 'https://github.com/TreyModels/atlas-of-education/blob/main/experiments/shadow-abm/README.md' },
      ],
      models: ['tutoring-abm'],
    },
    {
      id: 'calibration', kicker: 'Chapter 3 · The archived calibration',
      title: 'Fitting each explanation to the seven patterns',
      question: 'How well does each explanation reproduce what the survey reported?',
      evidence: [
        { claim: 'data', text: 'The fit asks each candidate setting to reproduce the patterns of Chapter 1: participation 81.9%, 74.7% in Grade 9, 89.8% in Grade 12, own-teacher share 57.7%, other-teacher share 40.9%, a small commercial share, and about half of teachers tutoring.' },
        { claim: 'method', text: 'Parameters were fitted by ABC-SMC with resampling and three Metropolis moves per generation. Each setting is scored on 10 school systems and judged by the 7th-smallest per-world maximum z-score, so a setting has to fit about 7 of 10 worlds.' },
      ],
      rule: [
        { claim: 'method', text: 'The acceptance rule is a tolerance on those per-world scores; a fresh-world check then reruns each accepted setting in new random school systems. The archived run stopped at a tolerance of 1.0–1.07, reached after the resampling fix that raised the favour variant’s final importance ESS from 71 of 400 to 121 of 200.' },
      ],
      result: [
        { claim: 'sim', text: 'On 20 fresh worlds per setting, the pair fit rate is 37–44%; the older single-world run gave 17–19%. Only 1–7% of settings fit at least 70% of fresh worlds (older: 0–1%). At a tolerance of 1, only 0–4% of proposals fit, and the evidence ratios are tiny: thin 2.5e-7, favour 2.1e-8, full 7.9e-9, diversion 0.' },
        { claim: 'sim', text: 'Calibrated teachers withhold almost nothing. Median withholding is 0% in every variant. Diversion settings withhold more than 1% of the curriculum in 21% of fresh worlds, with a 95th percentile of 9%.' },
      ],
      limitation: [
        { claim: 'open', text: 'Read all of this as historical. The provider observation equation now counts pupils naming providers, and the SMC evidence estimator now uses the raw proposal density; both were corrected on 16 November 2026. The numbers above predate those fixes and need rerunning, so they record what the archived calibration found, not what a current fit would find.' },
        { claim: 'open', text: 'The evidence ratios rest on a handful of fitting proposals. Thin fits most often, but each estimate rests on only a few accepted settings, so the ordering between explanations is not something to lean on.' },
      ],
      sources: [
        { label: 'Tutoring ABM review reruns: fresh-world fit, ESS and evidence', href: 'https://github.com/TreyModels/atlas-of-education/blob/main/experiments/shadow-abm/README.md' },
        { label: 'The research README (generated from results/*.json)', href: 'https://github.com/TreyModels/atlas-of-education/tree/main/research/shadow-education' },
      ],
      models: ['tutoring-abm', 'shadow-lab'],
    },
    {
      id: 'equivalence', kicker: 'Chapter 4 · Two labels, one model',
      title: 'Favour is thin relabelled',
      question: 'Can the three explanations be told apart, even in principle?',
      evidence: [
        { claim: 'method', text: 'With diversion off, a pupil compares three options: their own teacher, worth b + f; another teacher, worth b − c_o; a commercial provider, worth b − c_c. Buying nothing is worth 0. Raising f by some amount is the same as raising b and both costs by that amount. The utilities are unchanged, so the choice probabilities are unchanged.' },
        { claim: 'sim', text: 'The code check: each of the 116 distinct fitted favour settings was rewritten as a thin setting and compared with its favour original in three school systems — no policy, then each of the four policy levers. The largest difference in any output is 6.7e-16, which is rounding error.' },
        { claim: 'sim', text: 'The recovery test: 24,000 pretend datasets, 30 fresh school systems for each of 200 fitted settings per variant. Naming one of three explanations scores 45% (41–49) against 33% chance, and 41% (36–46) on the datasets that fit all seven patterns. Thin against diversion scores 52% (46–57). With every model output added at once, three-way accuracy is 49% (45–54).' },
        { claim: 'sim', text: 'The placebo row is the one to read. Thin against favour is the same model, yet the classifier names it correctly 62% of the time, because the two calibrations settled in different corners of their allowed ranges. Any separation at or below that level is an artefact of the ranges, not of the explanations.' },
      ],
      rule: [
        { claim: 'method', text: 'Why the explanations agree about policy: they share one model.py. Only 6 of about 215 lines and 2 of 15 priors differ. Removing the thin-market channel or the alternative providers moves every variant’s policy effects together — the ban effect on participation goes from −0.35 to −0.51 — and the fit collapses. Changing the diversion-specific withholding cost or convexity changes nothing.' },
        { claim: 'sim', text: 'So the policy picture is one picture. A ban on teachers tutoring their own pupils cuts participation by about 35–40 points and coverage by 5–6 points, and sends pupils to parallel-class and commercial providers. Paying teachers not to tutor their own pupils cuts participation by 16–19 points. Ten more points of class time is the only lever that raises coverage, by about 8 points, and it barely touches participation.' },
      ],
      result: [
        { claim: 'open', text: 'In the wording the review recommends: “The current aggregate targets poorly distinguish the variants; favour and thin are equivalent under the stated transformation where the commercial-cost floor does not bind.”' },
        { claim: 'sim', text: 'Diversion mostly behaves like thin. The median fitted diversion setting withholds 0.000 of the curriculum, and a setting that withholds nothing is thin.' },
      ],
      limitation: [
        { claim: 'open', text: 'The transformation is only exact where the commercial-cost floor does not bind: the implementation clamps commercial cost at zero after the commercial-entry policy, and 32 of the 116 rewritten favour settings fell outside the thin variant’s allowed prior ranges. Those ranges, not different behaviour, explain the different fit rates in the archived calibration.' },
        { claim: 'open', text: 'Diversion can generate withholding, so the algebra does not make all three identical everywhere; it makes favour and thin identical wherever the floor is slack.' },
        { claim: 'open', text: 'And a classifier struggling in one finite experiment does not show that no data could separate the explanations. It shows that these seven aggregate patterns, read through this model, do not — and the pretend datasets come from settings fitted to those same patterns, so the test describes the region that fits Siem Reap, not every possible school system.' },
      ],
      maths: {
        plain: 'A pupil weighs three paid options against buying nothing. Each option has a value: your own teacher gives the base lesson plus any favour; another teacher or a commercial provider gives the base lesson minus what it costs to go outside. The logit rule turns those values into probabilities. If you add the same amount to the base value and to both costs, every option keeps its value and nothing about the pupil’s choice changes.',
        formula: 'U_own = b + f,   U_other = b − c_o,   U_commercial = b − c_c,   U_none = 0;   P(j) = e^(U_j) / (1 + Σ_k e^(U_k))',
        symbols: [
          ['b', 'the base value of a lesson to the pupil'],
          ['f', 'favour: the extra value of buying from your own teacher'],
          ['c_o', 'the extra cost of buying from another teacher'],
          ['c_c', 'the extra cost of buying from a commercial provider'],
          ['U_j', 'the value (utility) of option j; buying nothing is worth 0'],
          ['P(j)', 'the logit probability that the pupil picks option j'],
        ],
        example: 'Take b = 1, f = 0.5, c_o = 0.3, c_c = 0.8. With favour: own = 1.5, other = 0.7, commercial = 0.2. Now set f = 0 and raise b, c_o and c_c by 0.5, so b′ = 1.5, c_o′ = 0.8, c_c′ = 1.3: own = 1.5, other = 1.5 − 0.8 = 0.7, commercial = 1.5 − 1.3 = 0.2. Same three utilities, so the same three probabilities. These numbers are illustrative and are not estimates.',
      },
      sources: [
        { label: 'Research README: equivalence, recovery test and discrimination test', href: 'https://github.com/TreyModels/atlas-of-education/tree/main/research/shadow-education' },
        { label: 'Tutoring ABM review reruns: shared code and policy agreement', href: 'https://github.com/TreyModels/atlas-of-education/blob/main/experiments/shadow-abm/README.md' },
      ],
      models: ['tutoring-abm'],
    },
    {
      id: 'signatures', kicker: 'Chapter 5 · What would separate them',
      title: 'Three signatures nobody has measured yet',
      question: 'What would each explanation predict that the others do not?',
      evidence: [
        { claim: 'open', text: 'Favour: school-assessed marks rise for pupils who buy from their own teacher, while externally marked exam scores do not. That needs marks in the model and both kinds of score in the data.' },
        { claim: 'open', text: 'Diversion: content covered in regular lessons is lower in a tutoring teacher’s classes than in the same teacher’s classes in a subject or year where tutoring is not sold. That needs a within-teacher comparison, not a comparison between teachers.' },
        { claim: 'open', text: 'Thin: take-up tracks timetabled hours against curriculum load across subjects and grades, whoever the teacher is.' },
      ],
      rule: [
        { claim: 'method', text: 'Each signature asks for something the model does not carry: school marks kept apart from exam scores; a teacher’s own coverage recorded where tutoring cannot be sold; hours and curriculum load entered by subject and grade.' },
        { claim: 'method', text: 'The order of work is data first. The pupil-level survey behind Bray et al. may already hold some of this; asking for it comes before any more modelling.' },
      ],
      result: [
        { claim: 'open', text: 'None of the three signatures is built or tested. They are proposals, listed here so that the next version can be judged against something it did not invent after the fact.' },
      ],
      limitation: [
        { claim: 'open', text: 'A proposed signature is not evidence. A model written to produce one would still need testing on data it was not built from, and the earlier lesson stands: two rules that look different can leave the same trace.' },
      ],
      sources: [
        { label: '“To make the explanations rivals”: the candidate signatures', href: 'https://github.com/TreyModels/atlas-of-education/tree/main/research/shadow-education' },
      ],
      models: ['research-folder'],
    },
    {
      id: 'credential', kicker: 'Chapter 6 · A second test, same outcome',
      title: 'Who leaves school? The credential floor',
      question: 'Does a wealth profile tell the credential stories apart?',
      evidence: [
        { claim: 'data', text: 'UIS completion rates by wealth quintile, from the Cambodia DHS 2021–22, put the share of lower-secondary non-completers who come from the poorest 40% of households at 55–64%.' },
        { claim: 'sim', text: 'A separate Atlas model reads that share from three structures. Human capital: 71% (54–89) under a hard liquidity threshold, 57% (53–60) under a graded one. Positional: 78% (59–92) hard, 58% (54–61) graded. Relational floor: 85% (69–97) hard, 58% (54–61) graded.' },
      ],
      rule: [
        { claim: 'method', text: 'The threshold is the rule that matters. A hard liquidity threshold creates a completion cliff by wealth, so households either can or cannot pay. A graded threshold lets them trade school against work at the margin.' },
      ],
      result: [
        { claim: 'sim', text: 'With a hard threshold no structure fits the full wealth profile, and the relational floor fails. With a graded threshold all three fit and predict the same share. So this test does not separate the credential stories either.' },
      ],
      limitation: [
        { claim: 'open', text: 'Child weights per quintile are assumed; the DHS microdata would remove that assumption. The earlier rejection of the relational floor came from the hard threshold rather than from the data, and the v1 bundle also compared a 2035 value with 2021 data — a known error now recorded in the review notes.' },
      ],
      sources: [
        { label: 'Cambodia DHS 2021–22 (FR377)', href: 'https://www.dhsprogram.com/pubs/pdf/FR377/FR377.pdf' },
        { label: 'DHS credential-floor test: code and results · ZIP', href: 'research/shadow/credential_floor_dhs.zip' },
      ],
      models: ['credential-dhs'],
    },
  ],
  deeper: ['research-folder'],
  models: {
    'shadow-lab': { id: 'shadow-lab', title: 'Shadow education lab (stored runs)', purpose: 'mechanism', state: 'historical', note: 'The lab page keeps the archived calibration and its policy explorer. It predates the 16 November 2026 corrections to the provider observation equation and the SMC evidence estimator, so its numbers are a record, not a current fit.', research: 'research/shadow-education.html' },
    'tutoring-abm': { id: 'tutoring-abm', title: 'Tutoring agent-based model (code and calibration)', purpose: 'mechanism', state: 'historical', note: 'Six schools, 72 teachers, 1,260 pupils. The shipped calibration bundle predates the corrections, so its posterior tables and evidence ratios need rerunning; the ODD protocol has not been externally reviewed.', engine: 'research/shadow/tutoring_abm.zip' },
    'credential-dhs': { id: 'credential-dhs', title: 'Credential floor and the DHS wealth profile', purpose: 'mechanism', state: 'evaluated', note: 'Compared with UIS completion rates by wealth quintile (Cambodia DHS 2021–22). Once the liquidity threshold is graded, all three structures predict the same share, so the data do not discriminate them; child weights per quintile are assumed.', engine: 'research/shadow/credential_floor_dhs.zip' },
    'research-folder': { id: 'research-folder', title: 'Shadow education research track', purpose: 'mechanism', state: 'developing', note: 'The equivalence check, the simulated dataset bank, the recovery test and the discrimination test, with scripts to rerun them. Still developing: the planned paper on telling the explanations apart cannot be written from this model as built.', research: 'https://github.com/TreyModels/atlas-of-education/tree/main/research/shadow-education' },
  },
  bottomLine: 'In the archived runs the three explanations fit the seven published patterns about equally well, and favour turned out to be thin with a different label: all 116 fitted favour settings, rewritten, give identical outputs. Their agreement about policy comes from shared code, not from independent evidence, so nothing here ranks the explanations. What the work does deliver is a sharper question and three measurable signatures for the next version.',
}
