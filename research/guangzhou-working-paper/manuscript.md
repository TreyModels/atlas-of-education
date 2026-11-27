# Same Score, Same Chance: Procedural Equity and Positional Competition in Guangzhou's Education System

27 November 2026



James W. Menefee III

## Abstract

This paper studies how family resources relate to simulated admission outcomes in a stylized model of Guangzhou’s academic-track selection system. A 40,000-pupil synthetic cohort is evaluated across 1,024 independently sampled parameter configurations; selected analyses use separate sweeps. The model compares local-hukou pupils in the bottom and top 40% of the local wealth distribution, with thresholds for the top score and talent quintiles and the top-decile admission target calculated on the full synthetic cohort. In the independent sweep, the median rich-to-poor same-score ratio is 0.91, the joint score-and-ability ratio is 1.19, and the comparable-ability ratio is 1.41. Switching off modeled wealth-dependent post-gate channels lowers the latter by about half in a separate ablation, while residual differences are consistent with persistent earlier inputs and within-cell differences under the model. A paired scenario comparison that compares the baseline with no pre-gate tutoring restriction and no senior-2 re-banding has a median equal-talent ratio change of −0.013; this is a hypothetical model contrast, not a causal estimate of the 2021 policy. The model is not fitted to administrative pupil records, its parameter draws are not a probability sample of plausible Guangzhou states, and results are not estimates for the city. Qualitative context comes from the author’s observations and one informant; no transcript or fieldnotes are circulated. The paper contributes a transparent scenario analysis of how different fairness criteria can diverge under rank-based, capacity-constrained selection.

## 1. Argument and scope

The question is whether, among local-hukou pupils represented by this model, including those outside the academic track, a score-based allocation can yield similar outcomes for families with different resources. This is one procedural criterion, not a claim about what Guangzhou families consider fair. Admission rules vary by route and category, and this paper does not survey public views or evaluate fairness as a whole.

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

The analysis of enforcement draws on Liu et al. (2024), who report 486 parent questionnaires and 23 interviews in a Guangzhou school setting, and Liu and Bray (2025), who examine continuing hidden demand. These motivate a wealth-graded effective restriction, whose numerical coefficient remains assumed. Yang (2026) studies imperfect enforcement in a different model. Zhang (2023) provides a regulatory framework, and Bray (2024) emphasizes the timescapes of tutoring. Zhang and Bray (2018) connect tutoring access with tracking. Reardon et al. (2016) provide a precedent for simulating college sorting, while Zhou (2019) examines conditioning on credentials in a different empirical setting.

## 2. How the system works

The account below combines the author’s observations as a senior-high teacher with an informal conversation with one teacher at a private tutoring institution (informant A). These are context-setting sources, not a representative sample. Each observer has a partial view, and neither can establish prevalence or population-wide behavior.

1. **Before 15.** The model links residence, family resources and junior-school teaching. These relationships are assumptions for this application. The policy environment changed after 2021, while the model allows some pre-gate tutoring to persist. This stylized allowance is not a measure of actual prevalence; transitions into academic high school and the vocational track also shape who enters the modeled competition.
2. **The zhongkao gate.** Places are allocated by score. For 2026, Guangzhou’s rules require eligible public high schools to allocate at least 50% of their plans to junior schools and set the maximum plan share for eligible non-hukou applicants within an 8–18% range, with details depending on the category and school (Guangzhou Municipal Admissions Committee Office, 2026). The model approximates these rules rather than implementing each school’s eligibility and allocation procedure. Its sensitivity sweep samples the modeled zhibiao share from 30% to 60% and non-hukou cap from 8% to 20%, so some draws fall outside the stated 2026 rule envelope; these draws are sensitivity scenarios, not rule-compliant reconstructions.
3. **Boarding high school.** At the author’s observed school, pupils board from Sunday evening to Friday; phones go to the head teacher; homework is done in evening self-study and checked mostly for completion, though careful marking is part of what top-class teachers give. The author reports heavy weekend homework and few day pupils at that school, and pupils who want tutoring in term must ask the school for leave.
4. **Classes and re-banding.** The author and informant describe score-based class placement and advantages in top classes. Their accounts do not establish a citywide prevalence or effect size. At senior 2 classes are re-formed, often by subject combination, but a pupil who barely got in and lands in class 16 can, by working hard inside the school, reach class 1 (the informant confirmed this path).
5. **Where tutoring went.** The informant described term-time clients in two groups: pupils too weak to follow lessons and ambitious pupils targeting specific weak points. She described holiday demand for summer pre-learning of next term's content, and the winter break except about the three Spring Festival days, even in senior 3.
6. **Routes the rich buy.** Some families keep the school place but buy full-time study at an institution: about 100,000 yuan a month one-to-one, or 60,000-80,000 a semester in small classes of about 15. Others choose the art-exam route, where a modest academic score reaches a good university, or pursue eligibility for the separate joint exam under its residency and documentation requirements.

