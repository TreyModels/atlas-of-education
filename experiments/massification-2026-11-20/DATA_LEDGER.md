# DATA_LEDGER — Massification and Its Mechanisms (four-country data pull)

Prepared by `data-hunter` for `lead`. Retrieval window: **2026-11-20 12:15–12:23 HKT (04:15–04:23 UTC)**.
Machine-readable series live in `data/*.csv`; raw API/table bytes in `raw/`; hashes and HTTP status in `SOURCES.json`.

Four units: **PHL** Philippines, **KHM** Cambodia, **HKG** Hong Kong SAR (China), **CHN** China.

## What is here

| File | Content | Rows |
|---|---|---|
| `data/wdi_4countries_long.csv` | World Bank WDI API, 48 indicators × 4 countries, 1990–2024, long format with indicator code, name, definition and source note | 4,671 |
| `data/uis_sdg4_4countries_long.csv` | UNESCO UIS SDG4 dataset (release 2026-11), 30 indicators × 4 countries, long format, incl. qualifiers | 2,120 |
| `data/uis_sdg4_data_sources.csv` | UIS per-country-year **data-source metadata** (which survey produced each value) | 2,120 |
| `data/national_headline_figures.csv` | Country-specific headline numbers from primary national sources/reports (Cambodia CLFS 2019, China MOE 2024, HK EDB 2025/26, Kwo & Bray 2011) | 26 |
| `data/edb_*.csv` | HK Education Bureau figures, verbatim table dumps (enrolment by level, attainment, secondary, government expenditure) | 4 files |
| `raw/worldbank/*.json` | Raw WDI API responses + indicator catalogue | 51 files |
| `raw/uis/SDG_202611.zip` | Raw UIS SDG4 bulk archive (37,025,136 bytes, release 2026-11). The 407 MB extraction was deleted after filtering to keep the workspace small; re-extract losslessly with `unzip -o SDG_202611.zip -d extracted` | 1 file |
| `raw/cambodia/` | CLFS 2019 report PDF (via Wayback) + extracted text with page markers | 2 files |
| `raw/hongkong/` | HK EDB xlsx figures, HKEAA stats page, Kwo & Bray (2011) IIAS article PDF + text | 8 files |
| `raw/china/`, `raw/philippines/` | MOE 2024 statistics table, NBS index page; DepEd/PSA Wayback snapshots | 6 files |

**Coverage summary: 48 WDI indicators (43 with all four countries) + 30 UIS SDG4 indicators (7 with all four) + 26 national headline values + 4 HK EDB tables. Seven indicators appear in both WDI and UIS and were cross-checked (spending, pupil-teacher ratios, tertiary GER, out-of-school); the values agree within rounding, which is the main consistency check on the pull.**

## Definitions that must not be conflated

- **Enrolment ≠ attendance ≠ completion.** WDI `SE.PRM.ENRR`/`SE.SEC.ENRR` are gross enrolment ratios (all ages ÷ official-age population, can exceed 100). `*.NENR` are net. UIS `CR.1/2/3` are **completion rates** (share of the population 3–5 years above graduation age that has completed the level), not enrolment. UIS `ROFST.*.CP` are out-of-school rates; `ROFST.H.*` are the household-survey versions. Nothing here is an attendance measure: the UIS SDG4 release does **not** publish adjusted net attendance for these countries (the older UIS "EDU" dataset did; not fetched here — recorded as a gap).
- **WDI `SE.SEC.CMPT.LO.ZS` is not the UIS completion rate.** Its own source note says it is a *gross intake ratio to the last grade*. It reads 97.4 for the Philippines in 2022 while the UIS completion rate `CR.2` is 84.2. Do not mix them.
- **Attainment ≠ current flow.** `SE.SEC.CUAT.PO.ZS` / `SE.TER.CUAT.BA.ZS` are modelled stock shares of the population 25+ (Barro–Lee / Wittgenstein), not labour-force shares and not shares of jobs.
- **Labour-market categories are separate.** "Informal employment" (ILO definition, Cambodia CLFS 88.3%) is not "own-account/contributing family worker", is not "no contract", and is not "no degree". "Degree holder" (CLFS 6.6% of employed) is not "job requiring a degree".

## A. World Bank WDI (API, `api.worldbank.org/v2`, no key required)

Source: World Development Indicators, accessed 2026-11-20. Definitions below are the verbatim `sourceNote`/`sourceOrganization` returned by the WDI indicator catalogue. Full per-country-year values: `data/wdi_4countries_long.csv`.

