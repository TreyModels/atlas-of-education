# DESIGN — v1.5 **BIMODAL-GATE** on the frozen v1.2/v1.3 stack (architecture; build-ready, **not built, not run**)

**`LABEL: SYNTHETIC` — declared-assumption design only. Not evidence about any country. No causal or direction claim.
C1–C4 not reopened. A3-D not re-tuned. HELD data stays HELD.** Thresholds live in
[`PRE_DECLARATIONS.md`](PRE_DECLARATIONS.md) (frozen); every parameter and its provenance in
[`PARAMETERS.csv`](PARAMETERS.csv); the build sequence in [`DRY_RUN_PLAN.md`](DRY_RUN_PLAN.md).

---

## 1. What problem this architecture solves

A3-D (EXP-2) wired household demand to the generator's **upper-school gate probability**, which the model makes
**≈0.999** (`SYNTHESIS_022.md:108`) — a gate that does not ration. A demand channel attached to a non-binding gate is
**inert by construction** (D124). The correct reading is **"the unrationed single-gate model cannot represent a
bimodal system"** — a model-specification failure, **not** "demand falsified".

v1.5 changes the **object the model can hold**, in two independent moves:

1. **A two-tier supply/demand structure** so that "seats untaken" and "gates contested" are both representable in
   one country-year — and so that the **binding** gate is the **credentialed job rung** (`p₄ ≈ 0.151`), not the
   school gate (V8).
2. **A declared cross-level accounting link** `upper_t ≤ κ·lower_{t−3}` (κ = 0.949, observed median, never fitted)
   built **into** the transition, because EXP-7 shows the pipeline does not exist in the generator and a post-hoc
   projection cannot make the upper level *inherited* (`repro_path_2026-11-20/FINDINGS.md:152-166`).

Plus one **theory rule**: the **one-way ratchet** — no reversal term anywhere (D125), tested only by construction.

### 1.1 What the frozen model already does — stated so the contrast is not overstated

v1.3 is **not** a world without spare capacity: at upper secondary 2024 it has **0.1418 of cohort spare adequate
places**, and its **job** gate binds hard (`p₄ ≈ 0.151`, V8). "Bimodal" is therefore **not literally absent** from
v1.3 — what is absent is:

1. a **declined-place object** — v1.3's `rationed` column is excess **demand**; spare capacity is an arithmetic
   leftover of a low `demand_share`, never a household that was offered a place and refused it;
2. **rationing at the school gate** — so a *declined place* and a *contested place* can never occur at the **same
   level** in the **same year** (check (a-iv): the `same_level` count is 0 in the single-gate arm);
3. a demand channel attached to a **binding** gate — the A3-D error (demand wired to `p ≈ 0.999`).

v1.5 is designed against exactly those three absences, and the pre-declaration says so (`PRE_DECLARATIONS.md` §6(a)).
It does **not** claim to discover spare capacity in a model that already had it.

---

## 2. Where v1.5 sits on the existing code (nothing is edited; a new file is built)

Base: `generator_v1_3/code/sim_v1_3.py` (`70ae8f0e…`), itself `generator_v1_2/code/sim_v1_2.py` (`61123aa9…`) +
the frozen shadow block. v1.5 is a **new** file `code/sim_v1_5_bimodal.py` that **imports the frozen modules
read-only** (`shutil.copy2` of the base into `code/base_v1_3_sim.py`, hash-verified — the v1.4 convention,
`generator_v1_4_demand/code/base_v1_3_sim.py` hashes `70ae8f0e…`) and layers the tier block on top. **No file under
`generator_v1_2/`, `generator_v1_3/`, `generator_v1_4_demand/`, `shadow_module/` or `repro_path_2026-11-20/` is
written** (`PRE_DECLARATIONS.md` §6(e) e-iii).

### 2.1 The one code path, two switches

