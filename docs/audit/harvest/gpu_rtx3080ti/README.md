# GPU RTX 3080 Ti — harvested legacy outputs (PRE-REPAIR / AUTHOR-REPORTED / UNRESOLVED)

**Status: NOT Gate-1 evidence. Do not cite as a repair, a calibration, or an E1/Q3 reconstruction.**
Harvested read-only from the old-window lane `gpu-rtx3080ti` (branch `research/gpu-rtx3080ti-2026-11-25` @
`9f7dfa9`, pushed; box dir `/root/work/gpu`, never written by us). The lane handed over and stopped; the binaries
here are byte-identical to that branch record (verified by sha256; see `../HARVEST_MANIFEST.csv`).

## What ran

| job | output | labels that MUST accompany any use |
|---|---|---|
| Job 2 — 7-parameter ABC (200,000 draws) | `bray_and_contest/bray_abc_and_contest_surface.json` — accept 92/200,000 (0.046 %), best `max_z` 0.455 | **NOT a 7-parameter calibration**: `theta[:,5]` (`teacher_threshold`) never enters utilities or moments, so it is unidentified. Review §5 confirmed. |
| Job 2b — 6-parameter corrective ABC (200,000 draws) | `bray_and_contest_6param/bray_abc_and_contest_surface.json` — accept 77/200,000 (0.0385 %), best `max_z` 0.4075, `dropped_param = teacher_threshold` | Corrective rerun that drops the dead parameter; still a sensitivity/self-test, not an empirical estimate. |
| Job 2 — contest sensitivity surface (2,000 points) | inside both JSONs — paradox shares 1.0 / 1.0, mean participation jump 0.3709 | **APPROXIMATE** fixed-point best-response exercise, not a boundary map of the engine's realized contest mechanism. Review §5. |
| Job 1 — E1/Q3 wild-cluster selftest (GPU + CPU-forced reference) | `e1_q3_selftest/wild_cluster_ri_results.json`, `e1_q3_selftest_cpu_ref/wild_cluster_ri_results.json`, `branch/results/gpu_vs_cpu_diff.json` | **GPU-numerics validation only**, NOT an E1/Q3 robustness check: **panel mode was NOT RUN — the panel CSV is MISSING**. As shipped, panel mode builds `X=[1,x]`, dropping controls/fixed effects (review §5). |
| Environment | `branch/env_lock_rtx3080ti.txt`, `branch/RUN_REPORT.md` | torch 2.7.1+cu118, CUDA available on RTX 3080 Ti (capability 8.6), py 3.10.8, numpy 1.24.1; recorded by the legacy lane, not re-verified by us in Gate 1. |

**GPU/CPU agreement (selftest only):** every deterministic quantity agrees to max abs diff **8.9e-15**; RNG-dependent
bootstrap percentiles differ because CUDA and CPU RNG streams differ for the same seed; p-values identical
(wild-cluster `p = 0.000499750` = 1/2001 floor; block-permutation `p = 0.000999` = 1/1001 floor).

## Why it is here and what it may be used for

* As **prior evidence for wave-2 GPU-estimator repair** (review §5): the correct labelling is already established —
  6-parameter corrective run, approximate contest surface, E1/Q3 reconstruction MISSING.
* As an **environment record** for the box GPU (torch cu118 installed and verified by the Lead; GPU stays parked in
  wave 1 — no GPU campaign is authorised here).
* It may **not** be cited as: a 7-parameter calibration, a contest-mechanism boundary map, an E1/Q3 reconstruction,
  or any Gate-1/Gate-2 evidence. No numbers from it enter the Gate-1 report.

## Provenance

* branch tip `9f7dfa9` ("GPU: RTX 3080 Ti run record (torch cu118, Job2 ABC/contest, Job1 E1/Q3 selftest)"),
  pushed to `origin/research/gpu-rtx3080ti-2026-11-25`; box artifacts `/root/work/gpu/results_rtx3080ti/**`
  pulled 2026-11-25 with `/tmp/box_pull.sh` (read-only) and matched to the branch JSONs by sha256.
* Full branch record (RUN_REPORT, MANIFEST, env lock, logs list) harvested under `branch/` for auditability.
