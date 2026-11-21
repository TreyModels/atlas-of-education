# CAP-04 — survival floor 0.02: DISCLOSED DEFECT + one cheap sensitivity (DEBUG)

**LABEL: `DEBUG`.** Ruling applied (Lead, 2026-11-21): **do not retro-fix any delivered panel.** CAP-04 is
recorded as a **disclosed defect** — an **undeclared** survival floor (`clip(..., 0.02, 0.995)` at
`generator_v1_3/code/sim_v1_3.py:826`) that **binds in 24 tertiary cells (1970–72, 20 countries)** and changes
`completion_cohort` and every downstream level number, identical on all three frozen panels. It is **not** the
named defect of this debug run and is **not** fixed in any delivered artifact.

## The one cheap sensitivity (copies only)

Two copies of the v1.3 generator, both carrying the CAP-01 one-sided-floor fix, differ **only** in the survival
clamp floor: **0.02** (as delivered) vs **0.00** (sensitivity). Same seed (20261120), draw order, inputs, shadow
settings; each panel written once; `results/RUNS.json` records both.

| 2024 endpoint (`completion_uis`, pp) | as delivered (floor 0.02, cap 1.0) | floor 0.02 copy (CAP-01 fixed) | floor 0.00 copy | **CAP-04 delta** | max abs(delta) across 30 countries |
|---|---:|---:|---:|---:|---:|
| primary | 100.000000 | 100.787281 | 100.787281 | **+0.000000** | 0.000000 |
| lower_secondary | 85.874640 | 85.874640 | 85.874640 | **+0.000000** | 0.000000 |
| upper_secondary | 76.639081 | 76.639081 | 76.639081 | **+0.000000** | 0.000000 |
| tertiary | 37.378691 | 37.378691 | 37.378688 | **−0.000003** | 0.000228 |

- **Max |CAP-04 delta| at 2024 across all 30 countries × 4 levels: 0.000228 pp** — far below the 0.01 pp bar.
- **Cells differing by > 0.01 pp in 2024: 0.**
- The primary 100.000 → 100.787 difference between the as-delivered column and the copies is the **CAP-01 fix**
  (D173), not CAP-04; it is disclosed there as a prospective amendment and the delivered panel is untouched.

## Ruling applied

**CAP-04 = burn-in dissipated by 2024.** No published 2024 endpoint would move by more than 0.01 pp if the
undeclared floor were removed. The defect stands recorded (not fixed) as an **undeclared convention** in the debug
record; it affects 1970–72 tertiary burn-in cells only, with no material 2024 consequence on any endpoint checked.
The delivered panels and the gate-passed write-up are **untouched**.
