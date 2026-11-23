# Auditor marks on the Synthetic Council 42-claim inventory (810506b)

`novelty-review`, 24 November 2026. Companion to `claims-map.md`, `discrepancy.md`,
`centerpiece-verdicts.md`, `paperF-final-read.md`, `paperN4-final-read.md`.

**Method.** I marked each inventory row against my independent audit, not against the Council's verdicts. Marks:
**AGREE** = my audit supports the row as written; **ADJUST** = row is right but needs the wording/status I give;
**VERIFY** = I re-derived the number and confirm it; **NOTE** = prior-art or caveat to attach; **FLAG** = residual
integrity risk. I independently re-derived the M6 ordering figures from the committed
`data/event_dates_subsistence_v2.csv` (see below).

## A. Fertility block

| Row | Mark | Auditor note |
|---|---|---|
| F1-F3 | AGREE | match the audited panel results; prior work: Caldwell 1980, Cleland-Rodríguez 1988, Kravdal 2002 on the level side; Durlauf et al. 2005, Eberhardt-Teal 2011 on the levels-vs-changes method. |
| F4-F5 | AGREE (NOTE) | 400-draw and 13,800-draw batteries are different runs — keep both labelled as separate batteries, do not merge the percentages. |
| F6 | AGREE (NOTE) | ~90% placebo is the paper's key caveat; the placebo is a diagnostic, and the 80% decision rule is now documented in PREREGISTRATION.md (Paper F @ f9dd325). |
| F7 | AGREE | shape V / conventional hinges U — matches Paper F's verdict-table grade S (shape) / C (hinges). |
| F8-F11 | AGREE | matrix, UN marriage, mechanisms, level-vs-volatility as recorded; F11's volatility null is the new part, the level link is known since the child-survival literature. |
| F12-F13 | **ADJUST** | project-record findings I did **not** independently recompute (transition ordering: mortality leads fertility 12y; schooling precedes fertility by 15y in 67%). Mark them "project-record, auditor not reconfirmed" — the same recomputation discipline applied to the 37.5% should apply here. |
| F14 | AGREE (NOTE) | model-structural counterfactual; the negative out-of-sample result is the publishable part, not a causal finding. |
| F15 | AGREE | tie, correctly labelled N. |
| F16 | AGREE | negative result (identification limit) — good. |
| F17-F19 | AGREE | nulls; keep them as nulls, not as "refutations". |
| F20 | AGREE (NOTE) | ecological/micro split correct; the DHS gradient is the key referee risk in Paper F and must stay labelled V (ecological) / U (micro). |
| F21 | AGREE (NOTE) | credential measurement only; credential inflation itself is a 50-year-old claim (Collins 1979; Spence 1973; Arrow 1973). |

## B. Massification block

| Row | Mark | Auditor note |
|---|---|---|
| M1 | AGREE (NOTE) | multiverse method prior art: Steegen et al. 2016, Simonsohn et al. 2020, Patel et al. 2015. |
| M2 | AGREE (post-diff) | INCREMENTAL / border-NEW design arithmetic is the honest rank; dependence kill shot recorded. Prior: Simonsohn et al. 2015/2020; Patel et al. 2015; Klau et al. 2020; BY 2001. |
| M3-M4 | AGREE | gap-fill and controls audits. |
| M5 | AGREE (NOTE) | closest competitor: Porzio, Rossi & Santangelo 2021 (NBER w29390); world-polity prior: Boli et al. 1985, Ramirez & Boli 1987, Soysal & Strang 1989, Benavot-Riddle 1988, Meyer et al. 1992, Schofer-Meyer 2005. |
| M6 | **VERIFY** | I independently recomputed both orderings from the committed event CSV: schooling-vs-fertility on 64 three-event countries = **24 schooling-first (37.5%)**, 20 simultaneous (31.25%), 20 fertility-first (31.25%), median gap 0 (IQR −5/+8); all 81 = 29 (35.8%); the 68.75% is 24 + 20 ties. Release-vs-fertility on the 64 three-event countries = **60/64 fertility-first (93.75%)**, 4/64 release-first (AFG, LBR, MWI, ZMB), 0 ties — matches the corrected row. Both correct. Keep the "systematises a known pattern" framing (Sandberg 1979; Mitch 1992; Porzio et al. 2021). |
| M7 | AGREE (NOTE) | Boppart et al. 2023 (10.3386/w31101); Herrendorf et al. 2014 chapter is only NBER-WP-verified. |
| M8 | AGREE (NOTE) | Heaps 0.333 is below the 0.4-0.6 canon; ILOSTAT 1-digit aggregation caveat must travel with the number. |
| M9-M10 | AGREE | GPU scale/batch-layout dependence; credential-inflation audit only. |

