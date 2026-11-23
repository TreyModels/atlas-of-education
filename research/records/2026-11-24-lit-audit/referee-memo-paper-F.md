# Referee-attack memo — Paper F (fertility omnibus)

Independent auditor: `novelty-review`, 24 November 2026. Drafted from the claims as scoped by the lead and from
Crossref-verified prior work (see `claims-map.md`). Three strongest objections a demography/development referee
would make, and whether the current evidence can answer each.

## Objection 1 — The ecological fallacy (the kill shot)
*"You show that the country-level schooling-fertility association disappears within countries, then talk as if
schooling does not affect fertility. The individual-level literature has found an education gradient for fifty
years."* The referee has Robinson (1950, *ASR* 15(3), 10.2307/2087176), Cleland & Rodríguez (1988, *Population
Studies* 42(3), 10.1080/0032472031000143566), Kravdal (2002, *Demography* 39(2), 10.2307/3088337) and Martin &
Juárez (1995, 10.2307/2133523) to hand.

**Can the current evidence answer it?** Only if the DHS/individual section does the work explicitly: report the
individual gradient and the country-level gradient side by side on the same data, and state that the paper's claim
is about the **country-level relation** (what a national policy can infer), not about individual schooling. If the
paper only has the country panel and a paragraph, the objection lands and the paper should be reframed as a
macro-level decomposition, not a test of education's effect. This is the single highest-risk item.

## Objection 2 — The levels-vs-changes decomposition is standard, and Caldwell is the canonical counter-claim
*"A between-versus-within decomposition of a trending cross-country relation is textbook growth econometrics
(Durlauf, Johnson & Temple 2005, 10.1016/s1574-0684(05)01008-7; Eberhardt & Teal 2011,
10.1111/j.1467-6419.2010.00624.x). And the strongest account of mass education as a fertility determinant is
Caldwell (1980, 10.2307/1972729), which you do not engage."*

**Can the current evidence answer it?** Yes, by reframing: the contribution is not "a new decomposition" but the
**systematic decomposition across the whole 380-link matrix plus a future-schooling placebo plus a
random-grouping transportability yardstick** — a quantified audit, not a discovery. The paper must cite Caldwell
1980 as the opposing account and say what in the data adjudicates between it and the null. If it claims "we are
not aware of within-versus-between tests for education and fertility", that claim fails: Kravdal (2002) already
separates individual from community effects and Kravdal (2012, 10.4054/demres.2012.27.22) extends it.

## Objection 3 — Thresholds and transportability are asserted, not identified
*"You claim a tipping point and non-transportability, but the threshold is not estimated and the random grouping
null tests only whether an association travels, not whether a causal effect exists."* Referee ammunition:
Granovetter (1978, 10.1086/226707) for thresholds, Scheffer et al. (2009, 10.1038/nature08227) for critical
transitions, Pearl & Bareinboim (2011, 10.1109/icdmw.2011.169) and Brock & Durlauf (2001, 10.1596/17447) for
transportability/heterogeneity.

**Can the current evidence answer it?** Partly. The transportability part is answerable if the paper (a) states
plainly that a repartition holds the pooled association fixed and therefore tests heterogeneity, not causation,
and (b) pre-registers the grouping families. The threshold part is answerable only if the ~6-year and ~9-year
hinges are estimated with a stated criterion; otherwise the paper must downgrade "tipping point" to "non-linearity
consistent with a threshold" and say so in the abstract.

## Additional referee-visible defect: citation integrity
A demography referee will check the classics. In the current `lit/refs.json`, three entries resolve to the wrong
paper for their key: `notestein1945` resolves to "Population Problems of Palestine" rather than "Population — the
long view" (which has no DOI — cite by hand and mark unverified); `davis1963` resolves to Davis & Blake (1956)
"Social Structure and Fertility" rather than Davis (1963) "The Theory of Change and Response"
(10.2307/2732014); `becker1960` carries the Becker-Murphy-Tamura (1990) title. Also `trow1974` has no year,
`schultz1961` resolves to a 1972 item, and `chen2010` is a 2026 paper. **Answerable:** yes, trivially — relabel or
mark unverified — but only if caught before submission.

## Verdict for this paper

The strongest defensible claim is the **quantified decomposition with placebos and a transportability map**,
framed as an audit of a known relation, with the DHS section reconciling the macro null with the micro gradient.
The weakest are the **threshold/tipping** claim (needs an estimated threshold) and any framing that reads as
"education does not affect fertility" (the individual literature will defeat it). The paper is publishable as a
macro-demography audit if Objection 1 is answered in the text, not the appendix.
