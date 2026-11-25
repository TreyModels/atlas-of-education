# Tutoring codebook verification — PISA / SEA-PLM / China surveys (status pass)

**Owner:** `contest-math` (re-tasked by Lead, 2026-11-25; host-only, no box). **Status:** public-documentation
check **only** — no microdata acquired, no restricted files downloaded. **Evidence classes:** **D** = documented
in a public source actually located/read in this pass; **L** = reported in the literature (secondary);
**V** = plausible but still unverified — must be checked in the codebook/dataset before use.

**Network limitation (recorded because it bounds what this pass can claim):** direct retrieval was possible only
for some hosts. Successfully read in this pass: Peking University Open Research Data Platform and CIEFR
(`opendata.pku.edu.cn`, `ciefr.pku.edu.cn`) and Renmin University CSSD/CEPS (`ceps.ruc.edu.cn`, `cssd.ruc.edu.cn`).
OECD, IEA, SEA-PLM, KOSTAT, ERIC, NCES, UNICEF and Springer hosts could not be reached from this environment
(hostname resolution blocked); their rows therefore rest on **indexed public snippets/secondary literature** and
are marked **D(snippet)** or **V**, never asserted as codebook-verified.

## 1. Item-by-item verification

| item | source | claimed content | class | evidence / how verified | still needed |
|---|---|---|---|---|---|
| PISA out-of-school / after-school lessons item exists in several cycles | OECD PISA student questionnaire | participation and hours per week in out-of-school/after-school lessons; used in published analyses | **D(snippet)** | PISA 2018 Results Volume V has a chapter section on after-school lessons ("Learning time during and after school hours: After-school lessons can have different purposes"); PISA 2009 Singapore study analyses "out-of-school lessons"; 2024 *Large-scale Assessments in Education* paper analyses private supplementary tutoring in PISA 2022 | exact item codes and wording per cycle (2018/2022), subject coverage, response categories |
| PISA cycles available | OECD | 2000–2022; item availability varies by cycle | **D(snippet)/V** | PISA cycle list public; item presence evidenced for 2009/2018/2022 as above; earlier cycles **V** | cycle-by-cycle questionnaire check |
| PISA country coverage | OECD | HK (all cycles), PH (2018, 2022), CN (2009/2012 Shanghai; 2015/2018/2022 B-S-J-Z variants), KH not a participant (PISA-D 2017 only) | **D(snippet)/V** | PISA participation lists public; CN variant composition **V** for 2022 | confirm 2022 CN participation and variant composition from OECD participation list |
| PISA ESCS linkage | OECD | standard ESCS socio-economic index available in all cycles; supports quintiles | **D** | standard PISA index, documented in PISA technical report/questionnaires | confirm ESCS construction/derivation in the 2022 codebook |
| PISA expenditure item | OECD PISA questionnaires | **none** (no tutoring cost/expenditure question) | **D(snippet)/V** | PISA student/school questionnaires are not expenditure instruments; no expenditure item surfaced in any located source | confirm in 2022 student/school questionnaire codebooks |
| PISA provider-type item (own teacher vs firm) | OECD PISA questionnaires | **none** | **D(snippet)/V** | same as above; no provider-type item surfaced in located sources | confirm in codebook |
| SEA-PLM 2019 student/parent/school questionnaires published | SEA-PLM/UNICEF | questionnaires + codebook are public documents; 2019 first cycle covers KH, PH (+ Lao, Malaysia, Myanmar, Vietnam) | **D(snippet)** | SEA-PLM 2019 codebook and school questionnaire URLs located; 2019 Main Regional Report public; 2024 questionnaire framework public (shows SEA-PLM item-code style) | access the 2019 student codebook and search for tutoring/extra-lesson items |
| SEA-PLM tutoring item exists | SEA-PLM 2019 | plausible (learning-support/out-of-school-practice content) but **not confirmed** | **V** | no located source names a tutoring/extra-lesson variable in the 2019 codebook | codebook check (highest priority for Cambodia) |
| PISA-D 2017 (KH) out-of-school-lesson item | OECD | limited; item presence unconfirmed | **V** | PISA-D 2017 was administered in Cambodia; questionnaire content not located | PISA-D questionnaire/codebook check |
| CIEFR-HS waves and samples | PKU CIEFR (verified pages) | 2017: 29 provinces, 355 districts, 40,011 households, 21,000 students; 2019: 29/345/34,643 households, 18,000 students; 2021: 29/269/22,027 households, 14,000 students | **D (verified)** | CIEFR release page (fetched) and PKU dataverse description (fetched) | — |
| CIEFR-HS content | PKU CIEFR | household educational **expenditure** (detailed), enrolment choices, government subsidies, kindergarten→higher education; 2017/2019/2021 (+2022 questionnaire); merge with CHFS via `hhid`/`pline` | **D (verified)** | CIEFR release page (fetched) | tutoring-specific question wording: questionnaire PDFs (2021/2022) are on the dataverse but access-restricted; need approved access or public questionnaire mirror |
| CIEFR-HS access route | PKU dataverse | register on `opendata.pku.edu.cn` → apply via `dataverse/ciefrhs`; **institutional email required** (`xxx@xxx.edu.cn`; personal qq/163 rejected); academic use only; no redistribution; approval by review | **D (verified)** | dataverse file page + CIEFR release page (both fetched) | submit application; approval is the gate (not a fee) |
| CIEFR-HS datasets/DOIs | PKU dataverse | 2021 `doi:10.18170/DVN/QOM4FT`; 2019 `doi:10.18170/DVN/YDQJ3D`; 2017 update `doi:10.18170/DVN/B6HK6Y`; original `doi:10.18170/DVN/KE1JYM` | **D (verified)** | dataverse listing (fetched) | — |
| Double Reduction evaluation using CIEFR-HS | CIEFR published analyses | short-term evaluations of the 2021 "双减" policy using CIEFR household survey (+ web-platform data) | **D (verified link)** | CIEFR release page links two such reports | whether the evaluation files/data are obtainable (they are reports, not data) |
| CEPS waves and access | Renmin Univ. CSSD | CEPS is a nationally representative longitudinal survey of junior-high cohorts; **3 data waves published**; platform requires real-name authentication + signed data-use agreement; public data one-click download, restricted data by online application/approval | **D (verified)** | CSSD launch announcement page (fetched); CEPS questionnaire/tech-report pages public | wave list/年份 confirm from CEPS data page; tutoring item wording from CEPS questionnaires |
| CFPS tutoring items | PKU ISSS CFPS | questionnaire asks whether the household **hired a tutor** ("是否请家教") and **hours per week in other tutoring classes** ("每周上多少小时其他辅导班"); education-expense module (family education expense, past year) | **D(snippet)** | CFPS questionnaire PDFs indexed with these item texts | exact variable names/years (2010–2022) from CFPS codebook |
| CFPS access route | PKU ISSS | free registration/download for academic use via CFPS website (Data Acquisition page) | **D(snippet)/V** | ISSS Data Acquisition page indexed; page fetch failed in this environment | confirm current registration and licence terms on site |
| KOSTAT Private Education Expenditures Survey | Statistics Korea | annual national survey: participation rate, weekly hours, monthly private-education expenditure per student; school level, region; provider type (private institute/hagwon, individual/group tutoring, online, after-school) | **D(snippet)/L** | 2024 press-release page located (Statistics Korea social statistics); series used in literature | confirm the income/wealth breakdown and exact provider categories in the 2024 report tables |
| TIMSS/PIRLS tutoring-adjacent items | IEA | background questionnaires include extra-lesson/tutoring-adjacent items; variable harmonisation guidance lists such variables; used in shadow-education analyses | **D(snippet)** | PIONEERED D4.1 harmonisation guidelines; TIMSS South Africa shadow-education working paper | exact item codes/wording, cycles, and country availability |
| HK EDB tutoring survey content | HK EDB commissioned survey | Volume 3 includes a "Demand for tutoring" section | **D(snippet)** | EDB T-survey Volume 3 PDF indexed with that heading | participation/expenditure/provider tables; whether microdata exist (none located) |
| DHS tutoring variables | DHS programme | **none** — standard DHS core questionnaires contain no tutoring or education-expenditure module; the eight DHS experiments here have no tutoring variable | **D (verified in-repo)** | DHS experiment schema (`experiments/dhs_v1`) and DHS questionnaire scope | — (none expected) |

