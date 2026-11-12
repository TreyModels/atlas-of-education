import { useEffect, useRef, useState } from 'react'
import type { Language, Translate } from '../types'

const base = 'reference/east-asia-schools/'
export const schoolFutures = {
  'school-futures': {
    title: 'East Asia school and teacher futures',
    description: 'Compare enrollment, training, and teacher staffing through 2050.',
    file: 'index.html',
    notes: 'README.md',
  },
  'city-networks': {
    title: 'Hong Kong and Guangzhou school networks',
    description: 'Compare school operations, class sizes, and staffing under different policies.',
    file: 'city-networks.html',
    notes: 'CITY-NETWORKS.md',
  },
}
export type SchoolFuturesRoute = keyof typeof schoolFutures

export function SchoolFutures({ route, navigate, t, language }: {
  language: Language
  route: SchoolFuturesRoute
  navigate: (id: string) => void
  t: Translate
}) {
  const frame = useRef<HTMLIFrameElement>(null)
  // A generous initial height prevents a second, trapped scroll area before the child reports.
  const [height, setHeight] = useState(2400)
  const dashboard = schoolFutures[route]
  const dashboardUrl = base + dashboard.file + "?lang=" + language

  useEffect(() => {
    setHeight(2400)
    const requestHeight = () => frame.current?.contentWindow?.postMessage({ type: 'atlas-school-frame-request-height' }, '*')
    function receive(event: MessageEvent) {
      if (event.source !== frame.current?.contentWindow || event.origin !== 'null') return
      if (event.data?.type === 'atlas-school-frame-height') {
        const next = event.data.height
        if (Number.isFinite(next) && next > 0 && next < 100000) setHeight(Math.ceil(next + 2))
      }
      if (event.data?.type === 'atlas-school-frame-route' && event.data.route === 'city-networks') navigate('city-networks')
    }
    window.addEventListener('message', receive)
    window.addEventListener('resize', requestHeight)
    const retries = [0, 150, 500, 1200, 2500].map(delay => window.setTimeout(requestHeight, delay))
    return () => {
      window.removeEventListener('message', receive)
      window.removeEventListener('resize', requestHeight)
      retries.forEach(window.clearTimeout)
    }
  }, [navigate, dashboardUrl])

  return <main id="main-content" className="shell school-futures">
    <p className="eyebrow">{t('Planning Lab')}</p>
    <h1>{t(dashboard.title)}</h1>
    <p>{t(dashboard.description)}</p>
    <nav aria-label={t('School planning dashboards')}>
      {(Object.keys(schoolFutures) as SchoolFuturesRoute[]).map(id => (
        <button key={id} className={'button ' + (route === id ? 'button-primary' : 'button-secondary')}
          aria-current={route === id ? 'page' : undefined} onClick={() => navigate(id)}>
          {t(schoolFutures[id].title)}
        </button>
      ))}
      <a className="text-link" href={dashboardUrl}>{t('Open the full dashboard')}</a>
      <a className="text-link" href={base + dashboard.notes} download>{t('Download model notes')}</a>
    </nav>
    <iframe ref={frame} title={t(dashboard.title)} src={dashboardUrl} height={height} scrolling="no"
      onLoad={() => frame.current?.contentWindow?.postMessage({ type: 'atlas-school-frame-request-height' }, '*')}
      sandbox="allow-scripts allow-downloads allow-popups allow-popups-to-escape-sandbox" />
  </main>
}
