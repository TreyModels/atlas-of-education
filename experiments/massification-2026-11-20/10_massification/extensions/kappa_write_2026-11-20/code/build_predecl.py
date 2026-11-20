#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
build_predecl.py -- EXP-24 KAPPA-WRITE (worker KW)

Writes PRE_DECLARATIONS.md.  The EXP-24 block is INJECTED verbatim from
08_council/brief_025/SYNTHESIS_025.md (lines 603-641, the seven numbered items of
section 6.4) rather than retyped, so that no character can drift.  Input hashes are
re-derived here from disk at build time and written into the predeclaration table;
run_kappa_write.py then re-verifies both the table and the files at verdict time.

RUN ONCE.  Re-running after the predeclaration is hashed changes its bytes; the
runner's embedded hash check will then refuse to write a verdict (that is the
intended behaviour, D158 rule 1).

Usage:
  "/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python" code/build_predecl.py
"""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.dirname(os.path.dirname(HERE))    # .../10_massification/extensions
ROOT = os.path.dirname(os.path.dirname(EXT))    # programme root

SYNTHESIS = os.path.join(ROOT, "08_council/brief_025/SYNTHESIS_025.md")
BLOCK_FIRST_LINE = 603
BLOCK_LAST_LINE = 641

UNIVERSE = [
    "10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_RESULTS.csv",
    "10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_DETAIL.csv",
    "10_massification/extensions/kappa_fwd_2026-11-20/results/KAPPA_FWD_SECONDARY.csv",
    "10_massification/extensions/kappa_fwd_2026-11-20/FINDINGS.md",
    "10_massification/extensions/pipe_loo_2026-11-20/results/PIPE_LOO_RESULTS.csv",
    "10_massification/extensions/pipe_loo_2026-11-20/results/PIPE_LOO_PAIRS.csv",
    "10_massification/extensions/pipe_loo_2026-11-20/FINDINGS.md",
    "10_massification/extensions/repro_path_2026-11-20/results/KAPPA_LINK.csv",
    "10_massification/extensions/repro_path_2026-11-20/results/REPRO_PATH_RESULTS.csv",
    "10_massification/extensions/repro_path_2026-11-20/FINDINGS.md",
    "10_massification/extensions/synthetic_2026-11-20/generator_v1_5_bimodal/results/KAPPA_BIND_CELLS.csv",
    "10_massification/extensions/synthetic_2026-11-20/generator_v1_5_bimodal/results/kappa_cap_audit.csv",
    "10_massification/extensions/synthetic_2026-11-20/generator_v1_6_repair/results/kappa_object_audit.csv",
    "10_massification/extensions/synthetic_2026-11-20/generator_v1_6_repair/results/panel_A01D_kappa.csv",
    "08_council/DECISIONS.md",
    "08_council/brief_025/SYNTHESIS_025.md",
    "10_massification/STATUS.md",
]


def sha256_of(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    with open(SYNTHESIS, "r", encoding="utf-8") as fh:
        lines = fh.read().split("\n")
    block = "\n".join(lines[BLOCK_FIRST_LINE - 1:BLOCK_LAST_LINE])
    if not block.startswith("1. **First-order link"):
        sys.exit("BLOCK START DOES NOT MATCH -- refusing to build")
    if not block.rstrip().endswith("a number that changes the negative."):
        sys.exit("BLOCK END DOES NOT MATCH -- refusing to build")

    rows = []
    for rel in UNIVERSE:
        p = os.path.join(ROOT, rel)
        rows.append("| `%s` | `%s` |" % (rel, sha256_of(p)))
    input_table = "\n".join(rows)

    doc = TEMPLATE
    doc = doc.replace("<<BLOCK>>", block)
    doc = doc.replace("<<INPUT_TABLE>>", input_table)
    doc = doc.replace("<<N_UNIVERSE>>", str(len(UNIVERSE)))
    doc = doc.replace("<<N_REMAINDER>>", str(193 - len(UNIVERSE)))
    doc = doc.replace("<<SYNTH_SHA>>", sha256_of(SYNTHESIS))

    out = os.path.join(os.path.dirname(HERE), "PRE_DECLARATIONS.md")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write(doc)
    print("wrote %s" % out)
    print("sha256 %s" % sha256_of(out))


TEMPLATE = r"""# PRE-DECLARATIONS — EXP-24 **KAPPA-WRITE** (worker KW)

