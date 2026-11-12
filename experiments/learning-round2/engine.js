'use strict';
globalThis.AngkorLearningRound2=(()=>{
 const defaults={outside:1.2,portability:.75,movingCost:.25,localRepair:.5,climate:'drought',mobility:'open',seed:42,mode:'fixed',learningRate:.03,lossStrength:.5,initialKnowledge:.5,carrier:'elite',retention:0,forgetting:0,obligationDecay:0,templeRate:.025,southDrought:.85,beta:1.227,maintenanceFirst:false,forcedExit:0,shockYear:120};
 const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
 const rng=seed=>{let s=seed>>>0;return()=>((s=(Math.imul(s,1664525)+1013904223)>>>0)/4294967296);};
 const initial=(rural,core,land,elite)=>({rural,core,land,elite,knowledge:.5,water:.6,temple:0,store:.03});
 function economy(s,weather,localRepair,eliteShare,p){
  const coordination=1+(5**(p.beta-1)-1)*s.knowledge;
  const before=s.store,people=s.rural+s.core+s.elite;
  const harvest=s.land*1.5*coordination*(.65+.35*s.water)*weather*Math.min(1,s.rural/(.65*s.land));
  // Local upkeep can continue independently of elite participation.
  const maintenanceNeed=s.land*.035;
  const tax=harvest*.2*(.3+.7*eliteShare),retained=harvest-tax;
  const farmFood=Math.min(s.rural,retained),farmGap=s.rural-farmFood;
  const farmSurplus=retained-farmFood;
  const localUpkeep=Math.min(farmSurplus,localRepair*maintenanceNeed);
  const householdOther=farmSurplus-localUpkeep;
  const transportLoss=tax*.08;let budget=tax-transportLoss;
  const urbanNeed=s.core+s.elite,urbanFood=Math.min(urbanNeed,budget);budget-=urbanFood;
  const storageLoss=s.store*.04;s.store-=storageLoss;
  const rawGap=farmGap+urbanNeed-urbanFood,release=Math.min(s.store,rawGap);s.store-=release;
  const gap=rawGap-release,hunger=gap/people;
  let ritual,courtUpkeep;
  if(p.maintenanceFirst){
   courtUpkeep=Math.min(budget*.45,Math.max(0,maintenanceNeed-localUpkeep));budget-=courtUpkeep;
   ritual=Math.min(budget,s.temple*p.templeRate);budget-=ritual;
  }else{
   ritual=Math.min(budget,s.temple*p.templeRate);budget-=ritual;
   courtUpkeep=Math.min(budget*.45,Math.max(0,maintenanceNeed-localUpkeep));budget-=courtUpkeep;
  }
  const deposit=Math.min(budget*.35,Math.max(0,people-s.store));s.store+=deposit;budget-=deposit;
  const reclamation=Math.min(budget*.55,(1-s.land)*.15);budget-=reclamation;
  const construction=budget;s.temple=s.temple*(1-p.obligationDecay)+construction;s.land=Math.min(1,s.land+reclamation*.6);
  const upkeep=localUpkeep+courtUpkeep;s.water=clamp(s.water+.08*(upkeep/maintenanceNeed-s.water),.1,1);
  const completed=clamp((upkeep+reclamation+construction)/Math.max(.001,maintenanceNeed+.04*s.land),0,1);
  const forgotten=p.mode==='fixed'?0:s.knowledge*p.forgetting;
  s.knowledge-=forgotten;
  const learned=p.mode==='fixed'?0:p.learningRate*completed*(1-s.knowledge);
  s.knowledge=clamp(s.knowledge+learned,0,1);
  const growth=.012*clamp((harvest-people)/people,-1,1)-.08*hunger;
  const demographicChange=(s.rural+s.core)*growth;s.rural*=1+growth;s.core*=1+growth;
  const foodUsed=farmFood+urbanFood+release;
  const ledger=harvest+before-(foodUsed+householdOther+transportLoss+ritual+upkeep+reclamation+construction+storageLoss+s.store);
  // Utilities are declared indices, not recovered historical prices or measured income.
  const coverage=clamp((urbanFood+release*(urbanNeed/people))/Math.max(.0001,urbanNeed),0,1);
  return{harvest,gap,upkeep,completed,learned,forgotten,maintained:upkeep/maintenanceNeed,ledger,demographicChange,
    returnIndex:.65*coverage+.35*s.water-2*hunger};
 }
 function run(options={}){
  const p={...defaults,...options},random=rng(p.seed),old=initial(.16,.015,.2,.008),south=initial(.05,.005,.08,.002),eliteTotal=.01;
  old.knowledge=south.knowledge=p.initialKnowledge;
  const rows=[];let maxMassError=0,maxLedgerError=0;
  for(let year=0;year<=240;year++){
   const noise=1+.04*(random()-.5),dry=p.climate==='drought'&&((year>=150&&year<175)||(year>=190&&year<205));
   const oldShare=old.elite/eliteTotal, southShare=south.elite/eliteTotal;
   const a=economy(old,noise*(dry?.62:1),p.localRepair,oldShare,p);
   const b=economy(south,noise*(dry?p.southDrought:1),p.localRepair,southShare,p);
   // The southern climate and market advantage are scenario assumptions.
   const oldUtility=a.returnIndex;
   const southUtility=p.outside*b.returnIndex-(1-p.portability)*.5*old.water;
   const advantage=southUtility-oldUtility;
   const massBefore=old.rural+old.core+old.elite+south.rural+south.core+south.elite;
   const oldEliteBefore=old.elite,southEliteBefore=south.elite;
   let eliteMove=0,workerMove=0,knowledgeTransferred=0,knowledgeOverflow=0;
   if(p.mobility==='open'||p.mobility==='elite-only'){
    if(advantage>p.movingCost)eliteMove=old.elite*Math.min(.08,.12*(advantage-p.movingCost));
    if(advantage < -p.movingCost)eliteMove=-south.elite*Math.min(.08,.12*(-advantage-p.movingCost));
    old.elite-=eliteMove;south.elite+=eliteMove;
   }
   if(p.mobility==='open'||p.mobility==='workers-only'){
    // Workers respond to food coverage and shifts in demand, at a different rate.
    const jobsShift=(south.elite/eliteTotal-.2)*.3;
    const workerAdvantage=(b.returnIndex-a.returnIndex)+jobsShift;
    if(workerAdvantage>.15)workerMove=old.core*Math.min(.025,.04*(workerAdvantage-.15));
    if(workerAdvantage<-.15)workerMove=-south.core*Math.min(.025,.04*(-workerAdvantage-.15));
    old.core-=workerMove;south.core+=workerMove;
   }
   if(p.forcedExit>0 && year===p.shockYear && p.mobility==='closed'){
    eliteMove=old.elite*p.forcedExit;old.elite-=eliteMove;south.elite+=eliteMove;
   }
   function transfer(move,originPopulation,weight){
    if(!move||!weight)return;
    const from=move>0?old:south,to=move>0?south:old;
    const amount=from.knowledge*p.lossStrength*(1-p.retention)*weight*Math.abs(move)/Math.max(1e-12,originPopulation);
    from.knowledge-=amount;
    const overflow=Math.max(0,to.knowledge+amount-1);
    to.knowledge=Math.min(1,to.knowledge+amount);
    knowledgeTransferred+=amount;knowledgeOverflow+=overflow;
   }
   if(p.mode==='learning-loss'){
    transfer(eliteMove,eliteMove>=0?oldEliteBefore:southEliteBefore,p.carrier==='worker'?0:p.carrier==='mixed'?.5:1);
    transfer(workerMove,workerMove>=0?old.core+workerMove:south.core-workerMove,p.carrier==='elite'?0:p.carrier==='mixed'?.5:1);
   }
   const massAfter=old.rural+old.core+old.elite+south.rural+south.core+south.elite;
   maxMassError=Math.max(maxMassError,Math.abs(massAfter-massBefore),Math.abs(old.elite+south.elite-eliteTotal));
   maxLedgerError=Math.max(maxLedgerError,Math.abs(a.ledger),Math.abs(b.ledger));
   rows.push({year,oldEliteShare:old.elite/eliteTotal,oldRural:old.rural,oldCore:old.core+old.elite,
    southRural:south.rural,southCore:south.core+south.elite,oldWater:old.water,southWater:south.water,
    oldUpkeep:a.maintained,southUpkeep:b.maintained,oldHarvest:a.harvest,southHarvest:b.harvest,
    oldGap:a.gap,southGap:b.gap,oldUtility,southUtility,eliteMove,workerMove,
    oldLedger:a.ledger,southLedger:b.ledger,oldKnowledge:old.knowledge,southKnowledge:south.knowledge,oldLearned:a.learned,southLearned:b.learned,oldForgotten:a.forgotten,southForgotten:b.forgotten,knowledgeTransferred,knowledgeOverflow});
  }
  let exitYear=null;for(let i=0;i<=rows.length-10;i++){if(rows.slice(i,i+10).every(r=>r.oldEliteShare<.4)){exitYear=rows[i].year;break;}}
  const last=rows.at(-1),ruralPeak=Math.max(...rows.map(r=>r.oldRural)),corePeak=Math.max(...rows.map(r=>r.oldCore));
  return{parameters:p,rows,exitYear,finalEliteShare:last.oldEliteShare,oldRuralRetained:last.oldRural/ruralPeak,
    oldCoreRetained:last.oldCore/corePeak,oldWater:last.oldWater,oldKnowledge:last.oldKnowledge,foodGap:rows.reduce((s,r)=>s+r.oldGap,0),maxMassError,maxLedgerError};
 }
 return{defaults,run};
})();
