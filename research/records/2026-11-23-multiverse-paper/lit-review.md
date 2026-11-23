# Literature review and standing assessment

**Question.** Has anyone else done anything like the grouping multiverse? Where does the paper actually stand? How strong are the results? Do we recommend other researchers do this?

**Date.** 23 November 2026. **Author of this memo.** methods-paper (worker), for Dr. Menefee and run-lead.

---

## 1. How I searched, and what this memo cannot do

I searched OpenAlex and Crossref by title, abstract and bibliographic query; publisher full texts were blocked from this machine, so the judgements below rest on titles, abstracts, and bibliographic records, not on reading the papers in full. I ran roughly twenty query variants across five strands: multiverse analysis; specification-curve analysis; vibration of effects; heterogeneity in cross-country panel work; transportability and randomisation inference. I did **not** systematically search *Comparative Education Review*, *Comparative Education*, *Compare*, *International Journal of Educational Development*, or the political-economy journals. Absence of a hit is therefore weak evidence, and the paper's "we are not aware" wording is the right one.

---

## 2. Prior art, strand by strand

### 2.1 Multiverse analysis and the specification curve (borrowed, not ours)

Steegen, Tuerlinckx, Gelman, and Vanpaemel (2016) introduced the multiverse analysis: enumerate defensible analytic choices, run them all, report the distribution. Simonsohn, Simmons, and Nelson (2020) turned it into a visual and inferential object (the specification curve). Young and Holsteen (2017) and Muñoz and Young (2018) brought it into sociology with a computational framework and a multiplicity discipline; Del Giudice and Gangestad (2021) reviewed its promises and pitfalls. The method is now mainstream: Nepomuceno, Ghosal, Sandoval-Lentisco, and Ioannidis (2026, preprint) document 613 multiverse-style studies, and Young and Vermeent (2023) distribute an R package (`multitool`). **Nothing here is ours**, and the paper says so.

### 2.2 Vibration of effects and sampling uncertainty (the closest methodological relative I found)

Patel, Burford, and Ioannidis (2015) show that varying model specification produces a "vibration of effects" that can demonstrate the instability of an observational association. Klau, Hoffmann, Patel, Ioannidis, and Boulesteix (2021) extend the framework to **model, measurement and sampling uncertainty** — including variation in the sample definition. This is the closest existing work to the *idea* that results should be examined across sample choices. But their sampling dimension concerns sampling variability and sample size, not a systematic partition of countries into substantive typologies, and there is no random-partition null and no resolution calculus. **Reviewers will ask about this literature, and the paper should cite it.**

### 2.3 Cross-national and comparative multiverse applications (the closest applications)

Four papers matter:

- **Engzell and Mood (2023, *American Sociological Review*)** run a multiverse over 82,944 definitions of income mobility, "varying how and for whom income is measured", on Swedish register data. The "for whom" dimension is a *population-definition* multiverse — conceptually the nearest thing to a partition multiverse — but it is within one country, and there is no random-partition null, no transportability framing, and no resolution analysis.
- **Herrala (2023, *Research in Social Stratification and Mobility*)** runs 768 multilevel models on 26 European countries, varying exclusion criteria, operationalisation and model formula. This is a genuine cross-national multiverse, but the dimension is analytic choice; the set of countries is fixed.
- **Luo, Zeraatkar, Glymour, Ellis, Estiri, and Patel (2024, *BMC Medicine*)** use a specification curve with 5,357 specifications "to identify heterogeneity" in dementia risk factors across subtypes and analytic scenarios. Heterogeneity is the target, but across outcome definitions and models, not across population partitions.
- **Cakici, Fieberg, Neszveda, Piljak, and Zaremba (2026, *Journal of Banking & Finance*)** examine "Lost in the multiverse": 15 predictors across up to 13,824 implementations of the cross-section of country equity returns, varying nine design choices. Some design choices are about which countries are in the sample, and they find that "setups emphasizing small, segmented countries enhance performance, while those focused on liquid, investable markets tend to weaken it". This is the closest economics analogue of "the answer depends on which countries you include", but it is not a typology multiverse, has no random-partition null, and uses bootstrap/out-of-sample rather than the calibration logic here.

