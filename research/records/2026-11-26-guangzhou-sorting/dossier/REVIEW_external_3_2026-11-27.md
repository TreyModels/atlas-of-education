Third review: Same Score, Same Chance

Recommendation: Minor-to-moderate methodological revisions, followed by circulation as a working paper.

This revision has produced a more interesting result than the original research hypothesis. Guangzhou’s apparent procedural equity conceals a persistent advantage for wealthier pupils after admission, while the institutional mechanisms that reduce household expenditure differ from those that improve educational equity.

The paper now has a substantive discovery, an explanation for that discovery, and a methodological framework capable of investigating similar systems elsewhere.

The responses to the previous review are unusually thorough. The joint equity diagnostic, factorial experiment, direct interventions, revised historical counterfactual, qualitative methodology, estimator classification, and version reconciliation all materially improve the research.

I would resist expanding the paper much further. Several remaining problems require attention, including two numerical inconsistencies, a population-definition problem, and an important distinction between conditional and causal equity.

1. The central discovery has changed

Four measures of educational inequality

Current Guangzhou simulation, rich-to-poor elite-university admission ratiosReported simulation medians. The four measures condition on different populations and cannot be interpreted as additive components.

Conditioning	Richer pupils’ relative admission probability
Same zhongkao score	9% lower
Same score and latent talent	18% higher
Same latent talent	35% higher
Unconditional	135% higher

The joint diagnostic is the most consequential addition. The richer-to-poorer ratio of 1.18, exceeding parity in 99% of configurations, changes the interpretation of the entire system.

A family observing pupils with identical entrance scores sees something resembling fairness. The simulation reveals that those pupils arrive with systematically different combinations of underlying ability and acquired advantage.

This gives the paper a potentially generalizable proposition: a meritocratic selection system can display conditional socioeconomic parity while continuing to transmit socioeconomic advantage.

That proposition deserves greater prominence in the literature review and discussion.

2. The joint diagnostic still needs one causal qualification

The new measure addresses much of the collider problem identified in the previous review. Standardizing the comparison across pooled score-and-talent cells is a sensible approach.

However, holding score and talent constant does not automatically identify the causal effect of post-admission wealth.

Pupils with the same score and talent may still differ in the composition of their earlier educational advantages. One may have benefited from better teachers, another from tutoring, another from home inputs. If those components persist differently, their later outcomes can diverge even without additional expenditure after admission.

There is also a common-support problem. Some of the 25 score-and-talent cells may contain few or no pupils from one wealth group.

I would require the following diagnostics:

* Report cell counts, overlap, and the proportion of pupils excluded because of insufficient common support.
* Test whether the result survives finer grids, such as 10×10 and 20×20.
* Disable all wealth-dependent post-gate mechanisms while retaining the same pupils, scores, talents, and initial school assignments.
* Recompute under that intervention.

If the ratio moves from 1.18 toward 1.00, you have considerably stronger evidence that the remaining advantage arises from post-admission mechanisms.

This should be straightforward with the existing simulation.

3. Correct the expenditure discrepancy in the abstract

The abstract reports a reduction of approximately 4,600 yuan per pupil over five years. The before-and-after table reports 34,600 yuan before and 29,000 yuan now. The difference between those medians is 5,600 yuan.

Meanwhile, the factorial decomposition attributes 4,600 yuan of reduced expenditure to the ban itself.

These quantities may be distinct and individually correct.

Difference between scenario medians

¥5,600

16.2% lower expenditure

Shapley contribution of the ban

¥4,600

Across factorial configurations

If 4,600 yuan is also the median paired difference between historical and current configurations, explicitly identify it as such. A difference between medians need not equal the median of paired differences.

The same issue appears in the intervention table:

Intervention	Reported T	Reported change	Difference from 1.35
No home advantage	1.19	−0.13	−0.16
Equal zone teachers	1.25	−0.08	−0.10
No pre-gate tutoring effect	1.32	−0.03	−0.03
All three removed	1.09	−0.25	−0.26
No alternative routes	1.27	−0.07	−0.08

These discrepancies are consistent with reporting median paired treatment effects alongside marginal medians. Add a table note confirming the calculation.

4. The factorial experiment answers a different question from the historical comparison

The factorial experiment is an excellent addition. It reveals how different institutional mechanisms affect expenditure and equity.

Contribution to equal-talent inequality

