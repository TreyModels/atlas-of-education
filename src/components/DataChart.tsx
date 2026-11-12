import { useMemo, useRef, useState } from 'react'
import type { Translate, View } from '../types'

const COLORS = { live: '#176b52', reference: '#68736c', observed: '#a6532c', alternate: '#a6532c', contrast: '#3f6a8c' }

export function DataChart({ view, t, worldId, playbackX, playing = false }: { view: View; t: Translate; worldId?: string; playbackX?: number; playing?: boolean }) {
  const svgRef = useRef<SVGSVGElement>(null)
  const [showTable,setShowTable]=useState(false)
  const [pinned,setPinned]=useState(false)
  const [cursor, setCursor] = useState<number | null>(null)
  const labelX=(x:number)=>worldId==='china'?`${Math.floor(x)}-${String(Math.floor((x%1)*12)+1).padStart(2,'0')}`:worldId==='campaign'?`${Math.floor(x)} · ${Math.round((x%1)*3)+1}`:String(Number(x.toFixed(3)))
  const allLines = view.lines ?? []
  const lines = playing && playbackX !== undefined ? allLines.map(line => ({ ...line, points: line.points.filter(point => point[0] <= playbackX) })) : allLines
  const chart = useMemo(() => {
    const points = allLines.flatMap(line => line.points).filter(point => Number.isFinite(point[1]))
    const observations = points.map(point => point[1]).concat(view.band ? view.band.points.flatMap(([, low, , high]) => [low, high]) : [])
    const xmin = Math.min(...points.map(point => point[0]))
    const xmax = Math.max(...points.map(point => point[0]))
    const min = Math.min(...observations), max = Math.max(...observations)
    const padding = (max - min) * 0.1 || 1
    const lo = view.yZero && min >= 0 ? 0 : Math.max(min >= 0 ? 0 : -Infinity, min - padding), hi = max + padding
    const left = 66, right = 760, top = 20, bottom = 278
    const x = (year: number) => left + (year - xmin) / (xmax - xmin || 1) * (right - left)
    const y = (value: number) => bottom - (value - lo) / (hi - lo || 1) * (bottom - top)
    return { xmin, xmax, lo, hi, left, right, top, bottom, x, y }
  }, [allLines, view.band, view.yZero])

  const move = (clientX: number) => {
    const bounds = svgRef.current?.getBoundingClientRect()
    if (!bounds) return
    const svgX = (clientX - bounds.left) / bounds.width * 800
    const ratio = (svgX - chart.left) / (chart.right - chart.left)
    setCursor(Math.max(chart.xmin, Math.min(chart.xmax, chart.xmin + ratio * (chart.xmax - chart.xmin))))
  }

  const nearest = (points: [number, number][], year: number) => points.reduce((best, point) => Math.abs(point[0] - year) < Math.abs(best[0] - year) ? point : best, points[0])
  const inspectionX = playbackX ?? cursor
  const active = inspectionX === null || inspectionX === undefined ? null : lines.map(line => ({ line, point: line.points.length ? nearest(line.points, inspectionX) : null })).filter(item => item.point)
  const grid=[...new Set(lines.filter(l=>l.points.length>1).flatMap(l=>l.points.map(p=>p[0])))].sort((a,b)=>a-b)
  const activeYear = inspectionX===null||inspectionX===undefined?undefined:grid.reduce((best,x)=>Math.abs(x-inspectionX)<Math.abs(best-inspectionX)?x:best,grid[0]??inspectionX)
  // Whole-number series (years, grades, counts) get whole-number ticks instead of 2027.75-style labels.
  const integerX = grid.length > 0 && grid.every(x => Number.isInteger(x))
  const xTicks = integerX ? (() => { const span = chart.xmax - chart.xmin, step = Math.max(1, Math.ceil(span / 5)); const ticks: number[] = []; for (let x = chart.xmin; x <= chart.xmax; x += step) ticks.push(x); if (ticks.at(-1) !== chart.xmax && chart.xmax - ticks.at(-1)! >= step / 2) ticks.push(chart.xmax); else if (ticks.at(-1) !== chart.xmax) ticks[ticks.length - 1] = chart.xmax; return ticks })()
    : Array.from({ length: 5 }, (_, index) => chart.xmin + (chart.xmax - chart.xmin) * index / 4)
  const yTicks = Array.from({ length: 5 }, (_, index) => chart.lo + (chart.hi - chart.lo) * index / 4)
  const pathFor = (points: [number, number][]) => {
    let path = '', previous: number | undefined
    for (const [year, value] of points) {
      if (!Number.isFinite(value)) { previous = undefined; continue }
      const start = previous === undefined || view.breaks?.some(yearBreak => previous! < yearBreak && yearBreak <= year)
      path += `${start ? 'M' : 'L'}${chart.x(year).toFixed(2)} ${chart.y(value).toFixed(2)}`
      previous = year
    }
    return path
  }

  return <div className="chart-wrap">
    <div className="chart-legend" aria-label={t('Chart legend')}>
      {lines.map(line => <span key={line.name}><i className={`legend-${line.style}`} style={{ '--series': COLORS[line.style] } as React.CSSProperties} />{t(line.name)}</span>)}
      {view.band && <span><i className="legend-band" />{t(view.band.name)}</span>}
    </div>
    <div className="chart-canvas">
      <svg ref={svgRef} className="data-chart" viewBox={`0 0 800 ${view.xTitle ? 340 : 320}`} role="img" aria-label={t(view.heading)} onPointerMove={event => move(event.clientX)} tabIndex={0} onClick={()=>setPinned(!pinned)} onKeyDown={event=>{if(!['ArrowLeft','ArrowRight','Home','End'].includes(event.key))return;event.preventDefault();const i=grid.findIndex(x=>x===(activeYear??grid[0]));setPinned(true);setCursor(event.key==='Home'?grid[0]:event.key==='End'?grid.at(-1)!:grid[Math.max(0,Math.min(grid.length-1,i+(event.key==='ArrowRight'?1:-1)))])}} onPointerLeave={() => {if(!pinned)setCursor(null)}}>
        <title>{t(view.heading)}</title>
        <desc>{t(view.note)}</desc>
        {yTicks.map((tick, index) => <g key={index}><line className="chart-grid" x1={chart.left} x2={chart.right} y1={chart.y(tick)} y2={chart.y(tick)} /><text x="54" y={chart.y(tick) + 4} textAnchor="end">{view.axis?.(tick) ?? tick.toFixed(1)}</text></g>)}
        {xTicks.map((tick, index) => <text key={index} x={chart.x(tick)} y="306" textAnchor="middle">{labelX(tick)}</text>)}
        {view.xTitle && <text className="axis-title" x={(chart.left + chart.right) / 2} y="334" textAnchor="middle">{t(view.xTitle)}</text>}
        {view.breaks?.map(yearBreak => <g key={yearBreak}><line className="chart-break" x1={chart.x(yearBreak)} x2={chart.x(yearBreak)} y1={chart.top} y2={chart.bottom} /><text className="break-label" x={chart.x(yearBreak) + 7} y="34">{yearBreak}</text></g>)}
        {view.band && <polygon className="chart-band" points={view.band.points.filter(([year])=>!playing||playbackX===undefined||year<=playbackX).map(([year, , , high]) => `${chart.x(year)},${chart.y(high)}`).concat([...view.band.points.filter(([year])=>!playing||playbackX===undefined||year<=playbackX)].reverse().map(([year, low]) => `${chart.x(year)},${chart.y(low)}`)).join(' ')} />}
        {lines.map(line => line.style === 'observed'
          ? <g key={line.name}>{line.points.map(([year, value], index) => <circle key={index} cx={chart.x(year)} cy={chart.y(value)} r="3" fill={COLORS.observed} />)}</g>
          : <path key={line.name} d={pathFor(line.points)} stroke={COLORS[line.style]} className={line.style === 'reference' ? 'reference-line' : ''} />)}
        {active && <line className="chart-cursor" x1={chart.x(activeYear!)} x2={chart.x(activeYear!)} y1={chart.top} y2={chart.bottom} />}
        {active?.map(({ line, point }) => line.style !== 'observed' && <circle key={line.name} cx={chart.x(point![0])} cy={chart.y(point![1])} r="4.5" fill={COLORS[line.style]} stroke="var(--surface)" strokeWidth="2" />)}
      </svg>
      {active && <div className={`chart-tooltip ${chart.x(activeYear!) > 570 ? 'align-right' : ''}`} style={{ left: `${(chart.x(activeYear!) / 800) * 100}%` }}>
        <strong>{labelX(activeYear!)}</strong>
        {active.map(({ line, point }) => <span key={line.name}><i style={{ background: COLORS[line.style] }} />{t(line.name)} ({labelX(point![0])}) <b>{view.axis?.(point![1]) ?? point![1].toFixed(1)}</b></span>)}
      </div>}
    </div>
    <div className="chart-actions"><button className="text-button" onClick={()=>{const rows=['series,x,x_label,y',...lines.flatMap(l=>l.points.map(([x,y])=>[JSON.stringify(l.name),x,JSON.stringify(labelX(x)),y].join(',')))];const url=URL.createObjectURL(new Blob([rows.join('\n')],{type:'text/csv'}));const a=document.createElement('a');a.href=url;a.download=`atlas-${worldId??'chart'}-plotted-data.csv`;a.click();setTimeout(()=>URL.revokeObjectURL(url),1000)}}>{t('Export plotted data CSV')}</button>
    <button className="text-button" onClick={()=>setShowTable(!showTable)} aria-expanded={showTable}>{t('Inspect chart data')}</button></div>
    {showTable&&<div className="table-scroll"><table><thead><tr><th>{t('Observation')}</th>{lines.map(l=><th key={l.name}>{t(l.name)}</th>)}</tr></thead><tbody>{[...new Set(lines.flatMap(l=>l.points.map(p=>p[0])))].sort((a,b)=>a-b).map(x=><tr key={x}><th>{labelX(x)}</th>{lines.map(l=><td key={l.name}>{l.points.find(p=>p[0]===x)?.[1]??'—'}</td>)}</tr>)}</tbody></table></div>}
  </div>
}
