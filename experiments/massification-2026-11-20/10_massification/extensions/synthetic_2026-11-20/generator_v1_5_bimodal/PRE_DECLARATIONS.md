# PRE-DECLARATIONS — Amendment A5 / v1.5 **BIMODAL-GATE** (design + frozen pre-declaration, **run-ready, NOT RUN**)

**`LABEL: SYNTHETIC` for every generator object; `LABEL: OBSERVED` for every PHL series; `LABEL: DECLARED` for every
behavioural assumption.** This file is a **declared pre-registration of a synthetic experiment**. It is **not
evidence about the Philippines or any country**, it licenses **no causal claim and no direction claim**, it
**re-opens no C1–C4 claim**, and it **fits nothing to the known PHL outcome**.

- Object: **Amendment A5 — BIMODAL-GATE** (`MODEL_ARCHITECTURE.md:348-446`, D124), plus the **A5 addendum**
  (D121 cross-level link; D125 one-way ratchet).
- Base instrument: frozen **`generator_v1_3`** — `code/sim_v1_3.py`
  sha256 `70ae8f0eef83358493dad3d3feb2d6a8841c4bb6fad3966627f4eed70e2a9877`; panel
  `results/synthetic_panel_v1_3.csv` sha256 `47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3`
  (6 720 rows = 30 countries × 1970–2025 × 4 levels, 89 columns). The v1.3 instrument is itself the frozen v1.2
  generator (`code/sim_v1_2.py` `61123aa9…`, panel `14729c51…acf5ac`) plus the frozen shadow block
  (`shadow_module/PRE_DECLARATIONS.md` `cf8c61cb…` + S1 note `af49a616…`). **No file in any existing generator,
  experiment or repo directory is edited, moved or written by this design.**
- This directory contains **design + pre-declaration only**. **No model has been run, no results file exists, no
  RNG has been drawn.** `results/` is **not** created by this delivery.
- **Status of this file:** frozen on creation. Its sha256 is recorded in `RUN_MANIFEST.json` and `SHA256SUMS.txt`
  **before any run**. The build must refuse to run if the on-disk sha256 differs from that recorded value.
  **No threshold, bar, year set, cell rule, κ value, band, arm definition or verdict word in this file may be
  changed after results are seen.** If a declared step cannot be implemented exactly as written it is **reported
  as not implemented**, not silently approximated.

---

## 0. The question, in one paragraph, and what would count as an answer

The user's structural point (D124, `THEORY_FRAME.md:30-45`): the Philippine system is **bimodal within itself** —
low-cost, if not free, seats go **untaken** by families choosing out of education, **at the same time** as extreme
competition at the high gates. A single scarce gate cannot represent that coexistence; the A3-D result is therefore
**"the unrationed single-gate model cannot represent a bimodal system"** (a **model-specification failure**), and
**never** "demand falsified". v1.5 asks: *can a declared two-tier structure — open low-quality seats that may go
unfilled, rationed high-quality gates (school gates **and** the credentialed-job rung), and an explicit
outside-option block — hold both facts in the same synthetic country-year, while obeying the declared cross-level
pipeline link and carrying no reversal term?*

**What counts as an answer is fixed in §6 below, in advance.** Checks (a)–(e) are scored with declared thresholds;
a **MIXED** or **FAIL** verdict is a legitimate, reportable result and is **not** rescued, re-tuned, re-specified or
re-run to flip.

---

## 1. Frozen facts this pre-declaration takes as given (read-only; not re-derived here)

These are on disk **before** this file. They are quoted so the checks cannot be re-worded around them.

**1.1 Pipeline capability (EXP-7 REPRO-PATH, predecl `74f9d0e0…`).**
`repro_path_2026-11-20/FINDINGS.md:20,67-102`:
leg (a) **`ENDPOINT-ONLY`** — **9/33** observed year-level comparisons within ±5 pp against a predeclared bar of
**≥17/33**; median signed deviation primary **−4.30**, lower **−29.44**, upper **−27.59** pp; the panel matches only
in 2021–2024 (7/11 cells, median +0.04 pp) and misses 20/22 earlier cells (median −28.21 pp).
leg (b) **`b2`** — **20/53** anchor-type years violate `upper_t ≤ 0.949·lower_{t−3}` before the projection (every year
2006–2025), **0/53** after; upper 2024 **76.6391 → 63.9695** (**Δ −12.6695 pp**), `0.949 × 67.4073 = 63.9695`;
baseline guard **`BASELINE-GUARD-PASS`** (byte-identical `14729c51…acf5ac`).
**Consequence carried into v1.5: the link must be built into the transition, not post-processed** (`FINDINGS.md:152-166`).

**1.2 v1.2 validity scope (D119).** v1.2 is **crossing/endpoint placement, not a path**: **9/33** within ±5 pp;
median lower **−29.44**, upper **−27.59** pp; every pre-2021 lower/upper value **24–37 pp low**; 2024 upper
**+1.61 pp**. **Any v1.5 statement that inherits a v1.3 level inherits this scope**, and every level statement in
this experiment is therefore readable only as a **2022–2024 placement** statement. This disclosure is repeated on
every level-bearing output (`results/v1_5_checks.csv` `scope_note` column).

**1.3 The binding queue is the job rung (cycle-14 V8).** `08_council/brief_022/SYNTHESIS_022.md:108`: rung-4
absorption `p₄ = rung4_emp/rung4_demand` for `SYN00_PHL_LIKE` (2010+, upper-secondary rows) has **median 0.151**
(range 0.110–0.189), `SYN28` 0.177, `SYN18` 1.000, panel median 0.507; the model's upper-school-gate advance
probability is **≈0.999**. **Tier H must therefore contain the credentialed-job rung, not only the school gate.**

**1.4 The generator has no cross-level accounting (V2).** Synthetic `upper_t/lower_{t−3}` exceeds **1.10** in
**12** anchor-type years (all 2013–2024), panel-wide **177/1 590** cells, max **1.444** (`SYN07` 2014); the observed
PHL maximum is **1.072** (`SYNTHESIS_022.md:106`).

