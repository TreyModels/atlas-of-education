# retrieval_log.md — every attempt, including blocked ones

Window: **2026-11-20, 12:15–12:50 HKT (04:15–04:50 UTC)**. Client: `curl` and bundled `/usr/bin/python3` 3.9.6; `pypdf` 6.21.4 and `openpyxl` installed into `/tmp` (outside the workspace) only to read PDFs and xlsx. No credentials were used anywhere. No value was guessed, interpolated, or substituted.

Status vocabulary: **OK** (retrieved and used) / **BLOCKED** (host or policy refused) / **PARTIAL** (retrieved but not usable for the intended extraction) / **SKIPPED** (deliberately not attempted, with reason).

## 1. World Bank WDI API — OK

| Attempt | Result |
|---|---|
| `GET https://api.worldbank.org/v2/country/PHL/indicator/SE.TER.ENRR?format=json` (connectivity probe) | HTTP 200 |
| 41 indicator pulls, `country/PHL;KHM;HKG;CHN/indicator/{code}?format=json&per_page=4000&date=1990:2024` | HTTP 200 each; raw JSON in `raw/worldbank/{code}.json` |
| `SE.PRM.PTRN` | **HTTP 200 but JSON error `Invalid value`** — indicator code retired. Replaced with `SE.PRM.ENRL.TC.ZS` (retrieved, 140 rows). |
| `SE.SEC.CMPT.UP.ZS` | **Invalid code** in the WDI catalogue — upper-secondary *completion* is not published in WDI. This is why the 67.0%/67.5% claim had to be checked against UIS `CR.3`, and it is confirmed: WDI has no equivalent series. |
| `SP.POP.1524.TO.ZS` | **Invalid code**; skipped. Population shares `SP.POP.0014.TO.ZS`, `SP.POP.1564.TO.ZS` retrieved instead. |
| 10 additional indicator pulls (`SE.SEC.ENRR.UP`, `SE.SEC.UNER.LO.ZS`, `SE.SEC.ENRL.VO.ZS`, `SE.SEC.CUAT.PO.ZS`, `SE.SEC.CUAT.LO.ZS`, `SE.PRM.UNER.ZS`, `SE.PRM.TCAQ.ZS`, `SL.UEM.NEET.ZS`, …) | HTTP 200 each |
| `GET https://api.worldbank.org/v2/indicator?format=json&per_page=25000` (indicator catalogue with definitions) | HTTP 200; `raw/worldbank/_indicator_catalog.json`. Used for the `definition` column and to discover that some codes are retired. |

Landing: 48 indicators, 4,671 rows, `data/wdi_4countries_long.csv`. No API key needed; terms are World Bank open data (CC BY 4.0).

## 2. UNESCO UIS — OK via bulk archive (API not attempted for lack of a key)

| Attempt | Result |
|---|---|
| `GET https://api.uis.unesco.org/api/public/...` | **SKIPPED** — requires a subscription key (documented at `apiportal.uis.unesco.org`). Not requested; bulk route used instead. |
| `GET https://databrowser.uis.unesco.org/download/UIS_EDU.csv` | HTTP 404 |
| `GET https://api.uis.unesco.org/bulk/UIS_EDU.csv` | HTTP 404 |
| `GET https://sdg4-data.uis.unesco.org/` | HTTP 000 (host not resolvable/refused) |
| `GET https://databrowser.uis.unesco.org/resources/bulk` | HTTP 200 — lists the current release archives |
| `HEAD https://download.uis.unesco.org/bdds/202611/SDG.zip` | HTTP 200, 37,025,136 bytes, Last-Modified 2026-11-17 |
| `GET` that zip | HTTP 200, downloaded to `raw/uis/SDG_202611.zip`, unzipped to `raw/uis/extracted/` (7 files, 407 MB uncompressed), filtered, and the extraction then deleted to keep the iCloud workspace small — the zip remains the authoritative artifact and re-extraction is lossless. README inside states release 2026-11, data extracted 2026-10-22, licence CC BY-SA 3.0 IGO. |
| Filter `SDG_DATA_NATIONAL.csv` to PHL/KHM/HKG/CHN × 30 indicators | 2,120 rows → `data/uis_sdg4_4countries_long.csv`; 2,120 source-metadata rows → `data/uis_sdg4_data_sources.csv` |
| `OPRI.zip` (61 MB, other indicators) | **SKIPPED** — not needed for the manuscript claims. |
| UIS "EDU" full education dataset (would contain adjusted net attendance, NAR/GAR, financial indicators) | **SKIPPED/NOT FOUND** — not listed in the 2026-11 release page (only SDG, OPRI, DEM). Large gap, recorded in `DATA_LEDGER.md` §E. |

