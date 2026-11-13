# 02 · Verify an input

**Goal.** Turn a number that was entered from memory into one of: verified against a fetched source (`v`), derived
from a recorded calculation (`d`), dropped because it is an assumption rather than an observation, or still
unverified (`m`). Keep the evidence and the code consistent, and say honestly what could not be checked.

**Use it when** a data file carries an `m` flag, when you are correcting a value in `engine/firms/data_china.py`,
or when a paper's number is challenged. The worked example is `docs/china_input_verification.md`: the 6 November
2026 audit that closed every remaining `m` flag in the China inputs. It is 344 lines long — read its §1, §2, §4 and
§5 before starting your own; the recipe below is the reusable part.

**You need.** The data file (usually `engine/firms/data_china.py`), a browser or `curl` with internet, the
existing source notes, and the acceptance test. `requests`-style scripting is not required: this is a reading job.

## The flags, in one sentence each

The convention is declared at the top of `engine/firms/data_china.py` and is the same one
`engine/impute/panel.py` uses for every country-year panel:

- `v` — verified this session against a page named in `SOURCES`.
- `m` — entered from memory of an official release, not verified this session.
- `d` — derived by a transformation or imputation, not observed (record the formula).
- `''` — missing (panels only; there is no number).

A flag records *how the number was checked*, not how confident a search result makes you feel.

## Steps

1. **List the flags.** Open the data file and find where its provenance is declared:

   ```bash
   grep -n "_FLAG" engine/firms/data_china.py
   ```

   Expect the four flag dicts — `GRAD_FLAG` and `TERTIARY_FLAG` all `v`, `BIRTHS_FLAG` all `d`,
   `PROPERTY_FLAG` all `v` — with no `'m'` values left in the China series: the 6 November 2026 audit closed
   them all. (The letter `m` still appears in the file's legend and in `urban()`'s fallback return for a month
   outside `_URB_CHECKED`; that is the convention, not an unchecked value. `tests/test_evidence.py` enforces the
   claim.) For other files, list the series and start with one series, not one value.

2. **Copy the audit table shape.** Work one series per table with these columns, exactly as in
   `docs/china_input_verification.md` §2: series, year, month, current value, verified value, recommended flag,
   source institution and release date, URL, quote, status. One row per value. The quote is not decoration: it is
   what lets a reviewer check you without re-doing the search.

3. **Find the primary page first.** Prefer the issuing institution over any aggregator or news summary: the
   Ministry of Education's annual 全国教育事业发展统计公报 for entrants, NBS yearbook tables for births, NBS release
   pages for unemployment. Open the page (browser, or `curl -L <url>`) and read the sentence that contains the
   number. Record the URL you actually opened and the date; a URL copied from an older audit is not evidence.

4. **When the primary page cannot be fetched, use the two-transcription rule and say so.** The China urban series
   is the example: `data.stats.gov.cn` returned HTTP 403 (a WAF block) from the audit session, so the values were
   confirmed against *two independent transcriptions of the same NBS series* that agree on all 53 overlapping
   months — a Wikipedia table citing NBS National Data, and 聚汇数据/gotohui citing 国家统计局, the latter also
   giving the unrounded values (2018-01 4.96 published as 5.0). Key months were additionally anchored by
   contemporaneous release reports (央广网 2018-04-17 and 2020-03-16; 中国经济周刊 2020-03-30). Put both evidence
   kinds in `SOURCES` and say in the audit that the primary database was unreachable — do not describe a
   transcription as if you had read the NBS page.

5. **Decide the flag before touching code.**
   - Confirmed from a fetched page, or from agreeing transcriptions plus anchors → `v`.
   - Computed from published components → `d`, with the formula in the file. Example: births are not published
     annual counts; they are `birth_rate_per_thousand × mean(year-end population, previous year-end population)
     / 1000 / 100`, so `BIRTHS_FLAG` is `d`.
   - Not observed at all (a scenario assumption, a forward projection) → drop it from observations. Example: 2026
     tertiary entrants 10.8m had no MoE source and was dropped on 5 November 2026.
   - Could not be confirmed → leave `m` and record why.
   - Do not mix conventions inside one series. The 2021 tertiary entrants case: the published 2021 total 552.58万
     **includes** 45.20万 five-year-vocational transfers, while the 2019–20 communiqués report them separately
     ("另有…") and the 2022–24 ones say "不含". The series strips them:
     444.60 + 4.14 + (552.58 − 45.20) = 956.12万 = 9.56m. Record that convention in the file.

