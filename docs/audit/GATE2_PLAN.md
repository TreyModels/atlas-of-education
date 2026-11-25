# GATE-2 PLAN — calibration on the repaired engine (PREPARATION ONLY; NO RUNS STARTED)

**Status: BLOCKED — GO, CONDITIONAL. Nothing in this plan may be launched** until all three preconditions hold:
- **(a) Canonical spec frozen by the operator.** Recommended (Lead): freeze the **540 parameterisation on the
  repaired engine**, with explicit `GATE_SPECS`: **KR-TRACKED primary, KR-SINGLE sensitivity**, and the **420
  generation documented as the alternative** (not run in Gate 2 core).
- **(b) Runner hardening (`task-13`, audit-runner) reported green** — incremental checkpointing/resume, atomic final
  assembly, collection-phase watchdog, process-group kill semantics, memory-aware worker caps.
- **(c) A7 residual declared in the Gate-2 plan** (see §7).

Owner: `atlas-commander` (execution). Evidence taxonomy: every number produced in Gate 2 must carry one of
VERIFIED EMPIRICAL / REPRODUCED SIMULATION / VALIDATED SIMULATION / AUTHOR-REPORTED / CONTRADICTED / UNRESOLVED.

---

## 1. What must be frozen before the first calibration run (G2-A artefact)

A single `docs/audit/CANONICAL_SPEC.md` + machine-readable `canonical_spec.json` containing:
1. **Code**: commit hash of the audit branch; sha256 of `engine/eduengine/{core,rng,contest_math}.py`,
   `modules/{tutoring,labour,schools}.py`, `planning.py`; whether task-12 memo module is in (bit-identical outputs,
   so declares numerics).
2. **Environment**: `/root/work/venv-declared` pip freeze hash (numpy 2.2.6/scipy 1.15.3), box cgroup 10 CPUs,
   BLAS/OMP=1, worker policy.
3. **Parameters**: full parameter dict, including gate list (`GATE_SPECS['KR-TRACKED']` primary; KR-SINGLE
   sensitivity), levels, N, T, measure_from, seeds (matched seed list), and every legacy-neutral default.
4. **Data**: the benchmark registry (below) with citation + survey year + population + denominator; **no target
   without a source**; derived targets marked as targets, not observations.
5. **Pre-registration**: selection rule, score function, training/holdout split, pass/fail criteria, number of runs,
   and what will be reported even if it fails (preserve inconvenient results).
6. **Known limitations**: 420 generation AUTHOR-REPORTED; GPU/ABC claims QUARANTINED; pool-hang risk; engine cost.

**Stop rule for G2-A:** no calibration run starts until the spec file + registry are committed and Lead-approved.

## 1b. Canonical-spec decision (OPEN — draft both variants, do not presuppose)

The operator has not yet chosen the canonical spec. Both variants are drafted here so the decision is cheap:
* **V540-freeze (Lead recommendation):** the 540 parameterisation (N=300, T=46, measure_from=18; HK/KR base params
  as in the legacy runner) on the repaired engine, with explicit `GATE_SPECS` — **KR-TRACKED primary** (G9 selective
  placement: share 0.35, quality_mult 1.10, earnings_logw 0.15, g12_track_bonus 1.25) and **KR-SINGLE sensitivity**
  (G9 open); HK unchanged. Rationale: Gate-1 migration table is already measured on this spec
  (`GATE1_MIGRATION_TABLE.md`), it is the reproduced artifact, and the CF4 flip is characterised on it.
* **V420-port (documented alternative):** the 420 generation (N=400, T=70; y_median 3.0, subsist 0.15, borrow 0.5,
  contest_alpha 1.2/1.25, price .12/.11, max_e 4.0/4.5, elite_logw .85/1.15, bar gates 0/0/0) ported to the
  repaired engine. Evidence for this variant is **AUTHOR-REPORTED / PRE-REPAIR / UNCALIBRATED** (legacy branch
  `d20ba6e`, calibration **FAILED**: untuned 66.27 %/80.77 pp/5.32×; best grid 91.63 %/37.11 pp/1.59× vs targets
  76.5/32.1/3.4 — see `harvest/HARVEST.md` §4). Cost ≈2× V540 (see §2).
