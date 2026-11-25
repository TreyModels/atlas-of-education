# AUDIT VERDICT — Atlas of Education contest audit v2 (2026-11-25)

**Programme:** Atlas of Education · shadow-education contest papers A/B + repaired `eduengine`.
**Adjudicator:** `paper-adjudicator` (independent; did not write the manuscript, the engine repairs, or the audit).
**Date:** 2026-11-25. **Branch:** `research/contest-audit-v2-2026-11-25`. **Mode:** read-only synthesis; no
experiments run. **Inputs:** the two `.docx` manuscripts (text and tables extracted), `REVIEW_RESPONSE_2026-11-25.md`,
`GATE0_REPORT.md`, `GATE0_VERIFICATION.md`, `GATE1_REPORT.md`, `GATE1_MIGRATION_TABLE.md`, `CODE_CHANGES.md`,
`TEST_REPORT*.md`, `SCIENTIFIC_CLAIM_LEDGER.md`, the P0 annex (`ABC_IDENTIFICATION_AUDIT.md`,
`CONTEST_MATH_VALIDATION.md`, `SYNTHETIC_DGP_VALIDATION.md`, `BOOTSTRAP_REPORT.md`, `CONTEST_MATH_PERF.md`),
`GATE2_BENCHMARK_REGISTRY.csv`, `docs/audit/harvest/**`, `results/audit/**`, and the committed empirical records
on `research/e6e8-sequencing-2026-11-25` @ `bd782be`, `research/e8-fisher-ri-2026-11-25`, and
`research/gender-split-e6e8-2026-11-25` @ `b4eb680`.

**Taxonomy (verbatim):** `VERIFIED EMPIRICAL` · `REPRODUCED SIMULATION` · `VALIDATED SIMULATION` ·
`AUTHOR-REPORTED` · `CONTRADICTED` · `UNRESOLVED`.

---

## 0. One-paragraph verdict

The audit did its job: the engine defects are real and now repaired, the 540-run reproduction is solid, and the
identification/DGP/inference annexes are decisive. The **papers did not survive that repair**. Paper A's empirical
E8 block is real and citable (the only VERIFIED EMPIRICAL result in either paper), but its simulation and
identifiability half is unsupported — the "theorem" is not a theorem, the 1,640-run H2 experiment has no artifact,
the `t*` null is unresolved, and the archived ABC/DGP evidence is contradicted. Paper B's entire counterfactual
apparatus is a **420-generation, D2-artefact, spec-dependent** construction whose policy signs reverse on the
repaired engine; it is not a calibrated comparative study. **Neither manuscript is publishable in its present
form.** The programme does have four genuinely new, publishable findings — the D2 calibration artefact, the CF4
spec-dependence, the ABC/DGP identification failure, and the invalid E1/Q3 inference — but they are audit findings,
not paper findings, and they support a methods paper rather than the two current submissions.

---

## 1. What survives

### 1.1 VERIFIED EMPIRICAL (citable, with limits)

| Finding | Evidence | Limit |
|---|---|---|
| E8 fee-abolition event study: abolition-year primary-GER ATT **+12.44 pp**; post mean **+25.26 pp**; event path +23.82 / +25.94 / +22.12 / +25.19 / +28.56 / +25.92 | committed record `research/records/2026-11-25-e6e8-sequencing/results/e8_event_SE.PRM.ENRR_verified8.csv` @ `bd782be`; reproduction gate passed in `research/records/2026-11-25-e8-fisher-ri/results/repro_gate.json` | Observational CS ATT; association only; the source record explicitly forbids causal language. 7 treated cohorts, wide CIs (e=0 CI [−2.36, 27.24]). |
| Fisher randomization inference: **p = 9.999e-05** (placebo-date, both T0 and Tpost) and **5.999e-04 / 2.9997e-04** (placebo-country) | committed `e8-fisher-ri` record, B = 10,000 per family, pre-registered, reproduction-gated | .0001 is the 1/(B+1) resolution floor; p-values are conditional on strong exchangeability assumptions and a 40-country donor pool with unresolved-date contamination risk. |
| Gender differential: **D = −3.94 pp, 95% CI [−8.72, +0.29]**; pre-registered reading "no detected sex difference" | committed `gender-split-e6e8` record @ `b4eb680`, 500 paired bootstrap replicates, 498 used | Near-boundary non-detection, not a precise zero; IV/normal framings exclude zero; event-level estimates at +1/+2 have CIs excluding zero; 7 treated countries. |
| Within-gate equifinality: 176 collisions vs null mean 190.52, p = 0.838 (319,600 pairs) | committed `equifinality-phase` record @ `ab415f2` (`equifinality_null.json`), label "SIMULATION ONLY" | Not re-executed in this audit; descriptive simulation, chance-level result. |

### 1.2 VALIDATED / REPRODUCED (audit evidence, not paper findings)

* **Engine repairs validated against the contract.** Invariant suite BEFORE 7 failed / 12 passed / 8 xfail →
  AFTER **27/27** (host, box, and Commander independent); `ENGINE_CHECKS` 13/13; `TUTORING_CHECKS` 17/17;
  `contest_math` 68/68. The seven contract defects are closed: universal-seat positional effort 5.969 → 0;
  non-selective gate pricing → 0; KR G9 award persists (0 → 112 `elite`+112 `elite_prize`); expected = PL
  (max|ΔP| 5.55e-17, ΣP = seats); applicants-based seat denominator 0.513 → 0.2500; policy-invariant RNG
  (51 → 0 mismatches); gate prize paid as declared (0.6 → 0.1).
* **The 540-run reproduction is solid.** Host 9,174/9,180 seed + 842/846 summary values exactly equal to the
  supplied reference (max abs 3.553e-15 / 4.441e-16); box (NumPy 1.24.1/x86) 9,164/9,180 + 831/846 (max abs
  7.105e-15); 56-vs-8-worker bit-identical; every reported 2-d.p. figure identical. **REPRODUCED SIMULATION.**
* **The deterministic PL module is validated.** Exact subset DP matches `n!` enumeration to 1e-12; `auto` = exact
  for 12 < n ≤ 20; quadrature vs exact ≤ 1.0e-5; `auto` vs 400k MC max 0.0020; ΣP = seats exactly;
  `pl_realize` deterministic. **VALIDATED SIMULATION** (probability module only).
* **The repaired-engine 540 migration is recorded** (`GATE1_MIGRATION_TABLE.md`, sha256 `455649da…`):
  HK baseline elite Q5 46.36 → 25.01, gap 70.63 → 34.76, ratio 39.81 → 2.47; KR 36.12 → 22.13,
  68.36 → 29.71, 18.01 → 2.11; participation 59.07 → 61.92 / 57.44 → 58.38; contest effort 2.192 → 0.042 /
  1.711 → 0.016; expected/realised 2.41× / 1.96× → 1.0000. **REPRODUCED SIMULATION, uncalibrated, not validated.**

### 1.3 What is publishable as-is

* **A short, descriptive Paper A1** on the E8 event study + Fisher RI + gender analysis. Real, committed,
  reproduction-gated work. Association-only wording; full lead vector; near-boundary gender caveat.
* **An audit/methods paper** built from the four new findings below. This is the strongest publishable output the
  programme currently has.

---

## 2. What is contradicted

### 2.1 Paper A

1. **Identifiability "theorem" / "proves" full structural identification.** The only independent computation of the
   affiliated design gives rank **4/5** (not 5), a **2-dimensional null space**, **44 distinct parameter vectors**
   reproducing the moments, and **local rank 5/5 only** after two added micro-moments. No global injectivity.
   (A-14, A-17, A-18, A-20.)
2. **"Five independent aggregate moments" / rank 5/7 with condition 1.09e13.** No artifact; the archived moment
   set is rank 4/5; condition numbers are not identification evidence. (A-13, A-18.)
3. **"Flat pre-trends (−0.03, −0.13) and a clean −6-year placebo (−0.39)."** The committed event table has leads
   e=−5 **+6.39** and e=−4 **+1.35**; the −0.39 is a placebo-6 **post-period mean**, not a lead. (A-05.)
4. **Gender non-detection is "robust to inverse-variance weighting".** The committed follow-up says the opposite in
   part: IV point −4.05 with an IV CI [−5.94, −2.17] excludes zero; the pre-registered paired CI upper bound is
   +0.29; it is a near-boundary non-detection. Discussion's "lifting boys and girls alike" is unsupported. (A-06.)
5. **"Validates a mechanistic simulator out-of-sample."** No reproduced run; the repaired engine changes the
   mechanism. (A-25.)
6. **Replication claim in the Author Note.** The package contains no Exp 1/3/4/5 code, seeds or results. (A-31.)
7. **GPU/ABC/DGP evidence lineage.** 14 of 20 GPU-bundle claims are CONTRADICTED; the legacy synthetic DGP is
   degenerate (rank 3/5). (A-32, A-20.)

### 2.2 Paper B

1. **"Tutoring taxes backfire on spending and equity."** Pre-repair 540 reproduces it; repaired 540 reverses it
   (HK spend 96.49, elite 24.67; KR 96.88, 21.57 — both below baseline). It is a D2 artefact, not a structural law.
   (B-14, B-15, B-16.)
2. **"Wage compression raises Q5 elite capture."** Repaired 540 reverses it (HK 23.64, KR 21.48 — both below
   baseline). (B-23.)
3. **"Effort caps broaden participation / only CF1b is Win-Win."** Repaired participation is flat; CF1b fails spend
   (97.21 / 99.25), while CF3b and CF4a pass. (B-21, B-24.)
4. **"Only pairing wage compression with caps/seat expansion reaches the Win-Win frontier."** The manuscript has no
   combined-arm table; the 540 pre-repair test falsifies it; the repaired engine reverses it; the 420-port passes it.
   Three generations, three verdicts. (B-22, B-39.)
5. **"Seat expansion lowers Q5 elite capture in both jurisdictions."** HK yes; KR no (repaired CF2a 22.27 > 22.13
   baseline; CF2b flat). (B-19.)
6. **"Reproduces / directly explains the 2024 Korean medical-seat shock."** A simulation cannot reproduce a
   historical event; the episode's data are proposed-vs-finalised (2,000 vs ~1,500), 2024 KRW 29.2 tn vs 2025
   ~27.5 tn, arXiv-preprint-sourced. The archived 100 % seat-expansion paradox is an S-grid truncation artefact;
   the corrected surface is an inverted-U ending at 0. (B-20, B-27.)