**Qualitative method and confidentiality.** Informant A is a personal contact, not a recruited or representative participant. In one Mandarin conversation on 26–27 November 2026, she reviewed a checklist of model assumptions. Her statements are used only to identify possible mechanisms and broad sensitivity ranges; her population estimates, including the uncertain denominator for full-time institutional study, are not prevalence estimates. Her identity is withheld. The scope of consent for recording, transcription, research use, and public dissemination has not been documented sufficiently for release of verbatim material. Accordingly, this working paper contains no quotations, transcript, translation, audio, or fieldnotes; none is circulated or deposited in the public archive. Any future use of identifiable or verbatim material would require explicit documented consent and appropriate ethics review. The account is limited to this anonymous, nonrepresentative conversation and the author’s own observations.

**Provenance and openness.** Tutoring participation, timing, prices, full-time study, and alternative routes are uncertain in this application. Some inputs are informed by one anonymous informant or by the author’s observations; others are literature-based or assumptions. The model therefore treats uncertain inputs as ranges rather than precise facts. Code, parameter ranges, registrations, and simulation outputs are linked in the archive; no field transcript or fieldnotes are included. A reader can substitute assumptions and inspect how model outputs change.

## 3. Measuring educational equity

We report four ratios comparing modeled admission rates for local-hukou pupils in the bottom and top 40% of the local family-wealth distribution; the middle 20% is not part of this rich-to-poor contrast. Wealth cutoffs are calculated from all local pupils, not from a score-selected subgroup. For S and T, top-quintile thresholds use the full cohort before restricting estimates to local pupils. S* uses both five-way partitions within the top score quintile; the elite outcome targets the top 10% of the full cohort, subject to cutoff ties. A ratio of 1.00 indicates equal rates under the named conditioning rule.

**Same-score ratio (one procedural standard).** Among local pupils with zhongkao scores in the cohort-wide top fifth, averaged over ten score bands:

```latex
S = \frac{1}{10}\sum_{b=1}^{10} \Pr(U=1 \mid Z \in b,\ \text{rich}) \Big/ \frac{1}{10}\sum_{b=1}^{10} \Pr(U=1 \mid Z \in b,\ \text{poor})
```

**Equal-talent ratio (a stricter standard).** The same comparison among pupils of equal latent talent, the ability a child brings before home, school and tutoring add to it. It can only be computed in a model, because talent is not observed. Formally, T is S with talent bands in place of score bands: ten equal-count bands of latent talent within the cohort-wide top fifth of talent, an unweighted average of rates across bands for each wealth group, and local-hukou pupils; wealth cutoffs use all local pupils. The simulation reports common-support diagnostics where cells are used.

**Unconditional ratio.** The plain ratio of elite-university rates, richer to poorer, with no conditioning.

**Joint diagnostic S\*.** The same comparison grouping jointly by zhongkao score and modeled starting ability, over a 5 × 5 grid of score and talent bands. Both sets of five-way bin cutoffs are computed within the cohort-wide top entrance-score quintile; the analytic population is the local-hukou pupils in the cohort-wide top score quintile, standardized to the pooled mix of supported rich/poor cells:

```latex
S^{*} = \frac{\sum_{c} n_c \Pr(U=1 \mid c,\ \text{rich})}{\sum_{c} n_c \Pr(U=1 \mid c,\ \text{poor})}, \qquad c = (\text{score band},\ \text{talent band})
```

S describes parity within entrance-score bands under one procedural criterion. We have not measured parents’ fairness judgments. But conditioning on a score that both talent and family resources produce makes richer and poorer pupils at the same score differ in talent (a collider effect), so S alone cannot say whether the system treats them alike after admission. S\* separates the two: if S is below 1 while S\* is about 1, the favourable result for poorer pupils is composition; if S\* is above 1, richer pupils do better after admission, because of post-admission mechanisms, because earlier advantages persist, or because of differences within the score-talent cells. Section 4 separates the first from the rest by ablation.

The ratios are not additive: differences between them change the populations compared, so we do not read them as shares of inequality. Section 4 attributes inequality to sources by intervening directly on the mechanisms in the model.

