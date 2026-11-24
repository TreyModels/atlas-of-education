# Q3 — When does the grouping multiverse get fooled? Known-truth calibration and full BH/BY on the real families

Branch `research/q3-multiverse-calibration-2026-11-25`. Record `research/records/2026-11-25-q3-calibration/`.
Pre-registration committed **before any run**: commit **15b6c64** (`PRE_REGISTRATION.md`). This report
responds to Codex review **F07** and **F08** (`research/records/2026-11-24-codex-review/REVIEW.md`,
branch `research/codex-handoff-run-2026-11-24`) and to the methods-paper dependence analysis
(`research/methods-multiverse-paper-2026-11-23`, §6.6, `results/dependence_analysis.json`). Box3 was
used for computation (`/root/work/q3`, single process, thread caps). No regression engine was rerun.

## Bottom line (restrained)

1. **The verdict rule controls false positives well.** In a known-null world it calls a link ROBUST,
   GROUP or BEATS in **4.2%** of replicates (95% CI 2.7–6.7); with shared country trends and no
   effect, **5.0%** (3.3–7.6). It detects a strong uniform effect (b = 0.15) with a **2.5%**
   false-negative rate. These pass the pre-registered benchmarks.
2. **It fails the two benchmarks that matter for the minority-effect complaint.** When the true effect
   lives in only one third of countries, the rule still calls the link robust **87%** of the time
   (ROBUST+H 48.2% + ROBUST-but-GROUP 38.8%) while flagging the planted group in only **42.0%** of
   replicates (95% CI 37.3–46.9). "Robust everywhere" is therefore **not** a homogeneous-effect
   certificate; it is a descriptive label that a minority effect wins about half the time. This
   confirms, with independent seeds and intervals, what F07/F08 reported from the exploratory run.
3. **The real-family step-up story does not change under the full vector.** Recomputing BH and BY from
   the full sorted 272-link p-value vector gives BH = **35 up, 19 down, 15 sign-flip, 53
   heterogeneity** — exactly the committed counts — and BY = **0 for every family**. The "0/35/44"
   story is unchanged: 0 under dependence-robust BY, 35 under BH over 272, 44 under BH with the
   effective-test approximation m_eff = 157. The unmodified Codex `fdr_check.py` agrees exactly.
4. **Exchangeability/permutation validity checks pass; exact p-value recomputation does not, for a
   documented data-management reason** (the committed null array is stored rounded to 4 significant
   digits). Details below.

## Job 1 — known-truth calibration of the actual verdict rule

**Engine.** A copy of the known-truth simulator from `research/assessment-and-next-experiments-2026-11-24`
(`scripts/known_truth_sim_orig.py`, SHA256 in `inputs/SHA256SUMS.txt`), extended in
`scripts/calibrate.py` with: independent seeds per replicate, a BEATS tier so all four verdict
categories are represented, a strength ladder, the design-size grid, Wilson intervals, and vectorised
random-partition statistics. The vectorised statistics were validated against the original loop
implementation (self-test passes: group-t max difference 2.7e-15, heterogeneity 1.9e-15). The
self-test failed twice before that — once from a permutation convention, once from passing the t-ratio
into the heterogeneity statistic — and the fixes are in the script history; the failure sequence is
preserved in `results/` (see "Failures preserved").

**Design (pre-registered).** N = 150 countries, T = 50 periods; 4 grouping families × (2-cut, 3-cut)
= 8 groupings, 20 tags; 400 random re-partitions per replicate; 400 independent replicate seeds per
regime (seed = 20261125 + 1000·rep); α-equivalent 5%. The paper-rule implementation is the simulator's:
ROBUST = whole-sample both specifications significant and same sign, share ≥ 0.5, family-minimum
share ≥ 0.25, flip rate ≤ max(0.10, random mean + 0.05); heterogeneity split into ROBUST+H and
ROBUST-HET; GROUP = tag-level BH at 5% with mean-z and share conditions; BEATS = share-level BH at 5%
against the random-draw null. **Simplifications stated plainly:** eight groupings not fifty, one link
per replicate not 272, no nesting beyond the family structure. This calibrates the *rule*, not the
real pipeline.

### Table 1. Main regimes (400 replicates each, R = 400 draws); rates with Wilson 95% intervals

