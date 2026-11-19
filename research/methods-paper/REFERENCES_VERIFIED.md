# References verified for the methods paper

Checked 14 November 2026 against publisher, Crossref, RePEc, library-catalogue and author-page records fetched that day. Method: for each item I fetched a bibliographic record (usually the Crossref record for the DOI, or a publisher/catalogue page) and compared it with the citation. "Claim" means the specific thing the outline or the task attributes to the work; I only mark a claim verified where I read an abstract, table of contents or description that supports it. I did not read the full text of any book. Anything I could not confirm is marked "unconfirmed". Nothing below was filled in from memory.

Status key: VERIFIED = the work exists and the citation details given are confirmed. PARTLY VERIFIED = exists, but a named detail (edition, pages, DOI, year) or the attributed claim is not confirmed. NOT VERIFIED = could not be checked.

Source labels: Crossref = `https://api.crossref.org/works/<DOI>` (a metadata record; it confirms bibliographic fields, not content).

---

## A. Analytical sociology and the educational-inequality lineage (the references the task asked for)

### A1. Hedström & Ylikoski (2010) — VERIFIED
Hedström, P. & Ylikoski, P. (2010). "Causal mechanisms in the social sciences." *Annual Review of Sociology* 36: 49–67. DOI 10.1146/annurev.soc.012809.102632.
- Verified at: https://api.crossref.org/works/10.1146/annurev.soc.012809.102632 (authors, year, volume, pages); https://www.annualreviews.org/doi/10.1146/annurev.soc.012809.102632 (abstract).
- Verified: existence and all bibliographic details. Claim: the abstract describes a review of mechanism-based explanation in philosophy of science and in the social sciences, and its last part covers analytical sociology, including the use of simulations of interacting agents to build mechanism-based explanations. (The Annual Reviews page text did not itself print the author names; they come from Crossref.)

### A2. Hedström (2005) — VERIFIED
Hedström, P. (2005). *Dissecting the Social: On the Principles of Analytical Sociology.* Cambridge: Cambridge University Press. DOI 10.1017/CBO9780511488801. ISBN 978-0-521-79229-5 (hardback; Crossref also lists 9780521796675 and the e-book 9780511488801).
- Verified at: https://api.crossref.org/works?query.bibliographic=Hedstrom+Dissecting+the+Social (DOI, ISBNs); https://lehmanns.ch/shop/sozialwissenschaften/2945320-9780521792295-dissecting-the-social (ISBN-13 and -10); https://www.iffs.se/publikationer/bocker/dissecting-the-social-on-the-principles-of-analytical-sociology/ (table of contents); https://www.cambridge.org/core/books/dissecting-the-social/social-mechanisms-and-explanatory-theory/F7F309BA9E647835420D487F41FC63B2 (chapter 2).
- Verified: existence, publisher, year, ISBN, and that chapter 2 ("Social mechanisms and explanatory theory", pp. 11–33) argues that a phenomenon is explained by identifying the mechanism that regularly produces it. The table of contents includes a chapter on quantitative research and agent-based simulation. Unconfirmed: total page count, and what the simulation chapter concludes (I did not read it).

### A3. Hedström & Swedberg (eds.) (1998) — PARTLY VERIFIED
Hedström, P. & Swedberg, R. (eds.) (1998). *Social Mechanisms: An Analytical Approach to Social Theory.* Cambridge: Cambridge University Press. ISBN 978-0-521-59687-9 (one edition).
- Verified at: https://www.bookwire.com/book/USA/Social-Mechanisms-9780521596879--47410626 (title, editors, publisher, year, ISBN).
- Verified: existence, editors, publisher, year, one ISBN. Unconfirmed: DOI, page count, the hardback ISBN, and any series name. Unconfirmed: the 1996 *Acta Sociologica* article by the same pair, which a JASSS paper (Salgado et al. 2014) cites as "Hedström and Swedberg (1996)"; I did not check it.

