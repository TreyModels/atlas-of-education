# PRE-DECLARATIONS — Loop 4 (U1 KOR fee test, U1b HK multi-moment OOS, U2 recovery/forced-ID, U3 holdout, U4 verdict)

Written BEFORE any loop-4 run. Scope `05b_experiments/loop4/`. Workers ≤ 2 (numpy-only),
`PYTHONDONTWRITEBYTECODE=1`, matched seeds 0..4, failures logged, no unrun cell claimed. All numbers
are stylized model output; only observed data cells are compared; no imputed cell used.

Standing context: loop 3's stop rule fired (stage-matched incidence FAILED 3/3). Incidence is therefore
**not a fitting target**. Loop 4 is an identification round.

## U1 — KOR-like variant: price/entry block vs verified Korean fee moments

**New data** (`04_data/shadow_round2/data/shadow_fees_round2.csv`, `shadow_incidence_round2.csv`):
KOR 2023 — average monthly private-education expenditure **434k won per student**, **553k per
participating student**; by level 462k (elementary), 596k (middle), 740k (high); hours 7.5/7.4/6.7
(all 7.3 h/week); participation 78.5% all (86.0 elementary, 75.4 middle, 66.4 high).
**Declared conversion** (fixed before running): annual fee = monthly ×12; income anchor = GDP per
capita (current US$) 36,238.6 in 2024 from `ECONOMY_SERIES.csv`, converted at a declared
**1,330 KRW/USD** (2023–24 average, declared). Observed annual fee/income ratios: per student
**10.8%**, per participant **13.8%**, by level 11.5% / 14.9% / 18.4%.
**Model.** KOR-like config in the loop-3 structural shadow module (`loop3/code/shadow3.py` static
market: demand by stage × urban/rural; commercial + teacher-tutor supply at unit cost; teacher capacity
limited). KOR parameters declared: income numeraire 1.0 (= GDP pc), urban 0.81, public-school substitute
0.60, gate stakes elementary 0.7 / middle 0.9 / high 1.3, credential returns 0.4/0.6/0.9, provider cost
multiplier 2.4 (high-wage providers; declared wage-index scaling), F_cm=4.5, F_tt=0.6, cap_cm=0.08,
cap_tt=0.035, teacher capacity 0.30, enrolment shares 0.42/0.30/0.28. **No parameter is set to a fee
moment.**
**Estimands.** Model annual fee/GDP-pc ratio (per student and per participant) vs observed 10.8%/13.8%;
participation by stage vs 78.5/86.0/75.4/66.4 (all/elementary/middle/high); hours → **UNABLE** (the
module has no hours object — declared).
**Threshold (predeclared).** U1 PASS iff the model per-participant fee/income ratio lies inside
**[10.5%, 18.5%]** (the observed by-level band) AND the per-student ratio lies inside **[9.5%, 16%]**;
participation is reported descriptively (within ±15 pp of 78.5% = "level plausible", else "under/over");
otherwise U1 FAIL (price block declared unusable for KOR).
**Prediction before running.** Price ratio should land ~12–14% (inside the band) because the declared
KOR provider-cost scaling is high; participation will likely be under-predicted (demand intercept is not
KOR-calibrated). If so the verdict is "price block usable, demand block not identified for KOR".

## U1b — HKG multi-moment out-of-sample check (the one check that can rescue a single-country claim)

**New data** (`04_data/shadow_round2/data/shadow_incidence_round2.csv`; Bray & Kwok 2003, peer-reviewed,
Table 1 p.616, 6-school quota sample n=630, 1998/99): stage participation **S1-3 35.1%, S4-5 46.6%,
S6-7 70.3%, all-secondary 48.8%**; provider mix **commercial large-scale mass-lecture classes 72.4% at
S6-7, 33.0% at S4-5**; multi-provider 12.3/29.4/19.8. Fee moments (1998/99): 28.1% >HK$1,000/month,
8.5% >HK$2,000; **fees 1.1–5.0% of household monthly income**; modal 6–10 h/month.
**Design.** Start from the HKG-like config, **calibrate the provider/demand block to the 2010
senior-secondary 85% only** (the existing single calibration; one common demand intercept shift, solved
by bisection). Do **not fit** the 1998/99 rows. Derive the 1998/99 config by declared time-trend
factors (fixed before running): gate stakes ×0.70, credential returns ×0.75, public-school substitute
0.85, income ×0.78 (HK GDP pc ratio 1998/2010), provider cost multiplier ×0.9. Map S1-3→lower,
S4-5→middle, S6-7→senior stages.
**Estimands.** Model 1998/99 gradient at the three stages; monotonicity and rank correlation with the
observed gradient; model fee/income ratio vs the observed 1.1–5.0% band; model commercial mass-lecture
share by stage (declared provider rule: teacher-tutor capacity is allocated to the highest-stakes stage
first; commercial providers serve the remainder, so commercial share should rise with stage) vs observed
72.4% (S6-7) and 33.0% (S4-5).
**Threshold (predeclared).** U1b PASS ("single-country check") iff (i) model 1998/99 take-up is strictly
rising across S1-3 < S4-5 < S6-7, (ii) each stage is within **±15 pp** of the observed value, (iii)
commercial mass-lecture share is higher at S6-7 than S4-5 with a gap ≥20 pp, and (iv) model fee/income
ratio lies inside the observed **1.1–5.0%** band. If (i) and (iii) hold but (ii) or (iv) fail: **shape-only,
incidence claim stays withdrawn for all countries**. If (i) fails: **FAIL**.
**Prediction before running.** The gradient shape should pass (stakes rise with stage). Levels are likely
low at the bottom stages because the 2010 calibration was to senior only, so U1b may come out shape-only.

