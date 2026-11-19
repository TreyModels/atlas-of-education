import type { Journey } from './angkor-journey'

export const fertilityJourney: Journey = {
  "kicker": "Fertility & family formation",
  "title": "Fertility & family formation",
  "lede": "Why did fertility fall across six East and Southeast Asian places, and what can still move it? This journey separates observed period fertility from assumed mechanisms, simulated scenarios and open questions. Read the labels: data, simulation, assumption, open.",
  "family": "fertility",
  "repo": "https://github.com/TreyModels/atlas-of-education",
  "why": [
    {
      "claim": "open",
      "text": "Fertility fell almost everywhere in the region, often far below replacement. The question is not only why, but which parts of the explanation are observed, which are assumed, and which remain open."
    },
    {
      "claim": "method",
      "text": "The research treats six places — the Philippines, Thailand, South Korea, Japan, Hong Kong and China — as a small panel. Six places is too few for confident leave-one-out inference: each held-out error rests on one place, so the spread is wide and unstable, not a confidence interval."
    },
    {
      "claim": "method",
      "text": "Period total fertility rate (TFR) mixes timing with quantity. A fall in period TFR can reflect postponed births rather than fewer children per woman. This is a central limitation, not a footnote."
    }
  ],
  "chapters": [
    {
      "id": "observed-tfr",
      "kicker": "Observed data",
      "title": "Six places, observed period fertility",
      "question": "What does the observed period TFR actually show across the six places?",
      "evidence": [
        {
          "claim": "data",
          "text": "Period TFR from World Bank series via FRED, 1961–2024, for the Philippines, Thailand, South Korea, Japan, Hong Kong and China. The page series matches the panel TFR exactly."
        },
        {
          "claim": "data",
          "text": "All six places fell below their development path at once after 2015, by about 0.46 children on average in the fitted comparison. This is an observed pattern in the fitted residuals, not a causal estimate."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "Observed series are kept separate from fitted model lines. Each model line on the page is fitted on the other five places and predicts the held-out one."
        }
      ],
      "result": [
        {
          "claim": "data",
          "text": "Held-out mean absolute error, 1985–2024: development model 0.40 (range 0.24 Hong Kong to 0.81 Philippines); with matching and the post-2015 dummy 0.39 (range 0.13 Hong Kong to 0.94 Philippines)."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "Six held-out errors do not make a confidence interval. The spread is wide and depends on which place is held out."
        }
      ],
      "sources": [
        {
          "label": "Fertility collapse lab",
          "href": "research/fertility.html"
        },
        {
          "label": "Fertility research bundle (ZIP)",
          "href": "research/fertility/fertility-research-full.zip"
        }
      ],
      "models": [
        "development-survival",
        "matching-dummy"
      ],
      "interactive": "beta"
    },
    {
      "id": "survival-levels",
      "kicker": "Observed levels, not a causal floor",
      "title": "Survival and fertility: a levels relation that fails the trend check",
      "question": "Does rising life expectancy explain falling fertility?",
      "evidence": [
        {
          "claim": "data",
          "text": "In levels, life expectancy tracks each place’s fertility decline closely (R² 0.65–0.94 across places)."
        },
        {
          "claim": "data",
          "text": "In first differences the relation does not survive. Four of twelve differenced slopes are significant at 5%, with signs disagreeing across places and small explained variance except in China (driven by the 1961–63 swing)."
        },
        {
          "claim": "data",
          "text": "Engle-Granger finds no cointegration at 5% in any place over 1961–2024 (lowest p 0.079, Philippines). Over 1964–2024 only Japan passes, while its differenced slope is near zero."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "A levels fit is a shared trend, not a predictor. The trend check is in the project repository under experiments/fertility-trend-check."
        }
      ],
      "result": [
        {
          "claim": "data",
          "text": "The levels relation is real across places but is not shown to be a stable year-to-year relation. The 1.3–1.5 “floor” is a fitted curve, not a finding, and the held-out 2024 predictions do not show it for Japan and Korea."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "Period TFR, n = 64 per place, two covariates only, and pooled standard errors that ignore cross-place dependence. Unit-root and cointegration tests have low power at this sample size."
        }
      ],
      "maths": {
        "plain": "Compare the slope of fertility on life expectancy in levels with the slope in year-to-year changes.",
        "formula": "ΔTFRₜ = α + β·ΔLEₜ + εₜ",
        "symbols": [
          [
            "ΔTFRₜ",
            "change in period TFR from year t−1 to t"
          ],
          [
            "ΔLEₜ",
            "change in life expectancy"
          ],
          [
            "β",
            "differenced slope; near zero or sign-flipping across places"
          ]
        ],
        "example": "Philippines: levels slope −0.380 (R² 0.89); differenced slope +0.019 (p 0.0001, wrong sign, R² 0.06)."
      },
      "sources": [
        {
          "label": "Fertility trend check (repository)",
          "href": "https://github.com/TreyModels/atlas-of-education/blob/main/experiments/fertility-trend-check/README.md"
        },
        {
          "label": "Fertility collapse lab",
          "href": "research/fertility.html"
        }
      ],
      "models": []
    },
    {
      "id": "credential-cohort",
      "kicker": "Simulated mechanism",
      "title": "Children as credential projects",
      "question": "Does mass higher education turn childrearing into an arms race that lowers births?",
      "evidence": [
        {
          "claim": "sim",
          "text": "In the cohort model — an illustration with invented parameters — each child costs more to raise competitively, lowering births in every regime by roughly 0.4 children, mostly second births."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "The cohort model is a synthetic simulation. Its parameters are invented to show what the mechanism can do, not measured effects."
        }
      ],
      "result": [
        {
          "claim": "sim",
          "text": "The credential-race mechanism reproduces a fall of about 0.4 children through fewer births per married couple. This is a simulation result, not an estimate."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "Some conclusions are partly built into how the model is coded. National enrolment ratios could not confirm the marriage-jam component (failed the placebo test)."
        }
      ],
      "sources": [
        {
          "label": "Fertility collapse lab",
          "href": "research/fertility.html"
        },
        {
          "label": "Fertility research bundle (ZIP)",
          "href": "research/fertility/fertility-research-full.zip"
        }
      ],
      "models": [
        "credential-cohort"
      ]
    },
    {
      "id": "marriage-jam",
      "kicker": "Simulated, not yet proven",
      "title": "The marriage market jam",
      "question": "Where births require marriage, does women overtaking men in status leave many unmatched?",
      "evidence": [
        {
          "claim": "sim",
          "text": "In the mechanism lab, the “credential floor plus women marrying up” combination was the only one that reproduced all five Korean facts — unmarried educated women alongside unmarried less-educated men."
        },
        {
          "claim": "sim",
          "text": "The jam is large in East Asia and shrinks by about 70% where births outside marriage are common, as in the Philippines."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "The mechanism lab is a synthetic cohort of 3,000 women and men searching for partners from age 18 to 45. Parameters are invented; it shows what the mechanism can do, not measured effects."
        }
      ],
      "result": [
        {
          "claim": "sim",
          "text": "The marriage squeeze appears only in simulations. National enrolment data cannot confirm it."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "A real model crowd needs new kinds of data, above all who stays unmarried by sex and education."
        }
      ],
      "sources": [
        {
          "label": "Fertility collapse lab",
          "href": "research/fertility.html"
        },
        {
          "label": "Fertility research bundle (ZIP)",
          "href": "research/fertility/fertility-research-full.zip"
        }
      ],
      "models": [
        "mechanism-assortative"
      ]
    },
    {
      "id": "late-marriage-fecundity",
      "kicker": "Simulated, calibrated to medical data",
      "title": "Late marriage meets the biological clock",
      "question": "How much of the fertility fall comes from later marriage meeting declining fecundity?",
      "evidence": [
        {
          "claim": "sim",
          "text": "The fecundity-age curve is calibrated to medical fecundity data. Every year of delay costs more than the last, steepening after 33–35."
        },
        {
          "claim": "sim",
          "text": "Share of the fertility fall explained by late marriage in the simulation: Hong Kong 26%, Korea 21%, China 18%, Thailand and the Philippines 1–2% (still marrying in their mid-20s)."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "Medical fecundity curves describe individual biological capacity. They are not causal validation of aggregate fertility."
        }
      ],
      "result": [
        {
          "claim": "sim",
          "text": "IVF recovers only about a sixth of this loss in the simulation — checked against Korea’s 15% of births from fertility treatment."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "The IVF and policy estimates are simulated conditional effects, not policy forecasts. The fecundity curve is a calibration input, not a test of the aggregate story."
        }
      ],
      "sources": [
        {
          "label": "Fertility collapse lab",
          "href": "research/fertility.html"
        },
        {
          "label": "Fertility research bundle (ZIP)",
          "href": "research/fertility/fertility-research-full.zip"
        }
      ],
      "models": [
        "fecundity-age",
        "ivf-policy"
      ]
    },
    {
      "id": "post-2015-shock",
      "kicker": "Observed pattern, open cause",
      "title": "A post-2015 period dummy",
      "question": "What happened to fertility after 2015, and can we say why?",
      "evidence": [
        {
          "claim": "data",
          "text": "All six places fell below their development path at once, by about 0.46 children on average — 0.71 against their own earlier, recovering trends."
        },
        {
          "claim": "data",
          "text": "The drop was the same whether or not births require marriage, so it is not the marriage jam. Nothing in pre-2015 trends predicted it: models trained up to 2014 forecast 1.86 for China in 2024; the actual figure was 1.01."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "A period dummy fits the timing. It cannot separate competing explanations that share the same timing."
        }
      ],
      "result": [
        {
          "claim": "open",
          "text": "The tested timing patterns did not identify a common cause. A period dummy cannot distinguish diffusion between places, environmental exposures, technology or economic shocks; stronger causal evidence is needed."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "A period dummy is a description of when, not a causal identification of why."
        }
      ],
      "sources": [
        {
          "label": "Fertility collapse lab",
          "href": "research/fertility.html"
        },
        {
          "label": "Fertility research bundle (ZIP)",
          "href": "research/fertility/fertility-research-full.zip"
        }
      ],
      "models": [
        "shock-suite",
        "microplastics-test"
      ]
    },
    {
      "id": "tipping",
      "kicker": "Illustration with invented parameters",
      "title": "Can a temporary shock do permanent damage?",
      "question": "Can a temporary shock tip fertility into a lasting low?",
      "evidence": [
        {
          "claim": "sim",
          "text": "In the tipping lab, people adopt a “small family, no rush to marry” life plan once social pressure passes their personal threshold. A shock runs in years 30–39, then stops; policy can push back from year 45."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "This is an illustration with invented parameters. Traps need two things: strong peer influence and a fairly uniform society."
        }
      ],
      "result": [
        {
          "claim": "sim",
          "text": "With strong feedback, undoing a collapse took about eight times the push that would have prevented it."
        },
        {
          "claim": "data",
          "text": "Japan and Hong Kong show a pull back toward their path; Japan recovered from 1.26 to 1.45. Korea and China show none. The data did not confirm a clean tipping cliff."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "The tipping result is a simulation, not an estimate. The observed data do not confirm a clean cliff."
        }
      ],
      "sources": [
        {
          "label": "Fertility collapse lab",
          "href": "research/fertility.html"
        },
        {
          "label": "Fertility research bundle (ZIP)",
          "href": "research/fertility/fertility-research-full.zip"
        }
      ],
      "models": [
        "momentum-test"
      ]
    },
    {
      "id": "policy",
      "kicker": "Simulated conditional effects",
      "title": "What policy can do — in the simulation",
      "question": "Which simulated levers move births, and by how much?",
      "evidence": [
        {
          "claim": "sim",
          "text": "Simulated effect on births per woman: accepting births outside marriage +0.37; more people marrying (+10 points) +0.12; support for second births +0.13; marrying 2 years earlier +0.04; IVF for everyone who needs it +0.02; cash (+30%) +0.08; best four combined +0.35."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "These are simulated conditional effects from a Korea-like synthetic cohort with baseline completed fertility 1.07. They are not policy forecasts."
        }
      ],
      "result": [
        {
          "claim": "sim",
          "text": "Even the combined package leaves Korea far below replacement in the simulation."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "Simulated conditional effects depend on invented parameters and model structure. They should not be read as predictions of real policy outcomes."
        }
      ],
      "sources": [
        {
          "label": "Fertility collapse lab",
          "href": "research/fertility.html"
        },
        {
          "label": "Fertility research bundle (ZIP)",
          "href": "research/fertility/fertility-research-full.zip"
        }
      ],
      "models": []
    },
    {
      "id": "ruled-out",
      "kicker": "Failed hypotheses, kept open",
      "title": "What was ruled out along the way",
      "question": "Which candidate explanations failed their tests?",
      "evidence": [
        {
          "claim": "data",
          "text": "Ruled out: a 15–20 year lag from education to fertility (the effect is immediate); an age-29 trap below 1.3 (Japan is a counterexample); national enrolment ratios as evidence for the marriage jam (failed the placebo test); competition within marriage as the main driver in Korea; educated Chinese women wanting fewer children (surveys show about 1.7, the same as others); diet and stress as a major factor."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "Failed hypotheses are kept in the record. Ruling something out is a result, not a gap."
        }
      ],
      "result": [
        {
          "claim": "open",
          "text": "The post-2015 cause remains open. Timing alone does not separate smartphones, COVID, economic shocks or microplastics."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "Ruling out is only as strong as the test. Several of these tests rest on small samples or simulations."
        }
      ],
      "sources": [
        {
          "label": "Fertility collapse lab",
          "href": "research/fertility.html"
        },
        {
          "label": "Fertility research bundle (ZIP)",
          "href": "research/fertility/fertility-research-full.zip"
        }
      ],
      "models": []
    }
  ],
  "deeper": [],
  "models": {
    "development-survival": {
      "id": "development-survival",
      "title": "Development (survival) model",
      "purpose": "mechanism",
      "state": "developing",
      "note": "Fits period TFR on life expectancy in levels across six places. Strong in levels; fails first differences and cointegration. A shared trend, not a causal floor.",
      "engine": "research/fertility/fertility-research-full.zip",
      "research": "research/fertility.html"
    },
    "matching-dummy": {
      "id": "matching-dummy",
      "title": "Development + matching + post-2015 period dummy",
      "purpose": "mechanism",
      "state": "developing",
      "note": "Adds a marriage-matching term and a post-2015 period dummy to the development model. Improves held-out fit slightly (0.39 vs 0.40). The dummy describes timing, not cause.",
      "engine": "research/fertility/fertility-research-full.zip",
      "research": "research/fertility.html"
    },
    "credential-cohort": {
      "id": "credential-cohort",
      "title": "Credential cohort model",
      "purpose": "mechanism",
      "state": "developing",
      "note": "Synthetic cohort in which mass education raises the cost of each child. Invented parameters; shows what the mechanism can do, not measured effects.",
      "engine": "research/fertility/fertility-research-full.zip",
      "research": "research/fertility.html"
    },
    "mechanism-assortative": {
      "id": "mechanism-assortative",
      "title": "Assortative matching mechanism lab",
      "purpose": "mechanism",
      "state": "developing",
      "note": "Synthetic cohort of 3,000 women and men searching for partners from 18 to 45. Reproduces Korean marriage facts under a credential floor plus women marrying up. Invented parameters.",
      "engine": "research/fertility/fertility-research-full.zip",
      "research": "research/fertility.html"
    },
    "fecundity-age": {
      "id": "fecundity-age",
      "title": "Fecundity-age model",
      "purpose": "mechanism",
      "state": "developing",
      "note": "Age-specific fecundity curve calibrated to medical data, used to translate marriage delay into lost births. A calibration input, not causal validation of aggregate fertility.",
      "engine": "research/fertility/fertility-research-full.zip",
      "research": "research/fertility.html"
    },
    "ivf-policy": {
      "id": "ivf-policy",
      "title": "IVF and policy suite",
      "purpose": "mechanism",
      "state": "developing",
      "note": "Simulated conditional effects of IVF and policy levers on completed fertility in a Korea-like synthetic cohort. Not policy forecasts.",
      "engine": "research/fertility/fertility-research-full.zip",
      "research": "research/fertility.html"
    },
    "shock-suite": {
      "id": "shock-suite",
      "title": "Post-2015 shock suite",
      "purpose": "mechanism",
      "state": "developing",
      "note": "Tests a post-2015 period dummy against country spread and pre-2015 trends. Fits the timing; cannot separate smartphones, COVID, economic shocks or microplastics.",
      "engine": "research/fertility/fertility-research-full.zip",
      "research": "research/fertility.html"
    },
    "microplastics-test": {
      "id": "microplastics-test",
      "title": "Microplastics test",
      "purpose": "mechanism",
      "state": "developing",
      "note": "Tests whether microplastics fit the post-2015 pattern. The pattern is wrong for microplastics as the main cause, but timing alone does not rule it out definitively.",
      "engine": "research/fertility/fertility-research-full.zip",
      "research": "research/fertility.html"
    },
    "momentum-test": {
      "id": "momentum-test",
      "title": "Tipping / momentum lab",
      "purpose": "teaching",
      "state": "developing",
      "note": "Illustration with invented parameters: peer-driven thresholds can tip fertility into a lasting low. Not an estimate; observed data do not confirm a clean cliff.",
      "engine": "research/fertility/fertility-research-full.zip",
      "research": "research/fertility.html"
    }
  },
  "bottomLine": "Observed period fertility fell across all six places, and a post-2015 drop is visible in the fitted residuals. The levels relation between survival and fertility is real across places but fails the trend check, so it is not a causal floor. Credential races, the marriage jam, late-marriage fecundity and policy effects are simulations with invented parameters, not estimates or forecasts. The post-2015 cause remains open: timing alone does not separate smartphones, COVID, economic shocks or microplastics. Read every number by its label."
}
