# DRAFT — Five silent failures: when the pipeline runs, the numbers look plausible, and the check says yes

**Methods draft, 25 Nov 2026.** Evidence: `research/records/2026-11-25-meta-science/` (branch
`research/meta-science-silent-failures-2026-11-25` @ `de3821e`; confirmatory essay `01f9e45`, receipt-drift audit
`de3821e`, pre-registrations `5b93a41` / `f474e23`). Every quoted commit, file and line was verified with
`git show`; receipts are in `RECEIPTS.csv` (38 rows) and `results/receipt_audit.csv` (46 rows).

## Abstract

We study five defects in an education-research repository that did not crash anything. Each pipeline ran to
completion, wrote finite numbers, and left a check that said yes. The numbers were wrong in ways that mattered:
an interval that was too narrow, a fixed-effects matrix with unit and time dummies swapped, finite estimates for
contrasts the data could not identify, an all-zero exit decomposition in every run, and a runner that called a
script "PASS" because its process exited zero even when the script's own rule said `PASS=False`. The common
structure is a **mismatch between the object the code observes and the object the claim is about**: the bootstrap
observes a de-duplicated resample; the regression a permuted dummy set; the pseudo-inverse the column space but
not the contrast; the driver the post-compaction roster; the runner the process exit code. Detection, in all five
cases, came from line-by-line review of code and records, not from the tests in place. A sixth finding shows how
such bug lists decay: a correct quarantine list, quoted downstream, **coalesced into a citation of a commit that
does not exist**. A follow-up audit of two handoff documents found receipt *existence* clean but receipt
*content* drifted in 8 of 46 assertions (17%).

## 1. Method: the commit history as the receipt trail

The corpus is the repository's own history. The protocol was fixed before any claim (`OUTLINE.md`, `5b93a41`):
show the **before state** (`<sha>^`) as well as the fix; **quote the hunk** pinned to `<commit>:<path>:<line>`;
label derived statements *recomputation*, not quotation; **reconcile** report/log/JSON disagreements; **preserve
retractions** as additive commits; and **report missing receipts** when a suggested commit does not exist.
Receipts are pinned to commits, not branches.

## 2. The five cases

1. **The bootstrap that deleted its own duplicates (DHS).** A country-cluster bootstrap resampled countries with
   replacement and then filtered the panel by membership (`estimate.py` @ `3faeff3^`:146–148:
   `samp = list(rng.choice(common, …, replace=True))`; `ra = [r for r in pa if r["country"] in samp]`), keeping
   each country **at most once**. Multiplicities were discarded, so the quantity was a subsampling bootstrap over
   distinct countries; ~36.5–36.6% of resampled slots were dropped and intervals were too narrow. *Silent
   because* the estimator still ran and intervals were finite and plausible; the fix by construction cannot move
   a point estimate. Fix: expand the resample by multiplicity (`Counter`/`_expand`), `3faeff3`, `93b882a`;
   separation of "CIs only" vs "interaction set" recorded later at `9e063bf`.
2. **The transposed TWFE matrix (equation suite).** `eq09` built unit dummies with `np.tile` and time dummies
   with `np.repeat` — swapped. Finite, plausible coefficients, wrong fixed effects. Fix `0a91afb` swaps
   `tile`/`repeat`, moves 2SLS residuals to the actual D, and uses `σ² = Σe²/(n−k)`; the old numbers remained
   committed until re-recorded at `d575bfe`. *Silent because* the design matrix was still full-rank and the
   regression produced ordinary-looking output.
3. **`pinv`, empty strata, and zero variance.** The full-system test screen used a pseudo-inverse that masked
   rank deficiency, `all([])` returning True on empty strata, and zero-variance false positives — producing
   "supported" verdicts the data could not support. Fix `22c4bb8` added rank/estimability guards; the supported
   set fell **49 → 45**, with exactly four rows moved to `not_estimable` (supply→formal_share_gdp, learning→
   tut_rate ×2, jobs→skill_premium). *Silent because* a pseudo-inverse always returns a number and the tests
   asserted the wrong object.