6. **Write the audit doc before editing code.** Put the tables, the proposed change set and a "what worked / what
   did not" section in `docs/`. The China example puts a machine-readable JSON block in §3 and marks the doc
   "audit only, no code edited by the verifier"; a second lane applies it. That separation is deliberate: the person
   who verifies the source is not the person who changes the calibrated model, and the change set can be reviewed
   line by line.

7. **Apply the change set narrowly.** Change only the values and flags in `engine/firms/data_china.py`; add or
   extend the `SOURCES` entry with the URL, the source institution and what was and was not fetched. Then lock the
   check into the file where drift is possible. The pattern already there:

   ```python
   _URB_CHECKED = {(y, m + 1): v for y, row in _URB_M.items() for m, v in enumerate(row)}
   for (_y, _m), _v in _URB_CHECKED.items():
       assert _URB_M[_y][_m - 1] == _v, ('remembered urban rate contradicts the verified series', _y, _m, _URB_M[_y][_m - 1], _v)
   ```

   Add a test for each move in `tests/test_evidence.py`, named after the number, e.g.
   `test_2023_01_urban_is_the_corrected_5_5`, `test_births_are_flagged_derived_and_the_rate_series_is_present`.
   Tests that guard inputs belong there, not in the fit tests.

8. **Run the acceptance checks.**

   ```bash
   python tests/test_evidence.py          # 11 tests, fast
   cd engine && python -c "import firms.data_china as D; print(len(D._URB_CHECKED), D.urban(2023, 1))"
   # expected: 55 (5.5, 'v')
   ```

   Then `python run_all.py` from the project root and confirm every step passes. The import-time assert fails the
   import, so a contradicting value cannot hide from any script that reads the data.

9. **Record the before/after headline results.** The quick run does not refit: `RUN_REPORT.md`'s headline numbers
   come from the stored fits in `engine/firms/results/`, so they will not move merely because an input changed.
   Refits happen in `--full` or in the individual fitting scripts. Save the old report (or copy the results folder,
   as `engine/firms/results/before_input_fix/` does) and after the refit state, in the audit, which numbers moved
   and by how much. Provenance repair does not license silently changing calibrated conclusions.

10. **Write down what did not work.** The China audit's §4 is the model: `data.stats.gov.cn` HTTP 403 with
    `reason:UrlACL`; `ycharts.com` HTTP 202 with an empty body; old `moe.gov.cn` `jyb_xwfb` paths returning 404
    (use `https://` and follow redirects); JS-driven monthly-release listings that could not be read economically.
    The next person should not repeat that search. Never paste an un-fetched URL into `SOURCES` as though it had
    been read.

## Checks

- `python tests/test_evidence.py` passes, and the new test names describe the values they guard.
- `python run_all.py` is all pass.
- Every remaining `m` in the targeted series has a reason in the audit; every removed value's removal is explained.
- `SOURCES` contains what was actually read, with dates, and distinguishes fetched pages from transcriptions.

## Common failures (all seen in the China audit)

- **A supplied audit is not a verified audit.** The 5 November pass rejected two of the supplied corrections
  (January 2025 urban stays 5.2, April 2025 stays 5.1), and the 6 November pass found an adjacent error in an
  already-`v` value (2023-01 was 5.6; NBS says 5.5). Re-fetch before applying.
- **Rounding trap.** February 2020 was "up 1 point" from January in an English report, implying 5.2; the Chinese
  reports say 6.2% with January at 5.3% and "环比上升0.9个百分点". 5.3 is correct. One-decimal publication versus
  unrounded aggregator values is the same trap (4.96 → 5.0).
- **Announced versus realised.** `GRADUATES` is the graduating-class scale *announced for employment planning*
  ("全国普通高校毕业生人数"), not realised regular-HEI graduates from the education communiqués (2008: 5.59 announced
  vs 5.12 realised). Renaming the series without changing the definition, or the reverse, is a silent break.
- **Derived values described as observations.** Births are reconstructed from a birth rate and adjacent year-end
  populations; call them NBS-derived and keep `d`, and keep the formula in the file.
- **A series with a convention break.** The 2021 tertiary-entrant correction exists because one year's published
  total includes five-year vocational transfers and the rest exclude them. Fixing one year is right; mixing the
  two conventions is not.
- **Editing the code and the audit in separate sessions without a saved before/after.** Then nobody can say which
  headline number moved. Save the report first.
