<!-- Writer: lit-archivist, 2026-11-20, task-35. Scope: literature only. No model output below.
Verification legend: VERIFIED = primary text read this session (file in 02_lit/raw/ or /tmp archive, hash noted).
STANDARD-CITATION = canonical account, primary text NOT retrieved this session; the mechanism and any
thresholds are as standardly cited in the literature, and must be checked against the original before
publication. NOT-FOUND = searched and did not find; treat as a gap, not as zero. -->
# MASSIFICATION_THEORY — the accounts, their mechanisms, timing predictions, and falsifiers

**Purpose.** The Council's brief 013 and the model's success criteria need *discriminating* predictions, not a literature review. Each section below ends with **timing prediction** and **falsifier** because those are what the model must be able to fail.

---

## 1. Trow (1973) — access phases — STANDARD-CITATION
**Mechanism.** Higher-education systems pass through three phases defined by the enrolment ratio of the relevant age cohort: **elite (<15%)**, **mass (15–50%)**, **universal (>50%)**. Each phase has its own function, curriculum, institutional form and political logic; the transition is not merely quantitative.
**Equation.** None. Trow's thresholds are descriptive cut-points, not a fitted curve.
**Timing prediction.** Phase transitions cluster around the 15% and 50% ratios; the *behaviour* of the system changes at those ratios (e.g. selection logic, drop-out tolerance).
**Falsifier.** A system that crosses 15% or 50% with no change in selection/curriculum/attrition regime — or sustained growth through both thresholds with no discontinuity. **Note the scope limit: Trow is a theory of tertiary access, not of universal primary/secondary completion.** The programme's first-order object (universalization of *schooling*) is outside Trow's original scope; borrowing his thresholds for ANER/primary series would be a category error.

## 2. Schofer & Meyer (2005), *ASR* 70(6) — world society / institutional expansion — STANDARD-CITATION
**Mechanism.** Higher-education expansion is driven by globally legitimated models of the modern nation-state (mass education as an attribute of statehood), transmitted through international organisations and professional networks, and legitimated by science and democracy. Expansion is therefore partly *decoupled* from immediate economic demand.
**Equation.** Empirical panel model (country fixed effects over the 20th century) with national wealth, democratisation, science, and world-society embeddedness as covariates. I did not retrieve the exact specification or coefficients this session.
**Timing prediction.** Broad, roughly synchronous cross-national expansion; countries at very different income levels expanding together; expansion continues where economic returns are weak.
**Falsifier.** Expansion tracking economic returns tightly with little cross-national synchrony; expansion stalling when world-society ties weaken while domestic demand is unchanged.
**Why it matters for push-pull.** This is the classic **supply-push** account. It predicts education expansion *leading* labour-market absorption, and predicts credential expansion in economies with no skill shortage.

## 3. Raftery & Hout (1993), *ASR* 58(1) — maximally maintained inequality (MMI) — STANDARD-CITATION
**Mechanism.** When a level of education expands, advantaged groups saturate it first; inequality in *conditional transition probabilities* falls only after the advantaged approach saturation. Expansion alone does not equalise.
**Equation.** Class-specific conditional transition probabilities `P(transition | origin class, level)`; inequality measured as odds ratios across origins at each transition. No closed-form law.
**Timing prediction.** Inequality falls **after** saturation of a level, not during expansion. Order of magnitude: expansion first widens, then narrows, the origin gradient.
**Falsifier.** Inequality falling *during* rapid expansion before saturation; or saturation with persistent odds ratios.
**Model use.** This is the natural benchmark against which the programme's "floor" mechanism must be compared: MMI predicts the *gradient* dynamics without any relational-floor mechanism. If the model's floor adds nothing beyond saturation, MMI wins.

