# Novelty ledger — what of this session is actually new?

Worker `novelty-review`, branch `research/novelty-2026-11-23`, 23 November 2026.
Purpose: test Dr. Menefee's suspicion that we have been rediscovering known things. One row per candidate
claim: closest prior work, what if anything is new, and a verdict. Plain words; no variable names.

**Verdict legend**
- **NEW** — we are not aware of this result or this exact design rule in the literature.
- **INCREMENTAL** — the components are known; the application, combination or calibration is a genuine addition.
- **KNOWN** — this is established prior work; we have replicated it, not discovered it.

**Verification method.** Web search only (the Mac's general web path is degraded; GitHub and Crossref direct
are unreachable, and fetching journal pages fails). A citation is marked `[verified URL]` when a search result
pointed at the work itself or its Crossref/PubMed/Scopus record; `[unverified]` when only the bibliographic
details are known. No fabricated citations. Where I could not reach the full text, the judgement is based on
titles, abstracts and snippets, and is flagged.

---

## A. ELECTRICITY AND THE SCHOOLING DRIVERS (priority)

**The session's claim.** Electricity → schooling, wage jobs → schooling and farm-input → schooling look strong in
a pooled cross-country panel with country fixed effects; once each country gets its own straight-line trend they
vanish. A power simulation says a true 20-point electricity effect would have been detected nine times in ten.
Reading: "cannot be separated from development at this sample size", not "zero". The famous +16.05 comes from one
specification; on the full matrix with trends the electricity-to-lower-secondary estimate is +0.07 ± 0.19.

### A1. "Electricity raises schooling" — the effect itself
Prior work is abundant, and mostly micro/regional: rural electrification and human capital in China
`[verified URL: tandfonline DOI 10.1080/00220388.2026.2727160]`; small hydropower and girls' education
`[verified URL: ScienceDirect S0304387826001458]`; energy poverty and gender equality in education
`[verified URL: ScienceDirect S0040162524000702]`; energy poverty and inclusive education in Sub-Saharan Africa
`[verified URL: doi 10.1007/s43546-026-01322-2]`; a school-electrification geography study from Aarhus
`[verified URL: pure.au.dk]`; and a cross-country study titled "Electrification and Children's Education: A
Cross-Country Analysis" `[unverified details — author/year/journal not confirmed]`.
**What is new:** nothing about the existence of a positive association. **Verdict: KNOWN.**

### A2. "Country trends remove the effect" — the econometric critique
This is textbook panel econometrics. Trending regressors and common cross-country factors generate correlations
that disappear under country-specific trends or common-factor estimators; Pesaran's common correlated effects
estimator is the standard fix `[verified URL: Econometrica 2006, jstor.econometricsociety.org]`, and
Eberhardt & Teal's review of cross-country growth empirics makes exactly this fragility argument
`[verified URL: Journal of Economic Surveys 25(1):109-155, 2011, via Scopus record]`. Spurious regression with
trended variables goes back to Granger & Newbold `[unverified]`. The structural-transformation literature the
project borrowed from (Boppart et al., NBER w31101, "The Macroeconomics of Intensive Agriculture",
`[verified URL: nber.org/papers/w31101]`) is about a common latent development factor, not about schooling;
note it is an agriculture paper, so it is a framing source, not a prior education result.
**What is new:** nothing in the method; the result is the standard critique applied to this variable set.
**Verdict: KNOWN.**

### A3. The power-tested version — "cannot be separated from development"
The distinctive addition is methodological: most "it dies under trends" critiques cannot distinguish confounding
from a test too weak to see an effect. This project runs a power simulation on a null world with no effect
(2-4% false positives with trends, 98% without) and an S-curve world with true effects (a 20-point effect caught
in 91% of panels with trends, 49% without), then reports the real-data interval (+0.07 ± 0.19) against that
calibration. I found no paper that pairs a full cross-country link matrix with a purpose-built power simulation
for the trend test and then reports the result as an interval rather than as a null.
**What is new:** the power calibration and the honest interval-based reading; it turns a known critique into a
measured statement about this sample. **Verdict: INCREMENTAL** — the most defensible part of the electricity work.

