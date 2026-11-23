# Paper N2 — claims-prior-art, centered on the levels-versus-changes claim

**Centerpiece verdict (literature auditor, novelty-review e51c4cf): INCREMENTAL — new assembly, not a
new fact or method.** The within/between move is known; the aggregation critique is known; what the
auditor could not find is a paper that shows the country-level schooling–fertility correlation
vanishing under the standard within-change specification, quantified across thousands of country
partitions with a purpose-built placebo. This file records the closest prior work, the search
strategy, what is replicated and what is new. The paper must be framed as an audit, never a
discovery, and no "first" claim is made.

## Search strategy (recorded)
1. **Auditor memo and claims map.** The independent literature auditor (novelty-review) supplied a
   centered prior-work memo (commit e51c4cf) and an earlier claims map for the session's fertility
   and massification claims (`research/records/2026-11-24-lit-audit/claims-map.md`, branch
   `research/lit-audit-2026-11-24`, commit 0bcd33f). Those lists are the starting point; this file
   adds the schooling–fertility both-ways works and the transportability literature the auditor
   flagged as mandatory.
2. **Crossref.** Every entry below was checked against `api.crossref.org` (polite `mailto`): direct
   DOI lookup where a DOI was known, otherwise `query.bibliographic` with the top two hits inspected
   for title/author/year/venue agreement. Status: **V** = DOI resolved directly, title/author/year
   match; **S** = Crossref bibliographic match, not re-opened; **U** = no DOI located in-session;
   **N** = book/report/unpublished, no DOI. No citation was invented; items that could not be
   verified are marked and are not used as evidence.
3. **Queries used.** "levels vs changes demographic transition"; "within-country schooling fertility
   change"; "ecological fallacy aggregation"; "growth empirics heterogeneity"; "vibration of effects
   model specification"; "multiverse analysis"; "schooling fertility natural experiment"; author
   searches for Robinson, Nickell, Durlauf, Eberhardt–Teal, Steegen, Simonsohn, Patel, Caldwell,
   Bongaarts, Kravdal, Liu–Raftery, Herzer–Strulik–Vollmer, Murtin, Barro–Lee, Pritchett, Duflo,
   Chicoine.

## The closest competitor, named

**Liu and Raftery (2020, PDR 46(3), DOI 10.1111/padr.12347)** — country-level education–fertility
modelling with explicit between-country structure. It is the closest prior work because it models the
education–fertility relationship at the country level and takes the between-country structure
seriously. **Why ours differs:** Liu–Raftery estimate the level relationship and build a
projection/model around it; they do not decompose the same measures into level and within-change
estimates, they do not quantify transportability across thousands of country partitions, and they do
not run a future-schooling placebo. They are a modelling competitor for the *level* claim, not for
the audit.

**Kravdal (2002, Demography 39(2), DOI 10.2307/3088337)** — individual and community effects of
education on fertility in sub-Saharan Africa. Closest prior work on the **level-of-analysis problem**
in this literature: it separates a woman's own education from the education of her community.
**Why ours differs:** Kravdal works at the individual/community level with survey data; we work at the
country-panel level and ask whether the country-level gradient survives the within-country change
design. The two are complementary and must be reconciled in the paper, not treated as rivals.

## Claim 1 — The within/between (level-of-analysis) distinction is known

| work | DOI | status | why it matters / new vs replicated |
|---|---|---|---|
| Nickell (1981), *Biases in dynamic models with fixed effects*, Econometrica 49(6) | 10.2307/1911408 | V | **Replicated:** the fixed-effects bias critique; our change estimate does not include a lagged dependent variable, but the finite-sample concern is acknowledged. |
| Angrist & Pischke (2009), *Mostly Harmless Econometrics* | 10.1515/9781400829828 | S | Replicated: the standard teaching of what fixed effects remove; our paper uses it, adds nothing. |
| Durlauf, Johnson & Temple (2005), *Growth econometrics*, Handbook of Economic Growth | 10.1016/s1574-0684(05)01008-7 | V | Replicated: the levels-versus-growth distinction in cross-country work. |
| Eberhardt & Teal (2011), *Econometrics for grumblers*, Journal of Economic Surveys 25(1) | 10.1111/j.1467-6419.2010.00624.x | V | Replicated: cross-country level regressions can reflect common factors and trends; the closest methodological warrant for the audit. |
| Robinson (1950), *Ecological correlations and the behavior of individuals*, ASR 15(3) | 10.2307/2087176 | V | Replicated: the aggregation critique; the paper's scope limitation. |

