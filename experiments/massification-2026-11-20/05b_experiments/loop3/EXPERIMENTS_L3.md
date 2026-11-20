# EXPERIMENTS — Loop 3: stage-matched shadow checks (S1), non-universality (S2), price/entry (S3)

**NEW module:** `loop3/code/shadow3.py` — a declared structural shadow-incidence model (demand by
stage × urban/rural from gate stakes, credential returns, public-school substitute, income and
price/income; supply from commercial firms and teacher-tutors with entry costs, capacity, limited
teacher-tutor reach and a static long-run competitive equilibrium). NOT massabm / floorworld / triad /
a reproduction. Predeclaration: `PRE_DECLARATIONS_L3.md`. All numbers are **stylized model output**;
only observed target cells are compared; no imputed cell is used.

**Intake corrections from loop 2 (Council brief 005).** (1) `02_lit/SHADOW_TARGETS.csv` has **11
`use_as_model_target=YES` rows**, not 6; all 11 are reported below. (2) The loop-2 provider-entry effect
is **54–67 pp** (PH 66.5, HK 53.8, KHM 62.9), not 46–66 pp; the 46–66 figure came from the uncalibrated
loop-2 run and is superseded here (loop-2 files are not edited).

**Status.** completed, 0 failures (3 countries; S1 table 15 literature rows incl. the HKG gradient;
S2 600-draw joint search per country; S3 675-point grid × 3 countries). `SUMMARY_L3.csv`,
`RUN_MANIFEST_L3.json`, `runs/{s1_table.csv,s2_search.csv,s3_grid.csv,findings}`.

## S1 — stage-matched check table (all 11 YES rows + HKG gradient)

Model baseline = declared structural parameters, **not calibrated to these rows** except HK 0.85, which
is reported as a **calibration, never incidence evidence**. Range = literature low–high where given, else
point ±5 pp (declared range rule). “UNABLE” rows are reported, not dropped.

| source | iso | stage | lit % | range | model % | assessment |
|---|---|---|---|---|---|---|
| SHADOW_TARGETS | KOR | all levels (elem+middle+high) | 78.5 | [78.3,78.7] | — | UNABLE: no KOR-like variant |
| SHADOW_TARGETS | KOR | elementary | 90.0 | [88.0,92.0] | — | UNABLE: no KOR-like variant |
| SHADOW_TARGETS | JPN | primary grade 6 (juku) | 41.8 | [22.1,57.9] | — | UNABLE: no JPN-like variant |
| SHADOW_TARGETS | HKG | senior secondary | 85.0 | [80.0,90.0] | 54.4 | **CALIBRATION** (excluded from pass/fail) |
| SHADOW_TARGETS | KHM | lower secondary (grade 9) | 68.4 | ±5 pp | 21.3 | assessed — OUTSIDE (under) |
| SHADOW_TARGETS | KHM | primary | 41.3 | ±5 pp | 12.8 | assessed — OUTSIDE (under) |
| SHADOW_TARGETS | KHM | primary urban | 60.5 | ±5 pp | 19.6 | assessed — OUTSIDE (under) |
| SHADOW_TARGETS | KHM | primary rural | 26.4 | ±5 pp | 10.5 | assessed — OUTSIDE (under) |
| SHADOW_TARGETS | PHL | all basic education | 46.5 | [42.0,49.9] | 23.5 | assessed — OUTSIDE (under) |
| SHADOW_TARGETS | PHL | elementary | 23.8 | ±5 pp | 17.4 | assessed — OUTSIDE (under) |
| SHADOW_TARGETS | PHL | upper secondary (review centres) | 28.1 | ±5 pp | 39.4 | assessed — OUTSIDE (over) |
| TARGETS_SHADOW | HKG | lower secondary 2010 | 72.0 | ±5 pp | 30.6 | assessed — OUTSIDE (under) |
| TARGETS_SHADOW | HKG | middle secondary 2010 | 82.0 | ±5 pp | 40.2 | assessed — OUTSIDE (under) |
| TARGETS_SHADOW | HKG | senior secondary 2010 | 85.0 | ±5 pp | 54.4 | CALIBRATION (excluded) |
| TARGETS_SHADOW | HKG | primary 1996 | 45.0 | n/a | 21.4 | UNABLE: no dated model equivalent |
| TARGETS_SHADOW | HKG | lower sec 1996 | 26.0 | n/a | 30.6 | UNABLE: no dated model equivalent |
| TARGETS_SHADOW | HKG | middle sec 1996 | 34.0 | n/a | 40.2 | UNABLE: no dated model equivalent |
| TARGETS_SHADOW | HKG | senior sec 1996 | 40.0 | n/a | 54.4 | UNABLE: no dated model equivalent |

