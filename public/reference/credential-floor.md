# The relational-floor test in Cambodia, Vietnam and China

Results note, v2.1, 14 November 2026. Replaces the 5 November note (v1). Model: `engine/relfloor_countries.py`, which uses the same household model as `engine/relfloor.py`. Output: `reference/relfloor_countries_v2.json`. v1's output is kept as `reference/relfloor_countries.json`. Each country × structure gets 24,000 parameter draws. Sources for every target: `inputs/credential_floor_sources.json`, with a URL, a table reference and a verification flag for each value.

## What changed from v1

1. **The v1 Cambodia comparison used the wrong year.** v1 reported the share of non-completers from the bottom 40% (`exit_low`) in 2035, after 11 extrapolated years. The DHS comparison in `research/shadow/credential_floor_dhs.zip` then tested that 2035 value against 2021 data. v2 reads it in the survey year.
2. **Cambodia is now tested on the model's own margin.** v1 had no wealth gradient for Cambodia. The DHS bundle then used DHS Table 2.12, which counts all children aged 12–18 who are not in secondary school. v2 uses UIS lower-secondary completion by wealth quintile (CR.2.Q1–Q5). UIS computes it from DHS 2005, 2010, 2014 and 2021–22 microdata. This covers most of what the DHS microdata request was meant to settle (review item 2.1). The microdata are still needed to weight quintiles by children rather than people (see Limits).
3. **Vietnam has a second test.** The full MICS 2014 quintile profile (Table ED.5A, upper-secondary adjusted net attendance, ages 15–17): 40.4, 67.3, 74.3, 85.4, 93.3%.
4. **China's gaokao registrants are divided by births 18 years earlier** (NBS).
5. **Income growth priors are sourced.** The band is the WDI real GDP per capita CAGR for 2000–2023, ±1 point: Cambodia 4.6–6.6%, Vietnam 4.1–6.1%, China 6.8–8.8%. v1 used 3–6%, 4–6.5% and 5–9%.
6. **Each posterior is shown next to its prior**, with a Kolmogorov–Smirnov test.
7. **Seeds are deterministic.** v1 seeded with Python's per-process string hash, so v1 runs cannot be reproduced exactly. Rerunning v2 with v1's priors (`--v1-priors`) gives acceptance counts within about 10% of v1's.

## Targets

| | Margin | Targets |
|---|---|---|
| Cambodia | lower-secondary completion | 17% (2000), 33–50% (2010), 50–62% (2021). **By quintile (UIS CR.2):** 17, 25, 37, 53, 65% (2014); 29, 48, 54, 66, 79% (2021). |
| Vietnam | upper-secondary completion | Young Lives, age 19 (2013): 57.7% overall, 80.5% top quintile, 25.1% bottom. MICS 2014 profile above. |
| China | college entry | gross enrolment ~30% (2012), 48% (2019), 60.2% (2023); relative graduate pay 0.75 → 0.60 (2018 → 2023). |

## Results (sourced priors, hard liquidity threshold)

| | Accepted draws (of 24,000) | Bottom-40% share of non-completers, 2021, median [5–95%] | Relational weight: posterior vs prior | Q3+ completion change if the premium falls 40% by 2035 |
|---|---|---|---|---|
| **Cambodia** human capital | 1,361 | 71% [54, 89] | — | −12 pts |
| + positional | 800 | 78% [59, 92] | — | −6 pts |
| + relational | 463 | **85% [69, 97]** | 0.32 [0.04, 0.74] vs prior 0.40 [0.04, 0.76] | ~0 |
| **Vietnam** human capital | 1,407 | — | — | −13 pts |
| + positional | 799 | — | — | −9 pts |
| + relational | 180 | — | **0.10 [0.01, 0.37]** vs 0.40 [0.04, 0.76] | −6 pts |
| **China** human capital | 55 | — | — | −13 pts |
| + positional | 51 | — | — | −8 pts |
| + relational | 13 | — | 0.15 [0.02, 0.49] vs 0.40 [0.04, 0.76] (13 draws) | −6 pts |

**Observed Cambodia value:** 55–64% of lower-secondary non-completers in 2021 were in the poorest 40% of households. The range runs from equal child weights per quintile up to twice as many children in the poorest fifth as in the richest. The 2014 figure is 52–61%.

