# DEFECTS — DHS methods/QA review (v1 starter → QA-hardened engine)

**Owner:** `qa-verifier` (DHS methods/QA) · **date:** 2026-11-25
**Scope:** review of the v1 starter (`qa/original/experiments.R`, sha256
`6705c9ec3a4b8cee2bb8b1c34d36a0dfb58e1dae0e26059d4545f96a3f3da817`), the scout candidate engine
(`engine/experiments_v2.R`, attributed), and the QA-hardened canonical engine
(`qa/experiments_v2.R` == `experiments.R`, sha256 `46c490652ea9893ce4e2418216c545dc74692a0bd25937da61ec046bc4e78f45`).
Provenance: `qa/adopted/` holds the scout QA drafts (experiments_v2.R, run_tests.R, validate_benchmarks.R)
adopted into QA ownership and superseded by the consolidated engine + `qa/qa_tests.R`; they are kept for
history only, **not** execution candidates.

## A. v1 starter defects (file:line in qa/original/experiments.R)

| id | line(s) | defect | evidence / test | fix in canonical engine |
|---|---|---|---|---|
| D1 | 39,43 | `sub(design, domain)` re-creates a **domain-only design**: PSUs with no domain member are dropped. Domain variance/SEs are wrong (lead MC: subset SE understates; observed here: scout engine SEs deviate up to −8% / +40% vs full-design reference on 19/155 cells) and a genuine singleton stratum aborts the whole cell with only a generic "design error". | T05 (analytic stratified-PSU-total reference), T24 (MC), scout audit | full-design domain estimation: outcome set to NA outside the group-domain; per-group `svymean` on the design that keeps **all** base PSUs |
| D2 | 14 | `options(survey.lonely.psu='fail')` set globally, never restored, no pre-flight diagnostics or recorded policy; real singleton strata produce an opaque failure. | T04 | explicit `--lonely-psu=fail|adjust|certainty|remove` (default fail), pre-flight singleton list in status, policy + ledger hash in manifest; D-07 pre-declared primary `adjust` |
| D3 | 31,33,45 | missingness conflated: age-ineligible vs missing outcome vs missing group collapsed into one `complete_n`; no missingness table (README requires). | T21/T22 | `missingness.csv` with n_type_rows / n_age_eligible / n_complete / outcome-missing / group-missing / verified-never / unknown |
| D4 | 42 | per-group `complete_n` compares `z[[group]] == ans[j,1]`; factor/character coercion can silently give 0 counts | T21 | typed comparison on the analysis frame |
| D5 | 42 | no small-cell suppression / disclosure control, no RSE or design-df flags | T11/T12 | pre-declared rule: suppress n<30 OR n_psu<2 OR design_df<1 OR non-finite SE; flags n<50, RSE>25/30%, df<30; suppressed-cell ledger by reason |
| D6 | whole file | no multiplicity reporting for many experiment×country×wave tests | T13 | exploratory flag, BH q column, manifest multiplicity statement (descriptive only) |
| D7 | 7,10-13 | validation gaps: non-finite weights pass; no sex/age/school_years/CEB/household-size checks; no PSU→stratum mapping; no weight-variable provenance | T08/T09 | strict structural validation; DHS DK/sentinel codes mapped to NA with recorded warning; optional `weight_variable` validated (person vs woman weight labels must differ) |
| D8 | 7 | `na.strings` lacks `.` and other missing tokens | T08/T09 | extended missing tokens |
| D9 | 42 | normal 1.96 CI with no design df reported | estimates schema | `design_df`, `ci_method`, df<30 caution flag |
| D10 | 47-49 | no run manifest/hashes/benchmark hook | T14/T15/T16/T25 | manifest.json (input+script sha, R/survey versions, design vars, weight provenance, policy, singleton ledger hash, benchmark coverage), optional `--meta`, `--benchmarks` |

## B. E6 definitional change (lead decision D-01, approved)

v1/README specified **E6 = woman record + `currently_in_school`**. No DHS IR/WI recode carries a
current-attendance item; on the delivered data the variable is non-missing for **0** woman rows in all 6
IR files (independent audit). The canonical engine therefore implements **E6 = person-record domain:
females aged 20-24, PR `hv121`/`hv110`, person weight `hv005`**, explicitly labelled as a deviation
(`--e6=woman` retained for comparison only). This is the sign-off basis; results must be reported as the
person-record definition, not the v1 woman-recode definition.

## C. Scout candidate engine (`engine/experiments_v2.R`, attributed, EXPLORATORY only)

| id | defect | evidence | consequence |
|---|---|---|---|
| S1 | **retains D1**: `dsub <- subset(des, .dom)` then `svyby(..., dsub, ...)` | code line 133/136; independent recomputation: SE(scout)/SE(full-design) median 1.0016, but 19/155 cells >10% off (up to +40% conservative), 1 cell −8% | point estimates sound; **CIs/p-values/contrasts need regeneration** through the canonical engine before execution evidence |
| S2 | **coverage bug (Conflict A)**: used `HV121` only and concluded VN + pre-2017 ID/PH have "no attendance item" | frozen per-file data: attendance non-missing and age-profile-valid via `hv110` in VN 1997/2002/2005ais, ID 1991/94/97/2002-03/2007/2012, PH 1993/98/2003 (share ages 9-14 = 0.85–0.95, ages 25-49 ≈ 0); data-team matrix shows `hv110` present with non-missing counts >0 | 41 feasible cells unexecuted; scout pass covers 55/96 cells only (exploratory) |
| S3 | run_meta records `lonely_policy: 0` (not the named policy) and 2 cells "ok with N lonely PSU in domain" without pre-flight ledger | `runs/2026-11-25_all/run_meta.txt`; singleton ledger has 22 strata (PH2008 19, VN1997 1, VN2002 1, ID2007 1) | audit trail incomplete; recomputed SEs for those 2 cells are within 0.3% of full-design, so impact is small but the policy record is defective |
| S4 | ran on the merged `dhs8_local/normalized_all.csv` (14 survey-records) rather than frozen per-file inputs | run_meta input path/sha | merged layer does not preserve file-level PSU/stratum identity; coverage and singleton accounting must be done per file |