Negative values indicate a reduction in the rich-to-poor admission ratio.

Contribution to household expenditure

Median Shapley contributions reported in Section 4, relative to the all-off factorial baseline.

The important complication is that the Shapley decomposition uses an all-off to all-on comparison. The historical counterfactual already includes boarding, holiday tutoring, and alternative routes.

Consequently, the factorial results establish the average contribution of mechanisms across institutional configurations. They do not directly decompose the historical change from 2021.

Indeed, the reported median Shapley contributions sum to an increase of 0.04 in T and approximately 3,400 yuan in expenditure, whereas the historical comparison shows reductions in both. The different baselines explain why these results can coexist.

I would report two decompositions:

Decomposition	Research question
Full factorial	What does each institution contribute to the system’s overall operation?
Historically anchored	What accounts for the simulated change between the pre-2021 and current regimes?

For the historically anchored comparison, hold boarding and pre-existing alternative routes constant, then vary the ban, re-banding, and any incremental substitution into tutoring.

The paper also needs evidence establishing whether senior-2 re-banding became more prevalent after 2021. The manuscript currently treats its historical absence as an assumption.

5. The early educational advantage result is now convincing within the model

The direct interventions are substantially more informative than the previous attempt to subtract equity ratios.

Equal-talent inequality under alternative interventions

Current system

1.35

Remove pre-gate tutoring effect

1.32

Remove alternative admission routes

1.27

Equalize zone-school teachers

1.25

Remove home-input advantage

1.19

Remove all three pre-gate advantages

1.09

Bar lengths represent inequality above parity (1.00), rather than the full admission ratio.

Removing all three pre-gate mechanisms reduces the distance above parity from 0.35 to 0.09, a reduction of approximately 74% calculated from the reported medians.

This is a strong conditional result. It gives the paper a policy implication: interventions directed at household learning conditions and early school quality may have considerably greater equity effects than restrictions on commercial tutoring.

I would nevertheless define exactly what each intervention does. For example, removing home-input advantage could mean eliminating home inputs entirely, giving every pupil the population-average input, or removing only the relationship between wealth and home inputs.

Those interventions have different implications for achievement levels, admission competition, and welfare.

The code should also report whether total learning rises or falls under each intervention. Fixed university capacity means that an intervention can improve equity while reducing aggregate achievement, or increase achievement while preserving inequality.

6. Head-start fade remains the critical empirical parameter

The revised paper reports that the equal-talent ratio varies from approximately 1.55 with no fade to 1.16 with substantial fade.

The significance of that result warrants a dedicated figure in the manuscript.

Illustrative head-start sensitivity

Pre-gate advantage fade

50%

Equal-talent admission ratio

1.35×

Remaining excess inequality

36%

Linear interpolation between the manuscript’s reported endpoints. This is an illustration, not a fitted response curve or an additional simulation result.

The actual figure should use the simulation outputs, with uncertainty bands for the remaining parameters.

I would also test whether home inputs, school quality, and tutoring have different persistence rates. Treating all earlier advantages as a single stock with a common decay parameter imposes a substantial restriction.

Tutoring may produce temporary examination familiarity. Strong early teaching may produce durable mathematical understanding. Household learning environments may continue influencing pupils throughout high school.

A useful extension would distinguish:

h_{it}=h_{it}^{H}+h_{it}^{S}+h_{it}^{T}

with separate persistence parameters for home, school, and tutoring inputs.

That would establish whether the early-advantage result survives a more heterogeneous model of learning.

7. Review of the revised equations

N1. Classroom-level production

The revised dynamic equation is a considerable improvement. It now incorporates tutoring, teacher allocation, peer effects, and shocks.

One issue remains: the stock of earlier advantage needs its own transition equation.

h_{i,t+1}=(1-\delta_t)h_{it}

Without defining how evolves, the achievement equation leaves ambiguity about how much earlier advantage is removed in successive periods.

The paper also says that classroom placement is re-decided before each year, whereas the institutional description emphasizes senior-2 re-banding. Clarify whether senior-3 assignment changes.

The revised quantile-based placement rule addresses the previous capacity problem, subject to a deterministic rule for ties and rounding when school enrollment multiplied by the top-band share is not an integer.

N2. School-margin trade-off

This equation is ready for inclusion.

The numerical example is correct:

0.20-0.44(0.65-0.15)=-0.02

The qualification concerning bundled RD treatment effects is also appropriate.

