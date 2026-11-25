# DASHBOARD — Atlas contest audit v2 (Lead = dashboard; Commander = execution)

owner: lead (this window) · executor: **atlas-commander** · date: 2026-11-25 · status: SETUP

rule: this is the one-screen monitor. **The Commander updates it at every milestone** (append-only delta log,
current-state table). The Lead reads it, relays deltas to the user, and does **not** run research/experiments.
Every claim in a delta must link an artifact path (or say explicitly "no artifact yet").

## Role split (binding)

- **Lead = dashboard**: infrastructure, fleet provisioning, relays deltas/asks, holds the Gate-1 sign-off and
  final packaging gate. Does not edit engine/model files, does not run campaigns.
- **Commander (`atlas-commander`)**: owns execution. Coordinates lane agents, enforces Gate 0→1 order, applies
  pre-declarations, keeps artifacts + sha256, writes the master evidence table, reports deltas here.
- **Lane agents**: one coherent write scope each; report to Commander; commit on the audit branch.

## Current state

| gate | state |
|---|---|
| G0 environment + artifact inventory | **IN PROGRESS** — audit-runner deploying to box `/root/work/gate0`; `system_host.txt`, `system_box.txt`, `ARTIFACT_REGISTRY.csv` (partial), `ARCHIVE_BRANCH_INVENTORY.csv` appearing (untracked) |
| G0 legacy 540 reproduction vs reference | **IN PROGRESS** — audit-runner running; box re-run queued (16 workers) |
| G1 engine repairs (gates/G9, PL probabilities, tutoring accounting, prep stock, stable RNG) | **IN PROGRESS** — Phase A: `docs/audit/TUTORING_AUDIT.md` (commit fa34409); `engine/eduengine/contest_math.py` draft (387 L, untracked); binding contract `docs/audit/ENGINE_INTERFACE_CONTRACT.md` v1.0 |
| G1 invariant test suite (12 required tests) | **IN PROGRESS** — qa-verifier writing test-first against the unrepaired baseline |
| G1 first-failure report to Lead | PENDING (baseline failures being collected) |
| G2 empirical benchmark registry | NOT STARTED |
| G2 calibration | BLOCKED by G1 |
| G3 policy campaign | BLOCKED by G1/G2 + Lead sign-off |
| GPU lane (torch install in flight on box) | NOT STARTED (parked; GPU out of wave 1) |

## Box CPU allocation (issued by Commander 2026-11-25 14:30 CST; total 56/80 workers)

Box `autodl-container-wjb02xe512-3c3a2b3b` (80 vCPU, 251 GB RAM; box python `/root/miniconda3/bin/python` 3.10.8,
numpy 1.24.1, scipy 1.13.1 confirmed; helpers `/tmp/box_ssh.sh`, `/tmp/box_scp.sh`; MCP `autodl_*` tools are stale — do not use).
Rules given to every lane: single private dir, never write/kill another lane's work, `nice -n 10`,
`OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1`, no shutdown/reboot/poweroff, no watchers/timers,
back off if `/proc/loadavg` > 60, deploy read-only from a committed SHA via `git archive`, pull results back with
sha256. Code edits only on the Mac worktree, never on the box.

| lane | workers | private dir | allowed work |
|---|---|---|---|
| audit-runner | 16 | `/root/work/gate0` | 540-run reproduction + environment-independence re-runs |
| contest-math | 24 | `/root/work/contest` | exact-DP / Monte-Carlo validation + approximation-error grids |
| qa-verifier | 12 | `/root/work/qa` | invariant suite, parallel/ordering replication (test 12) |
| engine-core | 2 | `/root/work/core` | small deterministic probes only |
| engine-tutoring | 2 | `/root/work/tut` | small deterministic probes only |
| atlas-commander | remainder (≤24) | `/root/work/cmd` | independent verification (540 on corrected engine) |

## Open decisions (for the user, surfaced by Lead)

1. Canonical spec: 420 design ported to patched engine (model-fix recommendation) vs 540 spec. **Default: hold —
   do not freeze until the engine repairs land and Gate 1 passes.**
