Second review: Same Score, Same Chance

This is a substantially stronger paper than the previous two-paper draft. Combining the shadow-education and equity arguments around a common institutional mechanism gives the research a clearer intellectual identity. The introduction of three equity measures, the revised account of tutoring behavior, and the four proposed equations address several of my earlier concerns.

The paper now has a recognizable thesis: Guangzhou operates a publicly managed positional competition in which schools control instructional resources, student time, and the allocation of opportunities after the zhongkao.

Its most interesting finding is that the system can approach procedural fairness at the point of secondary-school selection while preserving considerable inequality in the production of the scores used for selection.

There are, however, several mathematical and identification problems that I would resolve before circulating this version academically.

1. The three equity ratios are a major improvement

Simulated rich-to-poor elite-university admission ratios

1.00 represents equal admission probability under the specified conditioning.

Same zhongkao score

Before

0.91

Now

0.90

Equal latent talent

Before

1.43

Now

1.35

Unconditional

Before

2.47

Now

2.32

Source: Section 4, medians across 400 simulated configurations.

These three ratios give the paper an analytical structure capable of accommodating competing definitions of educational fairness.

Measure	What it evaluates
Same score (S)	Procedural equity after prior achievement is established
Equal talent (T)	Opportunity equity under the model’s definition of latent ability
Unconditional	Realized socioeconomic inequality in admission

This distinction could itself constitute a methodological contribution to the Atlas.

There is a mathematical problem in Section 3, however. The difference between S and T does not directly measure how much inequality enters before age 15. Conditioning on achievement changes the composition of the populations being compared. The same problem applies to interpreting the difference between T and the unconditional ratio as inequality attributable to talent.

A proper decomposition requires standardized populations and explicit counterfactual interventions on the mechanisms producing achievement. Since the simulation contains the underlying variables, you can perform those interventions directly.

I would retain all three ratios and remove the additive causal interpretation of their differences until that decomposition has been completed.

2. The same-score result may partly arise from collider bias

This is the most important statistical issue in the revised paper.

The draft explains the 0.90 same-score ratio by arguing that poorer pupils who achieve a given zhongkao score have done so with less assistance. Consequently, they possess greater underlying talent and perform better subsequently.

That is plausible within the model. It also describes a classic conditioning problem.

Conditioning on a score jointly produced by talent and wealth can induce an association between those two inputs.

Among pupils with identical scores, greater wealth-derived assistance can compensate for lower latent talent. Conditioning on the score therefore selects systematically different rich and poor pupils.

If talent continues to influence gaokao performance while earlier purchased advantages fade, the poorer pupils can outperform their wealthier counterparts.

Your simulation is particularly well suited to demonstrating this because latent talent is known.

I would introduce a fourth diagnostic:

S^* =
\frac{\Pr(U=1\mid Z,\theta,\text{rich})}
{\Pr(U=1\mid Z,\theta,\text{poor})}

Here, both zhongkao score and latent talent are held constant, with appropriate standardization across their joint distribution.

S remains a legitimate descriptive measure of procedural equity. S* would help establish whether the favorable outcomes for poorer pupils arise from institutional treatment after admission or from the composition of the selected population.

That distinction could become one of the paper’s principal findings.

3. The paper cannot yet attribute the improvement to Double Reduction

The before-and-after comparison changes several institutional mechanisms simultaneously.

Mechanism	Before	Now
Legal pre-gate tutoring	Open	Restricted
High-school boarding	Day-school baseline	Boarding
Class reassignment	Absent	Present
Tutoring market	Conventional	Holidays and institutions

The draft acknowledges that boarding expanded gradually from the 2000s. Its historical baseline is explicitly counterfactual.

The abstract nevertheless attributes the reduction in expenditure and improvement in equity to the 2021 reform.

I would run a factorial experiment separating four mechanisms:

* Restrictions on pre-gate tutoring.
* Boarding and time constraints.
* Senior 2 re-banding.
* Substitution into holidays, institutions, and alternative admission routes.

A full binary factorial design requires only 16 institutional configurations for each parameter draw. Shapley decomposition could then allocate the combined change in expenditure and equity across mechanisms while accounting for their interactions.

This would establish how much of the simulated improvement comes from Double Reduction itself.

It would also allow the historical counterfactual to retain boarding and re-banding wherever they existed before 2021.

4. The magnitude of the reform

The revised estimates are considerably more restrained than those in the earlier draft.

