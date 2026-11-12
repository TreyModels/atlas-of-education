import { ArrowLeft, ArrowRight, ArrowUpRight } from 'lucide-react'
import type { Translate } from '../types'
import { familyItems, familyResearch, modelFamilies, type CatalogueItem, type ModelFamily } from '../data/model-catalogue'
import { familyStories, type ClaimTag, type StoryBlock } from '../data/family-stories'
import { ModelLink } from './Library'

const tagMeta: Record<ClaimTag, { label: string; className: string }> = {
  data: { label: 'data', className: 'tag-data' },
  sim: { label: 'sim', className: 'tag-sim' },
  'ruled-out': { label: 'ruled out', className: 'tag-ruled' },
  open: { label: 'open', className: 'tag-open' },
  method: { label: 'method', className: 'tag-method' },
}

function Tag({ tag, t }: { tag: ClaimTag; t: Translate }) {
  const meta = tagMeta[tag]
  return <span className={`claim-tag ${meta.className}`}>[{t(meta.label)}]</span>
}

function Block({ block, t }: { block: StoryBlock; t: Translate }) {
  if (block.kind === 'list') return <div className="story-block">
    {block.tag && <Tag tag={block.tag} t={t} />}
    <ul>{block.items.map((item, index) => <li key={index}>{t(item)}</li>)}</ul>
  </div>
  if (block.kind === 'table') return <figure className="story-block story-table-wrap">
    {block.caption && <figcaption>{block.tag && <Tag tag={block.tag} t={t} />}{t(block.caption)}</figcaption>}
    <div className="table-scroll"><table>
      <thead><tr>{block.head.map((cell, index) => <th scope="col" key={index}>{t(cell)}</th>)}</tr></thead>
      <tbody>{block.rows.map((row, index) => <tr key={index}>{row.map((cell, cellIndex) => cellIndex === 0 ? <th scope="row" key={cellIndex}>{t(cell)}</th> : <td key={cellIndex}>{t(cell)}</td>)}</tr>)}</tbody>
    </table></div>
  </figure>
  return <p className="story-block">{block.tag && <Tag tag={block.tag} t={t} />}{t(block.text)}</p>
}

export function StoryPage({ family, t, navigate }: { family: ModelFamily; t: Translate; navigate: (id: string) => void }) {
  const story = familyStories[family]
  const models = familyItems(family)
  const research = familyResearch[family]
  const index = modelFamilies.indexOf(family)
  const previous = modelFamilies[(index + modelFamilies.length - 1) % modelFamilies.length]
  const next = modelFamilies[(index + 1) % modelFamilies.length]

  return <main id="main-content" className="story-page">
    <header className="story-hero shell">
      <p className="eyebrow">{t(familyStories[family].kicker)} · {t('Class {i} of {n}').replace('{i}', String(index + 1).padStart(2, '0')).replace('{n}', String(modelFamilies.length).padStart(2, '0'))}</p>
      <h1>{t(story.title)}</h1>
      <p className="story-lede">{t(story.lede)}</p>
      {story.cta && <p><button className="button button-primary" onClick={() => navigate(story.cta!.route)}>{t(story.cta.label)}<ArrowRight size={17} /></button></p>}
      <p className="story-legend">
        {(Object.keys(tagMeta) as ClaimTag[]).map(tag => <span key={tag}><Tag tag={tag} t={t} />{t({ data: 'measured from real data', sim: 'produced by a simulation', 'ruled-out': 'tested and rejected', open: 'still unsettled', method: 'a computational tool' }[tag])}</span>)}
      </p>
    </header>

    <div className="story-body shell">
      <div className="story-sections">
        {story.sections.map((section, sectionIndex) => <section className="story-section" key={sectionIndex}>
          <h2><span>{String(sectionIndex + 1).padStart(2, '0')}</span>{t(section.heading)}</h2>
          {section.blocks.map((block, blockIndex) => <Block key={blockIndex} block={block} t={t} />)}
        </section>)}
        {story.bottomLine && <aside className="story-bottomline">
          <h2>{t('The one-paragraph version')}</h2>
          <p>{t(story.bottomLine)}</p>
        </aside>}
      </div>

      <aside className="story-rail">
        <section className="story-rail-box">
          <h3>{t('Models in this class')}</h3>
          <ul className="story-model-list">
            {models.map((item: CatalogueItem) => <ModelLink key={item.id} item={item} t={t} navigate={navigate} />)}
          </ul>
        </section>
        <section className="story-rail-box">
          <h3>{t('Research & downloads')}</h3>
          <ul className="story-research-list">
            {research.map(link => <li key={link.href}><a href={link.href} {...(link.href.startsWith('http') ? { target: '_blank', rel: 'noreferrer' } : {})}>{t(link.label)}<ArrowUpRight size={15} /></a></li>)}
          </ul>
        </section>
      </aside>
    </div>

    <nav className="story-pager shell" aria-label={t('Browse model classes')}>
      <button onClick={() => navigate(`story-${previous}`)}><ArrowLeft size={17} /><span><small>{t('Previous class')}</small>{t(familyStories[previous].title)}</span></button>
      <button onClick={() => navigate(`story-${next}`)}><span><small>{t('Next class')}</small>{t(familyStories[next].title)}</span><ArrowRight size={17} /></button>
    </nav>
  </main>
}