**Decision status: DECIDED (operator, 2026-11-25): V540-FREEZE.** Frozen artefact `docs/audit/canonical_spec.json`
(content sha256 `c5f9e2de…4a05`, file `35576fed…7b95`); GATE_SPECS KR-TRACKED primary / KR-SINGLE sensitivity; 420
is a documented alternative only (no 420 port work). New-generation campaign preregistered in
`docs/audit/GATE2_PREREGISTRATION.md` (frozen before launch).

## 2. Measured compute budget (do not plan on a hoped-for speed-up)

Measured on the repaired engine (`98baf6b` + task-12 memo): **HK ≈20.3 CPU-s/run, KR ≈41.9 CPU-s/run**
(540-class ≈ **4.66 CPU-h**; box observed 49.3 min at 6 workers). Task-12 shipped memo-only gives **1.113×**
end-to-end (bit-identical); **2–5× is UNPROVEN**. Levers (not assumed): tutoring prep grid 9→5 ⇒ ~1.7×, 9→4 ⇒
~2.0× (tutoring-numerics decision); compiled kernel 5–10× (violates pure-NumPy). If the canonical spec is the
**420 generation (N=400, T=70)**, per-run cost scales ≈ (400/300)·(70/46) ≈ **2.0×** ⇒ ~9.4 CPU-h per 540-class.
All estimates below assume the 540 spec and **no** speed-up beyond the shipped 1.113×.

| stage | design | runs | CPU-h (×1.113 only) | wall @10 CPUs (×1.5 overhead) |
|---|---|---|---|---|
| G2-B pilot | 500 candidate configs × **3 matched seeds** | 1,500 | **13.0** | ~1.9 h |
| G2-C search | 5,000 candidates × **5 seeds** | 25,000 | **216** | ~32 h |
| G2-D refine | top 100 × **30 matched seeds** | 3,000 | **26** | ~3.9 h |
| G2-E final held-out | ~60 selected specs × 30 seeds | ~1,800 | **15.5** | ~2.3 h |
| **total core** | | ~31,300 | **~271 CPU-h** | **~40 h** |

**Lead budget decision (2026-11-25):** the full staged budget above is **APPROVED** (≈271 CPU-h, ~40 h wall at 10
CPUs), **conditional on two stop gates**: (i) G2-A identifiability rank adequate or the system pre-registered
reduced; (ii) G2-B pilot finds **≥5 candidates inside the declared bands**. If either fails, **stop and report** —
do not spend the ~216 CPU-h search. The **reduced 1,000×5 search (~6.5 h wall at 10 CPUs)** is documented as the
operator's faster alternative and is being put to the operator alongside the canonical-spec decision.

Budget notes: (i) search stage is the dominant cost — a 5,000×5 grid is ~9 days of single-core work; it is feasible
on the 10-CPU cgroup only at ~2 days wall, or must be reduced (e.g. 1,000×5 ≈ 4.3 days single-core → ~6.5 h at 10
CPUs); this reduction is a Lead decision. (ii) policy-arm re-runs are **Gate 3**, not in this budget. (iii) if the
canonical spec is the 420 generation, multiply by ≈2.0.

## 3. Staged design (Lead-specified shape, with acceptance rules)

1. **G2-B pilot (500×3)** — purpose: identify the feasible region, detect degeneracy/identification problems, and
   validate the benchmark registry parsing; **stop rule**: if <5 candidates inside the declared score bands, report
   and stop (do not proceed to search); output a Pareto table + seed-SE.
2. **G2-C search (5,000×5 or Lead-reduced)** — purpose: locate candidate optima on the pre-declared score
   (e.g. S = ((part−76.5)/2.8)² + ((gap−32.1)/3.0)² as used in the legacy pre-registered sweep, **to be
   re-declared** in G2-A); holdout moments are NOT used to fit.
3. **G2-D refine (100×30)** — re-simulate the top 100 with 30 matched seeds; report seed uncertainty separately
   from calibrated-parameter uncertainty.
