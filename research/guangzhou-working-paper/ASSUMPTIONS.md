# Guangzhou education simulation: assumptions and data dictionary

This document describes the synthetic-pupil model in `gz_v5.py` and the parameter design used by `sweep.py` and `repeats.py`. The model is a scenario simulator, not a forecast or a reconstruction of an observed Guangzhou cohort. Its outputs are conditional on the mechanisms, parameter ranges, and proxies below.

## How to read the inputs

The sweep draws 31 parameters independently from uniform ranges in `ranges.json`; it does not use empirical joint distributions or encode correlations between uncertain assumptions. The archived v8 sweep used a Latin hypercube. The new sweep uses independent uniform draws. For every draw, `TEACH_SD` is also assigned to `HS_TEACH_SD`. Each result simulates 40,000 pupils. `repeats.py` independently samples 128 parameter settings and simulates each under eight cohort seeds to examine seed-to-seed variation; it compares the baseline with a counterfactual that sets `BAN_RED=0` and turns re-banding off.

Unless indicated otherwise, score and skill quantities are in standard-deviation (SD) units. Shares are fractions of the stated denominator. Wealth is a standardized latent log-wealth index unless a yuan amount is shown. “Official,” “literature,” “informant,” “assumed,” and “unknown” are the evidence labels in the parameter register, not ratings of causal validity.

## Swept parameters

Ranges and defaults below come from `ranges.json` and `PARAMETER_REGISTER.md`. The model’s defaults are reference values; sweep outputs draw values from the ranges.