## 4. Breen & Goldthorpe (1997) — relative risk aversion (RRA) — STANDARD-CITATION
**Mechanism.** Class differences in educational continuation are produced by **rational** choices under class-specific costs, benefits and *relative* risk: families compare the expected class position from continuing against the risk of downward mobility from not continuing. Relative risk aversion, not differential ability, generates the gradient.
**Equation.** Expected-utility comparison over class destinations; the canonical parameter is relative risk aversion in the expected-utility functional. I did not read the original coefficients.
**Timing prediction.** The gradient persists even as absolute costs fall, because it is relative position that is being defended; universalization compresses the gradient only when continuing becomes the low-risk option for all classes.
**Falsifier.** Gradient driven by ability/attainment differences only; or gradient vanishing when direct costs fall.
**Model use.** This is the *only* theory in the set that supplies a household-side microfoundation for "pay even when absolute returns fall", and it does so without the programme's insurance story. The model must not claim novelty for a mechanism that RRA already supplies in rational-choice form.

## 5. Human capital — Becker (1964), Mincer (1974) — STANDARD-CITATION for Mincer form
**Mechanism.** Schooling raises productivity; households invest until marginal private return equals marginal cost (including foregone earnings).
**Equation (canonical Mincer, safe to state).** `ln Y = α + rS + β₁X + β₂X² + ε`, where `S` = years of schooling, `X` = experience, `r` = private return to a year of schooling.
**Verified magnitude (VERIFIED, WPS8402):** global average private return to one additional year of schooling **≈8.8%** (headline "about 9%"), EAP **8.7%**, social returns **>10% at secondary and higher**. Source: Psacharopoulos & Patrinos 2018, WB PRWP 8402 (`02_lit/raw/psach_patrinos2018_wps8402.txt`).
**Timing prediction.** Expansion follows *expected* returns, with a lag equal to the perceived payoff horizon; expansion should *slow* when returns fall.
**Falsifier.** The famous one: **expansion while absolute returns fall**. That is the programme's motivating puzzle, and it is a genuine anomaly for the simplest version.

## 6. Signalling (Spence 1973) and filtering (Arrow 1973) — STANDARD-CITATION
**Mechanism.** Education conveys pre-existing ability as a signal; firms pay for the signal, not productivity. Private returns can be positive while social returns are near zero; the equilibrium can be Pareto-inefficient over-investment.
**Equation.** Signalling equilibrium conditions on cost-of-acquisition differences by type; screening/filter model with test costs. Not reproduced here (originals not retrieved).
**Timing prediction.** Investment continues as long as the signal separates; it *intensifies* as the signal saturates (defensive acquisition of the next tier).
**Falsifier.** Employer learning about productivity eroding the credential's return (the "employer learning" literature); or returns surviving after ability controls.
**Note.** If the manuscript's household story rests on signalling, it must engage the empirical signalling critique and the ~8.8% Mincer estimate jointly — the two are in tension.

## 7. Job competition — Thurow (1975) — STANDARD-CITATION
**Mechanism.** Workers queue for jobs ranked by **training cost**, not by skill price; education moves a worker up the queue. Schooling is therefore **defensive**: its value is relative position, not productivity.
**Equation.** Labour queue with rank by background/training cost; wage set by the job, not the worker. No closed form reproduced.
**Timing prediction.** Education expands whenever the queue lengthens, regardless of skill demand; the *level* required rises with the queue, not with job content.
**Falsifier.** Wage variation explained by worker attributes within job cells; queue position not predicting access after controls.

## 8. Collins (1979) — credential inflation — STANDARD-CITATION
**Mechanism.** Credentials are status-group closure devices; expansion produces inflation, with the required credential ratcheting up while job content is unchanged.
**Timing prediction.** Ratchet, not equilibrium: each credential level devalues and is superseded.
**Falsifier.** Stable credential requirements over long periods with rising schooling; or returns stable while supply doubles.

## 9. State-building — Gellner (1983), Tilly (1990), Paglayan (2024) — STANDARD-CITATION (Paglayan verified in earlier ledger as cited, not read)
**Mechanism.** Gellner: industrial society requires standardized, literate, mobile workers → mass schooling. Tilly: extraction/administration needs legible populations. Paglayan: mass schooling often expanded *after internal conflict* to instil order, not in response to economic demand.
**Timing prediction.** Expansion follows state capacity, war/conflict and administrative need, not returns.
**Falsifier.** Expansion uncorrelated with state capacity or conflict; or expansion predicted by returns after controlling for capacity.
**Model use.** The programme's "state capture" story is a variant of this; Paglayan's non-fiscal motive is the direct competitor to a purely fiscal state.