| # | indicator_code | indicator_name | unit | coverage (iso3 first–last year, n; latest) |
|---|---|---|---|---|
| 1 | `BX.TRF.PWKR.CD.DT` | Personal remittances, received (current US$) | see indicator_name | PHL 1990-2024 (n=35); latest 2024=40279405932.4; KHM 1992-2024 (n=33); latest 2024=2827917512.1; HKG 1998-2024 (n=27); latest 2024=457568834.4; CHN 1990-2024 (n=35); latest 2024=24980610480.0 |
| 2 | `BX.TRF.PWKR.DT.GD.ZS` | Personal remittances, received (% of GDP) | see indicator_name | PHL 1990-2024 (n=35); latest 2024=8.7; KHM 1992-2024 (n=33); latest 2024=6.1; HKG 1998-2024 (n=27); latest 2024=0.1; CHN 1990-2024 (n=35); latest 2024=0.1 |
| 3 | `IT.NET.USER.ZS` | Individuals using the Internet (% of population) | see indicator_name | PHL 1990-2024 (n=32); latest 2024=67.3; KHM 1990-2024 (n=29); latest 2024=68.5; HKG 1990-2024 (n=35); latest 2024=95.8; CHN 1990-2024 (n=33); latest 2024=92.0 |
| 4 | `NY.GDP.PCAP.CD` | GDP per capita (current US$) | see indicator_name | PHL 1990-2024 (n=35); latest 2024=3985.3; KHM 1990-2024 (n=35); latest 2024=2627.9; HKG 1990-2024 (n=35); latest 2024=54274.8; CHN 1990-2024 (n=35); latest 2024=13293.1 |
| 5 | `NY.GDP.PCAP.KD` | GDP per capita (constant 2015 US$) | see indicator_name | PHL 1990-2024 (n=35); latest 2024=3926.1; KHM 1990-2024 (n=35); latest 2024=2183.6; HKG 1990-2024 (n=35); latest 2024=44734.4; CHN 1990-2024 (n=35); latest 2024=13119.1 |
| 6 | `NY.GDP.PCAP.PP.CD` | GDP per capita, PPP (current international $) | see indicator_name | PHL 1990-2024 (n=35); latest 2024=11813.8; KHM 1990-2024 (n=35); latest 2024=7981.5; HKG 1990-2024 (n=35); latest 2024=75341.7; CHN 1990-2024 (n=35); latest 2024=27139.5 |
| 7 | `SE.ADT.1524.LT.ZS` | Literacy rate, youth total (% of people ages 15-24) | see indicator_name | PHL 1990-2022 (n=12); latest 2022=99.8; KHM 1998-2023 (n=13); latest 2023=96.6; HKG none; CHN 1990-2020 (n=4); latest 2020=99.8 |
| 8 | `SE.PRM.CMPT.ZS` | Primary completion rate, total (% of relevant age group) | see indicator_name | PHL 1990-2024 (n=21); latest 2024=91.4; KHM 1997-2024 (n=27); latest 2024=91.0; HKG 2001-2024 (n=23); latest 2024=91.7; CHN 1990-2010 (n=13); latest 2010=103.5 |
| 9 | `SE.PRM.CUAT.ZS` | Educational attainment, at least completed primary, population 25+ years, total (%) (cumulative) | see indicator_name | PHL 2000-2022 (n=10); latest 2022=85.7; KHM 2000-2023 (n=11); latest 2023=49.0; HKG 2006-2024 (n=18); latest 2024=100.0; CHN 2000-2020 (n=2); latest 2020=95.8 |
| 10 | `SE.PRM.DURS` | Primary education, duration (years) | see indicator_name | PHL 1990-2024 (n=35); latest 2024=6.0; KHM 1990-2024 (n=35); latest 2024=6.0; HKG 1990-2024 (n=35); latest 2024=6.0; CHN 1990-2024 (n=35); latest 2024=6.0 |
| 11 | `SE.PRM.ENRL` | Primary education, pupils | see indicator_name | PHL 1990-2024 (n=31); latest 2024=13061453.0; KHM 1990-2024 (n=32); latest 2024=2265817.0; HKG 1990-2024 (n=34); latest 2024=329780.0; CHN 1990-2024 (n=29); latest 2024=108566854.0 |
| 12 | `SE.PRM.ENRL.TC.ZS` | Pupil-teacher ratio, primary | see indicator_name | PHL 1990-2017 (n=24); latest 2017=29.1; KHM 1990-2018 (n=26); latest 2018=41.7; HKG 1991-2018 (n=26); latest 2018=13.3; CHN 1990-2018 (n=23); latest 2018=16.4 |
| 13 | `SE.PRM.ENRR` | School enrollment, primary (% gross) | see indicator_name | PHL 1990-2024 (n=31); latest 2024=94.0; KHM 1990-2024 (n=32); latest 2024=109.0; HKG 2001-2024 (n=23); latest 2024=103.2; CHN 1990-2024 (n=29); latest 2024=99.6 |
| 14 | `SE.PRM.NENR` | School enrollment, primary (% net) | see indicator_name | PHL 1992-2017 (n=19); latest 2017=93.8; KHM 1997-2018 (n=16); latest 2018=90.3; HKG 1995-2018 (n=9); latest 2018=95.5; CHN 1990-1997 (n=8); latest 1997=89.3 |
| 15 | `SE.PRM.PRIV.ZS` | School enrollment, primary, private (% of total primary) | see indicator_name | PHL 1990-2020 (n=27); latest 2020=9.5; KHM 1999-2019 (n=21); latest 2019=5.7; HKG 1990-2024 (n=30); latest 2024=20.6; CHN 1990-2024 (n=24); latest 2024=6.4 |
| 16 | `SE.PRM.TCAQ.ZS` | Trained teachers in primary education (% of total teachers) | see indicator_name | PHL 2010-2024 (n=15); latest 2024=100.0; KHM 2001-2024 (n=24); latest 2024=100.0; HKG 1998-2024 (n=27); latest 2024=93.6; CHN none |
| 17 | `SE.PRM.UNER` | Children out of school, primary | see indicator_name | PHL 1990-2024 (n=27); latest 2024=1616165.0; KHM 1997-2024 (n=22); latest 2024=76741.0; HKG 2001-2024 (n=24); latest 2024=4490.6; CHN 1990-1997 (n=8); latest 1997=8248401.0 |
| 18 | `SE.PRM.UNER.ZS` | Children out of school (% of primary school age) | see indicator_name | PHL 1990-2024 (n=27); latest 2024=11.6; KHM 1997-2024 (n=22); latest 2024=3.7; HKG 2001-2024 (n=24); latest 2024=1.4; CHN 1990-1997 (n=8); latest 1997=6.7 |
| 19 | `SE.SEC.CMPT.LO.ZS` | Lower secondary completion rate, total (% of relevant age group) | see indicator_name | PHL 1990-2024 (n=22); latest 2024=84.8; KHM 1997-2024 (n=25); latest 2024=61.6; HKG 2001-2024 (n=21); latest 2024=129.5; CHN 1990-2012 (n=14); latest 2012=103.6 |
| 20 | `SE.SEC.CUAT.LO.ZS` | Educational attainment, at least completed lower secondary, population 25+, total (%) (cumulative) | see indicator_name | PHL 1990-2022 (n=7); latest 2022=61.9; KHM 2007-2021 (n=7); latest 2021=22.1; HKG 1991-2022 (n=12); latest 2022=80.6; CHN 1990-2020 (n=4); latest 2020=72.4 |
| 21 | `SE.SEC.CUAT.PO.ZS` | Educational attainment, at least completed post-secondary, population 25+, total (%) (cumulative) | see indicator_name | PHL 1990-2022 (n=10); latest 2022=26.1; KHM 2007-2023 (n=10); latest 2023=6.8; HKG 1991-2022 (n=12); latest 2022=32.4; CHN 1990-2020 (n=3); latest 2020=16.1 |
| 22 | `SE.SEC.CUAT.UP.ZS` | Educational attainment, at least completed upper secondary, population 25+, total (%) (cumulative) | see indicator_name | PHL 2000-2022 (n=8); latest 2022=34.5; KHM 1997-2023 (n=12); latest 2023=10.4; HKG 1991-2024 (n=20); latest 2024=66.3; CHN 2000-2020 (n=3); latest 2020=31.8 |
| 23 | `SE.SEC.DURS` | Secondary education, duration (years) | see indicator_name | PHL 1990-2024 (n=35); latest 2024=6.0; KHM 1990-2024 (n=35); latest 2024=6.0; HKG 1990-2024 (n=35); latest 2024=6.0; CHN 1990-2024 (n=35); latest 2024=6.0 |
| 24 | `SE.SEC.ENRL` | Secondary education, pupils | see indicator_name | PHL 1990-2024 (n=30); latest 2024=11865598.0; KHM 1991-2024 (n=19); latest 2024=1171516.0; HKG 1996-2024 (n=25); latest 2024=340877.0; CHN 1990-2024 (n=32); latest 2024=97983183.0 |
| 25 | `SE.SEC.ENRL.VO.ZS` | Share of all students in secondary education enrolled in vocational programmes (%) | see indicator_name | PHL 1990-2018 (n=9); latest 2018=9.7; KHM 1991-2008 (n=11); latest 2008=2.3; HKG 1996-2019 (n=20); latest 2019=1.6; CHN 1990-2019 (n=25); latest 2019=18.1 |
| 26 | `SE.SEC.ENRR` | School enrollment, secondary (% gross) | see indicator_name | PHL 1990-2024 (n=30); latest 2024=85.3; KHM 1991-2024 (n=19); latest 2024=58.8; HKG 2001-2024 (n=23); latest 2024=107.2; CHN 1990-2012 (n=20); latest 2012=92.3 |
| 27 | `SE.SEC.ENRR.UP` | Gross enrolment ratio, upper secondary, both sexes (%) | see indicator_name | PHL 1998-2018 (n=19); latest 2018=66.0; KHM 1998-2008 (n=10); latest 2008=28.7; HKG 2001-2019 (n=19); latest 2019=106.1; CHN 1996-2019 (n=21); latest 2019=79.4 |
| 28 | `SE.SEC.NENR` | School enrollment, secondary (% net) | see indicator_name | PHL 1992-2015 (n=17); latest 2015=65.6; KHM 1998-2008 (n=10); latest 2008=38.3; HKG 1996-2018 (n=19); latest 2018=96.1; CHN none |
| 29 | `SE.SEC.PRIV.ZS` | School enrollment, secondary, private (% of total secondary) | see indicator_name | PHL 1998-2020 (n=17); latest 2020=23.9; KHM 1999-2007 (n=6); latest 2007=2.0; HKG 2002-2024 (n=23); latest 2024=22.1; CHN 2006-2024 (n=19); latest 2024=13.7 |
| 30 | `SE.SEC.UNER.LO.ZS` | Adolescents out of school (% of lower secondary school age) | see indicator_name | PHL 1992-2024 (n=25); latest 2024=13.1; KHM 1998-2024 (n=20); latest 2024=17.6; HKG 2001-2024 (n=24); latest 2024=0.7; CHN none |
| 31 | `SE.TER.CUAT.BA.ZS` | Educational attainment, at least Bachelor's or equivalent, population 25+, total (%) (cumulative) | see indicator_name | PHL 2010-2022 (n=7); latest 2022=18.1; KHM 2017-2023 (n=5); latest 2023=5.8; HKG none; CHN 2000-2020 (n=3); latest 2020=7.7 |
| 32 | `SE.TER.ENRL` | Enrolment in tertiary education, all programmes, both sexes (number) | see indicator_name | PHL 1990-2017 (n=21); latest 2017=3589484.0; KHM 1990-2019 (n=24); latest 2019=222879.0; HKG 1992-2019 (n=20); latest 2019=297934.0; CHN 1990-2019 (n=30); latest 2019=46993614.0 |
| 33 | `SE.TER.ENRR` | School enrollment, tertiary (% gross) | see indicator_name | PHL 1990-2024 (n=30); latest 2024=47.4; KHM 1990-2024 (n=29); latest 2024=21.4; HKG 2003-2024 (n=22); latest 2024=120.1; CHN 1990-2024 (n=35); latest 2024=76.9 |
| 34 | `SE.TER.PRIV.ZS` | Percentage of enrolment in tertiary education in private institutions (%) | see indicator_name | PHL 1999-2017 (n=15); latest 2017=54.3; KHM 2000-2019 (n=11); latest 2019=68.1; HKG 2003-2019 (n=14); latest 2019=17.7; CHN 2013-2019 (n=7); latest 2019=14.4 |
| 35 | `SE.XPD.TOTL.GB.ZS` | Government expenditure on education, total (% of government expenditure) | see indicator_name | PHL 1995-2024 (n=25); latest 2024=16.5; KHM 1998-2024 (n=19); latest 2024=11.2; HKG 1990-2024 (n=27); latest 2024=15.7; CHN 1992-2023 (n=8); latest 2023=11.9 |
| 36 | `SE.XPD.TOTL.GD.ZS` | Government expenditure on education, total (% of GDP) | see indicator_name | PHL 1995-2024 (n=25); latest 2024=3.9; KHM 1998-2023 (n=18); latest 2023=2.2; HKG 1990-2024 (n=27); latest 2024=3.8; CHN 1992-2023 (n=8); latest 2023=3.9 |
| 37 | `SL.AGR.EMPL.ZS` | Employment in agriculture (% of total employment) (modeled ILO estimate) | see indicator_name | PHL 1991-2024 (n=34); latest 2024=21.2; KHM 1991-2024 (n=34); latest 2024=34.2; HKG 1991-2024 (n=34); latest 2024=0.2; CHN 1991-2024 (n=34); latest 2024=22.2 |
| 38 | `SL.EMP.TOTL.SP.ZS` | Employment to population ratio, 15+, total (%) (modeled ILO estimate) | see indicator_name | PHL 1991-2024 (n=34); latest 2024=60.0; KHM 1991-2024 (n=34); latest 2024=82.2; HKG 1991-2024 (n=34); latest 2024=55.1; CHN 1991-2024 (n=34); latest 2024=61.9 |
| 39 | `SL.IND.EMPL.ZS` | Employment in industry (% of total employment) (modeled ILO estimate) | see indicator_name | PHL 1991-2024 (n=34); latest 2024=19.5; KHM 1991-2024 (n=34); latest 2024=28.4; HKG 1991-2024 (n=34); latest 2024=14.1; CHN 1991-2024 (n=34); latest 2024=31.6 |
| 40 | `SL.SRV.EMPL.ZS` | Employment in services (% of total employment) (modeled ILO estimate) | see indicator_name | PHL 1991-2024 (n=34); latest 2024=59.3; KHM 1991-2024 (n=34); latest 2024=37.4; HKG 1991-2024 (n=34); latest 2024=85.7; CHN 1991-2024 (n=34); latest 2024=46.2 |
| 41 | `SL.UEM.1524.ZS` | Unemployment, youth total (% of total labor force ages 15-24) (modeled ILO estimate) | see indicator_name | PHL 1991-2024 (n=34); latest 2024=7.0; KHM 1991-2024 (n=34); latest 2024=0.7; HKG 1991-2024 (n=34); latest 2024=9.5; CHN 1991-2024 (n=34); latest 2024=15.0 |
| 42 | `SL.UEM.NEET.ZS` | Share of youth not in education, employment or training, total (% of youth population) | see indicator_name | PHL 2006-2024 (n=19); latest 2024=16.5; KHM 1996-2023 (n=22); latest 2023=6.3; HKG 2009-2024 (n=16); latest 2024=5.7; CHN 2000-2000 (n=1); latest 2000=12.7 |
| 43 | `SL.UEM.TOTL.ZS` | Unemployment, total (% of total labor force) (modeled ILO estimate) | see indicator_name | PHL 1991-2024 (n=34); latest 2024=2.2; KHM 1991-2024 (n=34); latest 2024=0.3; HKG 1991-2024 (n=34); latest 2024=3.0; CHN 1991-2024 (n=34); latest 2024=4.6 |
| 44 | `SP.DYN.TFRT.IN` | Fertility rate, total (births per woman) | see indicator_name | PHL 1990-2024 (n=35); latest 2024=1.9; KHM 1990-2024 (n=35); latest 2024=2.5; HKG 1990-2024 (n=35); latest 2024=0.8; CHN 1990-2024 (n=35); latest 2024=1.0 |
| 45 | `SP.POP.0014.TO.ZS` | Population ages 0-14 (% of total population) | see indicator_name | PHL 1990-2024 (n=35); latest 2024=27.9; KHM 1990-2024 (n=35); latest 2024=29.8; HKG 1990-2024 (n=35); latest 2024=10.5; CHN 1990-2024 (n=35); latest 2024=16.0 |
| 46 | `SP.POP.1564.TO.ZS` | Population ages 15-64 (% of total population) | see indicator_name | PHL 1990-2024 (n=35); latest 2024=66.6; KHM 1990-2024 (n=35); latest 2024=64.0; HKG 1990-2024 (n=35); latest 2024=66.8; CHN 1990-2024 (n=35); latest 2024=69.3 |
| 47 | `SP.POP.TOTL` | Population, total | see indicator_name | PHL 1990-2024 (n=35); latest 2024=115843670.0; KHM 1990-2024 (n=35); latest 2024=17638801.0; HKG 1990-2024 (n=35); latest 2024=7524100.0; CHN 1990-2024 (n=35); latest 2024=1408975000.0 |
| 48 | `SP.URB.TOTL.IN.ZS` | Urban population (% of total population) | see indicator_name | PHL 1990-2024 (n=35); latest 2024=55.5; KHM 1990-2024 (n=35); latest 2024=40.9; HKG 1990-2024 (n=35); latest 2024=100.0; CHN 1990-2024 (n=35); latest 2024=65.9 |

