# PRE-REGISTRATION — dense phase-diagram grid (20 x 20 x 2 gates x 20 seeds)

Written and committed BEFORE any dense run. Base commit of the quick grid: `research/phase-transition-2026-11-25`
@ `2e58d64` (pre-registration `408aa3e`, quick grid 10x10x5). This document is the resolution scale-up.

## Why this run exists
The pre-registered quick grid (10x10, 5 seeds = 500 runs/gate) returned an **ABSENT/PARTIAL** boundary verdict:
max adjacent-cell jump in `tut_q5_q1_gap` / `liq_share` / `gate_fail_share` along the fee axis had
`sharpness` 0.01–0.29 against the pre-declared threshold `sharpness >= 2` (boundary/equifinality statistics,
`research/box-runs-2026-11-25` @ `75968e6`). Two explanations remain: (i) the mechanism has no sharp
boundary in this parameter range; (ii) the 10x10 grid is too coarse to resolve it. This run discriminates
between them at 4x the cell density. **It is a resolution test, not a re-test after seeing a positive.**

## Design (fixed, no post-hoc changes)
- X = `vac0` (formal vacancies per cohort entrant), 20 levels, geometric from 0.02 to 0.50:
  `0.02, 0.02369, 0.02807, 0.03325, 0.03939, 0.04666, 0.05527, 0.06547, 0.07756, 0.09188, 0.10884,
  0.12893, 0.15274, 0.18093, 0.21433, 0.25390, 0.30078, 0.35630, 0.42208, 0.50000`
- Y = `fee_primary` (primary fee as share of median income; 0.0 = E8 abolition slice), 20 levels,
  linear 0.00–0.19 in steps of 0.01.
- Gates: `bar` and `quota` exactly as in `phase_sweep_quick.py::GATES` (unchanged).
- Seeds: 0..19 per cell (20 seeds).
- Cells per gate: 400; runs per gate 8,000; total 16,000.
- Runner: `phase_sweep_quick.py` (unmodified except `--x-levels/--y-levels/--seeds`), engine
  `/root/work/edsystem/engine`, workers 10, `--n 400 --t 70 --measure-from 35`.
- Determinism: seeds fixed; outputs deterministic (a duplicate grid previously reproduced byte-identical rows).

## Statistics (identical definitions and thresholds as `408aa3e`)
- `J_max` / `sharpness`: sharpest adjacent-cell jump along the fee axis within each vacancy level,
  normalised by the median absolute level of the response; responses: `tut_q5_q1_gap`, `liq_share`,
  `gate_fail_share`, `tut_rate`, `completion_lower`, `completion_lower_q_gap`.
- Gate contrast `C`: same (x,y) cell, bar vs quota; median and max absolute difference.
- Equifinal pairs: |Δ`completion_lower`| < 0.5 pp AND (|Δ`liq_share`| > 25 pp OR |Δ`tut_rate`| > 20 pp),
  searched within each gate's grid.

## Decision rule (fixed before the run)
- **SIGNATURE** if any sharpness >= 2 in `tut_q5_q1_gap` or `gate_fail_share` AND its location is
  interior (not at the fee=0 or fee=max edge) AND the gate contrast median |Δtut gap| > 0.05.
- **PARTIAL** if sharpness in [1, 2) for those responses, or the sharpest jump sits on an edge.
- **ABSENT** if no response reaches sharpness >= 1 anywhere.
- Equifinal pairs are reported regardless (count + top pairs); the auditor's thresholds are not
  re-tuned after seeing results.
- Any verdict is **SIMULATION ONLY**, no causal language. A negative result is reported as the result.

## Cost / stop rule
~9-10 min per gate at observed throughput (2,000 runs / 133 s at 10 workers). If the first gate exceeds
25 min or errors appear, stop, keep the partial output, and report the failure rather than re-running.
