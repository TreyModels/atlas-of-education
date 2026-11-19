// About and "How these models work": plain article pages. Content by Claude from Trey's own words (19 Nov 2026).
// Rendered by src/components/ArticlePage.tsx; Kimi owns presentation.

export interface ArticleSection { heading: string; paras: string[]; quote?: { text: string; who: string }; maths?: { plain: string; formula?: string; example?: string } }
export interface Article { id: string; kicker: string; title: string; lede: string; sections: ArticleSection[] }

export const about: Article = {
  id: 'about', kicker: 'About this site', title: 'Turning arguments about society into models anyone can run',
  lede: 'This is a working laboratory of computational social science by Dr. Trey Menefee. Each model takes an argument that usually lives in words, about schools, families, cities or states, and writes it as rules a computer can play out thousands of times. The code, available data, assumptions and current limitations are shared. Draft papers are being added; public availability does not imply peer review.',
  sections: [
    { heading: 'Why this exists', paras: [
      'I have wanted to do computational sociology since 2010. When I started my PhD I gave myself a year to learn Python well enough to build the models I had in mind. I couldn’t do it. The ideas stayed verbal: arguments in papers, never tested against their own logic.',
      'That has changed. With AI coding assistants (Claude, ChatGPT/Codex, DeepSeek and Kimi helped build this site and its models) and with other researchers’ published models to learn from and build on, I can now turn those verbal arguments into working models. Where a model borrows from someone else’s work, the page says so and cites it.',
    ] },
    { heading: 'Who I am', paras: [
      'I am a comparative education researcher. I lived and worked in China for about twenty years, did my PhD at the University of Hong Kong on farmer field schools (studying under Mark Bray), and have written on shadow education, credentials and schooling. A larger project, a long working paper on human evolution and the role of schools, is now being broken down into separate models here.',
      'My limit is fieldwork: I can’t easily collect new data. So these models are built from published studies, public statistics and my own observations, and each one says which of those it rests on.',
    ] },
    { heading: 'What kind of models these are', paras: [
      'Most are descriptive models: they try to represent how something actually works, with as much detail as the evidence supports, rather than the simplest possible toy. Each has a declared purpose. Some implement findings from peer-reviewed studies (marked “published study”; other sources, such as drafts and official statistics, are named as such). Some explore what would follow if a mechanism held. Some exist to teach an idea. Some are still being built.',
      'Many are based on draft papers. Those drafts will be published alongside the models as the next stage of this project.',
    ] },
    { heading: 'When a model doesn’t prove what I hoped', paras: [
      'Several models here do not support the argument I started with, at least not yet. In one, two explanations of private tutoring turn out to be the same model under different labels. In another, national case counts cannot tell a theory of corruption apart from simpler rivals. That is not a failure of the site. It is the point: a model that can disagree with its author is a test, and a test that can fail is science.',
      'Those results stay visible, labelled for what they are. They tell me where to go back and keep working, and they are an open invitation for anyone else to try.',
    ], quote: { text: 'All models are wrong, but some are useful.', who: 'George E. P. Box, statistician (1979)' } },
    { heading: 'Come and work on them', paras: [
      'Every model’s code can be downloaded and run on your own machine. If you think a model is missing something, change it and propose your version. Proposals are reviewed before anything is listed here. Everything is licensed CC BY-NC 4.0: reuse and adapt it with credit, for noncommercial purposes. Releases are versioned for citation; DOI 10.5281/zenodo.24369167.',
    ] },
  ],
}

export const howModelsWork: Article = {
  id: 'how-models-work', kicker: 'Start here', title: 'How these models work, without the jargon',
  lede: 'You don’t need to know any programming or statistics to read this site. This page explains the four ideas every model page uses: models, agents, Monte Carlo runs and status labels.',
  sections: [
    { heading: 'A model is an argument written precisely', paras: [
      'Social scientists make arguments all the time: “families pay for tutoring because the school day is too short”, or “drought weakened Angkor”. A computational model writes that argument as explicit rules. Once the rules are written down, a computer can follow them and show what they actually imply, including consequences the author did not expect.',
      'Writing the rules down forces every assumption into the open. That is the main benefit, even before any result.',
    ], quote: { text: 'The choice, then, is not whether to build models; it’s whether to build explicit ones.', who: 'Joshua M. Epstein, “Why Model?” (2008)' } },
    { heading: 'Agents: many small decisions, one big pattern', paras: [
      'Many models here are agent-based. Instead of one equation for a whole country, they simulate many individual actors (pupils, farmers, teachers, officials) each following simple rules. The pattern you see on a chart, such as the share of pupils buying tutoring, is what all those individual decisions add up to.',
    ] },
    { heading: 'Monte Carlo: run it thousands of times', paras: [
      'Real life has chance in it: a good or bad harvest, who meets whom. A model includes that chance with random numbers. So one run tells you very little; it is one possible history. A Monte Carlo simulation runs the same model hundreds or thousands of times with different random draws and reports what happens across all of them.',
      'Runs can differ for three reasons: chance events inside a run (random seeds), uncertain settings such as a crop response nobody has measured (parameter draws), and different versions of the rules themselves (structural alternatives). Pages say which kind of variation a result covers. When a page says “1,260 of 2,000 runs decline”, it means the model was run 2,000 times and the outcome happened in 1,260 of them. “Matched” runs use the same random draws in two scenarios, so the only difference between them is the thing being compared, for example real drought versus neutral climate.',
    ], maths: {
      plain: 'The main quantity is just a share: how many runs show the outcome, out of how many were run. A plotted range may describe different simulated outcomes or different parameter choices. Only a defined sampling interval measures finite-run precision; more runs do not remove uncertainty about the rules and inputs.',
      formula: 'share = runs with the outcome ÷ total runs',
      example: 'Angkor: with the drought record, 1,260 of 2,000 runs decline, a share of 1,260 ÷ 2,000 = 0.63, or 63%. With neutral climate, 0 of 2,000 decline. The matched comparison measures the effect of the drought record within this model and these assumptions. The 63% is a share of tested simulated cases, not the probability that drought explains the historical decline.',
    } },
    { heading: 'What a result can and cannot tell you', paras: [
      'A model result says: if these rules held, this is what would follow. Whether the rules do hold is a separate question, answered by comparing the model with data it was not built from. Many models here have not passed that second test yet, and the pages say so.',
      'Some numbers depend on an assumption nobody has measured. When that happens the page shows the result at several values of that assumption, so you can see how much it matters.',
    ] },
    { heading: 'Reading the labels', paras: [
      'The narrated model pages distinguish two kinds of label. Purpose says why it exists: a published foundation, a mechanism exploration, a teaching model, or a description that keeps accounts consistent. Development state says how far it has been checked: implementation checked, in development, historical result, or empirically evaluated. A label is a limit on what the model can claim, not a grade.',
      'Each paragraph on a model page is also marked as coming from a published study, from observed data, from an Atlas simulation, or as still unsettled.',
    ] },
  ],
}

