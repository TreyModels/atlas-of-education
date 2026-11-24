# Box-run evidence — 25 Nov 2026 (pre-shutdown freeze)

Everything in this record was produced on the AutoDL instance
`autodl-container-a8f742b5ee-292349c5` (`ssh -p 45973 root@connect.cqa1.seetacloud.com`,
15-CPU cgroup quota, RTX 4090 D, Python 3.10.8 / numpy 1.24.1) and pulled host-side before the
instance was released. Nothing here was edited by hand; each file is the artefact as written by its
runner.

## Contents

| dir | what | runner | notes |
|---|---|---|---|
| `engine-fixed-1440/` | `results_multiverse_fixed.json` (1,440 runs = 144 combos × 10 seeds), `summary_multiverse_fixed1440.json`, `decomp_fixed1440.json`, `analyze_fixed1440.log`, `run_fixed.log`, `report_decomp.py` | `run_edsystem_multiverse.py` from `fix/edsystem-exit-reason-2026-11-25` @`4679ddb` (driver reads `e.exits` via `aggregate_exits`) | wall 319.9 s at 12 workers on the box; `driver_sha256` recorded in `decomp_fixed1440.json`. Exit shares partition the measured child population (exits + censored at horizon); **combo 0**: started-liquidity 0.4393, started-choice 0.1729, q1 liquidity 0.6850 (the broken driver produced universal 0/0/0). |
| `engine-fixed-40seeds/` | bonus 40-seed grid (5,760 runs) + summary/decomp/logs; raw rows gzipped | same fixed driver | 213.9 s at 12 workers; exit shares partition 1.0, censored present. Byte-identical rows to a concurrent duplicate run (sha `fee303cf`), an independent determinism cross-check. |
| `phase-sweep-quick/` | `phase_sweep_quick_summary.csv` / `.json`, runner, log | `phase_sweep_quick.py` against the same fixed engine | pre-registered in `research/phase-transition-2026-11-25` (`PREREGISTRATION_PHASE_SWEEP.md`, commit `408aa3e`, committed **before** this run). 10 × 10 axes × 5 seeds = 500 runs, 57.3 s at 8 workers, gate = `bar`, 100 cells. This is the quick-mode "step 1" phase diagram only; boundary statistics are computed host-side from the CSV, not here. |
| `dhs-patched-verify/` | `VERIFICATION.json` (PASS_BYTE_IDENTICAL), `m4_surveytype_check.json` | `dhs_patched_rerun.sh` (staged Neon `ir_pipeline.py` post-image + `estimate.py`/`corrected_reduction.py` @`45b974e`) | 4/4 script hashes, IR `--selftest` 51 rows + OK, **13/13 output files byte-identical** to the committed corrected run, 27/27 numeric anchors (full precision), M4 pre-registered `SurveyType == "DHS"` check passed (76 non-DHS cells excluded; DHS-only M1: −0.5537 / −1.5749 / −2.5241 vs pooled −0.5541 / −1.5837 / −2.5382). IR individual-level estimation **NOT FEASIBLE** on this instance (0/72 microdata files present) — recorded as such, nothing fabricated. |
| `phase-sweep-dense-bar/` | dense bar-gate sweep: 10 × 10 × **20 seeds = 2,000 runs**, 132.6 s at 10 workers | same pre-registered runner/axes | higher-seed-density version of the quick grid; gate contrast uses this + the quota arm. |
| `phase-sweep-quota/` | same runner, gate = `quota` second pass (10 × 10 × 5 = 500 runs) | same | completed 00:59 CST; same pre-registration (gate contrast C uses both `bar` and `quota` arms). |
| `locks/` | `pip_freeze_autodl3.txt`, `input_sha256.txt`, `env_summary.txt` | `pip freeze` + `sha256sum` on the box | replication lockfile for the instance (128 packages, 40 input files, host/python/numpy/kernel/cgroup summary). |

## Reproduce

The engine and scripts are on the branches named above; the box paths recorded in the JSONs
(`engine_root`, `source`, `driver_sha256`) identify exactly which code produced each file. The DHS
re-run is byte-identical to the committed corrected run, so it reproduces `research/dhs-corrected-2026-11-25`
@`d9c5139` rather than adding a new result.

## What this does NOT establish

- These are **simulation** outputs (eduengine toy worlds) except the DHS estimates, which are
  observationally corrected reductions of committed DHS panels.
- The phase sweep is quick-mode only; no boundary statistic or verdict is claimed here.
- The DHS IR (individual-level) leg was never estimated — no microdata on the instance.
- No causal language applies to any file here.
