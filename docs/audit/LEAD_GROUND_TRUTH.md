# LEAD GROUND TRUTH — Atlas contest audit v2 (verified 2026-11-25 ~14:25 CST)

This file records facts the Lead **verified directly**, so no agent re-derives them. Do not edit
without citing evidence. Everything here is infrastructure/environment, not research findings.

## 1. Version control layout (verified with `git worktree list`, `git ls-remote`)

| item | value |
|---|---|
| canonical clone | `/Users/treymenefee/neon-boot/repos/atlas` (partial clone, `blob:none`; tree restored clean at `55732f4` main) |
| **primary work tree** | `/Users/treymenefee/neon-boot/wt4/auditv2` — branch **`research/contest-audit-v2-2026-11-25`** @ `7356c97` |
| pristine Gate-0 work tree | `/Users/treymenefee/neon-boot/wt4/repro` — branch `research/gate0-repro-2026-11-25` @ **`1c3417c`** (never edit this tree) |
| directive start commit | `1c3417c4a2a17f47f31388e0686396a1a3877757` |
| parent of our base | `7356c97` = `1c3417c` + one doc commit (`REVIEW_RESPONSE_2026-11-25.md`) |
| integrated branch (pushed) | `research/shadow-education-contest-2026-11-25` @ **`7356c97`** |
| archive branch (pushed) | `research/atlas-all-work-2026-11-25` @ **`46950ab`** |
| remote | `https://github.com/TreyModels/atlas-of-education` — reachable from host (HTTP 200) |
| git identity | `TreyModels <355726889+TreyModels@users.noreply.github.com>` |

**Pending branches from the previous window DO NOT exist on the remote and hold no commits locally:**
- `research/model-revision-2026-11-25`: local worktree `~/neon-boot/wt3/model` is **clean at `1c3417c`** — the
  model-fix agent persisted **nothing** (no commits, no untracked files, no RUN_REPORT anywhere).
- `research/gpu-rtx3080ti-2026-11-25`: local worktree `~/neon-boot/wt3/gpu` is at `55732f4` with only
  `research/records/2026-11-25-gpu-rtx3080ti/` untracked (scripts: `gpu_bray_abc_and_contest_surface.py`,
  `gpu_e1_q3_wild_cluster_ri.py`, README, sha256). No results.
→ **Treat both lanes as not started.** The handoff's "in-flight" state did not persist across the window.

Existing research worktrees (read-only for this programme, do not write): `~/neon-boot/wt3/shadow` (7356c97),
`~/neon-boot/wt3/model`, `~/neon-boot/wt3/allwork` (46950ab), `~/neon-boot/wt3/gpu`.

## 2. Key assets in the auditv2 tree

- `engine/eduengine/` — `core.py` (580 L), `planning.py` (113), `ledger.py`, `measure.py`, `settle.py`, `struts.py`,
  `modules/{tutoring.py (171), labour.py (206), schools.py, sdg4.py, anchor.py, state.py}`.
- `papers/shadow-education-contest/code/run_hk_korea_comparative.py` (293 L) — 18 arms × 30 seeds = 540 runs,
  hardcoded `N_SEEDS=30`, 8-worker `ProcessPoolExecutor`; no CLI/config.
- `papers/shadow-education-contest/code/compare_cf4_reference.py` — reference vs actual comparator.
- `papers/shadow-education-contest/code/results/hk_korea_comparative_with_cf4.json` — 540-run output (sha256 `c1fa0926…2e99`).
- `.../results/reference/hk_korea_comparative_with_cf4_bundle_reference.json` — supplied reference.
- `.../results/verified_results_2026_11_25.json` — **420-run** (N=400/T=70) record used by Paper B docx tables.
- `papers/shadow-education-contest/REVIEW_RESPONSE_2026-11-25.md` — confirmed review findings (authoritative triage).
- `.../code/{REPRODUCTION_CF4,RUNNER_STATUS,MISSING_ARTIFACTS,RUN_ATTEMPT_2026-11-25}.md`.
- `papers/shadow-education-contest/{paper_a_general_mechanism,paper_b_hk_korea}/` — manuscripts.
- GPU scripts also at `papers/shadow-education-contest/code/rtx3080ti_gpu_scripts/`.

## 3. Local execution environment (host, verified)

- macOS arm64, Python **3.10.2** at `/Users/treymenefee/neon-boot/venv/bin/python`, NumPy **2.2.6**.
- Engine import needs `PYTHONPATH="$PWD/engine"` from the worktree root; runner's own `ENGINE_DIR` points at a
  non-existent `papers/.../code/engine`, so **PYTHONPATH is required**.
- Verified reproduction command (from previous window, 178.7 s on 8 workers, `exit 0`, bit-identical to reference):
  `PYTHONPATH="$PWD/engine" /Users/treymenefee/neon-boot/venv/bin/python papers/shadow-education-contest/code/run_hk_korea_comparative.py`
- No `timeout` binary on macOS; use `gtimeout` if needed.

## 4. Box (verified live 2026-11-25 14:19 CST)

