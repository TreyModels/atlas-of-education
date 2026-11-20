# CLAIM_VERIFICATION — manuscript numbers against retrieved primaries

Compiled 2026-11-20 by `data-hunter` for `lead`. Every value below is traceable to a file in `raw/`, a row in `data/*.csv`, and an entry in `SOURCES.json`. Verdicts: **verified** / **partial** / **unresolved** / **contradicted**. Where a claim is about a *model output* rather than an observation, it is out of scope here and marked so.

Manuscripts: `00_handoff/papers/01_june_bjorn.txt` (June paper) and `02_october_massification.md` (October paper).

---

## 1. Philippines upper-secondary completion, 67.5% (2013) and 67.0% (2022)

**Claim (June, line 116):** "The last observed UNESCO Institute for Statistics (UIS) series value - upper-secondary completion at 67.0% in 2022 - sits near the pre-reform 2013 baseline of 67.5%, well above the floor critics forecast, though the 2022 figure partly reflects pandemic disruption; the UNESCO modeled trend continues rising through 2024."

**Verdict: PARTIAL — the 2013 baseline is verified exactly; the 2022 value is not reproducible in the current UIS release and appears to be a superseded vintage. The correction strengthens the paper's argument.**

| Piece | Current UIS SDG4 (release 2026-11) value | Verdict |
|---|---|---|
| Upper-secondary completion (`CR.3`), Philippines, **2013** | **67.47%** (source: Philippines DHS 2013) | Rounds to 67.5 — **verified exactly** |
| Upper-secondary completion (`CR.3`), Philippines, **2022** | **68.28%** (source: UIS based on PHL Labour Force Survey 2022, ILO harmonised microdata) | 67.0% **not reproduced**; likely an earlier UIS vintage. Treat 67.0% as superseded/stale unless the exact vintage is cited. |
| `CR.3`, Philippines, 2023 | **71.93%** (PHL LFS December 2023) | — |
| `CR.3`, Philippines, 2024 | **75.03%** (PHL LFS December 2024) | Post-reform completion now **7.5 pp above** the 2013 baseline |
| Modelled trend (`CR.MOD.3`), 2022 / 2024 / 2025 | **72.09 / 73.06 / 73.54** | "continues rising through 2024" — **verified** |

Files: `data/uis_sdg4_4countries_long.csv` (`CR.3`, `CR.MOD.3`, iso3=PHL); source metadata in `data/uis_sdg4_data_sources.csv`; raw archive `raw/uis/SDG_202611.zip`.

**Two cautions for the text.**
1. **Cross-instrument comparison.** PHL `CR.3` is DHS-based in 2013 and 2017 and **LFS-based from 2022 onward**. The 67.5% → 68.3%/75.0% movement crosses survey instruments as well as time. The 2017 value (76.4%, DHS) is *higher* than the 2013 value, which means the "2022 dip" is not a clean within-instrument trend either.
2. **"Last observed UIS series value" is no longer true.** Observations now exist for 2023 and 2024. Suggested replacement: *"UIS upper-secondary completion rose from 67.5% in 2013 (DHS) to 75.0% in 2024 (LFS), with a pandemic trough at 68.3% in 2022; the UIS modelled series rises without interruption, 70.2% (2018) → 73.1% (2024)."* Note that the 2024 value belongs to cohorts who entered senior high school after RA 10533 took effect, so it is the first clean post-reform reading.

---

## 2. "More than four in ten" / "more than half" lost before secondary completion (Philippines)

**Claims (June, line 74):** "A state losing more than four in ten students before secondary completion cannot run hard norm-referenced sorting at mass scale…"; (line 115): "extended the pipeline by two years while already losing more than half their students before secondary completion under K-10".

**Verdict: MIXED — the "four in ten" figure is verified for the late-1990s/early-2000s K-10 pipeline but is false of 2013, the reform baseline the paper uses elsewhere; the "more than half" figure is not supported by any completion series in the ledger.**

UIS observations for the Philippines (all available years, `data/uis_sdg4_4countries_long.csv`):

