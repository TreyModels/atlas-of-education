# Claim-by-claim prior art

For each claim in Paper 3: the status in this paper (replication / correction / new), the closest prior work,
the specific increment over that work, and the Crossref status of every DOI (checked 24 Nov 2026 by querying
`api.crossref.org`). "Replicated" means we re-estimated the same object from rebuilt data; "corrected" means we
replaced a test that did not measure the object; "new" means the object is not in the original or the
antecedents as far as this search found.

| # | claim | status | closest prior work | what is new here | DOI status |
|---|---|---|---|---|---|
| 1 | In poor countries investment and intermediate goods are expensive relative to labour because non-agricultural TFP is low, so farmers substitute labour into agriculture | **replication** (cross-sectional link) | Boppart, Kiernan, Krusell & Malmberg (2023) 10.3386/w31101; Restuccia & Rogerson (2008); Restuccia, Yang & Zhu (2008) 10.1016/j.jmoneco.2007.11.006; Caselli & Coleman (2001) 10.1086/321015; Herrendorf, Rogerson & Valentinyi (2014) 10.3386/w18996 | re-estimated on rebuilt USDA/PWT data; the mechanism holds in direction, elasticities lower than the paper's | verified, except Restuccia-Rogerson 2008 (chapter not returned by Crossref; related Rogerson 2019 chapter verified 10.1093/oxfordhb/9780198793847.013.2) |
| 2 | The substitution elasticity between capital and labour, and between intermediates and labour, exceeds one | **replication** | Boppart et al. (2023); Alvarez-Cuadrado, Long & Poschke (2017) 10.3982/te2106; Alder, Boppart & Müller (2022) 10.1257/mac.20190303 | our point estimates are **lower** (1.24/1.11 in 2005 against 1.90/1.75), and the land elasticity is not estimable without GAEZ land quality; reported as partial replication | verified |
| 3 | Input intensification explains roughly two-thirds of the agricultural labour-productivity gap | **replication** (order of magnitude) | Boppart et al. (2023); Gollin, Lagakos & Waugh (2014) 10.1093/qje/qjt056; Restuccia, Yang & Zhu (2008); Duarte & Restuccia (2010) 10.1162/qjec.2010.125.1.129 | rebuilt decomposition gives 55-69%, consistent with "a bit less than two-thirds" | verified |
| 4 | Relative input price and input intensity are strongly negatively associated across countries | **replication** | Boppart et al. (2023) | independent rebuilt estimate, -1.13 (0.15) and -1.28 (0.11), two benchmark years | verified |
| 5 | Intensity is negatively associated with the agricultural employment share | **replication** | Boppart et al. (2023); Herrendorf, Rogerson & Valentinyi (2013) 10.1257/aer.103.7.2752 | rebuilt cross-section, -4.71 (0.89) and -4.38 (1.15), with the relative-price coefficient insignificant | verified |
| 6 | Input adoption **precedes** labour release in the transition | **new test; not identified** | Boppart et al. (2023) is cross-sectional; the closest dynamic work is Alder, Boppart & Müller (2022); Alvarez-Cuadrado et al. (2017) | a ten-year country panel with country and decade fixed effects; the level association is the wrong sign (+1.75) and the reverse association is stronger (-3.32), so the ordering cannot be established. This is a **negative** result about a claim the theory needs | verified |
| 7 | Labour release feeds schooling and lowers fertility at decadal horizons | **new test; precise null** | no antecedent estimates this link at this horizon; the project's own transition and dose records do so over longer horizons and with models | a precise null: fertility change -0.0003 (0.0058), n=503, MDE about 0.016 births; reported as a null with power | n/a |
| 8 | The project's earlier "Boppart test" (world commodity price index × farm-employment share) did not test this paper's object | **correction** | none: this is the project's own earlier test, not a published claim | replaces a proxy test with the paper's actual objects (input quantities, relative prices, substitution elasticity, development decomposition); stated factually | n/a |
| 9 | A joint demography-agriculture-absorber model can reproduce the stylised transition | **new demonstration** | Alder, Boppart & Müller (2022); Boppart et al. (2023); Herrendorf et al. (2014) | a demonstration model with 5 free parameters, 2 of 5 identified; the mortality decline is the first mover, mechanisation empties agriculture, the pipeline converts released labour into schooling | verified (antecedents) |
| 10 | Replication should be reported with pre-registration, deviations and a data-availability statement | **procedural** (the paper's own standard) | Christensen & Miguel (2018) 10.1257/jel.20171350; Nosek et al. (2015) 10.1126/science.aab2374; Nosek, Spies & Motyl (2012) 10.1177/1745691612459058; Open Science Collaboration (2015) 10.1126/science.aac4716; Mueller-Langer et al. (2019) 10.1016/j.respol.2018.07.019 | applied to a macro-development paper rather than to laboratory experiments or to randomised trials | verified; Camerer et al. (2016) DOI not verified in session |

## Reading of the prior-art position
- The **object-level replication** (claims 1-5) is a replication of Boppart et al. with rebuilt data and a
  honest statement that our elasticities are lower and the land margin untestable. It is not a confirmation.
- The **sequencing tests** (claims 6-7) are new in the sense that the original paper does not estimate them;
  both return negatives. We do not claim that no one has studied the sequencing of mechanisation and labour
  release historically — that literature is large (see the historical-sequence record) — only that the
  country-panel test does not identify it.
- The **correction** (claim 8) is about a test internal to this project. It is stated factually: the earlier
  test measured the exposure of farm employment to a common world price shock, which contains none of the
  paper's objects, so it could not see the paper's mechanism even in principle. That is a statement about what
  the test measured, not about anyone's competence.
- No claim of being first appears anywhere in the paper. Where a result is new within this project, it is
  labelled "new test" and the closest external literature is named.
