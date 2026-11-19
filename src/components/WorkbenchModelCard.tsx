import { purposeLabel, stateLabel, type ModelCard } from '../data/angkor-journey'
import { journeyModels } from '../data/journey-models'
import type { CatalogueItem } from '../data/model-catalogue'
import stories from '../data/model-stories.json'
import type { Translate, World } from '../types'
import './../model-card.css'

/**
 * A real model card at the top of every workbench page.
 *
 * The workbench previously opened straight into controls and a narrative
 * paragraph, with the honest labels (what the model is for, how far it has been
 * checked, what it cannot show) only present on the family journey page. Trey's
 * complaint — "no real model card explaining what we're looking at" — is fixed
 * here by surfacing the journey's model card on the workbench itself.
 */
export function WorkbenchModelCard({ world, item, t, navigate }: {
  world: World
  item?: CatalogueItem
  t: Translate
  navigate: (id: string) => void
}) {
  const card: ModelCard | undefined = journeyModels[world.id]
  const summary = (stories as Record<string, string>)[world.id] ?? world.question
  // The pinned engine version strings still carry the historical project name.
  // Show the version number here; the full historical label stays in the
  // evidence panel and the exported run JSON, so provenance is not rewritten.
  const versionLabel = world.version.replace(/^Atlas of Education\s+/, '')
  const openTag = (tag: string) => window.dispatchEvent(new CustomEvent<string>('atlas:search', { detail: `#${tag}` }))

  return <section className="model-card" aria-labelledby="model-card-title">
    <header className="model-card-head">
      <p className="eyebrow">{t('MODEL CARD')}</p>
      <h2 id="model-card-title" className="sr-only">{t(world.title)}</h2>
      <div className="model-card-badges">
        {card && <span className={`badge purpose-${card.purpose}`} title={t(purposeLabel[card.purpose].help)}>{t(purposeLabel[card.purpose].label)}</span>}
        {card && <span className={`badge state-${card.state}`} title={t(stateLabel[card.state].help)}>{t(stateLabel[card.state].label)}</span>}
        <span className="badge badge-mode">{t(world.stored ? 'Stored results' : 'Live model')}</span>
      </div>
    </header>

    <div className="model-card-grid">
      <div>
        <h3>{t('What you are looking at')}</h3>
        <p>{t(summary)}</p>
      </div>
      {card && <div>
        <h3>{t('Why this model exists')}</h3>
        <p>{t(purposeLabel[card.purpose].help)}</p>
      </div>}
      {card && <div>
        <h3>{t('How far it has been checked')}</h3>
        <p>{t(stateLabel[card.state].help)}</p>
      </div>}
      {card?.note && <div>
        <h3>{t('What it does not show')}</h3>
        <p>{t(card.note)}</p>
      </div>}
    </div>

    <footer className="model-card-foot">
      <span className="model-card-source" title={world.version}>{t('Model version')}: {versionLabel}</span>
      {item && <button className="text-link" onClick={() => navigate(`story-${item.family}`)}>{t('Read the family journey')}</button>}
      <a className="text-link" href="#model-explanation">{t('Evidence & assumptions')}</a>
      {item && <span className="model-card-tags" aria-label={t('Tags')}>{item.tags.slice(0, 6).map(tag =>
        <button key={tag} className="tag-chip tag-chip-quiet" onClick={() => openTag(tag)}>#{tag}</button>)}</span>}
    </footer>
  </section>
}
