# Same Score, Same Chance: Procedural Equity and Positional Competition in Guangzhou's Education System

Working paper · Version 1.0 · 27 November 2026

James W. Menefee III

## Abstract

This paper studies how family resources relate to simulated admission outcomes in a stylized model of Guangzhou’s academic-track selection system. A 40,000-pupil synthetic cohort is evaluated across 1,024 independently sampled parameter configurations; selected analyses use separate sweeps. The model compares local-hukou pupils in the bottom and top 40% of the local wealth distribution, with thresholds for the top score and talent quintiles and the fixed top-decile admission capacity calculated on the full synthetic cohort. In the independent sweep, the median rich-to-poor same-score ratio is 0.91 and the joint score-and-talent ratio is 1.19. Switching off modeled wealth-dependent post-gate channels lowers the latter by about half in a separate ablation, while residual differences are consistent with persistent earlier inputs and within-cell differences under the model. A paired scenario comparison that jointly removes the modeled pre-gate tutoring restriction and senior-2 re-banding has a median equal-talent ratio change of −0.05; this is a hypothetical model contrast, not a causal estimate of the 2021 policy. The model is not fitted to administrative pupil records, its parameter draws are not a probability sample of plausible Guangzhou states, and results are not estimates for the city. Qualitative context comes from the author’s observations and one informant; no transcript or fieldnotes are circulated. The paper contributes a transparent scenario analysis of how different fairness criteria can diverge under rank-based, capacity-constrained selection.

## 1. Argument and scope

The question is whether, among local-hukou pupils in the academic track represented by this model, a score-based allocation can yield similar outcomes for families with different resources. This is one procedural criterion, not a claim about what Guangzhou families consider fair. Admission rules vary by route and category, and this paper does not survey public views or evaluate fairness as a whole.

The institutional account considered here combines boarding, supervised study time, class placement, and regulation of tutoring. National survey evidence records a decline in reported off-campus academic tutoring between 2017 and 2023, including declines before and after the 2021 “double reduction” policy; this descriptive trend alone does not identify the policy’s causal effect (Wei, 2024).

The model allows family resources to affect pre-gate inputs, post-gate tutoring, and modeled alternative routes. One informant described additional tutoring arrangements, but this account is not a population estimate. The principal equity ratios concern local-hukou pupils, including those outside the academic track; non-hukou access, vocational placement, and other provinces are outside the primary analysis (Section 7).

The methodological contribution is a simulation-based diagnostic: it examines how common education estimators behave under stylized sorting at school, class, and tutoring levels, then sets out four candidate specifications. It does not establish that these specifications are novel in the broader literature.

## Related literature

The analysis draws on work on shadow education, positional competition, skill formation, endogenous social effects, and equality of opportunity. These literatures motivate mechanisms and measurement choices; the present paper does not provide a comprehensive review.

- **Shadow education.** Bray’s work on private supplementary tutoring (Bray, 2007; Bray & Lykins, 2012) treats tutoring as a mirror of schooling whose scale and form follow institutional design. The model treats regulation, boarding, and time constraints as channels that may reshape tutoring supply and demand (Bray & Lykins, 2012; Zhang & Bray, 2021).
- **Positional goods and tournaments.** Hirsch (*Social Limits to Growth*, 1976) argued that goods whose value depends on relative position cannot be spread by growth; Lazear and Rosen (1981) modelled rank-order tournaments in which prizes are fixed and effort is set by rank. With fixed seats and admission by rank, tutoring is a positional good and a tournament input, which motivates N3 (Hirsch, 1976; Lazear & Rosen, 1981). The tournament literature also separates private from social returns: tutoring can raise a pupil's admission chance, add to learning, and consume resources in a contest for fixed seats all at once, so its welfare effect is not settled by spending figures alone.
- **Skill formation.** Cunha and Heckman (2007) and related work model skills as built dynamically, with early inputs that persist and raise later productivity. The head-start fade parameter here is a crude version of that persistence, and our main empirical gap (Cunha & Heckman, 2007).
- **Social effects.** Manski (1993) showed why peer and group effects are hard to identify when groups are formed endogenously. Banding by score is an extreme case, which motivates caution in interpreting Equations 36 and 79 (Manski, 1993).
- **Equality of opportunity.** Roemer (1998) separates inequality due to circumstances from inequality due to effort. Our equal-talent ratio treats family wealth and neighbourhood as circumstances; the same-score ratio, by conditioning on a score shaped by circumstances, can show parity while circumstances still matter, which S\* makes visible. Equal latent talent is one particular standard of opportunity; Roemer's framework requires normative choices about which circumstances people are held responsible for, which we do not make here. Bourdieu and Passeron’s (1977) account of how schooling converts family advantage into apparently merit-based credentials is the sociological counterpart.

## 2. How the system works

The account below combines the author’s observations as a senior-high teacher with an informal conversation with one teacher at a private tutoring institution (informant A). These are context-setting sources, not a representative sample. Each observer has a partial view, and neither can establish prevalence or population-wide behavior.

