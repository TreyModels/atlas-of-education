'use strict';
const assert = require('node:assert/strict');
const crypto = require('node:crypto');
const fs = require('node:fs');
const path = require('node:path');
const test = require('node:test');
const vm = require('node:vm');
const root = path.join(__dirname, 'public');
const ctx = vm.createContext({});
const index = fs.readFileSync(path.join(__dirname, 'tests/fixtures/model-loader.html'), 'utf8');
for (const [, file] of index.matchAll(/<script defer src="([^"]+)"/g)) {
  if (['app.js', 'languages.js'].includes(file)) continue;
  vm.runInContext(fs.readFileSync(path.join(root, file), 'utf8'), ctx, {filename: file});
}
const {worlds, sha256} = ctx.AtlasWorldsLab;
const fileFor = name => {
  for (const dir of ['engines', 'reference/angkor', 'reference', '../inputs']) {
    const file = path.join(root, dir, name);
    if (fs.existsSync(file)) return file;
  }
  throw new Error('Missing input ' + name);
};
for (const world of worlds) {
  test(world.id + ' produces a finite baseline with traceable inputs', () => {
    const current = world.run(world.defaults);
    const view = world.view(current, current);
    assert.ok(view.metrics.every(m => !/NaN|Infinity/.test(m.value)));
    assert.ok(!view.lines || view.lines.every(s => s.points.every(([x, y]) => Number.isFinite(x) && Number.isFinite(y))));
    for (const name of world.engines) {
      const hash = crypto.createHash('sha256').update(fs.readFileSync(fileFor(name))).digest('hex');
      assert.equal(sha256[name], hash);
    }
    for (const [, href] of world.links) {
      if (!href.startsWith('https://')) assert.ok(fs.existsSync(path.join(root, href.split('#')[0] || '../index.html')), href);
    }
  });
  if (!world.stored) test(world.id + ' responds to its default-facing slider', () => {
    const field = world.controls[0];
    const base = world.run(world.defaults);
    const changed = world.run({...world.defaults, [field.key]: field.max});
    assert.notEqual(JSON.stringify(world.view(changed, base).lines[0].points),
      JSON.stringify(world.view(base, base).lines[0].points));
  });
}
test('Mandala historical failure and seed comparison remain visible', () => {
  const w = worlds.find(x => x.id === 'mandala');
  const ref = w.run(w.defaults);
  const canal = w.run({scenario: 'canal_first'});
  assert.equal(ref.summary.angkor_leads_1200.mean, 0);
  assert.equal(ref.summary.post_1300_decline.mean, .28);
  assert.equal(canal.summary.post_1300_decline.mean, .65);
  assert.equal(ref.population.length, 76);
  assert.ok(canal.population.every(([, lo, mid, hi]) => lo <= mid && mid <= hi));
});
test('Credential selectors use the stored country and structure summaries', () => {
  const w = worlds.find(x => x.id === 'credentials');
  const current = w.run({country: 'Vietnam', structure: 'M_HC'});
  const view = w.view(current);
  assert.equal(current.rows.M_HC.accepted, 1460);
  assert.equal(view.table.rows.filter(r => r.selected).length, 1);
  assert.equal(view.table.rows.find(r => r.selected).cells[0], 'Human capital');
});
test('continuous slider input updates mid-drag and flushes the final value', () => {
  const elements = new Map(), handlers = new Map(), timers = new Map();
  let time = 0, next = 0;
  const advance = ms => {
    time += ms;
    for (const [id, {due, fn}] of timers) {
      if (due <= time) {
        timers.delete(id);
        fn();
      }
    }
  };
  Object.assign(ctx, {
    location: {hash: '#teachers'},
    addEventListener() {},
    document: {querySelectorAll() { return []; }, getElementById(id) {
      if (!elements.has(id)) elements.set(id, {
        children: [], classList: {toggle() {}},
        addEventListener(event, fn) { handlers.set(id + ':' + event, fn); }
      });
      return elements.get(id);
    }},
    setTimeout(fn, delay) {
      timers.set(++next, {due: time + delay, fn});
      return next;
    },
    clearTimeout(id) { timers.delete(id); }
  });
  vm.runInContext('globalThis.window = globalThis', ctx);
  vm.runInContext(fs.readFileSync(path.join(__dirname, 'tests/fixtures/classic-controller.js'), 'utf8'), ctx);
  const metrics = () => elements.get('metrics').innerHTML;
  const initial = metrics();
  const target = {dataset: {key: 'growth'}, type: 'range', validity: {valid: true}};
  for (const value of [.025, .03, .035, .04]) {
    target.valueAsNumber = value;
    handlers.get('controls:input')({target});
    advance(20);
  }
  assert.notEqual(metrics(), initial);
  const midDrag = metrics();
  target.valueAsNumber = .05;
  handlers.get('controls:input')({target});
  assert.equal(metrics(), midDrag);
  handlers.get('controls:change')({target});
  assert.notEqual(metrics(), midDrag);
  assert.equal(timers.size, 0);
});
test('campaign distance delays return, captures transfer people, and grain balances', () => {
  const model = ctx.AngkorCampaign;
  const base = model.run();
  const long = model.run({distance: 540, fightingDays: 130});
  assert.ok(long.campaignDays > base.campaignDays);
  assert.ok(long.rows.some(r => r.season === 'Harvest' && r.localSoldiers > 0));
  assert.ok(!base.rows[1].alliedSoldiers);
  assert.ok(base.rows.some(r => r.alliedSoldiers));
  assert.ok(base.rows.some(r => r.captured > 0));
  for (const [i, row] of long.rows.entries()) {
    assert.equal(row.weather, base.rows[i].weather);
    assert.equal(row.population + row.frontierPopulation, 340000);
    assert.ok(Math.abs(row.grainBalanceError) < 1e-8);
    assert.ok(row.villageGrain >= 0 && row.courtGrain >= -1e-8);
  }
  assert.ok(model.compare(model.defaults).pairedSeeds.every(row => row.foodGapDelta === 0 && row.capturedDelta === 0));
});
test('fish and earthworks have separate balanced effects', () => {
  const model = ctx.AngkorCampaign;
  const lake = model.run();
  const corridor = model.run({fishery: 'corridor'});
  const noFish = model.run({fishery: 'none'});
  const hardGround = model.run({digging: 3});
  assert.ok(lake.rows.some(r => r.fishProteinKg > 0));
  assert.ok(noFish.rows.every(r => r.fishProteinKg === 0));
  assert.notEqual(lake.rows[0].fishCatch, corridor.rows[0].fishCatch);
  assert.equal(lake.responseDays, noFish.responseDays);
  assert.ok(hardGround.rows[0].channels < lake.rows[0].channels);
  for (const result of [lake, corridor, noFish, hardGround]) {
    assert.ok(result.rows.every(r => Math.abs(r.fishBalanceError) < 1e-8 && Math.abs(r.grainBalanceError) < 1e-8));
  }
});
test('signalling uses matched challenges and spends conserved resources', () => {
  const model = ctx.AngkorSignalling;
  for (const options of [{}, {loss: .85, displayShare: .6}, {stoneWeight: 0, signalScale: .6}]) {
    const pair = model.compare(options);
    assert.equal(JSON.stringify(pair), JSON.stringify(model.compare(options)));
    assert.equal(pair.pairedSeeds.length, 32);
    for (const [i, row] of pair.current.rows.entries()) {
      const informed = pair.truth.rows[i];
      assert.equal(row.demand, informed.demand);
      assert.equal(row.harvestShock, informed.harvestShock);
      assert.equal(informed.pledged, informed.defended);
      if (i) assert.equal(row.tributeReceived, pair.current.rows[i-1].pledged ? pair.current.assumptions.tribute : 0);
      for (const entry of [row, informed]) {
        assert.ok(Math.abs(entry.grainBalanceError) < 1e-8);
        assert.ok(entry.reserve >= 0 && entry.reserve <= pair.current.assumptions.storageCapacity);
        assert.ok(entry.build + entry.upkeepLabour + entry.replacementLabour + entry.defenceSpend <= entry.openingLabour + 1e-8);
      }
    }
  }
  const mixed = model.compare();
  const elephants = model.compare({stoneWeight: 0});
  assert.ok(mixed.pairedSeeds.some(row => row.falseReassurance > 0));
  assert.ok(elephants.pairedSeeds.reduce((n,row) => n + row.falseReassurance, 0) <
    mixed.pairedSeeds.reduce((n,row) => n + row.falseReassurance, 0));
});
test('obligations consume the selected upstream pledges and compare return rules', () => {
  const model = ctx.AngkorObligations;
  const options = {upstream:{stoneWeight:0,loss:.55}, seed:42, returnRule:'open'};
  const run = model.compare(options);
  const upstream = ctx.AngkorSignalling.run({...options.upstream,seed:options.seed});
  assert.equal(run.current.upstreamParameters.stoneWeight, 0);
  assert.ok(run.current.rows.every((row,i)=>row.upstreamTribute===upstream.rows[i].tributeReceived));
  assert.ok(run.current.rows.every(row=>Math.abs(row.balanceError)<1e-8));
  assert.ok(run.paired.some(r=>r.returnYear!==null));
  assert.ok(model.compare({...options,returnRule:'closed'}).paired.every(r=>r.returnYear===null));
  assert.equal(model.compare({returnRule:'open'}).paired.filter(r=>r.returnYear!==null).length,21);
});
test('published monsoon browser run matches the stored review draw', () => {
  const M=ctx.AngkorMonsoon;
  const result=M.run({sensitivity:.07,draw:42});
  const csv=fs.readFileSync(path.join(root,'research/buckley/results.csv'),'utf8').trim().split('\n');
  const head=csv[0].split(',');
  const target=csv.slice(1).map(line=>Object.fromEntries(line.split(',').map((v,i)=>[head[i],v])))
    .find(row=>row.sensitivity==='0.07'&&row.seed===String(result.parameters.seed));
  const coreAt=y=>result.current.find(row=>row.year===y).core;
  assert.ok(target);
  assert.ok(Math.abs(coreAt(1450)/coreAt(1300)-Number(target.core1450_vs1300))<1e-10);
  assert.equal(result.current.length,201);
  assert.equal(result.climate.find(r=>r.year===1403).pdsi,-7.209);
  assert.equal(result.summary.declines,1260);
});