**1.5 A3-D is PARKED and is not re-tuned here (D116/D118).** The demand block (`generator_v1_4_demand/`) is
**not** wired into v1.5, is **not** re-scored, and **no** A3-D parameter is moved. Its `guard` convention (block OFF ⇒
byte-identical v1.3 panel, sha256 `47d4b082…`) is **reused** (§6(e) E1).

**1.6 Observed PHL anchors used for bands (OBSERVED; never fitted).**
`10_massification/data/UNIVERSALIZATION_SERIES.csv`, rows `status=observed`, UIS SDG4 release 2026-11:
primary 2017 = **91.918** (`:49`), 2024 = **98.305** (`:53`); lower-secondary 2021 = **80.896** (`:39`),
2023 = **88.442** (`:41`), 2024 = **92.414** (`:42`); upper-secondary 2017 = **76.433** (`:61`),
2022 = **68.277** (`:62`), 2023 = **71.929** (`:63`), 2024 = **75.025** (`:64`); out-of-school rate upper-secondary
2021 = **24.969** (`:480`), 2024 = **22.884** (`:483`), 2025 = **23.714** (`:484`); GER upper-secondary
2018 = **66.046** (`:296`).

---

## 2. The two-tier gate structure (declared architecture; parameters in `PARAMETERS.csv`)

Every level `L ∈ {primary, lower_secondary, upper_secondary, tertiary}` has adequate places `seats_L(t)` from the
frozen v1.3 supply rule. v1.5 splits **places**, not demand, into two declared segments:

```
K_H,L(t) = h_share_L · seats_L(t)          Tier H — rationed high-quality places
K_O,L(t) = (1 - h_share_L) · seats_L(t)    Tier O — open-access low-cost places
seats_L(t) = K_H,L(t) + K_O,L(t)           identity; no third segment, no reallocation (declared)
```

### 2.1 Tier O — open-access, low-cost/low-quality places that **can go unfilled**

- **Near-zero private cost**: `cost_O,L = cost_O_mult · cost_base_L` with `cost_O_mult = 0.03` (`PARAMETERS.csv` T07);
  nominal, not zero, so the take-up equation is not degenerate. Declared, not observed.
- **Low quality**: `Q_O,L(t) = q_O_mult · Q_L(t)`, `q_O_mult = 0.55` (T05); it feeds survival, so Tier O is a
  **lower-return** place, not a free label.
- **Take-up is an equilibrium, not a residual**:
  `T_O,L(t) = C_L(t) · Σ_i w_i · 1[ U_O,i,L(t) ≥ max(U_H,i,L(t) refused, U_work,i,L(t), U_both,i,L(t), U_neither,i,L(t)) ]`,
  bounded above by `K_O,L(t)`.
- **Unfilled places are a primary output, reported directly**:
  `V_O,L(t) = max(0, K_O,L(t) − T_O,L(t))`, `unfilled_share_O,L(t) = V_O,L(t) / K_O,L(t)`.
  `V_O` is **not** `seats − demand` (a residual), it is the count of places for which **no household's utility
  comparison selects Tier O**. Panel columns: `tierO_capacity`, `tierO_takeup`, `tierO_unfilled`,
  `tierO_unfilled_share`, `tierO_takeup_share`.
- **Declared prohibition (audited):** unfilled Tier O places are **never** reallocated to Tier H, never converted to
  quality, never carried forward. `K_H` is computed from `seats` alone and must be provably independent of `T_O`
  (`results/tier_audit.csv`, code audit T-AUD-3).

### 2.2 Tier H — rationed high-quality gates

Tier H carries **both** the rationed school gate **and** the credentialed-job rung (V8; §1.3).

- **School gates (levels 1–3).** Candidates `A_H,L(t)` = household cells whose utility comparison ranks Tier H first.
  Places `K_H,L(t)`. Admission by **declared rank** (§2.4), top `K_H` of `A_H`:
  `admitted_H,L = min(A_H,L, K_H,L)`, `queue_H,L = max(0, A_H,L − K_H,L)`,
  `queue_ratio_H,L = A_H,L / K_H,L`, `p_adv_H,L = admitted_H,L / A_H,L ≤ 1`.
