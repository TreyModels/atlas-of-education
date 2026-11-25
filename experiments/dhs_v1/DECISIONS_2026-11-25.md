# DHS fleet — decisions log, 2026-11-25 (interim, pre-execution)

**Lead:** `deepseek-dhs`. **Status:** E1–E8 not executed; QA sign-off pending. These decisions are binding for
the run and are pre-declared (recorded before estimation).

## D-01 E6 definition (approved, supersedes starter)

The starter specified E6 on `record_type='woman'` with `currently_in_school`. No delivered IR/WI recode carries a
current-school item, so E6 as specified is **unrunnable** on the available data. **Decision:** E6 becomes a
person-record domain of females aged 20–24 (PR `hv121`, household/person weight `hv005`); documented as a
person-record definitional change. If an IR/WI current-school item is verified to exist, it is run only as a
documented sensitivity, never as the primary. Rationale: keeps the age domain and outcome concept, uses the
design variables actually present; avoids silently dropping E6.

## D-02 Domain variance estimator (with Monte-Carlo evidence)

QA D1 is **confirmed**: `subset.survey.design` is `x <- x[r, ]` and drops PSUs with no domain members; correct
domain estimation must retain the full design. Adjudication by synthetic two-stage Monte-Carlo (600 reps small
design; 300 reps 20 strata × 5 PSUs):

| estimator | mean SE (small design, empir. sd 0.447) | mean SE (larger design, empir. sd 0.206) |
|---|---|---|
| `svymean(~y, subset(des, dom))` | 0.427 | — |
| `svymean(~y, des, subset=dom)` | 0.300 | 0.150 |
| **NA-indicator, full design, `na.rm=TRUE`** | **0.427** | **0.212** |

**Decision:** use the NA-indicator full-design estimator (per-group `svymean` loop over the full design, outcome
set to NA outside the domain), not `svyby` on a subset and not `svymean(..., subset=)`. QA must add this
Monte-Carlo comparison as a fixture and document it in DEFECTS.md/QA_REPORT.md. (No estimator is asserted
"correct" on theory alone; the choice is empirically benchmarked and will be re-checked in QA T04/T05.)

## D-03 Disclosure/reliability rule (adopted, pre-declared)

Suppress a cell when `n_unweighted < 30` OR `n_psu < 2` OR `design_df < 1` OR SE non-finite. Additionally flag
(not suppress) `n_unweighted < 50`, RSE > 25 %, `design_df < 30`. Keep a suppressed-cell ledger by reason.
This is stricter than the starter's status-only 50-case rule; the deviation is deliberate and recorded.

## D-04 Benchmarks (partial availability, no invented values)

`benchmarks/benchmark_registry_v0.1.csv`: KH 2021-22 DHS FR377 Table 2.12 values are AVAILABLE
(primary NAR 72.8; M 72.0/F 73.5; secondary NAR 42.0; urban/rural 75.5/71.3) with a **definitional caveat** —
prior HV121∈{1,2} any-attendance extract gives 74.7, so comparison tolerance ±2.5 pp and direction of the
definitional gap must be reported. PH/ID/VN and E4–E8 rows are **BENCHMARK-PENDING**; results without a matching
published table carry `not_externally_benchmarked=true` and no validation claim. Data team may fill PENDING rows
only from public report tables with exact citations; prior-run numbers are not published benchmarks.

## D-05 Directory ownership

`experiments/dhs_v1/harmonize/` = data team; `experiments/dhs_v1/qa/` = QA (including `experiments_v2.R` +
`run_tests.R`, adopted from the scout draft, provenance noted); `benchmarks/`, `runs/`, top-level docs = lead;
`runs/` only written by the lead's execution harness.

## D-06 Execution gate

No E1–E8 estimation runs until QA posts **QA-SIGNED-OFF** with: DEFECTS.md, full QA_REPORT.md, synthetic test
results (T01–T20 incl. T20 domain-variance), sign-off checklist, and confirmation that the fixed engine reproduces
the benchmark registry within tolerance. Data availability/adapters and benchmark registry v0.2 are prerequisites
for the run script, not for sign-off.

## Status at logging

* Data team: `harmonize/` adapters produced; normalized_all.csv 939,684 rows / 14 survey-records independently
  audited by QA with 0 discrepancies; no singleton strata found; 99-known-never preserved.
* QA: code review D1–D10 (D1 verified by lead); synthetic fixtures mostly passing; T04/T05 under debug.
* Lead: local R 4.5.3 + survey 4.5 ready; benchmark registry v0.1; matrix inventory + schema v0.1 committed
  (`5a8fa2b`); rules in force (no causal language, no restricted data off-Mac, no synthetic data as real).


## D-07 Singleton-PSU treatment (pre-declared; blocking)

Data-team audit found singleton-PSU strata in PH 2008 (19), VN 1997 (1), VN 2002 (1), ID 2007 (1); all other 24
normalized files have none. QA's earlier "none" is to be reconciled (likely caused by auditing the merged
`normalized_all.csv`, where file-level PSU/stratum codes are not preserved). The README requires investigating
the design rather than quietly changing options, so the treatment is **pre-declared here**:

* **Primary:** `options(survey.lonely.psu = "adjust")` — singleton strata are centred at the population mean and
  contribute no between-PSU variance; every affected cell is flagged with the count of singleton strata included.
* **Sensitivity:** repeat affected cells with `"certainty"` (and, where feasible, `"remove"`); report the range of
  estimates/SEs. No cell may be interpreted if the primary/sensitivity range crosses the suppression/reliability
  thresholds.
* **Pre-flight:** a machine-readable `singleton_ledger.csv` (file, stratum, PSUs) must exist in `qa/` and be
  reproduced by the run harness manifest before any estimation.
* PH 2008's 19 singleton strata are outside the feasible cells (attendance absent) but remain in the ledger.

## D-08 Accepted coverage corrections (data team, verified)

* `WI` files are **wealth-index** files, not woman recodes ⇒ **E4/E5/E7/E8 = KH 5 waves + PH 2022 only**.
* **VN E2/E3 are FEASIBLE**; E1 needs wealth and is feasible only where wealth exists (ID 2002-03+, PH 2003/2017/
  2022, VN 2005ais, KH 2005+); PH 2008/2013 E1–E3 blocked (attendance absent); E6 is the person-record domain.
* 96 feasible cells of 176 wave×experiment cells; `AVAILABILITY_FINAL_2026-11-25.md` is the execution source of truth.
* Benchmarks: KH 74.65 vs published NAR 72.8 (+1.85 pp, inside ±2.5 pp) recorded; B002 F is +2.64 pp (report the
  definitional gap); B003 excluded as validation (level-specific vs any-level); B005–B008 remain BENCHMARK-PENDING.
