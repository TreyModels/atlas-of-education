Review: Guangzhou Sorting System, Two Working Papers

Overall assessment: A promising research program with a coherent theoretical argument, an unusually transparent simulation framework, and several potentially publishable contributions. The main weakness is identification.

The six-page document is stronger as a research memorandum than as evidence for its two central claims. Paper 1 offers a plausible explanation for Guangzhou’s limited shadow-education market among boarders, but its empirical test measures boarding and school selectivity rather than tutoring behavior. Paper 2 has a more developed quantitative foundation, although its equity conclusions depend heavily on an unmeasured parameter governing how quickly educational advantages acquired before age 15 disappear.

The distinction between synthetic and observed results is handled carefully in the opening. That discipline should extend to the conclusions, where some language becomes stronger than the evidence permits.

My assessment of the two papers differs:

* Paper 1: Strong conceptual contribution; empirical evidence remains preliminary.
* Paper 2: More substantial methodological contribution; the central equity finding is sensitive to model assumptions.
* Equation tests: Potentially valuable, but require sharper definitions of what each estimator is supposed to identify.
* Formal verification: Useful for establishing properties of the mathematical system; its contribution to the substantive findings needs more precise boundaries.

The most important revision is to distinguish findings that follow mathematically from the model’s design, findings that survive uncertainty about its parameters, and findings that have independent empirical support.

1. Highest-priority finding: the admissions rules need a more exact implementation

I checked the official Guangzhou regulations, and this is the most concrete issue I found.

The draft describes zhibiao as allocating half of elite-school seats to the highest-scoring pupils within each junior school. Guangzhou’s 2026 rules are more specific:

* Eligibility generally requires Guangzhou hukou (or protected status) and qualifying junior-school enrollment history.
* The 50% allocations depend on the numbers of eligible pupils, with district-specific rules, computerized assignment, and special provisions for certain weaker schools.
* Admission requires meeting a school-specific minimum score and other requirements; unused allocated seats can revert to ordinary admission. gzzk.gz.gov.cn +1

The 2027–2029 rules also confirm that ordinary non-hukou applicants face school-specific ceilings of 8–20% at public high schools, alongside separate eligibility requirements involving school enrollment and residence documentation. gzzk.gz.gov.cn

These details matter because Paper 2’s conclusions about zhibiao, hukou, and the effects of removing quotas depend on how admissions are implemented.

Required check: Inspect gz_v3.py for hukou eligibility, enrollment requirements, allocation by eligible student count, school-specific migrant caps, minimum scores, and reassignment of unused seats. The document’s description does not establish whether these mechanisms are already present in the code.

The claim that zhibiao contributes little to equity should remain provisional until that check is complete.

2. Paper 1: Shadow education when the state controls time

The paper’s most interesting contribution is its treatment of time as a constraint on the production and consumption of tutoring. That mechanism deserves development.

The four conditions specified in the draft, competitive gate, instructional gap, available time, and household resources, give you a framework that could travel across education systems. The theoretical contribution could be more substantial than the Guangzhou case itself.

The central empirical problem is that boarding and tutoring are different dependent variables.

The finding that admission cutoffs and boarding capacity have a within-district rank correlation of 0.22 (permutation p ≈ 0.011) is useful. It establishes a relationship between selectivity and boarding provision within the observed schools. It does not directly establish that boarding suppresses tutoring.

Boarding may correlate with institutional prestige, school resources, family preferences, residential geography, or admissions policies. Those variables could influence tutoring independently.

The strongest empirical test would measure actual tutoring participation and expenditure, comparing boarders and day pupils with similar prior achievement and household characteristics. Include regular school weeks, weekends, and vacations separately.

The model’s result that boarding acts as a threshold in 100% of draws needs particular scrutiny. If tutoring becomes impossible whenever available time falls below a programmed minimum, the result follows from the functional form. Compare the threshold specification against a continuous time-cost model, where boarding reduces opportunities without eliminating them.

A chronology problem

The argument combines two mechanisms operating at different educational stages.

The 2021 Double Reduction policy primarily targeted compulsory education through grade 9. Guangzhou’s boarding mechanism in this paper concerns senior high school, grades 10–12. The Ministry of Education’s description confirms the compulsory-school focus of the original reform. en.moe.gov.cn +1

The distinction matters for causal interpretation.

For pupils preparing for the zhongkao, restrictions on commercial tutoring change the availability of supply. For senior-high boarders preparing for the gaokao, the proposed mechanism concerns control over time and the provision of instruction inside school.

These mechanisms can complement one another. They need separate predictions and evidence.

The residual-market prediction is especially valuable

The draft predicts that tutoring should concentrate among day-school pupils who narrowly missed elite admission cutoffs. This is a testable and potentially distinctive implication.

However, the inference that wealthy families in expensive core districts are purchasing the experience boarders receive through schools currently goes beyond the observed data. Bed coverage and residential property values do not directly measure tutoring expenditure.

