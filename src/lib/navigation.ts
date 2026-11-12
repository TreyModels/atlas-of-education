import type {Values} from '../types'
export const sections=new Set(['main-content','result-title','controls-title','model-explanation','method','model-collection','education-models','planning-lab','angkor-case','fertility-models','shadow-models'])
export function parseLocation(hash:string){const [page,section]=hash.replace(/^#/,'').split('/');return {route:page==='home'?'':page,section:section??''}}
export function sectionHash(route:string,section:string){if(!sections.has(section))throw Error('Unknown section');return '#'+(route||'home')+'/'+section}
export function preserveHandoff(defaults:Values,previous:Values|undefined,values:Values){return {...defaults,...previous,seed:values.seed,upstream:{...values}}}