## C. Synthesis records

| Row | Mark | Auditor note |
|---|---|---|
| P1 | AGREE (update) | Paper F now signed off at **f9dd325** (four auditor fixes closed; all framing checks passed). |
| P2 | AGREE (update) | Paper M fertility-ordering corrected at **95dc135** and independently re-verified by me; two declared opens remain (threshold recoding, date-source table). |
| P3 | AGREE | Paper N1 correctly excluded the 68.75% and flagged it; N2 folded the levels memo. |
| P4 | NOTE | Paper S/BOPPART sections were not part of my six-paper read; only their refs were spot-checked (Boppart 10.3386/w31101 V; Gollin et al. 2002 V; Restuccia et al. 2008 V; Acemoglu-Restrepo 2018 V). |
| P5-P6 | AGREE | Earlier novelty ledger and this audit are consistent after the corrections. |

## D. Measurement / infrastructure

X1-X7: **AGREE**. X6 (GPU determinism audit, `all_identical=False`) and X7 (ABC weight collapse, ESS ≈ 1/600) are
correctly classified as audit/methods value, not new correlations — these were the two candidates missing from the
first inventory pass and they are now in.

## Residual integrity flags for the Council record

1. **Release-vs-fertility 60/64 has no committed recompute artefact.** The number is correct (I re-derived it), but
   unlike the schooling-vs-fertility 37.5% it has no script/output committed next to the source CSV. Add the same
   kind of artefact (`recompute_release_ordering.py` + JSON) or a line in
   `subsistence-v2/results/NOTE_fertility_ordering.md` so the figure cannot repeat the 68.75% failure mode.
2. **F12/F13 transition orderings are project-record only** — not independently recomputed in this audit; mark them
   accordingly in the inventory.
3. **Do not merge F4 and F5** (400-draw vs 13,800-draw batteries) — they are separate runs with different
   percentages.

---

## LOOP CLOSED — Council a2128d1 (24 Nov)

Both flagged items are fixed and verified:
1. **Sample labels**: DECISION.md, NOVELTY_INVENTORY.md M6 and CANDIDATES.md now state both samples explicitly —
   64 three-event countries: 60 fertility-first / 4 release-first (93.75% / 6.25%), 0 ties; 95 countries with both a
   farm-exit and a fertility date: 86/9 (90.53% / 9.47%), 0 ties, with the nine named (AFG, LBR, MWI, ZMB, BDI, BFA,
   ERI, NGA, TLS). The earlier "64 countries with both dates" label is gone.
2. **Committed recompute artefact**: `lit/recompute_release_fertility_ordering.py` + `lit/release_fertility_ordering.json`
   exist next to the data, with the CSV sha256 recorded. I verified the hash my downloaded Paper M CSV gives is
   `d0c02f95ade0850e…` (exact match), and the JSON's four orderings reproduce my independent derivation exactly:
   schooling-vs-fertility 64 = 24/20/20 (37.5% [26.67, 49.75]); all-81 = 29 (35.80%); release-vs-fertility 64 =
   4/60, 0 ties, median gap −25.5; both-dates 95 = 9/86, 0 ties, median gap −20.0.
My other marks are folded (F12-F13 "project-record, auditor not independently recomputed"; F4-vs-F5 separate-battery
note; P1 signed off at f9dd325; P2 corrected at 95dc135/76d929a with the two opens; section E added). **Council
inventory: CLOSED.**
