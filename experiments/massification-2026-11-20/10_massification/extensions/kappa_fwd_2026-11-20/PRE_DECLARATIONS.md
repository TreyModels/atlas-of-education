# PRE-DECLARATIONS — EXP-11 KAPPA-FWD

**`LABEL: OBSERVED` for the observed completion series; `DERIVED` for every ratio, slope, median, bound, error and
verdict computed from it.** No synthetic object enters this experiment.
Experiment: **EXP-11 KAPPA-FWD** from Council brief 023 (D136 #1), `08_council/brief_023/SYNTHESIS_023.md` §6.1, rank
**#1**. Worker **KF** · created 2026-11-21 (Asia/Shanghai) · **written before any script was executed on the data**.

This file is frozen on creation: its sha256 is written to `PRE_DECLARATIONS.sha256` **before**
`code/run_kappa_fwd.py` executes, and the script **refuses to run** unless the on-disk file's sha256 equals the constant
embedded in the script. **No threshold, bar, pairing rule, half-sample split rule, hold-out construction, verdict string
or consequence mapping in this file may be changed after results are seen.** If any declared step cannot be implemented
exactly as written, it is **reported as not implemented**, not silently approximated.

**This is a measurement audit of an observed series. It makes no causal claim and no direction claim.** κ is
**not asserted to cause anything**; it is tested only as a *forward-usable declared input*. **No C1–C4 reopening.**
**No re-scoring of EXP-6** (different estimand, §9). **D63 remains `UNABLE as to cause`** either way.

---

## 0. Scope and question

**Question (first-order).** Is the per-system lower→upper one-stage transition ratio κ — the coefficient the next model
line (V16-REPAIR) is about to carry as a **declared input** — constant enough to be applied **forward** in a system, or
only describable **within** the window it was computed on?

**Operational form — two legs, both purely within-system.**

- **Leg (a) STATIONARITY (κ-STABLE).** Does the ratio series drift over its own observed window? Two bars, both on the
  ratio itself: an **OLS trend** in `upper_year` and a **half-sample level shift**.
- **Leg (b) TEMPORAL HOLD-OUT.** Fit κ on the **pre-2021** pairs only, then ask whether the **post-2020** cells respect
  the resulting **upper bound** `upper_t ≤ κ_pre · lower_{t−3}`.

Nothing is estimated across countries. Nothing is extrapolated beyond the observed window. The verdict is a statement
about **usability as a declared input**, not about mechanism.

**Data used (on disk only, read-only).**

| file | role |
|---|---|
| `10_massification/data/UNIVERSALIZATION_SERIES.csv` | observed `completion_upper_secondary` / `completion_lower_secondary`, `status=observed`, for PHL/KOR/KHM/CHN — the **re-derived** source of every pair |
| `10_massification/extensions/pipe_loo_2026-11-20/results/PIPE_LOO_PAIRS.csv` | EXP-6's 43 frozen pairs — **cross-check only** (ratio, `lower_year_used`, `year_offset_used`, `loo_kappa` must be reproduced, not consumed) |
| `08_council/brief_023/SYNTHESIS_023.md` | verbatim source of §6.1 and the byte-comparison check in §1 |
| `08_council/DECISIONS.md` | D133's per-system κ register: provenance of the κ values compared in §3 |

**No web. No external data. No DATA ASK. No writes outside this directory. No model code executed.**

**Declared non-entrants (recorded, never imputed).** **HKG and JPN cannot enter** — the frozen file carries no
`completion_lower_secondary` or `completion_upper_secondary` rows for either ISO3 (V14, D135). They are reported
`NON-ENTRANT` with `n_pairs = 0`. No proxy numerator, no GER substitution (D118), no interpolation, no imputation.

---

## 1. Frozen source, verbatim

### 1.1 `SYNTHESIS_023.md` §6.1 — **EXP-11 block**, byte-exact (source lines 403–434)

Reproduced below inside a four-backtick fence with **no prefix, no re-wrapping, no re-punctuation**. The fence body is
byte-identical to `08_council/brief_023/SYNTHESIS_023.md` lines 403–434; `code/run_kappa_fwd.py` **re-extracts those
lines from the source file and byte-compares them to this fence body** on every run. A mismatch is a **BLOCK** —
reported as a predeclaration defect, never repaired silently.

````
### 6.1 EXP-11 — **KAPPA-FWD**: is the per-system transition ratio a *forward-usable* declared input? (rank **#1**)

1. **First-order link (schooling + cohort flows).** Whether the one-stage transition ratio — the object the batch
   renamed "the ceiling" and the coefficient the next model line is about to carry as a **declared input** — is
   constant enough to be applied **forward** in a system, or only describable **within** the window it was computed on.
2. **What changes if positive vs negative.** **Positive** (`κ-STABLE` and the bound holds out of sample) → κ enters the
   model as a **declared constant per system**, the pipeline link is a forward constraint, and the ceiling question
   stays "what sets κ?". **Negative** (a trend in PHL/KOR/KHM, or bound violations in the 7 hold-out cells) → κ enters
   only as a **within-window description**; the link must be declared a **trajectory input** (a declared path, never
   extrapolated) or dropped as a forward constraint, and every downstream statement about 2025+ inherits that limit.
   Either way the answer is **actionable in the predeclaration before V16-REPAIR is frozen**.
3. **Why it is not a niche.** κ is about to become a parameter. A parameter whose stationarity is untested is the
   "fitted curve treated as a law" failure the step-back rule names — and the batch already contains the failure mode:
   **CHN's ratio runs 0.6448 → 0.9662 while its lower series is flat**. A reader of the first-order question is entitled
   to know whether "the ceiling is a pipeline ratio" means a **system property** or a **window**.
4. **Data on disk (no DATA ASK).** `pipe_loo_2026-11-20/results/PIPE_LOO_PAIRS.csv` — columns `iso3`, `upper_year`,
   `lower_year_used`, `year_offset_used`, `ratio`, `loo_kappa`; **43 pairs** (PHL 8, KOR 19, KHM 11, CHN 5); declared
   pre-2021 medians **PHL 0.9596 / KOR 0.9887 / KHM 0.5950 / CHN 0.7222**; **post-2020 hold-out cells: PHL 2, KOR 3,
   KHM 2, CHN 0 (7 total)**. Declared limitation: **HKG and JPN cannot enter** (zero completion pairs, V14).
5. **Threshold + falsifier (fixed before the run).** *Leg (a) stationarity:* per system, `κ-STABLE` iff
   **|OLS slope of `ratio` on `upper_year`| ≤ 0.005 per year** **and** the **first-half vs second-half LOO median
   differ by ≤ 2.0 pp**; else `κ-TRENDING`. *Leg (b) temporal hold-out:* for each system with a pre-2021 κ, predict the
   post-2020 cells as `upper_t ≤ κ_pre · lower_{t−3}`; `BOUND-HOLDS` iff **≥ 6 of the 7** hold-out cells are within the
   bound; `BOUND-BREAKS` iff **≥ 2** violations. **Verdict: `FORWARD-USABLE` iff (a) all three of PHL/KOR/KHM are
   `κ-STABLE` and (b) `BOUND-HOLDS`; `WINDOW-ONLY` otherwise.** **Falsifier:** a PHL slope > 0.005/yr or ≥ 2 hold-out
   violations → `WINDOW-ONLY`, and **no downstream predeclaration may treat κ as a forward constraint**.
   Report all 43 ratios and all 7 hold-out cells; no threshold may move after results.
6. **Closed-claim check.** Does **not** re-score EXP-6 (different estimand: out-of-sample *in time* and a trend slope,
   not LOO in-sample); EXP-6's `PREDICTIVE (3/4)` stands regardless of this outcome. No re-fit (κ values are observed
   medians), no C1–C4 reopening, no direction claim. A `WINDOW-ONLY` verdict is not a falsification of the pipeline
   reclassification — it bounds its **use**.
