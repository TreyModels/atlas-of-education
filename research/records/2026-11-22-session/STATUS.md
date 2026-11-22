# STATUS — what in this record can be trusted

**Read this before citing anything from this folder.**

Every result in `results/` carries a tier below. Tiers were assigned *after* the
work, some of it retroactively, because several early runs turned out to be broken
or superseded. Nothing here has been cleaned up to look better than it is.

| Tier | Meaning |
|---|---|
| **A — SOLID** | Survived a test designed to break it, or is a computed fact rather than a claim. Cite freely. |
| **B — FRAGILE** | Real in the specification reported, but sensitive to analyst choices. Cite **only with the caveat stated here.** |
| **C — NULL** | Tested and failed. Publishable as a negative result. Do not cite as evidence for the hypothesis. |
| **D — DO NOT CITE** | Superseded, broken, or produced no valid output. Kept for provenance only. |

---

## Tier A — solid

### `results/luck_test_20000.txt`
The schooling–fertility association is not an artefact of chance. Observed 11.97% of
within-country variation explained; across 20,000 simulated worlds in which each
country's education series was time-shifted (destroying the link but keeping the
country, the years, and the shape of the series), the **maximum was 4.57%** and
**none of 20,000 reached the observed value**. Survives measurement error up to
about 40% (20% noise → 9.1%; 40% → 5.3%; 60% → 3.1%).

### `results/exp1b_chain_vs_common_cause.txt`
At the reported specification, a symmetric common modernisation factor **cannot**
produce the observed wage-employment coefficient. 1,200 simulated panels per world;
common-cause median 0.000 (5–95%: −0.260 to +0.255); observed +1.425; **zero of
1,200 panels reached it.**

**Caveat that belongs with this tier:** the simulation was run at the specification
where the coefficient is *largest*. It establishes direction conditional on that
specification. It does not establish that the specification is the right one — see
`spec_curve_1536.txt`, which demotes the finding overall.

### `results/spec_curve_1536.txt`
The audit. 1,536 defensible specifications. Median ≈ 0; 5–95% range −0.040 to
+1.371; significant and positive in **27.9%**. Leave-one-country-out across 203
drops stays positive in **100%** (range +0.83 Turkey to +1.22 North Macedonia).

This is Tier A as a *finding about fragility*. It is the reason the wage result is
downgraded to Tier B.

### `results/replication_and_crossers.txt`
Descriptive accounting, not a causal claim. 111 countries fell below 2.1 births per
woman; profiles at 20/10/5 years before crossing; 8 countries that crossed while
still poor. Correctly computed. Any causal reading of it would be wrong, and the
file does not support one.

---

## Tier B — fragile, cite only with the caveat

### Wage employment → tertiary enrolment, **+1.43 (±0.41)**
**CAVEAT: the signal appears in only 27.9% of defensible specifications.** It is
strongest at lag 0 with no controls and a level outcome; it is **0.00 at lag 10**,
and **0.00 under a log transform**, and adding any control beyond the country's own
starting level takes the median across specifications from +0.12 to +0.01.

Correct statement: *"The association is positive and survives a common-cause
falsification at its strongest specification, but it is not robust across
specifications; most defensible specifications return zero."*

Do **not** write "wage employment leads higher education" without that sentence.

### Electricity → lower-secondary completion, **+16.05**
**CAVEAT: this has not been through the specification curve.** It comes from a
single within-country specification in the repo's `tight/` analysis, plus a
posterior inclusion probability of 1.00 from one Bayesian model averaging run.
Given that the wage result collapsed under the same scrutiny, **treat this as
untested until the curve is run on it.** That is the first job next session.

### Early marriage → slower lower-secondary growth, **−0.116 (±0.044)**
Single specification, 1,130 observations, 113 countries. Survives its own control
set but has not been through a specification curve. Tier B by default.

### `results/absorption_decomposition.txt`
The tertiary→secondary edge (+0.106) shrinks to +0.035 when cities enter. One
decomposition, one control order family. The direction is plausible and consistent
with the collinearity (r = 0.69–0.80 among electricity, cities, paid employment),
but it rests on a single design.

