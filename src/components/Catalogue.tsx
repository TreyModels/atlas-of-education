import {useState,Fragment} from 'react'
import catalogue from '../data/model-catalogue.md?raw'
import chineseCatalogue from '../data/model-catalogue.zh-Hans.md?raw'
import vietnameseCatalogue from '../data/model-catalogue.vi.md?raw'
import type {Language, Translate} from '../types'

// Render only the small Markdown subset used by the supplied catalogue.
// React escapes text; source HTML and scripts are never executed.
function inline(text:string):React.ReactNode[]{
 return text.split(/(\[[^\]]+\]\(https?:\/\/[^\s)]+\)|\*\*[^*]+\*\*|\*[^*]+\*|`[^`]+`)/g).map((part,i)=>{
  const link=part.match(/^\[([^\]]+)\]\((https?:\/\/[^\s)]+)\)$/)
  if(link)return <a key={i} href={link[2]} target="_blank" rel="noreferrer">{link[1]}</a>
  if(part.startsWith('**')&&part.endsWith('**'))return <strong key={i}>{part.slice(2,-2)}</strong>
  if(part.startsWith('*')&&part.endsWith('*'))return <em key={i}>{part.slice(1,-1)}</em>
  if(part.startsWith('`')&&part.endsWith('`'))return <code key={i}>{part.slice(1,-1)}</code>
  return <Fragment key={i}>{part}</Fragment>
 })
}
function blocks(text:string){
 const lines=text.trim().split('\n'),out:React.ReactNode[]=[]
 for(let i=0;i<lines.length;i++){
  const line=lines[i].trim();if(!line)continue
  if(line.startsWith('|')){
   const rows:string[][]=[]
   while(i<lines.length&&lines[i].trim().startsWith('|')){rows.push(lines[i].trim().slice(1,-1).split('|').map(s=>s.trim()));i++}i--
   const body=rows.slice(1).filter(r=>!r.every(c=>/^:?-+:?$/.test(c)))
   out.push(<div className="table-scroll" key={i}><table><thead><tr>{rows[0].map((c,j)=><th scope="col" key={j}>{inline(c)}</th>)}</tr></thead><tbody>{body.map((r,j)=><tr key={j}>{r.map((c,k)=>k===0?<th scope="row" key={k}>{inline(c)}</th>:<td key={k}>{inline(c)}</td>)}</tr>)}</tbody></table></div>);continue
  }
  if(line.startsWith('- ')){
   const items=[];while(i<lines.length&&lines[i].startsWith('- ')){items.push(lines[i].slice(2));i++}i--
   out.push(<ul key={i}>{items.map((s,j)=><li key={j}>{inline(s)}</li>)}</ul>);continue
  }
  let paragraph=line
  while(i+1<lines.length&&lines[i+1].trim()&&!lines[i+1].startsWith('|')&&!lines[i+1].startsWith('- ')){paragraph+=' '+lines[++i].trim()}
  out.push(<p key={i}>{inline(paragraph)}</p>)
 }
 return out
}
const documents = {en: catalogue, 'zh-Hans': chineseCatalogue, vi: vietnameseCatalogue, fr: catalogue}
const sectionsFrom = (document: string) => document.split(/^## /m).slice(1).map((part,index)=>{const end=part.indexOf('\n');return {id:'catalogue-'+index,title:part.slice(0,end),body:part.slice(end+1)}})
export function Catalogue({t, language}:{t:Translate; language:Language}){
 const parts=sectionsFrom(documents[language])
 const [query,setQuery]=useState('')
 const selected=parts.filter(p=>(p.title+' '+p.body).toLowerCase().includes(query.toLowerCase()))
 return <main id="main-content" className="shell catalogue-page">
  <header><p className="eyebrow">{t('Research catalogue')}</p><h1>{t('Atlas of Models')}</h1><p>{t('Browse published mechanisms, rival explanations and the proposed build queue.')}</p></header>
  <div className="catalogue-note"><strong>{t('Research notes · awaiting verification')}</strong><p>{t('This catalogue records proposed work and claims from the supplied document. Publication details, data, licences and numerical claims still need source checks. Entries marked Port or Build are planned work; the model selector lists the runnable app modules.')}</p><a href="research/model-catalogue.md" download>{t('Download original catalogue')}</a></div>
  <label className="catalogue-search">{t('Search the catalogue')}<input type="search" value={query} onChange={e=>setQuery(e.target.value)} placeholder={t('Search by author, model or country')}/></label>
  <nav className="catalogue-topics" aria-label={t('Catalogue topics')}>{selected.map(p=><button key={p.id} onClick={()=>document.getElementById(p.id)?.scrollIntoView({block:'start'})}>{p.title}</button>)}</nav>
  {!selected.length&&<p role="status">{t('No matching catalogue sections.')}</p>}
  {selected.map(p=><section key={p.id} id={p.id} className="catalogue-section"><h2>{p.title}</h2>{blocks(p.body)}</section>)}
 </main>
}
