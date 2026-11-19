/* Isolated adapters for shipped browser engines. Input/output: one JSON object. */
'use strict';
const fs=require('node:fs'),path=require('node:path'),vm=require('node:vm');
const root=path.resolve(__dirname,'..');
const load=name=>{const ctx=vm.createContext({});vm.runInContext(fs.readFileSync(path.join(root,'public/engines',name),'utf8'),ctx);return ctx;};
const seeded=seed=>{let s=seed>>>0;return()=>((s=(Math.imul(s,1664525)+1013904223)>>>0)+.5)/2**32;};
const mean=a=>a.reduce((x,y)=>x+y,0)/a.length;

function camchild(t){
  const M=load('camchild.js').CamChild,s=t.settings,r=seeded(t.parameter_seed),u=(a,b)=>a+(b-a)*r();
  const over={};
  if(s.uncertainty)for(const reg of ['pp','rural']){
    const b=M.REGIONS[reg];
    over[reg]={yMedian:b.yMedian*u(.75,1.25),debt:b.debt*u(.5,1.5),
      vPrim:b.vPrim*u(.8,1.2),vLow:b.vLow*u(.8,1.2),vUp:b.vUp*u(.8,1.2)};
  }
  const opts={N:s.n,years:s.years,seed:t.seed,over,randomMode:'indexed',wealthDefinition:s.wealth};
  const base=M.simulate(opts),last=base.rows.at(-1);
  const metrics={base_cl:last.all.cl,base_attend:last.all.attend,base_cl_poor:last.all.clPoor,
    base_cl_rich:last.all.clRich,base_migrant:last.all.migrant};
  const policies={cash:.075,cashU:.075,feeding:.5,protection:.5,leftSupport:.5,harvest:.5,
    bridging:.5,tutorFix:.5,ban:.5,debtRelief:.5,garmentBoom:.25,thaiOpen:0,floorRise:.5};
  for(const [name,value] of Object.entries(policies)){
    const result=M.simulate({...opts,policy:{[name]:value}}),a=result.rows.at(-1).all;
    metrics[name+'_effect_cl']=a.cl-last.all.cl;
    metrics[name+'_effect_attend']=a.attend-last.all.attend;
    metrics[name+'_effect_migrant']=a.migrant-last.all.migrant;
    metrics[name+'_child_years_avoided']=base.rows.reduce((v,row,i)=>v+(row.all.cl-result.rows[i].all.cl)*s.n,0);
    metrics[name+'_incremental_cost_index']=result.spent.total-base.spent.total;
    if(result.rows.some(row=>Math.abs(row.all.balance)>1e-10))throw Error('child-state accounting failed');
  }
  return {metrics,parameters:{over,policies,randomMode:opts.randomMode,wealthDefinition:s.wealth},
    evidence_role:'paired theoretical policy experiments across assumed nuisance ranges',
    limitation:'income proxies for wealth; simplified work classification; invented programme cost and response coefficients; school attendance calibration is definition-sensitive'};
}

function angkor(t){
  const P=load('petri.js').AngkorPetri,R=load('relocation.js').AngkorRelocation;
  const s=t.settings,r=seeded(t.parameter_seed),u=(a,b)=>a+(b-a)*r();
  const petri={...s,seed:t.seed,maintenance:u(.1,.8),extraction:u(.1,.4),relief:u(0,1)};
  petri.scenario=s.climate;
  const relocation={...s,seed:t.seed,outside:u(.8,1.6),movingCost:u(.05,.5),localRepair:u(0,1),portability:u(0,1)};
  const p=P.run(petri),a=R.run(relocation);
  const metrics={petri_retained:p.retained,petri_gap:p.gap,petri_ledger_error:p.maxLedgerError,
    elite_exit:Number(a.exitYear!==null),final_elite_share:a.finalEliteShare,
    old_water:a.oldWater,relocation_ledger_error:a.maxLedgerError,mass_error:a.maxMassError};
  for(const knockout of ['coordination','water','transport','relief','temple']){
    const b=P.run({...petri,knockout});
    metrics[knockout+'_effect_retained']=b.retained-p.retained;
    metrics[knockout+'_effect_gap']=b.gap-p.gap;
    if(b.maxLedgerError>1e-10)throw Error('Petri ledger failed');
  }
  for(const mobility of ['closed','elite-only','workers-only']){
    const b=R.run({...relocation,mobility});
    metrics[mobility+'_effect_water']=b.oldWater-a.oldWater;
    metrics[mobility+'_elite_exit']=Number(b.exitYear!==null);
    if(b.maxLedgerError>1e-10||b.maxMassError>1e-10)throw Error('relocation accounts failed');
  }
  if(p.maxLedgerError>1e-10||a.maxLedgerError>1e-10||a.maxMassError>1e-10)throw Error('baseline accounts failed');
  const monsoon=load('monsoon.js').AngkorMonsoon;
  // Distinct pre-generated parameter draws; explicitly report the reused index.
  const climateDraw=1+t.draw%2000;
  for(const sensitivity of [0,.04,.07,.10])for(const response of ['linear','exponential'])for(const pdsiCap of [null,3]){
    const q=monsoon.run({sensitivity,draw:climateDraw,response,pdsiCap,seed:t.seed});
    const key='pdsi_'+sensitivity+'/'+response+'/cap'+pdsiCap;
    metrics[key+'_onset']=Number(q.score.onset!==null);
    metrics[key+'_population_retained']=q.score.pop1431;
  }
  return {metrics,parameters:{petri,relocation},evidence_role:'mechanism knockouts, structural and parameter sensitivity',
    monsoon_parameter_index:climateDraw,
    limitation:'judgement sensitivities; PDSI crop coefficients are unsourced and extrapolated; accounting does not establish historical correspondence'};
}

