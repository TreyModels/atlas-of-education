# Discrepancy log: independent auditor (novelty-review) vs Paper M

Auditor: `novelty-review` (task-35). Memo: `research/records/2026-11-24-lit-audit/referee-memo-paper-M.md`
(branch `research/lit-audit-2026-11-24`). Diff message: 24 Nov 2026. This file records every item and its
resolution. Status: **FIXED**, **DISPUTED-WITH-REASON**, or **OPEN**.

## A. Referee-memo items

| # | item | status | resolution |
|---|---|---|---|
| A1 | "Schools before factories is not new" — must cite Sandberg 1979, Mitch 1992, world-polity, Squicciarini & Voigtländer 2015, de Pleijt & van Zanden 2016 | FIXED | Section 1 now cites all of them and the claim is reframed as systematic coding, not direction; Section 3 asks "has anyone established this ordering?"; claims-prior-art Claim 1 rewritten with the prior claims and the "new assembly" label |
| A2 | Dates/coding are the paper — need date-by-date source table and recoding robustness | PARTLY FIXED / OPEN | date-perturbation robustness added (Section 6.3; median 26, IQR 16–29 across all 64 / 17–29 across the 61 forward cases, 93% >10y, 15y uniform error needed); alternative-threshold re-detection and the date-source table are named as the central vulnerability (Section 15, Section 13.1) and are **open** because the raw series were on a server that went down |
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

The auditor's verdict is that the 61/64 event-ordering comparison is **not known as a systematic test**: the
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