Mean tutoring expenditure

−26.4%

¥40,500 → ¥29,800

Pre-gate tutoring participation

−13 pp

40% → 27%

Equal-talent excess inequality

−18.6%

0.43 → 0.35 above parity

Unconditional admission ratio

2.32×

Previously 2.47×

Calculated from the reported simulation medians. These are model comparisons rather than observed policy effects.

The equal-talent excess-inequality calculation is worth reporting. Moving from 1.43 to 1.35 represents an 18.6% reduction in the distance above parity, which conveys the substantive magnitude more clearly than the raw ratio change.

The unconditional ratio of 2.32 also deserves greater prominence. Even under the current institutional configuration, wealth remains strongly associated with access to elite universities.

Specify the expenditure period throughout. It is unclear whether ¥29,800 represents annual expenditure, cumulative expenditure before the zhongkao, or expenditure over the entire modeled educational trajectory.

5. The four new equations

These are the most intellectually ambitious part of the paper. They differ considerably in their readiness for publication.

N1. Classroom-level educational production

The proposed production function is sensible:

A_i^{18}=(1+g)\theta_i+(1-\phi)h_i
+v_{s(i)}+(\kappa_T+\kappa_P)B_i

It incorporates school value added, the persistence of prior advantage, and classroom-specific provision.

My concern is that the equation, as printed, omits tutoring despite tutoring being central to the paper. It also compresses three years of educational production into a terminal equation, making it difficult to represent the cumulative effects of class placement before and after re-banding.

I would introduce a dynamic version:

A_{i,t+1}=A_{it}+g_t\theta_i-\delta_t h_{it}
+v_{s(i),t}+\kappa_{T,it}
+\kappa_P\overline A_{-i,c,t}
+\tau_tT_{it}+\varepsilon_{it}

This permits classroom assignment to influence achievement before the next assignment decision. It also makes teacher effects, peer effects, tutoring, and unexplained achievement shocks separately identifiable within the simulation.

The printed N1 can remain as a reduced-form representation.

One further issue: the weighted combination of entry rank and current rank need not itself have a uniform distribution. Applying a threshold of to that combination can produce a top band containing something other than the intended proportion .

Given the corrected top-class capacity bug, the printed equation should explicitly use the within-school quantile of the combined ranking statistic.

N2. The school-margin trade-off

This is the cleanest of the four equations.

