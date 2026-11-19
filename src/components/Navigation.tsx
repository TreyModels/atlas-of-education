import { useEffect, useMemo, useRef, useState } from 'react'
import { ArrowRight, ArrowUpRight, Baby, BookOpen, Building2, Columns2, Footprints, ChevronDown, FlaskConical, Globe2, GraduationCap, Home, Landmark, Menu, Network, School, Search, X } from 'lucide-react'
import { worlds } from '../models'
import type { Language, Translate } from '../types'
import { allTags, broadTags, catalogue, familyGroups, familyInfo, specificTags, statusTags, tagCounts, typeTags } from '../data/model-catalogue'
import { tagGroup } from '../data/model-tags'
import { addTag, hasQuery, matchesQuery, parseTags, removeTag } from '../lib/search'
import '../hashtags.css'

type Navigate = (id: string) => void

type NavigationProps = {
  route: string
  navigate: Navigate
  t: Translate
  language: Language
  setLanguage: (language: Language) => void
}

const familyFor = (route: string) => {
  if (route === 'angkor-guide') return 'angkor'
  if (route.startsWith('story-')) return route.slice(6)
  const item = catalogue.find(model => model.route === route)
  if (item) return item.family
  if (route === 'catalogue') return 'research'
  return 'home'
}

function Brand({ onClick, t }: { onClick: () => void; t: Translate }) {
  return <button className="brand" onClick={onClick} aria-label={t('Atlas Worlds home')}>
    <span className="brand-mark" aria-hidden="true"><i /><i /><i /></span>
    <span>{t('Atlas Worlds')}<small>{t('Model Lab')}</small></span>
  </button>
}

function LanguagePicker({ language, setLanguage }: Pick<NavigationProps, 'language' | 'setLanguage'>) {
  return <label className="language-picker">
    <Globe2 size={19} aria-hidden="true" />
    <span className="sr-only">Language / 语言 / Ngôn ngữ</span>
    <select aria-label="Language / 语言 / Ngôn ngữ" value={language} onChange={event => setLanguage(event.target.value as Language)}>
      <option value="en">English</option><option value="zh-Hans">简体中文</option>
    </select><ChevronDown size={13} aria-hidden="true" />
  </label>
}