Two further applications are adjacent: Hertel, Barone, and Smallenbroek (2025, *European Societies*) run a "multiverse of social class" over macro-, meso- and micro-level class schemes (a multiverse over *classification schemes*, though of individuals rather than countries), and Cantone and Tomaselli (2023, *Quality & Quantity*) give a formal treatment of multiverse sampling structure for panel models, arguing the set of specifications is an information network rather than i.i.d. draws. Kvarven, Lilletvedt, Strømland, and Johannesson (2026, *Research in Economics*) extend multiverse robustness testing to macroeconomic calibration models — evidence that the multiverse idea is spreading through economics, with a different target (calibration, not cross-country heterogeneity).

### 2.4 The heterogeneity critique in cross-country work (the framing, not the method)

Brock and Durlauf (2001) and Durlauf, Johnson, and Temple (2005) are the canonical statement that pooled cross-country regressions impose homogeneity and that robustness over specifications answers a different question from heterogeneity across countries. Maddala and Wu (2000) and Hineline (2008) make the same point empirically (pooling under heterogeneity; instability over time and regimes). Levine and Renelt (1992) and the "two million regressions" tradition are the sensitivity-analysis antecedent that the paper contrasts itself with. **The framing is borrowed; the paper's contribution is to make it measurable.**

### 2.5 Calibration and inference machinery (borrowed)

The p-value floor of 1/(R+1) comes from Monte Carlo and permutation theory (Hope, 1968; Ernst, 2004; Phipson & Smyth, 2010; North, Curtis, & Sham, 2002). The multiplicity correction is Benjamini and Hochberg (1995). The negative-control interpretation follows Lipsitch, Tchetgen Tchetgen, and Cohen (2010), and the randomised-inference relative is Young (2019). Recent work is pushing multiverse inference further: Rognon-Vael and Rossell (2026, arXiv) propose e-values for multiplicity control in multiverse analysis, and a 2025 neuroimaging paper develops inference for same-data meta-analysis of multiverse results. **The arithmetic of the resolution analysis is built on these; the combination with the step-up cluster correction appears to be ours.**

### 2.6 What I did not find

I found **no** study that (a) treats the partition of countries into substantive typologies as the multiverse dimension, (b) calibrates the multiverse against random partitions of identical group sizes and nesting, (c) states the empirical p-value floor and derives the draws needed for Benjamini–Hochberg certification (including the step-up cluster result), and (d) interprets the whole exercise as a transportability test that holds the pooled association fixed. I also found no random-partition null of this form in the permutation or cluster-inference literature; the closest relatives are randomisation tests for weak null hypotheses and negative-control designs, both of which the paper cites.

---

## 3. Where we actually stand

**Borrowed and correctly attributed:** multiverse logic, specification curves, vibration-of-effects, grouped fixed effects, permutation and Monte Carlo p-values, Benjamini–Hochberg, negative controls, transportability, and the heterogeneity critique. The paper's prior-work section already says it makes no claim to have invented the components.

**Genuinely ours (narrow, defensible):**

1. **A multiverse over country partitions, including estimated typologies.** The dimension is the population partition — regions, income, demography, schooling, farm structure, fiscal capacity, k-means profiles, and Bonhomme–Manresa classes — not the analyst's model choices. The closest prior work (Engzell & Mood; Herrala; Cakici et al.) varies definitions or analytic choices *within* a fixed set of countries.
2. **The random-partition null as an estimable calibration device.** Same countries, same sizes, same nesting, same estimator; only the country-type structure is destroyed. That is what makes the null a test of *heterogeneity/transportability* rather than of existence, and it is the paper's conceptual core.
3. **The resolution analysis.** Empirical p-floor 1/(R+1) against BH's 0.05/M; 5,440 draws for a lone link; the step-up cluster result (30 at the ceiling → 35 certified at 400 draws); the draws-vs-cluster-size table. This is the paper's real methods novelty.
4. **The scale of the demonstration.** 272 links × 179 groups × 400 random partitions = 38.4 million regressions, with determinism and split-halves checks. Scale is not novelty, but it is what makes the resolution calculus concrete.

