# Claims → closest prior art (Paper M)

**Verification discipline.** Every DOI below was queried against `api.crossref.org` (query.bibliographic, title +
year matching) on 24–25 Nov 2026; the paper's own run is `data/refs_crossref.json` (script
`scripts/verify_refs_crossref.py`), and the section leads' runs are referenced where their entries are used.
Status: **Crossref ✓** = resolved with matching title/year; **WEAK** = title similar, year/venue unconfirmed;
**no DOI / not returned** = cited from bibliographic knowledge and explicitly flagged. Books, reports and some
working papers have no Crossref DOI; they are not presented as verified. "New" never means "first": for each
claim the table states which components are replicated from the literature and what this paper adds on top.
The search strategy is recorded in `search-strategy.md`.

---

## Claim 1 — In late-industrialising countries, the schooling take-off precedes the release of labour from agriculture (61 of 64 countries; median lead 26 years; reverse ordering 5%, 0–11%)

| work | what it shows | status | new vs replicated |
|---|---|---|---|
| Boli, Ramirez & Meyer (1985), *Comparative Education Review* 29(2):145–170 | origins and expansion of mass education are not driven by industrial demand; nation-state model | Crossref ✓ 10.1086/446504 | **replicated**: mass schooling can precede economic demand |
| Soysal & Strang (1989), *Sociology of Education* 62(4):277–288 | first mass education systems in 19th-c. Europe follow state-building, with uneven economic demand | Crossref ✓ 10.2307/2112831 | replicated (European cases) |
| Meyer, Ramirez & Soysal (1992), *Sociology of Education* 65(2):128–149 | world expansion of mass education 1870–1980 | Crossref ✓ 10.2307/2112679 | replicated (diffusion) |
| Benavot & Riddle (1988), *Sociology of Education* 61(3):191–210 | primary expansion 1870–1940 loosely coupled with development | Crossref WEAK (title/year) 10.2307/2112627 | replicated |
| Goldin & Katz (2008), *The Race between Education and Technology* | US high-school movement; demand-led reading | no DOI (book) | contrast case: demand-led in the first industrialiser |
| Boppart, Kiernan, Krusell & Malmberg (2023), NBER WP 31101 | agricultural labour share as equilibrium outcome of relative input prices | Crossref ✓ 10.3386/w31101 | framing + mechanism, not the event ordering |
| Porzio, Rossi & Santangelo (2021), NBER WP 29390, *The Human Side of Structural Transformation* | human capital accumulation as a driver of structural transformation — education leading sectoral reallocation | Crossref ✓ 10.3386/w29390 (re-verified 24 Nov 2026) | **closest competitor**: same direction (education before reallocation) but a different design — a quantitative model with micro evidence on skill reallocation, not a cross-country event comparison with bootstrap intervals; the two are complementary, and this paper's contribution is the assembly and the supply/demand decomposition |
| **This paper** | **common pre-registered event comparison of schooling take-off vs agricultural release across 64 countries, with bootstrap intervals and a fairness correction** | — | **new assembly**: the event-ordering comparison at this scale; the institutionalist claim tested as timing rather than diffusion |

**Closest competitor.** Porzio, Rossi and Santangelo (2021), *The Human Side of Structural Transformation* (NBER
WP 29390, Crossref ✓ 10.3386/w29390), is the closest prior claim in direction: they argue human capital
accumulation drives structural transformation, i.e. education before sectoral reallocation. Our ordering result is
consistent with that, but the designs differ: theirs is a quantitative model with micro evidence on skill
reallocation, ours is a common cross-country event comparison with bootstrap intervals and a supply/demand
decomposition. The paper treats them as complementary and does not claim precedence.

**Not previously assembled in this form (as far as we know; search recorded):** the specific event-ordering
comparison of schooling take-offs against agricultural-labour-release dates across a common country panel. The
components are old: mass education before demand (world-polity), the agricultural transition (structural change),
case narratives (economic history). No "first" is claimed.

## Claim 2 — Labour-market demand (wage premium, paid employment) does not lead the schooling take-off (7% of 58 countries)

