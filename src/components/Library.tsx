import { useEffect, useMemo, useState } from 'react'
import { ArrowRight, ArrowUpRight, BookOpen, Search, X } from 'lucide-react'
import type { Translate } from '../types'
import { catalogue, classicLabs, familyCounts, familyInfo, familyItems, totalModels, type CatalogueItem, type ModelFamily } from '../data/model-catalogue'

import { modelFamilies } from '../data/model-catalogue'
const families = modelFamilies
const sectionIds: Record<ModelFamily, string> = {
  education: 'education-models', systems: 'school-systems', planning: 'planning-lab', angkor: 'angkor-case', fertility: 'fertility-models', shadow: 'shadow-models', deephistory: 'deep-history',
}

export function ModelLink({ item, t, navigate }: { item: CatalogueItem; t: Translate; navigate: (id: string) => void }) {
  const content = <>
    <span className="catalogue-item-copy">
      <span className="catalogue-item-meta">{t(item.method)}<i>·</i>{t(item.format)}</span>
      <strong>{t(item.title)}</strong>
      <span className="catalogue-item-question">{t(item.question)}</span>
    </span>
    <span className="catalogue-item-action">{t('Open entry')}{item.href ? <ArrowUpRight size={18} /> : <ArrowRight size={18} />}</span>
  </>
  const external = item.href?.startsWith('http')
  return <li className="catalogue-item">
    {item.href
      ? <a href={item.href} {...(external ? { target: '_blank', rel: 'noreferrer' } : {})}>{content}</a>
      : <button onClick={() => navigate(item.route!)}>{content}</button>}
  </li>
}

