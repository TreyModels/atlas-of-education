# BENCHMARK MEMO — the benchmark hierarchy: persistence/trend as a humility floor, and what would count as a dynamic

**`LABEL: DEBUG`** · debug-mode memo, **MODEL-DEBUG MODE** (ceiling-cap defect work-stream), dispatched under the Lead's user directive.
Directory `10_massification/extensions/model_debug_2026-11-21/benchmark_memo/` — own directory, new files only; **no existing repo file was modified**.
Authority: [`PRE_DECLARATIONS.md`](../PRE_DECLARATIONS.md) §2–§3 item 3 (sha256 `748335cf915394c3f0dc0241fa2c5b6eaaae9c0af201dba97d3c2de24d8f6553`).

| field | value |
|---|---|
| document | `benchmark_memo/BENCHMARK_MEMO.md` — the benchmark-hierarchy note (debug cell 3 of 3) |
| label | **`DEBUG`** on every artifact in this directory; inherited labels preserved where a number is quoted (`OBS` / `SIM` / `DERIVED` / `DECLARED` / `HELD`) |
| class tags | `A1 anchor class (12 arms)` · `v1.2` / `v1.3 A00` · `v1.7 (A17)` — carried wherever a model number is quoted (D165(xii)) |
| status of this memo | **`PROSPECTIVE`** — it proposes text the user may approve later; it applies nothing |
| the document it reads, and does **not** edit | [`PHASE_WRITEUP.md`](../../lit/PHASE_WRITEUP.md) sha256 `d0820eb8311c315d04610e872c44b9f9e257cb6817e057d80f050704384a251e`, gate [`PHASE_WRITEUP_GATE.md`](../../lit/PHASE_WRITEUP_GATE.md) sha256 `cee5b0c84602fd431b34e3097d37c60217329fd0e4eaabfc606e634aa375196d`, **`WRITE-UP-GATE: PASS`** |
| what this memo does not do | no model run, no re-run, no re-score, no new number, no new cell, **no reproduction claim**, no causal claim, no direction claim |
| phase verdict | untouched — `PARTIAL / DESCRIPTIVE / EQUIVALENT` (D76/D77 are *applied*, never amended here); experiment programme `CLOSED` at 0 new cells (D167) |

---

## 0. Why this memo exists

The shipped write-up states the phase's level result as a loss: the A1 anchor class is reproduced at a **conditional level** and it **loses to the 4.35 pp linear-trend benchmark**. That sentence is correct and stays. What it does **not** say — and must not be read as saying — is anything about dynamics. The user's objection (quoted in §1) is exactly that the "lost to a straight line" framing, read as a finding about the world, identifies no dynamic: it restates "line goes up".

This memo does three things and nothing else:

1. records the directive **verbatim** (§1);
2. states the **hierarchy** — persistence and linear-trend comparators are a **humility floor**, a **necessary benchmark only**, never sufficient evidence of a dynamic — and then walks the programme's **actual** results through that hierarchy, one by one, naming which are **DYNAMIC-type** and which are **FLOOR-ONLY** (§3, with the machine-readable twin `BENCHMARK_INVENTORY.csv`);
3. writes down **what would count** as identifying a dynamic (§4), names the candidate directions the programme already has on disk **without claiming them**, and flags a **prospective amendment** the user can approve later (§5, boxed).

**No number in this memo is computed here.** Every number is a **quotation** from a delivered file, cited by path + column (Appendix A), or appears inside a sentence quoted from the write-up, which carries its own citation. A quotation is not a new number, and a memo is not a result: nothing here changes a verdict, a label, a threshold or a cell.

---

## 1. The user directive (verbatim)

On the "lost to a straight line" framing — the user's critique, relayed by the Lead on **2026-11-21**, recorded verbatim in [`PRE_DECLARATIONS.md`](../PRE_DECLARATIONS.md) §2:

> "Of course what happened last year predicts what happens next year… I'm questioning who the fuck cares — that doesn't identify any dynamic other than 'line goes up'."

*Attribution.* This is **the user's critique of the "lost to a straight line" framing**, relayed by the Lead (2026-11-21); it is reproduced here exactly as given, and it is the reason this memo exists. It is a statement about **what the benchmark can and cannot license**, not a statement that the write-up's number is wrong. The write-up's number stays; what changes is the **reading** of what that number is evidence for, and this memo proposes that reading (§5).

---

## 2. The hierarchy

### 2.1 Two levels, not one

| level | question it answers | what a result at this level licenses | what it cannot license |
|---|---|---|---|
| **HUMILITY FLOOR** — persistence / linear-trend benchmark | does the model add **predictive content over extrapolation**? | "the class does / does not beat extrapolating the series" — a statement about the model's **level error against the past** | anything about a mechanism, a transition, a crossing, an asymmetry, or a distribution |
| **DYNAMIC TEST** — transitions, asymmetries, crossing timing, distributional change | does the model carry **the process that produced the observed change**? | a claim about *how* the path was generated, bounded by its window and its counterfactual | a level claim, a forecast, a causal claim, a direction claim |

**The rule, stated flatly.** Persistence / linear-trend benchmarks are a **HUMILITY FLOOR, not a dynamic test**. Beating or losing to a trend says only that the model **adds (or fails to add) predictive content over extrapolation**. It is a **necessary benchmark only** — never sufficient evidence of a dynamic. The programme's **dynamic** claims must rest on **transitions, asymmetries, crossing timing, and distributional change**; nothing else in this record can carry them.

### 2.2 Why a trend is necessary but can never be sufficient

Four reasons, each independent of any result:

1. **It is the same series, extrapolated.** A persistence or trend comparator contains no transition, no crossing and no asymmetry, because it is built to have none. A model that beats it has shown it tracks the series better than the series tracks itself; that is a statement about error, and error is a level object.
2. **It cannot discriminate among mechanisms.** Every driver that is monotone in time shares the trend's sign; that is why the comparator is cheap, and why it is weak. In this record **all 12 arms carry the standing scaling verdict `FAIL`**, and the write-up records the class as **losing on holdout to the trend** — a comparator that the class fails tells you the class is *not there yet*; it does not tell you *what dynamic is there*. (The `none` arms show the other tail: they fit best and hold worst — the overfit story, W-1.3. A floor verdict that moves with the arm set is fragile by construction, which is another reason it cannot carry a dynamic claim; see the reading hazard in §3.4 item 1.)
3. **A falsifier stated on it is a level bar.** "Holdout MAE below 4.35 pp" is a bar on a level error. The programme's own discipline reads moving a model against a level as a **fit** (D144(5)/R27; D154 forbidden re-entries), so a level bar cannot be the falsifier that identifies a dynamic without inverting the discipline.
4. **It is what the user said it is.** "Line goes up" is the trend restated. If the benchmark is the whole test, the model's content is the benchmark's content, and no dynamic has been identified by anyone.

### 2.3 What the shipped write-up actually says — quoted, never edited

The gate-passed write-up is quoted here for the record; it is **not** edited by this memo (sha256 above; `WRITE-UP-GATE: PASS`).

`[C-01 · SIM · A1 anchor class (12 arms), the phase's level object O-1 · — · CLOSED]`, verbatim:

> The phase's level statement is conditional level reproduction at fit MAE 1.047492271754753–3.2916863270693772 and holdout 4.014780434743067–6.122199101442962 across the 12 arms, losing to the 4.35 pp linear-trend benchmark, with placement 9/33 recorded separately as a placement and not as a reproduction.

The W-1.1 phase-object block, verbatim:

> Conditional **level** reproduction — fit MAE **1.047492271754753–3.2916863270693772** across the 12 arms, holdout **4.014780434743067–6.122199101442962**, losing to the **4.35 pp** linear-trend benchmark (`4.352883341604888`) — plus observational equivalence and one unreproduced upper-secondary asymmetry; **placement** (`v1.2` / `v1.3 A00`, status `CLOSED`): **9/33**, and a placement is not a reproduction.

The C-04 benchmark-bounded clause, verbatim:

> … and **benchmark-bounded** (the decisive comparator is the linear trend, stored `4.352883341604888` in `calibration_table.csv` column `naive_trend` at `iso = PHL`, with persistence stored `8.599852941176476` in column `naive_persistence`).

**Reading of these three quotations, under this memo's hierarchy.** They are correct, and they are **floor statements**. The write-up already does the hard part: it scopes the negative (specification-, record-, sign- and benchmark-bounded) and it refuses to read placement as reproduction. What it does not do — because the gate did not ask it to — is say out loud that the benchmark is a **floor**, so that a reader cannot mistake "lost to a straight line" for "a dynamic was tested and failed". That is the whole content of the prospective amendment in §5. Nothing in the three quotations is wrong; one sentence of *frame* is missing.

---

## 3. The inventory — what the programme actually has

Ten results are inventoried below; the machine-readable twin is [`BENCHMARK_INVENTORY.csv`](BENCHMARK_INVENTORY.csv) (same rows, same classifications, same evidence paths).

**How the two classification words are used, exactly.**

- **`DYNAMIC`** — the *object under test* is a dynamic-type object: **a crossing, a transition, an asymmetry, a lag, or a placement over time**. The row records how far the result actually evidences that dynamic via the `dynamic grade` column. `DYNAMIC` does **not** mean "a dynamic was identified".
- **`FLOOR-ONLY`** — the result carries **no dynamic content**: it is a level/benchmark statement, an identification null, a static cross-section, an identity null, a representation capability, or a declared theory. `FLOOR-ONLY` is not a slur on the result; several of these are the programme's most defensible products.

**The single most important number in this table is the last column: `0` of 10 results identify a dynamic** under the criteria of §4. The programme has dynamic-type **objects** on disk; it does not yet have a dynamic **identification**.

### Table 3.1 — the ten results, classified

