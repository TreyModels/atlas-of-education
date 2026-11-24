# Multiverse methods paper — record README

**Status:** complete draft, 23 November 2026 (E1 update 25 November). The manuscript is `paper.md` in this directory. It incorporates **three** runs: the 74-draw run (`research/records/2026-11-23-grouping-multiverse/`), the 400-draw run (`research/records/2026-11-23-grouping-multiverse-400/`), and the 1,200-draw extension (`research/records/2026-11-25-e1-multiverse/` @ `7e6f7b5`). No placeholders remain. This record is the paper's public face, so every number in it is traceable to a named results file below.

**Reviewer-facing verdict (honest):** 3.5/5 — a method that finds only five robust links out of 272, and finds that they are the least surprising five, is a method that is working. The paper's strength is methodological (the resolution analysis and the transportability framing), not the substantive payoff; the group-specific labels are hypotheses, not findings. The resolution analysis is reported as a **design rule with an explicit dependence caveat**, not a calibrated test: the 272 links' null series share draws and are neither independent nor uniformly positively dependent, so §6.6 reports a three-way strict-tier range — **0** under the dependence-robust Benjamini–Yekutieli procedure (about 33,650 draws for a lone link), **35** under the nominal independence–PRDS arithmetic (5,440 draws), and **44** under an anti-conservative effective-tests sensitivity (about 3,140) — and a dependence-aware permutation null (zero in 400 pseudo-runs, qualified because the pseudo-runs share draws). The 1,200-draw E1 extension shows the counts are draw-budget-dependent: BH becomes 41/23/20/53, and BY certifies **32 heterogeneity links** at 1,200 (first rank 29) while up/down/sign-flip stay zero; group localisation shows 1 of the 5 robust links and 20 of the 32 BY-certified links are group-concentrated, so "robust" is a share rule, not homogeneity.

**Branch:** `research/methods-multiverse-paper-2026-11-23` (off `research/grouping-multiverse-2026-11-23`). The 400-draw record directory `research/records/2026-11-23-grouping-multiverse-400/` is merged into this branch (from branch `research/grouping-multiverse-400-2026-11-23` @ `1152cec`), and the 1,200-draw E1 record `research/records/2026-11-25-e1-multiverse/` is merged from `research/e1-multiverse-1200-2026-11-25` @ `7e6f7b5`. Every results file cited by the paper is present on this branch, so a reader who clones it can trace every number without switching branches.

## What is in this directory

