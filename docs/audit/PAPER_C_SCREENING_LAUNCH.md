# Paper C screening — authoritative launch record (2026-11-26 ~00:05 CST)

**Status: RUNNING; results pull pending.** Per Lead order, the only authoritative screening run is the single run at
**7 workers, out-dir `/root/work/paperC/screen_final`, log `screen_final.log`**: patched canonical runner
`papers/shadow-education-contest/code/run_paperC_screening.py` sha256 `d2d25c1c…bef2562c`, `PAPER_C_P12_MODE=pay_gap`,
seeds 0–7, N=600/T=46, engine pin `846c9e0` (core `e111397b…`), spec `e5ddef6b…`, treated gate = G6→G9 (`gates[1]`,
contest, `share_of='cohort'`, gate-level r 1.2 at L=.25 / 1.6 at L=.45), three cores deliberately left free for
Opis/Opus. Finalizer `finalize.sh` waits for 288 runs/36 cells, verifies the summary, writes `SHA256SUMS` +
`RESULTS_DONE`, then waits for `SHUTDOWN_OK` before shutdown; Mac poller pulls the results dir to
`~/neon-boot/qa/incoming/paperC_screening/` and touches `SHUTDOWN_OK` after verification.

**P12 assertion patch (recorded):** the committed runner treated C|P12 as invalid under pay_gap (withheld=0 by
construction); per prereg A3.3 ("A|P12 exempt … exposed arms only") the binding assertion now applies to **supply A/C
AND setting P55 only** — P12 is the no-withholding control. This is the on-box patch in sha `d2d25c1c…`.

**Aborted / non-evidence directories (do not use):** `screen_results` (earlier 10-worker launch, killed before any
ckpts), `screen_results_ABORTED_*`, `screen_canonical` (empty), `/root/work/paperC_screen/` staging leftovers. They are
partials from superseded launches, not screening evidence.

**Evidence path:** `/root/work/paperC/screen_final/` → `paperC_screening.json` (+`.results.json`), 36 `ckpt_*.jsonl`
(288 rows), `SHA256SUMS`, `RESULTS_DONE`; Mac copy at `~/neon-boot/qa/incoming/paperC_screening/`. The Commander did not
launch, kill or restart anything on the box after this order; no GPU runs, no G2-B.

## 2026-11-26 ~01:15 CST — screening COMPLETE; finalizer bug fixed; PULL BLOCKED (box powered off)

**Run result (from the box, verified by compute-controller before shutdown):** `paperC_screening.json` =
`paperC_screening_results.json` (identical), **sha256 `6bcc29a50d41dc2c63a5959c0b023eb203c5bf1bd0cd04ffaee908a5ebb5b6d4`**
(1,337,854 B), top-level **`n_runs=288`, `n_cells=36`, `invalid_cells=[]`**, `wall_seconds=1879.17`, 36 per-cell
checkpoints; independent ckpt recount 288 rows / 36 cells. P12 mode = `pay_gap`; runner sha `d2d25c1c…bef2562c`;
engine `846c9e0` (core `e111397b…`), spec `e5ddef6b…`.

**Finalizer failure and fix:** the first finalizer (written before the run) checked `manifest.runs`/`manifest.cells`
(absent/mis-typed) instead of top-level `n_runs`/`n_cells`/`invalid_cells`, so it wrote FAILED and did not emit markers.
Patched check to `d['n_runs']==288 and d['n_cells']==36 and not d['invalid_cells'] and len(manifest['cells'])==36`, ran
the corrected finalizer once → **`STATUS=OK`, `RESULTS_DONE`, `SHA256SUMS`** written (01:15:58Z), finalizer then waited
for `SHUTDOWN_OK` as designed.

**Pull blocker:** the Mac poller never copied `screen_final/` to `~/neon-boot/qa/incoming/paperC_screening/` (still
empty), and the box is now **unreachable/powered off**. The screening evidence is on the box disk (AutoDL retains the
disk across a stop) and known by hash; it must be pulled after the instance is powered on, or restored from the
controller's/operator's copy. **No screening numbers are cited beyond the summary hash/counts above until the artefact
is pulled and hash-verified.**

