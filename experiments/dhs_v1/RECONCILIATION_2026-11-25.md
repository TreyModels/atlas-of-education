# DHS reconciliation — scout pass vs QA-gated pipeline (2026-11-25)

**Owner:** `deepseek-dhs` (lead). **Scope:** reconcile the scout subagent's serial execution pass (commits
`af89b4b`, `766e9e4`, Bridge `51cdff15`) with the lead-owned QA-gated pipeline, resolve worktree ownership, and
define the single execution-evidence set for milestone 2. **Nothing here is adopted as final evidence until QA
signs off; all scout numbers are labelled EXPLORATORY-CANDIDATE.**

## 1. What the scout produced (verified on the branch)

* `engine/` — candidate execution engine: `experiments_v2.R` (corrected engine, `--lonely=fail|adjust|remove`,
  recorded policy), `contrasts.R` (design-based contrasts), `run_tests.R` (14/14 synthetic tests), 
  `validate_benchmarks.R`, `summarise.py`.
* `harmonize/harmonize.py` — scout's own 14 adapters (attendance via `HV121` only) + `harmonize/aggregate_layer.py`.
* `runs/2026-11-25_all/` — candidate results: `estimates.csv` (155 estimates / 55 experiment-cells),
  `status.csv` (55 ok, 8 no-records, 1 insufficient), `contrasts.csv`, `SUMMARY.md`, `hashes.txt`.
* `REPORT.md`, `ADAPTERS.md`, `ADDENDUM.md` — results, per-file recode evidence, model-mapping addendum
  (states Domus v44 / 150-equation inventory / prior dense matrix have **no artifact in this checkout** — honest,
  and consistent with milestone-1 inventory M10/M4 living on other branches/worktrees).

Attribution: produced by the scout subagent (`b8e998db`) serial pass, on this branch, while the durable data/QA
teams were active. The scout has been told to stop writing; the branch is owned by this lead.

## 2. Ownership resolution (D-09)

| path | owner | status |
|---|---|---|
| `experiments/dhs_v1/engine/` | scout artifacts, **adopted** by lead with attribution | candidate execution engine; may be superseded by QA verdict |
| `experiments/dhs_v1/runs/2026-11-25_all/` | scout artifacts, **adopted** by lead with attribution | EXPLORATORY-CANDIDATE estimates; not final evidence |
| `experiments/dhs_v1/qa/` | QA (`qa-verifier`) exclusively | QA reference engine + fixtures + audits |
| `experiments/dhs_v1/harmonize/` | data team (closed, frozen) | adapters + pinned per-file normalized outputs + ledger/run-map/hashes |
| `experiments/dhs_v1/runs/` (new dirs) | lead harness only | pinned, preflighted execution |
| `experiments/dhs_v1/integration/`, docs, benchmarks | lead | schema, prototype, decisions, registries |

Conflict resolved: QA's engine lives under `qa/` (adopted/contrasts.R); scout's under `engine/`; neither is
deleted. Research branch history retains both commits with messages; this file is the attribution record.

## 3. Coverage reconciliation (verified numerically)

* Scout: **55 ok experiment-cells** — KH 5 waves × E1–E8 = 40 cells minus KH-2000 E1 (blocked, no wealth) = 39;
  ID-2017 (E1/E2/E3/E6) = 4; PH-2017 (4); PH-2022 (8) → 55 (53 "ok" + 2 "ok with lonely PSU in domain");
  155 estimates.
* Data-team verified feasible matrix: **96 of 176 wave×experiment cells** (`AVAILABILITY_FINAL_2026-11-25.md`).
* **Scout cells ⊂ feasible cells** (0 scout cells infeasible). **41 feasible cells were not executed**, all
  leveraging `hv110` (current-attendance) rather than `hv121`:
  * ID 1991/1994/1997/2002-03/2007/2012 — E2/E3/E6 (and E1 for 2002-03/2007/2012);
  * PH 1993/1998 — E2/E3/E6; PH 2003 — E1/E2/E3/E6;
  * VN 1997/2002/2005ais — E2/E3/E6 (and E1 for 2005ais).
