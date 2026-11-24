# Five silent failures: when the pipeline runs, the numbers look plausible, and the check passes

**Record:** `research/records/2026-11-25-meta-science/` · **Branch:** `research/meta-science-silent-failures-2026-11-25`
**Base:** `origin/main` @ `55732f4` · **Status:** forensic methods essay (additive; no causal claims about real systems)
**Receipts:** every quoted commit, file and line is in `RECEIPTS.csv` and was verified with `git show` before being
quoted. Derived statements are labelled *recomputation* or *inference*. Retractions are preserved, not softened.

---

## Summary

This record studies five defects in this repository that did not crash anything. Each pipeline ran to completion,
wrote finite numbers, and left a check that said yes. The numbers were wrong in ways that mattered: an interval
that was too narrow, a fixed-effects matrix with unit and time dummies swapped, finite estimates for contrasts the
data could not identify, an all-zero exit decomposition in every run, and a runner that called a script "PASS"
because its process exited zero even when the script's own rule said `PASS=False`.

The common structure is a **mismatch between the object the code observes and the object the claim is about**:
the bootstrap observes a de-duplicated resample; the TWFE regression a permuted dummy set; the pseudo-inverse the
column space but not the contrast; the driver the post-compaction roster; the runner the process exit code.
Nothing raises, because each wrong observation is a legal numerical object.

Detection, in all five cases, came from **line-by-line review of code and records**, not from the test suites in
place at the time. The repairs share a shape: make the wrong state impossible to represent or loudly labelled —
estimability guards, partition and sentinel assertions, explicit verdict categories, re-recorded outputs. The
record also supplies a sixth case: a correct quarantine list that, quoted downstream, **coalesced into a citation
of a commit that does not exist**. Bug lists decay into folklore by the same mechanism by which the bugs stayed
silent.

## 1. The problem

A computational social-science result is a chain: data → estimator → output file → summary table → claim. A crash
breaks the chain visibly; a silent failure substitutes a different, plausible object somewhere in the middle and
lets the chain run. The output is well-formed; the JSON parses; the report generates; the tests are green because
they test the wrong object or nothing where the defect lives. What is lost is the specific thing the claim needs:
the sampling distribution, the contrast, the estimand, the population, the verdict.

This essay asks one answerable question: given this repository's own commits, can each of five reported silent
failures be shown — defective line, mechanism of silence, fix, guard — without relying on memory? And can the five
be put into a small operational taxonomy?

## 2. Method: the commit history as the receipt trail

The corpus is the repository's own history, reached through a partial clone. The plan (`OUTLINE.md`,
`5b93a41`) fixed the protocol before any claim: show the **before state** (`<sha>^`) as well as the fix; **quote
the hunk** pinned to `<commit>:<path>:<line(s)>`; label derived statements *recomputation*, not quotation;
**reconcile** report/log/JSON disagreements; **preserve retractions** as additive commits (`4679ddb`, `3afac25`,
`d532478`); and **report missing receipts** when a suggested commit does not exist or shows something else (§8).

The defects are not all on `main`; they live on research branches visible through `git log --all`. Receipts are
pinned to **commits, not branches** — branches move while this is written.

## 3. Case 1 — the bootstrap that deleted its own duplicates (DHS)

**Symptom.** A country-cluster bootstrap for the DHS ecological estimates produced intervals that were too narrow.
Point estimates were fine. The intervals moved one verdict at the margin: the Africa-11 two-group ratio, which had
excluded 1.0, came to sit on the boundary.

**Root cause.** The bootstrap resampled countries with replacement and then filtered the panel by membership
(`estimate.py` @ `3faeff3^`:146–148, R1.2):

```python
samp = list(rng.choice(common, size=len(common), replace=True))
ra = [r for r in pa if r["country"] in samp]
rb = [r for r in pb if r["country"] in samp]
```

`rng.choice(..., replace=True)` emits a list in which some countries appear several times; the comprehension keeps
each panel row whose country is **in** the list — at most once. Multiplicities are discarded, so the quantity is a
subsampling bootstrap over distinct countries, not a cluster bootstrap, and its intervals are narrower. The same
pattern is in `corrected_reduction.py` @ `3faeff3^`:161 (R1.2).

**Why silent.** No exception; the estimator still runs; the intervals are narrower but finite and plausible. The
fix, by construction, cannot move a point estimate, and the record says so:

> `CORRECTED_RUN_2026-11-25.md` @ `22de735`:46–52 (R1.5)
> "**(a) Cluster-bootstrap multiplicities → bootstrap CIs only; it cannot move a point estimate.** … That is a
> subsampling bootstrap, not a country-cluster bootstrap: ~36.8 % of resampled slots were dropped and the intervals
> were too narrow."

*Recomputation.* A standard bootstrap retains `G·(1−(1−1/G)^G)` distinct countries in expectation; at the sample
sizes here (`G` = 65, 80) that discards **≈36.5–36.6 %** of resampled slots (asymptotically 36.79 %, the ~36.8 %
the record rounds to). Verified arithmetically and by simulating the exact sampling line on the host (`numpy`).

**Detection.** External line audit ("Neon audit item 1") plus the handoff's item 1: *"cluster bootstrap drops
duplicates (`r["country"] in samp`) → fix to multiplicity weighting"* (`MIGRATION_2026-11-25.md` @ `354f7c0`:
48–52, R1.8).

**Fix.** Draw multiplicities and replicate each country's cells (`estimate.py` @ `3faeff3`:154–159, R1.1):

```python
mult = Counter(rng.choice(common, size=len(common), replace=True).tolist())
def expand(panel):
    return [dict(r) for r in panel if r["country"] in mult for _ in range(mult[r["country"]])]
```

The same change is in `corrected_reduction.py` (`_expand`, `3faeff3`:149–151). A second branch, `93b882a`
(parallel, also cut from `fe762b9`), carries the same fix with a CR1/`t_{G−1}` correction and a change from
imputing to dropping a missing pipeline control (R1.3) — found and fixed twice, independently.

**A correction to the correction.** The first corrected record (`3faeff3`) attached the D4 point-estimate change to
the bootstrap fix. That is impossible, and a later commit separates them: *"DHS corrected-run record: separate the
bootstrap CI change from the D4 interaction-set change"* (`9e063bf`, R1.4). It matters: *"if his `estimate.py`
patch fixes **only** the bootstrap multiplicity, the D4 point estimate will return to ≈ −0.0775"* (`22de735`:
138–140, R1.5). A correct fix with a wrong attribution is a second-order defect.

**Where the record does not reconcile.** The table's Africa-11 two-group row gives `1.0698 [0.9987, 1.1403]` and
says *"now includes 1.0 — verdict moves to indeterminate"* (`22de735`:90, R1.5). That interval is from
`corrected_reduction.py` (`corrected_results.json` @ `3faeff3`, R1.7); the same run's `estimate.py` bootstrap wrote
`[1.0011, 1.1403]` into `results/africa11/results.json` and the run log (`3faeff3`, R1.6/R1.7), *excluding* 1.0 by
about a thousandth of a ratio unit. The record acknowledges the two implementations differ in the last digits
(`22de735`:107–108) and that closing the provenance caveat *"still does not resolve the separate `estimate.py`
bootstrap-diff reconciliation item"* (`22de735`:118–123). The honest statement: **the verdict flip is
implementation-dependent at the boundary** — true for the cross-check implementation, not the package's own
bootstrap.

**Guard.** No committed regression test for the multiplicity. The available guard is a second, independently
written implementation (`corrected_reduction.py`) run against the committed panels (`max_abs_delta = 0.0036`,
`22de735`:104) — it catches gross errors but not this defect, because the same wrong sampling line was in both
implementations. **A real gap**: the right test (assert a duplicate resample changes the estimate toward frequency
weighting) was not added.

**Lesson.** A bootstrap is a claim about a sampling distribution; code that "resamples" but de-duplicates has
silently changed the estimand.

## 4. Case 2 — the transposed TWFE matrix (equation suite)

**Symptom.** The identification demonstration reported a two-way fixed-effects bias of −0.50 in a known-truth
staggered-adoption world. After the fix it reports −1.15, and the transposed version's null-world TWFE mean was
−0.023.

**Root cause.** With `Y` of shape `N × T`, `Y.reshape(-1)` is row-major: row index is `i*T + t`. A unit dummy is
constant over a block of `T` rows (`np.repeat`); a time dummy cycles with period `N` (`np.tile`). The code had
them the other way round (`eq09_identification.py` @ `0a91afb^`:30–33, R2.1):

```python
for i in range(1, N):
    X.append(np.tile((np.arange(N) == i).astype(float), T))
for t in range(1, T):
    X.append(np.repeat((np.arange(T) == t).astype(float), N))
```

