# 04_data — four-country data ledger

Owner: `data-hunter` (task-3). Retrieval window 2026-11-20 12:15–12:50 HKT. **Write scope honoured: everything here is under `04_data/`.**

## Read in this order

1. **`CLAIM_VERIFICATION.md`** — the manuscript's numbers, claim by claim, with verdicts. The headline results:
   - Cambodia's **6.6%** is now **resolved** to a primary table (CLFS 2019, Table 5.3): 6.6% of *employed persons 15+* hold a university degree (urban 13.8%, rural 2.9%). It is **not** a share of jobs and **not** a labour-force share. The "~6% for Phnom Penh" recollection is not supported.
   - Philippines upper-secondary completion: **67.5% (2013) verified exactly**; the manuscript's **67.0% (2022) is superseded** — the current UIS release gives 68.3% (2022), 71.9% (2023), **75.0% (2024)**.
   - Philippine attrition: "more than four in ten" is **verified for c.1999–2004** (1999 non-completion 40.3%) but **false of 2013** (32.5%); "more than half" is **not supported** by any completion series.
   - Hong Kong **85% senior-secondary tutoring** traced to Kwo & Bray (2011) reporting a 2010 survey, **with the authors' own "not statistically robust" caveat**; the manuscript's Bray & Lykins (2012) attribution is an unverified secondary citation.
   - HKDSE is **standards-referenced**, not norm-referenced (HKEAA).
2. **`DATA_LEDGER.md`** — one row per series: agency, indicator code, definition, country coverage, latest values, file pointer, caveats.
3. **`retrieval_log.md`** — every attempt including the blocked ones (Philippine PSA/DepEd HTTP 403, `nis.gov.kh` DNS blackhole, ADB 404, ILOSTAT 403).
4. **`SOURCES.json`** — URL, HTTP status, retrieval UTC, SHA-256, bytes, licence, notes for all 70 retrieved artifacts.

## Data files (`data/`)

| File | Rows | Content |
|---|---|---|
| `wdi_4countries_long.csv` | 4,671 | World Bank WDI, 48 indicators × PHL/KHM/HKG/CHN, 1990–2024, with definitions |
| `uis_sdg4_4countries_long.csv` | 2,120 | UNESCO UIS SDG4 release 2026-11, 30 indicators, with qualifiers/magnitude |
| `uis_sdg4_data_sources.csv` | 2,120 | Per-value data-source metadata (which survey produced each UIS value) |
| `national_headline_figures.csv` | 26 | Cambodia CLFS 2019, China MOE 2024, HK EDB 2025/26, Kwo & Bray 2011 |
| `edb_student_enrolment_by_level.csv` … | 4 files | HK EDB figures, verbatim table dumps |
| `gmr_observed_6countries_1970_2024.csv` | 4,635 | Observed-only GMR panel, six countries (adds Japan, Korea), 1970–2024, with source layer per value |
| `gmr_annual_1980_2020_imputed.csv` | 7,011 | Annual 1980–2020 panel with documented imputation and per-cell status flags |
| `imputation_summary.csv` | 171 | Coverage audit per country×indicator |
| `gmr_wide_ger_1980_2020.csv` / `_status.csv` | 246 | Wide GER panel and status codes for plotting |
| `gmr_source_disagreements.csv` | 18 | Cells where the three source layers disagree (>0.5 pp) |
| `uis_edunoncore_6countries_long.csv` | 1,417 | UIS EDUNONCORE archive extract (net enrolment, gross intake, PTR) |


`raw/uis/SDG_202611.zip` is the raw UIS archive (37 MB); its 407 MB extraction was deleted after filtering — re-extract with `unzip -o SDG_202611.zip -d extracted`. Total footprint of this folder: ~73 MB.

Tidy long format: `country, iso3, indicator_code, indicator_name, year, value, unit, definition, source, retrieved_utc`.

## Only two rules were load-bearing

- **No invented values.** Where a source was blocked, the cell is empty and the blocker is named in `retrieval_log.md`. The only modelled series present are UIS `CR.MOD.*`, labelled as such. Nothing was interpolated.
- **Definitions are kept apart.** Gross vs net enrolment, enrolment vs completion vs modelled completion, attainment stock vs current flow, informality vs occupation vs credential requirement. `DATA_LEDGER.md` opens with the conflation traps that matter for these four countries.

## Extension: 1980–2020 six-country panel with imputation

Added on request (see `IMPUTATION_METHOD.md`): Cambodia, Japan, Hong Kong, Philippines, China and Korea, UIS/WDI enrolment at pre-primary/primary/lower-secondary/upper-secondary/tertiary levels, with documented interpolation for gaps. **Imputed cells are flagged in `status`; they are not observations and must not be cited as such.** No extrapolation beyond observed endpoints; gaps longer than 15 years left unfilled.

## Known limits (stated plainly)

- **Philippines has no national administrative series in this pull** — PSA and DepEd returned HTTP 403 from this environment; only WDI/UIS (which are themselves UIS/ILO-derived) cover the Philippines. That is the weakest corner of the ledger.
- **Hong Kong is absent from UIS completion series** (HK does not report `CR.1/2/3`), so any HK pipeline claim must rest on EDB/HKEAA, not UIS.
- **China** is represented by MOE's 2024 enrolment table and UIS/WDI flows, but not by gaokao/zhongkao counts, NBS youth-unemployment releases, or the Double Reduction policy text.
- **ILOSTAT** (403) and the **UIS "EDU" full dataset** (not in the current release page) were not obtained; adjusted net attendance is therefore missing.

Requests for follow-up access are at the end of `retrieval_log.md` §6.
