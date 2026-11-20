# PRE-DECLARATIONS — v1.3 shadow-education-at-the-gates module (VERBATIM COPY)

**LABEL: SYNTHETIC.** This file is a copy. It is not a new pre-declaration and it changes
nothing. The binding documents are the two frozen files in `shadow_module/`, reproduced below
byte-for-byte:

| frozen source | sha256 |
|---|---|
| `shadow_module/PRE_DECLARATIONS.md` | `cf8c61cb818cd63acfb2ada594bc9541bfcb0711f801e13b7eee3b86508f94f2` |
| `shadow_module/PRE_DECLARATIONS_S1_NOTE.md` | `af49a616a7b57c4ef23a693c155d022cd17817f66f5acafba4dc6798dedb65eb` |

`code/sim_v1_3.py` re-hashes both frozen files at start-up and refuses to run on mismatch, and
it also checks that this copy contains both of them verbatim (so the copy cannot drift).

Implementation gap resolutions (which v1.2 country carries which declared country type, the
gate-state contract, the feedback hook) are **not** here: they are declared separately in
`IMPLEMENTATION_NOTE.md` and `IMPLEMENTATION_NOTE_N1.md`, both written and hashed before the
first v1.3 run. Nothing in those notes changes a parameter or a threshold.

---

# PART 1 — `shadow_module/PRE_DECLARATIONS.md` (verbatim)

# PRE-DECLARATIONS — shadow-education gating module (synthetic generator v1.3)

**STATUS: FROZEN BEFORE ANY RUN.** Written 2026-11-20T22:40+08:00 (Asia/Shanghai), worker W2.
**LABEL: SYNTHETIC.** Everything a v1.3 run emits is a declared-assumption simulation — not evidence, not an
estimate, not a forecast, not a model of any real country. No causal claim, no direction claim, no welfare claim.
**This file is not changed after any v1.3 result is seen.** Its sha256 is recorded in `RUN_MANIFEST.json`;
`code/sim_v1_3.py` must re-hash it at start-up and **refuse to run on mismatch**.

---

## 0. The directive this module encodes (verbatim)

> Shadow education was paused and must now "show up" **around the relevant gating**: tutoring demand is a
> *demand signal at the gates/queue*, not a generic add-on.

Recorded from Dr. Trey Menefee's directive, relayed to worker W2 on 2026-11-20. The module therefore has **no
free-standing "shadow sector" block**: the only object it computes is *household tutoring demand at a gate*, and
the only way demand can be non-zero is through gate pressure, credential stakes, tutoring's effect on passing,
and household liquidity.

## 1. What is inherited, and the binding exclusion list

**Inherited (read-only, never re-fitted):** `MODEL_ARCHITECTURE.md` (Layer 2 gate/queue machinery; Amendments A1,
A2), `v1_2/PRE_DECLARATIONS.md` (the frozen v1.2 spec this module extends), `generator_v1/FINDINGS.md` (what v1
does, fails, and which assumption is load-bearing), and the closed shadow phase
(`LOOP_CLOSEOUT.md`, `08_council/brief_008/`, `04_data/TARGETS_SHADOW.csv`, `02_lit/SHADOW_TARGETS.csv` +
`COUNTRY_CARDS/`, `04_data/shadow_round2/SHADOW_DATA.md`, `09_relations/data/shadow_gradients.csv`).

**Binding exclusions carried from `LOOP_CLOSEOUT.md` §2, §5** — this module may not, and does not, reopen:
1. Gate architecture identification (which gate binds) — EXCLUDED.
2. Provider technology as *the* missing channel — EXCLUDED.
3. **Cross-country shadow-education incidence — EXCLUDED as an empirical claim.** The module may not claim any
   country's incidence level or trajectory; its "ordering check" (§9, c4) is a *synthetic reproduction check on a
   declared parameterisation*, and must be reported with that wording.
4. Mechanism classification from national aggregates — EXCLUDED.
5. Country completion forecasting — EXCLUDED.
6. Pricing the shadow sector (provider entry costs, hours, rents) — NOT OBSERVABLE; the module carries **fees**
   only as declared cost shares, never a provider model.

**Also binding:** the programme's own verdict language — "Within this model class and the available evidence,
identification of these claim classes is not established."

## 2. Unit of the model

A **household** `i` (in income quintile `q`) facing **gate** `g` in synthetic country `c`, year `t`, decides
whether to buy tutoring. The module emits, per `(c, g, t)`:

- `p_{c,g,q,t}` — household probability of buying tutoring (one decision per household);
- `D_{c,g,t} = Σ_q ω_q · p_{c,g,q,t}` — **gate participation** (share of households at that gate buying tutoring);
- `S_{c,g,t} = Σ_q ω_q · p_{c,g,q,t} · F_{c,g}` — implied monthly tutoring spend (declared fee units);
- `D*_{c,t} = Σ_{g∈{1,2,3}} ν_{c,g} · D_{c,g,t}` — **cohort incidence** (share of the declared secondary-age cohort
  buying tutoring; out-of-school youth count as non-participants);
- `Π_{c,g,t} = π⁰ + D_{c,g,t}·(π¹ − π⁰)` — the realised gate advance rate after the shadow channel.

There is **no separate shadow-sector supply block**. Tutoring is available at the declared fee; the module does
not model providers, hours, rents or entry.

### The gate list (frozen)

| gate | name | credential contested | decisive transition (mechanical, from v1.2 state) |
|---|---|---|---|
| `g0` | PRE-GATE (control, not a gate) | none — no positional good | primary seat ratio; declared `δ_0 ≈ 0` |
| `g1` | GATE-LS | lower-secondary completion | entry into lower secondary (`intake₁ / grads₀`) |
| `g2` | GATE-US | upper-secondary completion | upper-secondary credential converting onward (`ter eligibility / grads₂`) |
| `g3` | GATE-TER | tertiary entry | entry into tertiary (`intake₃ / grads₂`) |
| `g4` | GATE-JOB | credential → formal rung | hiring into formal rungs 1–3 (`hires / pool`) |

`g0` exists **only** as the c3 control. It is never scored as a gate and never enters `D*`.

## 3. State variables read from the generator (no new state except demand)

Read-only from v1.2: `seat_L`, `surv_L`, `intake_L`, `grads_L`, `comp_L`, `Cann_L`, `elig_L`, `ger_L`; `vac_r`,
`queue_r`, `pool_r`, `hires_r`, `rankf_r`, `w_for_r`, `w_inf`; `X`, `Tstate`, `Y`, `lit`, `sec`.
Written by the shadow block: `D`, `S`, `π⁰`, `π¹`, `Π`, `R`, `V`, `s`, and the per-quintile `p`. Nothing else.

## 4. The shadow-demand equation (FROZEN)

For household `i` in quintile `q` at gate `g`, country `c`, year `t`, with `σ(x)=1/(1+e^{−x})`:

```
p_{i,c,g,q,t} = σ( Θ_{c,g,q,t} )

Θ_{c,g,q,t} = a_g
            + b_Z · ln R_{c,g,t}                    (i)   GATE PRESSURE
            + b_V · ln(1 + V_{c,g})                 (ii)  EXPECTED CREDENTIAL RETURN
            + b_Δ · ln(1 + Δπ_{c,g,t})              (iv)  TUTORING'S LIFT AT THE GATE
            + b_y · ln(y_{c,q,t} / ȳ_{c,t})         (iii) HOUSEHOLD INCOME POSITION
            − b_F · ln(1 + s_{c,g} / (y_{c,q,t}/ȳ_{c,t}))   (iii) FEE BURDEN

D_{c,g,t} = Σ_q ω_q · p_{i,c,g,q,t},   ω_q = 1/5 (declared equal quintile weights)
```

This equation is frozen. No term may be added, dropped, re-signed, re-specified or re-weighted after this file is
hashed. Every parameter appears in `PARAMETERS.csv` with its provenance label and where it enters.

### 4.1 Gate pressure `R` (mechanical — defined, never hand-set in v1.3)

For each gate, from the generator's own state:

```
Q_{c,g,t} = candidates_{g} / capacity_{g}          (queue length: applicants per place; clipped [0,10])
π⁰_{c,g,t} = advances_{g} / candidates_{g}          (P(advance | current level, rank); clipped [0.01,0.999])
κ_{c,g,t} = rankf at the destination rung           (credential rank factor; clipped [1.0, 5.0])

R_{c,g,t} = (1+Q)^{0.40} · (1/π⁰)^{0.40} · (κ)^{0.20}      clipped to [1.0, 20.0]
```

