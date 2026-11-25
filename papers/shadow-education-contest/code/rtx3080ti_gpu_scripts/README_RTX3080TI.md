# RTX 3080 Ti (CUDA 11.8, 12GB VRAM) Runbook for DeepSeek

## Environment (Miniconda, Python 3.10, Ubuntu 22.04, CUDA 11.8)
```bash
pip install torch --index-url https://download.pytorch.org/whl/cu118
pip install numpy pandas scipy
nvidia-smi
```

## 1. Exact Patched Engine & HK/Korea Code Bundle (Already Verified on Google Drive)
Download `hk_korea_contest_code_bundle.zip` (Drive File ID: `1FTJiVvt-BGFMjBxRsHiN6uiZbEkfeAAS`, 125 KB) containing:
- `engine/eduengine/core.py` (exact `Engine(modules, **params)` + `E.R` + Tullock `contest` gate, 22/22 tests PASS)
- `engine/eduengine/modules/tutoring.py`
- `contest_gate.patch` (`git apply --check` PASS on `68da16e`)
- `run_hk_korea_comparative.py` (18 arms x 30 seeds, including CF4a & CF4b Win-Win arms)
- `hk_korea_comparative_with_cf4.json` (completed 540-run output)

Place into `papers/shadow-education-contest/code/` on branch `research/shadow-education-contest-2026-11-25` and push to GitHub.

## 2. GPU Job 1 (~8-12 min on RTX 3080 Ti): Paper #1 Wild-Cluster & Block-Permutation Null
```bash
# Quick selftest (verifies GPU batched CR1 + wild-cluster bootstrap):
python3 gpu_e1_q3_wild_cluster_ri.py --B 2000 --out-dir ./results_rtx3080ti/e1_q3_selftest

# Full run on E1/Q3 panel CSV:
python3 gpu_e1_q3_wild_cluster_ri.py \
  --panel-csv <path_to_e1_panel.csv> \
  --y-col <y_col> --x-col <x_col> --cluster-col country \
  --B 2000 --out-dir ./results_rtx3080ti/e1_q3_wild_cluster
```

## 3. GPU Job 2 (~2-3 min on RTX 3080 Ti): 200k-Draw Bray 7-Param ABC + 2,000-Point Contest Surface
```bash
python3 gpu_bray_abc_and_contest_surface.py \
  --n-abc 200000 \
  --out-dir ./results_rtx3080ti/bray_and_contest
```

## 4. Push Outputs
Commit `results_rtx3080ti/*.json` + `pip freeze > env_lock_rtx3080ti.txt` to `papers/shadow-education-contest/code/results/`, and push to GitHub.

> **Deposit note (shadow branch, 2026-11-25):** this runbook is deposited from the canonical all-in-one bundle
> as received, with one change: the original "and power off the RTX 3080 Ti instance" instruction has been
> removed. Powering instances off or rebooting them is **operator-only** in this repository; agents must not do it.
