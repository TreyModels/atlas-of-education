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

**Citation-verification evidence (engine-tutoring, commit `3d8b80a`; `CITATION_VERIFICATION_SHADOW_ED.md` sha256
`020ece4f08c00c5b82325fee5d3a98671b903676a7239a2557cb0a0156d9ef45`):** **0 of inventory §5 equations (57–86) are
verified quotations** of any named source; every "citation" is a **placeholder** (`UIS+2`, `OECD+3`,
`hanushek.stanford.edu+2`, `doi.org+4`, …); one **false publisher** is attached (`RCNi Company Limited`, a nursing
publisher, to Becker & Lewis 1973). The named sources contain (Dang & Rogers 2008) a graphical framework + one
unnumbered naive OLS, (Tansel & Bircan 2006) a Tobit expenditure model, (Bray 1999/2009) monographs with no
equations, (Kim & Lee 2010) a demand/positional empirical study, and (Biswal 1999) text not retrieved. **Jayachandran
(2014, JDE 108:190–205) — full published text read — DOES model teacher withholding** (school-day material `m`,
achievement `s(m,t)` with `s_mt<0`, teacher effort/penalty `φ(m)`, and kickbacks/coercion in an earlier version) but
**inventory E57–E86 contains no `m`, teacher-effort, or withholding/detection equation** → direct textual support for
the **M3** omission lemma (and the M1 school-day-material gap). Correct DOIs/pages are listed in the report; this
does **not** make the inventory equations citable.

**REFS/DOIs register (citation/register pass, commit `f77e8f1`; `REFS_DOIS.md` sha256
`9ecf1a67ab82bb7e80c9c1a60e3ce6a3efc5dc3ae349effc769373127573989e`):** one row per source cited anywhere in the
audit corpus — **52 sources**: **27 Crossref DOIs**, **1 dataset-DOI family (CEPS)**, **20 no-DOI book/report/data rows**
(ISBN or publisher recorded), **0 unregistered DOIs**, **0 unflagged citation-like mentions**. The register separates
(a) verified records (e.g. Dang & Rogers `10.1093/wbro/lkn004`; Tansel & Bircan `10.1016/j.econedurev.2005.02.003`;
Jayachandran `10.1016/j.jdeveco.2014.02.008`; Biswal `10.1111/j.1746-1049.1999.tb00232.x`; Kim & Lee `10.1086/648186`;
Dang 2007 `10.1016/j.econedurev.2007.10.003`; Callaway–Sant'Anna `10.1016/j.jeconom.2020.12.001`; Sun–Abraham
`10.1016/j.jeconom.2020.09.006`; Todd–Wolpin `10.1111/1468-0297.00097`; Cunha–Heckman `10.1257/aer.97.2.31`;
Becker–Lewis `10.1086/260166`; Spence `10.2307/1882010`; PISA 2018 `10.1787/b5fd1b8f-en`, 2022 `10.1787/53f23881-en`);
(b) **no-DOI books/reports** (Becker 1964, Mincer 1974, Hirsch 1977, **Caplan 2018 [model-zoo tag V]**, Bray 1999/2009,
Bray & Lykins 2012, Tullock 1980 original, Hanushek 1986, plus DHS/UIS/World Bank/OECD/SEA-PLM/KOSTAT institutional
sources); (c) **unverified** sources (Biswal paywalled, Dang 2007 paywalled, Kim & Lee abstract-only, "Hanushek" cited
without year/title, benchmark moments **KEDI 2024/2025 + HK 2011/12 already DROPPED at G2-A**, KEIA/SBS/SeoulStart
secondary material). **The 183-equation inventory's placeholder citations are explicitly excluded** from the register
(candidate map ≠ bibliography, per the attribution rule). `PAPER_D_EQUATION_AUDIT.md`, `MODEL_ZOO_DISCRIMINATORS.md`
and `MODEL_ZOO_SCOPE.md` now end with DOI/ISBN cross-reference sections; **no DOI was invented**, no manuscript/claim
was altered, and no box job was run. **Status: register only — no claim is upgraded by being listed; Caplan 2018 stays
V; verified source DOIs do not make the inventory equations citable.**

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

## 4I. Model Zoo v2 / engine probes EP-1–EP-2 — pre-registration review (design-only; **no run yet**)

Artefact: `docs/audit/MODEL_ZOO_DISCRIMINATORS.md` **sha256
`bd0bf29efe6705b029937cbaf6aa5c886c1196a1911f06998ab6671bc2a2eeb1`** (commit `9035547`), superseding v1
(`5a67fcf1…`, `6e780c2`). Design-only; nothing has run.

**Reclassification (Codex/Lead, binding):** **D1/D2 are ENGINE PROBES, not named-theory discriminators.** Omitting S
from a demand regression is not the same as a zero true response; `q0` shifts **both** public and private quality; and
the Lean omission lemma is **definitional invariance**, not an empirical magnitude claim.

* **EP-1 — matched public-feedback intervention** (mechanism probe, not a theory test): arms C0 (none), **P**
  (`school_feedback=x`, `feedback_intensity=0` — the declared inert toggle / **no-effect negative control**, must be
  **bit-identical to C0** on every declared outcome, pre-run assertion), **T** (`feedback_intensity=1`, public basic
  schools only, costed in teacher marking time — manipulation check S>0 and marking hours increase), B (`q0` raised to
  the same average quality increase — declared **bundle** contrast showing why `q0` cannot isolate public S). Matched
  seeds **100–131**, same cohorts and teacher-time budget in P/T. Primary: Δ K–12 tutoring participation T−C0, with
  P−C0 as the negative control; secondary: spend, absolute own/firm counts/spends, L6/L9, fixed-R gap-close and rank-R
  admission probability, gap_by_q, teacher marking hours. **STATUS: NOT RUNNABLE TODAY** — the engine has no positive
  public-school effort/preparation lever; requires the wave-2 `school_feedback` extension. A "mechanism absent" result
  is an engine-geometry limitation to report, **not** evidence about the world or a named theory.
* **EP-2 — own access × firm constraint 2×2** (mechanism probe): E00 (own_ban .95, firm_ban 0; own-closed/firm-open
  baseline), E01 (.95/.9), E10 (0/0), E11 (0/.9); fixed `q0=1.0`, `p_firm=0.08`, HK base, **seeds 100–131 matched
  across all four cells**. Primary `own_share_financial` (own vs firm among **financial** tutoring; contest-only pupils
  excluded from the denominator; absolute own/firm counts and spends also reported), E11−E10 with E01−E00 as the
  contamination-matched control; pre-registered DiD participation sign `(E01−E00)−(E11−E10) < 0`; binding assertions
  E10/E11 `withheld>1e-3`, E00/E01 `withheld<5e-3`, and `own_count+firm_count+contest_only_count==tutored_count`.
  `firm_price` reported but **not** mechanism evidence. **STATUS: NOT CONFIRMATORY-RUNNABLE** until the additive
  reporting series land (fixed denominator + `contest_prep_class` + absolute counts/spends); switches exist.
* **Seeds:** **0–7 = EXPOSED/exploratory** (Pilot-0 v3, never confirmatory); **confirmatory = 100–131 (32 matched,
  frozen, disjoint)**; no seed in both blocks.
* **A/R formalism shared with Lean:** `gap = max(0, R − A)` is definitionally `LeanStarter.gap`; capacity feasibility
  `Feasible required capacity`; fixed-R and rank-R predictions reported separately, never pooled.
* **Row 8 "Kaplan" → Bryan Caplan (probable, UNCONFIRMED, tag V):** signalling/human-capital-critique model (likely
  *The Case Against Education*, 2018); **must be primary-source verified before being cited as Caplan**. Protocol =
  **both competing models on the same evidence (Mode A) AND complementary modules (Mode B)**; outcomes
  holds/fails/indeterminate/not-testable; no straw man. If "Kaplan" means Kaplan, Inc. or Kaplan–Meier, §5.1 says what
  changes (industry case / estimator, not a general theory).
* **Runnability matrix:** EP-1 blocked on the wave-2 public-only S lever; EP-2 blocked on the additive series;
  model-zoo *competing* tests need EP-1/EP-2 + external data; *complementary modules* are design-ready but
  model-fitting is not in-engine "evidence". **No run** until (i) the Paper C prereg is amended per its residual items
  + Codex protocol/Kaplan confirmation, (ii) this probe design is signed off, (iii) seeds 100–131 + engine/spec/runner
  hashes are frozen, (iv) capacity is allocated.
* **UNFALSIFIABLE/data-blocked list retained:** time allocation; Mincer returns (no earnings); withholding magnitudes/
  own-vs-firm provider mix (no own-provider/teacher-pay data); firm profits/entry (no firm-market data); exact CES
  substitution sign. Empirical validation requires external data; engine-simulated moments are **not** empirical
  evidence. The list stays flagged so later nobody claims these were tested.

**Status: design-only, pre-registerable probes, not results.** EP-1/EP-2 are recorded as engine-mechanism probes; the
D1–D9 "named-theory discriminator" framing is withdrawn. **DOI/ISBN cross-references are now in
`MODEL_ZOO_DISCRIMINATORS.md`/`MODEL_ZOO_SCOPE.md` pointing at `REFS_DOIS.md` (commit `f77e8f1`); Caplan 2018 remains
`V` (unverified citation) and no source listing upgrades a model claim.**

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

## 4K. X-27 gate-architecture grid — ADJUDICATED AGAINST AMENDMENT A3 (provisional until clean re-run)

**Artefact (verified):** `/root/work/gate846/results/gate_architecture_results.json`, **294,532 B**, sha256
**`685db398a9e6052446312e6dacfc2b06f09aa809d60b2f2b145e8e6cf2453f40`**; `runs 5632`, `n_cells 176`, aggregation
wall **7.63 s** (all cells skipped from existing checkpoints — **no simulation rerun**). Provenance in JSON: engine
**`846c9e0`**, core `e111397b…`, spec `e5ddef6b…`, runner `92d3055e…`, `event_key year_t`, `unfired_events_asserted
true`, N=300/T=20/T0=12, 32 seeds, fail routing track primary/stop sensitivity, pre-stated primary/quota/secondary/
exploratory multiplicity, null rule recorded. **Cross-check:** every primary/secondary/H1/bar number matches the
adjudicator's independent checkpoint re-aggregation **exactly** (all diffs 0.0).

