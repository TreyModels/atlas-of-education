const assert = require("node:assert/strict");
const fs = require("node:fs");
const vm = require("node:vm");
const {performance} = require("node:perf_hooks");
const html = fs.readFileSync(process.argv[2] ?? "index.html", "utf8");
assert.doesNotMatch(html, /<script\b[^>]*\bsrc\s*=|<link\b[^>]*\bhref\s*=|\bfetch\s*\(|\/\*(DATA|CITY_COHORT|CITY_HK|CITY_GZ|MODEL|UI)\*\//i);
const scripts = [...html.matchAll(/<script[^>]*>([\s\S]*?)<\/script>/g)].map(match => match[1]);
const nodes = Object.fromEntries([...html.matchAll(/\sid="([^"]+)"/g)].map(([,id]) => [id,{
  value:"", checked:false, disabled:false, events:{}, addEventListener(k,f){this.events[k] = f;}, appendChild(){}
}]));
for (const [,id,attrs] of html.matchAll(/<input id="([^"]+)"([^>]*)>/g)) {
  for (const [,key,value] of attrs.matchAll(/(min|max|value)="([^"]*)"/g)) nodes[id][key] = value;
}
nodes.policy.value = "reference";
let download;
const browserWindow={matchMedia(){return {matches:true};},addEventListener(){}};
browserWindow.parent=browserWindow;
const context = vm.createContext({
  document:{getElementById:id=>nodes[id],addEventListener(){},hidden:false,createElement:()=>({click(){download = this.download;},addEventListener(){},className:"",disabled:false,textContent:""})},
  window:browserWindow,Blob,setTimeout(){},setInterval(){return 1;},clearInterval(){},URL:{createObjectURL(){return "blob:qa";},revokeObjectURL(){}}
});
scripts.forEach(script => vm.runInContext(script,context));
const data = vm.runInContext("DATA",context);
const P = context.Pipeline;
assert.match(nodes.evidence.textContent,/Hong Kong network model/);
assert.match(nodes.stats.innerHTML,/First modeled layoffs/);
assert.match(nodes.chart.innerHTML,/<svg/);
assert.doesNotMatch(nodes.chart.innerHTML,/NaN|Infinity/);

