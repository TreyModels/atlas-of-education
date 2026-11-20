# RESULTS_README — WT1–WT5 battery outputs

## Files in `results/`

| file | rows | content |
|---|---|---|
| `RESULTS.csv` | 7 | one row per test (WT1, WT2, WT3, WT4, WT5) plus two **HELD** rows that carry **no numbers** |
| `DETAIL.csv` | 996 | the per-series / per-country quantities that every statistic is built from |
| `run_info.json` | — | frozen thresholds, input+output sha256, verdict map, seed (`null`) — emitted by the run itself |

## `RESULTS.csv` columns

| column | meaning |
|---|---|
| `test_id` | `WT1`…`WT5`, plus `WT2.HELD-1`, `WT5.HELD-2` |
| `estimand` | the quantity the block asks for, in words |
| `statistic` | the number the verdict is read from (empty for HELD) |
| `threshold` | the predeclared bar, verbatim from the block (empty for HELD) |
| `verdict` | closed vocabulary: `SUPPORTED` / `NOT SUPPORTED` / `DATA LIMITED` / `DESIGN-ONLY` / `HELD` |
| `n` | independent units entering the statistic: series (WT1), countries (WT2, WT3), series (WT4), surveys (WT5) |
| `n_countries` | distinct countries in that statistic |
| `label` | `OBSERVED` (statistic read from the series), `DERIVED` (constructed statistic), `HELD` (no number) |
| `components` | **every** number the verdict depends on, including the **binding leg** that failed |
| `note` | reading / caveat / provenance for that row |
| `data_basis` | constant `OBSERVED-ONLY (no synthetic, no toy)` |

**All cells are reported, including nulls.** No HELD cell contains a number. No cell is imputed, interpolated,
back-cast or forecast.

## `DETAIL.csv` columns

`test_id, unit_id, iso3, indicator, metric, n_obs, year_range, value, label, note`

`unit_id` is `WDI:<iso3>:<indicator>`, `IN2:PHL:<indicator>`, `CTY:<iso3>`, `COMBO:<P>x<C>`, `HKG:<...>`,
`KOR:2023`, or `HELD:<iso3>`. Every metric is either an OBSERVED series value or a DERIVED construction, and
each `note` says which.

Selected metrics worth reading directly:

- **WT1** — `n_obs`, `rise_runs`, `fall_runs`, and one row per qualifying run (`rise_run`/`fall_run` with its
  year span and cumulative Δ). `excluded_n_lt_15` records every series the n≥15 rule kept out, including the
  three PHL detail series.
- **WT2** — `D_cred_pct_growth`, `D_dest_pp_change`, `decoupled_flag`, `reversal_flag` (with the peak, the
  trough and the run length in `note`), plus `D_cred_pp_change_DIAGNOSTIC` (M7 unit caveat; **not** used for the
  verdict).
- **WT3** — `P1_saturation_ceiling`, `P2_reversal_count_detrended` (+ raw sensitivity),
  `C1_median_eci`, `C2_median_formal_nonagric_share`, `income_log_gdp_pc_2015`, and the four
  `spearman_raw` / `spearman_partial_on_log_income` combinations.
- **WT4** — the eleven OBSERVED PHL upper-secondary values, the observed tertiary values, and one
  `below_threshold_block` row per below-threshold spell with its length, span, and recovery flag.
- **WT5** — the four gate-ratio readings (cross-year as the block states it, same-year 1996, same-year 2010,
  HKG 2003 stage gradient), the KOR 2023 participation/spend rows, and the five `HELD` systems.

## Reproduce

```bash
cd 10_massification/extensions/wt_2026-11-20
"<venv>/bin/python" code/run_wt.py                  # writes results/, overwriting
"<venv>/bin/python" code/run_wt.py --outdir _determinism/run_b
cmp results/RESULTS.csv _determinism/run_b/RESULTS.csv && \
cmp results/DETAIL.csv  _determinism/run_b/DETAIL.csv
"<venv>/bin/python" code/build_manifest.py          # rebuilds RUN_MANIFEST.json
```

No RNG, no bootstrap, no seed. Determinism is by construction (fixed sorts, `%.6f` formatting, no
dict-order dependence) and is **verified**: the two runs are byte-identical for all three output files.

## Reading discipline

- A `SUPPORTED` here means *the predeclared descriptive pattern is present on disk*. It is **not** validation of
  the hysteresis paper, not a causal finding, and not a model license.
- `NOT SUPPORTED` means a formed statistic missed the predeclared bar — **not** that the opposite mechanism is
  proven.
- `DATA LIMITED` is reserved for statistics that could not be formed at all.
- `DESIGN-ONLY` (WT5) means the row is a tabulation, deliberately **not scored**.
