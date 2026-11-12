# How we built Angkor Atlas: a collaborative design history

**Status:** reconstruction of the design conversation and the code in this package, not an independently archived software-development log. Earlier prototypes discussed in conversation are not included here and their numerical results are not independently verified by this archive.

## The original question

We began with an apparent puzzle: Angkor contains monumental temples and engineered water systems of astonishing scale, but its people lived across a vast agricultural landscape, much of it built in wood and earth. What kind of political economy could concentrate enough food, skill and labor to build the monuments? Why could the royal center diminish while temples and farming settlements endured?

## The sequence of ideas

**1. Dispersed urbanism instead of a compact city.** We distinguished Angkor Wat's approximately 2 km² outer footprint, Angkor Thom's roughly 9 km² enclosure, the civic-ceremonial core, and the approximately 3,000 km² Greater Angkor Region. The model's `regionKm2`, `riceKm2`, `coreShare`, and cell population densities emerged from that distinction. We explicitly rejected the assumption that 700,000–900,000 people lived inside a temple precinct.

**2. Rice as a binding budget.** We discussed 1.5 t/ha as a tentative Angkor-era yield anchor and a 2.5 t/ha later Cambodian comparator. We converted cultivated area into unmilled rice output and subtracted seed/losses and population consumption. This led to the model's yield, field area, rice requirement, imports and surplus variables. The initial interactive slider demonstrated why gross production is not equivalent to free royal surplus.

**3. Slaves, corvée, and estate concentration.** We compared Khmer temple dependents and rotating service obligations with Roman slavery, European manors, Mesopotamian temple estates and later Philippine haciendas. We chose separate `bonded` and `corveeDays` parameters because the legal status and reproduction of unfree labor matter. The present code is a first approximation; it does not yet model individual slave households or hereditary status.

**4. Two outputs from one surplus.** We added monumental construction and military mobilization as competing uses of appropriated resources. Monument output is expressed as cumulative effective ornamental worker-days on a log scale; soldiers are a synthetic annual campaigning force. The earlier on-screen calculator used a 500-person battalion-equivalent display, a comparison convention rather than an attested Khmer unit. The packaged simulation uses a different integrated annual budget and should be treated as the authoritative code for its own results.

**5. Seasonal movement and calendars.** We noted inscriptional evidence of alternating lunar-fortnight temple service, and hypothesized monsoon-dependent agricultural work, travel, festivals, and dry-season building. The browser model currently records a seasonal visitor proxy; the full calendar remains an explicit next step.

**6. Capturable landscape capital.** We proposed a definition of the Neolithic transition in terms of productive assets that rivals can seize: fields, waterworks, transport links, stored food and dependent populations. Angkor's rain-fed drainage system and the Tonle Sap flood-pulse economy prompted a distinction between natural productivity and engineered, maintenance-dependent assets. The present model approximates this with fields, infrastructure condition, maintenance and conquest damage.

**7. Defenses and religious enclosure.** We separated Angkor Wat's sacred enclosure and moat from Angkor Thom's more clearly defensive walls. The historical-event scenario allows a 1177 war shock, but the reference scenario does not impose it. We compared sacred precincts with Egyptian temples and treated fortification as a choice under insecurity.

**8. Mandala competition.** We extended the idea of a king's resource budget to rival courts, shifting allegiance, captive raiding, diplomacy and political sacking. This drew on mainland Southeast Asian mandala scholarship and comparisons with Ava/Pegu and other regional polities. In v1.0, the rival is a stochastic power function rather than a full independent agent.

**9. A shareable demonstration.** The user requested an offline ZIP that could be opened locally or handed to another AI assistant, with bilingual English/Chinese controls, scenario presets, Monte Carlo plots, regressions and population density. The result is the standalone `index.html`/`app.js`/`model.js` application. The present research edition adds documentation, a reproducible results script, CSV output and machine-readable regression diagnostics.

## Who contributed what

The user supplied the central questions and conceptual direction: capturable productive capital, the relationship between dispersed agriculture and monumental centers, labor-status comparisons, seasonal population movement, mandala rivalry, and the desire for a modular Atlas of Education-style modeling environment. The assistant translated those ideas into an initial browser interface, mathematical rules, presets, tests and documentation. Neither the software nor the research paper represents fieldwork, archaeological discovery, or peer-reviewed empirical estimation.

## What we inherited from earlier conceptual work

The larger Atlas of Education ambition is a modular, hypothesis-driven simulation platform with reproducible scenarios, Monte Carlo experiments, sensitivity testing and model cards. This ZIP is a small standalone demonstration of that approach. It does not include or replace the user's larger Atlas codebase, and we have not independently inspected that codebase as part of preparing this archive.

## What is verifiable in this ZIP

The actual engine and its formulas are in `model.js`. The nine presets are declared in `PRESETS`. The scenario outputs can be recreated with `node scripts/reproduce_results.js`; tests run with `node test_model.js`. The discussion history above is a narrative provenance account; only the files and reproduced calculations are independently inspectable here.
