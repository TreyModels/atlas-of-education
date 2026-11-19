import type { Journey } from './angkor-journey'

export const extensionJourney: Journey = {
  kicker: 'Family extension',
  title: 'Farmer field schools & food politics',
  lede:
    'Training programmes promise better farming. Prices, tenure and fiscal limits decide whether better farming pays. This extension follows that gap from a doctoral thesis through two small models.',
  why: [
    {
      claim: 'open',
      text:
        'The question came first. If field schools teach sound practice, why do graduates sometimes not adopt it? The thesis behind this extension asked that in agricultural training contexts in the Philippines and Kenya. It was qualitative work on motivation, not a validated country comparison, and no adoption rates are claimed here.',
    },
    {
      claim: 'method',
      text:
        'Two models follow. One asks when a farming practice pays and can spread through contact. The other asks what a government does when consumer and farmer interests pull against each other. They share a question, not code: the connection is conceptual.',
    },
  ],
  chapters: [
    {
      id: 'question',
      kicker: 'Chapter 1',
      title: 'Why train if the maths does not work?',
      question:
        'Field schools spread knowledge. Does knowledge alone move a farmer to adopt?',
      evidence: [
        {
          claim: 'open',
          text:
            'Trey Menefee’s 2016 HKU thesis, The Crisis Machine, motivates the question of why agricultural training may not lead to adoption. Its qualitative observations do not calibrate these models or establish national adoption rates.',
        },
      ],
      rule: [
        {
          claim: 'method',
          text:
            'Treat adoption as a decision under cost, yield and price, not as a knowledge gap. A farmer adopts only if the change is expected to pay and the upfront cost is affordable.',
        },
      ],
      result: [
        {
          claim: 'sim',
          text:
            'Under the stated rules, a practice can fail to spread because its net benefit is negative or its upfront cost is unaffordable. The model does not measure what farmers know.',
        },
      ],
      limitation: [
        {
          claim: 'open',
          text:
            'The thesis context is qualitative. Nothing here estimates how common non-adoption is, and the two models below are illustrative mechanisms, not forecasts.',
        },
      ],
      sources: [
        { label: 'Field schools README', href: 'research/field-schools/README.md' },
        { label: 'Validation notes', href: 'research/field-schools/VALIDATION.md' },
      ],
      models: [],
    },
    {
      id: 'observations',
      kicker: 'Chapter 2',
      title: 'What the fieldwork actually supports',
      question:
        'What can the thesis context carry into a model, and what can it not?',
      evidence: [
        {
          claim: 'open',
          text:
            'The thesis examined agricultural training in the Philippines and Kenya. Its contribution is motivational: it explains why adoption may stall even when training is sound. It is not a validated cross-country comparison, and this extension invents no adoption rates from it.',
        },
      ],
      rule: [
        {
          claim: 'method',
          text:
            'Carry the mechanism, not the magnitude. The models take the thesis claim as a hypothesis about incentives and test its internal logic, leaving empirical calibration open.',
        },
      ],
      result: [
        {
          claim: 'method',
          text:
            'The result is a set of transparent rules that can be argued with, rather than a number that pretends to settle the question.',
        },
      ],
      limitation: [
        {
          claim: 'open',
          text:
            'Qualitative motivation does not identify causal effects. No Kenya water or risk inference is drawn, and empirical inputs remain unresolved.',
        },
      ],
      sources: [
        { label: 'Field schools README', href: 'research/field-schools/README.md' },
      ],
      models: [],
    },
    {
      id: 'diffusion',
      kicker: 'Chapter 3',
      title: 'Adoption as a finite-horizon process',
      question:
        'If adoption pays for some farmers, how far does it spread?',
      evidence: [
        {
          claim: 'sim',
          text:
            'Model A places farmers on a lattice with one seed adopter. A neighbour becomes eligible when the net benefit is positive and the cost is affordable. Contact is adoption-mediated: only adopters recruit.',
        },
      ],
      rule: [
        {
          claim: 'method',
          text:
            'Gross benefit is access times price times one minus output share times yield gain. Expected margin is reliability times gross benefit minus perceived cost. Reliability is an assumed probability that the incremental yield benefit is realised. It is not the probability that profit exceeds cost, and it is not estimated risk aversion.',
        },
      ],
      result: [
        {
          claim: 'sim',
          text:
            'A round with no new adopters can be followed by further transmission. The process stops only when no eligible nonadopter has an adopted neighbour, or the horizon is reached. Full grids were regenerated; 17 checks pass.',
        },
      ],
      limitation: [
        {
          claim: 'open',
          text:
            'There is no separate knowledge or use state and no ongoing training mechanism. The conditional tenure cliff depends on cost, yield and price; the 25 percent marker is an illustrative output share, not statutory rent under PD 27, and no rent law is modelled.',
        },
      ],
      sources: [
        { label: 'Field schools README', href: 'research/field-schools/README.md' },
        { label: 'Validation notes', href: 'research/field-schools/VALIDATION.md' },
      ],
      models: ['fs-diffusion'],
    },
    {
      id: 'foodprice',
      kicker: 'Chapter 4',
      title: 'The price a government chooses',
      question:
        'Where should a government set the farmgate price when consumers and farmers want opposite things?',
      evidence: [
        {
          claim: 'sim',
          text:
            'Model B has a government pick the farmgate price that maximises a reduced-form political support function under a fiscal limit. Consumers want low prices; farmers want high ones. The tension is the point.',
        },
      ],
      rule: [
        {
          claim: 'method',
          text:
            'Farm productive aptitude is fixed, input intensity is chosen afresh each year, and farms may exit irreversibly. There is no advice market or accumulating productivity state.',
        },
      ],
      result: [
        {
          claim: 'sim',
          text:
            'The political counterfactual sets the support weight to one with zero subsidy allowance. That is a political scenario, not a welfare planner. Operating breakeven is computed before exit on current inputs, excluding outside wages.',
        },
      ],
      limitation: [
        {
          claim: 'open',
          text:
            'The supplied world price index is undocumented and not verified observed data. The 21 years from 2004 to 2024, seed 3, give a simulated pooled OLS of 0.39 rising and 0.57 falling. That is descriptive, not causal. All 18 checks pass and the seed 3 baseline is preserved.',
        },
      ],
      sources: [
        { label: 'Field schools README', href: 'research/field-schools/README.md' },
        { label: 'Validation notes', href: 'research/field-schools/VALIDATION.md' },
      ],
      models: ['fs-foodprice'],
    },
    {
      id: 'historical',
      kicker: 'Chapter 5',
      title: 'The treadmill and the price tag',
      question:
        'What older framings does this extension inherit, and how far can they be trusted?',
      evidence: [
        {
          claim: 'open',
          text:
            'The treadmill framing bundles the farm and the training machine. It is superseded here and has not been revalidated. The price tag framing carries an ambiguity about private advice and willingness to pay; that side branch is also not revalidated.',
        },
      ],
      rule: [
        {
          claim: 'method',
          text:
            'Keep the historical framings as context, not as tested claims. The current models stand on their own rules.',
        },
      ],
      result: [
        {
          claim: 'open',
          text:
            'Both historical cards are shown here once, as background. Neither is used to support a current result.',
        },
      ],
      limitation: [
        {
          claim: 'open',
          text:
            'Superseded framings can mislead if read as findings. They are included for lineage, and their open questions remain open.',
        },
      ],
      sources: [
        { label: 'Field schools README', href: 'research/field-schools/README.md' },
      ],
      models: ['fs-treadmill', 'fs-pricetag'],
    },
    {
      id: 'limits',
      kicker: 'Chapter 6',
      title: 'What this extension does not settle',
      question:
        'Where should a careful reader stop trusting these models?',
      evidence: [
        {
          claim: 'open',
          text:
            'The generated critiques are AI review notes, not peer review. Empirical inputs are unresolved, and no Kenya causal inference about water or risk is drawn.',
        },
      ],
      rule: [
        {
          claim: 'method',
          text:
            'Models A and B are separate. Their connection is conceptual, not coupled, and neither is calibrated to observed adoption or prices.',
        },
      ],
      result: [
        {
          claim: 'method',
          text:
            'The bundle ships code, tests, generated tables, figures and docs. It excludes source PDFs, prompts and manuscripts. The 35 checks across both models pass, and both remain developing.',
        },
      ],
      limitation: [
        {
          claim: 'open',
          text:
            'You are invited to download the bundle, change an assumption, and propose a version. The repository is public and the models are meant to be argued with.',
        },
      ],
      sources: [
        { label: 'Field schools README', href: 'research/field-schools/README.md' },
        { label: 'Validation notes', href: 'research/field-schools/VALIDATION.md' },
      ],
      models: [],
    },
  ],
  deeper: [],
  models: {
    'fs-diffusion': {
      id: 'fs-diffusion',
      title: 'Finite-horizon adoption on a lattice',
      purpose: 'mechanism',
      state: 'developing',
      note:
        'One seed adopter; neighbours adopt when net benefit is positive and cost is affordable. Reliability is an assumed probability the yield gain is realised. Quiet round is not absorption. 17 checks pass.',
      engine: 'research/field-schools/field-schools-models.zip',
      research: 'research/field-schools/README.md',
    },
    'fs-foodprice': {
      id: 'fs-foodprice',
      title: 'Farmgate price under political support',
      purpose: 'mechanism',
      state: 'developing',
      note:
        'Government picks farmgate price to maximise reduced-form political support under a fiscal limit. Fixed farm aptitude, annual input optimisation and irreversible exit. 18 checks pass; seed 3 baseline preserved.',
      engine: 'research/field-schools/field-schools-models.zip',
      research: 'research/field-schools/README.md',
    },
    'fs-treadmill': {
      id: 'fs-treadmill',
      title: 'The agricultural treadmill',
      purpose: 'mechanism',
      state: 'historical',
      note:
        'Bundled farm and training machine framing. Superseded and not revalidated; kept for lineage.',
      engine: 'research/field-schools/field-schools-models.zip',
      research: 'research/field-schools/README.md',
    },
    'fs-pricetag': {
      id: 'fs-pricetag',
      title: 'The price tag on advice',
      purpose: 'mechanism',
      state: 'historical',
      note:
        'Private advice and willingness-to-pay side branch. Ambiguous and not revalidated; kept for lineage.',
      engine: 'research/field-schools/field-schools-models.zip',
      research: 'research/field-schools/README.md',
    },
  },
  bottomLine:
    'Training changes what farmers know. Prices, tenure and fiscal limits change what they can do. These models make that gap explicit and invite you to test it.',
  repo: 'https://github.com/TreyModels/atlas-of-education',
  family: 'extension',
}
