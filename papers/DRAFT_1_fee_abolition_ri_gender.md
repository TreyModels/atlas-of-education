# DRAFT — Fee abolition and the primary-GER jump: randomization inference and a sex split

**Working draft, 25 Nov 2026. Association only; no causal claims.** Evidence: `research/records/2026-11-25-e8-fisher-ri/`
(branch `research/e8-fisher-ri-2026-11-25` @ `fb8b67e`) and `research/records/2026-11-25-gender-split-e6e8/`
(branch `research/gender-split-e6e8-2026-11-25` @ `b4eb680`). Estimator and verified dates from
`research/e6e8-sequencing-2026-11-25` @ `bd782be` (`e8_fee_event_study.py`).

## Abstract

Using eight source-verified African primary-fee abolition dates (1994–2005) and World Bank/UNESCO
gross primary enrolment ratios, the staggered-adoption Callaway–Sant'Anna (CS) event study shows a large
post-abolition rise in primary GER. A design-based Fisher randomization inference (RI) check over 2 × 10,000
placebo re-assignments places the observed statistics far outside both placebo distributions (two-sided
p = 1.0 × 10⁻⁴ for the placebo-date family, 6.0 × 10⁻⁴ / 3.0 × 10⁻⁴ for placebo-country). The result is
"consistent with" a date-specific association; it is not causal, the treated sample is small (7–8 countries),
and the on-impact estimate's bootstrap CI includes zero. A female-vs-male split finds no detected sex
difference in the mean post-abolition jump (D = −3.94 pp, 95% CI [−8.72, +0.29]). The `t* = t_abolition + L_primary`
"bulge arrival" leg is **NOT-ESTIMABLE** (`L_primary` sourced 0/8; no sex-disaggregated repetition/transition
series; DHS IR microdata absent).

## 1. Data

- Outcome: WDI `SE.PRM.ENRR` (primary GER, annual), vintage Last Updated **2026-11-11**; sex series
  `SE.PRM.ENRR.FE` / `.MA`. Committed long panels with raw-zip sha256 (E8: `ca495dfe…`; panels exact against a
  fresh download).
- Treatment: the **8 VERIFIED** abolition dates — MWI 1994, ETH 1995, UGA 1997, LSO 2000, TZA 2001, KEN 2003,
  MOZ 2004, GHA 2005 (`data/fee_dates.csv` @ `bd782be`). The 4 unresolved dates (CMR, ZMB, RWA, BDI) are
  never-treated controls.
- Sample: Sub-Saharan Africa per WDI metadata, 1990–2015; 48 SSA countries in the outcome panel.

## 2. Estimator and reproduction gate

CS ATT(g,t) with universal base period g−1, not-yet-treated controls (≥3), event time −5…+6, cohort-size-weighted
event aggregation; country-cluster bootstrap (500). Before any new analysis, the published verified-8 table was
reproduced **exactly**: ATT(0) = 12.44362392207772 (|Δ| = 0.0), SE_boot(0) = 7.550738928931049 (|Δ| = 0.0),
all 11 event ATTs within 2.2 × 10⁻¹⁶. This gate is the only reason the new inference is trusted.

| event | CS ATT | boot SE | 95% CI |
|---|---|---|---|
| −5 | 6.39 | 3.30 | [−0.08, 12.86] |
| −4 | 1.35 | 3.93 | [−6.35, 9.04] |
| −3 | −0.13 | 3.62 | [−7.23, 6.98] |
| −2 | −0.03 | 1.74 | [−3.43, 3.38] |
| **0** | **12.44** | 7.55 | [−2.36, 27.24] |
| +1 | 23.82 | 11.11 | [2.05, 45.60] |
| +2 | 25.94 | 10.95 | [4.48, 47.40] |
| +3 | 22.12 | 8.42 | [5.62, 38.62] |
| +4 | 25.19 | 8.50 | [8.54, 41.84] |
| +5 | 28.56 | 9.67 | [9.61, 47.51] |
| +6 | 25.92 | 8.82 | [8.64, 43.20] |

Pre-trends at −2/−3 are flat; the on-impact estimate (e=0) is positive but its CI spans zero; post-period
estimates are consistently positive. Mean post ATT (+1…+6) = **25.2607 pp**.

## 3. Fisher randomization inference

