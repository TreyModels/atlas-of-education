# COUNTRY_TYPOLOGY — which relations hold in which types of country

**Author:** `pattern-scout` · 2026-11-20 · task-21. Evidence = the split-sample FE regressions in `data/panel_heterogeneity.csv` (110 regressions),
thresholds in `data/country_typology.csv`, typology computed from **observed 1985–2000 country means** (no imputation).

**Thresholds (medians of the 30-country panel):** GDP pc US$1,706 (2015 const) · tax/GDP 13.1% · 1990 secondary GER 47.3% · urban share 40.2%.
**Asia** = 19 countries (CHN, HKG, KHM, PHL, KOR, JPN, VNM, THA, IDN, MYS, SGP, MMR, LAO, MNG, IND, BGD, PAK, LKA, NPL); **non-Asia** = 11.

## The six conditional relations (the deliverable Dr. Menefee asked for)

| # | Relation | Holds where | Fails where | Numbers (coef, se) | What the condition *is* |
|---|---|---|---|---|---|
| T1 | **Spending → secondary enrolment** | Asia; low 1990 secondary GER | outside Asia; near-universal systems | Asia **+0.189** (0.090); non-Asia +0.010 (0.106); GER-low +0.132 (0.072); GER-high +0.077 (0.044) | It is a *capacity-binding* relation: money buys places only when places are the constraint and the state is the marginal financier. In high-GER and non-Asian systems the marginal peso goes to quality/teachers, not to a GER that is already near the ceiling. |
| T2 | **Private provision → secondary enrolment** | Asia; low income; low tax capacity | high income; high tax capacity | Asia **+0.086*** (0.016); non-Asia +0.003 (0.111); low-income **+0.081*** (0.018); high-income +0.014 (0.084); low-tax **+0.102*** (0.018); high-tax −0.065 (0.081) | Private schooling is a **substitute for a weak state**, not a general growth engine. Where state capacity is high, private share is a composition variable with no enrolment effect. |
| T3 | **Tax capacity → education spending** | Asia; low-urban; low-GER | non-Asia; high-urban | Asia **+0.541*** (0.125); non-Asia −0.320 (0.370); low-urban **+0.582*** (0.165); low-GER **+0.431*** (0.091) | Fiscal space is only *binding* where the budget constraint actually binds. In high-income/high-urban systems, education spending is a political allocation, not a residual of the tax take. |
| T4 | **Income → tertiary enrolment** | everywhere, **strongest in Asia** | non-Asia (not significant) | Asia **+1.075*** (0.219); non-Asia +0.281 (0.475); world (pooled) **+0.848*** (0.172); low- and high-income both positive (0.846***, 0.697***) | This is the most universal relation in the file, but the *elasticity* is an Asia phenomenon — consistent with Asia's fast income growth coinciding with the tertiary transition (Korea, China, Vietnam). It is correlational; the model should treat it as a demand channel, not an estimate of the causal return. |
| T5 | **Teacher supply → primary enrolment** | low income; low tax capacity | high income; high tax capacity | low-income **+0.528*** (0.056); high-income +0.192 (0.157); low-tax **+0.510*** (0.064); high-tax +0.244 (0.155) | Capacity constraint. Where teachers are scarce (poor, low-capacity states) the teacher stock *is* the school system; where they are abundant the constraint is demand, not supply. Partly mechanical (R10). |
| T6 | **Fertility / cohort size → completion** | everywhere; strongest at low completion and low urbanisation | nowhere (holds in every split) | Asia −0.172*** (0.052); non-Asia −0.222*** (0.060); low-GER −0.171*** (0.056); low-urban −0.213*** (0.039) | The one relation that is **not** country-conditional: cohort size dilutes completion universally. This is the safest cross-country parameter in the register (R07). |

## Secondary conditionings worth recording

- **`log_cmpt_s` ~ `log_gdppc`**: non-Asia +0.488** vs Asia +0.350* — income raises completion more where baseline completion is lower
  (the non-Asia group contains the low-completion African/South-Asian-inclusive set). High-urban +0.446* vs low-urban +0.030 ns.
- **`log_ger_s` ~ `log_gdppc` (5y lag)**: Asia +0.211** vs non-Asia +0.166 ns — income→secondary is an Asia relation at this horizon.
- **`log_cmpt_s` ~ `log_ptr_p` (5y lag)**: high-income +0.579** / low-income +0.098 ns, high-urban +0.547*** — the "sign conflict" of R11 is itself
  concentrated in high-income/high-urban systems, i.e. where enrolment booms are demand-led rather than capacity-constrained.
