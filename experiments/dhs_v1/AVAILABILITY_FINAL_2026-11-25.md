# DHS — FINAL data availability (corrected), 2026-11-25

**Supersedes §5 of `MATRIX_INVENTORY_2026-11-25.md`.** Source of truth for execution:
`harmonize/_out/availability_E1_E8.csv` (per wave × experiment, with n and groups) and
`harmonize/_out/availability_matrix.csv` (per variable), produced by the data team and independently audited by
QA against the local raw files. **Corrections accepted from the data team:**

1. **The `WI` files (`IDWI3A`, `PHWI31/3A`, `VNWI31/41`) are wealth-index files** (`whhid`, `wlthindf`,
   `wlthind5`), **not woman recodes**. Therefore **E4, E5, E7, E8 are feasible only for KH (5 waves) and
   PH 2022** — the preliminary matrix's ID/VN coverage was wrong.
2. **VN E2/E3 are FEASIBLE** (attendance present in VN PR); preliminary "blocked" was wrong.
3. E1 requires a wealth grouping: feasible only where wealth exists (ID 2002-03+, PH 2003, PH 2017/2022,
   VN 2005ais, KH 2005+); PH 2008/2013 have attendance "na" (outcome absent); ID 1991–97, KH 2000, PH 1993/98,
   VN 1997/2002 are E1-BLOCKED (no wealth) but E2/E3 feasible.
4. E6 = person-record domain of females 20–24 (PR, `hv121`/`hv110`, `hv005`) — approved as D-01; **no** IR/WI
   recode carries a current-school item.

## Feasible cells (22 waves × 8 experiments = 176 cells; **96 feasible, 80 blocked**)

| experiment | feasible waves (n = complete cases) | countries |
|---|---|---|
| **E1** attendance by wealth, 14–17 | ID 2002-03/2007/2012/2017; KH 2005/2010/2014/2021-22; PH 2003/2017/2022; VN 2005ais (12) | ID, KH, PH, VN |
| **E2** attendance by residence | 20 waves: ID 1991–2017 (7), KH 2000–2021-22 (5), PH 1993/98/2003/2017/2022 (5), VN 1997/2002/2005ais (3) | ID, KH, PH, VN |
| **E3** attendance by sex | same 20 waves as E2 | ID, KH, PH, VN |
| **E4** children ever born by schooling, women 40–49 | KH 2000/2005/2010/2014/2021-22; PH 2022 (6) | KH, PH only |
| **E5** birth <20 by schooling, women 25–34 | same 6 waves | KH, PH only |
| **E6** current school by residence, women 20–24 | 20 waves (ID 7, KH 5, PH 5, VN 3) | ID, KH, PH, VN |
| **E7** union <20 by schooling, women 25–34 | same 6 waves | KH, PH only |
| **E8** household size by schooling, women 40–49 | same 6 waves (person-record women) | KH, PH only |

Complete-case n per cell are in `availability_E1_E8.csv` (e.g. E4 KH 2021-22 n=4,228, PH 2022 n=6,601;
E1 KH 2021-22 n=6,337). Cells below the D-03 suppression thresholds will be suppressed at run time, not dropped
silently.

## Normalized inputs (local only, not committed)

`~/neon-boot/dhs-normalized/` — 28 CSVs: KH 10 (person+woman × 5 waves), ID 7 (person), PH 8 (7 person + PH2022
woman), VN 3 (person). Raw microdata stays at `~/neon-boot/pulled/dhs`; both are local-only (DHS terms).
Weights: PR/person `hv005/1e6`, IR/woman `v005/1e6` (never mixed). Attendance: `hv110==1` where present, else the
per-wave verified `hv121` code; ages/schooling sentinels 97/98/99 → NA (99-only for known never birth/union).

## Singleton-PSU design issue (blocking, per D-07)

