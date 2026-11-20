# MUST_REPRODUCE — the ranked target list for a synthetic-data generator

**Companion to** [`STYLIZED_FACTS.md`](STYLIZED_FACTS.md) / [`STYLIZED_FACTS.csv`](STYLIZED_FACTS.csv). Fact ids refer to
that register. Paths are relative to `experiments/massification-2026-11-20`.
**Ranking rule:** (i) the fact must be checkable from disk; (ii) it must be one a generator can *fail*; (iii) it must be
load-bearing for the programme's own claim (anchor asymmetry, scaling, timing, or a hard negative). Facts that are
descriptive-only, n≤6, or disputed are demoted or excluded — see §2.

---

## 1. Reproduce these first, in this order

### R1 — The PHL asymmetry (the anchor). Facts PHL-01, PHL-02, PHL-03, PHL-06. Label VERIFIED.
**Check.** Over 1999–2024, the generated PHL series must satisfy, simultaneously:
- primary completion first reaches ≥90 in **2017** and is ≥98.0 by 2024 (observed 91.918 / 98.305);
- lower-secondary completion first reaches ≥90 in **2024** (observed 92.414; 2023 = 88.442);
- upper-secondary completion **never** reaches 90 in any year ≤2024, peaks in **[75.0, 77.0]**, and is 75.03 ± 1.5 in
  2024;
- the floor-to-middle crossing gap is **[5, 9] years**;
- the ceiling residual at 2024 is **[13, 17] pp**.

**Pass rule:** all five hold in the same run with **no level-specific free parameters**. A generator that hits the three
levels independently has not reproduced this fact; the content is that the ceiling does not respond to what moved the
floor. This is the only fact that, alone, would justify calling the generator a model of massification.

### R2 — Participation ≠ completion in the same system. Fact PHL-05. Label VERIFIED.
**Check.** If the generator emits GER as well as completion: PHL primary GER ≥95 in **every** year 1971–2017, <95 in
2018–2024 (min 88.83 in 2021, 94.03 in 2024), and primary NER ≈ 96.79 (±2) in 1976.
**Pass rule:** the participation series and the completion series must be able to diverge by ≥8 pp in both directions over
the window. If GER is a monotone transform of completion, this check fails and every "universalisation date" the
generator reports is ambiguous.

### R3 — The completion trajectory shape, not just the crossing year. Facts PHL-01, PHL-02.
**Check.** Generated PHL completion in 1999 / 2013 / 2017 / 2024 within **±2 pp** of observed:
primary 83.16 / 87.45 / 91.92 / 98.30; lower-secondary 58.86 / 71.27 / 81.25 / 92.41.
**Pass rule:** RMSE ≤ 2 pp over the 11 observed points at each level. This is a *shape* check: it stops a generator from
landing the right crossing year with the wrong curvature (a logistic that saturates at 100 in 2010 fails).

### R4 — Tertiary: a 35-point rise with a mid-course dip. Fact PHL-04. Label VERIFIED.
**Check.** Generated PHL tertiary GER = 16.3 ± 2 in 1971, 47.4 ± 3 in 2024, 51.1 ± 3 in 2025; the 2016→2018 fall from
38.3 to 28.1 (**−10.2 pp**) must be present as a fall, and the 2018→2026 recovery must reach ≥50 by 2025.
**Pass rule:** the dip exists in the generated series **without** a tuition-elasticity parameter (the K-12 cohort delay is
a sufficient candidate explanation and is a declared open test, not an established cause — do not claim a cause, just
reproduce the shape). If the generator needs a free "policy shock" dummy to produce the dip, record that as a parameter
and disclose it.

### R5 — Positive income scaling, with the right within/between structure. Facts SCA-01, SCA-02, SCA-03. Label VERIFIED.
**Check.** Re-estimate the generator's own output on the same 30-country panel and the same two FE structures:
- secondary GER ~ GDPpc: within **0.09 ± 0.04**, between **0.215 ± 0.03**, between > within;
- tertiary GER ~ GDPpc: within **0.85 ± 0.10**, between **0.57 ± 0.05**, within > between;
- lower-secondary completion ~ GDPpc: within **0.247 ± 0.06**, between **0.169 ± 0.03**.
**Pass rule:** all six coefficients positive **and** each interval containing the disk value, **with no exponent supplied
as a parameter**. The gap *sign* must differ between the secondary and tertiary laws — a generator with one within/between
rule fails on one of the two.

### R6 — The six-system gradient must collapse at 30 countries. Facts INC-01, INC-02, INC-03. Label VERIFIED.
**Check.** Within slope of upper-secondary GER on log GDP = **+56 ± 25 pp/log point on the six systems (n≈93, 5 clusters)**
and **+15 ± 10 on 30 countries (CI must include 0)**. Observed +56.066 and +14.740 (CI −1.559…+31.038).
**Pass rule:** both, from the same generator, in one run. If a generator matches +56 everywhere it is wrong; if it matches
+15 everywhere it is also wrong (it then cannot produce the steep six-system segment).