### WDI definitions (verbatim source notes, abbreviated)

- `BX.TRF.PWKR.CD.DT` — Personal remittances comprise personal transfers and compensation of employees. Personal transfers consist of all current transfers in cash or in kind made or received by resident households to or from nonresident households. Personal transfers thus include all current transfers between resident and nonresident individuals. Compensation of employees refers to the income of border, seasonal, and other short-term worke
- `BX.TRF.PWKR.DT.GD.ZS` — Personal remittances comprise personal transfers and compensation of employees. Personal transfers consist of all current transfers in cash or in kind made or received by resident households to or from nonresident households. Personal transfers thus include all current transfers between resident and nonresident individuals. Compensation of employees refers to the income of border, seasonal, and other short-term worke
- `IT.NET.USER.ZS` — Internet users are individuals who have used the Internet (from any location) in the last 3 months. The Internet can be used via a computer, mobile phone, personal digital assistant, games machine, digital TV etc.
- `NY.GDP.PCAP.CD` — Gross domestic product is the total income earned through the production of goods and services in an economic territory during an accounting period. It can be measured in three different ways: using either the expenditure approach, the income approach, or the production approach. The core indicator has been divided by the general population to achieve a per capita estimate.This indicator is expressed in current price
- `NY.GDP.PCAP.KD` — Gross domestic product is the total income earned through the production of goods and services in an economic territory during an accounting period. It can be measured in three different ways: using either the expenditure approach, the income approach, or the production approach. The core indicator has been divided by the general population to achieve a per capita estimate.This indicator is expressed in constant pric
- `NY.GDP.PCAP.PP.CD` — This indicator provides values for gross domestic product (GDP) per person expressed in current international dollars, converted by purchasing power parities (PPPs). PPPs account for the different price levels across countries and thus PPP-based comparisons of economic output are more appropriate for comparing the output of economies and the average material well-being of their inhabitants than exchange-rate based co
- `SE.ADT.1524.LT.ZS` — Youth literacy rate is the percentage of people ages 15-24 who can both read and write with understanding a short simple statement about their everyday life.
- `SE.PRM.CMPT.ZS` — Primary completion rate, or gross intake ratio to the last grade of primary education, is the number of new entrants (enrollments minus repeaters) in the last grade of primary education, regardless of age, divided by the population at the entrance age for the last grade of primary education. Data limitations preclude adjusting for students who drop out during the final year of primary education.
- `SE.PRM.CUAT.ZS` — The percentage of population ages 25 and over that attained or completed primary education.
- `SE.PRM.DURS` — Primary duration refers to the number of grades (years) in primary school.
- `SE.PRM.ENRL` — Primary education pupils is the total number of pupils enrolled at primary level in public and private schools.
- `SE.PRM.ENRL.TC.ZS` — Primary school pupil-teacher ratio is the average number of pupils per teacher in primary school.
- `SE.PRM.ENRR` — Gross enrollment ratio is the ratio of total enrollment, regardless of age, to the population of the age group that officially corresponds to the level of education shown. Primary education provides children with basic reading, writing, and mathematics skills along with an elementary understanding of such subjects as history, geography, natural science, social science, art, and music.
- `SE.PRM.NENR` — Net enrollment rate is the ratio of children of official school age who are enrolled in school to the population of the corresponding official school age. Primary education provides children with basic reading, writing, and mathematics skills along with an elementary understanding of such subjects as history, geography, natural science, social science, art, and music.
- `SE.PRM.PRIV.ZS` — Private enrollment refers to pupils or students enrolled in institutions that are not operated by a public authority but controlled and managed, whether for profit or not, by a private body such as a nongovernmental organization, religious body, special interest group, foundation or business enterprise.
- `SE.PRM.TCAQ.ZS` — Trained teachers in primary education are the percentage of primary school teachers who have received the minimum organized teacher training (pre-service or in-service) required for teaching in a given country.
- `SE.PRM.UNER` — Children out of school are the number of primary-school-age children not enrolled in primary or secondary school.
- `SE.PRM.UNER.ZS` — Children out of school are the percentage of primary-school-age children who are not enrolled in primary or secondary school. Children in the official primary age group that are in preprimary education should be considered out of school.
- `SE.SEC.CMPT.LO.ZS` — Lower secondary education completion rate is measured as the gross intake ratio to the last grade of lower secondary education (general and pre-vocational). It is calculated as the number of new entrants in the last grade of lower secondary education, regardless of age, divided by the population at the entrance age for the last grade of lower secondary education.
- `SE.SEC.CUAT.LO.ZS` — The percentage of population ages 25 and over that attained or completed lower secondary education.
- `SE.SEC.CUAT.PO.ZS` — The percentage of population ages 25 and over that attained or completed post-secondary non-tertiary education.
- `SE.SEC.CUAT.UP.ZS` — The percentage of population ages 25 and over that attained or completed upper secondary education.
- `SE.SEC.DURS` — Secondary duration refers to the number of grades (years) in secondary school.
- `SE.SEC.ENRL` — Secondary education pupils is the total number of pupils enrolled at secondary level in public and private schools.
- `SE.SEC.ENRR` — Gross enrollment ratio is the ratio of total enrollment, regardless of age, to the population of the age group that officially corresponds to the level of education shown. Secondary education completes the provision of basic education that began at the primary level, and aims at laying the foundations for lifelong learning and human development, by offering more subject- or skill-oriented instruction using more speci
- `SE.SEC.ENRR.UP` — Total enrollment in upper secondary education, regardless of age, expressed as a percentage of the total population of official upper secondary education age.
- `SE.SEC.NENR` — Net enrollment rate is the ratio of children of official school age who are enrolled in school to the population of the corresponding official school age. Secondary education completes the provision of basic education that began at the primary level, and aims at laying the foundations for lifelong learning and human development, by offering more subject- or skill-oriented instruction using more specialized teachers.
- `SE.SEC.PRIV.ZS` — Private enrollment refers to pupils or students enrolled in institutions that are not operated by a public authority but controlled and managed, whether for profit or not, by a private body such as a nongovernmental organization, religious body, special interest group, foundation or business enterprise.
- `SE.SEC.UNER.LO.ZS` — Adolescents out of school are the percentage of lower secondary school age adolescents who are not enrolled in school.
- `SE.TER.CUAT.BA.ZS` — The percentage of population ages 25 and over that attained or completed Bachelor's or equivalent.
- `SE.TER.ENRL` — The total number of students enrolled at public and private tertiary education institutions.
- `SE.TER.ENRR` — Gross enrollment ratio is the ratio of total enrollment, regardless of age, to the population of the age group that officially corresponds to the level of education shown. Tertiary education, whether or not to an advanced research qualification, normally requires, as a minimum condition of admission, the successful completion of education at the secondary level.
- `SE.TER.PRIV.ZS` — Total number of students in tertiary education enrolled in institutions that are not operated by a public authority but controlled and managed, whether for profit or not, by a private body (e.g., non-governmental organisation, religious body, special interest group, foundation or business enterprise), expressed as a percentage of total number of students enrolled in tertiary education.

