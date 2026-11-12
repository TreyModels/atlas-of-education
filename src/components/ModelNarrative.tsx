import type {World,Values,Translate,View} from '../types'
import stories from '../data/model-stories.json'
import cards from '../data/cards.json'
const trials:Record<string,Values>={provisioning:{community:100},relocation:{mobility:'closed'},petri:{knockout:'coordination'},monsoon:{sensitivity:.1},cambodia:{feeding:1},china:{gradSupply:1.5},teachers:{lag:5},angkor:{yieldT:.7},campaign:{distance:540},signalling:{signalScale:.6},obligations:{returnRule:'open'},mandala:{scenario:'high_shock'},credentials:{structure:'M_HC'},institutions:{scenario:'elite_drought'},flight:{scenario:'extraction_fortified'},maintenance:{scenario:'stable'},accounts:{scenario:'stable'},cohort:{rep1:0},sector:{ptrT:30},schoolmap:{rule:'largest'},lays:{hlo:540},absorption:{gradGrowth:.08}}
export function ModelNarrative({world,view,referenceView,values,referenceControls,onChange,t,pending,campaignLaunches}:{world:World;view:View;referenceView:View;values:Values;referenceControls?:Values;onChange:(v:Values)=>void;t:Translate;pending:boolean;campaignLaunches?:number}){
 const ref=referenceControls??world.defaults
 const changed=world.controls.filter(c=>!['seed','draw','runs'].includes(c.key)&&JSON.stringify(values[c.key])!==JSON.stringify(ref[c.key]))
 const format=(key:string,value:Values[string])=>{const c=world.controls.find(c=>c.key===key)!;return typeof value==='number'&&c.format?t(String(c.format(value))):t(c.options?.[String(value)]??String(value))}
 const evidence=typeof world.evidence==='function'?world.evidence(values):world.evidence
 const trial=trials[world.id],finding=cards.find(c=>c.href==='#'+world.id)?.details[1].description ?? evidence.find(e=>e.flag)?.body ?? evidence[0].body
 return <>
 <section className="story-intro"><p>{t((stories as Record<string,string>)[world.id])}</p>
 {finding&&<p><strong>{t('Earlier experiment finding')}: </strong>{t(finding)}</p>}
 <p><strong>{t('Reference setting')}: </strong>{world.controls.filter(c=>!['seed','draw','runs'].includes(c.key)).slice(0,3).map(c=><span key={c.key}>{t(c.label)}: <strong>{format(c.key,ref[c.key])}</strong>; </span>)}</p><details><summary>{t('Reference setting')}</summary><p>{world.controls.filter(c=>!['seed','draw','runs'].includes(c.key)).map(c=><span key={c.key}>{t(c.label)}: <strong>{format(c.key,ref[c.key])}</strong>; </span>)}</p><p><strong>{t('Run settings')}: </strong>{world.controls.filter(c=>!['seed','draw','runs'].includes(c.key)).map(c=><span key={c.key}>{t(c.label)}: {format(c.key,values[c.key])}; </span>)}</p><p>{referenceView.metrics.slice(0,3).map(m=><span key={m.label}>{t(m.label)}: <strong>{t(String(m.value))}</strong>; </span>)}</p></details>
 <p className="try-experiment"><strong>{t('Try this')}: </strong>{Object.entries(trial).map(([key,v])=><button key={key} className="button button-secondary" disabled={pending} onClick={()=>onChange({...values,...trial})}>{t(world.controls.find(c=>c.key===key)!.label)} → {format(key,v)}</button>)}</p>
 </section>
 <section className="change-reading" aria-label={t('What your settings changed')}><h3>{t('What your settings changed')}</h3>
 {pending?<p role="status">{t('Updating…')}</p>:<>
 <p>{t(changed.length?'These settings differ from the reference. The comparisons below describe the completed run.':'You are viewing the reference settings. Try the suggested change to compare an alternative.')}</p>
 {changed.map(c=><p key={c.key}><strong>{t(c.label)}: {format(c.key,ref[c.key])} → {format(c.key,values[c.key])}.</strong> {t(c.note)}</p>)}
 {world.id==='obligations'&&values.upstream&&<p>{t('Upstream signalling settings')}: {JSON.stringify(values.upstream)}</p>}
 {world.id==='campaign'&&<p><strong>{t('Planned trip: {days} days; harvest starts after 120 days.').replace('{days}',String(parseFloat(String(view.metrics[1].value))))}</strong> {t(campaignLaunches===0?'No funded campaign launched in this history. The planned travel time does not mean troops were actually away.':parseInt(String(view.metrics[2].value))>0?'The levy is still away when harvest begins, reducing farm work. Stored food can cushion that loss; unlimited storage in this version limits what we can conclude about food security.':'No harvest overlap is recorded in this history. Planned duration and actual funded campaigns are different outcomes.')}</p>}
 {changed.length>0&&<ul>{view.metrics.slice(0,3).map((m,i)=><li key={m.label}>{t(m.label)}: <strong>{t(String(referenceView.metrics[i]?.value??''))} → {t(String(m.value))}</strong></li>)}</ul>}
 {changed.length>0&&view.metrics.every((m,i)=>String(m.value)===String(referenceView.metrics[i]?.value))&&<p>{t('These displayed summary values are unchanged. Inspect the curve and detailed results before concluding that the assumption has no effect.')}</p>}
 {changed.length>1&&<p>{t('Several assumptions changed together. This comparison cannot isolate the contribution of each change.')}</p>}
 </>}
 </section>
 </>
}
export {trials}
