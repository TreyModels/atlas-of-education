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
| current utilization | **0.0 / 10 CPU (idle)** at 15:59:27 — **all box work complete**; 540 finished ~15:57 and every lane has released its workers. Box idle since then (see §12 final state). |
| band check | 90 % is **inside** the 8.5–10.0 target band; hard worker cap respected (see §3b for the withdrawn 540→8 proposal); `loadavg` 18.8 is host-wide and is not our container (see §2) |
| headline | **Gate-1 AFTER invariant suite is GREEN on the declared stack** (box replication: 27 passed in 56.73 s, 5 workers) |
| ETA (controller box 540) | 540 × ~31 CPU-s/run ÷ 6 workers ≈ 47 min from 15:07:45 → **~15:54:30**, now with the full 6 cores (legacy ended) |
| box 540 backup status | **COMPLETE — now the PRIMARY Gate-1 migration source** (host hung again, PID 63896, 0 % CPU, no JSON). `Completed 540 runs in 2960.4s` = 49.3 min, 6 workers, started 15:07:45 / finished ~15:57; verified 540 seed rows + 18 arms; **sha256 `455649da…34ec21`**; provenance declared venv py3.10.8 / **numpy 2.2.6**, engine clean `98baf6b`; intermediates kept; handed to commander + Lead. **Fallback rule unchanged: any subset fallback must be explicitly LABELLED, never a silent partial.** |
| **task-12 measured result** | **SHIPPED keep-memo-only** (commits `fceca3b`, `d1acdf3`; report `1b34d36`): post-revert ref **21.036** → shipped **18.904 CPU-s = 1.113×**, **outputs bit-identical (0.000e+00, 130 fixtures)**, 68/68 tests pass in 14.05 s; forward re-association (≤1.4e-15 drift, not bit-identical) **reverted**; batch path (0.87–0.96×, slower) **reverted**. **2–5× UNPROVEN.** Gate-2/Gate-3 budgets use the pre-optimisation cost; shipped engine ≈1.11× faster (540 ≈ 42 min). |
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
| `qa-verifier` | **2** (band-2; was 3–4 for task-7/8) | 0 | 1) Gate-1 AFTER ✅ · 2) task-7 DGP 500 pops ✅ (2.6 CPU-s/pop) · 3) task-8 bootstrap ✅ (70.2 s) · 4) **second independent DGP seed band** (2w, queued) | pure NumPy ABC, 0 engine runs |
| `atlas-commander` | **6** | 6 | 540 repaired-engine **cross-environment replication** (authoritative 540 = host); `/root/work/cmd` controller-managed | parent 14765 + workers 14767–14772, started 15:07:45 |
| `contest-math` | **2 → 4** | 0 | task-6 ✅ (box, 5 s) · task-9 ✅ (box replication 15:15–15:20, 1 proc) · **task-12 optimisation of `contest_math.py`** (2w now, 4 after qa) | owns the hot file; host authoritative for correctness |
| `audit-runner` | **1** | 0 | task-11 harness/manifest/ledger ✅ (box job 3 s) | released |
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
| J-02 | 540 repaired-engine **cross-env replication — now PRIMARY Gate-1 migration source** | controller (commander handoff) | 6 | 15:07:45 | ✅ **DONE ~15:57** (`Completed 540 runs in 2960.4s`) | 540 runs × 32.9 CPU-s/run = 17,762 CPU-s; verified 540 seed rows, 18 arms (HK 9 + KR 9) | done in **49.3 min** | `/root/work/cmd/papers/shadow-education-contest/code/hk_korea_comparative_with_cf4.json` — **sha256 `455649daf2a1e3367820004c3338deb41236991814887c295b6e7a2bb634ec21`**; stable copy `/root/work/cmd/hk_korea_comparative_with_cf4_boxw6_2026-11-25.json` (+`.sha256`); log `run_540_w6c.log`; provenance: declared venv py3.10.8 / **numpy 2.2.6**, engine clean `98baf6b` (`core.py` `72cbddf7…`, `contest_math.py` `23a01730…` = pre-task-12) |
| J-03 | task-6 rank/Jacobian audit (~1,000 prior-box points) | contest-math | 1 (analytic; 0 pool) | ~15:02 | staging/analytic on host | 1 moment-map + Jacobian per point; 0 `pl_win_probs` calls | <5 s once launched | `/root/work/contest` harness currently staged |
| J-04 | task-11 harness/manifest/ledger box proof | audit-runner | 1 | 15:00:49 | ✅ DONE 15:00:52 | 3 s wall | done | `/root/work/audit/p07_box_evidence.tar.gz`, 18/18 PASS |
| J-05 | task-7 synthetic DGP (500 pops = 5 configs × 100, 20k draws × 16 moments, pure NumPy ABC, **0 engine runs**) | qa-verifier | 3 | 15:10:40 | ✅ **DONE ~15:18** | measured: 500 pops / ~7.3 min @3w = **2.6 CPU-s/pop, 1.14 pops/s aggregate** | done | `/root/work/qa/full_out` (6 artifacts, sha256 in ledger: accepted_draws `62fa1b4b…`, posterior_predictive `0cf9ce27…`, summary `698649f6…`) |
| J-06 | task-8 bootstrap factorial | qa-verifier | 4 | 15:22 | ✅ **DONE** | 70.21 s wall; FE size 0.052–0.062 across confounding; pooled size 0.996–1.000 (OVB); permutation invariance 6.66e-16; shipped stats reproduced | done (commit `01cb4d3`) | `/root/work/qa/bs_out`: parquet sha256 **`41c62895…9216ebf`**, summary sha256 **`e266710d…755ab6d13`** |
| J-08 | **second independent DGP seed band** (Lead-approved) | qa-verifier | 2 | 15:25:12 | ✅ **DONE ~15:36** | 2.6 CPU-s/pop; 6 artifacts in `band2_out` | done | `/root/work/qa/band2_out` |
| J-10 | **third independent DGP seed band** (Lead-approved filler) | qa-verifier | 2 | 15:36:5x | ✅ **DONE ~15:48** (box clock) | rank 5/5 crossed 500/500, legacy 3/3; RMSEs indistinguishable from bands 1–2 | done; qa queue EMPTY, slots released | `/root/work/qa/band3_out` (+`band3_sha256.txt`, summary sha256 `a0caca66…3f9b047`) |
| J-09b | task-12 optimisation of `contest_math.py` | contest-math | 2 | patch `191de03` → shipped `d1acdf3` | ✅ **DONE (shipped keep-memo-only)**; slots released | post-revert end-to-end **21.036 → 18.904 CPU-s = 1.113×**, bit-identical outputs, 68/68 tests in 14.05 s | 2–5× unproven; levers above lane (tutoring grid 9→5 ⇒ 1.7×) | hashes: `contest_math.py` `cd7b5ba6…`, `CONTEST_MATH_PERF.md` `85c7cd09…`, results JSON `fd478d03…` |
| J-09 | **task-12 optimisation of `contest_math.py`** (Lead-approved; owner = contest-math, not engine-core) | contest-math | 2 → 4 when qa finishes | queued (asked 15:25) | pending claim/launch | benchmark 1 HK run = 20.3 CPU-s baseline; profile: 92.7 % in PL quadrature | target 2–5×; report CPU-s/run before/after | `/root/work/contest` |
| J-07 | task-9 general-r Tulloch validation | contest-math | 1 (analytic) | blocked on J-03 | queued | ~200 PL calls × 14–49 ms ≈ 3–10 s | <1 min | `/root/work/contest` |

