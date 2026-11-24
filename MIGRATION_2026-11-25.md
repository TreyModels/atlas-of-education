# MIGRATION HANDOFF — 25 Nov 2026 (retiring window / agents)

Repo: **https://github.com/TreyModels/atlas-of-education**
Review index: `research/records/2026-11-25-neon-review/WHERE_TO_LOOK.md` on `research/handoff-2026-11-24`.

## What this session was
Full-system massification work (not shadow-education-only): the four-piece chain (family affordability → learning →
selection gates → credential/jobs), a full-system multiverse, statistical tests, observed-core model, equation suite,
MASSENG v5/v6 coupling, DHS public-API work, and a line-by-line code audit by Neon that found serious estimator and
data bugs. All committed work is pushed; nothing is only on the Mac.

## Heads (origin)
| branch | head | what |
|---|---|---|
| research/handoff-2026-11-24 | this commit | migration handoff + status |
| research/masseng-edsystem-2026-11-25 | b7108da | 1,440-run full-system multiverse (eduengine) + report |
| research/edsystem-tests-2026-11-25 | aadbbb4 | cluster-robust/seed-FE/Holm/stratum tests (has audited bugs; see below) |
| research/equation-suite-2026-11-25 | a7fcfb9 | 10-script inventory suite (numbers quarantined pending fixes) |
| research/shadow-equations-review-2026-11-25 | 264c059 | first-pass shadow demand/learning/gate/earnings + Bray check (one corner) |
| research/masseng-tutoring-2026-11-25 | b9d68c1 | MASSENG v5 switchable tutoring subclass (switch-off bit-identical) |
| research/masseng-gate-jobs-2026-11-25 | 6728494 | v6 gate + labour prototype (audited bugs; see below) |
| research/masseng-edsystem-migration-2026-11-25 | d57d126 (+ pending run) | rural–urban migration extension |
| research/observed-core-2026-11-25 | b563cf1 | observed-core model; honest negative forecast result |
| research/equation-test-bench-2026-11-25 | ab8ca9d | test bench: mostly UNTESTABLE/NOT IDENTIFIED, no false verdicts |
| research/edsystem-audit-2026-11-25 | fe9c6ee | audit of suite/full-system claims (17 flags) |
| research/masseng-audit-2026-11-25 | 8429422 | MASSENG v5 claim-layer audit |
| research/dhs-api-ecological-2026-11-24 | fe762b9 | DHS ecological estimates (D3/D4 under correction) |
| research/dhs-acquisition-2026-11-24 | f4a7f65 | IR pipeline + access records |
| research/apple-silicon-gpu-2026-11-24 | 52d74ec | Apple Silicon port + CUDA equivalence |
| research/synthetic-matrix-2026-11-24 | 77d6f23 | matrix v2/v2b (exploratory pending audit) |
| research/synthetic-phaseb-2026-11-24 | 2b1a160 | Phase B scripts/result (exploratory) |
| research/codex-wave-synthesis-2026-11-24 | c7307ca | synthesis incl. full-system section |
| research/dashboard-2026-11-23 | 54bbb12 | dashboard incl. DHS correction + full-system |
| research/full-system-data-2026-11-25 | 34fd7c9 | observed-vs-assumed data readiness matrix |

Papers: M `a22f3c4`, N1 `5a56864`, F `2bcb7d7` (plus negatives branches); older heads unchanged.

## What is trustworthy
- **MASSENG v5 boundary table**: no learning state, no score/quota gate, no labour market, no rural/urban, no borrowing;
  tutoring absent; credentials only as exogenous premium drivers. This is verified in code and should anchor claims.
- **Switch-off identity** for the tutoring subclass (318/318 array comparisons).
- **Observed-core**: 3 PASS / 9 WEAK / 0 FAIL on LOO, but **future-year splits beat persistence in 0.3% of cells** —
  a structured description, not a validated forecaster. GDP↔enrolment association robust; demand block not estimable.
