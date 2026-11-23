# Paper F section: The fertility mechanism under test — care work, policy bounds, and tipping points

*Draft section for the consolidated Fertility paper (lead: un-data). Every number below traces to a
verified record; the claims→source map is in `SOURCE_MAP.md`. Pre-registrations were committed before
analysis in each record. This section reports three pre-registered attempts to find the fertility
mechanism the framework predicts — a care-work loop, an off-switch that policy cannot reach, and a
terminal enclosure visible as a critical transition — and what their outcomes do and do not imply.*

## 1. What the framework predicts

The morphological-governance framework ("Networked Domus") treats fertility decline as a
by-product of a credential pipeline: as schooling becomes the gate to livelihood, the
opportunity cost of childbearing rises, and the decline becomes self-reinforcing. Three
predictions follow that are sharp enough to be killed, and they are the ones this section tests.

**Prediction 1, the care-work loop.** Fertility decline should be amplified by the growth of
paid care work. A rising care share of female employment provides the outside option that makes
childbearing costly, and the education–fertility link should steepen where care work is common.

**Prediction 2, no off-switch.** Pronatalist policy that works inside the pipeline — cash,
leave, childcare subsidies — should not restore sustained fertility above roughly 1.6 births per
woman. The mechanism, not the policy budget, sets the ceiling.

**Prediction 3, terminal enclosure as a tipping point.** The enclosure should behave like a
critical transition: before it, the fertility series should show the textbook early-warning
signature of rising variance and rising lag-one autocorrelation, and after it the schooling–
fertility link should show diminishing returns (a ratchet).

Each prediction was pre-registered with explicit killing tests, placebos and decision rules. The
short version is that none of the three survives in the form predicted, while one substantive
result — a plainly diminishing schooling–fertility link near the top — does survive, but
confounded with an arithmetic floor.

## 2. The care-work loop: a real association that is income and urbanisation

**Design and sample.** The pre-registered test used ILO sectoral employment (education and
health/social work) for 656 country-years covering 148 countries (2010–2023, eight ILO years),
merged with World Bank fertility, female attainment, income and urbanisation. The care share of
female employment is large and gendered: mean 18.3% (sd 12.1, range 1.2–52.1, n = 148), against
5.9% for men and 9.8% female manufacturing employment. The first test is whether the care share
rises along the credential pipeline.

**A1: the raw association is strong; the pipeline association is not.** Mean care share is 8.1%
in the bottom female-attainment tercile, 19.0% in the middle and 28.4% at the top (n = 47 per
tercile, 148 countries). That is the pattern the framework wants. Once national income enters,
it disappears: with log GDP per head controlled, the attainment coefficient on the care share
is **+0.009 (t = +0.17, n = 140)**, while log GDP carries **+0.242 (t = 2.47)** and, with
urbanisation added, urban carries **+0.42 (t = 3.38)**. The pre-registered falsifier "fully
explained by income and urbanisation" fires. What looks like a pipeline effect is a
development-and-urbanisation effect.

**A3: the amplification claim flips sign.** The pre-registered interaction of attainment with
the care share on fertility is **−0.131 (t = −1.38, n = 141)** without controls and **+0.128
(t = +1.53)** once log GDP and urbanisation are in. An interaction that changes sign under
controls is not a stable mechanism, and the predicted amplification fails.

**Placebos are decisive.** Replacing women's care employment with men's care employment gives an
interaction of **+0.179 (t = 2.10)**, and replacing it with manufacturing gives **−0.189
(t = −3.47)** — the unrelated-sector placebo produces a larger "effect" in the predicted
direction than care work itself. The pre-registered placebo falsifier fires.

**A2: the dynamic test has the wrong sign.** Across 119 country pairs (earliest versus latest
ILO year), fertility change on the early care share is **+0.199 (t = 2.14)** without controls
(higher care share goes with *less* fertility decline — the wrong sign for the amplification
story) and **−0.045 (t = −0.41)** with log GDP. Null.

**Specification curve.** Across 36 pre-registered specifications (two attainment measures ×
three control sets × three samples × three fixed-effect patterns) the care-share coefficient
takes both signs, from about −0.57 to +0.27, and its significance tracks the fixed effects, not
the care measure. One degenerate, perfectly collinear specification is reported rather than
dropped.

