# Angkor Atlas model card v1.0

## Research question

Could interacting regional agricultural production, elite estates, labor obligations, ritual mobility, infrastructure maintenance, monument investment and competition for hegemony generate something resembling Greater Angkor's rise, monumental concentration and later political transformation?

## Units and observational distinctions

- Population: aggregate regional inhabitants, **not** all inside Angkor Wat or the ceremonial core.
- `regionKm2`: total regional denominator for density, by default 3,000 km².
- `riceKm2`: mapped/assumed cultivated rice area. This is not all simultaneously cropped every year in reality.
- `yieldT`: tons of unmilled paddy per hectare per modeled year; 1.5 t/ha is a literature-derived historical anchor, with large uncertainty.
- `surplus`: modeled annual usable rice after losses, plus simplified imports, minus population rice demand.
- `ornamentalIndex`: log10(1+cumulative effective ornamental worker-days / 1,000,000); **not** cubic meters of stone.
- `seasonalVisitors`: temporary participants drawn from existing adults; not additive to population.
- `soldiers`: annual model campaigning force, not a documented Khmer battalion count.

## Historical sequence anchors, not deterministic claims

- 850: an illustrative starting point after Jayavarman II's conventional 802 date.
- 1113: Suryavarman II's reign, associated with Angkor Wat construction.
- 1177: Cham assault in historical narratives; shock magnitude remains uncertain. The optional shock is **zero** in reference preset, nonzero in chronology stress test.
- 1181: Jayavarman VII and a new period of royal construction and defensive walls.
- 1300 onward: option for a rising climate-stress scenario, not a forced decline.
- 1431: conventional political transition date, not a single universal abandonment event.

## Evidence vs parameters

Relatively well grounded: geographic scale of Greater Angkor, dispersed agro-urban settlement, temple/monument size, existence of corvée and bonded temple personnel, construction of Angkor Thom fortifications, increasing elite landholdings, archaeological religious and settlement continuity after the court moved.

Weak/uncertain: exact yearly rice yields, percentage of enslaved field laborers, total seasonal visitors, temple workers' sleeping arrangements, rice import volumes, real estate size distributions, maintenance costs, and mobilization efficiencies.

Pure model hypotheses: formulas for loyalty, military contest likelihood, land production feedbacks, fertility, rivalry, monument prestige gain, temple autonomy and population mobility. A successful simulation does not independently validate these rules.

## Existing model components

- 140 spatial cells spanning schematic uplands and Tonle Sap-adjacent lowlands.
- Cells vary in arability, accessibility, population, rice cultivation, water condition and allegiance.
- Climate anomalies, maintenance and food production affect demographic outcomes.
- Court gains resources through modeled surplus; allocates to soldiers, monuments and maintenance.
- Rival-power process creates endogenous warfare, captives, defects and sometimes sacks.
- Temple survival and political legitimacy have separate state variables.
- Paired-seed treatment differences; randomized parameter-sweep OLS with standardized regressors.

## Five required falsification tests for next version

1. **Food balance:** reproduce a plausible 12th–13th-century population while staying within supported cultivated area, agricultural yields, mixed diets and feasible transport.
2. **Chronology without imposition:** produce growth and contraction without forcing a deterministic 1431 collapse.
3. **Raiding independence:** allow substantial state development without captive acquisition. Compare household corvée, voluntary labor and migrant attraction.
4. **Monument preservation filter:** generate wooden housing and stone monuments then impose differential preservation. Verify whether the surviving record resembles Angkor.
5. **Cross-polity transport:** apply the same model architecture to Bagan, Ava/Pegu, Ayutthaya and the Khmer heartland, changing landscape/institutions rather than tuning one-off decline scripts.

## Suggested empirical literature

- Carter et al. (2021), estimates of Greater Angkor's population and chronology.
- Klassen and Evans (2020), landscape organization and top-down/bottom-up water management.
- Lucero, Fletcher & Coningham (2015), tropical low-density cities including Tikal, Angkor and Anuradhapura.
- Lustig & Lustig, Angkor's inscriptions and alternating service groups.
- Zhou Daguan (1296–1297), descriptions of Angkorian markets and daily life.
- Stephen Lansing & James Kremer (1993), Balinese irrigation coordination.

## Regression warning

Sampled input ranges are intentionally broad experimental intervals. They are not confidence intervals for historical quantities. OLS coefficients and R² express behavior of the simulator under those ranges. Random seeds control pseudo-randomness, but paired comparisons with feedback still require causal care. Never interpret fitted coefficients as evidence of historical real-world effect sizes.