**Provenance (clean re-run confirmed):** the provisional JSON (`685db398…3f40`) was produced by executing the
unmodified script logic with `builtins.np = numpy` injected (no simulation code edit, no seeds recomputed) because the
deployed box runner copy lacked module-scope `import numpy as np`. The **clean re-run** with a literal module-top
`import numpy as np` (runner `cbdea3cd…`, aggregation-only 13.5 s, 5,632 runs from the same checkpoints) produced
**`bce3da363afbdcfd16052d2c661107dc8c88d082d640625ef1b0b334d8f72638`**; a NaN-aware semantic diff shows **only
`metadata.runner_sha256` and `metadata.elapsed_seconds` changed — every result is identical (diff 0.0)**. The clean
artifact is committed at `results/audit/newgen/gate_architecture_results.json` (+ `docs/audit/GRID_X27_NOTE.md`);
the injection note is **superseded provenance**, retained only for lineage.

**Amendment-A3 adjudication (pre-stated rules):**
* **Primary H2 = +5.0551 pp** (contest, vac0=.08, `fail='track'`; Δcut(S=.25) − Δcut(S=.70)); paired-seed bootstrap
  95 % CI **[2.4820, 7.9614]**, **half-width/MDE proxy 2.7397**. |H2| > MDE and the CI excludes 0 → **primary met**
  (positive: the fee-abolition gap effect is larger at low seat share than high). Δcut(S=.25) = **+5.6170** [3.5509,
  7.8840]; Δcut(S=.70) = **+0.5619** [−0.9924, 2.0855] — the high-S effect is not separated from zero, which is where
  the H2 contrast comes from.
* **Secondary quota H2 = +0.9915** [0.5675, 1.4893] — positive but ~5× smaller than contest, supporting an
  architecture-specific (contest vs quota) contrast, not a generic "any gate" effect.
* **Stop-sensitivity (contest, `fail='stop'`) = +5.4715** [2.2078, 8.4476] — positive and similar to primary;
  the result is **robust to the fail-routing sensitivity factor**.
* **Per-vac0 Δcut curve (contest, track):** +3.105 / **+5.055** / +1.145 / +0.325 at vac0 .02/.08/.25/.50 — non-monotone
  with a peak at .08; **the primary vac0=.08 was pre-declared**, the whole curve is reported, no post-hoc switching.
* **H1 = +7.9350 pp** [6.9585, 8.9127] (fee=0 gap_delta(S=.25) − gap_delta(S=.70)); **Spearman = −1.00** across S
  (fee=0 gap_delta by S: +1.017, −2.498, −5.033, −6.432, −6.918) — monotone widening as seats shrink, as pre-stated.
* **Exploratory bar/bar_high:** bar H2 = **−0.255** [−0.850, 0.325]; bar_high = **+0.204** [−0.322, 0.763] — no
  evidence either way (CIs include 0); reported only as exploratory, **never as the paper's H2**.
* **Null rule:** the pre-repair +0.1086 is the **AUTHOR-REPORTED baseline, not a target**; the repaired-engine
  +5.055 is the new-generation result, not a "failure" to match +0.1086.
* **Four Codex criticisms:** no identification claim is made from (c); grade×urban counts are a design check only
  (reported; no empty synthetic cell enters an estimator); uncertainty is seed-MC only; no permutation inference or
  country blocking. All four recorded in the JSON metadata and honored here.

**Prereg deviation / diagnostic gap (declared):** `design_diagnostics` realized admission rates are **NaN for every
cell** — `contest_candidates`, `contest_seats`, `contest_admitted`, `contest_applicant_seat_ratio`,
`contest_admit_rate` are all NaN in the **raw checkpoints themselves**, not just the aggregated JSON; only
`quintile_urban_cells` and `gate_spec` (r/alpha/cut0/share) are valid. Therefore the pre-registered requirement to
report **realized admission rates** for bar/bar_high (and contest) is **not met**; re-aggregation cannot recover them
(the series were never recorded). The **primary and secondary estimands do not use these series** and are unaffected;
a future rerun with the diagnostic series enabled would be needed to report realized admission rates. Recorded as a
**diagnostic gap / prereg deviation, not a model failure**.

**X-29 diagnostic — COMPLETE / RESOLVED (2026-11-25).** `results/audit/newgen/gate_architecture_diagnostic.json`
sha256 **`57889777afd358adce843d7f2b35acfb037d1439d195643223a30bd7f2e78652`** (72,947 B), **1,280 runs** = 40 contest
cells (S .25/.35/.45/.55/.70 × fee .19/.00 × vac0 .02/.08/.25/.50) × 32 seeds, engine `846c9e0`/core `e111397b…`/spec
`e5ddef6b…`, runner `e5c4075c…`, aggregation-only. **Per-level `nanmean` extraction restored admission diagnostics in
40/40 cells** (`contest_candidates/seats/admitted/applicant_seat_ratio/admit_rate`; first-cell admit_rate 0.2517; range
0.2500–0.7067; `applicant_seat_ratio` and `gate_spec` r/alpha present). **DIAGNOSTIC-ONLY, separate `results_diag/`, never
mixed with X-27 primary/secondary**; the primary H2 fields are identical to X-27 (diagnostic does not alter them). Recovery
was **aggregation-only** — the run completed 1,280/1,280 rows, an arch-filtered `KeyError: 'bar'` was fixed with an
arch-aware exploratory dict, no simulation rerun. **No admission number was cited before this artefact.** Bar/bar_high
contest-admission series are not applicable. **X-29 CLOSED — diagnostic met; not a primary/secondary result; no effect on
X-27.****Status: CLOSED — REPRODUCED SIMULATION** (pre-registered confirmatory new-generation simulation; frozen spec;
uncalibrated; seed-MC only) — **explicitly NOT VALIDATED**. X-27 is closed on the clean re-run
(`bce3da36…`; identical numbers, diff 0.0); the **X-29 admission-rate diagnostic gap is now RESOLVED** (diagnostic-only artefact `57889777…`; 40/40 cells
with admission diagnostics, never mixed with X-27) — X-29 closed; X-27 primary/secondary unaffected.

## 4L. Paper C confirmatory pre-registration — FOUR-CRITICISM REVIEW (**CONDITIONAL; amendments required before preregistered-final**)

Draft: `docs/audit/PAPER_C_CONFIRMATORY_PREREG.md` sha256
`10406a33dcc8bbd51392907291950ceaf96e02a9196c34424f7f5ffef8e94bf7` (commit `2e69339`). Design-only; **no compute
authorized**; Pilot-0 v3 (128 runs) is correctly declared **EXPLORATORY** and excluded from confirmatory evidence. The
design is materially better than the Paper B-generation specs (explicit factors, one-primary-per-test intent, binding
assertions, contamination declarations, MDE/indeterminate rules, evidence layering, compute cap). **It is not yet
preregistered-final**; the following must be amended.

**BLOCKING (must be fixed before preregistration-final):**
1. **The 36-cell appendix table is missing.** §1 promises "cells declared in the appendix table" but the file has no
   appendix; the six private-supply configurations, the pay_ratio/monitoring pairing, gate kind(s), `contest_r`
   placement and per-cell seeds are not enumerated. Without it "no post-hoc cells" cannot be audited. Attach the full
   36-row table (S, L/gate kind, own_ban, firm_ban, pay_ratio, monitoring, contest_r, seeds, expected assertions).
2. **One primary outcome per test is violated in T3 and T4.** T3 lists "withheld `h` and `own_share`"; T4 lists
   "Q5−Q1 spend gap / participation". Pick exactly one primary per test; move the other to a pre-declared secondary
   family with Holm or mark exploratory. (T1 and T2 already have one each.)
3. **T4 overclaims "positional but not via learning."** The design does not use `contest_prep_mode='learning'` and T5
   is declared wave-2/not-testable; therefore T4 can only show that gate pressure raises the gap/participation, **not**
   that the channel is positional rather than learning. Rewrite T4 as "gate pressure raises Q5−Q1 spend gap (or
   participation), consistent with positional demand; the positional-vs-learning decomposition is not testable in this
   design (T5 wave-2)".
4. **Two-stage screening→confirmatory selection is not handled.** "N=1500 confirmatory only for cells passing
   screening (|effect| ≥ min effect)" selects on the observed effect → winner's-curse/conditional bias. Amend either
   (a) run **all 36 cells** at confirmatory N (recompute cost), or (b) pre-declare **disjoint seeds** (screening 0–7,
   confirmatory e.g. 8–23), a fixed pass rule and an explicit "screening-confirmation, selection acknowledged"
   label; do not present a selected subset as independent confirmation.
5. **The four Codex criticisms are only in the covering message, not in the prereg.** Add an explicit section: (i) no
   identification/rank claim (the 4θ map and 6-param ABC rank-4/6 are recorded elsewhere and not addressed); (ii)
   grade×urban cell counts reported as a **design check only** (no empty cell enters an estimator); (iii) seed-MC
   uncertainty only, no pooled/FE selftest claim; (iv) no permutation inference/country blocking.
6. **T1 is not a clean S-substitution test.** `q0` scales **both** public and private school quality (the prereg says
   so); therefore the T1 contrast is a **quality-bundle** effect, not public school provision S. Rename/qualify T1
   ("q0 quality-bundle substitution; cannot isolate public-only S") or add a public-only lever (not available; wave-2).
   The −3 pp minimum effect also needs a power justification.
7. **T2/T3 contrasts and `own_share` definition are underspecified.** T2 must state the exact cells (e.g., own_ban=0,
   pay_ratio=.55, monitoring=.2, same S/L, firm_ban .9 vs 0) and the `own_share` formula/denominator; the declared
   mixing of contest-prep with firm tutoring must be carried into the estimand (or a clean `tut_own_by_grade`-based
   robustness check). T3's "vs market-only" is near-trivial because market-only has own_ban=.95 (own_share≈0 by
   construction); use a meaningful control (own-open, withholding off, pay_ratio=1.2) and treat h>0/own_share>0.1 as
   **binding assertions, not outcomes**.
8. **Provenance/stop rules missing:** freeze and commit the runner **before launch** and record runner/engine/spec
   hashes in every output; commit the analysis script; pre-declare exclusion rules, assertion-failure handling (invalid
   cell reported, not silently dropped), stopping rules, and confirmatory seed disjointness.

