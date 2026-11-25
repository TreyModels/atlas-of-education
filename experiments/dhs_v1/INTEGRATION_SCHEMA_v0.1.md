# Atlas — DHS × macro matrix integration schema, v0.1 (2026-11-25)

**Owner:** `deepseek-dhs`. **Status:** DESIGN DRAFT — no prototype run yet. Companion to
`MATRIX_INVENTORY_2026-11-25.md`. **Rules in force:** exploratory/descriptive; no causal claims; wealth ≠
income; household size ≠ kin support; strata/PSU/weights mandatory; raw restricted microdata stays local;
no synthetic data presented as real; multiplicity corrected and limits reported.

## 1. Layer model (all joins one-directional, provenance-preserving)

```
L0  microdata (Mac only, restricted)
    PR / IR / HH recodes per country-wave, person & household rows,
    weights hv005 / v005, PSU hv021|v021, strata hv022-23|v022-23
        │  documented harmonization adapter (validated against published tables)
        ▼
L1  survey aggregate layer (non-disclosive; may leave the Mac)
    domain = country × wave × geo_level × region × age-band × sex × wealth_quintile
    estimate, design SE, CI, design df, n_unweighted, n_psu, weight_sum,
    denominator definition, suppression flag, source_id/source_hash
        │  key-level join on (iso3, year/period, geo where compatible)
        ▼
L2  macro linkage layer (independently sourced)
    country-year (and, only where defensible, admin1-year) indicators from
    M1/M3 matrices, M6 DHS-API panels, World Bank/UN series; each row keeps
    source_id, version/hash, unit, coverage years, imputation/estimate flag
        │  lag & alignment rules (§4); no interpolation of exposure into the outcome window
        ▼
L3  analysis matrix (the studies)
    one row per (exposure, outcome, geography, period, estimator spec)
    b, se, n_countries, n_effective, design, controls, multiplicity family, p, q, verdict
```

## 2. L1 schema (v0.1)

| field | type | notes |
|---|---|---|
| `record_id` | string | deterministic hash of the row content |
| `iso3`, `country` | str | ISO-3166 alpha-3 + survey name |
| `wave_id` | str | e.g. `KH2021DHS`, `ID2017DHS`, `PH2022DHS`, `VN2002AIS` |
| `year_start`, `year_end` | int | fieldwork window |
| `record_type` | enum | `person` \| `woman` \| `household` |
| `geo_level` | enum | `national` \| `region` (survey region only; **no displaced-GPS precision**) |
| `region_code`, `region_name` | str | as released; never reverse-engineered from jittered GPS |
| `age_lo`, `age_hi`, `sex` | int/str | domain definition (inclusive) |
| `wealth_quintile` | int 1–5 or null | survey-specific relative index, **not** income/expenditure |
| `variable` | str | e.g. `attendance`, `children_ever_born`, `early_birth`, `currently_in_school`, `early_union`, `household_size` |
| `estimand` | enum | `mean` \| `share` \| `ratio` |
| `estimate`, `se`, `ci_lo`, `ci_hi` | float | design-based (Taylor linearisation), normal approx |
| `design_df` | int | PSUs − strata |
| `n_unweighted`, `n_psu`, `n_strata` | int | raw counts |
| `weight_var`, `weight_sum` | str/float | `hv005` (person/household) or `v005` (woman); sum for weighted denominator |
| `denominator_def` | str | explicit (e.g. "women 40–49 with non-missing CEB and schooling") |
| `missing_n`, `missing_share` | int/float | for outcome and group variables |
| `suppressed` | bool | true if below disclosure/±precision rule (§3) |
| `source_id`, `source_hash` | str | microdata file + sha256, adapter version/hash |
| `notes` | str | recode decisions, comparability caveats |

## 3. Disclosure / reliability rules (pre-declared, applied programmatically)

* Suppress a cell when `n_unweighted < 30` **or** `n_psu < 2` **or** `design_df < 1` **or**
  the SE is not finite; mark `suppressed=true` and report the reason.
* Report `n`, `weight_sum` and `n_psu` for every published cell; never publish unweighted person-level data.
* Round estimates/SEs to 1 decimal of a percentage point / 3 significant figures before disclosure; never
  publish cell counts < 5.
* Keep the suppressed-cell ledger in the output (counts by reason) so coverage loss is visible.

## 4. Linkage rules (L1→L2) — temporal and geographic discipline

1. **Country-year only by default.** Subnational linkage is allowed only when (a) both sources use the same
   admin boundaries, (b) the macro source is genuinely subnational (not a national series disaggregated by
   population), and (c) geographic permissions allow the published region codes. DHS cluster GPS is displaced
   (urban clusters displaced up to 2 km, rural 5 km/1 % of country, 99 % are displaced/randomly shifted) —
   **never treat jittered coordinates as precise locations**; use released region codes only.
