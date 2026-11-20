# Economic complexity as a metric — method and caveats

**Added 20 Nov 2026 (user request: "econ complexity should be a metric").**
Source: Growth Lab at Harvard University, *Growth Projections and Complexity Rankings*
(Harvard Dataverse, DOI [10.7910/DVN/XTAQMC](https://doi.org/10.7910/DVN/XTAQMC), CC0 1.0;
file `growth_proj_eci_rankings.csv`, time period 1995–2023/24, retrieved 2026-11-20 from the
Archived raw copy used by `pattern-scout`).

## What the metric is

- **ECI (Economic Complexity Index)** — a measure of the knowledge/capabilities embedded in a
  country's export basket, computed from the diversity of its exports and the ubiquity of those
  products (Hidalgo & Hausmann 2009; reflections method). Higher = more complex.
- **ECI rank** — the country's rank among ranked economies. **Rank is not a level**: do not mix
  the two series.
- **Growth Projection (`growth_proj`)** — the Growth Lab's 10-year growth forecast implied by a
  country's ECI/COI relative to its income level.
- Three product classifications are published: **SITC**, **HS92**, **HS12**. They are not
  interchangeable; the headline series here is `eci_sitc` (longest continuous coverage).

## Files

| File | Content |
|---|---|
| `ECONOMIC_COMPLEXITY.csv` | tidy long: iso3, country, year (1995–2024), `eci_sitc`, `eci_rank_sitc`, `eci_hs92`, `eci_rank_hs92`, `eci_hs12`, `eci_rank_hs12`, `growth_proj`, `in_rankings`, source. 180 rows (6 countries × 30 years). |
| `ECONOMIC_COMPLEXITY_WIDE.csv` | one row per country: first/last year, ECI first/last/min/max, rank first/last, latest growth projection. |
| `raw/eci_growth_proj_rankings.csv` | archived raw Growth Lab file (no edits). |

## Six-country values (headline, `eci_sitc`)

| country | 1995 ECI | latest ECI | 1995 rank | latest rank |
|---|---|---|---|---|
| Japan | 2.063 | 1.542 | 1 | 2 |
| Korea | 1.231 | 1.437 | 14 | 3 |
| Hong Kong | 1.156 | 1.416 | 19 | 6 |
| China | 0.716 | 1.298 | 34 | 8 |
| Philippines | 0.337 | 0.748 | 60 | 40 |
| Cambodia | −1.320 | 0.298 | 124 | 64 |

## Caveats (do not skip)

1. **Level ≠ rank.** `eci_sitc` is a standardized index (can be negative); ranks are ordinal and
   move with the comparison set.
2. **Classification breaks.** SITC/HS92/HS12 give different level and rank series; a series must be
   used consistently, not spliced silently.
3. **Small/open economies.** Hong Kong is an entrepôt with re-exports; Cambodia's early ECI is
   extreme because its export basket was narrow (garments). Levels for these two should be read with
   the trade-re-exports caveat.
4. **Coverage/eligibility.** `in_rankings` marks countries meeting trade-volume/population/data
   requirements; values outside that flag are not comparable ranks.
5. **Endogeneity.** Complexity is correlated with income, schooling, and state capacity. It can
   **condition** relations or proxy a latent capability; it cannot identify a causal education effect
   and it is not a mechanism.
6. **Vintage.** Dataset release 2024-09-17 (latest version 12); values may be revised in later
   releases. Record the retrieval date with any use.

## How to use it in the model

`COMPLEXITY_MAP.md` lists the plug points. The Council's brief 009 already encodes complexity as a
third country-type axis (low/high) and as assumed elasticities (P46–P49, CX-01–CX-04); the data here
makes that axis observable rather than assumed.
