# OUTLINE / METHODS PLAN — five silent-failure bugs, evidence-first

**Record:** `research/records/2026-11-25-meta-science/`
**Branch:** `research/meta-science-silent-failures-2026-11-25` (additive; base `origin/main` @ `55732f4`)
**Author:** meta-science worker (task-4), 25 Nov 2026
**Status:** plan + receipt-verification protocol; article to follow in this same record.

This is a methods/forensics essay about **this repo's own failures**. It is not a re-analysis and makes no
substantive empirical claim. Its only object of study is the commit history: each reported defect must be
shown from a commit, a diff hunk or a file line, and every inferred statement must be labelled as inference.

---

## 1. What the piece argues (one paragraph)

The expensive failures in this repo were not crashes. They were runs that **completed, printed
plausible numbers, and passed** their own checks: a bootstrap that resampled but silently deleted
duplicates; a TWFE dummy matrix transposed; a pseudo-inverse that returned finite estimates for
non-identified contrasts; a driver that read the post-compaction roster and therefore reported zero
exits in every cell; a runner that called a script "PASS" because its process exited 0 while the
script's own decision rule said `PASS=False`. The common shape is that the **verdict object and the
failure object were different objects**, so nothing raised. Detection came from line-by-line external
audit, not from the test suites — and the durable repair was always the same: make the wrong state
*unrepresentable or loudly reported* (estimability guards, partition/sentinel assertions, separation of
"executed" from "passed", re-recorded results), and keep the retraction on the record.

## 2. The five bugs (working list; receipts to be verified per §4)

| # | short name | suggested receipts | status in plan |
|---|---|---|---|
| 1 | cluster-bootstrap multiplicity (DHS) | `3faeff3`, `93b882a`, `9e063bf` + corrected record | verified in commit history; article will quote old/new code |
| 2 | transposed TWFE design matrix (equation suite) | `0a91afb` + the eq03 transpose commit | **`0a91afb` verified; no eq03 TWFE-transpose commit found** — see §3 |
| 3 | `pinv` masking rank deficiency / empty-stratum & zero-variance false positives | `22c4bb8`, `test_full_system.py`, `test_guards.py`, 49→45 rows | verified |
| 4 | `e.kids['reason']` vs `e.exits` (universal 0/0/0 decomposition) | `219747a`, `4679ddb`, `3afac25`, `747be44` | verified |
| 5 | `returncode == 0` hiding `PASS=False` (`run_all.py`) | `93a351e` | verified |

## 3. Honest finding on the suggested receipt set (recorded before writing)

