# CONTEST_MATH_APPROX_ERROR — legacy `1−exp(−λx^r)` vs exact Plackett–Luce

**Lane:** `contest-math` (Gate 1c, task-4). **Date:** 2026-11-25.
**Branch:** `research/contest-audit-v2-2026-11-25`. **Reference module:** `engine/eduengine/contest_math.py`
(commit `1a6f3d5`, validated in `docs/audit/CONTEST_MATH_VALIDATION.md`).
**Contract:** `docs/audit/ENGINE_INTERFACE_CONTRACT.md` v1.0 §1.3, D2; findings D2/§5.4 of the review.
**Evidence class:** deterministic numerical analysis (exact reference probabilities + seeded validation MC) —
*not* an empirical claim.

**Purpose.** The legacy engine prices a contest gate with an *expected-probability approximation*
`P̂ = 1 − exp(−λ x^r)` while the gate *realizes* admission with Gumbel-max top-K Plackett–Luce over the same
`x_eff` (review finding D2, `core.py` L178 vs L406–426). This document quantifies, on a reproducible grid,
where that approximation is acceptable (< 2 pp individual error) and where it is misleading, to feed the
expected-vs-realized reconciliation and the review's fix option.

---

## 1. The two objects

**Legacy expected (belief) probability** — `core.py` L178 (pre-repair), where `x = x_eff` and `r = r_c`:

```python
P_hat = 1.0 - np.exp(-np.clip(self.lam_contest[m] * (x ** r), 0.0, 50.0))
```

**λ-solving procedure** — exactly the engine's bisection, `core.py` L416–426 (reproduced verbatim in the
analysis so the table is reproducible; `seats = max(round(share·N), 1)`, `len(ci)` = number of candidates):

```python
target_s = min(seats / max(len(ci), 1), 0.99)
w  = x_eff ** r                       # candidate weights
lo, hi = 1e-12, 50.0 / max(float(np.percentile(w, 10)), 1e-9)
for _ in range(30):
    mid = 0.5 * (lo + hi)
    if float(np.mean(1.0 - np.exp(-np.clip(mid * w, 0.0, 50.0)))) < target_s:
        lo = mid
    else:
        hi = mid
lam_new = 0.5 * (lo + hi)
self.lam_contest[m] = 0.7 * self.lam_contest[m] + 0.3 * lam_new     # EMA across years
```

λ is the fixed point of that EMA at a stationary candidate pool; at that point **the pool-mean of `P̂` equals
`seats/n` by construction**. (The EMA transient — belief lag — is an engine-core question, not analysed here.)

**Truth** — exact top-K PL individual win probability from `pl_win_probs_exact` (subset DP, machine precision
for n ≤ 20; validated against `n!` brute force and against 400k MC in the companion document).

## 2. Grid design (reproducible)

Reference candidate pool, n = 20 candidates, arithmetic mean effort = 1 (effort is scale-free: PL
probabilities depend only on relative weights, and λ is re-solved after any rescale):

| component | values |
|---|---|
| 9 target effort levels (the required 0.2x–5x grid) | 0.2, 0.35, 0.5, 0.75, 1.0, 1.5, 2.0, 3.0, 5.0 (sum 14.3, min 0.2, max 5) |
| 11 fillers (sum 5.7; one at 0.2, ten log-spaced 0.25→1.2 scaled to sum 5.5) | 0.2, 0.222, 0.264, 0.315, 0.375, 0.446, 0.531, 0.632, 0.752, 0.896, 1.066 |

The pool is right-skewed (a minority of heavy investors drags the mean up while the bulk sits at 0.2x–1.1x),
which is the politically relevant shape for a positional contest; **pool composition sensitivity is reported in
§3.6**. Age-ability `b_i` and prep effort `e_i` enter the contest only through the scalar
`x_eff = x0·max(L,0.1)/ends[m] + alpha·prep`; therefore the "effort level" and "ability level" slices are the
same one-dimensional slice (a child with the same `x_eff` has the same true and approximate probability
regardless of whether `x_eff` came from ability or effort). The quintile slice is over the distribution of
`x_eff`.

