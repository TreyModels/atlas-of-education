# GPU PL backend — port onto the canonical pin (host port + Mac verification; box parity pending)

Owner lane: `engine-core` · 2026-11-25 · branch **`research/gpu-pl-port-auditv2-2026-11-25`** (short-lived,
branched off `research/contest-audit-v2-2026-11-25` @ `b0925ae`).
**Engine port commit: `59fd2497765f15c108de3ec182d1febbe3d28c8a`** (the commit that contains the engine files and
`port_verify.py`; later commits on this branch are documentation-only).
Source: `~/neon-boot/wt5/gpuport` @ `research/gpu-port-2026-11-25` (`7c6f9ac` GPU commit, `c80b43c` artefacts).
Status: **HOST PORT COMPLETE + MAC CHECKS PASS; BOX PARITY PENDING (Commander runs it).**
No box job was started from this lane.

## 1. Port summary (additive only; canonical pin preserved)

Base engine state (before port): core `e111397b…8e71`, spec `e5ddef6b…` (metadata commit `98baf6b` in the spec; the
code pin is the hash). The port does **not** touch `_validate_events`, `EVENT_CACHED_PARAMS` or any canonical
Gate-1 code — verified by diff (`core.py` has exactly two hunks).

| file | pre-port sha256 | post-port sha256 | change |
|---|---|---|---|
| `engine/eduengine/contest_gpu.py` | *(absent)* | **`ab08a53b…596f`** | new, copied byte-identical from gpuport |
| `engine/eduengine/contest_math.py` | `cd7b5ba6…0ab38bb` | **`5fceb4d5…0bee944`** | +169 lines: `_GPU_MODULE`, `register_gpu_backend`, `pl_backend`, `set_pl_backend`, `_quadrature_inputs`, `_gpu_dp`, `_gpu_backend`, `pl_win_probs_batch`, GPU stats keys, `__all__` additions. Canonical task-12 caches (`_GRID_CACHE`, `_RESULT_CACHE`) untouched. `pl_realize` byte-identical. |
| `engine/eduengine/__init__.py` | `f4e53bb5…2b5a18` | **`2c082d5c…b348f`** | +11-line optional registration block (`ATLAS_PL_BACKEND=gpu` → `contest_gpu.available() and warmup()` → `register_gpu_backend`) |
| `engine/eduengine/core.py` | `e111397b…8e71` | **`5bcbc0b3…279f75`** | +11/−? exactly two hunks: import `pl_win_probs_batch, pl_backend`; `_pl_probs` GPU one-row batch branch (CPU path unchanged) |
| `engine/eduengine/modules/tutoring.py` | `7a6fd4c3…8adc2f8` | **`b3d32cee…c3fdf`** | 2 hunks: one batched 9-point prep-grid call (`_pl_win_probs_batch`) + `_pl_win_probs_batch` helper with per-row seat-sum renormalisation |
| `docs/gpu/port_verify.py` | *(absent)* | **`6ba6013c…c4026`** | new host/box verification harness (see §4) |

`git diff --stat HEAD -- engine/eduengine`: 4 files, **+222/−10**, plus the new `contest_gpu.py` (10,469 B).
Default `ATLAS_PL_BACKEND` unset ⇒ CPU reference path; import stays **torch-free** (checked: `torch` and
`eduengine.contest_gpu` absent from `sys.modules`). With `ATLAS_PL_BACKEND=gpu` on a host without torch the engine
still imports and stays on CPU (`pl_backend()=='cpu'`; `set_pl_backend('gpu')` raises the documented `RuntimeError`).

## 2. Mac verification (host, CPU default; `ATLAS_PL_BACKEND` unset)

Commands from the worktree root:
`PYTHONPATH="$PWD/engine" venv/bin/python <cmd>` with `OPENBLAS/MKL/OMP=1`.

| check | result |
|---|---|
| 68-test contract suite (`pytest tests/test_contest_math.py -q`) | **68 passed** (9.09 s) |
| 130-fixture CPU central digest (`port_verify.py cpu-digest`) | **`e55a4309ad39c9ddfaa7ffae64c9f286ed01cd109428afd4fe8a7bf8757a8379`** |
| same digest on canonical pre-port tree (`/tmp/canon_ref` from `git archive HEAD`) | **identical** `e55a4309…8379` |
| fixture-definition digest | `60bab112…b59a72c` (identical both trees) |
| CPU `pl_win_probs_batch` vs per-row loop | **bit-identical** (130/130 rows, `max_batch_delta=0.0`) |
| seat-sum `ΣP = seats_eff` on fixtures | OK |
| full-run CPU digest, HK Baseline seed 0, N=300/T=46 (`port_verify.py e2e-digest`) — ported | series `e458fbac…9c4374`, E.ALL `b661817c…ea75d6d` (8.96 s) |
| same full-run digest, canonical pre-port | **identical** series/E.ALL digests (8.98 s) |
| RNG integrity (`port_verify.py rng-integrity`) — ported | `pl_realize` mask digest `e608cbe2…a2d3f`, reference masks `1f92aca5…3ca14`, probability calls consume **no** caller RNG, 23/23 boundary cases OK |
| same RNG-integrity digests, canonical pre-port | **identical** |
| torch-free default import | OK; `ATLAS_PL_BACKEND=gpu` without torch falls back to CPU gracefully |

