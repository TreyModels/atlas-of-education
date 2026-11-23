# Multiverse methods paper — record README

**Status:** complete draft, 23 November 2026. The manuscript is `paper.md` in this directory. It incorporates **both** runs: the 74-draw run (`research/records/2026-11-23-grouping-multiverse/`) and the 400-draw run (`research/records/2026-11-23-grouping-multiverse-400/`). No placeholders remain. This record is the paper's public face, so every number in it is traceable to a named results file below.

**Reviewer-facing verdict (honest):** 3.5/5 — a method that finds only five robust links out of 272, and finds that they are the least surprising five, is a method that is working. The paper's strength is methodological (the resolution analysis and the transportability framing), not the substantive payoff; the group-specific labels are hypotheses, not findings.

**Branch:** `research/methods-multiverse-paper-2026-11-23` (off `research/grouping-multiverse-2026-11-23`). The 400-draw record directory `research/records/2026-11-23-grouping-multiverse-400/` is merged into this branch (from branch `research/grouping-multiverse-400-2026-11-23` @ `1152cec`), so every results file cited by the paper is present on this branch and a reader who clones it can trace every number without switching branches.

## What is in this directory

- `paper.md` — full manuscript: abstract; introduction (Durlauf as named foil); literature review; method; data; results sorted under (1) Fertility and (2) Massification; resolution analysis; relation to prior work; discussion; limitations; reproducibility; target venues; appendices (definitions, grouping inventory, plain-language abstract and five-point summary).
- `README.md` — this file.
- `refs.md` — APA 7th bibliography with per-entry verification status.
- `lit-review.md` — prior-art search and standing assessment (23 Nov 2026): closest work (multiverse, vibration of effects, cross-national multiverse applications, heterogeneity critique), what is genuinely ours vs borrowed, an honest strength score for each result, a use/don't-use checklist for other researchers, and the situating patch (nine verified references; applied in this revision to §2.1 and §2.8 of the paper — see commit 45b2ad5).
- `scripts/verify_refs.py` — Crossref DOI checker used for the bibliography (prints bibliographic fields only).
- `scripts/find_refs.py` — Crossref bibliographic search used to recover DOIs for the entries whose DOI was uncertain.

## Verified vs provisional

**Verified (from pushed results, reproducible from the repository):**

- Whole-sample counts 127 / 43 / 26 (74-draw run) — `2026-11-23-grouping-multiverse/results/summary.txt` line 3.
- Verdict counts 5 / 81 / 27 / 159 (74 draws) — `.../results/summary.txt`, "Class counts by topic".
- Verdict counts 5 / 76 / 30 / 161 (400 draws) — `2026-11-23-grouping-multiverse-400/results/headline.json`, `class_new`.
- 46 beats random at 400 draws (42 survive of old 43, 1 dies, 4 new) — 400 record README, "Bottom line"; `headline.json`, `tier2_retest` / `movement_tier2`.
- 43 beats random, 21 worse, 36 flips at 74 draws — 74 record README; `summary.txt` lines 4–6.
- 20 worse, 32 flips at 400 draws — 400 record README; `headline.json`, `tier2_retest`.
- Strict tier at 400 draws: 35 up certified (30 at ceiling), 19 down, 15 flips, 53 heterogeneity — `headline.json`, `new_counts` and `empirical_floor_check`; cross-checked against statsmodels `fdr_bh` (same file, `statsmodels_bh_crosscheck.matches = true`).
- Resolution arithmetic: floor 1/401 = 0.00249; BH first step 0.05/272 = 0.00018; 5,440 draws for a lone link; cluster table 1→5,440, 5→1,088, 10→544, 14→389, 20→272, 30→182, 35→156 — `headline.json`, `draws_needed_for_BH`, `empirical_floor_check.draws_for_cluster`.
- Five robust links — 74: `2026-11-23-grouping-multiverse/results/edge_table.csv` rows `u5mr->fertility`, `life_exp->fertility`, `u5mr->life_exp`, `agri_va->gdppc_log`, `gdppc_log->urban`; 400: `...400/results/edge_table400.csv` same rows (same five; see below).
- Fertility per-application counts (2 robust / 3 beats-random-no-clear-group / 13 group-specific / 14 no-better) — 400 record README, section "(1) Fertility".
- Massification per-application counts (0 robust / 7 beats-random-no-clear-group / 30 group-specific) — 400 record README, section "(2) Massification".
- Wage-employment null examples (9% vs 16%; 6% vs 3%; 21% vs 21%) — 74 `edge_table.csv` rows `wage_emp->lsc`, `wage_emp->sec`, `wage_emp->ter` (`share_TR`, `null_TR`); the 400 README confirms no wage link beats random.
- Halves stability: 42 both, 43 vs 49, 8 disagreements, overlap 84%, full agree 267/269, Spearman 0.994, null-share max diff 0.76 pp — `...400/results/headline.json`, `halves`.
- Determinism: bit-identical replicates 7/250/400 and real pass; 74 overlapping draws identical — `...400/results/determinism.txt`; `headline.json`, `determinism_vs_old_run`.
- Runtime: 3,711 s, 38,420,908 regressions, 16 workers, ~9.2 s/draw — `...400/results/run400.log`; `headline.json`, `runtime_seconds` / `total_fits`.
- 74-draw runtime total 7,185,790 regressions — `2026-11-23-grouping-multiverse/results/summary.txt` line 1.

