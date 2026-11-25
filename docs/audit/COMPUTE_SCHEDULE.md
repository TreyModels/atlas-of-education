# COMPUTE_SCHEDULE — Atlas contest audit v2 · box lane

scheduler: **`compute-controller`** (dedicated, does not run research) · box: **`autodl-container-wjb02xe512-3c3a2b3b`**
access: `/tmp/box_ssh.sh`, `/tmp/box_scp.sh` · interpreter `/root/miniconda3/bin/python` (3.10.8) · declared stack `/root/work/venv-declared` (numpy **2.2.6**)
branch: `research/contest-audit-v2-2026-11-25` · programme date 2026-11-25 (Asia/Shanghai)

status: **LIVE** — refreshed every ~2–3 min while jobs run. All times CST (box clock = host clock, checked 15:03:50).
Box-side ledger with PIDs/hashes: `/root/work/compute/ledger/COMPUTE_LEDGER.md` (+ legacy snapshot `/root/work/compute/legacy_snapshot/`).

---

## 1. TL;DR (last refresh 15:04:10 CST)

| item | value |
|---|---|
| quota | **10 CPUs** (`/sys/fs/cgroup/cpu.max = 1000000 100000`); `nproc`=80 is the host and is **misleading** |
| current utilization | **9.0 / 10 CPU (90 %)** at 15:12:07 — `cmd` 540 (6 workers, 9.0 % done) + `qa` task-7 (3 workers); contest-math 1-worker replication starting → 10.0/10 |
| band check | 90 % is **inside** the 8.5–10.0 target band; hard worker cap respected (see §3b for the withdrawn 540→8 proposal); `loadavg` 18.8 is host-wide and is not our container (see §2) |
| headline | **Gate-1 AFTER invariant suite is GREEN on the declared stack** (box replication: 27 passed in 56.73 s, 5 workers) |
| ETA (controller box 540) | 540 × ~31 CPU-s/run ÷ 6 workers ≈ 47 min from 15:07:45 → **~15:55**, now with the full 6 cores (legacy ended) |
| driver resolution | legacy "relaunch loop" = box-side **`run_parts.sh`**, a finite 4-part script (not an infinite watcher); killed 7×, re-issued by an external agent session within 5 s each time; current instance is being **allowed to finish** (§7) |
| ETA (commander host 540) | authoritative run; host is ≈2× faster per run (Apple core vs Xeon) → ≈22–25 min from 14:55 → ~15:17–15:20 |
| ETA (qa task-7 DGP) | **not yet launched**; provisional 100 populations × ~1 engine run ≈ 100 × 31 CPU-s = 0.86 CPU-h → ~9 min at 6 workers / 17 min at 3 workers (to be replaced by a measured pilot) |
| ETA (qa task-8 bootstrap) | not yet scoped; resampling of stored results, expect minutes not hours (confirm B and cells) |
| ETA (contest-math task-6) | analytic, no box pool: **< 5 s** single process (1,000 Jacobian evals, closed-form) — host; harness copy staged on box 15:02 |
| ETA (contest-math task-9) | ~200 `pl_win_probs` calls × 14–49 ms ≈ **3–10 s** + cheap scalar grid |
| ETA (audit-runner task-11) | box job **DONE** 15:00:49–15:00:52 (3 s, 1 worker, 18/18 assertions PASS, 12/12 manifest OK) |

**BIGGEST FINDING FOR THE PROGRAMME:** the **repaired engine is ~20–39× slower per simulation** than the legacy
engine. Measured on the box (isolated 1-process, same `build_arms()` config): HK Baseline **20.3–20.4 s/run**,
KR Baseline **41.9 s/run** (single-threaded CPU-seconds). The legacy engine did 540 runs in **71.9 s wall at 8 workers**
= **1.07 CPU-s/run** (`/root/work/gate0/run_box_8w.log`). Consequence: the 540-run campaign is **4.7–6.2 CPU-hours**
on the repaired engine, not ~10 CPU-min; every downstream campaign (G2 calibration, G3 policy) inherits this factor.
Plan compute against measured cost, not against the legacy 178.7 s / 540 figure.

---

## 2. Box ground rules (verified)

