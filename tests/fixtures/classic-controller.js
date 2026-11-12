'use strict';
(() => {
  const {worlds, sha256} = AtlasWorldsLab;
  const $ = id => document.getElementById(id);
  const states = new Map();
  const colors = {live: '#126550', reference: '#596b63', observed: '#91451f', alternate: '#91451f'};
  const esc = value => String(value).replace(/[&<>"']/g, char => ({'&':'&amp;', '<':'&lt;', '>':'&gt;', '"':'&quot;', "'":'&#39;'}[char]));
  let world, values, baseline, baselineKey, lastRun, pending;

  function makeChart({heading, lines, axis, band, breaks = []}) {
    const points = lines.flatMap(s => s.points).filter(p => Number.isFinite(p[1]));
    const observations = points.map(p => p[1]).concat(band ? band.points.flatMap(([, lo,, hi]) => [lo, hi]) : []);
    const xmin = Math.floor(Math.min(...points.map(p => p[0])));
    const xmax = Math.max(...points.map(p => p[0]));
    const min = Math.min(...observations), max = Math.max(...observations);
    const padding = (max - min) * .09 || 1;
    const lo = Math.max(min >= 0 ? 0 : -Infinity, min - padding), hi = max + padding;
    const left = 58, right = 700, top = 16, bottom = 229;
    const x = t => left + (t - xmin) / (xmax - xmin) * (right - left);
    const y = v => bottom - (v - lo) / (hi - lo) * (bottom - top);
    const coords = (t, v) => x(t).toFixed(2) + ' ' + y(v).toFixed(2);
    const yTicks = Array.from({length: 5}, (_, i) => lo + (hi - lo) * i / 4);
    const xTicks = Array.from({length: 5}, (_, i) => Math.round(xmin + (xmax - xmin) * i / 4))
      .filter(t => t <= xmax);
    let svg = '<svg class="chart" viewBox="0 0 720 262" role="img" aria-label="' + esc(heading) + '">';
    for (const v of yTicks) svg += '<line class="grid" x1="' + left + '" x2="' + right + '" y1="' + y(v) + '" y2="' + y(v) + '"/><text x="49" y="' + (y(v) + 4) + '" text-anchor="end">' + esc(axis(v)) + '</text>';
    for (const t of xTicks) svg += '<text x="' + x(t) + '" y="251" text-anchor="middle">' + t + '</text>';
    for (const t of breaks) svg += '<line x1="' + x(t) + '" x2="' + x(t) + '" y1="' + top + '" y2="' + bottom + '" stroke="#a4775e" stroke-dasharray="3 4"/>';
    if (band) {
      const upper = band.points.map(([t,,, v]) => coords(t, v));
      const lower = [...band.points].reverse().map(([t, v]) => coords(t, v));
      svg += '<polygon points="' + upper.concat(lower).join(' ') + '" fill="' + colors.live + '" fill-opacity=".16"/>';
    }
    // Paint the reference last so a coincident baseline remains visible.
    for (const {points: entries, style} of lines) {
      if (style === 'observed') {
        for (const [t, v] of entries) svg += '<circle cx="' + x(t) + '" cy="' + y(v) + '" r="2.7" fill="' + colors[style] + '"/>';
        continue;
      }
      let path = '', prev;
      for (const [t, v] of entries) {
        if (!Number.isFinite(v)) { prev = undefined; continue; }
        const start = prev === undefined || breaks.some(b => prev < b && b <= t);
        path += (start ? 'M' : 'L') + coords(t, v);
        prev = t;
      }
      svg += '<path d="' + path + '" stroke="' + colors[style] + '"' + (style === 'reference' ? ' stroke-dasharray="5 5"' : '') + '/>';
    }
    const keys = lines.map(({name, style}) => [name, style === 'reference' ? 'dash' : style === 'observed' ? 'dots' : '', colors[style]]);
    if (band) keys.push([band.name, 'band', colors.live]);
    return svg + '</svg><div class="legend">' + keys.map(([name, kind, color]) =>
      '<span><i class="' + kind + '" style="--color:' + color + '"></i>' + esc(name) + '</span>').join('') + '</div>';
  }

  function makeTable(table) {
    return '<div class="table-scroll"><table><thead><tr>' + table.head.map(label => '<th scope="col">' + esc(label) + '</th>').join('') +
      '</tr></thead><tbody>' + table.rows.map(({cells, selected}) => '<tr' + (selected ? ' class="selected"' : '') + '><th scope="row">' +
      esc(cells[0]) + '</th>' + cells.slice(1).map(v => '<td>' + esc(v) + '</td>').join('') + '</tr>').join('') + '</tbody></table></div>';
  }

  function control(field) {
    const {key, label, type, note, format, min, max, step, options} = field;
    const value = values[key];
    const id = 'control-' + key;
    const tip = id + '-note';
    const input = type === 'select'
      ? '<select id="' + id + '" aria-describedby="' + tip + '" data-key="' + key + '">' + Object.entries(options)
        .map(([v, title]) => '<option value="' + esc(v) + '"' + (v === value ? ' selected' : '') + '>' + esc(title) + '</option>').join('') + '</select>'
      : '<input id="' + id + '" aria-describedby="' + tip + '" data-key="' + key + '" type="' + type + '" min="' + min +
        '" max="' + max + '" step="' + (step ?? 1) + '" required value="' + value + '">';
    return '<label class="field"><span class="field-head"><span>' + esc(label) + '</span>' +
      (format ? '<output id="value-' + key + '" for="' + id + '">' + esc(format(value)) + '</output>' : '') + '</span>' +
      input + '<small id="' + tip + '">' + esc(note) + '</small></label>';
  }

  function renderRun() {
    clearTimeout(pending);
    pending = undefined;
    const reference = {...world.defaults};
    if ('seed' in values) reference.seed = values.seed;
    const key = JSON.stringify(reference);
    if (baselineKey !== key) {
      baseline = world.run(reference);
      baselineKey = key;
    }
    const current = JSON.stringify(values) === key ? baseline : world.run(values);
    const view = world.view(current, baseline);
    $('result-title').textContent = view.heading;
    $('metrics').innerHTML = view.metrics.map(({label, value, detail}) =>
      '<div class="metric"><span>' + esc(label) + '</span><strong>' + esc(value) + '</strong><small>' + esc(detail) + '</small></div>').join('');
    $('visual').innerHTML = view.table ? makeTable(view.table) : makeChart(view);
    $('chart-note').textContent = view.note;
    const evidence = typeof world.evidence === 'function' ? world.evidence(values) : world.evidence;
    $('evidence').innerHTML = '<div class="evidence-grid">' + evidence.map(({title, body, flag}) =>
      '<article' + (flag ? ' class="flag"' : '') + '><h4>' + esc(title) + '</h4><p>' + esc(body) + '</p></article>').join('') +
      '</div><div class="source-links">' + world.links.map(([label, href]) => '<a href="' + esc(href) + '">' + esc(label) + ' ↗</a>').join('') + '</div>';
    lastRun = {
      protocol: 'Atlas Worlds browser 1', world: world.id, modelVersion: world.version,
      mode: world.stored ? 'stored experiment' : 'live simulation',
      sourceSha256: Object.fromEntries(world.engines.map(file => [file, sha256[file]])),
      controls: {...values}, referenceControls: reference, current, reference: baseline
    };
    $('run-status').textContent = view.metrics.map(m => m.label + ' ' + m.value).join('. ');
  }

  const guideSteps = [["provisioning","Published foundation · Temple communities","How did temple communities provision a city?","The published paper links coordinated temple communities to agricultural production and distance from the core.","The curve is a normalized output index. The historical sample is shown in the cookbook; it records buildup without simulating it.","Compare 100 and 500 people per community, then choose constant output per person. Inspect the separate distance associations.","Published relationships and assumptions","Community size changes the organization of a fixed illustrative population. Distance is a location. Neither slider proves what a ruler could achieve by decree.","These relationships are not a grain ledger or a decline simulation. They do not feed numerical inputs to the other engines."],["campaign", "1 · Provision the landscape", "What feeds the people who build and fight?", "Rice and fish supply households. Grain and work time also pay for campaigns, channels and construction. The court collects a share after the village reserve.", "Village grain after each season is a stock of food. Campaign time shows when mobilised workers are absent. The cards compare the selected scenario with its reference.", "Try a longer frontier route, then increase the levy. Watch campaign days and harvest overlap before interpreting the food gap.", "Your choices", "Distance, levy size, the share of bonded work assigned to fields, and the collection share represent scenario decisions. Yield, digging cost and transport performance also depend on assumed conditions.", "This experiment covers 18 years in an illustrative provisioning area. Stores have no physical cap. Its grain totals are kept separate from the other experiments."], ["angkor", "2 · Follow growth through time", "How can production support a larger settlement?", "The existing water-and-rice model follows a synthetic regional population through time. Harvests depend on yield and infrastructure condition; population responds within that framework.", "Read the whole population trajectory, including its buildup. The peak and final population describe the modeled region. The chart is a scenario generated by these equations.", "Change maintenance intensity and compare the trajectory. Then vary dependence on waterworks to see whether the same maintenance setting has a different effect.", "Decisions and conditions", "Maintenance intensity represents upkeep effort. Waterworks dependence and paddy yield describe the production system; climate pressure is an imposed scenario.", "The geography and population are synthetic. The engine has no annual grain ledger, and its military and monument allocations can exceed its budget. Use it to examine the growth rules while those gaps remain open."], ["signalling", "3 · Turn resources into authority", "What does visible construction tell a tributary?", "The court inherits monuments and elephants, then divides resources between new construction and a military response. A supplier decides whether to pledge tribute using visible signals or actual capacity.", "The lines distinguish inferred capacity from actual capacity. Dots show the same frontier challenges in both observer worlds. Tribute changes the following year’s resources.", "Increase new construction and watch inferred and actual capacity. Vary the weight given to inherited stone to test how long an old signal can retain allegiance.", "Allocation and observer assumptions", "New construction is a court allocation. Stone weight and trust describe the assumed audience response. Revenue lost at succession is an imposed shock.", "The monument is inherited at the start of this experiment. The seasonal lab separately shows construction costs; these two monument stocks have no numerical handoff."], ["obligations", "4 · Pay the commitments", "Can the court afford to stay, leave or return?", "Local receipts and pledged outside deliveries must cover ritual and court bills. The court can leave after repeated unpaid bills. A separate rule determines whether adequate funding permits return.", "The chart shows the reserve and unpaid court bill. The cards count exits, returns and continued ritual funding across 32 matched seeds.", "Use the signalling model’s handoff button to bring your pledge settings here. Change the rigidity of the court bill and allow funded return.", "Commitments and disruptions", "Bill rigidity and the return rule describe institutional choices. The delivery cut and its duration impose a disruption for comparison.", "This is the implemented link: signalling settings and seed determine pledges and matched harvests here. Separate ledgers prevent double-counting their grain. The exit threshold remains an assumption."], ["monsoon", "5 · Test a published decline account", "What changes when the documented climate sequence is applied?", "Buckley’s regional drought proxy changes agricultural conditions after 1250 in the existing long-run social engine. The comparison uses the same parameters with neutral climate after 1250.", "The chart shows one parameter draw. The cards summarize 2,000 completed draws at the selected crop response. Core activity is court presence multiplied by regional population.", "Compare the climate and neutral lines. Open the technical assumptions to test how the PDSI-to-crop translation changes the result.", "Technical assumptions", "Crop sensitivity is our uncertain translation of a climate proxy into agricultural conditions. Parameter draw selects a sampled set of assumptions. Neither is a policy a ruler can choose.", "This comparison is a separate long-run engine. It does not receive the earlier experiments’ ledgers. Weather before 1250 is synthetic, and residents have no separate migration stock."]];
  function showStepGuide(id) {
    const el = $('step-guide');
    if (!el) return;
    const index = guideSteps.findIndex(s => s[0] === id);
    el.hidden = index < 0;
    if (index < 0) return;
    const [key,label,question,economy,reading,action,kind,controls,boundary] = guideSteps[index];
    const previous = guideSteps[index - 1], next = guideSteps[index + 1];
    el.innerHTML = '<p class="eyebrow">'+esc(label)+'</p><h3>'+esc(question)+'</h3><p>'+esc(economy)+'</p><div class="step-reading"><div><h4>Read the result</h4><p>'+esc(reading)+'</p></div><div><h4>Try this</h4><p>'+esc(action)+'</p></div></div><details><summary>Controls and model boundaries</summary><h4>'+esc(kind)+'</h4><p>'+esc(controls)+'</p><p>'+esc(boundary)+'</p></details><nav class="step-navigation" aria-label="Move through the sequence"><a href="'+(previous?'#'+previous[0]:'#angkor-guide')+'">'+(previous?'← '+esc(previous[1]):'← Sequence overview')+'</a><a class="play-link" href="'+(next?'#'+next[0]:'#angkor-guide')+'">'+(next?esc(next[1])+' →':'Return to sequence overview →')+'</a></nav>';
  }

  function openWorld() {
    clearTimeout(pending);
    const id = location.hash.slice(1);
    const inModel = worlds.some(w => w.id === id);
    if ($('model-library')) $('model-library').hidden = inModel || id === 'angkor-guide';
    if ($('angkor-guide')) $('angkor-guide').hidden = id !== 'angkor-guide';
    if ($('library-intro')) $('library-intro').hidden = inModel || id === 'angkor-guide';
    if ($('model-workbench')) $('model-workbench').hidden = !inModel;
    world = worlds.find(w => w.id === id) || worlds[0];
    if (!states.has(world.id)) states.set(world.id, {...world.defaults});
    values = states.get(world.id);
    baselineKey = null;
    for (const a of $('world-nav').children) {
      if (a.hash === '#' + world.id) a.setAttribute('aria-current', 'page');
      else a.removeAttribute('aria-current');
    }
    showStepGuide(world.id);
    $('world-meta').textContent = world.meta;
    $('world-title').textContent = world.title;
    $('world-question').textContent = world.question;
    $('world-mode').textContent = world.stored ? 'Stored results' : 'Live model';
    $('world-mode').classList.toggle('stored', !!world.stored);
    $('controls-title').textContent = world.stored ? 'Choose a comparison' : 'Controls';
    $('export').textContent = world.stored ? 'Save results JSON ↓' : 'Save run JSON ↓';
    $('csv').hidden = !world.csv;
    $('handoff').hidden = world.id !== 'signalling';
    $('upstream-note').hidden = world.id !== 'obligations';
    if (world.id === 'obligations') {
      const p = values.upstream || AngkorSignalling.defaults;
      const fmt = v => Math.round(v * 100) + '%';
      $('upstream-note').textContent = (values.upstream ? 'Using your signalling settings' : 'Using the reference signalling settings') +
        ' · revenue loss ' + fmt(p.loss) + ', stone weight ' + fmt(p.stoneWeight) +
        ', construction ' + fmt(p.displayShare) + ', trust ' + fmt(p.signalScale) + '.';
    }
    for (const link of document.querySelectorAll('.angkor-sequence a')) {
      if (link.hash === '#' + world.id) link.setAttribute('aria-current', 'step');
      else link.removeAttribute('aria-current');
    }
    $('controls').innerHTML = world.id === 'monsoon' ? '<details class="technical-controls"><summary>Technical assumptions and parameter draw</summary>'+world.controls.map(control).join('')+'</details>' : world.controls.map(control).join('');
    renderRun();
  }

  $('world-nav').innerHTML = worlds.map(w => '<a href="#' + w.id + '">' + esc(w.nav) + '</a>').join('');
  $('controls').addEventListener('input', e => {
    const el = e.target;
    const field = world.controls.find(f => f.key === el.dataset.key);
    if (!field || !el.validity.valid) return;
    values[field.key] = field.type === 'select' ? el.value : el.valueAsNumber;
    if (field.format) $('value-' + field.key).value = field.format(values[field.key]);
    // Keep the first scheduled update and render the latest values when it fires.
    if (pending === undefined) pending = setTimeout(renderRun, field.type === 'range' ? 80 : 0);
  });
  $('controls').addEventListener('change', e => {
    if (e.target.type === 'range' && pending !== undefined) renderRun();
  });
  $('controls').addEventListener('focusout', e => {
    if (e.target.type === 'number' && !e.target.validity.valid) e.target.value = values[e.target.dataset.key];
  });
  $('handoff').addEventListener('click', () => {
    const target = worlds.find(item => item.id === 'obligations');
    const previous = states.get(target.id) || target.defaults;
    states.set(target.id, {...previous, seed: values.seed, upstream: {...values}});
    location.hash = '#obligations';
  });
  $('reset').addEventListener('click', () => {
    states.delete(world.id);
    openWorld();
  });
  function download(data, type, extension) {
    const url = URL.createObjectURL(new Blob([data], {type}));
    const anchor = document.createElement('a');
    anchor.href = url;
    anchor.download = 'atlas-' + world.id + '.' + extension;
    anchor.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  $('export').addEventListener('click', () => {
    if (pending !== undefined) renderRun();
    download(JSON.stringify(lastRun, null, 2), 'application/json', 'json');
  });
  $('csv').addEventListener('click', () => {
    if (pending !== undefined) renderRun();
    download(world.csv(lastRun.current), 'text/csv', 'csv');
  });
  window.addEventListener('hashchange', openWorld);
  openWorld();
})();