Completed / released: J-01, J-04, J-05, J-06, J-08, J-10, J-09b, J-02. **FINAL (15:59): every lane has released its workers; box idle 0/10; total 0.** No lane currently exceeds its cap.

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
| — | **task-7 DGP pilot** (5 populations = 1/config) | declared venv (numpy 2.2.6, pandas 2.3.3), 3 workers | **7.43 s wall for 5 pops ≈ 4–5 CPU-s/pop** (n1000 config ~2–3 s/pop, n100 ~0.3 s, legacy ~0.8 s) | **0 engine runs**; pandas/pyarrow already present, no pip needed |
| — | **engine cProfile** (1 HK Baseline seed 0; `cProfile`, 1 proc) | declared venv (numpy 2.2.6) | **19.82 s wall**; 2.37 M calls | **92.7 % of a run is the PL-probability quadrature**: 405 `pl_win_probs` calls = 18.37 s, dominated by `contest_math._quadrature_win_probs` (10.17 s tottime) + numpy `cumsum` (4.64 s) + `einsum` (2.38 s); 46 year-`step()`s = 19.81 s. This is the mechanism behind the 20–39× slowdown vs the legacy engine and the **#1 optimisation target**. |
| — | **task-12 end-to-end perf** (1 HK Baseline seed 0) | declared venv, 1 proc each | pre-patch `98baf6b` **18.812 s** vs patch build `191de03` **16.905 s** = **1.113×** (lane harness 22.183 → 18.550 = 1.196×); **shipped memo-only** post-revert **21.036 → 18.904 CPU-s = 1.113×** | shipped version **bit-identical outputs (max|diff| 0.000e+00)**, 68/68 tests pass in 14.05 s; batch path 0.87–0.96× **reverted**; **2–5× UNPROVEN** |

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
| **15:14:38** | **23.8** | **9.9** (99 %) | 540 6 + qa 3 | qa pilot measured (5 pops / 7.43 s @3w = 4–5 CPU-s/pop); 540 14.4 % done |
| 15:19:21 | 25.0 | **6.0** (60 %) | 540 6 | qa task-7 finished (6 artifacts written 15:18); gap before task-8 |
| 15:20:55 | 28.4 | **7.0** (70 %) | 540 6 + profiling 1 | profiler pilot done: 92.7 % of a run = PL quadrature |
| 15:25:04 | 16.3 | **6.5** (65 %) | 540 6 | qa task-8 ✅ done; waiting on qa band-2 + contest-math task-12 launches to return to 10/10 |
| 15:33:05 | 23.6 | **8.0** (80 %) | 540 6 + qa band-2 2 | contest-math task-9 + task-12 baseline probe finished; task-12 patch being coded (bursts will use its 2 reserved slots) |
| 15:37:49 | 21.1 | **8.1** (81 %) | 540 6 + band-3 2 | band-2 done; band-3 (`--seed 20261127`) running; task-12 bench partial (equivalence PASS) |
| 15:47–15:54 | — | **60–80 %** | 540 6 + task-12 bursts | band-3 ended ~15:48; task-12 bench/revert bursts; 540 last stragglers |
| 15:53:54 | 15.4 | **5.0** (50 %) | 540 2–3 of 6 | 540 tail: most workers done, last KR arms finishing |
| **15:57–15:59** | **7.9** | **0.0** (idle) | 0 | **540 COMPLETE (49.3 min)**; every lane released; box idle by design (§12) |

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
   **Profiled (15:20, 1 HK run, cProfile):** 92.7 % of the run is the PL-probability quadrature — 405
   `pl_win_probs` calls = 18.37 s of 19.82 s, with `contest_math._quadrature_win_probs` 10.17 s tottime and
   `np.cumsum` 4.64 s + `np.einsum` 2.38 s inside it. The legacy engine used the closed-form `1−exp(−λx^r)`;
   the honest PL object is what costs 20–39×. **Action: hand this profile to `engine-core`** for a targeted
   optimisation pass (vectorise/cache the quadrature across the 46 years, hoist the seat-sum renormalisation) —
   even a 2× win halves every remaining campaign; a 5× win would bring the repaired engine near legacy speed.
