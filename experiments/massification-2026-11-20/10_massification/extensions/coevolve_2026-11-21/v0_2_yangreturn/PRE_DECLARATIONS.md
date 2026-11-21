# v0.2-YANGRETURN PRE-DECLARATIONS — return-side Yang wiring (`g(N) × C_value`) — BEFORE ANY RUN

**Label: `SIMULATED` / `ILLUSTRATIVE`.** New extension; **coevolve v0 and v0.1-YANG stay frozen** (v0
predeclaration `7d25e176…`; v0.1 predeclaration `3dea4786…`). This document is hashed before any run.

## 0. What this wires, stated plainly

This is a **return-side** wiring: the Yang occupational-variety mapping scales the **credential/option value** the
household places on a level, not the incidence of credential requirements at gate places. The v0.1 audit found the
gate-incidence reading **inert by construction** (every gate applicant already holds the prerequisite credential;
0/447,098 candidates lacking it), so this extension does **not** test gate scarcity — it tests whether a
**city-size-scaled return margin** changes household decisions and education outcomes. Both the wiring and its
limits are declared here.

**City-size block.** Town size `N ∈ {200k, 500k, 1m, 2m}` enters **only** through Yang variety and the resulting
`g(N)`. Household/cohort structure, district geography, gates, supply and prices are otherwise **fixed at v0's
declared values**. The choice is explicit: this isolates the gate/return margin, **not demography**.

**Yang mapping.** `D(N) = b·ln N + (anchorD − b·ln 1e6)` with `b = 128` and `anchorD = D(1e6) = 500` as the baseline
declarations (Yang et al. 2026 b adopted; intended for a local slice, not the paper's MSA estimate; no city data
read). `g(N) = clip((D(N) − D(50k)) / (D(2m) − D(50k)), 0, 1)`. Mapping variants (equal probability in the MC):
(i) linear `g = (D − D_lo)/(D_hi − D_lo)`; (ii) proportional `g = D/D_hi`; (iii) convex
`g = 1 − exp(−(D − D_lo)/scale)` with `scale ~ U[100, 400]`.

