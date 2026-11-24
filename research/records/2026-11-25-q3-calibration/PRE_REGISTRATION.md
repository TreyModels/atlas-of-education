# Pre-registration — Q3 multiverse calibration: known-truth errors and full BH/BY on real families

Branch `research/q3-multiverse-calibration-2026-11-25`, record
`research/records/2026-11-25-q3-calibration/`. This file is committed **before any calibration or
BH/BY run**. It responds to Codex review findings **F07** and **F08** (research/records/2026-11-24-codex-review/REVIEW.md
on branch research/codex-handoff-run-2026-11-24) and to the methods-paper dependence analysis
(`research/methods-multiverse-paper-2026-11-23`, paper §6.6, `results/dependence_analysis.json`).

## What this exercise can and cannot establish (fixed now)
- The calibration is a **design check at the share level**, built on the known-truth simulator
  (`known_truth_sim.py`, Sonnet, branch `research/assessment-and-next-experiments-2026-11-24`). It is
  not the paper's regression engine and does not re-estimate the real panel. Its purpose is to measure
  the operating characteristics of the **actual verdict rule** under known regimes, with Monte Carlo
  intervals and a design-size grid.
- The BH/BY recomputation uses the **real 272-link empirical p-values** from
  `grouping-multiverse-400 @ 1152cec` (`results/edge_table400.csv`, columns `emp_p_up_TR`,
  `emp_p_dn_TR`, `emp_p_flip_le`, `emp_p_Q_up`) — four strict-tier families, 272 links each — not floor
  counts. The 400-draw null array (`results/null_shares_TR.csv.gz`) is used to validate the
  share-based p-values and their exchangeability.
- No result will be described as a validation of the substantive claims; F07's request is a
  descriptive-rule calibration and a full step-up calculation. Failures will be preserved.

## Job 1 — known-truth calibration of the actual verdict rule

**Engine.** Copy of Sonnet's `known_truth_sim.py` (N = 150 countries, T = 50 periods; 4 grouping
families × (2-cut, 3-cut) = 8 groupings, 20 tags; random re-partition null with the same group sizes,
R draws). The paper-rule implementation is retained: ROBUST = whole-sample both specs significant and
same sign, share ≥ 0.5, family-minimum share ≥ 0.25, flip rate ≤ max(0.10, random mean + 0.05);
GROUP = tag-level BH at 5% with a mean-z and share condition; plus a heterogeneity check
(real heterogeneity rate ≤ 95th percentile of the random rate) that splits ROBUST into ROBUST+H and
ROBUST-HET, and a BEATS tier (share-level BH at 5% against the random-draw null). Documented
simplifications: eight groupings not fifty, one link per replicate not 272, no nesting across cuts
beyond the family structure. The calibration therefore bounds the *rule's* behaviour, not the real
pipeline's.

**Regimes (pre-specified).**
| id | regime | truth | interpretation of a good rule |
|---|---|---|---|
| R0 | null | no effect (independent series) | ROBUST/GROUP/BEATS rare (FP) |
| R1 | uniform strong | b = 0.15 for all countries | ROBUST+H common; NONE rare (FN) |
| R2 | uniform strength ladder | b ∈ {0.02, 0.04, 0.06, 0.10, 0.15, 0.25} | power curve |
| R3 | minority-only | b = 0.40 in top third of one latent family | planted tag localised; ROBUST rare (false "everywhere") |
| R4 | shared trend | null + shared country-specific trends (spurious link) | FP rare |
| R5 | sign-split | +0.25 / −0.25 by median of one latent family | BEATS/GROUP behaviour under opposite signs |

**Design.** 400 independent replicate seeds per regime (seed = 20261125 + 1000·rep), R = 400 draws,
α-equivalent 5%. Categories: ROBUST+H, ROBUST-HET, ROBUST-but-GROUP, GROUP, BEATS, NONE. Metrics with
Wilson 95% intervals: false-positive rate (R0, R4), false-negative rate (R1), power curve (R2),
localisation (R3: planted-tag hit rate; share wrongly ROBUST), and category composition for all
regimes.

**Monte Carlo versus mechanism/sample-size uncertainty (separate axes).** MC uncertainty is the Wilson
interval at 400 replicates (half-width ≤ 5 points at p = 0.5; ≤ 2.5 at p = 0.1). Mechanism/sample-size
uncertainty is a **design grid**: for R0, R2 (b = 0.06) and R3, repeat at N ∈ {80, 150, 220} and
T ∈ {30, 50, 60} with 200 replicates per cell, and at R ∈ {100, 400} for R0 and R2(b = 0.06). Rates are
reported per cell; no single cell is treated as the answer. Differences across design cells are
reported as mechanism/sample-size sensitivity, not as MC error.