**What this section claims.** Not that care work is irrelevant to fertility — the cross-country
association is real — but that the framework's specific care-work *loop* is not separable from
income and urbanisation in this sample, and its placebos behave like the treatment. This is
falsifier (iv) of the pre-registration firing, not a missing result.

## 3. No off-switch: falsified in strong form, supported in weak form

**Design and sample.** We coded 38 pronatalist policy introductions (cash benefits, parental
leave, childcare packages, population-policy reversals) in 25 countries, each with fertility
below 1.6 at introduction — "saturated" countries where the framework says the policy cannot
work. Fertility is the 1960–2023 country-year panel (217 countries). The pre-registered bound
test asks how often fertility rises above 1.6 within ten years of an introduction; the
persistence test asks whether any country holds it above 1.6 for three or more consecutive
years.

**The bound test.** 34 of 396 post-introduction country-years are above 1.6 = **8.6% (one-sided
95% upper bound 11.3%)**. The pre-registered prediction was "below 10%": the point estimate
passes, the confidence bound does not. Ten of 38 events have at least one year above 1.6 within
ten years.

**The persistence falsifier fires.** Five of 38 events have three or more consecutive years
above 1.6 within ten years: Russia 2007 and 2011 (6 years, maximum 1.78), Czechia 2008 (3 years,
maximum 1.71), Estonia 2004 (5 years, maximum 1.72), Belarus 2007 (5 years, maximum 1.73).
Extending beyond the pre-registered window, **9 of 38** events ever have such a run, and the
longest is Bulgaria — 1.37 at introduction, ten consecutive years above 1.6 (2014–2023), still
1.81 in 2023. Romania held 8 years, Czechia 7, Russia 6, Estonia and Belarus 5, Latvia 4. **The
highest fertility reached after any introduction is 1.83**, and most crossings reversed.

**The average effect is small and not an income artefact.** An event study with country and
calendar-year fixed effects, first saturated introduction per country (467 country-years, 25
countries), gives an average post-introduction shift of **+0.035 births (SE 0.025; 95% CI −0.014
to +0.083)**. Power: the design detects **+0.070** at 80% power, so it rules out a sustained
average recovery larger than about +0.07 births; it cannot rule out smaller ones. Without
controls the shift is **+0.028 (SE 0.028)**; with the income cycle, urbanisation and net
migration controlled it is **+0.028 (SE 0.028)**; with country-specific trends it is **+0.017
(SE 0.010)**. The small positive shift is not an income, urbanisation or migration artefact.

**Descriptive and case evidence.** The maximum fertility in the ten years after an introduction
exceeds the five-year pre-mean by a median of **+0.15 births** (mean +0.18). Thailand, included
as a case because its 1997 reversal is outside the saturated set, went from 1.84 in 1997 to
1.73 in 2000, 1.56 in 2010 and 1.21 in 2023 — the reversal was followed by continued decline.

**What this section claims.** The strong form of the no-off-switch claim — that sustained
fertility above about 1.6 after pipeline-compatible policy does not occur — is **falsified**:
nine introductions were followed by three-to-ten-year runs above 1.6, and Bulgaria has been
above 1.6 for a decade. The weak form — that policy does not restore fertility toward
replacement — is **supported**: the maximum reached anywhere is 1.83, the average effect is
+0.035 (SE 0.025), and most crossings reverse. This is not a claim that "policies don't work";
it is a claim about how far, and for how long, they work.

## 4. The terminal enclosure as a critical transition: no early-warning signature

**Design and sample.** If the enclosure is a critical transition, its approach should be visible
as rising variance and rising lag-one autocorrelation in the fertility series during the 15
years before the fall. Using the pre-registered event rule (first year of the fastest sustained
ten-year fall of at least 1.0 births), 184 countries have a transition; **80** also have the full
pre-event window because annual series mostly start in 1960. For each, the same statistics were
computed at 200 pseudo-event dates drawn from its own series, never within ten years of the real
event, and compared within country.

**The signature is absent.** The lag-one autocorrelation trend before real events is **−0.025
(SE 0.008, t = −3.3)** relative to pseudo-events — the opposite sign to the prediction. The
variance trend is **+0.079 (SE 0.034, t = +2.3)**, the right sign, but it fails the pre-registered
surrogate null: re-shuffling and re-integrating the pre-event first differences 16,000 times
gives a share of **0.42** of surrogates with a trend at least as large. For autocorrelation the
surrogate share is **0.57**. Per the pre-registered rule the early-warning signal is absent,
and for autocorrelation it is not merely absent but backwards.