| # | result (object) | class / object | classification | dynamic grade | identifies a dynamic? | evidence (path · column / row) | decision |
|---:|---|---|---|---|---|---|---|
| 1 | **A1 anchor-class negative** — 12 arms; the class is recorded as losing on holdout to the trend, and that loss is the phase's level statement | `A1 anchor class (12 arms)` | **FLOOR-ONLY** | `LEVEL-BENCHMARK-NEGATIVE` | **NO** | `10_massification/model/anchor_out/anchor_table.csv` · `fit_mae`, `hold_mae`, `scaling_verdict`; `10_massification/model/calib/calibration_table.csv` · `naive_trend`, `naive_persistence` (`iso = PHL`) | D76/D77; D165(x); D168(a) |
| 2 | **Observational-equivalence / discrimination null** — capacity-gated ties law-only; the direction is not identifiable (forced-ID) | `A1 anchor class (12 arms)` + `DECLARED` | **FLOOR-ONLY** | `IDENTIFICATION-NULL` | **NO** | `10_massification/model2/runs/recovery.csv` · `truth`, `best`; `10_massification/model2/A5B_REPORT.md`; `anchor_table.csv` · `hold_mae` (`capacity_gated` vs `law_only`) | D77; R13; A5b |
| 3 | **Upper-secondary asymmetry** — floor moves, ceiling does not; unreproduced by every model on disk; placement 9/33 | `OBS` + `SIM` (`A1 anchor class`, `v1.2` / `v1.3 A00`) | **DYNAMIC** | `ASYMMETRY-UNREPRODUCED` | **NO** — the bar is a cell count, and the asymmetry's first element was never recorded (C8 gap) | `anchor_table.csv` · `M2`, `M3`; `extensions/synthetic_2026-11-20/generator_v1_7_partrepair/results/observed_path_A17.csv` · `within_5pp_A00`; `10_massification/data/UNIVERSALIZATION_SERIES.csv` · `value` | D77 sharpened statement; W-2.7; C-07/C-15 |
| 4 | **EXP-7 path result** — 9/33 in band against the 17/33 bar → `ENDPOINT-ONLY` | `v1.2` / `v1.3 A00`, `SYNTHETIC` panel | **DYNAMIC** | `ENDPOINT-PLACEMENT` | **NO** — a crossing/endpoint **placement** statement, not a path | `extensions/repro_path_2026-11-20/results/PATH_COMPARISONS.csv`; `.../FINDINGS.md` §2 (verdict `ENDPOINT-ONLY`) | D122 #2; D141 (A00 comparator); W-1.2 |
| 5 | **EXP-21 conversion register** — 12 frozen system × level cells on `T = completion / GER`; 4 `INTERCHANGEABLE`, 6 `NOT-INTERCHANGEABLE`, 2 `THIN` | `DERIVED` (EXP-21 rows) | **FLOOR-ONLY** | `STATIC-CROSS-SECTION` | **NO** — same-year ratios, no time-evolution object | `extensions/conv_reg_2026-11-20/results/CONV_REG.csv` · `verdict`, `n_pairs`, `T_min`, `T_max`, `in_band_share`, `crossing_year`; `M_CONSTANCY.csv` | D160/D164; W-2.1–W-2.6 |
| 6 | **EXP-22 participation spans** — gross − net spans by level; identity test negative | `DERIVED` (PHL `ger_<level> − ner_<level>`) | **FLOOR-ONLY** | `HISTORICAL-IDENTITY-NULL` | **NO** — historical spans (pairs end 2017/2015), no observed counterpart for the model object, `comparison_performed = FALSE` | `extensions/part_margin_desc_2026-11-20/results/PART_MARGIN_DESC.csv` · `span_min_pp`, `span_max_pp`, `n_pairs`, `identity_test`, `placement`; `OBJECT_IDENTITY_AUDIT.csv` | D164 (EXP-22); W-3 |
| 7 | **EXP-23 D63 split** — residual 14.974746704101562 pp split 58.6008386858443 % pipeline / 41.3991613141558 % transition at the declared t−3 pair; B1 `OUTSIDE`, B2/B3 `INSIDE` | `DERIVED` (upper-only leg) | **DYNAMIC** | `LAG-DECOMPOSITION-BOUNDED` | **NO** — a t−3 accounting decomposition with no counterfactual; `D63 UNABLE as to cause` | `extensions/d63_bounds_2026-11-20/results/D63_BOUNDS_RESULTS.csv` · rows S1, S8, S9, B1–B3, columns `value_num`, `outcome` | D153(xiii); D164 (EXP-23); W-4 |
| 8 | **EXP-24 κ register** — per-system transition ratio, four windows, hold-out cells | `DERIVED` (κ = transition ratio) | **DYNAMIC** | `TRANSITION-RATIO-WINDOW-ONLY` | **NO** — explicitly **not forward**; KOR is the counter-example | `extensions/kappa_write_2026-11-20/results/KAPPA_WRITE_REGISTER.csv` · `kappa_full`, `window_full_upper`, `slope_ratio_per_year`, `half_median_shift_pp`, `holdout_within`; `KAPPA_WRITE_SUMMARY.csv` | D138; D143(i); D153(ii); D164 (EXP-24) |
| 9 | **v1.5–v1.7 representation** — upper unfilled 15/15, both-level queue 30/30, strict both-level coexistence 0/15, 0/33 vs the ≥17/33 bar, crossings 1/3 | `v1.7 (A17)` (closed family) | **FLOOR-ONLY** | `REPRESENTATION-ONLY` | **NO** — a representation capability; not a level claim and not a dynamic | `extensions/synthetic_2026-11-20/generator_v1_7_partrepair/results/v1_7_checks.csv` · rows S1–S3, `synthetic_value`, `threshold`, `legs_passed`; `representation_cells.csv` · `unfilled`, `queue_ratio`, `coexists` | D150; D153(ix); D154 |
| 10 | **One-way ratchet / bimodal A5** — the user's structural frame | `DECLARED-THEORY` | **FLOOR-ONLY** | `DECLARED-THEORY` | **NO** — declared as theory, never evidence; no synthetic PASS may be read as confirmation | `extensions/synthetic_2026-11-20/THEORY_FRAME.md` §1–§2 (D124 bimodal; D125 one-way ratchet) | D124/D125; C-34; W-6.4 |

*Table caption (A-1 form):* `DEBUG` memo table; label(s) `DERIVED` (classification) + inherited labels per row; objects as printed; **no κ window is attached to a row that does not quote κ** (row 8 carries its windows in the evidence column); status `PROSPECTIVE`. Every evidence path resolves on disk at the hashes in `RUN_MANIFEST.json`.

### 3.2 The counts, and what they mean

| classification | count | rows |
|---|---:|---|
| **`DYNAMIC`** (dynamic-type object) | **4** | 3 (asymmetry), 4 (EXP-7 endpoint), 7 (D63 lag split), 8 (κ transition ratio) |
| **`FLOOR-ONLY`** | **6** | 1 (A1 benchmark negative), 2 (identification null), 5 (EXP-21 cross-section), 6 (EXP-22 spans), 9 (representation), 10 (declared theory) |
| **identifies a dynamic under §4** | **0** | — |

**Consequence, stated without softening.** Four results in this record are *about* dynamic-type objects; **none** of the four is a dynamic identification. Six results are floor-only, and one of them (row 1) is the very result the "lost to a straight line" framing names. The programme's honest position is therefore:

- the **negative** (row 1) is a **floor** result — it says the `A1 anchor class` adds no predictive content over extrapolation on this record, and it says nothing about dynamics either way;
- the **asymmetry** (row 3) is the closest thing to a dynamic in the record, and it is **unreproduced**: an asymmetry observed, no model on disk producing it, and the instrument that measured it (placement 9/33) is a cell count, not a crossing-time test;
- the **κ register** (row 8) is the only object on disk that is a genuine transition-rate quantity, and its own predeclared test came back **`WINDOW-ONLY`** — KOR passes the stationarity bars and then misses **0/3** hold-out cells, which is precisely why the register may not be written forward.

### 3.3 The four dynamic-type objects, one line each

1. **Row 3 — the asymmetry.** Observed: primary completion ≥90 first (2017), lower-secondary ≥90 (2024), upper-secondary never ≥90 by 2024. Reproduced: `M2` clean **0/12**; `M3` in-window **12/12** with two post-window overshoots. The asymmetry is a genuine dynamic-type object — an ordering in time where one level moves and another does not — but the test applied to it is a **placement count** (9/33 within ±5 pp), which is a level bar in cell units, and the C8 reporting gap means the asymmetry's first element (the primary 2017 crossing) was never in the committed A1 outputs, so it was tested with that element missing. An unreproduced asymmetry is evidence **about the models**, not evidence **of the mechanism**.
2. **Row 4 — EXP-7.** `ENDPOINT-ONLY`: 9/33 in band, 13/33 within ±10 pp, and the split at 2020 (22 cells → 2 in band; 11 cells → 7 in band) is the finding that the panel is a **2021–2024 placement**, not a path. A placement is a crossing/endpoint statement; it is not a path, and it is not a transition.
3. **Row 7 — D63.** The split is at a **declared one-stage pair** (upper 2024 against lower 2021) and every citation must carry the t−3 sentence (at the contemporaneous lower value the pipeline share is −0.14544291665697634 and the ratio share 1.145442916656977). The lag structure is real; the decomposition is bounded (B1 `OUTSIDE`, B2/B3 `INSIDE`, `BOUNDS-EDGE` = 1 of 3 outside and nothing else), and `D63` stays **`UNABLE as to cause`**. A lag accounting identity is not a counterfactual.
4. **Row 8 — κ.** The transition ratio is the right *kind* of object and the register is honest about its limits: PHL 0.949135 (windows 2003–2017 / 2003–2024, half-shift 2.1348 pp, hold-out 2/2), KOR 0.989758 (2005–2020 / 2005–2023, 0/3 hold-out), KHM 0.594984 (2000–2017 / 2000–2023, 1/2), CHN 0.722222 (2012–2020, 0 hold-out cells). It is **`WINDOW-ONLY`**, and the KOR counter-example bars "κ-STABLE is forward-usable". The object qualifies as dynamic-type; the result does not qualify as a dynamic identification, by the predeclared test's own verdict.

### 3.4 The six floor-only results, one line each