3. **Worker count vs quota**: `nproc` reports 80 and an earlier 56-worker allocation was issued against it; it is
   withdrawn. All current allocations total ≤10.
4. **Declared venv now functional** (`/root/work/venv-declared`, numpy 2.2.6): the Gate-1 AFTER box run used it,
   so the Gate-0 "numpy below declared floor" caveat is closed operationally (label remains: box x86 replication,
   host is authoritative for values).
5. **Clock/monitor hygiene**: box clock == host clock (checked to the second at 15:03:50); times in this file are CST.
   `loadavg` misleads by construction; do not substitute it for cgroup numbers.
6. **Lane over-cap / stalled-job policy**: message the lane, record here, rebalance. None so far. The only
   over-cap event of the day was the legacy tenant (8 workers on a 10-CPU box, repeatedly).
7. **Programme-level findings from compute work today** (Lead asked these be explicit; both handed to commander):
   (a) **task-8 size control is decisive** — FE size 0.052–0.062 vs **pooled size 0.996–1.000 under a zero-effect
   null**, i.e. the pooled estimator over-rejects at ~100 %, exactly the OVB the external audit identified;
   permutation within-invariance 6.66e-16 confirms the within algebra numerically; shipped/auditor statistics
   reproduced exactly. (b) **92.7 % of repaired-engine runtime is one function** (`contest_math` PL quadrature) →
   Gate-2/Gate-3 budget consequence + optimisation target, assigned as task-12.
