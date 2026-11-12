(function(root) {
  "use strict";
  const START = 2020, BASE = 2025, END = 2050;
  const LENGTH = [3,6,3,3];
  const POLICIES = [
    {key:"reference",label:"Recent-response reference",site:[0.45,0.2,0.2,0.45],staff:1,protect:false},
    {key:"retain",label:"Retain staff and sites",site:[0.45,0.2,0.2,0.45],staff:1,protect:true},
    {key:"rapid",label:"Faster capacity adjustment",site:[0.85,0.5,0.5,0.65],staff:1.2,protect:false},
  ];
  const DEFAULTS={kgGrowth:-0.065,longKgGrowth:0,primaryDemand:0};
  const sum=a=>a.reduce((n,v)=>n+v,0);
  const clamp=(v,l,h)=>Math.min(h,Math.max(l,v));
  const median=a=>{
    const b=[...a].sort((x,y)=>x-y);
    return (b[Math.floor((b.length-1)/2)]+b[Math.ceil((b.length-1)/2)])/2;
  };
  const range=(a,b)=>Array.from({length:b-a+1},(_,i)=>a+i);
  const raw=(d,y,s)=>d.history[y-START][1][s];

  function reconstruct(data, year, stage) {
    const [,total,,entry]=raw(data,year,stage);
    if (!stage) return [total];
    const distribution=range(1,LENGTH[stage]-1).map(g=>raw(data,Math.max(START,year-g),stage)[3]);
    const factor=(total-entry)/sum(distribution);
    return [entry,...distribution.map(x=>x*factor)];
  }

  function coefficients(data, origin) {
    const years=range(Math.max(START+1,origin-2),origin);
    const movement=[null,...[1,2,3].map(s=>median(years.map(y=>{
      const prev=reconstruct(data,y-1,s).slice(0,-1);
      const [,pupils,,entry]=raw(data,y,s);
      return clamp((pupils-entry)/sum(prev),0.92,1.09);
    })))];
    const baseK=median(years.map(y=>raw(data,y,0)[1]/raw(data,y-1,0)[1]-1));
    const primary=median(years.map(y=>raw(data,y,1)[3]/raw(data,y-1,0)[1]));
    const junior=median(years.map(y=>{
      const leaving=raw(data,y-1,1)[4]??reconstruct(data,y-1,1).at(-1);
      return raw(data,y,2)[3]/leaving;
    }));
    const senior=median(years.map(y=>raw(data,y,3)[3]/reconstruct(data,y-1,2).at(-1)));
    return {movement,baseK,primary,junior,senior};
  }

  function demand(data,origin,end,settings) {
    const fit=coefficients(data,origin);
    const rows={};
    rows[origin]=data.stages.map((_,s)=>reconstruct(data,origin,s));
    let unshiftedIntake=rows[origin][1][0];
    for(const year of range(origin+1,end)){
      const previous=rows[year-1];
      const horizon=year-origin;
      const previousK=previous[0][0];
      const previousPreviousK=rows[year-2]?.[0][0]??raw(data,origin-1,0)[1];
      const initialRate=settings?.kgGrowth??fit.baseK;
      const longWeight=settings ? clamp((year-2031)/5,0,1) : 0;
      const nearRate=initialRate*Math.max(0.35,1-0.1*(horizon-1));
      const kRate=nearRate*(1-longWeight)+(settings?.longKgGrowth??0)*longWeight;
      const kindergarten=Math.round(previousK*(1+kRate));
      const smoothIntake=fit.primary*previousK;
      const linkedIntake=unshiftedIntake*previousK/previousPreviousK;
      unshiftedIntake=Math.round(0.6*smoothIntake+0.4*linkedIntake);
      const primary=unshiftedIntake*(1+(settings?.primaryDemand??0)*Math.min(1,horizon/4));
      const p6=year===origin+1?(raw(data,origin,1)[4]??previous[1].at(-1)):previous[1].at(-1);
      const entrants=[kindergarten,primary,p6*fit.junior,previous[2].at(-1)*fit.senior];
      rows[year]=entrants.map((n,s)=>s?[Math.round(n),...previous[s].slice(0,-1).map(x=>Math.round(x*fit.movement[s]))]:[n]);
    }
    return rows;
  }

  function simulate(data, settings={}) {
    const opts={...DEFAULTS,...settings};
    const path=demand(data,BASE,END,opts);
    return Object.fromEntries(POLICIES.map(policy=>[policy.key,Object.fromEntries(range(BASE,END).map(y=>[
      y,path[y].map((grades,s)=>{
        const [baseSites,basePupils,baseStaff]=raw(data,BASE,s);
        const enrollment=Math.round(sum(grades));
        const ratio=enrollment/basePupils;
        const sites=Math.round(baseSites*ratio**policy.site[s]);
        const staff=Math.round(baseStaff*ratio**policy.staff);
        return {enrollment,entry:s?Math.round(grades[0]):null,
          sites:policy.protect?Math.max(baseSites,sites):sites,
          staff:policy.protect?Math.max(baseStaff,staff):staff,
        };
      }),
    ]))]));
  }

  function backtest(data) {
    const out=[];
    for(const origin of range(2022,2024)){
      const year=origin+1;
      const result=demand(data,origin,year)[year];
      for(const [s,x] of result.entries()){
        const previous=raw(data,origin,s),actual=raw(data,year,s);
        const forecast=Math.round(sum(x));
        out.push({origin,year,stage:s,metric:"pupils",model:forecast,actual:actual[1],naive:previous[1]});
        if(s) out.push({origin,year,stage:s,metric:"entry",model:x[0],actual:actual[3],naive:previous[3]});
        // Check the transparent capacity rule independently of the policy stress cases.
        const f=forecast/previous[1];
        out.push({origin,year,stage:s,metric:"sites",model:Math.round(previous[0]*f**POLICIES[0].site[s]),actual:actual[0],naive:previous[0]});
        out.push({origin,year,stage:s,metric:"staff",model:Math.round(previous[2]*f),actual:actual[2],naive:previous[2]});
      }
    }
    return out;
  }
  const api={BASE,END,POLICIES,DEFAULTS,simulate,backtest};
  if(typeof module==="object"&&module.exports)module.exports=api;
  else root.Guangzhou=api;
})(globalThis);