- **Full-system multiverse qualitative ordering** (gates, affordability, jobs, rural dominate; tutoring gate-driven and
  second-order) is consistent across the run and tests, but see the audited bugs below before quoting exact numbers.

## Quarantined / must-fix before citation (Neon line audit + in-repo audits)
1. **DHS (highest priority — verdict-flipping):** `scripts/estimate.py` cluster bootstrap drops duplicates
   (`r["country"] in samp`) → fix to multiplicity weighting; corrected 2-group D3 should include 1.0
   (Full G=80 [0.9084,1.0164]; Africa-11 [0.9987,1.1323]). `stacked()` omits higher×con (+0.1804, p=0.030) and
   pri/hi interactions; corrected D4 secondary gap ≈ −0.1962. `ir_pipeline.py` has pre-microdata blockers (v190,
   region×round, CMC, weights, survey_type, MIS/AIS, clustering). Old D3/D4 numbers are superseded.
2. **eduengine driver:** the exit-reason bug is in `run_edsystem_multiverse.py` (reads `e.exits` incorrectly), not in
   `core.step`; retract the "engine overwrites reason" claim and restore the liquidity-vs-choice decomposition.
3. **edsystem-tests:** `pinv` on rank-deficient designs creates false "supported" rows; empty-stratum `all([])`; 21/49
   supported rows fail cell-level sign checks. Recompute and reconcile `MULTIVERSE_TESTS.md`.
4. **equation-suite:** quarantine eq03/04/05/07/09/10 until TWFE transpose, probit/Tobit, CES Jacobian, q-shadowing,
   2SLS intercept, Theil/Gini domains, and `run_all.py` decision-rule parsing are fixed. "3 pre-declared FAILs" framing
   is wrong: only S4 is a pre-declared FAIL; S3/S6 are post-hoc; S10 fails a dropped pre-registered rule.
5. **test bench:** F9 join n=0, `inv` singular matrix; E8/PHL panels absent; current matrix correctly says
   UNTESTABLE/NOT IDENTIFIED, not SUPPORTED.
6. **tutoring/gate-jobs:** `_record()` double-counts spend when `spend_feedback=False`; MNL price/option mismatch vs
   Bray; fractional-mass vacancy (4× over-hiring); quota double-count; Tullock invariance; v6 not wired to runner.

## In flight when retired
- DHS fixes (task-49: bootstrap, stacked, ir_pipeline) — dhs-scout.
- eduengine driver + test_full_system pinv fixes (task-50) — corrected-runner.
- test bench F9/pinv/E8-PHL fixes — port-commander.
- migration run on the server (results may need re-pull/commit).
- gate/jobs and observed-core items committed; further fixes per Neon audit.
- Neon (external) is writing drop-in diffs; patch order: **DHS first**, then eduengine driver, then edsystem-tests, then
  equation-suite, then tutoring/gate-jobs.

## Server
- `ssh -p 45973 root@connect.cqa1.seetacloud.com` (key auth installed; **no password stored**). 192 reported cores but
  **cgroup quota = 15 CPUs**; 1007 GB RAM; RTX 4090 D; `/root/miniconda3/bin/python` 3.10.8.
- Queue state: `/root/work/queue/queue.log`; the auto-shutdown watcher was **canceled** to allow corrected re-runs.
- Nothing important is only on the server; all results/records are pulled/committed or documented.

## Next session first moves
1. Apply Neon's DHS fixes, re-run full + Africa-11, correct dashboard/handoff D3/D4.
2. Fix eduengine driver + e.system tests; re-run; correct the false engine-blame sentence everywhere.
3. Fix test bench F9/pinv; add E8/PHL panels from repo records; run naive gate.
4. Quarantine equation-suite numbers; patch or rebuild; never quote eq03/04/05/07/09/10 as-is.
5. Decide server lifetime with Trey (keep for re-runs vs 关机); no instance changes without explicit instruction.

Rules preserved: pre-registration before runs, additive branches only, no secrets, simulation labels, no causal language,
preserve failures, recompute before quoting.