8. **task-12 outcome — SHIPPED keep-memo-only; the 2–5× target is UNPROVEN.** contest-math's decision (commits
   `fceca3b`, `d1acdf3`, report `1b34d36`): ship only the result LRU (64 entries, 37/405 hits = 9.1 %) + Simpson-grid
   memo + `pl_stats()`; **reverted** the forward float64 re-association (changed outputs ≤1.4e-15 — not bit-identical,
   rejected on the Lead rule) and the slower batch/vectorised path (0.87–0.96×). Post-revert measured pair (box, same
   core, adjacent): reference **21.036 CPU-s** → shipped **18.904 CPU-s** = **1.113×**; **outputs bit-identical to
   pre-task-12 (max|diff| = 0.000e+00, 130 fixtures)**; unchanged 68-test suite **68 passed in 14.05 s**; determinism
   bit-identical; exact-cap A6 raise still enforced before any cache lookup. Scheduler independent earlier pair:
   18.812 → 16.905 CPU-s = 1.113× (build `191de03`, superseded). Artifact hashes: `contest_math.py` sha256
   `cd7b5ba6…0ab38bb`, `CONTEST_MATH_PERF.md` `85c7cd09…b4b8c4`, results JSON `fd478d03…89209375`.
   **Gate-2/Gate-3 budgets still assume the pre-optimisation cost for the current numbers**, with the shipped memo
   version ≈**1.11× faster** (540-class ≈ 42 min, was 47). If a 2× win is required the reported levers are decisions
   above the lane (tutoring prep grid 9→5 points ⇒ projected 1.7×; 9→4 ⇒ 2.0×; or relax equivalence to 1e-3).

---

## 10. What would speed this up (ranked by ROI)

1. **Stop the external legacy orchestrator** (biggest single win): returns ~4–5 CPUs immediately, cuts J-02 from
   ~56 min to ~47 min and lets qa task-7 run at full 3-worker cap without contention. Cost: 0 box resources.
2. **Run the 540 at 8 workers, not 6**, once qa's task-7 has a measured size and the box is clear → 42 min vs 56 min
   (with legacy) / 35 vs 47 (clean). Diminishing beyond 8 because of the 10-CPU cap + control slot.
3. **Optimise the one hot function** (§5 profile, §9.2): **92.7 % of every repaired-engine run is `pl_win_probs`**
   (405 calls = 18.37 s of 19.82 s; `_quadrature_win_probs` 10.17 s tottime + `cumsum` 4.64 s + `einsum` 2.38 s).
   Assigned to **contest-math as task-12** (it owns `contest_math.py`). A 2× win cuts the 540-class job from 4.7 to
   2.35 CPU-h and halves every Gate-2/Gate-3 campaign; a 5× win returns near-legacy speed and changes the whole
   Gate-2 budget. Highest-leverage compute task on the board.
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
- **15:14:38** util **9.9/10 (99 %)**, 540 14.4 % done (2,412/16,794 CPU-s, ETA ~15:54); qa pilot returned
  **5 populations / 7.43 s wall @3 workers = 4–5 CPU-s/pop**, 0 engine runs, pandas/pyarrow already present
  (no pip) → full 500-population run ETA **~15:23–15:28**; task-8 scoped at 600–900 CPU-s (~5 min at 3 w).
- **15:18** qa task-7 box run **DONE** (500 pops in ~7.3 min at 3 workers = **2.6 CPU-s/pop, 1.14 pops/s**;
  6 artifacts in `/root/work/qa/full_out`, sha256 recorded: accepted_draws `62fa1b4b…`, moment_recovery `c5b55201…`,
  posterior_predictive `0cf9ce27…`, rank_diagnostics `b3c2f6a1…`, recovery_samples `4ed67041…`, summary `698649f6…`).
- **15:20:55** profiling pilot (1 HK run, cProfile, 1 proc): **19.82 s**, **92.7 % in PL quadrature** (405 calls,
  18.37 s; `_quadrature_win_probs` 10.17 s tottime; `cumsum` 4.64 s; `einsum` 2.38 s) → concrete optimisation target
  for engine-core; util 7.0/10 (540 27.8 % + profiler).
- **15:15–15:20** contest-math task-9 box replication (1 worker, PID 15740) ran and exited; host stays authoritative.
- **15:23** qa **task-8 DONE** (70.21 s wall, 3 workers): FE size median 0.05925 (holds), pooled size under
  confounding 1.0, permutation invariant (6.7e-16); artifacts `/root/work/qa/bs_out` + `qa_results.tgz` (18 MB).
- **15:25** Lead decisions: (a) optimisation of `contest_math.py` → **contest-math task-12** (2–3 box workers, not
  engine-core, to keep file ownership single); (b) qa gets a **second independent DGP seed band**. Cap arithmetic:
  6 + 4 + 2 = 12 > 10, so the remaining 4 CPUs split **qa 2 + contest-math 2** now, with contest-math rising to 4
  after qa's band finishes.
- **15:25:04** util **6.5/10 (65 %)** = 540 6 + measurement overhead; gate: waiting on qa band-2 and contest-math
  task-12 launches. 540 at **36.7 %** (6,157/16,794 CPU-s), ETA **~15:54**.
