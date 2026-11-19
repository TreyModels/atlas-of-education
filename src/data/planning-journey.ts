import type { Journey } from './angkor-journey'

export const planningJourney: Journey = {
  "kicker": "Education planning",
  "title": "Education planning: the arithmetic, shown",
  "lede": "Twelve small planning tools in the IIEP, UIS and education-sector-analysis tradition. They compute; they do not judge. Each card says what a tool is for and how far it has been checked.",
  "family": "planning",
  "repo": "https://github.com/TreyModels/atlas-of-education",
  "why": [
    {
      "claim": "open",
      "text": "A planning office is asked a simple question: will there be enough places, teachers and money, and will children actually learn? Answering it needs arithmetic that anyone can follow."
    },
    {
      "claim": "method",
      "text": "This page walks through twelve tools grouped by the question they answer. For each we say the question, what evidence it uses, the rule it applies, what it returns, and where it stops being trustworthy."
    },
    {
      "claim": "open",
      "text": "Plain language comes first. Optional formulas and a worked example appear where they help. Nothing here is an official UNESCO product or a forecast of any country."
    }
  ],
  "chapters": [
    {
      "id": "population-enrolment",
      "kicker": "Population and enrolment",
      "title": "Who will be of school age, and who is enrolled?",
      "question": "How many children will need a place, and what share of them are actually in school?",
      "evidence": [
        {
          "claim": "data",
          "text": "Inputs are raw counts: population by age and enrolment by level. These are assumptions about the future, not observations of it."
        },
        {
          "claim": "method",
          "text": "Cohort-component projection carries each age group forward with assumed fertility, mortality and migration."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "The projection ages the population year by year. The flows model tracks promotion, repetition and dropout grade by grade."
        }
      ],
      "result": [
        {
          "claim": "sim",
          "text": "You get projected school-age numbers and a flow of pupils through the grades. These are simulation outputs, not measured data."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "Projections inherit every assumption fed in. Small changes in fertility or migration move the answer a lot."
        }
      ],
      "maths": {
        "plain": "Each year, survivors of an age group move up one year; births add a new youngest group.",
        "formula": "P(t+1, a+1) = P(t, a) × s(a) + migration",
        "symbols": [
          [
            "P(t, a)",
            "population aged a in year t"
          ],
          [
            "s(a)",
            "survival share to the next age"
          ]
        ],
        "example": "Hypothetical: of 100 pupils, 80 progress and 20 repeat. The 80 progress to the next grade; the 20 repeat the same grade. This example omits dropout and new entrants."
      },
      "sources": [
        {
          "label": "School-age population tool",
          "href": "https://github.com/TreyModels/atlas-of-education/blob/main/src/models/worlds.js"
        }
      ],
      "models": [
        "sector",
        "cohort"
      ]
    },
    {
      "id": "indicators-efficiency",
      "kicker": "Indicators and efficiency",
      "title": "Turning counts into indicators",
      "question": "Given raw counts, what do the standard education indicators actually say?",
      "evidence": [
        {
          "claim": "data",
          "text": "Inputs are enrolment, population and teacher counts. The tool does no projecting; it only re-expresses what you give it."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "GER, NER, GIR, adjusted gender parity and teacher ratios are computed from their standard definitions."
        }
      ],
      "result": [
        {
          "claim": "method",
          "text": "You get the indicator values. The arithmetic has been checked; the definitions are the conventional ones."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "A correct ratio from bad counts is still misleading. The tool does not audit the data."
        }
      ],
      "maths": {
        "plain": "Gross enrolment ratio is total enrolment divided by the school-age population.",
        "formula": "GER = E / P",
        "symbols": [
          [
            "E",
            "total enrolment at a level"
          ],
          [
            "P",
            "population of official school age"
          ]
        ]
      },
      "sources": [
        {
          "label": "Indicator calculator",
          "href": "reference/education/index.html#tool=indicators"
        }
      ],
      "models": [
        "indicators"
      ]
    },
    {
      "id": "teachers-deployment",
      "kicker": "Teachers and deployment",
      "title": "Do teachers go where the pupils are?",
      "question": "Are teacher allocations following pupils, or following something else?",
      "evidence": [
        {
          "claim": "data",
          "text": "Inputs are teacher counts and pupil counts by school or district."
        },
        {
          "claim": "method",
          "text": "The education-sector-analysis R² diagnostic compares the two distributions."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "Fit pupils against teachers and read the R²: near one means allocation tracks pupils."
        }
      ],
      "result": [
        {
          "claim": "method",
          "text": "A single diagnostic number describing how closely teachers follow pupils."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "A high R² does not prove fairness; it only says the two move together. It is a diagnostic, not a verdict."
        }
      ],
      "sources": [
        {
          "label": "Teacher supply projection",
          "href": "https://github.com/TreyModels/atlas-of-education/blob/main/src/models/worlds.js"
        },
        {
          "label": "Teacher deployment tool",
          "href": "reference/education/index.html#tool=deployment"
        }
      ],
      "models": [
        "teachers",
        "deployment"
      ]
    },
    {
      "id": "money-equity-grants",
      "kicker": "Money, equity and grants",
      "title": "Who gets the public money?",
      "question": "Does public education spending reach the children it is meant for, and how should grants be split?",
      "evidence": [
        {
          "claim": "data",
          "text": "Inputs are spending by level and household use of each level, plus school characteristics for the grant formula."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "Benefit incidence traces spending across a cohort with a Lorenz curve. The grant formula combines per-pupil, poverty and remoteness weights."
        }
      ],
      "result": [
        {
          "claim": "method",
          "text": "A distribution of benefit across the cohort, and an allocation per child under the weights."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "Weights are choices, not facts. Different weights give different answers, and the tool does not pick for you."
        }
      ],
      "maths": {
        "plain": "A grant per school is the sum of weighted per-pupil amounts.",
        "formula": "G = n × (w_p + w_pov × pov + w_rem × rem)",
        "symbols": [
          [
            "n",
            "pupils at the school"
          ],
          [
            "w_p",
            "base per-pupil weight"
          ],
          [
            "pov, rem",
            "poverty and remoteness shares"
          ]
        ]
      },
      "sources": [
        {
          "label": "Who gets public spending",
          "href": "reference/education/index.html#tool=equity"
        },
        {
          "label": "School grant formula",
          "href": "reference/education/index.html#tool=grants"
        }
      ],
      "models": [
        "equity",
        "grants"
      ]
    },
    {
      "id": "access-places",
      "kicker": "Access and places",
      "title": "Where are the places, and who can reach them?",
      "question": "Are school places located where children can actually get to them?",
      "evidence": [
        {
          "claim": "data",
          "text": "Inputs are school locations and population locations. These are mapped assumptions about geography."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "The school map compares where places exist with where children live."
        }
      ],
      "result": [
        {
          "claim": "sim",
          "text": "A picture of coverage and gaps. It is a description of the inputs, not a measurement on the ground."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "Map data ages quickly and misses informal arrangements. Treat gaps as questions to check, not conclusions."
        }
      ],
      "sources": [
        {
          "label": "Access and places",
          "href": "https://github.com/TreyModels/atlas-of-education/blob/main/src/models/worlds.js"
        }
      ],
      "models": [
        "schoolmap"
      ]
    },
    {
      "id": "learning-targets-absorption",
      "kicker": "Learning, targets and absorption",
      "title": "Is the target realistic, and can the system absorb the growth?",
      "question": "Can a coverage target be reached at a speed countries have managed, and can the economy take the extra graduates?",
      "evidence": [
        {
          "claim": "method",
          "text": "The logistic tool compares the S-curve speed a target requires with speeds historically achieved. The absorption tool compares graduate-job openings with the number of graduates."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "Fit a logistic curve to the target and read off the implied growth rate; compare it with the historical range. The absorption tool balances openings against graduates each year."
        }
      ],
      "result": [
        {
          "claim": "sim",
          "text": "A feasibility check, not a forecast. It says whether the required speed is unusual, not whether it will happen."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "Historical speeds are a rough guide. A country can beat or miss them, and the tool cannot know which."
        }
      ],
      "maths": {
        "plain": "A logistic curve rises slowly, then fast, then levels off. The steepness is the speed the target demands.",
        "formula": "C(t) = K / (1 + e^(−r(t − t0)))",
        "symbols": [
          [
            "K",
            "ceiling coverage"
          ],
          [
            "r",
            "speed of growth"
          ],
          [
            "t0",
            "midpoint year"
          ]
        ]
      },
      "sources": [
        {
          "label": "Is the deadline realistic?",
          "href": "reference/education/index.html#tool=logistic"
        },
        {
          "label": "Learning and targets",
          "href": "https://github.com/TreyModels/atlas-of-education/blob/main/src/models/worlds.js"
        }
      ],
      "models": [
        "logistic",
        "lays",
        "absorption"
      ]
    }
  ],
  "deeper": [
    "population"
  ],
  "models": {
    "sector": {
      "id": "sector",
      "title": "Population and enrolment",
      "purpose": "teaching",
      "state": "developing",
      "note": "Cohort-component projection of school-age numbers feeding a sector simulation of intake, repetition, dropout, teachers and cost. Developing: the demo country is stylised and only primary is simulated.",
      "engine": "https://github.com/TreyModels/atlas-of-education/archive/refs/heads/main.zip",
      "route": "sector",
      "research": "https://github.com/TreyModels/atlas-of-education/blob/main/src/models/worlds.js"
    },
    "cohort": {
      "id": "cohort",
      "title": "Flows and internal efficiency",
      "purpose": "teaching",
      "state": "checked",
      "note": "Promotion, repetition and dropout through the grades. Arithmetic implementation checked; not a policy validity claim.",
      "engine": "https://github.com/TreyModels/atlas-of-education/archive/refs/heads/main.zip",
      "route": "cohort",
      "research": "https://github.com/TreyModels/atlas-of-education/blob/main/src/models/worlds.js"
    },
    "indicators": {
      "id": "indicators",
      "title": "Indicator calculator",
      "purpose": "accounting",
      "state": "checked",
      "note": "GER, NER, GIR, adjusted gender parity and teacher ratios from raw counts. Arithmetic implementation checked; not UNESCO endorsement.",
      "engine": "https://github.com/TreyModels/atlas-of-education/archive/refs/heads/main.zip",
      "research": "reference/education/index.html#tool=indicators"
    },
    "teachers": {
      "id": "teachers",
      "title": "Teachers",
      "purpose": "teaching",
      "state": "developing",
      "note": "Age-structured teacher supply and demand projection with training lag, intake cap and quit rates. Developing: initial age counts and completion are synthetic.",
      "engine": "https://github.com/TreyModels/atlas-of-education/archive/refs/heads/main.zip",
      "route": "teachers",
      "research": "https://github.com/TreyModels/atlas-of-education/blob/main/src/models/worlds.js"
    },
    "deployment": {
      "id": "deployment",
      "title": "Teacher deployment",
      "purpose": "teaching",
      "state": "checked",
      "note": "Education-sector-analysis R² diagnostic of whether teachers follow pupils. Arithmetic implementation checked; a diagnostic, not a fairness verdict.",
      "engine": "https://github.com/TreyModels/atlas-of-education/archive/refs/heads/main.zip",
      "research": "reference/education/index.html#tool=deployment"
    },
    "equity": {
      "id": "equity",
      "title": "Who gets public spending",
      "purpose": "accounting",
      "state": "checked",
      "note": "Lorenz curve and benefit-incidence trace of public spending across a cohort. Arithmetic implementation checked; weights are user choices.",
      "engine": "https://github.com/TreyModels/atlas-of-education/archive/refs/heads/main.zip",
      "research": "reference/education/index.html#tool=equity"
    },
    "grants": {
      "id": "grants",
      "title": "School grant formula",
      "purpose": "accounting",
      "state": "checked",
      "note": "Per-pupil, poverty and remoteness weights combined into an allocation per child. Arithmetic implementation checked; weights are choices, not facts.",
      "engine": "https://github.com/TreyModels/atlas-of-education/archive/refs/heads/main.zip",
      "research": "reference/education/index.html#tool=grants"
    },
    "schoolmap": {
      "id": "schoolmap",
      "title": "Access and places",
      "purpose": "teaching",
      "state": "developing",
      "note": "Compares school locations with population locations. Developing: map data ages quickly and informal arrangements are missed.",
      "engine": "https://github.com/TreyModels/atlas-of-education/archive/refs/heads/main.zip",
      "route": "schoolmap",
      "research": "https://github.com/TreyModels/atlas-of-education/blob/main/src/models/worlds.js"
    },
    "logistic": {
      "id": "logistic",
      "title": "Is the deadline realistic?",
      "purpose": "teaching",
      "state": "checked",
      "note": "Compares the S-curve speed a coverage target requires with speeds historically achieved. A feasibility check, not a forecast.",
      "engine": "https://github.com/TreyModels/atlas-of-education/archive/refs/heads/main.zip",
      "research": "reference/education/index.html#tool=logistic"
    },
    "lays": {
      "id": "lays",
      "title": "Learning and targets",
      "purpose": "teaching",
      "state": "developing",
      "note": "Learning-adjusted years of schooling: expected years × harmonised score ÷ 625. Developing: the 625 benchmark is a convention and harmonised scores carry error.",
      "engine": "https://github.com/TreyModels/atlas-of-education/archive/refs/heads/main.zip",
      "route": "lays",
      "research": "https://github.com/TreyModels/atlas-of-education/blob/main/src/models/worlds.js"
    },
    "absorption": {
      "id": "absorption",
      "title": "Work and external efficiency",
      "purpose": "teaching",
      "state": "developing",
      "note": "Graduate-job queue: openings from replacement and job growth balanced against graduates each year. Developing: wages and firm hiring choices are absent.",
      "engine": "https://github.com/TreyModels/atlas-of-education/archive/refs/heads/main.zip",
      "route": "absorption",
      "research": "https://github.com/TreyModels/atlas-of-education/blob/main/src/models/worlds.js"
    },
    "population": {
      "id": "population",
      "title": "School-age population",
      "purpose": "teaching",
      "state": "developing",
      "note": "Projection uses assumed fertility, mortality and migration, not a verified country forecast.",
      "engine": "https://github.com/TreyModels/atlas-of-education/archive/refs/heads/main.zip",
      "research": "reference/education/index.html#tool=population"
    }
  },
  "bottomLine": "These twelve tools compute; they do not judge. The arithmetic has been checked, but the values are only as good as the counts and assumptions you feed in. Treat every output as a question to review, not a verdict."
}