| work | what it shows | status | new vs replicated |
|---|---|---|---|
| Schultz (1961), *American Economic Review* 51(1):1–17 | human capital investment; demand-side logic | Crossref WEAK 10.2307/2551855 | the theory being tested |
| Becker (1964), *Human Capital* | investment calculus; returns drive schooling | no DOI (book) | theory |
| Mincer (1958), *Journal of Political Economy* 66(4):281–302 | earnings function; returns estimated from schooling | Crossref ✓ 10.1086/258055 | method behind demand measures |
| Goldin & Katz (2008) | US: education raced technology; demand-led | no DOI (book) | the strongest demand-led case, which the US case supports |
| Acemoglu & Autor (2011), *Handbook of Labor Economics* | skill-biased technical change | Crossref ✓ 10.1016/S0169-7218(11)02410-5 | theory of labour demand for schooling |
| Psacharopoulos & Patrinos (2018), *Education Economics* 26(5) | returns to schooling ~8-9% | Crossref ✓ 10.1596/30154 (WP) | benchmark: returns exist; our result is about *timing* |
| **This paper** | **the demand variables the theory names (wage premium, paid employment) tested for precedence against schooling take-off** | — | **new test**: 7% lead; the raw 73% demand-first is a data-availability artefact |

## Claim 3 — Supply-side measures dominate the horse race (+0.456, SE 0.174, vs +0.006, SE 0.203; n=78, 51 countries)

| work | what it shows | status | new vs replicated |
|---|---|---|---|
| Meyer (1977), *American Journal of Sociology* 83(1):55–77 | education as institution; expansion not reducible to economic demand | Crossref ✓ 10.1086/226506 | replicated (interpretation) |
| Flora & Alber (1981), in *The Development of Welfare States in Europe and America* | welfare/schooling legislation as state-building, comparative dates | no DOI (book chapter) | replicated (state supply matters) |
| Lindert (2004), *Growing Public* | public schooling spending has political roots | no DOI (book) | replicated (supply is political) |
| Alesina & Reich (2013), "Nation building and education" (working paper) | nation-building motive for public education | not returned by Crossref in-session | replicated (motive) |
| Gradstein & Justman (2002), *American Economic Review* 92(4):1192–1204 | education as social-cohesion public good | Crossref ✓ 10.1257/00028280260344740 | replicated (political supply) |
| Schofer & Meyer (2005), *American Sociological Review* 70(6):898–920 | worldwide higher-education expansion | Crossref ✓ 10.1177/000312240507000602 | replicated (institutional expansion) |
| **This paper** | **standardized horse race between measured supply and demand blocks in a country panel** | — | **new test** on this question; association, not causal identification |

## Claim 4 — The historical sequence splits: Prussia supply-led (80–120 yrs), France statute-led/attainment-following, Britain demand-led (40–90 yrs), US North supply-led locally — all dates UNVERIFIED literature standard

| work | what it shows | status | new vs replicated |
|---|---|---|---|
| Schleunes (1989), *Schooling and Society: The Politics of Education in Prussia and Bavaria 1750–1900* | Prussian compulsory schooling state before industrialisation | no DOI (book) | replicated (case) |
| Flora, Kraus & Pfenning (1983), *State, Economy and Society in Western Europe 1815–1975* | legislative dates | no DOI (handbook) | source for dates (unverified in session) |
| Diebolt, Jaoul & San Martino (2005) | French education series; statute vs attainment | Crossref NO_MATCH in-session (working paper/chapter) | replicated (French case) |
| Sanderson (1999), *Education and Economic Decline in Britain 1870–1990* | British schooling after industrialisation | no DOI (book) | replicated (British case) |
| Mitch (1984), *Journal of Economic History* 44(2):385–394 | underinvestment in literacy in 19th-c. England | Crossref WEAK 10.1017/S0022050700034140 | replicated |
| Goldin & Katz (2008); US Historical Statistics series H-598+ | US common schools and high-school movement | no DOI (book; series) | replicated (US case) |
| **This paper** | **one set of pre-registered definitions applied to four cases chosen by who supplied schooling; date provenance labelled** | — | **new comparison frame**; the case narratives themselves are replicated, not new |

## Claim 5 — The agricultural-floor mechanism is real in the cross-section but not identified in the dynamics (elasticities 1.24/1.11 OLS, 1.73/1.76 extremes; inputs explain 55–69%; dynamic lead-lag not identified)