```
simulate_country(cp, ..., bimodal=False, kappa_link=False)
    ├── per level L:  seats, q, Q, cls, demand, rationing, survival, completion   [v1.3 arithmetic when OFF]
    ├── NEW  tier_split(seats[L])            → K_H, K_O                          [bimodal ON only]
    ├── NEW  tier_choice(...)                → A_H, T_O, V_O, p_adv_H, queue_H    [bimodal ON only]
    ├── NEW  kappa_cap(adm_upper, comp_lower) → adm_upper                         [kappa_link ON only]
    ├── matching / rungs / wages / shadow     [v1.3, plus tier returns when ON]
    └── panel columns                          [v1.3 columns always; tier columns appended when ON]
```

`bimodal=False, kappa_link=False` ⇒ every new function is the identity and the panel **projected onto v1.3's column
set** is **byte-identical** to `47d4b082…` (E1). The switch must be a **single boolean read at exactly one place
per insertion point** — no scattered `if`s — so the guard is auditable (T-AUD-4).

### 2.2 Insertion points (exact anchors in `sim_v1_3.py`)

| # | anchor | what happens there now | what v1.5 inserts |
|---|---|---|---|
| **I1** | `state_shares()` `:609-637` | four-state utility comparison `U_school/U_both/U_work/U_neither` for a representative household | **unchanged** (the outside option). A new `tier_choice()` **calls** it to obtain `U_work, U_both, U_neither` as the refusal values; it never re-defines them |
| **I2** | after `out["seats"][:, t] = seats` `:757-780` | `q`, `Q`, class size from cohort/seat ratio | split `K_H, K_O`; tier qualities `Q_H = q_H_mult·Q`, `Q_O = q_O_mult·Q`; tier class sizes |
| **I3** | household demand block `:782-806` | `D_off, D_oa` from `state_shares` × eligibility | **bimodal ON**: `tier_choice()` over the 15-cell lattice produces `A_H, A_O, A_work, A_both, A_neither`; `D_off = A_H + min(A_O, K_O)`; **bimodal OFF**: the v1.3 lines run verbatim |
| **I4** | rationing block `:808-816` (`phys = min(phys_cap*seats, overage_cap*C)`) | official-age first, then over-age, remainder out of school | Tier H: `admitted_H = min(A_H, K_H)` by rank; Tier O: `T_O ≤ K_O` by the utility comparison (**no rationing needed at O — that is the point**); `V_O = K_O − T_O` written out |
| **I5** | survival/completion `:826-838` | `surv = surv_max·Q^θ`; `comp_coh = adm(t−dur)·surv` | per tier: `surv_H` from `Q_H`, `surv_O` from `Q_O`; completion = admission-weighted sum over tiers (only when ON) |
| **I6** | pools `:866-872` | `newpool = grads[L−1]·pool_mult + pool_retain·pools[L]` | **κ cap** on the upper entry cohort: `adm_upper ← min(adm_upper, κ·comp_lower_cohort)` (see §4); no other level |
| **I7** | matching `:896-947`, esp. the rung loop `:912-935` | rungs 3→0 hiring, `queue_r`, `rankf`, `E_r` update; rung-4 absorption `rung4_emp/rung4_demand` | Tier H **job gate**: the rung-4 slot is rank-rationed with the same rank/queue machinery; `p₄` reported; Tier O credential holders are **not** routed into rung 4 (declared: Tier O confers no credential rank) |
| **I8** | shadow block `:948-1000` | `D_sh` per gate g0–g4 from gate state | **unchanged equation and parameters**; shadow demand is **evaluated at the tier's gate state** — `D_H` at g2/g4, `D_O` at the open tier (`R≈1`) — and written as new columns only |
| **I9** | `build_panel`/`build_panel_v13` `:1003`, `:1465` | 67 / 89 columns | append tier + κ columns when ON; the A00 guard artefact keeps **exactly** v1.3's columns |

