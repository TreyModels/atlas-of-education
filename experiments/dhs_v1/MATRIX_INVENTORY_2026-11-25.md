# DHS fleet — first milestone record (2026-11-25)

**Lead:** `deepseek-dhs` (this session). **Worktree:** `/Users/treymenefee/neon-boot/wt5/dhs8`,
branch `research/dhs-eight-experiments-2026-11-25`. **Assignment:** Bridge `366086d3` (E1–E8) + `a2a2bc25`
(integration into the existing Atlas matrices). **Status:** exploratory only; no validation claims for the
untested R starter; no restricted microdata leaves the Mac.

## 1. R environment

| environment | status | detail |
|---|---|---|
| Box (AutoDL, 10-CPU cgroup) | **READY** | `Rscript` 4.1.2 (2021-11-01), `survey` 4.1.1 (`r-base-core 4.1.2-1ubuntu2`, `r-cran-survey 4.1-1-1`). Usable for synthetic QA/tests; **no restricted microdata may be placed there** (DHS terms / third-party server). |
| Mac (host) | **IN PROGRESS** | `brew install r` first attempt failed on a stale bottle-cache conflict; retry running. Execution of E1–E8 against real microdata must be on the Mac — see §5 policy. |

Policy resolution: **real microdata is processed locally only**; the box is used for (a) synthetic
QA/tests, (b) non-disclosive aggregate analyses after extraction. This supersedes any plan text that assumed
R-on-box for the real run.

## 2. Dedupe inventory (prior DHS work — reuse, do not rebuild)

| prior artifact | branch/worktree @ commit | what it is | verdict |
|---|---|---|---|
| Cambodia ingest + quintile profile | `wt3/dhs` @ `2d651e5`; `research/cambodia-dhs-2026-11-25` | `ingest_cambodia_dhs.py`, `quintile_profile.py`; validated 2021-22 primary NAR 72.8 vs DHS Table 2.12; attendance by wealth/sex/residence CSVs | **REUSE** as reference for KH adapter + benchmark |
| DHS IR pipeline + acquisition record | `wt2/dhs` @ `fc9b7f7`; `research/dhs-ir-pipeline-neon-2026-11-25` | acquisition plan, execution-ready record, AMENDMENT_03 code audit, IR inventory target CSVs (92 files/14 countries, 48 DHS+13 MIS+6 AIS = 67 E8 target rows) | **REUSE** metadata/targets; **no microdata in repo** |
| DHS API ecological panel | `wt2/dhseco` @ `792dba1`; `research/dhs-api-ecological-2026-11-24`, `dhs-corrected-2026-11-25` | country-year public DHS API indicator panels (`panel_edu2_FE_*.csv`), AFRICA11 extension, pre-reg + amendments + negative controls | **REUSE** as macro-linkage source (public aggregates) |
| Bulge micro-DHS feasibility | `wt2/bulge` @ `230521b`; `research/bulge-micro-dhs-2026-11-25` | DHS fertility target inventory, LSMS-ISA item scan, DATA_AVAILABILITY; bulge test NOT-ESTIMABLE | **REUSE** (feasibility + absent-data ledger); do not cite as estimation |
| PH/VN/Cambodia credential-floor extracts | `research/id-dhs-2026-11-25` @ `206bbde`, `ph-dhs-*`, `vn-dhs-*` (in `wt3/{iddhs,phdhs,vndhs}`) | bottom-40 share of non-attenders, attendance/completion by wealth | **REUSE** as prior descriptive results + extraction choices |
| Eight-experiment starter | `experiments/dhs_v1/` (this worktree) | `README.md`, `experiments.R`, `source_attachment.tar.gz` sha `6a6f2363…` | **USE** (binding), untested |

**Not duplicated / do not use as evidence:** `research/dhs-eco-gfr-uncomputed` claims were retracted
(GFR never estimated); any ecological result that mixes DHS-API with within-country micro data must be labelled
ecological. No prior artifact contains the E1–E8 design.

