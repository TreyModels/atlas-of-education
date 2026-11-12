# Atlas of Models: a catalogue of formal models for development and education

Nov 8, 2026 · @James W. Menefee III

## How to use this catalogue

Each entry is a claim about how a system works, written so it can become a runnable Atlas world. The catalogue favours rival models of the same outcome, scored against the same data.

Every entry records:

- **Claim**: the outcome it explains, in one sentence.
- **Mechanism**: the causal rule, in plain words.
- **Equations or rules**: where to find them (paper section, appendix, code).
- **Code and data**: what is public and under what licence.
- **Fit test**: the observed pattern it must reproduce.
- **Rivals**: other entries that explain the same outcome differently.

| Status | Meaning |
| --- | --- |
| Live | Already a world in the Atlas |
| Port | Public code or data exists; adapt it |
| Build | Equations are published; implement from the paper |
| Narrative | An argument with data but no formal model; the Atlas would formalise it |
| Heavy | Exists, but needs Dynare, MATLAB or large microdata; not for the browser |

## China's boom: rival mechanisms

Three formal models explain the same facts (rising investment, falling labour share, growing foreign surplus) with different causes. Score them on one shared dataset to make the disagreement visible.

| Model | Cause it names | Status | Fit test |
| --- | --- | --- | --- |
| [Song, Storesletten & Zilibotti, *Growing Like China* (AER 2011)](https://econpapers.repec.org/RePEc:aea:aecrev:v:101:y:2011:i:1:p:196-233) | Credit frictions: productive private firms finance themselves; less productive firms survive on better credit access | Port: AER dataset and author code ([Zilibotti](https://campuspress.yale.edu/zilibotti/published-research)) | Sustained return on capital, reallocation toward private firms, foreign surplus since 1992 |
| [Chang, Chen, Waggoner & Zha, *Trends and Cycles in China's Macroeconomy* (2015)](https://www.nber.org/papers/w21244) | Preferential credit for heavy industry | Heavy: two-sector DSGE; simplify to its credit-allocation rule | Weak investment–consumption comovement; rising investment rate; falling labour share |
| [Bai, Hsieh & Song, *The Long Shadow of a Fiscal Expansion* (2016)](https://www.nber.org/papers/w22801) | 2009–10 stimulus financed off balance sheet by local financing vehicles, favouring connected firms | Build: no formal model; formalise as land-collateral borrowing | Permanent rise in investment after 2010; off-balance-sheet spending near 5% of GDP a year after the stimulus |

**Shared scoring data:** investment rate, labour share, current account, private versus state output share, 1992–2024. Chang et al. publish a consistent annual and quarterly macro series that can serve as the common dataset.

**Open question:** the dual-track price reform (Isabella Weber, *How China Escaped Shock Therapy*) is a fourth candidate cause for the 1980s start, but has no formal model yet.

## China: credit and real estate

The credit story is well argued but not formalised in public. The two housing papers disagree on whether property is a crisis trigger or an amplifier.

| Work | Argument | Status |
| --- | --- | --- |
| [Logan Wright, *Broken China* (Polity, 2026)](https://fsi.stanford.edu/node/39615) | The slowdown is rooted in the financial system and the end of an unprecedented credit expansion. Background: [*Credit and Credibility* (CSIS, 2018)](https://www.csis.org/analysis/credit-and-credibility-risks-chinas-economic-resilience) | Narrative |
| [Rogoff & Yang, *Peak China Housing* (2020)](https://www.nber.org/papers/w27697) | Real estate and related sectors reach about 29% of GDP; a housing decline trims a cumulative 5–10% of output | Build: input–output multiplier, small and browser-ready |
| [Fang, Gu, Xiong & Zhou, *Demystifying the Chinese Housing Boom* (2015)](https://www.nber.org/papers/w21112) | Prices rose with incomes; down payments above 35% make housing an amplifier, not a trigger | Build: price-to-income and leverage rules for buyer cohorts |
| [Tianlei Huang, *Detox* (PIIE, forthcoming)](https://www.pulse.bot/real-estate/news/understanding-chinas-economy-and-the-housing-bust-with-tianlei-huang-aab32144-79af-4919-be93-176d6e7de292/) | The bust forces a local-government fiscal reckoning | Narrative |

**Proposed Atlas world: a stock-flow consistent credit and property model.** Sectors: households, developers, local financing vehicles, banks, central government. Each loan is someone's asset, so balance sheets must reconcile every period. Levers: land-sale dependence, pre-sale financing, down-payment rules, credit growth target, bank forbearance. Fit tests: household leverage, developer default timing after the 2020 borrowing limits, land revenue share of local budgets.

Tools for the build: the Godley–Lavoie stock-flow framework, with open implementations such as the R package `sfcr` and Steve Keen's Minsky. Rogoff–Yang's input–output footprint can sit on top as the output channel.

## China: the 1999 university expansion and youth unemployment

The empirical studies disagree on the expansion's labour-market effect, and no open formal model of youth unemployment turned up. The Atlas graduate queue may already be the most formal public version.

| Study | Finding | Use in the Atlas |
| --- | --- | --- |
| [Knight, Deng & Li (2017)](https://econpapers.repec.org/RePEc:csa:wpaper:2016-04) | Enrolment grew almost six-fold 1998–2008; lower relative wages, higher unemployment and fewer good jobs, but only for the entering cohort; incumbents protected | Fit test for the graduate queue: does the model shield insiders? |
| [Ou & Zhao (2022)](https://econpapers.repec.org/RePEc:bla:chinae:v:30:y:2022:i:2:p:117-141) | Unemployment fell for men and college graduates in the short run; women's participation and high-skill earnings fell | Rival result; provincial variation and a Bartik demand control |
| [Yu (2014)](https://dalspace.library.dal.ca/handle/10222/50406?show=full) | Unemployment of young graduates up 8.7%; full-time employment down 21% | Rival result, CHNS data |
| [Li, Whalley & Xing (2014)](https://econpapers.repec.org/RePEc:iza:izadps:dp4974) | Expansion raised college-going sharply and unevenly across groups | Access side of the queue |

**Data caution:** the official 16–24 rate excluded students from 2023, so earlier figures are not comparable. Under the old method the rate peaked at 21.3% in June 2023; under the new one it reached 18.9% in August 2026 ([report](https://www.qatar-tribune.com/article/255654/business/chinas-youth-unemployment-hits-record-high-as-ai-deepens-job-crunch)).

**Null model to add:** a plain search-and-matching "lake model" (QuantEcon) with job-finding and separation rates only. The Tilly categories earn their place if they explain what the null model cannot: the July spike, waiting outside the labour force, and insider protection.

## Learning and dropout: the Philippines

The Pritchett learning-profile models are the strongest buildable entry here. Calibrated to low- and middle-income countries, they find that universal Grade 10 completion adds little learning, while slowing the curriculum adds the equivalent of 1.6 years of schooling. That bears directly on K–12, which added two years.

| Work | Mechanism | Status |
| --- | --- | --- |
| [Beatty & Pritchett, *Negative Consequences of Overambitious Curricula* (2012)](https://www.cesifo.org/DocDL/cesifo1_wp4040.pdf) | Learning happens when a child's skill matches the level taught; a curriculum that outpaces learners flattens the learning profile | Build: simple simulation, equations in the paper |
| [Kaffenberger & Pritchett, structured model of learning dynamics (2021)](https://pmc.ncbi.nlm.nih.gov/articles/PMC7994294) | Same "potential pedagogical function", calibrated to observed learning trajectories | Build: open-access paper with parameters |
| [PIDS, Senior High School and the labour market](https://pidswebs.pids.gov.ph/CDN/INFOCUS/pidsupdates79.html) | More boys than girls drop out or fail in basic education | Fit target |
| [Etulle & Carmelotes, K–12 dropout simulation (2014)](https://rmrj.usjr.edu.ph/rmrj/index.php/RMRJ/article/view/99) | Projects 89% of students dropping out across K–12 | Do not build on: the projection is implausible |

**Proposed Atlas world:** a Philippine cohort that combines the Atlas reconstructed cohort (who stays) with the Pritchett function (what they learn each year). Levers: curriculum pace, remediation, the Grade 10 to 11 transition. A cited 2018 figure puts the share of junior high learners not moving on to senior high at 18% ([source](https://portal.amelica.org/ameli/journal/725/7253717004/html/)), which gives the transition a fit target. Output: learning-adjusted years and learning poverty, linking to the existing LAYS tool.

**Open question:** which Philippine assessment series (national tests, PISA 2018 and 2022) best calibrates the learning profile by grade?

## Classic development models to build

These are small, textbook models with known equations; each takes about a day and gives readers a baseline to compare the country worlds against.

| Model | Mechanism | Connects to |
| --- | --- | --- |
| Lewis dual economy | Surplus rural labour moves to a modern sector at a fixed wage until the surplus runs out (the turning point) | China and Cambodia labour supply; rural and Phnom Penh wages |
| Harris–Todaro migration | Rural workers migrate on expected urban wages, so urban unemployment can rise as jobs are created | Cambodia migration and the graduate queue |
| Doepke & Zilibotti, labour standards and child labour ([Zilibotti publications](https://campuspress.yale.edu/zilibotti/published-research)) | Whether international labour standards prolong child labour | Cambodia minimum-age enforcement lever |
| Schelling segregation | Mild preferences about neighbours produce strong sorting | School choice and segregation, a teaching model |
| Poverty traps (threshold models) | Below a capital or nutrition threshold, households cannot invest their way out | Cambodia household choices and debt relief |
| Spence signalling and Dore's diploma disease | Credentials sort workers even when they add no skill, so credential requirements inflate | Credential floor and graduate queue |

**Open question:** which of these should be agent-based (Schelling, Harris–Todaro with heterogeneous migrants) and which closed-form (Lewis, Spence)?

## Data sources and existing libraries

No existing library offers browser-runnable development and education models that put rival mechanisms against the same country data. That gap is the Atlas's niche.

| Resource | What it holds | Use |
| --- | --- | --- |
| [Wittgenstein Centre Human Capital Data Explorer](https://iiasa.ac.at/models-tools-data/wcde) | Population by age, sex and education for 200 countries, seven scenarios to 2100; earlier versions reconstruct attainment back to 1950 | Data spine for China, the Philippines and Cambodia (CSV download) |
| [CoMSES Computational Model Library](https://comses.net/resources/standards) | Over 1,100 agent-based models with ODD documentation, mostly NetLogo | Port candidates; ODD as the Atlas documentation standard |
| [Macroeconomic Model Data Base](https://www.macromodelbase.com/news-item/mmb-release-3-3) | 161 structural macro models on one comparison platform (release 3.3) | Heavy: Dynare; reference for model-comparison design |
| ReplicationWiki | Replication status of published papers, including *Growing Like China* | Check before porting any paper's code |
| QuantEcon lectures | Open Python and Julia code for growth, job search and lake models | Null models and teaching baselines |

**Licensing:** reimplementing a model from published equations is fine with citation. Porting someone's code needs its licence checked first; many replication packages carry none, so ask the authors.

## Build queue

Build the Philippine learning model first: it is small, its equations are published, and it plugs into two existing worlds.

| Rank | Model | Effort | Data needed | Connects to | Status |
| --- | --- | --- | --- | --- | --- |
| 1 | Pritchett learning profile, Philippine cohort | 2–3 days | Philippine assessments by grade; cohort flow rates | Reconstructed cohort, learning-adjusted years | Not started |
| 2 | China boom: three rival mechanisms, simplified | 1–2 weeks | Chang et al. macro series; AER dataset | China graduate queue | Not started |
| 3 | Credit and property, stock-flow consistent, with Rogoff–Yang footprint | 1–2 weeks | Total social financing, land revenue, input–output tables | Graduate absorption, China queue | Not started |
| 4 | Knight cohort-shock test and lake-model null | 2 days | NBS youth series (already in the Atlas) | China graduate queue | Not started |
| 5 | Wittgenstein data spine for three countries | 1 day | WCDE CSV download | Cambodia, sector simulation, teachers | Not started |
| 6 | Doepke–Zilibotti labour standards check | 2 days | Paper equations | Cambodia enforcement lever | Not started |
| 7 | Lewis, Harris–Todaro, Schelling, signalling | 1 day each | None (textbook) | Library baselines | Not started |

Effort assumes the existing Atlas pipeline: world definition, translations, control audit and tests.
