/* Seasonal grain, labour and travel experiment. All rates are illustrative. */
'use strict';
globalThis.AngkorCampaign = (() => {
  const defaults = Object.freeze({distance: 180, yield: 1.6, collection: .24, levy: .12,
    fightingDays: 65, fieldShare: .75, transport: 'elephant', fishery: 'lake', digging: 1, seed: 42});
  const constants = Object.freeze({initialPeople: 240000, initialBonded: 6000, frontierPeople: 100000,
    farmHectares: 76000, quarryKm: 35, years: 18, firstYear: 1200,
    initialVillageGrain: 26000, initialCourtGrain: 12000, adults: .45, annualRation: .21,
    storageLossPerSeason: .035, capturePerSoldier: .12, workDaysPerSeason: 60,
    alliedShare: .25, alliedReserveMultiple: 1.6, fishPaddyEquivalent: .35,
    fishProteinFraction: .18, fishStorageLoss: .25, earthworkDaysPerUnit: 900000});
  const modes = Object.freeze({foot: {speed: 22, supply: 1, stone: 36},
    elephant: {speed: 18, supply: .78, stone: 56}, river: {speed: 35, supply: .65, stone: 80}});

  const fisheries = Object.freeze({lake: [.014, .008, .022], corridor: [.017, .003, .013], none: [0, 0, 0]});
  const riverAccess = [.8, .95, 1.15];

  function run(options = {}) {
    const p = {...defaults, ...options}, c = constants, mode = modes[p.transport];
    const days = [120, 120, 125], names = ['Planting', 'Campaign', 'Harvest'];
    const responseDays = Math.ceil(p.distance / (mode.speed * (p.transport === 'river' ? riverAccess[1] : 1)));
    const campaignDays = 2 * responseDays + p.fightingDays;
    let rng = p.seed >>> 0;
    const random = () => ((rng = (Math.imul(1664525, rng) + 1013904223) >>> 0) / 4294967296);
    let free = c.initialPeople - c.initialBonded, bonded = c.initialBonded, frontier = c.frontierPeople;
    let village = c.initialVillageGrain, court = c.initialCourtGrain;
    let tour = null, planting = 1, stone = 0, timber = 0, completed = 0, fish = 0, channels = 0;
    const rows = [];

    for (let t = 0; t < c.years * 3; t++) {
      const s = t % 3, duration = days[s], year = c.firstYear + Math.floor(t / 3);
      const weather = .76 + random() * .42;
      const encounter = random();
      const openingGrain = village + court;
      const spoilage = openingGrain * c.storageLossPerSeason;
      village *= 1 - c.storageLossPerSeason;
      court *= 1 - c.storageLossPerSeason;
      let launched = false, campaignGrain = 0;
      if (s === 1 && !tour) {
        const local = Math.floor(free * c.adults * p.levy);
        const perSoldier = campaignDays * .0008 * mode.supply;
        const allies = completed > 0 && court >= local * perSoldier * c.alliedReserveMultiple
          ? Math.floor(local * c.alliedShare) : 0;
        const soldiers = local + allies;
        const supply = soldiers * perSoldier;
        if (soldiers && court >= supply) {
          court -= supply;
          campaignGrain = supply;
          tour = {local, allies, left: campaignDays, capture: Math.floor(soldiers * c.capturePerSoldier * encounter)};
          launched = true;
        }
      }
      const away = tour ? Math.min(duration, tour.left) : 0;
      const localSoldiers = away ? tour.local : 0;
      const alliedSoldiers = away ? tour.allies : 0;
      const labourLost = localSoldiers * away / duration * c.workDaysPerSeason;
      const freeDays = free * c.adults * c.workDaysPerSeason - labourLost;
      const bondedDays = bonded * c.adults * c.workDaysPerSeason;
      const openingFish = fish;
      const fishSpoilage = fish * c.fishStorageLoss;
      const fishCatch = Math.min(c.initialPeople, free + bonded) * fisheries[p.fishery][s] * weather;
      fish += fishCatch - fishSpoilage;
      const fishingDays = Math.min(freeDays, fishCatch * 8);
      const availableFree = freeDays - fishingDays;
      const required = c.farmHectares * (s === 1 ? 18 : 72);
      const fieldDays = Math.min(required, availableFree + bondedDays * p.fieldShare);
      const coverage = fieldDays / required;
      if (s === 0) planting = coverage;
      const harvest = s === 2 ? c.farmHectares * p.yield * weather * Math.min(planting, coverage) * (1 + .12 * channels) : 0;
      village += harvest;
      const fullRation = (free + bonded) * c.annualRation * duration / 365;
      const fishEaten = Math.min(fish, fullRation * .08 / c.fishPaddyEquivalent);
      fish -= fishEaten;
      const ration = fullRation - fishEaten * c.fishPaddyEquivalent;
      const fromVillage = Math.min(village, ration);
      village -= fromVillage;
      const fromCourt = Math.min(court, ration - fromVillage);
      court -= fromCourt;
      const foodGap = ration - fromVillage - fromCourt;
      const collection = s === 2 ? p.collection * Math.max(0, village - (free + bonded) * c.annualRation * 240 / 365) : 0;
      village -= collection;
      court += collection;
      const availableDays = Math.max(0, availableFree + bondedDays - fieldDays);
      const discretionaryDays = Math.min(availableDays, free * c.adults * 6 + bondedDays * (1 - p.fieldShare),
        foodGap > 0 ? 0 : court / .001);
      const usableChannels = channels * .94;
      const diggingDays = Math.min(discretionaryDays * .30, (1 - usableChannels) * c.earthworkDaysPerUnit * p.digging);
      channels = usableChannels + diggingDays / (c.earthworkDaysPerUnit * p.digging);
      const buildDays = discretionaryDays - diggingDays;
      const buildingGrain = buildDays * .001;
      const diggingGrain = diggingDays * .001;
      court -= buildingGrain + diggingGrain;
      const stoneAdded = Math.min(buildDays * .006, mode.stone * (p.transport === 'river' ? riverAccess[s] * (1 + .25 * channels) : 1) * 35 / c.quarryKm);
      const timberAdded = Math.max(0, buildDays - stoneAdded / .006) * .012;
      stone += stoneAdded;
      timber = timber * .93 + timberAdded;
      let captured = 0;
      if (tour) {
        tour.left -= away;
        if (tour.left === 0) {
          captured = Math.min(frontier, tour.capture);
          frontier -= captured;
          bonded += captured;
          completed++;
          tour = null;
        }
      }
      rows.push({year: year + s / 3, calendarYear: year, season: names[s], weather, harvest, villageGrain: village,
        courtGrain: court, spoilage, collection, foodGap, ration, rationPaid: fromVillage + fromCourt,
        fishCatch, fishEaten, fishProteinKg: fishEaten * c.fishProteinFraction * 1000, fishInStore: fish,
        fishSpoilage, fishingDays, fishBalanceError: openingFish + fishCatch - fishSpoilage - fishEaten - fish,
        channels, diggingDays, diggingGrain, campaignGrain, localSoldiers, alliedSoldiers, daysAway: away, campaignStarted: launched, farmCoverage: coverage, buildingGrain,
        captured, bonded, population: free + bonded, frontierPopulation: frontier, stone, timber,
        grainBalanceError: openingGrain + harvest - spoilage - fromVillage - fromCourt -
          buildingGrain - diggingGrain - campaignGrain - village - court});
    }
    return {parameters: p, constants: c, transport: mode, responseDays, campaignDays, rows};
  }
  function compare(options) {
    const current = run(options);
    const differences = Array.from({length: 32}, (_, i) => {
      const seed = ((options.seed + i - 1) % 4294967295) + 1;
      const base = run({seed});
      const trial = run({...options, seed});
      const sum = (result, key) => result.rows.reduce((total, row) => total + row[key], 0);
      return {seed, foodGapDelta: sum(trial, 'foodGap') - sum(base, 'foodGap'),
        capturedDelta: sum(trial, 'captured') - sum(base, 'captured'),
        alliedCampaignsDelta: trial.rows.filter(r => r.campaignStarted && r.alliedSoldiers).length -
          base.rows.filter(r => r.campaignStarted && r.alliedSoldiers).length};
    });
    return {...current, pairedSeeds: differences};
  }
  return {defaults, run, compare};
})();
