# The relational-floor test in Cambodia, Vietnam and China

Results note, 5 November 2026. Model: `engine/relfloor_countries.py` (same household model as `relfloor.py`). Output: `engine/results/relfloor_countries.json`. 24,000 parameter draws per country and structure. Follows `relational_floor_test.md` (Philippines).

## Setup

Same three-part credential value (human capital, positional, relational), cost, liquidity constraint and rerouting. What changes by country is the decision margin, the length of the credential, income level and growth, and the targets a draw must hit to be accepted.

| | Margin | Sourced targets |
|---|---|---|
| Cambodia | lower-secondary completion | 17% (2000), 37–49% (2010, two series disagree), 56–58% (2021). **No wealth gradient found.** |
| Vietnam | upper-secondary completion at 19 | 57.7% overall, **80.5% top quintile, 25.1% bottom** (Young Lives, 2013). |
| China | college entry | gross enrolment ~30% (2012), 48% (2019), 60.2% (2023). Relative graduate pay falls 0.75→0.60 (2018→2023). |

Sources: indexmundi and measuredworld (Cambodia completion), Young Lives Vietnam country report, MoE and NBS through China Daily and Yicai (China enrolment), SCMP, Global Times and The Star (exam registrations).

## Results

| | Fits history (accepted share of draws) | Relational weight, posterior median [5–95%] (prior 0–0.8) | Exits from the bottom 40%, median | Q3+ completion change if the relative premium falls 40% by 2035 |
|---|---|---|---|---|
| **Cambodia** human capital only | 4.4% | — | 65% | −11.5 pts |
| + positional | 3.9% | — | 83% | −4 pts |
| + relational | 3.3% | 0.37 [0.03, 0.76] | **98%** | ~0 |
| **Vietnam** human capital only | **6.1%** | — | 48% | −12.8 pts |
| + positional | 3.1% | — | 50% | −9.4 pts |
| + relational | **0.8%** | **0.09** [0.007, 0.35] | 53% | −6.5 pts |
| **China** human capital only | 0.3% | — | 56% | −14 pts |
| + positional | 0.7% | — | 67% | −5 pts |
| + relational | 0.5% | 0.30 [0.05, 0.75] | **91%** | ~0 |

## Reading

1. **Vietnam is the only country where history pushes back on the relational floor.** It is the only one with a sourced quintile gradient. Human capital fits history about eight times as often as the relational version, and the relational weight that survives is small. In Cambodia, China and the Philippines, the posterior for relational weight sits near the prior, meaning the data say nothing about it.
2. **Cambodia is where the household test would discriminate most.** Liquidity binds and the model gives sharply different answers on where leavers come from: about 65% from the bottom 40% under human capital, 98% under the relational floor. The Cambodia DHS 2021–22 has wealth-quintile attendance. That is the one table that would settle it. It is the only case where the paper's test is cheap and decisive.
3. **China cannot be settled from the enrolment series.** Three aggregate points fit all structures about equally (79, 165 and 120 accepted draws). Each structure predicts a different college-entry response to the 20% fall in relative graduate pay by 2023, measured against a no-fall counterfactual: human capital −6.8% [−9.9, −1.1], positional −4.7%, relational −0.9% [−5.7, 0]. Observed:
   - Gaokao registrants fell 13.42m → 12.9m (−3.9%) from 2024 to 2026. This sits inside every band except the relational median. It is not corrected for cohort size, which no source I fetched addresses, and the later fall is outside the pay-ratio window.
   - Postgraduate-exam applicants fell 4.74m → 3.88m (−18%) from 2023 to 2025. That is a bigger response than any structure predicts for college entry, but it is a different margin. The paper itself says positional value dominates at elite gates. A fall there fits the human-capital and positional versions better than the paper's prediction that positional competition **intensifies** under saturation.
4. **Rerouting is not evidence.** Civil-service applicants rose 2.6m → 3.7m, but every structure reroutes about 60% of exiters (Philippine run).

## What would change the answer

- Cambodia DHS 2021–22 attendance by wealth quintile, 14–17: the share of non-attenders from the bottom two quintiles.
- China: gaokao registrants adjusted for the 18-year-old cohort, and who the 2025–26 non-registrants are (vocational leavers, rural, urban).
- Vietnam: MICS 2014 quintile enrolment (40, 67, 74, 85, 93% for upper secondary) as a full profile test. I used only the Young Lives end quintiles. A smooth profile across middle quintiles argues against a liquidity-threshold floor.

## Limits

- Income level and growth priors by country are stylised and wide, not sourced.
- China's premium path uses graduate pay relative to urban average as a stand-in for the college-vs-high-school premium.
- Vietnam's age-19 observation is mapped to 2013 although the cohort was born in 1994.
- One decision per child, no grade-by-grade survival.
- The Cambodian 2010 series disagree (36.7% vs 49.4%), so that target is wide.
