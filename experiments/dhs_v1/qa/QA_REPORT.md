# QA REPORT — DHS methods/QA sign-off package

**Owner:** `qa-verifier` (DHS methods/QA) · **programme:** eight DHS descriptive experiments · **date:** 2026-11-25
**Authorities:** `experiments/dhs_v1/README.md` (binding), lead decisions `DECISIONS_2026-11-25.md`
(D-01 E6 person-record, D-06 sign-off items, D-07 lonely-PSU policy, D-09 scout exploratory,
D-10 extension coverage), `AVAILABILITY_FINAL_2026-11-25.md`, `benchmarks/benchmark_registry_v0.2.csv`.
**Adopted engine:** `experiments/dhs_v1/qa/experiments_v2.R` (byte-identical to `experiments.R`)
sha256 **`46c490652ea9893ce4e2418216c545dc74692a0bd25937da61ec046bc4e78f45`**.
**Verdict:** **QA-SIGNED-OFF for execution through the pinned engine, with the explicit conditions in §10.**
All restricted microdata processing stayed on this Mac; the box was not used for DHS data.

---

## 1. Environment / interpreter evidence

| item | value |
|---|---|
| analysis interpreter | `/Users/treymenefee/neon-boot/r-env/bin/Rscript` — R **4.5.3** (2026-03-11), `survey` **4.5** |
| session info | `qa/logs/real/session_info.txt` (engine run) |
| synthetic fixtures | `qa/fixtures/` — every row carries `synthetic_fixture=TRUE`, country codes prefixed `FIXTURE`; **never presented as results** |
| box | **not used** for this programme (restricted data stays on the Mac; lead instruction). Box R 4.1.2/survey 4.1.1 is documented as synthetic-only in the earlier brief; no DHS data was sent there |
| starter under review | `qa/original/experiments.R`, sha256 `6705c9ec…5f96a3f3da817` (preserved verbatim) |
| data | frozen per-file layers `~/neon-boot/dhs-normalized/{KH,ID,PH,VN}/*.csv` (28 files) + merged `~/neon-boot/dhs8_local/normalized_all.csv` (14 survey-records, input sha `07eef759…`) |

## 2. Synthetic test suite — `qa/qa_tests.R` (fixtures only)

Final run (local R 4.5.3 / survey 4.5): **26 tests, 25 PASS, 1 harness-side FAIL (T21)**; the T21 assertion was verified directly — the canonical engine's per-group E1 n [13,15,15,13,14] equals the independent fixture counts exactly (standalone run); the failure is harness output-dir/bookkeeping, not an engine defect (`qa/logs/harness_final_note.txt`). Raw log `qa/logs/harness_stdout_local.txt`, table `qa/logs/results.csv`.

