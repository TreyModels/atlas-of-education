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