7. **Cost / rank.** **Small** (one deterministic script, read-only, no RNG). **Rank #1.**
````

### 1.2 `DECISIONS.md` D136 — the EXP-11 clause, byte-exact

The single sentence in D136 that adopts this experiment (extracted from the D136 row, `κ-STABLE` through
`→ WINDOW-ONLY`), quoted with no edit:

````
**EXP-11 KAPPA-FWD** — is the per-system transition ratio forward-usable? (κ-STABLE iff |slope of ratio on upper_year| ≤ 0.005/yr and first/second-half LOO medians differ ≤ 2.0 pp; temporal hold-out on the 7 post-2020 cells with the pre-2021 κ; FORWARD-USABLE iff PHL/KOR/KHM all stable and ≥6/7 within bound; falsifier PHL slope > 0.005 or ≥2 violations → WINDOW-ONLY)
````

### 1.3 `DECISIONS.md` D133 — the per-system κ register and the CHN exclusion, byte-exact

Quoted with no edit (the clause that makes κ **per-system, never global**, and that makes **CHN unusable forward**):

````
CORRECT: the pipeline object's coefficient is **PER-SYSTEM, never global** — κ = PHL **0.9491**, KOR **0.9898**, KHM **0.5950**, CHN **0.7222** (spread 0.395; a single κ=0.949 overstates KHM by 0.354); pre-2021 values 0.9596/0.9887/0.5950/0.7222 (PHL moves 0.0105 when 2023–24 added); **CHN's κ is a within-sample median of a non-stationary series and may not be used as a forward constraint**.
````