test('published provisioning ratios preserve scale and keep distance separate',()=>{
 const M=ctx.AngkorProvisioning,a=M.run({community:100}),b=M.run({community:500});
 assert.ok(Math.abs(b.perPersonIndex/a.perPersonIndex-5**.227)<1e-12);
 assert.equal(M.run({community:1000,scaling:'linear'}).perPersonIndex,100);
 assert.equal(M.run({distance:20}).perPersonIndex,b.perPersonIndex);
 assert.ok(Math.abs(M.run({distance:20}).distanceOutput-100*2**(-.846))<1e-12);
 assert.equal(b.periods.at(-1).population,213521);
});
test('Petri ledger balances; under the old assumed multiplier, coordination knockout changes recovery',()=>{
 const M=ctx.AngkorPetri,old={coordination:5**.227,waterFloor:.1},a=M.run(old),b=M.run({...old,knockout:'coordination'});
 const d=M.run(),k=M.run({knockout:'coordination'});
 assert.ok(d.maxLedgerError<1e-10&&Math.abs(d.retained-k.retained)<1e-12,'default multiplier 1: knockout is a no-op');
 assert.ok(a.maxLedgerError<1e-10&&b.maxLedgerError<1e-10);
 assert.ok(a.retained>.99&&b.retained<.8);
 assert.ok(b.gap>a.gap);
 assert.ok(a.rows.every(r=>r.rural>=0&&r.core>=0&&r.store>=0));
});

