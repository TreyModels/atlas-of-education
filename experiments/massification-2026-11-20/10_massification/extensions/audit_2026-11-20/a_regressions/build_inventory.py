"""Build REGRESSION_INVENTORY.csv for the 2026-11-20 massification regression audit.

Read-only w.r.t. the programme: opens files only to hash them. Every metadata string
below was transcribed from a file that was read during this audit; paths are relative
to the experiment BASE.
"""
import csv, hashlib, os

BASE = "/Users/treymenefee/massification_live/experiments/massification-2026-11-20"
OUT = os.path.join(BASE, "10_massification/extensions/audit_2026-11-20/a_regressions/REGRESSION_INVENTORY.csv")

R = "10_massification/relations/"
D = R + "data/"
Q = "09_relations/"
S = Q + "scripts/"
L = "10_massification/extensions/"
FA = "10_massification/model2/runs/"

rows = []
def add(**kw):
    rows.append(kw)

G6 = "PHL;KHM;CHN;HKG;KOR;JPN"
W30 = "30-country WDI panel (Asia 19 + comparators 11)"

# ---------------------------------------------------------------- group A: relations
add(artifact="A01", path=D+"UNIVERSALIZATION_TIMING.csv", domain="universalization timing",
    estimand="First sustained year at/above each milestone threshold (M0-M4), by measure, with band and censoring status",
    data_files="data/gmr_observed_6countries_1970_2024.csv; 10_massification/data/UNIVERSALIZATION_SERIES.csv; 09_relations/data/panel_wdi_wide.csv",
    countries=G6, years="1970-2026", n="63 rows (5 levels x 6 countries + reconstructed bounds)",
    key_result="Crossings: PHL primary 2017-2021, lower-sec 2023-2024, tertiary 2024-2025, upper-sec mass <=1999 (censored), upper-sec 90 not crossed; CHN primary 2012-2014, lower-sec 2014-2016, tertiary 2016-2017; HKG primary 1978-1979; JPN/KOR mostly censored",
    status="derived", evidence_role="load-bearing",
    note="Supplies the observed crossing/spacing vector that the A4/A6/D77 verdict is scored on. 42 reconstructed bound rows flagged; never impute.")

add(artifact="A02", path=D+"universalization_timing_summary.md", domain="universalization timing",
    estimand="Human-readable rendering of A01 (30 observed/measured rows)",
    data_files="A01", countries=G6, years="1971-2026", n="30 rows",
    key_result="Same crossings as A01; censored rows shown as one-sided bounds (JPN primary ?-1971, KOR ?-2000/2003, PHL upper-sec mass ?-1999)",
    status="derived", evidence_role="load-bearing",
    note="MISLABEL: flags column renders as literal '<Flags(allows_duplicate_labels=True)>' (pandas repr leak). 'not_crossed_by_last_obs' rows print as '2024-?' / '2023-?' which reads like proximity to crossing although PHL upper-sec 90 is 75.03 in 2024 and KHM is 27.87.")

add(artifact="A03", path=D+"UNIVERSALIZATION_TIMING_PATTERN.csv", domain="universalization timing",
    estimand="Ordering and spacing of measured crossings per country",
    data_files="A01", countries=G6, years="1978-2024", n="6 rows",
    key_result="HKG order primary<tertiary<lower-sec, primary_to_lower 37.0y; PHL order primary<lower-sec<tertiary, primary_to_lower 4.5y; CHN order upper-mass<primary<lower-sec<tertiary, primary_to_lower 2.0y; upper_mass_to_tertiary 5.5y; KOR and KHM have zero measured crossings",
    status="derived", evidence_role="descriptive-only",
    note="Spacing columns are blank wherever a component is censored, so the 'ordering' is only computed on measured members: the PHL ordering omits upper-secondary mass (crossed <=1999).")

add(artifact="A04", path=D+"universalization_fits.csv", domain="universalization curve fits",
    estimand="Logistic/Gompertz K, r, t0 per series, full sample and 1980-2010 fit with 2011-2024 holdout",
    data_files="data/gmr_observed_6countries_1970_2024.csv; 10_massification/data/UNIVERSALIZATION_SERIES.csv; 09_relations/data/panel_wdi_wide.csv",
    countries=G6, years="1970-2024", n="634 parameter rows / 194 series (68 identified)",
    key_result="PHL secondary GER K=92.3(2.4) r=0.0525(0.0051) t0=1971.9(0.9) R2=0.96; KOR secondary NER 98.2 r=0.1414 t0=1974.7; CHN tertiary 125.6 r=0.1267 t0=2020.1 R2=0.995; 320 rows not_identified, 246 rows are fit-sample rows with no fit_status",
    status="derived", evidence_role="load-bearing",
    note="CHECK REFERENCE for the A1 midpoint criterion, never a parameter (SCALING_NOTES §Status). Do not quote unidentified midpoints (68/194 identified). 246/634 rows carry NaN fit_status because only full-sample rows are classified.")

add(artifact="A05", path=D+"universalization_fits_supplement.csv", domain="universalization curve fits",
    estimand="In-school rate (100-OOS) curves where the OOS series still varies",
    data_files="10_massification/data/UNIVERSALIZATION_SERIES.csv", countries=G6, years="1971-2024", n="13 rows",
    key_result="KHM lower-secondary K=86.58 r=0.4857 t0=2004.7 R2=0.913; KHM upper-secondary K=53.44 r=0.1929 R2=0.954; KOR/JPN primary R2<0 (not identified)",
    status="derived", evidence_role="descriptive-only",
    note="Correctly reports non-identification instead of forcing a fit (KOR r2 -0.35/-0.52/-0.39).")

add(artifact="A06", path=D+"universalization_common_shape.csv", domain="common-shape test",
    estimand="Asymptotic F test of a shared slope r with country-specific K and t0",
    data_files="data/gmr_observed_6countries_1970_2024.csv", countries="4-6 of six", years="1970-2024", n="4 indicators (N=84-240)",
    key_result="REJECT common slope: secondary F=4.210 (p=0.0030), tertiary F=60.941 (p<0.001), upper-secondary F=3.580 (p=0.0179), primary NER F=2.770 (p=0.0453)",
    status="check", evidence_role="descriptive-only",
    note="CONTRADICTED BY ITS OWN ROBUSTNESS FILES A07/A08 (both fail to reject). The rejection is an asymptotic F on 4-6 nonlinear series and should not be quoted as a finding without the caveat.")

add(artifact="A07", path=D+"universalization_common_shape_bootstrap.csv", domain="common-shape test",
    estimand="Residual-bootstrap p for the common-shape F",
    data_files="data/gmr_observed_6countries_1970_2024.csv; 09_relations/data/panel_wdi_wide.csv", countries="4-26", years="1970-2024", n="4 rows",
    key_result="secondary: F=4.339, boot_reps=3, p_bootstrap=1.000 -> 'NOT rejected'; tertiary: F=60.941, boot_reps=24, p_bootstrap=0.125 -> 'NOT rejected'; WDI 26-country row boot_reps=0 'bootstrap failed'",
    status="check", evidence_role="descriptive-only",
    note="UNINFORMATIVE AS RUN: 3 and 24 replications (script default reps=50), one row failed. A p of 1.000 on 3 reps is not evidence of a common shape and must not be reported as a non-rejection.")

add(artifact="A08", path=D+"universalization_common_shape_jackknife.csv", domain="common-shape test",
    estimand="Leave-one-country-out F for the same restriction",
    data_files="data/gmr_observed_6countries_1970_2024.csv", countries="5-6", years="1970-2024", n="2 indicators",
    key_result="secondary F_all=0.236 (p=0.9178), F_jack 0.196-0.290; tertiary F_all=0.303 (p=0.9110), F_jack 0.189-0.394; verdict 'rejection NOT robust'",
    status="check", evidence_role="descriptive-only",
    note="NOT A JACKKNIFE OF A06: F_all here (0.236 / 0.303) is 18x-200x smaller than A06's F (4.210 / 60.941) on the same data, so the restricted-fit routine differs. It reproduces neither A06 nor A07. Two mutually inconsistent 'robustness' files.")

