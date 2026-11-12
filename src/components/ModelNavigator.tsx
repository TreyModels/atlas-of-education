import type { Translate } from '../types'
import { catalogue, familyInfo, familyItems, type ModelFamily } from '../data/model-catalogue'

export const educationIds = ['china', 'cambodia', 'credentials']
export const planningIds = ['teachers', 'cohort', 'sector', 'schoolmap', 'lays', 'absorption']
export const angkorGuidedIds = ['provisioning', 'campaign', 'angkor', 'signalling', 'obligations', 'monsoon']
export const angkorFurtherIds = ['mandala', 'accounts', 'institutions', 'flight', 'maintenance', 'relocation', 'petri']

const families: { id: ModelFamily; entry: string }[] = [
  { id: 'education', entry: 'home/education-models' },
  { id: 'systems', entry: 'home/school-systems' },
  { id: 'planning', entry: 'home/planning-lab' },
  { id: 'angkor', entry: 'angkor-guide' },
  { id: 'fertility', entry: 'home/fertility-models' },
  { id: 'shadow', entry: 'home/shadow-models' },
  { id: 'deephistory', entry: 'home/deep-history' },
]

export function ModelNavigator({ route, navigate, t }: { route: string; navigate: (id: string) => void; t: Translate }) {
  const activeItem = catalogue.find(item => item.route === route)
  const family = families.find(item => item.id === activeItem?.family || (item.id === 'angkor' && route === 'angkor-guide'))
  const open = (id: string) => {
    const item = catalogue.find(model => model.id === id)
    if (!item) return
    if (item.href) window.open(item.href, '_blank', 'noopener,noreferrer')
    else if (item.route) navigate(item.route)
  }
  return <nav className="model-navigator" aria-label={t('Switch models')}>
    <div className="shell model-navigator-inner">
      <div className="model-families">
        <button className={!route ? 'active' : ''} aria-current={!route ? 'page' : undefined} onClick={() => navigate('')}>{t('Model library')}</button>
        {families.map(item => <button key={item.id} className={family?.id === item.id ? 'active' : ''} aria-current={family?.id === item.id ? 'page' : undefined} onClick={() => navigate(item.entry)}>{t(familyInfo[item.id].short)}</button>)}
        <button className={route === 'catalogue' ? 'active' : ''} aria-current={route === 'catalogue' ? 'page' : undefined} onClick={() => navigate('catalogue')}>{t('Research catalogue')}</button>
      </div>
      <label className="model-switcher"><span>{t('Switch models')}</span><select value={activeItem?.id ?? ''} onChange={event => open(event.target.value)} aria-label={t('Choose a model')}>
        <option value="">{t(route === 'angkor-guide' ? 'Guided sequence' : 'Choose a catalogue entry')}</option>
        {families.map(group => <optgroup key={group.id} label={t(familyInfo[group.id].title)}>{familyItems(group.id).map(item => <option key={item.id} value={item.id}>{t(item.title)}{item.href ? ' ↗' : ''}</option>)}</optgroup>)}
      </select></label>
    </div>
  </nav>
}