| Indicator | 1999 | 2000 | 2003 | 2004 | 2008 | 2010 | 2013 | 2017 | 2022 | 2024 |
|---|---|---|---|---|---|---|---|---|---|---|
| `CR.3` upper-secondary completion (%) | 59.7 | 60.1 | 61.7 | 60.4 | 64.1 | 66.1 | **67.5** | 76.4 | 68.3 | 75.0 |
| → implied **not** completing (%) | **40.3** | 39.9 | 38.3 | 39.6 | 35.9 | 33.9 | **32.5** | 23.6 | 31.7 | 25.0 |
| `CR.2` lower-secondary completion (%) | 58.9 | 65.0 | — | 66.1 | 68.0 | 71.1 | 71.3 | 81.3 | 84.2 | 92.4 |
| → implied **not** completing (%) | **41.1** | 35.0 | — | 33.9 | 32.0 | 28.9 | 28.7 | 18.7 | 15.8 | 7.6 |

- **"More than four in ten" — verified for c.1999–2004**, and also at the start of the run for lower secondary (41.1% in 1999). The claim is defensible if it is **dated to the turn of the century** ("at the end of the 1990s, two in five Philippine adolescents did not complete upper secondary").
- **The same claim is false of 2013.** If the paper's own pre-reform baseline is 2013 (67.5% completion), then the K-10 system at the moment of reform was losing **one in three**, not four in ten. As written, §"deliberate calibration" (line 74) and §"structural opposite" (line 115) are dated to the reform moment and therefore overstate attrition.
- **"More than half" is not supported.** The lowest completion value in the whole UIS run is 58.9% (lower secondary, 1999) — a maximum implied loss of 41.1%. No completion series in the ledger reaches a >50% loss. A *cohort-survival* measure could be lower, but it is a different statistic and was **not retrieved** (DepEd returns HTTP 403; see `retrieval_log.md` §6), so it cannot be asserted.

**Suggested action:** date the four-in-ten claim ("in the late 1990s") or restate it at the 2013 baseline as "one in three"; delete "more than half" unless a DepEd cohort-survival citation is added.

## 3. Cambodia: "6% of jobs", and "6.6% of the national labour force with a post-secondary qualification"

**Status in handoff:** explicitly unresolved; user recalls "near 6%" for Phnom Penh jobs or degree holders, and a secondary lead of 6.6% of the national labour force with a post-secondary qualification.

**Verdict: RESOLVED — the primary table has been found. 6.6% is the share of *employed persons aged 15+* whose highest educational attainment is a university degree (CLFS 2019, Table 5.3). It is not a share of jobs, not a share of the labour force, and not a "post-secondary qualification" share in the broad sense. The "~6% for Phnom Penh jobs" recollection is NOT supported: the urban figure is 13.8%, and Phnom Penh is the most educated part of urban Cambodia.**

Source: NIS/ILO, *Cambodia Labour Force Survey 2019*, final report, **Table 5.3 "Employed Population, by Education Level, Area, and Sex" (report p.32; PDF p.48)**; raw PDF `raw/cambodia/CLFS19_Final_Full_Report_EN.pdf`, extracted text `raw/cambodia/CLFS19_Final_Full_Report_EN.txt`. Row in `data/national_headline_figures.csv`.

Table 5.3, employed persons 15+ (n = 7,883,106), by highest attainment:

| Highest education | Cambodia | Urban | Rural |
|---|---|---|---|
| Never attended school | 10.8 | 5.6 | 13.5 |
| Primary | 38.1 | 28.6 | 43.1 |
| Lower secondary | 25.1 | 28.9 | 23.1 |
| Upper secondary | 15.7 | 20.7 | 13.1 |
| Vocational certificate | 0.4 | 0.5 | 0.3 |
| **University (degree)** | **6.6** | **13.8** | **2.9** |

Corroborating text (executive summary, p. xi; ch. 4 §4.2): "Only 6.6% of them were university graduates, and 0.4% obtained a vocational certificate… There was no significant difference between the proportion of employed males (7.4%) and employed females (5.8%) with a university degree."