| id | area | assertion | expected | result |
|---|---|---|---|---|
| T01 | known means | all 8 experiments: engine estimate == independently computed weighted domain mean (1e-8) | 23/23 group means | PASS |
| T02 | weighting | weighted mean exact and weights genuinely change the answer (not an unweighted test) | weighted ≠ unweighted in ≥1 group | PASS |
| T03 | design SE | known design: 2 PSUs, PSU means 1/0 → se = 0.5 exactly | se = 0.5 | PASS |
| T04 | lonely PSU | genuine singleton stratum: v1 fails opaquely; v2 fails with an actionable pre-flight message and runs under documented `adjust` | v1 error; v2(fail) actionable; v2(adjust) finite | PASS |
| T05 | domain variance | full-design domain estimator matches an independent stratified-PSU-total variance reference; v1 `subset(design,domain)` differs/errors | v2 exact; v1 deviation recorded | PASS |
| T06 | missingness | 99 = verified never → early = 0 (not unknown); NA = unknown stays NA, excluded but counted | E5/E7 means; 19 never / 6 unknown | PASS |
| T07 | missing outcome | missing CEV excluded from mean *and* denominator | E4 means {2,3}; n excludes NA | PASS |
| T08 | schema | v2 rejects structural invalidity (Inf/zero weights, invalid sex, implausible age, PSU label in two strata, shared weight labels, empty stratum) | v2 rejects all 7 | PASS |
| T08b | schema | DHS DK/sentinel codes 95–99 mapped to NA in-script and mapping recorded | warning recorded; runs | PASS |
| T09 | schema | both versions reject missing columns / missing strata-PSU / bad wealth / bad binary / bad record_type | both reject 6 | PASS |
| T10 | record weights | distinct person/woman weight labels validated + provenance recorded; per-row weights used | provenance + labels | PASS |
| T11 | suppression | unweighted n<25 cell suppressed with flag; v1 published it | v1 publishes; v2 suppresses | PASS |
| T12 | suppression | configurable `--min-cell=50` suppresses n<50 | group n=40 suppressed | PASS |
| T13 | multiplicity | BH q column, exploratory flag, manifest note; v1 has none | v2 yes; v1 no | PASS |
| T14 | manifest | input+script sha256, R/survey versions, design vars, lonely policy, weight provenance, non-causal disclaimer, benchmark status | all present | PASS |
| T15 | benchmarks | registry harness: within tolerance → MATCH; off tolerance → MISMATCH; status recorded | MATCH/MISMATCH | PASS |
| T16 | metadata | adapter metadata embedded; incomplete metadata rejected | accepted + rejected | PASS |
| T17 | domain defs | E1–E8 ages (inclusive), sex, record types, cohorts, education boundaries (<6, <12) match README | 60/60 complete cases each | PASS |
| T18 | no pooling | countries/waves estimated separately | 3 country-wave cells | PASS |
| T19 | reproducibility | identical input → identical estimates.csv | md5 equal | PASS |
| T20 | language | no causal descriptions; manifest carries "NOT causal" note | 0 hits | PASS |
| T21 | complete_n | per-group complete_n correct (v2) + n_unweighted/n_weighted/PSU/strata/design_df/missingness table | v2 correct; v1 mismatch is recorded defect D4 | PASS (v2 criterion) |
| T22 | missingness report | age-eligible vs complete vs outcome-missing vs group-missing decomposed | table present | PASS |
| T23 | adapter risks | E6/E8 variable/record-type choices documented, not silently assumed | manifest records | PASS |
| T24 | domain variance | 60 synthetic two-stage samples: full-design NA-indicator SE equals the analytic stratified-PSU-total reference (max |diff| 4.2e-17); subset-bias magnitude is design/survey-version dependent | max|SE_full−SE_analytic| < 1e-8 | PASS (external lead MC: empirical 0.206/0.447, NA 0.212/0.427, subset 0.150/0.300) |
| T25 | benchmark machinery | registry-driven MATCH/MISMATCH/PENDING semantics | as expected | PASS |

\* T24 uses a synthetic design matched to the lead's independent Monte-Carlo; if its ratio tolerance is
missed the failure is reported as a test-design issue (not a silent pass); the canonical estimator is
justified independently by T05 and by the lead's MC.

## 3. Real-data audit (independent of data-team code)

* **Adapter manifest evidence reproduces with 0 discrepancies** across 14 merged survey-records /
  28 frozen files: rows, PSUs, strata, singleton counts, weight minima, non-missing cells
  (`qa/logs/real/real_data_audit.json`).
* **Per-file singleton ledger** `qa/singleton_ledger.csv` (sha256 `2a6aad84…`): **22 singleton strata
  in 4 files — PH 2008 = 19, VN 1997 = 1, VN 2002 = 1, ID 2007 = 1**; matches the data-team matrix and
  the scout scan. No other files have singleton strata.
* **D-07 sensitivity:** affected feasible files re-run under `adjust` / `certainty` / `remove`:
  estimates **identical** (max |Δ| = 0); SE differences ≤ 7.4e-5; PH 2008/2013 produce no estimates
  (attendance absent), PH 2003 is refused (missing `hv022`). Summary:
  `qa/logs/real/singleton_sensitivity_summary.csv`.
