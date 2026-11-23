# Data availability, rebuild, and every deviation from Boppart et al. (2023)

## What the original provides, and what it does not
The paper's online appendix at `nber.org/data-appendix/w31101` was fetched in this project (with a browser user
agent) and contains **only the appendix PDF, no data**. No replication package was available. Everything below
is therefore a **rebuild**, not the authors' data, and the paper's numbers are compared to ours as published
values, not re-computed from their files.

## What was rebuilt, from where
| object | source | coverage | notes |
|---|---|---|---|
| agricultural quantities: capital, labour, intermediates, land, output | USDA ERS agricultural input-output accounts, migrated into the project panel (`/root/work/local_data`, `data/`) | 182 countries, 1961-2023 | the primary quantity source |
| relative input prices | Penn World Table: price level of investment, labour share, GDP per worker | 1960-2019 | the paper uses country-specific non-agricultural prices |
| agricultural employment share, GDP per capita, urbanisation, fertility, population | World Bank WDI, pulled from the API for this job | 207,622 rows, 207 countries | download script committed |
| demography for the joint model | transition record long-run panel (`/root/work/transition/out/long_run_panel.csv`) | 1800-2024, 197 countries | child mortality, life expectancy, schooling, urban share |

## Deviations from the original, one by one
1. **Land quality is not adjusted** (the paper uses GAEZ agro-ecological zones). Consequence: **the land
   elasticity cannot be estimated here**, and any land-augmenting heterogeneity is absorbed into TFP. This is
   the single largest deviation.
2. **No country-specific intermediate input prices.** The paper uses BACI bilateral trade prices; the rebuild
   uses the non-agricultural price level as a proxy. This biases relative input prices toward a common
   component and is the most likely reason our substitution elasticities come out **below** the paper's rather
   than at them.
3. **No LSMS land or intermediate cost shares.** Cost shares used in the decomposition are assumed and
   documented rather than measured from household surveys.
4. **Benchmark years 2005 and 2015**, not a single 2005 cross-section as in the paper. Both are reported so a
   reader can see the year sensitivity.
5. **Sample differs**: 127 countries in 2005 and 128 in 2015 for the cross-section, against the paper's own
   sample, which we cannot reproduce without their data. Samples are stated with every estimate.
6. **Labour input** is USDA's agricultural labour index, not the paper's hours-based measure.
7. **The dynamic panel is our construction** (ten-year differences, country and decade fixed effects,
   clustered by country). The paper is primarily cross-sectional; the dynamic test is our addition, not a
   re-estimate of one of their claims.

## Reproducibility
All scripts are in `research/records/2026-11-23-subsistence/scripts/` (`pull_wdi.py`, `boppart_replicate.py`,
`corrected_test.py`, `model.py`) and `research/records/2026-11-23-subsistence-v2/scripts/`
(`pull_us_history.py`, `sequencing.py`, `model_v2.py`). Results are committed as JSON and text alongside each
record. Raw files (the WDI 207,622-row extract, the NBER appendix PDF, the OWID pulls) live on the project
server at `/root/work/subsistence/data/` and `/root/work/subsistence_v2/data/`; the large WDI extract is not
committed for size, and its download script is committed so it can be re-pulled.

## What cannot be tested with rebuildable data
- **Land-augmenting technology and land quality**: needs GAEZ or equivalent, which is obtainable in principle
  but was not pulled here; without it the land margin is untestable.
- **The paper's exact sample and weights**: needs their data.
- **Hours-based labour input and household-level cost shares**: needs LSMS-style surveys for the countries in
  the cross-section, which is a multi-month data-construction project, not a replication.
- **Any causal claim about the sequencing of input adoption and labour release**: our dynamic panel cannot
  order the two events (the reverse association is stronger), and no historical series was obtainable for the
  early industrialisers that would break the tie.