**Honest risk register.** A reviewer could say: (i) the random-partition null is a special case of permutation testing with clustered data; (ii) the resolution analysis is "just" the Monte Carlo p-floor applied to BH, which is obvious once stated; (iii) the paper is a methods demonstration with a thin substantive payoff. The first two are fair, and the paper's defence is that the combination and the design rule are new and that nobody states them; the third is fairer than it looks, and Section 4 below says why.

---

## 4. How strong are the results?

I score honestly, on a 5-point scale, judging each result against what it claims.

| Result | Strength | Why |
|---|---|---|
| Resolution analysis (floor, BH, cluster, draws table) | **4/5** | Rigorous, checkable arithmetic; independent of the data; useful as a design rule. Not deep theory — "obvious once stated" — but nobody states it, and it changes how a reader must report a multiverse. |
| Transportability framing ("holds the pooled association fixed") | **3.5/5** | Conceptually correct and well matched to Durlauf; the operationalisation is the contribution, not the idea. |
| The five robust links | **2.5/5 as substance** | Two are the demographic-transition relationships (near-identities: child mortality and life expectancy both go with fewer births), three are structural/accounting relations (farm output falls with income; income and urbanisation rise together; mortality and life expectancy move together). They are reassuring, not surprising. Their real value is negative evidence: 14 of the project's 24 earlier "survivors" are no better than random. |
| Massification nulls | **3/5** | Informative and policy-relevant: no massification driver travels; paid employment is a clean null with a 400-draw power check; electricity is strong only with country effects and flips sign across income/trajectory classes. Limited by crude country-level measures and by the associational estimator. |
| Group-specific labels (76 links) | **1.5/5** | Descriptive, not certified; the smoothed tier cannot certify a single tag at 400 draws. Should be sold as hypotheses about where a link is concentrated, not as findings. |
| Overall paper | **3.5/5** | A solid methods paper with a modest empirical payoff; its strongest claims are methodological. That is the right framing, and the paper already uses it. |

The single most important honest sentence for a reader: **a method that finds only five robust links out of 272, and finds that they are the least surprising five, is a method that is working.** The alternative — a method that "finds" 43 robust links — would be the suspicious result.

---

## 5. Do we recommend other researchers do this?

**Yes, conditionally.** It is a good robustness/transportability diagnostic for large cross-country macro panels, and it is cheap relative to collecting new data. But it is easy to do badly, and the failure modes are exactly the ones the paper documents. My recommendation, as a checklist:

**When to use it**

1. You have a macro panel with roughly 100 or more countries and at least 15–20 years, and a claim you want to describe as general.
2. You can pre-specify the typologies *before* seeing the multiverse results (the groupings here were pre-specified and documented; a pre-registration would be better).
3. You are willing to report tiers (strict / smoothed / descriptive) and to state the draw budget's resolution before making claims.
4. You want to distinguish "travels" from "only in some types" from "no better than random" — the three-way distinction is the method's value.

**When not to use it**

1. Small-N panels (under ~50 countries): the groups become too small for cluster-robust inference, and the whole exercise is underpowered.
2. Microdata with adequate sample sizes: ordinary subgroup analysis with pre-registered subgroups is simpler and better understood.
3. Identified causal designs: use the transportability literature (selection diagrams, generalisation weights) rather than a partition multiverse of associations.
4. As a way to "rescue" a pooled coefficient: the method can only tell you whether the association is heterogeneous, not whether it is causal.

**Practical rules**

