/* Atlas formalization of Lieberman & Buckley's climate account.
 * NOAA data provide PDSI for 1250–1450. Crop translation and social rules are Atlas assumptions. */
'use strict';
globalThis.AngkorMonsoon = (() => {
const pdsi = {"1250": -1.423, "1251": -1.53, "1252": -0.14, "1253": 1.947, "1254": 1.02, "1255": 0.117, "1256": 0.713, "1257": 4.794, "1258": 6.657, "1259": 2.717, "1260": 0.308, "1261": -0.098, "1262": 1.102, "1263": 1.533, "1264": 0.746, "1265": 0.655, "1266": 0.846, "1267": -1.348, "1268": 0.316, "1269": 2.634, "1270": -0.942, "1271": -1.911, "1272": -0.355, "1273": 1.276, "1274": 3.577, "1275": 4.24, "1276": 3.486, "1277": 3.031, "1278": 2.841, "1279": 3.619, "1280": 3.073, "1281": 0.208, "1282": 0.829, "1283": 3.445, "1284": 1.93, "1285": 0.581, "1286": 0.539, "1287": 0.821, "1288": 2.741, "1289": 2.038, "1290": -0.346, "1291": -1.0, "1292": 0.349, "1293": 0.225, "1294": -1.257, "1295": -1.497, "1296": 0.183, "1297": 0.407, "1298": 1.392, "1299": 2.799, "1300": 0.647, "1301": -0.942, "1302": -1.009, "1303": 0.771, "1304": -0.495, "1305": -2.267, "1306": -0.86, "1307": 1.417, "1308": 0.564, "1309": -3.74, "1310": -2.027, "1311": 0.97, "1312": 0.564, "1313": -1.265, "1314": -0.694, "1315": 2.907, "1316": 5.158, "1317": 2.27, "1318": -0.719, "1319": 0.879, "1320": -1.497, "1321": -0.314, "1322": 4.198, "1323": 2.328, "1324": 0.225, "1325": -2.416, "1326": -4.841, "1327": -4.237, "1328": -2.383, "1329": -1.166, "1330": -0.471, "1331": -0.76, "1332": -1.075, "1333": 0.572, "1334": 2.336, "1335": 4.745, "1336": 3.371, "1337": -0.479, "1338": -4.047, "1339": -3.335, "1340": -1.216, "1341": -2.383, "1342": -2.722, "1343": -0.429, "1344": 0.001, "1345": -3.351, "1346": -4.891, "1347": -3.178, "1348": -1.845, "1349": -0.678, "1350": -0.975, "1351": -2.284, "1352": -1.514, "1353": -1.778, "1354": -1.936, "1355": -2.54, "1356": -2.896, "1357": -1.812, "1358": -1.447, "1359": -1.373, "1360": -1.985, "1361": -3.691, "1362": -4.75, "1363": -6.174, "1364": -3.898, "1365": -0.346, "1366": -0.247, "1367": -2.556, "1368": -1.398, "1369": 0.026, "1370": 0.332, "1371": 1.674, "1372": 0.382, "1373": -2.904, "1374": -1.953, "1375": 3.817, "1376": 4.364, "1377": 1.326, "1378": -0.048, "1379": 0.887, "1380": -1.546, "1381": -1.588, "1382": 3.039, "1383": 2.766, "1384": -0.239, "1385": -1.671, "1386": -0.496, "1387": 0.871, "1388": 0.779, "1389": 1.334, "1390": 0.945, "1391": -0.628, "1392": -1.522, "1393": -2.275, "1394": -0.852, "1395": 0.837, "1396": 0.73, "1397": 2.054, "1398": 2.717, "1399": 1.831, "1400": -0.214, "1401": -4.196, "1402": -6.878, "1403": -7.209, "1404": -5.38, "1405": -0.951, "1406": 1.135, "1407": 0.217, "1408": -2.871, "1409": -1.1, "1410": 1.847, "1411": -1.298, "1412": -1.994, "1413": 0.208, "1414": 1.193, "1415": -0.868, "1416": -4.287, "1417": -4.254, "1418": -2.126, "1419": -1.116, "1420": -1.456, "1421": -0.669, "1422": 0.051, "1423": -2.151, "1424": -5.123, "1425": -2.656, "1426": 1.086, "1427": -0.818, "1428": -0.901, "1429": 1.16, "1430": 2.559, "1431": 1.194, "1432": -0.901, "1433": 0.15, "1434": 1.185, "1435": -1.373, "1436": -3.393, "1437": -3.012, "1438": -2.706, "1439": -1.067, "1440": -0.115, "1441": -1.538, "1442": -0.636, "1443": 0.912, "1444": 1.5, "1445": 1.558, "1446": -0.851, "1447": -1.323, "1448": -0.446, "1449": 0.523, "1450": -1.571};
const summaries = {"0.00": {"n": 2000, "declines": 0, "medianOnset": null, "coreRatio": 1.007064273278183}, "0.04": {"n": 2000, "declines": 217, "medianOnset": 1402, "coreRatio": 0.9446913854592252}, "0.07": {"n": 2000, "declines": 1260, "medianOnset": 1362.0, "coreRatio": 0.8936454586418797}, "0.10": {"n": 2000, "declines": 1657, "medianOnset": 1338, "coreRatio": 0.8434980835481041}};
/* Angkor 802-1450: the standard explanations as switchable mechanisms. One step per year.
 * Background in every run: kings die (mean reign 20 years); some successions are contested,
 * and a contest cuts the labour the court can command (waxing and waning).
 * Mechanisms and the dates they take from outside evidence:
 *   war       Ayutthaya attacks 1353, 1370, 1431 (chronicle dates): people carried off, court flees.
 *   orgy      Jayavarman VII's building 1181-1218 takes labour first, and every temple built
 *             carries endowed upkeep forever after (temples were assigned villages and workers).
 *   theravada royal temple-labour claims fade: monks at Angkor 1296 (Zhou Daguan), royal Pali
 *             inscription 1308/09. Ramp centre drawn 1290-1320.
 *   trade     an outside option pulls the court south. Date NOT fixed by evidence (1150-1450).
 *   drought   dry 1335-1365 and 1400-1425 (Buckley et al. 2010).
 *   hydraulic upkeep per unit of network rises as channels silt (Groslier, Fletcher).
 * Population is a share of food-limited capacity (~590k people in the seasonal model). */
'use strict';
function makeClimateEngine(sensitivity, neutral) {
  const FIRST = 802, LAST = 1450;
  const MECH = ['war', 'orgy', 'theravada', 'trade', 'drought', 'hydraulic'];
  const fixed = Object.freeze({droughts: [[1335, 1365], [1400, 1425]], attacks: [1353, 1370, 1431],
    orgy: [1181, 1218], fieldLabour: .26});
  const rngFrom = seed => { let s = seed >>> 0; return () => ((s = (Math.imul(1664525, s) + 1013904223) >>> 0) / 4294967296); };
  const logistic = (t, mid, width) => 1 / (1 + Math.exp(-(t - mid) / width));

  function run(p, on) {
    const wr = rngFrom(p.seed), kr = rngFrom(p.seed ^ 0x9e3779b9);   // separate streams: weather, kings
    const b = p.bondedShare;
    const pool0 = p.bondedWork * b + p.corvee * (1 - b);              // court labour at baseline
    const unitNeed = pool0 / p.slack;                                  // upkeep per unit of network at baseline
    let N = .08, B = .08 * b, C = .3, E = 1, S = .088, M = 0;
    let reignLeft = 1 + Math.floor(-20 * Math.log(1 - kr())), contest = 0;
    const rows = [];
    for (let year = FIRST; year <= LAST; year++) {
      // kings: succession contests are the background waxing and waning
      if (--reignLeft <= 0) {
        reignLeft = 1 + Math.floor(-20 * Math.log(1 - kr()));
        if (kr() < p.contestProb) contest = 2 + Math.floor(kr() * 14);
      }
      const cohesion = contest > 0 ? p.contestCut : 1;
      if (contest > 0) contest--;
      // weather
      const dry = on.drought && fixed.droughts.some(([a, z]) => year >= a && year <= z);
      const originalWeather = Math.min(1.15, (dry ? p.droughtMean : 1) + p.noise * (wr() + wr() + wr() - 1.5));
      const w = year >= 1250 ? Math.max(.4, Math.min(1.15, 1 + (neutral ? 0 : pdsi[year]) * sensitivity)) : originalWeather;
      const buffered = w < 1 ? w + C * p.buffer * (1 - w) : w;
      const capacity = buffered * (1 + p.channelGain * C) / (1 + p.channelGain);
      const P0 = N + B;
      const harvest = capacity * Math.min(1, (N + .75 * B) / fixed.fieldLabour);
      const shortfall = Math.max(0, 1 - harvest / P0);
      const follow = p.follow * (1 - E);
      const growth = shortfall > 0 ? -p.famine * shortfall : p.growth * (1 - P0 / harvest);
      N = Math.max(0, N * (1 + growth - follow));
      const captives = p.attrition * b * N / (1 - b);                  // steady inflow keeps B/P ~ b
      B = Math.max(0, B * (1 - p.attrition - (shortfall > 0 ? p.famine * shortfall : 0) - follow) + captives);
      // war: attacks carry people off and drive the court out for a while
      if (on.war && fixed.attacks.includes(year)) { N *= 1 - p.warLoss; B *= 1 - 2 * p.warLoss; E *= 1 - p.warFlight; }
      // labour the court commands; Theravada erodes temple-labour claims
      const devotion = on.theravada ? 1 - (1 - p.theravadaFloor) * logistic(year, p.theravadaYear, 10) : 1;
      const pool = (p.bondedWork * B + p.corvee * E * N) * devotion * cohesion;
      // upkeep: network built for the peak, silting, and endowed temples
      S = Math.max(S, N + B);
      const silt = on.hydraulic ? 1 + p.silt * Math.max(0, year - 1000) / 100 : 1;
      const need = unitNeed * S * silt + (on.orgy ? p.templeUpkeep * M : 0);
      const inOrgy = on.orgy && year >= fixed.orgy[0] && year <= fixed.orgy[1];
      let build, upkeep;
      if (inOrgy) { build = pool * p.orgyShare; upkeep = Math.min(need, pool - build); }
      else { upkeep = Math.min(need, pool); build = pool - upkeep; }
      M += build;
      const maintained = need > 0 ? upkeep / need : 1;
      C = C * (1 - p.decay) + p.decay * Math.min(1, maintained);
      // court presence: per-head revenue against an outside option
      const Pn = Math.max(1e-9, N + B);
      const revenue = .5 * Math.min(1.5, harvest / Pn) + .5 * (B / Pn) / b;
      const outside = on.trade ? p.outside0 + (p.outside1 - p.outside0) * logistic(year, p.tradeYear, 20) : p.outside0;
      const gap = revenue - outside;
      E = Math.min(1, Math.max(0, E + p.court * (gap > 0 ? (1 - E) * gap : E * gap)));
      rows.push({year, P: N + B, C, E, build, maintained, core: E * (N + B), moat: E * Math.min(1, maintained),
        devotion, cohesion});
    }
    return rows;
  }

  function score(rows) {
    const at = y => rows[y - FIRST];
    const mean = (a, z, k) => { let s = 0; for (let y = a; y <= z; y++) s += at(y)[k]; return s / (z - a + 1); };
    const sustained = (test, from, span) => {
      for (let y = from; y <= LAST - span; y++) {
        let ok = true;
        for (let k = 0; k < span; k++) if (!test(at(y + k))) { ok = false; break; }
        if (ok) return y;
      }
      return null;
    };
    const coreRef = mean(1250, 1290, 'core'), buildRef = mean(1100, 1220, 'build');
    const onset = sustained(r => r.core < .85 * coreRef, 1250, 15);
    const deep = sustained(r => r.core < .4 * coreRef, 1250, 15);
    const moatLost = sustained(r => r.moat < .3, 1250, 10);
    let peak = 0, peakYear = FIRST; rows.forEach(r => { if (r.P > peak) { peak = r.P; peakYear = r.year; } });
    return {onset, deep, moatLost, peakYear,
      build1230_90: buildRef > 0 ? mean(1230, 1290, 'build') / buildRef : 0,
      build1300_50: buildRef > 0 ? mean(1300, 1350, 'build') / buildRef : 0,
      pop1431: at(1431).P / peak};
  }

  // Observations, each from a dated source (see RESULTS2.txt)
  function tests(s) {
    return {
      buildingFalls: s.build1230_90 < .35,                                  // few monuments after ~1220
      buildingStops: s.build1300_50 < .1,                                   // last major temple 1295
      coreOnset: s.onset != null && s.onset >= 1300 && s.onset <= 1340,  // moat cores
      moatBy1400: s.moatLost != null && s.moatLost <= 1400,                 // moat cores
      gradual: s.onset != null && ((s.deep ?? 1451) - s.onset) >= 40,       // moat cores
      notEmpty: s.pop1431 > .25,                                            // reoccupation, Angkor Wat used on
      apogee: s.peakYear >= 1150 && s.peakYear <= 1340};                    // lidar population study
  }

  function drawPriors(rnd, seed) {
    const u = (a, z) => a + (z - a) * rnd();
    const attrition = u(.02, .06);
    return {seed, attrition, bondedShare: Math.min(.4, u(.0028, .0038) / attrition),
      growth: u(.01, .025), famine: u(.3, 1), follow: u(.005, .04), decay: u(.03, .1), slack: u(1.1, 1.6),
      bondedWork: u(.3, .7), corvee: u(.03, .08),
      buffer: u(.3, .8), channelGain: u(.12, .4), droughtMean: u(.65, .85), noise: u(.05, .12),
      contestProb: u(.2, .6), contestCut: u(.2, .6),
      warLoss: u(.05, .2), warFlight: u(.3, .8),
      orgyShare: u(.5, .9), templeUpkeep: u(.002, .02),
      theravadaYear: u(1290, 1320), theravadaFloor: u(.2, .6),
      silt: u(.02, .15), court: u(.05, .3), outside0: u(.5, .8), outside1: u(1, 1.6), tradeYear: u(1150, 1450)};
  }
  return {run, score, tests, drawPriors, rngFrom, MECH, fixed, FIRST, LAST};
}

  const initialEngine = makeClimateEngine(0, true);
  const random = initialEngine.rngFrom(20261106);
  const priors = Array.from({length:2000}, (_, i) => initialEngine.drawPriors(random,1000+i));
  const defaults = Object.freeze({sensitivity:.07,draw:42});
  function run(options={}) {
    const controls={...defaults,...options};
    const index=Math.max(0,Math.min(1999,Math.floor(controls.draw)-1));
    const parameters={...priors[index]};
    const model=makeClimateEngine(controls.sensitivity,false);
    const neutral=makeClimateEngine(controls.sensitivity,true);
    const current=model.run(parameters,{}), reference=neutral.run(parameters,{});
    const summary=summaries[Number(controls.sensitivity).toFixed(2)];
    return {controls,parameters,source:'NOAA Bidoup Nui Ba 2010 PDSI, 1250–1450',
      translation:{coefficient:controls.sensitivity,minimum:.4,maximum:1.15},
      before1250:'Original synthetic initialization weather',
      current:current.filter(r=>r.year>=1250), reference:reference.filter(r=>r.year>=1250),
      summary, score:model.score(current), climate:Object.entries(pdsi).map(([year,value])=>({year:+year,pdsi:value}))};
  }
  return {defaults,run};
})();
