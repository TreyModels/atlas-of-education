# FINDINGS — DT1–DT5 battery (brief 020)

**Worker:** DT · **Date:** 2026-11-20 · **Scope:** `10_massification/extensions/dt_2026-11-20/`
**Predeclaration:** [`PRE_DECLARATIONS.md`](PRE_DECLARATIONS.md), frozen before the first run (sha256 in
[`RUN_MANIFEST.json`](RUN_MANIFEST.json)). **No threshold was changed after results.**
**Inputs:** observed on-disk series only. No HELD series was proxied or fabricated; DT3 is design-only.

## Battery at a glance

| test | what it asks | statistic | threshold | verdict |
|---|---|---|---|---|
| **DT1** | does literacy track lagged schooling exposure after income/urbanization? | median income-partial ρ = **+0.015** (raw median +0.387); 2/5 countries ≥ +0.40; n=91, 5 countries | median partial ρ ≥ +0.40, sign retained | **NULL (negative)** |
| **DT2** | is adult-literacy change driven by the schooling-exposed entrant share after income control? | `E_entrant` b = **+1.605** (p=0.00036); `gap0` b = +0.327 = **0.20 ×** `E_entrant`; n=241, 25 countries | b ≥ +1.0 & p<0.05; gap0 ≤ 0.5×E | **NON-NULL (support)** |
| **DT3** | does a reform move the behavioural syndrome? | UNABLE — no series on disk | ≥5% of within-series SD + parallel trends | **UNABLE (HELD, design-only)** |
| **DT4** | does installation depth order literacy and predict persistence? | partial ρ = **+0.202**; top-half zero-reversal **10/11 (90.9%)**; bottom-half ≥1 reversal **2/11 (18.2%)**; n=27 | ρ ≥ +0.40; top ≥80%; bottom ≥40% | **NULL (falsifier)** |
| **DT5** | joint induced-competence + asymmetric-exit signature? | joint **14/24 (58.3%)**; PHL residual z = **−0.508** | joint ≥50%; PHL z ≤ −1.0 | **NULL (falsifier)** |

**One-line answer to the Council's gate: DT1 is null, DT2 is non-null → the D104 conditional gate is NOT met, and
the induction grounding is PARKED.** DT2 passing alone cannot open it.

---

## 1. DT1 — literacy does not survive income and urbanization control on the reachable overlap

**Plain reading.** The block asks whether youth literacy rises with primary completion five years earlier, once
income and urbanization are held constant. On the 30-country panel, only **5 countries** have the required
≥12 overlapping years of youth literacy, lagged primary completion, income and urbanization: **COL, IDN, LKA, MEX,
PER** (91 country-years). In those five, the uncontrolled rank correlation is moderate (median +0.387), but the
income-and-urban-partial correlation collapses to a **median of +0.015**. Only **2 of 5** countries (IDN +0.533,
MEX +0.436) keep ρ ≥ +0.40; PER (+0.015), LKA (+0.006) and COL (−0.003) lose the association almost entirely.

**Reading.** At this granularity, literacy is **not orderable by lagged schooling exposure after income and
urbanization** — the block's own falsifier wording: "literacy orderable by income alone; induction has no footprint
at this granularity." This is a genuine null, not a sign flip: the raw association is positive, and the control
variables absorb it.

**Two honest qualifications.** (i) **Coverage is thin** — 5 of 30 countries meet the eligibility rule, so the null
rests on a small, non-random set (four middle-income Latin American/Asian cases plus Sri Lanka). It is a real test
of the fixed rule, but not a strong one. (ii) This does **not** contradict the on-disk E9 (`lit_youth ~ log
completion` +29.9, within-R² 0.55): E9 is a pooled two-way FE association **without** income/urban controls; DT1 is
the income-controlled, per-country version, and the difference between the two is exactly the finding.

**Label:** DERIVED. **Diagnostic value:** partially diagnostic; a positive would have been weak evidence (literacy is
definitionally taught in school), so a null is correspondingly strong against the simple exposure story at this
granularity.

---

## 2. DT2 — the entrant-share signature survives income control (the one non-null)

**Plain reading.** The on-disk cohort decomposition splits adult-literacy change into an entrant component
(`E_entrant`), an exit component, and a residual. Re-estimated with log income added and with the initial
literacy gap (`gap0`) in the same model, the entrant coefficient is **+1.605 (p=0.00036)** — still above the
block's +1.0 support bar and still significant. The initial-gap coefficient is **+0.327**, which is **0.20 ×**
the entrant coefficient, comfortably below the block's 0.5× subordination bar. Income itself is negative and
insignificant (−1.35, p=0.58). The income-controlled entrant-only model gives +1.634 (p=0.0013). The two-way FE
specification reproduces the on-disk D1 coefficient **+1.654508** to 2.2×10⁻¹⁶, so the estimator is the same one
that produced the existing decomposition regressions.

