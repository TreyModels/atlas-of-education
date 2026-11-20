# DATA_NOTES_MASSIFICATION — task-34 minimum-viable data batch (v1)

`data-hunter`, 2026-11-20 14:35 Asia/Shanghai. **Observed values only; no imputation is presented as observation.** Built by reusing the on-disk observed panels (`04_data/data/gmr_observed_6countries_1970_2024.csv`, `04_data/econ_round2/data/econ_panel_round2.csv`, `04_data/data/national_headline_figures.csv`) rather than re-fetching, because the WDI API was returning intermittent HTTP 000 during this window. Every row carries source, vintage and retrieval time; `status` distinguishes `observed`, `derived` (arithmetic, flagged) and `check` (proxy — do NOT use as a target).

## Files in this batch

| File | Rows | Content |
|---|---|---|
| `UNIVERSALIZATION_SERIES.csv` | 2,458 | GER by level (pre-primary, primary, lower sec, upper sec, secondary, tertiary), NER by level, completion (primary/lower sec/upper sec), out-of-school rates, gross-intake transition proxies, population and derived 0–14 cohort size. Six countries, 1970–2026 for the education flows. |
| `JOBS_AND_MARKETS_PANEL.csv` | 5,622 | Sector employment (agri/industry/services), status in employment (wage/self-employed/employers/vulnerable), LFPR total + youth, unemployment total/youth, NEET, GDP p.c. (PPP, current US$), GDP growth, urbanisation, remittances (%GDP and US$), population and age structure, inflation, trade openness, teachers, pupil-teacher ratios, education spending (%GDP, %budget), UIS spending cross-checks — plus Cambodia CLFS 2019 formality/credential rows. Annual 1995–2024 (education flows 1970–2026). |

Key headline values (all `status=observed`): upper-secondary completion PHL 75.0 (2024), KHM 27.9 (2023), CHN 87.5 (2020), KOR 99.5 (2023) — **HKG and JPN have no UIS completion series**; tertiary GER PHL 53.0 (2026), KHM 21.1 (2025), HKG 118.7 (2025), CHN 75.8 (2025), KOR 111.9 (2024), JPN 65.2 (2024). Jobs 2024: wage-and-salaried share PHL 63.5, KHM 44.2, HKG 92.2, CHN 61.9, KOR 77.1, JPN 90.8; vulnerable employment KHM 52.6, PHL 33.9, CHN 33.8, KOR 17.9, JPN 7.6, HKG 5.8; agriculture KHM 34.2, CHN 22.2, PHL 21.2, KOR 5.2, JPN 2.9, HKG 0.2.

## What is BLOCKED or missing (recorded, not omitted)

**DATA BLOCKED:**
- **ILOSTAT** (`ilostat.ilo.org`) — HTTP 403 on every path. No ILOSTAT tables pulled; occupation (ISCO), informality by country other than Cambodia, and earnings by education remain unavailable from this route.
- **OECD** (`oecd.org`, including Education at a Glance 2024 and the PISA 2022 database pages) — **HTTP 403** bot block. OECD tables not obtained in this batch; retry via `sdmx.oecd.org`/alternate endpoints in batch 2.
- **PSA (Philippines)** — HTTP 403 (continuing). No FIES/APIS/LFS microdata.
- **Enterprise Surveys data API** — `api.enterprisesurveys.org` HTTP 000; the PHL 2015 country-profile PDF is archived in `04_data/econ_round2/raw/` but contains no education-requirement table; the 2023 PHL wave is not obtained.
- **WDI productivity codes** (`SL.GDP.PCAP.EM.KD`, `SL.GDP.PCAP.EM.KD.ZG`) — HTTP 000 during this window; productivity/value-added-per-worker is therefore **missing from v1** and will be retried.