## 3. Cambodia — several routes, one success

| Attempt | Result |
|---|---|
| `GET https://www.nis.gov.kh/nis/CLFS/CLFS19_Final_Full%20Report_EN.pdf` with `curl` | **HTTP 000.** `nslookup www.nis.gov.kh` → 198.18.1.209, a **reserved benchmarking range** — the name does not resolve to a real public address in this environment. |
| Same URL with `web_fetch` | **BLOCKED by tool policy**: "URL hostname resolves to a non-public IP address". |
| `GET https://web.archive.org/web/2024id_/https://www.nis.gov.kh/nis/CLFS/CLFS19_Final_Full%20Report_EN.pdf` | **HTTP 200, 17,830,983 bytes** → `raw/cambodia/CLFS19_Final_Full_Report_EN.pdf` |
| Text extraction with pypdf 6.21.4 | 218 pages, 378,370 characters → `raw/cambodia/CLFS19_Final_Full_Report_EN.txt` with page markers. **Found Table 5.3 (degree share 6.6%) and Table 6.2 (informality 88.3%) directly**, resolving the handoff's open question. |
| NIS 2019 Census thematic reports ("Literacy and Educational Attainment", "Economic Activities and Employment") | **SKIPPED** — surfaced in search results, direct download blocked by the same DNS issue; the CLFS tables already answer the question. |
| ILO Cambodia Labour Force Survey 2019 report (`ilo.org/publications/...`) | **SKIPPED** — the CLFS final report is the primary and was obtained. |
| 2019/20 CSES | **SKIPPED** — not needed for the resolved claim; would be the route for household expenditure/tutoring, which the handoff flags as desirable but not required. |

## 4. Hong Kong — OK

| Attempt | Result |
|---|---|
| `GET https://www.censtatd.gov.hk/en/web_table.html?id=130-00001` | HTTP 200 but the table is rendered by JavaScript; **PARTIAL**, no data extracted, not pursued once EDB xlsx was found. |
| `GET https://www.edb.gov.hk/en/about-edb/publications-stat/figures/index.html` | HTTP 200 |
| 4 xlsx figures: `enrol-by-level.xlsx`, `educational-attainment.xlsx`, `sec.xlsx`, `gov-expenditure.xlsx` | HTTP 200 each → `raw/hongkong/`, converted with openpyxl to `data/edb_*.csv` |
| `GET https://www.ugc.edu.hk/eng/ugc/stat/statistics.html` | **HTTP 404** — UGC statistics path changed; not pursued. |
| `GET https://www.hkeaa.edu.hk/en/our_services/exam_stat/` and `/en/hkdse/introduction/` | HTTP 200. Introduction page gave the **standards-referenced** wording used in `CLAIM_VERIFICATION.md` §5. Aggregate DSE candidature/JUPAS series **not extracted** (the statistics page serves per-school sample reports, not the aggregate tables). |
| `GET https://www.iias.asia/sites/iias/files/nwl_article/2019-05/IIAS_NL56_20_0.pdf` | HTTP 200 → `raw/hongkong/bray_iias_hk.pdf`. **Found the 85% senior-secondary tutoring figure and its caveat** (Kwo & Bray 2011, p.20). |
| `GET https://core.ac.uk/download/pdf/45602862.pdf` (Bray, "Forty years ago…") | **HTTP 403** |
| ADB Bray & Lykins (2012) book `https://www.adb.org/sites/default/files/publication/29704/shadow-education.pdf` | **HTTP 404** (both direct and Wayback). Book not retrieved; the manuscript's secondary citation remains unconfirmed. |

## 5. China — partial success

