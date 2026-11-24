# Phase-diagram boundary + equifinality (SIMULATION ONLY)

cells: bar 100 (20 seeds), quota 100 (5 seeds)

## Sharpest adjacent-cell jump along the fee (liquidity) axis, per response
- **bar / tut_q5_q1_gap**: J_max = -0.0101 at x=7.0 (0.08->0.10), sharpness = 0.03
- **quota / tut_q5_q1_gap**: J_max = -0.0422 at x=9.0 (0.06->0.08), sharpness = 0.10
- **bar / liq_share**: J_max = -0.0153 at x=7.0 (0.16->0.18), sharpness = 0.15
- **quota / liq_share**: J_max = -0.0123 at x=8.0 (0.06->0.08), sharpness = 0.11
- **bar / gate_fail_share**: J_max = -0.0012 at x=0.0 (0.10->0.12), sharpness = 0.29
- **quota / gate_fail_share**: J_max = +0.0057 at x=8.0 (0.02->0.04), sharpness = 0.08
- **bar / tut_rate**: J_max = +0.0032 at x=2.0 (0.12->0.14), sharpness = 0.01
- **quota / tut_rate**: J_max = +0.0107 at x=3.0 (0.10->0.12), sharpness = 0.02
- **bar / completion_lower**: J_max = -0.0156 at x=1.0 (0.16->0.18), sharpness = 0.02
- **quota / completion_lower**: J_max = -0.0013 at x=3.0 (0.16->0.18), sharpness = 0.00
- **bar / completion_lower_q_gap**: J_max = +0.0199 at x=9.0 (0.08->0.10), sharpness = 0.02
- **quota / completion_lower_q_gap**: J_max = +0.0425 at x=6.0 (0.00->0.02), sharpness = 0.05

## Gate contrast (same cell, bar vs quota)
- tut_q5_q1_gap: median |diff| = 0.0919, max |diff| = 0.1759 over 100 cells
- liq_share: median |diff| = 0.0117, max |diff| = 0.1453 over 100 cells
- gate_fail_share: median |diff| = 0.0644, max |diff| = 0.0824 over 100 cells

## Equifinal pairs (same completion level, different liquidity/tutoring)
- total pairs meeting thresholds: **20**
- completion_lower within 0.14 pp but Δliq 12.45 pp / Δtut 20.54 pp: (x0.0,y9.0) vs (x9.0,y5.0)
- completion_lower within 0.135 pp but Δliq 11.3 pp / Δtut 21.62 pp: (x0.0,y9.0) vs (x9.0,y8.0)
- completion_lower within 0.14 pp but Δliq 12.41 pp / Δtut 20.33 pp: (x0.0,y9.0) vs (x9.0,y6.0)
- completion_lower within 0.13 pp but Δliq 11.62 pp / Δtut 20.97 pp: (x0.0,y9.0) vs (x9.0,y7.0)
- completion_lower within 0.06 pp but Δliq 10.97 pp / Δtut 21.47 pp: (x0.0,y9.0) vs (x9.0,y9.0)
