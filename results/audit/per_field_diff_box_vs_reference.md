# Per-field difference report — box (numpy 1.24.1) reproduction vs supplied reference

- file A: `/Users/treymenefee/neon-boot/wt4/repro/papers/shadow-education-contest/code/results/reference/hk_korea_comparative_with_cf4_bundle_reference.json`
- file B: `/tmp/gate0_box/box8w_output.json`

## Totals

- numeric values compared: **10566**
- exactly equal: **10535**
- differing: **31**
- non-numeric differing (incl. metadata): **1**
- all summary `total_spend_index` equal at 2 d.p.: **True**

- NONNUMERIC_DIFF `metadata.elapsed_seconds`: `165.47` != `71.85`

## Summary-level reported figures (all 18 arms x 2 jurisdictions x 8 statistics)

- summary numeric values: **846**; equal at 2 d.p.: **846**; differing at 2 d.p.: **0**

## Largest per-field differences (grouped; full detail in the CSV)

| group | n | differing | max abs | max rel | max-abs location |
|---|---|---|---|---|---|
| `seeds[].q5_q1_spend_ratio` | 540 | 8 | 7.105e-15 | 3.961e-16 | `seeds[365].q5_q1_spend_ratio` |
| `summary[jur][arm].delta_vs_baseline.q5_q1_spend_ratio.ci95_hi` | 18 | 4 | 1.776e-15 | 4.869e-16 | `summary.KR.CF1a.delta_vs_baseline.q5_q1_spend_ratio.ci95_hi` |
| `summary[jur][arm].delta_vs_baseline.q5_q1_spend_ratio.ci95_lo` | 18 | 4 | 8.882e-16 | 4.027e-16 | `summary.KR.CF1a.delta_vs_baseline.q5_q1_spend_ratio.ci95_lo` |
| `summary[jur][arm].delta_vs_baseline.q5_q1_spend_ratio.mean` | 18 | 3 | 8.882e-16 | 4.971e-16 | `summary.KR.CF1a.delta_vs_baseline.q5_q1_spend_ratio.mean` |
| `summary[jur][arm].delta_vs_baseline.q5_q1_spend_ratio.sd` | 18 | 3 | 4.441e-16 | 2.690e-16 | `summary.KR.CF4b.delta_vs_baseline.q5_q1_spend_ratio.sd` |
| `summary[jur][arm].q5_q1_spend_ratio.sd` | 18 | 1 | 4.441e-16 | 2.105e-16 | `summary.HK.CF2a.q5_q1_spend_ratio.sd` |
| `seeds[].k12_spend_by_q[0]` | 540 | 8 | 1.388e-17 | 3.842e-16 | `seeds[365].k12_spend_by_q[0]` |
| `metadata.base_commit` | 0 | 0 | 0.000e+00 | 0.000e+00 | `` |

Full per-field table: `/Users/treymenefee/neon-boot/wt4/auditv2/results/audit/per_field_diff_box_vs_reference.csv`