1. **Before 15.** Primary and junior schools are assigned by residence; teacher quality follows neighbourhood. The policy environment changed after 2021, while the model allows some pre-gate tutoring to persist. This stylized allowance is not a measure of actual prevalence; transitions into academic high school and the vocational track also shape who enters the modeled competition.
2. **The zhongkao gate.** Places are allocated by score. For 2026, Guangzhou’s rules require eligible public high schools to allocate at least 50% of their plans to junior schools and set the maximum plan share for eligible non-hukou applicants within an 8–18% range, with details depending on the category and school (Guangzhou Municipal Admissions Committee Office, 2026). The model approximates these rules rather than implementing each school’s eligibility and allocation procedure. Its sensitivity sweep samples the modeled zhibiao share from 30% to 60% and non-hukou cap from 8% to 20%, so some draws fall outside the stated 2026 rule envelope; these draws are sensitivity scenarios, not rule-compliant reconstructions.
3. **Boarding high school.** Pupils board from Sunday evening to Friday; phones go to the head teacher; homework is done in evening self-study and checked mostly for completion, though careful marking is part of what top-class teachers give. Every subject sets heavy weekend homework. Day pupils are rare, and pupils who want tutoring in term must ask the school for leave.
4. **Classes and re-banding.** Classes are banded by score; the top classes get the most experienced teachers and a stronger study atmosphere. At senior 2 classes are re-formed, often by subject combination, but a pupil who barely got in and lands in class 16 can, by working hard inside the school, reach class 1 (the informant confirmed this path).
5. **Where tutoring went.** In term, weekend tutoring is used by two groups: pupils too weak to follow lessons and ambitious pupils targeting specific weak points. In holidays it is widespread: summer pre-learning of next term's content, and the winter break except about the three Spring Festival days, even in senior 3.
6. **Routes the rich buy.** Some families keep the school place but buy full-time study at an institution: about 100,000 yuan a month one-to-one, or 60,000-80,000 a semester in small classes of about 15. Others choose the art-exam route, where a modest academic score reaches a good university, or pursue eligibility for the separate joint exam under its residency and documentation requirements.

**Qualitative method and confidentiality.** Informant A is a personal contact, not a recruited or representative participant. In one Mandarin conversation on 26–27 November 2026, she reviewed a checklist of model assumptions. Her statements are used only to identify possible mechanisms and broad sensitivity ranges; her population estimates, including the uncertain denominator for full-time institutional study, are not prevalence estimates. Her identity is withheld. The scope of consent for recording, transcription, research use, and public dissemination has not been documented sufficiently for release of verbatim material. Accordingly, this working paper contains no quotations, transcript, translation, audio, or fieldnotes; none is circulated or deposited in the public archive. Any future use of identifiable or verbatim material would require explicit documented consent and appropriate ethics review. The account is limited to this anonymous, nonrepresentative conversation and the author’s own observations.

**Provenance and openness.** Tutoring participation, timing, prices, full-time study, and alternative routes are uncertain in this application. Some inputs are informed by one anonymous informant or by the author’s observations; others are literature-based or assumptions. The model therefore treats uncertain inputs as ranges rather than precise facts. Code, parameter ranges, registrations, and simulation outputs are linked in the archive; no field transcript or fieldnotes are included. A reader can substitute assumptions and inspect how model outputs change.

**The starting hypothesis and what happened to it.** The work began from the author's comparison with Cambodia, where teachers withhold part of the curriculum and sell it back as private lessons. The hypothesis was that Guangzhou does the opposite: the state pushes the hours a pupil needs onto school teachers, through boarding, evening self-study and heavy weekend homework, so that the private market has little left to sell. The field evidence supports this for term time (boarders' weekends go to school homework, and term-time tutoring is limited to the weakest and the most ambitious) but shows the private market is larger than the hypothesis allowed. It moved into the holidays, and at the top of the wealth distribution it takes a form the author had not anticipated: pupils who keep their registration at a school while studying full-time with one-to-one or small-class tutors at an institution, so that the school seat is held but not used. A Xinhua investigation documented full-time tutoring institutions and enrollment arrangements in Taiyuan (Wang, 2020). That reporting is contextual evidence from another city and does not establish the prevalence or operation of this route in Guangzhou. The simulation includes the mechanism as a scenario informed by the conversation; its local scale and school-level implications remain unverified.

## 3. Measuring educational equity

We report four ratios comparing modeled admission rates for local-hukou pupils in the bottom and top 40% of the local family-wealth distribution; the middle 20% is not part of this rich-to-poor contrast. Wealth cutoffs are calculated from all local pupils, not from a score-selected subgroup. Score and talent quintile cutoffs are calculated on the full synthetic cohort, before restricting estimates to local pupils; the elite outcome is the fixed top 10% of the full cohort. A ratio of 1.00 indicates equal rates under the named conditioning rule.

