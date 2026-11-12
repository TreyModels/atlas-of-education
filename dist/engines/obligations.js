'use strict';
globalThis.AngkorObligations = (() => {
  const defaults = Object.freeze({externalShare:.55, rigidity:.85, disruption:.65, duration:3, supplier:'display', returnRule:'closed', seed:42, upstream:null});
  const assumptions = Object.freeze({fullReceipts:200, ritualBill:40, courtBill:130,
    startingReserve:70, storageCapacity:100, lossRate:.10, disruptionStart:4, missedYearsToExit:2});

  function run(options = {}) {
    const p = {...defaults,...options}, a = assumptions;
    const upstream = AngkorSignalling.run({...p.upstream, seed:p.seed}, p.supplier);
    let reserve = a.startingReserve, arrears = 0, missed = 0, exitYear = null, returnYear = null;
    let elitePresent = true;
    const rows = [];
    for (const input of upstream.rows) {
      const {year, harvestShock, tributeReceived} = input;
      const open = reserve;
      const spoiled = open * a.lossRate;
      const interrupted = year >= a.disruptionStart && year < a.disruptionStart + p.duration;
      const deliveryFraction = (elitePresent || p.returnRule === 'open') && tributeReceived > 0 ? 1 - (interrupted ? p.disruption : 0) : 0;
      const local = a.fullReceipts * (1-p.externalShare) * harvestShock;
      const external = a.fullReceipts * p.externalShare * deliveryFraction;
      const available = open - spoiled + local + external;
      const returned = !elitePresent && p.returnRule === 'open' && external > 0 &&
        available >= a.ritualBill + a.courtBill;
      if (returned) {
        elitePresent = true;
        returnYear ??= year;
      }
      const presentAtPayment = elitePresent;
      const ritualPaid = Math.min(a.ritualBill, available);
      const courtDue = elitePresent ? a.courtBill * (p.rigidity + (1-p.rigidity)*deliveryFraction) : 0;
      const courtPaid = Math.min(courtDue, available - ritualPaid);
      const unpaid = courtDue - courtPaid;
      arrears += unpaid;
      missed = unpaid > 1e-8 ? missed + 1 : 0;
      const exited = elitePresent && missed >= a.missedYearsToExit;
      if (exited) {
        exitYear ??= year;
        elitePresent = false;
        missed = 0;
      }
      const unspent = available - ritualPaid - courtPaid;
      reserve = Math.min(a.storageCapacity, unspent);
      const overflow = unspent - reserve;
      rows.push({year, upstreamTribute:tributeReceived, deliveryFraction, local, external, openingReserve:open,
        spoiled, ritualPaid, courtDue, courtPaid, unpaid, cumulativeUnpaid:arrears, elitePresent:presentAtPayment,
        eliteExited:exited, eliteReturned:returned, reserve, overflow,
        balanceError:available - ritualPaid - courtPaid - overflow - reserve});
    }
    return {parameters:p, assumptions:a, upstreamParameters:upstream.parameters, exitYear, returnYear, rows};
  }

  function compare(options = {}) {
    const p = {...defaults,...options}, current = run(p);
    const reference = run({...p, disruption:0});
    const paired = Array.from({length:32}, (_,i) => {
      const seed = ((p.seed-1+i)%4294967295)+1;
      const a = run({...p,seed}), b = run({...p,seed,disruption:0});
      return {seed, exitYear:a.exitYear, returnYear:a.returnYear, referenceExitYear:b.exitYear, referenceReturnYear:b.returnYear,
        ritualContinues:a.exitYear !== null && a.rows.some(r => r.year > a.exitYear && r.ritualPaid >= assumptions.ritualBill),
        unpaid:a.rows.at(-1).cumulativeUnpaid, referenceUnpaid:b.rows.at(-1).cumulativeUnpaid};
    });
    return {current, reference, paired};
  }
  return {defaults, run, compare};
})();
