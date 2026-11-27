import { useState } from 'react'
import './guangzhou.css'

const bins = [
  { label: '0–15%', value: 1.639 }, { label: '15–30%', value: 1.512 },
  { label: '30–45%', value: 1.436 }, { label: '45–60%', value: 1.347 },
  { label: '60–75%', value: 1.237 }, { label: '75–90%', value: 1.191 },
]
const release = 'https://github.com/TreyModels/atlas-of-education/releases/tag/v2026.11.27-guangzhou'

export function Guangzhou() {
  const [fade, setFade] = useState(3)
  const current = bins[fade]
  return <main id="main-content" className="gz">
    <header className="gz-hero"><div className="gz-wrap">
      <p className="gz-kicker">ATLAS OF EDUCATION · GUANGZHOU</p>
      <h1>Same score,<br /><em>same chance?</em></h1>
      <p className="gz-lead">A model of family resources, tutoring and the competition for university places.</p>
      <p>When students reach the same entrance score by different routes, what does equal treatment at the next gate tell us about fairness?</p>
      <div className="gz-actions"><a className="gz-primary" href="research/guangzhou/paper.pdf">Read the working paper</a><a href={release}>Explore code and results ↗</a></div>
    </div></header>
    <div className="gz-wrap">
      <aside className="gz-note"><strong>A simulation, not a survey.</strong> These results describe synthetic cohorts under explicit assumptions. They are not estimates of Guangzhou’s actual admission gaps or causal effects of policy.</aside>
      <section className="gz-section"><p className="gz-kicker">HOW TO READ THIS MODEL</p><h2>What you are looking at</h2>
        <p>This page summarizes an exploratory simulation of students moving through Guangzhou’s education system. The computer creates synthetic pupils, gives them different family resources and school experiences, and follows their path from the zhongkao entrance exam through high school to a simulated university admission.</p>
        <div className="gz-steps">
          <div><strong>1. Before high school</strong><p>Family resources, junior-school teaching and tutoring contribute to a pupil’s exam score. Each pupil also has a simulated starting ability.</p></div>
          <div><strong>2. High school</strong><p>Pupils are sorted into schools and classes. A school’s top band receives a modeled teaching and peer advantage. Some pupils are reassigned in senior 2.</p></div>
          <div><strong>3. The final competition</strong><p>Eligible academic-track pupils compete for places equal to 10% of the whole synthetic cohort. The model adds bonuses for two alternative routes in one simplified ranking.</p></div>
        </div>
        <p>Each of the 1,024 runs uses 40,000 newly generated pupils and a different set of 31 assumptions sampled from stated ranges. The figures below are medians across those runs. They describe a model of how a system could behave, not measured outcomes for Guangzhou.</p>
        <p>For the richer–poorer comparisons, richer means the top 40% and poorer the bottom 40% of modeled family wealth among local-hukou pupils. The ratios include local pupils who do not enter the academic track, who have no chance of the modeled university place.</p>
      </section>
      <section className="gz-section"><p className="gz-kicker">ONE SYSTEM, THREE QUESTIONS</p><h2>What does “the same” mean?</h2>
        <p>Each ratio compares the admission rate of pupils from richer local families with the rate for pupils from poorer local families. A value of 1 means equal rates. The comparisons use different groups of pupils.</p>
        <div className="gz-ratios">
          {[['Similar entrance scores',0.91,'The rates are close, with a modest advantage for the poorer group.'],['Similar scores and starting ability',1.19,'The richer group is 19% more likely to win a place.'],['Similar starting ability',1.36,'The richer group is 36% more likely to win a place.']].map(([label,value,description]) => <div className="gz-ratio" key={label}><div className="gz-ratio-label"><strong>{label}</strong><b>{Number(value).toFixed(2)}</b></div><div className="gz-track"><div className="gz-bar" style={{width: `${Number(value)/1.6*100}%`}} /></div><p>{description}</p></div>)}
        </div><p className="gz-caption">Medians across 1,024 independently sampled parameter settings, with 40,000 simulated pupils per setting. Starting ability is a model variable and cannot be observed directly.</p>
      </section>
      <section className="gz-section gz-split"><div><p className="gz-kicker">THE IMPORTANT UNKNOWN</p><h2>How long does an early advantage last?</h2><p>Home resources, teachers and tutoring can affect a pupil’s score before senior high school. The model combines these into one early advantage and varies how much fades later.</p><p>Move the slider to select one of six ranges for the share of early advantage that fades. The number shows the median rich-to-poor admission ratio among runs in that range. A ratio of 1 would mean equal rates. Other assumptions also vary within each range, so moving the slider compares existing groups of simulations; it does not run the model or isolate a causal effect.</p></div>
        <div className="gz-explore"><label htmlFor="gz-fade">Early advantage that fades <strong>{current.label}</strong></label><input id="gz-fade" type="range" min="0" max="5" step="1" value={fade} onChange={e => setFade(Number(e.target.value))} /><div className="gz-ends"><span>Less fades</span><span>More fades</span></div><div className="gz-big" aria-live="polite">{current.value.toFixed(2)} <span>times the admission rate</span></div><div className="gz-track"><div className="gz-bar" style={{width: `${current.value/1.8*100}%`}} /></div><p>At equal simulated starting ability, richer pupils are {current.value.toFixed(2)} times as likely to win a slot in the median run in this group.</p></div>
      </section>
      <section className="gz-section"><p className="gz-kicker">FIXED SEATS</p><h2>When one pupil gains a place</h2><div className="gz-seat"><strong>187</strong><p>of 4,000 places changed hands in the median simulated cohort when route bonuses were added. Across the middle 90% of runs, about 53–418 places changed hands.</p></div><p>In the model, the number of places stays fixed. Lean checked the mathematical statement that every new admission is matched by a lost place when both rankings admit the same number of pupils. Real art and joint-exam admissions have separate rules and capacities; the simulation uses a single-ranking approximation.</p></section>
      <section className="gz-section"><p className="gz-kicker">BEFORE AND AFTER</p><h2>What happens when the rules change?</h2><p>In a hypothetical paired comparison, the model switches on a pre-gate tutoring restriction and senior-2 re-banding together. The equal-ability gap narrowed in 807 of 1,024 runs, and median modeled tutoring spending fell by about ¥5,069 per pupil across five school years.</p><p>We do not know whether performance-based re-banding became more common after 2021. This comparison is not an estimate of the causal effect of Double Reduction.</p></section>
      <section className="gz-section"><p className="gz-kicker">WHAT IS ASSUMED</p><h2>Where the results come from</h2>
        <p>The model fixes the number of university proxy places and assumes school and class placement depend partly on exam scores. It represents academic tutoring as more common among both low- and high-achieving pupils, with take-up influenced by wealth and classmates. It applies route bonuses within one common ranking, although actual admission routes have separate eligibility and capacities.</p>
        <p>The size and persistence of home, school and tutoring advantages are uncertain. Parameters are drawn independently and uniformly over selected ranges, rather than fitted to Guangzhou pupil records. The 5th–95th percentile ranges in the paper describe variation under these chosen assumptions; they are not confidence intervals for the city.</p>
        <p>Selected mathematical properties were checked in Lean, including the balance between pupils gaining and losing seats when both rankings fill the same number of places. The Python cutoff admits ties, so exact seat capacity is checked for each sampled run rather than guaranteed for every possible input.</p>
        <p>Field context comes from the author’s observations and one confidential informant. The informant’s educational pathway is not included on this public page.</p>
      </section>
      <section className="gz-section"><p className="gz-kicker">OPEN RESEARCH</p><h2>Help improve the assumptions</h2><p>The most valuable evidence would connect entrance scores, class and teacher assignments, tutoring, family resources and later results. The parameter register identifies the ranges and their sources. Contributions with a clear population, year, units and source are welcome.</p><div className="gz-actions"><a className="gz-primary" href="research/guangzhou/paper.pdf">Read the paper</a><a href={release}>Code, proofs and synthetic data ↗</a><a href="https://doi.org/10.5281/zenodo.24575246">Cite the archived release · DOI ↗</a><a href="https://github.com/TreyModels/atlas-of-education/issues">Suggest evidence ↗</a></div></section>
    </div>
  </main>
}
