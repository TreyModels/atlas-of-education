# G2-A CITATION VERIFICATION — hard gate result (2026-11-25)

**Status: HARD GATE NOT PASSED — all four calibration moments are demoted to UNRESOLVED and dropped from the
training set. G2-B calibration therefore CANNOT start.** This is the gate working as pre-declared: unsourced moments
are not used, and no improvised substitute is made.

## What was attempted (evidence)

1. **External retrieval.** Web search located candidate sources: the Korean 2024 "Private Education Expenditures
   Survey" press release (`mods.go.kr/board.es?...list_no=436035`), 2025 English coverage, and HK shadow-education
   literature/survey pages. **Every direct fetch failed in this environment with `URL hostname resolves to a
   non-public IP address`** (tested: mods.go.kr, kess.kedi.re.kr, kedi.re.kr file link, sciencedirect,
   core.ac.uk, en.wikipedia.org, m-en.yna.co.kr, en.news1.kr, en.sedaily.com, asiae.co.kr, chinaview.cn,
   rki.kbs.co.kr, headfoundation.org, eservices-help.edb.gov.hk). The environment’s network policy blocks these
   hosts, so the values could not be independently verified here.
2. **Repository evidence.** The Paper B manuscript (`Shadow_Education_Arms_Race_HK_Korea_APA.docx`) asserts
   "published benchmarks" for HK Grade 9 (53.8 %) / Grade 12 (71.8 %) and Korean K−12 participation (75.7–78.5 % vs
   76.5 %), and a Korean quintile gap (+32.1 pp) / spend ratio (3.4×), **but its reference list contains no KEDI
   2024/2025 entry and no HK 2011/12 survey entry**. The Korean text cites `Statistics Korea & Ministry of Education
   (2023) 2022 Private Education Expenditure Survey` and two web summaries for a **2023 = 78.5 %** figure — not the
   2024 = 80.0 % figure used in the programme record. No traceable citation exists in the tree for the four exact
   moments.

## Per-moment gate decision (consequence)

| moment | prior status | verification result | G2-A disposition |
|---|---|---|---|
| KR overall participation 2024 = **80.0 %** | AUTHOR-REPORTED | no KEDI report in tree; 80.0 % does not appear in the manuscript (it reports 78.5 % for 2023); source host unfetchable | **UNRESOLVED — DROPPED** from fit |
| KR overall participation 2025 = **75.7 %** (held-out) | AUTHOR-REPORTED | manuscript cites web summaries/SBS, not the survey; host unfetchable | **UNRESOLVED — DROPPED** (held-out slot stays empty) |
| HK Grade 9 = **53.8 %** (2011/12) | AUTHOR-REPORTED | no HK 2011/12 survey reference entry; literature pages unfetchable | **UNRESOLVED — DROPPED** from fit |
| HK Grade 12 = **71.8 %** (2011/12, held-out) | AUTHOR-REPORTED | same | **UNRESOLVED — DROPPED** (held-out slot empty) |
| KR Q5−Q1 gap = **32.1 pp** (target) | AUTHOR-REPORTED derived | derived target; no empirical source located | **UNRESOLVED — DROPPED** (cannot be fitted or validated) |
| KR Q5/Q1 spend ratio = **3.4×** (target, per-student) | AUTHOR-REPORTED derived | derived target; no empirical source located; per-participant vs per-student unresolved in sources | **UNRESOLVED — DROPPED** |
| KR participation target 76.5 % | derived, diagnostic-only | overlaps survey rows; already excluded from fit | **DIAGNOSTIC only (unchanged)** |

**Consequence:** the calibration training set is **empty**, so G2-B is **blocked at G2-A** pending sources. This is
also a reproducible-audit finding: the manuscript's "published benchmarks" are **not traceable to its reference list**
— a citation/reproducibility defect in the same class as review §7, now recorded as a claim-ledger row.

## What unblocks G2-A (operator action required)

Provide the **primary sources** (PDF/Excel or exact citation + table/page) for:
1. Statistics Korea / Ministry of Education (KEDI) *Private Education Expenditure Survey* — 2024 and 2025 reports,
   with the overall participation rate, population, denominator, and sampling uncertainty;
2. the HK 2011/12 private supplementary tutoring survey (e.g. Bray/Kwo or EDB) with Grade 9/Grade 12 participation,
   population and denominator;
3. the empirical basis of the Korean Q5−Q1 participation gap (32.1 pp) and per-student spend ratio (3.4×),
   **stating household-income brackets and per-student vs per-participant definition**.
If the operator instead supplies microdata or a pre-agreed fallback, G2-A can re-derive moments with the same
definitions and record them as **REPRODUCED from supplied source**, not author-asserted. Until then: no calibration.

## Re-verification protocol (when sources arrive)

For each source: record citation, survey year, population, denominator, outcome definition, table/page, and
uncertainty; hash the supplied file (sha256) and archive it under `docs/audit/sources/`; re-run this gate table and
only then promote a row to CALIBRATION / HELD-OUT. The four moments remain DROPPED until that happens.
