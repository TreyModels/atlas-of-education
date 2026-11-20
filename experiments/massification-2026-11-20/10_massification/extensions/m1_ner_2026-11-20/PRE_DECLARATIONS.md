# PRE-DECLARATIONS — M1-NER (EXP-3): construct equivalence of the cohort-flow NER analogue

**Worker MN, 2026-11-20 (Asia/Shanghai). FROZEN BEFORE ANY STOCK-OR-FLOW COMPUTATION.**
**Scope:** `10_massification/extensions/m1_ner_2026-11-20/` only. No file in `synthetic_2026-11-20/`
(v1.2 or addendum), `hkg_transfer_2026-11-20/`, or anywhere else in the repository is edited, moved,
or rewritten by this experiment.

**LABELS.** The test objects are **SYNTHETIC** model output and **DERIVED** NER columns. The HKG and
PHL observed series are **OBSERVED-REFERENCE-ONLY**. Nothing here is observed, estimated, fitted,
forecast, or evidence about any country. **No causal or direction claim.** This is a
**measurement / construct** test, not a causal test.

**Hash.** The sha256 of this file is recorded in `RUN_MANIFEST.json` as
`predeclaration_sha256` before the first run. This file is not edited after the first run.

---

## 1. Authority and question

Council brief 021 (D112 #3) places **EXP-3 — M1-NER** at rank #3 and makes it condition **H1** of the
SR-9 conditional authority to run the HKG diagnostic transfer. The question, quoting the brief:

> 1. **First-order channel link.** **Schooling + measurement** — does the model's NER object measure what
>    the HKG target measures? One sentence: it decides whether a DIAGNOSTIC-TRANSFER comparison is a
>    comparison or a measure artefact.

This experiment answers only that question. It does not run the HKG transfer, does not compare the
synthetic model to HKG, and does not produce any HKG or portability verdict.

---

## 2. The Council definitions, verbatim

Copied from `08_council/brief_021/SYNTHESIS_021.md` §4, EXP-3 block (lines 343–363), and from the H1
row of §3.3 (line 227). These definitions and thresholds are fixed; nothing in §3–§9 below widens them.

### 2.1 EXP-3 block (verbatim)

> ### EXP-3 — M1-NER: construct equivalence of the cohort-flow NER analogue (rank **#3**)
>
> 1. **First-order channel link.** **Schooling + measurement** — does the model's NER object measure what
>    the HKG target measures? One sentence: it decides whether a DIAGNOSTIC-TRANSFER comparison is a
>    comparison or a measure artefact.
> 2. **What changes if positive vs negative.** *Admissible* → SR-1 clears at the construct level; the HKG run may use the
>    object with a declared caveat. *Not admissible* → the run must use a stock object or return
>    `BLOCKED-MEASURE(SR-1)`; the analogue is labelled a cohort-flow analogue only.
> 3. **Why it is not a niche.** It is the hinge of the SR-9 authority question, D75(iii)'s "never spliced", and PA-4. Without
>    it, a TRANSFER-HOLDS/FAILS would be uninterpretable (measure vs timing).
> 4. **Data on disk.** v1.2.1 NER panel (`admitted_official`, `cohort`, `ner*` columns — draft, on disk);
>    `data/gmr_observed_6countries_1970_2024.csv` HKG NER/ANER 1971–1996 as a **construct reference only**;
>    `UNIVERSALIZATION_SERIES.csv` PHL `ner_primary` (30 observed) as a second reference. No DATA ASK.
> 5. **Numeric threshold + falsifier.** Stock analogue = **mean of `admitted_official / cohort` over the last `dur`
>    years** (declared, parameter-free). **Admissible** iff |stock − flow| **≤ 2.0 pp** in **every** year where the flow
>    analogue ∈ [85, 95] **and** the implied first-sustained crossing years differ by **≤ 1 y**. **Falsifier:** > 2.0 pp
>    at any such year, or a ≥ 2 y crossing difference. **Declared expected sign:** during expansion the flow analogue
>    leads the stock (flow ≥ stock), so the bias, if present, makes crossings **earlier** — the direction that could flatter
>    a 1974/1979 target.
> 6. **Closed-claim check.** No C1–C4; measurement only; does not re-score v1.2 checks; no direction claim; the observed
>    HKG series is a construct reference, **not** a validation of the synthetic model.
> 7. **Cost / rank.** **Small. Rank #3.**

### 2.2 H1 condition (verbatim, §3.3)

> **H1 — measure admissibility (clears SR-1 at the construct level)** | The NER **construct-equivalence test** (EXP-3) must return **ADMISSIBLE**: the stock reconstruction and the cohort-flow analogue differ by **≤ 2.0 pp** in every year where the analogue is in the 85–95 band, **and** the implied first-sustained crossing years differ by **≤ 1 y**. Crossing definition fixed as **first sustained 5-year crossing** before the comparison. | EXP-3 result file; if FAIL → `BLOCKED-MEASURE(SR-1)`, authorisation void

---

## 3. Operands and the stock-analogue formula (declared before the run)

### 3.1 Input panel

`10_massification/extensions/synthetic_2026-11-20/generator_v1_2_addendum/results/synthetic_panel_v1_2_ner.csv`
— the delivered v1.2.1 NER panel. Label `SYNTHETIC` on every row. 6 720 data rows (30 countries × 4
levels × 56 years, 1970–2025). One row per country-level-year. The panel is read **read-only**.

### 3.2 Flow analogue

For row (country `c`, level `L`, year `t`):

```
flow(c,L,t) = 100 * admitted_official(c,L,t) / cohort(c,L,t) = the panel's `ner` column
```

on the row's own level; for primary rows this is identically `ner_primary`. This is the v1.2.1
addendum's cohort-flow analogue (addendum `PRE_DECLARATIONS.md` §2), **not** the UIS stock NER. The
code re-derives `flow` from `admitted_official` and `cohort` and checks it against the panel's `ner`
column at display precision; it does not re-estimate anything.

### 3.3 Stock analogue

For country `c`, level `L`, year `t`, with the level duration `dur_L`:

```
stock(c,L,t) = 100 * (1/dur_L) * SUM_{k=0}^{dur_L-1} [ admitted_official(c,L,t-k) / cohort(c,L,t-k) ]
```

i.e. **the mean of the per-year `admitted_official / cohort` ratios over the last `dur_L` years,
including year `t`** (the brief's wording, read literally as a mean of ratios, not a ratio of sums).
The analogue is declared and parameter-free: it uses only the frozen panel and the factory's declared
durations. It is the accounting reconstruction of a stock-style NER: the official-age admission flows
still enrolled in the level at `t`, divided by the official-age band.

### 3.4 Durations (`dur`)

Taken from the frozen factory's declared level durations
(`generator_v1_2/code/sim_v1_2.py:65`, `DVEC`; `generator_v1_2/PARAMS.md` §3):

| level | `dur` (years) |
|---|---|
| primary | 6 |
| lower_secondary | 3 |
| upper_secondary | 3 |
| tertiary | 4 |

For **primary**, `dur = 6`, so `stock` exists only from **1975** onward (a complete 6-year window
1970–1975 is needed). A stock value is computed only where the full window is present; there is no
truncated or partial-window value and no imputation.

### 3.5 Difference

```
diff(c,L,t) = stock(c,L,t) - flow(c,L,t)   [percentage points, pp]
```

The reported bar is `|diff| ≤ 2.0 pp`. "During expansion the flow leads the stock (flow ≥ stock)"
therefore corresponds to `diff ≤ 0`.

---

## 4. Declared comparison windows (exact)

### 4.1 Verdict-bearing series and years

**Country `SYN00_PHL_LIKE`, level `primary`, years 1970–2025.** This is the PHL-calibrated anchor's
primary-NER series — the same series named by the addendum's §6 smoke test — and primary NER is the
level of the D75 HKG target. It is declared here, before any stock or difference is computed, as the
single series on which H1 is decided.

- **Band years (the comparison set):** every year `t` with **1975 ≤ t ≤ 2025** (so that the 6-year
  stock window is complete) and **85.0 ≤ flow(t) ≤ 95.0** (inclusive at both ends).
- Years 1970–1974 are outside the stock window even if their flow lies in the band; they are reported
  in the comparison file with `stock_window_complete = FALSE` and are **not** counted in the band test.
- There is **no** other filter, no winsorising, no smoothing of `flow`, and no exclusion of
  non-monotone years.

### 4.2 Panel-wide sensitivity window (descriptive only, not verdict-bearing)

To guard against a verdict that hides panel-wide behaviour, the same band rule is also applied to
**all 30 synthetic countries × all 4 levels**, each year with a complete `dur` window and
`85.0 ≤ flow ≤ 95.0`. This sensitivity panel is reported and labelled **DESCRIPTIVE-SENSITIVITY**.
It cannot change the §4.1 verdict; it can only be reported as a scope caveat in `FINDINGS.md`.

---

## 5. Decision rule (fixed)

H1 has two conditions; **both** must hold for the overall verdict `ADMISSIBLE`.

### 5.1 Condition B — band agreement

- Evaluate every band year in §4.1.
- **PASS** iff `|diff| ≤ 2.0 pp` in **every** band year.
- **FAIL** (falsifier) iff `|diff| > 2.0 pp` at **any** band year.
- Numeric handling: the bar is inclusive; a violation is `abs(diff) > 2.0 + 1e-9`. The `1e-9` is a
  floating-point equality tolerance, **not** a widened tolerance.
- If the band set is empty, Condition B is `UNDETERMINED` and the overall verdict is **not**
  `ADMISSIBLE`.

### 5.2 Condition C — crossing-year agreement

- Thresholds: **90** and **95** (percent). Both are evaluated.
- Compute the first-sustained crossing year (§6) for `flow` and for `stock` on the §4.1 series.
- For each threshold: if both crossings exist, `delta = |stock_year - flow_year|`; **PASS** iff
  `delta ≤ 1 y`; **FAIL** iff `delta ≥ 2 y`.
- If exactly one analogue has no crossing by 2025, Condition C is **FAIL** for that threshold (an
  undefined difference cannot satisfy a ≤ 1 y bar).
- If **both** analogues have no crossing by 2025, the threshold counts as **PASS** for Condition C
  (neither crosses) and this is recorded explicitly; Condition B still governs.
- Condition C passes overall iff both 90 and 95 pass.

### 5.3 Overall

```
ADMISSIBLE      iff Condition B PASS and Condition C PASS (both thresholds)
NOT ADMISSIBLE  otherwise
UNDETERMINED    only if the band set is empty (recorded as not admissible)
```

A single `NOT ADMISSIBLE` is sufficient for `BLOCKED-MEASURE(SR-1)` under H1. No post-hoc narrowing of
the window, no switching to a different country/level, and no tolerance change is permitted after the
run.

---

## 6. First-sustained crossing rule

Mirroring the addendum §6 rule and the on-disk sustained-crossing rule
(`10_massification/relations/data/UNIVERSALIZATION_TIMING.csv`: "observed first-sustained crossing
(≥ 5 consecutive years above)"):

- A **first-sustained crossing** at threshold `T` is the first year `y` such that **every** year
  `y, y+1, ..., y+4` has value `≥ T` (five consecutive years **at or above** the threshold).
- Synthetic series are contiguous annual series, so no missing-year rule is needed there. The `flow`
  series is evaluated on 1970–2025; the `stock` series on 1975–2025 (primary).
- If no such `y` exists by 2025, report `none_by_2025`.
- `first-at-or-above` (first single year `≥ T`) is also reported, because it is needed to explain a
  noisy series; it is **not** the crossing used in the verdict.

---

## 7. Declared expected sign (descriptive)

During expansion, the brief declares **flow ≥ stock** (the flow leads; the expected `diff ≤ 0`), so a
bias would make crossings **earlier** — the direction that could flatter a 1974/1979 target.

- "Expansion" is defined mechanically as `flow(t) > flow(t-1)` using the same series (for `t = 1975`,
  `flow(1974)` is available).
- Report, among band years: the count and share with `flow ≥ stock` (`diff ≤ 0`), the count with
  `flow < stock`, and the mean `diff` in expansion band years.
- This is **reported descriptively**. A counter-sign year is recorded and discussed, but is **not**
  itself one of the two numeric falsifiers in §5; the verdict is set only by Conditions B and C.

---

## 8. Reference-only observed series (not validation)

Read-only, no interpolation:

1. **HKG** from `data/gmr_observed_6countries_1970_2024.csv`: `ner_primary` and `aner_primary`,
   restricted to the declared window **1971–1996** (24 observations each; there is a 1986–1994 gap in
   the observed record, and observations outside 1971–1996 are excluded from the reference block by
   this predeclaration).
2. **PHL** from `10_massification/data/UNIVERSALIZATION_SERIES.csv`: `ner_primary`, all 30 observed
   years (1976–2017; the series is sparse and non-contiguous).

Rules for reference crossings:

- Observed years are **not** interpolated and no values are imputed.
- A first-sustained crossing requires five **consecutive calendar years, each observed**, all `≥ T`;
  crossings are therefore computed **within contiguous observed blocks** and the earliest such year
  across blocks is reported, with the block and the number of observations.
- `first-at-or-above` is the first observed year `≥ T`.
- These series are **construct references only**. They are **not** compared with the synthetic stock
  or flow series, not used to set any threshold, not used to choose the synthetic country, and not a
  validation of the model. Their output is labelled `OBSERVED-REFERENCE-ONLY`.

---

## 9. Outputs (all inside this directory)

| file | content |
|---|---|
| `results/M1_NER_RESULTS.csv` | test, statistic, threshold, verdict, n, label (band test, crossing tests at 90/95, overall H1, expected sign, sensitivity summary) |
| `results/M1_NER_COMPARISON.csv` | year-by-year `flow`, `stock`, `diff`, `|diff|`, bar-met flag, for every band year (verdict series and sensitivity panel separately labelled) |
| `results/M1_NER_CROSSINGS.csv` | first-sustained crossing years (90/95) for `flow` and `stock`, by series, with difference and ≤ 1 y flag |
| `results/M1_NER_REFERENCE.csv` | observed HKG/PHL reference series and their crossings, labelled `OBSERVED-REFERENCE-ONLY` |

All numeric report fields use `%.6f`; years are integers; `none_by_2025` is a string, never a number.
No result file contains a timestamp, hostname, path, process id, or float-repr instability.

---

## 10. Determinism and hashing

- The analysis code is deterministic: no RNG, no seed, no wall clock, no network, no environment
  dependence, no locale dependence. It reads only the files named above.
- It is run **twice**; the four result CSVs from the two runs must be **byte-identical** (`sha256`
  equality). Run 1 writes `results/`; run 2 writes `_determinism/run2/`. Both are retained.
- `RUN_MANIFEST.json` records the sha256 of this predeclaration, the code, every input (v1.2.1 panel,
  its addendum manifest and predeclaration; frozen v1.2 panel, code and PARAMS; the observed
  reference CSVs; brief 021), every result file, and the determinism evidence.

---

## 11. What this experiment does not do

- It does **not** run the HKG transfer, compare the synthetic model to HKG, or produce a
  `TRANSFER-HOLDS` / `TRANSFER-FAILS` / `FAIL-RE-FIT` verdict.
- It does **not** make an HKG, portability, capacity-timing, or phase-verdict claim.
- It does **not** re-score, re-fit, re-tune, or edit any v1.2 or addendum check, parameter, result, or
  file.
- It does **not** treat the observed HKG or PHL series as validation; they are construct references.
- It does **not** claim that a cohort-flow object *is* the UIS stock NER. The addendum's §2.1
  limitation stands: the object is a cohort-flow analogue. This experiment tests whether the stock
  reconstruction and that analogue are close enough, in the declared band and at the declared
  crossings, for the HKG diagnostic comparison to be a measure comparison rather than a measure
  artefact.
- The result is a statement about the **synthetic model-interface object** under frozen bars. It is
  not evidence about any education system.