## 2. One-line verdict per country — what can be tested

* **Hong Kong — feasible-partial (participation/hours only).** PISA 2018/2022 gives participation and hours (ESCS
  quintiles) once the codebook is confirmed; **no open microdata for expenditure or provider type**
  (EDB report-level only). Own-teacher vs firm is **unobserved**, so the supply-form prediction **cannot be tested**.
* **Philippines — feasible-partial (participation/hours only).** PISA 2018/2022 (plus SEA-PLM 2019 participation
  pending codebook); **no provider-type or expenditure microdata**; supply-form prediction **cannot be tested**.
* **Cambodia — feasible-partial at best, conditional (participation proxy only).** Not a PISA participant
  (PISA-D 2017 only); the only route is the **SEA-PLM 2019 codebook — tutoring item still V**. No provider-type,
  no expenditure. Supply-form prediction **cannot be tested**.
* **China — strongest, still partial.** Participation/hours: PISA (2009–2022, B-S-J-Z variants) + CFPS/CEPS;
  expenditure: **CFPS (open registration)** or **CEPS (CSSD agreement)** or **CIEFR-HS (verified access route,
  institutional-email review)**; **Double Reduction (2021) before/after is feasible** with CIEFR-HS 2019 vs 2021
  (+ CFPS 2020 vs 2022), with published evaluations as reference. Provider type only **partial** (CFPS "tutor vs
  classes"; CIEFR-HS needs questionnaire check). Own-teacher *withholding* remains unobserved.
* **Korea — reference benchmark only (not a target country).** KOSTAT aggregates provide participation,
  expenditure **and provider-type** benchmarks; suitable as the supply-form comparator, not as a study country.

## 3. Binding limitation (must appear in Paper C claims and both companion docs)

**HK-vs-PH supply-form (own-teacher vs firm) is unobserved in both settings.** With the current portfolio the
**emergence/supply-form prediction cannot be tested**; Paper C's empirical leg is **feasible-partial
(participation/hours only)** until (i) PISA 2018/2022 codebooks are checked, (ii) the SEA-PLM 2019 tutoring item is
confirmed or ruled out, and (iii) China microdata access (CIEFR-HS/CFPS) is granted. The **theory-only list**
(withholding, positive school-supply `S`, learning decomposition `G=max(0,L−S)`, supply-form equilibrium,
informal prices/teacher hours/firm capacity) **remains intact** and must not be imputed from these sources.

## 4. Next steps (in order)

1. PISA 2018 and 2022 student-questionnaire codebooks: confirm out-of-school/after-school lesson items, exact
   wording, hours categories, subject coverage, ESCS derivation; check for any expenditure/provider item
   (expected none). Public documents; no microdata needed for the codebook check.
2. SEA-PLM 2019 student and parent codebooks: confirm/deny the tutoring/extra-lesson item for KH/PH; record
   coverage and wording.
3. China: submit CIEFR-HS access request (institutional email) and/or register CFPS; obtain CEPS agreement;
   confirm tutoring item wording in CIEFR-HS 2021 questionnaire once access allows.
4. Only after 1–3: draft Paper C's pre-registration with a data-availability matrix per regime, keeping anything
   unobserved theory-only.
