// Exploratory factory-opening extension. No packages: node pathways_factory.cjs [seed count]
// Illustrative units are annual household income units, not currency.
const scenarios=['baseline','factory16','factorySecondary'];
function noise(seed,c,i,y,k){let x=seed+1009;for(const n of[c,i,y,k]){x=Math.imul(x^n,0x45d9f3b);x^=x>>>16}return(x>>>0)/4294967296}
// Yang et al. (2026), doi:10.1073/pnas.2509729123. Urban occupational diversity
// increases logarithmically with city size. Reference size, slope and employer
// credential rules below are illustrative assumptions for twelve factory posts.
function factoryOccupations(cityPopulation, scaling) {
 if (!Number.isFinite(cityPopulation) || cityPopulation <= 0) throw Error("Invalid city size");
 const count = scaling ? 2 + Math.floor(Math.log2(cityPopulation / 50000)) : 2;
 return Math.max(1, Math.min(12, count));
}
function run(seed,scenario,cityPopulation=50000,scaling=false,credentialGate=false){
 const people=[]; const years=36; let rows=[];
 for(let y=0;y<years;y++){
  // Same 64 arrivals/year as pathways.cjs, split evenly between urban and rural.
  for(let i=0;i<64;i++)if(y>=0)people.push({c:y,i,r:i%2,skill:noise(seed,y,i,0,2),school:noise(seed,y,i,0,3),g:0,left:false,completed:false});
  const row={seed,scenario,y,leaving:0,secondaryComplete:0,factoryJobs:0,farmWorkers:0,informalWorkers:0,formalWorkers:0,householdIncome:0,farmLaborOpportunityCost:0,students:0};
  const occupiedTypes = factoryOccupations(cityPopulation, scaling);
  row.factoryTypes = y >= 23 && scenario !== 'baseline' ? occupiedTypes : 0;
  const selected = new Set();
  if (y >= 23 && scenario !== 'baseline') {
   const ranked = people.filter(p => !p.left && 6+y-p.c >= 16 && 6+y-p.c <= 24)
    .sort((a,b) => noise(seed,a.c,a.i,y,8)-noise(seed,b.c,b.i,y,8));
   for (let slot=0; slot<12; slot++) {
    const occupation = slot % occupiedTypes;
    const needsDiploma = scenario==='factorySecondary' || (credentialGate && occupation>=2);
    const candidate = ranked.find(p => !selected.has(p) && (!needsDiploma || p.g>=12));
    if (candidate) selected.add(candidate);
   }
  }
  for(const p of people){
   const age=6+y-p.c;if(age<6||age>24||p.left)continue;
   const inSchool=p.g<16;
   // Per-person annual values. Farm = 1.0, informal = 1.4, formal = 2.0,
   // factory = 2.3. Going to school forgoes a 1.0 farm contribution.
   const farm=1.0, informal=1.4, formal=2.0, factory=2.3;
   let eligibleFactory= selected.has(p);
   let wage=eligibleFactory?factory:0;
   const alternative=age>=18?formal:informal;
   // School is chosen when expected qualification value and preference beat work income.
   const studyValue=.9+.8*p.school+.5*p.skill+(p.g<12?.45:0);
   const workValue=Math.max(farm,alternative,wage);
   let work=age>=16 && workValue>studyValue;
   if(work){p.left=true;row.leaving++; row.householdIncome+=workValue;
    if(wage===workValue){row.factoryJobs++}
    else if(age>=18&&formal===workValue)row.formalWorkers++;
    else if(informal===workValue)row.informalWorkers++;
    else row.farmWorkers++;
    continue;
   }
   if(inSchool){row.students++;row.householdIncome+=farm;row.farmLaborOpportunityCost+=farm;
    // Six-year primary, six-year secondary. Annual progression is uncertain.
    if(noise(seed,p.c,p.i,y,7)<.78+.18*p.skill){p.g++;if(p.g===12){p.completed=true;row.secondaryComplete++}}
   }
  }
  rows.push(row);
 }
 return rows;
}
if(require.main===module && process.argv.includes('--yang')){
 const seeds=Number(process.argv[2]) || 20;
 console.log('population,scaling,extra_types_require_diploma,types,annual_leaving,annual_secondary_completions,annual_factory_hires');
 for(const population of [50000,200000]) for(const scaling of [false,true]) for(const gate of [false,true]){
  const sums=[0,0,0];
  for(let seed=0;seed<seeds;seed++) for(const row of run(seed,'factory16',population,scaling,gate).slice(23)){
   [row.leaving,row.secondaryComplete,row.factoryJobs].forEach((v,i)=>sums[i]+=v);
  }
  console.log([population,scaling,gate,factoryOccupations(population,scaling),...sums.map(v=>(v/(13*seeds)).toFixed(3))].join(','));
 }
} else if(require.main===module){
 const n=Number(process.argv[2]||20), agg={};
 for(const s of scenarios){agg[s]=[];for(let seed=0;seed<n;seed++)agg[s].push(run(seed,s))}
 const years=[20,21,22,23,24,25,26,27,28,29,30,31,32,33,34,35];
 console.log('Assumptions: toy annual income units; farm 1.0, informal 1.4, formal 2.0, factory 2.3; students earn farm income but incur equal farm-labor opportunity cost. Factory opens y=23; factory16 eligible age >=16, factorySecondary eligible age >=16 with 12 completed grades. Choices use illustrative study-value rule; no calibration.');
 console.log(`Matched common seeds: ${n}. Pre-shock match check compares baseline and both policy arms for y=20..22: population, leaving, completion, jobs, and income.`);
 for(const y of [20,21,22]){let ok=true;for(let seed=0;seed<n;seed++){let a=agg.baseline[seed][y],b=agg.factory16[seed][y],c=agg.factorySecondary[seed][y];for(const k of ['leaving','secondaryComplete','factoryJobs','householdIncome'])if(a[k]!==b[k]||a[k]!==c[k])ok=false;}console.log(`pre-shock y=${y}: matched=${ok}`)}
 console.log('\nMean outcomes across seeds; years 23–35 (post opening):');
 console.log('scenario,leaving,secondary_completion,factory_jobs,farm_workers,informal_workers,formal_workers,household_income,farm_labor_opportunity_cost');
 for(const s of scenarios){let sums={};for(const r of agg[s])for(const y of years)for(const k of ['leaving','secondaryComplete','factoryJobs','farmWorkers','informalWorkers','formalWorkers','householdIncome','farmLaborOpportunityCost'])sums[k]=(sums[k]||0)+r[y][k];let denom=n*years.length;console.log([s,...['leaving','secondaryComplete','factoryJobs','farmWorkers','informalWorkers','formalWorkers','householdIncome','farmLaborOpportunityCost'].map(k=>(sums[k]/denom).toFixed(3))].join(','))}
 console.log('\nLimitation: this is an illustrative behavioral toy, with a deterministic choice rule and stylized income values; it does not estimate real wage, learning, capacity, or household responses.');
}