- **Credentialed-job rung (rung 4).** Capacity `J_4(t)` (the model's own rung-4 demand), absorption
  `p₄(t) = rung4_emp(t)/rung4_demand(t)` — the **binding** quantity (V8: 0.151 in the anchor type; §1.3). The
  credentialed job is a **gate**, so access to it is rank-rationed exactly like a school gate, with its own shadow
  competition (rank rule S06; there is **no** separate job-gate parameter — the rung-4 capacity is the model's own
  `J_4`). The school gate is **not** re-used as the job gate: `p_adv_H` at the school
  gate and `p₄` at the job rung are **separate reported objects** (the 6.6× domain error of A3-D is not repeated).
- **Returns differ by tier**: `w_H = (Y/1000)·mult_r·(1 + cred_prem_H·r)·rankf_r` and
  `w_O = (Y/1000)·mult_r·(1 + cred_prem_O·r)·rankf_r` with `cred_prem_H = 0.18`, `cred_prem_O = 0.03`
  (`PARAMETERS.csv` T08/T09). With the block OFF the wage equation is **exactly** v1.3's single `cred_prem = 0.10`.

### 2.3 The explicit outside option (v1.2 childworld four-state block, unchanged structure)

The outside option is **the v1.3/v1.2 four-state household block itself** — `school` / `both` / `work` / `neither`,
with the childworld-derived utility form and the declared parameter names `y_med, w_child, farm, compat, v0, decay,
cost, neither, girl_care, haz` (**`BORROWED-FROM-ATLAS-STRUCTURAL`**, structure and names only; no childworld value,
prior or posterior is imported — `generator_v1_2/PARAMS.md` §5.1-5.5).

- **Out-of-school defaults to work** (`ration_work_share = 0.90`); **no passive "neither" sink** — "neither" is
  declared, bounded and reported separately (`neither_final`), never absorbs a residual.
- Three of the four states enter the tier comparison directly: `U_work`, `U_both`, `U_neither` are the **refusal
  values** against which `U_O` and `U_H` are compared. This is why free seats can sit empty while others queue: the
  low tier's return can fall **below the option value of work**.
- The tier block **adds no fifth state** and **removes no state**.

### 2.4 Sorting (declared; no fitted taste parameter)

Households are a **declared 5×3 lattice**: 5 income quintiles × 3 ability strata = 15 cells, joint weights
`cell_weight` (`PARAMETERS.csv` S01; row sums 0.20, total 1.00; mild positive income–ability association declared).
Income within a cell is `y_i = ybar_c · exp(sigma_tier · z_q)` with `sigma_tier = 0.80` (S03) and the standard-normal
quintile midpoints `z_q` reused from the shadow module (`shadow_module/PARAMETERS.csv` B23). Ability
`a_i ∈ {0.25, 0.50, 0.75}` (S04).

```
U_H,i,L = util(y_i − cost_H,L) + v_H,L + H_h · p̂_adv,H,L · G_H · 1[a_i ≥ a_gate] − risk_pen · (1 − p̂_adv,H,L)
U_O,i,L = util(y_i − cost_O,L) + v_O,L
outside  = { U_work, U_both, U_neither }   from the frozen four-state block (unchanged)
```
with `p̂_adv,H,L = p_adv_H,L(t−1)` (declared **one-year expectation lag**; S07) and `G_H` the model's own
formal–informal log-wage gap (`ln(w_for[rung 2]/w_inf)`, as v1.3 uses at g4; `IMPLEMENTATION_NOTE.md` §3 item 3).
**Rank rule** for admission: `rank_score_i = 0.30·(y_i/ybar_c) + 0.70·a_i` (S06) — income position and ability only;
no country-specific, level-specific or year-specific rank weight.

**Utility parameters `v_H,L`, `v_O,L` are one declared vector applied to every level and every country** (T10):
`v_H,L = v0 · decay^L` and `v_O,L = v0 · decay^L · 0.45`. **There is no level-specific free shim**: the only
level-indexed objects in the whole tier block are the declared structural vectors `h_share, q_mult, cost_mult,
cred_prem` — each a single vector for all 30 countries, audited (T-AUD-1/2, mirroring shadow c4c).
**The v1.2 "work-incentive weight" is removed as a free parameter**: `w_work_free = 0.0` (T11) and the constant is
held at 0 in both tiers and in the outside option; the ceiling must come from tier quality, the outside option and
sorting — **not** from a level-anchored utility shim.

### 2.5 Tier-specific exit cost (declared, for the Council — **not** a D101 re-opening)

Declared **asymmetry**, reported but **not** a check and **not** a result: a household may leave Tier O at
`exit_cost_O ≈ 0` (declared; no re-entry penalty, no fee clawback) and the model must show Tier O places going
unfilled/abandoned; leaving the **credential gate** carries a declared `exit_cost_H > 0` (forfeited rank, credential
non-transferability), modelled only as a **rank/queue retention** term on the Tier H queue (`queue_retain`,
inherited v1.2 constant) — **no** exit-cost *layer* is added (D101: no exit-cost layer until WT1 ∧ WT3 both
non-null; both are closed null). The Council question is noted in `DESIGN.md` §7; v1.5 **does not** test it.

---

## 3. Pipeline precondition — the declared cross-level accounting link (`upper_t ≤ κ · lower_{t−3}`)

**Declared constraint, never fitted.** κ is **not** estimated in v1.5, **not** updated from the panel, **not** swept
to make the link bind, and **not** re-derived at run time.

```
κ      = 0.949          declared: median of the 8 observed PHL upper_t/lower_{t-3} pairs
κ      = 0.960          declared SENSITIVITY only (pre-2018 median); non-verdict-bearing
lag    = 3 years        exact; no nearest-year matching, no extrapolation
register: completion_uis (UIS convention), the only admissible numerator (V6)
```

Provenance (re-derived read-only for this pre-declaration, arithmetic only; **not a run**): the 8 observed PHL pairs
under the V4/V5 rule (exact lag 3, else nearest available lower year at lag 2 or 4, else drop) are
`0.9493 (2003), 0.9283 (2004), 0.9698 (2008), 0.9730 (2010), 0.9490 (2013), 1.0725 (2017), 0.8892 (2023),
0.9274 (2024)`; median = **0.94916 → 0.949**; pre-2018 median = **0.95956 → 0.960**. This reproduces the EXP-7
declared provenance check exactly (`repro_path_2026-11-20/FINDINGS.md:71`). κ is therefore **`OBSERVED`-derived and
`DECLARED` as a system input**, never a fitted parameter.

### 3.1 Internal form (built into the transition — **not** a post-hoc projection)

The constraint is enforced **inside** the year loop as an admission cap on the upper-secondary entry cohort, which is
the form in which the upper level is **inherited** rather than clipped:

```
adm_upper_cohort(s)  ←  min( adm_upper_cohort(s),  κ · comp_lower_cohort(s) )        for every year s
```
i.e. the cohort admitted to upper secondary in year `s` cannot exceed κ times the lower-secondary cohort completion
**of the same year `s`**. Because upper completion at `t` is `m·adm_upper(t−3)·surv_upper(t)` and
`surv_upper ≤ 0.995 < 1`, the cap is a **sufficient** condition for the completion-level statement
`comp_uis_upper(t) ≤ κ · comp_uis_lower(t−3)` (the `m` and the 3-year lag cancel), which is then **audited** cell by
cell as the implied ratio. Only the upper-secondary entry is capped; **no other level, year, parameter or country
is touched**. `κ` is a declared input to the cap, not a fit: with `kappa_link = OFF`, the cap is the identity
(`adm_upper ≤ ∞`) and the arithmetic is **exactly** v1.3's.

**Declared consequence, stated before the run (pre-freeze arithmetic, §9, not a result):** with `κ = 0.949` and
v1.3's `comp_uis_lower(2021) = 67.4073`, the implied upper-secondary ceiling at 2024 is
`0.949 × 67.4073 = 63.9695` pp. **The v1.5 upper 2024 endpoint is therefore expected to be ≤ 63.97**, i.e. **≈11 pp
below the observed 75.025** and **outside the v1.2 band [73,77]**. This is declared **now**, so that it cannot be
presented later as a discovery, a failure, or a reason to move κ. It is the `b2` finding of EXP-7 carried into the
model: **the binding defect is the lower series, not the upper ceiling.**

### 3.2 What the link must NOT be able to do

The link may change **only** upper-secondary entry. It may **not** change primary, lower-secondary or tertiary
dynamics, wages, rungs, or the four-state block. This is a guard, not an aspiration: §6(e) E2 requires
`primary`, `lower_secondary`, `tertiary` columns to be **cell-identical** to v1.3 in all 6 720 rows under arm
`(bimodal OFF, κ ON)`, and upper rows to differ **only** where the cap binds.

---

## 4. The one-way ratchet (D125) — declared irreversibility, **no reversal diagnostic**

**DECLARED-THEORY. Theory only, never evidence.** The user's macro-principle ("there is no reverse button") is
recorded in `THEORY_FRAME.md` §1 and D125. v1.5 encodes it as **three declared construction rules** and **nothing
else**:

1. **No reverse/reversal term anywhere in the transition rules.** No term of the form
   `+ λ·(level_{t−k} − level_t)`, no restoring force toward a stored prior configuration, no "return to the prior
   state" branch, no negative-feedback term whose target is a **pre-installation** level. The tier block adds
   **none**; the κ cap is a monotone upper bound, not a restoring force (it can only remove admissions, never add
   them).
2. **Shocks enter only as declared inputs and may set back levels, never reverse the path.** `gnoise` (growth) and
   `hhnoise` (household income) are the only shocks; both are the frozen v1.3 declared inputs, applied unchanged.
   No new shock, no shock-contingent rule change, no regime switch triggered by a shock.
3. **The option set is path-created.** Rungs open at `x_open` thresholds and once opened stay open; the takeoff
   state `Tstate` is non-decreasing (v1.2/v1.3 property, unchanged). Tier membership is **not** reversible in the
   option-set sense: a Tier H credential, once earned, is never converted back into a Tier O credential.

**Explicit statement required by the brief: `NO REVERSAL DIAGNOSTIC IS TO BE INFERRED FROM THIS RUN.`**
v1.5 contains **no** reversal test, **no** exit-episode test and **no** "did the system go back" statistic. The
absence of a reversal term is a **construction fact**, verifiable by code audit (R1 below); it is **not** a test of
the strong claim. Our data show **setbacks without reversal** (PHL upper-secondary 2017→2022 **−8.16 pp**, recovery
to 75.03, never ≥90; WT4 zero sustained exit episodes, **descriptive and fragile**) — a **bounded observable
implication, NOT a test of the strong claim**. The strong claim ("nobody ever goes back") is **untestable on our
data**; any future reversal diagnostic must be separately predeclared and labelled **descriptive**
(`THEORY_FRAME.md:53-67`).

---

## 5. Two orthogonal switches, four arms

| switch | levels | meaning |
|---|---|---|
| `bimodal` | `OFF` / `ON` | OFF = the frozen v1.3 single-gate stack, arithmetically untouched; ON = the Tier O/Tier H split, sorting, outside-option comparison, tier returns and the tier columns |
| `kappa_link` | `OFF` / `ON` | OFF = no cross-level cap (v1.3 behaviour); ON = the declared admission cap of §3.1 |

| arm | `bimodal` | `kappa_link` | role |
|---|---|---|---|
| **A00** | OFF | OFF | **no-re-fit guard**: panel projected onto the v1.3 column set must be **byte-identical** to `47d4b082…` (E1) |
| **A10** | ON | OFF | diagnostic only: what the tier structure does **without** the pipeline (reported, **not scored**) |
| **A01** | OFF | ON | **the linked arm**: a **new** panel, reported **separately**, never compared for identity (E2) |
| **A11** | ON | ON | **the scored arm** — checks (a)–(e) are scored here |

Plus declared sensitivity/ablation arms, each reported separately and **none** able to change the A11 verdict:
`h_share ± 0.10` (2 arms), `q_H_mult ∈ {1.10, 1.40}` (2 arms), `q_O_mult ∈ {0.40, 0.70}` (2 arms), `κ = 0.960`
(1, non-verdict), `child wage +10%` (1, check d-iii), `Tier O quality −20%` (1, check d-iv), `sorting OFF` (1, check d
context).
**Ten extra arms; all declared here; no arm may be added after results.**

---

## 6. CHECKS — frozen with thresholds; scored in `results/v1_5_checks.csv`

Scored on **arm A11** unless a check says otherwise. Country of record for (a)–(d): **`SYN00_PHL_LIKE`**, the only
v1.3/v1.2 country whose trait block is anchored on an observed path (it is **not** the Philippines). All
year-level statements are **2022–2024 placement** statements (D119, §1.2) and are labelled as such.

### (a) Bimodality in one system — untaken low-cost places **and** excess demand at the high gates, same country-year

- **(a-i) unfilled floor.** `unfilled_share_O,L(t) ≥ 0.10` in **≥ 15 of the 30** scored cells
  `(t, L) ∈ {2010..2024} × {lower_secondary, upper_secondary}`.
- **(a-ii) high-gate bar.** `queue_ratio_H,L(t) = A_H,L(t)/K_H,L(t) ≥ 1.10` in **≥ 15 of the same 30 cells**.
- **(a-iii) simultaneity (the actual object).** In **≥ 8 of the 15 years** 2010–2024, (a-i) and (a-ii) both hold —
  **in the same country-year**. Additionally the **job gate** condition `p₄(t) ≤ 0.50` must hold in **≥ 8 of those
  15 years** (V8: expected ≈0.15, so this leg is expected to pass and its role is to confirm that the credential
  queue is present, not to discriminate).
- **(a-iv) the single-gate contrast (representation statistic, not a claim of absence).** The same-level coexistence
  statistic is `same_level(t) = 1[ spare_upper(t) > 0 ] · 1[ rationed_official(upper, t) > 0 ]`, where
  `spare_upper = seats_upper − enrolment_upper`. **In arm A01 (`bimodal OFF`, the frozen single-gate stack) this count
  must be 0 over 2010–2024**, because the upper school gate is unrationed (`rationed_official = 0`; V3, V8), and it
  must be **≥ 8** in arm A11 (the (a-iii) count). The single-gate model therefore cannot put a *declined place* and a
  *contested place* at the **same level** in the **same year**.
- **What the frozen model already does — declared so the contrast is not overstated.** v1.3 is **not** literally a
  world with no spare capacity: its upper-secondary spare adequate places are **0.1418 of cohort in 2024**, and its
  **job** gate is binding (`p₄ ≈ 0.151`; V8). What it lacks is (i) a **declined-place object** (its `rationed` column
  is excess *demand*; spare capacity is an arithmetic leftover, never a household decision), (ii) **rationing at the
  school gate** (so no same-level coexistence is possible), and (iii) a demand channel attached to a **binding**
  gate (the A3-D error). **(a-iv) is scoped to exactly those three absences** and is **not** the claim that the
  single-gate model has no unused capacity.
- **Verdict.** `PASS` iff (a-i) ∧ (a-ii) ∧ (a-iii) ∧ (a-iv). `MIXED` iff (a-iv) holds and 1–2 of (a-i)–(a-iii) fail.
  `FAIL` iff none of (a-i)–(a-iii) holds. `UNDETERMINED` iff a required column is missing or NaN in a scored cell.
- **Declared honesty caveat (frozen).** With `h_share` **declared**, the *coexistence* is partly **arithmetical**
  (§9 pre-freeze arithmetic: at 2024 the split makes ≥25% of Tier O places structurally unfillable **if** every
  refused Tier H candidate would accept Tier O). **(a) is therefore a REPRESENTATION check — "the model class can
  hold both facts" — and NOT evidence about the Philippines.** Its diagnostic content is (i) the **magnitude** of
  the unfilled share, (ii) its **monotone response** to the declared `h_share` sensitivity grid, and (iii) the
  **exact zero** in arm A01. This is stated before the run so that no PASS can travel as an empirical finding.

### (b) Level pattern — primary near-universal while upper-secondary **stalls** (v1.2/v1.3 PHL signature bands, D119 scope)

- **(b-i) floor.** Primary `completion_uis` first sustained ≥ 90 occurs in **2014–2020** (the v1.2 band,
  `v1_2/PRE_DECLARATIONS.md` §5 check (a)); and primary 2024 **≥ 92**. (No upper bound is declared: the model's
  primary 2024 sits at the `m = 1.10` convention's clip of **100.0**, and a saturation artefact must not be scored
  as an overshoot.)
- **(b-ii) stall.** Upper-secondary `completion_uis < 90` in **every** year ≤ 2024, and upper 2024 `∈ [55, 85]`
  (a stall band, not a collapse: it admits both the v1.2 band and the κ-implied ≈63.97).
- **(b-iii) endpoint placement (reported, NOT verdict-bearing).** Upper 2024 `∈ [73.0, 77.0]` — the v1.2 band.
- **Verdict.** `PASS` iff (b-i) ∧ (b-ii) ∧ (b-iii). **`MIXED` iff (b-i) ∧ (b-ii) ∧ ¬(b-iii)** — the *pattern*
  emerges but the **endpoint is displaced** by the declared κ link. `FAIL` iff ¬(b-i) ∨ ¬(b-ii).
  `UNDETERMINED` iff a required series is absent.
- **Declared expectation (pre-freeze, not a result):** the κ cap implies upper 2024 ≤ **63.9695**, so
  **(b-iii) is expected FALSE and (b) is expected `MIXED`.** The pre-declaration of this expectation is
  deliberate: it makes a `MIXED` verdict an accountable prediction rather than a post-hoc excuse, and it forbids
  reading the endpoint displacement as a demand or tier failure.
- **D119 scope disclosure, mandatory on every (b) row:** v1.2/v1.3 levels are a **2021–2024 placement**, 24–37 pp
  low before 2021; (b) is a **shape** statement about the model, never a reproduction of the PHL path.

### (c) Shadow placement — shadow demand concentrated at the **high** gates, low at the **open** tier

Re-uses the v1.3 shadow module's demand equation and its c1/c3/c5 checks **unchanged** (no threshold moved); a new
**placement** object is added because the tier split creates a denominator the v1.3 spec never had.

- **(c-i) placement ratio.** `D_H(t)/D_O(t) ≥ 5.0` in **every** year 2010–2024 for `SYN00_PHL_LIKE`, where `D_H` is
  the cohort-incidence shadow demand at the high gates (school gate g2 plus the job gate g4, reported separately)
  and `D_O` is the **same demand equation** evaluated at the open tier's gate state (`R_O ≈ 1`, no rationing,
  `V_O` from the tier return).
