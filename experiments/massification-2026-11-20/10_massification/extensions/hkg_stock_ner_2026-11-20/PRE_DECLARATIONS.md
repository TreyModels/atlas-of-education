# PRE-DECLARATIONS — STOCK-NER-D (EXP-10): frozen stock-style NER object for the HKG diagnostic transfer

> `SCALING: FAIL (standing, A12/B02) — DIAGNOSTIC-TRANSFER ONLY — NOT EVIDENCE`

**Worker SN, 2026-11-21 (Asia/Shanghai). FROZEN. RUN-READY. NOT RUN.**

**Status of this document: a frozen specification, not a result.** No stock value has been computed, no band
test has been scored, no crossing has been read, and no HKG object has been assembled. `results/` does not
exist in this directory. The sha256 of this file is recorded in `RUN_MANIFEST.json` **before any run**, and
this file is not edited after a run.

**Label: DIAGNOSTIC-TRANSFER / DESIGN-ONLY.** The test objects named here are **SYNTHETIC** model output.
The HKG observed series is **OBSERVED-REFERENCE-ONLY** and is **never read by the object or by the construct
test**. Nothing here is observed, estimated, fitted, forecast, or evidence about any country.

**No causal claim. No direction or push–pull claim (R13/D77). No portability claim (R22). No capacity-timing
claim (D61/D74/R28). No policy claim. No phase-verdict claim (D76/D77). Nothing here licenses a change to any
locked verdict.**

**Scope:** this directory only (`10_massification/extensions/hkg_stock_ner_2026-11-20/`). No file in
`m1_ner_2026-11-20/`, `hkg_transfer_2026-11-20/`, `synthetic_2026-11-20/`, `10_massification/data/`,
`08_council/`, or anywhere else is edited, moved, or rewritten by this experiment.

---

## 0. One-line statement, and the design verdict

**One line.** D114 voided the HKG diagnostic transfer for the model's cohort-flow NER analogue and named a
stock-style object as the only forward path; this document freezes — before any computation — the **object**,
its **operands**, its **construct test**, its **pre-registered direction**, the **carried constraints**, the
**data limits**, and the **labels**, such that the object can be construct-tested **without ever reading the
two HKG target years** and **without any fitted quantity**.

