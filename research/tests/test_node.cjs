'use strict';
const test=require('node:test'),assert=require('node:assert/strict'),fs=require('node:fs'),vm=require('node:vm'),path=require('node:path');
const root=path.resolve(__dirname,'../..');
const ctx=vm.createContext({});vm.runInContext(fs.readFileSync(path.join(root,'public/engines/camchild.js'),'utf8'),ctx);
const M=ctx.CamChild;
test('indexed random events do not depend on conditional draw consumption',()=>{
  const a=M.eventUniform(7,0,0,1,2);
  M.eventUniform(7,0,0,1,1);
  assert.equal(a,M.eventUniform(7,0,0,1,2));
  assert.notEqual(a,M.eventUniform(7,0,0,1,3));
  assert.ok(a>0&&a<1);
});
test('identical policy arms have exactly zero paired difference',()=>{
  const a=M.compare({N:80,years:2,seed:7,randomMode:'indexed',wealthDefinition:'national_income',policy:{}});
  assert.equal(a.yearsAvoided,0);
  assert.equal(JSON.stringify(a.base.rows),JSON.stringify(a.pol.rows));
});
test('income quintiles cross region boundaries and are equally sized',()=>{
  const a=M.simulate({N:100,years:1,seed:4,randomMode:'indexed',wealthDefinition:'national_income'});
  assert.equal(a.rows[0].all.n,100);
  assert.equal(a.rows[0].all.balance,0);
  assert.equal(JSON.stringify(a.design.quintileCounts),JSON.stringify([20,20,20,20,20]));
  // Wealth changes observed grouping, not household income assignments.
  const b=M.simulate({N:100,years:1,seed:4,randomMode:'indexed',wealthDefinition:'within_region_rank'});
  assert.equal(a.H.map(x=>x.y0).join(','),b.H.map(x=>x.y0).join(','));
});
test('alternative monsoon responses never reuse the stored linear summary',()=>{
  const c=vm.createContext({});vm.runInContext(fs.readFileSync(path.join(root,'public/engines/monsoon.js'),'utf8'),c);
  const baseline=c.AngkorMonsoon.run(),variant=c.AngkorMonsoon.run({response:'exponential',pdsiCap:3,seed:5});
  assert.ok(baseline.summary);assert.equal(variant.summary,null);
  assert.equal(c.AngkorMonsoon.run({sensitivity:.071}).summary,null);
  assert.equal(variant.translation.response,'exponential');
  const zero=c.AngkorMonsoon.run({sensitivity:0,response:'exponential',pdsiCap:3});
  assert.equal(JSON.stringify(zero.current),JSON.stringify(zero.reference));
});
const P=require(path.join(root,'public/reference/east-asia-schools/source/pipeline.js'));
test('returning applicants enter the next years candidate stock',()=>{
  const system={stages:{primary:{ages:[6,6],history:{2025:[1,100,10]},
    training:{years:{},future:20,before:20},lag:1,firstShare:1}}};
  const population={Toy:Object.fromEntries(P.years.map(y=>[y,[0,0,0,0,0,0,100]]))};
  const data={systems:{Toy:system},population};
  const a=P.simulate(data,'Toy','primary',{qualify:1,seek:1,exits:0,applicantRetention:0});
  const b=P.simulate(data,'Toy','primary',{qualify:1,seek:1,exits:0,applicantRetention:1});
  assert.equal(a[2].unmatched,20);assert.equal(b[2].unmatched,40);
});
