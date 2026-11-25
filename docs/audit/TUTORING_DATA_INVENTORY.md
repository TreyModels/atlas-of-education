# Tutoring-data inventory — HK / Philippines / Cambodia / China (and Korea reference)

**Owner:** `contest-math` (re-tasked by Lead, 2026-11-25; host-only, no box). **Status:** inventory only — **no
data acquired, no microdata downloaded, no downloads committed, no validation claim**. Supersedes the 40-line
provisional pass committed at `0bf24b6`; changes are marked. Access/licence lines must be re-verified against the
provider's current terms before any acquisition.

**Purpose:** identify what data could test the Paper C predictions on *why shadow education emerges* and *what
determines its supply form* (own teacher vs firm/private institute vs online), especially HK vs Philippines, with
Cambodia and China as anchors. Paper C is currently theory/simulation because the repository holds no tutoring
participation/expenditure microdata (`PAPER_C_MODEL_GAP.md`: demand/supply/withholding are modelled; the
empirical leg is absent).

**Verification method and its limit (stated because it matters):** this pass used public web search results and
public documentation; PDFs/codebooks were **not** fetched (the environment could not resolve the publishers'
hosts). Rows are therefore marked **D** = documented in a public source located in this pass, **L** = reported in
the literature, **V** = must be verified in the codebook/dataset before use. Do not upgrade a **V** row to fact
without the codebook.

## 1. Matrix — source × country × variables × years × access

