# Access request 3 — World Bank Enterprise Surveys (credential/hiring module) + establishment census

**Status: DRAFT — HOLD. Do not send without the user's approval.**
**Reopens (rank 3):** credential requirement schedule in hiring; provider/firm entry costs; formal-job creation
elasticity to educated labour supply — the most load-bearing `not observable` parameters in
`04_data/econ_round2/PARAMETER_MAP.csv`.

## Ask

1. **Enterprise Surveys** — Philippines (2015, 2023) and Cambodia (2016) firm-level microdata. Variables:
   workforce composition by education; **education/credential requirements for typical positions**; hiring
   difficulty and the reason; skills as an obstacle; firm size, sector, ownership, exports, sales; location.
   Note: the ES public API returned HTTP 000 and the PHL 2015 country profile has no education-requirement table,
   so the unit-record route is the ask.
2. **Establishment census** (PSA/NSB) — establishment counts by size/sector/region to construct formal-job
   counts, not just shares.
3. If microdata is refused: the questionnaire module wording and any published tabulations of hiring requirements.

## Purpose and mapping

- Credential requirement share by level → the gate/floor parameter the model currently assumes.
- Firm entry/size distribution → provider/firm entry costs for the shadow sector (E2's cost-plus 1.5–4.2× rent
  diagnostic needs a cost benchmark).
- Educated workforce vs formal job creation → the elasticity behind the two-way model (R13 currently negative).

## Route, terms, cost

WB Enterprise Surveys microdata via the World Bank Microdata Catalog (credentialed request; terms restrict
re-publication). National statistics establishment census via the same NSB/PSA request as items 1 and 2 where
possible. Cost: 2–6 weeks.

## Deliverable if granted

`04_data/econ_round2/es_*.csv` (derived aggregates), `PARAMETER_MAP.csv` rows upgraded from `not observable` to
`observable (partial)` with the exact question wording, and request references in `retrieval_log.md`.
