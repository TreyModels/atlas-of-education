# Atlas Worlds release QA — release blocked until every gate passes

## 1. Numbers

- [ ] Every reported figure traces to a final result file or cited source. Final rival outputs are not yet complete.
- [ ] README and figures regenerated from final outputs. Generators are written; final outputs are pending.
- [x] Twelve transcribed World Bank values spot-checked against the API: 12/12 passed within 0.0005; see `outputs/qa/world_bank_spotchecks.json`.
- [ ] CHED headcounts and DepEd transition figures checked against original sources. **DepEd passed:** 1,587,416 Grade 10 completers SY2016–17 and 1,481,103 Grade 11 entrants SY2017–18, 93.3%, reference year 2018. CHED server fetch failed; still open.
- [x] Tutoring citations separated and checked as far as the sources allow. Original Bray & Kwok 2003: S1–3 35.1%, S4–5 46.6%, S6–7 70.3%, overall 48.8%. Original Zhan, Bray, Wang, Lykins & Kwo paper (published 2013): Grade 9/S3 53.8%, Grade 12/S6 71.8%, overall 61.1%. Caritas 2010 is **73.5% overall** in that later paper; 85.5% is a **senior-secondary** figure traced only through Bray & Lykins 2012, with the Caritas original still unverified. Do not label 85% as the Caritas overall figure.

## 2. Honesty of claims

- [ ] Losses reported before preference or interpretation. The generator does this; final scores are pending.
- [x] Reporting language fixed to `not calibrated` or `illustrative` unless a stated criterion actually passes.
- [x] Test described as retrospective and inspected, not blind.
- [x] Protocol amendments: none. Computational continuation of an optimiser is recorded separately and is not a protocol amendment.
- [ ] Recovery-test failures reported; unrecovered parameters labelled `not identified`. Recovery is pending.

## 3. Bray's work

- [x] Bray 1996, *Counting the Full Cost*, original checked. It supports full-cost accounting and an equity argument for fee-free primary schooling, not blanket fee-free provision at every level. The manuscript no longer uses household payments as proof that demand originated independently of the state.
- [x] Bray 1999, *The Private Costs of Public Schooling*, original UNESCO full text checked. Takeo Grade 1–6 household-cost percentages and the 1996 rural/urban quintile table were verified; sample-specific figures are not presented as national administrative accounts.
- [x] Bray & Kwo 2013 original checked; it contains no Cambodia spending numbers.
- [x] Tutoring distinguishes remedial, enrichment/consolidation and examination preparation in the source-check notes.
- [ ] Siem Reap tutoring study is credited to Bray, Kobakhidze, Liu and Zhang / their team; the original fetch returned 403, so original verification remains open.

## 4. Paper fixes

- [x] ASEAN timing corrected against ASEAN's own record: economic ministers August 2014, education ministers September 2014, labour ministers ad referendum through May 2015—all after RA 10533 (2013). Manuscripts now describe anticipated coordination costs, not compulsion by an already-endorsed AQRF.
- [x] No `half go abroad` claim; measured bachelor's-place outside-HK share remains 13–26%.
- [x] Completion discrepancy resolved as unlike indicators: 67% is QBEDP SHS **net enrolment** for SY2023–24; 73% is its rounded SHS **completion** baseline. UIS separately reports 72.6% upper-secondary completion for 2022. See `outputs/qa/completion_indicator_check.json`; do not average them.
- [x] China credential-floor sign checked: observed raw and cohort-adjusted changes are negative, while all three models predict positive changes and no 10–90% interval crosses zero. **FAIL:** these results are not support for the relational account. See `outputs/qa/credential_floor_china_check.json`.

## 5. Reproducibility

- [ ] Fresh copy runs on the Mac.
- [x] Current model test directory passes: 34 passed. A repository-wide pytest collection also collects the stand-alone `scripts/recovery_test.py` and fails for missing CLI arguments; the supported command is `python -m pytest -q tests`.
- [ ] Results regenerate byte-identically, with hashes compared.
- [ ] Final requirements and code hashes recorded. Exact requirements and the generator are present; final hashes await final outputs.

## Current gate

**NOT READY.** R4 and the computational continuation of R1 are running; scoring, recovery, final figure generation and fresh-copy reproduction remain incomplete. CHED and Siem Reap original-source access are still open. No Atlas Worlds release is authorised by this document.
