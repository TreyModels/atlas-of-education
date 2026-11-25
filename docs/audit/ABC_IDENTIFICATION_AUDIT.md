# ABC_IDENTIFICATION_AUDIT — moment rank, null space, and what the synthetic Bray ABC can identify

**Lane:** `contest-math` (P0-01 + P0-02 of the external GPU-bundle audit, task-6). **Date:** 2026-11-25.
**Branch:** `research/contest-audit-v2-2026-11-25`. **Deliverable:** this report +
reproducible harness `docs/audit/code/abc_identification_audit.py`
(sha256 `25da334f90ab9ad8fe494dfc581290b9109ffec56125d2e8f1fc0dfc84e592f6`, commits `5fcee05`/`8281dd9`).
**Authoritative record of the defects:** `docs/audit/EXTERNAL_AUDIT_GPU_2026-11-25.md` (P0-01/02/03).
**Evidence class:** deterministic numerical algebra on a *frozen synthetic design* — not an empirical or
simulation claim. No archived ABC output is used as evidence; archived `best_theta` values appear only as
clearly-marked arithmetic checks (the whole GPU bundle is `QUARANTINED`).

---

## 0. Bottom line

1. **The five advertised moments have rank 4, not 5.** `m_part = ⅔ m_g9 + ⅓ m_g12` holds identically for every
   θ (420 G9 / 210 G12 pupils); the left-null certificate is exact (residual ≤ 3.4e-16 over 1,000 prior-box
   points) and the Jacobian has numerical rank 4/5 at **1,000/1,000** points. With 6 active parameters the
   null space is **2-dimensional**: at least two directions are locally unidentified, and in fact 44 distinct
   parameter vectors inside the frozen prior box reproduce the same five moments.
2. **What is actually identified** by the advertised moments is only: the provider-choice parameter δ
   (**analytic**, not estimated) and the **three cell participation probabilities** A (urban G9), B (rural G9),
   C (rural G12). The income slope, the school-quality slope and their trade-offs against the intercepts are
   **not identified** by these moments; the archived posterior spread along those directions is prior-driven.
3. **P0-02 confirmed independently:** `P(own|tutoring) = 1/(1+e^δ)` exactly, δ = ln(0.32/0.68) =
   **−0.7537718023763802**, giving own share 0.68 to 1.1e-16 and exactly invariant to income, school gap, grade
   and urban residence. The archived estimates (69.51 % / 66.11 %) are 1.51 / 1.89 pp off — **inside the frozen
   6 pp tolerance**, so tolerance-based ABC acceptance masked a parameter that is exactly solvable.
4. **Reduced problem (after δ substitution): 5 parameters, 3 independent participation moments → rank 3, null
   dimension 2 → exactly two further independent moments are required** to reach full local rank.
5. **Paper A micro-moments (our independent operationalisation):** one income + one within-grade
   school-quality micro-moment restore rank **5/5** in the substituted 5-parameter model and **6/6** in the
   unsubstituted 6-parameter model. This is **local identification only** (full-rank Jacobian at a point;
   inverse-function theorem). Paper A's own Jacobian proposition must be recomputed from its own specification
   and **must not cite the archived ABC outputs** — see §5.
6. **New (composition) finding from the target algebra (P0-03 quantitative):** with zero urban Grade-12 pupils,
   the advertised "urban−rural gap = 0.14" is **not** a within-grade gap. The moments imply cell means
   A = 0.8233, B = 0.5167, C = 0.85, i.e. an **implied within-grade urban−rural gap of 30.7 pp**, more than
   twice the advertised number; 0.14 is a grade-composition-weighted mixture.

## 1. Object audited (frozen design, read-only)

From `docs/audit/gpu_abc_bundle/gpu_bray_abc_and_contest_surface_6param.py` @ `045a63e`
(sha256 `012b14bb…c1623f`; bundle frozen, not modified):

