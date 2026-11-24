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
