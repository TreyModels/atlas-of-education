# The relational-floor test in Cambodia, Vietnam and China

Results note, v2, 13 November 2026. Replaces the 5 November note (v1). Model: `engine/relfloor_countries.py`, which uses the same household model as `engine/relfloor.py`. Output: `reference/relfloor_countries_v2.json`. v1's output is kept as `reference/relfloor_countries.json`. Each country × structure gets 24,000 parameter draws. Sources for every target: `inputs/credential_floor_sources.json`, with a URL, a table reference and a verification flag for each value.

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

## Results (sourced priors)

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

## Reading

1. **Cambodia: the relational floor fails the matched test.** Its 5th percentile (69%) is above the highest observed value (64%). Only 1.5% of accepted relational draws fall inside the observed range. Human capital fits: 22% of its draws fall inside, and its median is 7 points above the observed maximum. Positional is in between (12%). With v1's growth priors the verdict is the same and stronger: 0.3% of relational draws are inside.
2. **No structure fits Cambodia's full quintile profile.** Zero draws in any structure match all five 2014 and 2021 quintiles within 10 points. The model produces a cliff at the liquidity threshold, and quintiles above it complete at 75–99%. In the data, completion rises smoothly: 29, 48, 54, 66, 79%. Item 1 is therefore a ranking of three structures inside a model that misses the shape of the gradient. It is not a test of the relational floor against reality.
3. **Vietnam: both tests point the same way.** On Young Lives, human capital fits about eight times as often as the relational version. The surviving relational weight is small (median 0.10, against a prior median of 0.40). On the full MICS profile almost nothing fits: 10 human-capital draws, 2 positional and 0 relational out of 24,000 each. The cause is the same smooth middle-quintile rise the model cannot produce. MICS measures attendance at 15–17, not completion, so it is a shape test more than a level test.
4. **The posterior equals the prior in three of four countries** (v1 priors; the fourth is the Philippines, `relational_floor_test.md`). In Cambodia and China the relational-weight posterior is statistically indistinguishable from its uniform prior (KS p = 0.44 and 0.07). The data say nothing about relational weight there. Vietnam is the only country where the data move it. With sourced growth priors, Cambodia's posterior is formally different (KS D = 0.11), but its 90% interval still covers 96% of the prior's. China's moves, but on only 13 accepted draws.
5. **China is not explained by any structure.** Gaokao registrants per birth 18 years earlier fell 5.3% from 2024 to 2026 (raw −3.9%; births 2006 15.84m, 2008 16.08m). Every structure predicts a 2024–26 *rise* in college entry of 3–11% (5–95% across structures), because incomes keep growing after the pay ratio stops falling in 2023. Registrants are not entrants: they include repeaters and spring-gaokao vocational candidates, and enrolment kept rising. The test is not like-for-like, but the model's sign is wrong. The response to the 2018–23 pay fall, against a no-fall counterfactual, is human capital −7.8% [−10.9, −4.2], positional −6.1%, relational −5.1% [−6.9, −0.8]. It has no observed counterpart.
6. **Rerouting is not evidence.** Every structure reroutes about 60% of exiters (Philippine run).

## Limits

- **Income level is a free scale parameter.** Income, cost and subsistence are in stylised units with no observed counterpart. Only the growth rate is sourced, and it uses GDP per capita, not household income.
- **Quintile child weights are assumed.** DHS wealth quintiles hold equal shares of people, not of children. The observed range spans weights from 1:1 to 2:1 (poorest to richest). Matching on children needs the DHS microdata (`hv105`, `hv121`, `hv122`, `hv270`), which require registration with the DHS Program.
- **Timing.** UIS completion is measured 3–5 years after the official graduation age. The model compares it to the decision in the survey year.
- China's premium path uses graduate pay relative to the urban average as a stand-in for the college-vs-high-school premium.
- Vietnam's age-19 observation is mapped to 2013, although the cohort was born in 1994.
- One decision per child, with no grade-by-grade survival.
