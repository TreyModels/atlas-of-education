# Cambodia child labour: seed spread of the headline outputs

Script: `run.cjs` (this folder). Output: `results.json` (this folder). Engine: `public/engines/camchild.js`
(SHA-256 `948eb353260ac51050319d11db97fd9ad9ebb2b0ca4708f09e2b36c06ab54f38`, the file as it stood after the
comment-only edits of 13 Nov 2026).

Run: `node experiments/camchild-seeds/run.cjs [seeds]` from the repository root. Default is 50 seeds (seeds 1 to 50).
Each seed is one 6,000-household, 12-year history (2025 to 2036). The run takes about 10 minutes on Node 26 and
makes 700 simulations (50 reference plus 13 scenarios times 50 seeds). `run.cjs` loads the engine in a `vm` context
the way `test-worlds.cjs` does. It needs Node 18 or later only for `test-worlds.cjs`; `run.cjs` itself runs on Node 16.

## Scenarios

No curated scenario file (`web/camchild_scenarios.js`) exists in this repository, so the policy scenarios here are
defined by `run.cjs`, not taken from the app. The reference is the engine default: every lever at zero, Thailand route
open. Each policy scenario sets one of the Cambodia world's 13 levers, alone, to half of its slider maximum (cash
0.075, cashU 0.075, garmentBoom 0.25) or to 0 (thaiOpen, closing the route). Three are context levers, not
programmes: floorRise, garmentBoom and thaiOpen. They get no cost index.

