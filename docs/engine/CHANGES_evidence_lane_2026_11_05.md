# Change list: China and cross-country evidence lane, 5 November 2026

Scope: verify memory-flagged China inputs against fetched sources; get age-aligned survey evidence for the India and Kyrgyzstan school/work tests; keep links and unresolved discrepancies; run the tests. Cambodia financing and child-labour code (`camchild*`, ridge, ledgers) were not touched.

## Result in three lines

1. **India, retested on one survey and matching age bands, still fails**, but for a different reason than the first round said. Matched only on out-of-school (7–14: 3.4%, 15–17: 16.6%), the model predicts 31% of children combining school and work [8–68]; the survey has 0.4%. It reproduces India only in a corner (110 of 100,000 worlds at three times the tolerance) where work around school is almost shut, and then the composition test is weak (a range 87 points wide).
2. **Kyrgyzstan cannot be tested as a point prediction** with what could be retrieved. The first-round "pass" is withdrawn: it rested on an 18.0% child-labour figure that MICS6 does not contain (MICS6 gives 26.7% for 5–17 on a broader definition that includes chores), and the DOL's 38.4% has no definition.
3. **China:** one more graduate year (2020), seven urban-unemployment months and one tertiary-entrants year are now verified against fetched pages; one remembered value (January 2020 urban, 5.3) conflicts with its source's implied 5.2 and stays flagged. No value was changed, so no stored China result needs a rerun.

## Files changed

| File | Change |
|---|---|
| `engine/childworld.py` | `simulate` also returns age-banded outputs: `oos_7_14`, `oos_15_17`, `neither_share_oos_7_14`, `neither_share_oos_15_17`, `both_7_14`, `both_15_17`. They consume no random numbers: the stored 20,000-world results (`childworld_mc_v1/v2.{json,md}`) were rerun and are byte-identical. |
| `engine/data/asia_school_work.json` | New `age_aligned` block for India (PLFS 2018/19 bands 6–17, 6–10, 7–14, 15–17; derived out-of-school; page numbers and link) and Kyrgyzstan (out-of-school by level; broad child-labour figure; list of unresolved items). Old fields untouched. |
| `engine/childworld_agealigned.py` (new) | Age-aligned tests. India specification 1 (match 7–14 and 15–17 out-of-school) and specification 2 (also match school-and-work, tolerance ladder ×1, ×2, ×3); Kyrgyzstan matched on out-of-school by level and compared with the broad survey figures as upper bounds. `--report-only` rebuilds the report from the stored JSON. |
| `engine/results/childworld_agealigned.{json,md}` (new) | 100,000 worlds, priors v1, master seed 7. |
| `engine/firms/data_china.py` | `_URB_CHECKED` (7 months, asserted equal to the remembered values at import; `urban()` returns `'v'` for them); `GRAD_FLAG[2020]` now `'v'`; `TERTIARY_FLAG` (2022 `'v'`); `BIRTH_RATE_PERMILLE` (verified yearbook rates, 1990–2010, as a cross-check); source links in comments. **No series value changed.** |
| `tests/test_evidence.py` (new, 11 tests) | Survey rows add to 100%; derived out-of-school equals work-only plus neither; unresolved items kept; age-banded outputs are proportions; checked China months equal remembered values and are flagged `v`; January 2020 stays `m`; 2020 graduates `v`, 2008–18 still `m`; 2022 entrants within 0.011 of the bulletin sum; births stay `m`; stored result structure. |
| `run_all.py` | New step for `tests/test_evidence.py`; `--full` step for `childworld_agealigned.py --worlds 100000` (about 5 minutes). |
| `docs/asia_school_work.md` | Tests section rewritten: first-round verdicts marked superseded, age-aligned round added, unresolved list, next structure to try, new sources. The old "Why India fails" paragraph is replaced. |
| `TODO.md` | Cross-country stage 1 updated; new P1 item for the remaining survey inputs; the `m`-flag item updated with this pass. |
| `docs/CHANGES_evidence_lane_2026_11_05.md` (this file) | |

If the other context also edited `run_all.py` or `TODO.md`, merge by hand: my edits are one inserted line in the default steps, one in the `--full` steps, and the two TODO paragraphs named above.

## Checks run

`python run_all.py`: all steps pass (firms 31 tests, validation 9, childworld 5, Monte Carlo manager 15, evidence 11, node parity and camchild suites, round 8). Stored childworld Monte Carlo results reproduce byte for byte. The `--full` steps were not rerun because no China value changed.

## Verified this pass (source, what it showed)