The fixed version swaps them and states the reason (`0a91afb`:27–40, R2.2): *"unit dummy is constant within a
T-long block (np.repeat) and a time dummy cycles across blocks (np.tile). The previous version had these transposed
(tile for units, repeat for time), so both dummy sets hit the wrong observations."*

*Recomputation of the indexing.* For `N=3, T=2`, row-major positions decode as `(i,t) = (p//T, p%T)`. The old
"unit 1" dummy `np.tile([0,1,0], 2)` = `[0,1,0,0,1,0]` has ones at positions 1 and 4, decoding to `(0,1)` and
`(2,0)` — one row from unit 0 and one from unit 2, not two rows from unit 1; the correct `np.repeat([0,1,0], 2)`
= `[0,0,1,1,0,0]` decodes to `(1,0)`, `(1,1)`. Running both variants on the suite's own `did_world` DGP with its
seed (`20261125`, 60 reps, `N=40, T=20`) gives old `0.785 / −0.499 / −0.023` and new `0.138 / −1.146 / 0.003` for
`twfe_mean / twfe_bias / null_twfe_mean` — identical to the committed before/after JSONs (R2.3/R2.4).

**Why silent.** The design matrix stays full column rank, `np.linalg.pinv` does not complain, OLS returns finite
coefficients and SEs, and the outcome is plausible. The old, smaller-magnitude bias made TWFE look *less* biased
than it is — the defect flattered the estimator it affected. The suite's own rule did not fire: the null-world
TWFE mean was near zero in both versions (−0.023 vs 0.003), so `null_twfe_near_zero` was `True` before the fix. A
wrong design can pass a null check.

**Detection.** External line audit and handoff quarantine item 4; the fix commit names it (`0a91afb`). The fix
also corrects the 2SLS SE, which had used residuals from the *fitted* regressor `Dhat` rather than actual `D`
(`0a91afb^`:64–66, R2.1; after: `0a91afb`:69–75, R2.2, using `sigma2 = sum(e**2)/(n−k)`).

**Fix.** Swap `tile`/`repeat`; use actual-`D` residuals and the `n−k` denominator. The report records the
movement: *"TWFE mean 0.785 → 0.138, bias −0.499 → −1.146 … IV SE mean 0.082 → 0.045"* (`SUITE_REPORT.md` @
`73e99e0`:165–167, R2.4).

**A second-order silent failure in the record.** The fix commit changed **only the script** (R2.2); the committed
`results/eq09_identification.json` still carried the old numbers at `0a91afb` (R2.3) and was re-recorded only when
the suite was re-run end to end (`d575bfe`, 19 files, R2.5). Between those commits the record quoted old numbers
under a fixed-code commit: a code fix is not a record fix.

**Guard.** No regression test for the TWFE indexing in the receipt set; the protection is the re-recorded results
plus the report's fix note. A minimal guard would be a property test: for a balanced panel with additive unit and
time effects and `D=0`, the explicit-dummy TWFE coefficient must equal the within-transformed estimator. It does
not exist here.

**Lesson.** Dummy-coding is an indexing claim. When it is wrong the estimator still returns finite numbers — and
may look better. Test the design matrix against an independent formulation of the same estimator.

## 5. Case 3 — `pinv`, empty strata, and zero variance (full-system screen)

**Symptom.** The full-system screen claimed "supported effects (Holm p<0.05 and sign-consistent across strata)" for
49 rows. Four were artefacts. After the fix the supported set is **45** rows (R3.4/R3.5) and four rows are
reported `not_estimable`.

**Root cause.** Three mechanisms, all in the pre-fix test code (`test_full_system.py` @ `22c4bb8^`, R3.1):

```python
XtX_inv = np.linalg.pinv(X.T @ X)                                    # :30
sgn = all(x > 0 for x in strat) if eff > 0 else all(x < 0 for x in strat)   # :108
r["supported"] = bool(r["p_holm"] < 0.05 and r.get("sign_consistent") is True and r.get("effect") is not None)  # :119
```

`pinv` returns a minimum-norm solution for a rank-deficient design: a coefficient, an SE and a p-value for a
direction the data cannot identify. `all([])` is `True` in Python, so an empty stratum list passed the
sign-consistency check. And a zero-variance outcome (tutoring switched off by construction) gave effect `2.8e-17`,
SE `4.2e-19`, `p_holm = 0` — division by a numerically zero variance.