Pre-registered (`4e466a3`) before any permutation: B = 10,000 per family, master seed 20261125, statistic
T0 = CS ATT(0) (primary) and Tpost = mean post ATT (secondary), p = (1 + #{|T_perm| ≥ |T_obs|}) / (B+1).

- **Placebo-date**: redraw each treated country's date uniformly from its feasible 1990–2010 window (excluding
  true ±2). T0 permutation mean −0.90 (SD 1.25); **0/10,000** draws reach |T_obs|; p2 = 9.999 × 10⁻⁵ (the exact
  resolution floor 1/(B+1)). Tpost mean −2.54 (SD 3.76); p2 = 9.999 × 10⁻⁵.
- **Placebo-country**: keep the 8 dates, reassign to 8 of 40 never-treated SSA countries. T0 mean −0.40
  (SD 2.15); 5/10,000 reach |T_obs|; p2 = 5.999 × 10⁻⁴. Tpost mean −1.04 (SD 5.17); 2/10,000; p2 = 2.9997 × 10⁻⁴.

**Pre-registered classification: `robust`** (all four two-sided p < 0.05) → "consistent with a date-specific
association; RI passes both placebo schemes". Two exploratory probes — excluding the 4 unresolved-date countries
from the placebo pool (P = 36) and a local placebo window (true date ±3, excluding ±2) — both left the conclusion
**unchanged** (p2(T0) = 1.0 × 10⁻⁴ and 9.999 × 10⁻⁵ respectively; `fb8b67e`).

**Caveats.** The observed assignment is a real policy process, so this is a design-based placebo check, not a
randomized-experiment test; p-values are conditional on the pre-registered schemes and the 40-country pool. The
placebo-date p sits at the Monte-Carlo floor. The on-impact CI still includes zero. The four unresolved-date
countries are controls and could contaminate the null (direction unsigned).

## 4. Female-vs-male split

Outcomes `SE.PRM.ENRR.FE` / `.MA`, same CS design, 500 paired country-cluster bootstraps (same country draw for
both sexes; seeds 20261125+i). Pooled gate reproduced exactly before interpreting the split.

- ATT_F(0) = **11.63** [3.34, 29.68]; ATT_M(0) = **13.38** [4.73, 34.06].
- Mean post: female **22.81**, male **26.75**.
- Primary statistic D = mean post_F − mean post_M = **−3.94 pp**, 95% CI **[−8.72, +0.29]** (498/500 reps):
  includes zero → pre-registered verdict **"no detected sex difference"** (male-higher point estimate, not
  statistically separated).
- Descriptive event-level: male-higher at +1 (−3.99 [−7.09, −0.53]) and +2 (−4.67 [−8.61, −0.87]); others include
  zero. Pre-trends flat in both sexes.
- Exploratory follow-up: the aggregate null is **not** a weighting artefact. An inverse-variance weighted D
  (−4.05 [−5.94, −2.17]) appears to exclude zero only because marginal event SEs ignore the strong positive
  correlation of event differences in the paired bootstrap; with the joint paired SE both the IV and equal-weight
  estimates include zero. Leave-one-event-out range 0.27 pp; dropping MOZ gives D = −3.95 [−8.32, +0.24]. The
  confirmatory headline is preserved; the upper CI endpoint (+0.29) makes this a near-boundary non-detection,
  not a precise zero.

## 5. What is not estimable

`t* = t_abolition + L_primary` ("bulge arrival") is **NOT-ESTIMABLE**: the primary-cycle length `L_primary` is
sourced **0/8**; no committed sex-disaggregated final-grade repetition or primary→secondary transition series
exists; DHS IR microdata are not in the repository. No proxy, no borrowed cycle lengths, no auditor candidate
dates were used. This is a data-acquisition gap, not a compute gap.

## 6. Claims → source

| claim | value | file |
|---|---|---|
| ATT(0), verified-8 | 12.44362392207772 | `…e8-fisher-ri/results/e8_ri_results.json` (`observed.T0`) |
| RI p2, date/country | 9.999e-05 / 5.999e-04 | same (`families.*.p_two_sided`) |
| classification | robust | same (`decision.classification`) |
| `t*` | NOT-ESTIMABLE, L_primary 0/8 | same (`t_star`) |
| D, sex split | −3.94395098, CI [−8.7178, 0.2946] | `…gender-split-e6e8/results/gender_split_results.json` |

**No causal language.** The strongest reading used is "consistent with".
