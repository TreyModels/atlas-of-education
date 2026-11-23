# Methods paper §6.6 — auditor stress test of the dependence revision (head 734d055)

`novelty-review`, 24 November 2026. Read of `research/methods-multiverse-paper-2026-11-23` @ 734d055,
`paper.md` §6.6 and `scripts/dependence_analysis.py` / `results/dependence_analysis.json`.

## What the revision gets right

1. The assumption is now stated instead of buried: BH needs independence or PRDS, the 272 null-share series share
   the 400 draws, `mean |r| = 0.041`, 51/49 positive/negative, max 0.44, so PRDS is not established empirically.
2. The claim is correctly downgraded to "a pre-specified draw budget and certification-ceiling rule, conditional on
   independence or positive dependence, with an effective-tests sensitivity bound and a dependence-aware permutation
   null" — that is the honest form of the claim, and §7 no longer presents the rule as a calibrated test.
3. The dependence-aware permutation null (each of the 400 draws treated as pseudo-real, same BH step-up, zero
   certified) is a genuine improvement: it answers the specific objection "is the cluster count driven by shared
   draws?" rather than waving at it.
4. The final sentence correctly flags that the project's own 13,800-partition battery shares the same structure and
   needs its own check.

## Holes, in referee order

### H1 (main): the procedure the paper cites for arbitrary dependence is never applied — BY certifies 0 at 400 draws

§6.6 cites Benjamini–Yekutieli (2001) for the PRDS condition, but the BY *procedure* (valid under arbitrary
dependence) is not computed. I computed it from the paper's own numbers (M = 272, α = 0.05, 400 draws):

- H_M = Σ 1/i = 6.185; BY threshold at rank k = k·0.05/(272·6.185) = **2.97e-5** for a lone link.
- The Monte Carlo p floor at 400 draws is 1/(400+1) = **2.49e-3**.
- A link can only clear BY if it is at the floor and k ≥ ceil(0.002494·272·6.185/0.05) = **84**; only **30** links
  are at the floor. **BY therefore certifies 0 links at 400 draws — not 35, not 44.**
- The BY draw budget is correspondingly larger: lone link ≈ **33,650** draws; a cluster of 30 ≈ **1,120** draws;
  cluster of 35 ≈ **960** (vs the paper's nominal 5,440 / 182 / 156 and M_eff 3,140 / 105 / 90).

So the honest range is **0 (BY, arbitrary dependence) / 35 (nominal, independence–PRDS) / 44 (M_eff sensitivity)**,
and the sentence "The floor-cluster certification is robust in every case — it never falls below the baseline" is
false under BY (0 < 35). This is the number a methods referee will compute first, because the paper itself supplies
the ingredients. Add a BY row to the certification grid and to the draws table, and soften "robust in every case"
to "robust across the M grid but not under BY".

### H2: the M_eff correction moves the wrong way to be a bound

M_eff = 157 < 272 loosens the BH threshold, so certifications rise 35 → 44. But BH under PRDS is already valid at
the nominal M (it is, if anything, conservative there); loosening it is justified only if the dependence is
effectively positive — which is precisely what §6.6 says is *not* established (49% of pairs negative). So M_eff = 44
is not a dependence-robust bound; it is a "what if the dependence were effectively positive" sensitivity, and it
sits on the anti-conservative side of the nominal number. Present it that way (or replace it with a dependence-robust
procedure: BY, Romano–Wolf stepdown, Westfall–Young maxT, or a permutation-based FDR). The current sentence
"certification can be recomputed under the effective count … 44 rather than 35" reads as the improved answer, not as
a directional sensitivity — a referee will read it as the former.

### H3: Li–Ji is applied to a proxy matrix, not to the test statistics

The input is the correlation matrix of the 272 **null-share series** (bounded family-balanced shares across 400
draws), not the null correlation of the test statistics or p-values that BH acts on. The Li–Ji (2005) formula —
implemented correctly in the script as `(Σλ)²/Σλ²` — assumes jointly normal test statistics with a known correlation
structure. Applying it to null-share correlations is a heuristic, and the paper should label M_eff ≈ 157 and
"162 PCs for 90% variance" as properties of the proxy, not of the tests. (Also justify the M = 50 lower bound in the
sensitivity grid; it currently looks chosen rather than derived.)

### H4: the rule-of-three bound assumes independent pseudo-runs

"Zero certified in 400 pseudo-runs → chance ≤ 0.75%" uses n = 400 as if the pseudo-runs were independent. They are
not: all 400 pseudo-runs reuse the same 400 draws (each draw is compared with the other 399), so the effective number
of independent pseudo-runs is below 400, and the bound should be 3/n_eff (or obtained by a blocked/permutation
scheme). The qualitative conclusion (the observed 35 is far above a shared-draw null) survives; the "0.75%" number
is optimistic. `dependence_analysis.json` already carries an `M_eff` field for the permutation null — use it to
compute the bound.

### H5: the "what would change our minds" budget is conditional

§6.7 says a 5,440-draw replication "would convert the main-tier claims into strict individual certifications". Under
BY the lone-link budget is ≈33,650 draws (6.2× nominal), cluster-30 ≈1,120. Quote both, or the resolution cost is
understated exactly where the paper is most careful.

### H6 (minor): make the 13,800-battery flag operational

The final §6.6 sentence is right, but say what the check is: those 13,800 partitions of the same 217 countries
overlap heavily, so they are not independent draws; if any certification is read from them, run the same BY/block
check; if the 71–99% shares in Paper F are descriptive, say so explicitly. ("Needs its own dependence check" is a
good flag; naming the check closes it.)

## Verdict

The revision is a real improvement and the downgrade is the right claim. But as it stands the paper reports the two
*dependence-sensitive* numbers (35 nominal, 44 effective) and omits the one *dependence-robust* number (BY = 0 at
400 draws, ~33,650 draws for a lone link), which is the number the paper's own cited procedure implies. Add H1 and
the §6.7 budget, reframe M_eff as a directional sensitivity (H2), and the rule-of-three bound with n_eff (H4); H3
and H6 are wording.