**Definitional corrections to apply in the text:**
- **Denominator** = employed persons, not labour force. Labour force = 7,883,106 employed + 97,687 unemployed; the degree share of the labour force is therefore ≈ 6.5%, not 6.6%.
- **"Post-secondary" is broader than "university".** University 6.6% + vocational certificate 0.4% = 7.0%. If the lead meant post-secondary in the ISCED sense (including sub-degree), the number is ~7%, and CLFS does not separate diploma-level tertiary.
- **"Share of jobs requiring a degree" does not exist in any retrieved source.** CLFS records workers' *attainment*, not employers' *requirements*. The manuscript must not convert one into the other. The employment-based proxy for credential saturation — how many *employed* people hold a degree — is 6.6%; the matching "is the degree needed for the job" question would require an employer skills-needs survey (MLVT 2024) or a returns/overeducation measure, **not retrieved**.
- **Cross-check, different concept:** WDI `SE.SEC.CUAT.PO.ZS` (modelled attainment, population 25+, at least completed post-secondary) gives Cambodia **6.66% in 2020** (5.87 in 2021, 6.81 in 2023) — numerically close to 6.6% but a *modelled stock* estimate, not a survey tabulation. Do not cite it as the CLFS number. It is included in `data/wdi_4countries_long.csv` with its definition.

**Also verified in the same report (useful context for the Cambodia cell):** informal employment = **88.3%** of the 7.88 million employed (6,960,060 informal; 923,046 formal; Table 6.2, p.36/PDF p.52), rural 90.0%, urban 85.0%; unemployment 1.2% overall, 2.5% for ages 15–24, 1.2% for university graduates (Table 10.4); NEET (15–24) 12.7% (Table 12.1).

---

## 4. Hong Kong: "85 percent senior secondary tutoring rate"

**Claim (June, line 44):** "Hong Kong's 85 percent senior secondary tutoring rate … (Bray & Lykins, 2012)."

**Verdict: PARTIAL — the number exists and is correctly a senior-secondary figure, but its provenance is a 2010 survey by an unnamed social-welfare body, reported by Kwo & Bray (2011), and the reporting authors explicitly warn that the survey is not statistically robust. The attribution to Bray & Lykins (2012) is a secondary citation (the ADB book was not retrieved in this pass; see gap below).**

Source retrieved: Ora Kwo and Mark Bray, "Facing the shadow education system in Hong Kong", *IIAS Newsletter* No. 56, Spring 2011, p.20. `raw/hongkong/bray_iias_hk.pdf` (+ `.extracted.txt`).

Two survey pairs, verbatim from p.20:
- **1996** telephone survey organised by the **Hong Kong Federation of Youth Groups**: primary 45%, lower secondary 26%, middle secondary 34%, **senior secondary 40%**.
- **2010**, "a social welfare body": lower secondary 72%, middle secondary 82%, **senior secondary 85%**.
- The authors' own caveat, immediately after: *"Neither of these surveys should be considered statistically robust. However, they match the general public perception that the shadow had expanded."*

**Suggested action:** cite the 85% as "a 2010 survey reported by Kwo and Bray (2011), which the authors themselves describe as not statistically robust", and pair it with the 1996 HKFYG figure (40% at senior secondary) so the reader sees the *trend* (40% → 85%) rather than a single fragile point. If Bray & Lykins (2012) is cited, add "as reported in" and note the underlying survey. **Gap:** the ADB book itself was not retrievable (the usual PDF path returns 404; no working copy found), so the manuscript's secondary citation is unverified.

**Bonus verified figure from the same article**, usable for HK's credential-floor narrative: "Thirty years ago, local university education served only **2 percent** of the age group… Now, local universities serve **19 percent** of the population" (p.20, authors' phrasing; note "of the population" is loose — treat as age-group participation).

---

## 5. Hong Kong: HKDSE described as "norm-referenced"

**Claim (June, line 74):** "Hong Kong's HKDSE approaches near-lossless on the positional dimension: fine-grained, **norm-referenced** scores across multiple subjects…"

**Verdict: CONTRADICTED on the reporting model (terminology); the substantive point can be restated accurately.** HKEAA states that HKDSE Category A subjects "adopt **Standards-referenced Reporting** of assessment results… candidates' achievement is reported against a set of standards divided into five levels (levels 1 to 5)… Candidates with the best performance in level 5 are awarded a 5**, and the next top group is awarded a 5*." Source: HKEAA HKDSE introduction page, `raw/hongkong/hkeaa_dse_intro.html`.

