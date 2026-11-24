# ERRATUM — E6/E8 sequencing record (25 November 2026)

**Record:** `research/records/2026-11-25-e6e8-sequencing/`.
**Branch:** `research/e6e8-sequencing-2026-11-25` (base/verified head at the time of the erratum: `2d19da7`; this
erratum is an additive commit on that branch — no rewrite, no force-push).
**Raised by:** paper-reviser, task-3 (revision of Paper M / Paper N1), **confirmed as task-7**. Two record
corrections: a prose-vs-data mismatch in E6 (Issue A) and a fee-date provenance ambiguity in E8 (Issue B).
**What is changed:** two marked pointer lines in `REPORT.md`, one provenance note in the `scripts/e8_fee_event_study.py`
docstring, a new reproduction script + output, and this file. **No number in the record is changed** and the
original sentences stay visible.

---

## Issue A — the E6 line "18–33% strict schooling-first" does not reproduce

### Where

`REPORT.md`, §1 E6, the "Reading." paragraph (the original line is retained; a `CORRECTION` pointer now follows
the paragraph). Original sentence:

> **Reading.** On pre-1990 series, demand take-off precedes schooling take-off in **10–24% of identifiable
> countries** (point estimates by proxy), below the pre-registered one-third threshold; **schooling-first is the
> majority strict ordering** (18–33% strict schooling-first, with the remainder weak ties or undetermined).

### What reproduces, and from what

Source file: `results/e6_summary.json` (the committed E6 output; the rows used are the four full-overlap
1900–2012 proxies). Definitions are the record's own: `forward` = demand take-off first (strict); `reverse` =
schooling take-off first (strict) — this is the "schooling-first" category; `forward_or_tie` = weak forward
ordering; `undetermined` = no ordering inside the window; `n_in_window` = countries with both series in the
window; `n_all` = all countries with both series.

| proxy | forward | reverse | forward_or_tie | undetermined | identifiable (= f+r+tie) | school-first / identifiable | school-first / in-window | school-first / all | school-first / strict orderings |
|---|---|---|---|---|---|---|---|---|---|
| GGDC non-agricultural employment | 2 | 5 | 13 | 10 | 20 | **25.00%** | 16.67% | 13.51% | 71.43% |
| WDI urbanisation | 10 | 14 | 41 | 36 | 65 | **21.54%** | 13.86% | 9.79% | 58.33% |
| WDI industry value added | 13 | 25 | 16 | 22 | 54 | **46.30%** | 32.89% | 17.48% | 65.79% |
| WDI agricultural value added (falling) | 9 | 21 | 18 | 35 | 48 | **43.75%** | 25.30% | 14.69% | 70.00% |

Ranges over the four proxies:

| denominator | range |
|---|---|
| identifiable countries (`forward + reverse + forward_or_tie`) | **21.54–46.30%** → the paper-facing **21.5–46.3%** |
| in-window countries (`n_in_window`) | 13.86–32.89% |
| all countries with both series (`n_all`) | 9.79–17.48% |
| strict orderings only (`forward + reverse`, weak ties excluded) | 58.33–71.43% |

**No denominator produces a range with endpoints 18 and 33.** The clause does not reproduce. The neighbouring
claims in the same paragraph do reproduce: demand-first 10.0–24.1% of identifiable countries (10.0 / 15.4 /
24.1 / 18.8 by proxy, all below the one-third threshold) and the weak-forward share 21.05–43.33% of in-window
countries (21–43%).

### The "majority" wording

With the correct numbers, schooling-first **exceeds demand-first in all four proxies** (21.5–46.3% versus
10.0–24.1% of identifiable countries), but it is **not a majority of identifiable countries** (maximum 46.3%).
It is a majority only among *strict orderings* (58.3–71.4%). The correct wording is therefore "the larger strict
ordering", not "the majority strict ordering" — a second, wording-level correction in the same sentence.