**Pre-registered adequacy benchmarks (honest pass/fail, not post-hoc).** Null FP ≤ 5% with Wilson
upper bound ≤ 10%; uniform-strong FN (NONE) ≤ 5%; minority planted-tag hit ≥ 80% with false-ROBUST
≤ 10%; shared-trend FP ≤ 5%. Failure of any benchmark is reported as a failure of the rule, and the
verdict wording is adjusted to descriptive.

## Job 2 — validate permutation p-values and full BH/BY on four real families

**Families (fixed).** Four strict-tier families, each 272 links, from the real 400-draw multiverse:
(1) up (`emp_p_up_TR`), (2) down (`emp_p_dn_TR`), (3) sign-flip (`emp_p_flip_le`), (4) heterogeneity
(`emp_p_Q_up`).

**Validation before interpretation (pre-specified).**
- V1 recomputation: recompute p_up and p_dn from the 400-draw null share array and require exact
  agreement with the committed columns (max abs difference < 1e-12; mismatch count 0), else report the
  discrepancy.
- V2 floor/range: p ∈ (0, 1]; count at the floor 1/401 equals the committed ceiling counts; no
  NaN/infinite.
- V3 marginal uniformity: for links not claiming superiority (p > 0.05 in the up family; p > 0.05 in
  the other families), test uniformity of p with a KS test; report the statistic, p, and the fraction
  of p ≤ 0.05 (expected ≈ 5%).
- V4 exchangeability of draws: split the 400 draws into four blocks of 100 and, for every link, test
  equality of block means by permutation (10,000 permutations); report the share of links with p <
  0.05 (expected 5%) and a global summary. Also report the rank correlation between draw index and the
  across-link mean null share (expected ≈ 0).
- V5 validity limitation: the 400-draw array covers the share statistics only. The flip and
  heterogeneity p-values cannot be recomputed from draws; they are used **as committed** and labelled
  "committed-p only" wherever they matter.

**Step-up computation.** Run the Codex `fdr_check.py` (copied, unmodified, on valid complete
families; CSV columns family,link,p, 272 rows per family, unique links, finite p) with q = 0.05 to get
BH and BY per family. Independently recompute BH and BY in the analysis script; require the two agree
exactly. Then reproduce the "0/35/44" story: BY count over the 272-link up family (expect 0); BH over
272 (expect 35); BH using the effective number of tests m_eff = 157 from the dependence analysis
(expect 44). Record whether the story changes for each of the four families, and report BY counts for
down, flip and heterogeneity families (no prior expectation; report as computed).

**Decision rule (fixed).** "The 0/35/44 story changes" if and only if the full-vector recomputation
disagrees with the committed counts (up 35, down 19, flip 15, heterogeneity 53; BY 0; BH at m_eff 157 =
44) beyond floating-point identity. Otherwise the story is unchanged, and this is reported with the
validation status (V1–V4) attached. If any validation fails, the BH/BY counts are reported as
conditional on invalid p-values and no claim about FDR control is made.

## Data and reproducibility
- Real p-values: `grouping-multiverse-400 @ 1152cec` → `results/edge_table400.csv`,
  `results/null_shares_TR.csv.gz`, `results/headline.json` (committed counts), `results/summary400.txt`.
- Dependence analysis: `methods-multiverse-paper-2026-11-23` → `results/dependence_analysis.json`
  (m_eff = 157, H_M = 6.1849, BY = 0, BH by M table).
- Codex checker: `research/codex-handoff-run-2026-11-24` → `research/records/2026-11-24-codex-handoff/scripts/fdr_check.py`
  (copied unmodified; SHA256 recorded).
- Simulator: `research/assessment-and-next-experiments-2026-11-24` →
  `research/records/2026-11-24-assessment-and-next-experiments/scripts/known_truth_sim.py` (copied;
  SHA256 recorded; modifications limited to: independent per-replicate seeds, BEATS tier, the strength
  ladder, the design grid and Wilson intervals — all documented in the report).
- Compute: box3 (`ssh autodl3`, repo `/root/work/repo`), single process, thread caps on. No heavy
  regression is run; the share-level simulation is CPU-light. All failures and crashed runs are kept.
