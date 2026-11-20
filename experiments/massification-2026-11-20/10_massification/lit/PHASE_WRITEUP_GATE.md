<!-- PHASE WRITE-UP GATE — the A-1…A-8 self-check of 10_massification/lit/PHASE_WRITEUP.md.
Authored by Writer Wu under D166/D168. Read-only checks: NO model run, NO re-run, NO re-score, NO new number.
The Council issues no SPINE-REPLACED verdict; the Lead checks this gate. Every result below is PASS or FAIL with
evidence lines; the overall string is PASS only because all eight hold. -->

# PHASE WRITE-UP GATE — A-1…A-8 self-check

| field | value |
|---|---|
| document under check | [`PHASE_WRITEUP.md`](PHASE_WRITEUP.md) (726 lines, 60,588 characters at the time of the check) |
| gate | **A-1…A-8**, frozen by D166 and ordered by D168 (W-1…W-6) |
| checker | the author (self-check), for the Lead's check; the Council issued **no** `SPINE-REPLACED` verdict and certifies nothing here |
| checks run | read-only, on disk: link resolution, claim-tag and one-sentence parse, banned-pattern scan with the quoted-and-barred register excluded, verbatim diff against `KAPPA_WRITE_REGISTER.csv` column `admissible_sentence`, HELD-table diff against `SYNTHESIS_026.md` Appendix B, numeric-token whitelist against the delivered result files |
| **overall** | **`WRITE-UP-GATE: PASS`** |

| gate | result | evidence |
|---|---|---|
| A-1 | **PASS** | 36/36 claims tagged and one-sentence; 16/16 tables captioned; 0 untagged claim sentences |
| A-2 | **PASS** | 0 untraceable numbers; 748 numeric tokens (218 distinct) outside the register, all mapped to the 21 provenance groups of Appendix G; 8 automated flags resolved |
| A-3 | **PASS** | 0 banned sentences outside Appendix F; 35 patterns scanned, 34 at 0; the one non-zero pattern is the quoted clause inside the mandated KOR counter-example |
| A-4 | **PASS** | two-object headline block present (W-1.1); the untagged headline occurs 0 times in the document |
| A-5 | **PASS** | 4/4 κ sentences verbatim with windows; KOR counter-example present; the barred κ-link and 2027 sentences absent; column 15 not lifted |
| A-6 | **PASS** | HELD table 14/14 rows match `SYNTHESIS_026.md` Appendix B verbatim; HKG two-part condition present with its standing third gate |
| A-7 | **PASS** | 12-arm range stated **with its arm set** (12 tuples enumerated; six-arm subset named) |
| A-8 | **PASS** | 79 links, 35 unique, **0** unresolved; the 14-item read order resolves |

---

## A-1 — every headline, caption and claim carries label · class tag · object · window · status · exactly one permitted sentence

**Result: PASS.**

**What was checked.** (i) Every claim in W-1…W-6 is introduced by a tag of the form
`` `[C-nn · label · class/object · window · status]` ``; (ii) the text after each tag is **one paragraph that ends with a
single full stop and contains no internal sentence break** (`\.\s+[A-Z(“]` returns 0 matches for all 36); (iii) every
markdown table is preceded or followed by a caption carrying the same five fields and a permitted-sentence reference;
(iv) no claim sentence exists outside a tag.

**Counts.** 36 claims (C-01…C-36, no gaps, no duplicates); 16 tables, 16 captions; 0 untagged claim sentences.

