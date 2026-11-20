# FINDINGS — EXP-22 **PART-MARGIN-DESC**: the participation margin as a descriptive object

**`LABEL: OBSERVED` for the enrolment series values; `LABEL: DERIVED` for every span, median and range (a product of
two observed values); `LABEL: SYNTHETIC` for every model number, with its class tag (v1.6 / v1.7); `LABEL: DECLARED`
for convention statements. No causal or direction claim is made anywhere. No value is adopted.**
**Cell:** EXP-22 PART-MARGIN-DESC, Council brief 025, D156 #2 (rank #2). **Verdict: `NO-OBSERVED-COUNTERPART`.**
**Predeclaration:** `PRE_DECLARATIONS.md`, sha256 `8f47aa216395b6c0da1eb78e696ed80796a077c72780ac4211d2143ddda439bd`,
enforced by the runner before any input is read and again before the verdict is written.

---

## 1. The answer, in one paragraph

The observed record **does** contain a participation margin, and it is **steeper across levels than any single number
can carry**: a same-year gross-minus-net enrolment gap of **2.1966–14.6273 pp** at primary (30 pairs, 1976–2017),
**17.4120–29.2395 pp** at lower secondary (4 pairs, 2014–2017) and **46.0621–51.7045 pp** at upper secondary
(**2 pairs, `THIN`**). But that object is **not the model's object**. The model's participation margin is
`demand_share` — the **choice share** `p_school + p_both` over the model's level cohort, a fraction in [0, 1]
(`generator_v1_3/code/sim_v1_3.py` lines 787 and 804, carried unchanged into v1.6 and v1.7). The observed gap is a
difference of two **enrolment ratios** in percentage points of the official age band. They share **neither numerator
nor denominator nor unit**, and EXP-21's register — the only register that could license a comparison — records **no
line** for either object (its convention family is completion/GER; it explicitly computes no NER statistic). The
identity test therefore fails at all three levels and the verdict is **`NO-OBSERVED-COUNTERPART`**: the model's
declared shares **cannot be placed** against any observed range in this record. The honest answer to "low relative to
what?" is: **relative to nothing observed on this disk** — the model's participation object is a choice share, not an
enrolment rate, and the level question cannot be settled descriptively either. The gross − net span enters the record
as the **bound on any participation claim**, not as a benchmark for the model.

---

## 2. The observed spans, per level (PHL, same-year pairs only)

| level | pairs | window | span min (year) | span max (year) | median | `THIN` | identity test | placement |
|---|---:|---|---|---|---:|---|---|---|
| primary | **30** | 1976–2017 | **2.196578 pp** (1976) | **14.627307 pp** (1999) | 10.086482 pp | no | `NO-REGISTERED-COUNTERPART` | **WITHHELD** |
| lower_secondary | **4** | 2014–2017 | **17.412040 pp** (2017) | **29.239540 pp** (2016) | 28.518155 pp | no | `NO-REGISTERED-COUNTERPART` | **WITHHELD** |
| upper_secondary | **2** | 2014–2015 | **46.062110 pp** (2014) | **51.704530 pp** (2015) | 48.883320 pp | **yes** | `NO-REGISTERED-COUNTERPART` | **WITHHELD** |

- **Source and arithmetic, every number:** `10_massification/data/UNIVERSALIZATION_SERIES.csv`, column `value` at
  `indicator = ger_<level>` minus `value` at `indicator = ner_<level>`, same `iso3 = PHL`, same `year`, both
  `status = observed`. Per-pair values with both source columns are in `results/PART_MARGIN_DESC_DETAIL.csv`
  (36 rows).
- **Reproduces the Council's anchors** (V35a–V35c, D153(xii)) to the magnitude: 2.1966–14.6273 (30), 17.412–29.2395
  (4), 46.0621–51.7045 (2). The 2017 primary pair is **5.591073 pp** (V35a: 5.5911).
- **Sign notation.** D153(xii) writes the span with a leading minus (net − gross, the gap read as a shortfall); the
  frozen block and V35a write `ger − ner`, which is **positive in every paired year**. The magnitudes are identical;
  this cell reports the block's signed value and makes **no direction claim**.
- **Record note.** `VERIFICATION_025.csv` V35b's note column reads `THIN` for lower secondary, which has **4** pairs.
  The frozen rule is **`< 3` pairs** and D153(xii) marks only upper as `THIN`; the rule governs, so lower secondary is
  **not** `THIN`. The discrepancy is recorded in the row's `notes` column, not silently resolved.
- **No pooled or cross-level margin is formed.** The three levels are reported separately; a single cross-level
  participation margin does not exist in this record (D153(xii)), and this cell does not construct one.

---

## 3. The identity test: why the model's share cannot be placed

The cell runs the identity test **against EXP-21's delivered register**, and it runs it **before** the observed series
is opened and **before** either model panel is read (event order in `results/COUNT_BLIND_AUDIT.json`; the open guard
would have aborted the run otherwise).

