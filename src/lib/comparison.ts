import type {World,Values} from '../types'
export type Comparison={id:string;referenceControls:Values;matched:string[];plot:string;scope:string}
export function comparisonFor(world:World,values:Values):Comparison {
 let referenceControls:Values={...world.defaults,...('seed' in values?{seed:values.seed}:{})}
 const plot:Record<string,string>={accounts:'Maintained canals under the selected climate and stored run.',maintenance:'Maintained canals under the selected climate and stored run.',relocation:'Movement blocked, with the other selected conditions unchanged.',obligations:'No additional delivery cut; the same upstream settings and other selected conditions.',signalling:'Display and informed observers face the same challenges in separate evolving worlds.',monsoon:'Published and neutral climate use the same parameter draw; each line is normalized to its own year 1300.',provisioning:'The selected scaling curve is compared with constant output per person.'}
 if(['accounts','maintenance'].includes(world.id))referenceControls={...values,scenario:'stable'}
 if(world.id==='flight')referenceControls={...values,scenario:'redistribution_open'}
 if(world.id==='credentials')referenceControls={...values,structure:'M_HC'}
 if(world.id==='relocation')referenceControls={...values,mobility:'closed'}
 if(world.id==='obligations')referenceControls={...values,disruption:0}
 const scope=['accounts','maintenance','flight'].includes(world.id)?'Curve: one selected history. Cards: medians of 40 histories.':world.id==='institutions'?'One trial per scenario.':world.id==='monsoon'?'Curve: one parameter draw. Cards: 2,000-draw summaries.':world.stored?'Stored summaries; see each output label for its sample.':'See each metric and chart note for the run count and units.'
 return{id:world.id+'-comparison-v1',referenceControls,matched:Object.keys(values).filter(k=>JSON.stringify(values[k])===JSON.stringify(referenceControls[k])),plot:plot[world.id]??'Selected settings compared with the model reference settings.',scope}
}