## Robustness: graded liquidity constraint (decides the verdict)

The model above has a hard liquidity threshold: a household below `y_sub + kappa x cost` cannot pay, except with probability `p_fin`. That makes a cliff in completion by wealth, and no draw fits Cambodia's or Vietnam's smooth quintile profile. The graded variant (`--smooth-liq`) makes the chance of financing rise smoothly in log income around the threshold. It adds one parameter, `s_liq` ~ U(0.1, 1.0). Output: `reference/relfloor_countries_v2_smoothliq.json`.

| | Accepted, aggregate test (HC / POS / REL) | Accepted, full quintile profile | Bottom-40% share of non-completers, 2021, REL median [5–95%] | Relational weight posterior (prior 0.40 [0.04, 0.76]) |
|---|---|---|---|---|
| Cambodia | 689 / 633 / 565 | 64 / 91 / 44 | 67% [57, 80]; profile-fitted: 58% [54, 61] | 0.38 [0.04, 0.75], KS p = 0.60; profile 0.43, p = 0.55 |
| Vietnam (Young Lives) | 6,056 / 5,563 / 5,061 | MICS: 996 / 1,370 / 1,626 | — | 0.36 [0.03, 0.75], KS D = 0.05; MICS 0.40, p = 0.36 |
| China | 9 / 25 / 11 | — | — | 0.28 [0.07, 0.71], p = 0.36 (11 draws) |

## Reading

1. **The data do not discriminate the relational floor.** Under the graded constraint, all three structures fit Cambodia's and Vietnam's full quintile profiles. In those fits the relational-weight posterior equals its prior. The profile-fitted structures all predict 57–58% of Cambodian non-completers from the bottom 40%, inside the observed 55–64%.
2. **The earlier verdicts come from the hard threshold.** With it, the relational floor fails Cambodia's matched test (85% [69, 97] predicted, against 55–64% observed). Vietnam's relational weight is also pushed down (0.10). But that model fits no quintile profile (0 draws in Cambodia, at most 10 in Vietnam). Its verdicts are a ranking inside a misspecified model. They are not evidence about the relational floor.
3. **Projections are not robust.** The Q3+ completion change under a 40% premium fall by 2035 changes sign with the constraint: relational ~0 (hard) vs +10 points (graded); human capital −12 vs −6. Do not quote them.
4. **The posterior equals the prior almost everywhere.** In the hard-threshold model this holds in Cambodia and China (KS p = 0.44 and 0.07, v1 priors) and in the Philippines (`relational_floor_test.md`). In the graded model it holds in all three countries tested here.
5. **China is not explained by any structure in either version.** Gaokao registrants per birth 18 years earlier fell 5.3% over 2024–26 (raw −3.9%). Every structure predicts a 3–11% rise in college entry. Registrants are not entrants: they include repeaters and vocational candidates, and enrolment kept rising. The model's sign is still wrong.
6. **Rerouting is not evidence.** Every structure reroutes about 60% of exiters (Philippine run).

## What would change the answer

A test that separates the structures needs a margin where they predict different things *once each fits the wealth profile*. Wealth gradients in completion cannot do this; the graded fits show that. Candidates: completion responses to a measured change in the premium (a panel of pay and completion by region), or eligibility discontinuities (jobs that require the credential regardless of skill).

## Limits

- **Income level is a free scale parameter.** Income, cost and subsistence are in stylised units with no observed counterpart. Only the growth rate is sourced, and it uses GDP per capita, not household income.
- **Quintile child weights are assumed.** DHS wealth quintiles hold equal shares of people, not of children. The observed range spans weights from 1:1 to 2:1 (poorest to richest). Matching on children needs the DHS microdata (`hv105`, `hv121`, `hv122`, `hv270`), which require registration with the DHS Program.
- **Timing.** UIS completion is measured 3–5 years after the official graduation age. The model compares it to the decision in the survey year.
- China's premium path uses graduate pay relative to the urban average as a stand-in for the college-vs-high-school premium.
- Vietnam's age-19 observation is mapped to 2013, although the cohort was born in 1994.
- One decision per child, with no grade-by-grade survival.