- `paper.md` — full manuscript: abstract; introduction (Durlauf as named foil); literature review; method; data; results sorted under (1) Fertility and (2) Massification; resolution analysis; relation to prior work; discussion; limitations; reproducibility; target venues; appendices (definitions, grouping inventory, plain-language abstract and five-point summary).
- `README.md` — this file.
- `refs.md` — APA 7th bibliography with per-entry verification status.
- `lit-review.md` — prior-art search and standing assessment (23 Nov 2026): closest work (multiverse, vibration of effects, cross-national multiverse applications, heterogeneity critique), what is genuinely ours vs borrowed, an honest strength score for each result, a use/don't-use checklist for other researchers, and the situating patch (nine verified references; applied in this revision to §2.1 and §2.8 of the paper — see commit 45b2ad5).
- `scripts/verify_refs.py` — Crossref DOI checker used for the bibliography (prints bibliographic fields only).
- `scripts/find_refs.py` — Crossref bibliographic search used to recover DOIs for the entries whose DOI was uncertain.
- `scripts/dependence_analysis.py` — dependence analysis for the resolution rule: correlation structure of the 272 null-share series, Li–Ji effective number of tests, BH certification under an effective-tests sensitivity grid, draws-needed scaling, and a dependence-aware permutation null for the certified count.
- `results/dependence_analysis.json` — the outputs of that script (the numbers cited in paper §6.6).

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
- Dependence analysis (§6.6): mean absolute off-diagonal correlation 0.041 (51% positive / 49% negative, max 0.44); Li–Ji effective tests ≈157 (162 PCs for 90% variance; a proxy-matrix heuristic, anti-conservative); certified 35 at M=272, 44 at M_eff=157, 46/52/60 at M=150/100/50; dependence-aware permutation null of the certified count = 0 in all 400 pseudo-runs (qualified: pseudo-runs share draws) — `results/dependence_analysis.json`; script `scripts/dependence_analysis.py`; input matrix `2026-11-23-grouping-multiverse-400/results/null_shares_TR.csv.gz`.
- Benjamini–Yekutieli dependence-robust procedure (§6.6): H_M = 6.185; first-step threshold 2.97e-5; at the 400-draw p floor a link needs rank ≥ 84 but the floor cluster is 30 (up), 19 (down), 15 (flip), 53 (heterogeneity) — all below 84, so **BY certifies 0 at 400 draws in each of the four strict-tier procedures**; BY draws: lone ≈33,646, cluster-30 ≈1,122, cluster-35 ≈962. **Family definition:** each procedure is a BH over the 272-link family (one trends-specification p-value per link; `analyse400.py` `bh(p_up[J])`, J = 272 values); the up/down/sign-flip/heterogeneity counts are four separate procedures, not one joint 122-test procedure. A hypothetical 68-link per-direction family would give BY=35 with 6,533/218/186 draws, but no 68-link family exists in the committed code — recorded in `results/dependence_analysis.json`, `benjamini_yekutieli.hypothetical_per_direction_68` — `results/dependence_analysis.json`, `benjamini_yekutieli`. Floor-count source: the up floor (30) is recomputed from `null_shares_TR.csv.gz`; the down/flip/het floors (19/15/53) are taken from `2026-11-23-grouping-multiverse-400/results/headline.json` (same `analyse400.py` machinery; those null matrices were not saved), so they are deductions from committed counts, not independent recomputations; the BY = 0 claim rests on the up procedure, where the committed matrix exists.
- **E1 draw-budget ladder (1,200 draws):** BH certifications up/down/sign-flip/heterogeneity = 35/19/15/53 at 400, 41/20/17/53 at 800, **41/23/20/53 at 1,200**; BY = 0 in all four families at R ≤ 800, and at 1,200 BY certifies **32 heterogeneity links** (first BY rank 29; het floor 32) while up/down/sign-flip remain 0 — `2026-11-25-e1-multiverse/results/summary_by_R.json`, `families.<R>.<proc>.certified_BH` / `.certified_BY` / `.first_rank_BY` / `.n_floor`. Sign-flip is the committed "flips more than random" direction; the "flips less" sensitivity certifies 0 at every R (`sensitivity_flip_less_*`).
- **E1 reproduction and split halves:** R=400 counts reproduce the committed headline exactly (35/19/15/53; robust 5/5; per-link share difference ≤ 5e-7), with the declared panel-vintage deviation max |Δt| = 3.97e-5 (`repro400.json`, `panelcheck.json`); 1,200-draw halves: up-p rank correlation 0.9965, BH half-counts 34/38, 21/23, 15/21, 53/51, BY zero in both halves (R=600) so BY Jaccard is 0 by construction (`split_halves.json`); runtime 5,426.8 s on 8 workers, 4.52 s/draw (`run_meta.txt`, `progress.log`).
- **E1 group localisation:** 1 of 5 robust links is group-concentrated (`gdppc_log → urban`: b 2.317, t 3.98, top-5 countries BWA/GNQ/OMN/LBY/LBR carry 22% of summed |Δb|, t 2.47 after removal, relative change in b 0.510); 20 of the 32 BY-certified heterogeneity links are group-concentrated (`group_localisation.json`, `summary.n_robust_group_concentrated` = 1, `summary.n_by_group_concentrated` = 20).

**Provisional / weakest claims (flagged in the paper):**

- **Group-specific labels are the least certain verdicts.** They rest on a smoothed-null test across ~16,600 tag-by-link comparisons; at 400 draws a single tag claim cannot be certified strictly (same floor arithmetic). Treat as descriptions of where a link is concentrated, not certified claims.
- **Single-region and single-class claims** (e.g. farm output → lower-secondary completion in Latin America) are the weakest evidence in the run.
- **The 4 new beats-random links** (wage employment→child mortality, secondary completion→wage employment, female labour participation→secondary completion, birth rate→life expectancy) are new at 400 draws and depend on the normal fit; the t-fit version keeps 2 of them.
- **The strict-tier count is a range (0 / 35 / 44), not a point.** The 272 links' tests are dependent (mean absolute correlation 0.041) and the dependence is not uniformly positive, so BH's PRDS assumption is not established. The dependence-robust Benjamini–Yekutieli procedure certifies **0** at 400 draws (lone-link budget ≈33,650 draws); the nominal independence–PRDS arithmetic certifies **35** (5,440 draws); the anti-conservative effective-tests sensitivity gives **44** (≈3,140 draws) and up to 60 at an arbitrary M=50 anchor. The dependence-aware permutation null certifies 0 in 400 pseudo-runs, a bound qualified because the pseudo-runs share draws. The paper reports the rule as a pre-specified draw-budget/certification-ceiling design conditional on the dependence assumption, with the range explicit. The FDR family is the 272-link family (one trends-specification test per link); the up, down, sign-flip and heterogeneity counts are four separate procedures over that family, not one joint 122-test procedure.
- **The range is draw-budget-dependent, and "robust" is not homogeneous.** At 1,200 draws BY certifies 32 heterogeneity links but zero up/down/sign-flip; BH counts become 41/23/20/53. The split-halves show counts stable (34/38, 21/23, 15/21, 53/51) but BY zero in each half (R=600), so individual BY certification is not stable by construction. Localisation: 1 of 5 robust links is group-concentrated, and 20 of the 32 BY-certified heterogeneity links are group-concentrated — the verdict is a share rule, not a homogeneity claim.
- **The t-fit tier** certifies 42 links against 46 for the normal fit (median fitted df 157; they agree on 42, disagree on 4).
- **Data provenance is a working compilation, not a published dataset.** Per-series sources are carried in the panel metadata but were not re-verified series-by-series for this paper; confirm before submission.