function schools(){
  const dir=path.join(root,'public/reference/east-asia-schools/source/city');
  const read=name=>JSON.parse(fs.readFileSync(path.join(dir,name),'utf8'));
  const N=require(path.join(dir,'network.js')),G=require(path.join(dir,'guangzhou.js'));
  const hk=read('data.json'),gz=read('guangzhou.json'),approvals=read('approvals.json'),plans=read('plans.json');
  const h=N.testHistory(hk),g=G.backtest(gz),raw=[...h.historical,...h.workforceRows];
  const metrics={},backtests={};
  function summarize(city,rows){
    const groups={};
    for(const row of rows)(groups[row.metric]??=[]).push(row);
    for(const [name,group] of Object.entries(groups)){
      const errors=group.map(x=>Math.abs(x.model-x.actual)),naive=group.map(x=>Math.abs(x.naive-x.actual));
      metrics[city+'/'+name+'/mae']=mean(errors);metrics[city+'/'+name+'/benchmark_mae']=mean(naive);
      metrics[city+'/'+name+'/n']=group.length;
    }
    backtests[city]=rows;
  }
  summarize('hong_kong',raw);summarize('guangzhou',g);
  const scenarios=[];
  for(const births of [20000,30000,40000])for(const exitScale of [.35,1,1.5]){
    const result=N.run(hk,approvals,plans,{births,exitScale}).records;
    for(const [policy,years] of Object.entries(result))for(const year of [2031,2035,2040,2050]){
      scenarios.push({city:'hong_kong',births,exitScale,policy,year,stages:years[year]});
    }
  }
  for(const growth of [-.03,0,.02]){
    const result=G.simulate(gz,{longKgGrowth:growth});
    for(const [policy,years] of Object.entries(result))for(const year of [2031,2035,2040,2050])
      scenarios.push({city:'guangzhou',longKgGrowth:growth,policy,year,stages:years[year]});
  }
  // Expose multi-year errors from the original cohort model separately. The latest
  // merger-policy rules have no completed historical test and are never scored here.
  const C=require(path.join(dir,'model.js'));
  const multi=C.backtest(hk,false);
  summarize('hong_kong_multi_year',multi);
  const parent=path.dirname(dir),P=require(path.join(parent,'pipeline.js'));
  const systems=JSON.parse(fs.readFileSync(path.join(parent,'systems.json'),'utf8'));
  const population=JSON.parse(fs.readFileSync(path.join(parent,'population.json'),'utf8'));
  const national=[];
  for(const [system,definition] of Object.entries(systems)){
    if(definition.family)continue;
    for(const stage of Object.keys(definition.stages)){
      summarize(system+'/'+stage,P.historicalCheck({systems,population},system,stage).map(r=>
        ({metric:'pupils',actual:r.actual,model:r.expected,naive:r.flat,year:r.year})));
      for(const hiringTail of ['taper','hold2030'])for(const applicantRetention of [0,.5,1]){
        const rows=P.simulate({systems,population},system,stage,{hiringTail,applicantRetention});
        national.push({system,stage,hiringTail,applicantRetention,rows});
      }
    }
  }
  return {metrics,backtests,scenarios,national,
    evidence_role:'retrospective checks with current data vintage plus conditional scenarios',
    limitation:'Hong Kong closure backtests score the earlier historical rule; no completed test of latest merger rules; scenarios through 2050 have no validated probability distribution'};
}

const task=JSON.parse(fs.readFileSync(0,'utf8'));
const result={camchild,angkor,schools}[task.family](task);
// Python records undefined numerical fields; catch nonfinite Node metrics explicitly.
result.nonfinite_metrics=Object.entries(result.metrics).filter(([,v])=>typeof v==='number'&&!Number.isFinite(v)).map(([k])=>k);
process.stdout.write(JSON.stringify(result));