7. **"Every lever produces qualitatively identical dynamics / the exact same policy hierarchy."** False across
   jurisdictions and generations. (B-25.)
8. **"Calibrated across 420 matched simulation runs … demonstrates."** The 420 generation is not reproducible; the
   540 run is not calibrated on participation. (B-01, B-34, B-26.)
9. **"Published targets 32.1 pp / 3.4×"** are **derived targets with no located empirical source**, not published
   observations; 76.5 % is a diagnostic-only derived band; 2024 = 80.0 % / 2025 = 75.7 % is the registry record.
   (B-05, B-06, B-07, B-08, B-09.)

### 2.3 Both papers / shared apparatus

* **The 420-run generation cannot be cited as a result.** It has no runnable runner; the docx tables are a verbatim
  rendering of a self-reported JSON. (B-01; `RECONCILIATION.md`; `LEAD_GROUND_TRUTH.md` §5.1.)
* **The archived GPU/ABC bundle is quarantined and mostly contradicted** (see §3.3). GPU-vs-CPU agreement is
  arithmetic only and validates no claim.
* **The shipped E1/Q3 pooled selftest is invalid** (see §3.4).
* **The 100 % seat-expansion paradox is contradicted** (see §3.2).

---

## 3. The four genuinely new findings

These are the programme's real contributions. They are **audit findings**; neither manuscript currently reports
them correctly, and neither may be cited as a paper result until written up separately.

### 3.1 FINDING 1 — the "540 lost the Korean calibration" is largely a D2 code-defect artefact, not a parameterisation failure

**Evidence.** `GATE1_MIGRATION_TABLE.md`; `GATE1_REPORT.md` §5; repaired 540 JSON sha256 `455649da…`.

* Pre-repair, households bought contest preparation against an expected admission probability **2.41×** (KR G12:
  0.292 vs 0.121) and **1.96×** (HK G12: 0.455 vs 0.232) the realised Plackett–Luce probability. Contest prep was
  **92–94 %** of pre-repair K–12 household spending in this config.
* After the D2 repair (expected P = the exact PL object; per-gate expected/realised = **1.0000**), and with **no
  parameter re-estimation**, the KR gap moves **68.36 → 29.71 pp** (target 32.1) and the spend ratio
  **18.01 → 2.11×** (target 3.4). Contest effort collapses 98–99 %; participation is essentially unchanged.
* The pre-repair "calibration failure" that the external review treated as a parameterisation failure is therefore
  mostly a **code-consistency failure**. What remains is a smaller, real calibration task: gap 29.7 vs 32.1,
  ratio 2.11 vs 3.4 — and, separately, participation and grade-12 participation, which the repair did **not** fix
  (KR K–12 58.4 % vs 76.5 %; HK G12 49.3 %, KR G12 36.0 % vs 71.8 %).
* **Both sides of the review exchange were partly wrong:** the review's "lost calibration" over-attributed to
  parameters; the author's "calibrated" ignored participation. The corrected statement is in §5.

**Why it is new:** the review identified the D2 defect and the calibration failure as separate items; the audit
connects them causally and quantifies it. No previous document in the programme makes this inference.

### 3.2 FINDING 2 — the CF4 combined-policy verdict is specification-dependent; three generations, three verdicts

**Evidence.** `GATE0_VERIFICATION.md` (540 pre-repair); `GATE1_MIGRATION_TABLE.md` (540 repaired);
`docs/audit/harvest/HARVEST.md` §4b (420-port legacy V1); `code/REPRODUCTION_CF4_2026-11-25.md`.

| generation | CF4a Win-Win? | CF1b Win-Win? | CF3b Win-Win? |
|---|---|---|---|
| 420-port legacy V1 (AUTHOR-REPORTED / PRE-REPAIR / UNCALIBRATED) | **YES both** | — | — |
| 540 pre-repair (REPRODUCED SIMULATION) | **NO** (HK elite 48.64 > 46.36) | **YES** (only arm) | NO |
| 540 repaired (REPRODUCED SIMULATION, uncalibrated) | **YES both** (HK 70.58/23.44; KR 72.48/21.47) | **NO** (spend 97.21/99.25) | **YES** (70.88/23.64; 72.55/21.48) |

The paper's "only wage compression paired with caps/seats reaches the win-win frontier" and the reproduction record's
"only CF1b passes" are both generation artefacts. **No policy conclusion is established**; the ranking requires a
frozen canonical spec, Gate-2 calibration, and Gate-3 re-runs.

**Why it is new:** the review and the Gate-0 record each reported one generation's CF4 verdict as if it were stable.
The audit's own repair then flipped it again, and the harvest supplied a third verdict. The spec-dependence is the
finding; it must be reported, not resolved by preference.

### 3.3 FINDING 3 — the ABC/DGP identification apparatus is invalid: rank 4/5, 2-dim null, 44 θ, analytic δ; legacy DGP 3/5 vs corrected 5/5 in 500/500

**Evidence.** `ABC_IDENTIFICATION_AUDIT.md` (task-6); `SYNTHETIC_DGP_VALIDATION.md` (task-7);
`SCIENTIFIC_CLAIM_LEDGER.md` G-01…G-08, A1–A4, A10.

* The advertised 5-moment Jacobian has **rank 4/5** at **1,000/1,000** prior-box points (left-null certificate
  ≤3.4e-16): `m_part ≡ ⅔·m_g9 + ⅓·m_g12` identically (420/210 pupils). With **6 active parameters** the null space
  is **2-dimensional**; **44 distinct θ** inside the prior reproduce the same five moments; the null motion is
  0.266 with residual 1e-16.
* `θ5` (`teacher_threshold`) never enters the utilities or moments. `P(own|tutoring) = 1/(1+e^δ)` is **analytic**:
  δ = ln(0.32/0.68) = **−0.7537718023763802**; the archived estimates (69.51 % / 66.11 % own share) were inside the
  frozen tolerance and masked an exactly solvable parameter.
* The "posterior correlation condition number" (25.96 → 21.03, or 447.16 → 23.97 in Paper A's variant) is an
  eigenvalue ratio of accepted draws, **not** a moment-Jacobian rank statistic and **not** identification evidence.
* The legacy synthetic DGP is degenerate: **G12×urban cell empty**, no school identifiers, `school_gap ~ U(0,1)`
  i.i.d. per pupil. Legacy Jacobian **rank 3/5** (min SV exactly 0) in 100/100 populations; recovery RMSE 0.58–0.64
  for income/school-gap. The corrected crossed design (4 cells, 32 schools, income–quality link) gives **rank 5/5 in
  500/500 populations** across three independent seed bands, recovery RMSE 0.04–0.13, with 182,212 accepted draws
  and 106,902 posterior-predictive draws retained.
* Paper A's own Jacobian was never deposited. Its micro-moments restore **local rank 5/5 only** on the affiliated
  design; the archived ABC outputs cannot support it.

**Why it is new:** this invalidates a whole class of identifiability claims (both papers and the GPU bundle) and
supplies the corrected design that future work must use. It is the most quantitatively decisive finding in the audit.

### 3.4 FINDING 4 — the pooled E1/Q3 selftest cannot support any inference; the permutation is within-invariant

**Evidence.** `BOOTSTRAP_REPORT.md`; `SCIENTIFIC_CLAIM_LEDGER.md` G-12…G-14, A9.

* Under a true zero-effect null, the pooled OLS selftest rejects **99.6–100 %** of the time when country
  confounding κ ≥ 0.25 (bias +0.23/+0.39/+0.49; coverage 0.02/0.00/0.00) — the DGP puts the country effect in both
  the regressor and the outcome, so the "minority-effect leakage" result is **omitted-variable bias**.
* Country FE (and country+year FE) hold nominal size **0.052–0.062** across κ and have honest power ≈0.78–0.80 at a
  12 % average effect.
* The shipped country-block permutation is **algebraically within-invariant** under FE:
  `x*_it − x̄*_i ≡ x_it − x̄_i`; numerical deviation **6.66e-16**; FE β changes by ≤9.71e-17 across permutations. Its
  "p = 0.001" tests the pooled estimand, not the within estimand. Adding FE to it cannot repair it.
* Valid replacements: restricted wild-cluster bootstrap (size 0.025–0.042) and whole-trajectory cluster bootstrap
  (size 0.033–0.050; coverage 0.95–0.97).
* The auditor's four reported statistics and the negative control are independently reproduced (β = 0.4447407389,
  SE = 0.0829135845, t = 5.3639067888, p = 0.0004997501; negative-control β = 0.3054438887, t = 4.9745).

**Why it is new:** Paper A's declared replication bundle includes the E1/Q3 script; the received manuscript makes no
E1/Q3 claim (keep it that way), but any draft that cited the pooled/bootstrap selftest is contradicted. The finding
also sets the inference standard for all future E1/Q3 work: FE estimator + wild-cluster or whole-trajectory
bootstrap, never the shipped permutation.

---

## 4. What remains unresolved (tasks, not results)

| # | Unresolved item | Blocks | Evidence |
|---|---|---|---|
| 1 | **Canonical spec not frozen** (420 vs 540; G9 design KR-TRACKED vs KR-SINGLE) | every calibration and policy claim | `GATE2_PLAN.md` §1b; `DASHBOARD.md` open decision 1 |
| 2 | **Gate-2 calibration not run** (~271 CPU-h approved, conditional) | Paper B calibration and any policy arm; Paper A simulator forecast | `GATE2_PLAN.md` §2; STOP conditions (identifiability rank, pilot ≥5 in-band candidates) |
| 3 | **Paper A Exp 1/3/4/5 runners, seeds, raw results not deposited** | A-07…A-25 | `MISSING_ARTIFACTS.md` |
| 4 | **420-era runner not runnable** | Paper B Tables 2–4 and Figures 1–4 | `RECONCILIATION.md`; `LEAD_GROUND_TRUTH.md` §5.1 |
| 5 | **KR benchmark sources not established** (gap 32.1, ratio 3.4, KR 2024 80.0 %, HK 2011/12) | Paper B calibration; Gate-2-A | `GATE2_BENCHMARK_REGISTRY.csv` |
| 6 | **Gate-1 migration residual risks**: A7 pool-map approximation (future-gate expected P uses current sitting cohort; universal share not literal); quota CDF unchanged (still normal-CDF, not PL); `schools.py`/`anchor.py` still legacy sequential RNG; legacy G9 premium delivered in the unmodified 540 config | strict validity of the repaired-engine numbers | `GATE1_REPORT.md` §9 |
| 7 | **Runner completion-phase hang** (host failed twice) — hardening in progress (`task-13`) | Gate-2 campaign launch | `GATE1_POOL_HANG_INCIDENT.md`; `HANG_63896.txt` |
| 8 | **No GPU campaign**; GPU conclusions remain quarantined | any GPU-based claim | `EXTERNAL_AUDIT_GPU_2026-11-25.md`; ledger §D |
| 9 | **Paper A causal language** in the E8 block (association-only record) | A1 publishability | `e8-fisher-ri/REPORT.md` language rule |
| 10 | **Corrected DGP design assumptions** (ρ = 0.50, 32 schools, ICC) are labelled assumptions, not estimates | future identification work | `SYNTHETIC_DGP_VALIDATION.md` §2, §8 |