**Why silent.** Every wrong object is a legal number. Among the old JSON's 49 "supported" rows (R3.4):

- supply → `formal_share_gdp`: `0.1352`, SE `0.00303`, `p_holm = 0` — the outcome exists only in the fiscal-loop
  arms, so the contrast is collinear with the intercept;
- learning → `tut_rate` for `plus_private`: `2.78e-17`, SE `4.19e-19`, `p_holm = 0`;
- learning → `tut_rate` for `plus_private_tutoring`: `0.1591`, SE `0.00376`, no strata;
- jobs → `skill_premium`: `0.882`, SE `0.0106`, no strata.

The audit stated it exactly: *"4 'supported' rows have no strata at all (empty `all([])` returns True), and one
zero-variance outcome is classified supported (tut_rate effect 2.8e-17, SE 4.2e-19, p_holm 0)"* (`AUDIT.md` @
`fe9c6ee`:30–33, R3.8), and flagged that the report and JSON disagreed on the supported set (`fe9c6ee`:33–34,
`156–164`). The tiny SEs are the signature: an unidentified direction does not produce an error, it produces an
implausibly precise estimate.

**Fix.** Three guards plus a relabelling (`test_full_system.py` @ `22c4bb8`, R3.2): a rank/estimability test
(`RANK_REL_TOL = 1e-8`, `row_space_basis()`, `contrast_estimable()`; :99), a zero-variance check (:96), a
non-empty-strata check (`sign_consistent = None; if strat: …`, :252–254), and a supported rule requiring
`estimable is True` plus a non-`None` Holm p (:272–277). A deviation note was added: the screen's p-values were
never pre-registered, and the multiverse pre-registration said *"no p-values"* (`TEST_PREREGISTRATION_DEVIATION.md`
@ `22c4bb8`:6–11, R3.7; `MULTIVERSE_TESTS.md` @ `22c4bb8`:7–13, R3.6). The supported set is published in full at
45, the four artefacts listed as `not_estimable` with reasons.

**Guard.** `test_guards.py` is new in `22c4bb8` (R3.3): `unit_checks()` (duplicate-column rank, non-estimable
individual coefficient, estimable sum, missing reference rows, zero-variance outcome, rank-deficient arm) and
`integration_check()`, which builds a synthetic multiverse carrying all three defect shapes and asserts none is
ever "supported". I ran it from the fix commit on the host (`numpy` only): `ALL PASS`. Run against the pre-fix
module it exits non-zero (the guard API is absent), so it cannot silently pass either. The integration check is
the substantive defence: it encodes the original defect shapes.

**Lesson.** Never call `pinv` to answer a question about a *contrast*; ask whether the contrast is in the row space
first. Treat `all([]) is True` as a bug generator. An SE computed from a zero-variance outcome is not a small SE —
it is not an estimate.

## 6. Case 4 — the emptied roster (exit reason 0/0/0 in every run)

**Symptom.** The 1,440-run full-system multiverse reported, for push-out decomposition, `liquidity = choice =
never = 0.0` and `started_share = 1.0` **in every run**. The first run report called this an engine limitation and
declared the decomposition unusable.

**Root cause.** The engine compacts exited children out of the state at the end of every step — appending them to
`e.exits`, then keeping only survivors (`engine/eduengine/core.py` @ `origin/main`:444–447, R4.2):

```python
if len(ex):
    self.exits.append({kk: (v[ex] if v.ndim == 1 else v[ex]) for kk, v in k.items()})
    keep = k['reason'] < 0
    self.kids = {kk: v[keep] for kk, v in k.items()}
```

After `e.run()`, `e.kids['reason']` is all `−1` (survivors are censored, not exited). The driver read the emptied
roster (`run_edsystem_multiverse.py` @ `219747a^`:114, R4.1): `k = e.kids`.

**Why silent.** Reading the survivors is legal, gives correct array shapes, and produces exactly `0.0` for three
mutually exclusive categories and `1.0` for "started". No exception, no NaN, no shape mismatch. The wrong number
was not an outlier a sanity check would flag; it was the structurally correct output of reading the wrong object:

> `RUN_REPORT.md` @ `4679ddb`:183–184 (R4.5)
> "therefore **all −1**, and the driver's `k = e.kids; reason = k["reason"]` read only the survivors:
> liquidity = choice = never = 0.0 and started_share = 1.0 in **every** run, by construction."