| Item | Value | Source |
|---|---|---|
| India activity status by age band, PLFS 2018/19 | table in `docs/asia_school_work.md` | UNICEF Innocenti, *Child Labour and Schooling in India: A reappraisal* (2024), Table 7 p. 34, overall table p. 32: https://www.unicef.org/innocenti/media/9356/file/UNICEF-Innocenti-Child-labour-schooling-India-Report-2024.pdf |
| Kyrgyz out-of-school by level (MICS6 2018) | primary 1.0, lower secondary 1.4, upper secondary 11.4 | UNICEF Kyrgyzstan snapshots: https://www.unicef.org/kyrgyzstan/media/6066/file/MICSStatisticalSnapshots.pdf |
| Kyrgyz child labour 5–17 (MICS6) | 26.7% (thresholds include 28+ hours of chores and hazardous work) | same |
| Kyrgyz DOL table | 34.0% working (5–14), 94.7% attending (5–14), 38.4% combining (7–14), no definition | https://www.dol.gov/sites/dolgov/files/ILAB/child_labor_reports/tda2020/Kyrgyz-Republic.pdf |
| Urban unemployment 2020-02 = 6.2 | | Xinhua/China Daily 17 Mar 2020: https://govt.chinadaily.com.cn/s/202003/17/WS5e7048b2498ea01b9aea1a7a/chinas-job-market-remains-generally-stable-in-february.html |
| Urban unemployment 2020-12 = 5.2 | | Yicai Global 18 Jan 2021: https://yicaiglobal.com/news/china-unemployment-rate-stayed-at-52-in-december |
| Urban unemployment 2022-04 6.1, 05 5.9, 06 5.5, 07 5.4 | | NBS spokesperson, Global Times 15 Aug 2022: https://globaltimes.cn/page/202208/1272999.shtml |
| Urban unemployment 2022-03 = 5.8 (derived: April 6.1 "up 0.3") | | Global Times 16 May 2022: https://globaltimes.cn/page/202205/1265776.shtml |
| Graduates 2020 = 8.74 million | | Ministry of Education (Wang Hui), China News Service 28 Sep 2020: https://www.chinanews.com/gn/2020/09-28/9302046.shtml |
| Tertiary entrants 2022 ≈ 10.15 million (467.94 + 7.63 + 538.98 ten-thousand) | held 10.14 | MoE 2022 statistical bulletin, 5 Jul 2023: https://www.gov.cn/lianbo/bumen/202307/content_6890116.htm |
| Birth rate per thousand, 1990–2010 | e.g. 21.06, 14.03, 11.90 | NBS yearbook 2011 table 3-2: https://www.stats.gov.cn/sj/ndsj/2011/html/D0302e.htm |

## Unresolved discrepancies and gaps (nothing below was filled from memory)

- **Urban January 2020:** held at 5.3, flagged `m`. The February article calls 6.2 "up 1 point from the previous month", which implies 5.2. Possibly no separate January release; not confirmed.
- **Tertiary entrants 2022:** the three bulletin components sum to 10.15 million against 10.14 held; the bulletin also excludes 54.29 ten-thousand five-year vocational transfers. Left as is.
- **Births:** the source fetched gives rates, not counts; the population table was not on the fetch allowlist. Counts stay `m`.
- **Still `m`:** urban 2018–19, 2020 (other than Feb and Dec), 2021, 2022 January/February; graduate classes 2008–18; tertiary entrants other than 2022. The NBS monthly release pages themselves were not retrievable (the fetched archive pages were headline-only), so the urban checks rest on Xinhua, China Daily, Yicai and Global Times reporting of NBS releases.
- **Kyrgyzstan:** the 38.4% has no definition or stated denominator; MICS6 tables PR3.1–PR3.3 (child labour by age and attendance) and the final report file could not be fetched; the snapshot's attending vs not-attending split is in unlabelled bars and was not used; school-level age bands follow the national system; the 18.0% child-labour figure used in the first round is not in MICS6.
- **India:** whether the 0.4% school-and-work counts principal status only (which would undercount working students) is unchecked; the same report gives different numbers for the 2011/12 survey (0.6% and 10.7% out of school), so cross-survey comparisons are unreliable; the PLFS 2023–24 has only a secondary-source count (20.07 million aged 14–18 not attending). The PLFS microdata could not be tabulated here.
- **Order of results:** the age-aligned India specification 2 uses tolerances three times larger than specification 1 to find any world at all. Treat its pass as weak.

## Next

1. Fetch or be given the Kyrgyz MICS6 final-report tables (PR3.x, TC) and the PLFS 2018/19 microdata tabulation by age and principal/subsidiary status.
2. Build the rival structure with a shared time budget for school and work, and run the same age-aligned tests on it.
3. Verify the remaining `m` China series from NBS pages Trey can open or paste; any value that changes needs the affected `--full` steps rerun.