4. **G2-E final held-out** — evaluate the selected specs on held-out empirical moments (declared in G2-A); report
   pass/fail against pre-stated tolerances; preserve failures.
5. **G2-F report** — calibration report + updated registry + evidence ledger; no policy claims (that is Gate 3).

## 4. Benchmark registry requirement (mandatory)

`docs/audit/GATE2_BENCHMARK_REGISTRY.csv` (draft committed) must, before G2-B, contain for **every** moment:
**citation, survey year, population, denominator, value, unit, source artifact, evidence status**. No derived target
may be presented as an empirical observation. The draft has 8 rows (Korean participation 2024/2025; HK Grade 9 /
Grade 12 participation; Korean Q5−Q1 gap target; Korean Q5/Q1 spend-ratio target; participation target; HK grade
targets); **all are currently AUTHOR-REPORTED / pending citation** — Gate 2 must verify each against the actual
survey source or demote it to UNRESOLVED and drop it from the training set.

## 4b. Pre-declared calibration moments and tolerances (before any run)

Every moment below has a row in `docs/audit/GATE2_BENCHMARK_REGISTRY.csv` with claim, jurisdiction, survey year,
population/denominator, outcome definition, source+citation, uncertainty, and permitted use. **Rows with incomplete
citations are provisional and must be verified or demoted to UNRESOLVED before G2-B.**

**Definition discipline (binding):**
* Never pool survey years or jurisdictions: Korea 2024 and Korea 2025 are separate moments; HK 2011/12 is a third,
  separate dataset. No "contemporary cross-country benchmark".
* Never mix **household income brackets** with the model's **simulated ability/income quintiles** (`k['q']`):
  the simulated `q` is a cohort ability/income proxy; the empirical target is by household income bracket. G2-A must
  declare the mapping (or use a bracket-matched model statistic) before fitting.
* Never mix **per-student** and **per-participant** expenditure. The legacy spend-ratio target (3.4×) is a
  **per-student** ratio; if only per-participant data exist, the target must be re-derived, not re-labelled.
* No derived target may be counted as an independent empirical moment (participation target 76.5 % overlaps the
  2024/2025 survey rows; the gap and spend-ratio targets are derived).

| moment | role | tolerance / uncertainty handling |
|---|---|---|
| KR overall participation 2024 = 80.0 % | calibration | survey uncertainty to be sourced; fit tolerance declared in G2-A (provisional ±2.8 pp) |
| HK Grade 9 participation 2011/12 = 53.8 % | calibration | survey uncertainty to be sourced; provisional tolerance ±5 pp |
| KR Q5−Q1 participation gap = 32.1 pp (household income brackets) | calibration | target tol 3.0 pp; **empirical source must be located or moment dropped** |
| KR Q5/Q1 per-student spend ratio = 3.4× (household income brackets) | calibration | target tol 0.5×; **empirical source must be located or moment dropped** |
| KR overall participation 2025 = 75.7 % | **held-out** | never used in fitting; scored out-of-sample |
| HK Grade 12 participation 2011/12 = 71.8 % | **held-out** | never used in fitting; note same survey as G9 (declare dependence) |

At least **two held-out moments** are reserved (KR 2025 participation; HK Grade 12).

**Same-instrument dependence (Lead-required declaration).** KR 2024 (calibration) and KR 2025 (held-out) are
**adjacent years of the same KEDI instrument** — 2025 is a **temporal holdout, NOT an independent validation**;
correlated sampling/instrument error means it cannot certify external validity. Likewise HK Grade 9 (calibration)
and HK Grade 12 (held-out) come from the **same 2011/12 survey** and are dependent moments. The calibration report
must state this and treat held-out success as temporal/within-instrument evidence only. No pooling across years or
jurisdictions, ever.

**Citation verification is a HARD GATE (G2-A).** Each empirical moment must be verified against the actual survey
source (KEDI 2024/2025; HK 2011/12 survey) with citation, survey year, population and denominator recorded. **Any
moment that cannot be sourced is demoted to UNRESOLVED and dropped from the training set**; the calibration report
states the reduced training set explicitly. No improvised substitute, no relabelling, no borrowed number.