**Outcome and populations.** The modeled outcome is a fixed-capacity top-decile slot among the entire synthetic cohort (academic-track pupils are ranked against a target equal to 10% of the full cohort; the inclusive cutoff can exceed that target in tied inputs); it is a proxy, not an observed university admission. Real admission also depends on provincial quotas, subject combinations, preferences, and institution-level rules. The primary estimands use local-hukou pupils including those outside the academic track, with wealth cutoffs defined on the full local-hukou population:

| Outcome | Population | Reported in |
| --- | --- | --- |
| Ordinary-exam equity | Local-hukou pupils, including non-academic pupils; ordinary score ranking | Section 4 |
| All-route equity | The same pupils, with modeled art and joint-exam routes added | Sections 4 and 6 |
| System-wide access | The full synthetic cohort, including modeled vocational placement and registration status | Section 7 (descriptive only) |

## 4. Results

All reported ranges are the 5th–95th percentiles over sampled parameter settings and cohorts. They describe the selected design distribution. They are not confidence intervals for Guangzhou. The principal experiment has 1,024 independently sampled settings with 40,000 pupils each. The mechanism checks reuse its first 150 settings. A separate experiment repeats 128 independently sampled settings with eight cohort seeds each. All analyses are exploratory.

### The three equity comparisons

| Measure | Principal experiment, median (5th–95th) |
| --- | --- |
| Same-score ratio S | 0.905 (0.671 to 1.109) |
| Joint score-and-ability ratio S* | 1.186 (1.062 to 1.402) |
| Comparable-ability ratio T | 1.414 (1.155 to 1.974) |
| Joint-grid support share | 0.986 (0.922 to 1.000) |

The median ratios follow S < 1 < S* < T. These are different conditional comparisons. “Comparable” means within the stated score and ability bins; it does not mean exact matching. The simulated ability variable is unobserved in real data.

### Combined scenario and isolated restriction

The combined counterfactual removes the modeled pre-gate tutoring reduction and disables senior-2 re-banding. The isolated restriction counterfactual removes the tutoring reduction while holding re-banding on. Both use the same initial cohort seed and parameter setting; later random events can differ as paths diverge. Neither comparison identifies the causal effect of Double Reduction. Evidence that re-banding intensified after 2021 is absent.

| Quantity | Median (5th–95th) |
| --- | --- |
| T, no restriction/no re-banding | 1.424 (1.168 to 1.982) |
| T, baseline | 1.414 (1.155 to 1.974) |
| Combined change in T | -0.013 (-0.123 to 0.093) |
| Restriction-only change in T | -0.005 (-0.073 to 0.056) |
| Combined spending change, yuan | -4159.044 (-10642.380 to -336.233) |
| Route displacement, seats | 189.000 (52.000 to 421.850) |

The combined change is negative in 598 of 1,024 settings (58.4%; Wilson 95% interval 55.4%–61.4%). The restriction-only change is negative in 585 (57.1%; Wilson interval 54.1%–60.1%). These intervals describe repeated sampling from this design, rather than uncertainty about Guangzhou's population.

The spending calculation uses assumed annual unit costs. Five-year totals equal ¥15,000 × three junior years for pre-gate tutoring, ¥17,540 × two senior years for term tutoring, ¥10,000 × two senior years for holiday tutoring, plus two annual full-time fees when applicable. Each indicator is treated as sustained over that period. This is a coarse accounting proxy.

### Wealth-graded enforcement

BAN_GRAD modifies the effective reduction as clip[BAN_RED × (1 + BAN_GRAD × (1 − 2wr)), 0, 1]. The principal design varies this coefficient uniformly from 0 to 1. The following quartiles summarize its restriction-only differences while all other parameters also vary.

| BAN_GRAD range | Restriction-only change in T | T fell |
| --- | --- | --- |
| 0.00–0.25 | -0.007 (-0.084 to 0.046) | 149/245 (60.8%) |
| 0.25–0.50 | -0.008 (-0.082 to 0.050) | 163/266 (61.3%) |
| 0.50–0.75 | -0.006 (-0.061 to 0.055) | 148/250 (59.2%) |
| 0.75–1.00 | 0.001 (-0.062 to 0.066) | 125/263 (47.5%) |

A controlled sensitivity check fixes BAN_GRAD at 0, 0.5 and 1 at the same 256 settings, holding each setting’s other parameters fixed.

