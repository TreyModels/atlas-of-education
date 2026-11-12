/* Angkor Mandala Lab model v1.0. Offline JavaScript, deterministic for each seed.
   A deliberately stylized mechanism test, NOT a historical reconstruction. */
(function (root, factory) {
  const api = factory();
  if (typeof module === 'object' && module.exports) module.exports = api;
  else root.AngkorModel = api;
})(typeof globalThis !== 'undefined' ? globalThis : this, function () {
  'use strict';
  const clamp=(x,a,b)=>Math.max(a,Math.min(b,x));
  function rng(seed){let a=(seed>>>0)||1;return ()=>{a+=0x6D2B79F5;let t=a;t=Math.imul(t^(t>>>15),t|1);t^=t+Math.imul(t^(t>>>7),t|61);return ((t^(t>>>14))>>>0)/4294967296;};}
  const normal=(r)=>{let u=1-r(),v=1-r();return Math.sqrt(-2*Math.log(Math.max(1e-9,u)))*Math.cos(2*Math.PI*v);};
  const DEFAULTS = Object.freeze({start:850,end:1450,seed:42,population:250000,regionKm2:3000,riceKm2:1100,yieldT:1.6,lossPct:16,riceKg:200,importsT:6000,localShare:0.62,estateShare:0.25,hydraulicDependency:0.45,maintenanceIntensity:0.38,climateVolatility:0.11,growthPct:0.65,corveeDays:24,bonded:10000,bondedBirthPct:1.0,raidIntensity:0.45,diplomacy:0.48,warExpense:0.28,buildShare:0.34,monumentSkill:0.65,ritualMobilityPct:8,tradeIntegration:0.48,templeAutonomy:0.52,coreShare:0.16,defenseSpend:0.15,sackShock:0,lateDrought:0.18,marketElasticity:0.35,conquestDamage:0.4});
  const PRESETS = {
    'reference': {name:'Evidence-anchored starting assumptions',zh:'证据约束的起点假设', patch:{},note:'Indicative midpoint assumptions; many values remain unidentified. Starting population refers to the whole modeled region.',zhNote:'示意性中点假设；多数参数仍无确定史料依据。人口指整个模拟区域。'},
    'villages': {name:'Autonomous irrigation villages',zh:'自治灌溉村落', patch:{localShare:.89,estateShare:.07,hydraulicDependency:.18,maintenanceIntensity:.21,corveeDays:10,raidIntensity:.15,templeAutonomy:.74},note:'Bali-like coordination mechanisms, not a claim that Angkor was Bali.',zhNote:'参考巴厘岛式合作机制，不代表吴哥与巴厘岛相同。'},
    'estates': {name:'Elite estate consolidation',zh:'精英庄园整合', patch:{localShare:.28,estateShare:.69,hydraulicDependency:.73,maintenanceIntensity:.66,corveeDays:50,bonded:35000,raidIntensity:.67,buildShare:.44},note:'Tests forced labor, consolidated land and maintenance-sensitive engineering.',zhNote:'测试强迫劳动、土地集中及依赖维护的工程体系。'},
    'raiding': {name:'Captive-raiding military engine',zh:'掳掠劳动力的军事体系', patch:{raidIntensity:.9,diplomacy:.22,bonded:24000,corveeDays:35,warExpense:.50,defenseSpend:.14,estateShare:.48},note:'Captive acquisition can supply labor while also destabilizing neighbors and consuming surplus.',zhNote:'掠夺能够补充劳力，同时消耗剩余并扰乱周边局势。'},
    'court': {name:'Fortified royal monumentalism',zh:'设防王权与纪念建筑', patch:{buildShare:.58,monumentSkill:.78,defenseSpend:.44,warExpense:.32,templeAutonomy:.25,localShare:.4},note:'Tests tradeoffs among masonry, fortification, irrigation and armies.',zhNote:'比较石造纪念物、防御工程、灌溉与军队的资源竞争。'},
    'trade': {name:'Commercial and monastic continuity',zh:'贸易与寺院延续', patch:{importsT:25000,tradeIntegration:.85,marketElasticity:.68,templeAutonomy:.85,diplomacy:.7,localShare:.72},note:'Allows independent merchants and religious institutions to support population after a court changes.',zhNote:'商人和寺院可在王庭更替后继续支撑人口。'},
    'climate': {name:'Late drought and flood instability',zh:'晚期旱涝波动', patch:{climateVolatility:.24,lateDrought:.43,hydraulicDependency:.79,maintenanceIntensity:.60,importsT:3000},note:'A hypothetical stressed network, not a deterministic climate-collapse claim.',zhNote:'假设水网压力情境，而非预设气候必然导致崩溃。'},
    'mandala': {name:'Competitive mandala geopolitics',zh:'曼荼罗式霸权竞争',patch:{raidIntensity:.76,diplomacy:.22,warExpense:.54,defenseSpend:.36,tradeIntegration:.32,conquestDamage:.62},note:'Competing regional courts, shifting allegiances and endogenous attacks.',zhNote:'区域王庭竞争、附属关系变动与内生战争。'},
    'chronology': {name:'Historical-event stress test',zh:'历史事件冲击测试',patch:{sackShock:.55,lateDrought:.31,raidIntensity:.57},note:'Stylized 1177 war shock and increased post-1300 climate pressure. Dates are interpretive anchors; impacts are assumed.',zhNote:'1177年战争冲击与1300年后气候压力；日期有史学依据，强度是假设。'}
  };
  const GRID_W=14, GRID_H=10;
  function initialize(p,r){
    const cells=[];let weightSum=0, arableWeight=0;
    for(let y=0;y<GRID_H;y++)for(let x=0;x<GRID_W;x++){
      const xdist=(x-6.3)/7, ydist=(y-5.9)/5.8;
      const access=clamp(1.14-0.7*Math.sqrt(xdist*xdist+ydist*ydist)+.17*(r()-.5),.15,1.35);
      const upland=y<2, flood=y>7;
      const fertility=clamp(.72+.4*r()+.12*(flood?1:0)-.17*(upland?1:0),.48,1.35);
      const wt=Math.max(.04,access*fertility*(upland?.55:1)*(flood?.7:1));
      const arable=clamp(fertility*(flood?.72:1)*(upland?.5:1),.12,1.55);
      weightSum+=wt; arableWeight+=arable;
      cells.push({x,y,access,fertility,weight:wt,arable,pop:0,fields:0,loyalty:0,infra:clamp(.32+.45*access+.1*r(),.2,.9),local:clamp(p.localShare+.18*(r()-.5),.03,.98)});
    }
    cells.forEach(c=>{c.pop=p.population*c.weight/weightSum;c.fields=p.riceKm2*c.arable/arableWeight; c.loyalty=clamp(.36+.30*c.access+.18*r(),.05,.99)});
    return cells;
  }
  const periods=[{year:850,label:'Foundation / early expansion'},{year:1000,label:'Agrarian and political expansion'},{year:1113,label:'Suryavarman II / Angkor Wat'},{year:1177,label:'Cham attack / military crisis'},{year:1181,label:'Jayavarman VII / rebuilding'},{year:1300,label:'Later Angkor / climatic variability'},{year:1431,label:'Political-center transition'}];
  function step(s,p,year,r){
    const {cells}=s;
    const prePop=cells.reduce((a,c)=>a+c.pop,0);
    const seasonal=year>=1300?Math.max(0,(year-1300)/125):0;
    const shock=clamp(normal(r)*p.climateVolatility+(year>=1300?-(p.lateDrought*seasonal*.42):0),-.72,.55);
    let fieldProduction=0,maintenanceNeed=0,alignment=0;
    for(const c of cells){
      const regionalWeather=clamp(1+shock+normal(r)*p.climateVolatility*.35,.16,1.55);
      const hEffect=clamp(1-p.hydraulicDependency*(1-c.infra)*.42,.46,1.12);
      const autonomyEffect=.93+.08*c.local;
      const stress=clamp((p.corveeDays-20)/250,0,.16);
      const tons=c.fields*100*p.yieldT*c.fertility*regionalWeather*hEffect*autonomyEffect*(1-stress*p.estateShare);
      fieldProduction+=Math.max(0,tons);
      maintenanceNeed+=c.fields*100*(.9+4*p.maintenanceIntensity*p.hydraulicDependency)*(1.18-c.local*.35);
      alignment+=c.loyalty*c.pop;
    }
    const usable=fieldProduction*(1-p.lossPct/100);
    const imports=p.importsT*(.4+.6*p.tradeIntegration)*clamp(.85+.1*normal(r),.3,1.3);
    const demand=prePop*p.riceKg/1000;
    const grainBalance=usable+imports-demand;
    const foodRatio=clamp((usable+imports)/Math.max(1,demand),0,2.2);
    const surplus=Math.max(0,grainBalance);
    // Seasonal work-time budget: overlap avoided by assigning bonded work before corvee.
    const adults=prePop*.45;
    const bonded=clamp(s.bonded,0,adults*.5);
    const fieldReserve=clamp(.33+(.17*(1+shock*-1)),.30,.61);
    const corveeDayPool=Math.max(0,adults-bonded)*p.corveeDays*clamp((1-fieldReserve)*(1+.3*p.localShare),.15,.85);
    const bondedDayPool=bonded*175*clamp((1-fieldReserve)*1.3,.20,.85);
    const laborPool=corveeDayPool+bondedDayPool;
    const maintLabor=Math.min(maintenanceNeed,laborPool*.36+maintenanceNeed*p.localShare*.17);
    const maintSatisfaction=clamp(maintLabor/Math.max(1,maintenanceNeed),0,1.4);
    for(const c of cells){
      const floodDamage=clamp(-shock*.038*(.5+p.hydraulicDependency),0,.075);
      c.infra=clamp(c.infra+(.006+.015*p.maintenanceIntensity)*maintSatisfaction-(.005+.016*p.hydraulicDependency*p.maintenanceIntensity)-floodDamage+(.006*c.local),.03,1);
    }
    const allocatable=surplus*clamp(.18+.51*p.estateShare+.17*p.tradeIntegration,.10,.73);
    const armyBudget=allocatable*p.warExpense;
    const monumentBudget=allocatable*p.buildShare;
    const maintainBudget=allocatable*Math.max(0,1-p.buildShare-p.warExpense);
    const soldiers=Math.min(prePop*.035,Math.floor(armyBudget/.12));
    const buildPersonDays=Math.max(0,Math.min(laborPool-maintLabor, monumentBudget*1000/.45));
    const ornamentalDays=buildPersonDays*p.monumentSkill*(.38+.4*s.courtLegitimacy);
    s.monument+=ornamentalDays;
    const corePower=(soldiers/2500)*(.45+.85*s.courtLegitimacy)+s.courtLegitimacy*7+clamp((surplus/16000),0,7);
    const rivalBase=9.5 + 5*Math.sin((year-842)/67)+.014*(year-850)+normal(r)*1.6;
    const rivalPower=Math.max(1,rivalBase*(.72+.48*p.raidIntensity));
    const loyaltyFrac=alignment/Math.max(1,prePop);
    let conflict=0,captives=0,casualties=0,defection=0;
    if(year>p.start+12){
      const contest=clamp((rivalPower-corePower)/30,-.6,.6);
      const warProb=clamp((.016+.055*p.raidIntensity+.045*contest)*(1-.38*p.diplomacy),.002,.20);
      if(r()<warProb){
        conflict=1;s.wars++;
        const chance=clamp(.29+.22*contest+.14*(1-loyaltyFrac)-.15*p.defenseSpend,.06,.72);
        const loss=r()<chance;
        if(loss){
          s.defeats++;casualties=prePop*(.0006+.002*r())*(.6+.7*p.conquestDamage);
          s.courtLegitimacy=clamp(s.courtLegitimacy-(.055+.075*r()),.05,1);
          defection=.02+.04*r();
          if(r()<.25+.35*p.conquestDamage){s.sacks++;s.shockYears.push(year); s.courtLegitimacy*=.83;}
        }else{
          s.victories++;captives=Math.round((300+850*r())*p.raidIntensity);
          s.courtLegitimacy=clamp(s.courtLegitimacy+.012+.017*r(),.05,1);
        }
      }
    }
    // Optional dated exogenous war stress, competing with endogenous raids.
    if(year===1177&&p.sackShock>0){const damage=p.sackShock;
      s.courtLegitimacy=clamp(s.courtLegitimacy-.27*damage,.05,1);s.sacks++;s.shockYears.push(year);
      casualties+=prePop*.013*damage;defection+=.09*damage;
      for(const c of cells){if(c.access>.74)c.infra=clamp(c.infra-.12*damage,.03,1);}
    }
    const growth=clamp(p.growthPct/100 + .013*(foodRatio-1)+normal(r)*.0017,-.065,.028);
    const targetGrowth=clamp(growth,-.06,.03);
    const emigrRate=clamp((1-s.courtLegitimacy)*.0019 + Math.max(0,1-foodRatio)*.024,.0,.045);
    const migration=Math.round((p.ritualMobilityPct/100)*adults*(.6+.4*s.courtLegitimacy));
    let factor=clamp(1+targetGrowth-emigrRate-casualties/Math.max(1,prePop),.87,1.045);
    // Redistribution between high opportunity and low opportunity cells (cohort ABM).
    let newTotal=0;
    for(const c of cells){
      const change=clamp((c.access-.62)*p.marketElasticity*.001 + (c.local-.5)*.001,-.002,.002);
      c.pop=Math.max(1,c.pop*factor*(1+change));newTotal+=c.pop;
      c.loyalty=clamp(c.loyalty+.012*(s.courtLegitimacy-.5)+.003*p.diplomacy-.018*defection+normal(r)*.009,.03,.98);
    }
    s.bonded=clamp((bonded+captives)*(1 + .008*p.bondedBirthPct-.01)-bonded*.007*(1-s.courtLegitimacy),0,newTotal*.23);
    const cropTax=surplus>0?clamp(allocatable/Math.max(1,surplus),0,1):0;
    s.courtLegitimacy=clamp(s.courtLegitimacy+.005*clamp(foodRatio-1,-1,1)+.007*cropTax+.002*Math.log1p(ornamentalDays/500000)-.0025*(1-loyaltyFrac)-.004*p.warExpense-.004*(!surplus?1:0),.035,1);
    s.shrine=clamp(s.shrine+.0025*p.templeAutonomy+.0014*(ornamentalDays/500000)-.002*(1-foodRatio>0?1-foodRatio:0)-.0022*(1-s.courtLegitimacy),.02,1);
    s.courtPower=corePower;s.rivalPower=rivalPower;
    s.latest={year,pop:newTotal,density:newTotal/p.regionKm2,corePop:newTotal*p.coreShare*(.68+.32*s.courtLegitimacy),grossRice:fieldProduction,usableRice:usable,imports,demand,surplus,grainBalance,foodRatio,maintenance:maintSatisfaction,infra:cells.reduce((a,c)=>a+c.infra,0)/cells.length,corveeDays:corveeDayPool,bondedDays:bondedDayPool,bonded:s.bonded,soldiers,buildDays:buildPersonDays,ornamentalIndex:Math.log10(1+s.monument/1000000),cumulativeMonumentDays:s.monument,loyalty:loyaltyFrac,legitimacy:s.courtLegitimacy,shrine:s.shrine,seasonalVisitors:migration,wars:s.wars,sacks:s.sacks,victories:s.victories,defeats:s.defeats,courtPower:corePower,rivalPower,fieldKm2:p.riceKm2};
    return s.latest;
  }
  function simulate(args, options={}){
    const p=Object.assign({},DEFAULTS,args||{});
    p.start=Math.round(p.start);p.end=Math.round(p.end);if(p.end<p.start) throw Error('End year precedes start year');
    const r=rng(p.seed);let cells=initialize(p,r);
    const state={cells,courtLegitimacy:.72,shrine:.49,bonded:p.bonded,monument:0,wars:0,sacks:0,victories:0,defeats:0,shockYears:[]};
    const timeline=[];const snapshots=[];const cadence=options.cadence||5;
    for(let year=p.start;year<=p.end;year++){
      const out=step(state,p,year,r);
      if((year-p.start)%cadence===0||year===p.end) timeline.push({...out});
      if((year-p.start)%50===0||year===p.end) snapshots.push({year,cells:cells.map(c=>({x:c.x,y:c.y,pop:c.pop,fields:c.fields,infra:c.infra,loyalty:c.loyalty}))});
    }
    return {params:p,timeline,final:{...state.latest},events:{wars:state.wars,sacks:state.sacks,victories:state.victories,defeats:state.defeats,shockYears:state.shockYears},snapshots};
  }
  function mc(base, options={}){
    const n=clamp(Math.floor(options.n||100),1,2000), seed=Math.floor(options.seed||1234);
    const control=Object.assign({},DEFAULTS,base);
    const treatment=Object.assign({},control,options.treatment||{});
    const rows=[];
    for(let i=0;i<n;i++){
      const ss=seed+i*37;
      const a=simulate({...control,seed:ss},{cadence:1000}).final;
      const b=simulate({...treatment,seed:ss},{cadence:1000}).final;
      rows.push({seed:ss,control:a,treatment:b,
        diffPop:b.pop-a.pop,diffMonument:b.ornamentalIndex-a.ornamentalIndex,diffSoldiers:b.soldiers-a.soldiers,diffSacks:b.sacks-a.sacks,diffDensity:b.density-a.density});
    }
    return {rows,n,control,treatment};
  }
  function quantile(a,q){const s=[...a].filter(Number.isFinite).sort((x,y)=>x-y);if(!s.length)return NaN;const p=(s.length-1)*q,lo=Math.floor(p),hi=Math.ceil(p);return s[lo]+(s[hi]-s[lo])*(p-lo);}
  function summarize(values){const a=values.filter(Number.isFinite),mean=a.reduce((x,y)=>x+y,0)/(a.length||1);return {n:a.length,mean,median:quantile(a,.5),q05:quantile(a,.05),q95:quantile(a,.95),min:Math.min(...a),max:Math.max(...a)};}
  // Ordinary least squares with centered predictors, partial-pivot Gaussian elimination, and conventional SE.
  // Useful for association diagnostics across simulated runs, NOT causal inference.
  function inverse(matrix){const n=matrix.length,m=matrix.map((row,i)=>[...row,...Array.from({length:n},(_,j)=>+(i===j))]);
    for(let i=0;i<n;i++){let im=i;for(let k=i+1;k<n;k++)if(Math.abs(m[k][i])>Math.abs(m[im][i]))im=k;
      if(Math.abs(m[im][i])<1e-9)return null;
      [m[im],m[i]]=[m[i],m[im]];const d=m[i][i];for(let j=0;j<2*n;j++)m[i][j]/=d;
      for(let k=0;k<n;k++)if(k!==i){const f=m[k][i];for(let j=0;j<2*n;j++)m[k][j]-=f*m[i][j];}
    }return m.map(row=>row.slice(n));
  }
  function regress(rows,dependent,independent){
    const clean=rows.filter(r=>Number.isFinite(r[dependent])&&independent.every(k=>Number.isFinite(r[k])));
    const n=clean.length,k=independent.length+1;if(n<=k+2)return {error:'Not enough observations for OLS'};
    const means=independent.map(name=>clean.reduce((a,row)=>a+row[name],0)/n);
    const std=independent.map((name,i)=>Math.sqrt(clean.reduce((a,row)=>a+(row[name]-means[i])**2,0)/n));
    if(std.some(x=>x<1e-12))return {error:'At least one predictor has no variation. Run a parameter sweep.'};
    const X=clean.map(row=>[1,...independent.map((key,i)=>(row[key]-means[i])/std[i])]);
    const Y=clean.map(row=>row[dependent]);
    const xx=Array.from({length:k},()=>Array(k).fill(0)),xy=Array(k).fill(0);
    for(let i=0;i<n;i++)for(let j=0;j<k;j++){xy[j]+=X[i][j]*Y[i];for(let h=0;h<k;h++)xx[j][h]+=X[i][j]*X[i][h];}
    const inv=inverse(xx);if(!inv)return {error:'Singular design matrix'};
    const beta=inv.map(row=>row.reduce((a,v,j)=>a+v*xy[j],0));const fitted=X.map(row=>row.reduce((a,v,j)=>a+v*beta[j],0));
    const ym=Y.reduce((a,b)=>a+b,0)/n,sse=Y.reduce((a,v,i)=>a+(v-fitted[i])**2,0),sst=Y.reduce((a,v)=>a+(v-ym)**2,0);
    const s2=sse/(n-k);const se=beta.map((_,i)=>Math.sqrt(Math.max(0,s2*inv[i][i])));
    return {n,dependent,predictors:['Intercept',...independent],beta,se,r2:sst>0?1-sse/sst:NaN,adjR2:sst>0?1-(1-sse/sst)*(n-1)/(n-k):NaN,scale:'All predictor coefficients standardized per one standard deviation; outcome remains in original units.',warning:'Exploratory OLS on synthetic data. Relationships are associations; shocks, feedback and endogenous institutions prevent causal interpretation.'};
  }
  function sweep(base, options={}){
    const n=clamp(Math.floor(options.n||180),20,1500),r=rng(options.seed||9951),keys=options.keys||['yieldT','estateShare','raidIntensity','hydraulicDependency','tradeIntegration'];
    const rows=[];
    const bounds={yieldT:[1.1,2.5],estateShare:[.05,.82],raidIntensity:[.08,.94],hydraulicDependency:[.12,.89],tradeIntegration:[.08,.91],corveeDays:[4,80],importsT:[0,35000],diplomacy:[.10,.9]};
    for(let i=0;i<n;i++){
      const p={...DEFAULTS,...base,seed:10000+i*101};
      for(const key of keys){const [lo,hi]=bounds[key]||[0,1];p[key]=lo+(hi-lo)*r();}
      const result=simulate(p,{cadence:1000}).final;
      const row={run:i,...Object.fromEntries(keys.map(key=>[key,p[key]])),pop:result.pop,density:result.density,monument:result.ornamentalIndex,soldiers:result.soldiers,sacks:result.sacks,surplus:result.surplus,infra:result.infra};
      rows.push(row);
    }
    const predictors=keys.slice(0,Math.min(5,keys.length));
    return {rows,regressions:{population:regress(rows,'pop',predictors),monuments:regress(rows,'monument',predictors),conflicts:regress(rows,'sacks',predictors)},keys};
  }
  return {DEFAULTS,PRESETS,periods,GRID_W,GRID_H,simulate,mc,sweep,regress,summarize,quantile};
});