add(artifact="A09", path=D+"universalization_refit_verification.csv", domain="provenance check",
    estimand="Re-fit of ger_secondary from data-hunter's series vs scout's GMR-based parameters",
    data_files="10_massification/data/UNIVERSALIZATION_SERIES.csv; A04", countries="PHL;KHM;CHN;HKG;KOR", years="1970-2024", n="5 rows",
    key_result="All 5 rows identical=True (e.g. PHL K 92.29/92.29, r 0.0525/0.0525, t0 1971.9/1971.9)",
    status="check", evidence_role="descriptive-only",
    note="Not an independent replication: both sides derive from the same underlying observations, which SCALING_NOTES states. 'identical=True' is therefore near-tautological and should not be read as a data-validation result.")

add(artifact="A10", path=D+"e6_shape_comparison.csv", domain="E6 shape model comparison",
    estimand="Out-of-sample RMSE of logistic / Gompertz / linear / exponential on the declared holdout",
    data_files="data/gmr_observed_6countries_1970_2024.csv; 10_massification/data/UNIVERSALIZATION_SERIES.csv", countries=G6, years="1970-2024", n="48 rows / 12 series",
    key_result="Holdout winners: logistic 5, Gompertz 3, linear 3, exponential 1. E.g. PHL secondary Gompertz holdout RMSE 5.983 vs logistic 6.326; CHN tertiary Gompertz 13.047; HKG tertiary logistic 14.455",
    status="check", evidence_role="load-bearing",
    note="Winner is the best of four bad options in several series (holdout RMSE 12-14 pp). Report the winning form AND the absolute error; a 'logistic beats linear' claim holds only 5/12.")

add(artifact="A11", path=D+"e6_timing_comparison.csv", domain="E6 timing comparison",
    estimand="Predicted crossing year per shape vs observed crossing midpoint, timing error in years",
    data_files="A04; A01", countries=G6, years="1970-2026", n="36 rows (9 crossing rows x 4 forms)",
    key_result="JPN tertiary: logistic 1.5y, Gompertz 3.7y, exponential -0.4y, linear 47.0y; HKG tertiary 1.5/2.4/1.0/64.8; CHN tertiary Gompertz 4.5y, exponential -1.1y, linear 141.0y; 6 of 36 cells have no prediction (NaN)",
    status="check", evidence_role="load-bearing",
    note="PARTIAL BY CONSTRUCTION: PHL and CHN tertiary have no logistic/Gompertz prediction (NaN), and all censored KOR rows have NaN error. Timing is never fitted here, consistent with R4/R19.")

add(artifact="A12", path=D+"scaling_laws.csv", domain="scaling laws",
    estimand="Within (country+year FE, CR1) and between (year FE only) log-log exponents for 15 education-economy relations",
    data_files="09_relations/data/panel_wdi_wide.csv", countries=W30, years="1970-2024", n="30 rows / 15 relations",
    key_result="Secondary GER~GDPpc within 0.090(0.124) ns / between 0.215(0.035); tertiary 0.848(0.172) / 0.567(0.082); lower-sec completion 0.247(0.119) / 0.169(0.034); primary completion~TFR -0.189(0.044) / -0.122(0.027); ag share -0.120 ns / -0.990(0.216)",
    status="derived", evidence_role="load-bearing",
    note="Source of the A3 estimator range (+0.090...+0.215 secondary; +0.567...+0.848 tertiary). Its between-exponents (0.215/0.567) DIFFER from the between-exponents in C02 (0.286/0.776) that A1 used as its target: two 'between' estimates for the same pair on disk.")

add(artifact="A13", path=D+"push_pull_tests.csv", domain="push-pull lead-lag",
    estimand="Panel Granger-style Wald tests on driver lags 1-5, two-way FE, CR1, annual changes",
    data_files="09_relations/data/panel_wdi_wide.csv", countries="27-30", years="1970-2024", n="13 tests (N=295-787)",
    key_result="ORIENTATION-CORRECTED (dependent column is the estimated outcome): education->growth null in all three (secondary GER->GDP F=1.727 p=0.125; tertiary GER->GDP F=0.648 p=0.663; completion->GDP F=1.516 p=0.181); GDPpc growth->tertiary GER F=6.522 p<0.001 sum +0.205; GDPpc growth->completion F=3.514 p=0.004 sum -0.667; secondary GER->wage-share F=4.108 p=0.001 sum +0.050",
    status="derived", evidence_role="load-bearing",
    note="HYPOTHESIS LABELS ARE INVERTED RELATIVE TO THE MODELS ESTIMATED (FLAG-00): push_pull.py regresses the `dependent` column on lags of the `driver` column, so P1/P2/P3 estimate education->growth (not growth->education) and P5 estimates GDP->tertiary GER (not the reverse). SCALING_NOTES 3 and MASSIFICATION_CLOSEOUT 2/3 quote the labels, so their push-pull sentence is reversed on both halves. The EQUIVALENT label and the R13 no-direction verdict are unaffected.")

add(artifact="A14", path=D+"event_windows.csv", domain="state-push event windows",
    estimand="Post-window mean minus pre-window linear trend (pp) around dated policy events, naive SE",
    data_files="10_massification/data/POLICY_TIMELINE.csv; 10_massification/data/UNIVERSALIZATION_SERIES.csv; 09_relations/data/panel_wdi_wide.csv; A01", countries=G6, years="1971-2024", n="20 rows (7 computed, 3 inferred, 10 UNABLE)",
    key_result="HKG 2009 free senior secondary +9.08pp (se 1.75, t=5.20); CHN 1999 HE expansion +4.70 (0.59, t=7.94); PHL 2018 free tuition -5.39 (1.80, t=-3.00); PHL 1987 Constitution -0.22 (1.54, t=-0.15); PHL K-12 +0.42 (0.83, t=0.50)",
    status="derived", evidence_role="load-bearing",
    note="Basis of D51 ('PHL state pushes do not align'). Descriptive by construction: no control group, naive SE ignores serial correlation; 10/20 rows UNABLE, not zero. Only 2 of 7 computed shifts are significant (HKG 2009, CHN 1999).")

add(artifact="A15", path=D+"capacity_alignment.csv", domain="capacity alignment",
    estimand="Capacity index 5y before / at / 5y after each milestone crossing, per country",
    data_files=D+"state_capacity.csv; "+D+"UNIVERSALIZATION_TIMING.csv", countries=G6, years="1971-2024", n="24 rows (6 countries x 4 milestones)",
    key_result="PHL primary: pre 49.5, at 84.7 (2019), change +35.2; PHL lower-sec +4.4; CHN -5.2 / -12.6; HKG -6.8 / -16.0; KOR +3.8 / +6.4; JPN/KHM rows empty",
    status="derived", evidence_role="load-bearing",
    note="+35.2 DOES NOT REPRODUCE: from state_capacity.csv the 5-year pre-window mean (2014-18) is 57.2 and the 2019 value 83.4 -> +26.1; at the A4 first-crossing year 2017 the values are 42.9 -> 57.4 (+14.4); on the panel-comparable capacity_index the change is +3.7 (2019) / +14.1 (2017). KHM/JPN rows are blank but still annotated 'censored: uses upper-bound year'.")

add(artifact="A16", path=D+"capacity_crosscountry.csv", domain="capacity cross-country",
    estimand="Spearman rho between mean 1980-2000 capacity and the crossing year, per level",
    data_files=D+"state_capacity.csv; "+D+"UNIVERSALIZATION_TIMING.csv", countries="PHL;CHN;HKG;KOR;JPN (n=5 per level)", years="1980-2000 capacity vs 1971-2024 crossings", n="4 rows, n=5 each",
    key_result="primary rho=+0.872 (p=0.054); lower-secondary rho=+0.900 (p=0.037); upper-secondary mass rho=+0.103 (p=0.870); tertiary rho=+0.800 (p=0.104)",
    status="derived", evidence_role="load-bearing",
    note="DIRECTLY CONTRADICTS THE PHASE HEADLINE: CAPACITY_LAYER.md, STATUS 3o and MASSIFICATION_CLOSEOUT all report +0.15/+0.10/+0.41/+0.30 'all ns' - numbers that appear in no file. Recomputed from components: JPN enters at capacity_within 20.0 vs 46-61 for the other four, so the two high rho are one-country artefacts of the within-country index.")