| Attempt | Result |
|---|---|
| `GET https://en.moe.gov.cn/documents/statistics/` | HTTP 200 but 97-byte JavaScript redirect to `./2024/national/` |
| `GET https://en.moe.gov.cn/documents/statistics/2024/national/` | HTTP 200, index of tables |
| `GET .../202603/t20260319_1431433.html` ("Number of Students of Formal Education by Type and Level") | HTTP 200 → `raw/china/moe_students_formal_2024.html`. **Full 2024 enrolment table extracted** (bilingual HTML table parsed). |
| Three sibling table pages initially fetched by guessing IDs | Wrong tables (kindergarten); kept in `raw/china/` for audit, not used. |
| `GET http://www.moe.gov.cn/jyb_sjzl/moe_560/` | HTTP 200 but 77-byte body (JS redirect); **PARTIAL**. |
| `GET https://www.stats.gov.cn/english/PressRelease/` | HTTP 200 → index page. Individual youth-unemployment releases **not extracted** (time-boxed; and the 2023 definition change makes NBS/ILO comparisons non-trivial — flagged in the ledger). |
| Wayback captures of specific MOE/NBS articles guessed by URL | HTTP 404 on both guesses; not pursued further. |
| Double Reduction (2021) policy text, gaokao/zhongkao registration counts | **SKIPPED** — the manuscript makes no numeric claim that depends on them, and inventing them was not an option. Recorded as an open request. |

## 6. Philippines — BLOCKED

| Attempt | Result |
|---|---|
| `GET https://psa.gov.ph/statistics/labor-force-survey` | **HTTP 403** (bot protection) |
| `GET https://psa.gov.ph/statistics/labor-force-survey/statistical-tables` | **HTTP 403** |
| `GET https://deped.gov.ph/` | **HTTP 403** |
| `GET https://deped.gov.ph/2024/08/26/deped-reports-over-26-9-million-learners-enrolled-for-sy-2024-2025/` | **HTTP 403** |
| Wayback snapshots of `deped.gov.ph` home and PSA LFS page | HTTP 200 but **stub/landing pages** without tables (`raw/philippines/`, 24 KB and 353 KB of chrome/navigation). Not usable. |
| `GET https://openstat.psa.gov.ph/` | **SKIPPED** — not attempted after the 403 pattern; recorded as a request instead. |

**Consequence:** no Philippine *national administrative* series (DepEd enrolment, CHED, TESDA, PSA LFS/FIES) is in this ledger. Philippine evidence here is WDI + UIS only, both of which are themselves UIS/ILO-derived — so the verification is not fully independent of the manuscript's own source. This is the single biggest limitation of the pull and should be stated in the methods note.

**Request to whoever has a permitted network:** run the PSA/DepEd/CHED pulls (they need an ordinary browser User-Agent at minimum, possibly an institutional IP), and the UIS "EDU" dataset for adjusted net attendance. Drop files anywhere under `04_data/raw/` and re-run the conversion script pattern documented in `DATA_LEDGER.md`.

## 7. Other sources attempted / considered

| Source | Result |
|---|---|
| ILOSTAT `https://ilostat.ilo.org/data/` | **HTTP 403**. No ILOSTAT series pulled; comparability tabulations for PHL/CHN/HKG are missing as a result (Cambodia informality came from CLFS instead). |
| UNESCO EFA Global Monitoring Reports / SDG4 methodological notes | **SKIPPED** — the UIS release README and embedded metadata supplied release date, definitions, licence and per-value data sources; no need to fetch GMR PDFs. |
| UN World Population Prospects (`population.un.org/wpp/`) | **SKIPPED** — WDI population/age-structure/fertility series already pulled; WPP would be needed for cohort projections, not for verification. |
| DHS Program (`dhsprogram.com`, registration) | **SKIPPED** — and note the Philippines `CR.3` 2013/2017 values come *from* DHS via UIS, so the DHS route would only re-derive them. |
| Atlas-bridge / GitHub | **Not touched**, per instructions. |

## 8. Reproducibility notes

- Every raw response is byte-identical to what the API/site returned; SHA-256 and byte counts are in `SOURCES.json`.
- The UIS zip is the release artifact, so `SDG_DATA_NATIONAL.csv` inside it can be re-filtered exactly (the filter is a country set plus a 30-code include list; the code list is printed in `DATA_LEDGER.md` §B).
- pypdf and openpyxl were installed to `/tmp/pdflibs` and `/tmp/xlsxl` only; nothing was installed into the workspace or system Python.
- Time-boxing: total wall clock ≈ 35 minutes. Depth was traded for verifiability: one claim fully resolved (Cambodia 6.6%), one claim corrected upward (Philippines 2022/2024 completion), one claim narrowed to its primary provenance with caveat (HK 85%), one claim contradicted (HKDSE "norm-referenced"), and two claims left unresolved with a named blocker (Philippine attrition; Bray & Lykins book).

