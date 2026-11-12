'use strict';
globalThis.AngkorAllocation=(()=>{
 const sectors=['agriculture','military','irrigation','monuments','religion'];
 const defaults={allocation:{agriculture:.5,military:.2,irrigation:.15,monuments:.1,religion:.05},tax:.35,distanceStep:45,garrisonPerTown:150,expansion:true,climate:'stable',religionCoordination:true,seed:42,years:60,frontierTowns:12,waterMaintenance:10,shiftAt:10000,afterAllocation:null};
 const C={homePopulation:20000,adults:.45,days:180,bondedShare:.15,homeLand:4000,homeLandCap:6000,frontierTowns:12,townPopulation:1000,townLand:350,annualRation:.21,yield:1.6,postHarvestRetention:.84,farmDaysPerHa:162,homeGuard:200,initialHouseholdStore:3000,initialCourtStore:2000};
 const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
 function run(options={}){
  const p={...defaults,...options,allocation:{...defaults.allocation,...options.allocation}};
  const sum=sectors.reduce((n,k)=>n+p.allocation[k],0);
  if(Math.abs(sum-1)>1e-10||sectors.some(k=>!Number.isFinite(p.allocation[k])||p.allocation[k]<0))throw Error('Labour shares must be nonnegative and sum to one');
  if(p.afterAllocation && (Math.abs(sectors.reduce((n,k)=>n+p.afterAllocation[k],0)-1)>1e-10||sectors.some(k=>!Number.isFinite(p.afterAllocation[k])||p.afterAllocation[k]<0)))throw Error('Invalid later allocation');
  let state=p.seed>>>0;const random=()=>((state=(Math.imul(state,1664525)+1013904223)>>>0)/4294967296);
  let towns=[],homeLand=C.homeLand,water=.6,roads=.1,monument=0,household=C.initialHouseholdStore,court=C.initialCourtStore,compliance=1;
  const rows=[];let maxGrainError=0,maxLabourError=0,maxPopulationError=0;
  for(let year=0;year<p.years;year++){
   // Consume fixed draws in every policy, whether it campaigns or not.
   const weatherDraw=random(),battleDraw=random();
   const dry=p.climate==='drought'&&((year>=25&&year<31)||(year>=43&&year<47));
   const weather=(.94+.12*weatherDraw)*(dry?.7:1);
   const startTowns=towns.length,population=C.homePopulation+startTowns*C.townPopulation;
   const labourSupply=population*C.adults*C.days;
   const shares=year>=p.shiftAt&&p.afterAllocation?p.afterAllocation:p.allocation;
   const planned=Object.fromEntries(sectors.map(k=>[k,shares[k]*labourSupply]));
   // Bonded labour is excluded from military recruitment; unfilled military slots remain idle.
   planned.military=Math.min(planned.military,labourSupply*(1-C.bondedShare));
   const openingGrain=household+court,spoilage=openingGrain*.06;household*=.94;court*=.94;
   const land=homeLand+startTowns*C.townLand,requiredFarmDays=land*C.farmDaysPerHa;
   const farmCoverage=Math.min(1,planned.agriculture/requiredFarmDays);
   const harvest=land*C.yield*C.postHarvestRetention*weather*(.8+.2*water)*farmCoverage;
   const collected=harvest*p.tax*compliance,meanDistance=startTowns?towns.reduce((n,t)=>n+t.distance,0)/(startTowns+1):0;
   const transportLoss=collected*Math.min(.5,meanDistance*.0008/(1+roads));
   household+=harvest-collected;court+=collected-transportLoss;
   const requiredGarrison=C.homeGuard+startTowns*p.garrisonPerTown;
   const plannedMilitaryPeople=planned.military/365;
   const plannedFieldDays=Math.max(0,planned.military-requiredGarrison*365);
   const frontierDistance=60+startTowns*p.distanceStep;
   const campaignDuration=60+2*frontierDistance/20;
   const plannedCampaignPeople=p.expansion&&startTowns<p.frontierTowns?plannedFieldDays/campaignDuration:0;
   const logisticsNeed=plannedMilitaryPeople*.00002*meanDistance+plannedCampaignPeople*.00004*frontierDistance;
   const publicDays=planned.military+planned.irrigation+planned.monuments+planned.religion;
   const publicRationsNeed=publicDays/365*C.annualRation;
   const funded=Math.min(1,court/Math.max(1e-12,publicRationsNeed+logisticsNeed));
   const publicRations=publicRationsNeed*funded,logistics=logisticsNeed*funded;court-=publicRations+logistics;
   const actual={agriculture:planned.agriculture,...Object.fromEntries(sectors.filter(k=>k!=='agriculture').map(k=>[k,planned[k]*funded]))};
   const publicPeople=publicRations/C.annualRation;
   const civilianNeed=(population-publicPeople)*C.annualRation;
   const householdFood=Math.min(household,civilianNeed);household-=householdFood;
   const relief=Math.min(court,Math.max(0,civilianNeed-householdFood));court-=relief;
   const foodGap=Math.max(0,civilianNeed-householdFood-relief);
   // Soldiers' ordinary rations are included above, never charged again to civilians.
   const militaryPeople=actual.military/365,garrisonFilled=Math.min(requiredGarrison,militaryPeople);
   const garrisonCoverage=requiredGarrison?garrisonFilled/requiredGarrison:1;
   const availableFieldDays=Math.max(0,actual.military-garrisonFilled*365);
   const campaignPeople=p.expansion&&startTowns<p.frontierTowns?availableFieldDays/campaignDuration:0;
   const infraForRoads=actual.irrigation*.25,infraForWater=actual.irrigation-infraForRoads;
   const maintenanceNeed=land*p.waterMaintenance,upkeep=Math.min(maintenanceNeed,infraForWater);
   const upkeepCoverage=maintenanceNeed?upkeep/maintenanceNeed:1;
   water=clamp(water*.94+.06*upkeepCoverage,.1,1);
   roads=clamp(roads*.96+infraForRoads/2000000,0,1);
   const reclamation=Math.min(Math.max(0,infraForWater-upkeep)/250,C.homeLandCap-homeLand);homeLand+=reclamation;
   const monumentNeed=monument*.01,monumentUpkeep=Math.min(monumentNeed,actual.monuments);
   monument=monument*(1-.03*(monumentNeed?1-monumentUpkeep/monumentNeed:0))+Math.max(0,actual.monuments-monumentUpkeep);
   const ritualNeed=.04*labourSupply,ritualCoverage=Math.min(1,actual.religion/ritualNeed);
   compliance=p.religionCoordination?.85+.15*ritualCoverage:1;
   let joined=0,left=0;
   for(const town of towns)town.neglect=garrisonCoverage<.75?town.neglect+1:0;
   if(towns.length&&towns.at(-1).neglect>=2){towns.pop();left=C.townPopulation;}
   else if(p.expansion&&towns.length<p.frontierTowns&&campaignPeople>=350&&foodGap===0){
    const probability=clamp(.25+.5*(campaignPeople-350)/700,.25,.9);
    if(battleDraw<probability){towns.push({distance:frontierDistance,neglect:0});joined=C.townPopulation;}
   }
   // A seceding town takes its proportional share of the pooled household store.
   const exportGrain=left?household*left/population:0;household-=exportGrain;
   const afterPopulation=C.homePopulation+towns.length*C.townPopulation;
   const popError=population+joined-left-afterPopulation;
   const paidFood=publicRations+householdFood+relief;
   const grainError=openingGrain+harvest-spoilage-transportLoss-logistics-paidFood-exportGrain-household-court;
   const actualTotal=sectors.reduce((n,k)=>n+actual[k],0),idle=labourSupply-actualTotal;
   const labourError=labourSupply-actualTotal-idle;
   maxGrainError=Math.max(maxGrainError,Math.abs(grainError));maxLabourError=Math.max(maxLabourError,Math.abs(labourError));maxPopulationError=Math.max(maxPopulationError,Math.abs(popError));
   rows.push({year,population,afterPopulation,towns:startTowns,afterTowns:towns.length,labourSupply,...Object.fromEntries(sectors.map(k=>[k+'Days',actual[k]])),idleDays:idle,harvest,householdStore:household,courtStore:court,spoilage,transportLoss,logistics,publicRations,civilianNeed,householdFood,relief,foodGap,requiredGarrison,garrisonFilled,garrisonCoverage,campaignPeople,campaignDuration,frontierDistance,farmCoverage,upkeepCoverage,water,roads,monument,ritualCoverage,joined,left,exportGrain,grainError,labourError,popError});
  }
  const last=rows.at(-1);return{parameters:p,constants:C,rows,finalTowns:last.afterTowns,peakTowns:Math.max(...rows.map(r=>r.afterTowns)),lostTowns:rows.filter(r=>r.left).length,foodGap:rows.reduce((n,r)=>n+r.foodGap,0),garrisonShortYears:rows.filter(r=>r.garrisonCoverage<.75).length,finalWater:last.water,finalMonument:last.monument,maxGrainError,maxLabourError,maxPopulationError};
 }
 return{defaults,constants:C,sectors,run};
})();
