Fourth review: Same Score, Same Chance

Recommendation: Freeze the simulation, complete the documentation and research ethics requirements, and release as a working paper.

This version resolves nearly every substantive methodological objection raised in the previous reviews. More importantly, the additional experiments have produced findings that qualify the earlier conclusions in scientifically meaningful ways.

The post-gate ablation is particularly valuable. It establishes that approximately half of the socioeconomic advantage among pupils of comparable scores and talent comes from mechanisms operating after the zhongkao, with a residual advantage associated with earlier educational inputs.

I would stop the cycle of major computational revisions here. The remaining limitations principally concern empirical validation, documentation, and the precision of several claims.

1. The research has arrived at a stable substantive finding

Socioeconomic inequality under different definitions of fairness

Rich-to-poor probability ratio for a simulated top-decile admission slotAblated means wealth-dependent post-gate mechanisms are switched off. These ratios use different conditioning populations and are not additive.

The results now support a coherent account of educational inequality within the simulated system:

Research question	Result
Do pupils with similar entrance scores have similar outcomes?	Approximately, S = 0.91
Does family wealth still matter at comparable score and talent?	Yes, S* = 1.19
Does removing post-gate wealth mechanisms eliminate that advantage?	Partially, S* falls to 1.09
How unequal are outcomes at equal talent?	T = 1.35
How unequal are realized outcomes overall?	2.34

The paper’s central proposition has survived successive attempts to challenge and refine it.

The original manuscript emphasized the fairness of Guangzhou’s sorting system. The current manuscript explains why different measures of fairness produce different answers, identifies mechanisms responsible for those differences, and establishes their relative importance within the model.

That is a considerably more useful research contribution.

2. The post-gate ablation is the strongest new result

Excess socioeconomic advantage at comparable score and talent

49%

removed by disabling post-gate wealth mechanisms

49%

51%

Post-gate mechanisms

Holiday tutoring, institutions and alternative routes

Residual advantage

Attributed to persistent earlier inputs within the model

The ablation directly addresses the causal qualification raised in the previous review. The comparison uses the same pupils and disables wealth-dependent mechanisms operating after admission.

There is one remaining interpretive issue. The residual 1.09 ratio is attributed entirely to persistent earlier advantage. That attribution requires either an exhaustive accounting of the remaining mechanisms or an additional intervention that eliminates the persistence of earlier advantage.

Because S* uses discretized score-and-talent cells, some residual inequality could also arise from differences within those cells.

I would qualify the residual as consistent with persistent earlier advantage under the model’s assumptions. This requires a wording change rather than another simulation.

3. The common-support analysis is satisfactory

The sensitivity of S* to the grid resolution is reassuring.

Grid resolution	S*	Population covered
5 × 5	1.19	99%
10 × 10	1.20	92%
20 × 20	1.16	47%

The 10 × 10 result provides particularly useful corroboration because it improves conditioning precision while retaining most of the analytical population.

The 20 × 20 result is less directly comparable because it excludes more than half the relevant pupils. The manuscript correctly reports that limitation.

I would retain the 5 × 5 estimate as the primary result and report the others as sensitivity checks.

4. The historical decomposition now works

The distinction between the historically anchored experiment and the full factorial resolves the previous baseline problem.

Historically anchored contributions to the simulated change

Tutoring expenditure

−¥4,800

Median paired change over five years

Equal-talent inequality

−0.06

Median paired change in T

Contribution to change in T

−0.02

−0.04

Tutoring banSenior-2 re-banding

Illustrative proportions calculated from the reported median Shapley contributions.

The policy distinction is important. Restricting tutoring reduces family expenditure, while allowing pupils to move between ability bands accounts for a larger portion of the simulated improvement in equal-talent equity.

The remaining historical uncertainty is explicitly acknowledged: the manuscript has yet to establish that performance-based re-banding became more prevalent after 2021.

Consequently, the spending result has a firmer historical foundation than the equity result. I would maintain that distinction in the abstract.

5. The early-intervention findings have considerable policy significance

The addition of aggregate learning outcomes strengthens the analysis considerably.

Intervention	Excess inequality removed	Mean learning change
Equalize home inputs	44%	0.00 SD
Equalize zone-school teacher quality	22%	0.00 SD
Eliminate pre-gate tutoring effects	8%	−0.02 SD
Combined intervention	74%	−0.02 SD

Within the model, redistributing early educational inputs produces substantial equity gains with little aggregate learning loss.

The policy implications differ considerably from those of a paper focused primarily on commercial tutoring.

However, the near-zero aggregate learning effect may follow mechanically from the model’s additive production function and preservation of average inputs. If educational inputs have diminishing returns or interact with existing skills, redistribution could change aggregate achievement.

Similarly, giving every household the average home input is a theoretical intervention. Its practical cost and feasibility remain unknown.

Present these results as distributional counterfactuals. They identify where an intervention might matter, without establishing the cost-effectiveness of any particular policy.

6. Head-start persistence should now become the empirical research program

Persistence of earlier advantage and equal-talent inequality

Reported simulation medians across 400 configurations, grouped by the proportion of pre-gate advantage that fades by senior 2.

This is probably the most important figure to include in the eventual published paper.

The difference between the first and last parameter bands represents a 71% reduction in excess inequality above parity. The empirical uncertainty surrounding this parameter therefore matters enormously.