**Not done in this paper (stated as such):**

- No known-truth simulation of the verdict rules' size and power (Section 6.7 lays out the design; the project's simulation branch is the intended home).
- No GPU implementation in the reported runs; all numbers are CPU.
- No causal identification; the paper says plainly the method tests transportability, not identification.

## Plain-words summary of the paper

The paper asks a simple question about a common kind of cross-country claim: a single number from a panel of countries is an average over countries that may not share the relationship at all. It answers by cutting the countries into groups 50 different ways (region, income, birth rate, schooling, farm economy, taxes, data-driven clusters, trajectory classes), rerunning the whole analysis inside every group, and comparing with random cuts of the same sizes. Random cuts are the yardstick for what chance alone produces. Two things follow: the method can tell claims that travel across country types from claims that only hold in some types, and the number of random cuts is a hard ceiling on how strong the evidence can be. In the two applications, two demographic links travel (child mortality and life expectancy to fewer births), no schooling-expansion driver travels, and paid employment is a clean null. The honest limit: 400 random cuts can vouch for a cluster of very strong findings but not for one finding on its own; a lone finding would need about 5,440 cuts (about 3,140 once the overlap among the 272 links is taken into account). And the cluster rule is a design rule with a stated caveat — the 272 links are not independent tests — not a calibrated test. Depending on how cautiously one corrects for that dependence, the strict count at 400 cuts is 0 (most cautious), 35 (standard), or 44 (a correction that can overstate the evidence); the most cautious procedure would need about 33,650 cuts for a lone finding.

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
| dependence: mean |r| 0.041; M_eff ≈157 | `results/dependence_analysis.json` | `dependence.mean_abs_offdiag_r`, `.m_eff_li_ji` |
| certified 35 (M=272) → 44 (M_eff) → 60 (M=50) | `results/dependence_analysis.json` | `certification.certified_by_M` |
| draws 5,440→3,140 (lone); 182→105 (cluster-30) | `results/dependence_analysis.json` | `draws_needed` |
| dependence-aware null: 0 certified in 400 pseudo-runs (qualified) | `results/dependence_analysis.json` | `permutation_null_of_certified_count` |
| E1 BH counts by R: 35/19/15/53 (400), 41/20/17/53 (800), 41/23/20/53 (1200) | `2026-11-25-e1-multiverse/results/summary_by_R.json` | `families.<R>.<proc>.certified_BH` |
| E1 BY at 1,200: het 32 (first rank 29, floor 32); up/down/flip 0 | same | `families.1200.*.certified_BY`, `.first_rank_BY`, `.n_floor` |
| E1 R=400 reproduction: counts exact; share diff ≤5e-7; max |Δt| 3.97e-5 | `.../results/repro400.json`, `panelcheck.json` | `certified_BH_ours/committed`, `max_abs_share_TR_diff`, `max_abs_diff` |
| E1 halves: rank corr 0.9965; BH 34/38, 21/23, 15/21, 53/51; BY 0 both | `.../results/split_halves.json` | `up_p_rank_correlation`, `family_agreement` |
| E1 localisation: 1/5 robust, 20/32 BY links concentrated | `.../results/group_localisation.json` | `summary.n_robust_group_concentrated`, `.n_by_group_concentrated` |
| FDR family: 272 links per procedure (not 68; not one joint 122) | 400 record `scripts/analyse400.py`; `results/dependence_analysis.json` | `bh(p_up[J])`, J = 272 TR p-values; `benjamini_yekutieli.family_size` / `.family_members` |
| BY: H_M 6.185; threshold 2.97e-5; rank ≥84 needed; certified 0 in each of four procedures | `results/dependence_analysis.json` | `benjamini_yekutieli`, `.per_procedure_by_zero` |
| hypothetical 68-link family: BY=35; draws 6,533/218/186 (not the committed family) | `results/dependence_analysis.json` | `benjamini_yekutieli.hypothetical_per_direction_68` |
| BY draws: lone ≈33,646; cluster-30 ≈1,122; cluster-35 ≈962 | `results/dependence_analysis.json` | `benjamini_yekutieli.draws_needed` |

## Report format compliance

- Plain words: the README's summary and the paper's Appendix C contain no variable names and no Greek letters; the technical sections use standard terms for an academic audience.
- The two applications are sorted under "(1) Fertility" and "(2) Massification" in the paper (Sections 5.6 and 5.7).
- For every headline number the paper gives the estimate, the uncertainty (or the resolution caveat), the sample, and the test designed to kill it (the multiverse verdict, the random-grouping null, the split-halves test, the determinism check).
- Nulls are reported prominently: 161 of 272 links are no better than random; paid employment is a clean null; electricity is a weak, group-dependent driver.
- Every file is listed above; provisional numbers are flagged in the "Provisional" section.