- SSH: `/tmp/box_ssh.sh "<remote command>"` and `/tmp/box_scp.sh "<local...>" "/remote/dir"` (expect wrappers;
  password in `/tmp/.box_pass`, mode 600). Host `autodl-container-wjb02xe512-3c3a2b3b`, `root@connect.nmb2.seetacloud.com:36934`.
- **HOST 80 vCPU / 251 GB RAM, but the CONTAINER CPU QUOTA IS 10 CPUs** (`/sys/fs/cgroup/cpu.max` =
  `1000000 100000` → 10 CPUs; `nproc` reports the host and is misleading). **All box jobs must budget ~10 CPUs,
  not 80** — total concurrent workers ≤8 with `nice -n 10` and BLAS thread caps, else the box thrashes
  (observed load 15.4 on a 10-CPU quota). RTX 3080 Ti 12 GB (idle, 1 MiB used), overlay 30 G (27 G free).
- **torch IS installed and verified on the box (14:35):** `torch 2.7.1+cu118`, `cuda_available=True`,
  RTX 3080 Ti, capability (8,6), matmul OK. Installed from a local wheel downloaded direct-to-box via a
  16-connection parallel-range fetcher (sha256 `89433c62b02ec802d4c0887c867d935887ae8f00d7cc549ecf1c2640d096bd4c`).
  The original `download-r2.pytorch.org` path was stalled at 27 KB/s (~9 h ETA) — do not reintroduce it.
- Python: **`/root/miniconda3/bin/python` (3.10.8)**, numpy 1.24.1. Bare `python3` is NOT on PATH in non-interactive
  ssh — always use the absolute path or `bash -lc`.
- `/root/work/gpu/` exists with the two GPU scripts + `run_gpu_jobs.sh` + `pip_torch.log`. `pip` is **still
  downloading torch 2.7.1+cu118 (905 MB)** (pid 2515, started 14:09); pip cache ~1.8 GB. GPU stays idle until it lands.
  Do not start a second install; check `ps aux | grep pip`.
- No `/root/work/modelrev` yet.
- **HARD RULES (operator): no shutdown/reboot/poweroff, no watchers/timers.** Heavy CPU work capped at **≤8 workers of the 10-CPU
  quota** with `nice -n 10`, leaving ~30 % for paper/analysis work. `OPENBLAS_NUM_THREADS=1`,
  `MKL_NUM_THREADS=1`, `OMP_NUM_THREADS=1` to prevent oversubscription.
- Repro/small jobs do NOT need the box: the 540-run legacy repro is ~3 min on the Mac.

## 5. Confirmed review findings (from REVIEW_RESPONSE, code-checked there; re-verify in audit)

1. Two result generations disagree: 420-run (N=400/T=70, Paper B docx) vs 540-run (N=300/T=46, reproduced JSON).
   Baseline elite Q5: HK 30.0 % vs 46.36 %; KR 24.6 % vs 36.12 %.
2. Combined CF4 "win-win" fails: only single-lever **CF1b (cap −50 %)** passes (HK spend 67.39, elite Q5 41.96 %;
   KR 76.42, 26.39 %). CF4a fails HK equity (48.64 % > 46.36 %); CF4b fails spend (90.88/88.04 ≥ 80).
3. KR G9 contest: `k['elite']` set only when `m_ == self.nlev - 2` (G12 gate) → G9 winners get no lasting state,
   yet `contest_prep` prices the G9 contest from `elite_logw` ("phantom prize"); `set_voc=False`.
4. Expected vs realized probabilities differ: beliefs use `P = 1 − exp(−λ x^r)`; realized gate uses Gumbel-max
   Plackett–Luce over `x_eff`; λ is re-solved each year to match aggregate seats.
5. Seat denominator: `seats = max(round(share·N), 1)` — share of entering cohort, not applicants.
6. 540 design lost KR calibration: Q5−Q1 participation gap 68.36 pp (target 32.1); Q5/Q1 spend ratio 18.01× (target 3.4×).
7. GPU scripts: `theta[:,5]` (`teacher_threshold`) unused (7-param ABC not identified); panel mode `X=[1,x]` drops
   controls/FE, so it is not an E1/Q3 reconstruction.

## 6. Standing methodological rules for this programme

- Evidence taxonomy (use verbatim): **VERIFIED EMPIRICAL / REPRODUCED SIMULATION / VALIDATED SIMULATION /
  AUTHOR-REPORTED / CONTRADICTED / UNRESOLVED.**
- Preserve existing commits, datasets, manifests, manuscripts, prior results; keep the 420 spec available.
- One commit per coherent stage. Audit branch only. Never force-push the archive/integrated branches.
- **Gate discipline: NO large calibration or policy campaign until (a) Gate 0 reproduction is recorded and
  (b) Gate 1 invariants are green and the Lead has seen the first test-failure report.** Small deterministic
  tests and fuzz first.
- Calibration benchmarks must carry citation + survey year + population + denominator; Korea 2024 = 80.0 %,
  Korea 2025 = 75.7 % overall private-education participation; HK Grade 9 = 53.8 %, Grade 12 = 71.8 % (2011/12 survey).
- Report Monte Carlo uncertainty separately from calibrated-parameter uncertainty.
- Preserve inconvenient results (CF4 failure stays reported).
