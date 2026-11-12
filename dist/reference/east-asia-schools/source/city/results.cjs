const fs=require("node:fs"),path=require("node:path");
const N=require("./network.js"),G=require("./guangzhou.js");
const hk=require("./data.json"),approvals=require("./approvals.json"),plans=require("./plans.json");
const profiles=require("./primary-profiles.json"),gz=require("./guangzhou.json");
const out=process.argv[2]??"results";
fs.mkdirSync(out,{recursive:true});
const quote=x=>'"'+String(x??"").replaceAll('"','""')+'"';
function csv(name,header,body){
  fs.writeFileSync(path.join(out,name+".csv"),[header,...body].map(row=>row.map(quote).join(",")).join("\n")+"\n");
}
const a=N.run(hk,approvals,plans), b=G.simulate(gz);
const keys=["entry","enrollment","sites","staff","classes","classSize","required","departures","hires","netTeacherChange","cutsFrom2025","involuntary","planned"];
const forecast=(data,cases,stages)=>cases.flatMap(p=>Object.entries(data[p.key]).flatMap(([year,values])=>
  values.map((r,s)=>[year,stages[s],p.label,...keys.map(k=>r[k])]))); 
const prefix=["year","stage","policy",...keys];
csv("hong_kong_default_scenarios",prefix,forecast(a.records,N.CASES,N.stages));
csv("guangzhou_default_scenarios",prefix,forecast(b,G.POLICIES,gz.stages));
const t=N.testHistory(hk);
csv("backtests",["city","origin","year","stage","metric","actual","model","benchmark","conditional_given_enrollment"],[
  ...[...t.historical,...t.workforceRows].map(r=>["Hong Kong",r.origin,r.year,N.stages[r.stage],r.metric,r.actual,r.model,r.naive,r.conditional]),
  ...G.backtest(gz).map(r=>["Guangzhou",r.origin,r.year,gz.stages[r.stage],r.metric,r.actual,r.model,r.naive]),
]);
csv("hong_kong_primary_approvals_by_district",["district","matched_public_profiles","previous_P1","approved_P1","newly_zero_P1"],
  N.districtApprovals(profiles,hk.districts).map(d=>Object.values(d)));
csv("hong_kong_reported_school_plans",["school","status","merger_partner","timing_used","effective_year","source"],
  plans.schools.map(r=>[...r.slice(0,5),r[5]??plans.reported.url]));

const pick2050=(city,label,stages,results)=>results.map((r,s)=>[city,label,2050,stages[s],r.enrollment,r.sites,r.staff]);
csv("2050_demand_sensitivities",["city","demand_assumption","year","stage","enrollment","school_operations","teachers"],[
  ...[-0.03,0.02].flatMap(birthGrowth=>pick2050("Hong Kong",Math.round(birthGrowth*100)+"% annual birth growth at 30000 starting births",
    N.stages,N.run(hk,approvals,plans,{birthGrowth}).records.policy[2050])),
  ...[20000,30000,40000].flatMap(births=>pick2050("Hong Kong",births+" births/year",N.stages,N.run(hk,approvals,plans,{births}).records.policy[2050])),
  ...[-0.03,0,0.02].flatMap(longKgGrowth=>pick2050("Guangzhou",Math.round(longKgGrowth*100)+"% long-run annual preschool growth",
    gz.stages,G.simulate(gz,{longKgGrowth}).reference[2050])),
]);