| regime | ROBUST+H | ROBUST-HET | ROBUST-but-GROUP | GROUP | BEATS | NONE | key error rate |
|---|---|---|---|---|---|---|---|
| R0 null | 0.0% [0.0, 1.0] | 0.0% [0.0, 1.0] | 0.0% [0.0, 1.0] | 0.2% [0.0, 1.4] | 4.0% [2.5, 6.4] | 95.8% [93.3, 97.3] | false-positive **4.2%** [2.7, 6.7] |
| R1 uniform strong (b = 0.15) | 95.5% [93.0, 97.1] | 1.0% [0.4, 2.5] | 1.0% [0.4, 2.5] | 0.0% [0.0, 1.0] | 0.0% [0.0, 1.0] | 2.5% [1.4, 4.5] | false-negative **2.5%** [1.4, 4.5] |
| R3 minority-only (b = 0.40, top third) | 48.2% [43.4, 53.1] | 0.0% [0.0, 1.0] | 38.8% [34.1, 43.6] | 3.2% [1.9, 5.5] | 0.0% [0.0, 1.0] | 9.8% [7.2, 13.1] | planted tag flagged **42.0%** [37.3, 46.9]; false-ROBUST (strict ROBUST+H) **48.2%** [43.4, 53.1]; any-robust 87.0% |
| R4 shared country trends, no effect | 0.2% [0.0, 1.4] | 0.0% [0.0, 1.0] | 0.0% [0.0, 1.0] | 1.8% [0.9, 3.6] | 3.0% [1.7, 5.2] | 95.0% [92.4, 96.7] | false-positive **5.0%** [3.3, 7.6] |
| R5 sign-split (+0.25 / −0.25) | 0.0% [0.0, 1.0] | 0.0% [0.0, 1.0] | 0.0% [0.0, 1.0] | 3.2% [1.9, 5.5] | 64.5% [59.7, 69.0] | 32.2% [27.9, 37.0] | no robust; BEATS is the dominant (correct) label |

Reading: null and shared-trend regimes behave; a strong uniform effect is almost always found; a
sign-split is never called robust (good) and is mostly labelled BEATS. The minority-only regime is the
failure mode: about half the replicates are called "robust everywhere" when the effect is present in
only one third of countries, and the planted group is localised in under half.

### Table 2. Uniform-effect strength ladder (400 replicates per strength)

| b per country | ROBUST+H (strict) [95% CI] | any-robust (ROBUST+H + ROBUST-but-GROUP) [95% CI] | NONE (false negative) [95% CI] |
|---|---|---|---|
| 0.02 | 0.2% [0.0, 1.4] | 0.2% [0.0, 1.4] | 97.2% [95.1, 98.5] |
| 0.04 | 3.8% [2.3, 6.1] | 3.8% [2.3, 6.1] | 93.5% [90.6, 95.5] |
| 0.06 | **19.0%** [15.5, 23.1] | 19.2% [15.7, 23.4] | 78.5% [74.2, 82.2] |
| 0.10 | **60.0%** [55.1, 64.7] | 60.5% [55.6, 65.2] | 37.2% [32.7, 42.1] |
| 0.15 | **95.0%** [92.4, 96.7] | 95.8% [93.3, 97.3] | 3.0% [1.7, 5.2] |
| 0.25 | 97.5% [95.5, 98.6] | 98.5% [96.8, 99.3] | 0.0% [0.0, 1.0] |

Source of each power-ladder figure (canonical file `results/calibration.json`, the committed run):
strict ROBUST+H = `strength_ladder[b].ROBUST+H_rate`; any-robust =
`strength_ladder[b].correct_robust_rate` (adds the ROBUST-but-GROUP category); false negative =
`strength_ladder[b].false_negative_rate`. The earlier draft quoted only the any-robust field; both
are shown here because the difference (19.0 versus 19.2, 60.0 versus 60.5, 95.0 versus 95.8) is the
small ROBUST-but-GROUP category, not a different seed or run.

The rule needs a per-country effect of roughly 0.10–0.15 for acceptable power at N = 150, T = 50;
effects below 0.06 are mostly missed. This is the power boundary the paper should quote next to any
"robust" verdict.

### Table 3. Design-size grid (200 replicates per cell) — mechanism/sample-size uncertainty, separate from the Monte Carlo intervals above