**Recommended corrected wording** (used by Paper M, `research/paper-massification-2026-11-25` @ `fb9f419`):
"schooling-first is the larger strict ordering in all four proxies — 21.5–46.3% of identifiable countries against
10.0–24.1% demand-first, and 58.3–71.4% of strict orderings — with the remainder weak ties or undetermined."

### Reproduction

- `scripts/erratum_check_e6_prose.py` in this record reads `results/e6_summary.json` and writes
  `results/erratum_check.json` (stdlib only; prints the table and ranges above). Run:
  `python3 scripts/erratum_check_e6_prose.py`.
- Independent cross-check: Paper M's `scripts/verify_revision_numbers.py` (branch
  `research/paper-massification-2026-11-25` @ `fb9f419`) recomputes the same 21.5–46.3% of identifiable countries
  as check `E6 strict schooling-first share (identifiable, range)`; the paper uses the recomputed range and does
  **not** quote 18–33%.

### Where else does 18–33% appear?

A scan of this record and of the whole `research/e6e8-sequencing-2026-11-25` branch worktree for `18–33`, `18-33`,
and `18` within four characters of `33` found **exactly one occurrence: `REPORT.md` line 53 (the sentence above)**.
It appears in no table, script, result file, pre-registration, or data file, and it was not propagated to Paper M
or Paper N1. There is therefore no other occurrence to cross-reference; the pointer added under the paragraph is
the only correction site.

---

## Issue B — E8 fee-date provenance: `bfb8c6f` vs `9a0fd69`

### Where

- `REPORT.md`, §2 E8, "Dates." paragraph: "…(`research/codex-source-verification-2026-11-25` @ `bfb8c6f`, file
  `fee_dates.csv`)…" (line 63–64 in the pre-erratum file).
- `scripts/e8_fee_event_study.py`, module docstring line 5: "…@ bfb8c6f): MWI 1994, …".

### Facts

| item | value |
|---|---|
| cited commit | `bfb8c6f` — "Codex source verification: fee-abolition dates (8 verified, 4 unresolved), E8 verified-only set, sources and resolution rule" |
| verified branch head | `9a0fd69` — "Codex source verification: demand-series availability (GGDC/PWT/WDI, no pre-1990 wage series), prior art Q1-Q3 (24 DOI-verified), unverified-list marks" |
| relationship | `bfb8c6f` is an ancestor of `9a0fd69` (`git merge-base --is-ancestor bfb8c6f 9a0fd69` confirms) |
| file at `bfb8c6f` | `research/records/2026-11-25-codex-source-verification/fee_dates.csv` |
| file at `9a0fd69` | same path |
| **sha256 identity** | `1a08d4652371f7a3c79a54725b79c48429a793e3d88252d170715018ddd8e2ab` at **both** commits, and the same sha256 for the copy at `data/fee_dates.csv` in this record |
| head the papers cite | `9a0fd69` (Paper M §7.6 and Paper N1 §8 both cite `9a0fd69`) |

**Reading:** citing `bfb8c6f` for the fee dates is not wrong about *which commit introduced* `fee_dates.csv`, but
it is the fee-date commit, not the verified head under which the independent audit was accepted. Because the file
is byte-identical at both commits, the fix is provenance-only: the record now states both commits, the sha256
identity check, and that the papers cite `9a0fd69`. No dates, no numbers, no data change.

A `PROVENANCE NOTE` pointer now follows the "Dates." paragraph in `REPORT.md`, and an equivalent note is in the
`scripts/e8_fee_event_study.py` docstring.

---

## Effect on the papers

- **Paper M** (`research/paper-massification-2026-11-25` @ `fb9f419`): uses the recomputed 21.5–46.3% of
  identifiable countries (its own verification script); it does not quote 18–33% and already cites `9a0fd69` for
  the fee dates. No change needed.
- **Paper N1** (`research/paper-sequencing-novel-2026-11-25` @ `62c27a3`): cites the E6 demand-first shares
  (10.0–24.1%) and bounds (6.7–53.0%), not the 18–33% clause; it cites `9a0fd69` for the fee dates. No change
  needed.
