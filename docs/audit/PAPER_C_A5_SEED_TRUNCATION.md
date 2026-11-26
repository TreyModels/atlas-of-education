# Paper C — A5 amendment: pre-declared 16-seed confirmatory truncation (approved, 2026-11-26)

**Authority:** adjudication commit **`1c51f17`** (A5 approved before aggregation); Lead decision in flight to avoid the
measured compute overrun (confirmatory at 32 seeds was projecting ≈42–48 CPU-h against the pre-declared ≤22 CPU-h
envelope because the treated G6→G9 contest gate makes PL quadrature ~O(N²)).

**A5 rule (frozen before any outcome inspection):**
* Confirmatory uses **exactly 16 matched seeds, 100–115** (seeds **116–131 excluded**; no optional stopping, no
  effect-based stops/additions).
* The 6 frozen passers, all other design fields unchanged: passers `b64a69f0…` (adjudication `bbc0b92`), N=1500/T=46,
  engine pin `846c9e0` (core `e111397b…`), spec `e5ddef6b…`, runner `ddeffe42…` @ `1b3a510`, A4 `8c967eab…`,
  P12 = pay_gap no-withholding control, gate-level r 1.2/1.6 by L.
* **Estimands untouched:** T2 = `own_share_financial_proxy` (C−A), min +0.10, proxy caveat; T3 = `withheld`
  (A|P55−A|P12), min +0.05 with assertion support; Holm family **T2/T3 only** (m=2, α=.05). T1 (+0.655 vs ≥3.0) and
  T4 (+1.767 pp vs ≥2.0) remain **screening failures**, not confirmatorily tested. No S-generalisation beyond S=.85.
* **New envelope:** ≤**24 CPU-h**, wall ~3.5–4 h at 6 parallel cells. **Precision: SE ×√2 vs 32 seeds** (8→16 seeds);
  the report must give achieved CI/MDE and label results **A5 interim precision**, with **no full-precision claim**.
* **No outcome inspection before freeze:** only timings and row counts were observed (attested below); no per-cell
  effect was inspected. If outcome peeking had occurred, A5 would be invalid (full 32 seeds or exploratory only).

**Attestation:** before aggregation, the Commander observed only process CPU/wall/row counts and checkpoint line counts;
no `paperC_confirmatory` outcome values were read.

**Aggregation:** 16-seed aggregator over the per-cell checkpoints, seeds filtered to 100–115, writing
`paperC_confirmatory.json` with `n_runs=96`, `n_cells=6`, `invalid_cells=[]`, manifest citing this A5 record + the
frozen passers + runner/engine/spec hashes, 16-seed summary schema identical to screening (per-cell seed_stats/rows),
`SHA256SUMS` + `CONFIRM_RESULTS_DONE` markers for pull/verify. Full 32-seed fallback exists only if A5 is rejected
(overrun declared) — A5 **is approved**, so the confirmatory artefact is the 96-run one.

## Execution record (A5)

* **A5 record committed before aggregation:** this file sha256 `365155965423b4f9171b5ad69a87dd0ef11c0710b5216190d043beebfb16bf99`
  (commit `aa1d0bd`); manifest updated (`c8649511…`).
* **Stop-at-16 watchdog launched on box** (`/root/work/paperC/stop16.sh`, sha `ac979c9a…`, PID 2361, log
  `stop16.log`): waits until each cell's ckpt has ≥16 rows for seeds 100–115, then stops that cell's process; when all
  cells are stopped it runs the **16-seed aggregator** (`paperC_confirm_aggregate.py`, sha `223628668…`) → writes
  `paperC_confirmatory.json` (n_runs=96, n_cells=6, invalid=[]), `SHA256SUMS`, `CONFIRM_RESULTS_DONE`.
* **8-seed insurance snapshot** (`/root/work/paperC/snap8.sh`, watchdog) tars the ckpts at 8 seeds to
  `/root/work/paperC/snap8.tar.gz` (pullable if anything goes wrong at ~50 %).
* **Measured rate (pre-truncation):** ~13.5 min/seed/cell, ~809 CPU-s/run ⇒ 32-seed projection 43.2 CPU-h / 7.2 h wall;
  A5 16-seed envelope ≤24 CPU-h (wall ~3.6 h from 07:20 ⇒ ~10:55–11:15 CST). No outcome values inspected before freeze
  (attested; only timings/row counts observed).