test('relocation conserves migrants and food at both centres',()=>{
 const M=ctx.AngkorRelocation;
 for(const mobility of ['open','closed','elite-only','workers-only']){
  const r=M.run({mobility,outside:1.6,movingCost:.05});
  assert.ok(r.maxMassError<1e-10&&r.maxLedgerError<1e-10);
  assert.ok(r.rows.every(x=>x.oldRural>=0&&x.southRural>=0&&x.oldCore>=0&&x.southCore>=0));
  if(mobility==='closed')assert.ok(r.rows.every(x=>Math.abs(x.oldEliteShare-.8)<1e-12));
  if(mobility==='workers-only')assert.ok(r.rows.every(x=>x.eliteMove===0));
  if(mobility==='elite-only')assert.ok(r.rows.every(x=>x.workerMove===0));
 }
});
test('under the old assumed multiplier, moving hurdle changes elite exit',()=>{
 const M=ctx.AngkorRelocation,old={coordination:5**.227,waterFloor:.1},a=M.run({...old,movingCost:.05}),b=M.run({...old,movingCost:.5});
 assert.ok(a.finalEliteShare<b.finalEliteShare);
 assert.ok(a.exitYear!==null&&b.exitYear===null);
});

test('institution explorers preserve all 804 histories and the year55 timing repair',()=>{
 const D=ctx.AngkorInstitutionData;
 assert.equal(Object.values(D.models).reduce((n,m)=>n+Object.values(m).reduce((a,g)=>a+g.length,0),0),804);
 for(const climate of ['normal','drought'])for(let seed=0;seed<40;seed++){
  const a=D.models.maintenance['stable_'+climate][seed],b=D.models.maintenance['maintenance_only_'+climate][seed];
  assert.equal(JSON.stringify(a.slice(0,55)),JSON.stringify(b.slice(0,55)));
 }
 const w=worlds.find(w=>w.id==='maintenance');
 assert.equal(Math.round(w.run({scenario:'maintenance_only',climate:'drought',draw:0}).summary.state),6209);
 const a=worlds.find(w=>w.id==='accounts');
 assert.equal(Math.round(a.run({scenario:'reshuffle',climate:'drought',draw:0}).summary.state),4918);
});
test('all stored institution scenarios expose valid trajectories and downloadable csv',()=>{
 for(const id of ['institutions','flight','maintenance','accounts']){
  const w=worlds.find(w=>w.id===id);
  for(const scenario of Object.keys(w.controls[0].options))for(const climate of ['normal','drought']){
   const r=w.run({...w.defaults,scenario,...(id==='institutions'?{}:{climate,draw:39})});
   assert.ok(r.rows.every(x=>Number.isFinite(x[0])&&Number.isFinite(x[1])&&Number.isFinite(x[4])));
   assert.ok(w.csv(r).startsWith('scenario,year,state,refuge,total,canal,shortfall'));
   if(id!=='institutions')assert.ok(r.rows.every(x=>Math.abs(x[1]+x[2]-x[3])<.00001));
  }
 }
});