| work | what it shows | status | new vs replicated |
|---|---|---|---|
| Boppart, Kiernan, Krusell & Malmberg (2023), NBER WP 31101 | nested CES; relative input prices; intensification ~two-thirds of productivity gap | Crossref ✓ 10.3386/w31101 | **replicated** (partial): elasticities below theirs, intensification 55–69% |
| Restuccia, Yang & Zhu (2008), *Journal of Monetary Economics* 55(2):234–250 | agriculture and aggregate productivity | Crossref ✓ 10.1016/j.jmoneco.2007.11.006 | replicated framing |
| Gollin, Parente & Rogerson (2002), *American Economic Review* 92(2):160–164 | role of agriculture in development | Crossref ✓ 10.1257/000282802320189177 | replicated |
| Adamopoulos & Restuccia (2014), *American Economic Review* 104(6):1667–1697 | farm size and productivity | Crossref ✓ 10.1257/aer.104.6.1667 | benchmark |
| Caselli & Coleman (2001), *Journal of Political Economy* 109(3):584–616 | agriculture's role in income differences | Crossref ✓ 10.1086/321015 | benchmark |
| **This paper** | **the sequencing test of the floor: inputs before release? Not identified; downstream effects precise nulls** | — | **new negative/limit result**: cross-section real, dynamics not identified |

## Claim 6 — Scaling laws in these data are between-country regularities, not laws of change; no universal fertility–attainment collapse curve; theta/gamma not estimable

| work | what it shows | status | new vs replicated |
|---|---|---|---|
| Heaps (1975), *Information Retrieval* (book); Heaps exponent 0.4–0.6 | sublinear category growth | no DOI (book) | benchmark: our 0.333 (SE 0.011) is below it |
| Petersen et al. (2012), *Scientific Reports* 2:313 | scaling in word use | Crossref ✓ 10.1038/srep00313 | replicated direction |
| Tria et al. (2014), *Scientific Reports* 4:5890 | generative model of category growth | Crossref ✓ 10.1038/srep05890 | replicated direction |
| Yang, Bettencourt et al. (2026), *PNAS* | function diversity and theta/gamma formalism | Crossref ✓ 10.1073/pnas.2509729123 | **test target**; not estimable with 1-digit data |
| Bettencourt (2013), *Science* 340:1438–1441 | urban scaling | Crossref ✓ 10.1126/science.1235823 | benchmark |
| Schofer & Meyer (2005) | higher-education expansion | Crossref ✓ 10.1177/000312240507000602 | framing |
| **This paper** | **between/within test of education–income exponents; rejection of the universal collapse curve (country effects 71.6% of residual); Heaps/threshold/Zipf/urban S-curve audits** | — | **new audits and the rejection**; the regularities themselves are known |

## Claim 7 — No driver is robust everywhere; the credential–occupation gap is not a positional fertility mechanism; the care loop is absorbed by income

| work | what it shows | status | new vs replicated |
|---|---|---|---|
| Spence (1973), *Quarterly Journal of Economics* 87(3):355–374 | signaling | Crossref ✓ 10.2307/1882010 | theory being tested |
| Arrow (1973), *Journal of Public Economics* 2(3):193–216 | education as filter | Crossref ✓ 10.1016/0047-2727(73)90013-3 | theory |
| Collins (1979/2019), *The Credential Society* | credential inflation and positional competition | Crossref ✓ 10.7312/coll19234 (2019 reissue) | theory |
| Bills (2003), *Review of Educational Research* 73(4):441–469 | credentials, signals, screens | Crossref ✓ 10.3102/00346543073004441 | theory |
| Hungerford & Solon (1987), *Journal of Labor Economics* 5(2):175–189 | sheepskin effects | Crossref ✓ 10.1086/298143 | benchmark for credential effects |
| Jaeger & Page (2004), *Journal of Human Resources* 39(3):730–753 | degrees and signaling | Crossref ✓ 10.3368/jhr.XXXIX.3.730 | benchmark |
| **This paper** | **the credential–occupation gap tested against fertility (corr −0.15; wrong-signed interaction); care loop absorbed by income/urbanisation; male-care and manufacturing placebos** | — | **new tests** of the mechanism; nulls reported with the same prominence |
| Cleland & Wilson (1987), *Population Studies* 41(1):5–30 | demand theories of fertility transition | Crossref ✓ 10.1080/0032472031000142516 | framing for the fertility outcomes |

---

## What this paper is *not* claiming

