import { useEffect, useMemo, useState } from 'react'
import { ArrowRight, ArrowUpRight, BookOpen, Search, X } from 'lucide-react'
import type { Translate } from '../types'
import { catalogue, classicLabs, experimentalInterfaces, familyCounts, familyGroups, familyInfo, familyItems, totalModels, type CatalogueItem, type ModelFamily } from '../data/model-catalogue'
import { statusIntro, familyStatus, callToAction } from '../data/site-status'
import { purposeLabel, stateLabel } from '../data/angkor-journey'
import { homeExplainer } from '../data/home-explainer'

import { modelFamilies } from '../data/model-catalogue'
const families = modelFamilies
const sectionIds: Record<ModelFamily, string> = {
  education: 'education-models', systems: 'school-systems', planning: 'planning-lab', angkor: 'angkor-case', fertility: 'fertility-models', shadow: 'shadow-models', deephistory: 'deep-history', politics: 'political-economy', extension: 'extension-field-schools',
}
const isDownloadItem = (item: CatalogueItem) => item.method.toLowerCase().includes('download')

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
  return <li className={`catalogue-item${isDownloadItem(item) ? ' catalogue-item-download' : ''}`}>
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

  const featured = familyStatus[0]
  const featuredInfo = familyInfo[featured.family as ModelFamily]
  const featuredItems = familyItems(featured.family as ModelFamily)
  const downloadsLabel = t('Downloads') === 'Downloads' && t('Home') === '首页' ? '下载' : t('Downloads')

  return <main id="main-content">
    <section className="landing-hero shell">
      <p className="eyebrow">{t('COMPUTATIONAL SOCIAL SCIENCE · BY TREY MENEFEE')}</p>
      <h1>{t('Social science you can run.')}</h1>
      <p className="landing-lede">{t('Explore questions about schools, families, cities and states through models you can inspect and change. Some reproduce published findings; others test proposed mechanisms or teach an idea. Each states its assumptions, results and limits. Start with a question, then follow the reasoning.')}</p>
      <div className="hero-actions">
        <button className="button button-primary" onClick={() => document.getElementById('questions')?.scrollIntoView({ block: 'start' })}>{t('Start with a question')}<ArrowRight size={18} /></button>
        <a className="text-link" href="https://comparativist.substack.com" target="_blank" rel="noreferrer">{t('Read the essays on The Comparativist')}<ArrowUpRight size={16} /></a>
        <button className="text-link" onClick={() => navigate('sector')}>{t('Try the Scenario Theatre')}<span className="experimental-chip">{t('Experimental')}</span><ArrowRight size={16} /></button>
      </div>
    </section>

    <section className="landing-section shell" aria-labelledby="home-what-title">
      <header className="landing-section-head">
        <h2 id="home-what-title">{t(homeExplainer.intro.title)}</h2>
        {homeExplainer.intro.paragraphs.map((paragraph, index) => <p key={index}>{t(paragraph)}</p>)}
      </header>
      <div className="hero-actions">
        <button className="button button-primary" onClick={() => navigate('how-models-work')}>{t('How models work')}<ArrowRight size={18} /></button>
        <button className="button button-secondary" onClick={() => navigate('about')}>{t('About')}<ArrowRight size={18} /></button>
        <a className="text-link" href="#home-status-title">{t('Read this first')}<ArrowRight size={16} /></a>
      </div>
    </section>

    <section className="landing-section shell" aria-labelledby="home-author-title">
      <header className="landing-section-head">
        <h2 id="home-author-title">{t(homeExplainer.author.title)}</h2>
        <p>{t(homeExplainer.author.paragraph)}</p>
      </header>
    </section>

    <section className="landing-section shell" aria-labelledby="home-how-it-works-title">
      <header className="landing-section-head">
        <h2 id="home-how-it-works-title">{t('How it works')}</h2>
      </header>
      <ol className="landing-steps">
        {homeExplainer.howItWorks.map((step, index) => <li key={index}>
          <span>{index + 1}</span>
          <strong>{t(step.title)}</strong>
          <p>{t(step.text)}</p>
        </li>)}
      </ol>
    </section>

    <section className="landing-section shell" aria-labelledby="home-how-to-read-title">
      <header className="landing-section-head">
        <h2 id="home-how-to-read-title">{t('How to read these models')}</h2>
      </header>
      <dl>
        {homeExplainer.howToRead.map((limit, index) => <div key={index}>
          <dt>{t(limit.title)}</dt>
          <dd>{t(limit.text)}</dd>
        </div>)}
      </dl>
    </section>

    <section className="landing-section shell" aria-labelledby="home-invitation-title">
      <header className="landing-section-head">
        <h2 id="home-invitation-title">{t(homeExplainer.invitation.title)}</h2>
        {homeExplainer.invitation.paragraphs.map((paragraph, index) => <p key={index}>{t(paragraph)}</p>)}
      </header>
    </section>

    <section className="home-featured shell" aria-labelledby="home-featured-title">
      <p className="eyebrow">{t('START WITH A QUESTION')}</p>
      <h2 id="home-featured-title">{t(featuredInfo.title)}</h2>
      <p className="home-featured-question">{t(featuredInfo.question)}</p>
      <p className="home-featured-status">{t(featured.line)}</p>
      <ol className="home-chapter-path">
        {featuredItems.slice(0, 4).map(item => <li key={item.id}>{t(item.title)}</li>)}
      </ol>
      <button className="button button-primary" onClick={() => navigate(featured.route)}>{t('Read what the models found')}<ArrowRight size={18} /></button>
    </section>

    <section className="home-status shell" aria-labelledby="home-status-title">
      <div className="landing-section-head">
        <p className="eyebrow">{t(statusIntro.kicker)}</p>
        <h2 id="home-status-title">{t(statusIntro.title)}</h2>
        <p>{t(statusIntro.text)}</p>
      </div>
      <ul className="home-status-grid">
        {familyStatus.map(status => {
          const info = familyInfo[status.family as ModelFamily]
          return <li key={status.family} className="home-status-item">
            <h3>{t(info.short)}</h3>
            <p>{t(status.line)}</p>
            <ul className="home-status-badges">
              {status.purposes.map(purpose => <li key={purpose}><span className={`badge purpose-${purpose}`}>{t(purposeLabel[purpose].label)}</span></li>)}
              {status.states.map(state => <li key={state}><span className={`badge state-${state}`}>{t(stateLabel[state].label)}</span></li>)}
            </ul>
            <button className="text-link" onClick={() => navigate(status.route)}>{t('Read what the models found')}<ArrowRight size={15} /></button>
          </li>
        })}
      </ul>
    </section>

    <section className="home-stories shell" id="questions" aria-labelledby="home-stories-title">
      <div className="landing-section-head">
        <p className="eyebrow">{t('START WITH A QUESTION')}</p>
        <h2 id="home-stories-title">{t('{n} collections, {m} catalogue entries.').replace('{n}', String(families.length)).replace('{m}', String(totalModels))}</h2>
      </div>
      <div className="home-story-groups">
        {familyGroups.map(group => <section className="home-story-group" key={group.id} aria-labelledby={`home-story-group-${group.id}`}>
          <h3 id={`home-story-group-${group.id}`} className="home-story-group-title">{t(group.title)}</h3>
          <ul className="home-story-grid home-story-group-grid">
            {familyStatus.filter(status => group.families.includes(status.family as ModelFamily)).map(status => {
              const family = status.family as ModelFamily
              const info = familyInfo[family]
              const items = familyItems(family)
              return <li key={family} className={`home-story-card${family === familyStatus[0].family ? ' home-story-card-featured' : ''}`}>
                <span className="home-story-count">{familyCounts[family]}</span>
                <h3>{t(info.title)}</h3>
                <p className="home-story-question">{t(info.question)}</p>
                <p className="home-story-status">{t(status.line)}</p>
                <ul className="home-status-badges">
                  {status.purposes.map(purpose => <li key={purpose}><span className={`badge purpose-${purpose}`}>{t(purposeLabel[purpose].label)}</span></li>)}
                  {status.states.map(state => <li key={state}><span className={`badge state-${state}`}>{t(stateLabel[state].label)}</span></li>)}
                </ul>
                <ol className="home-chapter-path">
                  {items.slice(0, 3).map(item => <li key={item.id}>{t(item.title)}</li>)}
                </ol>
                <button className="button button-secondary" onClick={() => navigate(status.route)}>{t('Read what the models found')}<ArrowRight size={16} /></button>
              </li>
            })}
          </ul>
        </section>)}
      </div>
      <p className="home-stories-more"><a className="text-link" href="#catalogue">{t('Every model, searchable.')}<ArrowRight size={15} /></a></p>
    </section>

    <section className="landing-steps shell" aria-label={t('How it works')}>
      <ol>
        <li><span>1</span><strong>{t('Pick a question')}</strong><p>{t('Each collection starts from a real puzzle and a short story of what the models found.')}</p></li>
        <li><span>2</span><strong>{t('Change the assumptions')}</strong><p>{t('Move the sliders: school fees, sea level, teacher pay, rainfall. Most interactive models run in your browser; downloadable Python models run on your own machine.')}</p></li>
        <li><span>3</span><strong>{t('See what holds up')}</strong><p>{t('Every finding is labelled: measured from data, produced by a simulation, ruled out, or still open.')}</p></li>
      </ol>
    </section>

    <section className="landing-methods shell">
      <div className="landing-section-head"><p className="eyebrow">{t('HOW TO READ THESE MODELS')}</p><h2>{t('Plain language first. Math when you want it.')}</h2></div>
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
        const modelItems = items.filter(item => !isDownloadItem(item))
        const downloadItems = items.filter(item => isDownloadItem(item))
        return <section className={`catalogue-family catalogue-family-${family}`} id={sectionIds[family]} key={family}>
          <header className="catalogue-family-heading">
            <div className="family-title"><span>{String(families.indexOf(family) + 1).padStart(2, '0')} / {items.length}</span><h2>{t(info.title)}</h2></div>
            <div><h3>{t(info.question)}</h3><p>{t(info.description)}</p><button className="text-link" onClick={() => navigate(`story-${family}`)}>{t('Read the class story')}<ArrowRight size={15} /></button>{family === 'angkor' && <button className="text-link" onClick={() => navigate('angkor-guide')}>{t('Start with the guided sequence')}<ArrowRight size={15} /></button>}</div>
          </header>
          {modelItems.length > 0 && <ul className="catalogue-items">{modelItems.map(item => <ModelLink key={item.id} item={item} t={t} navigate={navigate} />)}</ul>}
          {downloadItems.length > 0 && <div className="catalogue-downloads">
            <h3 className="catalogue-downloads-title">{downloadsLabel}</h3>
            <ul className="catalogue-items">{downloadItems.map(item => <ModelLink key={item.id} item={item} t={t} navigate={navigate} />)}</ul>
          </div>}
        </section>
      })}
    </section>

    <section className="classic-labs shell" id="experiments">
      <div className="classic-labs-heading"><p className="eyebrow">{t('EXPERIMENTAL INTERFACES')}</p><h2>{t('Experiments')}</h2><p>{t('Prototypes for comparing model runs. These are experimental interfaces, not additional models, and are not counted in the catalogue above.')}</p></div>
      <ul className="catalogue-items">{experimentalInterfaces.map(item => <ModelLink key={item.id} item={item} t={t} navigate={navigate} />)}</ul>
    </section>

    <section className="classic-labs shell">
      <div className="classic-labs-heading"><p className="eyebrow">{t('ORIGINAL IMPLEMENTATIONS')}</p><h2>{t('Standalone laboratories')}</h2><p>{t('Alternative interfaces and methods studios. These complement the {n} catalogue entries rather than inflating the count.').replace('{n}', String(totalModels))}</p></div>
      <div className="classic-labs-list">{classicLabs.map(lab => <a href={lab.href} key={lab.href}><span>{t(lab.label)}</span><strong>{t(lab.title)}</strong><p>{t(lab.description)}</p><ArrowUpRight size={19} /></a>)}</div>
    </section>

    <section className="home-cta shell" aria-labelledby="home-cta-title">
      <h2 id="home-cta-title">{t(callToAction.title)}</h2>
      <p>{t(callToAction.text)}</p>
      <ul className="home-cta-actions">
        {callToAction.actions.map(action => <li key={action.href}>
          <a className="button button-secondary" href={action.href} target="_blank" rel="noreferrer">{t(action.label)}<ArrowUpRight size={16} /></a>
        </li>)}
      </ul>
      <footer className="home-licence"><p>{t(callToAction.licence)}</p></footer>
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
