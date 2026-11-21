# MC PRE-DECLARATIONS — parameter Monte Carlo for the Yang-mapped factory toy (BEFORE THE MC RUN)

**Status: ILLUSTRATIVE / EXPLORATORY toy. Not evidence; no calibration; no claims about any country.**
Written **before** the Monte Carlo run, per the Lead's instruction (2026-11-21). The v2 design
(`PRE_DECLARATIONS.md`, frozen) is unchanged: same toy, same outcomes, same falsifier. This document only declares
the **parameter draws**, the **MC design**, and the **MC analysis rules**.

## 0. What this MC is — and is not

The v2 grid is **seed Monte Carlo** (many random arrivals, one parameter set); with 200 seeds × 23 scored years ×
64 arrivals per year, sampling noise is tiny. **The material uncertainty is in the declared parameters.** This MC is
therefore a **parameter Monte Carlo with paired seeds (common random numbers)** plus a descriptive sensitivity read:
it asks how often the predeclared Yang-activity bar is met across plausible declaration space, and which parameters
carry the gap. It is **not** an estimate of any real quantity and **not** a Bayesian posterior.

**CRN (common random numbers).** The toy's arrival noises depend only on `(seed, cohort, individual, year, channel)` —
never on the design or the parameter draw. The same seed therefore gives the **same arrivals across designs** (paired
designs) and the same arrivals across draws; parameter draws move the decision rules, not the noise. This is the
declared pairing structure.

## 1. Parameter draws (uniform, independent unless stated)

| parameter | symbol in code | draw |
|---|---|---|
| Yang slope | `b` | **Uniform[100, 160]** (paper 128) |
| Yang anchor | `anchorD = D(1e6)` | **Uniform[400, 600]** (v2 declares 500) |
| future weight | `beta` | **Uniform[0.3, 0.7]** (v2 0.5) |
| p_dip intercept | `pDipInt` | **Uniform[0.60, 0.80]** (v2 0.70) |
| p_dip skill slope | `pDipSlope` | **Uniform[0.10, 0.30]** (v2 0.20) |
| rural travel base | `travelBase` | **Uniform[0.05, 0.20]** (v2 0.10) |
| rural travel spread | `travelSpread` | **Uniform[0.15, 0.35]** (v2 0.25) |
| factory wage multiplier | `wageFactory` × | **Uniform[0.85, 1.15]** × 2.3 |
| formal wage multiplier | `wageFormal` × | **Uniform[0.85, 1.15]** × 2.0 |
| informal wage multiplier | `wageInformal` × | **Uniform[0.85, 1.15]** × 1.4 |
| gate mapping variant | `gateMapping` | **equal probability**: (i) linear `g=(D−D_lo)/(D_hi−D_lo)`; (ii) proportional `g=D/D_hi`; (iii) convex `g=1−exp(−(D−D_lo)/scale)` with `scale` **Uniform[100, 400]** |
| endog threshold high | `endogHigh` | **Uniform[2, 4]** (v2 3) |
| endog threshold low | `endogLow` | **Uniform[0.5, 1.5]** (v2 1) |

`b` and `anchorD` jointly determine `D(N)=b·ln N + (anchorD − b·ln 1e6)`; the gate share is computed per the drawn
mapping. The study value uses the drawn `gs` (city-level gate share) as in v2 — declared.

## 2. MC design (frozen)

- **1,000 parameter draws.**
- **Paired seeds {0, 1, 2}** per draw (same arrival noises across designs for a given draw/seed).
- **City sizes {50k, 200k, 500k, 1m, 2m}** (the v2 sizes minus 100k; the bar uses 5 sizes as the Lead specified).
- **Designs {none, yang, yang_endog}**.
- **Fixed RNG seed for the parameter draws: 20261121** (one numpy-free JS PRNG stream; the same stream on every run).
- **Total runs:** 1,000 × 3 × 5 × 3 = **45,000** toy runs; target runtime **< 10 minutes** (v2.1 grid is ~12.7 s for
  4,800 runs; expected MC ~2–4 minutes).
- **Determinism:** two complete MC runs must produce **byte-identical** result files.
- **Pre-shock check:** for each draw × seed × size, the y=20–22 means must be identical across the three designs
  (design affects selection only from y=23); the harness asserts this and the MC run fails `PRE-SHOCK-MISMATCH` if not.

## 3. Outcomes (per draw)

For each draw `d`, seed `s`, size `N`:
- `completion_gap(d,s,N) = completion_yang(d,s,N) − completion_none(d,s,N)`
- `leaving_gap(d,s,N) = leaving_yang(d,s,N) − leaving_none(d,s,N)`
and the same for `yang_endog`.
Per draw: the **mean over seeds** at each size, then the **mean over the 5 sizes** (`gap_bar`), and the
**distribution over draws** (mean, p5, p95) of the size-mean gaps. (Declared pooling: seeds are paired within a
draw; sizes are treated as equally weighted cells.)

## 4. Analysis rules (frozen)

1. **Robust-ACTIVE share.** For a draw, a size **counts** if the predeclared v2 bar is met there:
   `|completion_gap| ≥ 0.5 pp OR |leaving_gap| ≥ 0.5 pp` (the v2 falsifier's outcome pair), using the
   seed-mean gap at that size. A draw is **robustly ACTIVE** if **≥ 3 of the 5 sizes** count. The reported headline
   is the **share of draws robustly ACTIVE**, for `yang` and for `yang_endog` separately.
2. **Distribution.** Median and p5/p95 (over draws) of the size-mean `completion_gap` and `leaving_gap`, by size and
   pooled, for `yang` and `yang_endog`.
3. **Sensitivity (descriptive).** Spearman rank correlation between `gap_bar` (per draw, mean over seeds and sizes;
   primary = `completion_gap`, secondary = `leaving_gap`) and each drawn parameter (with `gateMapping` mapped to its
   variant index; `convexScale` only defined for variant (iii), reported separately). **Top-3 load-bearing parameters**
   = the three largest |Spearman ρ|, reported with ρ and draw range.
4. **Variance decomposition (descriptive).** For each drawn parameter, a univariate OLS of `gap_bar` on the
   standardized parameter; report **R²**; the **share** is the parameter's R² divided by the sum of all univariate R²
   (declared as a simple, non-causal decomposition; parameters are independent by construction, but univariate R²
   can double-count joint variation). Report the top five shares.
5. **Inertion.** A draw is **`YANG-INERT-DRAW`** if **0 of 5 sizes** count. Report the count/share and the drawn
   parameter values of the first five inert draws (descriptive). (The v2 grid's own bar is checked separately in
   `results/grid_200seeds.csv`.)
6. **Labels.** Every number `SIMULATED`/`DERIVED`; the toy is `ILLUSTRATIVE`; no country claims, no causal or
   direction claims; no tuning after results; failures reported as failures.

## 5. What this MC cannot claim

- It does not estimate the Yang law, nor any city's occupational variety; the law is a declared mapping.
- Draws are **declared plausibility ranges**, not a posterior; the uniform/independent choices are conventions.
- The toy has no capacity, quality, commuting network, firm entry/exit, learning, or real wages; its "pp" units are a
  toy index, not measured percentage points.
- A robust-ACTIVE share is a statement about **this toy's declaration space**, not about the world.
