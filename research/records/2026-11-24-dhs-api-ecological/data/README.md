# data/ — DHS public API cache (OBSERVED aggregates, no microdata)

Everything here is from the free DHS Program API (`api.dhsprogram.com`), pulled **2026-11-24**, with no key
and no login. Nothing here is microdata: the unit is the DHS-published cell
(country × survey round × background category). No credentials, no gated file, no synthetic data.

## Files

| File | What it is |
|---|---|
| `indicator_catalogue.json` | The full public indicator catalogue (4,655 indicators: id + label), pulled as metadata to select indicators **before** any value was read. |
| `indicator_availability.json` | Metadata-only audit: for each candidate indicator, which `CharacteristicCategory` values the API publishes (requested with `returnFields=IndicatorId,CharacteristicCategory,CharacteristicLabel`; **`Value` was never requested**). This is the evidence for the pre-registration's indicator table and for the finding that the surviving-children measure has **no education breakdown**. |
| `raw/*.json` | The cached raw API pages for the pull, one file per indicator (all pages concatenated). Produced by `scripts/pull_dhs_api.py`. |
| `raw_surveys.json`, `raw_countries.json` | Survey and country metadata from the API (377 surveys; 92 countries). |
| `MANIFEST.sha256` | sha256 of every cached raw file + the panel CSV. |

## Exact API calls

```
GET https://api.dhsprogram.com/rest/dhs/indicators?f=json&perpage=1000&returnFields=IndicatorId,Label,IndicatorType&page=1..5
GET https://api.dhsprogram.com/rest/dhs/surveys?f=json&perpage=1000&returnFields=SurveyId,CountryName,DHS_CountryCode,SurveyYear,SurveyType,SurveyStatus,NumberOfWomen,RegionName,SubregionName,FieldworkStart,FieldworkEnd
GET https://api.dhsprogram.com/rest/dhs/countries?f=json&perpage=1000
GET https://api.dhsprogram.com/rest/dhs/data?indicatorIds=<ID>&breakdown=background&f=json&perpage=5000&page=1..N
    &returnFields=IndicatorId,Indicator,CountryName,DHS_CountryCode,SurveyId,SurveyYear,SurveyType,SurveyYearLabel,
                  CharacteristicId,CharacteristicCategory,CharacteristicLabel,Value,DenominatorUnweighted,
                  DenominatorWeighted,CILow,CIHigh,IsPreferred,IsTotal
```

`breakdown=background` is required for background-characteristic cells; without it the API returns national
"Total" only, and `breakdown=ALL` returns only age-group cells for the CEB indicators.

## Provenance caveats

- Values are **published DHS aggregates** (survey-weighted estimates as DHS publishes them), **OBSERVED**.
- `DenominatorUnweighted` / `DenominatorWeighted` are the published cell denominators; they are used as cell
  weights, not as women.
- The catalogue and cache are snapshots: DHS releases new surveys and re-releases indicators. The `sha256`
  manifest pins the vintage used in the analysis.
- Region category labels/counts differ across surveys; regions are never pooled across rounds.

## Pull revisions (2026-11-24, before any estimate)

1. `PR_DESL_W_WNM` is published crossed with a second dimension (number of living children). The first pull did
   not request `ByVariableId`, so the cache held 8 rows per education label. Fixed by re-pulling this one
   indicator with `ByVariableId,ByVariableLabel` and keeping `ByVariableId == 1000` (the main-effect cells);
   the national-total pull is filtered the same way. See `../AMENDMENT_01.md` A1.2.
2. Rate/median indicators (`FE_FRTR_W_TFR`, `FE_FRTR_W_GFR`, `PR_WTFR_W_WFR`, `FE_AAFB_W_M25`) publish **no
   denominators**; their cells are kept with `n = 0, has_denom = 0` and enter unweighted models only. See
   `../AMENDMENT_01.md` A1.1.
3. Panels in `data/panel_*.csv` are the pre-registered analysis inputs; `data/panel_checks.json` records the
   structural checks. `data/MANIFEST.sha256` pins every cached JSON and panel CSV.

## Compute location

The API pull and `build_panel.py` are network/IO-light and were run on the Mac. **All estimation ran on
region-42** (`/root/work/dhs-api/`, 48-worker `multiprocessing`, 13 s wall); see `../REPORT.md` §10 and
`../results/server/`. No estimate was computed on the Mac.