**Reading of the brief that binds this run.** Leg (a) is a **stationarity** test of κ, so **both** its bars are on the
ratio's level: the slope bar and the half-sample **median-ratio** shift (§4). Leg (b) is a **one-sided upper bound**
(`≤`), never a two-sided accuracy band (§5). The brief's own §6.1 item 4 supplies the 43 pairs and the 7 hold-out cells;
this run **re-derives** both from the observed series and reports the reconciliation (§2.4), it does not consume them.

---

## 2. Data and pairing rule (as EXP-6 §2, re-declared exactly and re-derived)

For each ISO3 with upper/lower series `upper[t]`, `lower[y]` (`status=observed` only; **no interpolation, no imputation**):

1. For every observed **upper** year `t`, set `target = t − 3` (declared one-stage transition lag, **3 years**).
2. If `lower[target]` exists → **exact pair** at `t − 3`, flag `EXACT`, `year_offset_used = 0`.
3. Else candidates = observed **lower** years within **±1 y** of `target`. If none → the upper year is **dropped** and
   logged `DROPPED_NO_LOWER_WITHIN_1Y`.
4. Else use the nearest candidate; **ties break toward the earlier year**:
   `min(cands, key=(|y − target|, y))` (EXP-1's convention). Flag `NEAREST_1Y`, `year_offset_used = lower_year − target`.
5. `ratio = upper[t] / lower[lower_year_used]`.

Both inputs are completion percentages (`unit = percent`), so **ratios are dimensionless** and every error/slack below
is in **percentage points (pp)**. Pairing is applied **per country and independently**; no pair crosses a country
boundary. **Every** upper year is either paired or logged as dropped.

### 2.1 Declared expected structure (pre-freeze reference, **not** a result)

43 pairs — PHL 8, KOR 19, KHM 11, CHN 5; 16 upper years dropped; 11 observed upper years across the four systems are
never upper years in a pair. This structure is **recomputed** and, on any disagreement, the disagreement is **reported
and blocks the verdict** (`UNDETERMINED`, §7.3) rather than being reconciled by hand.

### 2.2 No pair is ever removed, added, re-weighted or re-flagged after an error is seen

All 43 pairs and all 7 hold-out cells are reported in `results/KAPPA_FWD_DETAIL.csv`. No subset is ever substituted for
the full set.

### 2.3 LOO construction (recomputed, used only for the declared secondary checks)

For country `c` with `n_c` pairs and pair `i`: `κ̂_(c,−i) = median` of the ratios of the **other** `n_c − 1` pairs of
`c` (sample median; even counts → mean of the two central order statistics). Never fitted, never cross-country, never
shrunk. Used **only** to (i) reproduce EXP-6's `loo_kappa` column as a cross-check and (ii) report the declared
secondary half-sample statistics of §4.3. **No verdict depends on it.**

### 2.4 Cross-check against EXP-6 (reported, never used to choose a value)

For each of the 43 pairs, this run's `ratio`, `lower_year_used` and `year_offset_used` are compared to
`PIPE_LOO_PAIRS.csv`. The file carries 4-decimal rounding, so the tolerance is **`|Δratio| ≤ 5e-5`** and years must match
**exactly**. Any pair failing this is reported in `results/KAPPA_FWD_SECONDARY.csv` as a `CROSSCHECK` row; the
**recomputed** value stands. This is a reproducibility check on the input pairs, **not** a re-scoring of EXP-6.

---

## 3. The per-system κ series and its provenance

**κ_c (full window)** = median of system `c`'s **43-pair subset** ratios. **κ_pre,c (training value)** = median of
system `c`'s ratios for pairs with **`upper_year ≤ 2020`**.

Declared reference values, taken from **D133's register** and from **§6.1 item 4** — recorded here as **text, before the
run**, so that agreement is a *check* and never a target:

| system | D133 full-window κ | §6.1 pre-2021 κ | n pairs (declared) | post-2020 cells (declared) |
|---|---|---|---|---|
| PHL | **0.9491** | **0.9596** | 8 | 2 |
| KOR | **0.9898** | **0.9887** | 19 | 3 |
| KHM | **0.5950** | **0.5950** | 11 | 2 |
| CHN | **0.7222** | **0.7222** | 5 | 0 |

**Reconciliation rule (fixed now).** The run recomputes all eight medians and compares them at 4 dp. **The recomputed
value stands**; agreement is reported as `MATCH` / `DIFFERS` with both numbers. A difference is **reported**, never used
to re-cut a bar, a pair or a system set. D133's own note is carried: a **single** κ overstates KHM by **0.354**
(median difference) — therefore **no pooled or global κ is computed, reported or used anywhere in this experiment.**

**Provenance labels.** κ values are **OBSERVED medians of observed ratios** — **DERIVED, never fitted**. No parameter is
estimated by any optimisation; there is **no re-fit** anywhere in this file.

---

## 4. Leg (a) — STATIONARITY: definitions, split rule, bars

### 4.1 Slope bar (per system)

`slope_c` = **OLS slope of `ratio` on `upper_year`** over system `c`'s pairs, computed exactly as

`slope = Σ(x−x̄)(y−ȳ) / Σ(x−x̄)²`, with `x = upper_year` (integer years), `y = ratio`, **no weighting, no robust
estimator, no transformation, no outlier removal** (KHM's 2000 collapse pair stays in; removing it after seeing its
residual would be a re-fit).

**Bar:** `|slope_c| ≤ 0.005 per year` → slope leg satisfied. Inclusive at 0.005. Units: **ratio units per year**
(0.005/yr = 0.5 pp of the ratio per year).

### 4.2 Half-sample split (per system)

1. Sort the system's pairs by `upper_year` **ascending** (ties cannot occur — one pair per upper year).
2. `h = n // 2`. **First half** = the first `h` pairs; **second half** = the last `h` pairs.
3. If `n` is **odd**, the single **middle pair belongs to neither half** (`half_member = MIDDLE_EXCLUDED`) — the split
   is symmetric by construction and no pair changes sides. Declared consequence: KOR `h = 9` (2014 middle), KHM `h = 5`
   (2013 middle), CHN `h = 2` (2016 middle); PHL `h = 4`, no middle.
4. A system with `n < 4` would have `h < 2` and an undefined half test → `UNDETERMINED` for that system (§7.3). Does not
   arise at the declared counts but is declared, not silently handled.

### 4.3 Half-sample statistic (the brief's "first-half vs second-half LOO median")

**Primary statistic — `half_median_shift_pp`.** For each half, `κ̂_half = median` of **that half's own ratios** (the same
median-ratio estimator as κ, applied to the half), and