**Design verdict (this document's own verdict, and the only verdict it emits):**

```
PRE_DECL-FROZEN
```

`PRE_DECL-FROZEN` is defined (Council D120 / SYNTHESIS_022 §6.10 item 5) as: **N1–N6 are all satisfied** and
**the predeclaration hash is recorded before any run**; otherwise the design is `BLOCKED-MEASURE`. Evidence
that the six conditions are satisfied is the §2 table (verbatim carry) plus the §2.7 cross-walk (where each
condition is discharged in this document). The hash is recorded in `RUN_MANIFEST.json`
(`predeclaration_sha256`) and in `SHA256SUMS.txt`, both written **before** any run.

**`PRE_DECL-FROZEN` is a statement about the specification, not a forecast that the construct test passes.**
The construct test is **not executed here and is not authorised here** (§8). Its outcome is pre-registered as
either `CONSTRUCT-EQUIVALENT` or `BLOCKED-MEASURE` (§6.5), and §7 states, in advance, the analytically derived
expectation about the sign and the likely size of the stock–flow wedge. A `BLOCKED-MEASURE` on the construct
test is a **terminal, legitimate, informative** outcome — it closes the HKG arm on the measure rather than
running a diagnostic on a measure already declared not-the-target.

---

## 1. Authority

| source | what it binds here |
|---|---|
| **D114** (`08_council/DECISIONS.md:128`) | H1 = **NOT ADMISSIBLE** on the cohort-flow analogue (band max **2.685005 pp**, 7/15 band years; crossings **3 y** / **2 y**); the HKG transfer must return `BLOCKED-MEASURE(SR-1)` unless a **new predeclaration specifying a stock-style NER object** exists. This document is that predeclaration's design half. |
| **D120** (`:136`) | **`DESIGN-ONLY STOCK-NER PREDECLARATION`** — design a stock object, construct-testable by its own rule, **run-ready and NOT run**; conditions **N1–N6** binding before freeze; **execution NOT authorised**. |
| **D122** / **SYNTHESIS_022 §6.10** (`08_council/brief_022/SYNTHESIS_022.md:421–446`) | EXP-10 **STOCK-NER-D**, rank #5 / **drop-first**: design verdict, construct-test threshold, falsifier. Definitions and thresholds are copied verbatim in §2. |
| **D111** (`:124`) | SR-9 authority, **H2–H6**, the standing banner, and the licensing limits. Carried verbatim in §2.4. |
| **D75** (`:84`) | the **six constraints** every later HKG run must satisfy. Carried verbatim in §2.5. |
| **D115 / D117–D119** | measurement context only: the anchor's level misses (primary −4.30, lower −29.44, upper −27.59), completion is a cohort-flow object, v1.2 scope is crossing/endpoint placement **not** a path. Nothing here re-scores them. |
| **D131** (`:153`) | v1.5 state (`a=MIXED; b=FAIL; …; ALL=FAIL`; representation admitted, level pattern not reproduced). Recorded as context; **not** a premise of this object, and no v1.5 number is used. |
| `hkg_transfer_2026-11-20/` | the frozen transfer predeclaration (`99be01d7…`), its inventory, checklist, and `HKG_H1_OUTCOME.md`. This document **amends neither**; it supplies the object that D114 required, and it leaves the frozen HKG predeclaration untouched. |
| `m1_ner_2026-11-20/` | the failed construct test (predecl `9eb35a92…`). This document **is not a rescue of M1-NER**: it declares a *different* object (a ratio of two stocks, §3.5) under *the same* bars, and if the bars fail again the object is `BLOCKED-MEASURE` — not re-specified. |

---

## 2. The Council definitions and thresholds, verbatim

Copied from `08_council/brief_022/SYNTHESIS_022.md` §5.2 (N1–N6) and §6.10 item 5 (EXP-10 threshold +
falsifier), and from the D111 / D75 rows of `08_council/DECISIONS.md`. **Nothing in §3–§12 widens, relaxes, or
reinterprets any of it.** Two table cells below are reproduced as block quotes rather than table rows because
their `|` characters would break a Markdown table; their text is unchanged.

### 2.1 N1–N6 (SYNTHESIS_022 §5.2, verbatim)

> **N1 — object** | A **stock-style NER analogue** constructed by a **declared, parameter-free rule** from the
> model's own objects (entry cohorts `admitted_official`, `cohort`, declared `survival`, level duration),
> **not** the mean-of-ratios window that M1-NER tested and not the cohort-flow `ner` column. The rule must
> state how repeaters and over-age admissions are treated. The target series is never read by the construction.

> **N2 — construct test** | The object's own construct test: **|stock − flow| ≤ 2.0 pp** in every year where
> the analogue ∈ [85,95] **and** first-sustained (5-year) crossing years differ by **≤ 1 y**, scored on
> **both** `SYN00_PHL_LIKE` and `SYN28` primary. **If it FAILS, the object is `BLOCKED-MEASURE` too — not
> re-specified, not run.**

> **N3 — direction pre-registered** | D114 established that the flow analogue **leads** the stock by 2–3 y.
> The predecl must state that a stock object can only move crossings **later**, that a `TRANSFER-FAILS` on it
> is therefore **expected and confirmatory** (not a new finding), and that a `TRANSFER-HOLDS` on it is the
> **more informative** outcome. This must be written before the run, not after.

> **N4 — carried unchanged** | D111 **H2–H6** and D75's six constraints, verbatim: fixed PHL behaviour, only
> declared country inputs re-set; no re-fit/extra free parameter/target fitting (`FAIL-RE-FIT`, name the moved
> parameter); HKG **timing-only**, levels check-only, **NER ≥90 in 1974 / ≥95 in 1979**, threshold-specific,
> never spliced; CHN arm only with censoring rules and the 1986-law **−27 y** miss as is; the standing banner
> `SCALING: FAIL (standing, A12/B02) — DIAGNOSTIC-TRANSFER ONLY — NOT EVIDENCE` in every table; verdicts
> `TRANSFER-HOLDS`/`TRANSFER-FAILS`/`FAIL-RE-FIT`/`BLOCKED-*`, never `PASS`.

> **N5 — no observed-validation claim at the target window** | The observed-data cross-check of the
> reconstruction is possible **only for 2012–2018** (HKG `ger_primary` exists 2001–2024; `ner_primary`
> 1971–1985, 1995–1996, 2012–2018; overlap **7 years**, NER **88.5–99.2**). The predecl must state that the
> object cannot be validated against observed HKG data **in 1971–1996**, and that the 7-year saturated overlap
> is not a substitute. Any need for a single-age HKG population series is a **DATA ASK, HELD** (never
> fabricated, never derived from the target series).

> **N6 — labels** | Every file carries the N4 banner, the `DIAGNOSTIC-TRANSFER` vocabulary, and the sentence
> "**no HKG result exists until one is produced; nothing here licenses a portability, capacity-timing, or
> phase-verdict claim**". `BLOCKED-*` is terminal.

### 2.2 EXP-10 threshold + falsifier (SYNTHESIS_022 §6.10 item 5, verbatim)

> **Threshold + falsifier.** Design verdict: `PRE_DECL-FROZEN` iff N1–N6 are all satisfied and the predecl hash
> is recorded before any run; `BLOCKED-MEASURE` otherwise. Construct test (executed only under a further
> decision): **absolute (stock − flow) ≤ 2.0 pp** in every year with the analogue ∈ [85,95] **and** crossing
> difference **≤ 1 y**, on **both** `SYN00_PHL_LIKE` and `SYN28`. **Falsifier:** any target-year reference
> (1974/1979) inside the predecl, or any fitted quantity, makes the design `FAIL-RE-FIT` and it is not
> dispatched.

### 2.3 The object's *first-order* question (SYNTHESIS_022 §6.10 item 1, verbatim)

> 1. **First-order link (measurement for the diagnostic arm).** Whether a stock-style NER object can be
>    constructed, construct-tested and frozen **before** any transfer is attempted — the object D114 named as
>    the only forward HKG path.

### 2.4 D111 H2–H6, verbatim (`08_council/DECISIONS.md:124`)

> **H2** the v1.2.1 addendum must be a delivered artifact (predecl hash, manifest, FINDINGS, determinism note,
> SHA256SUMS; two byte-identical runs) and the SR-2 gate must carry a status note correcting its path to
> `generator_v1_2/` (checklist still reads the predecl-only `v1_2/`), without editing the frozen predecl.
> **H3** SR-2 recorded as PASS-CONDITIONAL (m window, m=1.05/1.12 failure points, design-phase calibration,
> demand/quality-driven ceiling); no HKG file may say "v1.2 passes". **H4** D7–D9 declared values
> pre-tabulated with on-disk sources or DECLARED rationales that do not reference 1974/1979, hashed before the
> run; post-hoc change = FAIL-RE-FIT. **H5** D75 six constraints (fixed PHL behaviour; no re-fit/extra free
> parameters; HKG timing-only + levels check-only + NER ≥90 in 1974 / ≥95 in 1979, threshold-specific, never
> spliced; CHN arm only with censoring rules and the 1986-law −27 y miss as is; scaling-FAIL banner in every
> table; verdicts `TRANSFER-HOLDS`/`TRANSFER-FAILS`/`FAIL-RE-FIT`/`BLOCKED-*`, never PASS). FINDINGS must
> state that **TRANSFER-FAILS is the informative outcome**. **H6 scope:** timing-only, primary NER only,
> 1974/1979 only, ±5 y, no completion series, no level in verdict, no HKG/portability/phase-verdict claim.

And the D111 **licensing** sentence, verbatim:

> **Licensing:** TRANSFER-HOLDS licenses only "the frozen parameterisation places the two primary NER
> crossings within ±5 y" — a statement about the simulator, not portability (R22), not evidence about HKG, not
> an anchor upgrade, not a verdict change, not "capacity explains timing" (D61/R28); TRANSFER-FAILS licenses
> only "the timing error recurs on a second high-capacity system"; FAIL-RE-FIT = void; BLOCKED-* = no
> diagnostic.

### 2.5 D75's six constraints, verbatim (`08_council/DECISIONS.md:84`)

> (i) fixed PHL behaviour/parameters, only declared country inputs re-set (R20); (ii) **no re-fit, no extra
> free parameters, no target fitting — any occurrence = FAIL** and the moved parameter named; (iii) HKG
> **timing-only, levels check-only** (NER≥90 1974, NER≥95 1979, threshold-specific, never spliced); (iv) CHN
> with censoring rules and the 1986-law **−27 y** miss reported as is; (v) standing scaling **FAIL** printed in
> every table; (vi) verdict vocabulary **DIAGNOSTIC-TRANSFER** (transfer-holds / transfer-fails / FAIL-re-fit),
> **never PASS**, and the predecl must say **what it would change** given the anchor's own misses.

Also verbatim from the same row — the authority clause this document does **not** satisfy and does not claim
to satisfy:

> A later run requires a new Council decision + predecl under six constraints.

### 2.6 What N4 means for a **design-only** document

This document carries H2–H6 and D75's six constraints **unchanged**, and it **does not discharge any of them**.
Specifically it does **not** authorise an HKG run, does **not** create the object's code as a delivered
artifact, does **not** grant SR-9 authority, and does **not** assert H2/H3 compliance of anything. The six
constraints become operative only in the run that a **further** Council decision would authorise; N4 is
carried here because D120 makes carrying it a condition of the freeze, not because this document executes it.

### 2.7 Cross-walk — where each of N1–N6 is discharged

| condition | discharged by | checkable artefact |
|---|---|---|
| **N1 object** | §3 (algebra, operands, durations, parameter-free argument), §4 (operand rows), §3.4 (repeaters / over-age), §3.6 (target isolation) | this file §3–§4; `STOCK_NER_DESIGN.md` §3–§7; guard **G6** in `DRY_RUN_PLAN.md` §6 |
| **N2 construct test** | §6 (windows, band rule, crossing rule, decision rule, two required test types, terminal vocabulary) | this file §6; `DRY_RUN_PLAN.md` §4 |
| **N3 direction** | §7 (pre-registered direction and the analytic sign of the wedge) | this file §7; `STOCK_NER_DESIGN.md` §10 |
| **N4 carried unchanged** | §2.4, §2.5 (verbatim), §8 (execution not authorised) | this file §2.4–§2.5, §8 |
| **N5 no observed-validation claim** | §11 (target-window validation impossible; 2012–2018 overlap only; HELD data ask) | this file §11 |
| **N6 labels** | §0, §11, §12 (banner, `DIAGNOSTIC-TRANSFER` vocabulary, `BLOCKED-*` terminal, the N6 sentence) | every file in this directory; guard **G7** |

---

## 3. N1 — the object

### 3.1 Definition (frozen)

For country `c`, level `L` with declared duration `d = dur_L`, and year `t`, on the frozen v1.2 panel:

```
w_k(c,L,t)  =  survival(c,L,t) ^ (k / d)                                  k = 0, 1, ..., d-1
N(c,L,t)    =  SUM_{k=0..d-1}  admitted_official(c,L,t-k) * w_k(c,L,t)   [pupils]
B(c,L,t)    =  SUM_{k=0..d-1}  cohort(c,L,t-k)                           [persons]
STOCK(c,L,t) = 100 * N(c,L,t) / B(c,L,t)                                  [percent, pp]
FLOW(c,L,t)  = 100 * admitted_official(c,L,t) / cohort(c,L,t)             [comparator only]
DIFF(c,L,t)  = STOCK(c,L,t) - FLOW(c,L,t)                                 [percentage points]
```

`STOCK-NER-D` is the object. `FLOW` is **not** part of the object: it is the declared comparator that the
construct test of §6 scores the object against, and it is bit-for-bit the panel's `ner` column (§5).

### 3.2 What each term is, in words

- **`N` is a pupil stock.** It is the reconstruction of *how many official-age pupils are in level `L` in year
  `t`*, built from the entry cohorts that are inside the level's declared duration window at `t`: the cohort
  admitted at `t` (grade 1), the cohort admitted at `t−1` (grade 2), …, the cohort admitted at `t−(d−1)`
  (grade `d`). Each entry cohort enters at its own `admitted_official` flow and is carried forward with the
  level's declared survival.
- **`B` is the official-age band.** It is the reconstruction of *how many persons of official age for level `L`
  are alive in year `t`*: the same `d` single-year cohorts, each counted at the size it had when it was the
  entry-age cohort (`cohort(c,L,t−k)`). It is the model's own `cohort` column summed over the same window.
- **`STOCK` is therefore a ratio of two stocks** — pupils over persons — which is the dimensionality of the UIS
  net enrolment ratio `NER.1.cp`. This is the formal reason the object is a *stock-style NER analogue* and not
  a flow object: numerator and denominator are both counts at `t`, not annual flows divided by annual flows.
- **`w_k` is the declared holding weight.** `w_0 = 1`: the cohort admitted this year is counted before any
  attrition. The weight decays geometrically to `w_d = survival` at the end of the level's duration. The
  single survival number the model carries for a level-year is thus spent as a **constant-hazard** schedule
  over the level's `d` grade-years.

### 3.3 Durations (`d`) — taken, not chosen

`d` is the frozen factory's declared level duration (`generator_v1_2/code/sim_v1_2.py:65`, `DVEC`;
`generator_v1_2/PARAMS.md` §3), which this document **does not re-declare and may not change**:

