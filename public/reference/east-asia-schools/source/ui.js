(function () {
  "use strict";
  const $ = id => document.getElementById(id);
  const fmt = new Intl.NumberFormat("en");
  const display = (value, digits = 0) => value == null ? "—" :
    digits ? value.toLocaleString("en", {maximumFractionDigits:digits}) : fmt.format(value);
  const options = (obj, label) => Object.keys(obj).map(key => `<option value="${key}">${label(obj[key],key)}</option>`).join("");
  const number = (id, factor = 1) => {
    const field = $(id);
    if (field.value === "") return null;
    const parsed = Number(field.value);
    return Number.isFinite(parsed) ? Math.max(Number(field.min), Math.min(Number(field.max), parsed)) / factor : null;
  };
  const whole = id => {
    const value = number(id);
    return value == null ? null : Math.round(value);
  };
  const controls = ["override","lag","qualify","seek","firstShare","exits","secondaryExits","force","cost","births","policy","year","metric"];
  const table = [
    ["year","Year"], ["enrollment","Enrollment"], ["sites","School operations"], ["required","Staffing target"],
    ["employed","Employed teachers"], ["demographicTarget","Enrollment-based target"], ["departures","Departures"], ["openings","All openings"], ["excess","Incumbents above target"],
    ["layoffs","Modeled layoffs"], ["starts","Training intake"], ["feederIntake","Feeder intake"], ["qualified","Newly qualified"],
    ["applicants","New applicants"], ["firstOpenings","Entry openings"], ["unmatched","Applicant gap"],
    ["planLow","Published recruitment low"], ["planHigh","Published recruitment high"], ["planFloor","Reference recruitment floor"],
    ["historicalEntrants","Observed first-time entrants"], ["historicalRecruitment","Reported public recruitment"],
    ["age","Age-band population"], ["classSize","Pupils per class"], ["pupilTeacherRatio","Pupils per teacher"], ["payroll","Teacher payroll"]
  ];
  const series = {
    pipeline:[["applicants","New applicants"],["firstOpenings","Entry openings"],["openings","All openings"],["planLow","Published recruitment low"],["planHigh","Published recruitment high"],
      ["historicalEntrants","Observed first-time entrants"],["historicalRecruitment","Reported public recruitment"]],
    workforce:[["employed","Employed teachers"], ["demographicTarget","Enrollment-based target"],["required","Staffing target"]],
    cuts:[["excess","Incumbents above target"],["layoffs","Modeled layoffs"]],
    enrollment:[["enrollment","Enrollment"],["age","Age-band population"]],
    sites:[["sites","School operations"]]
  };
  const chartNames = {pipeline:"Applicants and openings",workforce:"Teachers and staffing target",
    cuts:"Excess posts and layoffs",enrollment:"School demand",sites:"School operations"};
  const colors = ["#075e5b","#9e411d","#68538e","#4a6981","#8c6210","#336b3f","#604456"];
  let results = [];
  let activeColumns = [];
  let activeConfig = {};
  let playTimer = null;
  let playing = false;
  let paused = false;
  const $system = $("system");
  const $stage = $("stage");
  $system.innerHTML = options(DATA.systems, (_, key) => key);
  $system.value = "Hong Kong";
  $("cohortBirth").innerHTML = Array.from({length:19},(_,i)=>2026+i).map(year=>`<option value="${year}"${year===2027?" selected":""}>${year}</option>`).join("");
  const getSystem = () => DATA.systems[$system.value];
  const getStage = () => getSystem().stages[$stage.value];

  function stages() {
    const prior = $stage.value;
    const all = getSystem().stages;
    $stage.innerHTML = options(all, stage => stage.name);
    $stage.value = Object.hasOwn(all, prior) ? prior : $system.value === "Hong Kong" ? "ps" : "p";
    const slider = $("births");
    const hk = getSystem().family === "hk";
    slider.min = getSystem().family === "gz" ? -6 : hk ? 50 : -50;
    slider.max = getSystem().family === "gz" ? 4 : hk ? 150 : 50;
    slider.value = hk ? 100 : 0;
    reset();
  }

  function reset() {
    const stage = getStage(), system = getSystem();
    $("override").value = stage.training?.future ?? "";
    $("override").placeholder = stage.training ? "Scenario intake" : "No matched series";
    $("lag").value = stage.lag ?? 4;
    $("firstShare").value = Math.round(100 * (stage.firstShare ?? 0.5));
    const hkExits = {k:14.9,p:6.5,s:6.7,ps:6.5};
    $("exits").value = system.family === "hk" ? hkExits[$stage.value] : 4;
    $("secondaryExits").value = 6.7;
    $("cost").value = 0;
    $("metric").value = stage.history || stage.city ? "pipeline" : "enrollment";
    render();
    renderCohort();
  }

  function draw(rows, metric, year) {
    const data = series[metric].map(([key, label], i) => ({
      key, label, color:colors[i], values:rows.filter(row => row[key] != null)
    })).filter(item => item.values.length);
    $("chartTitle").textContent = chartNames[metric];
    if (!data.length) {
      $("chart").textContent = "No series is available for this measure and stage.";
      $("legend").innerHTML = "";
      return;
    }
    const W = 960, H = 263, left = 76, right = 21, top = 17, bottom = 34;
    const plotWidth = W - left - right, plotHeight = H - top - bottom;
    const max = Math.max(1, ...data.flatMap(item => item.values.map(row => row[item.key])));
    const scaled = max / 4;
    const power = 10 ** Math.floor(Math.log10(scaled));
    const unit = [1,2,2.5,5,10].find(n => n * power >= scaled) * power;
    const ceiling = 4 * unit;
    const x = y => left + (y - Pipeline.BASE) * plotWidth / (Pipeline.END - Pipeline.BASE);
    const y = v => top + (1 - v / ceiling) * plotHeight;
    const guide = [0,1,2,3,4].map(i => {
      const value = i * unit, pos = y(value);
      return `<line x1="${left}" y1="${pos}" x2="${W-right}" y2="${pos}" stroke="#d8dfd5"/><text x="${left-9}" y="${pos+4}" text-anchor="end">${display(value,2)}</text>`;
    }).join("");
    const axis = [2025,2030,2035,2040,2045,2050].map(v => `<text x="${x(v)}" y="${H-8}" text-anchor="middle">${v}</text>`).join("");
    const lines = data.map(item => {
      const points = item.values.map(row => `${x(row.year)},${y(row[item.key])}`).join(" ");
      const focus = item.values.length === 1 ? item.values[0] : item.values.find(row => row.year === year);
      return `<polyline points="${points}" fill="none" stroke="${item.color}" stroke-width="3" vector-effect="non-scaling-stroke"/>` +
        (focus ? `<circle cx="${x(focus.year)}" cy="${y(focus[item.key])}" r="4" fill="${item.color}"><title>${item.label} · ${display(focus[item.key])}</title></circle>` : "");
    }).join("");
    $("chart").innerHTML = `<svg class="chart" viewBox="0 0 ${W} ${H}" role="img" aria-label="${chartNames[metric]} from 2025 through 2050">${guide}${axis}<text x="${left}" y="10">Observed 2025</text><text x="${W-right}" y="10" text-anchor="end">Modeled years</text><line x1="${x(year)}" x2="${x(year)}" y1="${top}" y2="${H-bottom}" stroke="#7a8884" stroke-dasharray="4 5"/>${lines}</svg>`;
    $("legend").innerHTML = data.map(item => `<span><i style="background:${item.color}"></i>${item.label}</span>`).join("");
  }

  function renderCohort() {
    const birth = Number($("cohortBirth").value), stages = getSystem().stages;
    const keys = getSystem().family === "hk" ? ["k","p","s"] : getSystem().family === "gz" ? ["k","p","j"] : ["k","p","j"];
    const milestones = [["Kindergarten",3],["Primary",6],["Lower secondary",12]];
    $("cohortSteps").innerHTML = "";
    milestones.forEach(([label,offset],i) => {
      const key = keys[i], year = birth + offset, button = document.createElement("button");
      button.className = "primary";
      button.textContent = `${label} · ${year}`;
      button.disabled = !stages[key] || year > 2050;
      button.addEventListener("click", () => {
        stopPlayback();
        $stage.value = key;
        reset();
        $("year").value = year;
        render();
      });
      $("cohortSteps").appendChild(button);
    });
  }

  function render() {
    const system = getSystem(), stage = getStage();
    const staffed = !!(stage.history || stage.city);
    $("unanchored").hidden = !stage.hiring;
    if (!stage.hiring && $("policy").value === "enrollment") $("policy").value = "reference";
    ["exits","secondaryExits","force","cost","lag","qualify","seek","firstShare"].forEach(id => $(id).disabled = !staffed);
    $("override").disabled = !staffed || !stage.training;
    $("secondaryExitsField").hidden = !(system.family === "hk" && $stage.value === "ps");
    $("exitsLabel").textContent = system.family === "hk" && $stage.value === "ps" ? "Primary annual exits (%)" : "Annual exits (%)";
    const births = number("births");
    const signed = births > 0 ? "+" + births : String(births);
    $("birthLabel").textContent = system.family === "gz" ? "Long-run preschool demand" : system.family === "hk" ? "Births index (observed 2025 = 100)" : "Future births vs. UN medium";
    $("birthOut").textContent = system.family === "hk" ? `${births} · ${display(31100 * births/100)} births` : `${signed}%`;
    $("birthNote").textContent = system.family === "hk" ?
      "100 means 31,100 annual births, the observed 2025 level. The index applies after the near-term EDB anchors; it is not a TFR." :
      system.family === "gz" ? "Annual growth in preschool enrollment after the city model transitions to its long-run path. Participation and migration also affect this measure." :
      "Relative to UN medium births, starting with cohorts born in 2027. Those cohorts reach preschool ages in 2030, primary in 2033 and lower secondary in 2039.";
    $("staffNote").textContent = !staffed ? "This view shows age-band population." : system.family === "hk" ?
      "Exit inputs are prefilled from 2025/26 EDB stage rates: 14.9% kindergarten, 6.5% primary and 6.7% secondary. The combined view keeps separate editable primary and secondary rates. Cost starts at 0 because no common salary estimate is assumed." :
      "The 4% exit rate and 50% share of openings available to first-time applicants are illustrative defaults. Cost starts at 0 because no common salary estimate is assumed. Both are editable.";
    $("hiringNote").textContent = stage.hiring ?
      "The Korean reference reserves at least the published public recruitment count for entrants in 2026–27, and the midpoint of the planned ranges in 2028–30. The floor then fades out by 2034 as a scenario assumption. Choose Enrollment-only reference to remove it. Other policies also run without the floor." : "";
    $("trainingNote").textContent = stage.training?.label ?? (staffed ?
      "Enter annual training intake to test candidate supply. A stage-matched series is unavailable in this build." :
      "Training and staffing are available for stages with a matched employment series.");
    const year = number("year");
    $("yearOut").textContent = year;
    activeConfig = {policy:$("policy").value, births:system.family === "hk" ? births / 100 - 1 : births / 100, exits:number("exits",100), secondaryExits:number("secondaryExits",100),
      firstShare:number("firstShare",100), override:whole("override"), lag:whole("lag"),
      qualify:number("qualify",100) ?? 0.85, seek:number("seek",100) ?? 0.8, force:$("force").checked, cost:number("cost") || null};
    results = Pipeline.simulate(DATA, $system.value, $stage.value, activeConfig);
    const selected = results.find(row => row.year === year);
    const first = key => {
      const row = results.find(row => row[key] > 0);
      return row ? String(row.year) : results.some(row => row[key] != null) ? "None through 2050" : "Unavailable";
    };
    const cards = staffed ? [
      ["Teachers employed in " + year, display(selected.employed)],["Entry openings in " + year,display(selected.firstOpenings)],
      ["New applicants in " + year,display(selected.applicants)],
      ["Applicant gap in " + year,display(selected.unmatched)],
      [stage.training?.partial && activeConfig.override == null ? "First gap for the PGDE route" : "First applicant gap",first("unmatched")],
      ["First year above staffing target",first("excess")],
      ["First modeled layoffs",activeConfig.force ? first("layoffs") : "Cuts off"]
    ] : [["Age-band population in " + year,display(selected.age)]];
    $("stats").innerHTML = cards.map(([label,value]) => `<div class="stat"><span>${label}</span><strong>${value}</strong></div>`).join("");
    activeColumns = table.filter(([key]) => results.some(row => row[key] != null));
    $("thead").innerHTML = "<tr>" + activeColumns.map(([,label]) => `<th scope="col">${label}</th>`).join("") + "</tr>";
    $("rows").innerHTML = results.map(row => `<tr${row.year === year ? ' class="selected"' : ""}>` +
      activeColumns.map(([key]) => `<td>${key === "year" ? row.year : display(row[key],key === "classSize" || key === "pupilTeacherRatio" ? 1 : 0)}</td>`).join("") + "</tr>").join("");
    draw(playing || paused ? results.filter(row => row.year <= year) : results, $("metric").value, year);
    $("playbackStatus").textContent = playing ? `Playing completed run · ${year} / 2050` : paused ? `Paused · ${year} / 2050` : `Completed run ready · inspecting ${year}`;
    $("evidence").textContent = system.note;
    $("sources").innerHTML = [["source","School and workforce source"],["trainingSource","Training source"],["enrollmentSource","Enrollment source"],["hiringSource","Recruitment source"],["recruitmentSource","2026 and 2027 recruitment counts"]]
      .filter(([key]) => system[key]).map(([key,label]) => `<a href="${system[key]}">${label}</a>`).join("");
    const check = Pipeline.historicalCheck(DATA, $system.value, $stage.value);
    const error = key => 100 * check.reduce((n,row) => n+Math.abs(row[key]-row.actual),0) / check.reduce((n,row) => n+row.actual,0);
    $("backtest").textContent = check.length ?
      `Retrospective one-year enrollment check (${check.length} ${check.length === 1 ? "year" : "years"}). Age-based scaling had ${display(error("expected"),1)}% weighted error, compared with ${display(error("flat"),1)}% holding enrollment flat. The UN age series is from a single release, including projections for 2024 onward.` :
      system.family ? "See network detail for the city’s historical enrollment and staffing checks." : "";
  }

  function stopPlayback() {
    if (playTimer) clearInterval(playTimer);
    playTimer = null;
    playing = false;
    paused = false;
    $("play").textContent = "Replay run";
  }
  function pausePlayback() {
    if (playTimer) clearInterval(playTimer);
    playTimer = null;
    playing = false;
    paused = true;
    $("play").textContent = "Resume";
  }
  function startPlayback() {
    const resume = paused;
    stopPlayback();
    playing = true;
    if (!resume) $("year").value = 2026;
    paused = false;
    $("play").textContent = "Pause";
    render();
    playTimer = setInterval(() => {
      const next = Number($("year").value) + 1;
      if (next > 2050) { stopPlayback(); render(); return; }
      $("year").value = next;
      render();
    }, 150);
  }
  $("play").addEventListener("click", () => playing ? (pausePlayback(), render()) : startPlayback());
  document.addEventListener("visibilitychange", () => { if (document.hidden && playing) { pausePlayback(); render(); } });

  $("download").addEventListener("click", () => {
    const keys = table.map(([key]) => key);
    const lines = [["system","stage",...Object.keys(activeConfig),...keys].join(","),
      ...results.map(row => [$system.value,$stage.value,...Object.values(activeConfig),...keys.map(key => row[key])].join(","))];
    const url = URL.createObjectURL(new Blob([lines.join("\n")+"\n"],{type:"text/csv;charset=utf-8"}));
    const link = document.createElement("a");
    link.href = url;
    link.download = `${$system.value.toLowerCase().replaceAll(" ","-")}-${$stage.value}-2050.csv`;
    link.click();
    setTimeout(() => URL.revokeObjectURL(url),1000);
  });
  $system.addEventListener("change",stages);
  $stage.addEventListener("change",reset);
  $("cohortBirth").addEventListener("change",renderCohort);
  controls.forEach(id => $(id).addEventListener("input", () => {
    if (id === "year" && (playing || paused)) { pausePlayback(); render(); }
    else { stopPlayback(); render(); }
  }));
  stages();
  if (!window.matchMedia("(prefers-reduced-motion: reduce)").matches) startPlayback();
  else render();
})();
