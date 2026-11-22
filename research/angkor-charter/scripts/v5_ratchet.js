// v5_ratchet.js — test of ONE mechanism, not a model of Angkor.
//
// H-endowment: the crown's fiscal base shrinks because temple endowments permanently alienate
// land and labour from taxable status, while obligations (stipends, network, defence) grow with
// the polity. Prediction: fiscal capacity peaks at an interior date with no resource ceiling,
// no climate shock, no defeat.
//
// Units: km2, t (paddy), people, years.
'use strict';

const P = {
  start: 800, end: 1600,
  A: 400, Amax: 1110,        // cultivated km2 -> planted ceiling
  y: 1.5, lossPct: 16,
  pop: 400000, riceKg: 200,
  // endowment ratchet
  endowRate: 0.0016, endowMax: 0.90,
  // elite
  elite0: 6000, stipendT: 0.35, eliteGrow: 0.004,
  // crown
  taxRate: 0.10,
  // network
  km0: 40, kmPer1000T: 14, pdPerKm: 3000, pdToT: 1 / 180,
  // defence
  defShare: 0.18,
  // land expansion
  expandRate: 0.010
};

function run(over) {
  const p = Object.assign({}, P, over || {});
  let A = p.A, e = 0.02, E = p.elite0, pop = p.pop, km = p.km0;
  let charter = 0.6, peakRev = 0, yrPeak = 0, crossYear = 0, peakCoverYear = 0, bestCover = 0;
  const rows = [];

  for (let yr = p.start; yr <= p.end; yr++) {
    const prod = A * 100 * p.y * (1 - p.lossPct / 100);
    const demand = pop * p.riceKg / 1000;

    // land expansion: population pressure against the complex's ceiling
    const carrying = (p.Amax * 100 * p.y * (1 - p.lossPct / 100)) / (p.riceKg / 1000);
    const pressure = pop / carrying;
    if (A < p.Amax && pressure > 0.25) A = Math.min(p.Amax, A * (1 + p.expandRate * (1 - pressure)));

    // the ratchet: endowment share only rises
    e = Math.min(p.endowMax, e + p.endowRate * (0.4 + charter));

    // revenue on the non-alienated share
    const taxable = A * (1 - e);
    const revenue = taxable * 100 * p.y * (1 - p.lossPct / 100) * p.taxRate;

    // obligations
    const stipends = E * p.stipendT;
    const network = km * p.pdPerKm * p.pdToT;
    const defence = revenue * p.defShare;
    const obligations = stipends + network + defence;
    const cover = revenue / Math.max(1, obligations);

    // network follows revenue with a lag
    km += (p.km0 + revenue * p.kmPer1000T / 1000 - km) * 0.03;

    // elite overproduction while the stipend is affordable
    if (revenue / Math.max(1, E) > p.stipendT * 1.25) E *= (1 + p.eliteGrow);

    // charter: earned by solvency, lost by insolvency
    charter = Math.max(0, Math.min(1, charter + (cover > 1 ? 0.0025 : -0.004)));

    // population
    let g = 0.006 * (1 - pressure);
    if (prod < demand) g -= 0.008 * Math.min(1, (demand - prod) / Math.max(1, demand));
    pop = Math.max(30000, pop * (1 + g));

    if (revenue > peakRev) { peakRev = revenue; yrPeak = yr; }
    if (cover > bestCover) { bestCover = cover; peakCoverYear = yr; }
    if (!crossYear && yr > p.start + 60 && cover < 1) crossYear = yr;

    rows.push({ yr, A: Math.round(A), e: +e.toFixed(3), revenue: Math.round(revenue),
      obligations: Math.round(obligations), cover: +cover.toFixed(2), E: Math.round(E),
      pop: Math.round(pop), km: Math.round(km), charter: +charter.toFixed(2) });
  }
  const last = rows[rows.length - 1];
  return { rows, peakRev: Math.round(peakRev), yrPeak, peakCoverYear, bestCover: +bestCover.toFixed(2),
    crossYear, endRev: last.revenue, endObl: last.obligations, endE: last.e, endCharter: last.charter };
}

if (require.main === module) {
  const r = run();
  console.log('fiscal peak', r.peakRev, 't at', r.yrPeak, '| best solvency', r.bestCover, 'at', r.peakCoverYear);
  console.log('crossover (revenue<obligations) at', r.crossYear || 'never', '| end rev', r.endRev, 'obl', r.endObl, 'endow', r.endE);
  console.log('\nyear   land  endow revenue oblig cover  elites     pop   km  charter');
  r.rows.filter((x, i) => i % 40 === 0).forEach(x => console.log(
    String(x.yr).padEnd(6), String(x.A).padStart(5), String(x.e).padStart(6),
    String(x.revenue).padStart(7), String(x.obligations).padStart(5), String(x.cover).padStart(5),
    String(x.E).padStart(7), String(x.pop).padStart(7), String(x.km).padStart(4), String(x.charter).padStart(5)));
}
module.exports = { run, P };