**A wrong blame, then a retraction, then a correction of the wording.** The first run report blamed the engine:
*"the engine's final state records no liquidity exits … the `reason` code is overwritten … so the decomposition
reads 0/0/0 and is not usable"* (pre-fix §3.8, quoted from the diff that removed it, `4679ddb`, R4.7). `4679ddb`
retracts it: *"the bug was the driver reading `e.kids['reason']` after the engine had compacted exits into
`e.exits`"* (`RUN_REPORT.md` @ `4679ddb`:13–15). The suite audit carried the same wrong blame as FS-12, so a later
retraction-completeness pass added an erratum — *"This is **wrong and is retracted.** The engine is correct … The
defect was the **driver**, not the engine"* (`ERRATUM_FS-12.md` @ `3afac25`:12–15, R4.6) — leaving the unqualified
audit text as evidence (`3afac25`:21–26). The handoff still says the driver *"reads `e.exits` incorrectly"*
(`354f7c0`:53–54, R4.8), a third phrasing that is not the code fact: three records, three paraphrases, one line.

**A two-stage fix.** The first fix read `e.X`, the engine's concatenation of exit records only (`747be44`, R4.3),
recovering exits but dropping survivors — not a partition of the population. The final fix (`219747a`:104–127,
141, R4.4) rebuilds the full population from exits plus survivors via `aggregate_exits(e)`, reports survivors as
`censored`, and makes the terminal categories a partition. A fresh instrumented run gives liquidity 35.7 % under
cash-only affordability and 20.3 % under credit+poverty, with quota rationing only in the quota arm
(`RUN_REPORT.md` @ `4679ddb`:196–209).

**Guard.** `test_exit_reason.py` (new in `219747a`, R4.4) pins the invariant that caused the bug
(`e.kids['reason']` all `−1`), then asserts population = survivors + exits, known reason codes, liquidity and
choice exits present, `n_exits > 0`, group shares summing to 1, and positive started-children liquidity
(`test_exit_reason.py` @ `219747a`:74–102). I ran it from the fix commit against the local engine (`N=80, T=40`):
`ALL PASS`. The assertion set would have caught the original driver — a survivors-only read gives `n_exits = 0`
and zero liquidity in every group (inference; against the pre-fix driver the test exits non-zero on the missing
`aggregate_exits` API).

**Lesson.** When a structure maintains a live set and an archive, "read the population" is a two-part operation:
assert the partition (sums to 1, sentinel `−1` is a category, not an absence). And when the record has blamed the
wrong component, the blame must be retracted where it was published, with the old text preserved.

## 7. Case 5 — `returncode == 0` hiding `PASS=False` (`run_all.py`)

**Symptom.** The equation suite's runner recorded all ten scripts as PASS with `failures = []`, while three
scripts' own decision rules said `PASS=False`. The suite report's headline read "Failures: []" and its per-script
section "smoke PASS, full PASS". The audit's summary: *"10/10 scripts executed; 3 decision rules fail"*
(`AUDIT.md` @ `fe9c6ee`:17, R5.3).

**Root cause.** The runner used the process exit code as the verdict (`run_all.py` @ `93a351e^`:42, 81–82, 93,
R5.1):

```python
"status": "PASS" if p.returncode == 0 else "FAIL",
manifest["failures"] = [r["script"] for r in manifest["smoke"] + manifest["full"] if r["status"] != "PASS"]
return 0 if not manifest["failures"] else 1
```

The scripts execute cleanly and fail their *decision rule* — they do not exit non-zero on a failed rule. So
`returncode == 0`, `status` is "PASS", `failures` is empty, and the runner exits 0. The verdict object (the
script's `decision_rule.PASS`) was already in each output JSON; the runner never read it.

**Why silent.** The purest control-flow masking in the set: two true statements — "the process exited 0" and
"the script ran" — standing in for "the script's test passed". The report inherited the runner's vocabulary:
"Failures: []", "smoke PASS, full PASS", "All ten scripts passed smoke and full. No script failed" (`AUDIT.md` @
`fe9c6ee`:96–102). Failures were visible only in per-script bullets.

**Fix.** Read the decision rule from the script's JSON and separate execution from verdict (`run_all.py` @
`93a351e`:36–58, 73–86, R5.2):

