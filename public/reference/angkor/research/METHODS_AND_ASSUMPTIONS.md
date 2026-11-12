# Technical methods, assumptions, and audit notes

## Runtime and file map

- `index.html`: offline user interface, English/Chinese text, input controls and layout.
- `app.js`: event handling, visualization, plotting and CSV export.
- `model.js`: seeded simulation, presets, Monte Carlo, parameter sweep and OLS.
- `test_model.js`: basic reproducibility and numerical sanity checks.
- `scripts/reproduce_results.js`: generates the scenario CSV and JSON regression results in this research edition.

No network services or external packages are needed to run the browser app. Node.js is only needed to run the tests or reproduce the research tables.

## Exact baseline values from `model.js`

| Parameter | Default | Interpretation |
|---|---:|---|
| `start`, `end` | 850, 1450 | Synthetic annual simulation span |
| `population` | 250,000 | Starting regional population, not peak historical population |
| `regionKm2` | 3,000 | Density denominator, Greater Angkor-scale geography |
| `riceKm2` | 1,100 | Assumed rice-field area, constant in current code |
| `yieldT` | 1.6 | Annual nominal paddy t/ha |
| `lossPct` | 16 | Seed/harvest/storage deduction from output |
| `riceKg` | 200 | Annual unmilled rice equivalent per person |
| `importsT` | 6,000 | Nominal imports before trade multiplier and annual noise |
| `localShare` | 0.62 | Local coordination/autonomy parameter |
| `estateShare` | 0.25 | Elite estate concentration proxy |
| `hydraulicDependency` | 0.45 | Output sensitivity to infrastructure condition |
| `maintenanceIntensity` | 0.38 | Maintenance demand and repair effectiveness |
| `corveeDays` | 24 | Annual duty days per eligible adult, prior to seasonality adjustment |
| `bonded` | 10,000 | Starting bonded workforce, not an archaeological count |
| `raidIntensity` | 0.45 | Raiding/conflict mechanism strength |
| `warExpense` | 0.28 | Fraction of allocatable surplus for armies |
| `buildShare` | 0.34 | Fraction of allocatable surplus for building |
| `ritualMobilityPct` | 8 | Fraction of adult population used for visitor proxy |
| `coreShare` | 0.16 | Core population fraction, modified by legitimacy |
| `sackShock` | 0 | No forced 1177 attack in reference scenario |

All other default values and exact formulas are available in `model.js`; avoid treating these defaults as historical posterior means.

## Calculation path

1. Initialize 140 cells, distributing population and rice area according to randomly perturbed accessibility and arability.
2. Compute each cell's annual gross rice production from cultivated area, yield, fertility, weather, hydraulic condition, local coordination and estate/corvée stress.
3. Sum usable rice after `lossPct`, add simplified imports, subtract `population × riceKg / 1,000` to obtain `grainBalance` in tonnes.
4. Construct available adult labor as 45% of regional population, with bonded labor allocated first and a seasonal work-time reduction applied to both pools.
5. Allocate some labor to infrastructure maintenance; adjust cell infrastructure through repair, depreciation, weather damage and local coordination.
6. Calculate `allocatable` surplus, then army, monument and residual maintenance budgets. Soldier count uses army budget / 0.12 tonne of rice equivalent per soldier-season and a cap of 3.5% of population. Monumental worker-days use a cap of monument budget / 0.45 kg per worker-day.
7. Update political competition, victories/defeats, captive acquisition, casualties, loyalty and legitimacy.
8. Update population using baseline growth, food-ratio feedback, emigration and casualties; update bonded labor and shrine persistence.
9. Report annual output and sampled spatial snapshots.

## Critical caveats identified during the research-edition audit

**Food-stock inconsistency.** The engine computes a yearly `grainBalance` but does not carry inventories from year to year. A negative balance can coexist with population growth, because the demographic equation reacts gradually to the food ratio. This must be corrected before claims about historical carrying capacity.

**Final-year zero armies.** At seed 42, all nine scenarios end in 1450 with `soldiers=0`, because army funding draws only from *positive current-year* modeled surplus. Historical armies could be supplied through reserves, taxation, nonrice foods, tributaries and external trade. The zero is a modeling artifact.

**Budget allocation can exceed one.** `warExpense` and `buildShare` are separate fractions of the allocatable surplus, and some preset combinations can sum to more than 1. The code clamps the residual maintenance budget to zero but does not renormalize the first two. The next version should enforce a single conserved resource budget.

**Labor double counting risk.** `bonded` is included in the population and is removed from the corvée pool, but army recruitment is not explicitly subtracted from the same adult labor stock in the annual engine. Agricultural work is handled as a yield stress adjustment, not a fully balanced household labor calendar.

**No explicit agent households.** Each cell stores aggregate population and fields. There are no births, deaths, marriages, inheritance, household moves or slave-status transitions at the individual level.

**No georeferencing.** The 14×10 grid is schematic; the model does not know the real locations of Angkor Wat, Angkor Thom, Kulen, the Tonle Sap shoreline or historical roads.

**War rivals are synthetic.** `rivalPower` is a stochastic function, not a named Champa, Ayutthaya, Ava or Pegu state with its own territory, economy and decisions.

**Ornament index is not stone volume.** `ornamentalIndex = log10(1 + cumulative effective ornamental worker-days / 1,000,000)`. It is neither a building height nor an archaeological monument count. Large values should not be read as physical dimensions.

**Regressions are simulator diagnostics.** The OLS uses standardized predictors, conventional standard errors and an intercept. Input intervals are arbitrary exploratory ranges. Model nonlinearity, correlated outputs and feedback undermine causal interpretation.

## Proposed validation ladder

A. Conservation tests for grain, labor and population, including inventories and consumption.

B. Unit tests for agricultural seasonality, flood damage, maintenance and migration.

C. Reproduction of historical-scale quantities without imposing observed outcomes directly.

D. Spatial validation against independently mapped fields, ponds, mounds and canals.

E. Alternative institutional rules that fit the same archaeological observations, plus posterior predictive comparison.

F. Cross-case portability tests for Anuradhapura, Bagan, Bali and other landscapes without retuning every equation.