### A4. The single-specification debunk (+16.05 vs +0.07)
Fragility of a headline estimate across specification choices is the specification-curve / robustness tradition
(Leamer; Sala-i-Martin; Simonsohn et al. — see B). Applying it to a published-looking education-development
estimate is a useful case study, not a new method.
**Verdict: INCREMENTAL (case study).**

---

## B. GROUPING MULTIVERSE AND THE RESOLUTION ARITHMETIC

### B1. Multiverse / specification-curve machinery
Multiverse analysis is Steegen, Tuerlinckx, Gelman & Vanpaemel (2016), "Increasing transparency through a
multiverse analysis" `[verified URL: Crossref record for doi 10.1177/1745691616658637]`; the specification curve
is Simonsohn, Simmons & Nelson (2020) `[unverified URL; Nature Human Behaviour 4:1208-1214]`; the garden of
forking paths is Gelman & Loken `[unverified]`. The grouping dimension is a natural extension of the same logic
to how countries are sliced, and subgroup/heterogeneity analysis is old.
**Verdict: KNOWN components.**

### B2. The random-grouping null
A random repartition of countries with the same group sizes is a permutation/randomisation device: it asks what
chance slicing would produce. The principle is standard in randomisation inference, and permutation p-values have
a known floor of 1/(R+1) when R permutations are drawn — Phipson & Smyth, "Permutation p-values should never be
zero" `[verified URL: zbmath record 6398291]`. Using it as a *calibration yardstick for transportability* (real
groups vs random groups of the same size) is a sensible and, as far as I can see, uncommon framing for
cross-country panels.
**What is new:** the estimable random-grouping yardstick as a transportability test, rather than a
heterogeneity/specification test. **Verdict: INCREMENTAL.**

### B3. The resolution arithmetic (lone link ~5,440 draws; cluster of 30 ~182; 35 certified at 400)
The two ingredients are textbook: the 1/(R+1) permutation floor (Phipson & Smyth `[verified URL]`), and the
Benjamini-Hochberg step-up rule (BH 1995 `[unverified]`). The discrete/floor p-value setting is discussed in the
multiple-testing literature, e.g. "False discovery rate control for grouped or discretely supported p-values"
`[verified URL: idescat.cat SORT article]`. What I could not find is the explicit *design rule*: how many random
draws a multiverse needs depends on how many links pile up at the ceiling — R+1 >= M/(0.05 j) — and the
demonstration that at 400 draws 35 links are certifiable *because* a 30-link floor cluster clears BH, while a lone
link would need ~5,440.
**What is new:** the derivation as a stated resolution rule for random-grouping multiverses, with the empirical
demonstration. It is a packaging of known statistics, but a genuinely useful and apparently unstated one.
**Verdict: INCREMENTAL, border-NEW** — the strongest novelty candidate in the session. Publishable as a methods
note or as the methods section of a paper.

---

## C. CHILD MORTALITY: LEVEL VERSUS VOLATILITY

**The session's claim.** Fertility responds to the slow *level* of child mortality (+0.0067 births per point,
standard error 0.0015, 7,531 country-years, 193 countries) but not to its *volatility* (+0.0020, standard error
0.0020; circular-shift permutation p = 0.29), and the design would have detected a volatility effect as large as
the level effect.

### C1. The level effect — old
The "child survival hypothesis" is old: "The child survival hypothesis", Population Studies 30(2):263-278, 1976
`[verified URL: pubmed.ncbi.nlm.nih.gov/22077806]`, and the broader mortality-decline-precedes-fertility argument
is standard demographic transition theory (Notestein; Davis `[unverified]`). Doepke (2005) tests the
Barro-Becker model against the facts `[verified URL: Springer doi 10.1007/s00148-004-0208-z]`.
**Verdict: KNOWN.**

