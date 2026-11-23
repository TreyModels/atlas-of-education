# Part 3 — Pre-registered experiment plan (designs, not results)

All designs below are written to be frozen before their data are touched: each names the estimand in plain words,
the result that would kill the mechanism, a power/minimum-detectable-effect (MDE) statement, and the data gap.
"Have" = already in the project (server or repo); "need" = public data to acquire; "new" = would have to be collected
or constructed by us. MDEs are 80% power at 95% two-sided, i.e. 2.80 × the standard error of the estimate, unless
stated otherwise; they are anchored on the standard errors actually observed in the 380-link matrix (u5mr → fertility
se 0.0011, life expectancy → fertility se 0.0078, both with country trends; n = 8,567 and 9,266 country-years,
193-210 countries).

---

## E1 — Level versus volatility of child mortality (the only fully separable country-level test)

**Question.** Does fertility respond to the *level* of child mortality or to its *volatility/uncertainty*?

**Design.** Build annual child-mortality series (1960-2024, already in the panel). For each country decompose into
(a) a slow trend (decade means, or local linear trend), and (b) residuals. Build a 5-year volatility measure (rolling
standard deviation of residuals over 5-10 years, lagged so it is known before the fertility window). Regress the
ten-year change in births per woman on the trend level and the lagged volatility jointly, with country effects, decade
effects, logged income and urbanisation, with and without country trends, clustered by country. Report the two
coefficients and their difference. Also run the reverse decomposition for life expectancy.

**Data.** Have: annual child mortality and total fertility (panel, observed arm; box2 `/root/work/data`, migrated copy under
`/root/autodl-tmp/migrated/`). Need: nothing.

**Estimand.** The difference in births per woman over the next ten years caused by a one-unit higher mortality *level*
versus a one-unit higher mortality *volatility*, holding the other fixed.

**Falsifier.** If volatility carries a large positive coefficient and the level coefficient collapses towards zero,
the insurance/uncertainty channel wins and pure replacement/quantum is ruled out. If volatility is ~0 and the level
coefficient is unchanged, the uncertainty channel is dead and the association must be replacement, tempo, quantity-
quality, life-history or common cause.

**Power / MDE.** Level MDE 0.0031 births per 1,000 child-mortality points (observed effect 0.0060, ~1.9× MDE).
The volatility regressor is noisier; assuming its standard error is 1.5-2× the level's, the MDE is 0.005-0.006 —
i.e. we can only detect a volatility effect about as large as the level effect. A volatility effect a quarter that
size would be missed.

**Failure mode.** Volatility is measured with error and correlated with the level and with income shocks; the
mortality series is itself modelled by international agencies. A null on volatility is therefore weak evidence.

---

## E2 — Replacement versus insurance in birth spacing after a child death (highest identification value)

**Question.** When a child dies, do parents have a replacement birth sooner (replacement), or do they have extra
births in anticipation of losses (insurance/hoarding)?

**Design.** DHS/WFS birth histories, parity-specific discrete-time hazard of a subsequent birth. Key regressors:
death of the previous child, death of earlier children, parity, mother's age, education, wealth, urban/rural, survey
fixed effects, country fixed effects. Distinguish the two mechanisms by (i) timing — replacement responds to an
actual death, insurance predicts higher fertility *before* any death in high-risk settings; (ii) target — replacement
responds to death of the *most recent* child most strongly; (iii) parity — replacement is stronger at higher parities.
Also estimate the "insurance" signature as the response to the child's *predicted* mortality risk (age, sex, region,
epidemic year) before any death. Use 12-, 24- and 36-month windows to allow slow replacement.

**Data.** Need: DHS birth-history microdata (public, ~90 countries, 1985-2024, typically 5,000-30,000 births per
survey; requires registration and extraction). Have: nothing individual-level yet.

**Estimand.** The change in the probability of a subsequent birth within 24 months after a child death, in percentage
points, by parity — compared with the same probability for a surviving child of the same age, sex and family.

**Falsifier.** If there is no household replacement response at all (hazard unchanged) while the country-level
association is strong, the aggregate correlation cannot be household replacement: it must be insurance, tempo,
quantity-quality, life-history or common cause. If replacement exists but is tiny (e.g. <10% of the implied aggregate
effect), same conclusion.

**Power / MDE.** With about 2,000 death-exposed birth intervals and 18,000 unexposed, a 30% subsequent-birth rate
gives an MDE of about 3 percentage points (≈10% relative) at 80%/95%. Policy-relevant replacement responses
(typically 10-30% relative) are detectable.

**Failure mode.** Deaths are correlated with unobserved maternal health and with poverty; survivor and recall bias;
misreported birth histories; replacement may take longer than 36 months.

---

## E3 — Tempo versus quantum: does longer life change when births happen or how many?

**Question.** Does the life-expectancy link operate by shifting the timing of births or by reducing completed family
size?