**Same-score ratio (the system's own standard).** Among local pupils with zhongkao scores in the cohort-wide top fifth, averaged over ten score bands:

```latex
S = \frac{1}{10}\sum_{b=1}^{10} \Pr(U=1 \mid Z \in b,\ \text{rich}) \Big/ \frac{1}{10}\sum_{b=1}^{10} \Pr(U=1 \mid Z \in b,\ \text{poor})
```

**Equal-talent ratio (a stricter standard).** The same comparison among pupils of equal latent talent, the ability a child brings before home, school and tutoring add to it. It can only be computed in a model, because talent is not observed. Formally, T is S with talent bands in place of score bands: ten equal-count bands of latent talent within the cohort-wide top fifth of talent, an unweighted average of rates across bands for each wealth group, and local-hukou pupils; wealth cutoffs use all local pupils. The simulation reports common-support diagnostics where cells are used.

**Unconditional ratio.** The plain ratio of elite-university rates, richer to poorer, with no conditioning.

**Joint diagnostic S\*.** The same comparison holding both the zhongkao score and latent talent fixed, over a 5 × 5 grid of score and talent bands. Score and talent quintile cutoffs are cohort-wide; the analytic population is the local-hukou pupils in the cohort-wide top score quintile, standardized to the pooled mix of supported rich/poor cells:

```latex
S^{*} = \frac{\sum_{c} n_c \Pr(U=1 \mid c,\ \text{rich})}{\sum_{c} n_c \Pr(U=1 \mid c,\ \text{poor})}, \qquad c = (\text{score band},\ \text{talent band})
```

S is a legitimate description of procedural equity: it is what a parent sees. But conditioning on a score that both talent and family resources produce makes richer and poorer pupils at the same score differ in talent (a collider effect), so S alone cannot say whether the system treats them alike after admission. S\* separates the two: if S is below 1 while S\* is about 1, the favourable result for poorer pupils is composition; if S\* is above 1, richer pupils do better after admission, because of post-admission mechanisms, because earlier advantages persist, or because of differences within the score-talent cells. Section 4 separates the first from the rest by ablation.

The ratios are not additive: differences between them change the populations compared, so we do not read them as shares of inequality. Section 4 attributes inequality to sources by intervening directly on the mechanisms in the model.

**Outcome and populations.** The modeled outcome is a fixed-capacity top-decile slot among the entire synthetic cohort (academic-track pupils are ranked for exactly 10% of all cohort seats); it is a proxy, not an observed university admission. Real admission also depends on provincial quotas, subject combinations, preferences, and institution-level rules. The primary estimands use local-hukou pupils including those outside the academic track, with wealth cutoffs defined on the full local-hukou population:

| Outcome | Population | Reported in |
| --- | --- | --- |
| Ordinary-exam equity | Local-hukou pupils, including non-academic pupils; ordinary score ranking | Section 4 |
| All-route equity | The same pupils, with modeled art and joint-exam routes added | Sections 4 and 6 |
| System-wide access | The full synthetic cohort, including modeled vocational placement and registration status | Section 7 (descriptive only) |

## 4. Results: what the system does, and what produces the gaps

The paired scenarios differ in both modeled pre-gate tutoring restrictions and senior-2 re-banding; the contrast is hypothetical and cannot identify the causal effect of either the 2021 policy or historical changes in Guangzhou. Equal-score comparisons coexist with residual modeled wealth gradients at equal score and talent. Levels are medians across configurations with 5th-95th percentile ranges; changes are medians of paired differences within the same configuration, which need not equal the difference between the medians of levels. Spending is cumulative per pupil over junior 1-3 and senior 1-2. These describe the model under its parameter ranges, not confidence intervals for Guangzhou.

**Hypothetical paired scenario contrast.** The comparison labeled “before” keeps boarding, holiday tutoring, and alternative routes, but jointly sets the modeled pre-gate tutoring reduction and senior-2 re-banding to zero (150 configurations in this analysis). It is not an observed pre-2021 cohort and does not isolate either mechanism. Whether performance re-banding became more common after 2021 is undocumented. The table below summarizes this separate 150-configuration analysis; the 1,024-draw independent replication sweep is reported separately in Section 8 and uses a different set of parameter draws.

| Measure (all routes) | Paired counterfactual | Baseline scenario | Paired difference | Lower in draws |
| --- | --- | --- | --- | --- |
| Equal-talent ratio T | 1.41 (1.17-1.92) | 1.35 (1.11-1.90) | -0.06 (-0.18 to +0.04) | 84% |
| Same-score ratio S | 0.92 (0.69-1.10) | 0.91 (0.67-1.12) | -0.01 | 64% |
| Unconditional ratio | 2.50 (1.47-4.57) | 2.34 (1.38-4.25) | -0.11 | 83% |
| Household tutoring spend (yuan) | 35,800 (23,500-46,400) | 28,800 (19,900-41,700) | -4,800 (-11,900 to -400) | 99% |

The distance of T above parity falls by about 15%. The unconditional ratio stays large: richer local pupils remain more than twice as likely as poorer ones to win a top-decile slot.

**Ordinary exam versus all routes.** On the equal-talent and joint score-and-talent standards, and unconditionally, richer families' advantage is smaller through the ordinary gaokao alone than when the art and joint-exam routes are counted: T 1.25 against 1.35, S\* 1.11 against 1.19, unconditional 2.20 against 2.34. On the same-score standard the ordinary exam departs further from parity, in poorer pupils' favour (0.85 against 0.91). Which is fairer depends on the standard.

**Same score, but not same treatment.** Holding score and talent fixed, richer pupils do better: S\* is 1.19 (1.07-1.40) on a 5 x 5 grid, 1.20 on 10 x 10 and 1.16 on 20 x 20. Common support (pupils in cells with at least five richer and five poorer pupils) covers 99%, 92% and 47% of the top fifth respectively. Switching off every wealth-dependent post-gate mechanism for the same pupils lowers S\* to 1.09 (above 1 in 94% of configurations), removing a median 49% of its excess. The rest is consistent with earlier advantage that persists under the model's assumptions (among pupils with the same score and talent, the richer reached that score with more help from home and zone schools, part of which is still there at the gaokao), with some contribution from differences within the score-talent cells. The 5 x 5 grid is the primary estimate; the finer grids are sensitivity checks.

**Two decompositions.** They answer different questions and use different baselines, so their parts do not add to the same total.

| Mechanism | Historically anchored: change in T | Historically anchored: change in spend (yuan) | Full factorial, all-off baseline: change in T | Full factorial: change in spend (yuan) |
| --- | --- | --- | --- | --- |
| Ban on pre-gate tutoring | -0.02 (-0.10 to +0.04) | -5,000 (-11,900 to -400) | -0.01 | -4,600 |
| Senior-2 re-banding | -0.04 (-0.14 to +0.04) | about 0 | -0.04 | about 0 |
| Boarding | held on | held on | -0.01 | -5,600 |
| Holidays, institutions, art and joint-exam routes | held on | held on | +0.10 | +13,600 |

The historically anchored decomposition (Shapley over two model switches, with boarding and pre-existing tutoring and routes held on) summarizes this hypothetical scenario contrast; it is not an estimate of change caused by the 2021 policy. The full factorial describes what each institution contributes to the system's operation from a baseline with none of them.

Under the model’s chosen tutoring-reduction parameter, simulated pre-gate take-up and spending fall; this is a scenario result, not a causal evaluation. A CIEFR household-survey analysis reports off-campus academic tutoring participation of 36.1% in 2017 and 13.5% in 2023, with a declining trajectory that includes years before the 2021 policy (Wei, 2024). The descriptive series therefore should not be attributed wholesale to “double reduction.” The survey and simulation also cover different populations and measures.

**Where the remaining gap comes from.** Interventions on the current system, for the same pupils. “No home advantage” gives every pupil the average home input (removing its link to wealth); “equal zone teachers” removes the link between neighbourhood wealth and junior teacher quality, keeping variation within schools; “no pre-gate tutoring effect” makes pre-gate tutoring ineffective.

| Intervention | T | Paired change | Share of excess above parity removed | Change in mean learning, academic pupils (SD) |
| --- | --- | --- | --- | --- |
| None (current) | 1.35 | - | - | - |
| No home advantage | 1.19 | -0.15 | 44% | 0.00 |
| Equal zone teachers | 1.28 | -0.07 | 22% | 0.00 |
| No pre-gate tutoring effect | 1.33 | -0.03 | 8% | -0.02 |
| All three | 1.09 | -0.24 | 74% | -0.02 |

In this model, equalizing selected pre-gate inputs removes a substantial portion of the modeled equal-talent gap with little change in mean learning, because the intervention redistributes rather than removes most inputs. This result depends on the additive production function and is not a costed or feasible policy estimate. This follows partly from the model's additive production function; with diminishing returns or interactions with existing skill, redistribution could change aggregate learning. These are distributional counterfactuals that show where an intervention might matter, not costed or feasible policies. How much of the head start survives to the gaokao depends on how fast it fades in high school, a highly influential and weakly measured model parameter:

| Share of pre-gate head start that fades by senior 2 | 0-15% | 15-30% | 30-45% | 45-60% | 60-75% | 75-90% |
| --- | --- | --- | --- | --- | --- | --- |
| Equal-talent ratio T (median, 400 configurations) | 1.55 | 1.45 | 1.44 | 1.32 | 1.25 | 1.16 |

The model treats home, school and tutoring advantages as one stock with a common fade. Tutoring may fade faster than good early teaching or home learning; separate persistence rates are the most important extension.

**What the rich routes buy.** For the richest fifth, post-gate tutoring and full-time institutions raise a pupil's own chance of a top-decile slot by a median 2.9 percentage points per 100,000 yuan (0.2-8.7). A pre-registered threshold claim that this stays under 5 points held in 72% of configurations (against an 80% criterion); we therefore report the simulated distribution without treating it as an empirical return estimate.

## 5. Which standard economic equations apply

In these simulated cohorts, common estimators sometimes fail to recover the mechanisms they are intended to measure when pupils are sorted by school, class, and tutoring take-up. We fitted equations from a 183-item inventory of the economics of education (Atlas equation inventory, numbered as there) to simulated cohorts where the generating mechanisms are known, across 300 configurations. Each row states what the estimator would be read as measuring, what it reports, and the truth.

| Eq | Estimator | Usually read as | Reports (median, 5th-95th) | Truth | Failure type |
| --- | --- | --- | --- | --- | --- |
| 74 | Tutoring on gaokao, with prior score and family controls | Effect of tutoring | -0.02 (-0.17 to 0.13) | 0.12 (0.01-0.24) | Selection into treatment: weak pupils' take-up survives the controls (understates by 0.14) |
| 74 | Same, no controls | Effect of tutoring | 0.13 (-0.08 to 0.35) | 0.12 | None on average; imprecise (within 0.05 SD in 33%) |
| 76 | Tutoring x family background | Who gains more | Significant at 5% (two-sided) in 64% of configurations, against 5% expected by chance | 0 | Selection into treatment |
| 58 | Logit of tutoring on income | Who buys tutoring | pseudo-R2 0.06 | Demand at both tails: 0.35 with rank and rank squared | Functional-form misspecification |
| 79 | Classmates' tutoring on own tutoring | Peer pressure in demand | 0.89 whatever the true value | 0-1 (rank correlation 0.19) | Endogenous grouping (classes sorted by score) |
| 36 | Linear-in-means peer effect | Peer effect | 1.9 (0.9-7.5) | not comparable: the coefficient is per SD of class-mean zhongkao score; the true peer component is a 0.05-0.25 SD top-class premium (34% of the class effect) | Quantitative recovery unresolved (units not comparable); endogenous grouping and teacher allocation bundled with peers |
| 35 | School fixed effects, elite vs regular | School quality | 2.2 SD (1.8-2.6) | 0.25 SD (0.03-0.47) | Descriptive quantity read causally: it measures intake |
| 159 | Multilevel variance split | Share due to schools | 58% between schools | about 1% is value added | Descriptive quantity read causally |
| 152 | Fuzzy RD at the elite cutoff | School quality at the margin | 0.19 (-0.41 to 0.85) | 0.25 net of any lost top-class place | Bundled treatment: school, class placement, peers and boarding together |
| 32 | Value added with zhongkao control | School quality | 0.27 (0.00-0.55) | 0.25 | Closest; imprecise |
| 34 | Teacher effects from class means | Teacher quality | correlation 0.73 with truth | - | Usable; imprecise |
| 20, 179, 117 | Skill accumulation, seat constraint, subsidy incidence | Accounting | - | - | None |

Three lessons follow. In a banded system, fixed effects and variance shares describe sorting, and the class, not the school, is where provision differs, so school-level estimands need an explicit model of class placement. Peer and demand-spillover estimates need exogenous grouping, which banding removes. And in this system the usual controlled regression understates tutoring's effect because the weakest pupils buy it; this offers one mechanism for null or negative estimates in the literature, but it does not show that published estimates arise from it, and designs with credible exogenous variation (for example the 2021 ban as a natural experiment) can identify tutoring effects.

## 6. Four new equations

We propose four model specifications for relationships the inventory lacks: provision by class, a trade-off at the school margin, tutoring demand as insurance against consequential thresholds, and admission through separate capacity-limited gates. Their novelty relative to the wider literature is not yet established; their contribution may lie mainly in combining familiar mechanisms for this institutional setting. N1 and N2 are implemented in the model in reduced form; N3 and N4 are implemented as simpler approximations, described under each.

**N1. The class is the unit of provision.** In dynamic form, achievement in year t+1 depends on talent, a fading head start, school and teacher value added, peers, tutoring and a shock, with class placement set at entry and re-decided once, at senior 2:

```latex
A_{i,t+1} = A_{it} + g_t\,\theta_i - \delta_t\, h_{it} + v_{s(i),t} + \kappa_{T,c(i,t)} + \kappa_P\, \bar A_{-i,c(i,t),t} + \tau_t T_{it} + \varepsilon_{it}
```

Placement at senior 2 uses the within-school quantile of a mix of current and entry rank, so the top band always holds the share β of each school:

```latex
B_i = \mathbf{1}\Big[\, Q_{s(i)}\big(\rho\, r_i^{16} + (1-\rho)\, r_i^{15}\big) \ge 1-\beta \Big]
```

The head start has its own transition, h\_{i,t+1} = (1 - δ\_t) h\_{it}; in the model it is reduced once, by the share φ, between entry and senior 2. Placement is decided at entry (by zhongkao rank) and once more at senior 2; senior-3 placement is assumed unchanged. Q\_s is the within-school empirical quantile; the top band takes the first round(β n\_s) pupils in that order, with ties ordered by NumPy’s sorting algorithm. The model's reduced form adds the two years: talent θ, the head start h with fade φ, school value added v, the top-class teacher and peer effects κ\_T and κ\_P, and tutoring.

**N2. The margin trade-off.** For a pupil choosing between a stronger school s' and a weaker school s, holding other channels fixed:

```latex
\Delta_i = (v_{s'} - v_s) - (\kappa_T + \kappa_P)\,\big[p_i(s) - p_i(s')\big], \qquad p_i(s) = \Pr(B_i = 1 \mid s)
```

With a 0.20 SD school advantage, a 0.44 SD top-class effect, and top-class chances of 65% in the weaker school against 15% in the stronger one, the stronger school is worth -0.02 SD to that pupil. A regression discontinuity at an elite cutoff estimates the whole admission bundle (school, class placement, peers, boarding, travel), of which N2 is one component.

**N3. Tutoring demand as positional insurance.** Let a family face consequential thresholds c\_k (for example an undergraduate line and an elite line), each with a loss L\_k if the child falls below it, and an uncertain score Y = μ\_i + τT + ε with ε \~ N(0, σ²). Facing price p and a budget, it chooses tutoring T to minimise expected loss plus cost:

```latex
\min_{0 \le T \le \min(W_j,\; y_i/p)} \; pT + \sum_k L_k\, \Phi\!\Big(\frac{c_k - \mu_i - \tau T}{\sigma}\Big) \quad\Rightarrow\quad p = \frac{\tau}{\sigma}\sum_k L_k\, \phi\!\Big(\frac{c_k - \mu_i - \tau T^{*}}{\sigma}\Big)
```

The printed condition holds at an interior stationary point, but the objective is not globally convex: with z\_k = (c\_k - μ\_i - τT)/σ, its second derivative is -(τ²/σ²) Σ\_k L\_k z\_k φ(z\_k), which changes sign. The optimum therefore compares every interior minimum with the boundaries T = 0 and T = min(W\_j, y\_i/p). The model predicts the largest marginal returns to tutoring for pupils whose expected score lies near a consequential threshold, subject to price, uncertainty, time windows and budget; whether that coincides with the tails of a class depends on how classes are formed relative to the thresholds. W\_j is the hours available in time window j (term weekend, holiday) and y\_i/p the budget; larger losses for falling below the family's own position raise L\_k for richer families. Because seats are fixed and admission is by rank, a gain every family buys changes no one's rank: the spending is defence, though pupils may still learn more. The thresholds are taken as given here; in a fixed-seat contest they are set jointly by all families' investments, which a full equilibrium version would solve. The simulation uses a behavioural approximation (take-up rising at the tails of the class, with the gap between wealth rank and achievement rank, and with one round of classmates' lagged take-up) and applies a budget constraint only to the full-time route.