Grid: seat scarcity `seats/n ∈ {0.05, 0.2, 0.5, 0.9}` → `seats = round(s·n)` = {1, 4, 10, 18} (exact in this
pool); contest discrimination `r ∈ {1.0, 1.5, 2.5}`; weights `w = x^r`; bias = `P̂ − P_exact` in percentage
points (positive = engine over-states the candidate's chance). Analysis truth cross-checked against
`pl_win_probs_mc(n_mc=200 000)`: max |exact−mc| = 0.0010–0.0035, z ≤ 3.1 for all 12 cells.

## 3. Results

### 3.1 Cell summary (pp)

`max|err| bulk` is over effort 0.5x–2x; `max|err| tail` over 0.2x–0.35x and 3x–5x.

| seats/n | r | seats | λ (fixed point) | max\|err\| all levels | max\|err\| bulk 0.5–2x | max\|err\| tail | mean bias |
|---|---|---|---|---|---|---|---|
| 0.05 | 1.0 | 1 | 0.0530 | 1.71 | 0.17 | 1.71 | −0.13 |
| 0.05 | 1.5 | 1 | 0.0402 | **3.92** | 0.60 | 3.92 | −0.19 |
| 0.05 | 2.5 | 1 | 0.0155 | **7.74** | 1.76 | 7.74 | −0.13 |
| 0.20 | 1.0 | 4 | 0.2579 | 1.20 | 0.69 | 1.20 | −0.23 |
| 0.20 | 1.5 | 4 | 0.2392 | 1.65 | 1.65 | 1.57 | −0.22 |
| 0.20 | 2.5 | 4 | 0.2001 | **3.09** | **3.09** | 1.53 | −0.26 |
| 0.50 | 1.0 | 10 | 1.0332 | 0.74 | 0.56 | 0.74 | +0.07 |
| 0.50 | 1.5 | 10 | 1.3141 | 0.87 | 0.87 | 0.77 | +0.10 |
| 0.50 | 2.5 | 10 | 2.1852 | 1.34 | 1.34 | 1.34 | +0.03 |
| 0.90 | 1.0 | 18 | 5.3725 | 0.55 | 0.55 | 0.71 | +0.05 |
| 0.90 | 1.5 | 18 | 9.7542 | 0.67 | 0.67 | 1.02 | +0.05 |
| 0.90 | 2.5 | 18 | 36.3875 | 0.51 | 0.51 | 1.69 | +0.11 |

**Aggregate identity.** `Σ_i P̂_i = seats` (λ bisection) and `Σ_i P_exact_i = seats` (exact PL), so the mean
bias over the pool is 0 to ≤ 3.6e-3 (roundoff of the bisection) in every cell. The approximation is therefore a
**redistribution of individual probability, not a level shift** — the expected-vs-realized *aggregate* check
cannot see it (see §5).

### 3.2 Bias by effort level (pp) — the required 0.2x–5x slice

**seats/n = 0.05**

| r | 0.2x | 0.35x | 0.5x | 0.75x | 1x | 1.5x | 2x | 3x | 5x | max |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.0 | +0.1 | +0.1 | +0.1 | +0.1 | +0.2 | +0.1 | +0.1 | −0.3 | −1.7 | 1.7 |
| 1.5 | +0.0 | +0.1 | +0.1 | +0.2 | +0.4 | +0.5 | +0.6 | +0.2 | **−3.9** | 3.9 |
| 2.5 | +0.0 | +0.0 | +0.1 | +0.2 | +0.4 | +0.9 | +1.8 | +3.2 | **−7.7** | 7.7 |

**seats/n = 0.20**

| r | 0.2x | 0.35x | 0.5x | 0.75x | 1x | 1.5x | 2x | 3x | 5x | max |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.0 | +0.2 | +0.2 | +0.2 | +0.2 | +0.1 | −0.3 | −0.7 | −1.2 | −0.9 | 1.2 |
| 1.5 | +0.1 | +0.2 | +0.3 | +0.3 | +0.1 | −0.7 | −1.6 | −1.6 | +1.1 | 1.6 |
| 2.5 | +0.0 | +0.1 | +0.2 | +0.5 | +0.4 | **−2.3** | **−3.1** | +1.5 | +0.2 | 3.1 |

**seats/n = 0.50**

| r | 0.2x | 0.35x | 0.5x | 0.75x | 1x | 1.5x | 2x | 3x | 5x | max |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.0 | +0.3 | +0.2 | −0.1 | −0.4 | −0.6 | −0.3 | +0.2 | +0.7 | +0.5 | 0.7 |
| 1.5 | +0.3 | +0.3 | −0.1 | −0.7 | −0.7 | +0.5 | +0.9 | +0.3 | +0.0 | 0.9 |
| 2.5 | +0.2 | +0.5 | +0.1 | −1.3 | +0.2 | +0.6 | +0.0 | +0.0 | +0.0 | 1.3 |

**seats/n = 0.90**

| r | 0.2x | 0.35x | 0.5x | 0.75x | 1x | 1.5x | 2x | 3x | 5x | max |
|---|---|---|---|---|---|---|---|---|---|---|
| 1.0 | −0.4 | −0.5 | +0.2 | +0.5 | +0.4 | +0.1 | +0.0 | +0.0 | +0.0 | 0.5 |
| 1.5 | −0.3 | −0.4 | +0.7 | +0.4 | +0.1 | +0.0 | +0.0 | +0.0 | +0.0 | 0.7 |
| 2.5 | +0.1 | +0.4 | +0.5 | +0.0 | +0.0 | +0.0 | +0.0 | −0.0 | −0.0 | 0.5 |

Worked example, `seats/n=0.05, r=1.5`: engine says 36.2 % for a 5x-effort candidate where the exact PL
probability is 40.1 % (under-stated by 3.9 pp); at `r=2.5` the same candidate is 58.1 % vs 65.8 % exact
(under-stated by 7.7 pp), while a 3x candidate is over-stated by 3.2 pp (21.5 % vs 18.3 %).

### 3.3 Quintile slices of the contest-input distribution (bias pp)

| seats/n | r | Q1 (0.2–0.5x) | Q2 (0.5–0.75x) | Q3 (0.75–1.2x) | Q4 (1.2–3x) | Q5 (3–5x) |
|---|---|---|---|---|---|---|
| 0.05 | 1.0 | +0.1 | +0.1 | +0.1 | +0.2 | −0.4 |
| 0.05 | 1.5 | +0.0 | +0.1 | +0.2 | +0.3 | −0.6 |
| 0.05 | 2.5 | +0.0 | +0.0 | +0.1 | +0.3 | −0.5 |
| 0.20 | 1.0 | +0.2 | +0.2 | +0.2 | +0.1 | −0.8 |
| 0.20 | 1.5 | +0.1 | +0.2 | +0.3 | +0.1 | −0.7 |
| 0.20 | 2.5 | +0.0 | +0.1 | +0.3 | +0.4 | −0.9 |
| 0.50 | 1.0 | +0.3 | +0.1 | −0.2 | −0.5 | +0.3 |
| 0.50 | 1.5 | +0.3 | +0.3 | −0.3 | −0.7 | +0.4 |
| 0.50 | 2.5 | +0.2 | +0.4 | −0.5 | −0.3 | +0.2 |
| 0.90 | 1.0 | −0.5 | −0.4 | +0.4 | +0.4 | +0.0 |
| 0.90 | 1.5 | −0.6 | −0.2 | +0.6 | +0.2 | +0.0 |
| 0.90 | 2.5 | −0.6 | +0.4 | +0.2 | +0.0 | +0.0 |

(The Q5 mean is diluted because quintiles average four candidates each; the per-level tail values in §3.2 are
the policy-relevant ones.)

### 3.4 Effort-return gradient bias — `dP/d ln x` in pp per ln unit (0.5x → 2x)

This is the object that drives the tutoring first-order condition (`dV·P̂` priced from the belief formula):

| seats/n | r | gradient bias |
|---|---|---|
| 0.05 | 1.0 | −0.04 |
| 0.05 | 1.5 | +0.33 |
| 0.05 | 2.5 | +1.22 |
| 0.20 | 1.0 | −0.67 |
| 0.20 | 1.5 | −1.37 |
| 0.20 | 2.5 | −2.40 |
| 0.50 | 1.0 | +0.21 |
| 0.50 | 1.5 | +0.67 |
| 0.50 | 2.5 | −0.05 |
| 0.90 | 1.0 | −0.13 |
| 0.90 | 1.5 | −0.48 |
| 0.90 | 2.5 | −0.37 |

At 20 % seat scarcity and r=2.5 the engine under-states the marginal return to contest effort in the
0.5x–2x range by 2.4 pp per ln unit (≈ 28 % of the exact gradient, which is ~8.6 pp/ln): it under-prices
tutoring at the intensive margin *and* under-states the top-tail level (§3.2), i.e. both margins of the
positional race are compressed relative to true PL.

### 3.5 The engine's actual gate configurations (same reference pool)

Share/r from the HK/KR scenario (`papers/shadow-education-contest/code/run_hk_korea_comparative.py`
L84, L115–116): HK zhongkao `share=0.23, r=1.5`; KR G9 `share=0.35, r=1.6`; KR G12 `share=0.12, r=1.6`.

| gate | seats in pool | λ | max\|err\| | bias 0.2x | bias 1x | bias 5x |
|---|---|---|---|---|---|---|
| HK zhongkao (share 0.23) | 5 | 0.3436 | **1.61** | +0.1 | −0.2 | +1.3 |
| KR G9 elite (share 0.35) | 7 | 0.6435 | **1.12** | +0.2 | −0.8 | +0.2 |
| KR G12 gate (share 0.12) | 2 | 0.0860 | **2.78** | +0.1 | +0.5 | −2.8 |

The HK and KR-G9 gates are inside the 2 pp acceptance band at every effort level on this pool; the KR G12
gate is acceptable below 2x effort (≤ 0.5 pp) but mis-states a 5x-effort candidate by −2.8 pp (under-states
the top of the race).

### 3.6 Pool-composition robustness (engine cohort scale, n = 400)

Pool: lognormal effort σ_log = 0.7 clipped to [0.2, 5] × mean, seats = round(s·400) = {20, 80, 200, 360};
truth by Rao-Blackwellised MC (conditional on the seats-th best pool score, exact given the draw; SE ≤ 0.04 pp).

| seats/n | r | seats | max\|err\| | mean bias |
|---|---|---|---|---|
| 0.05 | 1.0 | 20 | 0.15 | +0.03 |
| 0.05 | 1.5 | 20 | 0.44 | +0.08 |
| 0.05 | 2.5 | 20 | **1.42** | +0.22 |
| 0.20 | 1.0 | 80 | 0.34 | +0.11 |
| 0.20 | 1.5 | 80 | 0.39 | +0.14 |
| 0.20 | 2.5 | 80 | 0.42 | +0.12 |
| 0.50 | 1.0 | 200 | 0.21 | +0.12 |
| 0.50 | 1.5 | 200 | 0.24 | +0.11 |
| 0.50 | 2.5 | 200 | 0.27 | +0.09 |
| 0.90 | 1.0 | 360 | 0.34 | +0.16 |
| 0.90 | 1.5 | 360 | 0.45 | +0.16 |
| 0.90 | 2.5 | 360 | 0.53 | +0.13 |

At engine cohort scale every cell is inside 2 pp (worst 1.42 pp, in the 5x tail of the most scarce and most
discriminatory contest) — **but the sign flips to a small over-statement** there: with a dense high-effort
pool the true win probability of a 5x candidate is lower, so `P̂` over-states it. The sign of the tail error is
therefore pool-composition dependent; its magnitude is bounded by the pool's density near the seat margin.

## 4. Verdict — acceptable vs misleading

Acceptance rule used here (as specified): individual error < 2 pp acceptable, ≥ 2 pp misleading.

**Acceptable (< 2 pp):**
* every cell with `seats/n ≥ 0.5` (max 1.69 pp, the bulk < 1.4 pp);
* every cell with `r = 1.0` (max 1.71 pp);
* the bulk 0.5x–2x effort range at *any* scarcity/r in the exact n=20 panel (max 1.76 pp);
* the engine's HK zhongkao (1.61 pp) and KR G9 (1.12 pp) configurations at all effort levels;
* at engine cohort scale (n=400) **all** cells (max 1.42 pp).

**Misleading (≥ 2 pp, up to 7.7 pp):**
* scarce seats (`seats/n ≤ 0.05`) with `r ≥ 1.5`, concentrated in the **top effort tail**: a 5x-effort
  candidate's true PL win probability is under-stated by 3.9 pp (r=1.5) to 7.7 pp (r=2.5);
* `seats/n = 0.20` with `r = 2.5`: the 1.5x–2x **bulk** band is under-stated by 2.3–3.1 pp in the sparse
  20-candidate pool (this shrinks to 0.4 pp at n=400, so treat it as a small-pool sensitivity, not a universal
   error);
* the engine's KR G12 gate (share 0.12, r=1.6) at ≥ 4x effort: −2.8 pp at 5x.

**Direction.** The exponential saturates earlier than exact PL in the upper tail of a *sparse, strongly
discriminating* candidate pool, so it **under-states elite contest returns** (and over-states mid-high effort
at 20 % scarcity / r=2.5 in a small pool). At engine cohort scale the residual error is a small over-statement
instead. Either way it is not a random perturbation: it is a systematic re-shaping of the effort-return curve
(gradient bias −2.4 pp/ln at the worst cell), which is exactly the object that determines tutoring demand.

## 5. Implications for the expected-vs-realized reconciliation and the fix

1. **Aggregate reconciliation is blind to D2.** Because λ is solved so that the pool mean of `P̂` equals
   `seats/n` (and exact PL also sums to `seats`), any check of the form
   `|admit_rate − mean P̂| within 4 seed-SE` passes under *both* the legacy formula and exact PL. Such a check
   cannot detect the individual-level distortion documented here; the reconciliation must compare the
   *distribution* (e.g. by effort/ability quintile, §3.3) or the individual predicted-vs-realized frequencies,
   not just the mean.
2. **Fix option (review §D2).** Replace the belief formula and the gate's expected probabilities with the one
   contract function `pl_win_probs(w, seats_eff, method='auto')` — exact DP (n≤20) or deterministic
   quadrature above, with `ΣP = seats_eff`. That removes the approximation error in this table by construction:
   expected and realized probabilities then differ only by Monte-Carlo/finite-cohort sampling, not by
   functional form.
3. **Transitional reading of legacy results.** For any pre-repair result that depends on the belief formula,
   the error map is: harmless at moderate/abundant seats and r≈1; at scarce seats with r≥1.5 the model
   under-prices the top of the positional race by up to ~4–8 pp per candidate (small/sparse pools) and
   compresses the effort gradient; at cohort scale the same gates are within ~1.5 pp with the opposite sign.
   Report which regime a quoted result lives in before comparing it to a repaired run.
4. **Sensitivity choice for the canonical spec.** Keep the *default* as the exact/auto PL object. If a legacy
   arm is retained for comparison, it must carry this table as its sensitivity bound, and the canonical spec
   should report the contest-input distribution (the pool composition) alongside any expected-vs-realized
   statistic, because both the magnitude *and the sign* of the approximation error depend on it.

## 6. Reproduce

```bash
cd /Users/treymenefee/neon-boot/wt4/auditv2
export OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1
export PYTHONPATH="$PWD/engine"
/Users/treymenefee/neon-boot/venv/bin/python /tmp/contest_math_analysis.py   # analysis driver used for this table
# truth: pl_win_probs_exact(w, seats) from engine/eduengine/contest_math.py @ 1a6f3d5
# lambda: bisection reproduced verbatim from core.py L416-426 (snippet in §1)
```

Seeds are fixed (`RNG_SEED = 20261125`); exact truth has no sampling error; the n=400 robustness panel is
MC with its SE reported (≤ 0.04 pp). Analysis ran locally on the host (no box compute), so no capacity caveat.

**Limits.** The exact n=20 panel is the largest exact pool; §3.6 bounds the pool-size/composition sensitivity
at engine cohort scale. λ is the stationary EMA fixed point (transient belief lag is not analysed here). All
bias numbers are in percentage points of individual win probability, not of admission-rate aggregates.

Companion document: `docs/audit/CONTEST_MATH_VALIDATION.md` (module validation, 68 tests, accuracy/runtime).
