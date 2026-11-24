# Discrepancy log: independent auditor (novelty-review) vs Paper M

Auditor: `novelty-review` (task-35). Memo: `research/records/2026-11-24-lit-audit/referee-memo-paper-M.md`
(branch `research/lit-audit-2026-11-24`). Diff message: 24 Nov 2026. This file records every item and its
resolution. Status: **FIXED**, **DISPUTED-WITH-REASON**, or **OPEN**.

## A. Referee-memo items

| # | item | status | resolution |
|---|---|---|---|
| A1 | "Schools before factories is not new" — must cite Sandberg 1979, Mitch 1992, world-polity, Squicciarini & Voigtländer 2015, de Pleijt & van Zanden 2016 | FIXED | Section 1 now cites all of them and the claim is reframed as systematic coding, not direction; Section 3 asks "has anyone established this ordering?"; claims-prior-art Claim 1 rewritten with the prior claims and the "new assembly" label |
| A2 | Dates/coding are the paper — need date-by-date source table and recoding robustness | PARTLY FIXED / OPEN | date-perturbation robustness recomputed with boundary dates treated as censored (Section 5.3; 34 of 64 identified, 31 forward; both-exact median 18, IQR 8–31; 26 of 34 forward after a 15y error); the earlier median 26 / 93% >10y figures are withdrawn; alternative-threshold re-detection and the date-source table are named as the central vulnerability (Section 15, Section 13.1) and are **open** because the raw series were on a server that went down |
| A3 | Horse race under-identified | FIXED | called a **decomposition, not a test** (Section 7.6 and 12.4); names the natural experiments needed (compulsory-law adoption, church-state competition, colonial schooling policy) in Sections 7.6, 13.3 |
| A4 | Scaling/θγ presented as tested claim | FIXED | Section 10 labelled a diagnostic frame, θ/γ not fitted, data gap stated |
| A5 | Credential inflation is a 50-year-old claim | FIXED | Collins, Spence, Arrow, Bills & Brown cited; contribution limited to the measurement, with the data gap stated |
| A6 | Drivers null must carry power statement AND positive micro literature | FIXED | Section 10.4 carries the 400-draw resolution arithmetic and explicitly says the country-panel null is not evidence electrification does not matter; positive micro literature cited as the counterweight |

## B. DOI/record-integrity diff (auditor checked each against Crossref directly)

| # | item | status | resolution |
|---|---|---|---|
| B1 | claims-prior-art.md had four wrong DOIs: Boli et al. 1985 (10.1086/447306), Meyer et al. 1992 (10.2307/2112690), Benavot & Riddle 1988 (10.2307/2112628), Soysal & Strang 1989 (10.2307/2112832) | FIXED | all four replaced with the correct values already present in refs.md: 10.1086/446504, 10.2307/2112679, 10.2307/2112627, 10.2307/2112831 |
| B2 | books cited with review-article DOIs: Becker 1964 (10.2307/2229541 review), Schultz 1964 (10.2307/2228861 review), Soysal 1994 (10.2307/2077636 review), Lindert 2004 (10.1086/531331 review) | FIXED | Becker/Schultz/Soysal: DOI removed, marked no book DOI; Lindert: replaced with the verified book DOI 10.1017/cbo9780511510717 |
| B3 | Becker 1960 DOI 10.3386/w1793 resolves to a different 1986 paper | FIXED | DOI removed; cited as book chapter, UNVERIFIED |
| B4 | Nelson & Phelps 1966 DOI 10.58837/chula.taic.522 resolves to unrelated item | FIXED | DOI removed; cited without DOI, UNVERIFIED |
| B5 | Mincer 1958 claims-entry DOI 10.1086/258116 resolved to a Japanese-economy book review | FIXED | claims-prior-art now uses 10.1086/258055 (the value already in refs.md) |
| B6 | Paper F refs.json may use 10.1086/258116 for Mincer 1958 | FIXED (relayed) | Paper F lead (un-data) messaged with the correct DOI 10.1086/258055 |
| B7 | citation-integrity watch: every refs.md DOI must be checked against metadata, not just resolution | FIXED | Part A entries carry title/year-matched status; no-match/weak entries are flagged; Part C auditor statuses marked "re-verification pending" |

## C. Centerpiece verdict

The auditor's verdict is that the schooling-versus-release event-ordering comparison is **not known as a systematic test**: the
world-polity school argued mass schooling precedes economic demand (Boli et al. 1985; Soysal & Strang 1989; Meyer
et al. 1992) and economic history has case narratives (Prussia, Britain, France, US), but no common event-ordering
comparison across ~64 countries with bootstrap intervals was found. Verdict: **INCREMENTAL-NEW assembly**,
contingent on (a) the date table and (b) the paper stating it systematises a known pattern. We accept the verdict
and hold that line: the paper's claim is the systematic measurement and the supply/demand decomposition, not the
direction, and the dates/coding vulnerability is stated as the central one.