**N4. Gate switching with separate capacities.** Each gate k (ordinary gaokao, art track, joint exam for Hong Kong, Macau and Taiwan residents) has its own eligibility, ranking and capacity Q\_k:

```latex
U_{ik} \in \{0,1\}, \quad U_{ik} = 1 \Rightarrow \big(k \in G_i \ \text{and}\ R_{ik} \le Q_k\big), \qquad \sum_k U_{ik} \le 1, \qquad \sum_i U_{ik} \le Q_k, \qquad U_i = \sum_k U_{ik}
```

G\_i is the set of gates pupil i is eligible for, R\_{ik} the pupil's rank in gate k, and a matching rule (for example, each pupil takes the most preferred gate among those whose capacity admits them) resolves pupils who qualify through several. Eligibility for the joint exam has its own residency conditions and is not conferred by place of birth alone. The current simulation does not implement separate gates: it approximates N4 with a single ranking and an additive bonus per route. In that approximation the art and joint-exam routes take a median 10% of top-decile slots (3-19%, depending on their assumed size) and add a median paired 0.07 to the equal-talent ratio (300 configurations of v5.1, same pupils with and without the routes); these figures should be read as properties of the approximation. The 0.10 gap between the all-route and ordinary-exam medians in Section 4 comes from a different run and also reflects the reallocation of seats, so it is not the same quantity.