1. **Row 1 — the A1 negative.** The benchmark result itself: 12 arms, fit 1.047492271754753–3.2916863270693772, holdout 4.014780434743067–6.122199101442962, against `naive_trend` 4.352883341604888 (persistence 8.599852941176476, a higher level error). *That the class loses to the trend is its point* — the negative is **benchmark-bounded**, and a benchmark-bounded negative is a floor statement by construction. The overfit story (the three `none` arms fit best — 1.047492271754753, 1.318865482339633, 1.371270727493839 — and hold worst — 5.875474290798293, 5.938227008289883, 6.111754907690532) is the honest version of the level claim, and it is still a level claim.

   **Reading hazard (recorded, not adjudicated).** The arm-level holdout cell for `complementary · capacity_gated` is **4.014780434743067** (`anchor_table.csv` column `hold_mae`), numerically below the trend's **4.352883341604888** (`calibration_table.csv` column `naive_trend`, `iso = PHL`), while the write-up's sentence compares the 12-arm class against that trend. The two cells come from **different tables and different objects** (per-arm anchor fit vs the rival-level calibration comparator), and this memo **does not re-score the comparison** and does not call the sentence wrong. It records the hazard because it is the same point as §2.2: a floor verdict that can flip on one arm is a fragile level object, and a fragile level object is the last thing that should be asked to carry a dynamic claim.