| rule | value |
|---|---|
| CPU quota | 10 CPUs cgroup. Never plan against `nproc`=80. |
| true utilization metric | `Δ usage_usec / Δt / 1e6` from `/sys/fs/cgroup/cpu.stat` (container-only) |
| `cat /proc/loadavg` | **HOST-wide**, not container-only: reads 13–25 all day even when our container is idle. Use as a secondary/flag metric only (target band as issued: 8.5–10.0, flag <7, >11), never as truth for our quota. |
| per-job rules | `nice -n 10`; `OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1`; single private dir per lane; no watchers/timers; **no GPU work**; **never shutdown/reboot/poweroff** |
| dirs ours | `/root/work/{gate0,qa,core,tut,venv-declared,cmd,audit,contest,compute}` |
| dirs legacy / read-only | `/root/work/{modelrev,gpu}` (never edit/kill `modelrev/pkg`; its `results/` is harvested + hashed) |
| deployment | lanes deploy read-only from a committed SHA (`git archive`); code edits only on the Mac worktree |
| declared stack | `/root/work/venv-declared` (py 3.10, numpy 2.2.6) — this **now has numpy** and was used for the Gate-1 AFTER box run, closing the Gate-0 numpy-floor caveat operationally |

---

## 3. Worker allocation (as issued 14:57, amended 15:03)

Total box budget **≤ 10 concurrent worker processes**, keep 1 slot for control/analysis when the box is saturated.

| lane | box cap | in use | queue (strict order) | note |
|---|---|---|---|---|
| `qa-verifier` | **3** | 3 | 1) Gate-1 AFTER suite ✅ done · 2) task-7 DGP 500 populations (5 configs × 100) — 1st config RUNNING since 15:10:40 (parent 15122 + workers 15124–15126) · 3) task-8 bootstrap factorial | pure NumPy ABC, 0 engine runs |
| `atlas-commander` | **6** | 6 | 540 repaired-engine **cross-environment replication** (authoritative 540 = host); `/root/work/cmd` now controller-managed | parent 14765 + workers 14767–14772, started 15:07:45 |
| `contest-math` | **1** | 0 | task-6 rank/Jacobian ~1,000 pts (analytic, ≤15 s single proc) · task-9 general-r Tulloch (~5–15 s) | box harness staged 15:02; releases immediately |
| `audit-runner` | **1** | 0 | task-11 harness/manifest/ledger (box job done, 3 s) | releases immediately |
| `engine-core`, `engine-tutoring` | **0** | 0 | host-only deterministic probes | no box jobs requested |
| control / reserve | **1** | 0–1 | monitoring, pilots | this scheduler |

### 3b. Cap arithmetic decision (15:13) — recorded for the operator

Lead proposed raising the 540 from 6 → 8 workers to fill the quota while qa runs 3. **Withdrawn at the scheduler's
recommendation, Lead concurred:** 8 + 3 = **11 worker processes > the hard 10 cap**, i.e. the "fill" would have
re-created oversubscription; and restarting the 540 to change its pool size would discard **9 % of completed CPU work**
(1,518 of 16,794 CPU-s). The 10th slot is instead filled by the only **non-duplicative** ready job — contest-math
task-9 box cross-env replication at exactly 1 process (host remains authoritative). Final split: **540 6 + qa 3 +
contest-math 1 = 10 workers = 10.0/10**, automatic trim if any lane asks for more.

Rules the scheduler enforces: total ≤ 10; a lane exceeding its cap is messaged and flagged here; a job with
no output progress for >10 min is messaged and flagged; any box job must report PID + worker count + ETA.

---

## 4. Queue / job board

