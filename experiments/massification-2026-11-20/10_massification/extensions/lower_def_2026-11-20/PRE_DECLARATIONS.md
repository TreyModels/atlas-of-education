# EXP-13 LOWER-DEF — PRE-REGISTRATION

**Experiment:** EXP-13 **LOWER-DEF** — where does the lower-secondary series lose its **13.35 pp**?
**Authority:** Council brief 023 (`08_council/brief_023/SYNTHESIS_023.md` §6.3), adopted as **D136 #3, rank #3**.
**Worker:** LD. **Written and hashed before the script that produces any share or verdict was executed.**
**Scope of writes:** `10_massification/extensions/lower_def_2026-11-20/` only. Nothing else on disk is modified.
**Labels:** panel arithmetic = `SYNTHETIC`; the PHL reference series = `OBSERVED`; required value, capacities and
allocation rules = `DERIVED` / `DECLARED` as marked. **No causal claim and no direction claim is made anywhere in
this experiment.** The decomposition says *where the arithmetic of the declared chain sits*, not *why Philippine
lower-secondary completion is what it is*.

---

## 0. Freeze protocol

1. This file is written **before** `code/run_lower_def.py` is executed. Its sha256 is recorded in
   `PRE_DECLARATIONS.sha256` and in `RUN_MANIFEST.json`.
2. **No threshold, tolerance, label, precedence rule or allocation rule in §5–§7 may change after the run.**
   The verdict is whatever the frozen rules return. If a rule returns a label the analyst did not expect,
   the label stands and is discussed in `FINDINGS.md`; it is not re-specified.
3. **No re-fit, no new parameter, no re-run of the generator, no re-scoring of EXP-7 or of v1.5.** The panel and
   the code are read-only inputs. The only executable is this experiment's own arithmetic on frozen output.
4. If the frozen rules do not determine a case, the case is reported as an **unresolved component** in
   `results/LOWER_DEF_RESULTS.csv` and the overall label is **not** adjusted to hide it.

---

## 1. The Council block, verbatim (SYNTHESIS_023.md §6.3, lines 474–508)

> Reproduced **verbatim** from `08_council/brief_023/SYNTHESIS_023.md`; nothing in this quotation is paraphrased.
> The block's definitions and thresholds are the binding ones; §2–§7 below only *operationalise* them and are void
> where they conflict with this quotation.

### 6.3 EXP-13 — **LOWER-DEF**: where does the lower-secondary series lose its 13.35 pp? (rank **#3**)

1. **First-order link (cohort flows + schooling supply, with measurement).** Whether the **named defect** of the whole
   generator line — the lower-secondary series, **required 80.76 vs realised 67.4073** (V12) — is a **rationing**,
   a **survival/quality**, or a **convention** problem, since the repair's target depends on which.
2. **What changes if positive vs negative.** **`RATIONING-CARRIED`** → the repair must act on the **lower gate**
   (`admitted_official/cohort`, 0.783805 in 2018), which is a **capacity** object. **`SURVIVAL-CARRIED`** → it must act
   on the **quality/congestion → survival** law (`0.781819` in 2021), which is a **tier-quality** object and connects
   directly to §5.3. **`CONVENTION-CARRIED`** → the `m = 1.10` constant or the duration vector is doing it, which is a
   **measurement** problem. **`JOINT`** → no single lever is admissible and the repair must move both, with a declared
   joint target. In every case the repair's parameter provenance is fixed **before** V16-REPAIR runs.
3. **Why it is not a niche.** It is the one number that every level claim in v1.2/v1.3/v1.4/v1.5 inherits: EXP-7's
   class **b2** says the **lower** series is the binding defect, and v1.5 widened the gap (**A11 lower 2021 = 43.73**,
   **37.03 pp** short). Without this decomposition the repair would be guessing which block to change — which is how
   target-fitting starts.
4. **Data on disk (no DATA ASK).** `synthetic_panel_v1_2.csv` — `completion_uis`, `completion_cohort`, `survival`,
   `admitted_official`, `cohort`, `measurement_factor` (lower_secondary, SYN00_PHL_LIKE, 2017–2021);
   `generator_v1_2/code/sim_v1_2.py:604-610` and `DVEC = (6,3,3,4)` (lower duration **3**); observed reference
   `UNIVERSALIZATION_SERIES.csv` (`completion_lower_secondary`, PHL 2021 = **80.896**). Verified chain:
   `1.10 × 0.783805 × 0.781819 = 0.674073` = the delivered `completion_uis` **exactly**.
