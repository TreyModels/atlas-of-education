# EXP-19 PLACES-BOUND — PRE-REGISTRATION

**Experiment:** EXP-19 **PLACES-BOUND** — can the required coverage be bounded by anything observed
on disk, or is it a **declared assumption**?
**Authority:** Council brief 024 (`08_council/brief_024/SYNTHESIS_024.md` §5.4), adopted as **D145 #4, rank #4**;
the required-state inputs are **D148** (EXP-17 `SINGLE-LEVER-IDENTIFIED`); the coverage/data ruling is **D146**;
the process rules are **D147**.
**Worker:** PB, cycle 16. **Written and hashed before the script that computes any implied-coverage cell or
verdict was executed.**
**Scope of writes:** `10_massification/extensions/places_bound_2026-11-20/` only. **No other file on disk is
created, modified or moved.** All inputs are read-only. The running server is not touched. No web access.
**Labels used throughout.** On-disk ratio, enrolment, backlog and flow values = `OBSERVED`; anything computed
from them, including the required state imported from EXP-17 and every implied coverage = `DERIVED`; the norm
class sizes and every conversion assumption = `DECLARED`; the norm values are declared and **none is adopted**;
data the programme does not hold = `HELD`. **No causal claim and no direction claim is made anywhere in this
experiment.** The cell measures what the observed record can and cannot bound; it says nothing about what raises
completion anywhere, nothing about the Philippines, and nothing about policy.

---

## 0. Freeze protocol

1. This file is written **before** `code/run_places_bound.py` is executed. Its sha256 is recorded in
   `PRE_DECLARATIONS.sha256`, embedded **in the script**, and embedded in `RUN_MANIFEST.json`. The script
   **refuses to run** if the embedded value and the file's actual sha256 disagree (the v1.2 freeze pattern).
2. **No threshold, matching rule, year window, level-fallback rule, interval construction, label or precedence
   rule in §3–§7 may change after the run.** The verdict is whatever the frozen rules return. A label the analyst
   did not expect stands and is discussed in `FINDINGS.md`; it is not re-specified.
3. **No re-fit, no new parameter, no generator run, no re-scoring of EXP-13, EXP-14, EXP-16, EXP-17 or any
   delivered cell.** The only executable is this cell's own arithmetic on frozen on-disk series. `phys_cap` is not
   read as a free parameter, not changed, and not re-argued. D139 and D131 are not re-argued.
4. **No fabrication.** The probe never invents a classroom count, a school count, a cohort count, a utilisation
   rate or a quality series. Rows that are `unable` on disk stay `unable`; the HELD items in §3.3 stay HELD and
   are named. No number is chosen to make an interval contain or exclude the required state.
5. **No proxy substitution outside the declared family.** This cell *is* the one cell permitted by D146 to
   construct a proxy; the proxy is the declared conversion family in §4, it is labelled `DERIVED`, its
   distortions are stated in §4.6 and in `results/PROXY_DISTORTION.md`, and **nothing is adopted**.
6. If the frozen rules do not determine a case, the case is reported as `UNDETERMINED` with its reason in
   `results/PLACES_BOUND_RESULTS.csv`; the label is not adjusted to hide it.

---

## 1. The Council block, verbatim

> Reproduced **verbatim** from `08_council/brief_024/SYNTHESIS_024.md` §5.4 (lines 546–587). Nothing in this
> quotation is paraphrased. **The block's definitions and thresholds are the binding ones**; §2–§9 below only
> *operationalise* them and are void where they conflict with this quotation.