1. Do the resolution arithmetic **first**: decide whether you need to certify a lone link (thousands of draws) or a cluster (hundreds), and budget accordingly.
2. Report the pooled coefficient alongside the multiverse, never instead of it.
3. Treat group-specific labels as descriptions of concentration, not as findings; the single-region and single-class claims are the weakest.
4. Pre-specify the groupings and document them; a multiverse chosen after seeing results is a garden of forking paths.
5. Pair the multiverse with the specification-robustness tradition rather than replacing it: the two answer different questions.
6. Report the determinism and split-halves checks; they are what distinguish a calibrated multiverse from a fishing expedition.

---

## 6. What this means for the paper (patch applied 23 November 2026)

The paper's `paper.md` currently claims "we are not aware of a study that treats the partition of countries as the multiverse dimension..." — that claim **survives this search**, but the paper is thinner on adjacent work than it should be, and three literatures need to be acknowledged explicitly or a reviewer will think we missed them:

1. **Vibration of effects** (Patel et al., 2015; Klau et al., 2021) — especially Klau et al.'s extension to sampling uncertainty. Suggested addition to §2.1, after the multiverse sentence: "A related framework, the vibration of effects, examines how findings move across model and, in later versions, measurement and sampling choices (Patel, Burford, & Ioannidis, 2015; Klau et al., 2021); we share the diagnostic impulse but vary the population partition rather than the analytic decisions."
2. **Cross-national multiverse applications** (Engzell & Mood, 2023; Herrala, 2023; Cakici et al., 2026) — add to §2.1 or §2.8: "Multiverse methods have been applied to income mobility (Engzell & Mood, 2023), educational stratification across European countries (Herrala, 2023), and the cross-section of country equity returns (Cakici et al., 2026); in each case the dimension is analytic choice or outcome definition within a fixed set of countries, whereas here it is the country partition itself."
3. **Classification multiverses and panel multiverse theory** (Hertel et al., 2025; Cantone & Tomaselli, 2023; Kvarven et al., 2026) — a sentence in §2.8 or the discussion, to show that the multiverse is spreading into economics and classification work and that our contribution is the transportability framing.

The "we are not aware" sentence should then be narrowed to its defensible form: *"We are not aware of a study that treats the partition of countries into substantive typologies as the multiverse dimension and calibrates it against random partitions of identical size and nesting."* That remains true after this search.

**Also worth adding to the limitations:** the search behind this paper is not systematic; a systematic review of the comparative-education and comparative-politics journals is still needed before submission, and a reviewer who knows Engzell & Mood (2023) will otherwise read the paper as less situated than it is.

The patch was approved and applied on 23 November 2026. Section 2.1 of `paper.md` now cites the vibration-of-effects and cross-national multiverse work (Patel et al., 2015; Klau et al., 2021; Engzell & Mood, 2023; Herrala, 2023; Cakici et al., 2026; Luo et al., 2024; Hertel et al., 2025; Cantone & Tomaselli, 2023; Kvarven et al., 2026), Section 2.8 states and answers the two fair attacks (clustered permutation inference; the Monte Carlo p-floor applied to BH), and `refs.md` carries the nine entries with Crossref status. Numbers and the paper's spine are unchanged; the branch was pushed for re-verification.

---

## 7. References added by this memo (verification status)

All records checked 23 November 2026 against Crossref and OpenAlex records (fields only, not full text). Status key as in `refs.md`: VERIFIED = existence and fields confirmed; PREPRINT = confirmed but not peer-reviewed.

