'use strict';
globalThis.AngkorProvisioning = (() => {
  // Klassen, Ortman, Lobo & Evans, Table 5. Normalized associations, not grain tonnes.
  const coefficients = Object.freeze({beta:1.227, betaSE:.023, outputDistance:-.846, waterDistance:-.409, areaDistance:.521, platformElasticity:.085});
  const periods = [
    {begin:770,end:906,communities:93,population:24894,areaKm2:1327},
    {begin:907,end:961,communities:192,population:55062,areaKm2:1321},
    {begin:962,end:1001,communities:380,population:136912,areaKm2:1279},
    {begin:1002,end:1113,communities:511,population:184275,areaKm2:1244},
    {begin:1114,end:1180,communities:568,population:209357,areaKm2:1323},
    {begin:1181,end:1308,communities:571,population:213521,areaKm2:1323}
  ];
  const defaults=Object.freeze({community:500,distance:10,scaling:'fitted'});
  function run(options={}) {
    const controls={...defaults,...options};
    const beta=controls.scaling==='linear'?1:controls.scaling==='theory'?7/6:coefficients.beta;
    const population=10000;
    const scale=n=>100*(n/100)**(beta-1);
    const sizeCurve=Array.from({length:100},(_,i)=>({year:10*(i+1),index:scale(10*(i+1))}));
    const distanceCurve=Array.from({length:40},(_,i)=>{const d=i+1;return{year:d,output:100*(d/10)**coefficients.outputDistance,water:100*(d/10)**coefficients.waterDistance,area:100*(d/10)**coefficients.areaDistance};});
    return {controls,coefficients,beta,population,communityCount:population/controls.community,
      perPersonIndex:scale(controls.community),totalIndex:scale(controls.community),
      distanceOutput:100*(controls.distance/10)**coefficients.outputDistance,
      distanceWater:100*(controls.distance/10)**coefficients.waterDistance,
      distanceArea:100*(controls.distance/10)**coefficients.areaDistance,
      sizeCurve,distanceCurve,periods,
      scope:'Normalized published associations. Community size is a structural counterfactual. Population is fixed at 10,000 for the regrouping calculation. No calibrated food budget, famine relief, growth dynamics or collapse mechanism.'};
  }
  return{defaults,coefficients,periods,run};
})();
