# EXP-17 JOINT-COVER — PRE-REGISTRATION

**Experiment:** EXP-17 **JOINT-COVER** — is there **one declared coverage path** that satisfies **both** lower
channels at once?
**Authority:** Council brief 024 (`08_council/brief_024/SYNTHESIS_024.md` §5.2), adopted as **D145 #2, rank #2**;
batch ruling **D142**; process rules **D147**.
**Worker:** JC, cycle 16. **Written and hashed before the script that evaluates the equation was executed.**
**Scope of writes:** `10_massification/extensions/joint_cover_2026-11-20/` only. **No other file on disk is
created, modified or moved.** All inputs are read-only.
**Labels used throughout.** Panel values and everything computed *from* them = `SYNTHETIC`; the requirement
`0.8076` = `DERIVED`; the observed PHL reference `80.8960494995` = `OBSERVED` (**reported only, never in the
verdict path**); the laws' constants = `DECLARED` / `CONVENTION` as marked in §2.3. **No causal claim and no
direction claim is made anywhere in this experiment.** The equation says *what state the declared law would
require*; it says nothing about what raises completion anywhere, nothing about the Philippines, and nothing about
policy.

---

## 0. Freeze protocol

1. This file is written **before** `code/run_joint_cover.py` is executed. Its sha256 is recorded in
   `PRE_DECLARATIONS.sha256`, embedded **in the script**, and embedded in `RUN_MANIFEST.json`. The script
   **refuses to run** if the embedded value and the file's actual sha256 disagree (the v1.2 freeze pattern).
2. **No threshold, tolerance, bracket, grid resolution, label, precedence rule or reporting rule in §3–§8 may
   change after the run.** The verdict is whatever the frozen rules return. A label the analyst did not expect
   stands and is discussed in `FINDINGS.md`; it is not re-specified.
3. **No re-fit, no new parameter, no generator run, no re-scoring of EXP-13 or EXP-14.** The panel, the
   simulation source and `PARAMS.md` are read-only inputs. The only executable is this cell's own arithmetic on
   frozen output plus the declared laws.
