# Angkor Atlas: A Generative Research Sandbox for Agro-Urbanism, Labor Mobilization, Monumental Building, and Mandala Competition

**Research edition 1.1 | 6 November 2026 | Working paper, not peer reviewed**

## Abstract

This paper describes a reproducible, offline JavaScript simulation of Greater Angkor from an illustrative start in 850 CE to 1450 CE. It asks whether dispersed rice production, temple and estate labor obligations, transport and maintenance costs, ritual mobility, military competition, and royal investment in monuments can jointly produce large agro-urban populations and a politically vulnerable ceremonial center. The model consists of 140 heterogeneous spatial cells, an aggregate population and rice economy, an institutional labor budget, a royal court, a stylized rival-power process, and separate legitimacy and shrine-survival states. The program offers nine scenario presets, paired-seed Monte Carlo comparisons, randomized parameter sweeps, and ordinary least-squares regressions. These are **mechanism experiments**, not estimates of what happened at Angkor. In one reproducible run (seed 42), the reference preset ends in 1450 with 782,035 inhabitants over a 3,000 km² modeled region, 17 simulated conflicts, three sacks, and a rice deficit of 22,276 tonnes. That last deficit is a material model limitation, not evidence for a historical famine. The simulation presently has no explicit food stocks, imports by source, household agents, named independent states, or calibrated construction engineering. It is most useful as an executable argument whose assumptions can be challenged and replaced.

## 1. Research problem

The surviving stone architecture of Angkor can make its political center look like an isolated collection of temples. Archaeological mapping instead reveals a large, low-density, inhabited and cultivated landscape: mounds, ponds, fields, channels, embankments, roads, temples, and ceremonial precincts. The model asks how agricultural production and dispersed residence could support concentrations of ritual, political, and construction activity, and how the political center could contract while settlements and religious institutions persisted.

The guiding hypothesis is that **productive infrastructure becomes capturable capital**. Rice fields, ponds, canals, transport nodes, and dependent communities may attract coercive appropriation because an incoming ruler can acquire already-developed productive capacity. Yet those assets remain dependent on people, ecological knowledge, coordination, and maintenance. Capture may preserve output, redirect it, or damage it. This hypothesis emerged from the research discussion; it is not an established archaeological conclusion.

## 2. Evidence and comparison cases

**Greater Angkor.** Population reconstructions on the order of 700,000–900,000 for a broadly defined Greater Angkor region, approximately 3,000 km², provide a rough external scale benchmark. This estimate does not mean that all inhabitants lived inside Angkor Wat or Angkor Thom. A separate estimate for the concentrated civic-ceremonial core is roughly 160,000, with uncertainty in boundaries and chronology. Agricultural mapping suggests over 1,000 km² of rice-field landscape; the area was not necessarily planted or harvested uniformly each year. The reference yield of 1.5 t/ha is a literature-derived illustrative anchor, while 2.5 t/ha is a later historical comparator, not a measured medieval mean.

**Labor and institutions.** Inscriptions and temple accounts indicate large institutional service populations, while Zhou Daguan's late-thirteenth-century account describes markets, domestic life, and forms of unfreedom. Alternating service groups associated with lunar fortnights have been identified in inscriptional research. The fraction of field workers who were enslaved, the scale of seasonal migration, and specific sleeping arrangements for temporary workers remain unknown. The model therefore separates *bonded labor* and *corvée obligations* as parameters and does not infer either directly from monumental size.

**Political security.** Angkor Wat's moat and sacred enclosure have cosmological and hydraulic significance, while Angkor Thom's later walls and moat are a much clearer defensive investment. The 1177 Cham attack and Jayavarman VII's subsequent building program motivate a historical stress-test preset. The reference scenario deliberately does not force a 1177 sack. The wider mandala model permits shifting allegiances, tribute, raiding, and competing centers, but the current code has only a stylized rival-power process.

