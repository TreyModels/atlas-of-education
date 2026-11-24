# AMENDMENT 01 — statistic definition for the dense grid (declared BEFORE analysis)

**Written and committed before any dense number is read.** The bar arm has been running since
`2026-11-25T01:13:48Z`; no dense output has been analysed at the time of this commit.

## Correction
The statistics section of `PREREGISTRATION_PHASE_SWEEP_DENSE.md` described `J_max` / `sharpness` in the
Lead's preliminary **fee-axis, level-normalised** form (`|Δ response| / median(level)`), with the ≥2
threshold. That is **not** the statistic pre-registered in `408aa3e`, and it is a known-bad metric:
phase-sweep's reconciliation (`research/phase-transition-2026-11-25` @ `6ba9f95`) showed it yields
0.01–0.29 on both quick grids (≥2 effectively unreachable), and it is blind to the vacancy axis where the
only surviving candidate lives. Carrying it into the dense grid would manufacture an "ABSENT" artefact.

## Declared statistic for the dense analysis (identical to `408aa3e`)
For every adjacent cell pair along **both** axes:
`J(pair) = |Δ response| / median(seed SD of the two cells)`
`J_max = max J`; `J_edge = median J over grid-boundary pairs`; `sharpness = J_max / J_edge`.
Thresholds unchanged: **SIGNATURE** requires `sharpness >= 2` AND `J_max >= 4` AND an interior location
AND gate contrast `C = median |Δ tut_q5_q1_gap| (bar vs quota) > 0.05`; **PARTIAL** if `sharpness >= 1`
or `J_max >= 2`; otherwise **ABSENT**. Responses: `tut_q5_q1_gap`, `gate_fail_share`, `liq_share`,
`tut_rate`, `completion_lower`, `completion_lower_q_gap`. Equifinal pair thresholds unchanged.

This is a **declared deviation** (metric corrected to the pre-registered definition), not a post-hoc
choice: it is committed before the dense statistics are computed, and it makes the test stricter on the
fee axis and non-blind on the vacancy axis. Implementation: `dense_boundary.py` (committed with the
analysis outputs). Simulation only; no causal language.
