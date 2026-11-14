> **Warning (November 2026):** these results come from a frozen engine copy that uses the old coordination multiplier (5^0.227 ≈ 1.44, a size association treated as a causal effect) and a water floor of 0.1. Both were removed from the public engines after the external review (see experiments/angkor-review/README.md). In the public relocation engine, removing them changes the headline result, so these numbers have not been checked under the new defaults. Treat them as historical.

# Administrative learning and elite exit: matched experiment

Exploratory extension of the two-centre relocation model. No historical calibration or probability claim. Existing website engines are unchanged.

## Main drought comparison

| Rule | Persistent departures / 576 | Mean core retained, final/own peak | Mean final core, normalized people | Cumulative old-centre food shortfall |
|---|---:|---:|---:|---:|
| fixed | 192 | 78.8% | 0.07771 | 3.283 |
| learning | 224 | 83.4% | 0.08843 | 2.222 |
| learning-loss | 255 | 72.9% | 0.07883 | 2.578 |

Learning reduces shortfalls from 3.283 to 2.222 normalized person-year food units, about 32%. Knowledge loss increases them to 2.578, about 16% above learning with local retention. The mean final core is about 10.9% smaller with knowledge loss than with learning alone, but remains slightly larger than in the fixed-coordination arm.

Knowledge loss worsens core retention in 352/576 paired drought settings and raises shortfalls in 477/576. The effect is not universal. Mean final old water condition is nearly unchanged between the learning arms (51.6% versus 51.5%). In this implementation the strongest channel is productive coordination, not a demonstrated hydraulic-network cascade.

Learning can increase departures because both centres learn and their relative attractiveness changes. Under stable climate, departures number 215/576 with fixed coordination and 224/576 in each learning arm. Under drought they are 192, 224 and 255 respectively. A persistent departure is fewer than 40% of all elites at the old centre for ten consecutive steps.

## Equations and controlled differences

All arms start with the same population, land, water, stores, elite allocation and knowledge K = 0.5. Coordination multiplies harvest by 1 + (5^0.227 - 1)K. This is an Atlas experimental mapping using the published 1.227 scaling exponent as motivation; it is not an estimated causal learning equation. The fixed arm holds K at 0.5, so its initial productivity is identical to the other arms. It differs from the older relocation model, which used the full multiplier in every year.

The learning arm updates K by learningRate × completedWork × (1-K). Completed work is a bounded spending-based proxy: (paid maintenance + reclamation + construction)/(maintenance need + 0.04 × developed land), capped at 1. Spending was already financed in the food ledger. This proxy assumes financed work succeeds; it is not a record of skilled supervisor hours or military experience. There is no background forgetting in these experiments.

The learning-loss arm uses the same update, then transfers K × lossStrength × departingFraction from the origin when elites move. The receiver gains that index amount, up to K = 1. Overflow is recorded separately. This is a stylised administrative-knowledge index, not a measured stock of trained people. It assumes administrators move with the elite cohort. Knowledge preserved in village institutions is represented indirectly by lossStrength below 1, not by a separate cadre stock.

All other relocation equations, demographic rules and climate assumptions are copied unchanged. Both centres receive identical random weather noise within a matched triple. The southern climate advantage and outside opportunities remain imposed assumptions. Household food losses, elite movement and worker movement are distinct. Rural households cannot migrate. Model years are elapsed time, not historical dates. There is no campaign or military scheduling module in this experiment.

## Design

Main grid: outside opportunity 0.8/1.2/1.6; moving hurdle 0.05/0.25/0.5; local repair 0/0.75; stable/drought climate; seeds 1–32. Portability is fixed at 0.75, learning rate at 0.03 and knowledge-loss strength at 0.5. This produces 1,152 matched triples, or 3,456 histories.

Sensitivity grid: learning rate 0.01/0.03/0.06; loss strength 0.25/0.5/1; both climates; seeds 1–32. Outside opportunity = 1.2, moving hurdle = 0.25, local repair = 0.5. This adds 576 triples, or 1,728 histories. Controls duplicated across sensitivity levels are repeated comparators, not independent evidence. Full results and grouped summaries are included.

## Checks and reproduction

Food ledgers, migrant conservation and elite totals are checked to 1e-10. Every knowledge update is checked against learning, transfer and receiver overflow. Fixed coordination remains fixed. With movement blocked, the learning-loss and learning histories match exactly. Maximum food/migration accounting error was 1.34e-15 normalized units.

Run `node run.cjs` in the extracted folder. It rewrites results.csv, summary.json and prints the checks. Node is required only for batch reproduction. The report and CSV can be read on iOS. This archive is an offline experiment, not a deployed website update.

The published motivation is Klassen, Ortman, Lobo and Evans, Provisioning an Early City, DOI: 10.1007/s10816-021-09535-5. Atlas supplies the dynamic knowledge rules. Hall, Penny and Hamilton's Koh Ker comparison (10.1371/journal.pone.0203962) motivates separating court departure from continued settlement; it does not calibrate learning or loss rates.
