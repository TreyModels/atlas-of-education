# Assessment of the 20-24 Nov 2026 work: what we have, what the papers should be, what to run next

Written 24 Nov 2026. Branch: `research/assessment-and-next-experiments-2026-11-24`. Nothing on any existing branch was changed.

## Read in this order
1. `PAPER_PLAN.md` - what the papers should be (four papers, one optional note, a stop list).
2. `CLAIMS_LEDGER.md` - every headline number with its status (holds / narrowed / dead / artefact / unverified), plus corrections to external reviews.
3. `TEXT_FIXES.md` - edits still required in the seven pushed drafts (one wrong headline, the "7%" claim, appears in three).
4. `NEXT_EXPERIMENTS.md` - runnable experiments with decision rules; written for DeepSeek and other agents.
5. `RUN_ON_SERVER.md` - how to run them on a rented CPU server.
6. `DATA_SOURCES.md` - data in this record and data still needed.

## One-paragraph answer
The programme has measurement, sequencing and falsification results and no identified causal mechanism. What stands: schooling
take-off precedes farm-labour release in 31 of 34 identifiable countries; the schooling-fertility link is a between-country level
gradient that future schooling predicts as well as current; fertility transitions are better fit by exponential-to-floor than by
a logistic in the annual window (not yet tested on complete transitions); and most cross-national links are group-specific or
no better than random. What fell: electricity, wage jobs, early marriage, care work, credential inflation, tipping points, and the
surplus-motor reading of the Philippine models.

## New results in this record (all exploratory; scripts and outputs in `scripts/` and `results/`)
| Result | File |
|---|---|
| The "labour demand precedes schooling in 7% of 58 countries" figure is a data-start artefact: the narrow demand series start in 1991, 92% of schooling take-offs are dated by 1990 | `results/demand_series_start_check.txt` |
| Orthogonalised future-schooling placebo: future schooling keeps a coefficient comparable to or larger than current schooling for lower-secondary, secondary and tertiary, with country fixed effects. It does not separate a common trend from anticipation/quantity-quality or a schooling effect (see PAPER_PLAN Paper 2) | `results/placebo_orthogonal.txt` |
| Income at onset is unrelated to fertility-transition timing (n=68); schooling timing survives it; starting child mortality explains 29% (onset) and 53% (midpoint) of the variance | `results/n4_gdp_mortality.txt` |
| Known-truth simulation of the grouping-multiverse verdicts: false positives 0-2%; group-specific tags undetectable at 25 draws, found from 100 draws; a link planted in one third of countries is labelled "robust everywhere" ~85% of the time | `results/known_truth_sim_summary.md` |

## Status of this session's work
- Run here: the four results above (single core, ~10 minutes in total).
- Not run here (needs network, a panel not in the repo, or >1 core-day): E1-E16 and N1-N8 in `NEXT_EXPERIMENTS.md`.
- Web check of fee-abolition dates done only against secondary sources (see CLAIMS_LEDGER C3); no primary source checked.
- Gemini's provenance claims for +0.05 +/- 0.19, the 60%/75% sign-flip shares and CR.3 67.5% -> 75.0% were not opened.

## Caveats on the simulation (read before citing it)
Simplified estimator (country-clustered OLS from per-country sufficient statistics), 150 countries, 50 years, 8 groupings, 100
replicates, three of the paper's four verdict tiers (no "beats random" tier). Effect sizes were set by looking at whole-sample t
statistics only; I saw the verdicts of a 4-replicate smoke test before changing the data-generating process (the effect was moved
from the innovation to the full series), and I replaced a first heterogeneity rule that was discretised by the 8 groupings
(`results/sim_run2_het_rule_v1_DISCARDED.log`). Run 1 of the paper rule alone is kept in `results/known_truth_sim_run1_paper_rule_only.json`.
It is a design check, not evidence about the substantive claims.
