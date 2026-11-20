# SHADOW_DATA — round 2: closing (as far as the free sources allow) the shadow-education gap

Owner: `data-hunter` (task-16). Written 2026-11-20. Directory: `04_data/shadow_round2/`. **No value here is imputed or modelled.** Every row is an observation from a retrievable source; every gap is recorded as a gap with the blocker named. The incidence table (`data/shadow_incidence_round2.csv`, 38 rows) and the fee table (`data/shadow_fees_round2.csv`, 20 rows) carry source, table/page, year, denominator, scope and confidence per row.

## Verdict against the previous matrix

The iteration-2 matrix said shadow calibration was possible only for Hong Kong. After this round:

| Country | Previous status | Now | What changed |
|---|---|---|---|
| Rep. of Korea | unresolved | **HIGH — official, traceable** | MODS/KEDI *Private Education Expenditures Survey 2023*, English press release PDF, Table 2 and Summary: participation by school level, hours, monthly expenditure, provider-type spend |
| Japan | unresolved | **HIGH for grade 6 prefecture data; MEDIUM for 2007 national** | Rappleye & Komatsu (2020), *EPAA* 28(67): prefecture-level juku attendance from the national achievement test, mean 41.8%, range 22.1–57.9%; plus OECD/MEXT 2007 national figures |
| China | unresolved | **MEDIUM (2014) + LOW (post-2021)** | Liu & Bray (2020) national survey statistic 29.8% (2014); 中国教育报 (Mar 2022) post-Double-Reduction headline (>80% not attending off-campus academic tutoring → participation <20%) |
| Cambodia | unresolved | **MEDIUM-LOW — case study only** | Brehm & Silova (2013 WP39; 2014 JERO 6(1)): grade-6 urban 60.5% / rural 26.4%; grade-9 Khmer 52% / 39%; **explicitly one district, six schools — not national** |
| Hong Kong | LOW (1996/2010 surveys) | **LOW for those, plus a new MEDIUM-HIGH 2003 anchor** | Bray & Kwok (2003) school survey: S1–3 35.1%, S4–5 46.6%, S6–7 70.3%, all 48.8%; provider split and fees |
| Philippines | unresolved | **still unresolved — blocked** | PSA HTTP 403 on every path; data.gov.ph is an Angular SPA without a CKAN API; PIDS search is JS-only; no APIS/FIES/LFS tutoring item retrieved |

