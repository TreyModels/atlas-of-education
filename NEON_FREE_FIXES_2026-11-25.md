# NEON-FREE FIXES — 25 Nov 2026 (Commander session)

**Status: four of Neon's quarantine items are fixed, tested, and PUSHED** (additive branches, no
main, no force). Neon's own drop-in diffs are still pending — nothing here replaces them; where they
overlap, his diff wins and the tests here are the acceptance gate.

| # | branch (pushed) | head | what was fixed | test |
|---|---|---|---|---|
| 1 | `research/dhs-corrected-2026-11-25` | `3faeff3` | DHS cluster-bootstrap multiplicities (Neon item 1) + corrected run committed | host reproduction to 1e-12; validation gate passes (max\|Δ\| 0.0036) |
| 2 | `fix/edsystem-exit-reason-2026-11-25` | `4679ddb` | driver read `e.kids['reason']` after `core.step` compacted exits into `e.exits` → universal 0/0/0 decomposition; RUN_REPORT retracted | `test_exit_reason.py` ALL PASS |
| 3 | `fix/edsystem-tests-pinv-2026-11-25` | `22c4bb8` | `pinv` on rank-deficient designs, empty-stratum `all([])`, zero-variance false positives; full 45-row set published | `test_guards.py` ALL PASS |
| 4 | `fix/equation-test-bench-2026-11-25` | `2c575d9` | F9 join `lag=1` → n=0 (schooling is 5-yearly); `inv` singular on collinear controls; Q1 permutation; E8/PHL explicit | `test_bench_guards.py` ALL PASS |

### Provenance of the corrected DHS numbers (important)

