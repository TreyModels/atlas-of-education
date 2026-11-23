# 8. Discussion, limitations, and conclusion

## 8.1 The verdict table

Table 8 collects the paper's claims and their evidence grades. **S** = survives the reported specification space
and its designed falsifiers; **F** = contradicted by the reported evidence; **C** = cannot be tested with these
data, with the missing observation named.

**Table 8. What the project knows now.**

| # | claim | grade | key number |
|---|---|---|---|
| 1 | Schooling–fertility is large and negative in levels, all eight measures | S | women's attainment −0.129 (0.029), n = 5,915, 192 countries; 8/8 negative-significant |
| 2 | The levels result is robust across the specification space | S | 99.7% of 288 period specs negative; 91.3% negative-significant; 0% positive-significant; median −0.475 |
| 3 | The level relation is a global between-country property | S (this relation) | 71–99% of 13,800 random six-group partitions negative-significant vs 0–7% in changes |
| 4 | The standard change design erases or reverses the relation | S | women's attainment +0.111 (0.045); 0/8 negative-significant; 3/8 positive-significant |
| 5 | The level relation is a development gradient, not an identified schooling effect | S | future-schooling placebo 52.9% vs 58.8% negative-significant (~90% as strong) |
| 6 | The gradient is steepest at the massification margin (shape), with conventional hinge locations | S (shape) / C (hinge locations) | below 6y −0.326 [−0.405, −0.248]; 6–9y −0.092 [−0.175, −0.013]; >9y +0.112 [+0.057, +0.171]; hinges at 6 and 9 years are conventional, not data-searched |
| 7 | A survey-level (DHS) negative gradient exists across 86 countries | S (ecological) | primary −0.57 (0.06), secondary −1.62 (0.17), higher −2.54 (0.24); 99% of 346 surveys negative |
| 8 | The gradient steepens in later cohorts and denser pipelines | F | attenuates instead: cohort +0.26 (0.13); pipeline +0.13 (0.05) |
| 9 | Individual-level and wealth-controlled tests of the gradient | C | DHS Individual Recodes not publicly obtainable |
| 10 | A care-work loop generates a self-reinforcing low-fertility trap | F | care-work gradient +0.009 (t 0.17) once income (+0.242, t 2.47) and urbanisation (+0.42, t 3.38) enter; male-care placebo +0.179 (t 2.10); manufacturing placebo −0.189 (t −3.47) |
| 11 | A strong "no-off-switch" | F (strong); S (weak) | 34/396 country-episodes rebound (8.6%, upper 11.3%); 5/38 within 10y; ceiling 1.83; event study +0.035 (0.025), MDE 0.070 |
| 12 | A tipping point / critical slowing down | F | autocorrelation −0.025 (0.008), wrong sign; variance +0.079 (0.034) fails surrogate (0.42) |
| 13 | Mortality decline is the leading driver of the collapse | F | freezing pre-antibiotic mortality removes 3.2% (range −1.8 to +8.2%); ±50% band 0.9–4.7%; 4.5× check 10% |
| 14 | The individuation model beats a development-only rival out of sample | F (tie) | 24.43 vs 21.10, diff +3.32 [−3.76, +11.14]; 3/6 countries |
| 15 | Wide model intervals are a statistical artefact | F | four of five spreads stay 0.87–1.01 across the tolerance ladder |

## 8.2 What the audit establishes and what it leaves open

The audit establishes four things. First, the between-country gradient is one of the most robust regularities
available for this relation: it survives the full specification curve, all eight measures, and 13,800 arbitrary
re-groupings of countries. Second, the field's standard change specification erases it: the same measures on the
same panel give weak or positive coefficients, with no negative-significant change cell. Third, the erasure is a
design property, not a substantive finding: the within estimator removes the between-country variation in which
the gradient lives, and the paper's decomposition of that variation is the audit's core. Fourth, the level
gradient is descriptive: the future-schooling placebo is about 90 per cent as strong as the correct-time
relation, which is the signature of a shared development process rather than an identified effect of schooling.