| item | value |
|---|---|
| synthetic population | 630 pupils = **420 G9** (210 urban + 210 rural) + **210 G12 (all rural)**; `is_urban = [1]×210 + [0]×420` |
| covariates | `log_y ~ N(0,1)`, `school_gap ~ U(0,1)`, drawn **per pupil, no school identifiers** |
| utilities | `V0 = 0`, `V_own = base`, `V_other = base + δ`; `base = θ0 + θ1·log_y + θ2·school_gap + θ3·is_g12 + θ4·is_urban` |
| 6 active parameters | θ0 (intercept), θ1 (income), θ2 (school gap), θ3 (G12), θ4 (urban), θ5 = δ_other |
| prior box | `lo = [-1, 0, 0, 0, -0.5, -2.5]`, `hi = [2.5, 2, 2.5, 2.5, 1.5, 1.5]` |
| advertised moments | `m_part, m_g9, m_g12, m_ur, m_own` = targets `0.73, 0.67, 0.85, 0.14, 0.68` |
| frozen tolerances | `τ = [0.05, 0.05, 0.05, 0.04, 0.06]` |
| 0.68 target ⇒ δ | `ln(0.32/0.68) = −0.7537718023763802` |

The archived script draws the population from a *GPU* `torch.Generator` and does not save the raw covariates,
so the exact realised population is not independently reproducible; the audit uses a NumPy population with the
same stated distributions and the frozen design (seed 20261125). Rank/null-space results are properties of the
moment map and are checked across 1,000 prior-box points; they do not depend on one draw.

## 2. Method

**Closed-form moment map.** With `σ_i = logistic(V_i + ln(1+e^δ))` the participation probability of pupil `i`
(three-option logit collapses to a binary logit),

```
m_part = mean_all σ_i,        m_g9 = mean_{420 G9} σ_i,      m_g12 = mean_{210 G12} σ_i,
m_ur   = mean_{210 urban G9} σ_i − mean_{420 rural} σ_i,     m_own = 1/(1+e^δ).
```

**Analytic Jacobian.** `∂σ_i/∂θ_j = σ_i(1−σ_i)·d_j(i)` with `d = (1, log_y, school_gap, is_g12, is_urban)`
and `d/dθ5 = [e^δ/(1+e^δ)]·d/dθ0`; `∂m_own/∂θ5 = −ω(1−ω)` with `ω = 1/(1+e^δ)`. Rows 1–4 are cell means;
`m_own` depends on θ5 only. Verified against central finite differences (`h=1e-6`) at 200 prior-box points:
**max abs err 2.6e-10, max rel err 4.3e-6** (cell Jacobian: 2.0e-10).

**Rank / null space.** SVD of the Jacobian; numerical rank with relative threshold 1e-10 (the exact rank gaps
are ≥ 1e-2, so the result is threshold-insensitive). Null space = right singular vectors with zero singular
value. Scaling: columns rescaled by the prior widths `hi−lo`; null spaces compared by principal angles.

**Target manifold.** Invert the advertised moments to cell means:
`B = (4 m_g9 − m_g12 − 2 m_ur)/3 = 0.516667`, `A = 2 m_g9 − B = 0.823333`, `C = m_g12 = 0.85`
(check: `(A+B)/2 = 0.67`, `A−(B+C)/2 = 0.14`). With δ pinned, solve the 3 cell equations in the 5 parameters
by box-projected damped Gauss-Newton from 61 starts (1 archived-arithmetic start + 60 prior-box starts).

