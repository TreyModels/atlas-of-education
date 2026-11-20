# FINDINGS — EXP-23 **D63-BOUNDS**

**`LABEL: OBSERVED`** for the UIS completion values; **`DERIVED`** for every logarithm, share, required value,
interval and verdict; **`DECLARED-THRESHOLD`** for the 90 pp comparison level; **`CITATION-ONLY`** for the single κ
value. **No model was run.**

Worker **D63** · 2026-11-21 · Council brief 025 (**D156 #3**, rank **#3**), `SYNTHESIS_025.md` §6.3, anchored by
**D153(xiii)**. Predeclaration: [`PRE_DECLARATIONS.md`](PRE_DECLARATIONS.md), sha256
`dc714963f9c4273ebc36837d50bb98542dba98bf1d66c7b7a3ce076d36efad36`, **hashed before the run and enforced by the
runner at verdict time** (D158 rule one). No threshold, comparison, outcome rule or verdict string was changed after
results. The five quoted regions of the brief and the decisions were **re-extracted from the frozen sources by the
runner** and matched byte-for-byte before any computation.

Files: [`code/run_d63_bounds.py`](code/run_d63_bounds.py) ·
[`results/D63_BOUNDS_RESULTS.csv`](results/D63_BOUNDS_RESULTS.csv) ·
[`results/D63_BOUNDS_DETAIL.csv`](results/D63_BOUNDS_DETAIL.csv) ·
[`RUN_MANIFEST.json`](RUN_MANIFEST.json) · [`SHA256SUMS.txt`](SHA256SUMS.txt).

---

## 1. The answer in plain English

Philippine upper-secondary completion was **75.02525329589844** in 2024, against a declared 90 pp level — a gap of
**14.974747 pp**. Splitting the **log** gap at the declared one-stage pair (upper 2024 against lower 2021) gives
**58.6008 % pipeline level / 41.3992 % transition ratio**. Two channels, neither of which alone closes the gap.
**`RESIDUAL-SPLIT`.**

Then three comparisons against what the record actually contains:

- **The pipeline channel does not fit inside the record.** At the 2024 ratio, lower-secondary completion would have
  had to reach **97.042584 pp**. The highest lower-secondary completion anywhere in the observed series is
  **92.4139633178711** (2024). The required value is **4.628621 pp above it** — outside the observed envelope.
- **The ratio channel does fit inside the record.** At the record's 2024 lower completion (92.4139633178711), the
  transition ratio would have had to be **0.973879**. The observed eight-pair range is **0.889–1.072**
  (0.8891573087274445 to 1.0724421619315192). The required ratio is **inside** it.
- **The level itself is not excluded by the record.** At the record's highest lower completion, the observed ratio
  range implies an upper-completion interval of **82.170551 to 99.108631 pp**. That interval **contains** 90.

Two comparisons inside, one outside → **`BOUNDS-EDGE`**. Read plainly: **the record bounds the residual on the
transition-ratio channel and not on the pipeline channel.** The lower series the required level needs is not in the
record; the ratio that level needs is. So the record neither contains the required path nor rules it out — and the
90 pp level sits **inside** the interval the record's own ratio range implies, not outside it.

**D63 stays `UNABLE as to cause`.** The split is descriptive. It says where the arithmetic sits, not why.

---

## 2. The split

| element | value | label | source |
|---|---|---|---|
| upper-secondary completion 2024 | 75.02525329589844 | `OBSERVED` | series, `completion_upper_secondary`, `year=2024` |
| lower-secondary completion 2021 | 80.89604949951172 | `OBSERVED` | series, `completion_lower_secondary`, `year=2021` |
| gap to 90 | 14.974747 pp | `DERIVED` | 90 − upper 2024 |
| `G = ln(90 / upper_2024)` | 0.18198490285627197 | `DERIVED` | log gap |
| `P = ln(90 / lower_2021)` | 0.1066446793553944 | `DERIVED` | pipeline level |
| `Q = ln(lower_2021 / upper_2024)` | 0.07534022350087775 | `DERIVED` | transition ratio |
| `P + Q` minus `G` | floating point only | `DERIVED` | identity residual, in DETAIL |
| **pipeline share** | **0.586008 (58.6008 %)** | `DERIVED` | `P / G` |
| **ratio share** | **0.413992 (41.3992 %)** | `DERIVED` | `Q / G` |
| split verdict | `RESIDUAL-SPLIT` | `DERIVED` | both shares inside the declared band |

**The split is an accounting identity with zero free parameters and zero residual by construction.** It is a product
decomposition of one log ratio, not an estimated attribution: the two shares add to one, and nothing was fitted to make
them do so. The band test is the block's own: both shares must lie between one-third and two-thirds, and they do
(0.586008 and 0.413992). The `THIN` rule does not bind — the ratio range rests on eight pairs, above the declared floor
of three — but the rule was checked in code, not assumed.

---

## 3. The three bounds

Each comparison is a statement about **the observed record's envelope**, evaluated in full precision with no
tolerance, no epsilon and no band. Equality would count as inside; no comparison is near enough for that to matter.

| id | required / implied | record envelope | outcome |
|---|---|---|---|
| **B1** | lower completion needed at the 2024 ratio: **97.042584** pp | highest observed lower completion: **92.4139633178711** (2024) | **`OUTSIDE`** (+4.628621 pp) |
| **B2** | ratio needed at the 2024 lower completion: **0.973879** | observed eight-pair range: **0.889–1.072** | **`INSIDE`** |
| **B3** | upper completion implied by that range at the record's highest lower completion: **82.170551 – 99.108631** pp | the 90 pp level | **`INSIDE`** (the interval contains 90) |

**Bounds verdict: `BOUNDS-EDGE`** — one channel outside the record's envelope, two comparisons inside it. The mapping
from outcomes to label is fixed in the predeclaration (§4 there): all three inside → `BOUNDS-INSIDE`; none inside →
`BOUNDS-OUTSIDE`; mixed → `BOUNDS-EDGE`. The label means "the record contains part of the required condition and not
all of it". It is **not** a proximity-to-threshold label: no margin, tolerance or epsilon exists anywhere in these
three tests, so nothing here is "close".

**Why B2 is the informative one.** The required ratio 0.973879 is not exotic. Observed pairs sit at 0.972965 (upper
2010) and 0.948990 (upper 2013) and at 1.072442 (upper 2017); the record contains ratios on both sides of the required
value. What the record does **not** contain is the **joint** combination — a lower completion at the record maximum
together with a ratio near 0.9739. The 2024 pair itself ran at 0.927428. So B2/B3 say the required ratio is
arithmetically available in the record's own range; they say nothing about the world producing that combination.

---

## 4. Verdicts

| layer | verdict |
|---|---|
| split | **`RESIDUAL-SPLIT`** |
| bounds | **`BOUNDS-EDGE`** |
| D63 | **`UNABLE as to cause`** — fixed by the block, D153(vi) and D153(xiii); no outcome of either verdict changes it |

The two layers are reported separately because the block and D156 ask for both. Its falsifier did not fire: the
2024/2021 pair is present, unduplicated, and `status = observed`.

---

## 5. What this does NOT establish

- **No cause.** D63 stays `UNABLE as to cause`. The split names two accounting channels; it does not say what produced
  either of them, and it is not a re-attribution of D63.
- **Nothing about whether the ceiling is structural — in either direction.** The record does not establish that it is
  structural, and it equally does not establish that it is not. The barred sentence cannot be written; neither can its
  mirror image. What the cell shows is narrower: the 90 pp level sits **inside** the interval the record's own ratio
  range implies at the record's highest lower completion, so the record cannot deliver that verdict either way.
- **Not evidence that the level was reached in fact.** B2 and B3 are arithmetic on observed numbers **combined across
  different years**. The implied interval's endpoints come from different pairs, and the joint combination was never
  observed. An interval containing 90 is not evidence that 90 would have been reached; no counterfactual is claimed and
  no direction is implied.
- **No model comparison.** The delivered deviation count, the generator panels and the participation objects are
  outside this cell. No model value enters any bound; the one generator number on disk is a `CITATION-ONLY` row and is
  not used. The size of any behavioural miss remains undecomposable (that is EXP-21's object, not this one).
- **Nothing about the lower level.** This is an **upper-level leg by construction**. It may not be cited as evidence
  about the lower-secondary level or about any two-level object (D158 rule four).
- **No forecast, no policy target, no required state.** The two values called "required" are arithmetic inversions of
  the identity, labelled `DERIVED`, not `REQUIRED-STATE` objects. They are not targets and were not adopted.

---

## 6. Honest limits

1. **Eight Philippine pairs.** The observed ratio range is a **PHL** range from eight pairs. It is the block's declared
   range and it is consumed as a range, not re-tested — no in-band test was recomputed, no CEIL-ATTRIB verdict was
   touched — but it is a thin, single-system object and the bounds inherit that.
2. **The declared lag is a choice, and the split depends on it.** The realised pairs are not all at the exact
   three-year lag: the declared ±1 y tolerance was used where the exact lag was missing. The consequences are not
   cosmetic. At the **contemporaneous** lower value (92.4139633178711, 2024) instead of the 2021 value, the pipeline
   share is **−0.145443** and the ratio share is **1.145443**, with an observed same-year ratio of **0.811839** — the
   pipeline term changes sign, the 2024 lower completion already sitting above the 90 pp level. The 58.6008 % figure is
   therefore a statement **about the declared one-stage pair**, not a lag-free property of the residual. Any citation
   of the split must carry that sentence. The sensitivity is `DESCRIPTIVE / NOT-VERDICT-BEARING` and changes no verdict.
3. **The record maximum is contemporaneous with the residual.** The record's highest lower completion is the 2024 cell,
   the same year as the upper cell in the residual. B1 therefore compares a 2021-based requirement with a 2024 maximum;
   that is the block's declared construction, and it is the most favourable envelope available, so the `OUTSIDE` result
   does not rest on an outdated maximum.
4. **The threshold is declared, not observed.** 90 pp is the D34/A6 crossing bar (90/90/90 pp). Nothing here says 90 is
   the right level for upper secondary; it is the level the phase verdict uses, and the cell takes it as given.
5. **Three of the eleven observed upper years cannot enter the pair set** — no lower observation sits within the
   declared tolerance of the exact three-year lag for them. The pair set is the block's eight, not a census.
6. **The identity is exact, which is not the same as informative.** Zero residual by construction means the split
   cannot fail; what can be wrong is the reading put on it. The band and the bounds are the tests; the identity is
   bookkeeping.

---

## 7. What this changes for the write-up

- The sentence calling the upper-secondary ceiling structural **cannot be written**. Neither can a sentence asserting
  the opposite. That is the cell's contribution to the spine: it removes a sentence and supplies no replacement
  verdict about the world.
- The write-up **may** carry, with these numbers and their provenance: the residual is **14.974747 pp**; the log gap
  splits **58.6008 % pipeline level / 41.3992 % transition ratio** at the declared one-stage pair; the lower completion
  required at the 2024 ratio is **97.042584 pp**, which is **4.628621 pp** above the record maximum
  **92.4139633178711**; the ratio required at the record's 2024 lower completion is **0.973879**, **inside** the
  observed eight-pair range **0.889–1.072**; at the record's highest lower completion that range implies an
  upper-completion interval of **82.170551–99.108631 pp**, which contains 90; verdict **`BOUNDS-EDGE`**.
- Every one of those sentences must carry the lag sentence from limit two, and **D63 stays `UNABLE as to cause`.**

**Mandatory sentences carried by this cell** (from the predeclaration's register):
**"D63 stays `UNABLE as to cause`."** · **"The observed ratio range is consumed as a range; it is not re-tested."** ·
**"The split is an accounting identity with zero free parameters and zero residual by construction."** ·
**"No model was run and no model value enters any bound."**

---

## 8. Reproduction of the Council's stated numbers

All eleven stated values reproduce under the predeclared rounding rule (a value stated to *d* decimals is reproduced
iff the difference is at most half a unit in the last stated place). Full table with recomputed values and differences
in `results/D63_BOUNDS_DETAIL.csv` (rows `R_*`). The cells stated at full stored precision (R1, R2, R8) reproduce
exactly. The largest difference anywhere is **0.000442**, on the range maximum stated to three decimals — inside the
rule, and the least comfortable of the eleven. No block number was adjusted, and no number from this cell was
substituted for a Council number.

---

## 9. Discipline and determinism

- **No model run, no re-fit, no adoption, no proxy, no grid, no web.** Nothing outside this experiment directory was
  written; every input was opened read-only and hash-checked before computation.
- **Determinism:** two runs (`results/` and `results/determinism_run2/`) are **byte-identical** — the results table, the
  detail table and the console log all match, hash for hash (`RUN_MANIFEST.json`, `determinism` block).
- **Provenance:** every number in this document appears in `results/D63_BOUNDS_DETAIL.csv` with its path, column, filter
  and derivation; the runner's number-register check confirms it, and reports zero unmatched tokens and zero banned
  strings in this file and in both result tables.
- **Labels:** `OBSERVED` for the completion cells; `DERIVED` for every product; `DECLARED-THRESHOLD` for 90 pp;
  `CITATION-ONLY / window-only` for κ = 0.949135. **No causal claim and no direction claim is made anywhere in this
  document.**
