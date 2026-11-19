#!/usr/bin/env node
// DeepSeek fleet runner. Runs coding tasks against DeepSeek (Flash by default), writes the
// returned files into a local checkout, runs checks, and prints a compact report.
//   node fleet.mjs init <api-key>          store key (mode 600) in ../.deepseek_key
//   node fleet.mjs models                  list available models
//   node fleet.mjs run <tasks.json> [-p N] run tasks, N in parallel (default 3)
//   node fleet.mjs show <task-id>          print the full report for one task
// tasks.json: [{ id, repo, prompt, context: [paths], allow: [path globs it may write],
//                checks: ["npm run build", ...], model?, maxTokens? }]
import fs from 'node:fs'
import path from 'node:path'
import { execSync } from 'node:child_process'
import { fileURLToPath } from 'node:url'

const HERE = path.dirname(fileURLToPath(import.meta.url))
const HOME = path.resolve(HERE, '..')
const KEYFILE = path.join(HOME, '.deepseek_key')
const REPORTS = path.join(HOME, 'reports')
const DEFAULT_MODEL = process.env.FLEET_MODEL || 'deepseek-flash'
const [cmd, ...args] = process.argv.slice(2)

const key = () => fs.readFileSync(KEYFILE, 'utf8').trim()
const api = (p, body) => fetch('https://api.deepseek.com' + p, {
  method: body ? 'POST' : 'GET',
  headers: { Authorization: 'Bearer ' + key(), 'Content-Type': 'application/json' },
  body: body && JSON.stringify(body),
}).then(async r => { const j = await r.json(); if (!r.ok) throw Error(r.status + ' ' + JSON.stringify(j).slice(0, 300)); return j })

const SYSTEM = `You are a careful senior engineer working in an existing repository.
Return ONLY complete files, each wrapped exactly like this:
=== FILE: relative/path.ext ===
<entire file content>
=== END FILE ===
After the files, add one block:
=== NOTES ===
<at most 8 short lines: what you did, assumptions, anything uncertain>
=== END NOTES ===
Never return partial files or diffs. Do not change files you were not asked to change.`

function parse(text) {
  const files = [...text.matchAll(/=== FILE: (.+?) ===\n([\s\S]*?)\n=== END FILE ===/g)].map(m => ({ path: m[1].trim(), content: m[2] + '\n' }))
  const notes = (text.match(/=== NOTES ===\n([\s\S]*?)\n=== END NOTES ===/) || [])[1] || ''
  return { files, notes }
}
const allowed = (p, globs) => globs.some(g => g.endsWith('/**') ? p.startsWith(g.slice(0, -3)) : p === g)

async function runTask(t) {
  const started = Date.now()
  const ctx = (t.context || []).map(p => `--- ${p} ---\n${fs.readFileSync(path.join(t.repo, p), 'utf8')}`).join('\n\n')
  const res = await api('/chat/completions', {
    model: t.model || DEFAULT_MODEL, max_tokens: t.maxTokens || 16000, temperature: 0.2, ...(t.thinking === false ? { thinking: { type: 'disabled' } } : {}),
    messages: [{ role: 'system', content: SYSTEM }, { role: 'user', content: `${t.prompt}\n\nRepository files for context:\n\n${ctx}` }],
  })
  const text = res.choices[0].message.content
  const { files, notes } = parse(text)
  const written = [], refused = []
  for (const f of files) {
    if (!allowed(f.path, t.allow || [])) { refused.push(f.path); continue }
    const full = path.join(t.repo, f.path); fs.mkdirSync(path.dirname(full), { recursive: true }); fs.writeFileSync(full, f.content); written.push(f.path)
  }
  const checks = (t.checks || []).map(c => {
    try { const out = execSync(c, { cwd: t.repo, stdio: 'pipe', timeout: 600000 }).toString(); return { c, ok: true, tail: out.split('\n').slice(-4).join('\n') } }
    catch (e) { return { c, ok: false, tail: ((e.stdout || '') + (e.stderr || '')).toString().split('\n').slice(-25).join('\n') } }
  })
  const report = { id: t.id, model: res.model, usage: res.usage, seconds: Math.round((Date.now() - started) / 1000), written, refused, notes, checks, raw: text }
  fs.mkdirSync(REPORTS, { recursive: true }); fs.writeFileSync(path.join(REPORTS, t.id + '.json'), JSON.stringify(report, null, 1))
  return report
}

async function pool(tasks, n) {
  const out = []; let i = 0
  await Promise.all(Array.from({ length: Math.min(n, tasks.length) }, async () => {
    while (i < tasks.length) { const t = tasks[i++]; try { out.push(await runTask(t)) } catch (e) { out.push({ id: t.id, error: e.message }) } }
  }))
  return out
}

if (cmd === 'init') { fs.mkdirSync(HOME, { recursive: true }); fs.writeFileSync(KEYFILE, args[0].trim(), { mode: 0o600 }); console.log('key stored', KEYFILE) }
else if (cmd === 'models') console.log((await api('/models')).data.map(m => m.id).join('\n'))
else if (cmd === 'run') {
  const tasks = JSON.parse(fs.readFileSync(args[0], 'utf8'))
  const n = args.includes('-p') ? Number(args[args.indexOf('-p') + 1]) : 3
  for (const r of await pool(tasks, n)) {
    if (r.error) { console.log(`✗ ${r.id}: ${r.error}`); continue }
    console.log(`${r.checks.every(c => c.ok) ? '✓' : '✗'} ${r.id} · ${r.model} · ${r.usage?.total_tokens} tok · ${r.seconds}s · wrote ${r.written.join(', ') || 'nothing'}${r.refused.length ? ' · REFUSED ' + r.refused.join(', ') : ''}`)
    if (r.notes) console.log('  notes: ' + r.notes.trim().split('\n').join('\n         '))
    for (const c of r.checks) console.log(`  ${c.ok ? 'ok ' : 'FAIL'} ${c.c}${c.ok ? '' : '\n' + c.tail.split('\n').map(l => '      ' + l).join('\n')}`)
  }
}
else if (cmd === 'show') { const r = JSON.parse(fs.readFileSync(path.join(REPORTS, args[0] + '.json'), 'utf8')); delete r.raw; console.log(JSON.stringify(r, null, 1)) }
else if (cmd === 'brief') for (const id of args) { try { const r = JSON.parse(fs.readFileSync(path.join(REPORTS, id + '.json'), 'utf8')); console.log(`${id}: ${r.usage?.completion_tokens} out tok (${r.usage?.completion_tokens_details?.reasoning_tokens} reasoning) · wrote ${r.written.join(', ') || 'NOTHING'}${r.refused.length ? ' · refused ' + r.refused : ''}`); for (const c of r.checks) console.log(`  ${c.ok ? 'ok' : 'FAIL'} ${c.c.slice(0, 50)} :: ${c.tail.trim().slice(-300)}`) } catch (e) { console.log(id + ': no report yet') } }
else if (cmd === 'bg') { const { spawn } = await import('node:child_process'); const log = path.join(HOME, 'reports', 'bg-' + path.basename(args[0]) + '.log'); fs.mkdirSync(path.dirname(log), { recursive: true }); const out = fs.openSync(log, 'w'); spawn(process.execPath, [fileURLToPath(import.meta.url), 'run', ...args], { detached: true, stdio: ['ignore', out, out] }).unref(); console.log('started; log', log) }
else console.log('usage: init <key> | models | run <tasks.json> [-p N] | show <id>')
