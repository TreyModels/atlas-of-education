# Corrected run — 25 Nov 2026 (Neon audit item 1: cluster-bootstrap multiplicities)

**Status: PROVISIONAL.** These numbers come from the in-flight fix applied on the server, **not** from Neon's
drop-in diff. They are recorded now so nothing is lost if the instance is powered off. Do **not** update the
dashboard / handoff D3–D4 text from this file until Neon's patch is applied and reproduces them.

**Branch:** `research/dhs-corrected-2026-11-25` (additive, cut from `fe762b9`). Nothing pushed yet.

## What changed

Neon's line audit found that `_boot_task()` in `scripts/estimate.py` (and `ratio_boot()` in
`scripts/corrected_reduction.py`) did `r["country"] in samp`, which keeps each resampled country **at most once**.
That is a subsampling bootstrap, not a country-cluster bootstrap: ~36.8 % of resampled slots were dropped and the
intervals came out too narrow. Fix: draw multiplicities (`collections.Counter`) and replicate each resampled
country's cells `count` times — frequency weighting, exactly equivalent to `weight = count`.

The separate fixed-effect bug (dropped reference level with no intercept, −0.01 to −0.02 children bias) was
already fixed in `d63754f` and is unchanged here; both `estimate.py` and the independent
`corrected_reduction.py` still carry it.

## Run

- Box: `autodl-container-a8f742b5ee-292349c5` (`connect.cqa1.seetacloud.com:45973`), 8 workers, numpy 1.24.1.
- Driver: `/root/work/run_neon_fix.sh`; log + wall clock preserved in
  `results/server_box3_corrected/{run.log,stats.txt}`. Wall time **211 s**.
- Inputs unchanged: `sha256sum -c data/MANIFEST.sha256` → 28/28 OK on the box.
- JOB A full sample (`estimate.py --outdir results`), JOB B Africa-11 (`--countries ... --outdir results/africa11`),
  JOB C independent cross-check (`corrected_reduction.py`). All exit 0.

## Headline numbers after the fix

Full sample (88 countries / 369 surveys, weighted M1, 4-level): primary **−0.554**, secondary **−1.584**,
higher **−2.538** children (SE 0.0588 / 0.1667 / 0.2419); 2-group **−1.5514** (0.1452).
Point estimates essentially unchanged versus `d63754f` — the fix moves **intervals and D4**, not the gradient.

| quantity | before (d63754f) | after (this run) | verdict effect |
|---|---|---|---|
| Q2a ratio, 2-group (full, G=80) | 0.958 [0.914, 1.002] | **0.958 [0.906, 1.019]** | stays includes-1.0 |
| Q2a ratio, 4-level (full, G=65) | 1.003 [0.932, 1.077] | **1.003 [0.921, 1.095]** | stays includes-1.0 |
| Q2b1 C_vs_B (wanted vs actual TFR, SD) | −0.0775 (0.0217) | **−0.1962 (0.0495)** | **D4 secondary gap re-read: ≈ −0.196, not −0.078** |
| Q2b1 A_vs_B | 0.0158 (0.0411) | **0.0711 (0.0757)** | smaller claim, wider CI |
| Africa-11 ratio, 2-group | 1.070 [1.011, 1.135] | **1.0698 [0.9987, 1.1403]** | **now includes 1.0 — verdict flips to indeterminate** |
| Africa-11 ratio, 4-level | 1.178 [1.027, 1.356] | **1.1780 [1.0042, 1.3877]** | stays below 1.0 |

This matches the handoff's predicted corrected values (`D4 secondary gap ≈ −0.1962`; Africa-11 ≈
`[0.9987, 1.1323]`; full 2-group `[0.9084, 1.0164]`) to within Monte-Carlo noise, i.e. Neon's diagnosis was right.

## Independent verification (host-side, no server needed)

`scripts/corrected_reduction.py` was re-run on the Mac against the committed panels (`data/`, 13 MB) with the
fixed script: it reproduces every number above to ~1e-12 (Africa-11 2-group ratio `1.069843350505824`,
CI `[0.9987338159871082, 1.1403490938072518]`; A_vs_B `−0.19669737936298431`; C_vs_B `−0.0031318298867118`),
and its built-in validation gate against the prior record passes (`max_abs_delta = 0.0036`). So the fix is
reproducible off the server; only the 500-draw bootstrap is slow there, not compute-bound.

Minor: `estimate.py`'s own bootstrap and `corrected_reduction.py`'s differ in the last digits of the CI
(2-group full [`0.9056, 1.0144`] vs [`0.9060, 1.0191`]) — different RNG streams/implementations, both include 1.0.

## Open (for Neon / next window)

- Apply Neon's actual drop-in diffs; if they differ from this implementation, re-run and reconcile.
- `stacked()` higher×cohort interaction (+0.1804, p=0.030) and pri/hi interactions from the handoff item 1 were
  **not** added here — this run keeps the committed interaction set. `ir_pipeline.py` blockers (v190, region×round,
  CMC, weights, survey_type, MIS/AIS, clustering) are untouched.
- Only after that: update dashboard / handoff D3–D4 text.