### A4. Hedström & Bearman (eds.) (2009) — VERIFIED (with a date note)
Hedström, P. & Bearman, P. (eds.) (2009). *The Oxford Handbook of Analytical Sociology.* Oxford: Oxford University Press. Online edition DOI 10.1093/oxfordhb/9780199215362.001.0001; ISBN 9780199215362.
- Verified at: https://api.crossref.org/works?query.bibliographic=Hedstrom+Bearman+Oxford+Handbook+of+Analytical+Sociology (Crossref lists editors Bearman, Hedström; year 2011 for the online edition); https://www.gemass.fr/member/manzo-gianluca/?lang=en and a review in *European Sociological Review* (DOI 10.1093/esr/jcq057, by Mignot and Manzo) confirm the print book is 2009/2010.
- Date note: Crossref dates the DOI 2011 (online edition); print is cited as 2009 in the literature. Cite as 2009 and add the DOI. Unconfirmed: page count (a review title I saw gives 772 pp. in a URL slug only).

### A5. Manzo — the works that implement educational-choice or Boudon-type models computationally

Manzo's own publication list at https://www.gemass.fr/member/manzo-gianluca/?lang=en was my index (the page was truncated; there may be more). I then checked each item below at the source named.

**A5.1 Manzo (2013) — VERIFIED. The most relevant item.**
Manzo, G. (2013). "Educational choices and social interactions: a formal model and a computational test." In G. E. Birkelund (ed.), *Class and Stratification Analysis*, Comparative Social Research vol. 30, pp. 47–100. Bingley: Emerald. DOI 10.1108/S0195-6310(2013)0000030007.
- Verified at: https://www.emerald.com/insight/content/doi/10.1108/S0195-6310(2013)0000030007 (title, editor, series, volume, year, DOI, abstract); https://www.gemass.fr/member/manzo-gianluca/?lang=en (pages 47–100); https://ccl.northwestern.edu/papers/2013/Manzo2013a.pdf (text of the paper, as read by the fetch tool).
- What it does (paraphrase): Manzo adds peer pressure to a rational-choice model of educational choice in which agents weigh their ability and the perceived benefit of schooling, then runs agent-based simulations against French survey data. Ability and benefit perceptions alone do not reproduce the observed stratification of choices; network influence is needed, and it amplifies the segregation that private calculation produces.
- Relation to Breen-Goldthorpe and Boudon (from the fetched text; one reading by a summarising tool, so check against the paper): it builds on Breen and Goldthorpe (1997) without formalising it wholesale (it keeps group differences in the ability distribution and in perceived benefits, but changes the distributional form and adds an ability-by-benefit term). It draws on Boudon (1974) for an idea Boudon stated but did not model, namely that the cost of a choice depends on what one's friends choose, and it invokes Boudon (1979) on amplification when interpreting the simulations.

**A5.2 Manzo (2011), "Relative deprivation in silico" — VERIFIED. A computational treatment of a Boudon model, but not about education.**
Manzo, G. (2011). "Relative deprivation in silico: agent-based models and causality in analytical sociology." In P. Demeulenaere (ed.), *Analytical Sociology and Social Mechanisms*, ch. 13, pp. 266–308. Cambridge: Cambridge University Press. DOI 10.1017/CBO9780511921315.014.
- Verified at: https://api.crossref.org/works/10.1017/CBO9780511921315.014 (title, book, publisher, year, pages); https://www.gemass.fr/wp-content/uploads/2020/12/Relative-Deprivation-CUP-2011.pdf (content).
- What it does (paraphrase): it generalises Boudon's formal model of relative deprivation as an agent-based model in which agents choose between a costlier, better good and a cheaper, worse one, with dissatisfaction built from disappointment, envy and regret; it then compares comparison with the whole population against comparison within random and scale-free networks. The case is a generic opportunity-and-choice setting, not school choice, so it supports "Boudon-type models have been run as ABMs" but not "educational inequality".

**A5.3 Manzo (2009), *La spirale des inégalités* — PARTLY VERIFIED.**
Manzo, G. (2009). *La spirale des inégalités: choix scolaires en France et en Italie au XXe siècle.* Paris: Presses de l'Université Paris-Sorbonne (coll. L'intelligence du social).
- Verified at: https://www.gemass.fr/wp-content/uploads/2020/12/Educational-Inequalities-2009-book-Flyer.pdf (publisher flyer); the author's list gives the same title and series.
- What it does (paraphrase, from the flyer): an empirical study of school inequalities in France and Italy that explains them through cost-benefit reasoning, the market value of diplomas and social interaction, and that builds a multi-agent simulation of "virtual societies" to test the mechanisms. The flyer text I read does not mention Boudon. Unconfirmed: ISBN (a catalogue URL shows a truncated string only), page count (a URL slug suggests 336 pp., not read on a page), and the content of the simulation chapter.

