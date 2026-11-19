// Home page explainer content. Rendered by src/components/Library.tsx.
// Every string here is translated via work/home-explainer-translations.json.

export interface HomeExplainerIntro {
  title: string
  paragraphs: string[]
}

export interface HomeExplainerAuthor {
  title: string
  paragraph: string
}

export interface HomeExplainerStep {
  title: string
  text: string
}

export interface HomeExplainerLimit {
  title: string
  text: string
}

export interface HomeExplainerInvitation {
  title: string
  paragraphs: string[]
}

export interface HomeExplainer {
  intro: HomeExplainerIntro
  author: HomeExplainerAuthor
  howItWorks: HomeExplainerStep[]
  howToRead: HomeExplainerLimit[]
  invitation: HomeExplainerInvitation
}

export const homeExplainer: HomeExplainer = {
  intro: {
    title: 'An open laboratory for computational social science',
    paragraphs: [
      'This site is a working laboratory, not a finished textbook. It takes human questions about schools, families, history and institutions and turns them into models a computer can run. Each model begins with a question a person might actually ask: why do families pay for private tutoring, why did fertility fall so far across East Asia, how did Angkor feed a vast city, how did early humans move out of Africa?',
      'A model here is an argument made explicit. Instead of leaving assumptions buried in prose, we write them as rules: who acts, what they know, what they choose, and what happens next. Then we run those rules many times and compare the outcomes with evidence. The point is not to produce a single impressive number. It is to keep the reasoning visible, so you can see where a conclusion comes from and where it might break.',
    ],
  },
  author: {
    title: 'Who made this',
    paragraph: 'I am Trey Menefee, a comparative education researcher. I have wanted to do computational sociology since 2010; during my PhD I gave myself a year to learn Python well enough to build these models and did not finish them. New tools now make it possible to turn those verbal arguments into working models, and this site is where I am doing that in the open. Claude, Codex, DeepSeek and Kimi helped build the code and site; I remain responsible for the research questions, assumptions and claims.',
  },
  howItWorks: [
    {
      title: 'Start with a question',
      text: 'Every collection begins with a real puzzle, not a method in search of a use. It may come from an observation, a draft argument, or a published study. The question is stated plainly before any model appears.',
    },
    {
      title: 'Write the assumptions as rules',
      text: 'We make the assumptions explicit: what actors exist, what they can do, and what constraints they face. Writing the rules down forces hidden guesses into the open, which is useful even before any result.',
    },
    {
      title: 'Run, repeat, compare',
      text: 'Models are run many times with different random draws, because real life contains chance. We compare outcomes across runs and, where suitable data exist, against observations. Each model says whether that comparison used fitting data or a separate evaluation. A single lucky run cannot carry the argument.',
    },
    {
      title: 'Keep findings and limits visible',
      text: 'Every result is labelled for what it is: measured from data, produced by a simulation, ruled out, or still open. Limits stay on the page rather than in a footnote, because a model that can disagree with its author is a test worth having.',
    },
  ],
  howToRead: [
    {
      title: 'Descriptive where evidence supports detail',
      text: 'Most models here try to represent how something actually works, with as much detail as the evidence allows, rather than the simplest possible toy. Where a model is instead a simple teaching device, the page says so. Code and models borrowed from other researchers are credited and cited.',
    },
    {
      title: 'Published findings are kept separate from my own hypotheses',
      text: 'Some models implement results from peer-reviewed studies. Others explore what would follow if a mechanism held, or exist to teach an idea. These are marked differently. A model whose code has been checked is not the same as a tested historical explanation, and the pages do not pretend otherwise.',
    },
    {
      title: 'Negative findings are findings',
      text: 'When a model fails to support the argument I started with, that stays visible. A negative result can expose a coding error, a bad assumption, or a limit in the data; it does not by itself refute a social theory. It tells us where to look next.',
    },
  ],
  invitation: {
    title: 'Come and work on them',
    paragraphs: [
      'The code and available data are shared. Manuscripts are being added; I am not promising that everything is available today. Interactive workbenches run in your browser, while downloadable Python models run on your own machine, and the two are different things. If you think a model is missing something, change it and propose your version. Proposals are reviewed before anything is listed here; nothing is uploaded automatically.',
      'You do not need to know any programming to read the story. The math is optional and the words come first. A Monte Carlo run means the model was repeated with specified random draws; a figure like 63% is a share of tested simulated cases, not the probability that a claim is true.',
    ],
  },
}
