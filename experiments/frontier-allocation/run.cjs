const fs=require('fs'),vm=require('vm'),assert=require('node:assert/strict');const c=vm.createContext({});vm.runInContext(fs.readFileSync(__dirname+'/engine.js','utf8'),c);const M=c.AngkorAllocation;
const policies={balanced:[.5,.2,.15,.1,.05],farm_first:[.65,.15,.1,.05,.05],military_first:[.4,.35,.1,.1,.05],irrigation_first:[.5,.15,.25,.05,.05],monument_first:[.4,.15,.1,.3,.05],religion_first:[.45,.15,.1,.05,.25],military_from_farms:[.35,.35,.15,.1,.05],military_from_monuments:[.5,.3,.15,0,.05],military_from_irrigation:[.5,.3,.05,.1,.05],irrigation_from_monuments:[.5,.2,.25,0,.05]};
const rows=[];for(const [policy,shares]of Object.entries(policies))for(const climate of ['stable','drought'])for(const distanceStep of [20,80])for(const tax of [.25,.4])for(const frontierTowns of [12,40])for(const waterMaintenance of [10,30,60])for(let seed=1;seed<=32;seed++){
 const allocation=Object.fromEntries(M.sectors.map((k,i)=>[k,shares[i]]));const r=M.run({allocation,climate,distanceStep,tax,seed,frontierTowns,waterMaintenance});
 assert.ok(r.maxGrainError<1e-7&&r.maxLabourError<1e-7&&r.maxPopulationError===0);
 assert.ok(r.rows.every(x=>x.idleDays>=-1e-8&&x.householdStore>=-1e-8&&x.courtStore>=-1e-8));
 assert.ok(r.rows.every(x=>Math.abs(x.publicRations+x.civilianNeed-x.population*.21)<1e-7));
 rows.push({policy,climate,distanceStep,tax,seed,frontierTowns,waterMaintenance,finalTowns:r.finalTowns,peakTowns:r.peakTowns,lostTowns:r.lostTowns,foodGap:r.foodGap,garrisonShortYears:r.garrisonShortYears,finalWater:r.finalWater,finalMonument:r.finalMonument,maxGrainError:r.maxGrainError});
}
const shiftPolicies={hold_balanced:policies.balanced,shift_army_to_monuments:[.5,.1,.15,.2,.05],shift_irrigation_to_army:policies.military_from_irrigation,shift_farms_to_army:[.4,.3,.15,.1,.05]};
for(const [policy,shares]of Object.entries(shiftPolicies))for(const climate of ['stable','drought'])for(const distanceStep of [20,80])for(const tax of [.25,.4])for(let seed=1;seed<=32;seed++){
 const afterAllocation=Object.fromEntries(M.sectors.map((k,i)=>[k,shares[i]]));
 const r=M.run({climate,distanceStep,tax,seed,frontierTowns:40,waterMaintenance:30,shiftAt:30,afterAllocation});
 assert.ok(r.maxGrainError<1e-7&&r.maxLabourError<1e-7&&r.maxPopulationError===0);
 rows.push({policy,climate,distanceStep,tax,seed,frontierTowns:40,waterMaintenance:30,finalTowns:r.finalTowns,peakTowns:r.peakTowns,lostTowns:r.lostTowns,foodGap:r.foodGap,garrisonShortYears:r.garrisonShortYears,finalWater:r.finalWater,finalMonument:r.finalMonument,maxGrainError:r.maxGrainError});
}
const keys=Object.keys(rows[0]);fs.writeFileSync(__dirname+'/results.csv',[keys.join(','),...rows.map(r=>keys.map(k=>r[k]).join(','))].join('\n'));
const summary=[];for(const policy of [...Object.keys(policies),...Object.keys(shiftPolicies)]){const r=rows.filter(x=>x.policy===policy),mean=k=>r.reduce((n,x)=>n+x[k],0)/r.length;summary.push({policy,runs:r.length,towns:mean('finalTowns'),peak:mean('peakTowns'),lost:mean('lostTowns'),gap:mean('foodGap'),garrisonShortYears:mean('garrisonShortYears'),water:mean('finalWater'),monument:mean('finalMonument')});}
// Mechanism check: expansion creates an ongoing garrison obligation.
const a=M.run({seed:42}),b=M.run({seed:42,expansion:false});assert.ok(a.rows.some(r=>r.requiredGarrison>200));assert.ok(b.rows.every(r=>r.requiredGarrison===200&&r.joined===0));
assert.throws(()=>M.run({allocation:{agriculture:.9}}));
assert.throws(()=>M.run({afterAllocation:{agriculture:.5}}));
assert.ok(a.rows.every(r=>r.afterTowns>=0&&r.afterTowns<=a.parameters.frontierTowns));
fs.writeFileSync(__dirname+'/summary.json',JSON.stringify({histories:rows.length,policies,summary},null,2));console.log(JSON.stringify({histories:rows.length,summary},null,2));console.log('Grain, labour, population, ration and garrison checks passed.');