> ### 5.4 EXP-19 — **PLACES-BOUND**: can the required coverage be bounded by anything observed on disk? (rank **#4**)
>
> 1. **First-order link (government capacity, as measurement).** If EXP-17 identifies the lower defect as a **coverage**
>    requirement, the programme must know whether that coverage is **measurable on disk** at all — or whether it is a
>    **declared** object that must carry its own label and sensitivity. This is the D119/D135/D140 measurement question
>    in its narrowest, most decision-relevant form.
> 2. **What changes if positive vs negative.** **`PROXY-BOUNDS`** → the successor may declare its coverage path from a
>    **DERIVED** proxy with its distortion stated, and the HELD ask is downgraded to a validation item. **`PROXY-
>    EXCLUDES`** → the required state is **outside** the observed regime; the proxy cannot carry it and the HELD ask is
>    the **only** route (the successor's coverage declaration must then be labelled `DECLARED`, with a sensitivity, and
>    the level statement is conditional on it). **`PROXY-SILENT` / `DATA-BLOCKED`** → no declared conversion
>    discriminates (or the underlying count is `unable`), every coverage statement must be `DECLARED`, and the **proxy
>    route is closed** so no future worker spends a cycle on it.
> 3. **Why it is not a niche.** The successor's **only** admissible lower lever (if EXP-17 lands) is coverage, and the
>    programme's standing rule is that a proxy must **carry its name**. A cell that either supplies the proxy with its
>    distortion or **demonstrates its absence** is what stops the next predeclaration from inventing a utilisation
>    number — the exact failure A5's data clause forbids.
> 4. **Data on disk (no DATA ASK).** `10_massification/data/SCHOOL_EXPANSION.csv` — PHL `classroom_student_ratio_
>    elementary` **39** (2010) / **29** (2019) / **32** (2021); `classroom_student_ratio_junior_high_school` **54** /
>    **39** / **44**; `classroom_student_ratio_senior_high_school` **31** (2019); `pupil_teacher_ratio_high_school`
>    **37** (2000) / **27** (2014) / **24** (2017); `share_students_in_congested_public_elementary_schools` **90.0 /
>    76.8 / 66.0 / 60.1 / 57.7** (2021, five regional values, one `percent` column, no region key — a declared
>    limitation); `classrooms_needed_backlog` **110 954** (2019); `classrooms_needed_per_year` **10 000**. **Blocked, and
>    named as blocked:** `STATE_CAPACITY.csv` delivery rows — *number of public schools by year* (`unable`),
>    *classroom construction completed by year* (`unable`); `SCHOOL_EXPANSION.csv` — `number_of_classrooms_by_year`,
>    `number_of_public_schools_by_year`, `senior_high_school_capacity_2016_2018` all `unable`.
> 5. **Threshold + falsifier (fixed before the run).** One **declared conversion family**: classrooms → places using a
>    **declared norm class size interval {40, 45, 50}** (all three declared before the run, **none adopted**), combined
>    with the on-disk classroom counts/backlog to produce a **coverage interval** in the relevant years; report it
>    beside the **required coverage from EXP-17** (the `λ*`-implied `seats/cohort` at both years). **Verdict:
>    `PROXY-BOUNDS` iff the required coverage lies inside the interval under `≥ 2` of the `3` declared norms;
>    `PROXY-EXCLUDES` iff outside under `≥ 2` of `3`; `PROXY-SILENT` if the interval is wider than the required
>    state or the conversion is not identified; `DATA-BLOCKED` if the necessary count is `unable` in every year.**
>    **Falsifier:** conflict between two on-disk counts for the same object/year → `PROXY-SILENT`, and the conflict is
>    named (no reconciliation; the cell does not choose a number).
> 6. **Closed-claim check.** Does **not** change `phys_cap`; does **not** re-argue D139 or D131; **never fabricates a
>    utilisation or quality series**; HELD stays HELD; no re-fit; no direction claim; no level bar is used anywhere in
>    the cell.
> 7. **Cost / rank.** **Small.** **Rank #4** — it depends on EXP-17 and its most likely honest outcomes
>    (`PROXY-SILENT` / `DATA-BLOCKED`) are *bounded negatives*, which is why it ranks below the two cells that change
>    what may be declared.

### 1.1 The adopting decision (D145), verbatim

> Reproduced **verbatim** from `08_council/DECISIONS.md`, row **D145**, the EXP-19 clause:

> **EXP-19 PLACES-BOUND** — can the required coverage be bounded by anything observed on disk, or is it a declared
> assumption? (one declared conversion family, norm class size {40,45,50} declared and none adopted, from the on-disk
> PHL classroom/PTR series; verdicts PROXY-BOUNDS / PROXY-EXCLUDES / PROXY-SILENT / DATA-BLOCKED against EXP-17's
> required coverage; no phys_cap change, no fabrication, HELD named) **#4**;

### 1.2 The required-state inputs (D148), verbatim

> Reproduced **verbatim** from `08_council/DECISIONS.md`, row **D148**, the two EXP-19-relevant sentences:

> **Scope flag that binds downstream:** λ\* was solved on the **v1.2 panel, where the 2018 gate is capacity-limited**
> (0.783805 = 1.15·coverage); it does **NOT** transfer to A10's participation-limited gate (0.681570) — EXP-18/19 may
> cite it only as **`REQUIRED-STATE (EXP-17)`** with the **`DERIVED`** target **0.8076** attached (the lower-2021 value
> that would hold the model's own delivered upper-2024 76.6391 under κ=0.949; internal-consistency, not an external
> standard/policy target/forecast). **EXP-19 inputs:** required seats/cohort **0.759712** (2018) and **0.873523**
> (2021); observed-reference variant only +0.079/+0.090 pp higher. **No λ is adopted.**

The full-precision values used here are read from
`10_massification/extensions/joint_cover_2026-11-20/results/JOINT_COVER_RESULTS.csv`:
`coverage_2018 = 0.759712104599164`, `coverage_2021 = 0.87352319872549` (both `DERIVED`).
**No λ is installed, adopted or used as a parameter anywhere in this cell.**

### 1.3 The coverage/data ruling (D146), verbatim (excerpt)

> Reproduced **verbatim** from `08_council/DECISIONS.md`, row **D146** (two sentences; `[…]` marks omitted text):

> The **places** object is **not on disk as a count**: STATE_CAPACITY.csv delivery rows are `unable` for number of
> public schools by year and classroom construction completed by year, and SCHOOL_EXPANSION.csv is `unable` for
> number_of_classrooms_by_year, number_of_public_schools_by_year and senior_high_school_capacity_2016_2018.
> […] **no proxy substitution outside EXP-19** (the only cell permitted to construct a proxy — must label it DERIVED,
> state its distortion and adopt nothing).

---

## 2. The question, stated as a measurement question

EXP-17 returns a **required state**: one coverage path that satisfies both lower channels under the frozen law,
with required `seats/cohort` **0.759712** at the 2018 entry year and **0.873523** at the 2021 completion year
(`DERIVED`; `REQUIRED-STATE (EXP-17)`; the `DERIVED` target 0.8076 travels with it). The question of this cell is
**not** whether that state is substantively right and **not** whether PHL can reach it. The question is narrower:

> Is such a `seats/cohort` level **inside anything the programme can observe on disk** today, or is it an object
> that can only be **declared** (and therefore must carry a `DECLARED` label and a sensitivity)?

A **place count** would answer this directly. D146 establishes that no place count is on disk: the delivery rows for
public-school counts and completed classroom construction are `unable`, and `number_of_classrooms_by_year` and
`number_of_public_schools_by_year` are `unable`. What *is* on disk is a **class-size / PTR / enrolment description**.
This cell asks whether that description, through **one declared conversion family**, can be made to bound the
required state — and returns a bounded negative if it cannot.

---

## 3. Data on disk (read-only; no DATA ASK)

### 3.1 OBSERVED series used

Every value below is `OBSERVED` and is re-read from the named file+column at run time (D113a). The block's own
values are quoted in §1; the runner reads the columns, it does not trust the quotation.