**RECOMMENDED (amend before final, not necessarily blocking):**
9. Pre-declare **power/MDE per test** (T1 −3 pp, T2 +0.10, T4 threshold) at 8-seed screening and 16-seed confirmatory;
   otherwise screening is directional/descriptive only.
10. Pre-declare secondary outcome families and their Holm/exploratory labels (currently only "all other outcomes
    secondary/exploratory").
11. Clarify **L**: which gate (G6→G9 share vs bar-threshold pair) and where `contest_r ∈ {1.2,1.6}` sits (separate
    factor → grid size changes; fixed → justify).
12. Declare the **4 regime anchors'** role, seeds and compute (not used in T1–T4); recalibrate the ≤7 CPU-h envelope
    with Pilot-0 measured costs before launch.
13. Tag evidence status **D/L/V** for PISA 2022 ST297, SEA-PLM 2024 PA18A–D, CIEFR-HS/CEPS/CFPS; keep the empirical
    leg feasible-partial (participation only) and withholding/S/learning theory-only. X-29 diagnostic rerun separate.
14. Add "no result means the model is wrong" wording (holds/fails/indeterminate-by-context) and negative-result
    preservation explicitly to the prereg body, not just the checklist.

**Verdict: CONDITIONAL APPROVAL — not cleared for preregistered-final.** No confirmatory compute until (a) these
amendments land, (b) the four-criticism section is in the file, and (c) Codex's protocol/Kaplan confirmation arrives.
The design's core (orthogonal factors, one-primary intent, binding assertions, seed-MC, evidence layering) is sound.

## 4M. Lean verification track — **methods artefact (X-30); the engine is NOT formally verified**

Artefacts: commit `4d42101`; `docs/audit/LEAN_VERIFICATION_SCOPE.md` sha256
`9f31108e496fdc3ac9509547ea388128d156188df9b0540c486d4406d1d3f23c`; `LEMMA_LEDGER.csv` sha256
`840945ffcef2698cdc1093b145e0d9b902a7af44f6f8d4af3ab031205e755940`; `LEMMA_LEDGER.md` sha256
`c9bb869173d833166f0d7d802e84bd700da14d7e7c059b15c0745e97692d70c2`; baseline
`LEMMA_LEDGER_BASELINE.json` `77098a5d…` (current 132-row baseline `07f83156…`; prior 130-row `f2ce655e…`, `b990c99f…`,
`3ff88d39…`, `55f75eea…` pins preserved in git history, not rewritten).

**Answer to "can we run everything against Lean?" — NO, and claiming so would be false.** The scope doc is explicit:

* **Tier 1 (recommended and prototyped):** accounting identities, budget/teacher-salary ledger, seat-share
  denominators, prep-stock recursion, tax/resource ledger, gate accounting, and the **inventory/omission lemmas**
  (each Paper D omitted channel M1–M5 as a *definitional invariance* theorem of the classical demand equation).
* **Tier 2 (conditional on CI Mathlib):** general-n Plackett–Luce top-K identities. **Mathlib is not installed on this
  host** (multi-GB cache/oleans, not viable against the free disk/RAM); Tier 2 is **CI-only**. The n=2 symbolic seed is
  done.
* **Tier 3 (NOT Lean-provable as theorems):** float32 numpy numerics, DID/bootstrap *inference*, the 5,632-run outputs,
  and empirical claims about the world. These are **computations/data claims, not theorems**; they stay
  reproducible-artifact evidence under hashes and tests.
* **Architecture:** Lean-verified reference mathematics + differential tests + reproducible artefacts. **That is not
  "the engine is verified".** Theorems are about the model objects; empirical claims are `EmpiricalClaim` records with
  artifact hashes, never asserted as theorems. **Unproved ≠ false; empirical ≠ theorem.**

**Prototype (measured, Lean 4.36.0; `lake build` 16 jobs PASS, 0 `sorry`, `#print axioms` for every theorem → only `propext`, 0 prohibited/non-standard axioms, Mathlib unused):** proved
`budget_ledger_identity`, `tax_revenue_le_base`, `seat_count_positive`, `prep_recursion_closed_form`; finite PL n=2
(`pl_top1_sum_eq_denom/_min`, `pl_topK_selected_sum`); Kind-3 `decide` lemmas for the **A-34 tolerance, A-38
infeasibility, B-41/B-42 Win–Win accounting cells**; **five omission/independence lemmas**
`classical_demand_ignores_{school_supply, positional_seats, withholding, time_budget, supply_form}` (Paper D M1–M5)
plus `D02_paradox_not_universal` counterexample. **LEMMA_LEDGER (current):** **132 rows** (18 declared + **114** explicit NOT-YET) frozen to the current
**132-row baseline `b990c99f…`** (ledger `3e9dbbc1…`; generator `--expect-sha/--expect-rows` pin enforced);
differential Lean↔Python bridge **9/9 exact fixtures**; CI hook (`lake build`, comment-aware `sorry` scan, axiom
allow-list, 18/18 claim-id check) PASS. The earlier 130-row pair (`f2ce655e…` + `da956fc1…`) is preserved in git
history; **drift resolved at `54b1f74` / audit-runner `4c06025`**.

**QA mechanical audit — FINAL PASS, re-affirmed after the X-29 status-only re-pin (recorded):**
`docs/audit/LEMMA_LEDGER_AUDIT.md` at QA commit `b176c1c` (audit-runner re-pin `5c485c0`): **R1–R8 all PASS** on the
current pair **baseline `paper_claims.csv` `07f83156…`/132** (only X-29 changed `UNRESOLVED → REPRODUCED SIMULATION`)
× **ledger `840945ff…`/132** (ledger `.md` `c9bb8691…`, baseline JSON `77098a5d…` records `07f83156…`/132, proof-status
`7c0e753c…`); **18 declared + 114 explicit NOT-YET = 132**, mapping/declarations unchanged, X-29 remains explicit
NOT-YET (a baseline-status change is not a Lean declaration); 0 code `sorry`, in-Lean 18/18, proof-status 107/107,
axioms only `''`/`propext`. This was a **content/status-only** change with no id/row/mapping delta, so R1–R8 were
**re-affirmed, not re-run from scratch**; the prior `e0a5662`/`3ff88d39`/`55f75eea` and 130-row/`b990c99f` pins remain in
git history. **This certifies the claim→declaration mapping and axiom hygiene only — not the truth of empirical claims
and not engine numerics; the engine is NOT formally verified.** Repro:
`python3 docs/audit/lemma_audit.py --claims results/audit/paper_claims.csv --ledger docs/audit/LEMMA_LEDGER.csv --lean-dir
verification/lean`.

**Install provenance (honest):** elan 4.4.0 → Lean `v4.36.0` via the GitHub release mirror because the default CDN
measured **70 B/s**; 608.4 MiB download, **~23 min** install window, **3.0 GiB** unpacked, disk 12 → 8.9 GiB free;
**Mathlib not installed** (multi-GB, not viable on this Mac) — Tier 2 is CI-only.

**Significance for Paper D:** "the classical demand equation provably ignores school supply S / positional fixed seats /
withholding / time budgets / supply form" is now a **machine-checked invariance statement**, not rhetoric — strong
support for the omission lemma (M1–M5), alongside the counterexample lemmas (`fixed_seat_relative_rank_counterexample`,
`complementarity_counterexample`, `feedback_capacity_counterexample`, `max_not_additive`) that keep the formal claims
conditional rather than universal. It does **not** show the omissions are empirically important (that is the EP-1/EP-2
probe and external-data job) and it carries the Tier-3 disclaimer.

### Re-review — Paper C prereg **Amendment A1** (2026-11-25): **CONDITIONAL; 4 residual fixes**

Amended draft: `docs/audit/PAPER_C_CONFIRMATORY_PREREG.md` sha256
**`dd58919dc7941c05952c642df804431149258d0d5c5abd1c6868b4ea55b94666`** (commit `c0f4eb6`; §8 A1.1–A1.8). The
**8 original blocking items are substantively addressed in-file**: 36-cell ids/factor mapping + screening seeds 0–7;
one primary per test; T4 overclaim removed (T5 wave-2/not testable); disjoint confirmatory seeds 100–131 + pre-declared
pass rule + all-cell fallback; in-file four-criticism section; T1 relabelled school-quality-bundle; T2/T3 contrasts
with `own_share_financial` definition + absolute quantities; provenance/stop/exclusion/MDE/Holm/Caplan-V. **Residual
fixes are still required before preregistered-final:**

1. **Body vs §8 inconsistency.** §§1–6 still carry the pre-A1 wording (16 confirmatory seeds; T2 `own_share`; T3
   `h and own_share`; T4 "(positional) but not via learning"; §6 ≤4 CPU-h / 16 seeds). A preregistration must have
   **one canonical spec**: update §§1–6 or add an explicit "**§8 supersedes §§1–6 where inconsistent**" statement.
2. **T3 cell mapping is internally inconsistent.** §8 A1.1 defines supply **B = own_ban .95 / firm_ban 0** (own channel
   ~closed), but A1.7 calls B "own-open, pay-gap"; T3 "B vs A on `withheld`" would then test a cell with tiny h and
   `own_share≈0`, so the `h>0` / `own_share>0.1` assertions cannot pass. Re-map T3 to **A|P55 vs A|P12** (own-open
   pay-gap vs own-open no-gap) or correct the supply labels; verify the binding assertions in the chosen cells.
3. **Compute envelope inconsistent with the amended design.** A1.1 uses **32 confirmatory seeds**, but §6 still says
   **16 seeds / ≤4 CPU-h**; Pilot-0 measured ~5–7 min/seed at N=1500 ⇒ ~3.2 CPU-h **per cell**, so ≤4 CPU-h allows
   ~one cell, not multiple passers. Recompute and either raise the cap, reduce confirmatory seeds/cells, or pre-limit
   the passers; state the achieved MDE/power at 32 seeds. Update §6 with the actual projection.
4. **Gate kind / `contest_r` missing from the 36-cell mapping.** The grid is S×L×supply×settings; `contest_r ∈
   {1.2,1.6}` is "only where the gate is contest-based", but no gate-kind dimension or fixed-gate declaration is in
   the cell ids. State the fixed gate kind per cell (or add gate as a factor and change the grid size); the appendix
   must resolve this before launch.

**Recommended:** (5) add the explicit 36-row table or state "36 = the full Cartesian product; no other cells";
(6) label the design **"screening-confirmation on pre-declared passers"** — disjoint seeds remove MC reuse but the
target remains conditional on the screening selection; state the estimand and keep the all-cell fallback;
(7) pin runner + analysis commit/sha and engine/spec hashes in a **launch manifest** before the run, with per-run
`event_log`/`unfired_events` assertions. **EP-1/EP-2 probes are not runnable today** (EP-1 needs the wave-2 public-only
S lever; EP-2 needs the additive series); the clean public-S follow-up is therefore **not** part of Paper C now.

**Verdict: still CONDITIONAL — not cleared for preregistered-final.** No confirmatory compute until the four residual
fixes land, the body is canonical, and Codex's protocol/Kaplan confirmation arrives.

### Re-review — Paper C prereg **Amendment A2** (2026-11-25): **CONDITIONALLY CLEARED (2 textual pre-launch amendments)**

File: `docs/audit/PAPER_C_CONFIRMATORY_PREREG.md` sha256
**`04532581e768983734664c2dac94dc8af2cb834ea723882f483761c94b4a1647`** (commit `bb26d49`). **All four A1 residual
items are addressed in-file:** (1) authority rule at top (`§8 A1 supersedes §§1–6`; authoritative design = §8 +
Appendix); (2) explicit **36-row appendix** with ids, factors, seed mapping, **gate kind = contest**, `share_of='cohort'`,
**`contest_r` mapped by L** (r=1.2 at L=.25, r=1.6 at L=.45 — fixed by L, not an independent factor); (3) **T3 remapped
to A|P55 vs A|P12** at the same S,L (own access open both; exposed arm h≈.144/own_share≈.53 vs h=0; binding assertions
must hold or the contrast is INVALID); (4) **compute recalibrated from measured Pilot-0** (~6.9 CPU-min/run at N=1500;
N=600 ≈2.8 CPU-min/run → screening 288 runs ≈**13.4 CPU-h**; confirmatory ≤6 passers ×32 seeds ×N=1500 ≈**22 CPU-h**;
**≤36 CPU-h total**; "screening-confirmation on pre-declared passers"; **launch manifest** requires engine core, spec,
runner+analysis commit, seeds, cells, frozen passer list). **Pilot-0 record corrected to 128/16**, stale `dcd0ad9`
explicitly superseded (`PILOT0_RECORD.md` sha `601e13ce…`); capacity reserve recorded: **X-29 diagnostic at 6 workers**
(COMPUTE_SCHEDULE §13.28; ~45–50 min, not 35).

**Conditional clearance — 2 required textual pre-launch amendments (no design change):**
1. **Pre-declare the >6-passer selection rule.** Screening may pass more than 6 cells; state e.g. "all passers if ≤6;
   if >6, the first 6 in the fixed appendix cell order are confirmatory and the remaining passers are reported as
   screening-only" (or raise the cap). No post-hoc choice; the frozen passer list goes in the manifest.
2. **Resolve the all-cell fallback vs the ≤36 CPU-h envelope.** All-36 confirmatory at 32 seeds × N=1500 is ≈**132
   CPU-h**, far outside the cap. State that the fallback is a **separate re-approved run/new budget** (not part of
   ≤36 CPU-h) or drop it; otherwise the compute claim and the fallback are inconsistent.

**Recommended (wording):** (a) explicitly exempt the no-withholding control **A|P12** from the `h>0/own_share>0.1`
binding assertions (apply to the exposed/withholding arms only; failed exposed arm = INVALID); (b) state that **L is a
gate-pressure bundle** (share + contest_r fixed by L) and T4 cannot separate the two components; (c) screening is also
compute and starts only after clearance + Codex.

**Verdict: CONDITIONALLY CLEARED for preregistration-final.** Launch only after the two textual amendments and Codex's
protocol/Kaplan confirmation; the launch manifest must carry engine core `e111397b…`, spec `e5ddef6b…`, engine commit
`846c9e0`, runner+analysis commit hashes, screening seeds 0–7 / confirmatory seeds 100–131, the 36-cell list + frozen
passer list, N/T/T0/measure_from, fail routing, per-run `unfired_events==[]`, and the 1–2 slot capacity reserve.

### Re-review — Paper C prereg **Amendment A3** (2026-11-25): **CLEARED FOR PREREGISTRATION-FINAL**

File: `docs/audit/PAPER_C_CONFIRMATORY_PREREG.md` sha256
**`0089f2830781dd74696db75e863f40edca2d9559b9a81b6496f9d730785a044c`** (commit `a61ffa8`). The two required A2
pre-launch amendments and the recommended wording are in-file and **no design change** was made:

* **A3.1 — >6-passer rule:** if screening passes ≤6 cells, all run confirmatory; if >6, the **first 6 in fixed appendix
  row order** run confirmatory and **all remaining passers are screening-only**; the **frozen passer list goes into the
  launch manifest before any confirmatory run**; no cap raising without a separately approved budget. No post-hoc
  choice.
* **A3.2 — all-cell fallback removed:** all-36 confirmatory at 32 seeds × N=1500 (≈**132 CPU-h**) is **explicitly not
  part of the ≤36 CPU-h envelope**; if ever run it is a separate, re-approved run/new budget.
* **A3.3 — assertions/bundle:** **`A|P12` is exempt** from `h>0`/`own_share>0.1` (no-withholding control); assertions
  apply to exposed arms only; a failed exposed arm is **INVALID** and reported, never dropped; **L is a gate-pressure
  bundle** (contest `share` + `contest_r` fixed jointly by L), so T4 makes **no component-separation claim**.
* **A3.4 — screening timing:** screening is compute and starts only after (i) this prereg is marked final, (ii) Codex's
  protocol/Kaplan confirmation is in, (iii) the 1–2 slot Luna/MASSENG reserve is honoured.
* **Manifest requirements** listed: engine `846c9e0`, core `e111397b…8e71`, spec `e5ddef6b…`, runner+analysis
  commit+sha, seeds 0–7 exploratory / 100–131 confirmatory, 36 cells + frozen passer list, N/T/T0/measure_from, fail
  routing, per-run `unfired_events==[]`, workers (≤8, reserve), wall/CPU, output hashes.

**Housekeeping flag (textual, non-blocking for design):** the top authority rule still says only "§8 A1 supersedes
§§1–6", while **A1.4 (line 114) still mentions the now-removed all-cell fallback**. For a single canonical spec, the
top rule should read "**§9 A3 supersedes §8 A1 where inconsistent**" (or A1.4 should be struck), and the status line
should change from DRAFT to FINAL when signed. This is a one-line edit, not a design change.

**Verdict: CLEARED FOR PREREGISTRATION-FINAL** — A3 satisfies the A2 conditional-clearance requirements. **Final
designation and any compute remain gated on:** (i) the authority/status housekeeping edit, (ii) **explicit Codex
protocol/Kaplan confirmation recorded in the launch trail**, (iii) the launch manifest and 1–2 slot capacity reserve.
Screening is compute and must not start before all three.

**FINAL FREEZE VERIFIED — PREREGISTRATION FINAL (design frozen 2026-11-25) + LAUNCH MANIFEST FROZEN.** Final
prereg: `docs/audit/PAPER_C_CONFIRMATORY_PREREG.md` sha256
**`445ec423c03ffdc8521a820694a72662cabbe342331dc1c8a839023e00053a8d`** (commit `e34b901`): line 7 now reads
**"PREREGISTRATION FINAL (design frozen 2026-11-25; no compute yet)"**; §8 historical-status line corrected (A1
superseded by A3; overall status FINAL); authority rule, A1.4 struck fallback, and §10 Codex trail unchanged.
Frozen manifest: `docs/audit/PAPER_C_LAUNCH_MANIFEST.json` sha256
**`6400c9db99b567faa01d9c1e62df552280170b00c062762250302daa0bb2f01a`** (commit `62dc609`), status **FROZEN (reconciled)**, carrying
engine `846c9e0`/core `e111397b…`, spec `e5ddef6b…`, runner file+sha (`fbeba460…` with the pre-launch extension note),
36 cells, screening seeds 0–7 / confirmatory 100–131, N=600/1500, T=46, measure_from=18, T0 n/a, fail routing (G6→G9
contest, `share_of='cohort'`, `contest_r` fixed by L), per-run `unfired_events==[]` + exposed-arm assertions (`A|P12`
exempt; failed exposed = INVALID), >6-passer rule (first 6 in appendix order), ≤36 CPU-h envelope (13.4 screening +
22 confirmatory), 1–2 slot Luna/MASSENG reserve (X-29 at 6 workers), and the no-compute gates.

**Provenance reconciliation — DONE (2026-11-25).** The frozen manifest now cites the **final canonical prereg
`445ec423…`** (commit `e34b901`); `prereg.sha256_at_freeze_time = ff61f1e6…` and `prereg.superseded_by` record that
the only difference is the §8 historical-status sentence (no design change). Manifest sha
**`6400c9db…`** (commit `62dc609`), status **FROZEN (reconciled)**; engine pins, 36 cells, seeds 0–7/100–131,
N=600/1500, T=46/measure_from=18, fail routing, assertions (`A|P12` exempt; failed exposed INVALID), >6-passer rule,
≤36 CPU-h envelope, 1–2 slot reserve (X-29 at 6 workers), and Codex trail are unchanged. **No screening/confirmatory
compute until the 1–2 slot reserve is in place** (the hash citation and Codex trail are now satisfied).
Adjudication status: **PREREGISTRATION FINAL (design frozen); MANIFEST FROZEN (reconciled); launch gated only on the 1–2 slot reserve.**

## 4N. GPU Plackett–Luce port — **methods artefact (X-31); no GPU numbers claimed; box parity pending**

Branch **`research/gpu-pl-port-auditv2-2026-11-25`** (tip `2399aa1`); engine port commit
**`59fd2497765f15c108de3ec182d1febbe3d28c8a`** (later branch commits are documentation-only). Host port complete; **Mac
checks pass; box parity pending (Commander)**. No box job started from this lane.

| file | post-port sha256 | change |
|---|---|---|
| `engine/eduengine/contest_gpu.py` | **`ab08a53b…596f`** | new, byte-identical to the validated GPU backend |
| `engine/eduengine/contest_math.py` | **`5fceb4d5…e944`** | +169 L GPU section/batch API; canonical task-12 caches and `pl_realize` untouched |
| `engine/eduengine/__init__.py` | **`2c082d5c…348f`** | +11-line optional registration (`ATLAS_PL_BACKEND=gpu`) |
| `engine/eduengine/core.py` | **`5bcbc0b3…9f75`** | exactly two hunks (import + `_pl_probs` one-row batch); `_validate_events`/`EVENT_CACHED_PARAMS` intact |
| `engine/eduengine/modules/tutoring.py` | **`b3d32cee…3fdf`** | 9-point batched prep grid + helper |
| `docs/gpu/port_verify.py` | **`6ba6013c…4026`** | harness |
| `docs/gpu/PORT_REPORT.md` | **`23b7a8c1…5650`** | report (`59fd249` pinned as engine port commit) |

**Mac evidence (flag unset / CPU path):** 68/68 tests; **130-fixture digest identical**; CPU batch ≡ per-row **0.0**;
full-run HK Baseline seed 0 digests identical; RNG-realise digests identical (no RNG consumed by probability calls); 23
boundary cases OK; default import **torch-free** with graceful CPU fallback (`pl_backend()=='cpu'`; forcing GPU without
torch raises the documented `RuntimeError`). Diff is additive: 4 files +222/−10 + new `contest_gpu.py` (10,469 B).

**BINDING BOUNDARIES (recorded):**
* The branch's **core hash `5bcbc0b3…` is NOT the canonical pin `e111397b…`**, so **GPU runs are gate-grid/sensitivity
  only**; they **must not replace CPU primary artifacts**, the canonical spec hash, or any Gate-1 evidence; **no
  retroactive substitution** of CPU results.
* **Cross-replica batching is staged, not implemented**; no multi-GPU claims.
* **No GPU numbers are claimed in this adjudication**; none may be cited until the parity gate clears.

**Pending parity gate (before any GPU use):** box parity — fixtures, discrete-winner comparison, and full-wall
benchmark — run by the Commander; QA to add `tests/test_contest_math_gpu.py` and sign off **only on ≤1e-7 agreement with
flips quantified**. Until then: **no GPU runs; no substitution; no performance claims.**

**QA tests (conditional):** branch commit `6c68d96`; `tests/test_contest_math_gpu.py` sha
**`9ee72f9e…8729`** (8 tests), `GPU_TESTS_QA.md` sha **`7ab291f0…f950`**, `docs/gpu/results/gpu_parity_qa.json` sha
**`3df35bd7…81cc`**. **Mac 5 passed/3 skipped; CUDA box (torch 2.7.1+cu118, RTX 3080 Ti) 8/8 passed in 57.29 s;
independent `port_verify.py gpu-parity`: max|dP| 4.83e-8, 0/130 >1e-7, 0 seat-sum violations, 0 fixture winner
flips**; engine file hashes match the port. **Harness provenance defects (not engine failures; Commander fixing and
re-emitting):** `env.backend='cpu'` recorded because the backend is reset at `port_verify.py:236` before the manifest
write at `:239`; `engine_commit` empty at `:113`; `spec_sha256` missing. **Remaining GPU gate:** Commander's cell-level
parity (2 Pilot-0 cells × seeds 100–101; per-gate-year Jaccard/sym-diff/flipped seats) + **full-wall benchmark**; sign
off only if ≤1e-7 and no unresolved flip changes a headline outcome, otherwise CPU fallback.

**Gate-status check (2026-11-25):** QA searched the Mac and box work dirs (`/root/work/gpuport*`, `gpu_qa`, `gpu`,
`gpu2`) — the **Commander's cell-level pair-cells artefacts and full-wall benchmark are NOT present yet**; only the
fixture-level parity (`gpu_parity_qa.json`: max|dP| 4.83e-8, 0/130 >1e-7, 0 flips) exists. QA added a ready checker
`docs/gpu/qa_parity_review.py` (commit `ee7e3ef`; sha **`02afa739…f0fa`**) implementing the gate: **P1 ≤1e-7; P2
Jaccard/sym-diff/flips reported, not failed; P3 any unresolved headline-outcome flip → CPU fallback; P4 full-wall
benchmark; P5 provenance (engine commit/core hash equal on both sides)**. When the Commander uploads the pair-cell and
benchmark paths/hashes, QA returns PASS/FAIL + benchmark comparison. **No GPU numbers are claimed in the meantime.**

**Status: METHODS ARTEFACT (X-31) — CONDITIONAL; no GPU numbers claimed. Parity gate OPEN: fixture parity exists, but
cell-level + full-wall benchmark artefacts are missing; QA checker ready.**

## 4O. Paper C Pilot-0 payload — **EXPLORATORY / PENDING QA (X-Pilot); not a result**

Payload: `/root/work/paperC/results/paperC_pilot0_results.json`, **69,286 B**, sha256
**`c6e50bc1e86f8d41a8d8a332e860898445de4ce90f8f9ec7d004e438fa523f9d`**; **128/128 rows**, 16 cells (4 regimes ×
q0 {1.0, 1.2} × p_firm {.03, .08}) × 8 seeds (0–7); wall **6860.01 s ≈ 1 h 54 min** at 8 workers, all cells exited
cleanly; 16 `ckpt_*.jsonl` + `MANIFEST_SHA256SUMS.txt`. Copied to `~/neon-boot/qa/incoming/paperC_results/` (payload +
16 ckpts + MANIFEST; `sha256sum -c` all OK; bundle `paperC_results_bundle.tar.gz` sha `ec868a57…a4fb0b`); qa-verifier
notified. Manifest: engine `846c9e0`, core `e111397b…`, spec `e5ddef6b…`, runner `bc833b76…`, status
**EXPLORATORY**, `withholding_note`/`contamination_note` recorded.

**QA: PASS A1–A10** — `docs/audit/PILOT0_QA.md` sha256
**`620375a6361380176f430130e2be1013bf28db0fad39073ca9f284b2d07d676a`** (commit `0f1013e`; CPU-only campaign):
payload `c6e50bc1…`; design/params 128/16, 8 seeds/cell; runtime pin `846c9e0`/core `e111397b…` + spec
`e5ddef6b…` (re-pin `46c080d` provenance) verified against git; **no-op guard 12/12 non-market cells**; A10 ckpt→summary
reproduction all 16 cells; manifest **17/17** hashes OK; A9 log clean (short/minimal). **Caveats:** `completion_primary`
and `completion_upper` are **all-NaN in every cell/seed — do not cite** (reporting-field artefact, not run failure);
`tut_*_by_grade_last` clean; own_share/tut_firm contamination note stands; **exploratory only, no causal/multiplicity/
welfare claims**; CPU-only on the canonical pin (GPU is a separate artefact).

**Status: EXPLORATORY-VALIDATED (QA PASS A1–A10), not a confirmatory result; no Paper C claim moved.** No Paper C
claims until **X-29 closes**; CSV remains frozen.

**X-29 diagnostic — COMPLETE/RESOLVED:** `results/audit/newgen/gate_architecture_diagnostic.json` sha256
`57889777…8652`; 1,280 runs, 40/40 cells with non-NaN admission diagnostics (admit_rate range 0.2500–0.7067);
DIAGNOSTIC-ONLY, separate `results_diag/`, no effect on X-27; aggregation-only recovery (no simulation rerun).
**Bundle reconciliation:** canonical QA bundle `~/neon-boot/qa/incoming/paperC_results_bundle.tar.gz` sha
`ec868a57…a4fb0b` (33,095 B); the Commander's `/tmp/paperC_results.tar.gz` (`14567f66…ac06`) is an informal
re-compression of the identical directory (same payload/ckpts/MANIFEST; gzip timestamp/ordering only) — **not a second
bundle, no file changes**.

## 4P. Paper C screening — **QA PASS S1–S11 (integrity only; SCREENING-ONLY; no claims moved)**

Artefacts: `docs/audit/SCREENING_QA.md` sha256
**`25cc49092dd78747720444434f931129e4d65fa7b8a28ca54b3e7fd11fd063f6`** (commit `f065458`), machine
`docs/audit/results/screening_qa.json` sha256 `f720e584…`; payload `paperC_screening.json` sha256
**`6bcc29a50d41dc2c63a5959c0b023eb203c5bf1bd0cd04ffaee908a5ebb5b6d4`** (1,337,854 B; duplicate `_results`
byte-identical). **288 runs = 36 appendix-order cells × 8 seeds (0–7)**; `invalid_cells=[]`; wall 1879.17 s.

**Verified (S1–S11 all PASS):** 40/40 SHA256SUMS + checkpoint map 36/36; pins engine `846c9e0`/core
`e111397b…`/spec `e5ddef6b…`/runner `d2d25c1c…` (matches repo file)/prereg `445ec423…` = launch-manifest prereg;
36-cell grid exactly in fixed appendix order; 288 unique rows with N=600/T=46/measure_from=18; per-row
supply/settings/q0/gate (G6→G9 contest, share_of cohort, r by L), `unfired_events==[]`; exposed-arm assertions
correct; summary 36×18 with n=8; ckpt→summary exact (1e-12); no `completion_*` NaNs; `SCREENING-ONLY` label + queue
`STATUS=OK` + `RESULTS_DONE`.

**Defects/notes (recorded):**
* **D-S1 (low; fix before confirmatory):** runner row metadata flags **A|P12 as exposed** (96 row flags; rule text says
  only "B exempt"; `run_paperC_screening.py:207`), while the **actual binding check** (`:154`) correctly applies only to
  `A/C AND P55`; A|P12 (h=0) was not asserted, `invalid_cells=[]`, S7 passes. **No effect on screening results**, but
  the metadata contradicts prereg A3.3 — fix flag/rule text before any confirmatory bundle.
* **D-S0 (info):** launch manifest records pre-launch runner `fbeba460…` while executed runner is `d2d25c1c…`
  (documented extension; actual file matches run manifest) — reconciled.
* **D-S2 (info):** row `params.contest_r` is static 1.5 while the gate override sets `gate.r` by L (1.2/1.6); the
  engine uses the gate override, which is authoritative — harmless but potentially confusing downstream.

**Caveats / pre-confirmatory conditions:** **SCREENING-ONLY** — no Paper C claims/numbers are interpreted or moved;
**P12=pay_gap requires the A4/prereg clarification** before confirmatory use; the >6-passer rule/frozen passer list is
downstream; confirmatory remains gated on the D-S1 metadata fix + A4 clarification + frozen passer list + the 1–2 slot
reserve. **Status: screening QUEUE/ARTEFACT integrity PASS; not a confirmatory result; CSV frozen.**

## 4Q. Screening→passer freeze — **BLOCKED pending rule amendment (A4); computed tests below**

Computed by the adjudicator from the QA-verified screening payload (`6bcc29a5…`; per-seed rows, 8 seeds/cell, paired).
**A4 recorded (formal clarification, no design change):** **`P12 = pay_gap` is the no-withholding control**; **exposed
arms = A/C ∧ P55**; **`A|P12` is exempt** from `h>0`/`own_share>0.1`; failed exposed arm = INVALID. This matches A3.3
and the actual screening assertion (`run_paperC_screening.py:154`), despite the D-S1 metadata defect.

**Test-level screening results (lead-specified tests):**
* **T1 (participation, S=.85 − S=1.15, min −3 pp):** 12/12 contrasts **do not reach** the minimum; observed means
  **+0.32 … +1.08 pp** and every 95 % CI upper bound is **< 3 pp**. This is **indeterminate/underpowered at N=600 × 8
  seeds**, not a clean failure (direction is positive, magnitude below the pre-declared MDE).
* **T2 (own_share C−A, min +0.10):** **12/12 pass** (0.359 … 0.709).
* **T3 (binding, A|P55):** **6/6 pass** (`h=0.144`; own_share 0.429 … 0.524 > 0.1); `A|P12` exempt (A4).
* **T4 (L=.45 − .25):** primary **Q5−Q1 spend gap** positive **18/18** (+0.011 … +0.023 in spend units; the pre-declared
  "+2 pp" threshold is in pp and does not map directly to this spend-gap scale — **units/threshold need confirmation**);
  secondary **Q5−Q1 participation gap negative 18/18** (−0.66 … −5.07 pp), **opposite** to the predicted L↑ gap↑. So T4
  primary direction is positive but threshold/scale is ambiguous, and the secondary contradicts the predicted sign.

**Blocking rule problems (why I cannot freeze a passer list yet):**
1. **"Cells" vs "tests" is undefined.** If a cell must pass **all** T1–T4, there are **zero passers** (T1). If a cell
   passes when implicated by **any** passing test, nearly all 36 cells pass via T2/T3/T4.
2. **The >6 → first-6 appendix-order rule is structurally incoherent with T1/T4.** The first six cells are all
   **S=.85, L=.25** (A/B/C × P55/P12): they contain **no S contrast** (only S=.85) and **no L contrast** (only L=.25),
   so a confirmatory block of those six **cannot test T1 or T4**. The cap rule and the test design conflict.
3. **T4 threshold/units** need a pre-declared scale (+2 pp vs spend units) and a decision on the contradicting
   participation-gap secondary.

**Proposed amendment A4 (for Lead decision; no compute until accepted):** define passers as **complete contrast blocks**
(not first-N raw cells) and pre-declare a **6-cell contrast-complete anchor block** covering T1–T4 at one coherent anchor:
`S0.85|L0.25|A|P55`, `S1.00|L0.25|A|P55`, `S1.15|L0.25|A|P55` (T1 S contrast), `S1.00|L0.25|C|P55` (T2 C−A),
`S1.00|L0.25|A|P12` (T3 A|P55 vs P12), `S1.00|L0.45|A|P55` (T4 L contrast). Six cells ≈ the same 22 CPU-h envelope.
T1 is screening-indeterminate; confirmatory can still test it as pre-registered, with T1 reported as underpowered at
screening (not silently promoted). Alternative: raise the cap to cover a contrast-complete set / restrict confirmatory
to T2/T3/T4. **No confirmatory compute until the Lead chooses and the frozen list is signed and put in the manifest.**

**PASSER FREEZE SIGNED (2026-11-26) — conditional on manifest/runner provenance.** Verified
`docs/audit/PAPER_C_PASSERS.json` sha256 **`b64a69f0391d0089b535b6e43cfd2a55680f6c812159c3f0e37efc6ba95b99e7`**
(source screening `6bcc29a5…`; 288 runs/36 cells; `invalid_cells=[]`) and `PAPER_C_A4_P12_CLARIFICATION.md` sha
`8c967eab…`. Rules: α=.05, **Holm across T1–T4**, 8 matched seeds, pre-declared min effects, >6 → first 6 in appendix
order. Test outcomes: **T1 +0.655 pp (se .021) vs min 3.0 → FAILS**; **T2 +0.540 (se .0003) vs min .10 → PASSES**;
**T3 +0.144 (se 0) vs min .05 with assertion-support h(A|P55)=.144/h(A|P12)=0 → PASSES**; **T4 +1.7668 pp (se .024) vs
min 2.0 → FAILS** (95 % CI ≈[1.72, 1.81], entirely below 2; no threshold change). **24 candidates (A/C cells from T2/T3)
→ 6 frozen passers in appendix order:** `S0.85|L0.25|A|P55`, `S0.85|L0.25|C|P55`, `S0.85|L0.25|A|P12`,
`S0.85|L0.25|C|P12`, `S0.85|L0.45|A|P55`, `S0.85|L0.45|C|P55`; remainder screening-only.

**Signed meaning:** T2/T3 are the only confirmatory tests; **T1 and T4 are screening failures to be reported, not
confirmatory tests** (no post-hoc threshold change, no promotion). The six passers are all **S=.85**; T2 is testable at
L=.25 P55/P12 and L=.45 P55, T3 at L=.25/.45 — **no S-generalisation** beyond .85. **Conditions before any confirmatory
compute:** (i) the confirmatory manifest must cite A4 `8c967eab…` + passers `b64a69f0…` + a **committed** runner sha
(HEAD `48ec3485…`) and its commit; the worktree currently has **uncommitted** screening-runner edits (`ddeffe42…`) and an
**untracked** `run_paperC_confirmatory.py` (`fcf86c8b…`) — commit/pin before use, no uncommitted runner; (ii) pre-declare
the confirmatory **Holm family explicitly** (T2/T3 only, or T1–T4 with T1/T4 marked screening-fail/not-run); (iii) N=1500,
seeds 100–131, 6 cells, ≤22 CPU-h, 1–2 slot reserve; no compute until the manifest is frozen and the Lead allocates the
box. **Status: PASSER FREEZE SIGNED (conditional); no confirmatory compute launched.**

## 4R. Paper C confirmatory — **PRE-LAUNCH RECORD: CLEARED (pending Lead allocation + reserve)**

Manifest: `docs/audit/PAPER_C_CONFIRMATORY_MANIFEST.json` sha256
**`f34751d861bfe863e1db530502171e11824780d8b68307c62796a9a58626ee14`** (commit `4a4a8fa`), status
`FROZEN_PENDING_ADJUDICATOR_PRELAUNCH_RECORD`. **All three prior conditions are met:**
1. **Citations/hashes verified:** prereg FINAL `445ec423…` (`e34b901`); **A4** `8c967eab…`; **passer freeze**
   `b64a69f0…` (signed `bbc0b92`); screening source `6bcc29a5…` (288/36, `invalid_cells=[]`); **committed runner**
   `run_paperC_screening.py` sha **`ddeffe42…` @ commit `1b3a510`** (HEAD; no uncommitted runner; the untracked
   `run_paperC_confirmatory.py` `fcf86c8b…` is explicitly **NON-AUTHORITATIVE — do not use**). Code enforcement verified:
   `PAPER_C_STAGE=confirmatory` requires seeds **100–131**, requires `--cells` + `--allow-subset`, and screening mode
   refuses seeds 100–131.
2. **Holm family pre-declared:** **T2/T3 only (m=2, α=.05)**; **T1/T4 are screening failures** (T1 +0.655 pp vs ≥3.0;
   T4 +1.767 pp vs ≥2.0, CI below 2) and are **not tested confirmatorily**; **no threshold change**. T2 estimand =
   `own_share_financial_proxy` (C−A), min 0.10, paired by seed; T3 = `withheld` (A|P55−A|P12), min 0.05 with
   h(A|P55)≥0.05 and h(A|P12)≤0.01; seed-MC uncertainty (32 matched seeds), parameter uncertainty zero.
3. **Design/gates:** 6 frozen passers (all **S=0.85** — **no S-generalisation claim**), seeds 100–131, N=1500/T=46,
   ≤**22 CPU-h** upper estimate, 8 workers, **1–2 slot Luna/MASSENG reserve**; gates = this pre-launch record + Lead box
   allocation + reserve confirmed; no confirmatory compute launched.

**Caveats recorded for the confirmatory write-up:** T2 is **proxy-based** (`own_share_financial_proxy`; contest-prep
mixing; no clean own-vs-firm spend split) — T2 claims must carry that caveat; T2 is tested only at L=.25 (P55/P12) and
L=.45 (P55), not the full 2×2; T3 is the assertion-support test; **T1/T4 screening failures are reportable results, not
confirmatory findings**; no S-generalisation beyond .85.

**LAUNCH OBSERVED (2026-11-26 ~07:20 CST) — manifest flipped FROZEN_APPROVED.** Manifest sha
**`bf7b7842e418d5b9e272a866ec0d7d798f824d79c1671829c63ac834cb042499`** (commit `5f0bfbc`), status
`FROZEN_APPROVED`, citing adjudication `9506640` and the observed box allocation. Launch: driver PID **1364**,
`PAPER_C_STAGE=confirmatory`, `PAPER_C_P12_MODE=pay_gap`, seeds **100–131**, N=1500/T=46, the 6 frozen `--cells`,
`--allow-subset`, `--analysis-commit 8121bf6`, out-dir `/root/work/paperC/confirm_final`; box runner sha
`ddeffe42…` **= committed `1b3a510`** (enforcement verified); engine pins `846c9e0`/core `e111397b…`/spec
`e5ddef6b…`; screening artefact on disk unchanged (`6bcc29a5…`). **Capacity deviation recorded:** `--workers 10` vs
manifest's 8 and the 1–2 slot Luna/MASSENG reserve **not explicitly enforced**; only 6 cells exist, so instantaneous
load is 6 processes (4 configured workers idle; no external job affected at launch). This is a **capacity/protocol
deviation, not an estimand change** — record actual CPU/wall on completion. ETA 1.5–2 h; on completion the Commander
will pull/hash-verify, copy to `~/neon-boot/qa/incoming/paperC_confirmatory/`, and send the confirmatory JSON +
T2/T3 Holm results for adjudication **before any claim**. **No confirmatory number is cited yet.**

**RESOURCE-RUNWAY WARNING (2026-11-26 ~07:33 CST; no outcome numbers cited).** Measured in `confirm_final`
(PID 1364): 6 cells at ~99.9 % CPU; after ~13 min, 4 cells completed 1 seed each and the L=.45 cells were still on seed
0 ⇒ **per-seed wall ≈13–15 min, ~800–900 CPU-s/run** at N=1500 with the treated G6→G9 contest gate. Projection:
**192 runs ≈ 42–48 CPU-h vs the pre-declared ≤22 CPU-h envelope**; wall ≈7–8 h at 6 parallel cells. The
profile-based 170 s/run estimate was a different gate configuration (seat share .25/.45 makes the PL quadrature ~O(N²)).
**No confirmatory number has been inspected or cited.**

**Adjudication position:** **prefer option (a) — complete the full pre-registered 32-seed run and record the
compute-envelope overrun as a protocol/resource deviation**, not a design or estimand change: 6 frozen passers, seeds
100–131, N=1500/T=46, T2/T3 Holm m=2 α=.05, min effects and proxy/range caveats unchanged. The envelope was a
pre-launch **estimate**, not a scientific threshold; preserving the pre-registered precision is the scientifically clean
choice. If box allocation genuinely cannot support ~42–48 CPU-h / 7–8 h, **fallback (b) A5 interim at 16 seeds/cell** is
acceptable only under strict conditions: **freeze A5 before any outcome inspection**; fixed seeds **100–115** (no
outcome-based choice); estimands/min effects/Holm family unchanged; **no optional stopping/peeking** (run exactly 16
seeds/cell or complete all 32); report achieved SE/CI and label **interim precision** (SE ≈ √2 × the 32-seed target), no
claim of full preregistered precision; T2/T3 proxy/range caveats unchanged. **Option (c) N=600 is rejected** — it
changes the design/power and is the largest deviation. The run should not be killed without Lead instruction; the
overrun is **resource, not design.**

**A5 APPROVED (2026-11-26) — pre-declared 16-seed truncation, estimand untouched (resource-driven precision
amendment).** Confirmatory uses **16 matched seeds, 100–115** (instead of 32), pre-declared and matched across the 6
frozen passers; seeds **116–131 are not run/are excluded**. Everything else unchanged: 6 passers `b64a69f0…`;
N=1500/T=46; engine `846c9e0`/core `e111397b…`/spec `e5ddef6b…`; committed runner `ddeffe42…`@`1b3a510`; P12=pay_gap/A4
`8c967eab…`; **Holm m=2 α=.05, T2/T3 only**; T1/T4 remain screening failures; min effects unchanged. New envelope
**≤24 CPU-h** (96 runs ≈21–24 CPU-h; wall ~3.5–4 h). **Consequence: precision halves (SE ×√2); achieved CI/MDE and
the interim-precision label must be reported; no claim of full 32-seed precision.**

**Approval conditions (binding):**
1. **No outcome inspection before A5 freeze:** only per-seed timings/row counts were used (Lead attests); no per-cell
   effect/mean has been inspected or used to choose the truncation. If any outcome was inspected, A5 is invalid — revert
   to the full 32-seed run (option a) or label exploratory.
2. **A5 must be recorded before aggregation:** a timestamped A5 record (file or manifest field) with this 16-seed
   truncation, fixed seeds 100–115, and the unchanged estimands must be committed/cited **before** the 16-seed bundle is
   aggregated/analysed; the confirmatory manifest must cite A5.
3. **No optional stopping/peeking:** run exactly seeds 100–115 per cell; do not add seeds or stop based on effects;
   cells that complete >16 seeds must have 116–131 excluded from the A5 analysis.
4. **Analysis/reporting:** T2 (`own_share_financial_proxy` C−A, min .10; proxy/range caveats) and T3 (`withheld`
   A|P55−A|P12, min .05; assertion support) with Holm m=2 α=.05; seed-MC only; parameter uncertainty zero; report
   achieved CI/MDE and label **A5 interim precision**; decision holds/fails/indeterminate; T1/T4 screening failures
   reported, not confirmatory; no S-generalisation beyond .85.

**A5 EXECUTION RECORD — ACCEPTED CONDITIONALLY (aggregation hold).** A5 rule committed **before aggregation** at
`aa1d0bd`: `PAPER_C_A5_SEED_TRUNCATION.md` sha **`36515596…bf99`** (the version cited by the manifest); the later
execution-record update (`ecb02ad`) has file sha **`7512c7f5…fac8`** but `git diff aa1d0bd..ecb02ad` shows **only the
Execution-record section appended — the A5 rule text is unchanged**. Manifest `PAPER_C_CONFIRMATORY_MANIFEST.json` sha
`c8649511…` status `FROZEN_APPROVED_A5`, `amendment_A5` cites `1c51f17` + `36515596…`; 16-seed design (100–115);
stop-at-16 watchdog `ac979c9a…`; 16-seed aggregator `223628668…`; measured ~13.5 min/seed, ~809 CPU-s/run; A5 ETA
~10:55–11:15 CST. **Attestation recorded:** before freeze only process CPU/wall times and checkpoint row counts were
observed; **no per-cell outcome values were read**; no effect-based stopping/peeking. **8-seed insurance snapshot is
non-inferential** (crash insurance only; must not be analysed or used for stopping/inference).

**Aggregation hold — two provenance items must be fixed before the 16-seed bundle is aggregated/analysed:**
1. **Aggregator is untracked.** `papers/shadow-education-contest/code/paperC_confirm_aggregate.py` sha
   `223628668…` is currently `??` (untracked). It must be **committed** (and the commit recorded in A5/manifest) before
   it runs; otherwise the 96-run artefact would be produced by uncommitted code. (The untracked
   `run_paperC_confirmatory.py` remains NON-AUTHORITATIVE.)
2. **Manifest still says "32 matched seeds."** `confirmatory_statistics.uncertainty` must be corrected to **16 matched
   seeds (A5, 100–115)** and the A5 citation/approval linked; `compute.wall_note` still says "≤22/8" while
   `observed_runaway` records the truncation — correct the stats/uncertainty fields before aggregation. The A5 rule
   itself is valid; this is a manifest-consistency fix.

**A5 EXECUTION ACCEPTED — HOLDS LIFTED; AGGREGATION AUTHORIZED (2026-11-26).** Both provenance fixes are in:
1. **Aggregator committed** at **`0324205`**, sha **`223628668…978`**: reads per-cell checkpoints, filters **seeds
   100–115 only**, writes `paperC_confirmatory.json` (`n_runs=96`, `n_cells=6`, `invalid_cells=[]`) with A5/A4/passers/
   runner citations + `SHA256SUMS`/`CONFIRM_RESULTS_DONE`; no outcome-based selection; the watchdog runs this exact sha.
2. **Manifest corrected** — final sha **`0b70c105…3c01`** (commit `f15f559`; the commander's interim `3d3da8d7…` is
   superseded): `uncertainty` = **16 matched seeds (A5, 100–115), SE = √2 × the 32-seed plan, label A5 interim
   precision, NO full-precision claim**; `n_seeds_used=16`; A5 citation/approval (`1c51f17`, record `aa1d0bd`) linked;
   aggregator commit cited; `wall_note` reconciled (**16-seed ≈21.6 CPU-h / ~3.6 h** vs 32-seed 43.2 CPU-h / 7.2 h);
   `observed_runaway` retained. A5 rule remains the committed `36515596…` version (`aa1d0bd`; execution update
   `7512c7f5…`/`ecb02ad` appended only). **8-seed snapshot is non-inferential** (crash insurance only; not analysed, not
   a stopping source). Attestation (no per-cell outcome values read before freeze) recorded.

**CLEAN A5 RUN PLAN — CONFIRMED (with two execution-provenance reconciliations).** Lead killed the overrun run at
07:33 and relaunched a **clean A5 run** (`confirm_a5`, started 07:34, PID **2273**, `--workers 6`, `--seeds 100–115`,
6 frozen passers, N=1500/T=46, out-dir `/root/work/paperC/confirm_a5`) using the **committed runner
`ddeffe42…`@`1b3a510`**; the **driver itself aggregates** with committed code; `stop16.sh`/`snap8.sh` are stood down and
the untracked/committed external aggregator is not the production path; the old overrun `confirm_final` is killed and
must not be used. Duplicate A5 `PAPER_C_A5_16SEED_TRUNCATION.*` (sha `94d1d5be…`/`e6253c6d…`, commit `b825796`) is
**SUPERSEDED**; canonical A5 = `aa1d0bd` rule sha `36515596…` (current doc `f1916573…` = rule + execution/provenance
appendices only; `git diff aa1d0bd HEAD` verified no rule changes; manifest `0b70c105…` cites the canonical rule and
corrected uncertainty/A5/wall).

**Two reconciliation items remain (do not block the run; must be in the final artefact/manifest before analysis):**
1. **Manifest `launch_observed` still records the old overrun run** (`confirm_final`, PID 1364, workers 10,
   `--analysis-commit 8121bf6`). It must be updated to the clean `confirm_a5` run (PID 2273, workers 6, seeds 100–115,
   clean out-dir) and mark the old run **killed/abandoned, no outcomes used**.
2. **Clean run cites `--analysis-commit b825796`** — the **superseded duplicate A5** commit. The final artefact/manifest
   must cite the canonical A5 (`aa1d0bd`/`36515596…`, adjudication `1c51f17`) and record a provenance note mapping
   `b825796` → canonical A5 (same rule, duplicate superseded); `b825796` must not be presented as authoritative.

**A5 EXECUTION RECONCILED — both provenance items satisfied (2026-11-26).** Manifest `PAPER_C_CONFIRMATORY_MANIFEST.json`
sha **`8d0edbe7c3418e69215db1ed26b10746e5a7a116e6ea00562dd904ec25a18244`** (commit `217aa31`, status
`FROZEN_APPROVED_A5`):
1. **Clean run recorded:** `confirm_a5`, PID **2273**, **6 workers**, seeds **100–115**, N=1500/T=46, started 07:34 CST,
   runner `ddeffe42…`@`1b3a510`, driver self-aggregates; **old `confirm_final` (PID 1364, workers 10, analysis-commit
   `8121bf6`) marked KILLED/ABANDONED — no outcomes used, no aggregation**; stop16/snap8 watchdogs stopped; committed
   aggregator `0324205` retained but **NOT used**.
2. **Provenance mapping recorded:** clean run's `--analysis-commit b825796` is the **superseded duplicate A5**; canonical
   A5 = `aa1d0bd`/`36515596…` (approved `1c51f17`) is authoritative; final artefact must cite canonical A5 and `b825796`
   must not be presented as authoritative.
   `uncertainty` = 16 matched seeds (A5, SE×√2, no full-precision); `wall_note` reconciled; 6 workers on a 10-CPU quota
   (4 CPUs idle; Luna reserve per Lead). **Box verified:** `confirm_final` has no `paperC_confirmatory.json`/
   `CONFIRM_RESULTS_DONE`; `confirm_a5` driver PID 2273 running; no watchdog/aggregator processes remain.

**Status: both reconciliations satisfied; A5 execution accepted; clean run continues (ETA ~10:55–11:15 CST). No
confirmatory number cited. On completion: pull/hash-verify → T2/T3 Holm (m=2, α=.05) + achieved CI/MDE under A5 interim
precision; independent second hash-check accepted (send path/sha).**

**Status: clean A5 run CONFIRMED; aggregation path satisfies the holds; two provenance reconciliations required before
analysis/report; no confirmatory number cited yet.**

**Status: aggregation AUTHORIZED on seeds 100–115 only; on completion pull/hash-verify and report T2/T3 Holm m=2 α=.05
results with achieved CI/MDE under A5 interim precision; T2 proxy/range caveats; T3 assertion support; T1/T4 screening
failures; no S-generalisation; no confirmatory number cited yet.**

**Status: A5 EXECUTION ACCEPTED CONDITIONALLY — HOLD AGGREGATION until the aggregator is committed/pinned and the
manifest uncertainty/citation fields are corrected; then analyse seeds 100–115 only, report achieved CI/MDE and A5
interim precision; no confirmatory number cited.**

**Status: A5 APPROVED (conditional on conditions 1–2 being recorded before aggregation); no confirmatory number cited.**

**Status: RESOURCE WARNING RECORDED; RUN CONTINUES PENDING LEAD DECISION; no confirmatory number cited.**

**Status: LAUNCH OBSERVED / APPROVED; RESULTS PENDING; pre-launch record remains the adjudication basis.**


**Status: CLEARED FOR LAUNCH once the Lead allocates the box and the 1–2 slot reserve is confirmed.** The manifest
status may then be flipped from `FROZEN_PENDING_ADJUDICATOR_PRELAUNCH_RECORD` to frozen/approved. The run must report
PID/ETA/hashes and write a **separate** confirmatory artefact (`paperC_confirmatory.json` + per-cell checkpoints + run
manifest), never mixed with screening/Pilot-0.

## 4T. A5 confirmatory — **HALTED by statistical stop; NO RESULT (degenerate T2/T3)**

**Stop (2026-11-26 ~07:58 CST):** driver/cells killed (PIDs 2272/2273/2276–2285), finalizer/poller stopped,
checkpoints preserved (**10 rows / 6 cells; no aggregation, no summary**), `queue/STOP_CONFIRM_A5` written; no new
confirmatory run launched. The adjudicator's box check was unreachable (SSH closed); the stop/checkpoint state is
recorded from the Lead's report and must be hash/row-count verified if the box returns. **No confirmatory numbers are
cited or usable.**

**Verified defects (from the QA-verified screening artefact `6bcc29a5…`, not confirmatory data):**
1. **T3 is degenerate.** `withheld` = **exactly 0.144 in all 96 exposed P55 runs — one distinct value**, SE 0; it is the
   arithmetic `0.4 × (1 − 0.55) × (1 − 0.2)`. There is no estimable effect; T3 is a **setting-arithmetic assertion**, not
   a confirmatory estimand. (A1.2 already called h>0/own>0.1 assertions; using T3 as a primary confirmatory test was
   invalid.)
2. **T2 is a manipulation check.** `own_share` is **C ≈ 0.889–0.945 (overall ≈0.919) vs A ≈0.148–0.524 (overall ≈0.348)**;
   C−A ≈ **0.406–0.741**, screening SE ≈0.0003. With `firm_ban=.9`, the treatment mechanically moves own/(own+firm);
   **the input returns as the output**. It is a compliance/validity check, not a behavioural effect.
3. **A5's m=2 Holm family (T2/T3 only) cannot fail** while the substantive **T1/T4 failed screening** (T1 +0.655 vs ≥3.0;
   T4 +1.767 vs ≥2.0, CI below 2). A "T2/T3 confirmed" report would present the model's settings as findings; the A5
   narrowing of the pre-declared T1–T4 family compounds the problem.