4. **Blindness disclosure (D147's standard; the EXP-14 C-5 lesson applied at freeze, not after it).** Before this
   freeze the analyst executed **no evaluation of the equation at any λ**, and no grid, bisection or root-finder
   was run. What *was* known before the freeze is stated here so that no later sentence can imply more blindness
   than the record supports:
   (i) the value of the equation at the declared anchor **λ = 1**, which is D142's delivered chain
   (`1.10 × 0.783805 × 0.781819 = 0.6740731179`, re-derived at intake from the frozen panel per D113a) — an
   **anchoring number**, not a result of this cell;
   (ii) the **λ-structure** of the declared law, which is algebra (§7): both channels are non-decreasing in λ, so
   the declared law admits **at most one** root on the bracket except on a measure-zero plateau. §7 states that
   consequence in advance rather than leaving it to be discovered afterwards.
   **What this cell adds, and what was not computed before the freeze:** the number `λ*`, the implied coverage at
   both years, the implied `(a, s)` pair, the law's maximum over the bracket, and the falsifier.
5. If the frozen rules do not determine a case, the case is reported as `UNDETERMINED` with its reason in
   `results/JOINT_COVER_RESULTS.csv`; the label is not adjusted to hide it.

---

## 1. The Council block, verbatim

> Reproduced **verbatim** from `08_council/brief_024/SYNTHESIS_024.md` §5.2 (lines 461–503). Nothing in this
> quotation is paraphrased. **The block's definitions and thresholds are the binding ones**; §2–§9 below only
> *operationalise* them and are void where they conflict with this quotation.

> ### 5.2 EXP-17 — **JOINT-COVER**: is there a *single declared coverage path* that satisfies both lower channels at once? (rank **#2**)
>
> 1. **First-order link (cohort flows + schooling supply, lower series).** The lower-secondary series delivers
>    **0.5861505373** at 2021 in A10 (**58.61505373 pp**) against the internal requirement **0.8076**, because the gate's
>    entry admission and the survival law are **both functions of one object** — adequate-place coverage `seats/cohort`
>    (`gate = min(1.15·seats, 1.05·cohort)/cohort`; `surv = 0.91·exp(−0.55·max(0, cohort/seats − 1))`). D140's `JOINT`
>    label is a statement about **two channels**; the question this cell answers is whether they are in fact **one
>    lever** — i.e. whether a single declared coverage path can satisfy the required state **at both years** (entry and
>    completion) simultaneously.
> 2. **What changes if positive vs negative.** **`SINGLE-LEVER-IDENTIFIED`** (unique required uplift in range) → the
>    lower defect becomes a **coverage requirement** with **one** number; the successor declares a coverage path, **not**
>    two channels, and D140's split-language is **superseded** by "one object, two channels, one required state" (the
>    shares remain reported, and remain unidentified as separate levers). **`LAW-INCOMPATIBLE`** (no uplift reaches the
>    requirement) → the declared law family cannot produce the cell, any lower repair would require a **law
>    re-declaration** with its own justification (a different, larger act, **not** licensed this cycle), and the
>    successor's lower cells are known-failing **before** it is built. **`MULTIPLE`** → the requirement is not
>    identified by coverage alone and the successor must declare an interval, not a point.
> 3. **Why it is not a niche.** The lower series is the named defect of the whole generator line and the successor's
>    lower cells are **0/11**. If the defect is one declared coverage number, the successor's predeclaration has a
>    **parameter**; if it is a law incompatibility, the successor cannot pass by any admissible route and building it
>    would be a guarantee of failure. Either way the answer fixes the successor's parameter provenance **before** it is
>    frozen — which is exactly what D134(3)/D140 demanded and what cycle 15 could not supply.
> 4. **Data on disk (no DATA ASK).** `synthetic_2026-11-20/generator_v1_2/results/synthetic_panel_v1_2.csv` — `seats`,
>    `cohort`, `seat_coverage`, `congestion_q`, `quality_q`, `survival`, `completion_uis`, `measurement_factor`;
>    `generator_v1_2/PARAMS.md` — `surv_max = (0.96, 0.91, 0.90, 0.90)`, `theta = 1.0` (lower), `gamma = 0.55`,
>    `phys_cap = 1.15`, `overage_cap = 1.05`; `lower_def_2026-11-20/results/LOWER_DEF_DETAIL.csv` for the verified chain
>    (`admission_rate`, `survival`, `chain_reconstruction`, `chain_abs_error`); the internal requirement **0.8076** and
>    the observed reference **80.8960494995** (labelled `OBSERVED`, reference only).
> 5. **Threshold + falsifier (fixed before the run).** One declared unknown: a **multiplicative coverage uplift `λ`**,
>    applied to the panel's own coverage path at **both** the entry year and the completion year (so the *path shape* is
>    the panel's and only its level moves). Solve, for `λ ∈ [0.5, 2.0]`,
>    `m · min(1.15·λ·seats(t−3), 1.05·cohort(t−3))/cohort(t−3) · 0.91·exp(−0.55·max(0, cohort(t)/(λ·seats(t)) − 1)) =
>    0.8076` at the 2021 completion / 2018 entry cell. **Report:** the root set, `λ*`, the implied coverage at both
>    years, the implied `(a, s)` pair, the implied `phys_cap·coverage`, and the required-vs-realised gap. **Verdict:**
>    unique root in range → `SINGLE-LEVER-IDENTIFIED`; no root → `LAW-INCOMPATIBLE`; more than one → `MULTIPLE`. Also
>    report the **law's maximum** of the product over `λ` (so "no root" is distinguishable from "root outside range").
>    **Falsifier:** if the `λ = 1` chain does not reproduce the panel's 2021 `completion_uis` to **1e-9**, the accounting
>    is not the one executed → **`UNDETERMINED`**, and no λ is reported.
> 6. **Closed-claim check.** Pure read-only arithmetic on the declared laws plus the frozen panel; **does not re-run the
>    generator**; **does not re-score EXP-13** (it consumes the verified chain and changes none of its shares); **adopts
>    no λ** (the value is a required state, not a parameter); no fit; no direction claim; D140's label is not reopened.
> 7. **Cost / rank.** **Small** (one deterministic script, no RNG, no model run). **Rank #2** — it is the successor's
>    lower-parameter provenance and can **retract D140's action-reading** before it is cited again.

### 1.1 The adopting decision (D145), verbatim

> Reproduced **verbatim** from `08_council/DECISIONS.md`, row **D145**, the EXP-17 clause:

> **EXP-17 JOINT-COVER** — is there **one declared coverage path** satisfying both lower channels? (one declared unknown λ = multiplicative uplift on the panel's own coverage path at both entry and completion years; solve m·min(1.15λ·seats(t−3), 1.05·cohort(t−3))/cohort(t−3) · 0.91·exp(−0.55·max(0, cohort(t)/(λ·seats(t)) − 1)) = 0.8076 on λ∈[0.5,2.0]; unique root → SINGLE-LEVER-IDENTIFIED, none → LAW-INCOMPATIBLE, >1 → MULTIPLE; report λ*, implied coverage at both years, implied (a,s) pair and the law's maximum; **no λ adopted**; falsifier: λ=1 must reproduce the panel's 2021 completion_uis to 1e-9 else UNDETERMINED) **#2**;

### 1.2 The batch conditions that travel with this cell (D142, D143, D147)

- **D142 (EXP-13 row):** chain error at the verdict cell **1.91465732158e-11** (tol 1e-9), max over 53 scored cells
  **2.05882477733e-10**; `a*` **0.939069193922** (required entry coverage **0.816581907758** vs realised
  **0.681569976**, `REACHABLE-BY-CAPACITY`); `s*` **0.936688813872** > `surv_max` **0.91**; ceiling
  **0.784589277801**, **2.301072 pp** short; **target provenance 80.76 internal vs 80.896 observed (+0.136 pp)
  travels with every downstream cell**; the successor **scores 2021 and reports the whole path**.
- **D143 (ix):** D140's **action-reading is corrected** — the split is unidentified over weight
  `[0.466649, 0.525137]`, and **"fix survival only" is barred** by the block's own reachability finding. This cell
  does **not** reopen D140's label and does not change any of its shares.
- **D147 (c):** the four authoring rules bind here — **(i) precedence** is stated in §5.1; **(ii) resolution
  pretest**: this cell's only "shock" is the declared λ-uplift, and its resolution is checked in §4.6 (the shift
  moves the gate and the survival term, or the cell is `UNFIRABLE-BY-DESIGN`); **(iii) arm tuple**: this cell has
  **one arm** and **no switches** — `arm = (panel = synthetic_panel_v1_2.csv, country = SYN00_PHL_LIKE, level =
  lower_secondary, bimodal = n/a, kappa = n/a, t = 2021, t−3 = 2018)`, so the capability lint is trivially
  satisfied and is asserted in code (§4.7); **(iv) count-blind**: this cell computes **no observed-path count**,
  reads no 33-cell object, and emits no deviation from the observed series — the only `OBSERVED` number on disk
  is the reference in §6.2 item 5, and it is not read by the verdict arithmetic.

---

## 2. The equation (as declared in the block, clause 5), and its components

### 2.1 Symbolic form (no content changed)

```
F(λ) = m · G(λ) · S(λ)

G(λ) = min(1.15 · λ · seats(2018), 1.05 · cohort(2018)) / cohort(2018)      "the gate"    (entry year)
S(λ) = 0.91 · exp( −0.55 · max(0, cohort(2021) / (λ · seats(2021)) − 1) )   "the law"     (completion year)
F(λ*) = 0.8076                                                              the required state
λ ∈ [0.5, 2.0],   m = 1.10 frozen
```

The two years are fixed by the block: **completion year `t = 2021`**, **entry year `t − 3 = 2018`**, with the
lower-secondary duration **3 y** (`DVEC = (6,3,3,4)`). No other year is scored; §6.2 item 4 reports the same
computation at other years as **context only**.

`λ` multiplies **the panel's own seats path at both years and nothing else**: `seats(y) → λ · seats(y)`. The
**shape** of the coverage path is the panel's; only its **level** moves, by one common factor. That is what makes
this a *single declared lever* rather than a two-parameter repair: **one** unknown, moved at both years together.

### 2.2 The two channels are one object (why the equation has this form)

Under the declared laws the gate and the survival term are both functions of the **same** ratio
`coverage = seats/cohort`:

```
gate(y)   = min(phys_cap · seats(y), overage_cap · cohort(y)) / cohort(y)   phys_cap = 1.15, overage_cap = 1.05
q(y)      = cohort(y) / seats(y)                 (congestion, "frozen spec")
Q(y)      = exp(−gamma · max(0, q(y) − 1))       gamma = 0.55
surv(y)   = clip(surv_max · Q(y)^theta, 0.02, 0.995)   surv_max = 0.91 (lower), theta = 1.0
row       = m · gate(t − 3) · surv(t)            m = 1.10
```

so raising coverage raises the gate **and** lowers congestion **and** raises survival — the block's "one object,
two channels". `λ` is therefore not a decomposition of the two channels; it is the **single number** the declared
law would require if the two channels are to be satisfied **by one coverage path**.

### 2.3 Declared constants — all copied, none fitted, none new