The corrected DHS run that produced these numbers was executed on the box by a **lingering agent from
the retired window** (not by this session's Commander): `/root/work/dhs-api`, runner
`/root/work/run_neon_fix.sh`, log `/root/work/neon_fix.log`, run window ~00:15–00:20 CST. That is the
same agent whose on-box `shutdown_after_two.sh` later powered the instance off (see POWER RULES).
What makes the numbers usable is **not** that authorship: it is that Commander independently
re-ran the reduction host-side with the fixed script and reproduced every reported number to ~1e-12,
and the prior-record validation gate passed (max |Δ| 0.0036). Treat the numbers as **PROVISIONAL from
an unattributed box run that has been host-reproduced** until Neon's `ir_pipeline.py`/`estimate.py`
diff is applied and the run is redone under a known runner.

**Not pushed, local only:** `fix/equation-suite-2026-11-25` (in `~/neon-boot/wt/eq`) — framing and
domain fixes only (deviations log, eq04 boundary flag, eq07 Gini/Theil domains + data tier,
`run_all.py` execution-vs-decision-rule separation). The math fixes Neon lists (TWFE transpose,
probit/Tobit, CES Jacobian, 2SLS intercept, q-shadowing) are **not done** — his diffs should land
first. Do not quote eq03/04/05/07/09/10 numbers until then.

## Key results

- **DHS (verified on the box and reproduced on the host):** full-sample Q2a 2-group ratio 0.958
  [0.906, 1.019]; Africa-11 2-group ratio **1.0698 [0.9987, 1.1403] — now includes 1.0** (was
  [1.011, 1.135]); Q2b1 wanted-vs-actual **−0.1962** (was −0.0775) → D4 re-read. Point estimates
  unchanged. **PROVISIONAL** until Neon's `ir_pipeline.py`/estimate diff is applied; dashboard and the
  migration handoff's D3–D4 text deliberately untouched.
- **eduengine driver:** the engine was correct; exits live in `e.exits`. Spot check at record defaults:
  liquidity push-out **35.7 %** of the child population under cash-only affordability vs **20.3 %**
  under credit+poverty-line need; quota rationing appears only in the quota arm.
- **edsystem-tests:** supported rows **49 → 45**; the four dropped are exactly Neon's flags
  (supply→`formal_share_gdp`, learning→`tut_rate` ×2, jobs→`skill_premium`), now `not_estimable`.
  Strict per-cell disclosure: 17/45 supported rows contain ≥1 cell sign flip; only 6/45 have a flip
  ≥10 % of the pooled effect. New `TEST_PREREGISTRATION_DEVIATION.md` logs the "no p-values"
  pre-registration violation.
- **test bench:** F9 **REJECTED (does not beat both benchmarks)** — n=1,495, 135 countries, 5 folds,
  model RMSE 0.2381 vs persistence 0.2855 vs null 0.2311; 2/5 folds beat both; β −0.2531 (SE 0.0322);
  spec sign share 1.00. F10 construct divergence n=14,578, median |Δ| 0.284. Q1 permutation PASS
  (0.15). F1–F8 / E8 / PHL / ablation / multiverse swap stay UNTESTABLE (data or code absent).
  Data committed under `data/` with `PROVENANCE.json` + `MANIFEST.sha256` (all verify).

## Still open (Neon patch order)

5. **equation-suite** — apply Neon's two diffs; then the math fixes above; re-run and correct
   `SUITE_REPORT.md` framing (only S4 is a clearly pre-declared FAIL; S3/S6 post hoc; S10's dropped
   pre-registered rule fails).
6. **tutoring / gate-jobs v6** — `_record()` spend double-count when `spend_feedback=False`, MNL
   price/option mismatch vs Bray, fractional-mass vacancy (4× over-hiring), quota double-count,
   Tullock invariance, v6 not wired to runner; plus Neon's gate-jobs tail files.
7. **Re-run the 144×10 / 144×40 multiverse** with the fixed driver (needs the box; currently HELD
   pending the operator's explicit go-ahead).
8. **`ir_pipeline.py`** — Neon's diff; microdata blockers (v190, region×round, CMC, weights,
   survey_type, MIS/AIS, clustering) remain.

## Server / environment notes

- Live box: `ssh -p 45973 root@connect.cqa1.seetacloud.com`, host
  `autodl-container-a8f742b5ee-292349c5` (alive again after the incident).
- **MCP `autodl` is stale**: `~/.dsh/mcp/autodl/work/autodl-connection.json` points at dead
  `region-9.autodl.pro:36667`. Use direct SSH. When the box is off, the proxy accepts TCP then closes
  with no SSH banner — that is the signature to check before diagnosing a network fault.
- **No agent may change power state (see POWER RULES below).** Do not run `shutdown`, `reboot`,
  `poweroff`, any wrapper, or any watcher/timer that could power off or restart the instance.
- Pulled artefacts (host): `~/neon-boot/pulled/` — corrected DHS results, eqsuite new results,
  edsystem 40-seed multiverse JSON, migration run, testbench data. Residual risk:
  `gate-jobs/record/results` and `observed-core/results` were sized but not pulled before the incident;
  both are committed on their branches.
- Queue state at the incident: all ten equation-suite scripts exit 0; the queue's JOB3 failed
  instantly (`--seed-offset` is not a supported flag of `run_edsystem_multiverse.py`) — fix the queue
  script before relying on its repeat block.

---

## POWER RULES — non-negotiable (verbatim, from `~/neon-boot/POWER_RULES_2026-11-25.md`)

### What happened
At 00:26 CST an agent-authored watcher `/root/work/queue/shutdown_after_two.sh` was written onto the
AutoDL box. It waited for `DHS_DONE` + `EDSYS_DONE`, slept 60 s, checked for a cancel flag named
`CANCEL_TWO_SHUTDOWN` (which did not exist; only `CANCEL_SHUTDOWN` did), then ran `shutdown -h now`.
It fired at **16:31:04 UTC = 00:31:04 CST**, powering the instance off mid-session.

**Authorship (forensic, read-only):** the author was a **lingering agent from the retired window**, not
this session's Commander and not the Lead. Evidence: `/root/work/run_neon_fix.sh` has mtime 00:17 — before
this session's first action at 00:18; the dhs-api estimate/corrected-reduction edits are 00:15–00:20; the
corrected-multiverse artifacts under `/root/work/edsystem` are 00:29–00:30; and that same worker wrote
`shutdown_after_two.sh` (00:26) plus its own `DHS_DONE`/`EDSYS_DONE` markers (00:27/00:30). Commander's
command inventory over the box is read-only and consistent with this.

The operator recovered it. The 7-minute timer the Lead armed was NOT the trigger (it would have fired
6 minutes later), but it was of the same class of mistake and has been deleted.

### Rules — absolute, no exceptions, no agent interpretation
1. **No agent may power off, shut down, reboot, stop, or restart the AutoDL instance, ever.**
   Not via `shutdown`, `reboot`, `poweroff`, the AutoDL stub, the console, an API, or a wrapper.
2. **No agent may create, arm, edit, or re-enable any watcher, timer, cron, `at` job, or script whose
   effect is to power the machine off or restart it.** Includes "shutdown when done" patterns of any kind.
3. **No standing rules.** A power decision is made by the operator, in-conversation, for one specific
   action, immediately before that action. Never infer it from silence, a handoff, or a past message.
4. Existing agent-authored watchers on the box are defused and renamed `*.DISABLED_2026-11-25`;
   `CANCEL_SHUTDOWN` and `CANCEL_TWO_SHUTDOWN` flags are present. Do not reverse this.
5. If an agent believes the instance should be powered down, it says so and stops. It does not act.

### Current state (verified)
- Instance alive: `autodl-container-a8f742b5ee-292349c5`, `ssh -p 45973 root@connect.cqa1.seetacloud.com`, key auth.
- Both shutdown watchers renamed `.DISABLED_2026-11-25`; no shutdown-capable process running.
- No DSH schedules armed in the Lead session.
