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
      <section className="gz-section"><p className="gz-kicker">ONE SYSTEM, THREE QUESTIONS</p><h2>What does “the same” mean?</h2>
        <p>Each ratio compares the admission rate of pupils from richer local families with the rate for pupils from poorer local families. A value of 1 means equal rates. The comparisons use different groups of pupils.</p>
        <div className="gz-ratios">
          {[['Similar entrance scores',0.91,'The rates are close, with a modest advantage for the poorer group.'],['Similar scores and starting ability',1.19,'The richer group is 19% more likely to win a place.'],['Similar starting ability',1.36,'The richer group is 36% more likely to win a place.']].map(([label,value,description]) => <div className="gz-ratio" key={label}><div className="gz-ratio-label"><strong>{label}</strong><b>{Number(value).toFixed(2)}</b></div><div className="gz-track"><div className="gz-bar" style={{width: `${Number(value)/1.6*100}%`}} /></div><p>{description}</p></div>)}
        </div><p className="gz-caption">Medians across 1,024 independently sampled parameter settings, with 40,000 simulated pupils per setting. Starting ability is a model variable and cannot be observed directly.</p>
      </section>
      <section className="gz-section gz-split"><div><p className="gz-kicker">THE IMPORTANT UNKNOWN</p><h2>How long does an early advantage last?</h2><p>Home resources, teachers and tutoring can affect a pupil’s score before senior high school. The model combines these into one early advantage and varies how much fades later.</p><p>Move the slider to see the median admission ratio in each group of runs. Other assumptions also vary, so these are sensitivity results.</p></div>
        <div className="gz-explore"><label htmlFor="gz-fade">Early advantage that fades <strong>{current.label}</strong></label><input id="gz-fade" type="range" min="0" max="5" step="1" value={fade} onChange={e => setFade(Number(e.target.value))} /><div className="gz-ends"><span>Less fades</span><span>More fades</span></div><div className="gz-big" aria-live="polite">{current.value.toFixed(2)} <span>times the admission rate</span></div><div className="gz-track"><div className="gz-bar" style={{width: `${current.value/1.8*100}%`}} /></div><p>At equal simulated starting ability, richer pupils are {current.value.toFixed(2)} times as likely to win a slot in the median run in this group.</p></div>
      </section>
      <section className="gz-section"><p className="gz-kicker">FIXED SEATS</p><h2>When one pupil gains a place</h2><div className="gz-seat"><strong>187</strong><p>of 4,000 places changed hands in the median simulated cohort when route bonuses were added. Across the middle 90% of runs, about 53–418 places changed hands.</p></div><p>In the model, the number of places stays fixed. Lean checked the mathematical statement that every new admission is matched by a lost place when both rankings admit the same number of pupils. Real art and joint-exam admissions have separate rules and capacities; the simulation uses a single-ranking approximation.</p></section>
      <section className="gz-section"><p className="gz-kicker">BEFORE AND AFTER</p><h2>What happens when the rules change?</h2><p>In a hypothetical paired comparison, the model switches on a pre-gate tutoring restriction and senior-2 re-banding together. The equal-ability gap narrowed in 807 of 1,024 runs, and median modeled tutoring spending fell by about ¥5,069 per pupil across five school years.</p><p>We do not know whether performance-based re-banding became more common after 2021. This comparison is not an estimate of the causal effect of Double Reduction.</p></section>
      <section className="gz-section"><p className="gz-kicker">OPEN RESEARCH</p><h2>Help improve the assumptions</h2><p>The most valuable evidence would connect entrance scores, class and teacher assignments, tutoring, family resources and later results. The parameter register identifies the ranges and their sources. Contributions with a clear population, year, units and source are welcome.</p><div className="gz-actions"><a className="gz-primary" href="research/guangzhou/paper.pdf">Read the paper</a><a href={release}>Code, proofs and synthetic data ↗</a><a href="https://github.com/TreyModels/atlas-of-education/issues">Suggest evidence ↗</a></div></section>
    </div>
  </main>
}