I would retain N2 in its current compact form. Its simplicity is part of its value.

N3. Tutoring as positional insurance

The optimization framework represents a substantial theoretical improvement.

The objective function is:

C(T)=pT+
\sum_k L_k\Phi\left(
\frac{c_k-\mu_i-\tau T}{\sigma}
\right)

The printed first-order condition is correct for an interior stationary point. However, the objective is not globally convex.

Defining

z_k=\frac{c_k-\mu_i-\tau T}{\sigma},

the second derivative is

C’’(T)=-
\frac{\tau^2}{\sigma^2}
\sum_k L_kz_k\phi(z_k).

Its sign can change across the feasible interval. A stationary point may therefore be a minimum or maximum, and multiple stationary points may exist.

The solution must compare feasible interior minima with the boundary solutions:

T=0,\qquad
T=\min(W_k,y_i/p).

The model also does not necessarily produce maximum tutoring demand at both classroom tails. It predicts greater marginal returns to tutoring around consequential thresholds, subject to prices, uncertainty, available time, and household resources.

Whether those thresholds correspond to classroom tails depends on how pupils are grouped.

Marginal benefit of tutoring near admission thresholds

Conceptual illustration of threshold-dependent returns. Optimal purchased tutoring also depends on cost and constraints.

There is a deeper theoretical opportunity here. In a fixed-seat competition, admission thresholds are endogenous to the investments of other families.

The present optimization treats thresholds as given. A complete positional-insurance model would determine thresholds jointly with tutoring demand and the seat constraint.

That could become a separate theoretical extension rather than a requirement for this paper.

N4. Gate switching

There is a direct contradiction in Section 6.

The introductory paragraph states that N1, N2, and N4 are implemented as written. The final paragraph of N4 says that the current simulation uses a single ranking with additive bonuses instead of separate capacity-constrained admission gates.

Correct the implementation statement.

The proposed mathematical specification also needs a matching constraint:

\sum_k U_{ik}\leq1

and a consistent definition of total admission:

U_i=\sum_k U_{ik}.

Eligibility must constrain assignments, and the allocation rule must determine what happens when pupils qualify through several gates.

Until separate gates are implemented, the estimate that alternative routes account for 10% of elite seats and add 0.07 to the equity ratio remains a result from the additive-bonus approximation.

8. The analytical population is internally inconsistent

The paper defines its population as local-hukou academic-track pupils who sit the ordinary gaokao. Yet it includes art and joint-exam admission routes in its principal university-admission outcome.

This matters because joint-exam eligibility may involve a different registration and residency population.

I recommend separating the following outcomes:

Outcome	Population
Ordinary-exam equity	Local academic-track pupils competing through ordinary gaokao admission
All-route equity	Defined origin cohort, including eligible alternative admission routes
System-wide access	Entire relevant age cohort, including vocational placement and exclusion

This would allow you to determine whether ordinary academic competition approaches procedural equity while access to alternative competitions increases inequality across the broader population.

There is a related issue with defining elite universities as the top 10% of gaokao results. This is a simulated fixed-capacity outcome. Actual elite-university admission depends on provincial quotas, subject combinations, preferences, and institutional admission rules.

Throughout the methods section, call the modeled outcome a top-decile admission slot or explicitly identify it as a proxy for elite-university admission.

9. The estimator tests now have a defensible methodological structure

The classification of failure types resolves much of the previous concern about criticizing descriptive estimators for their lack of causal identification.

The remaining opportunity is to establish which corrective specifications recover the known simulated effects.

Problem demonstrated	Corrective test worth adding
Tutoring selection	Randomized tutoring assignment as a benchmark
Nonlinear demand	Rank splines or threshold-distance specifications
Peer-demand endogeneity	Lagged leave-one-out class participation
Teacher-peer confounding	Separate teacher effects and exogenous peer assignment
School sorting	Prior-achievement controls and simulated randomized school assignment
RD treatment bundling	Compare RD estimates with the true local bundled treatment effect

A randomized benchmark would be particularly valuable. If the same estimator recovers the programmed effect under randomized treatment and fails under endogenous treatment, the source of the failure becomes much clearer.

For Equation 76, report the significance level used to establish the 64% rejection rate when the true interaction is zero. The reader needs to distinguish ordinary false positives from systematic misspecification.