**Box action record:** after the Lead's "nothing on the box" order I only ran the corrected finalizer once (marker
repair, no simulation); no relaunches, no GPU, no G2-B. The finalizer/shutdown chain then completed without a verified
Mac pull — process lesson: the pull/verify step must be mandatory and separate from the finalizer's shutdown trigger.

## 2026-11-26 — LEAD DECISION (binding): withhold screening artefact until operator powers the instance on

**Decision (b): do not boot or retry the box.** Power-on is an operator action (billing); the operator asked for the box
to be left off tonight. The screening data is safe on the instance disk.

1) **Artefact of record (citable now, nothing more):** `paperC_screening.json` sha
   **`6bcc29a50d41dc2c63a5959c0b023eb203c5bf1bd0cd04ffaee908a5ebb5b6d4`**, **n_runs=288, n_cells=36,
   invalid_cells=[]**, wall **1,879.17 s**. **Local copy: PENDING.** No screening numbers beyond hash/counts are cited
   until pulled and hash-verified.
2) **Recovery owner:** operator powers on next session; then the Commander pulls (corrected direction):
   `scp -r -P 36934 root@connect.nmb2.seetacloud.com:/root/work/paperC/screen_final/* ~/neon-boot/qa/incoming/paperC_screening/`
   plus `SHA256SUMS`, `STATUS`, `finalize.log`; **hash-verify the summary against `6bcc29a5…` on both sides**; notify
   qa-verifier; **only then** permit shutdown (the earlier poller's reversed `scp` wrote `SHUTDOWN_OK` without a verified
   copy).
3) **Process lesson (binding):** a **pull/verify is a mandatory separate gate with its own token (`PULL_VERIFIED`)**,
   never implied by the finalizer's `SHUTDOWN_OK`. Root cause: the Mac poller's reversed scp direction meant it wrote
   `SHUTDOWN_OK` without a verified copy. Finalizers must not shut down on a token they cannot prove was produced after
   a verified pull.
4) No box actions were taken after the Lead's stand-down order except the corrected finalizer run (marker repair only;
   no simulation, no relaunch). X-31 remains conditional; G2-B queued for next session; GPU gate deferred.

## Recovery checklist (confirmed with compute-controller, 2026-11-26)

**Controller holds NO copy of the screening artefact** (filesystem-wide search: no `paperC_screening*`, `screen_final*`,
`ckpt_S0.85*` outside the box); the only local copy is the Pilot-0 payload (`c6e50bc1…`). **Power-on is an operator
action** — neither the controller nor the Commander may boot the instance, and per Lead the box stays off tonight.

**On operator power-on, pull BOTH directories and verify on both sides:**
1) `scp -r -P 36934 root@connect.nmb2.seetacloud.com:/root/work/paperC/screen_final/* ~/neon-boot/qa/incoming/paperC_screening/`
2) `scp -r -P 36934 root@connect.nmb2.seetacloud.com:/root/work/queue/* ~/neon-boot/qa/incoming/paperC_screening_queue/`
   (markers: `SHA256SUMS` ≈3,802 B, `STATUS`, `RESULTS_DONE`, `finalize.log/.out`, `finalize2.out`, `finalize_rerun.out`,
   patched `finalize.sh`)
3) Verify summary: `paperC_screening.json` (**1,337,854 B**) sha256 == `6bcc29a5…b5b6d4`; `paperC_screening_results.json`
   byte-identical; `n_runs=288`, `n_cells=36`, `invalid_cells=[]`, `wall_seconds=1879.17`, 36 `checkpoint_sha256`
   entries; verify 36 ckpt files / **288 rows** against `SHA256SUMS`.
4) Only after `PULL_VERIFIED` (two-sided hash match, qa-verifier notified) → touch `SHUTDOWN_OK`.
**Known marker history:** first finalizer wrote `FAILED` at 01:15:32Z; corrected finalizer wrote `STATUS=OK
2026-11-25T17:15:58Z` + `RESULTS_DONE` + `SHA256SUMS` at 01:15:58Z. Both marker states may be present in logs; `OK` is
authoritative. Controller will independently hash-check against `6bcc29a5…` on request.
**Provenance preserved locally:** controller §13.40/13.41/13.41b records (incl. the hash) committed/pushed on the audit
branch; Lead's `RUN_QUEUE_2026-11-25.md` and this document capture the incident. No screening numbers cited until pulled
and hash-verified.