`half_median_shift_pp = |κ̂_half2 − κ̂_half1| × 100` — i.e. the level shift of the ratio expressed in **percentage points**
(0.02 in ratio units = 2.0 pp), the unit D133 uses for κ moves ("PHL moves 0.0105 when 2023–24 added").

**Bar:** `half_median_shift_pp ≤ 2.0` → half-sample leg satisfied. Inclusive at 2.0.

**Why this statistic is primary, declared before the run.** The brief's phrase names the **LOO median** — the
median-of-ratios estimator of §2.3 — and asks whether *the estimate itself* moves between halves. The natural
half-sample reading is therefore the median of the half's ratios. The two obvious alternatives are **computed and
reported as declared, non-verdict-bearing** (`results/KAPPA_FWD_SECONDARY.csv`), because **neither may be promoted or
demoted after results**:

- **S-A1 — median of the half's per-pair LOO κ̂ values.** Declared **degenerate by construction**: `κ̂_(c,−i)` is the
  median of the *other* `n−1` pairs, so for every pair it sits within one order statistic of the full-sample κ and the
  statistic is nearly constant across halves by construction. Reported so the reader can see the degeneracy rather than
  take it on trust.
- **S-A2 — median of the half's `|LOO error|`** (EXP-6's accuracy object). This measures **prediction accuracy drift over
  time**, not κ's level drift, and is therefore **not** the leg (a) object; it is reported because it is the reading a
  careless reader will assume.

