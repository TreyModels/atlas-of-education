# Section 4. The survey-level gradient: what DHS says about schooling and completed fertility, and what it cannot say

*Draft section for Paper F. Source: `research/dhs-micro-2026-11-23` @ `31ded00`; record
`research/records/2026-11-23-dhs-micro/` (`README.md` §1-2, `results/model_education.json`,
`results/cohort_gradients.csv`, `results/survey_gradients.csv`).*

## 4.1 The question, and the data gap stated first

The between-country gradient of Section 4 is a country-level object. The literature that most demographers
have in mind when they say "education lowers fertility" is an individual-level object: within a population,
women with more schooling have fewer children. The two can differ in size and even in sign, and the difference
is the ecological fallacy in its most consequential form (Robinson, 1950). This section asks what the
Demographic and Health Surveys — the standard source for the individual-level claim — can add, and it begins
with a limitation that must not be buried: **the pre-registered individual-level test could not be run.** DHS
women's Individual Recode files are not publicly downloadable; the public API exposes indicator aggregates and
a file inventory but no download link, the flat files sit behind a registered account, IPUMS-DHS requires a key,
and the project's local data store contains no DHS microdata. Every attempt is logged in the record's
`data/microdata_probe.txt`. What can be analysed, and is analysed here, are the DHS's **published cells**: mean
children ever born to women aged 40-49 by education, mean age at first birth by education, and the wealth and
residence breakdowns — 81,962 published cells from 377 surveys in 87 countries, 1985-2025. The unit is a
country × survey × education cell, not a woman. Every claim in this section is therefore a **survey-level
(ecological) claim**, and the section labels it as such throughout.

## 4.2 The gradient is large, monotone, and almost universal

Within country × survey, with cell weights (the number of women each published cell represents) and standard
errors clustered by country, completed fertility falls monotonically with education relative to no education:
primary education **−0.57 children (SE 0.06)**, secondary **−1.62 (0.17)**, higher **−2.54 (0.24)**. The sample
is 1,291 education cells from 86 countries, median 401 women per cell. The per-survey gradient — secondary or
higher minus none/primary — is negative in **99 per cent of 346 surveys**, with a median of **−1.90 children
(IQR −2.48 to −1.43)**. On these data the canonical gradient is about as universal as a social-science
regularity gets, and it is large in the units that matter: nearly two children between women with secondary
schooling and women with none, within the same survey.

This is the survey-level counterpart of Section 4's country-level gradient, and the two agree in sign and
importance. A country with more schooling has fewer births, and within a country women with more schooling have
fewer children. The agreement is reassuring for the descriptive claim; it does not resolve the causal question,
and the rest of this section explains why not.

## 4.3 The dynamic predictions were contradicted

The project pre-registered two dynamic predictions for the survey data, both grounded in the massification
story: the gradient should *steepen* in later cohorts (as schooling becomes a stronger marker of the modern
sector) and should steepen where the education pipeline is denser (the "pipeline-density" prediction). Both were
**contradicted**, and the record reports the contradiction rather than re-spinning it.

On cohorts: the education × cohort interaction is **positive** — the gradient *flattens* over time — at
**+0.26 children per decade (SE 0.13)** for secondary and **+0.40 (0.16)** for higher education. The
cohort-specific median survey gradients trace the same attenuation: 1940s **−2.50** (48 surveys), 1950s
**−1.90** (78), 1960s **−1.85** (122), 1970s **−1.80** (95), 1980s **−1.50** (3). On pipeline density: the
interaction with the survey's own share of women with secondary or higher is also **positive** — the gradient is
*shallower* where schooling is more massified: **+0.13 (SE 0.05)** per ten percentage points for secondary and
**+0.16 (0.05)** for higher education, with median per-survey gradients of **−2.10** (low pipeline tercile),
**−2.00** (middle), and **−1.60** (high). The gradient is negative in **every** pipeline tercile; the direction
is universal, the magnitude is not, and the magnitude moves opposite to the pre-registered prediction.

The most likely reading is composition, and the record says so: "secondary education" is a small elite in early
cohorts and a mass phenomenon later, so the same label spans very different amounts of schooling and different
selection. The survey cells cannot separate composition from a genuine change in the education-fertility
relationship; the individual birth histories that could are the data that were not obtainable. This is the C
label — cannot be tested with these data — applied to the most interesting version of the question.

## 4.4 Delay and number cannot be separated here either

The same cells allow a quantum-versus-tempo comparison that the record reports as suggestive, not decisive.
Secondary education is associated with a median age at first birth **+2.65 years (0.15)** later than no
education, and higher education **+5.27 (0.39)** later, while completed fertility is 1.62 and 2.54 children
lower. Both a delay and a lower final number are present, and the published cells cannot say how much of the
fertility difference is tempo (later starts, possibly caught up) and how much is quantum (fewer births). With
1,291 cells, 333 surveys, and 86 countries, the delays are precisely estimated; the decomposition between delay
and number needs birth histories. The paper therefore treats the DHS section as evidence that the survey-level
gradient is real and universal, and not as evidence about its mechanism.

## 4.5 What the section does and does not add to the synthesis

What it adds: an independent, survey-based confirmation that the schooling-fertility gradient is negative and
large at the education-cell level across 86 countries and four decades of surveys, which rules out the
possibility that Section 4's country-level gradient is an artefact of national aggregates; and a set of
*negative* results — cohort attenuation and pipeline attenuation in the opposite direction from the
pre-registered predictions — that matter for the massification interpretation. If the gradient were purely a
development-level marker, one might expect it to weaken as schooling spreads; the survey data show exactly that
attenuation (from −2.50 in the 1940s cohorts to −1.80 in the 1970s), which is a finding worth reporting in its
own right. It does not uniquely support the development-gradient reading, because saturation, composition change
and ceiling effects would produce attenuation too, and the composition caveat means it cannot be stated as an
individual-level fact. What it does not add: the individual-level test, the wealth horse-race, the community placebo, and the
quantum/tempo decomposition, all of which require microdata. The record states the data gap and the manual
download procedure (a free DHS account, dataset-access request, Individual Recode Stata files, and the
specified variables) rather than substituting country aggregates for the missing test. A synthesis that claimed
the survey-level gradient settled the individual-level question would be committing the same ecological error
it criticises in Section 4.