- **(c-ii) open-tier ceiling.** `D_O(t) ≤ 0.025` in **every** country-year (the v1.3 c3 ceiling, reused verbatim).
- **(c-iii) the asymmetry that is not structural.** The declared `R → 2R` experiment at the **high** gate raises
  `D_H` by **≥ +10.0 pp** (the v1.3 c1(ii) bar, applied here to the anchor type only), while the **same** doubling
  applied at the **open** tier raises `D_O` by **≤ +1.0 pp** — i.e. the gate-pressure response is **located at the
  high gate**. (The ≤ +1.0 pp open-tier leg is new; it is what stops a generic "tutoring rises with anything"
  result from passing as placement.)
- **(c-iv) declared comparison (reported, NOT re-scored).** The v1.3 values are carried verbatim for comparison:
  `c1` PASS (R-doubling at g2: HKG +32.67, PHL +30.93, KHM +30.10 pp), `c2` PASS (+4.26/+3.43/+2.90 pp),
  `c3` PASS (max `D_g0` 0.0205), **`c4a` FAIL** (0.340215 vs [0.75, 0.95]), **`c4b` FAIL** (+0.0967 vs ≥0.10;
  +0.1119 ≥ 0.05), `c4c` PASS, `c5` PASS, `c6` PASS — `generator_v1_3/results/shadow_checks_v1_3.csv` rows 1–10.
  **c4a/c4b are NOT re-scored and NOT rescued under v1.5** (the tier split changes their denominator; re-scoring
  them would be a threshold change under a new object). Their FAIL stands exactly as delivered (D117).
