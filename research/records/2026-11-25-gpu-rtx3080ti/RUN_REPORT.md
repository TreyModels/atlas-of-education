# RTX 3080 Ti GPU run — 2026-11-25

Branch `research/gpu-rtx3080ti-2026-11-25`. Record `research/records/2026-11-25-gpu-rtx3080ti/`.
Owner: `gpu-rtx3080ti` (shared task `task-10`). Host: AutoDL box `root@connect.nmb2.seetacloud.com:36934`.
Source bundle: `rtx3080ti_gpu_scripts_bundle.zip`, SHA256 `bb481b87a8ae1bac63d33ca3a4424ef7195fd29baaae9c3432d7e92ee7785550` (verified before use; see `bundle/SOURCE_BUNDLE.sha256`).

## Bottom line

- **Environment installed and GPU verified**: `torch 2.7.1+cu118`, `torch.cuda.is_available() == True`, GPU = **NVIDIA GeForce RTX 3080 Ti** (12,288 MiB, capability 8.6, CUDA runtime 11.8). The two supplied GPU scripts both ran on the GPU (`[GPU] Using NVIDIA GeForce RTX 3080 Ti (CUDA 11.8)` in both logs); a separate CUDA burn held `nvidia-smi` at **100 % util / ~287 W**.
- **Job 2 ran**: 200,000-draw ABC, accept rate **0.046 %** (92/200,000), best `max_z` **0.455**; 2,000-point contest surface, paradox shares **1.0 / 1.0**, mean participation jump **0.3709**. Raw JSON committed.
- **Job 1 selftest ran**: GPU-internal elapsed **1.234 s**; wild-cluster `p = 0.000499750` (= 1/2001 floor), block-permutation `p = 0.000999` (= 1/1001 floor). A CPU-forced rerun of the same selftest agrees on every deterministic quantity to **max abs diff 8.9e-15**; RNG-dependent bootstrap percentiles differ because CUDA and CPU RNG streams differ for the same seed (p-values still identical). Raw JSONs committed.
- **E1/Q3 full panel mode: NOT RUN — panel CSV MISSING** (details below).
- **Scope qualifications** (review findings; do not overclaim): the shipped 7-parameter ABC is **not identifiable** (one parameter is dead) — a corrective 6-parameter run is included and labelled separately; the contest surface is an **approximate** fixed-point sensitivity exercise, not a boundary map of the engine's realized contest mechanism; the E1/Q3 selftest is a **GPU-numerics validation only**, not a robustness check for E1/Q3.
- Box left **RUNNING** (not powered off). No secrets committed; no watchers/timers created.

## Box and environment

| Item | Value |
|---|---|
| Host / OS | AutoDL container `autodl-container-wjb02xe512-3c3a2b3b`, Ubuntu 22.04.1 LTS |
| CPU / RAM | 80 cores, Intel(R) Xeon(R) Gold 6248 CPU @ 2.50 GHz / ~251 GiB |
| GPU | NVIDIA GeForce RTX 3080 Ti, 12,288 MiB, VBIOS 94.02.71.40.24, capability 8.6 |
| Driver | 595.71.05 (driver-reported “CUDA Version: 13.2”; runtime installed is cu118) |
| Python | /root/miniconda3/bin/python 3.10.8 |
| Libraries | numpy 1.24.1 (pre-existing), pandas 2.3.3, **torch 2.7.1+cu118** |
| Disk | 30 GB overlay, ~29 GB free after install |

Full `nvidia-smi` output: `logs/nvidia_smi.txt`; one-line spec: `logs/gpu_spec.csv`.
Frozen environment: `env_lock_rtx3080ti.txt` (`pip freeze`, 152 packages).

## Install (including the failure that was hit and fixed)

Step 1, exactly as instructed:

```
/root/miniconda3/bin/pip install torch --index-url https://download.pytorch.org/whl/cu118
```

**This first attempt FAILED** (`TORCH_EXIT:1`; full log `logs/pip_torch.log`). Exact error:

```
Discarding https://files.pythonhosted.org/.../typing_extensions-4.16.0-...whl (from https://download.pytorch.org/whl/cu118/typing-extensions/)
  (requires-python:>=3.9): Requested typing-extensions>=4.10.0 from https://files.pythonhosted.org/... has inconsistent Name:
  expected 'typing-extensions', but metadata has 'typing_extensions'
Downloading typing_extensions-4.16.0.tar.gz (113 kB)
Installing build dependencies: started ... error: subprocess-exited-with-error
ERROR: Could not find a version that satisfies the requirement flit_core<4,>=3.11 (from versions: none)
ERROR: No matching distribution found for flit_core<4,>=3.11
```

Cause: pip 22.3.1 + a `typing-extensions` metadata-name mismatch made pip fall back to a **source** distribution, whose build isolation used the pytorch-only index, which hosts no `flit_core`. `pandas` had already installed OK from the box's default Aliyun mirror (`Successfully installed pandas-2.3.3 tzdata-2026.6`).

Recovery (all logs kept: `logs/pip_fix.log`, `logs/install_local.log`, `logs/finish.log`):

1. `pip install typing_extensions` (Aliyun mirror) — satisfied the dependency so the sdist fallback was skipped.
2. Retried torch: dependency resolution now worked but the official CDN (`download-r2.pytorch.org`) delivered the 905 MB torch wheel at ~10–170 KB/s (unusable; a 155 MB triton wheel was also crawling at ~174 KB/s).
3. Fetched the same wheels from the Aliyun pytorch-wheels mirror with resumable curl, **verified their SHA256 against the pytorch index**, and installed from the local files:

```
curl -sSL --retry 8 -C - -o torch-2.7.1+cu118-cp310-cp310-manylinux_2_28_x86_64.whl \
  https://mirrors.aliyun.com/pytorch-wheels/cu118/torch-2.7.1%2Bcu118-cp310-cp310-manylinux_2_28_x86_64.whl
sha256sum → 89433c62b02ec802d4c0887c867d935887ae8f00d7cc549ecf1c2640d096bd4c  (905,334,729 bytes; matches pytorch index)
curl ... -o triton-3.3.1-cp310-cp310-manylinux_2_27_x86_64.manylinux_2_28_x86_64.whl   (aliyun mirror)
sha256sum → b74db445b1c562844d3cfad6e9679c72e93fdfb1a90a24052b03bb5c49d1242e  (matches pytorch index)
/root/miniconda3/bin/pip install ./triton-3.3.1-...whl
/root/miniconda3/bin/pip install ./torch-2.7.1+cu118-...whl --index-url https://download.pytorch.org/whl/cu118
```

Final verification:

```
torch 2.7.1+cu118
cuda_available True
cuda_version 11.8
gpu NVIDIA GeForce RTX 3080 Ti
capability (8, 6)
matmul_sum -162.28988647460938
```

GPU-active evidence (independent of the job logs): an 8 s CUDA matmul burn sampled with `nvidia-smi` showed **100 % util, 380 MiB, 40–42 °C, 287–288 W** (`logs/gpu_burn_util.txt`):

```
2026/11/25 14:37:43.123, 100 %, 380 MiB, 40, 286.99 W
2026/11/25 14:37:45.178, 100 %, 380 MiB, 42, 288.08 W
```

## Job 2 — Bray ABC + contest sensitivity surface

Command (run from `/root/work/gpu`, wall **2.73 s**):

```
/root/miniconda3/bin/python gpu_bray_abc_and_contest_surface.py \
  --n-abc 200000 --out-dir ./results_rtx3080ti/bray_and_contest
```

Log first line: `[GPU] Using NVIDIA GeForce RTX 3080 Ti (CUDA 11.8)`. Raw JSON: `results/bray_and_contest/bray_abc_and_contest_surface.json`.

### Part A — as-shipped 7-vector ABC (NOT a 7-parameter calibration; see qualifications)