## 3. Data inventory (local microdata — restricted, stays on the Mac)

`~/neon-boot/pulled/dhs` = 2.8 GB. Recodes present:

| country | person recode (PR) | woman recode (IR/WI) | household (HH) |
|---|---|---|---|
| Cambodia (KH) | 2000, 2005, 2010, 2014, 2021-22 (**`.SAS7BDAT` only**) | same 5 waves (`.SAS7BDAT`) | — |
| Indonesia (ID) | 1991, 1994, 1997, 2002-03, 2007, 2012, 2017 (DTA) | IDWI3A 1997 (verify parse) | IDHH01 1987 |
| Philippines (PH) | 1993, 1998, 2003, 2008, 2013, 2017, 2022 (DTA + SAS mixes) | PHIR82 2022 (DTA); PHWI31/3A 1993/1998 | — |
| Vietnam (VN) | 1997, 2002, 2005-AIS (DTA) | VNWI31 1997, VNWI41 2002 | — |

Verified variable presence (from `.DCT/.DO` and SAS headers): PR `hv121` (attendance), `hv270/271`
(wealth quintile; **KH 2000 PR lacks wealth**), `hv108` (school years), `hv009` (household size), `hv005`
(weight), `hv021/22/23` (PSU/strata); IR/WI `v005,v021,v022,v023,v025,v133,v716/v717/v731` (current school);
`v201/v212/v511/v525` (CEB, age first birth, age first union) are present in standard IR and **must be
verified per wave by the data team** (older WI/PR variants need `convert_categoricals=False` in pandas; the
2022 PH IR has non-unique value labels that break naive `read_stata`).

No `.dta`/`.sav` is committed to git (correct — DHS terms).

## 4. Matrix inventory (the existing large programme — found, not invented)