**S1 verdict: FAIL.** All 3 assessable countries are outside their literature ranges (HKG gradient
lower/middle both missed; KHM under by 20–48 pp; PHL mixed: all-basic/elementary under, upper-secondary
over). Threshold (≥2 countries outside) is met 3/3 ⇒ **stop claiming incidence**. The stage-matched
baseline shows the opposite failure to loop 2: loop 2 over-universalised; a stage-matched structural
baseline under-predicts shadow incidence in HKG/KHM. Neither reproduces the literature. KOR/JPN are
UNABLE (no country variant), so the brief’s “≥2 of 4” cannot be applied literally; reported as 3/3
assessable plus 2 UNABLE.

## S2 — what makes tutoring non-universal? (structural parameters only)

Structural parameters (declared ranges; no take-up rate set directly): gate-stakes scale, public-school
substitute, income scale, provider cost multiplier, teacher-tutor capacity, credential-return scale,
entry scale, capacity scale. Targets: PHL {46.5, 23.8, 28.1}, KHM {68.4, 41.3, 60.5, 26.4}, HKG {72, 82}
(85 excluded). Threshold: all within ±5 pp = reproduces; within ±10 pp = partial; else none works.

| country | baseline RMSE | joint-search RMSE | best joint model | verdict |
|---|---|---|---|---|
| PH-like | 15.2 pp | **11.7 pp** | all-basic 28.8, elementary 25.0, upper 37.9 | **none works** |
| HK-like | 41.6 pp | **0.2 pp** | lower 72.0, middle 81.7 | reproduces (2 targets, 8 free parameters — weak identification) |
| KHM-like | 35.2 pp | **8.3 pp** | lower 62.9, primary 34.1, urban 47.1, rural 29.8 | partial |

**What does the work (one-parameter RMSE reductions):** HKG — gate stakes **+28.2 pp**, public-school
substitute **+23.7 pp**, credential returns **+18.2 pp**, income **+15.3 pp**; KHM — gate stakes
**+10.9 pp**, income **+9.8 pp**, credential returns **+5.0 pp**; PH — all one-parameter effects
≤0.6 pp (PH targets are not jointly reachable inside the declared ranges).

**S2 verdict: PARTIAL overall, NONE WORKS for PHL.** Gate stakes, public-school substitute and
credential returns are the structural parameters that plausibly make tutoring non-universal (defensible
ordering: stakes/returns rise with stage). PHL 46.5 is **not** reachable without moving parameters
outside their independently justified ranges; KHM lower-secondary 68.4 is approached only at the edge
of the stakes/income ranges. So the loop-2 over-universalisation is not fixed by any defensible
structural combination in this module — a valid negative finding.

## S3 — price / provider-entry calibration

675-point grid (entry-cost multipliers × capacity multipliers × teacher-capacity multipliers) per
country. Estimands: price, price/income, provider counts, teacher share, whether the price sits at the
declared floor.

| country | price range | price/income range | points with finite price | points with price/income in [1%,15%] | provider counts | teacher share |
|---|---|---|---|---|---|---|
| PH-like | 0.004–0.500 | 0.004–0.500 | 306/675 | 476/675 | n_cm 0.0–2.3, n_tt 1.6–11.8 | 0.53–1.00 |
| HK-like | 0.009–2.475 | 0.003–0.825 | 395/675 | 416/675 | n_cm 0.0–7.1, n_tt 0.9–20.2 | 0.18–1.00 |
| KHM-like | 0.002–0.144 | 0.004–0.288 | 270/675 | 495/675 | n_cm 0.0, n_tt 1.6–6.8 | 1.00–1.00 |

**S3 verdict: UNABLE TO ASSESS.** The only verified fee moments are Korean (434k won/month per
student; 553k per participant) and there is no KOR model variant and no verified PH/HK/KHM fee moment,
so the observed-range comparison cannot be made — marked UNABLE, never a pass. Structurally, the grid
shows the loop-2 floor collapse was an under-priced entry-cost block: with costs scaled up, prices stay
finite and inside a 1–15% of income band at 416–495 of 675 grid points, with teacher-tutor shares
0.53–1.00. That is a modelling improvement, not an empirical calibration.

## Pending (not run)

- L2-4 recovery with truths outside the candidate set + forced-identification rate: **not run**.
- L2-5 1980–2010 fit / 2011–2024 held-out test on PH & KHM observed completion: **not run**.
No claim is made from either; they are the next round.