**A5.4 Manzo, working paper on "educational traps" — PARTLY VERIFIED.**
Manzo, G. "Educational choices and educational traps: towards an integration between computational and statistical modelling in the sociology of social stratification." FMSH Working Paper 2013-48 (the page also shows a 2011 date; the date is ambiguous).
- Verified at: https://www.fmsh.fr/en/dissemination/28478 (abstract). The HAL record would not load (bot protection).
- What it does (paraphrase): an "interdependent educational choice model" combining individual cost-benefit evaluation with peer pressure, tested by agent-based simulation. It reproduces the main patterns of educational inequality in France and Italy and suggests that inequality accumulates through highly homophilous personal networks ("educational traps"). The page text does not mention Boudon. This looks like an earlier version of A5.1; I did not compare the texts.

**A5.5 Other Manzo items found on his list, not opened — listed for the record, NOT VERIFIED beyond the list**
- Manzo (2009), "Boudon's model of relative deprivation revisited," in M. Cherkaoui & P. Hamilton (eds.), *Raymond Boudon: A Life in Sociology*, vol. 3, ch. 46, pp. 91–121 (Oxford: Bardwell Press).
- Manzo (2007), "Le modèle du choix éducatif interdépendant" (venue not shown on the part of the list I read).
- Manzo (2012), "Reason-based explanations and analytical sociology: a rejoinder to Boudon," *European Journal of Social Sciences* 50(2): 35–65.
- Manzo (ed.) (2025), *Boudon Reexamined: Nuts and Bolts for Contemporary Sociological Science*, Sorbonne University Press.
Source for all four: https://www.gemass.fr/member/manzo-gianluca/?lang=en. I did not verify them elsewhere.

**A5.6 Manzo (ed.) (2014), *Analytical Sociology: Actions and Networks* — PARTLY VERIFIED.**
Manzo, G. (ed.) (2014). *Analytical Sociology: Actions and Networks.* Chichester: Wiley. Manzo's own chapter: "Data, generative models, and mechanisms: more on the principles of analytical sociology," pp. 4–52.
- Verified at: https://www.gemass.fr/member/manzo-gianluca/?lang=en (the author's list). Unconfirmed on a publisher or Crossref page: ISBN, DOI, page count, the other chapters. I did not check whether the volume contains an education chapter.

**A5.7 Manzo (2022), *Agent-based Models and Causal Inference* — VERIFIED (with a date discrepancy).**
Manzo, G. (2022 [published 23 Dec 2021 per one retailer]). *Agent-Based Models and Causal Inference.* Chichester: Wiley. ISBN 978-1-119-70447-8; 208 pp. (hardback).
- Verified at: https://www.schweitzer-online.de/en/buch/Manzo/Agent-Based-Models-Causal-Inference/9781119704478/B544471/ (title, publisher, ISBN, pages, description); https://www.gemass.fr/member/manzo-gianluca/?lang=en (lists 2022).
- Date discrepancy: the retailer shows 23 Dec 2021, the author lists 2022. Check the copyright page before citing.
- Claim (paraphrase of the retailer description): it examines when quantitative methods can support causal claims, contrasts agent-based models with experiments, instrumental variables and causal graphs, and argues that none has a clear advantage for establishing causation and that combining them is strongest. Not verified from the book itself.

### A6. Breen & Goldthorpe (1997) — VERIFIED
Breen, R. & Goldthorpe, J. H. (1997). "Explaining educational differentials: towards a formal rational action theory." *Rationality and Society* 9(3): 275–305. DOI 10.1177/104346397009003002.
- Verified at: https://econpapers.repec.org/RePEc:sae:ratsoc:v:9:y:1997:i:3:p:275-305 (authors, journal, volume, issue, pages, year, DOI, abstract). The subtitle is from the title of a search-result listing for the same article, not from the RePEc page, which shows the short title.
- Claim (paraphrase of the abstract): a formal rational-action model in which families weigh the costs, benefits and perceived chances of success of educational options, built to explain rising participation, stable class differences and the narrowing of gender differences, attributing class differences to resources and constraints rather than culture. It is a mathematical model, not a simulation; the executable versions are other people's work (see A5.1, B1-B3).

### A7. Maroulis and colleagues, education-policy complex-systems and ABM work

