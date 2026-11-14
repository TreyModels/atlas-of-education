'use strict';
globalThis.AtlasWorldsLab = (() => {
  const {mandala, relfloor, sha256} = AtlasEvidence;
  const number = (x, digits = 0) => new Intl.NumberFormat('en', {maximumFractionDigits: digits}).format(x);
  const pct = (x, digits = 1) => number(x * 100, digits) + '%';
  const signed = (x, digits = 1) => (x > 0 ? '+' : '') + number(x, digits);
  const line = (name, points, style = 'live') => ({name, points, style});
  const series = (rows, read) => rows.map(row => [row.year, read(row)]);
  const range = (key, label, min, max, step, format, note) => ({key, label, min, max, step, format, note, type: 'range'});
  const select = (key, label, options, note) => ({key, label, options, note, type: 'select'});
  const seed = {key: 'seed', label: 'Random seed', min: 1, max: 4294967295, type: 'number', note: 'Both runs use this seed. Changes can alter the sequence of events.'};
  const evidence = (title, body, flag = false) => ({title, body, flag});
  const metric = (label, value, detail) => ({label, value, detail});
  const education = ['Full Education Atlas and Planning Lab', 'reference/education/'];
  const angkor = ['Bilingual Angkor app · maps, Monte Carlo and regression', 'reference/angkor/'];
  const methods = ['Monte Carlo Methods Lab', 'reference/monte-carlo/'];
  const mandalaArchive = ['Original Mandala explorer', 'reference/mandala/'];
  const history = ['Mandala model card and historical checks', 'reference/mandala/model_card.json'];

  const chinaFit = {...ATLAS_DATA.defaults, ...ATLAS_DATA.tilly_defaults, ...ATLAS_DATA.params.tilly,
    demand: 'observed', grad_demand: 'observed'};
  // All CamChild policy levers are exposed. Lines average matched seeds; "no programmes" keeps the Thailand route.
  const camBaseCache = new Map();
  const camSummary = sim => ({spent: sim.spent.total, rows: sim.rows.map(r => ({year: r.year, cl: r.all.cl, attend: r.all.attend,
    clPoor: r.all.clPoor, clRich: r.all.clRich, clGirls: r.all.clGirls, clBoys: r.all.clBoys, clLeft: r.all.clLeft,
    migrant: r.all.migrant, clCity: r.pp.cl, clRural: r.rural.cl}))});
  const camMean = (runs, read) => runs[0].rows.map((_, i) => runs.reduce((s, run) => s + read(run.rows[i]), 0) / runs.length);
  const cambodia = {
    id: 'cambodia', nav: 'Cambodia · Child labour', title: 'School and work in Cambodia',
    meta: 'EDUCATION WORLD 01 · 2025–2036', question: 'What happens to child labour when school costs less or offers more protection?',
    version: 'Atlas of Education 0.11.2 · Cambodia child world · all policy levers', engines: ['camchild.js'],
    defaults: {cash: 0, cashU: 0, feeding: 0, protection: 0, leftSupport: 0, harvest: 0, bridging: 0, tutorFix: 0,
      ban: 0, floorRise: 0, garmentBoom: 0, debtRelief: 0, thaiOpen: 1, runs: '4', seed: 7},
    controls: [
      {...range('cash', 'Cash for school attendance', 0, .15, .005, pct, 'Per enrolled child in the poorest 40%, as a share of an adult annual wage.'), group: 'Paying for school'},
      {...range('cashU', 'Unconditional cash to poor households', 0, .15, .005, pct, 'Paid to the same households whatever the child does: an income effect only.'), group: 'Paying for school'},
      {...range('tutorFix', 'End teacher-sold extra classes', 0, 1, .05, pct, 'Teachers are paid instead of selling private tutoring to their own pupils.'), group: 'Paying for school'},
      {...range('debtRelief', 'Microfinance debt relief', 0, 1, .05, pct, 'Restructures household loan repayments and eases borrowing after a shock.'), group: 'Paying for school'},
      {...range('protection', 'Safety and care at school', 0, 1, .05, pct, 'Intensity of safe routes, adult care and counselling.'), group: 'What school offers'},
      {...range('feeding', 'School meal coverage', 0, 1, .05, pct, 'Share of schools the programme covers.'), group: 'What school offers'},
      {...range('leftSupport', 'Support for children of migrant parents', 0, 1, .05, pct, 'Care and follow-up for children whose parents work away.'), group: 'What school offers'},
      {...range('harvest', 'Flexible timetable at harvest', 0, 1, .05, pct, 'Rural adolescents can combine school with planting and harvest work.'), group: 'What school offers'},
      {...range('bridging', 'Re-entry and bridging classes', 0, 1, .05, pct, 'Lowers the penalty for returning after time out of school.'), group: 'What school offers'},
      {...range('ban', 'Minimum-age enforcement', 0, 1, .05, pct, 'Intensity of enforcement in factories.'), group: 'Work, credentials and migration'},
      {...range('floorRise', 'Formal jobs asking for a Grade 12 diploma', 0, 1, .05, pct, 'Raises the credential floor: more formal jobs read the upper-secondary diploma.'), group: 'Work, credentials and migration'},
      {...range('garmentBoom', 'Rise in teen wages in Phnom Penh', 0, .5, .05, pct, 'Higher pay in factories and construction pulls older teens towards work.'), group: 'Work, credentials and migration'},
      {...range('thaiOpen', 'Thailand route open', 0, 1, .05, pct, 'Context, not a programme. The reference keeps the route open; 0% closes it, as after the July 2025 border conflict.'), group: 'Work, credentials and migration'},
      select('runs', 'Simulated histories per setting', {'1': '1 · fastest', '4': '4 · with range', '8': '8 · slower, steadier'}, 'More histories make the average steadier and the range more informative, but take longer to calculate.'),
      seed
    ],
    run({seed, runs, ...policy}) {
      const seeds = Array.from({length: Number(runs) || 1}, (_, i) => (Number(seed) + i) >>> 0);
      const thaiOpen = policy.thaiOpen;
      // With every programme at zero the run is the no-programme baseline itself, so it is simulated once.
      const noProgramme = Object.entries(policy).every(([k, x]) => k === 'thaiOpen' || !Number(x));
      const baseFor = s => {
        const key = s + ':' + thaiOpen;
        if (!camBaseCache.has(key)) camBaseCache.set(key, camSummary(CamChild.simulate({seed: s, policy: {thaiOpen}})));
        return camBaseCache.get(key);
      };
      const current = seeds.map(s => noProgramme ? baseFor(s) : camSummary(CamChild.simulate({seed: s, policy})));
      const base = seeds.map(baseFor);
      const N = 6000;
      const avoided = current.map((run, k) => run.rows.reduce((s, r, i) => s + base[k].rows[i].cl - r.cl, 0) * N);
      const yearsAvoided = avoided.reduce((a, b) => a + b, 0) / seeds.length;
      const spent = current.reduce((s, run) => s + run.spent, 0) / seeds.length;
      return {parameters: {seeds, policy, N, years: 12}, current, base, yearsAvoided, costPer: yearsAvoided > 0 ? spent / yearsAvoided : null};
    },
    view({current, base, yearsAvoided, costPer}) {
      const years = current[0].rows.map(r => r.year), mean = read => camMean(current, read), baseMean = read => camMean(base, read);
      const cl = mean(r => r.cl), clBase = baseMean(r => r.cl), last = years.length - 1;
      const final = current.map(run => run.rows[last].cl), lo = Math.min(...final), hi = Math.max(...final);
      const at = read => mean(read)[last];
      return {
        heading: 'Child labour rate',
        metrics: [
          metric('Working in 2036', pct(cl[last]), current.length > 1 ? 'Mean across simulated histories' : 'Model definition of child labour'),
          metric('Change vs no programmes', signed(100 * (cl[last] - clBase[last])) + ' pp', 'National rate in 2036'),
          metric('Child-years avoided', number(yearsAvoided), 'Over 12 years per 6,000 children'),
          metric('Attending school, 2036', pct(at(r => r.attend)), 'School only, or school and work'),
          metric('Child labour, poorest fifth', pct(at(r => r.clPoor)), 'Bottom income quintile, 2036'),
          metric('Child labour, richest fifth', pct(at(r => r.clRich)), 'Top income quintile, 2036'),
          metric('Child labour, countryside', pct(at(r => r.clRural)), 'Rural region, 2036'),
          metric('Child labour, Phnom Penh', pct(at(r => r.clCity)), 'Capital region, 2036'),
          metric('Children of migrant parents', pct(at(r => r.clLeft)), 'In child labour, 2036'),
          metric('Teens working away from home', pct(at(r => r.migrant)), 'Share of all children, 2036'),
          metric('Range across histories', pct(lo) + '–' + pct(hi), 'Child labour in 2036'),
          metric('Illustrative cost index per child-year avoided (invented unit costs)', costPer === null ? '—' : number(costPer, 2), 'Adult annual wages')
        ],
        lines: [line('Current settings', years.map((y, i) => [y, cl[i] * 100])), line('No programmes', years.map((y, i) => [y, clBase[i] * 100]), 'reference')],
        band: current.length > 1 ? {name: 'Range across histories', points: years.map((y, i) => {
          const v = current.map(run => run.rows[i].cl * 100); return [y, Math.min(...v), cl[i] * 100, Math.max(...v)]; })} : undefined,
        axis: v => number(v, 1) + '%',
        note: 'Lines average simulated histories with matched seeds; the band spans the lowest and highest history. “No programmes” keeps the same seeds and the same Thailand route.'
      };
    },
    evidence: [
      evidence('Observed · Out of school', 'The parent model uses UIS age-banded out-of-school rates. Attending school and being in child labour can occur together.'),
      evidence('Assumed · Programme effects', 'Safety, meals, tutoring, bridging and the factory ban use stylised effect sizes. Unit costs are assumed, in adult annual wages.'),
      evidence('Assumed · Migration and the credential floor', 'The Thailand route, Phnom Penh wages and the Grade 12 floor change what work and schooling are worth. Their strengths are assumptions drawn from the Atlas papers.'),
      evidence('Fit gap · Rural lower secondary', 'The full Atlas documents a large unexplained boost to staying in school that the model needs to reproduce the rural pattern.', true)
    ], links: [education],
    csv({current}) {
      const keys = ['history', 'year', 'cl', 'attend', 'clPoor', 'clRich', 'clGirls', 'clBoys', 'clLeft', 'migrant', 'clCity', 'clRural'];
      return [keys.join(','), ...current.flatMap((run, k) => run.rows.map(r => [k + 1, ...keys.slice(1).map(key => r[key])].join(',')))].join('\n');
    }
  };

  const china = {
    id: 'china', nav: 'China · Graduate jobs', title: 'China’s graduate queue',
    meta: 'EDUCATION WORLD 02 · MONTHLY LABOUR MARKET', question: 'How do the number of graduates and the demand for graduate jobs change youth unemployment?',
    version: 'Atlas of Education 0.11.2 · Tilly graduate queue', engines: ['youth.js', 'atlas_data.js'],
    defaults: {gradSupply: 1, dr_drop: chinaFit.dr_drop, hoard: chinaFit.hoard, wait_max: chinaFit.wait_max},
    controls: [
      range('gradSupply', 'Graduate entrants from 2019', .5, 1.5, .01, v => number(v, 2) + '×', 'Scale the graduate input series after 2018.'),
      range('dr_drop', 'Aug-2021 step (unexplained residual, fitted)', 0, .6, 'any', pct, 'Unexplained residual (fitted), not a measured demand shock. No sourced series matches it.'),
      range('hoard', 'Secure jobs reserved for insiders', 0, .8, .01, pct, 'Share of secure openings filled through the network. An assumption, not estimated.'),
      range('wait_max', 'Maximum monthly move into waiting', 0, .3, 'any', pct, 'Graduates waiting outside the labour force are outside the official unemployment rate. The waiting mechanism is untested: no data on family support for waiting.')
    ],
    run(values) {
      const parameters = {...chinaFit, ...values};
      return {parameters, run: AtlasYouth.run(ATLAS_DATA, parameters)};
    },
    view(current, base) {
      const start = [2024, 1], end = [2026, 9];
      const mean = key => AtlasYouth.windowMean(current.run, key, start, end);
      const data = r => r.year.map((y, i) => {
        const date = y + (r.month[i] - .5) / 12;
        return [date, date < 2024 ? r.rate_old[i] : r.rate_new[i]];
      }).filter(p => p[0] >= 2018);
      const observations = ATLAS_DATA.inputs.youth.filter(o => o[4] === 'v')
        .map(o => [o[0] + (o[1] - .5) / 12, o[2]]);
      return {
        heading: 'Youth unemployment',
        metrics: [
          metric('Model rate · 2024–26', number(mean('rate_new'), 1) + '%', 'Mean through September 2026'),
          metric('Change vs fitted run', signed(mean('rate_new') - AtlasYouth.windowMean(base.run, 'rate_new', start, end)) + ' pp', 'Same reporting window'),
          metric('Graduates waiting', number(mean('waiting'), 2) + 'm', 'Mean outside the labour force'),
          metric('Broad rate · 2024–26', number(mean('broad_u'), 1) + '%', 'Unemployed plus graduates waiting'),
          ...AtlasYouth.benchmarks(ATLAS_DATA).filter(b => b.id !== 'fit_2018_22').map(b =>
            metric(b.label, number(b.model, 1) + ' model · ' + (b.naive == null ? '–' : number(b.naive, 1)) + ' naive', b.detail))
        ],
        lines: [line('Current model', data(current.run)), line('Fitted reference', data(base.run), 'reference'), line('Verified points in Atlas’s NBS series', observations, 'observed')],
        axis: v => number(v, 1) + '%', breaks: [2024],
        note: 'The Atlas series switches to the student-excluding NBS definition in 2024. The chart separates the two series at the break.'
      };
    },
    evidence: [
      evidence('Observed · NBS rates', 'The points come from the supplied Atlas extract and use its verified flag. The plot omits entries flagged as recalled from memory.'),
      evidence('Fitted · Whole-record reference', 'The reference was fitted to the record shown, so its fit statistics are in sample. Supply, demand and wage responses interact. The hoarding share, insider split and wage wedge were set as assumptions, not estimated. The waiting and emulation mechanisms are untested, and the 2021 step is an unexplained residual.'),
      evidence('Holdout · Earlier fit missed the bulge', 'The Atlas documents that a model fitted to 2018–22 misses the later youth unemployment rise. A naive benchmark (the same month of 2022, carried forward) does better on the 2023 H1 holdout and on the verified months from December 2023.', true)
    ], links: [education]
  };

  const teachers = {
    id: 'teachers', nav: 'Planning · Teachers', title: 'Can teacher supply keep up?',
    meta: 'PLANNING TOOL 01 · 2025–2050', question: 'When does a teacher shortage open up if training takes longer or more teachers leave?',
    version: 'Atlas of Education 0.11.2 · Planning Lab teacher projection', engines: ['lab_models.js'],
    defaults: {growth: .02, lag: 4, cap: .1, youngQuit: .06},
    controls: [
      range('growth', 'Annual growth in teachers needed', -.04, .05, .005, pct, 'Sets the demand path from the starting teacher stock.'),
      range('lag', 'Training length', 1, 5, 1, v => v + ' yr', 'Years between intake and graduation.'),
      range('cap', 'Annual change allowed in college intake', .02, .4, .01, pct, 'Caps expansion and contraction.'),
      range('youngQuit', 'Annual quit rate under 30', .01, .15, .005, pct, 'Retirement and exits at older ages follow the original demo.')
    ],
    run(values) {
      const {growth, lag, cap, youngQuit} = values;
      const initialByAge = Array.from({length: 38}, (_, i) => 1000 * (1 + .5 * (i / 38 - .5) * 1.6));
      const total = initialByAge.reduce((a, b) => a + b, 0);
      const parameters = {...values, years: 26, startYear: 2025, retire: 60, intake0: 3000,
        completion: .85, absorption: .9, initialByAge, olderExitRates: {'30–55': .015, '56–59': .04}};
      const {rows} = AtlasLab.teacherProjection({...parameters, capGrowth: cap,
        required: t => total * (1 + growth) ** t, exitRate: age => age < 30 ? youngQuit : age > 55 ? .04 : .015});
      return {parameters, rows};
    },
    view({rows}, base) {
      const last = rows.at(-1), worst = rows.reduce((a, b) => b.gap > a.gap ? b : a);
      return {
        heading: 'Teacher supply and demand',
        metrics: [metric('Largest shortage', number(Math.max(0, worst.gap)), worst.gap > 0 ? 'Teachers in ' + worst.year : 'Teachers'),
          metric('Teachers in post', number(last.stock), '2050'),
          metric('Teachers required', number(last.required), '2050')],
        lines: [line('Current supply', series(rows, r => r.stock)), line('Reference supply', series(base.rows, r => r.stock), 'reference'),
          line('Current demand', series(rows, r => r.required), 'alternate')],
        axis: v => number(v / 1000, 1) + 'k', note: 'This is an age-structured projection using the synthetic Planning Lab demo.'
      };
    },
    evidence: [
      evidence('Method · Age-structured stock', 'Teacher supply changes with quits, retirement, graduations and hiring. The original Planning Lab follows IIEP teacher projection practice.'),
      evidence('Assumed · Starting system', 'Initial age counts, training completion and hiring eligibility are synthetic. This example aggregates subjects and locations.')
    ], links: [education]
  };

  const angkorLive = {
    id: 'angkor', nav: 'Angkor · Water & rice', title: 'Water, rice and population in Angkor',
    meta: 'HISTORICAL WORLD 01 · ANGKOR RESEARCH EDITION V1.0', question: 'How does the model respond when harvests depend more on hydraulic infrastructure?',
    version: 'Angkor Atlas Research Edition v1.0 · JavaScript', engines: ['model.js'],
    defaults: Object.fromEntries(['yieldT', 'hydraulicDependency', 'maintenanceIntensity', 'lateDrought', 'seed'].map(k => [k, AngkorModel.DEFAULTS[k]])),
    controls: [
      range('yieldT', 'Annual paddy yield', .7, 3.5, .05, v => number(v, 2) + ' t/ha', 'Nominal yield before weather and other adjustments.'),
      range('hydraulicDependency', 'Dependence on waterworks', 0, 1, .01, pct, 'How strongly infrastructure condition affects harvest.'),
      range('maintenanceIntensity', 'Maintenance intensity', 0, 1, .01, pct, 'Changes both upkeep demand and repair effectiveness.'),
      range('lateDrought', 'Climate pressure after 1300', 0, .8, .01, pct, 'An illustrative stress parameter.'),
      seed
    ],
    run: values => AngkorModel.simulate(values, {cadence: 1}),
    view(current, base) {
      const peak = current.timeline.reduce((a, b) => b.pop > a.pop ? b : a);
      return {
        heading: 'Simulated regional population',
        metrics: [metric('Population in 1450', number(current.final.pop), 'People in the modeled region'),
          metric('Change vs reference', signed(current.final.pop - base.final.pop, 0), 'People in 1450'),
          metric('Peak population', number(peak.pop), 'In ' + peak.year + ' CE')],
        lines: [line('Current run', series(current.timeline, r => r.pop)), line('Same-seed reference', series(base.timeline, r => r.pop), 'reference')],
        axis: v => number(v / 1000, 1) + 'k',
        note: 'One simulated history per setting. The grid and population are synthetic.'
      };
    },
    evidence: [
      evidence('Historical anchor · Paddy yields', 'The model card cites about 1.5 t/ha as an uncertain literature anchor. The reference starts at 1.6 t/ha.'),
      evidence('Assumed · Waterworks and drought', 'The sliders vary model rules and stress. The reference leaves the optional scripted 1177 shock off.'),
      evidence('Accounting gaps · Grain and armies', 'Annual grain inventories are absent. Military and monument allocations can exceed the available budget. These gaps limit the population and military claims.', true)
    ],
    links: [angkor, ['Research methods and audit', 'reference/angkor/research/METHODS_AND_ASSUMPTIONS.md'],
      ['Source and provenance notes', 'reference/angkor/research/SOURCES_AND_PROVENANCE.md']]
  };

  const scenarios = {reference: 'Reference', canal_first: 'Canal first', resilient: 'Maintenance and autonomy',
    high_shock: 'High climate shock', no_water: 'No engineered water'};
  const mandalaWorld = {
    id: 'mandala', nav: 'Angkor · 100 seeds', title: 'Angkor across 100 seeds',
    meta: 'HISTORICAL WORLD 02 · ORIGINAL PYTHON MANDALA LAB', question: 'How often does the result recur across simulated histories, and where does the reference miss history?',
    version: 'Angkor Mandala Lab v0.1 · Monte Carlo Methods Lab', stored: true, engines: ['results.json', 'trajectories_100_seeds.csv'],
    defaults: {scenario: 'reference'},
    controls: [select('scenario', 'Stored scenario', scenarios, '100 existing runs per scenario, using seed indices 0–99.')],
    run({scenario}) { return {scenario, seedIndices: Array.from({length: mandala.seeds}, (_, i) => i),
      summary: mandala.summary[scenario], paired: mandala.paired[scenario] || null, population: mandala.population[scenario]}; },
    view(current, base) {
      const s = current.summary;
      return {
        heading: 'Regional population across seeds',
        metrics: [
          metric('Population falls after 1300', Math.round(100 * s.post_1300_decline.mean) + '/100', 'Runs with fewer people in 1500 than 1300'),
          metric('Angkor leads in 1200', Math.round(100 * s.angkor_leads_1200.mean) + '/100', 'Rank by aligned population'),
          metric('Median population in 1500', number(s.population_1500_k.median / 1000, 2) + 'm', 'Synthetic region')],
        band: {name: 'Current 10th–90th percentile', points: current.population},
        lines: [line('Current median', current.population.map(([y,, m]) => [y, m])),
          line('Reference median', base.population.map(([y,, m]) => [y, m]), 'reference')],
        axis: v => number(v / 1e6, 2) + 'm',
        note: 'The band measures seed variation inside this model. “No engineered water” removes both irrigation gains and infrastructure damage.'
      };
    },
    evidence: [
      evidence('Failed · Angkor as leading centre', 'Angkor leads by aligned population in 0 of 100 reference runs at 1200. This is a model proxy for historical political centrality.', true),
      evidence('Scale check · Population', 'The supplied model card cites a 700,000–900,000 estimate for the 13th-century Greater Angkor region. The reference median reaches 2.14 million by 1500 on a synthetic board with no matching geography.', true),
      evidence('Structural uncertainty · Water regime', 'Scenarios change assumptions about investment or waterworks. Seed variation within one scenario answers a separate question.')
    ], links: [methods, mandalaArchive, history]
  };

  const margins = {Cambodia: 'Lower-secondary completion', Vietnam: 'Upper-secondary completion at 19', China: 'College entry'};
  const structures = {M_HC: 'Human capital', M_POS: '+ Positional', M_REL: '+ Relational'};
  const targets = {
    Cambodia: 'Completion was about 17% in 2000 and 56–58% in 2021. The two 2010 series give 37–49%. The comparison has no wealth gradient.',
    Vietnam: 'Young Lives reports 57.7% completion at 19, with 25.1% in the bottom wealth quintile and 80.5% in the top.',
    China: 'Tertiary gross enrolment is the proxy for college entry. The 2012, 2019 and 2023 anchors are about 30%, 48% and 60.2%.'
  };
  const floor = {
    id: 'credentials', nav: 'Education · Credential floor', title: 'What keeps students in school?',
    meta: 'COMPARATIVE EDUCATION · STORED PARAMETER DRAWS', question: 'Which explanations fit the targets, and who leaves when the relative value of a credential falls?',
    version: 'Atlas 0.11.2 · relfloor_countries.py · 5 November 2026', stored: true, engines: ['relfloor_countries.json'],
    defaults: {country: 'Cambodia', structure: 'M_REL'},
    controls: [
      select('country', 'Country', {Cambodia: 'Cambodia', Vietnam: 'Vietnam', China: 'China'}, 'Each country uses a different credential margin.'),
      select('structure', 'Highlight a mechanism bundle', structures, 'The comparison keeps all three bundles visible.')
    ],
    run({country, structure}) { return {country, structure, drawsPerBundle: 24000, rows: relfloor[country]}; },
    view({country, structure, rows}) {
      const r = rows[structure];
      return {
        heading: margins[country],
        metrics: [metric('Draws meeting targets', pct(r.rate, 2), number(r.accepted) + ' of 24,000'),
          metric('Exits from poorest 40%', pct(r.exit_low[1]), 'Median among accepted draws'),
          metric('2035 completion change', signed(100 * r.fall35_q3[1]) + ' pp', 'Middle quintile and above')],
        table: {head: ['Mechanisms', 'Draws accepted', 'Exits from poorest 40%', '2035 change'],
          rows: Object.entries(rows).map(([key, v]) => ({selected: key === structure,
            cells: [structures[key], pct(v.rate, 2), pct(v.exit_low[1]), signed(100 * v.fall35_q3[1]) + ' pp']}))},
        note: 'The stored 2035 experiment lowers the relative earnings premium by 40%. The change refers to the middle quintile and above. Acceptance shares depend on each country’s targets and priors.'
      };
    },
    evidence: ({country}) => [
      evidence('Historical targets · ' + country, targets[country]),
      evidence('Model comparison · Wealth gradient', 'Vietnam supplies a wealth gradient in this comparison. Its acceptance share drops from 6.1% for human capital alone to about 0.8% with the relational mechanism.'),
      evidence('What the comparison leaves open', 'The supplied research note identifies missing wealth gradients for Cambodia and China. China’s graduate pay relative to urban average is a proxy for the college versus high-school premium.', true)
    ], links: [['Comparative results note', 'reference/credential-floor.md'], ['Stored parameter summaries', 'reference/relfloor_countries.json']]
  };
  const campaign = {
    id: 'campaign', nav: 'Angkor · Campaigns & distance', title: 'Can the army get home before harvest?',
    meta: 'HISTORICAL WORLD 03 · EXPERIMENTAL SEASONAL MODEL',
    question: 'How far can a court send a levy before the campaign competes with farming, construction and grain reserves?',
    version: 'Angkor Seasonal Campaign Lab v0.2', engines: ['campaign.js'],
    defaults: AngkorCampaign.defaults,
    controls: [
      range('distance', 'One-way route to the frontier', 30, 540, 10, v => number(v) + ' km', 'Route distance from the court, rather than straight-line distance.'),
      range('fightingDays', 'Days campaigning at the frontier', 10, 180, 5, v => number(v) + ' days', 'Travel time is added in both directions. The levy can miss harvest.'),
      select('transport', 'Transport regime', {foot: 'Foot and porters', elephant: 'Foot with elephant support', river: 'River route'}, 'Illustrative speeds and freight capacities. River runs assume a navigable route.'),
      range('yield', 'Paddy per hectare at full staffing', .8, 3, .05, v => number(v, 2) + ' t/ha', 'Seasonal weather and missing farm work reduce realized output.'),
      range('collection', 'Court share of grain above village reserve', .05, .55, .01, pct, 'Collected at harvest after household rations.'),
      range('levy', 'Share of free adults called up', .02, .3, .01, pct, 'The levy remains absent until it returns.'),
      range('fieldShare', 'Bonded work time assigned to fields', 0, 1, .05, pct, 'The balance can go to construction. Returned captives also need food.'),
      select('fishery', 'Access to fish', {lake: 'Lake and floodplain', corridor: 'Downstream river corridor', none: 'Fish supply off'}, 'Changes the amount and timing of the modeled catch. Route settings are held fixed.'),
      range('digging', 'Labour cost of digging channels', .5, 3, .1, v => number(v, 1) + '×', 'Lower cost lets the same digging crew build or restore more channel capacity.'),
      seed
    ],
    run: values => AngkorCampaign.compare(values),
    view(current, base) {
      const rows = current.rows, sum = key => rows.reduce((n, r) => n + r[key], 0);
      const allies = rows.find(r => r.alliedSoldiers);
      const worse = current.pairedSeeds.filter(r => r.foodGapDelta > 1e-8).length;
      const missed = rows.filter(r => r.season === 'Harvest' && r.localSoldiers > 0).length;
      return {
        heading: 'Village grain after each season',
        metrics: [metric('Earliest arrival at frontier', current.responseDays + ' days', 'Travel only, one way'),
          metric('Round trip with fighting', current.campaignDays + ' days', '120 days before harvest starts'),
          metric('Harvests with levy still out', number(missed) + '/18', 'Campaign overlaps the harvest season'),
          metric('People taken captive', number(sum('captured')), 'Transferred from the frontier on return'),
          metric('First allied contingent', allies ? String(allies.calendarYear) : 'None', 'After a completed campaign and adequate reserves'),
          metric('Fish protein consumed', number(sum('fishProteinKg') / (1000 * 18), 1) + ' t/yr', 'Average across 18 modeled years'),
          metric('Channel capacity', pct(sum('channels') / rows.length), 'Average share of the modeled maximum'),
          metric('Larger food gap', worse + '/32', 'Paired seeds vs reference')],
        lines: [line('Current village reserve', series(rows, r => r.villageGrain)),
          line('Same-seed reference', series(base.rows, r => r.villageGrain), 'reference')],
        axis: v => number(v / 1000, 1) + 'k t',
        note: 'Runs on this device. The chart shows one seed. The food-gap card compares 32 paired histories using the same weather and capture draws. Download the CSV to inspect the court reserve, farm work, campaigns, captures, fish, earthworks, stone and timber.'
      };
    },
    evidence: [
      evidence('Geography · A region, not one dense city', 'Klassen and colleagues estimate 700,000–900,000 people at the 13th-century apogee within a study region of about 3,000 km². This lab models one illustrative provisioning area.'),
      evidence('Assumed · Routes and campaigning', 'Distance is a scenario input. Mode speeds, transport savings and capture rates are illustrative. The model assumes a completed campaign and sufficient reserves attract an allied contingent. Every funded campaign returns with a sampled captive count. There is no opponent strategy or battle outcome.', true),
      evidence('Accounting · People and rations', 'A returning captive leaves the frontier population, enters the dependent population and draws household rations in later seasons. Allied soldiers are an external contingent that the court provisions on campaign. The frontier economy and population growth are outside this first model.'),
      evidence('Comparative case · Straits polities', 'Srivijaya linked a riverine hinterland to maritime trade. A rival coalition rule would recruit partners through route access and shared trade returns. The current river option changes transport only.'),
      evidence('Flood pulse · Lake and corridor', 'The lake and downstream corridor both get fish, with different modeled seasons. Catch uses labour. Fish add protein and offset at most 8% of the grain ration. Seasonal catch has an illustrative ecological cap. There is no changing fish population. The grain conversion is also illustrative.'),
      evidence('Earthworks · Labour buys channels', 'Digging and maintenance draw on the same grain and work time as monuments. Channel capacity improves future rice yields and river freight under assumed rates. The slider varies digging cost, with the underlying hydrology held fixed.'),
      evidence('Building · Timber and stone', 'Construction draws on available labour and grain. Stone faces a freight cap. Timber capacity depreciates seasonally. The freight and decay rates are experimental.')
    ],
    links: [['Angkor population reconstruction', 'https://doi.org/10.1126/sciadv.abf8441'],
      ['Srivijaya and its maritime hinterland', 'https://doi.org/10.1093/oxfordhb/9780199355358.013.37'],
      ['Mekong River Commission · flood pulse', 'https://www.mrcmekong.org/hydrology/'],
      ['Inspect the seasonal model code', 'engines/campaign.js']],
    csv(run) {
      const keys = Object.keys(run.rows[0]);
      return [keys.join(','), ...run.rows.map(row => keys.map(key => row[key]).join(','))].join('\n');
    }
  };
  const signalling = {
    id: 'signalling', nav: 'Angkor · Monument signalling', title: 'Would you pay tribute to the successor?',
    meta: 'ANGKOR · EXPERIMENT 03 · UNDER ACTIVE EXAMINATION',
    question: 'Two observers see the same inherited monument. One judges by the display, the other can see what the court could actually muster.',
    version: 'Angkor Monument Signalling Lab v0.1', engines: ['signalling.js'],
    defaults: AngkorSignalling.defaults,
    controls: [
      range('loss', 'Revenue lost at succession', 0, .85, .05, pct, 'The monument starts intact. Local grain revenue recovers over eight modeled years.'),
      range('stoneWeight', 'Weight observers give to stone', 0, 1, .05, pct, 'The remaining weight goes to the elephants the court can visibly maintain this year.'),
      range('displayShare', 'Resources assigned to new construction', 0, .6, .01, pct, 'New work uses both labour and grain before the court provisions a response.'),
      range('signalScale', 'How strongly observers trust the display', .6, 1.2, .05, v => number(v, 2) + '×', 'Scales the capacity an observer infers from the same stone and elephants.'),
      seed
    ],
    run: values => AngkorSignalling.compare(values),
    view({current, truth, pairedSeeds}) {
      const falseYears = current.rows.filter(r => r.pledged && !r.defended).length;
      const kept = pairedSeeds.filter(r => r.tributeYearsDelta > 0).length;
      const lost = pairedSeeds.filter(r => r.tributeYearsDelta < 0).length;
      return {
        heading: 'What the court can muster',
        metrics: [
          metric('Pledge despite failed defence', falseYears + '/12', 'Display observer · one seed'),
          metric('Display retains more pledge years', kept + '/32', 'More pledged years than informed observer'),
          metric('Display retains fewer pledge years', lost + '/32', 'Fewer pledged years than informed observer')
        ],
        lines: [
          line('Capacity inferred from display', series(current.rows, r => r.displayedCapacity), 'live'),
          line('Actual capacity · display world', series(current.rows, r => r.trueCapacity), 'reference'),
          line('Actual capacity · informed world', series(truth.rows, r => r.trueCapacity), 'alternate'),
          line('Frontier challenge', series(current.rows, r => r.demand), 'observed')
        ],
        axis: v => number(v) + ' t',
        note: 'Grain-equivalent tonnes of response capacity. Dots are shared simulated challenges. The chart shows one seed. The cards compare 32 paired runs. A pledge affects the following year’s grain, so the observer rule can change what the court can actually muster.'
      };
    },
    evidence: [
      evidence('Borrowed · Costly signalling', 'Monumental display as a costly signal is an existing archaeological explanation. This experiment asks when inherited stone gives a tributary stale information.'),
      evidence('Evidence · Elephants and transport', 'The historical gallery depicts elephants in the royal procession. Quarry research suggests a canal route for sandstone. Elephant maintenance costs here are abstract grain equivalents, with no assumed elephant freight fleet.'),
      evidence('Assumed · Beliefs and tribute', 'The weights, recovery schedule and pledge decision are illustrative. We have no direct measure of what tributaries inferred from a monument or an elephant contingent.', true),
      evidence('Test · Identical challenges', 'Both worlds start with the same stock of stone and elephants, and face the same harvest shocks and challenges. One observer uses visible signals. The other sees actual capacity.')
    ],
    links: [
      ['Experiment 03 cookbook and review results', 'research/signalling.html'],
      ['Inspect the signalling engine', 'engines/signalling.js'],
      ['Quarries and sandstone transport · Uchida and Shimoda', 'https://doi.org/10.1016/j.jas.2012.09.036']
    ],
    csv(run) {
      const rows = [...run.current.rows, ...run.truth.rows];
      const keys = Object.keys(rows[0]);
      return [keys.join(','), ...rows.map(row => keys.map(key => row[key]).join(','))].join('\n');
    }
  };
  const obligations = {
    id: 'obligations', nav: 'Angkor · Obligations and exit', title: 'Who pays the bill after the court leaves?',
    meta: 'ANGKOR · EXPERIMENT 04 · UNDER ACTIVE EXAMINATION',
    question: 'Can worship continue when outside deliveries no longer cover the court’s commitments? What would let a court come back?',
    version: 'Angkor Obligations Lab v0.2', engines: ['obligations.js', 'signalling.js'],
    defaults: AngkorObligations.defaults,
    controls: [
      range('externalShare', 'Share of receipts expected from outside', 0, .9, .05, pct, 'Supplies are collected from linked tributaries rather than produced in the core.'),
      range('rigidity', 'Share of the court bill that cannot be cut', 0, 1, .05, pct, 'The rest scales with actual outside deliveries.'),
      range('disruption', 'Cut to outside deliveries', 0, 1, .05, pct, 'Starts in model year four, on top of any pledged deliveries already lost.'),
      range('duration', 'Duration of the cut', 0, 7, 1, v => v + ' yr', 'The added cut ends after this many years.'),
      select('supplier', 'What suppliers see', {display: 'Monument and elephants', truth: 'Actual military capacity'}, 'Uses the corresponding pledge decisions from Experiment 03.'),
      select('returnRule', 'Can the court return?', {closed: 'Exit ends court operations', open: 'Return if funding covers both bills'}, 'With return open, pledged deliveries can resume and a solvent court can return.'),
      seed
    ],
    run: values => AngkorObligations.compare(values),
    view({current, reference, paired}) {
      const count = key => paired.filter(r => r[key] !== null).length;
      return {
        heading: 'Grain available after each year’s bills',
        metrics: [
          metric('Court exits', count('exitYear') + '/32', 'With the selected delivery cut'),
          metric('Court exits without the added cut', count('referenceExitYear') + '/32', 'Same pledges, harvests and other rules'),
          metric('Court returns', count('returnYear') + '/32', 'Under the selected return rule'),
          metric('Ritual funded after an exit', paired.filter(r => r.ritualContinues).length + '/32', 'Fully funded in at least one later year')
        ],
        lines: [line('Reserve with selected cut', series(current.rows, r => r.reserve)),
          line('Reserve without added cut', series(reference.rows, r => r.reserve), 'reference'),
          line('Unpaid court bill', series(current.rows, r => r.unpaid), 'alternate')],
        axis: v => number(v) + ' t eq.',
        note: 'One history in the chart, 32 matched seeds in the cards. Grain-equivalent units and the two-year exit trigger are illustrative. Use the CSV to see exit and return years for every seed.'
      };
    },
    evidence: [
      evidence('Actual handoff · Pledges and harvests', 'Use the handoff button in Monument Signalling to carry your settings and seed here. Pledge status sets whether outside deliveries arrive. The ledgers are separate and their grain amounts are not added.'),
      evidence('Assumed · Obligations and exit', 'Ritual receives first claim in this version. Two consecutive years of unpaid court bills trigger exit. The return rule lets receipts resume and tests whether both bills can be covered.', true),
      evidence('Historical check · Different timelines', 'Angkor Thom’s core land use declined in the early 1300s. The Angkor Wat enclosure had a separate occupation and reuse history. This experiment has no dated calibration.')
    ],
    links: [['Angkor research sequence', 'research/angkor-sequence.html'],
      ['Inspect the obligations engine', 'engines/obligations.js'],
      ['Angkor Thom land-use chronology', 'https://doi.org/10.1073/pnas.1821460116']],
    csv(run) {
      const keys = Object.keys(run.paired[0]);
      return [keys.join(','), ...run.paired.map(row => keys.map(key => row[key] ?? '').join(','))].join('\n');
    }
  };
  const relocation={id:'relocation',nav:'Angkor · Elite relocation',title:'When does the court choose another centre?',meta:'SEPARATE TWO-CENTRE EXPERIMENT · EXPLORATORY',question:'Elites compare staying with a second centre. Workers move under a different rule, while farmers remain attached to their fields. Compare the same economy with movement blocked.',version:'Atlas Relocation v0.1',engines:['relocation.js'],defaults:AngkorRelocation.defaults,
   controls:[range('outside','Opportunity at the second centre',.6,1.8,.05,v=>number(v,2),'Multiplies the second centre’s utility index. This is an assumed advantage, not a measured trade return.'),range('portability','Share of wealth treated as portable',0,1,.05,pct,'Moving loses part of the place-bound asset value. The model uses an opportunity-cost index rather than a private wealth ledger.'),range('movingCost','Hurdle for moving',0,.6,.05,v=>number(v,2),'A utility difference must exceed this threshold before movement begins. This is not a grain expense.'),range('localRepair','Maintenance covered by local cooperation',0,1,.05,pct,'Farm surpluses can fund this share of maintenance independently of elite presence.'),select('climate','Climate scenario',{stable:'Stable climate',drought:'Two imposed drought episodes'},'The old centre faces 62% and the second centre 85% of ordinary conditions during the same synthetic droughts.'),select('mobility','Who can move?',{open:'Elites and workers',closed:'Movement blocked','elite-only':'Elites only','workers-only':'Workers only'},'Elites and workers transfer between centres; rural households remain in place. Births and food stress affect household population separately.'),seed],
   run:v=>({current:AngkorRelocation.run(v),closed:AngkorRelocation.run({...v,mobility:'closed'})}),
   view({current,closed}){return{heading:'Share of elites remaining at the old centre',metrics:[metric('Elite households remaining',pct(current.finalEliteShare),'Share of the fixed elite population'),metric('Old farming population retained',pct(current.oldRuralRetained),'Final population divided by its own peak'),metric('Old residential core retained',pct(current.oldCoreRetained),'Residents and elites; final divided by own peak'),metric('Water condition vs blocked movement',signed(100*(current.oldWater-closed.oldWater))+' pp','Same controls and weather, movement blocked')],lines:[line('Movement under selected rule',series(current.rows,r=>100*r.oldEliteShare)),line('Movement blocked',series(closed.rows,r=>100*r.oldEliteShare),'reference')],axis:v=>number(v)+'%',note:'Elapsed model years, without historical dates. The old centre starts with 80% of elite households. Food is produced and accounted for at both sites. Leaving transfers people; it does not make them disappear. Persistent departure means fewer than 40% of elites remain for ten consecutive years.'};},
   evidence:[evidence('Mechanism · Exit and continuing settlement','Elite presence affects collection and central maintenance resources. Local repair can continue from farm surpluses. Recurring construction commitments can also shrink after departure, so water condition need not worsen. Whether the court leaves depends on the coordination multiplier: with the default 1 no elite exit occurs in 32 drought seeds at outside advantage 1.2, and with the old 5^0.227 all 32 do.'),evidence('Declared assumptions · Outside options','Utility combines provisioning and water condition. Portability reduces the loss of place-bound assets. The second centre’s market and drought advantages are scenario inputs, not inferred historical parameters.'),evidence('Historical comparison · Koh Ker','Hall, Penny and Hamilton (2018) found continued occupation and land use for centuries after the royal court left Koh Ker. That constrains the question; it does not calibrate the rates in this simulation.'),evidence('Limit · Testing an exit hypothesis','Elite households form a fixed stock; ordinary households can grow or shrink. Rural households cannot relocate in this version. Utilities, movement rates and the ten-year departure criterion are assumptions. No historical fit score is claimed.',true)],links:[['Published provisioning paper','https://doi.org/10.1007/s10816-021-09535-5'],['Relocation methods and matched results','research/relocation.html'],['All relocation comparisons · CSV','research/relocation-results.csv'],['Koh Ker occupation study','https://doi.org/10.1371/journal.pone.0203962'],['Inspect the relocation engine','engines/relocation.js']],csv(run){const keys=Object.keys(run.current.rows[0]);return[keys.join(','),...run.current.rows.map(r=>keys.map(k=>r[k]).join(','))].join('\n');}};

  const petri={id:'petri',nav:'Angkor · Provisioning Petri lab',title:'Can a provisioning economy rise and decline?',meta:'ATLAS DYNAMIC EXTENSION · PAPER-INSPIRED · EXPLORATORY',question:'A separate synthetic economy builds fields, waterworks and monuments, then faces a declared climate scenario. Remove one mechanism and compare matched runs.',version:'Atlas Provisioning Petri v0.1',engines:['petri.js'],defaults:AngkorPetri.defaults,
   controls:[select('scenario','Climate scenario',{stable:'Stable climate',drought:'Two imposed drought episodes'},'Droughts occupy model years 150–174 and 190–204 at 62% of ordinary conditions. These are synthetic tests, not dated reconstructions.'),select('knockout','Remove a mechanism',{none:'All mechanisms',coordination:'Remove coordination gain (no effect at the default multiplier 1)',water:'Remove hydraulic dependence',transport:'Remove transport losses',relief:'Remove household relief',temple:'Remove recurring temple obligations'},'Each removal changes one declared rule. Matched random seeds keep weather noise comparable.'),range('maintenance','Treasury share offered to maintenance',0,1,.05,pct,'Maintenance competes with storage, reclamation and building after court provisioning and ritual obligations.'),range('extraction','Harvest collected by the temple-centre system',0,.5,.025,pct,'Gross collection is an Atlas assumption. Collected food can support the core, reserves and public commitments.'),range('relief','Eligibility for reserve relief',0,1,.1,pct,'Share of a household food shortfall eligible for available stored food. This is a hypothesis, not an attested Angkor rule.'),seed],
   run:v=>AngkorPetri.run(v),view(current,base){return{heading:'Population and political core · synthetic units',metrics:[metric('Peak population index',number(current.peak/.175*100,1),'Initial population = 100'),metric('Final population retained',pct(current.retained),'Final population divided by its own peak'),metric('Accumulated food shortfall',number(current.gap,3),'Normalized person-year food units')],lines:[line('Regional population',series(current.rows,r=>r.population/.175*100)),line('Residential core',series(current.rows,r=>r.core/.175*100),'alternate'),line('Reference population',series(base.rows,r=>r.population/.175*100),'reference')],axis:v=>number(v),note:'Model years are elapsed time, not calendar dates. All food and population quantities are normalized. The baseline uses the reference controls with the same seed. The source page reports matched knockout runs and grain-ledger checks.'};},
   evidence:[evidence('Published input · Coordination','The exponent 1.227 from Klassen, Ortman, Lobo and Evans (2022, Table 5) is a size association between communities of 500 and 100 people. It is not a measured productivity effect: the paper builds output as population × land × reservoir volume, so the exponent exceeds 1 only because larger communities were assigned more land and water per person. The default coordination multiplier is 1, so the association has no causal effect unless the multiplier is raised. The old base-5 value 5^0.227 (about 1.44) and a midpoint (about 1.20) are sensitivities.'),evidence('Atlas extension · Dynamic accounts','Growth, migration, finite stores, storage loss, gross extraction, maintenance, reclamation and recurring temple costs are added rules. Their rates are illustrative and uncalibrated.'),evidence('Open test · Rise and decline','The model is a mechanism test. It has no historical fit score and no claim to identify the cause of Angkor’s decline. Removing water dependence also removes its productivity penalty; removing transport losses makes transfers costless.',true)],links:[['Published provisioning paper','https://doi.org/10.1007/s10816-021-09535-5'],['Economy, charter states and model cookbook','research/provisioning.html'],['Petri knockout results · CSV','research/petri-results.csv'],['Inspect the Petri engine','engines/petri.js']],csv(run){const keys=Object.keys(run.rows[0]);return[keys.join(','),...run.rows.map(r=>keys.map(k=>r[k]).join(','))].join('\n');}};

  const provisioning = {
    id:'provisioning',nav:'Angkor · Temple communities',title:'How did temple communities provision a city?',
    meta:'PUBLISHED ECONOMIC ACCOUNT · KLASSEN, ORTMAN, LOBO & EVANS',
    question:'Explore the paper’s community-scale and distance relationships. Output is an archaeological production index, with a separate historical sample showing settlement buildup.',
    version:'Atlas Provisioning v0.1 · normalized published relationships',engines:['provisioning.js'],defaults:AngkorProvisioning.defaults,
    controls:[range('community','People per temple community',100,1000,25,v=>number(v),'Regroup the same illustrative 10,000 people. This is a structural comparison, not a measured policy effect.'),
      select('scaling','Community scaling rule',{fitted:'Published fitted exponent · 1.227',theory:'Settlement scaling theory · 7/6',linear:'Constant output per person · 1'},'Compare the published association with the theoretical exponent and a constant-productivity comparator.'),
      range('distance','Straight-line distance from Bayon',1,40,1,v=>number(v)+' km','Uses the separate log–log distance regressions in Table 5. The two panels are not multiplied into a joint production function.')],
    run:v=>AngkorProvisioning.run(v),
    view(current,base){return{
      heading:'Output per person · 100 people per community = 100',
      metrics:[metric('Selected community output per person',number(current.perPersonIndex,1),'Normalized index; total population held fixed'),
        metric('Output per hectare at selected distance',number(current.distanceOutput,1),'Separate association · 10 km = 100'),
        metric('Water storage per hectare',number(current.distanceWater,1),'Separate association · 10 km = 100'),
        metric('Land area per person',number(current.distanceArea,1),'Separate association · 10 km = 100')],
      lines:[line('Selected community',[[current.controls.community,current.perPersonIndex]],'observed'),line('Selected scaling relationship',series(current.sizeCurve,r=>r.index)),line('Constant output per person',current.sizeCurve.map(r=>[r.year,100]),'reference')],axis:v=>number(v),
      note:'Horizontal axis: people per temple community. The curve compares group sizes while holding total population fixed. Distance cards show separate fitted associations. These indices do not measure rice tonnes or prove a causal gain from consolidation.'};},
    evidence:[
      evidence('Published model · Coordination and distance','The paper applies settlement scaling theory and spatial equilibrium to temple communities. Table 5 reports an output–population exponent of 1.227 (SE 0.023). Its theoretical comparator is 7/6. Output is not measured: it is population × land × reservoir volume. The exponent is therefore 1 plus the rate at which land and water rise with population, not output per farmer.'),
      evidence('Constructed measure · Agricultural output','The authors multiply proxies for labour, land and irrigation inputs. Labour is also used as the predictor. This is a constructed production index, not an independent harvest measurement.'),
      evidence('Historical sample · Buildup','Table 4B records 93 to 571 inhabited communities and 24,894 to 213,521 associated people across six periods. These are the complete-data sample under continuous occupation assumptions, not Greater Angkor’s total population.'),
      evidence('Open question · Who received the surplus?','The paper leaves elite extraction versus shared prosperity unresolved. Temple-platform volume is a proxy for net proceeds. Its 0.085 log–log coefficient is an elasticity; this implementation does not treat it as a tax rate.'),
      evidence('Separate hypothesis · Famine insurance','Redistributing stored food to households in bad years would require evidence or declared assumptions about reserves, access, losses and obligations. The paper supplies no calibrated famine-insurance rule.',true)
    ],links:[['Published provisioning paper','https://doi.org/10.1007/s10816-021-09535-5'],['Economy, charter states and model cookbook','research/provisioning.html'],['Published sample chronology · CSV','research/provisioning-periods.csv'],['Inspect the provisioning engine','engines/provisioning.js']],
    csv(run){const keys=['begin','end','communities','population','areaKm2'];return[keys.join(','),...run.periods.map(r=>keys.map(k=>r[k]).join(','))].join('\n');}
  };

  const monsoon = {
    id: 'monsoon', nav: 'Angkor · Monsoon account', title: 'Can monsoon history explain the decline?',
    meta: 'ANGKOR · LITERATURE ACCOUNT 01 · LIEBERMAN & BUCKLEY',
    question: 'The published climate sequence drives an Atlas model of population and upkeep. Compare it with the same parameter draw under neutral climate after 1250.',
    version: 'Atlas Monsoon Account v0.1', engines: ['monsoon.js'],
    defaults: AngkorMonsoon.defaults,
    controls: [
      range('sensitivity', 'Crop response to each PDSI unit', .04, .10, .03, v => number(v, 2), 'No published per-PDSI coefficient for rainfed rice in Cambodia, Thailand or Laos was found (inputs/other_sources.json, item C). The tested sensitivities 0.04, 0.07 and 0.10 are unsourced judgement values, and they decide the monsoon result: at 0 no draw of 2000 shows an onset decline, while 217, 1260 and 1657 draws decline at 0.04, 0.07 and 0.10. Weather response is capped at 0.4–1.15 before buffering.'),
      {key:'draw',label:'Parameter draw',type:'number',min:1,max:2000,note:'Pick one of the same 2,000 parameter draws used in the review results.'}
    ],
    run: values => AngkorMonsoon.run(values),
    view(run) {
      const at1300 = run.current.find(r=>r.year===1300).core;
      const ref1300 = run.reference.find(r=>r.year===1300).core;
      return {
        heading: 'Core activity index · 1300 = 100 in each run',
        metrics: [
          metric('Sustained decline', number(run.summary.declines) + '/2,000', 'Across the stored matched parameter draws'),
          metric('Median onset among declines', run.summary.medianOnset ?? 'None', '15-year sustained drop below the scoring baseline'),
          metric('Core activity in 1450', number(100*run.summary.coreRatio,1), 'Median index relative to 1300')
        ],
        lines: [line('Published monsoon sequence',series(run.current,r=>100*r.core/at1300)),
          line('Neutral climate after 1250',series(run.reference,r=>100*r.core/ref1300),'reference')],
        axis:v=>number(v),
        note:'The chart reruns one parameter draw in your browser. Cards summarize 2,000 completed runs at the selected crop sensitivity. The older engine defines core activity as court presence × regional population. It does not simulate residents moving out of the core.'
      };
    },
    evidence: [
      evidence('Published account · Rise and decline', 'Lieberman and Buckley (2012) argue that monsoon fluctuations contributed to the formation and collapse of early mainland kingdoms. Their later comparison proposes both smaller hydrological fluctuations and new sources of state power.'),
      evidence('Observed proxy · Annual PDSI', 'Buckley and colleagues’ NOAA archive provides regional March–May drought estimates from Vietnamese tree rings. This run uses the 201 annual values from 1250 to 1450. The proxy is not local rainfall or a Tonle Sap flow series.'),
      evidence('Atlas contribution · Executable comparison', 'We map PDSI into agricultural conditions in the existing Atlas long-run engine and run a neutral-climate comparison. All six dated historical-driver switches are off. The published papers do not provide this social model.'),
      evidence('Open test · Buildup and chronology', 'Weather before 1250 is the existing synthetic initialization. This run does not test the early rise using observed annual climate. Harvest translation, infrastructure rules and the core-activity proxy are assumptions.', true)
    ],
    links: [['Read the account, equations and results','research/monsoon.html'],
      ['Lieberman & Buckley 2012','https://www.cambridge.org/core/journals/modern-asian-studies/article/abs/impact-of-climate-on-southeast-asia-circa-9501820-new-findings/4EA47A9F9791A563B829EE6ACABAAC66'],
      ['Buckley et al. 2010','https://doi.org/10.1073/pnas.0910827107'],
      ['Published climate subset CSV','research/buckley/buckley-1250-1450.csv'],
      ['All 8,000 review runs CSV','research/buckley/results.csv'],
      ['Inspect the browser implementation','engines/monsoon.js']],
    csv(run) {
      const rows=[...run.current.map(r=>({scenario:'published_climate',...r})),
        ...run.reference.map(r=>({scenario:'neutral',...r}))];
      const keys=Object.keys(rows[0]);
      return [keys.join(','),...rows.map(row=>keys.map(key=>row[key]).join(','))].join('\n');
    }
  };
  // Planning Lab tools ported from the full Atlas (same inputs, defaults and engine calls).
  const sumOf = a => a.reduce((s, x) => s + x, 0);
  const money = v => Math.abs(v) >= 1e9 ? number(v / 1e9, 2) + 'bn' : number(v / 1e6, 0) + 'm';
  const planningSource = method => evidence('Method · ' + method[0], method[1]);

  const cohortWorld = {
    id: 'cohort', nav: 'Planning · Reconstructed cohort', title: 'How many entrants finish primary school?',
    meta: 'PLANNING TOOL 02 · FLOWS AND INTERNAL EFFICIENCY', question: 'How do repetition and dropout change how many of 1,000 entrants graduate, and how many pupil-years each graduate costs?',
    version: 'Atlas of Education 0.11.2 · Planning Lab reconstructed cohort', engines: ['lab_models.js'],
    defaults: {rep1: .18, repLater: .07, drop1: .08, dropLater: .05, maxRep: 3},
    controls: [
      range('rep1', 'Repetition in Grade 1', 0, .4, .01, pct, 'Share of Grade 1 pupils who repeat the grade.'),
      range('repLater', 'Repetition in later grades', 0, .3, .01, pct, 'Applied to Grades 2–6.'),
      range('drop1', 'Dropout in Grade 1', 0, .3, .01, pct, 'Share of Grade 1 pupils who leave school that year.'),
      range('dropLater', 'Dropout in later grades', 0, .2, .005, pct, 'Applied to Grades 2–6.'),
      range('maxRep', 'Repetitions allowed per grade', 0, 5, 1, v => number(v), 'Pupils who exceed the limit leave school (UIS convention).')
    ],
    run(v) {
      const n = 6, r = Array.from({length: n}, (_, g) => g ? v.repLater : v.rep1), d = Array.from({length: n}, (_, g) => g ? v.dropLater : v.drop1);
      const p = r.map((x, g) => Math.max(0, 1 - x - d[g]));
      const c = AtlasLab.cohort(p, r, {maxRep: v.maxRep});
      return {parameters: {...v, grades: n, size: 1000}, reach: c.reach, graduates: c.graduates, survival: c.survival,
        yearsPerGraduate: c.yearsPerGraduate, efficiency: c.coefficientOfEfficiency, wasted: c.wastedShare, balance: c.balance};
    },
    view(current, base) {
      const pts = run => run.reach.map((x, g) => [g + 1, x]).concat([[7, run.graduates]]);
      return {
        heading: 'Pupils of 1,000 entrants reaching each grade',
        metrics: [
          metric('Graduate', number(current.graduates), 'Of 1,000 entrants'),
          metric('Pupil-years per graduate', number(current.yearsPerGraduate, 1), 'Against 6 for no wastage'),
          metric('Coefficient of efficiency', pct(current.efficiency), 'Graduates × 6 ÷ pupil-years used'),
          metric('Pupil-years wasted', pct(current.wasted), 'Used by repeaters and dropouts'),
          metric('Reach the last grade', pct(current.survival.at(-1)), 'Survival rate to Grade 6')
        ],
        lines: [line('Current flow rates', pts(current)), line('Reference flow rates', pts(base), 'reference')],
        xTitle: 'Grade reached (7 = graduated)', yZero: true,
        axis: v => number(v),
        note: 'Constant flow rates; no re-entry, transfer or migration. Flow rates derived from enrolment data inherit any misreporting of repeaters.'
      };
    },
    evidence: [
      planningSource(['Reconstructed cohort', 'UIS reconstructed cohort method and IIEP planning training material. The cohort follows 1,000 entrants grade by grade with constant promotion, repetition and dropout rates.']),
      evidence('Assumed · Demo flow rates', 'The reference rates are stylised. Replace them with rates derived from two years of enrolment and repeater counts.'),
      evidence('Limit · No re-entry', 'Pupils who leave never return, and transfers and migration are ignored. Real systems with re-entry waste fewer pupil-years than this cohort shows.', true)
    ], links: [education]
  };

  const demoPop = growth => (t, age) => 400000 * Math.pow(1 + growth, t - (age - 6));
  const sectorWorld = {
    id: 'sector', nav: 'Planning · Sector simulation', title: 'Can the budget pay for the plan?',
    meta: 'PLANNING TOOL 03 · POPULATION AND ENROLMENT · 2025–2045', question: 'What teachers, classrooms and money do intake, repetition and dropout targets imply, and what is left unfunded?',
    version: 'Atlas of Education 0.11.2 · Planning Lab sector simulation', engines: ['lab_models.js'],
    defaults: {intakeT: 1, repT: .03, dropT: .01, ptrT: 40, salaryT: 3.5, growth: .05, eduShare: .15, popGrowth: 0},
    controls: [
      range('intakeT', 'Target gross intake rate', .8, 1.2, .01, pct, 'New Grade 1 entrants as a share of six-year-olds, reached by 2035.'),
      range('repT', 'Target repetition', 0, .2, .01, pct, 'Today 9%; moves to the target by 2035.'),
      range('dropT', 'Target dropout', 0, .1, .005, pct, 'Today 5%; moves to the target by 2035.'),
      range('ptrT', 'Target pupils per teacher', 25, 60, 1, v => number(v), 'Today 45 pupils per teacher.'),
      range('salaryT', 'Teacher salary (× GDP per capita)', 1.5, 7, .1, v => number(v, 1) + '×', 'Today 3.2 times GDP per capita.'),
      range('growth', 'Real GDP growth', 0, .1, .005, pct, 'Sets the resource envelope from the macro-fiscal frame.'),
      range('eduShare', 'Education share of public spending', .08, .25, .005, pct, 'Primary receives 45% of the education budget.'),
      range('popGrowth', 'Cohort growth', -.03, .03, .005, pct, 'Annual change in the size of each new school-age cohort.')
    ],
    run(v) {
      const S = AtlasLab.sectorSimulation({grades: 6, years: 21, E0: [470e3, 400e3, 370e3, 345e3, 320e3, 300e3], rooms0: 42000, gdp0: 4e10,
        popAge: demoPop(v.popGrowth), population: t => 1.7e7 * Math.pow(1 + v.popGrowth * .6, t), entryAge: 6,
        intake0: .92, intakeT: v.intakeT, rep0: .09, repT: v.repT, drop0: .05, dropT: v.dropT, ptr0: 45, ptrT: v.ptrT, salary0: 3.2, salaryT: v.salaryT,
        nonsal0: .18, nonsalT: .22, targetYear: 10, classSize: 45, shifts: 1, roomCost: 6, revenue: .19, eduShare: v.eduShare, primaryShare: .45,
        growth: v.growth, startYear: 2025});
      return {parameters: v, rows: S.rows.map(r => ({year: r.year, pupils: r.pupils, ger: r.ger, teachers: r.teachers, newRooms: r.newRooms,
        recurrent: r.recurrent, capital: r.capital, cost: r.cost, resources: r.resources, gap: r.gap, completion: r.completionRate, unitCost: r.unitCostShareGDPpc})),
        pupilBalance: Math.max(...S.pupilBalance.map(Math.abs))};
    },
    view({rows}, base) {
      const r10 = rows[10], first = rows[0];
      return {
        heading: 'Cost of the plan and resources for primary',
        metrics: [
          metric('Financing gap, 2035', (r10.gap < 0 ? '−' : '') + money(Math.abs(r10.gap)), 'Cost minus resources; negative is a surplus'),
          metric('Share of cost unfunded, 2035', pct(Math.max(0, r10.gap) / r10.cost), 'Gap ÷ total cost'),
          metric('Primary completion, 2035', pct(r10.completion), 'Completers ÷ population of completion age'),
          metric('Gross enrolment ratio, 2035', pct(r10.ger), 'Pupils ÷ population of primary age'),
          metric('Teachers needed, 2035', number(r10.teachers), 'Pupils ÷ target ratio'),
          metric('Change in teachers since 2025', signed(r10.teachers - first.teachers, 0), 'Teachers'),
          metric('Unit cost, 2035', pct(r10.unitCost), 'Of GDP per capita, per pupil'),
          metric('New classrooms by 2035', number(sumOf(rows.slice(0, 11).map(r => r.newRooms))), 'Built to keep 45 pupils per room')
        ],
        lines: [line('Total cost', series(rows, r => r.cost)), line('Reference total cost', series(base.rows, r => r.cost), 'reference'),
          line('Resources for primary', series(rows, r => r.resources), 'alternate')],
        axis: money,
        note: 'Currency units of a stylised country. A plan that cannot be financed still runs: the gap is the warning, never clipped to the budget. Pupils are conserved every year.'
      };
    },
    evidence: [
      planningSource(['Sector simulation', 'UNESCO EPSSim and IIEP sector-simulation practice. Targets are interpolated to 2035; resources come from GDP, revenue and the education share.']),
      evidence('Assumed · Stylised country', 'Enrolment, classrooms, GDP, salaries and the non-salary share describe a demo country of 17 million people, not a real system.'),
      evidence('Limit · One level, one region', 'Only primary education is simulated, with no regional detail. This is not a replication of the EPSSim workbooks.', true)
    ], links: [education]
  };

  const schoolMapWorld = {
    id: 'schoolmap', nav: 'Planning · School mapping', title: 'Where should the next schools go?',
    meta: 'PLANNING TOOL 04 · ACCESS AND PLACES', question: 'How far do children walk as new schools are added, and does building in the largest villages do as well as choosing sites carefully?',
    version: 'Atlas of Education 0.11.2 · Planning Lab school mapping', engines: ['lab_models.js'],
    defaults: {add: 4, rule: 'greedy', maxKm: 3},
    controls: [
      range('add', 'New schools', 0, 12, 1, v => number(v), 'Schools added one at a time to the existing school.'),
      select('rule', 'Siting rule', {greedy: 'Least total walking', largest: 'Largest village'}, 'Least total walking is a greedy p-median rule; the alternative builds in the largest unserved village.'),
      range('maxKm', 'Acceptable walk', 1, 6, .5, v => number(v, 1) + ' km', 'Children living farther than this from a school count as poorly served.')
    ],
    run(v) {
      const M = AtlasLab.schoolMap({add: v.add, maxKm: v.maxKm, rule: v.rule});
      return {parameters: v, history: M.history.map((h, k) => ({schools: k, mean: h.mean, beyond: h.beyond})),
        children: sumOf(M.villages.map(x => x.kids)), villages: M.villages.length};
    },
    view(current, base) {
      const h = current.history, last = h.at(-1);
      return {
        heading: 'Average walk to the nearest school',
        metrics: [
          metric('Mean walk', number(last.mean, 2) + ' km', 'To the nearest school'),
          metric('Children beyond the acceptable walk', pct(last.beyond), 'Share of all children'),
          metric('Mean walk before new schools', number(h[0].mean, 2) + ' km', 'One existing school'),
          metric('Schools', number(h.length), 'Including the existing school'),
          metric('Children in the district', number(current.children), 'In sixty villages')
        ],
        lines: [line('Current siting', h.map(x => [x.schools, x.mean])), line('Reference siting', base.history.map(x => [x.schools, x.mean]), 'reference')],
        xTitle: 'New schools built', yZero: true,
        axis: v => number(v, 1) + ' km',
        note: 'Sixty synthetic villages in four clusters, one existing school. Straight-line distance; rivers, roads, school size and safety are ignored.'
      };
    },
    evidence: [
      planningSource(['School mapping', 'IIEP school mapping and micro-planning (Hallak 1977; Caillods) with a Teitz–Bart greedy location-allocation rule. Adding a school never lengthens any child’s walk.']),
      evidence('Assumed · Synthetic district', 'Village locations and numbers of children are generated from a fixed seed. Real micro-planning starts from a census of villages and roads.'),
      evidence('Limit · Distance only', 'Capacity, school size, safety, terrain and the cost of each site are ignored, so the best site here may be unbuildable.', true)
    ], links: [education]
  };

  const laysWorld = {
    id: 'lays', nav: 'Planning · Learning-adjusted years', title: 'Are years in school years of learning?',
    meta: 'PLANNING TOOL 05 · LEARNING AND TARGETS', question: 'How many years of schooling turn into years of learning, and how many children cannot read with comprehension?',
    version: 'Atlas of Education 0.11.2 · Planning Lab learning-adjusted years', engines: ['lab_models.js'],
    defaults: {hlo: 450, eys: 9.5, oos: .08, bmp: .3},
    controls: [
      range('hlo', 'Harmonised test score', 300, 625, 5, v => number(v), 'Harmonised learning outcomes on the 300–625 scale; 625 is the benchmark of full learning.'),
      range('eys', 'Expected years of schooling', 4, 14, .1, v => number(v, 1), 'Years a child entering school today can expect to complete.'),
      range('oos', 'Out of school at end-primary age', 0, .5, .01, pct, 'Counted as not proficient in learning poverty.'),
      range('bmp', 'Pupils reading at minimum proficiency', 0, 1, .01, pct, 'Share of pupils at the end of primary who read with comprehension.')
    ],
    run(v) {
      const A = AtlasLab.learningAdjusted(v);
      const curve = Array.from({length: 11}, (_, i) => { const eys = 4 + i; return [eys, AtlasLab.learningAdjusted({...v, eys}).lays]; });
      return {parameters: v, lays: A.lays, lostYears: A.lostYears, learningPoverty: A.learningPoverty, curve};
    },
    view(current, base) {
      const v = current.parameters;
      return {
        heading: 'Learning-adjusted years at each length of schooling',
        metrics: [
          metric('Learning-adjusted years', number(current.lays, 1), 'Expected years × score ÷ 625'),
          metric('Years lost to low learning', number(current.lostYears, 1), 'Expected minus learning-adjusted years'),
          metric('Learning poverty', pct(current.learningPoverty), 'Cannot read with comprehension at age 10'),
          metric('Gain from +50 test points', number(v.eys * 50 / 625, 2) + ' yr', 'With the same years in school')
        ],
        lines: [line('Current test score', current.curve), line('Reference test score', base.curve, 'reference'),
          line('Selected system', [[v.eys, current.lays]], 'observed')],
        xTitle: 'Expected years of schooling', yZero: true,
        axis: v => number(v, 1) + ' yr',
        note: 'Each year in school counts as test score ÷ 625 of a year of learning. The dot marks the selected system. Learning poverty uses end-of-primary reading, not secondary.'
      };
    },
    evidence: [
      planningSource(['Learning-adjusted years', 'World Bank Human Capital Index (LAYS) and the learning-poverty indicator: LAYS = expected years × test score ÷ 625.']),
      evidence('Observed · Cambodia comparison', 'Cambodia’s PISA for Development (2017) found 8% of 15-year-olds at minimum reading proficiency and 10% in mathematics, a different age and test from learning poverty.'),
      evidence('Limit · A convention', 'The 625 benchmark is a convention and harmonised scores combine different tests with error. LAYS ranks systems; it does not measure what a child knows.', true)
    ], links: [education]
  };

  const absorptionWorld = {
    id: 'absorption', nav: 'Planning · Graduate absorption', title: 'Can the economy absorb its graduates?',
    meta: 'PLANNING TOOL 06 · WORK AND EXTERNAL EFFICIENCY · 2025–2045', question: 'Do graduate-job openings keep pace with graduates, and how long does the queue of the unabsorbed grow?',
    version: 'Atlas of Education 0.11.2 · Planning Lab graduate absorption', engines: ['lab_models.js'],
    defaults: {gradGrowth: .05, gdpGrowth: .05, elasticity: .4, skillShift: .01, clear: .4},
    controls: [
      range('gradGrowth', 'Growth in graduates a year', -.02, .12, .005, pct, 'Starts from 90,000 graduates in 2025.'),
      range('gdpGrowth', 'GDP growth', 0, .1, .005, pct, 'Output growth creates graduate jobs through the employment elasticity.'),
      range('elasticity', 'Employment elasticity of growth', 0, 1, .05, v => number(v, 2), 'Percentage growth in graduate jobs for each percentage point of GDP growth.'),
      range('skillShift', 'Shift toward graduate jobs a year', 0, .05, .005, pct, 'Technological or structural change that adds graduate jobs beyond growth.'),
      range('clear', 'Share of the queue clearing each year', .1, 1, .05, pct, 'Unabsorbed graduates leave the queue for other work, migration or inactivity.')
    ],
    run(v) {
      const rows = AtlasLab.absorption({years: 21, jobs0: 1e6, grads0: 9e4, replacement: .03, queue0: 0, startYear: 2025, ...v});
      return {parameters: v, rows};
    },
    view({rows}, base) {
      const first = rows[0], last = rows.at(-1);
      return {
        heading: 'Graduates, graduate-job openings and the queue',
        metrics: [
          metric('Openings per graduate, 2045', number(last.ratio, 2), 'Below 1, graduates outnumber openings'),
          metric('Queue, 2045', number(last.queue), 'People waiting for a graduate job'),
          metric('Queue in years of graduates', number(last.queue / last.grads, 1), 'Queue ÷ graduates that year'),
          metric('Openings per graduate, 2025', number(first.ratio, 2), 'Starting balance'),
          metric('Graduate jobs, 2045', number(last.jobs), 'From one million in 2025'),
          metric('Graduates, 2045', number(last.grads), 'A year')
        ],
        lines: [line('Queue', series(rows, r => r.queue)), line('Reference queue', series(base.rows, r => r.queue), 'reference'),
          line('Graduates', series(rows, r => r.grads), 'alternate'), line('Graduate-job openings', series(rows, r => r.openings), 'contrast')],
        axis: v => number(v / 1000, 0) + 'k',
        note: 'People. A reduced-form balance with no wages and no firm choices. The China graduate-queue world is the version in which firms choose vacancies.'
      };
    },
    evidence: [
      planningSource(['Graduate absorption', 'Education sector analysis guidelines on external efficiency, with Harris and Todaro’s queue logic: openings come from replacement and job growth.']),
      evidence('Assumed · Stylised economy', 'One million graduate jobs, 3% annual replacement and 90,000 graduates in 2025 describe a demo economy.'),
      evidence('Limit · The planner’s balance sheet', 'Wages, firms’ hiring choices and credential competition are absent. Use the China graduate-queue world to see those mechanisms.', true)
    ], links: [education, ['China graduate-queue world', '#china']]
  };

  return {worlds: [china, cambodia, floor, teachers, cohortWorld, sectorWorld, schoolMapWorld, laysWorld, absorptionWorld,
    provisioning, campaign, angkorLive, signalling, obligations, monsoon, mandalaWorld, relocation, petri], sha256};
})();
