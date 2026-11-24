# ERRATUM — Codex source verification record (25 November 2026)

**Record:** `research/records/2026-11-25-codex-source-verification/`.
**Branch:** `research/codex-source-verification-2026-11-25` @ `9a0fd69` (the verified head audited by task-11).
This erratum is an additive commit on that branch; **no history rewrite, and the `9a0fd69` commit message itself
is left untouched** (it cannot be edited without rewriting the branch).
**Raised by:** task-11 prose-vs-data audit (`research/prose-data-audit-2026-11-24` @ `ff390fe`,
`research/records/2026-11-24-prose-data-audit/AUDIT.md`, check SV-04); actioned as task-12.
**What is changed:** a marked `METADATA ERRATUM` pointer in `README.md`, this file, and a reproduction script +
output. **No table value, fee date or status mark is changed.**

---

## §A — metadata erratum: "24 DOI-verified" should be 21 V / 2 U / 1 W

### Where

The commit message of the verified head `9a0fd69`:

> Codex source verification: demand-series availability (GGDC/PWT/WDI, no pre-1990 wage series), prior art
> Q1-Q3 (24 DOI-verified), unverified-list marks

The same description is quoted in the E6/E8 record's `ERRATUM.md` §B (in the Issue-B provenance note identifying
`9a0fd69` as the verified head). It may also be quoted in downstream handoff/dashboard text, which the Lead is
routing separately.

### What reproduces

`README.md` Job 3 contains three prior-art tables (Q1/Q2/Q3, 8 works each). Recounting the `Status` column of the
committed tables (scripts below):

| table | V (DOI verified) | W (working paper) | U (no DOI / book) | works |
|---|---|---|---|---|
| Q1 — schooling/structural transformation | 8 | 0 | 0 | 8 |
| Q2 — path comparison | 5 | 1 | 2 | 8 |
| Q3 — multiverse calibration | 8 | 0 | 0 | 8 |
| **total** | **21** | **1** | **2** | **24** |

So **24 prior-art works were checked, but 21 DOIs were verified**; 2 works have no DOI (the Mahoney &
Rueschemeyer and Gerring books) and 1 is a working-paper version whose published *Econometrica* DOI was not
verified (Romano & Wolf). "24 DOI-verified" conflates works checked with DOIs verified.

**Correct description:** "24 prior-art works checked; **21 DOIs verified (V)**, **2 works without DOI (U)**,
**1 working-paper version whose published DOI was not verified (W)**."

### Note on the audit's own summary line

The task-11 audit's check SV-03 note prints "table statuses V=22, W=1, U=2" (which sums to 25, one more than the
24 works in the tables); its SV-04 note and the commit-message check give "21 V, 2 U, 1 W". The committed
tables recount to **21 / 2 / 1** (script below); the SV-03 line appears to be a miscount in the audit record and
is flagged here for that record's owner. The E6/E8 erratum's quotation of the commit message is corrected by
cross-reference in E6/E8 `ERRATUM.md` §D.

### Why the commit message is not edited

Project rule: never rewrite, force-push or amend an existing branch. The metadata correction therefore lives in
this file + the `README.md` pointer, not in the commit message. The verified head remains `9a0fd69`.

### Reproduction

```
python3 scripts/erratum_check_prior_art_statuses.py
# -> results/erratum_check_prior_art.json
```

Parses the three Job-3 tables in `README.md` and recounts the status column. `git show -s --format=%B 9a0fd69`
shows the commit message being corrected.

### Effect on the papers/data

None. No fee date, DOI, prior-art status, table value or result changes; the papers cite `9a0fd69` as the
verified head (correct) and do not repeat the "24 DOI-verified" description. This is a metadata-description
correction only.
