'use strict';
const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const c=vm.createContext({});vm.runInContext(fs.readFileSync(__dirname+'/engine.js','utf8'),c);const M=c.AngkorLearningRound2;
const arms={retained:{mode:'learning'},elite:{mode:'learning-loss'},worker:{mode:'learning-loss',carrier:'worker'},mixed:{mode:'learning-loss',carrier:'mixed'},retention50:{mode:'learning-loss',retention:.5},retention90:{mode:'learning-loss',retention:.9},equal_drought:{mode:'learning-loss',southDrought:.62},equal_drought_retained:{mode:'learning',southDrought:.62},forgetting:{mode:'learning-loss',forgetting:.005},obligations_expire:{mode:'learning-loss',obligationDecay:.02},maintenance_first:{mode:'learning-loss',maintenanceFirst:true},theory_scaling:{mode:'learning-loss',beta:7/6},constant_productivity:{mode:'learning-loss',beta:1}};
const rows=[];let maxError=0;
function record(design,arm,controls){
 const r=M.run(controls);assert.ok(r.maxLedgerError<1e-10&&r.maxMassError<1e-10);
 maxError=Math.max(maxError,r.maxLedgerError,r.maxMassError);
 for(let i=1;i<r.rows.length;i++){
  const a=r.rows[i-1],b=r.rows[i];
  assert.ok(Math.abs(b.oldKnowledge+b.southKnowledge-a.oldKnowledge-a.southKnowledge-(b.oldLearned+b.southLearned-b.oldForgotten-b.southForgotten-b.knowledgeOverflow))<1e-10);
 }
 assert.ok(r.rows.every(x=>x.oldKnowledge>=0&&x.oldKnowledge<=1&&x.southKnowledge>=0&&x.southKnowledge<=1));
 const last=r.rows.at(-1),pre=r.rows[119],after=r.rows[120],recover=r.rows[160];
 rows.push({design,arm,...controls,exitYear:r.exitYear,elite:r.finalEliteShare,core:r.oldCoreRetained,coreAbsolute:last.oldCore,rural:r.oldRuralRetained,water:r.oldWater,knowledge:r.oldKnowledge,gap:r.foodGap,knowledgePre:pre.oldKnowledge,knowledgeAfter:after.oldKnowledge,knowledge40Later:recover.oldKnowledge,waterPre:pre.oldWater,water40Later:recover.oldWater});
 return r;
}
for(const outside of [.8,1.2,1.6])for(const movingCost of [.05,.25,.5])for(const localRepair of [0,.75])for(const climate of ['stable','drought'])for(let seed=1;seed<=16;seed++){
 const common={outside,movingCost,localRepair,climate,seed};
 for(const [name,arm]of Object.entries(arms))record('robustness',name,{...common,...arm});
}
for(const localRepair of [0,.5,.75])for(const climate of ['stable','drought'])for(const learningRate of [.01,.03,.06])for(let seed=1;seed<=32;seed++){
 const common={localRepair,climate,learningRate,seed,mobility:'closed',forcedExit:.4};
 record('forced_exit','retained',{...common,mode:'learning'});
 record('forced_exit','elite',{...common,mode:'learning-loss'});
 record('forced_exit','retention90',{...common,mode:'learning-loss',retention:.9});
}
const keys=[...new Set(rows.flatMap(Object.keys))];fs.writeFileSync(__dirname+'/results.csv',[keys.join(','),...rows.map(r=>keys.map(k=>r[k]??'').join(','))].join('\n'));
const summary=[];for(const design of ['robustness','forced_exit'])for(const climate of ['stable','drought'])for(const arm of [...new Set(rows.filter(r=>r.design===design).map(r=>r.arm))]){
 const r=rows.filter(r=>r.design===design&&r.climate===climate&&r.arm===arm),mean=k=>r.reduce((s,x)=>s+x[k],0)/r.length;
 summary.push({design,climate,arm,runs:r.length,exits:r.filter(x=>x.exitYear!==null).length,elite:mean('elite'),core:mean('core'),coreAbsolute:mean('coreAbsolute'),water:mean('water'),knowledge:mean('knowledge'),gap:mean('gap'),knowledgeAfter:mean('knowledgeAfter'),knowledge40Later:mean('knowledge40Later')});
}
// Placebos: eliminating the productivity effect eliminates economic differences from knowledge loss.
for(const seed of [1,42]){
 const a=M.run({seed,beta:1,mode:'learning'}),b=M.run({seed,beta:1,mode:'learning-loss'});
 for(let i=0;i<a.rows.length;i++)for(const key of ['oldRural','oldCore','oldWater','oldHarvest','oldGap','oldEliteShare'])assert.equal(a.rows[i][key],b.rows[i][key]);
 const k=M.run({seed,mode:'learning-loss',retention:1}),l=M.run({seed,mode:'learning'});assert.equal(JSON.stringify(k.rows),JSON.stringify(l.rows));
}
fs.writeFileSync(__dirname+'/summary.json',JSON.stringify({histories:rows.length,maxError,summary},null,2));console.log(JSON.stringify({histories:rows.length,maxError,summary},null,2));console.log('Food, population, knowledge and placebo checks passed.');
