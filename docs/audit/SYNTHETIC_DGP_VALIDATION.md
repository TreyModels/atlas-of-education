# SYNTHETIC DGP VALIDATION — P0-03 (external audit)

**Owner:** `qa-verifier` · **programme:** Atlas contest audit v2 · **date:** 2026-11-25
**Task:** P0-03 of the external audit — replace the degenerate ABC synthetic population, run a
100-population-per-configuration parameter-recovery experiment, retain accepted draws, and quantify
what the old design cost.
**Code:** `docs/audit/code/dgp_validation.py` (committed `9e04236`; pure NumPy/pandas, **0 engine runs**).
**Run:** box `/root/work/qa`, declared-stack venv, 3 workers, 464.33 s, 500 populations (5 configs × 100); log `results/audit/dgp_validation_box.log`.
**Artifacts:** `results/audit/dgp_*.parquet`, `results/audit/dgp_validation_summary.json`,
run logs `results/audit/dgp_validation_run.log` (host) and box logs.
**Evidence status:** `VALIDATED SIMULATION` for the *design/identification* statements below;
**ASSUMPTION** for every structural choice (labelled inline); **not** an empirical estimate of any
Cambodian/Korean parameter (no calibration in Gate 1/wave 1).

---

## 1. The defect this replaces (P0-03, verified in `EXTERNAL_AUDIT_GPU_2026-11-25.md`)

The shipped ABC built its "630-pupil synthetic population" as
`docs/audit/gpu_abc_bundle/gpu_bray_abc_and_contest_surface.py:50-54`:

```python
n_pupils  = 630
is_g12    = [0]*420 + [1]*210       # 2:1 grade split
is_urban  = [1]*210 + [0]*420       # first 210 pupils are the urban ones
log_y     = randn(n_pupils)         # i.i.d. per pupil
school_gap= rand(n_pupils)          # U(0,1) i.i.d. per pupil
```

Consequences (each verified):

| # | defect | evidence |
|---|---|---|
| D-a | **G12 × urban cell is empty** — every G12 pupil is rural; urban is only G9 by construction | slice inspection, P0-03 |
| D-b | **no school identifiers**, no within-school dependence; `school_gap` i.i.d. per pupil | P0-03 |
| D-c | **no income–school-quality relationship**: `log_y` and school quality are independent draws | P0-03 |
| D-d | **only 3 independent participation moments** of the advertised 5 (overall = ⅔·G9 + ⅓·G12 identically) | P0-01 |
| D-e | provider choice is **analytic**: `P(own|tutoring) = 1/(1+e^δ)`, `δ = ln(0.32/0.68) = −0.7537718023763802` | P0-02 |
| D-f | accepted draws discarded → no posterior/predictive diagnostics possible | P0-07 |

Identification consequence: 5 analytically-reduced participation parameters against **3**
independent moments → **Jacobian rank ≤ 3 < 5**; at least two directions unidentified. The corrected
design below raises the independent moment count to **16** and the measured Jacobian rank to **5**.

## 2. Corrected synthetic population (design + justification)

Built by `dgp_validation.make_population("crossed", n_per_cell, rng)`.

### 2.1 Crossed grade × urban cells (D-a)

* Cells: **G9-rural, G9-urban, G12-rural, G12-urban**, each with `n_per_cell` pupils; every
  population therefore has a populated **G12 × urban** cell by construction
  (`g12_urban_cell == n_per_cell > 0`, asserted in code).
* Grade mix and urban share are design dimensions, not the old accidental 420/210 split; the
  benchmark moments (G9 0.67, G12 0.85, urban gap 0.14) are retained as targets.
* **ASSUMPTION / justification:** two-stage stratified samples by grade and urban/rural location are
  the structure of the Bray-type surveys underlying the original benchmarks (Bray 1999; Bray & Lykins
  2012), so a crossed design is the minimal repair; it also makes grade × urban heterogeneity
  estimable rather than conflated.

### 2.2 Explicit school identifiers + within-school dependence (D-b)