| Fixed BAN_GRAD | Restriction-only change in T | T fell |
| --- | --- | --- |
| 0 | -0.0077 (-0.1164 to 0.0473) | 150/256 (58.6%) |
| 0.5 | -0.0044 (-0.0833 to 0.0533) | 144/256 (56.2%) |
| 1 | 0.0009 (-0.0643 to 0.0666) | 123/256 (48.0%) |

The median becomes slightly positive at the strongest gradient. Its interval spans both directions and the share of negative changes remains close to one-half. This shows a possible sign reversal under the assumed enforcement mechanism, rather than a robust prediction that the policy raises inequality. Liu et al. (2024) and Liu and Bray (2025) motivate attention to heterogeneous access and hidden demand. Yang (2026) provides a different model of imperfect enforcement; its quantitative results are not a validation of our coefficient.

### Ordinary scores, routes and post-gate inputs

In the 150-setting mechanism sample, ordinary-score ranking yields T = 1.33, S* = 1.11 and S = 0.87, compared with 1.42, 1.19 and 0.91 under route bonuses. Fairness comparisons therefore depend on the criterion. The unconditional wealth ratio is 2.56.

Switching off post-gate tutoring, full-time instruction and both route bonuses changes median S* from 1.19 to 1.10. The median paired fraction of excess above parity removed is 50%. The residual is consistent with persistent earlier inputs and within-cell composition. This intervention does not exhaustively identify its source.

| Grid | S*, median | Supported share, median |
| --- | --- | --- |
| 5 × 5 | 1.187 | 98.4% |
| 10 × 10 | 1.195 | 91.5% |
| 20 × 20 | 1.145 | 44.6% |

The finer grids condition more precisely but retain a different and smaller population. The 5 × 5 result is primary. Under the principal experiment's two rankings, exactly 4,000 places were asserted for every sampled cohort. Gains equaled losses, every new winner held a route bonus, and no pupil received both bonuses. Real art and joint-exam systems have separate eligibility and capacities; the bonuses are approximations.

### Early-input interventions

| Intervention | T, median | Paired change in T | Excess above parity removed | Academic skill change |
| --- | --- | --- | --- | --- |
| Home gradient set to zero | 1.230 | -0.168 (-0.682 to 0.011) | 46.6% | -0.001 |
| Zone-teacher gradient set to zero | 1.302 | -0.115 (-0.298 to 0.020) | 25.7% | -0.001 |
| Pre-gate tutoring effect set to zero | 1.366 | -0.039 (-0.185 to 0.042) | 9.8% | -0.017 |
| All three | 1.094 | -0.321 (-0.884 to -0.059) | 78.1% | -0.023 |

These are distributional counterfactuals. Small changes in mean learning partly follow from the additive production function and redistribution of inputs. Costs and feasibility are unmodeled. A single persistence rate combines home, school and tutoring effects, although the literature gives reasons to expect heterogeneous persistence (Cunha & Heckman, 2007; Jacob et al., 2010).

| Share of early inputs that fades | T, median (5th–95th) |
| --- | --- |
| 0%–15% | 1.668 (1.299 to 2.151) |
| 15%–30% | 1.556 (1.254 to 2.047) |
| 30%–45% | 1.488 (1.209 to 1.840) |
| 45%–60% | 1.413 (1.155 to 1.702) |
| 60%–75% | 1.293 (1.149 to 1.552) |
| 75%–90% | 1.243 (1.100 to 1.456) |

A two-factor decomposition averages each effect over both orders of adding the restriction and re-banding. At the 150 settings, the median contributions to T are -0.006 and -0.005, respectively. Differences between medians need not equal a median paired change.

## 5. Estimands and model diagnostics

Tutoring comparisons must distinguish exposure, dose and the population whose effect is being estimated. A binary indicator for term or holiday tutoring combines two episodes, while POST_EFF is a per-episode increment. A regression coefficient on that binary indicator need not equal POST_EFF even in synthetic data. School fixed effects, class means and variance shares likewise target quantities different from an assigned school or band premium. No general estimator-failure claim is made from those comparisons.

Bray (2014) reviews the measurement and design difficulties in tutoring research. Zhang, Y. (2013), Zhang, L. (2024), and Zhang, Z., et al. (2025) use distinct populations and designs, so their estimates are not interchangeable calibrations. Manski (1993) explains difficulties with endogenous group effects. Future diagnostic work should specify a target estimand and an oracle contrast with matching units before scoring an estimator.

## 6. Four candidate specifications

