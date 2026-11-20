# SUBNATIONAL_DATA_SEARCH — bounded public-source search (A8, part 4)

`data-hunter`, 2026-11-20. Public web only; no forms, no credentialed APIs, no proxy-variable substitution. Every 403/block is recorded. **Status: PARTIAL** — one high-value subnational dataset found (PIDS regional attainment), the rest blocked.

## Access log (PHL regional; CHN provinces)

| Target | URL | Result |
|---|---|---|
| PSA main site (FIES/APIS/LFS regional tables) | `https://psa.gov.ph/` and all subpaths tried | **HTTP 403** — bot block; no regional tables |
| PSA OpenSTAT / labour force survey tables | `psa.gov.ph/statistics/labor-force-survey*` | **HTTP 403** |
| data.gov.ph (CKAN + portal) | `https://data.gov.ph/`, `https://www.data.gov.ph/`, `data.gov.ph/api/3/action/package_search` | HTTP 200 but an Angular SPA shell; **no CKAN API**; no datasets served without JS |
| DepEd (enrolment, schools, teachers, regional) | `https://www.deped.gov.ph/` and article paths | **HTTP 403** |
| Official Gazette (RA texts) | `https://www.officialgazette.gov.ph/` | **HTTP 403** |
| NEDA | `https://neda.gov.ph/` | **HTTP 000** (DNS) |
| DBM | `https://www.dbm.gov.ph/` | **HTTP 000** (DNS) |
| CHED (UAQTEA / regional HEI tables) | `https://ched.gov.ph/uaqtea` | **HTTP 403** |
| Senate legacy press releases | `https://legacy.senate.gov.ph/...` | **HTTP 403** |
| PIDS | `https://www.pids.gov.ph/` | **HTTP 200**; the 2025 education book PDF (7.4 MB) was obtained and used |
| PRC (nurse licensure) | `https://prc.gov.ph/articles/exam-results` | HTTP 200 but results are per-examination pages without an aggregate annual table; no annual licensure series extracted |
| IBPAP (IT-BPM industry data) | `https://www.ibpap.org/` | HTTP 200; employment/revenue figures are JavaScript chart widgets, not machine-readable tables |
| World Bank Enterprise Surveys (PHL 2015/2023) | `enterprisesurveys.org` profile PDFs; API | PHL 2015 profile PDF obtained earlier (no credential table); **API HTTP 000**; 2023 wave not obtained |
| China NBS provincial / MOE provincial | not attempted beyond nbs.stats.gov.cn English release index (HTTP 200, no machine-readable provincial education-employment cross-tab found) | **UNATTEMPTED/PARTIAL** — CHN provincial series not obtained |

## What was found (and is now in `BASELINE_SERIES.csv`)

**PIDS (2025) regional education attainment and inequality table** (`BASELINE_SERIES.csv`, 144 rows): mean years of schooling and education Gini for **17 Philippine regions**, by sex, for the **1960–64 and 1990–94 birth cohorts**, computed by the PIDS authors from the PSA 2010 Census. This is genuine subnational attainment data and the only regional education series obtained in this pass — useful for portability tests (NCR vs ARMM is the widest gap: NCR male mean 11.53 → 12.05 years, ARMM 7.00 → 8.10; education Gini NCR 0.16 → 0.13 vs ARMM 0.40 → 0.34).

Source: PIDS (2025), *Making Philippine Education Reforms and Interventions More Transformative*, ch.3 Table 1, p.86 (PDF p.117), source line "Authors' calculations using PSA (2010)".

## What is missing for E4 (Bartik) and what would fill it

- **PH regional sector employment** (the Bartik shift-share input): blocked at PSA. Would need PSA LFS regional tables (403 here) or a public mirror; PSA OpenSTAT API needs an account. **UNABLE this pass.**
- **PH regional schooling outcomes** (completion/transition by region): DepEd 403. The PIDS book has some regional attainment but not regional completion/transition panels. **PARTIAL/blocked.**
- **CHN provincial enrolment-employment tables**: not obtained. NBS English pages do not carry provincial education-employment cross-tabs; the provincial yearbooks are Chinese-language and not machine-readable from here. **UNATTEMPTED** (recorded, not guessed).
- **PH regional wage/employment by sector**: PSA LFS/APIS blocked. Would need openstat.psa.gov.ph with an account, or the PSA's published statistical tables (403).

**Recommendation:** treat E4's subnational Bartik design as data-blocked from public sources; if the Council keeps E4, it needs either a PSA microdata request (user approval) or a World Bank/ADB subnational dataset that is public. Do not proxy regional employment with national sector shares.