| # | label | class / object | window | status | permitted sentence (opening) | one sentence |
|---|---|---|---|---|---|---|
| C-01 | `SIM` | A1 anchor class (12 arms) · O-1 | — | CLOSED | "The phase's level statement is conditional level reproduction at fit MAE …" | yes |
| C-02 | `SIM` | `v1.7 (A17)`, closed `v1.5`–`v1.7` family · O-3 | — | CLOSED | "The post-close class is representation-only — upper-secondary unfilled 15/15 …" | yes |
| C-03 | `DERIVED` | O-1 / O-2 / O-3 | — | CLOSED | "The record carries three model/observed objects that may not be substituted …" | yes |
| C-04 | `SIM` | A1 anchor class (12 arms) | — | CLOSED | "On this record the cohort-flow class does not generate the positive income-scaling sign …" | yes |
| C-05 | `SIM` | the one-cell repair cell | — | CLOSED | "The licensed one-cell repair failed …" | yes |
| C-06 | `SIM` + `DECLARED` | A1 anchor class (12 arms) | — | CLOSED | "The capacity-timing claim is not credited …" | yes |
| C-07 | `OBS` + `SIM` | observed signature vs the 12 arms | — | CLOSED | "The observed signature is primary completion ≥90 first in 2017 …" | yes |
| C-08 | `DERIVED` | EXP-21 rows (system × level) | — | LIVE | "Completion and GER are one scale in 4 of the 12 frozen cells …" | yes |
| C-09 | `OBS` | PHL primary / lower / upper 2024 | — | LIVE | "The three 2024 PHL completion values are completion objects only …" | yes |
| C-10 | `OBS` + `DECLARED` | `ger_secondary` vs the level GER series | — | LIVE | "`ger_secondary` in 2024 is 85.2945085684493 and the level-specific series end in 2018 …" | yes |
| C-11 | `DERIVED` | EXP-21 row PHL/primary 2017 | — | LIVE | "PHL primary completion in 2017 is 91.91800689697266 percent and the conversion T …" | yes |
| C-12 | `DERIVED` | EXP-21 rows KOR/primary, CHN/lower_secondary | — | LIVE | "KOR/primary and CHN/lower_secondary rest on exactly one same-year pair each …" | yes |
| C-13 | `DECLARED` + `SIM` | A17, v1.3, v1.2 panels | — | CLOSED | "m = 1.10 is a DECLARED point convention on a synthetic panel …" | yes |
| C-14 | `OBS` | PHL three-level signature | — | LIVE | "The observed order is primary (91.91800689697266, 2017) then lower-secondary …" | yes |
| C-15 | `SIM` | the 12 arms against the M-vector | — | CLOSED | "No arm reproduces M2 and M3 …" | yes |
| C-16 | `DERIVED` | PHL gross − net spans | — | LIVE | "The observed participation margin is a same-year gross − net gap …" | yes |
| C-17 | `DERIVED` | the identity test over the audited candidates | — | LIVE | "The identity test fails at all three levels …" | yes |
| C-18 | `DERIVED` | the historical window vs the model year | — | LIVE | "The pairs end in 2017 (primary, lower) and 2015 (upper) …" | yes |
| C-19 | `DERIVED` | the D63 residual (upper-only leg) | — | LIVE | "The residual is 14.974746704101562 pp and it splits …" | yes |
| C-20 | `DERIVED` | the three bounds | — | LIVE | "Of the three declared bounds, B1 is OUTSIDE …" | yes |
| C-21 | `DERIVED` | the bounds verdict | — | LIVE | "BOUNDS-EDGE means 1 of 3 outside and nothing else …" | yes |
| C-22 | `DECLARED` | D63, as ruled | — | LIVE | "D63 stays UNABLE as to cause …" | yes |
| C-23 | `DERIVED` | PHL κ (transition ratio) | **2003–2024 / 2003–2017** | LIVE | "The PHL sentence, verbatim: …" | yes |
| C-24 | `DERIVED` | KOR κ | **2005–2023 / 2005–2020** | LIVE | "The KOR sentence, verbatim: …" | yes |
| C-25 | `DERIVED` | KHM κ | **2000–2023 / 2000–2017** | LIVE | "trending, shift 7.4361 pp …" | yes |
| C-26 | `DERIVED` | CHN κ | **2012–2020** | LIVE | "reported only; non-stationary; not a forward constraint …" | yes |
| C-27 | `DERIVED` | KOR as the counter-example | **2005–2023** | LIVE | "The KOR counter-example ships with the register …" | yes |
| C-28 | `DERIVED` | the κ use count and its universe | — | LIVE | "Of 309 enumerated uses, 299 are applied …" | yes |
| C-29 | `DECLARED` | the two κ symbols | — | LIVE | "Two different objects are written κ in this programme …" | yes |
| C-30 | `DECLARED` | the barred κ families | — | LIVE | "Two sentence families are barred from this write-up …" | yes |
| C-31 | `HELD` | 14 HELD objects + the HKG condition | — | LIVE | "Fourteen objects are HELD …" | yes |
| C-32 | `SIM` | A1 anchor class (12 arms) | — | CLOSED | "The phase's fit range is 1.047492271754753–3.2916863270693772 …" | yes |
| C-33 | `DECLARED` | the external read order | — | LIVE | "Three paths in the external read order do not resolve …" | yes |
| C-34 | `DECLARED` | the user's structural frame | — | LIVE (theory only) | "The programme carries the user's structural insight as DECLARED-THEORY …" | yes |
| C-35 | `DECLARED` | parks and verdicts | — | CLOSED | "The parks stand — A3 KILLED, the exit-cost/induction layer PARKED …" | yes |
| C-36 | `DECLARED` | the status of this document | — | LIVE | "This document is authorship, not an experiment …" | yes |