## B. UNESCO UIS SDG4 dataset, release 2026-11 (`download.uis.unesco.org/bdds/202611/SDG.zip`, no key)

Archive README states: dataset "Sustainable Development Goal 4", release 2026-11, **data extracted 2026-10-22**, licence **CC BY-SA 3.0 IGO**. National file `SDG_DATA_NATIONAL.csv` was filtered to the four countries and 30 indicators: `data/uis_sdg4_4countries_long.csv`. Per-value **data-source metadata** (which survey produced the value — critical for revisions) is `data/uis_sdg4_data_sources.csv`. Values carry `QUALIFIER` (`NAT_EST` national estimate, `UIS_EST` UIS estimate) and `MAGNITUDE` (`NIL`, `NA`, `SUPP`, `LOWREL`, `INCLUDES`, `INCLUDED`).

| # | indicator_code | indicator | coverage (iso3 first–last year, n; last 2 values) |
|---|---|---|---|
| 1 | `CR.1` | Completion rate, primary (%) | PHL 1999–2024 (n=11); 2023=97.5, 2024=98.3; KHM 2000–2023 (n=14); 2021=82.3, 2023=84.6; HKG **none**; CHN 2000–2020 (n=7); 2018=97.8, 2020=99.2 |
| 2 | `CR.1.F` | Completion rate, primary, female (%) | PHL 1999–2024 (n=11); 2023=98.7, 2024=99.1; KHM 2000–2023 (n=15); 2021=87.3, 2023=87.9; HKG **none**; CHN 2000–2018 (n=6); 2016=97.7, 2018=97.4 |
| 3 | `CR.1.M` | Completion rate, primary, male (%) | PHL 1999–2024 (n=11); 2023=96.4, 2024=97.6; KHM 2000–2023 (n=13); 2021=77.6, 2023=81.7; HKG **none**; CHN 2000–2018 (n=6); 2016=95.0, 2018=98.1 |
| 4 | `CR.2` | Completion rate, lower secondary (%) | PHL 1999–2024 (n=11); 2023=88.4, 2024=92.4; KHM 1996–2021 (n=8); 2019=45.9, 2021=56.0; HKG **none**; CHN 2010–2020 (n=6); 2018=90.3, 2020=95.7 |
| 5 | `CR.2.F` | Completion rate, lower secondary, female (%) | PHL 1999–2024 (n=11); 2023=92.6, 2024=94.4; KHM 1996–2021 (n=9); 2019=46.5, 2021=58.3; HKG **none**; CHN 2010–2018 (n=5); 2016=94.2, 2018=94.7 |
| 6 | `CR.2.M` | Completion rate, lower secondary, male (%) | PHL 1999–2024 (n=10); 2023=84.1, 2024=90.5; KHM 1996–2021 (n=8); 2019=45.2, 2021=53.9; HKG **none**; CHN 2000–2018 (n=6); 2016=87.0, 2018=86.3 |
| 7 | `CR.3` | Completion rate, upper secondary (%) | PHL 1999–2024 (n=11); 2023=71.9, 2024=75.0; KHM 1996–2023 (n=18); 2021=26.7, 2023=27.9; HKG **none**; CHN 2010–2020 (n=6); 2018=75.0, 2020=87.5 |
| 8 | `CR.3.F` | Completion rate, upper secondary, female (%) | PHL 1999–2024 (n=11); 2023=76.1, 2024=79.8; KHM 1996–2023 (n=17); 2021=28.1, 2023=31.6; HKG **none**; CHN 2010–2018 (n=5); 2016=65.9, 2018=77.8 |
| 9 | `CR.3.M` | Completion rate, upper secondary, male (%) | PHL 1999–2024 (n=10); 2023=68.3, 2024=70.4; KHM 1996–2023 (n=18); 2021=25.2, 2023=24.0; HKG **none**; CHN 2010–2018 (n=5); 2016=55.9, 2018=72.2 |
| 10 | `CR.MOD.1` | Completion rate, primary, MODELLED (%) | PHL 1981–2025 (n=45); 2024=95.9, 2025=96.2; KHM 1981–2025 (n=45); 2024=81.9, 2025=82.7; HKG **none**; CHN 1981–2025 (n=45); 2024=98.9, 2025=99.0 |
| 11 | `CR.MOD.2` | Completion rate, lower secondary, MODELLED (%) | PHL 1981–2025 (n=45); 2024=82.6, 2025=83.1; KHM 1981–2025 (n=45); 2024=59.0, 2025=60.8; HKG **none**; CHN 1981–2025 (n=45); 2024=94.3, 2025=94.7 |
| 12 | `CR.MOD.3` | Completion rate, upper secondary, MODELLED (%) | PHL 1981–2025 (n=45); 2024=73.1, 2025=73.5; KHM 1981–2025 (n=45); 2024=24.7, 2025=25.6; HKG **none**; CHN 1981–2025 (n=45); 2024=88.4, 2025=89.8 |
| 13 | `GER.5T8` | Gross enrolment ratio, tertiary (%) | PHL 1971–2026 (n=51); 2025=51.1, 2026=53.0; KHM 1971–2025 (n=41); 2024=21.4, 2025=21.1; HKG 1971–2025 (n=38); 2024=120.1, 2025=118.7; CHN 1970–2025 (n=52); 2024=76.9, 2025=75.8 |
| 14 | `PTRHC.1` | Pupil-teacher ratio, primary | PHL 1971–2025 (n=50); 2024=24.8, 2025=24.0; KHM 1971–2025 (n=44); 2024=49.2, 2025=49.5; HKG 1971–2025 (n=52); 2024=11.7, 2025=11.6; CHN 1970–2025 (n=50); 2024=16.1, 2025=15.9 |
| 15 | `PTRHC.2` | Pupil-teacher ratio, lower secondary | PHL 1998–2025 (n=18); 2024=21.9, 2025=21.1; KHM 1998–2025 (n=28); 2024=48.2, 2025=47.6; HKG 2001–2005 (n=5); 2004=17.6, 2005=17.8; CHN 1995–2025 (n=28); 2024=12.7, 2025=12.9 |
| 16 | `PTRHC.2T3` | Pupil-teacher ratio, secondary | PHL 1971–2025 (n=44); 2024=23.9, 2025=22.3; KHM 1971–2021 (n=10); 2007=28.9, 2021=9.9; HKG 1971–2025 (n=44); 2024=10.7, 2025=11.0; CHN 1970–2025 (n=52); 2024=13.2, 2025=13.2 |
| 17 | `PTRHC.3` | Pupil-teacher ratio, upper secondary | PHL 1998–2025 (n=18); 2024=29.1, 2025=25.3; KHM 1998–2021 (n=9); 2007=25.3, 2021=4.4; HKG **none**; CHN 1996–2025 (n=26); 2024=13.9, 2025=13.6 |
| 18 | `ROFST.1.CP` | Out-of-school rate, primary age (%) | PHL 1976–2025 (n=39); 2024=11.6, 2025=12.8; KHM 1997–2025 (n=23); 2024=3.7, 2025=11.9; HKG 1971–2025 (n=41); 2024=1.4, 2025=1.3; CHN 1987–1997 (n=11); 1996=7.9, 1997=6.7 |
| 19 | `ROFST.1T2.CP` | Out-of-school rate, primary+lower secondary age (%) | PHL 1979–2025 (n=27); 2024=12.2, 2025=13.3; KHM 1998–2025 (n=19); 2024=8.2, 2025=9.1; HKG 1977–2025 (n=33); 2024=1.2, 2025=1.2; CHN **none** |
| 20 | `ROFST.1T3.CP` | Out-of-school rate, primary+lower+upper secondary age (%) | PHL 1979–2025 (n=26); 2024=14.0, 2025=15.0; KHM 1998–2025 (n=14); 2024=18.2, 2025=21.2; HKG 2001–2024 (n=23); 2022=1.2, 2024=1.1; CHN **none** |
| 21 | `ROFST.2.CP` | Out-of-school rate, lower secondary age (%) | PHL 1979–2025 (n=27); 2024=13.2, 2025=14.0; KHM 1998–2025 (n=21); 2024=17.6, 2025=3.2; HKG 1977–2025 (n=32); 2022=1.2, 2025=1.0; CHN **none** |
| 22 | `ROFST.3.CP` | Out-of-school rate, upper secondary age (%) | PHL 1979–2025 (n=26); 2024=22.9, 2025=23.7; KHM 1998–2025 (n=16); 2024=48.9, 2025=58.9; HKG 2001–2024 (n=23); 2022=1.4, 2024=1.0; CHN **none** |
| 23 | `ROFST.H.1` | Out-of-school, primary age, household survey (%) | PHL 2004–2022 (n=3); 2018=2.3, 2022=3.6; KHM 2000–2020 (n=6); 2019=0.8, 2020=22.1; HKG **none**; CHN 2010–2020 (n=4); 2014=2.9, 2020=5.6 |
| 24 | `ROFST.H.2` | Out-of-school, lower secondary age, household survey (%) | PHL 2004–2022 (n=3); 2018=5.4, 2022=5.6; KHM 2000–2020 (n=6); 2019=10.4, 2020=33.1; HKG **none**; CHN 2010–2020 (n=5); 2018=2.7, 2020=6.7 |
| 25 | `ROFST.H.3` | Out-of-school, upper secondary age, household survey (%) | PHL 2004–2022 (n=3); 2018=17.2, 2022=13.8; KHM 2000–2020 (n=6); 2019=40.9, 2020=53.4; HKG **none**; CHN 2010–2020 (n=6); 2018=18.1, 2020=11.7 |
| 26 | `TRTP.1` | Trained teachers, primary (%) | PHL 2010–2025 (n=16); 2024=100.0, 2025=100.0; KHM 2001–2025 (n=25); 2024=100.0, 2025=100.0; HKG 1998–2025 (n=28); 2024=93.6, 2025=93.6; CHN **none** |
| 27 | `TRTP.2` | Trained teachers, lower secondary (%) | PHL 2016–2025 (n=10); 2024=100.0, 2025=100.0; KHM 2001–2025 (n=24); 2024=100.0, 2025=100.0; HKG **none**; CHN **none** |
| 28 | `TRTP.3` | Trained teachers, upper secondary (%) | PHL 2016–2025 (n=10); 2024=100.0, 2025=100.0; KHM 2001–2021 (n=5); 2007=99.8, 2021=100.0; HKG **none**; CHN **none** |
| 29 | `XGDP.FSGOV` | Government expenditure on education, % of GDP | PHL 1980–2025 (n=30); 2024=3.6, 2025=3.4; KHM 1998–2025 (n=23); 2024=2.0, 2025=2.0; HKG 1971–2025 (n=42); 2024=3.8, 2025=3.6; CHN 1971–2024 (n=27); 2023=3.9, 2024=4.0 |
| 30 | `XGOVEXP.IMF` | Government expenditure on education, % of total government expenditure | PHL 1982–2025 (n=29); 2024=16.5, 2025=15.2; KHM 1998–2026 (n=24); 2025=11.6, 2026=10.7; HKG 1981–2025 (n=33); 2024=15.7, 2025=15.1; CHN 1981–2024 (n=17); 2023=11.9, 2024=12.2 |

