# ERRATUM — Q2 pathways record (25 November 2026)

**Record:** `research/records/2026-11-25-q2-pathways/`.
**Branch:** `research/q2-pathways-2026-11-25` @ `f71b789` (the verified head audited by task-11). This erratum is an
additive commit on that branch; no history rewrite.
**Raised by:** task-11 prose-vs-data audit (`research/prose-data-audit-2026-11-24` @ `ff390fe`,
`research/records/2026-11-24-prose-data-audit/AUDIT.md` §3.1, checks Q2-08…Q2-11); actioned as task-12.
**What is changed:** one marked `CORRECTION` pointer in `REPORT.md`, this file, and a reproduction script + output.
**No table or result file is changed**; the original sentences stay visible.

---

## §A — the random-matching yardstick compares the wrong observed statistic

### Where

`REPORT.md` §4.3 "Random-matching yardstick (descriptive, not a p-value)". Original text (retained; the
`CORRECTION` pointer follows the paragraph):

> 1,000 random disjoint pairings of the same 105 countries (seed 71201; same 52-pair/1-unpaired structure). The
> observed matched pairs are **not unusually divergent**:
> - median absolute schooling gap: observed **0.82 years**; random median **0.825**; share of random draws whose
>   median is at least as large as observed **52.4%** (random 2.5-97.5% range 0.60-1.045);
> - median absolute TFR gap: observed **0.77**; random median **0.773**; share ≥ observed **50.3%**.
>
> In other words, matching on 1980 similarity does **not** produce larger 1990-2010 divergence than random pairing
> in this sample. This is the central honest null of Q2: the pair benchmark describes paths, but it does not show
> that similar starts produce unusually divergent outcomes. Source: `results/audit/audit_random_yardstick.json`.

### What is wrong

`results/audit/audit_random_yardstick.json` stores `observed.median_schooling_gap = 0.8200` and
`observed.median_tfr_gap = 0.7715`, computed by `scripts/q2_audit.py::random_yardstick()` as the median absolute
1990–2010 gap over **all 5,460 unordered pairs** of the 105 baseline-complete countries. Each random draw, by
contrast, computes the median over **its 52 random pairs**. The two statistics are therefore on different pair
sets, and the reported shares (52.4% / 50.3%) compare random 52-pair medians to an all-pairs population median —
not to the matched pairs the paragraph is about. The committed JSON is a self-consistency check of the random
pairing, not a matched-pairs-versus-random comparison.

The matched pairs' own medians are in the committed primary pair table `results/audit/pairs_primary.csv`
(columns `mean_years_schooling_gap`, `tfr_observed_1950plus_gap`):

| statistic | all-pairs median (what the JSON computes) | matched-pair median (what §4.3 claims) |
|---|---|---|
| absolute schooling gap | 0.8200 years | **0.6200 years** |
| absolute TFR gap | 0.7715 | **0.2375** |

Against the matched-pair medians, the share of the 1,000 random draws whose median is at least as large as the
matched-pair median is **96.1%** (schooling: 961/1,000) and **100.0%** (TFR: 1,000/1,000), not 52.4% / 50.3%.
Random-pair medians are 0.825 (schooling) and 0.7728 (TFR), so **the matched pairs are less divergent than random
pairing**, not "not unusually divergent" in the sense the prose implies.

### What survives and what must change

- **Direction survives, and is in fact stronger.** The paper's point is that matching does not produce *more*
  divergence than random pairing; the corrected statistic supports that (matched pairs are *less* divergent).
  The paper must not claim "equally divergent"/"not unusually divergent" — the correct statement is that matched
  pairs are **less** divergent than random pairing.
- **The "central honest null" sentence must be rewritten**, because the committed check compares two different
  observed statistics. The honest null survives as "matching on 1980 similarity did not produce more divergence
  than random pairing — it produced less — so the pair benchmark describes paths rather than showing that similar
  starts produce unusually divergent outcomes."
- The random 2.5–97.5% range 0.60–1.045 is a property of the random draws and remains valid.

### Reproduction

```
python3 scripts/erratum_check_q2_yardstick.py
# -> results/audit/erratum_check_q2_yardstick.json
```

The script reads the committed `data/long_run_panel.csv` and `results/audit/pairs_primary.csv`, re-runs the
committed random yardstick (seed 71201, 1,000 draws, same permutation/pairing logic as
`scripts/q2_audit.py::random_yardstick`) and reproduces both comparisons: 0.524 / 0.503 against the all-pairs
medians (matching the committed JSON exactly) and **0.961 / 1.000** against the matched-pair medians.

### Recommended fix (not applied here)

Either (a) compute the observed statistic on the 52 matched pairs (0.620 / 0.2375) and rerun the shares
(96.1% / 100%) before quoting §4.3, or (b) explicitly define the observed statistic as the all-pairs median of
the 105-country population and delete the matched-pairs framing. The task-11 audit's recommended correction
(REC §6.1) is (a).

### Effect on the papers

None traced. Neither Paper M (`research/paper-massification-2026-11-25` @ `fb9f419`) nor Paper N1
(`research/paper-sequencing-novel-2026-11-25` @ `62c27a3`) quotes the 0.82 / 0.77 / 52.4% / 50.3% statistics;
the Q2 numbers quoted in the paper drafts are the pair-smoke counts and matching-overlap figures, which are
unaffected. No other file in this record repeats the 52.4%/50.3% shares.