export function Navigation({ route, navigate, t, language, setLanguage }: NavigationProps) {
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)
  const [query, setQuery] = useState('')
  const [allTagsOpen, setAllTagsOpen] = useState(false)
  const searchInput = useRef<HTMLInputElement>(null)
  const tagsPanel = useRef<HTMLDivElement>(null)
  const family = familyFor(route)
  const activeWorld = worlds.find(world => world.id === route)

  const results = useMemo(() => catalogue.filter(model => matchesQuery(model, query, t)), [query, t])
  const activeTags = parseTags(query)
  const previewBroad = allTagsOpen ? broadTags : broadTags.slice(0, 18)
  // Suggested tags are drawn from what is on screen, plain-language tags first.
  const suggestedTags = useMemo(() => {
    if (!hasQuery(query)) return []
    const counts = new Map<string, number>()
    for (const model of results) for (const tag of model.tags) if (!activeTags.includes(tag)) counts.set(tag, (counts.get(tag) ?? 0) + 1)
    return [...counts.entries()]
      .filter(([, count]) => count >= 2)
      .sort((a, b) => (tagGroup(a[0]) === 'broad' ? 0 : 1) - (tagGroup(b[0]) === 'broad' ? 0 : 1) || b[1] - a[1] || a[0].localeCompare(b[0]))
      .slice(0, 10)
      .map(([tag]) => tag)
  }, [results, query])

  useEffect(() => {
    setDrawerOpen(false)
    setSearchOpen(false)
    setQuery('')
  }, [route])

  useEffect(() => {
    const onKey = (event: KeyboardEvent) => {
      if (event.key === 'Escape') { setDrawerOpen(false); setSearchOpen(false) }
      if (event.key === '/' && !['INPUT', 'TEXTAREA', 'SELECT'].includes((event.target as HTMLElement).tagName)) {
        event.preventDefault(); setSearchOpen(true)
      }
    }
    window.addEventListener('keydown', onKey)
    return () => window.removeEventListener('keydown', onKey)
  }, [])

  // Cards and the workbench header open the Find-a-model modal with a #tag query.
  useEffect(() => {
    const open = (event: Event) => {
      const detail = (event as CustomEvent<string>).detail
      setQuery(typeof detail === 'string' ? detail : '')
      setSearchOpen(true)
    }
    window.addEventListener('atlas:search', open as EventListener)
    return () => window.removeEventListener('atlas:search', open as EventListener)
  }, [])

  useEffect(() => {
    document.body.style.overflow = drawerOpen || searchOpen ? 'hidden' : ''
    if (searchOpen) requestAnimationFrame(() => searchInput.current?.focus())
    return () => { document.body.style.overflow = '' }
  }, [drawerOpen, searchOpen])

  const go = (id: string) => { navigate(id); setDrawerOpen(false); setSearchOpen(false) }
  const primary = [
    { id: 'story-education', label: familyInfo.education.short, icon: GraduationCap, family: 'education' },
    { id: 'story-systems', label: familyInfo.systems.short, icon: Network, family: 'systems' },
    { id: 'story-planning', label: familyInfo.planning.short, icon: FlaskConical, family: 'planning' },
    { id: 'story-angkor', label: familyInfo.angkor.short, icon: Landmark, family: 'angkor' },
    { id: 'story-fertility', label: familyInfo.fertility.short, icon: Baby, family: 'fertility' },
    { id: 'story-shadow', label: familyInfo.shadow.short, icon: School, family: 'shadow' },
    { id: 'story-deephistory', label: familyInfo.deephistory.short, icon: Footprints, family: 'deephistory' },
    { id: 'story-politics', label: familyInfo.politics.short, icon: Building2, family: 'politics' },
    { id: 'story-extension', label: familyInfo.extension.short, icon: School, family: 'extension' },
  ]
  const workflowLabel = language === 'zh-Hans' ? '我的数字工作流程' : t('My digital workflow')

  const navContent = <>
    <nav className="primary-nav" aria-label={t('Primary navigation')}>
      <p className="nav-label">{t('Start here')}</p>
      <button className={route === 'about' ? 'active' : ''} aria-current={route === 'about' ? 'page' : undefined} onClick={() => go('about')}>
        <Landmark size={18} strokeWidth={1.7} /><span>{t('About')}</span>{route === 'about' && <span className="nav-active-dot" />}
      </button>
      <button className={route === 'how-models-work' ? 'active' : ''} aria-current={route === 'how-models-work' ? 'page' : undefined} onClick={() => go('how-models-work')}>
        <FlaskConical size={18} strokeWidth={1.7} /><span>{t('How models work')}</span>{route === 'how-models-work' && <span className="nav-active-dot" />}
      </button>
      <button className={route === 'workflow' ? 'active' : ''} aria-current={route === 'workflow' ? 'page' : undefined} onClick={() => go('workflow')}>
        <BookOpen size={18} strokeWidth={1.7} /><span>{workflowLabel}</span>{route === 'workflow' && <span className="nav-active-dot" />}
      </button>
      {familyGroups.map(group => <div className="nav-family-group" key={group.id}>
        <p className="nav-label">{t(group.title)}</p>
        {group.families.map(familyId => {
          const item = primary.find(entry => entry.family === familyId)
          if (!item) return null
          return <button key={item.family} className={family === item.family ? 'active' : ''} aria-current={family === item.family ? 'page' : undefined} onClick={() => go(item.id)}>
            <item.icon size={18} strokeWidth={1.7} /><span>{t(item.label)}</span>{family === item.family && <span className="nav-active-dot" />}
          </button>
        })}
      </div>)}
    </nav>
    <button className="all-models-link" onClick={() => { setDrawerOpen(false); setSearchOpen(true) }}><Search size={17} /><span>{t('Find a model')}</span><span className="model-total">{catalogue.length}</span></button>
    <div className="nav-resources">
      <p className="nav-label">{t('Resources')}</p>
      <button className={route === 'sector' ? 'active' : ''} aria-current={route === 'sector' ? 'page' : undefined} onClick={() => go('sector')}><Columns2 size={17} /><span>{t('Scenario Theatre')} · {t('Experimental')}</span></button>
      <button className={route === 'about' ? 'active' : ''} aria-current={route === 'about' ? 'page' : undefined} onClick={() => go('about')}><Landmark size={17} /><span>{t('About')}</span></button>
      <button className={route === 'how-models-work' ? 'active' : ''} aria-current={route === 'how-models-work' ? 'page' : undefined} onClick={() => go('how-models-work')}><FlaskConical size={17} /><span>{t('How models work')}</span></button>
      <button className={route === 'catalogue' ? 'active' : ''} onClick={() => go('catalogue')}><BookOpen size={17} /><span>{t('Research catalogue')}</span></button>
      <a href="research/index.html"><ArrowUpRight size={17} /><span>{t('Research library')}</span></a>
      <a href="research/fertility.html"><ArrowUpRight size={17} /><span>{t('Fertility collapse lab')}</span></a>
      <a href="research/shadow-education.html"><ArrowUpRight size={17} /><span>{t('Shadow education lab')}</span></a>
      <a href="research/out-of-africa.html"><ArrowUpRight size={17} /><span>{t('Coast or herds? Out of Africa')}</span></a>
      <a href="reference/education/index.html"><ArrowUpRight size={17} /><span>{t('Full Education Atlas')}</span></a>
    </div>
  </>

  return <>
    <aside className="desktop-rail">
      <div className="rail-brand"><Brand onClick={() => go('')} t={t} /></div>
      <div className="rail-scroll">{navContent}</div>
      <div className="rail-current">
        <span>{t(activeWorld ? 'Current model' : 'Interactive atlas')}</span>
        <strong>{activeWorld ? t(activeWorld.nav) : t('{n} catalogue entries · 2 languages').replace('{n}', String(catalogue.length))}</strong>
        <small>{t('Runs locally in your browser')}</small>
      </div>
    </aside>

    <header className="site-header">
      <div className="mobile-brand"><Brand onClick={() => go('')} t={t} /></div>
      <div className="header-context"><span>{t(family === 'home' ? 'Model library' : primary.find(item => item.family === family)?.label || 'Research catalogue')}</span>{activeWorld && <><span className="context-slash">/</span><strong>{t(activeWorld.nav)}</strong></>}</div>
      <div className="header-actions">
        <button className="search-trigger" onClick={() => setSearchOpen(true)}><Search size={17} /><span>{t('Find a model')}</span><kbd>/</kbd></button>
        <LanguagePicker language={language} setLanguage={setLanguage} />
        <button className="mobile-menu-button" onClick={() => setDrawerOpen(true)} aria-label={t('Open navigation')} aria-expanded={drawerOpen}><Menu size={22} /></button>
      </div>
    </header>

    {drawerOpen && <div className="drawer-layer" role="presentation" onMouseDown={event => { if (event.target === event.currentTarget) setDrawerOpen(false) }}>
      <section className="mobile-drawer" role="dialog" aria-modal="true" aria-label={t('Navigation menu')}>
        <div className="drawer-heading"><Brand onClick={() => go('')} t={t} /><button className="icon-button" onClick={() => setDrawerOpen(false)} aria-label={t('Close navigation')}><X size={22} /></button></div>
        <div className="drawer-scroll">{navContent}</div>
        <div className="drawer-language"><span>{t('Language')}</span><LanguagePicker language={language} setLanguage={setLanguage} /></div>
      </section>
    </div>}

    {searchOpen && <div className="search-layer" role="presentation" onMouseDown={event => { if (event.target === event.currentTarget) setSearchOpen(false) }}>
      <section className="model-search" role="dialog" aria-modal="true" aria-label={t('Find a model')}>
        <div className="model-search-input"><Search size={21} /><input ref={searchInput} type="search" value={query} onChange={event => setQuery(event.target.value)} placeholder={t('Search models, questions, or #tags')} aria-label={t('Search models')} /><button className="icon-button" onClick={() => setSearchOpen(false)} aria-label={t('Close search')}><X size={20} /></button></div>
        <div className="search-tags" ref={tagsPanel}>
          {activeTags.length > 0 && <div className="search-tag-row" aria-label={t('Active tags')}>{activeTags.map(tag => <button key={tag} className="tag-chip tag-chip-active" aria-pressed="true" onClick={() => setQuery(removeTag(query, tag))}>#{tag}<span aria-hidden="true"> ×</span></button>)}</div>}
          {!hasQuery(query)
            ? <div className="tag-browser">
                <p className="tag-browser-label">{t('Browse tags')}</p>
                <p className="tag-hint">{t('Try #economics, #education, #history, #jobs')}</p>
                <div className="tag-group">
                  <span className="tag-group-label">{t('Broad topics')}</span>
                  <div className="tag-cloud">{previewBroad.map(tag => <button key={tag} className="tag-chip tag-chip-broad" onClick={() => setQuery(addTag(query, tag))}>#{tag}<span className="tag-count">{tagCounts[tag]}</span></button>)}</div>
                </div>
                {allTagsOpen && <>
                  <div className="tag-group">
                    <span className="tag-group-label">{t('Specific topics')}</span>
                    <div className="tag-cloud">{specificTags.map(tag => <button key={tag} className="tag-chip" onClick={() => setQuery(addTag(query, tag))}>#{tag}<span className="tag-count">{tagCounts[tag]}</span></button>)}</div>
                  </div>
                  <div className="tag-group tag-group-compact">
                    <span className="tag-group-label">{t('Model type & status')}</span>
                    <div className="tag-cloud">{typeTags.map(tag => <button key={tag} className="tag-chip tag-chip-quiet" onClick={() => setQuery(addTag(query, tag))}>#{tag}<span className="tag-count">{tagCounts[tag]}</span></button>)}{statusTags.map(tag => <button key={tag} className="tag-chip tag-chip-quiet" onClick={() => setQuery(addTag(query, tag))}>#{tag}<span className="tag-count">{tagCounts[tag]}</span></button>)}</div>
                  </div>
                </>}
                <button className="tag-cloud-more" aria-expanded={allTagsOpen} onClick={() => { setAllTagsOpen(open => !open); requestAnimationFrame(() => { if (tagsPanel.current) tagsPanel.current.scrollTop = 0 }) }}>{allTagsOpen ? t('Fewer tags') : t('All {n} tags').replace('{n}', String(allTags.length))}</button>
              </div>
            : suggestedTags.length > 0 && <div className="search-tag-row" aria-label={t('Suggested tags')}><span className="tag-row-label">{t('Suggested tags')}</span>{suggestedTags.map(tag => <button key={tag} className="tag-chip" onClick={() => setQuery(addTag(query, tag))}>#{tag}</button>)}</div>}
        </div>
        <div className="search-meta"><span>{hasQuery(query) ? t('Matching models') : t('All interactive models')}</span><span>{results.length}</span></div>
        <div className="search-results">
          {results.map(model => {
            const content = <><span><small>{t(familyInfo[model.family].short)} · {t(model.format)}</small><strong>{t(model.title)}</strong><span>{t(model.question)}</span><span className="search-result-tags">{model.tags.slice(0, 4).map(tag => <span key={tag} className="tag-chip tag-chip-static">#{tag}</span>)}</span></span>{model.href ? <ArrowUpRight size={19} /> : <ArrowRight size={19} />}</>
            // File bundles (zip etc.) open their family page instead of downloading straight from search.
            const fileLink = !!model.href && /\.(zip|tgz|tar\.gz|csv|pdf|xlsx)(\?|#|$)/i.test(model.href)
            return model.href && !fileLink
              ? <a key={model.id} href={model.href} onClick={() => setSearchOpen(false)}>{content}</a>
              : <button key={model.id} onClick={() => go(fileLink ? `story-${model.family}` : model.route!)}>{content}</button>
          })}
          {!results.length && <div className="search-empty"><strong>{t('No models found')}</strong><p>{t('Try a broader topic, or a #tag such as #water or #teachers.')}</p></div>}
        </div>
        <div className="search-footer"><span>{t('Select a model to open its workbench')}</span><kbd>ESC</kbd></div>
      </section>
    </div>}

    <nav className="mobile-bottom-nav" aria-label={t('Quick navigation')}>
      <button className={family === 'home' ? 'active' : ''} onClick={() => go('')}><Home size={20} /><span>{t('Home')}</span></button>
      <button onClick={() => setSearchOpen(true)}><Search size={20} /><span>{t('Models')}</span></button>
      <button className={family === 'planning' ? 'active' : ''} onClick={() => go('home/planning-lab')}><FlaskConical size={20} /><span>{t('Planning')}</span></button>
      <button onClick={() => setDrawerOpen(true)}><Menu size={20} /><span>{t('Menu')}</span></button>
    </nav>
  </>
}
