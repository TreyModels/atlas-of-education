# Centerpiece verdicts — Paper F (levels-vs-changes/transportability) and Paper M (sequencing)

Worker `novelty-review`, 24 November 2026. Written for Dr. Menefee's priority change: establish whether the two
novelty candidates have prior work, give the closest paper, a verdict (NEW / INCREMENTAL / KNOWN), a referee-attack
memo, and the implications/future-research content a domain referee would expect.

All DOIs below were Crossref-verified in-session (status V = resolves with matching metadata; W = working-paper
version; U = no DOI, cite by hand).

---

## PAPER F CENTERPIECE — the schooling-fertility correlation is large in levels and vanishes in within-country changes; quantified across ~13,800 random partitions

### Independent prior-work map (closest first)

| # | Work | Status | Relation to the claim |
|---|---|---|---|
| 1 | **Liu, A. & Raftery, A. E. (2020). How do education and family planning accelerate fertility decline?** *Population and Development Review* 46(3). | **V 10.1111/padr.12347** | **Closest prior.** Country-level education-fertility modelling with explicit between-country structure (UN regions); the closest existing treatment of the level relation at country level. Does not do the within-change decomposition. |
| 2 | Kravdal, Ø. (2002). Education and fertility in sub-Saharan Africa: individual and community effects. *Demography* 39(2). | V 10.2307/3088337 | Separates individual from community effects — the *conceptual* ancestor of a within/between split, though not a panel decomposition. |
| 3 | Cleland, J. & Rodríguez, G. (1988). The effect of parental education on marital fertility in developing countries. *Population Studies* 42(3). | V 10.1080/0032472031000143566 | Individual-level gradient benchmark; the literature whose results the level correlation seems to reflect. |
| 4 | Herzer, D., Strulik, H. & Vollmer, S. (2012). The long-run determinants of fertility: one century of demographic change 1900–1999. *Journal of Economic Growth* 17. | V 10.1007/s10887-012-9085-6 | Long-run cross-country panel of fertility determinants; the closest long-panel precedent. |
| 5 | Murtin, F. (2013). Long-term determinants of the demographic transition, 1870–2000. *Review of Economics and Statistics* 95(2). | V 10.1162/rest_a_00302 | Long-run cross-country determinants; another precedent for the level relation. |
| 6 | Durlauf, Johnson & Temple (2005). Growth econometrics. *Handbook of Economic Growth*. | V 10.1016/s1574-0684(05)01008-7 | The levels-vs-growth regression distinction; gives the method its warrant. |
| 7 | Eberhardt & Teal (2011). Econometrics for grumblers. *JES* 25(1). | V 10.1111/j.1467-6419.2010.00624.x | Cross-country level regressions vs within-country change; the fragility argument. |
| 8 | Nickell, S. (1981). Biases in dynamic models with fixed effects. *Econometrica* 49(6). | V 10.2307/1911408 | Within-estimator bias; a referee will ask whether the change specification is biased. |
| 9 | Angrist, J. & Pischke, J.-S. (2009). *Mostly Harmless Econometrics*. | V (book DOI in Paper F's refs) | The textbook "FE removes between variation" statement; the method is standard. |
| 10 | Robinson (1950). Ecological correlations and the behavior of individuals. *ASR* 15(3). | V 10.2307/2087176 | The aggregation critique the paper is really invoking. |
| 11 | Patel, Burford & Ioannidis (2015). Assessment of vibration of effects due to model specification... *J Clin Epidemiol* 68(9). | V 10.1016/j.jclinepi.2015.05.029 | The multiverse/vibration-of-effects precedent for the random-partition quantification. |
| 12 | Steegen et al. (2016) multiverse; Simonsohn et al. (2020) specification curve. | V (in their refs) | The multiverse method. |

### Verdict

**INCREMENTAL — a new assembly, not a new method and not a new fact.**
- The levels-vs-changes move is **KNOWN** as econometrics (Nickell 1981; Angrist-Pischke; Durlauf et al.;
  Eberhardt-Teal). The aggregation critique is **KNOWN** (Robinson 1950).
- The specific schooling-fertility *level correlation* is **KNOWN and modelled** at country level (Liu & Raftery
  2020; Herzer et al. 2012; Murtin 2013), and the *individual* gradient is **KNOWN** (Cleland-Rodríguez 1988;
  Kravdal 2002).
- What I could not find is the **systematic demonstration that the country-level schooling-fertility correlation
  vanishes under the within-change specification, quantified across thousands of random partitions**. That
  assembly appears new. It is not a new discovery; it is a rigorous audit that makes a known suspicion measurable.
- A referee will say "this is the standard within/between critique applied to fertility" — and be right about the
  method. The paper's defence is the systematic quantification plus the placebo plus the transportability map, not
  the direction of the result.

### Referee-attack memo (F centerpiece)

1. **"This is just the within-between critique, already standard."** Answerable: concede the method, and show the
   audit is the contribution (13,800 partitions, placebo, both layers reported). Cite Nickell, Durlauf et al.,
   Eberhardt-Teal, and Liu-Raftery 2020 as the closest empirical precedent.
2. **"Your change specification is biased / your measure of schooling is wrong."** Nickell bias in dynamic panels,
   attenuation from measurement error in schooling, and the timing of the change window are all objectable.
   Answerable only with a robustness panel: alternative change windows, measurement-error correction, dynamic-panel
   estimator, and the level-relation benchmark re-estimated on the same sample.
3. **"The country-level null does not overturn the individual-level gradient."** The ecological-fallacy objection
   (Robinson 1950; Cleland-Rodríguez 1988; Kravdal 2002). Answerable only if the paper reports the DHS individual
   gradient and the country-level gradient side by side and scopes the claim to the country level.

### What a domain referee would need in Implications / Future research

- **Implications:** state plainly that the result is about what national aggregates can support — not about
  whether educating girls lowers fertility at the household level; and that it changes what a cross-country
  regression can claim, not what a schooling policy does.
- **Future research (what would turn this into a genuine new correlation or causal claim):** (i) individual-level
  DHS panel analysis with country fixed effects (schooling reform exposure) to identify the micro effect;
  (ii) subnational within-country education-fertility panel (DHS regions) to test whether the gradient survives
  within countries at a finer aggregation; (iii) natural experiments in schooling supply (school construction,
  compulsory-schooling laws, Osili-Long 2008 style) to identify the causal effect on fertility; (iv) pre-registered
  multiverse with a documented universe of specifications (the 13,800 partitions should be described as a
  sensitivity universe, not a hypothesis test).

---

## PAPER M CENTERPIECE — schooling expansion precedes agricultural labour release (61/64 countries, median 26 years; labour demand leads 7%)

### Independent prior-work map (closest first)

| # | Work | Status | Relation to the claim |
|---|---|---|---|
| 1 | **Porzio, T., Rossi, F. & Santangelo, G. (2021). The human side of structural transformation.** NBER WP 29390 (later title circulated as "Does schooling cause structural transformation?"). | **V/W 10.3386/w29390** | **Closest prior on the schooling→structural-change direction.** Systematically links schooling expansion to structural transformation; the paper must engage it and explain what the 61/64 event ordering adds. |
| 2 | Boli, J., Ramirez, F. O. & Meyer, J. W. (1985). Explaining the origins and expansion of mass education. *Comparative Education Review* 29(2). | V 10.1086/446504 | The world-polity claim that mass schooling is not driven by industrial demand — the sequencing claim in institutionalist form. |
| 3 | Soysal, Y. N. & Strang, D. (1989). Construction of the first mass education systems in nineteenth-century Europe. *Sociology of Education* 62(4). | V 10.2307/2112831 | State-building drives early mass schooling; includes the European cases. |
| 4 | Benavot, A. & Riddle, P. (1988). The expansion of primary education, 1870–1940. *Sociology of Education* 61(3). | V 10.2307/2112627 | Cross-national enrolment expansion facts. |
| 5 | Meyer, J. W., Ramirez, F. O. & Soysal, Y. N. (1992). World expansion of mass education, 1870–1980. *Sociology of Education* 65(2). | V 10.2307/2112679 | Diffusion/supply account. |
| 6 | Schofer, E. & Meyer, J. W. (2005). The worldwide expansion of higher education. *ASR* 70(6). | V 10.1177/000312240507000602 | Later expansion, supply-led. |
| 7 | Sandberg, L. G. (1979). The case of the impoverished sophisticate. *Journal of Economic History* 39(1). | V 10.1017/s0022050700096418 | Sweden: mass literacy before industrialisation — the canonical case. |
| 8 | Mitch, D. (1992). *The Rise of Popular Literacy in Victorian England*. | V 10.9783/9781512807189 | England: literacy before/around the factory system. |
| 9 | Goldin, C. & Katz, L. F. (2008). *The Race between Education and Technology*. | V (book) 10.2307/jctvf9x5x | The demand-led contrast case (US). |
| 10 | Squicciarini & Voigtländer (2015). *QJE* 130(4). | V 10.1093/qje/qjv025 | Upper-tail knowledge before industrialisation. |
| 11 | de Pleijt & van Zanden (2016). *EREH* 20(4). | V 10.1093/ereh/hew013 | Human capital before pre-industrial growth. |
| 12 | Graff, H. J. (2017/1979). *The Literacy Myth*. | V 10.4324/9781315132969 | The sceptical reading of literacy-before-development. |
| 13 | Boppart, Kiernan, Krusell & Malmberg (2023). NBER 31101. | V 10.3386/w31101 | The agricultural/structural-change mechanism the paper positions against. |

### Verdict

**INCREMENTAL-NEW as an assembly; KNOWN as a pattern.**
- The *direction* (schooling before industrial demand) is **KNOWN**: Sandberg 1979, Mitch 1992, the world-polity
  school (Boli et al. 1985; Soysal & Strang 1989; Meyer et al. 1992), and Porzio-Rossi-Santangelo (2021) for the
  schooling-to-structural-change link.
- A *systematic common event-ordering comparison across ~64 countries* (schooling take-off vs agricultural
  labour release, bootstrap intervals, forward/reverse shares) appears **new as an assembly**. I found no paper
  that codes both events on a common country panel and reports the lead distribution.
- The paper must therefore claim: "we systematise and quantify a known historical pattern", never "we discover
  that schools came before factories". The draft's "not claiming" section already says this — hold that line.

### Referee-attack memo (M centerpiece)

1. **"This is not new — Sandberg 1979 said it for Sweden and the world-polity school said it for everyone."**
   Answerable by reframing as systematic coding + bootstrap + horse race; cite Porzio-Rossi-Santangelo as the
   closest systematic treatment and explain the added value (common event metric, cross-country distribution).
2. **"The dates are unverified literature standard; your 61/64 is a coding artefact."** The paper's own
   date-perturbation (median gap 26, IQR 17–29; 93% forward >10 years; a uniform 15-year error needed to cut the
   forward share materially) is a good start but not enough. Answerable only with (i) a date-by-date source table
   and (ii) an alternative-threshold recoding of at least a subsample.
3. **"The horse race is under-identified."** Both supply and demand correlate with development, state capacity and
   the demographic transition. Answerable by calling it a decomposition, naming the exogenous variation needed
   (compulsory-schooling laws, church-state competition, colonial schooling policy), and not using the drivers-null
   to imply demand does not matter.

### What a domain referee would need in Implications / Future research

- **Implications:** sequencing is a statement about the order of two social processes, not about which one causes
  the other; the policy reading is that schooling supply can run ahead of labour demand (and did, historically),
  which bears on the "skills mismatch" debate but does not establish that supply *caused* massification.
- **Future research (what would turn this into a genuine new correlation or causal claim):** (i) build the
  date-by-date source table from primary series (Benavot-Riddle; Lindert; Flora; national histories) and release
  it; (ii) recode with alternative thresholds and report sensitivity of the 61/64; (iii) use compulsory-schooling
  or church-state reforms as instruments for the schooling take-off (Angrist-Pischke style), and ask whether
  agricultural labour release follows; (iv) extend Porzio-Rossi-Santangelo's schooling→structural-change design
  with the event-ordering data; (v) province/district-level data for Prussia/Britain/France to test the sequence
  within countries.

---

## Files and status

- This file answers the lead's priority change; the full claim-by-claim tables remain in `claims-map.md`.
- Paper M's DOI/record integrity gaps (wrong DOIs, review-article DOIs used for books, internal inconsistency
  between claims-prior-art.md and refs.md) were sent to panel-matrix and are listed in `discrepancy.md`.
- Paper F's 15 missing works and 7 wrong-paper flags remain OPEN in `discrepancy.md`; the full draft is still a
  skeleton, so the next diff will be against the completed draft.