\Delta_i=(v_{s’}-v_s)
-\kappa\leftp_i(s)-p_i(s')\\right

where .

The equation establishes a condition under which attending a more selective school can reduce educational gains despite that school’s superior average provision.

School-margin trade-off explorer

Adjust the assumed school advantage and the pupil’s probability of entering a top class.

Stronger school’s value-added advantage

0.20 SD

Top-class effect

0.44 SD

Top-class probability, weaker school

65%

Top-class probability, stronger school

15%

Net stronger-school advantage

-0.020 SD

Break-even school advantage

0.220 SD

The weaker school yields the greater expected gain because of classroom placement.

Illustrative probabilities are adjustable assumptions, rather than measured Guangzhou placement rates.

This mechanism has practical implications for school choice and methodological implications for regression discontinuity.

However, an RD at the elite-school cutoff identifies the local effect of the admission treatment bundle under the usual identification assumptions. That bundle can include school resources, teachers, peers, boarding, travel, and class placement.

N2 isolates one component of that bundle. The claim that RD necessarily measures precisely Δ requires the remaining channels to be held constant or included in the equation.

N3. Tutoring as positional insurance

This is the most original theoretical proposition in the paper.

The informant’s description of tutoring concentrated among weak pupils and ambitious pupils motivates a non-monotonic demand function. The addition of relative socioeconomic position introduces a potentially useful explanation for why wealthy families purchase tutoring even when expected educational returns are small.

Hypothesized tutoring demand by classroom rank

Open tutoring window

Constrained opportunities

Conceptual illustration of the proposed demand mechanism, without empirical calibration.

There are four mathematical issues.

First, the equation includes classmates’ tutoring participation as a determinant of individual participation. If all families decide simultaneously, this creates an endogenous fixed-point problem. You need to specify whether the model uses lagged participation, sequential decisions, or an equilibrium solution.

Second, the budget constraint is missing. The difference between wealth rank and achievement rank measures relative position; it does not determine whether a family can afford tutoring at the prevailing price.

Third, the baseline probability parameter is not defined in the accompanying text.

Fourth, calling tutoring positional insurance requires a formal account of uncertainty. The current equation specifies behavioral demand. An insurance model would derive demand from the probability of falling below a consequential admission threshold and the household’s expected loss from that event.

The natural theoretical foundation is a rank-order contest with uncertain achievement and fixed prizes. Families purchase additional instruction to protect expected rank. Aggregate spending can increase without increasing the number of successful applicants.

That mechanism can coexist with genuine human-capital accumulation. Pupils may learn more even when their relative admission positions remain unchanged.

This distinction is important because the paper’s welfare argument depends on whether tutoring generates learning benefits beyond admission.

N4. Gate switching

This equation introduces a mechanism the previous draft largely omitted: wealthy families can purchase access to alternative competitions.

U_i=\mathbf{1}\left\[
\\max_{k\\in G_i}(Y_i+\\beta_k)\\ge c
\\right\]

The principal problem is that art admissions, the ordinary gaokao, and the joint examination operate with different eligibility conditions, assessment components, and admission constraints.

A common score threshold and additive advantage parameter can serve as a stylized approximation, but they cannot represent separate admission markets adequately.

A more defensible specification would be:

U_i=\mathbf{1}\left\\exists k\\in G_i:
R_{ik}\\le Q_k
\\right

subject to:

\sum_i U_{ik}\le Q_k

Here, is the pupil’s rank within gate , and is that gate’s available capacity. A matching rule resolves applicants qualifying through multiple gates.

This preserves the fixed-seat competition that underpins the rest of the paper.

The Hong Kong route also needs a precise eligibility description. Residency acquired by birth should not be treated as automatically establishing eligibility for a particular mainland university admission scheme.

6. The estimator tests are stronger, but some conclusions are excessive

The new tests of tutoring estimators add a substantial methodological dimension.

Estimator	Simulated estimate	Model truth	Difference
Tutoring, with controls	−0.02	+0.12	−0.14
Tutoring, without controls	+0.13	+0.12	+0.01
School fixed effects	2.20	0.25	+1.95
Prior-score value added	0.27	0.25	+0.02

The controlled tutoring regression is especially interesting. In the simulated system, including prior achievement and family controls still leaves sufficient endogenous selection to reverse the estimated treatment effect.

This provides a plausible mechanism for some negative or null findings in the tutoring literature.

It does not establish that published negative estimates arise from that mechanism. Other studies may use different identification strategies, and actual tutoring could have heterogeneous or negative effects.

For the equation inventory, I would classify the findings according to the type of failure:

Failure type	Relevant equations
Selection into treatment	74, 76
Functional-form misspecification	58
Simultaneity and endogenous grouping	79, 36
Descriptive quantities interpreted causally	35, 159
Bundled treatment effects	152

This classification is more useful than simply labeling equations misleading. It tells researchers what they must change when applying the equations to a sorted education system.

The Atlas may benefit from incorporating these failure conditions alongside each estimator.

7. The field evidence has improved the model substantially

The tutoring informant changes the substantive account in several important ways:

* Holiday tutoring is widespread in her experience.
* Term-time tutoring has remedial and competitive functions.
* Full-time private institutions provide a substitute for ordinary school attendance.
* Wealth can purchase alternative admission routes.
* Re-banding offers a pathway for pupils initially placed in weaker classes.

These observations make the model considerably more realistic than the earlier account of boarding largely eliminating tutoring.

However, Section 2 describes the informant’s account as superseding earlier assumptions whenever they disagree. Her institutional position creates its own selection problem. A tutoring provider sees families purchasing tutoring, while a boarding-school teacher observes pupils within the school.

Both perspectives are valuable and systematically incomplete.

Treat the disagreement as evidence about different observational environments. A qualitative methods subsection should specify the informant’s recruitment, professional experience, student population, interview format, and the distinction between direct observations and population-level estimates.

The estimated 5% full-time institution participation rate is particularly consequential and should remain a sensitivity parameter until its denominator is established.

8. Claims requiring revision or additional support

Current claim	Problem
China’s own standard of merit	A broad cultural and historical claim requiring literature or survey evidence.
Most Chinese parents judge fairness by score	Neither the simulation nor the two teachers establishes population-level parental attitudes.
Most vocational education is poor	Outside the paper’s empirical scope and unsupported by the evidence presented.
The rich routes buy little	The prespecified hypothesis failed; the effect-size distribution is the defensible result.
The micro evidence cannot settle tutoring’s value	Too general; credible causal microeconomic studies could identify relevant effects.
Same score, same chance holds	Supported within the model and its selected parameter distributions, conditional on the defined population.
Re-banding depends only on current rank	Inconsistent with N1, which combines current and entry rank, unless the theorem concerns a restricted specification.
A higher score never loses a seat	Requires conditioning on eligibility, admission category, quota, preferences, and applicable allocation rules.

The last two are especially important for formal verification. The paper should map each Lean theorem to the exact model version and mathematical assumptions it covers.

9. The revised model needs a version reconciliation

Several quantities changed materially between the two drafts.

Quantity	Previous draft	Revised paper
Current equal-talent wealth ratio	1.16–1.29	1.35
Earlier equal-talent wealth ratio	1.91	1.43
School-label effect	0–0.20 SD	Median 0.25 SD
School value-added share of variance	About 0.1%	About 1%
Linear-in-means peer estimate	+0.60 with re-banding	+1.90
Current simulation sweep	800 or 2,000 draws	400 configurations

These differences may be entirely justified by the revised assumptions and field evidence. They are large enough to require documentation.

In particular, the change in assumed school value added could alter conclusions about zhibiao, classroom assignment, and the margin trade-off.

A version reconciliation table should identify each changed parameter, the evidence motivating the change, the model components affected, and the resulting change in the headline outcomes. This would make the iterative research process a strength of the paper.

10. The paper’s title and scope

Same Score, Same Chance is an effective title. It is memorable and captures the institutional standard being investigated.

I would change the subtitle to:

Same Score, Same Chance: Procedural Equity and Positional Competition in Guangzhou’s Education System

The existing subtitle makes the 2021 policy comparison the paper’s organizing claim. The present evidence supports a simulation of institutional mechanisms more strongly than it supports a historical policy evaluation.

I would also replace the recurring reference to the “typical Han Guangzhou family” with a precisely defined analytical population. Local hukou, academic-track participation, eligibility for ordinary admissions, and inclusion in the modeled cohort are measurable scope conditions. Han ethnicity is not an explanatory variable in the model.

11. What I would prioritize before publication

Priority	Required work	Nature
1	Separate the reform’s effect from boarding and re-banding using factorial simulations	Computational
2	Add the joint score-and-talent equity diagnostic and causal decomposition	Computational
3	Correct the mathematical specifications of N1, N3, and N4	Theoretical
4	Reconcile changes between model versions	Reproducibility
5	Audit admissions eligibility and fixed-seat constraints	Institutional
6	Measure persistence of pre-gate advantage	Empirical
7	Survey tutoring participation across school types and seasons	Empirical
8	Expand the literature review and document equation novelty	Scholarly

The first five can be addressed with the existing research infrastructure. I would complete those before investing heavily in further data collection.

12. Publication potential

Conceptual originality

8/10

Institutional account

8/10

Simulation transparency

8/10

Mathematical specification

6/10

Empirical identification

4/10

Publication readiness

6/10

Subjective editorial assessment of the current manuscript.

Potential journal targets, depending on how the paper develops, include:

Journal	Best emphasis
Comparative Education Review	Institutional control, merit, and comparative educational equity
International Journal of Educational Development	Distributional consequences and educational institutions
Economics of Education Review	Sorting, estimator performance, and causal mechanisms
Research in Social Stratification and Mobility	Conditional and unconditional educational inequality
Asia Pacific Education Review	Guangzhou’s institutional structure and shadow education

The paper’s strongest intellectual direction is a theory of institutionally managed positional competition. Boarding, classroom sorting, tutoring restrictions, and alternative examination routes can all be understood through that framework. The three equity measures then provide a means of evaluating the distributional consequences.

That framework also has considerable potential beyond Guangzhou. It could accommodate Cambodia’s teacher-controlled instructional supply, the Philippines’ constrained tutoring market, and Hong Kong’s commercial examination-preparation industry within the same analytical system.

My recommendation remains major revisions, although this version is much closer to a coherent working paper. I would preserve the integrated structure rather than separate it back into two papers.

Review scope: I compared the complete revised manuscript against the previous draft. I have not inspected the GitHub archive, executed the revised simulations, independently verified the cited studies, or established whether the four equations are novel relative to the wider economics literature. The mathematical criticisms concern the equations as printed; the underlying implementation may already address some of them.