# Implementation and review record

18 November 2026. The new directory preserves V5. SPEC.md preceded the experiment batch. The requested gpt-6.1-terra agent reviewed the design, code, tests and analysis.

Corrections before the first batch included full-budget allocation, head appointees' ability to owe favors, immutable creditor and protection-provider IDs, pre-discharge relationship exposure, first-act risk sets, payment support restricted to a live relevant superior, removal of hidden shields from target scores, full supplier resets and unconfounded controls. The reviewer caught an editing error that had changed payment support in the no-replacement and zero-attraction arms. Complete-policy equality checks now verify those controls.

Thirteen grouped checks passed before the first 828-job batch. That batch exposed a serialization defect: the sum for a cohort's first-act risk became a NumPy integer after a departure. JSON could not export it, even though the numerical checks passed. The batch was stopped with exit status 130; its incomplete files under `results/runs` are excluded from the release. An explicit integer conversion fixes export without changing numerical behavior. A complete cohort-run export and stale-resume regression was added, bringing the passing groups to fourteen.

The restarted batch runs under `results_completed`, bound to a new source hash. All cohort event histories are exported. The peer review records the fix and found no blocker in the cohort analysis. The delivered results must be checked for full completion before release.

During execution the user supplied ccporg.org. Its methods and selected source links were inspected. CCPORG_ASSESSMENT.md documents usefulness and selection limits; a conservative evidence adapter rejects rumor, unverified, future-published and uncertain-end records. The source was not fitted to the model. Its source assessment is outside the fixed simulation input directory, so it does not alter the running experiment.
