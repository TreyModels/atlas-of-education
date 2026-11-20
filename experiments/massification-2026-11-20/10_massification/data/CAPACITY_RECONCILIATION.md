# CAPACITY RECONCILIATION — two files, one canonical source (executor adjudication)

**Date:** 2026-11-20. **Owners:** data-hunter (`data/`), pattern-scout (`relations/`).
**Rule:** models may not pick whichever capacity file supports the story — this note fixes which file is canonical
for which purpose. This is a data-governance decision, not a claim.

| File | Owner | Content | Canonical for |
|---|---|---|---|
| `10_massification/data/STATE_CAPACITY.csv` (1,799 rows) + `STATE_CAPACITY_NOTES.md` | data-hunter | **Three separate dimensions** — fiscal 611 / delivery 509 / enforcement 679 rows; source/definition/`status` ∈ {observed, policy_fact, check, unable}; no imputation | **the three dimensions** |
| `10_massification/relations/data/state_capacity.csv` (1,182 country-years × 30 countries, 1971–2024) + `CAPACITY_LAYER.md` | pattern-scout | **Declared-weight composite** (`capacity_index`, `capacity_within`, `n_components`, `weight_coverage`, raw + normalised components, weights string) | **the derived composite only — labelled DERIVED, never a claim variable** |

## Resolutions
1. **Composite is derived; dimensions are primary.** The anchor takes fiscal / delivery / enforcement separately;
   the scout index is used only as a declared composite for descriptive sensitivity/timing checks, labelled
   `derived`. No single collapsed index may carry a capacity claim.
2. **tax/GDP discrepancy (recorded, not papered over).** Scout's index includes `tax_gdp` (weight 0.20) from WDI
   `GC.TAX.TOTL.GD.ZS`, with component + raw columns and weights metadata in the file (PHL 11.9/13.0/13.6 for
   2005/2015/2017). data-hunter's separate `GC.*` pull failed (`api.worldbank.org` HTTP 000 ×3) and is `unable`.
   Resolution: tax enters the index **only with scout's WDI provenance, never spliced** with the blocked rows;
   data-hunter re-attempts `GC.*` (+ derived volatility) next batch; if provenance cannot be timestamp-verified the
   component is dropped and weights renormalised (`weight_coverage` already tracks this).
3. **WGI governance `.15` blocked in BOTH files** → not proxied; index renormalises over the remaining **0.85**
   coverage; governance/enforcement is a declared assumption (R28).
4. **De jure ≠ de facto (binding for the anchor predeclaration).** UIS `YEARS.FC.*` (PHL **12** compulsory years) is
   distinct from delivery (PHL classroom backlog **110,954 rooms** SY2019-20; ≥1:50 congestion in 90% of NCR
   Northern Manila elementaries) and from enforcement (inspection/sanctions UNABLE). Three separate inputs — no
   collapse.
5. **BEPER 2019 = DATA BLOCKED** (not retrievable this pass; `WEB_BASELINE_NOTES.md`). No citation of unread material
   (D49). Schools/classrooms/procurement and attendance enforcement remain UNABLE.
6. **User-approval asks remain queued (nothing sent):** PSA FIES/APIS/LFS microdata; WB Enterprise Surveys
   credential/skills module; real per-pupil spending; fiscal tax/revenue/volatility; delivery schools/classrooms/
   procurement; enforcement inspection/sanctions (STATUS §3h/§3l).

## Required agent actions
- **data-hunter & pattern-scout:** ACK each other's capacity NEW and align headers/notes to this split (data-hunter
  owns dimensions; scout owns the derived composite).
- **exp1:** consume dimensions separately in the anchor predeclaration; index only as labelled sensitivity; carry the
  de jure/de facto gap explicitly; report `weight_coverage`/κ/weight sensitivity.
