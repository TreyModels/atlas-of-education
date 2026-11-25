# BOOTSTRAP REPORT — P0-04 (size/power factorial) + P0-05 (invalid within-country permutation)

**Owner:** `qa-verifier` · **programme:** Atlas contest audit v2 · **date:** 2026-11-25
**Code:** `docs/audit/code/bootstrap_factorial.py` (commit `ffed664`; NumPy only, no GPU/torch).
**Artifacts:** `docs/audit/BOOTSTRAP_SIZE_POWER_RESULTS.parquet` (60-cell factorial),
`results/audit/boostrap_factorial_summary.json` (benchmark reproduction, permutation invariance,
replacement-inference sizes), box log `results/audit/bootstrap_factorial_box.log`.
**Evidence status:** `VALIDATED SIMULATION` (this is a Monte-Carlo size/power study of the shipped
inference procedure, not an empirical claim).

**Run:** box `/root/work/qa`, declared-stack venv (`/root/work/venv-declared/bin/python`, py3.10.8 /
numpy 2.2.6 / scipy 1.15.3), `--workers 4`, `--n-datasets 2000`, `--seed 20261125`, `nice -n 10`,
BLAS/OMP=1. **Runtime 70.21 s**, exit 0.

---

## 1. The defects this addresses (P0-04 / P0-05, verified in `EXTERNAL_AUDIT_GPU_2026-11-25.md`)

The shipped E1/Q3 selftest (`gpu_e1_q3_wild_cluster_ri.py:172-185`) generates

```
c_eff = Normal(0,1)[country]
x1    = Normal(0,1) + 0.5·c_eff            # country effect in the regressor
y     = 0.2 + 0.8·active_c·x1 + 0.3·x2 + c_eff + noise   # ... and in the outcome
```

and the **pooled** regression omits `c_eff` → omitted-variable bias (OVB). Clustered SEs address
within-cluster correlation, **not** OVB. The shipped country-block permutation
(`x*_it = x̄_{π(i)} + (x_it − x̄_i)`) is, after country FE,
`x*_it − x̄*_i = x_it − x̄_i` **identically** — a within-invariant transform, so it cannot test the
within estimand (algebraic identity, not a finite-sample issue).

## 2. Design (matched to the shipped selftest; G=60 countries, T=20 years, N=1,200 observations)

* DGP: `x1 = e + κ·c_eff`, `y = 0.2 + τ·active·x1 + 0.3·x2 + c_eff + ε`, `τ = 0.8`; active countries
  are a **random subset** of size `round(share·G)` (exchangeable across countries by construction).
* Factorial: minority-effect share ∈ {0, 5, 15, 50, 100 %} × country confounding κ ∈ {0, 0.25, 0.5, 1.0}
  × estimator ∈ {pooled OLS, country FE, country+year FE}; **2,000 independently generated datasets
  per cell** (60 cells; 120,000 datasets total). OLS/within fits with **CR1 cluster-robust SEs**
  (G/(G−1) correction, same convention as the shipped code); two-way within transformation by
  alternating demeaning (15 iterations).
* Size is measured in the true-null world (share = 0, `τ·active ≡ 0`); power/bias/coverage on the
  alternative worlds; nominal level 5 %, `|t| > 1.96`.

## 3. Independent reproduction of the shipped/auditor statistics

| statistic | shipped/auditor value | this independent NumPy implementation |
|---|---|---|
| pooled β (selftest, seed 20261125) | 0.4447407388610457 | **0.4447407388610453** |
| CR1 SE | 0.08291358451449403 | **0.08291358451449392** |
| t | 5.363906788800104 | **5.363906788800106** |
| wild-cluster p (Rademacher, B=2000) | 0.0004997501249375312 | **0.0004997501249375312** |
| **negative control** (τ = 0 everywhere): pooled β | 0.3054 (auditor) | **0.30544388867506994** |
| negative control t | 4.975 (auditor) | **4.974547803854034** |
| negative control wild-cluster p | 0.0005 (auditor) | **0.0004997501249375312** |

