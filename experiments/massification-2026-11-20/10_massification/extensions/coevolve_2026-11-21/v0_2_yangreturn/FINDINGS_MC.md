# FINDINGS — v0.2 Yang return-side wiring: parameter Monte Carlo (`SIMULATED`)

**Label: `SIMULATED` / `ILLUSTRATIVE`.** New extension; coevolve v0 and v0.1-YANG stay frozen. Contract:
`PRE_DECLARATIONS.md` sha256 `3c527ce49046a7fb01db797d9fd5271c8ea6c98446027ae1276a2dc231e15da7` (frozen before the
run). No parameter, threshold, bar, draw range or seed changed after any result.

## 0. What the wiring is (return side, not gate incidence)

`C_eff(L,N) = C_L · (1 + α·g(N))`, with YANG `D(N)=b·ln N + (anchorD − b·ln 1e6)`,
`g(N)=clip((D−D_50k)/(D_2m−D_50k),0,1)`, `α = 1.0` baseline and a drawn `premium_mult U[0.85,1.15]`. City size N
enters **only** through `g(N)`; household/cohort structure, geography, gates, supply and prices are v0's. This is a
**return-side** wiring: it scales the credential/option value in the household decision, not the number of
credential-required places. It **cannot** test gate scarcity; v0.1 showed that reading is inert by construction
(0/447,098 applicants lacked a required credential). Designs: `none` (α·g=0), `yang` (fixed g(N)), `yang_endog`
(one-year-lag bounded response of the credential factor to applicants per gated place: step ±0.05, bounds
[0.25,1.50], mean applicants/place over the selective and university gates).

## 1. Identity guard and determinism

- **Identity guard PASS:** with default declarations and α·g=0, the copied simulator reproduces the frozen v0
  **baseline** run (arm `baseline`, seed 20261121) **byte-identically** on panel and pupil-year tables.
- **Pre-shock:** the wiring is a standing parameter on from t=0, so cross-design y=20–22 equality is not implied;
  the declared identity guard replaces it (statement in the predeclaration).
- **Determinism:** two complete MC runs (150 draws, 3,600 runs) produce **byte-identical** `mc_results.json` and
  `mc_per_draw.csv`.
- **Runtime:** **1,115 s** (18.6 min) with 6 worker processes, inside the declared 45-minute limit; the 150-draw
  design was **not** reduced.

## 2. (a) Robust-ACTIVE — the headline

**`yang`: 100% of the 150 draws are robustly ACTIVE** (completion gap ≥0.5 pp at ≥3 of the 4 sizes); **`yang_endog`:
98.0%**. **Inert share (yang): 0.0%.** The return-side margin is **active in every declared draw**, unlike the
gate-incidence reading which was inert by construction.

## 3. (b) Gap distributions by size (completion gap, pp; over draws, seed-mean)

| size | `yang` median | p5 | p95 | `yang_endog` median |
|---:|---:|---:|---:|---:|
| 200k | **+2.927** | +1.331 | +5.930 | +3.783 |
| 500k | **+4.490** | +2.029 | +7.196 | +5.911 |
| 1m | **+5.672** | +2.784 | +7.827 | +7.439 |
| 2m | **+6.674** | +3.610 | +9.418 | +8.576 |

**Pooled (4 sizes, per draw):** `yang` completion gap mean **+4.956**, median +5.109, p5 **+2.468**, p95 **+7.192**
(range +1.554 to +7.930). `yang_endog` pooled mean **+6.125**, median +6.519, p5 +1.802, p95 +9.021. **Leaving gap**
(pp): `yang` mean **−8.633** (median −8.602; p5 −15.259; p95 −2.447) — the wiring reduces early leaving in every
size; `yang_endog` reduces it further.
**Size pattern:** the gap rises monotonically with city size (2.9 → 6.7 pp), as `g(N)` does.

## 4. (c) Top-3 load-bearing parameters (Spearman on the pooled completion gap; R² share)

