# PRE-DECLARATION — state capacity as a first-class mechanism (capacity-gated state push)

**Owner:** experiment-runner (`deepseek-exp1`). **Status:** predeclared before any capacity-gated anchor run.
**Authority:** user directive (20 Nov 2026, state capacity first-class), Council A6/A7 (R23–R25), R26 capacity rule,
D56–D58/R27 phase cap, brief 013 `UNIVERSALIZATION_MILESTONES.md` (M0–M4), and the amended `PRE_ANCHOR_A1.md`
(sha b7020cf4…). Simulated vs observed labelled throughout; **capacity enters as an observed input, never a target**;
**no crossing year is ever fitted**.

## 1. The three observed capacity inputs (with on-disk status)
| dimension | input | on-disk series | status |
|---|---|---|---|
| **Fiscal** | government expenditure on education (% GDP), (% of govt expenditure), per-student spend, revenue/tax capacity | WDI `SE.XPD.TOTL.GD.ZS`-type series in `04_data/data/wdi_4countries_long.csv` and `10_massification/data/JOBS_AND_MARKETS_PANEL.csv`; HKG EDB table 2020–25 | observed where present; **PHL per-student/revenue series NOT found → declared DATA BLOCKED, not imputed** |
| **Delivery** | pupil–teacher ratio path, teacher counts/hires, classrooms/public schools | `10_massification/data/SCHOOL_EXPANSION.csv` (PHL high-school PTR **37 (2000) → 27 (2014) → 24 (2017)**, observed/high; teachers hired 2012–16 ≈ 200k elementary + 40k SHS, **check/medium**; classroom ratios 2010/2019/2021 observed/high; classroom construction by year **UNABLE = DATA ASK**); WDI PTR primary/secondary + teacher counts | usable observed delivery path; annual classroom construction missing |
| **Enforcement** | compulsory-schooling duration; enforcement proxies (attendance, conditionalities, truancy/penalty) | `POLICY_TIMELINE.csv` (PHL 1987 Constitution free primary/secondary; RA 10533 2013 → 13-year cycle); 4Ps conditionality (status `check`) | duration observed as policy fact; **attendance/truancy/penalty enforcement series NOT on disk → declared DATA BLOCKED; a declared proxy is used (see §3), not a measurement** |

## 2. Gate function (declared form and parameters, NOT fitted to crossing years)
`effective_state_push_t = marker_t × G(C_t)` with
- `C_t` = capacity index in [0,1], a **declared weighted composite** of standardised capacity inputs:
  delivery 0.5, fiscal 0.3, enforcement 0.2 (weights declared; sensitivity reported for ±0.1);
  standardisation = min–max over the observed window per input; annual interpolation between observed points;
  missing input for a country → its weight is dropped and the remaining weights renormalised (declared; no imputation);
- `G(C) = 1 / (1 + exp(−(C − C0)/s))` with declared `C0 = 0.5`, `s = 0.15` (capacity gate opens around the midpoint;
  parameters **declared**, sensitivity at C0 ∈ {0.4,0.5,0.6}, s ∈ {0.10,0.15,0.20});
- `marker_t` = declared policy marker (K-12 2013 / SHS 2016-17; free SHS 2016; free tertiary RA 10931 2018) with
  affected level and transition cohorts declared — still only a **candidate marker under R24**, never assumed to move
  levels unless the alignment test passes;
- the state-push magnitude enters only through the gate × a declared scale parameter `push_scale` (declared
  prior range, fitted only inside the brief-013 fit window, never on crossing years).

## 3. Capacity-timing hypothesis (the PHL non-alignment test)
**Hypothesis:** PHL's laws did not move levels because capacity lagged; the crossing follows **capacity**, not the law
date. Evidence to compute (descriptive, R25): delivery capacity improved 2012–2017 (PTR 37→27→24; JHS classroom ratio
54→39 between 2010 and 2019; ≈240k teachers hired 2012–16), i.e. capacity moved in the same window as the primary ≥90
crossing (**2017**) while the law dates do not align (1987 Constitution → 2017/2021 crossing = 31 y; K-12 2016 →
upper-secondary mass already crossed ≤1999).
**Declared test and threshold:** a capacity episode is "aligned" if its observed improvement interval overlaps the
observed crossing band ±5 y (R24-style). Predicted result (declared now): **capacity aligns, law does not**; the
capacity-gated arm should reproduce the crossing ordering better than the law-only arm. Failure to find alignment is
reported as such (null is valid).
**Model-side discriminating test (within-model, declared):** four arms, identical fit/holdout and seeds —
(a) law-only (`G ≡ 1`), (b) **capacity-gated** (marker × G(C)), (c) capacity-only (no marker), (d) no state push.
The capacity-gated arm is credited only if it reproduces the crossing ordering/spacing within tolerance while the
law-only arm does not; otherwise report EQUIVALENT/no identification (R13).

