#!/usr/bin/env python
"""Build STYLIZED_FACTS.csv from the hand-curated fact rows below.

Deterministic: rerunning rewrites a byte-identical CSV. Paths are relative to
BASE = experiments/massification-2026-11-20. Every numeric cell was either
re-read from the cited file (VERIFIED-FROM-DISK) or is quoted from the file /
audit named in `note` and labelled accordingly.

Label vocabulary (fixed by the task):
  VERIFIED-FROM-DISK        value re-read/re-computed by this worker from the cited file
  REPORT-ONLY-UNRELIABLE    value is quoted in narrative but is absent from, or contradicted by, disk
  DISPUTED                  two on-disk objects disagree, or one object is internally contradictory
  MODEL-OUTPUT-NOT-FACT     produced by a model/toy run, not a property of the world
  SIMULATED                 stipulated toy; design constraint only
"""
import csv
import os

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "STYLIZED_FACTS.csv")

COLS = ["fact_id", "plain_english", "value_units", "source_paths", "evidence_label",
        "confidence", "what_a_generator_must_reproduce", "note"]

U = "10_massification/data/UNIVERSALIZATION_SERIES.csv"
G = "data/gmr_observed_6countries_1970_2024.csv"
B = "10_massification/data/BASELINE_SERIES.csv"
TA = "10_massification/relations/data/UNIVERSALIZATION_TIMING.csv"
TB = "10_massification/data/UNIVERSALIZATION_TIMING.csv"
SL = "10_massification/relations/data/scaling_laws.csv"
SE = "10_massification/model2/runs/scaling_estimates.csv"
SC = "10_massification/model/calib/scaling_check.csv"
RS = "10_massification/model/calib/repair_scaling.csv"
CC = "10_massification/relations/data/capacity_crosscountry.csv"
CA = "10_massification/relations/data/capacity_alignment.csv"
STC = "10_massification/relations/data/state_capacity.csv"
PPT = "10_massification/relations/data/push_pull_tests.csv"
SMK = "10_massification/model/smoke/structure_smoke.csv"
REC = "10_massification/model2/runs/recovery.csv"
A5B = "10_massification/model2/runs/a5b_equivalence_to_observed.csv"
E_SUM = "10_massification/extensions/lab_2026-11-20/results/SUMMARY.csv"
E1F = "10_massification/extensions/lab_2026-11-20/results/E1_income_gradient.csv"
E10F = "10_massification/extensions/lab_2026-11-20/results/E10_replication.csv"
BR = "10_massification/extensions/lab_2026-11-20_b/RESULTS.csv"
CR = "10_massification/extensions/lab_2026-11-20_c/RESULTS.csv"
Y3C = "10_massification/extensions/lab_2026-11-20_c/Y3_capacity_floor/results/Y3_correlations.csv"
Y3L = "10_massification/extensions/lab_2026-11-20_c/Y3_capacity_floor/results/Y3_leave_one_out.csv"
RG = "10_massification/extensions/audit_2026-11-20/a_regressions/REGRESSION_INVENTORY.md"
MI = "10_massification/extensions/audit_2026-11-20/b_models/MODEL_INVENTORY.md"
TI = "10_massification/extensions/audit_2026-11-20/c_toys/TOY_INVENTORY.md"
S18 = "08_council/brief_018/SYNTHESIS_018.md"

