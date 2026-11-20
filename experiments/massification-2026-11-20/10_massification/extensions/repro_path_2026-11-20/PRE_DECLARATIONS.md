# PRE-DECLARATIONS — EXP-7 REPRO-PATH

**`LABEL: SYNTHETIC` for the generator side; `OBSERVED` for the PHL UIS completion series side.**
Experiment: **EXP-7 REPRO-PATH** from Council brief 022 (D122 #2), `SYNTHESIS_022.md` §6 EXP-7, rank **#2**.
Worker **RP** · created 2026-11-20 (Asia/Shanghai) · **written before any run**.

This file is frozen on creation: its sha256 is written to `PRE_DECLARATIONS.sha256` before
`code/run_repro_path.py` executes, and the script refuses to run unless the on-disk file's sha256 equals
the constant embedded in it. **No threshold, bar, year set, cell rule, κ value, outcome-class definition or
verdict rule in this file may be changed after results are seen.** If any declared step cannot be implemented
exactly as written, it is **reported as not implemented**, not silently approximated.

**This is a descriptive/diagnostic audit. It makes no causal claim and no direction claim.** D63 remains
`UNABLE as to cause`. The v1.2 verdict `PASS-CONDITIONAL` is **audited**, not re-scored; the `m = 1.10` convention
and v1.2's scope (crossing/endpoint placement) are **unchanged** by this experiment. No re-fit, no tuning, no
re-run of the generator, no RNG.

---

## 0. Scope and question

Two legs, both from the frozen block:

- **Leg (a) — path.** Does the delivered frozen v1.2 panel reproduce the **observed PHL completion path** at the
  33 observed year-level comparison points? (V1's 33 comparisons; §2 below fixes the construction exactly.)
- **Leg (b) — link.** Does a **declared** cross-level accounting constraint `upper_t ≤ κ · lower_{t−3}` with
  **κ = 0.949** (an observed median, declared, **never fitted**) bind in the generator — and if it binds, into which
  of the predeclared outcome classes **b1/b2/b3** does the result fall?

**Data used.** Frozen `generator_v1_2/code/sim_v1_2.py` (sha256 `61123aa9…`), `generator_v1_2/PARAMS.md`,
`generator_v1_2/results/synthetic_panel_v1_2.csv` (sha256 `14729c51…acf5ac`, 6 720 rows, 30 countries ×
1970–2025 × 4 levels); `10_massification/data/UNIVERSALIZATION_SERIES.csv` (PHL `completion_primary`,
`completion_lower_secondary`, `completion_upper_secondary`, `status=observed`, 11 each). **No web, no external
data, no writes outside this directory, no DATA ASK.** `09_relations/data/panel_wdi_long.csv` is not needed:
leg (b)'s lag is a declared 3-year accounting lag fixed by the block, not a duration estimate.

**Copy discipline.** The only v1.2 object this experiment writes inside its own directory is a **byte copy** of the
frozen panel (for the baseline guard). The κ-link is applied **in memory** as a declared post-processing constraint
on that unmodified copy. **No generator code is edited, and no generator file is written.**

---

## 1. Frozen extract from `SYNTHESIS_022.md` §6 EXP-7 — **verbatim**

Quoted from `08_council/brief_022/SYNTHESIS_022.md`, §6 "EXP-7 — **REPRO-PATH**", items 2 and 5,
character-for-character (line breaks preserved as in the source):

> 2. **What changes if positive vs negative.** **Leg (a), path:** `PATH-REPRODUCED` iff **≥17/33 (51.5%)** of observed
>    year-level comparisons are within **±5 pp** → the synthetic level claims are readable as levels and v1.2's label
>    stands. Else `ENDPOINT-ONLY` (currently 9/33 = 27.3%) → **v1.2 is relabelled** "crossing/endpoint placement", every
>    synthetic level statement in EXP-1/EXP-2/A3-S is re-scoped to 2022–2024, and the next model line starts from the
>    **lower** series (median −29.44 pp). **Leg (b), link:** add the declared constraint
>    `upper_t ≤ κ · lower_{t−3}` with **κ = 0.949** (median of the 8 observed PHL pairs; sensitivity κ = 0.960, the
>    pre-2018 median), on an **unmodified copy** with a byte-identical baseline guard, no other change, no re-fit. Three
>    predeclared outcome classes: **(b1)** upper 2024 stays in **[73,77]** → the link is compatible and the ceiling can be
>    inherited; **(b2)** upper 2024 **< 71** → the link binds and the binding defect is the **lower series**, not the upper
>    ceiling (the expected class given 0.949 × 67.41 = 63.9); **(b3)** **|Δ| < 1.0 pp** → the link is non-binding and the
>    upper block dominates.

> 5. **Threshold + falsifier.** Leg (a): **≥17/33 within ±5 pp** = `PATH-REPRODUCED`; falsifier = ≤16/33. Leg (b): the
>    three classes above; **falsifier for the link** = a baseline panel that is not byte-identical
>    (`14729c51…acf5ac`) or any parameter moved besides the declared κ. Both legs report all 33 comparisons, not a subset.

**Frozen data item (verbatim, item 4, operative sentence):**

> 4. **Data on disk.** `generator_v1_2/results/synthetic_panel_v1_2.csv` (`completion_uis`, `level`, `year`,
>    `country_id`); `10_massification/data/UNIVERSALIZATION_SERIES.csv` (PHL `completion_primary`,
>    `completion_lower_secondary`, `completion_upper_secondary`, `status=observed`); frozen
>    `generator_v1_2/code/sim_v1_2.py` (`61123aa9…`) copied unmodified for leg (b) exactly as CEIL-ATTRIB did.

---

## 2. Frozen pre-existing facts this experiment audits (Council V1–V2, quoted)

These are the Council's read-only re-derivations, already on disk in the brief **before** this predeclaration.
They are **not** this experiment's results; they are the numbers leg (a) and leg (b) audit, and they are quoted so
that the verdict cannot be re-worded around them.

> **V1** — v1.2 reproduces endpoints, not the path. Against the 11 observed PHL years × 3 levels (33 comparisons),
> the UIS-convention completion series is within **±5 pp in 9/33 (27.3%)**, ±10 pp in 13/33 (39.4%). Median signed
> deviation: primary **−4.30**, lower-secondary **−29.44**, upper-secondary **−27.59** pp. The 2024 upper value is
> **+1.61 pp** (76.64 vs 75.03); every pre-2021 upper and lower value is **24–37 pp low** (worst: upper 1999
> **−36.62**, lower 2000 **−33.37**).

> **V2** — v1.2 has no cross-level linkage; the anchor type violates the pipeline bound. Synthetic
> `upper_t / lower_{t−3}` exceeds **1.10** in **12 years for `SYN00_PHL_LIKE`**, including every year 2013–2024;
> panel-wide **177/1 590 cells (11.1%)**, max **1.444** (`SYN07`, 2014); the observed PHL maximum is **1.072**. The
> model can complete upper secondary for cohorts that never completed lower secondary — the accounting the observed
> ceiling obeys.

---

## 3. Leg (a) — the 33-comparison construction, fixed **now**, in full

### 3.1 The comparison universe (33 cells, fixed denominator)

A **comparison** is one **(year, level)** cell defined by the **observed** side. The universe is:

- source: `10_massification/data/UNIVERSALIZATION_SERIES.csv` (sha256 `85bc8693…`), rows with
  `iso3 == "PHL"` **and** `status == "observed"` **and** `indicator ∈ {completion_primary,
  completion_lower_secondary, completion_upper_secondary}`;
- that is **11 cells per level, 33 cells total**, with these year sets (read from disk at freeze time, not chosen):
  - `primary` (11): 1999, 2000, 2004, 2008, 2010, 2013, 2017, 2021, 2022, 2023, 2024
  - `lower_secondary` (11): 1999, 2000, 2004, 2008, 2010, 2013, 2017, 2021, 2022, 2023, 2024
  - `upper_secondary` (11): 1999, 2000, 2003, 2004, 2008, 2010, 2013, 2017, 2022, 2023, 2024
- **the year sets differ by level** (2003 exists only for upper; 2021 exists only for primary and lower). The
  comparison universe is the **cell**, not the calendar year: 33 cells, **not** 12 years × 3 levels = 36. This is
  exactly the block's "11 observed years × 3 levels" read at the cell level, and it is the only construction that
  yields 33. No cell is added, dropped, or averaged across years.

### 3.2 The synthetic side and the mapping

- source: `generator_v1_2/results/synthetic_panel_v1_2.csv`, rows with `country == "SYN00_PHL_LIKE"` (the anchor
  type: the only v1.2 country built on the observed PHL cohort path), `year` equal to the observed cell's year, and
  `level` mapped **one-to-one with no substitution**: `primary → primary`, `lower_secondary → lower_secondary`,
  `upper_secondary → upper_secondary`.
- value: `completion_uis`, which is written as a **fraction (0–1)** in the panel. It is converted to percent by
  `× 100` so that it is on the observed series' unit (`percent`, 0–100). This conversion is units-only; it moves no
  parameter and applies no adjustment. Check: 2024 upper becomes **76.64**, matching V1's stated 76.64.
- **no interpolation, no nearest-year substitution, no re-basing, no country substitution.** The year match is
  **exact**. `SYN00_PHL_LIKE` is the only synthetic country eligible; the other 29 synthetic countries are not
  used in leg (a) because no observed comparison exists for them (and none may be manufactured).

### 3.3 The statistic

- **deviation** `d = synthetic − observed`, in **pp**, computed at full float precision and reported to 2 dp.
- **within ±5 pp** iff `|d| ≤ 5.0` **inclusive**, on the unrounded value (display rounding never decides a pass).
- **count within ±5** = number of the 33 cells with `|d| ≤ 5.0`.
- Non-verdict-bearing companions, all reported: count within ±10 pp; per-level count within ±5 and per-level median
  signed deviation; maximum |miss|; the number of cells where the synthetic value is **above** the observed value.

### 3.4 Missing-cell rule (declared, and the only admissible handling)

1. If the observed cell set is **not** 33 at run time, leg (a) = `VOID` (input sha is guarded, so this can only mean
   the input changed). Nothing is filled in.
2. If a synthetic cell needed for an observed cell is **absent**, the comparison is still emitted, with
   `synthetic_value = MISSING`, `deviation_pp = MISSING`, `within_5pp = NO`, and it **stays in the denominator (33)**.
   It is **not** dropped, **not** imputed, **not** replaced by a neighbouring year.
3. If a synthetic value is present but non-numeric, it is treated as `MISSING` under rule 2 and the row is flagged
   `non_numeric`.
4. Synthetic-only years (1970–1998, 2025, and any year with no observed cell) are **never** compared and are not
   part of the denominator.

### 3.5 Leg (a) verdict rule (fixed)

- `PATH-REPRODUCED` iff `count_within_5pp ≥ 17` (≥ 51.5% of 33).
- `ENDPOINT-ONLY` iff `count_within_5pp ≤ 16` (the block's falsifier).
- `VOID` iff the observed universe is not 33 cells or the guarded input hashes do not match.
- Exactly one token. All 33 comparisons are reported, not a subset.

---

## 4. Leg (b) — the declared κ-link, fixed **now**, in full

### 4.1 The constraint

**`upper_t ≤ κ · lower_{t−3}`**, with **κ = 0.949** and `lower_{t−3}` the **lower-secondary** `completion_uis` of the
**same country** at year **t − 3**.

- **κ = 0.949** is the **median of the 8 observed PHL `upper_t / lower_{t−3}` pairs** (V4/V5 pair rule: t−3 exact,
  else nearest within ±1 y, else drop; 7 of 8 in [0.90,1.10], 0.889–1.072). It is **declared, not estimated, and
  never fitted**: it is not re-derived at run time, not updated from the panel, and not swept to make the link bind.
  The run may **verify** that the median of those 8 pairs is 0.949 and must report that check, but a mismatch would be
  reported as `KAPPA-PROVENANCE-MISMATCH` and would **not** license a different κ.
- **sensitivity κ = 0.960** (the pre-2018 median, per the block) is run in parallel and reported. It is
  **non-verdict-bearing**; the verdict uses 0.949 only.
- The constraint is an **accounting/necessary-condition** statement of the form the observed series obeys
  (`upper_t/lower_{t−3}` ≤ 1.072 observed max). It is a **declared** constraint. **It is not a causal claim, not a
  direction claim, and not a fitted relationship.**

### 4.2 The scored cells (fixed)

- **country:** `SYN00_PHL_LIKE` (the anchor type used by V2/V3/V8 and by the block's b1–b3, which are stated on the
  anchor type's upper 2024).
- **years:** every panel year `t` in **1970–2025** for which **both** `upper_secondary(t)` and
  `lower_secondary(t−3)` exist in the frozen panel. That is **t = 1973 … 2025 = 53 cells**.
- **t ∈ {1970, 1971, 1972}** have no `t−3` inside the panel (panel starts 1970). They are recorded as
  **`NOT-SCORABLE`** with reason `no lower_{t-3} in panel`, are **excluded from the violation denominator** (which is
  reported as 53), and are **never imputed** from outside the panel (no extrapolation, no back-cast).
- cells are matched **exactly** by (country, year, level). No nearest-year matching is used in leg (b); the 3-year lag
  is exact by declaration.
- units: `completion_uis` is a fraction; the constraint is **scale-invariant** (`upper_t ≤ κ·lower_{t−3}` is a ratio
  statement). It is therefore evaluated on the native fractions and **reported** in pp (×100) for readability. The
  ratio `R_t = upper_t / lower_{t−3}` is unit-free and is reported to 6 dp.

### 4.3 Violation, enforcement, and the "after" arm

- **violation** at t iff `upper_t > κ · lower_{t−3}` — **strict** comparison, no epsilon, no tolerance band.
  `violation_margin_pp = (upper_t − κ·lower_{t−3}) × 100`, reported for every scored cell (negative = slack).
- **enforcement (the declared post-processing constraint):** `upper_t^linked = min(upper_t, κ · lower_{t−3})`,
  applied **only** to `upper_secondary` at scored years, **in memory**, on the unmodified copy. **Nothing else
  changes** — no other level, no other year, no other parameter. This is the whole intervention; it is a declared
  constraint projection, not a re-fit (no quantity is estimated from the panel).
- **Δ_t** = `upper_t^linked − upper_t` (pp), reported per cell and summarised.
- **violations after** the link are reported and **must be 0 among the 53 scored cells**. That is a check on the
  implementation, not a second finding; if it is not 0 the leg is reported `LINK-IMPLEMENTATION-FAIL` and no
  outcome class is assigned.

### 4.4 The three predeclared outcome classes (verbatim thresholds; **class assignment rule fixed now**)

Evaluated on **upper_secondary 2024 of `SYN00_PHL_LIKE`**, `after = min(upper_2024, 0.949·lower_2021)`:

- **b1** — upper 2024 stays in **[73,77]** (inclusive) → the link is compatible and the ceiling can be inherited.
- **b2** — upper 2024 **< 71** → the link binds and the binding defect is the **lower series**, not the upper ceiling
  (the block's expected class given 0.949 × 67.41 = 63.9).
- **b3** — **|Δ| < 1.0 pp** → the link is non-binding and the upper block dominates.

**Precedence when more than one class is arithmetically true (fixed now, in advance):** **b2 > b3 > b1.**
Rationale: b2 is the sharp binding outcome; b3 asserts the link does not bind at all, so it must outrank b1
("compatible", which is vacuous if the constraint never bites); b1 then applies only when the link does bite
(|Δ| ≥ 1.0 pp) and lands inside the declared band. b2 and b3 cannot both be true (b2 requires `after < 71`, which
forces |Δ| ≥ 1.0 pp whenever the unlinked value ≥ 72, and the block's own baseline is 76.64).

**Residual class, declared now so that nothing is invented after results:** if none of b1/b2/b3 holds — e.g. `after`
lands in **[71,73)** or above 77 — the class is **`b-UNCLASSIFIED`** and **both** the unlinked and linked 2024 values
are reported with the arithmetic. `b-UNCLASSIFIED` is a reported class, not a failure of the run, and it licenses
**no** inheritance claim. It is not a licence to adjust a boundary.

**All three classes are evaluated and all three are reported, including the ones that are false on the numbers.**
The verdict names the unique class after precedence, plus the component numbers (unlinked 2024, bound, linked 2024,
Δ, ratio) so the reader can recompute every boundary by hand.

### 4.5 Baseline-invariance guard (verdict-critical; the block's falsifier)

The unlinked arm **must reproduce the frozen panel byte-for-byte**. Four checks, all reported:

- **G1** — `sha256(generator_v1_2/results/synthetic_panel_v1_2.csv) == 14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac`
  (the block's `14729c51…acf5ac`; recorded in full here so the prefix cannot drift).
- **G2** — the copy this experiment writes at `results/BASELINE_UNLINKED_PANEL.csv` is a **byte copy** and its
  sha256 equals the same value.
- **G3** — every value used in `results/KAPPA_LINK.csv` for the unlinked arm is read from that byte-identical copy,
  and the 53 scored cells are additionally re-read from the frozen original and compared cell-by-cell; any
  difference = **G3 FAIL**.
- **G4** — the frozen generator files (`code/sim_v1_2.py`, `PARAMS.md`, `RUN_MANIFEST.json`, the panel) have the
  **same sha256 after the run as before it**; `sim_v1_2.py` must remain `61123aa9…`. No file under
  `generator_v1_2/` is written.

**Any guard failure ⇒ leg (b) = `BASELINE-GUARD-FAIL`, the link result is recorded as `INVALID`** (components still
printed), **and the block's falsifier is triggered**: no outcome class is licensed, no inheritance claim is made, and
the failure is the finding. The guard is the same invariance test CEIL-ATTRIB passed.

---

## 5. Verdict vocabulary (exactly this; nothing invented)

| token | meaning |
|---|---|
| `PATH-REPRODUCED` | leg (a): ≥ 17/33 within ±5 pp |
| `ENDPOINT-ONLY` | leg (a): ≤ 16/33 within ±5 pp (the block's falsifier) |
| `VOID` | leg (a) could not be constructed as declared (input hash/cell-count failure) |
| `b1` | leg (b): linked upper 2024 ∈ [73,77] |
| `b2` | leg (b): linked upper 2024 < 71 |
| `b3` | leg (b): \|Δ\| < 1.0 pp at 2024 |
| `b-UNCLASSIFIED` | leg (b): no b1/b2/b3 holds; arithmetic reported, no inheritance claim |
| `BASELINE-GUARD-PASS` | G1–G4 all hold |
| `BASELINE-GUARD-FAIL` | any of G1–G4 fails; leg (b) is `INVALID` |
| `NOT-SCORABLE` | a cell-level status (1970–1972 lower_{t−3} absent), never a verdict |

**Combined EXP-7 verdict string:** `<leg-a-token> + <b-token> + <guard-token>`.
No other token may appear in a `verdict` field of any results file. Prose in `FINDINGS.md` may explain, but may not
rename.

---

## 6. Pre-freeze calibration of the bars (**not results** — arithmetic from the block and V1/V2)

Stated so that the reader can see the bars were not chosen after the numbers:

- Leg (a) bar 17/33 sits **8 comparisons above** the already-published V1 count (9/33). A reproduction claim needs a
  majority of the path, not one more than a third.
- Leg (b) expected class per the block is **b2** (0.949 × 67.41 = **63.97** < 71), with |Δ| ≈ 12.7 pp — far outside
  b3's 1.0 pp, so b3 is not the expected class and is not being fitted as one.
- V2 already reports the anchor type above 1.10 in 12 years (every year 2013–2024), so violations **before** the link
  are expected to be numerous; the informative quantity is **where** the link bites and **what 2024 becomes**, not
  whether violations exist.
- The observed maximum ratio is 1.072; κ = 0.949 is the observed **median**, i.e. the link is deliberately placed at
  the centre of the observed distribution, not at its max. It is therefore expected to bind on the synthetic panel,
  which sits far above the observed distribution. **That expectation is stated before the run and is not evidence.**

---

## 7. Reporting discipline (frozen)

1. **All 33 comparisons** are written to `results/PATH_COMPARISONS.csv`, one row per cell, with year, level,
   synthetic, observed, deviation pp, within-±5 flag, within-±10 flag, and the mapped panel row identity.
2. **All 53 scored cells** (plus the 3 `NOT-SCORABLE` years, flagged) are written to `results/KAPPA_LINK.csv` with
   `upper_t`, `lower_{t−3}`, ratio, bound (κ=0.949), bound (κ=0.960), violation flags before, margins, linked value,
   Δ, violation after, class, and status.
3. `results/REPRO_PATH_RESULTS.csv` is a long-format table of **(test, statistic, value, threshold, verdict,
   components)** covering leg (a), leg (b), the κ sensitivity, and the baseline guard.
4. `results/BASELINE_GUARD.json` records G1–G4 with the hashes and the pre/post comparison.
5. `FINDINGS.md` is plain English and states: the descriptive/diagnostic status, **no causal or direction claim**,
   that `m = 1.10` and v1.2's scope are unchanged, and the implication for the v1.5 BIMODAL-GATE predeclaration
   (whether the pipeline link must be **built into** v1.5 rather than post-processed).
6. Labels `SYNTHETIC` / `OBSERVED` appear on every number that is one or the other; every file carries the
   no-causal-claim statement.
7. **Determinism:** the script is RNG-free and timestamp-free; it is run twice into `results/` and
   `results/determinism_run2/`, and every output is compared byte-for-byte. Any difference is reported as
   `NON-DETERMINISTIC` and is a finding.

---

## 8. No-threshold-change statement

The thresholds in this file — **17/33**, **±5 pp inclusive**, **κ = 0.949** (sensitivity 0.960), the **exact 3-year
lag**, the **53 scored cells / 33 comparison cells**, the **[73,77] / <71 / |Δ|<1.0** class boundaries, the
**b2 > b3 > b1** precedence, and the **byte-identical** guard — are fixed at the sha256 recorded in
`PRE_DECLARATIONS.sha256` **before the first run**, and are reported against exactly as written. **No threshold, bar,
year set, cell rule, κ, class boundary or verdict word will be changed after results are seen.** If a result sits on a
boundary, the boundary as written decides, and the proximity is reported.