- **`log_ger_p` ~ `log_spend_gdp`**: essentially zero everywhere (R02) — the saturation result is *not* country-conditional.

## What the typology implies for the model's country presets

| Preset | Which relations are "live" | Which are dormant |
|---|---|---|
| **PHL-like** (low-middle income, low tax capacity, high private share, large informal sector) | T1, T2, T3, T5, T6; R09 private supply; R21 gate tutoring | T4 tertiary elasticity weaker; spending→primary (R02) dead |
| **KHM-like** (low income, very low capacity, case-study shadow data) | T1, T2, T3, T5, T6 strongly; R24 urban gradient (60.5% vs 26.4%, case study) | R26 returns→tutoring (no data); teacher-tutoring rerouting untested |
| **HK-like** (high income, high capacity, near-universal secondary) | T4 only weakly (income→tertiary near saturation); R21 gate gradient (70% at S6–7) and R22 income elasticity (rich-country tutoring) | T1, T2, T3, T5 all dormant; spending has no enrolment margin |
| **CHN-like** (middle income, high state capacity, Double Reduction) | T4 strongly (income→tertiary); R25 policy shock; R23 two-margin tutoring | T2 private provision (state capacity high); R26/R29 unidentified |
| **KOR/JPN benchmark** | T4 saturated; R22 income elasticity (Korea 1.33) and R24 urban gradient (Japan 2.62×) are the *only* measured shadow relations at this income level | T1–T3, T5 dormant; R07 still active |

**Bottom line for the model:** four of the six conditional relations (T1, T2, T3, T5) are all versions of one condition — **whether the state is the
binding constraint on school places**. Country presets should carry one flag (`capacity_binding: bool`) that switches these channels on, rather than four
separate elasticities. T4 and T6 are unconditional (income demand; cohort dilution) and can be global parameters.

## 7. Complexity as a second typology dimension (task-28)

**Why add it:** the Council asked whether complexity is the missing country-type axis. The tests above say: it is a *descriptive* axis and a conditioner of one channel (education->growth), but **not** a conditioner of the spending channel. It should be added to the typology, but as a secondary axis, not as a replacement for the state-capacity flag.

**ECI levels for the six countries (SITC, 1995 -> 2024):** JPN 2.06 -> 1.54 (high, falling); KOR 1.23 -> 1.44; HKG 1.16 -> 1.42; CHN 0.72 -> 1.30 (fast catch-up); PHL 0.34 -> 0.75; KHM -1.32 -> 0.30 (from far below zero). The income ordering and the complexity ordering are *not* the same: HKG is richer than KOR but slightly less complex; CHN is poorer than HKG but converging fast.

| Typology cell | Countries (1995) | Relations that are live | Relations that are dormant |
|---|---|---|---|
| **low complexity + low income** | KHM, IND, BGD, PAK, LAO, MMR | T1 spending->enrolment, T2 private provision, T3 tax capacity, T5 teacher supply, R07 fertility, R42 completion<-ECI, **R48 schooling->growth payoff is largest here** | ECI->tertiary (income carries it), spending x ECI |
| **low complexity + high income (resource/rentier)** | MYS (1995), TUR, MEX, ZAF, NGA | T1, T2, T3 still live; R48 payoff fading | ECI->completion weak |
| **mid complexity + mid income** | CHN, THA, IDN, PHL(2024), VNM | R41 income->tertiary, R42 ECI->completion survives income, R45 ECI->growth null | R48 payoff near zero |
| **high complexity + high income** | JPN, KOR, HKG, SGP | R21 gate tutoring, R22 income elasticity, R23 two-margin shadow demand, R49 metric | T1/T2/T3/T5 dormant (capacity not binding); R48 schooling->growth payoff fades/reverses |

**The key conditional finding (state it plainly):** for the *model's* purposes, complexity is a good **state variable** and a poor **mechanism**. Use it to set a country's initial complex-job share and formal-job pool (massabm `vac_paths`, twoway `Vc0`, `eps_ec`), and to label the typology cells — but do **not** use it to switch the spending elasticity (the interaction is a clean null) and do **not** assume higher complexity means a bigger schooling payoff (the interaction is negative in this sample).
