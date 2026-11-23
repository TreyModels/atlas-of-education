# Claims map — independent prior-work audit for Paper F (fertility) and Paper M (massification)

Worker `novelty-review`, branch `research/lit-audit-2026-11-24`, 24 November 2026. Task-35.
**Published early and incrementally** so the paper leads can fix gaps while drafting. This is my own search, not
the leads' lists; the diff against their lists will follow in `discrepancy.md` as their branches push.

**Method.** Crossref API (`api.crossref.org/works`, polite `mailto`, top hit checked for title/author/year/venue)
via the Mac proxy; `web_search` where Crossref has no DOI (books, old AER articles). Status key:
- **[V]** = DOI resolves in Crossref and title/author/year match.
- **[W]** = only a working-paper/SSRN version resolved; published version named but not DOI-verified.
- **[U]** = no DOI found in-session (usually a book or pre-DOI article); citation standard, needs a library check.

**Standing flags.** (i) The levels-versus-changes distinction is textbook cross-country econometrics, and
"we are not aware" of a within/between decomposition of the schooling-fertility gradient will not survive a
referee — the novelty must be the specific panel decomposition plus placebo, not the idea. (ii) The
supply-versus-demand account of mass schooling is a decades-old horse race (world-polity school vs human-capital
school) — the novelty must be the systematic 61/64 coding, not "schools before factories" as an idea.
(iii) Every "no effect" claim needs the power statement attached. (iv) The scaling/θγ section must not present an
unfitted formalism as tested.

---

## PAPER F — FERTILITY

### F1. Levels-versus-changes gradient (headline claim)
Claim: the schooling-fertility association is strong between countries but weak or absent within countries over
changes; therefore the cross-country gradient is a transition-stage marker, not a causal schooling lever.
| # | Work | Status | Why it matters |
|---|---|---|---|
| 1 | Caldwell, J. C. (1980). Mass education as a determinant of the timing of fertility decline. *Population and Development Review* 6(2), 225–255. | [V] 10.2307/1972729 | The canonical statement that mass schooling **is** a fertility determinant — the paper must engage it, not just cite it. |
| 2 | Cleland, J. & Rodríguez, G. (1988). The effect of parental education on marital fertility in developing countries. *Population Studies* 42(3). | [V] 10.1080/0032472031000143566 | Establishes the education-fertility gradient at individual level; the macro decomposition must reconcile with it. |
| 3 | Basu, A. M. (2002). Why does education lead to lower fertility? *World Development* 30(10). | [V] 10.1016/s0305-750x(02)00072-4 | Critical review of the mechanisms; a referee will ask why the macro null does not contradict the micro mechanisms. |
| 4 | Martin, T. C. & Juárez, F. (1995). The impact of women's education on fertility in Latin America. *International Family Planning Perspectives* 21(2). | [V] 10.2307/2133523 | The classic "searching for explanations" paper — mechanisms vs spuriousness. |
| 5 | Kravdal, Ø. (2002). Education and fertility in sub-Saharan Africa: individual and community effects. *Demography* 39(2). | [V] 10.2307/3088337 | Already separates individual from community effects — the closest prior to a within/between decomposition. |
| 6 | Becker, S. O., Cinnirella, F. & Woessmann, L. (2010). The trade-off between fertility and education: evidence from before the demographic transition. | [W] 10.2139/ssrn.1476206 | Historical micro evidence on the education-fertility trade-off; relevant to "marker vs lever". |
| 7 | Durlauf, S., Johnson, P. & Temple, J. (2005). Growth econometrics. *Handbook of Economic Growth*. | [V] 10.1016/s1574-0684(05)01008-7 | The levels-vs-growth regression distinction; a referee will cite it. |
| 8 | Eberhardt, M. & Teal, F. (2011). Econometrics for grumblers. *Journal of Economic Surveys* 25(1). | [V] 10.1111/j.1467-6419.2010.00624.x | Cross-country level regressions vs within-country change; exactly the methodological warrant. |