| rank | parameter | ρ (completion) | ρ (leaving) | univariate R² | variance share |
|---|---|---:|---:|---:|---:|
| 1 | **`beta_mult`** (future/option weight) | **+0.722** | +0.844 | **0.547** | **65.3%** |
| 2 | **`child_wage_mult`** (alternative work return) | **−0.324** | −0.468 | 0.123 | 14.7% |
| 3 | **`premium_mult`** (the Yang/wage analogue on `C_eff`) | **+0.249** | −0.146 | 0.051 | 6.0% |
Next: mapping variant index (+0.195, 5.4%), convex scale (−0.184, 4.6%), travel (−0.120, 2.1%), Yang slope
**+0.097** (1.7%), anchor **+0.028** (0.2%). **Yang's own slope/anchor remain nearly inert; the load is carried by how
much families weight the future and the alternative wage, with the premium multiplier third.** This mirrors D178
(the Yang-toy margin is a return-premium object) and adds the coevolution-specific finding that the **future/option
weight dominates**.

## 5. (d) Boundary contingency — the Yang-toy wage-premium boundary does **NOT** reproduce

Yang-toy inert definition (low premium multiplier + high alternative return) mapped to this MC as
**`premium_mult ≤ 0.95` AND `child_wage_mult ≥ 1.05`** (declared proxy). Contingency (coevolve inert = not robustly
ACTIVE):

| | coevolve ACTIVE | coevolve INERT |
|---|---:|---:|
| **Yang-toy inert draws** (n=14) | **14** | **0** |
| Yang-toy active draws (n=136) | 136 | 0 |

**Every Yang-toy-inert draw is coevolve-ACTIVE**, and no draw is coevolve-inert. So the **wage-premium boundary
does not reproduce** in the return-side coevolution wiring: at the coevolution scale the margin survives the same
premium/wage draws that made the Yang toy inert. (The Yang toy's inertness came from the factory-vs-formal wage
comparison; in coevolve the credential value enters a broader household value with fees, travel, option value and
a different wage structure, so the same draws remain active.)

## 6. (e) Coexistence metrics by design/size (mean over scored years 6–17)

| metric | none (all sizes) | `yang` 200k | `yang` 1m | `yang` 2m |
|---|---:|---:|---:|---:|
| unused accessible share | 0.266 | **0.218** | — | **0.171** |
| qualified per selective place (queue ratio) | 5.422 | **5.887** | — | **6.843** |
| gate-tutoring household share | 0.208 | **0.204** | — | **0.189** |

`none` is identical across sizes by construction (N enters only through `g`), which is also a live check of the
declared wiring. Under `yang`, as N rises the **unused accessible share falls** (0.266 → 0.171), the **queue ratio
rises** (5.42 → 6.84) and the **gate-tutoring household share falls modestly** (0.208 → 0.189): the return-side margin
pulls more families into the pipeline (fewer unused places) and intensifies the selective gate, without raising the
*share* of applicants buying gate tutoring.

## 7. What this does and does not show

- The **return-side Yang wiring is strongly active** in this toy: 100% of draws meet the bar, with completion gaps
  of ~3–7 pp rising in city size and early leaving falling ~9 pp.
- It **cannot** speak to gate scarcity or credential requirements at places; it only moves the return margin. The
  v0.1 audit remains the statement that the gate-incidence reading is inert by construction.
- **No observed data, no country claims, no causal or direction claims; no tuning.** The gap is a model-internal
  `SIMULATED` quantity; the MC is over declared plausibility ranges, not a posterior.

## 8. Files

`results/mc_results.json`, `results/mc_per_draw.csv`, `results/mc_console.log`; `code/coevolve_v0_2_yangreturn.py`
(copied v0 + wiring), `code/mc_yangreturn.py`; `PRE_DECLARATIONS.md` (+ `.sha256`). Two complete runs byte-identical.
