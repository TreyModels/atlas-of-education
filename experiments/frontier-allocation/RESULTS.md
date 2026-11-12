# Frontier obligations and five competing labour uses

This experiment implements a finite labour-day budget and two grain accounts. It is an illustrative accounting model, without a historical fit to Angkor. Existing website models are unchanged.

## Five allocations

Each year's nonnegative shares must sum to one: agriculture, military service, irrigation/roads, monuments, religion. The initial population is 20,000; available labour is population × 0.45 × 180 person-days/year. Military recruitment is restricted to the assumed 85% free share of this labour supply. All other categories are treated as fungible labour. Neither the 15% bonded share nor this allocation authority is historically calibrated. There is no occupational skill matrix, seasonal scheduling or captive-taking.

A standing garrison post requires 365 duty-days/year. Campaigns use only military days remaining after garrisons. Capturing a town adds 1,000 residents and 350 hectares of fields next year, plus 150 garrison posts every subsequent year. Home defense requires 200 posts. This makes a conquest both a resource acquisition and a recurring duty. Frontier people transfer into the polity; they are not created as captives. No deaths or demographic growth are modeled; food gaps record unmet rations.

## Allocation policies used from the start

| Policy | Agriculture | Military | Irrigation/roads | Monuments | Religion |
|---|---:|---:|---:|---:|---:|
| balanced | 50% | 20% | 15% | 10% | 5% |
| farm_first | 65% | 15% | 10% | 5% | 5% |
| military_first | 40% | 35% | 10% | 10% | 5% |
| irrigation_first | 50% | 15% | 25% | 5% | 5% |
| monument_first | 40% | 15% | 10% | 30% | 5% |
| religion_first | 45% | 15% | 10% | 5% | 25% |
| military_from_farms | 35% | 35% | 15% | 10% | 5% |
| military_from_monuments | 50% | 30% | 15% | 0% | 5% |
| military_from_irrigation | 50% | 30% | 5% | 10% | 5% |
| irrigation_from_monuments | 50% | 20% | 25% | 0% | 5% |

## Territory and provisioning

The frontier route is 60 + held towns × distanceStep kilometres. Campaign duration is 60 fighting days plus round-trip travel at 20 km/day. A campaign needs at least 350 soldier-equivalents; capture probability is a declared function of available force, capped at 90%. These combat assumptions are not historical estimates. Every seed consumes the same weather and encounter draws across policies.

Mean route distance raises delivery losses on collected grain and military logistics requirements. Roads reduce collection transport losses. Garrison coverage below 75% for two consecutive years causes the furthest town to secede. That is a testable model rule, not evidence for how Khmer towns changed allegiance. A seceding town removes its population, fields and proportional share of the pooled household grain store. No local fortification stock, hostile rival strategy or garrison reinforcement network is represented.

Harvest depends on cultivated area, assigned farm-days, water condition and weather. Initial home land is 4,000 ha, with a 6,000 ha reclamation ceiling. Nominal output is 1.6 grain-equivalent tonnes/ha, reduced by a 16% post-harvest factor. Farm work requires 162 person-days/ha. These are illustrative common-unit assumptions; no conversion from archaeological production proxies to historical tonnes is claimed.

Household and court stores each lose 6% annually. A gross collection rate of 25% or 40% transfers harvest to the court, subject to delivery losses. The court pays all publicly assigned workers' service-day rations plus military logistics. It can fund only the fraction its grain covers; unfunded public labour becomes idle. Soldiers' ordinary rations are charged once. Public rations plus civilian ration demand always equal population × 0.21 grain-equivalent tonnes/year. Households feed the remainder; remaining court grain can relieve shortages. Rations use one common grain-equivalent unit, rather than mixing paddy and milled rice. Physical harvest conversions and diet composition need separate calibration.

Three quarters of funded irrigation-sector work pays for water maintenance and reclamation; one quarter builds roads. Maintenance requires 10, 30 or 60 days/ha/year in the sensitivity grid. Water condition decays with inadequate upkeep. Remaining water-sector work can reclaim home land at 250 days/ha. Monument stock is embodied labour-days, not sandstone tonnes: upkeep requires 1% of the stock's days each year, with deterioration if missed. Quarry access and hauling caps are outside this experiment.

Religious work has a separate routine requirement of 4% of available labour. Coverage sets next year's collection compliance between 85% and 100%. This is a declared narrow coordination benefit. Extra religious allocation beyond that routine threshold has no added modeled benefit. Monuments have no deterrence or prestige return here. Consequently these comparisons cannot establish an optimal historical allocation or classify monumental/religious work as waste.