**If the three statistics disagree in label for a system, the disagreement is reported in `FINDINGS.md` and the
primary label stands.** The primary is named here, before the run, precisely so it cannot be chosen afterwards.

### 4.4 Per-system label

`κ-STABLE` **iff** `|slope_c| ≤ 0.005/yr` **and** `half_median_shift_pp ≤ 2.0`; otherwise **`κ-TRENDING`**.
Both bars are conjunctive: a system clearing one and failing the other is `κ-TRENDING`.
No third label exists (`κ-UNCERTAIN`, `κ-MIXED`, `κ-BORDERLINE` do not exist and may not be introduced).

---

## 5. Leg (b) — TEMPORAL HOLD-OUT: definitions

### 5.1 Cells

**Training set** for system `c` = its pairs with **`upper_year ≤ 2020`**; `κ_pre,c` = median of their ratios.
**Hold-out cells** = its pairs with **`upper_year ≥ 2021`** (the brief's "post-2020 cells"). A system with **no**
pre-2021 pair cannot be trained → leg (b) is `N/A` for it (§7.3). Declared counts: **PHL 2, KOR 3, KHM 2, CHN 0 → 7**.

### 5.2 Bound and violation

For a hold-out cell with observed upper value `upper_t`:

`bound_t = κ_pre,c × lower_used`, where `lower_used` is **that cell's own observed lower value at the year the pairing
rule actually used** (§2).
`excess_t = upper_t − bound_t` (pp, **signed**; positive = the observed upper exceeds the pre-2021 bound).

**Violation:** `excess_t > 1e-9 pp` (a strict reading of the brief's `upper_t ≤ κ_pre · lower_{t−3}`; `1e-9` is a
floating-point guard only, not a substantive tolerance). `slack_t = −excess_t`.

### 5.3 The literal `lower_{t−3}`

`lower_{t−3}` is used directly wherever it is **observed**. Where it is **not observed**, the pairing rule's `±1 y`
observation is the denominator, and the literal `t−3` bound is **declared `UNAVAILABLE` (no observed lower at t−3)** and
**is not imputed** — imputing it would fabricate the very object under test. `results/KAPPA_FWD_SECONDARY.csv` reports,
per cell, whether the literal `t−3` value exists and what the literal bound would have been; the primary uses the
pairing-rule value for **all** cells, so no cell is scored on two different denominators.

### 5.4 Aggregate label

Let `V` = number of violating cells among the **7** hold-out cells (PHL + KOR + KHM; CHN contributes none, §6).

- **`BOUND-HOLDS`** iff `V ≤ 1` (i.e. **≥ 6 of 7** within bound).
- **`BOUND-BREAKS`** iff **`V ≥ 2`**.

Exhaustive over `V ∈ {0,…,7}`: `V = 0` → 7/7 within → HOLDS; `V = 1` → 6/7 → HOLDS; `V ≥ 2` → BREAKS. There is no
third label. The **per-system** within-counts are also reported (`bounds_hold x/y`), but they are **descriptive** and do
**not** carry a per-system verdict string of their own.

### 5.5 Declared sensitivity (non-verdict-bearing, fixed now)

**S-B1 — `±5.0 pp` slack band.** `within_slack` iff `excess_t ≤ 5.0 pp` (EXP-6's own ±5 pp convention, imported only as
a *description*, never as this experiment's bar). Reported per cell and in aggregate. **Does not enter the verdict.**
Declared before the run: if S-B1 and the primary disagree in aggregate, both are reported, the primary stands, and the
disagreement is named in `FINDINGS.md` — a 0.6 pp breach and a 6 pp breach are different objects and neither may be
re-labelled as the other.

**S-B2 — literal-`t−3` availability**, per §5.3. Descriptive.

**S-B3 — per-cell `ratio_t` vs `κ_pre,c`** (dimensionless), so the reader can see the direction of each miss without any
direction *claim* being made about causes.

---

## 6. CHN — reported, **not** a forward constraint (D133)

**CHN's κ is a within-sample median of a non-stationary series and may not be used as a forward constraint** (D133,
verbatim in §1.3). Therefore:

- CHN **is** computed and **fully reported**: its 5 pairs, ratio series, slope, half-sample medians, and full-window κ.
- CHN **is excluded from** (i) the `FORWARD-USABLE` conjunction, (ii) the 7-cell hold-out denominator, (iii) the
  falsifier's violation count. CHN has **0** post-2020 cells, so its leg (b) is `N/A — no post-2020 cell` (not a pass,
  not a failure).