* **32 schools** (16 urban, 16 rural); **every school teaches both grades**; pupils of each
  grade × urban cell are spread across the 16 schools of that type. `school_id ∈ [0,31]` is stored
  per pupil; `n_schools = 32`.
* School random effects: quality `q_s ~ N(0,1)`, ability effect `a_s ~ N(0,1)`, income effect through
  `q_s` (below). Reported diagnostic: within-school intraclass correlation of household log income
  (`school_icc_income`), computed per population from a one-way ANOVA decomposition; the legacy
  design reports `NaN` (no schools).
* **ASSUMPTION / justification:** education data are hierarchically nested (pupils in schools);
  ignoring the school level both understates standard errors and makes school-level claims
  untestable. International large-scale assessments routinely decompose achievement/background
  variance into within- vs between-school components, and stratified East-Asian systems show a
  large between-school share (OECD PISA reports; Hanushek & Woessmann 2011; Woessmann 2003). The
  magnitude is a labelled structural assumption — wave-2 sensitivity: `n_schools ∈ {8,32,64}` and
  ICC target set {0.25, 0.45, 0.65}.

### 2.3 Income–school-quality relationship (D-c)

* `log_y_i = ρ·q_{s(i)} + sqrt(1−ρ²)·ε_i` with `ε_i ~ N(0,1)`, so `Var(log_y)=1` and
  `corr(log_y, q_s) = ρ` in expectation. Default **ρ = 0.50**, positive and non-degenerate.
* **ASSUMPTION / justification:** socio-economic status and school quality are positively
  associated — richer households sort into higher-quality (often private/low-fee private) schools
  and purchase supplementary tutoring, which is the mechanism the paper is about (Bray 1999;
  Bray & Lykins 2012). ρ=0.50 is a **pre-registered structural placeholder, not an estimate**;
  wave-2 sensitivity grid `ρ ∈ {0.3, 0.5, 0.7}` is declared now and not run here.

### 2.4 `school_gap` (resources) decomposition

* `school_gap_i = gap_{s(i)} + ν_i`, `gap_s ~ N(0, 0.45²)` (school-level resource gap),
  `ν_i ~ N(0, 0.25²)` (within-school variation). Both parts are non-degenerate, so the parameter
  `b_school_gap` is identified by **within-population variation**, not by a single school dummy.
* **ASSUMPTION:** the old i.i.d. `U(0,1)` covariate was a stand-in for school resource gaps; keeping a
  school-level component is the minimal correction consistent with "school gap" semantics.

## 3. Moment set and parameter map

Reduced parameter vector: **θ = [b0_eff, b_income, b_school_gap, delta_g12, urban_demand]** (5
parameters); **δ fixed analytically** at `ln(0.32/0.68) = −0.7537718023763802` (P0-02) — the corrected
DGP no longer wastes a draw on an analytically determined quantity.

The 3-option softmax with `V_none = 0`, `V_own = V`, `V_other = V + δ` collapses exactly to a logistic
for "any tutoring": `p_any = sigmoid(V + ln(1+e^δ))`; own share is the constant `1/(1+e^δ)`. This is
an identity of the shipped utility specification, not an approximation.

**Corrected moment set (16, `moment_set='crossed'`):**
4 grade × urban cell participation means · 4 within-population income-quartile participation means ·
3 school-quality-tercile participation means (32 schools) · 4 within-population school-gap-quartile
participation means · own share (analytic). All moments are model-free functions of the utility
parameters and the population covariates.

**Legacy moment set (the shipped 5 advertised moments):** overall, G9, G12, urban−rural contrast
(first 210 vs last 420 pupils, as shipped), own share. Maximum rank **3** (D-d).