**Brief.** Council brief 025, `SYNTHESIS_025.md` §6.4 (EXP-24, rank **#4**), adopted by **D156** (cycle 17);
policy frame **D138** κ `WINDOW-ONLY`, **D133** per-system register, **D142/D143/D153** dispositions,
authoring rules **D158** (seven), **D159** record. Sequence position: EXP-24 runs after EXP-21 (D156 sequencing).

**Status.** `PRE_DECL-FROZEN`. This file was written before any register row or use row was emitted, and is
hashed; `code/run_kappa_write.py` enforces that hash at the moment the verdict is written (D158 rule 1). A
recorded-but-unenforced hash may not carry a verdict.

| field | value |
|---|---|
| cell | EXP-24 KAPPA-WRITE |
| worker | KW |
| object | the per-system transition-ratio κ register, as a **write-up instrument** |
| type | **static register, not a run** — no model execution, no simulation, no re-fit, no estimation |
| inputs | on-disk results and governance texts only (table in §5) |
| writes | `10_massification/extensions/kappa_write_2026-11-20/` **only**; no existing repo file is modified |
| determinism | two runs, byte-identical result files |
| adoption | **none** — nothing here is adopted, re-scored, re-fitted, or turned into a parameter |
| claims | descriptive only; **no causal claim, no direction claim** |

---

## 0. What this cell is, and what it is not

The programme holds one cross-system coefficient: the lower→upper one-stage transition ratio κ, per system
(PHL, KOR, KHM, CHN). D138 ruled it a **within-window description**, never a forward constraint, and D143
fixed it as "a descriptive record and nothing else". A rule that lives only in a decision log is a rule the
next author violates. This cell builds the **register**: every numeric κ use on disk is enumerated, checked
against a **declared window**, and either admitted (with a fixed sentence) or named and barred.

This cell **is not**: a model run; a re-score of EXP-6/EXP-7/EXP-11/EXP-14; a re-fit; a re-opening of the HKG
arm; an external request; a proxy construction; a direction or causal claim; a paper-test slate (D113b); a
generator of new numbers. It produces **citations and boundaries**, not a number that changes the negative.

---

## 1. The EXP-24 block, copied VERBATIM

Injected byte-for-byte from `08_council/brief_025/SYNTHESIS_025.md` lines 603–641 (the seven numbered items of
§6.4) by `code/build_predecl.py`; the synthesis file hash is in §5. The runner re-extracts this fence and
compares it to the synthesis at verdict time. **Where this block and any later section of this document differ,
the block governs.**

<!-- VERBATIM-BEGIN EXP-24 SYNTHESIS_025.md L603-L641 -->
<<BLOCK>>
<!-- VERBATIM-END -->

**Note on label names.** The block's own two outcome labels are `REGISTER-CLEAN` (100 % of numeric κ uses
inside the declared window) and `USE-OUTSIDE-WINDOW` (an object named and flagged; its sentence barred). The
adopted decision **D156** states the verdict set as **`REGISTER-CONSISTENT` > `REGISTER-NARROWED` >
`REGISTER-UNUSABLE`**. Both sets are carried; §9 declares the mapping, and the verdict word written to disk is
D156's, with the block's label reported beside it. The mapping was fixed by the block's own items 2 and 5
(name/flag/bar vs 100 % in-window), **not** by any observed count.

---

## 2. Definitions (declared here; these are the operational reading of the block)

**D1 — κ value.** A numeric literal in the interval `(0, 1]` that is a value of the *per-system lower→upper
transition ratio* κ. A literal qualifies only if it appears in (a) a declared **κ-value column** (§4.1), or
(b) a text position captured by a declared **text pattern** (§4.2), or (c) a declared κ-conditioned object
(§4.4). Values `≤ 0`, `> 1`, and the sentinel `-1` are **not** κ values.

**D2 — κ use.** An application of a κ value to an object at a year, or a statement of the value as the
system's coefficient. A use is registered once per (file, system, year, κ-column) for structured files, once
per (file, line, token) for text, and once per (file, span) for κ-conditioned objects (§4.4).

**D3 — register line.** One row of `KAPPA_WRITE_REGISTER.csv`: a system's κ with its window, its EXP-11
slope/half-shift/hold-out, its admissible use, and a provenance pointing at a **file + column + row key**.

**D4 — window.** For system *s*, the window is the year span of *s*'s **own observed pair set**, in
`upper_year` terms, reported twice as the block requires: `[pre-2021 span]` = first..last `upper_year` with
`upper_year ≤ 2020`; `[full span]` = first..last `upper_year` over all pairs. The `lower_year_used` span is
recorded beside it. The window is **observed, not chosen**: it is derived at run time from
`KAPPA_FWD_DETAIL.csv` and must equal the anchor span or the register line is `UNVERIFIED`.