**Note on the 16 captions.** Seven use the form `*Table caption (A-1):*`; three use `*Table W-n — …*` (W-1.1, W-2.1,
W-3.1); six use `*Table X-n (A-1 caption):*` (A-1, B-1, C-1, D-2, F-1, G-1). Each carries label(s), object, κ window
where κ appears, status and a permitted-sentence reference. The one table with **no** permitted sentence of its own is Appendix F (F-1): it is the
quoted-and-barred register, no row of it is a sentence of the document, and its caption says so.

---

## A-2 — 0 untraceable numbers

**Result: PASS.**

**Method.** Every number in `PHASE_WRITEUP.md` is either (i) a value cell of a delivered results file, cited by path +
column in the text or in Appendix G, (ii) a `V`-id of
[`VERIFICATION_026.csv`](../../08_council/brief_026/VERIFICATION_026.csv) that resolves to such a cell, or (iii) a
structural token (a year, a section/table/claim/decision id, or a declared threshold). No number was computed for this
document.

**Scan (Appendix F excluded, because its numbers are quoted-to-bar source text).** 748 numeric tokens, 218 distinct.
White-list built from the 16 delivered result/data files of Appendix G plus the declared constants; 8 tokens were
flagged by the automated matcher and **all 8 were resolved by hand**:

| flagged token | resolution |
|---|---|
| `0.000704` | the PHL slope, stored as −0.000704 in `KAPPA_WRITE_REGISTER.csv` column `slope_ratio_per_year`; the document prints the Unicode minus, the matcher reads only ASCII |
| `0.14544291665697634` | row X1 `value_num` of `D63_BOUNDS_RESULTS.csv` (negative; Unicode minus in the document) |
| `2.733722425389776`, `2.526712979736413`, `1.0343696359734724` | `repair_scaling.csv` column `generated` (negative; ASCII hyphen in the document, minus-sign lookbehind on the matcher) |
| `0.8891573087274445` | `D63_BOUNDS_DETAIL.csv` rows D13 and P7 (`ratio_min`); also stated at full precision in V60 |
| `1.0724421619315192` | `D63_BOUNDS_DETAIL.csv` (`ratio_max`); also stated at full precision in V60 |
| `50` | the declared M4 milestone threshold (tertiary GER ≥50), a `DECLARED` value carried from the A6 signature, not a result |

**Provenance groups.** Appendix G lists 21 groups (12-arm table; calibration benchmarks; repair table; repair scaling;
observed path 9/33 and 0/33; `v1_7_checks`; representation cells; the 12 conversion cells; the 2017 `T` detail;
`M_CONSTANCY`; the universalization series; `PART_MARGIN_DESC`; the object-identity audit; the D63 results; the κ
register; the κ summary; the KOR counter-example; the HELD ledger; D76/D77; the read-order defect; the shell). Each
group names a file, a column or row key, and a `V`-id where one exists.

**Zero untraceable.** The three places where a number is quoted at a rounded precision rather than the stored
precision state both: `4.35` (stored 4.352883341604888, same cell) and `14.974747` (stored 14.974746704101562, same row,
`value_display`), and `58.6008 / 41.3992` (stored 58.6008386858443 / 41.3991613141558, rows S8/S9).

---

## A-3 — 0 banned sentences outside the quoted-and-barred register

**Result: PASS.**

**Method.** The 35 patterns below were scanned against the whole document with the marker block
`<!-- BANNED-REGISTER-START --> … <!-- BANNED-REGISTER-END -->` removed. 34 patterns return **0**. One pattern
returns **1**, and it is a permitted occurrence inside a mandated quotation (row 2 below). The literal string barred by
D-2 (the stale column-15 value) returns **0 in the whole file, register included** — it is registered by description
(B-17), not reproduced.

