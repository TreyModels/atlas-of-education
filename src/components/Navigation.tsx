import { useEffect, useMemo, useRef, useState } from 'react'
import { ArrowRight, ArrowUpRight, Baby, BookOpen, ChevronDown, FlaskConical, GraduationCap, Home, Landmark, Menu, Network, School, Search, X } from 'lucide-react'
import { worlds } from '../models'
import type { Language, Translate } from '../types'
import { catalogue, familyInfo } from '../data/model-catalogue'

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
  return <button className="brand" onClick={onClick} aria-label={t('Atlas of Education home')}>
    <span className="brand-mark" aria-hidden="true"><i /><i /><i /></span>
    <span>{t('Atlas of Education')}<small>{t('Model Lab')}</small></span>
  </button>
}

function LanguagePicker({ language, setLanguage }: Pick<NavigationProps, 'language' | 'setLanguage'>) {
  return <label className="language-picker">
    <span className="sr-only">Language / 语言</span>
    <select aria-label="Language / 语言" value={language} onChange={event => setLanguage(event.target.value as Language)}>
      <option value="en">EN</option><option value="zh-Hans">中文</option><option value="vi">Tiếng Việt</option>
    </select><ChevronDown size={13} aria-hidden="true" />
  </label>
}

export function Navigation({ route, navigate, t, language, setLanguage }: NavigationProps) {
  const [drawerOpen, setDrawerOpen] = useState(false)
  const [searchOpen, setSearchOpen] = useState(false)
  const [query, setQuery] = useState('')
  const searchInput = useRef<HTMLInputElement>(null)
  const family = familyFor(route)
  const activeWorld = worlds.find(world => world.id === route)

  const results = useMemo(() => {
    const needle = query.trim().toLowerCase()
    return catalogue.filter(model => !needle || `${model.title} ${model.question} ${model.method} ${model.keywords ?? ''}`.toLowerCase().includes(needle))
  }, [query])

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

  useEffect(() => {
    document.body.style.overflow = drawerOpen || searchOpen ? 'hidden' : ''
    if (searchOpen) requestAnimationFrame(() => searchInput.current?.focus())
    return () => { document.body.style.overflow = '' }
  }, [drawerOpen, searchOpen])

  const go = (id: string) => { navigate(id); setDrawerOpen(false); setSearchOpen(false) }
  const primary = [
    { id: '', label: 'Overview', icon: Home, family: 'home' },
    { id: 'story-education', label: familyInfo.education.short, icon: GraduationCap, family: 'education' },
    { id: 'story-systems', label: familyInfo.systems.short, icon: Network, family: 'systems' },
    { id: 'story-planning', label: familyInfo.planning.short, icon: FlaskConical, family: 'planning' },
    { id: 'story-angkor', label: familyInfo.angkor.short, icon: Landmark, family: 'angkor' },
    { id: 'story-fertility', label: familyInfo.fertility.short, icon: Baby, family: 'fertility' },
    { id: 'story-shadow', label: familyInfo.shadow.short, icon: School, family: 'shadow' },
  ]

  const navContent = <>
    <nav className="primary-nav" aria-label={t('Primary navigation')}>
      <p className="nav-label">{t('Explore')}</p>
      {primary.map(item => <button key={item.family} className={family === item.family ? 'active' : ''} aria-current={family === item.family ? 'page' : undefined} onClick={() => go(item.id)}>
        <item.icon size={18} strokeWidth={1.7} /><span>{t(item.label)}</span>{family === item.family && <span className="nav-active-dot" />}
      </button>)}
    </nav>
    <button className="all-models-link" onClick={() => { setDrawerOpen(false); setSearchOpen(true) }}><Search size={17} /><span>{t('Find a model')}</span><span className="model-total">{catalogue.length}</span></button>
    <div className="nav-resources">
      <p className="nav-label">{t('Resources')}</p>
      <button className={route === 'catalogue' ? 'active' : ''} onClick={() => go('catalogue')}><BookOpen size={17} /><span>{t('Research catalogue')}</span></button>
      <a href="research/index.html"><ArrowUpRight size={17} /><span>{t('Research library')}</span></a>
      <a href="research/fertility.html"><ArrowUpRight size={17} /><span>{t('Fertility collapse lab')}</span></a>
      <a href="research/shadow-education.html"><ArrowUpRight size={17} /><span>{t('Shadow education lab')}</span></a>
      <a href="reference/education/index.html"><ArrowUpRight size={17} /><span>{t('Full Education Atlas')}</span></a>
    </div>
  </>

  return <>
    <aside className="desktop-rail">
      <div className="rail-brand"><Brand onClick={() => go('')} t={t} /></div>
      <div className="rail-scroll">{navContent}</div>
      <div className="rail-current">
        <span>{t(activeWorld ? 'Current model' : 'Interactive atlas')}</span>
        <strong>{activeWorld ? t(activeWorld.nav) : t('{n} catalogue entries · 3 languages').replace('{n}', String(catalogue.length))}</strong>
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
        <div className="model-search-input"><Search size={21} /><input ref={searchInput} type="search" value={query} onChange={event => setQuery(event.target.value)} placeholder={t('Search models, questions, or topics')} aria-label={t('Search models')} /><button className="icon-button" onClick={() => setSearchOpen(false)} aria-label={t('Close search')}><X size={20} /></button></div>
        <div className="search-meta"><span>{query ? t('Matching models') : t('All interactive models')}</span><span>{results.length}</span></div>
        <div className="search-results">
          {results.map(model => {
            const content = <><span><small>{t(familyInfo[model.family].short)} · {t(model.format)}</small><strong>{t(model.title)}</strong><span>{t(model.question)}</span></span>{model.href ? <ArrowUpRight size={19} /> : <ArrowRight size={19} />}</>
            return model.href
              ? <a key={model.id} href={model.href} onClick={() => setSearchOpen(false)}>{content}</a>
              : <button key={model.id} onClick={() => go(model.route!)}>{content}</button>
          })}
          {!results.length && <div className="search-empty"><strong>{t('No models found')}</strong><p>{t('Try a broader topic, such as teachers, climate, or work.')}</p></div>}
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