### R7 — Two income → education predictive associations with opposite signs, and a null the other way. Facts PP-01, PP-02, PP-03, PP-04. Label VERIFIED.
**Check.** On the 30-country panel with the file's own specification (own lags 1–5 + driver lags, two-way FE, CR1):
- income growth → **tertiary** GER: F in **[4, 9]**, coefficient sum **+0.21 ± 0.10** (observed F=6.522, sum +0.2051);
- income growth → **secondary completion**: F ≥ 2.8, coefficient sum **−0.67 ± 0.25** (observed F=3.514, −0.6674);
- wage-share growth → secondary GER: F in **[2.5, 6]**, sum positive (observed 4.108, +0.0504);
- **education → income growth: null in all three** (F < 2.0 in each; observed 0.943 / 0.648 / 1.516).
**Pass rule:** the one-way pattern (significant one direction, null the other) in all four. A symmetric lead-lag is a
**falsifier**, not a partial pass. Carry no direction/causation claim (PP-05, R13).

### R8 — Regional equalization across 17 regions. Facts REG-01…REG-05. Label VERIFIED.
**Check.** Generate 17 regions × 2 cohorts of `mean_years_of_schooling` and `education_gini` with:
ΔMYS > 0 in **17/17**; ΔGini ≤ −0.02 in **17/17**; ρ(ΔMYS, MYS₀) = **−0.44 ± 0.10**; ρ(ΔGini, Gini₀) = **−0.62 ± 0.12**;
Q1/Q4 median-ΔMYS ratio in **[1.05, 1.15]**; smallest ΔMYS in the richest region.
**Pass rule:** all six. This is the cleanest observed result in the programme and the only place where a *within-country*
design is available at n=17. Regional **tertiary** participation must be labelled GENERATED — nothing observed exists to
check it against (REG-06).

### R9 — Crossings as censored intervals, not dates. Facts TIM-01, TIM-02, TIM-03. Label VERIFIED.
**Check.** Generated crossing output must be an interval or an inequality, and must match:
JPN primary ≥95 reported as **≤1971**; KOR primary ≥95 as **≤1971**, KOR lower-secondary completion ≥90 as **≤2003**,
KOR upper-secondary completion ≥90 as **≤2000**; HKG primary NER ≥90 at **1974**, ≥95 at **1979**; HKG upper-secondary
NER ≥90 **never**; PHL primary 2017–2021, lower-secondary 2023–2024, tertiary 2024–2025, upper-secondary never.
**Pass rule:** every one reported with its measure named and its censoring flagged. A point date for JPN or KOR is an
automatic fail — the data do not contain one.