| # | source (type) | HK | PH | KH | CN | KR | tutoring variables (what is plausibly there) | expenditure | provider type | income/wealth linkage | years | access / licence | verdict for Paper C |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | **PISA** (ILSA, OECD) | yes (all cycles 2000–2022) **D** | yes (2018, 2022) **D** | **no** (PISA-D 2017 instead) **D** | yes (2009/2012 Shanghai; 2015/2018/2022 B-S-J-Z variants) **V** | yes (all cycles) | **out-of-school / after-school lessons** items: participation and **hours per week** in several cycles (PISA 2009 SG study **D**; PISA 2018 Results Vol V ch. on after-school lessons **D**; PISA 2022 private-tutoring study **D**); subject-specific in some cycles **V** | **not collected** (no cost/expenditure item) **D** | **no** own-teacher vs firm distinction **D** | ESCS socio-economic index (not income); ESCS quintiles usable | 2000–2022 (item availability varies by cycle) **V** | public-use microdata via OECD PISA database / registration; free for research | **Best for participation + hours in HK/PH/CN**; cannot answer (b) provider share or expenditure; can answer (a) participation by ESCS quintile |
| 2 | **SEA-PLM 2019** (ILSA, UNICEF/SEAMEO) | no | **yes** | **yes** | no | no | student/parent/teacher context questionnaires include learning-support and out-of-school-practice items; a tutoring-specific item is **plausible but unverified** (**V**; codebook: `SEA-PLM MS19 Codebook Student Questionnaire` **D** URL below) | unlikely **V** | no | parental education/occupation, home resources (not income) | 2019 (first cycle); 2024 cycle framework published **D** | public reports; microdata via SEA-PLM/UNICEF agreement | **Candidate for KH/PH participation** (proxy), not provider/expenditure; highest value for Cambodia, which has no PISA |
| 3 | **PISA-D 2017** (ILSA, OECD) | no | no | **yes** | no | no | limited out-of-school lesson items **V** | no | no | ESCS-like | 2017 only | public reports/microdata via OECD | fallback for KH; single cross-section, no policy variation |
| 4 | **TIMSS / PIRLS** (ILSA, IEA) | yes (TIMSS 4/8; PIRLS) **D** | PH: TIMSS 2003 (not current) **V** | no | HK only (mainland not a TIMSS/PIRLS participant) | yes | student/parent background questionnaires contain extra-lesson/tutoring-adjacent items; IEA harmonisation guidance lists such variables (**D** PIONEERED D4.1; TIMSS-SA shadow-education study uses TIMSS items **L**) | no | no | home resources, parental education | TIMSS 1995–2023; PIRLS 2001–2021 | public via IEA (registration) | secondary; useful for HK/KR cross-checks, not for PH/KH/CN |
| 5 | **KOSTAT Private Education Expenditures Survey** (national statistics, KR) | no | no | no | no | **yes** | participation rate, weekly hours, **monthly private-education expenditure per student**; by school level, region, income level **V**, and **provider type** (private institute/hagwon, individual/group tutoring, online, after-school) **D** (2024 press release) | **yes** (aggregate; microdata by approval) | **yes — best source for own-vs-firm-type share** | income-level breakdown **V** (not a full quintile micro linkage) | annual series ~2007–2024 **D** | press releases/reports public; microdata via KOSTAT MDIS approval | **Best for (b) provider-type and expenditure**, KR only; enables descriptive before/after around KR fee caps/curfew — not causal |
| 6 | **China Family Panel Studies (CFPS)** (household panel, PKU ISSS) | no | no | no | **yes** | no | household education-expenditure module **D** (questionnaire D5 family education expense past year) and tutoring questions **D** ("whether hired a tutor"; "hours per week in other tutoring classes") | **yes** (household education spending; tutoring-specific items **V**) | partial: tutor vs classes wording **V** | household income/expenditure, assets, education | 2010, 2012, 2014, 2016, 2018, 2020, 2022 **V** | free registration (PKU ISSS) for research | **Best open micro source for CN expenditure + Double Reduction before/after** (2020 vs 2022 waves) |
| 7 | **CEPS** (China Education Panel Survey, Renmin Univ.) | no | no | no | **yes** | no | after-school tutoring time/expenditure items used widely in the literature **L**; waves 2013-14, 2014-15 | **yes (L)** | limited **V** | household income/wealth, parental education | 2013-14, 2014-15 (pre-Double-Reduction only) | academic application/agreement | strong CN micro source **but ends before 2021 policy** → cannot test Double Reduction itself |
| 8 | **CIEFR-HS** (China Institute for Educational Finance Research household survey, PKU) | no | no | no | **yes** | no | education expenditure + tutoring modules; used in published **Double Reduction short-term evaluations** (**L**; Chinese-language report) | **yes** | partial **V** | income/expenditure | 2017, 2019, 2021, 2023 **V** | academic application (CIEFR) | **strongest candidate to test the 2021 Double Reduction break in CN**; access is the constraint |
| 9 | **Philippines APIS / FIES** (national household surveys, PSA) | no | **yes** | no | no | no | education-expenditure modules (tuition/allowances/other school costs); tutoring-specific line **V** (likely not separate) | partial (education total) | no | income/expenditure (FIES) | APIS annual-ish; FIES every 3 years | PSA microdata request/public-use files | weak for tutoring; can give household capacity for income-quintile joins |
| 10 | **Cambodia CSES** (national household survey, NIS) | no | no | **yes** | no | no | education-expenditure categories (tuition, supplies, transport; "extra classes" line **V**) | partial **V** | no | consumption/income quintiles | periodic (2019/2021/2023) | NIS/World Bank request | weak for tutoring; household capacity only |
| 11 | **Hong Kong** (EDB commissioned survey; Census & Statistics Dept thematic surveys; academic Bray-type surveys) | **yes** | no | no | no | no | **demand-for-tutoring survey content** (**D** EDB T-survey Volume 3 lists "Demand for tutoring"), participation/expenditure/provider items **V**; academic surveys **L** | possibly (reports) | possibly **V** | household income bands **V** | ad hoc/periodic **V** | reports/publications only; **no open microdata found** | **only route for HK provider/expenditure is report-level**; treat as descriptive literature, not dataset |
| 12 | **DHS** (household surveys; used by this programme) | no DHS | PH DHS yes | KH DHS yes | no DHS | no | **no tutoring or education-expenditure module in the standard DHS core questionnaires**; the eight DHS experiments here contain no tutoring variable | no | no | wealth index (relative assets), not income | PH 1993–2022; KH 2000–2021-22 | DHS programme (gated access, already held locally for these countries) | **cannot test tutoring**; can only constrain household demand/composition correlates (see companion mapping) |
| 13 | **OECD / KEDI / other** | — | — | — | — | KEDI analyses of KOSTAT data **L** | KR series literature; no new microdata | — | — | — | — | — | reference/literature only |

**Explicit gaps:** no source located that simultaneously provides (i) tutoring participation, (ii) expenditure,
(iii) own-teacher vs firm provider, (iv) teacher hours/withholding, and (v) learning outcomes for even one of
HK/PH/KH/CN. Any Paper C empirical design must combine sources with explicit joins and declared missingness.

## 2. Feasible tests (what the portfolio can actually support)