**Design.** Age-specific fertility by 5-year age group (UN WPP), 1960-2024. Compute (a) completed cohort fertility
(quantum proxy), (b) mean age at childbearing (tempo), (c) the Bongaarts-Feeney tempo-adjusted period TFR. Run the
matrix design (ten-year change on starting level, country and decade effects, income logged, urbanisation, with and
without country trends) on each outcome against life expectancy and child mortality. The comparison of the tempo
component with the quantum component is the test.

**Data.** Need: UN WPP age-specific fertility tables (public). Have: total fertility only.

**Estimand.** The effect of one more year of life expectancy on completed births per woman versus on mean age at
childbearing (years) — and how much of the raw TFR response survives tempo adjustment.

**Falsifier.** If the raw association is entirely tempo (completed family size unchanged, only ages shift), the
longevity channel is a timing phenomenon and "life expectancy lowers fertility" must be restated. If completed family
size falls, it is a quantum effect and needs a quantity mechanism.

**Power / MDE.** Age-specific rates are model-smoothed and precise; MDE for the tempo component about 0.05 years of
mean age and for the quantum component about 0.02 births per woman. This design is well powered.

**Failure mode.** Completed cohort fertility is observed only for cohorts that have finished childbearing, so the
newest period is projected; the dose model's "mostly quantum" result depends on weights that are being fixed and must
not be leaned on.

---

## E4 — Within-country mortality shocks as natural experiments

**Question.** Does an *exogenous* fall in child mortality cause fertility to fall?

**Designs, in order of identification strength.** (a) Vaccination/measles campaign rollouts; (b) antimalarial
campaigns, bed-net distribution, indoor residual spraying; (c) oral rehydration therapy rollout; (d) epidemics
(1918 influenza, COVID) and famines; (e) conflict (the DRC conflict paper is the template). Common design: staggered
event-study difference-in-differences, country and year effects, country-specific trends, clustered errors; first stage
= campaign → child mortality; reduced form = campaign → births; ratio = causal effect under monotonicity.

**Data.** Have: our country panel. Need: campaign rollout timing and intensity (WHO/UNICEF/WUENIC coverage, AidData,
DHS/MICS coverage modules, national programme documents) and, where relevant, subnational data.

**Estimand.** The change in births per woman (and in the next-birth hazard where micro data exist) in countries/years
exposed to a mortality-reducing campaign, relative to unexposed comparisons.

**Identifying assumptions.** Parallel trends absent the campaign; campaign timing unrelated to fertility trends;
campaign not targeted on the basis of fertility (or targeted on it in a way we can model).

**Falsifier.** If campaigns cut child mortality strongly (first stage) but fertility does not move, or moves only
after more than a decade, household replacement is not the channel and the common-cause rival gains. If the reduced
form is present only where state capacity also rose, common cause is supported.

**Power / MDE.** A campaign that cuts child mortality by 10 points per 1,000 implies, at our matrix coefficient, a
fall of about 0.06 births per woman. A typical country-year DiD standard error on births is 0.02-0.05, so the MDE is
about 0.06-0.14 births: **only large campaigns are detectable**, and a 10-point mortality reduction is at the edge of
power. Needs many campaigns or subnational variation to be viable.

**Failure mode.** Campaign rollout is correlated with state capacity (the common-cause rival) — a positive result is
not clean evidence; a null is informative. Campaign intensity data are poor and often self-reported.

---

## E5 — Quantity-quality interaction: does the mortality link weaken where schooling pays more?

**Question.** Does the child-mortality → fertility link weaken where the returns to education are high?

**Design.** Estimate the matrix mortality → fertility link separately (and with an interaction) for countries grouped
by the return to schooling (wage premium / Mincer returns; Psacharopoulos-Patrinos style global returns), or by the
human-capital stock. Three groups (low/middle/high returns) with country and decade effects, same controls.

**Data.** Need: a country-year returns-to-education dataset (public, Patrinos/Psacharopoulos updates; or estimate
wage premia from survey microdata). Have: the fertility/mortality panel.

**Estimand.** The difference in the mortality → fertility coefficient between high-return and low-return countries
(births per woman per point of child mortality).

**Falsifier.** If the coefficient is the same across education-return strata, the quantity-quality/human-capital
channel does not modulate the link and the association is more likely replacement/insurance/life-history/common cause.
If the link is *stronger* where returns are high, the quantity-quality story is in trouble (it predicts weaker).

**Power / MDE.** An interaction standard error is typically 1.4-1.7× the main standard error; with a main se of
0.0011 the MDE for the difference is about 0.006-0.007 — as large as the entire main effect. This design is
**underpowered** unless the strata are large or the returns measure is very precise.

**Failure mode.** Returns data are sparse, noisy and endogenous to fertility; misclassification biases the
interaction towards zero.

