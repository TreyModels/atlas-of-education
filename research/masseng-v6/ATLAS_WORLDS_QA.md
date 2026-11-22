# Atlas Worlds release QA — release blocked until every gate passes

## 1. Numbers

- [x] Every reported figure traces to a final result file or cited source. The paper, README, report and figures are generated from the final JSON outputs.
- [x] README, paper and figures regenerated from final outputs; all compared copies are byte-identical.
- [x] Twelve transcribed World Bank values spot-checked against the API: 12/12 passed within 0.0005; see `outputs/qa/world_bank_spotchecks.json`.
- [ ] CHED headcounts and DepEd transition figures checked against original sources. **DepEd passed:** 1,587,416 Grade 10 completers SY2016–17 and 1,481,103 Grade 11 entrants SY2017–18, 93.3%, reference year 2018. CHED server fetch failed; still open.
- [x] Tutoring citations separated and checked as far as the sources allow. Original Bray & Kwok 2003: S1–3 35.1%, S4–5 46.6%, S6–7 70.3%, overall 48.8%. Original Zhan, Bray, Wang, Lykins & Kwo paper (published 2013): Grade 9/S3 53.8%, Grade 12/S6 71.8%, overall 61.1%. Caritas 2010 is **73.5% overall** in that later paper; 85.5% is a **senior-secondary** figure traced only through Bray & Lykins 2012, with the Caritas original still unverified. Do not label 85% as the Caritas overall figure.

## 2. Honesty of claims

- [x] Losses reported before preference or interpretation in the report, README and new paper. R2 wins among rivals but loses to persistence.
- [x] Reporting language fixed to `not calibrated` or `illustrative` unless a stated criterion actually passes.
- [x] Test described as retrospective and inspected, not blind.
- [x] Protocol amendments: none. Computational continuation of an optimiser is recorded separately and is not a protocol amendment.
- [x] Recovery-test failures reported. `kappa` is **not identified** (60% within ±25%; required 80%). `b_h` meets the numerical rule but hits a bound in 15/20 replicates and is explicitly flagged as boundary recovery, not positive-mechanism evidence.

## 3. Bray's work

- [x] Bray 1996, *Counting the Full Cost*, original checked. It supports full-cost accounting and an equity argument for fee-free primary schooling, not blanket fee-free provision at every level. The manuscript no longer uses household payments as proof that demand originated independently of the state.
- [x] Bray 1999, *The Private Costs of Public Schooling*, original UNESCO full text checked. Takeo Grade 1–6 household-cost percentages and the 1996 rural/urban quintile table were verified; sample-specific figures are not presented as national administrative accounts.
- [x] Bray & Kwo 2013 original checked; it contains no Cambodia spending numbers.
- [x] Tutoring distinguishes remedial, enrichment/consolidation and examination preparation in the source-check notes.
- [x] Siem Reap tutoring study checked against the publisher's original article sections: Bray, Kobakhidze, Liu and Zhang (2016), with This Life Cambodia and a University of Hong Kong team; six schools; 81.9% of sampled students reported tutoring. Credit remains with the full team, not Bray alone.

## 4. Paper fixes

- [x] ASEAN timing corrected against ASEAN's own record: economic ministers August 2014, education ministers September 2014, labour ministers ad referendum through May 2015—all after RA 10533 (2013). Manuscripts now describe anticipated coordination costs, not compulsion by an already-endorsed AQRF.
- [x] No `half go abroad` claim; measured bachelor's-place outside-HK share remains 13–26%.
- [x] Completion discrepancy resolved as unlike indicators: 67% is QBEDP SHS **net enrolment** for SY2023–24; 73% is its rounded SHS **completion** baseline. UIS separately reports 72.6% upper-secondary completion for 2022. See `outputs/qa/completion_indicator_check.json`; do not average them.
- [x] China credential-floor sign checked: observed raw and cohort-adjusted changes are negative, while all three models predict positive changes and no 10–90% interval crosses zero. **FAIL:** these results are not support for the relational account. See `outputs/qa/credential_floor_china_check.json`.
- [x] Both original massification papers are restored unchanged in `manuscripts/original/`. The new Philippine paper is a separate results-led work.

## 5. Reproducibility

- [x] Fresh copy runs on the Mac: 35 tests passed in both original and fresh copies.
- [x] Results regenerate byte-identically: all 13 compared files match—six fits, scores, recovery, report, two figures, README and new paper. See `outputs/qa/fresh_copy_comparison.json`.
- [x] Final requirements, source hashes and output hashes recorded. See `requirements-v5.txt`, `outputs/qa/reproducibility_inputs.json` and `outputs/qa/final_output_hashes.json`.

## Current gate

**NOT READY.** All final computational and reproduction gates pass. CHED original-source access remains open, so no Atlas Worlds release is authorised by this document. Hong Kong has not been started.