## 9. Second wave (2026-11-20 12:39–12:58 HKT): 1980–2020 six-country enrolment panel with imputation

Requested by the Lead after the first report: Cambodia, Japan, Hong Kong, Philippines, China, Korea; UIS enrolment at various levels 1980–2020; impute missing data.

| Attempt | Result |
|---|---|
| `https://api.uis.unesco.org/api/public/education/indicators` | **HTTP 404** — UIS API needs a subscription key; `/api/public/...` is not an open route. API-key route abandoned; bulk archives used instead. |
| `https://databrowser.uis.unesco.org/api/indicators` | **HTTP 404** — browser backend not an open API. |
| `https://uis.unesco.org/en/bulk-data` (old bulk page) | HTTP 200 but no links to a full education dataset; current bulk page lists only SDG, OPRI, DEM (current release) plus six archive zips. |
| Probes for a full UIS education archive: `bdds/{201907,201807,201706,201512,202001}/{EDU,UIS-EDU,UISEDU}.zip`, `bdds/202611/EDU.zip`, `bdds/archive/EDU.zip` | All **HTTP 404**. The "core" UIS education indicators (GER by level) are not in any free bulk file. |
| `https://download.uis.unesco.org/bdds/archive/EDUNONCORE-FEB2020.zip` | **HTTP 200, 15,880,513 bytes** → used. Feb-2020 UIS archive of historical *non-core* education indicators (net enrolment rates, gross intake ratios, PTR, over/under-age). Filtered to the six countries → `data/uis_edunoncore_6countries_long.csv` (1,417 values, 67 series). Japan is almost absent from it (only PTR 2013–2018). |
| 21 WDI indicators pulled for `KHM;JPN;HKG;PHL;CHN;KOR`, 1970–2024 (`raw/worldbank6/`) | **HTTP 200 each**. Discovery: WDI's Japan level enrolment *ratios* exist only for 2013–2023, and Korea's only for 2000–2024 (no pre-2000 Korea ratios at all); Japan/Korea enrolment *headcounts* run 1971–2023 and were added. Korea's 1980–1999 coverage therefore rests on UIS **net** enrolment rates (EDUNONCORE, 1971–2017), not gross ratios. |
| `https://api.uis.unesco.org/api/public/...` (repeat, for GER.1/GER.2) | Not attempted again — the missing level ratios are core indicators; recorded as an API-key request. |
| UNdata (`http://data.un.org/Data.aspx?d=UNESCO&f=series%3AGER_1`) | HTTP 200 filter page, but `Handlers/DownloadHandler.ashx?...&Fmt=csv` returned the HTML homepage, not CSV. **PARTIAL/abandoned**; no UNdata values ingested. |
| `web_fetch` on `data.un.org` | Not used; `curl` sufficed for the probe. |
| UIS SDG4 re-extraction for JPN/KOR (`raw/uis/SDG_202611.zip` → `raw/uis/x/`) | OK. Found: Japan has **no** `CR.1/2/3` but good `GER.5T8` (1971–2024), `PTRHC.1` (1971–2024), `ROFST.1.CP` (1971–2024); Korea has `CR.2/CR.3` (2000–2023), `GER.5T8` (2000–2024), `ROFST.*` (2000–2024), `PTRHC.*` (1971–2024). |

**Consequence.** A three-layer harmonisation was built (UIS SDG4 > UIS EDUNONCORE > WDI/UIS-derived) and gaps were imputed under written rules: linear (2–8-year gaps), log-linear (9–15-year gaps), no extrapolation, gaps >15 years left empty, structural breaks flagged. Result: 7,011 skeleton cells, 53.6% observed, 12.5% imputed, 1.3% long-gap, 32.5% no anchor. Full audit in `IMPUTATION_METHOD.md`; conflicts between layers (18 cells) in `data/gmr_source_disagreements.csv`.

