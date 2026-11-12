export type Language = 'en' | 'zh-Hans' | 'fr' | 'vi'
export type Translate = (value: string) => string

export type Control = {
  key: string
  label: string
  note: string
  type: 'range' | 'select' | 'number'
  min?: number
  max?: number
  step?: number | 'any'
  options?: Record<string, string>
  format?: (value: number) => string
  group?: string
}

export type Values = Record<string, string | number | undefined | Record<string, unknown>>
export type ChartLine = { name: string; points: [number, number][]; style: 'live' | 'reference' | 'observed' | 'alternate' | 'contrast' }
export type View = {
  heading: string
  metrics: { label: string; value: string; detail: string }[]
  lines?: ChartLine[]
  band?: { name: string; points: [number, number, number, number][] }
  axis?: (value: number) => string
  breaks?: number[]
  xTitle?: string
  yZero?: boolean
  note: string
  table?: { head: string[]; rows: { cells: string[]; selected: boolean }[] }
}

export type World = {
  id: string
  nav: string
  title: string
  meta: string
  question: string
  version: string
  stored?: boolean
  defaults: Values
  controls: Control[]
  engines: string[]
  run: (values: Values) => unknown
  view: (current: never, baseline: never) => View
  evidence: ((values: Values) => { title: string; body: string; flag?: boolean }[]) | { title: string; body: string; flag?: boolean }[]
  links: [string, string][]
  csv?: (current: unknown) => string
}