- Cakici, N., Fieberg, C., Neszveda, G., Piljak, V., & Zaremba, A. (2026). Lost in the multiverse: Methodological uncertainty in studying global equity returns. *Journal of Banking & Finance, 190*, 107775. https://doi.org/10.1016/j.jbankfin.2026.107775 — VERIFIED.
- Cantone, G. G., & Tomaselli, V. (2023). Theory and methods of the multiverse: An application for panel-based models. *Quality & Quantity, 58*(2), 1447–1480. https://doi.org/10.1007/s11135-023-01698-5 — VERIFIED (Crossref dates the online version 2023; the issue is 2024).
- Engzell, P., & Mood, C. (2023). Understanding patterns and trends in income mobility through multiverse analysis. *American Sociological Review, 88*(4), 600–626. https://doi.org/10.1177/00031224231180607 — VERIFIED.
- Herrala, K. (2023). Does industrial development predict equalization in educational opportunity? A multiverse analysis. *Research in Social Stratification and Mobility, 83*, 100757. https://doi.org/10.1016/j.rssm.2023.100757 — VERIFIED.
- Hertel, F. R., Barone, C., & Smallenbroek, O. (2025). The multiverse of social class: A large-scale assessment of macro-level, meso-level and micro-level approaches to class analysis. *European Societies, 27*(5), 840–888. https://doi.org/10.1162/euso_a_00044 — VERIFIED.
- Hineline, D. R. (2008). Parameter heterogeneity in growth regressions. *Economics Letters, 101*(2), 126–129. https://doi.org/10.1016/j.econlet.2008.07.011 — VERIFIED (no abstract available; cited for the heterogeneity point only).
- Klau, S., Hoffmann, S., Patel, C. J., Ioannidis, J. P. A., & Boulesteix, A.-L. (2021). Examining the robustness of observational associations to model, measurement and sampling uncertainty with the vibration of effects framework. *International Journal of Epidemiology, 50*(1), 266–278. https://doi.org/10.1093/ije/dyaa164 — VERIFIED (Crossref dates the DOI 2020; the issue is 2021).
- Kvarven, A., Lilletvedt, J. S., Strømland, E., & Johannesson, M. (2026). Multiverse robustness tests in macroeconomic calibration models. *Research in Economics, 80*(3), 101135. https://doi.org/10.1016/j.rie.2026.101135 — VERIFIED.
- Luo, R., Zeraatkar, D., Glymour, M. M., Ellis, R. J., Estiri, H., & Patel, C. J. (2024). Specification curve analysis to identify heterogeneity in risk factors for dementia: Findings from the UK Biobank. *BMC Medicine, 22*(1), 216. https://doi.org/10.1186/s12916-024-03424-w — VERIFIED.
- Maddala, G. S., & Wu, S. (2000). Cross-country growth regressions: Problems of heterogeneity, stability and interpretation. *Applied Economics, 32*(5), 635–642. https://doi.org/10.1080/000368400322534 — VERIFIED.
- Nepomuceno, A., Ghosal, A., Sandoval-Lentisco, A., & Ioannidis, J. P. A. (2026). Uptake and implementation of multiverse-style analyses across 613 studies [Preprint]. bioRxiv. https://doi.org/10.64898/2026.07.15.738584 — PREPRINT.
- Patel, C. J., Burford, B., & Ioannidis, J. P. A. (2015). Assessment of vibration of effects due to model specification can demonstrate the instability of observational associations. *Journal of Clinical Epidemiology, 68*(9), 1046–1058. https://doi.org/10.1016/j.jclinepi.2015.05.029 — VERIFIED.
- Rognon-Vael, P., & Rossell, D. (2026). E-values for multiplicity control in multiverse analysis [Preprint]. arXiv. https://doi.org/10.48550/arxiv.2607.17596 — PREPRINT.
- Young, E., & Vermeent, S. (2023). multitool: Run multiverse style analyses [R package]. CRAN. https://doi.org/10.32614/cran.package.multitool — VERIFIED (software record).

Levine and Renelt (1992) is named as the sensitivity-analysis antecedent; its record was not retrieved in this search and it remains UNVERIFIED (as noted in `refs.md`, the Sala-i-Martin/Leamer antecedents are already cited).

**One-line bottom line.** The grouping multiverse is a defensible, modest methods contribution: the resolution analysis is the strongest part, the transportability framing is sound but not new in substance, the substantive results are honest and mostly negative (which is the point), and the closest prior work varies analytic choices within fixed country sets rather than partitioning countries as a transportability test. The paper should recommend the method to others *only* with the resolution discipline and the tiered reporting it describes — and it should cite the vibration-of-effects and cross-national multiverse work before submission so that a knowledgeable reviewer sees the paper knows the neighbourhood.