| level | `d` (years) |
|---|---|
| primary | 6 |
| lower_secondary | 3 |
| upper_secondary | 3 |
| tertiary | 4 |

The construct test is scored on **primary only** (`d = 6`), because D75's HKG target is primary NER (N4/H6).
Other levels are not scored and are not reported.

### 3.4 N1 — repeaters and over-age admissions, declared explicitly

| population | treatment in `N` | why, and what it costs |
|---|---|---|
| **Official-age first-time entrants** (`admitted_official`) | **counted**, at their own flow, through the duration window | the model's own official-age admission object; the same numerator the flow analogue uses |
| **Over-age admissions** (`admitted_overage`) | **excluded, everywhere** | `NER.1.cp` is an *official-age* ratio; the model's rationing rule admits official age first and over-age only from residual capacity (`sim_v1_2.py:588–589`), so the two components are separable and are not mixed. Including them would make the object an age-agnostic admission stock (a GER-like object), which is the substitution `SR-8`/constraint (iii) bar. **Declared cost:** in a system that seats over-age pupils in official-age places, the object omits them, so it is biased **downward** relative to a measure that counted them. |
| **Repeaters** | **not represented; the object carries none** | the frozen generator has **no grade structure and no repeater state**: an admitted pupil is carried as one entry cohort and there is no re-entry flow (`PARAMS.md` §3–§4; `sim_v1_2.py:567–607`). A repeater is therefore representable in the model only as an **over-age** admission, which is already excluded. **Declared cost:** a repeater of official age *would* be counted by `NER.1.cp`, so the object is biased **downward** by the missing repeater stock. This bias is **not** corrected, **not** imputed, and **not** bounded by any number in this document; it is a declared limitation of the model interface. |
| **Dropouts within the level** | represented by `w_k` (survival) | the model's own `survival` column; see §3.5 on why it is spent as a constant hazard |
| **Out-of-school / never-entered children** | absent from `N` by construction | they are in `B` (the band) and not in `N`, which is exactly what a net (not gross) ratio does |