1. **The model object.** `demand_share` is the four-state block's `p_school + p_both`: the probability that a household
   in the level's cohort chooses school or both. It is a **fraction of a cohort**, not an enrolment count and not an
   enrolment rate (`generator_v1_3/code/sim_v1_3.py` 787 and 804; restated in `generator_v1_7_partrepair/FINDINGS.md`
   §1). In v1.6 it is a declared share (0.900000 / 0.900000 / 0.820000 at 2024); in v1.7 it is the same block's own
   share (0.995644 / 0.953477 / 0.800311 at 2024).
2. **The register.** `conv_reg_2026-11-20/results/CONV_REG.csv` has 18 rows and **one convention family only** —
   `UIS completion (pop 3-5y above grade) / GER (official age band)`. At each PHL level it carries exactly **1** line,
   and **0** lines name a numerator in {demand, choice} over a cohort. Its overall verdict is `REGISTER-BINDING`
   (6 of 12 frozen cells `NOT-INTERCHANGEABLE`, 6 cross `T = 1.0`). The register's own predeclaration hash was
   verified before the register was used — no register line here is `RECORDED-NOT-ENFORCED`.
3. **Silence is not a licence.** EXP-21's §3 states that it computes **no NER statistic** and that no NER line may be
   cited from it. So the register cannot license the span either; EXP-22's use of NER is licensed by its **own frozen
   block** and only inside `ger − ner`.
4. **Every candidate observed object fails the same-convention test** (`results/OBJECT_IDENTITY_AUDIT.csv`):
   - `ger_*` — all-age enrolment ÷ official age band, **percent**;
   - `ner_*` — official-age enrolment ÷ the same band, **percent**;
   - `completion_*` — cohort attainment on the population 3–5 years above grade, **percent**;
   - `oos_*` — out-of-school population ÷ official age population, **percent**;
   - `gross_intake_*` — entrants (all ages) ÷ official age population, **percent** and `status = check` (a throughput
     proxy, not an observation — `DATA_NOTES_MASSIFICATION.md` trap 4), so it is not even in the observed set and is
     therefore **not audited as an observed candidate**;
   - the **span** itself — **pp**, a difference of two ratios.
   None has the model's numerator (a choice probability) or its denominator (the model's level cohort).
5. **Consequence.** No observed range exists for the model object, so the placement is **`WITHHELD-NO-IDENTITY`**. The
   model values are printed beside the spans **for orientation only**: printing is not a comparison, and the cell
   asserts `cross_source_arithmetic_ops = 0` and `comparison_performed = FALSE`.

An independent, **declared** limit points the same way: the observed pair windows end in **2017** (primary, lower) and
**2015** (upper), while the model shares are at **2024**. There is **no observed same-year span at 2024** at any level,
so even a licensed range would be a **historical** range, not a same-year one.

---

## 4. Where the model's shares sit — the honest answer

| level | v1.6 `demand_share` (2024) | v1.7 `demand_share` (2024) | placed? |
|---|---:|---:|---|
| primary | **0.900000** | **0.995644** | **no — `WITHHELD-NO-IDENTITY`** |
| lower_secondary | **0.900000** | **0.953477** | **no — `WITHHELD-NO-IDENTITY`** |
| upper_secondary | **0.820000** | **0.800311** | **no — `WITHHELD-NO-IDENTITY`** (also `THIN`) |

`SYNTHETIC`; class-tagged; read from `generator_v1_6_repair/results/panel_A10_repaired.csv` and
`generator_v1_7_partrepair/results/panel_A17.csv`, column `demand_share`, rows `country = SYN00_PHL_LIKE`,
`year = 2024`. **Not verdict-bearing, never regenerated, never placed.**

- The two **classes differ from each other** (primary 0.900000 vs 0.995644; lower 0.900000 vs 0.953477; upper 0.820000
  vs 0.800311). That is a fact about two synthetic arms, **not** a result of this cell, and it is **not** a comparison
  with the observed record.
- The observed spans are in **pp**; the model shares are **fractions of a cohort**. Setting one against the other —
  including by any rescaling, any conversion, or any "so the model is N pp low" arithmetic — is barred by D158(2) and
  by the block's falsifier. No such number is computed anywhere in this cell.

---

## 5. What this changes for the write-up

- **Retired sentence.** *"The model's participation share is too low (0.900 vs 0.996)."* It compares two **synthetic
  classes** and implies an observed benchmark that the record does not contain. It is now barred, and this cell's
  verdict is why.
