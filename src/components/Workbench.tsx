import { useEffect, useMemo, useState } from 'react'
import { useModelRun } from '../model/useModelRun'
import { ArrowLeft, ArrowRight, ArrowUpRight, Download, Pause, Pin, Play, RotateCcw, X } from 'lucide-react'
import guideData from '../data/guide.json'
import { sourceHashes } from '../models'
import type { Control, Translate, Values, World, View } from '../types'
import { DataChart } from './DataChart'
import { ModelNarrative } from './ModelNarrative'
import { ModelQuestions } from './ModelQuestions'
import stories from '../data/model-stories.json'

function download(data: string, type: string, filename: string) {
  const url = URL.createObjectURL(new Blob([data], { type }))
  const anchor = document.createElement('a')
  anchor.href = url
  anchor.download = filename
  anchor.click()
  window.setTimeout(() => URL.revokeObjectURL(url), 1000)
}

const TECHNICAL=['seed','draw','runs']

function Parameter({ control, value, reference, onChange, t }: { control: Control; reference: Values[string]; value: Values[string]; onChange: (value: string | number) => void; t: Translate }) {
  const id = `control-${control.key}`
  const technical=TECHNICAL.includes(control.key)
  const basis=control.key==='runs'?'A calculation setting, not a social or policy variable.':technical?'A numbered selection, not a social or policy variable.':control.type==='select'?'Named alternatives change model assumptions; they are not an uncertainty interval.':control.min===0&&control.max===1?'Zero and one bound this model’s fraction or intensity scale. The reference setting and real-world effects still require supporting evidence.':'Exploratory endpoints chosen for this interface. A supported historical or policy uncertainty interval has not been established.'
  const format=(v:Values[string])=>typeof v==='number'&&control.format?t(control.format(v)):t(control.options?.[String(v)]??String(v))
  return <div className="parameter">
    <label htmlFor={id} className="parameter-heading"><span>{t(control.label)}</span>{control.format && typeof value === 'number' && <output htmlFor={id}>{t(control.format(value))}</output>}</label>
    {control.type === 'select' ? <span className="select-wrap"><select aria-describedby={`${id}-note`} id={id} value={String(value)} onChange={event => onChange(event.target.value)}>{Object.entries(control.options ?? {}).map(([key, label]) => <option key={key} value={key}>{t(label)}</option>)}</select></span>
      : <input id={id} type={control.type} min={control.min} max={control.max} step={control.step} value={Number(value)} onChange={event => { if (event.target.validity.valid) onChange(event.target.valueAsNumber) }} required aria-describedby={`${id}-note`} />}
    <small id={`${id}-note`}>{t(control.note)}</small>
    <details className="parameter-rationale"><summary>{t('Why these choices?')}</summary><small><strong>{t('Reference setting')}: </strong>{format(reference)}. {t('The reference is a model comparison point; it is not automatically a best estimate.')}</small>
    <small><strong>{t('Why these choices?')} </strong>{t(basis)} {control.type!=='select'&&<span>{format(control.min)} → {format(control.max)}</span>}</small></details>
  </div>
}