## Static-policy results at the wider frontier

The table holds the frontier pool at 40 towns and water-maintenance demand at 30 days/ha. Each row averages 256 runs across two climates, two route spacings, two collection rates and 32 matched seeds. Unmet food is cumulative grain-equivalent tonnes over 60 years.

| Policy | Final towns held | Cumulative food gap | Final water condition |
|---|---:|---:|---:|
| balanced | 6.00 | 0.0 | 99.0% |
| farm_first | 4.00 | 0.0 | 89.2% |
| military_first | 17.50 | 1500.3 | 75.0% |
| irrigation_first | 4.00 | 0.0 | 99.0% |
| monument_first | 4.00 | 0.0 | 89.2% |
| religion_first | 4.00 | 0.0 | 89.2% |
| military_from_farms | 17.50 | 9336.1 | 97.6% |
| military_from_monuments | 12.50 | 0.0 | 99.0% |
| military_from_irrigation | 12.50 | 0.0 | 39.9% |
| irrigation_from_monuments | 6.00 | 0.0 | 99.0% |

The policy with 35% of labour assigned to farming and 35% to military service holds more towns but accumulates substantial food gaps. Expanding military work at the expense of irrigation instead leaves a weaker water system. These outputs are consequences of the stated labour requirements and unmodeled benefits must be considered before judging allocations.

## Changing priorities after conquest

All four cases start at 50/20/15/10/5 allocation. At year 30 they either keep that allocation or make the indicated ten-percentage-point transfer. All use the 40-town frontier and 30-day maintenance setting, with the same 256 weather/route/collection combinations.

| Reallocation at year 30 | Peak towns | Final towns | Towns lost | Years below garrison threshold | Food gap | Final water condition |
|---|---:|---:|---:|---:|---:|---:|
| hold_balanced | 6.0 | 6.0 | 0.0 | 0.0 | 0.0 | 99.0% |
| shift_army_to_monuments | 6.0 | 3.0 | 3.0 | 4.0 | 0.0 | 99.0% |
| shift_irrigation_to_army | 12.5 | 12.5 | 0.0 | 0.0 | 0.0 | 42.1% |
| shift_farms_to_army | 12.5 | 12.5 | 0.0 | 0.0 | 0.0 | 96.9% |

The clearest allocation result is that reducing the army after conquest can shed territory while food remains sufficient. In the army-to-monuments case the model loses three of six held towns. That follows directly from standing duty requirements and the stipulated secession threshold. Increasing army allocation by cutting irrigation grows territory but leaves water condition around 42%. Cutting farming by ten points after year 30 does not create a food gap in this particular setup; earlier land development and stores buffer it. A larger farming cut from the outset does create shortfalls. Timing and accumulated capital matter.

## Experimental design and limits

Static grid: 10 allocations × 2 climates × 2 frontier distance increments (20/80 km) × 2 collection rates (25/40%) × 2 finite frontier pools (12/40 towns) × 3 maintenance requirements (10/30/60 days/ha) × 32 seeds = 15,360 histories. Stable climate is compared with synthetic 30% harvest shocks at years 25–30 and 43–46. Four mid-course allocation cases add 1,024 histories. Total: 16,384.

The original twelve-town pool masked military limits in the first exploratory pass. The retained result files include sensitivity to both frontier sizes. Standing garrisons use 365 duty-days, while the annual labour supply is measured at 180 available days per adult. Town-count outcomes can become nearly deterministic as the system reaches its labour-constrained frontier, despite stochastic capture attempts. They should not be reported as estimated historical conquest probabilities.

This is annual aggregate accounting. It does not determine which actual individuals rotate through year-round garrison slots, or whether harvest-season obligations can be met by the same workers. It also excludes independently managed provincial stores, class-specific rights, military losses, population growth, specialist training, climate reconstruction, religious welfare and monumental signalling. Those are separate mechanisms to connect explicitly.

## Checks and reproduction

Run `node run.cjs` in this folder using Node. It rewrites results.csv and summary.json. Checks enforce nonnegative shares summing to one, no labour over-allocation, nonnegative stores within numerical tolerance, conservation of grain and transferred people, ordinary soldier rations counted once, and higher recurring garrison demand when towns are captured. Food residual tolerance is 1e-7 grain-equivalent tonnes. Frontier size and incomplete allocation inputs are checked. The report and CSV can be read on iOS after unzipping; no JavaScript browser app is included.
