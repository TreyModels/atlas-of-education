# Cambodia (KHM) facts for cohort-model port

Compiled 2026-11-21 via WebSearch/WebFetch. Figures are as read from fetched pages (some via a summarising fetch tool). Anything not found is marked NOT FOUND.

## 1. Grade structure since 1990

- 1979-1987: 10 years (4+3+3); 1987-1994: 11 years (5+3+3); 1994 onward: 12 years (6+3+3). Basic education = grades 1-9. So 6+3+3 holds for the whole period from 1994, and the 1990-1993 period was 5+3+3 (11 years).
  - Source: https://lib.ncdd.gov.kh/storage/app/public/library_backend/CAT_24537_1/2017-EducationReform-cambodia-en.pdf (Cambodian gov't/NCDD library copy of a 2017 education reform paper)
  - Reliability: moderate; secondary summary of ministry history, single source. Confirm the 1994 switch before relying on it for 1990-1994 cohorts.
- WDI (World Bank) lists official primary entry age = 6, primary duration = 6, secondary duration = 6, lower-secondary duration = 3, constant for every year reported (1970-2025; lower secondary through 2020). These do NOT show the 1990-1993 5+3+3 structure.
  - Source: World Bank API, SE.PRM.AGES, SE.PRM.DURS, SE.SEC.DURS, SE.SEC.DURS.LO (see wdi_series.json).
  - Reliability: high for entry age 6; WDI structure series is flat, so likely misses the pre-1994 change.

## 2. Grade 12 national exam (Bac II) pass rates

First-sitting pass rates, % of candidates:

| Year | Pass rate | Notes | Source |
|---|---|---|---|
| 2012 | 86.48 | no candidate count | Bangkok Post |
| 2013 | 86.77 (also reported as 87) | no candidate count | Bangkok Post; NBC |
| 2014 | 25.72 | 23,126 of 89,937 candidates passed (exam Aug 4); after the Oct re-sit the final rate was 40.67; re-sit pass rate 18% of ~60,000 | Bangkok Post; Cambodia Daily; Phnom Penh Post |
| 2015 | 55.87 | 46,560 of 83,341 (Cambodia Daily; exam Aug 24-25); one source gives 55.88 | Cambodia Daily; Cambodianess |
| 2016 | 62.18 | | Cambodianess |
| 2017 | 63.84 | | Cambodianess |
| 2018 | 67.07 | (female 69.38) | Cambodianess; MoEYS Education Congress report 2018-19 |
| 2019 | 68.62 | | Cambodianess |
| 2020 | no exam | cancelled for COVID-19; all students passed automatically | Cambodianess |
| 2021 | 65.65 | | Cambodianess |
| 2022 | 72.33 | | Cambodianess |
| 2023 | 72.89 | | Cambodianess |
| 2024 | 79 | 106,351 passed | Cambodianess |

- 2014 reform: ~10,000 Anti-Corruption Unit-trained monitors; the pass rate fell from ~87% to 25.72%, "the lowest since 1994". Cheating (bribing proctors, buying answer keys) had been common.
- Sources:
  - https://www.bangkokpost.com/world/429454/cambodia-cheating-crackdown-works (2012: 86.48; 2013: 86.77; 2014: 25.72 with counts. Year labels inferred by the fetch tool from "last year" wording)
  - https://www.nbcnews.com/news/asian-america/cambodia-cracks-down-cheating-75-percent-fail-final-exam-n194566 (2013: 87%; 2014: 25.72%; ~90,000 candidates)
  - https://english.cambodiadaily.com/?p=94086 (2015: 55.87%, 46,560/83,341; 2014 final 40.67%; Sept 14, 2015)
  - https://www.cambodianess.com/index.php/article/bac-ii-exam-sets-record-pass-rate (2014-2024 series)
  - https://planipolis.iiep.unesco.org/sites/default/files/ressources/cambodia_education_congress_report_2018-2019_eng.pdf (2017-18: 67.07%)
  - https://opendevelopmentcambodia.net/news/exam-pass-rate-increases/ (Phnom Penh Post, Sept 2017: slight increase, scores "may be plateauing"; the 63% in the page text was only decoded from share-link text, so ignore it in favour of the 63.84 above)