| Input | Meaning and operationalization | Sweep range; default | Units and evidence / uncertainty |
|---|---|---:|---|
| `TAL_WEALTH` | Correlation between latent talent and log wealth. | 0–0.30; 0.10 | Correlation; assumed. |
| `TEACH_SD` | SD of teacher effects in junior schools; copied to `HS_TEACH_SD` for high schools. | 0.15–0.45; 0.20 | SD units; literature range cited in register is 0.17–0.50 SD. |
| `TEACH_ZONE` | Junior teacher-quality gradient per SD of zone wealth. | 0–0.25; 0.10 | SD per SD of zone wealth; assumed. |
| `HOME` | Home-input contribution to initial skill per SD of log wealth. | 0–0.30; 0.15 | SD per wealth SD; assumed and identified as a key driver. |
| `DECAY` | Fraction of the pre-gate “head start” that fades by the later high-school stage. One common fade rate applies to home, junior-school teacher, and pre-gate tutoring components. | 0–0.90; 0.50 | Fraction; unmeasured and flagged as highly influential. |
| `SCHOOL_VA` | School value added per regular tier; elite tier receives twice this amount in the code. | 0–0.50; 0.10 | SD; literature range of 0–0.20 widened to 0–0.50. |
| `ZB_FLOOR` | Minimum score threshold for zhibiao eligibility, expressed as the top fraction of the full synthetic cohort. | 0.20–0.40; 0.30 | Share; assumed, described as consistent with 2026 rules. |
| `TOP_TEACH` | Teacher premium assigned to pupils in a high-school top band. | 0.20–0.40; 0.30 | SD; one-county magnet-class evidence; paired with `PEER` to approximate a 0.435 SD total. |
| `PEER` | Peer premium assigned to pupils in a top band. | 0.05–0.25; 0.14 | SD; one-county magnet-class evidence; paired with `TOP_TEACH`. |
| `ZHIBIAO` | Fraction of the model’s elite-seat pool reserved for school-based zhibiao allocation, among local-hukou eligible academic pupils. | 0.30–0.60; 0.50 | Share; official-rules motivated, but the sweep includes values below the stated 50% minimum (see rule mismatch below). |
| `NONHUKOU` | Fraction of the synthetic cohort without local hukou. | 0.10–0.40; 0.20 | Share; unknown. |
| `QUOTA` | Maximum non-hukou fraction used for public academic seats and, separately, for the elite tier. | 0.08–0.20; 0.15 | Share; rules cited as 8–15% core districts, 8–18% outer districts, and 8–20% from 2027. The sweep reaches beyond the stated 2026 outer-district upper bound. |
| `MINBAN_PEN` | Junior-school teacher-quality penalty for non-hukou pupils, standing in for minban or purchased-place schooling. | 0–0.30; 0.15 | SD; assumed; register cites private-school VA near zero. |
| `NH_WEALTH` | Additive mean wealth shift for non-hukou families. | −0.60–0; −0.30 | Wealth-index units; assumed. |
| `NOISE` | SD of exam measurement noise, used at zhongkao, interim high-school observation, and gaokao. | 0.25–0.50; 0.35 | SD; assumed. A common magnitude is reused across exams. |
| `ACAD` | Share of cohort initially assigned a public academic-track place before private/exit handling. | 0.45–0.65; 0.65 | Share; informant estimate about 50%, with earlier 60–70% figures also cited. |
| `PRE_SHARE` | Wealth-weighted probability scale for pre-gate tutoring absent the ban. | 0.20–0.60; 0.40 | Share scale; informant evidence and CIEFR 2017 survey (36%) cited. |
| `BAN_RED` | Fraction of pre-gate tutoring removed by the 2021 ban. | 0–0.60; 0.40 | Fraction; informant evidence and CIEFR comparison (36.1% to 13.5%) cited. |
| `PRE_EFF` | Initial-skill gain for a pupil taking pre-gate tutoring. | 0–0.30; 0.15 | SD; literature range described as mixed, zero to about 0.15. |
| `REBAND_PERF` | Weight on observed senior-1 performance versus zhongkao rank in senior-2 class assignment. | 0–0.50; 0.30 | Weight; informant evidence. |
| `TERM_SHARE` | Baseline term tutoring take-up scale for academic pupils when boarding (both skill-distribution tails); tripled when `BOARD=False`. | 0.02–0.15; 0.10 | Share scale; informant and author observation, uncertain. |
| `HOL_SHARE` | Baseline holiday tutoring take-up scale (both tails), before wealth/skill weighting. | 0.20–0.60; 0.40 | Share scale; informant evidence. |
| `POST_EFF` | Gaokao-skill gain per term or holiday tutoring episode. | 0–0.20; 0.10 | SD per episode; literature mixed, meta-analysis cited as near zero. |
| `FT_SHARE` | Target share of the whole cohort in full-time outside-institution study while retaining a school place. | 0–0.05; 0.03 | Share; informant estimate about 5%, denominator unconfirmed. |
| `FT_EFF` | Gaokao-skill effect of full-time institution study relative to school-class effects. | −0.20–0.30; 0.00 | SD; sign unknown. Pupils in this route lose modeled in-school teacher and peer effects. |
| `INSURE` | Strength of tutoring response to a positive gap between family wealth rank and pupil skill rank (“fear of falling”). | 0–2; 1.00 | Behavioral coefficient; assumed approximation of informant mechanism. |
| `RHO_DEMAND` | Strength of one-round peer escalation in classmates’ tutoring take-up. | 0–1; 0.50 | Behavioral coefficient; assumed. |
| `ART_SHARE` | Target share of cohort taking the art-exam route; selection is weighted toward wealthier and lower-skill academic pupils. | 0–0.06; 0.04 | Share; informant evidence. |
| `ART_BONUS` | Additive effective-score advantage for art route. | 0.30–1.20; 0.80 | SD; informant description of specialist exam as easier; assumed scale. |
| `HK_SHARE` | Target share of cohort using the Hong Kong/Macau/Taiwan joint-exam route; selected from the wealthiest academic pupils. | 0–0.02; 0.01 | Share; informant evidence. |
| `HK_BONUS` | Additive effective-score advantage for the joint-exam route. | 0.50–1.50; 1.00 | SD; informant description of easier entry; assumed scale. |

