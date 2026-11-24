# Schools before factories: schooling, structural change and the sequencing of massification in late-industrialising countries

**Draft synthesis — Paper M of the Atlas of Education project. Working paper, 25 November 2026.**
Not for circulation outside the project until the verification pass is complete. Every number in the text is
traceable to a project record at a named branch and commit (the claims-to-source map is a separate file); the
literature claims are DOI-verified in `claims-prior-art.md` and `refs.md`; the historical dates are labelled
verified or unverified throughout.

---

## Abstract

Most theories of mass schooling are demand stories. This paper is built around one ordering claim, stated before the theory: in late-industrialising countries, the schooling take-off typically precedes the release of agricultural labour, and the structural-change proxies the demand story names do not usually turn on first. Families invest in education because returns rise, employers demand literate workers, and the labour market pulls children through school. In a panel of 64 late-industrialising countries where both events can be dated, the schooling take-off **precedes** the release of labour out of agriculture in 61 of them (95%), with a median lead of 26 years (bootstrap 95% interval 22–26 years); the reverse ordering occurs in 5% (0–11%). On pre-1990 structural-change series the demand take-off precedes the schooling take-off in **10.0%** of identifiable countries (GGDC non-agricultural employment), **15.4%** (urbanisation), **24.1%** (industry value added) and **18.8%** (agricultural value added); all-country bounds are **6.7–53.0%**, and another **21–43%** are weak ties or left-censored. Demand is neither eliminated nor cleanly ordered: the honest summary is that **schooling and structural change move together, with schooling typically but not universally first**. In a horse race with country and period fixed effects, supply-side measures carry the association with schooling expansion (+0.456, SE 0.174) while demand-side measures do not (+0.006, SE 0.203; n=78 country-periods, 51 countries). The raw event ordering looks demand-led (73% of countries, 64–82%), but that is an artefact of when the series begin: 61 of 108 schooling take-offs sit on the first observable year of the common window, and the supply series start in the median country only in 1975; in the fair sample (33 countries) supply precedes schooling in 76% and demand in 79%, and the two sides turn together. One supply-side shock can be tested with an event study: fee abolition in eight African countries with verified dates (1994–2005) is followed by large primary-enrolment gains (Callaway–Sant'Anna post-effects of roughly +22 to +29 points at +1 to +6, TWFE similar, flat pre-trends at −2/−3/−4); the on-impact effect includes zero, the treated sample is small (7 countries), and it is **consistent with** a supply effect, not a causal estimate. The historical record splits: Prussia's compulsory schooling state precedes industrialisation and the farm exodus by 80–120 years; France's 1833 statute precedes but attainment follows demand until the 1880s; in Britain — the first industrialiser — industrialisation and the farm exodus precede mass schooling by 40–90 years; the northern United States is supply-side in the local-public-goods sense. We read the evidence as a **late-industrialiser regularity, not a universal law**, and as an association rather than a causal sequence: where the state built the pipeline first, schooling typically led; where industrialisation came first, demand led. The paper also reports the agricultural-floor mechanism (real in the cross-section, not identified in the dynamics), scaling regularities that are between-country regularities rather than laws of change, and credential and care mechanisms unsupported in the data they can be tested on. Data tiers are labelled throughout: GGDC/WDI/PWT structural-change and enrolment series are **observed**; the long-run schooling event series is **reconstructed**; the WDI total-fertility series is **observed** (births per woman) and is not the project's effective-fertility measure. The contribution is a systematic, pre-registered, multi-country **event-ordering** of massification against structural change, joined to the historical cases, with the demand-side theory's own variables given a fair test.

**Keywords:** mass schooling; structural transformation; compulsory education; supply-side schooling expansion;
event sequencing; late industrialisation.

---

## 1. Introduction
The central fact of modern social history is that whole populations became literate and schooled within about
a century and a half, and that the process began at very different income levels and at very different times.
The standard economic explanation is that schooling is an investment: families and governments buy it because
returns to skill rise, first with industrialisation and then with technological change (Schultz 1961;
Becker 1964; Mincer 1958, 1974; Goldin and Katz 2008; Acemoglu and Autor 2011). On this account mass schooling
is, at bottom, a response — to factories, to cities, to the demand for numerate and literate labour. The
sociological alternative, associated with the world-polity tradition, has argued the opposite: that mass
education is an institutional project that spreads through states and international organisations largely
independently of local economic demand (Meyer 1977; Boli, Ramirez and Meyer 1985; Ramirez and Boli 1987;
Benavot and Riddle 1988; Soysal and Strang 1989; Meyer, Ramirez and Soysal 1992; Schofer and Meyer 2005). The
two accounts make different predictions about **timing**. Neither the direction nor the case material is new: Sandberg (1979) called pre-industrial Sweden the "impoverished sophisticate" because it had mass literacy before industrialisation; Mitch (1992) traced English literacy rising before the factory system; the world-polity school has argued since the 1980s that mass schooling is supply-led and spread by institutional imitation rather than industrial demand (Boli, Ramirez and Meyer 1985; Ramirez and Boli 1987); Squicciarini and Voigtlaender (2015) and de Pleijt and van Zanden (2016) show upper-tail human capital leading European industrialisation; and Graff (1979/2017) is the sceptical classic. What has not been assembled, as far as our recorded search can find, is a common, pre-registered event comparison across a large country panel with the demand variables the human-capital theory names given a fair test alongside the supply variables. The closest competitor in spirit is Porzio, Rossi and Santangelo (2021), who argue that human capital accumulation drives structural transformation: consistent in direction with our ordering, but their design is a quantitative model with micro evidence on skill reallocation, not a cross-country event comparison, and the two claims are complementary rather than competing. The claim is about systematic measurement, not the direction of the historical pattern. If schooling is demand-led, labour-market demand must
turn on before school systems expand. If schooling is an institutional/supply project, school systems can be
built before the labour market demands the graduates.

This paper tests the timing prediction directly and at scale. We assembled, from the project's country panel
and its long-run historical sources, a set of comparable **event dates**: the take-off of schooling (the first
sustained rise in a national schooling series, or the first enforced national schooling statute), the release
of labour out of agriculture (the first sustained fall in the agricultural employment share), and the onset of
the supply-side and demand-side conditions that the competing theories say should precede them. We fixed the
definitions, the windows, the thresholds and the verdict rules **before** assembling the dates (project
pre-registrations, listed in the claims-to-source map), and we report the consequences even when they contradict
the framing that motivated the exercise. The result is a systematic event-ordering of massification against
labour-market demand — to our knowledge, and we say this cautiously, a comparison that has been argued case by
case in the historical literature but has not been assembled as a common, pre-registered event comparison
across late-industrialising countries.

**The finding, in one paragraph.** Among 64 countries where all three events can be dated in a common 1965–2010 window, schooling precedes agricultural labour release in 61 (95%; release-first 5%, bootstrap 95% interval 0–11%), with a median lead of 26 years (22–26). Schooling also precedes the fertility decline in only 37.5% of those countries under a strict ordering (26.6–50.0%; 31.3% simultaneous, 31.3% fertility-first; the source JSON's 68.75% counted ties as schooling-first and is not used). The raw supply-versus-demand event comparison looks demand-led (73% of 89 countries, 64–82%; supply 28%, 19–37%) but is contaminated by data availability — 61 of 108 schooling dates sit on the window's first year and the supply series begin in the median country only in 1975; in the fair sample of 33 countries supply precedes schooling in 76% and demand in 79%, so the two sides turn together. The horse race puts the conditional association on supply (+0.456, SE 0.174) against demand (+0.006, SE 0.203; n=78, 51 countries), with enrolment capacity (+0.307) and education spending (+0.125) individually significant and every demand measure null. On pre-1990 structural-change series, demand-first is 10.0–24.1% of identifiable countries, bounds 6.7–53.0%, another 21–43% weak ties or left-censored: **schooling and structural change move together, with schooling typically but not universally first.**

**Why the historical cases matter.** Four cases where the sequence can be followed against a century of
scholarship resolve the apparent contradiction and make the paper's framing. In **Prussia**, the compulsory
schooling state (1763 General-Landschul-Reglement, the 1794 Landrecht, the 1812 Hardenberg edict) precedes both
industrialisation and the farm exodus by 80–120 years: the strongest case of state supply running ahead of demand. In **France**, the supply
statute (Guizot 1833) precedes, but measured attainment lags until the Ferry laws of 1881–82, which arrive with
the farm exodus: statute-led, attainment demand-following. In **Britain**, the first industrialiser, the
industrial revolution and the agricultural exodus precede national mass schooling by 40–90 years: the classic
demand-led counterexample, and the case where the theory should have needed the least state supply. The
**northern United States** is supply-side in the local-public-goods sense: locally financed common schools
precede the national farm exodus, while the high-school movement (1910–40) coincides with it. These dates are
standard literature dates, and in this paper **every one of them is labelled UNVERIFIED literature standard**
— we have not re-read the primary sources in this pass; the primary series that would settle them are named so a
future pass can.

**The argument, stated carefully.** The evidence does not support "the labour market causes mass schooling" as a
general account of late industrialisation, and it does not support "schooling causes the release of labour"
either: our event data are period data, not linked cohort histories, and the horse race is a conditional
association, not an identified causal effect. The defensible claim is narrower and it is the paper's thesis:
**in late-industrialising countries, mass schooling and structural change moved together, with the schooling
take-off typically — but not universally — first, and the strict demand-first ordering limited to 10–24% of
identifiable countries; this is a late-industrialiser regularity, not a universal law.** The historical cases
show that the pattern is associated with who supplied the schooling, not that supply caused massification: the
demand-led account is the better description of the first industrialiser, and supply-side construction the
better description of the late industrialisers. The paper is explicit about which parts are replicated from the
existing literature, which parts are new in this assembly, and which parts the data cannot decide.

**Roadmap.** Section 2 states the finding and the claim discipline; Section 3 reviews the literature around the question the finding raises; Sections 4-8 develop the evidence (data, strategy, sequencing, supply versus demand, historical typology); Sections 9-11 report the supporting evidence (agricultural floor; scaling and drivers; credential and care); Section 12 draws the implications for the debate, the classic cases and policy; Section 13 sets out the future research; Section 14 collects the synthesis; Section 15 lists the limitations including the central vulnerability; Section 16 concludes.

Two reading conventions. First, **every number carries its sample and its uncertainty**; where a number comes from a project record, the claims-to-source map at `claims-to-source-map.md` gives branch, commit, file and field. Second, the paper does not claim to be first at anything. The components — mass schooling often running ahead of economic demand in Europe, Prussia as a schooling state before an industrial one, Britain industrialising before it schooled, agriculture's decline as structural transformation's core — are established; what is new is the assembly: a common pre-registered event comparison, a horse race between measured supply and demand, and a joint reading of the cases and the panel under one rule.


## 2. The finding
The paper is built around one ordering claim, and it is worth stating plainly before the literature, the data or
the qualifications. In the 64 late-industrialising countries where the three events — the take-off in schooling,
the release of labour out of agriculture, and the fertility decline — can all be dated in the common 1965-2010
window, **the schooling take-off precedes the release of agricultural labour in 61 countries (95.3%)**, with a
median lead of **26 years** (bootstrap 95% interval for the median 22-26 years; interquartile range 16-29 years across all 64 gaps (17-29 years across the 61 forward cases)). The reverse ordering — the farm exodus first, which is what the demand-led
account requires — occurs in **3 countries (4.7%; bootstrap 95% interval 0-11%)**. The schooling take-off also
precedes the fertility decline in **37.5%** of the same countries under a strict ordering (95% interval 26.6-50.0%; 31.3% simultaneous, 31.3% fertility-first; the source record's JSON reported 68.75% by counting the simultaneous cases as schooling-first, and that figure is not used). The result is not carried
by one region: Latin America, South Asia, East Asia, North Africa and Sub-Saharan Africa are all represented
among the forward cases.

**The demand side, measured on series that go back before 1990, is not ruled out.** The retired "7%" figure was computed on the 1991-start wage-employment and paid-employment series and is not used here: its apparent demand-last ordering is a data-start artefact, not evidence about demand. On pre-1990 structural-change series (GGDC non-agricultural employment from 1947/1950, WDI urbanisation and sector value added from 1960), the demand take-off precedes the schooling take-off in **10.0%** (GGDC), **15.4%** (urbanisation), **24.1%** (industry value added) and **18.8%** (agricultural value added, falling) of identifiable countries; all-country bounds are **6.7–53.0%**, and a further **21–43%** sit in weak ties or are left-censored at the first observable year. Demand-first is therefore a minority strict ordering, but neither eliminated nor cleanly distinguished from ties: **schooling and structural change move together, with schooling typically but not universally first.** The horse race in ten-year changes with country and period fixed effects puts the conditional association on the supply side (**+0.456, SE 0.174**, against **+0.006, SE 0.203** for demand; n=78, 51 countries), with enrolment capacity (+0.307, SE 0.146) and education spending (+0.125, SE 0.058) individually significant; the raw demand-first appearance of the broad proxies is a data-availability artefact covered in Section 7.2. This is a decomposition, not a test, and it does not establish that demand is absent.

**The classic cases show why the regularity is conditional, not universal.** Prussia is the paradigm case of
state supply: compulsory schooling from 1763, near-universal enrolment by the 1860s, industrialisation from the
1840s-70s — schooling ahead of industrialisation and the farm exodus by **80-120 years**. Britain is the
counterexample: the industrial revolution and the agricultural exodus precede national mass schooling by
**40-90 years**, and the 1870 Education Act arrives after the economy had already been transformed. France sits
between the two: the Guizot statute of 1833 precedes the farm exodus by half a century, but measured attainment
lags until the Ferry laws of 1881-82 arrive with it. The northern United States is supply-side in the
local-public-goods sense: publicly funded common schools from the 1830s precede the national farm exodus, while
the high-school movement (1910-40) coincides with it. **Every historical date is UNVERIFIED literature standard**
— a standard secondary date that this pass did not check against a primary source — and the paper says so wherever
the dates appear.

**The claim is an ordering claim, not a new correlation.** The negative association between schooling and
fertility, the positive association between schooling and income, and the rise of mass education are among the
most replicated facts in social science; nothing in this paper claims to discover them. The paper's claim is
that the **order of events** in late-industrialising countries is, in most but not all identifiable cases, the
opposite of what a general demand-led account predicts, that this ordering had not been assembled as a common,
pre-registered, cross-country event comparison before this project (as far as our recorded search can find; the
search is documented), and that the ordering is associated with who supplied the schooling — a state-built
pipeline first in Prussia, a market first in Britain. The contribution is the systematic measurement of a pattern
that has been argued case by case for decades, plus the decomposition that shows the conditional association
sitting with supply measures rather than the narrow labour-market demand variables, plus the demonstration that
the strongest demand-side mechanism (the agricultural floor) does not deliver the sequence the theory needs.

**What the finding does not say.** It does not say that schooling caused the release of labour, or growth, or the
fertility decline; the evidence is timing plus conditional association, not causal identification. It does not
say that the demand story is wrong for the first industrialisers — Britain is exactly where demand led. It does
not say that institutions always lead — France and the United States are mixed cases, and the four historical
cases are a dated argument, not a sample. It does not say the regularity is universal — the sample is the
late-industrialisers the post-1965 data can see, and the framing throughout is **a late-industrialiser
regularity, not a universal law**. What it does say is that in the countries where the question can be measured,
the schooling system is better described as moving with structural change and typically ahead of the narrow
labour-market demand ordering than as following it, and that this is associated with who built the pipeline and
when.

## 3. What the literature predicts - and has anyone established this ordering?
### 3.1 Human capital and the demand for schooling

The economics of education begins with the idea that schooling is an investment in productive capacity.
Schultz (1961) framed human capital as an input produced by education and health; Becker (1964) gave the
investment calculus its canonical form; Mincer (1958, 1974) turned it into the earnings function that made
returns to schooling estimable. The demand-led reading of massification follows directly: as the technology of
production becomes more skill-intensive, the return to schooling rises, families demand more of it, and school
systems grow to meet the demand. Goldin and Katz (2008) give the account its most influential historical form
for the United States — the twentieth century as a race between education and technology — and Acemoglu and
Autor (2011) give it its modern labour-market form, with skill-biased technical change shifting demand toward
educated workers. Nelson and Phelps (1966) add a complementary mechanism: educated workers are better at
adopting and implementing new technology, so the return to schooling rises with the pace of technological
change.

On this account, the timing prediction is unambiguous: **labour-market demand should turn on before, or at
least not long after, school systems expand.** Wages for educated workers should rise first; employment should
shift toward sectors that hire educated workers; then schooling should follow. The account is not naive about
supply — Goldin and Katz (2008) themselves stress that the American high-school movement required public
provision — but the causal primacy is on the demand side. A finding that schooling systematically precedes
labour-market demand in late-industrialising countries is a problem for the account's generality, not
necessarily for its logic: it may be that the demand story is a story about the first industrialisers, where
the demand shock was real and large, and that late industrialisers faced a different problem — building the
pipeline in anticipation of demand that had not yet arrived, or for reasons that were not economic at all.

### 3.2 World culture and institutionalist theory

The institutionalist tradition in the sociology of education argues that mass schooling spread because it became
a legitimate model of the modern state, not because local economies demanded it. Meyer (1977) argued that
education's effects are institutional as much as technical: schools certify categories of person and sort them
into a common status order. Boli, Ramirez and Meyer (1985) located the origins of mass education in the
construction of the nation-state and the model of the educated citizen, not in industrial demand; Ramirez and
Boli (1987) traced the political construction of mass schooling across Europe and its worldwide
institutionalisation; Soysal and Strang (1989) showed that the first mass education systems in nineteenth-century
Europe were built by states with weak or uneven economic demand, and that the timing followed state-building and
nation-making more closely than industrialisation. Benavot and Riddle (1988) documented the worldwide expansion
of primary education between 1870 and 1940 and its loose coupling with economic development. Meyer, Ramirez and
Soysal (1992) documented the world expansion of mass education as a diffusion process; Schofer and Meyer (2005)
extended the argument to higher education. Meyer and Rowan (1977) and DiMaggio and Powell (1983) supply the
mechanism: organisations adopt legitimate forms, and states adopt the school because it is the legitimate form of
the modern state.

The timing prediction of this literature is the mirror image of the human-capital prediction: **school systems
can, and often do, expand before the labour market demands their graduates**, because the demand that matters
is the demand for legitimacy, not the demand for skills. This literature does not usually frame its claims as
event-ordering tests, and that is exactly the gap the present paper addresses: the institutionalist claim has
been argued from diffusion patterns and case histories, not from a common event comparison across countries.
If schooling precedes labour-market demand, the institutionalist account gains a timing fact it has lacked;
if demand precedes schooling, the institutionalist account is in trouble in that sample. The truth, as this
paper will show, is conditional: it depends on who built the pipeline and when industrialisation arrived.

### 3.3 State building and compulsory schooling

A third literature explains school expansion as state building. Soysal (1994) and Soysal and Strang (1989)
link mass education to the construction of national citizenship. Flora and Alber (1981) and Flora, Kraus and
Pfenning (1983) document the welfare-state and schooling legislation of Western Europe in a comparative
data handbook that remains the standard source for statutory dates. Lindert (2004) shows that public schooling
spending has deep political roots and that its growth is not simply an income effect. Alesina and Reich (2013)
model nation building as a motive for public education: states school populations to build a common identity,
especially where the state is young or heterogeneous. Gradstein and Justman (2002) and Gradstein, Justman and
Meier (2005) formalise education as a social-cohesion technology — a public good whose provision is political,
not a private investment responding to wages. Bowles and Gintis (1976) offer the critical version: schooling
formats workers for the social relations of production, a reading that also predicts schooling can run ahead of
or alongside economic demand rather than simply following it.

The state-building literature supplies the mechanism that makes state-supplied massification plausible: a state with
ambitions and capacity can build schools before there is an economic return, because the return it seeks is
political and administrative. It also supplies the key comparative prediction: state-supplied expansion should
be most visible where the state was strong relative to the market — Prussia is the paradigm — and least visible
where the market led — Britain. This is the prediction the historical cases in Section 8 test.

### 3.4 The economic history of the sequence

The historical literature has argued about the sequence case by case, and the cases disagree. For **Prussia and
Germany**, Schleunes (1989) and the Flora et al. (1983) legislative handbook document a schooling state that
predates industrialisation: compulsory schooling edicts in the eighteenth century, an bureaucracy that enforced
them unevenly, and an educational apparatus that was in place before the industrial take-off. For **Britain**,
Sanderson (1999), Mitch (1984, 1993) and West (1967) document the opposite: the first industrial revolution, the
agricultural exodus and urbanisation all precede national mass schooling, and the 1870 Elementary Education Act
arrives after the economy had already been transformed. Mitch (1984) asks whether there was underinvestment in
literacy in nineteenth-century England and finds the question genuinely open; West (1967) analyses the political
economy of public school legislation; the Newcastle Commission (1861) is the near-primary source for attendance
before 1870. For **France**, Diebolt and co-authors (Diebolt, Jaoul and San Martino 2005) reconstruct the French
education series: the Guizot law of 1833 creates a school in every commune, but measured primary attainment
lags until the Ferry laws of 1881–82 — a case where the statute and the attainment move decades apart. For the
**United States**, Goldin (1998, 2001) and Goldin and Katz (2008) document the common-school movement
(1830–60) and the high-school movement (1910–40); US Historical Statistics, series H-598 onward, is the standard
enrolment series. The historical consensus, then, is that the sequence varies by country — which is exactly why
a systematic comparison is useful and why "one universal law" would be the wrong conclusion.

### 3.5 Structural change and the agricultural floor

The demand story has a structural-transformation version that is more sophisticated than "skills demand rises".
Agriculture's labour productivity is low in poor countries, and labour leaves agriculture as productivity rises.
Boppart, Kiernan, Krusell and Malmberg (2023) give the most developed recent account: a cross-country nested CES
agricultural production function in which low non-agricultural TFP makes investment and intermediate goods
expensive relative to labour in poor countries, so those countries substitute labour into agriculture; the
agricultural productivity gap and the agricultural employment share are then equilibrium outcomes, not
distortions. Restuccia, Yang and Zhu (2008) quantify agriculture's contribution to aggregate productivity
differences; Gollin, Parente and Rogerson (2002) and Gollin (2010) lay out the role of agricultural productivity
in development; Adamopoulos and Restuccia (2014) connect farm size distributions to productivity;
Herrendorf, Rogerson and Valentinyi (2014) survey structural transformation; Caselli (2005) provides the
development-accounting frame; Schultz (1964)'s *Transforming Traditional Agriculture* is the classic statement
of the agricultural-efficiency view; Matsuyama (1992) models agricultural productivity and industrialisation;
and Buera, Kaboski and Rogerson (2022) link skill-biased structural change to the demand for education.

If the demand story is right, the release of labour from agriculture is the event that should precede schooling:
the farm exodus creates the wage-labour demand, and the schooling system responds. If mass schooling precedes
the agricultural release, the demand story's central event ordering is wrong for that country. The project
therefore tested both: the agricultural-floor mechanism itself (Section 9) and its timing relative to schooling
(Section 6).

### 3.6 Scaling, credentialing and the institutional reading

Two further literatures bear on massification. The scaling literature asks whether social quantities follow
power laws — urban output superlinear, infrastructure sublinear, city sizes Zipf, distinct categories Heaps —
and the project's theory invokes a diversity formalism in which systems diversify functionally as they scale
(Bettencourt et al. 2007; Bettencourt 2013; Zipf 1949; Gibrat 1931; Heaps 1978; Ortman et al. 2014;
Yang et al. 2026). Section 10 reports what could and could not be estimated; the relevant point for this paper
is that a scaling regularity is not a causal identification, and that between-country regularities need not
hold within countries as they grow. The credentialing literature — Spence (1973), Collins (1979), Bills (2004)
— supplies the complementary reading of massification as positional competition: schooling expands because it
certifies, and the credential ratchet can outrun the skill content of jobs. Section 11 tests the
credential-inflation and care-work mechanisms and finds them unsupported in the available cross-country data.

### 3.7 What is unresolved, and the question this paper asks

Each literature has a timing prediction, and they have never been put into a common event comparison. The
human-capital and structural-change literatures predict that labour-market demand shows up before schooling
expands. The institutionalist and state-building literatures predict the reverse, at least where the state is
the supplier. The economic-history literature suggests the answer differs by country. The question this paper
asks is therefore simple to state and hard to answer: **relative to the take-off in schooling, which side turns
first — the supply-side conditions that build school systems, or the demand-side conditions that the human-
capital story requires — and does the answer depend on who industrialised first?** Section 4 describes the data
that let us answer it, and the data-availability problems that almost produced the wrong answer.

## 4. Data and measurement
### 4.1 The country panel and the long-run sources

The spine of the paper is a country–year panel assembled by the project (the "Atlas panel"). It combines a
17-measure socio-economic panel covering 1950–2023 with long-run historical sources: Maddison Project income
per head, Gapminder/Wittgenstein child mortality and life expectancy, Barro–Lee and Wittgenstein schooling
attainment, World Bank WDI, the Penn World Table, USDA ERS agricultural quantities, and the United Nations
World Population Prospects. The panel's series are documented in the project's prior records; the event dates
and the horse-race variables used in this paper are in the records listed in the claims-to-source map
(`claims-to-source-map.md`), which gives branch, commit, file and field for every number.

Two facts about the panel constrain what can be measured. First, its long-run schooling series (mean years of
schooling for the population aged 15–64) begins in **1870** for the early industrialisers and in the 1950s for
most countries, so the take-off of the countries we care about most — Prussia, France, Britain before 1870 — is
**not observable in our own data**; the historical cases in Section 8 must rest on the literature and are
labelled accordingly. Second, the reliable cross-country agricultural employment shares begin only around
1960–70 (ILO/WDI modelling), which sets the common event window for the modern panel to 1965–2010.

**Data tiers, labelled.** Following the project's evidence rules, every series used here carries a tier label,
and the tier is stated wherever a number from that series appears:

| series | tier | notes |
|---|---|---|
| GGDC 10-Sector employment, WDI urbanisation and sector value added, WDI primary/secondary GER, PWT | **observed** | harmonised official series; GGDC/ILO reconstruction of missing intermediates is noted where it applies |
| agricultural employment share (WDI/ILO modelled, 1991+) | **observed, model-based** | used only in robustness/sensitivity, never as a pre-1990 demand-timing proxy |
| long-run mean-years-of-schooling panel (1870–2020) | **reconstructed** | historical reconstruction on a 5-year grid |
| WDI total fertility rate (births per woman) | **observed** | a birth-based TFR; **not** the project's effective-fertility measure (expected surviving children), and never labelled as it |
| event dates (schooling take-off, agricultural release, fertility decline) | **reconstructed** from the series above | threshold rules fixed in advance; ties remain weak inequalities |
| supply and demand onset dates and horse-race variables | **observed / reconstructed** | spending, enrolment and urbanisation observed; paid employment and the wage-premium proxy partly modelled/reconstructed (paid-employment coverage starts 1991) |
| fee-abolition dates (E8) | **verified** (8 countries) / **unresolved** (4, excluded from main) | independent source audit, primary/authoritative sources with quotes |
| four historical sequences (Prussia, France, Britain, US North) | **literature-standard, UNVERIFIED** | secondary dates not re-checked against primary sources in this pass |

These are
data limits, not design choices, and they motivate the careful measurement rules below.

### 4.2 Event definitions, fixed in advance

The paper compares three events. All definitions were fixed and committed **before** the dates were assembled.
For the modern panel the definitions were part of the subsistence-v2 pre-registration (commit `62730fc`); for
the historical cases they were in `DEFINITIONS.md` (commit `74e0fe2`).

1. **Schooling take-off.** The first year in a common window in which a national schooling series rises by at
   least **1.0 year of schooling within ten years**, using the mean-years-of-schooling series (population 15–64).
   The threshold is large on purpose: it isolates the sustained rise, not a year-on-year fluctuation. For the
   historical cases the literature date is used instead (statute or measured enrolment series), and statute and
   attainment are recorded separately where they differ, as they do in France.
2. **Agricultural labour release.** The first year in which the agricultural employment share **falls by at
   least 3 percentage points within ten years** and does not recover above its starting value. The 3-point
   threshold is the smallest fall that is robust to the cross-country differences in how the share is measured.
3. **Fertility decline.** The first year in which the **total fertility rate** (WDI, observed; births per
   woman) **falls by at least 1.0 birth per woman within ten years**. This is a birth-based TFR and is a
   different construct from the project's effective-fertility measure (expected surviving children per woman);
   the two are not interchangeable (median absolute difference 0.3042, maximum 4.2677 in the source audit), and
   the effective-fertility series is not used in this paper. The TFR result is used for the secondary sequencing
   result (schooling against fertility) and for the framing; it is not the paper's primary outcome.

For the supply-versus-demand comparison the following onset definitions were pre-registered:
**supply onset** = the first year in which any of (i) public education spending rises by at least 1.0 percentage
point of GDP within ten years, (ii) the primary pupil–teacher ratio falls by at least 10% within ten years, or
(iii) primary gross enrolment rises by at least 10 percentage points within ten years.
**Demand onset** = the first year in which any of (i) the non-agricultural-to-agricultural labour productivity
ratio (a wage-premium proxy) rises by at least 20% within ten years, (ii) the paid-employment share rises by at
least 5 percentage points within ten years, or (iii) the urban share rises by at least 5 percentage points
within ten years. A "labour-market-only" variant uses only the wage-premium and paid-employment measures, which
is the version closest to what the human-capital theory requires. All windows are ten years, and the common
detection window is 1950–2010, constrained by data availability as described next.

### 4.3 The data-availability problem, stated before the results

The raw event comparison can mislead, and we say this before reporting it because we nearly fell into it. Three
problems stack:
- **Right-censoring at the window start.** 61 of 108 countries with a schooling date have their take-off exactly
  at the first year of the window (1965), because the schooling series rise from a low base as soon as the common
  window opens; their true take-off may be earlier and unobservable.
- **Left-censoring of supply data.** The World Bank education-spending, pupil–teacher and enrolment series begin
  in the median country only in **1975**. A country whose schooling rose in 1965 cannot possibly show a supply
  onset before it in these series.
- **Different measurement of "demand".** Income and urbanisation are available from 1960 and rise almost
  everywhere; the labour-market variables the human-capital theory actually names (wage premia, paid jobs) have
  much shorter coverage.
The consequence is that the raw ordering is biased **against supply and in favour of demand**. Section 7 reports
the raw ordering, then the fair-sample comparison (countries whose schooling take-off is after the window start
and whose supply data begin before the take-off), then the horse race, which does not depend on event dating.
This ordering of evidence — raw, corrected, then horse race — was fixed in advance and is reported in that
order so the reader can see how the correction changes the answer.

### 4.4 Supply measures, demand measures, and the horse race

**Supply measures.** (i) Public education spending as a share of GDP (World Bank WDI `SE.XPD.TOTL.GD.ZS`);
(ii) the primary pupil–teacher ratio (WDI `SE.PRM.ENRL.TC.ZS`), where a fall is a supply expansion;
(iii) the primary gross enrolment ratio (WDI `SE.PRM.ENRR`) as a capacity proxy; and, for a six-country deep
dive, the project's state-capacity file (`STATE_CAPACITY.csv`, which contains education spending, teacher
counts, pupil–teacher ratios and years of compulsory education guaranteed in law for China, Hong Kong, Japan,
Cambodia, Korea and the Philippines). Compulsory/free-schooling law dates come from the project's compiled
`POLICY_TIMELINE.csv` (six systems, sources inside the file) and from the standard literature for the four
historical cases. A full cross-country compulsory-schooling-law compilation from the literature was **not**
completed in this pass and is reported as a data gap rather than proxied.

**Demand measures.** (i) The non-agricultural-to-agricultural labour productivity ratio, constructed from WDI
agricultural value added, agricultural employment share, labour force and GDP; (ii) the paid-employment share
from the project panel (available from 1991); (iii) the urban share; (iv) GDP per worker growth. The agricultural
labour-release event is the fifth demand measure, but it is also the event being explained, so it is not used as
a predictor of schooling.

**The horse race.** For every country–period, we compute ten-year changes in mean years of schooling and in
each supply and demand measure, enter the supply and demand blocks separately and then together, with country
and period fixed effects, and cluster the standard errors by country. Regressors are standardized so that the
coefficients are comparable within blocks. The sample is limited by supply-data coverage: 78 country-period
observations from 51 countries in the joint specification; the demand-only specification has 300 observations
from 103 countries. What this design can and cannot identify is stated in Section 5.3: it identifies conditional
associations and timing, not causal elasticities.

### 4.5 Historical cases and their evidence classes

The four historical cases — Prussia/Germany, France, Britain and the northern United States — were chosen for
the question "who supplied the schooling?" not for representativeness. The definitions were fixed first
(`DEFINITIONS.md`, commit `74e0fe2`): a **supply-first** verdict (the pre-registration's "supply-led") requires schooling to precede the farm exodus by
at least ten years with the take-off statute-driven; a **demand-led** verdict requires the farm exodus to
precede the schooling take-off by at least ten years with enrolment rising as industrial jobs pull families in;
otherwise the case is **simultaneous or undated**. Every date is assigned an evidence class: **VERIFIED**
(dated in a primary or near-primary source read in this pass), **UNVERIFIED literature standard** (a standard
secondary date not re-checked against a primary source here) or **CONTESTED**. Every date in Section 8 is
**UNVERIFIED literature standard**, and the text says so at each case. The primary series that would promote
them to verified are named: Prussian enrolment 1800–1870 (Flora et al. 1983; Lindert 2004), UK school attendance
1850–1900 (Newcastle Commission 1861; Board of Education annual reports), French primary enrolment 1830–1900
(Diebolt, Jaoul and San Martino 2005; the ministry's *Statistique de l'enseignement primaire*), and US
high-school enrolment 1890–1940 (US Historical Statistics, series H-598 onward).

### 4.6 Scaling, credential and care data

The paper also synthesises three further bodies of evidence: scaling (project panel, prior scaling tables, ILOSTAT occupation counts by ISCO major group, attempted city-population and firm-level sources), credential and care (ILO SDMX employment 2010–23, WDI fertility, female participation, attainment and income, and the prior jobs-and-markets panel, checked but unusable because it covers only six countries), with data-availability statements in the relevant records.


## 5. Empirical strategy: an ordering claim, not a new correlation
### 5.1 Pre-registration

Every empirical exercise in this paper had its definitions, thresholds, samples and verdict rules committed
**before** the data were assembled or the estimates run. The relevant first commits are: subsistence-v2
`62730fc` (sequencing event definitions and falsifiers), supply-demand `f7b38f3` (supply/demand measures, fair
sample, horse race), historical-sequence `74e0fe2` (`DEFINITIONS.md`), scaling `f8f782f` (scaling rules and
verdicts), care-credential `7356e76` (care and credential mechanisms), and the grouping-multiverse
pre-registration. Where a pre-registered test came out against the framing, it is reported as such (Section 7
reports the raw ordering that favoured demand before the correction; Section 10 reports the rejected collapse
curve; Section 11 reports the null care and credential mechanisms). No analysis in this paper was added after
seeing a result in order to rescue a claim; the sensitivity checks that were added are labelled as such.

### 5.2 Event-ordering statistics

For each comparison we report three statistics: the **share of countries ordering one way**, with a bootstrap
95% interval from 1,000 resamples of countries (clustered by country by construction); the **median gap in
years**, with its bootstrap interval; and the **cross-tabulation** of the two orderings (supply-first only,
demand-first only, both before schooling, neither). Event dates are integers (years) and ties are counted as
simultaneous. The unit is the country-event, and countries are weighted equally: this is a statement about how
many countries show an ordering, not about how many people live under it. Sample sizes are reported with every
statistic: 64 countries for the three-event sequencing, 89 for the supply-versus-demand comparison, 33 for the
fair comparison, 58 for the labour-market-only demand measure.

### 5.3 The horse race, and what it identifies

The horse race regresses ten-year changes in schooling on ten-year changes in the supply block and the demand
block, with country fixed effects (absorbing fixed national characteristics) and period fixed effects (absorbing
common global changes), with standard errors clustered by country. It is a **conditional association**: it says
which block of correlates moves with schooling once the other is held fixed and national differences are
absorbed. It does **not** identify a causal effect of either block. Education policy, state capacity, income
and schooling are jointly determined, and there is no instrument here. The design can distinguish a timing
pattern and a conditional correlation; it cannot tell us whether spending "caused" schooling or schooling caused
spending. We therefore use the horse race only to arbitrate between the two theories' *descriptions* — which
block carries the association when both are present — and never as a causal estimate. Section 15 returns to
this.

### 5.4 Multiple comparisons and honesty rules

Where many links or countries are tested we report the multiple-testing correction used in the source record
(for the massification matrix: Benjamini–Hochberg at 5% across 272 links; for the multiverse: the 400-draw
empirical p-value floor of 1/401 and BH step-up arithmetic). The paper inherits those corrections rather than
re-running tests. For the event orderings there is one test per country group, so no multiplicity correction is
applied, but the bootstrap intervals and the cross-tabs are reported so the reader can see how much of the
headline share is carried by a few countries. "No first" is a rule, not a courtesy: the search strategy for the
literature is recorded in `search-strategy.md`, and the prior-art tables state what is new and what is
replicated for every claim.


## 6. The sequence: schools before factories
### 6.1 The headline result

Among the 64 countries where all three events — schooling take-off, agricultural labour release and fertility
decline — can be detected in the common 1965–2010 window, the schooling take-off **precedes** the agricultural
labour release in **61 countries (95.3%)**, with a median lead of **26 years** (bootstrap 95% interval of the
median 22–26 years; full record `subsistence-v2 @ ce66cfc`, `results/sequencing.txt`, fields
`pct_release_before_schooling` and `median gap release->schooling`). The reverse ordering — the farm exodus
first, the demand-led prediction — occurs in **3 countries, 4.7%** (bootstrap 95% interval 0–11%). The schooling
take-off also precedes the fertility decline in **37.5%** of those countries under a strict ordering (95% interval
26.6–50.0%; 31.3% simultaneous, 31.3% fertility-first), with a median gap of **0 years** (interquartile range −5
to +8). The source record's JSON reports **68.75%** for this ordering because it counts the 20 simultaneous cases
as schooling-first; a direct recomputation from the same record's event CSV gives **37.5%** among the 64 three-event
countries (**35.8%** across all 81 countries with both dates), and this paper reports the strict ordering and the
discrepancy rather than the JSON figure (recomputation: `scripts/recompute_fertility_ordering.py`, output
`data/recompute_fertility_ordering.json`). The related but **different** ordering of the farm exodus against the fertility decline is not used as a claim
in this paper: computed from the same event file it is **4/64 = 6.25%** release-first (no ties; the fertility
decline comes first in **60/64 = 93.75%**), and it must not be conflated with the 20/64 simultaneity in the
schooling-versus-fertility comparison (recomputation: `scripts/recompute_fertility_ordering.py`,
`data/recompute_fertility_ordering.json`).

The 64 countries are not a random sample: they are the countries where the events are dated at all, which
over-represents the later industrialisers that dominate the post-1965 data. This is a limitation, and it is also
the point of the paper: the regularity is a late-industrialiser regularity because late industrialisers are
what the modern data can see. The historical cases in Section 8 are how we check whether it extends backwards.

### 6.2 What the result does and does not mean

The result is an **event-ordering** result, not a causal one. It says that in this sample, the first sustained
rise in a national schooling series arrives, on average, a generation before the first sustained fall in the
agricultural employment share. It does **not** say that schooling caused the labour release. Schooling and
structural change can both be consequences of a third process — state building, for example — and the event
data cannot separate them. The result does say that the simple demand narrative — farms release labour, the
labour market demands skills, schooling follows — is **not the typical ordering** in the countries where the
16 sequence can be measured. The median 26-year lead is long enough that the two events are not part of a
single contemporaneous adjustment.

### 6.3 Robustness: which countries carry the result, and the window boundary

The 61-of-64 result is not driven by one region: the forward cases span Latin America, South Asia, East Asia, North Africa and Sub-Saharan Africa, and the three reverse cases are not a bloc. One concern is the window boundary: because both events are detected in the same 1965–2010 window, countries whose schooling take-off is exactly at 1965 may have led by more or less than 26 years; the bootstrap interval on the median (22–26 years) reflects that imprecision. A second is that the agricultural employment series are ILO-modelled for many countries and modelled shares can lag real sectoral change; if the effect were large it would shorten the measured lead, and the lead survives it. **Coding robustness (computed for this paper from the committed event dates).** Because the dates are the paper's central vulnerability, we report how the headline count behaves under date perturbation on the committed event-date file (alternative-threshold re-detection was not possible after the box went down and is stated as remaining work). In the 64-country sample the gap distribution is: median **26 years**, interquartile range **16–29 years** across all 64 gaps (**17–29** across the 61 forward cases); **59 of 61 (97%)** exceed 5 years, **57 of 61 (93%)** exceed 10, **52 of 61 (85%)** exceed 15, **43 of 61 (70%)** exceed 20 and **13 of 61 (21%)** exceed 30. A uniform 5-year overstatement would leave 59 of 61 forward cases; 10 years, 57; 15 years, 52 — the headline needs a systematic error above 15 years in the same direction to fall materially. What this does not do is re-detect the events under alternative definitions (statute vs enrolment; 1 vs 2 years of schooling; 3 vs 5 points of agricultural decline); that recoding is the paper's main empirical vulnerability and the first next step. Source: `subsistence-v2 @ ce66cfc`, `results/event_dates.csv`, columns `schooling` and `release`; the counts are arithmetic on that file, not a new estimate.

### 6.4 The demand variables, measured the way the theory measures them

The sequencing result says the labour release comes later; it does not yet say anything about labour-market
**demand**. Section 7 fills that in with pre-1990 structural-change series and with the wage-premium and
paid-employment measures, flagging that the paid-employment series begin in 1991 and cannot carry a pre-1990
demand-timing test. The sequencing result already limits the demand story: if the labour demand that is supposed
to pull schooling had turned on a generation earlier, it would have to be demand that was not associated with the
release of agricultural labour — a form of demand the agricultural-floor version of the story does not predict.


## 7. Supply versus demand: the horse race
### 7.1 The raw event ordering looks demand-led

The raw comparison of supply and demand onsets against the schooling take-off appears to favour demand. Among
the **89 countries** with both a supply and a demand onset and a schooling date, the **demand onset precedes**
the schooling take-off in **73.0%** (bootstrap 95% interval 64–82%), with a median gap of **−5 years** (demand
turns five years before schooling), while the **supply onset precedes** schooling in **28.1%** (95% interval
19–37%), with a median gap of **+10 years** (supply turns after schooling). Supply precedes demand in only
**28%** of countries (95% interval 19–38%). Read alone, this looks like a demand-led result: 43 countries are
"demand-first only", 22 are "both before schooling", 21 are "neither", and only 3 are "supply-first only"
(`supply-demand @ 963e5e5`, `results/supply_demand.json`, fields `supply_before_schooling_pct`,
`demand_before_schooling_pct`, `n_both`; and `results/supply_demand.txt` for the cross-tab).

### 7.2 Why that reading is a measurement artefact

The raw ordering is contaminated by when the data exist, in three ways that all push in the same direction.
First, **61 of the 108 schooling dates sit on the first year of the common window (1965)**: countries that
schooled early are censored at the boundary, and a supply onset can only be detected after 1965. Second, the
**supply series start in the median country in 1975** (education spending, pupil–teacher ratios and enrolment
capacity), so a country whose schooling rose in 1965–75 cannot show a supply onset before it; the demand series
(income, urbanisation) start in 1960. Third, the demand block includes **income and urbanisation**, which rise
almost everywhere almost always and are not what the human-capital theory names. The bias is therefore not
subtle: the raw test is stacked against supply.

### 7.3 The fair comparison: the two sides turn together

Restricting to a fair comparison sample — countries whose schooling take-off is **after** the window start and
whose supply data begin **before** the take-off (33 countries) — changes the answer. In that sample, **supply
precedes schooling in 76%** and **demand in 79%** of countries, and **supply precedes demand in only 39%**;
the median supply–schooling gap is **−5 years** and the median demand–schooling gap is **−10 years**
(`supply-demand @ 963e5e5`, `results/supply_demand.txt`, C1b section). The two sides turn at essentially the
same time. The fair sample is small, and it is selected on data availability, so it cannot carry a strong claim
by itself; but it removes the artefact that produced the demand-first result, and in doing so it removes the
demand-first result.

### 7.4 The horse race: supply carries the association

The sharper test does not depend on event dating. In ten-year changes with country and period fixed effects and
country-clustered standard errors, the **supply block dominates**: the composite standardized coefficient is
**+0.456 (SE 0.174)** for supply against **+0.006 (SE 0.203)** for demand (n=78 country-periods, 51 countries).
Individually, primary gross enrolment (**+0.307, SE 0.146**) and education spending (**+0.125, SE 0.058**) are
significant, the pupil–teacher ratio is positive but imprecise (+0.098, SE 0.102), and **every demand measure is
null**: the wage-premium proxy (−0.209, SE 0.114), paid employment (+0.051, SE 0.117), urbanisation (−0.049,
SE 0.096) and income growth (+0.140, SE 0.136). With no supply block in the specification, the demand block
alone is also null (n=300, 103 countries; all four coefficients small and insignificant). The horse-race sample
is limited by supply-data coverage and is younger than the full panel, so it speaks to the period where both
blocks are measured — but within that period, the association with schooling expansion is on the supply side.

### 7.5 Structural change on pre-1990 series: schooling and structural change move together

The narrow labour-market measures that motivated the old "7%" figure cannot carry a pre-1990 test: WDI's
wage-employment and paid-employment series start in 1991, so on a 1965–2010 window they mechanically cannot
precede a schooling take-off for most countries. That figure is retracted as a data-start artefact and is not
used in this paper. The project therefore re-ran the demand-timing comparison on pre-1990 structural-change
series (E6, `research/e6e8-sequencing-2026-11-25` @ `2d19da7`): GGDC non-agricultural employment
(1947/1950–2012), WDI urbanisation (1960–) and WDI industry and agricultural value-added shares (1960–), with
demand take-off defined as a sustained move of at least 3 percentage points in ten years and the schooling
take-off as a sustained rise of at least 1.0 year in ten years. The demand take-off precedes the schooling
take-off in **10.0%** of identifiable countries on GGDC non-agricultural employment (2 of 20), **15.4%** on
urbanisation (10 of 65), **24.1%** on industry value added (13 of 54) and **18.8%** on agricultural value added
(9 of 48). Bounds over all countries with both series are **6.7–53.0%**; another **21–43%** of countries are
weak forward-or-tie orderings or are left-censored at the first observable year, so demand-first cannot be
excluded there, only weakly ordered. Across 54 threshold/smoothing definitions the strict demand-first share
ranges **0.0–30.8%** (median 10.45%; N3), which is why the ordering is reported as an interval rather than a
single percentage.

The honest reading is not that demand is ruled out. Strict schooling-first exceeds strict demand-first in every
proxy (**21.5–46.3%** of identifiable countries versus **10.0–24.1%**), but in none is it a majority, and
demand-first is a minority ordering that cannot be eliminated. **Schooling and structural change move together,
with schooling typically but not universally first.** That is a weaker claim than "supply-led massification", and
it is the claim the data support.

### 7.6 Supply-side event evidence: fee abolition and primary enrolment

One supply-side shock can be tested with an event study with checked pre-trends. Between 1994 and 2005, eight
Sub-Saharan African countries abolished primary-school fees at dates verified against primary or authoritative
sources (MWI 1994, ETH 1995, UGA 1997, LSO 2000, TZA 2001, KEN 2003, MOZ 2004, GHA 2005; four further dates —
Cameroon, Zambia, Rwanda and Burundi — remain unresolved and are excluded from the main specification). E8
(`research/e6e8-sequencing-2026-11-25` @ `2d19da7`; dates from task-49 @ `9a0fd69`) estimates
Callaway–Sant'Anna event studies on WDI primary gross enrolment (observed), 1990–2015, with not-yet-treated
controls, event time −5 to +6 and a country-cluster bootstrap (500 draws), with a TWFE event study as the
comparison. The pre-trends at −2, −3 and −4 are flat (−0.03 [−3.43, 3.38], −0.13 [−7.23, 6.98], 1.35 [−6.35,
9.04]); the earliest horizon, −5, is positive but imprecise and rests on six cohorts (6.39 [−0.08, 12.86]). The
on-impact estimate is positive but its interval spans zero (+12.4 [−2.4, 27.2]); from event year +1 the
post-treatment effects are large and positive (23.8 [2.05, 45.6] at +1; 25.9 [4.48, 47.40] at +2; 22.1 [5.62,
38.62] at +3; 25.2 [8.54, 41.84] at +4; 28.6 [9.61, 47.51] at +5; 25.9 [8.64, 43.20] at +6), and the TWFE
estimates are similar (21.0–27.6). A placebo with dates shifted six years earlier gives a mean post-effect of
−0.39, and the leave-one-country-out range is 18.2–26.2, so the sign and rough magnitude do not depend on a
single country. The requested lower-secondary outcome is proxied by WDI secondary GER, where the post-period
estimates are smaller and all intervals include zero; that is reported as a proxy with no clear detected effect,
not as a null.

What the design cannot do is as important as what it can. The treated sample is small (seven countries with
primary-GER coverage, six or seven cohorts per event horizon), the on-impact estimate is sensitive to ±1-year
date shifts (mean post 12.3 with a +1 shift, 18.6 with a −1 shift), four date conflicts are unresolved, and the
outcome is an enrolment ratio, not attainment or learning. The dating discipline that governs the rest of the
paper applies here too: onset definitions are thresholds, ties remain weak inequalities, and 61 of 108 schooling
take-offs are left-censored at 1965. Within those limits, the finding is **consistent with** a supply-side effect
of fee abolition on primary enrolment — this is the one place in the paper where an event study with checked
pre-trends licenses "consistent with" for a causal-style statement — and it does not identify massification,
attainment, or the schooling-versus-farm-exit ordering.

### 7.7 What this changes for the theory

The honest summary is conditional. The raw event ordering cannot distinguish the theories because it is dominated by data availability; the fair event comparison shows the two sides arriving together; the horse race puts the conditional association on supply; and the pre-1990 timing test finds schooling and structural change moving together with demand-first a minority that cannot be excluded. The narrow labour-market demand account finds no support in the timing tests, but neither is demand ruled out. The broad-development version of the demand story (income and urbanisation lead schooling) is supported, but it is not a human-capital story in the narrow sense — it is the familiar finding that richer, more urban places school more, which is consistent with institutionalist as well as demand accounts. What the evidence supports is the **descriptive** claim that in late industrialisers school systems were often built by states with their own reasons while schooling and structural change moved together, and that the narrow labour-market demand ordering arrives later. That is consistent with the institutional reading, and it is a description of the data, not a causal identification. A referee should read the horse race as a **decomposition, not a test**: both blocks correlate with development, state capacity and the demographic transition; exogenous variation in school supply would make it a test, and only the fee-abolition event study in Section 7.6 comes close, for one outcome.

## 8. The historical cases as a typology: Prussia and Britain as the two poles
*This section integrates the historical-sequence record (`research/historical-sequence-2026-11-23` @ `ab658c7`,
definitions first committed at `74e0fe2`), drafted for this paper by the historical-sequence lead and edited into
the paper's voice. All historical dates are UNVERIFIED literature standard; the evidence labels are stated at
each case.*

The 1965–2010 panel finds that schooling take-off precedes the release of agricultural labour in 61 of 64
countries. That regularity could be a law of development or a property of the late-industrialising countries that
dominate post-1965 data. The historical cases are where the question can be asked directly, and the answer is
split: schooling typically came first where the state built the pipeline ahead of demand.

**Prussia** is the clean case of state supply. The General-Landschul-Reglement of 1763 made schooling compulsory,
reaffirmed in the 1794 Landrecht and the 1812 Hardenberg edict; roughly half of school-age children were enrolled
around 1800 and enrolment was near universal by the 1860s; industrialisation is dated to the 1840s–1870s and the
agricultural employment share began its sustained fall after 1850. Schooling precedes industrialisation and the
farm exodus by **80 to 120 years**. The state built the schools before there was industrial demand for literate
labour, which is exactly the theory's pipeline-first mechanism. **All dates here are UNVERIFIED literature
standard.**

**France** shows the statute and the attainment take-off coming apart. Guizot's 1833 law required a primary school
in every commune, followed by Falloux in 1850 and the Ferry laws of 1881–82. But measured attainment does not
follow 1833: primary enrolment is estimated at about 45% in the 1830s and only reaches 75–80% by 1880, while the
agricultural share was about 52% in 1851, 41% in 1901 and 30% by 1930. The statute precedes the farm exodus by
about fifty years; measured attainment arrives with it. The honest verdict is **statute-led and
attainment demand-following**, and it is why the policy date and the attainment date are reported separately.
**All dates UNVERIFIED literature standard.**

**Britain** is the case that started the question, and it inverts the ordering. The industrial revolution dates to
roughly 1780–1840, and the agricultural employment share fell from about 35% in 1800 to 22% in 1851 and 9% by
1901. Mass schooling arrives late: the Elementary Education Act in 1870, compulsory attendance in 1880, free
schooling in 1891, and attendance of about one child in eight as late as 1858. **Industrialisation and the farm
exodus precede mass schooling by 40 to 90 years.** This is where "the floor falls first" is true, and it is also
the case in which a state-supplied mechanism should have been least needed. **All dates UNVERIFIED literature
standard**; the near-primary source for the attendance figure is the Newcastle Commission (1861).

**The northern United States** sits in between. Common schools were built in 1830–60 with public funding from the
1830s and the first state compulsory law in Massachusetts in 1852; the national agricultural employment share was
about 63% in 1840, 50% in 1870, 31% in 1910 and 12% in 1950, and the high-school movement dates to 1910–40.
Schooling take-off precedes the national farm exodus by sixty or more years, but the schools were locally
financed and demand-driven, and the high-school movement coincides with the final exodus rather than preceding
it. **All dates UNVERIFIED literature standard**; the enrolment series that would verify them is US Historical
Statistics series H-598 onward.

| case | schooling take-off | supply-side policy date | farm exodus | order | verdict |
|---|---|---|---|---|---|
| Prussia / Germany | ~50% enrolment c.1800; near-universal 1860s | **1763** Landschul-Reglement; 1794; 1812 | after 1850; under 40% by 1900 | schooling first, 80–120 yrs | supply first (state-built) |
| France | ~45% 1830s; 75–80% by 1880 | **1833** Guizot; 1850 Falloux; **1881–82** Ferry | ~52% (1851) to ~30% (1930) | statute first 50 yrs; attainment with exodus | statute-led, attainment demand-following |
| Britain | ~1 child in 8 in 1858; near-universal by 1900 | 1833 Factory Act; **1870** Education Act; 1880 compulsory | ~35% (1800) to ~22% (1851) to ~9% (1901) | **industrialisation and exodus first, 40–90 yrs** | demand-led |
| US North | common schools **1830–60**; high schools 1910–40 | Massachusetts 1852 | ~63% (1840) to ~31% (1910) | schooling first nationally 60+ yrs; high schools coincide | state-supplied, locally demand-driven |

**Reading.** The panel regularity survives only with the qualifier *where the state built the pipeline before
demand arrived*. Prussia is the clean case; France separates the statute from the attainment by half a century;
Britain inverts the ordering; the United States sits between. The implication is that the 61-of-64 result is a
**late-industrialiser regularity, not a universal law**, and it is evidence about who built the pipeline and when
rather than evidence that schooling causes the labour release. Read together, the four cases are best treated as
the two poles of a typology — state-built pipeline versus market-led — rather than as rival stories; Section 12.2
develops the typology and its limits.

**Evidence classes and the data gap.** Every date above is a standard literature date but **none was verified against a primary source in this pass**; all are labelled **UNVERIFIED literature standard**. Two facts are verified in-session, both negative: the project's own long-run panel cannot adjudicate them, because its schooling series starts in 1870 for all four countries and its urban-share series in 1950, so the pre-registered rule returns the start of the data for every case (`historical-sequence @ ab658c7`, `results/sequence_from_panel.json`); and no national enrolment series was obtainable from public APIs, so no lead or lag is estimated from a series. This section is a dated argument, not a measurement; the series that would make it one are named in Section 13.2.

**What the cases establish, and what they do not.** They establish that the ordering is not fixed across
countries, that the first industrialiser inverted it, and that the modern panel's regularity is therefore
conditional on the state being the supplier. They do not establish a causal effect of schooling on the farm
exodus; the cases show sequence and political economy, not identification. The next section turns to the
strongest theoretical version of the demand story — the agricultural floor — and tests it on its own terms.


## 9. Supporting evidence I: the agricultural floor and the joint model
*This section integrates the two subsistence records (`research/subsistence-2026-11-23` @ `41f6429`,
pre-registered at `d47e5ed`; `research/subsistence-v2-2026-11-23` @ `ce66cfc`, pre-registered at `62730fc`),
drafted for this paper by the subsistence lead and edited into the paper's voice.*

Boppart, Kiernan, Krusell and Malmberg (2023) — BKKM — explain why poor-country agriculture uses so much
labour: low non-agricultural productivity makes investment and intermediate goods expensive relative to labour,
so farmers substitute the cheap factor in; as non-agricultural productivity rises inputs get cheaper, farms
intensify, and labour is released. Their evidence is cross-sectional, but the argument implies a sequence:
**inputs before labour release**. We re-estimated the cross-sectional objects on rebuilt data and tested the
sequence.

**The earlier test was not this paper's object.** An earlier stage regressed farm exit, wage jobs and births on a world commodity-price index interacted with the farm employment share; that test contains none of BKKM's objects (no input quantities, relative input prices, substitution elasticity or development decomposition), measures exposure to a common world price shock, and could not have detected the input-price mechanism even in principle, so its null carries no information about BKKM either way.

**Rebuild.** The paper's appendix contains no data, so everything is rebuilt: USDA ERS agricultural quantities
(182 countries, 1961–2023), Penn World Table relative input prices, World Bank WDI outcomes and controls
(207,622 rows), and the project's long-run transition panel for demography. The deviations are documented; the
two that matter are no land-quality adjustment (so **the land elasticity is not estimable**) and no
country-specific intermediate prices (the non-agricultural price level is a proxy, which attenuates the
elasticities).

**Cross-section: direction replicated, magnitude not.** Log input intensity on the log relative input price:
**−1.13 (SE 0.15), n=126** in 2005 and **−1.28 (SE 0.11), n=128** in 2015. The elasticities are above one but
below the paper's: capital–labour **1.24 (SE 0.08)** in 2005 and **1.40 (SE 0.07)** in 2015, intermediates–labour
**1.11 (SE 0.08)** and **1.27 (SE 0.07)**, against the paper's 1.90 and 1.75; at the development extremes ours
reach **1.73** and **1.76**. Input quantities rise **570x** (capital) and **637x** (intermediates) from poorest
to richest in 2005, inside the paper's 300–800x range. Input intensification accounts for **55.0 to 69.4 per
cent** of the agricultural labour-productivity gap, against the paper's "a bit less than two-thirds". Intensity
and the agricultural employment share are strongly negatively related, **−4.71 (SE 0.89), n=126** and **−4.38
(SE 1.15), n=128**; the relative-price coefficient in that equation is positive as predicted but insignificant.
This is a **partial replication, not a confirmation**. The attenuation explanation (proxy prices) is consistent
with the extremes sitting close to the paper's values while the full sample sits below; but without the authors'
data we cannot distinguish "the paper is slightly high" from "our proxy is slightly noisy", and we say so.

**Sequencing: not identified.** A ten-year country panel with country and decade fixed effects (503
country-year observations, 128 countries, clustered) gives the wrong-signed level association: change in the
agricultural employment share on intensity at t is **+1.75 (SE 0.71)**, so more intensive farms at t release
*less* labour over the next decade. The reverse association is stronger: past agricultural-share change on
current intensity is **−3.32 (SE 0.70), n=383**. Past **changes** in intensity and price do not predict future
release (both nulls, n=472); the only stable predictor of the change in the agricultural share is its own level
(**−0.53, SE 0.10**), i.e. convergence. Both variables converge and each predicts the other, so this design
cannot order them in time. The cross-section is real; the sequence is not established.

**Downstream: a precise null.** Ten-year change in secondary completion on labour release and intensity:
**−0.16 (SE 0.25)** and **−1.18 (SE 3.20), n=278**; ten-year fertility change: **−0.0003 (SE 0.0058)** and
**−0.005 (SE 0.050), n=503**, with income and urbanisation controls. The minimum detectable fertility effect is
about **0.016 births**, so the null has power at this horizon. This is important for the demand story: the
mechanism that is supposed to connect the agricultural floor to schooling and fertility is not visible at the
ten-year country-panel horizon.

**Joint demography–agriculture model: demonstration.** BKKM-style production with substitution elasticity 1.5, a
quantity-quality demographic block, and a wage sector plus schooling queue absorbing released labour; **five free
parameters**, all calibrated to 1950–2020 stylised-country medians. Repair status: the agricultural share
reaches **17.6 per cent against 19.4 in the data** (inside the 5-point pre-registered tolerance), birth-based TFR **2.35 vs
2.06**, schooling **7.5 vs 9.6 years**, while the population index is **1.58 vs 2.92** — the population repair
failed in the other direction (too slow). Counterfactuals in 2020: freezing mechanisation leaves the
agricultural share at **39.9 per cent**, schooling at **0.2 years** and TFR at **3.29**; freezing the schooling
pipeline leaves schooling at **3.0 years** and TFR at **2.94**; freezing the mortality decline takes the
population index to **0.39** and TFR to **3.96**. The mortality decline is the model's first mover,
mechanisation empties the floor, and the pipeline converts released labour into schooling. But the
parameter-recovery test identifies only **two of the five free parameters**, so the counterfactuals illustrate
structure and are **not historical estimates**.

**What this section establishes.** The BKKM mechanism is real in the cross-section: relative input prices,
input intensity and agricultural employment line up as the theory predicts, and input intensification explains a
large minority-to-majority share of the agricultural productivity gap. That is the strongest version of the
demand story, and it deserves the fair test it gets here. But the sequence that the demand story needs — inputs
first, labour release second, schooling and fertility after — is **not identified** in the country panel: the
two ends of the mechanism converge on each other, the downstream effects at ten years are precise nulls, and the
joint model that reproduces the qualitative path fits the population badly and identifies only two of five
parameters. The floor is real; the timing story built on it is not established.


## 10. Supporting evidence II: scaling regularities, the diversity formalism, and what the evidence says moves massification
*This section integrates the scaling records (`research/scaling-2026-11-23` @ `fd691a6`, pre-registered at
`f8f782f`; `research/scaling-data-hunt-2026-11-23` @ `9e15b6d`; `research/scaling-laws-catalogue-2026-11-23` @
`cfe372f`; `research/sfi-scan-2026-11-23` @ `fd4cfd2`) and the grouping-multiverse record
(`research/grouping-multiverse-400-2026-11-23` @ `1152cec`). The paper's theory invokes scaling laws and a
theta/gamma diversity formalism; this section reports what the data can and cannot say about them, and then the
direct evidence on what the evidence says moves massification.*

### 10.1 Scaling laws in this data are between-country regularities, not laws of change

The project applied a strict rule: a *law* is a power law whose exponent is stable across samples and estimators and has an interpretation; a *regularity* is a stable pattern without those; and an exponent strong between countries but weak or different within them is a **between-country regularity**. Estimated on the project panel (30–261 countries, 1960–2024), the education–income relations split sharply: secondary enrolment (between **0.215**, SE 0.035; within 0.090, SE 0.124), upper-secondary attainment (0.312 vs 0.072), education stock (1.176 vs 0.051), cohort size vs enrolment (−0.612 vs −0.006) and agriculture share (−0.990 vs −0.120) are between-country regularities; tertiary enrolment (0.567 vs 0.848), lower-secondary completion (0.169 vs 0.247), services share (0.294 vs 0.275) and urban share (0.012 vs 0.011) are law-like candidates stable in both layers. Across an 18-pair stability test with five estimators, three relations were called "scaling law (stable across estimators)", fourteen "period/region regularity", one unidentified. **The discipline result is that the relations we may call law-like are the ones stable in both the cross-section and within countries; several relations the project's theory leans on (secondary enrolment, attainment, education stock) are cross-sectional regularities only.** A scaling regularity is not a causal identification; the results are used only to police the theory's language.

### 10.2 The universal fertility–attainment collapse curve is rejected

The theory's strongest scaling claim is that fertility falls on a single curve as female attainment rises — "same
niche, same function". The project tested it on **4,394 country–cohort points (158 countries, cohorts born
1950–1996**, cohort fertility measured at age 28, female attainment = secondary completion × gender-parity
adjustment at age 20). The best common curve is exponential: fertility = 1.13 (SE 0.26) + 5.97 (SE 0.23) ×
exp(−0.0197 (SE 0.0025) × attainment), pooled R² = 0.78. But **country identity explains 71.6% of the remaining
residual variance**: country intercepts R² = 0.914, country-specific slopes R² = 0.955, slope-heterogeneity
F = 46.4 on 313 and 3,717 degrees of freedom; residual scatter is 0.847 births per woman (11.2% of the fertility
range) and still 0.434 after a country-level rescaling. The residuals are structured: low-income countries sit
+0.40 births above the common curve and high-income countries −0.11; the 1950s cohorts sit +0.29 and the 1970s
cohorts −0.17. **Verdict: a common shape with country-specific levels and slopes, not a single universal curve.**
The related levels-vs-changes result is the same warning: the fertility–attainment slope is −0.479 between
countries, −0.299 (SE 0.026) within countries at levels, and only −0.056 for ten-year changes within countries
(2,064 changes, 201 countries) — about a sixth as strong in changes as between countries. Fertility vs income is
a power law with exponent −0.263 (SE 0.013; n=11,345, 213 countries, R²=0.50) with mild curvature — a
regularity, no canonical exponent.

### 10.3 Heaps, Zipf and the diversity formalism

The project also tested the scaling regularities the theory invokes. **Heaps' law**: distinct occupation
categories vs sample size, from ILOSTAT occupation counts (295 areas, 1969–2025; 151 countries usable). The
estimated exponent is **0.333 (SE 0.011)** — below the literature's 0.4–0.6 band — but the measurement is
1-digit ISCO major groups, which cannot produce the category depth a real Heaps estimate needs; rarefaction
corrections were applied and the estimate remains coarse. **No universalisation threshold break** was found
(p=0.22). **Zipf's law** for city populations rests on 55 countries and 22,465 cities; the median rank-size exponent is
**0.859 (CI 0.746–0.978; p=0.23 against 1.0)** — weaker than the canonical 1.0, a weak test reported as weak
because full city-size distributions were not obtainable. Gravity for migration: PPML with fixed effects
**−0.970 (SE 0.076)**; OLS-FE −1.306 (SE 0.053); n=8,020 pairs, sizes around 0.5 — partial. The
urbanisation–income relation is a **logistic S-curve**, not a power law: slope 0.572 (SE 0.030), n=10,986 points
from 208 countries, midpoint about $3,647, out-of-sample RMSE 0.1523 versus 0.1598 for the linear alternative. **The theta/gamma diversity formalism cannot be estimated with the accessible data**:
the formalism needs functional-category counts at depth (2–4 digit occupations, credential registries,
firm-level category data), and the project could obtain only 1-digit ISCO depth; the latent theta/gamma parameters were **not estimable**, and
the available proxies (income p=0.75, region p=0.26) are stated as proxies, not as a test. The theory's central
quantitative claim — that the credential economy crossed into a high-theta regime — is therefore **not testable**
with these data, and no substitute was fabricated. The scaling material in this paper is a **diagnostic frame**, not a fitted claim: we did not estimate theta or gamma, and the formalism is not presented as tested.

### 10.4 What the evidence says about massification drivers: the driver null

The direct evidence on massification drivers comes from the grouping multiverse: 50 real groupings in 8 families (179 groups) and 400 random re-partitions as the yardstick, with the 17-measure lead-lag matrix rerun inside every group and correction across 272 links. With 400 draws, **46 of 272 links beat random groupings with trends** (42 of the earlier 43 survive, one dies, four are new), **20 are worse** than random, **32 show more sign-flipping**, and **only five links are robust in every kind of grouping**, all fertility-side or accounting-side: child mortality → life expectancy (62.7% of real groups vs 48.5% random), child mortality → fertility (95.0 vs 93.0), income → urbanisation (52 vs 49), farm share → income (53 vs 37) and life expectancy → fertility (80.9 vs 93.0). **No schooling driver is robust anywhere.** **Electricity** has the strongest country-effect association (t 4.12, 4.40, 3.85, 3.57, 6.02) but collapses under country trends (0.53, −0.26, 0.02, −0.77, −1.94) and is the most sign-flipping driver; **paid employment is the cleanest null** (no wage-employment link to a schooling outcome beats random groupings in any kind of group; q≈1); **farm change** is group-specific; urbanisation and income → secondary completion are no better than random. The resolution arithmetic matters: a lone link needs about 5,440 draws to be certified at 5% false discovery, a cluster of 30 extreme links about 182, and 400 draws certify the strict tier's **35 up / 19 down / 15 sign-flip / 53 heterogeneity** links — the cluster, not the individual. **This is a between-country panel result, not evidence that electrification does not matter.** The micro literature finds positive effects of rural electrification and energy access on schooling; those estimates come from local variation our panel cannot see. The correct reading is that country-level electricity access is not separable from development here, not that energy access is irrelevant to households.


## 11. Supporting evidence III: credential inflation and the care loop
*This section integrates the care-credential record (`research/care-credential-2026-11-23` @ `e626cb8`,
pre-registered at `7356e76`).*

**The credential-inflation mechanism.** The theory's version: massification is positional; the credential
economy expands because credentials certify access to jobs, and the credential–occupation gap — female tertiary
attainment minus the share of female jobs in managerial and professional occupations — should predict lower
fertility, especially where attainment is already high (a saturation prediction). The data do not support it.
Across the countries with the required data the credential–occupation gap correlates **−0.15** with fertility
(about 2% of variance), while female attainment (−0.62) and the credentialed-jobs share (−0.65) correlate
strongly with it; in the horse race, attainment carries **−0.81 (t=−4.6)** and the gap **+0.33 (t=1.9)** — the
opposite sign — and with controls attainment is −0.80 (t=−2.85) and the gap +0.32 (t=1.61). The gap predicts
fertility **worse** in high-attainment countries (R² 0.17) than in low-attainment ones (R² 0.50), the opposite
of the saturation prediction. Attainment and the credentialed-jobs share correlate **+0.81** (r=0.807, n=46,
re-verified from the committed cross-section), so the gap is small relative to the level variables that move
together. The mechanism is not supported as a positional effect.

**The care-work loop.** The theory's version: the care share of female employment rises with the pipeline, and
mass schooling is partly absorbed by care work. The raw cross-section looks supportive — the care share of
female employment is **8.1%** in the bottom attainment tercile, **19.0%** in the middle and **28.4%** at the top
(148 countries) — but the association is **fully absorbed by income and urbanisation**: with log GDP per head in
the model the attainment coefficient is **+0.009 (t=0.17, n=140)** while log GDP carries +0.24 (t=2.5) and
adding urbanisation gives it +0.42 (t=3.4). The pre-registered killing test fires. The placebos are decisive:
replacing female care work with **male** care work gives an interaction of +0.18 (t=2.1) and replacing it with
**manufacturing** gives −0.19 (t=−3.5), so the unrelated-sector placebo produces a larger "effect" in the
predicted direction than care work does. Across 36 specifications, the care-share coefficient takes both signs
(from about −0.57 to +0.27) and its significance tracks the fixed effects, not the care measure. The care loop
is not supported.

**What this means for the paper.** Both mechanisms are parts of the theory of massification-as-formatting, and
both come back null on the data they can be tested on. That does not refute the broader institutional reading —
it says that two candidate mechanisms (positional credentialing and care absorption) are not visible in
cross-country data, and that the institutional reading must rest on the timing evidence of Sections 6–7 rather
than on these channels. The nulls are reported with the same prominence as the positive findings because they
are part of the paper's answer.

## 12. Implications
The finding matters in three places: for the theoretical debate about why mass schooling spread, for how the
classic historical cases should be read, and for the policy question of what lever actually moves massification.
It does not settle the first, and the paper is explicit about that; an ordering claim can shift the burden of
argument without identifying the mechanism.

### 12.1 For the massification debate: supply-side versus demand-led accounts

The human-capital account and the world-culture account have been argued for four decades, largely from
different kinds of evidence: returns-to-schooling estimates and earnings functions on one side, diffusion
patterns and institutional case histories on the other. The ordering evidence speaks to the debate on the
world-culture side, but in a specific and limited way.

For **world-culture theory** (Meyer 1977; Boli, Ramirez and Meyer 1985; Soysal and Strang 1989; Schofer and Meyer 2005), the finding supplies something the tradition has usually lacked: a timing fact at scale. The tradition argues that mass education is an institutional project that spreads through states and international models, not a local response to economic demand; the sequencing result shows that in late industrialisers the schooling take-off usually precedes the farm exodus, and that on pre-1990 series demand-first is a minority ordering (10–24% of identifiable countries) with a large tie/censoring band, while supply-side measures are the block associated with schooling expansion in the horse race. That is consistent with the tradition's prediction, but consistency is not identification: our data show timing and conditional association and cannot separate a state that built schools because it believed in the school as the form of the modern state from one that built them because it expected future demand, had fiscal capacity, or was competing with a neighbour. The finding also does not test the diffusion mechanism, and it would be a mistake to present it as proof that world culture caused massification.

For **human-capital theory** (Schultz 1961; Becker 1964; Mincer 1958, 1974; Goldin and Katz 2008; Acemoglu and Autor 2011), the finding is not a refutation but a boundary condition. The theory's core mechanism — returns to schooling shape investment in schooling, and technology raises those returns — is well supported by the returns literature; nothing here overturns it. What the ordering shows is that the timing implication of a general labour-demand account — the narrow wage-premium and paid-employment measures turning on before schooling — is not reproduced on pre-1990 series: demand-first is a minority ordering (10–24% of identifiable countries), with a large tie/censoring band that cannot be read as demand-last. The most defensible synthesis is that the demand story describes the **first industrialiser** — Britain, where industrialisation and the farm exodus precede mass schooling by 40-90 years — while a state-built-pipeline account is a better description of many **late industrialisers**, whose states expanded school systems in anticipation of, or for reasons independent of, demand that had not yet arrived.

### 12.2 Reading Prussia and Britain as a typology

The two classic cases are usually told as rival stories. The finding suggests they are better read as the two
poles of a typology of massification, with the sequence associated with who supplied the schooling.

| dimension | state-built pipeline (Prussia pole) | market-led (Britain pole) |
|---|---|---|
| who supplied | state, with compulsory statutes and an administrative apparatus | private, charitable and local provision, national statute late |
| timing relative to industrialisation | schools before industrialisation and before the farm exodus (80-120 years in Prussia) | industrialisation and farm exodus before national mass schooling (40-90 years in Britain) |
| what the statute does | creates schools and compels attendance; enforcement varies but the pipeline exists | ratifies and extends provision that demand has already created; 1870 Act after the transformation |
| the mixed cases | France: statute-led (1833) but attainment follows demand until the 1880s; US North: local public goods, state-supplied before the national farm exodus, high schools coincident with it | |

The typology is descriptive, not a theory: with four cases it cannot establish that the supplier is the operative
difference, only that the two poles show the sequence co-varying with the supplier. It is nonetheless useful
because it tells a referee where to look: if the typology is right, the ordering should weaken in the
early-industrialiser set and hold in the state-building set, and cases where the state was weak relative to the
market should look more like Britain. France is the instructive middle: the statute can lead without attainment
following, which is why the paper keeps the policy date and the attainment date separate. A future study with
proper historical series (Section 13) could test the typology rather than illustrate it.

### 12.3 For policy: state capacity versus labour-market demand as the lever

If the ordering is right, the policy implication is a sequencing one: **in a late-industrialising country, waiting
for the narrow labour-market demand variables to move before expanding schooling is waiting for the wrong
signal**, because on pre-1990 series those variables usually do not turn on before the schools do (and the
earlier wage-employment result that appeared to show otherwise is a data-start artefact). The lever associated
with historical massification was state capacity to build and staff a school system — finance, teachers, a
compulsory-law framework, an administrative apparatus — rather than the measured wage premium. That is consistent
with the state-building literature (Lindert 2004; Alesina and Reich 2013; Gradstein and Justman 2002) and with the
practical experience of countries that expanded schooling ahead of measured industrial demand.

Three cautions are essential, and the paper takes them seriously. First, **there is no causal estimate here**: the
policy inference is about the sequencing logic, not about effect sizes, and it would be overreach to say that
building schools "causes" development from this evidence. Second, **supply without quality is not massification**:
the paper's supply measures are spending, teachers and enrolment capacity, and it cannot speak to learning
outcomes, which the growth literature shows matter more than years of schooling. Third, **credential inflation is
a real risk of supply-side expansion**: the credential literature (Collins 1979; Spence 1973; Arrow 1973) and the
project's own credential test (Section 11) warn that expansion can outrun the jobs that justify it, and the care
loop and gap tests come back null rather than reassuring. The policy reading is therefore "build the pipeline
early, and watch the quality and the credential gap", not "build schools and growth follows".

### 12.4 What the implications are not

They are not a claim that schooling caused the agricultural transition, the fertility decline or growth; the
evidence is ordering and conditional association. They are not a claim that institutions always lead; Britain is
the counterexample, and France and the United States are mixed. They are not a claim that the demand story is
wrong in general; it is the better description of the first industrialiser. And they are not a claim that the
paper has identified the mechanism; it has identified the order of events, which is the first thing a mechanism
has to explain.

## 13. Future research: what would settle it
The paper's central vulnerability is that its dates are ours — literature-standard dates and our own event
definitions — and its central claim is an ordering claim. Future work should attack both, in the order of what
would most change the conclusion.

### 13.1 The ordering itself: recoding and re-detection

Before any new data, the ordering claim needs a robustness pass that this session could not complete (the raw
series were on a server that went down, so alternative-threshold recoding was not possible). Concretely: re-detect
the three events under alternative definitions — statute versus measured enrolment for schooling; 1 versus 2
years of schooling per decade; 3 versus 5 points of agricultural-employment decline; different windows and
smoothing rules — and report how many of the 61 forward cases flip under each. A second coder should code a
sample of countries blind to the first coder's dates, with a pre-registered agreement threshold, and a
date-by-date source table with page references should be published for every country in the headline table. What
this would settle: whether the 61/64 count is a property of the events or of our definitions. What it would not
settle: causality.

### 13.2 Historical enrolment series: measuring the classic cases properly

The four historical cases are the paper's weakest evidence because their dates are literature-standard. Four
series would turn them into measurements:

The four series are Prussian enrolment 1800–1870 (Flora, Kraus and Pfenning 1983; Lindert 2004), UK school attendance 1850–1900 (Newcastle Commission 1861; Board of Education annual reports), French primary enrolment 1830–1900 (Diebolt's series; the ministry's *Statistique de l'enseignement primaire*) and US high-school enrolment 1890–1940 (US Historical Statistics, series H-598 onward). Each would replace a literature date with a measured series; none would identify causal effects, only date the events better and attach series-level uncertainty to the lead/lag.

What these series would not do: identify causal effects. They would date the events better, and they would allow
the lead/lag to be quantified with the uncertainty of each series rather than as point dates. Definitional
changes in the series (who counts as enrolled, attendance versus registration) are themselves a research problem,
not a nuisance.

### 13.3 Compulsory-schooling-law dates as treatment

The strongest design the project can see is to use the staggered adoption of compulsory-schooling laws as a
natural experiment. The data exist in Flora and Alber (1981), Flora, Kraus and Pfenning (1983) and the subsequent
literature; the design is an event study or difference-in-differences around law adoption, with pre-trends and
heterogeneity by enforcement. What it identifies: the effect of a **law**, not of schooling per se, on enrolment,
attainment, fertility and labour supply — a policy-relevant parameter, and a test of whether state action moved
the pipeline. Threats: laws are endogenous to demand and to state capacity, enforcement varied enormously (the
Prussian case is a warning), adoption is bundled with other reforms, and anticipation can shift effects earlier.
A credible design would need enforcement variation (e.g. district-level enforcement intensity) and would have to
be pre-registered.

### 13.4 Subnational school-construction variation

The most promising design for the mechanism is subnational: district-level school openings or school-construction
programmes, matched to census attainment, fertility and employment. What it identifies: local effects of school
supply on attainment and on the labour market, with better control of national policy and income; spillovers and
migration are the main threats, and they are measurable. Data needs: school registers or construction records,
census microdata, and boundary maps. The project does not have these data, but the design is the natural next
step for a country-level research programme, and it is the design that could turn the supply-side reading from a description
into an estimate.

### 13.5 Cohort-linked microdata for the generational claim

The theory's generational wording — a cohort that entered school as the farm exodus accelerated had fewer
children — needs cohort-linked microdata: DHS or IPUMS samples with attainment, fertility and employment for the
same women. What it identifies: the individual-level relationship, the wealth horse race, and the quantum-tempo
decomposition that the project's cell-level (ecological) DHS gradient could not test. The data gap is documented
in the record (the public DHS API exposes aggregates only; individual recodes sit behind registration).

### 13.6 What the current evidence cannot claim

Stated plainly, so that no reader mistakes the paper for more than it is:

- The historical **dates are literature-standard, not verified** in this pass; every one is labelled UNVERIFIED,
  and a referee should spot-check two.
- The **event definitions are ours** (1 year of schooling per decade; 3 points of agricultural decline; 10-year
  windows), chosen in advance but not given by nature; alternative thresholds have not been run.
- There is **no causal identification**: the horse race is a decomposition, the event ordering is timing, and the
  policy implications are about sequencing logic, not effect sizes.
- The data are **period series, not cohorts**; the generational claim is not tested here.
- The 64-country sample is **selected on data availability**, and the historical cases are a **dated argument,
  not a sample**.
- The literature search could not use subscription databases (no Scopus/Web of Science/EconLit), so "as far as
  our recorded search can find" is a real qualification, not boilerplate.

## 14. What we know now: synthesis and the "what we know now" box
### 14.1 The synthesis verdict

The paper set out to test the timing prediction that separates the demand-led and institutional accounts of
massification. The evidence, taken together, supports a conditional synthesis:

1. **In the late-industrialising countries where the modern panel can date the events, schooling precedes the release of labour from agriculture**: 61 of 64 countries, a median lead of 26 years (bootstrap 22–26 years), reverse ordering 5% (0–11%). Schooling precedes the fertility decline in only 37.5% of those countries under a strict ordering (26.6–50.0%; 31.3% simultaneous, 31.3% fertility-first; the record JSON's 68.75% counted simultaneous take-offs as schooling-first and is not used). The sequencing is not a cohort-level measurement, but it is a systematic event-ordering, not a handful of cases.
2. **Structural change on series that go back before 1990 is neither cleanly ordered nor ruled out**: demand-first is 10.0% (GGDC non-agricultural employment), 15.4% (urbanisation), 24.1% (industry value added) and 18.8% (agricultural value added) of identifiable countries, with all-country bounds of 6.7–53.0% and another 21–43% in weak ties or left-censored cases. **Schooling and structural change move together, with schooling typically but not universally first.** The retired "7%" figure came from the 1991-start wage-employment series and is not used. The fair sample turns together (76% vs 79%), and the horse race puts the conditional association on supply (+0.456, SE 0.174, vs +0.006, SE 0.203; n=78, 51 countries) — a decomposition, not a test.
3. **The historical cases split in a way that makes the modern regularity conditional, not universal**: Prussia shows state supply 80–120 years ahead of industrialisation and the farm exodus; France separates the statute (1833) from the attainment (1880s); Britain inverts the ordering (industrialisation and the farm exodus 40–90 years before mass schooling); the northern United States is supply-side in the local-public-goods sense. All historical dates are UNVERIFIED literature standard.
4. **The agricultural floor — the strongest version of the demand story — is real in the cross-section and not identified in the dynamics**: input prices and intensity are negatively related (−1.13, SE 0.15; −1.28, SE 0.11); inputs explain 55–69% of the agricultural labour-productivity gap; but the dynamic lead-lag is not identified (the reverse association is *stronger*), the downstream ten-year effects are precise nulls, and the joint model identifies only two of five parameters.
5. **Scaling regularities are between-country regularities, not laws of change**, and the universal fertility–attainment collapse curve is rejected (country identity explains 71.6% of the residual); theta/gamma is not estimable with the data that exists.
6. **The mechanisms the formatting reading might use are not supported in the data they can be tested on**: no driver is robust everywhere (only five links, all fertility-side); electricity is the most fragile driver and paid employment the cleanest null; the credential–occupation gap is almost unrelated to fertility (−0.15 vs −0.62 for attainment) and predicts the wrong way; the care-work loop is absorbed by income and urbanisation, and male-care and manufacturing placebos behave like the treatment.

### 14.2 "What we know now" box

> **What we know now — massification**
>
> - **The sequence**: in 61 of 64 late-industrialising countries, the schooling take-off precedes the release
>   of labour from agriculture, median gap 26 years (22–26, bootstrap); reverse 5% (0–11%).
> - **Which comes first, supply or demand**: the raw event ordering looks demand-led (73%), but that is a data
>   artefact; the fair sample turns together (supply 76%, demand 79%) and the horse race puts the association
>   on supply (+0.456, SE 0.174) not demand (+0.006, SE 0.203; n=78, 51 countries).
> - **Demand timing on pre-1990 series**: demand-first is 10.0% (GGDC), 15.4% (urbanisation), 24.1%
>   (industry) and 18.8% (agriculture) of identifiable countries; bounds 6.7–53.0%; another 21–43% weak ties
>   or left-censored. Schooling and structural change move together, with schooling typically first.
> - **A supply-side event study**: fee abolition in eight African countries with verified dates (1994–2005)
>   is followed by large primary-enrolment gains (Callaway–Sant'Anna post-effects +22 to +29 points, flat
>   pre-trends at −2/−3/−4, TWFE similar); the on-impact interval spans zero and coverage is sparse —
>   "consistent with" a supply effect, not a causal estimate.
> - **History**: Prussia shows state supply 80–120 years ahead; France statute-led with attainment
>   demand-following; Britain demand-led by 40–90 years; US North supply-side locally. All dates unverified.
> - **The agricultural floor**: real in the cross-section (elasticities 1.24/1.11 OLS, 1.73/1.76 at the
>   extremes; inputs explain 55–69% of the gap) but no identified dynamic sequence.
> - **Scaling**: between-country regularities, not laws of change; no universal fertility–attainment collapse
>   curve (country effects 71.6% of residual).
> - **Drivers and mechanisms**: no robust driver among development variables; credential inflation and the
>   care loop are null in the data they can be tested on.
> - **The framing**: a late-industrialiser regularity, not a universal law; the data are better described
>   as schooling and structural change moving together, with a supply-side conditional association in the
>   horse race — not an identified cause.

### 14.3 The reading, stated carefully

The defensible interpretation is a **political-economy reading of timing**: where the state was the supplier,
school systems were typically built first, for reasons that were partly political (nation building,
citizenship, social cohesion) and partly institutional (the legitimate form of the modern state); where
industrialisation came first, schooling arrived later as the market expanded and the sequence reverses. The
evidence is timing and conditional association, so the correct verb is "is better described as" rather than
"is caused by".
The paper's contribution to the theory is the systematic event comparison and the horse race, plus the
demonstration that the strongest demand-side mechanism (the agricultural floor) does not deliver the sequence
the theory needs. The paper's contribution to the empirical literature is a set of verified, traceable results
and a set of honest nulls.


## 15. Limitations and referee objections
We state the objections a domain referee would make, and whether the current evidence answers them.

**1. "Your event dates are period data, not cohorts; you cannot speak about a cohort's own outcomes."** True and
accepted. The sequencing claim is about **events in countries**, not about linked cohort histories. The theory's
generational wording would require cohort-level attainment, employment and fertility for the same women (DHS
or census-linked data), which this project does not have. The paper's language is therefore "schooling
take-off precedes labour release", not "the cohort that entered as mechanisation accelerated had lower
fertility". The cohort-level test is stated as future work; the event ordering is the strongest claim the data
can carry.

**2. "The dates are the paper - a different coding gives a different count."** Yes. Section 6 (robustness subsection) reports the perturbation exercise: 93% of forward cases exceed a 10-year gap and a systematic 15-year error is needed to cut the forward share materially. But we did **not** re-detect the events under alternative definitions (statute vs enrolment; 1 vs 2 years of schooling; 3 vs 5 points of agricultural decline), because the raw series were unreachable after the box went down. That recoding is the paper's central empirical vulnerability and the first item for the next pass; a date-by-date source table with page references is also owed for the historical cases.

**2b. "Your headline sequencing result is a selection of the countries that happen to have data."** Partly true.
The 64 countries are those where all three events are detectable in the 1965–2010 window; they over-represent
late industrialisers, which is exactly the population the paper claims to describe. The historical cases
(Section 8) are how we check backwards, and they show the regularity does not extend to the first
industrialiser. The paper says "late-industrialiser regularity" throughout for this reason.

**3. "Your supply-versus-demand raw ordering is demand-led; you overturned it with a small fair sample."** The
raw ordering is indeed demand-led, and we report it first. The fair sample is 33 countries and is selected on
data availability, so it cannot carry a strong claim alone; that is why the horse race — which does not depend
on event dating — is the primary supply-demand evidence, and the horse race puts the association on supply.
The honest statement is that the raw ordering is uninformative because of censoring, not that it is wrong.

**4. "The horse race is endogenous — education spending responds to schooling and income."** Yes. We do not
claim causality, and the empirical-strategy section (Section 5) says so explicitly. The horse race is used only to arbitrate between the two
theories' **descriptions**, and the paper's causal language is restrained accordingly. An instrument for
education spending or state capacity would be the next step, and none is available here.

**5. "The historical dates are unverified."** Yes — every one is labelled UNVERIFIED literature standard, and
the primary series that would verify them are named. The four cases are a dated argument, not a measurement.
A referee should read Section 8 as a synthesis of the historical literature under one set of definitions, not as
new archival work.

**6. "The agricultural-floor test contradicts a well-known paper."** No: the cross-section **replicates** BKKM's
mechanism (direction, magnitudes in the right range, intensification share). What fails is the **dynamic
sequence** in our panel and the downstream effects at ten years. The paper says the cross-section is real and
the sequence is not identified; that is a limit of the design, not a refutation of BKKM.

**7. "The scaling section criticises a formalism it cannot test."** Correct, and the paper says so: theta/gamma
are not estimable with 1-digit ISCO data, and no proxy is presented as a test. The scaling results are used to
police the theory's language ("laws" vs "regularities"), not to refute it.

**8. "The null driver and mechanism results may be power-limited."** The grouping multiverse nulls are powered
by 400 random groupings and 38.4 million regressions, with a resolution analysis showing what 400 draws can and
cannot certify; the ten-year downstream null has a minimum detectable fertility effect of about 0.016 births.
The nulls are therefore informative, not merely absence of evidence. Where a test is underpowered, it is
labelled.

**9. "This is a synthesis of the project's own work, not a new dataset."** True. The paper is a synthesis with
four new empirical elements: the event comparison between schooling and structural change (as far as we know,
not previously assembled in this form), the horse race between measured supply and demand, the pre-1990
demand-timing re-estimate that replaced the retracted "7%" figure, and the fee-abolition event study. It is not
presented as a new data collection.

**11. "Your old labour-demand result said 7%; why is it gone?"** The 7% figure was computed on wage-employment
and paid-employment series that begin in 1991, so on a 1965–2010 event window it could not have preceded a
schooling take-off for most countries; it is a data-start artefact, retracted project-wide, and is replaced by
the pre-1990 series in Section 6.5. The replacement does not rule demand out: demand-first is 10–24% of
identifiable countries, bounds 6.7–53.0%, with another 21–43% weak ties or left-censored.

**12. "The fee-abolition event study is causal, surely?"** It is an event study with checked pre-trends, so it
licenses the phrase "consistent with" for a supply effect on primary enrolment — no stronger. The treated
sample is seven to eight countries, the on-impact interval includes zero, four fee dates are unresolved and
excluded from the main specification, and the outcome is an enrolment ratio, not attainment; the design says
nothing about massification or the schooling-versus-farm-exit ordering.

**10. "Publication fit."** The paper is a synthesis with new tests; it fits a review/synthesis venue
(*Review of Educational Research*, *Annual Review of Sociology*, *Sociology of Education*) or a development
economics venue (*World Development*, *Journal of Development Economics*). It does not fit *Explorations in
Economic History* as a standalone archival paper, because the historical section is a synthesis of literature
dates, not new archival measurement; that is a deliberate division of labour with the historical record, which
names the archival work needed.

## 16. Conclusion
Massification is usually told as a demand story: factories and cities raise the return to schooling, and
schooling follows. This paper tested the timing that story requires across 64 late-industrialising countries and
found a different ordering: the schooling take-off precedes the release of labour from agriculture in 61 of
them, by a median of 26 years; on pre-1990 structural-change series, demand-first is a minority ordering
(10–24% of identifiable countries) with another 21–43% in weak ties or left-censored, so demand is neither
eliminated nor cleanly ordered; the raw broad-proxy demand-first appearance is a data artefact, and in the fair
comparison the two sides turn together, with the horse race putting the conditional association on supply. A
fee-abolition event study is consistent with a supply effect on primary enrolment, with the caveats of sparse
coverage and an on-impact interval that includes zero. The historical cases show why the answer is conditional:
Prussia built its schools a century before it industrialised; Britain industrialised before it schooled. The
framing that survives is **a late-industrialiser regularity, not a universal law**, and the verb is "is better
described as" rather than "is caused by". The agricultural floor is real but does not deliver the sequence;
scaling regularities are regularities, not laws; the credential and care mechanisms are null in the data they
can be tested on. What remains is a clear, traceable, falsifiable statement about the order of events in
massification, an honest set of limits, and a research agenda — cohort-linked microdata, archival verification
of the historical dates, and an instrument for state capacity — that would let the next pass turn the
correlation into identification.

---


## Appendix A. Evidence labels, data tiers and verification status
Section numbers refer to the paper's top-level numbering. Every number in the revised draft was re-checked
against the committed source record and recomputed where the record's files allow it; the recomputation is
`scripts/verify_revision_numbers.py` and its output `data/revision_verification.json` (41/41 checks pass).

| section | evidence | data tier | label / source |
|---|---|---|---|
| 3 | literature claims | — | in-text citations; DOI and Crossref status in `claims-prior-art.md` and `refs.md` |
| 6 | 61/64 sequencing, median 26 years, bootstrap CI; fertility strict ordering 37.5% | reconstructed event dates from observed/reconstructed series | recomputed in `verify_revision_numbers.py` (`subsistence-v2 @ ce66cfc`) |
| 7.1–7.4 | raw 28%/73%; fair 76%/79%/39%; horse race +0.456/+0.006 | observed/reconstructed | recomputed (`supply-demand @ 963e5e5`) |
| 7.5 | E6 demand-first 10.0/15.4/24.1/18.8%; bounds 6.7–53.0%; ties 21–43%; N3 0.0–30.8% | observed (GGDC, WDI) | recomputed from `data/e6_summary.json`, `data/n3_recommendation.json` (`e6e8 @ 2d19da7`) |
| 7.6 | E8 fee-abolition CS/TWFE event study | observed outcome (WDI GER); verified dates | recomputed from `data/e8_results.json`, `data/fee_dates.csv` (`e6e8 @ 2d19da7`; `task-49 @ 9a0fd69`) |
| 8 | Prussia/France/Britain/US dates and percentages | literature-standard, not re-measured | **UNVERIFIED literature standard**; our own panel cannot see them |
| 9 | elasticities, intensification share, dynamic nulls, model | observed inputs; model simulated | verified in record (`subsistence @ 41f6429`, `subsistence-v2 @ ce66cfc`); model numbers are simulation, not history |
| 10 | scaling exponents, collapse-curve rejection, driver nulls | reconstructed panel | verified in records (`scaling @ fd691a6`, `grouping-multiverse-400 @ 1152cec`) |
| 11 | credential gap and care loop numbers | observed ILO/WDI | verified in record (`care-credential @ e626cb8`) |


## Appendix B. Reproduction and provenance
Every number in Sections 6–11 is a field in a results file on a named branch at a named commit; the
claims-to-source map (`claims-to-source-map.md`) lists claim, number, branch @ commit, file and field. The
revision recomputed the quoted numbers against committed copies of the source records in `data/`; the
recomputation script and its output are `scripts/verify_revision_numbers.py` and
`data/revision_verification.json`. The
scripts that produce the numbers are in the corresponding records, and the pre-registrations are the first
commits of their branches. No new heavy computation was done for this paper: it is a synthesis and integration
of verified records plus the reference-verification run (Crossref API, this branch). The literature search
strategy is recorded in `search-strategy.md`; the prior-art tables and reference list are
`claims-prior-art.md` and `refs.md`.


## Appendix C. Data gaps, stated not proxied
1. **Cohort-linked microdata** (the theory's generational claim): not available in this project; DHS/other
   microdata were not obtainable without registration (documented in the massification record).
2. **Compulsory-schooling-law dates** across countries: only the project's six-system policy timeline and the
   four historical cases; a full literature compilation is future work.
3. **Historical enrolment series** (Prussia, Britain, France, US): named primary sources; not digitised in this
   pass.
4. **City-size distributions / function-category depth**: UN WUP and GeoNames failed; 1-digit ISCO is the
   ceiling; the theta/gamma formalism is therefore not estimated.
5. **Credential registries and care-sector detail**: ILO SDMX only; BLS and Credential Engine returned 403.
6. **The pilot of the paper's own design on cohort data**: not possible without data; stated as the next step.