For Equation 36, put the estimated and true peer effects into comparable units. An estimated coefficient of 1.9 cannot be directly compared with peers accounting for 34% of a 0.44 SD class effect without defining their respective scales.

10. Qualitative evidence and research ethics

The qualitative methods subsection is now much stronger. Disclosing that the informant is a personal contact, that she reviewed 41 assumptions, and that her population estimates enter sensitivity ranges gives readers an appropriate understanding of the evidence.

Two additions remain advisable.

First, document consent for recording, translation, research use, and archiving. Given the discussion of potentially prohibited tutoring activity, the archived transcript may contain identifying details even when the informant’s name is withheld.

Second, distinguish what the informant directly observed from what she inferred about Guangzhou generally. A supplementary evidence table linking each model parameter to its supporting observation would make this especially transparent.

The existing version reconciliation is worth preserving. It documents how new evidence changed the model and shows that the initial equity conclusion became less favorable as previously omitted mechanisms were introduced.

That is scientifically useful.

11. The title is now right, but the paper needs a literature section

Same Score, Same Chance: Procedural Equity and Positional Competition in Guangzhou’s Education System accurately captures the revised contribution.

The principal scholarly weakness is now the limited engagement with existing theory. The paper needs to locate its contribution within established research on educational production, positional goods, rank-order tournaments, shadow education, and equality of opportunity.

In particular, I would investigate the relevance of:

Scholar or literature	Connection to the paper
Mark Bray	Shadow education and institutional variation
Fred Hirsch	Positional goods and socially scarce opportunities
Lazear and Rosen	Rank-order tournament incentives
James Heckman and colleagues	Dynamic skill formation and persistence
Charles Manski	Identification of endogenous social effects
John Roemer	Equality of opportunity and circumstances
Bourdieu	Transmission of family advantage through education

These are suggested theoretical connections, rather than a verified literature review.

I would describe N1–N4 as proposed model specifications until their novelty relative to existing research has been established. Their contribution may lie primarily in integrating familiar economic mechanisms within a particular institutional system.

12. Assessment across the three drafts

Development of the research

Conceptual framework

V1

6/10

V2

8/10

V3

9/10

Causal reasoning

V1

4/10

V2

6/10

V3

8/10

Mathematical specification

V1

5/10

V2

6/10

V3

8/10

Simulation transparency

V1

8/10

V2

8/10

V3

9/10

Empirical identification

V1

3/10

V2

4/10

V3

5/10

Working-paper readiness

V1

4/10

V2

6/10

V3

8/10

Subjective editorial assessment of the three manuscripts, rather than a standardized evaluation.

13. What I would do before releasing this version

Priority	Task	Estimated effort
1	Reconcile expenditure figures and paired-effect reporting	Low
2	Correct N4 implementation statement and population definitions	Low
3	Run post-gate mechanism ablation for S*	Low–moderate
4	Produce historically anchored factorial decomposition	Moderate
5	Correct N3 optimization conditions	Low
6	Report common support and parameter distributions	Moderate
7	Add literature review and institutional source references	Moderate
8	Audit informant consent and archive confidentiality	Low

I would then freeze this model version and circulate the paper.

Further development should focus on empirical validation, especially measuring the persistence of earlier educational advantage. Repeatedly expanding the simulation risks producing greater computational sophistication without a corresponding improvement in knowledge about Guangzhou.

Final assessment

The paper has evolved from a defense of Guangzhou’s educational fairness into an investigation of how institutional design produces, conceals, and sometimes reduces inequality.

Its principal contributions are now identifiable:

* Substantive: Same-score parity can conceal socioeconomic advantages after admission.
* Policy: Tutoring restrictions and classroom reassignment operate through different expenditure and equity mechanisms.
* Methodological: The joint equity diagnostic and estimator tests reveal how student sorting changes the interpretation of educational statistics.
* Theoretical: Positional insurance and classroom-level provision provide a framework for studying educational competition across institutional settings.

I would regard this as a credible simulation-based working paper after the remaining corrections. Submission to a peer-reviewed economics or comparative education journal would require a fuller literature review, reproducibility audit, and stronger empirical grounding.

Review scope: I reviewed the complete third manuscript against both earlier versions, checked the printed mathematical expressions, and calculated the numerical comparisons above. I have not executed the simulations, inspected the GitHub archive, independently verified the field evidence, or established the novelty of the proposed equations. My assessment of publication readiness concerns the manuscript as supplied.