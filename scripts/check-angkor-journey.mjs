// Checks the Angkor journey content: structure, labels, links, the Klassen boundary
// language, and the scaling helper. Run: node scripts/check-angkor-journey.mjs
import assert from 'node:assert/strict'
import { existsSync } from 'node:fs'
import { build } from 'esbuild'

async function load(path) {
  const out = await build({ entryPoints: [path], bundle: true, format: 'esm', write: false, platform: 'node', logLevel: 'silent' })
  return import('data:text/javascript;base64,' + Buffer.from(out.outputFiles[0].text).toString('base64'))
}

const { journey, purposeLabel, stateLabel } = await load('src/data/angkor-journey.ts')
const { perPersonIndex } = await load('src/lib/scaling.ts')

// Chapter order and Klassen first.
assert.deepEqual(journey.chapters.map(c => c.id), ['klassen', 'campaign', 'growth', 'signalling', 'obligations', 'climate'])
const k = journey.chapters[0]
assert.equal(k.interactive, 'beta', 'chapter 1 carries the beta comparison')
assert.equal(journey.chapters.filter(c => c.interactive).length, 1, 'sliders only at one "watch this" moment')

// Every chapter tells the full story.
for (const c of journey.chapters) for (const part of ['evidence', 'rule', 'result', 'limitation']) assert.ok(c[part].length > 0, `${c.id}.${part}`)

// Klassen values and boundary sentences must survive edits.
const kText = JSON.stringify(k)
for (const s of ['1.227', '0.023', '7/6', '−0.846', '−0.409', '+0.521', '0.085', '93', '571', '10.1007/s10816-021-09535-5']) assert.ok(kText.includes(s), 'Klassen value missing: ' + s)
for (const s of ['not measured tonnes of rice', 'separate associations', 'not a constant surplus share', 'our hypothesis']) assert.ok(kText.includes(s), 'Klassen boundary missing: ' + s)

// Cards: every referenced model exists and has both labels.
const ids = [...journey.chapters.flatMap(c => c.models), ...journey.deeper]
for (const id of ids) {
  const m = journey.models[id]
  assert.ok(m, 'missing card ' + id)
  assert.ok(purposeLabel[m.purpose], id + ' purpose')
  assert.ok(stateLabel[m.state], id + ' state')
  assert.ok(m.note.length > 20, id + ' note')
}
assert.equal(new Set(ids).size, ids.length, 'each model appears once')

// Relative links resolve to files the site serves.
const rel = [...journey.chapters.flatMap(c => c.sources.map(s => s.href)), ...Object.values(journey.models).flatMap(m => [m.engine, m.research].filter(Boolean))]
for (const href of rel) if (!/^https?:/.test(href)) assert.ok(existsSync('public/' + href), 'broken link: ' + href)

// Scaling helper.
assert.equal(perPersonIndex(100, 1.227), 100)
assert.equal(perPersonIndex(500, 1), 100)
assert.ok(Math.abs(perPersonIndex(500, 1.227) - 144.1) < 0.1, 'N=500 gives 144.1')
assert.ok(perPersonIndex(10, 1.227) < perPersonIndex(100, 1.227) && perPersonIndex(100, 1.227) < perPersonIndex(2000, 1.227), 'increasing in N')
for (const n of [10, 2000]) assert.ok(Number.isFinite(perPersonIndex(n, 1.227)))

// Generic checks for every other family journey.
for (const [file, name] of [['src/data/shadow-journey.ts', 'shadowJourney'], ['src/data/extension-journey.ts', 'extensionJourney'], ['src/data/ccp-journey.ts', 'ccpJourney']]) {
  const j = (await load(file))[name]
  const ids = [...j.chapters.flatMap(c => c.models), ...j.deeper]
  for (const c of j.chapters) for (const part of ['evidence', 'rule', 'result', 'limitation']) assert.ok(c[part].length > 0, `${name} ${c.id}.${part}`)
  for (const id of new Set(ids)) { const m = j.models[id]; assert.ok(m && purposeLabel[m.purpose] && stateLabel[m.state], `${name} card ${id}`) }
  for (const href of [...j.chapters.flatMap(c => c.sources.map(s => s.href)), ...Object.values(j.models).flatMap(m => [m.engine, m.research].filter(Boolean))])
    if (!/^https?:/.test(href)) assert.ok(existsSync('public/' + href), `${name} broken link: ${href}`)
  assert.ok(j.family && j.repo, name + ' family/repo')
  console.log(`${name}: ${j.chapters.length} chapters, ${new Set(ids).size} cards, links ok.`)
}
console.log(`Angkor journey: ${journey.chapters.length} chapters, ${ids.length} model cards, ${rel.length} links checked. Passed.`)