- Reliability: press reports of ministry figures. 2012-2015 are well corroborated across 3+ outlets. 2016-2024 come from a single Cambodianess table except 2018. Several older articles carry no calendar year, so years were inferred. Treat 2012/2013 as approximate (about 86-87). 2011 and earlier: NOT FOUND (an undated Phnom Penh Post piece gives 70.7% "previous year" and ~78% "current year" with 77,178 and 86,610 candidates; year unknown, not used).
- Not used: https://www.phnompenhpost.com/national/national-exam-scores-improve (undated).

## 3. Tertiary enrolment counts and private share

- Totals (Perkin 2006, cited in Hiroshima Univ. Higher Education Forum paper): 1970: 9,228; 1980: 702; 1990: 5,479; 2000: 22,108; 2005: 56,810. Text says UNIS enrolment grew 260% 2000-2005 (MoEYS figures, which include multiple enrolments, show higher growth). Private tertiary enrolment grew 86.5x from 1997 to 2008 vs 4.8x for public; by 2008 almost 90% of enrolments were fee-paying.
  - Source: https://ir.lib.hiroshima-u.ac.jp/37025/files/33695
  - Reliability: moderate; counts are from a secondary compilation, and the public/private-by-year chart (1996-2008) had no extractable numbers.
- 2012/13: just over 255,000 students in higher education degree programmes; about 60% attended private HEIs (note: possible double counting of students enrolled at several HEIs).
  - Source: https://cdri.org.kh/new/wp-content/uploads/2025/02/cdr15-4e-3_1617679788.pdf (CDRI, Cambodia Development Review)
  - Reliability: moderate-good; exact year-split depends on the author's reading of MoEYS data.
- 2017-18: 211,484 students in higher education (+4,050, +1.95% on 2016-17, so 2016-17 is about 207,434); bachelor's 168,242; associate's 19,871; postgraduate 23,371. 48 public and 77 private HEIs (institution counts only). Public/private student split NOT reported in the text read.
  - Source: https://planipolis.iiep.unesco.org/sites/default/files/ressources/cambodia_education_congress_report_2018-2019_eng.pdf (MoEYS Education Congress report 2018-19)
  - Reliability: high (official ministry report), but the 2012/13 total (255k) vs 2017/18 (211k) gap suggests a definitional or double-counting difference between sources; do not splice without checking.