### Key UIS notes and caveats

- **Hong Kong does not report completion (`CR.1/2/3`) or pupil-teacher ratios to UIS.** Only `ROFST.3.CP` (out-of-school, marked low-reliability `*` in the release), `GER.5T8` (tertiary gross enrolment) and education-spending series exist for HKG. Any HK completion/pipeline claim must come from EDB/HKEAA, not UIS.
- **China's UIS completion series stop in 2020** (`CR.3` 2020 = 87.5); there is no UIS upper-secondary completion value for 2021–2025. The modelled series `CR.MOD.3` runs to 2025 (89.8).
- **Cross-vintage warning.** The manuscript's Philippines value of **67.0% upper-secondary completion in 2022 does not appear in the 2026-11 release**; the release gives **68.28%** for 2022, and **71.9% (2023)**, **75.0% (2024)** from the Philippine LFS. 2013 = **67.47%** (DHS 2013), which matches the manuscript's 67.5% baseline exactly. See `CLAIM_VERIFICATION.md`.
- **Source changes inside one series.** PHL `CR.3` is DHS-based in 2013 and 2017 and LFS-based from 2022; the 2023–2024 values come from the December LFS. Comparing 67.5% (2013 DHS) with 67–75% (2022–24 LFS) crosses survey instruments, not just time.
- Modelled series (`CR.MOD.*`) are UIS estimates for gap-filling, not observations. The manuscript's statement that "the UNESCO modeled trend continues rising through 2024" is borne out: PHL `CR.MOD.3` 72.1 (2022) → 73.1 (2024) → 73.5 (2025).
- Reporting lags: PHL `CR.3` observations exist for 1999, 2004, 2008, 2010, 2013, 2017, 2022, 2023, 2024 only. Do not interpolate between them.