## D. Remaining open items before submission
1. Alternative-threshold recoding (Section 13.1) — blocked by data unavailability in this session.
2. Date-by-date source table with page references for the historical cases (Section 13.2).
3. Re-verify Part C auditor-supplied DOIs in this paper's own Crossref run.
4. Paper F's refs.json Mincer line (relayed; un-data to fix).

## E. Closest competitor identified by the auditor (24 Nov 2026)

Porzio, Rossi and Santangelo (2021), *The Human Side of Structural Transformation* (NBER WP 29390, Crossref ✓
10.3386/w29390, re-verified in this pass) is the closest prior claim in direction: human capital accumulation as a
driver of structural transformation. Status: **FIXED** — cited in Section 1 and in `claims-prior-art.md` Claim 1 as
the closest competitor, with the design difference stated (their quantitative model + micro evidence on skill
reallocation vs our cross-country event ordering and supply/demand decomposition). Their work is complementary;
no precedence is claimed.

## F. Fertility-ordering figure: 68.75% vs direct recomputation (30 Nov 2026 — blocking fix for submission)

**The discrepancy.** The source record `subsistence-v2 @ ce66cfc` reports
`pct_schooling_before_fertility = 68.75` in `results/sequencing.json` (and `sequencing.txt`: "schooling before
fertility: 69%"). A direct recomputation from the same record's `results/event_dates.csv` does **not** reproduce
it: under a strict ordering (schooling take-off year < fertility decline year) it is **24/64 = 37.5%** in the
64-country three-event sample (bootstrap 95% interval 26.6–50.0%), with **20/64 = 31.3% simultaneous** (both
take-offs in the same year) and **20/64 = 31.3% fertility-first**; across all 81 countries with both dates it is
**29/81 = 35.8%** (CI 25.9–45.7%), ties 33.3%. The JSON's 68.75% is obtained by counting the 20 simultaneous cases
as schooling-first (24 + 20 = 44; 44/64 = 68.75%). Paper N1 (`research/paper-fertility-2026-11-25` @ `7f73ff1`)
independently found the same discrepancy (its PAPER.md lines 458–459 and claims-to-source.md line 25) and does not
use the 68.75% figure.

**Resolution.** Paper M adopts route (a): it now reports the **strict ordering (37.5%, 95% interval 26.6–50.0%;
31.3% simultaneous, 31.3% fertility-first; median gap 0, IQR −5 to +8)** and states the JSON/CSV discrepancy
explicitly, in the abstract (paper.md line 77), Section 2 (line 137), Section 6 (line 513), the "What we know now"
box (line 1101), README line 42, and claims-to-source-map claim 3. The 69/68.75% figure is not presented as a
headline anywhere. The recomputation is committed: `scripts/recompute_fertility_ordering.py` (input
`data/event_dates_subsistence_v2.csv`, a verbatim copy of the committed event CSV; output
`data/recompute_fertility_ordering.json`, seed 7, 1,000 bootstrap resamples of countries).

**Status: FIXED.** The record-level JSON field remains wrong upstream; Paper M flags it rather than propagating it,
and the record owner should correct `sequencing.json`/`sequencing.txt` for future users.

## G. Release-vs-fertility ordering check (30 Nov 2026)

Surfaced by gpu-dose while fixing N3: the **release-vs-fertility** ordering is a different comparison from
**schooling-vs-fertility**, and its 4/64 = 6.25% must not be mixed up with the schooling–fertility tie count.
Checked every Paper M file for a release-vs-fertility claim: **none is used**. The only "release-first" mention is
paper.md line 76, which refers to agricultural release before **schooling** (the 4.7% reverse case), not release
before fertility; the fertility-ordering passages (paper.md lines 77, 137, 513-517, 1106-1107) are all
schooling-vs-fertility; claims-to-source-map claim 3 is schooling-vs-fertility; there was no release-vs-fertility
row. The source record's `sequencing.txt` line "release before fertility: 6%" is consistent with the strict
recomputation.

Independent recomputation from the committed `data/event_dates_subsistence_v2.csv` (same code path,
`scripts/recompute_fertility_ordering.py` class of arithmetic): **release-first 4/64 = 6.25%** (bootstrap not
reported; zero ties), **fertility-first 60/64 = 93.75%**; across all 95 countries with both dates 9/95 = 9.47%
release-first, 0 ties, 90.53% fertility-first. This matches gpu-dose's independent recomputation exactly
(release-first AFG, LBR, MWI, ZMB). Action taken: a clarifying sentence was added to Section 6 distinguishing the
two orderings, and claims-to-source-map row 31 records the check. No existing claim or number was changed.
**Status: VERIFIED, not used as a claim.**