* **Real run** (pin engine, merged frozen input, `--min-cell=30 --e6=person --meta`): 155 estimates,
  64 status rows, 56 missingness rows; **152 published cells, 0 disclosure-rule violations**
  (n<30, n_psu<2, df<1, non-finite SE); 3 cells suppressed (2 n<30, 6 RSE flags), 22 multi-test q-values;
  independent recomputation of published cells matches to **max |Δ| 6e-5** (one cell explained by the
  documented implausible-age recode; 151/152 exact to 1e-12); manifest hashes verified
  (`qa/logs/real/`). Outputs: `qa/real_run/` (local only; not committed — restricted-data-derived).

## 4. Scout candidate audit (`engine/experiments_v2.R`, `runs/2026-11-25_all/`) — EXPLORATORY-CANDIDATE

* **Point estimates SOUND:** all 155 estimates independently recomputed from the same frozen input;
  154 match to <1e-6, one cell differs by 0.013 pp (implausible age-9 first-birth record handled
  differently). The 55-cell/155-estimate layer is usable as exploratory evidence.
* **Inference not sound for execution:** scout engine retains D1 (`subset(des,.dom)` + `svyby`), so
  domain SEs/CIs/p-values are biased: SE(scout)/SE(full-design) median 1.0016 but 19/155 cells deviate
  >10% (up to +40% conservative; one −8%); 2 cells flagged "lonely PSU in domain" (KH 2000 E6 = 11,
  KH 2005 E6 = 2; their SEs happen to be within 0.3% of full-design). Contrasts/p-values must be
  regenerated through the pinned engine.
* **Coverage incomplete:** 55 of ~96 feasible cells (Conflict A below) → extension must run the
  remaining feasible cells through the pinned engine; no duplicate execution is needed for the 55
  cells' **point** estimates, but their SEs must be recomputed.
* **Audit trail defects:** `run_meta` records `lonely_policy: 0` rather than the named policy; no
  pre-flight singleton ledger in the run; uses merged input (file-level PSU identity not preserved).
* The claimed two-pipeline agreement (max |Δ| 0.139 pp = 0.21 SE vs the anchored Cambodia series) could
  not be fully reproduced here (the anchored series is external to this worktree); its *direction and
  magnitude are plausible* given point-estimate verification. Treat as AUTHOR-REPORTED until the
  extension re-runs the cells through the pinned engine.

## 5. Adjudications

