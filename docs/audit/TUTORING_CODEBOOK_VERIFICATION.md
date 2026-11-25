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

## 1b. Verification attempt log — tool-based fetch was also blocked (important)

The Lead asked for tool-based retrieval (not `curl`). I retried with the platform's `web_fetch` tool on the
specific documents and on alternative mirrors/hosts. **Result: every external education host was refused by the
sandbox's DNS resolution step** (`URL hostname "<host>" resolves to a non-public IP address`), including:
`www.oecd.org`, `www.oecd-ilibrary.org`, `www.seaplm.org`, `omb.report`, `files.eric.ed.gov`, `nces.ed.gov`,
`timssandpirls.bc.edu`, `unesdoc.unesco.org`, `core.ac.uk`, `www.moe.gov.my`, `ied.edu.hk`, `teric.naer.edu.tw`,
`www.naer.edu.tw`, `www.unicef.org`, `mods.go.kr`, `scispace.com`, `plp.moeys.gov.kh`, `pioneered-project.eu`,
`link.springer.com`. Only Peking University / Renmin University / CIEFR hosts resolved
(`opendata.pku.edu.cn`, `ciefr.pku.edu.cn`, `ceps.ruc.edu.cn`, `cssd.ruc.edu.cn`).

**Consequence:** exact PISA/SEA-PLM **item codes, wording and page numbers could not be read from the source
documents in this environment**, despite retrying via the tool. They remain **V** (unverified) and must not be
presented as verified. `web_search` returns only indexed snippets/URLs (with occasional page anchors) and cannot
substitute for a codebook read. Workaround: retrieve the four documents below from a host with open egress (or the
operator's machine) and read the item text directly; the URLs are known-good public documents:
PISA 2018 student questionnaire (OECD iLibrary PISA-2018-datasets/questionnaires directory), PISA 2022 technical
report (`.../pisa-2022-technical-report_599753f0/01820d6d-en.pdf`, questionnaire appendix), SEA-PLM 2019 codebooks
(`seaplm.org/PUBLICATIONS/SEA-PLM_2019_Datasets/Codebooks/`), SEA-PLM 2019 Cambodia national report
(`seaplm.org/images/DOWNLOADS/SEA-PLM_National_Report_Cambodia.pdf`).

## 1c. Handoff prerequisites (NO applications submitted — operator action)

Per the Lead's instruction, no CIEFR-HS / CFPS / CEPS access application was submitted (they require the
operator's institutional email and data-use agreement). Exact steps, to be handed to Trey:

* **CIEFR-HS (China, preferred for Double Reduction)** — *verified from fetched PKU pages/metadata JSON*:
  1. Register at <https://opendata.pku.edu.cn/> (PKU Open Research Data Platform).
  2. After approval, request the dataset at <https://opendata.pku.edu.cn/dataverse/ciefrhs>.
  3. **Institutional email required** (`xxx@xxx.edu.cn`); personal emails (qq/163) are rejected — this is the
     reason the operator must do it, not the agent.
  4. Terms: academic use only; no redistribution; no upload to other platforms (dataverse terms of access, fetched);
     contact `ciefrhs@ciefr.pku.edu.cn`. Note: **all files are access-restricted, including the questionnaire PDFs**
     (dataset metadata: `restricted: true` on 2021/2022 questionnaires, data `.rar`, and the user guide; the
     dataset *metadata* is CC0 but that does not grant file access).
  5. DOIs: 2021 `10.18170/DVN/QOM4FT`, 2019 `10.18170/DVN/YDQJ3D`, 2017 update `10.18170/DVN/B6HK6Y`, original
     `10.18170/DVN/KE1JYM`. 2021 fieldwork: 2021-07 to 2022-08. Files: 2021 data `.rar` 4.45 MB, questionnaire
     PDFs ~600 KB each, user guide 542 KB.
  6. Expected turnaround: **not published**; plan on staff review (estimate 1–4 weeks; treat as an estimate, not a
     promise). After access, the first check is the tutoring/extra-lesson item wording in the 2021 questionnaire.
* **CFPS (China, open)** — register at PKU ISSS CFPS site (Data Acquisition page:
  <https://www.isss.pku.edu.cn/cfps/en/faq/data23/>); free registration for academic research. **Verify current
  licence and download terms on site (V — page could not be fetched here).** Tutoring items located in indexed
  questionnaire PDFs (“whether hired a tutor”; “hours per week in other tutoring classes”).
* **CEPS (China, pre-2021 policy only)** — Renmin CSSD platform <https://cssd.ruc.edu.cn/>: real-name
  authentication + signed data-use agreement; already-published waves are one-click downloadable, restricted data
  by online application/approval (verified from the fetched CSSD launch page). Expected turnaround: immediate for
  public waves; application/approval for restricted (unpublished SLA).
* **SEA-PLM 2019 (KH/PH)** — codebooks/questionnaires are public documents on `seaplm.org`; no application needed,
  but the host was unreachable from this environment → operator-side download then codebook search for the
  extra-lesson/tutoring item.
* **PISA 2018/2022** — public-use microdata via OECD registration; questionnaires/technical report public. No
  application needed for the codebook check; only the sandbox's egress blocks the documents.

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

## 5. What remains V after this pass (explicit)

1. PISA 2018/2022 **exact item codes and wording** for out-of-school/after-school lessons, hours categories and
   subject coverage (item existence remains D-snippet only).
2. PISA **absence** of expenditure and provider-type items (strongly indicated, not codebook-confirmed).
3. PISA country/variant composition for China 2022 (B-S-J-Z confirmation).
4. SEA-PLM 2019 **tutoring/extra-lesson item existence, wording and coverage** for Cambodia/Philippines.
5. PISA-D 2017 Cambodia out-of-school-lesson item.
6. CFPS exact variable names/years and current licence terms.
7. KOSTAT income breakdown and exact provider categories/turnaround; TIMSS/PIRLS exact items; HK EDB tables.
8. CIEFR-HS **tutoring item wording** (questionnaire is access-restricted; access route is D-verified).
**Remaining D (not V):** CIEFR-HS waves/samples/access/DOI/restriction metadata; CEPS platform/access; PISA item
existence (snippet-level); DHS absence of tutoring variables; the binding HK-vs-PH limitation below.


## 6. ADDENDUM — verified from lead-supplied official PDFs (2026-11-25)

The Lead fetched the official PDFs from a shell with open egress and left them locally (`/tmp/pdfs/`: SEA-PLM 2024
Test Questionnaire Framework, SEA-PLM 2019 Parent Questionnaire + 6-page codebook, PISA 2022 Technical Report,
plus `SEAPLM_EVIDENCE.txt`). Text was extracted locally with `pypdf`; the checks below are **D (verified from the
official document text)**, with page references.

### 6.1 SEA-PLM 2019 Parent Questionnaire — NO tutoring item (verified absence, converts earlier V → D-absent)

Full text of `seaplm2019_parent.pdf` (13 pages) and `seaplm2019_parent_codebook.pdf` (6 pages) searched: **zero
occurrences** of `PA18`, "additional instruction", "tutor", "extra class", "extra lesson", "outside of school",
"paid". Codebook has no PA18. **Verdict: SEA-PLM 2019 cannot measure tutoring for Cambodia/Philippines.** This
kills the earlier (unverified) hope that SEA-PLM 2019 was the KH route.

### 6.2 SEA-PLM 2024 Test Questionnaire Framework, p.89 — PA18 "additional instruction" (verified wording)

Exact item text (parent questionnaire, p.89):
> "18. In this past school year, has your child attended the following types of additional instruction? …
> Additional instruction may be any extra assistance outside regular schooling to support students.
> a) Paid assistance outside of school — PA18A
> b) Free tutoring outside of school — PA18B
> c) Paid tutoring provided by your child's school — PA18C
> d) Free tutoring provided by your child's school — PA18D"

