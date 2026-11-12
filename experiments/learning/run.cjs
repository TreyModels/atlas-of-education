'use strict';
const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');
const c=vm.createContext({});vm.runInContext(fs.readFileSync(__dirname+'/learning.js','utf8'),c);const M=c.AngkorLearning;
const rows=[];let accounting=0;
function matched(design,p){
 for(const mode of ['fixed','learning','learning-loss']){
  const r=M.run({...p,mode});
  assert.ok(r.maxLedgerError<1e-10&&r.maxMassError<1e-10);
  assert.ok(r.rows.every(x=>x.oldKnowledge>=0&&x.oldKnowledge<=1&&x.southKnowledge>=0&&x.southKnowledge<=1));
  for(let i=1;i<r.rows.length;i++){
   const prev=r.rows[i-1],now=r.rows[i];
   const delta=(now.oldKnowledge+now.southKnowledge)-(prev.oldKnowledge+prev.southKnowledge);
   assert.ok(Math.abs(delta-(now.oldLearned+now.southLearned-now.knowledgeOverflow))<1e-10);
  }
  if(mode==='fixed')assert.ok(r.rows.every(x=>x.oldKnowledge===.5&&x.southKnowledge===.5));
  accounting=Math.max(accounting,r.maxLedgerError,r.maxMassError);
  rows.push({design,...p,mode,exitYear:r.exitYear,finalEliteShare:r.finalEliteShare,oldCoreFinal:r.rows.at(-1).oldCore,oldRuralFinal:r.rows.at(-1).oldRural,oldCoreRetained:r.oldCoreRetained,oldRuralRetained:r.oldRuralRetained,oldWater:r.oldWater,oldKnowledge:r.oldKnowledge,foodGap:r.foodGap});
 }
}
for(const outside of [.8,1.2,1.6])for(const movingCost of [.05,.25,.5])for(const localRepair of [0,.75])for(const climate of ['stable','drought'])for(let seed=1;seed<=32;seed++)matched('main',{outside,movingCost,localRepair,climate,seed,portability:.75,learningRate:.03,lossStrength:.5});
for(const learningRate of [.01,.03,.06])for(const lossStrength of [.25,.5,1])for(const climate of ['stable','drought'])for(let seed=1;seed<=32;seed++)matched('sensitivity',{outside:1.2,movingCost:.25,localRepair:.5,climate,seed,portability:.75,learningRate,lossStrength});
const keys=Object.keys(rows[0]);fs.writeFileSync(__dirname+'/results.csv',[keys.join(','),...rows.map(r=>keys.map(k=>r[k]??'').join(','))].join('\n'));
const summary=[];
for(const design of ['main','sensitivity'])for(const climate of ['stable','drought'])for(const mode of ['fixed','learning','learning-loss']){
 const a=rows.filter(r=>r.design===design&&r.climate===climate&&r.mode===mode),mean=k=>a.reduce((s,r)=>s+r[k],0)/a.length;
 summary.push({design,climate,mode,runs:a.length,exits:a.filter(r=>r.exitYear!==null).length,elite:mean('finalEliteShare'),core:mean('oldCoreRetained'),coreAbsolute:mean('oldCoreFinal'),rural:mean('oldRuralRetained'),water:mean('oldWater'),knowledge:mean('oldKnowledge'),foodGap:mean('foodGap')});
}
const paired=[];for(let i=0;i<rows.length;i+=3){const [f,l,k]=rows.slice(i,i+3);paired.push({design:f.design,climate:f.climate,learnVsFixed:l.oldCoreRetained-f.oldCoreRetained,lossVsLearn:k.oldCoreRetained-l.oldCoreRetained,lossFoodGap:k.foodGap-l.foodGap,lossExit:(k.exitYear!==null)-(l.exitYear!==null)});}
fs.writeFileSync(__dirname+'/summary.json',JSON.stringify({histories:rows.length,maxAccountingError:accounting,summary,paired},null,2));console.log(JSON.stringify({histories:rows.length,maxAccountingError:accounting,summary},null,2));
// With migration blocked, the learning-with-loss arm must equal the learning arm.
for(const seed of [1,42]){const a=M.run({seed,mode:'learning',mobility:'closed'}),b=M.run({seed,mode:'learning-loss',mobility:'closed'});assert.deepEqual(JSON.stringify(a.rows),JSON.stringify(b.rows));}
console.log('Accounting, knowledge balance, fixed-control and blocked-exit checks passed.');
