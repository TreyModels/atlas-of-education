# Complexity extras — WDI proxies (only the cheap gap-fill; Lead-built ECI panel is authoritative)

The primary complexity panel is the **Lead-built** `../ECONOMIC_COMPLEXITY.csv` (+ `_WIDE`, `COMPLEXITY_METHOD.md`, `COMPLEXITY_MAP.md`), built from the Growth Lab Dataverse file `growth_proj_eci_rankings.csv` (doi:10.7910/DVN/XTAQMC, CC0) that `pattern-scout` archived in `09_relations/raw/`.

This folder adds only what that file does **not** contain — flagged WDI proxies — and records the gaps that could not be closed:

| File | Content |
|---|---|
| `COMPLEXITY_WDI_PROXIES.csv` | 4 WDI series × 6 countries, annual 1980–2024: manufacturing value added (%GDP), high-technology exports (% manufactured exports), exports of goods & services (%GDP), merchandise exports (current US$). Every row `status=proxy`. |
| `raw/wdi_*.json` | Raw WDI API payloads (hashes in `SHA256SUMS.txt`). |

## Not obtained (recorded, not fabricated)
- **COI / Economic Complexity Outlook Index**: the archived Dataverse dataset `DVN/XTAQMC` contains only `growth_proj_eci_rankings.csv` (ECI levels/ranks + 10-yr growth projection) and its data dictionary — **no COI file**. Harvard Atlas API paths probed (`/api/v1/…`, `/static/data/…`) all return 404/HTML; OEC API endpoints returned HTTP 400 without a key. COI therefore remains **not retrieved**.
- **Export diversification / product count with RCA>1**: would require the product-level trade files (Dataverse `FTUUJU` HS22 / `T4CHWJ` HS92 / `H8SFD2` SITC) and a full RCA computation; not built in this pass (cost > value here). The WDI proxies above are not substitutes for it.
- The ECI panel's own caveats (HS92 vs SITC vs HS12 revisions, level-vs-rank, HKG/KHM small-economy) are documented in the Lead's `../COMPLEXITY_METHOD.md`; do not mix revised baskets when comparing 1995 with 2024.
