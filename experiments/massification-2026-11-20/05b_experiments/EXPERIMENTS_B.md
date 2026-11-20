# EXPERIMENTS — Batch B result records (`experiment-runner-2`)

Independent adversarial batch run in parallel with runner 1's `05_experiments/` suite. Pre-declarations
(including two recorded amendments) are in `PRE_DECLARATIONS_B.md`, written before the relevant runs.
Failures, amendments and interpretation issues are in `ERROR_LOG_B.md`. Per-run commands, raw CSVs,
logs and `findings.txt` are in `runs/<BID>/`. **Every number below is simulated model output**, not an
observed country value. Seed dispersion (sd across replications) is reported separately from any
parameter-uncertainty statement; no parameter-uncertainty sampling was done in Batch B.

**Counts.** completed = 5 experiments (B1, B2, B3, B4, B5); failed runs = 0 of 72 (B1), 0 of 72 (B2/B3),
0 invariant failures out of 60 trajectories (B4), 0 of 800 static screening cells (B5). One
implementation defect was found in code review *before* the affected model ran (B4, degree-share
denominator) and fixed; it never produced a reported number. One method issue: B1's predeclared
plausibility gate was written on an arm mean and passed a numerically unstable cell; a clearly labelled
post-hoc diagnostic (not the declared test) is reported and it downgrades the verdict.

**Headline table:** `SUMMARY_TABLE_B.csv` (188 rows). **Manifest:** `RUN_MANIFEST_B.json`.

**Data note (added at close-out, no result changed).** A UIS/WDI enrolment panel for PHL, KHM, HKG,
CHN, JPN, KOR became available as `04_data/data/gmr_annual_1980_2020_imputed.csv`
(`04_data/IMPUTATION_METHOD.md`; 53.6% observed, 12.5% imputed, rest missing/no anchor, with per-cell
`status`/`method`/confidence/break flags). **No Batch-B result uses it:** B4 and B5 are stylized
possibility models and make no country-level comparison, so no observed or imputed cell from this
panel is cited anywhere in Batch B. The panel is registered in `RUN_MANIFEST_B.json` as the natural
input for a future country-calibrated E12/E16, on the rule that only `status == observed` cells may be
used as observations and imputed cells may be cited only with their method/gap/confidence flags.

**Commands** (all with `PYTHONDONTWRITEBYTECODE=1`, `nice -n 10`, workers=2, per-run timeout 300 s):
```
PYTHONPATH=code/ext_massabm:code  python code/run_B1.py    --out runs/B1        # 72 runs, N=3000
PYTHONPATH=code/stock:code        python code/run_B2B3.py  --out runs/B2_B3     # 72 runs, N=6000
python code/e12_traj.py --out runs/B4                                          # 60 trajectories
python code/e16_readers.py --out runs/B5                                      # 800 static screenings
python code/b1_robust.py                                                       # post-hoc, no model runs
python code/make_manifest_B.py                                                 # table + manifest
```

---

## B1 — Independent replication of the matched-elasticity rival, with a precision + plausibility rule

**ID and question.** Does a competitive CES skill-price world with a formal/informal margin reproduce
a fall in diploma holders' *absolute* income after a college-cost shock, at sigma in {0.5, 1, 2}? If
so, the paper's discriminating claim C3 ("only the surplus/slot account can make diploma holders
lose") is contradicted.

**Status.** completed (72/72 runs ok, wall 97 s at N=3000, reps=6). **Purpose.** adversarial replication
of Council priority #1; the stored E13b pass had been provisional at reps=1 and, by the time of this
batch, runner 1 had upgraded it to reps=6/N=5000.

**Why the comparison is informative.** If a fair competitive rival reproduces the paper's signature
loss, the mechanism is not identified; if only a numerically degenerate corner of the rival does, the
paper's claim survives but must be stated on the employment margin, not on absolute income.

**Model and version.** runner 1's **NEW** extension `mode='hc_fair_slots'` (a copy of massabm with CES
skill prices on the SAME formal vacancy path; see `05_experiments/code/new/README_EXTENSION.md` and
`code/ext_massabm/`). This is not a reproduction of the paper's own rival script. My driver
(`code/run_B1.py`) and outcome extraction are new. Comparator: stored
`05_experiments/runs/E13b` (reps=6, N=5000, wall 282 s).

