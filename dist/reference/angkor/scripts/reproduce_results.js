'use strict';
const fs=require('fs'), path=require('path');
const M=require('../model.js');
const out=path.join(__dirname,'../research');
const rows=Object.keys(M.PRESETS).map(k=>{
 const p={...M.DEFAULTS,...M.PRESETS[k].patch,seed:42};
 const x=M.simulate(p);
 return {scenario:k,seed:42,end:p.end,population:Math.round(x.final.pop),density_per_km2:+x.final.density.toFixed(2),monumental_log_index:+x.final.ornamentalIndex.toFixed(4),final_year_soldiers:x.final.soldiers,wars:x.events.wars,sacks:x.events.sacks,rice_balance_t:Math.round(x.final.grainBalance),bonded_workers:Math.round(x.final.bonded)};
});
const ks=Object.keys(rows[0]);
fs.writeFileSync(path.join(out,'scenario_results_seed42.csv'),[ks.join(','),...rows.map(x=>ks.map(k=>x[k]).join(','))].join('\n')+'\n');
const paired=M.mc({...M.DEFAULTS,end:1250},{n:30,seed:2026,treatment:M.PRESETS.estates.patch});
const sweep=M.sweep({...M.DEFAULTS,end:1250},{n:50,seed:2026});
const summary={modelVersion:'1.0',scenarioYear:1450,scenarioSeed:42,paired:{control:'reference',treatment:'estates',end:1250,n:30,seed:2026,differencePopulation:M.summarize(paired.rows.map(r=>r.diffPop))},sweep:{end:1250,n:50,seed:2026,keys:sweep.keys,populationR2:sweep.regressions.population.r2,monumentsR2:sweep.regressions.monuments.r2,populationRegression:sweep.regressions.population,monumentRegression:sweep.regressions.monuments,sacksRegression:sweep.regressions.conflicts}};
fs.writeFileSync(path.join(out,'experiment_summary.json'),JSON.stringify(summary,null,2)+'\n');
console.log('Wrote reproducible results');