ROWS = [
# ---------------------------------------------------------------- (a) PHL anchor
dict(
 fact_id="PHL-01",
 plain_english="Filipino children finished primary school at a rate that crossed 90% for the first time in 2017 and kept rising to 98% by 2024.",
 value_units="primary completion: 83.16% (1999) -> 87.45% (2013) -> 91.918% (2017, first year >=90) -> 95.40% (2021) -> 98.305% (2024); percent, all status=observed",
 source_paths=U + " | " + G,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="A PHL primary-completion path that is first >=90 in 2017 and >=98 by 2024, with each of the five quoted years within +/-2 pp of the observed value.",
 note="Re-read from UNIVERSALIZATION_SERIES.csv (11 observed rows 1999-2024) and cross-checked against data/gmr_observed_6countries_1970_2024.csv indicator CR.1 (identical values). 2013 = 87.450 < 90, so 2017 is genuinely the first crossing. ANCHOR FACT."),
dict(
 fact_id="PHL-02",
 plain_english="Filipino children finished lower secondary at 92.4% in 2024, the first year that rate reached 90%.",
 value_units="lower-secondary completion: 58.86% (1999) -> 71.27% (2013) -> 81.255% (2017) -> 88.442% (2023) -> 92.414% (2024); percent, observed",
 source_paths=U + " | " + G,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="Lower-secondary completion first >=90 in 2024, one level below primary and seven years behind it.",
 note="Re-read; matches GMR file indicator CR.2 exactly. 2023 = 88.442 < 90 so 2024 is the crossing year on this series. ANCHOR FACT."),
dict(
 fact_id="PHL-03",
 plain_english="Upper-secondary completion in the Philippines peaked at 76.4% in 2017 and was 75.0% in 2024 - it never reached 90%.",
 value_units="upper-secondary completion: 59.70% (1999) -> 67.47% (2013) -> 76.433% (2017, series maximum) -> 68.277% (2022) -> 71.929% (2023) -> 75.025% (2024); never >=90; gap to 90 = 14.975 pp",
 source_paths=U + " | " + G + " | " + TA,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="A ceiling that never reaches 90 over 1999-2024, peaks near 76.4, and sits ~15 pp below the threshold in the last observed year.",
 note="Re-read all 11 observed rows; max = 76.432953 (2017); 2024 = 75.025253. A01 timing file records PHL upper_secondary_universal 90 as not_crossed_by_last_obs. THIS IS THE ANCHOR ASYMMETRY - see PHL-06."),
dict(
 fact_id="PHL-04",
 plain_english="Tertiary enrolment in the Philippines went from about 16 school places per 100 young people in 1971 to 51 in 2025.",
 value_units="tertiary GER: 16.336% (1971) -> 27.52% (1999) -> 38.345% (2016) -> 28.117% (2018 dip) -> 47.414% (2024) -> 51.072% (2025) -> 52.990% (2026); percent, observed",
 source_paths=U + " | " + G,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="Tertiary GER ~16.3% in 1971 rising to 51.1% in 2025, including the 2017-2018 dip from 38.3% to 28.1%.",
 note="51 annual observed points re-read; matches GMR indicator GER.5T8. The 2018 dip coincides with the K-12 cohort change and the 2018 free-tuition policy - the timing is a fact, the cause is not established (see MUST_REPRODUCE 'do not reproduce' list)."),
dict(
 fact_id="PHL-05",
 plain_english="Almost every Filipino child was already enrolled in primary school in 1971 (99.5%) - the 2017 'universal primary' date is about finishing school, not about getting in.",
 value_units="primary GER: 99.54% (1971) -> 106.47% (1990) -> 103.41% (2015) -> 99.37% (2017) -> 94.55% (2018) -> 88.83% (2021) -> 94.03% (2024); primary NER 96.79% (1976); percent",
 source_paths=U + " | " + G + " | " + TB,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="If the generator reports participation (GER) as well as completion, PHL primary GER must be >=95 in every observed year 1971-2017 and fall below 95 only after 2017.",
 note="43 observed GER rows re-read. This is the fact that makes the crossing vector measure-dependent: on GER, primary access was 'universal' 46 years before the completion crossing. Audit FLAG-05."),
dict(
 fact_id="PHL-06",
 plain_english="The Philippine system moved its floor and its middle over the 90% line within seven years, but its ceiling never moved at all.",
 value_units="primary 90 crossed 2017; lower-secondary 90 crossed 2024 (7-year gap); upper-secondary max 76.43% and 75.03% in 2024 (never crossed); tertiary GER 50 crossed 2025",
 source_paths=U + " | " + TA + " | " + S18,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="At least one level that saturates below threshold while the level below it completes: a hard ceiling that does NOT respond to the same drivers that lifted the floor.",
 note="SYNTHESIS_018 calls this 'the observed asymmetry signature (A6/D77)'. It is the single most important structural target for a synthetic generator and the one no model on disk reproduces (see MOD-02)."),
# ---------------------------------------------------------------- (b) regional
dict(
 fact_id="REG-01",
 plain_english="All 17 Philippine regions raised their average years of schooling between the 1960-64 and 1990-94 birth cohorts.",
 value_units="dMYS > 0 in 17/17 regions; range +0.505 y (NCR) to +2.095 y (CAR); mean +1.250 y",
 source_paths=B,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="17/17 regions with strictly positive cohort-on-cohort attainment gain, smallest gain in the richest region (NCR).",
 note="Recomputed from BASELINE_SERIES.csv, sex rows averaged per region (34 rows/period = 17 regions x 2 sex rows). Matches X10 (lab_2026-11-20_b RESULTS.csv) and the Council re-derivation in SYNTHESIS_017."),
dict(
 fact_id="REG-02",
 plain_english="Education inequality fell by at least 0.02 Gini points in every one of the 17 Philippine regions.",
 value_units="dGini <= -0.02 in 17/17 regions; range -0.030 (NCR) to -0.095 (ARMM); mean -0.057",
 source_paths=B,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="17/17 regional Gini declines of at least 0.02, largest in the lowest-attainment region (ARMM).",
 note="Recomputed from BASELINE_SERIES.csv (education_gini, sex rows averaged). Matches X11 count=17 in lab_2026-11-20_b/RESULTS.csv."),
dict(
 fact_id="REG-03",
 plain_english="The regions that started with the least schooling gained the most, so regional gaps closed.",
 value_units="Spearman rho(dMYS, MYS_1960-64) = -0.443627 (n=17, no CI computed)",
 source_paths=B + " | " + BR,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="A negative rank correlation between initial attainment and subsequent gain of about -0.44 (+/-0.1) across 17 regions.",
 note="Recomputed exactly (-0.443627) and matches the X10 row in lab_2026-11-20_b/RESULTS.csv and the Council's independent re-derivation (SYNTHESIS_017 table, MATCH)."),
dict(
 fact_id="REG-04",
 plain_english="Regions that started with the most unequal schooling saw inequality fall the most.",
 value_units="Spearman rho(dGini, Gini_1960-64) = -0.621524 (n=17)",
 source_paths=B + " | " + BR,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="rho(dGini, Gini0) near -0.62 (+/-0.1) with 17 regions and all declines >= 0.02.",
 note="Recomputed exactly; matches X11 (rho=-0.621524) and SYNTHESIS_017 (MATCH)."),
dict(
 fact_id="REG-05",
 plain_english="The schooling gain was mildly pro-poor: the bottom quarter of regions gained about 10% more years than the top quarter.",
 value_units="median dMYS Q1 = 1.340 y vs Q4 = 1.220 y; ratio = 1.098; quartile cut-offs on MYS_0 = 9.16 / 9.39 / 9.82; Q1 n=5, Q4 n=4",
 source_paths=B + " | " + BR,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="Q1/Q4 median-gain ratio in [1.05, 1.15]; do NOT reproduce a strong pro-poor gradient (the gradient is mild).",
 note="Recomputed with the battery's disclosed cut-offs: Q1 median 1.340 (5 regions), Q4 median 1.220 (4 regions), ratio 1.098361. Matches X12. SYNTHESIS_017 notes the asymmetric quartile sizes are disclosed, verdict unchanged."),
dict(
 fact_id="REG-06",
 plain_english="We have no regional university-enrolment numbers for the Philippines, so the regional story is about years of schooling and inequality, not about who went to university.",
 value_units="BASELINE_SERIES.csv contains 144 rows and only 4 region-level indicators (education_gini, mean_years_of_schooling, PTR, teachers hired); zero regional tertiary GER/participation series exist on disk",
 source_paths=B + " | " + BR,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="Nothing numerically - but a generator that reports regional tertiary participation must declare it as GENERATED, because no observed counterpart exists.",
 note="Absence verified from the file's own indicator list and stated by X10/X11/X12's own LIMITATION columns. This is the binding limitation on REG-01..REG-05: they are attainment/inequality facts, not post-secondary participation facts."),
# ---------------------------------------------------------------- (c) income scaling
dict(
 fact_id="SCA-01",
 plain_english="Within a country, secondary enrolment barely responds to income; across countries it responds modestly.",
 value_units="secondary GER ~ GDPpc (log-log): within (country+year FE) 0.0904 (se 0.1238, p=0.465, ns, n=1042, 30 cty); between (year FE) 0.2154 (se 0.0349, p<0.001)",
 source_paths=SL,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="Within exponent in [0.05, 0.13] and insignificant; between exponent in [0.18, 0.25] and significant; between > within.",
 note="Read verbatim from scaling_laws.csv rows S1-within / S1-between. This is the pair the closeout's '+0.286 target' is compared against - see SCA-06."),
dict(
 fact_id="SCA-02",
 plain_english="Tertiary enrolment rises strongly with income and rises faster inside a country over time than across countries.",
 value_units="tertiary GER ~ GDPpc: within 0.8482 (se 0.1719, p<0.001, n=1037); between 0.5666 (se 0.0817, p<0.001); within > between by 0.28",
 source_paths=SL + " | " + SE,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="A within-country tertiary income exponent of about 0.85 and a between exponent of about 0.57, i.e. within > between.",
 note="Read verbatim from scaling_laws.csv S2-within / S2-between. Note the direction of the within-vs-between gap is opposite to the secondary case (SCA-01) - a generator that imposes one gap sign everywhere will fail one of the two."),
dict(
 fact_id="SCA-03",
 plain_english="Lower-secondary completion rises with income about a quarter of a percent per percent, both within and across countries.",
 value_units="lower-secondary completion ~ GDPpc: within 0.2468 (se 0.1188, p=0.038, n=629, 28 cty); between 0.1690 (se 0.0343, p<0.001)",
 source_paths=SL,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="Completion exponents of about 0.25 (within) and 0.17 (between); the within estimate is only marginally significant.",
 note="Read verbatim from scaling_laws.csv S4. Ties to SCA-06: the A1 gate's tertiary target 0.776 sits below this range while its secondary target 0.286 sits above it."),
dict(
 fact_id="SCA-04",
 plain_english="The gap between within-country and across-country income slopes is large and has opposite signs for agriculture and industry - this gap, not the level, is the structural target.",
 value_units="agricultural employment share: within -0.1201 (se 0.0834, ns, n=1017) / between -0.9901 (se 0.2162); industrial share: within +0.5283 (se 0.1508, p=0.0005) / between +0.1426 (se 0.0555, p=0.010)",
 source_paths=SL,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="Both sector gaps: agriculture between far more negative than within; industry within far more positive than between. A model with a single relabelled income term cannot produce both.",
 note="Read verbatim from scaling_laws.csv S7/S8. GAPS_AND_LEADS (a_regressions) nominates this gap as the best model-discriminating moment at n=1017."),
dict(
 fact_id="SCA-05",
 plain_english="Countries with higher fertility have lower primary completion - about 0.19 percentage points per unit of fertility within a country.",
 value_units="primary completion ~ TFR (semi-log): within -0.1893 (se 0.0436, t=-4.34, n=712, 28 cty); between -0.1222 (se 0.0267, t=-4.57)",
 source_paths=SL,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="A negative cohort-size association of about -0.19, negative in at least 8 of 10 sample splits (split evidence is REPORT-ONLY from the relations layer, not re-derived here).",
 note="Read verbatim from scaling_laws.csv S12. The 8/10 split claim is quoted from the audit/relation layer (REGRESSION_INVENTORY B02) and was NOT re-derived by this worker."),
dict(
 fact_id="SCA-06",
 plain_english="Two different 'income-scaling targets' sit on disk - 0.286 (secondary) and 0.776 (tertiary) from one estimator, versus 0.215 and 0.567 from another - and the gate used the pair that its own containment range rejects.",
 value_units="model2 between-estimator targets: secondary 0.285844 (se 0.045163, n=30), tertiary 0.776087 (se 0.086416, n=30); relations year-FE values: 0.2154 / 0.5666; repair gate writes A1=0.286 against A3 range [0.0904, 0.2154] -> 0.286 is OUTSIDE",
 source_paths=SE + " | " + SL + " | " + RS,
 evidence_label="DISPUTED", confidence="high",
 what_a_generator_must_reproduce="Pick ONE target pair and declare it. If the target is 'containment in the relations range', secondary must land in [0.090, 0.215]; if it is 'within 1 se of model2', 0.286 +/- 0.045. A generator cannot be scored against both.",
 note="Both numbers verified on disk. D-13 (repair_scaling.csv: A1_value=0.286 vs A3_hi=0.2154) makes the criterion unwinnable on the secondary law; D-14 notes the A1 target is itself one of the two estimators. The SIGN failure of the old model class is robust to this dispute (SCA-07)."),
dict(
 fact_id="SCA-07",
 plain_english="The old cohort-flow model generated income-scaling exponents with the wrong sign, and this is a property of the model class, not of the world.",
 value_units="generated OOS 2011-2024 exponents: secondary -1.893 / -0.379 / -0.743 (three rivals); tertiary -1.229 / -0.137 / -0.353; repair cell: secondary -2.734 / -2.527 / -1.034, tertiary -0.319 / -1.317 / -0.391; signs_ok 1/3, contained 0/3",
 source_paths=SC + " | " + RS + " | " + MI,
 evidence_label="MODEL-OUTPUT-NOT-FACT", confidence="high",
 what_a_generator_must_reproduce="The POSITIVE sign (SCA-01..SCA-03). This row is the negative to avoid: a generator whose income channel is demand-side only will produce these wrong-signed exponents.",
 note="Values read from scaling_check.csv and repair_scaling.csv. Caveat D-11: scaling_check.csv has no generator script in the tree (orphan artefact), so the numbers are quoted, not reproduced; the sign conclusion also survives via repair_scaling.csv, which does have a pipeline."),
# ---------------------------------------------------------------- (d) six-system gradient
dict(
 fact_id="INC-01",
 plain_english="In the six detailed countries, one percentage point of log income is associated with about 56 points of upper-secondary enrolment - but that estimate rests on only five clusters.",
 value_units="within slope upper-secondary GER on log GDP = +56.066 (se 19.558, CI 17.732..94.400, n=93, 5 clusters, within R2 0.726); between slope +159.857 (se 3.333, n=5)",
 source_paths=E1F + " | " + E_SUM,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="Nothing as a law. If the generator is fitted to the six systems, it must at least reproduce the ORDER of magnitude of the within slope (~+56 pp/log point) while carrying the 5-cluster caveat.",
 note="Read from E1_income_gradient.csv. The between slope (159.9, n=5 clusters) is a 5-point regression and is not usable as a target. Label 'strong' in SUMMARY.csv is the audit's FLAG-08 complaint."),
dict(
 fact_id="INC-02",
 plain_english="When the same income gradient is estimated on 30 countries instead of six, it falls to +14.7 and is no longer distinguishable from zero.",
 value_units="30-country pooled slope +14.7397 (se 8.3156, 95% CI -1.5588..+31.0382, n=14); E1 value +56.066 for comparison",
 source_paths=E10F + " | " + E_SUM,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="Do not target +56 as a law. A generator calibrated to +56 on six systems must be reported as failing at 30 countries, exactly as here (ratio ~0.26, CI includes 0).",
 note="Read from E10_replication.csv. This is the programme's own internal falsifier of E1 and the reason CAST this as a fact about the data rather than a law."),
dict(
 fact_id="INC-03",
 plain_english="The six-system income gradient is a description of six countries and is not portable; the battery attributes it to China and Cambodia.",
 value_units="E1 +56.07 (6 systems, 5 clusters) vs E10 +14.74 (30 countries, CI spans 0); implied shrinkage ~74%",
 source_paths=E1F + " | " + E10F + " | " + RG,
 evidence_label="VERIFIED-FROM-DISK", confidence="medium",
 what_a_generator_must_reproduce="If a generator matches the six-system gradient, it must also produce the 30-country collapse - i.e. the steep segment must be a property of two systems, not of the income channel.",
 note="The two slopes and their CIs are verified. The CHN/KHM attribution is quoted from the battery FINDINGS and the audit (FLAG-08) and was NOT re-derived by this worker - hence confidence medium."),
# ---------------------------------------------------------------- (e) timing / censoring
dict(
 fact_id="TIM-01",
 plain_english="Japan and Korea had already finished universalising primary school before our data start, so we can only bound their dates, not measure them.",
 value_units="JPN primary >=95: censored_above_at_first_obs at 1971 (reconstructed NER band 1975-1976, reconstructed=True); KOR primary NER >=95: censored at 1971; KOR lower-secondary completion >=90: censored at 2003; KOR upper-secondary completion >=90: censored at 2000 while NER crosses 2009.5",
 source_paths=TA,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="Left-censoring: report JPN/KOR as '<=1971' (or '<=2000/2003' for the Korea levels), never as a point crossing year. Any generator scoring crossing years must accept interval/inequality targets for these systems.",
 note="Read from UNIVERSALIZATION_TIMING.csv (relations, A01, 63 rows). A02/A01 status strings 'censored_above_at_first_obs' are the on-disk censoring marker."),
dict(
 fact_id="TIM-02",
 plain_english="Hong Kong reached 90% primary enrolment in 1974 and 95% in 1979, and never reaches 90% at upper-secondary on the net measure.",
 value_units="HKG primary NER >=90: 1974 (band 1973-1974); >=95: 1979 (band 1978-1979); lower-secondary NER >=90: 2015.5 (measure artefact per EVENT_WINDOWS s5); upper-secondary NER >=90: not crossed (in-school variant 2014.5)",
 source_paths=TA,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="HKG primary >=90 by 1974 and >=95 by 1979; upper-secondary >=90 never on NER.",
 note="Read from A01. The upper-secondary HKG value is the ONLY dated upper-secondary crossing the Y4 null model had (2011.5 median), so it carries the whole Y4 conclusion - see NEG-06."),
dict(
 fact_id="TIM-03",
 plain_english="The Philippine crossing vector on the completion measure is: primary 2017-2021, lower-secondary 2023-2024, tertiary GER 2024-2025, upper-secondary never.",
 value_units="A01 rows: PHL primary_universal 95/completion crossing_lo 2017, hi 2021 (mid 2019); PHL lower_secondary_universal 90/completion 2023-2024 (mid 2023.5); PHL tertiary_mass 50/GER 2024-2025 (mid 2024.5); PHL upper_secondary_universal 90/completion 2024..NaN, status not_crossed_by_last_obs",
 source_paths=TA,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="Exactly this ordering and rough spacing: primary before lower-secondary before/at tertiary, with upper-secondary absent.",
 note="Read from A01. Note the bands, not points: '2017' is the band start and '2019' the band midpoint - the +35.2 capacity claim used 2019 (see CAP-02)."),
dict(
 fact_id="TIM-04",
 plain_english="Two timing files with the same name give different crossing years for the same country because they use different measures and different definitions.",
 value_units="A01 (relations, 63 rows, completion/NER, first-sustained) vs C03 (data, 128 rows, GER/NER, first-at-above): PHL primary -> 2017-2021 vs 1971 GER / 1976 NER; PHL lower-secondary -> 2023-2024 vs 2014 GER; CHN lower-secondary -> 2014-2016 vs 2006 GER; PHL tertiary -> 2024-2025 vs 2025 (agree)",
 source_paths=TA + " | " + TB,
 evidence_label="DISPUTED", confidence="high",
 what_a_generator_must_reproduce="Pick one measure per milestone and declare it (M1 NER/GER, M2/M3 completion, M4 GER is the predeclared mapping). Do not mix: a completion crossing compared with a participation law is a category error.",
 note="Audit FLAG-05. Both files are internally valid; nothing on disk disambiguates them at the point of use. The observed signature (PHL-01..PHL-03) stands because A01's primary row is already the completion row."),
dict(
 fact_id="TIM-05",
 plain_english="There is no single agreed crossing vector on disk yet - the corrected vector was ordered but not produced.",
 value_units="0 corrected single-measure crossing files exist under 10_massification/relations/data/ ; the two on-disk vectors are A01 (63 rows) and C03 (128 rows)",
 source_paths=TA + " | " + TB + " | " + S18,
 evidence_label="DISPUTED", confidence="high",
 what_a_generator_must_reproduce="Do not target 'the' crossing vector. Target the milestone facts (PHL-01/02/03, TIM-01, TIM-02) and treat any year as measure-qualified.",
 note="SYNTHESIS_018 Z2 ordered the corrected vector ('C2 prerequisite'); it has not landed. Audit GAPS_AND_LEADS lists this as one of the three numbers that must be re-derived before reuse."),
# ---------------------------------------------------------------- capacity
dict(
 fact_id="CAP-01",
 plain_english="The sentence 'capacity does not predict crossing timing (Spearman +0.15/+0.10/+0.41/+0.30, all ns, n=5)' is not supported by anything on disk.",
 value_units="values in capacity_crosscountry.csv: primary_universal +0.872 (p=0.054); lower_secondary_universal +0.900 (p=0.037); upper_secondary_mass +0.103 (p=0.870); tertiary_mass +0.800 (p=0.104); n=5 each",
 source_paths=CC + " | " + RG + " | " + STC,
 evidence_label="REPORT-ONLY-UNRELIABLE", confidence="high",
 what_a_generator_must_reproduce="NOTHING from the '+0.15 all ns' sentence. If capacity timing is modelled at all, the honest target is 'not identifiable at n=5' (and the +0.900 is a one-country artefact: JPN enters at capacity_within 20.0 vs 46.5-61.1).",
 note="Audit FLAG-02. The four narrative numbers appear in no file; the four file numbers are verified on disk and were independently recomputed by the auditor from state_capacity.csv + timing. SYNTHESIS_018 withdrew the narrative and ordered re-derivation (Z2, not run)."),
dict(
 fact_id="CAP-02",
 plain_english="The claim that Philippine state capacity rose 35.2 points into the primary crossing does not reproduce; on the same index the rise is 14.4 or 26.1 points depending on the crossing year used.",
 value_units="capacity_alignment.csv row: PHL primary, crossing_year_used=2019, capacity_5y_before=49.5, capacity_at_crossing=84.7, capacity_change_pre=+35.2. Recomputed from state_capacity.csv capacity_within: 2014-18 mean 57.214 -> 2019 value 83.36 = +26.15; 2012-16 mean 42.946 -> 2017 value 57.38 = +14.43; capacity_within 2017 (57.38) is BELOW 2005 (58.89)",
 source_paths=CA + " | " + STC + " | " + RG,
 evidence_label="REPORT-ONLY-UNRELIABLE", confidence="high",
 what_a_generator_must_reproduce="No +35.2. The reproducible statements are: PHL delivery capacity rose over 2005-2021 and the upper-secondary ceiling did not move. Any capacity-into-crossing path must be re-derived from state_capacity.csv with a declared crossing year.",
 note="Audit FLAG-03; recomputation performed by this worker from state_capacity.csv and agrees with the auditor's +26.1 / +14.4. Caveat: weight_coverage falls 1.00 (2005) -> 0.90 (2017) -> 0.60 (2019-23), so the 2019 index is differently composed."),
dict(
 fact_id="CAP-03",
 plain_english="Philippine primary class sizes fell and education spending rose while upper-secondary completion stayed flat at 75% - a genuine counterexample to a pure capacity story.",
 value_units="PHL primary PTR 35.074 (2005) -> 29.084 (2017) -> NaN after 2018; education spending 2.328% GDP (2005) -> 3.964% GDP (2017); upper-secondary completion 76.433% (2017) -> 75.025% (2024)",
 source_paths=STC + " | " + U,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="A generator whose capacity channel drives both floor and ceiling must be able to produce capacity rising while the ceiling is flat; if it cannot, the capacity channel is mis-specified.",
 note="ptr_primary_raw and spend_gdp_raw re-read from state_capacity.csv PHL rows; completion from UNIVERSALIZATION_SERIES.csv. This is the descriptive core that survives FLAG-02/FLAG-03 (REGRESSION_INVENTORY s3, A15/A16/A21)."),
dict(
 fact_id="CAP-04",
 plain_english="With only five or six countries, we cannot tell whether capacity tracks the floor rather than the ceiling.",
 value_units="Y3: rho(dPTR-improvement, floor) = +0.50 (n=5, meets the |rho|>=0.50 bar only at the boundary); rho(dPTR-improvement, ceiling) = +0.60 (n=6, fails the |rho|<0.50 bar); leave-one-out floor 0.0..0.8, ceiling 0.3..0.9; both conditions hold only when JPN is dropped",
 source_paths=Y3C + " | " + Y3L + " | " + CR,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="Nothing as a mechanism. A synthetic world may impose 'capacity buys the floor, not the ceiling', but it must be labelled a stipulation: the observed data cannot separate the two at n=6.",
 note="Read from Y3_correlations.csv / Y3_leave_one_out.csv. Y3 verdict = NOT SUPPORTED (not separable). A10's 'floor not ceiling' remains a model-side ruling."),
# ---------------------------------------------------------------- (g) push-pull
dict(
 fact_id="PP-01",
 plain_english="Income growth predicts later tertiary enrolment growth very strongly - and the file's own label says the opposite direction.",
 value_units="push_pull_tests.csv row P5: dependent=d_log_ger_t, driver=d_log_gdppc -> F=6.522, p<0.001, sum of lag coefficients +0.2051 (n=774, 30 cty). Correctly oriented: GDP-pc growth -> tertiary GER.",
 source_paths=PPT + " | " + RG,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="An income-to-tertiary-enrolment predictive association with F~6.5 and a POSITIVE coefficient sum (~+0.21).",
 note="Verified by reading the dependent/driver columns (the estimation is y_t ~ own lags + driver lags). FLAG-00: the 'hypothesis' text on every row is reversed, so the file's P5 label reads 'tertiary-GER -> GDP'. SYNTHESIS_018 sA item 8 relies on this corrected orientation."),
dict(
 fact_id="PP-02",
 plain_english="Income growth predicts LOWER secondary completion (coefficient -0.67), which is the reversed reading of the 'education -> growth -0.667' constraint.",
 value_units="row P6: dependent=d_log_cmpt_s, driver=d_log_gdppc -> F=3.514, p=0.0035, sum -0.6674 (n=376, 27 cty)",
 source_paths=PPT + " | " + RG,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="A negative income-to-completion predictive association (~-0.67) alongside the positive income-to-tertiary one; the two signs differ in the data.",
 note="FLAG-00 again: the note and closeout quote this as 'education -> growth negative'. Correctly it is GDP growth -> completion. The sign is what a generator must carry; the interpretation as a causal constraint is withdrawn (R13)."),
dict(
 fact_id="PP-03",
 plain_english="There is no detectable effect of education on later income growth in any of the three education-to-growth tests.",
 value_units="education -> GDP-pc growth rows: P1 secondary GER F=0.943 p=0.452; P2 tertiary GER F=0.648 p=0.663; P3 secondary completion F=1.516 p=0.181 (all n>=376, 27-30 cty)",
 source_paths=PPT,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="A NULL in the reverse direction. A generator that produces a symmetric lead-lag (education<->income both significant) is falsified by this file.",
 note="These three rows are the file's P1/P2/P3, whose hypothesis labels claim the income->education direction; correctly oriented, they are the education->income tests. This asymmetry (significant one way, null the other) is the sharpest moment in the file (GAPS_AND_LEADS (b) item 1)."),
dict(
 fact_id="PP-04",
 plain_english="Wage-share growth predicts secondary enrolment growth (F=4.11), while the reverse is only marginal (F=1.88, p=0.094).",
 value_units="row P9: dependent=d_log_wage, driver=d_log_ger_s -> F=4.108, p=0.0010, sum +0.0504 (n=493); row P10: dependent=d_log_ger_s, driver=d_log_wage -> F=1.881, p=0.0940, sum +0.1059",
 source_paths=PPT,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="The one-way pattern: market-side (wage share) leads schooling, not the reverse, at a 4:1 F-ratio.",
 note="Orientation read from dependent/driver. Signs of sum are both positive; the discriminating feature is significance, not sign."),
dict(
 fact_id="PP-05",
 plain_english="None of this identifies a direction of causation; the pure push and pure pull worlds are both recoverable and an outside truth is forced.",
 value_units="recovery: demand 1.00, supply 1.00, complementary 0.00; forced-ID 1.00; equivalence 0.07 (model2/runs/recovery.csv: truth C is classified S in 5/5 seeds, truth OUT misclassified in 3/5)",
 source_paths=REC + " | " + MI + " | " + A5B,
 evidence_label="MODEL-OUTPUT-NOT-FACT", confidence="high",
 what_a_generator_must_reproduce="No direction claim. A generator may embed a direction as a STIPULATION but must not claim the data license it.",
 note="recovery.csv re-read (20 rows): the D and S truths are recovered 5/5, the C truth never; equivalence flags mostly False. The 'forced-ID 1.00 / equivalence 0.07' summary is quoted from MODEL_INVENTORY s3.7, not re-derived. R13 stands."),
dict(
 fact_id="PP-06",
 plain_english="Every push-pull row in the file is labelled with the opposite direction to the one that was estimated.",
 value_units="13/13 rows: the `hypothesis` column names x -> y where the model is y_t ~ own lags + x lags with x = `driver`; e.g. P5 hypothesis says 'tertiary-GER growth -> GDP-pc growth' but dependent=d_log_ger_t",
 source_paths=PPT + " | " + RG,
 evidence_label="DISPUTED", confidence="high",
 what_a_generator_must_reproduce="If these numbers are used as moments, they must be used in the corrected orientation (PP-01..PP-04). The label defect must not be inherited.",
 note="Audit FLAG-00, 'the most serious labelling defect in the regression layer'. The EQUIVALENT label and direction_claim='none' are correct in the same file; only the hypothesis text is reversed."),
# ---------------------------------------------------------------- (h) negatives
dict(
 fact_id="NEG-01",
 plain_english="Once you remove the common trend, schooling and market variables show no detectable lead-lag relationship in either direction.",
 value_units="max |cross-lag partial r| = 0.208 (schooling->market, lag 1; n=700, 30 countries); 0/24 cells reach the 0.25 bar; zero-order correlations 0.49-0.71 are shared trend; reverse-direction cells -0.057..+0.090",
 source_paths=CR,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="Max |partial lead-lag r| < 0.25 in all 24 cells. A generator that produces a strong schooling<->market lead-lag is over-fitting the visible co-movement.",
 note="Values read from the Y2 row of RESULTS.csv (estimate, n, threshold, caveats). The computation was NOT re-run by this worker (partial-correlation panel work is a regression). GAPS_AND_LEADS calls this 'the cheapest available specification test in the programme'."),
dict(
 fact_id="NEG-02",
 plain_english="The two absorption proxies fail to replicate each other: one is -0.86 in six countries and the other is +0.80 in thirty, with opposite signs.",
 value_units="X1 within slope TER on ABSORB_F = -0.858 (se 1.559, CI -3.915..2.198, n=139, 6 cty); X2 30-country = +0.797 (se 0.612, CI -0.402..1.996, n=654, 30 cty); both CIs include 0; X1's ABSORB_S variant also negative (-1.897, CI includes 0)",
 source_paths=BR + " | " + S18,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="Either proxy's sign, but NOT a claim that tertiary expansion is absorbed by formal jobs. The honest target is 'no replicated association'.",
 note="Read from lab_2026-11-20_b/RESULTS.csv (X1/X2 rows). SYNTHESIS_017 condition 4: cite only as 'consistent with the closed scaling failure (model-class limit)', never as a world claim."),
dict(
 fact_id="NEG-03",
 plain_english="The one absorption measure that 'survives' is close to mechanical - its numerator is a lagged stock of tertiary attainment.",
 value_units="X3 slope of QUEUE on TER = +0.366 (se 0.086, CI 0.198..0.534, n=190, 26 cty), CI excludes 0 in 3/3 specs; QUEUE = (BA+ attainment) / wage-share",
 source_paths=BR + " | " + S18,
 evidence_label="REPORT-ONLY-UNRELIABLE", confidence="high",
 what_a_generator_must_reproduce="Nothing. Do not carry 'post-secondary absorption supported' into a generator's targets.",
 note="Council relabelled X3 derived/mechanical (SYNTHESIS_017 cluster-1 row; condition 2). The number is real arithmetic; the interpretation is void."),
dict(
 fact_id="NEG-04",
 plain_english="Bigger countries do not have proportionally more or less tertiary enrolment, and the city-state comparison rests on a single usable pair.",
 value_units="X7 SIZE coefficient -1.739 (se 1.857, CI -5.377..1.900, n=30, 30 cty), NOT SUPPORTED; X8 duration ratio large/HKG = 0.667 from ONE usable pair (CHN 13.0 y vs HKG 19.5 y), i.e. HKG slower; X9 markets proxy +0.056 (CI -0.009..0.121), PARTIAL one sample only",
 source_paths=BR,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="No system-size effect on enrolment rates; no city-state speed advantage.",
 note="Read from battery-B RESULTS.csv. Audit D-19/D-21: X7's CI spans 57 log points (uninformative), X8's HKG volatility is inflated by a series break - so these are uninformative nulls, not demonstrations of absence."),
dict(
 fact_id="NEG-05",
 plain_english="Countries do not cross the same thresholds at the same income levels, and the structure around a crossing is heterogeneous rather than a shared package.",
 value_units="E2: max share of crossings inside the cross-country GDP IQR = 0.60 (secondary 90 / tertiary 50), rule >=4/6 not met; X4 inside-IQR counts LGDP 3/5, URBAN 3/5, SVCS 3/5 (tertiary set) and 2/6, 2/6, 2/6 (secondary set); X5 DATA LIMITED; X6 UNABLE (n=3)",
 source_paths=E_SUM + " | " + BR,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="Crossing years that are NOT a deterministic function of income: hold income fixed and the crossing year must still vary across systems.",
 note="Read from the E2 rows of SUMMARY.csv and the X4/X5/X6 rows of battery-B RESULTS.csv. X6's UNABLE (n=3 dated countries with both crossings) is a data limit, not a null."),
dict(
 fact_id="NEG-06",
 plain_english="A 'world-society' null model that has every country cross at the same median year invents upper-secondary crossings for four countries that never crossed.",
 value_units="upper-secondary null year 2011.5 (from ONE dated crossing, HKG); 4 never-crossed systems (CHN, JPN, KHM, PHL); 4 false crossings, 2 evidence-backed (CHN, PHL); across all four 90% levels: 7 false cells, 4 evidence-backed",
 source_paths=CR + " | " + TI,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="A generator must NOT make upper-secondary universalisation automatic at a common world date. If it does, it reproduces the rival that the data reject.",
 note="Read from battery-C RESULTS.csv Y4 row. Two caveats to carry: (i) the null rests on a single dated upper-secondary crossing (HKG), so it is thin; (ii) the two cited finals (CHN 79.39, PHL 66.05) are GER, not completion - on completion they are 87.52 and 75.03 (verified in both series files). FLAG-11."),
dict(
 fact_id="NEG-07",
 plain_english="The Philippines' upper-secondary completion sits 15 points below universal, and the one candidate explanation tested (opportunity cost) was discarded.",
 value_units="ceiling residual = 90 - 75.025 = 14.975 pp; Y1 income-partial rho(ceiling, agri share) = -0.105 (bar: <= -0.40); rho(ceiling, youth unemployment) = +0.246 (bar: <= -0.40); n=30",
 source_paths=U + " | " + CR,
 evidence_label="VERIFIED-FROM-DISK", confidence="high",
 what_a_generator_must_reproduce="A ~15 pp unreachable margin at upper-secondary that no simple demand/opportunity-cost observable explains. The generator may leave it as an unexplained residual; it may not 'explain' it with the discarded account.",
 note="Residual is arithmetic from the observed 75.025. Y1 verdict NOT SUPPORTED (both candidate correlations fail the predeclared sign/magnitude bar). A 6-system check points the other way (-0.714) and is disclosed as a tension in the same row."),
dict(
 fact_id="NEG-08",
 plain_english="'All systems share one logistic shape' is neither established nor rejected - three on-disk tests disagree.",
 value_units="A06 asymptotic F: secondary 4.210 (p=0.0030), tertiary 60.941 (p<0.001) -> reject; A07 bootstrap p: 1.000 (3 reps) / 0.125 (24 reps) -> not rejected; A08 jackknife F_all: 0.236 (p=0.9178) / 0.303 (p=0.9110) -> not robust",
 source_paths=RG,
 evidence_label="DISPUTED", confidence="high",
 what_a_generator_must_reproduce="Neither a common-shape constraint nor a rejection of it. A generator may use any shape; it must not cite 'no common shape' as evidence.",
 note="FLAG-04. A08's F cannot be a jackknife of A06's F on the same data (18x/200x smaller), so the three files are not three views of one test. SYNTHESIS_018 ruling: relabel to 'not established', drop rejection language."),
# ---------------------------------------------------------------- (i) toys
dict(
 fact_id="TOY-01",
 plain_english="If public school places expand while private providers exit, the net gain is about half the gross gain - so a generator must model exits, not just entries.",
 value_units="gross +20 seats -> net +9.73, R = 0.486; exit share 0.685; per-seed bimodal +5 (137/200 seeds) vs +20 (63/200); F=$12 variant R=0.665; cap30 variant R=0.314 with 42/200 seeds net <= 0",
 source_paths=TI,
 evidence_label="SIMULATED", confidence="high",
 what_a_generator_must_reproduce="Supply as NET of private exit. Concrete check: with a public expansion of 20% of capacity and private providers that exit whole when under break-even, net/gross must fall in [0.3, 0.7].",
 note="Toy A2, boundary-conditioned (14-seed swing). TOY_INVENTORY s2.2. The magnitude is arithmetic (R = 1 - exit_share x lost lump/gross), not an elasticity - carry the design requirement, never the number as an estimate."),
dict(
 fact_id="TOY-02",
 plain_english="A fixed entry cost on its own does not create hysteresis - entry and exit stay near-symmetric.",
 value_units="A_high = 1.0338 vs A_low = 1.0254, difference 0.008332 against a required >= 0.25; exit seats 9.80 vs entry seats 9.48; falsifier T1a/T1b both fired",
 source_paths=TI,
 evidence_label="SIMULATED", confidence="high",
 what_a_generator_must_reproduce="Do not encode a 'hysteresis parameter'. If asymmetry is needed, it must come from an asymmetric friction (separate entry and exit elasticities plus a decision-to-installation lag), not from a fixed cost.",
 note="Toy A1, the battery's 'strongest negative' - but near-symmetry is partly by construction (symmetric shock, contemporaneous decisions, censored up-shock). TOY_INVENTORY s2.1; GAPS_AND_LEADS D81 lesson 2."),
dict(
 fact_id="TOY-03",
 plain_english="Saturation at the top level is set by who is eligible, not by how many seats you build: doubling upper-secondary seats raises the ceiling only ~4.6 points, while the same money at the floor raises it ~44 points.",
 value_units="floor +44.43 pp [44.19, 44.68]; middle +11.71 [11.29, 12.12]; ceiling +4.58 [4.38, 4.77]; ceiling max +11.67 pp even with all levels doubled; secondary conversion 70.2% of added seats (15% idle, utilisation 0.851) -> T7c FAIL (>50% cap); floor peak 90.46 pp",
 source_paths=TI,
 evidence_label="SIMULATED", confidence="high",
 what_a_generator_must_reproduce="A gate/eligible-pool constraint at the ceiling (not a seat count). Check: doubling ceiling capacity must move ceiling completions by <15 pp while doubling floor capacity moves floor completions by >30 pp.",
 note="Toy C7. The 70.2% conversion falsified the Council's own <50% prediction - the informative part is that saturation is gate-determined, not level-determined (TOY_INVENTORY s2.7; D81 lesson 3). The completions=admitted identity (no dropout) forces part of this."),
dict(
 fact_id="TOY-04",
 plain_english="A law that only puts children on the register moves measured compliance about nine times more than it moves actual attendance.",
 value_units="paper law (L=1, e=0): registration +9.91 pp, attendance +1.09 pp, completion +0.51 pp -> ratio 9.09x; enforced (e=1): attendance +18.63 [18.09, 19.17], completion +20.29 [19.77, 20.81]; enforcement without law = 0.000 in all eight metrics",
 source_paths=TI,
 evidence_label="SIMULATED", confidence="high",
 what_a_generator_must_reproduce="Two distinct compliance states: enrolled-on-register and actually-attending, with a de facto enforcement parameter. Check: a de jure-only law must move register compliance >=5x its effect on attendance.",
 note="Toy C8. Magnitudes are stipulated (delta_norm=0.010, reg_norm=0.10); the e x L null is built in. Carry the measurement requirement ('register != classroom'), never the 9x as an observed effect (TOY_INVENTORY s2.8; D81 lesson 4)."),
dict(
 fact_id="TOY-05",
 plain_english="Roll-out order shifts when each level crosses, but not the gap between the floor and the ceiling - the credential pipeline sets that gap.",
 value_units="spacing S (floor->ceiling) = 21 y control, 13 y primary-first, 11 y lower-first, 11 y upper-first, 13 y simultaneous; paired S(primary_first) - S(simultaneous) = 0.0 (rule >= 2, so P10-2c fails); crossing years shift by up to 18 y across arms",
 source_paths=TI,
 evidence_label="SIMULATED", confidence="high",
 what_a_generator_must_reproduce="A pipeline-delay structure (level duration x progression) that fixes floor-to-ceiling spacing in the 11-13 year band regardless of the expansion order. Check: change the order of expansion and the spacing must move <2 y while crossing years move >5 y.",
 note="Toy D10, PARTIAL. Order-dependence of crossing years is partly a design property (a level cannot complete before the level below), so P10-1 is unfirable as a finding; the spacing negative is the transferable part (TOY_INVENTORY s2.10; D81 lesson 7)."),
dict(
 fact_id="TOY-06",
 plain_english="A demand shock to one field raises total participation, not just switching between fields - about 30% as much again as the field-switching margin.",
 value_units="open access: field-A completers +90.07, TOTAL completers +24.68 [23.93, 25.43] (rule <= 10); closed: +32.26 field / +27.16 total (ratio 0.303); field-B applications 0.00 under a field-A shock",
 source_paths=TI,
 evidence_label="SIMULATED", confidence="medium",
 what_a_generator_must_reproduce="Separate a participation margin from a switching margin in any demand-shock channel. Check: a one-field return shock must raise TOTAL completions by 15-40% of the field-specific response, not by 0.",
 note="Toy E14. Corner solution (SHOCK=2.5 > aptitude range 1.0) maximises the margin, so only the direction travels (TOY_INVENTORY s2.14; D81 lesson 8). Confidence medium for that reason."),
# ---------------------------------------------------------------- model defects
dict(
 fact_id="MOD-01",
 plain_english="The old model's enrolment ratios were 3 to 35 times too large, so every enrolment-rate milestone it reported is meaningless.",
 value_units="structure_smoke.csv, 1458 rows: ger_lower 332.8-1477.0%, ger_upper 837.3-3514.4%, ger_tertiary 583.4-3247.9%; 1458/1458 rows >100% at each of the three levels; ger_primary 64.3-206.6% (98/1458 rows >100)",
 source_paths=SMK + " | " + MI,
 evidence_label="MODEL-OUTPUT-NOT-FACT", confidence="high",
 what_a_generator_must_reproduce="The opposite: GER bounded in [0, ~105] at every level and year, with no per-country scale factor. This is exactly the Z1 validity gate.",
 note="Re-read from structure_smoke.csv. Defect D-02 (accumulated cycle lengths multiplied into the progression chain); D-16 notes the accounting check reported 0 failures while this was true. SYNTHESIS_018 Z1 makes GER in [0,105] a hard gate."),
dict(
 fact_id="MOD-02",
 plain_english="The model's reported milestone results cannot be used as facts: the tertiary crossing happened in 1960 in every arm for arithmetic reasons, and the fitted parameters were never saved.",
 value_units="M4 (tertiary GER >=50): crossed 1960 in all 12 arms incl. the no-push arm; M2 (lower-secondary >=90, observed 2024): 0/12 clean hits; M3 (upper-secondary >=90, observed never): in-window R6 12/12 but 2/12 post-window overshoots (2027, 2031); fitted theta not persisted for any arm",
 source_paths=MI + " | " + S18,
 evidence_label="MODEL-OUTPUT-NOT-FACT", confidence="high",
 what_a_generator_must_reproduce="Nothing. In particular, do not calibrate 'initialise at the observed 1960 level' from these arms; M4=1960 is caused by MOD-01, not by PHL history.",
 note="Read from MODEL_INVENTORY s3.1. Defects D-02 (M4 artefact) and D-03 (theta lost, per-arm series absent), so the 12-arm table cannot be reconstructed without a re-fit barred by R27/R12. SYNTHESIS_018 lists the 12-arm crossing table as KILL / non-citable."),
]

def main():
    assert len(ROWS) == len({r["fact_id"] for r in ROWS}), "duplicate fact_id"
    for r in ROWS:
        assert set(r) == set(COLS), (r["fact_id"], set(r) ^ set(COLS))
        assert r["evidence_label"] in {
            "VERIFIED-FROM-DISK", "REPORT-ONLY-UNRELIABLE", "DISPUTED",
            "MODEL-OUTPUT-NOT-FACT", "SIMULATED"}, r["fact_id"]
        assert r["confidence"] in {"high", "medium", "low"}, r["fact_id"]
    with open(OUT, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=COLS, quoting=csv.QUOTE_MINIMAL)
        w.writeheader()
        for r in ROWS:
            w.writerow(r)
    from collections import Counter
    print("wrote", OUT, len(ROWS), "rows")
    print(Counter(r["evidence_label"] for r in ROWS))
    print(Counter(r["confidence"] for r in ROWS))

if __name__ == "__main__":
    main()