| id | job | owner | workers | start (CST) | status | measured rate | ETA / done | output |
|---|---|---|---|---|---|---|---|---|
| J-01 | Gate-1 AFTER invariant suite, box replication (declared venv, numpy 2.2.6) | qa-verifier | 5 (test-12 caps pool ≤4 + parent) | 14:59:1x | ✅ DONE | 27 tests / 56.73 s | done ~15:00:10 | `/root/work/qa/AFTER_box.log` |
| J-02 | 540 repaired-engine cross-env replication | atlas-commander | 6 | 15:03:31 | **RUNNING** | ~31 CPU-s/run (pilot) → ~2.2 runs/min aggregate | ~15:50–16:00 | `/root/work/cmd/run_540.log`, then `papers/.../results/hk_korea_comparative_with_cf4.json` |
| J-03 | task-6 rank/Jacobian audit (~1,000 prior-box points) | contest-math | 1 (analytic; 0 pool) | ~15:02 | staging/analytic on host | 1 moment-map + Jacobian per point; 0 `pl_win_probs` calls | <5 s once launched | `/root/work/contest` harness currently staged |
| J-04 | task-11 harness/manifest/ledger box proof | audit-runner | 1 | 15:00:49 | ✅ DONE 15:00:52 | 3 s wall | done | `/root/work/audit/p07_box_evidence.tar.gz`, 18/18 PASS |
| J-05 | task-7 synthetic DGP (500 pops = 5 configs × 100, 20k draws × 16 moments, pure NumPy ABC) | qa-verifier | 3 | 15:10:40 | **RUNNING (config 1/5)** | 76 CPU-s/worker after 77 s; per-pop rate pending first artifact | first config ETA pending; total ~5 sequential configs | `/root/work/qa/full_out` (parquet, written at config end) |
| J-06 | task-8 bootstrap factorial | qa-verifier | ≤3 | blocked on J-05 | queued | unknown until scoped (resample stored results; expect minutes) | — | `/root/work/qa` |
| J-07 | task-9 general-r Tulloch validation | contest-math | 1 (analytic) | blocked on J-03 | queued | ~200 PL calls × 14–49 ms ≈ 3–10 s | <1 min | `/root/work/contest` |

Completed / released: J-01, J-04. No lane currently exceeds its cap.

---

## 5. Measured per-unit costs (box pilots, 2026-11-25)

Pilots were run from a clean `git archive 98baf6b` bundle in `/root/work/compute` (single process, single-thread BLAS,
`nice -n 10`), calling the real `_run_single()` from `papers/.../run_hk_korea_comparative.py`.

| pilot | unit | environment | measured cost | notes |
|---|---|---|---|---|
| P1 | HK Baseline 1 run (N=300, T=46) | miniconda py3.10.8 / numpy 1.24.1 | **20.38 s, 20.20 s** | CPU-bound, 100 % of one core |
| P1 | KR Baseline 1 run | miniconda / numpy 1.24.1 | **41.86 s** | 2.1× HK |
| P2 | HK Baseline 1 run | **declared venv** / numpy 2.2.6 | 33.5 s wall under 13-way contention (≈22 CPU-s) | wall inflated by legacy tenant; numpy 2.x is **not faster** |
| P2 | KR Baseline 1 run | declared venv / numpy 2.2.6 | 87.7 s wall under contention (≈57 CPU-s) | wall inflated; use isolated P1 numbers for planning |
| legacy | 540 runs, 8 workers (old engine) | miniconda / numpy 1.24.1 | **71.9 s wall = 575 CPU-s total = 1.07 CPU-s/run** | `/root/work/gate0/run_box_8w.log`; **20–39× faster than repaired** |
| — | Gate-1 invariant suite (27 tests) | declared venv, QA_WORKERS=5 | **56.73 s wall** | full suite, CPU-bound; host equivalent 132 s at 4 workers |
| — | task-11 dry-run harness | miniconda, 1 proc | **3 s wall** | 2 subprocesses, negligible |

Per-unit planning numbers (box, repaired engine): **HK arm = 20.3 CPU-s**, **KR arm = 41.9 CPU-s**,
**540-run mix (270 HK + 270 KR assumed 9+9 arms) = 16,794 CPU-s = 4.7 CPU-h**.

---

## 6. ETA model (measured, not guessed)

`wall ≈ N_units × CPU-s_per_unit / workers` (single-thread BLAS, so workers ≈ cores), plus a 5–10 % contention haircut.

**J-02 540 cross-env replication** (16,794 CPU-s):

| workers | wall | with +20 % contention |
|---|---|---|
| 4 | 70 min | 84 min |
| **6 (current)** | **47 min** | **56 min** |
| 8 | 35 min | 42 min |
| 10 (quota max) | 28 min | 34 min |

