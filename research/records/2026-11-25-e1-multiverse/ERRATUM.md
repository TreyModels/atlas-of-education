# ERRATUM — E1 multiverse R=1200 record (25 November 2026)

**Record:** `research/records/2026-11-25-e1-multiverse/`.
**Branch:** `research/e1-multiverse-1200-2026-11-25` @ `7e6f7b5` (the verified head audited by task-11). This
erratum is an additive commit on that branch; no history rewrite.
**Raised by:** task-11 prose-vs-data audit (`research/prose-data-audit-2026-11-24` @ `ff390fe`,
`research/records/2026-11-24-prose-data-audit/AUDIT.md`, checks E1-07 and E1-12); actioned as task-12.
**What is changed:** two marked `CORRECTION` pointers in `REPORT.md`, this file, and a reproduction script +
output. **No table or result file is changed**; the original sentences stay visible.

---

## §A — the 136-parity sentence contradicts the record's own table and JSON

### Where

`REPORT.md`, §"Headline answers", paragraph (a). Original sentence (retained; a `CORRECTION` pointer follows the
paragraph):

> Under the committed 136-parity convention the same pattern appears (BY het = 39 at 1,200; up/down/flip 0/0/0).

### What reproduces

`results/summary_by_R.json` → `families.1200.<proc>.certified_BY136` (the record's committed 136-parity counts;
the same values are in the R=1200 rows of the REPORT's own table):

| procedure | `certified_BY136` at R=1200 | prose claim |
|---|---|---|
| up | **25** | 0 |
| down | **15** | 0 |
| sign-flip | **0** | 0 |
| heterogeneity | **39** | 39 |

**Only the sign-flip zero is right.** Under the 136-parity convention the up and down families also certify (25 and
15 links respectively), so the sentence's substantive point — that it is *only* heterogeneity that changes under BY
at 1,200 — is wrong for the 136-parity convention. (The record's conservative-family statement elsewhere — "BY is
zero at every R for up/down/flip; only heterogeneity certifies" and the table column `BY cert` — is correct and
unaffected: that column is the conservative `(1+c)/(1+R)` p-value convention, where up/down/flip are 0.)

**Recommended corrected sentence:** "Under the committed 136-parity convention heterogeneity still certifies **39**
links at 1,200, but the up and down families also certify (**25** and **15** respectively; sign-flip 0)."

### Downstream restatements (not edited here)

The task-11 audit notes that the methods paper / README restatements quote the conservative-family "0/0/0" for the
136-parity convention. Those are different records and are being routed separately (Lead will direct the paper/
synthesis corrections); this erratum corrects only the E1 record.

### Reproduction

```
python3 scripts/erratum_check_e1_prose.py
# -> results/erratum_check_prose.json
```

Reads `results/summary_by_R.json` and prints `certified_BY136` for all four procedures against the prose claim.

---

## §B — runtime minimum worker wall is 31.045 s, not 31.1 s

### Where

`REPORT.md`, "Determinism and integrity", runtime bullet. Original text (retained; a `CORRECTION` pointer follows
the bullet):

> per-draw worker wall mean 37.8 s, median 36.4 s, max 136.2 s (the real pass), min 31.1 s (`results/progress.log`,
> `results/run_meta.txt`).

### What reproduces

`results/progress.log` column 2 (worker wall seconds; 1,201 rows, one per draw plus the real pass):

| statistic | recomputed | prose |
|---|---|---|
| mean | 37.759 s | 37.8 s ✓ |
| median | 36.406 s | 36.4 s ✓ |
| max | 136.204 s | 136.2 s ✓ |
| **min** | **31.045 s** | **31.1 s ✗** |

31.045 s rounds (and truncates) to **31.0** at one decimal, not 31.1. This is a 0.05 s rounding-level mismatch at
the stated precision; mean/median/max reproduce.

**Recommended correction:** "min **31.0 s**".

### Reproduction

Same command as §A; the output's `issue_B_runtime.recomputed` block carries the four statistics and the rounded
minimum.

---

## Effect on the papers

Neither Paper M (`research/paper-massification-2026-11-25` @ `fb9f419`) nor Paper N1
(`research/paper-sequencing-novel-2026-11-25` @ `62c27a3`) quotes the E1 136-parity up/down/flip counts or the
31.1 s runtime; no paper in this revision depends on either correction. The methods-paper restatement of the
136-parity zero is flagged above for separate routing.