The actual sweep has 31 unique dimensions.

## Fixed inputs

The following are not sampled by `sweep.py`; they remain at defaults (except cohort size and seed, which the scripts override). Evidence is as documented in the register or code.

| Input | Fixed value | Meaning, units, and provenance / uncertainty |
|---|---:|---|
| `n` | 60,000 default; 40,000 in sweep scripts | Synthetic pupils; computational design choice, not a population estimate. |
| `seed` | 0 default; generated per simulation in scripts | Random-number seed; design choice. `sweep.py` uses seed sequence root `27112026`; `repeats.py` uses `12272026`. |
| `SEG` | 0.60 | Correlation of family wealth with assigned zone wealth; assumed. |
| `N_JUNIOR` | 300 | Number of junior schools; stylized fixed design. |
| `JR_CLASSES` | 6 | Junior classes per school; stylized fixed design. Pupils are assigned uniformly to classes within the school. |
| `ELITE` | 0.10 | Elite seats/schools proxy: top decile of cohort; model assumption. |
| `N_HS` | 60 | Public academic high schools; stylized fixed design. |
| `HS_CLASS` | 50 | Target high-school class size used to form class groups; pupils are split into as many roughly balanced classes as the school size allows under integer division logic. |
| `TOP_BAND` | 0.125 | Top-band fraction within each high school; 12.5%, a structural assumption. |
| `PRIVATE_COST` | 75,000 yuan/year | Private-school affordability threshold; dossier value. Private seat is affordable if cost is below 40% of modeled family income. |
| `AFFORD` | 0.40 | Share of modeled income affordable for the private-place decision; assumed threshold. |
| `MED_INCOME` | 200,000 yuan/year | Median-income scale in income construction; dossier cited. Income is `MED_INCOME * exp(0.7*logw)`. |
| `N_PRIV` | 12 | Private high-school slots/groups; stylized fixed design. |
| `BOARD` | `True` | Boarding regime; structural scenario switch. When false, term tutoring baseline is tripled. |
| `FT_COST` | 140,000 yuan/year | Full-time study affordability price; informant estimate of 60–80k yuan per semester. Affordability threshold is cost < 50% of modeled income. |
| `REBAND` | `True` | Whether senior-2 bands are reassigned; sweep defaults to true. `repeats.py` sets false only for its comparison scenario. |
| `ELITE_BUY` | 0.0 | Share of elite places acquired by wealth-based paid admission; zero in Guangzhou scenarios. |
| `ZONE_ADMIT` | 0.0 | Weight of junior-school zone wealth in open elite admission; zero in Guangzhou scenarios. |
| `HS_TEACH_SD` | tied to `TEACH_SD` | High-school class-teacher SD; scripts explicitly set equal to junior teacher SD. |

## Structural rules and hard-coded choices

These rules are part of the implementation and are not independently varied in the sweep:

1. **Synthetic population.** Junior-school zones receive standard-normal wealth draws; pupils are assigned to zones uniformly. Family wealth combines a zone component scaled by `SEG`, an independent normal residual, and the `NH_WEALTH` shift for non-hukou pupils. Income is a deterministic exponential transform of wealth. Talent combines a wealth-correlated component and independent normal residual. The code does not estimate these distributions from individual administrative records.
2. **Junior school and home inputs.** Local-hukou pupils receive a teacher draw associated with their school and one of six classes; non-hukou pupils receive a separate teacher draw centered at `−MINBAN_PEN`. Initial skill is talent plus junior teacher, home wealth input, and pre-gate tutoring gain. Tutoring probability rises linearly with wealth rank, is clipped to [0,1], and is reduced by the ban via `(1−BAN_RED)`.
3. **Zhongkao and academic access.** Zhongkao score is initial skill plus Gaussian noise. Pupils are sorted by score, and a sequential cap limits non-hukou pupils among public academic seats to `QUOTA * seats`; other high scorers shut out of public seats can buy one of 12 private slots if modeled income passes the affordability test, otherwise they exit. Academic cohort is then public plus private. This means `ACAD` is the initial seat count and not always the final academic-track share after private entrants are added.
4. **Elite placement and zhibiao.** Elite capacity is `int(ELITE*n)`. The school-based pool is `int(ZHIBIAO * elite seats)`. Eligibility requires academic placement, local hukou, and a score at or above the global top `ZB_FLOOR` fraction. The pool is split among junior schools proportional to each school’s eligible pupils; each allocation is rounded and the school’s highest-scoring eligible pupils fill it. Remaining elite places are filled by open score ranking, with a separate non-hukou quota cap. These mechanics are a stylized approximation, not a district-by-district admissions implementation. Rounding, empty eligibility, and the global eligibility floor can leave some reserved capacity unfilled until the open round.
5. **High schools, classes, and bands.** Elite pupils are distributed by score order across the first `round(N_HS*ELITE/ACAD)` schools (at least one); regular academic pupils go to the rest. Private pupils are assigned to separate school indices. School value added is 2× `SCHOOL_VA` in elite schools and 1× in regular public schools. In each school the top `round(TOP_BAND * school size)`, with minimum one, are labeled top band. Pupils are sorted into class groups of roughly `HS_CLASS`; random class-teacher effects are drawn independently. Top-band pupils receive the fixed `TOP_TEACH` and `PEER` premiums.
6. **Skill progression and re-banding.** Later skill retains `(1−DECAY)` of the combined head start; talent is included again and gets `GROW * talent` learning. High-school value added, class-teacher effect, and top-band teacher and peer premiums are added. Senior-2 re-banding ranks a composite of interim observed skill and original zhongkao rank, weighted by `REBAND_PERF`; `band_and_class` preserves approximately the same top-band size per school. With `REBAND=False`, earlier bands/classes and teacher draws are carried forward.
7. **Post-gate tutoring.** Take-up is modeled only among academic pupils. Skill rank below 20% or above 80% gets a 2× tail weight; the middle gets 0.5×. This is multiplied by wealth weighting. The insurance response uses `max(wealth rank − skill rank, 0)`, so it raises take-up only for richer families whose pupil ranks lower in skill. One peer-feedback round raises probabilities using classmates’ baseline take-up; probabilities are clipped to [0,1]. Boarding scales term tutoring by one; day-school scenario scales it by three. Holiday tutoring does not use this switch.
8. **Full-time study and exams.** Full-time candidates are academic pupils who pass the affordability condition and fall below the median academic skill rank; a random subset is selected up to `int(FT_SHARE*n)`. They retain a school place but lose in-school teacher and peer effects in the final skill equation; `FT_EFF` is added instead. Term and holiday tutoring each add `POST_EFF` if taken. Gaokao score adds fresh noise. Art route is sampled with weights proportional to wealth-rank squared times (1.5 minus skill rank), and the Hong Kong/Macau/Taiwan route is sampled among academic pupils above the 70th wealth percentile. Their bonuses are additive to the effective score.
9. **University outcome.** Exactly the top 10% of the full 60,000-person cohort is designated `uni`, by effective gaokao score among academic pupils (non-academic pupils receive negative infinity). Thus the target is fixed at 10% of all pupils even when the academic share changes. Alternative exam routes change ranking, not the number of university outcomes. `sweep.py` asserts the count is 4,000 in its 40,000-person runs and that entrants who displace ordinary-score top-decile pupils use the art or HK/Macau/Taiwan route.
10. **Subsidy arithmetic.** Per-pupil subsidy is calculated with fixed yuan amounts and hukou/public/private status in the returned data. This is an accounting formula, not a modeled government budget process; it does not determine admission.

## What the replication scripts measure