- It is **not** claiming to be first at the event-ordering question; it claims a new common assembly, and
  `search-strategy.md` records the search. The historical literature has argued the sequence case by case for
  decades (Prussia, Britain, France, US), and the world-polity literature has argued that mass education
  precedes economic demand since the 1980s.
- It is **not** claiming that supply *causes* schooling: the horse race is a conditional association, stated as
  such in the paper.
- It is **not** claiming that the historical dates are verified: every date is labelled **UNVERIFIED literature
  standard**, and the primary series needed to verify them are named.
- It is **not** claiming a universal law: the framing throughout is **"late-industrialiser regularity, not a
  universal law"**.

---

## Independent-audit gaps, and how this paper addresses them

The independent auditor (`novelty-review`, task-35) sent a prior-work list and a referee memo
(`research/records/2026-11-24-lit-audit/referee-memo-paper-M.md`, branch `research/lit-audit-2026-11-24`) before
this branch was pushed. Its three strongest objections are addressed in the paper as follows; this section records
the additions so the diff is auditable.

**Objection 1 — "schools before factories is not new."** Accepted. The paper now cites Sandberg (1979, the
"impoverished sophisticate"), Mitch (1992), the world-polity school, Squicciarini and Voigtländer (2015), de
Pleijt and van Zanden (2016) and Graff as the prior claims, in the introduction (Section 1), and reframes the
contribution as the **systematic 61/64 event coding plus the supply-versus-demand decomposition**, not the
direction of the historical pattern. No sentence claims awareness-failure. Works added: Sandberg 1979
(10.1017/s0022050700096418), Mitch 1992 (10.9783/9781512807189), Goldin & Katz 1999 (10.3386/w6439; published
chapter 10.1017/cbo9780511572777.012), Squicciarini & Voigtländer 2015 (10.1093/qje/qjv025), de Pleijt & van
Zanden 2016 (10.1093/ereh/hew013), Graff 1979/2017 (10.4324/9781315132969), Lindert 2004 (10.1017/cbo9780511510717),
Benavot & Riddle 1988 (10.2307/2112627), Meyer, Ramirez & Soysal 1992 (10.2307/2112679), Schofer & Meyer 2005
(10.1177/000312240507000602). All marked in `refs.md` as auditor-verified (V/W/U).

**Objection 2 — "the dates and coding are the paper."** Accepted and partly answered: Section 5.3 now reports the
date-perturbation robustness (median gap 26 years, IQR 17–29; 93% of forward cases exceed a 10-year gap; a uniform
15-year error is needed to cut the forward share materially). Alternative-threshold re-detection could not be run
(the raw series were on the unreachable box) and is named as the paper's central remaining vulnerability, with a
date-by-date source table owed for the historical cases. Demand-side theory added: Galor & Moav 2006
(10.1111/j.1467-937x.2006.00370.x) and Becker & Woessmann 2009 (10.1162/qjec.2009.124.2.531).

**Objection 3 — "the horse race is under-identified."** Accepted; the paper now calls it a **decomposition, not a
test**, states that both blocks correlate with development/state capacity/demography, and names the exogenous
variation that would make it a test (compulsory-schooling-law adoption, church-state competition, colonial
schooling policy, school construction with a credible instrument). Acemoglu & Restrepo 2018
(10.1257/aer.20160696) added on the mechanisation/labour-demand channel.

**Secondary risks.** Scaling: the section is now explicitly a **diagnostic frame**, with theta/gamma not fitted and
the data gap stated; Bettencourt et al. 2007 (10.1073/pnas.0610172104) and Yang et al. 2026 (arXiv 2208.06487;
PNAS DOI not verified) added. Credential: Collins, Spence and Arrow were already cited; Bills & Brown 2011
(10.1016/j.rssm.2011.01.004) added; the paper states the contribution can only be the measurement, and that the
deep credential-to-occupation measurement is a data gap. Drivers null: the paper now carries the **positive micro
literature** on rural electrification/energy access and states plainly that the country-panel null is not evidence
that energy access does not matter (micro DOI 10.1080/00220388.2026.2727160 and the small-hydropower/energy-poverty
studies supplied by the audit; status to be re-verified before submission).

**Status of the auditor diff.** These additions are our response to the memo; the auditor's full
claims-map diff will be run against this file after the push, and any remaining discrepancy will be resolved here
before submission.
