# EXP-19 PLACES-BOUND — FINDINGS

**Verdict: `PROXY-SILENT`.** The observed record on disk does **not** bound EXP-17's required coverage.
The required state remains a **`DECLARED` / `REQUIRED-STATE (EXP-17)`** object that must carry its own
label and sensitivity; the **HELD** places ask stays **HELD**. No norm, coverage path or λ is adopted.
No causal or direction claim is made.

**Predeclaration:** `PRE_DECLARATIONS.md`, sha256 `22786090d91598cb03d04ae081c48ec41aa664bae8a1bd40d33aa77de7e1d25f`
(frozen before execution; verified by the runner). Determinism: two independent runs, all five result files
byte-identical.

---

## 1. What the cell asked, in one paragraph

EXP-17 identified a **required state**: one coverage path that satisfies both lower channels, with required
`seats/cohort` **0.759712** at the 2018 entry year and **0.873523** at the 2021 completion year (`DERIVED`;
`REQUIRED-STATE (EXP-17)`; the `DERIVED` target **0.8076** travels with it). EXP-19 asks a narrower, measurement
question: **is that level inside anything the programme can observe on disk today**, or can it only be declared?
A direct place count would answer it. D146 establishes that no place count is on disk: the delivery rows for public
schools and completed classroom construction are `unable`, and `number_of_classrooms_by_year` /
`number_of_public_schools_by_year` are `unable`. What is on disk is a **class-size / PTR / enrolment description**.
The cell declares **one** conversion family from that description to an implied `seats/cohort`, declares the **three
norm class sizes {40, 45, 50}** (none adopted), and compares the implied interval with the required state under
frozen rules.

## 2. The numbers (all `DERIVED` from `OBSERVED` inputs)

Implied `seats/cohort` under the declared family (F1: rooms = enrolment ÷ observed students-per-classroom ratio;
places = norm × rooms; coverage = GER × norm/divisor):

| required year | norm 40 | norm 45 | norm 50 | required at that year |
|---|---:|---:|---:|---:|
| 2018 (entry) | 0.952760 | 1.071855 | 1.190950 | **0.759712** |
| 2021 (completion) | 0.780606 | 0.878182 | 0.975757 | **0.873523** |

Interval across the two required years, and its relation to the required state `R = [0.759712, 0.873523]`:

| norm | `I_n` = [min, max] | classification |
|---|---|---|
| 40 | [0.780606; 0.952760] | `STRADDLE` (overlaps `R`, but does not contain it) |
| 45 | [0.878182; 1.071855] | `OUTSIDE` (the whole interval is above `R`) |
| 50 | [0.975757; 1.190950] | `OUTSIDE` (the whole interval is above `R`) |

Gaps at the required points: at **2018** the proxy is **+19.30 / +31.21 / +43.12 pp** above 0.759712 under norms
40/45/50; at **2021** it is **−9.29 / +0.47 / +10.22 pp** relative to 0.873523. The closest single cell is
**2021, norm 45: 0.878182**, only **0.466 pp** above the required 0.873523.

**Do not read the table as "the proxy excludes the requirement."** The frozen rules do not return that label, for
two reasons set out next.

## 3. Why the verdict is `PROXY-SILENT`, not `PROXY-EXCLUDES`

**Reason 1 — the conversion is not identified at the required object.** The level-matched divisor for lower
secondary (`classroom_student_ratio_junior_high_school`) is observed at **2010, 2019, 2021**. The level-matched
enrolment ratio (`ger_lower_secondary`) is observed only through **2018**. **The two year sets do not intersect**:
there is **no year on disk** with a same-year, level-matched pair. At the 2018 required year the divisor is carried
from **2019** (one year); at the 2021 required year the enrolment ratio is the **broader `ger_secondary`**
(`LEVEL-FALLBACK`), because `ger_lower_secondary` stops at 2018. The predeclared identification gate therefore
**FAILS at both required years**, and the block's own clause — *"`PROXY-SILENT` if … the conversion is not
identified"* — controls. The intervals above are a **non-verdict-bearing sensitivity**, not a bound.