We propose four model specifications for relationships the inventory lacks: provision by class, a trade-off at the school margin, tutoring demand as insurance against consequential thresholds, and admission through separate capacity-limited gates. Their novelty relative to the wider literature is not yet established; their contribution may lie mainly in combining familiar mechanisms for this institutional setting. N1 and N2 are implemented in the model in reduced form; N3 and N4 are implemented as simpler approximations, described under each.

**N1. School and class provision.** Define the initial head start h_i as the sum of junior teaching, HOME × log wealth, and PRE_EFF × the pre-gate tutoring indicator. Let u_c be the class-teacher draw, B_i1 and B_i2 the two top-band indicators, v_s the school premium and f_i the full-time institution indicator. The implemented skill equations are

```latex
K_{i,16} = (1+GROW)θ_i + (1-DECAY)h_i + v_s + u_{c1} + 0.5(TOP_TEACH+PEER)B_{i1}
K_{i,18} = K_{i,16} + (1-f_i)[u_{c2}+0.5(TOP_TEACH+PEER)B_{i2}] + POST_EFF(Term_i+Holiday_i) + f_i FT_EFF.
```

Noisy examinations are added after the relevant skill calculation. TOP_TEACH and PEER are cumulative premiums for top-band participation at both stages. Each is applied at half at each stage. Wu et al. (2019) report a final gaokao effect; the equal stage allocation is an assumption. Teacher draws are separate from these top-band premiums.

Initial school bands use zhongkao rank. When enabled, senior-2 placement uses a weighted mixture of observed senior-1 performance rank and entry rank. Each nonempty school selects max(1, round(TOP_BAND × enrollment)) pupils, capped by enrollment. The code's sort determines tie order. Park et al. (2015) and Dee and Lan (2015) inform the discussion of school effects in other settings, rather than directly estimating this model's parameters.

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

G\_i is the set of gates pupil i is eligible for, R\_{ik} the pupil's rank in gate k, and a matching rule (for example, each pupil takes the most preferred gate among those whose capacity admits them) resolves pupils who qualify through several. Eligibility for the joint exam has its own residency conditions and is not conferred by place of birth alone. The current simulation does not implement separate gates: it approximates N4 with a single ranking and an additive bonus per route. The joint-exam proxy is sampled first, and art selection excludes those pupils. The principal experiment counts displaced ordinary-score winners directly, as reported in Section 4. The model does not solve a separate-capacity matching system.

## 7. What this paper does not claim

The finding is about whether the race to the gaokao is fair for those running it; it says nothing about what the race is worth, or about those who never start it.

- **The vocational track.** The simulation does not follow vocational pupils’ subsequent education, training or employment. It cannot assess the quality of vocational provision.
- **After the gaokao.** A good university does not guarantee a job or economic security; graduate unemployment is high. Our measure stops at admission.
- **Children outside the academic track by registration.** In the model, of all non-hukou pupils in a cohort, a median 31% reach a public academic seat, 10% go private, 13% leave Guangzhou or school, and 45% go vocational. Among those who stay on the academic track the hukou gap at equal talent is modest (1.19), but exclusion at entry is large and depends on how many non-hukou children there are, which we do not know.
- **The rest of China.** Admission quotas differ by province, so opportunities depend on provincial rules and category-specific eligibility; children left behind in their home provinces never enter this system. Both are larger equity questions than anything inside Guangzhou.
- **The costs of control.** Boarding leaves pupils one day a week with their families, restricted phones and internet, and long supervised days. We document these costs; the model does not price them.
- **Whether the exam measures the right thing.** We take the gaokao as given. It rewards learning ability, memory and persistence; a top score does not mean the best problem-solver.
- **Ethnicity and gender.** The analytical population is defined by hukou, track and admission category, not by ethnicity; the model does not estimate subgroup differences by ethnicity or gender.

## 8. Data, methods and verification

The Double Reduction policy is described in the General Offices’ 2021 directive (General Office of the CCP Central Committee & General Office of the State Council, 2021). The simulation design follows the distinction between aims, data-generating mechanisms, estimands and performance measures described by Morris et al. (2019). Public data opportunities include CEPS (National Survey Research Center, 2014), CFPS (Institute of Social Science Survey, n.d.), and the 2026 local admissions documents (Guangzhou Admissions Office, 2026a, 2026b, 2026c).

Quantitative results are simulation outputs, not estimates from observed Guangzhou pupil records. The primary independent replication sweep uses 1,024 parameter draws and 40,000 synthetic pupils per draw; other analyses use separate configuration sets as noted. Parameters combine published estimates, official rule documents, a single nonrepresentative informant account, author observations, and explicit assumptions. The uniform independent draws are a sensitivity design, not an empirical probability distribution over plausible Guangzhou systems. An accompanying parameter register documents meanings, ranges, sources, and limitations.