| quantity | value | label | source (file:line / decision) |
|---|---|---|---|
| `m` = `meas_completion_factor` | 1.10 | `CONVENTION` | `generator_v1_2/code/sim_v1_2.py:133`; `PARAMS.md` §7 |
| `phys_cap` | 1.15 | `DECLARED` | `sim_v1_2.py:109`; `PARAMS.md` §4.1 |
| `overage_cap` | 1.05 | `CONVENTION` | `sim_v1_2.py:110`; `PARAMS.md` §4.1 |
| `surv_max` (lower) | 0.91 | `DECLARED` | `sim_v1_2.py:113`; `PARAMS.md` §4.1 |
| `surv_theta` (lower) | 1.0 | `DECLARED` | `sim_v1_2.py:114`; `PARAMS.md` §4.1 |
| `gamma` | 0.55 | `DECLARED` | `sim_v1_2.py:112`; `PARAMS.md` §4.1 |
| `DVEC` (lower) | 3 y | `DECLARED` | `sim_v1_2.py:65` |
| clip bounds, survival | [0.02, 0.995] | `DECLARED` | `PARAMS.md` §4.1; v1.6 `PARAMS.md` |
| required value | **0.8076** | `DERIVED` | D133/D140: `76.6391 / 0.949 = 80.7577` → 80.76 at 2 dp |
| bracket | [0.5, 2.0] | `DECLARED` (block) | §5.2 clause 5 |
| falsifier tolerance | 1e-9 | `DECLARED` (block) | §5.2 clause 5 |
| grid resolution | N = 6001 points, step 2.5e-4 | `DECLARED` here | §4.2 |
| root acceptance | abs residual ≤ 1e-12 **and** bracket width ≤ 1e-12 | `DECLARED` here | §4.5 |
| method agreement | ≤ 1e-9 in λ | `DECLARED` here | §4.4 |
| output precision | `%.12g` (grid, implied) / `%.15g` (root, residuals) | `CONVENTION` here | §6.5 |

**The target's provenance (D142 C-4 — must travel).** `0.8076` is **`DERIVED`**, not observed: it is the
lower-secondary 2021 value that would hold the model's **own delivered** upper-secondary 2024 = **76.6391** under
the declared **κ = 0.949** (`76.6391/0.949 = 80.7577`). It is an **internal-consistency requirement** of the
declared generator line. It is **not** an external standard, **not** a policy target, **not** a forecast, and
**not** the Philippines. The observed PHL lower-secondary 2021 value **80.8960494995** (`OBSERVED`,
`UNIVERSALIZATION_SERIES.csv`, `status = observed`) sits **+0.136049 pp** away; it is reported **only** as a
reference (§6.2 item 5) and is **not** the target of this cell.

### 2.4 The panel anchors (read-only, `SYNTHETIC`)

From `synthetic_2026-11-20/generator_v1_2/results/synthetic_panel_v1_2.csv`, `SYN00_PHL_LIKE`,
`lower_secondary` (panel sha256 recorded in `RUN_MANIFEST.json`):

| quantity | value | row/column |
|---|---|---|
| `cohort(2018)` | 2435636.21 | year 2018, `cohort` |
| `seats(2018)` | 1660056.513 | year 2018, `seats` |
| `coverage(2018)` = `seats/cohort` | 0.6815699759 | year 2018, `seat_coverage` |
| `cohort(2021)` | 2376200.54 | year 2021, `cohort` |
| `seats(2021)` | 1862168.339 | year 2021, `seats` |
| `coverage(2021)` = `seats/cohort` | 0.7836747394 | year 2021, `seat_coverage` |
| `q(2021)` = `cohort/seats` | 1.2760395987 | year 2021, `congestion_q` |
| `survival(2021)` | 0.7818186593 | year 2021, `survival` |
| `completion_uis(2021)` | 0.6740731179 | year 2021, `completion_uis` |
| `demand_official(2018)/cohort(2018)` | 0.9547733465 | year 2018, `demand_official`, `cohort` |

The last row is not used by the equation. It is used by **one scope check** (§6.2 item 2): the equation's gate
term is the *capacity* term, and it is only the realised gate while
`1.15·λ·coverage(2018) ≤ demand_official/cohort`. The check is reported; it is **not** verdict-bearing.

---

## 3. Definitions (frozen)

1. **The declared unknown.** `λ` is a single dimensionless multiplicative uplift applied to the panel's
   `seats(y)` at **both** the entry year and the completion year. It is a **required state**, not a parameter of
   the generator and not an estimate (§8).
2. **The coverage path.** `coverage(y) = seats(y)/cohort(y)`, the panel's own column `seat_coverage`. The implied
   path is `λ·coverage(y)`; the implied seat count is `λ·seats(y)`.
3. **The two lower channels.** (a) the **gate** — entry admission, `min(1.15·seats, 1.05·cohort)/cohort`; (b) the
   **survival law** — `0.91·exp(−0.55·max(0, q−1))`. "Both channels satisfied" means the **product**
   `m · gate · survival` equals the required `0.8076` at the declared cell, with `m` frozen at 1.10.