---

## 4A. Reimplementation plan (operator decision, 2026-11-25)

The operator clarified that **Gemini ran both papers inside its app and made other mistakes**. We are **not
recovering its files; there is no Codex Paper-A re-run to compare against** (Codex is the independent auditor, and it
did not like what Gemini did). We are **reimplementing what Gemini was trying to do — bigger and better — on the
repaired engine, using the server**. The old docx numbers are the **AUTHOR-REPORTED
BASELINE**; the new runs are a **NEW GENERATION** with pre-registration, hashes, provenance, uncertainty, baselines
and sensitivity. Full plan: `docs/audit/PAPER_A_REPRODUCTION_ATTEMPT.md` (reimplementation plan + status) and
`docs/audit/PAPER_A_BASELINE_VS_NEWGEN_TEMPLATE.md` (two columns: AUTHOR-REPORTED baseline vs NEW GENERATION).

**Paper A — five computations and status:**

| # | computation | new-generation design | status |
|---|---|---|---|
| (a) | E8 fee-abolition event study | fresh hashed WDI vintage; **CS-style group-time ATT** (not-yet-treated controls), 500 cluster bootstraps + 2,500 Fisher/scheme; full event path | **DONE (REPRODUCED EMPIRICAL ANALYSIS)** — impact **+12.322 pp** (bootstrap mean 12.308, 95% CI [4.48, 22.64]) and post mean **+25.083 pp** (author +25.26) **both replicate**; event path 12.32, 23.66, 25.79, 21.88, 24.94, 28.45, 25.78; Fisher p 0.0044/0.0040. Declared deviations: equal weights, no DR covariates, 8 clusters → wide CI, fresh vintage. Simple-DiD +2.54 is **estimator sensitivity**, not a data difference |
| (b) | Delayed secondary-bulge `t*` | fresh hashed WDI; `t* = abolition + SE.PRM.DURS`; outcome SE.SEC.ENRR; 2,500 perms/scheme | **DONE (fresh WDI)** — ATT at `t*` **−0.956 pp**, post +0.30, Fisher p **0.251 / 0.384** → **no detectable secondary-bulge jump**; **UNRESOLVED** (no-effect evidence), consistent with the manuscript's honest-null framing |
| (c) | Gate-architecture / H2 (≥5,000 runs) | repaired `846c9e0`; **Amendment A3**: 4 architectures × 5 S × 2 fee × 4 vac0 × 32 matched seeds = 5,120 primary (`fail='track'`) + 512 `fail='stop'` sensitivity = **5,632 runs**; POST e=+1..+6; primary H2 = contest vac0=.08; paired-seed bootstrap 5,000; secondaries quota/vac0-curve/H1/Spearman; bar exploratory | **CLEARED FOR LAUNCH (A3 verified); RUN PENDING** — report conditions recorded in §4E; run launches after Paper B full (~2.4 h at 8 workers); no fee-contrast result yet |
| (d) | Multi-seed identifiability/Jacobian | frozen V540-FREEZE 4θ × 4-moment calibration map; 5 matched seeds/column; declared steps 5/3/5/4 %; central differences; **3 starts** (stop gate satisfied); report rank/SV/null across starts, local-only | **REVIEWED — STOP GATE MET WITH DECLARED RESTRICTION** (`LOCAL_FULL_RANK_CONDITIONING_UNRESOLVED`): local full rank established at the tested points — rank **4/4**, null dim **0** at **3/3** starts (SVs 50.030/32.596/1.907/**0.341**; 46.916/17.058/6.801/**0.128**; 46.852/23.579/1.993/**0.046**). The fourth direction is not stable (pairwise rel |ΔJ| **0.287 / 0.350 / 0.416**; s4 0.3409 → 0.1278 → 0.0457), so the conditioning is unresolved and Gate-2 must declare a reduced parameterisation or a ridge/prior for that direction. **No global-identification or condition-number claim.** |
| (e) | Fee-abolition forecast with held-out | fixed engine `846c9e0` (canonical re-pin `46c080d`); `year_t=T0`; `assert E.unfired_events==[]`; 40 seeds; held-out e=+5,+6 | **ACCEPTED — REPRODUCED SIMULATION (NEW GENERATION)** — abolition − persistence **+17.19 … +25.35 pp** (e=0..6); full-7 RMSE **2.764 / MAE 2.432** vs persistence **23.759 / 23.260** (**−88.4 %**); held-out e=+5,+6 RMSE **1.637 / MAE 1.350**. **Calibration fallback:** the author's **74.88 % anchor is infeasible** in the repaired world (max 71.0 % at fee 0; A-38), so fee 0.15 + engine pre-abolition level, **no post tuning**; conditional simulation, not a reproduction of the author's calibration. v1 numbers remain uncited |

**New-generation E8 empirical result (fresh hashed WDI, label `REPRODUCED EMPIRICAL ANALYSIS`):** **both the
impact and the delayed amplification replicate under the author's estimator family.** CS-style group-time ATT
(not-yet-treated controls) gives ATT(e=0) **+12.322 pp** (bootstrap mean 12.308, 95% CI [4.48, 22.64]) and post mean
e=+1..+6 **+25.083 pp** vs author +12.44 / +25.26; event path 12.32, 23.66, 25.79, 21.88, 24.94, 28.45, 25.78;
pre-trend e=−3 +0.138; Fisher p **0.0044 dates / 0.0040 countries** (2,500 each, 500 cluster bootstraps). Declared
deviations: **equal country weights** (no cohort-size weighting), **no doubly-robust covariates**, **8 treated
clusters → wide CI**, fresh vintage. The earlier simple-DiD **+2.54 pp** is **estimator sensitivity**, not a data
difference. The **delayed-bulge `t*`** gives ATT **−0.956 pp** and Fisher p **0.251 / 0.384**: **no detectable
secondary-bulge jump**, recorded as **UNRESOLVED** (no-effect evidence), consistent with the manuscript's honest-null
framing. Artefacts: `docs/audit/CS_ESTIMATOR_NEWGEN.md` (sha256 `04faf9dc…b196`),
`results/audit/newgen/cs_estimator_fresh_wdi_2026-11-25.json` (sha256 `4ac9551d…1905`),
`docs/audit/E8_BULGE_NEWGEN.md` (sha256 `97734cdc…`), WDI manifest sha256
`d7296e1fed3eb6806ba5111de2538e7fcd206323832307a1fabeeaefc6c55ee4`. **Forecast (e) is now a new-generation conditional simulation (REPRODUCED SIMULATION) on the fixed engine:**
abolition − persistence **+17.19…+25.35 pp**, full-7 RMSE **2.764** vs persistence **23.759** (−88.4 %), held-out
e=+5,+6 RMSE **1.637**; but the author's **74.88 % level anchor is infeasible** in the repaired world (max 71.0 % at
fee 0; A-38), so the run uses a declared fallback (fee 0.15, engine pre-abolition level, no post tuning) and does not
reproduce the author's calibration. v1 numbers remain uncited.**

**Paper B:** the **420 design is AUTHOR-REPORTED BASELINE** (runner/raw output not found where searched; docx tables
== self-reported JSON). The **540 is reproduced** — scripts/data in hand (`hk_korea_exact_bundle.zip` /
`hk_korea_contest_code_bundle.zip` / `ALL_ATLAS_WORK_2026_11_25.zip`; runner `dd0b1d8d…`, engine
`618bd6dd…`/`b2d213b6…`, reference `851bb1df…`) — and all HK/Korea-dependent tables were regenerated as a **NEW
GENERATION**: `PAPER_B_TABLE_REGENERATION.md`, `results/audit/paper_b_540_regenerated_tables.csv`
(sha256 `da40a2ee…c5c1`). **The 100-seed Paper B new generation is now complete** (`a4b0808`; TRACKED `cf801af8…`,
SINGLE `2b69fa08…`, provenance `8f08164d…`; engine `98baf6b`, frozen spec, seed-MC only): **CF4a meets the pre-stated
both-jurisdiction Win-Win** (HK 70.59/23.21 vs 24.82; KR-TRACKED 73.13/22.16 vs 23.90; KR-SINGLE 75.43/22.04 vs
24.08) — the **CF4 reversal is explicit** — while **CF4b (89.99/109.70) and CF1b (97.25/99.19) fail spend** and
**CF3b also passes both** (70.88/23.43; 73.21/22.21). **Caveat: participation falls ~13 pp under CF4a** (HK 61.93 →
48.60; KR 55.79 → 42.81) — the criterion is spend+elite only. Full record: §4F; the pre-repair failure remains
reported.

**What was re-executed (adjudicator, host):** (i) the independent ABC identification audit ran and produced
`/tmp/abc_identification.json` sha256 `66bb2648…15808`, **bit-identical to the committed host output** in
`ABC_IDENTIFICATION_AUDIT.md` §6 (rank 4/5, 2-dim null, analytic δ −0.7537718023763802, cell means
0.8233/0.5167/0.85, local 5/5 after two micro-moments); (ii) the bootstrap size/power factorial re-ran to exit 0 and
its summary matches the committed result to last-bit float (FE size median **0.05925**, pooled size under
confounding **1.0**, permutation within-invariance **6.661338147750939e-16**, `permutation_invariant=true`,
`benchmark_matches=true`; only date/runtime/last-bit fields differ); (iii) the corrected-DGP harness was still
running under host load at finalisation — its committed result (rank 5/5 vs legacy 3/5) stands and is labelled as the
audit's.

**Nothing was reconstructed from memory.** The missing original artefacts are noted but are **not the blocker**; the
repaired engine and the server are.

## 4B. NEW-GENERATION EVIDENCE vs AUTHOR-REPORTED LEGACY vs CONTRADICTED (honesty register)

This is the distinction the papers and the errata must carry:

* **NEW-GENERATION EVIDENCE (REPRODUCED SIMULATION / VALIDATED SIMULATION):** the repaired 540 (`98baf6b`, sha256
  `455649da…`), the migration table, the **100-seed Paper B new generation** (corrected artifacts `cf801af8…` /
  `2b69fa08…` / `8f08164d…`; engine `98baf6b`; **CF4a meets the pre-stated both-jurisdiction Win-Win** with a ~13 pp
  participation reduction whose welfare interpretation is unresolved; CF4b/CF1b fail spend; CF3b also passes), the **CF4 reversal** (CF4a Win-Win both; CF1b no
  longer passes; CF4b fails; CF3b passes), the D2 calibration artefact (KR gap 68.36 → 29.71; ratio 18.01 → 2.11 without re-estimation), the
  regenerated Paper B tables, the P0 audits (ABC rank 4/5 + 2-dim null + analytic δ + local 5/5; corrected DGP 5/5
  vs legacy 3/5; bootstrap FE size 0.052–0.062 vs pooled 0.996–1.000; permutation within-invariance 6.66e-16), and
  the verified E8 empirical block. **These are what we can cite.**
* **AUTHOR-REPORTED LEGACY (AUTHOR-REPORTED BASELINE):** the Paper B 420 tables, and Paper A Exp 1/3/4/5 (bulge `t*`,
  1,640-run gate matrix, Jacobian, forecast). These are baseline for comparison — **not results, not reproduced, not
  to be silently replaced**.
* **CONTRADICTED BY THE REPAIRED ENGINE / MEASURED AUDITS:** the Paper B "tax backfires", "wage compression is
  regressive", "only CF1b", "only pairing compression with caps/seats" claims (all reverse or become spec-dependent);
  the "published benchmarks" attributions (G2-A: all four moments dropped/UNRESOLVED); the archived ABC "7-parameter
  calibration", the "100 % seat-expansion paradox", and the pooled E1/Q3 selftest. **These must be removed or
  rewritten.**

## 4C. Pre-registration review criteria (for when the Commander's design lands)

When the reimplementation pre-registration and design land, review them against the independent auditor's four
criticisms. Each must be **fixed by design**, and the pre-registration must name the acceptance test:

| Codex audit criticism (measured in our P0 annex) | required design fix | acceptance test |
|---|---|---|
| **Moment rank 4/6**: with 6 active parameters the advertised 5-moment Jacobian has rank **4/5** at 1,000/1,000 prior-box points; null space **2-dimensional**; **44 distinct θ** reproduce the same moments; analytic δ = −0.7537718023763802 | run a **rank audit before estimation**; declare a reduced parameterisation or add independent moments until rank = number of free parameters; fix δ analytically; no condition-number-as-identification claims | rank ≥ free parameters at every declared perturbation; null space dimension 0; report the null vectors if not |
| **Empty G12×urban cell / no school identifiers** in the legacy synthetic DGP (legacy rank 3/5; corrected crossed design rank **5/5 in 500/500**) | cross grade × urban cells; add school identifiers + within-school dependence; positive income–quality relationship; declare the design assumptions (ρ, school count, ICC) | G12×urban cell non-empty; rank 5/5 across 500 populations and 3 seed bands; recovery RMSE reported |
| **Pooled E1/Q3 selftest size ≈ 1.0 under the null** vs country-FE size **0.052–0.062** (OVB) | use the **FE estimator** with a **restricted wild-cluster bootstrap** (size 0.025–0.042) or a whole-trajectory cluster bootstrap (size 0.033–0.050, coverage 0.95–0.97); never the pooled selftest as evidence | nominal size control in a pre-registered Monte Carlo; no pooled-selftest claim |
| **Country-block permutation within-invariant** (6.66e-16; FE β changes ≤9.71e-17) | do **not** use the shipped permutation; use wild-cluster / whole-trajectory bootstrap for the within estimand | permutation invariance check fails by design (i.e., the chosen method actually moves the within estimand); size control demonstrated |

**Verdict requirement:** the pre-registration must be rejected by this review if it uses any of the four legacy
procedures unchanged, or if it claims global identification from a local rank, or if it presents the repaired 540
(`455649da…`, legacy gate list) as the frozen `canonical_spec.json` V540 run.

## 4D. Review of new-generation identifiability — item (d) — **REVIEWED: STOP GATE MET WITH DECLARED RESTRICTION**

Artefacts: `docs/audit/G2A_IDENTIFIABILITY_MULTISEED.md` (sha256 `9c40aeed…3b07`) and
`results/audit/newgen/identifiability_multiseed_846c9e0_pin.json` (sha256 `66535941…4be3`). The map is the **frozen
V540-FREEZE calibration map** (4 θ: price/alpha/prize/ymed multipliers; 4 moments: KR participation, KR gap, KR
spend ratio, HK G9 participation), **5 matched seeds per finite-difference column**, declared steps 5 %/3 %/5 %/4 %,
central differences, **3 starts**, 90 + 45 evaluations, engine pin `98baf6b` (core `72cbddf7…`; numerics unchanged vs
`846c9e0`; pre-re-pin recorded). It is **not** Paper A's legacy 10-parameter `masseng-tutoring` model; it is the
operational Gate-2 calibration-map identifiability.

| start | θ | rank | singular values | null dim |
|---|---|---|---|---|
| 0 | (1.0, 1.0, 1.0, 1.0) | **4/4** | 50.0299, 32.5956, 1.9066, **0.3409** | 0 |
| 1 | (1.5, 0.8, 1.5, 0.95) | **4/4** | 46.9156, 17.0582, 6.8014, **0.1278** | 0 |
| 2 | (0.7, 1.2, 0.8, 1.3) | **4/4** | 46.8523, 23.5794, 1.9931, **0.0457** | 0 |

**Pairwise start-to-start stability (max |ΔJ| / rel):** 0-1 **11.476 / 0.287**; 0-2 **14.006 / 0.350**; 1-2
**14.071 / 0.416**; global max **14.071 / 0.416**. **s4 trajectory: 0.3409 → 0.1278 → 0.0457 — it keeps drifting
downward; there is no stable fourth direction.**

**Stop-gate verdict (verbatim from the artefact): `LOCAL_FULL_RANK_CONDITIONING_UNRESOLVED`.** The declared
`conditioning_settled` criterion (pairwise rel |ΔJ| < 0.10) **fails at all three pairs** (0.287 / 0.350 / 0.416);
rank is full and null dim is 0 at every start, but the fourth direction is not stable across starting points.
Therefore:

* **local full rank at the tested points: YES** (rank 4/4, null dim 0, 3/3 starts);
* **global identification: NO** — and none is claimed;
* **fourth-direction conditioning: UNRESOLVED** — the smallest singular value is unstable and shrinking;
* **Gate-2 stop-gate decision: MET WITH DECLARED RESTRICTION.** Local full rank at the tested points is
  established (3/3 starts, rank 4/4, null dim 0), so the gate's rank requirement is satisfied; but the fourth
  direction's conditioning is **not settled** (s4 drifts 0.3409 → 0.1278 → 0.0457; pairwise rel |ΔJ| up to 0.416).
  Gate-2 therefore proceeds **only** with a declared **reduced parameterisation** or a **ridge/prior for the fourth
  direction**, recorded in the pre-registration. The 4-parameter map must **not** be treated as identified in its
  fourth direction merely because the numerical rank is 4.
* **A condition number is not identification evidence.** Report rank/SV/null space and their start-to-start
  variation — not a single condition number.

**Assessment against the four Codex criticisms (measured P0 numbers):**

| criticism | status for (d) | carried to the pre-registration review |
|---|---|---|
| **rank 4/6** (original 5-moment ABC: rank 4/5 at 1,000/1,000 points; 6 active params ⇒ 2-dim null; 44 θ replicate; analytic δ) | **not answered** — (d) is a **reduced 4θ** map. Rank 4/4 for 4 parameters does not establish identification for the 6-parameter ABC; the reduction drops the income/school-gap null directions. | the prereg must not claim the 6-param ABC is identified; state the reduction explicitly |
| **empty G12×urban / no school IDs** (legacy synthetic DGP rank 3/5; corrected 5/5 in 500/500) | **not addressed by (d)** — the four moments have no grade×urban cross or school-level moments; this is an engine calibration map, not the synthetic ABC design. | a **(c)/design issue**: any identification claim must use the corrected crossed grade×urban, school-identified design |
| **pooled E1/Q3 selftest size ≈1.0 vs FE 0.05–0.06** | **not applicable to (d)** (identifiability, not E1/Q3) | any E1/Q3 claim in the same prereg must use the FE estimator + WCR/whole-trajectory bootstrap, never the pooled selftest |
| **within-invariant permutation 6.66e-16** | **not applicable to (d)** | any E1/Q3 permutation claim must not use the shipped country-block permutation |

**Ledger:** A-39 is **VALIDATED SIMULATION (STOP GATE MET WITH DECLARED RESTRICTION)** — the deterministic
identification computation is validated and the **local** full-rank claim is established at the tested points; the
claim/action record the 3-start numbers, pairwise instability, s4 trajectory, the
`LOCAL_FULL_RANK_CONDITIONING_UNRESOLVED` label, and the required restriction. **No global-identification and no
condition-number claim is made.**

**Item (c) review — the ONLY remaining Paper A computation.** The gate-architecture pre-registration has **not
landed**; when it does, review it against the same four criticisms (rank-4/6 structure, empty G12×urban, pooled
selftest, within-invariant permutation) before any (c) run is accepted. (d) is now closed with the declared
restriction; (a), (b), (e) are closed (A-34/A-35, A-36, A-37).

## 4E. Review of item (c) gate-architecture pre-registration — **CLEARED FOR LAUNCH (Amendment A3 verified); report conditions recorded**

Sources reviewed: `docs/audit/GATE2_PREREGISTRATION.md` §2(c); runner
`papers/shadow-education-contest/code/run_gate_architecture.py` (sha256 `b046318c…e3a`). Design as submitted:
repaired engine pin `846c9e0`; NEW SSA-like world (N=300, T=20, T0=12, KR primary base); 4 architectures
{bar, bar_high, quota, contest} at the G6→G9 transition × 5 seat shares {0.25,0.35,0.45,0.55,0.70} × 2 fee regimes
{0.19 kept, 0.00 abolished at T0} × 4 vacancy rates {0.02,0.08,0.25,0.50} × 32 matched seeds = **5,120 runs**;
per-run `E.unfired_events == []`; fee-cell pilot verified `event_log == [(12,'fee abolition',{'fee_public':0.0})]`.

**Verdict: structure is sound; the run is CONDITIONAL. Do not launch the fee contrast until the pre-registration is
amended with the three must-fix items below; the `--fees 0.19` fee-free block may launch meanwhile.**

**Must fix before the fee-contrast launch:**

1. **Fail routing undeclared and currently `fail='stop'`.** The canonical KR primary G9 gate is `fail='track'`
   (`canonical_spec.json`: KR-G9-track, share 0.35, `track_consequence`). With `stop`, the experiment becomes a
   **dropout** experiment and the Q5−Q1 tutoring gap is confounded with selection/dropout, so it is not comparable to
   the paper's vertical-tier/universal-K12 design. Declare **primary = `fail='track'`** (matches the KR spec) with
   `stop` as a declared sensitivity (extra cells), or run both as an explicit 2-level factor.
2. **POST window truncated at +4** (`POST = range(T0+1, T0+5)` = e=+1..+4) although `T=20` allows e=+1..+6. The
   paper's H2 is over post e=+1..+6. Extend to `range(T0+1, T0+7)` (free; no extra runs) or declare the +4 truncation
   as a deviation and do not compare H2 magnitude to the paper's.
3. **Primary estimand and uncertainty not pre-declared.** Specify: primary H2 = **contest at vac0 = 0.08** (the
   paper's 2×2) — the runner currently averages H2 over vac0 and computes it for bar/bar_high too (averaging can
   cancel the inverted-U); quota H2 as comparator; bar/bar_high H2 **exploratory only** (their S is a bar-threshold
   mapping, not a realized seat share — report realized admission rates); H1 = gap_delta(fee=0, S=.25) −
   gap_delta(fee=0, S=.70) plus a monotonicity/Spearman statistic; **paired-seed bootstrap 95% CI** (resample the 32
   matched seeds, pair fee0/fee0.19 by seed) for H2/H1/per-vac0 Δcut — currently H2 is a difference of independent
   means with **no CI**; a multiplicity rule; and a **null-reporting rule** (the pre-repair +0.1086 is
   AUTHOR-REPORTED baseline, not a target; a null/negative repaired-engine H2 is a result, not a failure).

**Analysis/provenance fixes (commit with the amendment):** (4) engine label says "98baf6b" in the docstring/LABEL but
metadata hardcodes `846c9e0` — make consistent; (5) record `fees/archs/shares/vacs/N/T0/T/measure_from/start_year`,
spec hash, runner hash, `event_key`, and per-run `event_log` in metadata/output; (6) use **`year_t=T0`** for the fee
event (additive engine feature; bit-identical; robust to `start_year`) and keep the unfired assertion; (7) verify and
print the effective gate-level `r=0.6/alpha=0.5` (engine supports them; add a smoke assertion); (8) report per-quintile
× urban cell counts and per-gate applicants/seats/realized admit rate per cell; (9) state an MDE/achievable CI
half-width for H2 at 32 seeds, and that a null is inconclusive if the effect is below it.

**Four Codex criticisms — positions accepted subject to four sentences in §2(c):** (i) no identification claim from
(c); the 4θ map limitation and the 6-param ABC rank-4/6 are recorded elsewhere and not addressed; (ii) grade×urban cell
counts are a design check, not an estimation population (no empty synthetic cell); (iii) seed-MC uncertainty only, no
pooled/FE claim; (iv) no permutation inference / country blocking.

**Label:** NEW GENERATION — REPRODUCED SIMULATION; not a reproduction of the Gemini 1,640-run design; paper H2/H1
numbers remain AUTHOR-REPORTED baseline.

**A3 VERIFIED — LAUNCH CLEARED (2026-11-25).** Amendment A3 (commit `3d289fd`; prereg §6) and runner v2
(sha256 `6ac09cff84c06ec2ecbbc9d6461bfbdb1b6f0771bb07e298be278a99e0af4f77`) satisfy the three launch conditions and the
provenance fixes: primary `fail='track'` 5,120 runs + declared contest/S∈{.25,.70}/all vac0/both fees/32-seed
`fail='stop'` sensitivity 512 = **5,632 runs**; POST e=+1..+6; primary H2 = contest at vac0=.08 with paired-seed
bootstrap 5,000, MDE proxy, quota/vac0-curve/H1/Spearman secondaries, bar/bar_high exploratory, one-primary/multiplicity
and null rules; engine label 846c9e0, `year_t=T0`, per-run `event_log`, `unfired_events==[]`, gate r/alpha in
`gate_spec`, quintile×urban counts, applicants/seats/admit rates. Engine core `e111397b…` and spec file
`e5ddef6b…` verified in tree; runner compiles.

**Report conditions (non-blocking):** (1) compute the **stop-sensitivity H2** explicitly (runner v2 executes the 512
stop cells but does not compute their H2 — add `h2('contest','stop')` or compute in analysis); (2) assert
`d_lo['seeds'] == d_hi['seeds']` before zipping in `h2`; (3) report the design cohort window for the quintile×urban
counts as a design check only; (4) report H1 uncertainty if feasible; (5) report the achieved primary CI half-width
(MDE) and interpret a small/negative H2 as inconclusive-or-null. Result will be adjudicated against the prereg when
the grid completes; X-27 moves from amendment-pending to adjudicated then.

## 4F. Paper B NEW GENERATION — CF4 reversal confirmed, **with a participation-cost caveat** (100 matched seeds)

**Provenance (verified).** Corrected artifacts at `a4b0808`, re-aggregated from intact checkpoints (HK aggregation
bug fixed; **no rerun**): TRACKED **`cf801af8e07f9ebf615d075c42ec742f00d5a98a19a0e938005a3632e28836d3`**
(HK+KR, `total_runs=1,800`); SINGLE **`2b69fa08ea521c664bda59da4d6fce0d9b48d494d5cee793b69987795bef0330`**
(`total_runs=900`); provenance **`8f08164d08006d5c0225cd2115352270560806fe4055294ff16f453dd62e3301`** (campaign
2,700; wall 11,234.49 s; 8 workers). **Engine `98baf6b`** (pre-re-pin; 118-series numerics unchanged vs `846c9e0`);
spec content `c5f9e2de…`; 100 matched seeds; frozen parameters → **zero calibrated-parameter uncertainty**, seed-MC
only. The adjudicator's independent HK re-aggregation from the raw checkpoints matches the corrected JSON **exactly**
(max |mean diff| 0.0; all spend indices identical); KR-TRACKED/SINGLE match the committed summaries exactly. The
superseded defective artifacts (`14fc2a31…`, `697e7ca9…`, `cba8ee0f…`) must not be cited.

**Result (pre-stated criterion: spend index < 80 AND elite Q5 below same-jurisdiction baseline, both jurisdictions):**

| arm | HK spend / elite | KR-TRACKED spend / elite | KR-SINGLE spend / elite | both-jurisdiction Win-Win? |
|---|---|---|---|---|
| **CF4a** | **70.59 / 23.21** (base 24.82) | **73.13 / 22.16** (base 23.90) | **75.43 / 22.04** (base 24.08) | **YES** — primary and sensitivity |
| CF4b | 89.99 / 23.07 | 109.70 / 23.61 | 117.74 / 23.59 | NO (spend) |
| CF1b | 97.25 / 23.49 | 99.19 / 23.53 | 98.99 / 23.64 | NO (spend) |
| **CF3b** | **70.88 / 23.43** | **73.21 / 22.21** | **75.53 / 22.09** | **YES — single lever** |

**Explicit CF4 reversal.** Pre-repair 540: CF4a **failed HK** (48.64 > 46.36), CF1b the only pass. Repaired 540
(legacy gate list, 30 seeds): CF4a **passes both** (70.58/23.44; 72.48/21.47). New generation (frozen V540-FREEZE,
100 seeds): CF4a **passes both** (70.59/23.21; 73.13/22.16), and under KR-SINGLE (75.43/22.04). The reversal is
robust across two repaired-engine specs and 30 vs 100 seeds; the pre-repair failure remains reported as the prior
result and is not erased.

**FIRST-CLASS CAVEAT — substantial participation reduction; welfare interpretation unresolved.** The criterion is spend + elite share; it does **not** capture
participation. Under CF4a, K–12 participation falls **HK 61.93 → 48.60 (−13.33 pp)** and **KR-TRACKED 55.79 → 42.81
(−12.98 pp)**; G12 falls HK 49.37 → 39.14 (−10.23) and KR 36.25 → 30.56 (−5.69). CF3b has a similar drop (48.56 /
42.80). Correct phrasing: **"CF4a meets the pre-stated spend/elite criterion while reducing participation by ~13 pp"**
— not "win-win" unqualified. A ~13 pp K-12 participation fall under CF4a is an **unmeasured welfare change**, not automatically a welfare cost: it could be lost useful support, substitution by school-provided preparation, or families dropping low-value tutoring purchases. Interpretation requires learning/access/teacher-workload/student-time data that the programme does not yet have. The criterion's Win-Win is therefore an **accounting statement about spend and elite-Q5, not a welfare statement**.

The engine already implements the withholding / own-teacher / positional-vs-learning mechanisms, but Paper B's spec (`own_ban=0.95`, `mode=positional`) suppressed them; the emergence question is a separate, upcoming track (**Paper C**), not something Paper B answers.


**Uncertainty.** Paired-seed elite deltas for CF4a: HK **−1.62 [−1.73,−1.50]**, KR-TRACKED **−1.74 [−1.87,−1.61]**,
KR-SINGLE **−2.03 [−2.19,−1.87]**; spend-index seed CIs tight (CF4a HK [70.54,70.64], KR [73.07,73.19]). CF4b's KR
elite delta [−0.58,+0.01] includes zero (irrelevant: spend fails).

**Against the AUTHOR-REPORTED 420 tables and the repaired-540 migration.** 420 baseline elite HK 30.0 / KR 24.6;
**no CF4a/CF4b rows exist in the 420 tables** (the pairing claim was asserted, not tabulated); 420 CF1b 82.1/74.1
spend, 25.1/22.9 elite (HK spend > 80 → also fails); 420 CF3b 52.8/54.9 spend, 36.3/27.5 elite (regressive). New-gen
CF3b is **not** regressive (23.43/22.21) — the "wage compression is regressive" reading is contradicted; new-gen CF1a
spend 96.47/97.12 < 100 — "tax backfires on spending" is contradicted. New-gen baseline K–12 is 61.93/55.79, not the
420's 40.0/76.5; the generations are not interchangeable.

**Status: REPRODUCED SIMULATION (new generation; frozen spec; uncalibrated; seed-MC only).** Not VALIDATED. The
paper's "only pairing compression with caps/seats works" conclusion is **CONTRADICTED** (CF3b, a single lever, also
meets the criterion); the CF4 reversal itself is a **reproduced new-generation result**.

## 4G. Paper D — candidate new-generation finding (design audit; **no inventory equation is declared false**)

Artefacts: `docs/audit/PAPER_D_EQUATION_AUDIT.md` **sha256 `b6bafd1490b0a98df021f8b6ad1caff52b6ddf1a18b5606d4982ef8e1050a49d`**
(commits `02990f9` + `044f7d0`); inventory `docs/audit/refs/education-equation-inventory-20261124.txt` **sha256
`0fd30f770a75ee55cdf26d3ce332df795f78d29d070bed01af38810bfa4752df`**; companion
`docs/audit/PAPER_C_MODEL_GAP.md` **sha256 `d994df74d10ac2888e2646dad7f59469c8305cd308c644f3660a4b9192643ffc`**
(commit `02990f9`).

**Stance (binding):** the audit uses the engine as a mechanism-rich test bed; it **does not declare any inventory
equation false**. It separates:

* **Omissions (candidate gaps, not errors):** **M1** school-supplied effective preparation S; **M2** positional
  externalities with fixed seats; **M3** teacher-as-supplier withholding/rent extraction; **M4** student/teacher time
  budgets; **M5** supply-form choice (own teacher vs firm vs state). The engine evidence that each omission can
  matter is recorded in `PAPER_D_EQUATION_AUDIT.md` §3 (e.g. M1 q0 0.8→1.2 lowers K–12 tutoring 0.605→0.491 and spend
  161.7→135.9; M3 switching withholding on raises h 0→0.144 and own share 0.04→0.53; M5 firm ban moves own share
  0.53→0.98 and price 0.07→2.10).
* **Already-recorded contradictions (measured, not "inventory is wrong"):** KR G9 phantom prize (D1), expected ≠
  realised admission probabilities (D2), the 100 % seat-expansion paradox, and Paper B's pairing claim. These remain
  CONTRADICTED in this ledger for the reasons already recorded elsewhere.
* **Divergence tests D1–D9** each state a **standard-equation prediction X vs a mechanism-rich prediction Y**, the
  engine cell, the discriminating outcome and minimal compute (≈300–420 runs at N=600/T=30, ≈2–3 CPU-h; D3/D7 need
  wave-2 extensions; D1/D2/D4/D5/D6/D8/D9 are runnable on the current engine). They are **pre-registerable, not
  results**; no Paper D compute until the Paper C confirmatory run and an approved prereg.

**Attribution-risk checklist (binding):** the inventory is an **AI-generated candidate map with placeholder citations**
("UIS+2", "OECD+3", "doi.org+4", etc.). **No equation or citation may be used from it without primary-source
verification** (Hanushek; Todd & Wolpin; Cunha & Heckman; Becker; Mincer; Dang & Rogers; Bray; Tansel & Bircan;
Biswal; Jayachandran; Kim & Lee; UIS/World Bank/OECD measurement sources). Equation numbering refers to the committed
inventory text, not the published sources — cite sources, not inventory numbers.

**Status: candidate new-generation finding/section (design audit), UNRESOLVED as results.** The omissions are
pre-registerable hypotheses; the divergences are future work; the already-recorded contradictions remain as recorded.

## 4H. Paper C — design-only provisional anchors and the pre-registration gate

Artefact: `docs/audit/PAPER_C_MODEL_GAP.md` (sha256 `d994df74…3ffc`). The probes are **read-only host anchors**, not
adjudicated claims.

| anchor | value | reading |
|---|---|---|
| Paper B canonical = private-market regime | `withheld = 0.00000` (HK and KR); own-teacher share of tutored **2.47 % HK / 2.82 % KR**; K–12 tutoring 0.617 / 0.556; spend 156.5 / 128.3 | Paper B suppresses the withholding/own-teacher channel (`own_ban=0.95`, `mode=positional`); it is a firm-market regime |
| better school provision substitutes | `q0` 0.8→1.2 lowers K–12 tutoring **0.605→0.491** and spend **161.7→135.9** | the S-substitution channel Paper C needs |
| withholding regime ON (`pay_ratio=.55`, `monitoring=.2`, `own_ban=0`) | `h = 0.144`, own share **0.528**, K–12 tutoring 0.776, spend 165.0 | teacher withholding/rent is a live mechanism when enabled |
| withholding ON + `firm_ban=.9` | own share **0.978**, spend **118.1**, firm price **2.0957** | supply-form/ban interaction; firm price ×30 |

**Status of the anchors: REPRODUCED SIMULATION (provisional, design-only)** — they establish that the mechanisms
exist and are switchable; they are **not** Paper C results and must not be cited as such.

**Paper C confirmatory grid (pre-registration required):** 3 (S) × 3 (L) × 4 (private supply) = **36 cells** × 8
matched seeds = 288 runs + 4 regime anchors × 8 = 32 runs = **320 runs**; suggested N=600/T=46 screening (≈**2.2
CPU-h**; ≈20 min at 8 CPUs) and N=1500 confirmatory subset (≈12 CPU-h). **No box compute until a pre-registration is
approved.** When the Commander drafts it, review with the same four-criticism discipline: no identification
overclaim; grade×urban/design-cell counts only; seed-MC uncertainty; no permutation inference. **Paper D compute is
gated** on the Paper C confirmatory run and an approved prereg (Commander rule).

## 4I. Model Zoo / D1–D2 discriminators — pre-registration review (design-only; **no run yet**)

Artefact: `docs/audit/MODEL_ZOO_DISCRIMINATORS.md` **sha256 `5a67fcf1db9648dda02be88c3cedace5ff0818e9ad1dd8261cbabcd1caf1f48f`**
(commit `6e780c2`). Design-only; nothing has run.

**D1/D2 32-run confirmatory core (reviewed):** N=600, T=46, seeds 0–7 matched, HK base; D1A/D1B and D2A/D2B reuse
the four Paper C Pilot-0 **v3** cell definitions (N=1500 exploratory → N=600 re-execution; cell definitions reused,
results new). Optional D1C q0=0.8 (+8) and mechanism-grade D2 (+16).
* **D1 (S in demand vs demand-only):** primary paired Δ K–12 tutoring participation (D1B − D1A: q0 1.2 vs 1.0);
  standard/demand-only prediction **≈0 pp**, mechanism-rich prediction **≤ −2.0 pp** (probe prior −3.7 pp, spend
  −6.6 %). Decision/indeterminate rules: |Δ| < 1.0 pp → indeterminate (extend seeds, do not reinterpret).
* **D2 (cap vs withholding displacement):** primary paired Δ `own_share` (D2B − D2A: `own_open_gap` ± `firm_ban=.9`);
  X (reduced-form) predicts proportional spend fall, **own_share flat**; Y (mechanism) predicts **Δown_share ≥ +0.20**
  and firm-revenue collapse exceeding the spend fall; Δown_share < 0.05 → X not rejected/indeterminate in this regime.
* **Pre-registration content checked and adequate:** 12-item checklist (§6) — exact cells, seeds 0–7, one primary
  outcome per test + Holm-corrected secondary family, predicted signs/thresholds, decision/indeterminate rules,
  paired per-seed CIs, contamination declarations, no-op binding assertions, engine/spec hashes, exclusion rules,
  report-all-cells/no selective reporting.
* **Run gate (binding):** D1/D2 + the model zoo need **Codex's protocol/Kaplan confirmation** and this prereg review
  before any run; **no run may start until that lands.**
* **Pilot-0 script inconsistency (flagged):** the `run_paperC_pilot0.py` docstring says "96 runs / 3 supply regimes /
  `pay_ratio=0.8`", but the committed **v3 code** has **4 regimes (→128 runs)** and `pay_ratio=0.55`,
  `monitoring=0.2`, matching commit `fbc1991`; the prereg must quote **code + commit**, not the docstring. (Pilot-0 v3
  = 128 runs, not 96; earlier 96 was v2. The Commander is checking which version actually launched.)

**10-model zoo (reviewed):** ten candidates mapped to 2–3 observable predictions each, with five **discriminating
moment families** (gate pressure; school supply S; supplier availability; credential-vs-skill; time; state-vs-market).
Explicitly **UNFALSIFIABLE / data-blocked now:** (i) student/teacher **time allocation** (no time variables; engine
lacks the time budget); (ii) **Mincer returns** (no earnings in DHS); (iii) **withholding magnitudes / provider mix**
(no own-provider/teacher-pay data); (iv) **Kaplan-type firm profits** (no firm-market entry/price/profit data);
(v) **exact CES substitution sign** (needs `production='ces'` extension). DHS has no tutoring module → all
shadow-education moments are ILSA/CEPS/theory-only. **These are pre-registerable tests, not results**; the
unfalsifiable list is binding so that later no one claims those were tested.

## 4J. Evidence-layer limits for Papers C/D and the Model Zoo (binding)

Sources: `docs/audit/TUTORING_DATA_INVENTORY.md` (current sha256
`3469c644f7112e4b8de0c635e1ec72e7598b0a0c3b7ef0fb9e905fbc6cbe2608`; commits `f95164d`/`2c315c0`; the earlier
`a33fa368…` version cited by the Lead is superseded by the codebook-verification commits) and
`docs/audit/DHS_E1E8_MODEL_MAPPING.md` (current sha256
`7e27e83c38495bd160d2f055d53c43d20942c5da7053fe90a69e757c46b2d770`; earlier `11252df2…` superseded).

1. **HK-vs-PH 2019 supply-form is unobserved; SEA-PLM 2024 is a candidate route, not yet testable.** PISA 2018/2022
   gives tutoring participation/hours by ESCS quintile for HK/PH/CN but **no expenditure and no own-teacher-vs-firm
   item**; provider-type data exist only for **Korea** (KOSTAT survey). **The SEA-PLM 2019 parent questionnaire has NO
   tutoring item** (full 13 pages + 6-page codebook read; the earlier "KH route = SEA-PLM 2019" is **REFUTED**).
   **SEA-PLM 2024 framework p.89 item PA18 (verified text, D) is a 2×2 supply-form item: PA18A paid assistance
   outside school / PA18B free tutoring outside school / PA18C paid tutoring provided by the school / PA18D free
   tutoring provided by the school** — exactly the paid/free × outside/school distinction Paper C's supply-form claim
   needs; **SEA-PLM 2024 results/data are released (ILSA-Gateway), so 2024 may be usable pending KH/PH coverage +
   parent–student linkage/codebook checks (dataset presence/linkage still V).** Until that verification, Paper C's
   empirical leg is **feasible-partial (participation/hours only)** and the supply-form/withholding predictions remain
   **theory/simulation**; the blanket "theory-only" label is too strong and must be qualified. D/L/V: PA18 text =
   **D**; dataset presence/linkage = **V**.
2. **DHS E1–E8 cannot test the model zoo.** They contain no tutoring, learning, gate/seat, time-use, earnings or
   expenditure variables. They can weakly constrain demand-side distributional implications (wealth gradient sign,
   urban–rural gap, sex-gap reversal) and **falsify a proxy** (E8 household size ≠ kin support), but they cannot test
   tutoring demand, withholding, test-prep/state supply, positional-vs-human-capital, signalling, Hanushek, time
   allocation, or any policy-change prediction. **No model may "win" on DHS alone**; use DHS only as auxiliary
   descriptive targets in a separate evidence layer.
3. **D/L/V convention is binding:** `D` = documented snippet/committed file; `L` = located/access-route; `V` =
   verified item/source. **Nothing marked V may be asserted as fact** (the current inventory explicitly lists the
   remaining V items as unverified: PISA/SEA-PLM exact item wording, expenditure/provider confirmation, CIEFR/CFPS/
   CEPS access). Papers C/D must not imply the empirical leg exists.

## 4K. X-27 gate-architecture grid — RUN COMPLETE, AGGREGATION RUNNER DEFECT, ADJUDICATION PENDING

* **Grid complete:** 5,632/5,632 rows; 176 cell checkpoints (5,120 primary `fail='track'` + 512 `fail='stop'`
  sensitivity); no cell missing.
* **Driver crashed post-run at aggregation:** `NameError: name 'np' is not defined` in `h2` (runner line 201). The
  **grid and model ran to completion**; this is a **runner defect, not a grid/model failure**. **No simulation rerun is
  needed** — the checkpoints are intact; the Commander is re-aggregating from them (fix `import numpy as np`; commit
  the fixed runner; re-emit the JSON with runner commit + engine pin + spec hash + row/cell counts + checkpoint hashes).
* **Methods/negative-paper line (citable):** this is the **third bug of this class caught by reading raw artefacts
  rather than summaries** — (i) fee no-op (simulation-index vs calendar-year event), (ii) seed-0 hardcode, (iii)
  missing `np` import. Summary-level QA would have missed all three; raw-artifact inspection is the detection method.
  Add to the methods/negative paper.
* **Adjudicator independent re-aggregation (PROVISIONAL; pending the corrected artifact; NOT the adjudicated result):**
  primary H2 = contest, vac0=.08, `fail='track'`: **+5.0551 pp** (paired-seed bootstrap 95% CI **[2.482, 7.961]**;
  half-width 2.740); Δcut(S=.25) +5.617 [3.551, 7.884], Δcut(S=.70) +0.562 [−0.992, 2.086]. Secondary: quota H2
  **+0.9915** [0.5675, 1.4893]; contest vac0 curve **+3.105 / +5.055 / +1.145 / +0.325** (vac0 .02/.08/.25/.50);
  **H1 = +7.935 pp** with Spearman **−1.00** across S; stop-sensitivity H2 **+5.4715** [2.2078, 8.4476]; bar
  exploratory **−0.255** [−0.850, 0.325]; bar_high **+0.204** [−0.322, 0.763]. Full output
  `/tmp/adjud/gate_independent.txt`. These numbers must be cross-checked against the corrected JSON before any ledger
  move; X-27 stays **UNRESOLVED** until then.

## 5. Evidence-status register (programme level)

| Status | Count (paper + programme rows) | Notes |
|---|---|---|
| VERIFIED EMPIRICAL | **4** (4 A) | descriptive/associational; not causal; author committed E8 record |
| **REPRODUCED EMPIRICAL ANALYSIS** *(new-generation label, Lead-defined)* | **2** (2 A) | A-34 impact (+12.322 vs +12.44) and A-35 amplification (+25.083 vs +25.26) — fresh-WDI **CS-style group-time ATT**; manifest-hashed vintage |
| REPRODUCED SIMULATION | **23** (2 A, 12 B, 9 programme) | all conditional and/or uncalibrated unless marked; includes the 100-seed Paper B new generation (CF4 reversal + unmeasured-welfare-change caveat), the three Paper C provisional anchors (C-01…C-03), the new-generation forecast (A-37), the 74.88 % infeasibility finding (A-38), the re-executed ABC audit, the re-executed bootstrap factorial, and the Paper B 540 table regeneration |
| VALIDATED SIMULATION | **4** (1 A, 3 programme) | **A-39 item (d) local identifiability (stop gate met with declared restriction)**; engine/PL module validation, corrected DGP design, bootstrap size/power |
| AUTHOR-REPORTED | **44** (20 A, 18 B, 6 programme) | **AUTHOR-REPORTED BASELINE**: the 420 generation, the Paper A Exp 1/3/4/5 legacy numbers, the author JSON bundle; not results, not reproduced, not to be silently replaced |
| CONTRADICTED | **32** (8 A, 14 B, 10 programme) | only where committed code/algebra/measured audit output refutes the claim; includes the 100 % paradox, invalid E1/Q3, legacy DGP, "published benchmark" attributions, and the Paper B policy reversals |
| UNRESOLVED | **18** (2 A, 0 B, 16 programme) | A-31 replication inventory; A-36 bulge `t*` (no-effect evidence); Paper C confirmatory prereg (C-04); Paper D omissions/divergences (D-01/D-03) and inventory attribution risk (D-04); Model Zoo D1/D2 + run gate + Pilot-0 provenance (MZ-01…MZ-04); evidence-layer limits (EV-01…EV-04); canonical spec/Gate-2; GPU quarantine |

The machine-readable one-row-per-claim record is `results/audit/paper_claims.csv` (127 rows; sha256
`b50c9f36a0f34c42852ae8f76585d45734f204d699937d22b1b357db6dad892a`). The Lead-defined new-generation label **REPRODUCED EMPIRICAL ANALYSIS** is used for the fresh-WDI E8 rows; all
other rows use the verbatim six-status taxonomy.

---

## 5A. The repaired-engine runs are a **NEW GENERATION** (not a recovery of the 420 generation)

Per the operator decision, the repaired-engine results are framed as a **new generation** — a different model
generation with its own provenance, not a corrected version of the manuscript's 420 numbers. Everything below is
REPRODUCED SIMULATION, **uncalibrated**, not validated.

**Engine provenance.** Commit **`98baf6b`** (Gate-1 tree: `f31e176` gate1a + `6bc8d61` gate1b + `1a6f3d5`/`23a0173`
gate1c), archived in `/root/work/cmd/engine`. File hashes (`docs/audit/canonical_spec.json` / `GATE1_REPORT.md`):

| file | sha256 |
|---|---|
| `engine/eduengine/core.py` | `72cbddf7…` **(the repaired 540 was run on this hash)**; a later validation-only fix `846c9e0` gives `e111397bd8a50f94e82bb77715f236ee3d5c0bf863a23d84afdf1c6c71fa8e71` — numerics unchanged (118-series identical); **canonical spec re-pinned at `46c080d`** (content sha `280b5d95…`, file `e5ddef6b…`; 27-suite PASS; old-vs-new max|Δ|=0.0) |
| `engine/eduengine/rng.py` | `ada4a760d75a14f4d82a8aaf70964dee6a2f7f4130d53018ad190fafa4920b08` |
| `engine/eduengine/contest_math.py` | `23a01730bf939a9e22befa3ca395094a48c5e870fb10901ceb015cddd793a3c8` |
| `engine/eduengine/modules/labour.py` | `0ccfb3ce5b4c88fc2969909dbdbbc4d32184052fe5359688f96e00c2667b3f7d` |
| `engine/eduengine/modules/tutoring.py` | `7a6fd4c33cc2aefcd47da097b47ac7945744cc1adf9dedbb8ab1ec57d8adc2f8` |
| `engine/eduengine/planning.py` | `13d91bc9cc8c0bccbffb2caf8364b4a3376da582ece25f44fa1660380358987d` |
| `engine/eduengine/modules/schools.py` | `9b079280e0b01cc0681dfdb956b9cff8bcc82a9274f03263f209999bc7142745` *(still legacy sequential RNG - residual)* |
| `engine/eduengine/modules/sdg4.py` | `5ce05c8b3663f32169a8a1f8b2407e0d5418a9dca50fdd1cba1af7fb02e592be` |
| `engine/eduengine/modules/state.py` | `3c5500ae9b4fc5757be574e508a31b9d8627be979edc884d94d90cea60993068` |

**Design / gate definitions.** The 540 generation: `N=300`, `T=46`, `measure_from=18`, **18 arms x 30 matched seeds =
540 runs**; HK single G12 gate `share=0.23`; KR stacked G9 (`share=0.35`) + G12 (`share=0.12`). The frozen
`canonical_spec.json` is **V540-FREEZE** with `GATE_SPECS` = **KR-TRACKED primary / KR-SINGLE sensitivity** and the
hardened runner sha256 `932515ca...`. **The repaired 540 run actually used (`455649da...`) predates that freeze and
used the legacy 540 gate list** - so the regenerated tables are repaired-engine + legacy-gate-list, and the
frozen-spec V540 run is a **new Gate-2 job not yet executed**. State this wherever the regeneration is cited.

**What changed in the new generation** (`CODE_CHANGES.md`, `GATE1_REPORT.md` section 4):
* **D1** KR G9 phantom prize -> explicit persistent `k['track']` consequence (learning multiplier, later-gate weight,
  earnings premium); the legacy G9 prize is now *delivered*, not priced as a phantom.
* **D2** expected admission P changed from `1-exp(-lambda x^r)` (lambda re-solved to aggregate seats) to the **exact
  Plackett-Luce object**; pre-repair expected/realised = **2.41x (KR G12) / 1.96x (HK G12)** -> **1.0000** per gate.
* **D3** seat denominator `share` now of **applicants** (realised admit rate 0.513 -> 0.2500 in the invariant test),
  with per-gate applicants/seats/ratio/admit-rate/expected-P diagnostics.
* **D6** policy-invariant, event-keyed RNG (`rng.py`): 51 mismatched cohort-covariate groups -> **0**.
* **D4/D5** tax / outlay / receipt ledger split; `firm_rev` resource-only; per-gate `prep_stock`.
* **D7** labour prizes applied last, multiplicatively, to leavers and queuers; per-child `elite_prize`.

**The CF4 reversal (must be reported, old result preserved).** Pre-stated Win-Win criterion: spend index < 80 **and**
elite Q5 share below the same-jurisdiction baseline, **both** jurisdictions.

| arm | pre-repair 540 | **repaired 540 (NEW GENERATION)** |
|---|---|---|
| **CF4a** (delta-V -50 % + cap) | **FALSE** - HK elite 48.64 % > 46.36 % baseline | **TRUE** - HK 70.58 / 23.44 %; KR 72.48 / 21.47 % |
| CF1b (cap -50 %) | **TRUE (only arm)** - HK 67.39/41.96; KR 76.42/26.39 | **FALSE** - HK 97.21; KR 99.25 (spend >= 80) |
| CF3b (delta-V -50 %) | FALSE | **TRUE** - HK 70.88/23.64; KR 72.55/21.48 |
| CF4b (delta-V -50 % + seats) | FALSE - spend 90.88/88.04 | FALSE - spend 89.98/105.54 |

This is the single most consequential new-generation fact for Paper B: the combined-policy ranking **reverses**
(CF4a passes; CF1b fails), so neither the manuscript's "only pairing compression with caps/seats" nor the review's
"only CF1b" is an established result.

**Provenance of the new-generation run.** old (pre-repair) 540 = `results/audit/commander/hk_korea_540_commander_independent_2026-11-25.json`
sha256 `722c370b...af54`; new (repaired) 540 = `results/audit/commander/hk_korea_540_REPAIRED_box98baf6b_2026-11-25.json`
sha256 `455649da...ec21` (box cross-env, declared venv py3.10.8/numpy 2.2.6, 6 workers, 540/540 exit 0, 49.3 min);
migration table `GATE1_MIGRATION_TABLE.md`; regenerated tables `PAPER_B_TABLE_REGENERATION.md`. The host authoritative
run failed twice in the pool-completion phase; the box run is the labelled source.

## 6. Publishability, bluntly

### Paper A — *When Fee Abolition Meets Rationed Gates*

**Current combined manuscript: NOT PUBLISHABLE.**

* Publishable core: **the E8 abolition impact AND the delayed amplification** — author +12.44 / +25.26, and
  fresh-WDI **CS-style group-time ATT** **+12.322 / +25.083** (bootstrap CI [4.48, 22.64]; Fisher p 0.0044/0.0040;
  manifest-hashed vintage), labelled **REPRODUCED EMPIRICAL ANALYSIS**. Caveats: equal weights, no DR covariates,
  **8 clusters → wide CI**, fresh vintage; association-only wording.
* The earlier simple-DiD **+2.54 pp** is **estimator sensitivity**, not a contradiction; report it as a sensitivity
  check beside the CS-style result.
* **The bulge `t*` is a no-effect result on fresh data** (ATT −0.956 pp; Fisher p 0.251/0.384) — **UNRESOLVED**
  (no-effect evidence), consistent with the manuscript's honest-null framing; not a contradiction.
* **The forecast (Exp 5) is a new-generation conditional simulation** (A-37): fixed-engine run gives
  abolition − persistence **+17.19…+25.35 pp** (e=0..6), full-7 RMSE **2.764** vs persistence **23.759** (−88.4 %),
  held-out e=+5,+6 RMSE **1.637**. **Calibration caveat:** the author's **74.88 % anchor is infeasible** in the
  repaired world (max 71.0 % at fee 0; A-38), so the run uses a declared fallback (fee 0.15, engine pre-abolition
  level, no post tuning) and is **not** a reproduction of the author's calibration. v1 numbers remain uncited.
* Not publishable: the identifiability "theorem", the 1,640-run H2 experiment, the simulator forecast, Table 3, and
  the causal framing; the one independent recomputation contradicts the headline identifiability numbers.
* Salvage plan: **Paper A1** = short empirical paper on the **abolition impact**, with the estimator-dependence of the
  amplification explicitly reported (or the CS re-run on fresh data added first). **Paper A2** = measurement
  proposal as a pre-registration / conjecture with an independently computed local-rank appendix and the corrected
  DGP design, with no "theorem" language.

### Paper B — *Why Tutoring Taxes Backfire and Expanding Elite Seats Fuels the Arms Race*

**Current manuscript: NOT PUBLISHABLE.**

* Every causal/counterfactual headline is either (i) from the non-reproducible 420 generation, (ii) a D2 artefact,
  or (iii) spec-dependent to the point of sign reversal. The tables are not the reproduced run, and the reproduced
  run is not calibrated.
* **The new generation now gives a coherent, citable core for a methods/negative paper:** the CF4 reversal is
  reproduced on two repaired-engine specs and 30 vs 100 seeds (CF4a meets the pre-stated spend/elite criterion in
  both jurisdictions, **while participation falls ~13 pp**; CF4b/CF1b fail spend; **CF3b, a single lever, also
  meets it**, so "only pairing" is false); the D2 migration explains the pre-repair calibration failure; the
  100-seed run has seed-MC uncertainty only (frozen parameters, zero parameter uncertainty).
* The methods/negative paper is honest and useful, but it still requires Gate-2 calibration + Gate-3 policy re-runs
  for any calibrated policy claim, and it must not use "win-win" without the participation reduction and its unresolved welfare interpretation. It is not the paper
  currently written.

### Do not submit either draft. Do not cite the 420 tables, the H2 numbers, the identifiability theorem, the
simulator RMSE, the `t*` null, or any GPU/ABC output. For Paper B, the **new-generation** table
(`cf801af8…`) may be cited — with the participation-cost caveat — but not the 420 tables.

---

## 7. Required sequence before any submission or citation

1. **Freeze/re-pin the canonical spec** (operator decision; recommended 540 parameterisation on the repaired engine
   with explicit `GATE_SPECS`, 420 documented as alternative). **Re-pin to engine commit `846c9e0` / `core.py`
   `e111397b…`** after the mid-run-calendar-event fix (numerics unchanged vs `98baf6b`, 118-series identical), and
   record the `E.unfired_events == []` assertion for every forecast/event arm. `GATE2_PLAN.md` §1/§1b;
   `ENGINE_MIDRUN_EVENTS.md`.
2. **Finish runner hardening** (`task-13`) so a Gate-2 campaign cannot lose a run.
3. **Gate-2 calibration** against the benchmark registry only (sourced moments; derived targets marked; KR 2025
   held out; no target without a source). Report the residual honestly — gap/ratio and, especially, participation.
4. **Gate-3 policy re-runs** on the calibrated canonical spec: all arms including CF4a/CF4b, with seed uncertainty;
   report the CF4 verdict and its spec-dependence.
5. **Repair the papers** per `MANUSCRIPT_ERRATA.md`; every table/figure regenerated from the canonical result file.
6. **Deposit the replication packages**: Paper A Exp 1/3/4/5 (WDI extract, runners, seeds, raw outputs, hashes);
   Paper B's 420 runner or a documented 540-only re-specification; the 540 runner + engine commit + seeds already
   exist.
7. **Keep the audit's new findings as a separate methods paper** (D2 artefact, CF4 spec-dependence, ABC/DGP failure,
   invalid E1/Q3 inference) — do not bury them as caveats in either manuscript.

---

## 8. What this audit itself does NOT establish (honesty about the audit)

* The repaired engine was **not calibrated** in Gate 1. The migration is REPRODUCED SIMULATION, uncalibrated, not
  VALIDATED, and not a policy result.
* The repaired 540 run's source was the **box cross-environment run** because the host authoritative run failed
  twice in the pool-completion phase; outputs and hashes are recorded, but the host run is not the source.
* **A7 residual**: future-gate expected probabilities use the current sitting cohort's curve (interpolated);
  `share=1.0` is no longer literally universal; quota expected-P still uses a normal-CDF at a lagged cutoff.
* `schools.py`/`anchor.py` still use the legacy sequential RNG — residual path dependence.
* **No GPU campaign** was authorised; GPU conclusions remain quarantined; GPU-vs-CPU agreement is arithmetic only.
* The E8 empirical block was verified against committed records on other branches; this adjudication did **not**
  re-estimate the WDI panel or re-run the CS/RI/gender pipelines. The records' own reproduction gates passed.
* The Paper B direction findings (B-17, B-18, B-35–B-39) are **direction-only**; magnitudes are generation-specific
  and not validated.

---

## 9. Explicit "do not cite" list (after this adjudication)

1. Any Paper B table or figure from the 420 generation, or the 420 self-reported JSON as a run.
2. Paper A Exp 3 H2/H1 numbers, Table 2, Figure 2 (no artifact; provenance broken).
3. Paper A Exp 1 `t*` null and "prove too coarse" (no artifact; committed record says NOT-ESTIMABLE).
4. Paper A Exp 4 rank 5/7 → 7/7, condition numbers, "theorem", posterior-correlation-condition-number evidence.
5. Paper A Exp 5 RMSE/forecast numbers, Table 1 simulation columns, Table 3, the 70 %/<1 % baseline claims, and
   "validates out-of-sample" until deposited and reproduced.
6. Paper B "tutoring taxes backfire", "wage compression is regressive", "only CF1b", "only combining reaches
   win-win", "reproduces the medical-seat shock", "exact same policy hierarchy", "calibrated across 420 runs".
7. Any GPU-bundle output as a calibration, 7-parameter identification, contest boundary map, or E1/Q3
   reconstruction; the "100 % seat-expansion paradox".
8. The pooled E1/Q3 selftest or the shipped country-block permutation as inference.
9. The legacy 7-parameter ABC as identified, and the legacy synthetic DGP as an identification base.
10. Any causal reading of the E8 association ("fee abolition lifts GER") — the empirical record permits only
    "consistent with".
