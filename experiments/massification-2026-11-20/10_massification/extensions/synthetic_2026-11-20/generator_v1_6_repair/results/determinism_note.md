# Determinism

Two complete runs: `results/` and `results/determinism_run2/`.
Seed 20261120, one PCG64 stream, the frozen v1.2 draw order; the V16 blocks draw nothing.
Floats written at `%.10g`; no wall-clock, hostname, PID or iteration order enters any output.

| status | files compared | byte-identical |
|---|---:|---:|
| DETERMINISM-PASS | 17 | 17 |

Compared file list:

- `child_wage_A10.csv` — identical
- `crossing_check.csv` — identical
- `decomposition.csv` — identical
- `kappa_object_audit.csv` — identical
- `lower_channel_report.csv` — identical
- `observed_path.csv` — identical
- `panel_A00CF_identity.csv` — identical
- `panel_A00_v13cols.csv` — identical
- `panel_A01D_kappa.csv` — identical
- `panel_A10W_childwage.csv` — identical
- `panel_A10_repaired.csv` — identical
- `phys_cap_sensitivity.csv` — identical
- `propagation_ledger.csv` — identical
- `representation_cells.csv` — identical
- `sensitivity_arms.csv` — identical
- `v1_6_checks.csv` — identical
- `v1_6_checks_detail.csv` — identical