Reproduction is exact to floating-point tolerance; the auditor's four reported statistics and its
negative control are confirmed. **The shipped selftest is "significant" at p≈0.0005 when the true
effect is zero in every country** — it cannot attribute its result to minority-effect leakage.

## 4. Task A — size/power factorial

### 4.1 Size at the true null (share = 0; rejection rate at nominal 5 %)

| country confounding κ | pooled OLS | country FE | country+year FE |
|---|---|---|---|
| 0.00 | 0.050 | 0.054 | 0.056 |
| 0.25 | **0.996** | 0.056 | 0.056 |
| 0.50 | **1.000** | 0.062 | 0.052 |
| 1.00 | **1.000** | 0.062 | 0.052 |

**Size control first:** the country-FE and country+year-FE estimators hold the nominal 5 % level
(0.052–0.062) regardless of confounding, because FE absorbs `c_eff`. The pooled estimator is
**correct only when κ = 0**; with country confounding it rejects a true null 99.6–100 % of the time —
exactly the OVB the auditor identified. This is the headline: the shipped pooled "significant"
finding is not evidence of a minority effect.

### 4.2 Bias (posterior/point estimate minus the true average effect)

share = 15 % (true average effect = 0.8 × 9/60 = 0.12):

| κ | pooled OLS | country FE | country+year FE |
|---|---|---|---|
| 0.00 | +0.001 | +0.000 | −0.001 |
| 0.25 | **+0.231** | +0.001 | +0.001 |
| 0.50 | **+0.394** | +0.000 | −0.002 |
| 1.00 | **+0.493** | +0.001 | +0.000 |

### 4.3 Coverage of the 95 % CI (share = 15 %)

| κ | pooled OLS | country FE | country+year FE |
|---|---|---|---|
| 0.00 | 0.993 | 0.996 | 0.995 |
| 0.25 | **0.020** | 0.995 | 0.994 |
| 0.50 | **0.000** | 0.998 | 0.998 |
| 1.00 | **0.000** | 0.996 | 0.996 |

### 4.4 Power (share = 15 %, true average effect 0.12)

| κ | pooled OLS | country FE | country+year FE |
|---|---|---|---|
| 0.00 | 0.613 | 0.786 | 0.785 |
| 0.25 | **1.000** (spurious) | 0.788 | 0.802 |
| 0.50 | **1.000** (spurious) | 0.792 | 0.789 |
| 1.00 | **1.000** (spurious) | 0.779 | 0.797 |

At 50 % and 100 % minority share all estimators have power 1.00 (not shown in full; the parquet has
all 60 cells). The pooled "power" at κ>0 is **not** power: it is 100 % rejection of a false pooled
model under OVB. The FE estimators have honest power ≈0.78–0.80 at a 12 % average effect, and their
size is nominal, so the FE-based E1/Q3 design is the defensible one.

## 5. Task B — the permutation cannot test the within estimand; replacement inference

### 5.1 Algebraic and numerical proof (P0-05)

For `x*_it = x̄_{π(i)} + (x_it − x̄_i)`, the within transform gives
`x̄*_i = x̄_{π(i)}` and hence `x*_it − x̄*_i = x_it − x̄_i` for every permutation π.

Numerical check (200 random country permutations, the shipped selftest data):