| id | name / version | location (branch @ commit; data) | axes | units | provenance / restrictions |
|---|---|---|---|---|---|
| M1 | **Imputed lead–lag matrix**, 2026-11-23 | `origin/research/imputed-matrix-2026-11-23` @ `5e4602b`; `research/records/2026-11-23-imputed-matrix/` (`results/all_links.csv`, `coverage.csv`, `matrix_decomp.json`) | 217 countries × 74 years (1950–2023) × 17 measures; 20 imputation draws `m01–m20`; 272 ordered links | lead–lag coefficients (cause starting level → outcome 10-year change), SE, t, p, n, n_countries, year window; coverage shares | panel box2 `/root/work/data_imputed` (not on Mac); committed results are the durable record; **country-year aggregate**, imputed cells flagged; placebos: wrong-country null 21.7 % significant ⇒ **not causal** |
| M2 | **Imputed panel backcast** | `origin/research/imputed-panel-2026-11-23` @ `1552cf6`; `.../2026-11-23-imputed-panel/scripts/` | same panel; backcast/impute pipeline | imputation outputs + validation | scripts; rerun pending (metadata says matrix rerun pending) |
| M3 | **Marriage-extended matrix** (20 measures), 23 Nov | `origin/research/matrix-marriage-2026-11-23` @ `559a4e9`; `data/matrix20.csv` | 20 measures × 19 = 380 ordered links × 2 settings (country FE; +trend); country-year panel, survey years ~1990–2014 | coefficient `b`, `se`, `n`, `nc`, `n10`, `year_first/last`, `t`, `p`, `q` | box2 `/root/work/matrix_marriage`; CSV committed is durable; marriage never a control |
| M4 | **Phase-transition dense 20×20 grid**, 25 Nov | `origin/research/phase-transition-dense-2026-11-25` @ `ced04a7`; `wt2/dense` records `2026-11-25-phase-transition-dense/` | 20 `vac0` (0.01–0.63, geometric) × 20 fee (0.00–0.19) × 20 seeds × 2 gates = 16,000 runs / 800 cells | simulation outcomes per cell (tutoring Q5−Q1 gap, gate-fail share, completion, liquidity, …) | box `/root/work/equifinality_phase`; **SIMULATION ONLY**; pre-registered statistic + amendment |
| M5 | **Synthetic worlds matrix**, 24 Nov | `origin/research/synthetic-matrix-2026-11-24` @ `77d6f23`, `synthetic-loop-2026-11-24` @ `394fb32`; `research/records/2026-11-24-synthetic-loop/results/*.json` | 64 countries × 10 independent blocks × 6 specs × 4 literature worlds + s=0; N=10k | synthetic calibration/rejection/predictive-discrimination metrics | **SYNTHETIC**; not empirical; no held-out claim |
| M6 | **DHS API ecological panel** | `origin/research/dhs-api-ecological-2026-11-24` @ `9fd9d90`; `wt2/dhseco` `research/records/2026-11-24-dhs-api-ecological/data/panel_edu2_FE_*.csv` | country-year (AFRICA11 extension) | public DHS API indicator values (levels/trends), FE coefficients | public aggregates; ecological — not household behaviour |
| M7 | **Bulge micro-DHS target inventory** | `origin/research/bulge-micro-dhs-2026-11-25` @ `230521b`; `research/records/2026-11-24-dhs-acquisition/data/` | 14 countries / 92 DHS files; 67 E8-country target waves (48 DHS+13 MIS+6 AIS) | metadata/targets only (held=NO) + LSMS-ISA item scan | DHS gated; no microdata in repo |
| M8 | **Massification full-system multiverse** | branch `research/masseng-edsystem-2026-11-25`; `wt2/dense/research/records/2026-11-25-masseng-edsystem/` | 144 combinations (affordability × supply × gate kind × labour regime) × 10 seeds = 1,440 runs | simulation outcomes, multiverse summary JSON | **SIMULATION ONLY**; illustrative parameters; exit-reason retraction recorded |
| M9 | **Comparative cases registry** v0.2 (2026-11-04) | `docs/engine/comparative_cases/case_registry.json` | country/policy cases (PH nursing, PH K-12, …) | case metadata, policy events, observed series | mixed evidence levels (quasi-experimental / administrative) — per-case status |
| M10 | **150-equation suite** | `wt2/eq` `research/records/2026-11-25-equation-suite/` (`SUMMARY`, `PRE_REGISTRATION`, `NEON_PATCHES`) | ~150 equations / model components catalogue | equation inventory + implementations + audit status | paper/engine audit; verify count from SUITE_REPORT before citing |
| M11 | **Engine data extracts** | `engine/data/asia_school_work.json`, `engine/data/*`; `inputs/{credential_floor_sources,other_sources}.json`, `inputs/trajectories_100_seeds.csv` | Asia country-year school/work; credential-floor sources | series values, source metadata | mixed provenance; check each before linkage |

**Dedupe result:** the "large multi-country matrix programme" = **M1/M3 (country-year lead–lag matrices,
imputed + observed)**, **M4/M8 (simulation grids)**, **M5 (synthetic worlds)**, **M6 (DHS API ecological)**,
**M9/M10 (case and equation inventories)**. The DHS household experiments add a **new micro→aggregate layer**
that does not yet exist in any of them; M1/M3 provide the country-year macro spine, M6 the public DHS API
country-year comparators, M9/M10 the model observables/equations to map onto.

## 5. E1–E8 data availability (preliminary; data team to verify)

