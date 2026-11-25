# GATE-1 HARDENING — ProcessPoolExecutor completion-phase hang (incident + bounded reproduction)

**Status:** observed once during the Gate-1 authoritative 540 run; **not reproduced** in 10 bounded trials of the
pool/orchestration path; root cause not proven; recorded as a **first-class wave-2 residual risk**. It is **loud, not
corrupting**: the failed run wrote no output file and no partial table was ever treated as a result. Hardening item
added for wave 2: **incremental checkpointing** (per-arm/per-seed result files written as they complete, atomic final
assembly), so a completion-phase failure can never lose ~6 × 18.6 CPU-min again.

## What was observed (first attempt, 2026-11-25 ~14:56–15:26)

* Command: clean `git archive 98baf6b` tree, `/tmp/gate1-540`, `python papers/.../run_hk_korea_comparative.py`
  with `workers=6`, `chunksize=4`, host macOS arm64 py 3.10.2, 8 cores.
* The runner printed only `Running 540 simulations (18 arms x 30 seeds) on 6 workers...`.
* All worker compute completed: each of the six workers had accumulated **18 min 34–35 s CPU time** (≈ 6 × 1,115
  CPU-s = 6,690 CPU-s, consistent with a completed 540-run workload at repaired-engine cost).
* Then **no further progress**: main process 0.0 % CPU, state `S`, workers gone, **no output JSON**, `lsof` showed 12
  stale PIPE fds to dead workers, `sample` showed the process blocked inside `pymain`/`run_file` (i.e. Python-level
  wait, not compute), no traceback in stderr. Killed at 15:26.
* Context: at that time the host also carried qa-verifier's DGP run (4 workers) + contest-math task-9 (1), i.e. 11
  compute processes on an **8 GiB** host → memory pressure (Mach free pages were near-exhausted at points).

## Bounded reproduction attempt 1 (INVALID — operator error, loud failure)

A trivial 540-task `ProcessPoolExecutor(max_workers=8)`, `ex.map(..., chunksize=2)`, `list()` script **without an
`if __name__ == "__main__":` guard** raised
`concurrent.futures.process.BrokenProcessPool: A process in the process pool was terminated abruptly ...` on macOS
(spawn start method re-imports the main module in workers). This is **not** a reproduction of the silent hang; it is
recorded only to show that when Python *does* detect a broken worker it fails loudly. Script discarded.

## Bounded reproduction attempt 2 (valid — no hang)

Corrected script (guarded `main`, macOS-spawn-safe), same orchestration path as the runner
(`ex.map(worker, range(540), chunksize=2)`, `list()`), trivial payload, 5 trials at 6 workers and 5 at 8 workers:

```
workers=6 trial=0..4: OK n=540 wall=0.41–0.47 s each
workers=8 trial=0..4: OK n=540 wall=0.53–0.59 s each
→ NO HANG REPRODUCED in 10 x 540-task trials
```

**Interpretation:** the hang is not a deterministic property of the pool/chunksize path. The evidence is consistent
with an **external worker termination under host memory pressure** (the completion phase then waits on a pipe that
will never produce a result), but the exact termination cause was not captured (no OOM/jetsam log at run time).
**Therefore it stays an UNRESOLVED residual risk**, not something to explain away.

## Hardening items (wave 2, recorded in the Gate-1 report)

1. **Incremental checkpointing** in every long runner: write per-(arm, seed) JSON as soon as each result returns
   (atomic rename), keep a resume index; assemble the final artifact atomically. A completion-phase failure then loses
   at most one chunk.
2. **Memory-aware worker caps** on the 8 GiB host: do not co-schedule two engine-heavy pools (observed condition);
   cap a single full-size 540 pool at 6 workers while other lanes are active.
3. **Watchdog on the collection phase** (bounded wait on each future; if a future exceeds the expected per-run time
   by >5×, abort loudly with the partial index rather than hanging).
4. Re-run this bounded reproduction on the final wave-2 runner to confirm the hardening holds; document that the
   original silent hang remains unreproduced.

## Addendum — root cause of the second slow-down (orphaned workers) and kill semantics

After the first attempt was killed with `kill -9 <main> <wrapper>`, its **six worker processes survived** (macOS uses
the `spawn` start method; workers are children of the main process but reparent to PID 1 on its death and keep
computing). During the restart they were still each burning ~38 % CPU and holding memory, with the host swapping
(swap used 4.0 GB of 5.1 GB) and load average >130 on 8 cores. This explains the second slow-down (new run's workers
stuck at ~32 %→64 % CPU). The orphans were identified by elapsed time (38 min) and killed one by one at ~15:34; the
restart immediately recovered to ~64 %/worker.

**Operational lesson (wave-2 hardening item 0):** kill the whole **process group / all descendants**, not the main
PID: on macOS inspect `pgrep -P <main>` and then the reparented `multiprocessing.spawn` children (`pgrep -f
'multiprocessing.spawn'`, check their elapsed time), or launch long pools with `setsid` so a single group kill is
possible. This is added to the wave-2 hardening list alongside incremental checkpointing. It is an environment
orchestration defect, not a model defect, and no result was corrupted.
