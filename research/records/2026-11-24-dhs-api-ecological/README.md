# DHS public-API ecological sprint — record (2026-11-24)

**Task:** task-16. **Branch:** `research/dhs-api-ecological-2026-11-24` (base
`origin/research/handoff-2026-11-24 @ 9242214`). **Status:** complete; results computed on region-42.

**One line:** using **all** DHS survey rounds the public API publishes with education breakdowns (369 surveys,
87 countries, 1985–2025), the schooling → completed-fertility gradient is **−1.57 children** (secondary vs none,
within survey), **98.8% of 346 surveys are negative**, it survives country FE, period FE and country trends,
it is **the same** for period TFR and cumulative completed fertility (standardised ratio 1.017 [0.944, 1.102]),
but the **wanted-fertility** gradient is materially weaker (−0.089 SD, p=0.00025) and the
**surviving-children** series is demonstrably different from TFR (corr 0.82; median gap 0.63 children). All
**OBSERVED / ECOLOGICAL**; no causal language; **not** a substitute for the blocked individual-level test.

| File | What it is |
|---|---|
| [`PRE_REGISTRATION.md`](PRE_REGISTRATION.md) | Fixed **before any value was pulled** (`88073d0`): scope, indicator set, panels, models M0–M5, contrasts, decision rules D1–D7, limits |
| [`AMENDMENT_01.md`](AMENDMENT_01.md) | Pre-estimation amendment (`856c421`): denominators absent for rate indicators; hidden second dimension in want-no-more; consistency-check method |
| [`REPORT.md`](REPORT.md) | Headline numbers, Q1 (gradient + heterogeneity), Q2a (window), Q2b (constructs), cohort proxy, D1–D7 scorecard, limits, reproduction |
| [`data/`](data/README.md) | Cached public-API JSON + panels + checks + `MANIFEST.sha256` (no microdata) |
| [`scripts/`](scripts) | `pull_dhs_api.py` (cache), `build_panel.py` (checks/panels), `estimate.py` (models; 48-worker pool on the box) |
| [`results/`](results) | `results.json`, model table, heterogeneity CSVs, survey-level construct table, server logs |

**Compute:** region-42 `/root/work/dhs-api/`, `/root/miniconda3/bin/python scripts/estimate.py`,
`DHS_WORKERS=48`, **13 s wall**, load average 10.5–11.8 sampled, system CPU 5–19% `us`; numpy 1.24.1 on the box
vs 1.24.3 local — coefficients identical to 4 dp. **Nothing is running on the Mac** (the local run was killed
per instruction and never resumed).