**The 76.5 % blended participation target is DIAGNOSTIC ONLY** (`KR_part_target_76_5` in the registry): it overlaps
the 2024 and 2025 survey rows and must **never enter the fit**. Calibration moments are only: KR 2024 = 80.0 %,
HK Grade 9 = 53.8 %, KR Q5−Q1 gap = 32.1 pp, KR Q5/Q1 per-student spend ratio = 3.4× — each conditional on its
citation verifying.

**`k['q']` mapping (hard declaration).** The model's `k['q']` is a simulated cohort ability/income quintile, NOT an
empirical household-income bracket. Before fitting the bracket-based gap and spend-ratio targets, G2-A must declare
the mapping and choose a bracket-matched model statistic (e.g. map simulated `q` to income brackets via the model's
income distribution and verify the match), or drop the bracket-based targets. No silent substitution of quintile
definitions.

**Per-student vs per-participant (hard declaration).** The 3.4× spend-ratio target is a **per-student** ratio. If the
verified source provides only per-participant expenditure, the target must be **re-derived** from the source
(per-student = participation × per-participant) with the procedure recorded — never re-labelled.

## 4c. Identifiability assessment BEFORE joint estimation (ABC lesson, mandatory)

Before fitting, compute the **Jacobian J of the calibration map (parameters → the declared calibration moments)** at
the candidate parameter points, and report its **rank, singular-value spectrum and explicit null-space directions**.
Do not infer identification from a condition number (the ABC work showed a raw condition number of 7.03 can coexist
with rank 4/5 and a 2-dimensional null space; the prior-scaled condition number 10.41 was equally uninformative).
Requirements:
* rank must equal the number of jointly estimated parameters (or the system must be reduced and the reduction
  declared); if rank < #params, report the null space and **freeze/qualify** one direction rather than silently
  relying on a prior;
* include a local + finite-domain check (multiple starting points across the prior box), not a single point;
* if the moment map is not differentiable, use a finite-difference Jacobian with step-size sensitivity reported;
* the identifiability report is a G2-A artefact and a **stop gate**: no joint estimation until rank is adequate or
  the reduced system is pre-registered. **G2-A result (`G2A_IDENTIFIABILITY.md`): rank 4/4, null_dim 0 at 2 starts (multi-seed 5/column in `G2A_IDENTIFIABILITY_MULTISEED.md`; **item (d) PROVISIONAL — third start running on host**; stop gate requires ≥3 starts),
  BUT one-seed FD Jacobians are unstable (max|ΔJ| 26.5, rel 0.52) — G2-B MUST use multi-seed Jacobians with the
  registered step sizes (5 %/3 %/5 %/4 %) and ≥3 starts; no prior or condition-number inference;**
* it is computed **for the chosen canonical spec** (after the operator freezes V540-freeze or V420-port); drafting
  both variants in §1b is not a substitute for the chosen-spec Jacobian/rank/null-space artefact.

## 4d. Uncertainty reporting (separate, mandatory)

Two uncertainty objects are reported separately and never conflated:
1. **Monte Carlo / seed uncertainty**: standard deviation and 95 % CI of each moment across the 30 matched seeds
   (within-model stochasticity). Report n, sd, se.
2. **Calibrated-parameter uncertainty**: bootstrap over the calibration moments / survey sources (and over
   populations where applicable); report parameter CIs and the induced moment CIs.
The calibration report must state which CIs include which source; no single "CI" may mix the two.

## 5. Evidence ledger (mandatory)

`docs/audit/GATE2_EVIDENCE_LEDGER.md` (created at G2-A): one row per claim → status. Excluded from calibration
inputs by list:
* **QUARANTINED**: all GPU ABC / contest-surface / E1-Q3 conclusions (external audit `98baf6b`,
  `SCIENTIFIC_CLAIM_LEDGER.md`); the archived 100 % seat-expansion paradox (CONTRADICTED); the archived general-r
  Tullock map (UNVALIDATED; use corrected solver).
* **AUTHOR-REPORTED**: the 420-run generation and every Paper B table derived from it; legacy calibration-sweep
  numbers (PRE-REPAIR/UNCALIBRATED).