**Response scale (important):** the framework gives four response columns — **"Yes in Literacy", "Yes in
Numeracy", "Yes in Literacy and Numeracy", "No"** — not a binary yes/no. A participation indicator therefore
requires a coding decision (any yes vs both vs literacy/numeracy separately), and a paid-vs-free / school-vs-outside
supply-form share must be defined on that coding. The item is a **2×2 supply-form distinction** (paid/free ×
outside/school) — exactly Paper C's supply-form variable, with the caveat that it is *parent-reported
participation in additional instruction*, not hours/expenditure/provider-firm identity.

### 6.3 SEA-PLM 2024 coverage and data availability

* 2024 is a **six-country** cycle (SEA-PLM 2024 Main Regional Report / Datasets page). **Confirmed participants
  relevant to us: Cambodia (national report published), Philippines, Malaysia (national summary published),
  Vietnam (results/news)**. The other two countries are **not verified here** — do not assume; candidates (Lao
  PDR, Timor-Leste) are unconfirmed, and Myanmar's 2024 status is unconfirmed.
* Data release: per the Lead, ILSA-Gateway announced **"SEA-PLM 2024: Writing Results and Data Now Available"**.
  Official pages located: Datasets & Questionnaires 2024
  (`seaplm.org/index.php/sea-plm-2024/datasets-and-questionnaires-2024`), **SEA-PLM 2024 Data User Manual**
  (December 2025, `seaplm.org/images/PUBLICATION/2025/Datasets__Questionnaires_2024/SEA-PLM_2024_data_manual_December_2025.pdf`),
  Coding/Scaling/Scoring report (2026, documents parent-questionnaire content), and the 2024 Main Regional Report.