5. **Threshold + falsifier (fixed before the run).** Declared log decomposition
   `ln comp = ln m + ln(adm_rate at t−3) + ln surv`; attribute the gap `ln(0.8076) − ln(0.674073)` (i.e. to the
   **required 80.76**, re-derived as `76.6391/0.949`) across the three factors under a declared **equal-split
   (Shapley) attribution**. **`X-CARRIED` iff factor X ≥ 50 % of the gap; `JOINT` iff the two largest factors are within
   **10 percentage points** of each other; `UNDETERMINED` if the chain identity fails in any scored year (tolerance
   1e-9).** **Falsifier:** if the chain does not reproduce `completion_uis` exactly, the accounting is not the one
   executed and the experiment reports `UNDETERMINED` — it does **not** re-derive its own model. Secondary
   (non-verdict-bearing): the same decomposition on **all 30 country types**, and the width of the gap at 2017, 2022,
   2024, so the Lead can see whether the shortfall is local to 2021.
6. **Closed-claim check.** Pure arithmetic on frozen output plus one frozen code line; **no re-fit, no new parameter, no
   re-run, no re-scoring of EXP-7**. Does not reopen class **b2** or the endpoint object; makes no claim about observed
   Philippine cause.
7. **Cost / rank.** **Small.** **Rank #3** — it is cheap, it gates the repair's parameter choice, and it is the
   "one thing that mattered" of the step-back.


---

## 2. The chain identity (as declared in the block, clause 5)

The block declares one identity and one gap. Restated symbolically **without changing any content**:

```
completion_uis(level L, year t) = m · admission_rate(L, t − DVEC[L]) · survival(L, t)
admission_rate(L, y)           = admitted_official(L, y) / cohort(L, y)
DVEC[lower_secondary]          = 3            (declared duration, sim_v1_2.py:65)
m                              = 1.10         (meas_completion_factor, sim_v1_2.py:133)
```

At the verdict cell (`SYN00_PHL_LIKE`, `lower_secondary`, 2021) the block declares

```
1.10 × 0.783805 × 0.781819 = 0.674073
```

**Identity check (falsifier, block clause 5).** For every scored cell the reconstruction
`m · admission_rate(t − 3) · survival(t)` is compared with the panel's stored `completion_uis` at **absolute
tolerance 1e-9**. Any scored cell failing → **`UNDETERMINED`**. The experiment does **not** re-derive its own model
in that case.

**Rounding rule, declared now (not a tolerance change).** The panel is written at 10 significant digits
(`%.10g`), so a reconstruction from stored strings carries print-rounding of order 1e-10 and the 6-decimal
constants printed in the block (`0.783805`, `0.781819`, `0.674073`) carry up to 5e-7. Accordingly:

- **Primary falsifier check** = full-precision reconstruction from the stored panel, tolerance **1e-9** (as declared
  in the block). This is the only check that can produce `UNDETERMINED`.
- **Display reproduction** = the block's 6-dp constants, reported separately with tolerance **5e-7**. A display
  deviation is a printing artefact and is **not** an identity failure; it is reported either way.

**Scored cells.** The verdict-bearing identity scope is `SYN00_PHL_LIKE` / `lower_secondary` / every year with a
lagged entry year (`t − 3 ≥ 1970`), i.e. **1973–2025** — the full series, not only 2021. The other three levels of
the same type are reported **descriptively only** (see §6.3 for why they cannot bear on the verdict).

---

## 3. The gap (as declared in the block, clause 5)

```
G_log = ln(0.8076) − ln(m · admission_rate · survival)
G_pp  = 100 × (0.8076 − m · admission_rate · survival)
```

- **Required** = `0.8076` (**80.76 %**), `DERIVED`: `76.6391 / 0.949 = 80.7577` → 80.76 at 2 dp, per V12/D133 —
  the lower-2021 value that would hold the model's own delivered **upper 2024 = 76.6391** under **κ = 0.949**.
  **It is an internal-consistency requirement, not an external standard, not a policy target, and not a forecast.**