## U2 — recovery with truths outside the candidate set + forced-identification rate (L2-4)

**Design.** A declared two-channel identification model (NOT the full ABM): candidate worlds
EDUCATION_LED (ed=0.8, ec=0.0), DEMAND_LED (0.0, 0.8), COMPLEMENTARY (0.6, 0.6). Truths **outside the
candidate set**: COMMON_SHOCK (ed=ec=0, common shock γ=0.9) and OPPOSITE_SIGN (ed=ec=−0.6). Data per
truth: two policy arms (schooling push S=+1; demand push D=+1) and a placebo arm (no push), outcomes
Δjobs and Δattainment with seed noise σ=0.30; seeds 0..4 (20 simulations per truth = 4 seeds × 5 noise
draws, declared). Estimator (declared): difference-in-differences vs placebo — êd = Δjobs_S −
Δjobs_placebo, êc = Δattain_D − Δattain_placebo; classify by threshold |ê| ≥ 0.25 (with a 2·seed-sd
significance check): both → complementary; only êd → education-led; only êc → demand-led; neither → none.
**Estimands.** Recovery = share of candidate-truth simulations correctly classified; forced-ID = share of
outside-truth simulations classified as any candidate. Also report the **no-placebo** variant (forced-ID
when common shocks cannot be netted out).
**Threshold (predeclared).** Claim identification iff **recovery ≥ 0.67 and forced-ID = 0**; otherwise
report the negative. **Prediction:** with the placebo estimator, recovery should be high and forced-ID
low for COMMON_SHOCK; OPPOSITE_SIGN should classify neither. Without a placebo, COMMON_SHOCK will force a
candidate → we expect the no-placebo forced-ID to be 1.0.

## U3 — holdout: fit 1980–2010 PH/KHM completion, test 2011–2024 (L2-5)

**Data.** `04_data/data/gmr_observed_6countries_1970_2024.csv` observed upper-secondary completion:
PHL 1999–2024 (11 obs); KHM 1996–2023 (18 obs). HK has no completion observation → UNABLE.
**Model.** loop-2 two-way module (`loop2/code/twoway.py`, `R3_complementary`), horizon extended to
60 years so t=0 ↔ 1965 and t=59 ↔ 2024; model completion path s_t. **Fit one parameter only:** a
multiplier on s0 (grid 0.40–1.60 step 0.02), chosen to minimise RMSE on the fit window (PHL 1999–2010,
6 obs; KHM 1996–2010, 8 obs). **Holdout:** PHL 2011–2024 (5 obs), KHM 2011–2023 (7 obs). Naive benchmark:
carry the last fit-window observation forward.
**Threshold (predeclared).** U3 PASS for a country iff held-out MAE ≤ **5.0 pp** AND held-out MAE < naive
benchmark MAE; else "no country claim" for that country. Report in-sample RMSE vs held-out MAE.
**Prediction.** The module was not built to fit country completion paths; one free parameter is likely
insufficient → expect FAIL (no country claim), which is the honest test.

## U4 — publishable verdict

No new compute. Using loop-3 S1–S3 and U1–U3: state the exact claim the model can support and the claim
it cannot; identify the publishable object (negative/identification map + provider economics + data-first
program). Every unrun or UNABLE item is named.

## Failure rule

Any failed run is logged and excluded with counts reported. Cells not executed are marked `not run`.

---

## Amendment L4-1 (declared before running; lead update with improved anchors)

**U1 is now calibrated on the KOR official 2023 anchors, not only 78.5%.** Predeclared U1 procedure:
calibrate ONE common demand intercept so model all-levels participation = 78.5% (the official anchor),
then CHECK (without further fitting): by-level participation ordering and levels vs official 86.0
(elementary) / 75.4 (middle) / 66.4 (high); spend per student/per participant vs the official ratios;
provider mix: commercial share of capacity vs the official hagwon share of expenditure 241/434 = 55.5%;
hours 7.3 h/week = **UNABLE** (no hours object in the module; declared, not fitted away). The fee
thresholds are unchanged: per-participant ratio inside [10.5%,18.5%] and per-student inside [9.5%,16%]
=> price block usable; otherwise unusable. By-level participation is descriptive (pass if ordering and
levels within ±15 pp, else reported as a demand-block failure).
**Anchors declared as calibration/check set:** Korea 2023 official (calibration + checks); Japan grade-6
41.8 (check; no JPN variant → UNABLE); HK 2003 (U1b checks); China 2014 29.8 and post-2021 <20% and
Cambodia case-study bounds (not used in loop 4 cells); PH blocked. Korea 2011 "90%" is NOT used (not
traceable).