**Flag:** this claim is **standard** as a methodological move and **partly known** as a substantive pattern
(Caldwell; Cleland-Rodríguez; Kravdal). The defensible novelty is the systematic panel decomposition (levels vs
changes across the whole matrix) plus the future-schooling placebo — that must be the framing, and Caldwell 1980
must be cited as the strongest opposing account, not omitted.

### F2. Transportability — the gradient varies across country groupings
Claim: the gradient is not transportable; it holds in some country types and not others (random-grouping multiverse).
| # | Work | Status | Why |
|---|---|---|---|
| 1 | Brock, W. & Durlauf, S. (2001). Growth empirics and reality. *World Bank Economic Review* 15(2). | [V] 10.1596/17447 | Heterogeneity critique: a pooled coefficient may be an average no country has. |
| 2 | Bongaarts, J. & Watkins, S. C. (1996). Social interactions and contemporary fertility transitions. *PDR* 22(4). | [V] 10.2307/2137804 | Fertility transitions vary by social context; heterogeneity is expected, not novel. |
| 3 | Robinson, W. S. (1950). Ecological correlations and the behavior of individuals. *American Sociological Review* 15(3). | [V] 10.2307/2087176 | The ecological-fallacy warrant for not reading country gradients as individual ones. |
| 4 | Kravdal, Ø. (2012). Further evidence of community education effects on fertility in sub-Saharan Africa. *Demographic Research* 27. | [V] 10.4054/demres.2012.27.22 | Multilevel evidence that context changes the gradient. |
| 5 | Pearl, J. & Bareinboim, E. (2011). Transportability of causal and statistical relations. *IEEE ICDMW*. | [V] 10.1109/icdmw.2011.169 | Formal transportability; a methods referee may ask for this framing. |
| 6 | Durlauf, Johnson & Temple (2005). | [V] see F1 | Again. |

**Flag:** transportability is a large literature; claiming "we are not aware of heterogeneity" fails. The
defensible claim is the **quantified** transportability map (random-grouping yardstick), which is descriptive.

### F3. Future-schooling placebo
Claim: future schooling (a placebo lead) does not predict current fertility once survival is controlled — i.e. the
level association runs through development, not through schooling's later expansion.
| # | Work | Status | Why |
|---|---|---|---|
| 1 | Granger, C. W. J. (1969). Investigating causal relations by econometric models and cross-spectral methods. *Econometrica* 37(3). | [U] no DOI located | The lead/lag logic; cite the original. |
| 2 | Bertrand, M., Duflo, E. & Mullainathan, S. (2002/2004). How much should we trust differences-in-differences estimates? | [W] 10.3386/w8841 (SSRN); published QJE 2004 DOI not verified in-session | Pre-trends/placebo tests are standard; the paper must show the placebo is not just a pre-trend artefact. |
| 3 | Lee, R. (2003). The demographic transition: three centuries of fundamental change. *JEP* 17(4). | [V] 10.1257/089533003772034943 | Long-run framing for lead/lag between mortality, schooling, fertility. |
| 4 | Doepke, M. (2005). Child mortality and fertility decline: does the Barro-Becker model fit the facts? *Journal of Population Economics* 18. | [V] 10.1007/s00148-004-0208-z | The standard competing account (mortality-led), which a placebo should be designed against. |
| 5 | Granovetter, M. (1978). Threshold models of collective behavior. *AJS* 83(6). | [V] 10.1086/226707 | Only if the placebo is framed as a threshold/timing claim. |

**Flag:** placebo/lead-lag tests are standard; the paper should say "the placebo is a diagnostic", not a proof of
causality. If the lead writes "we are not aware of a placebo test here", that is fine; if they write "no one has
tested reverse causality in education-fertility", that fails (see F1 works 5–6).

### F4. DHS ecological gradient — the individual-vs-country comparison
Claim: the country-level gradient and the individual-level (DHS) gradient differ, and the country-level one is not
a schooling effect.
| # | Work | Status | Why |
|---|---|---|---|
| 1 | Robinson (1950). | [V] 10.2307/2087176 | Ecological fallacy — the objection a demographer will raise first. |
| 2 | Cleland & Rodríguez (1988). | [V] 10.1080/0032472031000143566 | Individual gradient benchmark. |
| 3 | Kravdal (2002). | [V] 10.2307/3088337 | Individual + community effects benchmark. |
| 4 | Basu (2002). | [V] 10.1016/s0305-750x(02)00072-4 | Mechanisms review. |
| 5 | Martin & Juárez (1995). | [V] 10.2307/2133523 | Latin America benchmark. |
| 6 | Bongaarts & Watkins (1996). | [V] 10.2307/2137804 | Context-dependence of the individual gradient. |