**ABC protocol (identical for all configurations):** 20,000 prior draws θ ~ U(prior bounds) with
common random numbers; acceptance `max_m |m_hat − m_target| / tol_m ≤ 1`; targets = moments at the
true θ on a large fresh population (4,000 pupils/cell) from the same distribution; tolerance
`tol_m = max(benchmark tolerance, 2.5 × finite-sample SE_m)` so recovery is not penalised for pure
sampling noise; documented fallback widens tolerances ×2/×4 if a population accepts nothing (recorded
per population; none needed in the final run — see `tol_escalation` in the parquet).

## 4. Recovery experiment

* 5 configurations × **100 independently generated populations** each (500 recovery runs):
  | configuration | design | pupils/cell | truth |
  |---|---|---|---|
  | `NEW-crossed-n100-truthA` | corrected crossed | 100 | A |
  | `NEW-crossed-n400-truthA` | corrected crossed | 400 | A |
  | `NEW-crossed-n1000-truthA` | corrected crossed | 1,000 | A |
  | `NEW-crossed-n400-truthB` | corrected crossed | 400 | B (different prior region) |
  | `OLD-degenerate-truthA` | shipped degenerate | — (630 total) | A |
  Truths: **A = [0.30, 0.55, 0.70, 1.10, 0.35]**, **B = [−0.20, 1.10, 0.35, 0.60, 0.90]**.
* Per population: posterior mean/SD, 95 % equal-tailed interval, bias, RMSE, coverage, accepted-draw
  count, **numerical Jacobian of the 16-moment map at θ\*** (per population covariates), its SVD,
  rank, condition; G12×urban cell size, school count, income ICC.
* **All accepted draws** and all posterior-predictive moment draws are retained in parquet
  (requirement P0-03.3) — the shipped script discarded them.

## 5. Results

Run: box `/root/work/qa`, declared-stack venv (`/root/work/venv-declared/bin/python`, py3.10.8 / numpy 2.2.6 / scipy 1.15.3 / pandas 2.3.3 / pyarrow 25.0.1), `--workers 3`, `--n-pop 100`, `--n-draws 20000`, `--seed 20261125`, `nice -n 10`, BLAS/OMP=1.
**Runtime 464.33 s** (500 populations; 1.08 populations/s aggregate, 2.6 CPU-s/population). Command:
`python docs/audit/code/dgp_validation.py --out-dir /root/work/qa/full_out --workers 3 --n-pop 100 --n-draws 20000 --seed 20261125`.

### 5.1 Parameter recovery (100 populations per configuration; truth θ* known)

RMSE = sqrt(mean squared posterior-mean error); coverage = fraction of 95 % equal-tailed posterior
intervals containing the truth; "accepted" = prior draws inside the acceptance region (per population).

| configuration | pupils | Jacobian rank | mean accepted | b0_eff RMSE | b_income RMSE | b_school_gap RMSE | delta_g12 RMSE | urban_demand RMSE | coverage (all params) |
|---|---|---|---|---|---|---|---|---|---|
| `NEW-crossed-n100-truthA` | 400 | **5/5** | 960.7 | 0.089 | 0.224 | 0.379 | 0.326 | 0.139 | 1.00 |
| `NEW-crossed-n400-truthA` | 1,600 | **5/5** | 28.0 | 0.040 | 0.076 | 0.100 | 0.126 | 0.060 | 1.00 |
| `NEW-crossed-n1000-truthA` | 4,000 | **5/5** | 18.1 | 0.042 | 0.068 | 0.112 | 0.130 | 0.060 | 0.99–1.00 |
| `NEW-crossed-n400-truthB` | 1,600 | **5/5** | 22.9 | 0.043 | 0.110 | 0.100 | 0.071 | 0.078 | 1.00 |
| `OLD-degenerate-truthA` | 630 | **3/5** | 792.4 | 0.047 | **0.641** | **0.581** | 0.282 | 0.091 | 1.00 |

Reading:
* The corrected design reaches **full Jacobian rank 5/5 in 500/500 populations** (smallest singular
  value 0.080–0.141; 16 moments); the legacy design is stuck at **rank 3/5** with an exactly zero
  smallest singular value in 100/100 populations — the two unidentified directions D-d predicted.