- **Verdict.** `PASS` iff (c-i) ∧ (c-ii) ∧ (c-iii); `MIXED` iff 1–2 fail; `FAIL` iff none; `UNDETERMINED` iff the
  shadow columns are absent.
- **Declared caveat (frozen).** (c-i)/(c-ii) are **largely structural** — the v1.3 run already gives
  `D_g2(2020) = 0.2606` vs `D_g0(2020) = 0.0128` (ratio ≈ 20×) — so **(c-iii) is the only discriminating leg**, and
  (c) is reported with that decomposition. This mirrors the v1.3 c3 honesty note (`shadow_module/PRE_DECLARATIONS.md`
  §8 c3 + S1 note item 3).

### (d) The ceiling from sorting / quality / outside option, with **NO free taste parameter**

- **(d-i) no free taste, no level shim (audit).** `w_work_free = 0.0` (T11) in **both** tiers and in the outside
  option; and the code audit `T-AUD-1/2` finds **zero** level-targeted utility constants and **zero**
  country-specific values of `h_share, q_mult, cost_mult, cred_prem, rank_weights, v_H, v_O, sigma_tier`
  (one vector each, all 30 countries). If any exists, **(d) = `FAIL`** (mirror of shadow c4c's VOID rule; here FAIL,
  not VOID, because (d) is the check the audit protects).
