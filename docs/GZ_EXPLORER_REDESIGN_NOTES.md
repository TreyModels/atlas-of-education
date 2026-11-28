# Guangzhou Explorer — redesign notes (28 Nov 2026)

Audience: **absolute beginners and expert readers (e.g. Mark Bray)**. Must work on **mobile first** (iPhone 15 Pro Max = minimum; new iPhone 17 Pro-class orange phone too) and desktop. Sky is the limit on tech (Canvas/WebGL, React, JS).

## Audit findings (page at `public/guangzhou-explorer/`)
- Hero opens with "65.8% vs 81.8%" and ratios 0.91 / 1.17 / 1.37 and never says what they are. Too many unstated assumptions.
- ~230 words total, one chart, no hero visual. Nothing hits you on arrival.
- Undefined terms: entrance score, joint score & ability, setting, top 10% ability, academic track, seeds.
- **The double reduction (双减) policy is not explained at all.** Needs a plain-language section: what it is, what it banned/limited, why it matters to the model, what the enforcement-sensitivity runs test. Beginner paragraph + expert box (policy details, sources, model parameters).
- Screenshot via file:// showed empty findings grid and chart. Probably data fetch blocked on file://, **verify on the live site** (could be a real first-screen bug).
- Stage 1 done: author name changed to "Dr. Trey Menefee" (committed to this branch, not yet on `main`/live).

## Plan
1. **Check `data.json` first**: per-pupil outcomes or aggregates only? If aggregates only, the sorter replays a sample drawn to match saved rates and must say so ("replay of saved run #…"). Never invent outcomes.
2. **Plain-language "What is this?"** block under the title (question, simulated pupils, what the model does, what numbers mean), 3-4 short paragraphs. Expert "details" toggle beside it.
3. **Hero = sorting machine.** ~4,000 dots (one per pupil) fall through the real stages (tutoring, school type, entrance score) into baskets (selective university / other university / vocational / out). Colour by family income (warm = richer 40%, cool = poorer 40%, grey = middle). Live share counters per basket. Caption: "each dot stands for one of ~41 million simulated pupils" (40,000 pupils x 1,024 settings, plus tutoring runs).
4. **Three-sorts toggle.** Re-sort the same pupils by entrance score / score + ability / starting ability; dots animate and the rich-poor gap widens 0.91 -> 1.17 -> 1.37. This explains why the ratios differ.
5. **Double-reduction scenario toggle** on the sorter: policy off vs on, and enforcement level. Show what changes.
6. Later: ability-vs-outcome swarm with "turn tutoring on" slider; Sankey pathway ribbons (income -> track -> destination); 1,024-setting heatmap that loads a run into the sorter; scrollytelling captions; mini animated bar pairs on finding cards; glossary tooltips; "what this model can't tell you" note.
7. Reuse school-pathway diagrams already in `research/` (paper).

## Constraints
- Mobile layout first: single column, thumb-sized controls, no hover-only info, canvas sized to viewport, ~60 fps on a phone (cap dot count adaptively), pause/replay button, honour `prefers-reduced-motion` (static end state).
- Bilingual: every new string goes in `i18n.js` (EN + zh-Hans). Chinese reader gets same explanations.
- Keep "precomputed saved runs only" honesty label visible.
- Accessibility: text alternatives for the animation (live-region summary of basket shares).
- Deploy only runs from `main` (`.github/workflows/pages.yml`); this branch is `claude/busy-mayer-mdo5c4`.

## Atlas Bridge
No access to Bridge from the coding session. Paste this file's "Plan" section into the Bridge log.

## Data-type analysis and precedents (from memory, NOT yet verified: re-check with web research)

**What the data is:** a *parameter-sweep ensemble of an agent-based model*. 1,024 settings x 40,000 synthetic pupils; saved outputs are aggregates (rates, ratios, intervals) per setting, plus 40-setting / 8-seed tutoring runs. Three kinds of question: (a) *composition* (who ends where), (b) *comparison across settings* (sensitivity), (c) *measurement choice* (0.91 / 1.17 / 1.37 are the same pupils judged by different yardsticks).