**Adjudication:** **A5 confirmatory is VOID/STOPPED — no confirmatory result, no claim.** The preserved 10 checkpoint
rows must **not** be aggregated or analysed for inference; they are a failed-run record. Screening T1/T4 failures stand.
T2/T3 are recategorised as **manipulation/compliance checks**, not estimands. The A5 resource amendment is moot.

**Required redesign before any confirmatory rerun (A6/Paper C v2):**
* Estimands must be **behavioural outcomes not mechanically determined by the treatment**: e.g. K–12 participation/
  spend/gap, learning L6/L9, fixed-R gap-close, rank-R admission; the treatment lever must **not enter the outcome's
  definition or denominator** (own_share with `firm_ban`, withheld with `pay_ratio`/`monitoring` are excluded).
* **Pre-launch degeneracy screen:** for every outcome, report distinct values/within-cell variance and the
  treatment→outcome mapping; reject SE=0/deterministic or input-derived outcomes; separate manipulation checks.
* **Multiplicity:** pre-declare the full substantive family (T1–T4 or a fixed new family) for Holm; **no post-screening
  family narrowing** to trivial tests.
* **Power/MDE:** re-estimate N/seeds for the behavioural endpoints; do not keep trivial endpoints to manufacture
  significance; a pilot may estimate variance, not select outcomes.
