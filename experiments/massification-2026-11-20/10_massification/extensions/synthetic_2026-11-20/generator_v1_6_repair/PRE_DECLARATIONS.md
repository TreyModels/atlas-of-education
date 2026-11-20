# PRE_DECLARATIONS — EXP-14 **V16-REPAIR** (the repaired bimodal generator)

**`LABEL: SYNTHETIC` for every generator object. `LABEL: OBSERVED` for every PHL series. `LABEL: DECLARED` for
every behavioural assumption. This is a new cell with a new predeclaration. It is NOT an independent test of A5 —
its parameters are post-observation — it does NOT re-run, re-score or rescue v1.5 (v1.5's verdict string stands
permanently), it re-opens no C1–C4 claim, it makes no causal and no direction claim, it fits nothing to the known
PHL outcome, and it does not license the phrase "demand falsified" in any paraphrase.**

Frozen before the scored run: this file, `PARAMS.md`, `code/base_v1_3_sim.py` (verbatim copy of the frozen v1.3
code), `code/build_v16.py`, and the generated `code/sim_v1_6_repair.py`. The built code embeds the sha256 of this
file and **refuses to run on any mismatch**; it also parses the machine-readable block in §5 and refuses if any
declared parameter differs from the code.

Two predeclaration inputs were required by D136 before EXP-14 could be frozen, and both landed on disk:

- **EXP-11 KAPPA-FWD** — `kappa_fwd_2026-11-20/PRE_DECLARATIONS.md`, predecl sha256 `bda79ac4…`, verdict
  **`WINDOW-ONLY`** (D138). Consequence carried here: κ **may not be a forward constraint** (Rule R6).
- **EXP-13 LOWER-DEF** — `lower_def_2026-11-20/PRE_DECLARATIONS.md`, predecl sha256 `0ab3a90e…`, verdict
  **`JOINT`** (D140). Consequences carried here: target provenance, both lower channels together, `m` frozen at
  1.10, the lower target scored on **2021 not 2024**, the survival ceiling stated, the clip boundary declared
  (Rule R7).

---

## 1. What this cell is, and what it is not

**Question (EXP-14, first-order link: schooling + cohort flows + markets, at the level).** Can the two-tier class
hold the **coexistence** *and* a **level pattern**, once (i) the κ link is bounded at the right object, (ii) Tier O
quality acts on **take-up** rather than on survival, and (iii) the outside option is tested on a margin it can move?

**What it is.** The repair of the frozen v1.5 `BIMODAL-GATE` implementation against the four defects ruled in
SYNTHESIS_023 §5 / D134, on **declared parameters**, scored on the **observed path** (33 PHL observed cells) with
the voting rule and thresholds fixed in §6 below, plus the guards in §7.

**What it is not.**

1. **Not "v1.5 passing".** v1.5's verdict (`a=MIXED; b=FAIL; c=MIXED; d=FAIL; e=MIXED; ALL=FAIL`) is permanent and
   is not re-scored. This is a new cell with new guards on the same base instrument.
2. **Not an independent test of A5.** The A5 block's parameters were declared after the PHL record was observed;
   nothing here can adjudicate A5 as a theory. It can only report what the declared class does.
3. **Not a re-tune.** No parameter, threshold, band, year set, arm definition or verdict word is chosen by
   reference to a level bar or to the observed path. The parameter values are carried from the frozen v1.5
   declaration (T01–T15) or from the frozen v1.3 declaration; the single re-location of a value (0.55) is a
   *margin* change mandated by D134(3), not a value change (Rule R4).
4. **Not a scaling-repair iteration** (R27 untouched), **not a re-tune of A3-D** (KILLED, D130), **no C1–C4
   reopening**, **no direction claim**, **D63 stays `UNABLE as to cause`**.
5. **Not a data experiment.** No new data is read; HELD data stay HELD and are named in §10.

---

## 2. EXP-14 block, **verbatim** (SYNTHESIS_023 §6.4, "6.4 EXP-14 — **V16-REPAIR**: the repaired generator, on declared parameters, scored on the observed path (rank **#4**)")

