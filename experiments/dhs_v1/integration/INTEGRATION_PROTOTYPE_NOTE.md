# L1 → M6 matrix linkage prototype (v0.1, 2026-11-25)

**Owner:** `deepseek-dhs` (lead). **Status:** working prototype on non-disclosive aggregates only; no E1–E8
estimation has been run yet (QA gate closed). **Code:** `integration/build_l1_m6.py`; **outputs:**
`integration/prototype_l1_m6.csv`, `prototype_coverage.csv`, `prototype_missing_links.csv`,
`prototype_manifest.json`.

## What it joins

* **L1** = `harmonize/_out/aggregate_layer.csv` (data-team deliverable): survey-wave × experiment × group
  aggregates with design-based SEs and suppression flags; household microdata is not included and never leaves
  the Mac. 236 non-suppressed cells of 252 (16 suppressed, 6.3 %).
* **M6** = public DHS API indicator panels from the prior M6 record (`wt2/dhseco/.../data/panel_edu{2,4}_FE_*.csv`):
  six indicators (TFR, GFR, MNC, AAFB, WNM, WFR) × two education strata (`edu_level` 0 = no/primary,
  1 = secondary+), country-year public aggregates.
* **Join key:** country (ISO2) + indicator year. Two alignments per L1 cell: `same_year` (survey start year) and
  `lag5y` (start year − 5). Every row carries the indicator's survey id, year, education stratum, source panel
  and panel sha256.

## Result (exploratory)

| country | same_year rows | lag5y rows | experiments covered | indicators |
|---|---:|---:|---:|---:|
| KH | 3,156 | 1,148 | 8 | 6 |
| ID | 1,632 | 1,056 | 4 | 6 |
| PH | 1,426 | 928 | 8 | 6 |
| VN | 384 | 192 | 3 | 6 |

Total **9,922 prototype rows**; **146 missing links** (survey years with no M6 observation at the requested lag,
recorded in `prototype_missing_links.csv` rather than interpolated). Effective N for cross-country statements is
**4 countries**, not 9,922 rows.

## Guardrails encoded in the output

* `evidence_class = exploratory_descriptive_context`, `causal_claim = False`, `ecological_caution = True` on every
  row; the contextual indicator is never treated as a household-level measurement (ecological-fallacy guard).
* Lagging is **context only**: a lagged indicator is not an exposure unless a design demonstrates it precedes the
  outcome mechanism; no lagged regression or causal interpretation is produced here.
* No interpolation across missing years; missing links are explicit. Units are the published indicator's unit
  (indicator-specific; see the M6 catalogue) — not harmonised into a single scale.
* Subnational linkage remains **BLOCKED** (survey regions are not a defensible subnational macro unit; DHS GPS is
  displaced). M1/M3 country-year matrices are not local and are declared out of scope for this prototype.

## Next steps

1. After QA sign-off and E1–E8 execution, re-run L1→M6 with the final estimate table (same script; only L1 input
   changes) so the prototype reflects the executed cells rather than the data-team aggregate layer.
2. Add a **within/between decomposition** layer and a held-out check (e.g. hold out one wave or one country for
   any contextual association reported); with 4 countries, report country-specific estimates and leave-one-country-out
   sensitivity, never a precise pooled "effect".
3. Verify whether M1/M3 can be brought in locally (their panels are box-only); until then the macro spine is M6 +
   the L1 layer itself. Any addition of M1/M3 must preserve imputation flags and the wrong-country-null caveat
   (21.7 % false-positive rate at |t|>1.96 — these matrices cannot certify causal links).