A survey showing elevated tutoring among near-cutoff day pupils, after adjusting for wealth and prior achievement, would materially strengthen the paper.

The anonymous boarding-school survey proposed in the final section should have priority over further simulation runs. I would also measure academic help received through informal, online, and holiday arrangements.

Publication judgment: The conceptual framework is promising. The Guangzhou component needs direct tutoring data before it can carry the substantive conclusion.

3. Paper 2: Equity after the gate

This paper contains the more developed quantitative work. Separating latent talent from acquired skill creates a way to examine the influence of early educational advantages in the simulation.

Its greatest vulnerability is also contained in that distinction.

The unmeasured fade parameter dominates the conclusion

The draft reports that the speed at which pre-gate educational advantages fade in high school has rank correlations of approximately −0.6 to −0.8 with the equity outcomes.

That is an exceptionally important result.

The paper’s claim that Guangzhou approaches equality of opportunity at equal talent depends on how much earlier advantage disappears after age 15. The draft identifies this assumption as unmeasured.

The median rich-to-poor ratio of 1.16 in v3 is encouraging as a model outcome, but the 5th–95th percentile range of 0.99–1.60 includes scenarios with substantial inequality. These are sensitivity percentiles over the chosen input distribution, rather than statistical confidence intervals about Guangzhou.

I would make fade the organizing variable in the results. Show how university access changes across its full admissible range, holding other assumptions constant, and identify the thresholds at which the level-field conclusion changes.

It is also worth establishing which observations could identify this parameter. Longitudinal panel data may track achievement persistence, although separating genuine catch-up from regression to the mean, measurement error, and selective entry into academic high schools will require care.

Equality conditional on talent has a narrow interpretation

The simulation treats talent as an individual characteristic that can be separated from teaching and home inputs. That is a coherent modeling assumption.

Empirically, talent is latent. Its definition and the assumed relationship with wealth determine what the model counts as opportunity inequality.

You therefore need an explicit defense of the equal-talent counterfactual. The main text should identify whether talent represents potential achievement absent environmental differences, an innate latent trait, or something else.

I would report outcomes under several definitions of fairness: equal latent talent, equal achievement at the zhongkao, and unconditional access across socioeconomic groups.

This would also reduce dependence on a single normative interpretation of merit.

The hukou conclusion is narrower than the framing

The draft concludes that weaker pre-gate schooling explains more of the remaining hukou gap than the high-school quota.

That is interesting, particularly because the prespecified tests did not support the hypothesis that the quota is the dominant mechanism.

However, the model distinguishes several populations that must remain separate analytically: all non-hukou children, those reaching the zhongkao, those eligible for public academic admission, those entering private schools, and those leaving the modeled pathway.

A small gap among pupils who remain can coexist with substantial exclusion at entry.

The reported 95% public academic placement rate among high-talent non-hukou pupils, the 3.5% exit rate, and the 1.11× local-to-non-hukou university-access ratio need explicit denominators and conditioning rules.

The statement that 95% of high-talent non-hukou pupils obtain public academic seats could be highly sensitive to the assumed size and composition of the non-hukou cohort.

That sensitivity is acknowledged. It should become a principal result rather than a qualification.

The zhibiao and re-banding conclusions need more precise language

The prespecified zhibiao claim was supported in 47.4% of draws against a 90% threshold. That establishes failure of the prespecified criterion. It does not by itself establish that zhibiao has zero effect.

Similarly, re-banding narrowed the local wealth gap in 80.4% of draws. The 90% decision rule was missed, while the direction of the effect was favorable in a substantial majority of simulated configurations.

Report the distribution of effect sizes, including the conditions under which each mechanism helps or harms disadvantaged pupils. This would be more informative than binary success labels alone.

The subsidy claim needs a clearer welfare interpretation

A public subsidy concentration index of 0.02 is consistent with nearly wealth-neutral allocation as measured by that index.

It does not establish equivalent educational quality, equivalent private cost, or equal access to desirable pathways.

The result appears sensitive to vocational subsidies of approximately 38,400 yuan per pupil-year. Since vocational outcomes are outside the model, the paper should state explicitly that the measured equality concerns public expenditure, not the quality-adjusted educational benefit received.

The reported 206,000-yuan twelve-year subsidy difference also should be reconciled carefully with the roughly 290,000-yuan additional private-school expense. They measure distinct quantities.

4. Equation tests: a methodological contribution worth preserving

This section may eventually be the most generalizable part of the work.

The school fixed-effects result is striking:

School fixed-effects contrast

2.22 SD

Median model output

True school-label effect

0–0.20 SD

Assumed model range

The gap illustrates how selective student sorting can generate large school-level differences when causal school effects are small.

There is an important methodological distinction, though.

School fixed effects do not automatically estimate causal school quality. A fixed-effects coefficient identifies a conditional school-level association unless additional assumptions justify causal interpretation. Similarly, a multilevel variance decomposition describes the location of observed variation rather than identifying the causal contribution of schools.

