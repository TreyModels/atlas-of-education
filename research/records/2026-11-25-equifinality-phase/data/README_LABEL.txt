SIMULATION ONLY - eduengine toy worlds; illustrative parameters; no causal/empirical claims.

Label sidecar for CSV artefacts in this directory (CSV files are headerless of metadata; the label is
recorded here, in every JSON metadata block in this directory, and in ../REPORT.md and
../PRE_REGISTRATION.md).

Files:
  phase_sweep_full_runs.csv         16,000 seed-level rows (20 X x 20 Y x 2 gates x 20 seeds); ok/error columns;
                                    exit shares partition to 1.0; GER_sim = 1 - never_share (declared simulated
                                    participation, not an empirical GER).
  phase_sweep_full_summary.csv      800 per-cell seed means + SDs + gate-binding diagnostics.
  phase_sweep_full_summary.json     same, with design, engine/code sha256 hashes, host, timing, label.
  equifinality_pairs.csv            every qualifying pair (176 within-gate primary + 4,132 cross-gate secondary).
  equifinality_top50.csv            top 50 within-gate pairs by |dliq|+|dtut| (pp).
  equifinality_top50_crossgate.csv  top 50 cross-gate pairs (secondary, descriptive).
  equifinality_completion_lower_pairs.csv   secondary pairing (0 rows).
  repro_subset_runs.csv             360-run determinism re-run (18 cells x 2 gates x 20 seeds).
  repro_subset_summary.json         its per-cell summary.
No causal or empirical claim is made anywhere in these files.
