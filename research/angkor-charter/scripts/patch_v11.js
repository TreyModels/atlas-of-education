// patch_v11.py — Angkor model v1.1: two mechanism changes, nothing else touched.
//   1. grain stock (1-3 yr granary) so a bad year does not zero the army
//   2. army payment from the stock and from crown dues, not only from surplus
// Everything else (parameters, presets, spatial grid, rivals, monuments) is unchanged.
// Writes model_v11.js.
'use strict';
const fs = require('fs');
const path = require('path');
const ROOT = path.resolve(__dirname, '..');
let s = fs.readFileSync(path.join(ROOT, 'model.js'), 'utf8');
const before = s;

// --- 1. state: add a granary ---
// state object (search-anchored on a unique literal)
const stateAnchor = "const state={cells,courtLegitimacy:.72,shrine:.49,bonded:p.bonded,monument:0,wars:0,sacks:0,victories:0,defeats:0,shockYears:[]};";
if (s.indexOf(stateAnchor) < 0) throw new Error('state anchor missing');
s = s.replace(stateAnchor,
  "const state={cells,courtLegitimacy:.72,shrine:.49,bonded:p.bonded,monument:0,wars:0,sacks:0,victories:0,defeats:0,shockYears:[],store:0,storeYears:p.storeYears||1.5};");

// --- 2. step(): grain balance -> store, and army paid from store ---
const balanceAnchor = "    const grainBalance=usable+imports-demand;";
if (s.indexOf(balanceAnchor) < 0) throw new Error('balance anchor missing');
s = s.replace(balanceAnchor,
  "    const grainBalance=usable+imports-demand;\n" +
  "    // v1.1 granary: draw down / accumulate, capped at storeYears x annual demand\n" +
  "    const storeCap=demand*clamp(s.storeYears,.5,4);\n" +
  "    const storeAfter=clamp((s.store||0)+grainBalance,-storeCap*.35,storeCap);");

const allocAnchor = "    const allocatable=surplus*clamp(.18+.51*p.estateShare+.17*p.tradeIntegration,.10,.73);";
if (s.indexOf(allocAnchor) < 0) throw new Error('alloc anchor missing');
s = s.replace(allocAnchor,
  "    // v1.1: crown dues on harvest + reserves drawdown, so an army can be paid through a deficit year\n" +
  "    const crownDues=usable*clamp(.06+.20*p.estateShare+.08*p.tradeIntegration,.04,.34);\n" +
  "    const reserveDraw=Math.max(0,Math.min((s.store||0),Math.max(0,-grainBalance)))*clamp(.12+.30*p.warExpense,.10,.45);\n" +
  "    const allocatable=(surplus+crownDues+reserveDraw)*clamp(.18+.51*p.estateShare+.17*p.tradeIntegration,.10,.73);");

// --- 3. write the store back at end of step ---
const latestAnchor = "    s.latest={year,pop:newTotal";
if (s.indexOf(latestAnchor) < 0) throw new Error('latest anchor missing');
s = s.replace(latestAnchor, "    s.store=storeAfter;\n" + latestAnchor);
// expose it in the timeline row
s = s.replace("grainBalance,foodRatio,", "grainBalance,foodRatio,store:storeAfter,");

fs.writeFileSync(path.join(ROOT, 'model_v11.js'), s);
console.log('wrote model_v11.js, ' + (s.length - before.length) + ' bytes added');