Started 15:03:31 → ETA **~15:50–16:00** at 6 workers. (At the 1-worker size the commander first chose on the box,
this job would have taken **4.7 h**; it was resized to 6 at 15:00 and relaunched 15:03.)

**J-05 task-7 DGP (provisional, replace with lane-reported pilot):** if 1 population ≈ 1 repaired-engine run,
100 populations = ~3,100 CPU-s → 17 min at 3 workers, 9 min at 6. If a population instead needs ~18-arm evaluation,
multiply by 18 → **5 + CPU-hours**: must be scoped before launch.

**Host vs box:** commander's single-run smoke test of KR Baseline seed 0 on the repaired engine took **20.1 s** on the
host vs **41.9 s** on the box — same numbers out (k12 58.12 / gap 30.39 / elite 20.85 / contest_e 0.0167), so the host is
≈2× faster per run. Host 540 at 6 workers ≈ 22–25 min. **The host, not the box, is the right place for latency-critical
engine campaigns when its cores are free.**

---

## 7. Legacy tenant retirement register (first job, and it is not over)

Goal: legacy `/root/work/modelrev` 1080-sim policy campaign relaunched contrary to its handover terms, occupying
8 of our 10 CPUs. Authorised to retire; `modelrev/pkg` never touched. Outputs recorded+hashed **before** each kill.

| # | time (CST) | what was killed | recorded before kill | result |
|---|---|---|---|---|
| 1 | ~14:56 | 14:50 relaunch: runner **9433**, workers **9561–9568** (8×99.8 %) | 6 files in `results/` hashed; `policy_arms_v1v2v3.json` sha256 `e1ce873a…d9025b`; snapshot to `/root/work/compute/legacy_snapshot/` | killed; box idle (0.10 CPU, 14:59) |
| 2 | ~15:01 | relaunch via sshd **9889**: launcher **9901** (`setsid nohup`, ppid 1), runner **9904**, workers **10031–10038** | no new files | killed (group `-9904` + sshd) |
| 3 | ~15:02 | relaunch via sshd **10590**: launcher **10622**, runner **10624**, workers **10751–10758** | no new files; restored completed `policy_arms_v1v2v3.json` from snapshot (sha256 `e1ce873a…` unchanged) | killed |
| 4 | ~15:03 | **variant sweep** starts: launcher **11430**, runner **11432**, workers **11638–11645**, `--variant V1_canonical --jur HK --partial` | no `part_*.json` (killed before flush) | killed |
| 5 | ~15:03:4x | `--variant V1_canonical --jur KR --partial`: launcher **12432**, runner **12433**, workers **12563+** | — | killed |
| 6 | ~15:04:0x | `--variant V2_g9_removed --jur KR --partial`: launcher **12645**, runner **12646**, workers **12774+** | — | killed |
| 7 | ~15:04:1x | `--variant V3_g9_no_consequence --jur KR --partial`: launcher **12928**, runner **12929**, workers **13057+** | — | killed; box 6.0 CPU (J-02 only) |
| 8 | **15:05:24** | relaunch #8 = **same finite script**: `bash -c` **13672** → `bash run_parts.sh` **13673** → runner **13677** → workers **13804–13811** | `run_parts.sh`: 651 B, mtime 15:03, sha256 **`1d29f163c21f5bbddf095c72de90270faa16edd2d7881eb56fe5e057be967862`** | **not killed** — allowed to self-terminate under the Lead-approved bounded plan (§7b) |

### 7a. Root cause (found 15:05:19)

The "relaunch loop" is a **box-side finite script**, not a watcher: `/root/work/modelrev/run_parts.sh` (written by the
external session at 15:03) loops over **4 parts** — `V1_canonical:HK`, `V1_canonical:KR`, `V2_g9_removed:KR`,
`V3_g9_no_consequence:KR` — each part = 270 sims (9 arms × 30 seeds) at 8 workers, `--partial`, skipping any part whose
JSON already exists, then `echo ALL_DONE` and **exits**. Killing a part makes the external agent re-issue the script
(observed: kill 15:05:19 → `pgrep` empty 15:05:23 → re-issued **15:05:24**, 5 s). The box-side launcher chain is always
short-lived `bash -c`; **there is no persistent Mac-side supervisor process** — each launch is a fresh `ssh`/expect
tool-call from another agent session, invisible to this scheduler's process scope. **Only the operator closing that
session is a permanent stop.**