## 7. What this paper does not claim

The finding is about whether the race to the gaokao is fair for those running it; it says nothing about what the race is worth, or about those who never start it.

- **The vocational track.** Roughly 35-50% of each Guangzhou cohort goes to vocational schools, and the author's view, from observation rather than from this study's evidence, is that most of them receive a poor education; this paper offers no defence of it and does not evaluate it. Vocational education matched to labour markets is not a solved problem anywhere, and this paper does not address it.
- **After the gaokao.** A good university does not guarantee a job or economic security; graduate unemployment is high. Our measure stops at admission.
- **Children outside the academic track by registration.** In the model, of all non-hukou pupils in a cohort, a median 31% reach a public academic seat, 10% go private, 13% leave Guangzhou or school, and 45% go vocational. Among those who stay on the academic track the hukou gap at equal talent is modest (1.19), but exclusion at entry is large and depends on how many non-hukou children there are, which we do not know.
- **The rest of China.** Admission quotas differ by province, so a Beijing pupil reaches top universities far more easily than a pupil elsewhere; children left behind in their home provinces never enter this system. Both are larger equity questions than anything inside Guangzhou.
- **The costs of control.** Boarding leaves pupils one day a week with their families, restricted phones and internet, and long supervised days. We document these costs; the model does not price them.
- **Whether the exam measures the right thing.** We take the gaokao as given. It rewards learning ability, memory and persistence; a top score does not mean the best problem-solver.
- **Ethnicity and gender.** The analytical population is defined by hukou, track and admission category, not by ethnicity; the model does not estimate subgroup differences by ethnicity or gender.

