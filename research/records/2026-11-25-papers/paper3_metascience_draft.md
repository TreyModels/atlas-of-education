# Silent failures in an AI-assisted social-science pipeline: a forensic audit with commit receipts

**Draft — comment / perspective length.** Target venues: *Nature* Comment, *PNAS* Perspective,
*Sociological Methods & Research*. This is a single-programme forensic report, not a survey; no external
citations are used in this draft, and no generalisation beyond the case is claimed. Every number below is
traceable to a branch and commit, or to the QA gate file `~/neon-boot/QA_GATE_2026-11-25.md`.

## 1. The phenomenon: a green pipeline with wrong verdicts

Between 20 and 25 November 2026 a research programme built a full-system simulation
(`eduengine`), an equation inventory suite, an ecological DHS replication, a micro-data pipeline and a
multiverse of design choices, using AI agents as the principal implementation and audit labour. At the
final gate the programme held **16 tracked branch heads** — model, data, tests, handoff — and its software
signals were, by the ordinary standards of research engineering, excellent:

- every suite script **executed** (10/10, `returncode 0`; one component's fit-readiness protocol reported
  **all 34 tests passing**, `research/masseng-v6/FIT_READINESS.md`);
- every multiverse row was written, every JSON parsed, every output hash recorded
  (`results/run_all_manifest.csv`, box-runs lockfile with 128 packages and 40 input hashes);
- runners printed confident verdicts: "SUPPORTED", "NOT IDENTIFIED", "PASS if …", and a headline
  "Failures: []".

Yet the substantive verdicts were wrong. Not approximate — wrong in the way that survives a
plausibility read. The statistical tests declared **49 of 72** contrast-outcome rows "supported"; four of
those were artefacts of rank-deficient designs that the estimator had silently papered over (final honest
count: **45/72**). A push-out decomposition reported **0 %** liquidity exits, choice exits and
never-started children — a universal `0/0/0` — because the driver read the wrong object. The equation
suite's headline rule table was computed from `returncode == 0`; the scripts' own decision rules disagreed
with it in **3 of 10** cases.

The programme's own diagnosis is the point of this comment: **the failure mode was not broken software. It
was correct software computing the wrong inference, with every execution-status signal green.**

## 2. Five failure classes, each with its receipt

**Class (a) — resampling that drops its own duplicates.** The DHS cluster bootstrap resampled countries
but kept each drawn country at most once (`r["country"] in samp`), silently converting a cluster bootstrap
into a subsampling bootstrap. The estimator (`scripts/estimate.py`, `_boot_task`; `corrected_reduction.py`,
`ratio_boot`) ran without error and produced intervals that were too narrow (each resampled country kept at most once; ~36.8 % of draw slots discarded). The receipt: Africa-11 2-group
ratio point estimate **1.069843350505824** is unchanged by the fix, while its 95 % CI moves from
**[1.011, 1.135] to [0.9987, 1.1403]** — crossing 1.0 and changing the substantive verdict. Branch
`research/dhs-corrected-2026-11-25` @ `22de735` (authoritative record), earlier fixes `3faeff3`, `45b974e`.
A separate estimator-scope error in the same programme — a single-secondary interaction where the
pre-registered contrast was the full construct × schooling set — moved the D4 point estimate from
**−0.0775 to −0.1962**; conflating the two changes would misattribute a point-estimate move to a
resampling fix, which cannot move a point estimate at all (`SUPERSESSION_2026-11-25.md`, canonical
`research/dhs-api-ecological-2026-11-24` @ `792dba1`).

**Class (b) — transposed design matrices.** The two-way fixed-effects estimator built unit dummies with
`np.tile` and time dummies with `np.repeat` for a row-major `i*T + t` layout — transposed assignments, so
both dummy sets hit the wrong observations. The estimator ran, converged and reported a "null" estimate.
Receipt: eq09 fix `0a91afb`, part of `research/equation-suite-neon-fixes-2026-11-25` @ `575d4cd`
(`NEON_PATCHES_2026-11-25.md` row for eq09; deviation log item 7 records TWFE bias **−0.499 → −1.146**).
The fix is verified by identity: dummy-TWFE equals the within transform to **8.4e-15** on a re-run seed
(QA re-run; 575d4cd).

**Class (c) — masked rank deficiency.** Three of nine outcomes were populated only in some experimental
arms, so the outcome-specific design lost levels (rank **16/18** for `tut_rate`, **17/18** for
`formal_share_gdp` and `skill_premium`). `np.linalg.pinv` returned coefficients and standard errors for
directions the data could not identify, producing effects with p-values of exactly 0 — for example
supply → `formal_share_gdp` "effect 0.135, SE 0.003". No error, no warning. Receipt:
`fix/edsystem-tests-pinv-2026-11-25` @ `3e35ff0` (fix `22c4bb8`); supported rows **49 → 45**, with the four
artefacts now reported as `not_estimable`; empty-stratum `all([])` and zero-variance outcomes also guarded.

**Class (d) — reading state after the engine compacted it.** The exit-reason decomposition read
`e.kids["reason"]` after `core.step` had already moved exited children into `e.exits` and left survivors at
reason −1. The driver therefore saw only survivors: liquidity = choice = never = **0.0** and
`started_share = 1.0` in every one of 1,440 runs. The engine was correct; the driver was wrong. Receipt:
`fix/edsystem-exit-reason-2026-11-25` @ `4679ddb`; evidence at record defaults — 28,000 children,
4,284 censored, 23,716 exits, with q1 liquidity **68.99 %** (40-seed mean) once `e.exits` is read
(`decomp_fixed40.json`, 5,760-run grid); regression test `test_exit_reason.py`. The earlier published
sentence "the engine overwrites the exit reason" is retracted, with the retraction shipped to every
downstream record (e.g. `3afac25`, `d87b89f`, `6935026`).