```python
dr = obj.get("decision_rule")
if not isinstance(dr, dict) or "PASS" not in dr:
    res["rule_error"] = "no decision_rule.PASS in output JSON"; return res
res["decision_rule_pass"] = bool(dr["PASS"])
...
if p.returncode != 0:  status = "FAIL"        # execution
elif ... is True:      status = "PASS"        # decision rule
elif ... is False:     status = "RULE_FAIL"
else:                  status = "NO_RULE"     # missing verdict = not a pass
```

A missing or unreadable rule is now `NO_RULE` — a failure for the runner's own exit code — not a pass.

**After the re-record.** The re-run committed at `d575bfe` shows the separation working: `execution_failures: []`
and `decision_rule_failures: ["eq04_transitions_gates.py", "eq06_migration_rural_urban.py",
"eq10_tutoring_shadow.py"]`, every one with `returncode = 0` (`run_all.json` @ `d575bfe`:501–522, R5.4). The old
`PASS` for S10 was itself wrong under the pre-registered rule; the new verdict surfaces it as `RULE_FAIL`.

**Guard.** No dedicated regression test for `run_all.py` was committed. The durable guard is the output contract:
`verdict_rule`, `execution_status`, `decision_rule_pass`, `execution_failures`, `decision_rule_failures`,
`no_rule_verdict` (R5.2/R5.4), so a future run that hides a rule failure is detectable in the record. A test that
runs a deliberately failing rule and asserts `RULE_FAIL` would be stronger; it is not in the receipt set.

**Lesson.** Process success is a transport property, not a verdict. A runner must read the verdict from the object
the claim is about and have a distinct "no verdict" state so a missing rule cannot default to pass.

## 8. A sixth finding: the receipt that coalesced (eq03 / TWFE)

The task that produced this record listed, for the TWFE case, a second receipt: *"the eq03 TWFE transpose commit
you locate"*. **No such commit exists in the reachable history**, and how it came to be believed is itself a small
silent failure of the record.

- `git log --all --oneline -- '*eq03*'` returns **five** commits: `5880c7f`, `53b158a`, `a7fcfb9`, `aefade0`,
  `d575bfe` — none touches a transposed dummy matrix.
- The only TWFE-transpose fix is `0a91afb`, in **eq09**: `git log --all -S'np.tile' --
  research/records/2026-11-25-equation-suite` returns three commits — the initial suite (`5880c7f`), the eq09 fix
  (`0a91afb`), the patch record (`d289f2e`) — and only `0a91afb` changes the dummy indexing.
- The eq03 fix that exists is `aefade0`: a 1-D grid over ρ becomes a 2-D (ρ, ω) CES grid on the A-scale
  (`eq03_learning_quality.py` @ `aefade0`:36–40, R2.6). The patch record describes it under *eq03* as *"CES fit:
  2-D (ρ, ω) grid … scale concentrated out"* (`NEON_PATCHES_2026-11-25.md` @ `d289f2e`:24, R2.7). Not a transpose.

Where the wrong citation comes from is legible in the handoff's quarantine list:

> `MIGRATION_2026-11-25.md` @ `354f7c0`:57–59 (R2.8)
> "**equation-suite:** quarantine eq03/04/05/07/09/10 until TWFE transpose, probit/Tobit, CES Jacobian,
> q-shadowing, 2SLS intercept, Theil/Gini domains, and `run_all.py` decision-rule parsing are fixed."

That line is correct as a *quarantine*: six scripts held back pending a bundle of fixes, of which the TWFE
transpose (belonging to eq09) is one. Read as a per-script defect list, it invites exactly the inference supplied
to me — "eq03 had a TWFE transpose". A correct quarantine became a wrong citation downstream: a plausible,
well-formed object (a sentence naming a script and a defect) inherited authority from its source while no longer
denoting the same fact. The date-stamp, the exact SHA and the "which script" question dissolve it; the same
receipt discipline applied to citations prevents it.

Two related remaps: the handoff calls the eq03 item *"CES Jacobian"*, while the fix that landed is a 2-D (ρ, ω)
grid (`aefade0`; `d289f2e`:24); and handoff item 2 says the driver *"reads `e.exits` incorrectly"* when the code
read `e.kids` (`MIGRATION_2026-11-25.md`:53–54 vs `219747a^`:114). Neither changed a number.

## 9. A latent case worth naming (verified, not known to have fired)

The Lead flagged a control-flow hazard in the gate dispatch, and it verifies in-repo at `origin/main`
(`engine/eduengine/core.py`:164 and 369–371, R6.1):