| Quantity | Value |
|---|---|
| n_draws | 200,000 |
| n_accepted | **92** |
| accept_rate_pct | **0.046 %** |
| best_max_z | **0.455** (within tolerance; `best_theta` is an accepted draw) |
| best_theta_7param | `[-0.7231, 0.387, 1.3392, 1.4155, 1.316, 0.2097, -0.8241]` |
| posterior_corr_cond_6active | 25.96 |
| elapsed_sec (ABC) | 0.31 |
| wall (whole script) | 2.73 s |

The JSON key says `best_theta_7param`, but as shipped **`theta[5]` (`teacher_threshold`) never enters the utilities or the moment equations**; only 5 moment targets are used. This is therefore an ABC over 7 sampled coordinates with **5 active parameters and 5 moments**, i.e. **not** a 7-parameter calibration.

### Part A-corrected — 6-parameter variant (this lane, after review finding)

`scripts/gpu_bray_abc_and_contest_surface_6param.py` is a minimal corrective variant of the supplied script: it **drops the dead `teacher_threshold` coordinate**, draws 6 parameters `[b0_eff, b_income, b_school_gap, delta_g12, urban_demand, delta_other]` against the same 5 moment targets, and records `n_params: 6` / `dropped_param` in its JSON. Everything else (moments, tolerances, seed 20261125) is unchanged; Part B is unchanged.

Command: `/root/miniconda3/bin/python gpu_bray_abc_and_contest_surface_6param.py --n-abc 200000 --out-dir ./results_rtx3080ti/bray_and_contest_6param`
Log first line: `[GPU] Using NVIDIA GeForce RTX 3080 Ti (CUDA 11.8)`. Raw JSON: `results/bray_and_contest_6param/bray_abc_and_contest_surface.json`.

| Quantity | Value |
|---|---|
| n_draws | 200,000 |
| n_params | **6** (`teacher_threshold` dropped) |
| n_accepted | **77** |
| accept_rate_pct | **0.0385 %** |
| best_max_z | **0.4075** |
| best_theta_6param | `[-0.6343, 0.2392, 0.9809, 1.349, 1.2229, -0.6682]` |
| posterior_corr_cond_6active | 21.03 |
| elapsed_sec (ABC) | 0.30 |

Caveat retained: 6 parameters against 5 moment targets is still one dimension short of a strictly identified fit by moment count; the low acceptance rates (0.04–0.05 %) and moderate posterior condition number (21–26) describe a thin, correlated accepted region rather than a strong calibration.

### Part B — 2,000-point contest sensitivity surface (APPROXIMATE)

| Quantity | Value |
|---|---|
| grid_points | 2,000 (20 r × 20 price × 5 seat shares) |
| r_range | [0.8, 2.5] |
| price_range | [0.05, 0.30] |
| seat_shares | [0.12, 0.16, 0.23, 0.35, 0.50] |
| share_cells_paradox_S012_to_S016 | **1.0** |
| share_cells_paradox_S012_to_S050 | **1.0** |
| mean_participation_jump_S012_to_S050 | **0.3709** |
| elapsed_sec | 0.036 |

The paradox indicator is `1.0` in **every** cell, so this surface **saturates**: the simplified solver says expanded seats raise mean spend everywhere in the grid, not “in a mapped subset”. Combined with the mechanism caveat below, read this as a qualitative/approximate sensitivity exercise, not as an exact boundary map or as the engine's realized contest mechanism.

## Job 1 — E1/Q3 wild-cluster bootstrap + block-permutation selftest

Command (run from `/root/work/gpu`, wall **3.59 s**):

```
/root/miniconda3/bin/python gpu_e1_q3_wild_cluster_ri.py --B 2000 --out-dir ./results_rtx3080ti/e1_q3_selftest
```

Log first line: `[GPU] Using NVIDIA GeForce RTX 3080 Ti (CUDA 11.8)` — **no CPU fallback**. Raw JSON: `results/e1_q3_selftest/wild_cluster_ri_results.json`.