- **Realised** = the chain value at the verdict cell (`SYNTHETIC`).
- Both the log gap and the pp gap are reported. The pp gap is the block's "**13.35 pp**".

**Observational reference, reported and non-verdict-bearing:** `UNIVERSALIZATION_SERIES.csv`
(`completion_lower_secondary`, PHL, 2021) = **80.896** (`status = observed`). It is reported for orientation only;
no statement is made about the observed Philippine cause, and the observed series is never used to fit anything.

---

## 4. Declared constants and provenance (nothing fitted, nothing new)

| quantity | value | label | source |
|---|---|---|---|
| `m` = `meas_completion_factor` | 1.10 | `CONVENTION` | `generator_v1_2/code/sim_v1_2.py:133`; PARAMS.md |
| `DVEC` lower duration | 3 y | `DECLARED` | `sim_v1_2.py:65` |
| admission rate at entry | `admitted_official/cohort` at `t − 3` | `DECLARED` rule | `sim_v1_2.py:604-610` (`a_entry = adm_hist[...]`) |
| `survival` | panel column, `= clip(surv_max·Q^theta, 0.02, 0.995)` | `SYNTHETIC` | panel; PARAMS.md §4.1 |
| `surv_max` lower | 0.91 | `DECLARED` | PARAMS.md §4.1 |
| `surv_theta` lower | 1.0 | `DECLARED` | PARAMS.md §4.1 |
| `gamma` | 0.55 | `DECLARED` | PARAMS.md §4.1 |
| `phys_cap` | 1.15 | `DECLARED` | PARAMS.md §4.1 |
| `overage_cap` | 1.05 | `CONVENTION` | PARAMS.md §4.1 |
| required `0.8076` | 80.76 % | `DERIVED` | V12/D133 (`76.6391/0.949`) |
| identity tolerance | 1e-9 | `DECLARED` in block | §6.3 clause 5 |
| `X-CARRIED` threshold | 50 % | `DECLARED` in block | §6.3 clause 5 |
| `JOINT` window | 10 percentage points | `DECLARED` in block | §6.3 clause 5 |

No parameter is estimated, tuned or selected in this experiment. `m`, `surv_max`, `phys_cap` and the required value
enter as constants copied from frozen files.

---

## 5. Attribution rule D1 — the declared equal-split (Shapley) attribution (**verdict-bearing**)

The block declares the decomposition `ln comp = ln m + ln(adm_rate at t−3) + ln surv` and an **equal-split (Shapley)
attribution** of the gap across the three factors. Because the function is **additive in logs**, the Shapley value
of an additive game is each factor's own log term, so all that has to be declared is the **required state**
`(m*, a*, s*)` — the factor values at which the required product `0.8076` holds. One equation, three unknowns:
**the required state is not identified from the data on disk.** D1 therefore declares it and says so:

**D1 (declared, verdict-bearing).**

1. **The convention is held at its declared value: `m* = m = 1.10`.** `m` is a declared constant applied uniformly
   to every cell and level; it is not a state variable of the panel and cannot be moved by a repair of the lower
   series. Choosing `m` by reference to a level bar is `FAIL-RE-FIT` under D134, and the convention question is
   assigned to **EXP-15 CONV-REG**. So the required state does not re-open the convention.
2. **The residual required log product is split equally between the two state factors:**
   `a* = s* = exp( ½ · ln(0.8076 / 1.10) )`.
3. **Contribution** of factor *i*: `c_i = ln(x_i* / x_i)`; **share**: `share_i = c_i / G_log`. By construction
   `Σ c_i = G_log` (exactly, up to double rounding), so the shares sum to 100 % of the declared gap.
4. The equal split in (2) is a **declared normalisation, not an estimate**. It is disclosed as such, its
   non-identification is stated here, and its consequences are bounded in §5.1 — not repaired after seeing results.

### 5.1 Non-identification of the required split (declared now)

`a*` and `s*` trade off one-for-one against a fixed product, so the **split of the required log product between
rationing and survival is not identified by the panel**. D1 fixes it at ½/½. Two consequences, both computed and
reported and neither verdict-bearing:

- **Flip condition (declared):** under D1 the two state shares differ by `|ln s − ln a| / G_log`. The label leaves
  `JOINT` for `X-CARRIED` only if that difference exceeds **10 pp**, i.e. if `|ln s − ln a| > 0.10 · G_log`.
  This inequality is evaluated and reported; it is a property of the realised factors, not of the split rule.
- **Split sensitivity (declared):** the required log product is also split at weights **0.25 / 0.75** and
  **0.75 / 0.25** between `a*` and `s*`. Shares are reported for all three weights as
  `split_weight_sensitivity`. This is reported to show how much of the label is the rule and how much is the data.

### 5.2 Alternate allocation rules (declared, **non-verdict-bearing**)

- **D2 — absolute-log shares:** `share_i = |ln x_i| / Σ_j |ln x_j|`. Weights each factor by its distance from unity;
  designed to be reported even though it treats the `m > 1` uplift as a positive term.
- **D3 — single-lever (leave-one-out) solve:** for each factor, the value that alone closes the gap,
  `x_i* = 0.8076 / Π_{j≠i} x_j`. Reported with a **reachability** verdict under the declared rules (§5.3). This is
  the decision-relevant object and it needs no allocation rule.
- **D4 — literal-order labels:** the block lists `X-CARRIED` before `JOINT` and states **no precedence**. Every
  label is reported **twice**: under D1 precedence (§6.2) and under literal order.

### 5.3 Reachability of a single lever (declared criteria, computed by the code)

| factor | lever value that closes the gap alone | declared reachability test |
|---|---|---|
| convention `m` | `0.8076/(a·s)` | **`ARITH-ONLY` — `DECLARED-EXCLUDED`**: formable, but choosing `m` to hit a level bar is `FAIL-RE-FIT` (D134) and belongs to EXP-15. Never reported as a repair option. |
| rationing `a` | `0.8076/(m·s)` | `REACHABLE-BY-CAPACITY` iff the implied entry-year coverage `a*/phys_cap` ≤ 1.0 (the gate is `min(phys_cap·seats, overage_cap·cohort)`, so `a = phys_cap · seat_coverage` while that term binds) |
| survival `s` | `0.8076/(m·a)` | `UNREACHABLE-UNDER-DECLARED-LAW` iff `s* > surv_max` (the survival rule is `clip(surv_max·Q^θ)`, `Q = exp(−γ·max(0,q−1)) ≤ 1`, so `surv_max` is a hard ceiling for the channel) |

---

## 6. Verdict function (frozen)

### 6.1 Vocabulary

Exactly three labels, from the block: **`RATIONING-CARRIED`**, **`SURVIVAL-CARRIED`**, **`CONVENTION-CARRIED`**,
plus **`JOINT`** and **`UNDETERMINED`**. No other label may be returned.

### 6.2 Precedence (declared now — the block states none)

The block's two conditions can hold at once (a factor at 50.7 % with the second within 10 pp is both "≥ 50 %" and
"two largest within 10 pp"). The block lists `X-CARRIED` first but does not order the tests. **D1 precedence:
`JOINT` is tested first.** Reasons, recorded before the run: (i) the block's own consequence clause says `JOINT`
means "**no single lever is admissible** and the repair must move both" — a near-tie is exactly that case, and
(ii) under the literal order `JOINT` would be unreachable whenever one factor is just over 50 % and the second is
close, i.e. the `JOINT` clause would be vestigial in precisely the situation it exists to name.
**The literal-order label is nevertheless computed and reported for every cell** (§5.2 D4), so the Council can read
either construction. The label under literal order is never used in prose without the D1 label beside it.

Algorithm, in order:

1. If the frozen identity check fails in any scored cell → **`UNDETERMINED`** (stop; no shares are reported as a verdict).
2. Compute D1 shares. Let `top` = largest share, `second` = second largest, `delta = top − second`.
3. If `delta ≤ 10.0` → **`JOINT`**.
4. Else if `top ≥ 50.0` → **`X-CARRIED`** (X named).
5. Else (`top < 50` and `delta > 10`) → **`JOINT`** with the flag **`NO-MAJORITY`**: the declared vocabulary has no
   third label, and `top < 50` already denies a single-lever reading. The flag is reported; it changes no number.
6. `label_literal_order`: if `top ≥ 50.0` → `X-CARRIED`, else `JOINT`.