### R10 — The visible co-movement **and** the null partials. Fact NEG-01. Label VERIFIED.
**Check.** Zero-order schooling↔market correlations in **[0.49, 0.71]**, while the country-demeaned cross-lag **partial**
correlations (controlling the dependent's own lag-1, lags 1–3, both directions) satisfy **max |partial r| < 0.25** in all
24 cells.
**Pass rule:** both. This is the cheapest available over-fitting test: a generator that produces a strong partial
lead-lag has reproduced the shared trend as a mechanism.

### R11 — Positive capacity facts, with the ceiling flat. Facts CAP-03, CAP-04. Label VERIFIED.
**Check.** Generated PHL primary PTR falls **35.07 (2005) → 29.08 (2017)**; education spending rises **2.33 → 3.96 %GDP**;
upper-secondary completion is **76.43 (2017) → 75.03 (2024)** — i.e. capacity improves while the ceiling does not move.
**Pass rule:** the three together. Capacity may be a floor precondition; it must **not** be a ceiling driver. If the
generator's capacity channel lifts the ceiling, this check fails and the anchor asymmetry (R1) is being produced by the
wrong mechanism.

### R12 — Bounded enrolment rates and gate-determined saturation. Facts MOD-01 (inverse), TOY-03 (design). Labels MODEL-OUTPUT-NOT-FACT / SIMULATED.
**Check.** Generated GER ∈ **[0, 105]** at every level and year with **no per-country scale factor** (the old class produced
332.8–3514.4%: `model/smoke/structure_smoke.csv`, 1458/1458 rows >100). Then, as a design check: doubling **ceiling**
capacity must move ceiling completions by **<15 pp**, while doubling **floor** capacity moves floor completions by
**>30 pp** (toy magnitudes: +4.58 vs +44.43).
**Pass rule:** the bound is a hard gate (this is Z1); the saturation asymmetry is a design constraint, and its *numbers*
must not be reported as evidence.

---

## 2. Do **not** try to reproduce these — contaminated, disputed, or non-facts

### X1 — "Capacity does not predict crossing timing (+0.15 / +0.10 / +0.41 / +0.30, all ns, n=5)". Fact CAP-01. REPORT-ONLY-UNRELIABLE.
**Those four numbers are in no file.** The file (`relations/data/capacity_crosscountry.csv`) says **+0.872 (p=.054) /
+0.900 (p=.037) / +0.103 (p=.870) / +0.800 (p=.104)** — the opposite sign of association — and even that is a
one-country artefact (JPN enters at `capacity_within` 20.0 vs 46.5–61.1). **Target instead:** "not identifiable at n=5"
(no capacity→timing claim, in either direction). Audit FLAG-02; narrative withdrawn in `SYNTHESIS_018`.

### X2 — PHL "+35.2 points of capacity into the primary crossing". Fact CAP-02. REPORT-ONLY-UNRELIABLE.
The row exists in `capacity_alignment.csv` (49.5→84.7 at `crossing_year_used=2019`) but does not reproduce:
**+26.15** at 2019 and **+14.43** at 2017 from `state_capacity.csv`, and `capacity_within` in 2017 (57.38) is *below* its
2005 value (58.89). **Target instead:** R11's descriptive triple (PTR down, spending up, ceiling flat).

### X3 — "The" crossing vector, and the single-measure milestone dates. Facts TIM-04, TIM-05. DISPUTED.
Two identically-named timing files disagree on PHL primary (2017 vs 1971/1976), PHL lower-secondary (2024 vs 2014) and
CHN lower-secondary (2014–16 vs 2006), because they use different measures *and* different crossing definitions. The
corrected vector was ordered (`SYNTHESIS_018` Z2) and **has not landed**. **Target instead:** R9's measure-qualified
milestones, each with its measure named.

### X4 — The scaling target pair 0.286 / 0.776 **as a single criterion**. Fact SCA-06. DISPUTED.
The gate requires secondary **+0.286** while its own containment range is **[0.0904, 0.2154]**
(`model/calib/repair_scaling.csv`: `A1_value=0.286`, `A3_hi=0.2154`, `contained=False`), and 0.286 is itself one of the
two estimators that define the target. **Target instead:** R5, which states both on-disk pairs and requires the
generator to be scored against a *declared choice of one*. Do not build a pass/fail on the unwinnable pair.

### X5 — The old model's milestone table and its "1960 tertiary crossing". Fact MOD-02. MODEL-OUTPUT-NOT-FACT.
M4 (tertiary ≥50) "crossed in **1960**" in all 12 arms *including the no-push arm* — an artefact of the 3–35× GER
mis-scaling, not a timing result. M2 has **0/12** clean hits against the observed 2024, and no fitted θ was persisted for
any arm (D-03), so the table cannot be re-scored without a re-fit barred by R27/R12. **Target instead:** R12's bound, and
the observed milestones (R1, R9).

---

## 3. What would count as success

A synthetic generator succeeds when **a reader who did not build it can rerun the checks in §1 from its output files and
get PASS on R1–R12 without being told what the generator was trying to do** — and when the honest failures are printed
alongside the passes rather than tuned away.

Concretely, success is:

1. **R1 and R2 together** — the asymmetry (floor and middle cross, ceiling does not) reproduced *with* participation and
   completion as separately generated quantities. This is the one thing the programme could not do, and the reason the
   phase closed at PARTIAL.
2. **R5 and R6 together** — correct-sign income scaling with the right within/between gap structure, *and* the honest
   30-country collapse. A generator that passes R5 by imposing the exponents as parameters has failed the test's
   purpose; the exponents must be generated, not supplied.
3. **R7 and R10 together** — the one-way predictive pattern and the null partials, i.e. the model reproduces both what
   the data show and what they do not. A generator that finds a strong schooling↔market lead-lag has over-fitted the
   shared trend and should be rejected even though it "fits better".
4. **R9 and R11 together** — censoring reported as censoring, and capacity improving while the ceiling stays flat.
5. **Every number labelled**, with the three non-facts (§2, X1–X3) absent from the output rather than reproduced, and the
   five disputed/model rows either excluded or printed with their dispute.

**And success explicitly does not include** any of: a direction-of-causation claim (R13; the identification machinery
cannot license one), a "capacity explains timing" sentence, a single-number scaling target, a point crossing year for a
censored system, or any toy magnitude quoted as an estimate. A generator that reproduces R1–R12 and makes none of those
five claims is a genuine advance on the state of the programme; one that reproduces three of them and makes two of those
claims is a regression dressed as a result.