with `(candidates, capacity, advances)` = `(grads₀, seats₁, intake₁)` at g1; `(grads₁, seats₂, intake₂)` at g2;
`(grads₂, seats₃, intake₃)` at g3; `(pool₁₋₃, vac₁₋₃, hires₁₋₃)` at g4. At a neutral gate (`Q=0, π=1, κ=1`),
`R=1` and `ln R = 0`. **The three components are reported separately** in the output so a reader can see which
drives `R`; the weights (0.40, 0.40, 0.20) are declared, not estimated.

### 4.2 Credential value `V` (declared; Mincer-anchored)

```
V_{c,g} = φ_c · r_EAP · ΔS_g · H            for g ∈ {g1, g2, g3}
V_{c,g4} = φ_c · G_c · H                    (formal-rung wage gap form; G_c from the model's own wage block)

φ_c   = 1 − vulnerable-employment share (observed, 2019)   — probability a credential is rewarded in wage work
r_EAP = 0.087     East-Asia-Pacific private Mincer return (compiled; calibration-only, NOT causal)
ΔS_g  = (3, 3, 4) years added by the credential at g1, g2, g3
H     = 20        declared present-value-equivalent working years
```

`V` is the **positional** value of the credential at a gate (its exchange value against the queue), **not** a
total human-capital return and **not** a causal effect. `V_{g0} = 0` **by definition** (no gate, no positional
good) — see §9 c3.

### 4.3 Tutoring's lift `Δπ` (declared effectiveness)

```
π¹_{c,g,t} = min(0.999, π⁰_{c,g,t} + δ_g · (1 − π⁰_{c,g,t}))
Δπ_{c,g,t} = π¹ − π⁰ = δ_g · (1 − π⁰_{c,g,t})      (tutoring closes a fraction δ_g of the failure gap)
δ_g = 0.30, 0.30, 0.25, 0.20   for g1..g4;   δ_0 = 0.02
```

`Δπ` is **larger where the gate is tighter** — this is the mechanism that makes shadow demand rise exactly where
the horse race is. It is a *declared* technology, not an estimated tutoring effect.

### 4.4 Income and fee burden

Household income is declared lognormal, `ln y_q ~ N(ln ȳ_c, σ_c²)`, evaluated at the five quintile midpoints
`z = (−1.2816, −0.5244, 0, 0.5244, 1.2816)` and normalised so that `mean(y_q) = ȳ_c`. `s_{c,g} = F_{c,g}/ȳ_c` is
the fee as a share of mean monthly household income. `σ_c` is a declared dispersion (no Gini series is on disk —
see `PARAMETERS.csv` and the grounding flags in `SHADOW_MODULE.md` §7).

## 5. The feedback loop (FROZEN)

Tutoring → gate pass → credential → queue → future pressure, one cohort duration lag:

```
Π_{c,g,t}   = (1 − D_{c,g,t}) · π⁰_{c,g,t} + D_{c,g,t} · π¹_{c,g,t}
intake_{L+1,t+1} uses Π instead of π⁰ as the realised advance rate
   ⇒ next period Q_{c,g+1,t+1} and R_{c,g+1,t+1} rise (via the generator's own queue_carry)
   ⇒ D_{c,g+1,t+1} rises   (the credential-inflation loop)
```

**Hard constraint:** the shadow block may only modify the *realised advance rate* by the bounded amount
`|Π − π⁰| ≤ δ_g(1−π⁰)`. It may **not** touch `seat`, `surv`, `pipe`, `ger_cap`, any wage parameter, the `X`
path, or any v1.2 behavioural parameter. Check c6 enforces this by ablation.

## 6. Declared parameters (central values — frozen; full table in `PARAMETERS.csv`)

| symbol | central | range for pre-declared sensitivity |
|---|---|---|
| `a_0` (pre-gate intercept) | −4.80 | — (not varied) |
| `a_g` (gate intercepts g1–g4) | −2.80 | — (not varied) |
| `b_Z` gate pressure | 2.00 | {1.2, 2.0, 2.8} |
| `b_V` credential return | 1.00 | {0.5, 1.0, 1.5} |
| `b_Δ` tutoring lift | 2.00 | {1.0, 2.0, 3.0} |
| `b_y` income position | 0.60 | {0.3, 0.6, 0.9} |
| `b_F` fee burden | 0.80 | {0.4, 0.8, 1.2} |
| `δ_g` (g1..g4) | 0.30, 0.30, 0.25, 0.20 | {0.15, 0.30, 0.45} |
| `r_EAP` | 0.087 | — (observed-compiled) |
| `H` | 20 | {10, 20, 30} |