- The E6/E8/N3 numbers used downstream are unaffected: only the one prose range and the "majority" wording were
  wrong.

## Files in this erratum commit

- `ERRATUM.md` — this file (new).
- `REPORT.md` — two marked pointer lines added (original sentences left visible; no number changed).
- `scripts/e8_fee_event_study.py` — provenance note added to the docstring (no code change).
- `scripts/erratum_check_e6_prose.py` — new reproduction script for Issue A.
- `results/erratum_check.json` — new output of that script (per-proxy counts and shares under four denominators).

---

## Additional audit note (not one of Issues A/B; reported for follow-up, not corrected here)

A full prose-vs-data audit of the record was run while preparing this erratum. Everything else checked and
reproduced — the eight E6 table rows against `results/e6_summary.json` (0 mismatches); all eleven E8 event-table
rows (CS ATT/SE/CI, TWFE ATT, treated n) against `results/e8_results.json` (0 mismatches); E8 sensitivity, placebo
(−0.39), all-12-dates (20.80) and leave-one-out (18.17–26.16); N3 definition count (54, all ≥20 countries), q1
default (6.2 / 70.6 / 17.6), bounds (5.9–82.4), the 0.0–30.8% strict range and the 10.45% median.

One further prose-vs-data mismatch was found, **outside the two issues this erratum corrects**:

- `REPORT.md` §3 (N3) states "the **weak forward-or-tie share ranges 56–84%**". From `results/n3_table.csv` the
  plausible quantities are:
  - weak tie (`forward_or_tie`) as a share of identifiable countries: **56.67–88.46%**;
  - weak tie as a share of all countries (`n`): **50.00–82.14%**;
  - `forward_share_incl_ties` (weak-forward plus weak tie): **56.70–100.00%**.

  None gives 56–84%, and no subset (q1-only, non-survival) reproduces the endpoints. This looks like a stale or
  hand-rounded range. It is **not** corrected in this commit because task-7 scoped the record correction to Issues
  A and B; it is flagged here so the record owner can issue the follow-up correction (the recommended replacement
  would be the reproducible "weak tie share of identifiable countries ranges 56.7–88.5%", or the
  `forward_share_incl_ties` range, with the denominator stated explicitly). Downstream papers: Paper M quotes the
  E6 demand-first range and N3's *strict demand-first* range (0.0–30.8%, median 10.45) but **not** the 56–84% line,
  so no paper text is affected.


---

## §C — the N3 line "weak forward-or-tie share ranges 56–84%" does not reproduce

*(Added 25 Nov 2026, task-10. This section closes the "Additional audit note" item above.)*

### Where

`REPORT.md`, §3 N3, the "Result" paragraph. Original sentence (retained; a `CORRECTION` pointer now follows the
paragraph):

> **Result (`results/n3_table.csv`, 54 definitions; all have ≥20 countries).** The **demand-first strict share
> ranges 0.0–30.8% across definitions, median 10.45%**; the **weak forward-or-tie share ranges 56–84%** (ties and
> left-censoring dominate because GGDC demand take-offs are often at the series start).

### What reproduces, and from what

Source file: `results/n3_table.csv` (54 committed definitions; all have n ≥ 20). Candidate "weak forward-or-tie"
quantities and their exact ranges across all 54 definitions:

| quantity | denominator | range | min / max definition |
|---|---|---|---|
| weak tie (`forward_or_tie`) | identifiable = `n − undetermined` | **56.67–88.46%** | min `q1 Δs=0.5 Δr=5.0 smooth=1`; max `q1 Δs=1.5 Δr=2.0 smooth=7` |
| weak tie (`forward_or_tie`) | all countries in the definition (`n`) | **50.00–82.14%** | same definitions |
| `forward_share_incl_ties` ((forward + forward_or_tie) / identifiable) | identifiable | **56.70–100.00%** | min `q1 Δs=0.5 Δr=5.0 smooth=1`; max `q1 Δs=1.5 Δr=2.0 smooth=5` |
| (forward + `forward_or_tie`) | identifiable | **56.67–100.00%** | as above |
| (forward + `forward_or_tie`) | `n` | **50.00–92.86%** | as above |

