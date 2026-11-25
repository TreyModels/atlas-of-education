# Corrected GPU-experiment harness (P0-07 execution-integrity remediation)

**Audit target (frozen, read-only):** [`../gpu_abc_bundle/`](../gpu_abc_bundle/) @ `045a63e` — never modified by
this harness. **Audit finding:** [`../EXTERNAL_AUDIT_GPU_2026-11-25.md`](../EXTERNAL_AUDIT_GPU_2026-11-25.md) §P0-07.
**Status:** harness built + failure-propagation proof executed (CPU only, tiny n, no CUDA, no torch); the real
GPU/CPU-torch experiment matrix is defined but **not executed** in this audit (torch parked, no GPU campaign).

This directory is a **new** directory; it does not patch or rewrite the frozen audited snapshot. The archived
runner is preserved byte-for-byte and its defects are retained as the negative record.

---

## 1. What the archived runner did wrong (P0-07, verified against the bundle)

`gpu_abc_bundle/run_gpu_jobs.sh` (sha256 `b0334816…96df3`):

| # | defect (audit §P0-07) | consequence |
|---|---|---|
| 1 | `set -u` only; `run()` captures `PIPESTATUS[0]` but only **echoes** it — no `set -e`/`pipefail` | a failed job does not stop the sequence; the run ends with `DONE` and can look clean |
| 2 | the **6-parameter run is absent** from the runner | the deposited 6-param JSON cannot be reproduced by the deposited runner |
| 3 | `gpu_bray_abc_and_contest_surface_6param.py` keeps the 7-param default `--out-dir` | a default run would **overwrite** the 7-param output |
| 4 | JSON writes are plain `open(...,"w")` inside job scripts | a crash can leave a truncated/partial result file |
| 5 | job parameters/configs are not hashed anywhere | no way to prove which configuration produced an output |
| 6 | one fixed seed `20261125`; no seed provenance | validation runs are indistinguishable from replays |
| 7 | accepted draws discarded; advertised “100-Fresh-Seed Stability Bank” not implemented (`gpu_bray…py` docstring) | no posterior diagnostics/predictive checks possible; the stability claim is contradicted |

## 2. What this harness changes (fix ↔ mechanism)

| fix | mechanism in `run_gpu_jobs_fixed.sh` |
|---|---|
| fail-fast + real failure propagation | `set -euo pipefail`; each job's rc captured explicitly; **first non-zero rc aborts the whole run with that exact rc**; `run_failure.json` written; no `manifest.json` assembled |
| unique, non-colliding output locations | `RUN_ID = <UTC timestamp>-<git short sha>-<urandom nonce>`; `mkdir` fails on collision; every job gets `runs/<RUN_ID>/jobs/<job_id>/`; `--out-dir` is always injected by the harness |
| include the 6-param run | first-class job `job2b_bray_abc_6param` (distinct job dir ⇒ cannot overwrite the 7-param output) |
| atomic JSON writes | jobs write into `jobs/<job_id>/.staging/`; only after rc==0 does the harness `mv` the single expected JSON into its final path (same-filesystem atomic rename); on failure staging is removed |
| hashed configs | every `configs/*.json` sha256 recorded in `evidence/config_hashes.json` and per job in the run manifest |
| independent validation seeds | `tools/make_seeds.py` draws from the OS CSPRNG (`secrets.randbits(31)`), one per job; seeds recorded in `seeds.json`, hashed, and the archived seed `20261125` is explicitly not reused |
| frozen-target integrity | `verify_bundle_manifest.sh` runs `MANIFEST.sha256` check **before and after** each run and records a whole-directory digest; the run aborts if the two digests differ |
| audited-script gate | bundle scripts are refused unless their sha256 equals the audited hashes (7-param `0709032c…`, 6-param `012b14bb…`, E1/Q3 `3bbbc19a…`) |

## 3. Files