**No other population is admitted.** There is no migration adjustment, no mortality adjustment inside the
window (the band is taken at its entry-year size, which is the model's own convention), no interpolation, and
no smoothing.

### 3.5 Why the object is parameter-free

The claim is not "no choices were made". The claim is that **no number in the object was chosen, fitted,
tuned, or calibrated**, and that the one shape choice is spent by the model's own identity:

1. **The only numbers are panel values.** `admitted_official`, `cohort`, `survival` are columns of the frozen
   panel; `d` is a frozen factory constant. Nothing else is read.
2. **The exponent is not a parameter.** `k/d` is fixed by `d` and by the grade index `k`; there is no free
   exponent.
3. **The endpoints of `w` are both given, not chosen.** `w_0 = 1` is the definition of an entry cohort at
   entry; `w_d = survival` reproduces the model's **own** completion identity,
   `completion_cohort(c,L,t) = admitted_official(c,L,t−d) * survival(c,L,t)` (`sim_v1_2.py:606`). A constant
   hazard is the schedule with **no free shape value** between those two fixed endpoints: it is the unique
   geometric interpolation, so the object adds **no further degree of freedom** to the model.
4. **Nothing is estimated from data, and nothing is estimated from the target.** There is no regression, no
   anchor, no per-country override, no per-level array, no interpolation through observed years. The run
   refuses if any parameter set differs from the frozen one (`DRY_RUN_PLAN.md` §6, G2/G3).
5. **The object is a closed-form function of the frozen panel.** Given the panel, the object is uniquely
   determined; two implementations that read the same columns must produce the same numbers (§10).

The one **declared** choice — geometric (constant-hazard) holding rather than a linear or an endpoint-only
schedule — is disclosed as a choice and is **not** re-chosen after a result (§3.7). Alternative schedules are
enumerable and are **not** part of this declaration.

### 3.6 N1 — the target series is never read (target isolation)

- The object and its construct test read **one** file: the frozen synthetic panel
  `generator_v1_2/results/synthetic_panel_v1_2.csv` (SYNTHETIC), plus the addendum panel
  `generator_v1_2_addendum/results/synthetic_panel_v1_2_ner.csv` **only** as a display-precision cross-check of
  the comparator's re-derivation (§5). No observed series is opened by the object or by the construct test.
- **No observed HKG series, no `UNIVERSALIZATION_SERIES.csv` value, no `UNIVERSALIZATION_TIMING.csv` row, no
  PHL series, and no target year participates in the construction.** The object's construction has no
  country-specific input of any kind: `SYN00_PHL_LIKE` and `SYN28` are selected only as *test types* for the
  construct test, and the same formula is applied to both without modification.
- The target years appear in this document **only inside the quoted Council text** of §2 (N3/N4/N5, D111 H5/H6,
  D75 (iii)). They are **labels carried unchanged**, not operands: no rule in §3–§7 reads, filters, compares
  to, or is calibrated by them, and no computed quantity in the construct test is a function of them.
- **Guard G6** (`DRY_RUN_PLAN.md` §6) makes this mechanical: the runnable object module must contain **zero**
  integer constants equal to 1974 or 1979 and **zero** string constants containing them; if either token
  appears in the module, the run aborts before computing anything. The object's operand list is asserted
  against a frozen allow-list of three column names (G4).
- **The falsifier (§2.2, verbatim) is treated as discharged if and only if** (a) **no operand, rule, filter,
  threshold, or computed quantity in this document is a function of the two target years**, and (b) **G6
  mechanically forbids the literals in the runnable module**. The two years do occur in this file, and every
  occurrence is accounted for and is one of exactly three kinds: (i) the **N4-mandated verbatim carry** in
  §2.1–§2.5 (N3, N4, N5, D111 H5/H6, D75 (iii), D111 licensing); (ii) the **discipline statements** of this
  §3.6; (iii) the **left-edge statement** in §4.2 and the **scope exclusion** in §6.7. There is no fourth kind.
  A reviewer can confirm this with `grep -n "1974\|1979" PRE_DECLARATIONS.md` and will find no operand, no
  threshold, no window bound, and no formula that contains either year.
- **Falsifier (verbatim, §2.2):** any target-year reference inside the predecl, or any fitted quantity, makes
  the design `FAIL-RE-FIT` and it is not dispatched.

### 3.7 What will **not** happen after a result

- If the construct test returns `BLOCKED-MEASURE`, **no** alternative weighting, denominator, level, country,
  window, threshold, or tolerance is tried, and the object is not re-specified. The terminal state is recorded
  and the HKG arm closes on the measure (N2).
- No parameter, no threshold, no band, no crossing rule, and no tolerance in §6 is edited after a result.
- This file is not edited after a run. A defective rule is corrected only by a **new** predeclaration under a
  **new** Council decision (`hkg_transfer_2026-11-20/HKG_TRANSFER_PRE_DECLARATIONS.md` §12, same discipline).

---

## 4. Operands — exact rows and columns

### 4.1 Input panel

`10_massification/extensions/synthetic_2026-11-20/generator_v1_2/results/synthetic_panel_v1_2.csv`
(sha256 `14729c5141a71dd9aaf87a5ad2e973a84b5f04603577aae627f2833276fac5ac`). 6 720 data rows; 67 columns;
30 countries × 4 levels × 56 years (1970–2025); every row `label = SYNTHETIC`. Read **read-only**.

Columns **read** by the object (allow-list; nothing else is read):

| column | role in the object |
|---|---|
| `country`, `year`, `level` | row identity |
| `admitted_official` | numerator flows `A(c,L,t−k)` and the comparator's numerator |
| `cohort` | denominator band terms `C(c,L,t−k)` and the comparator's denominator |
| `survival` | the level-year holding weight `s(c,L,t)` |
| `label` | must be `SYNTHETIC` on every row read |

Columns **deliberately not read**: `ner*` (the addendum's derived columns — read only in the §5 cross-check,
never in `N` or `B`), `band_population` (rejected denominator, §3.2 and `STOCK_NER_DESIGN.md` §13.1),
`admitted_overage`, `enrolment`, `ger`, `rationed_official`, and every other column.

### 4.2 Rows used, and the left edge

- A stock value is computed **only** where the full `d`-year window exists (`t−d+1 ≥ 1970`). For primary,
  `STOCK` exists from **1975** onward. There is no truncated window, no partial-window value, no back-cast, and
  no imputation at the left edge. Years 1970–1974 are reported in the comparison output with
  `stock_window_complete = FALSE` and are **not** in the band test.
- No row is dropped, winsorised, smoothed, or re-ordered. No level is pooled. No country is pooled.
- The panel is contiguous annual data, so no missing-year rule is needed. If any operand row were missing, the
  run **fails closed** (`BLOCKED-INPUT`) rather than skipping the year.

### 4.3 Precision

All arithmetic in IEEE double precision on the published `%.10g` values; all report fields written at
`%.6f`. Years are integers. Comparisons use `1e-9` as a floating-point equality tolerance **only** — it is never
a widened bar.

---

## 5. The comparator (`FLOW`) and its verification

`FLOW(c,L,t) = 100 * admitted_official / cohort` on the row's own level. For primary rows this is identically
the addendum's `ner_primary` column (`generator_v1_2_addendum/PRE_DECLARATIONS.md` §2). The run:

1. re-derives `FLOW` from `admitted_official` and `cohort` on the parent panel;
2. cross-checks it against the addendum panel's `ner` column for the same `(country, year, level)` at
   `%.10g` display precision;
3. **aborts** (`BLOCKED-INPUT`) on any mismatch beyond display precision. No value is substituted.

The comparator is used **only** to score the construct test. It is never an input to `N` or `B`, and the
object does not reduce to it except in the degenerate case `survival = 1` with a stationary `A/C` (§3.2;
`STOCK_NER_DESIGN.md` §8.1).

---

## 6. N2 — the construct test (declared in full, **not executed here**)

### 6.1 Test types (both required; the object must pass on both)

| id | country | level | series | why this type |
|---|---|---|---|---|
| **T1** | `SYN00_PHL_LIKE` | `primary` | `STOCK` vs `FLOW`, 1970–2025 | the PHL-calibrated anchor and the series on which H1 was decided; the programme's primary comparison |
| **T2** | `SYN28` | `primary` | `STOCK` vs `FLOW`, 1970–2025 | `SYN28` is the **highest-2020-GDPpc** synthetic type (`gdppc` 2020 = **48 270.81**, top of 30 — verified on the frozen panel) and is the generator's `SYN_HKG_LIKE` host (`generator_v1_3/TUNE_LOG.md:50`). It is required by N2 as the second, high-capacity test type so that the construct cannot be cleared on the PHL-like anchor alone. |

Both types are scored with the **same** formula, the **same** band rule, the **same** crossing rule, and the
**same** bars. **MET** on one test type and **NOT MET** on the other is `BLOCKED-MEASURE`.

### 6.2 Band condition (Condition B)

- **Band years** for a series: every year `t` with a **complete** window (`t ≥ 1975` for primary) **and**
  `85.0 ≤ FLOW(t) ≤ 95.0` (inclusive at both ends). The band is defined on `FLOW`, the comparator, exactly as
  in M1-NER §4.1 and D111 H1.
- **MET** iff `|DIFF(t)| ≤ 2.0 pp` in **every** band year of that series.
- **NOT MET** iff `|DIFF(t)| > 2.0 + 1e-9` at **any** band year.
- If a series' band set is empty, Condition B for that series is `UNDETERMINED` and the construct test overall
  is **not** `CONSTRUCT-EQUIVALENT`.
- No other filter, no winsorising, no smoothing, and no exclusion of non-monotone years.

### 6.3 Crossing condition (Condition C)

- Thresholds: **90** and **95** percent. Both are evaluated.
- **First-sustained crossing** at threshold `T`: the first year `y` such that **every** year `y, y+1, …, y+4`
  has value `≥ T` (five consecutive years at or above), mirroring the on-disk rule
  ("observed first-sustained crossing (>=5 consecutive years above)",
  `10_massification/relations/data/UNIVERSALIZATION_TIMING.csv:21`) and M1-NER §6.
- `FLOW` is evaluated on 1970–2025; `STOCK` on 1975–2025. If no such `y` exists by 2025, report
  `none_by_2025`. `first-at-or-above` is also reported for transparency and is **not** the crossing used in
  the verdict.
- For each threshold: if both series have a crossing, `delta = |STOCK_year − FLOW_year|`; the component is
  **MET** iff `delta ≤ 1 y` and **NOT MET** iff `delta ≥ 2 y`.
- **Undefined-crossing convention (fixed before the run):** if **exactly one** series has no crossing at `T`,
  the component is **NOT MET** (an undefined difference cannot satisfy a ≤ 1 y bar). If **both** have no
  crossing at `T`, the component is **MET** for that threshold and this is recorded explicitly.
- Condition C is **MET** for a series iff **both** thresholds are MET. It is MET overall iff it is MET on
  **both** test types. Component results in every output file are written `MET` / `NOT_MET` / `UNDETERMINED`,
  never `PASS` / `FAIL` (so that the forbidden-string guard G7 has no collision with a component word).

### 6.4 The `SYN28`-specific disclosure

`SYN28` is a high-income type; its primary `FLOW` may reach the 85–95 band, leave it, or never sustain a
crossing at 95 before 2025. The undefined-crossing convention of §6.3 is the whole handling of that
possibility: it is declared **now**, it is not decided after seeing the series, and it cannot be relaxed.

### 6.5 Decision rule and verdict vocabulary (closed set)

```
CONSTRUCT-EQUIVALENT          iff  B(T1) MET and B(T2) MET and C(T1) MET and C(T2) MET
BLOCKED-MEASURE(N2-BAND)      iff  any band condition NOT MET and no crossing condition NOT MET
BLOCKED-MEASURE(N2-CROSSING)  iff  any crossing condition NOT MET and no band condition NOT MET
BLOCKED-MEASURE(N2-BOTH)      iff  a band condition and a crossing condition are both NOT MET
BLOCKED-MEASURE(N2-EMPTY)     iff  a band set is empty (Condition B UNDETERMINED)
```

- `BLOCKED-*` is **terminal**. It is never a result, never a model failure, never a country finding, and is
  never upgraded by relaxing a rule (N6; `HKG_TRANSFER_PRE_DECLARATIONS.md` §4).
- **`PASS`, `VALIDATED`, `ADMISSIBLE` (as a bare token), `SUPPORTED` and `HOLDS` are forbidden output strings**
  for the construct test. The equivalent positive state is spelled `CONSTRUCT-EQUIVALENT` and nothing else.
- `CONSTRUCT-EQUIVALENT` clears the **construct** condition only. It does **not** authorise the HKG transfer
  (§8): execution still requires a further Council decision, the full HKG gate (SR-1…SR-9), and the
  checklist §2 hash verification.
- A **`FAIL-RE-FIT`** on the construct test's own run (any moved parameter, any changed threshold/target/
  tolerance, any added free parameter, any target-year reference in the module or in an operand) overrides any
  component result and voids the run.