## C. Hong Kong Education Bureau figures (xlsx, retrieved directly)

| File | Table | Coverage | Headline values |
|---|---|---|---|
| `raw/hongkong/edb_enrol-by-level.xlsx` → `data/edb_student_enrolment_by_level.csv` | Student Enrolment by Level of Education (thousands) | 2020/21–2025/26 | 2025/26: secondary 361.4k, primary 321.7k, post-secondary 354.7k, pre-primary 115.3k (pre-primary down from 166.8k in 2020/21) |
| `raw/hongkong/edb_educational-attainment.xlsx` → `data/edb_educational_attainment.csv` | Distribution of Educational Attainment (%) | 2020–2025 | 2025: degree course 27.6, sub-degree 5.7, diploma/certificate 3.1 (post-secondary total 36.4), secondary 47.6, primary & below 16.1 |
| `raw/hongkong/edb_sec.xlsx` → `data/edb_secondary_education.csv` | Secondary Education | 2020/21–2025/26 | 2025/26: 513 schools, 347,820 students in table population (S1–S3 184,003; S4–S6 160,833; S7 2,984), 30,329 teachers |
| `raw/hongkong/edb_gov-expenditure.xlsx` → `data/edb_government_expenditure.csv` | Government Expenditure on Education | 2020/21–2024/25 | 2024/25: HK$113,783M, **3.6% of GDP**, 15.1% of total government expenditure |

