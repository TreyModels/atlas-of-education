# ERRATUM — Paper F fertility record (25 November 2026)

**Record:** `research/records/2026-11-25-paper-fertility/`.
**Branch:** `research/paper-fertility-2026-11-25` @ `ec899cc` (the verified head audited by task-11). This
erratum is an additive commit on that branch; no history rewrite.
**Raised by:** task-11 prose-vs-data audit (`research/prose-data-audit-2026-11-24` @ `ff390fe`,
`research/records/2026-11-24-prose-data-audit/AUDIT.md`, check PF-02); actioned as task-12.
**What was changed (task-12):** a marked `CORRECTION` pointer in the draft, this file, and a reproduction script +
output; the draft's number was left visible in that commit. **Update (task-14):** the correction has now been
**applied** to the draft and its sources — see §B. The original −0.228 is preserved in §A as the audit trail.

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
**Applied in task-14 (commit `e21b6c4`) — see §B.**

### Reproduction

```
git show 161b563:research/records/2026-11-23-corr-rebuild/data/results_part1.json > /tmp/results_part1.json
python3 scripts/erratum_check_pf_total_attainment.py /tmp/results_part1.json
# -> data/erratum_check_pf_total_attainment.json
```

The script reads the committed JSON, prints `b / se / n / nc` and the 3-dp and 4-dp roundings, and lists the six
occurrences of −0.228 as they stood when the erratum was raised. It is retained as the pre-correction audit trail;
the draft is now corrected (§B).

### Effect on the papers

Only Paper F's own draft/record carries the value; no other paper record quotes the total-attainment level
coefficient (the −0.228 does not appear in Paper M, Paper N1, the methods paper or the E1/Q2/E6/E8 records). The
paper's substantive conclusion is unchanged — this is a rounding slip of 0.0005 at the reporting precision.

---

## §B — correction applied (task-14, commit `e21b6c4`)

**Status: APPLIED.** The draft and its assembled source files now print **−0.227** (never −0.228). The committed
coefficient remains **−0.22745836147084678**; the SE (**0.042**), n (**1,394**) and country count (**144**) are
unchanged.

### Source replacements (4 occurrences)

| file | replacement |
|---|---|
| `draft/frame_intro_new.md` §1.2 | "Total attainment: −0.228 (0.042)" → **−0.227** |
| `sections/section1_levels_changes.md` Table 1 row | `**−0.228** (0.042)` → **−0.227** |
| `sections/section1_levels_changes.md` income-rival paragraph | "total attainment at −0.228 (0.042)" → **−0.227** |
| `data/claims_sources.csv` row A1 | "-0.228 (0.042) n=1394/144" → **-0.227 (0.042) n=1394/144** |

### Assembly

The draft is generated, so the assembly script was rerun:

```
python3 build_paper.py
# wrote draft/paperF_draft.md: 19,831 words total (17,796 before references); 64 references
```

The regenerated `draft/paperF_draft.md` contains **3 occurrences of −0.227** (the §1.2 sentence, Table 1 and the
income-rival paragraph) and **0 occurrences of −0.228**. The task-12 `CORRECTION` pointer (which was added to the
generated draft only, not to its sources) was removed by the rebuild, as intended; the audit trail is this file
plus `scripts/erratum_check_pf_total_attainment.py` / `data/erratum_check_pf_total_attainment.json`, which retain
the original claim and the committed value. A grep for `−0.228` / `-0.228` over `draft/`, `sections/`, `data/`
and `README.md` leaves only those historical erratum artefacts (the ERRATUM quote and the erratum-check JSON), never
the paper's own text.

### Effect on other papers

A grep of Paper M (`research/paper-massification-2026-11-25` @ `fb9f419`) and Paper N1
(`research/paper-sequencing-novel-2026-11-25` @ `62c27a3`) for `0.228` found **no references** to this coefficient
in either draft; nothing was edited outside the Paper F record.