### 7b. Bounded plan (Lead-approved 15:07)

Let relaunch #8 run to its natural `ALL_DONE` (~2 min/part × 4 ≈ **15:13–15:14**) instead of kill #9: the kill loop is
unwinnable from the box side and wastes more quota than a known-finite script. Conditions: (i) verify `ALL_DONE` +
`policy_chunks.log` + empty `pgrep` at ~15:14 and record hashes/PIDs here; (ii) if the external session launches the
**full 1080-sim run** instead, kill it immediately and report; (iii) legacy must not exceed 8 workers while our 540 runs;
(iv) qa task-7 must fill the freed slots. Container util during the overlap: **9.0/10 CPU (90 %)** — inside band.
Mitigation already applied: the completed `policy_arms_v1v2v3.json` is restored in place (sha256 `e1ce873a…d9025b`),
so any completion-signal check by the external session sees a complete run.
Why it could never complete on its own: each part is 270 sims × ~3.6 CPU-s/8 workers ≈ 2.1 min + startup, and the
external session's remote command is killed at its own tool-call timeout (observed: four invocations, four
`running 270 simulations` lines in `policy_chunks.log`, **zero `part_*.json`** written). A fresh invocation restarts
part 1 from scratch → the loop is structural, not malicious.

### 7c. Operator stop (final)

At **~15:07** the **operator ordered the external agent session to stop** (Lead relay). Final verification at 15:07:51:
`pgrep -fa 'run_hk_korea_canonical|run_parts'` **EMPTY**, no relaunch; legacy tenant is **ended by operator order** and
no further re-issue is expected. Final legacy artifact hashes (recorded 15:07:51; `modelrev/pkg` never touched):

```
1d29f163c21f5bbddf095c72de90270faa16edd2d7881eb56fe5e057be967862  /root/work/modelrev/run_parts.sh   (651 B, mtime 15:03)
2e77f1cbadf3a672889d972882a789735a3c12ee1612b76b75c0c4f61ad9876f  results/policy_chunks.log          (4 x "running 270 simulations", no part JSON)
fa04b8a97e8f17b9d2a4dc42dada8b622013eec298402bb6304e015f908ca7af  results/policy_run.log
3ccdf532703bab5e1b9d7b2f714061092a0e08b9780a087e2644982ac1f29097  results/run_all.log
e1ce873a0a106b9632fae97cf923ab6432ebc6e32043f64fb501d8c93ec9025b  results/policy_arms_v1v2v3.json    (restored completed 14:48 artifact)
205ac04dee9db63b1a2ed021adde9b636977d2e49dd3e910da63b3ab5a0a3d9f  results/calibration_bestfit_holdout.json
5e1dc73409bc6905531853861c4065dc1f64cef81f94e4e884e249c777bfe593  results/calibration_sweep.json
0448b72938ba697c56048ae89c5c5438c4b375935023e1231c46eaf6a827c956  results/calibrate_run.log
```

---

## 8. Utilization history (measured, container-only)

| time (CST) | `loadavg` (host) | CPU-equiv (cgroup) | active workers | note |
|---|---|---|---|---|
| 14:55:11 | 20.43 | **8.06** (81 %) | 8 legacy | pre-retirement; legacy tenant at 100 %×8 |
| 14:59:0x | 16.24 | **0.10** (1 %) | 0 | idle after kill #1 — harvest window |
| 15:00:3x | 25.40 | **3.0** (30 %) | legacy 8 + qa pytest 5 | kill #2 window, oversubscribed |
| 15:02:4x | 23.4 | **1.9** (19 %) | 1 | between relaunches |
| 15:03:2x | 13.4 | **2.0** (20 %) | 1 | 540 at 1 worker (pre-resize) |
| 15:05:19–24 | 20.9 | **10.0** (100 %) | legacy 8 + 540 6 | kill #7 at 15:05:19; relaunch #8 at 15:05:24 (5 s) |
| 15:06:40 | 18.4 | **9.0** (90 %) | legacy 8 + 540 6 (+1 contest parent) | bounded-plan overlap; inside band |
| **15:07:56** | **11.9** | **6.0** (60 %) | 540 6 | **legacy ENDED by operator order**; 6/10 → fill with qa task-7 |
| 15:0x (next refresh) | — | — | — | target 9.5–10/10: 540 6 + qa 3 + contest-math 1 = 10 |
| **15:12:07** | **18.8** | **9.0** (90 %) | 540 6 + qa 3 | qa task-7 live (config 1/5); 540 9.0 % done (1,518/16,794 CPU-s) |
| 15:14 (next refresh) | — | — | — | + contest-math 1-worker replication → **10.0/10** |