| # | pattern family | hits outside the register |
|---:|---|---:|
| 1 | the B-1…B-16 sentence families (demand, survival, conversion, participation, D63, κ phrasings) | 0 |
| 2 | the B-16 clause "κ-STABLE is forward-usable" | **1 — permitted**: it occurs only inside the **KOR counter-example** (C-27), the sentence that *bars* it and that A-5 requires verbatim; it is not asserted anywhere |
| 3 | the D-2 column-15 string and "κ is eligible as a forward constraint" | 0 |
| 4 | "every κ use on disk is in-window"; "the register is clean" | 0 |
| 5 | the proxy phrase B-19 and the two-level capability phrase B-20 | 0 |
| 6 | the untagged D77 headline and "the model reproduces the PHL level path" (B-21) | 0 |
| 7 | "v1.2 passes"; "the repair made the model worse" (B-22, B-23) | 0 |
| 8 | "EXP-25 ran"; a claimed spine-replacement verdict (B-24) | 0 as an assertion; the verdict token itself occurs once, negated (see below) |
| 9 | "no observed counterpart exists" unqualified (B-25) | 0 |
| 10 | "the 12-arm fit MAE is 2.03–3.29 pp" (B-26) | 0 (the stored value **2.03256440424153** does appear as a table cell — it is a single arm's fit, not the range) |
| 11 | κ-implied future values and the 2027 value (B-27) | 0; the barred number 87.710 appears nowhere |
| 12 | κ-link-as-validation (B-28) | 0 |

**One token, negated only.** The verdict token barred by B-24 occurs **once** outside the register — in the status
table at the top of the write-up, inside the negation "the Council issued **no** … verdict" — and once inside the
register (B-24). 0 occurrences as an assertion.

**The register itself** is Appendix F, B-1…B-28, opened and closed by explicit markers and headed "quoted only to bar";
no row of it is used as a sentence of the document.

---

## A-4 — the two-object headline block present; the untagged D77 headline absent as a post-close sentence

**Result: PASS.**

**Present (W-1.1), one sentence per object.** (1) The **phase object**, opening
"**PHASE OBJECT — A1 anchor class (12 arms), pre-close. Status `CLOSED` …**", carrying the 12-arm fit and holdout
ranges, the 4.35 pp benchmark, observational equivalence, the one unreproduced asymmetry and the placement **9/33**
with its `v1.2` / `v1.3 A00` tag. (2) The **post-close object**, opening
"**POST-CLOSE OBJECT — `v1.7 (A17)`, within the closed `v1.5`–`v1.7` family. Status `CLOSED` …**", carrying
representation-only, upper unfilled **15/15**, both-level queue **30/30**, strict both-level coexistence **0/15**,
**0/33** against the **≥17/33** bar, crossings **1/3**, and D63 `UNABLE` with the **58.6008 / 41.3992** split at the
declared t−3 pair.

**Absent.** The shell's untagged one-line headline (V68,
[`PHASE_WRITEUP_SHELL.md`](PHASE_WRITEUP_SHELL.md) line 15) occurs **0 times** in this document — not as a post-close
sentence, not as a caption, not anywhere, including the register (B-21 bars the unclassed fragment). Counts: full
string 0; unclassed fragment "conditional level reproduction" 1, in C-01, where it carries its class tag (A1 anchor
class, 12 arms), its statistic (fit and holdout ranges) and its date-status (pre-close, `CLOSED`) — the form B-21
permits.

**D77 applied, not amended.** The block says less about narrower objects than the single line did; D76/D77 are not
reopened, and the phase label is not amended (C-35).

---

## A-5 — the four κ sentences verbatim with windows; the KOR counter-example present; the κ-link and 2027 sentences absent

**Result: PASS.**

**Verbatim diff.** Each sentence below was compared character-for-character against
`KAPPA_WRITE_REGISTER.csv` column `admissible_sentence` (4 of 4 **MATCH**), and each ships with its system and its
window **in the same sentence-tag**:

| system | window (full / pre-2021) | verbatim | claim |
|---|---|---|---|
| PHL | 2003–2024 / 2003–2017 | **MATCH** | C-23 |
| KOR | 2005–2023 / 2005–2020 | **MATCH** | C-24 |
| KHM | 2000–2023 / 2000–2017 | **MATCH** | C-25 |
| CHN | 2012–2020 | **MATCH** | C-26 |

HKG/JPN are non-entrant with an empty window: no sentence ships for them, and none is invented.

**KOR counter-example.** Present (C-27), verbatim from `FINDINGS.md` §2, carrying slope +0.002875/yr, half-shift
0.6354 pp and 0/3 hold-out cells.

**Absent.** No citation of the κ-link as validation (0), no κ-implied future value (0), no 2027 value (0). The year
2027 occurs four times, none of them a κ sentence: an M3 model crossing year (C-15), the R29-flag reference in the same
claim, the bar statement in C-30, and B-27 in the register.

**No lift of column 15.** No table in the write-up has a forward-field column; the only forward label shipped is
`WINDOW-ONLY` (C-30), and the stale column-15 value appears nowhere (A-3 row 3).

---

## A-6 — the HELD table (14) and the HKG two-part condition present

**Result: PASS.**