- **(d-ii) the pattern is held under the cap.** Upper `completion_uis < 90` in every year ≤ 2024 and
  `slack_t = κ·lower_{t−3} − upper_t ≥ 0` in **all 53** scored anchor cells (1973–2025); **and the cap is
  non-binding** (`adm_upper` unchanged by it) in **≥ 5 of the 53** cells, so the upper level is not
  cap-determined in every year. (Because the cap is a *sufficient* form and `surv < 1`, strict `slack > 0` holds
  mechanically whenever the cap binds; the informative object is therefore **where the cap does not bind**, and
  `slack` is reported per cell rather than used as a pass condition.)
- **(d-iii) outside-option responsiveness (the discriminating ablation).** The declared shock **child wage +10%**
  (`w_child → 1.10·w_child`, all countries, all years, arm declared in §5) must lower upper `completion_uis(2024)` by
  **≥ 2.0 pp**. If it does not, the level pattern is **pipeline-stipulated**, the sorting/outside-option account is
  **decorative**, and (d) is `MIXED` at best. Bar 2.0 pp is the programme's declared comparative-static bar
  (`shadow_module/PRE_DECLARATIONS.md` §8 c2(ii)); it is a **declared bar, not a derived one**.
- **(d-iv) quality is an equilibrium, not a label.** The declared arm **Tier O quality −20%**
  (`q_O_mult → 0.80·q_O_mult`) must **raise** `unfilled_share_O` by **≥ 5.0 pp** (mean over 2010–2024, lower+upper).
  If take-up does not respond to Tier O quality, Tier O is not an equilibrium object.
- **Verdict.** `PASS` iff (d-i) ∧ (d-ii) ∧ (d-iii) ∧ (d-iv). `MIXED` iff (d-i) ∧ (d-ii) hold but (d-iii) or (d-iv)
  fails — **and the report must name which**. `FAIL` iff ¬(d-i) ∨ ¬(d-ii). `UNDETERMINED` iff an arm is missing.
- **Declared statement (frozen):** a synthetic PASS here says only *"the declared tier structure can produce the
  pattern without a free taste parameter"*. It is **non-diagnostic** unless the (d-iii)/(d-iv) ablations move the
  objects (D81 rule), which is why they are inside the check rather than beside it. It is **never** a statement
  about Philippine demand.

### (e) No-re-fit guards — **two orthogonal switches**, declared in advance

- **(e-i) `bimodal OFF + κ OFF` ⇒ byte-for-byte v1.3.** Arm **A00** writes a panel with **exactly** v1.3's column
  header, row order and `%.10g` formatting; its sha256 **must equal**
  `47d4b082f4ba5838cc20fbb09e59dd3dd847ad25393b1ce091069c94496657e3`. The v1.4 convention is verified on disk
  (`generator_v1_4_demand/results/_ablation/synthetic_panel_v1_4_demand_off.csv` hashes `47d4b082…`).
  A mismatch ⇒ **`BASELINE-GUARD-FAIL`**, the A11 result is **`INVALID`**, no check is scored, and **the failure is
  the finding**.
- **(e-ii) `bimodal OFF + κ ON` ⇒ the linked arm.** Arm **A01** is a **new panel**, reported **separately**; it is
  **never** compared for identity and its differences are **not** a defect. Three sub-guards:
  (1) `primary`, `lower_secondary`, `tertiary` columns **cell-identical** to v1.3 in all 6 720 rows;
  (2) `upper_secondary` rows differ **only** where the cap binds (`adm_upper` reduced) — every differing row is
  listed in `results/KAPPA_BIND_CELLS.csv`;
  (3) **0/53** violations of `comp_uis_upper(t) ≤ κ·comp_uis_lower(t−3)` in the 53 scored anchor cells
  (1973–2025; 1970–1972 `NOT-SCORABLE`, never imputed).
  A breach of (1) or (2) ⇒ **`KAPPA-GUARD-FAIL`**; the pipelink result is recorded `INVALID`.
- **(e-iii) frozen-file invariance.** Every file under `generator_v1_2/`, `generator_v1_3/`,
  `generator_v1_4_demand/`, `shadow_module/`, `repro_path_2026-11-20/` has the **same sha256 after the run as
  before it** (`results/FROZEN_FILE_GUARD.json`, all hashes from `SHA256SUMS.txt`). **No file outside
  `generator_v1_5_bimodal/` is written.**