**D5 — non-entrant.** HKG and JPN have **zero** completion pairs on disk (`NON-ENTRANT`, D135/V14). Their
window is **empty**. Any κ use attributed to them is **out-of-window by definition**; no proxy is permitted
(D118), and none is made.

**D6 — projection.** Any of: (i) a κ value applied to a year **outside** its system's window; (ii) a κ value
applied to a series that is **not** the observed pair series (e.g. a model-generated `lower` series); (iii) a
statement that computes a future or outside-window quantity from κ (`κ-implied upper max for 2027`, `κ predicts
…`, `κ constrains …`). Projection is a **use-class**, not a verdict word, and it is counted separately.

**D7 — in-window.** A use is **in-window** iff **all** hold: (a) its system has a non-empty window; (b) if it
carries a year, that year lies inside the full span; (c) its value passes the test that matches its **role**;
(d) it applies κ to the **observed pair series** and not to a model-generated series. The role-specific value
tests are declared here, before the run, and are three distinct tests rather than one loose one:

* **(c-i) quotation of the coefficient** (`full`, `pre`, `half1`, `half2`, `declared-4dp`, `median-ratio`,
  `text`): within `max(0.005, 1 % of the register value)` of that system's `kappa_full` or `kappa_pre` — a
  rounding of the register value at the precision quoted, which admits two-decimal and two-significant-figure
  quotations alike (`0.95`, `0.60`, `0.7222`, `0.949135`). A quotation failing this is **unattributable**, and
  out-of-window.
* **(c-ii) within-window estimator** (`loo`): inside the system's **observed ratio range** `[min, max]` over its
  own pairs. A leave-one-out median is not the register value and must not be forced to equal it; but a value
  outside the range of the pair set it estimates is not a value of that set.
* **(c-iii) applied bound** (`pre` as a hold-out bound, `link-primary`, `link-sensitivity`, `applied`): the
  applied coefficient is the system's declared κ **by construction** — the bound is `κ × object` — so the year
  test (b) governs and no value test is applied.

A use with **no stated year** that passes (a), (c), (d) is a statement *about* the window (a description of the
coefficient) and is in-window by definition: it cannot place κ outside a window it does not name.

**D8 — object identity (D158 rule 2).** κ is defined on the **observed** ratio
`completion_upper(t) / completion_lower(t−3)`. A κ-conditioned object whose `lower` series is model output is a
different object; it is recorded as `object_identity = MODEL-SERIES` and is **`NOT-COMPARABLE`** to the
register, so it can neither ground nor corroborate a write-up sentence about κ — even in a year inside the
window.

**D9 — κ-elasticity is a different object.** The programme also writes κ for the model's congestion elasticity
(`G(C) = C^κ`, `κ ∈ [0.5, 1.0]`, D60). That symbol is **not** the transition ratio. Lines where it appears are
recorded once as `OUT-OF-OBJECT` with file+line, are **excluded from the window denominator**, and are counted
and reported. Excluding them is object identity, not convenience: the two objects have different units,
different sources and different decision histories.

---

## 3. Register schema (`results/KAPPA_WRITE_REGISTER.csv`)

One row per system in the declared system set `{PHL, KOR, KHM, CHN}` (4 rows; HKG/JPN appear as
`NON-ENTRANT` rows with an empty window and `admissible_use = NONE`). Columns:

| # | column | content / rule |
|---:|---|---|
| 1 | `iso3` | `PHL`, `KOR`, `KHM`, `CHN`, `HKG`, `JPN` |
| 2 | `system` | name as in the delivered file |
| 3 | `n_pairs` | count of observed pairs (must match 8 / 19 / 11 / 5) |
| 4 | `n_pre2021` / 5 `n_holdout` | pre-2021 and post-2020 pair counts |
| 6 | `kappa_full` | median ratio over the full window (8 dp) |
| 7 | `kappa_pre` | median over the pre-2021 subset (8 dp) |
| 8 | `window_pre2021_upper` | `first..last` upper_year of the pre-2021 subset |
| 9 | `window_full_upper` | `first..last` upper_year of the full set |
| 10 | `window_lower_span` | `first..last` `lower_year_used` |
| 11 | `slope_ratio_per_year` | EXP-11 leg (a) slope (6 dp) |
| 12 | `half_median_shift_pp` | EXP-11 leg (a) half-median shift (4 dp) |
| 13 | `holdout_within` | `k/n` from EXP-11 leg (b) |
| 14 | `exp11_label` | `κ-TRENDING` / `κ-STABLE` |
| 15 | `exp11_forward_constraint` | as delivered (all `WINDOW-ONLY` at the aggregate) |
| 16 | `exp11_verdict` | per-system verdict word from `KAPPA_FWD_RESULTS.csv` |
| 17 | `holdout_violation_years` | years breaching the κ_pre bound (comma list; `none`) |
| 18 | `admissible_use` | `SENTENCE-ONLY` / `REPORTED-ONLY` / `NONE` |
| 19 | `admissible_sentence` | the fixed sentence, **verbatim** from the block (§7) |
| 20 | `register_label` | `DERIVED` (median of observed ratios) |
| 21 | `provenance_file` | path relative to the programme root |
| 22 | `provenance_column` | `kappa_full` etc., with the row key |
| 23 | `falsifier_status` | `TRACEABLE` iff the line reproduces from file+column; else `UNVERIFIED` |
| 24 | `out_of_window_uses` | count of that system's uses outside its window (integer) |

## 4. Use schema (`results/KAPPA_WRITE_USES.csv`) and extraction rules

Columns: `use_id, iso3, kappa_value, kappa_role, use_class, object_identity, file, column, row_key, year_applied,
year_status, window_pre2021_upper, window_full_upper, window_status, projection_flag, n_records, admissible,
label, note`.

`window_status ∈ {IN-WINDOW, OUT-OF-WINDOW-BELOW, OUT-OF-WINDOW-ABOVE, NOT-APPLIED, EMPTY-WINDOW}`.
`admissible ∈ {YES, NO-BARRED, NO-OUT-OF-OBJECT, NO-NOT-COMPARABLE, NO-NON-ENTRANT}`.

### 4.1 Structured files — declared κ-value column whitelist

A column is a κ-value column **iff** its name is in this closed list (case-sensitive):

```
kappa, kappa_full, kappa_pre, kappa_half1, kappa_half2,
kappa_full_declared, kappa_pre_declared,
loo_kappa, kappa_median_ratio, kappa_verdict, kappa_sensitivity, kappa_bound
```

No other column is read as a κ value. In particular `A01_kappa_bound_share`, `A01_kappa_lower_lag_pp`,
`bound_completion_units_pp`, `bound_pct_kappa_0.949` and `upper_linked_*` are **pp or share objects derived
from κ**, not κ; they are audited through their parent κ-conditioned object (§4.4), never read as κ values.
A value `-1` in `kappa_bound` is the delivered **sentinel** for a not-scorable cell: status `NOT-APPLIED`.

### 4.2 Text files — four declared patterns, on lines containing a κ token

A text line is read only if it contains `κ`, `κ̂`, or `kappa` (case-insensitive). On such a line:

* **P1 — κ-adjacent.** A κ token (`κ`, `κ̂`, or `kappa…`) followed by an optional `=`, `≈`, `:`, `~` and a
  decimal literal → that literal **is** a κ value (e.g. `κ = 0.949`, `κ ≈ 0.95`, `kappa_full=0.949135`). Bold
  markers (`**0.949**`) are stripped before matching. P1 needs no further test: the literal is κ-adjacent by
  construction, so a P1 literal that matches no register value is a **finding** (an unattributable use), not a
  parsing accident.
* **P2 — ISO3 then value.** An ISO3 followed by an optional `=` and a decimal literal with at least two
  decimals. Accepted **only if** the literal lies within `max(0.005, 1 % of the register value)` of some
  system's `kappa_full` or `kappa_pre`.
  A P2 hit that fails that test is **not** a κ value: it is another quantity that happens to sit next to an
  ISO3 on a κ line (a pp LOO error such as `KOR 0.48`, a pair count, a share), and it is discarded.
* **P3 — value then ISO3.** The mirror of P2, with the same acceptance test.
* **P4 — elasticity exclusion.** A line matching `C^κ` or `κ∈[0.5` is the model's congestion elasticity
  (D9), a **different object**. It is registered once as `OUT-OF-OBJECT`, excluded from the window
  denominator, and counted.