Band discipline: flag **<7** idle (fill from queue), **>11** oversubscribed (throttle the lowest-priority lane).
`loadavg` is host-wide and is reported only because it was the issued metric; the cgroup number is the truth.

---

## 9. Incidents & flags

1. **Legacy tenant driven by an external agent session** (§7). The box-side driver is a *finite* 4-part script
   (`run_parts.sh`, sha `1d29f163…`) that self-terminates; killing it only makes the external session re-issue it
   (5 s observed). Bounded plan: let it finish (~15:14) and verify. While it overlaps our 540, our workers get
   ~60–75 % of a core each → 540 ETA +~15 %. **Permanent fix: operator closes the external agent window.**
2. **Repaired engine is 20–39× slower than legacy** (§1/§5). Planning consequence: the repaired-engine 540 is
   ~4.7–6.2 CPU-h, and G2/G3 campaigns must be costed from engine-run counts, not from legacy elapsed times.
   **What would help:** a one-hour profile of `core.py` per-year loop (the new gate/PL solve is the suspect);
   even a 2× win halves every remaining campaign. Recommend assigning to `engine-core` after Gate 1 signs off.
3. **Worker count vs quota**: `nproc` reports 80 and an earlier 56-worker allocation was issued against it; it is
   withdrawn. All current allocations total ≤10.
4. **Declared venv now functional** (`/root/work/venv-declared`, numpy 2.2.6): the Gate-1 AFTER box run used it,
   so the Gate-0 "numpy below declared floor" caveat is closed operationally (label remains: box x86 replication,
   host is authoritative for values).
5. **Clock/monitor hygiene**: box clock == host clock (checked to the second at 15:03:50); times in this file are CST.
   `loadavg` misleads by construction; do not substitute it for cgroup numbers.
6. **Lane over-cap / stalled-job policy**: message the lane, record here, rebalance. None so far. The only
   over-cap event of the day was the legacy tenant (8 workers on a 10-CPU box, repeatedly).

---

## 10. What would speed this up (ranked by ROI)

1. **Stop the external legacy orchestrator** (biggest single win): returns ~4–5 CPUs immediately, cuts J-02 from
   ~56 min to ~47 min and lets qa task-7 run at full 3-worker cap without contention. Cost: 0 box resources.
2. **Run the 540 at 8 workers, not 6**, once qa's task-7 has a measured size and the box is clear → 42 min vs 56 min
   (with legacy) / 35 vs 47 (clean). Diminishing beyond 8 because of the 10-CPU cap + control slot.
3. **Profile the repaired engine** (§9.2): a 2× per-run win is worth ~2.3 CPU-h on the 540 alone and multiplies across
   every later campaign. Cheapest high-leverage compute task on the board.
4. **Keep latency-critical engine work on the host** (2× faster per run than the box) and use the box for
   throughput-parallel sweeps (e.g. the 540 replication, DGP populations) where the host cores are needed for authoring.