Note: the EDB enrolment total (361.4k secondary) and the EDB secondary table (347,820) differ because the latter excludes evening schools and some categories — use the table whose footnote matches the intended population.

## D. Country primary-source reports

| Country | Source | Access | What was extracted |
|---|---|---|---|
| Cambodia | NIS/ILO, **Cambodia Labour Force Survey 2019**, final report (218 pp.) | `nis.gov.kh` **not resolvable from this environment** (DNS → 198.18.1.209, a reserved benchmark address). PDF obtained from Wayback Machine; text extracted with pypdf 6.21.4 (`raw/cambodia/CLFS19_Final_Full_Report_EN.txt`, page markers inserted). | Table 5.3 (employed persons by education level, p.32/PDF p.48); Table 6.2 (informal/formal employment, p.36/PDF p.52); Tables 10.4–10.5 (unemployment by education/age); Table 12.1 (decent-work indicators, NEET). See `data/national_headline_figures.csv`. |
| China | Ministry of Education, **Educational Statistics 2024**, "Number of Students of Formal Education by Type and Level" | `en.moe.gov.cn` reachable | Higher education enrolment 58,436,680 (entrants 17,164,513; graduates 18,488,211); high-school-level 41,516,079 (regular senior secondary 29,222,814; secondary vocational 12,293,265); junior secondary 53,861,621; primary 105,843,743; pre-school 35,839,937. Not extracted: gaokao/zhongkao registrations, Double Reduction policy text. |
| Hong Kong | Kwo & Bray (2011), "Facing the shadow education system in Hong Kong", *IIAS Newsletter* 56, Spring 2011, p.20 | direct PDF | 1996 HKFYG telephone survey: primary 45%, lower sec 26%, middle sec 34%, senior sec **40%**. 2010 social-welfare-body survey: lower sec 72%, middle sec 82%, senior sec **85%**; authors write "Neither of these surveys should be considered statistically robust." Also: local universities served **2% of the age group** thirty years earlier and **19%** in 2010. |
| Philippines | PSA (LFS/FIES), DepEd, CHED | `psa.gov.ph` and `deped.gov.ph` return **HTTP 403** to this client; Wayback snapshots are stubs without tables | **No Philippine national administrative series retrieved in this pass.** PH evidence here rests on WDI/UIS only. Request: run PSA/DepEd pulls from a network that the sites permit (see `retrieval_log.md`). |

