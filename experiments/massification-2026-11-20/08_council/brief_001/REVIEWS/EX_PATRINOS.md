> **SYNTHETIC EXERCISE.** Panelists are AI-constructed composite personas whose positions are inferred from the
> published literature. Nothing in this file is a statement by, or endorsed by, the named individuals or any living
> person; names identify the published work each composite draws on, not participants in a deliberation.

# REVIEW — PATRINOS composite (drawing on Psacharopoulos & Patrinos 2018; Becker 1964; steel-man for the competitive rival) — brief_001

**G. GROUNDING.** Documented: the returns-to-education programme (Psacharopoulos & Patrinos 2018, decennial review)
finds private returns to schooling remain substantial, decline as schooling expands, and vary by level and region;
policy conclusion is evidence-based investment, not rejection of human capital. **COUNCIL EXTRAPOLATION:** my
steel-man of the competitive model below is mine and is deliberately given its best form. Basis: publication-level,
no full text fetched.

**M. MODEL RENDERING (KIDS) — the rival at its best.** M1: households by wealth quintile; wages set by supply and
demand with imperfect substitution (CES) between degree and diploma labour; formal and informal sectors both exist;
credit constraints and option value included, because a serious human-capital model has them. M2: investment
responds to expected marginal return net of costs and risk, with liquidity limits. M3: elasticity of substitution σ,
informal-sector wage, vacancy path — all explicit. M4 observable in this brief: after a graduate-supply shock with
formal vacancies fixed, diploma holders' absolute income and their probability of *any* formal work. M5 nesting: the
October model is the special case σ = ∞ within formal slots and a hard eligibility cut. M6 falsifier: a matched
supply shock that raises diploma holders' income in the rival while the surplus model lowers it — and the reverse.
M7 KIDS: both worlds must describe the same institutions (formal/informal margin, hiring rule, vacancy response)
before either is called a rival.

**A. VERDICTS.** C1 **ESTABLISHED** (reproduction: means match stored 4-rep within 0.013; see
`03_audit/logs/floor_test.log` 9–14 and stored lines 7–10). C2 **SIMULATION-ONLY** (see B). C3 **NOT ESTABLISHED** as
a beat of the competitive rival: the rival has no formal sector, so the headline outcome is undefined there
(`03_audit/runs/massabm/grad_supply/findings.txt` line 8 shows formal rate 0.000), and the fixed-vacancy, fixed-slot
rule is doing the work. **CONDITIONALLY SUPPORTED** only for the income-sign statement at these coded assumptions.
C4 **SIMULATION-ONLY**, and regime-dependent: employer contribution 1.49 of 4.29 under the skill world but 0.04
under the weak-skill world (necessity findings line 16 vs 28). C5 **SIMULATION-ONLY** (and Yoo already has it, per
C6). C6 **ESTABLISHED**. C7 **ESTABLISHED**. C8/C9 **UNABLE TO ASSESS**.

**B. WHAT IS IMPOSED.** C3's result follows from two coded choices: (i) formal jobs are slots allocated by
credentials, so more graduates mechanically displace diploma holders; (ii) vacancies are fixed, so there is nowhere
for displaced holders to go. Under those rules the sign is not a discovery; it is an accounting identity with a
utility function. A discovery would require the sign to survive endogenous vacancy posting and a rival with the same
margin.

**C. ESTIMAND AND DENOMINATOR PROBLEMS.** "Diploma holders' formal-employment rate" exists in one world and not the
other, so the paper's claim of "opposite answers on the same outcome" is true for absolute income and false for the
formal rate. Baseline diploma income differs (1.57 vs 1.07), so the shocks are not applied to comparable economies.
"Absolute income" is model units; fine if labelled.

**D. TYPE CONFUSION.** Comparative statics of two model structures are being described as a test between accounts.
The October text admits "they are not evidence about any country"; the *synthesis* of the result must carry the same
hedge, and Prediction 2 must say the rival arm needs the formal/informal margin.

**E. STRONGEST DEFENSIBLE SENTENCE.** "With formal vacancies fixed and hiring rationed by credentials, an increase
in graduate supply lowers diploma holders' probability of formal work and slightly lowers their absolute income —
a property of slot-rationed hiring; in a competitive CES world without rationed formal slots the same shock raises
their income as they become scarcer. The comparison is between architectures, not measurements."

**F. STRONGEST NEGATIVE RESULT.** The household knockouts (C4) reverse under weak skill returns; and the graduate
shock's income effect in the surplus model is tiny (−0.059) relative to the rival's (+0.285). If the mechanism only
moves income by 6 percent in model units, the formal-rate outcome is carrying the claim — and that outcome is the one
the rival cannot express.

**G2. STEEL-MAN (my seat).** The competitive null wins if, with (a) formal/informal margin in both worlds, (b) σ
∈ {0.5, 1, 2}, (c) endogenous vacancy posting and (d) matched vacancy paths, the rival reproduces a fall in diploma
holders' formal probability. That cell has not been run; until it is, C3 is not a beat.

**H. ALTERNATIVE EXPLANATION.** Search-and-matching with endogenous vacancy posting: a supply shock can *create*
formal vacancies (more educated workers make formal hiring profitable), reversing displacement. The model has no
vacancy-posting equation.

**I. WHAT WOULD CHANGE MY MIND; LIMITS.** The matched-elasticity cell; a formal sector in the rival; the 4-rep
floor-test rerun (small-rep noise is admitted to be up to 0.07 on slopes). I could not inspect the CES calibration or
the vacancy rule.
