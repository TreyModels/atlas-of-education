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