**Provisional / weakest claims (flagged in the paper):**

- **Group-specific labels are the least certain verdicts.** They rest on a smoothed-null test across ~16,600 tag-by-link comparisons; at 400 draws a single tag claim cannot be certified strictly (same floor arithmetic). Treat as descriptions of where a link is concentrated, not certified claims.
- **Single-region and single-class claims** (e.g. farm output → lower-secondary completion in Latin America) are the weakest evidence in the run.
- **The 4 new beats-random links** (wage employment→child mortality, secondary completion→wage employment, female labour participation→secondary completion, birth rate→life expectancy) are new at 400 draws and depend on the normal fit; the t-fit version keeps 2 of them.
- **The strict-tier count (35) depends on BH's positive-dependence assumption** for the shared 400 draws; a dependence-free (Bonferroni) rule would certify fewer, more draws would certify slightly more.
- **The t-fit tier** certifies 42 links against 46 for the normal fit (median fitted df 157; they agree on 42, disagree on 4).
- **Data provenance is a working compilation, not a published dataset.** Per-series sources are carried in the panel metadata but were not re-verified series-by-series for this paper; confirm before submission.

**Not done in this paper (stated as such):**

- No known-truth simulation of the verdict rules' size and power (Section 6.7 lays out the design; the project's simulation branch is the intended home).
- No GPU implementation in the reported runs; all numbers are CPU.
- No causal identification; the paper says plainly the method tests transportability, not identification.

## Plain-words summary of the paper

The paper asks a simple question about a common kind of cross-country claim: a single number from a panel of countries is an average over countries that may not share the relationship at all. It answers by cutting the countries into groups 50 different ways (region, income, birth rate, schooling, farm economy, taxes, data-driven clusters, trajectory classes), rerunning the whole analysis inside every group, and comparing with random cuts of the same sizes. Random cuts are the yardstick for what chance alone produces. Two things follow: the method can tell claims that travel across country types from claims that only hold in some types, and the number of random cuts is a hard ceiling on how strong the evidence can be. In the two applications, two demographic links travel (child mortality and life expectancy to fewer births), no schooling-expansion driver travels, and paid employment is a clean null. The honest limit: 400 random cuts can vouch for a cluster of very strong findings but not for one finding on its own; a lone finding would need about 5,440 cuts.

## Files behind each headline number (quick map)

| Headline | File | Field / location |
|---|---|---|
| 127 / 43 / 26 whole-sample links | 74 record `results/summary.txt` | line 3 |
| 5 / 81 / 27 / 159 verdicts (74 draws) | 74 record `results/summary.txt` | "Class counts by topic" |
| 5 / 76 / 30 / 161 verdicts (400 draws) | 400 record `results/headline.json` | `class_new` |
| 46 beats random; 42 survive / 1 dies / 4 new (400) | 400 record `results/headline.json` | `tier2_retest`, `movement_tier2` |
| 35 up / 19 down / 15 flips / 53 het certified (strict) | 400 record `results/headline.json` | `new_counts` |
| floor 1/401, BH 0.05/272, 5,440 draws | 400 record `results/headline.json` | `floor`, `bh_min_p`, `draws_needed_for_BH` |
| cluster table (1→5,440 … 35→156) | 400 record `results/headline.json` | `empirical_floor_check.draws_for_cluster` |
| five robust links + their statistics | 74 record `results/edge_table.csv`; 400 record `results/edge_table400.csv` | rows `u5mr->fertility`, `life_exp->fertility`, `u5mr->life_exp`, `agri_va->gdppc_log`, `gdppc_log->urban` |
| fertility split (2 / 3 / 13 / 14) | 400 record `README.md` | section "(1) Fertility" |
| massification split (0 / 7 / 30) | 400 record `README.md` | section "(2) Massification" |
| halves stability (42 both; 267/269 agree; ρ 0.994) | 400 record `results/headline.json` | `halves` |
| determinism (max diff 0) | 400 record `results/determinism.txt` | all blocks |
| runtime 3,711 s / 38,420,908 regressions | 400 record `results/run400.log`; `headline.json` | last line; `runtime_seconds`, `total_fits` |

## Report format compliance

- Plain words: the README's summary and the paper's Appendix C contain no variable names and no Greek letters; the technical sections use standard terms for an academic audience.
- The two applications are sorted under "(1) Fertility" and "(2) Massification" in the paper (Sections 5.6 and 5.7).
- For every headline number the paper gives the estimate, the uncertainty (or the resolution caveat), the sample, and the test designed to kill it (the multiverse verdict, the random-grouping null, the split-halves test, the determinism check).
- Nulls are reported prominently: 161 of 272 links are no better than random; paid employment is a clean null; electricity is a weak, group-dependent driver.
- Every file is listed above; provisional numbers are flagged in the "Provisional" section.