add(artifact="A17", path=D+"capacity_leadlag.csv", domain="capacity lead-lag",
    estimand="Correlation of 5-year changes in capacity_within and completion, lags -5/0/+5",
    data_files=D+"state_capacity.csv; 09_relations/data/panel_wdi_wide.csv", countries="PHL;KHM;HKG;KOR", years="1971-2024", n="12 rows (n=8-19)",
    key_result="PHL primary lag +5 r=0.509 (n=8), lag 0 0.095 (n=18), lag -5 0.066 (n=8); KHM lower-sec lag 0 r=-0.719 (n=17); HKG primary lag 0 0.530",
    status="derived", evidence_role="descriptive-only",
    note="Reports r and n only: no SE, no p, and the sign flips across countries/lags (KHM -0.72 vs HKG +0.53), so it cannot order capacity and participation. Reads as a lead-lag finding but is not one.")

add(artifact="A18", path=D+"state_capacity.csv", domain="state capacity index",
    estimand="Declared-weight composite of 7 observed fiscal/delivery components (governance 0.15 blocked, coverage renormalised)",
    data_files="09_relations/data/panel_wdi_wide.csv (WDI SE.XPD/GC.TAX/GC.XPN/SE.PRM.ENRL.TC.ZS/SE.PRM.TCHR/SP.POP.TOTL)", countries=W30, years="1971-2024", n="1,182 country-years",
    key_result="PHL capacity_within 58.89 (2005) -> 57.38 (2017) -> 83.36 (2019) -> 89.09 (2021) -> 91.47 (2024); weight_coverage falls 1.00 (2005) -> 0.90 (2017) -> 0.60 (2019-23) -> 0.55 (2024)",
    status="derived", evidence_role="load-bearing",
    note="CANONICAL ONLY AS A DERIVED COMPOSITE (D74). Composition break at 2014 (3 -> 6 components, coverage 0.35 -> 0.90) and at 2018 (6 -> 5): the trajectory it produces is partly a coverage artefact. JPN 1980-2000 sits at 20.0, far below the other five.")

add(artifact="A19", path=R+"SCALING_NOTES.md", domain="relations note",
    estimand="Method, caveats and the constraint list for the scaling/universalization layer",
    data_files="A04-A13", countries=G6, years="1970-2024", n="6 sections",
    key_result="Declares: fits are checks/constraints not targets; common-shape rejection provisional; 68/194 identified; 'no wages/earnings by education' is the largest push-pull gap",
    status="derived", evidence_role="descriptive-only",
    note="Honest on caveats, but its 'rejection is provisional' reading is weaker than its own files allow: A07 and A08 both fail to reject, so no rejection should be reported at all.")

add(artifact="A20", path=R+"EVENT_WINDOWS.md", domain="relations note",
    estimand="Narrative of the 20 event windows and the PHL/HKG/CHN alignment verdicts",
    data_files="A14; A01; 10_massification/data/POLICY_TIMELINE.csv", countries=G6, years="1971-2024", n="6 sections",
    key_result="PHL: discrete pushes do not align (1987->2017-21 = 31y; K-12 after upper-sec mass; free tuition window negative); HKG 2009 and CHN 1999 are the only aligned markers",
    status="derived", evidence_role="load-bearing",
    note="SUPERSEDED IN PART: §6 says SCHOOL_EXPANSION.csv 'was not on disk'; it now exists (27 rows) and is PHL-only. Policy dates are 'not primary-verified' by its own admission (see Y5/data-hunter labels).")

add(artifact="A21", path=R+"CAPACITY_LAYER.md", domain="relations note",
    estimand="Capacity index construction, PHL alignment narrative, cross-country test, model gate",
    data_files="A15-A18", countries=G6, years="1971-2024", n="5 sections",
    key_result="Claims PHL '+35.2 points into the primary >=90 crossing' and cross-country rho +0.15/+0.10/+0.41/+0.30 all ns",
    status="derived", evidence_role="load-bearing",
    note="Its two headline numbers are the ones that fail verification (A15 +35.2; A16 rhos). §2 also uses capacity_within 84.7 at 2019 while the index at the 2017 crossing year is 57.4. Its own caveat (iv) already flags the coverage composition issue.")

# ---------------------------------------------------------------- group B: 09_relations
add(artifact="B01", path=Q+"RELATION_CANDIDATES.csv", domain="relation register",
    estimand="49 graded candidate relations with estimate, SE/range, sample, method, model mapping",
    data_files="B02-B18 (each row names its own file+spec)", countries="6-30 depending on row", years="1970-2024", n="49 rows (R01-R49)",
    key_result="Grades: 1 plausibly-causal (R07 fertility->completion), 21 correlational, 7 not-identifiable/blocked, 1 imported causal target (R28 nurse licensing, 9.0 licensed per migrant); 2 unusable-as-parameter (R26, R29)",
    status="derived", evidence_role="load-bearing",
    note="Only grade-1 causal estimate (R28) is IMPORTED from literature (Abarcar & Theoharides), not re-estimated on disk; its replication experiment E3 is DATA BLOCKED. R30 (school construction) is UNVERIFIED at source.")

add(artifact="B02", path=Q+"data/panel_results.csv", domain="30-country panel",
    estimand="Two-way FE and first-difference coefficients for 30 education-economy specs",
    data_files=Q+"data/panel_wdi_wide.csv", countries=W30, years="1970-2024", n="66 rows (30 specs x levels/lag + 9 FD)",
    key_result="Tertiary GER~GDPpc 0.848(0.172); spending->secondary 0.152(0.110) ns, FD 0.014; fertility->primary completion -0.189(0.044); GDP growth~tertiary GER t-15 -1.035(0.240); PTR->completion levels +0.385(0.109) vs FD -1.243(0.318)",
    status="derived", evidence_role="load-bearing",
    note="Source of the two sign constraints the model is judged on (income->tertiary positive; education->growth negative). The PTR row is a documented sign conflict (R11) and must not be used as a parameter.")

add(artifact="B03", path=Q+"data/panel_heterogeneity.csv", domain="country typology",
    estimand="Split-sample FE coefficients across 5 typologies x 11 relations",
    data_files="B02; "+Q+"data/country_typology.csv", countries=W30, years="1970-2024", n="110 rows",
    key_result="Spending->secondary Asia +0.189(0.090) vs non-Asia +0.010(0.106); private share Asia +0.086(0.016) vs non-Asia +0.003; tax->spend Asia +0.541(0.125) vs non-Asia -0.320(0.370)",
    status="derived", evidence_role="descriptive-only",
    note="Supports the 'capacity-binding state' typology (T1-T5); correlational, and the Asia/non-Asia split is post hoc rather than predeclared.")

add(artifact="B04", path=Q+"data/country_typology.csv", domain="country typology",
    estimand="1985-2000 country means and group thresholds used for splits",
    data_files=Q+"data/panel_wdi_wide.csv", countries=W30, years="1985-2000", n="30 rows",
    key_result="Thresholds: GDP pc median US$1,706; tax/GDP 13.1%; 1990 secondary GER 47.3%; urban 40.2%",
    status="observed", evidence_role="descriptive-only",
    note="Thresholds are medians of the analysed sample, so 'low/high' groups are sample-relative, not absolute.")

add(artifact="B05", path=Q+"data/event_windows.csv", domain="event windows (WDI)",
    estimand="Interrupted-time-series log jump at 6 policy events, WDI outcomes",
    data_files=Q+"data/panel_wdi_wide.csv", countries="PHL;CHN;IDN;THA;MYS", years="1970-2024", n="6 rows",
    key_result="PHL 2018 log_ger_t -0.0878 (se 0.0200, t=-4.38, -8.40%); PHL 2016 log_ger_s -0.0081 (t=-1.16, ns); CHN 1986 +0.0914 (t=1.90, +9.57%); THA 1999 -0.1022 (t=-3.78); MYS 1996 +0.0223 (t=2.19)",
    status="derived", evidence_role="descriptive-only",
    note="Same events, different magnitudes from B06 and A14: PHL 2018 tertiary is -8.40% here, -28.87% in B06 and -5.39pp in A14. Three numbers for one event; the source choice, not the policy, drives the size.")

