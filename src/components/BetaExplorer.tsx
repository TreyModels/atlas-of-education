import { useId, useState } from 'react'
import type { Translate } from '../types'
import { KLASSEN_BETA, KLASSEN_SE, THEORY_BETA, perPersonIndex } from '../lib/scaling'

const MIN = 20, MAX = 1000
const lo = KLASSEN_BETA - 1.96 * KLASSEN_SE, hi = KLASSEN_BETA + 1.96 * KLASSEN_SE
const series = [
  { key: 'klassen', beta: KLASSEN_BETA, label: 'Published fit, β = 1.227' },
  { key: 'theory', beta: THEORY_BETA, label: 'Scaling theory, β = 7/6' },
  { key: 'flat', beta: 1, label: 'Constant returns, β = 1' },
]

/** "Watch this" moment for chapter 1: one slider, community size. */
export function BetaExplorer({ t }: { t: Translate }) {
  const [n, setN] = useState(500)
  const id = useId()
  const W = 560, H = 220, P = 36
  const yMax = perPersonIndex(MAX, hi) * 1.05, yMin = perPersonIndex(MIN, hi) * 0.95
  const x = (v: number) => P + (v - MIN) / (MAX - MIN) * (W - 2 * P)
  const y = (v: number) => H - P - (v - yMin) / (yMax - yMin) * (H - 2 * P)
  const xs = Array.from({ length: 50 }, (_, i) => MIN + i * (MAX - MIN) / 49)
  const path = (b: number) => xs.map((v, i) => `${i ? 'L' : 'M'}${x(v).toFixed(1)},${y(perPersonIndex(v, b)).toFixed(1)}`).join('')
  const band = path(hi) + xs.slice().reverse().map(v => `L${x(v).toFixed(1)},${y(perPersonIndex(v, lo)).toFixed(1)}`).join('') + 'Z'

  return <figure className="journey-interactive beta-explorer">
    <figcaption className="journey-watch"><strong>{t('Watch this')}</strong> {t('Move community size. With β above 1, each person’s share of the production index rises as communities grow.')}</figcaption>
    <label htmlFor={id} className="beta-control">{t('People in a temple community')}: <output>{n}</output></label>
    <input id={id} type="range" min={MIN} max={MAX} step={10} value={n} onChange={e => setN(Number(e.target.value))} />
    <svg viewBox={`0 0 ${W} ${H}`} role="img" aria-label={t('Per-person production index against community size for three scaling exponents')} className="beta-chart">
      <path d={band} className="beta-band" />
      {series.map(s => <path key={s.key} d={path(s.beta)} className={`beta-line beta-${s.key}`} />)}
      <line x1={x(n)} x2={x(n)} y1={P / 2} y2={H - P} className="beta-marker" />
      <text x={P} y={H - 8} className="beta-axis">{MIN}</text>
      <text x={W - P} y={H - 8} className="beta-axis" textAnchor="end">{MAX} {t('people')}</text>
      <text x={8} y={y(100) + 4} className="beta-axis">100</text>
    </svg>
    <table className="beta-readout">
      <thead><tr><th scope="col">{t('Assumption')}</th><th scope="col">{t('Index per person at')} {n}</th></tr></thead>
      <tbody>
        {series.map(s => <tr key={s.key} className={`beta-row-${s.key}`}><th scope="row">{t(s.label)}</th><td>{perPersonIndex(n, s.beta).toFixed(1)}</td></tr>)}
        <tr><th scope="row">{t('95% range of the published fit')}</th><td>{perPersonIndex(n, lo).toFixed(1)}–{perPersonIndex(n, hi).toFixed(1)}</td></tr>
      </tbody>
    </table>
    <p className="journey-note">{t('Index = 100 at 100 people. It is a product of archaeological proxies for labour, land and water, not tonnes of rice.')}</p>
  </figure>
}