---

## AMENDMENT — 25 Nov 2026: power rules + Neon-free fixes (read this before the next run)

**POWER RULES are absolute.** No agent may power off, shut down, reboot, stop, or restart the AutoDL
instance, ever — not by `shutdown`/`reboot`/`poweroff`/the AutoDL stub/console/API/wrapper, and no agent
may create, arm, edit, or re-enable any watcher, timer, cron, `at` job, or "shutdown when done" script.
No standing rules: power is the operator's in-conversation decision, per action. If an agent thinks the
box should go off, it says so and stops. This supersedes item 5 of "Next session first moves" above.
Full text: `NEON_FREE_FIXES_2026-11-25.md` in this branch and `~/neon-boot/POWER_RULES_2026-11-25.md`.
Incident: an agent-authored `shutdown_after_two.sh` fired at 00:31:04 CST and powered the box off; the
operator recovered it; both watchers are renamed `*.DISABLED_2026-11-25` — do not reverse that.
Forensics attribute the script and its markers to a **lingering agent from the retired window** (its
`run_neon_fix.sh` mtime is 00:17, before this session started), not to the Lead or to Commander; that
same worker produced the corrected DHS numbers, which is why their provenance is recorded in
`NEON_FREE_FIXES_2026-11-25.md` and validated by an independent host-side reproduction.

**Neon-free work already done and pushed** (four additive branches; see `NEON_FREE_FIXES_2026-11-25.md`):
DHS bootstrap-multiplicity corrected run (`research/dhs-corrected-2026-11-25`), eduengine driver
exit-reason fix (`fix/edsystem-exit-reason-2026-11-25`), e ds ystem test guards
(`fix/edsystem-tests-pinv-2026-11-25`), test-bench F9/`inv` fix (`fix/equation-test-bench-2026-11-25`).
Neon's own diffs (ir_pipeline, equation-suite ×2, gate-jobs tail) are still to be applied on top; where
they overlap, his diff wins and the regression tests in these branches are the acceptance gate.

---

## QUARANTINE ADDENDUM — 25 Nov 2026 (two branches withdrawn from citation)

Heads verified with `git ls-remote origin` on 25 Nov 2026. **Both branches are QUARANTINED — do not cite any number,
table or claim from them.** This is additional to (not instead of) item 5 on test bench F9/`inv`.

### Q1. `research/equation-test-bench-2026-11-25` @ `02d930c7e180463f94c71b5a49f6938855317ab3` — QUARANTINED — do not cite
Head-check note: `f36577fa` is **not** the branch head; it is an ancestor snapshot commit contained in the branch.
The current remote head is `02d930c`. Defects from the Neon line audit (task-49):
1. key-name bug killing `F2_supply` / `F6_growth` (both run on n=0 cells, so their "verdicts" are undefined);
2. out-of-sample evaluation drops controls (the comparison set differs from the in-sample fit set);
3. `wins` is a no-op (the statistic is never applied);
4. contemporaneous-Δ leakage: ΔX_t → ΔY_t, so the "predictor" is same-year change, not a lead.

The separate fix branch `fix/equation-test-bench-2026-11-25` @ `2c575d9` fixes **only** F9 (join n=0) and the `inv`
singular-matrix crash. **It does NOT cover the four items above.** Do not treat `2c575d9` as clearance for this branch.

### Q2. `research/shadow-equations-review-2026-11-25` @ `264c059032c58f74916106207b8e571d6bf4a6ba` — QUARANTINED — do not cite
Defects from the Neon line audit (task-49):
1. `gini(learn)` can be negative (invalid Gini domain);
2. `_income_elasticity == 0` (degenerate identity elasticity);
3. post-transfer quintile re-ranking (units are re-sorted after transfers, so quintile comparisons are not like-for-like);
4. three exact linear collinearities in the design (non-identified coefficients reported).
No fix branch exists for these items; nothing from this branch may be cited.
