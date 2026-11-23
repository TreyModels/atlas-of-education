# Methods paper §6.6 — second-round stress test (head 2fb55c6)

`novelty-review`, 24 November 2026. Re-read of `research/methods-multiverse-paper-2026-11-23` @ 2fb55c6,
paper.md §6.2-§6.7, `scripts/dependence_analysis.py`, `results/dependence_analysis.json`.

## H1-H6: correctly addressed

- **H1 (BY applied)**: H_M = 6.1849 at M = 272; first-step threshold 2.97e-5; floor 2.49e-3; rank ≥ 84 at the
  floor; BY draws lone ≈33,650, cluster-30 ≈1,120, cluster-35 ≈960 — all match my computation (rounding ±1).
  "Robust in every case" is gone; the range 0 / 35 / 44 is stated. Correct **for a joint 272-link family** (see H7).
- **H2**: M_eff now labelled "heuristic directional sensitivity, not a bound … anti-conservative, justified only
  if the dependence is effectively positive" — exactly right.
- **H3**: Li–Ji labelled a heuristic on a proxy matrix; M = 50 called an arbitrary lower anchor. Correct.
- **H4**: rule-of-three qualified (pseudo-runs share the 400 draws, n_eff < 400, bound not calibrated; block /
  permutation FDR named). Correct.
- **H5**: §6.7 quotes 5,440 nominal, 3,140 effective, 33,650 BY (6.2×), 86 h CPU (33,650 × 9.2 s = 86.0 h —
  arithmetic checks). Correct.
- **H6**: 13,800-partition / 342-link battery has a named check (BY or block/permutation FDR on its 342 links;
  transports descriptive until run). Correct.

So the revision is honest and complete on the six points. But the BY application exposes a **seventh hole**: the
FDR *family* is never defined, and the answer to "how many links does BY certify" depends on it.

## H7 (new, decision-relevant): which family is BY correcting over? 272 links or 68?

§6.2 says "over M = 272 links" — joint family. §6.3/§6.5 then say "the strict tier certifies **35 up links, 19
down links, 15 sign-flip links, and 53 heterogeneity links**" (total 122), and §6.6 says the strict tier has "30 up
links at the floor (and 19 down, 15 sign-flip and 53 heterogeneity links — all below 84)". These cannot all be
certifications of one BH procedure over 272 tests: the script's `certification` block has `certified_baseline = 35`
and `n_at_floor = 30` over the joint 272-link p-vector, while 30 + 19 + 15 + 53 = 117. Three readings, with
different answers:

| Reading | M | H_M | BY at 400 draws | BY draws (lone / cluster-30 / cluster-35) |
|---|---|---|---|---|
| (a) Joint family, 272 links, 30 at floor (the script) | 272 | 6.185 | **0** (floor rank 30 < 84) | 33,650 / 1,120 / 960 |
| (b) Per-direction family, 68 links (the "35 up" reading) | 68 | **4.804** | **35** — BY threshold at rank 35 = 35·0.05/(68·4.804) = **0.00536**, above the rank-35 p = 0.00499 | **6,533 / 218 / 186** |
| (c) Joint family with all four floor clusters (if 117 links are at the floor) | 272 | 6.185 | **≥117** — rank 117 threshold 117·2.97e-5 = 0.00348 > floor 0.00249 | — |

So the headline "BY certifies zero" holds only under reading (a), and only if the 19 / 15 / 53 are **not** strict-tier
BH certifications but results of their own direction-specific procedures. Under reading (b) — which is what "35 up
links" suggests — BY certifies the whole 35-link cluster, not zero, and the BY draw budget is 6,533 rather than
33,650. Under reading (c) BY certifies the floor cluster. Also note that under (b) a rank ≥ 84 is impossible by
construction (the family has 68 links), which is a tell that the "rank 84" arithmetic is being applied to a family
of the wrong size.

**Fix:** state the family explicitly in §6.2 and §6.6 — either "all 272 links joint" (then reword §6.3/§6.5 so the
19/15/53 are labelled as separate direction-specific procedures, not as the same BH, and keep BY = 0) or
"per-direction families of 68" (then recompute with H_68 = 4.804; BY = 35; draws 6,533/218/186; and the "0"
headline must go). The reviewer will test which one the code actually does; answer that in the text and the
numbers can be trusted either way.

## Minor

- BY cluster-35 draws: paper says ≈960, exact is 961-962 depending on ceil convention; "about" is fine.
- §6.6's "all below 84" parenthetical should be deleted under reading (a): rank 84 is not a meaningful rank for a
  direction-specific cluster in a 272-link family when only 30 links are at the floor.

## Verdict

H1-H6 are properly addressed. H7 is the remaining decision-relevant inconsistency — it does not undermine the
downgrade (the paper already says "conditional on the dependence assumption"), but it makes the specific number in
the three-way range ambiguous, and a referee who reads §6.2 (M=272) and §6.3 (35 up/19 down/15 flip/53 het) together
will ask this exact question. Fix H7 and the dependence section is defensible.