Three things remain open, and the paper names them rather than resolving them. The individual-level mechanism is
open because the DHS microdata were not obtainable; the survey-level gradient is consistent with an individual
gradient but cannot confirm it. The historical driver question is open in the sense that the transition model's
mortality counterfactual removes only 3.2 per cent of the collapse while the development-only rival ties the
individuation model out of sample; the magnitudes say the collapse is schooling-led within the model, and the
model is calibrated, not identified. The causal question is open by design: no observational design in the
project identifies the effect of schooling on fertility, and the paper's most useful contribution to the causal
literature may be the specification of what a credible design would need (Section 6).

## 8.3 Limitations

**Observational designs throughout.** The levels analysis is a between-country description; the change analysis
is a within-country association; the survey analysis is ecological; the transition analysis is a calibrated
model. The placebo is the paper's own statement of the limit, not an appendix to it.

**Measurement.** "Years of schooling" and "secondary education" mean different things across countries and
cohorts; the DHS cohort results are the clearest demonstration. Harmonised attainment series carry documented
reconstruction assumptions; enrolment and completion measures are not identical objects; gender-parity indices
can hide distributional change. The robustness of the levels sign across eight measures is reassuring for the
sign, not for the magnitude.

**Multiple comparisons.** The paper reports large specification grids without a formal family-wise correction.
The defence is procedural — pre-registered grids, every cell reported, claims about sign consistency rather than
single p-values — and it is a defence, not a substitute for one.

**Data gaps.** DHS Individual Recodes were not obtainable, so the individual-level test, the wealth horse-race,
the community placebo, and the quantum/tempo decomposition remain undone. The literature search is documented
but is not a PRISMA-style systematic review. One ad-hoc multiverse run produced during the project could not be
re-verified after the compute node went offline; it is not used for any number in this paper, and the published
battery covers the same ground.

**Generalisability.** The panel is 196 countries over 1960–2024. The transportability experiment shows the level
relation reproduces in arbitrary subsets of those countries; it does not show it would reproduce in another era
or measurement regime. The above-nine-years reversal is estimated on the richest and most schooled countries and
should not be read as a general statement about tertiary expansion.

**Authorship of evidence.** This is a synthesis across several workstreams; each section carries its record and
provenance, and the responsibility for a number is the record's. The claim-to-source map is the audit trail.

## 8.4 Conclusion

The level of analysis decides the answer. Between countries, the schooling–fertility relation is large, precise,
robust across 336 specifications, and reproduced in 71–99 per cent of 13,800 arbitrary country groupings. Within
countries, on decade changes, the same relation weakens and for several measures reverses, with no
negative-significant change cell. Both estimates answer different questions; reading one as if it answered the
other's question is what produced the contradiction this paper set out to audit. The audit's second conclusion is
less comfortable: the between-country gradient is not an identified schooling effect, because a future-schooling
placebo is about 90 per cent as strong as the correct-time relation. The gradient is descriptive — real, global,
steepest at the massification margin, and located in the first six years of schooling — and it should be read
that way.

The contribution is therefore a structural demonstration about a known correlation, not a new correlation: it
shows what the field's standard change specification does to the gradient, measures the erasure with a full
specification space and a random-re-partition yardstick, quantifies the development-gradient caveat with a
placebo, and places the gradient in the schooling distribution. The project's nulls — the care-work loop
absorbed by income, the falsified strong no-off-switch, the absent tipping point, the mortality counterfactual
that removes 3.2 per cent, the tolerance ladder that is an identification limit — are reported with the same
discipline, because a synthesis that reported only the surviving results would be doing to its own evidence what
the paper criticises in the literature. What survives is a development gradient at the massification margin;
what fails is the causal reading of it; what cannot be tested with these data is the individual-level mechanism,
and the paper names the data that would test it.