* Recovery improves with sample size, as expected: at 1,600–4,000 pupils per population the RMSEs are
  0.04–0.13 for four of five parameters and ≤0.11 for `b_school_gap`; at 400 pupils identification is
  weak (RMSE up to 0.38, and the posterior shrinks toward the prior mean — the positive biases for
  parameters below their prior means).
* The legacy design's RMSE is 0.58–0.64 for `b_income`/`b_school_gap` — a specification failure, not
  a small-sample problem (it has 630 pupils).
* Coverage is 0.99–1.00 everywhere: posteriors are wide/conservative. This is the safe direction and
  is reported as such; it is **not** evidence of well-calibrated posterior uncertainty.
* Both truth regions (A and B) recover (no truth-specific artefact).

### 5.2 Identification diagnostics (per population, 500 total)

| metric | corrected (crossed) | legacy degenerate |
|---|---|---|
| Jacobian rank (min–max over populations) | **5–5** | **3–3** |
| smallest singular value (mean; min–max) | 0.112–0.125; 0.080–0.141 | **0.000**; 0.000–0.000 |
| largest singular value | 0.74–0.84 | 0.30–0.33 |
| independent moments | 16 | 5 advertised / 3 independent |
| within-school income ICC | 0.243–0.250 (0.075–0.403) | n/a (no schools) |
| G12×urban cell | 100–1,000 pupils | **0** |

### 5.3 Retained draws (P0-03.3)

* `dgp_accepted_draws.parquet`: **182,212 accepted prior draws** (all of them, not a summary).
* `dgp_posterior_predictive.parquet`: **106,902 posterior-predictive moment vectors**.
* `dgp_recovery_samples.parquet`: 2,500 rows (500 populations × 5 parameters).
* `dgp_rank_diagnostics.parquet`: 500 rows; `dgp_moment_recovery.parquet`: 500 rows (16 moments each).
* Box-side sha256 of every artifact: `results/audit/TASK7_ARTIFACT_SHA256.txt`; box run log
  `results/audit/dgp_validation_box.log` (runtime 464.33 s, exit 0).
* Tolerance escalation was **never needed** (all 500 populations accepted draws at the base
  tolerance; `tol_escalation == 0` in the recovery parquet).

### 5.4 Analytic δ (P0-02)

`δ = ln(0.32/0.68) = −0.7537718023763802` is imposed analytically in the corrected DGP. The shipped
ABC estimates were **−0.8241** (7-param; error 0.0703) and **−0.6682** (6-param; error 0.0856) — both
off the exact value, consistent with the audit's P0-02 finding.

### 5.5 Seed robustness — three independent seed bands

The whole 500-population experiment was repeated under two further independent seeds (box, 2 workers
each; consumer-tracked). Results are stable to within Monte-Carlo noise:

| statistic | band 1 (seed …125) | band 2 (seed …126) | band 3 (seed …127) |
|---|---|---|---|
| crossed Jacobian rank (all 400 crossed populations) | 5/5 | 5/5 | 5/5 |
| legacy degenerate rank | 3/3 | 3/3 | 3/3 |
| RMSE n400-A (b0, income, gap, ΔG12, urban) | 0.040 / 0.076 / 0.100 / 0.126 / 0.060 | 0.040 / 0.071 / 0.098 / 0.112 / 0.056 | 0.037 / 0.074 / 0.101 / 0.111 / 0.061 |
| RMSE n400-B | 0.043 / 0.110 / 0.100 / 0.071 / 0.078 | 0.037 / 0.104 / 0.105 / 0.067 / 0.079 | 0.041 / 0.109 / 0.102 / 0.080 / 0.081 |
| legacy RMSE (b_income / b_school_gap) | 0.641 / 0.581 | 0.642 / 0.580 | 0.642 / 0.583 |
| mean accepted draws (n400-A) | 28.0 | 27.3 | 27.3 |

