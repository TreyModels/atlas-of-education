// shard.js — core-sharded runner for the full Angkor sensitivity study.
// Usage: node scripts/shard.js <mc|morris> <total> <cores> <tag>
// Each shard is a separate child process with a disjoint index block,
// so parts can be concatenated without overlap.
'use strict';
const fs = require('fs');
const path = require('path');
const { spawn } = require('child_process');
const ROOT = path.resolve(__dirname, '..');
const MODE = process.argv[2] || 'mc';
const TOTAL = parseInt(process.argv[3] || '120000', 10);
const CORES = parseInt(process.argv[4] || '96', 10);
const TAG = process.argv[5] || MODE;

const per = Math.ceil(TOTAL / CORES);
const t0 = Date.now();
let done = 0, started = 0;
const procs = [];
const outDir = path.join(ROOT, 'results', TAG + '_parts');
fs.mkdirSync(outDir, { recursive: true });

for (let c = 0; c < CORES; c++) {
  const lo = c * per, hi = Math.min(TOTAL, (c + 1) * per);
  if (lo >= hi) break;
  started++;
  const out = path.join(outDir, 'part_' + String(c).padStart(3, '0') + '.csv');
  const child = spawn(process.execPath, [path.join(__dirname, 'worker.js'), MODE, String(lo), String(hi), out],
    { stdio: ['ignore', 'ignore', 'pipe'] });
  child.stderr.on('data', d => { const s = d.toString().trim(); if (s) console.error('[shard ' + c + '] ' + s.slice(0, 300)); });
  const onExit = code => {
    done++;
    if (code !== 0) console.error('[shard done] code=' + code);
    if (done % 8 === 0 || done === started)
      console.log(done + '/' + started + ' shards, ' + ((Date.now() - t0) / 1000).toFixed(0) + 's');
    if (done === started) { console.log('all shards done in ' + ((Date.now() - t0) / 1000).toFixed(0) + 's'); process.exit(0); }
  };
  child.on('exit', onExit);
  procs.push(child);
}
