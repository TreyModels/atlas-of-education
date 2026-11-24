# Paper N2 — claims-to-source map

Every number in `paper.md`, `claims-prior-art.md` and `refs.md`. The empirical record is
`research/corr-battery-2026-11-23` @ **9363079** (branch pushed; pre-registration commits 772650a and
6a1927f, pushed before any code). Paths below are relative to `research/records/2026-11-23-corr-battery/`
unless stated. The literature audit is `research/lit-audit-2026-11-24` @ **0bcd33f** (claims map) and
the auditor memo **e51c4cf** (novelty-review, supplied via the Lead); no paper number depends on it.

## Run and design facts

| claim / number | file | field |
|---|---|---|
| 342 estimable ordered pairs; 19 measures (19 × 18 = 342) | `data/pair_table.csv` (342 rows); `README.md` | row count; "19 measures" |
| 936,657 estimable cells of 2,111,508 (44%); minimum-sample rule n ≥ 60, ≥ 8 countries | `README.md` (pre-registered grid table); `data/results_summary.json` → `grid_a` | `grid_a.levels.n` + `grid_a.changes.n` = 11,086 + 10,164 |
| 13,800 partitions × 6 groups × 342 pairs × 2 relations; 56,077,352 within-group regressions | `README.md`; `data/results_summary.json` → `counts.done.B` | `counts.done.B = 13800`; regression arithmetic in README |
| 10,447,698 recorded result rows; 3,018 s; 10 workers; one crash-and-resume | `README.md`; `results/logs/battery.log`; `data/results_summary.json` → `counts` | `counts.regs`, `counts.elapsed` |
| 500-rep clustered bootstrap (171,000 draws); threshold bootstrap (6,000); placebo grid (100,092) | `README.md`; `data/results_summary.json` → `counts.done.C`, `counts.done.T`, `counts.done.P` | `C = 342`, `T = 4`, `P = 342` |
| pre-registered rules (≥80% levels; <30% change; placebo ≥80%) | `PRE_REGISTRATION.md` | decision rules section |

## Levels versus changes (Table 1)

Source: `data/pair_table.csv`, columns `level_b`, `level_se`, `level_n`, `level_countries`,
`change_b`, `change_se`, `change_n`, `change_countries`, filtered to `outcome == fertility` and the eight
schooling predictors. The eight rows:
mean years women −0.129 (0.029) 5,915/192; total −0.227 (0.042) 1,394/144; secondary enrolment
−0.0213 (0.0037) 5,927/202; lower-secondary −0.0224 (0.0035) 4,106/193; primary −0.0239 (0.0033)
4,878/193; tertiary −0.0040 (0.0020) 5,126/198; gender parity secondary −1.968 (0.277) 5,708/199;
gender parity tertiary −1.265 (0.197) 4,455/198.
Change columns: +0.115 (0.046) 4,225/189; +0.189 (0.054) 1,107/109; +0.0029 (0.0026) 4,548/198;
+0.0064 (0.0031) 2,830/185; −0.0004 (0.0020) 3,561/185; −0.0044 (0.0026) 3,854/191; +0.059 (0.190)
4,900/195; +0.010 (0.207) 3,198/191.

## Specification-grid shares (Section 4.1–4.2)

Source: `data/pair_table.csv` columns `level_share_neg`, `level_share_negsig`, `change_share_neg`,
`change_share_negsig`. Values: level negative 0.704–0.834; level negative-significant 0.429–0.594;
change negative 0.241–0.443; change negative-significant 0.035–0.135. Matrix-wide (all 342 pairs):
`data/results_summary.json` → `grid_a.levels` (share_negative 0.422, share_negative_significant
0.307) and `grid_a.changes` (0.508, 0.090); all cells `grid_a.levels_all` (0.447, 0.199) and
`grid_a.changes_all` (0.509, 0.132).

## Transportability (Table 2, Section 4.3)

Source: `data/pair_table.csv` columns `transport_level_share`, `transport_change_share` for the same
eight rows: 0.913/0.000; 0.914/0.002; 0.979/0.001; 0.986/0.001; 0.989/0.028; 0.715/0.001; 0.962/0.072;
0.811/0.003. Aggregate over all 342 pairs: `data/results_summary.json` → `transport`:
levels_mean 0.2267 [q05 0.2144, q95 0.2388]; change_mean 0.1115 [0.1026, 0.1203], 13,800 partitions.
Per-partition data: `data/transport.csv`.

## Threshold shape and bootstrap (Section 4.4)

Source: `data/results_summary.json` → `threshold_bootstrap` (women's mean years: −0.326 [−0.405,
−0.248], −0.092 [−0.175, −0.013], +0.112 [0.057, 0.171]; total years: −0.387 [−0.483, −0.283], −0.274
[−0.364, −0.182], +0.174 [0.106, 0.250]); `data/results_summary.json` → `bootstrap` (8/8 focal pairs
exclude zero; all-pairs 74.6% of 342); `data/bootstrap.csv`.

## Placebo (Section 4.5)

Source: `data/results_summary.json` → `placebo_future`, `placebo_focal`, `correct_time_focal`,
`correct_time_same_cells`; `README.md` "(1) Fertility — the placebo, reported as it is": focal pairs
52.9% placebo negative-significant (median −0.0179) vs 58.8% correct-time (median −0.0224); all-pairs
20.1% vs 21.1%.

## Literature (claims-prior-art.md, refs.md)

Auditor-supplied centered list: novelty-review memo e51c4cf and
`research/records/2026-11-24-lit-audit/claims-map.md` (`research/lit-audit-2026-11-24` @ 0bcd33f).
Crossref verification for every reference was run 24 Nov 2026 via `api.crossref.org` (direct DOI
lookup and `query.bibliographic`); statuses V/S/U/N are recorded in `refs.md`. No citation in the
paper lacks a status mark.

## Notes
- No new estimation was run for this draft (box2 was down; none was needed). The paper's numbers are
  read from the committed JSON/CSV of the corr-battery record.
- The 13,800 partitions are an extension of the pre-registered 800 (load fill, same statistic); this
  is stated in the paper and the record.
- The paper's novelty framing follows the auditor's verdict (INCREMENTAL — new assembly) and makes no
  "first" claim.
