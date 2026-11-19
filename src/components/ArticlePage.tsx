import type { Translate } from '../types'
import type { Article } from '../data/about'

/** Plain long-form page (About, How these models work). Kimi owns the styling. */
export function ArticlePage({ article, t }: { article: Article; t: Translate }) {
  return <main id="main-content" className="journey-page article-page">
    <header className="journey-hero">
      <p className="eyebrow">{t(article.kicker)}</p>
      <h1>{t(article.title)}</h1>
      <p className="journey-lede">{t(article.lede)}</p>
    </header>
    {article.sections.map(s => <section className="journey-chapter article-section" key={s.heading}>
      <h2>{t(s.heading)}</h2>
      {s.paras.map((p, i) => <p className="journey-para" key={i}>{t(p)}</p>)}
      {s.quote && <blockquote className="article-quote"><p>“{t(s.quote.text)}”</p><cite>{t(s.quote.who)}</cite></blockquote>}
      {s.maths && <div className="journey-maths article-maths">
        <p>{t(s.maths.plain)}</p>
        {s.maths.formula && <pre><code>{s.maths.formula}</code></pre>}
        {s.maths.example && <p>{t(s.maths.example)}</p>}
      </div>}
    </section>)}
  </main>
}