**Provenance fixes (adjudication `b614b78`, before aggregation):** aggregator `paperC_confirm_aggregate.py` sha
`223628668355a1a68f16def0e0171fd7c528de6c82b536da2bc670857961c978` is **committed at `0324205`**; the confirmatory
manifest is corrected to **uncertainty = 16 matched seeds (A5, 100–115), SE×√2, no full-precision claim**, cites the
aggregator commit and the A5 approval (`1c51f17`), and reconciles `wall_note` (~21.6 CPU-h / ~3.6 h wall for the 16-seed
run) with `observed_runaway` (32-seed plan: 43.2 CPU-h / 7.2 h). The 8-seed snapshot is **non-inferential crash
insurance only** — it is not analysed and is not a stopping source.

## 2026-11-26 07:58 CST — A5 RUN STOPPED / VOID (Lead + operator relay; defects verified independently)

**Status: VOID / NO RESULT.** Lead stopped `confirm_a5` at **07:58 CST** on an operator relay (Claude/Opus → Trey) and
independently verified the defects from the screening artefact (not merely relayed):

1. **T3 is deterministic by construction:** `withheld` = exactly **0.144** in **96/96 exposed P55 runs** (1 distinct
   value; SE 0; arithmetic `h_max*(1-pay_ratio)*(1-monitoring) = 0.4*0.45*0.8`). It is a **setting**, not an estimand;
   more seeds cannot test it.
2. **T2 is a manipulation check:** `own_share` C ≈ 0.889–0.945 vs A ≈ 0.148–0.524 (SE ≈0.0003), driven by
   `firm_ban=.9` inside an **own/(own+firm)** outcome — the treatment input returns in the outcome, and the denominator
   embeds the treatment.
3. Consequently the m=2 (T2/T3) family can only "pass" while the substantive hypotheses **T1/T4 failed screening**;
   combined with the A5 narrowing (Holm m=2 vs prereg T1–T4) a confirmatory claim is indefensible.

**Execution state:** driver+cells killed (PIDs 2272/2273/2276–2285), finalizer killed, `queue/STOP_CONFIRM_A5` written;
**checkpoints preserved: 10 rows / 6 cells in `/root/work/paperC/confirm_a5/`; no aggregation, no summary JSON**;
Mac poller stopped. Box stays on (no shutdown; next-compute decision with operator/Lead). **Do not resume A5, do not
start a new confirmatory run.** The preserved rows are a failed-run record, not analysable.

**Redesign requirements recorded (Paper C confirmatory not runnable under this design; no claim):** behavioural
estimands not mechanically determined by treatment; treatment not in the outcome definition/denominator; pre-launch
degeneracy screen (distinct values/variance/input→output mapping; reject SE=0/input-derived); manipulation checks
separate; full pre-declared T1–T4 family for Holm (no post-screening narrowing); adequate power/MDE; pilot used for
variance only; no A5 data reuse; new **A6** prereg/manifest/runner pins.

**Communication/incident:** box SSH became unreachable ~07:45 CST (same network-side signature as 01:17; box is
**not** powered off — `uptime` 90 d; the finalizer `shutdown` was a container no-op). Controller monitoring is blind
until connectivity returns; `SHUTDOWN_OK` must not be touched.

## Carry-over: measured cost calibration (failed-run, not evidence) + path reconciliation

* **Measured N=1500 confirmatory cost (overrun telemetry, failed run):** **≈809 CPU-s/run, ≈13.5 min/seed/cell** (contested
  contest-gate configuration). Implication: 6 cells × 32 seeds ≈ **43 CPU-h / ~7.2 h wall at 6 concurrent**; if a future
  design is safely shardable, ≈26 CPU-h at 10 concurrent. Recorded as **failed-run cost calibration only — not evidence,
  not a claim**, for A6/v2 sizing.
* **Path reconciliation:** `/root/work/paperC/confirm_a5` is the clean A5 run (driver 2273, seeds 100–115, 6 workers,
  preserved 10 rows/6 ckpts, no summary, `queue/STOP_CONFIRM_A5`); `/root/work/paperC/confirm_final` is the earlier
  overrun run (driver 1364, workers 10, analysis-commit 8121bf6) which is **KILLED/ABANDONED with no outcomes used, no
  aggregation** (no `paperC_confirmatory.json`/`CONFIRM_RESULTS_DONE`). Any post-reconnect verification must check both
  paths and report them separately.
* **Reconnect verification checklist (armed by Commander + controller):** `queue/STOP_CONFIRM_A5` exists → confirm_a5
  has **10 rows / 6 ckpts, seeds 100–115, no `paperC_*.json`** and confirm_final has **no summary/aggregation** → no
  `run_paperC_screening` processes → hash `ckpt_*.jsonl`, copy read-only tarball to
  `~/neon-boot/qa/incoming/paperC_a5_void/`, report row counts/hashes to Lead + adjudicator, then stop. `SHUTDOWN_OK`
  stays untouched; no resume/relaunch.
