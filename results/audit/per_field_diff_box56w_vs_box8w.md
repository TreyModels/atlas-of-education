# Per-field difference report — box 56-worker variant vs box unmodified 8-worker run

- file A: `/tmp/gate0_box/box8w_output.json`
- file B: `/tmp/gate0_box/box56w_output.json`

## Totals

- numeric values compared: **10566**
- exactly equal: **10566**
- differing: **0**
- non-numeric differing (incl. metadata): **1**
- all summary `total_spend_index` equal at 2 d.p.: **True**

- NONNUMERIC_DIFF `metadata.elapsed_seconds`: `71.85` != `99.63`

## Summary-level reported figures (all 18 arms x 2 jurisdictions x 8 statistics)

- summary numeric values: **846**; equal at 2 d.p.: **846**; differing at 2 d.p.: **0**

## Largest per-field differences (grouped; full detail in the CSV)

| group | n | differing | max abs | max rel | max-abs location |
|---|---|---|---|---|---|
| `metadata.base_commit` | 0 | 0 | 0.000e+00 | 0.000e+00 | `` |
| `metadata.branch` | 0 | 0 | 0.000e+00 | 0.000e+00 | `` |
| `metadata.elapsed_seconds` | 0 | 0 | 0.000e+00 | 0.000e+00 | `` |
| `metadata.history_api` | 0 | 0 | 0.000e+00 | 0.000e+00 | `` |
| `metadata.n_arms` | 0 | 0 | 0.000e+00 | 0.000e+00 | `` |
| `metadata.n_seeds` | 0 | 0 | 0.000e+00 | 0.000e+00 | `` |
| `metadata.repo` | 0 | 0 | 0.000e+00 | 0.000e+00 | `` |
| `metadata.total_runs` | 0 | 0 | 0.000e+00 | 0.000e+00 | `` |

Full per-field table: `/Users/treymenefee/neon-boot/wt4/auditv2/results/audit/per_field_diff_box56w_vs_box8w.csv`