2. G9: implement lasting consequence (KR-TRACKED) and also run "G9 removed" (KR-SINGLE). **Default: implement both.**
3. Which equity dimension the welfare criterion uses (elite Q5 share vs Q5−Q1 tutoring gap). **Default: report both,
   pre-declare elite-Q5-share as primary per the 540 CF4 criterion.**

## Delta log (append-only; Commander writes, Lead reads)

- 2026-11-25T14:25+08:00 · Lead · infrastructure ready. audit branch `research/contest-audit-v2-2026-11-25`
  @ 7356c97 in `~/neon-boot/wt4/auditv2`; pristine repro tree @ 1c3417c in `~/neon-boot/wt4/repro`.
  Ground truth recorded in `docs/audit/LEAD_GROUND_TRUTH.md`.

- 2026-11-25T14:30+08:00 · Lead · **fleet provisioned (6 members, all running)**:
  `atlas-commander` (execution owner) + 5 lanes — `audit-runner` (task-1 Gate 0), `engine-core`
  (task-2 Gate 1a), `engine-tutoring` (task-3 Gate 1b), `contest-math` (task-4 Gate 1c), `qa-verifier`
  (task-5 Gate 1d). Write scopes are disjoint; commits only on the audit branch with per-file
  `git commit -- <paths>` + index.lock retry. Gate policy: no calibration/policy campaign and no heavy
  GPU work until Gate 1 is green and the Lead signs off. No artifact yet from lanes.

- 2026-11-25T14:32+08:00 · Commander · **binding engine interface contract published**:
  `docs/audit/ENGINE_INTERFACE_CONTRACT.md` (v1.0, 522 L). Fixes, for the whole Gate 1: gate schema
  (`open|fixed_bar|quota|contest`, `bar` deprecated alias, unknown → ValueError), persistent state
  (`k['track']` −1/0/1, `k['prep_stock']` (N,nlev), `k['elite']`, `k['elite_prize']`, immutable `k['pid']`),
  KR-SINGLE vs KR-TRACKED pre-registered gate data, tutoring→core accounting identities
  (`tut_outlay == res_cost + tut_tax`, `Σgov_tut_tax == Σtut_tax`, outlay-based cash budget), prep-stock
  depreciation convention (`rho` = depreciation; `rho=0` = legacy anchor — resolves the task-3 contradiction
  raised by engine-tutoring), `contest_math` API (deterministic `auto`; A5 amendment after reviewing the draft),
  event-keyed RNG API, labour-premium audit, backward-compatibility rules, and the 12 invariant-test definitions.
  Lanes notified; engine-core + engine-tutoring unblocked to Phase B.

- 2026-11-25T14:32+08:00 · Commander · **box CPU allocation issued** (56/80 workers, per table above):
  audit-runner 16 (`/root/work/gate0`), contest-math 24 (`/root/work/contest`), qa-verifier 12 (`/root/work/qa`),
  engine-core 2 (`/root/work/core`), engine-tutoring 2 (`/root/work/tut`), Commander remainder (`/root/work/cmd`).
  Box verified live: load 16.3, 251 GB RAM, overlay 27 G free, numpy 1.24.1 / scipy 1.13.1 on
  `/root/miniconda3/bin/python`; torch cu118 pip still downloading on one core (parked, GPU out of wave 1).
  No box job results yet.

- 2026-11-25T14:33+08:00 · Commander · **Gate-0 independent verification (host) COMPLETE** — re-ran the legacy
  540-run job from a clean `git archive HEAD` extraction (`/tmp/cmd-verify`; engine hashes core `618bd6dd…`,
  tutoring `b2d213b6…`, runner `dd0b1d8d…` = the verified artifacts). exit 0, 540/540, wall 100.79 s; output JSON
  sha256 `722c370b…eaf54`. vs committed reference: **9,174/9,180 seed values exact, 6 differ ≤3.55e-15; 842/846
  summary values exact, 4 differ ≤4.44e-16; all 2-d.p. spend indices identical**; only `elapsed_seconds` differs
  among metadata. Cross-lane: differs from audit-runner's host run in exactly one stored field
  (`elapsed_seconds`), all 10,025 other numeric values identical. CF4 verdict reproduced unchanged (only CF1b
  Win-Win in both; CF4a fails HK equity 48.64 % vs 46.36 %; CF4b fails spend 90.88/88.04). Artifacts:
  `results/audit/commander/` (README + JSON + comparison + SHA256SUMS), commit 48d1670. Verdict: REPRODUCED
  SIMULATION (bit-level: last-bit float only). Box environment-independence re-run still pending from audit-runner.