- **Analysis design.** All results are treated as exploratory. The analysis includes independently sampled parameter settings, a 150-setting mechanism experiment reusing the principal design and repeated cohorts at fixed settings. Frequencies describe the chosen sampling design.
- **Formal checks.** The checked-in Lean 4.36 file `Admission.lean` contains generic results on capacity-balanced displacement, monotonicity under a nonnegative score bonus, strict displacement, fixed prefix cardinality, a cutoff-tie case, and a conditioning example. `proof-check.txt` records the axiom dependencies: the strict-displacement and cutoff-tie witnesses have no additional axioms; other listed results use standard Lean axioms (`propext`, `Quot.sound`, and, for one result, `Classical.choice`). These prove properties of the stated abstractions, not the full Python model. Proofs of the current simulation’s admission code, insurance demand, gate switching, and partial re-banding are not supplied.
- **Field evidence.** The informant is referred to only as informant A. The study does not establish the scope of consent or institutional ethics approval. The informal conversation provides context and does not constitute a formally approved qualitative study. No transcript, translations, audio, identifying details, or fieldnotes are included in this paper or public archive. The parameter register links model inputs to their source type without releasing field materials.
- **Archive.** Code, parameter ranges, registrations, simulation outputs, and the Lean project are associated with the Guangzhou model archive linked in the reproducibility materials. The paper and archive do not include fieldnotes or the informant transcript. The complete Atlas archive is also identified by its Atlas collection DOI.

### Repeated-cohort uncertainty

Each of 128 independently sampled settings was repeated with eight cohort seeds. For the combined change in T, pooled within-setting SD is 0.057; between-setting SD after subtracting cohort variation is 0.031. At 119 settings the change takes both signs across cohorts. For the restriction-only contrast, these SDs are 0.038 and 0.017, with sign changes at 120 settings. The setting is the unit for uncertainty about settings; eight cohorts are not eight new parameter vectors.

The computational checks verify the draw count, finite reported values, exclusive route assignment and sampled capacity/band counts. Targeted regression checks confirm that a pupil in both bands receives the full cumulative premium and that BAN_GRAD has no effect when BAN_RED=0. Lean checks the stated mathematical abstractions, not the full stochastic program.

**Further research.** Measure the head-start fade, separately for home, school and tutoring advantages, with a longitudinal survey (CEPS, CFPS) or school records; document whether performance re-banding became more common after 2021; survey tutoring among boarders and day pupils anonymously, by term and holiday; estimate the non-hukou share of the zhongkao cohort; and test the tutoring effect using the 2021 ban as a natural experiment.

The Atlas inventory includes the standard accumulation equation 20, and dynamic skill formation equations 38–39. Prior research estimates the persistence of teacher-induced gains (Jacob et al., 2010). The common fade rate in this simulation combines different sources of advantage and remains a Guangzhou-specific uncertainty.

## References

Bourdieu, P., & Passeron, J.-C. (1977). *Reproduction in education, society and culture* (R. Nice, Trans.). Sage. (Original work published 1970) https://uk.sagepub.com/en-gb/eur/reproduction-in-education-society-and-culture/book203162

Bray, M. (2007). *The shadow education system: Private tutoring and its implications for planners* (2nd ed.). UNESCO International Institute for Educational Planning. https://etico.iiep.unesco.org/sites/default/files/2017-09/118486e.pdf

Bray, M. (2014). The impact of shadow education on student academic achievement: Why the research is inconclusive and what can be done about it. *Asia Pacific Education Review, 15*(3), 381–389. https://doi.org/10.1007/s12564-014-9326-9

Bray, M. (2024). Timescapes of shadow education: Patterns and forces in the temporal features of private supplementary tutoring. *Globalisation, Societies and Education, 22*(5), 890–903. https://doi.org/10.1080/14767724.2022.2143330

Bray, M., & Lykins, C. (2012). *Shadow education: Private supplementary tutoring and its implications for policy makers in Asia.* Asian Development Bank & Comparative Education Research Centre, University of Hong Kong. https://www.adb.org/sites/default/files/publication/29777/shadow-education.pdf

Cunha, F., & Heckman, J. (2007). The technology of skill formation. *American Economic Review, 97*(2), 31–47. https://doi.org/10.1257/aer.97.2.31