- **`sweep.py`:** For each of 1,024 parameter draws, runs baseline and a paired counterfactual on the same cohort seed. The counterfactual sets `BAN_RED=0` and `REBAND=False`; consequently reported spend change compares this combined policy state with the baseline and cannot isolate the tutoring-ban effect from re-banding. `T` and `S` are wealth-gradient ratios for university entry among local-hukou pupils in the top skill quintile: wealth-high (`>=60th` percentile) versus wealth-low (`<=40th` percentile), with talent (`T`) or zone wealth (`S`) partitioning/rate averaging. `Sstar` is a joint wealth gradient for cells of zone wealth and talent, restricted to cells with at least five pupils in each wealth group; `support` reports the share of weight retained. `displaced` counts ordinary-score top-decile pupils displaced by alternative routes. `spend_change` is a modeled spending proxy based on fixed amounts and take-up indicators, not observed household expenditure.
- **`repeats.py`:** Uses fixed sampled parameter settings and eight independent cohort seeds per setting. `delta_T` is baseline talent-gradient ratio minus the ratio in the paired `BAN_RED=0`, `REBAND=False` run. This estimates combined scenario sensitivity to cohort randomness for those sampled settings, not a standalone causal effect of the ban.

## 2026 rule alignment and known mismatches

The parameter register summarizes 2026 non-hukou quota rules as 8–15% in core districts and 8–18% in outer districts. The sweep’s `QUOTA` range is 8–20%, so draws above 18% do not match either stated 2026 range; draws from 15% to 18% also exceed the stated core-district maximum. The fixed default of 15% is at the core upper bound, inside the outer range. The code applies one quota parameter statewide and applies it to both public academic seats and elite seats, whereas the cited real-world limits vary by district and admission category. The register separately cites 8–20% from 2027; these later values should not be read as 2026 compliance.

The stated 2026 rule requires **at least 50%** of elite high-school places to be allocated through zhibiao. The default `ZHIBIAO=0.50` meets that minimum exactly, and values above it meet the minimum, but the sweep includes 30–50% draws that violate it. `ZHIBIAO` should therefore be interpreted as a sensitivity range, not a set of universally rule-compliant 2026 scenarios. A strict 2026-compliant analysis would constrain it to 0.50 or higher and constrain `QUOTA` to the applicable district’s 2026 cap. The model also approximates zhibiao eligibility and allocation with a cohort-wide score floor, proportional allocation to eligible pupils per junior school, and local-hukou restriction; it omits the full official district, school, and category details.

## Limitations and interpretation

- The cohort, schools, scores, family resources, and admissions are simulated. No pupil-level administrative dataset is fitted or validated here.
- Parameter ranges mix formal literature intervals, a few context-specific estimates, informant observations, and author assumptions. Several ranges are deliberately broad; uniform sampling means every point in each interval receives equal marginal design weight, not equal plausibility.
- Inputs are sampled independently even where dependencies are plausible. Correlated teacher and school effects, correlated tutoring access and tutoring benefit, or district-specific quota regimes are not represented except where explicitly tied (`HS_TEACH_SD = TEACH_SD`).
- The education trajectory compresses years and subjects into a handful of latent scores and rank-based transitions. The same Gaussian noise scale is used at several exams; many institutional details, regional variation, and policy categories are absent.
- `ELITE=0.10`, a fixed top-decile university outcome, fixed capacities, affordability thresholds, alternative-route bonuses, and the one-round peer-response equations are modeling choices. Resulting ratios are conditional scenario outputs and should not be reported as measured causal effects or population forecasts.
- `spend_change` uses 45,000 yuan per pre-gate tutoring indicator, 35,080 per term indicator, 20,000 per holiday indicator, and twice `FT_COST` per full-time pupil. These fixed unit costs are embedded in `sweep.py`, not in the parameter register; they are proxies and their price year, frequency, and pupil-level interpretation are not calibrated in that script.