**New vs replicated.** All replicated. The paper's methodological content is older than the paper.

## Claim 2 — The schooling–fertility gradient has been estimated both ways, but not decomposed in one place

| work | DOI | status | why it matters / new vs replicated |
|---|---|---|---|
| Caldwell (1980), *Mass education as a determinant of the timing of fertility decline*, PDR 6(2) | 10.2307/1972729 | V | **The strongest opposing account:** mass schooling as a determinant. Must be engaged, not omitted. Replicated: this is the causal reading the audit tests. |
| Bongaarts (1978), *A framework for analyzing the proximate determinants of fertility*, PDR 4(1) | 10.2307/1972149 | V | Replicated: schooling as a proximate/contextual determinant. |
| Bongaarts & Watkins (1996), *Social interactions and contemporary fertility transitions*, PDR 22(4) | 10.2307/2137804 | V | Replicated: context-dependence of fertility transitions. |
| Cleland & Rodríguez (1988), *The effect of parental education on marital fertility in developing countries*, Population Studies 42(3) | 10.1080/0032472031000143566 | V | Replicated: the individual gradient benchmark; the ecological-fallacy constraint. |
| Martin & Juárez (1995), *The impact of women's education on fertility in Latin America*, IFPP 21(2) | 10.2307/2133523 | V | Replicated: mechanisms versus spuriousness — the paper's framing question in the 1990s. |
| Basu (2002), *Why does education lead to lower fertility?*, World Development 30(10) | 10.1016/s0305-750x(02)00072-4 | V | Replicated: critical review of mechanisms; a referee will ask why the macro null does not contradict them. |
| Kravdal (2002), *Education and fertility in sub-Saharan Africa: individual and community effects*, Demography 39(2) | 10.2307/3088337 | V | **Closest level-of-analysis competitor** (see above). |
| Kravdal (2012), *Further evidence of community education effects on fertility*, Demographic Research 27 | 10.4054/demres.2012.27.22 | V | Replicated: context changes the gradient. |
| Barro & Lee (2013), *A new data set of educational attainment in the world, 1950–2010*, J Dev Econ 104 | 10.1016/j.jdeveco.2012.10.001 | S | Replicated: the attainment series behind cross-country work. |
| Pritchett (2001), *Where has all the education gone?*, World Bank Economic Review 15(3) | 10.1596/17434 | S | Replicated: schooling's returns are not automatic; the same caution for demographic returns. |
| Duflo (2001), *Schooling and labor market consequences of school construction in Indonesia*, AER 91(4) | 10.1257/aer.91.4.795 | S | **The design that could make the audit causal** (natural experiment on expansion). |
| Chicoine (2016), *Free primary education, schooling, and fertility: evidence from Ethiopia*, SSRN working paper | 10.2139/ssrn.2879794 | S | The other natural-experiment design; working-paper version only. |
| Lutz, Butz & KC (eds.) (2014), *World Population and Human Capital in the Twenty-First Century*, OUP | 10.1093/acprof:oso/9780198703167.001.0001 | S | Replicated: education as a driver in demographic projections. |
| Herzer, Strulik & Vollmer (2012), *The long-run determinants of fertility: one century of demographic change 1900–1999*, J Econ Growth 17(4) | 10.1007/s10887-012-9085-6 | V | Replicated: long-run cross-country determinants; a modelling competitor on the level relation. |
| Murtin (2013), *Long-term determinants of the demographic transition, 1870–2000*, REStat 95(2) | 10.1162/rest_a_00302 | V | Replicated: historical cross-country determinants; the closest historical competitor. |
| Liu & Raftery (2020), *How do education and family planning accelerate fertility decline?*, PDR 46(3) | 10.1111/padr.12347 | V | **Closest overall competitor** (see above). |