### 6.3 What is in scope of the falsifier and what is not (declared now)

- **In scope (can produce `UNDETERMINED`):** `SYN00_PHL_LIKE` / `lower_secondary`, chain years **1973–2025**, at 1e-9.
- **Out of scope, reported:** the other three levels of the same type; all 30 country types (§7 secondary); the
  block's display-constant reproduction (§2).
- **Declared clip boundary:** `completion_uis` is clipped to `[0, 1]` by the generator. In `primary` the product
  `m · completion_cohort` exceeds 1.0 in the late years, so the stored value is clipped and the identity **cannot**
  reproduce it. This is a declared clip, not an accounting failure, and it is outside the verdict scope because the
  verdict is a `lower_secondary` statement and no `lower_secondary` cell clips (max `m · completion_cohort` over
  that series is below 1.0; the value is reported). A clipped cell is never counted as an identity failure, and a
  `lower_secondary` cell that clipped **would** produce `UNDETERMINED`.

---

## 7. Secondary analyses (declared, **non-verdict-bearing** — the block, clause 5)

1. **All 30 country types**, `lower_secondary`, 2021: the same chain reconstruction, the same 1e-9 identity check,
   and the same D1 shares **against the same declared required value 0.8076 used as a common yardstick** (declared
   reading: this is a *common benchmark*, not a requirement derived for those types; those types have no upper-2024
   delivery of their own to derive one from). Types whose 2021 chain value is **at or above** `0.8076` have no
   shortfall and receive **`NO-SHORTFALL`** with blank shares; shares of a negative gap are not reported.
2. **Gap width at 2017, 2022 and 2024** (and every year in the detail file), so the Lead can see whether the
   shortfall is local to 2021. Same declared required value throughout; no year is treated as an estimate of another.
3. These two analyses **cannot** change the verdict, add a label, or qualify the primary shares. They are context.

---

## 8. Closed claims (no rescue, no reopening)

- **Pure arithmetic on frozen output plus one frozen code line.** No re-fit, no new parameter, no re-run, no
  re-scoring of EXP-7 (its `ENDPOINT-ONLY 9/33` verdict stands untouched), no re-tuning of A3-D, no reopening of
  C1–C4, no reopening of class **b2** or of the endpoint object.
- **No causal claim, no direction claim.** The decomposition locates arithmetic in a declared chain. It does **not**
  say that expanding lower-secondary places would raise completion, nor that quality causes dropout, nor anything
  about the observed Philippine cause. D63 remains `UNABLE as to cause`; the phase verdict and the scaling `FAIL`
  are untouched.
- **Not a repair, not a target, not a forecast.** `0.8076` is derived from the model's own delivered upper value; the
  experiment does not endorse it as a policy target and does not predict any future value.
- **Synthetic ≠ observed.** No `SYNTHETIC` number is described as an observed Philippine fact; the single
  `OBSERVED` number (80.896) is used only as a labelled reference and never inside a computation.
- **The required split is declared, not estimated** (§5.1). No reader may be told the ½/½ split is a finding.
- **Determinism.** `code/run_lower_def.py` uses no RNG, no clock, no network, no environment-dependent ordering.
  Two independent executions must produce **byte-identical** CSVs; the second run is stored in
  `results/determinism_run2/` and compared by sha256 in `RUN_MANIFEST.json`.

---

## 9. Files this experiment will write

| file | contents |
|---|---|
| `code/run_lower_def.py` | the frozen arithmetic (read-only on all inputs) |
| `results/LOWER_DEF_RESULTS.csv` | factor rows, shares, verdict, components, thresholds, reachability |
| `results/LOWER_DEF_DETAIL.csv` | year × level chain for the verdict type (`SYN00_PHL_LIKE`), 1970–2025 |
| `results/LOWER_DEF_TYPES.csv` | 30 types, 2021, §7.1 secondary |
| `results/INPUT_HASHES.json` | sha256 of every input read |
| `results/determinism_run2/` | byte-identical second execution |
| `FINDINGS.md`, `RUN_MANIFEST.json`, `SHA256SUMS.txt` | report, manifest, checksums |

**Declared verdict vocabulary is closed. Declared thresholds are frozen. Signed: WORKER LD, before the run.**