add(artifact="B06", path=Q+"data/event_windows_gmr.csv", domain="event windows (GMR)",
    estimand="Same ITS design on the 6-country GMR observed series",
    data_files="data/gmr_observed_6countries_1970_2024.csv", countries="PHL;JPN;CHN", years="1970-2024", n="5 rows",
    key_result="PHL 2018 ger_tertiary -0.3407 (se 0.0766, t=-4.45, -28.87%); PHL 2016 ger_secondary -0.0244 (t=-0.75, ns); CHN 1986 +0.2774 (t=1.50, +31.97%); JPN 1980 -0.0980 (ns)",
    status="derived", evidence_role="descriptive-only",
    note="Used by COUNTRY_TYPOLOGY/R18-R19. CHN 1986 pre-trend noise is 17.3% of the level, so the +32% jump is not separable from trend.")

add(artifact="B07", path=Q+"data/shadow_gradients.csv", domain="shadow education",
    estimand="Observed tutoring participation / spend gradients by stage, income, urbanisation, policy",
    data_files="04_data/shadow_round2/ (survey values); literature tables as cited per row", countries="HKG;KOR;JPN;KHM;CHN", years="2003-2023", n="17 rows (12 observed + 5 derived/labels)",
    key_result="HKG stage 35.1->46.6->70.3% (gate gradient +35.2pp); KOR income <3m 183 vs >=8m 671 thousand won (elasticity 1.325); KOR participation 86.0->66.4% while spend 398->491; JPN Tokyo 57.9 vs Akita 22.1%",
    status="observed", evidence_role="descriptive-only",
    note="Single surveys (HKG n=630 pupils in 6 schools; KHM one district/6 schools; CHN 2022 is a newspaper headline 'upper bound'). No SEs, no design: these are calibration priors, not estimates.")

add(artifact="B08", path=Q+"data/complexity_results.csv", domain="economic complexity",
    estimand="ECI -> schooling / formalisation / growth, two-way FE",
    data_files=Q+"data/economic_complexity_panel.csv; raw/eci_growth_proj_rankings.csv", countries=W30, years="1995-2024", n="14 rows (C1-C12 + horse races)",
    key_result="ECI->tertiary 0.306(0.140); ECI->lower-sec completion 0.197(0.069); ECI->secondary 0.165(0.075); ECI->growth -0.142(0.105) ns; horse race: ECI 0.120(0.075) vs log GDPpc 0.845(0.198)",
    status="derived", evidence_role="descriptive-only",
    note="The tertiary-complexity link does not survive the income control; the file reports this itself. Not wired into any model.")

add(artifact="B09", path=Q+"data/complexity_conditioning.csv", domain="economic complexity",
    estimand="Centred-ECI interactions on the spending and returns channels",
    data_files="B08", countries=W30, years="1995-2024", n="14 rows (X1-X8)",
    key_result="spend x ECI 0.081(0.080) ns; cmpt x ECI -> growth -0.039(0.015); tertiary x ECI -> growth -0.077(0.020); income x ECI 0.014(0.010) ns",
    status="derived", evidence_role="descriptive-only",
    note="Clean null on spending x complexity; the negative schooling x ECI interaction is the only survivor and is explicitly flagged as possibly convergence rather than complexity.")

add(artifact="B10", path=Q+"data/complexity_metric_choice.csv", domain="economic complexity",
    estimand="Coverage / correlation / stability comparison of ECI variants",
    data_files=Q+"data/economic_complexity_panel.csv", countries="6 then 30", years="1995-2024", n="2 rows",
    key_result="eci_sitc vs eci_hs92 r=0.983; HS92 t_gdp 3.29 (R2 0.183) vs SITC 2.43 (0.147); yr-on-yr sd 0.127 vs 0.132",
    status="derived", evidence_role="descriptive-only",
    note="Methodological, correctly labelled 'not an estimate'.")

add(artifact="B11", path=Q+"data/eci_growth_crosssection.csv", domain="economic complexity",
    estimand="ECI growth premium in year-FE cross-section, with robustness",
    data_files="B08", countries=W30, years="1995-2024", n="5 rows",
    key_result="ECI -> 10y growth -0.068 (se 0.067) year-FE; -0.158 (0.101) two-way FE; growth_proj -0.004 (0.020)",
    status="derived", evidence_role="descriptive-only",
    note="A genuine failure to replicate the published ECI premium; states the sample/period difference and does not overclaim.")

add(artifact="B12", path=Q+"data/eci_literacy_results.csv", domain="literacy x ECI",
    estimand="E1-E17: ECI x GDP x literacy x growth",
    data_files=Q+"data/panel_wdi_eci.csv; raw/eci_growth_proj_rankings.csv", countries="23-30", years="1975-2024", n="17 rows",
    key_result="ECI~GDP 0.322(0.098) and reverse 0.568(0.145); ECI~adult literacy 0.001(0.005) ns; ECI~primary completion t-10 0.593(0.176); literacy~GDP 3.91(2.67) ns",
    status="derived", evidence_role="descriptive-only",
    note="The flow-not-stock asymmetry is the useful result; the reverse regression shows joint determination, so no direction claim is possible.")

add(artifact="B13", path=Q+"data/literacy_cohort_decomposition.csv", domain="literacy demography",
    estimand="Entrant / exit / residual decomposition of 5-year adult-literacy change",
    data_files=Q+"data/panel_wdi_eci.csv", countries="25", years="1975-2024", n="241 country-periods",
    key_result="Median 62-66% of the literacy gain is cohort replacement; entrant-flow coefficient 1.655 (se 0.526); KHM/LAO/LKA/VNM/THA show replacement >1 (negative residual)",
    status="derived", evidence_role="descriptive-only",
    note="Exit component is bounded, not estimated; negative residuals are most plausibly series revisions, which the file says. Do not calibrate from it.")

add(artifact="B14", path=Q+"data/literacy_decomposition_regressions.csv", domain="literacy demography",
    estimand="Regressions behind the replacement share",
    data_files="B13", countries="25", years="1975-2024", n="3 rows",
    key_result="Entrant-flow coefficient 1.655 (se 0.526) on 5-year literacy change; replacement share 0.62-0.66",
    status="derived", evidence_role="descriptive-only",
    note="Three rows for a 241-observation panel: the reported coefficient depends on the bounded exit assumption, so it is a range, not a point.")

add(artifact="B15", path=Q+"data/literacy_country_examples.csv", domain="literacy demography",
    estimand="Per-country pyramid/literacy example rows (PHL, CHN, ...)",
    data_files="B13", countries="10", years="1980-2020", n="10 rows",
    key_result="PHL 1980->2020 literacy +15.2pp while 0-14 share 44.3->30.7; CHN +31.2pp with 65+ 4.6->12.6",
    status="derived", evidence_role="descriptive-only",
    note="Illustrative only; selected countries, no sampling frame.")

add(artifact="B16", path=Q+"data/population_pyramids.csv", domain="demography",
    estimand="3-band population shares plus derived 15-24 proxy",
    data_files=Q+"raw/wdi/ (SP.POP.0014/1564/65UP.TO.ZS, SP.POP.TOTL)", countries=W30, years="1960-2024", n="60 rows",
    key_result="3-band only (0-14 / 15-64 / 65+); 5-year bands unavailable from WDI API v2 ('invalid value'); 15-24 proxied from births 15y earlier (derived, flagged)",
    status="observed", evidence_role="descriptive-only",
    note="The 15-24 proxy is a declared derivation, not an observation - a trap for anyone reading the column as measured.")

add(artifact="B17", path=Q+"data/economic_complexity_panel.csv", domain="economic complexity",
    estimand="6-country ECI panel merged with WDI outcomes (model-input file)",
    data_files="04_data/complexity/ECONOMIC_COMPLEXITY.csv; "+Q+"data/panel_wdi_wide.csv", countries=G6, years="1995-2024", n="180 rows x 27 cols",
    key_result="Coverage 30/30 years for eci_sitc and eci_hs92 in all six; eci_hs12 only 2012-2024; growth_proj 2004-2024",
    status="observed", evidence_role="descriptive-only",
    note="Declared usable model input; no proxies. Not used by any model on disk.")

add(artifact="B18", path=Q+"data/economic_complexity_panel_30ctys.csv", domain="economic complexity",
    estimand="ECI column set for the 30-country panel tests",
    data_files=Q+"raw/eci_growth_proj_rankings.csv", countries=W30, years="1995-2024", n="895 rows",
    key_result="ECI SITC + HS92 (+HS12, growth_proj) for 30 countries; underpins B08-B11",
    status="observed", evidence_role="descriptive-only",
    note="Supporting data for the complexity rows; no independent estimation.")