Headline outputs are read from each history and compared with the reference history for the same seed. The rows are
the national child labour rate, child-years avoided, school attendance, labour by quintile and region, children of
migrant parents, and teens working away. The cost index is shown only as an illustrative per-seed ratio. Its unit
costs are UNSOURCED (see the engine's `cst()` comment).

Spread is the sample standard deviation (n minus 1) across the 50 seeds. Percentiles use linear interpolation.

## Seed spread of the reference (no programmes)

| Headline output (2036 unless stated) | Mean | SD | p5 | p50 | p95 |
|---|---:|---:|---:|---:|---:|
| Child labour rate, national, 2036 | 14.01% | 0.46 pp | 13.40% | 14.01% | 14.71% |
| Child-years of labour avoided over 12 years (vs reference) | 0 | 0 | 0 | 0 | 0 |
| Attending school (school only or school and work), 2036 | 81.61% | 0.43 pp | 80.92% | 81.65% | 82.19% |
| Child labour, poorest fifth, 2036 | 38.65% | 1.42 pp | 36.43% | 38.75% | 40.73% |
| Child labour, richest fifth, 2036 | 1.39% | 0.40 pp | 0.70% | 1.42% | 2.01% |
| Child labour, countryside, 2036 | 15.46% | 0.58 pp | 14.68% | 15.46% | 16.47% |
| Child labour, Phnom Penh, 2036 | 8.89% | 0.66 pp | 7.99% | 8.88% | 9.83% |
| Child labour, children of migrant parents, 2036 | 5.16% | 0.67 pp | 4.21% | 5.11% | 6.32% |
| Teens working away from home, share of all children, 2036 | 10.01% | 0.34 pp | 9.50% | 10.02% | 10.56% |
The reference's own spread is the yardstick. The national child labour rate in 2036 moves by about 0.46 percentage
points (pp) from one history to another (p5 to p95: 13.4% to 14.7%).

## Policy differences against the seed spread

Each row is the paired difference (scenario minus reference, same seed) in the national child labour rate in 2036,
compared with the reference's seed SD for that output. "Smaller than seed spread" means the absolute mean
difference is below the reference SD. Paired t is the mean difference over its standard error across the 50 seeds,
and it measures whether the difference is reliably non-zero under common seeds.

| Scenario | Lever | Working 2036, change vs reference (pp) | Reference seed SD (pp) | Ratio (diff / SD) | Smaller than seed spread? | Paired t | Share of seeds same sign | Child-years avoided, mean (scenario SD) |
|---|---|---:|---:|---:|---|---:|---:|---:|
| cash_0p075 | cash = 0.075 (programme) | -4.82 | 0.46 | 10.37 | no | -65.6 | 1.00 | 3415 (143) |
| cashU_0p075 | cashU = 0.075 (programme) | -2.07 | 0.46 | 4.46 | no | -27.0 | 1.00 | 1461 (134) |
| tutorFix_0p5 | tutorFix = 0.5 (programme) | -1.34 | 0.46 | 2.88 | no | -18.2 | 1.00 | 882 (112) |
| debtRelief_0p5 | debtRelief = 0.5 (programme) | -1.28 | 0.46 | 2.75 | no | -17.5 | 1.00 | 904 (114) |
| protection_0p5 | protection = 0.5 (programme) | -2.20 | 0.46 | 4.74 | no | -32.4 | 1.00 | 1542 (118) |
| feeding_0p5 | feeding = 0.5 (programme) | -2.30 | 0.46 | 4.95 | no | -30.0 | 1.00 | 1624 (132) |
| leftSupport_0p5 | leftSupport = 0.5 (programme) | -0.26 | 0.46 | 0.56 | yes | -3.5 | 0.66 | 113 (128) |
| harvest_0p5 | harvest = 0.5 (programme) | -0.50 | 0.46 | 1.08 | no | -6.6 | 0.84 | 314 (113) |
| bridging_0p5 | bridging = 0.5 (programme) | -0.44 | 0.46 | 0.94 | yes | -6.6 | 0.84 | 227 (97) |
| ban_0p5 | ban = 0.5 (programme) | -0.32 | 0.46 | 0.69 | yes | -4.4 | 0.74 | 224 (103) |
| floorRise_0p5 | floorRise = 0.5 (context) | -0.67 | 0.46 | 1.43 | no | -9.8 | 0.88 | 457 (112) |
| garmentBoom_0p25 | garmentBoom = 0.25 (context) | 0.02 | 0.46 | 0.04 | yes | 0.2 | 0.46 | -19 (109) |
| thaiOpen_0 | thaiOpen = 0 (context) | -0.00 | 0.46 | 0.01 | yes | -0.0 | 0.56 | -29 (238) |


Child-years avoided are compared over 12 years and summed over all 6,000 households. The reference has no spread on
this output by construction, so `smallerThanSeedSpread` in `results.json` is not meaningful for that output. Use the
scenario SD column above.

## Answer

Yes. Several headline policy differences are smaller than the seed spread.

- On the national child labour rate in 2036, five single-lever settings move the rate by less than the reference SD
  (0.46 pp): leftSupport (-0.26 pp), bridging (-0.44 pp), ban (-0.32 pp), garmentBoom (+0.02 pp) and thaiOpen closed
  (0.00 pp). Harvest (-0.50 pp, ratio 1.08) is just above the line. Debt relief, floor rise, tutoring, protection,
  feeding, unconditional cash and cash are all larger than the spread.
- The smaller-than-spread effects are not all zero. Under common seeds, leftSupport (t = -3.5), bridging (t = -6.6)
  and ban (t = -4.4) are reliably below zero, but they are small compared with a single history's variation. garmentBoom
  (t = 0.2) and closing the Thai route (t = -0.0) cannot be distinguished from zero on national child labour.
- Closing the Thai route leaves national child labour unchanged. Teens working away from home fall by 10.0 pp
  (about 29 reference SDs; paired t = -206). The migration channel is substituted, not removed: the same children
  end up in local work or school. Read the national rate and the migrant-teen rate together.
- The verdict depends on the output. For example, the Phnom Penh child labour rate under leftSupport is
  smaller than the seed spread (ratio 0.12), while the countryside rate under the same lever is also smaller
  (0.54). `results.json` holds the comparison for every headline output.

## Caveats

- The illustrative cost index is not a cost estimate. Its unit costs are invented and unsourced. For leftSupport the
  denominator is small (about 113 child-years avoided on average), so the per-seed ratio is unstable: its mean is
  8.4 over the 43 seeds with positive avoidance, and the pooled figure is 4.2. Do not quote either.
- The paired design is not perfect. Setting thaiOpen below 1 draws extra random numbers in the engine, so the paired
  comparison for that scenario is weaker than for the programme levers.
- Half-maximum levels are arbitrary. A different level changes the size of each difference but not the spread,
  so the ranking of "smaller than spread" against the reference SD may change with the level chosen.
- Seeds 1 to 50 were used. The Cambodia world uses seed 7 with up to 8 histories, so its figures are not reproduced
  exactly.
- The engine has an unresolved provenance problem: its school values (vPrim, vLow, vUp) are calibrated, not measured.
  This affects the level of child labour more than the spread. See the comments in the engine files.
