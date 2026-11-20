# DRY-RUN PLAN — implementing the shadow module as generator v1.3

**LABEL: SYNTHETIC / PLAN.** No v1.3 code exists. This is the step-by-step plan for the first dry run, what it will
emit, what it will check, and what would make it fail. Written after `PRE_DECLARATIONS.md` was frozen; it adds no
parameter and changes no threshold.

---

## 0. Dependency and non-goals

**Hard dependency.** v1.3 extends v1.2. There is no `v1_2/code/sim_v1_2.py` yet — only the frozen
`v1_2/PRE_DECLARATIONS.md`. v1.3 cannot be built or run before v1.2 exists, and check **c6** (v1.2 invariance)
cannot be scored until the frozen `results/synthetic_panel_v1_2.csv` exists. If it does not, c6 is `VOID` and the
v1.3 results are provisional.

**Not built here:** no provider/supply block; no hours; no fees beyond the declared cost share; no welfare
calculation; no estimation; no calibration; no re-fit of any v1.2 parameter; no country model. The module is one
function plus one substitution.

---

## 1. Where it plugs into v1.2

The insertion template is `generator_v1/code/sim_v1.py` (`simulate_country`, 255–488), which shares its structure
with the v1.2 spec. Line numbers below are **v1 line references used as the template**; in v1.2 they shift.

| # | hook | v1 template | state available at that point |
|---|---|---|---|
| H1 | after schooling supply and cohort flow are computed | after `comps` loop, v1 ~416 | `seat_L, surv_L, intake_L, grads_L, comps_L, Cann_L, elig_L, ger_cur` |
| H2 | after matching / queue update | after `queue_carry`, `E_r` update, v1 ~427–456 | `cand, hires, qr, rf, vac, pool, E_r, queue_carry` |
| H3 | after wages | v1 ~461–462 | `w_for, w_inf` (for `V_g4`) |
| H4 | **before** the store block | v1 ~474 | everything above |
| H5 | next period's eligibility terms | v1 ~384–387 (`elig[1]`, `elig[2]`, `ter_pool`) | where `Π` is substituted for `π⁰` |

### 1.1 The call

```python
# H4, inside simulate_country, after wages and before the store block
shadow = shadow_block(
    gate_state=gate_state_from(cp, t, seat, intake, grads, Cann, elig, ger_cur,
                               vac, hires, qr, rf, w_for, w_inf),
    params=P["shadow"],          # frozen block from PARAMETERS.csv
    country_inputs=cp["shadow"], # phi, s_g, sigma, nu  (declared per synthetic country)
)
# adds: shadow["D"][g], ["S"][g], ["R"][g], ["pi0"][g], ["pi1"][g], ["Pi"][g],
#       ["V"][g], ["Q"][g], ["kappa"][g], ["p_q"][g][q]
```

`shadow_block` is **pure**: it reads state, returns numbers, writes nothing. All persistence is in `out[...]`.

### 1.2 The one substitution (H5)

`Π` enters only the *next* period's advance rate, through the eligibility/tertiary-pool terms:

```python
# v1.3 replacement for v1 ~384-387 (one-year lag, inside the t-loop read of t-1 flows)
ratio_L = Pi_prev[L] / pi0_prev[L]                    # bounded to [1, 1 + delta_L]
elig[1] = max(out["grads"][0, t-1] * ratio_0 / max(Cann[1], 1e-9) * P["overage_cap"], 0.0)
elig[2] = max(out["grads"][1, t-1] * ratio_1 / max(Cann[2], 1e-9) * P["overage_cap"], 0.0)
elig[3] = max(100.0 * P["ter_trans_cap"] * ter_pool * ratio_2 / max(Cann[3], 1e-9), 0.0)
```

Nothing else in v1.2 is touched. The existing `queue_carry`, `seat`, `surv`, `pipe`, `ger_cap` and wage blocks are
read-only. This is what makes c6 a meaningful test rather than a formality.