- Gap: private share by year for 2005-2020 NOT FOUND in a usable table. The MoEYS 2016-17 statistical booklet (https://lib.ncdd.gov.kh/storage/app/public/library_backend/CAT_21263_1/2017-EducationStatistics- Indicators2016-2017-en.pdf) has no tertiary data. WDI SE.TER.ENRR (gross ratio) is saved as an alternative.

## 4. Policy events with dates

- 2000: Priority Action Program (PAP) introduced. Registration and other informal fees were abolished in primary and lower secondary schools. School operating-budget grants replaced household charges. PAP also funded summer remedial classes (PAP 2.2).
  - Source: https://planipolis.iiep.unesco.org/sites/default/files/ressources/cambodia_efa_mda.pdf (Cambodia EFA Mid-Decade Assessment)
  - Corroboration: ODI 2010 (Engel), https://cdn.odi.org/media/documents/11563.pdf, says start-of-year fees were abolished in 2000, which led to an enrolment surge, especially in remote areas, but informal fees by teachers persist.
  - Reliability: good (two sources agree on the year).
- 2000-2005 (strategy): cancelled enrolment payments, introduced a school funding formula favouring poor rural schools, built primary schools nationwide. 2006-2010 (strategy): lower secondary schools in all communes, secondary schools in all districts, scholarships for poor students to complete grade 9. 2009-2013: focus on reducing repetition and dropout. 2014-2018: equity, quality.
  - Source: https://lib.ncdd.gov.kh/storage/app/public/library_backend/CAT_24537_1/2017-EducationReform-cambodia-en.pdf
  - Reliability: moderate (summary; no project-level dates).
- 2001-2005 / 2004-2008 / 2006-2010: Education Strategic Plans (ESP). 2003: EFA National Plan 2003-2015 (adopted June 2003; 9 years free basic education). 2006: Fast Track Initiative status.
  - Source: EFA MDA link above.
- Scholarships: ADB Education Sector Development Program (loans approved 22 Oct 2001; closed 2004/2008). Lower secondary scholarship recipients were 13,938 in 2003-04 rising to 25,872 in 2007-08, funded by PAP 12 (from 2003-04) and the Japan Fund for Poverty Reduction (JFPR). Female share of lower secondary enrolment rose from 30.0% (2000) to 45.6% (2006-07). Transition rate to lower secondary: 77.3% (2000-01), 81.9% (2004-05), 78.7% (2006-07). Survival grades 1-6: 45.0% (1999) to 52.5% (2006-07). Net enrolment 2007-08: 93.3% primary, 34.8% lower secondary.
  - Source: https://www.adb.org/sites/default/files/project-documents//33396-cam-pcr.pdf (ADB project completion report)
  - Reliability: high (official donor evaluation).
- 2013: school financing formula revised to weight small and disadvantaged schools. 2015: new legislation on primary and secondary scholarships (US$9.4 million allocated in 2016; coverage still limited). Education budget: recurrent share 18.2% of the national budget in 2016. Primary education is not compulsory.
  - Source: https://www.allinschool.org/media/3456/file/Country-Study-Cambodia-2016.pdf (UNICEF/MoEYS/UIS Out-of-School Children study, 2016)
  - Reliability: good.
- 2014: anti-cheating exam reform (see section 2). 2015: teacher salary rises (primary US$124.46/month, lower secondary US$186.62) with a planned rise to US$250 (2017 reform doc above). 6 Nov 2018: inter-ministerial Prakas (No. 1245) giving scholarships to poor students in grades 1-3 (Education Congress report 2018-19, link in section 3). 2017 budget proposal: US$9 million for new schools.
- Free-tuition measures at tertiary level: NOT FOUND in the sources read (the CDRI paper notes only fee-paying programmes in public HEIs since the 1990s, and about 90% of enrolments were fee-paying by 2008; the ESP 2014-18 aimed to increase scholarships for poor students).
- School construction: no exact counts or dates found beyond the strategy statements above (ODI 2010 says only that school numbers "greatly expanded").

## 5. Household survey evidence by wealth quintile

- CSES 2012 (Cambodia Socio-Economic Survey), Q1 = poorest, Q5 = richest, from the out-of-school study authors' calculations:
  - Out of school, ages 6-11: Q1 20.1%, Q5 5.6%. Ages 12-14: Q1 24.2%, Q5 3.2%.
  - Adjusted net attendance, ages 6-11: Q1 79.9%, Q5 94.4% (net attendance 79.2% vs 92.9%).
  - Lower secondary net attendance, ages 12-14: Q1 17.3%, Q5 57.6%. Any schooling, ages 12-14: Q1 75.8%, Q5 96.8%.
  - Pre-primary (age 5): Q1 10.2% vs Q5 16.7%.
  - More than half of children in the poorest quintile have left school by age 16.
  - Source: https://www.allinschool.org/media/3456/file/Country-Study-Cambodia-2016.pdf (the extract was truncated after 100,000 characters, so later tables were not read).
  - Reliability: good (UNICEF/MoEYS/UIS, CSES microdata), but the table showing Q1 out-of-school counts for 12-14 seems to be duplicated from 6-11 (possible table error in the source).
- Primary enrolment by quintile 1997 and 2004 (ODI 2010 Figure 2): the poorest quintile made faster absolute progress; exact numbers NOT extractable from text. Source: https://cdn.odi.org/media/documents/11563.pdf
- DHS (2014 and 2021-22 reports at https://dhsprogram.com/pubs/pdf/FR312/FR312.pdf and https://dhsprogram.com/pubs/pdf/FR377/FR377.pdf): quintile attendance tables could NOT be read (FR312 fetch failed; FR377 table cut off). Use DHS STATcompiler if needed.

## 6. Private supplementary tutoring and informal fees

- Bray, Kobakhidze, Liu and Zhang (2016), "The Internal Dynamics of Privatised Public Education: Fee-charging Supplementary Tutoring Provided by Teachers in Cambodia," Int. J. Educational Development 49: 291-299. Sample of 1,274 students from six schools in Siem Reap Province (not national; survey year not stated in the text read): 81.9% received tutoring overall; grade 9: 74.7%; grade 12: 89.8%. Male 80.9%, female 82.8%. Urban 83.5% vs 80.9% rural. 45.3% of grade 12 students vs 8.1% of grade 9 students were tutored in more than five subjects. About 52.8% of 72 teachers surveyed gave tutoring. Fees: 500 riel (US$0.13) per lesson or 10,000 riel (US$2.50) per subject per month; average student spending 50,000 riel (US$12.50) per month. Teachers' average tutoring income 596,000 riel (US$166) per month vs official salary 633,000 riel.
  - Source: https://hub.hku.hk/bitstream/10722/225919/1/Content.pdf
  - Reliability: good for the study (peer-reviewed), but regional and small-scale; do not treat as a national rate.
- Marshall and Fukao (2018/19), Comparative Education Review 63(1): 98-120, nationally representative sample of 138 lower secondary schools. Higher-SES students more likely to access and enrol in fee-based extra classes from their own teachers; extra classes linked to higher maths and physics scores. No prevalence figure found in the summary page.
  - Source: https://etico.iiep.unesco.org/en/shadow-education-and-inequality-lower-secondary-schooling-cambodia-understanding-dynamics-private
  - Reliability: good (peer-reviewed); only qualitative findings were extracted.
- UNDP/related report "Curbing Private Tutoring and Informal Fee in Cambodia Basic Education": field study of 2013 (Pak et al.): share of parents paying for tutoring outside normal class time 45%, during school vacation 34%, Thursdays 35%, during class hours 12%. Tutoring is more common in urban and lower secondary schools than primary; most common in grade 9. Informal fee costs: Bray's study (cited as "1999") KHR 50,000-255,000 (US$12.50-64) per child in grade 1 up to KHR 224,000-507,000 (US$56-127) in grade 6, i.e. 5.3-20.4% of family income; NEP 2007: about KHR 443,800 (US$108) per child per year, 8.7% of family income (about US$60 for grades 1-3, US$90 grades 4-6, US$158 grades 7-9). A 2012 small survey of 155 exam takers: 67% had parents paying informal fees during the exam (secondhand).
  - Source: https://files.acquia.undp.org/public/migration/kh/Curbing-Private-Tutoring-and-Informal-Fee-in-Cambodia-Basic-Education.pdf
  - Reliability: moderate; secondary citing, with the source itself showing a date inconsistency (Bray's IIEP report is 1990 per the reference list, labelled 1999 in text) and a typo in one NEP line.
- Informal fees: persist despite the 2000 fee abolition because teacher salaries are low (ODI 2010; Out-of-school study 2016, which also cites extra tuition as a reason children are excluded).
- Other: MoEYS requested permission to pay hourly wages to teachers giving extra tuition to grade 12 students (Education Congress report 2018-19; approval not confirmed).
- Not found: national prevalence by grade from World Bank or Dawson; additional Bray figures.