I would prioritize longitudinal school records over another general household survey. Ideally, the dataset would include zhongkao subject scores, subsequent term examinations, initial class assignment, teacher assignment, senior-2 reassignment, family socioeconomic indicators, tutoring histories and final gaokao results.

Your teaching experience gives you a practical understanding of which records schools maintain and how classroom reassignment works. Even a carefully documented single-school longitudinal study could provide an initial empirical test of the persistence mechanism, although it would have limited external validity.

7. Remaining technical and editorial corrections

These are the issues I would fix before freezing the manuscript.

Location	Issue	Recommended correction
Section 3	Heading says three ratios, but four are reported	Rename to “Measuring educational equity”
Section 3	T still lacks a formal mathematical definition	Specify talent bands, weighting, population and common support
Section 3	S* above parity is interpreted as post-admission gain	Acknowledge persistent earlier inputs and residual within-cell differences
Section 4	Spending levels lack percentile ranges	Restore the ranges or explain their omission
Section 4	Ordinary-exam competition is described as fairer	Specify the equity criterion; S = 0.85 is farther from parity than 0.91
Section 5	Peer-effect estimate and model truth use incomparable units	Classify the quantitative recovery test as unresolved
Section 6	N1 says placement is reconsidered annually	Align with the entry and senior-2 assignment schedule
Section 6	N3 uses k for both thresholds and time windows	Use separate indices
Section 6	N4 reports a 0.07 route effect, while Section 4 shows a 0.10 difference in medians	Identify whether 0.07 is a paired effect or an earlier sweep
Section 8	Version history ends at v5–v7, but the freeze is called v5.1	Identify the exact code commit and manuscript version

One conceptual point deserves particular attention: the ordinary-exam ratio of 0.85 indicates a larger departure from socioeconomic parity than the all-route ratio of 0.91. The ordinary-exam system produces less rich-family advantage under T and S*, but describing it as uniformly fairer conflates the different standards the paper has carefully established.

8. The literature section is appropriate for a working paper

The new literature section gives the research an identifiable theoretical lineage. Its connections to Bray, Hirsch, Lazear and Rosen, Cunha and Heckman, Manski, Roemer, and Bourdieu are sensible.

Two distinctions would improve it.

Roemer’s equality-of-opportunity framework involves normative decisions about which circumstances and individual characteristics people should be held responsible for. Equal latent talent in your simulation represents one particular standard of opportunity. It should be distinguished from a comprehensive application of Roemer’s theory.

The tournament literature also provides a useful distinction between private incentives and social returns. Tutoring can increase individual admission probabilities, raise aggregate learning, and consume resources in competition for fixed seats. Those effects can coexist, which makes the welfare implications of tutoring more complicated than the expenditure analysis alone establishes.

Add complete bibliographic entries for the works named in the new section. They currently appear in the discussion but are missing from the formal source list.

9. Two outstanding requirements before circulation

Research ethics. Section 8 acknowledges that informant consent and transcript confidentiality still require documentation. This is a genuine release blocker, particularly because the conversation concerns potentially prohibited commercial activity. Resolve it before making the field archive publicly accessible.

Reproducibility. The paper should have a supplementary parameter register. This is more important now than additional equations or simulation sweeps.

Each parameter should have a documented definition, range, sampling distribution, source, evidentiary status, dependencies on other parameters, and model version.

The reported frequencies across configurations, including the 99% expenditure reduction and 84% equity improvement, depend on how those configurations are generated. A parameter register allows readers to assess whether those frequencies remain meaningful under alternative plausible assumptions.

The existing version reconciliation and preregistration history provide a good foundation for this.

10. Assessment across all four drafts

Editorial assessment of manuscript development

Subjective scores on a ten-point scale

	V1	V2	V3	V4
Conceptual framework	6	8	9	9
Causal reasoning	4	6	8	9
Mathematical specification	5	6	8	8
Simulation transparency	8	8	9	9
Empirical identification	3	4	5	5
Working-paper readiness	4	6	8	9

Empirical identification remains at five because the additional simulations improve understanding of the model rather than independently establishing the mechanisms’ magnitude in Guangzhou.

That distinction is now consistently acknowledged throughout the manuscript.

11. What I would do next

Action	Decision
Expand the simulation further	Defer
Implement full equilibrium tutoring demand	Separate theoretical extension
Implement separate admission markets	Future model revision
Extend Lean verification	Technical companion project
Complete parameter documentation	Before release
Document informant consent	Before release
Correct remaining textual inconsistencies	Before release
Circulate as a working paper	After corrections
Collect longitudinal achievement data	Highest research priority

I would also preserve the complete development history as a supplementary research record. Across these four drafts, the initial hypothesis became progressively less favorable to the system as additional evidence and mechanisms entered the model. The preregistered failures, corrected capacity bug, revised counterfactuals and changing equity estimates make that history worth documenting.

Publication verdict: Ready for working-paper circulation after the specified corrections and documentation requirements. A journal submission would still benefit from independent computational replication, fuller institutional citations and empirical validation.

My review covers the complete fourth manuscript and its development across the preceding three versions. I have checked the printed equations and reported numerical relationships. I have not inspected or executed the underlying code, verified the preregistration hashes, audited the Lean proofs, independently checked the cited literature, or examined the confidential field records. Those remain outside this assessment.