Sensitivity runs are **pre-declared one-at-a-time** (OAT) around the central values; no multi-parameter search,
no optimisation, no likelihood. A central-value result is the scored result; sensitivity is reported beside it and
cannot replace it.

## 7. Country cases (declared synthetic types — **not** the real countries)

Three synthetic country types, named `SYN_HKG_LIKE`, `SYN_PHL_LIKE`, `SYN_KHM_LIKE`. **The same behavioural
parameter values (a, b) are used for all three.** Country variation enters *only* through the declared country
inputs below (full provenance and ranges in `PARAMETERS.csv` §C).

| input | SYN_HKG_LIKE | SYN_PHL_LIKE | SYN_KHM_LIKE | label |
|---|---|---|---|---|
| `φ_c` = 1 − vulnerable employment (2019) | 0.940 | 0.677 | 0.464 | OBSERVED (WDI/ILO) |
| fee share `s_{c,g}` of mean monthly household income | 0.0305 | 0.0400 | 0.0210 | DERIVED / DECLARED / DERIVED |
| income dispersion `σ_c` | 0.55 | 0.80 | 0.75 | DECLARED (no Gini on disk) |
| cohort weights `ν_{c,1}, ν_{c,2}, ν_{c,3}` | 0.10, 0.62, 0.22 | 0.30, 0.35, 0.10 | 0.28, 0.13, 0.02 | DERIVED from observed UIS out-of-school rates |
| out-of-school at upper-secondary age (2020) | 5.4% | 24.7% | 57.0% | OBSERVED (UIS SDG4) |

Illustrative gate states used by the **toy design check only** (not a v1.3 result) are in
`toy_design_check.py`; in v1.3 they are computed from the run.

**HKG anchor.** The ~85% figure is recorded on disk twice: `04_data/TARGETS_SHADOW.csv:4` (HKG, senior secondary,
85%, 2010, Kwo & Bray 2011, confidence *low* — "Neither of these surveys should be considered statistically
robust") and `02_lit/SHADOW_TARGETS.csv:9` (HKG, senior secondary, 85%, c.2011, Bray & Lykins 2012, *second-hand
quotation*, confidence *medium*). It is **stage-specific** (senior secondary, not all secondary) and its
denominator is disputed by the programme's own card. It is therefore used as a **wide band**, not a point target.

## 8. Checks — frozen with thresholds, scored in `results/shadow_checks_v1_3.csv`

**c1 — shadow participation rises with gate pressure (monotone, positive).**
PASS iff (i) the numerical `∂D/∂ln R ≥ 0` in **every** scored `(c,g,t)` cell; **and** (ii) the declared
*R-doubling experiment* (R→2R at g2, all else fixed) raises `D` by **≥ +10.0 pp in all three country types**.

**c2 — shadow participation rises with expected returns.**
PASS iff (i) `∂D/∂ln(1+V) ≥ 0` in every scored cell; **and** (ii) the declared *return experiment* (+25% on `φ_c`,
i.e. `V → 1.25V`, at g2) raises `D` by **≥ +2.0 pp in all three country types**.

**c3 — near-zero shadow demand before the gate (primary).**
PASS iff (i) `D_{c,g0,t} ≤ 0.025` in every country-year; **and** (ii) `D_{c,g0,t} ≤ 0.20 · D_{c,g1,t}` in every
country-year. **Declared structural note:** this check is largely structural (`V_{g0}=0`, `δ_0=0.02`, `R_{g0}≈1`);
it is a *consistency* check (guarding against a mis-indexed gate term), **not** an empirical prediction. Observed
primary-stage tutoring — PHL 23.8% (`02_lit/SHADOW_TARGETS.csv:18`), KHM 41.3% (`:11`) — is **out of this
module's scope** and is not explained by it (see `SHADOW_MODULE.md` §7).

**c4 — the HKG > PHL > KHM ordering, as a PRE-DECLARED reproduction check (not a fit).**
- **c4a (level anchor).** `D_{HKG,g2,t*} ∈ [0.75, 0.95]` at the declared comparison year `t*` (2020). Band =
  85% ± 10 pp, widened for the source's own confidence caveats.
- **c4b (ordering).** On the cohort-incidence statistic `D*`: `D*_HKG − D*_PHL ≥ 0.10` **and**
  `D*_PHL − D*_KHM ≥ 0.05`.