- CHN's inclusion would **not** be conservative: it cannot make the verdict better or worse, and it may not be cited as
  either support or refutation of the verdict.

This is a **pre-existing Council disposition applied**, not a choice made by this run.

---

## 7. Verdict rule, vocabulary, and the falsifier

### 7.1 The conjunction (fixed now)

**`FORWARD-USABLE`** iff **both**:

- **(a)** **PHL, KOR and KHM are each `κ-STABLE`** (all three, per §4.4), **and**
- **(b)** the aggregate hold-out label is **`BOUND-HOLDS`** (per §5.4).

**`WINDOW-ONLY`** otherwise — including every case where any of PHL/KOR/KHM is `κ-TRENDING` regardless of leg (b), and
every case of `BOUND-BREAKS` regardless of leg (a).

**`UNDETERMINED`** only on a **mechanical block** (§7.3). It is **not** a soft verdict available when the result is
surprising, mixed, or inconvenient.

**No other verdict string exists.** There is no `PARTIAL`, no `MIXED`, no `INCONCLUSIVE`, no `FORWARD-USABLE (with
caveats)`. `WINDOW-ONLY` is not softened to "suggestive" and `FORWARD-USABLE` is not upgraded to "confirmed".

### 7.2 Falsifier (as written in the brief, and its enforcement)

The falsifier **trips** iff **`PHL slope > +0.005/yr`** (signed, as the brief writes it) **or `V ≥ 2` hold-out
violations**. On a trip the verdict **must** be `WINDOW-ONLY`, and **no downstream predeclaration may treat κ as a
forward constraint**. The script **enforces** `falsifier_tripped → verdict == WINDOW-ONLY` as an assertion and reports
`falsifier_tripped: TRUE/FALSE` plus **which arm** fired.