**Still blocked for this request:** Japan primary/secondary GER and NER 1980–2012 (needs UIS API key for core indicators, or Japan's e-Stat/MEXT tables); Korea level enrolment ratios 2001–2020 (same); any pre-1980 UIS series (the 2026-11 SDG release and the Feb-2020 archive both stop around 1970). Extractions of the 87 MB SDG national file and the 96 MB EDUNONCORE CSV were deleted after filtering to keep the iCloud workspace small; the zips remain and re-extraction is documented in `IMPUTATION_METHOD.md`.

## 10. GMR country-page snapshots (2026-11-20 12:52–13:05 HKT)

Request: "some snapshots of the country pages in GMR's across this time period. samples". Deliverable: `gmr_snapshots/`, ledger `gmr_snapshots/GMR_SNAPSHOTS.md`.

| Attempt | Result |
|---|---|
| `http://efareport.unesco.org/` and `www.` variant | **HTTP 000** — GMR legacy site is dead; only Wayback captures exist. |
| Wayback availability for `efareport.unesco.org` | OK (closest capture 2021-04-10), but the 2004 capture is a JavaScript redirect stub with no content. |
| Wayback CDX for `efareport.unesco.org` with domain match / filters | **HTTP 504 gateway timeouts**; prefix queries mostly empty. Legacy GMR site structure therefore not enumerable in reasonable time. |
| `https://unesdoc.unesco.org/...` (home, image PDFs, `/rest/search`, `/search`) | **HTTP 403 on every path**, with and without browser User-Agent. The country-profile PDFs cannot be fetched directly. |
| Wayback for a known unesdoc profile PDF (`images/0014/001472/147226e.pdf`) | **HTTP 200, application/pdf** at timestamps before ~2019 (the 2020+ capture is an HTML redirect). Confirms the Wayback route. |
| Wayback CDX listing of the directory `unesdoc.unesco.org/images/0014/001472/*` | **HTTP 200**, 246 entries. Enumerated all captured `NNNNNNe.pdf` IDs, fetched them, extracted page 1 and kept documents containing "Country profile … Global Monitoring Report". **28 GMR 2007 country profiles found**, including Philippines (CP/70) and Republic of Korea (CP/42). Qatar (CP/71) and Singapore (CP/75) kept as format exemplars. |
| `www.unesco.org/education/gmr2007/` via Wayback | HTTP 404. `gmr2008`–`gmr2015` microsite CDX listings were fetched: gmr2009 contains only **regional** factsheets (Arab States, CEE/CA, …), no country pages; gmr2008/2010/2011/2012/2015 listings contain no country-profile links. |
| GEM Report country member pages, `gem-report-2017.unesco.org/en/members/<country>/` (live and Wayback) | **HTTP 404 / no capture** at the tested paths. Not sampled. |
| GEM fact-sheet pattern `en.unesco.org/gem-report/sites/gem-report/files/<Country>_fact_sheet.pdf` | Live host returns a 1.78 MB SPA 404 for all six countries; the single known archived example (`Jordan_fact_sheet.pdf`) was used to confirm the family exists, but the naming is not uniform. |
| `https://www.education-inequalities.org/countries/<slug>` (WIDE, the GMR team's equity database) | **HTTP 200** for all six countries. Pages are Next.js/RSC; indicator values are embedded in the payload. Captured raw HTML + extracted text/indicator lists for all six. Slugs: cambodia, china, japan, hong-kong-china, philippines, rep-of-korea (korea-rep and republic-of-korea are 404). |

**Outcome.** 4 GMR-2007 country-profile PDFs + 6 WIDE country pages + 1 index captured, hashed and logged. Gaps recorded rather than guessed: unesdoc blocked (so the sample is 2 of 6 countries for the 2007 profiles), Cambodia/China/Japan profiles not in the archived batch, later editions not sampled, no pre-2002 country pages exist for this series.

## 11. Iteration-2 target sets (2026-11-20 13:05–13:30 HKT)

Task-11: build `TARGETS_SHADOW.csv`, `TARGETS_FLOW.csv`, `ECONOMY_SERIES.csv`, `TARGETS_README.md`.

| Attempt | Result |
|---|---|
| 23 WDI indicator pulls for PHL;KHM;HKG;CHN;KOR;JPN, 1991–2024 (`raw/worldbank_economy/`) + per-indicator metadata for definitions | HTTP 200 each (one transient HTTP 000 on `SL.EMP.TOTL.SP.ZS`, retried OK). Used for GDP p.c., urbanisation, remittances, sector/status employment, unemployment/NEET/LFPR, population. |
| WDI indicator *catalogue* (`per_page=25000`) | **Truncated at 25,000 entries ending at `SE.TER.TCHR.…`** — the `SL.*` labour codes are beyond the first page, so status-employment definitions were fetched per indicator instead. Noted because it silently limits catalogue-based lookups. |
| KEDI/MODS Korea private-education press release (`mods.go.kr`, 2023 survey) | HTTP 200 but the page body is navigation only (content in an attachment); participation rates not extractable. Korea tutoring remains **unresolved**. |
| DMW/POEA overseas deployment | **Not retrieved.** PSA remains HTTP 403; DMW pages not machine-readable in this pass. Recorded as unresolved rows in `ECONOMY_SERIES.csv`; remittances are the only migration-side series included. |
| Tutoring participation, all countries except Hong Kong | **No verified survey retrieved.** CFPS/CEPS, KEDI, APIS/FIES, Brehm & Silova (2014) tables not accessible here. Recorded as unresolved rows with the blocker named. |
| Transition / repetition / dropout / wage premium | **Not available** in UIS SDG4 bulk or WDI; UIS core education indicators are API-key only. Unresolved rows. |

**Outcome:** 747 flow rows (540 target, 172 check, 35 unresolved), 13 shadow rows (7 HK student-participation targets covering 1996 and 2010 stage-by-stage; 1 HK parent-level check; 5 unresolved country placeholders for PHL, KHM, CHN, KOR, JPN), 4,031 economy rows. Matrix and the "calibratable vs check vs unusable" split in `TARGETS_README.md`.

## 12. Shadow-education gap closure (task-16, 2026-11-20 13:15–13:45 HKT)

| Attempt | Result |
|---|---|
| Korea MODS/KEDI 2023 press release (`mods.go.kr` board page) | HTTP 200 but body is navigation only; found the attachment endpoint `boardDownload.es?bid=11758&list_no=430448&seq=2` → **HTTP 200, 1,358,684-byte PDF**, English release with tables. **Used.** |
| KEDI 2011 "90%" release | **Not retrieved.** KEDI site not queried directly (Korean-only pages, no stable English release); Wayback closest KEDI capture is 2026. The 2011 figure therefore remains an untraced assumption; 2023 = 78.5% is the traceable anchor. |
| Japan MEXT (`mext.go.jp`) | **HTTP 000** (DNS-level failure, same class as nis.gov.kh). WayBack not attempted for the expenditure survey PDFs; e-Stat (`e-stat.go.jp`) HTTP 200 but API needs an application ID. **Japan fee series unresolved.** |
| Rappleye & Komatsu (2020) EPAA | HTTP 200, 623,299-byte PDF, open access. **Used** for the grade-6 prefecture table (mean 41.8%, range 22.1–57.9) and the OECD/MEXT 2007 national figures. |
| Bray & Kwok (2003) HKU-hosted PDF | HTTP 200, 103,885-byte PDF. **Used** for HK 1998/99 participation by stage (35.1/46.6/70.3/48.8), provider mix (mass-lecture 72.4%/33.0%), fees and duration. |
| Brehm & Silova (2013 WP39, 2014 JERO) | Author site `willbrehm.com` HTTP 200 for both PDFs. **Used** for the Cambodia case study (one district, 6 schools, 444 students). `pedocs.de` frontdoor returned HTTP 000 (DNS) — author mirror used instead. |
| China: Liu & Bray (2020) | `eric.ed.gov` HTTP 200; **abstract** carries the 2014 national rate (29.8%). Underlying survey table not retrieved. |
| China: post-2021 | `jyb.cn` article HTTP 200 but body JavaScript-rendered; **only the headline** ("超八成受访学生未参加校外学科培训", >80% not attending) recovered. Confidence low. |
| Philippines | PSA HTTP 403 (all paths); `data.gov.ph` Angular SPA, no CKAN API; PIDS search JS-only; World Bank microdata catalog reachable but studies credentialed. **Nothing retrieved; recorded as blocked, not guessed.** |
| CFPS/CEPS microdata | **Access request not made** (needs registration + application). Recorded in SHADOW_DATA.md as the route if the loop wants China microdata. |

**Outcome:** 38 incidence rows and 20 fee rows in `shadow_round2/data/`; three country rows upgraded to high confidence (Korea participation/hours, Japan grade-6 prefecture attendance), four to medium, four Cambodian cells to medium-low with case-study scope stated; HK 2003 anchor added; Philippines remains blocked and the Korean 2011 figure remains untraced.