* **Conflict A (VN/older ID/PH attendance):** scout's adapters use `HV121` only and concluded "no attendance
  item" for VN and pre-2017 ID/PH; the data team's verified matrix shows `hv110` present and non-missing in those
  P1/P2 recodes and uses `attendance = hv110==1 where present`. Data-team reading is technically correct for the
  variable that exists; scout's conclusion is a **coverage bug**, not a wrong estimate. **QA must verify hv110
  semantics per wave** before extension execution.
* **Conflict B (PH 2003 design):** data-team matrix marks PH 2003 feasible, but its own availability row shows
  `hv022` present with **non-missing = 0** (variance stratum wholly missing). Scout excluded PH 2003 rather than
  substituting `HV023`. This looks like a **data-team matrix error**; QA must adjudicate (expected: BLOCKED unless
  `HV023`/design documentation justifies a documented substitution).
* **Consistent findings:** WI files are 3-column wealth stubs (scout and data team independently); E6 starter
  defect (person-record fix); `HV121` wave-specific coding; blank V212/V511 = verified never; PH 2008/2013
  attendance absent.

## 4. Adjudication and next steps

**D-09 (adopt, attributed):** the scout pass is adopted as the **exploratory candidate execution layer for its 55
cells** — no duplicate re-execution of those cells. Its estimates may be used as candidate evidence only after
QA's independent audit (code + numbers), and remain labelled `EXPLORATORY-CANDIDATE` until QA sign-off.

**D-10 (extension, not duplication):** the **41 unexecuted feasible cells** will be run on the frozen per-file
normalized inputs (`~/neon-boot/dhs-normalized`, data-team pinned hashes) through the QA-audited engine + lead
harness, after QA resolves Conflicts A/B. Extension is executed via `runs/run_all.py` (preflight pins inputs,
requires the singleton ledger, writes feasibility gaps and sha256 manifest) with `--lonely=adjust` primary and
`certainty`/`remove` sensitivity (D-07). If QA adopts the scout engine, the extension uses that engine; otherwise
the QA engine — decision pinned in `qa/QA_SIGNOFF.json`.

**D-11 (pending adjudications):** VN/ID/PH hv110 waves — PENDING QA semantics check; PH 2003 — PENDING design
verdict (expected BLOCKED). Neither is counted as evidence until resolved.

**D-12 (single evidence set):** milestone 2 evidence = scout 55 cells (candidate) + extension cells, all through
one post-processing layer (suppression D-03, BH multiplicity, benchmark registry v0.2, singleton ledger, sha256
manifest). No causal language; no panel/person links; wealth ≠ income; household size ≠ kin support.

**Milestone 2 structure (target):** unified `estimates_final.csv` (candidate+extension), cell status table with
BLOCKED reasons, benchmark table (KH NAR 72.8 comparison + pending), singleton treatment (22 strata ledger,
adjust/certainty sensitivity), coverage/missingness, limits section, and the L1 aggregate layer feed into the
L1→M6 prototype (re-run unchanged).

## 5. Open QA items this reconciliation feeds into

1. Audit the scout engine + estimates (independent recompute on a sample; verify HV121/HV110 coding, V212/V511
   never logic, WI stubs, design variables, weights, suppression, Holm).
2. Adjudicate Conflicts A and B with raw-data evidence and update the availability matrix if needed.
3. Verify scout's two-pipeline agreement claim (0.139 pp / 0.21 SE against the anchored Cambodia series) and the
   lonely-PSU handling of its two flagged cells.
4. Complete the remaining sign-off package (DEFECTS.md, QA_REPORT.md, T20 domain-variance Monte-Carlo, benchmark
   harness, engine path+sha256) and write `qa/QA_SIGNOFF.json` including the adopted-engine decision.
