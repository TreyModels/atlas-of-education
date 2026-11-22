# Three experiment rounds on the agent model (v10-v12)

Produced by a delegated agent, 2026-11-22, ~90 cores, 2,000+ runs.

## Round 1 (v10) — closed the fiscal-to-household loop
The defect: crown revenue was not coupled to household welfare, so mortality never bit.
Fixed by giving the network a length that grows with revenue, making the crown budget real,
routing harvest through `hEff = 0.55 + 0.45*infra`, replacing the mortality rule with
food-driven demography, and bounding prestige (v9's unbounded prestige pinned charter at 1.0,
which is why nothing downstream of charter ever fired).

Result: interior peak rate 0.99 of 672 runs (v9: 0.00). Default peak 1003, lag 128,
decline 0.80, elite land share 0.57. Ablation with the coupling off: peak 1583, no relocation.
**The coupling is the whole mechanism.**

## Round 2 (v11) — fixed a budget degeneracy
Round 1 had `(u0.30,m0.45)` bit-identical to `(u0.12,m0.18)`: only the ratio entered.
Replaced with committed obligations. Best variant `Y1 u85`: peak 1137, lag 135, decline 0.82.

## Round 3 (v12) — routed shocks through the capital stock
Raid and drought were dead parameters; they now cut infrastructure and abandon fields.
Best variant `Z5 pd4500`: peak 1099, lag 142, decline 0.80, pattern 1.00 on every seed.

## The caveat that matters
Those "hits" were found by choosing parameter values. Re-run under the derived priors in
`scripts/p1_priors.js` (see `scripts/p2_mc.js`), the same v12 engine peaks at **857 CE**
(90% CI 833-876), with P(peak in 1000-1300) = 2% and P(full pattern) = 0%.

So: the structural fixes are real and improved the model, but the apparent fit to Angkor's
timing is a tuning artefact. Every architecture tested - v8 stock, v9 agent, v12 agent -
peaks roughly 300 years too early once the parameters have to be defensible.

The open hypothesis: the ratchet cannot bite until the land frontier closes. Before that,
alienating land costs the crown nothing because unclaimed land replaces it. That predicts
the fiscal squeeze begins when cultivated area approaches its ceiling, not at founding.

Still dead: `monDep`, `migrateProb`, `mortSlope`/`mortMax`, `armyPerKm`, `clearProb`,
`netUp`, `crownShare`.
