# PRE-REGISTRATION AMENDMENT_01 — corrected small experiment (matrix layer)

**Status: committed BEFORE any confirmatory run.** This document amends
`research/records/2026-11-24-synthetic-matrix-v2/PRE_REGISTRATION_corrected.md`
(commit `77d6f23`, blob `618f4d1c…`, sha256 `eab63120…`). It supplies the definitions
requested by the Codex audit steer (Codex, Bridge `2026-11-24T12:07Z`: grouping types,
link/outcome/unit definitions, equivalence-margin justification, primary decision rule,
cross-validation units and dependence). It follows the programme Lead's proposed
resolutions on the Bridge (`2026-11-24T12:08Z`, "Re: Corrected preregistration:
definitions needed before confirmatory run") and is committed so that implementation and
independent review have a fixed target.

**Exploratory until reviewed.** Until Codex's review of this amendment and of a passing
smoke is recorded, no run under this amendment is confirmatory. Any run is labelled
EXPLORATORY. If Codex rejects any element, analyses depending on that element are
exploratory. Nothing in this amendment may be tuned after seeing results.

**Scope:** the matrix layer only. Everything in §G is unchanged; this amendment
supersedes only the grouping dimension, the link/outcome/unit definitions, the
equivalence margin, the decision rule, and the dependence/validation rules.

---

## A. Groupings — supersedes "full sample + 4 declared types" (80 groupings)

**Declared country types.** The committed 64 countries are assigned to the **eight declared
types of the v2 eight-type table** (`TYPES` rows 0–7, the same table from which the
corrected prereg's "4 declared types" were the first four rows), **8 countries per type**
(country `c` → type `c mod 8`), with within-type `N(0, 0.05)` jitter clipped to the declared
ranges. This supersedes the 4-type/16-country assignment, which cannot define the eight
typology splits; all eight rows are now used, the first four remain the four archetypes.

**Cell estimator (unchanged committed convention).** Within a grouping, the slope is
estimated separately in each declared group; the grouping-level estimate is the **mean of
the group slopes**. A cell is (link, specification, dose, block, grouping).

**(i) 64 seeded random four-way partitions.** For partition `k = 0..63`, permute the 64
country indices with `numpy.random.default_rng(20261124 + k)` and split the permutation into
four groups of 16. Fixed seed list; no re-drawing.

**(ii) 8 typology one-vs-rest splits.** For declared type `t = 0..7`: the 8 countries of
type `t` vs the other 56 countries. Declared labels in table order — 0 development-high,
1 development-low, 2 school-supply-high, 3 school-supply-low, 4 labour-market-formal,
5 labour-market-informal, 6 urbanised, 7 rural. These labels name the declared synthetic
archetypes; they are **not** measured real-world categories.

**(iii) 4 pair-pooled splits.** For `i = 0..3`: types `(2i, 2i+1)` pooled (16 countries) vs
the remaining six types pooled (48 countries).

**(iv) 4 extreme-quartile splits.** For each declared country-level index, computed from the
block's drawn country parameters and standardised (z) across the block's 64 countries:
- development `D = z(mu_y) + z(mu_a)`;
- school supply `S = z(f_pub_pre)`;
- labour-market formality `L = z(shadow_cost) − z(w_child)`;
- urbanisation `U = z(mu_y)` (declared proxy — the kernel has no urbanisation parameter).

Split each index into the **bottom 16 countries (below its 25th percentile) vs the top 16
countries (above its 75th percentile)**; the middle 32 countries are excluded from that
grouping (declared). The urbanisation proxy is recorded as the weakest of the four.

All membership rules are fixed from the declared type table and the block's drawn country
parameters before the run. Mixing the committed 4-type assignment into these 80 groupings is
not allowed.

## B. Links — outcome, predictor, units (supersedes the link-list wording)

**Predictor for every link:** `ΔGER`, the change in the school-participation share over the
specification's window (S1/S4: 10-year change; S2/S5: true 5-year change; S3: level; S6:
one-year change).

**Outcomes (7), model units:**
1. child-employment share (states 1,2 of the 4-state child-labour continuum);
2. study-and-work share (state 1);
3. visible-work-only share (state 2);
4. hidden-work share (state 3);
5. tutoring share (share of households using tutoring);
6. mean learning (grade-equivalents, upstream model units);
7. **log mean household income** (natural log of mean simulated household income; replaces
   the raw mean-income outcome).

**Raw slope unit:** outcome change per 1.0 `ΔGER` (proportion points, grade-equivalents or
ln points per unit GER). **Standardised slope:** coefficient from regressing
`outcome / SD(outcome)` on `predictor / SD(predictor)`, where each SD is computed on the
estimation sample of the relevant (block, world, specification, dose, group). Both raw and
standardised slopes are reported for every cell; **all equivalence claims use the
standardised scale.**

## C. Equivalence margin — supersedes the raw ±0.05 slope-unit margin

Equivalence is judged on **standardised slope differences**: `|Δβ_std| ≤ 0.05 SD`. The
margin is declared prospectively as the **smallest effect of interest** (one twentieth of a
standard deviation): below it, a cross-world slope difference is not interpretable as a
mechanism separation for this programme. Raw-unit slopes and link-specific SDs are reported
alongside so the margin is interpretable; **no raw-unit ±0.05 claim is made across
differently scaled links.** The margin is not tuned on results. If independent review
judges the margin unjustified for a given outcome, equivalence statements for that outcome
remain exploratory (declared).

## D. Primary decision rule — supersedes "TOST and/or predictive discrimination"

**Primary:** TOST on standardised cross-world slope differences, at the cell level.
Equivalence for a cell×pair is declared only if the **90 % CI of the paired difference lies
wholly inside ±0.05 SD**. The wall statistic is the **share of cells whose ten pairwise
world differences are all equivalent**, reported with its uncertainty (country-cluster
bootstrap over blocks/countries as declared in §E). Effect sizes — standardised `Δβ_std`
and raw `Δβ` — with CIs are reported for every cell and pair. **"Non-significant" alone is
not equivalence.**

**Secondary/exploratory only:** predictive discrimination (out-of-block AUC/accuracy with
country-clustered CIs). It is not a co-primary and cannot override the TOST result.

## E. Cross-validation units and dependence

- **Unit of independence:** the country. The 10 blocks draw fresh, independent country sets;
  within a block the same country characteristics are paired across worlds.
- **Cross-validation folds are by country, never by cell.** Declared split: train on blocks
  0–4, test on blocks 5–9; no country appears in both.
- **Slope-difference CIs:** country-cluster bootstrap, 1,000 draws over countries within
  blocks (and the paired independent-block t summary retained for comparability). Groups
  with fewer than 20 countries report the cluster count and use t with `df = G − 1`.
- **No cell-level binomial CIs anywhere.**

## F. Grid size and runtime consequence (declared before the run)

Group-units per block: `64×4 + 8×2 + 4×2 + 4×2 = 288`. Grouping-level cells:
`7 links × 6 specs × 2 doses × 10 blocks × 80 groupings = 67,200` (×5 worlds = 336,000
cell-world estimates), from ~1,209,600 group-level regressions. The original "1–2 minute"
expectation does not apply; **runtime must be measured and reported** before the run is
called complete. No post-hoc grid reduction.

## G. Unchanged from the committed corrected pre-registration

Worlds P, S, C, R **plus the s=0 zero-signal world included in the matrix**; N = 10,000
households/country; 64 countries; 25 years; 10 independent country blocks (fresh country
draws per block); the six specifications S1–S6 exactly as declared (including **true 5-year
windows** in S2/S5 and genuine first differences in S6); measurement-error doses 0× and 1×
(σ = 0.05; 2× dropped as declared); cluster-robust CIs over countries (no binomial over
cells); **Phase B corrections** (WOMEN = 4,000; B1 within-mother with explicit denominators;
feature-specific admissibility gates; independent s=0 draws); failure/rank preservation; no
tuning toward a result; old exploratory outputs untouched.

## H. Fixed identifiers for the amended run

- Amendment base: `PRE_REGISTRATION_corrected.md` @ `77d6f23`, sha256 `eab63120…`.
- Random-partition seed: `20261124 + k`, `k = 0..63`.
- Within-type jitter: `N(0, 0.05)`, clipped to declared ranges; type assignment `c mod 8`.
- Blocks: as in the base prereg (10 fresh independent country draws).
- Margin: standardised `0.05 SD`; TOST 90 % CI; α = 0.05.
- Bootstrap: 1,000 country-cluster draws; `df = G − 1` for `G < 20`.

Any departure from this amendment must be written into the run manifest **before** the run;
the run is then labelled EXPLORATORY and the departure reported to Codex.