## 4. Capacity in the portability test (HKG/CHN)
The **same gate function and declared parameters** transfer; capacity levels are re-set from each country's observed
series (HKG is high-capacity/100% urban with 2009 free upper-secondary aligned at +9.08 pp t=5.20; CHN has a 1999
tertiary expansion aligned at +4.70 pp t=7.94 but its 1986 compulsory law misses the primary crossing by 27 y).
Declared expectation: the gate explains why the same marker fails in CHN 1986 (low capacity at that date) and works in
HKG 2009 / CHN 1999 (capacity high); HKG/CHN may need **different capacity levels** to produce the same crossing — the
report states what transfers and what does not. Behavioural re-fit remains FAIL (R20); only declared country inputs
re-set.

## 5. Roles, caps and stop rules
- **Capacity = observed input, never a target; crossing years = HOLDOUT outcome, never fitted (R4/R5/R19/R24).**
- R26: capacity is **level-specific**; upper-secondary PTR is an **expansion marker only** (not a universalization
  driver); PIDS equity analysis is **check-only**. R25: event windows descriptive, quality A/B/C only, quality-C
  inferred episodes excluded. R27: one cell — no further capacity/scaling iteration without a new Council decision.
- **Phase cap stands (D56/R17/R23):** the model class fails the A1/A3 scaling criterion; the anchor verdict is at most
  **PARTIAL/DESCRIPTIVE, never PASS**, with observational equivalence where rivals tie and **no direction claim**.
  The scaling FAIL is reported in every result table.
- **Declared limitations:** enforcement is proxied (no attendance/truancy series); per-student/revenue capacity and
  annual classroom construction are DATA BLOCKED (data ask); the gate parameters are declared, not estimated, and
  their sensitivity is reported rather than tuned.

## AMENDMENT A10 / R29 (Council D62–D64; applied before the descriptive run)
1. **Gate form changed to a power function:** `G(C) = C^κ`, **κ ∈ [0.5, 1.0]** (declared default κ=0.75; sensitivity
   κ∈{0.5,0.75,1.0}), replacing the earlier logistic. `C` is the **observed** capacity trajectory (never a
   target/fitted); weights predeclared with sensitivity; missing inputs dropped, not imputed.
2. **Floor/ceiling split (level-specific, non-monotone):** capacity is a **necessary delivery precondition for FLOOR
   universalization** (primary/lower-secondary completion, intake) and **not sufficient for CEILING universalization**
   (upper-secondary/tertiary completion). The capacity-gated push therefore applies fully to floor levels and only a
   **declared saturating share** (ceiling_share = 0.25, declared) to ceiling levels; the model **may not generate
   upper-secondary/tertiary universalization the record does not show** (R6/R29). No tuning to rescue.
3. **Ceiling residual predeclared (report after the run):** observed residual to the ceiling threshold per level —
   PHL **upper-secondary completion 75.03 vs 90 → residual 14.97 pp**; tertiary GER 52.99 vs 50 → **crossed (mass
   ceiling reached; residual −2.99 pp, i.e. above threshold)**; lower-secondary completion 92.41 vs 90 → crossed
   (residual −2.41 pp); primary 98.30 vs 95 → crossed (residual −3.30 pp). Candidate accounts to list/test where an
   observable exists: (i) foregone income/opportunity cost of upper-secondary attendance; (ii) demand/returns to
   upper-secondary vs tertiary; (iii) gate structure/credential (transition rules, tertiary selection); (iv)
   enforcement (compulsory duration/conditionality/penalties). Where no discriminating observable exists, report
   **UNABLE**, not a story; no direction claim (R13).
4. **Law-only vs law×capacity requirement:** the capacity-timing claim is credited **only if** the
   `law × capacity` arm **beats the law-only arm on the crossing-year estimand** (M2/M4 timing and the M3
   non-crossing). If they tie or capacity-gated performs worse, report **EQUIVALENT/FAIL** — capacity does not earn
   the claim (R24/R29). The capacity-response function is fixed under portability; thresholds/trajectories remain
   declared country inputs (R20/R28).
