# Yang et al. (2026) log city-size / occupational-variety law — exploratory play

**Status: EXPLORATORY / DERIVED / SIMULATED. No observed city data read. No claim about any country.**
Source: Yang, Holehouse, Kempes, Youn, Arroyo, Redner & West, "Scaling laws for function diversity and
specialization across socioeconomic and biological complex systems", *PNAS* 2026,
doi:10.1073/pnas.2509729123 (arXiv:2208.06487). City relation (422 US MSAs): **D = b·ln N + c**,
**b = 128** occupations per ln(working population), R² = 0.94; their worked example δ = 0.71%/yr
(2019) ⇒ dD/dt = δb ≈ 0.9 occupations/year. Other systems follow D ∝ N^β with β = 0.35–0.57.

## What I did

Adopted b and δ verbatim; anchored c by declaring D(10⁶) = 500 with sensitivity {300, 500, 700};
explored four implications relevant to the massification programme. Code: `code/yang_play.py`
(deterministic). Outputs: `results/yang_play.csv`, `results/yang_play_summary.json`.

## Findings (all derived/simulated, not estimated)

1. **The residual-speed identity reproduces exactly:** δ·b = 0.0071 × 128 = **0.909 occupations/yr**.
   Over six years (2019-style urban growth) occupation-driven variety grows by **5.45 occupations
   (0.63% of 867)**.
2. **That is ~240× smaller than credential-count growth over the same window.** The Domus E4 package's
   credential offerings rise 738k → 1.85m (**×2.507, +150.7%**); ratio of credential growth to the
   occupation-variety benchmark = **239.6**. Even if every new occupation spawned a credential,
   occupation-driven diversification cannot generate credential proliferation. **This independently
   supports the E4 "two laws, not one" correction** (credentials are supplier-launched products, not
   occupational categories) — *conditional on the credential counts, which the review has flagged as
   partly invalid*.
3. **The elasticity of variety with respect to population falls as b/D.** With D(10⁶)=500:
   elasticity **2.05** at N=10⁵, **0.62** at 10⁶, **0.30** at 10⁷, **0.16** at 10⁸;
   rungs per 1,000 workers falls **2.05 → 0.50 → 0.079 → 0.011**. Variety is a small-city
   phenomenon per capita: each new resident adds b/N occupations (≈1 per 7,800 at N=10⁶; ≈1 per
   78,000 at N=10⁷).
4. **Gate-pressure implication (the most interesting for massification).** If each occupation type
   carries one credential rung and graduates are 10% of the population, **graduates per rung** rises
   **48.7 → 200 → 1,258** as N goes 10⁵ → 10⁶ → 10⁷. Bigger cities have *more* occupational variety
   and *far more* graduates per rung: a candidate mechanism for intense gate competition and tutoring
   demand in large cities, despite more variety. Testable with city-level data (not on disk).
5. **Aggregation over a Zipf system:** as urbanisation rises 20→100% (200 cities, α=1), total variety
   rises 10,444 → 44,331, but variety per urban resident *falls at the margin* (1,042 → 886 per
   million). Aggregate variety is driven by the number and sizes of cities, not by total population.
6. **Where the law breaks:** with the 10⁶=500 anchor, D = 0 below N ≈ **20,000**. The log law is an
   MSA fit and **cannot be extrapolated to towns and villages** — exactly the scale domain of the
   coevolution model. Any use below the MSA range is out of scope for the paper's fit.

## Limits

b and δ are adopted, not re-estimated; c is a declared anchor with sensitivity; Zipf α, rural
variety (20) and the 10% graduate share are declared for illustration; the credential numbers come
from the Domus package (flagged by its reviewer); "one rung per occupation" is a strong assumption.
No causal or country claim. The relationship is about *how many occupation types exist*, not how many
people are employed in them or what credentials they require.

## What I would do with it next

1. **Model side:** add Yang's D(N) = b·ln N to the coevolution model's city-size block (city size →
   occupational variety → number of named gates/rungs), and test whether the gate-pressure
   implication produces the coexistence pattern with *differentiated* one-change responses (the
   falsifier v0 failed).
2. **Data side:** fetch MSA population + occupation counts (BLS OES / Census) to re-estimate D(N)
   independently, and check the b=128 fit period by period.
3. **Paper side:** use the δ·b benchmark as a bound in the "offered vs paid vs required" paper — it
   says how fast the *occupational* margin can move, which makes the credential-offering explosion
   even harder to attribute to occupational change.

---

## Addendum — user-supplied `pathways_factory.cjs` toy (factory-opening extension of the Yang law)

**Status: ILLUSTRATIVE TOY — user-supplied code, run as given; not evidence; no calibration.** Code saved at
`code/pathways_factory.cjs` (deterministic; 100-seed reruns byte-identical; 500-seed sweep stable). 64 arrivals/yr
(50/50 urban/rural), 36 years, factory opens at y=23 with 12 posts; income units: farm 1.0, informal 1.4, formal
2.0, factory 2.3; pre-shock y=20–22 matched across arms (verified). The "Yang" mapping is `types = 2 + log2(N/50k)`,
clamped to 1–12; the credential gate applies only to occupation index ≥ 2.

**Default mode (200 seeds; means over years 23–35):**

| scenario | leaving | secondary completion | factory hires | formal workers | household income |
|---|---|---|---|---|---|
| baseline | 54.019 | 36.069 | 0.000 | 52.084 | 950.030 |
| factory16 | 56.500 | 34.209 | 7.797 | 46.844 | 946.523 |
| factorySecondary (diploma for all posts) | 59.781 | 36.069 | 9.750 | 48.097 | 953.058 |

Reading: opening factory posts **pulls children out earlier and lowers secondary completion** (factory16); requiring
the diploma for the posts **restores completion to baseline** but raises leaving further; income effects are small.

**Yang sweep (500 seeds, `--yang`):** almost completely **inert**. At N=50k the mapping gives 2 types and the gate
never binds (needs occupation ≥2); N=200k without scaling gives 2 types — identical. Only **N=200k + scaling + gate**
moves: types 2→4, half the slots gated; leaving 57.95→59.57, completion 33.29→34.12, hires 9.83→10.64. The gate can
*raise* hires in this cell — a composition artefact of *who* gets selected, not a benefit of gating.

**Diagnosis (why it is inert):**
1. The Yang mapping is a token gesture, not the published law: Yang et al. fit **D = 128·ln N + c** (hundreds of
   occupations, R²=0.94); this toy moves **2→4 types** over 50k→200k (Yang implies ≈+177 occupations over that
   range), then clamps at 12. City size therefore enters only through a 0/2/4-type step.
2. The study/work rule is **static** (studyValue does not include future gate-clearing or the factory/formal wage),
   so choice responses are myopic and hires never reach 12.
3. No employer endogeneity (fixed 12 posts, fixed credential rule), no commute/travel, no capacity/quality — so it
   cannot generate the coevolution brief's coexistence/differentiated-response test.

**Concrete fixes:** (a) map Yang properly — let the **gated share** be a continuous function of D(N)=128 ln N + c
(anchor D(10⁶)≈500), rather than a 2-type step; (b) endogenise the credential rule (top-m types gated, m rising with
applicant surplus); (c) give studying a dynamic return (expected future wage × gate probability); (d) add travel cost
and the rural/urban split to test unused places + selective queues; (e) grid over city sizes and gate designs.

**Honest bottom line:** the toy shows the right *direction* — factory posts reduce completion, a diploma gate protects
it — but its Yang component barely bites. The thing to chase is not city size per se but **how many rungs carry
credentials**; that is where the leverage is.