- 2026-11-25T14:32+08:00 · Commander · **engine-core Phase A delivered** (`docs/audit/ENGINE_CORE_AUDIT.md`,
  commit 6403089): defect list with anchors plus measured tracer evidence on the unmodified engine — D1 0 elite
  flags at KR G9 and 51.0 % of contest-prep spend (21,100/41,350 wage units) targeting the phantom gate; D2 KR G12
  mean expected P 0.292 vs realized 0.121 (HK 0.455 vs 0.232); D3 zero-seat quota admits everyone, double admission
  noise, in-sample cutoff; plus credential/track, closed-level, queue-premium, pass_rate and RNG-path defects.
  Phase B started against contract §1/§2/§3/§6/§7/§8. contest-math's deterministic `auto` path remains the
  integration dependency (A5) — flagged to that lane.

- 2026-11-25T14:33+08:00 · Commander · **Gate-0 box environment-independence re-run VERIFIED** (audit-runner ran it;
  Commander independently re-invoked the comparator on the box artifacts via /tmp/box_ssh.sh and parsed results):
  box = 80 vCPU Xeon Gold 6248, py 3.10.8, numpy 1.24.1, scipy 1.13.1 (host: py 3.10.2, numpy 2.2.6, scipy 1.15.3).
  box 8w vs bundle reference: 9,164/9,180 seed values exact, 16 differ ≤7.105e-15 abs / 3.961e-16 rel; summary
  831/846 exact, 15 differ ≤1.776e-15; **every 2-d.p. figure identical**; CF4 verdict identical (only CF1b
  Win-Win both). **box 56w vs box 8w: 9,180/9,180 seed values and 846/846 summary values BIT-IDENTICAL** → worker
  count does not perturb results. Box 56w used a transparent one-line runner variant (`workers=56` only;
  results/audit/box56w_runner_variant.diff). Output hashes: box8w `2e1bcb01…`, box56w `7620a983…`. Commander
  sign-off: `docs/audit/GATE0_VERIFICATION.md` (GATE 0 PASS pending audit-runner's GATE0_REPORT.md); registry
  independent re-hash 71/87 exact, 1 stale self-referential row (`system_box.txt`, grew after registration),
  15 post-snapshot Gate-0 outputs, archive inventory separately recorded (not Commander-verified).

- 2026-11-25T14:41+08:00 · Commander · **BOX QUOTA CORRECTION + FREEZE + LEGACY HARVEST.** (i) Lead verified the box is
  a **10-CPU cgroup** (`/sys/fs/cgroup/cpu.max = 1000000 100000`), not 80; my 56/80-worker allocation is withdrawn.
  All lanes messaged: box CPU work **frozen** until the legacy 1080-sim run (`/root/work/modelrev`) finishes, then
  total ≤8 workers globally / ≤4 per lane, nice -n 10, BLAS threads=1; directory claims relayed
  (`gate0`,`qa`,`core`,`tut`,`venv-declared` ours; `modelrev`,`gpu` legacy read-only). audit-runner recorded the
  correction in `GATE0_REPORT.md` (`5ac7a2b`) without touching the verified registry. No Gate-0 number affected
  (canonical box run = 8 workers; 56-worker = invariance check only). (ii) Legacy work **harvested read-only** into
  `docs/audit/harvest/` (25 files, `HARVEST_MANIFEST.csv` with sha256): `model-revision` branch `d20ba6e` (engine
  fixes 3A–3C + calibration sweep) and `gpu-rtx3080ti` branch `9f7dfa9` (5 result JSONs byte-identical to box).
  Labels: **AUTHOR-REPORTED / PRE-REPAIR, NOT Gate-1 evidence**. Our invariant suite re-run against the legacy
  `model-revision` engine (`git archive` + our tests) still fails the same 7 contract rows (7F/10P/10xfail) → none of
  its code is reusable (`HARVEST.md` diffs 3A/3B/3C vs contract). Preserved negative result: Korean calibration
  **FAILED** — untuned 420 port 66.27 % participation / 80.77 pp Q5−Q1 / 5.32× spend; best grid point 91.63 % /
  37.11 pp / 1.59× vs targets 76.5 / 32.1 / 3.4. (iii) contest-math committed **1a6f3d5**: deterministic
  `pl_win_probs` (exact n≤20, deterministic quadrature above; n=300/seats=36 accuracy ≤0.0029 vs 200k MC, 13.8–49.1
  ms/call; 62 tests) — engine-core unblocked for Phase B integration. `system_box_venv.txt` still pending install.

- 2026-11-25T14:43+08:00 · Commander · **BOX FREEZE RE-IMPOSED (correction).** qa-verifier detected that the legacy
  1080-sim relaunched at 14:42 (`run_hk_korea_canonical.py policy --seeds 30 --workers 8`, live PIDs ~8854+,
  ~100 % × 8 on the 10-CPU cgroup, load 11.8); the `policy_arms_v1v2v3.json` file-existence signal was stale (file is
  being rewritten). All lanes re-notified: **no box jobs until `ps aux | grep run_hk_korea_canonical` is empty and
  loadavg < 8**, confirmed by Commander. Host work unaffected. qa-verifier test 12 is already satisfied on the host
  at the corrected cap: 8 tasks, ProcessPoolExecutor(fork) chunksize 1/4, full task-order permutation,
  serial=repeat=chunksize1=chunksize4=shuffled bit-identical, QA_WORKERS=4 (commit 5f72ef0;
  refreshed baseline still 7F/12P/8xfail in 6.41 s). contest-math committed 47f6bd0 (68-test validation record +
  legacy `1−exp(−λx^r)` approximation-error study). No Phase-B engine commit yet.

- 2026-11-25T14:43+08:00 · Commander · **Gate 1c CLOSED (contest-math) + Lead pushed branch public.** contest-math
  delivered `1a6f3d5` (deterministic `pl_win_probs`: exact subset DP n≤20, deterministic Poisson-binomial /
  exponential-race quadrature n>20, seat-sum ΣP=seats hard-checked; `pl_realize` deterministic; 68-test suite) and
  `47f6bd0` (`CONTEST_MATH_VALIDATION.md`, `CONTEST_MATH_APPROX_ERROR.md`: 1-exp(−λx^r) approximation error
  misleading up to 7.7 pp in the 5×-effort/5 %-seat tail; mean-only reconciliation cannot detect D2 — use
  distributional checks). engine-core imports the module (`core.py` L24/L447, `tutoring.py` L341 in the in-progress
  tree). Master `docs/audit/TEST_REPORT.md` written with the BEFORE column and the (still empty) AFTER plan.
  Lead pushed `research/contest-audit-v2-2026-11-25` public (packet `b3ca85d`); pushes on this branch approved.
  Box: legacy 1080-sim still live (8 workers on the 10-CPU cgroup) — our freeze remains; declared-stack venv
  still installing (scipy 37.7 MB on the slow mirror). Gate 1a/1b Phase B still uncommitted.

- 2026-11-25T14:53+08:00 · Commander · **Gate-1 Phase B VERIFIED (independent, clean-tree) — awaiting qa AFTER column.**
  Both engine lanes committed and the branch is public: `6bc8d61` [gate1b] and `f31e176` [gate1a] (tip `98baf6b`).
  My independent clean-tree (`git archive 98baf6b`) checks: `docs/audit/ENGINE_CHECKS.py --runner` → **13/13 PASS**;
  `docs/audit/TUTORING_CHECKS.py` → **17/17 PASS**; `pytest tests/test_contest_math.py` → **68 passed**. Invariant
  suite on the clean tree: **91 passed / 4 failed**, and the 4 are TEST-SIDE (3 × `method='exact'` used with n>20 —
  A6 correctly raises; 1 × stale XPASS-strict CAPS for the now-existing `'open'` kind) — qa-verifier is fixing its
  own tests and re-running; no engine failure found. Contract amendment **A7** recorded (`contest_candidates(m)` =
  same-year sitting cohort; expected and realised P are the same object) + residual risk of future-gate pool-map
  interpolation noted. Fresh repaired-engine 540 run from clean `git archive 98baf6b` in progress (~20–30 min) for
  the headline migration reproduction with expected-vs-realised decomposition. Repaired-engine file hashes under
  verification: core/rng/contest_math/planning/labour/tutoring from `98baf6b`.
- 2026-11-25T14:53+08:00 · Commander · **P0 GPU-audit track routed by Lead; GPU conclusions QUARANTINED.**
  Lead's external audit of GPU bundle `045a63e` recorded at `docs/audit/EXTERNAL_AUDIT_GPU_2026-11-25.md` (`98baf6b`);
  all GPU ABC / contest-surface / E1-Q3 conclusions remain AUTHOR-REPORTED / PRE-REPAIR / UNRESOLVED. Routing:
  task-6 + task-9 → contest-math (messaged); task-7 + task-8 → qa-verifier AFTER Gate-1 AFTER suite (messaged);
  task-10 execution half → task-11 → audit-runner (Lead messaged); Commander keeps only coordination/dashboard
  recording (this delta). Gate-1 remains higher priority; no campaigns; GPUs parked.

## Compute allocation (compute-controller, from 2026-11-25T14:55+08:00)

Box = 10-CPU cgroup (`cpu.max = 1000000 100000`); `nproc`=80 is the host and must be ignored. All box jobs
`nice -n 10` with `OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1`; target load 8.5–10.0, no
oversubscription. `compute-controller` owns scheduling/monitoring/ETA; lanes request allocations through it.

| lane | worker-process cap | current job |
|---|---|---|
| qa-verifier | 5 | Gate-1 AFTER invariant suite first, then task-7 DGP / task-8 bootstrap |
| contest-math | 3 | task-6 ABC rank/Jacobian audit, then task-9 general-r Tulloch |
| audit-runner | 1 | task-11 GPU execution-integrity / manifest / claim ledger |
| atlas-commander | 0 (host 6-worker 540 run in flight) | independent fresh-540 repaired-engine verification on host |
| **total** | **9–10 / 10** | legacy tenant retired (3rd relaunch) |

**Legacy tenant retirement (authorised by Lead, executed by compute-controller):** `/root/work/modelrev` relaunched
an 8-worker policy campaign for the 3rd time against its handover terms; outputs snapshotted (hashes) before SIGTERM
of runner+workers only, `/root/work/modelrev/pkg` intact. Its outputs are already harvested read-only by Commander in
`docs/audit/harvest/model_revision/` (AUTHOR-REPORTED / PRE-REPAIR / UNCALIBRATED; see HARVEST.md §4/§4b).

## Lanes resumed (2026-11-25T14:56+08:00)

- qa-verifier: Gate-1 AFTER first (fix own 4 test-side items, clean-tree rerun), then task-7/task-8.
- contest-math: task-6 then task-9 (Gate 1c closed and verified: 68/68).
- audit-runner: task-11 (P0-07 execution integrity + manifest + claim ledger).
- engine-core / engine-tutoring: idle; Phase B committed and independently verified; available for fixes only.

- 2026-11-25T14:57+08:00 · Commander · **Legacy tenant retired + compute ledger.** compute-controller SIGTERMed the
  14:50 relaunch of `/root/work/modelrev` `run_hk_korea_canonical.py policy` (runner PID 9433 + workers 9561–9568)
  at **14:56 CST**; outputs hashed and snapshotted to `/root/work/compute/legacy_snapshot/` (+ `.sha256`),
  `/root/work/modelrev/pkg` untouched; compute ledger at `/root/work/compute/ledger/COMPUTE_LEDGER.md`. Commander's
  independent harvest of the same outputs already exists in `docs/audit/harvest/model_revision/` (AUTHOR-REPORTED /
  PRE-REPAIR / UNCALIBRATED). Current allocation: qa 5 / contest-math 3 / audit-runner 1 / Commander 0 (host 540
  run) / 1 reserve; box idle after retirement (brief controller pilot blips only). No oversubscription.

- 2026-11-25T15:03+08:00 · Commander · **GATE-1 AFTER SUITE GREEN — 27/27 invariant tests pass on the repaired
  engine.** qa-verifier commit `5df531d` (clean `git archive 98baf6b`): host **27 passed in 72.85 s**, box
  **27 passed in 56.73 s** using the declared-stack venv (numpy 2.2.6 — closes the Gate-0 numpy-floor caveat
  operationally), and my **independent** rerun (fresh archive + qa's committed tests) **27 passed in 112.12 s**.
  All 7 BEFORE rows (F1–F7: universal seat, non-selective gate, G9 persistence, expected=PL, seat denominator,
  policy-invariant RNG, gate prize) now PASS; 8 API-absent xfails run and pass; 12 baseline greens still green;
  **no new failures**. Residual risk recorded: under A7 the legacy-cohort `share=1.0` arm is not literally universal
  (max e_t 5.97→0.343 via pool-map approximation; use `share_of='applicants'` for universal arms). Commands and
  per-row table in `docs/audit/TEST_REPORT.md` §4. 540 migration run on the repaired engine (host 6 workers, clean
  `98baf6b`; box cross-env at 6 workers) in progress; `ENGINE_CHECKS` 13/13 and `TUTORING_CHECKS` 17/17 already
  verified clean-tree. Tutoring ledger from a real full-size run (KR + HK Baseline seed 0): identities
  outlay=resource+tax rel 0.0, receipts=Σtax rel 0.0, max e_t = cap 6.0 exactly (cap binds), max(extra_spend−cash)
  = −0.000636 (KR) / −0.3183 (HK) ≤ 0; `contest_spend_now` present as Σ outlay; expected-vs-realised per gate after
  repair = 1.0000 (KR G9 0.35/0.35, KR G12 0.12/0.12, HK G12 0.23/0.23) vs the pre-repair 2.41×/1.96× mismatch.

- 2026-11-25T15:07+08:00 · Commander · **P0 track progress + compute reconciliation.** `contest-math` task-6 COMPLETE
  (commits `5fcee05`, `8281dd9`, `79bc919`; box reproduction exit 0, 1 process, hashes in report): 5 advertised ABC
  moments **rank 4/5** (structural m_part ≡ ⅔m_g9+⅓m_g12; left-null certificate ≤3.4e-16), 6 active params ⇒
  2-dim null space, **44 distinct θ** inside the prior box reproduce the same moments, analytic Jacobian vs FD
  4.3e-6, analytic δ = −0.7537718023763802 exact/covariate-free, archived deltas inside the 6 pp tolerance,
  reduced 5-param/3-moment rank 3 ⇒ 2 further independent moments required, urban-rural gap is a composition
  artifact. Now on task-9. `audit-runner` task-11 COMPLETE (`c114a61`, `307b59c`): corrected harness 18/18 assertions
  host+box, failing job aborts with rc=7, `CORRECTED_GPU_EXPERIMENT_MANIFEST.json` (7/7 integrity defects),
  `SCIENTIFIC_CLAIM_LEDGER.md` (36 claims: CONTRADICTED 16 / AUTHOR-REPORTED 9 / UNRESOLVED 6 / REPRODUCED
  SIMULATION 4 / VALIDATED SIMULATION 1 arithmetic / VERIFIED EMPIRICAL 0) — accepted; worker released.
  Box: legacy driver DEAD (15:05:19); controller owns `/root/work/cmd` 540 cross-env replication at 6 workers
  (Commander hands-off after the 1-worker/6-worker relaunch race; host run is authoritative). Host authoritative
  540 run in progress (started 14:55, ETA ~15:17–15:20). Hard caps: qa ≤3, contest-math ≤3, audit 0, commander 0–1,
  total ≤10; controller's assignment wins.

- 2026-11-25T15:08+08:00 · Commander · **Host contention controlled for Gate-1.** Host 8-core machine was carrying
  the authoritative repaired-540 run (6 workers) + qa task-7 DGP (4) + contest task-9 (1) = 11 procs. Asked
  qa-verifier to cap host pools at 2 until the 540 lands (Gate-1 > P0; box preferred for task-7/8 under controller).
  540 ETA revised ~15:20–15:25. Box cross-env 540 relaunched by compute-controller at 6 workers
  (`/root/work/cmd/run_540_w6c.log`, controller-owned; Commander hands-off). Branch: local ahead of origin
  (`307b59c` remote); push planned with the Gate-1 pack.
