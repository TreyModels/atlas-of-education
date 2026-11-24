# `data/` — what is in here (and what is deliberately not)

All three files are **derived from public, non-gated sources**: the DHS Program public API
(`api.dhsprogram.com`) and public DHS Program web pages. **No DHS microdata is in this repository.**
DHS microdata cannot be redistributed (Terms of Use, `research/records/2026-11-24-dhs-acquisition/data/source_log.txt`,
section 1); this repository is public, so the woman-level files must never be committed here.

Pulled **2026-11-24T10:07Z** (18:07 Asia/Shanghai) from this worktree. Exact URLs and HTTP codes are in
[`source_log.txt`](source_log.txt).

| File | Rows | What it is | Why it is here |
|---|---|---|---|
| `dhs_ir_inventory_targets.csv` | 92 | Public file **inventory** metadata for the Individual Recode (IR) Stata files of the 14 target countries: `FileName`, `SurveyId`, survey type/status, fieldwork window, unweighted women, sample points, women's universe, bytes | Tells Trey exactly which ZIPs to download and what to expect inside them; lets the analysing code assert it has the right file |
| `ceb_education_cells.csv` | 318 | Published **aggregate** cells: mean children ever born to women age 40–49 by education, per survey-round, with `DenominatorUnweighted` / `DenominatorWeighted` | Quantifies the cohort-cell sample-size risk (§8 of the plan) with real denominators instead of a guess; also an external cross-check for the microdata once it arrives |
| `source_log.txt` | 58 | Probe log: every public page and API endpoint touched, HTTP status, and what it establishes | Evidence that the wall was tested and **not** breached; provenance for every URL cited in the plan |

## Exact provenance

`dhs_ir_inventory_targets.csv`
: assembled from
  `https://api.dhsprogram.com/rest/dhs/datasets?returnFields=FileName,CountryName,SurveyYear,SurveyId,FileType,FileFormat,FileSize,DatasetType&f=json&perpage=1000&page=1..16`
  (15,518 dataset records; 2,005 Individual Recode records; 2,000 unique IR filenames; 85 countries),
  filtered to `FileType == "Individual Recode"`, `FileFormat` starting `Stata`, and the 14 target countries,
  then joined on `SurveyId` to
  `https://api.dhsprogram.com/rest/dhs/surveys?f=json&perpage=1000&returnFields=SurveyId,CountryName,SurveyYear,SurveyType,SurveyStatus,NumberOfWomen,NumberOfSamplePoints,FieldworkStart,FieldworkEnd,UniverseOfWomen,PublicationDate,ReleaseDate`
  (377 surveys).

`ceb_education_cells.csv`
: from
  `https://api.dhsprogram.com/rest/dhs/data?indicatorIds=FE_FRTY_W_MNC&breakdown=background&countryIds=MW,ET,UG,LS,TZ,KE,MZ,GH,KH,PH,VN,BJ,NM,SZ&f=json&perpage=5000`
  (2,550 records; the 318 rows with `CharacteristicCategory == "Education"` are kept).
  The indicator is "Completed fertility of women age 40–49" (mean children ever born).
  Note: `breakdown=background` is required for background-characteristic cells;
  `breakdown=ALL` returns only age-group cells for this indicator.

## Caveats that travel with these files

- **The inventory is metadata, not data.** File names and byte sizes are DHS's public catalogue; the
  catalogue also lists files for surveys whose *data* are restricted (GPS/HIV, some country releases).
  A name in this CSV does **not** imply Trey will be approved for that country.
- **Release versions matter.** The same survey can appear with several release codes (`...7A`, `...7B`,
  `...73`). Use the exact `FileName` in the CSV; do not "download the latest" blind. Record the sha256 of
  the ZIP you actually receive, since DHS re-releases files with the same name under new version digits.
- **Aggregate cells are not microdata.** `ceb_education_cells.csv` is country × survey × education,
  not a woman. It cannot answer the individual-level question and must never be presented as doing so
  (the earlier attempt on `research/dhs-micro-2026-11-23 @ 31ded00` is an *ecological* analysis for exactly
  this reason).
- **No synthetic substitute.** DHS "model datasets" (public, no registration) are practice files built on
  the DHS-6 questionnaire; they are not country data and must not stand in for the real test.