### 6.6 Descriptive panel-wide sensitivity (reported, never verdict-bearing)

The same band rule is additionally applied to **all 30 synthetic countries × 4 levels**, each year with a
complete window and `85.0 ≤ FLOW ≤ 95.0`, and labelled `DESCRIPTIVE-SENSITIVITY`. It is reported as a scope
caveat and **cannot** change the §6.5 verdict in either direction. Unlike M1-NER, it is **not** offered as
evidence about the anchor's representativeness; it is a display of the construct's behaviour across the panel.

### 6.7 What the construct test does **not** compare

No observed HKG series, no observed PHL series, no crossing from `UNIVERSALIZATION_TIMING.csv`, and no
1974/1979 quantity enters the construct test. The test compares a **synthetic** stock reconstruction to a
**synthetic** flow analogue. It is a measurement/construct test on the simulator's own interface.

---

## 7. N3 — direction, pre-registered (written before any run)

### 7.1 The direction

D114 established that the cohort-flow analogue **leads** a stock-style object by **2–3 y** at the crossings
(≥90: flow 2007 vs stock 2010 = 3 y; ≥95: flow 2016 vs stock 2018 = 2 y) and sits **above** it in the band (all
15/15 band expansion years; mean `stock − flow` = **−1.751664 pp**). **A stock object can therefore only move
crossings later.** It cannot move them earlier by construction: a stock at `t` is a weighted backward average
of entry cohorts (§3.1–§3.2), so for a rising series `STOCK(t) ≤ FLOW(t)` and the year at which `STOCK` first
sustains a threshold cannot precede the year at which `FLOW` does.

