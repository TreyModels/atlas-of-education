#!/usr/bin/env node
// Link-destination guard for the Atlas Worlds catalogue.
//
// The bug this prevents: a catalogue entry whose *primary* click points straight
// at a file (.zip/.pdf/.csv/.json/...) so clicking a model starts a download.
// Rule: `href` is a page (or external URL); any file goes in `downloadHref` and
// is rendered as a separate, explicitly labelled download action.
//
// Checks:
//   1. every literal catalogue entry has a page/route primary target;
//   2. no primary `href` ends in a file extension;
//   3. every `downloadHref` has a page/route primary and an existing local file;
//   4. every local `.html` page target exists in public/.
//
// Usage: node scripts/check-link-destinations.cjs   (wired into scripts/check-all.sh)
const fs = require('node:fs')
const path = require('node:path')

const root = path.join(__dirname, '..')
const source = fs.readFileSync(path.join(root, 'src/data/model-catalogue.ts'), 'utf8')
const FILE_EXT = /\.(zip|pdf|csv|json|xlsx?|docx?|gz|tar|tgz)([?#].*)?$/i

const errors = []
const rows = []
for (const line of source.split('\n')) {
  const idMatch = line.match(/\{\s*id:\s*'([^']+)'/)
  if (!idMatch) continue
  // Catalogue rows always carry a `family: '…'` field; this skips nav groups etc.
  if (!/family:\s*'/.test(line)) continue
  const get = key => {
    const match = line.match(new RegExp(`${key}:\\s*'([^']*)'`))
    return match ? match[1] : undefined
  }
  const id = idMatch[1]
  const route = get('route')
  const href = get('href')
  const downloadHref = get('downloadHref')
  rows.push({ id, route, href, downloadHref })

  if (!route && !href) errors.push(`${id}: has no page or route as its primary destination`)
  if (href && FILE_EXT.test(href)) errors.push(`${id}: primary href points at a file (${href}) — move it to downloadHref`)
  if (downloadHref && !route && !href) errors.push(`${id}: has a download but no page/route primary`)
  if (downloadHref) {
    if (!/^(research\/|reference\/|https?:\/\/)/.test(downloadHref)) {
      errors.push(`${id}: unexpected downloadHref (${downloadHref})`)
    } else if (!/^https?:/.test(downloadHref)) {
      const local = path.join(root, 'public', downloadHref)
      if (!fs.existsSync(local)) errors.push(`${id}: downloadHref file is missing: public/${downloadHref}`)
    }
  }
  if (href && !/^https?:/.test(href) && /\.html([?#].*)?$/.test(href)) {
    const page = path.join(root, 'public', href.split('#')[0].split('?')[0])
    if (!fs.existsSync(page)) errors.push(`${id}: page target is missing: public/${href.split('#')[0]}`)
  }
}

const pagePrimaries = rows.filter(row => row.route || row.href).length
const downloads = rows.filter(row => row.downloadHref).length
console.log(`catalogue entries scanned: ${rows.length} · page primaries: ${pagePrimaries} · secondary downloads: ${downloads}`)
if (errors.length) {
  console.error('Link destination check FAILED:')
  for (const error of errors) console.error(' - ' + error)
  process.exit(1)
}
console.log('Link destination check: ok — no primary file links; every download has a page and an existing file.')
