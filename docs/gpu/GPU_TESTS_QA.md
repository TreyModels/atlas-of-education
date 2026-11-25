# GPU PL backend — QA test record (`tests/test_contest_math_gpu.py`)

**Owner:** qa-verifier (tests/** lane) · **date:** 2026-11-25 · **branch:** `research/gpu-pl-port-auditv2-2026-11-25`
**Engine port commit:** `59fd249` (branch head for engine files; docs follow-up `2399aa1`). GPU backend is
**gate-grid / sensitivity only** (amendment A-GPU-1): the canonical CPU pin (`e111397b…` / spec `e5ddef6b…`)
remains the primary path; this branch's core hash is `5bcbc0b3…` and **must not** replace canonical artifacts.
**Verdict: tests PASS on CPU (Mac) and on the CUDA box; 130-fixture GPU-vs-CPU parity max |dP| = 4.83e-8 ≤ 1e-7,
0 seat-sum violations, 0 discrete winner flips on fixtures. Final GPU sign-off still needs the Commander's
2-cell / seeds 100–101 cell-level Jaccard/flip parity + full-wall benchmark (not yet in hand).**

## Added test file

`tests/test_contest_math_gpu.py` (committed on this branch; engine untouched). Coverage:

1. **Default is CPU and torch-free** — subprocess import with `ATLAS_PL_BACKEND` unset: `pl_backend()=='cpu'`,
   `torch` and `eduengine.contest_gpu` absent from `sys.modules`, PL call works.
2. **Registration flag contract** — `set_pl_backend('cpu')`; `set_pl_backend('gpu')` raises the documented
   `RuntimeError` when no backend is registered (and round-trips on a GPU host); invalid names rejected.
3. **Graceful CPU fallback** — `ATLAS_PL_BACKEND=gpu` with torch blocked (`torch.py` raising ImportError on
   `PYTHONPATH`) still imports, stays `pl_backend()=='cpu'`, and computes.
4. **CPU batch ≡ per-row** — `pl_win_probs_batch` vs `pl_win_probs` **bit-identical** (`np.array_equal`) on a
   26-fixture representative set; seat sums exact.
5. **Boundary / capacity cases** — n ∈ {1,2,12,20,21}, seats {0,1,n−1,n}, equal/extreme weights
   (1e−200/1e200, geomspace 1e−12…1e12), multi-row batch independence: finite, [0,1], ΣP=min(seats,n),
   batch == per-row.
6. **GPU-vs-CPU 130-fixture parity** (CUDA host only) — canonical `docs/gpu/port_verify.py` fixture generator
   (seed 20261125, 130 fixtures); per fixture GPU one-row batch vs CPU reference; **max |dP| ≤ 1e-7**, seat
   sums preserved; asserts the GPU path was actually exercised (`pl_stats` batch/gpu counters).
7. **GPU boundary parity** — same boundary/capacity cases on GPU ≤ 1e-7 vs CPU.
8. **Discrete flips reported, not failed** — fixed-uniform `pl_realize` masks CPU vs GPU on 13 fixtures; flip
   count printed/collected (0 here); equivalence is declared on probabilities, not realisations.

## Run results

### Mac host (CPU-only, no torch) — default gate

```
PYTHONPATH="$PWD/engine" ~/neon-boot/venv/bin/python -m pytest tests/test_contest_math_gpu.py -q
# 5 passed, 3 skipped in 1.69s   (GPU tests skip cleanly: "torch/CUDA backend not available")
```

### Box (CUDA) — full suite

Host: `/root/miniconda3/bin/python` 3.10.8, torch **2.7.1+cu118**, CUDA 11.8, numpy 1.24.1, pytest 9.2.0,
GPU **NVIDIA RTX 3080 Ti** (idle), branch deployed read-only at `/root/work/gpu_qa`.

```
cd /root/work/gpu_qa
OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 ATLAS_PL_BACKEND=gpu \
PYTHONPATH=$PWD/engine nice -n 15 /root/miniconda3/bin/python -m pytest tests/test_contest_math_gpu.py -q -rA
# 8 passed in 57.29s
#   ... test_gpu_vs_cpu_130_fixture_parity_within_1e7 PASSED
#   ... test_gpu_boundary_cases_within_1e7 PASSED
#   discrete winner flips CPU-vs-GPU (reported, not failed): 0
```

### Independent 130-fixture parity artefact (box, `docs/gpu/port_verify.py gpu-parity`)

`docs/gpu/results/gpu_parity_qa.json` (copied from the box run):

| metric | value |
|---|---|
| max abs dP (GPU vs CPU) | **4.832148292610583e-08** (≤ 1e-7) |
| mean abs dP | 1.698424181981504e-08 |
| fixtures > 1e-7 / > 1e-6 | **0 / 0** of 130 |
| seat-sum violations | **0** |
| discrete winner flips (fixtures, fixed uniforms) | **0** (0 fixtures) |
| GPU path evidence | `batch_rows=130`, `gpu.engine_builds=112`, `gpu.gpu_calls=112` |
| engine hashes | core `5bcbc0b3…279f75`, contest_math `5fceb4d5…0bee944`, contest_gpu `ab08a53b…596f`, tutoring `b3d32cee…c3fdf` |
| env | python 3.10.8, numpy 1.24.1, torch 2.7.1+cu118, CUDA 11.8, RTX 3080 Ti |

## Defects / provenance gaps found in the verification harness (not engine failures)

| id | severity | finding |
|---|---|---|
| G1 | medium | `docs/gpu/port_verify.py` `gpu_parity()` resets `cm.set_pl_backend('cpu')` (line **236**) **before** building the manifest (line **239**), so the GPU artifact's `manifest.env.backend` records **`cpu`** even though the GPU path ran (the `pl_stats` counters prove it: `gpu.engine_builds=112`, `batch_rows=130`). Fix: snapshot `backend()`/gpu stats before the reset and pass them into `manifest()`. |
| G2 | low | `manifest.engine_commit` is empty (line **113**, `ENGINE_COMMIT` env not set in the run). For provenance, export `ENGINE_COMMIT=59fd249` (or record the core hash + branch) in box runs. |
| G3 | low | The manifest records engine file hashes but not the **canonical spec sha** (`docs/audit/canonical_spec.json`); add `spec_sha256` so GPU artifacts show the `e5ddef6b…` re-pin provenance next to engine `846c9e0`/port hashes. |

These are harness-reporting gaps only; the numeric parity evidence is sound (GPU-vs-CPU ≤ 1e-7, seat sums exact,
0 fixture flips). They do not affect the CPU primary path.

## Still pending before GPU sign-off (lead's condition)

1. Commander's **cell-level** box parity: 130 fixtures + 68 tests + **2 Pilot-0 cells × seeds 100–101**, per
   gate-year winner-set Jaccard / symmetric difference / **flipped seats**, and the **full-wall benchmark**.
2. Sign-off rule: ≤ 1e-7 **and** no unresolved flip that changes a headline outcome; otherwise **require CPU
   fallback** for that use. Discrete flips on ties are reported, not failed (declared equivalence is on P).
3. Pilot-0 remains a **CPU-only** campaign on the canonical engine pin; GPU artifacts are separate and are not
   part of the Pilot-0 record.
