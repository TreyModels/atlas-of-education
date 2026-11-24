# ERRATUM — Paper F fertility record (25 November 2026)

**Record:** `research/records/2026-11-25-paper-fertility/`.
**Branch:** `research/paper-fertility-2026-11-25` @ `ec899cc` (the verified head audited by task-11). This
erratum is an additive commit on that branch; no history rewrite.
**Raised by:** task-11 prose-vs-data audit (`research/prose-data-audit-2026-11-24` @ `ff390fe`,
`research/records/2026-11-24-prose-data-audit/AUDIT.md`, check PF-02); actioned as task-12.
**What is changed:** one marked `CORRECTION` pointer in the draft, this file, and a reproduction script + output.
The draft's number is left visible, not silently changed.

---

## §A — total-attainment level coefficient is −0.227458, not −0.228

### Where

`draft/paperF_draft.md` §1.2 (and the same sentence in `draft/frame_intro_new.md`):

> **In levels, the gradient is large, precise, and robust.** Women's mean years of schooling: −0.129 births per
> woman per year of schooling (SE 0.029), on 5,915 country-years and 192 countries. **Total attainment: −0.228
> (0.042).** Secondary enrolment: −0.0213 (0.0037). …

The same value appears in three more places in the record:

| file | location | text |
|---|---|---|
| `draft/paperF_draft.md` | line 468 (Table 1) | `mean years of schooling, total \| **−0.228** (0.042) \| **+0.190** (0.055) \| 1,394 / 144` |
| `draft/paperF_draft.md` | line 495 (income-rival paragraph) | "total attainment at −0.228 (0.042) with income −0.142 (0.087, not significant)" |
| `draft/frame_intro_new.md` | line 67 | the same §1.2 sentence |
| `sections/section1_levels_changes.md` | lines 79 and 106 | the same table row and income-rival sentence |
| `data/claims_sources.csv` | row A1 "levels coefficient total attainment" | "−0.228 (0.042) n=1394/144" |

### What reproduces

Committed source: `research/corr-rebuild-2026-11-23` @ `161b563`,
`research/records/2026-11-23-corr-rebuild/data/results_part1.json`, field `lags.mys_total["0"]`:

| field | committed value |
|---|---|
| `b` | **−0.22745836147084678** |
| `se` | 0.042166886912195396 |
| `n` | 1,394 |
| `nc` | 144 |

At the prose's stated precision (three decimals) the coefficient rounds to **−0.227** (−0.227458 → −0.227; it
also truncates to −0.227). The paper's −0.228 is a 0.0005 boundary slip. The SE (0.042), n (1,394) and country
count (144) all reproduce exactly.

**Recommended correction:** −0.228 → **−0.227** (or −0.2275 at four decimals) in all six locations listed above;
the table cell and the claims-source row should be changed with the draft, not before it.

### Reproduction

```
git show 161b563:research/records/2026-11-23-corr-rebuild/data/results_part1.json > /tmp/results_part1.json
python3 scripts/erratum_check_pf_total_attainment.py /tmp/results_part1.json
# -> data/erratum_check_pf_total_attainment.json
```

The script reads the committed JSON, prints `b / se / n / nc` and the 3-dp and 4-dp roundings, and lists the six
occurrences of −0.228 in the record without changing them.

### Effect on the papers

Only Paper F's own draft/record carries the value; no other paper record quotes the total-attainment level
coefficient (the −0.228 does not appear in Paper M, Paper N1, the methods paper or the E1/Q2/E6/E8 records). The
paper's substantive conclusion is unchanged — this is a rounding slip of 0.0005 at the reporting precision.