- **A sentence the record does support** (candidate; adoption is the Lead's / EXP-25's, not this cell's):
  > *"The model's participation object is a choice share over the cohort — `SYNTHETIC`, v1.6 0.900000 / 0.900000 /
  > 0.820000 and v1.7 0.995644 / 0.953477 / 0.800311 at 2024 — and no observed object on disk shares its numerator or
  > denominator. The observed participation margin is instead a gross − net enrolment gap: 2.1966–14.6273 pp at
  > primary (30 pairs, 1976–2017), 17.4120–29.2395 pp at lower secondary (4 pairs, 2014–2017) and 46.0621–51.7045 pp
  > at upper secondary (2 pairs, 2014–2015, `THIN`). The two objects are not comparable, so the model's share cannot
  > be placed in an observed range."*
- **What does not change.** D63 stays `UNABLE as to cause`; the generator line stays closed at representation-only
  (D150); the level miss stays non-decomposable (D153(xi)); no model, parameter, target or sentence is adopted here.
- **What a reader of the negative can now be told.** The negative is **not** "the model is too low relative to the
  observed margin", because no such comparison exists. It is "the model's participation object has no observed
  counterpart in this record; the observed margin spans levels steeply, and its upper-secondary leg rests on two
  pairs".

---

## 6. Honest limits

- **`THIN` upper secondary: 2 pairs, 2014–2015.** The largest observed gap (46–52 pp) is the **least measured** part
  of the record. Two pairs cannot support a range statement, no placement label was available there even before the
  identity test failed, and nothing in this cell says what the upper-secondary margin "typically" is.
- **Lower secondary: 4 pairs, 2014–2017.** Above the 3-pair gate, but four adjacent years in one system support no
  trend and no "typical" value. The median (28.518155 pp) is an arithmetic description of four pairs, nothing more.
- **Primary: 30 pairs but a closed window.** The pairs run 1976–2017 and **stop**, because the PHL primary NER series
  ends in 2017. The gap after 2017 is **not** observed here, and the model year 2024 has no same-year observed span at
  any level.
- **Two source campaigns.** `ger_*` is `WDI_UIS_derived`; `ner_*` is `UIS_EDUNONCORE_2020_02`. The span is the
  difference of two delivered observed series on the same declared denominator class, **not** a reconciled
  measurement and **not** a count of over-age pupils (this cell is count-blind; it forms no count).
- **One system, one series.** PHL only. The block's anchors are PHL's and the model's placement subject is its PHL
  row; other systems' `ger`/`ner` rows are **not computed** here (declared scope, §4.9 of the predeclaration).
- **No conversion, no proxy, no cause, no direction.** A gross − net gap is not evidence of a mechanism; a placement
  (were one licensed) would not be evidence about demand, capacity or policy; and the sign of the gap is not a
  direction claim.
- **The model numbers are placement subjects only.** They are `SYNTHETIC`, class-tagged, read from delivered panels,
  never regenerated, and never combined with an observed value.

---

## 7. What was not done (count-blind, closed claims)

- **No model run, no re-fit, no parameter set.** The panels are read, not regenerated.
- **No model score of any kind**: no 33-cell score, no 9-cell score, no deviation, no within-±5 pp hit count, no
  crossing count, no observed-path coverage count. The exhaustive list of counts the cell does compute is in
  `results/COUNT_BLIND_AUDIT.json` — three `n_pairs`, three `n_unpaired_years`, and five process counts of register
  rows, structure and the six placement values. Nothing else is counted.
- **No re-score of EXP-18**, no re-derivation of V6, no reopening of the level localisation, no re-attribution of the
  failure.
- **No proxy, no adoption, no new data ask, no web access, no touch to the running server**, and no write outside
  `10_massification/extensions/part_margin_desc_2026-11-20/`.

---

## 8. Provenance and reproduction

| what | where |
|---|---|
| predeclaration (definitions, thresholds, precedence, count-blind clause) | `PRE_DECLARATIONS.md`, hash `8f47aa216395b6c0da1eb78e696ed80796a077c72780ac4211d2143ddda439bd` |
| per-level spans (3 rows) | `results/PART_MARGIN_DESC.csv` |
| per-pair values with both source columns (36 rows) | `results/PART_MARGIN_DESC_DETAIL.csv` |
| object-identity audit, every candidate object and the model object (21 rows) | `results/OBJECT_IDENTITY_AUDIT.csv` |
| verdict, precedence trace, verbatim checks | `results/VERDICT.json` |
| count-blind audit: event order, allow-list, guards, count table | `results/COUNT_BLIND_AUDIT.json` |
| input hashes | `results/INPUT_HASHES.json` |
| determinism (two runs, byte-identical in all 6 artifacts) | `results/DETERMINISM.json`, `results/determinism_run2/` |
| run log (no clock, no absolute paths) | `results/console.txt` |

Reproduce (from the cell directory):

```
python code/verify_verbatim.py
python code/run_part_margin_desc.py --out results
python code/run_part_margin_desc.py --out results/determinism_run2
python code/run_part_margin_desc.py --compare results results/determinism_run2
python code/make_manifest.py
```

**Verdict: `NO-OBSERVED-COUNTERPART`** — clause 1 of the frozen precedence fired at all three levels; clauses 2 and 3
(`PLACEMENT-OUTSIDE`, `PLACEMENT-INSIDE`) were **not reached**, because no observed object with the model's convention
exists at any level-year.
