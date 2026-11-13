'use strict';
globalThis.AngkorPetri=(()=>{
 // coordination: multiplier on harvest. New default 1 = no causal productivity effect.
 // Old behaviour: coordination 5**.227 (=1.441, base-5 exponent from the Klassen et al. size association).
 // waterFloor: lower bound on the hydraulic condition. New default 0 = no artificial floor. Old behaviour: 0.1.
 const defaults={scenario:'drought',knockout:'none',maintenance:.45,extraction:.2,relief:1,seed:42,coordination:1,waterFloor:0};
 const rng=seed=>{let s=seed>>>0;return()=>((s=(Math.imul(s,1664525)+1013904223)>>>0)/4294967296);};
 function run(options={}){
  const p={...defaults,...options},random=rng(p.seed),coord=p.knockout==='coordination'?1:p.coordination;
  let rural=.16,core=.015,land=.2,water=.5,temple=0,store=.03;const rows=[];
  for(let year=0;year<=240;year++){
   const weather=1+.04*(random()-.5);const drought=p.scenario==='drought'&&((year>=150&&year<175)||(year>=190&&year<205));
   const climate=weather*(drought?.62:1),people=rural+core;
   const hydraulic=p.knockout==='water'?1:.65+.35*water;
   const labour=Math.min(1,rural/Math.max(.001,.65*land));
   const harvest=land*1.5*coord*hydraulic*climate*labour;
   const transport=p.knockout==='transport'?1:.92;
   const collected=Math.min(harvest,p.extraction*harvest),retained=harvest-collected;
   const delivered=collected*transport,transportLoss=collected-delivered;
   const need=people,localNeed=rural,coreNeed=core;
   const localFood=Math.min(localNeed,retained),unusedLocal=Math.max(0,retained-localFood);
   let treasury=delivered+unusedLocal,coreFood=Math.min(coreNeed,treasury);treasury-=coreFood;
   const beforeStore=store,storageLoss=store*.04;store-=storageLoss;
   const householdGap=Math.max(0,localNeed-localFood)+Math.max(0,coreNeed-coreFood);
   const release=p.knockout==='relief'?0:Math.min(store,householdGap*p.relief);store-=release;
   const gap=householdGap-release;
   // All new investment and recurring obligations compete for this year's treasury.
   const obligation=p.knockout==='temple'?0:temple*.025;
   const ritual=Math.min(treasury,obligation);treasury-=ritual;
   const maintenanceNeed=land*.035;
   const upkeep=Math.min(treasury*p.maintenance,maintenanceNeed);treasury-=upkeep;
   const maintained=maintenanceNeed?upkeep/maintenanceNeed:1;
   const deposit=Math.min(treasury*.35,Math.max(0,people-store));store+=deposit;treasury-=deposit;
   const reclamation=Math.min(treasury*.55,Math.max(0,1-land)*.15);treasury-=reclamation;
   const construction=treasury;treasury=0;temple+=construction;
   land=Math.min(1,land+reclamation*.6);
   if(p.knockout!=='water')water=Math.max(p.waterFloor,Math.min(1,water+.08*(maintained-water)));
   const hunger=people?gap/people:0;
   const foodMargin=(harvest-people)/Math.max(.001,people);
   const growth=.012*Math.max(-1,Math.min(1,foodMargin));
   rural=Math.max(.001,rural*(1+growth-.08*hunger));
   core=Math.max(.0001,core*(1+growth-.08*hunger));
   // Migration changes residential stocks without changing total population.
   const attractiveness=Math.min(.22,.025+temple*.015);
   let migration=(rural+core)*attractiveness-core;
   migration*=hunger>.02?.15:.035;
   if(hunger>.02)migration-=core*.08*Math.min(1,hunger*5);
   migration=Math.max(-core*.2,Math.min(rural*.03,migration));rural-=migration;core+=migration;
   const foodUsed=localFood+coreFood+release;
   const ledger=harvest+beforeStore-(foodUsed+ritual+upkeep+deposit+reclamation+construction+transportLoss+storageLoss+store-deposit);
   rows.push({year,rural,core,population:rural+core,land,water,temple,store,harvest,gap,release,upkeep,construction,ledger});
  }
  const peak=rows.reduce((a,b)=>a.population>b.population?a:b),last=rows.at(-1);
  return{parameters:p,rows,peakYear:peak.year,peak:peak.population,final:last.population,finalCore:last.core,retained:last.population/peak.population,gap:rows.reduce((s,r)=>s+r.gap,0),maxLedgerError:Math.max(...rows.map(r=>Math.abs(r.ledger)))};
 }
 return{defaults,run};
})();