| regime | N | T | R | key rate [95% CI] |
|---|---|---|---|---|
| C null | 80 | 50 | 400 | FP 3.0% [1.4, 6.4] |
| C null | 150 | 30 | 400 | FP 4.0% [2.0, 7.7] |
| C null | 150 | 50 | 400 | FP 2.0% [0.8, 5.0] |
| C null | 150 | 60 | 400 | FP 4.5% [2.4, 8.3] |
| C null | 220 | 50 | 400 | FP 5.0% [2.7, 9.0] |
| U uniform (b = 0.06) | 80 | 50 | 400 | any-robust 3.0% [1.4, 6.4] (strict ROBUST+H 3.0%) |
| U uniform (b = 0.06) | 150 | 30 | 400 | any-robust 10.5% [7.0, 15.5] (strict ROBUST+H 10.5%) |
| U uniform (b = 0.06) | 150 | 50 | 400 | any-robust 11.0% [7.4, 16.1] (strict ROBUST+H 11.0%) |
| U uniform (b = 0.06) | 150 | 60 | 400 | any-robust 11.0% [7.4, 16.1] (strict ROBUST+H 11.0%) |
| U uniform (b = 0.06) | 220 | 50 | 400 | any-robust 28.0% [22.2, 34.6] (strict ROBUST+H 28.0%) |
| B minority | 80 | 50 | 400 | tag hit 37.5% [31.1, 44.4]; false-ROBUST combined 27.5% (strict ROBUST+H 26.5%) |
| B minority | 150 | 30 | 400 | tag hit 54.5% [47.6, 61.3]; false-ROBUST combined 38.5% (strict ROBUST+H 38.5%) |
| B minority | 150 | 50 | 400 | tag hit 38.0% [31.6, 44.9]; false-ROBUST combined 52.0% (strict ROBUST+H 52.0%) |
| B minority | 150 | 60 | 400 | tag hit 40.0% [33.5, 46.9]; false-ROBUST combined 38.0% (strict ROBUST+H 38.0%) |
| B minority | 220 | 50 | 400 | tag hit 42.0% [35.4, 48.9]; false-ROBUST combined 55.5% (strict ROBUST+H 55.5%) |

Source: `results/calibration.json` → `design_grid[cell].ROBUST+H_rate` (strict),
`.correct_robust_rate` (any-robust), `.false_robust_everywhere_rate` (combined ROBUST+H + ROBUST-HET),
`.planted_tag_flagged_rate`.

Two design-size results deserve emphasis. First, for the uniform weak effect (b = 0.06) power ranges
from 3% at N = 80 to 28% at N = 220: **the same rule is underpowered in small samples and still not
well powered in moderate ones**. Second, for the minority regime, false-ROBUST rises with N
(combined 27.5% / strict ROBUST+H 26.5% at N = 80, rising to 55.5% at N = 220): with more countries the minority effect becomes significant in enough groups to pass
the share rule while the other groups stay null, so **more data make the "everywhere" mislabel worse,
not better**. This is the calibration answer to "does it just travel everywhere".

### Table 4. Draw-count axis (200 replicates per cell)

| regime | R | key rate [95% CI] |
|---|---|---|
| C null | 100 | FP 1.5% [0.5, 4.3] |
| C null | 400 | FP 3.0% [1.4, 6.4] |
| U uniform (b = 0.06) | 100 | correct ROBUST 9.0% [5.8, 13.8] |
| U uniform (b = 0.06) | 400 | correct ROBUST 13.0% [9.0, 18.4] |

R = 100 versus 400 changes the verdict rates by a few points, within/near the Monte Carlo intervals;
the R = 1,200 question is explicitly out of scope here (task-46).

### Pre-registered adequacy benchmarks

| benchmark | observed | passed |
|---|---|---|
| null FP ≤ 5% with upper CI ≤ 10% | 4.2% [2.7, 6.7] | **PASS** |
| uniform-strong FN (NONE) ≤ 5% | 2.5% [1.4, 4.5] | **PASS** |
| minority planted-tag hit ≥ 80% | 42.0% [37.3, 46.9] | **FAIL** |
| minority false-ROBUST ≤ 10% | 48.2% [43.4, 53.1] | **FAIL** |
| shared-trend FP ≤ 5% | 5.0% [3.3, 7.6] | **PASS** |

