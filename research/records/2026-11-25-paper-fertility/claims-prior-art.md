# Claims, closest prior art, and new-versus-replicated judgements (Paper F)

**Purpose.** For every empirical claim in the paper: the 3–8 closest works, full citation, DOI, Crossref status
(**V** = DOI resolves with matching metadata; **W** = working-paper/pre-publication version; **U** = no usable
DOI, hand-cited), and an explicit judgement of what is new here versus replicated. The paper's framing is a
**quantified audit of a known correlation**, never a discovery of a new correlation, and no claim uses "first".
The independent auditor's memo (novelty-review) was diffed against this list; gaps it found are incorporated and
noted at the end.

**Closest competitor, stated explicitly.** The closest claim-level competitor is **Caldwell (1980)** — mass
education as a determinant of the timing of the fertility decline. The paper agrees with the size and centrality
of the association and disagrees with the causal reading of the cross-country gradient, with the
future-schooling placebo as the measurable basis of the disagreement. The closest decomposition competitor is
**Kravdal (2002)** (individual vs community education effects in sub-Saharan Africa). The closest methodological
competitors are **Brock and Durlauf (2001)** and **Eberhardt and Teal (2011)**. The paper's distinct contribution
is the coordinated audit (full specification space + 13,800-partition transportability + placebo + threshold
location), not a new empirical relationship.

## A. The centrepiece claims

### A1. The schooling–fertility gradient is large and negative in levels, for all eight measures (S)

| work | DOI | status | relation to claim |
|---|---|---|---|
| Barro & Lee (2013), *J. Development Economics* 104, 184–198 | 10.1016/j.jdeveco.2012.10.001 | V | replicated: the canonical attainment data and the negative cross-country schooling–fertility link |
| Lutz & KC (2011), *Science* 333, 587–592 | 10.1126/science.1206964 | V | replicated: education–fertility link at the global accounting level |
| KC & Lutz (2017), *Global Environmental Change* 42, 181–192 | 10.1016/j.gloenvcha.2014.06.004 | V | replicated: education-specific human capital projections |
| Mincer (1958), *JPE* 66(4), 281–302 | 10.1086/258055 | V | theoretical lineage (human-capital investment and fertility) |
| Psacharopoulos & Patrinos (2004), *Education Economics* 12(2) | 10.1080/0964529042000239140 | V | replicated: returns-to-schooling context |
| Herzer, Strulik & Vollmer (2012), *J. Economic Growth* 17, 357–385 | 10.1007/s10887-012-9085-6 | V | replicated: long-run schooling–fertility cointegration |
| Murtin (2013), *Review of Economics and Statistics* 95(2) | 10.1162/rest_a_00302 | V | replicated: education among long-run transition determinants |
| Skirbekk (2008), *Demographic Research* 18, 145–180 | 10.4054/demres.2008.18.5 | V | replicated: negative educational fertility gradient |

**New vs replicated.** The *existence* of the negative level relation is fully replicated and older than this
paper. New: the same-panel, same-measures, eight-measure confirmation with the full specification curve and the
explicit statement that the level relation is a between-country gradient rather than an effect estimate.

### A2. The levels result is robust across the pre-registered specification space (S)

Closest works: Steegen, Tuerlinckx, Gelman & Vanpaemel (2016), *Perspectives on Psychological Science* 11(5),
702–712, 10.1177/1745691616658637, V; Simonsohn, Simmons & Nelson (2020), *Nature Human Behaviour* 4, 1208–1214,
10.1038/s41562-020-0912-z, V; Del Giudice & Gangestad (2021), *AMPPS* 4(2), 10.1177/2515245920954925, V;
Silberzahn et al. (2018), *AMPPS* 1(3), 337–356, 10.1177/2515245917747646, V; Levine & Renelt (1992), *AER*
82(4), 942–963, U; Sala-i-Martin (1997), *AER* 87(2), 178–183, U.

**New vs replicated.** Specification-curve reporting is a developed methodological literature; applying it to
this relation with a pre-registered, complete 336-cell grid is new to the project, and the paper reports the
distribution rather than a coefficient. No claim that the method is new.

### A3. The level relation is a global between-country property; the change relation is not (S)

| work | DOI | status | relation |
|---|---|---|---|
| Robinson (1950), *ASR* 15(3), 351–357 | 10.2307/2087176 | V | principle: ecological vs individual correlations — replicated idea, new application |
| Brock & Durlauf (2001), *World Bank Economic Review* 15(2), 229–272 | 10.1596/17447 | V | principle: level vs change regressions in cross-country work |
| Durlauf, Johnson & Temple (2005), *Handbook of Economic Growth* | 10.1016/s1574-0684(05)01008-7 | V | principle: growth econometrics critique |
| Eberhardt & Teal (2011), *J. Economic Surveys* 25(1) | 10.1111/j.1467-6419.2010.00624.x | V | closest methodological statement of level-vs-change fragility |
| King (1997), *A Solution to the Ecological Inference Problem* | 10.3886/icpsr01132.v1 | V | ecological-inference methodology (no re-partition test) |
| Kravdal (2002), *Demography* 39(2), 233–250 | 10.2307/3088337 | V | closest decomposition competitor: individual vs community effects |
| Kravdal (2012), *Demographic Research* 27 | 10.4054/demres.2012.27.22 | V | community education effects in SSA |
| Bareinboim & Pearl (2013), *J. Causal Inference* 1(1) | 10.1515/jci-2012-0004 | V | transportability formalism (not a re-partition test) |