* **Data access route: V (not yet read).** The Datasets page and Data User Manual are public documents but could
  not be fetched from this sandbox. Expected pattern (to verify from the data manual): registration/agreement,
  then download of student/parent/teacher/school files. **Parent↔student linkage: V** — the data manual is the
  document that defines the linking IDs; it must be read before assuming parent records can be merged to student
  records.
* **Codebook status for PA18A–D: V** — the framework defines the items; whether the public 2024 dataset includes
  PA18A–D variables and their exact coded values must be confirmed in the 2024 codebook/data manual.

### 6.4 PISA 2022 — student-level "additional mathematics instruction" vs school-level MACTIV (verified distinction)

From the PISA 2022 Technical Report (local `pisa2022_tech.pdf`, 545 pages):
* **Student level:** item **ST297 "Out-of-school experiences — Participation in additional mathematics
  instruction"** appears in the PISA 2022 student questionnaire item list (Annex 5.A.3; the row indicates
  **not in 2018, present in 2022**). It is a participation item (yes/no style); **no hours, no expenditure, no
  provider type**. Exact question wording/response options: **V** (the questionnaire itself is not in this bundle;
  the technical report gives the item label, not the wording).
* **School level:** **MACTIV** is a *school*-level index built from SC181 ("additional mathematics lessons offered
  at the school": enrichment/remedial/without differentiation) and SC053 (maths club, competitions, computer club),
  range 0–5 (technical report §19, p.415 context). **MACTIV is not a student out-of-school-lesson measure** — the
  Lead's caution is confirmed.
* PISA 2022 has **no tutoring expenditure item and no own-teacher-vs-firm provider item** among the located
  variables; no hours-of-out-of-school-lessons item surfaced in this report (the older-cycle "out-of-school
  lessons" analyses, e.g. PISA 2009/2018, need their own questionnaire checks — still V).

### 6.5 Net effect on Paper C's data feasibility

* **Cambodia/Philippines gain a real supply-form test** — participation plus **paid/free × school/outside**
  (PA18A–D) — **conditional on** (i) 2024 coverage/codebook confirmation, (ii) data access, (iii) parent↔student
  linkage, and (iv) a documented coding rule for the 4-column response scale. Until those are confirmed, the
  correct label is **"feasible pending verification"**, not "available".
* **Own-teacher withholding, hours, expenditure and firm identity remain unobserved** in SEA-PLM 2019/2024 and
  PISA; the theory-only list therefore stands for those constructs. The HK-vs-PH **own-teacher-vs-firm share**
  remains unobserved in both settings (PISA has no provider item; SEA-PLM PA18 gives school-vs-outside, not
  own-teacher-sell-back).