**Scout verdict:** point estimates **SOUND** (155/155 verified; 154 match to <1e-6; 1 differs by
0.013 pp because 1 implausible age-9 first-birth record is handled differently), inference SEs
**partially biased** (S1), coverage **incomplete** (S2). → scout pass is retained as
**EXPLORATORY-CANDIDATE**, not execution evidence; extension must run all 96 feasible cells through the
pinned canonical engine.

## D. Data-layer finding (blocking for E5/E7 on frozen per-file inputs)

The two delivered layers disagree on the README rule "99 = known never; NA = unknown":
* merged `dhs8_local/normalized_all.csv`: `age_first_birth/union` 99 = known never (KH2000 woman: 5,421/4,646),
* frozen per-file `dhs-normalized/**`: never recorded as **blank/NA** (KH2000 woman: 5,421 blank, **0** rows
  with 99), and blank V212/V511 are verified never (blank V212 ⇔ CEB=0, 0 violations across 6 IR files).

The canonical engine treats NA as unknown (README), so running E5/E7 on the frozen per-file layer as
delivered would **exclude never-birth/never-union women** and bias the early-birth/union means upward.
**Condition:** data team must encode verified never as 99 in the per-file layer (or provide an explicit
documented rule); until then E5/E7 must run from the merged layer (where 99 is preserved).

## E. Verified traps (scout claims independently checked)

| trap | verdict | evidence |
|---|---|---|
| HV121 wave-specific coding; code 2 = *currently attending* | **CONFIRMED** | data-team raw scan declares code 1 (KH2000) / 2 (KH2005+) per wave; recoded attendance age profile: share ages 25-49 = 0.000 and ages 9-14 = 0.76–0.97 in every file |
| blank V212/V511 = verified never | **CONFIRMED (semantics), but layer encode differs from README** | blank V212 iff CEB=0 (0 violations, 6 IR files); merged layer uses 99, frozen per-file layer uses blank → see §D |
| WI files are 3-column wealth stubs (`whhid`,`wlthindf`,`wlthind5`) | **CONFIRMED** | `pandas.read_stata` on `pulled/dhs/indonesia/1997/IDWI3ADT/IDWI3AFL.DTA` → exactly 3 columns; no WI outcomes → E4–E8 only KH 5 waves + PH 2022 |

## F. Adjudications requested by the lead

* **Conflict A (coverage / hv110): scout is WRONG.** `hv110` ("member still in school") is present and
  non-missing in VN 1997/2002/2005ais, ID 1991/94/97/2002-03/2007/2012 and PH 1993/98/2003 (frozen
  per-file attendance non-missing 26,826–177,818 rows, correct age profile; data-team availability matrix
  records `hv110` non-missing counts). Attendance is therefore available there; the 41 unexecuted cells
  in the extension are feasible (design permitting).
* **Conflict B (PH 2003 design): scout is RIGHT; the data-team availability matrix is wrong.** PH 2003
  `hv022` (variance stratum) is non-missing on **0 of 61,864** rows (PSU `hv021` present, 819 PSUs); the
  canonical engine refuses it with "missing stratum". No documented justification exists to substitute
  `hv023`. Verdict: **PH 2003 BLOCKED**; availability matrix should be corrected. PH 2008/2013 E1–E3 are
  also blocked (attendance absent, 0 non-missing) despite wealth being present.

## G. Pre-declared methodological choices (lead-approved)

1. **Disclosure/reliability rule (D-06):** suppress when `n_unweighted < 30` OR `n_psu < 2` OR
   `design_df < 1` OR non-finite SE; flags for n<50, RSE>25/30%, df<30; suppressed-cell ledger kept.
   This deliberately replaces the starter's status-only 50-complete-case gate (which is retained as the
   analysis-eligibility gate in addition).
2. **Lonely-PSU policy (D-07):** primary `options(survey.lonely.psu="adjust")`; sensitivity
   `"certainty"` (and `"remove"` where feasible). Pre-flight ledger required in the manifest; affected
   cells flagged with their singleton count. Empirically the policy choice is immaterial here: across
   the affected feasible files (VN 1997/2002, ID 2007) estimates are identical and SEs differ by
   ≤7.4e-5 across adjust/certainty/remove.
3. **Domain variance estimator (D1/D-06):** full-design NA-indicator per-group `svymean`, justified by
   an independent stratified-PSU-total reference (T05) and Monte-Carlo (T24): NA-indicator matches the
   empirical SD of the domain mean, while `subset()`-based SEs are biased (lead MC: 0.212 vs subset
   0.150–0.427 vs empirical 0.206–0.447 across configurations).
4. **Multiplicity:** all results exploratory; BH q-values reported for transparency only; no
   confirmatory discovery claims. No causal language: schooling may postdate early birth/union; E8 is
   current household size, not kin support; wealth is a relative index, not income.
5. **Benchmarking:** only the KH 2021-22 DHS FR377 Table 2.12 NAR family is externally validation-graded
   (primary 74.65 vs 72.8 = +1.85 pp inside ±2.5; male inside; female +2.64 pp outside → definitional
   gap reported; secondary NAR excluded as validation — definitional mismatch, direction only).
   PH/ID/VN and E4–E8 are **BENCHMARK-PENDING**; results carry `not_externally_benchmarked=true` and no
   validation claim.
