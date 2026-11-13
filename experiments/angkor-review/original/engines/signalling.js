/* Experiment 03. Illustrative grain-equivalent and labour accounts. */
'use strict';
globalThis.AngkorSignalling = (() => {
  const defaults = Object.freeze({loss: .55, stoneWeight: .65, displayShare: .16, signalScale: 1, seed: 42});
  const assumptions = Object.freeze({
    years: 12, startingGrain: 45, storageCapacity: 180, storageLoss: .12,
    annualGrain: 320, annualLabour: 420, recoveryYears: 8, tribute: 105,
    initialStone: 1, stoneLoss: .015, buildingScale: 620,
    initialElephants: 40, elephantUpkeep: 2.5, elephantLabour: 2, elephantBudgetShare: .28,
    replacementCost: 5, annualReplacements: 5, capacityScale: 300,
    annualThreatBase: 205, annualThreatSpread: 110, initialPledge: true
  });

  function run(options = {}, observer = 'display') {
    const p = {...defaults, ...options}, a = assumptions;
    let state = p.seed >>> 0;
    const draw = () => ((state = (Math.imul(1664525, state) + 1013904223) >>> 0) / 4294967296);
    let reserve = a.startingGrain, stone = a.initialStone, elephants = a.initialElephants;
    let pledged = a.initialPledge;
    const rows = [];

    for (let year = 1; year <= a.years; year++) {
      const harvestShock = .78 + .44 * draw();
      const demand = a.annualThreatBase + a.annualThreatSpread * draw();
      const localGrain = a.annualGrain * harvestShock * (1 - p.loss * Math.max(0, 1 - (year - 1) / a.recoveryYears));
      const tributeReceived = pledged ? a.tribute : 0;
      const openingReserve = reserve;
      const spoiled = reserve * a.storageLoss;
      let available = reserve - spoiled + localGrain + tributeReceived;
      const openingLabour = a.annualLabour;
      const build = Math.min(available * p.displayShare, openingLabour);
      available -= build;
      let labour = openingLabour - build;
      stone = Math.min(1.35, stone * (1 - a.stoneLoss) + build / a.buildingScale);

      const elephantBudget = available * a.elephantBudgetShare;
      const maintained = Math.min(elephants, Math.floor(elephantBudget / a.elephantUpkeep), Math.floor(labour / a.elephantLabour));
      const upkeep = maintained * a.elephantUpkeep;
      const upkeepLabour = maintained * a.elephantLabour;
      available -= upkeep;
      labour -= upkeepLabour;
      const replacements = Math.min(a.annualReplacements, a.initialElephants - maintained,
        Math.floor((elephantBudget - upkeep) / a.replacementCost), Math.floor(labour / a.elephantLabour));
      const replacementSpend = replacements * a.replacementCost;
      const replacementLabour = replacements * a.elephantLabour;
      available -= replacementSpend;
      labour -= replacementLabour;
      elephants = maintained + replacements;

      const trueCapacity = Math.min(available, labour);
      const displayedCapacity = a.capacityScale * p.signalScale * (p.stoneWeight * stone +
        (1 - p.stoneWeight) * maintained / a.initialElephants);
      const perceivedCapacity = observer === 'truth' ? trueCapacity : displayedCapacity;
      pledged = perceivedCapacity >= demand;
      const defended = trueCapacity >= demand;
      const defenceSpend = Math.min(trueCapacity, demand);
      const unspent = available - defenceSpend;
      reserve = Math.min(a.storageCapacity, unspent);
      const storageOverflow = unspent - reserve;
      rows.push({year, observer, harvestShock, demand, openingReserve, localGrain, tributeReceived,
        spoiled, build, stone, maintainedElephants: maintained, elephants, upkeep, replacementSpend,
        openingLabour, upkeepLabour, replacementLabour, trueCapacity, displayedCapacity, perceivedCapacity,
        pledged, defended, defenceSpend, storageOverflow, reserve,
        grainBalanceError: openingReserve + localGrain + tributeReceived - spoiled - build - upkeep -
          replacementSpend - defenceSpend - storageOverflow - reserve});
    }
    return {observer, parameters: p, assumptions: a, rows};
  }

  function compare(options = {}) {
    const p = {...defaults, ...options};
    const current = run(p), truth = run(p, 'truth');
    const pairedSeeds = Array.from({length: 32}, (_, i) => {
      const seed = ((p.seed - 1 + i) % 4294967295) + 1;
      const display = run({...p, seed});
      const informed = run({...p, seed}, 'truth');
      const count = (result, predicate) => result.rows.filter(predicate).length;
      return {seed,
        falseReassurance: count(display, row => row.pledged && !row.defended),
        lostCredibility: count(display, row => !row.pledged && row.defended),
        defenceYearsDelta: count(display, row => row.defended) - count(informed, row => row.defended),
        tributeYearsDelta: count(display, row => row.pledged) - count(informed, row => row.pledged)};
    });
    return {parameters: p, current, truth, pairedSeeds};
  }

  return {defaults, run, compare};
})();