| file | purpose |
|---|---|
| `run_gpu_jobs_fixed.sh` | the corrected harness (`--mode real|dry-run`, `--jobs real|control|failure`) |
| `verify_bundle_manifest.sh` | read-only `MANIFEST.sha256` verification + whole-directory digest (before/after witness) |
| `dry_run_failure_propagation.sh` | **acceptance test**: runs the archived-pattern demo, a control dry-run, and the deliberate-failure dry-run; asserts all properties; writes `evidence/dry_run_evidence.json` |
| `configs/jobs_real.json` | real-mode matrix: 7-param ABC, **6-param ABC**, E1/Q3 GPU selftest, CPU reference, derived GPU-vs-CPU diff |
| `configs/job*.json` | per-job parameter/config blocks (hashed at run time) |
| `configs/jobs_dry_run_control.json`, `configs/jobs_dry_run_failure.json` | dry-run matrices (tiny CPU stubs) |
| `stubs/stub_job_ok.py` | tiny CPU-only stub that writes atomically (n=8/5) |
| `stubs/stub_job_fail.py` | deliberately failing stub (writes a partial temp file, exits 7) |
| `tools/make_seeds.py` | independent validation seeds (OS CSPRNG; deterministic derived mode available) |
| `tools/record_job.py` | writes one JSON record per job attempt to `manifest.jsonl` |
| `tools/assemble_manifest.py` | builds `manifest.json` atomically; refuses to mark a run “ok” if any job failed or config/matrix diverge |
| `tools/gpu_vs_cpu_diff.py` | first-class derived arithmetic-diff job (replaces the ad-hoc archived artifact) |
| `tools/archived_pattern_demo.sh` | faithful reduction of the archived runner's defect (echo-only rc) used by the proof |
| `evidence/` | executed proof artifacts (dry-run runs, manifests, logs, `dry_run_evidence.json`) |

## 4. Running it

**Failure-propagation proof (CPU only, torch-free; this is what was executed):**

```bash
PYTHON=/root/miniconda3/bin/python ./dry_run_failure_propagation.sh
# or on the host: PYTHON=/Users/treymenefee/neon-boot/venv/bin/python ./dry_run_failure_propagation.sh
```

Expected result: `RESULT: PASS` and `evidence/dry_run_evidence.json` with
`"passed": true`. It proves, in one run:
- the **archived** pattern exits **0** and prints `DONE` even though a job exited 7 (defect reproduced);
- the **corrected** harness exits **7** (the exact failing rc), writes `run_failure.json`, assembles **no**
  `manifest.json`, leaves **no** partial result JSON, and **never starts** the sentinel job that follows the
  failure;
- the all-succeed control exits **0** with a valid manifest, matching output hashes, and an unchanged frozen-bundle
  digest.

**Real experiment matrix (not executed here; requires torch+GPU/CPU-torch):**

```bash
PYTHON=/root/miniconda3/bin/python ./run_gpu_jobs_fixed.sh --mode real --jobs real
# → runs/<timestamp>-<sha>-<nonce>/  (2×ABC incl. 6-param, E1/Q3 GPU + CPU ref, derived diff)
# → jobs/<job_id>/<output>.json, stdout.log, manifest.jsonl, manifest.json, seeds.json
```

**Manifest verification only:**

```bash
./verify_bundle_manifest.sh            # prints 12/12 OK + bundle_dir_digest_sha256
```

## 5. Executed evidence (this audit)

- **Host (macOS arm64, Python 3.10.2, numpy 2.2.6) 2026-11-25T06:59Z:** `RESULT: PASS` — archived pattern
  rc=0/DONE with a failing job; corrected control rc=0; corrected failure rc=7; all 18 assertions pass.
  → `evidence/dry_run_evidence.json`, `evidence/dry_runs/dryrun-*`, `evidence/archive*/`.
- **Box (`/root/work/audit`, `/root/miniconda3/bin/python` 3.10.8, numpy 1.24.1, 1 worker, `nice -n 10`):** same
  proof re-executed in the clean box environment; see `evidence/box_execution/` (copied back read-only).
- **Canonical `MANIFEST.sha256`: 12/12 files OK**; bundle directory digest
  `8d58e6ff750c8e512124f74474efd33ed71fe81c200f772e76c9539966f3cfbf` unchanged before/after every run and
  unchanged in git (`git status --porcelain docs/audit/gpu_abc_bundle` empty).

## 6. Limits (stated plainly)

- The harness contract is proven with **CPU stubs**, not by executing the GPU scripts: torch is parked and no GPU
  campaign is authorised. The real-mode matrix is therefore **defined, hashed and preflighted** (torch+numpy check,
  audited-script hashes, unique dirs) but its execution is future work; it will not run under this audit.
- The dry-run stubs are **not experiments**; their outputs carry no scientific status.
- GPU/CPU agreement remains arithmetic validation only; this harness does not and cannot promote any GPU claim to
  `VALIDATED SIMULATION` (see `../SCIENTIFIC_CLAIM_LEDGER.md`).