**A7.1 Maroulis et al. (2010) — VERIFIED (citation); claim PARTLY.**
Maroulis, S., Guimerà, R., Petry, H., Stringer, M. J., Gomez, L. M., Amaral, L. A. N. & Wilensky, U. (2010). "Complex systems view of educational policy research." *Science* 330: 38–39. DOI 10.1126/science.1195153.
- Verified at: https://amaral.northwestern.edu/publications/complex-systems-view-educational-policy-research/citation (full citation as given by the Amaral group; issue number not shown there, so omitted).
- Claim: a short paper arguing that schools and districts are complex adaptive systems. The abstract page I read does not mention agent-based modelling, so I cannot say it argues for ABM specifically. Page range: the two pages come from the Amaral citation.

**A7.2 Maroulis, Bakshy, Gomez & Wilensky (2014) — VERIFIED (citation); DOI unconfirmed.**
Maroulis, S., Bakshy, E., Gomez, L. & Wilensky, U. (2014). "Modeling the transition to public school choice." *Journal of Artificial Societies and Social Simulation* 17(2): 3.
- Verified at: https://www.jasss.org/17/2/3/3.pdf (title, authors, journal, volume, issue, article, year); model code record: https://catalog.comses.net/publications/443.
- What it does (paraphrase): an agent-based model of a district moving from assigned neighbourhood schools to choice among existing and new public schools, initialised with Chicago Public Schools data; it finds that the timing of new-school entry matters as much as their number and quality, and that households weighting achievement more can leave district-wide achievement lower.

**A7.3 Maroulis (2016) — VERIFIED.**
Maroulis, S. (2016). "Interpreting school choice treatment effects: results and implications from computational experiments." *JASSS* 19(1): 7. DOI 10.18564/jasss.3002.
- Verified at: https://www.jasss.org/19/1/7.html.
- What it does (paraphrase): uses an agent-based model of school choice to show that lottery-study treatment effects shrink as participation rises because capacity limits restrict access to the best schools, so effects are not comparable across districts without accounting for participation and capacity.

---

## B. Further directly relevant works found (agent-based or generative models of educational inequality; validation methods; critiques)

**B1. Salgado, Marchione & Gilbert (2014) — VERIFIED.** "Analysing differential school effectiveness through multilevel and agent-based modelling." *JASSS* 17(4): 3. DOI 10.18564/jasss.2534. https://www.jasss.org/17/4/3.html. Paraphrase: an ABM with homophily-based friendship sorting and teacher expectations, calibrated to a London school data set and compared with a multilevel model; the multilevel model predicts better, the ABM supplies a mechanism, and the authors call the two complementary. Directly relevant to the "why not just econometrics" objection, with an actual head-to-head.

**B2. Reardon, Kasman, Klasik & Baker (2016) — VERIFIED.** "Agent-based simulation models of the college sorting process." *JASSS* 19(1): 8. DOI 10.18564/jasss.2993. https://jasss.soc.surrey.ac.uk/19/1/8.html. Paraphrase: a stylised ABM of application, admission and enrolment testing five pathways through which family resources shape college sorting; most of the sorting is carried by the resources-achievement link.