Data team found singleton-PSU strata in **PH 2008 (19 strata), VN 1997 (1), VN 2002 (1), ID 2007 (1)**; all other
24 files have none. QA earlier reported "none" — reconciliation required (likely because QA audited the merged
`normalized_all.csv`, where per-file PSU/stratum codes are not preserved). PH 2008/2013 cells are blocked anyway
(attendance absent), but **VN 1997/2002 E2/E3/E6 and ID 2007 E1/E2/E3/E6 are feasible cells that include
singleton strata**, so the design treatment must be documented and sensitivity-tested before execution.

## Benchmark status (registry v0.2)

| id | published | DHS extract | verdict |
|---|---|---|---|
| B001 | KH 2021-22 primary NAR 72.8 (FR377 Table 2.12) | 74.65 | +1.85 pp, **within ±2.5 pp** definitional tolerance |
| B002 | KH 2021-22 M 72.0 / F 73.5 | M 73.23 / F 76.14 | M within; F +2.64 pp slightly outside → report direction/definitional gap |
| B003 | KH 2021-22 secondary NAR 42.0 | 60.18 | **not matched** (level-specific vs any-level attendance) — excluded as validation, kept as direction note |
| B004 | KH 2021-22 urban 75.5 / rural 71.3 | 76.93 / 73.44 | **within ±3.0 pp** |
| B005–B008 | PH/ID/VN, E4–E8 | — | **BENCHMARK-PENDING** (no exact public report value retrieved); no substitution, results flagged not externally benchmarked |

The KH extract reproduces the prior validated extraction exactly (74.7; M 73.2 / F 76.1), i.e. adapter recodes are
consistent with the earlier verified pipeline.

## L1 aggregate layer (input to the matrix prototype)

`harmonize/_out/aggregate_layer.csv` — 252 estimates, 176 cells, survey-matched SEs (full-design domain
estimator), 6.3 % suppressed by n<50/design; `coverage_missingness.csv` per cell; `join_manifest.json` records
country-year keys, weights, units, timing and provenance. Subnational linkage BLOCKED (survey-specific regions +
displaced GPS); macro candidates = M6 public DHS-API panels; M1/M3 declared not local. R 4.5.3 `survey` 4.5
cross-check on KH 2021-22 E1 reproduced Python estimates/SEs exactly (0.446623 / 0.017073). This layer is the
L1 input to `INTEGRATION_SCHEMA_v0.1.md`; household microdata is never included.

## Frozen inputs and run preflight (data-team follow-ups, commit `d0e832a`)

* `harmonize/_out/singleton_ledger.csv` (sha256 `9df4c109…a1895c`, 6,464 stratum rows) — **22 singleton strata**:
  PH 2008 19, VN 1997 1, VN 2002 1, ID 2007 1. This is the authoritative D-07 ledger QA must reconcile against.
* `harmonize/_out/run_map.csv` (sha256 `fa751827…b02e38b0`, 28 rows) — per-file feasible experiments derived from
  the verified availability matrix (person files → E1/E2/E3/E6 per D-01; woman files → E4/E5/E7/E8; PH2008/2013
  empty; E1 dropped where wealth is absent).
* `harmonize/_out/normalized_output_hashes.csv` (sha256 `3fd87f6e…f1841b9a`, 28 local files) — the normalized
  inputs are **FINAL/FROZEN**: path, sha256, bytes, rows. Any recode change requires a new commit + hash list.
* The run harness (`runs/run_all.py`) now **refuses** to run if any input's sha256 is not pinned, if the run map is
  missing, or if a feasible (file, experiment) pair produces no estimate; it writes `feasibility_gaps.csv` and
  records the singleton-ledger/hash-list/run-map sha256 in `run_manifest.json`. A simulated unpinned input is
  rejected with `[preflight] REFUSED: … not in normalized_output_hashes.csv` (verified).
* Benchmark source policy (data team, README §9): public-report references only (KH FR377 Table 2.12; PH FR381;
  ID 2017 final report); no further "published" numbers; B005–B008 stay PENDING unless an exact table is located.