Dee, T. S., & Lan, X. (2015). The achievement and course-taking effects of magnet schools: Regression-discontinuity evidence from urban China. *Economics of Education Review, 47*, 128–142. https://doi.org/10.1016/j.econedurev.2015.05.007

General Office of the Central Committee of the Communist Party of China, & General Office of the State Council. (2021, July 24). *Opinions on further reducing homework and off-campus training burdens for students in compulsory education* [Policy directive, in Chinese]. https://www.moe.gov.cn/jyb_xxgk/moe_1777/moe_1778/202107/t20210724_546576.html

Guangzhou Admissions Office. (2026a). *Notice on quota allocation for ordinary senior high schools in 2026* [In Chinese]. https://jyj.gz.gov.cn/gk/zfxxgkml/ywgz/zsks/content/post_10788402.html

Guangzhou Admissions Office. (2026b, May 12). *Results of the 2026 quota allocation lottery* [In Chinese]. https://gzzk.gz.gov.cn/zkzz/zkxx/zkzx/content/post_10809606.html

Guangzhou Admissions Office. (2026c). *Third- and fourth-batch ordinary high school admissions completed* [In Chinese]. https://gzzk.gz.gov.cn/gkmlpt/content/10/10910/post_10910997.html

Hirsch, F. (1976). *Social limits to growth.* Harvard University Press. https://www.hup.harvard.edu/books/9780674813650

Institute of Social Science Survey, Peking University. (n.d.). *China Family Panel Studies: Public-use and restricted data access guidelines.* https://www.isss.pku.edu.cn/cfps/en/data/restricted/index.htm

Jacob, B. A., Lefgren, L., & Sims, D. P. (2010). The persistence of teacher-induced learning. *Journal of Human Resources, 45*(4), 915–943. https://doi.org/10.3368/jhr.45.4.915

Lazear, E. P., & Rosen, S. (1981). Rank-order tournaments as optimum labor contracts. *Journal of Political Economy, 89*(5), 841–864. https://doi.org/10.1086/261010

Liu, D., Morgan, W. J., Zhang, X., & Wu, W. (2024). Private tutoring before and after the “double-reduction” policy in China: Choices and rationale. *SAGE Open, 14*(2), 1–14. https://doi.org/10.1177/21582440241255864

Liu, J., & Bray, M. (2025). Parental heuristics and demand for private tutoring: Continuities amidst changes brought by China’s double-reduction policy. *International Journal of Educational Development, 119*, Article 103451. https://doi.org/10.1016/j.ijedudev.2025.103451

Manski, C. F. (1993). Identification of endogenous social effects: The reflection problem. *The Review of Economic Studies, 60*(3), 531–542. https://doi.org/10.2307/2298123

Morris, T. P., White, I. R., & Crowther, M. J. (2019). Using simulation studies to evaluate statistical methods. *Statistics in Medicine, 38*(11), 2074–2102. https://doi.org/10.1002/sim.8086

National Survey Research Center, Renmin University of China. (2014). *China Education Panel Survey: Baseline parent questionnaire, 2013–2014.* https://ceps.ruc.edu.cn/Enlish/dfiles/11184/14391214047032.pdf

Park, A., Shi, X., Hsieh, C.-T., & An, X. (2015). Magnet high schools and academic performance in China: A regression discontinuity design. *Journal of Comparative Economics, 43*(4), 825–843. https://doi.org/10.1016/j.jce.2015.10.013

Reardon, S., Kasman, M., Klasik, D., & Baker, R. (2016). Agent-based simulation models of the college sorting process. *Journal of Artificial Societies and Social Simulation, 19*(1), Article 8. https://doi.org/10.18564/jasss.2993

Roemer, J. E. (1998). *Equality of opportunity.* Harvard University Press. https://doi.org/10.4159/9780674042872

Wang, F. (2020, November 26). Students retain school enrollment while training providers offer full-time schooling [In Chinese]. *Xinhua.* https://www.xinhuanet.com/politics/2020-11/26/c_1126790587.htm

Wei, Y. (2024). Short-term effects of burden-reduction policy: Evidence from the China household survey of education finance [In Chinese]. *China Education Finance* (No. 11, cumulative No. 255). Peking University. https://ciefr.pku.edu.cn/docs/2024-12/bcd3767a1681440c99e79c5c9e94fcd0.pdf

Wu, J., Wei, X., Zhang, H., & Zhou, X. (2019). Elite schools, magnet classes, and academic performances: Regression-discontinuity evidence from China. *China Economic Review, 55*, 143–167. https://doi.org/10.1016/j.chieco.2019.03.004