**The wiring.** `C_eff(L, N) = C_L · (1 + α·g(N))`, with `α = 1.0` baseline and the MC drawing **`premium_mult` ~
U[0.85, 1.15]` applied to `C_eff`** (the Yang-toy wage analogue). `C_eff` replaces the static `C_L` in the household
value of attending (v0 `_value_attend`: `weight_credential · C_L · c_market · p_gate` → 
`weight_credential · C_eff · c_market · p_gate`). No other object changes. **`g(N)` is fixed for `yang`;** it is
**0 for `none`** (α·g = 0).

## 1. Designs

- **`none`:** `α·g = 0` (the static v0 household value; must reproduce v0 baseline at default declarations — see §4).
- **`yang`:** fixed `g(N)` as above.
- **`yang_endog`:** the credential value responds to **applicants per gated place**, with a **declared one-year
  lag** and bounded dynamics. Exact rule: at the start of year `t`, read the previous year's `(t−1)` gate records;
  let `r_t = mean(applicants/places)` over the **selective** and **university** gates (both are the model's existing
  gated places; if a gate has no places, it is skipped); then
  `m_t = min(1.50, m_{t−1} + 0.05)` if `r_t > 3`; `m_t = max(0.25, m_{t−1} − 0.05)` if `r_t < 1`;
  otherwise `m_t = m_{t−1}`; `m_0 = 1.0`. The effective factor is `(1 + α·g(N)·m_t)` (clipped so it is
  non-negative). This is the declared bounded response — no tuning.

## 2. MC design (frozen)

- **150 parameter draws × paired seeds {0, 1} × sizes {200k, 500k, 1m, 2m} × designs {none, yang, yang_endog} =
  3,600 runs.**
- **Draw ranges:** Yang `b ~ U[100, 160]`; `anchorD ~ U[400, 600]`; mapping variant equal probability (linear /
  proportional / convex with `scale ~ U[100, 400]`); **`premium_mult ~ U[0.85, 1.15]`** on `C_eff`;
  **`beta_mult ~ U[0.7, 1.3]`** (future/option weight); **`travel_mult ~ U[0.5, 1.5]`**; **`child_wage_mult ~
  U[0.85, 1.15]`**. (The v0.1 request's formal-return multiplier is not drawn because the return-side wiring moves
  `C_value`; the alternative-return proxy used in the boundary test is `child_wage_mult`, declared in §5.)
- **Fixed draw RNG seed: 20261121.** One PRNG stream for the draws, identical on every run.
- **CRN:** arrival noises depend only on `(seed, cohort, individual, year, channel)` — never on design or draw — so
  the same seed gives the same arrivals across designs and draws (paired designs, common random numbers).
- **Determinism:** two complete MC runs must produce **byte-identical** `mc_results.json` and `mc_per_draw.csv`.
- **Runtime:** v0 runs ≈ 0.6–0.8 s; 3,600 runs serially ≈ 36–48 min, so the MC is executed with a **declared
  process pool of 6 workers** (the model is deterministic per run; aggregation is order-stable). Declared runtime
  limit **45 min**; if measured projection exceeds it, **reduce to 100 draws (2,400 runs)** and record the
  reduction and reason in the results — no other change.
- **Pre-shock:** the wiring is a **standing parameter on from t = 0** (not an event), so cross-design pre-shock
  equality at y=20–22 is **not implied** and is not used. Instead the declared **identity guard** is: with default
  declarations and `α·g = 0`, the `none` design must reproduce the frozen v0 **baseline** run (same seed) byte for
  byte on panel and pupil-year tables. The MC reports `PRE-SHOCK/IDENTITY: PASS` iff that holds.

## 3. Outcomes and the bar

- **Completion:** share of scored cohorts (entry years 6–17) completing **upper secondary by age 20**
  (`completed_upper_by_age_20`, cohort table), expressed in **pp** as ×100.
- **Leaving:** mean `left_secondary_early_share` over scored cohorts, pp.
- **Bar (same as the Yang MC):** per draw, a **size counts** if `|completion_gap| ≥ 0.5 pp` at that size, where
  `completion_gap = yang − none` (seed-mean). A draw is **robustly ACTIVE** if **≥ 3 of the 4 sizes** count; the
  headline is the **share of draws robustly ACTIVE** (primary `yang`; same computed for `yang_endog`). Report the
  leaving gap on the same basis (descriptive).
- **Distributions:** median and p5/p95 (over draws) of seed-mean completion/leaving gaps by size, for `yang` and
  `yang_endog`.
- **Coexistence metrics by design/size:** mean over scored years of `unused_accessible_share`, queue ratio
  (`qualified_per_place` at the selective gate) and `gate_household_share`, from the model's own
  `coexistence_series`; reported, not thresholded.
- **Sensitivity:** Spearman rank correlation of the pooled completion gap (per draw, mean over seeds/sizes) with
  each drawn parameter (`b`, `anchorD`, mapping index, `convexScale`, `premium_mult`, `beta_mult`, `travel_mult`,
  `child_wage_mult`); **top-3 by |ρ|**; a **variance share** from univariate OLS R² (declared descriptive,
  non-causal). Report the same for the leaving gap.
- **Boundary contingency (Yang-toy carry-over):** the Yang-toy inert-draw definition (low premium multiplier +
  high alternative return) is mapped to this MC as **`premium_mult ≤ 0.95` AND `child_wage_mult ≥ 1.05`** (the
  declared alternative-return proxy). Report the **2×2 contingency** (coevolve inert/active × Yang-toy inert/active)
  for the return-side margin, and state whether the same wage-premium boundary reproduces. Here "coevolve inert"
  = not robustly ACTIVE (fewer than 3 of 4 sizes meeting the bar).

## 4. Identity guard and what is forbidden

- `none` at default declarations must be **byte-identical** to the frozen v0 baseline run (same seed/arm). Failure
  is `IDENTITY-FAIL` → stop.
- **No parameter, threshold, design, bar, draw range or seed may change after any MC result is seen.** No tuning;
  failures reported as failures.
- **STOP clause:** if the return-side wiring is also structurally inert (e.g., `C_eff` never reaches the decision
  margin because the engine ignores it, or the effect is exactly zero in every run), record the structural reason
  and stop; do not force a variant.

## 5. What this extension cannot claim

No observed data; no country claims; no causal or direction claims. It does **not** test gate scarcity or
credential requirements at gates (v0.1 showed that reading is inert by construction); it tests only the **return
margin**. `SIMULATED`/`DERIVED`/`ILLUSTRATIVE` labels on every artifact.