add(artifact="B19", path=Q+"data/panel_wdi_wide.csv", domain="panel data",
    estimand="30-country x 45-indicator observed WDI panel, wide",
    data_files="raw/wdi/*.json (128 archived payloads)", countries=W30, years="1970-2024", n="1,950 rows x 65 cols",
    key_result="Observed cells only (value is None dropped, never filled); 1,650 country-years with any data; underlying data for A12/A13/A18/B02/B03",
    status="observed", evidence_role="load-bearing",
    note="The single most reused input in the audit (7 artefacts). Every within/between exponent and heterogeneity split traces here.")

add(artifact="B20", path=Q+"data/panel_wdi_long.csv", domain="panel data",
    estimand="Long form of the 30-country WDI panel",
    data_files="B19", countries=W30, years="1970-2024", n="63,570 rows",
    key_result="Long (iso3, indicator_code, year, value) form used by Y2/Y3 ('SE.SEC.ENRL.TC.ZS', 'SE.PRM.CMPT.ZS')",
    status="observed", evidence_role="load-bearing",
    note="Consistent with B19; used as the PTR source in Y3's sensitivity file.")

add(artifact="B21", path=Q+"data/panel_wdi_eci.csv", domain="panel data",
    estimand="WDI panel joined to ECI",
    data_files="B19; B18", countries=W30, years="1970-2024", n="1,950 rows x 66 cols",
    key_result="Adds eci_sitc/eci_hs92 to the wide panel; underlying data for B12-B16",
    status="observed", evidence_role="descriptive-only",
    note="Join is on (iso3, year); ECI exists only from 1995, so pre-1995 rows carry NaN ECI.")

add(artifact="B22", path=Q+"DATA_PATTERNS.md", domain="relations note",
    estimand="Narrative of the 66 panel specs, 110 splits, 11 event windows, 17 gradients",
    data_files="B02-B07", countries=W30, years="1970-2024", n="9 sections",
    key_result="States the identification warning once ('panel associations, not experiments'); PTR sign conflict disclosed; education->growth -1.035 flagged as a failure of eps_ec>0",
    status="derived", evidence_role="load-bearing",
    note="Claims '19 event-window estimates' but the two files hold 6 + 5 = 11 rows. Otherwise the numbers I spot-checked reproduce.")

add(artifact="B23", path=Q+"COUNTRY_TYPOLOGY.md", domain="relations note",
    estimand="Six conditional relations (T1-T6) and country-preset implications",
    data_files="B03; B04", countries=W30, years="1970-2024", n="6 tables",
    key_result="T1 spending Asia +0.189 vs +0.010; T2 private low-tax +0.102 vs -0.065; T3 tax->spend Asia +0.541; T4 income->tertiary Asia +1.075; T6 fertility negative in every split",
    status="derived", evidence_role="descriptive-only",
    note="The 'one capacity_binding flag' recommendation is the most model-relevant output of the relations layer and is untested as a model switch.")

add(artifact="B24", path=Q+"LITERACY_ECI_DEMOGRAPHY.md", domain="relations note",
    estimand="Literacy x GDP x ECI + cohort replacement + pyramid caveat",
    data_files="B12-B16", countries="23-30", years="1960-2024", n="17 tests + 2 decompositions",
    key_result="62-66% of literacy gains is cohort replacement; ECI tracks the flow (0.593) not the stock (0.001); ECI growth premium does not replicate (-0.068)",
    status="derived", evidence_role="descriptive-only",
    note="No KOR/JPN/HKG adult literacy series, so the developed benchmarks are absent from the decomposition; CHN literacy too sparse for the decomposition.")

add(artifact="B25", path=Q+"LITERATURE_ELASTICITIES.md", domain="relations note",
    estimand="Verified literature elasticities used as calibration priors",
    data_files="02_lit/ECON_TARGETS.csv; 02_lit/ECON_LIT.md", countries="world / EAP", years="1950-2024", n="~12 rows",
    key_result="Return to schooling 8.8%/yr (Psacharopoulos & Patrinos, FULL-TEXT); EAP 8.7%; PHL-US place premium 3.99x; nurses 9.0 per migrant (Abarcar & Theoharides); country Mincer returns NOT SUPPLIED",
    status="observed", evidence_role="DATA BLOCKED",
    note="Declared PARTIAL: spending->enrolment, school construction (Duflo not retrieved) and teacher supply have NO verified source. The requested domains are named as gaps, not filled - correct labelling.")

add(artifact="B26", path=Q+"MODEL_PLUG_MAP.md", domain="relations note",
    estimand="Mapping from each relation to a specific model parameter / functional form",
    data_files="B01; 05b_experiments/loop2/code/twoway.py; massabm", countries="n/a", years="n/a", n="3 tables (A twoway, B massabm, C do-not-plug)",
    key_result="Exact plug points (e.g. eps_ec, inc_sig, cap_cost, tuition_path, T_S/T_C); explicit 'do not plug in' list including eps_ec=0.6",
    status="derived", evidence_role="descriptive-only",
    note="The only place where each relation's model consequence is written down; it is a design document, not evidence.")

add(artifact="B27", path=Q+"STATUS.md", domain="relations note",
    estimand="Task status and completeness claims for the 09_relations layer",
    data_files="B01-B26", countries="n/a", years="n/a", n="3 sections",
    key_result="Claims: 30 -> 40 -> 49 register rows; 66 panel specs; 110 splits; 19 event windows; 17 gradients; all CSVs regenerable",
    status="derived", evidence_role="descriptive-only",
    note="'19 event-window estimates' does not match the 11 rows on disk. 'Every CSV is regenerable' is not true as written: every script reads 04_data/data/gmr_observed_... which does not exist (the file is at data/gmr_observed_...).")

# ---------------------------------------------------------------- group C: cited inputs
add(artifact="C01", path="data/gmr_observed_6countries_1970_2024.csv", domain="observed source series",
    estimand="UIS/GMR observed indicator panel, six countries, 32 indicators",
    data_files="UIS/GMR (source_detail per row)", countries=G6, years="1970-2026", n="4,635 rows",
    key_result="PHL completion_primary 83.16 (1999) / 87.45 (2013) / 91.92 (2017) / 98.30 (2024); completion_lower_secondary 88.44 (2023) / 92.41 (2024); completion_upper_secondary 76.43 (2017) / 75.03 (2024); ger_tertiary 47.41 (2024) / 51.07 (2025)",
    status="observed", evidence_role="load-bearing",
    note="PATH DRIFT: every script and note cites 04_data/data/gmr_observed_6countries_1970_2024.csv, which does not exist; the file is at data/. As written, A04-A11, A14, A18, B06 and the timing layer cannot be regenerated. The observed signature itself verifies.")

add(artifact="C02", path=FA+"scaling_estimates.csv", domain="scaling targets",
    estimand="Five-estimator exponents for 10 relations on WDI30 and UIS6",
    data_files="09_relations/data/panel_wdi_wide.csv; 10_massification/data/UNIVERSALIZATION_SERIES.csv", countries="30 and 6", years="1970-2024", n="91 rows",
    key_result="GER secondary~GDPpc between 0.2858(0.0452) [= A1 target +0.286]; tertiary between 0.7761(0.0864) [= A1 target +0.776]; lower-sec completion between 1.1740(0.1572); returns vs schooling row = UNABLE ('no earnings microdata')",
    status="derived", evidence_role="load-bearing",
    note="The A1 gate targets come from the BETWEEN estimator here, while A12's between-exponents are 0.215/0.567. The FAIL is sign-robust (generated -2.7 to -0.3), but the numeric target varies ~3x across artefacts on disk.")