## E. Deliberately not used / not available

- **ILOSTAT** (`ilostat.ilo.org`) returned **HTTP 403**; no ILOSTAT bulk pull was made. Informality for Cambodia comes from CLFS 2019 instead. ILOSTAT would supply comparable informal-employment series for PHL/CHN/HKG that WDI lacks.
- **UNESCO UIS adjusted-net-attendance / NAR / GAR** indicators are not in the SDG4 release; they would require the UIS "EDU" full education dataset (not fetched).
- **UIS API** (`api.uis.unesco.org`) requires a subscription key; the bulk archive was used instead, which is why no key was needed.
- No value in the CSVs is interpolated, modelled by this project, or synthetic. Modelled UIS series are labelled `CR.MOD.*` and flagged in this ledger. Every value is traceable to a URL, a table, and a retrieval timestamp in `SOURCES.json`.

## F. GMR-style enrolment panel, 1980–2020, six countries (extension requested 2026-11-20)

Added after the first report, on the Lead's request, to cover **Cambodia, Japan, Hong Kong, Philippines, China and the Republic of Korea** with UIS enrolment series 1980–2020, using documented imputation for gaps. Full method and audit: `IMPUTATION_METHOD.md`; scripts: `scripts/`.

| File | Content |
|---|---|
| `data/gmr_observed_6countries_1970_2024.csv` | Observed only. 4,635 values, 171 country×indicator series, 1970–2024, each with its source layer (`UIS_SDG4_2026_11`, `UIS_EDUNONCORE_2020_02`, `WDI_UIS_derived`, `DERIVED_WDI`) |
| `data/gmr_annual_1980_2020_imputed.csv` | Annual skeleton 1980–2020: 7011 rows, status observed/imputed/not_imputed_long_gap/missing_no_anchor, plus method, anchor years, gap size, confidence, structural-break flag |
| `data/imputation_summary.csv` | 171 rows: per-series coverage audit |
| `data/gmr_wide_ger_1980_2020.csv` (+ `_status.csv`) | Wide GER panel, six levels, with O/I/L/. status codes |
| `data/gmr_source_disagreements.csv` | 18 cells where source layers disagree by >0.5 pp |
| `data/uis_edunoncore_6countries_long.csv` | UIS EDUNONCORE archive extract (1,417 values; NER, gross intake, PTR, 1971–2018) |

Status of the skeleton: **observed 3760 (54%), imputed 876 (12%), long-gap left unfilled 94, no anchor 2281.** Mean series coverage 66%. Best-covered series: KHM ger_tertiary 100.0%; JPN enrolment_primary 100.0%; JPN enrolment_secondary 100.0%; JPN ger_tertiary 100.0%; JPN oos_primary 100.0%; JPN ptr_primary 100.0%. Worst: HKG ner_preprimary 2.4%; KOR completion_primary 2.4%; PHL ner_upper_secondary 4.9%; PHL gross_intake_lower_secondary 9.8%; PHL ner_lower_secondary 9.8%; KOR gross_intake_lower_secondary 12.2%.

Three UIS layers were needed because no single UIS product carries level enrolment ratios for 1980–2020: the UIS SDG4 release (2026-11) has completion/OOS/PTR/tertiary GER; the UIS EDUNONCORE archive (Feb 2020) has net enrolment rates and gross intake ratios; and the WDI education series (which the World Bank documents as obtained via the UIS API) carry the level GERs. Source precedence, disagreement handling, interpolation limits (no extrapolation; gaps >15 years left unfilled) and break flags are in `IMPUTATION_METHOD.md`.

**Source-sparsity facts worth knowing before using this panel:** the current UIS/WDI vintage has Japan level enrolment *ratios* only for 2013–2023 (headcounts run 1971–2023, and UIS tertiary GER/PTR/out-of-school for Japan are complete); Korea's level ratios in WDI begin only in 2000 (no pre-2000 gross ratios; net enrolment rates from EDUNONCORE cover 1971–2017); Cambodia's upper-secondary ratios stop in 2008; China's completion series begin in 2010. These are gaps in the sources, not artefacts of the imputation, and they are why 32.5% of skeleton cells have no anchor at all.