Interpretation: the CPU default path is **bit-identical to the canonical pin** (PL fixtures and a full 46-year engine
run), and `pl_realize`/boundary/seat-capacity semantics are unchanged. This satisfies Codex rule 1 on the host side;
the box `pair-cells` command (§4) supplies the backend-level RNG-call-log evidence.
`pl_realize` is untouched: masks are compared directly for fixed caller-supplied uniforms.

## 3. Codex rules mapping (and what is deliberately not done here)

| Codex rule | status / evidence |
|---|---|
| **1. RNG integrity** | `pl_realize` untouched + masks bit-identical (130 fixtures); probability calls consume no RNG (Generator state check); 23 boundary cases (n∈{1,2,12,20,21}, seats 0/1/n−1/n, equal/extreme weights) identical; engine RNG is event-keyed and backend-independent. Box `pair-cells` logs every `EventRNG.uniform` call (year, shock, pid-hash) per run and compares CPU vs GPU sequences. |
| **2. Parity scope** | Host: 68 tests + 130 fixtures at 0.0 CPU delta. Box: `gpu-parity` = 130 fixtures ≤1e-7 + fixed-uniform **winner-flip** counts; `pair-cells` = 2 Pilot-0 cells × seeds 100–101, CPU vs GPU, per-gate-year **winner-set Jaccard/symmetric difference/flipped seats**, plus outcome-scalar deltas. Discrete flips are **reported, not failed** (declared equivalence is on P, not on realisations). |
| **3. Benchmark** | `bench` measures startup import, warmup/compile, 9-row batch vs per-row CPU, peak GPU memory, data-transfer bytes. Full-cell wall clock recipe (§4.f) uses `/usr/bin/time -v` for **multiworker CPU vs GPU, same N/cells/seeds/precision**. Bounded GPU pilot (2 cells) precedes any expansion. |
| **4. Provenance** | every `port_verify.py` artifact carries a manifest: engine file sha256s, env (`ATLAS_PL_BACKEND`, python/numpy/torch/cuda/device), fixture seed+digest, tolerance, UTC, `ENGINE_COMMIT` env if set; CPU and GPU artifacts are written to **separate JSON files**. No retroactive substitution: CPU remains the preregistered primary path; GPU is gate-grid/sensitivity only (amendment A-GPU-1, declared max|dP| ≤ 1e-7). |
| **5. Cross-replica batching** | **NOT implemented** (staged after the bounded pilot). The port batches only the engine's 9-point tutoring grid (existing call shape) and one-row single calls; throughput before/after will be measured by `bench` on the box. Report measured numbers before proposing any cross-replica extension. |

## 4. Exact box parity command set (for `atlas-commander`; no box job from this lane)

Deploy the branch commit read-only to the box, then run **one process at a time**, `nice -n 10`,
`OPENBLAS/MKL/OMP=1`; nothing else on the GPU.