| series (indicator) | file | years → values | unit | status |
|---|---|---|---|---|
| `classroom_student_ratio_elementary` | `SCHOOL_EXPANSION.csv` (also `STATE_CAPACITY.csv`) | 2010→39; 2019→29; 2021→32 | students per classroom | observed |
| `classroom_student_ratio_junior_high_school` | same | 2010→54; 2019→39; 2021→44 | students per classroom | observed |
| `classroom_student_ratio_senior_high_school` | same | 2019→31 | students per classroom | observed |
| `pupil_teacher_ratio_high_school` | same | 2000→37; 2014→27; 2017→24 | learners per teacher | observed |
| `classrooms_needed_backlog` | same | 2019→110,954 | classrooms | observed |
| `classrooms_needed_per_year` | same | 2019→10,000 | classrooms/year | observed |
| `share_students_in_congested_public_elementary_schools` | same | 2021→90.0, 76.8, 60.1, 66.0, 57.7 | percent | observed (five values, one column; no region key in the block's declared limitation; not used in the verdict) |
| `pupil-teacher ratio, primary` | `STATE_CAPACITY.csv` | 1995–2017 (annual, observed years) | learners per teacher | observed |
| `pupil-teacher ratio, secondary` | `STATE_CAPACITY.csv` | 1995–2017 (annual, observed years) | learners per teacher | observed |
| `teachers, primary (persons)` / `teachers, secondary (persons)` | `STATE_CAPACITY.csv` | 1995–2024 | persons | observed |
| `ger_lower_secondary` | `UNIVERSALIZATION_SERIES.csv` | 1998–2018 (observed years; **last year 2018**) | percent | observed |
| `ger_secondary` | `UNIVERSALIZATION_SERIES.csv` | 1971–2024 | percent | observed |
| `ger_primary` | `UNIVERSALIZATION_SERIES.csv` | 1971–2024 | percent | observed |
| `ger_upper_secondary` | `UNIVERSALIZATION_SERIES.csv` | 1998–2018 | percent | observed |

**Observed year coverage, which is itself a finding (stated before the run).** The level-matched divisor for lower
secondary (`classroom_student_ratio_junior_high_school`) is observed at **2010, 2019, 2021**. The level-matched
enrolment ratio (`ger_lower_secondary`) is observed at 1998–2009 and 2014–**2018**. **The intersection of the two
year sets is empty**: no year on disk supplies a same-year, level-matched pair. At the 2018 required year the
divisor is missing (nearest 2019, one year away); at the 2021 required year the level-matched enrolment ratio is
missing (nearest broader series `ger_secondary`, same year). This is an input fact, not a result; §4.4 and §5 say
in advance what the cell does with it.

### 3.2 `unable` rows, named and not used

`STATE_CAPACITY.csv` delivery rows: *number of public schools by year* — `unable`; *classroom construction
completed by year* — `unable`. `SCHOOL_EXPANSION.csv`: `number_of_classrooms_by_year`,
`number_of_public_schools_by_year`, `senior_high_school_capacity_2016_2018` — all `unable`. These are the direct
place counts. **They are not filled, imputed or replaced by a number.** They are the reason the cell constructs a
ratio-based proxy at all, and they are named in the results as `DATA-BLOCKED` inputs.

### 3.3 HELD (complete, named, unused — D135/D146)

The measured places/PTR series (DepEd/CHED seats-vs-enrolment); capacity utilisation (the object `V_O` would be
validated against); private/public shares of enrolment and provision; SHS voucher take-up; upper-secondary
completion for additional systems; single-age HKG population 1971–1996; HKG senior-secondary queue/places; PSA
microdata; WB Enterprise Surveys; real per-pupil spending; annual capacity/enforcement; a measured credential-queue
(rung-4) series; PHL/KHM/CHN/JPN shadow participation; a measured remittance→schooling coefficient. **None is used,
none is fabricated, and no external request is made.** The one HELD item this cell speaks to directly is the
**measured places/PTR series** and, for a direct validation, **capacity utilisation**; the cell may *downgrade the
ask to a validation item* only on a `PROXY-BOUNDS` verdict, which it does not return.

---

## 4. The declared conversion family

### 4.1 The family

One family, two observed divisor routes, one norm conversion:

**F1 — class-size route (dimensionally a room count).**

```
rooms(t, level)   = enrolment(t, level) / class_size(t, level)          # students / (students per classroom)
places(n, t)      = n * rooms(t, level)                                  # n = norm class size
coverage(n, t)    = places(n, t) / cohort(t, level)
                  = [enrolment(t,level)/cohort(t,level)] * [n/class_size(t,level)]
                  = GER(t, level) * n / class_size(t, level)
```

**F2 — PTR route (declared; requires one-teacher-per-classroom).**

```
rooms(t, level)   = enrolment(t, level) / PTR(t, level)                  # under one class per teacher
coverage(n, t)    = GER(t, level) * n / PTR(t, level)
```

Both routes are algebraically the same family: an observed **group-size divisor** `d` (students per classroom, or
students per teacher) is used to infer rooms, and `n` converts rooms to places. The family's output is an
**implied `seats/cohort`**, not a place count.

### 4.2 The three declared norm class sizes — none adopted

`n ∈ {40, 45, 50}` (students per classroom). All three are declared **before the run**. **None is adopted, chosen,
preferred or carried into any successor as a value.** The three are reported side by side; the verdict rules in §5
are stated over the set, not over a chosen element. The set is the block's, not the analyst's.

### 4.3 Declared assumptions of the family

- **A1 (place = norm × room).** A usable classroom supplies exactly `n` student places; no double-shift, no
  room-sharing, no rented/anchor rooms, no non-teaching rooms, no decay, no utilisation discount.
- **A2 (rooms = enrolment ÷ observed ratio).** The observed national average students-per-classroom ratio divides
  the same enrolment stock that the ratio was computed on; rooms not in use are inside the average.
- **A3 (GER = enrolment/cohort).** The enrolment ratio is the gross enrolment ratio; it includes overage and
  repeaters, and it is an enrolment ratio, not a seats/cohort ratio. A1 is what converts one to the other.
- **A4 (same-level matching).** The divisor and the enrolment ratio must be for the same education level. The
  required state is **lower secondary** (EXP-17's cell); the matching divisor is **junior high school** (PHL K-12
  lower secondary) and the matching enrolment ratio is **`ger_lower_secondary`**.
- **A5 (time matching).** The divisor is **exact** if observed in the required year `t`; **carried** if observed at
  `t−1` or `t+1`; otherwise inadmissible. The enrolment ratio must be observed at `t` (no carry). No interpolation,
  no regression, no extrapolation.
- **A6 (level fallback, declared and flagged).** Where the level-matched enrolment ratio is absent at `t`, the
  broader **`ger_secondary`** at `t` is used and the cell is flagged `LEVEL-FALLBACK`. It is never used silently.
- **A7 (PTR route's extra assumption).** F2 requires **one class per teacher**. At secondary this is false where
  teachers are subject-specialised; the on-disk pair PTR-24 vs JHS-class-size-39/44 implies ~1.6–1.8 teachers per
  room. F2 is therefore **computed and reported as a declared variant but is not verdict-bearing**; it is the
  family's own demonstration that a teacher count is not a room count at this level.
- **A8 (no cohort count).** No observed lower-secondary cohort count is on disk; the cell never invents one. The
  GER route is used precisely because it is a ratio and needs no cohort count. The 0–14 population series is **not**
  a lower-secondary cohort and is not used.

### 4.4 Matching rules (frozen)

- **M1 — required years.** `t = 2018` (entry) and `t = 2021` (completion), from EXP-17's lower-secondary cell
  (`t−3` entry; D148).
- **M2 — required level.** lower secondary (PHL JHS).
- **M3 — divisor admissibility (F1).** For each `t`, every `classroom_student_ratio_junior_high_school` observation
  with year in `{t−1, t, t+1}` is admissible; each contributes one cell per norm. If none, F1 is inadmissible at
  `t`.
- **M4 — divisor admissibility (F2).** Same window on `pupil_teacher_ratio_high_school`. F2 cells are reported with
  `verdict_bearing = FALSE` (A7).
- **M5 — enrolment-ratio choice.** At each `t`: use `ger_lower_secondary` at `t` if observed (`LEVEL-MATCHED`);
  else use `ger_secondary` at `t` (`LEVEL-FALLBACK`); else the year is `UNIDENTIFIED`.
- **M6 — exact cell.** A cell is `LEVEL-AND-YEAR EXACT` iff the F1 divisor year equals `t` **and** the enrolment
  ratio is `LEVEL-MATCHED` at `t`.
- **M7 — identification gate G.** `G = PASS` iff at least one `LEVEL-AND-YEAR EXACT` F1 cell exists for **each**
  required year. `G = FAIL` otherwise.

### 4.5 Interval construction

For each norm `n`, the **coverage interval** is

```
I_n = [ min over all admissible F1 cells (both required years) of coverage(n, ·),
        max over all admissible F1 cells (both required years) of coverage(n, ·) ]
```

computed on the **primary F1 cells** (M3–M5). This is the block's "coverage interval in the relevant years". The
**required state** is the interval

```
R = [ R_2018 , R_2021 ] = [ 0.759712104599164 , 0.87352319872549 ]      # DERIVED, EXP-17
```

Each `I_n` is reported beside `R`. The **F2** cells, the **broader-GER alternative** (`ger_secondary` at both
required years), and the **elementary/SHS** level-sensitivity cells are reported as **separate, non-verdict-bearing
sensitivities**; they do not enter `I_n`.

### 4.6 Distortions (stated before the run; full text in `results/PROXY_DISTORTION.md`)

1. The proxy is **not a place count**. It is a ratio-based **implied capacity**; it cannot see unused rooms,
   double shifts, room condition, or whether a "seat" is adequate.
2. `GER` is **gross enrolment / cohort**, not seats / cohort; it includes overage and repeaters. A1 (one seat per
   enrolled student at the norm class size) is what bridges the two, and it is an assumption.
3. The class-size ratio is a **national average of a ratio**, not a room census; the denominator is the same
   average's implicit room stock. Heterogeneity (congested NCR vs uncongested regions) is not in the national
   average; the five 2021 congested-share values are `OBSERVED` but are not a room count and are not used.
4. **Time:** 2018 uses a 2019 class size (carried one year); 2021 uses the exact 2021 class size. No interpolation.
5. **Level:** 2018 uses the level-matched `ger_lower_secondary`; 2021 uses the broader `ger_secondary`
   (`LEVEL-FALLBACK`). The two required years are therefore **not converted on the same enrolment object**. This
   is a declared inconsistency, not a reconciled number.
6. **PTR:** the one-teacher-per-classroom assumption is contradicted by the on-disk PTR/class-size pair at
   secondary; F2 is reported, not used.
7. **Cross-object comparison:** `R` is a **synthetic-panel required state** (`SYNTHETIC` panel, `DERIVED` λ\*), and
   the proxy is an **observed PHL** ratio. Comparing them is a declared cross-object comparison; it asks whether the
   observed PHL regime is *consistent with* such a coverage level, not whether PHL has that exact number.
8. **Backlog/flow:** `classrooms_needed_backlog` 110,954 and `classrooms_needed_per_year` 10,000 are `OBSERVED` but
   are **not** a room stock and **not** a cohort; they cannot form `seats/cohort` without a base count (unable) and
   a cohort count (HELD). They are reported as context only, never in the verdict.

---

## 5. Verdict mapping and precedence (frozen)

The block's four labels are operationalised as follows. **Precedence is explicit and is tested in this order**
(D147(c)(i)); the first label that fires is the verdict:

1. **`DATA-BLOCKED`** — fires if **no usable divisor series** (`classroom_student_ratio_junior_high_school` and
   `pupil_teacher_ratio_high_school`) **or no usable enrolment-ratio series** (`ger_lower_secondary`,
   `ger_secondary`) can be read at all, i.e. no admissible cell can be formed in either required year. This is the
   "no usable series" case. It is **not** triggered merely because the *direct place count* is `unable`; that
   blocking is the premise of the cell (D146) and is named in the results.
2. **`PROXY-SILENT` (identification)** — fires if the identification gate **G = FAIL** (M7): the conversion is
   **not identified** at the required object, because no `LEVEL-AND-YEAR EXACT` cell exists for at least one
   required year. The interval `I_n` and every comparison are still reported, but as **non-verdict-bearing
   sensitivity**. This is the block's "the conversion is not identified" clause.
3. **`PROXY-BOUNDS`** — fires iff **G = PASS** and `R ⊆ I_n` under **≥ 2 of the 3** declared norms.
4. **`PROXY-EXCLUDES`** — fires iff **G = PASS**, not `PROXY-BOUNDS`, and `R ∩ I_n = ∅` (the required state is
   disjoint from the interval) under **every** one of the 3 declared norms. The block's headline says "≥ 2 of 3"
   and its own gloss says "under every declared norm"; where the two disagree this cell reads the **narrower**
   label (D147(c)(i)), and `PROXY-EXCLUDES` requires 3/3. The 2-of-3 count is reported either way, so the Council
   can read the headline threshold without the cell claiming the stronger label.
5. **`PROXY-SILENT` (non-discrimination)** — fires in every remaining case: at least one norm straddles `R`
   (partial overlap), or no ≥ 2-of-3 majority exists, or `I_n` is wider than `R` under ≥ 2 of 3 norms
   (`span(I_n) > 3 · span(R)` is the declared "uninformative-wide" test), or an `UNDETERMINED` cell prevents a
   classification. This is the block's "the interval is wider than the required state" clause.

**Per-norm classification (reported for every norm, verdict-bearing only if G = PASS):**

- `INSIDE` if `R ⊆ I_n` (both required-state endpoints lie in the interval);
- `OUTSIDE` if `R ∩ I_n = ∅` (the interval and the required state share no point);
- `STRADDLE` otherwise (partial overlap).

**No third value is introduced; no norm is preferred; no interval is trimmed.** `UNDETERMINED` is used only for a
cell the frozen rules cannot classify, with its reason stated.

**The falsifier (block clause 5).** A conflict between two on-disk counts for the **same object and year** →
`PROXY-SILENT`, the conflict named, no reconciliation, and the cell does not choose a number. **Falsifier-arm
audit.** Arm F1 (class-size route): **can fire** — it is evaluated on the JHS ratio and `ger_lower_secondary` /
`ger_secondary`; a same-object/year conflict (e.g. two different JHS ratios for one year) would trip it. Arm F2
(PTR route): **can fire** — it is evaluated on the PTR series; but it is not verdict-bearing (A7), so a conflict
there is reported and does not change the verdict. Arm S (sensitivity: elementary/SHS): **cannot fire** into the
verdict — it is reported only. **Expected direction of the statistic that fires the falsifier:** a conflict is a
*difference between two values for one object/year*, not a level; the cell reports the two values and the gap, and
returns `PROXY-SILENT` regardless of which value would have produced which label.

---

## 6. Closed-claim check (declared before the run)

- **Does not change `phys_cap`.** No `phys_cap` value is read as a free parameter, re-chosen, re-gridded or
  re-argued. `phys_cap` is not in the code's verdict path at all.
- **Does not re-argue D139 or D131.**
- **Never fabricates** a utilisation, quality, place, classroom, school or cohort series. `unable` stays `unable`;
  HELD stays HELD.
- **No re-fit.** No number is chosen by reference to `R`, to the `0.759712` / `0.873523` values, to any interval
  boundary, or to any observed cell.
- **No direction claim and no causal claim.** The cell measures a consistency/identification question; it does not
  say coverage *causes* completion, or that a higher coverage would *raise* anything.
- **No level bar is used anywhere in the cell.** The `≥17/33` observed-path bar is not read, computed or cited.
- **No model run, no generator import, no RNG, no network, no clock in any output.**
- **Adopt nothing.** The three norm class sizes are declared and none is adopted; `λ*` is not adopted; no coverage
  path is declared for the successor; the HELD places series is not replaced.
- **D63 remains `UNABLE` as to cause**; the phase verdict and scaling FAIL are untouched.

---

## 7. Outputs, labels and determinism

The runner writes, into `results/` and an independent second-run copy in `results/determinism_run2/`:

- **`PLACES_BOUND_RESULTS.csv`** — `record_type,item,value,unit,label,note`: every input used, the required state,
  the norm set, the implied coverage under each norm, the interval `I_n`, the per-norm comparison, the
  identification gate, the verdict, the components, the blocked/HELD rows, and the closed claims.
- **`PLACES_BOUND_DETAIL.csv`** — one row per cell: required year, divisor source/year/value, enrolment-ratio
  source/year/value, level relation, norm, `rooms_per_enrolled_student`, `implied_coverage`, `required_coverage`,
  `gap_pp`, classification, `cell_role`, `verdict_bearing`, `label`, `note`.
- **`PROXY_DISTORTION.md`** — the declared assumptions and why the proxy is / is not a place count.
- **`determinism_run2/`** — the same `PLACES_BOUND_RESULTS.csv`, `PLACES_BOUND_DETAIL.csv`, `INPUT_HASHES.json`
  and `console.txt` written by a second independent execution.

**Every numeric row carries `OBSERVED`, `DERIVED`, `DECLARED`, `SYNTHETIC` (only where an imported value is
synthetic-panel-derived) or `HELD`.** Determinism: no RNG; all rows sorted by a fixed key; floats formatted with a
fixed `%.12g` (percent gaps `%.6f`); no clock, no hostname, no absolute paths, no run-id in any output. The runner
is invoked twice with different `--outdir` values and the results files must be **byte-identical**.

---

## 8. Blindness disclosure (D147's standard; the EXP-14 C-5 lesson applied at freeze, not after it)

Before this freeze the analyst:

1. read the Council block, D145, D146, D147, D148, the two data files and `UNIVERSALIZATION_SERIES.csv` (the
   block's own data clause requires this, and D113a requires the anchoring numbers to be re-derived);
2. observed the **year coverage** of the series — that the JHS class-size ratio is observed at 2010/2019/2021 and
   `ger_lower_secondary` only through 2018, so the level-matched year sets do not intersect. This is an **input
   fact** (the series' own year labels), not a verdict;
3. did **not** execute any conversion, any implied-coverage cell, any interval construction, or any verdict rule
   before the freeze. No script was run against these data before `code/run_places_bound.py`; the predeclaration's
   §4–§5 rules were written first and hashed first.

What is known at freeze and is disclosed so that no later sentence can imply more blindness than the record
supports: the **approximate magnitude** of the observed ratios and GERs is visible in the block itself (39/44 and
~86–93%), so the analyst cannot claim to be blind to "roughly where" the implied coverage will land. The cell's
contribution is not a surprising number; it is the **precise identification finding** (no same-year, level-matched
pair at either required year), the **norm-by-norm interval**, and a **frozen rule** that says in advance what
counts as a bound. No interval boundary is chosen after seeing a result.

---

## 9. What would change the answer (declared, not a promise)

A single on-disk year that observed **both** the JHS class-size ratio **and** `ger_lower_secondary` would turn
`G` to `PASS` at that year and allow a level-and-year exact conversion; the verdict would then be read from §5
steps 3–5. A measured **classroom stock** (the HELD/`unable` count) would remove the conversion family entirely and
make the comparison a direct one. Neither is on disk, and neither is requested here (D146: no external request; user
approval required for any HELD item). **This cell does not close the HELD ask; it classifies why the ask is still
open.**

---

*Written and hashed before execution. This file is the freeze. If its sha256 changes, the run is void.*