### C2. The volatility test
The insurance/hoarding motive is old in anthropology/demography (Cain 1981 on risk and insurance in agrarian
settings `[unverified details]`), and mortality uncertainty is formalised in economics (Kalemli-Ozcan, "A
stochastic model of mortality, fertility, and human capital investment", Journal of Development Economics 2003
`[verified URL: ScienceDirect S0304387802000895]`). Nearly all of that evidence is household-level. A
country-level decomposition into level versus volatility, with the correct circular-shift permutation and a
cluster-preserving placebo, appears to be a new application — but it is weak identification for the mechanism it
speaks to.
**What is new:** the country-level discrimination and its null on volatility; the strong caveats are already
stated in the record (common cause not excluded; household insurance not ruled out).
**Verdict: INCREMENTAL.**

---

## D. THE DOSE MODEL AND ITS CORRECTION

### D1. The individuation hypothesis
Caldwell's wealth-flows theory `[unverified]` and the WEIRD programme — Henrich, Heine & Norenzayan, "The
weirdest people in the world?", Behavioral and Brain Sciences 2010 `[verified URL: cambridge.org]` — are the
sources. Tests of Caldwell's mechanism exist `[unverified]`.
**Verdict: KNOWN hypothesis.**

### D2. The out-of-sample result (individuation does not beat development-only)
This is a project-specific modelling comparison (held-out error 24.4 vs 21.1, difference +3.3, 95% interval
-3.8 to +11.1, 3 of 6 countries). It is a real, honest result **for this model**, but it is not a test of the
theory in the field's sense: both scenarios fit badly, the strengths are not identified, and the tolerance is
coarse. Against the literature it is a model-comparison exercise, not new evidence on Caldwell or Henrich.
**Verdict: INCREMENTAL (project result, not field result).**

### D3. The importance-weight collapse (effective sample size ~1 of 600) and its fix
Weight degeneracy in sequential ABC is a well-known pathology; the curse of dimensionality in ABC is standard
(Beaumont et al.; Del Moral et al. `[unverified]`), and ABC calibration of ABMs is an established practice
(Thiele et al. `[unverified]`). The correction (equal-weight rejection sampling) is textbook. What is new is the
*project-level* finding that the previous session's "the data cannot identify the mechanism" was an arithmetic
artefact.
**Verdict: KNOWN caution; the correction is a valuable internal audit, not a new method.**

---

## E. THE FULL TRANSITION IN THE GPU ABM (pending)

### E1. Simulating the demographic transition
Modelling the transition from high to low mortality and fertility is one of the oldest exercises in demography
(Notestein 1945; Davis 1945 `[unverified]`; unified growth theory, Galor & Weil, American Economic Review
90(4):806-828 `[verified URL: pubs.aeaweb.org/doi/pdf/10.1257/aer.90.4.806]`). Individual-level historical
microsimulation is also old: SOCSIM was developed at UC Berkeley in the 1970s and is still used
`[verified URL: National Academies NAP chapter; Wiley PDR supplement]`.
**Verdict: KNOWN question and known simulation tradition.**

### E2. Running it at population scale on a GPU with a mortality counterfactual
GPU agent-based simulation is an established field (FLAME GPU 2 `[verified URL: docs.flamegpu.com]`), and
agent-based models of historical populations predate GPUs. The plausible novelty is the *combination*: an
individual-level ABM calibrated to a real country panel, run across the pre-antibiotic-to-collapse arc at
millions of women, with a counterfactual that holds mortality at its pre-antibiotic level to ask whether the
fertility collapse survives. If that runs and validates, it is a new demonstration — a "computational
counterfactual" — not a new theory.
**Verdict: potentially NEW as a demonstration (pending); INCREMENTAL otherwise. This is the one result that could
carry a novelty claim beyond methods.**

---

## F. OTHER CANDIDATES

### F1. Circular-shift permutation for slow-moving series
Known: permutation tests for dependent data must preserve dependence structure (block/circular permutation),
e.g. "Permutation tests and bootstrap tests for dependent data" `[verified URL: arXiv 2512.17372]`; the
year-shuffle test is anti-conservative for serial correlation. The session used it correctly and killed two
results with it.
**Verdict: KNOWN method, correct application.**