**Reading.** The exposure-driven (induction-side) signature **does** survive income control, and the initial-gap
(secular/catch-up) channel does not dominate it. On the block's own terms this is a **support**. It is the most
diagnostic of the five tests and the only one that lands non-null.

**What it does not mean.** Cohort replacement is partly arithmetic — entrants mechanically replace exits — so the
raw coefficient is not the discriminating part. The discriminating part is precisely what passed: **income-controlled
survival + `gap0` subordination**. Even so, this is a descriptive association: it does not identify a causal
mechanism, does not validate the assembly paper, and — because DT1 is null — **cannot by itself satisfy the D104
gate**. The two papers' own "most diagnostic" test survives; the cheapest test does not.

**Label:** DERIVED.

---

## 3. DT3 — schedule-discipline: design-only, HELD, never scored

**Plain reading.** The block asks whether a compulsory-schooling reform or grade discontinuity moves a behavioural
syndrome (punctuality, schedule compliance, arrest/incarceration, evaluative orientation) by at least 5% of a
within-series SD, surviving a pre-declared parallel-trends check. **There is no reform/behavioural series on disk.**
The paper's behavioural citations are external, cited not measured (D49).

**Design recorded (not executed):** difference-in-differences / regression discontinuity on a reform or grade
threshold, treated vs adjacent untreated cohorts, pre-declared parallel-trends test, outcome = behavioural syndrome
measure; support iff the reform-associated shift is ≥5% of a within-series SD and survives the pre-trend check.

**Status:** **UNABLE (HELD, design-only)**. No number was produced anywhere in this battery. This is the Council's
drop-first (D103); its absence is **not** evidence for or against the formatting claim.

---

## 4. DT4 — depth does not order literacy, and the reversal gradient fails

**Plain reading.** The block builds an installation-depth proxy (standardized primary-completion level × standardized
declared schooling duration) and asks two things: does depth order the literacy tracer after income control, and do
high-depth countries avoid ≥3 pp literacy reversals over 1995–2024?

- **Ordering (a):** income-partial ρ(literacy, depth) = **+0.202**, below the +0.40 bar.
- **Persistence (b):** the top depth half has **10/11 (90.9%)** countries with zero reversal — this passes the ≥80%
  bar — but the bottom half has only **2/11 (18.2%)** countries with at least one reversal, far below the required
  ≥40%.

So the falsifier fires: there is **no depth gradient in reversal incidence** of the required shape, and the ordering
is too weak. Verdict **NULL**.

**An important construction caveat.** The block specifies the product of two standardized variables. Because a
z-score can be negative, countries with **below-average duration** get a negative depth even when completion is
high — COL, SGP and PER (completion means 106.6, 99.4 and 98.1) sit in the bottom half, while NPL and LAO
(completion means 91.9 and 81.1) sit in the top half. The resulting ordering is therefore hard to read as
"installation depth" in the intended monotone sense; the primary-duration-only sensitivity gives ρ = **−0.071**
(sign flip, also null). The null is the predeclared result and is reported as such, but it should be treated as
**weak evidence against the substantive claim**, not a clean refutation — the proxy does not behave as a clean
depth index. It would be a predeclaration violation to re-specify the proxy now to rescue the result.

**Label:** DERIVED. n=27 (BRA lacks primary completion; JPN and HKG lack adult literacy), income-confounded, low
power (Y1 lesson).

---

## 5. DT5 — the joint signature is present, but the PHL ceiling is not an unexplained outlier

**Plain reading.** The block defines a "literacy-universalized" country (adult literacy ≥90 by 2024) and a
"ceiling-persistent" country (upper-secondary attainment never ≥90 and no ≥5 pp sustained reversal), then asks
whether both occur in ≥50% of the panel **and** whether the PHL ceiling is unexplained by the same income/completion
observables.

- **Joint signature:** **14/24 (58.3%)** — passes the ≥50% bar. (16/24 are literacy-universalized; 21/24 are
  ceiling-persistent.)
- **PHL check:** in a cross-country regression of upper-secondary attainment on log income and primary completion,
  PHL sits **0.508 residual SD below** prediction. Under the fixed cut (−1.0), that is **not** an unexplained
  ceiling.

Verdict **NULL**. The "junction" reading does not earn comparative footing: the PHL ceiling is broadly what its own
income and completion predict.