So: **standards-referenced, not norm-referenced**; and **five levels plus two top sub-grades**, which is coarse rather than "fine-grained" at the subject level. The fine-grained positional signal the manuscript wants comes from the *aggregate* — JUPAS composite scores across several subjects — not from the per-subject grade scale. Suggested rewording: "standards-referenced per-subject levels (1–5, with 5*/5\*\* isolating the top tail), aggregated across subjects into a JUPAS composite score that ranks candidates within a known cohort."

---

## 6. Other manuscript claims checked briefly

| Claim | Location | Verdict | Note |
|---|---|---|---|
| SDG 4 (universal secondary completion) adopted September 2015, after RA 10533 (2013) | June 20, 113 | **Consistent / not re-verified from UN primary** | SDG 4 adopted by UN General Assembly 25 Sep 2015; RA 10533 signed 15 May 2013. The ordering is not in doubt; the UN resolution was not fetched in this pass. |
| Philippines "one of three countries globally still operating" a 10-year cycle in 2013 | June 110 | **Unresolved** | No retrieved source enumerates the countries with 10-year basic cycles in 2013. Treat as needing a citation (UIS ISCED duration data would settle it: `SE.SEC.DURS`/`SE.PRM.DURS` exist in `data/wdi_4countries_long.csv`, but a *global* count of 10-year systems was not pulled). |
| Philippines K-10 → K-12 reform in 2013, "ten-year cycle to twelve" | Oct 8, June 105–118 | **Verified as policy fact; wording note** | RA 10533 (2013) added kindergarten and grades 11–12; Philippine usage "K-12" = K + 6 primary + 4 JHS + 2 SHS. "Extended a ten-year basic cycle to twelve" is acceptable shorthand but the total formal span is 13 years including kindergarten. |
| China 2021 Double Reduction policy suppressed for-profit tutoring | Oct 196 | **Policy fact, text not retrieved** | The MOE policy document was not fetched; no numeric claim attached, so nothing to verify numerically. If the paper quotes enrolment/tutoring magnitudes for China, they must come from CFPS/CEPS or MOE, not from this ledger — the ledger has **no China tutoring series**. |
| Cambodia Grade 9 transition examination as the gate | June 56 | **Not in data** | CLFS 2019 does not report transition or examination pass rates. Grade 9 exam policy is a regulatory fact (MoEYS), not something this pull verifies. |
| HK "multiple consequential sorting gates" | June 44 | Qualitative | Supported indirectly by EDB structure (S4–S6 160,833 students in 2025/26 vs post-secondary enrolment 354.7k, i.e. post-secondary capacity exceeds the senior-secondary cohort). |
| October paper's model outputs (e.g. "−4.1 to −3.7 at 6%", graduation-supply shock results) | Oct 296–306 | **Out of scope** | These are simulation outputs, not observations. Note only that the "6%" at Oct line 306 is a *model elasticity parameter*, not the Cambodia recollection — do not conflate the two in revision. |

---

## 7. What remains unresolved (hand these to `lead`)

1. **Philippine cohort-survival / DepEd administrative series** — blocked by HTTP 403 on `deped.gov.ph` and `psa.gov.ph` from this environment. Needed to decide between "four in ten" and "half" and to give the paper a genuine K-10 attrition figure.
2. **PSA FIES/APIS/LFS microdata** — same block. The October paper's household-side claims (income tiers, credential pay) cannot be verified from this pull.
3. **Bray & Lykins (2012) ADB book** — not retrievable; the 85% claim is traced to Kwo & Bray (2011) reporting a 2010 survey. Secondary citation unconfirmed.
4. **China gaokao/zhongkao registrations, youth unemployment (NBS new definition), Double Reduction text** — MOE English statistics portal is reachable and the 2024 enrolment table was extracted (`raw/china/moe_students_formal_2024.html`), but the examination-administration and policy pages were not fetched. No number was invented to fill the gap.
5. **"Phnom Penh ~6% of jobs" recollection** — no source found; CLFS urban degree share is 13.8%, so the recollection is not merely unverified but implausible as a Phnom Penh figure. Recommend retiring it.