### `results/exp2_driver_battery.txt`
Ranking of drivers against a simulated common-cause noise band of ±1.2. The band
comes from a simulated world, not from theory; the ranking is therefore only as
good as that simulation, whose chain arm was calibrated 3–5× too strong.

### `results/roads_marriage_controls.txt`
Roads are unusable — 47 countries, one decade — and cannot support inference.
The marriage column is Tier B (above). Income appears as `0.0000` because it is
measured in dollars against percentage-point outcomes; **scale it to thousands
before reporting or it will look like a coding error.**

### `results/cluster_levels.txt`, `results/five_groupings.txt`, `results/massification_matrices.txt`
Exploratory groupings. **Cluster separation scores are 0.21–0.26**, which is below
the level at which one can call these natural types. They are cuts through a
continuum. The group-specific coefficients rest on small cells and were not
specification-tested. Use for hypothesis generation only.

---

## Tier C — null results

| Result | What was tested | Outcome |
|---|---|---|
| Gender parity in tertiary education | Women:men tertiary ratio against fertility and against enrolment growth | **Nothing, in every test.** Zero in six groupings, zero in the matrix, zero in Bayesian averaging. Consistent with the ratio being mechanically saturated at high enrolment. It appears never to have been estimated before, so this is a first test. |
| Three-condition takeoff conjunction | Household means × employer demand × state capacity jointly required | **Fails.** Only 38% of 39 takeoffs had all three; additive model beats joint model out of sample (0.1222 vs 0.1225); state capacity null to negative (−0.18, SE 0.20). |
| Farm decline → fertility | Agricultural employment share predicting the birth fall | **Direction reversed.** Farm share → births +0.0011 (SE 0.0041); **births → farm share +1.536 (0.406)**. Fertility leads. Farm share is the weakest term in a seven-variable horse race. |
| World food prices × farm dependence | FAO index 1990–2018 interacted with baseline farm share | Significant everywhere but **the sign is wrong** for the import-competition story (rising prices accelerate exit and fertility decline), and the window begins after most of the world's farm transition ended. |
| 20% fertility threshold | Event study around crossing 20% tertiary | **No break**, at any lag. A straight line across the whole window, consistent with Bongaarts & Watkins (1996) finding no fixed threshold. |
| Tertiary "push" on lower levels | Higher ed predicting growth in primary/secondary | **Absorbed by cities** (+0.106 → +0.035). |

---

## Tier D — do not cite

| File | Why |
|---|---|
| `scripts/spec_curve.py` (first version) | Rebuilt the panel inside every one of 24,576 specifications. Timed out twice, produced no output. Superseded by `spec_curve_final.py`. |
| `scripts/group_matrices.py` | Nested process pools; crashed before producing output. |
| `scripts/group_matrices2.py` | Indexing bug — used country codes as panel-row indices. Its first run silently returned **zero pairs for every group**. Superseded by `group_matrices3.py`. |
| `scripts/exp1.py` | The first chain simulator did not actually embed the chain (higher education responded to the *level* of wages contemporaneously, so controlling for its own level absorbed everything). It reported a null for the chain world, which was a bug, not a finding. Superseded by `exp1b.py`. |
| `scripts/run2.py` | Fixed-effects matrix was concatenated with the wrong orientation, producing results **identical** to the pooled model — a silent failure. |
| `scripts/battery.py` | Included World Bank regional aggregates as if they were countries (223 "countries"). Superseded by `massification_analysis.py`, which filters to real countries. |
| `results/bayes_hierarchical.txt` | Contains a single line. The Gibbs sampler errored out; no posterior was produced. |
| The "12% of the fall in births" figure | This is a **variance share with no direction in it.** It was derived by squaring a correlation. When the sign was finally checked, higher schooling went with a *slower* fall — a ceiling effect. The 12% is arithmetically correct and interpretively empty. Do not quote it as "girls' schooling explains 12% of the fertility decline." |

---

## The rule this folder follows

A result counts only if it survived a test designed to kill it. Six did not survive
and are recorded above as failures of the hypothesis rather than quietly deleted.

The most important line in this file is the caveat on +1.43. If someone cites that
number without reading the specification curve, they will be citing a result that
holds in roughly a quarter of defensible specifications.
