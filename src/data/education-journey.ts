import type { Journey } from './angkor-journey';
export const educationJourney: Journey = {
  "kicker": "Education & work · Credentials, schooling and labour markets",
  "title": "Who stays in school, and what is the diploma worth?",
  "lede": "A credential can teach a skill, rank an applicant or open a queue that would otherwise be closed. Those three jobs pull in different directions. This page follows one question through the Atlas models of education and work: when families, employers and states all respond to the same diploma, what can the evidence actually separate? The short answer is less than we would like, and the models are most useful when they show why.",
  "repo": "https://github.com/TreyModels/atlas-of-education",
  "family": "education",
  "why": [
    {
      "text": "Most families treat more schooling as a good thing. Most employers treat a diploma as a signal, not only a certificate of skill. Governments treat expansion as a target. Put those three responses together and a familiar puzzle appears: everyone invests more, yet the reward to the same credential can stay flat or fall. The queue lengthens rather than the payoff rising."
    },
    {
      "claim": "method",
      "text": "We ask two questions in order. First, what do the observed series and the published patterns say about school, work and credentials? Second, when an Atlas model is fitted to those patterns, what can it distinguish and what can it not? The second part is ours, and it is where the candid answer usually lives."
    },
    {
      "claim": "open",
      "text": "Nothing on this page is a verdict on a country’s education system. The models are mechanism tests and fitted descriptions. Where a result is a historical run, we say so. Where the code has been checked but the history has not, we say that too. Implementation checked is not empirical validation."
    }
  ],
  "chapters": [
    {
      "id": "why",
      "kicker": "Chapter 1 · The question",
      "title": "Why credentials and work belong in one story",
      "question": "Why should a page about schooling start with the labour market?",
      "evidence": [
        {
          "claim": "data",
          "text": "In Cambodia, the DHS 2021–22 puts the share of lower-secondary non-completers who come from the poorest 40% of households at 55–64%. Who leaves school early is not a random draw from the wealth distribution."
        },
        {
          "claim": "data",
          "text": "In China, gaokao registrants per birth 18 years earlier fell 5.3% over 2024–26 (raw −3.9%). A demographic fall in the applicant pool is not the same as a fall in college entry, and the series has to be read with that distinction in mind."
        },
        {
          "claim": "open",
          "text": "The Atlas family story puts the interpretive claim plainly: credentials are positional as much as productive. When everyone invests more, the queue can lengthen rather than the payoff rising. That claim organises the chapters below, but it is a hypothesis about mechanisms, not a measured law."
        },
        {
          "claim": "method",
          "text": "So the page follows the same order in every chapter: what is observed or published, what mechanism is proposed, what rules the model adds, what the stored experiments find, and what remains unsettled."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "The education family contains three live or fitted models — China youth unemployment, Cambodia child labour and schooling, and credential dynamics — plus four stored massification experiments. Each gets a model card at the bottom of the page. The full Education Atlas is an interface, not another model. Download bundles and duplicate interfaces are links, not extra entities."
        },
        {
          "claim": "method",
          "text": "Claims are labelled. “Data” means official statistics or surveys. “Sim” means an Atlas simulation result. “Open” means still unsettled. “Method” means how a model works. “Published” is reserved for peer-reviewed studies."
        }
      ],
      "result": [
        {
          "claim": "open",
          "text": "The family story’s bottom line is that credentials are positional as much as productive, and that this is why the same models feed the fertility story. The chapters below test how far that framing survives contact with the stored results."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "A framing is not a finding. The education models are calibrated or illustrative to different degrees, and several of the headline results are stored historical runs rather than current fits. Read each card’s state before reading its number."
        }
      ],
      "sources": [
        {
          "label": "Full Education Atlas",
          "href": "reference/education/index.html"
        },
        {
          "label": "Research library",
          "href": "research/index.html"
        },
        {
          "label": "Cambodia DHS 2021–22 (FR377)",
          "href": "https://www.dhsprogram.com/pubs/pdf/FR377/FR377.pdf"
        }
      ],
      "models": []
    },
    {
      "id": "china",
      "kicker": "Chapter 2 · China",
      "title": "The graduate queue and a step nobody can explain",
      "question": "Can a fitted labour-market model reproduce China’s graduate unemployment record, and what carries the rise?",
      "evidence": [
        {
          "claim": "data",
          "text": "The model is fitted to the supplied NBS graduate series. The on-disk full-window fit has a cost of 244.86 and a headline rise of +5.18 percentage points. A widened-bound refit lowers the cost to 227.25 and the rise to +5.06 points. The headline survives the refit."
        },
        {
          "claim": "sim",
          "text": "The Shapley decomposition of the on-disk headline is supply +1.47, composition −0.10, demand −0.04 and the Aug-2021 step +3.84, of a total +5.18 points. In the widened refit it is supply +1.91, composition −0.18, demand 0.00 and the step +3.33, of +5.06. The step carries most of the rise in both decompositions."
        },
        {
          "claim": "data",
          "text": "The step is not sourced at its fitted size. Sourced inputs give a data-sized step of about 0.020 to 0.068; the fitted full-window value is 0.30 on the old bounds and 0.32 on the widened bounds. The step size is also unstable across windows: it is 0.079 when the model is fitted to 2018–22 only."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "Graduates compete for jobs while some wait outside the labour force. The model combines graduate supply, job demand and access through networks. The reference was fitted to the displayed record; some mechanisms remain assumed. Changing a slider explores alternative explanations."
        },
        {
          "claim": "method",
          "text": "The official unemployment definition also changes in 2024. The model carries a measured rate and a broad rate. The broad rate counts unemployed plus waiting, over the labour force plus waiting, so it is the honest comparison for the accounting channel."
        }
      ],
      "result": [
        {
          "claim": "sim",
          "text": "With waiting and the same parameters, the measured rate rises by +5.07 points and the broad rate by +9.47 points. About 2.0 million graduates are waiting in 2024 to 2026. Graduates who wait leave both the numerator and the denominator of the measured rate, which is why the measured rate rises less."
        },
        {
          "claim": "sim",
          "text": "The “no waiting” counterfactual is +12.17 points in the current fit, not the +22.8 points in an older note. The +22.8 figure is not reproduced. Even the corrected waiting effect is about 7 points on the measured rate."
        },
        {
          "claim": "sim",
          "text": "A naive benchmark — the same month of 2022 — beats the early fit out of sample. On the true 2023 H1 holdout the early fit has MAE 7.14 against 2.50 for naive. On the verified Dec 2023 to Sep 2026 window the early fit has MAE 5.54 (n = 32) against 1.61 for naive."
        },
        {
          "claim": "sim",
          "text": "A plain four-parameter constant-rate lake null gets fit MAE 2.66, holdout 2023 H1 MAE 8.45 and verified new-method MAE 2.88. The categorical model gets 1.19, 7.14 and 5.54. Out of sample, the categorical model is not shown to beat the plain null. It has 11 parameters against 4."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "Status is fitted + free residual, not calibrated with a successful holdout. The Aug-2021 step is an unexplained fitted residual, not a sourced demand shock. Data-sized steps fit worse in sample and do not fix the vacancy check: the observed graduate-vacancy fall of about −22% year on year in H1 2025 is not reproduced by any variant, and the sign is wrong in all of them."
        },
        {
          "claim": "open",
          "text": "The parameter surface is flat. Seven parameters sat on bounds in the on-disk full fit, and several different parameter sets fit within a few cost units. lam_g is weakly identified: the free fit moves it between 0.004 and 1.0 across local optima, and pinning it at a data-derived value makes the in-sample fit worse while leaving the rise at 5–6 points."
        },
        {
          "claim": "open",
          "text": "The Tilly mechanisms presented as supported are set, not estimated: secure posts 10% of entry, hoarding 40%, wage wedge 20%, insider split 50%. No hukou, party-membership or parental-sector data exists in the inputs, so the insider line and the wedges are untested. Open microdata with those variables exist (CFPS, CCSS), so the claims are testable but untested."
        }
      ],
      "maths": {
        "plain": "A naive forecast says next year will look like the same month last year. The model has to beat that before its mechanisms deserve attention. On the 2023 H1 holdout the model’s average error is 7.14 percentage points; the naive rule’s is 2.50. A smaller error is better, so the naive rule wins.",
        "formula": "MAE = (1/n) · Σ |forecast − observed|",
        "symbols": [
          [
            "MAE",
            "mean absolute error, in percentage points"
          ],
          [
            "n",
            "number of months compared"
          ],
          [
            "forecast",
            "the model’s or naive rule’s value for that month"
          ],
          [
            "observed",
            "the recorded series value"
          ]
        ],
        "example": "The early-fit holdout MAE is 7.14 points and the naive MAE is 2.50 points on the same 2023 H1 months. The verified Dec 2023 to Sep 2026 window gives 5.54 against 1.61."
      },
      "sources": [
        {
          "label": "Youth review: bounds, step, holdout and lake null",
          "href": "https://github.com/TreyModels/atlas-of-education/blob/main/experiments/youth-review/README.md"
        },
        {
          "label": "China forecast ledger",
          "href": "https://github.com/TreyModels/atlas-of-education/blob/main/research/china-forecast-ledger/README.md"
        },
        {
          "label": "Full Education Atlas",
          "href": "reference/education/index.html"
        }
      ],
      "models": [
        "china"
      ]
    },
    {
      "id": "cambodia",
      "kicker": "Chapter 3 · Cambodia",
      "title": "Child work, school and a seed spread that swallows small effects",
      "question": "Which policies change child labour, and which differences are smaller than the simulation’s own noise?",
      "evidence": [
        {
          "claim": "data",
          "text": "The Cambodia household simulation is calibrated on out-of-school rates. Its costs are illustrative: the cost index’s unit costs are invented and unsourced, and the engine’s school values (vPrim, vLow, vUp) are calibrated, not measured. That affects the level of child labour more than the spread."
        },
        {
          "claim": "sim",
          "text": "The reference run has 6,000 households over 12 years, 2025 to 2036, with every lever at zero and the Thailand route open. Its national child labour rate in 2036 is 14.01%, with a seed standard deviation of 0.46 percentage points. The p5–p95 range is 13.40% to 14.71%."
        },
        {
          "claim": "sim",
          "text": "Policy and reference runs share matched seeds across the 12 simulated years, so the interface exposes the difference each policy makes. The seed comparison uses 50 seeds, 50 reference histories and 13 single-lever scenarios at half of each slider’s maximum, or at zero for the Thailand route."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "Children can attend school and work at the same time. The model asks how school costs, what school offers, enforcement, the credential floor and migration change that balance. The reference has no added programme and keeps the Thailand route open."
        },
        {
          "claim": "method",
          "text": "The yardstick is the reference’s own seed spread. A policy difference is called “smaller than seed spread” when its absolute mean paired difference is below the reference standard deviation for that output. That is a noise check, not a significance test."
        }
      ],
      "result": [
        {
          "claim": "sim",
          "text": "Five of the 13 single-lever settings move the national child labour rate in 2036 by less than the reference seed SD of 0.46 points: leftSupport −0.26, bridging −0.44, ban −0.32, garmentBoom +0.02 and closing the Thailand route 0.00. Harvest is just above the line at −0.50 (ratio 1.08)."
        },
        {
          "claim": "sim",
          "text": "Several effects are larger than the spread: cash −4.82, cashU −2.07, protection −2.20, feeding −2.30, tutorFix −1.34 and debtRelief −1.28 points. The smaller-than-spread effects are not all zero: under common seeds leftSupport (t = −3.5), bridging (t = −6.6) and ban (t = −4.4) are reliably below zero, but they are small compared with a single history’s variation."
        },
        {
          "claim": "sim",
          "text": "Closing the Thailand route leaves national child labour unchanged, but teens working away from home fall by 10.0 points (about 29 reference SDs, paired t = −206). The migration channel is substituted, not removed: the same children end up in local work or school. Read the national rate and the migrant-teen rate together."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "Status is calibrated out-of-school rates plus illustrative costs. Causal policy effects are not yet established: programme effect sizes are stylised, and the rural school-retention fit needs a large unexplained adjustment."
        },
        {
          "claim": "open",
          "text": "The cost index is not a cost estimate. For leftSupport the denominator is small, about 113 child-years avoided on average, so the per-seed ratio is unstable: its mean is 8.4 over the 43 seeds with positive avoidance and the pooled figure is 4.2. Do not quote either."
        },
        {
          "claim": "open",
          "text": "Half-maximum levels are arbitrary, and a different level changes the size of each difference while leaving the spread unchanged. The paired design is weaker for the Thailand-route scenario because setting thaiOpen below 1 draws extra random numbers. Seeds 1 to 50 were used; the app uses seed 7 with up to 8 histories, so its figures are not reproduced exactly."
        }
      ],
      "maths": {
        "plain": "Under matched seeds, each scenario is compared with the reference history for the same seed. The mean paired difference is the average policy effect. The reference seed standard deviation says how much a single history moves anyway. If the mean difference is smaller than that spread, the effect is hard to see in one run even if it is reliably non-zero across many seeds.",
        "formula": "d_s = scenario_s − reference_s;   mean difference = (1/S) Σ d_s;   reference SD = √(Σ(reference_s − mean_reference)² / (S − 1))",
        "symbols": [
          [
            "S",
            "number of seeds, 50 in the stored run"
          ],
          [
            "scenario_s",
            "national child labour rate in 2036 under the scenario for seed s"
          ],
          [
            "reference_s",
            "the same output in the reference history for seed s"
          ],
          [
            "d_s",
            "the paired difference for seed s"
          ]
        ],
        "example": "The reference mean is 14.01% and its seed SD is 0.46 points. leftSupport has mean paired difference −0.26 points, which is 0.56 of the SD, so it is classed as smaller than seed spread. Cash has −4.82 points, which is 10.37 of the SD, so it is not."
      },
      "sources": [
        {
          "label": "Cambodia child labour: seed spread of headline outputs",
          "href": "https://github.com/TreyModels/atlas-of-education/blob/main/experiments/camchild-seeds/README.md"
        },
        {
          "label": "The Cambodia household engine",
          "href": "engines/camchild.js"
        },
        {
          "label": "Full Education Atlas",
          "href": "reference/education/index.html"
        }
      ],
      "models": [
        "cambodia"
      ]
    },
    {
      "id": "credentials",
      "kicker": "Chapter 4 · Credential dynamics",
      "title": "The credential floor and the constraint that decides the verdict",
      "question": "Do the data discriminate a relational floor in schooling from human-capital or positional stories?",
      "evidence": [
        {
          "claim": "data",
          "text": "The matched test is Cambodia. UIS lower-secondary completion by wealth quintile, computed from DHS rounds, gives a 2021 profile of 29, 48, 54, 66 and 79% from poorest to richest. The observed share of lower-secondary non-completers from the poorest 40% is 55–64%."
        },
        {
          "claim": "data",
          "text": "Vietnam has a second test: the MICS 2014 upper-secondary adjusted net attendance profile for ages 15–17 is 40.4, 67.3, 74.3, 85.4 and 93.3%. China’s gaokao registrants per birth 18 years earlier fell 5.3% over 2024–26, while every structure predicts a 3–11% rise in college entry."
        },
        {
          "claim": "sim",
          "text": "Each country × structure gets 24,000 parameter draws. With a hard liquidity threshold, Cambodia accepts 1,361 human-capital draws, 800 positional draws and 463 relational draws. The relational structure predicts that 85% [69–97] of non-completers come from the poorest 40%, against 55–64% observed. No draw fits any quintile profile."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "Students may value a credential for earnings, relative position or access through relationships. The threshold is the rule that matters. A hard liquidity threshold creates a completion cliff by wealth: households either can or cannot pay. A graded threshold lets them trade school against work at the margin."
        },
        {
          "claim": "method",
          "text": "The premium counterfactual now compares the falling-premium and baseline paths in the same year, 2035. Older v2.1 values measured change from 2024 along the falling-premium scenario, including income growth, so they do not isolate the premium intervention. Those older values are historical. The paired same-year 2035 effect must be rerun."
        }
      ],
      "result": [
        {
          "claim": "sim",
          "text": "With the hard threshold no structure fits the full wealth profile, and the relational floor fails. With a graded threshold all three structures fit Cambodia’s and Vietnam’s full quintile profiles. The profile-fitted structures predict 57–58% of Cambodian non-completers from the poorest 40%, inside the observed 55–64%."
        },
        {
          "claim": "sim",
          "text": "In the graded fits the relational-weight posterior equals its prior. Cambodia’s relational posterior is 0.38 [0.04–0.75] against a prior of 0.40 [0.04–0.76], with KS p = 0.60; the profile-fitted value is 0.43, p = 0.55. The data do not discriminate the relational floor."
        },
        {
          "claim": "sim",
          "text": "The projections are fragile. Under a 40% premium fall by 2035 the Q3+ completion change changes sign with the constraint: relational about 0 under the hard threshold against +10 points under the graded one; human capital −12 against −6. The older v2.1 values should not be quoted as premium effects."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "The earlier rejection of the relational floor came from the hard threshold rather than from the data. A hard threshold fits no quintile profile, so its verdicts are a ranking inside a misspecified model. A fourth rival, relative risk aversion, cannot be separated either."
        },
        {
          "claim": "open",
          "text": "Income level is a free scale parameter: income, cost and subsistence are in stylised units with no observed counterpart, and only the growth rate is sourced. Quintile child weights are assumed; DHS wealth quintiles hold equal shares of people, not children. Matching on children needs the DHS microdata (hv105, hv121, hv122, hv270), which require registration."
        },
        {
          "claim": "open",
          "text": "China is not explained by any structure in either version: the model’s sign is wrong for the 2024–26 gaokao fall. Rerouting is not evidence either: every structure reroutes about 60% of exiters in the Philippine run. Large KS p-values do not establish that prior and posterior are equal."
        },
        {
          "claim": "open",
          "text": "v1 had two code errors: it was not reproducible because it was seeded with Python’s per-process hash(), and its exit_low was read in 2035 and compared with 2021 data. The stored v2.1 results are historical, not a current fit."
        }
      ],
      "maths": {
        "plain": "A threshold rule says a household can pay for school only if income clears a line. A hard threshold makes that a cliff: just below the line, almost nobody continues; just above, almost everybody does. A graded threshold makes the chance of paying rise smoothly with income, so the same wealth profile can be produced without a cliff. When the graded rule fits, three different stories can produce the same share of leavers from the poorest households.",
        "formula": "hard: P(finance) = 1 if y ≥ y_sub + κ · cost, else p_fin;   graded: P(finance) rises smoothly in log y around the threshold",
        "symbols": [
          [
            "y",
            "household income in stylised units"
          ],
          [
            "y_sub",
            "subsistence requirement"
          ],
          [
            "κ",
            "the share of the school cost the household must cover"
          ],
          [
            "p_fin",
            "a small probability of paying below the hard threshold"
          ],
          [
            "graded",
            "a smooth logistic-type rise with one extra parameter, s_liq ~ U(0.1, 1.0)"
          ]
        ],
        "example": "The hard model predicts 85% [69–97] of Cambodian non-completers from the poorest 40%; the observed range is 55–64%. The graded model’s profile-fitted relational prediction is 58% [54–61]. The rule, not the theory, changes the verdict."
      },
      "sources": [
        {
          "label": "The relational-floor test in Cambodia, Vietnam and China (v2.1)",
          "href": "reference/credential-floor.md"
        },
        {
          "label": "Credential-floor research folder",
          "href": "https://github.com/TreyModels/atlas-of-education/blob/main/research/credential-floor/README.md"
        },
        {
          "label": "Cambodia DHS 2021–22 (FR377)",
          "href": "https://www.dhsprogram.com/pubs/pdf/FR377/FR377.pdf"
        }
      ],
      "models": [
        "credentials"
      ]
    },
    {
      "id": "massification",
      "kicker": "Chapter 5 · Massification experiments",
      "title": "Four stored experiments on the credential pipeline",
      "question": "What keeps a credential pipeline moving when families, employers and the state all respond?",
      "evidence": [
        {
          "claim": "method",
          "text": "The massification lab holds four stored experiments: parents and peers, three actors, unequal access, and persistence. Each has 8 seeds per setting. They are mechanism tests, not measurements of what happened in a country."
        },
        {
          "claim": "open",
          "text": "The lab says plainly what is imposed rather than estimated: parent peer pressure is inserted into the model; exclusion and organisational inertia are imposed interventions; removing an actor also changes other actors’ incentives; and some differences vary substantially by seed."
        },
        {
          "claim": "method",
          "text": "The four experiments ask different questions of the same pipeline. Parents and peers: can the pressure to keep up raise aspirations faster than completion? Three actors: how do households, employers and the state reinforce a credential pipeline? Unequal access: who gets into credential-screened jobs when access is restricted? Persistence: can credential screening persist after referral networks return?"
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "The models are agent-based. Families, employers and the state make choices of their own; together those choices can make education expand and leave its rewards unevenly distributed. The stored runs compare settings within each experiment, not across countries."
        },
        {
          "claim": "method",
          "text": "The catalogue entries are links into stored experiments, not live workbenches. The full Education Atlas is the interface; the massification page is a model lab. Download bundles and duplicate interfaces are not separate models."
        }
      ],
      "result": [
        {
          "claim": "sim",
          "text": "The stored runs are the result. The lab reports that parent peer pressure is inserted, exclusion and organisational inertia are imposed, and removing an actor changes other actors’ incentives. Those are mechanism statements, not measured causal effects."
        },
        {
          "claim": "open",
          "text": "The page warns that some differences vary substantially by seed. With 8 seeds per setting, a difference between settings can be a difference between seed draws unless the paired design and the spread are read together. The stored CSVs are the place to check that."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "These are simplified rules with a small number of random seeds. They ask what can happen under stated assumptions, not what caused massification in the real world. Implementation checked is not empirical validation."
        },
        {
          "claim": "open",
          "text": "Exclusion and organisational inertia are imposed interventions, not estimated parameters. Removing an actor also changes other actors’ incentives, so an “actor removed” run is not a clean counterfactual for that actor alone."
        }
      ],
      "sources": [
        {
          "label": "Massification and durable inequality: four stored experiments",
          "href": "research/massification/index.html"
        },
        {
          "label": "Parent experiment data (CSV)",
          "href": "research/massification/parent-runs.csv"
        },
        {
          "label": "Three-actor results (CSV)",
          "href": "research/massification/actor-runs.csv"
        },
        {
          "label": "Inequality results (CSV)",
          "href": "research/massification/inequality-runs.csv"
        }
      ],
      "models": [
        "massification-parents",
        "massification-actors",
        "massification-access",
        "massification-persistence"
      ]
    },
    {
      "id": "settle",
      "kicker": "Chapter 6 · What would settle it",
      "title": "The tests the current data cannot provide",
      "question": "What would separate the explanations once each fits the observed profile?",
      "evidence": [
        {
          "claim": "open",
          "text": "For the credential floor, a test that separates the structures needs a margin where they predict different things once each fits the wealth profile. Wealth gradients in completion cannot do this; the graded fits show that. Candidates are completion responses to a measured change in the premium — a panel of pay and completion by region — or eligibility discontinuities, such as jobs that require the credential regardless of skill."
        },
        {
          "claim": "open",
          "text": "For China, open microdata with hukou, party and parental sector exist (CFPS, CCSS), so the insider and outsider claims are testable but untested. The Aug-2021 step also needs a source that can be measured independently of the fit."
        },
        {
          "claim": "open",
          "text": "For Cambodia, the DHS microdata would remove the assumed child weights per quintile. For the child-labour simulation, the school values are calibrated rather than measured, and the cost index is unsourced; both are data problems before they are modelling problems."
        },
        {
          "claim": "open",
          "text": "For the massification experiments, more seeds and a pre-registered paired design would tell a setting difference from a seed difference. The lab already warns that some differences vary substantially by seed."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "The order of work is data first. A proposed signature is not evidence. A model written to produce one would still need testing on data it was not built from."
        },
        {
          "claim": "method",
          "text": "The same rule applies to every card on this page: implementation checked means the code, ledgers and stored results were verified, not that the history was validated. A historical run is not a current fit."
        }
      ],
      "result": [
        {
          "claim": "open",
          "text": "None of these tests is built and passed here. They are listed so that the next version can be judged against something it did not invent after the fact."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "A proposed test is not a finding. The earlier lesson stands: two rules that look different can leave the same trace, and a model that fits the trace can still be wrong about the mechanism."
        },
        {
          "claim": "open",
          "text": "The education family’s models are at different stages. China is fitted + free residual and loses to a naive benchmark out of sample. Cambodia is calibrated on out-of-school rates with illustrative costs. Credential dynamics is illustrative and its stored v2.1 premium results are historical. The four massification experiments are stored mechanism tests. None of that is a verdict on a country."
        }
      ],
      "sources": [
        {
          "label": "Full Education Atlas",
          "href": "reference/education/index.html"
        },
        {
          "label": "Research library",
          "href": "research/index.html"
        },
        {
          "label": "Review status and evidence gaps",
          "href": "https://github.com/TreyModels/atlas-of-education/blob/main/REVIEW_STATUS.md"
        }
      ],
      "models": []
    }
  ],
  "deeper": [],
  "models": {
    "china": {
      "id": "china",
      "title": "China youth unemployment (fitted labour-market model)",
      "purpose": "mechanism",
      "state": "developing",
      "note": "Fitted to the supplied NBS graduate series. Status: fitted + free residual. The +5 pp rise survives refits, but the Aug-2021 step carries most of it and is unexplained; a naive benchmark beats the model out of sample (2023 H1 MAE 7.14 vs 2.50; verified Dec 2023–Sep 2026 5.54 vs 1.61). The 2024 reporting-definition change and several labour-market responses remain assumptions.",
      "route": "china",
      "research": "https://github.com/TreyModels/atlas-of-education/blob/main/experiments/youth-review/README.md"
    },
    "cambodia": {
      "id": "cambodia",
      "title": "Cambodia child labour and schooling (household simulation)",
      "purpose": "mechanism",
      "state": "developing",
      "note": "6,000 households over 12 years, 2025–2036. Out-of-school rates are calibrated; the cost index is illustrative and its unit costs are unsourced. Five of 13 single-lever effects on the 2036 national child-labour rate are smaller than the reference seed SD of 0.46 pp. School values are calibrated, not measured.",
      "engine": "engines/camchild.js",
      "route": "cambodia",
      "research": "https://github.com/TreyModels/atlas-of-education/blob/main/experiments/camchild-seeds/README.md"
    },
    "credentials": {
      "id": "credentials",
      "title": "Credential dynamics and the credential floor",
      "purpose": "mechanism",
      "state": "developing",
      "note": "24,000 draws per country × structure. With a hard liquidity threshold no draw fits the wealth profile and the relational floor fails; with a graded threshold all three structures fit and predict 57–58% against 55–64% observed. Stored v2.1 results are historical; the premium counterfactual now compares falling and baseline paths in the same year (2035), and the paired effect must be rerun.",
      "route": "credentials",
      "research": "https://github.com/TreyModels/atlas-of-education/blob/main/research/credential-floor/README.md"
    },
    "massification-parents": {
      "id": "massification-parents",
      "title": "Massification · Parents & peers",
      "purpose": "mechanism",
      "state": "checked",
      "note": "Stored experiment, 8 seeds per setting. Parent peer pressure is inserted into the model, not estimated. The lab warns that some differences vary substantially by seed. A mechanism test, not a measurement of what happened in a country.",
      "research": "research/massification/index.html"
    },
    "massification-actors": {
      "id": "massification-actors",
      "title": "Massification · Three actors",
      "purpose": "mechanism",
      "state": "checked",
      "note": "Stored experiment, 8 seeds per setting. Households, employers and the state interact; removing an actor also changes other actors’ incentives, so an “actor removed” run is not a clean counterfactual for that actor alone.",
      "research": "research/massification/index.html"
    },
    "massification-access": {
      "id": "massification-access",
      "title": "Massification · Unequal access",
      "purpose": "mechanism",
      "state": "checked",
      "note": "Stored experiment, 8 seeds per setting. Exclusion is an imposed intervention, not an estimated parameter. It asks who gets into credential-screened jobs when access is restricted, not who gets in in any named country.",
      "research": "research/massification/index.html"
    },
    "massification-persistence": {
      "id": "massification-persistence",
      "title": "Massification · Persistence",
      "purpose": "mechanism",
      "state": "checked",
      "note": "Stored experiment, 8 seeds per setting. Organisational inertia is an imposed intervention. It asks whether credential screening can persist after referral networks return; it does not estimate how long that took anywhere.",
      "research": "research/massification/index.html"
    }
  },
  "bottomLine": "The education models agree on a shape: credentials are positional as well as productive, so more investment can lengthen the queue rather than raise the payoff. But the evidence separates the explanations poorly. China’s fitted model loses to a naive benchmark out of sample, Cambodia’s policy effects are calibrated to illustrative costs, the credential floor’s verdict depends on whether the liquidity constraint is hard or graded, and the massification experiments are stored mechanism tests with 8 seeds per setting. The most useful result is a sharper list of tests the current data cannot provide."
};