**Reason 2 — even setting the gate aside, the arithmetic does not justify the stronger label.** The sensitivity is
2 of 3 norms `OUTSIDE` and 1 `STRADDLE`; the block's headline would call that `PROXY-EXCLUDES` (≥2 of 3), but its
own gloss says the proxy rules the required coverage out **under every declared norm**, and the **narrower** label
wins under D147(c)(i). Norm 40 **straddles** the required state, and the 2021 norm-45 cell is **0.466 pp** from the
required value — with the 2018 required value lying **below** the proxy and the 2021 required value **inside** it.
The sign of the comparison **flips between the two required years** under the same family. Calling that
"excluded" would overclaim: it would convert a one-year carried divisor and a broader-level fallback into a
statement about the required lower-secondary object. The honest reading is that the proxy **cannot discriminate**.

> **Non-verdict-bearing counterfactual, reported for the Council:** if the identification gate were ignored and the
> block's ≥2-of-3 headline applied, the sensitivity arithmetic would read `PROXY-EXCLUDES` (2 of 3 outside). The
> frozen precedence returns `PROXY-SILENT`; the counterfactual is recorded so the Council can see the difference,
> and it is **not** the verdict.

## 4. What this means for EXP-17's required state

- **The required state is not refuted, and it is not validated.** This cell says only that the observed record
  cannot bound it. `REQUIRED-STATE (EXP-17)`, the `DERIVED` target **0.8076**, and the `λ*`-implied values
  **0.759712 / 0.873523** stand exactly as D148 recorded them; **no λ is adopted** and none is installed as a
  parameter.
- **The successor's coverage declaration must be `DECLARED`, with a sensitivity.** A `PROXY-BOUNDS` verdict would
  have allowed a `DERIVED` proxy with its distortion stated and would have downgraded the HELD ask to a validation
  item. That is **not** what happened. The successor may cite the required state as a **required state**, but if it
  declares a coverage path it must label it `DECLARED` and show how the level statement moves with it.
- **The level statement is conditional on the coverage declaration.** The cell does not say the lower defect is
  "really" a coverage defect or that coverage would raise completion; it preserves D140's JOINT label and D148's
  scope flag (the required state is internal-consistency, not an external standard, policy target or forecast).
- **The required state is at the edge of, not outside, the observed regime.** The 2021 norm-45 cell (0.8782 vs
  0.8735) and the 2018 norm-40 cell (0.9528 vs 0.7597) show that the requirement is not an absurd number relative
  to observed class sizes; the problem is that the observed record cannot pin the same object at the same level and
  year. "Silent" means **unidentified**, not "impossible".

## 5. What this means for the HELD places ask

- **The HELD places / measured seats-vs-enrolment series stays `HELD`.** It is **not** downgraded to a validation
  item, because downgrading was conditional on `PROXY-BOUNDS`. Capacity utilisation, private/public shares, SHS
  voucher take-up and the rest of the D135/D146 list are untouched and named.
- **The proxy route is closed** so that no future worker spends a cycle on it: a class-size/PTR ratio is not a place
  count, and the declared conversion cannot identify the required object on this record. This is the block's
  intended use of `PROXY-SILENT`.
- **HELD is the only route to a measured place count.** A measured classroom/school stock, or a year that observes
  both the JHS class-size ratio and `ger_lower_secondary`, would change the answer (see §7). Neither is on disk.
  **No external request was made; user approval is required for any HELD item.**
- **D146 stands unchanged:** the places object is not on disk as a count; no proxy substitution outside this cell;
  this cell adopts nothing.

## 6. Honest limits

1. **The proxy is not a place count.** It is an implied `seats/cohort` built from a **national average of a ratio**,
   not a room census. It cannot see double shifts, room condition, rented/anchor rooms, unused rooms or whether a
   "seat" is adequate.
2. **GER is gross enrolment / cohort**, not seats / cohort; it includes overage and repeaters. The bridge from one to
   the other is the declared assumption that one enrolled student occupies one place at the norm class size.
3. **The two required years are not converted on the same enrolment object.** 2018 uses the level-matched
   `ger_lower_secondary`; 2021 uses the broader `ger_secondary` (`LEVEL-FALLBACK`). That is a declared
   inconsistency, not a reconciled number.
4. **The 2018 divisor is carried from 2019.** There is no 2018 class-size observation. No interpolation is done;
   the year is flagged in `PLACES_BOUND_DETAIL.csv`.
