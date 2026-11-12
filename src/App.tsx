import { useCallback, useEffect, useState } from 'react'
import { ArrowUpRight } from 'lucide-react'
import { worlds } from './models'
import { translate } from './lib/i18n'
import type { Language, Values } from './types'
import { Catalogue } from './components/Catalogue'
import { SchoolFutures, schoolFutures, type SchoolFuturesRoute } from './components/SchoolFutures'
import { Library } from './components/Library'
import { Guide } from './components/Guide'
import { Navigation } from './components/Navigation'
import { Workbench } from './components/Workbench'
import { StoryPage } from './components/StoryPage'
import { modelFamilies, type ModelFamily } from './data/model-catalogue'
import { familyStories } from './data/family-stories'
import './App.css'
import './education.css'
import './navigation.css'
import { parseLocation, sectionHash, sections, preserveHandoff } from './lib/navigation'

export default function App() {
  const [route, setRoute] = useState(() => parseLocation(window.location.hash).route)
  const [language, setLanguage] = useState<Language>(() => {
    try {
      const requested = new URLSearchParams(location.search).get('lang')
      const saved = requested || localStorage.getItem('atlas-language')
      return saved === 'zh-Hans' || saved === 'vi' ? saved : 'en'
    } catch { return 'en' }
  })
  const [states, setStates] = useState<Record<string, Values>>({})
  const t = useCallback((value: string) => translate(value, language), [language])
  const world = worlds.find(item => item.id === route)
  const schoolRoute = Object.hasOwn(schoolFutures, route) ? route as SchoolFuturesRoute : undefined
  const storyFamily = route.startsWith('story-') && modelFamilies.includes(route.slice(6) as ModelFamily) ? route.slice(6) as ModelFamily : undefined

  useEffect(() => {
    const update = () => {
      const location = parseLocation(window.location.hash)
      setRoute(location.route)
      if (location.section) requestAnimationFrame(() => {
        const el = document.getElementById(location.section)
        el?.setAttribute('tabindex', '-1'); el?.focus({ preventScroll: true }); el?.scrollIntoView({ block: 'start' })
      })
    }
    window.addEventListener('hashchange', update); window.addEventListener('popstate', update)
    return () => { window.removeEventListener('hashchange', update); window.removeEventListener('popstate', update) }
  }, [])

  useEffect(() => {
    document.documentElement.lang = language
    document.title = storyFamily ? `${t(familyStories[storyFamily].title)} · ${t('Atlas of Education')}` : schoolRoute ? `${t(schoolFutures[schoolRoute].title)} · ${t('Atlas of Education')}` : route === 'catalogue' ? `${t('Atlas of Models')} · ${t('Atlas of Education')}` : world ? `${t(world.title)} · ${t('Atlas of Education')}` : route === 'angkor-guide' ? `${t('ANGKOR · A GUIDED RECONSTRUCTION')} · ${t('Atlas of Education')}` : `${t('Atlas of Education')} · ${t('Model Lab')}`
    try { localStorage.setItem('atlas-language', language) } catch { /* Browser storage may be unavailable. */ }
  }, [language, world, route, schoolRoute, storyFamily, t])

  useEffect(() => {
    const section = parseLocation(window.location.hash).section
    if (!section) return
    const focus = () => {
      const el = document.getElementById(section)
      if (!el) return false
      el.setAttribute('tabindex', '-1'); el.focus({ preventScroll: true }); el.scrollIntoView({ block: 'start' }); return true
    }
    if (focus()) return
    const observer = new MutationObserver(() => { if (focus()) observer.disconnect() })
    observer.observe(document.body, { subtree: true, childList: true })
    return () => observer.disconnect()
  }, [route])

  const navigate = useCallback((id: string) => {
    const target = parseLocation('#' + id)
    window.dispatchEvent(new CustomEvent('atlas:section', { detail: target.section }))
    if (window.location.hash.slice(1) === id) {
      setRoute(target.route)
      if (target.section) requestAnimationFrame(() => document.getElementById(target.section)?.scrollIntoView({ block: 'start' }))
    } else window.location.hash = id
    if (!target.section) window.scrollTo({ top: 0, behavior: 'instant' })
  }, [])

  const handoff = (values: Values) => {
    const obligations = worlds.find(item => item.id === 'obligations')!
    setStates(previous => ({ ...previous, obligations: { ...preserveHandoff(obligations.defaults, previous.obligations, values) } }))
    navigate('obligations')
  }

  return <div className="app" onClick={event => {
    const link = (event.target as Element).closest('a[href^="#"]')
    if (!link) return
    const section = link.getAttribute('href')!.slice(1)
    if (!sections.has(section)) return
    event.preventDefault(); history.pushState(null, '', sectionHash(route, section))
    const el = document.getElementById(section); el?.setAttribute('tabindex', '-1'); el?.focus({ preventScroll: true }); el?.scrollIntoView({ block: 'start' })
  }}>
    <a className="skip-link" href="#main-content">{t('Skip to content')}</a>
    <Navigation route={route} navigate={navigate} t={t} language={language} setLanguage={setLanguage} />
    <div className="app-main">
      {!route && <Library t={t} navigate={navigate} />}
      {schoolRoute && <SchoolFutures key={schoolRoute} route={schoolRoute} navigate={navigate} t={t} language={language} />}
      {route === 'catalogue' && <Catalogue t={t} language={language} />}
      {route === 'angkor-guide' && <Guide t={t} navigate={navigate} />}
      {storyFamily && <StoryPage family={storyFamily} t={t} navigate={navigate} />}
      {world && <Workbench key={world.id} world={world} values={states[world.id] ?? world.defaults} onChange={values => setStates(previous => ({ ...previous, [world.id]: values }))} onReset={() => setStates(previous => { const next = { ...previous }; delete next[world.id]; return next })} onHandoff={handoff} navigate={navigate} t={t} />}
      {route && route !== 'angkor-guide' && route !== 'catalogue' && !storyFamily && !schoolRoute && !world && <Library t={t} navigate={navigate} />}
      <footer className="site-footer"><div className="shell"><span>{t('Atlas of Education')} · 2026</span><p>{t('Settings remain in this tab. Language is saved in this browser only.')}</p><p>{language === 'zh-Hans' ? '© 2026 Dr. Trey Menefee。使用或复制本作品时请注明并引用 Dr. Trey Menefee。仅限非商业用途；商业用途须事先获得许可。第三方材料可能适用其他条款。' : language === 'vi' ? '© 2026 Dr. Trey Menefee. Vui lòng ghi công và trích dẫn Dr. Trey Menefee khi sử dụng hoặc sao chép tác phẩm. Chỉ sử dụng phi thương mại; sử dụng thương mại cần được cho phép trước. Điều khoản của bên thứ ba có thể được áp dụng.' : '© 2026 Dr. Trey Menefee. Credit and cite Dr. Trey Menefee when using or reproducing this work. Noncommercial use only; commercial use requires prior permission. Third-party terms may apply.'} <a href="LICENSE.txt">{language === 'zh-Hans' ? '使用条款' : language === 'vi' ? 'Điều khoản sử dụng' : 'Reuse terms'}</a></p><a href="reference/education/index.html">{t('Full Education Atlas')}<ArrowUpRight size={14} /></a></div></footer>
    </div>
  </div>
}