> 1. **First-order link (schooling + cohort flows + markets, at the level).** Whether the two-tier class can hold the
>    **coexistence** *and* a **level pattern**, once the κ link is bounded at the right object, Tier O quality acts on
>    **take-up** rather than on survival, and the outside option is tested on a margin it can move.
> 2. **What changes if positive vs negative.** **Positive** (representation holds **and** the path bar is met) → the class
>    becomes a **candidate level model** for PHL and the next question is what sets κ and the tier share. **Negative**
>    (representation holds, path fails) → the class is recorded as a **representation-only** capability and the ceiling
>    remains **UNATTRIBUTED** (a stronger, cleaner negative than v1.5's). **Falsifier fires** → no successor is built this
>    phase and the level question is closed at `UNABLE`.
> 3. **Why it is not a niche.** It is the only path by which the user's structural requirement (D124) can become a model
>    that also reproduces the record, and the batch's own decomposition shows the pattern failure is attributable to the
>    **tier block**, not to the pipeline link (arm A01 alone: primary **100.0**, lower **85.87**, upper **55.66**).
> 4. **Data on disk (no DATA ASK).** Frozen `generator_v1_5_bimodal/code/sim_v1_5_bimodal.py`; frozen v1.3/v1.5 panels;
>    `UNIVERSALIZATION_SERIES.csv` for the **33 observed cells**; `PARAMETERS.csv` for the declared prov (all parameters
>    labelled DECLARED / DERIVED / CONVENTION, **none FITTED**). **HELD** (named, unused): DepEd/CHED seats-vs-enrolment,
>    private/public shares, SHS voucher take-up, capacity utilisation.
> 5. **Threshold + falsifier (fixed before the run).** **Primary bar: EXP-7's own, unchanged — ≥ 17/33 observed cells
>    within ±5 pp**, plus crossing years within **±5 y** (D34/A6). Reported, **not verdict-bearing**: upper 2024, the
>    `[55,85]` stall band, and the ratio audit. **Four binding design obligations** (§5): **(i)** κ bounded in completion
>    units with the survival allowance explicit and **per-system** for the four declared systems (single **0.949
>    labelled PHL-derived default** for the other 26 — never described as a per-system value); **(ii)** the guard restated
>    as a **counterfactual identity** + propagation ledger + one-way order; **(iii)** Tier O quality at the **return/
>    take-up** margin, any survival penalty separately declared; **(iv)** the child-wage shock tested in **A10** with a
>    sign derived before the run. **Falsifier: `FAIL-RE-FIT` if (a) any parameter is chosen by reference to the 17/33
>    bar or the `[55,85]` band, (b) the A00 arm is not byte-identical to `47d4b082…`, or (c) a within-year feedback from
>    the capped economy into same-year admission is found and not declared.**
> 6. **Closed-claim check.** A **new cell** with a new predeclaration; **v1.5's verdict stands and is not re-scored**
>    (no a–e check is re-frozen); **not** an independent test of A5 (its parameters are post-observation) — the
>    predeclaration must say so in its first paragraph; **not** a scaling-repair iteration (R27 untouched); **not** a
>    re-tune of A3-D (KILLED); no C1–C4 reopening; no direction claim; D63 stays `UNABLE`.
> 7. **Cost / rank.** **Medium–large** (build + run + audit). **Rank #4** — the largest single information gain but the
>    only member whose design depends on two others (KAPPA-FWD's verdict on forward-usability; LOWER-DEF's target), so it
>    is ranked below them and must not be predeclared before both return.

**Copied verdict from EXP-7 (the bar, unchanged):** `PATH-REPRODUCED` iff **≥ 17/33** observed cells within **±5 pp
inclusive**; `ENDPOINT-ONLY` / falsifier iff **≤ 16/33**. Sources: `repro_path_2026-11-20/PRE_DECLARATIONS.md`
§"Threshold + falsifier", `results/REPRO_PATH_RESULTS.csv` (9/33 as scored; **not re-scored here**).

---

## 3. The binding obligations, restated as rules (D134, D138, D139, D140)

### 3.1 D134(1) — bound the right object (Rule R1)

> "(i) **Bound the right object.** The constraint must be stated in **completion units** with the survival allowance
> explicit — `adm_upper(t) ≤ κ · comp_lower(t−3) / surv_upper(t)`, or equivalently a declared endpoint object
> `κ · lower · surv` — so that the audited completion ratio and the enforced object are the **same object** and the
> "≈ κ·lower" reading is not off by `1/surv` (V12: **8.31 pp**). **The predecl must say which object it bounds and
> which number it expects**; the v1.5 §9 omission may not recur."

| rule | binding text |
|---|---|
| **R1** | **Bounded object.** The κ constraint is enforced on the **upper-secondary official-age admission rate** `a_u(s) = admitted_official_upper(s) / cohort_upper(s)` — a **rate**, one register, declared once. The bound is set so that the **completion-unit object** `e(s) = m · a_u(s) · surv_upper(s)` satisfies `e(s) ≤ κ · comp_uis_lower(s−3)` **by construction**, with `m = 1.10` and `surv_upper(s)` the model's own survival law at `s`. **Enforced object = audited object = `e(s)`; the audit below re-computes `e(s)` from the panel and must return 0 violations.** The realised 3-year-later completion object `comp_uis_upper(s+3)` is **also** reported, with the `surv(s)→surv(s+3)` drift quantified, because that is the object EXP-7's leg (b) audited; the two objects are never conflated. |

### 3.2 D134(2) — declare a legitimate projection order (Rule R2)

> "(ii) **Declare a legitimate projection order.** The propagation cannot be removed, only **ordered and audited**: the
> cap is applied at the upper entry; graduates then feed the tertiary eligibility pool, the matching pool and growth;
> capacity and gates for **t+1** read the economy. The repair must ship a **propagation ledger** — every column that
> moves, its mechanism, and its sign relative to the cap — and must show **one-way** propagation (no within-year
> feedback from the capped economy back into the *same-year* school admission of any level). **If a within-year feedback
> exists, the cap is not a projection and the repair must say so.**"

| rule | binding text |
|---|---|
| **R2** | **Declared projection order (the order the code executes).** Within year `t`: **(O1)** capacity/seats from the declared lagged supply rule (`seat_lag`), then `q`, `Q`; **(O2)** demand and admission at **all four levels** from the **carry-in state of `t−1`** (pools, admission history, graduation history) and this-year exogenous inputs only; **(O3)** graduates and completion from admissions at `t−DVEC` × survival at `t`; **(O4)** tertiary eligibility pool / matching / formal employment / wages / growth at `t` from `t`'s graduates and `t−1`'s labour-market state; **(O5)** capacity and gates for **`t+1`** read the economy at `t`. A **propagation ledger** is emitted for every panel column that moves (§7.4), with mechanism and sign. A **static order audit** verifies that the admission region (O2) reads **no** variable assigned by the economy region (O4) in the same iteration; hit count must be **0**. |

**Declared within-year dependencies (the answer R2 demands).** Two exist and are declared rather than removed silently:

- **(W1) Tier-O take-up is an equilibrium in the same year as admission.** Unfilled Tier O places `V_O` are the
  *primary object* of the representation check; the admission of a level depends on the same-year demand/take-up
  computation **at that level**. This is an intra-level market clearing, not feedback from the capped economy.
- **(W2) Tertiary tier composition.** In v1.5 the tertiary tier *composition* inherited the **same-year** upper-secondary
  choice shares (a carry-forward disclosed in D131 post-run disclosures (iii)). **The repair removes this**: the tertiary
  composition inherits the upper-secondary tier shares of the **entry cohort** (`t−DVEC[2] = t−3`), which is the cohort
  that actually graduates at `t`. After this fix, **no same-year quantity crosses from one level's admission into another
  level's admission.** This is the only design change made under R2 and it is declared as such (TUNE_LOG C4).

**No within-year feedback from the capped economy into same-year admission exists.** The κ arm's cap enters the year at
exactly one point (upper official-age admission, O2) and no same-year decision is recomputed after it.

### 3.3 D134(3) — counterfactual identity, not panel identity (Rule R3)

> "(iii) **Restate the guard as a counterfactual identity, not a panel identity.** The test is: feed **A01's upper
> admission vector** into the **A00 accounting** and reproduce A01 cell-for-cell. That is the identity that actually
> certifies "the link changed nothing except through the declared channel". Alongside it, keep two cheap exact checks
> that V11 shows *do* hold: **primary and lower schooling columns cell-identical** (`completion_uis`, `enrolment`,
> `admitted_official`, `demand_official`, `teachers`, `ptr`, `ger`), and **tertiary admission moving only through the
> eligibility pool** (non-increasing when the cap binds). **A whole-panel identity guard must not be re-frozen.**"

| rule | binding text |
|---|---|
| **R3** | **Counterfactual identity.** Arm `A00CF` = A00 accounting with **A01D's upper official-age admission vector injected** at the same point (O2) and nothing else. `A00CF` must reproduce `A01D` **cell-for-cell on every column of the 89-column v1.3 panel** (6 720 rows × 89 columns, exact string equality). **Two exact checks** are also scored: (i) primary and lower-secondary schooling columns (`completion_uis`, `enrolment`, `admitted_official`, `demand_official`, `teachers`, `ptr`, `ger`) cell-identical between A01D and A00; (ii) tertiary admission moves **only** through the eligibility pool and is **non-increasing** wherever the cap binds. **No whole-panel identity guard is re-frozen.** Rationale (D134): a whole-panel identity is arithmetically unsatisfiable for any binding link. Note: `A00CF` is a **guard arm**, not a projection; its numbers are never reported as results. |

### 3.4 D134(3) — Tier O quality at the return/take-up margin (Rule R4)

> "(3) **Tier O quality collapse — re-declare the mapping, do not search the grid.** … Repair: locate the discount at the **return/take-up** margin; any retained survival penalty declared separately with its own value/justification/sensitivity; no parameter chosen by reference to a level bar (grid search landing on a passing cell = FAIL-RE-FIT); **retire the (b) family for the successor** in favour of EXP-7's observed-cell bar (≥17/33 within ±5 pp) plus ±5 y crossings."

| rule | binding text |
|---|---|
| **R4a** | **The quality discount acts at the return/take-up margin.** The open tier's expected return in the declared utility block is its schooling value `v_O`. The declared quality multiplier **`q_O = 0.55` (PARAMETERS.csv T05, carried unchanged in value)** now enters `U_O` **multiplicatively on `v_O`** — `U_O = util(y − cost_O) + q_O · v_H` — and **nowhere else**. Cost, the outside option, admission rank and **survival** are untouched by `q_O`. |
| **R4b** | **One discount, one place.** v1.5 applied **two** discounts to one A5 statement: `v_tier_scale = 0.45` (`v_O = 0.45 v_H`, T10) in the utility **and** `q_O = 0.55` (T05) on survival. The repair keeps **one**: `v_tier_scale` is **retired** for this cell and `q_O = 0.55` is carried to the return margin. (Net effect on the open tier's utility vs v1.5: `0.55 v_H` instead of `0.45 v_H`.) A **dual-discount variant** (`q_O = 0.55` on the return **and** `v_tier_scale = 0.45` retained) is run as a **declared, non-verdict-bearing** sensitivity so that the double-count is visible, not hidden. |
| **R4c** | **Retained survival penalty: declared separately.** The repaired generator retains **no** tier survival penalty: `surv_pen_H = surv_pen_O = 1.000`. **Justification (written before the run):** A5 places Tier O's defect in the **return** ("low quality and low return; take-up is an equilibrium"); no measured tier-conditional survival differential exists on disk (capacity utilisation and seats-vs-enrolment are HELD, §10); and v1.5's survival multiplier set the system's level with nothing observing it. **Own sensitivity:** a retained penalty `surv_pen_O ∈ {1.00, 0.95, 0.90}` is run in arm A10 as a **separate, non-verdict-bearing** arm, and any level statement under it is reported as conditional on that declared penalty. |
| **R4d** | **(b) family retired.** No check in this cell uses `primary 2024 ≥ 92`, `upper 2024 ∈ [55,85]`, `[73,77]`, or any level band. The successor's level test is **EXP-7's observed-cell bar** (§6.1) plus the **±5 y** crossings (§6.2). |

### 3.5 D134(2) — the child-wage re-specification (Rule R5)

> "(2) **Child-wage sign — the test was structurally unfirable.** … re-specify the object, not the bar: test it where the constraint is slack — **arm A10 (bimodal ON, κ OFF)** — with a declared sign on the **upper completion** object, and in the capped arm test it on the **pre-cap** object (`demand_official` / `A_H` / the queue), with a declared sign **derived from the declared utility block before the run**, and report the capped-arm completion response as a **composition effect**, non-verdict-bearing. **A completion-level sign test under a binding cap must not be re-frozen.**"

| rule | binding text |
|---|---|
| **R5a** | **Shock.** `w_child × 1.10` (the declared country trait, all 30 countries, same draws; no other parameter moves). |
| **R5b** | **Verdict-bearing leg (A10, κ OFF).** Object: `completion_uis` upper-secondary, `SYN00_PHL_LIKE`, **2024**. **Declared sign: NEGATIVE.** Derivation from the declared utility block, written before the run: `earn = 0.32 · AGE_W[L] · max(w_child/0.32, 0.55·farm)` enters `U_work` (and, through `0.5(1+compat)·earn`, `U_both`); a 10 % rise in `w_child` raises the outside-option utilities for every cell with `w_child/0.32 > 0.55·farm`, so the schooling take-up share and therefore `T_O` and the upper admission rate can only fall or stay equal; `completion_uis = 1.10 · a_entry(t−3) · surv(t)` is non-decreasing in `a_entry` with `surv` unchanged by `w_child`. Therefore **Δ ≤ 0**, with a strict inequality required for a pass (**Δ < 0**). The old magnitude bar (`≤ −2.0 pp`) is **retired with the old object**; the magnitude is reported, non-verdict-bearing. |
| **R5c** | **Capped-arm leg (A01D, κ ON — diagnostic arm).** Object: the **pre-cap** quantities `demand_official`, `A_H` and the Tier-H queue at upper-secondary, 2024. **Declared sign: NEGATIVE** for `demand_official` and `A_H`, **POSITIVE** for `queue_H = max(0, A_H − admitted_H)` **only if** the cap binds (admission is fixed by the cap, so a fall in `A_H` cannot raise the queue; a fall in `A_H` above `K_H` leaves the queue unchanged). Declared: `Δdemand ≤ 0`, `ΔA_H ≤ 0`, `Δqueue ≤ 0`. The **capped-arm completion response** is reported as a **composition effect** (H/O mix × survival) and is **non-verdict-bearing**. No completion-level sign test is scored under a binding cap. |

### 3.6 D138 — κ is WINDOW-ONLY (Rule R6)

> "**Consequence for V16-REPAIR: κ may NOT be a forward constraint — only a declared within-window trajectory (never extrapolated) or it must be dropped; the per-system register (D133) remains the descriptive record, not a projection input.**"

| rule | binding text |
|---|---|
| **R6** | **κ is dropped from the projection.** The **scored arm A10 has `kappa_link = FALSE`**: no κ constraint is enforced on the projection, and no κ value enters any scored number. κ survives in this cell only as **(i)** the declared descriptive register (`κ = 0.949` PHL; 0.9898 KOR; 0.5950 KHM; 0.7222 CHN, D133) and **(ii)** a **diagnostic arm `A01D`** that exists solely to (a) supply the upper admission vector for the counterfactual identity R3, (b) exercise the completion-unit bound of R1 so the enforced object is auditable, and (c) host the pre-cap child-wage leg R5c. **`A01D` is not a projection, is not scored, and may not be cited as a forward κ result.** The single 0.949 labelled "PHL-derived default" is used for the other 26 synthetic countries in that diagnostic only and is **never described as a per-system value**. |

### 3.7 D139 — phys_cap sensitivity (Rule R8)

> "**CONSEQUENCE: A10/D62 `capacity buys the floor` must be restated as CONDITIONAL on the declared crowding convention; … V16 must report the `phys_cap` sensitivity.**"

| rule | binding text |
|---|---|
| **R8** | The declared `phys_cap = 1.15` crowding allowance is **not re-chosen**. The scored arm runs at **1.15**; the sensitivity `phys_cap ∈ {1.00, 1.05, 1.08, 1.15, 1.22, 1.30}` is run in arm A10 and **reported in full** (`results/phys_cap_sensitivity.csv`). Every statement about the floor is reported as **conditional on the declared 1.15 convention**. |

### 3.8 D140 — the lower-series and register fixes (Rule R7)

> "**V16 must first fix:** target provenance (80.76 internal-consistency vs observed 80.896, +0.136 pp), **both lower channels declared together**, m frozen at 1.10, **scored on 2021 not 2024**, survival ceiling stated, clip boundary declared."

| rule | binding text |
|---|---|
| **R7a** | **Target provenance declared in both registers.** The lower-series target is reported twice: **80.76 pp** = `upper 2024 (untiered A00) / 0.949` — an **internal-consistency** number (the value the κ chain would require of the model's own untiered upper series), and **80.896 pp** = the **OBSERVED** PHL 2021 lower-secondary completion used as the compared cell. The difference is **+0.136 pp** (observed − internal). The **observed-path score uses 80.896**, i.e. `UNIVERSALIZATION_SERIES.csv`, never 80.76. |
| **R7b** | **Both lower channels declared together, at 2021.** The lower-secondary shortfall is reported as **two channels** — **rationing** (the entry gate: `demand_official` vs `admitted_official` at the 2018 entry cohort, i.e. `1 − admission rate`) and **survival** (`surv_lower(2021)`), with the **convention factor `m = 1.10`** displayed as the third, frozen multiplier. The D140 equal-split shares (**rationing 49.30 % / survival 50.70 %**, `JOINT`) are carried as the declared reading; the alternative literal-order reading (`SURVIVAL-CARRIED` at 50.70 %) is reported alongside. No channel is mentioned without the other. |
| **R7c** | **m frozen at 1.10.** `m = meas_completion_factor = 1.10`, a **CONVENTION**, not a conversion. Checked in every cell: `completion_uis / completion_cohort = 1.10 ± 1e-9` (6 720/6 720 cells required). No statement may say "m converts X to Y". |
| **R7d** | **Scored on 2021, not 2024.** The lower target comparison is the **2021** cell (the κ-chain year). 2024 lower is reported as a companion only. |
| **R7e** | **Survival ceiling stated.** `surv_max(lower) = 0.91`; the declared survival law is `surv = surv_max · Q^θ` with `θ = 1.0` for the first three levels, so the **lower ceiling at 2021 is 0.784589** (D140). The model's 2021 lower survival is reported against it. |
| **R7f** | **Clip boundary declared.** `survival ∈ [0.02, 0.995]`; `completion_uis`, `completion_cohort` ∈ [0, 1]; `q_O`-adjusted utilities are unclipped; `p_adv_H ∈ [0.01, 0.999]`; `ger ∈ [0, overage_cap·100]`; the admission rate is bounded by `min(1, phys/cap)`. The number of scored cells **at a clip boundary** is reported (target 0; a nonzero count is a finding, not a rescue). |

---

## 4. Arms — every leg names its arm by its **full switch tuple** (D134(4))

Switches: `bimodal` (tier block ON/OFF), `kappa_link` (κ constraint in completion units ON/OFF), `tier_surv` (per-tier
survival mapping — the **v1.5** defect — ON/OFF), `v15_recon` (v1.5-faithful reconstruction: `v_O = 0.45 v_H`,
duplicated demand object, same-year tertiary carry-forward), `inject_upper` (counterfactual replay), `w_child×1.10`.

| arm | bimodal | kappa_link | tier_surv | v15_recon | other | role |
|---|---|---|---|---|---|---|
| **A00** | OFF | OFF | OFF | OFF | — | no-re-fit guard: must equal v1.3 `47d4b082…` |
| **A10** | ON | OFF | OFF | OFF | — | **SCORED** — the repaired generator on declared parameters (κ dropped per D138) |
| **A11V15** | ON | OFF | ON | ON | — | v1.5-equivalent **reconstruction** (diagnostic; reconciliation only, never scored) |
| **A01D** | OFF | ON | OFF | OFF | — | κ diagnostic (R1 object + R3 vector source + R5c host). **Not a projection.** |
| **A00CF** | OFF | OFF | OFF | OFF | inject_upper = A01D | counterfactual identity guard (R3) |
| **A10W** | ON | OFF | OFF | OFF | `w_child×1.10` | child-wage A10 re-spec (R5b) |
| **A01DW** | OFF | ON | OFF | OFF | `w_child×1.10` | child-wage pre-cap object (R5c) |
| **S_qO_x** | ON | OFF | OFF | OFF | `q_O = x`, x ∈ {0.40, 0.55, 0.70, 0.85, 1.00} | declared q_O sensitivity (non-verdict-bearing) |
| **S_survpen_x** | ON | OFF | OFF* | OFF | `surv_pen_O = x`, x ∈ {0.95, 0.90} | retained-penalty sensitivity (R4c; non-verdict-bearing) |
| **S_dual** | ON | OFF | OFF | OFF | `q_O = 0.55` ∧ `v_tier_scale = 0.45` | double-count disclosure (R4b; non-verdict-bearing) |
| **D1_survonly** | ON | OFF | ON | OFF | `q_H_mult = q_O_mult = 1.0`, `v_O_scale = 0.45` | decomposition: v1.5's `v_O` with the survival multipliers REMOVED (diagnostic; non-verdict-bearing) |
| **S_hshare_pm** | ON | OFF | OFF | OFF | `h_share ± 0.10` (two arms) | tier-share sensitivity |
| **S_physcap_x** | ON | OFF | OFF | OFF | `phys_cap = x` (§3.7) | D139 floor sensitivity |
| **S_kappa0960** | OFF | ON | OFF | OFF | `κ = 0.960` | declared κ sensitivity (diagnostic) |

\* `S_survpen_x` applies the retained penalty as an **explicit survival multiplier on the untiered law**
(`surv_O = surv_O_untiered · x`, `surv_H` untouched), which is *not* the v1.5 mapping (`Q_O = q_O·Q`) and is declared as
such: it is the "what if a conditional survival penalty were imposed" sensitivity, not a re-run of v1.5.

**Decomposition arms (declared before the run).** `A11V15`, `D1_survonly` and `A10` differ in exactly two declared
objects: (i) the per-tier survival multipliers (`q_H_mult`, `q_O_mult`) and (ii) the open tier's return scale
(`v_O = 0.45 v_H` in v1.5 / `D1_survonly` vs `v_O = q_O v_H = 0.55 v_H` in A10). Reporting the three arms side by side
is how §5 of FINDINGS answers "which obligation changed what"; none of the three is used to choose a value.

**Scored arm = A10.** Every number in `results/v1_6_checks.csv` that is verdict-bearing is computed on **A10** unless
the row names another arm in its `arm` field. A01D/A11V15/CF/sensitivity numbers are diagnostic and are marked as such.

---

## 5. Declared parameters (authoritative: `PARAMS.md`; provenance codes DECLARED / DERIVED / CONVENTION, none FITTED)

Carried unchanged from the frozen v1.5 declaration (`PARAMETERS.csv` T01–T15, S01–S03) or from the frozen v1.3
declaration (`generator_v1_3/PARAMS.md`). The only change is the **margin** at which `q_O = 0.55` acts (Rule R4a/R4b).

```json
{"seed": 20261120,
 "base_code_sha256": "70ae8f0eef83358493dad3d3feb2d6a8841c4bb6fad3966627f4eed70e2a9877",
 "v13_panel_sha256": "47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3",
 "measurement_factor": 1.10,
 "kappa_diagnostic": 0.949, "kappa_lag": 3,
 "h_share": [0.15, 0.28, 0.40, 0.50],
 "cost_H_mult": 1.60, "cost_O_mult": 0.03,
 "q_O_return": 0.55, "v_tier_scale": null,
 "surv_pen_O": 1.00, "surv_pen_H": 1.00,
 "H_h": 20.0, "a_gate": 0.40, "risk_pen": 0.20, "sigma_tier": 0.80,
 "ability_grid": [0.25, 0.50, 0.75],
 "cell_weight": [[0.10,0.07,0.03],[0.08,0.08,0.04],[0.06,0.09,0.05],[0.04,0.09,0.07],[0.02,0.07,0.11]],
 "rank_w_income": 0.30, "rank_w_ability": 0.70,
 "padv_clip": [0.01, 0.999],
 "obs_bar": {"n_cells": 33, "min_cells": 17, "tol_pp": 5.0},
 "crossing_tol_y": 5,
 "crossing_thresholds_pp": {"primary": 90.0, "lower_secondary": 90.0, "upper_secondary": 90.0},
 "phys_cap_baseline": 1.15,
 "phys_cap_grid": [1.00, 1.05, 1.08, 1.15, 1.22, 1.30],
 "qO_grid": [0.40, 0.55, 0.70, 0.85, 1.00],
 "survpen_grid": [1.00, 0.95, 0.90],
 "child_wage_mult": 1.10,
 "lower_target_internal_pp": 80.76,
 "lower_target_observed_pp": 80.896}
```

**Parameters carried from v1.5 and their v1.5 provenance (unchanged values):** T01 `h_share = (0.15, 0.28, 0.40, 0.50)`
(DECLARED — Tier H share of adequate places by level); T05 `q_O = 0.55` (DECLARED — Tier O quality multiplier; **new
margin: return/take-up**); T06 `cost_H_mult = 1.60`, T07 `cost_O_mult = 0.03` (DECLARED); T10 `v_tier_scale = 0.45`
(**RETIRED for this cell**, R4b); T11 `w_work_free = 0` (DECLARED, audited); T12 `a_gate = 0.40`, T13
`risk_pen = 0.20`, T14 `H_h = 20.0` (DECLARED); S01 `cell_weight`, S02 `z_q`, S03 `sigma_tier = 0.80`, S04
`ability_grid` (DECLARED); S06 `rank_w_income = 0.30`, `rank_w_ability = 0.70`; S08 `padv_clip = (0.01, 0.999)`;
K01 `κ = 0.949` (DERIVED — observed PHL median, **diagnostic only**); `m = 1.10` (CONVENTION, frozen).

**The rule that fixes the parameters, stated before the run (R4d):** every parameter above has a value fixed by the
frozen v1.3/v1.5 declarations or by an observed median, **before** any v1.6 output exists. No parameter is chosen,
rescaled, or selected from a grid by reference to any level, any observed cell, the 17/33 bar, or the `[55,85]` band.
The declared grids are **sensitivities around fixed values**, and the **scored value is the pre-declared one**. A grid
cell that passes the bar is reported as a sensitivity, never adopted: adopting it would be `FAIL-RE-FIT`.

---

## 6. Scoring rule (fixed before the run)

### 6.1 Primary bar — observed-path count (EXP-7's own, unchanged)

- **Cells.** The **33** observed year×level cells for `SYN00_PHL_LIKE`, derived at run time from
  `data/UNIVERSALIZATION_SERIES.csv` (indicator `completion_<level>`, `iso3 = PHL`, non-missing value, year inside the
  panel window), **not** hard-coded: **11 primary** (1999, 2000, 2004, 2008, 2010, 2013, 2017, 2021, 2022, 2023, 2024),
  **11 lower-secondary** (same years), **11 upper-secondary** (1999, 2000, 2003, 2004, 2008, 2010, 2013, 2017, 2022,
  2023, 2024). No imputation, no nearest-year substitution; a missing synthetic cell stays `MISSING` in the denominator.
- **Statistic.** `d = 100·completion_uis(SYNTHETIC) − completion_observed(OBSERVED)` in pp; `within ±5 pp` iff
  `|d| ≤ 5.0` **inclusive, on the unrounded value** (display rounding never decides).
- **Bar.** `PATH-BAR-MET` iff **count ≥ 17 / 33**; falsifier `PATH-BAR-MISSED` iff **count ≤ 16 / 33**.
- **Construction check (mandatory).** The same procedure applied to the **A00** panel must return **9/33**, with level
  medians **−4.3008 / −29.4351 / −27.5857** pp — reproducing EXP-7's V1 construction. A different A00 count means the
  derivation is wrong and the run is **`INVALID`** (not a result).
- **Companions, reported and non-verdict-bearing:** per-level counts and medians; the ±10 pp count; the signed mean; the
  largest absolute miss; **upper 2024**; the ratio audit `upper_t / lower_{t−3}`.

### 6.2 Crossings — ±5 y (D34/A6)

- **Thresholds (declared):** `primary ≥ 90`, `lower_secondary ≥ 90`, `upper_secondary ≥ 90` completion pp.
- **Observed crossing year** = the **first observed year** at or above the threshold **with band = adjacent observed
  years** (D34). Computed from `UNIVERSALIZATION_SERIES.csv`: primary **2017** (91.918; 2013 = 87.45 below), lower
  **2024** (92.414; 2023 = 88.44 below), upper **none** (max 75.0253).
- **Model crossing year** = the first panel year ≥ threshold.
- **Leg passes** iff: observed crosses **and** |model − observed| ≤ **5 y**; **or** observed does **not** cross **and**
  the model does not cross by 2025. Otherwise the leg **fails**.
- **Crossings verdict:** `CROSSINGS-MET` iff 3/3 legs pass; `CROSSINGS-MISSED` otherwise. Reported per level with both
  years and the gap. Left-censoring: no leg here is left-censored (all observed crossings are inside the window).

### 6.3 Representation (reported alongside; EXP-14's question is coexistence **and** path)

Carried verbatim from v1.5's (a) family **except** the mislabelled (a-iv) leg, which is **not re-frozen** (D134(4)):
(a-i) `unfilled_share_O ≥ 0.10` in ≥ 15/30 scored cells (2010–2024 × lower, upper); (a-ii) `queue_ratio_H = A_H/K_H ≥
1.10` in ≥ 15/30; (a-iii) both in ≥ 8/15 years **and** `p4 = rung4_emp/rung4_demand ≤ 0.50` in ≥ 8/15. The corrected
contrast is reported instead of (a-iv): `same_level` counts **A00 = 0 vs A10 ≥ 8** (D134(4): the right contrast is the
bimodal switch, not the κ switch).

### 6.4 Verdict string and precedence

```
representation : REPRESENTATION-HOLDS | REPRESENTATION-FAILS   (§6.3, 2 of 3 legs)
path           : PATH-BAR-MET (>=17/33) | PATH-BAR-MISSED (<=16/33)     (§6.1)
crossings      : CROSSINGS-MET (3/3) | CROSSINGS-MISSED                 (§6.2)
guards         : GUARDS-PASS | GUARDS-FAIL                              (§7)
OVERALL        : precedence INVALID > FAIL-RE-FIT > GUARDS-FAIL >
                 (PATH-BAR-MET & CROSSINGS-MET) -> PATH-REPRODUCED
                 (PATH-BAR-MET xor CROSSINGS-MET) -> MIXED
                 (PATH-BAR-MISSED & CROSSINGS-MISSED) -> PATH-FAILED
```

`PATH-REPRODUCED` is the **positive** branch of EXP-14 §2; `PATH-FAILED` with `REPRESENTATION-HOLDS` is the
**negative** branch ("representation-only capability; the ceiling remains `UNATTRIBUTED`"). `FAIL-RE-FIT` voids the
run. A `UNDETERMINED` value is never substituted for a check that ran.

---

## 7. Guards (all must pass; a failure is reported, never rescued)

1. **G1 A00 identity.** The A00 panel (bimodal OFF, κ OFF, tier_surv OFF, all repair blocks OFF) must be **byte-identical**
   to `generator_v1_3/results/synthetic_panel_v1_3.csv`, sha256
   **`47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3`** (6 720 rows × 89 columns). Independent
   cross-check: the frozen base code `code/base_v1_3_sim.py` run directly must produce the same sha.
2. **G2 frozen-file invariance.** Every frozen input (v1.3 code, v1.3 panel, v1.5 code, v1.5 panel, v1.5 spec files,
   `UNIVERSALIZATION_SERIES.csv`, the predecl inputs of EXP-11/EXP-13) must be unchanged before and after the run.
3. **G3 counterfactual identity** (R3): `A00CF` ≡ `A01D` cell-for-cell, all 89 columns × 6 720 rows; plus the two exact
   checks (primary/lower schooling columns cell-identical; tertiary admission moving only through the eligibility pool
   and non-increasing where the cap binds).
4. **G4 propagation ledger + one-way order** (R2): every moving column with mechanism and sign; the static order audit
   (admission region reads 0 economy-region variables of the same year); the declared within-year dependencies (W1, W2)
   stated; `FAIL-RE-FIT` if a **capped-economy → same-year-admission** feedback is found and not declared.
5. **G5 determinism.** Two complete runs into `results/` and `results/determinism_run2/` with **byte-identical** result
   CSVs (`cmp` + sha256). One PCG64 stream, seed **20261120**, frozen v1.2 draw order, no wall-clock, no hostname, floats
   `%.10g`.
6. **G6 predeclaration integrity.** `sha256(PRE_DECLARATIONS.md)` equals the value embedded in the built code, and the
   declared JSON block equals the code's parameters. `sha256(PARAMS.md)` recorded and re-checked after the run.
7. **G7 no-fit audit.** The parameter values are those of §5 (fixed pre-run); the declared grids are disclosed; the
   scored arm uses the pre-declared value; no value was selected after seeing a level. A parameter chosen by reference
   to the bar or the band is `FAIL-RE-FIT`.

## 8. Rules that do not move

- **No threshold change.** 17/33, ±5 pp inclusive, ±5 y, the 3 crossing thresholds, the (a) thresholds, and the
  verdict vocabulary are fixed by this file. **No parameter, threshold, band, year, arm or verdict word changes after
  the scored run.**
- **No fit / no re-tune.** No parameter is estimated, calibrated, or selected against any observed series or level bar.
  A **grid search that lands on a passing cell is `FAIL-RE-FIT`** (D134(3)).
- **No fitting to the known PHL outcome.** The observed series enters **only** as the comparison object in §6; it is
  never read by the simulator. `SYN00_PHL_LIKE`'s trait block is the frozen v1.3 declared block, unchanged.
- **Banned language (carried):** **"demand falsified"** and every paraphrase of it; "reproduces universalization";
  "capacity explains the timing"; "portability holds"; any direction or causal word. The A3 demand line stays
  **KILLED** (D130) as a **specification** result, and no v1.6 number is evidence about demand.
- **Labels.** Every generator number `SYNTHETIC`; every PHL series `OBSERVED`; every behavioural assumption
  `DECLARED`. v1.5's verdict string is **not** re-scored; no v1.5 check is re-frozen.
- **HELD data stay HELD, named and unused:** DepEd/CHED seats-vs-enrolment; private/public shares of enrolment and
  provision; SHS voucher take-up; capacity utilisation (the object Tier O's `V_O` would be validated against);
  PSA microdata; WB Enterprise Surveys; real per-pupil spending; annual capacity/enforcement; a measured rung-4
  credential-queue series; PHL/KHM/CHN/JPN shadow participation; a measured remittance→schooling coefficient.
  **None is fabricated, proxied or imputed here.**

## 9. What the outcome will and will not license

- **Positive** (`PATH-REPRODUCED`): the class becomes a **candidate level model** for PHL's observed path **as a
  synthetic representation**, and the next question is what sets κ and the tier share. It still does not license a
  causal claim, a direction claim, or "A5 holds".
- **Negative** (`PATH-FAILED`, `REPRESENTATION-HOLDS`): the class is recorded as a **representation-only** capability;
  the ceiling remains **`UNATTRIBUTED`**; the report must say **which object** loses the path (take-up, aggregate
  demand, the lower series) rather than "the class fails".
- **Falsifier** (`FAIL-RE-FIT`): no successor is built this phase and the level question is closed at `UNABLE`.
- **In no case** does this cell produce evidence about the Philippines, a forecast, a causal statement, or a
  re-opening of C1–C4.
