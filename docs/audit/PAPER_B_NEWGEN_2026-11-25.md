# Paper B NEW GENERATION — final artefacts and result table (2026-11-25)

**Label: NEW GENERATION — REPRODUCED SIMULATION** (repaired engine, frozen V540-FREEZE spec). The Gemini-era 420/540
docx tables remain the **AUTHOR-REPORTED baseline**; this run is not a reproduction of them and no VALIDATED claim is
made. **Provenance note:** the campaign launched at 16:35 on the clean **`98baf6b`** engine (`core.py` `72cbddf7…`),
i.e. **before** the mid-run calendar-event fix (`846c9e0`, `core e111397b…`). Engine-core's 118-series signature shows
numerics unchanged between the two pins; the run stays labelled `98baf6b` and no number changes under `846c9e0`.

## Run configuration

| item | value |
|---|---|
| engine | clean `98baf6b` (pre-re-pin; numerics unchanged vs `846c9e0`) |
| spec | `docs/audit/canonical_spec.json` content sha `c5f9e2de1c04b4ef467f4e9016c942616f7c7e67f94bc3a08be9bbd7b2f34a05` (old V540-FREEZE, as launched) |
| gates | HK legacy 540 gates; KR primary `GATE_SPECS['KR-TRACKED']`; KR sensitivity `KR-SINGLE` |
| design | 18 arms × {HK, KR} × **100 matched seeds** = 1,800 (TRACKED) + KR-SINGLE 9 arms × 100 = 900 → **2,700 runs** |
| runner | `run_new_generation.py` sha256 `b5cd11c07dcf7716…` (re-aggregation uses `reaggregate_new_generation.py` sha `aba150774afd2cbb…`) |
| box | declared venv py3.10.8/numpy 2.2.6/scipy 1.15.3, 8 workers, nice 10, BLAS/OMP=1 |
| wall | **11,234.49 s ≈ 3 h 07 min** (driver PID 24480; 2,700/2,700 rows) |
| aggregation fix | the first aggregation emitted empty HK summaries (HK jobs keyed `PRIMARY` but looked up as `TRACKED`); **no re-run** — both JSONs re-aggregated from the intact per-seed checkpoints (9 HK × 100 rows), corrected `total_runs` (TRACKED 1,800; SINGLE 900) and engine label |

## Artifact hash table (re-hashed on the Mac; equals the box copies)

| file | sha256 |
|---|---|
| `results/newgen/paperB_new_generation_TRACKED.json` | `cf801af8e07f9ebf615d075c42ec742f00d5a98a19a0e938005a3632e28836d3` |
| `results/newgen/paperB_new_generation_SINGLE_KR.json` | `2b69fa08ea521c664bda59da4d6fce0d9b48d494d5cee793b69987795bef0330` |
| `results/newgen/new_generation_provenance.json` | `8f08164d08006d5c0225cd2115352270560806fe4055294ff16f453dd62e3301` |
| `results/audit/newgen/paperB_newgen_tables.csv` | full arms × metrics table with seed sd/CI and deltas |

## Compact results (mean over 100 matched seeds; seed sd in parentheses)

**HK (TRACKED primary):** Baseline K-12 61.93 (0.21), G12 49.37 (0.51), Q5−Q1 gap 34.89 (0.67) pp, Q5/Q1 spend 2.473,
elite-Q5 24.82 (1.06). **CF4a**: K-12 48.60, G12 39.14, gap 36.39, spend ratio 2.760, **spend index 70.6**,
**elite-Q5 23.21** → *spend < 80 and elite-Q5 below Baseline* → **Win-Win condition met in HK** (participation falls
materially, reported, not hidden). **CF4b**: spend index 90.0 → fails spend; elite-Q5 23.07. **CF1b**: spend index 97.2
→ fails spend. **CF3b**: spend 70.9, elite-Q5 23.43 → passes both but K-12 falls to 48.56.
**KR (TRACKED primary):** Baseline K-12 55.79 (0.24), G12 36.25 (0.52), gap 31.26 (0.79), spend ratio 2.205,
elite-Q5 23.90 (1.71). **CF4a**: K-12 42.81, spend ratio 2.391, **spend index 73.1**, **elite-Q5 22.16** → **met in KR**.
**CF4b**: spend index 109.7 → fails. **CF1b**: spend index 99.2 → fails. **CF3b**: spend 73.2, elite-Q5 22.21 →
passes spend/elite but K-12 falls to 42.80.
**KR-SINGLE sensitivity:** full table in `results/audit/newgen/paperB_newgen_tables.csv` and the SINGLE JSON.

## CF4 reversal — explicit

Pre-repair 540: **CF4a failed** the Win-Win criterion. New generation (100 matched seeds, repaired engine):
**CF4a meets the pre-stated Win-Win condition in BOTH HK and KR**, while **CF4b still fails** (HK spend 90.0; KR 109.7);
participation falls under CF4a (HK 61.93→48.60; KR 55.79→42.81), which is an **unmeasured welfare change**, not automatically a welfare cost: it could be lost useful support,
substitution by school-provided preparation, or families dropping low-value tutoring purchases. Interpretation requires
learning/access/teacher-workload/student-time data that the programme does not yet have. The Win-Win statement is an
accounting statement about spend and elite-Q5, **not a welfare statement**. The old CF4 failure is preserved in `GATE1_MIGRATION_TABLE.md` / `paper_claims.csv`.

## Uncertainty and labels

* Seed/MC uncertainty only (100 matched seeds, sd/95 % CI in the CSV); **calibrated-parameter uncertainty is zero in
  this stage** (frozen parameters) and is stated as such.
* Multiplicity: all 9 arms × 4 headline outcomes × 2 jurisdictions reported; **CF4a is the pre-stated primary** contrast.
* No VALIDATED claim; no causal claim; 420/540 docx numbers = AUTHOR-REPORTED baseline.