### F2. Naive value-scramble placebo is invalid
Same principle: scrambling breaks the dependence that the clustered standard error relies on. Known.
**Verdict: KNOWN.**

### F3. Gap-filling and controls robustness
Multiple-imputation pitfalls, and the "controls that change the sample rather than the estimate" decomposition,
are standard applied-econometrics warnings. The three-way labelling (coverage-driven / imputation-driven /
genuine) is a good practice, not a discovery.
**Verdict: KNOWN practice, well executed.**

### F4. The GPU engine itself
An engineering artefact: exact against its own reference, 5.8 million women per second, ~10 million women per
launch. Genuinely useful capability; not a scientific finding.
**Verdict: NEW capability (engineering), not a scientific claim.**

---

## The three strongest novelty claims

1. **The multiverse resolution arithmetic** (B3). A stated design rule for how many random groupings a
   transportability multiverse needs, derived from the permutation floor and BH's step-up property, with an
   empirical demonstration that a floor cluster can certify links while a lone link cannot. Apparently unstated in
   this form. Publishable as a methods contribution.
2. **The power-calibrated trend audit of cross-country education-development links** (A3). The critique is old,
   but pairing the full link matrix with a purpose-built power simulation and reading the result as an interval
   ("cannot separate from development at this power") rather than a null is a real increment — and the single
   specification behind +16.05 is a clean cautionary case.
3. **The full-transition GPU counterfactual** (E2), if it lands and validates: an individual-level, population-scale
   simulation of the whole transition with a no-mortality-decline counterfactual. New as a demonstration, not as a
   theory.

## The three weakest claims (do not present these as discoveries)

1. **"Electricity does not drive schooling."** Trending-regressor/common-factor critique is textbook; the
   micro literature on electricity and education is large and mostly positive. We have shown the cross-country
   association is not separable from development at this power — a replication of a known econometric warning.
2. **"Child survival drives fertility."** The child-survival hypothesis is fifty years old (1976 Population
   Studies); our contribution is a country-level level-versus-volatility discrimination, which is incremental.
3. **"Individuation loses to development-only."** That is a result about one model with poor fit and unidentified
   strengths, not a field-level verdict on Caldwell or Henrich. Present it as a model comparison, never as
   evidence that the individuation hypothesis is false.

## What the honest paper should claim — and explicitly not claim

**Claim:** (i) a methods contribution on multiverse resolution; (ii) a power-calibrated fragility audit of
cross-country education-development links, with the +16.05 specification as the case study, concluding "not
separable from development at this power"; (iii) if it validates, a GPU full-transition counterfactual as a
demonstration. Optionally (iv) a country-level level-versus-volatility result, framed as suggestive and limited.

**Do not claim:** that electricity does not matter; that mortality decline is *the* cause of fertility decline;
that individuation is refuted; that the GPU engine is a bit-exact rerun of the published model; that any of this
is causal identification; or "first" anywhere — use "we are not aware of".

## Plain-language summary for Dr. Menefee

Most of what we found today is **not new to the world** — it is new to us, or a careful replication. The claim
that electricity stops predicting schooling once each country's own trend is allowed is the standard
econometric warning about trending variables and common development, dressed in our data; the micro literature
on electricity and education is large and generally finds positive effects, so we should not tell anyone
electricity does not matter. The claim that child survival drives fertility is fifty years old; our addition is
a modest country-level test that it is the *level* of child mortality, not its year-to-year riskiness, that
matters. The individuation-versus-development result is a statement about one model that fits poorly, not a
verdict on the theory.

What is arguably new: a small piece of statistical bookkeeping about how many random groupings a multiverse
needs to be able to certify anything (a lone finding needs thousands of draws; a cluster of extreme findings
needs far fewer), the honest, power-calibrated way we reported the development-driven null, and — if it works —
running the whole demographic transition, from before antibiotics to the fertility collapse, inside the
individual-level model on a graphics card, with a counterfactual that removes the mortality decline. That last
one is the only candidate for a genuinely new scientific demonstration.