### 7.2 What that implies for the transfer (pre-registered)

- A **`TRANSFER-FAILS`** on a stock object — model crossings later than the recorded HKG years by more than
  ±5 y — is **expected and confirmatory**. It is **not** a new finding, **not** an HKG finding, and **not** a
  surprise to be explained away. It is the direction D114 already measured.
- A **`TRANSFER-HOLDS`** on a stock object is the **more informative** outcome, precisely because it is the
  harder one: it would mean the frozen parameterisation places the two primary NER crossings within ±5 y even
  after the measure has been moved in the direction that hurts.
- This ordering is written **before** the run and may not be reversed in a FINDINGS file. A `TRANSFER-FAILS`
  may not be presented as a discovery, and a `TRANSFER-HOLDS` may not be presented as a validation.

### 7.3 The wedge, pre-registered in sign (and its two components)

The object admits an exact algebraic decomposition (algebra, not a result):

```
STOCK = FLOW_w * sigma_bar
FLOW_w   = 100 * SUM(A over window) / SUM(C over window)          window-average entry rate
sigma_bar = SUM(A*w) / SUM(A)                                     weighted mean holding weight
```

- `sigma_bar < 1` whenever `survival < 1`, and `sigma_bar → (d−1+s)/d` in the endpoint-only schedule, which is
  the **largest** value any admissible non-increasing schedule with `w_0 = 1`, `w_d = s` can give. Hence
  `STOCK ≤ FLOW_w` for every `s < 1`, with slack of order `(1 − sigma_bar) * FLOW_w`.
