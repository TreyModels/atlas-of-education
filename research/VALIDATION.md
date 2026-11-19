# Verification record, 16 November 2026

These checks verify implementation and execution. They provide no external validation of the social explanations.

| Check | Result |
|---|---|
| Python known-answer and design tests | 11 passed |
| Node checks for indexed pairing, grouping, applicant stocks and climate-summary provenance | 5 passed |
| Existing world suite | 52 passed |
| Translation coverage/language-switch checks | Passed |
| Small common-runner batch | 57 of 57 succeeded across seven families; no pending or failed trials; source integrity matched at completion |
| Resume of that completed batch | All 57 trials reused from cache; source integrity matched |
| TypeScript/Vite production build | Passed; existing font-resolution and bundle-size warnings remain |
| Built worker checks | All 22 default models, three changed inputs, CSV views and error path passed |
| Python compilation and patch whitespace | Passed |
| Strict React translation audit | Fails on inherited missing translation entries: 82 Vietnamese and 177 French entries in both the baseline and revised dictionaries. No new missing language entries were introduced; new catalogue strings were translated |
| Out-of-Africa execution | Deferred: numba is absent from the review environment. Adapter syntax was compiled; companion code and grid are included for local execution |
| Production batches and new SMC calibration | Unrun; commissioning and interpretation remain local work |

The last monsoon change prevents a rounded sensitivity from borrowing a stored summary. Its known-answer tests passed after that change. No production numerical tables were regenerated. The ZIP omits dependencies, build products, local run outputs and Git metadata. Its package manifest records the delivered source and data bytes.
