<!-- Iteration 2 country card. Compiler: lit-archivist, 2026-11-20.
Every number below carries its source and access status. "NOT FOUND" means I looked and did not
find a citable figure - it does not mean the phenomenon is absent. "NOT VERIFIED" means a figure
exists in a source I could not retrieve this session. Do not promote a NOT VERIFIED figure to a
calibration target without reading the original. -->

# PHL - Philippines (country card)

**Headline for the model: participation is moderate and *gate-specific* - the money is at the college-entrance review centre, not the primary tutor.**

## 1. Shadow education

| Measure | Value | Year / survey | Source (access) | Denominator |
|---|---|---|---|---|
| Basic-education students availing >=1 shadow-education service | **46.5%** (574 / 1,235) | 2010 survey | de Castro & de Guzman, *Push and pull factors affecting Filipino students' Shadow Education participation*, KEDI Journal of Educational Policy 7(1): 43-66, Table 2 (FULL-TEXT, `raw/decastro_deguzman2010_kjep_philippines.pdf`) | 1,235 usable respondents (88.2% of fielded) |
| Elementary students using private tutors / tutorial centres | **23.8%** of 425 | same | de Castro & de Guzman 2010, Table 2 (FULL-TEXT) | elementary subsample 425 |
| Secondary students using **review centres** ahead of college entrance exams | **28.1%** of 810 | same | de Castro & de Guzman 2010, Table 2 (FULL-TEXT) | secondary subsample 810 |
| Learning-centre use, elementary vs secondary | **13.4%** of 425 vs **7.3%** of 810 | same | de Castro & de Guzman 2010 (FULL-TEXT) | by level |
| Participation range across grouped comparisons | **42.0-49.9%** | same | de Castro & de Guzman 2010 (FULL-TEXT) | grouped subsamples |
| Male students using a private tutor | **20.6%** of 626 | same | de Castro & de Guzman 2010 (FULL-TEXT) | male subsample |

**Access caveat, stated by the authors and repeated here because it governs use:** the instrument was **researcher-made** (Cronbach alpha 93.5%), the sample is a **select group** of 1,235 students (65.6% of them 4th-year high school), and the paper presents itself as "preliminary data". This is the **only** Philippines shadow-education survey I could retrieve. It is *not* nationally representative.

**NOT FOUND / NOT VERIFIED:** any nationally representative PH tutoring take-up rate (PSA APIS/FIES do not field a tutoring module that I could locate); any post-2013 (K-12) tutoring survey; income-quintile breakdown of tutoring take-up; hours; spending.
**Consequence for the model: PHL is data-thin at every stage except a single 2010 gate-specific survey.** Treat the 46.5% as a *medium-confidence* target and the provider split as the more useful signal.

## 2. Gates
- **College entrance**: historically the NCEE, then institution-specific/CHED-regulated tests; the survey's own framing is "review centres preparatory to college entrance examinations". Exact instrument history: **NOT VERIFIED** this session.
- **K-12 / Senior High School gate (2013, RA 10533)** raised the completion credential by two years; the October paper's whole case rests on this (see MANUSCRIPT_COMPARISON).
- **Civil service qualification standards**: CSC Resolution 2500229 (March 2025) reportedly made JHS completers eligible for posts formerly requiring the pre-2016 diploma - **NOT VERIFIED** (primary issuance not retrieved).
- **Licensure**: PRC board exams (nurses, engineers, etc.) - pass rates **NOT FOUND** this session.
- **Migration**: professional registration recognition; POEA/agency channel for the majority in elementary occupations.

## 3. Cohort flows
- Completion gradient: high-school completion ~40% among the poorest third vs 70-75% for non-poor (late-1990s surveys, Filmer & Pritchett 1999 / Manasan) - **NOT VERIFIED** (unresolved in `CLAIM_REGISTER.csv` O-25).
- Attrition cited in the 2012 Senate debate: of 100 children entering Grade 1, **43** finish high school and **14** finish college - **NOT VERIFIED** (Philstar reporting, not retrieved).
- Upper-secondary completion 67.0% (2022) / 67.5% (2013 baseline), UIS - **NOT VERIFIED** (unresolved; J-01).
- Tertiary GER 35.9% (2015) -> 28.1% (2018) -> 47.4% (2024), UIS - **NOT VERIFIED** (unresolved; O-29).
- **Every cohort-flow number in the manuscripts is currently unchecked. Do not hard-code any of them as a target.**

## 4. Economy context
- Large informal sector; formal work defined partly by credential - the mechanism the October paper needs.
- Overseas channel: in 2023, **41%** of OFWs in elementary occupations, **64%** among women (PSA SOF) - **NOT VERIFIED**.
- Nurse migration response: **~9 additional nurses licensed per migrant** (Abarcar & Theoharides 2024) - **NOT VERIFIED**, and it is the benchmark the project's own model fails against (0.25).
- Remittances ~$38.3bn, ~8.3% of GDP (2024) - **NOT VERIFIED**.

## 5. Policy timeline
1940 Education Act (grade eliminated) -> 1949+ UNESCO restoration recommendations -> 1953 RA 896 (unfunded) -> 2010 Aquino pledge -> 2012 EO 83 (PQF council) -> **Jan/May 2013 RA 10533** -> 2018 PQF Act. All dates from the October draft's table; **primary documents not retrieved** - check against the Official Gazette before publication.

## 6. Disagreements / unverifiable
- **Who pays for the reform**: the October draft itself concedes the Aquino-mandate reading is a serious rival to the "anticipated reclassification" reading.
- **Is PH tutoring a gate phenomenon or a general-schooling phenomenon?** de Castro & de Guzman's own split (review centres at the college gate; tutors at primary) supports gate-clustering, but one select sample cannot carry it.
- Nothing in the retrieved literature gives a PH income-quintile tutoring gradient. That is the single largest empirical hole for the paper's equity claims.