export const workflow: Article = {
  id: 'workflow', kicker: 'My digital workflow, 2026', title: 'How one researcher and a team of AI agents build these models',
  lede: 'My most-read post on my old blog was “My Digital Workflow”. This is the 2026 version. I know some HTML and I ran a WordPress site with too many plugins. Nearly everything else you see here (the models, the code, the tests, this website) was built by AI agents working under my direction. This page describes exactly how, because the method matters as much as the models.',
  sections: [
    { heading: 'The team and its division of work', paras: [
      'I work with four AI systems. Claude coordinates and reviews; Codex manages model families, checks and deployment; DeepSeek workers draft code, pages and translations; Kimi handles visual design. The division of work lets me direct the research while using the tools for implementation.',
      'The expensive models spend their tokens on judgement: planning, reviewing, catching mistakes. The cheap model writes the long files. That division is what makes this affordable for one person.',
    ] },
    { heading: 'A shared message board between the agents', paras: [
      'The agents do not talk to each other directly. They share a message board, the Atlas Bridge: a small MCP server (the Model Context Protocol, a standard way to give AI tools access to other tools) that runs on my laptop. Every agent can post, read and attach files to it.',
      'Coordination follows a few strict rules, written after two agents once started on the same model at the same time. Each piece of work has one owner from start to finish. Before starting, an agent posts a claim naming the files and branch it will touch. When finished, it posts what it did, the commit, and the output of every check. Only one agent deploys the website, and nothing goes live without a passing checklist.',
    ] },
    { heading: 'A fleet of cheap workers', paras: [
      'For heavy writing, the coordinating agent sends tasks to a fleet of DeepSeek workers through a small runner script. Each task names the files the worker may read, the files it may write, and the checks its output must pass. The worker returns complete files; the runner writes them, runs the checks, and reports one line per task. The coordinator reviews the returned code and check output, compares claims with sources, and sends defects back for correction. Passing an automated check is not a substitute for that review.',
      'A typical instruction from me is short: “go spin up some agents and run more experiments”, or “convert the remaining families”. The agents turn that into claims, tasks, checks and a pull request.',
    ] },
    { heading: 'The scientific process underneath', paras: [
      'The workflow serves one process. I start from a verbal model: an argument from the literature or from my own theory and observations. The agents and I write it as explicit rules, find the published studies and data it should answer to, and turn it into code. The code is checked for consistency (do the books balance, do people get counted once), then run many times, then compared with observations it was not built from where such data exist.',
      'Every model then gets two labels, why it exists and how far it has been checked, and every paragraph on its page says whether it comes from a published study, observed data, a simulation, or is still open. Models that fail a test stay on the site, labelled as a historical or limited result. Some of my favourite arguments have not survived this process yet. That is what the process is for.',
    ] },
    { heading: 'How mistakes get caught', paras: [
      'AI agents make mistakes confidently, so the process assumes they will. Every number on a model page is traced back to a source file before it is published; drafts with numbers that cannot be traced are sent back. Building this site, that caught a misquoted figure from the Angkor paper, a results table still showing pre-review numbers, broken links, and a worker that ran out of budget halfway through a file. Automated checks run before every merge: model tests, translation coverage, a browser build, and pages loaded at desktop and phone sizes.',
      'The final checks are mine. I decide what the questions are, which explanations are worth modelling, and whether a result says what the page claims. The agents do the building; the judgement stays human.',
    ] },
    { heading: 'Open by default', paras: [
      'The public models and available materials live on GitHub under the stated reuse terms. Releases are versioned for citation; Zenodo DOI 10.5281/zenodo.24369167. Anyone can download a model, change it, and propose a version through a simple form. If this workflow is useful to you, copy it.',
    ] },
  ],
}