| Quantity | Value |
|---|---|
| mode | selftest_minority_effect_15pct (built-in synthetic; N=1200, G=60) |
| beta1 | 0.4447407388610457 |
| se_cr1 | 0.08291358451449403 |
| t_obs | 5.3639067888 |
| p_wild_cluster | **0.0004997501249375312** (= 1/2001 floor, B=2000) |
| t_boot_q025 / q975 | -2.1116 / 2.1204 |
| p_block_perm | **0.000999000999000999** (= 1/1001 floor, B=1000) |
| perm_mean / perm_sd | 0.082946 / 0.052174 |
| elapsed_sec (GPU) | 1.234 |

### CPU-forced numerics reference (added by this lane)

Same script, same seed, CUDA hidden:

```
CUDA_VISIBLE_DEVICES="" /root/miniconda3/bin/python gpu_e1_q3_wild_cluster_ri.py \
  --B 2000 --out-dir ./results_rtx3080ti/e1_q3_selftest_cpu_ref
```

Log first line: `[CPU] CUDA not available; falling back to CPU` (as intended). Wall **2.41 s**, internal 0.316 s. Raw JSON: `results/e1_q3_selftest_cpu_ref/wild_cluster_ri_results.json`; diff: `results/e1_q3_selftest/gpu_vs_cpu_diff.json`.

- **Deterministic quantities (identical inputs)** agree to **max abs diff 8.88e-15**, max relative diff 3.0e-15: `beta1` 1.33e-15, `se_cr1` 1.11e-16, `t_obs` 8.88e-15, `beta_obs` 1.33e-15.
- **p-values identical**: `p_wild_cluster` = 0.0004997501… on both; `p_block_perm` = 0.000999… on both.
- **RNG-dependent bootstrap moments differ** by design: `t_boot_q025` Δ = 0.08998, `t_boot_q975` Δ = 0.00653, `perm_mean` Δ = 3.4e-6, `perm_sd` Δ = 6.2e-4. Reason: `torch.Generator(device='cuda')` and the CPU generator produce different streams for the same seed, so the resamples themselves differ; this is not numerical disagreement. Both p-values sit on their floor and are insensitive to it.

## E1/Q3 full panel mode — MISSING

The full mode requires a country-level panel CSV with `country`/`y`/`x` columns. **No such file exists in the repository**, so `--panel-csv` mode was **not run**.

Searched: `origin/main`, `origin/research/e1-multiverse-1200-2026-11-25`, `origin/research/q3-multiverse-calibration-2026-11-25`, `origin/research/shadow-education-contest-2026-11-25` (file lists and content greps for `e1_panel`, `panel.csv`, E1/Q3/panel CSVs). Closest artifacts — and why they are not the panel:

- `research/records/2026-11-25-q3-calibration/inputs/edge_table400.csv` (and the E1-multiverse copy): columns `x,y,topic,in_base_survivors,pooled_FE_t,pooled_TR_t,share_TR,...` — a **results table** of link statistics (`x`/`y` are indicator names, rows are links), not observations of `country`/`y`/`x`.
- `research/records/2026-11-25-q3-calibration/inputs/null_shares_TR.csv.gz` — a stored null array, not a panel.
- `research/records/2026-11-25-e1-multiverse/results/panel_hashes.txt` points to raw per-indicator JSON sources (`/root/work/data`, `ISOS_sha256=…`) that are **not committed**; the box has no `/root/work/data` directory.

Consequence: **no panel-mode numbers are reported, and none are fabricated**. Also, per the review, even a panel CSV would not make this a reconstruction of the E1/Q3 estimators: panel mode fits only `[intercept, x]` and drops controls/FE.

## Qualifications and scope limits (read before citing)

