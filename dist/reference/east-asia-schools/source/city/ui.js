(function(){
  "use strict";
  const C=window.HKModel, N=window.HKNetwork, G=window.Guangzhou;
  const e=id=>document.getElementById(id);
  const d=JSON.parse(e("input").textContent);
  const bands=["#195b4a","#a25a34","#657581"];
  const num=new Intl.NumberFormat("en");
  const f=x=>x==null?"–":num.format(x);
  const decimal=x=>x==null?"–":x.toFixed(1);
  const pct=x=>(x*100).toFixed(1)+"%";
  const signed=x=>x==null?"–":(x>0?"+":"")+f(x);
  const sy=y=>y+"/"+String(y+1).slice(-2);
  const esc=x=>String(x).replace(/[<>&"']/g,c=>({"<":"&lt;",">":"&gt;","&":"&amp;",'"':"&quot;","'":"&#39;"})[c]);
  const rows=(head,body)=>"<thead><tr>"+head.map(x=>"<th scope='col'>"+x+"</th>").join("")+"</tr></thead><tbody>"
    +body.map(r=>"<tr><th scope='row'>"+r[0]+"</th>"+r.slice(1).map(x=>"<td>"+x+"</td>").join("")+"</tr>").join("")+"</tbody>";
  const scope={
    enrollment:["Enrollment","Pupils enrolled",f],entry:["Entry intake","Pupils entering the first grade",f],
    sites:["School count","School operations by stage",f],staff:["Teachers employed","Teacher headcount or modeled positions",f],
    required:["Required posts","Modeled demand for teaching posts",f],hires:["Annual hires","Replacement and expansion hires needed",f],
    departures:["Normal departures","Departures at the selected rate",f],
    cutsFrom2025:["Teachers below 2025/26","Employment below 2025/26; a negative value means growth",signed],
    involuntary:["Forced cuts","Separations beyond normal departures",f],
    classSize:["Average class size","Pupils per operating class",decimal],
  };
  let city="hk", result, playTimer=null, playing=false, paused=false;
  const hkTests=N.testHistory(d.hk);
  const gzTests=G.backtest(d.gz);
  const district=N.districtApprovals(d.profiles,d.hk.districts);
  const tabs=[...document.querySelectorAll("[data-city]")];

  const choice=(select, items, initial)=>{
    select.replaceChildren();
    for(const [value,label] of items){
      const selected=String(value)===String(initial);
      select.add(new Option(label,String(value),selected,selected));
    }
  };
  function reset(){
    stopPlayback();
    for(const [key,value] of Object.entries(N.DEFAULTS)) e(key).value=key==="births"?100:["savedSites"].includes(key)?value:100*value;
    for(const [key,value] of Object.entries(G.DEFAULTS)) e(key).value=100*value;
    recompute();
  }
  function setCity(next){
    city=next;
    const hk=city==="hk";
    for(const t of tabs) t.setAttribute("aria-pressed",String(t.dataset.city===city));
    e("hkControls").hidden=e("hkEvidence").hidden=e("hkSources").hidden=!hk;
    e("gzControls").hidden=e("gzEvidence").hidden=hk;
    const stages=hk?N.stages:d.gz.stages;
    choice(e("stage"),stages.map((v,i)=>[i,v]),hk?1:2);
    const end=hk?N.END:G.END;
    choice(e("year"),Array.from({length:end-2025},(_,i)=>[i+2026,sy(i+2026)]),end);
    updateMetrics("sites");
    recompute();
  }
  function updateMetrics(initial){
    const hk=city==="hk", stage=+e("stage").value;
    const keys=hk?Object.keys(scope).filter(k=>stage||k!=="classSize"):["sites","staff","enrollment",...(stage?["entry"]:[])];
    choice(e("metric"),keys.map(k=>[k,scope[k][0]]),keys.includes(initial)?initial:"sites");
  }
  function recompute(){
    const settingsHK={savedSites:+e("savedSites").value,births:Math.round(31100*+e("births").value/100),birthGrowth:+e("birthGrowth").value/100,exitScale:+e("exitScale").value/100,demandShift:+e("demandShift").value/100};
    const settingsGZ={kgGrowth:+e("kgGrowth").value/100,longKgGrowth:+e("longKgGrowth").value/100,primaryDemand:+e("primaryDemand").value/100};
    for(const [id,v] of Object.entries({savedValue:f(settingsHK.savedSites),exitValue:pct(settingsHK.exitScale),
      demandValue:pct(settingsHK.demandShift),birthsValue:`${e("births").value} · ${f(settingsHK.births)} births`,birthGrowthValue:pct(settingsHK.birthGrowth),kgValue:pct(settingsGZ.kgGrowth),longKgValue:pct(settingsGZ.longKgGrowth),primaryValue:pct(settingsGZ.primaryDemand)}))e(id).textContent=v;
    result=city==="hk"?N.run(d.hk,d.approvals,d.plans,settingsHK):G.simulate(d.gz,settingsGZ);
    render();
  }
  function pathChart(cases,records,s,key,focus,end){
    const vals=cases.map(p=>Object.keys(records[p.key]).map(y=>[+y,records[p.key][y][s][key]]).filter(([yr,v])=>Number.isFinite(v)&&(!(playing||paused)||yr<=focus)));
    const points=vals.flat().map(p=>p[1]);
    const min=Math.min(...points),max=Math.max(...points);
    const span=Math.max(1,max-min,max*0.1);
    const lo=min-span*0.13,hi=max+span*0.16;
    const x=y=>64+(y-2025)/(end-2025)*674;
    const y=v=>18+(hi-v)/(hi-lo)*170;
    const ticks=Array.from({length:5},(_,i)=>lo+(hi-lo)*i/4);
    const years=Array.from({length:(end-2025)/5+1},(_,i)=>2025+i*5);
    const boundary=city==="hk"?2035:2031;
    const label=city==="hk"?"After EDB inputs":"Long-run settings";
    const axis=v=>Math.abs(v)>=1000?(v/1000).toFixed(Math.abs(v)>=10000?0:1)+"k":f(Math.round(v));
    e("chart").innerHTML=`<svg viewBox="0 0 765 216" role="img" aria-label="${scope[key][0]} by year under three policies">
      <rect x="${x(boundary)}" y="18" width="${x(end)-x(boundary)}" height="170" fill="#eef3e8"/>
      <text x="${x(boundary)+5}" y="13">${label}</text>
      ${ticks.map(v=>`<line x1="64" x2="738" y1="${y(v)}" y2="${y(v)}"/><text x="56" y="${y(v)+4}" text-anchor="end">${axis(v)}</text>`).join("")}
      <line class="focus" x1="${x(focus)}" x2="${x(focus)}" y1="18" y2="188"/>
      ${years.map(v=>`<text x="${x(v)}" y="209" text-anchor="middle">${v}</text>`).join("")}
      ${vals.map((line,i)=>`<polyline points="${line.map(([yr,v])=>x(yr)+","+y(v)).join(" ")}" fill="none" stroke="${bands[i]}" stroke-width="${i?2.5:3.2}" ${i?'stroke-dasharray="'+(i===1?"7 3":"2 3")+'"':""}/>`).join("")}
      </svg>`;
    e("legend").innerHTML=cases.map((p,i)=>`<span><i style="border-color:${bands[i]};border-top-style:${i?"dashed":"solid"}"></i>${p.label}</span>`).join("");
  }
  function render(){
    const hk=city==="hk", s=+e("stage").value, year=+e("year").value, key=e("metric").value;
    const policies=hk?N.CASES:G.POLICIES;
    const all=hk?result.records:result;
    const selected=policies.map(p=>all[p.key][year][s]);
    const stages=hk?N.stages:d.gz.stages;
    const base=all[policies[0].key][2025][s];
    e("projectionTitle").textContent=stages[s]+" in "+sy(year);
    e("forecastScope").textContent=scope[key][1]+". "+(hk
      ?"2025/26 is observed. EDB’s territory-wide age-six and age-twelve projections run through 2035. From 2036, cohort progression and the selected level and annual change in births drive demand."
      :"2025 is observed. All future counts are citywide scenarios. The long-run preschool assumption takes effect from 2032.");
    e("controlNote").textContent=hk
      ?"Faster consolidation permits forced separations if departures leave more staff than required. Selective retention adds classes within an assumed room limit."
      :"Guangzhou scenarios compare a recent-response rule with holding 2025 sites and staff and with faster adjustment.";
    const items=[["Enrollment","enrollment",f],...(s||hk?[["Entry intake","entry",f]]:[]),["School operations","sites",f],
      ["Change in schools since 2025","sites",x=>signed(x-base.sites)],["Teachers","staff",f],
      ["Change in teachers since 2025","staff",x=>signed(x-base.staff)]];
    if(hk)items.push(["Net teacher change this year","netTeacherChange",signed],["Normal departures","departures",f],
      ["Hires required","hires",f],["Forced separations","involuntary",f]);
    if(hk&&s)items.push(["Operating classes","classes",f],["Pupils per class","classSize",decimal]);
    e("comparison").innerHTML=rows(["Measure","Observed 2025",...policies.map(p=>p.label)],
      items.map(([title,k,fn])=>[title,fn(base[k]),...selected.map(v=>fn(v[k]))]));
    pathChart(policies,all,s,key,year,hk?N.END:G.END);
    e("playbackStatus").textContent=playing?`Playing completed run · ${sy(year)}`:paused?`Paused · ${sy(year)}`:`Completed run ready · inspecting ${sy(year)}`;
    showTests(hk,s);
    if(hk)e("districts").innerHTML=rows(["District","Public profiles","2025/26 P1","2026/27 approved P1","Newly zero P1",sy(year)+" modeled P1"],
      district.map((x,i)=>[esc(x.name),f(x.schools),f(x.previous),f(x.approved),f(x.zero),f(result.district[year][1][i][0])]));
    e("methods").textContent=hk
      ?"The reference ages pupils through grades and carries the observed primary approval adjustment through the affected cohorts. The secondary calculation approximates the 27-to-29 approval basis by cohort. After 2035, the age-six path eases from the last official figure toward the selected path for births. The secondary path follows those cohorts six years later. The staffing model uses 1.6 regular posts per primary class and 1.8 or 2.1 per junior or senior secondary class, with the difference to the 2025 all-sector headcount calibrated separately. Unspecified school exits and classroom capacity are assumptions. Net school operations can fall after mergers, even if buildings remain in use."
      :"Historical entry counts reconstruct the grade pipeline. Preschool demand informs P1, the primary leaving cohort informs junior entry, and the junior leaving cohort informs senior high. All three scenarios use the same pupil counts. The reference scales school counts and full-time teacher demand with enrollment. Guangzhou has no borrowed Hong Kong admission, payroll, departure or merger rules.";
  }
  function showTests(hk,s){
    const hit=(a,k)=>a.filter(x=>x.stage===s&&x.metric===k);
    const scores=hk?[
      ["Enrollment",hit(hkTests.historical,"pupils"),false],
      ["Intake",hit(hkTests.historical,"entry"),false],
      ["Net school-count change",hit(hkTests.historical,"siteChange"),true],
      ["Workforce under staffing rule",hit(hkTests.workforceRows,"network_staff"),false],
    ]:[
      ["Enrollment",hit(gzTests,"pupils"),false],
      ["Intake",hit(gzTests,"entry"),false],
      ["School count",hit(gzTests,"sites"),false],
      ["Teacher count",hit(gzTests,"staff"),false],
    ];
    e("testDescription").textContent=hk
      ?"Rolling one-year forecasts, 2020/21–2025/26. Workforce scoring starts in 2021/22. Historic school counts test the pre-2026 model; the new approval and merger rules have only a partial public record."
      :"Rolling one-year forecasts for 2023–2025. Results for each stage are shown next to a last-year benchmark. Small errors on total school counts can still hide poorly predicted openings and closures.";
    e("tests").innerHTML=rows(["Outcome","N","Model error","Benchmark error"],scores.filter(x=>x[1].length).map(([label,x,mae])=>{
      const m=C.metrics(x);
      return [label+(mae?" · schools MAE":" · WAPE"),f(m.n),mae?decimal(m.mae):pct(m.wape),mae?decimal(m.naiveMae):pct(m.naiveWape)];
    }));
  }
  function stopPlayback(){
    if(playTimer)clearInterval(playTimer);
    playTimer=null;playing=false;paused=false;e("play").textContent="Replay run";
  }
  function pausePlayback(){
    if(playTimer)clearInterval(playTimer);playTimer=null;playing=false;paused=true;e("play").textContent="Resume";
  }
  function startPlayback(){
    const resume=paused;stopPlayback();playing=true;if(!resume)e("year").value="2026";e("play").textContent="Pause";render();
    playTimer=setInterval(()=>{
      const end=city==="hk"?N.END:G.END,next=+e("year").value+1;
      if(next>end){stopPlayback();render();return;}
      e("year").value=next;render();
    },150);
  }
  function csv(){
    const hk=city==="hk", all=hk?result.records:result;
    const dataset=[];
    const keys=["entry","enrollment","sites","staff","classes","classSize","required","departures","hires","netTeacherChange","cutsFrom2025","involuntary","planned"];
    const cases=hk?N.CASES:G.POLICIES;
    for(const p of cases)for(const [year,stages] of Object.entries(all[p.key])){
      stages.forEach((v,i)=>dataset.push([year,(hk?N.stages:d.gz.stages)[i],p.label,...keys.map(k=>v[k])]));
    }
    const quote=x=>'"'+String(x??"").replaceAll('"','""')+'"';
    const blob=new Blob([[["year","stage","policy",...keys],...dataset].map(r=>r.map(quote).join(",")).join("\r\n")],{type:"text/csv;charset=utf-8"});
    const url=URL.createObjectURL(blob), a=document.createElement("a");
    a.href=url;a.download=(hk?"Hong_Kong":"Guangzhou")+"_Network_Scenarios.csv";a.click();
    setTimeout(()=>URL.revokeObjectURL(url),1000);
  }
  e("schoolPlans").innerHTML=rows(["School","Plan","Merger partner","Timing used in model"],d.plans.schools.map(r=>[
    esc(r[0]),esc(r[1]),esc(r[2]||"–"),esc(r[3])+(r[5]?' <a href="'+esc(r[5])+'">Source</a>':""),
  ]));
  e("gzSources").innerHTML=d.gz.history.map(r=>'<a href="'+esc(r[2])+'">'+r[0]+' bulletin</a>').join(" · ")
    +' · <a href="'+esc(d.gz.officialPlan.url)+'">2026 work plan</a>'
    +' · <a href="https://www.cse.edu.cn/index/detail.html?category=179&amp;id=4485">Published enrollment peak years</a>';
  for(const t of tabs)t.addEventListener("click",()=>{stopPlayback();setCity(t.dataset.city);});
  for(const id of [...Object.keys(N.DEFAULTS),...Object.keys(G.DEFAULTS)])e(id).addEventListener("input",()=>{stopPlayback();recompute();});
  e("reset").addEventListener("click",reset);
  e("play").addEventListener("click",()=>playing?(pausePlayback(),render()):startPlayback());
  document.addEventListener("visibilitychange",()=>{if(document.hidden&&playing){pausePlayback();render();}});
  e("metric").addEventListener("change",()=>{stopPlayback();render();});
  e("year").addEventListener("change",()=>{if(playing||paused)pausePlayback();else stopPlayback();render();});
  e("stage").addEventListener("change",()=>{stopPlayback();updateMetrics(e("metric").value);render();});
  e("download").addEventListener("click",csv);
  setCity("hk");
  if(!window.matchMedia("(prefers-reduced-motion: reduce)").matches)startPlayback();
})();