add(artifact="C03", path="10_massification/data/UNIVERSALIZATION_TIMING.csv", domain="observed source series / timing",
    estimand="Crossing year per level x threshold x measure, with band, censoring and confidence (data-hunter layer)",
    data_files="UIS/WDI observed series; UN WPP-2024 population for the reconstructed rows", countries=G6, years="1970-2026", n="128 rows (80 observed, 42 reconstructed, 6 unable)",
    key_result="PHL primary 95 NER left-censored at 1976 (NER 96.79); PHL primary 95 GER left-censored 1971 (GER 99.54); PHL lower-secondary 90 GER 2014 (band 2009-2014); PHL tertiary 50 GER 2025 (band 2024-2025); CHN lower-secondary 90 GER 2006; HKG primary 95 NER 1979",
    status="observed", evidence_role="load-bearing",
    note="SECOND TIMING LAYER, SAME FILENAME AS A01, DIFFERENT CONTENT: 128 rows vs 63, first-at-above vs first-sustained, GER/NER vs completion. PHL primary is 1971/1976 here and 2017 in A01. Not wrong - the measures differ - but nothing in either file disambiguates them, and the A4 milestone mapping mixes measures by level. Reconstructed CHN GER differs from observed GER by median 15.28 pp (its own notes), which is too large to be called a validated reconstruction.")

add(artifact="C04", path=R+"logs_fit.txt", domain="run log", estimand="Console output of the common-shape F test (4 indicators)",
    data_files="data/gmr_observed_6countries_1970_2024.csv", countries="4-6", years="1970-2024", n="8 lines",
    key_result="Reproduces A06 exactly (secondary 4.210/0.0030; tertiary 60.941/0.0000; upper-sec 3.580/0.0179; primary NER 2.770/0.0453) plus 'fits rows: 634 | series: 194'",
    status="derived", evidence_role="superseded",
    note="Superseded by A06; useful only as corroboration that A04/A06 came from one run. Its path reference is the broken 04_data/data one.")

add(artifact="C05", path=R+"logs_e6.txt", domain="run log", estimand="E6 shape/timing run log",
    data_files="none", countries="none", years="none", n="0 bytes",
    key_result="EMPTY FILE (0 bytes)",
    status="derived", evidence_role="superseded",
    note="UNREADABLE/NON-EXISTENT CONTENT: the E6 log exists but is empty, so the E6 run (A10/A11) has no console evidence on disk. Recorded as an empty file, not inferred.")

add(artifact="C06", path="10_massification/data/UNIVERSALIZATION_SERIES.csv", domain="observed source series",
    estimand="Universalization/enrolment/completion series for the six countries, observed-only with derived flags",
    data_files="UIS/WDI/national (source + source_detail per row)", countries=G6, years="1970-2026", n="2,458 rows",
    key_result="Underlies A01/A04/A05/A10/A11/A14 and Y3/Y4; carries unit, source, status (observed/derived/check/reconstructed) per row",
    status="observed", evidence_role="load-bearing",
    note="The only series file whose path in the scripts is correct. 2,458 rows matches the D16 claim in STATUS.")

add(artifact="C07", path="10_massification/data/JOBS_AND_MARKETS_PANEL.csv", domain="observed source series",
    estimand="39 labour-market/economy series for the six countries, observed-only",
    data_files="WDI/ILO-modelled (labelled per row)", countries=G6, years="1991-2024", n="5,622 rows",
    key_result="Supplies the formal-absorption, wage-share, agri-share, youth-unemployment and GDP series used by X1, X3, Y1 and Y5",
    status="observed", evidence_role="descriptive-only",
    note="Sector/wage series are ILO-modelled, not measured (labelled in-file), which is a standing caveat for every absorption-type result built on it.")

# ---------------------------------------------------------------- group D: lab batteries
E = L + "lab_2026-11-20/results/"
add(artifact="D01", path=E+"E1_income_gradient.csv", domain="lab E1", estimand="Within-system upper-secondary GER on log GDP, 6 systems",
    data_files="10_massification/data/UNIVERSALIZATION_SERIES.csv; 09_relations/data/panel_wdi_wide.csv", countries=G6, years="1995-2024", n="93 obs / 5 clusters",
    key_result="Within slope +56.07 GER pp per log GDP (se 19.56); between +159.9 (n=5, uninterpretable); drop-CHN +71.4; verdict 'strong'", status="derived", evidence_role="descriptive-only",
    note="LABEL OVERSTATES: 5 clusters, and its own replication E10 fails (14.74, CI -1.6..+31.0). 'Strong' should read 'not transferable, driven by CHN/KHM'. Consistent with A12 (log-log within 0.090), not with a 56 pp law.")
add(artifact="D02", path=E+"E2_crossing_structure.csv", domain="lab E2", estimand="Fraction of crossings inside the cross-country GDP/urban/agri IQR",
    data_files="A01; 09_relations/data/panel_wdi_wide.csv", countries=G6, years="1970-2024", n="9 milestone cells",
    key_result="Max fraction 0.60 (3/5 or 5/6); no milestone reaches the 4/6 rule -> 'not typical'", status="derived", evidence_role="descriptive-only",
    note="Threshold 4/6 with 5 usable cells makes 0.60 vs 0.667 a one-country difference; the verdict is threshold-driven and should be read as 'no single crossing package', not as a measured absence.")
add(artifact="D03", path=E+"E3_regional_equalization.csv", domain="lab E3", estimand="PHL regional Gini~mean-years-schooling slope by birth cohort",
    data_files="10_massification/data/BASELINE_SERIES.csv", countries="PHL 17 regions", years="1960-1994 cohorts", n="17 regions x 2 cohorts",
    key_result="Gini~MYS slope -0.0551 (se 0.0040, 1960-64) and -0.0511 (se 0.0028, 1990-94); Gini fell >=0.02 in 17/17 regions", status="derived", evidence_role="descriptive-only",
    note="Cleanest lab result (also replicated as X10-X12). Limitation stated in the file: regional tertiary enrolment is unobserved, so this is attainment/inequality proxy evidence around a national expansion.")
add(artifact="D04", path=E+"E4_scale_shape.csv", domain="lab E4", estimand="Duration and volatility ratios large-country/HKG",
    data_files="A01; A04", countries="HKG;CHN;PHL;KHM", years="1970-2024", n="<=4 per side",
    key_result="Duration ratio 1.10 (no clear difference); volatility ratio 0.326 (large countries smoother)", status="derived", evidence_role="descriptive-only",
    note="No SE, n<=4, and HKG volatility is inflated by a series break (disclosed in X8). Should not be quoted as a finding about city-states.")
add(artifact="D05", path=E+"E5_tertiary_structure.csv", domain="lab E5", estimand="Tertiary GER on services share, within FE",
    data_files=Q+"data/panel_wdi_wide.csv", countries=W30, years="1970-2024", n="358 obs / 15 clusters",
    key_result="Within services slope -0.495 (se 0.217); sign flips to +1.82 without log GDP and +0.42 without urban -> 'not robust'", status="derived", evidence_role="descriptive-only",
    note="Correctly self-labelled not robust. Shows collinearity suppression, not an effect.")
add(artifact="D06", path=E+"E6_formalisation_completion.csv", domain="lab E6", estimand="Within correlation of completion and wage-share, lag 0/5",
    data_files="10_massification/data/UNIVERSALIZATION_SERIES.csv; 09_relations/data/panel_wdi_wide.csv", countries="4 systems with completion", years="1995-2024", n="59 (lag0) / 39 (lag5)",
    key_result="lag0 r=+0.645; lag5 r=+0.586 (n=39, 4 countries) -> 'association'", status="derived", evidence_role="descriptive-only",
    note="4 countries and no SE/p; the lag-5 cell is weaker than lag-0, so it does not establish an ordering. 'association' is the right label.")
add(artifact="D07", path=E+"E7_capacity_around_crossings.csv", domain="lab E7", estimand="Capacity change around lower-secondary crossings, 3 dimensions",
    data_files="10_massification/data/STATE_CAPACITY.csv", countries="3 systems with coverage", years="1995-2024", n="3",
    key_result="Only delivery has coverage: delta -0.152 SD -> 'DATA LIMITED (only 1 dimension with coverage)'", status="derived", evidence_role="DATA BLOCKED",
    note="Correctly refuses to report a capacity-linked result. The fiscal/enforcement dimensions are absent at the needed windows - a data finding.")
add(artifact="D08", path=E+"E8_phl_strain.csv", domain="lab E8", estimand="PHL dPTR on dGER during secondary expansion",
    data_files="10_massification/data/UNIVERSALIZATION_SERIES.csv; 09_relations/data/panel_wdi_wide.csv", countries="PHL", years="1995-2024", n="35",
    key_result="Slope +0.245 (se 0.185) -> 'no strain' (rule >1.0)", status="derived", evidence_role="descriptive-only",
    note="A null with a wide CI on one country; also depends on which PTR series is used (WDI primary vs the PIDS classroom-based high-school ratio, which STATUS 3o says must never be spliced).")
