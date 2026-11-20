# EXPERIMENTS — Loop 4 (identification round): U1 KOR fee test, U1b HK OOS, U2 recovery/forced-ID, U3 holdout, U4 verdict

**New code:** `loop4/code/l4.py` — U1/U1b use the loop-3 declared structural shadow market (static
competitive equilibrium with commercial + teacher-tutor supply, capacity, stage demand); U2 is a declared
two-channel identification test; U3 fits the loop-2 two-way module and holds out 2011–2024. NOT massabm /
floorworld / triad / a reproduction. Predeclaration: `PRE_DECLARATIONS_L4.md` (+ Amendment L4-1 with the
lead's improved anchors). All numbers are **stylized model output**; only observed cells are compared; no
imputed cell used. **0 failed runs.**

New anchors used (`04_data/shadow_round2/data/*.csv`): Korea official MODS/KEDI 2023; Hong Kong Bray &
Kwok 2003 (6-school quota sample n=630); Japan grade-6 juku 41.8 (no JPN variant → UNABLE); China 2014
29.8 / post-2021 <20% and Cambodia case-study bounds (not used in these cells); PH blocked. Korea 2011
"90%" is **not used** (not traceable). HK 0.85 (2010) remains a **calibration**, never incidence evidence.

## U1 — KOR-like variant vs official Korean fee moments

One calibration: common demand intercept so all-levels participation = 78.5% (official anchor). Then
checks, not fits.

| item | observed (official 2023) | model | verdict |
|---|---|---|---|
| per-participant annual fee / GDP pc | 13.8% (553k won/month; declared 1,330 KRW/USD, GDP pc 36,238.6 US$) | **13.5%** | inside declared [10.5%,18.5%] band |
| per-student annual fee / GDP pc | 10.8% | **10.6%** | inside declared [9.5%,16%] band |
| participation by level | 86.0 elementary / 75.4 middle / 66.4 high | 71.9 / 78.9 / 88.0 | **ordering FAILS** (official declines with stage; model rises with stakes) |
| by-level spend | 462/596/740k won → 11.5/14.9/18.4% of GDP pc | uniform 13.5% | not reproduced (one price; no stage-specific provider choice) |
| provider mix | hagwon 241k = 55.5% of expenditure (1:1 37k, group 22k, internet 16k) | commercial share 82.9% | over-commercialised |
| hours | 7.3 h/wk (7.5/7.4/6.7 by level) | — | **UNABLE** (no hours object in this module) |

**U1 verdict: price block USABLE for KOR** — the first real fee-moment test passes (13.5% vs the
observed 13.8%, inside the predeclared band). **The demand block is not identified for KOR**: the model
predicts rising participation with stage while the official data fall with stage, it has no hours
object, and one uniform price cannot reproduce the by-level spend gradient. So KOR converts loop-3's fee
`UNABLE` into a pass on provider economics only.

## U1b — HKG multi-moment out-of-sample check

Calibrated ONLY on the 2010 senior-secondary 85% (shift +2.07); 1998/99 rows and provider mix are
checks, not fits. 2010 checks (not fitted): model lower 68.7 vs observed 72, middle 76.2 vs 82.

| stage | observed (Bray & Kwok 1998/99) | model | miss |
|---|---|---|---|
| S1-3 | 35.1 | 51.9 | **+16.8** |
| S4-5 | 46.6 | 58.7 | **+12.1** |
| S6-7 | 70.3 | 68.2 | −2.1 |

Monotone rising: **yes**; Spearman rank correlation with the observed gradient: **1.0**. Provider mix:
model commercial mass-lecture share S6-7 **22.3%** vs S4-5 **100.0%** — the declared rule (teacher-tutor
capacity allocated to the highest-stakes stage first) makes commercial provision *lower* at the top
stage, the **opposite** of the observed pattern (72.4% vs 33.0%). Fee/income: model **5.19%** vs observed
1.1–5.0% — 0.19 pp outside the band.

**U1b verdict: FAIL under the predeclared rule** (levels outside ±15 pp at S1-3/S4-5; provider-mix
ordering reversed; fee just outside). The gradient *shape* is right (monotone, rank correlation 1.0) and
the top-stage level is nearly right (−2.1 pp), but the predeclared rule requires all four conditions.
**The incidence claim therefore stays withdrawn for all countries; no single-country rescue.**

## U2 — recovery with truths outside the candidate set + forced-identification rate

Candidate set: EDUCATION_LED (ed=.8, ec=0), DEMAND_LED (0, .8), COMPLEMENTARY (.6, .6). Outside truths:
COMMON_SHOCK (γ=.9, no mechanisms) and OPPOSITE_SIGN (−.6, −.6). 20 simulations per truth, noise sd 0.30,
threshold |ê|>0.25, difference-in-differences estimator vs placebo arm.

| truth | mean êd | mean êc | recovery | forced-ID (placebo) | forced-ID (no placebo) |
|---|---|---|---|---|---|
| EDUCATION_LED | 0.794 | 0.103 | 0.50 | — | — |
| DEMAND_LED | 0.156 | 0.913 | 0.50 | — | — |
| COMPLEMENTARY | 0.520 | 0.536 | 0.50 | — | — |
| OUTSIDE_COMMON_SHOCK | −0.005 | 0.126 | — | **0.60** | **1.00** |
| OUTSIDE_OPPOSITE_SIGN | −0.622 | −0.664 | — | 0.00 | 0.00 |

**U2 verdict: NEGATIVE — identification NOT established.** Recovery = 0.50 (< 0.67 threshold); forced-ID
= 0.60 (≠ 0 required) under the placebo design; without a placebo the common-shock truth forces a
candidate in 100% of simulations. The predeclared thresholds are not met, so no mechanism
classification is claimed. (The plain 0.25 threshold, as predeclared, was used; the optional 2-sd
significance variant is not applied here.)

## U3 — holdout: fit 1980–2010, test 2011–2024

Model horizon extended to 60 years (t=0 ↔ 1965); one fitted parameter (s0 multiplier), mean over 5
seeds; observed GMR upper-secondary completion only.

| country | fit obs | holdout obs | best s0 mult | in-sample RMSE | held-out MAE | naive persistence MAE | verdict |
|---|---|---|---|---|---|---|---|
| PHL | 6 (1999–2010) | 5 (2013–2024) | 1.06 | 4.54 pp | **14.68 pp** | 5.70 pp | **FAIL — no country claim** (held-out miss exceeds both thresholds) |
| KHM | 7 (1996–2010) | 11 (2011–2023) | 0.40 (grid edge) | 14.80 pp | **1.84 pp** | 6.80 pp | PASS on the predeclared threshold — but in-sample fit is poor and the s0 multiplier sits at the grid edge; a pass on a flat path, **not** a validated country claim |

**U3 verdict: PHL rejected; KHM passes only mechanically** (its flat modelled path happens to sit near
the held-out values while the in-sample fit is bad). Predeclared threshold met for KHM, but the honest
reading is that the model does not reproduce either country's completion dynamics — no country claim.

## U4 — publishable verdict

See `U4_VERDICT.md`. In one line: the publishable object is a **negative/identification map + provider
economics + a data-first program**, not an incidence or massification forecast; U1 gives the only
positive provider finding (KOR fee level 13.5% vs 13.8%), while U1b, U2, U3 and loop-3 S1/S2 all return
negative or UNABLE results under predeclared thresholds.