* **No reuse of A5 data**; new prereg + manifest + runner pins; report screening failures honestly.

**Final void record (commit `803c994`):** `PAPER_C_A5_SEED_TRUNCATION.md` sha
**`cd049ccd0002e62b170d4087ea350b04261ac604a4b6344f2b8c2346b8dc99d9`**; `PAPER_C_CONFIRMATORY_MANIFEST.json` sha
**`c0767c820bc8cde75c362e4b3efe9ac7ee174e3832eea871ec823c24bdb2821c`**, status **VOID** + `void_record` (stopped
07:58 CST; defects; state; A6 next). Execution state per the verified record: driver/cells killed
(2272/2273/2276–2285), finalizer killed, `queue/STOP_CONFIRM_A5`, **checkpoints preserved 10 rows / 6 cells**, no
aggregation/summary, Mac poller stopped, **box stays on**. Box SSH was unreachable (~07:45+) at the adjudicator check —
the preserved checkpoint/`STOP_CONFIRM_A5` state is **reported, not yet independently verified**; it will be hash/row-count
verified if connectivity returns. **Do not resume A5, do not start a new confirmatory run.** The preserved rows are a
failed-run record, not analysable. A6 redesign requirements recorded verbatim (see §4T above). **No Paper C confirmatory
claim exists; T1/T4 remain screening failures; no S-generalisation.**



