import type {Translate,World,View} from '../types'
import advice from '../data/analysis-advice.json'
const position:Record<string,number>={provisioning:0,relocation:1,petri:1,monsoon:2,cambodia:1,china:1,teachers:1,angkor:0,campaign:1,signalling:2,obligations:1,mandala:0,credentials:2,institutions:0,flight:0,maintenance:0,accounts:0,cohort:1,sector:1,schoolmap:1,lays:1,absorption:1}
export function ModelQuestions({world,values,view,t}:{world:World;values:Parameters<World['run']>[0];t:Translate;view:View}){
 const evidence=typeof world.evidence==='function'?world.evidence(values):world.evidence
 const basis=evidence[position[world.id]??0]
 const credibility:Record<string,number>={provisioning:1,china:2,cambodia:3,teachers:1,monsoon:3,mandala:0,credentials:2};
 const limit=evidence[credibility[world.id]??evidence.findIndex(e=>e.flag)]??evidence.at(-1)
 return <section className="model-questions" aria-label={t('Questions this model must answer')}>
  <h2>{t('Questions this model must answer')}</h2>
  <div className="question-grid">
   <details><summary>{t('Are these parameters reasonable?')}</summary><p>{t(basis.body)}</p><a href="#controls-title">{t('Inspect the controls and their bounds')}</a></details>
   <details><summary>{t('How convincing are these results?')}</summary><p>{t(limit?.body??'')}</p></details>
   <details><summary>{t('How should I read the curve?')}</summary><p>{t(view.note)}</p><a href="#result-title">{t('Read the result and its explanation')}</a></details>
   <details><summary>{t('Do I need someone to analyse this?')}</summary><p>{t((advice as Record<string,string>)[world.id])}</p><a href="#method">{t('Inspect the evidence and unresolved limits')}</a></details>
  </div>
 </section>
}