| quantity | value |
|---|---|
| max abs deviation of within-transformed `x*` from `x` | **6.66e-16** |
| original country-FE β | 0.10534536554775698 |
| max abs deviation of permuted FE β from original | **9.71e-17** |
| pooled β sd across permutations (the shipped test's estimand) | 0.0563 |

So the FE coefficient is **bit-identical for every permutation**; a permutation p-value computed on
the within estimand is exactly degenerate. The shipped `p_block_perm = 0.001` is a *pooled* p-value —
it tests the pooled estimand (which the design does not want) and is dominated by cross-country
variation. **Adding FE to the shipped permutation cannot repair it**; the resampling must change.

### 5.2 Replacement inference (restricted wild-cluster bootstrap + whole-trajectory cluster bootstrap)

Null world (share = 0), country-FE estimator, 120 replicate datasets per κ, Rademacher weight grid:

| κ | restricted wild-cluster bootstrap size | whole-trajectory cluster bootstrap size | cluster-bootstrap 95 % coverage |
|---|---|---|---|
| 0.00 | 0.025 | 0.042 | 0.958 |
| 0.25 | 0.025 | 0.033 | 0.967 |
| 0.50 | 0.042 | 0.033 | 0.967 |
| 1.00 | 0.033 | 0.050 | 0.950 |

Both replacements control size at ≈5 % (or slightly under, which is the safe direction) **without
using the invalid permutation**, and the cluster bootstrap's coverage is 0.95–0.97. The wild-cluster
bootstrap is the recommended primary test for the FE estimand (it imposes the null exactly and keeps
the cluster dependence); the whole-trajectory cluster bootstrap is the recommended uncertainty
interval / robustness companion (whole countries resampled, preserving temporal dependence).

**Exchangeability caveat (defended explicitly):** the permutation-based null needs exchangeable
countries, which is not defensible for this panel (countries differ in institutions/school systems).
The replacement schemes avoid that assumption: the wild-cluster bootstrap keeps each country's
trajectory and only randomises cluster-level residual signs; the whole-trajectory bootstrap resamples
whole countries and therefore estimates sampling variability *of the observed country set*, not a
cross-country exchangeability null. For a finite set of countries the target is the sample estimand,
which is what the paper's FE specification estimates.

## 6. Conclusions (one line each)

1. **The shipped pooled E1/Q3 selftest cannot separate minority-effect leakage from OVB**: with a true
   null and κ ≥ 0.25 it rejects at 99.6–100 % (auditor's negative control reproduced exactly).
2. **Country FE (and country+year FE) hold nominal 5 % size** (0.052–0.062) across confounding, with
   honest power ≈0.78–0.80 at a 12 % average effect and ≈1.0 at ≥50 %.
3. **The shipped country-block permutation is within-invariant** (6.7e-16): it cannot test the within
   estimand and must be replaced.
4. **Restricted wild-cluster bootstrap** (size 0.025–0.042) and **whole-trajectory cluster bootstrap**
   (size 0.033–0.050, coverage 0.95–0.97) are valid replacements; the post-repair E1/Q3 inference
   should use the FE estimator with these.
5. The auditor's four reported statistics (β = 0.444740738861045, SE = 0.082913584514494, t =
   5.363906788800104, p = 0.0004997501249375312) and the negative control are **independently
   reproduced**.

## 7. Artifacts

| artifact | content |
|---|---|
| `docs/audit/BOOTSTRAP_SIZE_POWER_RESULTS.parquet` | 60 cells: share × confounding × estimator, n=2000 datasets/cell, beta_mean/sd, bias, rmse, mean_se, rejection_rate, coverage95, t moments, size_or_power |
| `results/audit/boostrap_factorial_summary.json` | benchmark reproduction, negative control, permutation invariance, replacement-inference sizes, acceptance flags |
| `results/audit/bootstrap_factorial_box.log` | box run log (runtime 70.21 s, exit 0) |
| box sha256 | `41c628952d89ccad…` (parquet), `e266710d185720bb…` (summary) |

## 8. Limitations

* Simulation magnitudes (κ, τ = 0.8, G = 60, T = 20, n = 1,200) are the shipped selftest's, so this
  study validates the *procedure*, not any empirical E1/Q3 estimate.
* CR1 SEs with G = 60 are slightly anti-conservative in general; the FE sizes here are 0.052–0.062,
  consistent with that; wave-2 should report a small-G sensitivity (wild bootstrap is the fix).
* The two-way FE within transform uses 15 alternating projections (max residual deviation <1e-12);
  documented rather than exact-solved.