Consequently, describing both estimators as misleading in every simulation draw risks criticizing them for failing to identify something they do not inherently claim to identify.

A stronger methodological contribution would specify each estimator’s target quantity, demonstrate the assumptions under which it becomes causal, and quantify the bias introduced when those assumptions fail under sorting.

The peer-effect sign reversal under re-banding is particularly interesting. That result deserves a complete derivation and a demonstration that the apparent sign reversal survives plausible alternative estimators.

The regression-discontinuity result is appropriately described as noisy. A median of zero with a 5th–95th percentile interval of approximately −0.53 to +0.55 SD supplies little information about a true effect assumed to lie between zero and 0.2 SD.

One additional model check is essential: the draft uses a 0.44 SD top-class effect incorporating teachers and peers, while independently varying teacher effects from 0.15 to 0.45 SD. Verify that the implementation accounts for their overlap and does not count teacher quality twice.

5. Simulation design, formal proofs, and reproducibility

The preregistered sweeps are a strength. It is especially useful that the document reports the failed tests prominently and admits that one directional result was partly built into the simulation.

However, a claim being supported in 97.8% of draws means it survives 97.8% of the sampled model configurations. Its interpretation depends on how those configurations were selected.

For publication, the complete joint parameter distribution, parameter dependencies, random seeds, outcome definitions, and decision thresholds should be disclosed. The paper should distinguish broad plausibility ranges from empirically estimated distributions.

The 26 Lean theorems are a credible contribution to software assurance, provided their statements and assumptions are available. Their current scope excludes v3, which produces many of the most consequential substantive results. Formal proof establishes the specified properties of the formalized model, while the realism of its empirical assumptions and the consistency of its software implementation require separate validation.

I would give the formal verification a technical appendix unless it becomes central to the paper’s methodological argument.

There is also a calibration concern. Matching the model’s teacher and between-school variance components to estimates from Haidian provides a useful benchmark. It is a limited test of Guangzhou-specific realism, especially where a model can reproduce observed between-school variance through sorting.

A stronger calibration section would distinguish parameters chosen to reproduce benchmarks from outcomes held back for independent validation.

6. Recommended revision sequence

01

Audit admissions implementation in v3.

Match the actual hukou eligibility rules, school-specific ceilings, zhibiao allocations, and unused-seat handling against the 2026 and 2027–2029 regulations. Rerun the main sensitivity study if necessary.

02

Make head-start persistence the central sensitivity analysis.

Identify the parameter values under which the 1.16× equity result approaches parity or diverges substantially.

03

Obtain direct tutoring measurements for Paper 1.

Prioritize a confidential survey of boarding and day pupils, with term-time and vacation outcomes distinguished.

04

Recast the equation tests around estimands.

Specify what each estimator recovers, what causal interpretation would require, and precisely how sorting or re-banding changes the result.

05

Complete the data provenance audit.

Reconcile the three citywide seat counts, document why 30 of 153 schools lack district matches, verify the subsidy measures, and trace the historical policy sources.

7. Editorial observations

The document is compact and readable. Its presentation of unsupported hypotheses is especially effective. The status table and the table of prespecified outcomes help distinguish exploratory findings from simulation results.

There are several small editorial improvements worth making. The subsidy row in the parameter table breaks awkwardly between pages 3 and 4. The table typography is dense, and the document needs source references that allow readers to trace the regression-discontinuity estimates, teacher-effect estimates, and subsidy schedules.

I would also reserve expressions such as “confirmed in every draw” for tightly specified computational results. The conclusion that a conventional estimator performs poorly under a given data-generating process is meaningful, but it depends on that process.

Finally, the two working papers should develop distinct literatures. Paper 1 belongs primarily in the comparative shadow-education and institutional-time literature. Paper 2 would benefit from anchoring itself more explicitly in equality of opportunity, student sorting, and the distinction between schools and classrooms as sites of educational production.

Publication assessment

Recommendation: Major revisions, with a favorable assessment of the underlying research program.

I would develop Paper 2 first as a simulation-based methodological paper, using Guangzhou as a documented institutional case and treating the empirical equity outcomes as conditional predictions. Its most convincing contribution may be the demonstration that classroom assignment, admissions rules, and persistence of earlier advantage jointly determine what school-level statistics appear to show.

Paper 1 has the more distinctive theoretical proposition. Its ability to become a convincing empirical paper depends on observing the tutoring behavior that its institutional explanation predicts.

The strongest existing result may be the identification of what remains unknown: the persistence of pre-gate advantage, the actual size and eligibility composition of the non-hukou cohort, and how boarding affects tutoring participation across the school year. Those are concrete empirical questions arising from an explicit model.

I reviewed the complete six-page document and checked the relevant official Guangzhou admissions provisions. I have not independently executed gz_talent.py, gz_v3.py, the equation tests, or the Lean project, so the reported simulation statistics and proofs remain unaudited.