4. **The emptied roster (exit reason 0/0/0).** The engine compacts exited children out of `e.kids` each step
   (`core.py`:444–447, `keep = k['reason'] < 0`; archive `self.X = concatenate(exits)`); the driver read
   `e.kids['reason']` after `run()`, getting all −1, so the exit-reason decomposition was 0/0/0 in **every** run.
   Retracted at `4679ddb` / `3afac25`; fixed driver at `219747a` reads `e.exits`. *Silent because* the
   decomposition was well-formed and plausible; the engine was actually correct.
5. **`returncode == 0` hiding `PASS=False`.** `run_all.py` (`93a351e^`) set
   `status = "PASS" if p.returncode == 0 else "FAIL"`, so a script that ran and decided `PASS=False` was
   reported PASS. Fix `93a351e` parses the script's own `decision_rule.PASS` and adds a `NO_RULE` state;
   re-recorded `run_all.json` @ `d575bfe` shows three `RULE_FAIL` rows with `returncode = 0`.

## 3. The sixth finding: receipt coalescence

The handoff at `MIGRATION_2026-11-25.md` @ `354f7c0`:57–59 bundled "quarantine eq03/04/05/07/09/10 until TWFE
transpose". Downstream, the TWFE transpose was cited as an **eq03** fix. It is not: `git log --all -- '*eq03*'`
(5 commits) touches no transposed dummy matrix; the transpose is `eq09` (`0a91afb`), and eq03's real fix is
`aefade0` (a 2-D (ρ, ω) CES grid). The receipt exists; the claim attached to it drifted. **A targeted audit**
(`de3821e`) of the two handoff documents found 46 assertions: **38 VERIFIED, 5 COALESCED, 1 WRONG-COMMIT,
2 MISSING**. Existence is clean (all 20 MIGRATION branches and all 4 NEON fix branches exist; tests re-run ALL
PASS); drift is in the claims layer — a stale head off by one commit, a wrong-object description (`e.exits` vs
`e.kids` in the handoff prose itself), a "point estimates unchanged" sentence that contradicts its own
−0.0775 → −0.1962, an implementation-dependent "now includes 1.0", a renumbering of quarantine items between
documents, and two numbers with no committed per-cell receipt.

## 4. Taxonomy and guards

- **T1 wrong-object/aliasing** (bootstraps, rosters): assert the identity and cardinality of the object read.
- **T2 numerically-masked degeneracy** (pinv, zero variance): rank/estimability guards; `pinv` never errors.
- **T3 aggregation/multiplicity** (clustered resampling): test the resample's multiplicity, not membership.
- **T4 control-flow/verdict masking** (returncode, empty strata): separate the program verdict from the process
  status; explicit `NO_RULE`/`not_estimable` states.
- **T5 provenance/retraction drift** (coalesced receipts): cite commit+path+line, re-verify before quoting, and
  keep retractions additive and visible.

`GUARDS_CHECKLIST.md` lists nine operational checks (partition sums, sentinel assertions, rank checks,
verdict-vs-exit-code separation, mutation/negative controls, receipt discipline, etc.).

## 5. Limits

This is a forensic case series, not a base rate. Detection came from review, and the audit is post-hoc and
targeted to two documents; 17% drift is not a population estimate. Two quarantine sub-rows were verified only to
object existence. One cited "local-only" branch lives in a different Git repository and was not inspected per the
no-touch rule. The article states real guard gaps for cases 1, 2 and 5.

## 6. What caught them

Not the test suites then in place: line-by-line review of code and records against claims. The repairs share a
shape — make the wrong state impossible to represent or loudly labelled (estimability guards, partition and
sentinel assertions, explicit verdict categories, re-recorded outputs). The sixth finding adds the corollary:
**a bug list is itself a data structure that decays**, and receipts must be re-verified, not inherited.
