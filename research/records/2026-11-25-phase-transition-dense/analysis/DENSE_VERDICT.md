# Dense-grid boundary + equifinality, pre-registered metric (SIMULATION ONLY)

cells: bar 400, quota 400; J=|d|/median(seed SD), both axes; sharpness=J_max/median(J_edge); edge=varying coord at boundary

## Verdict
- **bar / tut_q5_q1_gap**: **PARTIAL** — J_max 2.881 (interior 2.251) at X axis 18.0→19.0 (edge); sharpness 11.475
- **bar / gate_fail_share**: **PARTIAL** — J_max 2.865 (interior 2.865) at X axis 12.0→13.0 (interior); sharpness 5.274
- **quota / tut_q5_q1_gap**: **SIGNATURE** — J_max 11.5 (interior 11.5) at X axis 16.0→17.0 (interior); sharpness 18.167
- **quota / gate_fail_share**: **SIGNATURE** — J_max 12.582 (interior 12.582) at X axis 17.0→18.0 (interior); sharpness 23.483

- gate contrast (bar vs quota) median |Δtut Q5−Q1 gap| = 0.0741 (SIGNATURE needs > 0.05)

## J_max by axis (interior only)
- bar:tut_q5_q1_gap: X interior 2.2505144222411384, Y interior 1.6336149667097555, global 2.88 (edge)
- bar:gate_fail_share: X interior 2.8649014343979013, Y interior 1.2906046208160165, global 2.86 (interior)
- bar:liq_share: X interior 14.266344718575686, Y interior 2.763349526657905, global 21.15 (edge)
- bar:tut_rate: X interior 4.373124370150278, Y interior 1.7345971858112237, global 4.37 (interior)
- bar:completion_lower_q_gap: X interior 2.2611620365762817, Y interior 1.6710851095651578, global 2.26 (interior)
- quota:tut_q5_q1_gap: X interior 11.499916519348753, Y interior 1.8897250695104533, global 11.50 (interior)
- quota:gate_fail_share: X interior 12.582423893993663, Y interior 1.4813992100381335, global 12.58 (interior)
- quota:liq_share: X interior 11.909549656235969, Y interior 3.3394163216009187, global 11.91 (interior)
- quota:tut_rate: X interior 24.706764161906722, Y interior 1.5255088430745893, global 24.71 (interior)
- quota:completion_lower_q_gap: X interior 2.0340251848804836, Y interior 1.468652175301301, global 2.03 (interior)

## Equifinal pairs: **374**
- (0.0,19.0) vs (17.0,0.0): Δcompletion 0.258 pp, Δliq 15.45 pp, Δtut 20.86 pp
- (0.0,19.0) vs (17.0,2.0): Δcompletion 0.256 pp, Δliq 15.52 pp, Δtut 20.78 pp
- (0.0,19.0) vs (17.0,1.0): Δcompletion 0.259 pp, Δliq 15.43 pp, Δtut 20.79 pp
- (0.0,19.0) vs (17.0,3.0): Δcompletion 0.264 pp, Δliq 15.41 pp, Δtut 20.79 pp
- (0.0,19.0) vs (17.0,4.0): Δcompletion 0.243 pp, Δliq 15.12 pp, Δtut 20.8 pp
- (1.0,19.0) vs (17.0,0.0): Δcompletion 0.238 pp, Δliq 15.35 pp, Δtut 20.47 pp
