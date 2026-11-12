const assert=require("node:assert/strict");
const fs=require("node:fs"),vm=require("node:vm");
const N=require("./network.js"),G=require("./guangzhou.js"), C=require("./model.js");
const hk=require("./data.json"),approvals=require("./approvals.json"),plans=require("./plans.json");
const profiles=require("./primary-profiles.json"),gz=require("./guangzhou.json");
const named=profiles.schools.filter(x=>x.previousP1>0&&x.classes[0]===0);
assert.deepEqual(named.map(s=>s.name).sort(),plans.schools.map(x=>x[0]).sort());
assert.equal(approvals.previous[0]-approvals.approved[0],126);
const districts=N.districtApprovals(profiles,hk.districts);
assert.equal(C.sum(districts.map(d=>d.schools)),448);
assert.equal(C.sum(districts.map(d=>d.zero)),15);
assert.equal(C.sum(districts.map(d=>d.approved)),1438);
for(const settings of [{},{exitScale:0.35},{savedSites:0,demandShift:-0.15},{savedSites:30,demandShift:0.15,exitScale:1.5}]){
  const r=N.run(hk,approvals,plans,settings);
  for(const y of N.allYears){
    const ref=r.records.policy[y];
    for(const p of N.CASES){
      const before=r.records[p.key][y-1], now=r.records[p.key][y];
      for(const [s,x] of now.entries()){
        assert.equal(x.enrollment,ref[s].enrollment);
        assert.equal(x.staff,before[s].staff+x.hires-x.departures-x.involuntary);
        assert.ok(x.staff>=x.required&&x.hires>=0&&x.involuntary>=0);
        if(!p.force)assert.equal(x.involuntary,0);
      }
      assert.ok(now[1].sites<=591-now[1].planned || now[1].planned===0);
    }
    assert.equal(C.sum(r.district[y][1].map(x=>x[0])),ref[1].entry);
  }
  assert.equal(r.records.policy[2029][1].planned,4);
  for(const p of N.CASES)assert.deepEqual(r.records[p.key][2026],r.records.policy[2026]);
}
const reference=N.run(hk,approvals,plans);
assert.equal(reference.records.policy[2026][1].classes,C.sum(hk.history.at(-1)[1].classes)+C.sum(approvals.approved)-C.sum(approvals.previous));
assert.equal(C.sum(reference.records.policy[2031].map(x=>x.staff)),58818);
assert.equal(C.sum(reference.records.policy[2040].map(x=>x.staff)),53490);
assert.equal(reference.records.policy[2040][2].enrollment,224576);
assert.equal(reference.records.policy[2050][2].enrollment,189358);
assert.equal(C.sum(reference.records.policy[2050].map(x=>x.staff)),50472);
assert.equal(N.run(hk,approvals,plans,{birthGrowth:-0.03}).records.policy[2050][2].enrollment,146766);
assert.deepEqual(N.run(hk,approvals,plans,{birthGrowth:-0.03}).cohort.paths[2035].slice(1),reference.cohort.paths[2035].slice(1));
assert.ok(reference.records.policy[2040][2].entry>reference.records.policy[2035][2].entry);
const lowerBirths=N.run(hk,approvals,plans,{births:20000});
const higherBirths=N.run(hk,approvals,plans,{births:40000});
assert.deepEqual(lowerBirths.cohort.paths[2035].slice(1),higherBirths.cohort.paths[2035].slice(1));
assert.ok(lowerBirths.records.policy[2040][1].enrollment<higherBirths.records.policy[2040][1].enrollment);
assert.equal(lowerBirths.records.policy[2040][2].enrollment,higherBirths.records.policy[2040][2].enrollment);
assert.equal(C.sum(N.run(hk,approvals,plans,{exitScale:0.35}).records.rapid[2035].map(x=>x.involuntary)),311);
const gx=G.simulate(gz);
for(const y of Object.keys(gx.reference)){
  for(const [i,x] of gx.reference[y].entries()){
    assert.equal(x.enrollment,gx.retain[y][i].enrollment);
    assert.equal(x.enrollment,gx.rapid[y][i].enrollment);
  }
}
assert.equal(gx.reference[2025][1].enrollment,1340600);
assert.equal(gx.reference[2040][2].enrollment,438056);
assert.equal(gx.reference[2050][2].enrollment,425145);
assert.deepEqual(gx.reference[2048],gx.reference[2050]);
assert.equal(G.simulate(gz,{longKgGrowth:-0.03}).reference[2050][2].enrollment,323213);
const gzLow=G.simulate(gz,{longKgGrowth:-0.03}), gzHigh=G.simulate(gz,{longKgGrowth:0.02});
assert.deepEqual(gzLow.reference[2031],gzHigh.reference[2031]);
assert.ok(gzLow.reference[2040][1].enrollment<gzHigh.reference[2040][1].enrollment);
assert.ok(gx.reference[2034][3].enrollment>gx.reference[2033][3].enrollment);
assert.ok(gx.reference[2034][3].enrollment>gx.reference[2040][3].enrollment);
assert.equal(G.backtest(gz).filter(x=>x.metric==="sites").length,12);
assert.equal(N.testHistory(hk).workforceRows.length,15);
const html=fs.readFileSync(process.argv[2]??"index.html","utf8");
assert.doesNotMatch(html,/<script\b[^>]*\bsrc\s*=|<link\b[^>]*\bhref\s*=|\bfetch\s*\(|\/\*(DATA|STYLE|COHORT|HK|GZ|UI)\*\//i);
const scripts=[...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(m=>m[1]);
assert.deepEqual(JSON.parse(scripts[0]).gz,gz);
const mk=()=>({hidden:false,events:{},options:[],replaceChildren(){this.options=[];},add(o){this.options.push(o);if(o.selected)this.value=o.value;},
  addEventListener(k,f){this.events[k]=f;},setAttribute(){}});
const nodes=Object.fromEntries([...html.matchAll(/\sid="([^"]+)"/g)].map(m=>[m[1],mk()]));
for(const m of html.matchAll(/<input id="([^"]+)"[^>]*value="([^"]+)"/g))nodes[m[1]].value=m[2];
nodes.input.textContent=scripts[0];
const tabs=["hk","gz"].map(city=>Object.assign(mk(),{dataset:{city}}));
let download;
const cx=vm.createContext({document:{getElementById:id=>nodes[id],querySelectorAll:()=>tabs,addEventListener(){},hidden:false,
  createElement:()=>({click(){download=this.download;}})},
  Intl,Blob,setTimeout(){},setInterval(){return 1;},clearInterval(){},matchMedia(){return {matches:true};},URL:{createObjectURL(){return "blob:qa";},revokeObjectURL(){}},
  Option:function(text,value,defaultSelected,selected){Object.assign(this,{text,value,selected});}});
cx.window=cx;cx.parent=cx;
for(const script of scripts.slice(1))vm.runInContext(script,cx);
assert.match(nodes.projectionTitle.textContent,/Primary in 2050\/51/);
assert.match(nodes.comparison.innerHTML,/19,673/);
assert.match(nodes.schoolPlans.innerHTML,/Fresh Fish/);
assert.match(nodes.chart.innerHTML,/After EDB inputs/);
nodes.birthGrowth.value=-3; nodes.birthGrowth.events.input();
assert.match(nodes.comparison.innerHTML,/120,312/);
nodes.year.value="2040";nodes.year.events.change();
assert.match(nodes.projectionTitle.textContent,/Primary in 2040\/41/);
nodes.reset.events.click();
assert.equal(+nodes.births.value,100);
nodes.metric.value="involuntary";nodes.metric.events.change();
assert.doesNotMatch(nodes.chart.innerHTML,/NaN|Infinity/);
tabs[1].events.click();
assert.match(nodes.projectionTitle.textContent,/Junior secondary in 2050\/51/);
assert.match(nodes.comparison.innerHTML,/425,145/);
assert.match(nodes.chart.innerHTML,/Long-run settings/);
nodes.longKgGrowth.value=2;nodes.longKgGrowth.events.input();
assert.match(nodes.comparison.innerHTML,/508,455/);
nodes.download.events.click();
assert.equal(download,"Guangzhou_Network_Scenarios.csv");
tabs[0].events.click();
nodes.download.events.click();
assert.equal(download,"Hong_Kong_Network_Scenarios.csv");
console.log("Passed: plan and profile reconciliation, teacher flows, scenario invariants, Guangzhou backtest, offline build and interface logic.");