| test | source(s) | what is estimable | caveat |
|---|---|---|---|
| **Part (a) — participation by income/wealth quintile** | PISA 2018/2022 (HK, PH, CN) **D/V**; SEA-PLM 2019 (KH, PH) **V**; CFPS/CIEFR (CN) **D/L**; KOSTAT by income level (KR) **V**; HK reports **V** | participation rate and hours by ESCS quintile / income quintile, within country and wave | PISA gives ESCS, not income; wealth ≠ income (programme rule); KH/PH SEA-PLM item must be codebook-verified |
| **Part (b) — own-teacher vs firm/private-institute share** | **KOSTAT (KR) only, aggregate** **D/V**; HK EDB survey **V**; CFPS partial (tutor vs classes) **V** | provider-type shares and their trend (KR); partial micro split (CN) | **not available for PH/KH at all; not in PISA.** Own-teacher *withholding* (teacher selling back lessons) is **not observed anywhere** → theory-only |
| **Part (c) — change around a policy** | CN: CFPS 2020 vs 2022, CIEFR-HS 2017/2019/2021/2023 **D/L**; KR: KOSTAT annual series around fee caps/curfew **D/V**; HK/PH/KH: no cap policy located | descriptive before/after breaks in participation/expenditure/provider mix | none is causal; Double Reduction evaluation literature exists (**L**) but micro access (CIEFR) is the constraint; CEPS ends 2015 so pre-policy only |
| **Supplementary — expenditure levels** | KOSTAT (KR, aggregate), CFPS (CN, micro), CEPS (CN, pre-2021), HK reports | expenditure per student/per household, by income band | no expenditure in PISA/SEA-PLM/TIMSS; PH/KH only education-total proxies |
| **Supplementary — HK vs PH emergence/supply-form comparison** | PISA 2018/2022 (participation+hours both), KOSTAT KR for provider benchmark, literature (HK) | cross-country descriptive contrast of participation/intensity gradients | **supply-form (own vs firm) comparison is not feasible for HK vs PH** — HK provider data are report-level at best, PH has none; the emergence prediction can be *illustrated*, not tested, with this portfolio |

## 3. What remains theory-only (must not be imputed or asserted)

1. **Own-teacher withholding** — `h = h_max·driver(w_T/w_out)·(1−monitoring)·(1−own_ban)`; no dataset observes
   withheld lessons, side payments, or teacher sell-back.
2. **Teacher effort/time budget and school effort `S`** (homework/feedback/supervision as a *positive* supply
   lever); only indirect PISA school-questionnaire proxies exist.
3. **Learning decomposition `G = max(0, L − S)`** and substitution/complementarity between school and tutoring —
   requires linked learning measures and tutoring time, not available in one source.
4. **Supply-form equilibrium** (own-teacher strategy, firm entry/capacity, state supply, welfare) for HK/PH/KH.
5. **Own-teacher vs firm share in PH/KH** (and HK beyond report level).
6. **Informal market prices, teacher hours/workload, firm capacity** — no source.
7. **Fertility/massification mediation through tutoring** — no panel linking tutoring to fertility/completion.

## 4. Access/licence notes (public sources found in this pass; re-verify before acquisition)

* PISA microdata: OECD PISA database / public-use files, registration + terms of use (free for research).
  PISA 2022 technical report and questionnaires are public. PISA 2018 Results Volume V (after-school lessons)
  is public.
* SEA-PLM 2019/2024: public reports/frameworks; datasets via SEA-PLM/UNICEF agreement.
* TIMSS/PIRLS: IEA public-use data via registration; harmonisation guidance public.
* KOSTAT private-education survey: press releases/reports public; microdata via MDIS approval (Korean-language
  documentation).
* CFPS: free registration via PKU ISSS; CEPS/CIEFR-HS: academic application (Renmin/PKU) — **paywall/approval
  risk** is access, not fees.
* PH APIS/FIES and KH CSES: PSA/NIS microdata request (public-use files with conditions).
* HK EDB and Census thematic surveys: published reports only; **no open microdata located**.
* DHS: gated programme access; already held locally for PH/KH under access terms (not redistributed).
* World Bank household education-expenditure guidebook: useful for harmonising expenditure categories
  (tuition vs private lessons vs transport) when a survey has only education-total.

## 5. Sources located in this pass (URLs; not all fetched — see verification note)

* PISA 2018 Results Volume V, "Learning time during and after school hours" (after-school lessons):
  <https://www.oecd.org/en/publications/pisa-2018-results-volume-v_ca768d40-en/full-report/component-12.html>