**Attribution (P1 only).** Three steps, in order. (i) The ISO3 whose occurrence is **nearest by character
distance**, within 100 characters of the literal, **if that system's register values match** the literal under
(c-i). (ii) Failing that, the **unique** system whose values match. (iii) Failing that, **unattributed** —
out-of-window. Proximity, not "first ISO3 on the line", is the rule (a row about PHL that mentions HKG in
passing must not attribute PHL's coefficient to HKG); the value-match override is the second rule (the sentence
"a single κ = 0.949 overstates KHM by 0.354" quotes **PHL's** value next to KHM in order to warn against the
substitution — it is a PHL use, not a KHM use).

**Dedupe.** One use per `(file, line, system, value)`; a value quoted twice in one clause is one use.

### 4.3 Year attribution

* **Structured per-record files:** `year_applied` = the record's `upper_year` (the year the ratio is formed),
  not `lower_year_used`. For the κ-link file, `year` as delivered.
* **κ-conditioned files:** the file's year span (§4.4).
* **Text: the register does not read application years out of prose.** A prose year is an unreliable signal —
  every Council row carries its own date, and a κ citation routinely sits beside a year that belongs to a
  different object (a pair year, a decision date, a panel span). Text uses are therefore
  `year_status = UNSTATED` and are in-window iff D7(a), (c), (d) hold. **Prose projections are detected by
  language, not by incidental years:** a line matching `κ-implied … for <year>` (within 80 characters) is
  registered as a **`TEXT-PROJECTION`** row carrying that year, is `OUT-OF-WINDOW-ABOVE` and is barred
  (B4/B6). **Declared limit:** the scan catches **year-bearing** `κ-implied` prose only. Future-tense phrasing
  with no year (`κ predicts …`) is **not** machine-detected; it is covered by the banned-sentence register (B4)
  instead, and `FINDINGS.md` records that the register's projection count is a floor, not a ceiling. The scan
  is reported whether or not it finds anything.
* **Summary columns** (`kappa_full`, `kappa_pre`, `kappa_half*`, `kappa_*_declared`, `kappa_median_ratio`)
  are `year_status = SUMMARY`: they summarise the window and are `IN-WINDOW` by construction.

### 4.4 κ-conditioned objects (`use_class = FORWARD-APPLIED`)

A file that **applies** a κ value to an object without carrying a κ literal (its columns are `κ × object`) is
registered at **file-span granularity**: one row per file, with `year_applied` = `min..max` of its year column,
`n_records` = its row count, `kappa_value` = the κ declared by the upstream object (0.949 PHL full / 0.960 PHL
pre), and `window_status` = `OUT-OF-WINDOW-BELOW` if the span starts before the window and `OUT-OF-WINDOW-ABOVE`
if it ends after it (worst case reported when both; the two are counted separately in the summary). This is a
**declared aggregation**: the alternative — one row per cell — would produce ~9,500 rows of the same fact and
would obscure, not expose, the count. The row carries `n_records` so the aggregation is auditable.

### 4.5 Duplicates

`results/determinism_run2/` copies of an input are **not** enumerated separately: they are byte-identical by
construction, and double-counting them would inflate the denominator. The rule is declared here and applied by
hash: a file whose sha256 equals a file already enumerated is `DUPLICATE` and is skipped, with the pointer
recorded in the console. Identical files in *this* cell's own `determinism_run2/` are the determinism evidence,
not uses.

---

## 5. Declared enumeration universe (closed) and its limit

**<<N_UNIVERSE>> files are adjudicated**, each with its sha256 frozen here. The runner verifies every hash before it writes
a verdict; a mismatch is a hard stop.

| file (programme root) | sha256 |
|---|---|
<<INPUT_TABLE>>

`SYNTHESIS_025.md` sha256 (the verbatim source): `<<SYNTH_SHA>>`.

**The scope limit, stated as a number.** A repository-wide scan finds **193** text files containing a `κ` or
`kappa` token. **<<N_UNIVERSE>>** are adjudicated here. The remaining **<<N_REMAINDER>>** are prior-cycle predeclarations,
experiment findings, logs and model cards; they are **not** adjudicated by this register, and **no write-up
sentence may cite a κ value from a file outside this universe** — an unadjudicated citation has no register
line, and D158 rule 3 (`register before sentence`) makes it `UNVERIFIED`. This is a declared boundary, not a
claim of exhaustiveness: the register certifies the 16, and says so wherever it is cited.

This universe contains **all four delivered κ objects** (EXP-6 PIPE-LOO, EXP-11 KAPPA-FWD, EXP-7 REPRO-PATH's
κ-link, and the v1.5/v1.6 in-model κ caps) plus the three governance texts that cite κ numerically
(`DECISIONS.md`, `SYNTHESIS_025.md`, `STATUS.md`). If a κ object exists outside it, the register does not know
about it; that is the honest form of the guarantee.