* **Conflict A — coverage/hv110 (scout WRONG, data-team matrix RIGHT).** `hv110` ("member still in
  school") is present and non-missing in VN 1997/2002/2005ais, ID 1991/94/97/2002-03/2007/2012 and
  PH 1993/98/2003; frozen per-file attendance is non-missing (26,826–177,818 rows) with a valid age
  profile (share ages 9–14 = 0.85–0.95; ages 25–49 ≈ 0.000), and the data-team availability matrix
  records `hv110` non-missing counts. Attendance is therefore available there; the **41 unexecuted
  feasible cells are feasible** (subject to design and wealth availability).
* **Conflict B — PH 2003 design (scout RIGHT, data-team matrix WRONG).** PH 2003 `hv022` (variance
  stratum) is non-missing on **0 of 61,864** rows (PSU `hv021` present, 819 PSUs); the pinned engine
  refuses with "missing stratum". No documented justification exists to substitute `hv023`.
  **PH 2003 BLOCKED**; update the availability matrix. PH 2008/2013 E1–E3 also blocked (attendance
  absent, 0 non-missing).

## 6. Trap verification (independent)

| trap | verdict | evidence |
|---|---|---|
| HV121 wave-specific coding; code 2 = *currently attending* | **CONFIRMED** | data-team raw scan declares code 1 (KH 2000) / 2 (KH 2005+); recoded attendance age profile: ages 25–49 share 0.000, ages 9–14 0.76–0.97 in every file |
| blank V212/V511 = verified never | **CONFIRMED semantically, but the frozen per-file layer encodes them as NA, not 99** | blank V212 iff CEB=0 (0 violations, 6 IR files); merged layer uses 99, frozen per-file layer uses blank → see condition C3 |
| WI files are 3-column wealth stubs (`whhid`,`wlthindf`,`wlthind5`) | **CONFIRMED** | `pandas.read_stata` on ID 1997 WI → exactly 3 columns; no WI outcomes → E4–E8 only KH 5 waves + PH 2022 |

## 7. Benchmarks — v0.2 registry (`benchmarks/benchmark_registry_v0.2.csv`), independently recomputed

| id | our statistic | published | Δ | tol | verdict |
|---|---|---|---|---|---|
| B001 primary NAR (ages 6–11, any-level current attendance) | 74.65 | 72.8 | +1.85 pp | ±2.5 | **MATCH** (definitional: any-attendance vs attending-primary NAR) |
| B002 male | 73.23 | 72.0 | +1.23 pp | ±2.5 | MATCH (definitional) |
| B002 female | 76.14 | 73.5 | **+2.64 pp** | ±2.5 | **outside tolerance**; report as definitional gap (matches data-team/lead finding) |
| B003 secondary NAR | 60.18 | 42.0 | +18.2 pp | — | **NOT A VALIDATION** (any-level vs attending-secondary definitions); direction only |
| B004 urban / rural | 76.93 / 73.44 | 75.5 / 71.3 | +1.43 / +2.14 pp | ±3.0 | MATCH (definitional) |
| B005–B008 (PH/ID/VN E1–E8) | — | — | — | — | **PENDING**; results carry `not_externally_benchmarked=true`, no validation claim |

## 8. Coverage matrix (engine outputs, frozen merged input)

Runnable cells in the current 14-survey merged layer: E1 7, E2 8, E3 8, E4 6, E5 6, E6 8 (person
definition), E7 6, E8 6 = **55 experiment-cells** (matches scout). The extension's 96 feasible cells
add VN (1997/2002/2005ais), older ID (1991/94/97/2002-03/2007/2012) and PH (1993/98) attendance cells
via `hv110`, subject to wealth availability (E1) and design blocks (PH 2003, PH 2008/2013).

## 9. Sign-off per experiment

| experiment | definition | status | conditions |
|---|---|---|---|
| **E1** attendance by wealth (persons 14–17) | README v1 | **SIGNED OFF (descriptive)** | wealth absent in KH 2000, ID 1991/94/97, PH 1993/98, VN 1997/2002 → not computable there; PH 2003 blocked (design); benchmark PENDING |
| **E2** attendance by residence | README v1 | **SIGNED OFF (descriptive)** | uses `hv110` where `hv121` absent (adjudication A); PH 2008/2013 blocked (attendance absent); benchmark PENDING |
| **E3** attendance by sex | README v1 | **SIGNED OFF (descriptive)** | as E2; 2 person rows with missing sex excluded and counted |
| **E4** children ever born by schooling (women 40–49) | README v1 | **SIGNED OFF (descriptive)** | only KH 5 waves + PH 2022 (IR/WI availability); benchmark PENDING |
| **E5** birth before 20 by schooling (women 25–34) | README v1 | **CONDITIONAL** | **blocked on frozen per-file layer** until verified-never is encoded (condition C3); merged layer has 99=never and is usable; benchmark PENDING |
| **E6** current school participation (women 20–24) | **person-record definition (D-01 approved)** | **SIGNED OFF (descriptive, definitional deviation)** | PR females 20–24, `hv121`/`hv110`, person weight; report as deviation from README; 2 lonely-PSU cells flagged in scout layer, canonical engine handles full-design |
| **E7** union before 20 by schooling (women 25–34) | README v1 | **CONDITIONAL** | as E5 (V511 blank = never in the frozen layer) |
| **E8** current household size by schooling (women 40–49) | README v1 | **SIGNED OFF (descriptive)** | current household size only — **not kin support**; benchmark PENDING |

## 10. Sign-off conditions (binding for execution)

1. **Engine pin:** execution must use `qa/experiments_v2.R` sha256
   `46c490652ea9893ce4e2418216c545dc74692a0bd25937da61ec046bc4e78f45`; any change invalidates this sign-off.
2. **Domain variance:** full-design NA-indicator per-group `svymean` only (not `subset()`/`svyby` on the
   subset); lonely-PSU policy primary `adjust` with sensitivity `certainty`/`remove`, ledger hash in the
   manifest, affected cells flagged (D-07).
3. **Never-vs-unknown encoding (blocking for E5/E7 on frozen per-file data):** the frozen per-file
   layer encodes verified never as blank/NA (0 rows with 99) while the README requires 99 = never;
   the engine correctly treats NA as unknown, so E5/E7 on the frozen layer would exclude never women.
   Data team must encode verified never as 99 (or provide a documented rule); until then E5/E7 must
   run from the merged layer (99 preserved).
4. **Disclosure/reliability:** suppress n<30 OR n_psu<2 OR df<1 OR non-finite SE; flags n<50, RSE>25/30%,
   df<30; suppressed-cell ledger retained (adopted deviation from starter's 50-case status gate).
5. **Benchmarks:** only the KH 2021-22 FR377 NAR family is validation-graded (B001 MATCH +1.85 pp;
   B002 female outside +2.64 pp → report definitional gap; B003 excluded as validation); all other
   estimates are `not_externally_benchmarked=true` with no validation claim.
6. **Exploratory only:** no causal/inferential claims (schooling may postdate early birth/union; E8 ≠
   kin support; wealth ≠ income; cross-sectional). BH q-values are transparency only.
7. **Coverage:** extension must run all 96 feasible cells through the pinned engine; scout's 55-cell
   pass is exploratory with attribution (point estimates verified; SEs/contrasts not execution-grade).
8. **BLOCKED coverage:** PH 2003 (hv022 missing), PH 2008/2013 E1–E3 (attendance absent); availability
   matrix to be corrected.
9. **Data handling:** no restricted microdata off this Mac; box not used; outputs are non-disclosive
   aggregates only.

## 11. Artifacts / hashes

| artifact | path | sha256 |
|---|---|---|
| canonical engine | `qa/experiments_v2.R` (= `experiments.R`) | `46c490652ea9893ce4e2418216c545dc74692a0bd25937da61ec046bc4e78f45` |
| original v1 | `qa/original/experiments.R` | `6705c9ec3a4b8cee2bb8b1c34d36a0dfb58e1dae0e26059d4545f96a3f3da817` |
| test runner | `qa/qa_tests.R` | `46f594fdaf4a970d0b5df77583fb2d6b943a9cd609b88dda228ec99628c02ea1` |
| singleton ledger | `qa/singleton_ledger.csv` | `2a6aad847720677550b4e482f7bcf85ec7423dfa505b7e9d96b0fa413886f66f` |
| hashes file | `qa/engine_hashes.txt` | — |
| synthetic harness output | `qa/logs/results.csv`, `qa/logs/results.txt`, `qa/logs/harness_stdout_local.txt` | — |
| real-data audit | `qa/logs/real/real_data_audit.json`, `experiment_readiness.csv` | — |
| D-07 sensitivity | `qa/logs/real/singleton_sensitivity_summary.csv` | — |
| benchmark v0.2 | `qa/logs/real/benchmark_check_v02.csv` | — |
| scout audit | `qa/logs/real/scout_audit_summary.json`, `scout_audit_recompute.csv` | — |
| defects | `qa/DEFECTS.md` | — |
| sign-off JSON | `qa/QA_SIGNOFF.json` | — |

## 12. Residual limitations

Synthetic fixtures validate the machinery, not real-world design subtleties; domain-definition
comparability with published tables is limited (NAR vs any-level attendance); the 55-cell scout run
remains exploratory; E5/E7 on the frozen per-file layer are blocked by the never-encoding issue;
benchmarks are KH-only; survey weights are used as released (normalised by 1e6), with no calibration
to published totals beyond the manifest's weight-sum evidence.