- **(e-iv) determinism.** Two clean runs of A11 into `results/` and `results/determinism_run2/`, all outputs
  **byte-identical**; seed `20261120`, one `PCG64` stream, the tier block draws **no** random numbers.
- **Verdict.** `PASS` iff (e-i) ∧ (e-ii) ∧ (e-iii) ∧ (e-iv). `FAIL` iff (e-i) fails. `MIXED` iff (e-i) holds and any
  of (e-ii)–(e-iv) fails (the guard is satisfied but the link leaked or the run is non-deterministic).
  `UNDETERMINED` iff a hash cannot be read.

### Construction audits (not checks; a failure VOIDS the run)

- **R1 — ratchet-by-construction audit.** Source inspection of the v1.5 transition rules finds **no** reversal term:
  no `restore`, no `revert`, no target-return feedback, no negative-feedback term toward a stored pre-installation
  level, no shock-contingent rule change; `Tstate` non-decreasing in every country-year; the opened-rung set
  non-decreasing. Recorded in `results/RATCHET_AUDIT.json` with the token list searched and the count of hits
  (required **0**). **R1 failure ⇒ the run is `VOID`** (a declared construction requirement, not a score).
  **R1 is not a reversal test and no reversal conclusion may be drawn from it** (§4).
- **R2 — monotonicity report (descriptive).** For every country: the year-sequence of `Tstate`, of the opened-rung
  count, and of the Tier H credential stock is reported as non-decreasing/decreasing. **Descriptive only; no
  inference.**

---

## 7. Verdict vocabulary (exactly this; nothing invented)

| token | meaning |
|---|---|
| `PASS` | every declared leg of the check holds, exactly as written |
| `FAIL` | the declared failing condition holds (each check defines its own) |
| `MIXED` | a declared subset holds and the rest do not — **the subset must be named in the report** |
| `UNDETERMINED` | a required column/arm/hash is missing or non-finite; **never** a substitute for a FAIL |

- **No other token may appear in a `verdict` field.** Guard rows use a separate field
  `guard_status ∈ {GUARD-PASS, GUARD-FAIL}` and the arm-level tokens
  `{BASELINE-GUARD-PASS, BASELINE-GUARD-FAIL, KAPPA-GUARD-PASS, KAPPA-GUARD-FAIL, FROZEN-FILE-GUARD-PASS,
  FROZEN-FILE-GUARD-FAIL, DETERMINISM-PASS, DETERMINISM-FAIL}` — these are **statuses**, not check verdicts, and
  may not be written into a `verdict` column.
- **Combined verdict** (`results/v1_5_checks.csv`, row `ALL`), precedence **FAIL > MIXED > UNDETERMINED > PASS**:
  **`FAIL` if any of (a)–(e) is FAIL, or the baseline guard or the link guard fails; else `MIXED` if any is MIXED;
  else `UNDETERMINED` if any is UNDETERMINED; else `PASS`.** Prose may explain but may not rename.
- **A MIXED or FAIL verdict is the deliverable at least as often as a PASS.** No rescue, no re-tune, no re-run to
  flip, no threshold change, no new arm.

---

## 8. No-threshold-change rule and the freeze procedure

1. The thresholds in this file — (a) `0.10`/`≥15 of 30`/`≥15 of 30`/`≥8 of 15`; (b) `[2014,2020]`/`primary 2024 ≥ 92`/`<90`/
   `[55,85]`/`[73.0,77.0]`; (c) `≥5.0×`/`≤0.025`/`≥+10.0 pp`/`≤+1.0 pp`; (d) `w_work_free = 0`/`slack ≥ 0`/
   `cap non-binding ≥ 5 of 53`/`≥2.0 pp`/`≥5.0 pp`; (e) the exact sha256 `47d4b082…` and the cell-identity rules; `κ = 0.949` (sensitivity
   0.960); the 3-year lag; 30 scored cells; 53 scored anchor cells; the four arms; the ten declared
   sensitivity/ablation arms — are fixed **at the sha256 recorded in `RUN_MANIFEST.json` and `SHA256SUMS.txt` before
   the first run**, and are reported against exactly as written.
2. **If a result sits on a boundary, the boundary as written decides and the proximity is reported.** No boundary is
   moved, before or after.
3. **No parameter may be changed after the freeze to flip a check.** A v1.5 that cannot produce a leg reports that
   leg as failed and the finding stands.
4. The build must **refuse to run** if `PRE_DECLARATIONS.md` sha256 ≠ the value in `RUN_MANIFEST.json`
   (`EXPECTED_PREDECL_SHA` embedded in the v1.5 code), or if any input hash in `SHA256SUMS.txt` differs.

---

## 9. Pre-freeze arithmetic (stated so the reader can see the bars were not chosen after the numbers)

**These are arithmetic from frozen files, NOT results. Every one is `LABEL: SYNTHETIC` (derived from the v1.3
panel) or `LABEL: OBSERVED` (from a data file).**

| quantity | value | derivation |
|---|---|---|
| v1.3 upper place-coverage 2024 (`seats/cohort`) | **0.9421** | `synthetic_panel_v1_3.csv`, `SYN00_PHL_LIKE`, upper, 2024 (identical to the v1.2 value) |
| v1.3 upper demand share 2024 | **0.8003** | same row, `demand_share` |
| v1.3 upper spare adequate places 2024 | **0.1418** of cohort | 0.9421 − 0.8003 |
| `K_H`(upper, 2024) at `h_share = 0.40` | **0.3768** of cohort | 0.40 × 0.9421 |
| `K_O`(upper, 2024) | **0.5653** of cohort | 0.60 × 0.9421 |
| max possible Tier O take-up | **0.4235** of cohort | 0.8003 − 0.3768 (all refused H candidates accept O) |
| ⇒ unfilled O at upper 2024 | **≥ 0.1418** of cohort = **≥ 25.1 %** of `K_O` | 0.5653 − 0.4235; **arithmetical**, hence (a) is declared a representation check |
| κ-implied upper ceiling 2024 | **63.9695** | 0.949 × 67.4073 (`comp_uis_lower` 2021, v1.3 panel) |
| observed PHL upper 2024 | **75.025** | `UNIVERSALIZATION_SERIES.csv:64` (`OBSERVED`) |
| ⇒ expected endpoint displacement | **−11.06 pp** vs observed; **outside [73,77]** | therefore **(b) expected `MIXED`** |
| v1.3 shadow `D_g2`(2020) / `D_g0`(2020) | **0.2606 / 0.0128** = **20.4×** | `synthetic_panel_v1_3.csv` shadow columns; so (c-i)'s 5× bar is structural |
| rung-4 absorption, anchor type, 2010+ median | **0.151** | V8, `SYNTHESIS_022.md:108` (computed on `synthetic_panel_v1_2.csv`; v1.3 2024 = 0.1888); so (a-iii)'s `p₄ ≤ 0.50` leg is expected to hold |
| observed PHL OOS upper-secondary 2024 | **22.884 %** | `UNIVERSALIZATION_SERIES.csv:483` (`OBSERVED`) |
| v1.3 upper `oos_rate` 2024 | **0.1997** (19.97 %) | `synthetic_panel_v1_3.csv`; the declared proxy comparison, distortion stated in `DESIGN.md` §8.2 |

