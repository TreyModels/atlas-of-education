# GUARDS CHECKLIST — reusable, operational

Short list for any computational pipeline whose output feeds a written claim. Each item names the failure it
prevents and the case in `ARTICLE.md` that motivates it. Apply at the point where the object is created, not at
the end of the pipeline.

## 1. Partition and category sums
- [ ] If a set of categories should exhaust a population, assert `sum(shares) == 1` (tolerance explicit).
- [ ] Assert counts add up: survivors + exits = population; group counts = total.
- [ ] Name every sentinel value (`-1 = censored`, `-1 = not exited`) as a category; never let a sentinel double as
      "missing". *(Case 4: the driver read a roster whose `reason` was all `-1` and reported 0/0/0.)*

## 2. Sentinels and degenerate inputs
- [ ] Treat all-equal, all-zero, all-NaN, and all-sentinel arrays as **failure states**, not data. A zero-variance
      outcome must be reported `not_estimable`, never "supported with p=0". *(Case 3.)*
- [ ] Assert the expected sign/shape of the input before the estimator sees it (e.g. at least one positive exit
      reason; at least two countries; more rows than parameters).

## 3. Rank and estimability
- [ ] Before any pseudo-inverse, compute the numerical rank of the design (SVD, explicit relative tolerance) and
      the row space.
- [ ] For every reported contrast, test that the contrast vector lies in the row space; if not, report
      `not_estimable` and do not report a number, an SE, or a p-value. *(Case 3: `pinv` returned finite estimates
      and tiny SEs for directions the data could not identify.)*
- [ ] Check the outcome-specific design, not only the full design: collinearity can appear only for some outcomes.

## 4. Verdict vs exit code
- [ ] A script's PASS/FAIL is its **own decision rule**, read from its output, not its process exit code.
- [ ] Have a distinct `NO_RULE` / "no verdict" state; a missing or unreadable rule must fail, never default to
      pass.
- [ ] Aggregate runners must count `decision_rule_failures` separately from `execution_failures`. *(Case 5:
      `returncode == 0` hidden behind `PASS=False`.)*
- [ ] Any `if kind == ... else: ...` dispatch must reject unknown kinds explicitly; an `else` that silently
      implements a default is the same defect in miniature. *(Section 9, latent.)*

## 5. Resampling and multiplicity
- [ ] A bootstrap/resampling routine must assert how duplicates are handled; a de-duplicating membership filter
      changes the estimand. Replicate weights/multiplicities explicitly. *(Case 1.)*
- [ ] Report the resampling distribution's effective composition (distinct units, dropped slots) next to the CI.
- [ ] Do not use the point estimate as evidence that a resampling fix worked — resampling fixes cannot move point
      estimates; check the interval.

## 6. Wrong-object / aliasing
- [ ] For every "population" or "total" read, assert you are reading the live set **and** the archive (or only the
      archive, deliberately), and say which.
- [ ] Prefer an accessor that rebuilds the claimed object (e.g. `aggregate_exits`) over direct field access; test
      the accessor against the field it replaces. *(Case 4.)*
- [ ] Delete or rename fields that are known-empty after a lifecycle event, or expose a guard (`if all(reason ==
      -1): raise`).

## 7. Mutation / negative controls
- [ ] Every guard gets a test that injects the **defect shape** it is supposed to catch (rank-deficient arm,
      zero-variance outcome, empty stratum, all-sentinel roster) and asserts the guard fires. Happy-path tests do
      not test guards. *(Case 3: `test_guards.py` integration check; Case 4: `test_exit_reason.py`.)*
- [ ] Run each new guard against the pre-fix implementation; it must fail (or error), not pass.

## 8. Re-record and provenance
- [ ] After a code fix, regenerate and re-commit every output the record quotes; a code fix is not a record fix.
      *(Case 2.)*
- [ ] Pin quotes to `<commit>:<path>:<line(s)>`; keep the before state in the record.
- [ ] When a claim is retracted, publish the retraction where the claim was published (report, audit, handoff,
      JSON), preserve the old text, and use an additive commit. Expect more than one pass. *(Case 4: engine-blame →
      driver-bug → erratum.)*
- [ ] Re-read quarantine lists as **bundles**, not per-item citations; a bundle names one script per fix, not
      necessarily the right script. *(Section 8: "eq03 TWFE transpose" does not exist; the transpose was eq09.)*
- [ ] Reconcile every number across report/log/JSON; where two implementations disagree at a decision boundary
      (e.g. a CI including vs excluding 1.0), report both and label the verdict implementation-dependent.

## 9. Review protocol (the step that actually caught these)
- [ ] Line-by-line external audit of the estimator code against the claim, not just a re-run.
- [ ] Re-derive one number by hand/independently per estimator; agreement between two implementations that share
      the same wrong line is not verification.
- [ ] Audit the record as well as the code: does each sentence still denote the same fact as its source?

---

**One sentence:** make the wrong state unrepresentable or loudly reported — and put the guard where the wrong
object is created, not where the claim is written.