* **UNRESOLVED**: Paper A Exp 1/3/4/5 simulations, GPU outputs, the original 420 generation environment.
* Derived DGP/bootstrap findings are **REPRODUCED SIMULATION** design diagnostics, not empirical moments.

## 6. Runtime hardening dependency (task-13) — blocking

Gate 2 must not launch on the unhardened runner: the full-540 completion-phase hang occurred twice on the host
(all worker compute done, 0 % CPU, no output; `GATE1_POOL_HANG_INCIDENT.md`). Required before G2-B: per-arm/per-seed
checkpoint files + resume index + atomic final assembly; collection watchdog with bounded per-result wait; kill by
process group (macOS spawn workers reparent to PID 1); memory-aware worker cap (≤6 engine workers on the 8 GiB host).
Acceptance: a kill-test mid-run resumes from checkpoints and a simulated worker termination aborts loudly with a
partial index, not a hang.

## 7. A7 residual declaration (Gate-2 requirement)

`contest_candidates(m)` is the **same-year sitting cohort** (`cred==m & g==ends[m]-1`), not literal `cred<=m`;
future-gate expected P uses the current sitting cohort's probability curve by monotone interpolation (engine-core
`ENGINE_CORE_AUDIT.md` §B12). Consequences for Gate 2: (i) universal-admission arms MUST use
`share_of='applicants'`; a legacy cohort-share `share=1.0` arm is not universal (measured max e_t 5.97→0.34 under
the approximation); (ii) any Gate-2 run that changes the candidate pool must report the A7 gap; (iii) the plan
declares this approximation and its sensitivity as part of the calibration report.

## 7b. Precondition checklist (all three must be evidenced before G2-B)

| # | precondition | evidence link required | status |
|---|---|---|---|
| a | operator freezes canonical spec | `canonical_spec.json` + `CANONICAL_SPEC.md`, Lead-approved; variant V540-freeze or V420-port from §1b | **OPEN** |
| b | runner hardening (task-13, audit-runner) landed | hardening report + kill/resume test evidence (checkpoint resume, watchdog abort, process-group kill); `GATE1_POOL_HANG_INCIDENT.md` as the failure record | **PENDING** |
| c | A7 residual declared in Gate-2 plan | this plan §7 + Gate-2 calibration report must carry the A7 approximation + sensitivity | **DECLARED** (plan §7); report obligation carried |

**Gate-2 additionally requires:** benchmark registry reviewed (G2-A), identifiability report (G2-A §4c), and the
measured-budget table (§2) accepted as the planning basis (no assumed speed-up).

## 8. Gate-2 ordering and stop gates

```
G2-A freeze spec + registry + evidence ledger (no compute)     → Lead approves
G2-B pilot 500×3 (≈1.9 h)                                     → STOP if <5 feasible candidates or G2-A rank inadequate
G2-C search (≈32 h, or reduced per Lead)                       → top-100 table
G2-D refine 100×30 (≈3.9 h)                                   → seed-uncertainty report
G2-E held-out evaluation (~2.3 h)                             → pass/fail vs pre-stated tolerances
G2-F report                                                    → Lead decides Gate 3
```
No Gate-3 policy campaign before Gate-2 sign-off.

## 9. Risk register (Gate 2)

| risk | mitigation |
|---|---|
| pool completion hang (twice observed) | task-13 hardening; checkpoint/resume; watchdog; ≤6 host workers |
| host is 8 GiB, box is 10-CPU cgroup | box-declared venv, ≤10 total workers, controller-owned scheduling, memory caps |
| engine cost 4.7 CPU-h/540-class; search stage expensive | Lead-decided reduced search; task-12 memo only (1.113×); prep-grid lever requires tutoring-numerics decision |
| canonical spec dependence (420 vs 540; CF4 verdict flips) | freeze spec before any run; report spec-sensitivity explicitly |
| benchmark citations incomplete | registry review before G2-B; demote unresolved rows |
| CF4 flip | report as conditional simulation; old failure preserved; no policy claim in Gate 2 |
