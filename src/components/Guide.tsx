import { ArrowLeft, ArrowUpRight, MoveRight } from 'lucide-react'
import guide from '../data/guide.json'
import type { Translate } from '../types'

export function Guide({ t, navigate }: { t: Translate; navigate: (id: string) => void }) {
  return <main id="main-content" className="guide-page shell">
    <button className="back-link" onClick={() => navigate('')}><ArrowLeft size={17} />{t('Back to library')}</button>
    <section className="guide-intro">
      <p className="eyebrow">{t('ANGKOR · A GUIDED RECONSTRUCTION')}</p>
      <h1>{t('How does this society work?')}</h1>
      <p>{t('Start with food and labour. Follow how the existing experiments turn resources into growth, infrastructure and authority, then examine what happens when commitments or climate change.')}</p>
    </section>
    <div className="guide-boundary"><strong>{t('The models and their boundaries')}</strong><p>{t('These are existing experiments with different time scales and accounting boundaries. The guide connects their questions. The signalling-to-obligations handoff carries settings and pledges; other connections remain conceptual.')}</p></div>
    <section className="guide-steps" aria-label={t('Guided sequence')}>
      {guide.map((step, index) => <button key={step[0]} className="guide-step" onClick={() => navigate(step[0])}>
        <span className="step-index">{String(index + 1).padStart(2, '0')}<i /></span>
        <span className="step-copy"><span className="eyebrow">{t(step[1])}</span><strong>{t(step[2])}</strong><span>{t(step[3])}</span></span>
        <span className="step-open">{t('Open step')}<MoveRight size={19} /></span>
      </button>)}
    </section>
    <section className="guide-accounting">
      <div><p className="eyebrow">{t('What the economy has to account for')}</p><h2>{t('Households need food. Fields and waterways need labour.')}</h2></div>
      <div><p>{t('The centre also has to provision builders, soldiers and ritual obligations. Infrastructure can improve future production while creating maintenance costs. These resource claims are the thread through the sequence.')}</p><a href="research/angkor-sequence.html">{t('Read sources, results and handoff limits')}<ArrowUpRight size={16} /></a></div>
    </section>
  </main>
}
