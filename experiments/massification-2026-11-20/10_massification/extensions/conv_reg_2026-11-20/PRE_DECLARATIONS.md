# EXP-21 CONV-REG — PRE_DECLARATIONS

**Cell:** EXP-21 **CONV-REG** (rank #1 of the cycle-17 slate), Council brief 025, D156 #1.
**Question (frozen):** which object may carry which level statement, and is one constant conversion enough?
**Type:** descriptive register. Reads on-disk observed series and two frozen synthetic panels; **no model run, no
re-fit, no RNG, no proxy, no adoption, no causal or direction claim.**
**Write scope:** `10_massification/extensions/conv_reg_2026-11-20/` only. No existing repo file is modified.

**Status of this document.** Written and hashed **before** any register number was computed. The hash is
`PRE_DECLARATIONS.sha256` and is **enforced by `code/run_conv_reg.py` at the moment the verdict is written**
(D158(1)/§7 rule 1); a mismatch aborts the run with no verdict written. Nothing in §4 below adds a threshold:
§1 is the frozen block, copied verbatim. §4 only *operationalises* what the block already fixes (spelling out
comparison inclusivity, the crossing rule, the counting denominator, and the one state the block's three overall
labels do not name), and every such operational clause is flagged **`DECLARED-OPERATIONAL`** in place.

---

## 0. Machine-readable freeze fields

| field | value |
|---|---|
| cell | EXP-21 CONV-REG |
| authority | `08_council/brief_025/SYNTHESIS_025.md` §6.1 (verbatim in §1 below); `08_council/DECISIONS.md` D156 (EXP-21 clause verbatim in §2.1), D153(xi) (§2.2), D158 (§2.3) |
| thresholds frozen before results | yes — §1 verbatim; **no threshold may change after this file is hashed** (§8) |
| systems in the frozen test | PHL, KOR, KHM, CHN (block, §1 item 5) |
| levels in the frozen test | primary, lower_secondary, upper_secondary |
| statistic | `T = completion / GER`, same system × level × year, both `status = observed` |
| band | `T ∈ [0.85, 1.15]` |
| in-band rule | `>= 80 %` of that level's **paired** cells |
| range rule | `max(T) − min(T) <= 0.30` |
| identification gate | `< 3` same-year pairs → `THIN`, neither label |
| overall labels | `UNVERIFIED > REGISTER-BINDING > REGISTER-UNIFORM` (D147(i) precedence, stated as a block field per D158(6)) |
| m-constancy tolerance | `1e-9` on the model panel |
| falsifier | any register line not traceable to a named file + column → `UNVERIFIED`; no register line may be cited |
| verdict scope for `REGISTER-*` | the 12 frozen cells (4 systems × 3 levels); HKG/JPN are reported as **not in the frozen system list** and enter no verdict path (§4.8) |
| determinism | two runs, byte-identical (§9) |

---

## 1. The frozen block, verbatim

Copied without edit from `08_council/brief_025/SYNTHESIS_025.md`, §6.1, lines 473–525 (items 1–7 of the
seven-field block). This is the definition-and-threshold source; §4 does not replace it.

```markdown
### 6.1 EXP-21 — **CONV-REG**: which object may carry which level statement, and is one constant conversion enough? (rank **#1**)

1. **First-order link (measurement for every remaining level sentence).** *(This is the re-scoped successor of
   **EXP-15 CONV-REG**, ranked #5 / drop-first in cycle 15 and never run. It is now the right object, for a different
   reason: in cycle 15 the register was an **input to a repair** that no longer exists; in the post-generator phase it is
   the **licence for the write-up's own numbers** — and EXP-19 has since shown that a conversion which fails its own
   identification gate can still look decisive, so the register must separate identification from arithmetic. EXP-15's
   band test is kept unchanged, so the old question is answered rather than replaced.)* After the close, every level
   sentence the programme can still write is a sentence about one of four objects — `completion` (UIS), `GER`, `NER`, or
   the model's `completion_uis` / `demand_share` — and the record does **not** establish that they are one scale.
   EXP-16's `demand_share`, EXP-18's 33-cell verdict and the write-up's three headline numbers (98.3046 / 92.4140 /
   75.0253) all depend on which object is meant. This is the **precondition** for EXP-22, EXP-25 and every number in §4.
2. **What changes if positive vs negative.** **`REGISTER-UNIFORM`** (every system×level `INTERCHANGEABLE`, every wedge
   constant) → the write-up may use "completion" once, compare freely, and the 33-cell verdict needs no convention
   caveat; the register is one page. **`REGISTER-BINDING`** (any system×level not interchangeable, or any wedge that
   crosses 1.0 / varies beyond the band) → a **binding per-system × level register** is issued: every level sentence in
   the write-up and every future results table cites its object; **cross-object comparisons are barred** where the
   register says so; the constant-`m` convention is recorded as a **point** convention, not a level one, and §2.3 C-2
   stands. Either way the register is the citation for "which object" and the programme stops using three names for one
   thing.
3. **Why it is not a niche.** It is the only cell that can license the write-up's own numbers. Without it the paper
   cannot say "completion rose to 98.3 %" without an equivocation, and cannot say "the model is 13.4 pp low" without a
   convention caveat it has not measured. It is also the cell that retires the failure class that produced three
   recorded defects (WT5's cross-year ratio; v1.2 FINDINGS §1.2's 1.136; GER as a pipeline numerator).
4. **Data on disk (no DATA ASK).**
   `10_massification/data/UNIVERSALIZATION_SERIES.csv` — `completion_primary`, `completion_lower_secondary`,
   `completion_upper_secondary`, `ger_primary`, `ger_lower_secondary`, `ger_upper_secondary`, `ner_primary`,
   `ner_lower_secondary`, `ner_upper_secondary`, `status = observed`, and the 11 completion years
   (1999, 2000, 2004, 2008, 2010, 2013, 2017, 2021, 2022, 2023, 2024);
   `synthetic_2026-11-20/generator_v1_7_partrepair/results/panel_A17.csv` — `completion_uis`, `completion_cohort`,
   `measurement_factor`, `ger`, `demand_share`; `synthetic_2026-11-20/generator_v1_2/results/synthetic_panel_v1_2.csv`
   and `generator_v1_2/PARAMS.md` for the `m = 1.10` declaration; `data/gmr_observed_6countries_1970_2024.csv` for the
   GER series. Anchors (re-derived): PHL primary `completion/GER` **0.802590** (1999) → **0.925039** (2017) →
   **1.073853** (2021) → **1.045426** (2024); `measurement_factor = 1.1` in every A17 cell with
   `completion_uis/completion_cohort` = 1.1 ± **8.8395202269e-10** (6,720 rows).
5. **Threshold + falsifier (fixed before freeze).** For each **system × level** (PHL, KOR, KHM, CHN), for every year
   with **both** `completion` and `GER` observed, compute `T = completion/GER`. **Register label: `INTERCHANGEABLE` iff
   `T ∈ [0.85, 1.15]` in ≥ 80 % of that level's paired cells AND `max(T) − min(T) ≤ 0.30`; else
   `NOT-INTERCHANGEABLE`.** Report, per level: n pairs, `T_min`, `T_max`, the share in band, and **the year(s) at which
   `T` crosses 1.0** (a crossing is reported even when the band test passes). **Identification gate (binding, from
   EXP-19's lesson):** a level with **< 3** same-year pairs is reported `THIN` and **may not** receive an
   `INTERCHANGEABLE` label (it is neither interchangeable nor barred, it is unmeasured). **`m`-constancy test:** the
   model's `completion_uis/completion_cohort` must equal 1.10 within **1e-9** in every cell — it does (V34); the report
   states separately that the **observed** analogue `T` is *not* assumed constant. **Verdict (precedence stated per
   D147(i)):** `UNVERIFIED > REGISTER-BINDING > REGISTER-UNIFORM`, where `REGISTER-BINDING` iff any level is
   `NOT-INTERCHANGEABLE` or any `T` crosses 1.0. **Falsifier:** any register line that cannot be traced to a named file +
   column → `UNVERIFIED`, and no register line may be cited.
6. **Closed-claim check.** Does **not** re-derive V6 (V6 established that GER is not a pipeline numerator for the
   *ratio*; this is about *level* statements); does **not** run EXP-15 (never run — this is its re-scoped successor, and
   the difference is stated in item 1); does **not** re-score EXP-18's 33 cells (it reads no deviation); adopts no value;
   no fit; no causal or direction claim.
7. **Cost / rank.** **Small** (read-only arithmetic on observed series and two panels; no RNG, no run). **Rank #1** —
   it is the precondition for #2 and #5 and for every level sentence the write-up may keep.
```

---

## 2. Decision-form record, verbatim

### 2.1 D156 — the EXP-21 clause

From `08_council/DECISIONS.md`, D156 (2026-11-21 02:05):

```markdown
**EXP-21 CONV-REG** — which object may carry which level statement, and is one constant conversion enough? (per system×level, `T = completion/GER` on same-year pairs; `INTERCHANGEABLE` iff T ∈ [0.85,1.15] in ≥80% of that level's paired cells **and** max−min ≤ 0.30, else `NOT-INTERCHANGEABLE`; **identification gate:** a level with <3 same-year pairs is `THIN` and may receive neither label; report T_min, T_max, in-band share and the year T crosses 1.0; m-constancy tested at 1e-9; precedence `UNVERIFIED > REGISTER-BINDING > REGISTER-UNIFORM`; falsifier: any register line not traceable to a named file+column → `UNVERIFIED`) **rank #1**
```

### 2.2 D153(xi) — the non-constant observed relation

From `08_council/DECISIONS.md`, D153, clause (xi) only (the clause this cell exists to measure):

```markdown
(xi) **the size of the level miss is not decomposable** — `measurement_factor = 1.1` in every A17 cell and completion_uis/completion_cohort = 1.1 ± **8.8395202269e-10** over 6,720 rows, while observed completion/GER is **not constant** (PHL primary 0.802590 (1999) → 0.925039 (2017) → 1.073853 (2021) → 1.045426 (2024), **crossing 1.0 between 2017 and 2021**); "behaviourally 10.7–17.1 pp wrong" is **barred** until EXP-21; the verdict "does not face the observed completion series as delivered" stands;
```

### 2.3 D158 — the seven authoring rules (decision form)

From `08_council/DECISIONS.md`, D158 (2026-11-21 02:05). §6 carries the same seven rules in the brief's own words.

```markdown
| D158 | 2026-11-21 02:05 | **Seven authoring rules added (cycle 17), all binding on the next predeclaration.** (1) **Hash enforcement at verdict time** — a hash cited in a verdict row must be enforced by the runner when the verdict is written; a recorded-but-unenforced hash may be cited only as **`RECORDED-NOT-ENFORCED`** and may carry no verdict (EXP-16's RESULTS.csv hash). (2) **Object identity before comparison** — no two series may be compared/subtracted/placed unless both carry the same declared denominator/convention; otherwise the result is **`NOT-COMPARABLE`**, not a number; a comparison table not stating the convention is returned (EXP-18 C-2 / D153(xi)). (3) **Register before sentence** — no write-up sentence may use a number whose register line (convention, window, label, source) does not exist; a sentence without a register line is `UNVERIFIED` and may not ship. (4) **Level-symmetric legs** — a leg intended to test a two-level object must require **both** levels; a leg satisfiable by one level must say so in its own sentence and may not be cited as evidence about the object it was meant to protect. (5) **Class tags** — every model number carries its class (v1.6 or v1.7 or v1.5) and every localisation sentence names the class (D153(x)). (6) **Banned sentences register** — the barred phrasings ("demand falsified", "the participation margin is duplicated" as a cell sentence, "the upper-secondary ceiling is structural", "survival loses 50.7%", "fix survival only", "A17 0/33 vs A00 9/33" without its sentence, "behaviourally N pp wrong" before EXP-21) are enumerated and a predeclaration using one is returned. (7) **Label discipline for REQUIRED-STATE/DERIVED** — any λ*, required coverage or derived target carries "REQUIRED-STATE (EXP-17); not adopted" / "DERIVED" in the same sentence as the number. | the standing failure modes are laundered labels and transcription errors; rules living only in a decision log survive one cycle, so each becomes a predeclaration check | Council records; Lead enforces in every new predeclaration |
```

---

## 3. What this cell is not (closed-claim check, from the block's item 6)

- It does **not** re-derive V6: V6 established that GER is not a *pipeline numerator* for a *ratio*; this cell asks
  about *level* statements.
- It does **not** re-run EXP-15 (never run). It is EXP-15's re-scoped successor; the band test is kept unchanged.
- It does **not** re-score EXP-18's 33 cells; it reads no deviation, computes no model score, and cannot be cited
  as a re-score.
- It adopts no value, fits nothing, runs no model, constructs no proxy, makes no causal or direction claim, and
  licenses **no** change to any model, parameter or target. `m` is read, never set.
- It does **not** test NER. `ner_primary` / `ner_lower_secondary` / `ner_upper_secondary` are named in the block's
  data list and are present on disk, but the frozen statistic is `completion/GER` only; **this cell computes no
  NER statistic and no NER line may be cited from it** (§4.2).
- It does not touch the running server, does not read the web, and writes nothing outside its own directory.

---

## 4. Operational specification (frozen; `DECLARED-OPERATIONAL` clauses flagged)

Every number below is a **derived arithmetic product of two observed fields** → label `DERIVED`; the two inputs
are `OBSERVED`. Model-panel numbers are `SYNTHETIC`. No other label is used in the results files.

### 4.1 Objects

| id | object | file | column(s) | label | denominator stated by the file |
|---|---|---|---|---|---|
| O1 | UIS completion rate, level L | `10_massification/data/UNIVERSALIZATION_SERIES.csv` | `completion_primary`, `completion_lower_secondary`, `completion_upper_secondary` | OBSERVED (rows `status = observed`) | population **3–5 years above** the official graduation age (`DATA_NOTES_MASSIFICATION.md`, "Definition trap" §85–98) |
| O2 | gross enrolment ratio, level L | same file | `ger_primary`, `ger_lower_secondary`, `ger_upper_secondary` | OBSERVED (rows `status = observed`) | the level's **official age band** (gross: all ages enrolled / band population) |
| O3 | model completion, UIS convention | `10_massification/extensions/synthetic_2026-11-20/generator_v1_3/results/synthetic_panel_v1_3.csv` (and `generator_v1_2/results/synthetic_panel_v1_2.csv`, `generator_v1_7_partrepair/results/panel_A17.csv`) | `completion_uis` | SYNTHETIC | model-internal; `= m × completion_cohort` |
| O4 | model completion, cohort-flow convention | same panels | `completion_cohort` | SYNTHETIC | model-internal |
| O5 | declared measurement constant | `generator_v1_2/PARAMS.md` §7 ("Measurement convention (check d)") | `meas_completion_factor m = 1.10` | DECLARED / CONVENTION | — |
| — | NER | `UNIVERSALIZATION_SERIES.csv` | `ner_*` | OBSERVED | **not used** in any statistic (§3) |
| — | `demand_share` | panels | `demand_share` | SYNTHETIC | **not used** in any statistic; EXP-22's object |

`T` is defined **only** on O1/O2. `completion_uis/completion_cohort` is defined **only** on O3/O4. The two tests are
never pooled: the model ratio is a *declared* identity on a synthetic panel, the observed `T` is a *measured* ratio
of two differently-denominated observed series. Stating this separation is the point of the cell.

### 4.2 Pair rule — object identity before comparison (D158(2))

A pair exists for (system `iso3`, level L, year Y) **iff all four hold**:

1. a `completion_<L>` row exists with `iso3 == system`, `year == Y`, `status == "observed"`, value finite and `> 0`;
2. a `ger_<L>` row exists with `iso3 == system`, `year == Y`, `status == "observed"`, value finite and `> 0`;
3. the level tags agree (`completion_lower_secondary` pairs with `ger_lower_secondary`, **never** with `ger_secondary`
   — the total-secondary GER is a different level and cannot carry a lower-secondary statement);
4. the year is identical on both sides — **no lag, no interpolation, no nearest-year substitution, no carry-forward.**

Otherwise the cell contributes **`NOT-COMPARABLE`** and **no number**: the year is counted in
`n_not_comparable_years` and is excluded from `n_pairs`. `ger_secondary`, `gross_intake_*`, `oos_*`, `ner_*` and the
`check`/`derived` rows are never paired with a completion column. `T` is computed as `completion / ger` in the
file's own units (both percent); the ratio is dimensionless.

### 4.3 `T` and the band test

`T_Y = completion_L(Y) / ger_L(Y)`, carried at full double precision; **no rounding is applied before any test**,
and reporting to 6 dp is display only.

- `in_band` iff `0.85 <= T <= 1.15` (closed interval; endpoints inclusive — `DECLARED-OPERATIONAL`).
- `in_band_share = n_in_band / n_pairs`, denominator = **paired cells** (the block's words: "that level's paired
  cells"), not all years in the series.
- `range = T_max − T_min`; `range_ok = (range <= 0.30)` (inclusive — `DECLARED-OPERATIONAL`).

### 4.4 Per-cell label (exactly the block's two labels plus the gate's `THIN`)

```
if n_pairs < 3              -> THIN                        (neither label; unmeasured)
elif in_band_share >= 0.80 and range_ok -> INTERCHANGEABLE
else                        -> NOT-INTERCHANGEABLE
```

`THIN` is evaluated **first** and is the identification gate, not a verdict. A `THIN` cell is **not**
"interchangeable" and **not** "barred"; it is unmeasured, and no sentence may treat it as either.

### 4.5 Crossing years

For a cell's paired years sorted ascending, let `s(Y) = -1 if T_Y < 1`, `0 if T_Y == 1`, `+1 if T_Y > 1`. A
**crossing** is a consecutive pair `(Y1, Y2)` with `s(Y1) * s(Y2) < 0`, **or** with `s(Y1) != 0 and s(Y2) == 0`
(arrival at 1.0 exactly). The **crossing year** is `Y2`; consecutive-pair crossings only, so a level whose `T`
wanders across 1.0 several times reports **every** crossing year, semicolon-joined in year order, plus
`n_crossings` and the `crossing_interval` (`Y1->Y2`) of the first. A crossing is reported **even when the band
test passes**, and it does **not** by itself change a cell's label; it enters the overall verdict (§4.7), as the
block states.

### 4.6 `m`-constancy test (model panel)

For every row of the panel: `r = completion_uis / completion_cohort`;
`dev_ratio = |r − 1.10|`, `dev_factor = |measurement_factor − 1.10|` (where `measurement_factor` exists).
Test at **`1e-9`**, inclusive (`DECLARED-OPERATIONAL` on inclusivity).

- `CONSTANT` iff every testable row has `dev_ratio <= 1e-9` and `dev_factor <= 1e-9`, **and** no row is untestable.
- A row with `completion_cohort` null or `0` is `NOT-TESTABLE`; it is counted in `n_not_testable` and cannot be
  silently dropped: if `n_not_testable > 0` the verdict is `CONSTANT-ON-TESTABLE-SUBSET`, never `CONSTANT`.
- Otherwise `NOT-CONSTANT`.

A supporting identity check is reported (`max_abs_rel_residual` of `completion_uis` against
`1.10 × completion_cohort`), but the verdict rests on the `1e-9` ratio test above, not on the identity residual.

The panel set is declared: **v1.3** (`synthetic_panel_v1_3.csv`), **v1.2** (`synthetic_panel_v1_2.csv`) and **A17**
(`panel_A17.csv`), one `M_CONSTANCY.csv` row each, so the constant is tested on more than the panel that reports
it. None of the three is re-run or re-scored.

### 4.7 Overall register verdict (precedence as a block field, D158(6))

Tested **in this order**, on the 12 frozen cells:

1. **`UNVERIFIED`** if **any** register row fails its traceability check — the named file does not exist, the named
   column is absent, a value cannot be re-read from that path+column, or a row carries a null where a number is
   required. (Falsifier, verbatim from §1 item 5.)
2. **`REGISTER-BINDING`** if **any** frozen cell is `NOT-INTERCHANGEABLE` **or** **any** `T` crosses 1.0. The
   crossing clause is unconditional over `T`, exactly as the block writes it: a crossing in a cell with 2 pairs is
   a crossing even though the cell is `THIN` — `THIN` restricts **labels**, not **facts** (`DECLARED-OPERATIONAL`).
3. **`REGISTER-UNIFORM`** iff **all 12** frozen cells are `INTERCHANGEABLE` (hence none `THIN`, none
   `NOT-INTERCHANGEABLE`) and no `T` crosses 1.0 — the block's own parenthetical: "every system×level
   `INTERCHANGEABLE`, every wedge constant".
4. **`REGISTER-UNIFORM-PARTIAL`** — the one residual state the block's three labels do not name: no `UNVERIFIED`,
   no `NOT-INTERCHANGEABLE`, no crossing, but at least one frozen cell is `THIN`. It is declared here **before
   results** so that the label domain is total and no runner may improvise a label. It claims only what the
   record supports: *uniform on every measured cell; the `THIN` cells are unmeasured and may carry neither label,
   so the unconditional `REGISTER-UNIFORM` is unavailable.* It ranks **below** `REGISTER-BINDING` and **above**
   `REGISTER-UNIFORM` in the precedence order, and is flagged as `DECLARED-OPERATIONAL`, not a fourth claim
   about the world. If clause 1 or 2 fires, this label is not reached.

### 4.8 Systems outside the frozen list

The block names four systems (PHL, KOR, KHM, CHN). The series file also holds HKG and JPN, which carry **no UIS
completion series at all** (`DATA_NOTES_MASSIFICATION.md` §36–37: UNABLE, not a retrieval failure). They are
reported as rows with `frozen_system = FALSE`, `n_pairs = 0`, label `NO-COMPLETION-SERIES` (§4.4 gate applies:
`< 3` pairs), and they enter **no** verdict path. They are in the register because the write-up must know they
cannot carry a completion-based level sentence — but the register's `REGISTER-*` verdict is scoped to the 12 frozen
cells and says so in the same file.

### 4.9 System summary (`CONV_REG_SYSTEM.csv`)

One row per system: `n_levels_measured`, `n_levels_thin`, `min_T_over_levels`, `max_T_over_levels`,
`level_range_intersection` (`NONEMPTY` iff the intervals `[T_min_L, T_max_L]` of all measured levels share a common
point, `EMPTY` otherwise) and `spread_across_levels = max(T_max_L) − min(T_min_L)`. This is the direct arithmetic
answer to "is one constant conversion enough at this system's levels?"; it is a `DERIVED` product of register rows
and is stated as such. It makes no claim about direction or cause.

---

## 5. Register schema (fixed; columns cannot be added or dropped after freeze)

### 5.1 `results/CONV_REG.csv` — the register (one row per system × level)

| column | type | meaning |
|---|---|---|
| `system` | text | `iso3` (PHL, KOR, KHM, CHN, HKG, JPN) |
| `level` | text | `primary` / `lower_secondary` / `upper_secondary` |
| `convention_pair` | text | declared numerator/denominator, e.g. `UIS completion (pop 3-5y above grade) / GER (official age band)` |
| `n_pairs` | int | same-year pairs satisfying §4.2 |
| `n_not_comparable_years` | int | years dropped by §4.2 (declared, never silently dropped) |
| `T_min` | float 6dp | minimum `T` over paired years |
| `T_max` | float 6dp | maximum `T` |
| `range` | float 6dp | `T_max − T_min` |
| `in_band_share` | float 6dp | `n_in_band / n_pairs` |
| `n_in_band` | int | count of `T` in `[0.85, 1.15]` |
| `band_ok` | bool | `in_band_share >= 0.80` |
| `range_ok` | bool | `range <= 0.30` |
| `crossing_year` | text | first crossing year(s) `Y2`, semicolon-joined; `NONE` if none; `UNABLE` if `n_pairs < 2` |
| `crossing_interval` | text | `Y1->Y2` of the first crossing; `NONE` / `UNABLE` |
| `n_crossings` | int | count of crossings |
| `verdict` | text | `INTERCHANGEABLE` / `NOT-INTERCHANGEABLE` / `THIN` / `NO-COMPLETION-SERIES` |
| `label` | text | `DERIVED` (arithmetic product of two `OBSERVED` fields) |
| `frozen_system` | bool | TRUE for PHL/KOR/KHM/CHN; FALSE for HKG/JPN |
| `completion_column` | text | source column read (provenance) |
| `ger_column` | text | source column read (provenance) |
| `source_path` | text | programme-relative source path (provenance) |
| `traceable` | text | `TRACEABLE` or `UNTRACEABLE: <reason>` (+ `tracecheck` = the audit that re-read the value) |
| `predecl_sha256_12` | text | first 12 hex of the **enforced** predeclaration hash |

### 5.2 `results/CONV_REG_DETAIL.csv` — per-pair values with provenance

`system, level, year, completion_value, ger_value, T, in_band, source_path, completion_column, ger_column, status_completion, status_ger, label, traceable` — one row per pair. `T` at 6 dp; `completion_value`/`ger_value` as read (6 dp).

### 5.3 `results/CONV_REG_SYSTEM.csv` — §4.9, one row per system.

### 5.4 `results/M_CONSTANCY.csv` — one row per panel

`panel, panel_path, n_rows, n_tested, n_not_testable, completion_uis_column, completion_cohort_column, measurement_factor_column, declared_m, tolerance, max_abs_dev_ratio, max_abs_dev_factor, max_abs_rel_residual, verdict, label, traceable`.

### 5.5 `results/VERDICT.json`, `results/INPUT_HASHES.json`, `results/console.txt`, `results/DETERMINISM.json`

`VERDICT.json` carries: `overall_verdict`, the three-way precedence trace (which clause fired, with the cells that
fired it), `predeclaration_sha256`, `hash_enforced: true`, the per-label counts, the `m`-constancy verdicts, and
`adoption: "NONE"`. `INPUT_HASHES.json` carries the sha256 of every input file read. `console.txt` is the run log
(no clock, no absolute paths). `DETERMINISM.json` records the run1/run2 byte comparison. All four are
`DECLARED-OPERATIONAL` outputs, not register lines.

---

## 6. The seven authoring rules, verbatim (brief §7)

Copied without edit from `08_council/brief_025/SYNTHESIS_025.md` §7, lines 694–715; the decision form (D158) is in
§2.3. All seven bind this cell, and each is discharged in a named place:

| rule | discharged in |
|---|---|
| 1 hash enforced at verdict time | §8; `code/run_conv_reg.py` steps 1 and 2 |
| 2 object identity before comparison | §4.2 pair rule; `NOT-COMPARABLE` years counted, never numbered |
| 3 register before sentence | §5 schema — every row carries system, level, convention pair, source path and column |
| 4 level-symmetric legs | §4.4: each cell is one level; **no cross-level leg is claimed as a two-level test**; the cross-level question is answered only descriptively in §4.9, and §11 says so |
| 5 required-state isolation | §12: no REQUIRED-STATE object is read, computed or cited |
| 6 precedence as a block field | §4.7 tests `UNVERIFIED > REGISTER-BINDING > REGISTER-UNIFORM` in that order, in the predeclaration, not in the runner |
| 7 closed-line re-entry | §3: the cell licenses nothing; no model change, no re-fit, no re-entry |

```markdown
## 7. Authoring rules added this cycle (all binding on the next predeclaration)

1. **Hash enforcement at verdict time (from EXP-18's disclosure).** A hash cited in a verdict row must be **enforced by
   the runner at the moment the verdict is written**. A hash that was recorded but not enforced may be cited only with
   the qualifier **`RECORDED-NOT-ENFORCED`**, and no verdict may rest on it. (EXP-16's `RESULTS.csv` hash is the case:
   the file was rewritten by another process; the DETAIL and manifest were enforced.)
2. **Object identity before comparison (from EXP-18 C-2 / V33).** No two series may be compared, subtracted or placed
   against one another unless both carry the **same declared denominator/convention**. If identity is not established,
   the result is **`NOT-COMPARABLE`**, not a number. A comparison table that does not state the convention is returned.
3. **Register before sentence (from §5).** No write-up sentence may use a number whose **register line** (convention,
   window, label, source) does not exist. A sentence without a register line is `UNVERIFIED` and may not ship.
4. **Level-symmetric legs (from EXP-18 C-1).** A leg intended to test a **two-level** object must require **both**
   levels to satisfy it. A leg that can be satisfied by one level must say so in its own sentence and may not be cited
   as evidence about the object it was meant to protect.
5. **Required-state isolation (from EXP-17/EXP-19).** A `REQUIRED-STATE` may enter **no verdict path**; wherever it is
   cited it carries its `DERIVED` target and its provenance **in the same sentence**; a required state is never an
   input, a parameter, or a policy target.
6. **Precedence is a block field, not a runner choice (upgrading D147(i), which was violated in EXP-17's block).** Every
   threshold block states the order in which its labels are tested, in the block. A runner-supplied order is recorded as
   an authoring defect even when it is not verdict-bearing.
7. **Closed-line re-entry (from §3.3(ii)).** A closed line may be re-entered only by a **new measured object** plus a
   **new** Council decision; a re-specification, a re-labelled build, or a re-score is `FAIL-RE-FIT` by definition.
```

---

## 7. Banned sentences register (D158(6); brief §8, verbatim)

The brief's list, copied verbatim from `SYNTHESIS_025.md` §8, lines 736–740:

```markdown
- **Banned sentences (the list #5 carries into the write-up).** "The model reproduces the PHL level path"; "conditional
  **level** reproduction" **without** the 9/33 placement and the closed line; "the participation margin is duplicated"
  **without** the per-level split; "the repair made the model worse"; "the upper-secondary ceiling is structural"; "the
  proxy is consistent with the required coverage"; "κ ≈ 0.95 is forward-usable"; "the representation capability holds at
  both levels"; "the model is behaviourally 13–17 pp wrong"; "demand falsified"; "v1.2 passes".
```

This cell adds, for its own rows and for any downstream citation, the following barred phrasings:

1. "completion and GER measure the same thing at this level" — barred for any level whose cell is not
   `INTERCHANGEABLE`; for a `THIN` level it is barred as unmeasured.
2. "the conversion is 1.1 in the observed record" — barred: 1.1 is the **model's** declared `m` (SYNTHETIC /
   DECLARED), and the observed `T` is not assumed constant (§1 item 5).
3. "completion rose to 98.3 %" or any level sentence that does not name its object — barred by D158(3) until the
   register line for that object exists.
4. "behaviourally N pp wrong" — barred until EXP-21 records the size of the level miss as decomposable; this cell
   **does not** decompose it (§1 item 5; D153(xi)). The register measures conventions, not behaviour.
5. "the observed ratio is constant" / "the ratio is constant within the band" — barred wherever `range > 0.30` or
   `in_band_share < 0.80`; the register reports the numbers, and `INTERCHANGEABLE` is a **band** label, not
   constancy.
6. Any sentence that treats `THIN` as evidence for either side ("probably fine", "probably barred") — barred: `THIN`
   is unmeasured (§4.4).

---

## 8. Hash enforcement at verdict time (D158(1))

`code/run_conv_reg.py` shall, in this order:

1. read `PRE_DECLARATIONS.sha256`, recompute the sha256 of `PRE_DECLARATIONS.md`, and **abort (exit 2) with no
   verdict written** on mismatch — before reading any input, so no result can be produced under a drifted
   predeclaration;
2. re-verify the hash **immediately before writing `VERDICT.json`**, and write `predeclaration_sha256` plus
   `hash_enforced: true` into it;
3. stamp every register row with `predecl_sha256_12`.

A hash that appears in output but is not checked by the runner is `RECORDED-NOT-ENFORCED` and may carry no verdict.
No hash in this cell is in that state.

---

## 9. No-threshold-change rule

After this file is hashed, **no threshold, label, band, tolerance, counting denominator, crossing rule or
precedence order may change.** There is no amendment path inside this cell: a change of any of them is a **new
predeclaration** (and, per D155's sunset, not this cycle). The runner computes with the values in §0/§4 only, has
no CLI flag that alters them, and has no RNG call. If the record produces a result the predeclaration did not
foresee, the result is reported as it falls, including where that is a `THIN` cell, an `UNABLE` crossing, or a
`NOT-COMPARABLE` year — not repaired.

---

## 10. Determinism

Two runs, no clock in any output, no RNG, no environment-dependent ordering (sort keys are explicit; floats are
formatted with fixed precision):

- run 1 → `results/`;
- run 2 → `results/determinism_run2/` with the same code and inputs;
- `results/DETERMINISM.json` records the byte-for-byte comparison of the six register artifacts
  (`CONV_REG.csv`, `CONV_REG_DETAIL.csv`, `CONV_REG_SYSTEM.csv`, `M_CONSTANCY.csv`, `VERDICT.json`, `console.txt`).
  `DETERMINISM.json` itself is written only in run 1 and is excluded from the comparison.

---

## 11. Limits declared in advance

- **`THIN` levels are unmeasured, not measured-and-fine.** KOR has one observed `completion_primary` row and two
  observed `ner_upper_secondary` rows; CHN's completion series start late; upper-secondary completion exists for
  four systems only. `THIN` cells make no statement, and a level statement built on one is `UNVERIFIED`.
- **Not all systems have same-year pairs.** HKG and JPN have no UIS completion at all, so no `T` exists for them at
  any level. Their absence is a property of the record, not evidence about the objects.
- **`T` is a ratio of two differently-denominated observed series.** A `T` near 1.0 does not mean the two series
  measure the same quantity; it means the arithmetic relation is near 1.0 **at that level and year**, on the
  denominators stated in §4.1. The cell reads the relation; it does not interpret it.
- **The band test is a band test.** `INTERCHANGEABLE` = "within `[0.85, 1.15]` in ≥80 % of paired cells and range
  ≤0.30". It is not a test of statistical equivalence, not a measurement-error model, and not a licence to
  substitute one object for another in a *different* year or level.
- **One system, one record.** The register describes these six systems in this series file. It makes no claim about
  other systems, other vintages, or the world.
- **`m` is a model convention, not a measurement.** Its constancy on the panel is a property of the generator's
  arithmetic (SYNTHETIC), and says nothing about the observed relation.

---

## 12. Label discipline (D158(7))

- Observed series values → `OBSERVED`; every `T`, share, range, crossing and summary → `DERIVED` (product of two
  observed fields, with both source columns named in the same row).
- Panel values and `m` → `SYNTHETIC` / `DECLARED`; `PARAMS.md`'s `m = 1.10` → `DECLARED / CONVENTION`.
- No `REQUIRED-STATE` object appears anywhere in this cell: λ*, the required coverage (0.759712104599164 /
  0.87352319872549) and the `DERIVED` target 0.8076 are **not** inputs, not parameters, and enter no verdict path
  (D157; D158(7)). If any is ever cited downstream from this register, it carries "REQUIRED-STATE (EXP-17); not
  adopted" in the same sentence.
- Every model number that a downstream sentence cites from this cell carries its class where a class exists
  (v1.6 / v1.7 / v1.5 — D158(5)); this cell's only model objects are the completion pair `completion_uis` /
  `completion_cohort`, which is a **v1.2 convention** carried unchanged into v1.3 and v1.7 (the `m = 1.10`
  declaration is `generator_v1_2/PARAMS.md` §7), and it is labelled `SYNTHETIC / v1.2-convention` wherever cited.

---

*End of predeclaration. Frozen by hash before the runner existed; the runner's first act is to check that hash.*
