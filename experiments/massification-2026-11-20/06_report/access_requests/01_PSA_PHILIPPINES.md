# Access request 1 — Philippine Statistics Authority (PSA): FIES / APIS / LFS microdata

**Status: DRAFT — HOLD. Do not send without the user's approval.**
**Reopens (LOOP_CLOSEOUT §4 rank 1):** national shadow-education incidence; wage premium by education;
formal/informal transitions; LFPR by education; formal wage premium.

## Datasets and exact variables

1. **FIES (Family Income and Expenditure Survey)** — 2015, 2018, 2021, 2023 (and 2012 if available).
   Variables: total and per-capita income; **education expenditure** items (tuition, tutoring/review centres,
   other education-related); household size, age/sex of members, highest grade completed; urban/rural; region;
   weights.
2. **APIS (Annual Poverty Indicators Survey)** — 2016–2024. Education expenditure; school attendance/enrolment;
   working children; reason for not attending; weights.
3. **LFS (Labor Force Survey)** — 2010–2024 (all rounds). Highest grade completed; occupation; class of worker
   (wage/salaried, self-employed, unpaid family); industry; earnings where collected; underemployment; weights.

## Purpose and mapping

- Tutoring/review-centre expenditure → shadow-education incidence by income quintile and region (national, not
  the 2010 select sample). Fits `04_data/TARGETS_SHADOW.csv` rows currently `unresolved` for PHL.
- Earnings x education → Mincer/wage premium by level (currently `not observable` in `PARAMETER_MAP.csv`).
- Class of worker x education → formality/status transitions (needs two waves; FIES panel component).
- Attendance x work → the four child states (school/work/both/neither) for `childworld` validation.

## Route, terms, cost

PSA Data Enclave / microdata request (PSA website currently returns HTTP 403 to automated fetches; access is by
application). Alternative: World Bank Microdata Catalog mirror if licensed. Cost: application + 2–6 weeks;
restricted-use terms apply (no re-publication of unit records). Output: derived aggregates only, with the PSA
citation and the request reference.

## Deliverable if granted

`04_data/data/psa_*.csv` (derived aggregates), rows added to `TARGETS_SHADOW.csv`/`TARGETS_FLOW.csv` with
`source_access=PSA request`, and the exact request reference in `retrieval_log.md`.