- **c4c (one rule, no country-specific behaviour).** Code inspection confirms **no** country-specific value of
  `a_g, b_Z, b_V, b_Δ, b_y, b_F, δ_g`; every country-varying quantity appears in the declared input table (§7) and
  in the audit list `results/shadow_country_inputs_audit.csv`. **If any country-specific behavioural parameter
  exists, c4 is VOID** (not PASS, not FAIL).
- **Declared ex-ante risk.** The gate channel and the return channel pull in opposite directions for KHM (tight
  gates and cheap fees raise demand; low `φ` lowers it). The pre-declared expectation is that the **ordering is
  carried mainly by cohort exposure `ν`, not by gate-conditional demand**, and that KHM's *gate-conditional* rate
  may exceed PHL's while its *cohort incidence* does not. If the ordering fails, it is reported as FAIL with the
  channel decomposition; it is not rescued.

**c5 — identity / accounting.**
PASS iff, in every scored row: `p ∈ [0,1]`; `D ∈ [0,1]`; `Σ_q ω_q = 1 ± 1e-12`; `π⁰, π¹, Π ∈ [0.01, 1]` and
`Π ≥ π⁰`; `S ≥ 0`; `D* ≤ Σ_g ν_{c,g}`; tutored head-count ≤ cohort at gate; no NaN/inf; `D_{g0} < D_{g1}`.

**c6 — v1.2 invariance (no re-fit of v1.2 behaviour).**
PASS iff, with the shadow block switched off (`D ≡ 0`), the v1.3 panel reproduces the frozen
`synthetic_panel_v1_2.csv` **byte-for-byte** (sha256 equality). If that file is absent, c6 is `VOID`.

## 9. Verdict vocabulary (frozen)

| verdict | meaning |
|---|---|
| `PASS` | every stated condition of the check held on the frozen parameterisation |
| `FAIL` | at least one stated condition did not hold; reported with the component numbers, **not rescued** |
| `VOID` | the check could not be scored for a declared reason: frozen-hash mismatch; country-specific behavioural parameter detected (c4c); v1.2 panel absent (c6); required state missing |
| `NOT-SCORED` | diagnostic reported but pre-declared as outside the scoring set (e.g. KHM G9 case-study comparison, PHL 46.5% comparison) |

A `FAIL` and a `VOID` are **findings about the generator, not about the world**, and must be printed in
`FINDINGS.md` with the same prominence as a `PASS`.

## 10. No post-hoc parameter changes (binding rule)

1. **No parameter in `PARAMETERS.csv` may be changed after this file is hashed**, except by writing a new,
   separately dated and separately hashed pre-declaration that discloses what was seen before the change.
2. **No threshold in §8 may be changed** after any run output exists.
3. A run whose code hashes do not match the manifest must **refuse to execute** and write no results.
4. Adding a *new* diagnostic is allowed and must be labelled `NOT-SCORED` **and** dated later than this file; it
   may never be promoted into the scored set.
5. The scored result is the **central-value** run. Sensitivity runs are reported beside it; the best-looking
   sensitivity cell may not be substituted for the central result.
6. If a check fails, the response is to report it — not to re-parameterise, re-band, or re-specify.

## 11. Determinism and output contract

- One NumPy `PCG64` stream, seed **20261120** (inherited from v1.2). No wall-clock/OS entropy. Floats at `%.10g`.
- **Two clean runs must be byte-identical.**
- Outputs (written by v1.3, not by this design pass):
  `results/synthetic_panel_v1_3.csv`, `results/shadow_gates_v1_3.csv`, `results/shadow_checks_v1_3.csv`,
  `results/shadow_decomposition_v1_3.csv`, `results/shadow_sensitivity_v1_3.csv`,
  `results/shadow_country_inputs_audit.csv`, `RUN_MANIFEST.json`, `FINDINGS.md`.
- Every row carries `label = SYNTHETIC`.

## 12. The toy design check (pre-declared, and its limits)

A single small calculation (`toy_design_check.py`) is permitted **as a design check only**. It is pre-declared
here, before execution, with these limits:

- It evaluates the §4 equation on **declared illustrative gate states** (§7 table), not on a v1.2 run.
- It **can** test c1, c2, c3, c5 as internal-property checks of the frozen equation.
- It **cannot** test c4 in the full sense (c4 needs v1.2 state and cohort exposure over time), and it **cannot**
  test c6. Any c4-shaped number it prints is a **worked example of the arithmetic, labelled SYNTHETIC/TOY**, and
  may not be reported as a c4 result.