---

## 6. Threshold (frozen)

1. **The bar is 100 %.** Every enumerated κ use must be `IN-WINDOW`. There is **no tolerance band**, no
   "mostly in-window" reading, and no post-hoc slack: a single out-of-window use fails the bar. The ±5 pp slack
   convention that EXP-11 carried is **not** imported here — it belongs to a different object (cell excess) and
   importing it would be a re-fit.
2. Every use is counted, and the counts reported: `n_uses`, `n_applied`, `n_in_window`, `n_out_below`,
   `n_out_above`, `n_not_applied`, `n_projection`, `n_not_comparable`, `n_non_entrant`, `n_out_of_object`.
3. The window is **derived, not chosen** (D4). If a derived span disagrees with the anchor spans
   (PHL 2003–2024 / KOR 2005–2023 / KHM 2000–2023 / CHN 2012–2020) the register line is `UNVERIFIED`.
4. **No re-fit, no re-estimation, no model run.** κ values are read, not recomputed from raw completion data —
   except the **reconciliation check** in §6.5, which recomputes the median of the delivered pair ratios to
   confirm the register reproduces the delivered value at 4 dp. A reconciliation is a check, not an estimate.

### 6.5 Reconciliation check (declared)

For each system, recompute `median(ratio)` over the 43 delivered pairs of `KAPPA_FWD_DETAIL.csv` and compare to
`kappa_full` at 4 dp; recompute `median(ratio)` over the pre-2021 subset and compare to `kappa_pre` at 4 dp.
`MATCH` is required; a mismatch marks the register line `UNVERIFIED`. This reproduces the delivered medians
from the delivered pairs. It does **not** re-derive pairs from the completion series (that is EXP-11's and
EXP-6's act, and re-doing it here would be re-scoring a delivered cell).

---

## 7. The four fixed sentences, and the KOR counter-example (mandatory in the write-up)

Copied **verbatim** from the block (§6.4 item 5(ii)); they are carried in the register's `admissible_sentence`
column and in `FINDINGS.md`:

| system | fixed sentence (verbatim) |
|---|---|
| PHL | *"within-window; slope flat but half-shift 2.1348 pp > 2.0, so not stationary in level"* |
| KOR | *"slope flat and shift 0.6354 pp, yet 0/3 hold-out cells — κ-STABLE is never written forward-usable"* |
| KHM | *"trending, shift 7.4361 pp"* |
| CHN | *"reported only; non-stationary; not a forward constraint"* |

**The KOR counter-example sentence, which this register must carry** (D142/D143/D153(ii)):

> **KOR is the counter-example that bars "κ-STABLE is forward-usable": slope +0.002875/yr and half-shift
> 0.6354 pp both clear their bars, yet 0/3 hold-out cells (excess +0.6824, +0.6506, +0.5917 pp).**

A register that reports KOR as `κ-STABLE` without this sentence is **defective**; the runner checks that the
sentence is present in `PRE_DECLARATIONS.md` and in `FINDINGS.md` and marks the verdict `UNVERIFIED` if either
is missing. The sentence may not be shortened to "KOR is stable".

**One sentence per system, and no sentence without its register line** (D158 rule 3). The write-up may carry
the four sentences above; it may **not** generalise them into a cross-system sentence, a trend sentence, or a
forward sentence.

---

## 8. No-projection rule (frozen)

1. No κ value may be used **beyond its window**, and none may be **extrapolated**: no `κ-implied` value for a
   future year, no κ trend line carried past 2024 (PHL) / 2023 (KOR, KHM) / 2020 (CHN), no κ bound applied to a
   year with no observed pair.
2. No κ value may be applied to a **model-generated** series and then cited as evidence about the observed
   world (D8).
3. `κ-STABLE` may **never** be written as `forward-usable`, `predictive`, `validated`, or `a constraint` (KOR is
   the counter-example; D142 condition).
4. `CHN` may **never** appear as a forward constraint, in any sentence, in any form (D133).
5. A projection found on disk is **named, counted, and barred**; it is **never** re-scored, re-run or repaired
   (the block's item 2: "a record correction, never a re-score").

---

## 9. Verdicts, definitions, and precedence (frozen)

**Precedence, declared in the block, not chosen by the runner** (D158 rule 6):

```
REGISTER-CONSISTENT  >  REGISTER-NARROWED  >  REGISTER-UNUSABLE
```

The labels are tested **in that order**; the first that holds is written. The order is fixed here so that a
runner cannot pick a friendlier label after seeing counts.

**`REGISTER-CONSISTENT`** iff all of:
 (a) `n_in_window == n_applied` and `n_out_below == n_out_above == 0` (**100 %**);
 (b) `n_projection == 0`;
 (c) `n_not_comparable == 0`;
 (d) every register line is `TRACEABLE` and the reconciliation check is `MATCH`;
 (e) the KOR counter-example sentence is carried (§7) and all four fixed sentences are present.
→ the write-up may carry the four fixed sentences and the register ships as the citation for "what κ may be
used for"; the block's label is `REGISTER-CLEAN`.

**`REGISTER-NARROWED`** iff **not** CONSISTENT, **and** all of:
 (a) every register line is `TRACEABLE` and the reconciliation is `MATCH`;
 (b) the KOR counter-example sentence is carried and all four fixed sentences are present;
 (c) **every** out-of-window, projection or `NOT-COMPARABLE` use is confined to a **named object** that is
     either (i) a **closed** artifact — v1.5, v1.6, v1.7, or the EXP-7/v1.2 κ-link whose label is final under
     D143(iv)/D150/D153 — or (ii) a **declared diagnostic / non-verdict-bearing** object;
 (d) **no live verdict** (a delivered verdict not in the closed list of (c)) rests on any out-of-window,
     projection or `NOT-COMPARABLE` use;
 (e) at least the four systems' register values remain in-window `DESCRIPTIVE` uses, so that a window-only
     sentence per system is still groundable.
→ the register is **usable as a write-up instrument only in its narrowed form**: the four fixed sentences may
be carried; every named object is barred from citation; the barred-object list travels with the register. The
block's label is `USE-OUTSIDE-WINDOW`, reported with the object names.

**`REGISTER-UNUSABLE`** otherwise — in particular if any register line is `UNVERIFIED`, or an out-of-window use
is load-bearing for a live verdict, or the KOR counter-example cannot be carried, or no observed-pair
descriptive use remains in-window. Then the register may not be cited at all and κ may not appear in the
write-up.

**Falsifier (from the block, item 5).** Any register line not traceable to a delivered file + column →
`UNVERIFIED`, and the register may not be cited. The runner writes `falsifier_tripped = TRUE` if any register
line fails its provenance re-read, and the verdict is then `REGISTER-UNUSABLE` regardless of the counts.

---

## 10. The seven authoring rules (D158), binding on this predeclaration

1. **Hash enforcement at verdict time.** A hash cited in a verdict row is enforced by the runner when the
   verdict is written; a recorded-but-unenforced hash is cited only as `RECORDED-NOT-ENFORCED` and carries no
   verdict.
2. **Object identity before comparison.** No two series are compared, subtracted or placed against one another
   unless both carry the same declared denominator/convention; otherwise the result is `NOT-COMPARABLE`, not a
   number.
3. **Register before sentence.** No write-up sentence may use a number whose register line (convention, window,
   label, source) does not exist; a sentence without a register line is `UNVERIFIED` and may not ship.
4. **Level-symmetric legs.** A leg intended to test a two-level object requires both levels.
5. **Class tags.** Every model number carries its class (v1.5 / v1.6 / v1.7) and every localisation sentence
   names the class.
6. **Banned sentences register.** The barred phrasings are enumerated (§11) and a predeclaration using one is
   returned.
7. **Label discipline for REQUIRED-STATE/DERIVED.** Any λ*, required coverage or derived target carries
   "REQUIRED-STATE (EXP-17); not adopted" / "DERIVED" in the same sentence as the number.

This cell introduces **no** REQUIRED-STATE object and **no** DERIVED target; λ* and 0.8076 do not appear in any
register row, and rule 7 is satisfied vacuously and is recorded as such.

---

## 11. Banned sentences (this cell's register, plus D158(6))

The following may not appear in this cell's outputs, nor in any write-up sentence citing this register:

| # | banned | why |
|---:|---|---|
| B1 | "κ ≈ 0.95 for the Philippines" | the block's own named failure (§1, line 436): drops system, window, and label |
| B2 | "κ is stable across systems" | false as a cross-system sentence: 0.5950–0.9898 |
| B3 | "κ-STABLE is forward-usable" | **barred by the KOR counter-example** (0/3 hold-out) |
| B4 | "κ predicts / forecasts / constrains upper completion" | projection; D138 |
| B5 | "the κ-link validates the model path" | κ-link is a diagnostic on a closed artifact; projection (D6) |
| B6 | "κ-implied upper completion for 2027 = 87.710" | projection beyond the window; the sentence is named and barred (§12) |
| B7 | "κ is a parameter" / "κ enters the generator" | D138: within-window description only |
| B8 | "CHN is a forward constraint" | D133 |
| B9 | "κ explains / causes / drives the upper-secondary level" | no causal or direction claim |
| B10 | "the register is clean" / "all κ uses are in-window" when §9 yields `REGISTER-NARROWED` | mislabel |
| B11 | "A17 0/33 vs A00 9/33" without its sentence | D158(6) |
| B12 | "demand falsified"; "the participation margin is duplicated" (as a cell sentence); "the upper-secondary ceiling is structural"; "survival loses 50.7%"; "fix survival only"; "behaviourally N pp wrong" before EXP-21 | D158(6) |

---

## 12. What this cell will do if it finds an out-of-window use (declared in advance)

1. **Name** the object: file, column, year span, count (`KAPPA_WRITE_USES.csv` rows).
2. **Flag** it: `admissible = NO-BARRED`, `projection_flag = TRUE` where D6 applies.
3. **Bar the sentence**: add the object to the barred list in `FINDINGS.md` and this register, in the same
   words used here.
4. **Never** re-score, re-run, repair or re-fit it. A record correction names the object; it does not fix it.
5. If the object is **load-bearing for a live verdict**, the verdict is `REGISTER-UNUSABLE` — not "narrowed".

The worker declares in advance that **the most likely finding is a narrowing**, because the programme has
already ruled κ window-only **after** building four κ objects that apply it forward (the v1.5/v1.6 in-model
caps and the EXP-7 link). A register that found nothing would be a register that did not look. This
expectation is **not** a threshold: the verdict is computed from the counts, and the counts are whatever the
files say.

---

## 13. Determinism and file contract

* Runner: `code/run_kappa_write.py`; deterministic, **no RNG**, no clock in any output cell, no network, no
  model execution, no fit.
* Writes: `results/KAPPA_WRITE_REGISTER.csv`, `results/KAPPA_WRITE_USES.csv`,
  `results/KAPPA_WRITE_SUMMARY.csv`, `results/console.txt`; `--outdir results/determinism_run2` for the second
  run. Two runs must be **byte-identical**; the runner refuses to declare determinism if the diff is non-empty.
* `RUN_MANIFEST.json` and `SHA256SUMS.txt` are written by `code/make_manifest.py` after both runs.
* Ordering: rows are sorted by explicit keys (system order `PHL,KOR,KHM,CHN,HKG,JPN`; uses by
  `(file, row_key, kappa_role)`), never by dict iteration or filesystem order.
* Environment: `"/Users/treymenefee/Library/Application Support/dsh-massification/venv/bin/python"`; standard
  library only.

## 14. Disclosures (recorded before the run, not after)

1. **Not count-blind.** The worker read the source files before freezing, because the block **requires**
   re-derivation from disk (§6.4 item 4) and the register's object is a set of delivered numbers. No threshold
   was set by reference to any observed count: the 100 % bar and the precedence come from the block and D156.
   This disclosure is recorded so that no claim of a blind read is made (cf. D142 on EXP-14).
2. **The universe is <<N_UNIVERSE>> files, not the 193 that contain a κ token** (§5). The register says this wherever it is
   cited, and bars citations from outside the 16.
3. **The κ-conditioned objects are aggregated at file-span granularity** (§4.4), with `n_records` carried.
4. **κ is two symbols in this programme** (D9); the elasticity κ is excluded and counted, not silently merged.
5. **This register cannot make κ citable as a constraint.** At best it makes four window-only sentences
   citable. It adds no evidence, no estimate and no number that was not already on disk.
6. **No HKG/JPN content**: both are `NON-ENTRANT`; the register records the empty window and nothing else. The
   HKG leg of the block (item 5(iii), the two-part re-entry test) is **not** executed here — it belongs to the
   HELD ledger, and this cell's scope is the κ register only. It is not fabricated, not proxied, and not
   summarised as if it had been done.

---

## 15. Sign-off

Frozen before the first register row was written. `code/run_kappa_write.py` embeds the sha256 of this file and
stops if it does not match. Numbers are `OBSERVED` (the delivered series/ratio inputs) or `DERIVED` (medians,
spans, counts, verdicts); no other label is used. No adoption. No re-fit. No model run.
"""


if __name__ == "__main__":
    main()