```python
ref = gate['bar'] if gate['kind'] == 'bar' else self.cut[m]     # :164
if gate['kind'] == 'bar':                                       # :369
    ok = score >= gate['bar']
else:   # quota: seats = share x cohort size ...                # :371
```

Any gate kind other than `'bar'` is executed as a quota: at :164 it uses the quota cutoff belief; at 369–371 it
takes the `else`, reads `gate['share']`, and applies a rank cutoff. A future gate kind would be silently
implemented as a quota rather than rejected. The world configurations define only `'bar'` and `'quota'`
(`engine/worlds.py`:23–24; `engine/countries/china.py`:9–11), so the branch has never been taken with an unknown
kind as far as this record can establish. It is a **latent** instance of control-flow masking, not a sixth occurred
bug: the `else` is a silent default, the same structural property as case 5's `returncode == 0` and case 3's
`all([])`.

## 10. Taxonomy

| mode | definition | cases |
|---|---|---|
| **T1 wrong-object / aliasing** | the code observes a different object than the claim (empty roster vs population; survivors vs exits; record vs run) | 4, 8 |
| **T2 numerically-masked degeneracy** | a numerical routine returns finite, plausible numbers for a non-identified or degenerate quantity (`pinv` on rank deficiency; zero-variance SEs) | 3 |
| **T3 aggregation / multiplicity** | resampling, de-duplication or category construction changes the estimand or partition (`in samp` de-duplication; `all([])`; unasserted shares) | 1, 3, 4 |
| **T4 control-flow / verdict masking** | a transport object stands in for the claim (`returncode == 0`; empty-stratum `all`; `else` absorbing unknown gate kinds) | 5, 3, 9 |
| **T5 provenance / retraction drift** | the record drifts from the code or the run (results not re-recorded after a fix; wrong blame surviving in summaries; a quarantine bundle re-read as a per-script citation; three paraphrases of one code line) | 1, 2, 4, 8 |

The modes are not independent (case 3 is T2 and T3; case 4 is T1 and T3). And **T5 keeps the failure alive**:
code bugs get fixed, but a wrong sentence in a summary, a stale result file, or a receipt naming the wrong script
is copied forward. One case needed three retraction passes (engine-blame → driver-bug → erratum) — the cost of
letting the blame narrative outlive the code.

## 11. What caught them, and what the guards share

Detection is uniform: **external line-by-line review** found all five; the in-repo audits propagated the findings
and sometimes over-corrected them (FS-12); the test suites live at the time did not catch the defects because they
asserted the wrong object or nothing at the defect site. The fixes converge on four rules:

1. **Estimability before estimation** — no number for a contrast outside the design's row space, no estimate from a
   zero-variance outcome (case 3).
2. **Partition and sentinel assertions** — assert sums to 1; name `−1` as a category; do not treat an empty live
   set as data (cases 1, 3, 4).
3. **Separate verdict from transport** — execution status and decision-rule status are different fields; "no
   verdict" must not be a pass (cases 5, 9).
4. **Re-record after fixing** — a fix that does not regenerate committed outputs leaves a record disagreeing with
   itself (case 2); a retraction must be published where the wrong claim was (case 4).

The added guards (`test_guards.py`, `test_exit_reason.py`) share a second property: they encode the *defect shape*
(rank-deficient arm, zero variance, empty strata; the all-`−1` invariant), not just the happy path.

## 12. Limits

This is a five-case convenience sample from one repository, written by a participant in the same programme. It has
no base rate, no denominator, and cannot say whether these defects are typical. It makes no claim about why they
were introduced; statements about mechanisms are statements about code, not about people. The corpus is partial:
commits live on research branches, some receipts are records about records, and at least one suggested receipt does
not exist. Where records disagree — notably the Africa-11 interval — both values and both files are reported rather
than resolved. Recomputations used the repository's own seeds and code where possible and confirm mechanisms, not
new estimates. Verification is against the commits in `RECEIPTS.csv`.

## 13. What to carry forward

The operational residue is `GUARDS_CHECKLIST.md` (partition sums; sentinel assertions; rank and variance checks
before pseudo-inverses; verdict-vs-exit-code separation; mutation controls; re-record after fix; receipt
discipline). The one sentence to keep: **a pipeline that runs, prints plausible numbers and passes is evidence
about the pipeline, not about the claim — unless the check that passed was a check on the object the claim is
about.**
