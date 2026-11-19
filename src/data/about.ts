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
      'Every model can be downloaded, run on your own machine and changed. If you think a model is missing something, change it and propose your version. Proposals are reviewed before anything is listed here. Everything is licensed CC BY-NC 4.0: reuse and adapt it with credit, for noncommercial purposes. Releases are versioned for citation; a DOI will be displayed when issued.',
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