Declared note: the falsifier is a **sub-case** of the verdict rule, not an additional bar — a trip can only ever
*confirm* `WINDOW-ONLY`, never create `FORWARD-USABLE`. A **negative** PHL slope is *not* the falsifier's PHL arm; the
PHL arm uses the same `|slope| ≤ 0.005` bar as §4.1 for the label but a **signed** `> +0.005` test for the falsifier,
and both are reported separately so the two readings can never be confused.

### 7.3 What `UNDETERMINED` covers (exhaustive, and nothing else)

`UNDETERMINED` is returned iff **any** of: the predeclaration sha256 does not match the embedded constant; an input
file's sha256 does not match its recorded value; the recomputed pair structure (§2.1) differs from the declared
structure; a required system has `n < 4` pairs (half-split or slope undefined); a hold-out cell's pairing-rule lower
observation is missing. In every such case the run **stops and reports**, and it does **not** re-cut a rule to obtain a
number.

### 7.4 Consequence mapping (declared **before** results — this is what the verdict licenses)

- **`FORWARD-USABLE`** → κ may enter V16-REPAIR as a **declared per-system constant**, **never fitted**, and **only**
  for the systems that passed, **only** within the observed window's horizon, and **only** with D134's object-unit
  obligation honoured in completion units with survival explicit (`adm_upper ≤ κ·comp_lower(t−3)/surv_upper`, or the
  declared endpoint form). CHN stays excluded. The ceiling question becomes **"what sets κ?"**.
- **`WINDOW-ONLY`** → κ may **not** be a forward constraint. In V16-REPAIR it may appear **only** as (i) a **declared
  within-window trajectory input** — a declared path over the observed years, **never extrapolated** — or (ii) not at
  all. Every V16 statement about **2025+** inherits that limit and must be labelled as a **scenario/trajectory**
  statement, not a constraint; the model must **not** carry a single κ, a global κ, or an extrapolated κ path.
- **`UNDETERMINED`** → **nothing is licensed**: no κ is declared anywhere, and the V16 predeclaration must treat the
  parameter as **HELD/untested**, not as passed.

**Neither branch licenses a causal claim.** "Forward-usable" is a statement about a **predictive input**, not about a
mechanism, a policy lever, or the direction of any effect.

---

## 8. No-threshold-change rule; no re-fit; one estimand

**Everything in §2–§7 is frozen on creation of this file.** After results are seen, **no** bar, split rule, statistic
choice, sensitivity label, pairing rule, tie-break, system set, unit convention, verdict string or consequence mapping
may change, and **no pair may be dropped, added, re-weighted or re-flagged**. If the result surprises the worker, the
result stands and the surprise is written in `FINDINGS.md` as an observation **about the result** — never as a licence
to re-cut it.

**No re-fit, no re-parameterisation, no second estimand.** One pass of one deterministic script produces every number.
κ values are observed medians; they are **not** fitted, not shrunk, not weighted, not cross-validated beyond the declared
split. No data-driven choice is made anywhere: `3 y`, `±1 y`, `≤ 0.005/yr`, `≤ 2.0 pp`, `≥ 6/7`, `≥ 2 violations`,
`upper_year ≤ 2020` and `≥ 2021` are all fixed in this file **before** the run.

**The sensitivity legs (§4.3, §5.5) may not be promoted**, and the primary legs may not be demoted, on the basis of
their results. They exist to be **reported**, not to be chosen between.

---

## 9. Closed-claim check

- **Does not re-score EXP-6.** Different estimand: EXP-6 tested **out-of-sample prediction within the window** (LOO
  in-sample prediction, median |error| ≤ 3.0 pp); this run tests **drift in time** (a slope, a half-sample level shift,
  and an **out-of-time one-sided bound**). **EXP-6's `PREDICTIVE (3/4)` stands regardless of this outcome** — a
  `WINDOW-ONLY` here does **not** retract it, and a `FORWARD-USABLE` here does **not** strengthen it.