- **15:25–15:33** contest-math used its 2 reserved slots: task-9 box replication (PID 16730, 15:26:36, ~4 min) and the
  **task-12 baseline probe** (PID 17017, 15:28:35: HK Baseline seed 0 with call-pattern instrumentation + wall clock)
  → before/after pair will be contention-matched on the box (host deliberately not used for the speedup number;
  host load ~109 from other lanes). qa band-2 (`--seed 20261126`, 2 workers) on track ~15:36–15:38.
- **15:33:05** util **8.0/10 (80 %)**; 540 at **54.7 %** (9,186/16,794 CPU-s), ETA **~15:54:40**.
- **15:36** band-2 DONE (artifacts `band2_out`); qa self-started **band-3** immediately (`--seed 20261127`,
  2 workers, driver 17845 + workers 17847–17848) per Lead approval → ETA ~15:47–15:48.
- **15:35–15:38** task-12 patch `191de03` benchmark: **equivalence PASS** (130 randomised fixtures, max diff
  1.40e-15 ≤1e-12), determinism bit-identical; **cold path 0.97–1.21×**, **memoised path ~0.02 ms/call**,
   batch group 0.87× (slower); end-to-end section crashed twice on box paths → retry running (PID 17640).
  Honest read: caching wins on duplicate weight vectors only (engine has 37/405); a large end-to-end speedup is
  NOT yet demonstrated — noted as caveat §9.8, awaiting contest-math's end-to-end number.
- **15:37:49** util **8.1/10 (81 %)**; 540 at **64.0 %** (10,746/16,794 CPU-s), ETA **~15:54:30**; host 540
  authoritative ETA ~15:43–15:46 (commander; fallback rule recorded: labelled subset only, never silent partial).
- **15:44** task-12 end-to-end finally measured: lane harness ref **22.183 s** → opt **18.550 s** = **1.196×**;
  scheduler independent re-measure ref **18.812 s** → opt **16.905 s** = **1.113×**, outputs identical to 10 d.p.
  → **2–5× target UNPROVEN**; keep/revert rule relayed to contest-math (keep LRU memo only if net-positive, revert
  slower 9-call batch path); Gate-2 budget correction relayed to commander (assume current engine cost).
- **15:48** qa **band-3 DONE** (3-seed robustness: rank 5/5 crossed 500/500, legacy 3/3 in all bands; RMSEs
  seed-stable). qa CPU queue EMPTY → 2 slots released.
- **15:49** contest-math **decision: keep-memo-only** — shipped commits `fceca3b` + `d1acdf3`, report `1b34d36`;
  post-revert ref 21.036 → **18.904 CPU-s = 1.113×**, **bit-identical outputs (0.000e+00)**, 68/68 tests in 14.05 s;
  forward re-association and batch path **reverted**; **2–5× unproven**, levers (tutoring grid 9→5 ⇒ 1.7×) above lane.
  2 slots released. No lane holds a deployed artifact affected (all 540/Gate-1 evidence = `98baf6b`).
- **15:50** **host authoritative 540 hung AGAIN** (PID 63896, 0 % CPU, 23 min, no JSON) → **box cross-env 540 is now
  PRIMARY for the Gate-1 migration table**; on completion: verify log/JSON, sha256, provenance (declared venv numpy
  2.2.6, engine `98baf6b`, 6 workers), hand to commander + Lead, keep intermediates; **keep 1 CPU slot free** for the
  commander's fallback subset driver.
- **15:57** **BOX 540 COMPLETE** — `Completed 540 runs in 2960.4s` (49.3 min), 6 workers, started 15:07:45;
  JSON 435,872 B, **sha256 `455649daf2a1e3367820004c3338deb41236991814887c295b6e7a2bb634ec21`**, verified 540 seed
  rows / 18 arms (HK 9 + KR 9) / metadata elapsed 2960.41; stable copy + `.sha256` in `/root/work/cmd/`; provenance
  declared venv py3.10.8 / numpy 2.2.6, engine clean `98baf6b` (`core.py` `72cbddf7…`, `contest_math.py` `23a01730…`).
  Handed to commander + Lead; **Lead accepted it as the primary Gate-1 migration source and cancelled the 54-run
  fallback.**
- **15:59** all lanes released (qa task-7/8 + 3 bands; contest-math task-6/9/12; audit-runner task-11; commander 540).
  **Box idle 0/10 by design. STAND DOWN** per Lead: no new work until Gate-1 sign-off and the Gate-2 brief; keep
  ledger + profile/hang evidence; no shutdown/power-off/watchers. Idle slot: 10 CPUs (no queue — do not invent work).

---

## 12. Final state (15:59 CST) — stand-down record

