# Pre-registration: the care-work loop and credential inflation (23 November 2026)

**This file was committed before any data extraction, estimation or result.** It fixes the measures,
samples, tests, falsifiers and decision rules for both dynamics. Any departure from it will be stated in the
report, and no specification will be quietly dropped from the specification curve.

## Data sources and coverage rule
| source | series intended | role |
|---|---|---|
| ILO SDMX (ILOSTAT) | employment by sex and economic activity (ISIC), employment by sex and occupation (ISCO), employment by sex and education | care share and credentialed-jobs share |
| World Bank WDI | total fertility, female labour-force participation, female educational attainment, GDP per head (log), urban share | outcome and controls |
| project panel `/root/work/data` | fertility and participation already assembled by the project | cross-check |

Coverage rule: each dynamic is estimated on **one documented sample**, and if the two dynamics cannot share
a sample then both samples are reported and no cross-dynamic comparison is made. Pre-committed sample gates:
at least **30 countries** for a headline number; 15-29 countries → descriptive only; under 15 → declared a
data gap and reported as such. A published data gap is an acceptable result.

## A. Care-work loop — hypotheses fixed in advance
The theory: the schooling pipeline formats women for competitive self-investment and then employs a large
share of them in institutional care work (teaching, nursing, childcare, elder care) that replaced dissolved
kin alloparenting, pulling them further out of reproduction.
- **A1 (pipeline).** The care share of female employment rises with female attainment. Expected sign
  **positive**, country and year fixed effects.
- **A2 (loop).** Fertility falls faster where the care share is high: the care share interacted with time
  should predict a **larger fall** in fertility.
- **A3 (amplification).** The attainment-fertility association is **stronger** where the care share is high:
  the interaction of attainment with care share should be **negative** on fertility.
Measures, fixed now: care share = female employment in ISIC **P (education) + Q (health and social work)**
divided by total female employment. Occupation-based alternative (only if sectoral data fail, reported
separately): female employment in the teaching and health sub-major groups of ISCO. Attainment = share of
women 25+ with at least upper secondary schooling; fertility = total births per woman.
**Falsifiers, pre-committed:** (i) no association, or the sign reversed; (ii) the association disappears once
log GDP per head and urbanisation are included — "fully explained by income/urbanisation" kills it;
(iii) **male** care employment shows the same association as female care employment (then the mechanism is not
about women's care work); (iv) an unrelated sector (manufacturing) substituted for care gives the same answer.
**Decision rule:** "supported" only if A1 and A3 hold, survive (ii), and the placebo (iii) or (iv) fails.
If only A1 holds, the result is a **null** on the loop itself and will be reported that way.

## B. Credential inflation — hypotheses fixed in advance
The theory's signature: credentials proliferate relative to credentialed jobs, so queue **position** rather
than attainment is what matters.
- **B1 (positional).** Fertility tracks the credential-occupation gap more than average attainment: in a horse
  race containing both, the gap's coefficient is larger in magnitude and the attainment coefficient collapses.
- **B2 (saturation).** The positional measure predicts fertility better in high-attainment (saturated)
  countries than in low-attainment ones.
Measures, fixed now: attainment = share of women 25+ with tertiary schooling (secondary as robustness);
credentialed-jobs share = share of female employment in ISCO groups 1+2 (managers, professionals);
**credential-occupation gap = attainment minus credentialed-jobs share** (positive = more credentialed people
than credentialed jobs). Overeducation from ILO employment-by-education tables will be used **only if**
available for the same sample; otherwise it is declared unavailable and not mentioned as evidence.
**Falsifiers, pre-committed:** (i) the gap adds nothing once attainment is in the model — no explanatory gain
and the attainment coefficient does not fall (this kills B1); (ii) the gap's sign is the opposite of
predicted; (iii) the saturated/low-attainment split shows no difference (kills B2).
**Decision rule:** "supported" only if the gap survives alongside attainment **and** adds explanatory power;
a tie, or no gain, is reported as a null.

## Specification curve, fixed before estimation
For each dynamic, estimate **all** combinations of: measure variant (primary, secondary/alternative); controls
(none, log GDP per head, log GDP + urbanisation); sample (all, 30+ country core, 1990 onward); fixed effects
(country + year, year only). Report the full distribution of signs and significance, not just the chosen
specification. The headline is the pre-registered specification; the curve shows whether it is robust.

## Reporting rules agreed in advance
Every headline number carries its uncertainty, its sample, and the falsifier it survived or failed. Nulls are
reported with their power (sample size, standard errors). No causal language for cross-country associations.
A thin-data outcome is a result, not a failure, and will be stated as a data gap with the exact series that
were missing.