**Upgraded to high confidence (3):** Korea participation (all three levels + overall), Korea hours, Japan grade-6 juku attendance (mean + prefecture range).
**Upgraded to medium (4):** Japan 2007 national juku rates (primary 26%, lower secondary 53%), Japan grade 1–4 math-juku rate (15.0%), China 2014 national rate (29.8%), Korea provider-type expenditure mix.
**Upgraded to medium-low, must stay labelled as a case study (4):** Cambodia grade-6 urban/rural, grade-9 Khmer urban/rural.
**New medium-high (4):** Hong Kong 2003 S1–3/S4–5/S6–7/all.
**Remains assumption / unresolved:** the Korean 2011 "90%" figure (not traceable in this pass — the 2023 official is 78.5%; KEDI's 2011 release would need the KEDI site or KOSIS table, not retrieved); the Philippine rate; all Japanese and Chinese fee series; Hong Kong 1996/2010 survey values remain low-confidence as the source itself warns.

## 1. Korea — official tables, not press snippets

Source of record: **Ministry of Data and Statistics (MODS) / KEDI, "Private Education Expenditures Survey of Elementary, Middle and High School Students in 2023", English press release, released 2024-03-14**, downloaded as a 21-page PDF (1,358,684 bytes) from the MODS board attachment. Raw: `raw/kor_mods_seq2.bin`; text: `raw/korea_mods_2023_private_edu_survey.txt`. Source URL: `https://mods.go.kr/boardDownload.es?bid=11758&list_no=430448&seq=2`.

| Indicator (2023) | Elementary | Middle | High | All |
|---|---|---|---|---|
| Participation rate (%) — Table 2 | 86.0 | 75.4 | 66.4 | 78.5 |
| Participation hours per week — Table 2 | 7.5 | 7.4 | 6.7 | 7.3 |
| Monthly expenditure per student (1,000 won) | 398 | 449 | 491 | 434 |
| Monthly expenditure per *participating* student (1,000 won) | 462 | 596 | 740 | 553 |

Provider mix — as **expenditure** by private-education type, general subjects, per student per month, 2023 (Table 9): private academic institutes (hagwon) **241** thousand won; one-to-one tutoring **37**; group tutoring **22**; internet & correspondence **16**; textbooks with tutor's visit **11** (2022: 24.1/3.9/2.3/1.1 thousand — see table). Same table gives the 2023 artistic/physical split (institutes 10.5, one-to-one 8.3). Total spend 27.1 trillion won, +4.5% on 2022. Purposes of general-subject tutoring: makeup for classes 49.6%, study in advance 24.0%, preparation for higher school level 14.2%. Income gradient: 183 thousand won/month per student in households under 3m won, 671 thousand won in households at 8m won or more.

**Confidence: high** (official national survey, English release of the Korean official tables). The press release gives 2022→2023 changes but not the long series; **the 2011 = 90% claim cannot be traced to a table in this pass** and must remain an assumption or be dropped.

## 2. Japan — prefecture table, peer-reviewed

Source: **Rappleye, J. & Komatsu, H. (2020), "Is shadow education the driver of East Asia's high performance on comparative learning assessments?", Education Policy Analysis Archives 28(67)**, DOI 10.14507/epaa.28.4990, open access, 25 pp. Raw: `raw/rappleye_komatsu_epaa.pdf`; text: `raw/rappleye_komatsu_epaa.txt`.

- **Grade 6 juku attendance, 2018, mean across all prefectures: 41.8%**; prefecture range **22.1% (Akita) to 57.9% (Tokyo)** — their Table 2, built from the national achievement test (NIES) prefecture data. This is the table that the "41.8% prefecture-mean" needed. Note two things: it is a *mean of prefecture rates*, not a student-weighted national mean; and the authors' own finding is that juku attendance is **negatively** correlated with achievement across prefectures (r = −0.16, CI −0.44 to 0.16).
- Trend citations: **OECD (2012), *Lessons from PISA for Japan*, p.72** (cited at p.4 of the article): primary juku participation **16% (1985) → 26% (2007)**; lower secondary **44% → 53%**. Confidence medium (secondary citation of MEXT data).
- Grade/subject: mean share of **grades 1–4 taking math juku lessons 15.0%**, science 0.9% (from MEXT 2008) — confidence medium.
- Figure 1 in the article plots juku attendance by grade for 1976, 1985, 1993, 2007 (grades 1–9) and 2012 (grades 10–12), sourced to MEXT (2008) and NHK Broadcasting Culture Research Institute (2013). The series are **graphical only** — no numeric table, so they are not transcribed here.

**Japan fee series: unresolved.** The right sources are MEXT's 子供の学習費調査 (household education expenditure) and the Statistics Bureau's 家計調査 (family income and expenditure, which has a 学習塾費 line). `mext.go.jp` did not resolve from this environment (HTTP 000, DNS-level) and `e-stat.go.jp` requires an application ID for its API. No Japanese fee number is asserted.

## 3. China — one national rate, one post-policy marker

- **Pre-Double Reduction:** Liu, J. & Bray, M. (2020), "Evolving micro-level processes of demand for private supplementary tutoring", *Educational Studies* 46(2):170–187 — ERIC abstract EJ1245506 states: "National survey data indicate that **29.8% of primary and lower secondary students had received private supplementary tutoring in 2014**, with proportions rising at higher levels of the school system." Confidence **medium**: the rate is quoted in a peer-reviewed abstract, but the underlying survey table was not retrieved.
- **Post-2021:** 中国教育报 (China Education Daily), 2022-03-03, headline "超八成受访学生未参加校外学科培训" — "over 80% of surveyed students did not attend off-campus subject tutoring", i.e. **participation below 20%** in the post-Double-Reduction monitoring survey. Confidence **low**: newspaper report; survey name, sample and question wording are not stated in the page retrieved (the body is JavaScript-rendered; only the headline is machine-readable).
- **Microdata access request (recorded, not made):** CFPS (China Family Panel Studies, Peking University) and CEPS (China Education Panel Survey, Renmin University) require registration and an application for the restricted-use files. The 2014 national figure above is the best citable alternative until such access is granted.
- China fee series: unresolved.

## 4. Philippines — blocked, exactly as follows

| Route | Result |
|---|---|
| `https://psa.gov.ph/statistics/labor-force-survey` and `/statistical-tables` | **HTTP 403** (bot protection) |
| `https://psa.gov.ph/` (any path tried) | 403 |
| `https://www.data.gov.ph/` / `https://data.gov.ph/` | Angular single-page app (7.3 KB shell); `data.gov.ph/api/3/action/package_search` returns the same HTML shell, **no CKAN API** |
| `https://www.pids.gov.ph/publications?search=tutoring` | HTTP 200 but results are JavaScript-rendered; no tutoring study surfaced |
| World Bank microdata catalog `microdata.worldbank.org/index.php/catalog` | HTTP 200 (catalog reachable), but the FIES/APIS/LFS studies are credentialed downloads; **not requested in this pass** |
| ADB / PIDS alternatives | not attempted after the above |

The Philippine incidence row therefore stays `status=unresolved`. APIS does not have a tutoring module in its public documentation; FIES has education-expenditure items at household level but the microdata are credentialed. **What would close it:** a PSA microdata request for FIES/APIS, or PIDS's own household-survey work, or the DepEd "Basic Education Exit Assessment"/BESRA documentation if it contains a tutoring item.

## 5. Cambodia — case study, scope stated

Sources: **Brehm, W. C. & Silova, I. (2013), "Hidden Privatization of Public Education in Cambodia" (Education Support Program working paper 39)** — `raw/brehm_silova_wp39_2013.pdf`/`.txt`; and **Brehm & Silova (2014), JERO 6(1):94–116** — `raw/brehm_silova_jero_2014.pdf`/`.txt`.

- **Scope:** one district; **six schools** (three urban, three rural); **444 students tracked** (162 in grade 6, 282 in grade 9); 28 classroom observations; focus groups. This is a purposive case study selected to span the district's private-tutoring price range, **not a national survey**. It must never be quoted as a Cambodia-wide rate.
- **Incidence:** grade 6 **60.5% urban vs 26.4% rural**; grade 9 Khmer-language tutoring **52% urban vs 39% rural** after excluding NGO-supported students (chemistry tutoring was entirely NGO-funded).
- **Provider:** the dominant form is **Rien Kuo — government school teachers teaching their own students in government school buildings**, a paid continuation of the public curriculum. This is the Cambodian provider-mix fact for the model: not commercial centres but the state's own teachers, inside the state's own buildings.
- **Fees:** district lower-secondary range **500–1,000 Riel per session (≈US$0.13–0.25)**, corresponding to rural and urban schools; WP39 also gives an hourly range of **300–1,000 Riel (US$0.08–0.25)**. Students attend a public-school shift plus one to four hours of tutoring.
- **Context:** two-shift schooling covered ~81% of primary and ~41% of lower-secondary schools in 2005 (Benveniste et al., cited in the JERO article).

## 6. Hong Kong — the new 2003 anchor, provider mix and fees

Source: **Bray, M. & Kwok, P. (2003), "Demand for private supplementary tutoring: conceptual considerations, and socio-economic patterns in Hong Kong", Economics of Education Review 22:611–620**, 12-page PDF from HKU — `raw/bray_kwok_2003_hk.pdf`/`.txt`. Survey of 630 secondary pupils in six schools, one randomly selected class per level group, 1998/99.

| Stage | Participation (%) — Table 1 |
|---|---|
| Secondary 1–3 | 35.1 |
| Secondary 4–5 | 46.6 |
| Secondary 6–7 | 70.3 |
| All | 48.8 |

- **Provider mix (the loop's new structural variable):** the largest share attends **large-scale, examination-oriented mass-lecture commercial classes** — **72.4% of S6–7 pupils** and **33.0% of S4–5 pupils** received this type (not mutually exclusive); 12.3% (S1–3), 29.4% (S4–5) and 19.8% (S6–7) used **more than one tutoring type**. The paper also distinguishes one-to-one, small-group, large-class and company-run provision qualitatively; HK providers range from individuals working informally to multi-branch companies.
- **Fees:** **28.1%** of tutored pupils spent **over HK$1,000 per month** on fees and **8.5% over HK$2,000**; one third spent under HK$500; fees consumed **1.1–5.0% of monthly household income**. Modal duration **6–10 hours per month**; 30.4% over 10 hours and 6.5% over 25 hours.
- **Motives:** examination preparation dominates at the top (84.5% of S6–7 tutored pupils) vs 28.8% in S1–3, while "seeking guidance with homework" dominates lower down (60.3% in S1–3) — directly relevant to the model's why-buy distinction.
- The 1996 and 2010 stage rates (Kwo & Bray 2011) stay in the table as **low confidence**: the reporting authors state "Neither of these surveys should be considered statistically robust". The 2010 senior-secondary 85% is therefore not a substitute for the 2003 survey anchor; they measure different stages and both are weak in different ways.

## 7. Cross-country provider-mix summary (what the model can actually use)

| Country | Dominant provider form | Evidence |
|---|---|---|
| Rep. of Korea | Commercial hagwon dominant in **spend**: 241 of 434 thousand won/month per student, vs 37 one-to-one, 22 group, 16 internet | MODS/KEDI 2023 Table 9 |
| Hong Kong | Commercial mass-lecture chains dominant at senior secondary (72.4% of S6–7), individual/small-group common lower down | Bray & Kwok 2003 |
| Japan | Commercial juku dominant (home tutoring and remote tutoring are small in the figure, no numeric table) | Rappleye & Komatsu 2020, Figure 1 |
| Cambodia | **Government school teachers** selling the curriculum back in school buildings (Rien Kuo) | Brehm & Silova 2013/2014 |
| China | Commercial institutes before 2021; post-2021 subject tutoring pushed off-campus/informal — no provider split retrieved | Liu & Bray 2020; China Education Daily 2022 |
| Philippines | none retrieved | blocked |

## 8. Confidence rules for the loop

1. Use Korea, Japan (grade-6 mean/range), and HK-2003 as the **calibration** anchors. Use China-2014 and Cambodia as **bounds or priors**, not point targets.
2. Never quote the Cambodian case-study rates as national; never use the HK 1996/2010 rates without their "not statistically robust" caveat; never use the Chinese post-2021 newspaper figure as a rate — it is an inequality ("more than 80% did not attend"), not a point estimate.
3. Fee moments exist for Korea (rich), Hong Kong (2003), Cambodia (case study). They do **not** exist for Japan, China or the Philippines in this round.
4. The Korean 2011 = 90% figure is **not traceable** in this round. If the loop needs a Korean time path, the target must be 2023 = 78.5% plus whatever KEDI history can be obtained from KOSIS.

## 9. Files and provenance

```
shadow_round2/
  SHADOW_DATA.md                      this file
  data/shadow_incidence_round2.csv    38 rows; 17 columns; statuses incidence / provider_mix / hours / check / unresolved
  data/shadow_fees_round2.csv         20 rows; fees and expenditure moments by stage/provider/income
  raw/kor_mods_seq2.bin               Korea MODS/KEDI 2023 press release PDF (1,358,684 bytes)
  raw/korea_mods_2023_private_edu_survey.txt
  raw/rappleye_komatsu_epaa.pdf / .txt
  raw/bray_kwok_2003_hk.pdf / .txt
  raw/brehm_silova_wp39_2013.pdf / .txt
  raw/brehm_silova_jero_2014.pdf / .txt
  raw/china_jyb_2022_03_03.html
  raw/pedocs_frontdoor.html, eric_china.html, pids_search.html   (probe/blocker evidence)
```

All raw files are hashed in `SOURCES.json` (ids prefixed `shadow2_`). Retrieval attempts and exact blockers are in `retrieval_log.md` §12.