1. **The shipped 7-parameter ABC is not a 7-parameter calibration.** `theta[5]` (`teacher_threshold`) is dead code in the supplied script and only 5 targets are used. The as-shipped output is reported raw and explicitly labelled; a corrective 6-parameter run (dropping the dead coordinate) is included as `results/bray_and_contest_6param/`. Neither run should be described as a validated 7-parameter Bray calibration.
2. **The 2,000-point contest surface is APPROXIMATE.** It is a simplified fixed-point Tullock/Plackett-Luce best-response exercise on a 1,000-household synthetic income draw, distinct from the engine's realized contest mechanism. The paradox share saturating at 1.0/1.0 is a property of this simplification; do not read it as an exact H2 boundary or a mechanism-level result.
3. **The E1/Q3 selftest is GPU-numerics validation only.** The built-in synthetic minority-effect selftest plus the GPU-vs-CPU diff validate that the batched GPU implementation reproduces the float64 CPU computation (deterministic stats ≈1e-14 relative). It is **not** a robustness/reconstruction check for the published E1/Q3 estimators; panel mode itself fits only `[intercept, x]` with no controls/FE.
4. Raw outputs and both failure and success logs are preserved. Nothing in this record asserts academic results beyond the above.

## Box contention note (operational, for the operator)

While installing, a second, unexplained SSH session touched **this lane's** box working directory. Timeline (from `/proc` and logs):

- 14:27 local: a session (`sshd: root@notty`) ran `kill 2515 2510` — killing **this lane's** stalled pip — then started an Aliyun-mirror torch install in `/root/work/gpu` (`pip_fast.log`). The Lead confirmed it was not the Lead and `model-fix` (task-11) confirmed it was not them. Most likely the operator's separate window.
- 14:29–14:31: a session ran `wget -c -O /root/work/gpu/torch-2.7.1+cu118.whl <aliyun url>` plus a battery of mirror speed probes (aliyun offset probe, sjtu, ustc, huawei, official). That actor is independently repairing the same torch install. Its partial download (`torch-2.7.1+cu118.whl`, ~12.8 MB) was left untouched in `/root/work/gpu` (not operator data was moved/deleted).
- This lane stopped only **its own** stalled pip child (pid 3890) as part of the takeover, and used distinct filenames/logs for its verified install. `torch` was re-verified after all runs; nothing else on the box was touched. `model-fix` (scipy install, CPU-only work in `/root/work/modelrev`) is unaffected.

## Artifacts (all committed here; SHA256 in `MANIFEST.sha256`)

```
scripts/gpu_bray_abc_and_contest_surface.py            # shipped, as received (SHA256 0709032c…)
scripts/gpu_e1_q3_wild_cluster_ri.py                   # shipped, as received (SHA256 3bbbc19a…)
scripts/gpu_bray_abc_and_contest_surface_6param.py     # corrective 6-param variant (this lane)
scripts/run_gpu_jobs.sh                                # exact job driver used
bundle/README_RTX3080TI.md, bundle/SOURCE_BUNDLE.sha256
results/bray_and_contest/bray_abc_and_contest_surface.json
results/bray_and_contest_6param/bray_abc_and_contest_surface.json
results/e1_q3_selftest/wild_cluster_ri_results.json
results/e1_q3_selftest_cpu_ref/wild_cluster_ri_results.json
results/e1_q3_selftest/gpu_vs_cpu_diff.json
logs/  (job logs, full run wrapper, nvidia-smi, gpu spec, install/failure logs, gpu burn util, sha256_scripts.txt)
env_lock_rtx3080ti.txt
```

`bundle/SOURCE_BUNDLE.sha256` = the SHA256 of the downloaded zip. Box-side script hashes (`logs/sha256_scripts.txt`) match the committed copies exactly, confirming intact scp.

## Box state

Left **RUNNING and idle** (GPU no longer under load after the 8 s burn). `torch 2.7.1+cu118` remains installed in `/root/miniconda3`. No shutdown/reboot/power actions were taken; no watchers/timers were created. No secrets (box password, keys) were printed, copied into this repo, or committed — the only host identifiers committed are the non-secret ubuntu/GPU specs and hostname.
