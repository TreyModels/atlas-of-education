# Tutoring-data inventory (host task, 2026-11-25) — HK / PH / Cambodia / China

**Purpose:** what tutoring participation/expenditure data exist and are accessible for the Paper C design (supply-form:
private tutor vs own teacher vs school; positional vs learning). **Status: inventory only — no data acquired, no
downloads committed, no claims.** Access notes are provisional and must be re-verified before use.

## 1. International large-scale assessments (ILSA)

| source | coverage of our four settings | tutoring content | access | provisional verdict |
|---|---|---|---|---|
| **PISA 2022** (OECD) | Hong Kong, Macao, **Philippines 2022**, China (B-S-J-Z 2018/2022 variants); **Cambodia not a PISA participant** | Student questionnaire includes **out-of-school lessons / private tutoring** items (hours and sometimes expenditure) in several cycles; 2022 microdata are available via OECD PISA database / public-use files with registration | Public-use microdata, registration/EULA | **Best candidate for HK/PH tutoring participation/intensity**; expenditure coverage must be checked item-by-item |
| **SEA-PLM 2019** (UNICEF/SEAMEO) | Cambodia, Philippines (and Lao, Malaysia, Myanmar, Vietnam) | Contextual questionnaires cover home/school/learning support; tutoring-specific items are limited (main regional report documents contextual questionnaires) — must be checked in the codebook | Public reports + (restricted?) microdata via UNICEF/SEAMEO | **Candidate for Cambodia/PH**, likely participation proxies only; expenditure unlikely |
| **PISA-D / other** | Cambodia (PISA-D 2017) | limited; may include out-of-school lesson items | public | secondary fallback |
| **CEPS** (China Education Panel Survey) | China (nationally representative, 2014–15 etc.) | **After-school tutoring expenditure** questions used in published work | Academic access/application | **Best candidate for China expenditure**; not HK/PH/KH |
| **TIMSS/PIRLS** | HK, PH (sparse), China (some) | contextual questionnaires; tutoring items inconsistent | public | not primary |

## 2. National/household sources

* **Hong Kong**: no open household tutoring-expenditure microdata located in this quick pass; the published literature
  uses bespoke surveys (e.g., Bray's HK shadow-education surveys) — **theory-only unless a licensed dataset is supplied**.
* **Philippines**: PISA 2022 is the practical route; no open national tutoring-expenditure survey identified.
* **Cambodia**: SEA-PLM 2019 context questionnaires; no open tutoring-expenditure series identified.
* **China**: CEPS (expenditure) and CHFS/CFPS (household education spending, less tutoring-specific); CEPS is the
  standard source in the literature (e.g., rural-migrant-work / tutoring-expenditure studies).

## 3. What remains theory-only

Own-teacher **withholding** and teacher **effort/time budget** are not observed in any of these sources; they remain
model constructs. School-supply levers (homework, feedback, supervision) are observable only indirectly
(PISA school questionnaire), not as a positive supply S with teacher hours. **No source gives all of**: participation,
expenditure, own-teacher vs firm provider, teacher hours, student time, learning outcomes — the programme's outcome
accounting will have to combine sources with explicit joins and declared missingness.

## 4. Recommended next steps (host, no box compute)

1. Verify PISA 2022 student-questionnaire tutoring items and expenditure availability for HK/PH from the codebook.
2. Verify SEA-PLM 2019 codebook for Cambodia/PH tutoring items.
3. Obtain CEPS access route for China expenditure.
4. Only then preregister Paper C with a data-availability matrix per supply regime; anything unobserved stays
   theory-only, not imputed.