### 1.3 Gate-state contract (exact)

| gate | candidates | capacity | advances | `κ` source |
|---|---|---|---|---|
| g1 | `grads[0]` | `seat[1] * Cann[1]` | `intake[1]` | `rf[0]` |
| g2 | `grads[1]` | `seat[2] * Cann[2]` | `intake[2]` | `rf[1]` |
| g3 | `grads[2]` | `seat[3] * Cann[3]` | `intake[3]` | `rf[2]` |
| g4 | `pool[1:3]` | `vac[1:3]` | `hires[1:3]` | weighted mean `rf[1:3]` |

`Q = candidates/capacity` clipped `[0,10]`; `π⁰ = advances/candidates` clipped `[0.01,0.999]`;
`κ` clipped `[1.0,5.0]`; `R = (1+Q)^0.4 · (1/π⁰)^0.4 · κ^0.2` clipped `[1.0,20.0]`.
g0 uses the primary seat ratio with `V=0`, `δ_0=0.02`, and never enters `D*`.

### 1.4 Parameter file

`v1_3/PARAMS.md` is generated **from** `PARAMETERS.csv` (the module's frozen table) plus the v1.2 block, so there is
one source of truth. The generated file's sha256 goes into the run manifest, and `sim_v1_3.py` re-hashes both it and
`PRE_DECLARATIONS.md` at start-up and refuses to run on mismatch.

---

## 2. Data needed — all on disk

| input | file | used for | status |
|---|---|---|---|
| v1.2 frozen panel | `v1_2/results/synthetic_panel_v1_2.csv` | c6 byte-identity | **missing until v1.2 runs** |
| v1.2 code | `v1_2/code/sim_v1_2.py` | the thing being extended | **missing until v1.2 is built** |
| observed out-of-school rates | `10_massification/data/UNIVERSALIZATION_SERIES.csv` (`oos_upper_secondary`, 2020) | validation of the declared `ν` vector | on disk |
| vulnerable-employment shares | `04_data/ECONOMY_SERIES.csv` (2019) | `φ_c` | on disk |
| EAP Mincer return | `02_lit/ECON_TARGETS.csv:3` | `r_EAP` | on disk |
| tutor-fee record | `04_data/shadow_round2/data/shadow_fees_round2.csv`; `SHADOW_DATA.md` §5–§6 | fee shares `s_{c,g}` | on disk |
| shadow incidence record | `02_lit/SHADOW_TARGETS.csv`; `04_data/TARGETS_SHADOW.csv` | the 85% anchor and the out-of-scope contrasts | on disk |
| gate gradient | `09_relations/data/shadow_gradients.csv:2-5` | NOT-SCORED diagnostic (does the model produce an HK-like gradient?) | on disk |

No external data request. No web. No API.

---

## 3. What the first dry run emits

1. **`results/shadow_gates_v1_3.csv`** — one row per `(country, year, gate)`:
   `country, year, gate, Q, pi0, pi1, Pi, kappa, R, V, s_g, D_gate, spend, p_q1..p_q5`.
2. **`results/synthetic_panel_v1_3.csv`** — v1.2's panel plus `gate, D_gate, D_cohort, R, pi0, Pi, V, s`.
   Every row `label = SYNTHETIC`.
3. **`results/shadow_checks_v1_3.csv`** — `check_id, verdict, component, value, threshold, note` for c1–c6.
4. **`results/shadow_decomposition_v1_3.csv`** — per country-gate, the additive contribution of each Θ term
   (`a_g`, `b_Z lnR`, `b_V ln(1+V)`, `b_Δ ln(1+Δπ)`, income, fee) at the median household. This is the table that
   shows *why* a country's demand is what it is; it is arithmetic, not identification.
5. **`results/shadow_sensitivity_v1_3.csv`** — the pre-declared one-at-a-time grid (`b_Z`, `b_V`, `b_Δ`, `b_y`,
   `b_F`, `δ_g`, `H`, `σ_c`, `s_PHL`, `s_KHM`) with c1–c5 re-scored in every cell.
6. **`results/shadow_country_inputs_audit.csv`** — every country-varying quantity and its declared value; this is the
   file c4c is decided on.
7. **`FINDINGS.md`** — written after the run, PASS/FAIL/VOID/NOT-SCORED with the same prominence for failures.

A first *dry* run (smoke test) stops after 1–2 and prints the `R` distribution, the `D` distribution and the c5
identities — it does **not** score c1–c4. That is the recommended first execution: it costs seconds and catches
gate-mis-indexing and saturation before any check is scored.

---

## 4. Runtime

v1 is 30 countries × 56 years × 4 levels in ≈1 s (`generator_v1/FINDINGS.md`, header). The shadow block adds
`4 gates × 5 quintiles` sigmoid evaluations per country-year: 30 × 56 × 20 = **33 600 evaluations**, plus the four
`Π` substitutions — negligible against the existing loop.

| job | estimate |
|---|---|
| one scored v1.3 run | ≈ 1.5 s |
| smoke test (gate/queue dump) | < 2 s |
| c1/c2 counterfactual reruns (R×2, φ×1.25) | 2 extra runs, ≈ 3 s |
| c6 ablation (shadow off) | 1 run + sha256, ≈ 2 s |
| pre-declared OAT sensitivity (10 parameters × 3 values) | 30 runs, ≈ 45 s |
| two-clean-run determinism check | 2 runs + diff, ≈ 4 s |
| **whole check suite** | **< 2 minutes, single process, no parallelism** |

Memory: the panel is ~7 k rows; the shadow columns add < 1 MB. No GPU, no cluster.

---

## 5. What will be checked, in code

| check | implementation | what a failure would mean |
|---|---|---|
| **c1** | `check_c1()`: central-difference `∂D/∂lnR` by rerunning with `R×1.01` at each gate; plus a counterfactual run with `R→2R` at g2 only | The gate channel is inert (likely: v1.2's seats are generous, so `Q≈1` and `R≈1.1` everywhere). That is a **finding about the generator's gate machinery**, not about the world — report it and stop. |
| **c2** | `check_c2()`: `∂D/∂ln(1+V)`; plus a counterfactual `φ→1.25φ` at g2 | The return channel is too weak to matter, i.e. the model's tutoring demand is driven almost entirely by the fee and the queue. Report the decomposition that shows it. |
| **c3** | `check_c3()`: `max D_g0`; ratio `D_g0/D_g1` | A bug: gate terms are leaking into the pre-gate, or `V_g0 ≠ 0`. |
| **c4** | `check_c4()`: `D_HKG,g2` at the declared comparison year against `[0.75,0.95]`; `D*` ordering gaps; `shadow_country_inputs_audit.csv` inspection | Ordering carried by something other than the declared inputs (VOID if a country-specific coefficient exists). A FAIL with the decomposition is a substantive result: the gate rule alone does not reproduce the expected national ordering. |
| **c5** | `check_c5()`: vector identities and bounds on every row | A code defect. |
| **c6** | `check_c6()`: ablation run, sha256 of `synthetic_panel` vs the v1.2 frozen file | The shadow block is leaking into v1.2 arithmetic — the module is invalid until fixed, because it would mean v1.2 has been re-fitted. |

Supporting diagnostics, **NOT-SCORED**:
- HK 2003 gate gradient (`shadow_gradients.csv:2-5`): does the model produce a rise of similar shape from g1→g2?
  Reported, never scored — the observed gradient is a *grade* gradient in one city in one year.
- PHL 46.5 % all-basic (`SHADOW_TARGETS.csv:17`) beside `D*_PHL`: reported as an order-of-magnitude comparison only,
  with the denominator difference stated every time.
- KHM 68.4 % grade-9 case study (`:10`) beside `D_KHM,g1`: reported, labelled a two-school case study, and expected
  **not** to be reproduced, because the Cambodian mechanism is teacher-sold supply, which this module does not model.

---

## 6. Implementation steps (each with an acceptance gate)

1. **Copy and freeze.** `v1_3/code/sim_v1_3.py` = `v1_2/code/sim_v1_2.py` + the shadow block. Hash it. Gate: with
   `shadow_off=True` the panel is byte-identical to v1.2 (this is c6, checked *before* any scored run).
2. **Gate-state extractor.** `gate_state_from(...)` returning the §1.3 contract only. Gate: unit test on a hand-built
   state where `Q, π⁰, κ` are known — `R` must equal the closed-form value.
3. **`shadow_block`.** The frozen equation, no I/O, no RNG. Gate: golden-value test on three hand-computed cells.
4. **Smoke test.** Dump `R`, `D`, `Π` distributions. Gate: no NaN; `R ∈ [1,20]`; `D ∈ [0,1]`; `D_g0 ≪ D_g1`;
   `R` is not constant across gates (if it is, H1/H2 are mis-wired).
5. **Scored run.** c1–c6 + decomposition. Gate: every check has a verdict, including `VOID`.
6. **Sensitivity.** The pre-declared OAT grid. Gate: central result unchanged and *not* silently replaced.
7. **Determinism.** Two clean runs, byte-identical. Gate: diff is empty.
8. **`FINDINGS.md`.** Gate: every FAIL and VOID printed with the same prominence as every PASS, and the §13
   "cannot claim" paragraph copied verbatim into the results file.

---

## 7. Known risks, and what each would mean

1. **`R` is inert.** If v1.2's seat and vacancy paths are generous, `Q ≈ 1` and `π⁰ ≈ 0.9` at most gates, so
   `R ∈ [1.0, 1.3]`, `ln R ∈ [0, 0.26]`, and the gate channel contributes < 0.6 logit everywhere. Then c1's +10 pp
   threshold may still pass (the coefficient is 2.0), but the *cross-country* differentiation from pressure is
   small. **Meaning:** in this generator, demand differences are carried by exposure and returns, not by pressure;
   report it — do not raise `b_Z` to fix it.
2. **Saturation.** At hard gates `D → 0.95+`, so any pp-based threshold is mechanically hard to clear even when
   `∂D/∂lnR > 0`. **Meaning:** the check is informative only where `D ∈ [0.05, 0.90]`; the module must report the
   `D` distribution and, if a cell is saturated, mark that cell's c1/c2 component `NOT-SCORED` (pre-declared here,
   not chosen after seeing it) rather than counting it as a pass.
3. **Feedback explosion.** `Π → 1` raises next-period completers, lengthens the queue and raises `R`, which raises
   `D`. The loop is bounded by `R ≤ 20`, by `ger_cap`, by `seat`, and by the one-year lag; but a limit cycle is
   possible. **Meaning:** report the `R` time path; a cycle is a property of the generator, not a finding about
   credential inflation in any country.
4. **v1.2 absent or different.** Then c6 is `VOID` and nothing in v1.3 can be interpreted as "v1.2 unchained".
   **Meaning:** stop and wait for v1.2; do not substitute v1.
5. **KHM ordering.** Per `PRE_DECLARATIONS.md` §8 (c4, declared risk), KHM's gate-conditional rate may exceed PHL's
   while its cohort incidence does not. **Meaning:** if `D*` ordering fails, the FAIL is the result; the channel
   decomposition is the explanation; no parameter moves.

---

## 8. What the first dry run will *not* tell anyone

It will not tell anyone anything about Hong Kong, the Philippines or Cambodia. It will not identify an incidence
level, a causal return, a tutoring effect or a welfare consequence. It will tell us whether a declared gate-demand
rule, run on the generator's own queue state, behaves the way its specification says it behaves — and whether the
programme's expected high/medium/low ordering survives contact with the mechanism. Both answers are useful; only
the first is testable by this module alone.