**New vs replicated.** The *idea* that between and within estimates can disagree is replicated and old. New: the
random re-partition transportability experiment (13,800 partitions) for this relation, which turns "global
property" from an assertion into a measured distribution, and the matrix-wide honesty check.

### A4. The standard within-country change design erases the gradient (S)

Closest works: Nickell (1981), *Econometrica* 49(6), 1417–1426, 10.2307/1911408, V; Hausman & Taylor (1981),
*Econometrica* 49(6), 1377–1398, 10.2307/1911406, V; Angrist & Pischke (2009), *Mostly Harmless Econometrics*,
10.1515/9781400829828, V; Bell & Jones (2015), *PSRM* 3(1), 133–153, 10.1017/psrm.2014.7, V; Bertrand, Duflo &
Mullainathan (2004), *QJE* 119(1), 249–275, 10.3386/w8841, W; Roth (2022), *AER: Insights* 4(3), 305–322,
10.1257/aeri.20210236, V; Eberhardt & Teal (2011), as above.

**New vs replicated.** The within estimator's removal of between variation is textbook (replicated). New: the
demonstration, on one panel with the same eight measures and the full grids, that the change design erases the
gradient and that this is design-induced attenuation rather than a substantive null. The paper does not claim
the method is new; it claims the measured audit is new.

### A5. The level gradient is a development-gradient association, not an identified schooling effect (S)

Closest works: Davis (1963), *Population Index* 29(4), 345–366, 10.2307/2732014, V (change-and-response account);
Notestein (1945), *Food for the World*, U; Caldwell (1980), *PDR* 6(2), 225–255, 10.2307/1972729, V (closest
claim-level competitor); Lee (2003), *JEP* 17(4), 167–190, 10.1257/089533003772034943, V; Guinnane (2011), *JEL*
49(3), 589–614, 10.1257/jel.49.3.589, V; Doepke (2005), *J. Population Economics* 18(2), 337–366,
10.1007/s00148-004-0208-z, V; Galor & Weil (2000), *AER* 90(4), 806–828, 10.1257/aer.90.4.806, V.

**New vs replicated.** The development-gradient interpretation of cross-country associations is old (replicated).
New: the quantified future-schooling placebo showing the level relation is ~90% as strong when schooling is
measured after the outcome, and the pre-registered decision rule that converts this into a descriptive-not-causal
reading.

## B. The survey-level and null claims

### B1. A negative DHS survey-level schooling–fertility gradient exists across 86 countries (S, ecological)

Cleland & Rodriguez (1988), *Population Studies* 42(3), 10.1080/0032472031000143566, V; Kravdal (2002) as above;
Martín & Juárez (1995), *International Family Planning Perspectives* 21(2), 10.2307/2133523, V; Ainsworth, Beegle
& Nyamete (1996), *WBER* 10(1), 85–122, 10.1093/wber/10.1.85, V; Breierova & Duflo (2004), NBER WP 10513,
10.3386/w10513, W; Baird, McIntosh & Özler (2011), *QJE* 126(4), 1709–1753, 10.1093/qje/qjr032, V; Chicoine
(2012/2021), 10.2139/ssrn.2157920 / WBER, V/W; Osili & Long (2008), *J. Development Economics*, 10.3386/w13070, W;
Rutstein & Johnson (2004), DHS Comparative Report 6, U; Corsi et al. (2012), *IJE* 41(6), 1602–1613,
10.1093/ije/dys184, V.

**New vs replicated.** The individual gradient is replicated many times. New: the harmonised 81,962-cell
analysis across 377 surveys and the explicit reconciliation of the survey-level gradient with the macro change
null, plus the honest statement that the individual-level test could not be run.

### B2. The gradient steepens in later cohorts and denser pipelines (F — contradicted)

Same works as B1; additionally the pre-registered cohort/pipeline predictions were the project's own. **New vs
replicated:** the predictions were pre-registered and contradicted by the data; the attenuation (cohort
medians from −2.50 to −1.80) is consistent with composition, as the literature on education-category change would
predict, but the paper reports the contradiction rather than re-spinning it.

### B3. Care-work loop (F), strong no-off-switch (F), tipping point (F), weak no-off-switch (S)