| item | final value |
|---|---|
| quota | 10 CPUs (`cpu.max = 1000000 100000`) — never exceeded by our lanes |
| peak utilization | **9.9/10 = 99 %** at 15:14:38 (540 6w + qa task-7 3w) |
| steady-state | 8.5–10.0/10 whenever work existed; dips = queue gaps between lane jobs, **not** oversubscription |
| only oversubscription event | legacy tenant 8 workers before the **operator stop** (~15:07); 8 kills recorded, root-caused to a finite external `run_parts.sh` driver |
| final utilization | **0.0/10 (idle by design)** — all box jobs complete ~15:57, all lanes released ~15:59 |
| box jobs completed | Gate-1 AFTER suite (27 passed/56.73 s) · 540 cross-env **primary** (49.3 min, sha `455649da…`) · task-7 DGP 500 pops · task-8 bootstrap · 3 DGP seed bands · task-6 · task-9 replication · task-11 · task-12 perf/optimisation |
| measured engine costs (planning) | HK arm **20.3 CPU-s**, KR arm **41.9 CPU-s**, 540-class ≈ **16.8 k CPU-s (4.7 CPU-h)** pre-task-12; **×1.113** with shipped memo-only (not 2–5×) |
| deliverables | `docs/audit/COMPUTE_SCHEDULE.md` (this file, committed on `research/contest-audit-v2-2026-11-25`); box ledger `/root/work/compute/ledger/COMPUTE_LEDGER.md`; pilots/profiler `/root/work/compute/pilot/` |
| evidence retained | legacy snapshot `/root/work/compute/legacy_snapshot/` + hashes; profile `profile_hk.log`; task-12 bench results; host-hang notes; 540 JSON + `.sha256` |
| next | **Gate-2 brief** from Lead after Gate-1 sign-off (calibration pilot → search → refinement), costed at the measured engine costs above |
| idle-slot note | **all 10 CPUs idle; no queued box work exists.** Per Lead: stand down, do not invent work, keep one slot for emergencies only |

### 12b. Post-stand-down allocation (2026-11-25 16:15 CST) — task-13

audit-runner requested a **Lead-directed task-13** box leg (runner hardening / Gate-2 precondition #3: checkpoint/resume
equivalence smoke on 6 arms × 2 seeds + pytest hardening suite). **Allocation granted**, because the box is idle
(measured 0.0/10 CPU, no lane processes) and the footprint is tiny:

| field | value |
|---|---|
| lane / job | audit-runner / task-13 runner-hardening smoke |
| box cap | **≤2 worker processes** (parent + pool children included; pytest serial with the smoke, not concurrent) |
| dir | `/root/work/audit13` (new; legacy dirs untouched) |
| stack | `/root/work/venv-declared/bin/python` (declared stack, numpy 2.2.6) |
| rules | `nice -n 10`, BLAS/MKL/OMP=1, read-only deploy from committed SHA, `start_new_session`, no watchers/timers |
| planned start / ETA | ~16:25–16:35 CST; ~4–6 min smoke + ~4–5 min pytest |
| box state at grant | idle 0.0/10 cgroup delta; only the legacy `gpu` pip process (2.2 %) present and untouched |
| conditions | no second concurrent box job from the lane; message PID/start/workers at launch and exit code + wall + artifact sha256 at completion; keep intermediates |
| record | result to be appended to `/root/work/compute/ledger/COMPUTE_LEDGER.md`; monitoring resumed only for this allocation |

---

## 13. Priority change 16:25 CST — Paper A reproduction owns the box