- `FLOW_w ≤ FLOW(t)` whenever the entry rate is rising, by the backward-window/ramp term quantified in M1-NER
  §4 (~2–3 y, of order `delta*(d−1)/2` on a linear ramp).

**Pre-registered expectation (not a measurement):** the band difference is expected to be **systematically
negative** (stock below flow) and **dominated by the holding-weight term**, because the frozen panel's primary
`survival` is materially below 1 throughout 1975–2025 — `SYN00_PHL_LIKE` **0.7171–0.9241**,
`SYN28` **0.6830–0.8232** (a through-level rate, §3.5; these are input-column ranges, not test statistics).
The construct test's 2.0 pp bar is therefore a **demanding** bar for an
object of this kind, and a `BLOCKED-MEASURE` outcome is a **live possibility that this document accepts in
advance**. The sign is pre-registered; the magnitude is **not** predicted, not computed here, and not
extrapolated from the §11 illustration. **If the magnitude is large, the design's conclusion is that the
model's flow object cannot stand in for a stock NER — not that the bar should move.**

---

## 8. N4 — what this document does and does not authorise

**This document does NOT authorise execution of the construct test or of any HKG transfer.** D120: "execution
NOT authorised (further controller action after freeze + checklist §2 hash verification)". Specifically:

1. **No run.** No stock value, band year, difference, crossing, or output file of the construct test exists in
   this directory. `results/` does not exist.
2. **No HKG run is authorised by `CONSTRUCT-EQUIVALENT`,** if a future run returns it. Clearing the construct
   condition is necessary and not sufficient: the HKG gate still requires **SR-1** (a model that emits a
   declared NER object — this object is such a candidate but is not an emitted model column), **SR-2** (v1.2
   PHL precondition), and **SR-9** (a new Council decision), plus the checklist §2 hash verification and the
   determinism check. D111's authorisation remains **void for every object until H1-equivalence is established
   on that object**.