- **Does not reopen C1–C4**, does not re-run EXP-1/2/3/7/8/9, no WT/DT cell, no generator execution, no A3-S re-check.
- **Does not choose any V16-REPAIR parameter value.** It fixes only κ's **admissibility class** (constant vs
  trajectory vs held), which is exactly the input the V16 predeclaration needs before it is frozen.
- **No direction claim, no causal claim.** κ is not asserted to cause, produce, constrain or explain anything. A
  `κ-TRENDING` label says the ratio *moved*, **not** that anything moved it. A `BOUND-BREAKS` label says observed upper
  completion exceeded a pre-2021 ratio-implied bound, **not** that any policy, cohort or capacity change caused it.
- **D63 stays exactly where it stands**: `UNABLE as to cause`. Neither verdict moves it.
- **No measure substitution.** Completion only; GER/NER are **not** admissible numerators (D118). No proxy, no
  interpolation, no imputation, no synthetic object.
- **`WINDOW-ONLY` is not a falsification of the pipeline reclassification** — following §6.1 item 6 verbatim: it
  **bounds its use**.

---

## 10. What this experiment does NOT claim

- Not a claim that κ is "real", structural, causal, or a system invariant. `κ-STABLE` means *the observed ratio did not
  drift measurably within a short window with few pairs* — nothing more.
- Not a claim about **saturation physics**. KOR sits at 0.99 with a lower series at 100.00 in two years; a ratio pinned
  at the ceiling is **near-arithmetic by construction** and is reported as such (D132's condition), never as evidence of
  a mechanism.
- Not a **forecast**. No extrapolation past the last observed year is computed, plotted or implied. The hold-out cells
  are **observed** years, never future ones.
- Not a claim about **HKG, JPN** or any non-entrant (D114/D135), and not a claim that the four systems are
  representative.
- Not a claim about **lower-secondary measurement quality** or about the **2026 vintage** of either series.

---

## 11. Determinism and reproducibility contract

- **No RNG. No network. No clock-dependent output in any result file.** No timestamps, no absolute paths, no
  environment-dependent ordering in the CSVs. Every float is formatted to a **fixed number of decimals**; every row set
  is emitted in an **explicit sorted order** (`iso3`, then `upper_year`).
- **Two runs must be byte-identical.** `results/` and `results/determinism_run2/` are produced by two independent
  invocations of the same script and compared byte-for-byte; the comparison result is recorded in `RUN_MANIFEST.json`.
- The script **verifies** the predeclaration sha256 and each input sha256 **before** computing anything, and aborts on
  mismatch.

---

## 12. Files this run will produce

| file | content |
|---|---|
| `PRE_DECLARATIONS.md` | this file (frozen) |
| `PRE_DECLARATIONS.sha256` | its sha256, written before the run |
| `code/run_kappa_fwd.py` | deterministic implementation of §2–§7 |
| `code/make_manifest.py` | manifest + checksum generation |
| `results/KAPPA_FWD_RESULTS.csv` | **per system**: n, slope, half medians/shift, legs, hold-out counts/errors, verdict |
| `results/KAPPA_FWD_DETAIL.csv` | **all 43 pairs** and **all 7 hold-out cells** |
| `results/KAPPA_FWD_SECONDARY.csv` | declared sensitivities S-A1/S-A2/S-B1/S-B2/S-B3, cross-check (§2.4), non-entrants |
| `results/console.txt` | full console transcript of run 1 |
| `results/determinism_run2/` | byte-identical re-run |
| `FINDINGS.md` | plain-English report and what it licenses for V16-REPAIR |
| `RUN_MANIFEST.json`, `SHA256SUMS.txt` | provenance and checksums |

**Write scope: this directory only.** No existing repository file is modified by this experiment.