- Its output is `toy/TOY_DESIGN_CHECK.md` + `toy/toy_results.csv`, both labelled SYNTHETIC/TOY.
- It runs **after** this file is hashed; its own hash and output hash go into `RUN_MANIFEST.json`.

## 13. What a v1.3 result cannot claim (frozen)

No evidence about Hong Kong, the Philippines, Cambodia or any country. No causal claim about returns, tutoring
effects, or welfare. No identification of cross-country shadow incidence (LOOP_CLOSEOUT exclusion 3). No
provider/fee/rent claim (exclusion 6). No claim that gate pressure and expected returns are separately identified —
in the feedback loop they are collinear by construction (a tighter gate mechanically lowers `π⁰` and raises both
`R` and `Δπ`), so the module reports their **joint** contribution and cannot attribute shares. No policy claim.
A PASS means "this declared parameterisation can produce this pattern through the declared mechanism" — nothing
more.


---

# PART 2 — `shadow_module/PRE_DECLARATIONS_S1_NOTE.md` (verbatim)

# PRE-DECLARATION S1 NOTE (controller) — pre-run clarification of the country-ordering check

**Written:** 2026-11-20, AFTER `PRE_DECLARATIONS.md` was frozen (sha256 `cf8c61cb…`) and BEFORE any v1.3 run.
**This note changes NO threshold and NO parameter.** It records a conflict in the on-disk shadow record that the
dispatch brief did not carry, and fixes how one frozen check is to be *read*. It is binding on the v1.3 run.

## What the on-disk record actually says about the country ordering

The dispatch brief described the expected ordering as "HKG high, PHL mid, KHM low". The on-disk figures do **not**
establish that ordering, because the three headline rates are from different stages and sampling frames:

| country | headline rate | stage / sample | status on disk |
|---|---|---|---|
| HKG | **85%** (c.2010/2011) | **senior secondary**; second-hand quotation; source itself says surveys are not statistically robust | `02_lit/COUNTRY_CARDS/HKG.md:15`; `04_data/TARGETS_SHADOW.csv` row "senior secondary" |
| KHM | **68.4%** (2012-13) | **Grade 9**, two-school case study (1 urban, 1 rural), not national | `02_lit/SHADOW_TARGETS.csv`; `02_lit/COUNTRY_CARDS/KHM.md:15` |
| PHL | **46.5%** (2010) | **all basic education**, single select-sample survey (574/1,235), not nationally representative | `02_lit/SHADOW_TARGETS.csv`; `02_lit/COUNTRY_CARDS/PHL.md:15` |

At face value these give KHM (68.4) **>** PHL (46.5), which contradicts "PHL mid, KHM low". The stages are not
comparable (senior secondary vs Grade 9 vs all-basic), so **no country ordering is identifiable from these rates.**

## How the frozen checks are to be read

1. **c4a (HKG D ∈ [0.75, 0.95]) is the only empirical anchor**, and it is a wide band deliberately (±10 pp) because the
   source is second-hand, senior-secondary-only and of low survey robustness. It is a **reproduction of a declared
   level**, not a validation of any real system.
2. **c4b (D*_HKG − D*_PHL ≥ 0.10; D*_PHL − D*_KHM ≥ 0.05) is a DECLARED SYNTHETIC-REPRODUCTION CHECK on the model's
   cohort-incidence statistic D\***, driven by observed out-of-school exposure (§7 cohort weights), **not** a claim that
   the on-disk headline rates order the countries that way. If it fails, the FAIL and the exposure-vs-demand channel
   decomposition are reported; it is not rescued.
3. **c3 ("near-zero at primary") is a structural/consistency check of the module** (no gate, no rank competition,
   `V_g0 = 0`), **not an empirical prediction**. Observed primary-stage tutoring — PHL 23.8%, KHM 41.3% — is **out of
   this module's scope** and is not explained by it; it remains a declared gap, not a hidden residual.
4. The declared ex-ante risk in `PRE_DECLARATIONS.md` §8 stands: the gate channel and the return channel can pull in
   opposite directions for KHM; the ordering, if any, is carried by **cohort exposure**, not by demand intensity.

**No run may begin until this note is in the module and the v1.2 panel exists** (c6's no-re-fit guard).