**New vs replicated.** The gradient and its both-ways estimates are replicated. **New (assembly):** the
same eight measures estimated with both level and within-change specifications on the same panel, the
13,800-partition transportability audit, and the future-schooling placebo with a pre-registered
decision rule. The auditor's verdict — new assembly, not new fact or method — is adopted verbatim.

## Claim 3 — Aggregation, heterogeneity and transportability are known problems

| work | DOI | status | why it matters / new vs replicated |
|---|---|---|---|
| Brock & Durlauf (2001), *Growth empirics and reality*, World Bank Economic Review 15(2) | 10.1596/17447 | V | Replicated: a pooled coefficient may be an average no country has; the warrant for the transportability audit. |
| Pearl & Bareinboim (2011), *Transportability of causal and statistical relations*, IEEE ICDMW | 10.1109/icdmw.2011.169 | V (auditor-verified) | Replicated: formal transportability; a methods referee may ask for this framing. Our partitions are a sensitivity universe, not formal transportability. |

**New vs replicated.** Replicated. Our contribution is the quantified map for this specific gradient,
not the concept of transportability.

## Claim 4 — Multiverse / vibration-of-effects reasoning

| work | DOI | status | why it matters / new vs replicated |
|---|---|---|---|
| Steegen, Tuerlinckx, Gelman & Vanpaemel (2016), *Increasing transparency through a multiverse analysis*, Perspectives on Psychological Science 11(5) | 10.1177/1745691616658637 | V | Replicated: the multiverse frame. |
| Simonsohn, Simmons & Nelson (2020), *Specification curve analysis*, Nature Human Behaviour 4 | 10.1038/s41562-020-0912-z | V | Replicated: specification-curve reporting. |
| Patel, Burkhart & Ioannidis (2015), *Assessment of vibration of effects due to model specification*, Journal of Clinical Epidemiology 68(9) | 10.1016/j.jclinepi.2015.05.029 | S | Replicated: the vibration-of-effects framing used for the 6,174-cell grid. |
| Gelman & Loken (2014), *The statistical crisis in science / garden of forking paths* | no DOI (unpublished/online) | N | Context only; cited as the familiar statement of the problem, not as evidence. |
| Klau et al. (multiverse analysis) | not located with a verified DOI in-session | U | **Not cited as evidence.** The auditor's list included a Klau multiverse reference; no unambiguous DOI was verified, so it is recorded here as a search gap rather than cited. |

**New vs replicated.** Replicated. Our extension is applying the logic to the country set (partition
transportability) rather than only to specifications.

## What is new, what is replicated, and the honest summary

- **Replicated:** the ecological-fallacy critique; the within/between distinction and the
  fixed-effects literature; the multiverse/vibration-of-effects machinery; the schooling–fertility
  gradient itself (levels) and its individual-level counterpart (Cleland–Rodríguez; Kravdal);
  evidence that
  cross-country level regressions can be fragile (Eberhardt–Teal).
- **New assembly:** the eight schooling–fertility pairs estimated both ways on the same panel; the
  13,800-partition transportability audit; the future-schooling placebo at 90% strength with a
  pre-registered decision rule; the explicit distinction between a development gradient and a causal
  lever, applied to how the field reports these estimates.
- **Not new, and the paper does not claim it:** a new method, a new correlation, or a "first"
  demonstration of levels-versus-changes. The auditor's verdict is INCREMENTAL, and the paper's
  framing (audit, not discovery) follows it.

## Unverifiable or missing citations (recorded, not fabricated)
- **DHS individual-gradient comparison:** not estimated in this record (data gap). The paper scopes
  its claims to aggregates and cites Cleland & Rodríguez (1988), Basu (2002) and Kravdal (2002, 2012)
  for the individual gradient rather than estimating it.
- **Klau et al. (multiverse):** no DOI verified; not cited.
- **Gelman & Loken (2014):** no DOI; cited only as context, marked N.
- **Auditor memo:** novelty-review e51c4cf; its prior-work list is incorporated above. Any later
  auditor additions can be inserted without changing the claims.