Care economy: England & Folbre (1999), *Annals AAPSS* 561, 39–51, 10.1177/0002716299561001004, V (if DOI
unresolved, hand-cited); Folbre (2001), *The Invisible Heart*, U; Razavi (2007), UNRISD, U. Pronatalist policy:
Gauthier (2007), *Population Research and Policy Review* 26(3), 323–346, 10.1007/s11113-007-9033-x, V; Thevenon
(2011), *PDR* 37(1), 57–87, U (DOI not verified in-session); Thevenon & Gauthier (2011), *Community, Work &
Family* 14(4), 421–439, U. Critical transitions: Scheffer et al. (2009), *Nature* 461, 53–59,
10.1038/nature08227, V; Dakos et al. (2012), *PLoS ONE* 7(7), e41010, V; Granovetter (1978), *AJS* 83(6),
1420–1443, 10.1086/226707, V; Bongaarts & Watkins (1996), *PDR* 22(4), 639–682, 10.2307/2137804, V; Sear, Mace &
McGregor (2003), *Evolution and Human Behavior* 24(1), 25–42, 10.1016/s1090-5138(02)00105-8, V; Coall & Hertwig
(2010), *Behavioral and Brain Sciences* 33(1), 1–19, 10.1017/s0140525x09991105, V; Lesthaeghe (2010), *PDR*
36(2), 211–251, 10.1111/j.1728-4457.2010.00328.x, V.

**New vs replicated.** The nulls are new tests of the project's own pre-registered mechanisms, not replications of
specific published estimates; the critical-transition and care-economy literatures supply the hypotheses. The
paper's contribution is the falsification with placebos (male care-work, manufacturing) and the explicit verdict.

### B4. Transition model: mortality-led collapse (F), individuation out-of-sample (F/tie), tolerance ladder (F)

Notestein (1945), U; Davis (1945), *Annals AAPSS* 237, 1–11, 10.1177/000271624523700102, V; Caldwell (1976),
*PDR* 2(3/4), 321–366, 10.2307/1971615, V; Cleland & Wilson (1987), *Population Studies* 41(1), 5–30,
10.1080/0032472031000142516, V; Bongaarts (1978), *PDR* 4(1), 105–132, 10.2307/1972149, V; Galor & Weil (2000),
V; Becker & Barro (1988), *QJE* 103(1), 1–25, 10.2307/1882640, V; Doepke (2005), V; Guinnane (2011), V; Coale &
Watkins (1986), *The Decline of Fertility in Europe*, 10.1515/9781400886692, V (reissue); Beaumont, Zhang &
Balding (2002), *Genetics* 162(4), 2025–2035, 10.1093/genetics/162.4.2025, V; Beaumont, Cornuet, Marin & Robert
(2009), *Biometrika* 96(4), 983–990, 10.1093/biomet/asp052, V; Del Moral, Doucet & Jasra (2012), *Statistics and
Computing* 22, 1027–1043, 10.1007/s11222-011-9271-y, V.

**New vs replicated.** The transition ordering and mechanisms are replicated and old; the counterfactual
magnitudes (3.2% of the fall removed) and the out-of-sample tie are new to this project's calibrated engine, and
the paper explicitly labels them as model-based magnitudes, not sequence claims. The tolerance ladder is a
methods contribution: it shows the wide intervals are an identification limit.

### B5. Threshold shape: steep below six years, flat 6–9, reversed above nine (S)

Becker & Lewis (1973), *JPE* 81(2, Part 2), S279–S288, 10.1086/260166, V; Hanushek (1992), *JPE* 100(1), 84–117,
10.1086/261808, V; Black, Devereux & Salvanes (2005), *QJE* 120(2), 669–700, 10.1162/0033553053970179, V; Becker,
Cinnirella & Woessmann (2010), *J. Economic Growth* 15(3), 177–204, 10.2139/ssrn.1476206, W; Granovetter (1978),
V (thresholds in collective behaviour, different domain); Bongaarts & Watkins (1996), V (diffusion/threshold
dynamics). **No canonical DOI-verified paper on six-year/nine-year schooling hinges and fertility was found by
the auditor or by us**: the hinges are conventional boundaries from the attainment literature, chosen before
estimation, and the paper states that it does not imply an established threshold literature. **New vs
replicated:** the piecewise estimate and bootstrap intervals for this relation are new to the project; the
non-linearity of the quantity–quality trade-off is replicated background.

## C. Auditor gaps addressed (closure)

The auditor's memo (novelty-review) listed 15 missing DOI-verified works and 7 wrong-title entries. Response:
**added** Cleland & Rodriguez 1988; Kravdal 2002, 2012; Martín & Juárez 1995; Guinnane 2011; Coale & Watkins
1986; Galor & Weil 2000; Doepke 2005; Lee 2003; Granovetter 1978; Scheffer 2009; Sear, Mace & McGregor 2003; Coall
& Hertwig 2010; Beaumont 2002/2009; Del Moral 2012. **Fixed** notestein1945 (wrong paper → hand-cited classic),
davis1963 (wrong paper → Davis 1963 with correct DOI 10.2307/2732014; Davis & Blake 1956 kept separately),
becker1960 (wrong paper → hand-cited NBER chapter), schultz1961 (wrong paper → hand-cited AER 1961), trow1974
(year missing → hand-cited 1974 report), chen2010 (irrelevant 2026 paper → removed), bongaarts2011 (duplicate of
1978 → removed). Each fix is recorded in `lit/REFS_CLOSURE.md`. The auditor's point that the review may not use
"we are not aware" for the levels/changes principle is accepted: Section 2 frames the contribution as a
quantified audit, not a novel critique, and cites the principle as established.