**Where the bars come from, stated plainly.** The (a)/(c) bars are **declared**, chosen as round numbers above the
"10 % excess / 10 % unfilled" threshold that makes the coexistence non-trivial — not derived from any target. The
(b) bars are the **frozen v1.2 check-(a) bands**, carried over deliberately so that v1.5 is scored on the same
signature as v1.2 rather than on a band drawn around its own output. The (d-iii) 2.0 pp bar is the programme's
declared comparative-static bar. **No bar was chosen because a preliminary number was near it; no preliminary v1.5
number exists — nothing has been run.**

---

## 10. Output contract (what a run would produce; **nothing is produced by this delivery**)

| file | content |
|---|---|
| `results/v1_5_checks.csv` | one row per check (a)–(e) + the `ALL` row: `check, expected_pattern, synthetic_value, threshold, verdict, legs_passed, legs_failed, scope_note, label` |
| `results/v1_5_checks_detail.csv` | every leg of every check, with its computed statistic and cell counts |
| `results/BIMODALITY_CELLS.csv` | the 30 scored `(t, L)` cells × {`K_O, T_O, V_O, unfilled_share_O, A_H, K_H, queue_H, queue_ratio_H, p_adv_H, p₄`} |
| `results/TIER_PANEL_tabs.csv` | tier tabs: per country-year-level {`h_share, q_H, q_O, takeup_O, unfilled_O, admitted_H, queued_H, wage_H, wage_O, exit_cost_O`} |
| `results/synthetic_panel_v1_5.csv` | A11 panel: v1.3's 89 columns + the tier/κ columns |
| `results/panel_v1_5_A00_v13cols.csv` | A00 guard artefact: **exactly** v1.3's columns/format (E1) |
| `results/panel_v1_5_A01_linked.csv` | the **linked arm**, reported separately (E2) |
| `results/panel_v1_5_A10_bimodal_noKappa.csv` | the diagnostic arm (bimodal ON, κ OFF), reported, not scored |
| `results/BASELINE_GUARD.json`, `results/KAPPA_GUARD.json`, `results/KAPPA_BIND_CELLS.csv`, `results/FROZEN_FILE_GUARD.json`, `results/RATCHET_AUDIT.json`, `results/tier_audit.csv` | guards and audits (§6, §8) |
| `results/SENSITIVITY.csv`, `results/ABLATIONS.csv` | the ten declared arms, one row each |
| `results/determinism_run2/…`, `results/determinism_note.md` | E-iv |

Every file carries `label = SYNTHETIC` (or `OBSERVED` on a PHL row), the **D119 scope line**, and the
no-causal/no-direction statement. Floats `%.10g`. No timestamp, hostname, PID or wall-clock enters any output.

---

## 11. Language discipline (binding on every file this experiment produces)

1. **Banned phrase: "demand falsified"** — and every paraphrase of it ("demand absent", "demand does not respond",
   "demand is weak", "the demand hypothesis fails"). **Correct label:
   "the unrationed single-gate model cannot represent a bimodal system."** The A3-D result is a
   **model-specification failure**, and demand is **revealed and strong** (shadow education, queues for good
   schools, parental reaction to closures, credential chasing).
2. **No causal claim, no direction claim.** Nothing here says schooling causes anything, that any tier causes any
   outcome, or that the Philippines behaves like this model.
3. **Never evidence.** Every synthetic number is `LABEL: SYNTHETIC`; every PHL number is `LABEL: OBSERVED` and is
   used **only** as a band/anchor, never fitted.
4. **Never invented utilisation or quality.** No seat-utilisation number and no quality series exists on disk; the
   **HELD DATA ASK** (`DESIGN.md` §8.1) stands and no number is fabricated in its place. Declared proxies are
   `DERIVED` and carry their distortion.
5. **C1–C4 are not reopened**; no WT/DT cell is re-run or re-scored; no paper-test slate is added (D113b); the
   **tier-specific exit cost** is noted for the Council and **not tested** (§2.5, D101 unchanged).
6. **A3-D is not re-tuned** (no parameter moved, no check re-scored); the v1.4 `c4a`/`c4b` FAILs stand as delivered.
7. **The one-way ratchet is theory, not evidence**, and **no reversal diagnostic may be inferred** (§4).
8. **The A5 addendum's honesty bounds travel with every output:** D119 scope (crossing/endpoint placement),
   `m = 1.10` unchanged, `ENDPOINT-ONLY` carried from EXP-7, and D63 **`UNABLE as to cause`**.

---

## 12. Freeze declaration

This file was written **before any v1.5 computation**, contains **no result**, and is **not** an authorisation to
run. Its sha256 is recorded in `RUN_MANIFEST.json` (`predeclaration.sha256`) and in `SHA256SUMS.txt`, both written
after this file and before any run. **Run-ready, not run.**

**`LABEL: SYNTHETIC` — design + pre-declaration only — not evidence — no causal or direction claim — C1–C4 not
reopened — A3-D not re-tuned — HELD data stays HELD.**