**Not observable in these sources (structural gaps):**
- **Transition rates to tertiary, repetition, dropout** — not in the UIS SDG4 bulk; gross-intake ratios are provided as `status=check` proxies only.
- **Occupation (ISCO major groups)** — needs ILOSTAT or national LFS microdata; blocked.
- **Education-occupation mismatch** — requires occupation × education crosstabs; not obtained.
- **Wages/earnings by education** — requires LFS/FIES/ILOSTAT microdata; not obtained (this is the single biggest gap for push-pull).
- **Informality outside Cambodia** — ILOSTAT blocked; KHM 2019 CLFS is the only observed informality series on disk.

## Definition traps (do not mix)

1. **Status ≠ formality**: `SL.EMP.WORK.ZS` (wage and salaried) is status in employment; a salaried worker can be informal. The only observed informality numbers here are Cambodia's 88.3% informal / 11.7% formal (CLFS 2019, denominator = employed persons, not labour force).
2. **Gross ≠ net enrolment**: `ger_*` (gross) can exceed 100% (KHM primary 109, KOR tertiary 111.9); `ner_*` (net) is bounded by 100. Never mix in one fit.
3. **Completion ≠ enrolment**: completion is a cohort-attainment measure (population 3–5 years past graduation age). Using GER as completion will overstate throughput.
4. **Gross-intake ratios (AIR.1/AIR.2) are throughput proxies**, not transition rates — they are `status=check`.
5. **UIS vs WDI vintages differ for the same concept** (education spending PHL: WDI 3.93% of GDP 2024 vs UIS 3.45% 2025). Do not average.
6. **Latest UIS years (2025–2026) may be UIS estimates, not national observations** — check the UIS `QUALIFIER` (`UIS_EST`) before using the last one or two points in a logistic fit.
7. **ILO modelled estimates**: all `SL.*` series in WDI are ILO modelled, not national LFS tabulations.
8. **PPP ≠ current ≠ constant US$**: use `NY.GDP.PCAP.KD`/growth for real comparisons; `NY.GDP.PCAP.PP.CD` is current international $.
9. **Cohort size is derived**: `cohort_population_0_14` = total population × 0–14 share (both observed, the product is flagged `status=derived`). It is 0–14, not the school-age cohort by level.
10. **HKG is 100% urban** by construction; urbanisation cannot be a varying regressor there.

## Answer to lit-archivist ASK (bridge id 2e5c4bad) — ILO/OECD/WB jobs+skills tables

| Ask | Status now | Plan |
|---|---|---|
| 1. ILO WESO sectoral/informality/youth tables | **not yet obtained** — `ilo.org` root returns HTTP 200 (site reachable), specific publication pages 404; corpus work is batch 2 | batch 2: locate WESO/GET PDFs via ilo.org publications search; extract tables with page refs |
| 2. ILO "Women and Men in the Informal Economy" informality for PHL/KHM | **not yet obtained**; KHM 2019 CLFS (88.3%) is the on-disk observed fallback | batch 2; KHM already available from CLFS |
| 3. ILO Global Wage Report real wage growth by region | **not yet obtained** | batch 2 |
| 4. OECD Education at a Glance — tertiary attainment/enrolment KOR/JPN, transition/returns | **DATA BLOCKED — oecd.org HTTP 403** | retry OECD SDMX/stat API and Wayback; if still blocked I will post DATA BLOCKED explicitly |
| 5. WB Enterprise Surveys PHL/KHM (2023 PHL wave) | PHL 2015 profile PDF archived (no credential table); **2023 wave not obtained; ES data API HTTP 000** | batch 2: try ES site country pages + Wayback; record block |
| 6. STEP skills surveys PHL/KHM | **no STEP coverage found for PHL/KHM**; STEP microdata credentialed where they exist | record negative; no STEP claim for these two |

Recommendation for `LABOUR_MARKET_REPORTS.md`: cite only what is listed above as obtained; treat items 1–5 as "pending batch 2" and 6 as a negative finding until I post the corpus NEW.