**Power is stated, not hidden.** With the observed dispersion the minimum detectable differences
at 80% power are **0.095 for the variance trend** and **0.021 for the autocorrelation trend**. The
variance effect (0.079) is below its own MDE, so that null is weak evidence of absence; the
autocorrelation null is not weak, because the point estimate has the wrong sign.

**Diminishing returns are real, but confounded with a floor.** On 3,865 country-years and 238
countries, ten-year fertility change on lower-secondary completion and its square gives a
positive squared term of **+0.00019 (t = 18.2)**, and marginal effects of **−0.0099** births per
point of completion at the 10th percentile (bootstrap 95% CI −0.0116 to −0.0079), **+0.0064** at
the median (0.0059 to 0.0070) and **+0.0214** at the 90th percentile (0.0199 to 0.0230), with a
turning point near 39 of 100. The pattern the framework predicts is present. The honest reading
is contaminated by arithmetic: once fertility is near its floor it cannot fall further, and a
concave response and a floor look the same in this regression. The result is quoted as a boundary
condition on the schooling–fertility relation, not as evidence of a ratchet.

## 5. What survives, what does not, and what this section does not claim

| # | prediction | pre-registered killing test | outcome | verdict |
|---|---|---|---|---|
| 1 | care-work loop amplifies the schooling–fertility link | income/urbanisation absorption; placebo sectors | absorption: +0.009 (t 0.17) once GDP (t 2.47) and urban (t 3.38) are in; placebos male +0.179 (t 2.10) and manufacturing −0.189 (t −3.47) larger than care; 36-spec curve takes both signs | **falsified** |
| 2 | strong no-off-switch: no sustained fertility above ~1.6 after policy | bound test; persistence; event study; rivals | 8.6% of post-introduction years above 1.6 (upper 11.3%); persistence fires 5/38 within 10y and 9/38 long-run (Bulgaria 10 years, 1.81 in 2023); event study +0.035 (SE 0.025), MDE 0.070, rivals +0.028 (0.028), trends +0.017 (0.010); max reached 1.83 | **falsified in strong form; weak form supported** |
| 3 | terminal enclosure is a critical transition with early warning | event vs pseudo-event; surrogate null; power | autocorrelation −0.025 (SE 0.008), wrong sign; variance +0.079 (SE 0.034) fails surrogate (0.42); diminishing returns +0.00019 (t 18.2) but floor-confounded | **no early-warning signature; diminishing-returns part survives as a boundary condition** |

**What survives.** The plain attainment channel — the cross-country association between female
schooling and fertility — is not challenged here; the framework's own data show tertiary
attainment correlating −0.62 with fertility (n = 46 in the credential section of the companion
paper), and it survives the controls that kill the care loop. The weak form of no-off-switch
also survives. And the diminishing-returns result is a real, precisely estimated feature of the
schooling–fertility relation, even if it cannot be separated from the floor.

**What this section does not test.** It does not test the framework as a whole. It tests three
mechanisms the framework says are load-bearing: a care-work loop, a policy-proof ceiling, and a
critical transition. Nulls on mechanisms are informative about the mechanisms; they do not
adjudicate the broad claim that credential pipelines shape fertility. The care loop is tested on
a cross-section of 148 countries with a coarse care sector; the no-off-switch test uses 38
hand-coded policy dates, approximate to the year, with no dedicated housing measure; the
critical-transition test has 80 usable events and cannot rule out a transition with no early
warning. Each null is therefore a scope-limited result. What the three tests do jointly is
remove the three specific causal props the framework offered; the broad framing can survive them
only by specifying different mechanisms, not by reasserting these.

**A note on framing.** This is a theory-testing exercise with pre-registered falsifiers, not a
takedown. The framework's broad claim — that the credential pipeline is central to fertility
decline — is consistent with the plain attainment channel reported in the companion paper. What
this section shows is that three mechanisms often used to make that claim causal do not hold up
against the data the framework itself specifies, and that the honest summary of the policy
evidence is narrower than "no off-switch": policies do not restore replacement-level fertility,
but they are neither inert nor incapable of lifting fertility above 1.6 for extended periods in
particular post-socialist contexts.
