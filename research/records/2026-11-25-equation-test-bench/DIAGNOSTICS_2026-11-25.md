# Diagnostics — 25 Nov 2026 (session retirement record)

## F9 join coverage (`long_run_panel.csv`, 42,959 rows, 197 countries, years 1750–2024)
| column | non-missing rows |
|---|---|
| mean_years_schooling | 3,447 |
| tfr_observed_1950plus | 14,578 |
| effective_fertility | 15,837 |
| urban_share_pct | 14,775 |
| gdp_pc_maddison_1990int | 17,180 |
| all five | 1,630 |
| tfr + schooling | **1,703** |
| tfr + schooling + urban | 1,703 |
| tfr + schooling + GDP | 1,630 |

**Implication:** a lagged Δschooling→ΔTFR sample is **not empty** (≈1.6–1.7k rows in the cross-section); the `n=0`
in `test_bench2.py` is therefore an implementation/join bug (lag+control requirements and/or column handling), not a
data absence. The fix before any verdict: build the lagged panel, trim to the ≤1,630 overlapping rows, report n per
country/fold and coverage, use `pinv` + rank guards, drop collinear controls instead of failing.

## E8 / PHL panel availability (repo search, no pulls)
- `origin/research/e6e8-sequencing-2026-11-25`: `research/records/2026-11-25-e6e8-sequencing/data/fee_dates.csv`,
  `results/e6_classification.csv`, `results/e6_summary.csv`, `results/e6_inputs_and_hashes.csv`, `ERRATUM.md`.
- `origin/research/paper-massification-2026-11-25`: `research/records/2026-11-25-paper-massification/data/fee_dates.csv`,
  `data/e8_results.json`, `data/event_dates_subsistence_v2.csv`.
- **PHL 2013 K–12 series not located** in the searched branches — must be explicitly marked UNTESTABLE unless found
  elsewhere; the E8 fee-date files exist and can be copied with provenance for a benchmark gate.

## Status at retirement
Last committed head (before this diagnostics file): `ab8ca9d` on `research/equation-test-bench-2026-11-25`.
No new runs started after the last instruction; region-42 up, not shut down.