**HELD table.** Appendix E carries all **14** rows (H1…H14); each row's object string was diffed against
`SYNTHESIS_026.md` Appendix B — **14/14 MATCH**, with the "what it would change" and "cell that would consume it"
columns also carried. The caption labels the table `HELD`, and the text states that none is fabricated, that user
approval is required for any of them (D157), and that no cell is issued against any of them.

**HKG re-entry condition.** Present, as two required parts plus the standing gate: **(i)** a stock-NER object passes
D120's **N2** construct test on the systems that have completion, **and (ii)** the **HELD single-age HKG population
1971–1996** (H6) is on disk — and, both parts once satisfied, **(iii)** a new Council decision authorises re-entry
(D120, D133, D156 EXP-24 item 5(iii), D157). The text also records that `DEFER-HKG` stands, that the frozen design is
preserved unrun, and that no HKG sentence appears in the document (the six HKG cells are `NO-COMPLETION-SERIES`).

---

## A-7 — the 12-arm range stated with its arm set

**Result: PASS.**

**The range.** Fit **1.047492271754753–3.2916863270693772**; holdout
**4.014780434743067–6.122199101442962** (W-1.1, W-1.3, W-6.2; `anchor_table.csv` columns `fit_mae`, `hold_mae`;
V69).

**The arm set, stated in the same place.** The 12 arms are named as **demand_led / education_led / complementary ×
{`law_only`, `capacity_gated`, `capacity_only`, `none`}**, all twelve rows are printed in Table W-1.1 with their fit and
holdout values and their `scaling_verdict`, and the range is stated to be the min–max **over those twelve rows**.

**The six-arm subset is named, not quoted bare.** If the six `law_only` + `capacity_only` arms are mentioned, the six
are listed by name (W-1.3) and no six-arm range is printed as if it were the 12-arm range (B-26, A-3 row 10). The
`PARTIAL` verdict is recorded as not depending on the range.

---

## A-8 — every read-order link resolves

**Result: PASS.**

**Check.** All markdown links in `PHASE_WRITEUP.md` were resolved against the filesystem, relative to
`10_massification/lit/`: **79 links, 35 unique targets, 0 unresolved** (0 missing, 0 absolute, 0 fragment-only). The
check was re-run after this gate file was created, so the four links to `PHASE_WRITEUP_GATE.md` resolve.

**The read order.** The 14-item corrected order in W-6.3 resolves entry by entry (each row's link is one of the 35
unique targets). The three dead paths of the external order are named in the text but **not linked**, because their
targets do not exist: `06_report/AGENT_PROTOCOL.md` and `06_report/MASSIFICATION_CLOSEOUT.md` (the root copies are
linked instead) and `LEAD_HANDOFF.md` (replaced by
[`HANDOFF_expert-council.md`](../HANDOFF_expert-council.md)); V71 is the defect record, and D-4 is the correction.

---

## Reproduction of these checks (no runner, no model, no data written)

The four mechanical checks can be re-run by a reader with a stock Python 3, from
`10_massification/lit/`:

1. **links** — collect `\[[^\]]*\]\(([^)]+)\)` from the file, drop `http…`, and `os.path.exists` each target.
2. **one sentence per claim** — split at each `` `[C-`` occurrence; assert the paragraph after the tag ends with `.`
   and contains no `\.\s+[A-Z(“]`.
3. **banned scan** — slice out the text between the two register markers, then count the 35 patterns of A-3.
4. **verbatim κ** — read `../extensions/kappa_write_2026-11-20/results/KAPPA_WRITE_REGISTER.csv` column
   `admissible_sentence` and assert each of the four non-empty system sentences is a substring of the document.

All four were run before this line was written; the numbers in A-1…A-8 are their outputs. **No model was run, no cell
was re-run or re-scored, and no file outside `PHASE_WRITEUP.md` and this gate file was written.**

---

## The result

**`WRITE-UP-GATE: PASS`** — A-1 PASS · A-2 PASS · A-3 PASS · A-4 PASS · A-5 PASS · A-6 PASS · A-7 PASS · A-8 PASS.

**What this does and does not mean.** It means the document is checkable against the frozen gate by a reader without a
runner, which is what D166 required of the hand-off. It does **not** mean the Council has certified the spine — the
Council issued no `SPINE-REPLACED` verdict, EXP-25 did not run, and the Lead's check is the authority this self-check
serves. If the Lead's check finds a failing item, the correct overall string is **`WRITE-UP-GATE: PARTIAL`** with the
failing items named, and — per D155/D167 — a failing write-up is a **writing failure, not a register**, and does not
reopen the experiment programme.