4. **The scored cell.** `SYN00_PHL_LIKE | lower_secondary | 2021` with entry year 2018. Exactly one cell is
   verdict-bearing. No other type, level or year enters the verdict.
5. **What the equation does not include.** It does not include demand (`demand_official`), the eligibility pool,
   the over-age margin, or the tertiary block. It is the block's equation, not a superset of it; §6.2 item 2
   reports the one consequence of that (the capacity-regime check) and adopts nothing.

---

## 4. Root-finding protocol (declared before the run)

### 4.1 Bracket
`λ ∈ [0.5, 2.0]`, **closed**, as declared in the block. No point outside the bracket is used to find a root; the
bracket endpoints are evaluated **only** to report the "no root vs root-outside-range" distinction the block
requires.

### 4.2 Grid scan (uniqueness evidence, not the root)
`N = 6001` equally spaced points `λ_i = 0.5 + i·(1.5/6000)`, step `2.5e-4`, `i = 0…6000`. For each point record
`G`, the binding branch (`phys_cap` or `overage_cap`), `q`, `Q`, `S`, `F`, `F − 0.8076` and the sign of the
residual. A **sign change** is counted for every grid interval with `residual_i · residual_{i+1} < 0`. An
**exact grid zero** (residual within the §4.5 acceptance tolerance) is counted **once**, not twice. A
**plateau root** — an interval on which the residual is within tolerance at both endpoints — is counted as **two**
roots (the interval's ends) and is reported as `PLATEAU-ROOT` with its interval; this is the only way the declared
law can return more than one root (§7). The grid also reports the **monotonicity audit**: the number of grid
intervals on which `F` decreases by more than `1e-12` (expected 0; a non-zero count is `UNDETERMINED-METHOD`).

### 4.3 Bisection (the reported root)
For each sign-change bracket `[a, b]` from §4.2: bisect on the residual. Stop at the first of: bracket width
`≤ 1e-13`, `|residual(mid)| ≤ 1e-15`, or 300 iterations. The reported root is the midpoint of the final bracket.
**Acceptance:** `|F(λ*) − 0.8076| ≤ 1e-12` **and** final width `≤ 1e-12`; otherwise the cell is
`UNDETERMINED-METHOD`. The iteration trace (a, b, f(a), f(b), mid, f(mid), width) is written to
`results/JOINT_COVER_DETAIL.csv` as `bisect` rows.

### 4.4 Independent cross-check (Newton on the binding branch)
The declared law is smooth on the branch where the `phys_cap` term binds and `q > 1`:
`F = m · 1.15 · coverage(2018) · λ · 0.91 · exp(−0.55·(q/λ − 1))`, with analytic derivative
`F'(λ) = F(λ) · (1 + 0.55·q/λ) / λ`. Newton from `λ_0 = 1.2`, at most 100 iterations, stopping at
`|residual| ≤ 1e-15` or `|Δλ| ≤ 1e-15`. **Agreement rule, declared now:** `|λ*_bisect − λ*_newton| ≤ 1e-9`, else
`UNDETERMINED-METHOD` (a root that two independent methods cannot pin is not identified, and the cell says so
rather than reporting a number). `λ_0 = 1.2` is a **numerical seed**, not a prior and not a hypothesis about the
answer; it lies inside the bracket and above the anchor, and the method is reported with its seed.

### 4.5 Root acceptance tolerance
`1e-12` absolute on the residual, `1e-12` on the bracket width, `1e-9` on method agreement. These are
**numerical** tolerances, declared before the run; they are not thresholds on the substance and cannot change a
label except through the `UNDETERMINED-METHOD` rule, which is declared here.

### 4.6 Resolution pretest (D147 rule ii)
The declared λ-uplift must move **both** declared objects, or the leg is `UNFIRABLE-BY-DESIGN` and is not scored.
The check is analytic and is asserted in code at the root: `dG/dλ > 0` where the `phys_cap` branch binds, and
`dS/dλ > 0` where `q/λ > 1`, must both hold, and `|F(λ*+0.01) − F(λ*−0.01)| > 1e-6`. Reported as
`resolution_pretest` with both derivatives and the finite-difference magnitude.

### 4.7 Capability lint (D147 rule iii)
The declared arm tuple is `(panel = synthetic_panel_v1_2.csv, country = SYN00_PHL_LIKE, level = lower_secondary,
kernel = v1.2 declared laws, bimodal = n/a, kappa = n/a, completion year = 2021, entry year = 2018)`. The script
**fails the build** (non-zero exit, no results written) if: the panel file is absent; the required columns are
absent; the `SYN00_PHL_LIKE`/`lower_secondary`/2018 and 2021 rows are absent; `2018 + DVEC[lower] != 2021`; or the
declared predeclaration hash does not match. Every named object therefore **can** exist in the named arm.

---

## 5. Verdict function and precedence (frozen)

### 5.1 Precedence — declared now, because the block states none (D142 C-1 / D147 rule i)

The block names the three labels in the order `SINGLE-LEVER-IDENTIFIED` / `LAW-INCOMPATIBLE` / `MULTIPLE` but does
**not** state which wins when two could apply. **Precedence, declared before the run, tested in this order:**

1. **`UNDETERMINED`** — if the §5.3 falsifier fails, **or** if the §4.3/§4.4 numerical acceptance is not met, or
   if §4.2's monotonicity audit finds a decrease. **No λ is reported as a result** in that case (a number may be
   printed as an artefact with the label `NOT-A-RESULT`). *This rule is first because every other label is a
   statement about the equation's roots, and if the accounting or the solver is not the one executed, that
   statement is void.*
