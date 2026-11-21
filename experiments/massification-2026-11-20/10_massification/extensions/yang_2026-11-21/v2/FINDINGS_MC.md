# FINDINGS — v2.1 grid (200 seeds) + parameter Monte Carlo (1,000 draws)

**Status: `ILLUSTRATIVE` / `EXPLORATORY` / `SIMULATED`. Not evidence; no calibration; no claim about any country.**
Contract: `PRE_DECLARATIONS.md` (v2 design, frozen) + `MC_PRE_DECLARATIONS.md` (MC design, sha256
`6f9d8c35cb3c4786494c43fa1a1eb834259e71149fe87ffe411ab5d13f19fc32`, frozen before the MC run). No parameter,
threshold or analysis rule was changed after any result.

## 0. What was finished before the MC (the Lead's cleanups)

`code/pathways_yang.cjs` (v2.1; the Lead's working copy preserved as `code/pathways_yang.orig_leadrun.cjs`):
the ambiguous `formal()` helper replaced by an **explicit classification block** (`wage===workValue → factory; else
if age≥18 && alternative===FORMAL && workValue===FORMAL → formal; else if alternative===INFORMAL &&
workValue===INFORMAL → informal; else farm`); **`unfilled = POSTS − factoryJobs`** fixed; a **pre-shock y=20–22
match check** printed in grid mode (all designs must agree before the design acts); grid output saved; two runs
byte-identical. No parameter or threshold changed.

## 1. Deterministic grid at 200 seeds (`results/grid_200seeds.csv`, console log)

- 6 city sizes × 4 designs × 200 seeds = 4,800 runs, **12.7 s**; **pre-shock match PASS** (y=20–22 identical across
  designs at every size); **two runs byte-identical**.
- Gate share `g(N)` = 0 at 50k → 1 at 2m; `q(yang)` = 0/2/5/7/10/12 across the six sizes (the Lead's 20-seed numbers
  were 0/2/5/7/10/12 as well; gaps shift slightly with 200 seeds — documented, no re-tuning).
- **Yang vs none, mean secondary completion gap** (pp, 200 seeds): 50k **0.000**, 100k **+0.005**, 200k **+0.192**,
  500k **+0.531**, 1m **+1.226**, 2m **+1.652**; leaving gaps 0.000 / +0.010 / +0.333 / +0.901 / +1.976 / +2.644.
- **Predeclared v2 falsifier: `ACTIVE`** — the ≥0.5 pp bar is met at **3 of 6 sizes** (500k +0.531, 1m +1.226,
  2m +1.652; the leaving criterion alone would add none). 500k is marginal (0.531 vs 0.5).
- `yang_endog` (q rises/falls with applicants/post) raises completion and leaving at **every** size, including 50k
  (q ≈ 6.9 there despite `g=0`), i.e. the endog rule can manufacture gate pressure where the Yang map is flat.

## 2. Parameter Monte Carlo — (a)–(e) as requested

**Design (frozen):** 1,000 parameter draws × paired seeds {0,1,2} × sizes {50k, 200k, 500k, 1m, 2m} × designs
{none, yang, yang_endog} = **45,000 runs**; draw RNG seed 20261121; common random numbers (same arrival noises
across designs and draws); pre-shock check per draw/seed/size **PASS (0 failures)**; two complete runs
**byte-identical** (`mc_results.json` and `mc_per_draw.csv`).

### (a) Robust-ACTIVE share — the headline
**`yang`: 68.3% of draws** meet the predeclared ≥0.5 pp bar at **≥3 of 5 sizes**; **`yang_endog`: 82.3%**.
**Inert-draw share (`YANG-INERT-DRAW`, 0 of 5 sizes): 18.1%.** So the Yang gate margin is **robustly active in the
majority of the declared declaration space**, but **not universal**: roughly one draw in five makes it inert.

### (b) Gap distribution by size (completion gap, pp; mean / p5 / p95 over draws)
| size | mean | p5 | p95 | leaving-gap mean |
|---:|---:|---:|---:|---:|
| 50k | +0.015 | +0.000 | +0.103 | +0.022 |
| 200k | +0.337 | +0.026 | +0.872 | +0.418 |
| 500k | +0.674 | +0.127 | +1.539 | +0.852 |
| 1m | +1.030 | +0.205 | +2.130 | +1.386 |
| 2m | +1.274 | +0.205 | +2.771 | +1.790 |
**Pooled (5 sizes, per draw):** completion gap mean **+0.666** (median +0.621; p5 **+0.118**; p95 **+1.385**);
leaving gap mean **+0.894** (median +0.946; p5 **−0.210**; p95 **+1.975**). `yang_endog` pooled completion mean
**+1.251** (p5 +0.174, p95 +2.596).

### (c) Top-3 load-bearing parameters (Spearman ρ of the pooled completion gap with each draw)
| rank | parameter | ρ (completion) | ρ (leaving) | univariate R² | share of R² |
|---|---|---:|---:|---:|---:|
| 1 | **factory wage multiplier** | **+0.784** | +0.704 | **0.586** | **71.6%** |
| 2 | **formal wage multiplier** | **−0.357** | −0.311 | 0.115 | 14.1% |
| 3 | **β (future weight)** | **−0.232** | −0.182 | 0.064 | 7.8% |
Next: convex-mapping scale (−0.128, 2.1%), informal wage (+0.085, 0.9%). **Yang's own slope/anchor barely move the
gap** (ρ = −0.036 / +0.078): once the gate share is mapped, the toy's outcome is driven by the **relative factory
wage** and by **how much families weight the future** — the Yang mapping is necessary for a gate to exist, but its
parameters are not what makes the margin large. This is a toy decomposition, not a causal claim.

### (d) Does any parameter draw make Yang inert?
**Yes — 181 of 1,000 draws (18.1%).** Inert draws have a **lower factory-wage multiplier** (mean 2.08 vs 2.35
among active draws) and a **higher formal wage** (2.16 vs 1.98): the gate only binds when factory work pays enough
relative to the formal alternative. Inert draws are spread across all three gate-mapping variants (convex 69,
linear 58, proportional 54), so no single mapping is responsible; the binding parameters are the wage pair.

### (e) Runtime
**151.8 s** for run 1 and **155.6 s** for run 2 (≈2.5 min each), well inside the declared <10-minute target; 45,000
runs; two runs byte-identical.

## 3. What this means (and what it does not)

- The Yang gate margin is **robustly active in ~two-thirds of the declared parameter space** (and ~82% with the
  endogenous rule), with the effect rising in city size and **the factory wage premium and β doing the load-bearing
  work**. In roughly one draw in five the margin disappears because factory pay is too low relative to formal work.
- The predeclared v2 falsifier is **ACTIVE** at 200 seeds, but only just at 500k — so **"active" is not "large at
  every size"**: the 50k and 100k cells are inert by construction of the Yang map (g≈0).
- **No country claim, no evidence claim, no causal/direction claim.** The "pp" units are a toy index; the parameter
  ranges are declared plausibility ranges, not a posterior; the decomposition is descriptive (univariate R² shares,
  not causal).
- **Recommendation (per the Lead's instruction):** because the margin is robustly active in the majority of draws
  (and in 82% with the endogenous rule), the **next step is to wire the same parameter-MC + paired-seed test into the
  coevolution model's city-size block** — carrying (i) the same draw ranges, (ii) the same CRN pairing, (iii) the
  same ≥0.5 pp-at-≥3-sizes bar, and (iv) the **inert draw set as an explicit boundary condition** (the gate is a
  wage-premium object, not a city-size object alone). That test should be predeclared before any coevolution run; it
  is not run here.

## 4. Files

- `results/grid_200seeds.csv`, `results/grid_200seeds.console.log` — deterministic 200-seed grid.
- `results/mc_results.json` — MC summary (distributions, robust-ACTIVE, sensitivity, variance decomposition, inert
  draws, pre-shock check, seeds).
- `results/mc_per_draw.csv` — per-draw parameter values, size gaps, robust/inert flags.
- `results/mc_console.log` — run record (no clock in result JSON; runtime only in the console log).
- `MC_PRE_DECLARATIONS.md` (+ `.sha256`), `code/mc_yang.cjs`, `code/pathways_yang.cjs` (v2.1), original preserved as
  `code/pathways_yang.orig_leadrun.cjs`.