add(artifact="D09", path=E+"E9_remittances.csv", domain="lab E9", estimand="Remittance associations with spending and enrolment growth",
    data_files="09_relations/data/panel_wdi_wide.csv", countries="6", years="1995-2024", n="116-139",
    key_result="spending -0.046 (se 0.031); secondary GER growth -0.0007 (0.0013); tertiary growth -0.0024 (0.0014) -> 'no association'", status="derived", evidence_role="descriptive-only",
    note="Consistent with B02 (S12 ns). Small n and remittances measured as %GDP; a null here is weak evidence, not a refutation.")
add(artifact="D10", path=E+"E10_replication.csv", domain="lab E10", estimand="30-country replication of E1",
    data_files=Q+"data/panel_wdi_wide.csv", countries=W30, years="1995-2024", n="14",
    key_result="Pooled slope +14.74 (se 8.32; CI -1.56..+31.04) vs E1 +56.07; 'does not replicate'", status="derived", evidence_role="descriptive-only",
    note="The most important E-cell: it is the internal falsifier of the E1 headline. n=14 usable upper-secondary observations is thin.")

B = L + "lab_2026-11-20_b/"
add(artifact="D11", path=B+"cluster_1_absorption/results/X1_absorption_6systems.csv", domain="lab X1", estimand="Tertiary GER on formal-absorption proxy, 6 systems",
    data_files="10_massification/data/JOBS_AND_MARKETS_PANEL.csv", countries=G6, years="1995-2024", n="139 / G=6",
    key_result="Within slope -0.86 (se 1.56; CI -3.91..+2.20); services proxy -1.90 (CI -5.92..+2.13) -> NOT SUPPORTED", status="derived", evidence_role="descriptive-only",
    note="Correct verdict under falsifier precedence; the worker's PARTIAL reading is retained in the note. Proxy is declared, not a measured absorption rate.")
add(artifact="D12", path=B+"cluster_1_absorption/results/X2_absorption_30countries.csv", domain="lab X2", estimand="30-country replication of X1",
    data_files=Q+"data/panel_wdi_wide.csv", countries=W30, years="1995-2024", n="654 / G=30",
    key_result="Within slope +0.80 (se 0.61; CI -0.40..+2.00) - inside X1 CI but opposite sign -> NOT SUPPORTED", status="derived", evidence_role="descriptive-only",
    note="Both X1 and X2 are nulls with CIs spanning zero; the 'opposite sign' story is a point-estimate artefact and should not be over-read.")
add(artifact="D13", path=B+"cluster_1_absorption/results/X3_queue_depth.csv", domain="lab X3", estimand="Derived queue-depth ratio (BA+ attainment / wage share) vs tertiary GER",
    data_files="10_massification/data/JOBS_AND_MARKETS_PANEL.csv; UNIVERSALIZATION_SERIES", countries=W30, years="1995-2024", n="190 / G=26",
    key_result="+0.366 (CI +0.198..+0.534); log-log +0.637; first-diff +0.255; 3/3 CIs exclude 0 -> SUPPORTED", status="derived", evidence_role="descriptive-only",
    note="RELATIVE-MEASURE CAVEAT: the ratio's numerator is a lagged attainment stock and its denominator a wage share, so the cell is close to mechanical (Council relabelled it derived/mechanical). 'SUPPORTED' overstates: nothing here measures a queue.")
add(artifact="D14", path=B+"cluster_2_tertiary_crossings/results/X4_crossing_typicality.csv", domain="lab X4", estimand="Structure typicality at tertiary vs secondary crossings",
    data_files="A01; 09_relations/data/panel_wdi_wide.csv", countries=G6, years="1970-2024", n="8 cells",
    key_result="Tertiary 3/5 on all three vars; secondary 2/6 on all three; both fail >=4/6 -> NOT SUPPORTED", status="derived", evidence_role="descriptive-only",
    note="Denominator reinterpreted from 6 to 5 countries (disclosed). Same threshold sensitivity as E2.")
add(artifact="D15", path=B+"cluster_2_tertiary_crossings/results/X5_package_contrast.csv", domain="lab X5", estimand="Tertiary-50 vs secondary-90 structure package contrast",
    data_files="A01; 09_relations/data/panel_wdi_wide.csv", countries="4 vs 3 dated", years="1970-2024", n="4 vs 3",
    key_result="Median difference / pooled IQR: GDP 0.914 (different), urban 0.795 (different), services 0.296 (same) -> DATA LIMITED", status="derived", evidence_role="DATA BLOCKED",
    note="Below the declared n>=4 per set minimum. Correctly not promoted to a package claim; the point estimates are suggestive only.")
add(artifact="D16", path=B+"cluster_2_tertiary_crossings/results/X6_spacing_structure.csv", domain="lab X6", estimand="Secondary->tertiary spacing vs structure at the secondary crossing",
    data_files="A01", countries="HKG;PHL;CHN", years="1970-2024", n="3",
    key_result="HKG gap -4y (with a disclosed substitution), PHL 48y, CHN 44y; no rho reported -> UNABLE", status="derived", evidence_role="DATA BLOCKED",
    note="n=3; the HKG gap depends on substituting a censored crossing. Correctly UNABLE - the spacing question is one of the clearest data gaps in the programme.")
add(artifact="D17", path=B+"cluster_3_geo_size/results/X7_size_ger.csv", domain="lab X7", estimand="System size (log population) vs tertiary/secondary GER",
    data_files=Q+"data/panel_wdi_wide.csv", countries=W30, years="1995-2024", n="30 / 656",
    key_result="TER between -1.74 (CI -5.38..+1.90); within -5.64 (CI -34.14..+22.86) -> NOT SUPPORTED", status="derived", evidence_role="descriptive-only",
    note="Within CI spans 57 log points, so the null is uninformative about size rather than evidence of no relation; the verdict is right but the precision is not.")
add(artifact="D18", path=B+"cluster_3_geo_size/results/X8_citystate_pairwise.csv", domain="lab X8", estimand="HKG vs CHN/PHL/KHM duration and volatility",
    data_files="A01; A04", countries="HKG;CHN;PHL;KHM", years="1970-2024", n="<=4 per side",
    key_result="Only CHN usable: 13.0y vs HKG 19.5y -> ratio 0.667 (HKG slower); volatility ratios 0.50/0.51/0.26 -> NOT SUPPORTED", status="derived", evidence_role="descriptive-only",
    note="n=1 usable pair. The HKG volatility is dominated by a series discontinuity (disclosed). This cell cannot carry a city-state claim either way.")
add(artifact="D19", path=B+"cluster_3_geo_size/results/X9_markets_ger.csv", domain="lab X9", estimand="Declared number-of-markets proxy vs tertiary GER",
    data_files=Q+"data/panel_wdi_wide.csv", countries="6 and 30", years="1995-2024", n="139 / 656",
    key_result="6 systems +0.056 (CI -0.009..+0.121); 30 countries +0.035 (CI +0.0005..+0.070) -> PARTIAL", status="derived", evidence_role="descriptive-only",
    note="The 30-country CI lower bound is +0.0005 - a hair above zero. PARTIAL is generous; treat as a null with a wide positive tail.")
add(artifact="D20", path=B+"cluster_4_regional_proxy/results/X10_convergence.csv", domain="lab X10", estimand="PHL regional convergence in mean years of schooling",
    data_files="10_massification/data/BASELINE_SERIES.csv", countries="PHL 17 regions", years="2 cohorts", n="17",
    key_result="Spearman rho(dMYS, MYS0) = -0.444 (Council re-derived -0.443627); 17/17 regions improved -> SUPPORTED", status="derived", evidence_role="descriptive-only",
    note="Independent re-derivation matches (Council). Proxy limitation: regional tertiary enrolment unobserved; two cohorts only.")
add(artifact="D21", path=B+"cluster_4_regional_proxy/results/X11_gini.csv", domain="lab X11", estimand="PHL regional education-inequality change",
    data_files="10_massification/data/BASELINE_SERIES.csv", countries="PHL 17 regions", years="2 cohorts", n="17",
    key_result="17/17 regions dGini <= -0.02; rho(dGini, Gini0) = -0.622 (Council -0.621524) -> SUPPORTED", status="derived", evidence_role="descriptive-only",
    note="Re-derivation matches. Strongest replicated result in batteries B/C; still proxy-based and descriptive.")
