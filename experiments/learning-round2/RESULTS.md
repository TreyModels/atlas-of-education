> **Warning (November 2026):** these results come from a frozen engine copy that uses the old coordination multiplier (5^0.227 ≈ 1.44, a size association treated as a causal effect) and a water floor of 0.1. Both were removed from the public engines after the external review (see experiments/angkor-review/README.md). In the public relocation engine, removing them changes the headline result, so these numbers have not been checked under the new defaults. Treat them as historical.

# Administrative learning: round 2

Exploratory mechanism and structural-sensitivity tests. All units and rates remain synthetic. There is no fit to Angkor's historical decline.

## Main drought comparison

Each row averages the same 288 settings, with different outside opportunities, moving hurdles, local-repair arrangements and matched weather seeds.

| Rule | Persistent departures / 288 | Final old core, normalized people | Final old water condition | Cumulative food shortfall |
|---|---:|---:|---:|---:|
| Learning; knowledge retained | 112 | 0.08871 | 51.6% | 2.222 |
| Knowledge travels with elites | 127 | 0.07887 | 51.5% | 2.576 |
| Knowledge travels with workers | 112 | 0.08696 | 51.0% | 2.362 |
| Mixed carriers | 116 | 0.08137 | 50.4% | 2.520 |
| 50% of knowledge retained locally | 113 | 0.08187 | 50.5% | 2.482 |
| 90% retained locally | 112 | 0.08697 | 51.3% | 2.321 |
| Elite knowledge loss; equal drought exposure | 112 | 0.08160 | 50.7% | 2.576 |
| Knowledge retained; equal drought exposure | 112 | 0.09086 | 51.1% | 2.267 |
| Elite knowledge loss plus forgetting | 128 | 0.07322 | 49.5% | 3.032 |
| Recurring obligations decay 2% per year | 112 | 0.09499 | 90.9% | 1.970 |
| Maintenance funded before ritual | 80 | 0.11797 | 98.9% | 1.084 |
| Theoretical production exponent 7/6 | 99 | 0.07974 | 51.8% | 3.064 |
| Production exponent 1 | 96 | 0.06938 | 51.3% | 3.722 |

## Findings

1. Under the assumed rule that maintenance is funded before ritual, the drought food gap is lower than under the ritual-first order. The ordering is set by the model rule, so this is an assumption-driven result, not a finding. Relative to the elite-carried-knowledge arm, prioritizing maintenance lowers the cumulative drought food gap from 2.576 to 1.084, about 58%, and lowers persistent departures from 127/288 to 80/288. This swaps maintenance and ritual budget priority. It is not a finding that Angkor historically paid them in either order.

2. Expiring commitments also matter: 2% annual decay in the recurring-obligation base lowers the food gap to 1.970 and increases final water condition from 51.5% to 90.9%. The decaying variable is the cost-bearing temple stock inherited from the earlier model, not an independently measured temple endowment or a structural conservation estimate.

3. Who carries knowledge changes the result. Elite-carried knowledge loss yields 127 departures; worker-carried knowledge yields 112, and equal-weight mixed carriers 116. Knowledge retention at 90% restores departure incidence to 112/288 and reduces food gaps to 2.321. It does not fully restore the retained-knowledge food result of 2.222.

4. Giving both centres identical drought exposure leaves 112 departures in both the retained and knowledge-loss arms. Knowledge loss still raises food shortfalls from 2.267 to 2.576 (about 14%) and lowers mean final old-core population by about 10%. The earlier increase in departure incidence is therefore sensitive to the assumed destination climate advantage. Productivity losses persist in the equal-exposure test.

5. Knowledge loss has no economic effect when the production exponent is 1, confirmed in an exact placebo comparison. The causal channel exists because the model explicitly links knowledge to productive coordination. This test validates implementation, not the historical coefficient.

## Forced departure: isolate knowledge loss from the decision to leave

At model year 120, transfer 40% of the old elite cohort to the other centre in every matched arm, with all subsequent endogenous movement blocked. Compare knowledge retained, knowledge transferred with the cohort, and 90% local retention. The elite share falls from 80% to 48% by construction. These arms cannot be used to interpret spontaneous departure incidence, because movement is imposed and then blocked.

Average drought results:

| Knowledge rule | Knowledge immediately after shock | Knowledge 40 steps later | Final core, normalized people | Cumulative food gap |
|---|---:|---:|---:|---:|
| retained | 0.946 | 0.955 | 0.10897 | 2.056 |
| elite | 0.757 | 0.815 | 0.10441 | 2.247 |
| retention90 | 0.927 | 0.942 | 0.10857 | 2.072 |

Full transfer lowers the mean final core by about 4.2% and raises the food gap by about 9.3% relative to retention. Relearning partially repairs the knowledge deficit. Water-condition averages remain almost identical (about 43.5%). This experiment does not produce a hydraulic-network collapse from administrative departure. Its principal transmission channel is agricultural productivity.

## Exact design and assumptions

Robustness grid: 3 outside opportunities (0.8, 1.2, 1.6) × 3 moving hurdles (0.05, 0.25, 0.5) × 2 local repair shares (0, 0.75) × 2 climates (stable, drought) × seeds 1–16. Each of 576 settings runs all 13 rules, producing 7,488 histories.

Forced-shock design: 3 local repair shares (0, 0.5, 0.75) × 2 climates × 3 learning rates (0.01, 0.03, 0.06) × seeds 1–32. Each of 576 settings runs three knowledge-retention arms, producing 1,728 histories. Total: 9,216. These grids are sensitivity designs, not posterior distributions. Counts are scenario incidence, not probabilities of historical events.

Baseline knowledge rules: K starts at 0.5 in both centres. Coordination multiplier = 1 + (5^(beta-1)-1)K, beta = 1.227. Completed-work proxy = (financed upkeep + reclamation + construction)/(maintenance need + 0.04 × developed land), capped at 1. New learning = learningRate × completedWork × (1-K). Financed work is assumed completed. There is no explicit skill-occupation workforce or campaign model.

For the forgetting arm only, 0.5% of current knowledge is removed per step before new learning. Other arms have no background forgetting. Knowledge carried with a moving cohort = origin K × lossStrength × (1-retention) × carrier weight × fraction departing. Loss strength is 0.5. Elite-only and worker-only carrier weights are 1; mixed weights are 0.5 each. The receiver gains the removed amount up to K=1, with overflow recorded. These are organizational knowledge indices, not headcounts of qualified administrators. Rural households cannot move and rural knowledge is not represented as a separate stock.

The knowledge-retained arm has no migration-related loss. The 50% and 90% variants preserve those shares of the otherwise-transferable amount. The theory-scaling arm uses beta=7/6. The constant-productivity arm uses beta=1, eliminating the economic payoff to K. These exponents are structural scenarios; no archaeological regression is re-estimated.

The baseline temple-obligation base is perpetual. The sunset variant decays that base 2% annually before adding new construction. Maintenance-first is an assumed allocation order. It calculates the central maintenance allocation before ritual, using the same 45% maintenance-offer rule, and charges both to the same finite budget. The second-centre drought response is 0.85 by default and 0.62 in both equal-exposure arms. Old-centre response remains 0.62. Stable climate remains identical. All unmentioned relocation assumptions are inherited from round 1.

## Interpretation limits

The tests identify sensitive assumptions. They do not establish that temples historically extracted first, that ritual blocked repairs, or that administrators controlled all productive knowledge. Local autonomy, obligations and productive coordination have to be calibrated against separate evidence. The model still lacks a hydraulic graph, flood erosion/sedimentation cascades, explicit supervisor numbers, military labour schedules and rural migration. No claim is made that any tested rule reproduces Angkor's chronology.

## Reproduction and checks

Run `node run.cjs` in this extracted folder. It rewrites results.csv, summary.json and prints the check results. All food ledgers, migrant conservation and knowledge balances were checked within 1e-10. The largest food/population accounting residual was below 1.8e-15 normalized units. Knowledge transfer equals origin loss, less receiver overflow. Knowledge remains in [0,1]. Complete local retention exactly reproduces the learning-only histories. Constant productivity removes all economic differences caused solely by knowledge transfer in the tested placebo seeds.

engine.js is a separate experimental copy. The existing website models remain as previously deployed. The published motivation is Klassen, Ortman, Lobo and Evans, DOI 10.1007/s10816-021-09535-5; all dynamic learning, movement and budget-priority equations are Atlas additions.