**Robustness and caveats.** The PHL 2021 drop in WDI `SE.SEC.CUAT.UP.ZS` (58.46 in 2013 → 32.43 in 2021) mechanically
triggers the ≥5 pp sustained-reversal rule, so PHL is not counted as ceiling-persistent; even if it were, the joint
share would be 15/24 (62.5%) and the verdict would still be NULL on the PHL residual. Using the pre-break peak
(z ≈ +1.01) or the `UNIVERSALIZATION_SERIES` completion measure (z ≈ +2.06) also fails the "not explained" cut. The
null is therefore robust to the PHL measurement choice, but the series break should be recorded as a data caveat.
As the block itself warns, at n=24 and with the D63 ceiling already known this test is **near-circular** — the
weakest diagnostic of the five. It does not re-score WT2/WT4 and does not reopen C1–C4.

**Label:** DERIVED.

---

## 6. Paper-status implication (D104 gate)

D104 is binding: **"if DT1 AND DT2 both return non-null, the generator may name the induction mechanism in its
declared-assumption provenance; if either returns null, the induction grounding is PARKED."**

Here **DT1 = NULL** and **DT2 = NON-NULL**. The conjunction is **false**.

- The induction grounding is **PARKED**. Amendments A1 (literacy = takeoff prerequisite) and A3 ("school formats
  persons") keep their current **"declared assumption"** label with **no theory citation**.
- No model change follows: no "induction" parameter, no new layer, no "developmental-window" term (D104).
- The assembly paper remains **theory-only** — a candidate frame for the write-up, never evidence; its micro
  citations do not enter the verified ledger (D49).
- DT2's support is a **descriptive** result: it says the entrant-share signature survives income control in this
  decomposition. It does **not** say the assembly account is true, does not "reproduce induction", and does not
  validate the paper.

Because DT1's null is the binding constraint, the most useful next step is **not** to re-run DT1 with a different
aggregation or to substitute a different literacy tracer; that would be a post-hoc rescue. If the Council wants to
revisit the induction question, it needs a **new predeclared test with more country coverage** (the 5-country
overlap is the binding data limit), not a threshold change here.

---

## 7. What this cannot claim

1. **No causal claim and no direction claim.** Every statistic is a descriptive association. DT2's `E_entrant`
   coefficient is not an identified causal effect; DT1/DT4/DT5 are partial correlations and joint-presence shares.
2. **A DT PASS is not validation.** DT2 passing does not validate the assembly paper, the hysteresis paper, or the
   combined frame. The papers remain untested theory; neither may be cited as evidence.
3. **No C1–C4 reopening; no WT re-scoring.** Nothing here reopens the closed claims or re-scores WT1–WT5. DT5 is the
   joint-presence version only and does not touch the D63 ceiling residual as "explained".
4. **No model change.** The D104 gate is not met (DT1 null), so the induction grounding is PARKED. A DT PASS cannot
   create a fitted "induction parameter" (R4/R27).
5. **DT3 cannot speak.** It is HELD/design-only; its absence is not evidence for or against the formatting claim.
6. **Weak tests are labelled weak.** DT1 is data-thin (5 countries) and partially diagnostic; DT2 is partly
   mechanical; DT4's depth proxy is duration-sign-sensitive and income-confounded; DT5 is near-circular. None is a
   law, and none should travel as one.
7. **No external data, no web, no fabrication.** HELD series were neither read nor proxied. Anthropometric,
   behavioural/reform, and adoption/migrant series remain HELD.

---

## 8. Decision-relevant numbers

1. **DT1 median income-partial ρ = +0.015** (raw +0.387), only **2/5** countries ≥ +0.40 → the exposure association
   does not survive income/urbanization control on the reachable overlap.
2. **DT2 `E_entrant` = +1.605 (p=0.00036)**, `gap0` = 0.20 × `E_entrant` → the income-controlled entrant signature
   survives; the on-disk D1 (+1.654508) reproduces exactly.
3. **DT4 partial ρ = +0.202**, bottom-half reversal share **18.2%** (required ≥40%) → no depth gradient of the
   required shape; depth proxy construction is a caveat.
4. **DT5 joint signature 58.3% but PHL z = −0.508** (required ≤ −1.0) → joint presence alone does not make the PHL
   ceiling an unexplained junction phenomenon.
5. **Gate outcome: DT1 NULL ∧ DT2 NON-NULL → induction grounding PARKED**; A1/A3 stay "declared", no theory citation.

**Bottom line:** the battery returns **one non-null (DT2), three nulls (DT1, DT4, DT5), one UNABLE (DT3)**. The
one strongly diagnostic test survives; the cheapest mechanism test does not; the D104 gate is not met. The honest
summary is that the induction reading has a **descriptive footprint in the cohort decomposition** but **not** in the
income-controlled cross-country literacy association, and the programme should keep the assembly paper as a declared
theory frame rather than a grounded mechanism.

---

## 9. Determinism

`code/run_dt.py` was run twice into `results/run1/` and `results/run2/`. `RESULTS.csv` and `DETAIL.csv` are
**byte-identical** across runs (sha256 match, `cmp` clean). No RNG, no seed, no network. Full hashes are in
`RUN_MANIFEST.json`.