```bash
# 0) DEPLOY (Commander; from the Mac host)
git -C ~/neon-boot/wt4/auditv2 archive 59fd2497765f15c108de3ec182d1febbe3d28c8a | /tmp/box_ssh.sh \
  "mkdir -p /root/work/gpuport_audit && tar -x -C /root/work/gpuport_audit"

# On the box:
cd /root/work/gpuport_audit
export OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1
PY=/root/miniconda3/bin/python            # torch 2.7.1+cu118 expected; RTX 3080 Ti idle

# (a) 68-test contract suite, CPU default (bit-identical reference) -- expect 68 passed
PYTHONPATH=$PWD/engine nice -n 10 $PY -m pytest tests/test_contest_math.py -q -p no:warnings

# (b) 130-fixture CPU central digest -- MUST equal e55a4309ad39c9ddfaa7ffae64c9f286ed01cd109428afd4fe8a7bf8757a8379
PYTHONPATH=$PWD/engine nice -n 10 $PY docs/gpu/port_verify.py cpu-digest \
  --spec docs/audit/canonical_spec.json --json cpu_digest_box.json

# (c) GPU parity, 130 fixtures, declared bound 1e-7 + fixed-uniform winner flips -- expect n_gt_1e7=0
ATLAS_PL_BACKEND=gpu PYTHONPATH=$PWD/engine nice -n 10 $PY docs/gpu/port_verify.py gpu-parity \
  --spec docs/audit/canonical_spec.json --json gpu_parity_box.json

# (d) 68-test suite with GPU backend registered (contract tests must still pass)
ATLAS_PL_BACKEND=gpu PYTHONPATH=$PWD/engine nice -n 10 $PY -m pytest tests/test_contest_math.py -q -p no:warnings

# (e) PAIRED FULL-RUN CELLS (rule 2): 2 Pilot-0 cells, seeds 100-101 (confirmatory block),
#     CPU run vs GPU run; per-gate-year winner sets, RNG call logs, outcome deltas.
#     ~20-25 min bounded pilot on the box (N=1500/T=46, 8 runs total).
ATLAS_PL_BACKEND=gpu PYTHONPATH=$PWD/engine nice -n 10 $PY docs/gpu/port_verify.py pair-cells \
  --spec docs/audit/canonical_spec.json --n 1500 --t 46 --seeds 100-101 \
  --cells market_only,own_open_gap --json paired_cells_box.json

# (f) BENCHMARK (rule 3): microbench (startup/warmup/compile/transfer/peak memory)
ATLAS_PL_BACKEND=gpu PYTHONPATH=$PWD/engine nice -n 10 $PY docs/gpu/port_verify.py bench \
  --spec docs/audit/canonical_spec.json --json bench_gpu_box.json

# (g) full-cell wall clock, same N/cells/seeds/precision, multiworker CPU vs GPU
#     CPU: 2 workers, separate output dir; GPU: 1 process. /usr/bin/time -v for wall+RSS.
mkdir -p /root/work/gpuport_audit/out_cpu2w /root/work/gpuport_audit/out_gpu1w
PYTHONPATH=$PWD/engine nice -n 10 /usr/bin/time -v \
  $PY papers/shadow-education-contest/code/run_paperC_pilot0.py cell market_only 1.0 0.08 100-101 out_cpu2w \
  > out_cpu2w/cell.log 2>&1
ATLAS_PL_BACKEND=gpu PYTHONPATH=$PWD/engine nice -n 10 /usr/bin/time -v \
  $PY papers/shadow-education-contest/code/run_paperC_pilot0.py cell market_only 1.0 0.08 100-101 out_gpu1w \
  > out_gpu1w/cell.log 2>&1
```

Notes for the box run:
* `pair-cells` sets the backend explicitly per phase; launch it with `ATLAS_PL_BACKEND=gpu` so registration happens at
  import. It restores CPU at the end. Timings printed per phase.
* `bench`/`pair-cells` import `torch` only when the flag is set; the CPU checks stay torch-free.
* Keep `gpu_parity_box.json`, `paired_cells_box.json`, `bench_gpu_box.json`, `cpu_digest_box.json`,
  `out_*/cell.log` as **separate CPU/GPU artifacts**; do not overwrite the CPU-reference artifacts.
* GPU `gpu-parity` / `pair-cells` exit non-zero if 130-fixture max|dP| > 1e-7 or any `ΣP` violation; discrete winner
  flips are printed/counted, not failed.
* **No cross-replica batching**: if throughput is the only blocker after the bounded pilot, propose it as a staged
  follow-up with measured before/after (`bench` numbers), per rule 5.

## 5. Residual caveats / handoff notes

* GPU equivalence tests from gpuport (`tests/test_contest_math_gpu.py`) are **not committed here** because `tests/` is
  `qa-verifier` scope; the same checks are provided by `docs/gpu/port_verify.py gpu-parity` (and qa may add the test
  file). Everything else in `docs/gpu/` (GPU docs from gpuport) is likewise **not copied** — only the harness needed to
  verify this port on the box.
* The port's batch helper preserves the documented per-row seat-sum renormalisation; CPU batch is bit-identical by
  construction and verified (130/130).
* Declared deviation remains **max abs dP ≤ 1e-7** (measured on the gpuport box: 4.83e-8 worst over 130 fixtures).
  Run-level scalars can differ slightly more; the paired-cell artifacts report them instead of claiming a bound.
* GPU path stays **gate-grid / sensitivity only**; Paper C/Pilot-0 preregistered primary computation is the CPU path.
* Branch is short-lived and additive: it does not change the canonical spec, gates, RNG, or any CPU numerics.