export function Library({ t, navigate }: { t: Translate; navigate: (id: string) => void }) {
  const [active, setActive] = useState<ModelFamily | 'all'>('all')
  const [query, setQuery] = useState('')
  const [classicOnly, setClassicOnly] = useState(false)
  useEffect(() => {
    const syncSection = (section?: string) => {
      const family = families.find(id => sectionIds[id] === section)
      if (family) { setActive(family); setClassicOnly(false) }
      if (section === 'catalogue') setActive('all')
    }
    const onHash = () => syncSection(window.location.hash.split('/')[1])
    const onNavigate = (event: Event) => syncSection((event as CustomEvent<string>).detail)
    onHash()
    window.addEventListener('hashchange', onHash)
    window.addEventListener('atlas:section', onNavigate)
    return () => { window.removeEventListener('hashchange', onHash); window.removeEventListener('atlas:section', onNavigate) }
  }, [])
  const visible = useMemo(() => {
    const needle = query.trim().toLowerCase()
    return catalogue.filter(item =>
      (active === 'all' || item.family === active) &&
      (!classicOnly || item.format === 'Classic workbench') &&
      (!needle || `${item.title} ${item.question} ${item.method} ${item.keywords ?? ''} ${t(item.title)} ${t(item.question)} ${t(item.method)} ${t(familyInfo[item.family].short)}`.toLowerCase().includes(needle)),
    )
  }, [active, query, classicOnly, t])
  const visibleFamilies = families.filter(family => active === 'all' || active === family)
  const choose = (family: ModelFamily | 'all') => {
    setActive(family)
    if (family !== 'all') requestAnimationFrame(() => document.getElementById(sectionIds[family])?.scrollIntoView({ block: 'start' }))
  }

  return <main id="main-content">
    <section className="landing-hero shell">
      <p className="eyebrow">{t('COMPUTATIONAL SOCIAL SCIENCE · BY TREY MENEFEE')}</p>
      <h1>{t('Social science you can run.')}</h1>
      <p className="landing-lede">{t('These are simulations of how societies work: why families pay for tutoring, why fertility collapsed across East Asia, why Angkor declined, how people walked out of Africa. Each one turns an argument into rules a computer can play out, thousands of times. Change the assumptions, run it, and see whether the story still holds.')}</p>
      <div className="hero-actions">
        <button className="button button-primary" onClick={() => document.getElementById('questions')?.scrollIntoView({ block: 'start' })}>{t('Start with a question')}<ArrowRight size={18} /></button>
        <a className="text-link" href="https://comparativist.substack.com" target="_blank" rel="noreferrer">{t('Read the essays on The Comparativist')}<ArrowUpRight size={16} /></a>
      </div>
    </section>

    <section className="landing-steps shell" aria-label={t('How it works')}>
      <ol>
        <li><span>1</span><strong>{t('Pick a question')}</strong><p>{t('Each collection starts from a real puzzle and a short story of what the models found.')}</p></li>
        <li><span>2</span><strong>{t('Change the assumptions')}</strong><p>{t('Move the sliders: school fees, sea level, teacher pay, rainfall. Everything runs in your browser, nothing is sent anywhere.')}</p></li>
        <li><span>3</span><strong>{t('See what holds up')}</strong><p>{t('Every finding is labelled: measured from data, produced by a simulation, ruled out, or still open.')}</p></li>
      </ol>
    </section>

    <section className="landing-questions shell" id="questions">
      <div className="landing-section-head"><p className="eyebrow">{t('START WITH A QUESTION')}</p><h2>{t('{n} puzzles, {m} models.').replace('{n}', String(families.length)).replace('{m}', String(totalModels))}</h2></div>
      <div className="question-grid">
        {families.map(family => <button key={family} className={`question-card question-${family}`} onClick={() => navigate(`story-${family}`)}>
          <span className="question-meta">{t(familyInfo[family].short)}<i>·</i>{familyCounts[family]}</span>
          <strong>{t(familyInfo[family].question)}</strong>
          <span className="question-go">{t('Read what the models found')}<ArrowRight size={15} /></span>
        </button>)}
      </div>
    </section>

    <section className="landing-methods shell">
      <div className="landing-section-head"><p className="eyebrow">{t('HOW TO READ THESE MODELS')}</p><h2>{t('No equations required.')}</h2></div>
      <dl>
        <div><dt>{t('Agent-based models')}</dt><dd>{t('Give thousands of simulated people, teachers or households simple rules, let them interact, and watch what patterns emerge at the level of the whole society.')}</dd></div>
        <div><dt>{t('Monte Carlo')}</dt><dd>{t('When we do not know an input, say how fast people walked, we draw it at random from a plausible range and run the model again. Hundreds of runs show which conclusions survive our ignorance and which depend on one guess.')}</dd></div>
        <div><dt>{t('Fitting to evidence')}</dt><dd>{t('Keep only the simulated worlds that reproduce what we actually observe, then ask what those surviving worlds have in common.')}</dd></div>
      </dl>
    </section>

    <section className="catalogue-browser shell" id="catalogue">
      <div className="catalogue-intro">
        <div><p className="eyebrow">{t('THE FULL LIBRARY')}</p><h2>{t('Every model, searchable.')}</h2></div>
        <p>{t('Interactive models open here. Entries marked with ↗ open a standalone lab, a full write-up or a code-and-data download.')}</p>
      </div>

      <div className="collection-tabs" role="group" aria-label={t('Filter by collection')}>
        <button className={active === 'all' ? 'active' : ''} aria-pressed={active === 'all'} onClick={() => choose('all')}><span>{t('All entries')}</span><strong>{totalModels}</strong></button>
        {families.map(family => <button key={family} className={active === family ? 'active' : ''} aria-pressed={active === family} onClick={() => choose(family)}><span>{t(familyInfo[family].short)}</span><strong>{familyCounts[family]}</strong></button>)}
      </div>

      <div className="catalogue-tools">
        <label className="library-search"><Search size={18} /><input type="search" value={query} onChange={event => setQuery(event.target.value)} placeholder={t('Search a country, question, or method')} aria-label={t('Search the complete model library')} />{query && <button onClick={() => setQuery('')} aria-label={t('Clear search')}><X size={17} /></button>}</label>
        <label className="classic-filter"><input type="checkbox" checked={classicOnly} onChange={event => setClassicOnly(event.target.checked)} /><span>{t('Classic workbenches only')}</span></label>
        <output className="catalogue-result-count">{visible.length} {t('of {n}').replace('{n}', String(totalModels))}</output>
      </div>

      {visible.length === 0 && <div className="catalogue-empty"><h3>{t('No models match this view.')}</h3><p>{t('Try a broader country, topic or method, or reset the filters.')}</p><button className="button button-secondary" onClick={() => { setQuery(''); setActive('all'); setClassicOnly(false) }}>{t('Show the complete library')}</button></div>}

      {visibleFamilies.map(family => {
        const items = familyItems(family).filter(item => visible.includes(item))
        if (!items.length) return null
        const info = familyInfo[family]
        return <section className={`catalogue-family catalogue-family-${family}`} id={sectionIds[family]} key={family}>
          <header className="catalogue-family-heading">
            <div className="family-title"><span>{String(families.indexOf(family) + 1).padStart(2, '0')} / {items.length}</span><h2>{t(info.title)}</h2></div>
            <div><h3>{t(info.question)}</h3><p>{t(info.description)}</p><button className="text-link" onClick={() => navigate(`story-${family}`)}>{t('Read the class story')}<ArrowRight size={15} /></button>{family === 'angkor' && <button className="text-link" onClick={() => navigate('angkor-guide')}>{t('Start with the guided sequence')}<ArrowRight size={15} /></button>}</div>
          </header>
          <ul className="catalogue-items">{items.map(item => <ModelLink key={item.id} item={item} t={t} navigate={navigate} />)}</ul>
        </section>
      })}
    </section>

    <section className="classic-labs shell">
      <div className="classic-labs-heading"><p className="eyebrow">{t('ORIGINAL IMPLEMENTATIONS')}</p><h2>{t('Standalone laboratories')}</h2><p>{t('Alternative interfaces and methods studios. These complement the {n} catalogue entries rather than inflating the count.').replace('{n}', String(totalModels))}</p></div>
      <div className="classic-labs-list">{classicLabs.map(lab => <a href={lab.href} key={lab.href}><span>{t(lab.label)}</span><strong>{t(lab.title)}</strong><p>{t(lab.description)}</p><ArrowUpRight size={19} /></a>)}</div>
    </section>

    <section className="shell library-foot">
      <div className="library-notes">
        <BookOpen size={22} />
        <p>{t('The shared model library is translated. Classic workbenches, linked publications and archived research files retain their original language and interface.')}</p>
        <a href="research/index.html">{t('Research library')}<ArrowUpRight size={16} /></a>
      </div>
    </section>
  </main>
}