* PISA 2022 technical report (questionnaires appendices):
  <https://www.oecd.org/content/dam/oecd/en/publications/reports/2024/03/pisa-2022-technical-report_599753f0/01820d6d-en.pdf>
* "Illuminating the shadows: the role of private supplementary tutoring on student math performance in PISA 2022",
  *Large-scale Assessments in Education* (2024): <https://link.springer.com/article/10.1186/s40536-024-00228-5>
* PISA 2009 Singapore out-of-school-lessons study (NIE repository):
  <https://repository.nie.edu.sg/entities/publication/eb8236a1-f03a-42fa-9d33-251d7415d4fb>
* SEA-PLM 2019 student-questionnaire codebook:
  <https://www.seaplm.org/PUBLICATIONS/SEA-PLM_2019_Datasets/Codebooks/SEA-PLM%20MS19%20Codebook%20Student%20Questionnaire.pdf>
* SEA-PLM 2019 Main Regional Report (UNICEF EAP):
  <https://www.unicef.org/eap/media/7626/file/SEAPLM%202019%20Main%20Regional%20Report.pdf>
* SEA-PLM 2024 questionnaire framework:
  <https://www.seaplm.org/images/DOWNLOADS/SEA-PLM_2024_Test_Questionnaire_Framework_Final_.pdf>
* KOSTAT Private Education Expenditures Survey 2024 press release:
  <https://mods.go.kr/board.es?act=view&bid=11758&list_no=436035&mid=a20111010000>
* CFPS questionnaires (tutoring items: "whether hired a tutor", "hours per week in other tutoring classes"):
  <http://www.isss.pku.edu.cn/cfps/docs/20230418165136294533.pdf> ;
  CFPS education-expense item D5: <https://www.isss.pku.edu.cn/cfps/docs/20251009130808714749.pdf>
* Double Reduction short-term evaluation using CIEFR household data (Chinese-language):
  <http://mp.weixin.qq.com/s?__biz=MzI3MDE3Nzg0OA==&mid=2247488495&idx=1&sn=81e2d1675031d69d0124561b42724d1a> ;
  thesis: "Evaluating Shadow Education: International Evidence and China's Double Reduction Policy"
  <https://etheses.durham.ac.uk/id/eprint/16842/>
* HK EDB commissioned survey (Volume 3 includes "Demand for tutoring"):
  <https://eservices-help.edb.gov.hk/irooms/eservices/T-surf/Content/Documents/HKTC%20Volume%203.pdf>
* TIMSS/PIRLS variable-harmonisation guidance (PIONEERED D4.1):
  <https://www.pioneered-project.eu/public-deliverables/PIONEERED_101004392_D4-1_Data_harmonisation_guidelines_Public_19.10.2022.pdf>
* TIMSS South Africa shadow-education working paper (uses TIMSS background items):
  <https://www.timss-sa.org/wp-content/uploads/2022/10/OlivierHofmeyr_Illuminating-shadow-education-in-South-Africa_2022.pdf>
* World Bank, *Measuring Household Expenditure on Education: A Guidebook for Designing Household Survey
  Questionnaires*:
  <https://documents1.worldbank.org/curated/en/494931587033216249/pdf/Measuring-Household-Expenditure-on-Education-A-Guidebook-for-Designing-Household-Survey-Questionnaires.pdf>
* PH basic-education public expenditure review (World Bank) for education-expenditure context:
  <https://documents1.worldbank.org/curated/en/429921603168506339/Philippines-Basic-Education-Public-Expenditure-Review.docx>

## 6. Recommended acquisition order (host-only; no restricted data committed)

1. **PISA 2018 + 2022 public-use microdata** (HK, PH, CN) — verify out-of-school-lessons items, hours, ESCS
   quintiles. Best cost/benefit; answers (a) for three settings and gives participation for the HK/PH contrast.
2. **SEA-PLM 2019** (KH, PH) — codebook check for a tutoring/extra-lesson item; if absent, record as absent.
3. **CIEFR-HS or CFPS** (CN) — Double Reduction before/after; CIEFR preferred for policy timing, CFPS for open
   access.
4. **KOSTAT** (KR) — provider-type and expenditure benchmark (aggregate reports first; microdata only with
   approval).
5. HK: literature/report compilation only (Bray-type surveys, EDB thematic reports); no dataset acquisition path
   found.
6. Only then draft a Paper C pre-registration with a data-availability matrix per supply regime; anything
   unobserved stays theory-only.

**Do not** substitute PISA ESCS for income, hours for expenditure, or report-level HK figures for microdata.
