# V6 Tilly extension: executed results

Completed **828 runs**, with 37,260 annual rows. Behavioral code and input hashes match the executed manifest.

All people and event histories are synthetic. The appointment cohort consists of initially clean, high-integrity outsiders placed in organizational head positions in the 2013 experimental intervention. These are not identified historical Xi appointees. Behavioral parameters remain unestimated.

## Reference comparison

8 seeds; 64 original appointees per run. Misconduct percentages refer to the final five-year mean across all officials. Cohort outcomes retain the original 64-person denominator, including people who retire while clean.

| Regime | Current misconduct | Cohort misconduct by year 10 | Cohort misconduct by year 30 | Cohort true-case removal by year 30 |
|---|---:|---:|---:|---:|
| Open supplier access | 31.5% | 81.8% | 87.1% | 5.7% |
| Adaptation removed | 32.5% | 83.0% | 87.5% | 6.4% |
| Weak enforcement | 34.0% | 83.2% | 87.7% | 3.9% |
| Sustained campaign | 32.5% | 83.0% | 87.5% | 6.4% |
| Emulation removed | 32.5% | 83.0% | 87.5% | 6.4% |
| Equal resource allocations | 33.8% | 52.7% | 68.8% | 2.5% |
| Low demand for assistance | 28.2% | 73.6% | 82.2% | 4.1% |
| Organizational reset | 32.3% | 82.0% | 86.9% | 5.9% |
| No outsider appointment | 32.5% | N/A | N/A | N/A |
| Obligations removed | 28.6% | 75.8% | 83.8% | 5.1% |
| Payment-blind promotion | 32.5% | 83.0% | 87.5% | 6.4% |
| Exchange protection removed | 32.5% | 83.0% | 87.5% | 6.4% |
| Stronger oversight | 28.1% | 81.1% | 86.9% | 22.5% |
| New mechanisms removed | 28.7% | 45.1% | 61.3% | 1.4% |
| Zero resource-attraction coefficient | 33.5% | 60.0% | 73.4% | 2.5% |

A true-case removal means the person was removed following a case tied to a modeled misconduct act. A false-case removal can affect someone with other misconduct in their history. Neither label supplies a complete moral classification of the person. Delayed sanctions after retirement remain in the event histories.

## Paired sensitivity across assumptions

12 Latin-hypercube parameter settings, 3 matched seeds each. Quantiles describe parameter sensitivity; seed MCSE describes simulation noise conditional on a setting. Neither is an uncertainty interval for the actual CCP.

| Comparison with sustained campaign | Outcome | Median effect | 5th–95th percentile | Points above / below zero | Median seed MCSE |
|---|---|---:|---:|---:|---:|
| Open supplier access | cohort_act_10 | -0.0052 | -0.0260 to +0.0052 | 2 / 8 | 0.0052 |
| Obligations removed | cohort_act_10 | -0.0651 | -0.2339 to -0.0057 | 0 / 11 | 0.0121 |
| Equal resource allocations | cohort_act_10 | -0.1562 | -0.4766 to -0.0359 | 1 / 11 | 0.0255 |
| Zero resource-attraction coefficient | cohort_act_10 | -0.1302 | -0.3966 to +0.0594 | 2 / 10 | 0.0156 |
| Stronger oversight | cohort_act_10 | -0.0339 | -0.0573 to -0.0081 | 0 / 12 | 0.0097 |
| Organizational reset | cohort_act_10 | -0.0156 | -0.0284 to +0.0000 | 0 / 9 | 0.0090 |
| Emulation removed | true_misconduct | +8.33e-07 | -3.57e-05 to +1.72e-05 | Numerically negligible | 8.04e-06 |
| No outsider appointment | true_misconduct | +0.0002 | +0.0000 to +0.0004 | 12 / 0 | 0.0001 |

Settings with exactly zero differences are omitted from the above/below counts. The emulation effects are numerically negligible at the substantive scale shown; signs on such small differences provide no useful directional evidence. At reference parameters, adaptation, exchange protection and the additional payment-based promotion term also have little effect at the reported precision. These comparisons do not establish those channels as necessary for the observed synthetic pattern.

## Cohort accounting

Across the reference campaign runs, 448 of 512 original appointees had at least one misconduct act; 33 were removed on true cases and 1 on false cases. Total exposure was 8718 person-years. At their first misconduct act, 189 appointees received illicit payments from other officials in the same step. That count excludes their own direct contract diversion and unpaid obligations.

For 310 appointees, the first recorded obligation owed preceded or occurred in the same step as their first misconduct. Assistance and obligation creation occur before misconduct within a step. This timing describes the simulated sequence and does not identify a causal effect by itself.

The closed cohort is observed through the fixed horizon or a competing employment exit/retirement. The reported cumulative event fraction retains clean retirees in its denominator. Annual first-act incidence uses only still-employed, never-acted people at the step opening. Empty risk sets are undefined.

## What drives the result

Largest Morris screening effects on ten-year cohort misconduct: resource_attraction, cohort_integrity, obligation_pressure, rent, request_pressure. Four paths and two seeds per point provide an exploratory screen. Discrete cohort outcomes have appreciable Monte Carlo noise; larger replication is needed before ranking small effects.

The resource gradient, obligation pressure and response to assistance requests enter the decision rule explicitly. Their effects are conditional consequences of these assumptions. Negative and zero request-pressure coefficients, negative resource-attraction coefficients, equal-resource allocation and a zero-attraction arm permit contrary patterns. Rank extraction amounts and extraction per unit of resource are saved separately.

Organizational imitation uses public output and filed cases per official. Legitimate assistance can discharge obligations without misconduct. Organizational closure changes supplier access and can exist without a corrupt award. The campaign and no-replacement arms differ only in the exogenous appointment shock; cohort metrics are undefined in the no-replacement arm.

The model retains a positive baseline probability of misconduct and a positive baseline closure target. Long-horizon onset and rebuilt closure therefore follow partly from imposed propensities. The informative tests are paired changes in outcomes, including the new-mechanisms-off control. Onset alone cannot establish that obligations caused it.

## Empirical limits and artifacts

The package retains the official annual panel, 2026 monitoring/budget records and selected CSET notices. Existing normalized macro drivers affect resource allocation. Neither the Tilly mechanisms nor the synthetic appointee event rates have been fitted to observed Chinese officials. Historical evaluation requires a dated appointment-at-risk cohort and conduct-specific evidence, alongside institutional coverage and censoring rules.

- `cohort_event_histories.csv`: immutable identities, first events and competing exits.
- `paired_effects_by_point.csv`: assumption-specific effects and seed MCSE.
- `rank_gradients.csv`: participation, extraction per official, extraction per resource and assistance exposure.
- `morris_elementary_effects.csv`: raw screening calculations.
- `robustness_differences.csv`: population-scale and initialization checks.
- `runs/`: complete annual series, cohort records, parameters and seeds.
- `../PEER_REVIEW.md`: review by the requested gpt-6.1-terra agent.

- `../CCPORG_ASSESSMENT.md`: audit of the career/event source supplied during execution.