## 8. Data, methods and verification

Quantitative results are simulation outputs, not estimates from observed Guangzhou pupil records. The primary independent replication sweep uses 1,024 parameter draws and 40,000 synthetic pupils per draw; other analyses use separate configuration sets as noted. Parameters combine published estimates, official rule documents, a single nonrepresentative informant account, author observations, and explicit assumptions. The uniform independent draws are a sensitivity design, not an empirical probability distribution over plausible Guangzhou systems. An accompanying parameter register documents meanings, ranges, sources, and limitations.

- **Pre-registration.** Every sweep's claims and thresholds were written and hashed before running. Of the claims behind this paper: same score, same chance was supported (93.5% against an 80% bar); the claim that rich routes yield under 5 admission points per 100,000 yuan fell short (72% against 80%), so Section 4 reports the size rather than the claim; a comparison with a stylised Hong Kong was pre-registered and not supported, and is not pursued here. The joint diagnostic S\* and the factorial decomposition were added after an external review and pre-registered before running, without pass/fail thresholds. Earlier claims that failed, including that zone teachers carry most of the remaining gap, are recorded in the archive.
- **Corrections.** A bug that let top classes grow beyond their fixed share was found on 27 November and fixed; affected results were rerun and the equation verdicts did not change.
- **Formal checks.** The checked-in Lean 4.36 file `Admission.lean` contains generic results on capacity-balanced displacement, monotonicity under a nonnegative score bonus, strict displacement, fixed prefix cardinality, a cutoff-tie case, and a conditioning example. `proof-check.txt` records the axiom dependencies: the strict-displacement and cutoff-tie witnesses have no additional axioms; other listed results use standard Lean axioms (`propext`, `Quot.sound`, and, for one result, `Classical.choice`). These prove properties of the stated abstractions, not the full Python model. Proofs of the current simulation’s admission code, insurance demand, gate switching, and partial re-banding are not supplied.
- **Field evidence.** The informant is referred to only as informant A. The scope of consent for recording, transcription, research use, and public archiving is not documented for circulation. No transcript, translations, audio, identifying details, or fieldnotes are included in this paper or public archive. The parameter register links model inputs to their source type without releasing field materials.
- **Archive.** Code, parameter ranges, registrations, simulation outputs, and the Lean project are associated with the Guangzhou model archive (TreyModels, 2026a). The paper and archive do not include fieldnotes or the informant transcript. The complete Atlas archive is also identified by its DOI (TreyModels, 2026b).

