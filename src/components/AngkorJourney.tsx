import { useEffect, useRef, useState } from 'react'
import type { Translate } from '../types'
import { journey as angkorJourney, purposeLabel, stateLabel, claimLabel } from '../data/angkor-journey'
import type { Journey, ModelCard, Para } from '../data/angkor-journey'
import { BetaExplorer } from './BetaExplorer'
import './../journey.css'

/** One narrated paragraph, tagged with the kind of claim it makes. */
function Paragraph({ p, t }: { p: Para; t: Translate }) {
  return <p className={`journey-para claim-${p.claim ?? 'none'}`}>
    {p.claim && <span className="journey-claim">{t(claimLabel[p.claim])}</span>}
    {p.claim ? ' ' : null}
    {t(p.text)}
  </p>
}

/** One model, labelled by why it exists and how far it has been checked. */
function ModelCardView({ m, t, navigate, journey }: { m: ModelCard; t: Translate; navigate: (id: string) => void; journey: Journey }) {
  const purpose = purposeLabel[m.purpose]
  const state = stateLabel[m.state]
  return <article className="journey-card">
    <h4>{t(m.title)}</h4>
    <p className="journey-card-badges">
      <span className={`badge purpose-${m.purpose}`} title={t(purpose.help)}>{t(purpose.label)}</span>
      <span className={`badge state-${m.state}`} title={t(state.help)}>{t(state.label)}</span>
    </p>
    <p className="journey-card-note">{t(m.note)}</p>
    <p className="journey-card-actions">
      {m.route && <button className="button" onClick={() => navigate(m.route!)}>{t('Open workbench')}</button>}
      {m.engine && <a href={m.engine} download>{t('Download code')}</a>}
      {m.research && <a href={m.research}>{t('Notes')}</a>}
      <a target="_blank" rel="noopener" href={`${journey.repo}/issues/new?template=propose-a-version.yml&title=${encodeURIComponent(`Version: ${journey.family}/` + m.id)}`}>{t('Propose a version')}</a>
    </p>
  </article>
}

function cardsFor(journey: Journey, ids: string[]): ModelCard[] {
  return ids.map(id => journey.models[id]).filter((m): m is ModelCard => Boolean(m))
}

/** Narrated family page. Angkor is the default; other families pass their own journey. */
export function AngkorJourney({ t, navigate, journey = angkorJourney }: { t: Translate; navigate: (id: string) => void; journey?: Journey }) {
  const [active, setActive] = useState<string>(journey.chapters[0]?.id ?? '')
  const visible = useRef(new Map<string, boolean>())

  useEffect(() => {
    if (typeof IntersectionObserver === 'undefined') return
    const sections = journey.chapters
      .map(c => document.getElementById(`ch-${c.id}`))
      .filter((el): el is HTMLElement => el !== null)
    if (sections.length === 0) return
    const observer = new IntersectionObserver((entries) => {
      for (const entry of entries) visible.current.set(entry.target.id, entry.isIntersecting)
      const current = journey.chapters.find(c => visible.current.get(`ch-${c.id}`))
      if (current) setActive(current.id)
    }, { rootMargin: '-45% 0px -45% 0px', threshold: 0 })
    sections.forEach(section => observer.observe(section))
    return () => observer.disconnect()
  }, [])

  return <main id="main-content" className="journey-page">
    <header className="journey-hero">
      <p className="eyebrow">{t(journey.kicker)}</p>
      <h1>{t(journey.title)}</h1>
      <p className="journey-lede">{t(journey.lede)}</p>
      <div className="journey-why">
        {journey.why.map((p, index) => <Paragraph key={index} p={p} t={t} />)}
      </div>
    </header>

    <nav className="journey-nav" aria-label={t('Chapters')}>
      <ul>
        {journey.chapters.map(c => <li key={c.id}>
          <a
            href={`#ch-${c.id}`}
            aria-current={active === c.id ? 'true' : undefined}
            onClick={event => {
              event.preventDefault()
              setActive(c.id)
              document.getElementById(`ch-${c.id}`)?.scrollIntoView({ behavior: 'smooth', block: 'start' })
            }}
          >
            <span className="journey-nav-kicker">{t(c.kicker)}</span>
            <span className="journey-nav-title">{t(c.title)}</span>
          </a>
        </li>)}
      </ul>
    </nav>

    {journey.chapters.map(c => <section key={c.id} id={`ch-${c.id}`} className="journey-chapter">
      <p className="journey-kicker">{t(c.kicker)}</p>
      <h2>{t(c.title)}</h2>
      <p className="journey-question">{t(c.question)}</p>

      <div className="journey-block">
        <h3>{t('What the evidence says')}</h3>
        {c.evidence.map((p, index) => <Paragraph key={index} p={p} t={t} />)}
      </div>

      <div className="journey-block">
        <h3>{t('The rule we wrote')}</h3>
        {c.rule.map((p, index) => <Paragraph key={index} p={p} t={t} />)}
      </div>

      <div className="journey-block">
        <h3>{t('What the experiment shows')}</h3>
        {c.result.map((p, index) => <Paragraph key={index} p={p} t={t} />)}
      </div>

      {c.interactive === 'beta' && <BetaExplorer t={t} />}

      <div className="journey-block">
        <h3>{t('Limits')}</h3>
        {c.limitation.map((p, index) => <Paragraph key={index} p={p} t={t} />)}
      </div>

      {c.maths && <details className="journey-maths">
        <summary>{t('How the maths works')}</summary>
        <p>{t(c.maths.plain)}</p>
        {c.maths.formula && <pre><code>{t(c.maths.formula)}</code></pre>}
        {c.maths.symbols && c.maths.symbols.length > 0 && <dl>
          {c.maths.symbols.map(([symbol, meaning]) => <div key={symbol}>
            <dt>{symbol}</dt>
            <dd>{t(meaning)}</dd>
          </div>)}
        </dl>}
        {c.maths.example && <p>{t(c.maths.example)}</p>}
      </details>}

      {c.sources.length > 0 && <ul className="journey-sources">
        {c.sources.map(source => {
          const external = source.href.startsWith('http')
          return <li key={source.href}>
            <a href={source.href} {...(external ? { target: '_blank', rel: 'noopener' } : {})}>{t(source.label)}</a>
          </li>
        })}
      </ul>}

      <div className="journey-cards">
        {cardsFor(journey, c.models).map(m => <ModelCardView key={m.id} m={m} t={t} navigate={navigate} journey={journey} />)}
      </div>
    </section>)}

    <section className="journey-deeper">
      <h2>{t('Deeper experiments')}</h2>
      <div className="journey-cards">
        {cardsFor(journey, journey.deeper).map(m => <ModelCardView key={m.id} m={m} t={t} navigate={navigate} journey={journey} />)}
      </div>
    </section>

    <aside className="journey-bottomline">
      <p>{t(journey.bottomLine)}</p>
    </aside>

    <section className="journey-download">
      <h2>{t('Download and adapt')}</h2>
      <p>{t('Everything here, the models, their data and these notes, lives in one repository. Download it, run a model, and change a rule to see what carries the result.')}</p>
      <p>
        <a href={journey.repo} target="_blank" rel="noopener">{t('The repository on GitHub')}</a>
        {' · '}
        <a href={`${journey.repo}/archive/refs/heads/main.zip`} target="_blank" rel="noopener">{t('Download the code (zip)')}</a>
      </p>
    </section>
  </main>
}