**Verdict on job 1.** The rule is a good null controller and a poor homogeneity/localisation detector.
The paper must describe "robust everywhere" as a **descriptive significance-share label**, not as
evidence that an effect is the same in every kind of country. This is exactly F07's requested
correction, now with independent seeds, intervals, a power curve and a design-size grid.

## Job 2 — permutation validity and full-vector BH/BY on the four real families

**Inputs (committed).** `inputs/edge_table400.csv` and `inputs/null_shares_TR.csv.gz` from
`grouping-multiverse-400 @ 1152cec` (`results/edge_table400.csv`, `results/null_shares_TR.csv.gz`),
`inputs/dependence_analysis.json` from `methods-multiverse-paper-2026-11-23` (`results/dependence_analysis.json`),
and the unmodified `scripts/fdr_check.py` from `codex-handoff-run-2026-11-24`
(`research/records/2026-11-24-codex-handoff/scripts/`). SHA256 checksums are in
`inputs/SHA256SUMS.txt`; nothing was reconstructed silently.

**Families (fixed by the dependence analysis).** Four separate strict-tier procedures, each over the
same 272-link family: up (`emp_p_up_TR`), down (`emp_p_dn_TR`), sign-flip (`emp_p_flip_le`),
heterogeneity (`emp_p_Q_up`). `fdr_check.py` was run only on complete families: 272 rows per family,
unique links, finite p in [0,1] (it rejects otherwise; it accepted all four).

### Validation before interpretation

