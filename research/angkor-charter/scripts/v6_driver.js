// v6_driver.js — fan a shard set across all cores.
// Usage: node v6_driver.js <mode> <total> <cores> <tag>
'use strict';
var fs = require('fs');
var path = require('path');
var spawn = require('child_process').spawn;
var MODE = process.argv[2] || 'factorial';
var TOTAL = parseInt(process.argv[3] || '2048', 10);
var CORES = parseInt(process.argv[4] || '90', 10);
var TAG = process.argv[5] || MODE;
var ROOT = '/root/angkor';
var outDir = path.join(ROOT, 'results', TAG + '_parts');
fs.mkdirSync(outDir, { recursive: true });

var per = Math.ceil(TOTAL / CORES), started = 0, done = 0, t0 = Date.now();
for (var c = 0; c < CORES; c++) {
  var lo = c * per, hi = Math.min(TOTAL, (c + 1) * per);
  if (lo >= hi) break;
  started++;
  var out = path.join(outDir, 'part_' + String(c).padStart(3, '0') + '.csv');
  var ch = spawn(process.execPath, [path.join(ROOT, 'scripts/v6_worker.js'), MODE, String(lo), String(hi), out],
    { stdio: ['ignore', 'ignore', 'pipe'] });
  ch.stderr.on('data', function (d) { var s = d.toString().trim(); if (s) console.error(s.slice(0, 200)); });
  ch.on('exit', (function (code) {
    return function () {
      done++;
      if (done % 10 === 0 || done === started) console.log(done + '/' + started + ' shards, ' + ((Date.now() - t0) / 1000).toFixed(0) + 's');
      if (done === started) { console.log('done ' + ((Date.now() - t0) / 1000).toFixed(0) + 's'); process.exit(0); }
    };
  })(c));
}