2. **Row 2 — the equivalence / discrimination null.** Capacity-gated ties law-only in 2 of 3 rivals on crossings, better on holdout in 1 of 3, worse in 2 of 3; and the direction is not identifiable (forced-ID 1.00 against a declared bar of 0; equivalence 0.07 against a bar of <0.34; the outside cohort/fertility truth is forced into a candidate channel in 5 of 5 runs in `recovery.csv` — `truth = OUT`, `best` ∈ {`S`, `C`}). This is a result about **the map of models**, not about the world's dynamics; it identifies nothing.
3. **Row 5 — EXP-21.** A **static cross-section**: same-year `T = completion / GER` ratios over 12 frozen cells. It answers "are completion and GER one scale, and where?", not "how did the relation move". Its one apparently temporal column (`crossing_year`) records *when the ratio crossed 1.0* — and the write-up's own citation condition C-4 says a crossing there is **descriptive, not a trend** (KOR upper crosses five times). The `m`-constancy result (A17 `CONSTANT` 8.8395202269e-10; v1.3/v1.2 `NOT-CONSTANT` 4.7043695535e-02; 35 of 6,720 cells capped) is a conversion-convention statement, and the debug work-stream is repairing the cap as a defect — none of that is dynamic.
4. **Row 6 — EXP-22.** Spans: primary n = 30, 2.196578–14.627307 pp (median 10.086482); lower n = 4, 17.412040–29.239540 pp (median 28.518155); upper n = 2 **`THIN`**, 46.062110–51.704530 pp. The identity test fails at all three levels (0 matching register lines), placement `WITHHELD-NO-IDENTITY`, `comparison_performed = FALSE`, and the pairs end 2017/2015. A **historical, identity-negative** object: no observed counterpart exists for the model's object, so no distance exists to render. A distributional-looking span with no series and no counterpart is not a distributional-change test.
5. **Row 9 — representation.** `v1.7 (A17)` is **representation-only**: upper unfilled 15/15, both-level queue 30/30, strict both-level coexistence 0/15, 0/33 against the ≥17/33 bar, crossings 1/3. That is a statement about what the class **can represent**, and D153(ix) nails the capability down to a **single tier**. Representation is a precondition for a dynamic test, never the test.
6. **Row 10 — ratchet / bimodal A5.** Carried as `DECLARED-THEORY` (D124, D125): the bimodal-within-one-system frame and the no-reverse-button frame. "Never evidence" is textual in `THEORY_FRAME.md` §1–§2, and C-34 repeats it. Adjacent but distinct: WT4 in `extensions/wt_2026-11-20/FINDINGS.md` reports **exit episodes = 0** over its declared window — a descriptive non-event that is *consistent with* the ratchet and is **not** a test of it (the WT battery's decision-relevant legs both returned null and the layer stays `PARKED`, D101).

### 3.5 Three adjacent on-disk results, deliberately **not** in the inventory

- **HKG transfer** — `extensions/hkg_transfer_2026-11-20/HKG_H1_OUTCOME.md`: the construct test **failed** (band max 2.685005 pp; crossings 3 y and 2 y apart) and the transfer is `BLOCKED-MEASURE(SR-1)`. **No HKG result exists**, so there is nothing to classify.
- **Education → ECI** — `extensions/edu_eci_2026-11-20/FINDINGS.md`: a descriptive/associational 30-country panel with symmetric reverse-order specs and no direction claim. A cross-country association over a common window is not a dynamic test; it is also not a benchmark, so it sits outside both rows.
- **WT4** — covered in row 10 as adjacent, because it is the one on-disk object that speaks to the ratchet and it speaks as a **null**.

Excluding these three is a scope decision, stated here so that the count of ten is not mistaken for the whole record.

---

## 4. What would count as identifying a dynamic

### 4.1 The four conditions

A result identifies a dynamic only if **all four** hold:

- **D-1 · Object.** The quantity under test is a **transition, a crossing time, an asymmetry, or a distributional shift** — not a level and not a level's error. (A level can enter as a *diagnostic*; it cannot be the verdict object.)
- **D-2 · Out-of-window.** The object is **estimated in one window and evaluated in a window disjoint from it**, and it remains **stable or predictive out of the very window in which it was estimated**. In-sample stability is not this condition — it is the default failure mode of every level fit in this record.
- **D-3 · Counterfactual or distributional shift.** The result carries an **explicit counterfactual** (what the object would be under a stated no-shock / no-policy / no-capacity-change world) **or** a **distributional-shift test** (a change in a distribution — of enrolment age, of the participation margin, of gate ratios — not a change in a mean level).
- **D-4 · Falsifier.** The **predeclared falsifier is not a level bar**: it is phrased on the dynamic object itself (a crossing-year error, a transition-rate sign or stationarity, an asymmetry's sign, an out-of-window predictive failure). "Holdout MAE below x pp" and "k of n cells within ±5 pp" are level bars and cannot serve.

**Two corollaries.** (a) A dynamic identification that passes D-1…D-4 is still bounded by its window and its counterfactual; it licenses a sentence about **how this record's change was generated**, never a forecast and never a direction. (b) A **failed** dynamic test is a result; a **missing** dynamic test is not. The programme currently has more of the second than the first, and this memo does not convert one into the other.

### 4.2 The four conditions applied to the programme's own objects

| object | D-1 object | D-2 out-of-window | D-3 counterfactual / distribution | D-4 non-level falsifier | verdict |
|---|---|---|---|---|---|
| **κ transition ratio** (row 8) | **yes** — a transition rate | **no** — `WINDOW-ONLY`; KOR 0/3 hold-out | **no** — no counterfactual object | **partly** — slope/half-shift bars, but the shipped label is `WINDOW-ONLY` | **not a dynamic identification** |
| **asymmetry** (row 3) | **yes** — an ordering/asymmetry | **no** — tested in-window, first element missing (C8) | **no** | **no** — 9/33 and ≥17/33 are cell-count (level) bars | **not a dynamic identification** |
| **D63 split** (row 7) | **partly** — a lag decomposition | **no** — one declared pair, one year | **no** — cross-year arithmetic, no counterfactual | **no** — the bounds are level comparisons | **not a dynamic identification** |
| **EXP-7 path** (row 4) | **partly** — placement over time | **no** — in-sample placement | **no** | **no** — 17/33 cells | **not a dynamic identification** |

This table is the memo's answer to the user's question in the sharpest form available: the programme's dynamic-type objects fail on **D-2** (they are window-bound) and **D-4** (their falsifiers are level bars). Those are exactly the two conditions that "line goes up" cannot supply.

### 4.3 Candidate directions the programme already has on disk — **named, not claimed**

These are directions, not results. None is run, predeclared or claimed here; D167 closed the experiment programme at **0 new cells**, and any test below would require a new predeclaration and a new Council decision (D154's re-entry rule: a **measured** object currently `HELD` **and** a decision).

1. **A forward transition-ratio test.** The object exists — `KAPPA_WRITE_REGISTER.csv` carries `kappa_pre` / `kappa_full` and `holdout_within` per system, and the pre-2021/full split is already the right shape for D-2. **But the test has already been run and failed on its own terms**: D138 returned **`WINDOW-ONLY`**, and KOR passes the stationarity bars yet misses **0/3** hold-out cells. So the direction is *not* "re-run κ forward"; the honest direction is a **new** design in which the estimation and evaluation windows are disjoint **by construction**. Not admissible this phase.
2. **A crossing-timing test.** Crossing objects exist on disk: `crossing_year` / `crossing_interval` / `n_crossings` in `CONV_REG.csv` (PHL primary 2021; PHL upper 2017; KOR lower 2010 and 2017; KOR upper five crossings; KHM upper 2001 and 2008) and the `M0`–`M4` vector in `anchor_table.csv`. The **C2 re-opener** ("fixed-behaviour crossings within ±5 y on the corrected informative vector, incl. primary 2017") is a crossing-time object by construction. It would qualify under §4.1 **if** the falsifier were the **crossing-year error** (a D-4 non-level bar) and the evaluation window were outside the estimation window (D-2) — which is precisely what the shipped placement count (9/33 cells) is **not**. The instrument and the C2 object are not the same object, and the gap between them is the work.
3. **A distributional-change test on the enrolment-age structure.** The UIS completion convention counts population **3–5 years above grade** while GER counts the official age band — so `T = completion / GER` (EXP-21) is a monotone transform of an **age-structure distance**, and a shift in the age structure is exactly the kind of distributional object D-3 asks for. The obstacle is data, not method: there is **no observed enrolment-age series on disk** (the level-specific GER series end 2018; `T` is a single ratio per cell, not a distribution; the margin pairs end 2017/2015). This is a **data gap**, recorded as such, not a runnable test.

### 4.4 What would **not** count

- A better holdout MAE, or beating 4.35 pp on a subset or another arm. (Floor, D-4 violation.)
- A second extrapolative comparator — persistence is already in the table at 8.599852941176476, and adding comparators adds floors, not dynamics.
- A re-scored 33-cell count, or a re-run of any delivered cell (forbidden: D150/D154).
- Reading a κ value forward, or any κ projection past 2024/2023/2020 (barred: D138, C-30).
- Any synthetic PASS read as confirmation of the theory frame (barred: C-34).
- A finding that "the line went up" restated in transition vocabulary. A dynamic identification is a statement about **the process that produced the change**, with its window, its counterfactual and its falsifier named.

---

## 5. Prospective amendment — the write-up is **not** retro-edited

### 5.1 Status of the gate-passed document

`10_massification/lit/PHASE_WRITEUP.md` (sha256 `d0820eb8…`) passed its frozen gate — **`WRITE-UP-GATE: PASS`** (A-1…A-8) — and is **not edited** by this memo or by the debug work-stream. This memo is a **prospective amendment**: it proposes text the user can approve later, and it applies **nothing**. The "lost to a straight line" framing in the shipped write-up **stands as written**; what this memo records is that it should be **read as a humility floor** — a benchmark outcome, not a dynamic finding — and that one sentence of frame is missing. `BENCHMARK_MEMO.md` is dated 2026-11-21 and is not part of the gated document.

### 5.2 The proposed sentences (proposed, not applied)

> **PROPOSED AMENDMENT B-1 — prospective; `applied = false`.**
> Insert into **W-1.3**, immediately after the `benchmark-bounded` clause of C-04:
>
> > *"The linear-trend and persistence comparators are a **humility floor**, not a dynamic test: losing to the 4.35 pp trend says only that the A1 anchor class adds no predictive content over extrapolation, and beating it would have said no more about dynamics — the programme's dynamic claims rest on transitions, asymmetries, crossing timing and distributional change, none of which a level benchmark can supply."*

> **PROPOSED AMENDMENT B-2 — prospective; `applied = false`.** Optional status line for the write-up's metadata table:
>
> > *"Benchmark frame: the trend/persistence comparators are stated as a humility floor; this sentence is a prospective amendment, changes no number, label or verdict, and `WRITE-UP-GATE: PASS` stands as issued on the un-amended document."*

**Why B-1 is safe to add.** It is a **scope sentence**, not a new claim: it says *less* about *narrower* objects, which is what the write-up's own discipline permits (D168's headline rule — D77 **applied, not amended**). It carries **no number** (the only figure it mentions, 4.35 pp, is already in C-04 with its stored value), **no label change**, **no verdict change**, **no new cell**, and **no direction or causal claim**. It cannot strengthen the phase's claim; it can only stop a reader from over-reading the benchmark.

**Why it is proposed rather than applied.** The write-up is gate-passed and frozen; editing it after the gate would make the gate a formality, and the debug licence (PRE_DECLARATIONS §4) forbids retro-editing. Approval is the user's, and the amendment takes effect only at the next authorised editing pass.

### 5.3 What approval would and would not change

| would change | would not change |
|---|---|
| the **reading** of the benchmark sentence (floor, not dynamic test) | any number, range, cell or hash in the write-up |
| one inserted scope sentence in W-1.3 (and optionally a status line) | `WRITE-UP-GATE: PASS` as issued on the un-amended document |
| nothing else | the phase verdict `PARTIAL / DESCRIPTIVE / EQUIVALENT` (D76/D77), the closed line (D150/D154/D167), any park, any label, any decision |

---

## 6. Limits of this memo

1. **No new numbers.** Every number above is a quotation from a delivered file (Appendix A) or sits inside a sentence quoted from the write-up; nothing was computed, and no value was derived here.
2. **No model run, no re-run, no re-score, no reproduction claim.** The memo reads files; it executes nothing. Where it says a result "reproduces" or "does not reproduce", it is quoting the delivered verdict word, not asserting one.
3. **No causal and no direction claim.** `D63` stays **`UNABLE as to cause`**; κ stays **`WINDOW-ONLY`**; the equivalence map makes no direction claim; the theory frame is **theory only**.
4. **The count of ten is a scope choice** (§3.5): three adjacent on-disk results are excluded with reasons, and the classifications would not change if they were added — HKG has **no result**, ECI is associational, WT4 is a null.
5. **The `DYNAMIC` / `FLOOR-ONLY` binary is coarse by design.** The `dynamic grade` column in `BENCHMARK_INVENTORY.csv` carries the four distinct ways a dynamic-type object falls short; a reader who needs the nuance should use that column, not the binary.
6. **This memo is `DEBUG` and `PROSPECTIVE`.** It is an audit note on a framing, not a decision, and it has no verdict authority.

---

## 7. Handoff packet (for the stronger reviewer, Opus/Sol)

**`LABEL: DEBUG`** · **status `PROSPECTIVE`** · addressee: **a stronger reviewer (Opus/Sol)** · appended under
[`PRE_DECLARATIONS.md`](../PRE_DECLARATIONS.md) §6 (**AMENDMENT 1**, sha256 `7d8bade9…`; the contract v1 hash cited in
this memo's header is `748335cf…`, and both are recorded in §7.8) · **no new number, no new cell, no re-score, no
reproduction claim, no causal claim, no direction claim** · the gate-passed write-up is **not edited**.

**What §7 is, and what it is not.** §0–§6 answer the benchmark question this cell was dispatched for, in three tasks;
**§7 does not revise them**, and §0's "three things" sentence stands for §0–§6. §7 is the **packet**: the four lists
the user asked for — **(a)** the paper's claims quoted line by line against the delivered record, **(b)** one line per
delivered result with its label, **(c)** the open questions live on disk, **(d)** the benchmark critique — laid out so
that a reviewer who was not in this record can check every line against a file. It carries no verdict, no new evidence,
and no answer to the question it ends with (§7.5 Q-7).

### 7.1 Handoff terms (recorded, not argued)

| # | term | as recorded | status |
|---|---|---|---|
| **T-1** | **the experiments may have to be redesigned** | the user's view, relayed by the Lead with AMENDMENT 1 (2026-11-21) and recorded in [`PRE_DECLARATIONS.md`](../PRE_DECLARATIONS.md) §6 | **the user's view, recorded** — §7 does not argue it, answer it, or act on it (§7.5 Q-7); nothing in this packet licenses a redesign, and a redesign would need a new predeclaration and a Council decision (D154's re-entry rule; D167 closed the experiment programme at **0 new cells**) |
| **T-2** | **the packet is for a stronger reviewer** | Opus/Sol, by the Lead's relay of the same amendment | **`PROSPECTIVE`** — written to be checked, not to persuade; every claim below names its file and, where a number appears, its column or section |
| **T-3** | **the gate-passed write-up is not edited** without the user's approval | [`PHASE_WRITEUP.md`](../../../lit/PHASE_WRITEUP.md) sha256 `d0820eb8…`, gate `WRITE-UP-GATE: PASS` (this link goes up three levels; the `../../lit/…` form in this memo's header does not resolve from this directory — recorded, not patched) | **`APPLIED`** (the constraint) — §7 quotes the write-up and edits nothing; its sha256 is re-checked at write time (§7.8); any change to it remains the prospective amendment **B-1** (§5.2), `applied = false` |

*Table caption (A-1 form):* `DEBUG` terms table; labels `DECLARED` (the terms) + `DEBUG`; objects: this packet; no κ
window; status `PROSPECTIVE`. No term is a decision, and none is a claim about the world.

### 7.2 Where the paper is, and how its lines are pinned

*(This subsection also answers the locating instruction: `00_handoff/papers/02_october_massification.md`.)*

**Located — but not where the instruction assumes.** The live programme root
(`…/massification_live/experiments/massification-2026-11-20/`) has **no `00_handoff/` and no `01_sources/` directory**;
its only handoff-named file is `10_massification/HANDOFF_expert-council.md`. The handoff tree that the programme's own
documents point to (`PROVENANCE.md` line 13; `02_lit/MANUSCRIPT_COMPARISON.md` line 9; `RESULTS_README.md` §5) sits one
bundle over, in the working copy whose paths those documents quote:

```
/Users/treymenefee/Library/Mobile Documents/com~apple~CloudDocs/Downloads/DeepSeek/
    massification_2026-11-20/00_handoff/papers/02_october_massification.md
```

**377 lines · 84,592 bytes · sha256 `1138d453a79243f573b57f971369a61f598aecc6f4882f7ff052fd1ea90228cf`.** That is exactly
the hash recorded for `papers/02_october_massification.md` at line 9 of that tree's own `00_handoff/MANIFEST.sha256`,
where it verifies `OK`, and it is byte-identical to the `massification_2026-11-20_RESTORED` copy. The line count matches
the programme's own two citations of the file ("377 lines").

**How the lines are pinned.** Every line number in Table 7.1 is a line number in **that** file at **that** hash. The
quoted text was taken **mechanically from the file by offset, not retyped**, so a quotation can be checked by
`sed -n 'Np'` on the same file. Lines 1–377 include the notes block (lines 311–373) and the reference stub (377); a
reviewer must count in the file, not in a rendered PDF.

**The fallback was not needed.** The instruction's fallback — if the file were absent, list the claims from the
write-up's W-1/W-2 instead — is **not used**: the paper was located and hash-verified, so the claims in Table 7.1 are
the **paper's own**, not the write-up's.

**What the paper's models are, and are not, in this record.** The paper formalises its account in two agent-based models
(`massabm`, the case model; `triad`, the three-actor model; paper line 371, note `[^code]`). Their **code** sits in the
read-only source bundle (`01_sources/massification_project`, per `RESULTS_README.md` §5). **No `massabm`/`triad` output
is among this phase's adjudicated results**: the phase's delivered record is `10_massification/` — the A1 anchor class,
model2, the four registers, the closed generator line — plus the write-up. That distinction is load-bearing for Table
7.1: a paper claim can be **unshown by this record** without being wrong, and several are exactly that.

### 7.3 (a) The paper's claims, quoted line by line — SHOWN / PARTIALLY SHOWN / NOT SHOWN

**The three labels, exactly.**

- **SHOWN** — a **delivered programme result** establishes the claim (or the observed fact it asserts), and the file +
  column/section is cited in the row.
- **PARTIALLY SHOWN** — a delivered result establishes **part** of the claim, or establishes it for a **sibling object**
  whose difference is named in the row.
- **NOT SHOWN** — **no delivered result establishes it.** This is an evidential statement about **this record**; it is
  **not** a statement that the claim is false, and §7 has no basis for the latter and makes no such judgement.

**Table 7.1 — the paper's claims, with their lines, statuses and evidence.** *(Quotations verbatim; `[…]` marks a cut
inside a line. Line numbers as §7.2.)*

| claim | line | quoted claim (verbatim) | status | what the delivered record has (file · section/column · decision) | reading note |
|---|---|---|---|:---:|---|---|
| **P-01** | L8 | "Credential pipelines deepen even when their absolute returns compress. Households keep investing in schooling after the wage premium has begun to fall, which simple human-capital theory does not predict." | **NOT SHOWN** | `PHASE_WRITEUP.md` W-1.3 (C-04): all 12 arms carry `scaling_verdict = FAIL` in `anchor_table.csv`, so the delivered class does not generate the positive income-scaling sign; no observed wage-premium or household-investment series is on disk (`04_data/CLAIM_VERIFICATION.md` §7 item 2: PSA FIES/APIS/LFS microdata blocked) | an observed regularity the paper asserts; the delivered negative is about a model class and establishes neither the premise nor its denial |
| **P-02** | L8 | "A floor on its own produces persistence and exclusion: it keeps families in the pipeline and shuts those below it out of formal work, but it does not make them invest more as returns fall." | **NOT SHOWN** | no floor-vs-ranking ablation among the delivered results; the paper's own ablation table (lines 130–137) is `massabm` output, and no `massabm`/`triad` output is in this phase's record; the nearest delivered object, C-06 (W-1.4), does not test a floor against no floor | the floor/race separation is the paper's central mechanism, and it is precisely what this record did not instrument |
| **P-03** | L8 | "The ranked race above the floor produces intensification, provided adolescence is cheap and schooling either raises pay inside formal jobs or stays opaque to employers." | **NOT SHOWN** | same as P-02; C-06 (W-1.4) reports that capacity timing is not credited on the crossings, but that is a statement about the programme's 12 arms, not a test of the race | the claim's conditions (cheap adolescence; schooling pays inside formal jobs or stays opaque) are not objects on this disk |
| **P-04** | L8 | "Inside a ranked queue, the floor's distinct contribution is its upward movement, which drives investment beyond what a stable queue produces." | **NOT SHOWN** | C-06/W-1.4 equivalence and the R13 forced-ID null: the delivered map does not discriminate `capacity_gated` from `law_only` (ties on crossings in 2 of 3 rivals), so the floor's *movement* contribution is **not identified** on this record | an identification null is not a disproof; the row records that the claim was not tested, and why |
| **P-05** | L147 | "In the case model, better-off households' college entry rises as degree holders' absolute income falls, across scenarios of formal-job growth (a slope of about −0.09), while in a competitive skill-price world it falls steeply (+0.55)." | **NOT SHOWN** | the claim is the case model's own slope (`massabm`); the delivered class returns the opposite sign verdict (C-04 `FAIL`), which is a failure of *this* class; no check and no re-run of `massabm` is performed here (D150/D154 forbid re-entry) | the −0.09 / +0.55 pair is the paper's sharpest discriminating claim and has no delivered counterpart |
| **P-06** | L164 | "The two accounts give opposite answers on the same outcome. In the surplus model, graduates take formal slots that diploma holders used to fill: diploma holders' chance of formal work falls by about 16 points, and their absolute income falls slightly." | **NOT SHOWN** | no graduate-supply-shock cell was delivered; the record's shock-shaped object is the D63 residual split (C-19–C-22, `D63 UNABLE as to cause`), an accounting decomposition with no counterfactual | the paper's own design (line 153) is a pre-phase `massabm` run |
| **P-07** | L170 | "Employers follow rather than lead." […] "A minority of credential-reading firms suffices: barring three-quarters of firms from reading credentials leaves the pipeline intact." | **NOT SHOWN** | no firm-adoption or sequencing object among the delivered results; the user's theory frame is carried as `DECLARED-THEORY` (C-34/W-6.4), never as evidence | — |
| **P-08** | L172 | "Persistence comes from redundancy, not lock-in. Half of any actor's gain can be removed with little effect, and only the households' leg gives way before removal is complete, between half and three-quarters." | **NOT SHOWN** | no knockout/redundancy test in the delivered record; the closed generator line's repair-in-force check (D150) is a consistency check on a different object | — |
| **P-09** | L176 | "In the case model, 93 percent of licensure-board takers buy review, against 30 percent at the elite admission exam and 5 percent at the basic diploma." | **NOT SHOWN** | shadow education was demoted at reorientation and no tutoring series is on disk (`04_data/CLAIM_VERIFICATION.md` §7 items 3–4); no gate-clustering cell was delivered | this is the paper's Prediction 3, and it has the weakest data position in this record |
| **P-10** | L180 | "In the three-actor model, a state that funds schooling beyond primary for fiscal reasons raises attainment, but on its own books it ends up behind a state that funds only primary and taxes the household-financed attainment above it." | **NOT SHOWN** | no state-ledger cell among the delivered results; P5 remains a research proposition (paper line 200) and D167 issued 0 new cells | — |
| **P-11** | L186 | "Both models were built by the same hands with the same household logic, so their agreement is weaker evidence than two independent implementations would be; an independent re-implementation from the verbal specification would be worth more than further runs." | **PARTIALLY SHOWN** | the programme did perform the independent re-implementation the sentence asks for — the A1 anchor class (`anchor.py`) and the closed `v1.5`–`v1.7` line — and it did **not** agree with the observed path: C-04 (all 12 arms `FAIL`), C-02 (0/33 against the ≥17/33 bar), D150/D154 | a methodological claim, so 'partially shown' means: the act was performed and it produced a discriminating negative — not that any paper number was confirmed |
| **P-12** | L192 | "Where foreign readers or binding rules set part of the floor, extensions of the pipeline should respond to material changes in the cost of the existing structure (a binding equivalence rule, a recognition threshold, a mobility agreement, a fiscal or migration constraint) with step-change timing, rather than to normative pressure with smooth cumulative adoption." | **NOT SHOWN** | no documentary corpus on disk — the paper itself names it as the missing evidence (line 250); the programme's C2 re-opener (fixed-behaviour crossings within ±5 y) is a crossing-count instrument (C-14/C-15), not a reform-timing test, and a re-opener is not a delivered result (D76) | — |
| **P-13** | L198 | "The test needs first-time entrants by age and prior qualification, not enrollment stocks or gross enrollment ratios." | **PARTIALLY SHOWN** | EXP-21 (C-08/W-2.1): completion and GER are one scale in 4 of the 12 frozen cells and not interchangeable in the other 8 (6 `NOT-INTERCHANGEABLE`, 2 `THIN`), and all four interchangeable cells still cross 1.0; `ger_secondary` may never stand in for a level GER (C-10/W-2.3) | the register supports the *instrument* premise; the re-entry test itself was never run, and the participation object has no observed counterpart (C-17/W-3) |
| **P-14** | L214 | "Late-1990s surveys put high-school completion among the poorest third at roughly 40 percent against 70 to 75 percent for non-poor households." | **NOT SHOWN** | PSA microdata blocked (`04_data/CLAIM_VERIFICATION.md` §7 item 2); no income-gradient series on disk; the data asks are `HELD` (C-31, 14 items) | — |
| **P-15** | L216 | "In the case model, comparing the first ten twelve-year cohorts with a no-reform counterfactual, the reform cuts full-cycle completion by about 22 points in the poorest quintile and about 2 in the richest, and the rich-poor gap roughly doubles, from 0.20 to 0.41, with an aggregate cost near 6.5 points." | **NOT SHOWN** | the paper's own simulation result, which the paper scopes itself (line 216: observed reform effects by income 'remain to be estimated'); no reform-incidence cell was delivered, and the observed 2024 completion values (C-09) are a different object that may not be used as its counterpart (W-2.2) | — |
| **P-16** | L263 | "The case model reproduces the dip but not the recovery, and adding returning adults and free tuition narrows the gap without matching it." […] "Prediction 4 states what would separate them." | **NOT SHOWN** | the delivered re-entry object is identity-null: C-17/W-3 `NO-OBSERVED-COUNTERPART`, `WITHHELD-NO-IDENTITY`, `comparison_performed = FALSE`; the pairs end 2017/2015 (C-18) | the paper's own caution — re-entry and several rival readings are indistinguishable on this evidence — is exactly the state of the record |
| **P-17** | L26 | "a reform, the 2013 extension from a ten-year to a twelve-year basic cycle, that raised the floor by law after sixty-four years of recommendations had failed to." | **PARTIALLY SHOWN** | policy fact verified — `04_data/CLAIM_VERIFICATION.md` §6 ('Verified as policy fact; wording note': RA 10533, 2013); 'raised the floor' is the paper's mechanism reading, and the sixty-four-year count is arithmetic on the paper's own timeline (lines 228–242), not a delivered result | the only row where a delivered file establishes the asserted fact |
| **P-18** | L277 | "The first two are supported by the models, with the qualification that inside a ranked queue the floor's contribution is its movement, and are specified for testing; the last two are proposals with tests attached." | **NOT SHOWN** | no delivered test of Prediction 1 or Prediction 5 exists (D167, 0 new cells), so the record cannot confirm 'supported by the models' — that phrase refers to `massabm`/`triad`; it is consistent with the paper's own classification and contradicts nothing | — |

*Table caption (A-1 form):* `DEBUG` packet table; quoted text `DECLARED` (the paper's words) + status `DERIVED`
(this memo's adjudication of *coverage*, not of truth); objects: the paper's claims and this record's results; no κ
window; status `PROSPECTIVE`. Every status is a statement about **what this record established**, and no status is a
verdict on the paper.

#### 7.3.1 The counts

| status | count | rows |
|---|---:|---|
| **SHOWN** | **0** | — |
| **PARTIALLY SHOWN** | **3** | P-11, P-13, P-17 |
| **NOT SHOWN** | **15** | P-01–P-10, P-12, P-14–P-16, P-18 |
| **total** | **18** | the abstract (4), the mechanisms and the two models (7), the five predictions (2), the case (4), the conclusion (1) |

**Reading the count.** **0 of 18 SHOWN** is the packet's most important negative, and it has two causes, both structural
rather than accidental. (i) The paper's own model outputs are `massabm`/`triad` artefacts, and this phase adjudicated
**other** objects (the A1 anchor class, model2, four registers). (ii) Five of the paper's claims are predictions whose
**data are not on disk** — first-time entrants by age; the dated justification corpus; income-gradient microdata; a
graduate-supply shock; a tutoring series — which is the same data-gap bucket D167 used to close the programme. A
reviewer should read **0 of 18** as *"this record never set out to test the paper"*, **not** as *"the paper failed"*.

### 7.4 (b) What each delivered result shows — one line each, with its label

**The labels, exactly.** Five words, one per row, from this memo's inventory vocabulary:

- **DYNAMIC-type** — the *object under test* is a crossing, a transition, an asymmetry, a lag, or a placement over
  time. It does **not** mean a dynamic was identified.
- **FLOOR-ONLY** — a level/benchmark object or a static cross-section: no dynamic content.
- **REPRESENTATION** — a capability statement: what the class can represent.
- **BOUNDED** — a bounded decomposition, with its bounds reported.
- **NULL** — an identification null, an identity null, or **no result at all**.

The memo's own binary classification (Table 3.1: `DYNAMIC` / `FLOOR-ONLY`) is carried in the second column so the two
vocabularies cannot be confused. The handoff label is the row's **characteristic** label; where the two differ, the
difference is the point (D63 is `DYNAMIC` in the binary and **BOUNDED** here, because its bounds are what the result
actually delivers).

**Table 7.2 — the ten results, one line each.**

| # | result (object) | memo class (Table 3.1) | handoff label | what it shows, in one line | evidence |
|---|---|---|---|---|---|
| **B-1** | A1 anchor-class negative (12 arms) | FLOOR-ONLY | **FLOOR-ONLY** | the class adds no predictive content over extrapolation on this record: 12 arms, fit 1.047492271754753–3.2916863270693772, holdout 4.014780434743067–6.122199101442962, against `naive_trend` 4.352883341604888 (persistence 8.599852941176476), all 12 `FAIL` the scaling verdict | W-1.3/C-04; `anchor_table.csv` (`fit_mae`, `hold_mae`, `scaling_verdict`); `calibration_table.csv` (`naive_trend`, `naive_persistence`) |
| **B-2** | observational equivalence / forced-ID null | FLOOR-ONLY | **NULL** | the capacity-timing claim is not credited and the push–pull direction is not identifiable: `capacity_gated` ties `law_only` on crossings in 2 of 3 rivals; forced-ID 1.00 against a declared bar of 0; equivalence 0.07 against <0.34; `truth = OUT` → `best` ∈ {`S`, `C`} in 5 of 5 | W-1.4/C-06; R13; `recovery.csv`; `A5B_REPORT.md` |
| **B-3** | upper-secondary asymmetry | DYNAMIC | **DYNAMIC-type** | the observed ordering (primary ≥90 in 2017, lower ≥90 in 2024, upper never ≥90 by 2024) is not reproduced by any arm — M2 0/12 clean, M3 12/12 in-window with two post-window overshoots — and the instrument is a placement count (9/33) whose first element was never recorded (C8 gap) | C-07/C-14/C-15; W-2.7; `anchor_table.csv` (`M2`, `M3`); `observed_path_A17.csv` |
| **B-4** | EXP-7 path result | DYNAMIC | **DYNAMIC-type** | 9/33 in band against the 17/33 bar, and the 2020 split (22 cells → 2 in band; 11 cells → 7) says the panel is a 2021–2024 placement, not a path | `PATH_COMPARISONS.csv`; `FINDINGS.md` §2 (`ENDPOINT-ONLY`); W-1.2 |
| **B-5** | EXP-21 CONV-REG | FLOOR-ONLY | **FLOOR-ONLY** | a same-year cross-section on `T = completion / GER`: 4 of 12 cells `INTERCHANGEABLE`, 6 `NOT-INTERCHANGEABLE`, 2 `THIN`, and all four interchangeable cells still cross 1.0 — no time-evolution object | C-08/W-2.1; `CONV_REG.csv`; D160/D164 |
| **B-6** | EXP-22 PART-MARGIN-DESC | FLOOR-ONLY | **NULL** | historical gross−net spans (primary 2.196578–14.627307 pp; lower 17.412040–29.239540 pp; upper 46.062110–51.704530 pp `THIN`) with the identity test failed at all three levels: `NO-OBSERVED-COUNTERPART`, `WITHHELD-NO-IDENTITY`, `comparison_performed = FALSE`, pairs ending 2017/2015 | C-16–C-18/W-3; `PART_MARGIN_DESC.csv`; `OBJECT_IDENTITY_AUDIT.csv` |
| **B-7** | EXP-23 D63-BOUNDS | DYNAMIC | **BOUNDED** | a t−3 accounting split (58.6008386858443 % / 41.3991613141558 %) that is bounded: B1 `OUTSIDE` (+4.628621 pp), B2/B3 `INSIDE`, `BOUNDS-EDGE` = 1 of 3 outside, no counterfactual, `D63 UNABLE as to cause` | C-19–C-22/W-4; `D63_BOUNDS_RESULTS.csv`; D153(xiii) |
| **B-8** | EXP-24 KAPPA-WRITE | DYNAMIC | **DYNAMIC-type** | a transition-ratio register (PHL 0.949135, KOR 0.989758, KHM 0.594984, CHN 0.722222) whose own predeclared test returned `WINDOW-ONLY`; KOR clears the stationarity bars and then misses 0/3 hold-out cells, so κ is never written forward | C-23–C-27/W-5; `KAPPA_WRITE_REGISTER.csv`; D138 |
| **B-9** | v1.5–v1.7 representation | FLOOR-ONLY | **REPRESENTATION** | representation-only capability: upper unfilled 15/15, both-level queue 30/30, strict both-level coexistence 0/15, 0/33 against the ≥17/33 bar, crossings 1/3 — and single-tier (D153(ix)) | C-02/W-1.1; `v1_7_checks.csv`; `representation_cells.csv`; D150/D154 |
| **B-10** | HKG transfer | (outside the ten — §3.5) | **NULL** | no HKG result exists: the construct test failed (band max 2.685005 pp; crossings 3 y and 2 y apart) and the transfer is `BLOCKED-MEASURE(SR-1)` — a measure block, not a finding | `hkg_transfer_2026-11-20/HKG_H1_OUTCOME.md`; C-31; D153(vii) |

*Table caption (A-1 form):* `DEBUG` packet table; labels: `DEBUG` classification + inherited per row (`SIM`, `OBS`,
`DERIVED`); objects as printed (O-1, EXP-21…EXP-24 rows, the closed `v1.5`–`v1.7` family); **no κ window is attached to a
row that does not quote κ** — B-8 quotes κ values and carries its register label `WINDOW-ONLY`, never a projection;
status `PROSPECTIVE`. Classification is this memo's, not a new verdict: every line quotes a delivered verdict word.

**The counts.** Across the nine inventoried results listed here, the memo's binary reads **4 `DYNAMIC` / 5 `FLOOR-ONLY`**
(memo row 10, the declared theory, is not in the packet's list). The five handoff labels read **3 DYNAMIC-type**
(B-3, B-4, B-8) · **2 FLOOR-ONLY** (B-1, B-5) · **1 REPRESENTATION** (B-9) · **1 BOUNDED** (B-7) · **3 NULL** (B-2, B-6,
B-10, of which B-10 is NULL because no result exists). And **0 of 10 identify a dynamic** under the four conditions of
§4.1 — which is the count (d) is about.

### 7.5 (c) The open questions live on disk

Seven, in the order a reviewer should take them. Each names the object, its shipped label, and what is open.

**Q-1 · D63's cause.** The residual is `14.974746704101562` pp and splits at the **declared t−3 pair** into
`58.6008386858443 %` pipeline / `41.3991613141558 %` transition; at the contemporaneous lower value the split is
`−0.14544291665697634` / `1.145442916656977`, and it must be cited with that sentence. B1 is `OUTSIDE` (+4.628621 pp),
B2/B3 `INSIDE`, so `BOUNDS-EDGE` = **1 of 3 outside** and nothing else. **Open:** what produced either channel —
`D63 UNABLE as to cause`; no structural sentence about the upper-secondary ceiling may be written in **either**
direction (C-19–C-22; D153(xiii); W-4).

**Q-2 · κ dynamics.** The transition ratio is the right *kind* of object, and its own predeclared test returned
**`WINDOW-ONLY`**: PHL 0.949135 (hold-out 2/2), KOR 0.989758 (**0/3** hold-out — the counter-example), KHM 0.594984
(1/2), CHN 0.722222 (0 cells). **Open:** how a transition-rate object could be estimated and evaluated in **disjoint**
windows, given that KOR clears every stationarity bar and still fails out of window. Nothing may be written forward
(C-23–C-27, C-30; D138; W-5).

**Q-3 · the participation object's identity.** The spans are historical (primary n = 30, `2.196578–14.627307` pp;
lower n = 4, `17.412040–29.239540` pp; upper n = 2 `THIN`, `46.062110–51.704530` pp), the identity test finds **0**
matching register lines, and the verdict is **`NO-OBSERVED-COUNTERPART`** with placement `WITHHELD-NO-IDENTITY` and
`comparison_performed = FALSE`. **Open:** whether an observed object *with the model's numerator and denominator*
exists at all — the record can say only that none among the audited candidates does (C-16–C-18; W-3).

**Q-4 · HKG measurement.** The construct test **failed** (band max 2.685005 pp; crossings 3 y and 2 y apart) and the
transfer is **`BLOCKED-MEASURE(SR-1)`**: there is **no HKG result**. **Open:** the measure itself — the two-part re-entry
condition plus a new Council decision (C-31; D153(vii); W-6.1).

**Q-5 · the 12-arm holdout-vs-trend reading hazard.** The arm-level cell for `complementary · capacity_gated` is
**4.014780434743067** (`anchor_table.csv` column `hold_mae`), numerically **below** the trend's **4.352883341604888**
(`calibration_table.csv` column `naive_trend`, `iso = PHL`), while the write-up records the **class** as losing to that
trend. The two cells come from **different tables and different objects** (per-arm anchor fit vs the rival-level
calibration comparator). This memo **does not re-score the comparison** and does not call the shipped sentence wrong; it
records the hazard because a floor verdict that can move with one arm is fragile as well as level (§3.4 item 1;
`RUN_MANIFEST.json` `reading_hazards` H-1). **Open:** whether the arm-level cell may be read against the trend at all —
a question for the stronger reviewer, not a correction made here.

**Q-6 · the ceiling-cap question, being fixed in this debug run.** `completion_uis ≤ 1.0` binds in **35 of 6,720** cells
on v1.3 and **35 of 6,720** on v1.2, and in **0 of 6,720** on A17; with it, `m` reads `CONSTANT` on A17
(`8.8395202269e-10`) and `NOT-CONSTANT` on v1.3/v1.2 (`4.7043695535e-02`) — i.e. **constant exactly on the panel where
the cap never binds** (C-13; `M_CONSTANCY.csv`). The audit enumerates **34** clamp sites and classifies **30** as
declared conventions, **1** as an implementation artefact and **3** as undetermined, with **1** site for the fix, and
reports that **none of the 35 capped cells is a legitimate CR > GER case** (`0 of 70` rows; `CAP_AUDIT.md` §0, §1.2).
**Open:** whether the v1.3/v1.2 non-constancy is **cap-induced or real**, and whether the repair moves any level
sentence — Agent 2's re-run question (`PRE_DECLARATIONS.md` §3 item 2), not this memo's. The measure-aware rule holds
throughout: **GER may exceed 100, NER ≤ 100 is definitional, and a UIS completion rate's denominator is the older cohort
and may exceed GER** (AMENDMENT 1).

**Q-7 · the user's question: may the experiments have to be redesigned?** Recorded as **the user's question**, with the
packet's material bearing on it: **0 of 10** inventoried results identify a dynamic (§4.2); **0 of 18** paper claims are
shown outright by this record (§7.3.1); the four dynamic-type objects fail on **D-2** (window-bound) and **D-4** (their
falsifiers are level bars); D167 closed the experiment programme at **0 new cells**; and D154's re-entry rule requires a
**measured** object currently `HELD` **and** a new Council decision. **§7 does not answer it.** An audit note has no
authority to redesign anything, and the counts above are equally consistent with a redesign and with a narrower
statement of what this record supports — that choice is the reviewer's and the user's, not this memo's.

### 7.6 (d) The benchmark critique, in the form the reviewer needs it

1. **The hierarchy.** Persistence and linear-trend comparators are a **humility floor, not a dynamic test**: beating or
   losing to a trend says only that the model adds, or fails to add, **predictive content over extrapolation**. It is a
   **necessary benchmark only**, never sufficient evidence of a dynamic; the programme's dynamic claims must rest on
   **transitions, asymmetries, crossing timing, and distributional change** (§2.1). Four independent reasons are in §2.2,
   and the shipped write-up's three benchmark sentences are floor statements that the write-up itself scopes correctly
   (§2.3).
2. **The count.** Of the ten inventoried results, **0 of 10 identify a dynamic** under the four-condition test of §4.1:
   **D-1** a dynamic-type object (a transition, crossing time, asymmetry, or distributional shift — not a level or a
   level's error); **D-2** estimated in one window and evaluated in a **disjoint** window; **D-3** an explicit
   counterfactual **or** a distributional-shift test; **D-4** a predeclared falsifier **that is not a level bar**. The
   four dynamic-type objects fail on **D-2** (they are window-bound) and **D-4** (their falsifiers are cell counts and
   holdout errors) — the two conditions "line goes up" cannot supply (§4.2).
3. **The proposed amendment.** **B-1** is prospective and **`applied = false`**; it inserts one scope sentence after the
   `benchmark-bounded` clause of C-04 in W-1.3:

   > *"The linear-trend and persistence comparators are a **humility floor**, not a dynamic test: losing to the 4.35 pp
   > trend says only that the A1 anchor class adds no predictive content over extrapolation, and beating it would have
   > said no more about dynamics — the programme's dynamic claims rest on transitions, asymmetries, crossing timing and
   > distributional change, none of which a level benchmark can supply."*

   **B-2** is the optional metadata status line. Neither is applied; this packet applies neither; the gate-passed
   write-up is edited by neither (§5.2–§5.3).
4. **What would not count** (§4.4): a better holdout MAE; a second extrapolative comparator; a re-scored 33-cell count;
   a κ value read forward; a synthetic PASS read as confirmation of the theory frame; or "the line went up" restated in
   transition vocabulary.

### 7.7 Reading order for the reviewer (six files, in order)

| # | file | what it settles |
|---:|---|---|
| 1 | `00_handoff/papers/02_october_massification.md` (handoff tree; `1138d453…`) | the paper's claims at their line numbers — Table 7.1 is checked against this file only |
| 2 | `10_massification/lit/PHASE_WRITEUP.md` (`d0820eb8…`) and its gate (`cee5b0c8…`) | what the programme actually put its name to: W-1…W-6, C-01…C-36, `WRITE-UP-GATE: PASS` |
| 3 | `08_council/DECISIONS.md` — D76/D77, D138, D150/D154, D153, D160, D164–D170 | the rulings that bound every sentence: labels, parks, the closed line, the write-up order |
| 4 | `10_massification/model/anchor_out/anchor_table.csv` + `10_massification/model/calib/calibration_table.csv` | the 12 arms and the trend comparator — Q-5's reading hazard lives exactly here |
| 5 | the four registers: `CONV_REG.csv`, `PART_MARGIN_DESC.csv`, `D63_BOUNDS_RESULTS.csv`, `KAPPA_WRITE_REGISTER.csv` | the four delivered objects behind (b): one verdict each, with its columns |
| 6 | `10_massification/extensions/model_debug_2026-11-21/cap_audit/results/CAP_AUDIT.md` | the cap audit (Q-6): the only file on disk that enumerates the 35 cells |

### 7.8 Provenance for §7, and the limits of §7

| thing quoted in §7 | file (path from programme root, unless stated) | column / section |
|---|---|---|
| paper lines 8, 26, 147, 164, 170, 172, 176, 180, 186, 192, 198, 214, 216, 263, 277; 377 lines; hash | `00_handoff/papers/02_october_massification.md` (handoff tree, §7.2) | line numbers as printed; hash from `00_handoff/MANIFEST.sha256` line 9 |
| fit 1.047492271754753–3.2916863270693772; holdout 4.014780434743067–6.122199101442962; `complementary · capacity_gated` 4.014780434743067 | `10_massification/model/anchor_out/anchor_table.csv` | `fit_mae`, `hold_mae`, `scaling_verdict` |
| 4.352883341604888; 8.599852941176476 | `10_massification/model/calib/calibration_table.csv` | `naive_trend`, `naive_persistence`, `iso = PHL` |
| 4/12, 6 `NOT`, 2 `THIN`; all four interchangeable cells cross 1.0; 9/33, 13/33; 22 → 2, 11 → 7 | `…/conv_reg_2026-11-20/results/CONV_REG.csv`; `…/repro_path_2026-11-20/results/PATH_COMPARISONS.csv` | `verdict`, `n_pairs`, `T_min`, `T_max`, `crossing_year`; `within_5pp` (V39–V46, V75) |
| spans 2.196578–14.627307 / 17.412040–29.239540 / 46.062110–51.704530; `THIN`; 0 matching lines | `…/part_margin_desc_2026-11-20/results/PART_MARGIN_DESC.csv`; `…/OBJECT_IDENTITY_AUDIT.csv` | `span_min_pp`, `span_max_pp`, `thin`, `identity_test`, `placement`, `n_matching_lines` (V52, V54) |
| 14.974746704101562; 58.6008386858443 / 41.3991613141558; −0.14544291665697634 / 1.145442916656977; +4.628621 | `…/d63_bounds_2026-11-20/results/D63_BOUNDS_RESULTS.csv` | rows S1, S8, S9, X1/X2, B1–B3; `value_num`, `outcome` (V57–V62) |
| κ 0.949135 / 0.989758 / 0.594984 / 0.722222; KOR 0/3 | `…/kappa_write_2026-11-20/results/KAPPA_WRITE_REGISTER.csv` | `kappa_full`, `holdout_within`, `holdout_violation_years` (V64) |
| 15/15, 30/30, 0/15, 0/33, ≥17/33, 1/3; forced-ID 1.00, equivalence 0.07, `truth = OUT` 5/5 | `…/synthetic_2026-11-20/generator_v1_7_partrepair/results/`; `10_massification/model2/runs/recovery.csv` | rows S1–S3; `truth`, `best`, `equiv` (V75; R13) |
| HKG band max 2.685005 pp; crossings 3 y / 2 y; `BLOCKED-MEASURE(SR-1)` | `…/hkg_transfer_2026-11-20/HKG_H1_OUTCOME.md` | §The ruling |
| 35 of 6,720 (v1.3 35, v1.2 35, A17 0); 34 sites / 30 / 1 / 3; 0 of 70 CR > GER | `10_massification/extensions/model_debug_2026-11-21/cap_audit/results/CAP_AUDIT.md` | §0 Headline; §1.2 |
| A17 `CONSTANT` 8.8395202269e-10; v1.3/v1.2 `NOT-CONSTANT` 4.7043695535e-02 | `…/conv_reg_2026-11-20/results/M_CONSTANCY.csv` | `max_abs_dev_ratio`, `verdict` (V47) |
| RA 10533, 2013, "Verified as policy fact" | `04_data/CLAIM_VERIFICATION.md` | §6 table |

*Table caption (A-1 form):* `DEBUG` provenance table; labels as inherited per row; objects as printed; **no κ window is
attached to a row that does not quote κ** (the κ row prints its register fields); status `PROSPECTIVE`. `…/` abbreviates
`10_massification/extensions/`. No value in §7.8 was computed by this memo.

**Limits of §7 — five, stated plainly.**

1. **No number was computed here.** Every figure is a quotation from a delivered file (§7.8) or sits inside a sentence
   quoted from the paper or the write-up; nothing was derived, and §7 adds no cell.
2. **No model run and no re-run.** §7 executes nothing; it did not run, re-run or re-score `massabm`, `triad`, any
   anchor arm, any register cell, or the cap repair. The cap repair is Agent 2's, and Q-6 records the question.
3. **No reproduction claim.** "SHOWN / PARTIALLY SHOWN / NOT SHOWN" is a statement about **this record's coverage**, not
   about the world and not about the paper's truth. Where §7 says a result "reproduces" or "does not reproduce", it is
   quoting the delivered verdict word.
4. **No causal and no direction claim.** `D63` stays **`UNABLE as to cause`**; κ stays **`WINDOW-ONLY`**; the
   equivalence map makes no direction claim; the theory frame is theory only (§6 item 3 above).
5. **A contract-hash note, for the record.** This memo's header cites `PRE_DECLARATIONS.md` at sha256 `748335cf…`
   (contract v1). The contract on disk is now **`7d8bade9…`** (v1 + **AMENDMENT 1**, measure-aware), and §7 is written
   under the amended contract. No text in §0–§6 has been changed to match it; a future editing pass should reconcile
   the header citation, and this note is the record that it was noticed rather than patched.

**§7 has no verdict authority** (T-2). It is a packet: four lists, their provenance, and the limits above.

---

## Appendix A — provenance of every number quoted (quoted, not computed)

| number(s) as printed | file (path from programme root) | column / row | carried in the write-up as |
|---|---|---|---|
| fit 1.047492271754753–3.2916863270693772; holdout 4.014780434743067–6.122199101442962; the three `none` arms 1.047492271754753 / 1.318865482339633 / 1.371270727493839 (fit) and 5.875474290798293 / 5.938227008289883 / 6.111754907690532 (holdout); `M2`, `M3` vector; `complementary · capacity_gated` holdout 4.014780434743067 | `10_massification/model/anchor_out/anchor_table.csv` | `fit_mae`, `hold_mae`, `M0`–`M4`, `scaling_verdict` | V69; C-01, C-06, C-15, C-32 |
| 4.352883341604888 (trend); 8.599852941176476 (persistence) | `10_massification/model/calib/calibration_table.csv` | `naive_trend`, `naive_persistence`, `iso = PHL` | V75; C-04 |
| 9/33; 0/33; ≥17/33; crossings 1/3; 15/15; 30/30; 0/15 | `10_massification/extensions/synthetic_2026-11-20/generator_v1_7_partrepair/results/observed_path_A17.csv` (`within_5pp_A00`); `.../v1_7_checks.csv` (rows S1–S3); `.../representation_cells.csv` | as named | V75; C-02 |
| 12 cells: 4 `INTERCHANGEABLE`, 6 `NOT-INTERCHANGEABLE`, 2 `THIN`; PHL primary 0.802546–1.073853, crossing 2021; PHL upper 0.898892–1.093971, crossing 2017; PHL lower 0.746209–0.900968; KOR upper five crossings; KHM upper 2001/2008; KOR lower 2010/2017 | `10_massification/extensions/conv_reg_2026-11-20/results/CONV_REG.csv` | `verdict`, `T_min`, `T_max`, `in_band_share`, `n_pairs`, `crossing_year`, `n_crossings` | V39–V46; C-08 |
| A17 `CONSTANT` 8.8395202269e-10; v1.3/v1.2 `NOT-CONSTANT` 4.7043695535e-02; 35 of 6,720 cells | `10_massification/extensions/conv_reg_2026-11-20/results/M_CONSTANCY.csv` | `max_abs_dev_ratio`, `verdict`, `n_rows`, `n_tested` | V47; C-13 |
| primary n = 30, 2.196578–14.627307, median 10.086482; lower n = 4, 17.412040–29.239540; upper n = 2 `THIN`, 46.062110–51.704530; identity 0 matching lines | `10_massification/extensions/part_margin_desc_2026-11-20/results/PART_MARGIN_DESC.csv`; `.../OBJECT_IDENTITY_AUDIT.csv` | `n_pairs`, `span_min_pp`, `span_max_pp`, `span_median_pp`, `thin`, `identity_test`, `placement`, `n_matching_lines` | V52, V54; C-16, C-17 |
| 14.974746704101562; 58.6008386858443 / 41.3991613141558; G 0.18198490285627197; B1 97.0425841315231 vs 92.4139633178711; B2 0.9738788032543533 in [0.8891573087274445, 1.0724421619315192]; B3 [82.170551, 99.108631]; −0.14544291665697634 / 1.145442916656977 | `10_massification/extensions/d63_bounds_2026-11-20/results/D63_BOUNDS_RESULTS.csv` | rows S1, S8, S9, X1/X2, B1–B3; `value_num`, `outcome` | V57–V62; C-19–C-21 |
| κ PHL 0.949135 / −0.000704 / 2.1348 / 2/2; KOR 0.989758 / +0.002875 / 0.6354 / 0/3; KHM 0.594984 / +0.017318 / 7.4361 / 1/2; CHN 0.722222 / +0.041728 / 25.6573 / 0 cells; windows 2003–2017/2003–2024, 2005–2020/2005–2023, 2000–2017/2000–2023, 2012–2020 | `10_massification/extensions/kappa_write_2026-11-20/results/KAPPA_WRITE_REGISTER.csv` | `kappa_full`, `window_pre2021_upper`, `window_full_upper`, `slope_ratio_per_year`, `half_median_shift_pp`, `holdout_within` | V64; C-23–C-27 |
| 309 uses / 299 applied / 233 in-window / 77.9264 % / 68 barred / 132 observed / 0 load-bearing / 17 of 193 files | `10_massification/extensions/kappa_write_2026-11-20/results/KAPPA_WRITE_SUMMARY.csv` | rows `n_uses` … `corpus_files_with_kappa_token` | V63; C-28 |
| 9/33 (27.27 %); 13/33; medians −4.30 / −29.44 / −27.59; worst upper 1999 −36.62; 22 cells → 2 in band (9.1 %) −28.21; 11 cells → 7 in band (63.6 %) +0.04; verdict `ENDPOINT-ONLY` | `10_massification/extensions/repro_path_2026-11-20/results/PATH_COMPARISONS.csv`; `.../FINDINGS.md` §2 | `within_5pp`, `deviation_pp`; verdict string | not quoted in the write-up; quoted here from the delivered FINDINGS |
| forced-ID 1.00; equivalence 0.07; recovery 1.00; `truth = OUT` → `best` ∈ {`S`, `C`} in 5/5; D 4/5 | `10_massification/model2/runs/recovery.csv`; `10_massification/model2/EXPERIMENTS_M2.md` Part 4 | `truth`, `best`, `equiv` | R13; C-06 |
| WT4 exit episodes 0; gate ratio 1.889 vs same-year 0.889 | `10_massification/extensions/wt_2026-11-20/FINDINGS.md` | scoreboard row WT4 | not quoted in the write-up; adjacent |
| HKG band max 2.685005 pp; crossings 3 y / 2 y; `BLOCKED-MEASURE(SR-1)` | `10_massification/extensions/hkg_transfer_2026-11-20/HKG_H1_OUTCOME.md` | §The ruling | not quoted in the write-up; adjacent |

*Table caption (A-1 form):* `DEBUG` provenance table; labels as inherited per row (`OBS`/`SIM`/`DERIVED`); objects as printed; **no κ window is attached to a row that does not quote κ** (the κ row prints its windows); status `PROSPECTIVE`. No value in this table was computed by this memo.

## Appendix B — decisions and artefacts this memo relies on

| id | what it fixes | use here |
|---|---|---|
| **D76 / D77** | phase verdict `PARTIAL / DESCRIPTIVE / EQUIVALENT`; the honest headline rule and its barred phrasings | the floor reading must not amend either; D77's asymmetry statement is row 3 |
| **D138** | κ `WINDOW-ONLY` — not a forward constraint; KOR 0/3 hold-out | row 8; §4.3 direction 1 |
| **D150 / D154 / D167** | generator line closed at representation-only; 0 new cells; re-entry needs a measured `HELD` object + a decision | §3 row 9; §4.3 "not admissible this phase" |
| **D153(xiii)** | D63 residual split at the t−3 pair; `UNABLE as to cause`; a ceiling-cause sentence is barred in either direction | row 7 |
| **D164 – D169** | the four registers adjudicated; the write-up order W-1…W-6; the frozen gate A-1…A-8; `WRITE-UP-GATE: PASS` | §2.3, §5.1 |
| **D165(x)** | the 12-arm range correction (D-1) — fit/hold ranges over the **twelve** arms | row 1, §3.4 |
| **PRE_DECLARATIONS.md** (sha256 `748335cf…`) §2–§3 | the debug contract: the verbatim directive, the floor rule, this cell's scope | §0, §1, §5 |
| **`PHASE_WRITEUP.md` / `PHASE_WRITEUP_GATE.md`** | the shipped write-up and its `PASS` gate — quoted, never edited | §2.3, §5 |
| **`MASSIFICATION_CLOSEOUT.md`** | the D-1-corrected 12-arm range and the loss to the 4.35 pp trend | row 1 |
| **`BENCHMARK_INVENTORY.csv`** | machine-readable twin of Table 3.1 | §3 |