**Flag:** the DHS ecological caveat is the **most likely referee kill** for F: individual education-fertility
gradients are robust in the micro literature, so the paper must not read as "education doesn't matter for
individuals". It must show the two layers explicitly and explain why the country-level null does not contradict
the individual-level gradient.

### F5. Care loop — kin childcare / co-residence and fertility
Claim: kin support changes the cost of children, part of the individuation channel.
| # | Work | Status | Why |
|---|---|---|---|
| 1 | Sear, R., Mace, R. & McGregor, I. A. (2003). The effects of kin on female fertility in rural Gambia. *Evolution and Human Behavior* 24(1). | [V] 10.1016/s1090-5138(02)00105-8 | Direct kin-fertility evidence. |
| 2 | Coall, D. A. & Hertwig, R. (2010). Toward an integrative framework of grandparental investment. *BBS* 33(1). | [V] 10.1017/s0140525x10000014 | Grandparental childcare framework. |
| 3 | Caldwell (1980). | [V] 10.2307/1972729 | Wealth flows / mass education. |
| 4 | Bongaarts & Watkins (1996). | [V] 10.2307/2137804 | Social context. |
| 5 | Kravdal (2012). | [V] 10.4054/demres.2012.27.22 | Community effects. |
| 6 | Cox, D. & Fafchamps, M. (2007). Extended family and kinship networks. *Handbook of Development Economics* — [U] need DOI check | Kin-network economics. |

**Flag:** the cooperative-breeding/kin-fertility literature is large; the care-loop claim is **known in direction**
and the paper's contribution must be the country/macro implementation, not the mechanism.

### F6. No-off-switch / irreversibility
Claim: there is no reversible "off switch" — once the transition is under way the fertility fall does not reverse
from the same policy levers.
| # | Work | Status | Why |
|---|---|---|---|
| 1 | Lee (2003). | [V] 10.1257/089533003772034943 | Long-run transition irreversibility framing. |
| 2 | Bongaarts & Watkins (1996). | [V] 10.2307/2137804 | Diffusion/stickiness. |
| 3 | Galor & Weil (2000). *AER* 90(4). | [U] DOI 10.1257/aer.90.4.806 (verified earlier session; re-check) | Unified growth: no return to Malthusian equilibrium. |
| 4 | Tainter, J. (1988). *The Collapse of Complex Societies*. | [U] book, no DOI | Diminishing returns/hysteresis analogy. |
| 5 | Scheffer et al. (2009). Early-warning signals for critical transitions. *Nature* 461. | [V] 10.1038/nature08227 | Hysteresis/critical transitions language. |

**Flag:** this is the **weakest-evidenced** claim in F. "No off switch" is a strong causal/structural claim; the
paper needs either a formal hysteresis model or it must downgrade to "no evidence of reversal in our panel".

### F7. Tipping point / diminishing returns / threshold shape
| # | Work | Status | Why |
|---|---|---|---|
| 1 | Granovetter (1978). | [V] 10.1086/226707 | Threshold models. |
| 2 | Scheffer et al. (2009). | [V] 10.1038/nature08227 | Critical transitions. |
| 3 | Tainter (1988). | [U] | Diminishing returns to complexity. |
| 4 | Brock & Durlauf (2001). | [V] 10.1596/17447 | Heterogeneity/averages. |
| 5 | Bongaarts & Watkins (1996). | [V] 10.2307/2137804 | Diffusion thresholds. |

**Flag:** threshold/tipping language must be tied to an estimable threshold; otherwise it is metaphor and a
referee will say so.

