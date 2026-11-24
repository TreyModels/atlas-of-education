# Data used in this record and what is still needed

## In `data/` (copied from the repo, small)
| File | What | Origin |
|---|---|---|
| fertility.json, lsc.json, sec.json, prm_cmp.json, ter.json | TFR; lower-secondary completion; secondary enrolment; primary completion; tertiary enrolment, as [iso3, year, value] | `research/records/2026-11-22-session/data/` (branch `research/massification-session-2026-11-22`); World Bank WDI-derived |
| gdppc_log.json | GDP per capita in **levels** (despite the name; values 123-247,170); take the log | same |
| u5mr.json | under-five mortality | same |
| wage_emp.json, emp_agri.json, agri_va.json | paid employment share; agricultural employment share (both start 1991 for every country); agricultural value added (1960+, median start 1981) | same |
| meta.json | country metadata | same |
| n4_country_shape_parameters.csv | per-country onset, midpoint, floor, school_30/50 etc. | identical to `fix/n4-shape-2026-11-24:research/records/2026-11-25-paper-shape/results/country_shape_parameters.csv` |
| supply_demand_event_ordering.csv | per-country schooling, release, supply, demand event years | `research/supply-demand-2026-11-23:research/records/2026-11-23-supply-demand/results/event_ordering.csv` |

## Needed for the next experiments (not in the repo; network required)
| Experiment | Source | Notes |
|---|---|---|
| E1, E2, E4 | multiverse panel (`GM_DATA`) | confirm it exists, else rebuild with `corr-rebuild/scripts/download_raw.sh` |
| E6 | GGDC 10-Sector Database; Penn World Table; WDI sector shares | pre-1990 demand proxies |
| E8 | WDI SE.PRM.ENRR, SE.SEC.ENRR; fee-abolition primary sources | fee dates conflict across secondary sources |
| E9 | Clio Infra; Lee & Lee (2016); Maddison | pre-1950 |
| E11 | raw files listed in `corr-rebuild/data/RAW_SOURCES.md` | eight schooling indicators |
| E12 | DHS STATcompiler API | public, no login |
| E14, E15 | Human Fertility Database; Our World in Data; Chesnais (1992); UN WPP 2024 | long-run TFR |
| N5 | Barro-Lee, Lee-Lee cohort attainment | birth-cohort schooling |

The workspace used for this session could not download from these sites (outbound traffic is allow-listed), so none of the above was run here.