**Comparative mechanism library.** Anuradhapura and Tikal help frame low-density tropical cities; Bali's subak literature suggests decentralized irrigation coordination; Roman slavery and European manorial corvée supply contrasting labor institutions; Mesopotamian temple estates illuminate religiously organized extraction; Bagan and Ava/Pegu provide comparative Southeast Asian political and religious systems; Philippine haciendas offer a later, geographically distinct comparison for institutional land consolidation; Cahokia and Göbekli Tepe warn against equating monumental sites with permanent residential populations. These cases inspire alternative mechanisms. The app does not claim they were institutionally identical to Angkor.

## 3. Model construction and architecture

The program runs locally in a browser, with `model.js` containing all simulation mathematics, `app.js` controlling the user interface and plots, and `index.html` providing the bilingual interface. The model is seeded for repeatability. It is a **spatial cohort model inspired by agent-based modeling**, rather than a household-by-household ABM.

The region is represented by a 14 × 10 grid. Cells differ in arability, access, fertility, infrastructure condition, local coordination, population, fields, and loyalty. The grid is schematic and has no GIS correspondence to actual Khmer canals or settlements. The baseline sets 3,000 km² of regional area, 1,100 km² of rice fields, 250,000 inhabitants in 850, 1.6 t/ha nominal annual paddy yield, 16% losses, 200 kg paddy-equivalent annual rice consumption per person, and 6,000 tonnes of nominal imports before the model's trade adjustment. The default `coreShare` is 0.16, an experimental share rather than a direct archaeological reconstruction.

Each annual step generates a regional climate anomaly and cell-specific weather deviations. Paddy production depends on field area, nominal yield, fertility, weather, hydraulic condition, local coordination, and an estate/corvée stress term. Net usable paddy plus simplified imports is compared against population demand. Maintenance uses a portion of available labor; infrastructure then improves or degrades. The court appropriates a fraction of positive surplus and allocates it among campaigning, monumental work, and a residual maintenance budget. Monumental labor is capped by both available labor and the paddy-denominated building budget, then multiplied by a skilled-work factor and legitimacy factor. The resulting accumulated ornamental worker-days are transformed to a logarithmic index.

A stylized rival court's power changes with time and stochastic shocks. War probability depends on the relative power of court and rival, raiding intensity, and diplomacy. Battles can generate captives, casualties, loyalty losses, legitimacy changes, and sacks. These are **specified equations**, not historically estimated combat probabilities. Demography responds to food adequacy, a baseline growth parameter, emigration, and wartime casualties. The shrine and court legitimacy are separate stocks, allowing the model to represent religious persistence after political weakening.

Seasonal visitors are calculated from existing adults. They are a *flow/attendance proxy*, not extra inhabitants. The app currently does **not** execute a monthly lunar calendar, monsoon-driven migration trajectories, or explicit grain shipments; those remain design proposals.

## 4. Simulation and statistical methods

A single run produces annual state transitions, sampled timeline outputs, and spatial snapshots. A Monte Carlo comparison runs two configurations with identical starting seeds for each pair; the tool reports distributions of within-seed differences. Identical seeds reduce some simulation noise, although different feedback trajectories consume randomness differently. A parameter sweep samples specified input intervals uniformly and runs independent synthetic histories. OLS then regresses outputs on standardized sampled inputs, reporting coefficients, standard errors, R² and adjusted R².

A coefficient here measures an association **inside the software**, conditional on its assumed equations and sampling range. It does not estimate a historical causal effect. High R² can simply indicate that the model is largely deterministic over the selected input ranges.

## 5. Reproducible exploratory results

All nine presets were run with seed 42 from 850 through 1450. The accompanying `scenario_results_seed42.csv` contains the exact outputs. Selected figures:

| Scenario | 1450 population | People/km² | Wars | Sacks | Monument log index | 1450 rice balance (t) |
|---|---:|---:|---:|---:|---:|---:|
| Reference | 782,035 | 260.7 | 17 | 3 | 2.22 | −22,276 |
| Autonomous villages | 805,564 | 268.5 | 19 | 3 | 2.02 | −23,550 |
| Consolidated estates | 658,916 | 219.6 | 36 | 9 | 2.50 | −26,670 |
| Captive raiding | 714,683 | 238.2 | 44 | 6 | 2.38 | −34,377 |
| Fortified court | 762,631 | 254.2 | 19 | 1 | 2.32 | −20,738 |
| Trade and monasteries | 884,665 | 294.9 | 19 | 1 | 2.25 | −24,979 |
| Climate instability | 676,139 | 225.4 | 17 | 3 | 2.48 | −20,629 |
| Mandala competition | 727,673 | 242.6 | 44 | 6 | 2.18 | −34,772 |
| Historical shocks | 740,378 | 246.8 | 17 | 4 | 2.22 | −23,021 |

These values are model-generated illustrations, **not reconstructed historical outcomes**. The final-year army count is zero in every one of these nine seed-42 runs because the simulated court has no positive allocatable surplus in that year. This reveals a consequential model weakness: it cannot adequately represent armies sustained from accumulated grain stores, taxes in kind collected earlier, fish, credit, foreign tribute, or nonrice provisioning. Likewise, a negative annual rice balance does not directly reduce consumption through a stock-flow inventory system, and the demographic adjustment may allow implausible trajectories. Treat these as targets for model revision.

A paired Monte Carlo experiment (30 seeds, reference versus estate-consolidation preset, ending 1250) yielded a mean treatment-minus-control population difference of approximately **−90,428** (5th–95th percentiles approximately **−108,161 to −67,796**). This indicates how the *current equations* behave under that intervention, not evidence that estates historically reduced Angkor's population. A 50-run randomized parameter sweep ending 1250 produced an R² of approximately **0.996** for the population regression and **0.966** for the monument regression. Such high fits are a reason to audit the simulator's structural rigidity, not a validation claim. The exact regression coefficients and experimental metadata are in `experiment_summary.json`.

## 6. What the model can and cannot answer

It can ask: Under which parameter combinations does the simulated court accumulate monumental labor? How do estate consolidation, decentralized coordination, trade, warfare and climate alter synthetic population trajectories? Does ritual continuity persist after court legitimacy weakens? How robust are results across seeds and parameter changes?

It cannot yet determine the number of slaves at Angkor, actual annual rice imports, the true size of the Khmer field army, the number of masons on Angkor Wat, the proportion of seasonal residents, or the relative historical contribution of raids and voluntary migration. Nor can it establish that a particular mechanism *caused* Angkor's political transformation.

## 7. Priority research and engineering agenda

**First: fix provisioning accounting.** Add paddy and fish inventories, seed grain, storage losses, temple granaries, trade routes, seasonal prices, tribute and crop-specific diets. Make military and construction budgets draw on real stocks and flows. Verify conservation of people, labor-days and grain.

**Second: introduce a real calendar.** Add monsoon months, rice stages, flood recession, lunar-fortnight service rotations, festivals, commuting, dry-season construction, and campaign seasons. Allow temporary presence at the core to diverge from permanent residence.

**Third: implement named polities.** Give Khmer, Cham, and neighboring courts independent agents, territory, tribute networks, diplomacy, defenses, armies and succession. Allow submission and re-allegiance without necessarily destroying villages.

**Fourth: improve archaeological observability.** Simulate stone and timber structures, mounds, inscriptions, preservation and excavation. Compare surviving evidence, not just invisible historical states.

**Fifth: estimate parameters against evidence.** Use dated inscriptions, georeferenced LiDAR/GIS, excavated household data, field-area reconstructions, climate proxies and historically constrained yield distributions. Distinguish observed data, uncertain proxies, and free priors in every model card.

## 8. Conclusion

Angkor Atlas is a small executable framework for comparing alternative explanations of an agro-urban civilization. Its central contribution is a common accounting and spatial language for food, labor, monuments, population, infrastructure, and political rivalry. The next research step is to make those accounts materially consistent and geographically constrained before interpreting any simulated history as an explanation of Angkor.

**See `SOURCES_AND_PROVENANCE.md` for the literature map, `BUILD_HISTORY.md` for the collaborative design history, `METHODS_AND_ASSUMPTIONS.md` for precise implementation notes, and the machine-readable results for reproducibility.**
