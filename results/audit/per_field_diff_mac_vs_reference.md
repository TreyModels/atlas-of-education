# Per-field difference report — host Mac reproduction vs supplied reference

- file A: `/Users/treymenefee/neon-boot/wt4/repro/papers/shadow-education-contest/code/results/reference/hk_korea_comparative_with_cf4_bundle_reference.json`
- file B: `/Users/treymenefee/neon-boot/wt4/repro/papers/shadow-education-contest/code/hk_korea_comparative_with_cf4.json`

## Totals

- numeric values compared: **10566**
- exactly equal: **10556**
- differing: **10**
- non-numeric differing (incl. metadata): **1**
- all summary `total_spend_index` equal at 2 d.p.: **True**

- NONNUMERIC_DIFF `metadata.elapsed_seconds`: `165.47` != `118.36`

## Summary-level reported figures (all 18 arms x 2 jurisdictions x 8 statistics)

- summary numeric values: **846**; equal at 2 d.p.: **846**; differing at 2 d.p.: **0**

## Largest per-field differences (grouped; full detail in the CSV)

| group | n | differing | max abs | max rel | max-abs location |
|---|---|---|---|---|---|
| `seeds[].q5_q1_spend_ratio` | 540 | 3 | 3.553e-15 | 2.094e-16 | `seeds[130].q5_q1_spend_ratio` |
| `summary[jur][arm].delta_vs_baseline.q5_q1_spend_ratio.ci95_lo` | 18 | 1 | 4.441e-16 | 2.014e-16 | `summary.KR.CF2a.delta_vs_baseline.q5_q1_spend_ratio.ci95_lo` |
| `summary[jur][arm].delta_vs_baseline.q5_q1_spend_ratio.mean` | 18 | 1 | 4.441e-16 | 2.486e-16 | `summary.KR.CF2a.delta_vs_baseline.q5_q1_spend_ratio.mean` |
| `summary[jur][arm].delta_vs_baseline.q5_q1_spend_ratio.ci95_hi` | 18 | 1 | 2.220e-16 | 1.623e-16 | `summary.KR.CF2a.delta_vs_baseline.q5_q1_spend_ratio.ci95_hi` |
| `summary[jur][arm].delta_vs_baseline.q5_q1_spend_ratio.sd` | 18 | 1 | 2.220e-16 | 1.898e-16 | `summary.KR.CF2a.delta_vs_baseline.q5_q1_spend_ratio.sd` |
| `seeds[].k12_spend_by_q[0]` | 540 | 3 | 6.939e-18 | 1.810e-16 | `seeds[130].k12_spend_by_q[0]` |
| `metadata.base_commit` | 0 | 0 | 0.000e+00 | 0.000e+00 | `` |
| `metadata.branch` | 0 | 0 | 0.000e+00 | 0.000e+00 | `` |

Full per-field table: `/Users/treymenefee/neon-boot/wt4/auditv2/results/audit/per_field_diff_mac_vs_reference.csv`