add(artifact="D22", path=B+"cluster_4_regional_proxy/results/X12_gradient.csv", domain="lab X12", estimand="Bottom- vs top-quartile gain in MYS",
    data_files="10_massification/data/BASELINE_SERIES.csv", countries="PHL 17 regions", years="2 cohorts", n="17",
    key_result="Median dMYS ratio Q1/Q4 = 1.098 (1.34 vs 1.22) -> SUPPORTED (mild pro-poor)", status="derived", evidence_role="descriptive-only",
    note="Ratio of medians on 17 regions; no CI, so 'mild' is doing a lot of work. Direction is consistent with X10/X11.")
add(artifact="D23", path=B+"cluster_5_fragmentation_sim/results/AMENDMENT_B1/X13_split_delay_B1.csv", domain="lab X13 (simulated)",
    estimand="Median crossing-year delay from splitting into more markets (toy)",
    data_files="stipulated toy (no observed data)", countries="none (simulated)", years="simulated", n="200 seeds x K grid",
    key_result="Predeclared run undefined (contractive recursion); Amendment B1: median crossing year K=32 - K=1 = +1.00y (CI 0.00..1.00) -> PARTIAL", status="modelled", evidence_role="descriptive-only",
    note="SIMULATED. The predeclared run produced an all-censored artefact because r=0.08<1; that is a Lead predeclaration defect, disclosed. B1 is post hoc. Evidential weight zero (Council D88).")
add(artifact="D24", path=B+"cluster_5_fragmentation_sim/results/AMENDMENT_B1/X14_smoothing_B1.csv", domain="lab X14 (simulated)",
    estimand="Volatility ratio K=1/K=32 in the toy", data_files="stipulated toy", countries="none", years="simulated", n="200 seeds",
    key_result="Predeclared V=1.000 by construction; B1 V=1.231 (CI 1.201..1.251) -> PARTIAL", status="modelled", evidence_role="descriptive-only",
    note="SIMULATED. The predeclared run could not bind a ceiling, so V was mechanically 1.0.")
add(artifact="D25", path=B+"cluster_5_fragmentation_sim/results/AMENDMENT_B1/X15_heterogeneity_dose_B1.csv", domain="lab X15 (simulated)",
    estimand="Spearman rho(crossing year, binding-market dose f)", data_files="stipulated toy", countries="none", years="simulated", n="200 seeds x f grid",
    key_result="Predeclared undefined; B1 rho=1.000 over f=0..0.75 (f=1.0 cell 100% censored) -> PARTIAL", status="modelled", evidence_role="descriptive-only",
    note="SIMULATED. rho=1.000 on 4 finite cells is a mechanical monotone, not an estimate.")
add(artifact="D26", path=L+"lab_2026-11-20_c/Y1_ceiling_residual/results/Y1_correlations.csv", domain="lab Y1", estimand="Income-partial correlations of the tertiary ceiling residual with agri share / youth unemployment",
    data_files="10_massification/data/JOBS_AND_MARKETS_PANEL.csv; A04", countries="6 and 30", years="1995-2024", n="30 (partial) / 6 (raw)",
    key_result="rho(ceiling, agri) = -0.105 after income; rho(ceiling, youth-unemp) = +0.246; raw agri -0.718; 6-system raw check -0.714 -> NOT SUPPORTED (account discarded)", status="derived", evidence_role="descriptive-only",
    note="Discards the opportunity-cost account on a predeclared rule. The 6-system check points the other way and is left as a disclosed tension - correct handling.")
add(artifact="D27", path=L+"lab_2026-11-20_c/Y2_leadlag/results/Y2_PAIR_VERDICTS.csv", domain="lab Y2", estimand="Partial lead-lag between schooling and market indicators, own-lag-1 controlled",
    data_files=Q+"data/panel_wdi_long.csv", countries=W30, years="1970-2024", n="24 cells; up to 700 obs",
    key_result="Max |partial r| = 0.208 (schooling->market, lag 1, n=700, 30 countries); 0/24 cells reach 0.25; reverse direction -0.057..+0.090 -> NOT SUPPORTED", status="derived", evidence_role="descriptive-only",
    note="Zero-order 0.49-0.71 collapses to <=0.21 under an own-lag control: a clean demonstration that the visible schooling-market co-movement is shared trend. Reinforces EQUIVALENT.")
add(artifact="D28", path=L+"lab_2026-11-20_c/Y3_capacity_floor/results/Y3_correlations.csv", domain="lab Y3", estimand="Spearman rho(dPTR improvement, floor) and (., ceiling) across six systems",
    data_files=Q+"data/panel_wdi_long.csv; 10_massification/data/UNIVERSALIZATION_SERIES.csv", countries="5-6 systems", years="1995-2024", n="5 / 6",
    key_result="floor rho=+0.50 (n=5, JPN UNABLE); ceiling rho=+0.60 (n=6) -> NOT SUPPORTED (condition |rho ceiling|<0.50 fails)", status="derived", evidence_role="descriptive-only",
    note="Leave-one-out swings floor 0.0-0.8 and ceiling 0.3-0.9; both conditions hold only when dropping JPN. Correctly reported as not separable - this is the honest weakest link in the A10 'floor not ceiling' ruling.")
add(artifact="D29", path=L+"lab_2026-11-20_c/Y4_worldsociety/results/Y4_AUDIT.csv", domain="lab Y4", estimand="False crossings manufactured by a median-year world-society null",
    data_files="A01; data/gmr_observed_6countries_1970_2024.csv", countries=G6, years="1970-2024", n="30 rows / 5 levels",
    key_result="Upper-secondary null year 2011.5 (n=1 dated crossing, HKG); 4 never-crossed systems falsely crossed, 2 evidence-backed (CHN, PHL); 7 false cells across 4 levels -> DISTINGUISHED", status="derived", evidence_role="descriptive-only",
    note="LABEL MISMATCH: the evidence-backed figures quoted (CHN 79.39, PHL 66.05) are observed GER finals, while the threshold is completion >=90; on completion CHN is 87.52 and PHL 75.03, so the conclusion holds but the cited numbers are the wrong measure. Null rests on one dated crossing.")
add(artifact="D30", path=L+"lab_2026-11-20_c/Y5_portability_audit/results/transfer_checklist.csv", domain="lab Y5 (design audit)", estimand="Presence/absence of the six D75 CHN/HKG transfer inputs",
    data_files="UNIVERSALIZATION_SERIES; JOBS_AND_MARKETS_PANEL; STATE_CAPACITY; POLICY_TIMELINE; UNIVERSALIZATION_TIMING; DATA_NOTES_MASSIFICATION", countries="CHN;HKG", years="1995-2024", n="12 rows (6 inputs x 2 countries)",
    key_result="6/6 inputs present for both countries, 12/12 rows; SCHOOL_EXPANSION.csv is PHL-only; 0 NEW-ASK -> DATA-COMPLETE", status="observed", evidence_role="descriptive-only",
    note="Design-only: data completeness is not a portability result (R20/R22). Also records that CHN per-student spending has 3 observations and CHN education spending 5 - thin inputs behind a 'complete' verdict.")

# ---------------------------------------------------------------- write
os.makedirs(os.path.dirname(OUT), exist_ok=True)
cols = ["artifact", "path", "sha256", "domain", "estimand", "data_files", "countries",
        "years", "n", "key_result", "status", "evidence_role", "note"]
missing = []
for r in rows:
    p = os.path.join(BASE, r["path"])
    if not os.path.exists(p):
        missing.append(r["path"]); r["sha256"] = "FILE-MISSING"
        continue
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    r["sha256"] = h.hexdigest()

with open(OUT, "w", newline="", encoding="utf-8") as fh:
    w = csv.DictWriter(fh, fieldnames=cols)
    w.writeheader()
    for r in rows:
        w.writerow({k: r.get(k, "") for k in cols})

print("rows:", len(rows), "->", OUT)
print("missing paths:", missing)
from collections import Counter
print("status:", Counter(r["status"] for r in rows))
print("role:", Counter(r["evidence_role"] for r in rows))
