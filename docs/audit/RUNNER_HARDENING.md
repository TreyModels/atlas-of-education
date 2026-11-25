# RUNNER HARDENING — Gate-2 precondition #3 (task-13)

**Status:** IMPLEMENTED + host-tested; box smoke + final evidence in this document's §5.
**Owner:** `audit-runner` · **Branch:** `research/contest-audit-v2-2026-11-25`
**Incident:** [`GATE1_POOL_HANG_INCIDENT.md`](GATE1_POOL_HANG_INCIDENT.md) — authoritative 540-run host process hung in
the `ProcessPoolExecutor` completion/aggregation phase (all workers done, 0 % CPU, no output, stale pipes, blocked in
`pymain`; PID 63896, stack [`HANG_63896.txt`](HANG_63896.txt)); second attempt slowed by orphaned workers after a
naive `kill -9 <main>`.
**Model numerics: UNCHANGED.** The hardening edits only the execution layer; the model functions
(`_with_g12_share`, `_with_dv_scale`, `build_arms`, `_run_single`, `_stats`) are byte-identical to the pre-hardening
file (`dd0b1d8d…`) and a test asserts their AST source hashes on every run.

---

## 1. What changed (all in `papers/shadow-education-contest/code/run_hk_korea_comparative.py`)

| requirement (task-13) | mechanism |
|---|---|
| **1. incremental per-arm checkpointing** | Each seed result is written **by the worker that computed it** to `seeds/<jur>__<arm>__seedNN.json`, atomically (same-dir `os.replace`). When all of an arm's seeds exist, the host writes `arms/<jur>__<arm>.json` atomically (including `content_sha256`). A completion-phase hang therefore loses at most the seed/arm in flight, never the run. |
| **2. resumable driver, content-hash skip, atomic final assembly** | The driver validates every checkpoint on start (`row_sha256` over canonical JSON, `params_sha256`, engine fingerprint, schema); invalid files are discarded and recomputed; valid ones are skipped. It spawns the pool **only for missing tasks**. The final JSON is assembled from checkpoint files and written with the same atomic tmp+rename; `run_manifest.json` records `resumed`, `checkpointed_before_run`, `computed_this_run`, workers, fingerprint, output sha256. |
| **3. per-arm watchdog + process-GROUP kill + stall evidence** | Host enforces `--seed-timeout` (single result) and `--arm-timeout` (one arm). The driver independently watches checkpoint progress (`progress.json` token + seed-file count) against `--stall-timeout`; on a stall it writes `stall_<utc>.json` (reason, host pid/pgid, checkpoint index, last-progress time, `ps` snapshot, host-log tail) and kills the **whole process group**: `killpg(SIGTERM)` → grace (`--kill-grace`) → `killpg(SIGKILL)`. The host is launched with `start_new_session=True`, so its pool children are in the killable group (the incident's orphaned-workers failure mode). |
| **4. memory-aware worker cap / no unbounded result pickling** | `default_workers()` = min(cpu−2, 6, memory-derived cap) with `HK_MAX_WORKERS` override; the memory model reserves 2.5 GiB for OS/other lanes at 700 MiB/worker (the incident had 11 compute processes on an 8 GiB host). Workers **never send result payloads through pipes**: the row is written to disk in the worker and only a 4-element status tuple is returned; the parent holds no result list. |
| **5. loud failure, no silent partial** | Any failure → non-zero exit (3 stall, 4 host error, 5 incomplete, 2 config/fingerprint), `run_failure.json` with kind/reason/checkpoint index/kill signals, **no final JSON is written**, checkpoints preserved. A host exit code 0 is not trusted: the driver re-validates every checkpoint before aggregating. |
| **6. tests** | `docs/audit/code/test_runner_hardening.py` (6 pytest tests, real engine on tiny matrices) + `docs/audit/code/smoke_checkpoint_resume.py` (6-arm × 2-seed real-engine straight/interrupt/resume/aggregate equivalence report). |

**Fingerprint safety:** `fingerprint.json` pins the run to the exact `eduengine` source bytes + arm parameter hashes +
seed grid. After engine repairs (`core.py` now `72cbddf7…`) old checkpoints are **refused** (`exit 2`) unless
`--fresh` archives them — no silent mixing of pre/post-repair numbers.

**CLI:** unchanged default (`python run_hk_korea_comparative.py`) now runs the hardened driver and writes the same
output JSON; new flags: `--checkpoint-dir`, `--workers`, `--seed-timeout`, `--arm-timeout`, `--stall-timeout`,
`--kill-grace`, `--smoke-arms N` (N per jurisdiction; 3 → 6 arms), `--smoke-seeds N`, `--fresh`, `--dry-run`.
Checkpoints are also a **campaign primitive**: a killed 1,640-run Exp-3 job resumes from its last completed seed.

## 2. Exit codes / artifacts

| code | meaning | artifacts |
|---|---|---|
| 0 | success | final JSON + `run_manifest.json` (`status: ok`, `final_json_written: true`) |
| 3 | watchdog stall (seed/arm/completion); group killed | `stall_<utc>.json`, `run_failure.json` (`failure_kind: stall`, kill signals), partial checkpoints |
| 4 | host/worker error | `host_failure.json`, `run_failure.json` |
| 5 | incomplete/invalid checkpoints after host rc=0 | `run_failure.json` |
| 2 | fingerprint mismatch / bad config (no run) | refusal message; existing checkpoints untouched |

## 3. Test evidence (host)

Command:
```
PYTHONPATH="$PWD/engine" /Users/treymenefee/neon-boot/venv/bin/python -m pytest \
    docs/audit/code/test_runner_hardening.py -q
```
Host run: **6/6 PASS** (see §5 for the dated record; the suite takes ~10–15 min because every case runs real
engine seeds). The six tests:
1. `test_model_layer_numerically_frozen` — AST source hashes of the five model functions unchanged.
2. `test_dry_run_writes_fingerprint` — resume index + fingerprint only, no work.
3. `test_stalled_worker_group_kill_then_resume` — worker hangs (`stall_worker` test hook) → rc 3, stall evidence,
   `killpg` TERM seen, host pgid dead, no final JSON, partial checkpoints → resume rc 0, **final values identical to
   a straight run**, only the missing rows recomputed.
4. `test_completion_stall_then_resume` — host checkpoints all work then never returns (the incident's signature) →
   rc 3, all seed checkpoints preserved, no final JSON → resume with **0 tasks to compute**, values identical.
5. `test_corrupt_checkpoint_recomputed` — tampered row detected via `row_sha256`, exactly that seed recomputed.
6. `test_fingerprint_mismatch_refuses_without_fresh` — after a simulated code/param change: exit 2; `--fresh` archives
   the old checkpoint dir and proceeds.

## 4. Smoke evidence (6 arms × 2 seeds; checkpoint/resume equivalence)

Command (host or box; `--workers` ≤2):
```
PYTHONPATH="$PWD/engine" python docs/audit/code/smoke_checkpoint_resume.py \
    --workers 1 --arms-per-jur 3 --seeds 2 --report docs/audit/results/RUNNER_SMOKE_<host>.json
```
Passes: (1) straight 12-run reference; (2) mid-run watchdog kill (half the seeds checkpointed) → non-zero exit,
`run_failure.json`, partial index; (3) resume → values identical to (1); (4) aggregate-only re-run → 0 tasks computed,
values identical. Result is machine-readable in the report JSON (`assertions` + `passed`).

| host | python / numpy | workers | straight | interrupted (watchdog) | resume | aggregate-only | values equal |
|---|---|---|---|---|---|---|---|
| **box** `/root/work/audit13`, declared venv | 3.10.8 / 2.2.6 | 1 | rc 0, **311.72 s**, 12 rows | **rc 3**, 73.99 s, 1/12 rows preserved, no final JSON | rc 0, **296.62 s**, computed=11, `resumed=true` | rc 0, 0.32 s, computed=0 | **YES** |
| **host** macOS M1 | 3.10.2 / 2.2.6 | 2 | rc 0, **397.20 s**, 12 rows | **rc 3**, 122.04 s, 2/12 rows preserved, no final JSON | rc 0, **256.64 s**, computed=10, `resumed=true` | rc 0, 0.78 s, computed=0 | **YES** |

`RUNNER_SMOKE_box.json` sha256 `20a6160e4cd18e8d027c5588cb5deac533c8fc1e9847854bada412623533b686`
(copied to `docs/audit/results/box_evidence/`); `RUNNER_SMOKE_host.json` sha256
`e78ec97d897ce844bee60bfa9f1d92428608a7bfe6b8f0e9177a3174df048035`; pytest log
`docs/audit/results/RUNNER_HARDENING_PYTEST_host.log`.**

## 5. Dated execution record

- **2026-11-25 16:01–16:33 CST — implementation (host).** Hardened runner written; model functions AST-verified
  byte-identical to the pre-hardening file (`dd0b1d8d…`); 2-arm×2-seed manual straight/resume/aggregate equivalence
  and both stall-kill/resume paths PASS on host. Committed as **`4a3bd7c`** on
  `research/contest-audit-v2-2026-11-25` (runner sha256 `d1c60f0340d6607cfd0833562d4014e8ff60df0af13a8fc15786779b9920bd73`).
- **2026-11-25 16:34:27–16:56:17 CST — host pytest suite.** `pytest docs/audit/code/test_runner_hardening.py -q`
  → **6 passed in 533.03 s** (log: `docs/audit/results/RUNNER_HARDENING_PYTEST_host.log`). The suite runs real
  engine seeds; the stall/aggregation tests each take ~45 s of deliberate stall before the watchdog fires.
- **2026-11-25 16:34:27–16:47 CST — host smoke** (2 workers): straight 12 runs rc 0 / 397.2 s; simulated watchdog
  kill rc 3 / 122.0 s with 2/12 rows preserved and no final JSON; resume rc 0 / 256.6 s (computed=10); aggregate-only
  rc 0 / 0.78 s; **values equal after stripping `elapsed_seconds`.** Report sha256 `e78ec97d…8035`.
- **2026-11-25 16:34:30–16:45:06 CST — box smoke** from committed SHA `4a3bd7c`, read-only deploy to
  `/root/work/audit13`, `/root/work/venv-declared/bin/python` 3.10.8 / numpy 2.2.6, **1 compute worker**
  (PID 24170 smoke driver → 24172 hardened driver → 24173 host/pool; process group `start_new_session`),
  `nice -n 10`, OPENBLAS/MKL/OMP=1: straight rc 0 / 311.72 s, interrupted **rc 3 / 73.99 s** (1/12 rows preserved,
  `run_failure.json` + `stall_20261125T084017Z.json`, no final JSON), resume rc 0 / 296.62 s (computed=11,
  `resumed=true`), aggregate-only rc 0 / 0.32 s (computed=0); **value equality TRUE for both.** Report
  `/root/work/audit13/RUNNER_SMOKE_box.json` sha256 `20a6160e…b686` (copied to
  `docs/audit/results/box_evidence/`); intermediates kept under `/root/work/audit13/smoke_work/`.
  Independently verified on the box by compute-controller (same sha256).
- **Gate-2 precondition #3 verdict: MET.** A mid-run kill loses only the in-flight seed (observed: 1/12 on the box,
  2/12 on the host at the moment of the watchdog kill); the completed-index run resumes to values identical to a
  straight run; and a simulated worker/completion hang aborts **loudly** (rc 3, `run_failure.json`, partial index,
  process-group SIGTERM→SIGKILL) instead of hanging or emitting a silent partial.

## 6. Limits

- The watchdog bound is time-based, not causality-based: a *legitimately* slow seed > `--seed-timeout` aborts the run
  (default 600 s; a seed is ~15 s). Operators of a long campaign may raise these flags; the run_failure/stall evidence
  makes the choice auditable.
- The macOS host can still be OOM-killed externally (out of scope); the memory-aware cap plus checkpointing bounds the
  loss to the in-flight seed and makes resume trivial.
- GPU-bundle execution is unaffected (separate `fixed_harness/`).

## 7. Deliverables (task-13)

| file | role |
|---|---|
| `papers/shadow-education-contest/code/run_hk_korea_comparative.py` | hardened runner (model layer untouched) |
| `docs/audit/code/test_runner_hardening.py` | 6-test pytest suite (model freeze, stall-kill, completion-stall, resume, corrupt checkpoint, fingerprint guard) |
| `docs/audit/code/smoke_checkpoint_resume.py` | 6-arm × 2-seed straight/interrupt/resume/aggregate equivalence report |
| `docs/audit/results/RUNNER_SMOKE_box.json` + `box_evidence/` | box smoke report, log, stall evidence, run_failure, manifests (intermediates kept in `/root/work/audit13/smoke_work/`) |
| `docs/audit/results/RUNNER_SMOKE_host.json`, `RUNNER_SMOKE_host.log` | host smoke report + log |
| `docs/audit/results/RUNNER_HARDENING_PYTEST_host.log` | full pytest output (6 passed) |
| `docs/audit/RUNNER_HARDENING.md` | this document (design, exit codes, tests, evidence, limits) |

Commit: `4a3bd7c` (runner + tests + smoke script + doc skeleton); evidence commit follows this file's final version.
No GPU, no model-numeric changes; the runner writes the same output JSON schema as before.