**Initial conditions and timeline.** massabm `t0=1920, t1=2035`, no K-12 reform (`reform_rule='never'`),
tuition paths from the stock `SHOCKS`, cohorts entering 1995–2012, labour market window 2010–2030.

**Arms and shared controls.** Surplus world `mode='full'` (credential floors + ranked hiring) vs matched
rival `mode='hc_fair_slots'` at `fair_sigma ∈ {0.5, 1.0, 2.0}`; shocks: no shock / college half price
from 1995 / college 80% off from 1995. Identical households, per-spec identical tuition paths, the SAME
formal vacancy path (`macro_elasticity=0` in both worlds), matched seeds 20000+r (r=0..5), N=3000.

**Outputs.** Paired change vs no-shock in (a) diploma holders' absolute basic income, (b) diploma
holders' formal-employment probability, (c) diploma/degree income ratio; plus the rival's baseline
diploma/degree ratio used as the plausibility gate.

**Sampling.** 6 paired replications per cell; sd across replications. No parameter draws.

**Verification.** 0 failed runs; the sign pattern of the stored E13b reproduces (see below).

**Result.**

| world | sigma | shock | Δ diploma income | Δ formal\|dip | Δ ratio | baseline dip/deg ratio |
|---|---|---|---|---|---|---|
| surplus (slots+floors+rank) | — | half price | −0.0552 (0.0171) | −0.1430 (0.0186) | +0.0492 | 0.537 |
| surplus (slots+floors+rank) | — | 80% off | −0.0292 (0.0163) | −0.1543 (0.0175) | +0.0788 | 0.537 |
| competitive CES + slots | 0.5 | half price | −0.1094 (0.0297) | +0.0238 (0.0307) | −0.0680 | 0.234 mean (per-seed 0.022–1.212) |
| competitive CES + slots | 0.5 | 80% off | −0.1753 (0.0444) | +0.0513 (0.0122) | −0.0610 | 0.234 mean (per-seed 0.022–1.212) |
| competitive CES + slots | 1.0 | half price | −0.0099 (0.0180) | +0.0199 (0.0180) | −0.1067 | 0.340 |
| competitive CES + slots | 1.0 | 80% off | −0.0154 (0.0308) | +0.0240 (0.0190) | −0.1583 | 0.340 |
| competitive CES + slots | 2.0 | half price | **+0.0420** (0.0036) | −0.0068 (0.0033) | +0.0799 | 0.541 |
| competitive CES + slots | 2.0 | 80% off | **+0.0696** (0.0050) | −0.0150 (0.0050) | +0.1405 | 0.541 |

**Verdict — literal predeclared rule vs robust reading.** The predeclared three-condition rule fires
**only at sigma=0.5** (both shocks negative, |Δ| > 2·sd, mean baseline ratio ≥ 0.20). At sigma=1 the
negative is inside seed noise; at sigma=2 the rival produces clear **gains** and its baseline ratio
(0.541) matches the surplus world (0.537). A **post-hoc** diagnostic (labelled as such, not the
declared test) shows why the sigma=0.5 firing is not a fair-rival result: across the same 6 seeds the
rival's baseline ratio ranges **0.022 to 1.212** (5/6 below the plausibility gate) and its degree
income ranges **1.01 to 42.39** — an unstable CES corner, not a calibrated rival. So the honest verdict
is: **the contradiction does NOT survive as a fair-rival result.** What does survive is the
employment-margin difference: the surplus world loses **14–15 pp** of diploma holders' formal-employment
probability, while a stable competitive rival changes it by at most **+2 pp / −1.5 pp**. C3 is defensible
as a claim about *who gets the formal jobs*, not about absolute income.

**Assumptions / sources.** Rival mechanism and its mapping are declared in
`05_experiments/code/new/README_EXTENSION.md`; vacuum paths and wage rules are the stock model defaults.
N=3000 (not 5000) is a declared trade-off for the shared laptop; the stored N=5000 comparator is
reported alongside. I had seen the stored E13b output before predeclaring, so B1 is a replication, not
a blind test.

**Interpretation.** The discriminating claim should be restated: "a competitive world with a
formal/informal margin does not reproduce the formal-job displacement; it can, in some CES corners,
reproduce an absolute-income fall, and those corners are numerically fragile." Do not report a
rival contradiction as evidence against C3 without the degeneracy diagnostic.