**No denominator gives a range with endpoints 56 and 84.** Restricting the sweep to the 36 unsmoothed q1
definitions, or to the 36 non-survival definitions, gives the identical endpoint pairs (56.67–88.46 /
50.00–82.14 / 56.70–100.00), so the clause is not a subset artefact either. The lower endpoint 56 only matches the
lower end of the weak-tie/identifiable quantity (56.67, i.e. 17/30); **no** quantity has 84 as an upper endpoint
(nearest: 82.14 for weak tie/`n`; 88.46 for weak tie/identifiable). The line is therefore a **stale or
hand-rounded prose range**, not an error in `results/n3_table.csv` (the table itself is the reproducible object;
its strict demand-first 0.0–30.8% / median 10.45% and its q1 default 6.2 / 70.6 / 17.6 / 5.9 all reproduce).

**Recommended replacement** (state the denominator explicitly): "the weak tie share of identifiable countries
ranges 56.7–88.5%, or 50.0–82.1% of all countries in each definition; including weak-forward cases,
`forward_share_incl_ties` ranges 56.7–100.0%".

### Reproduction command

```
python3 scripts/erratum_check_n3_prose.py      # reads results/n3_table.csv; writes results/erratum_check_n3.json
```

### Effect on the papers

**None.** Paper M (`research/paper-massification-2026-11-25` @ `fb9f419`) and Paper N1
(`research/paper-sequencing-novel-2026-11-25` @ `62c27a3`) quote the N3 **strict demand-first** range
(0.0–30.8%, median 10.45%) and the E6 demand-first range (10.0–24.1%, bounds 6.7–53.0%, weak ties 21–43%); neither
quotes the weak forward-or-tie range. No paper text depends on 56–84%.

### Other prose-vs-table ranges found by this scan (listed, not silently fixed)

The scan also checked every other prose range in `REPORT.md`. All reproduced except two loose/stale ranges, which
are recorded here for a follow-up correction and are **not** changed in this commit:

1. **`REPORT.md` §2 "Estimator" paragraph (line 85): "25–30 control countries per event."** From
   `results/e8_results.json` (`SE.PRM.ENRR_verified8`, field `n_controls`, all eleven event rows) the observed range
   is **28–30** (min 28, max 30). "25–30" is loose rather than false — the observed values sit inside it — but the
   lower endpoint 25 is not realised; the exact statement is 28–30.
2. **`REPORT.md` §2 "Decision-rule assessment" paragraph (line 121): "(mean post 18–29 points against ~0 under
   placebo)."** The reproducible mean-post quantities from `results/e8_results.json` are: mean of the CS post
   ATTs at +1..+6 = **25.26**; sensitivity `mean_att_post` = 12.31 (`all+1`), 18.65 (`all-1`), 20.80 (`all12`),
   **18.17–26.16** (leave-one-out), **−0.39** (placebo). No quantity spans 18–29, so this line looks like a stale
   value from an earlier table; a reproducible replacement would be "mean post 12.3–26.2 across the ±1-year and
   leave-one-out checks, against −0.39 under the placebo".

Everything else audited reproduced: E6 demand-first 10–24% of identifiable countries and weak ties 21–43% of
in-window countries; E6 bounds 6.7–53.0%; the eight E6 table rows (0 mismatches); the eleven E8 event-table rows
(0 mismatches); E8 leave-one-out 18.17–26.16 and t0 7.00–13.94; 7–8 treated countries; N3 54 definitions all with
n ≥ 20; q1 default 6.2 / 70.6 / 17.6 / 5.9 and bounds 5.9–82.4; and the 100% below-75% statement.