**B3. Leoni (2021/2022) — VERIFIED (citation); abstract read via a fetch summary.** Leoni, S. "An agent-based model for tertiary educational choices in Italy." *Research in Higher Education* 63(5): 797–824 (online 2021). DOI 10.1007/s11162-021-09666-4 (Crossref https://api.crossref.org/works/10.1007/s11162-021-09666-4). Paraphrase: a NetLogo ABM of the decision to enrol in university after secondary school (expected returns, peer conformity, effort given ability), calibrated to Italian data, with three policy experiments; the fetched text names Manzo (2013) as its closest precedent. It does not mention Boudon.

**B4. Valdés (2022) — VERIFIED (citation).** Valdés, M. T. "Unequal expectations? Testing decisional mechanisms for secondary effects of social origin." *Social Science Research* 105: 102688. DOI 10.1016/j.ssresearch.2021.102688. https://www.sciencedirect.com/science/article/pii/S0049089X21001654. Not an ABM: a statistical test, with PISA 2018 data from Spain, of cultural-capital and rational-action mechanisms for secondary effects; about two-thirds of the origin gap stays unexplained. Useful as the non-simulation side of the Boudon / Breen-Goldthorpe literature.

**B5. Lucas (2001) — VERIFIED.** "Effectively maintained inequality: education transitions, track mobility, and social background effects." *American Journal of Sociology* 106(6): 1642–1690. DOI 10.1086/321300. https://api.crossref.org/works?query.bibliographic=Lucas+Effectively+Maintained+Inequality+American+Journal+of+Sociology+2001 . Citation only; I did not read it. It is the standard companion to Raftery & Hout (1993) and a reviewer in this field will expect both.

**B6. Keuschnigg, Lovsjö & Hedström (2018) — VERIFIED (citation).** "Analytical sociology and computational social science." *Journal of Computational Social Science* 1(1): 3–14. DOI 10.1007/s42001-017-0006-5 (Crossref dates it 2017 online; the volume is 2018 — confirm). Also: Arvidsson, Hedström, Jarvis & Keuschnigg (2024), "On the intersection of analytical sociology and computational social science," OSF preprint, DOI 10.31235/osf.io/4h5ys. Verified at https://api.crossref.org/works?query.bibliographic=Keuschnigg+Lovsjo+Hedstrom+Analytical+sociology+and+computational+social+science+2018 . Contents not read; I list it because its title says it positions analytical sociology relative to computational social science, which is the field the paper must be placed in.

**B7. Hedström & Manzo (2015) — VERIFIED.** "Recent trends in agent-based computational research: a brief introduction." *Sociological Methods & Research* 44(2): 179–185. DOI 10.1177/0049124115581211. Verified at https://www.gemass.fr/wp-content/uploads/2020/12/On-AMBs-with-P.-Hedstrom-SMR-2015.pdf (the paper itself). Paraphrase: introduces a special issue; calls agent-based modelling a likely crucial tool for the micro-macro link; cites Manzo (2013) as an example of combining a formal model with a computational test; cites Boudon (1979) "Generating models as a research strategy" to separate statistical from theoretical models. It does not claim ABM is the only tool.

**B8. Bruch & Atwell (2015) — VERIFIED.** "Agent-based models in empirical social research." *Sociological Methods & Research* 44(2): 186–221. DOI 10.1177/0049124113506405 (Crossref dates online release 2013; the issue is 2015). https://api.crossref.org/works?query.bibliographic=Bruch+Atwell+Agent-based+models+in+empirical+social+research+2015 . Citation only; I did not read it. It is the obvious sociological reference on empirical use and calibration of ABMs.

**B9. Fagiolo, Moneta & Windrum (2007) — VERIFIED; and Fagiolo, Guerini, Lamperti, Moneta & Roventini (2019) — VERIFIED.**
- Fagiolo, G., Moneta, A. & Windrum, P. (2007). "A critical guide to empirical validation of agent-based models in economics: methodologies, procedures, and open problems." *Computational Economics* 30(3): 195–226. DOI 10.1007/s10614-007-9104-4.
- Fagiolo, G., Guerini, M., Lamperti, F., Moneta, A. & Roventini, A. (2019). "Validation of agent-based models in economics and finance." In *Computer Simulation Validation* (Simulation Foundations, Methods and Applications), pp. 763–787. Springer. DOI 10.1007/978-3-319-70766-2_31. Publisher inferred from the DOI prefix, not shown on the record.
- Verified at Crossref (search records returned for the titles). Contents not read. These are the main critiques/guides on ABM empirical validation.

**B10. Thiele, Kurth & Grimm (2014) — VERIFIED (citation).** "Facilitating parameter estimation and sensitivity analysis of agent-based models: a cookbook using NetLogo and R." *JASSS* 17(3): 11. DOI 10.18564/jasss.2503. Crossref record lists volume 17 issue 3; the article number 11 is unconfirmed on the record I saw. It is the practical reference for approximate Bayesian computation (ABC) calibration of ABMs (I read only the title and record, so confirm that ABC is covered before citing it for that).

**B11. Beaumont, Zhang & Balding (2002) — VERIFIED.** "Approximate Bayesian computation in population genetics." *Genetics* 162(4): 2025–2035. DOI 10.1093/genetics/162.4.2025. The standard ABC reference if the paper names ABC calibration (the repo's `engine/mc.py` uses ABC tolerance matching per the v1 outline).

**B12. Andrianakis et al. (2015) — VERIFIED.** Andrianakis, I., Vernon, I. R., McCreesh, N., McKinley, T. J., Oakley, J. E., Nsubuga, R. N., Goldstein, M. & White, R. G. (2015). "Bayesian history matching of complex infectious disease models using emulation: a tutorial and a case study on HIV in Uganda." *PLoS Computational Biology* 11(1): e1003968. DOI 10.1371/journal.pcbi.1003968. A tutorial application of history matching to a stochastic individual-based epidemic model; the closest worked example to what v1 means by "history matching" for an ABM.

**B13. Macy & Willer (2002) — VERIFIED.** "From factors to actors: computational sociology and agent-based modeling." *Annual Review of Sociology* 28: 143–166. DOI 10.1146/annurev.soc.28.110601.141117. Citation only.

**Not found.** I searched for an agent-based or generative model of credential inflation specifically (Collins/Thurow/Spence-type) and found no peer-reviewed paper I could confirm; one 2026 working paper by Caravaggio, Catola and Leoni turned up in a search listing but I did not open it, so it is unconfirmed. I did not find an ABM-of-education paper that tests its model on a pre-registered out-of-sample forecast.

---

## C. References in the existing outline's section 6

| Reference | Status | What is confirmed / missing | Verified at |
|---|---|---|---|
| Boudon (1974), *Education, Opportunity, and Social Inequality* | VERIFIED (bibliography); claim PARTLY | New York: Wiley, 1974, xxvii + 220 pp., ISBN 0-471-09105-7 (the outline's 978-0471091059 is the same number in ISBN-13 form; I checked the arithmetic). Claim in outline ("Boudon effect": expansion need not equalise social opportunity because credential value is positional; primary vs secondary effects) not checked against the book; Manzo (2013, A5.1) is the nearest I read and treats the friend-dependent cost idea as Boudon's but unmodelled. | https://discovery.nypl.org/research/research-catalog/bib/b10140071 |
| Epstein (1999), *Complexity* 4(5): 41–60 | VERIFIED | Title "Agent-based computational models and generative social science"; the outline's DOI returns this record. | https://api.crossref.org/works/10.1002/(SICI)1099-0526(199905/06)4:5%3C41::AID-CPLX9%3E3.0.CO;2-F |
| Epstein (2006), *Generative Social Science*, Princeton UP | PARTLY VERIFIED | The outline's DOI 10.1515/9781400842872 resolves to the Princeton e-book dated 2012 by Crossref; the 2006 print date is the standard citation but I did not confirm it on a page. | https://api.crossref.org/works/10.1515/9781400842872 |
| Epstein (2008), "Why model?", *JASSS* 11(4): 12 | VERIFIED | Claim confirmed: explanation is distinct from prediction; he lists sixteen reasons to model other than prediction. No DOI shown on the article page (do not invent one). | https://www.jasss.org/11/4/12.html |
| Godley & Lavoie (2007), *Monetary Economics* | VERIFIED | Basingstoke/London: Palgrave Macmillan, 2007; DOI 10.1057/9780230626546; ISBN 9781349352746 (print), 9780230626546 (electronic). The subtitle is not shown on the record I read; the outline's subtitle is unconfirmed. | https://api.crossref.org/works/10.1057/9780230626546 |
| Axtell, Axelrod, Epstein & Cohen (1996), *CMOT* 1(2): 123–141 | VERIFIED | | https://api.crossref.org/works/10.1007/BF01299065 |
| Grimm et al. (2005), *Science* 310(5750): 987–991 | VERIFIED | All ten authors as in the outline. | https://api.crossref.org/works/10.1126/science.1116681 |
| Craig, Goldstein, Rougier & Seheult (2001), *JASA* 96(454): 717–729 | VERIFIED | | https://api.crossref.org/works/10.1198/016214501753168370 |
| Tilly (1998), *Durable Inequality*, UC Press | PARTLY VERIFIED | Exists; the record I found is the 2019 UC Press reissue (DOI 10.1525/9780520924222, ISBN 9780520924222). The 1998 first-edition date and place were not confirmed. | https://api.crossref.org/works?query.bibliographic=Tilly+Durable+Inequality |
| Tilly (2005), *Identities, Boundaries, and Social Ties*, Paradigm | PARTLY VERIFIED | Exists; the record I found is the Routledge 2015 reissue (DOI 10.4324/9781315634050). The 2005 Paradigm edition was not confirmed. | https://api.crossref.org/works?query.bibliographic=Tilly+Identities+Boundaries+and+Social+Ties |
| Dore (1976), *The Diploma Disease*, Allen & Unwin | VERIFIED | London: Allen and Unwin, 1976, xiii + 214 pp., ISBN 0043700764 (catalogue record; author field blank on the page but the work is the one reviewed under Dore's name in Crossref-listed reviews). | https://folio.caval.edu.au/Record/c000115827/Description |
| Collins (1979), *The Credential Society*, Academic Press; 2019 Columbia reissue | VERIFIED | The 2019 Columbia University Press DOI 10.7312/coll19234 returns the title and author. The 1979 Academic Press edition is confirmed by the metadata of three contemporary reviews (e.g. DOI 10.1093/sf/59.3.861), not by a catalogue record. | https://api.crossref.org/works/10.7312/coll19234 |
| Thurow (1975), *Generating Inequality*, Basic Books | PARTLY VERIFIED | The DOI in the outline (10.1007/978-1-349-15723-5) is a Palgrave Macmillan UK edition. The Basic Books New York 1975 original was not confirmed. | https://api.crossref.org/works/10.1007/978-1-349-15723-5 |
| Hirsch (1976), *Social Limits to Growth*, Harvard UP | VERIFIED | DOI 10.4159/harvard.9780674497900 matches the Crossref record (title, author, year, Harvard UP). ISBN: Crossref lists 9780674497894 and Open Library lists 9780674497900 for the same title (the second is the string used in the DOI); 218 pp. per Open Library. | https://api.crossref.org/works?query.bibliographic=Hirsch+Social+Limits+to+Growth+Harvard ; https://openlibrary.org/isbn/9780674497900 |
| Raftery & Hout (1993), *Sociology of Education* 66(1) | VERIFIED; end page unconfirmed | Title and authors confirmed; Crossref gave start page 41 only. | https://api.crossref.org/works/10.2307/2112784 |
| Todd & Wolpin (2006), *AER* 96(5): 1384–1417 | VERIFIED | | https://api.crossref.org/works/10.1257/aer.96.5.1384 |
| Basu & Van (1998), *AER* 88(3): 412–427 | VERIFIED | Authors given as Kaushik Basu and Pham Hoang Van. DOI not confirmed. | https://ideas.repec.org/a/aea/aecrev/v88y1998i3p412-27.html |
| Nordtveit (2010), *CER* 54(2): 223–242 | VERIFIED | | https://api.crossref.org/works/10.1086/651261 |
| Nordtveit (2016), *Schools as Protection?*, Springer | VERIFIED | Cham: Springer, 2016; ISBN 9783319256504 (print), 9783319256511 (electronic). The subtitle "Reinventing Education in Contexts of Adversity" is not on the record I read; unconfirmed. | https://api.crossref.org/works/10.1007/978-3-319-25651-1 |
| Altinok, Angrist & Patrinos (2018), World Bank | PARTLY VERIFIED | Title, authors, publisher, year confirmed. "Policy Research Working Paper 8314" is not stated on the record (it is inferred from the DOI suffix); treat the number as unconfirmed. | https://api.crossref.org/works/10.1596/1813-9450-8314 |
| Menefee & Nordtveit (2026), *Massification and Its Mechanisms* | NOT VERIFIED | Internal working paper; the path `related/massification_project/paper/...` is not in this checkout (no `related/` directory). Cannot be checked externally. |  |

Also: Boudon (1979), "Generating models as a research strategy" — PARTLY VERIFIED. I know it only through Hedström & Manzo (2015) (B7), which cites it to separate statistical from theoretical models. Publication details are unconfirmed; do not cite until checked. It matters for the novelty argument: Boudon himself used a "generating models" vocabulary a generation before Epstein.

---

## D. Notes for the author

1. The outline's DOIs for Epstein 1999, Axtell et al., Grimm, Craig, Raftery & Hout, Todd & Wolpin, Nordtveit 2010/2016, Collins 2019, Thurow and Hirsch all resolved to the right work.
2. Nothing in the outline's section 6 is wrong in a way that needs a retraction. The weaknesses are edition dates (Tilly, Thurow, Collins, Epstein 2006) and missing page ends.
3. The outline's section 6 contains none of the analytical-sociology literature. A reviewer who knows it will look for A1, A2, A4, A5.1, A6 and B6/B7 first.
4. Some fetches returned a summary produced by a tool rather than the page itself. I used that only for bibliographic fields and abstracts, and flagged the claims that rest on it (A5.1 especially).