**Operator order via Lead (16:25):** allocate box compute to the **Paper A reproduction** workstream, ahead of DHS and
Gate-2 prep, because Paper A's maths (Exp 1/3/4/5: bulge t*, 1,640-run gate architecture, identifiability/Jacobian,
E8 shock) has never been rerun (only Paper B's 540 was). G2-A is superseded for CPU; DHS is lower priority.

### 13.1 Queue and caps (total ≤10 workers; declared venv py3.10.8/numpy2.2.6; `nice -n 10`; BLAS/MKL/OMP=1; own dirs; hashes+logs+exit codes; loud failure, no silent partials)

| # | job | owner | cap | status at 16:26 |
|---|---|---|---|---|
| a | artefact search/inventory (archive @46950ab, bundles, worktrees, legacy branches) | commander | 1 | **not yet launched** (box 9/10 idle) |
| b | **Exp 3 — 1,640-run gate-architecture experiment** (locate or reimplement runner/configs, rerun on repaired engine) | commander / engine-core if slot frees | **up to 8** (7 while inventory runs, 6 while task-13 active) | pending runner/config; ETA model: 1,640 ≈ 3.04× the 540 mix ≈ **51 k CPU-s ≈ 14.1 CPU-h → ~106 min @8w / ~121 min @7w** (HK-heavy mixes are ~2× cheaper) |
| c | Exp 4 — tutoring identifiability/Jacobian recompute | commander | ≤2 | after/parallel-if-light; G2-A harness + task-6 analytic prior-box audit reusable |
| d | Exp 5 — E8 fee-abolition shock | commander | ≤2 | data-dependent |
| e | Paper B table regeneration from frozen canonical 540 (`sha 455649da…`) | commander | 1 | CPU-light; label as NEW canonical GATE_SPECS run, not the legacy-gate migration run |
| — | audit-runner task-13 (runner hardening / Gate-2 precondition #3) | audit-runner | ≤2 | reserved; not started at 16:26 (Gate-2 blocked on it) |
| — | DHS eight-experiment fleet (new tenant, `dhs_qa` R harness already running ~1 %) | DHS lead | **≤2** (capped; must request allocation) | pre-emptible QA loops; R is installed on the box |
| — | control / reserve | scheduler | 1 | monitoring |

Engine: frozen `/root/work/cmd/engine` (= clean `98baf6b`; `core.py` sha `72cbddf7…`, `contest_math.py` sha `23a01730…`)
for reproduction; the ×1.113 memo engine at `/root/work/contest/engine` is available but labelled and not used for
reproduction. Pilot harness for per-run wall/CPU: `/root/work/compute/pilot/e2e_engine.py`. Measured costs: HK 20.3,
KR 41.9 CPU-s; 540 mix 16,794 CPU-s.

### 13.2 G2-A result (completed 16:25 before the override — superseded for CPU, kept as evidence)

`/root/work/g2a/identifiability_report.json` (frozen `V540-FREEZE`, 4 theta × 4 moments, forward FD, isolated subprocess
per eval, seed 0): **start 0 rank 4/4, SVs [60.015, 32.125, 7.770, 0.683], null_dim 0**;
**start 1 rank 4/4, SVs [36.451, 14.423, 4.407, 0.091], null_dim 0** → locally identifiable at both starts.

### 13.3 Monitoring (resumed for this workstream only)

Sample every 2–3 min: cgroup delta utilization, per-lane worker counts, per-job progress; flag <7 idle, >10 workers,
no-progress >10 min. Record PIDs/hashes/exit codes in `/root/work/compute/ledger/COMPUTE_LEDGER.md`. Total concurrent
worker processes must stay ≤10; DHS and task-13 are the first to be paused if Exp 3 needs the full quota.

### 13.4 Update 16:30 — Exp 3/4/5 are NOT recoverable; revised actual queue

**Finding (commander + paper-adjudicator inventory):** no Exp3/Exp4/Exp5 runner, config, grid, or SSA country config
exists in any bundle, the archive branch `@46950ab`, the research branches, or any worktree. Paper A's Exp-3 grid
parameters are undocumented → a rerun would be a **"reconstruct from memory"** new experiment, which is **prohibited**.
**Exp 3 is therefore NOT queued** and the 14.1 CPU-h cost model for it is void. This is recorded so nobody later
"fills the box" with an experiment that has no provenance.

Actual jobs (16:30):

| job | owner | workers | status |
|---|---|---|---|
| box-job-1: independent re-execution of Paper-A audit harnesses (`abc_identification_audit.py` exit 0 → `bootstrap_factorial.py --workers 4` done → `dgp_validation.py --workers 3` live) | commander | 3–4 (driver 23223; dgp parent 23421 + workers 23423–23425) | RUNNING, started 16:27, **ETA ~16:38–16:40**, outputs `/root/work/pa_jobs/results/`, logs `/root/work/pa_jobs/logs/` |
| candidate-zip inventory (`INVENTORY2.txt` 47 KB + `INVENTORY2_SHA256SUMS.txt` 75 KB + `extract/`) | commander | 1–2 | DONE (16:29), evidence in `/root/work/pa_zips/` |
| audit-runner **task-13** (Gate-2 blocker) | audit-runner | ≤2 reserved | **NOT STARTED** at 16:30 (`/root/work/audit13` absent) — nudged 3× |
| DHS QA (`dhs_qa` R harness) | qa-verifier / DHS | ≤2 cap | finished its current loop (0 procs); must request allocations through scheduler |
| Paper B table regeneration | paper-adjudicator / commander | 1 | not on box yet; CPU-light |

**Utilization reality:** measured **3.0/10 (30 %)** at 16:30:25, on track to near-idle after ~16:40 — because the only
sustained CPU job in the programme (Exp 3) does not exist. The scheduler's standing rule applies: **do not invent work.**
Realistic fillers if the operator wants the cores used: run the remaining Paper-A audit harnesses **concurrently as
independent shards** (2 workers each), Paper B table regeneration (1w), task-13 (2w), zip extraction/hashing (1–2w).
Caps stay: total ≤10, DHS ≤2 (pre-emptible), control 1.

### 13.5 New-generation campaign + data unblock (16:35–16:39)

**Paper B new generation LAUNCHED** at 16:35:47 (prereg commit `dba0ecc`): `run_new_generation.py --seeds 0-99 --workers 8
--out-dir /root/work/newgen/results`, driver PID **24480**, 8 arm workers (24483/24486/24487/24490/24491/24493/24495/24496),
declared venv, `nice -n 10`, BLAS/OMP=1. Scope: **2,700 runs** = 1,800 KR-TRACKED primary (18 arms × 100 matched seeds)
+ 900 KR-SINGLE sensitivity. Per-seed atomic checkpoints (`ckpt_<jur>_<arm>_<variant>.jsonl`), arm-level subprocess
isolation, resume-on-restart, loud failure (no final JSON on rc≠0); **not** the hardened driver (no watchdog) — accepted
because checkpoints make restart safe; do **not** swap drivers mid-run.

**Allocation at 16:39 (measured cgroup delta 9.3/10 = 93 %):** Paper B 8 · task-13 1 · WDI network 1 · control 1 = 10.
DHS 0 (capped), Paper B table regen 0 (paused), no further audit harnesses.

**BOX-JOB-1 released (all stages exit 0):**
- `abc_identification_audit`: advertised 5×6 moment Jacobian **rank 4/5, null dim 2**, left-null certificate 1.25e-16,
  44 distinct in-box θ, **δ = −0.7537718023763802**, P(own|tutoring) = 0.68 exact (1.11e-16) → MATCH.
- `bootstrap_factorial --workers 4`: FE size median **0.05925**, pooled size **1.0**, within-invariance
  **6.661338147750939e-16**, shipped/auditor stats reproduced → MATCH.
- `dgp_validation --workers 3`: **479 s**, corrected design rank **5/5**, legacy **3/5**, δ_analytic −0.7537718023763804.
  Results + `SHA256SUMS` in `/root/work/pa_jobs/results/`; wall `TOTAL_WALL_SEC=556`.

**Data unblock:** the box can reach the **World Bank API (HTTP 200)** → Paper A (b) bulge t* is **not data-blocked**.
Fresh hashed WDI download on box: `/root/work/wdi/WDI_MANIFEST.json` (944 B, timestamped sha256 of every file) +
indicator JSONs (SE.PRM.DURS, SE.PRM.REPT.ZS, SE.SEC.PROG.ZS, SE.SEC.ENRR, SE.SEC.ENRL.TC.ZS, SE.PRM.ENRR, metadata
SSF region), 16:38. Analysis follows.

**ETA model (measured):** primary 1,800 runs = 900×20.3 + 900×41.9 = **55,980 CPU-s → 117 min @8 workers → ~18:35–18:45**;
full 2,700 ≈ **19:50–20:10**; refined from completed-arm timings as they land.

**Queue after Paper B primary:** gate-architecture ≥5,000-run grid = **43–60 CPU-h → 5.4–7.5 h at 8 workers**; E8
fresh-vintage event study (1–2 CPU-h) and forecast (1–3 CPU-h) and multi-seed Jacobian (2–6 CPU-h) share the 1–2 free
slots; bulge t* small CPU (now WDI-unblocked). GPU lane (`/root/work/gpu2`, 3080 Ti float64 PL prototype) is **separate
and outside the CPU cgroup**; CPU allocation unchanged until a ≥3× @≤1e-12 prototype result justifies moving the gate
grid to GPU.

### 13.6 GPU lane — separate, outside the CPU cgroup (16:42 update)

GPU plan changed: **no new port is being written.** The existing CUDA port was recovered —
`unified_gpu_suite_2026_11_24.zip` → a **CuPy/raw-CUDA-kernel ABM** (`exp1_unified_gpu_abm.py`, Philox RNG, N=250k) with
exp2/3/4 and its own **PRE_REGISTRATION**. `atlas-commander` will validate/run that suite on the 3080 Ti in a separate
lane (`/root/work/gpu2`). It is a **sibling model, not the repaired gate engine**, so it does **not** change Paper A/B CPU
allocation: Paper B stays at **8 workers**, task-13 **1**, control **1** (90 % target). **A GPU job gets box CPU only if the
Commander explicitly requests it through the scheduler.** The legacy GPU scripts in `/root/work/gpu` remain quarantined
and must not be touched.
