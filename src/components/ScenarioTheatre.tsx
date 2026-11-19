import { DataChart } from './DataChart'
import type { Control, Translate, Values, View, World } from '../types'
import '../scenario-theatre.css'

type PinnedScenario = { values: Values; view: View }

function formatControlValue(control: Control, value: Values[string], t: Translate) {
  if (typeof value === 'number' && control.format) return t(control.format(value))
  if (control.options && value !== undefined) return t(control.options[String(value)] ?? String(value))
  if (typeof value === 'number' && Number.isFinite(value)) {
    return new Intl.NumberFormat(undefined, { maximumFractionDigits: 4 }).format(value)
  }
  if (value && typeof value === 'object') return JSON.stringify(value)
  return t(String(value ?? '—'))
}

function parseMetric(value: string) {
  const cleaned = value.trim().replace(/,/g, '')
  const match = cleaned.match(/^([+\-−]?)(\d+(?:\.\d+)?)(\s*[%a-zA-Z]+)?$/)
  if (!match) return null
  const sign = match[1] === '-' || match[1] === '−' ? -1 : 1
  const number = sign * Number(match[2])
  if (!Number.isFinite(number)) return null
  return {
    number,
    suffix: (match[3] ?? '').trim(),
    decimals: match[2].split('.')[1]?.length ?? 0,
  }
}

function formatMetricChange(pinnedValue: string, currentValue: string) {
  const pinned = parseMetric(pinnedValue)
  const current = parseMetric(currentValue)
  if (!pinned || !current || pinned.suffix !== current.suffix) return '—'
  const delta = current.number - pinned.number
  const digits = Math.min(2, Math.max(pinned.decimals, current.decimals))
  const number = Math.abs(delta).toLocaleString(undefined, {
    maximumFractionDigits: digits,
    minimumFractionDigits: 0,
  })
  const sign = delta > 0 ? '+' : delta < 0 ? '−' : ''
  return `${sign}${number}${current.suffix && current.suffix !== '%' ? ` ${current.suffix}` : current.suffix}`
}

export function ScenarioTheatre({ world, pinned, currentView, currentValues, t }: {
  world: World
  pinned: PinnedScenario
  currentView: View
  currentValues: Values
  t: Translate
}) {
  const headlineMetrics = pinned.view.metrics.slice(0, 3)
  const changedControls = world.controls.filter(control =>
    JSON.stringify(pinned.values[control.key]) !== JSON.stringify(currentValues[control.key])
  )

  return <section className="scenario-theatre" aria-labelledby="scenario-theatre-title">
    <div className="scenario-theatre-heading">
      <div>
        <span className="panel-kicker">{t('Pinned scenario')}</span>
        <h2 id="scenario-theatre-title">{t('Scenario Theatre')}<span className="experimental-chip">{t('Experimental')}</span></h2>
      </div>
    </div>

    <div className="theatre-grid">
      <section className="theatre-panel" aria-labelledby="theatre-pinned-heading">
        <h3 id="theatre-pinned-heading">{t('Pinned')}</h3>
        <DataChart view={pinned.view} t={t} worldId={world.id} />
      </section>
      <section className="theatre-panel" aria-labelledby="theatre-current-heading">
        <h3 id="theatre-current-heading">{t('Current')}</h3>
        <DataChart view={currentView} t={t} worldId={world.id} />
      </section>
    </div>

    <div className="theatre-table-wrap">
      <div className="table-scroll">
        <table className="theatre-table" aria-label={t('Pinned scenario comparison')}>
          <caption className="sr-only">{t('Pinned scenario comparison')}</caption>
          <thead>
            <tr>
              <th scope="col">{t('Measure')}</th>
              <th scope="col">{t('Pinned')}</th>
              <th scope="col">{t('Current')}</th>
              <th scope="col">{t('Change')}</th>
            </tr>
          </thead>
          <tbody>
            {headlineMetrics.map(metric => {
              const currentMetric = currentView.metrics.find(item => item.label === metric.label)
              const pinnedValue = String(metric.value)
              const currentValue = currentMetric ? String(currentMetric.value) : '—'
              return <tr key={metric.label}>
                <th scope="row">{t(metric.label)}</th>
                <td>{t(pinnedValue)}</td>
                <td className={currentValue !== pinnedValue ? 'changed-value' : ''}>{t(currentValue)}</td>
                <td>{formatMetricChange(pinnedValue, currentValue)}</td>
              </tr>
            })}
          </tbody>
        </table>
      </div>
    </div>

    <div className="theatre-assumptions">
      <h3>{t('Changed assumptions')}</h3>
      {changedControls.length > 0
        ? <ul>
            {changedControls.map(control => <li key={control.key}>
              <span>{t(control.label)}</span>
              <span className="theatre-assumption-values">
                <b>{formatControlValue(control, pinned.values[control.key], t)}</b>
                <span aria-hidden="true"> → </span>
                <b>{formatControlValue(control, currentValues[control.key], t)}</b>
              </span>
            </li>)}
          </ul>
        : <p>{t('None')}</p>}
    </div>

    <p className="theatre-scope">{t('This compares model runs, not empirical validation.')}</p>
  </section>
}