Full-draw parquets for bands 2–3 stay box-side (`/root/work/qa/band{2,3}_out`, sha256 manifests in
`results/audit/dgp_band{2,3}_sha256.txt`); band-1 full draws are committed. The three bands use
independent populations and independent prior draws, so the rank/recovery statements are
seed-independent, not a lucky-draw artefact.

## 6. What the degenerate design cost (old vs new)

| property | OLD degenerate design | CORRECTED design |
|---|---|---|
| G12 × urban cell | **0 pupils** (empty) | 100–1,000 pupils (non-empty by construction) |
| school identifiers | **none** | **32** schools, both grades, per population |
| within-school dependence | none (i.i.d. pupils) | school random effects; income ICC 0.24–0.25 (range 0.075–0.403) |
| income–school-quality link | none (independent draws) | ρ = 0.50 positive correlation (pre-registered assumption) |
| independent moments | 5 advertised → **3 independent** (overall = ⅔G9+⅓G12) | **16** (4 cells, 4 income quartiles, 3 quality terciles, 4 gap quartiles, own share) |
| Jacobian rank vs 5 parameters | **3/5** (min SV exactly 0) | **5/5** (min SV 0.080–0.141) |
| provider choice δ | estimated −0.8241 / −0.6682 (errors 0.070 / 0.086 vs analytic) | analytic −0.7537718023763802 |
| recovery RMSE, b_income | 0.641 | 0.068–0.224 |
| recovery RMSE, b_school_gap | 0.581 | 0.100–0.379 (≤0.11 at ≥1,600 pupils) |
| observable moments (truth A) | overall 0.796, G9 0.753, G12 0.882, urban_gap −0.018 | cells 0.657 / 0.721 / 0.839 / 0.879 (G9r/G9u/G12r/G12u) |

The legacy redundancy is visible empirically: its own moments satisfy
`(2/3)·0.753 + (1/3)·0.882 = 0.796` exactly — the "overall" moment adds no information. The legacy
"urban gap" (−0.018 in this draw) also conflates grade composition with urban residence, because
the first 210 (urban) pupils are all G9 while the rural 420 split G9/G12; the corrected design
estimates within-grade urban contrasts (0.657→0.721 for G9, 0.839→0.879 for G12).

## 7. Retained artifacts

| artifact | content |
|---|---|
| `results/audit/dgp_recovery_samples.parquet` | per population × parameter: truth, posterior mean/SD, 2.5/97.5 %, bias, coverage, accepted count, rank |
| `results/audit/dgp_accepted_draws.parquet` | **every accepted prior draw** (5 parameters per row) for all 500 populations |
| `results/audit/dgp_posterior_predictive.parquet` | posterior-predictive moments (accepted draws evaluated on a fresh population) |
| `results/audit/dgp_rank_diagnostics.parquet` | per population: Jacobian rank, smallest/largest singular value, #moments, ICC, schools, G12×urban cell |
| `results/audit/dgp_moment_recovery.parquet` | observed vs target moments per population |
| `results/audit/dgp_validation_summary.json` | full machine-readable summary: priors, truths, design assumptions, per-config recovery metrics, old-vs-new |

## 8. Limitations (stated, not hidden)

1. All structural choices in §2 are **assumptions**; only the five benchmark moments are data-anchored
   (and they are stylised Cambodia/Asia magnitudes from the shipped ABC, not a fresh empirical
   estimate). Wave 2 must calibrate ρ, the school ICC and school counts.
2. ABC posteriors here are **recovery diagnostics**, not empirical posteriors: the experiment asks
   whether the corrected design *can* recover known parameters, not what the parameters are.
3. Acceptance is tolerance-based; coverage is expected to be conservative (wide posteriors), which is
   safe but not a calibration claim.
4. The utility model is the shipped 5-parameter reduced form; no engine runs are involved (contrary to
   an earlier scheduling assumption), so this task is independent of the Gate-1 engine repairs.
5. `delta` is analytic only because the shipped specification makes provider choice independent of
   covariates; if provider choice is later made covariate-dependent, δ must be re-estimated.