Yang, Z. (2026). Regulating private tutoring: Human capital formation, inequality, and intergenerational mobility. *Economies, 14*(9), Article 415. https://doi.org/10.3390/economies14090415

Zhang, L. (2024). Can private tutoring improve academic performance? A meta-analysis based on 21 empirical studies. *Frontiers of Education in China, 19*(3), 335–353. https://doi.org/10.3868/s110-010-024-0018-8

Zhang, W. (2023). *Taming the wild horse of shadow education: The global expansion of private tutoring and regulatory responses.* Routledge. https://www.routledge.com/Taming-the-Wild-Horse-of-Shadow-Education-The-Global-Expansion-of-Private/Zhang/p/book/9781032331553

Zhang, W., & Bray, M. (2018). Equalising schooling, unequalising private supplementary tutoring: Access and tracking through shadow education in China. *Oxford Review of Education, 44*(2), 221–238. https://doi.org/10.1080/03054985.2017.1389710

Zhang, W., & Bray, M. (2021). A changing environment of urban education: Historical and spatial analysis of private supplementary tutoring in China. *Environment and Urbanization, 33*(1), 43–62. https://doi.org/10.1177/0956247820981820

Zhang, Y. (2013). Does private tutoring improve students’ National College Entrance Exam performance? A case study from Jinan, China. *Economics of Education Review, 32*, 1–28. https://doi.org/10.1016/j.econedurev.2012.09.008

Zhang, Z., An, N., & Chen, J. (2025). More is worse: The impact of private supplementary tutoring on middle school students’ academic achievement. *Applied Economics, 57*(1), 106–119. https://doi.org/10.1080/00036846.2024.2386843

Zhou, X. (2019). Equalization or selection? Reassessing the “meritocratic power” of a college degree in intergenerational income mobility. *American Sociological Review, 84*(3), 459–485. https://doi.org/10.1177/0003122419844992

## Authoring and contributions

AI assistants helped draft text, code, figures and formal proofs. Computational checks and the scope of Lean verification are reported explicitly. The author is responsible for the final argument, institutional descriptions and use of field context. 

## Contributions and corrections

This is an open working paper. Readers with Guangzhou-specific evidence, corrections to institutional descriptions, or alternative parameter estimates are invited to contribute through the Atlas of Education repository’s issue tracker or pull requests. Contributions should identify the evidence source and whether it is descriptive, administrative, or causal. Please do not submit or circulate identifiable field material about informant A.


## Global rank sensitivity and neutral-world verification

The reproducibility package reports Spearman correlations and partial rank correlations (PRCCs) for all 32 independently sampled inputs against T, S*, the combined paired change and the isolated restriction change. PRCC residualizes each input rank and outcome rank against the other 31 input ranks. The design uses 1,024 settings with one cohort per setting. TEACH_SD also determines HS_TEACH_SD. These diagnostics describe approximately monotone associations within the chosen independent uniform input distribution; they are not causal effects, variance shares or a substitute for interaction analysis. Cohort noise is present. No significance tests or empirical confidence claims are attached to the ranks.

For T, the largest absolute PRCCs are DECAY (−0.886), HOME (+0.846) and TEACH_ZONE (+0.596). For S*, DECAY (−0.807) is largest. The largest absolute PRCC for the combined paired change is 0.210; for the isolated ban contrast it is 0.128 (BAN_GRAD). The full signed table is SENSITIVITY.md and machine-readable sensitivity.csv.

The neutral-world test disables wealth–ability association, wealth segregation, wealth-related home and teacher inputs, tutoring, paid routes and non-local eligibility differences. Other school and class processes remain active but wealth is independent of them. Across 20 seeded 40,000-pupil cohorts, geometric-mean ratios are T=1.0003, S=1.0044 and S*=1.0021. The automated check evaluates mean log-ratios against a prespecified numerical tolerance of the larger of 0.03 or three Monte Carlo standard errors. It does not require every finite cohort to produce exactly 1. The premium-scaling, route-exclusivity and no-restriction checks are also automated in verify_model.py. These tests establish selected implementation properties, not empirical validity.

Families do not re-optimize a household budget after an intervention. Fixed prices, fixed take-up rules and mechanically changing scores/classes allow some downstream changes but no equilibrium substitution response. The model has no empirical moment-matching calibration or independent out-of-sample validation. Section 5 is an exploratory estimand diagnostic, not a definitive assessment of published regression methods.