5. **Pilot every job type before launch** (this file's §5): the 1-worker box 540 would have burned 4.7 h; a 2-minute
   pilot replaced that guess with a 47-minute plan. Same applies to task-7 DGP (scope 1 population first) and task-8.
6. **Batch/pack small jobs**: task-6/task-9/task-11 are seconds-to-minutes single-process jobs — do not parallelise
   them, run them once on the cheapest available core and release.

---

## 11. Delta log (append-only)

- **14:55** scheduler online; box quota verified 10 CPU; legacy 1080-sim at 8.0 CPU-equiv.
- **14:56** legacy tenant retired #1; artifacts hashed+snapshotted (`e1ce873a…d9025b`); box idle; ledger written.
- **14:57** allocations issued (qa 5 / contest-math 3 / audit-runner 1 / commander 0 + control 1); lanes messaged.
- **14:59–15:00** qa Gate-1 AFTER box suite: **27 passed / 56.73 s** (declared venv numpy 2.2.6) — AFTER column green.
- **15:00** audit-runner task-11 box proof: 3 s, 18/18 PASS, 12/12 manifest, released.
- **15:00** commander 540 box job resized 1 → 6 workers (1 worker = 4.7 h at measured cost).
- **15:03:31** commander relaunches 540 at 6 workers (J-02 running); allocation amended: commander 6 / qa 3 / rest 0–1.
- **15:04** pilots: HK 20.3 s/run, KR 41.9 s/run (box, repaired) vs 1.07 s/run (legacy) → 20–39× engine slowdown found.
- **15:05** escalated to Lead: legacy tenant is driven by an external orchestrator; 7 kills so far, cannot stop from box side.
- **15:05:19** driver root-caused: box-side **`run_parts.sh`** (4 finite parts × 270 sims, 8 workers, sha `1d29f163…`);
  kill group `-13281`; `pgrep` empty 15:05:23; **re-issued 15:05:24** (PIDs 13672/13673/13677 + 13804–13811) → Lead
  approves **bounded plan**: let the finite script reach `ALL_DONE` (~15:14) instead of kill #9; container util at
  overlap **9.0/10 (90 %)**, inside band.
- **15:05:28** commander box 540 restored to 6 workers (it had been reverted to 1 worker at 15:04:49 = 4.7 h):
  PID 13844 + 13846–13851, log `/root/work/cmd/run_540_w6b.log`.
- **15:02:47** contest-math task-6 box job DONE (~5 s, 1 proc, 15:02:47, `abc_identification.json` sha `33120aab…`);
  task-9 is host-only (0 box workers). audit-runner task-11 box job DONE (3 s).
- **15:08** qa task-7 scoped: **0 engine runs** — pure-NumPy ABC, 500 populations (5 configs × 100), 20 000 prior
  draws × 16 moments per population; host authoritative run (4 workers) in flight; box pilot (5 populations, 3 workers)
  next, will report measured per-population seconds. task-8 = 60 cells × 2 000 datasets, NumPy, sized after pilot.
- **15:07:51** **OPERATOR ORDER: external agent session told to stop**; `pgrep -fa 'run_hk_korea_canonical|run_parts'`
  EMPTY, no relaunch. Legacy tenant ENDED (final hashes §7c). Box clean for the first time since 14:50.
- **15:07:45** `/root/work/cmd` **claimed by controller** (commander handoff, he will not relaunch); 540 cross-env
  replication relaunched at **6 workers** (PID 14765 + 14767–14772, log `run_540_w6c.log`) → ETA **~15:55**.
- **15:08** util 6.0/10 (60 %) = 540 alone → gap 3–4 CPUs; qa task-7 (0 engine runs, pure NumPy ABC, 500 populations
  = 5 configs × 100, 20k draws × 16 moments per population) asked to launch box pilot at 3 workers immediately;
  host authoritative run (4 host workers) already in flight since 15:03.
- **15:10:40** qa task-7 launched on the box at its 3-worker cap (config 1/5): PID 15122 parent + 15124–15126,
  `docs/audit/code/dgp_validation.py --out-dir /root/work/qa/full_out --workers 3 --n-pop 100 --n-draws 20000`;
  declared venv (numpy 2.2.6); 0 engine runs (pure NumPy ABC).
- **15:12:37** util **9.4/10 (94 %)**; 540 at **10.1 % done** (1,698/16,794 CPU-s, ETA ~15:54); qa 318 CPU-s in
  config 1 with no artifact yet; no legacy relapse (operator stop holds).
- **15:13** 540→8 proposal withdrawn (cap arithmetic, §3b); 10th slot = contest-math task-9 box replication at 1 worker
  (requested; host remains authoritative). If contest-math declines, the box holds 9.4/10 with the control slot free —
  still inside band.
- (next refresh: qa measured per-population seconds + config ETA; contest-math 10th-slot decision; 540 progress)
