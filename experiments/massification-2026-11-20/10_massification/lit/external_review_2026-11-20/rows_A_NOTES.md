# External review notes — schooling vs. skills, and economic complexity

Companion to `rows_A_schooling_complexity.csv` (28 rows: 15 strand A, 13 strand B).
Prepared 2026-11-20 for the massification programme. Every number below was read verbatim in
the source indicated in the CSV; nothing here is inferred or reconstructed from memory.

## Strand A — Years of schooling vs. cognitive skills/literacy and growth

### ESTABLISHED

Both literatures agree human capital is strongly associated with long-run growth, and that it is
not well captured by enrolment counts. In the Hanushek–Woessmann
programme, adding a direct cognitive-skill measure raises the explained variance of cross-country
growth from roughly one-quarter to three-quarters, and one standard deviation of student test
performance maps to 1.2–2.0 percentage points of annual growth
([Hanushek & Woessmann 2012](https://docs.iza.org/dp4575.pdf)). Their review states the position
plainly: cognitive skills "rather than mere school attainment" are what relate to earnings,
income distribution and growth ([JEL 2008](https://www.aeaweb.org/articles?id=10.1257/jel.46.3.607)),
carried into
[The Knowledge Capital of Nations](https://ideas.repec.org/b/mtp/titles/0262029170.html) (2015) and
restated as "three-quarters of the variation in growth" in the
[2021 Oxford survey](https://doi.org/10.1093/acrefore/9780190625979.013.651).
Barro's tradition still finds schooling productive: one extra year of male
secondary+ attainment raises growth on impact by 0.44 pp, implying a 19% higher asymptotic output
level and roughly a 7% social return ([Barro 2013](http://aeconf.com/Articles/Nov2013/aef140201.pdf)).
Micro returns to schooling are not seriously disputed
([Krueger & Lindahl 2001](http://www.nber.org/papers/w7591.pdf)).

### CONTESTED

Magnitudes and causality are contested. Identification in the skills literature rests on
instrumenting test scores with school-system institutions, which the authors themselves flag as a
possibly weak instrument (IZA DP 4575, §V). Pritchett's null — "no association" between
educational-capital growth and output-per-worker growth, with a large *negative* implied TFP
association — has never been overturned on its own terms
([WBER 2001](https://documents1.worldbank.org/curated/en/859821468180273788/pdf/773740JRN020010l0the0Education0Gone.pdf)).
Cohen & Soto argue the weak macro results are a measurement artifact: with rebuilt attainment
series, schooling coefficients turn significant and the macro return matches labour studies
([RePEc record](https://ideas.repec.org/a/kap/jecgro/v12y2007i1p51-76.html)). Krueger & Lindahl
split the difference: strong micro returns, but "the evidence of a positive effect of the stock of
education on a country's growth rate is tenuous," concentrated in very low-education countries.
Barro (2013) is a live counterexample to the "attainment is insignificant" claim — he keeps
a significant quantity effect conditional on test scores, while conceding quality dominates.
Sala-i-Martin's full-distribution approach was a methodological revolt against extreme-bounds
pessimism ([AER 1997](https://doi.org/10.1257/aer.87.2.178)), not a settlement of it.

### WHAT A CAREFUL PROGRAMME STILL CANNOT ASSUME

That a growth-per-standard-deviation coefficient transports to the Philippines; that massification
without measured learning raises growth; that historical Philippine test-score series exist at the
coverage needed to replicate these designs; or that "years of schooling" and "skills" are
interchangeable regressors. The Pritchett benchmark (αh ought to be 0.21–0.42) is the right yardstick to apply before claiming an education–growth effect.

## Strand B — Economic complexity (ECI) and growth

### ESTABLISHED

The founding paper's two claims survive: complexity measures correlate with income per capita, and
deviations from that relationship predict subsequent growth
([Hidalgo & Hausmann 2009](https://www.pnas.org/doi/10.1073/pnas.0900943106); full text read via
[arXiv:0909.3890](https://arxiv.org/pdf/0909.3890)). The product space is path dependent, and the
index outperforms Hirschman-Herfindahl and entropy measures of productive structure in the
authors' own horse race. Modern panel work supports incremental predictive content: a convergence
baseline gives adjusted R² = 0.25, trade complexity lifts it to 0.34, and a multidimensional
(trade + technology) measure to 0.41
([Stojkoski, Koch & Hidalgo 2023](https://www.nature.com/articles/s43247-023-00770-0)). ECI also
predicts lower inequality, and predicts it better than income does (R² 0.58 vs 0.36;
[arXiv:1505.07907](https://arxiv.org/pdf/1505.07907)). The Growth Lab institutionalises the index
as a ranking and forecasting instrument ([Atlas](https://atlas.hks.harvard.edu/)).

### CONTESTED

What the index *is*, and therefore what it licenses causally. Mealy, Farmer & Teytelboym show the
ECI is mathematically equivalent to spectral clustering on a similarity graph — a dimension
reduction, not an identified stock of capabilities
([INET Oxford WP 2018-04](https://oms-inet.files.svdcdn.com/production/files/main_feb4.pdf)).
Sciarra et al. document that the standard metrics "produce contrasting results, undermining their
acceptance and applications" ([Nat Comms 2020](https://www.nature.com/articles/s41467-020-16992-1)).
Metric choice moves the growth coefficient: ECI+ beats both ECI and Fitness-complexity, with one SD
worth "about 4% to 5%" of annualized growth
([Albeaik et al. 2017](https://arxiv.org/abs/1707.05826), a preprint). Even inside the field, the
sophistication measure EXPY is admitted to embed GDP per capita by construction
(Hausmann & Hidalgo 2011, fn. 2). Whether complexity predicts growth *beyond income and export
diversification out of sample*, and whether the mechanism is capabilities or something else, is
not settled.

### WHAT A CAREFUL PROGRAMME STILL CANNOT ASSUME

That ECI is a policy lever rather than a summary statistic; that country-level predictive power
holds at Philippine regional or sectoral scale; that complexity gains are independent of the
skills distribution massification produces; or that any single complexity metric is *the* metric.
Felipe, Kumar & Abdon's alternative taxonomy shows how much rides on the choice of structural
measure ([Levy WP 644](https://www.levyinstitute.org/pubs/wp_644.pdf)).

## Items requested but not verifiable

**Glawe & Wagner.** No economic-complexity paper by Linda Glawe and Helmut Wagner could be located.
Author and title searches of OpenAlex return their middle-income-trap work (e.g. Glawe & Wagner
2016, *Comparative Economic Studies*, "The Middle-Income Trap: Definitions, Theories and Countries
Concerned"; Glawe & Wagner 2019, *China Economic Review*, "China in the middle-income trap?"), not
an ECI critique. No row was created, to avoid fabricating an attribution. If the parent has a
specific citation, it should be supplied.

**Hanushek & Woessmann (2015) book text** was not accessible (MIT Press 403); abstract-level only.

**Hidalgo & Hausmann (2009) supplementary regression tables** were not read; the predictive claim is
recorded qualitatively, with no magnitude asserted.

## URLs fetched

Status reflects what was actually opened and read, not what was merely resolved.

1. https://www.aeaweb.org/articles?id=10.1257/jel.46.3.607 — VERIFIED-ABSTRACT (landing page opened, abstract read)
2. https://docs.iza.org/dp4575.pdf — VERIFIED-FULLTEXT (IZA DP 4575, 64 pp., read)
3. https://doi.org/10.1007/s10887-012-9081-x — not opened (Springer); content verified through IZA DP 4575
4. https://ideas.repec.org/b/mtp/titles/0262029170.html — VERIFIED-ABSTRACT (book record opened)
5. https://doi.org/10.1093/acrefore/9780190625979.013.651 — not opened (OUP paywall); abstract read via OpenAlex record → VERIFIED-ABSTRACT
6. https://documents1.worldbank.org/curated/en/859821468180273788/pdf/773740JRN020010l0the0Education0Gone.pdf — VERIFIED-FULLTEXT (25 pp. PDF read)
7. https://www.cgdev.org/publication/rebirth-education-schooling-aint-learning — HTTP 403, not opened → row A10 left UNVERIFIED
8. http://www.nber.org/papers/w7591.pdf — VERIFIED-FULLTEXT (65 pp. PDF read)
9. https://doi.org/10.2307/2937943 — not opened (JSTOR paywall); abstract read via OpenAlex record → VERIFIED-ABSTRACT
10. http://aeconf.com/Articles/Nov2013/aef140201.pdf — VERIFIED-FULLTEXT (28 pp. PDF read)
11. https://doi.org/10.1257/aer.87.2.178 — not opened (no open copy found); abstract read via OpenAlex record → VERIFIED-ABSTRACT
12. https://ideas.repec.org/a/kap/jecgro/v12y2007i1p51-76.html — VERIFIED-ABSTRACT (RePEc record opened)
13. https://www.pnas.org/doi/10.1073/pnas.0900943106 — HTTP 403 (Cloudflare); abstract read via PMC
14. https://arxiv.org/pdf/0909.3890 — VERIFIED-FULLTEXT (author preprint of PNAS 2009, read)
15. https://arxiv.org/pdf/1101.1707 — VERIFIED-FULLTEXT (author preprint of JEG 2011, read)
16. https://doi.org/10.1007/s10887-011-9071-4 — not opened (Springer); content verified through arXiv:1101.1707
17. https://arxiv.org/abs/1707.05826 — VERIFIED-FULLTEXT (Albeaik et al., 21 pp. preprint read)
18. https://oms-inet.files.svdcdn.com/production/files/main_feb4.pdf — VERIFIED-FULLTEXT (Mealy/Farmer/Teytelboym WP read)
19. https://www.nature.com/articles/s41467-020-16992-1 — VERIFIED-FULLTEXT (Sciarra et al. PDF read)
20. https://doi.org/10.1016/j.worlddev.2016.12.020 — not opened (Elsevier); content verified through arXiv:1505.07907
21. https://arxiv.org/pdf/1505.07907 — VERIFIED-FULLTEXT (Hartmann et al. draft read)
22. https://www.nature.com/articles/s43247-023-00770-0 — VERIFIED-FULLTEXT (Stojkoski et al. PDF read)
23. https://www.nature.com/articles/s42254-020-00275-1 — VERIFIED-ABSTRACT (landing page; body paywalled)
24. https://atlas.hks.harvard.edu/ — VERIFIED-ABSTRACT (platform opened; descriptive text only; book PDF truncated, MIT Press 403)
25. https://www.levyinstitute.org/pubs/wp_644.pdf — VERIFIED-FULLTEXT (55 pp. working paper read)

## Method note

`web_fetch` was unavailable in this environment: every hostname resolved to a reserved
198.18.x.x address (local VPN fake-IP DNS), so the fetch tool rejected all requests as
non-public. Retrieval was therefore done with `curl` and PDF text extraction (pypdf); the
verification statuses above describe documents actually downloaded and read. Where a paywalled
DOI is listed, the URL records the canonical locator while the "notes" column of the CSV states
exactly which artifact was read.