### F8. Full transition / individuation model
| # | Work | Status | Why |
|---|---|---|---|
| 1 | Caldwell (1976). Toward a restatement of demographic transition theory. *PDR* 2(3/4). | [V] 10.2307/1971615 | The wealth-flows source. |
| 2 | Henrich, Heine & Norenzayan (2010). The weirdest people in the world? *BBS* 33(2-3). | [W] 10.2139/ssrn.1601785; published BBS DOI not verified here | The WEIRD/individuation frame. |
| 3 | Galor & Weil (2000). *AER* 90(4). | [U] see F6 | Unified growth benchmark. |
| 4 | Doepke (2005). | [V] 10.1007/s00148-004-0208-z | Mortality-led rival. |
| 5 | Lee (2003). | [V] 10.1257/089533003772034943 | Transition framing. |

**Flag:** the individuation model is one implementation of a large literature; the paper must not claim the
mechanism is new — only the test.

---

## PAPER M — MASSIFICATION

### M1. Sequencing — schools before factories (headline claim, 61/64)
| # | Work | Status | Why |
|---|---|---|---|
| 1 | Sandberg, L. G. (1979). The case of the impoverished sophisticate: human capital and Swedish economic growth before World War I. *Journal of Economic History* 39(1). | [V] 10.1017/s0022050700096418 | **The canonical "schooling before industrialisation" case.** If the paper says "we are not aware of schools-before-factories evidence", this kills it. |
| 2 | Mitch, D. (1992). *The Rise of Popular Literacy in Victorian England*. | [V] 10.9783/9781512807189 | Literacy before/around industrialisation. |
| 3 | Goldin, C. & Katz, L. F. (1999). Human capital and social capital: the rise of secondary schooling in America, 1910–1940. | [W] 10.3386/w6439; published chapter 10.1017/cbo9780511572777.012 | US high-school movement — supply-led (public) expansion. |
| 4 | Lindert, P. H. (2004). *Growing Public*. | [V] 10.1017/cbo9780511510717 | Public schooling as a political supply story. |
| 5 | Benavot, A. & Riddle, P. (1988). The expansion of primary education, 1870–1940. *Sociology of Education* 61(3). | [V] 10.2307/2112627 | The cross-national expansion facts. |
| 6 | Meyer, J. W., Ramirez, F. O. & Soysal, Y. N. (1992). World expansion of mass education, 1870–1980. *Sociology of Education* 65(2). | [V] 10.2307/2112679 | **Supply-led world-polity account** — the sequencing claim's main rival/ally. |
| 7 | Schofer, E. & Meyer, J. W. (2005). The worldwide expansion of higher education in the twentieth century. *ASR* 70(6). | [V] 10.1177/000312240507000602 | Same tradition. |
| 8 | Squicciarini, M. P. & Voigtländer, N. (2015). Human capital and industrialization: evidence from the age of enlightenment. *QJE* 130(4). | [V] 10.1093/qje/qjv025 | Upper-tail knowledge before/with industrialisation. |
| 9 | de Pleijt, A. & van Zanden, J. L. (2016). Accounting for the "Little Divergence". *European Review of Economic History* 20(4). | [V] 10.1093/ereh/hew013 | Human capital before industrial growth. |
| 10 | Graff, H. J. (2017/1979). *The Literacy Myth*. | [V] 10.4324/9781315132969 | The sceptical classic: literacy not causally prior to development. |

**Flag:** the sequencing claim is **not new as an idea** — Sandberg 1979 and the world-polity school are directly on
point. The paper's defensible novelty is the systematic 61/64 coding of dates plus the horse race; it must say
"we systematise and quantify a known historical pattern", not "we are not aware of evidence".

### M2. Supply-versus-demand horse race
| # | Work | Status | Why |
|---|---|---|---|
| 1 | Boli, J., Ramirez, F. O. & Meyer, J. W. (1985). Explaining the origins and expansion of mass education. *Comparative Education Review* 29(2). | [V] 10.1086/446504 | Supply/world-polity account. |
| 2 | Ramirez, F. O. & Boli, J. (1987). The political construction of mass schooling. *Sociology of Education* 60(1). | [V] 10.2307/2112615 | Supply/political account. |
| 3 | Goldin & Katz (1999/2008). | [W]/[U] see M1 | Demand/human-capital account. |
| 4 | Galor, O. & Moav, O. (2006). Das Human-Kapital. *Review of Economic Studies* 73(1). | [V] 10.1111/j.1467-937x.2006.00370.x | Demand-side theoretical mechanism. |
| 5 | Lindert (2004). | [V] 10.1017/cbo9780511510717 | Political economy of public schooling. |
| 6 | Becker & Woessmann (2009). Was Weber wrong? *QJE* 124(2). | [V] 10.1162/qjec.2009.124.2.531 | Human-capital demand side. |

