import type { Journey } from './angkor-journey'

export const deepHistoryJourney: Journey = {
  "kicker": "Deep history",
  "title": "Deep history · Human dispersal",
  "lede": "Between roughly 85,000 and 65,000 years ago, modern humans spread from the Horn of Africa toward Sahul (Australia and New Guinea). A time-dependent least-cost dispersal model asks which way of making a living — following the coast, following big game, or mixing both — best fits the evidence we have.",
  "why": [
    {
      "claim": "method",
      "text": "The route out of Africa is hard to study because the Ice Age coastline people may have followed now lies under water. A model lets us compare rival ideas about how people moved, using the same climate and the same map, and see which ideas survive contact with the sites we can actually date."
    },
    {
      "claim": "open",
      "text": "This is a question about hypotheses, not a settled story. The model describes the logic of different strategies; it does not give a date for any event, and it is not a simulation of individual people."
    }
  ],
  "chapters": [
    {
      "id": "the-question",
      "kicker": "Why ask",
      "title": "Coast or herds?",
      "question": "Did the first people to reach Sahul follow the shoreline, chase big game inland, or do both?",
      "evidence": [
        {
          "claim": "data",
          "text": "Archaeological sources place people in interior Arabia during wet phases (for example the Nefud lakes) and on islands such as Sulawesi and Sumatra by particular dates. These are observations from published fieldwork, not model output."
        },
        {
          "claim": "data",
          "text": "During the exit window, ice sheets held enough water that sea level sat well below today, exposing shelves that are now seabed. The coastline people might have followed is now offshore, which makes the coastal idea hard to test from dry-land sites alone."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "The model is a time-dependent least-cost dispersal model on a grid from Libya to New Guinea. Every 1,000 years sea level redraws the coast and a humidity index switches the Saharo-Arabian belt between green savanna and desert. Each strategy turns that landscape into a speed surface for a spreading frontier."
        }
      ],
      "result": [
        {
          "claim": "sim",
          "text": "In paired runs — same climate, same sea level, same walking speed — the coastal strategy reaches Sahul before the big-game strategy in about three-quarters of runs. That figure is conditional on the model’s assumptions and priors, not a measured fact."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "The margin depends heavily on one assumption: how productive the shore was compared with good savanna. The current dry-land record cannot settle that, so the comparison is a test of logic, not a verdict on the past."
        }
      ],
      "maths": {
        "plain": "Each run draws every uncertain input at random from a wide range, and all strategies run on the same draw so comparisons are paired.",
        "example": "If the shore is assumed rich, coastal wins almost every time; if it is assumed poor, the advantage shrinks. The result moves with the assumption."
      },
      "sources": [
        {
          "label": "Full write-up and sources",
          "href": "research/out-of-africa.html"
        }
      ],
      "models": [
        "out-of-africa"
      ]
    },
    {
      "id": "how-it-works",
      "kicker": "Method",
      "title": "How the model works",
      "question": "What does the model actually compute, and what does it leave out?",
      "evidence": [
        {
          "claim": "method",
          "text": "The map is a grid of roughly 79,000 cells. Sea level and a single humidity index drive the landscape. A frontier cannot wait in a cell that turns uninhabitable, so a population caught inland when the rains fail dies out. Sea gaps cost an expected waiting time that grows steeply with width."
        },
        {
          "claim": "method",
          "text": "Three rival strategies share the same climate, map and priors: coastal (shore-adjacent quality), megafauna (grassland and game, with river refuges and a re-tooling delay on entering a new biome), and mixed (takes whichever is better in each cell)."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "These are rival structures tested on the same landscape, not three independently validated models. The comparison is fair because the inputs are shared; the outputs are simulations, not observations."
        }
      ],
      "result": [
        {
          "claim": "sim",
          "text": "The Nefud interior constraint and a zero switching cost both favour the mixed strategy: a coast-only population rarely reaches interior Arabia, while a mixed forager can use the coast as a highway and step inland when rains open the interior."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "Biomes are hand-drawn boxes, humidity is a single index for the whole desert belt, and the grid overstates strait widths. There is no population size, no competition with other hominins, and no multiple waves. Results describe the logic of strategies, not a date for any event."
        }
      ],
      "sources": [
        {
          "label": "Full write-up and sources",
          "href": "research/out-of-africa.html"
        }
      ],
      "models": []
    },
    {
      "id": "what-the-evidence-says",
      "kicker": "Results",
      "title": "What the evidence can and cannot decide",
      "question": "When we keep only runs that match the dated sites, what do the survivors have in common?",
      "evidence": [
        {
          "claim": "data",
          "text": "The scoring uses published dates: Sulawesi by about 67.8 ka, Sumatra by about 63 ka, and interior Arabia occupied during a wet phase. These are archaeological observations the model is checked against."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "Runs whose outcome matches all three long-chronology facts are kept, and the survivors are inspected. This is rejection-style approximate Bayesian inference, a way of asking what the evidence implies about the inputs."
        }
      ],
      "result": [
        {
          "claim": "sim",
          "text": "The surviving runs need fast movement, centring on roughly 3 km per year, and an early exit during Green Arabia. They say little about coastal productivity: that parameter’s distribution barely changes, so the dry-land record cannot break the coast-versus-herds tie."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "No definitive route is identified. The decisive sites would be drowned shelves, mostly in shallow water, which the current grid only partly resolves. The short chronology is hard for every strategy."
        }
      ],
      "sources": [
        {
          "label": "Full write-up and sources",
          "href": "research/out-of-africa.html"
        }
      ],
      "models": []
    },
    {
      "id": "what-next",
      "kicker": "Open questions",
      "title": "What would move the needle",
      "question": "What evidence would actually settle the coast-versus-herds question?",
      "evidence": [
        {
          "claim": "open",
          "text": "Dated sites on the drowned shelves the model flags — the Gujarat–Indus, Bay of Bengal–Myanmar and Sunda shelves — plus shell middens older than 60 ka between Yemen and India, would test the coastal idea directly."
        }
      ],
      "rule": [
        {
          "claim": "method",
          "text": "Better estimates of how fast coastal foragers actually expand would also sharpen the comparison, since front speed is one of the inputs the surviving runs constrain."
        }
      ],
      "result": [
        {
          "claim": "open",
          "text": "A separate release-and-capture hypothesis is being developed for this family. This page currently presents the dispersal model."
        }
      ],
      "limitation": [
        {
          "claim": "open",
          "text": "Until those sites are found and dated, the model supports a softened coastal view — the coast as a highway, not the whole road — and leaves the decisive assumption unresolved."
        }
      ],
      "sources": [
        {
          "label": "Full write-up and sources",
          "href": "research/out-of-africa.html"
        }
      ],
      "models": []
    }
  ],
  "deeper": [],
  "models": {
    "out-of-africa": {
      "id": "out-of-africa",
      "title": "Coast or herds? The route out of Africa",
      "purpose": "mechanism",
      "state": "developing",
      "note": "Time-dependent least-cost dispersal model comparing coastal, megafauna and mixed strategies on a shared climate and map. 800 paired Monte Carlo runs. Simulation output, not observed data; results are conditional on priors and assumptions.",
      "engine": "research/out-of-africa/coast-or-herds-model.zip",
      "research": "research/out-of-africa.html"
    }
  },
  "bottomLine": "Under the tested constraints and a zero switching cost, mixed strategies rank best — but this is not evidence that actual humans definitely followed the coast. The Nefud interior constraint and switching-cost sensitivities are decisive, and the decisive sites are on the seabed. This is a model of strategy logic, not a dated history.",
  "repo": "https://github.com/TreyModels/atlas-of-education",
  "family": "deephistory"
}