2. **`MULTIPLE`** — if the root count from §4.2 is `> 1`, including the plateau case. Precedes
   `SINGLE-LEVER-IDENTIFIED` by definition, and precedes `LAW-INCOMPATIBLE` because a cell with roots is not
   "no root".
3. **`LAW-INCOMPATIBLE`** — if the root count is `0`. With the sub-flag `ROOT-OUTSIDE-RANGE-LOW` if
   `F(2.0) < 0.8076` (the law never reaches the requirement up to 2.0) or `ROOT-OUTSIDE-RANGE-HIGH` if
   `F(0.5) > 0.8076` (the requirement is already met at the bottom of the bracket); reported with the law's
   maximum so the two readings are distinguishable, as the block requires. A third sub-flag
   `LAW-MAX-BELOW-TARGET` is added when `max_{[0.5,2.0]} F < 0.8076`, which is the exhaustive-negative reading.
4. **`SINGLE-LEVER-IDENTIFIED`** — exactly one isolated root in the closed bracket, accepted by §4.3 and §4.4.

Only these four labels may be returned. `FALSIFIER-FIRED` is never returned as a verdict word; the falsifier
returns `UNDETERMINED` (block, clause 5).

### 5.2 The verdict is about *coverage*, not about a repair
`SINGLE-LEVER-IDENTIFIED` means: **one** number `λ*` exists such that one declared coverage path, applied at both
years, satisfies both channels at the required value. It does **not** mean the coverage is achievable,
affordable, observed, or caused by anything. Those are other cells' questions (EXP-19 for measurement; no cell
for achievability, and none is licensed).

### 5.3 Falsifier (block, clause 5) — applied first, reported always
At `λ = 1` the equation must reproduce the panel's 2021 `completion_uis` to **1e-9** absolute:

```
| 1.10 · min(1.15·seats(2018), 1.05·cohort(2018))/cohort(2018)
      · 0.91·exp(−0.55·max(0, q(2021)−1))  −  completion_uis(2021) |   ≤   1e-9
```

A second, **diagnostic** comparison (same tolerance; does not fire the falsifier on its own but is reported with
it): the law's survival term at `λ = 1` against the panel's stored `survival(2021)`. A failure there while the
product passes is a **reporting-defect** note, not a verdict change.

**Falsifier-arm audit (D147 / EXP-11 C-1 discipline).** The falsifier has **one arm**. It **can** fire: the
product is a reconstruction from the stored `seats`, `cohort`, `survival`, `completion_uis` strings and the
declared constants, so any mismatch in the accounting — a wrong lag, a wrong `phys_cap`, a wrong survival law —
appears as a non-zero residual far above `1e-9`. The expected statistic under a correct accounting is the panel's
own print-rounding, of order `1e-10` (`%.10g` output), i.e. **below** the tolerance; the observed residual is
reported, not assumed. There is no signed test on an unsigned object here and no second arm carrying the label
(the two EXP-11 defect classes).

---

## 6. What is reported (frozen schema)

### 6.1 Required by the block
`λ*`; the root set (with the bracket each root was found in); the **implied coverage at both years**
(`λ*·coverage(2018)` and `λ*·coverage(2021)`) and the implied seats at both years; the **implied `(a, s)` pair**
(`a = G(λ*)`, `s = S(λ*)`) with the product check `m·a·s = 0.8076`; the implied `phys_cap·coverage` at entry; the
**required-vs-realised gap** (`0.8076 − F(1)`, in pp and in logs); and the **law's maximum** over the bracket.