| check | result | status |
|---|---|---|
| V1 exact p recomputation from the 400-draw null array | **not exact**: committed null shares are rounded to 4 significant digits, so p counts can differ by a draw. Up: 267/272 links within one draw count, max 9 draws; down: 271/272 within one draw, max 2. | **partial** — explained limitation, not silent |
| V2 floor/range/completeness | all p finite and in (0,1]; floor 1/401 = 0.00249377; links at floor: up 30, down 19, sign-flip 15, heterogeneity 39 (matching the committed ceiling counts) | **pass** |
| V3b permutation validity, leave-one-out null calibration | for each of 400 draws and 272 links, p = (1+#{other draws ≥ this draw})/400; n = 108,800; KS 0.0061 (p = 0.0005 at this n), share ≤ 0.05 = **4.98%** [4.86, 5.12] | **pass** (KS rejection is a large-n artefact; effect size 0.006) |
| V3a real-data marginal distribution (descriptive) | up family: 7.7% of links have p = 1; not a validity test (real links need not be null; links whose real share is at or below every draw get p = 1 by construction) | **descriptive only** |
| V4 exchangeability across draws | four blocks of 100; block-ANOVA p < 0.05 in **4.4%** of links (95% CI 2.5–7.6); KS of the 272 block p-values 0.059 (p = 0.29); Spearman draw index vs mean share 0.028 (p = 0.58); block means 0.13861 / 0.13849 / 0.13863 / 0.13872 | **pass** |
| V5 flip and heterogeneity p-values | the saved 400-draw array contains only share statistics; flip/heterogeneity p-values **cannot be recomputed from draws**. They are used **as committed** and labelled committed-p only. | **unverifiable** |

**What remains unverifiable, plainly.** (i) The committed null array is rounded to four significant
digits, so the exact empirical p-values cannot be re-derived; the recomputation agrees to within about
one draw count for 267/272 (up) and 271/272 (down) links, and we did not reconstruct the raw array.
(ii) The sign-flip and heterogeneity families have no saved null draws; their p-values are committed
values only. (iii) The calibration is a share-level simulation with eight groupings and one link, not
the real 50-grouping / 272-link pipeline.

### Table 5. Full sorted-vector BH and BY, four strict-tier families (272 links each, q = 0.05)

| family | BH (m = 272) | BY (m = 272, H = 6.1849) | BH at m_eff = 157 (approximation, not a procedure) | min p | links at floor |
|---|---|---|---|---|---|
| up | **35** | **0** | **44** | 0.00249 | 30 |
| down | **19** | **0** | 28 | 0.00249 | 19 |
| sign-flip | **15** | **0** | 27 | 0.00249 | 15 |
| heterogeneity | **53** | **0** | 56 | 0.00249 | 39 |

Independent check: the unmodified `fdr_check.py` output (`results/fdr_check_output.csv`) agrees
exactly with the in-script step-up for all four families (BH and BY counts identical). The cross-check
CSV is committed (`results/families_for_fdr_check.csv`).

**Does the 0/35/44 story change? No.** The full-vector computation reproduces the committed counts
(35/19/15/53 up/down/flip/het), reproduces 0 under dependence-robust BY for every family, and
reproduces 44 for the up family under the effective-test approximation m_eff = 157. The story is
therefore: **BH over 272 links certifies 35 up links; the dependence-robust BY bound certifies none;
the 44 figure is an approximation using an effective number of tests, not a procedure with an FDR
guarantee.** The committed counts were not floor-count artefacts.

**Cross-reference — what changes at 1,200 draws (E1, task-46; outside Q3's scope).** The same four
families were recomputed at 1,200 draws in `research/records/2026-11-25-e1-multiverse/` @ `7e6f7b5`
(field source: `results/summary_by_R.json` → `families.<R>.<proc>.certified_BH` / `.certified_BY` /
`.first_rank_BY` / `.n_floor`). The BH counts move with the draw budget: up 35 → **41**, down 19 →
**23**, sign-flip 15 → **20**, heterogeneity 53 → **53**. BY stays 0 for up, down and sign-flip at
1,200, but the heterogeneity family flips: BY certifies **32 heterogeneity links** at 1,200 (first BY
rank 29; 32 links at the floor), where it certifies 0 at 400. So "BY = 0" is a property of the
400-draw budget, not a universal property of the strict tier: at 400 no family has enough
floor/ceiling mass to clear the dependence-robust threshold, while by 1,200 the heterogeneity family
does. Q3 itself did not run 1,200 draws (explicitly deferred to task-46); this paragraph is a
cross-reference, and the E1 numbers come from that record's committed field, not from Q3.

## What the multiverse can and cannot claim (restrained)

- **Can claim:** with a known null or shared-trend null, the rule's false-positive rate is about 5%;
  it does not systematically manufacture robust verdicts from nothing. Strong uniform effects
  (b ≥ 0.15) are found ~96% of the time.
- **Cannot claim:** that "robust everywhere" identifies homogeneous effects. A minority-only effect is
  labelled robust in 87% of replicates and the planted group is localised in 42%; false-ROBUST rises
  with sample size. The label is a descriptive share rule, not a homogeneity test.
- **Cannot claim:** that the strict-tier FDR story survives a dependence-robust procedure. It does not:
  BH gives 35, BY gives 0. The multiverse can present BH numbers with an explicit dependence caveat;
  it cannot present BY-zero evidence as certified links.
- **Power boundary:** the rule's sensitivity for a uniform effect requires per-country effects around
  0.10–0.15; smaller effects are mostly missed, and this should be quoted with the verdict.

## Failures preserved and reproduction

- The calibration self-test failed twice before passing (permutation-convention mismatch; a t-ratio
  passed into the heterogeneity statistic). The fixed script passes at 2.7e-15 (group t) and 1.9e-15
  (heterogeneity). A quick smoke run (`results/calibration_quick.json`, `--quick`) was run before the
  full run; it is kept as evidence of the path, not used in the tables.
- Full run: `results/calibration.json`, log `results/calibrate.log`; BH/BY: `results/bhby.json`,
  `results/bhby.txt`, `results/fdr_check_output.csv`; tables regenerated by `scripts/make_tables.py`
  into `results/tables.md`; benchmarks in `results/benchmarks.json`.
- Reproduction commands (box3, single process, thread caps):
  `python scripts/calibrate.py --selftest`; `python scripts/calibrate.py --out results/calibration.json`;
  `python scripts/bhby.py`; `python scripts/make_tables.py`.
- No secrets in any committed file. No branch rewrites; history is append-only.

## Files

`PRE_REGISTRATION.md` (commit 15b6c64); `scripts/calibrate.py`, `scripts/bhby.py`,
`scripts/make_tables.py`, `scripts/fdr_check.py` (unmodified Codex checker),
`scripts/known_truth_sim_orig.py` (unmodified Sonnet simulator); `inputs/` (four source files +
`SHA256SUMS.txt`); `results/` (calibration JSON/log, BH/BY JSON/text, fdr_check output, family CSV,
tables, benchmarks, quick smoke run); this `REPORT.md`.
