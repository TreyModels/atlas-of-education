# Pre-registered protocol: Philippines calibration and test

Written 2026-11-21 15:27 UTC, before any parameter was fitted. Not edited after the first fit. Amendments go
at the end, dated, with the reason, and never change a test that has already been scored.

**Honest status of the test.** The 1996–2024 World Bank series were downloaded, and seen, in the same session
that built this model. No parameter has been fitted to them, and the fitting code cannot read them (it
receives only training rows; `tests/test_protocol.py` checks this). This is therefore a **retrospective
holdout, not a blind test**. It is the strongest test available without waiting for new data.

## 1. Fact to explain (Gate 1)

Philippine participation expanded in a particular order:
- Primary was near universal by 1971 (GER about 97–106).
- Secondary rose from GER 44 (1971) to about 70 (1990) and about 80 (2009), with a jump around 1988–90.
- Tertiary rose from 16 (1971) to about 25 (mid-1980s), sat near 27 for twenty years, rose in the 2010s, fell
  with the K-12 transition (2017–18), then climbed to 47 (2024).
- The private share of tertiary enrolment fell from 79% (AY1984-85) to about 54% (2015–20).

Second sources: CHED headcounts for 2015–2020 confirm the K-12 tertiary fall (−27% from AY2015-16 to
AY2017-18) and give the private share. **The sources disagree for 2015**: CHED Table 1 gives 54.1%, and a
UP CIDS paper gives 48%. CHED is preferred where both exist.

## 2. Rivals (Gate 2)

Demand side. The model structure is the same in each; only the demand term differs.
- **D1 income:** families keep children in school more as household income rises, so participation follows
  real income per head, including its falls (`demand_form='income'`).
- **D2 smooth diffusion:** the wish for schooling spreads as a smooth trend, independent of the economic
  cycle. The trend has the same average slope over 1971–1995 as log income (`demand_form='trend'`).
- **D3 no demand growth:** only cross-sectional income differences and costs; any expansion comes from cost
  policies and supply (`demand_form='none'`).

Supply side, tertiary public places:
- **S1 fiscal:** public places grow with real income per head.
- **S2 trend:** public places grow at a fitted constant rate.
- **S3 responsive:** public places grow in response to unmet public demand (applicants turned away).
- **S4 unconstrained:** no rationing of public places.

## 3. Separating observations (Gate 3), written before running

1. **Recessions.** GDP per head fell about 18% in 1983–85 and stalled in 1998. D1 predicts dips in
   secondary and tertiary GER in 1984–87 and around 1998–99; D2 and D3 do not.
2. **The 2010s acceleration.** GDP per head grew faster after 2010 than in 1971–1995. D1 predicts faster
   GER growth in 2010–2016 than D2.
3. **The tertiary private share** (2000, 2015–2020, never used in fitting) separates S1–S4. S4 predicts a
   share set only by preferences and costs; S1–S3 differ in how fast public places grew.
4. **The K-12 transition** (2017–2019) is not fitted. Every rival should reproduce a tertiary fall, because
   the cycle change is structural. Its size and recovery test the age-band and cohort accounting.

## 4. Training data and fitted parameters (Gate 4)

Training years: 1971–1995. Targets:
- WDI primary, secondary and tertiary GER;
- primary NER;
- primary private share;
- tertiary private share for 1985 only.

Loss: sum of squared errors in percentage points. Each series is weighted by 1/(number of its training
observations), so every series counts equally (indicator-balanced).

Fitted parameters (11): `eta, kappa, a_prim, a_sec, a_sec_entry, a_ter, a_ter_entry, mu_basic, mu_ter, nu,
k_ter`, plus `k_growth` (S2 only) and `k_resp` (S3 only).

Fixed, declared in `docs/assumptions.md`:
- cost shares by level and sector;
- policy cost changes;
- repetition 4% primary and 2% secondary;
- late entry 15%;
- the entry-age ramp.

Because 11 is more than five, a **recovery test** is required: synthetic data generated from known
parameters, with noise matching the training residuals, must be refitted. Recovery is accepted if every
behavioural parameter that the rivals turn on (`eta`, `kappa`) is recovered within ±25% in at least 80% of
20 replicates.

## 5. Test data (never used in fitting)

- WDI GER for all three levels, 1996–2024;
- primary NER 1996–2017;
- secondary NER 1996–2015;
- secondary private share 1998–2020;
- primary private share 1996–2020;
- tertiary private share 2000 and 2016–2020 (CHED);
- CHED tertiary headcount change from AY2015-16 to AY2017-18 and to AY2019-20;
- DepEd 2018-19 JHS and SHS private shares;
- APIS 2019 richest/poorest participation ratios (direction and rough size only).

## 6. Benchmarks (Gate 5)

On every test series the model must beat both naive rules on RMSE:
- **N1 persistence:** last training-year value carried forward;
- **N2 linear trend:** an OLS line through the 1971–1995 training points, extrapolated.

