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

## Structural gaps — explicit UNABLE status (recorded for D16 follow-up, 2026-11-20)

These are not omissions and must not be filled by imputation or proxy substitution without a flag:

| Gap | Status | Consequence |
|---|---|---|
| **HKG upper-secondary completion** (`UIS CR.3` and all `CR.*`) | **UNABLE — not reported to UIS by Hong Kong** (no UIS completion series exists, not a retrieval failure) | No observed upper-secondary completion for HKG in `UNIVERSALIZATION_SERIES.csv`. Any cohort-flow completion path for HKG must be a **declared assumption**, never fitted to UIS, and never interpolated from other countries. |
| **JPN upper-secondary completion** (and `CR.1/CR.2`) | **UNABLE — not reported to UIS by Japan** | Same as above: JPN has no UIS completion observations in this dataset. Japan's enrolment ratios exist only from 2013 in the current WDI vintage; do not extrapolate backwards. |
| **Productivity / value added per worker** (`SL.GDP.PCAP.EM.KD`, `SL.GDP.PCAP.EM.KD.ZG`) | **UNABLE in v1 — WDI API returned HTTP 000** during the pull window (retried twice) | `JOBS_AND_MARKETS_PANEL.csv` contains **no productivity series** in v1. Marked UNABLE/check; retry in batch 2. Do not substitute GDP per capita for it. |
| **ILOSTAT** (occupation ISCO, informality outside KHM, earnings by education) | **DATA BLOCKED — HTTP 403** on every path | Those quantities are absent; see "Not observable in these sources". |
| **OECD** (Education at a Glance 2024, Employment Outlook, PISA 2022) | **DATA BLOCKED — HTTP 403** | Retry via `sdmx.oecd.org` in batch 2 (timeboxed); otherwise record as blocked. |
| **PSA Philippines** (FIES/APIS/LFS) | **DATA BLOCKED — HTTP 403** | No PH microdata or summary tables. |

Rule restated: where a series is UNABLE or BLOCKED it stays blank in the CSVs with the reason in this file; it is **never imputed and never presented as an observation**.

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

## UNIVERSALIZATION_TIMING.csv — definitions, reconstruction method, censoring (A4/R19)

One row per country x level x threshold x measure. `status` ∈ {observed, reconstructed, check, unable}. `crossing_year` is the first observed year at or above the threshold that is followed by another observation also at or above it (sustained crossing); `band_earliest`–`band_latest` bracket the crossing between the last below-threshold observation and the first above-threshold one. `censoring=left` means the series is already above threshold at its first observation (crossing is only bounded: "<= first year"); `censoring=right` means it never reaches the threshold ("&gt; last year") — both are recorded as inequalities, not point estimates.

**Thresholds and measures.** Primary 50/90/95; secondary (total) 50/90; lower secondary 90; upper secondary 50/90; tertiary 15 (Trow "mass") and 50 (Trow "universal"). Measure is the **net enrolment rate (NER)** where a series exists (preferred: it is the closest available to "share of the cohort in school"), otherwise the **gross enrolment ratio (GER)**, labelled in the row. **Completion-based timing is UNABLE for HKG and JPN** (no UIS CR series exists) and is left out rather than proxied — those rows are `status=unable` with the national source that would fill them.

**Reconstruction (status=reconstructed).** GER_level(y) = WDI enrolment headcount for the level (SE.PRE/PRM/SEC/TER.ENRL) ÷ UN World Population Prospects 2024 single-age population (medium variant) summed over the official age window: primary 6–11, secondary 12–17 (PHL pre-2016: 12–15), tertiary 18–21. The WPP file reports population **in thousands** — converted to persons (a 1000x error here would silently wreck every ratio; caught in validation). The proportion is **derived, not imputed**: both numerator and denominator are observed series. Each reconstructed series is validated against the observed GER over its overlap window; median absolute difference is recorded in `derivation_method`, and confidence is **medium** if the median difference is ≤3 pp, **low** for 3–6 pp, **check** above that (or when there is no overlap). Reconstructed values are never presented as observations.

**Key censoring findings (why the timing regime matters).** JPN is censored, not merely hard to fit: reconstructed primary GER is already ~100% at the first available year (1971) — the crossing is **≤1971**, not dateable within the data window; JPN tertiary mass (15%) is likewise ≤1971, while JPN tertiary **universal (50%)** is reconstructed at **1994–95** (observed UIS series has a gap before 1999, so its bracket is wider: 1999–2013). KOR is censored at the left for primary (NER 95.9% in 1971 → ≤1971) and for upper-secondary GER (91.6% in 1994 → ≤1994); KOR secondary NER crosses 90 in **1996 (band 1992–96)**, and KOR tertiary mass/universal are reconstructed at **1980** and **1993** (observed series starts 2000 at 74.7%, consistent with a pre-2000 universal crossing). HKG: primary NER ≥95 in **1979 (1978–79)**, secondary NER ≥90 in **2016 (2015–16)**, tertiary mass **1992 (1984–92)**, tertiary universal **2008 (2007–08)**; HKG's upper-secondary GER ≥90 at **2012 (2011–12)** coincides with the 3-3-4 reform — a structural break, not a smooth crossing.

**Policy timeline.** `POLICY_TIMELINE.csv` lists compulsory-education and reform dates (JPN 1886/1947; KOR 1953/1985; HKG 1971/1978/2008/2012; CHN 1986; PHL 1987/2013; KHM 1996). Most are well-established policy facts that were **not re-verified against a primary document in this pass** — status `policy_fact` with that caveat in the `confidence` column; the ones tied to the user's own papers (PHL RA 10533 2013, HKG 3-3-4 2012) are sourced to workspace materials.

**Known weak spots in the timing table (do not hide).** HKG tertiary reconstruction disagrees with observed (reconstructed 1983 vs observed 1992 for the 15% crossing) — confidence `check`, use the observed row. JPN tertiary reconstruction (50% in 1994–95) is `check` too because the reconstruction denominator (WPP 18–21) omits older tertiary students; the observed row is authoritative where it exists. PHL secondary 90% NER is right-censored at 2015 (the NER series ends); the GER row (2022) is the usable one.

## Definition trap added 2026-11-20 — completion rate vs GER (different denominators)

The observed Philippine series has **completion above gross enrolment** at the same level and year. Verified from disk
2024 (`UNIVERSALIZATION_SERIES.csv`, `data/gmr_observed_6countries_1970_2024.csv`): **primary completion 98.30 vs GER
94.03**; **lower-secondary completion 92.41 vs secondary GER 85.29**; upper-secondary completion 75.03. This is not a
data error and must not be "corrected" by scaling: the **UIS completion rate is measured on children 3–5 years above
the official grade age**, while GER uses the level's age band — so the denominators differ and completion can exceed
GER. A cohort-flow synthetic model (see `10_massification/extensions/synthetic_2026-11-20/`) cannot produce
completion > entering GER and therefore reports later crossing dates than a GER-based reading.

**Rules that follow.** (1) Never mix completion-based and GER-based "universalisation" dates without stating the
measure — this is the R2 ambiguity in `facts/MUST_REPRODUCE.md`. (2) Any completion/GER ratio comparison must name
both series and their denominators. (3) A synthetic model may declare either the cohort-flow denominator or an
explicit measurement-factor convention, but must not silently fit completion up to observed levels (target encoding).
This also explains part of the old model's over-scale GER artefact (audit D-02).