**Evidence to collect next.** A stable rival calibration at the empirically plausible substitution
range (the sigma=2 cell) with a documented CES initialization; a formal convergence check across N and
seeds for sigma<1 before that corner is used in any claim.

**Reproduce.** `runs/B1/{b1_raw.csv, b1_summary.csv, b1_robustness.csv, findings.txt, run_meta.json}`;
`logs/B1.log`.

---

## B2 — Six-arm floor/race table at 4 reps, N=6000 (independent rerun; closes the reps gap)

**ID and question.** Do the stored October/manuscript 6-arm cells reproduce at the manuscript's 4 reps,
and what is the **unranked-lottery** intensification slope at 4 reps?

**Status.** completed (72/72 runs ok, wall 294 s under heavy load). **Purpose.** precision replication
of the race-and-floor design (menu E8); the stored number came from a 2-rep pilot.

**Model and version.** UNMODIFIED stock massabm copied from `01_sources/.../massabm` into
`code/stock/massabm` (sha256 in manifest), driven by `code/run_B2B3.py`; independent outcome
implementation. Comparator: `05_experiments/runs/E8` (reps=4, N=6000, wall 332 s).

**Initial conditions and timeline.** `reform_rule='never'`, `t1=2035`; cohorts entering 1995–2012;
labour market 2010–2030; formal-demand scales {0, 1, 2}; matched seeds 19000+r, r=0..3; N=6000.

**Arms and shared controls.** 2×3: ranking {on, off} × eligibility rule {none, adaptive employer floor,
fixed rule-set floor (elite=4, mid=4, routine=3)}. Identical cohorts, schedules, seeds and wage rules
across arms; utility/cost specification untouched.

**Outputs.** Basic-diploma completion (all, Q1); formal-employment rate below vs at the diploma; Q3–Q5
college entry; slope of Q3–Q5 college entry on degree holders' absolute income across demand scales —
reported **both** the stored pooled-across-reps OLS and the new per-rep slope mean ± sd.

**Result** (baseline demand means, sd across reps; slope pooled / per-rep mean (sd)):

| arm | diploma | diploma Q1 | formal\|<dip | formal\|dip | college Q3-5 | slope pooled | slope per-rep |
|---|---|---|---|---|---|---|---|
| ranked, no floor | 0.771 (0.001) | 0.571 (0.004) | 0.122 | 0.351 | 0.493 (0.002) | −0.039 | −0.039 (0.009) |
| ranked, adaptive employer floor | 0.770 (0.000) | 0.569 (0.002) | 0.119 | 0.225 | 0.542 (0.010) | −0.064 | −0.063 (0.006) |
| ranked, fixed rule-set floor | 0.772 (0.001) | 0.572 (0.003) | 0.117 | 0.354 | 0.492 (0.002) | −0.049 | −0.049 (0.017) |
| unranked, no floor (lottery) | 0.731 (0.003) | 0.538 (0.003) | 0.436 | 0.450 | 0.180 (0.013) | **+0.151** | **+0.198 (0.042)** |
| unranked, adaptive employer floor | 0.771 (0.001) | 0.570 (0.003) | 0.118 | 0.207 | 0.614 (0.002) | +0.036 | +0.037 (0.022) |
| unranked, fixed rule-set floor | 0.771 (0.001) | 0.571 (0.002) | 0.118 | 0.495 | 0.478 (0.008) | +0.630 | +0.800 (0.288) |

**Verdict.** The pooled slopes reproduce the stored E8 values exactly (−0.039 / −0.064 / −0.049 /
+0.151 / +0.036 / +0.630), so the 4-rep cell is independently confirmed. The unranked-lottery
intensification slope at 4 reps is **+0.151 pooled** (identical to the stored +0.151) and **+0.198
per-rep (sd 0.042; 2sd bar 0.084)** — positive and distinguishable from zero. **Rank-dependence of
intensification is confirmed at 4 reps** under the predeclared rule (all ranked arms negative;
lottery positive beyond 2sd). The 2-rep pilot's +0.221 is fully consistent with the 4-rep per-rep
estimate (+0.198 ± 0.042); the pooled number is attenuated by pooling scales and reps, which is why the
per-rep estimate is preferred for dispersion.

**Assumptions / sources.** The October stored numbers' provenance is unknown; this is a design
reproduction and direction/precision check, not a provenance claim. N=6000 used as specified.

