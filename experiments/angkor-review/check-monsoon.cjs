// Review 5.2: the monsoon sweep is kept unchanged. This script recomputes the decline counts from the
// engine (2000 draws per sensitivity) to check the stored summary and to show the result depends on the sensitivity value.
'use strict';
const fs = require('fs'), vm = require('vm'), path = require('path');
const dir = process.env.ENGINE_DIR || path.join(__dirname, '../../public/engines');
const c = vm.createContext({});
vm.runInContext(fs.readFileSync(path.join(dir, 'monsoon.js'), 'utf8'), c);
const M = c.AngkorMonsoon;
const out = {};
for (const sens of [0, 0.04, 0.07, 0.10]) {
  let declines = 0, deep = 0, moatLost = 0, onsets = [];
  for (let draw = 1; draw <= 2000; draw++) {
    const r = M.run({sensitivity: sens, draw});
    if (r.score.onset !== null) { declines++; onsets.push(r.score.onset); }
    if (r.score.deep !== null) deep++;
    if (r.score.moatLost !== null) moatLost++;
  }
  onsets.sort((a, b) => a - b);
  out[sens.toFixed(2)] = {n: 2000, onsetDeclines: declines, deepDeclines: deep, moatLost, medianOnset: onsets.length ? onsets[Math.floor(onsets.length / 2)] : null,
    storedSummary: M.run({sensitivity: sens, draw: 1}).summary};
}
console.log(JSON.stringify(out, null, 2));