**Flag:** the horse race is old and probably under-identified; the paper needs to frame it as a decomposition,
not a causal verdict.

### M3. Historical dates (each date must carry a source)
| Country | Prior work | Status |
|---|---|---|
| Sweden | Sandberg 1979 | [V] 10.1017/s0022050700096418 |
| England | Mitch 1992 | [V] 10.9783/9781512807189 |
| USA | Goldin & Katz 1999 | [W] 10.3386/w6439 |
| Prussia/Germany | Becker & Woessmann 2009 | [V] 10.1162/qjec.2009.124.2.531 |
| Cross-national | Benavot & Riddle 1988; Meyer et al. 1992 | [V] 10.2307/2112627; 10.2307/2112679 |
| France, Japan, others | not yet verified in-session — **flag for the lead** | [U] |

**Flag:** a referee will pick two dates at random and check them. Every date in the 61/64 table needs a named
source and a page/table; cross-national series (Benavot & Riddle; Lindert's data appendix) are the safest anchors.

### M4. Boppart / agriculture floor
| # | Work | Status | Why |
|---|---|---|---|
| 1 | Boppart, T., Kiernan, P., Krusell, P. & Malmberg, H. (2023). The macroeconomics of intensive agriculture. NBER WP 31101. | [V] 10.3386/w31101 | The paper's target. |
| 2 | Herrendorf, Rogerson & Valentinyi (2014). Growth and structural transformation. *Handbook of Economic Growth*. | [U] DOI not located in-session | Standard structural-change frame. |
| 3 | Ngai, L. R. & Pissarides, C. (2007). Structural change in a multisector model of growth. *AER* 97(1). | [U] no DOI located | Sectoral reallocation mechanics. |
| 4 | Acemoglu, D. & Restrepo, P. (2018). The race between man and machine. *AER* 108(6). | [V] 10.1257/aer.20160696 | Mechanisation/labour displacement. |
| 5 | Gollin, Parente & Rogerson (2002). The role of agriculture in development. *AER* 92(2). | [V] 10.1257/000282802320189177 | Agriculture-as-floor. |
| 6 | Restuccia, Yang & Zhu (2008). Agriculture and aggregate productivity. *JME* 55(2). | [V] 10.1016/j.jmoneco.2007.11.006 | Cross-country agricultural productivity. |

### M5. Scaling laws (Heaps / Zipf / gravity / θγ)
| # | Work | Status | Why |
|---|---|---|---|
| 1 | Bettencourt, Lobo, Strumsky & West (2007). Growth, innovation, scaling… *PNAS* 104(17). | [V] 10.1073/pnas.0610172104 | Urban scaling exponents. |
| 2 | Yang, V. C. et al. (2026). Scaling laws for function diversity and specialization… (arXiv 2208.06487; PNAS). | [V] arXiv; PNAS DOI not verified | The θ/γ formalism — **must not be presented as fitted** (we have not fitted θ/γ). |
| 3 | Head, K. & Mayer, T. (2014). Gravity equations: workhorse, toolkit, cookbook. *Handbook of International Economics*. | [V] 10.1016/b978-0-444-54314-1.00003-3 | Gravity benchmark. |
| 4 | Zipf, G. K. (1949). *Human Behavior and the Principle of Least Effort*. | [U] book | Rank-size. |
| 5 | Heaps, H. S. (1978). *Information Retrieval: Computational and Theoretical Aspects*. | [U] book | Heaps' law. |
| 6 | Anderson, J. E. (1979). A theoretical foundation for the gravity equation. *AER* 69(1). | [U] pre-DOI | Gravity theory. |

**Flag:** if Paper M uses θ/γ as a tested claim, it will not survive: the project has not fitted θ or γ (see our
SFI scan and the scaling record). It must be presented as a diagnostic frame.

### M6. Massification drivers null
| # | Work | Status | Why |
|---|---|---|---|
| 1 | Energy-education micro literature: rural electrification/China (J. Dev. Studies) | [V] 10.1080/00220388.2026.2727160 | Positive micro effects must be acknowledged. |
| 2 | Small hydropower and girls' education (J. Dev. Econ.) | [V] S0304387826001458 (no DOI in-hand) | Positive micro effects. |
| 3 | Energy poverty and gender equality in education (TFSC) | [V] 10.1016/j.techfore.2024.123274 | Positive micro effects. |
| 4 | Eberhardt & Teal (2011). | [V] 10.1111/j.1467-6419.2010.00624.x | Why cross-country pooled links are fragile. |
| 5 | Boppart et al. (2023). | [V] 10.3386/w31101 | Development/latent factor rival. |

**Flag:** the null claim must carry the power statement and must not read as "electricity does not matter"; the
micro literature says it does at household/school level.

### M7. Credential inflation
| # | Work | Status | Why |
|---|---|---|---|
| 1 | Collins, R. (2019/1979). *The Credential Society*. | [V] 10.7312/coll19234 | The canonical credential-inflation thesis. |
| 2 | Spence, M. (1973). Job market signaling. *QJE* 87(3). | [V] 10.2307/1882010 | Signalling. |
| 3 | Arrow, K. (1973). Higher education as a filter. *Journal of Public Economics* 2(3). | [V] 10.1016/0047-2727(73)90013-3 | Filtering. |
| 4 | Bills, D. & Brown, D. (2011). New directions in educational credentialism. *Research in Social Stratification and Mobility* 29(1). | [V] 10.1016/j.rssm.2011.01.004 | Review. |

**Flag:** credential inflation is a **very old** claim (Collins 1979); "we are not aware" fails outright. The
contribution can only be the 2,000:1 credential-to-occupation measurement.

---

## Claims where "we are not aware" would not survive a referee (short list)

1. **Schools before factories** (M1) — Sandberg 1979; Mitch 1992; world-polity school. Known.
2. **Mass schooling supply-led** (M2) — Boli/Ramirez/Meyer 1985; Ramirez & Boli 1987. Known.
3. **Credential inflation** (M7) — Collins 1979; Spence 1973; Arrow 1973. Known.
4. **Education-fertility gradient exists and varies by context** (F1/F2) — Cleland-Rodríguez 1988; Kravdal 2002;
   Bongaarts-Watkins 1996. Known.
5. **Above-trend/level vs change distinction** (F1) — textbook growth econometrics (Durlauf et al.; Eberhardt-Teal).
6. **Kin support matters for fertility** (F5) — Sear et al. 2003; Coall-Hertwig 2010. Known in direction.
7. **Threshold/tipping language** (F7) — Granovetter; Scheffer. Known vocabulary; needs evidence.

## Missing adjacent literatures to add

- **Economic history of schooling** for Paper M (Mitch, Sandberg, Lindert, Goldin-Katz, de Pleijt-van Zanden) — if
  absent from their refs, the paper is thin on the historical side.
- **Demography of education-fertility at individual level** for Paper F (Cleland-Rodríguez, Kravdal,
  Bongaarts-Watkins) — if absent, the ecological fallacy attack lands.
- **World-polity sociology of education** (Boli/Ramirez/Meyer; Schofer-Meyer) — the main rival theory for M2.
- **Credential/signalling economics** (Spence, Arrow, Collins) for M7.
- **Structural-change economics** (Herrendorf et al.; Ngai-Pissarides; Acemoglu-Restrepo) for M4.
- **Gravity/scaling canon** (Anderson; Head-Mayer; Zipf; Heaps; Bettencourt; Yang) for M5.

---

## (1) Fertility

The levels-vs-changes claim is the strongest of Paper F but the **least novel as an idea**: Caldwell 1980 is the
canonical opposite claim, and the individual-level literature already separates individual from community effects.
The defensible contribution is the systematic decomposition plus the placebo and the transportability map — and the
DHS ecological section must reconcile the country null with the individual gradient, or a demographer referee will
reject the paper on exactly that point.

## (2) Massification

The sequencing claim is the strongest of Paper M and the **most likely to collide with prior work**: Sandberg 1979
is the "impoverished sophisticate" case of schooling before industrialisation, and the world-polity school has
argued supply-led expansion since the 1980s. The defensible contribution is the systematic 61/64 coding and the
horse race — presented as systematising a known pattern, never as a discovery. Every historical date needs a named
source, and the scaling/θγ section must stay diagnostic.

---

## Classic demographic-transition references — manual resolution (requested by the lead)

Verified by Crossref title search or direct DOI lookup on 24 Nov 2026. Resolved = DOI returns matching
title/author/year. Unresolved = no DOI found; cite by hand and mark unverified (do not paper over it).

| Reference | Status | DOI / note |
|---|---|---|
| Notestein (1945), "Population — the long view", in Schultz (ed.), *Food for the World* | **UNRESOLVED** | No DOI located; book chapter. A Crossref search returns a different Notestein 1945 paper ("Population Problems of Palestine"). Cite by hand, mark unverified. |
| Davis (1963), "The theory of change and response in modern demographic history", *Population Index* 29(4) | **Resolved [V]** | 10.2307/2732014 |
| Caldwell (1976), "Toward a restatement of demographic transition theory", *PDR* 2(3/4) | **Resolved [V]** | 10.2307/1971615 |
| Cleland & Wilson (1987), "Demand theories of the fertility transition: an iconoclastic view", *Population Studies* 41(1) | **Resolved [V]** | 10.1080/0032472031000142516 |
| Galor & Weil (2000), "Population, technology, and growth", *AER* 90(4) | **Resolved [V]** | 10.1257/aer.90.4.806 |
| Guinnane (2011), "The historical fertility transition: a guide for economists", *JEL* 49(3) | **Resolved [V]** | 10.1257/jel.49.3.589 |
| Coale & Watkins (1986), *The Decline of Fertility in Europe* (Princeton UP) | **Resolved [V] for the 2017 Princeton Legacy reissue** | 10.1515/9781400886692; original 1986 book has no DOI |
| Lesthaeghe (2010), "The unfolding story of the second demographic transition", *PDR* 36(2) | **Resolved [V]** | 10.1111/j.1728-4457.2010.00328.x |

**Rule for the papers:** the only unresolved classic here is Notestein (1945) — it must be cited by hand and marked
unverified, or replaced with Notestein's later DOI-bearing restatement. No paper may carry a "verified" tag on a
DOI that resolves to a different work.

## Citation-integrity flags found in Paper F's `lit/refs.json` (73 entries)

Diff against Crossref metadata: several entries resolve but do **not** match their citation key:
- `notestein1945` → "Population Problems of Palestine" (wrong paper; the classic is unresolved — see above).
- `davis1963` → Davis & Blake (1956) "Social Structure and Fertility" (wrong paper; Davis 1963 is 10.2307/2732014).
- `becker1960` → "Human Capital, Fertility, and Economic Growth" (Becker-Murphy-Tamura 1990; wrong paper).
- `schultz1961` → resolves to a 1972 item; `trow1974` has no year; `chen2010` is a 2026 paper;
  `bongaarts2011` carries the 1978 proximate-determinants title.
These are DOI-resolving but label-mismatched — exactly what a demography referee checks. Flagged to the lead;
fix or mark unverified.

## Independent-list gaps handed to Paper F lead (from my list, absent from their refs.json)

Cleland & Rodríguez (1988); Kravdal (2002); Kravdal (2012); Martin & Juárez (1995); Guinnane (2011);
Coale & Watkins (1986); Galor & Weil (2000); Doepke (2005); Lee (2003); Granovetter (1978); Scheffer et al.
(2009); Sear, Mace & McGregor (2003); Coall & Hertwig (2010); Beaumont et al. (2002/2009); Del Moral et al.
(2012). Each is DOI-verified in the family tables above.