---

## E6 — Extend the individual-level dose model with explicit survival and longevity channels

**Question.** Which micro-specification reproduces both our country-level patterns and the micro facts (replacement
response from E2, tempo/quantum from E3, age at first birth from E4)?

**Design.** Add to the dose model: (i) child-survival channel — probability a birth survives to age 5, with a
volatility term; (ii) adult-longevity channel — horizon over which parents evaluate returns; (iii) a quality choice
responding to survival. Estimate four nested specifications (replacement-only; insurance/volatility; quantity-quality
with survival; life-history/timing). Calibrate non-testable parameters, estimate the channels that E2/E3 identify, and
confront each specification with the full set of country links plus the micro moments. Pre-register which parameters
are fixed from outside evidence and which are estimated.

**Data.** Have: the dose model code and country panel. Need: micro moments from E2/E3 as calibration targets.

**Estimand.** The model-implied response of births to a mortality decline, compared with the country-level coefficient
(0.006 births per point of child mortality; −0.048 per year of life expectancy).

**Falsifier.** Any specification that reproduces the country facts only by implying a replacement response smaller or
larger than E2 actually finds, or a tempo response outside E3's estimates, is rejected. If all four specifications can
be calibrated to fit the country facts, the country facts cannot identify the mechanism and the model must be tested
on new micro moments, not on the matrix.

**Power.** Not a sampling-power question but an identification one: with a single country-level moment and four
mechanisms, the model is under-identified. The design is only valid with at least three independent micro moments.

**Failure mode.** The dose model's weights are being fixed and should not be leaned on; flexible models with several
channels can fit the same aggregate facts (observational equivalence inside the model).

---

## E7 — The common-cause test: is the association a public-health/state-capacity artefact?

**Question.** Does the mortality-fertility association survive when public-health infrastructure and state capacity
are accounted for, and when mortality is moved by factors unrelated to fertility preferences?

**Design.** Two arms. (i) Add public-health/state-capacity controls (vaccination coverage, health spending, DPT/measles
coverage, government effectiveness) to the matrix link — interpret cautiously because these are also mediators.
(ii) Use technology-diffusion instruments: the global introduction dates of vaccines, ORS, antibiotics, and campaign
rollouts as sources of mortality change unrelated to any single country's fertility demand; compare the fertility
response to mortality changes driven by these instruments versus the raw link.

**Data.** Need: vaccination coverage (WUENIC), health expenditure, government effectiveness (WGI), programme
documents. Have: the fertility/mortality panel.

**Estimand.** The mortality → fertility coefficient with and without state-capacity controls, and the instrumented
response of fertility to mortality changes driven by health-technology diffusion.

**Falsifier.** If the coefficient collapses to zero once state capacity is controlled, or the instrumented mortality
change does not move fertility, the common-cause rival wins and the whole mechanism family loses its causal footing.
If it survives both, the family survives (though replacement/insurance/tempo remain entangled).

**Power / MDE.** Controls are highly collinear with mortality; the MDE inflates to 0.008-0.010 (i.e. 1.5-2× the main
effect). Weak instruments would make the design uninformative rather than null.

**Failure mode.** Controls are post-treatment mediators — a falling coefficient is *not* evidence against the
mechanism; and country-level state-capacity measures are too coarse to separate from mortality itself.

---

## Ranking, and what would kill the whole family

**Pre-registered ranking (by identification value per unit of cost):**
1. **E1** (level vs volatility) — nearly free; data in hand; the only mechanism fully separable with country data.
2. **E2** (replacement vs insurance) — highest identification value; public data but real preparation cost.
3. **E4** (mortality shocks) — the causal test; expensive and likely underpowered at country level.
4. **E3** (tempo vs quantum) — cheap once WPP age-specific data are pulled; clarifying rather than decisive.
5. **E5** (quantity-quality interaction) — cheap but underpowered.
6. **E6** (dose model extension) — only after E2/E3 provide moments; otherwise under-identified.
7. **E7** (common cause) — the most important rival but the hardest; needs the technology-diffusion instruments.

**Run first: E1.** It costs almost nothing (all data in hand), it is pre-specifiable, and its falsifier decides whether
the uncertainty/insurance channel is worth the DHS investment in E2. If E1 finds no volatility response, E2 becomes the
single highest-value study and should start immediately; if E1 finds one, E2's design must include the volatility
margin from the start.

**Falsifying the whole mechanism family.** The family fails if, jointly: (a) fertility responds to neither the level
nor the volatility of child mortality in E1; (b) there is no household replacement response in E2; (c) exogenous
mortality-reducing campaigns move mortality but not fertility in E4; and (d) the country association collapses when
state capacity or health-technology instruments are used in E7. Any one of these is diagnostic; all four together would
mean the mortality-fertility association is a development artefact, not a survival mechanism.
