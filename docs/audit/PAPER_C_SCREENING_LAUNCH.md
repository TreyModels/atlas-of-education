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