| exp | outcome (denominator) | KH | ID | PH | VN |
|---|---|---|---|---|---|
| E1 attendance by wealth, ages 14–17 | `hv121` × `hv270/271`, PR | **FEASIBLE** 2005–2021-22 (2000 lacks wealth) | FEASIBLE 2002-03+ (verify hv121/hv270 in 1991–97) | FEASIBLE 2003/2008/2013/2017/2022 (1993/1998 **BLOCKED**: no attendance/wealth) | **BLOCKED** (no attendance in PR) |
| E2 attendance by residence | `hv121` × `hv025`, PR | FEASIBLE all 5 | FEASIBLE 2002-03+ | FEASIBLE 2003+ | BLOCKED |
| E3 attendance by sex | `hv121` × `hv104`, PR | FEASIBLE all 5 | FEASIBLE 2002-03+ | FEASIBLE 2003+ | BLOCKED |
| E4 children ever born by schooling, women 40–49 | `v201` × `v133`, IR | FEASIBLE (all 5 waves, SAS) | PARTIAL (IDWI 1997 only) | PARTIAL (PHIR 2022; verify PHWI 1993/98) | PARTIAL (VNWI 1997/2002) |
| E5 birth <20 by schooling, women 25–34 | `v212` × `v133`, IR | FEASIBLE | PARTIAL | PARTIAL | PARTIAL |
| E6 current school by residence, women 20–24 | `v716` (IR) or `hv121` (PR, person weight) | FEASIBLE | FEASIBLE (PR 2002-03+) | FEASIBLE (PR 2003+; IR 2022) | PARTIAL/BLOCKED (verify v716 in VNWI) |
| E7 union <20 by schooling, women 25–34 | `v511/v525` × `v133`, IR | FEASIBLE | PARTIAL | PARTIAL | PARTIAL |
| E8 household size by schooling, women 40–49 | `hv009` × `hv108`, PR female rows (person weight) | FEASIBLE | FEASIBLE (PR waves) | FEASIBLE (PR 1993+; no attendance needed) | FEASIBLE (PR 1997/2002/2005) |

Status notes: "PARTIAL" = data exist for 1–2 waves only → report as limited-wave evidence, not a trend.
Record-type/weight rule: PR/person rows use `hv005`; woman recode rows use `v005`; **never mix**. Country
coverage gives a 2–5 country design ⇒ few-country inference; report country as the unit and effective N.

**BLOCKED list (preliminary):** E2/E3 for VN; E1–E3 for PH 1993/1998; E1 for KH 2000; ID 1987 (HH only).

## 6. Run plan and roles (gated)

| stage | owner | deliverable | gate |
|---|---|---|---|
| 0 | lead | this record + Bridge post; R local install | — |
| 1 | data team (`engine-tutoring`) | dedupe inventory, availability matrix (verified), adapters → `normalized.csv`, 2 published benchmarks/country | read by QA; **no execution** |
| 2 | QA (`qa-verifier`) | defect list on `experiments.R`, synthetic test suite (known means, design SEs, lonely PSU, missingness, domain variance, suppression, multiplicity), sign-off checklist | **sign-off required before E1–E8** |
| 3 | lead + QA | run E1–E8 locally (R), per country/wave; suppression + BH by pre-declared family; benchmark comparison; write `results/` + hashes + logs | milestone 2 |
| 4 | lead + data team | L1 aggregate layer → join to M1/M3/M6 macro spine; feasibility classification (FEASIBLE/PARTIAL/BLOCKED per link) | milestone 3 |
| 5 | model/audit (`engine-core`, queued) | model-observation mappings + competing mechanism predictions (fertility, massification, migration/prices, credentials, shadow ed) | after slot frees |
| 6 | QA | joined-prototype QA (ecological fallacy, pseudoreplication, effective N, held-out checks) | before any study write-up |

## 7. Open decisions / blockers

1. **Local R install** is the execution blocker for E1–E8 (microdata must stay local). Retry in progress.
2. Report-type weight mapping and IR `v716` presence must be verified per wave (data team).
3. PT/ID/PH `hv121` presence in pre-2002 waves is unverified (data team).
4. Matrix M1/M3 panels live on retired/box2 paths; committed result CSVs are the durable record — macro
   linkage prototype will use those plus M6 public API panels rather than re-running the box panels.
5. "150-equation" count must be read from the suite report before any claim (model/audit, when unqueued).