**Why these anchors.** They are the smallest set of points at which "who gets a place" is decided. Inserting at
demand (I3) without I4 would model **preferences** without **rationing** — the A3-D error in reverse. Inserting at
I4 without I6 would keep the upper level **stipulated** by its own block (EXP-7's `b2`). Inserting I6 without I2–I5
would clip a level the tier structure never produced (the post-hoc projection EXP-7 rules out).

---

## 3. Tier O — how **unfilled places** are represented (not a residual)

v1.2/v1.3 has no unfilled-seat object at all: `rationed` is **excess demand** (`D_off − adm_off`), and spare
capacity is only implicit in `seats − enrolment`. In v1.5 the unfilled place is a **first-class entity**:

```
K_O,L(t)         = (1 - h_share_L) · seats_L(t)                       capacity (declared split)
T_O,L(t)         = C_L(t) · Σ_i w_i · 1[ U_O,i,L(t) ≥ max(U_H,i,L refused, U_work, U_both, U_neither) ]
V_O,L(t)         = max(0, K_O,L(t) - T_O,L(t))                        UNFILLED places — an object
unfilled_share_O = V_O / K_O                                          the check-(a) statistic
```

Three design commitments that keep it from collapsing into a residual:

1. **It has its own equation.** `V_O` is computed from a **utility comparison per household cell**, not as
   `capacity − demand`. A household that ranks Tier H first and is refused at the gate gets a **second decision**
   (accept O or take the outside option); the refusal value is the *outside option*, not Tier O.
2. **It is reported as a level, a share and a take-up rate**, in `results/BIMODALITY_CELLS.csv` and the tier tabs
   (`tierO_capacity`, `tierO_takeup`, `tierO_unfilled`, `tierO_unfilled_share`, `tierO_takeup_share`).
3. **It cannot be reallocated.** `K_H` is a function of `seats` and `h_share` only; the audit **T-AUD-3** asserts
   `K_H` has no dependence on `T_O`/`V_O` (no free places move up a tier, no quality conversion, no carry-forward).
   A single reallocation line would convert the bimodal model back into a single gate with two labels.

**Why places can be unfilled at all.** Because the outside option is explicit and priced: for low-ability,
low-income cells the Tier O return (low `cred_prem_O`, `q_O_mult`-degraded survival) can sit **below the option
value of work** — the v1.2 finding that a low tier can be dominated by work is not a paradox here, it is the
mechanism. `w_work_free = 0` (T11) ensures the refusal is driven by **returns and costs**, not by a taste shim.

---

## 4. Tier H — rationing, rank, and the two gates it carries

### 4.1 The school gate

Candidates `A_H,L` (cells ranking H first) against `K_H,L` places, admitted by **declared rank**
`rank_score = 0.30·(y/ybar) + 0.70·ability` (S06):

```
admitted_H = min(A_H, K_H)          queue_H = max(0, A_H - K_H)
queue_ratio_H = A_H / K_H           p_adv_H = admitted_H / A_H  ≤ 1   (by construction)
p̂_adv_H(t) = p_adv_H(t-1)           declared one-year expectation lag (S07)
```

`p_adv_H < 1` **by construction** — the property A3-D lacked. Preferences respond to `p̂_adv_H` through the
expected-return term in `U_H` (`H_h · p̂ · G_H`), so demand pressure has something to press against; the queue is
an **output**, not an input.

### 4.2 The credentialed-job rung carries the demand (V8)

The model's binding queue is `p₄ = rung4_emp/rung4_demand ≈ 0.151` for the anchor type — **not** the ≈0.999 school
gate. Tier H therefore carries the job rung explicitly:

- The rung-4 slot is filled by **rank**, from Tier H credential holders (Tier O holders carry `cred_prem_O` and do
  not enter the rung-4 rank order — declared).
- `p₄` is a **separate reported object** from `p_adv_H`; the two are never substituted for one another.
  **This is the concrete correction of A3-D's 6.6× domain error** (`SYNTHESIS_022.md:108,398`).
- The **shadow** block's g4 gate keeps using the model's own wage gap and queue (`IMPLEMENTATION_NOTE.md` §3.3),
  unchanged; v1.5 only re-expresses *which* tier's candidates constitute the g4 queue.

### 4.3 Returns differ by tier (and only by the declared vectors)

`w_H = (Y/1000)·mult_r·(1 + cred_prem_H·r)·rankf_r`, `w_O` likewise with `cred_prem_O`; `cred_prem_H = 0.18`,
`cred_prem_O = 0.03` (T08/T09). `rankf_r` is the model's own rank factor (`rank_gain = 0.20`, v1.2) — **no new rank
parameter**. With `bimodal = OFF` the wage equation is **exactly** v1.3's single `cred_prem = 0.10`.

---

## 5. Sorting — implementation, and why it is not a fitted taste parameter

**The lattice.** 15 household cells = 5 income quintiles × 3 ability strata, joint weights `cell_weight` (S01,
row sums 0.20, mild positive income–ability association declared). Income `y_i = ybar_c·exp(0.80·z_q)`; ability
`a_i ∈ {0.25, 0.50, 0.75}`. Per country-year-level, `tier_choice()` evaluates the five states (H, O, work, both,
neither) per cell and aggregates by weight. Cost: 15 cells × 5 states × 4 levels × 56 years × 30 countries — a few
seconds (§`DRY_RUN_PLAN.md` §5).

**Utility (declared; childworld structure, our values):**

```
U_H,i,L = util(y_i - cost_H,L) + v_H,L + H_h · p̂_adv,H,L · G_H · 1[a_i ≥ a_gate] - risk_pen·(1 - p̂_adv,H,L)
U_O,i,L = util(y_i - cost_O,L) + v_O,L
outside = { U_work, U_both, U_neither }   from state_shares() — unchanged, no fifth state
choice  = argmax; ties → the outside option (declared tie-break, never a silent H)
```

**Why this is not a free taste parameter.**

1. `v_H,L = v0·decay^L` and `v_O,L = 0.45·v0·decay^L` — **one** vector, applied to **all** levels and **all** 30
   countries (T10). There is no per-level shim and no country branch; the audit T-AUD-1/2 fails the run if one
   exists (the mirror of shadow `c4c`, which VOIDs on any country-specific behavioural value).
2. `w_work_free = 0` is **held at zero** — the constant that A3-D tried to replace is not doing the work
   (`PRE_DECLARATIONS.md` §6 d-i).
3. **The level pattern is produced by three declared structural vectors** — quality by tier, cost by tier, returns
   by tier — plus the outside option; check (d-iii)/(d-iv) are ablations **on those vectors**, so a PASS cannot be
   obtained by a shim that the ablations do not move.
4. **Nothing is fitted.** No parameter in `PARAMETERS.csv` carries a `FITTED` label; the sensitive ones
   (`h_share, q_mult, cred_prem_H, cost_mult`) carry declared sensitivity grids and are reported under sensitivity.

**Rank and the credit constraint interact as declared.** Rank admits by income position **and** ability; cost_H is
paid from `y_i` through the concave `util`, so a poor high-ability cell can rank top but still be priced out — the
liquidity channel is in the utility form, not in a separate credit parameter (there is no credit-market series on
disk; declaring one would be invented structure).

---

## 6. The κ link and the ratchet — how they enter

### 6.1 κ (declared cross-level accounting link)

```
κ = 0.949   (observed median of the 8 PHL upper_t/lower_{t-3} pairs; sensitivity 0.960)
constraint: comp_uis_upper(t) ≤ κ · comp_uis_lower(t-3)          [the audited object]
internal:   adm_upper_cohort(s) ← min(adm_upper_cohort(s), κ · comp_lower_cohort(s))   [the sufficient form]
```

Entered at **I6** (the pool/admission step), **not** as a post-processing clip. Because upper completion at `t` is
`m·adm_upper(t−3)·surv_upper(t)` and `surv ≤ 0.995 < 1`, the admission cap implies the completion-level statement
(the `m` and the 3-year lag cancel), which is then **audited** cell-by-cell (E2-3: 0/53 violations). Only
**upper-secondary entry** is capped; `primary`, `lower`, `tertiary`, wages, rungs and the four-state block are
untouched (E2-1 asserts cell identity in all 6 720 rows).

**Declared consequence, before the run:** `0.949 × 67.4073 = 63.9695`, so upper 2024 is expected **≤ 63.97**,
≈11 pp below the observed 75.025 and outside the [73,77] band. This is EXP-7's `b2` carried into the model, **not**
a v1.5 discovery and **not** a reason to move κ.

### 6.2 The ratchet

Entered as **three absences**, not as a term (D125; `PRE_DECLARATIONS.md` §4): no reversal/restore term; shocks only
as the frozen declared inputs (`gnoise`, `hhnoise`); a path-created option set (`x_open` rungs once opened stay
open; `Tstate` non-decreasing). The tier block adds no exit/re-entry rule and the κ cap is a **monotone upper
bound** — it can only remove admissions, never add them, so it cannot act as a restoring force. Audit **R1**
searches the source for the reversal token list and requires **0 hits**; **R2** reports monotonicity
descriptively. **No reversal diagnostic is inferred** — the absence of a term is a construction fact, not a test of
"nobody ever goes back", which is **untestable on our data**.

---

## 7. What would be **built** vs what is only **declared** (no overclaiming)

| object | status |
|---|---|
| tier split `K_H/K_O`, unfilled `V_O`, queue `queue_H`, `p_adv_H`, `p₄`, tier returns/costs/quality | **would be built** (equations in §3–§4; parameters in `PARAMETERS.csv`) |
| κ admission cap + the completion-ratio audit | **would be built** (§6.1) |
| 15-cell sorting lattice and `tier_choice()` | **would be built** (§5) |
| shadow placement `D_H/D_O` | **would be built**, re-using the frozen shadow equation **unchanged** |
| checks (a)–(e), guards E1–E4, audits R1/R2 | **would be built** (`DRY_RUN_PLAN.md`) |
| **tier-specific exit cost** | **DECLARED ONLY** — noted for the Council, **not modelled, not tested** (D101 unchanged: no exit-cost layer until WT1 ∧ WT3 non-null) |
| "the model *explains* the PHL ceiling" | **NOT declared and not licensable** — the ceiling stays `UNABLE as to cause` (D63); v1.5 at most shows the model **can hold** the pattern |
| "demand responds to returns in the Philippines" | **NOT declared** — no causal/direction claim; the ablations are comparative statics of a synthetic model |
| any seat-utilisation or quality number for PHL | **NOT built** — HELD (§8.1 below) |
| the migration/remittance channel | **NOT built** — A3-D's declared-but-NOT-VERIFIED channel stays out (`lit/PUSH_PULL.md`: coefficient NOT VERIFIED) |

---

## 8. Data: the HELD DATA ASK and the declared proxies, with their distortions

### 8.1 HELD DATA ASK (recorded; **never fabricated**)

**True seat utilisation and quality are not on disk.** The ask (D124(d)), to be held until the user grants access:

1. **DepEd / CHED seats vs enrolment**, by level, track (SHS academic/TVL/sports/arts & design), and region;
2. **private / public shares** of enrolment and of provision by level and track (the WDI series below are national
   aggregates only);
3. **SHS voucher take-up** (number and share of voucher recipients, by track and region);
4. **capacity utilisation** — places offered vs places filled — which is the object Tier O's `V_O` would be
   validated against and which **has no on-disk proxy at all**.

**Corroborating evidence that this is genuinely blocked** (not an oversight):
`10_massification/data/STATE_CAPACITY.csv:2` — "number of public schools by year" = `DATA BLOCKED: deped.gov.ph 403;
DPWH 403; DepEd datasets page 403; Wayback 429`; `:3` — "classroom construction completed by year" =
`DATA BLOCKED: DPWH 403; DepEd facilities reports not public this pass`. The only capacity objects on disk are
**PTR**, **students-per-classroom** and **teachers**, which are **not** utilisation.

### 8.2 Declared proxies actually used (`DERIVED`; each with its distortion)

| proxy | value used | file:line | what it proxies | distortion (stated) |
|---|---|---|---|---|
| PHL out-of-school rate, upper-secondary | 2021 **24.969**, 2024 **22.884**, 2025 **23.714** % | `UNIVERSALIZATION_SERIES.csv:480,483,484` | the **upper bound** on "seats untaken" at upper-secondary age | OOS ≠ unfilled seats: it mixes no-place, no-demand, drop-out and migration; the model's `oos_rate` and `Tier O unfilled` are **different objects** and are reported separately, never equated |
| PHL enrolment vs cohort (completion, GER) | completion 1999–2024 (`:43-64`); GER upper 2018 **66.046** (`:296`) | same file | place-coverage / take-up **trend**, not level | completion is a **lagged-attainment** stock and **not** interchangeable with GER (V6: PHL upper completion/GER up to **1.094** in 2017); only the **shape**, never a level, is used |
| PHL private share, primary | **9.4803** % (2020) | `09_relations/data/panel_wdi_long.csv:20456` | order of magnitude of the **non-state** segment of Tier O | a **national aggregate**, no track/region split; says nothing about **quality** or **places**; used only to sanity-bound the declared `h_share` narrative, **not** as a parameter |
| PHL private share, secondary | **23.915** % (2020) | `panel_wdi_long.csv:31110` | same, secondary | same; and it is an **enrolment** share, not a capacity share |
| PHL PTR (high school, 2000) | **37** learners/teacher | `STATE_CAPACITY.csv:402` | congestion context for the declared quality path | PTR is **not** usable places (D81-5); the model's `Q` already uses `cohort/seat`, and PTR is **not** re-used as a quality parameter |
| PHL students per classroom (2010) | elementary **39**, JHS **54** | `STATE_CAPACITY.csv:403,404` | congestion magnitude | a **two-point** series; no utilisation, no vacancy, no track split |
| SHS policy dates (K-12 2013; free SHS tuition 2016) | — | `POLICY_TIMELINE.csv:16,18` | the declared build-out timing narrative | policy dates are **not** parameters in v1.5; the build-out path stays the frozen declared `seat_t50/seat_width` |

**Rule that binds the build:** *no seat-utilisation number and no quality series may be created to fill the HELD
gap.* If a run-time check wants a utilisation target, it is `UNDETERMINED`, not imputed.

---

## 9. Honesty bounds carried by every output

1. **D119 scope.** v1.3 levels are a **2021–2024 placement**, 24–37 pp low before 2021; **9/33** within ±5 pp;
   EXP-7 leg (a) = `ENDPOINT-ONLY`. Every v1.5 level statement inherits this and is written with the scope line.
2. **`m = 1.10` unchanged** (single declared measurement constant; check (d) of v1.2 still uses the cohort-flow
   series).
3. **`SYN00_PHL_LIKE` is not the Philippines.** It is the only country whose trait block is anchored on an observed
   PHL path; all 29 others are declared.
4. **A synthetic PASS is non-diagnostic unless the ablations fail** (D81): (a-iv), (d-iii), (d-iv) are inside their
   checks for exactly this reason.
5. **Language:** never "demand falsified"; the label is **"the unrationed single-gate model cannot represent a
   bimodal system"**. No causal claim, no direction claim, no policy claim, no forecast.
6. **C1–C4 not reopened; WT/DT cells not re-run; A3-D not re-tuned; the two papers remain scored rivals with no
   empirical footprint** (D99–D105).

---

## 10. Known risks of this design (declared, not discovered later)

- **R-a. The coexistence in (a) is partly arithmetical** given `h_share`. Mitigation: (a) is labelled a
  **representation** check with the arithmetic printed in `PRE_DECLARATIONS.md` §9, and the diagnostic weight sits on
  magnitude + monotone sensitivity + the A01 exact-zero.
- **R-b. The κ cap may make the tier block look decorative for the upper endpoint** (the cap binds and sets the
  level). Mitigation: (d) is scored on **responsiveness ablations** (child wage, Tier O quality), not on moving the
  endpoint; if they do not move, (d) is `MIXED` and the report says the pattern is **pipeline-stipulated**.
- **R-c. `p_adv_H` and the queue may be dominated by the declared `h_share`** rather than by household behaviour.
  Mitigation: the `h_share ± 0.10` sensitivity grid is reported beside every queue/unfilled statistic.
- **R-d. Tier O may take up nothing at all** (`V_O/K_O → 1`). That is a **legitimate FAIL** of (a-i)'s spirit and
  will be reported as such — an unfilled-share of 1.0 means the open tier is not a schooling option at all, which is
  a different (and informative) failure than a bimodal equilibrium.
- **R-e. The 15-cell lattice is coarse.** Declared, not estimated; it is the smallest lattice that carries income and
  ability separately. No finer lattice may be substituted after results.