**Class (e) — execution status masquerading as a verdict.** `run_all.py` reported `PASS` when the process
returned 0, regardless of the script's own `decision_rule.PASS`. The suite's headline read "Failures: []"
while the rules disagreed. Receipt: `575d4cd` — the same run now reports 10/10 executed, **0 execution
failures**, **3 RULE_FAIL** (eq04 pre-declared, eq06 post-hoc, eq10 dropped pre-registered rule), exit
code 1, wall **73.18 s**, 11/11 JSON strict-parse with **0 NaN/Infinity**. The old report's "smoke PASS,
full PASS" table is preserved as the error it was.

A sixth, smaller class belongs in the same family: a lagged panel join used `lag=1` on a five-yearly
schooling series and returned **n = 0**, then computed a verdict from it (`fix/equation-test-bench-2026-11-25`
@ `2c575d9`; the corrected join has **n = 1,495** across 135 countries).

## 3. What caught them — and what would not have

Nothing in the standard engineering stack caught these. Not unit tests (there were none on the faulty
paths). Not CI (all jobs green). Not return codes (all zero). Not code review for style. Not the
plausibility of results: "families with more schooling have fewer children" and "poor households exit for
liquidity reasons" are *expected* directions. The bugs were directionally plausible, numerically stable,
and invisible to tooling that asks only whether code ran.

What caught them was **line-by-line adversarial audit plus independent re-derivation**: a code audit that
rebuilt each estimator from the paper specification and compared, and a second implementation written from
scratch. The DHS reduction reproduced every reported number to ~1e-12 host-side with a validation gate
against the prior record (max |Δ| 0.0036). The verified commit trail then made the fixes checkable.

The second pattern is that **every fix shipped with a test that fails on the base commit** — the only
credible form of evidence for this class of bug. On the v6 ladder the fixed tree passes **22/22** tests
(labour 8/8, gate 4/4, dashboard 3/3, run-swaps 7/7) while the base commit `6728494` passes only
**1/8, 2/4, 2/3, 3/7**. The exit-reason test asserts the all−1 invariant and the corrected partition. The
estimability guards are unit-tested against synthetic rank-deficient and zero-variance designs. A fix
without a fail-on-base test is a hypothesis, not a correction.

## 4. The failure signature

The signature is: **software correct, inference wrong, and every status light green.**

| signal | what it measures | why it missed these bugs |
|---|---|---|
| `returncode == 0` | process health | wrong statistics compute fine |
| CI green | reproducibility of builds | the code reproduced the bug deterministically |
| JSON parses / hashes match | artefact integrity | artefacts were internally consistent |
| verdict strings | the script author's framing | the runner never read `decision_rule.PASS` |
| direction plausibility | face validity | wrong numbers pointed the expected way |

This is worth stating plainly because the dominant AI-assisted-research failure rhetoric is "hallucination"
— invented facts, fake citations. In this programme the software did not invent data; it computed
faithfully from real inputs along a mis-specified path. The failure was **silent and systemic**, and it was
found by reading code, not by asking a model whether it was sure.

## 5. What would have prevented it

1. **Pre-register the decision rule, then import it into the runner.** The rule must be data the runner
   reads (`decision_rule.PASS`), not prose in a report. When the rule was finally wired into `run_all.py`
   (575d4cd), the suite reported 3 RULE_FAIL that the old runner had rendered invisible.
2. **Declare the statistic before the run, in the same normalisation.** The phase-sweep work pre-registered
   a seed-SD-normalised jump statistic (`408aa3e`) and later had to correct a preliminary level-normalised
   variant that was effectively unreachable (`sharpness` 0.019 / 0.013 in `lead_reconciliation.json`;
   corrected in `RUN_REPORT.md` and the dense-grid amendment `40159c7`). Declaring the statistic *and its
   normalisation* in the same commit as the grid is cheap; reconciling two statistics after seeing data is
   not.
3. **Blind re-derivation.** A second implementation written from the specification, not from the first
   codebase, is the single highest-yield check. It caught the DHS point/CI distinction and would have
   caught the driver read in one afternoon.
4. **Fail-on-base regression tests as the merge criterion.** Every bug class above now has one; the gate
   requires it.
5. **Publish the audit trail as first-class output.** Commit receipts, retraction notes, quarantine lists
   and an explicit authoritative-record declaration (`SUPERSESSION_2026-11-25.md`) make the audit reusable.
   The clean path is not "no bug was ever published"; it is "the bug's correction is as citable as the
   claim it replaces."

## 6. Limits — including the audit's own errors

This is one programme, one primary auditor, one team, one week. The findings are not a prevalence estimate
for AI-assisted social science; the five classes are drawn from one codebase. The audit trail itself
contains errors, and that is part of the evidence for this paper's argument:

- The auditor briefly identified the wrong commit as a branch head (`f36577fa` is an ancestor snapshot, not
  the head; corrected in `MIGRATION_2026-11-25.md` line 122 on `research/handoff-2026-11-24`).
- The first "sharpness" statistic used in one analysis was level-normalised and effectively never
  triggerable; that is documented as a declared deviation, not a result (`RUN_REPORT.md` §reproduction;
  `results/lead_reconciliation.json`).
- During the gate, QA itself raised a false mass-deletion alarm from a `--no-checkout` clone's index state;
  it was retracted before it could poison the verdict (`QA_PROTOCOL_2026-11-25.md`, "Evidence rules").

That the process caught its own errors — and that the retractions are in the same commit history as the
claims — is the strongest available argument that the remedy is institutional and adversarial, not a better
linter. Silent failures in AI-assisted science will not be prevented by more automated checking of code
that already runs; they will be prevented by making the audit as executable, as public, and as citable as
the result.