const countries = ["Japan","South Korea","Taiwan","Thailand"];
const rowAt = (rows, y) => rows.find(row => row.year === y);
const first = (rows, key) => rows.find(row => row[key] > 0)?.year ?? null;
const t = performance.now();
const snapshots = [];
for (const name of Object.keys(data.systems)) {
  const system = data.systems[name];
  for (const key of Object.keys(system.stages)) {
    const defaultRows = P.simulate(data,name,key);
    const stage = system.stages[key];
    const forced = P.simulate(data,name,key,{force:true,exits:.02});
    const retained = P.simulate(data,name,key,{policy:"retain",force:true,exits:.02});
    const staffable = stage.city || stage.history;
    assert.equal(defaultRows.length,26);
    assert.equal(defaultRows[0].year,2025);
    assert.equal(defaultRows.at(-1).year,2050);
    assert.equal(defaultRows.some(row => row.layoffs > 0),false);
    if (!staffable) {
      assert.equal(defaultRows.at(-1).openings,null);
      assert.ok(defaultRows.at(-1).age > 0);
      continue;
    }
    for (let i = 1; i < defaultRows.length; i++) {
      for (const path of [defaultRows,forced,retained]) {
        const row = path[i];
        assert.equal(row.employed,path[i-1].employed-row.departures+row.openings-row.layoffs);
        assert.ok(row.employed >= row.required);
        if (row.firstOpenings != null) assert.ok(row.firstOpenings <= row.openings);
        if (row.unmatched != null) assert.ok(row.unmatched <= row.applicants);
      }
    }
    if (key === "p" || name === "Hong Kong" && key === "ps") {
      snapshots.push({name,key,
        pupils2025:defaultRows[0].enrollment,pupils2050:defaultRows.at(-1).enrollment,
        sites2050:defaultRows.at(-1).sites,staff2050:defaultRows.at(-1).employed,
        firstGap:first(defaultRows,"unmatched"),firstExcess:first(defaultRows,"excess"),
        firstLayoffs2pct:first(forced,"layoffs"),firstLayoffs2pctRetain:first(retained,"layoffs"),
        exampleGap:defaultRows.find(r=>r.unmatched > 0) ?? null,
        openings2030:rowAt(defaultRows,2030).firstOpenings,
        openings2050:defaultRows.at(-1).firstOpenings});
    }
  }
}
for (const name of countries) {
  for (const [stage, firstChange] of [["k",2030],["p",2033],["j",2039],["u",2042]]) {
    const a = P.simulate(data,name,stage,{births:-.5});
    const b = P.simulate(data,name,stage,{births:.5});
    assert.equal(a.findIndex((row,i) => row.age !== b[i].age),firstChange-2025);
  }
}
const korea = P.simulate(data,"South Korea","p");
assert.equal(rowAt(korea,2028).feederIntake,3847);
assert.equal(rowAt(korea,2029).feederIntake,3390);
assert.equal(rowAt(korea,2027).firstOpenings,2821);
assert.equal(rowAt(korea,2030).planLow,2500);
assert.equal(rowAt(korea,2030).planHigh,2800);
assert.equal(rowAt(korea,2031).planFloor,1988);
assert.equal(rowAt(korea,2034).planFloor,null);
assert.equal(rowAt(P.simulate(data,"South Korea","p",{policy:"enrollment"}),2027).openings,0);
const updated = P.simulate(data,"South Korea","p",{override:2000});
assert.equal(rowAt(updated,2030).feederIntake,3390);
assert.equal(rowAt(updated,2031).feederIntake,2000);
const hk = P.simulate(data,"Hong Kong","ps");
assert.equal(hk[0].employed,56724);
assert.equal(hk[1].feederIntake,461);
const gz = P.simulate(data,"Guangzhou","j");
assert.equal(rowAt(gz,2040).enrollment,438056);
const replacement = P.workforce(100,97,.05,false);
assert.equal(replacement.openings,2);
assert.equal(replacement.layoffs,0);
const excess = P.workforce(100,90,.05,true);
assert.equal(excess.layoffs,5);
assert.equal(excess.employed,90);

nodes.system.value = "South Korea"; nodes.system.events.change();
assert.equal(nodes.stage.value,"p");
assert.match(nodes.trainingNote.textContent,/3,847/);
nodes.births.value = "-30"; nodes.births.events.input();
assert.match(nodes.birthOut.textContent,/-30%/);
nodes.exits.value = "2"; nodes.exits.events.input();
nodes.force.checked = true; nodes.force.events.input();
assert.match(nodes.stats.innerHTML,/First modeled layoffs/);
nodes.override.value = "6500"; nodes.override.events.input();
assert.match(nodes.rows.innerHTML,/6,500/);
nodes.year.value = "2031"; nodes.year.events.input();
assert.match(nodes.rows.innerHTML,/<tr class="selected"><td>2031/);
nodes.download.events.click();
assert.equal(download,"south-korea-p-2050.csv");
nodes.system.value = "Thailand"; nodes.system.events.change();
nodes.stage.value = "j"; nodes.stage.events.change();
assert.equal(nodes.force.disabled,true);
assert.match(nodes.chartTitle.textContent,/School demand/);
assert.doesNotMatch(nodes.chart.innerHTML,/NaN|Infinity/);
nodes.system.value = "Guangzhou"; nodes.system.events.change();
assert.match(nodes.birthLabel.textContent,/preschool/);
console.log(JSON.stringify(snapshots,null,2));
console.log(`Passed model and interface checks (${(performance.now()-t).toFixed(0)} ms, including all systems and policies).`);
