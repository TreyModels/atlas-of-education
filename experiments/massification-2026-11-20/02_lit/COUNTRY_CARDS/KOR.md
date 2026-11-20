<!-- Iteration 2 country card. Compiler: lit-archivist, 2026-11-20.
Every number below carries its source and access status. "NOT FOUND" means I looked and did not
find a citable figure - it does not mean the phenomenon is absent. "NOT VERIFIED" means a figure
exists in a source I could not retrieve this session. Do not promote a NOT VERIFIED figure to a
calibration target without reading the original. -->

# KOR - Korea (country card)

**Headline for the model: the best-measured shadow sector in the world (official annual survey), and the only country with an *estimated* decomposition of competition-driven spending.**

## 1. Shadow education - official statistics

| Measure | Value | Year | Source (access) | Denominator |
|---|---|---|---|---|
| Private-education **participation rate**, elementary+middle+high | **78.5%** (+0.2pp vs 2022) | 2023 | Ministry of Data and Statistics (MODS, formerly MOE/KEDI survey), *Private Education Expenditures Survey of Elementary, Middle and High School Students in 2023*, press release 2024-03-14 (FULL-TEXT HTML) | all surveyed students |
| Total private-education expenditure | **27.1 trillion won** (+1.2tn, +4.5%) | 2023 | same | national total |
| Weekly participation hours per student | **7.3 hours** (+0.1h) | 2023 | same | per student |
| Avg monthly expenditure per student | **434,000 won** (+5.8%) | 2023 | same | per student |
| Avg monthly expenditure per **participating** student | **553,000 won** (+5.5%) | 2023 | same | per participant |
| General-subject expenditure per student / per participant | **326,000 / 518,000 won** | 2023 | same | per student / participant |
| Share spending >=700,000 won/month | **22%** (+2.9pp) | 2023 | same | per student |
| After-school programme participation | **41.0%** | 2023 | same | per student |
| Shadow education, **elementary** students | **~90%** | c.2011 | Bray & Lykins 2012, p. X, quoted verbatim by J. Dierkes, Jukupedia, 19 May 2012 (SECOND-HAND QUOTATION of the book's introduction) | elementary students |

**Verified cross-check on the manuscript's claim:** the June draft's "85% Hong Kong senior secondary" comes from the *same* Bray & Lykins page as the Korea ~90% elementary figure - see HKG card. Korea's own official series has since moved from the book's ~90% elementary figure to a 78.5% all-level rate.

**Model-relevant decomposition (not a take-up rate):** Kang (2026, FULL-TEXT) estimates that **77%** of secondary-school tutoring *expenditure* and **89%** in the final year is competition-driven (tournament channel), holding human-capital returns fixed; **less than half** of self-study time is competition-driven. These are **structural counterfactuals**, not observed shares - do not put them in a take-up target table.

## 2. Gates
- **CSAT (Suneung)** for university admission; **endogenous admission cutoffs from a seat vector** - Kang models college *tier*, not just admission.
- High-school equalisation and the post-2010 shift toward *admissions* competition (Kang's motivating fact: college tier is a vertical ordering that matters).
- Pass rates / seat counts by tier: **NOT FOUND** this session (Kang's data appendix not mined for these).

## 3. Cohort flows
- Tertiary entrance rate, completion, repetition: **NOT FOUND** this session (would need KEDI/KOSIS series; not retrieved).
- What is verified: the survey's *sample frame* is elementary+middle+high students, so participation can be read by level in the underlying KEDI file (`peesemhss2023.pdf`), which was **linked but not downloaded** - a 5-minute retrieval for whoever needs level-specific shares.

## 4. Economy context
- High tertiary participation, credential-intensive formal sector, severe youth labour-market queueing; **no verified numbers imported this session**.

## 5. Policy timeline
- Private-education expenditure surveys run annually since 2007 (KEDI -> MOE -> MODS); 2023 survey published March 2024. The 2024 survey is already published (linked from the same page).
- Curfew/regulation history (2008 hagwon curfew, 2014Special Act): **NOT VERIFIED** this session.

## 6. Disagreements / unverifiable
- The only disagreement that matters for calibration: **Kang's 77%/89% competition shares vs the possibility that they are artefacts of his functional-form choices**. They are model-implied; the paper should report them as "estimated" and never as "measured".
- Korea is the one country where the *level* target is unambiguous and official (78.5%, 2023). Use it as the benchmark that pins the model's overall intensity.