### Replication summary and formal checks

The checked-in `outputs/replication/summarize.py` summarizes 1,024 rows generated by `sweep.py`; every row contains 40,000 synthetic pupils and one independently sampled parameter vector. Values below are the 5th, 50th (median), and 95th percentiles across parameter draws, not confidence intervals. The reported `T` and `S` compare bottom-40% and top-40% local wealth groups, conditional on cohort-wide top-quintile talent and score bands, respectively. `S*` uses supported cells on a cohort-wide top-score-quintile population. The model’s `uni` outcome always assigns exactly 10% of the full cohort a slot.

| Quantity from independent sweep | 5th percentile | Median | 95th percentile |
| --- | ---: | ---: | ---: |
| Equal-talent ratio, paired scenario (`T_before`) | 1.164 | 1.410 | 1.952 |
| Equal-talent ratio, baseline (`T`) | 1.124 | 1.363 | 1.897 |
| Same-score ratio (`S`) | 0.667 | 0.908 | 1.114 |
| Joint score-talent ratio (`S*`) | 1.064 | 1.190 | 1.424 |
| Common-support share for `S*` | 0.925 | 0.986 | 1.000 |
| Paired tutoring-spend proxy change, yuan per pupil | −12,424 | −5,069 | −405 |
| Paired equal-talent ratio change (`T − T_before`) | −0.188 | −0.051 | +0.052 |

The paired comparison in this sweep jointly sets `BAN_RED=0` and `REBAND=False` in the counterfactual; its median `T` reduction occurs in 807 of 1,024 draws (78.8%; Wilson 95% interval 76.2%–81.2%). The tutoring-spend difference is a modeled proxy based on fixed cost assumptions and take-up indicators. It cannot isolate the ban from re-banding, establish what happened historically, or estimate actual household spending. Alternative-route displacement is capacity-balanced in code; its median is 187 cohort pupils per 40,000 (5th–95th: 53–418), and each entrant displaces one ordinary-score entrant.

The replication code also asserts that the top-band headcount equals the configured rounded target in both band assignments. The Lean file `Admission.lean` contains generic lemmas and witnesses for capacity-balanced displacement, monotonicity under a nonnegative score bonus, strict displacement, fixed prefix cardinality, a cutoff-tie case, and a conditioning example. `proof-check.txt` records the printed axiom dependencies: the strict-displacement and cutoff-tie witnesses have no additional axioms; the other listed theorems use standard Lean axioms (`propext`, `Quot.sound`, and in one theorem `Classical.choice`). These are mathematical checks of stated abstractions, not verification of the full Python simulation or current admission implementation. In particular, the cutoff-tie witness shows that an inclusive threshold can admit more tied applicants than available seats, so fixed-capacity allocation needs an explicit tie rule. The simulation relies on NumPy sorting for rank order; the code does not define a substantively justified institutional tie-break, and the proof does not validate tie behavior in the simulation. The sweep asserts the configured top-band headcount, including its rounded target, for both band assignments.

**Version reconciliation.** Headline numbers moved as the model gained mechanisms and as evidence corrected assumptions. The equal-talent ratio for the current cohort, by version:

| Version | What changed | Evidence for the change | Equal-talent ratio now (before) |
| --- | --- | --- | --- |
| Talent model | Talent separated from skill; full performance re-banding; school value added 0.1 SD | Dossier review of Chinese school and class effects | 1.29 (1.91 for a \~2015 cohort without re-banding or boarding) |
| v3 | Teachers, classes, zhibiao, hukou; school value added 0-0.2 SD | Dossier teacher-effect and admission studies | 1.16 |
| v3.1 | Admission rules matched to 2026 regulations; school value added widened to 0-0.5 SD | Official rules; first external review | 1.18 |
| v4 | Pre-gate tutoring persists; holiday tutoring; partial re-banding; full-time institutions | Informant A | 1.31 (superseded: band-size bug) |
| v5-v7 | Insurance demand; art and joint-exam routes; bug fixed; counterfactual keeps boarding | Informant A; second external review | 1.35 (1.41) |