## 10. Benavot — curriculum and expansion — STANDARD-CITATION
**Mechanism.** Primary enrolment expanded 1870–1940 in a patterned way across countries with common institutional features; curriculum content (particularly vocational vs general) responds to political and institutional forces more than to labour demand. Benavot's vocational-education work is the standard citation for the claim that vocational tracks expand/decline for political reasons.
**Timing prediction.** Expansion waves synchronised across countries; vocational share not tracking skill demand.
**Falsifier.** Vocational share tracking sectoral demand closely.

## 11. Recent formal models (from `02_lit/MODEL_CARDS.md`, all VERIFIED at equation level except where noted)
| Model | Mechanism | Timing prediction | Falsifier |
|---|---|---|---|
| **Yoo (2003)** | Rent-seeking contest; fixed bar `F(αe−t*)` vs endogenous quota cutoff | Effort peaks near the gate; aggregate rent seeking rises when the cutoff sits mid-distribution | Cutoff placed at extremes reduces aggregate effort (testable) |
| **Kim (2007)** | Two-family game; `W>2C` ⇒ PD | Defensive investment whenever benefit > 2× cost | Equilibrium without tutoring when `W<2C` |
| **Kang (2026)** | Estimated dynamic tournament; seats set tier cutoffs | 77% of secondary tutoring spend competition-driven (89% final year) | Equalising tiers collapses the competition share |
| **GXL (2017)** | SD pipeline; cascading + provider reinforcement (TPA) | Degree supply overshoots job demand after shocks; U-shaped in `r` | Removing provider feedback kills the overshoot |
| **He (2024)** | `S_cut = S̄ + kσ_S`; log utility | Effort concentrated near the mean+kσ line | Bar drawn at extremes reduces effort |
| **Ostrovsky & Schwarz (2010)** | Transcript compression; balanced disclosure | More-than-balanced disclosure ⇒ early contracting (unraveling) | Balanced disclosure ⇒ no unraveling |
| **Yang (2026)** — ABSTRACT ONLY | OLG, ranking admission, exam vs productive skills | Bans cause welfare losses; tutoring tax dominates | Full text not read — equations unverified |

## 12. Synthesis: the three genuinely rival massification mechanisms
1. **Returns-driven (human capital)**: expansion tracks returns. *Discriminating prediction:* expansion decelerates when returns fall.
2. **Positional/defensive (job competition, signalling, Collins, Kang)**: expansion intensifies as returns fall. *Discriminating prediction:* investment rises with saturation and with cohort size, independent of returns.
3. **Institutional/state (world society, state-building)**: expansion tracks legitimacy, state capacity and conflict, largely independent of both. *Discriminating prediction:* expansion in economies with no skill shortage and low returns; expansion after state-capacity/conflict shocks, not after return shocks.

**These three are separately falsifiable only if the data can separate returns, saturation and state capacity as predictors.** That is the identification problem the model must be built to fail or pass — and it is the core of `PUSH_PULL.md`.

---

## 13. Dated universalization timing — see `UNIVERSALIZATION_TIMING.md`
Added on user directive: for JPN/KOR/HKG universalization is achieved, so the research question is **when**. That file gives dated crossings by level (DERIVED from the UIS/GMR series on disk, with pre-1970 anchors labelled STANDARD-CITATION), the mechanisms the literature credits, and — the part that matters for brief-013 — **what each rival theory predicts about the crossing year**, with a falsifier each. Short version: Trow predicts no calendar date at all (only behaviour changes at the ratio); world society predicts cross-national *synchrony*; MMI predicts class-ordered crossings following lower-level saturation; human capital predicts crossings lagging returns; push-pull predicts demand-led crossings *following* job growth; state-building predicts crossings clustering after wars/disturbances (Meiji 1868, Korea 1950-53, HK 1966-67). The three cases form an accidental natural experiment on the trigger, and the literature pattern currently favours **state-building/order shocks as the trigger with demand shaping the upper levels** — a testable claim, not an established one.
