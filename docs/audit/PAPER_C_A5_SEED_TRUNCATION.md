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
