# EXP-22 PART-MARGIN-DESC — PRE_DECLARATIONS

**Cell:** EXP-22 **PART-MARGIN-DESC** (rank **#2** of the cycle-17 slate), Council brief 025, **D156 #2**.
**Question (frozen):** does the observed record contain a counterpart to the model's participation margin, and
where does the model's share sit relative to it?
**Type:** descriptive, **count-blind** cell. Reads an on-disk observed series, EXP-21's delivered register and two
delivered synthetic panels; **no model run, no re-fit, no RNG, no proxy, no adoption, no causal or direction claim.**
**Write scope:** `10_massification/extensions/part_margin_desc_2026-11-20/` only. No existing repo file is modified.

**Status of this document.** Written and hashed **before** any span, pair count, identity test or placement was
computed. The hash is `PRE_DECLARATIONS.sha256` and is **enforced by `code/run_part_margin_desc.py` as its first act
and again immediately before the verdict is written** (D158(1) / brief §7 rule 1); a mismatch aborts with no verdict.
§1, §2.1–§2.5 are copied **by line range** from the source files and are re-checked verbatim by the runner
(`verbatim_checks` in `results/VERDICT.json`) and by `code/verify_verbatim.py`. Nothing in §4 adds a threshold: §1 is
the frozen block. §4 only *operationalises* what the block already fixes, and every such clause is flagged
**`DECLARED-OPERATIONAL`** in place.

---

## 0. Machine-readable freeze fields

| field | value |
|---|---|
| cell | EXP-22 PART-MARGIN-DESC |
| authority | `08_council/brief_025/SYNTHESIS_025.md` §6.2 (verbatim in §1); `08_council/DECISIONS.md` D156 (EXP-22 clause, §2.1), D153(xii) (§2.2), D158 (§2.3); brief §8 (§2.4); `VERIFICATION_025.csv` V35a–V35c (§2.5) |
| thresholds frozen before results | yes — §1 verbatim; **no threshold may change after this file is hashed** (§9) |
| system in the frozen test | **PHL** (the block's anchors — 30 / 4 / 2 same-year pairs — are PHL's; the model's placement subject is its PHL row) |
| levels in the frozen test | `primary`, `lower_secondary`, `upper_secondary` |
| observed statistic | `span = ger_<level> − ner_<level>` (pp), same system × level × year, both `status = observed` |
| reported per level | `n_pairs`, `n_unpaired_years`, `span_min_pp`, `span_max_pp`, `span_median_pp`, year of each extreme, `thin` |
| THIN rule | `n_pairs < 3` → `THIN`; **no placement label may be carried**; the span is still reported |
| object-identity test | binding, run **against EXP-21's register, before the observed series and before the model panels are opened**; result per level `COUNTERPART-IDENTIFIED` / `NO-REGISTERED-COUNTERPART` |
| placement rule | reachable **only** if the identity test passes at a non-`THIN` level **and** the licensed observed object is in the model share's unit (a cohort fraction) |
| verdict vocabulary + precedence | **`NO-OBSERVED-COUNTERPART > PLACEMENT-OUTSIDE > PLACEMENT-INSIDE`** (tested in that order; block item 5, D158(6)) |
| count-blind | **no 33-cell and no 9-cell model score; no deviation, hit count or crossing count is computed**; enforced by three guards (§4.8) |
| falsifier | any comparison made without the identity line → **`NOT-COMPARABLE`**, no number, and the placement is **not reported** (block item 5) |
| traceability | any reported number that cannot be re-read from its path + column **aborts the run** (exit 3), so no defect state can be carried as a label (§8) |
| determinism | two runs, byte-identical (§10) |

---

## 1. The frozen block, verbatim

Copied without edit from `08_council/brief_025/SYNTHESIS_025.md`, **lines 527–562** (§6.2, seven-field block, items
1–7). Line range asserted at copy time; the runner re-asserts that the quoted text occurs verbatim in the source.

```markdown
### 6.2 EXP-22 — **PART-MARGIN-DESC**: the participation margin as a descriptive object — what in the observed record moves with it? (rank **#2**)

1. **First-order link (the failure object, described rather than modelled).** The level failure was localised to the
   **participation margin** (v1.6) and then to the **declared capacity + Tier-O margin** (v1.7). The programme has never
   described the first object in the observed record: what the gap between **gross** and **net** participation is, by
   level and year, and whether any observed object has the same numerator/denominator convention as the model's
   `demand_share`. This cell answers "low relative to what?" — the question a reader of the negative will ask.
2. **What changes if positive vs negative.** **`COUNTERPART-IDENTIFIED`** (an observed object with the same convention
   exists at ≥ 1 level-year) → the model's declared shares can be **placed** in an observed range and the write-up may
   say where they sit (`PLACEMENT-INSIDE` / `PLACEMENT-OUTSIDE`). **`NO-OBSERVED-COUNTERPART`** → the failure cannot be
   described in observed terms at all, and the write-up must say so: the model's participation object is a **choice
   share**, not an enrolment rate, and the level question cannot be settled descriptively either. Either way the
   **gross − net span** enters the record as the bound on any participation claim.
3. **Why it is not a niche.** It is the only cell that describes the object the programme blamed. Without it the
   write-up can say "the model is 10.7–17.1 pp low" (a number) but not "low relative to what" (a description), and a
   referee will ask the second.
4. **Data on disk (no DATA ASK).** `UNIVERSALIZATION_SERIES.csv` — `ger_primary` / `ner_primary` (30 same-year pairs,
   1976–2017), `ger_lower_secondary` / `ner_lower_secondary` (4 pairs, 2014–2017), `ger_upper_secondary` /
   `ner_upper_secondary` (2 pairs, 2014–2015); `panel_A17.csv` — `demand_share`, `admitted_official`, `cohort`
   (primary 2024 `admitted/cohort = 0.8960794699`); `partprov_2026-11-20/results/PARTPROV_RESULTS.csv` — P0/P1
   `mean_demand_over_cohort` and `mean_gap_pp`; `generator_v1_6_repair/PARAMS.md` for the declared `0.900000` /
   `0.820000`. Anchors (re-derived): gross − net **2.1966–14.6273 pp** primary (2017 = **5.5911**), **17.412–29.2395**
   lower, **46.0621–51.7045** upper (2 pairs, `THIN`).
5. **Threshold + falsifier (fixed before freeze).** Report the same-year `G − N` span per level (min, max, median,
   n, and the year of each extreme) and the model's declared shares beside it. **Object-identity test (binding):** the
   model's `demand_share` may be placed against an observed object **only** if the CONV-REG register (#1) records that
   object as the same convention; otherwise the cell returns `NO-OBSERVED-COUNTERPART` and reports the spans only.
   **Verdict (precedence):** `NO-OBSERVED-COUNTERPART > PLACEMENT-OUTSIDE > PLACEMENT-INSIDE`. **`THIN` rule:** a level
   with < 3 same-year pairs is reported `THIN` and may not carry a placement label. **Falsifier:** any comparison made
   without the identity line → `NOT-COMPARABLE`, and the placement is not reported. **Count-blind clause:** the cell
   computes **no** observed-path count (not 33, not 9), and reads only the named aggregates — it may not become a
   re-score of EXP-18.
6. **Closed-claim check.** Does not re-run the generator; does not re-score EXP-18 (no deviation is recomputed); does
   not reopen the localisation (it describes the object, it does not re-attribute the failure); no cause; no direction.
7. **Cost / rank.** **Small.** **Rank #2** — it depends on #1's register and it is the one cell that can change how the
   central negative is written.
```

---

## 2. Decision-form record, verbatim

### 2.1 D156 — the EXP-22 clause

From `08_council/DECISIONS.md`, the D156 row, the contiguous substring that begins at **EXP-22 PART-MARGIN-DESC**:

```markdown
**EXP-22 PART-MARGIN-DESC** — the participation margin as a descriptive object (same-year gross − net span per level; object-identity test against EXP-21's register before the model's shares may be placed; verdicts `NO-OBSERVED-COUNTERPART > PLACEMENT-OUTSIDE > PLACEMENT-INSIDE`; THIN rule <3 pairs; **count-blind clause: no 33-cell or 9-cell model score may be computed**) **#2**
```

### 2.2 D153(xii) — the observed participation margin

From `08_council/DECISIONS.md`, the D153 row, the contiguous substring `(xii)` … `;` before `(xiii)`:

```markdown
(xii) **the observed participation margin spans levels steeply** — primary −2.1966 to −14.6273 pp (30 pairs), lower −17.412 to −29.2395 (4 pairs), upper −46.0621 to −51.7045 (**2 pairs — THIN**); no single cross-level margin exists; 
```

**Sign note (record note, not a re-derivation).** D153(xii) writes the span with a leading minus (`net − gross`, the
gap read as a shortfall); the frozen block (§6.2 item 4) and `VERIFICATION_025.csv` V35a write **`ger − ner`**, which
is **positive** in every paired year. The magnitudes are identical (**2.1966–14.6273** primary, **17.412–29.2395**
lower, **46.0621–51.7045** upper). This cell reports the block's signed value (`ger − ner`, positive) and records the
notation difference in `PART_MARGIN_DESC.csv`; **no verdict rests on the sign**, and no direction claim is made.

### 2.3 D158 — the seven authoring rules

From `08_council/DECISIONS.md`, the D158 row, the contiguous text from **Seven authoring rules added** to the
rationale column:

```markdown
**Seven authoring rules added (cycle 17), all binding on the next predeclaration.** (1) **Hash enforcement at verdict time** — a hash cited in a verdict row must be enforced by the runner when the verdict is written; a recorded-but-unenforced hash may be cited only as **`RECORDED-NOT-ENFORCED`** and may carry no verdict (EXP-16's RESULTS.csv hash). (2) **Object identity before comparison** — no two series may be compared/subtracted/placed unless both carry the same declared denominator/convention; otherwise the result is **`NOT-COMPARABLE`**, not a number; a comparison table not stating the convention is returned (EXP-18 C-2 / D153(xi)). (3) **Register before sentence** — no write-up sentence may use a number whose register line (convention, window, label, source) does not exist; a sentence without a register line is `UNVERIFIED` and may not ship. (4) **Level-symmetric legs** — a leg intended to test a two-level object must require **both** levels; a leg satisfiable by one level must say so in its own sentence and may not be cited as evidence about the object it was meant to protect. (5) **Class tags** — every model number carries its class (v1.6 or v1.7 or v1.5) and every localisation sentence names the class (D153(x)). (6) **Banned sentences register** — the barred phrasings ("demand falsified", "the participation margin is duplicated" as a cell sentence, "the upper-secondary ceiling is structural", "survival loses 50.7%", "fix survival only", "A17 0/33 vs A00 9/33" without its sentence, "behaviourally N pp wrong" before EXP-21) are enumerated and a predeclaration using one is returned. (7) **Label discipline for REQUIRED-STATE/DERIVED** — any λ*, required coverage or derived target carries "REQUIRED-STATE (EXP-17); not adopted" / "DERIVED" in the same sentence as the number.
```

### 2.4 Brief §8 — banned sentences

From `08_council/brief_025/SYNTHESIS_025.md`, **lines 736–740**:

```markdown
- **Banned sentences (the list #5 carries into the write-up).** "The model reproduces the PHL level path"; "conditional
  **level** reproduction" **without** the 9/33 placement and the closed line; "the participation margin is duplicated"
  **without** the per-level split; "the repair made the model worse"; "the upper-secondary ceiling is structural"; "the
  proxy is consistent with the required coverage"; "κ ≈ 0.95 is forward-usable"; "the representation capability holds at
  both levels"; "the model is behaviourally 13–17 pp wrong"; "demand falsified"; "v1.2 passes".
```

### 2.5 VERIFICATION_025.csv — the three anchors, verbatim

`08_council/brief_025/VERIFICATION_025.csv`: rows **V35a, V35b, V35c**, quoted as CSV lines:

```csv
V35a,§3 observed,"primary ger-ner span (n pairs) and 2017 value","2.1966-14.6273 (30); 5.5911",pp,OBSERVED (arithmetic DERIVED),10_massification/data/UNIVERSALIZATION_SERIES.csv,ger_primary minus ner_primary for same-year pairs 1976-2017,Council arithmetic; min/max of the 30 same-year differences,only where both observed
V35b,§3 observed,"lower ger-ner span (n pairs)","17.412-29.2395 (4)",pp,OBSERVED (arithmetic DERIVED),10_massification/data/UNIVERSALIZATION_SERIES.csv,ger_lower_secondary minus ner_lower_secondary 2014-2017,Council arithmetic,THIN
V35c,§3 observed,"upper ger-ner span (n pairs)","46.0621-51.7045 (2)",pp,OBSERVED (arithmetic DERIVED),10_massification/data/UNIVERSALIZATION_SERIES.csv,ger_upper_secondary minus ner_upper_secondary 2014-2015,Council arithmetic,THIN; <3 pairs
```

**Record note on V35b (declared before results).** V35b's note column reads `THIN` for lower-secondary, which has
**4** same-year pairs. The frozen block's `THIN` rule is **`< 3` pairs** and D153(xii) marks **only upper** as THIN
("2 pairs — THIN"). The rule is authoritative, not the note: lower-secondary is **not** `THIN` (4 ≥ 3) and, if its
identity test had passed, it would have been eligible for a placement label. This discrepancy is reported, never
silently resolved, and it changes nothing here because no level passes the identity test (§4.5).

---

## 3. What this cell is not (closed-claim check, from the block's item 6)

- It does **not** re-run the generator, in any class (v1.5 / v1.6 / v1.7): the two `demand_share` arms are **read**
  from delivered panels as placement subjects.
- It does **not** re-score EXP-18 (not 33 cells, not 9) and recomputes **no deviation**: no model column is combined
  with an observed column anywhere in this cell (§4.8, `cross_source_arithmetic_ops = 0`).
- It does **not** reopen the level localisation and does **not** re-attribute the failure: it describes the object the
  localisation named (D153(x)); the localisation sentence itself is out of scope.
- It makes **no cause and no direction claim**: a gross−net span is a descriptive gap, not the effect of anything;
  the model's share being inside or outside a range would be a **placement**, not evidence about demand.
- It adopts **no value**, fits **nothing**, constructs **no proxy**, sets **no parameter**, and licenses **no** model
  or write-up change by itself.
- It does **not** compute a cross-level margin. The three levels are reported separately; "no single cross-level
  margin exists" (D153(xii)) is carried as a **per-level split**, and no pooled or averaged span is formed.
- It does **not** test the NER series as an object in its own right and cites **no** NER convention line from
  EXP-21 — that register states it computes no NER statistic and that no NER line may be cited from it. EXP-22's
  use of NER is licensed only by its own frozen block, and only inside `ger − ner`.
- It does not touch the running server, does not read the web, and writes nothing outside its own directory.

---

## 4. Operational specification (frozen; `DECLARED-OPERATIONAL` clauses flagged)

Every number in the results is one of three things: an **`OBSERVED`** series value as read, a **`DERIVED`** arithmetic
product of two observed values (span, median, range), or a **`SYNTHETIC`** model value read as a placement subject.
No fourth label is used.

### 4.1 Objects

| id | object | file | column(s) | label | declared numerator / denominator |
|---|---|---|---|---|---|
| O1 | PHL GER, level L | `10_massification/data/UNIVERSALIZATION_SERIES.csv` | `ger_primary`, `ger_lower_secondary`, `ger_upper_secondary` | `OBSERVED` (rows `status = observed`) | all-age enrolment ÷ the level's **official age band**, percent (file `measure` = "gross enrolment ratio"; denominator class per `DATA_NOTES_MASSIFICATION.md`) |
| O2 | PHL NER, level L | same file | `ner_primary`, `ner_lower_secondary`, `ner_upper_secondary` | `OBSERVED` (rows `status = observed`) | official-age enrolment ÷ the **same official age band**, percent (file `measure` = "net enrolment rate") |
| O3 | gross − net span | derived | — | `DERIVED` | O1 − O2, **pp of the official age band**; the numerator difference is by design (all-age vs official-age enrolment) — that is what the span measures |
| O4 | v1.6 `demand_share`, 2024 | `synthetic_2026-11-20/generator_v1_6_repair/results/panel_A10_repaired.csv` | `demand_share` (`country = SYN00_PHL_LIKE`, `year = 2024`) | `SYNTHETIC` — class **v1.6** | `p_school + p_both`: a **choice probability over the model's level cohort**, dimensionless fraction |
| O5 | v1.7 `demand_share`, 2024 | `synthetic_2026-11-20/generator_v1_7_partrepair/results/panel_A17.csv` | `demand_share` (`country = SYN00_PHL_LIKE`, `year = 2024`) | `SYNTHETIC` — class **v1.7** | the same frozen block's choice share, carried unchanged |
| O6 | EXP-21 CONV-REG register | `conv_reg_2026-11-20/results/CONV_REG.csv` (+ `VERDICT.json`, `PRE_DECLARATIONS.sha256`) | `system`, `level`, `convention_pair`, `verdict` | `DERIVED` (delivered register) | its only convention family is **completion ÷ GER**; it records **no** line for `demand_share` and **no** NER line (its own §3) |
| O7 | the model object's definition | `generator_v1_3/code/sim_v1_3.py` lines 787 and 804 (`ds = p_s + p_b`; `out["demand_share"][L, t] = ds`), read not run; restated in `generator_v1_7_partrepair/FINDINGS.md` §1 | — | `SYNTHETIC` / definition | a **choice share** in [0, 1], never an enrolment count or rate |

**Why O1 − O2 is a legitimate arithmetic and O4/O5 vs O3 is not.** O1 and O2 are both UIS participation ratios in
**percent**, on the **same declared denominator class** (the level's official age band), for the **same system, level
and year**; their difference is the share of participation that is over-age (or, if negative, under-age), in pp. O4/O5
are **fractions of the model's cohort** whose numerator is a **choice probability**, not enrolment: no observed column
carries that numerator or that denominator at any level-year, so no number may be formed between O4/O5 and O1–O3
(D158(2)). The two facts are stated together in every row.

### 4.2 Pair rule for the span — object identity before comparison (D158(2))

A pair exists for (system, level L, year Y) **iff all four hold**:

1. a `ger_<L>` row with `iso3 == "PHL"`, `year == Y`, `status == "observed"`, value finite;
2. a `ner_<L>` row with `iso3 == "PHL"`, `year == Y`, `status == "observed"`, value finite;
3. the level tags agree exactly (`ger_upper_secondary` with `ner_upper_secondary`; **never** `ger_secondary` or
   `ner_secondary`, and never a cross-level tag);
4. the year is identical on both sides — **no lag, no interpolation, no nearest-year substitution, no carry-forward.**

Otherwise the year contributes **`NOT-COMPARABLE`** and **no number**; it is counted in `n_unpaired_years` and excluded
from `n_pairs`. `derived` and `check` rows are never used (only `status == observed`).

### 4.3 Span statistic

`span_Y = value[ger_<L>](Y) − value[ner_<L>](Y)`, in **pp**, at full double precision; **no rounding before any
aggregate**; display to 6 dp.

- `span_min_pp = min(span_Y)`, `span_max_pp = max(span_Y)`, each with **the year of its first occurrence** (scan in
  ascending year order).
- `span_median_pp` = the median of the paired spans; with an even count it is the arithmetic mean of the two middle
  values (`statistics.median`), `DECLARED-OPERATIONAL`.
- No trend, slope, average-of-all-years, sign test or direction statistic is computed; the block asks for the range,
  n, and the year of each extreme.

### 4.4 `THIN` rule (the block's identification gate)

`thin = (n_pairs < 3)`. **Evaluated before any label.** A `THIN` level:

- **still reports** its span, pair count and extreme years (the block: "reported `THIN`");
- **may not carry a placement label** — not `PLACEMENT-INSIDE`, not `PLACEMENT-OUTSIDE`;
- is **unmeasured, not measured-and-fine**: neither "probably inside" nor "probably outside" may be written from it.

`THIN` is a flag, not a verdict. The overall verdict vocabulary is exactly the block's three labels (§4.7).

### 4.5 Object-identity test (binding; runs first)

Executed **against EXP-21's register, before the observed series is opened and before either model panel is opened**.
Seven steps, in this order:

1. Read `conv_reg_2026-11-20/results/CONV_REG.csv` and `VERDICT.json`; re-verify that cell's own predeclaration hash
   (from its `PRE_DECLARATIONS.sha256`) against its `PRE_DECLARATIONS.md` — **register binding** is checked before the
   register is used.
2. Read its `overall_verdict` (`REGISTER-BINDING` on delivery) and its per-level rows for **PHL**.
3. For each level L, count the register lines available at (PHL, L) → `n_register_lines_L` (0 is possible and is not
   an error).
4. Apply the **match predicate M** to every register line: a line licenses the model object **iff** its
   `convention_pair` names the model object's numerator **and** denominator — mechanically, the pair string must
   contain a numerator token in `{demand_share, demand, choice}` **and** a denominator token `cohort`, with unit a
   fraction. A line whose numerator is completion or GER, or whose denominator is an official age band or a
   "population 3–5 years above grade" population, is **not** a match.
5. `level_identity = COUNTERPART-IDENTIFIED` iff **≥ 1 matching line exists at that level** and the licensed object
   exists at **≥ 1 same-system, same-level, same-year `status = observed`** row. Otherwise
   `NO-REGISTERED-COUNTERPART`.
6. Record, per level, `n_register_lines`, `n_matching_lines`, and the register verdict read. **Silence is not a
   licence**: a register that does not name the object establishes no identity, and the block's falsifier then returns
   `NOT-COMPARABLE` for any comparison.
7. **Only after the identity result is recorded** may the observed series be opened (§4.2–4.3) and the model panels
   read (§4.10). The event order is written to `results/COUNT_BLIND_AUDIT.json` as ordinals, not timestamps.

**Overall rule.** If **any** level is `NO-REGISTERED-COUNTERPART`, the overall verdict is
`NO-OBSERVED-COUNTERPART` and clauses 2–3 of §4.7 are **not reached**. The spans are still reported: D153(xii) says
the gross − net span "enters the record as the bound on any participation claim" either way.

### 4.6 Placement rule (reachable only after a pass in §4.5)

A level is **placeable** iff (i) `level_identity = COUNTERPART-IDENTIFIED`, (ii) `thin = FALSE`, and (iii) the licensed
observed object's reported **unit equals the model share's unit** — a dimensionless fraction of a cohort in [0, 1]. Then:

- `observed_range_L = [min, max]` of the licensed observed object over its paired years (endpoints inclusive).
- **`PLACEMENT-INSIDE`** iff **both** class-tagged model shares (v1.6 and v1.7) at that level lie inside
  `observed_range_L`.
- **`PLACEMENT-OUTSIDE`** iff **any** class-tagged model share at that level lies outside it.
- **Otherwise** the placement is **`WITHHELD-NO-IDENTITY`** (or `WITHHELD-THIN`), **no** placement label is written,
  and the per-level row carries `comparison_performed = FALSE`.

**No conversion is licensed** between pp and a fraction, between a span and a share, between the model's cohort and an
observed age band, or between years. The model shares are printed **beside** the spans for the reader's orientation
only; printing is not a comparison, and the cell asserts `cross_source_arithmetic_ops = 0`.

### 4.7 Verdict (precedence as a block field, D158(6)) — tested in this order

1. **`NO-OBSERVED-COUNTERPART`** if **any** level's identity test is `NO-REGISTERED-COUNTERPART` (no observed object
   with the model's convention exists at any level-year). **This clause is tested first** and, when it fires, clauses
   2–3 are not reached.
2. **`PLACEMENT-OUTSIDE`** if the identity test passes at **≥ 1** non-`THIN` level and **any** class-tagged model
   share at that level lies outside the licensed range.
3. **`PLACEMENT-INSIDE`** if the identity test passes at **≥ 1** non-`THIN` level and **all** class-tagged model
   shares at those levels lie inside their ranges.

The order is a field of this document, not a runner choice. A `THIN` level cannot create, block or carry any of the
three labels; it is excluded from clauses 2–3 by §4.4.

### 4.8 Count-blind clause and its enforcement

**The clause.** The cell computes **no observed-path count and no model score**: not the 33-cell score, not the 9-cell
score, no deviation, no within-±5 pp hit count, no crossing count, no "n of 33 observed years" coverage count. It may
not become a re-score of EXP-18.

**Counts that are computed (exhaustive, declared before results).**

| count | value source | why it is not a model score |
|---|---|---|
| `n_pairs` per level (3 counts) | observed co-occurrence of two `status = observed` rows | required by the frozen block (§6.2 item 5) |
| `n_unpaired_years` per level (3 counts) | years in the observed union without both sides | the block's `NOT-COMPARABLE` tally; no value is formed for them |
| `n_register_lines`, `n_matching_lines` per level | EXP-21 register rows | process count of a delivered register, not a model score |
| `n_levels`, `n_register_rows` | document structure | process count |
| `n_model_share_values_read` (= 6) | three levels × two classes | placement subjects |

No other count appears in any output. Any count not in this table is a defect.

**Three enforcement layers (all active in the runner).**

- **L1 — allow-list open guard.** Every file open goes through `guarded_open()`, which permits **only** the files
  declared in §4.1 plus `PRE_DECLARATIONS.md`, `PRE_DECLARATIONS.sha256` and the runner's own three output paths. Any
  other path — in particular any EXP-18 score/decomposition artifact — raises `SystemExit(4)` **before** the file is
  opened, with no verdict written. A predicate self-test is run and recorded
  (`guard_selftest.forbidden_example_rejected = true`).
- **L2 — hash-before-data guard.** The observed series and both model panels may **not** be opened until the
  predeclaration hash has been verified **and recorded** (event 0); the identity test (§4.5) completes **before** the
  series is opened; the model panels are opened **only after** the identity result is recorded. Violations raise
  `SystemExit(4)`.
- **L3 — no cross-label arithmetic.** Observed values and `SYNTHETIC` values are accumulated in separate structures;
  the runner asserts that the set of observed columns read and the set of panel columns read are disjoint in use, that
  `cross_source_arithmetic_ops == 0`, and that `comparison_performed == FALSE`. The audit file records all three.

### 4.9 Scope: one system

The frozen test is **PHL only**. The block's anchors (30 / 4 / 2 pairs) are PHL's, and the model's placement subject is
its PHL row (`SYN00_PHL_LIKE`). Other systems carry their own `ger_*` / `ner_*` rows on disk; **this cell does not
compute them**, forms no cross-system comparison and makes no claim about them. This is a declared scope limit, not a
finding, and it may not be widened after results.

### 4.10 The model shares (placement subjects only)

Read at **2024**, all three levels, from the two delivered panels (never regenerated): v1.6 from
`generator_v1_6_repair/results/panel_A10_repaired.csv`, v1.7 from `generator_v1_7_partrepair/results/panel_A17.csv`,
column `demand_share`, row `country = SYN00_PHL_LIKE`, `year = 2024`. Expected on delivery: **v1.6 0.900000 /
0.900000 / 0.820000**; **v1.7 0.9956438554 / 0.9534771716 / 0.8003108482** (primary / lower / upper). They are
`SYNTHETIC`, they carry their **class tag** wherever printed (D158(5)), and they are **never verdict-bearing**: the
verdict is decided by §4.5 and §4.7 alone.

---

## 5. Output schemas (fixed; columns cannot be added or dropped after freeze)

### 5.1 `results/PART_MARGIN_DESC.csv` — one row per level (3 rows)

`system, level, span_convention, n_pairs, n_unpaired_years, pair_year_min, pair_year_max, span_min_pp, span_min_year,
span_max_pp, span_max_year, span_median_pp, thin, thin_rule, comparability, identity_test, identity_basis,
n_register_lines, n_matching_lines, register_verdict, model_object_convention, model_share_v1_6_2024,
model_share_v1_7_2024, model_class_tags, placement, placement_reason, comparison_performed, verdict, label_span,
label_model, ger_column, ner_column, source_path, traceable, notes, predecl_sha256_12`

### 5.2 `results/PART_MARGIN_DESC_DETAIL.csv` — one row per same-year pair (36 rows expected)

`system, level, year, ger_value, ner_value, span_pp, unit_ger, unit_ner, status_ger, status_ner, source_ger,
source_ner, source_path, ger_column, ner_column, label, traceable, predecl_sha256_12`

### 5.3 `results/OBJECT_IDENTITY_AUDIT.csv` — every candidate object, model object and span, with its convention

`level, object_id, object_kind, numerator, denominator_or_denominator_class, unit, source_path, column,
register_line_present, same_convention_as_model, model_share_comparable, reason, label`

### 5.4 `results/VERDICT.json`, `results/COUNT_BLIND_AUDIT.json`, `results/INPUT_HASHES.json`,
`results/console.txt`, `results/DETERMINISM.json`

`VERDICT.json` carries `overall_verdict`, the three-clause precedence trace with the evidence that fired or did not,
the per-level identity result, `predeclaration_sha256`, `hash_enforced: true`, `verbatim_checks`,
`adoption: "NONE"`, and the guard flags. `COUNT_BLIND_AUDIT.json` carries the event order, the allow-list, the files
opened, the exhaustive count table of §4.8 and the three guard results. `console.txt` is the run log (**no clock, no
absolute paths**). All are `DECLARED-OPERATIONAL` outputs, not register lines.

---

## 6. The seven authoring rules — discharge table (brief §7 / D158)

| rule | discharged in |
|---|---|
| 1 hash enforced at verdict time | §8; runner steps 1 and 8 (pre-input and pre-verdict-write) |
| 2 object identity before comparison | §4.2 (span pair rule), §4.5 (identity test first), §4.6 (placeability), §4.9 (scope) |
| 3 register before sentence | §5.1 — every row carries system, level, convention, source path and column, label, enforced hash |
| 4 level-symmetric legs | §4.4/§4.7: no cross-level leg is claimed as a two-level test; the three levels are reported separately and no pooled margin is formed (§3) |
| 5 class tags | §4.10 and every model column; `model_class_tags = "v1.6; v1.7"` in every row |
| 6 banned sentences register | §2.4 (brief §8 verbatim) + §7 (this cell's additions) |
| 7 required-state isolation | §12: no `REQUIRED-STATE` object is read, computed or cited |

---

## 7. Banned sentences register (D158(6)) — this cell's additions

In addition to brief §8 (§2.4), the following are **barred** in this cell and in any downstream citation of it:

1. **"the model's participation share is too low (0.900 vs 0.996)"** — the sentence this cell exists to retire: it
   compares two **model classes** to each other and implies an observed benchmark. Barred.
2. **"the model's participation margin is 0.900 vs the observed 2.2–14.6 pp"** or any sentence that sets a model
   fraction against an observed pp span — barred: different numerator, denominator and unit, **`NOT-COMPARABLE`**.
3. **"the model's share is inside / outside the observed participation range"** — barred: the identity test does not
   license any observed range for the model object (§4.5), so there is no range to be inside or outside of.
4. **"the observed participation margin is 2.2–14.6 pp at primary"** written without naming the level, the system, the
   years and both source columns — barred by D158(3); the span is a per-level, per-system derived value.
5. **"the participation margin is duplicated"** (brief §8) — barred without the per-level split; this cell supplies
   the split, not a licence for the unqualified sentence.
6. **"gross and net enrolment measure the same thing"**, **"the span is over-age enrolment"** as a measured quantity,
   or any sentence turning the span into a **count** of pupils — barred: GER and NER are explicitly not
   interchangeable (`DATA_NOTES_MASSIFICATION.md`, definition trap 2), the span is a descriptive gap, and this cell is
   count-blind.
7. **"the model is behaviourally N pp wrong"**, any paraphrase, and any word of **cause** or **direction** — barred
   (brief §8; D153(xi)); this cell measures conventions and spans, not behaviour.
8. **"THIN means the upper-secondary margin is probably in/outside"** — barred: `THIN` is unmeasured (§4.4).

---

## 8. Hash enforcement and traceability at verdict time (D158(1))

`code/run_part_margin_desc.py` shall, in this order:

1. read `PRE_DECLARATIONS.sha256`, recompute the sha256 of `PRE_DECLARATIONS.md`, and **abort (exit 2) with no verdict
   written** on mismatch — **before** any data file is opened;
2. record the verified hash in the run state (`hash_recorded` = event 0) — this is what "before the hash is recorded"
   in the block's count-blind clause refers to;
3. run the **verbatim checks** (§1, §2.1–§2.5) and abort (exit 2) if a quoted passage does not occur verbatim in its
   source;
4. run the identity test (§4.5) **before** opening the observed series;
5. compute the spans (§4.2–4.3) and the per-level rows;
6. open the model panels only after the identity result is recorded, and read the six placement values;
7. **re-verify every reported number by re-reading it from its path + column** (a fresh pass); any mismatch aborts
   (exit 3) with no verdict — traceability is an abort condition, never a label;
8. re-verify the predeclaration hash **immediately before writing `VERDICT.json`**, and stamp every row with
   `predecl_sha256_12`.

A hash that appears in output but is not checked by the runner is `RECORDED-NOT-ENFORCED` and may carry no verdict. No
hash in this cell is in that state. The register's own hash is checked in step 4.1 before the register is used, so no
register line here is `RECORDED-NOT-ENFORCED` either.

---

## 9. No-threshold-change rule

After this file is hashed, **no threshold, label, thin rule, span definition, pairing rule, identity predicate,
placement rule, verdict order, scope or count table may change.** There is no amendment path inside this cell: a change
of any of them is a **new predeclaration** (and, per D155's sunset, not this cycle). The runner has no CLI flag that
alters them and no RNG call. If the record produces a result the predeclaration did not foresee — a `NOT-COMPARABLE`
level, a `THIN` level, an identity result that differs by level — it is reported as it falls, not repaired.

---

## 10. Determinism

Two runs, no clock in any output, no RNG, explicit sort keys, fixed-precision formatting:

- run 1 → `results/`;
- run 2 → `results/determinism_run2/`, same code, same inputs;
- `results/DETERMINISM.json` records the byte-for-byte comparison of **six** artifacts
  (`PART_MARGIN_DESC.csv`, `PART_MARGIN_DESC_DETAIL.csv`, `OBJECT_IDENTITY_AUDIT.csv`, `VERDICT.json`,
  `COUNT_BLIND_AUDIT.json`, `console.txt`). `DETERMINISM.json` itself is written only in run 1 and is excluded from
  the comparison.

---

## 11. Limits declared in advance

- **Upper secondary is `THIN` (2 pairs, 2014–2015).** Its span (46.06–51.70 pp) is reported and is **unmeasured as a
  range**: two pairs cannot support a range statement, and no placement label is available at that level even if the
  identity test had passed. This is the level where the observed gap is largest, so the thinness bites exactly where
  the description would be most interesting.
- **Lower secondary has 4 pairs (2014–2017).** Above the 3-pair gate, but the window is four adjacent years in one
  system; no trend and no "typical" value may be read from it.
- **Primary has 30 pairs (1976–2017) and no pair after 2017**, because the PHL primary NER series ends in 2017. The
  model shares are at **2024**, so even a licensed range would be a **historical** range, not a same-year one: there is
  **no observed same-year span at 2024** at any level. This is a second, independent reason the placement is a
  historical comparison at best, and it is declared before results.
- **GER and NER are different objects by design** (gross vs net; `DATA_NOTES_MASSIFICATION.md` trap 2). The span is a
  descriptive gap and **not** a measured over-age enrolment count; the two inputs also come from different source
  campaigns (`WDI_UIS_derived` for `ger_*`, `UIS_EDUNONCORE_2020_02` for `ner_*`), so a span is a difference of two
  delivered series, not a reconciled measurement.
- **The model object is a choice probability, not an enrolment rate.** No observed object on disk carries its
  numerator (a demand/choice share) over its denominator (the model's level cohort). That is the identity finding, and
  it is a statement about **the record**, not about the world: it does not say demand is unmeasurable, only that no
  licensed observed counterpart is on this disk.
- **One system, one series, one window.** The cell describes PHL in `UNIVERSALIZATION_SERIES.csv`; it makes no claim
  about other systems, other vintages, other years, or the world.
- **No causal or direction claim.** The span's sign is not evidence of a mechanism, and a placement (were one
  licensed) would not be evidence about demand, capacity or policy.
- **The model numbers are placement subjects only.** v1.6 and v1.7 differ from each other by more than either differs
  from any observed object on this disk — but **no statement comparing the two classes is a result of this cell**; the
  classes are tagged so that a reader cannot mistake which number is which.

---

## 12. Label discipline (D158(7))

- Observed series values → `OBSERVED`; every span, median, extreme year and range → `DERIVED`; model values →
  `SYNTHETIC` with class tag `v1.6` / `v1.7`; convention statements → `DECLARED`.
- No `REQUIRED-STATE` object appears anywhere in this cell: λ*, the required coverage (0.759712104599164 /
  0.87352319872549) and the `DERIVED` target 0.8076 are **not** read, not inputs, not parameters, and enter no verdict
  path (D157; D158(7)). If any is cited downstream, it carries "REQUIRED-STATE (EXP-17); not adopted" in the same
  sentence.
- The `demand_share` numbers are `SYNTHETIC` **and** are not evidence about behaviour: they are the model's declared
  choice share, read from a delivered panel, never regenerated.

---

*End of predeclaration. Frozen by hash before the runner existed; the runner's first act is to check that hash.*
