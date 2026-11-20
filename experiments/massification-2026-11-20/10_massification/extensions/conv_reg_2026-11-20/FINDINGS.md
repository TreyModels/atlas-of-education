# EXP-21 CONV-REG — FINDINGS

**Cell:** EXP-21 CONV-REG (Council brief 025, D156 #1), descriptive register.
**Predeclaration:** `PRE_DECLARATIONS.md`, sha256 `1dd86bd139a81c22e0ba2918728818fe7184775d925211a28fdd2be00b975410`
— enforced by the runner twice (pre-input and immediately before the verdict was written), stamped on every
register row, recorded in `results/VERDICT.json` and `results/console.txt`.
**Run:** one run, `code/run_conv_reg.py`, no RNG, no clock, no model run, no network, no write outside this
directory. Two runs are byte-identical (`results/DETERMINISM.json`, 6/6 artifacts).
**Adoption:** none. This cell reads the record and writes a register. It licenses no parameter, no target, no
model change, no re-fit, and no causal or direction claim.

---

## 1. The answer in one paragraph

**`REGISTER-BINDING`.** Of the 12 frozen system × level cells, **6 are `NOT-INTERCHANGEABLE`, 4 are
`INTERCHANGEABLE`, and 2 are `THIN`**; **none** is untraceable. The observed conversion `T = completion / GER` is
**not a constant and not a near-constant**: its per-level range runs from 0.0838 (KOR lower) to 0.8026 (KHM upper),
it crosses 1.0 in **6 of the 12** cells (including **all 4** of the cells that pass the band test), and at CHN the
per-level `T` intervals do not even share a common point. One constant conversion is therefore **not enough**: the
model's single declared `m = 1.10` can only be a **point convention on a synthetic panel**, never a level
convention for the observed record. The cell's own model-side test says the same thing in a second way — the
`completion_uis / completion_cohort` identity holds at 1e-9 on the A17 panel (max deviation
**8.8395202269e-10**, reproducing V34) but **fails** on the v1.3 and v1.2 panels (max deviation
**4.7043695535e-02**) because those two panels cap the UIS-convention rate at 1.0 in **35 of 6,720** cells.

---

## 2. The register, read out

Source for every row: `results/CONV_REG.csv` (register) and `results/CONV_REG_DETAIL.csv` (per-pair, with file +
column). `T_min`/`T_max` years in brackets are the `year` column of the DETAIL rows carrying those values. All
register values are `DERIVED` from two `OBSERVED` fields of
`10_massification/data/UNIVERSALIZATION_SERIES.csv`, read as `value` where `indicator = <object>` and
`status = observed`.

### 2.1 PHL (the anchor system)

| level | pairs | `T_min` [year] | `T_max` [year] | range | in-band | crossing 1.0 | verdict |
|---|---:|---|---|---:|---:|---|---|
| primary | 9 | 0.802546 [2000] | 1.073853 [2021] | 0.271307 | **0.555556** (5/9) | **2021** (2017→2021) | `NOT-INTERCHANGEABLE` |
| lower_secondary | 4 | 0.746209 [2004] | 0.900968 [2017] | 0.154759 | **0.250000** (1/4) | none | `NOT-INTERCHANGEABLE` |
| upper_secondary | 6 | 0.898892 [2004] | 1.093971 [2017] | 0.195080 | **1.000000** (6/6) | **2017** (2010→2017) | `INTERCHANGEABLE` |

Three things to read off this table.

1. **Primary fails on the in-band share, not on the range.** Its T runs 0.803 → 1.074: four of nine paired years
   are outside `[0.85, 1.15]`, and the level **crosses parity in 2021**, exactly where D153(xi) says it does
   (0.925039 in 2017 → 1.073853 in 2021). The 1999, 2017, 2021 and 2024 anchors of V33 reproduce to the last
   digit in the DETAIL rows (0.802590 / 0.925039 / 1.073853 / 1.045426); `T_min` is a *different* year (2000,
   0.802546), because the register takes the minimum over all nine pairs, not over the four anchor years.
2. **Lower secondary is measured on only four pairs** — 1999, 2004, 2008, 2017 — because `ger_lower_secondary`
   stops at 2018 while `completion_lower_secondary` runs to 2024. Three of the four T values are below 0.85, hence
   `NOT-INTERCHANGEABLE`; but the four-pair base is thin in practice even though it clears the declared gate
   (4 ≥ 3). **The 2024 lower-secondary completion value (92.413963) has no same-year GER on disk and therefore no
   register line at all.**
3. **Upper secondary passes the band test and still crosses 1.0.** Every one of its six pairs is inside the band
   (T 0.899–1.094), so the cell is `INTERCHANGEABLE`; but T rises from 0.905307 (2010) to 1.093971 (2017) and
   crosses parity there. That is the cleanest illustration in the cell of the difference between a **band** label
   and a **constant**: an interchangeable cell is not a constant cell.

**PHL system line:** `min_T 0.746209`, `max_T 1.093971`, `spread_across_levels 0.347762`, per-level intervals
intersect at `[0.898892, 0.900968]` (`NONEMPTY`). The overlap is a 0.0021-wide arithmetic point inside three very
wide per-level ranges; the frozen test is the **band test**, which primary (56 %) and lower (25 %) fail. The
intersection is reported descriptively and rescues no constant.

### 2.2 The other three frozen systems

| system | level | pairs | `T_min` | `T_max` | range | in-band | crossing 1.0 | verdict |
|---|---|---:|---:|---:|---:|---:|---|---|
| KOR | primary | 1 | 0.988654 | 0.988654 | 0.000000 | 1.000000 | `UNABLE` | `THIN` |
| KOR | lower_secondary | 16 | 0.952004 | 1.035805 | 0.083801 | 1.000000 | 2010; 2017 | `INTERCHANGEABLE` |
| KOR | upper_secondary | 19 | 0.903371 | 1.079097 | 0.175726 | 1.000000 | 2006; 2007; 2008; 2009; 2016 | `INTERCHANGEABLE` |
| KHM | primary | 14 | 0.334070 | 0.790452 | 0.456382 | 0.000000 | none | `NOT-INTERCHANGEABLE` |
| KHM | lower_secondary | 6 | 0.525134 | 0.770959 | 0.245824 | 0.000000 | none | `NOT-INTERCHANGEABLE` |
| KHM | upper_secondary | 3 | 0.370991 | 1.173614 | 0.802623 | 0.000000 | 2001; 2008 | `NOT-INTERCHANGEABLE` |
| CHN | primary | 6 | 0.904041 | 1.004089 | 0.100048 | 1.000000 | 2014; 2016; 2020 | `INTERCHANGEABLE` |
| CHN | lower_secondary | 1 | 0.846909 | 0.846909 | 0.000000 | 0.000000 | `UNABLE` | `THIN` |
| CHN | upper_secondary | 5 | 0.572200 | 0.946374 | 0.374174 | 0.200000 | none | `NOT-INTERCHANGEABLE` |

- **KOR** is the one system where two levels pass cleanly (lower 100 % in band over 16 pairs; upper 100 % over 19),
  and both still cross 1.0 (upper five times). KOR primary is `THIN`: exactly **one** observed
  `completion_primary` row exists on disk (2012), so **no KOR primary conversion statement of any kind can be
  made** — neither "interchangeable" nor "barred".
- **KHM never passes**, at any level, and not narrowly: primary T sits in 0.334070–0.790452, upper T swings 0.370991–1.173614.
  This is the clearest case where completion and GER are **not two readings of one scale**.
- **CHN** passes at primary with a 0.100 range but **crosses 1.0 three times** (2014, 2016, 2020), i.e. its T
  oscillates 0.904–1.004; CHN lower is `THIN` (1 pair) because `ger_lower_secondary` stops in 2010 while completion
  starts in 2010; CHN upper fails badly (0.572–0.946, 20 % in band) and its per-level interval is what makes the
  CHN system intersection **`EMPTY`** — no single T value is simultaneously admissible at CHN's three levels.

**Systems outside the frozen list (reported, no verdict path).** HKG and JPN have **no UIS completion series at
all** (`DATA_NOTES_MASSIFICATION.md` §36–37: UNABLE, not a retrieval failure), so all six of their cells are
`NO-COMPLETION-SERIES` with `n_pairs = 0`. They cannot carry a completion-based level sentence, and this register
says so rather than leaving a blank.

---

## 3. Which objects may carry which level statement

Read this as the register's licence table. "May carry" means: **this object may appear in a level sentence, with
this level and this system named in the same sentence.** It never means the object may be substituted for the other.

| level | systems where completion/GER **may** be treated as one scale | systems where they **may not** | systems **unmeasured** |
|---|---|---|---|
| primary | CHN (6/6 in band, parity crossed 2014/2016/2020) | PHL (5/9 in band), KHM (0/14) | KOR (1 pair) |
| lower_secondary | KOR (16/16 in band) | PHL (1/4 in band), KHM (0/6) | CHN (1 pair) |
| upper_secondary | PHL (6/6 in band, parity crossed 2017), KOR (19/19 in band, five crossings) | KHM (0/3 in band), CHN (1/5) | — |

Consequences, stated at the level of the object rather than the sentence:

1. **`completion` and `GER` are not one object at PHL primary and lower, at any KHM level, or at CHN upper** — in
   those cells the ratio is outside the declared band in a majority of paired cells, and the direction of the
   deviation is **level-specific**: at KHM completion sits *below* GER (T ≈ 0.33–0.79), at PHL primary it moves from *below*
   (0.80) to *above* (1.07). A single "completion is GER-ish" statement is false at one or the other end of the
   record.
2. **`NER` is not tested here and may not be substituted.** The register computes no NER statistic (predeclared,
   §3 of the predeclaration). Any sentence that treats NER as a stand-in for GER, or for completion, has no
   register line from this cell.
3. **`completion_uis / completion_cohort` is a synthetic object.** It is exactly `1.10 ×` its cohort-flow
   counterpart on A17 and **not** on v1.3/v1.2 (see §4). It may not be compared with observed `T` in either
   direction: the model ratio is a declared identity, the observed ratio is a measured relation between two
   differently-denominated series.
4. **The three write-up headline numbers are completion objects only.** 98.304619 (PHL primary 2024), 92.413963 (PHL
   lower 2024) and 75.025253 (PHL upper 2024) are `completion_*` values; two of the three (lower, upper) have **no
   same-year GER on disk** (both GER series end 2018), so those two cannot be converted, compared to GER, or
   compared to the model's `completion_uis` on any register line this cell can produce.

---

## 4. Is one constant conversion enough? No — three independent ways

1. **The band test fails in 6 of 12 cells**, and fails *hard* where it fails (KHM primary 0.334–0.790; CHN upper
   0.572–0.946; PHL primary 56 % in band). A single `m` applied at all levels would be wrong by up to
   **|1.10 − 0.334| ≈ 0.77** at KHM primary — larger than the whole `[0.85, 1.15]` band is wide.
2. **All four cells that pass the band test cross 1.0.** A constant cannot represent a relation that passes
   through 1.0 and keeps going: PHL upper goes 0.905 → 1.094 between 2010 and 2017, KOR upper crosses parity five
   times, CHN primary three times. "In band" and "constant" are different properties, and the record separates
   them cleanly.
3. **The per-level levels are not one number.** `spread_across_levels` is 0.347762 (PHL), 0.175726 (KOR),
   **0.839544** (KHM), 0.431889 (CHN), and CHN's per-level intervals are **disjoint**. There is no system in which
   one constant is admissible at all three levels *and* stable within each level.

**And the model's own constant is not unconditional either.** The `m`-constancy test at 1e-9 on the three panels:

| panel | rows | `completion_uis / completion_cohort` max deviation from 1.10 | `measurement_factor` max deviation | verdict |
|---|---:|---|---:|---|
| A17 (v1.7) | 6,720 | **8.8395202269e-10** | 0.0000000000e+00 | `CONSTANT` |
| v1.3 | 6,720 | **4.7043695535e-02** | 0.0000000000e+00 | `NOT-CONSTANT` |
| v1.2 | 6,720 | **4.7043695535e-02** | 0.0000000000e+00 | `NOT-CONSTANT` |

The A17 result reproduces V34 exactly. The v1.2/v1.3 failure has a single mechanical cause, traceable in the
panels' own columns: **35 of 6,720 cells in each of those two panels carry `completion_uis = 1.0` exactly, and in
every one of the 35 `1.10 × completion_cohort > 1.0`** — i.e. the UIS-convention rate is **capped at 1.0** in those
panels (affected: `SYN00_PHL_LIKE`, `SYN07`, `SYN10_BOOM`, `SYN19`, `SYN23`, all at `primary`, cohort
0.9093260974–0.9497070256, years 2012–2025). The A17 panel has **no** cell with
`1.10 × completion_cohort > 1.0`, so the cap never binds there and the identity is exact. **The constant `m` is
exact only where its ceiling does not bind** — on the panels where the ceiling binds, the ratio is not 1.10 at all.
That is a statement about the panels' arithmetic (`SYNTHETIC`), not about the world, and it is not a re-score of
any generator.

**Verdict on the question as asked: `REGISTER-BINDING`. One constant conversion is not enough.** A binding
per-system × level register is issued (§3), and `m = 1.10` is recorded as a **point convention on a synthetic
panel — not a level convention** (the block's own required reading, item 2).

---

## 5. What this means for every level sentence in the write-up

Rule (D158(3), register before sentence): a level sentence may use a number **only** if its register row exists and
is cited. The citation form this register imposes is:

```
[object: completion_primary | system PHL | year 2024 | value 98.304619 (OBSERVED) |
 register row CONV_REG.csv PHL/primary | conversion label NOT-INTERCHANGEABLE | DERIVED]
```

Applied sentence by sentence:

| sentence the write-up might carry | what the register allows | why |
|---|---|---|
| "primary completion rose to 98.3 %" | **only** as `completion_primary, PHL, 2024`; the word "completion" alone is barred | the row exists (`PHL/primary`) but is `NOT-INTERCHANGEABLE`; the object must be named, and "rose" carries no direction licence from this cell |
| "the model is 13.4 pp low at primary" | **barred** | it compares `completion_uis` (SYNTHETIC, m = 1.10 point convention) with observed completion across a `NOT-INTERCHANGEABLE` cell; "behaviourally N pp wrong" is on the banned list until the miss is decomposable, and this cell does **not** decompose it |
| "completion/GER ≈ 1.05, so the two measures agree" | **barred** | the ratio is 0.803–1.074 at PHL primary across the record and crosses 1.0 in 2021; a single ratio is a point, not a relation |
| "lower-secondary completion 92.41 (2024)" | **only** as a completion value with its year; **no** ratio, no GER comparison | `ger_lower_secondary` ends 2018; there is no same-year pair for 2024 |
| "upper-secondary completion 75.03 (2024)" | same as above | `ger_upper_secondary` ends 2018 |
| "completion exceeded GER at upper secondary" | **allowed** with system + year: PHL upper, 2017 (T = 1.093971) | `PHL/upper_secondary` is `INTERCHANGEABLE` and the crossing year 2017 is in the register |
| any cross-system "completion is at X %" table | **must carry** the per-system × level row and the `NOT-INTERCHANGEABLE`/`THIN` label | 6/12 cells are barred, 2/12 are unmeasured |
| any KOR primary statement | **barred** (unmeasured) | 1 pair; `THIN` may carry neither label |
| any KHM level statement built on the completion/GER relation | **barred** | 0 % in band at all three levels |

Two further consequences for the write-up, both structural:

1. **No sentence may present `m` as a property of the observed record.** 1.10 is `DECLARED / CONVENTION` from
   `generator_v1_2/PARAMS.md` §7, and its exactness is a fact about the A17 panel. Any sentence of the form "the
   model's measurement factor matches the observed ratio" is barred: the observed ratio is not constant and the
   model factor is capped where the ceiling binds.
2. **The level sentence and the model sentence cannot be fused.** The write-up's level numbers are `OBSERVED`
   completion; the model's level numbers are `SYNTHETIC` `completion_uis` under a point convention. Where the
   register says `NOT-INTERCHANGEABLE`, fusing them is a convention error, not a rounding error.

---

## 6. What this means for EXP-22 (PART-MARGIN-DESC)

- **EXP-22's object-identity test cannot be inherited from this register.** This cell tests `completion/GER` only;
  it computes **no** statistic on `demand_share`, `ger − ner`, or any gross/net pair. EXP-22 must run its own
  identity test on its own declared pair and may not write "EXP-21 says the objects are the same" for
  `demand_share`. The honest statement it can carry is narrower: **the register records that no observed object in
  this cell shares the model's `demand_share` convention**, because `demand_share` is a choice share over a
  four-state block and nothing in `UNIVERSALIZATION_SERIES.csv` is denominated that way.
- **EXP-22's `G − N` span is a different pair and must say so.** `ger_*` and `ner_*` share the level age band but
  differ in numerator (gross vs net); that is a *different* convention question from `completion/GER` (which
  differs in **denominator**). The register's level split is still usable as context — the convention wedge is
  level-specific at every system measured — but EXP-22 may not cite EXP-21 as evidence about participation.
- **The one thing EXP-22 may take as given:** a level statement must name its object, and the level asymmetry the
  register measures (KHM 0.334–0.790 at primary vs PHL upper 0.899–1.094) is a convention asymmetry, not a
  participation finding.

## 7. What this means for EXP-25 (V-SPINE)

- **The object field of every level sentence is this register's row.** EXP-25 must attach
  `system × level × object × conversion label` to each level claim in the spine, and the label set is exactly
  `INTERCHANGEABLE` (4 cells), `NOT-INTERCHANGEABLE` (6), `THIN` (2), `NO-COMPLETION-SERIES` (HKG/JPN).
- **The "conditional level reproduction" headline cannot be repaired by adding a conversion caveat.** With
  `REGISTER-BINDING`, the spine needs a per-cell object statement; a single global footnote saying "conventions
  differ" is not a register line and is `UNVERIFIED` under D158(3).
- **The constant-`m` sentence must be written as a point convention**, per the block's item 2: *the constant-`m`
  convention is recorded as a point convention, not a level one*. EXP-25 should also carry the ceiling fact
  (§4 above): the identity is exact on A17 and capped in 35/6,720 cells of v1.2/v1.3.
- **Two cells are unmeasured, not clean.** `KOR/primary` and `CHN/lower_secondary` are `THIN`; a spine sentence
  that silently omits them reads as if they passed. They must be shown as unmeasured, or the spine's level table is
  incomplete.

---

## 8. Honest limits

1. **`THIN` is unmeasured, not measured-and-fine.** Two of twelve frozen cells (`KOR/primary`, `CHN/lower_secondary`)
   rest on exactly one same-year pair. They receive neither label and support no sentence in either direction.
   PHL lower secondary clears the gate with **four** pairs — legal under the frozen `< 3` rule, but thin in
   substance, and its 2024 completion values have no GER counterpart at all.
2. **Not all systems have same-year pairs, and the absences are systematic.** HKG and JPN have no UIS completion
   series (6 cells, `NO-COMPLETION-SERIES`). `ger_lower_secondary` ends in 2018 (PHL, KOR) or 2019 (KHM) and
   `ger_upper_secondary` in 2018 (PHL, KOR) or 2008 (KHM), while completion runs to 2024 — so the **most recent** completion values, including
   two of the write-up's three headline numbers, are structurally unpaired. `n_not_comparable_years` in
   `CONV_REG.csv` counts every year with only one side (43 at PHL primary, 44 at CHN primary); most of those are
   pre-1999 GER-only years and post-2018 completion-only years, not data errors.
3. **`T` is a ratio of two differently-denominated series.** UIS completion is measured on the population 3–5 years
   **above** the official graduation age; GER uses the level's **official age band**
   (`DATA_NOTES_MASSIFICATION.md`, "Definition trap"). A T near 1.0 is an arithmetic coincidence of those two
   denominators at that year — not evidence that the objects measure the same quantity, and not a correction of
   either series. This cell does not "adjust" completion or GER, and no number here may be used to do so.
4. **The band test is a band test, not an equivalence test.** `INTERCHANGEABLE` = in `[0.85, 1.15]` in ≥ 80 % of
   paired cells **and** range ≤ 0.30. No measurement-error model, no significance test, no inference beyond these
   six systems in this one series file.
5. **The crossing rule is descriptive.** Crossings are consecutive-pair sign changes over **observed** paired years
   only, so they locate parity between two observed years (PHL primary between 2017 and 2021; PHL upper between
   2010 and 2017), not in a specific unobserved year. Where T oscillates (KOR upper five times, CHN primary three
   times) the "crossing year" is not a stable object and must not be cited as one.
6. **The level table is not a cross-level test.** Each cell is one level. The cross-level summary (§2.1, §4.3) is
   descriptive arithmetic over register rows; per D158(4) this cell makes **no** claim to have tested a two-level
   object, and no leg here may be cited as one.
7. **`m` is not a measurement.** Its constancy is a property of the generator's arithmetic on a synthetic panel; it
   says nothing about the observed relation and licenses no re-scaling of observed completion.
8. **No causal or direction claim.** Nothing here says completion *causes*, *leads*, *tracks* or *predicts* GER, or
   that any level is converging, diverging, improving or deteriorating. The register reports ratios and their
   bands at named years; the words "rise", "fall", "cross" are used only as descriptions of the arithmetic
   sequence, never as a trend claim.
9. **No adoption, no re-fit, no model run.** No parameter, target, threshold or model is changed by this cell. No
   generator was executed. `m` was read from `PARAMS.md`, not set.

---

## 9. Falsifier and self-audit (all pass)

| check | result |
|---|---|
| any register line untraceable to a named file + column → `UNVERIFIED` | **0 untraceable**: 18 register rows, 90 detail rows and 3 panel rows re-read from the named path + indicator/column; `traceable = TRACEABLE` on every row (audit transcript in `results/console.txt`); `VERDICT.json` clause 1 `fired: false` |
| predeclaration hash enforced at verdict time (D158(1)) | **enforced twice** by the runner (pre-input, pre-verdict-write), mismatch aborts with exit 2 and writes no verdict; hash `1dd86bd1…` stamped on every register row |
| thresholds frozen before results, no re-fit | yes — §1 of the predeclaration is the block verbatim; no threshold, band, tolerance or precedence order changed after the hash; no CLI flag can change them |
| determinism | two runs, **6/6 artifacts byte-identical** (`results/DETERMINISM.json`) |
| label discipline (D158(5), D158(7)) | every row carries `OBSERVED` / `DERIVED` / `SYNTHETIC` / `DECLARED` in its `label` column; no `REQUIRED-STATE` object (λ*, required coverage, 0.8076) is read, computed or cited anywhere in this cell |
| write scope | all writes under `10_massification/extensions/conv_reg_2026-11-20/`; no existing repo file modified; no web; no server touched |

**Numbers in this document and where they come from** (D113a): every register value above is a column of
`results/CONV_REG.csv` or `results/CONV_REG_SYSTEM.csv`; every per-pair value and every `[year]` is a row of
`results/CONV_REG_DETAIL.csv` (`year`, `T`, `completion_value`, `ger_value`, with `source_path`,
`completion_column`, `ger_column` in the same row); every `m` figure is a column of `results/M_CONSTANCY.csv`
(`panel_path`, `completion_uis_column`, `completion_cohort_column`); the 35-cell cap count is reproducible from
`completion_uis == 1.0 and 1.10 × completion_cohort > 1.0` in those same panel columns, printed in
`results/console.txt`. The three headline completion values (98.304619 / 92.413963 / 75.025253) are the
`value` column of `UNIVERSALIZATION_SERIES.csv` at `indicator = completion_primary / completion_lower_secondary /
completion_upper_secondary`, `iso3 = PHL`, `year = 2024`, `status = observed`; they are quoted as completion
values only, and the lower/upper ones have no same-year GER on disk.

**One sentence, if only one is kept:** *completion and GER are one scale in 4 of 12 frozen system × level cells and
no scale at all in the other 8 (6 barred, 2 unmeasured), and even the 4 interchangeable cells cross parity — so the
write-up must name its object per level, and the model's single `m = 1.10` is a point convention on a synthetic
panel, not a level convention (`REGISTER-BINDING`).*