5. **The five 2021 congested-share values are shares, not counts**, and the block declares no region key. They are
   `OBSERVED`, reported, and **not used** in the verdict.
6. **The PTR route is a declared variant, not a second estimate.** One-teacher-per-classroom is contradicted by
   the on-disk pair PTR-24 vs JHS class size 39–44 (≈1.6–1.8 teachers per room at secondary). The PTR variant is
   reported (2018: 1.548/1.742/1.935 under norms 40/45/50) and is **not** verdict-bearing. 2021 has no PTR within
   ±1 year (last observed 2017).
7. **The backlog and flow cannot form a coverage ratio.** 110,954 classrooms needed (2019) and 10,000/year are
   `OBSERVED`, but there is no observed base room stock and no observed lower-secondary cohort count; using them to
   build a `seats/cohort` would require inventing both. They are context only.
8. **The comparison is cross-object.** `R` comes from a **synthetic** panel (EXP-17); the proxy is an **observed**
   PHL description. The cell asks whether the observed PHL regime is *consistent with* such a coverage level, not
   whether PHL has that exact number.
9. **Level sensitivity is real, and it is why the identification matters.** At the elementary level the implied
   coverage is 1.10–1.63; at SHS 2018 it is 0.85–1.07. The SHS 2018 norm-40 cell (0.8522) even lands inside `R`.
   A different level can bracket the requirement; the **lower-secondary** record cannot pin it. This is reported
   as a sensitivity, never in the verdict.
10. **The three norms are a declared set, not a probability distribution.** No norm is adopted; no interval is
    trimmed; no posterior is implied.

## 7. What would change the answer

A single on-disk year observing **both** the JHS class-size ratio **and** `ger_lower_secondary` would pass the
identification gate at that year and allow a level-and-year exact conversion; the verdict would then be read from
the frozen BOUNDS/EXCLUDES rules. A measured **classroom stock** (the HELD / `unable` count) would remove the
conversion family entirely. Neither is on disk; neither is requested here. **This cell classifies why the HELD ask
is still open; it does not close it.**

## 8. What was not done (closed-claim check)

- **No `phys_cap` change** — `phys_cap` is not in the verdict path; D139/D131 are not re-argued.
- **No fabrication** — `unable` stays `unable`; HELD stays HELD; no classroom, school, cohort, utilisation or
  quality number was invented.
- **No re-fit** — no number was chosen by reference to `R`, to 0.759712 / 0.873523, or to any observed cell.
- **No model run, no generator import, no RNG, no network, no clock in any output.**
- **No level bar** — the ≥17/33 observed-path bar is not read or computed.
- **No causal or direction claim.**
- **Adopt nothing** — three norms declared, none adopted; no coverage path declared for the successor; λ not
  adopted; the HELD places series not replaced.

## 9. Files and reproduction

| file | role |
|---|---|
| `PRE_DECLARATIONS.md` | freeze; verbatim block + conversion family + frozen verdict precedence |
| `PRE_DECLARATIONS.sha256` | hash of the freeze |
| `code/run_places_bound.py` | deterministic runner; refuses to run on a freeze mismatch |
| `code/make_manifest.py` | builds the manifest and checksum list from the delivered files |
| `results/PLACES_BOUND_RESULTS.csv` | every input, required state, implied capacity, intervals, comparison, verdict, blocked/HELD rows, closed claims |
| `results/PLACES_BOUND_DETAIL.csv` | 21 per-year/per-norm cells (primary, PTR variant, broader-GER and level sensitivities) |
| `results/PROXY_DISTORTION.md` | declared assumptions and why the proxy is not a place count |
| `results/determinism_run2/` | second independent run; the five output files are byte-identical |
| `RUN_MANIFEST.json`, `SHA256SUMS.txt` | package manifest and checksums |

Reproduce: from the experiment directory, run
`python code/run_places_bound.py --outdir results` and then
`python code/run_places_bound.py --outdir results/determinism_run2`; compare the five files by sha256. No input
file is written.

---

**One sentence for the Council.** The required coverage is **not bounded** by anything on disk: the class-size/PTR
record is a ratio, not a place count, and the one level-matched conversion it permits is not identified at either
required year — so EXP-17's required state stays a **declared** object, the HELD places ask stays **HELD**, and no
number is adopted.
