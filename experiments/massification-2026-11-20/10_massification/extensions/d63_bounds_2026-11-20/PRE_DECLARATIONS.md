# PRE-DECLARATIONS — EXP-23 **D63-BOUNDS**

**`LABEL: OBSERVED`** for the UIS completion values read from disk; **`DERIVED`** for every logarithm, share,
required value, interval and verdict computed from them; **`DECLARED-THRESHOLD`** for the 90 pp comparison level;
**`DESCRIPTIVE / WINDOW-ONLY`** for the single κ citation; **`SYNTHETIC`** for the single generator number cited as
context and **not used**. No model is run and no model value enters any bound.

Experiment: **EXP-23 D63-BOUNDS** from Council brief 025 (D156 **#3**, rank **#3**), `SYNTHESIS_025.md` §6.3.
Worker **D63** · created 2026-11-21 (Asia/Shanghai) · **written before any run of `code/run_d63_bounds.py`**.

This file is frozen on creation. Its sha256 is written to `PRE_DECLARATIONS.sha256` **before** the runner executes, and
the runner refuses to run unless the on-disk file's sha256 equals the constant embedded in it **and** unless the five
quoted regions below still match the Council's own bytes. **No threshold, comparison, outcome rule, verdict string,
pairing rule, declared identity or share denominator in this file may be changed after results are seen.** If a
declared step cannot be implemented exactly as written it is **reported as not implemented**, never silently
approximated.

**D63 stays `UNABLE as to cause` whatever this cell returns.** The cell is descriptive: it makes **no causal claim**
and **no direction claim**, licenses **no** model change (the generator line is closed, D150/D154), **runs no model**,
**re-fits nothing**, **adopts no value**, and **does not re-score** CEIL-ATTRIB, PIPE-LOO, LOWER-DEF or any of the 33
cells. It consumes the 8 declared pairs as a **range**, exactly as the block says, and does not re-test them.

---

## 0. Scope and question

**Question (the block's, operationalised).** Can the upper-secondary residual be **bounded descriptively** — how much of
it is the pipeline level, how much is the transition ratio, and is the 90 pp level reachable **inside the observed
record's own ratio range**? Stated as the block's one-line discriminative question: *can the upper-secondary residual
be bounded and split, and is 90 inside the observed ratio range?*

**What this cell may and may not produce.** It produces a **split** of the log gap into two additive accounting
components and **three bound comparisons** against the observed record. It does **not** produce a cause, a direction, a
counterfactual "what would have happened", a forecast, a policy target, or a re-attribution of D63. The 90 pp level is a
**`DECLARED-THRESHOLD`** (the D34/A6 crossing bar, 90/90/90 pp), **not** an observed object and **not** a policy target
for this cell.

**Objects and their declared labels.**

| object | where on disk | label |
|---|---|---|
| upper-secondary completion, 2024, PHL | `UNIVERSALIZATION_SERIES.csv`, `value` where `iso3=PHL`, `indicator=completion_upper_secondary`, `year=2024` | `OBSERVED` |
| lower-secondary completion, 2021, PHL | same file, `indicator=completion_lower_secondary`, `year=2021` | `OBSERVED` |
| lower-secondary completion, 2024, PHL (record maximum) | same file, same indicator, `year=2024` | `OBSERVED` |
| the 8 declared PHL pairs and their ratios | `pipe_loo_2026-11-20/results/PIPE_LOO_PAIRS.csv` (`ratio`), **recomputed** here from the series | `OBSERVED` values / `DERIVED` ratios |
| log gap, log components, shares, required lower, required ratio, implied interval | this cell | `DERIVED` |
| 90 pp comparison level | D34/A6 (90/90/90 crossings) | `DECLARED-THRESHOLD` |
| κ = 0.949135 (PHL) | `KAPPA_FWD_RESULTS.csv`, `kappa_full` | `DESCRIPTIVE / WINDOW-ONLY` — cited, **not used** |
| generator v1.3 upper 2024 = 76.6391 | `generator_v1_3/results/synthetic_panel_v1_3.csv`, `completion_uis`, `country_id=0`, `level=upper_secondary`, `year=2024` | `SYNTHETIC` — cited as context, **not used** |

**Object identity before comparison (D158 rule 2).** The two completion series compared here are **both** read from
the same file, under the same `measure` (UIS completion rate), the same `unit` (`percent`), the same `source` and
`vintage` (`UIS_SDG4_2026_11`), and the same `status` (`observed`); they differ in **level** and **year**, which is
exactly the declared comparison (`upper_t` vs `lower_{t−3}`). Identity is therefore established at the metric level and
the level/year difference is carried explicitly in every comparison row's `convention` field. **No GER value, no NER
value and no model value enters any comparison.** The EXP-21 CONV-REG register (`conv_reg_2026-11-20/results/CONV_REG.csv`)
is **cited for object naming only**; its completion-vs-GER interchangeability labels are **not** used here, because this
cell never compares completion to GER.

---

## 1. Frozen extract from `SYNTHESIS_025.md` §6.3 — **verbatim**

<!-- VERBATIM-BEGIN:SYNTHESIS_025-6.3 -->
> ### 6.3 EXP-23 — **D63-BOUNDS**: a bounded, descriptive decomposition of the upper-secondary residual (rank **#3**)
>
> 1. **First-order link (the asymmetry the phase verdict rests on).** The phase's headline asymmetry is that PHL's upper
>    secondary **never crosses 90** while primary and lower do. CEIL-ATTRIB established the residual is
>    **pipeline-consistent** and left D63 `UNABLE as to cause`. What has never been asked is whether the residual can be
>    **bounded descriptively** — how much of it is the pipeline level, how much is the transition ratio, and whether 90 is
>    even reachable inside the observed record's own ratio range.
> 2. **What changes if positive vs negative.** **`RESIDUAL-SPLIT`** (both channels in [1/3, 2/3] of the log gap) → the
>    write-up says *"the residual is split; neither channel alone closes it"* and reports both required values.
>    **`PIPELINE-DOMINANT`** → the write-up says the residual is a lower-level story, with the number. **`RATIO-DOMINANT`**
>    → the write-up says it is a transition story. In every case D63 stays `UNABLE as to cause`; what changes is that the
>    **"structural ceiling"** sentence becomes unavailable.
> 3. **Why it is not a niche.** The unreproduced upper-secondary asymmetry is one of the two objects in the phase
>    write-up. A sentence calling it structural is currently unsupported: the 90 threshold sits **inside** the observed
>    ratio range at the record's 2024 lower completion (V36), so whether upper completion crosses is a statement about the
>    path taken, not a demonstrated barrier.
> 4. **Data on disk (no DATA ASK).** `UNIVERSALIZATION_SERIES.csv` — `completion_upper_secondary` (**75.02525329589844**
>    at 2024; 11 observed years) and `completion_lower_secondary` (**80.89604949951172** at 2021; 92.4139633178711 at
>    2024); `ceil_attrib_2026-11-20/FINDINGS.md` §3 — the **8** declared pairs and their ratios (`upper_t/lower_{t−3}`,
>    ±1 y nearest, range **0.889–1.072**; the 2023 pair at 0.889 is the only out-of-band one); the κ register (PHL
>    **0.949135**) for a declared descriptive comparison only.
> 5. **Threshold + falsifier (fixed before freeze).** At the 2024 upper cell with lower at `t−3 = 2021`:
>    **`ln(90 / upper_2024) = ln(90 / lower_2021) + ln(lower_2021 / upper_2024)`** — report both shares as
>    `pipeline_share` and `ratio_share`. Inversions: report the lower completion required to reach 90 **at the 2024
>    ratio**, and the ratio required **at the 2024 lower completion**; report the upper-completion interval implied by the
>    **observed 8-ratio range** at the record's highest lower completion. **Verdict:** `RESIDUAL-SPLIT` if both shares lie
>    in [1/3, 2/3]; `PIPELINE-DOMINANT` if `pipeline_share > 2/3`; `RATIO-DOMINANT` if `ratio_share > 2/3`. **`THIN` rule:**
>    if the ratio range rests on **< 3** pairs the dominant labels are unavailable and only `RESIDUAL-SPLIT` may be
>    reported. **Falsifier:** if the 2024/2021 pair is absent or one of the two values is not `status = observed` →
>    `UNDETERMINED`. **No model value enters**; κ, if cited, is labelled `DESCRIPTIVE / WINDOW-ONLY` and is not used to
>    compute the bound.
> 6. **Closed-claim check.** Does **not** re-run CEIL-ATTRIB; does **not** re-freeze its `[0.90, 1.10]` band test (the 8
>    ratios are consumed as a **range**, not re-tested); does **not** re-score its `PIPELINE-CONSISTENT` verdict; D63 stays
>    `UNABLE as to cause`; **no cause and no direction claim**; the cell licenses **no** model change (the line is closed).
> 7. **Cost / rank.** **Small.** **Rank #3** — it is independent of #1 (it compares completion to completion only), it
>    bounds the asymmetry the write-up must report, and it removes an unsupported sentence.
<!-- VERBATIM-END:SYNTHESIS_025-6.3 -->

**Frozen status.** The block above is spliced mechanically from `08_council/brief_025/SYNTHESIS_025.md` (the heading
and items 1–7 of §6.3, line range fixed at authoring time). The runner re-extracts the same range from the frozen source
and **blocks** if the bytes differ. The block's item 5 fixes the identity, the two inversions and the split verdict; item
6 fixes what the cell may not do; item 4 fixes the data and the 8-pair range.

---

## 2. Frozen anchors from `08_council/DECISIONS.md` — **verbatim**

### 2.1 D153(xiii) — the split, the two inversions, and the barred sentence

<!-- VERBATIM-BEGIN:DECISIONS-D153-xiii -->
> (xiii) **D63's residual is split, not structural** — upper 2024 75.02525329589844 vs 90 = 14.974747 pp; ln(90/75.025) = ln(90/80.896) + ln(80.896/75.025) → **58.6008% pipeline level / 41.3992% transition ratio**; at the 2024 ratio the lower series would have to reach 97.042584 pp (+4.628621 above the record maximum 92.4139633178711), while at the record's 2024 lower completion the required ratio 0.973879 is **inside** the observed 8-pair range 0.889–1.072; D63 stays UNABLE, "the upper-secondary ceiling is structural" **barred**;
<!-- VERBATIM-END:DECISIONS-D153-xiii -->

### 2.2 D156 — the EXP-23 adoption (verdict vocabulary and precedence)

<!-- VERBATIM-BEGIN:DECISIONS-D156-EXP23 -->
> **EXP-23 D63-BOUNDS** — the D63 residual split as a descriptive bound (recompute 58.6008%/41.3992%; the required lower 97.042584 vs record max 92.4139633; the required ratio 0.973879 vs observed 8-pair range 0.889–1.072; verdicts `BOUNDS-INSIDE > BOUNDS-EDGE > BOUNDS-OUTSIDE`; D63 stays UNABLE) **#3**
<!-- VERBATIM-END:DECISIONS-D156-EXP23 -->

### 2.3 D158 — the seven authoring rules (all binding here)

<!-- VERBATIM-BEGIN:DECISIONS-D158 -->
> (1) **Hash enforcement at verdict time** — a hash cited in a verdict row must be enforced by the runner when the verdict is written; a recorded-but-unenforced hash may be cited only as **`RECORDED-NOT-ENFORCED`** and may carry no verdict (EXP-16's RESULTS.csv hash). (2) **Object identity before comparison** — no two series may be compared/subtracted/placed unless both carry the same declared denominator/convention; otherwise the result is **`NOT-COMPARABLE`**, not a number; a comparison table not stating the convention is returned (EXP-18 C-2 / D153(xi)). (3) **Register before sentence** — no write-up sentence may use a number whose register line (convention, window, label, source) does not exist; a sentence without a register line is `UNVERIFIED` and may not ship. (4) **Level-symmetric legs** — a leg intended to test a two-level object must require **both** levels; a leg satisfiable by one level must say so in its own sentence and may not be cited as evidence about the object it was meant to protect. (5) **Class tags** — every model number carries its class (v1.6 or v1.7 or v1.5) and every localisation sentence names the class (D153(x)). (6) **Banned sentences register** — the barred phrasings ("demand falsified", "the participation margin is duplicated" as a cell sentence, "the upper-secondary ceiling is structural", "survival loses 50.7%", "fix survival only", "A17 0/33 vs A00 9/33" without its sentence, "behaviourally N pp wrong" before EXP-21) are enumerated and a predeclaration using one is returned. (7) **Label discipline for REQUIRED-STATE/DERIVED** — any λ*, required coverage or derived target carries "REQUIRED-STATE (EXP-17); not adopted" / "DERIVED" in the same sentence as the number.
<!-- VERBATIM-END:DECISIONS-D158 -->

---

## 3. The decomposition identity (declared exactly)

Let `u24 = upper_2024`, `l21 = lower_2021`, `l24 = lower_2024`, and `T = 90` (`DECLARED-THRESHOLD`). All values are
`OBSERVED` percentages read from the named cells; every derived quantity is a natural logarithm of a **ratio of
percentages**, so the percentages' units cancel and the logs are dimensionless.

```
(1)  G  = ln(T / u24)          the log gap between 90 and observed upper 2024
(2)  P  = ln(T / l21)          the PIPELINE-LEVEL component   (lower completion three years earlier)
(3)  Q  = ln(l21 / u24)        the TRANSITION-RATIO component (upper_2024 / lower_2021)
(4)  G  = P + Q                the identity, exact up to floating point
(5)  pipeline_share = P / G ;  ratio_share = Q / G ;  pipeline_share + ratio_share = 1
```

The pair is the block's declared one-stage pair: **upper 2024 with lower at `t−3 = 2021`** (D153(xiii)'s own pair, the
8-pair set's `EXACT` 2024 pair). The identity is an **accounting identity**, not an estimate: it has **zero free
parameters** and therefore **zero residual by construction**. **Declared identity tolerance: `|(P + Q) − G| ≤ 1e-12`;
the residual is reported, and a larger residual is a `BLOCK`, not a result.** The shares are **not** estimated weights,
do **not** carry a causal reading, and are **not** a claim that either channel "explains" the gap in any sense beyond
this product decomposition; the block's own words are "pipeline level" and "transition ratio".

### 3.1 Split verdict — mapping and precedence

Tested in this declared order; the first label whose condition holds is the verdict:

1. **`UNDETERMINED`** if the 2024 upper cell or the 2021 lower cell is absent, duplicated, or carries `status ≠
   observed` (the block's own falsifier). Terminal.
2. **`PIPELINE-DOMINANT`** if `pipeline_share > 2/3`, else **`RATIO-DOMINANT`** if `ratio_share > 2/3`.
3. **`RESIDUAL-SPLIT`** if **both** shares lie in the closed interval `[1/3, 2/3]`.

**`THIN` rule (the block's).** If the ratio range rests on **fewer than 3** pairs, the two dominant labels are
**unavailable** and only `RESIDUAL-SPLIT` may be reported; if in that case both shares do not lie in `[1/3, 2/3]` the
split is `UNDETERMINED`. The 8 pairs give `n_pairs = 8 ≥ 3`, so this rule does not bind — but it is declared and is
checked in code, and the realised `n_pairs` is reported.

**Note on precedence (D158 rule 6, D147(i)).** Steps 2 and 3 are **mutually exclusive** (`pipeline_share > 2/3` and
`ratio_share > 2/3` cannot both hold, and either excludes both shares lying in `[1/3, 2/3]`), so the declared order is
**not verdict-bearing** here. It is stated anyway, in the block, as the rules require. The falsifier (step 1) is
tested **first** and is terminal.

---

## 4. The three bound comparisons and the bounds verdict

Three comparisons, each a statement about **the observed record's envelope**, never about the world. `T = 90` in all
three. The record is the PHL observed completion series (11 upper years, 11 lower years) and the 8 declared pairs.

| id | required / implied quantity | compared against | `INSIDE` iff |
|---|---|---|---|
| **B1** | `required_lower = T / (u24 / l21)` — the lower completion that would be needed **at the 2024 ratio** | `record_max_lower = max` observed lower completion (`l24`) | `required_lower ≤ record_max_lower` |
| **B2** | `required_ratio = T / l24` — the ratio that would be needed **at the record's 2024 lower completion** | `[ratio_min, ratio_max]` over the 8 declared pairs | `ratio_min ≤ required_ratio ≤ ratio_max` |
| **B3** | `implied_upper ∈ [l24 · ratio_min, l24 · ratio_max]` — the upper-completion interval implied by the observed 8-ratio range at the **record's highest** lower completion | `T` | `implied_lo ≤ T ≤ implied_hi` |

**No tolerance, no epsilon, no band, no rounding step exists in any of the three tests**: each comparison is evaluated
in full double precision on the values read from disk, and equality counts as `INSIDE` (all three operators are
inclusive). There is therefore nothing to tune and no margin to choose.

**Bounds verdict — mapping and precedence.** Tested in this declared order; the first label whose condition holds is
the verdict:

1. **`BOUNDS-INSIDE`** iff all three comparisons are `INSIDE`.
2. **`BOUNDS-EDGE`** iff the outcomes are **mixed** — at least one `INSIDE` and at least one `OUTSIDE`.
3. **`BOUNDS-OUTSIDE`** iff all three comparisons are `OUTSIDE`.

**Disclosure of operationalisation (required by D158 rule 6 and by honesty).** D156 names the three labels
(`BOUNDS-INSIDE > BOUNDS-EDGE > BOUNDS-OUTSIDE`) but does **not** define them; §6.3 states the two inversions and asks
for the implied interval without naming which mismatch is which label. This section **is** the definition, fixed before
the run: it partitions all 8 outcome combinations exhaustively and without a free parameter (3 `INSIDE` → INSIDE; 0
`INSIDE` → OUTSIDE; 1–2 `INSIDE` → EDGE). `BOUNDS-EDGE` consequently means **"the record contains part of the required
condition and not all of it — at least one channel lies outside the observed envelope and at least one lies inside"**.
It is **not** a proximity-to-threshold label, it does **not** mean "close", and no reader may read a margin into it.

**Overall cell status.** The split verdict (§3.1) and the bounds verdict (§4) are reported **separately and both**, as
D156 requires both ("recompute 58.6008 %/41.3992 %" … "verdicts `BOUNDS-INSIDE > BOUNDS-EDGE > BOUNDS-OUTSIDE`"). The
**D63 status is fixed at `UNABLE as to cause`** by the block, by D153(vi) and by D153(xiii): **no outcome of either
verdict changes it.** If any input guard or the falsifier fires, both verdicts are `UNDETERMINED` / `BLOCKED` and the
D63 status is still `UNABLE as to cause`.

---

## 5. Declared computations, in execution order

1. **Load** `10_massification/data/UNIVERSALIZATION_SERIES.csv` read-only; take the PHL `completion_upper_secondary`
   and `completion_lower_secondary` rows with `status = observed`; record both year→value maps.
2. **Falsifier check** (§3.1 step 1): 2024 upper and 2021 lower present exactly once each with `status = observed`.
3. **Identity** (1)–(5) in double precision; report `G`, `P`, `Q`, both shares, and the identity residual.
4. **Rebuild the 8 pairs** with the declared EXP-1/PIPE-LOO pairing rule — `t−3` exact, else the nearest lower
   observation within **±1 y**, ties toward the **earlier** year, else drop — over the PHL observed series, and require
   `n_pairs = 8`. **Cross-check** the realised pair set (upper year, lower year) against
   `PIPE_LOO_PAIRS.csv`'s PHL rows and require the ratios to agree at 4 dp. A pair-set mismatch is a `BLOCK`: the
   observed ratio range would then not be the block's range. The range is **consumed**, not re-tested: no `[0.90, 1.10]`
   in-band test is recomputed and no CEIL-ATTRIB verdict is touched.
5. **Three bound comparisons** B1–B3 (§4) on the full-precision values; report each required value, each envelope, each
   outcome, and the signed excess (`required − envelope`) so the direction of every miss is explicit.
6. **Verdicts** per §3.1 and §4.
7. **Reproduction check of the Council's stated numbers** (§6).
8. **Declared non-verdict-bearing sensitivity** (§7).
9. **Write** the two result files, the console log, and nothing else.

---

## 6. Reproduction check of the stated numbers (D113a), fixed before the run

The block and D153(xiii) state the following values; this cell recomputes each from disk and reports
`recomputed`, `stated`, `difference` and `reproduced = yes/no`. **Rounding rule (declared): a value stated to `d`
decimal places is reproduced iff `|recomputed − stated| ≤ 0.5 × 10^(−d)`.** A failure is a **`BLOCK` reported, not
adjusted**: an unreproducible block number is a blocking error (D159/D113a), never a number to be replaced by this
cell's own.

| # | stated (source) | recomputed here from |
|---|---|---|
| R1 | upper 2024 `75.02525329589844` (§6.3 item 4) | series cell |
| R2 | lower 2021 `80.89604949951172` (§6.3 item 4) | series cell |
| R3 | `14.974747` pp = 90 − upper 2024 (D153(xiii)) | DERIVED |
| R4 | `58.6008` % pipeline share (D153(xiii)) | DERIVED |
| R5 | `41.3992` % ratio share (D153(xiii)) | DERIVED |
| R6 | required lower `97.042584` pp (D153(xiii)) | DERIVED |
| R7 | `+4.628621` pp above the record max (D153(xiii)) | DERIVED |
| R8 | record max `92.4139633178711` (§6.3 item 4; D153(xiii)) | series cell |
| R9 | required ratio `0.973879` (D153(xiii)) | DERIVED |
| R10 | 8-pair range `0.889`–`1.072` (§6.3 item 4; D153(xiii)) | DERIVED, to 3 dp |

---

## 7. Declared non-verdict-bearing sensitivity (reported, never a verdict)

The block fixes the **`t−3`** pair. Because a reader could otherwise take the 58.6/41.4 split as a property of the
residual rather than of the declared lag, this cell reports **one** declared sensitivity: the same identity computed
with the **contemporaneous** lower value (`l24`) in place of `l21`, i.e. `P_t = ln(T/l24)`, `Q_t = ln(l24/u24)`, and the
shares `P_t/G`, `Q_t/G`.

**Label: `DERIVED`, `DESCRIPTIVE / NOT-VERDICT-BEARING`.** It enters **no** verdict, changes **no** bound, and is
reported in `results/D63_BOUNDS_RESULTS.csv` with `used_in_verdict = FALSE`. It exists so that the write-up cannot read
the declared split as lag-free. No other sensitivity, alternative lag, alternative threshold or alternative pairing rule
is computed: **no re-fit, no grid, no second estimand.**

---

## 8. Provenance schema (register before sentence, D158 rule 3)

Two files, one row per number. **Every number that appears in `FINDINGS.md` must appear in
`results/D63_BOUNDS_DETAIL.csv`; every number in `results/D63_BOUNDS_RESULTS.csv` must also appear in the DETAIL.** A
number in the prose that is not in the DETAIL is `UNVERIFIED` and may not ship.

**`results/D63_BOUNDS_RESULTS.csv`** — `row_type` (`SPLIT_COMPONENT` / `BOUND_COMPARISON` / `VERDICT` /
`SENSITIVITY_NVB`), `item_id`, `item`, `value_num`, `value_display`, `units`, `label`, `comparison`, `outcome`,
`used_in_verdict`, `note`.

**`results/D63_BOUNDS_DETAIL.csv`** — `number_id`, `row_type` (`OBSERVED_VALUE` / `DERIVED_VALUE` / `PAIR` /
`CITATION_ONLY`), `item`, `value`, `value_display`, `units`, `label`, `source_path` (relative to the programme root),
`source_column`, `source_filter`, `derivation`, `used_in_verdict`, `convention`, `note`.

Every `source_path` is a path relative to the programme root; every `source_column` names the column (or the
`indicator`/`year` filter that selects the cell) on that path; every `derivation` states the arithmetic. `CITATION_ONLY`
rows (κ, the v1.3 generator value) carry `used_in_verdict = FALSE` and are the only rows allowed to have no arithmetic
role.

---

## 9. The seven authoring rules — and where each is implemented

| rule (D158) | implementation in this cell |
|---|---|
| (1) **Hash enforcement at verdict time** | `code/run_d63_bounds.py` embeds `PREDECL_SHA256`, recomputes the file's sha256 at start-up and **aborts before any computation** on mismatch; the same is done for every input file it opens. The manifest records `enforced_at_verdict_time: true`. No hash in any verdict row is `RECORDED-NOT-ENFORCED`. |
| (2) **Object identity before comparison** | §0 identity line; a `convention` field on every comparison row; no GER/NER/model value is compared with a completion value anywhere in the cell. |
| (3) **Register before sentence** | §8 schema; `FINDINGS.md` numbers are checked against the DETAIL by a runner-emitted count (`n_numbers_in_findings` / `n_matched`), and no number is written into the prose that is not in the DETAIL. |
| (4) **Level-symmetric legs** | Not applicable in the *both-levels* sense — this cell is **upper-level by construction** and says so: its verdict is a statement about the **upper** residual only, it may **not** be cited as evidence about the lower level or about a two-level object, and the split's pipeline channel is a **lower-level quantity used as one input**, not a test of the lower level. Declared here so the leg cannot travel. |
| (5) **Class tags** | Every model number carries its class; the only model number cited is `v1.3` (`SYNTHETIC`, `completion_uis`), marked `CITATION_ONLY / not used`. No v1.5/v1.6/v1.7 value is cited at all. No localisation sentence is written. |
| (6) **Banned-sentences register** | §10 below, verbatim from the brief plus this cell's own bars; the runner asserts each banned string is **absent** from the files it writes. |
| (7) **REQUIRED-STATE / DERIVED label discipline** | No λ*, no required coverage, no `REQUIRED-STATE (EXP-17)` object appears in this cell at all. The two "required" values here are **`DERIVED` arithmetic inversions of the identity**, not required-state objects: they are `required_lower` and `required_ratio` and they are labelled `DERIVED` in every row and every sentence. Declared explicitly so that "required" cannot be read as a policy target. |

---

## 10. Banned sentences register

### 10.1 From the brief (§8), verbatim

<!-- VERBATIM-BEGIN:SYNTHESIS_025-8-banned -->
> - **Banned sentences (the list #5 carries into the write-up).** "The model reproduces the PHL level path"; "conditional
>   **level** reproduction" **without** the 9/33 placement and the closed line; "the participation margin is duplicated"
>   **without** the per-level split; "the repair made the model worse"; "the upper-secondary ceiling is structural"; "the
>   proxy is consistent with the required coverage"; "κ ≈ 0.95 is forward-usable"; "the representation capability holds at
>   both levels"; "the model is behaviourally 13–17 pp wrong"; "demand falsified"; "v1.2 passes".
<!-- VERBATIM-END:SYNTHESIS_025-8-banned -->

### 10.2 Cell-specific bars (this cell may not write these, in any tense or hedge)

- **"the upper-secondary ceiling is structural"** — barred by D153(xiii) and by §8; this cell's whole point is that the
  record does not establish it. Nor may the cell write the **opposite** claim as a finding: **"the ceiling is not
  structural"**, **"the ceiling is reachable"**, **"90 was attainable"**, **"the pipeline caused the miss"**,
  **"the transition ratio explains the ceiling"** are all barred, because the cell establishes neither direction.
- **"the residual is 58.6 % pipeline"** as a lag-free statement — the declared split is the `t−3` split, and §7's
  sensitivity must travel with it wherever the split is cited.
- Any sentence using **"because"**, **"caused"**, **"driven by"**, **"due to"**, **"led to"**, **"would have"**,
  **"if the ratio had"**, **"therefore upper would"** about the residual, the pipeline or the ratio.
- **"D63 is resolved"**, **"D63 is explained"** — D63 stays `UNABLE as to cause`.
- Any sentence citing **κ** as a bound input, or citing the **generator value 76.6391** as an input to any comparison.

### 10.3 Mandatory sentences (must appear, in these words)

- **"D63 stays `UNABLE as to cause`."**
- **"The observed ratio range is consumed as a range; it is not re-tested."**
- **"The split is an accounting identity with zero free parameters and zero residual by construction."**
- **"No model was run and no model value enters any bound."**

---

## 11. Discipline declared

No model run. No re-fit. No adoption. No web. No RNG (the runner imports no random module and any clock value is
absent from every result file). No writes outside `10_massification/extensions/d63_bounds_2026-11-20/`. No causal claim,
no direction claim, no forecast, no policy target. The running server is not touched. Two runs, `results/` and
`results/determinism_run2/`, must be **byte-identical**; the comparison is enforced by `code/make_manifest.py` and
recorded in `RUN_MANIFEST.json`.

---

## 12. Falsifiers, blocks and terminal states (all declared before the run)

| condition | terminal state |
|---|---|
| `PRE_DECLARATIONS.md` sha256 ≠ embedded constant | `BLOCKED-PREDECL-HASH` — no results |
| any quoted region (§1, §2, §10.1) ≠ the frozen source's bytes | `BLOCKED-VERBATIM` — no results |
| any input file's sha256 ≠ its declared value | `BLOCKED-FROZEN-INPUT` — no results |
| the 2024 upper or 2021 lower cell absent / duplicated / `status ≠ observed` | split `UNDETERMINED`, bounds `UNDETERMINED` (the block's falsifier) |
| `n_pairs ≠ 8`, or the pair set ≠ `PIPE_LOO_PAIRS.csv`'s PHL pairs | `BLOCKED-PAIR-SET` — the observed range is not the block's range |
| identity residual `|(P+Q) − G| > 1e-12` | `BLOCKED-IDENTITY` |
| any R1–R10 reproduction check fails | `BLOCKED-REPRODUCTION` — reported, not adjusted |

In every terminal state the D63 status remains **`UNABLE as to cause`**, and the cell reports the block rather than a
substitute number.

---

## 13. Authorship disclosure

This predeclaration was written **after** reading the block and D153(xiii), because D113a requires the anchoring numbers
to be re-derived from disk before freeze. It is written **before** `code/run_d63_bounds.py` first executed. **No
threshold, comparison operator, outcome rule, verdict string, pair set, declared identity or share denominator in this
file is a function of any number that is not already frozen in §6.3 or in D153(xiii)** — the two rules that this cell
adds (the §4 bounds mapping and the §7 sensitivity) are functions of **outcome combinations** and of **declared
formulas**, respectively, not of realised values. The author has seen the block's stated numbers; that is exactly why
§6's reproduction check is a separate, non-verdict-bearing test with a declared rounding rule rather than a threshold.