**Micro-moments (candidate definitions).** Within-grade **tercile gaps**:
`m_inc_g = mean σ(top income third) − mean σ(bottom income third)`, and the same on `school_gap` within each
grade; a pooled version averages the two grades. (These are *our* operationalisations of Paper A's proposal;
Paper A's exact definitions are not supplied — see §5.)

**Uncertainty.** Rank is a property of the map; survey tolerances τ only set practical precision. The
τ-standardised information matrix `Jᵀ diag(1/τ²) J` is inverted on the identified directions (pseudo-inverse
in the null directions) to report implied parameter 1σ at τ, τ/2, 2τ.

## 3. Results

### 3.1 Structural redundancy (P0-01) — `m_part ≡ ⅔·m_g9 + ⅓·m_g12`

| check | value |
|---|---|
| symbolic identity | `(1/630)Σ_all = (420/630)·mean_G9 + (210/630)·mean_G12 = ⅔ m_g9 + ⅓ m_g12`, for every θ |
| target identity `0.73 = ⅔(0.67)+⅓(0.85)` | residual `+0.0e+00` |
| numeric identity over 1,000 prior-box points | `max |m_part − ⅔ m_g9 − ⅓ m_g12| = 3.33e-16` |
| left-null certificate `ℓ = (1, −⅔, −⅓, 0, 0)` | `max |ℓ·J| = 3.43e-16` over 1,000 points (exact for all θ) |
| rank of 5×6 Jacobian | **4 at 1,000/1,000 points** → maximum rank 4 < 6 parameters |
| rank of the 4 participation rows (4×6) | 3 |
| rank of the 3×5 cell-mean Jacobian | 3 |
| null-space dimension (6 parameters − rank 4) | **2** |

5×6 singular values (median over 1,000 points, descending; the fifth is the structural zero):

| scaling | s1 | s2 | s3 | s4 | s5 | median cond (s1/s4 per point) |
|---|---|---|---|---|---|---|
| raw θ | 0.2516 | 0.1503 | 0.0843 | 0.0341 | 2.6e-17 | 7.03 |
| prior-box standardised | 0.9526 | 0.4616 | 0.1989 | 0.0818 | 6.5e-17 | 10.41 |

(SV columns are medians over points; the condition number is the median of the per-point ratio `s1/s4`, which is
why it is not the ratio of the two medians.) The structural rank (4) and null-space dimension (2) are invariant under invertible column scaling; the
mapped null spaces coincide (principal-angle deviation 8.9e-16). The condition number changes with scaling —
that is why condition numbers are **not** identification evidence, and the archived "posterior correlation
condition number (25.96 → 21.03)" is not a rank statistic.

### 3.2 Target point, local null space, finite non-identification

| quantity | value |
|---|---|
| implied cell means | `A (urban G9) = 0.823333`, `B (rural G9) = 0.516667`, `C (rural G12) = 0.850000` |
| representative θ* | `[−0.742049, 0.246164, 0.937204, 1.629669, 1.421925, −0.753772]` (all inside the prior box) |
| moments at θ* | `m_g9 = 0.670000`, `m_g12 = 0.850000`, `m_ur = 0.140000`, `m_own = 0.680000` |
| 3×5 cell Jacobian | rank 3, singular values `[0.35124, 0.13452, 0.10096]`, null dim 2 |
| 5×6 Jacobian at θ* | rank 4, singular values `[0.35627, 0.20586, 0.17931, 0.07383, 0]`, null dim 2 |
| solutions inside prior box | **53 of 61 starts converged; 44 distinct θ** reproduce the same five moments |
| archived 6-param `best_theta` moments (arithmetic check only) | `[0.7352, 0.6858, 0.8340, 0.1231, 0.6611]` → `max|diff|/τ = 0.42` (inside tolerance) |

**5-parameter null directions at θ\*** (components θ0, θ1, θ2, θ3, θ4; unit norm):

```
v1 = [−0.398, +0.238, +0.886, +0.009, −0.009]    (school-gap slope vs intercept)
v2 = [−0.159, −0.967, +0.190, −0.066, +0.011]    (income slope vs intercept / school gap)
6-parameter null vectors (θ0..θ5) have numerically zero θ5 component (δ pinned by m_own).
```

Interpretation: the moments pin the **cell means**, but the **within-cell income and school-gap gradients**
can be changed against the cell intercepts with no change to any advertised moment. Grade premium θ3 and urban
demand θ4 are close to identified (tiny null components); income and school-gap slopes are not.

**Finite (not merely infinitesimal) non-identifiability:** moving `t = 0.30` along `v1` and re-projecting onto
the moment manifold changes θ by `max|Δθ| = 0.266` while the participation-moment residual stays
`1.1e-16`; the four candidate micro-moments do move (`m_inc_g9: 0.1517 → 0.1814`,
`m_qual_g9: 0.1621 → 0.1973`), so the manifold is real and the micro-moments can in principle separate it.

### 3.3 The composition artifact: "urban−rural gap 0.14" is not a within-grade gap

With zero urban Grade-12 pupils, `m_ur = A − (B + C)/2` where `C = m_g12`. Given the advertised targets the
implied **within-grade** urban−rural gap in G9 is `A − B = 0.3067` (**30.7 pp**) — more than twice 0.14. The
advertised 0.14 is a composition-weighted mixture of the (large) urban−rural difference and the (large)
G12−G9 difference. Any claim about "the urban gap" from this ABC is therefore about a non-clean contrast, on
top of P0-03's empty G12×urban cell and absent school identifiers.

### 3.4 Analytic provider-choice parameter (P0-02)

| check | value |
|---|---|
| δ* = ln(0.32/0.68) | **−0.7537718023763802** |
| `P(own|tutoring) = 1/(1+e^δ*)` | 0.6799999999999999 (error 1.1e-16 vs 0.68) |
| invariants | exactly independent of income, school gap, grade, urban (max deviation 0.0 over 1,000 θ points) |
| archived 7-param δ = −0.8241 | own = 69.51 % → error **+1.51 pp** |
| archived 6-param δ = −0.6682 | own = 66.11 % → error **−1.89 pp** |
| frozen tolerance τ_own | 6.0 pp → both archived estimates **pass tolerance**, masking an exactly solvable parameter |

Consequence: `m_own` is not a moment to be fitted — it is an algebraically pinned parameter. The 6 active
parameters reduce to 5 (θ0–θ4) for participation, with the fitted δ relegated to an exact substitution.

### 3.5 Reduced system and the number of further moments required

After substituting δ: parameters `(θ0..θ4)`, free moments `{m_g9, m_g12, m_ur}` → 3×5 Jacobian rank 3,
null dimension **2**. By rank–nullity **two further independent moments are required**. Null-space loading
`‖Nᵀ r_i‖ / ‖r_i‖` of candidates at θ* (1.0 = fully inside the unidentified subspace):

| candidate extra moment | loading | rank with it alone | null dim |
|---|---|---|---|
| `m_inc_pooled` | 0.970 | 4 | 1 |
| `m_qual_pooled` | 0.954 | 4 | 1 |
| `m_inc_g9` | 0.984 | 4 | 1 |
| `m_inc_g12` | 0.943 | 4 | 1 |
| `m_qual_g9` | 0.993 | 4 | 1 |
| `m_qual_g12` | 0.789 | 4 | 1 |

Any **two** independent such moments give rank 5/5 (null 0), e.g. `m_inc_pooled + m_qual_pooled` (rank 5),
`m_inc_pooled + m_inc_g12` (5), `m_qual_g9 + m_qual_g12` (5), `m_inc_g9 + m_qual_g9` (5). One moment is never
enough; this is the quantitative form of the auditor's "two further independent moments are required".

### 3.6 Paper A's income and within-grade quality micro-moments (independent recomputation)

Paper A's draft README reports ("AUTHOR-REPORTED", no code/results deposited) *"adding income and within-grade
quality micro-moments restores rank 7/7 (condition 43.81)"* from a 7-parameter model. Our independent
recomputation on the frozen 6-active-parameter design with our stated micro-moment definitions:

| model (after δ substitution) | rank across 1,000 points | null dim | cond at θ* |
|---|---|---|---|
| base 3 moments (m_g9, m_g12, m_ur) | 3 | 2 | 3.48 |
| + income pooled | 4 | 1 | 3.91 |
| **+ income pooled + quality pooled** | **5** | **0** | 4.59 |
| + all four grade-specific micro-moments | 5 | 0 | 5.16 |

Unsubstituted 6-parameter model with the five advertised moments **plus** income + quality:
**rank 6/6** (singular values at θ* `[0.4056, 0.3255, 0.2059, 0.1344, 0.1089, 0.0858]`).

**Conclusion:** with one income and one within-grade quality micro-moment the model reaches full local rank
(5/5 substituted, 6/6 unsubstituted). This is **local identification only** — a full-rank Jacobian at a point
implies a local diffeomorphism (inverse-function theorem); no global-injectivity proof is offered or claimed.
It is also a statement about *this* synthetic design, not about real data.

### 3.7 Measurement uncertainty (propagated separately from structural rank)

Using the frozen τ for the three participation moments and an **assumed** 0.03 for each micro-moment:

| τ-scaling | parameter 1σ (θ0, θ1, θ2, θ3, θ4) | rank |
|---|---|---|
| τ | `[0.242, 0.089, 0.303, 0.381, 0.408]` | 5 |
| τ/2 | `[0.121, 0.044, 0.152, 0.191, 0.204]` | 5 |
| 2τ | `[0.484, 0.177, 0.607, 0.763, 0.815]` | 5 |

Tolerances scale parameter uncertainty linearly and **do not change rank**: the advertised 5-moment model has
rank 4 under τ/2, τ and 2τ alike. The `m_own` tolerance is irrelevant once δ is analytic (zero variance). The
τ-based acceptance criterion is therefore the wrong diagnostic for identification — it can pass a parameter
that is exactly computable (δ) while being silent about directions with zero information.

## 4. What the gate brief should say: identified vs not

**Identified by the advertised moments (in this model, at regular interior points):**
* δ = −0.7537718 exactly (from `m_own = 0.68`); equivalently own share 0.68;
* the three cell participation probabilities A = 0.8233 (urban G9), B = 0.5167 (rural G9), C = 0.85 (rural G12),
  equivalently the three independent moments `m_g9, m_g12, m_ur` — and nothing else about participation.
* the four identified linear combinations span rank 4 of 6; grade premium and urban demand are near-identified,
  income and school-gap slopes are not.

**Not identified:**
* two directions (a 2-dimensional manifold) in the 6-parameter model / in the 5 participation parameters.
  Substantively: within-cell **income gradient** and **school-quality gradient**, traded against cell
  intercepts (null vectors in §3.2). The 44 distinct in-box solutions with identical moments quantify this; the
  archived posterior spread along these directions is prior, not likelihood.
* Any claim about **school-level quality remediation** or **urban differences**: the population has no school
  identifiers, `school_gap` is an independent per-pupil `U(0,1)` draw, and the G12×urban cell is empty; the
  "urban−rural gap" is a mixture whose implied within-grade value is 30.7 pp (§3.3).

## 5. Paper A's Jacobian proposition — binding statement

Paper A's identifiability claim (rank 5/7 → 7/7, condition 1.09e13 → 43.81) is **AUTHOR-REPORTED**: no code,
model specification or result JSON was supplied in this repository, and the claim is quarantined as
`AUTHOR-REPORTED` / `PRE-REPAIR`. **Its Jacobian must be computed independently from Paper A's own model and
specification — it MUST NOT be supported by, or cite, the archived ABC outputs** (the bundle's accepted draws
were discarded and the inference is quarantined). Our recomputation here uses the frozen 6-active-parameter
design and explicitly stated candidate micro-moments; it reproduces the *qualitative* proposition ("income +
within-grade quality moments restore full local rank") but its condition numbers (3.48 → 4.59 substituted;
6-parameter singular values 0.086–0.406) are not comparable to the reported 43.81, which cannot be checked.
Paper A may cite this audit only as an independent, local, design-specific recomputation, with that caveat.

## 6. Reproduction

```bash
cd /Users/treymenefee/neon-boot/wt4/auditv2
OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
  /Users/treymenefee/neon-boot/venv/bin/python docs/audit/code/abc_identification_audit.py
# writes /tmp/abc_identification.json and /tmp/abc_identification_tables.md
```

Deterministic (seeds fixed at `20261125`); runs in a few seconds single-process, < 100 MB. The harness
imports only NumPy and nothing from the engine.

**Box reproduction (CPU only; 1 process, `nice -n 10`, BLAS/OMP=1):** deployed read-only from commit
`8281dd9` into `/root/work/contest`; run `2026-11-25T15:02:47+08:00` with `/root/miniconda3/bin/python`
**3.10.8 / NumPy 1.24.1** (below the host's declared NumPy floor — recorded; the script uses only
`np.quantile`, `np.linalg.svd`, `np.linalg.pinv`, `np.unique(axis=0)`) inside the **10-CPU cgroup**
(`cpu.max = 1000000 100000`), `EXIT 0`.

| artifact | sha256 |
|---|---|
| harness `abc_identification_audit.py` | `25da334f90ab9ad8fe494dfc581290b9109ffec56125d2e8f1fc0dfc84e592f6` (identical local and box) |
| box `abc_identification.json` | `33120aab735588c475157479913a14148d729212d4ec9e466dcd16be630dc6f0` |
| box `abc_run_box.log` | `1e0106f65ebb19bba82899fe0b128c50712294282253581d54c35c00079d558e` |
| box `abc_identification_tables.md` | `3c245dc0e6eb43cac7dce8a411f46d4b8eb0f5d3ccfbbad8cdf93aab9132423e` |
| host `abc_run.log` / JSON | `bd02516d…6fc41` / `66bb2648…15808` (byte hashes differ from box only in last-bit SVD/rounding; every headline field agrees — ranks identical, θ* identical to 8 dp, null-space principal-angle deviation ≤ 4.4e-16) |

## 7. Limits and caveats

1. **Population realisation is not deposited.** The archived ABC draws the 630-pupil population from a CUDA
   `torch.Generator` and saves neither the draws nor their hashes; this audit uses a NumPy population with the
   same distributions/design. Identification rank is structural and checked at 1,000 prior-box parameter
   points, so it does not depend on one draw; the exact archived numbers (e.g. θ*, SVs) would shift slightly
   with a different realised population.
2. **Our micro-moment definitions are ours, not Paper A's** (§3.6/§5). A different operationalisation changes
   the rows and hence must be recomputed; the qualitative rank result (2 additional independent moments →
   full local rank) is what this audit establishes for the frozen design.
3. **Local only.** Full-rank Jacobian at a point proves local identification. The 2-dimensional solution
   manifold outside the micro-moment set is demonstrated at finite distance (§3.2); no global injectivity is
   claimed for the augmented model.
4. **Synthetic, degenerate design.** Empty G12×urban cell, no school identifiers, `school_gap ~ U(0,1)` per
   pupil: "school-quality" micro-moments identify a synthetic coefficient, not school quality; "urban gap"
   moments are non-clean contrasts (§3.3). This is P0-03 and it caps what any reparameterisation of this design
   can establish.
5. **Not evidence for or against the archived ABC draws.** The archived `best_theta` values appear only as
   arithmetic checks; the bundle remains quarantined (`AUTHOR-REPORTED` / `PRE-REPAIR` / `UNRESOLVED`).
6. **Compute.** The run is seconds-long and was executed both on the host and on the box with 1 worker; no
   process pool, no GPU, no legacy directories touched.