2. **Lagged exposures only when timing precedes outcome.** A macro exposure is eligible only if its
   measurement year ≤ outcome survey start year − declared lag (default 5 years for stock variables; record the
   lag in `L3`). No future-cause placebos as "nulls" (the matrix record shows they are not usable nulls).
3. **No interpolation across the outcome window.** Macro series used as exposures must be observed in the lag
   year or drawn from a documented imputation with its uncertainty; imputed macro cells carry `imputed=true`.
4. **Units and definitions must be compatible.** DHS wealth = relative asset index (not income/spend);
   household size = current household (not kin support); attendance = current attendance question, not
   completion. Only compatible definitions link (definition register per variable).
5. **Aggregation weights = survey weights**, with domain declared; report design-based SEs; never re-weight
   to population totals that the survey does not support.

## 5. Analysis discipline (L3)

* **Ecological fallacy guard:** household-level and country-level associations are reported separately and
  never used to infer the other level. Country-level covariates do not enter household regressions as if
  measured on households.
* **Pseudoreplication guard:** number of countries is the effective N for cross-country contrasts; report
  `n_countries`, median within-country n, and do not treat pooled individuals as independent for
  country-level claims. Within-country models preferred where ≥3 waves exist.
* **Few-country inference:** with 2–5 countries, report country-specific estimates and a simple
  random-effects/leave-one-country-out sensitivity, not a precise pooled effect; label as few-country.
* **Multiplicity:** pre-declare families (e.g. one family per experiment across country-waves; one family per
  matrix-link block) and report BH q-values and Holm-adjusted p alongside raw p. No cherry-picking.
* **Held-out checks where feasible:** hold out one wave/country for prior-matrices comparisons; report
  out-of-sample RMSE for any model-observation mapping.
* **Evidence labels:** every output row carries `exploratory_descriptive` by default; causal language banned.
  Simulation (M4/M5/M8) and empirical outputs are never mixed in one claim.

## 6. Feasibility classification (first pass)

| link type | status | basis |
|---|---|---|
| DHS survey-wave aggregate layer (L1) for KH/ID/PH/VN, E1–E8 as in availability table | **FEASIBLE (partial waves)** | local microdata + design variables verified present; E2/E3 VN and E1–E3 PH 1993/98 blocked |
| L1 → M1/M3 country-year macro spine (lead–lag coefficients, imputed or observed arms) | **FEASIBLE (prototype)** | M1/M3 committed result CSVs carry iso3? — **must verify country identifiers in `all_links.csv`/`matrix20.csv` are country-grain** (they are link-grain; a companion panel keyed `(iso3, year)` is needed and may not be committed → **PARTIAL** until verified) |
| L1 → M6 DHS-API public country-year panels | **FEASIBLE** | public panels committed (`panel_edu2_FE_*.csv`); same indicator family as DHS; lag rule applies |
| L1 → subnational admin1 macro indicators | **BLOCKED (default)** | no committed defensible subnational-year source found; DHS GPS displaced; requires new sourced data + permission |
| L1 → LSMS-ISA tutoring expenditure | **BLOCKED** | not held (bulge record: item scan only; no microdata) |
| Model-observation mappings (M8/M9/M10 observables) | **PARTIAL → queued for model/audit team** | case registry + equation suite exist; mapping needs the 150-equation inventory verified |
| Migration / agricultural price / education-spending studies | **BLOCKED** | no verified exposure data in holdings; must be authored only after source inventory (Bridge c756c22a requirement) |

**Immediate prototype plan (next milestone):**
1. Build the L1 aggregate layer for one country/wave as a worked example (KH 2021-22 + PH 2022) with all
   schema fields, design-based SEs, suppression ledger and benchmark comparison.
2. Build the L2 macro linkage stub: join KH/PH/ID/VN country-year rows to M6 public panels and a committed
   macro spine derived from M1/M3 result CSVs (verify identifiers first); keep source/version/unit/lag in
   every row.
3. Deliver a machine-readable `schema/aggregate_layer_v0.1.json` + `prototype/` CSV with 20–50 rows, clearly
   labelled exploratory; no restricted microdata, no household-level rows.

## 7. Open questions for the data/QA/model teams

1. Do M1/M3 committed results include a country-year panel key (iso3 × year) or only link-level coefficients?
   (needed for L1→L2 joins; data team to verify from `all_links.csv`/`matrix20.csv` and branch scripts).
2. Which macro spine should be canonical: M1 imputed panel (box-only), M3 observed 20-measure panel, or M6
   public DHS-API panels (committed)? Recommend M3 for observed links + M6 for DHS-specific comparators;
   M1 only with imputation flags.
3. QA sign-off criteria for the L1 layer (suppression thresholds, domain SE checks, benchmark tolerances).
4. Whether any subnational macro source exists in holdings (currently none verified) — if not, subnational
   linkage stays BLOCKED and is recorded as such.