**Mapping data type -> best form**
- Composition of 40k pupils: unit/dot charts (one mark per person) beat bars; frequency-framed displays are better understood than percentages (Gigerenzer-style natural frequencies). Use dots, not decimals.
- Uncertainty across seeds: quantile dotplots and hypothetical-outcome-plot animations (Kay et al. 2016; Hullman et al. 2015) beat error bars for lay readers; keep a plain interval for experts.
- 1,024-setting sweep: small multiples, heatmap over the two most influential parameters, tornado/one-at-a-time sensitivity bars; parallel coordinates for experts. Always let a click load a setting into the main sorter.
- Pathways: Sankey/alluvial (income -> track -> destination), as in OECD Education at a Glance flows.
- Metric choice (the 3 ratios): one animated re-sort of the same dots; a slope/"dumbbell" chart per yardstick.

**Precedents to study**
- Opportunity Insights / Chetty: Opportunity Atlas and College Mobility Report Cards (rich vs poor access, dot/bar summaries, geographic exploration).
- NYT The Upshot: "Extensive Data Shows Punishing Reach of Racism for Black Boys", "The Rent-or-Buy Calculator", election needle (live uncertainty), "You Draw It".
- Explorable explanations: Nicky Case (Parable of the Polygons, Schelling segregation; sorting dynamics by colour), Bret Victor, Distill/Pudding pieces; Galton board / Plinko demos for "many random rolls".
- Gapminder (Rosling): animated bubbles with time/parameter slider and a narrated tour.
- Scrollytelling: Pudding, Reuters Graphics, Flourish/Scrollama patterns.
- Model-sharing: NetLogo Web, Observable notebooks, OpenABM/CoMSES documentation norms (ODD protocol, already in repo).
- Expert trust: show the ODD, assumptions table (134), DOI, seeds, and "what this cannot show" next to every headline number.

**Design implication:** lead with the dot sorter (frequency framing + colour), step to uncertainty (dotplots), then let experts drop into the heatmap/assumptions. Do a real research pass (haiku agent, WebSearch) tomorrow to confirm each precedent and pull 5-8 concrete design patterns with links.

## Verified by web search (28 Nov 2026)
- Quantile dotplots: least bias for magnitude/probability estimates (1-3 pp more precise than density plots, Kay et al. transit study); other displays can do better for decisions. Animated hypothetical-outcome plots help non-experts judge trends and compare 2-3 variables better than error bars/violins (Kale, Hullman et al.). Use dotplots for "how likely", animation for trends, plain intervals for experts. Sources: vis.mit.edu/classes/6.859/readings/pdfs/Kay-WhenishIsMyBus.pdf; arxiv.org/abs/2007.14516; hullmanlab.northwestern.edu (HOPs trends); Padilla, Kay & Hullman 2020 review.
- Parable of the Polygons (Nicky Case & Vi Hart): playable Schelling model, non-blaming tone, hopeful ending; copy the tone for inequality topics. Source: blog.ncase.me/i-do-and-i-understand/.
- Opportunity Atlas: results keyed to where children grew up; colour scale rescales to visible range; image/data download. Source: census.gov/ces/dataproducts/opportunityatlas.html.
- ABM parameter sweeps: average many replicates per setting; whole-space view (heatmap) to show parameter interactions; link summary to individual runs interactively (MASSIVE, PLOS ONE 2019; JASSS 18(4)/4).
- NOT confirmed: NYT Upshot examples; small multiples for ABM sweeps; Gapminder/Pudding/Sankey/natural-frequency claims (memory only).

## Plan changes
Sorter first; seed variation as quantile dotplot with exact interval one tap away; heatmap averages replicates and a click loads that setting; add data/image download; non-blaming tone in double-reduction text.

## Scripts (modules to build, all in public/guangzhou-explorer/, no build step)
- `dotplot.js`: quantile dotplot of seed variation for the 8-seed tutoring runs.
- `heatmap.js`: 1,024-setting heatmap over two chosen parameters, click selects a setting and emits `gz:select-setting`.
- `download.js`: buttons to download the displayed chart (PNG) and the saved data (CSV/JSON).