**Interpretation.** The floor/race table is stable at the manuscript's replication count. The
unranked-lottery sign is not a small-sample accident.

**Reproduce.** `runs/B2_B3/{b2b3_raw.csv, b2_summary.csv, findings.txt, run_meta.json}`;
`logs/B2_B3.log`.

---

## B3 — Allocation-rule knock-out: rank vs employer cutoff vs random-among-eligible

**ID and question.** Is intensification (investing more as degrees pay less) a property of **ranking**,
or does it also appear under a non-rank allocation — i.e. is the race mechanism allocation-specific or
mechanism-general? (Council priority #3.)

**Status.** completed as a predeclared subset analysis of B2's run set (72 runs shared; no extra runs).

**Estimand and design.** Same per-rep slope as B2, comparing four allocation rules with the household
utility/cost specification, cohorts, seeds and demand scales held fixed (2×2: ranking {on, off} ×
employer cutoff {on, off}):
`rank+cutoff = mode 'full'`; `rank only = 'no_floor'`; `cutoff + random among eligible = 'no_rank'`;
`random among all = 'lottery'`. This separates the cutoff (eligibility) from the rank race.

**Result.**

| allocation | slope pooled | slope per-rep (sd) | 2sd bar | degree-income span across scales |
|---|---|---|---|---|
| rank + employer cutoff | −0.064 | −0.063 (0.006) | 0.012 | 0.534 |
| rank only, no cutoff | −0.039 | −0.039 (0.009) | 0.018 | 0.599 |
| cutoff + random among eligible | +0.036 | +0.037 (0.022) | 0.045 | 0.401 |
| random among all (lottery) | +0.151 | +0.198 (0.042) | 0.084 | 0.216 |

**Verdict (predeclared threshold not fully met; report honestly).** All three ranked arms are negative
and both statistically clean non-rank arms are positive — the **sign flips under non-rank allocation**.
But the predeclared bar was "slope > 0 beyond 2·sd in **≥2** non-rank arms", and only the
random-among-all arm clears it; the **cutoff + random-among-eligible** arm is positive (+0.037) but
inside its 2sd bar (0.045). So: *"intensification requires ranking" is allocation-conditional in
direction, but only partially identified at 4 reps.* An employer eligibility cutoff **alone** does not
produce intensification (slope ≈ 0), which is the paper-relevant refinement: the cutoff is not the
race. The weak cell is specifically the cutoff-without-rank arm, and it needs more replications or a
within-cell design that isolates what the cutoff does to college demand.

**Assumptions / sources.** Shared with B2; the degree-income span check confirms the slope is
identified within each arm (no arm had span < 0.1). These are simulated model modes, not a
description of real employer allocation.

**Interpretation.** Do not present the race mechanism as general to all credential allocation; a
pure eligibility cutoff behaves like human-capital allocation (small positive slope), and the
intensification sign is attached to the rank race.

**Evidence to collect next.** Power the cutoff-without-rank arm (more reps, or a paired within-arm
cutoff sweep) to decide whether its positive slope is a true zero or a weak intensification.

**Reproduce.** `runs/B2_B3/{b3_knockout.csv, b2b3_raw.csv, findings.txt}`.

---

## B4 — E12 long-run massification trajectories, 10/20/30/40 years (NEW implementation)

**ID and question.** Starting from a plausible stylized world, do 40-year cohort/workforce trajectories
of entry, progression, completion, wages and employment mix **require a supplied (exogenous) education
trend**, or can an endogenous household decision path generate the rise?

**Status.** completed (60/60 trajectories, 0 invariant failures, deterministic accounting + declared
stochastic draws). **This is a NEW implementation** (`code/e12_traj.py`), not massabm, not triad, not
floorworld, and not a reproduction of the paper's E12. E12 was recorded as "not run" in
`05_experiments/PRE_DECLARATIONS.md` (covered only descriptively by E19); B4 supplies a first
model-based cell.

**Why the comparison is informative.** An "endogenous" massification claim is only meaningful if the
decision mechanism generates the rising curve without the analyst supplying it; otherwise the matching
is done by the input schedule.

**Model.** 40-year annual cohort-flow model, N=1000 births/year, 40-year burn-in to start from a
stationary workforce; declared inputs: secondary completion 0.65, college completion 0.85, formal
vacancies 0.12 birth-cohorts/year growing 2%/yr, births flat or 1%/yr, turnover horizon 40 or 20 years,
lognormal household college cost (median calibrated ONCE so the stylized t=0 entry share is 0.22 — a
calibration to an initial level, not to any trajectory), formal wages (1.70 diploma, 2.40×premium
degree, informal 1.00/1.15), discount 0.97. **Generated** quantities: degree share, degree premium
(congestion rule `(s_ref/s)^0.4`), hiring mix, wages, beliefs (lag-1 formal placement).

**Arms and controls.** (A) **EXO**: college-entry rate follows a supplied schedule 0.22→0.55
(input-driven by construction). (B) **ENDO**: entry = share of households whose drawn cost is below the
expected private return gap, with the return using the current premium and lag-1 placement beliefs —
generated. Same births/vacancy/completion inputs and 5 matched seeds in both arms. Variants: turnover
40 vs 20; births flat vs 1%/yr.

**Result (turnover 40, flat births; mean across 5 seeds, sd in the CSV).**

| mode | year | college entry | degree share | graduate formal prob | formal share | degree premium |
|---|---|---|---|---|---|---|
| EXO (input-driven) | 10 | 0.302 | 0.199 | 0.982 | 0.198 | 0.955 |
| EXO (input-driven) | 20 | 0.385 | 0.223 | 0.919 | 0.218 | 0.916 |
| EXO (input-driven) | 30 | 0.468 | 0.267 | 0.906 | 0.255 | 0.854 |
| EXO (input-driven) | 40 | 0.550 | 0.332 | 0.926 | 0.312 | 0.783 |
| ENDO (generated) | 10 | 0.020 | 0.140 (0.023) | 1.000 | 0.175 | 0.942 |
| ENDO (generated) | 20 | 0.212 (0.384) | 0.086 (0.007) | 0.866 (0.268) | 0.198 | 1.152 (0.110) |
| ENDO (generated) | 30 | 0.020 | 0.145 (0.024) | 0.880 (0.239) | 0.220 | 0.943 |
| ENDO (generated) | 40 | 0.020 | 0.157 (0.027) | 1.000 | 0.263 | 0.903 |
| ENDO_SMOOTH (POST-HOC) | 40 | 0.108 | 0.144 (0.026) | 1.000 | 0.294 | 0.880 |

**Verdict — requires a supplied trend.** The predeclared rule returns **"requires supplied trend"**:
EXO entry rises +0.330 over 40 years, while ENDO entry does not rise — it collapses toward its floor
(0.404 → 0.020) in a cobweb: a high-entry cohort lowers graduates' formal placement probability, which
collapses the next cohorts' expected return and hence entry, which restores the premium. The
post-hoc smoothing arm (partial adjustment 0.5/yr, added after the primary run and labelled post-hoc)
still does not rise (0.218 → 0.108). The 1%/yr-births and 20-year-turnover variants agree in sign. So
in this stylized world the endogenous decision path does not trace the massification curve; EXO
outcomes are **input-driven by construction** and cannot be counted as generated. The **degree share
and premium are generated** in both arms; births, vacancy growth, completion rates and turnover are
declared scenario inputs in both.

**Assumptions / sources / caveats.** Stylized possibility model, not a forecast for the Philippines,
Cambodia, HK or China. Each arm runs its own 40-year burn-in, so arms start from different states:
compare **trajectory direction**, not levels. The ENDO arm is genuinely unstable (seed sd up to 0.38 at
year 20: some seeds reset to the floor, others spike), which is itself evidence that a threshold
decision rule without a cost/demand trend does not settle on a rising path; we do not claim it
identifies a stable trajectory. No non-convergence concept applies (deterministic accounting +
explicit draws); invariant checks (workforce non-negative, stocks ≤ workforce, probabilities in [0,1])
passed 60/60.

**Interpretation.** Matching a rising massification curve in this class of model requires a supplied
education schedule **or** a supplied cost/demand trend (e.g. falling relative cost or skill-biased
formal demand); an endogenous return-driven rule alone reproduces neither the level nor the slope.
This is the menu's "input-driven versus generated" warning made concrete.

**Evidence to collect next.** A common-burn-in version and a cost-decline (free-tuition-style) arm,
to separate "endogenous decisions cannot massify" from "endogenous decisions cannot massify *without
a cost trend*".

**Reproduce.** `runs/B4/{e12_trajectories.csv, e12_checkpoints.csv, findings.txt, run_meta.json}`;
`logs/B4.log`.

---

## B5 — E16 credential readers: information, recognition and exclusion (NEW implementation)

**ID and question.** How do credential readers trade off hiring errors, exclusion, wages and
certification demand — domestic detailed reader vs coarse reader vs skill test vs formal eligibility
rule — and how do signal accuracy, screening cost, network access and cross-border recognition move
those trade-offs independently? (Menu E16, which was not run in `05_experiments/`.)

**Status.** completed (800/800 screening cells). **This is a NEW implementation**
(`code/e16_readers.py`), not massabm/triad/floorworld and not the paper's E16.

**Model.** One-period static screening model, N=2000 applicants, M=300 formal vacancies; latent
ability and SES standard normal; credential tier 0–3 with mild ability/SES selection; **true
productivity = ability + 0.25 × (2 × tier)**, so schooling is productive and no arm is optimal by
construction. Formal wage 2.2, informal 1.0. Readers: detailed domestic (ability + 0.2×years),
coarse (years only), skill test (ability only), eligibility rule (tier ≥ 2 then random), foreign reader
(recognition rate ρ on origin credential years + 0.5×ability). Factors varied independently:
accuracy (noise 0.3 / 0.8), applicant screening cost (0 / 0.5, paid only if affordable from
exp(0.5·SES)), SES-linked referral share (0 / 0.3), recognition ρ (1.0 / 0.3). Matched seeds 0–9.

**Result at the declared baseline** (accuracy high, cost 0, no network, ρ=1; mean, sd across 10 seeds):

| reader | coverage of true top-M | productivity error/hire | top-tertile exclusion | SES hire gap | certification demand |
|---|---|---|---|---|---|
| detailed domestic | 0.851 (0.016) | 0.045 | 0.550 | +0.105 | 0.062 |
| coarse domestic | 0.565 (0.022) | 0.411 | 0.620 | +0.269 | 0.217 |
| skill test | 0.696 (0.018) | 0.179 | 0.568 | +0.007 | 0.000 |
| eligibility rule | 0.397 (0.021) | 0.724 | 0.677 | +0.206 | 0.169 |
| foreign reader | 0.662 (0.027) | 0.259 | 0.592 | +0.250 | 0.194 |

**Verdicts.** (i) The predeclared calling-card claim was "detailed domestic reader has lower hiring
error than the coarse reader but induces **higher** certification demand" — the first half is
supported (error −0.365, 2sd 0.076, 10/10 seeds) but the second half is **contradicted**: the detailed
reader also has **lower** certification demand (−0.155, 2sd 0.030, 10/10). In this model richer
information lowers the private return to buying a credential because the coarse reader makes the
credential do all the sorting. (ii) the skill test beats the detailed reader on nothing here and loses
error (+0.133, 2sd 0.027): discarding schooling information costs more than within-tier noise; it has
zero certification demand by construction (declared limitation, not a finding). (iii) Screening costs
and SES-linked referrals convert reader quality into SES exclusion — the network-0.3 cell raises the
SES hire gap from +0.105 to +0.186 and cuts coverage from 0.851 to 0.729. (iv) **Foreign recognition:
counterintuitively, lowering ρ from 1.0 to 0.3 *improves* coverage (+0.105) and lowers error (−0.137)**
in this model, because the foreign reader at ρ=1 over-weights a credential whose true productivity
return is smaller than its signalling weight. This is a property of the declared parameters
(credential over-weighting), **not evidence about real migrant-recognition regimes** — a foreign reader
that is well informed needs no correction; the sign is a warning against assuming recognition always
helps matching.

**Assumptions / caveats.** Stylized static model; no learning, no general equilibrium, no country
calibration; productivity weights are declared, not estimated. The eligibility-rule and skill-test arms
are mechanism limits, not policy proposals.

**Reproduce.** `runs/B5/{b5_raw.csv, b5_summary.csv, findings.txt, run_meta.json}`; `logs/B5.log`.

---

## Not run in Batch B (recorded as proposed, never claimed)

- No new parameter-uncertainty sampling (Sobol/LHS), no country calibration, no causal claim.
- No floorworld / childworld / atlas cell is claimed.
- B5 is complete for E16's reader comparison; E16's "corruption" channel and a genuinely well-informed
  foreign reader (the menu's explicit control) were not run.