A loss is reported as a loss, first.

## 7. Decision rules

- The demand rival with the lowest test RMSE averaged over the three GER series is preferred, but only if it
  also beats D2 on separating observation 1. Otherwise demand is reported `not identified`.
- The supply rival with the lowest error on the test tertiary private shares is preferred, unless all are
  within 3 pp of each other, in which case supply is reported `not identified`.
- Status words follow Trey Menefee's GATE.md:
  - `calibrated` only if the model beats N1 and N2 on most test series;
  - otherwise `fitted + free residual` or `illustrative`.

## Amendments

**A1 · 2026-11-21 15:40 UTC.** The first full fit (D1 income demand, S1 fiscal supply) was scored and archived
unchanged in `outputs/scored/v1_first_scored_*.json`. It **lost to the persistence benchmark** on every GER
series. In that fit the cost coefficient `kappa` sat at its upper bound (10). This is a training-side
problem, so the bound is widened to 40. Nothing else in the model, the targets or the decision rules
changes. All rival fits below use the widened bound. The v1 numbers stay in the record.

**A2 · 2026-11-21 16:05 UTC (after the rivals were scored).** All six pre-registered rivals were fitted and
scored, and the results are archived unchanged in `outputs/PHL/v1/` as the pre-registered result. Two
problems were found.

- **Training side:** several intercepts and the private income slope sat at their bounds, in every rival.
- **Test side:** the 2019 richest/poorest participation ratios came out absurd (tertiary about 4×10^10,
  against a survey ratio of 2.6).

Both point to the cost term `kappa * cost/income`. It is so steep that the fit shuts out the poorest deciles
and pushes intercepts to their limits to keep the richest near 100%. v2 replaces it with the graded,
concave `kappa * ln(1 + cost/income)` and widens the intercept bounds. The rivals, targets, benchmarks and
decision rules are unchanged.

**Consequence: the v2 test is not a clean holdout.** The functional form was changed after test results
had been inspected. v2 results are labelled **test inspected**, and v1 remains the pre-registered result.

**A3 · 2026-11-21 16:35 UTC (after v2 was scored).** v2 still produced absurd richest/poorest ratios. The
cause is structural, not the cost form. One coefficient, `eta`, governed both:
- the rise of participation over time as national income grew; and
- the gap between rich and poor households at a point in time.

The training years need a large time effect. The 2019 survey shows a shallow cross-sectional gap: about 1.3
to 1.5 log-odds between the poorest and richest deciles at secondary and tertiary level. One coefficient
cannot do both, so the fit shut out the poorest deciles.

v3 therefore:
- **Splits the coefficient** into `eta` (time: national income, or a trend, or nothing, by rival) and
  `eta_x` (cross-section: decile income relative to the mean).
- **Moves the 2019 APIS richest/poorest ratios from test to calibration.** They are the only observation
  that pins `eta_x`. The move is dated in the facts register and never reversed.

The rivals now differ only in the time term. The remaining test set is section 5 minus the gradient. v3 is
also **test inspected**.

**This is itself a finding:** in the Philippines, participation rose over time far faster than the
cross-sectional income gradient would imply.

**A3 note.** The de-duplication of tertiary private-share sources was meant to prefer CHED Table 1. In
2019 it kept the PIDS figure (53.0%) instead of CHED's 52.7%, because both source strings contain "CHED".
This is fixed for v3 scoring. The effect on the v1 and v2 scores is under 0.1 pp RMSE.

**A4 · 2026-11-22 (after v3 was scored).** The v3 fit misses the primary private share inside the training
years themselves. The model falls from about 8.6% to 4.4% while the data rise from 4.9% to 7.6%. The
private-choice income slope `nu` sat at its lower bound (−2).

**Diagnosis.** One slope served both basic and tertiary education. The primary private share rose with
income, and the tertiary private share fell, so the fit compromised on a negative slope. That compromise
also flatters the `unconstrained` supply rival on the tertiary private share.

**Change.** v4 gives tertiary its own slope (`nu_ter`) and widens the slope bounds. The rest is unchanged.
**Motivation:** the visible training-period misfit. v4 is still **test inspected**.

**A5 · 2026-11-22 (after v4 was scored).** v4 lowered the training loss for four of the six rivals but made
held-out performance worse. The preferred rival (income demand, unconstrained supply) beats both naive
benchmarks on 1 of 7 series, against 3 of 7 in v3. One v4 fit (income/fiscal) ended at a higher training loss
than the v3 fit it nests, which shows the optimiser can stop at local optima. **v3 is therefore the reported
specification.** This choice was made after the test results were seen, and it is flagged as such in every
results table. The recovery test and the Cambodia port use v3. Cambodia uses the Philippine-preferred supply
rule (`unconstrained`), fixed before any Cambodian fit.