The model freeze is v5.1 (`gz_v5.py`, including the band-size correction); this manuscript is Working Paper Version 1.0, 27 November 2026. The release record is linked to the model archive tag (TreyModels, 2026a). The parameter register gives each parameter’s definition, range, sampling design, source type, evidentiary status, and model version. A tag and the larger Atlas archive DOI identify different levels of the archive (TreyModels, 2026a, 2026b).

**Next steps.** The model version is frozen for this working-paper release; further work should be empirical. Measure the head-start fade, separately for home, school and tutoring advantages, with a longitudinal survey (CEPS, CFPS) or school records; document whether performance re-banding became more common after 2021; survey tutoring among boarders and day pupils anonymously, by term and holiday; estimate the non-hukou share of the zhongkao cohort; and test the tutoring effect using the 2021 ban as a natural experiment.

The Atlas inventory includes the standard accumulation equation 20, and dynamic skill formation equations 38–39. Prior research estimates the persistence of teacher-induced gains (Jacob et al., 2010). The common fade rate in this simulation combines different sources of advantage and remains a Guangzhou-specific uncertainty.

## References

Bourdieu, P., & Passeron, J.-C. (1977). *Reproduction in education, society and culture*. Sage.

Bray, M. (2007). *The shadow education system: Private tutoring and its implications for planners* (2nd ed.). UNESCO International Institute for Educational Planning.

Bray, M. (2014). The impact of shadow education on student academic achievement: Why the research is inconclusive and what can be done about it. *Asia Pacific Education Review, 15*(3), 381–389. https://doi.org/10.1007/s12564-014-9326-9

Bray, M., & Lykins, C. (2012). *Shadow education: Private supplementary tutoring and its implications for policy makers in Asia*. Asian Development Bank.

Cunha, F., & Heckman, J. (2007). The technology of skill formation. *American Economic Review, 97*(2), 31–47. https://doi.org/10.1257/aer.97.2.31

Guangzhou Municipal Admissions Committee Office. (2026, July 21). *2026年广州市中考第三批次和第四批次普通高中录取顺利结束* [Third- and fourth-batch high-school admissions concluded for Guangzhou’s 2026 zhongkao]. https://gzzk.gz.gov.cn/gkmlpt/content/10/10910/post_10910997.html

Hirsch, F. (1976). *Social limits to growth*. Harvard University Press.

Jacob, B. A., Lefgren, L., & Sims, D. P. (2010). The persistence of teacher-induced learning. *Journal of Human Resources, 45*(4), 915–943. https://doi.org/10.3368/jhr.45.4.915

Lazear, E. P., & Rosen, S. (1981). Rank-order tournaments as optimum labor contracts. *Journal of Political Economy, 89*(5), 841–864. https://doi.org/10.1086/261010

Manski, C. F. (1993). Identification of endogenous social effects: The reflection problem. *Review of Economic Studies, 60*(3), 531–542. https://doi.org/10.2307/2298123

Roemer, J. E. (1998). *Equality of opportunity*. Harvard University Press.

TreyModels. (2026a). *Atlas of education: Guangzhou sorting model v5.1* [Code, parameter ranges, registrations, simulation outputs, and formal-check project]. GitHub release tag `v2026.11.27-guangzhou`. https://github.com/TreyModels/atlas-of-education/releases/tag/v2026.11.27-guangzhou

TreyModels. (2026b). *Atlas of education* [Research archive]. Zenodo. https://doi.org/10.5281/zenodo.24369167

Wang, F. (2020, November 26). 学生空挂学籍，有的公立校名师任教……部分校外培训机构违规办“全日制”学校 [Students retain nominal school enrollment while attending full-time tutoring institutions]. *Xinhua News*. https://www.xinhuanet.com/politics/2020-11/26/c_1126790587.htm

Wei, Y. (2024). 减负政策的短期效果评估：基于中国教育财政家庭调查的分析 [Short-term evaluation of the burden-reduction policy: An analysis based on the China Institute for Educational Finance Research Household Survey]. *中国教育财政, 2024*(11) (总第255期). https://ciefr.pku.edu.cn/docs/2024-12/bcd3767a1681440c99e79c5c9e94fcd0.pdf

Zhang, L. (2024). Can private tutoring improve academic performance? A meta-analysis based on 21 empirical studies. *Frontiers of Education in China, 19*(3), 335–353. https://doi.org/10.3868/s110-010-024-0018-8

Zhang, W., & Bray, M. (2021). A changing environment of urban education: Historical and spatial analysis of private supplementary tutoring in China. *Environment and Urbanization, 33*(1), 43–62. https://doi.org/10.1177/0956247820981820

Zhang, Y. (2013). Does private tutoring improve students’ National College Entrance Exam performance? A case study from Jinan, China. *Economics of Education Review, 32*, 1–28. https://doi.org/10.1016/j.econedurev.2012.09.008

Zhang, Z., An, N., & Chen, J. (2025). More is worse: The impact of private supplementary tutoring on middle school students’ academic achievement. *Applied Economics, 57*(1), 106–119. https://doi.org/10.1080/00036846.2024.2386843

## Contributions and corrections

This is an open working paper. Readers with Guangzhou-specific evidence, corrections to institutional descriptions, or alternative parameter estimates are invited to contribute through the Atlas of Education repository’s issue tracker or pull requests. Contributions should identify the evidence source and whether it is descriptive, administrative, or causal. Please do not submit or circulate identifiable field material about informant A.
