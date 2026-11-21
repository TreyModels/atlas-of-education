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