- The suggested **"eq03 TWFE transpose commit" does not exist** in the reachable history. `git log --all
  --oneline -- '*eq03*'` returns five commits; none touches a TWFE matrix. The only TWFE-transpose fix is in
  `eq09_identification.py` (`0a91afb`), and it is the *only* commit in the repo whose diff contains
  `np.tile`/`np.repeat` unit/time dummies (`git log --all -S'np.tile'`). The actual eq03 fix that exists is
  `aefade0` ("Part A patch"), which replaces a 1-D ρ grid with a 2-D (ρ, ω) CES grid — **not a transpose**.
  The task's phrasing appears to conflate the handoff's quarantine line ("equation-suite: quarantine
  eq03/04/05/07/09/10 until TWFE transpose, …", `MIGRATION_2026-11-25.md`, item 4) with an eq03-specific
  commit. The article will say this plainly and substitute `0a91afb` as the transpose receipt.
- One **internal inconsistency in the bug-1 corrected record** will also be reported, not smoothed: the
  record's table gives Africa-11 2-group ratio CI `[0.9987, 1.1403]` ("now includes 1.0 — verdict flips"),
  but that CI is from `corrected_reduction.py`; the same run's `estimate.py` bootstrap in the committed
  `run.log` gives `[1.0011, 1.1403]`, which excludes 1.0. Both are cited; the verdict-flip sentence is true
  for one implementation and not the other.
- An extra candidate from the Lead (gate dispatch `if kind=='bar' … else: # quota`) will be verified in the
  engine source before it is used; if it does not show what is claimed it will be omitted or labelled
  unverified.

## 4. Receipt-verification protocol (applies to every quoted item)

1. **Show, don't cite.** For each receipt: `git show <sha> --stat`, then the specific diff hunk, or
   `git show <sha>:<path>` for file content; record the path and the 1-based line numbers.
2. **Record the SHA in full** (short SHA in prose is allowed only when the full SHA is in `RECEIPTS.csv`).
3. **Record the before/after pair.** A fix is only evidence if the pre-fix text is also shown; the
   "before" state is `<sha>^` or a named earlier commit, stated explicitly.
4. **Separate quotation from inference.** Quoted code/numbers are inside quote blocks with a receipt id;
   derived claims (e.g. expected dropped bootstrap slots ≈ 1 − (1 − 1/n)^n) are labelled *recomputation*
   or *inference* and are not presented as repo evidence.
5. **Reconcile every number across records.** If a record, a log and a JSON disagree, report all three and
   say which is which; do not pick the convenient one.
6. **No commit-SHA invention, no paraphrase passed off as quotation.** If a suggested receipt is missing or
   shows something else, say so and substitute only a verified real one.
7. **Preserve retractions.** The original wrong diagnosis stays in the record; corrections are additive
   (the repo already works this way: `4679ddb`, `3afac25`, `d532478`).
8. **Push, don't rewrite.** Purely additive commits on the branch; no force-push; no history edits.

## 5. Per-bug schema (identical fields for all five)

| field | what it must contain |
|---|---|
| **Symptom** | what a user of the record would have seen — the numbers that were wrong, stated as they appeared |
| **Root cause** | the code-level defect, with the offending expression and its file:line |
| **Why silent** | the mechanism: no exception; plausible magnitudes; tests asserted the wrong object; exit code masked the verdict; rank deficiency produced small finite SEs; wrong object read |
| **Detection** | the audit/review step that caught it (external line audit; in-repo task audit; retraction-completeness pass), with the document that records the catch |
| **Receipt** | commit SHA(s), file path, diff hunk / line numbers (all verified per §4) |
| **Fix** | the corrected expression/behaviour, with its receipt |
| **Guard** | the regression test that now prevents it: file + test name, and whether it would have caught the original bug (stated honestly if partial) |
| **Lesson** | one generalisable sentence, tied to the taxonomy mode |

## 6. Taxonomy (working labels; article finalises)

- **T1 wrong-object / aliasing** — the code reports on a different object than the claim (bug 4; also the
  record-about-the-run vs the run).
- **T2 numerically-masked degeneracy** — `pinv`, rank deficiency, zero variance: finite numbers for
  non-identified quantities (bug 3).
- **T3 aggregation / multiplicity** — resampling that changes the estimand, duplicate-dropping, partition
  sums that should be 1 but are not asserted (bug 1; bug 3's empty-stratum `all([])`).
- **T4 control-flow / verdict masking** — process success (`returncode == 0`) standing in for the decision
  rule; `all([]) is True`; `else` branches silently absorbing unknown kinds (bug 5; bug 3; Lead's
  candidate if verified).
- **T5 provenance / retraction drift** — the record and the code diverge (results not re-recorded after a
  code fix; a wrong blame narrative that survives in audit text until superseded by an additive erratum;
  a record that says "provisional" and means it) (bugs 1, 2, 4).

## 7. Guards checklist (to be written as `GUARDS_CHECKLIST.md`)

Short, operational, each item tied to a bug above: partition sums asserted; sentinel assertions (all-−1,
all-zero, all-NaN) treated as failure, not data; rank/estimability checks before `pinv`; zero-variance
checks; verdict-vs-exit-code separation; mutation/negative controls (inject the defect, assert the guard
fires); receipt discipline (re-record after every fix; quote the before state; keep retractions additive).

## 8. Intended structure of the final article (`ARTICLE.md`, ~2,500–4,500 words)

1. **The problem** — silent failure in computational social-science pipelines; why "it ran" is not evidence.
2. **Method** — corpus = this repo's commit history; receipt protocol (§4); what counts as shown/inferred.
3. **Five cases** — one section each, same schema (§5); before/after hunks; the specific silent mechanism;
   what caught it; the guard that now pins it.
4. **Taxonomy** — T1–T5 (§6), with a table mapping each bug to its mode(s).
5. **What actually catches these things** — audit design: line-by-line external audit, mutation/negative
   controls, re-recorded outputs, retraction-completeness passes. Include the cases where the *retraction
   itself* needed a second pass (bug 4: engine-blame → driver-bug; bug 1: bootstrap vs interaction-set
   attribution).
6. **Limits** — a five-case convenience sample from one repo; no base rate, no causal claim about why the
   defects were introduced; authors' own account, checkable only against the commits.
7. **Recommendations** — the checklist as the practical residue.

## 9. Deliverables in this record

- `OUTLINE.md` (this file; committed first, alone)
- `ARTICLE.md` (~2,500–4,500 words)
- `RECEIPTS.csv` (bug, commit, file, hunk/line, claim)
- `GUARDS_CHECKLIST.md` (operational)
- `README.md` (what this record is, status, provenance, how to verify)

## 10. Status log

- 2026-11-25: OUTLINE committed; receipt verification in progress. No claims beyond §3 are asserted yet.