**Status: A5 HALTED/VOID; Paper C confirmatory is not runnable under this design; no confirmatory claim; CSV frozen.**

## 5. Evidence-status register (programme level)

| Status | Count (paper + programme rows) | Notes |
|---|---|---|
| VERIFIED EMPIRICAL | **4** (4 A) | descriptive/associational; not causal; author committed E8 record |
| **REPRODUCED EMPIRICAL ANALYSIS** *(new-generation label, Lead-defined)* | **2** (2 A) | A-34 impact (+12.322 vs +12.44) and A-35 amplification (+25.083 vs +25.26) — fresh-WDI **CS-style group-time ATT**; manifest-hashed vintage |
| REPRODUCED SIMULATION | **25** (2 A, 12 B, 11 programme) | all conditional and/or uncalibrated unless marked; includes the 100-seed Paper B new generation (CF4 reversal + unmeasured-welfare-change caveat), the closed X-27 pre-registered gate-architecture grid (primary H2 +5.0551 pp; clean re-run confirmed), the three Paper C provisional anchors (C-01…C-03), the new-generation forecast (A-37), the 74.88 % infeasibility finding (A-38), the re-executed ABC audit, the re-executed bootstrap factorial, and the Paper B 540 table regeneration |
| VALIDATED SIMULATION | **4** (1 A, 3 programme) | **A-39 item (d) local identifiability (stop gate met with declared restriction)**; engine/PL module validation, corrected DGP design, bootstrap size/power |
| AUTHOR-REPORTED | **44** (20 A, 18 B, 6 programme) | **AUTHOR-REPORTED BASELINE**: the 420 generation, the Paper A Exp 1/3/4/5 legacy numbers, the author JSON bundle; not results, not reproduced, not to be silently replaced |
| CONTRADICTED | **33** (8 A, 14 B, 11 programme) | only where committed code/algebra/measured audit output refutes the claim; includes the 100 % paradox, invalid E1/Q3, legacy DGP, "published benchmark" attributions, and the Paper B policy reversals |
| UNRESOLVED | **20** (2 A, 0 B, 18 programme) | A-31 replication inventory; A-36 bulge `t*` (no-effect evidence); Paper C confirmatory prereg (C-04); Paper D omissions/divergences (D-01/D-03) and inventory attribution risk (D-04); Model Zoo D1/D2 + run gate + Pilot-0 provenance (MZ-01…MZ-04); evidence-layer limits (EV-01…EV-04); X-30 (Lean methods artefact — not a scientific claim); canonical spec/Gate-2; GPU quarantine |

The machine-readable one-row-per-claim record is `results/audit/paper_claims.csv` (132 rows; sha256
`07f83156cb6f4cb22a46516ebbe313f5db47d22e7a6de0025f2d6625ddf6f9cb`). The Lead-defined new-generation label **REPRODUCED EMPIRICAL ANALYSIS** is used for the fresh-WDI E8 rows; all
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