### 6.2 Declared scope checks (reported, **non-verdict-bearing**)
1. **Law max vs the law's analytic bound.** `max_{[0.5,2.0]} F` equals `m · overage_cap · surv_max =
   1.10 · 1.05 · 0.91 = 1.05105` to `1e-12` **only if** the bracket reaches the fully saturated state (both caps
   binding). Both the grid maximum and the analytic bound are reported; a difference is not a failure, it is a
   statement about where the bracket ends.
2. **Capacity-regime check.** The equation's gate term is the *capacity* term; the realised gate would be
   demand-limited once `1.15·λ·coverage(2018) > demand_official(2018)/cohort(2018)`. The λ at which that happens
   (`λ_demand`) is reported, with `root_in_capacity_regime = (λ* < λ_demand)`. If the root lies **above**
   `λ_demand`, the reported `a` is flagged `EXCEEDS-DEMAND` — the *required* state is still reported, but the
   reader is told the equation would be over-stating the realised gate there. **This flag does not change the
   verdict** (the verdict is about the declared law's roots) and is declared now so that it can be used later
   neither to rescue nor to attack a label.
3. **Clip inactivity.** `S(λ)` is the declared law **without** its `clip(·, 0.02, 0.995)`. The clip is reported as
   inactive over the whole bracket if `0.02 ≤ S ≤ 0.995` at both endpoints **and** at the root.
4. **Same computation at other years (context, non-verdict-bearing).** The same arithmetic at `t = 2017, 2019,
   2020, 2022, 2023, 2024` (entry `t − 3`), each with its own bracket and root, reported as
   `context_by_year`. This is the D142/D143 requirement that the successor **report the whole path** rather than
   one year; it cannot change the 2021 verdict, adds no label, and **no** year is treated as an estimate of
   another.
5. **Observed-reference row (context, non-verdict-bearing).** The same solve against the **observed** reference
   `0.808960494995` (`OBSERVED`, +0.136049 pp above the derived requirement), reported as
   `reference_only_*`. It exists so that EXP-19 does not have to re-derive it and so that the +0.136 pp provenance
   delta is visible in one place. **It is not the requirement and no downstream cell may cite it as one.**

### 6.3 What is **not** reported as a result
No pp deviation of the panel from any observed series; no cell count over observed years; no "how far the model
is from the Philippines"; no achievable/affordable/implication reading of `λ*`. Those are outside this cell (the
observed-path counts belong to EXP-14/EXP-18).

### 6.4 Detail file
`results/JOINT_COVER_DETAIL.csv` carries the full grid, the sign-change brackets, the bisection trace, the Newton
trace, the critical λ points (`λ_cap`, `λ_demand`, `q(2021)`, bracket ends), the anchor row, and the by-year
context roots.

### 6.5 Precision and formatting
Values written at `%.12g` (grid, implied values) and `%.15g` (root, residuals, method agreement). The panel is
stored at `%.10g`, so a reconstruction carries print-rounding of order `1e-10`; the falsifier tolerance `1e-9`
absorbs it and the observed residual is reported (the EXP-13 pattern, `1.9e-11`).

---

## 7. What the declared law's structure implies before any evaluation (disclosed, not discovered after)

This section is algebra on the declared constants and the panel anchors of §2.4. It was written **before** the
script ran and is stated here so that the Council can see exactly how much of the answer is structure and how
much is measurement.

1. **The gate term is non-decreasing in λ and saturates.** `G(λ) = min(1.15·coverage(2018)·λ, 1.05)`; the
   `phys_cap` branch binds while `λ ≤ λ_cap = 1.05/(1.15·coverage(2018))`, above which `G = 1.05` exactly.
   (`λ_cap ≈ 1.34` on the anchors of §2.4; the exact value is reported by the run.)
2. **The survival term is non-decreasing in λ and saturates.** `q(2021)/λ ≤ 1` once `λ ≥ q(2021) ≈ 1.276`, at
   which point `S = 0.91` exactly and the `max(0, ·)` term is inactive.
3. **Therefore `F` is non-decreasing on `[0.5, 2.0]`, strictly increasing below `λ_cap`, and constant at
   `F = m·1.05·0.91 = 1.05105` above it.** *Consequence:* the declared law admits **at most one** isolated root on
   the bracket, and a second root can exist only on that plateau, i.e. only if the requirement equals `1.05105`
   exactly. **The verdict label is therefore largely implied by the declared structure; this cell's information is
   the number `λ*`, the implied `(a, s)`, the implied coverage and seats, and the falsifier — not the label.** That
   is stated here rather than presented afterwards as a discovery, and it is why `λ*` (not the label) is the
   object the successor consumes.
4. **At the anchor** `F(1) = 1.10 · 0.7838054723 · 0.7818186593 = 0.6740731179` (D142's delivered chain), which is
   **13.35268821 pp below** the requirement. Since `F(1) = 0.674073 < 0.8076 < 1.05105`, the root — if the
   accounting passes the falsifier — lies strictly inside the bracket and strictly below the plateau, i.e. in the
   **`phys_cap` branch with `q > 1`**, which is exactly the branch on which §4.4's Newton cross-check is valid.
5. `m` being an **uplift** (1.10 > 1) is why the requirement is not reachable by the convention: removing `m`
   widens the gap to 19.48 pp (D140). This cell does not move `m`; it is frozen.

**Nothing in this section is a substitute for the run:** the falsifier can still return `UNDETERMINED`, the solver
can still fail acceptance, and every *number* in §6.1 is produced by the script, not by this section.

---

## 8. No-adoption rule (binding on this cell and on every downstream cell)

1. **`λ*` is a required state, not a parameter.** It is the value the declared law would need; it is **not**
   adopted into any `PARAMS` block, not written into any generator, not used to re-score any cell, and not
   described as an estimate, a calibration or a measurement.
2. **No re-fit.** No constant in §2.3 is re-chosen, re-tuned or made year-specific. `m` is frozen at 1.10,
   `phys_cap` at 1.15, `surv_max` at 0.91, `gamma` at 0.55. Changing any of them to move `λ*` is `FAIL-RE-FIT`.
3. **No grid search for a level bar.** The grid in §4.2 exists to count roots and to evidence monotonicity. No grid
   cell is adopted, and no alternative `λ` is reported as a preferred value.
4. **Downstream citation rule.** EXP-18/EXP-19 may cite `λ*` **only** as `REQUIRED-STATE (EXP-17)` with the target
   `0.8076` and its `DERIVED` label attached; they may **not** cite it as an observed, achievable or calibrated
   coverage, and they may not round it into a declared parameter. Any use that drops the label is a
   `FAIL-RE-FIT`-class defect.

---

## 9. Closed claims (no rescue, no reopening)

- **Pure arithmetic** on the frozen panel plus the declared laws. **No generator was run**; no model code was
  imported; the panel, `sim_v1_2.py` and `PARAMS.md` are read-only inputs.
- **Does not re-score EXP-13.** It consumes the verified chain (`0.6740731179`) and changes none of D140's shares,
  none of its labels and none of its reachability verdicts. It does **not** reopen D140's `JOINT` label.
- **Does not re-score EXP-14**, does not re-freeze any of its checks, and carries no observed-path count.
- **No causal claim, no direction claim.** The equation says what coverage the declared law would require at one
  cell. It does **not** say that expanding places raises completion, that coverage causes survival, or anything
  about the Philippines. D63 remains `UNABLE as to cause`; the phase verdict and the scaling `FAIL` are untouched.
- **Not a target, not a forecast, not a policy input.** `0.8076` is the model's own internal-consistency
  requirement (§2.3) and `λ*` is its arithmetic consequence.
- **Synthetic ≠ observed.** Every number in the verdict path is `SYNTHETIC` or `DERIVED` from `SYNTHETIC` values.
  The single `OBSERVED` number (80.8960494995) appears in §6.2 item 5 only.
- **Determinism.** `code/run_joint_cover.py` uses no RNG, no clock, no network, no hash-order dependence, no
  locale-dependent formatting. Two independent executions must produce **byte-identical** files; the second run
  is stored in `results/determinism_run2/` and compared by sha256 in `RUN_MANIFEST.json`.

---

## 10. Files this experiment will write

| file | contents |
|---|---|
| `code/run_joint_cover.py` | the frozen arithmetic and root-finder (read-only on all inputs; refuses to run on a predecl hash mismatch) |
| `code/make_manifest.py` | manifest + checksums builder (deterministic; no clock) |
| `results/JOINT_COVER_RESULTS.csv` | falsifier, root(s), `λ*`, implied coverage/`(a,s)`, law max, checks, verdict |
| `results/JOINT_COVER_DETAIL.csv` | full grid, sign-change brackets, bisection trace, Newton trace, critical λ, by-year context |
| `results/INPUT_HASHES.json` | sha256 of every input read |
| `results/determinism_run2/` | byte-identical second execution |
| `FINDINGS.md`, `RUN_MANIFEST.json`, `SHA256SUMS.txt` | report, manifest, checksums |

**Declared verdict vocabulary is closed. Declared thresholds and tolerances are frozen. No λ is adopted.
Signed: WORKER JC, before the run.**