export function Workbench({ world, values, onChange, onReset, onHandoff, navigate, t }: {
  world: World
  values: Values
  onChange: (values: Values) => void
  onReset: () => void
  onHandoff: (values: Values) => void
  navigate: (id: string) => void
  t: Translate
}) {
  const [showMethod, setShowMethod] = useState(false)
  const [playState, setPlayState] = useState<'idle'|'playing'|'paused'|'done'>('idle')
  const [playIndex, setPlayIndex] = useState(0)
  const [pinnedScenario, setPinnedScenario] = useState<{values:Values;metrics:View['metrics'];heading:string}|null>(null)
  const {result,pending,recompute,error,runNumber}=useModelRun(world.id,values)
  const guideIndex = guideData.findIndex(step => step[0] === world.id)
  const guide = guideData[guideIndex]
  const previous = guideData[guideIndex - 1]
  const next = guideData[guideIndex + 1]

  const current=result?.current, baseline=result?.baseline
  const reference=result?.reference ?? world.defaults
  const view:View=result?world.view(current as never,baseline as never):{heading:'Model output',metrics:[],note:''}
  const timeline = useMemo(() => world.stored ? [] : [...new Set((view.lines??[]).filter(line=>line.points.length>1).flatMap(line=>line.points.map(point=>point[0])))].sort((a,b)=>a-b), [result, world.id, world.stored])
  const playbackX = playState === 'playing' || playState === 'paused' ? timeline[playIndex] : undefined
  const playbackValues = playbackX === undefined ? [] : (view.lines??[]).map(line=>({line,point:line.points.find(point=>point[0]===playbackX)})).filter(item=>item.point)
  const playbackAxis = view.xTitle ?? (['cambodia','teachers','sector','absorption','angkor','monsoon','mandala'].includes(world.id) ? 'Year' : ['signalling','obligations'].includes(world.id) ? 'Round' : world.id==='cohort' ? 'Grade' : world.id==='lays' ? 'Age' : 'Simulation step')
  useEffect(() => { setPlayState('idle'); setPlayIndex(0) }, [world.id])
  useEffect(() => {
    if (!result || timeline.length < 2 || playState !== 'idle') return
    if (window.matchMedia('(prefers-reduced-motion: reduce)').matches) { setPlayState('done'); return }
    const timer = window.setTimeout(() => { setPlayIndex(0); setPlayState('playing') }, 350)
    return () => window.clearTimeout(timer)
  }, [result, timeline, playState])
  useEffect(() => {
    if (playState !== 'playing') return
    const timer = window.setTimeout(() => {
      if (playIndex >= timeline.length - 1) setPlayState('done')
      else setPlayIndex(index => index + 1)
    }, Math.max(55, Math.min(150, 5000 / timeline.length)))
    return () => window.clearTimeout(timer)
  }, [playState, playIndex, timeline])
  useEffect(() => {
    const pauseWhenHidden = () => { if (document.hidden) setPlayState(state => state === 'playing' ? 'paused' : state) }
    document.addEventListener('visibilitychange', pauseWhenHidden)
    return () => document.removeEventListener('visibilitychange', pauseWhenHidden)
  }, [])
  const stopPlayback = () => setPlayState('done')
  const changeValues = (next:Values) => { stopPlayback(); onChange(next) }
  const launches=result&&world.id==='campaign'?(current as {rows:{campaignStarted:boolean}[]}).rows.filter(r=>r.campaignStarted).length:undefined
  const headline=world.id==='campaign'&&result?[view.metrics[1],view.metrics[2],view.metrics[7]]:view.metrics.slice(0,3)
  const selectedHistory=result&&['accounts','maintenance','flight'].includes(world.id)?(current as {rows:number[][];baseline:number[][]}):null
  const referenceView=result?world.view(baseline as never,baseline as never):view
  const atReference=!!result&&JSON.stringify(result.values)===JSON.stringify(reference)
  // Comparison cards read zero at the reference run; say so instead of showing a bare 0.
  const idle=(metric:{label:string;value:string})=>atReference&&/change|avoided|\bvs\b/i.test(metric.label)&&/^[+−-]?0(\.0+)?( ?pp| ?%)?$/.test(String(metric.value).trim())
  const evidence=typeof world.evidence==='function'?world.evidence(result?.values??values):world.evidence

  const exportRun = () => {
    if(!result)return
    download(JSON.stringify({
      protocol: 'Atlas Worlds React 2', world: world.id, modelVersion: world.version,
      mode: world.stored ? 'stored experiment' : 'live simulation',
      sourceSha256: Object.fromEntries([...new Set([...world.engines,'worlds.js','institution-worlds.js'])].map(file => {if(!sourceHashes[file])throw Error('Missing source hash: '+file);return [file, sourceHashes[file]]})),
      comparison:result.comparison,
      controls: result.values, referenceControls: reference, current, reference: baseline,
    }, null, 2), 'application/json', `atlas-${world.id}.json`)
  }

  return <main id="main-content" className="workbench shell">
    <div className="workbench-topline"><button className="back-link" onClick={() => navigate(guideIndex >= 0 ? 'angkor-guide' : '')}><ArrowLeft size={17} />{t(guideIndex >= 0 ? 'Guided sequence' : 'Back to library')}</button><span>{t(world.meta)}</span></div>
    <header className="world-header">
      <div><p className="eyebrow">{guide ? t(guide[1]) : t('THE ATLAS OF EDUCATION · MODEL LAB')}</p><h1>{t(world.title)}</h1><p>{t(world.question)}</p></div>
      <span className={`mode ${world.stored ? 'stored' : ''}`}><i />{t(world.stored ? 'Stored results' : 'Live model')}</span>
    </header>

    <div className="model-start">{result&&<ModelNarrative world={world} view={view} referenceView={referenceView} values={result.values} referenceControls={reference} onChange={changeValues} t={t} pending={pending} campaignLaunches={launches}/>}<nav><a href="#result-title">{t('Results')}</a><a href="#controls-title">{t('Controls')}</a><a href="#model-explanation">{t('About the models')}</a></nav></div>
    <div className="workspace">
      <aside className="controls-panel" aria-labelledby="controls-title">
        <div className="panel-heading"><div><span className="panel-kicker">{t('Scenario')}</span><h2 id="controls-title">{t(world.stored ? 'Choose a comparison' : 'Controls')}</h2></div><button className="icon-button" onClick={() => {stopPlayback();onReset()}} title={t('Reset')} aria-label={t('Reset')}><RotateCcw size={17} /></button></div>
        <div className="run-controls"><p>{t('Change a control to calculate automatically. You can also run the current settings again.')}</p><button className="button button-secondary" onClick={recompute}>{t(error?'Retry calculation':'Recompute results')}<RotateCcw size={16}/></button><p role="status" aria-live="polite">{t(error?'Calculation failed':pending?'Updating…':'Calculation complete')}{!pending&&runNumber>0?` · #${runNumber}`:''}</p></div>
        <div className="parameters">
          {world.id === 'monsoon' ? <details className="technical-controls" open><summary>{t('Technical assumptions and parameter draw')}</summary>{world.controls.filter(control=>!TECHNICAL.includes(control.key)).map(control => <Parameter key={control.key} control={control} value={values[control.key]} reference={reference[control.key]} onChange={value => changeValues({ ...values, [control.key]: value })} t={t} />)}</details>
            : world.controls.filter(control=>!TECHNICAL.includes(control.key)).map((control,index,list) => <div key={control.key} className="parameter-slot">{control.group&&control.group!==list[index-1]?.group&&<h3 className="parameter-group">{t(control.group)}</h3>}<Parameter control={control} value={values[control.key]} reference={reference[control.key]} onChange={value => changeValues({ ...values, [control.key]: value })} t={t} /></div>)}
          {world.controls.some(c=>TECHNICAL.includes(c.key))&&<details className="technical-controls"><summary>{t('Reproducibility and stored-run selection')}</summary>{world.controls.filter(c=>TECHNICAL.includes(c.key)).map(control=><Parameter key={control.key} control={control.type==='select'?control:{...control,type:'number'}} value={values[control.key]} reference={reference[control.key]} onChange={value=>onChange({...values,[control.key]:value})} t={t}/>)}</details>}
        </div>
        {world.id === 'signalling' && <button className="button button-secondary handoff" onClick={() => onHandoff(values)}>{t('Use this run in Obligations')}<ArrowRight size={16} /></button>}
        {world.id === 'obligations' && <p className="upstream-note">{t(values.upstream ? 'Using your signalling settings' : 'Using the reference signalling settings')}</p>}
        <div className="control-foot"><span aria-live="polite" className={pending ? 'computing active' : 'computing'}><i />{t(pending ? 'Updating…' : 'Ready')}</span><p>{t(world.stored ? 'Exploring completed simulations' : 'Calculations run in a browser worker')}</p></div>
      </aside>

      <section className="results-panel" aria-labelledby="result-title">
        {error&&<p role="alert">{t(error)}</p>}{!result&&<p role="status">{t(error?'Retry calculation':'Calculating the model…')}</p>}{pending&&result&&<p role="status">{t('Showing the previous completed run while the new settings calculate.')}</p>}{result&&<><div className="panel-heading results-heading"><div><span className="panel-kicker">{t('Model output')}</span><h2 id="result-title">{t(view.heading)}</h2></div><div className="result-header-actions"><button className="button button-quiet" onClick={()=>{stopPlayback();setPinnedScenario({values:result.values,metrics:view.metrics,heading:view.heading})}} disabled={pending}><Pin size={16}/>{t('Pin scenario')}</button><button className="button button-quiet" onClick={exportRun} disabled={pending}><Download size={16} />{t('Save run JSON')}</button></div></div>
        <p className="comparison-scope">{t(result.comparison?.plot??'')} {t(result.comparison?.scope??'')}</p>{pinnedScenario&&<section className="scenario-compare" aria-label={t('Pinned scenario comparison')}><div className="split-heading"><div><span className="panel-kicker">{t('Pinned scenario')}</span><h3>{t(pinnedScenario.heading)}</h3></div><button className="icon-button" onClick={()=>setPinnedScenario(null)} aria-label={t('Clear pinned scenario')}><X size={16}/></button></div><div className="table-scroll"><table><thead><tr><th>{t('Measure')}</th><th>{t('Pinned')}</th><th>{t('Current')}</th></tr></thead><tbody>{pinnedScenario.metrics.filter(metric=>headline.some(currentMetric=>currentMetric.label===metric.label)).map(metric=>{const currentMetric=headline.find(item=>item.label===metric.label)!;return <tr key={metric.label}><th>{t(metric.label)}</th><td>{t(String(metric.value))}</td><td className={String(metric.value)!==String(currentMetric.value)?'changed-value':''}>{t(String(currentMetric.value))}</td></tr>})}</tbody></table></div><p>{t('Changed assumptions')}: {world.controls.filter(control=>JSON.stringify(pinnedScenario.values[control.key])!==JSON.stringify(result.values[control.key])).map(control=>t(control.label)).join(', ')||t('None')}</p></section>}{selectedHistory&&<p>{t('Selected history: state-linked population')} <strong>{Math.round(selectedHistory.rows.at(-1)![1])}</strong>; {t('plotted reference')} <strong>{Math.round(selectedHistory.baseline.at(-1)![1])}</strong>. {t('The cards below summarize the ensemble.')}</p>}{timeline.length>1&&<div className="playback-bar"><div><strong>{t(playState==='playing'?'Playing the completed run':playState==='paused'?'Playback paused':'Completed run ready')}</strong><p>{t('A time cursor reveals actual calculated points on fixed axes. Change any control to stop playback and test a scenario.')}</p></div><button className="button button-secondary" onClick={()=>playState==='playing'?setPlayState('paused'):(playState!=='paused'&&setPlayIndex(0),setPlayState('playing'))}>{playState==='playing'?<Pause size={15}/>:<Play size={15}/>} {t(playState==='playing'?'Pause':playState==='paused'?'Resume':'Replay run')}</button>{playbackX!==undefined&&<input className="playback-scrubber" type="range" min="0" max={timeline.length-1} step="1" value={playIndex} aria-label={t('Inspect calculated step')} onChange={event=>{setPlayIndex(Number(event.target.value));setPlayState('paused')}}/>}{playbackX!==undefined&&<div className="playback-readout"><strong>{t(playbackAxis)}: {world.id==='china'?`${Math.floor(playbackX)}-${String(Math.floor((playbackX%1)*12)+1).padStart(2,'0')}`:Number(playbackX.toFixed(3))}</strong>{playbackValues.map(({line,point})=><span key={line.name}>{t(line.name)} <b>{view.axis?.(point![1])??point![1].toFixed(1)}</b></span>)}</div>}</div>}<p className="metric-scope">{t('Final-run summary cards · chart values above follow the time cursor')}</p><div className="metrics">{headline.map(metric => <div className={idle(metric)?'metric idle':'metric'} key={metric.label}><span>{t(metric.label)}</span><strong>{t(String(metric.value))}</strong><small>{idle(metric)?t('Reference run. Change a control to compare.'):t(metric.detail)}</small></div>)}</div>
        {view.table ? <div className="table-scroll"><table><thead><tr>{view.table.head.map(label => <th scope="col" key={label}>{t(label)}</th>)}</tr></thead><tbody>{view.table.rows.map(row => <tr key={row.cells[0]} className={row.selected ? 'selected' : ''}><th scope="row">{t(row.cells[0])}</th>{row.cells.slice(1).map((cell, index) => <td key={index}>{t(cell)}</td>)}</tr>)}</tbody></table></div> : <DataChart view={view} t={t} worldId={world.id} playbackX={playbackX} playing={playState==='playing'||playState==='paused'} />}
        {view.metrics.length>3&&<details className="additional-results"><summary>{t('More results')}</summary><div className="metrics">{view.metrics.filter(m=>!headline.includes(m)).map(metric=><div className="metric" key={metric.label}><span>{t(metric.label)}</span><strong>{t(String(metric.value))}</strong><small>{t(metric.detail)}</small></div>)}</div></details>}
        <p className="chart-note">{t(view.note)}</p>
        <div className="result-actions">{world.csv && <button className="text-button" disabled={pending} onClick={() => download(world.csv!(current), 'text/csv', `atlas-${world.id}.csv`)}><Download size={15} />{t('Save model results CSV')}</button>}<button className="text-button" onClick={() => {setShowMethod(!showMethod);if(!showMethod)setTimeout(()=>document.getElementById('method')?.scrollIntoView({block:'start'}),0)}} aria-expanded={showMethod}>{t('Method & limitations')}<ArrowRight size={15} /></button></div>
        <p className="sr-only" role="status">{view.metrics.map(metric => `${t(metric.label)} ${t(String(metric.value))}`).join('. ')}</p></>}
      </section>
    </div>

    <details className="model-explanation" id="model-explanation"><summary>{t('About the models')}</summary><p>{t((stories as Record<string,string>)[world.id])}</p><h3>{t('What stays fixed?')}</h3><p>{t('Each comparison holds the other controls at their selected settings. Unshown equations and assumptions remain in force. Open the assumptions below before interpreting a result.')}</p><a href="research/control-audit.json">{t('Download the control audit')}</a></details>
    {result&&<ModelQuestions world={world} values={result.values} view={view} t={t}/>}
    <details className="evidence-section" id="method" open={showMethod} onToggle={event=>setShowMethod(event.currentTarget.open)}><summary>{t('EVIDENCE & ASSUMPTIONS')}</summary>
      <div className="evidence-heading"><p className="eyebrow">{t('EVIDENCE & ASSUMPTIONS')}</p><h2>{t('What the model has to answer to')}</h2><p>{world.version}</p></div>
      <div className="evidence-list">{evidence.map((item, index) => <article key={item.title} className={item.flag ? 'flag' : ''}><span>{String(index + 1).padStart(2, '0')}</span><div><h3>{t(item.title)}</h3><p>{t(item.body)}</p></div></article>)}</div>
      <div className="source-links">{world.links.map(([label, href]) => <a key={href} href={href} {...(href.startsWith('http') ? { target: '_blank', rel: 'noreferrer' } : {})}>{t(label)}<ArrowUpRight size={15} /></a>)}{world.id === 'provisioning' && <a href="research/provisioning-paper.pdf">{t('Download model paper')}<Download size={15} /></a>}</div>
    </details>

    {guideIndex >= 0 && <nav className="step-pagination" aria-label={t('Guided sequence')}>
      <button onClick={() => navigate(previous?.[0] ?? 'angkor-guide')}><ArrowLeft size={18} /><span><small>{t('Previous')}</small>{t(previous?.[1] ?? 'Sequence overview')}</span></button>
      <button onClick={() => navigate(next?.[0] ?? 'angkor-guide')}><span><small>{t('Next step')}</small>{t(next?.[1] ?? 'Sequence overview')}</span><ArrowRight size={18} /></button>
    </nav>}
  </main>
}
