# Required text fixes in the existing drafts (not yet applied; do not overwrite the pushed fix branches)

Apply on a new branch per paper, e.g. `fix/<paper>-demand7-2026-11-NN`.

## 1. The "7%" labour-market demand claim (ARTEFACT; see CLAIMS_LEDGER B6)
Replace every statement that labour-market demand "precedes the schooling take-off in only 7% of (58) countries" with: *the narrow
labour-market demand measures (paid-employment share, agricultural-employment share, and the productivity premium built from
them) are observed only from 1991, so they cannot precede the schooling take-offs, 92% of which are dated by 1990; the
precedence comparison is uninformative for these measures.* Keep the ten-year-change horse race (+0.456 vs +0.006, n=78), which does not
depend on take-off dates, but note its sample starts after 1991 for the labour-market variables.

| Branch | File | Lines |
|---|---|---|
| fix/sequencing-censoring-2026-11-24 | research/records/2026-11-25-paper-sequencing-novel/PAPER.md | 22, 230 ("the most damaging single result"), 274, 486 |
| fix/sequencing-censoring-2026-11-24 | .../claims-to-source.md | 17 |
| fix/massification-sequencing-2026-11-24 | research/records/2026-11-25-paper-massification/paper.md | 21, 90, 144, 612, 1113, 1148, 1242, 1260 |
| fix/massification-sequencing-2026-11-24 | .../part_finding.md | 14 |
| fix/massification-sequencing-2026-11-24 | .../claims-prior-art.md, claims-to-source-map.md | 39-49; 14 |
| fix/agdev-sequencing-2026-11-24 | research/records/2026-11-25-paper-agdev/paper.md | 148 (and the "Labour-market demand does not lead" paragraph) |
| fix/agdev-sequencing-2026-11-24 | .../claims-prior-art.md, claims-to-source.md | 19; 57 |

Also revise the Council's claim #1 supporting statement if it quotes the 7%.

## 2. Methods paper: what "robust everywhere" certifies (CLAIMS_LEDGER B8)
`fix/methods-multiverse-2026-11-24`, `research/records/2026-11-23-multiverse-paper/paper.md`:
- Section 3.4: state that the robust-everywhere rule is a significance-and-similarity criterion and does not test homogeneity of
  magnitude. Add the heterogeneity condition or rename the tier.
- Section 5.3 ("the five links that travel"): re-test the five with the heterogeneity condition (E3) before keeping the word "travel".
- Section 6.8: replace the future-tense known-truth plan with the simulation in `results/known_truth_sim_summary.md` (design
  frozen before looking, simplified estimator, 100 replicates, R in {25, 100, 400}), and say the full-estimator version (E2) is pending.
- Draw-count section: add the empirical fact that group-specific tags are not detectable at R=25 and appear only from R=100,
  with 49% detection of the planted tag at R=400 (BH floor 1/(R+1)=0.0025 is exactly the first threshold).

## 3. Fertility audit
- Add the orthogonalised placebo (A6) to the placebo section; keep the "co-trending" wording and add that it cannot be separated
  from a causal slow-moving gradient by these data.
- Label nulls "power-calibrated" only where an MDE is computed.

## 4. Shape paper (N4)
- Add income-at-onset null (A8) and starting-mortality result (A9) as post-hoc, exploratory, with n and the sample change (n=60 vs 90).
- State that the annual window cannot distinguish a non-logistic form from an unidentified logistic, and name the double-logistic
  UN model as the comparator (E15).

## 5. Fee-abolition mentions
Wherever the +22-28 point effect is cited: "dates from secondary sources, partly conflicting (Cameroon 1999/2000, Ghana 1997/2005,
Ethiopia 1994/1995, Tanzania 2001/2003, Malawi 1994/1995, Mozambique 2004/2005); TWFE with staggered adoption; to be re-estimated."