3. **No carried constraint is discharged here.** §2.4–§2.5 carry H2–H6 and D75 (i)–(vi) because D120 makes
   carrying them a condition of the freeze. This document does not claim H2 compliance, does not claim H3
   status, and does not pre-tabulate the D7–D9 declared values that **H4** requires before an HKG run (that
   tabulation belongs to the HKG run's own predeclaration, under a Council decision).
4. **No D7–D9 value, no declared country input, and no HKG parameter appears in this document at all.**

---

## 9. Outputs that a future, authorised construct-test run must produce

Declared now so that the outputs cannot be shaped after the fact (schemas in `DRY_RUN_PLAN.md` §5):

| file (to be created only under a further decision) | content |
|---|---|
| `results/STOCK_NER_RESULTS.csv` | one row per statistic: `object_definition_id`, `test_type`, `level`, `condition`, `statistic`, `value`, `threshold`, `component_result`, `verdict_bearing`, `label` |
| `results/STOCK_NER_COMPARISON.csv` | year-by-year `country`, `year`, `stock`, `flow`, `diff`, `abs_diff`, `band_member`, `bar_met`, `stock_window_complete`, `role`, `label`, for T1 (`VERDICT`) and T2 (`VERDICT`) |
| `results/STOCK_NER_CROSSINGS.csv` | per test type and threshold: `first_at_or_above` and `first_sustained` for `stock` and `flow`, `delta_years`, `le_1y`, `defined`, `component_result`, `label` |
| `results/STOCK_NER_SENSITIVITY.csv` | the §6.6 panel-wide descriptive band statistics, labelled `DESCRIPTIVE-SENSITIVITY` |
| `results/STOCK_NER_VERDICT.txt` | exactly one token from §6.5, plus the banner |

**Banner carriage (declared).** Every `.md` file in this directory carries the banner in its header. The
run's CSVs carry `label = SYNTHETIC` on **every row**, and the banner is carried in
`results/STOCK_NER_VERDICT.txt`, declared here as the run's **banner carrier** (house convention: EXP-3 and
EXP-8 result CSVs carry a `label` column and the banner travels with the run's documents; a banner repeated in
every CSV row would make the CSVs unparseable). Guard G7 enforces exactly this. **None of these files exists at
freeze time.**

---

## 10. Determinism and hashing

- The construct-test code is deterministic: **no RNG, no seed, no wall clock, no network, no environment
  dependence, no locale dependence, no dict-ordering dependence**. It reads only the files named in §4.1 and
  §5.
- It is run **twice**; all four result files from the two runs must be **byte-identical** (`sha256` equality).
  Run 1 writes `results/`; run 2 writes `_determinism/run2/`. Both are retained.
- The run **refuses to start** unless: this file's sha256 matches `RUN_MANIFEST.json → predeclaration_sha256`;
  every input's sha256 matches `RUN_MANIFEST.json → inputs`; the panel schema matches §4.1 (6 720 rows, 67
  named columns, every `label = SYNTHETIC`); and guards G1–G8 of `DRY_RUN_PLAN.md` §6 pass.
- `RUN_MANIFEST.json` (this directory) records the sha256 of this file, of `STOCK_NER_DESIGN.md`, of
  `DRY_RUN_PLAN.md`, and of every cited input, **before any run**. `SHA256SUMS.txt` carries the same values in
  `shasum -a 256 -c` format, relative to the programme root.
- **This document contains no timestamp, hostname, process id, or path-dependent value in any computed field**
  (there are no computed fields). Its own hash is the freeze token.

---

## 11. N5 / N6 — labels, limits, and the sentences that must travel

### 11.1 N5 — no observed-validation claim at the target window

- The object **cannot be validated against observed HKG data in 1971–1996**. `ner_primary` exists for
  1971–1985 and 1995–1996 (17 observations in that window, 24 in the full record), and the D75 target years are
  inside it — but the object is a **synthetic** construction, and no observed series enters it.
- The only observed cross-check that exists at all is **2012–2018** (`ger_primary` exists 2001–2024;
  `ner_primary` exists 2012–2018 with an overlap of **7 years**, NER **88.5–99.2**). Those 7 years are
  **saturated**: at NER 88.5–99.2 a stock NER and any reasonable flow analogue are both near their ceiling, so
  agreement there would be uninformative and disagreement there would be uninterpretable. **The 7-year
  saturated overlap is not a substitute for the missing target-window validation**, and no claim of validation
  is made anywhere.
- **HELD DATA ASK — never fabricated, never derived from the target:** a **HKG single-age population series
  for 1971–1996**. It is needed **only** for an observed cross-check of the reconstruction (an age-band
  denominator), **not** for the object — the object's denominator is the model's own `cohort` column. Until it
  is supplied, the observed cross-check cannot be built at the target window, and this document builds
  nothing in its place.
- Nothing in this directory imputes, interpolates, back-casts, or reconstructs an observed HKG series, a
  completion series, a population series, or a crossing.

### 11.2 N6 — the label block (every output, every table, every caption)

> `SCALING: FAIL (standing, A12/B02) — DIAGNOSTIC-TRANSFER ONLY — NOT EVIDENCE`

> **No HKG result exists until one is produced; nothing here licenses a portability, capacity-timing, or
> phase-verdict claim.**

Verdict vocabulary, wherever a token is emitted: `DIAGNOSTIC-TRANSFER` only, in the closed set
`TRANSFER-HOLDS` / `TRANSFER-FAILS` / `FAIL-RE-FIT` / `BLOCKED-*` (never `PASS`); for the construct test, the
closed set of §6.5. `BLOCKED-*` is **terminal** and is never reported as a result, a model failure, or a
country finding.

### 11.3 Per-file label block

Every file in this directory states, in its header: `SYNTHETIC` for every model-derived value;
`OBSERVED-REFERENCE-ONLY` for anything read from an observed series; the banner of §11.2; the
`DIAGNOSTIC-TRANSFER` vocabulary restriction; and that `BLOCKED-*` is terminal.

---

## 12. Freeze statement

This file was written **before** any computation of the object, any band test, any crossing, and any HKG input
assembly. **No result exists at the time of writing.** Its sha256 is recorded in `RUN_MANIFEST.json` as
`predeclaration_sha256` and in `SHA256SUMS.txt`; the run refuses to start unless the on-disk hash matches.

**If a rule here turns out to be wrong, the correct action is a new predeclaration under a new Council
decision — never an edit to this file.**

**Design verdict: `PRE_DECL-FROZEN`.** **Construct test: not executed — `NOT-RUN-NOT-AUTHORISED`.**

**No HKG result exists. No HKG run is authorised. No portability, capacity-timing, or phase-verdict claim is
made or implied.**
