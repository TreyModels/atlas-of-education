# Literature review: sweeps, lead-lag maps and Trow-threshold tests for educational expansion

Verification key. [V] means I opened the abstract or paper this session. [M] means it is cited from memory and I did not check it. Details marked [M] (years, exact findings) should be confirmed before they go into a manuscript.

## 1. Has this been done before?

**Bottom line.** I found no study that combines (a) extreme-bounds or Sala-i-Martin robustness over education-expansion outcomes, (b) the same sweep with every variable as outcome to give a directed map, and (c) a joint-necessity hazard test for the Trow 15% threshold. The pieces exist separately. Absence from my searches is not proof of absence; only a handful of searches were run.

**Robustness and BMA methods (the toolkit)**
- Levine & Renelt 1992 (AER), extreme-bounds analysis of growth regressions; few variables survive [M].
- Sala-i-Martin 1997 (AER, "I just ran two million regressions"), CDF-based robustness; this is the origin of your CDF(0)>=0.95 rule [M].
- Sala-i-Martin, Doppelhofer & Miller 2004 (AER), BACE for growth [M].
- Fernández, Ley & Steel 2001 (J. Applied Econometrics), BMA for growth [M].
- Applications to educational outcomes are thin. I did not find BMA or EBA applied to enrollment expansion specifically [not found].

**Cross-national determinants of educational expansion**
- Schofer & Meyer 2005 (ASR): pooled panels, 1900-2000. Higher-education enrollment rises more in countries tied into world society, with high secondary enrollment and greater development, and where state control is weaker. Global trends outweigh national differences. [V]
- Meyer, Ramirez & Soysal 1992 (Sociology of Education): world-polity account of primary expansion, with expansion driven by institutional isomorphism more than by economic demand [M].
- Clemens 2004 (CGD WP 37, "The Long Walk to School"): enrollment rises slowly and uniformly. Economic conditions and slowly changing parental education matter more than policy. Many countries that missed the MDGs still expanded quickly by historical standards. [V, abstract only]
- Yu & Delaney 2016 (Educational Policy 30(2)): event-history model of tertiary policy using Trow's 15% and 50% thresholds, 1999-2005. Secondary participation and politics matter, and diffusion matters through proximity to pioneers and region. [V]. This is the closest antecedent to your hazard test, but it has no joint-necessity conditions.
- Benavot and Riddle 1988 and Benavot 1996 on primary expansion, and Barro & Lee 1993/2013 (attainment data) [M]. Cohen & Soto 2007 (J. Economic Growth, "Growth and human capital: good data, good results"): cleaner attainment data [V, title only].
- Lutz, Cuaresma & Sanderson 2008 (Science, "The demography of educational attainment and economic growth"): the age structure of attainment matters for growth [V, title only]. Lutz & KC 2011 (Science) projects attainment from demographic cohort-component models [M].

**Education versus democracy and income (sequencing)**
- Acemoglu, Johnson, Robinson & Yared 2005 (NBER WP 11204, "From Education to Democracy?"): the education coefficient is +0.027 in pooled OLS but -0.005 (SE 0.019) with country fixed effects, -0.018 with Anderson-Hsiao and -0.017 with Arellano-Bond. They conclude there is no evidence that expanding education makes countries more democratic. [V] This is the key cautionary precedent for your "X leads Y" claims: cross-sectional lead-lag can vanish within countries.
- Glaeser, La Porta, Lopez-de-Silanes & Shleifer 2004 (J. Economic Growth, "Do institutions cause growth?"): human capital precedes institutions [M].
- Bils & Klenow 2000 (AER): schooling and growth, with reverse causality; growth explains only a minority of the schooling-growth link [M].

**Data-driven development dynamics**
- Spaiser, Ranganathan, Bali Swain & Sumpter 2017 (Int. J. Sustainable Development & World Ecology 24(6)): dynamical-systems models of SDG indicators. Growth and consumption drive conflicts among goals, while government investment in education, health and renewables avoids them. [V]. The earlier Spaiser et al. 2014 paper on democracy, development and cultural values is by the same group (a fit of coupled ODEs to country panels) [M on details; the White Rose repository listing was seen but not opened].
- Hidalgo & Hausmann 2009 (PNAS) on economic complexity; Hartmann et al. 2017 (World Development) link complexity to inequality, and schooling-complexity links exist [M]. I did not find a causal-discovery (PC/FCI) study of education indicators [not found].
- Quantity-quality fertility-schooling: Becker & Lewis 1973 and Galor & Weil 2000 are theory [M]. Empirical cross-country support is mixed. Lutz-type work supports education to fertility, with reverse links in the micro literature [M]. Your finding that fertility and child mortality lead and tertiary lags is consistent with Galor-style demographic-transition sequencing, but this is not tested against it.

## 2. Tighter versions of the test

Your design has these weaknesses:
- Regressing a 10-year change on levels with fixed decade dummies and no country effects is exposed to omitted-country-trait confounding, which is exactly the Acemoglu et al. problem above.
- With level included and country effects added, you get Nickell bias.
- "Predicts X but not vice versa" is a difference between a significant and a non-significant result. It is not itself a test.
- Thousands of CDF tests need multiplicity control.

Assessment of the options, and the three best upgrades:

1. **Add country fixed effects with a dynamic-panel-bias-safe estimator, and test asymmetry directly (best upgrade).**
   - Use half-panel jackknife or split-panel correction (Dhaene & Jochmans 2015, Rev. Econ. Studies [M]) or Juodis, Karavias & Sarafidis 2021 (Empirical Economics, "A homogeneous approach to testing for Granger non-causality in heterogeneous panels" [V, title and listing seen]). System GMM is weak here because T is short (about 4-5 decades) and instruments proliferate.
   - Pre-specify the asymmetry test as the difference of coefficients (beta_XY minus beta_YX) with a clustered bootstrap, not "significant versus not."
   - Justification: this is the only change that addresses the Acemoglu et al. within-country result.

2. **Replace pairs/singletons-of-controls EBA with BMA using dilution priors (or a double/debiased-ML partialling step), plus FDR control.**
   - Variables such as fertility, child mortality and youth share are near-collinear. Pair/singleton conditioning sets cannot absorb a collinear block, so "robust" can mean "proxy for the demographic block."
   - Options: BMA with dilution priors (George 2010 [M]) or Moral-Benito 2012 (dynamic-panel BMA, J. Applied Econometrics [M]). Or DML (Chernozhukov et al. 2018, Econometrics J.) with random-forest nuisance functions [M].
   - For 58 x 57 directed tests, control the false discovery rate with Benjamini-Hochberg or Benjamini-Yekutieli (dependence), and report q-values. Add a placebo test with permuted lead-lag direction.
   - Your two-half replication is a good start. Randomize it over many splits (about 200), report a stability proportion, and split by region or cluster, not random countries, to avoid spillover leakage.

3. **Event studies and out-of-sample forecasting as external validation of direction.**
   - Dated shocks: fee abolitions (Uganda 1997, Malawi 1994, Kenya 2003), electrification rollouts. Use staggered-adoption DiD estimators (Callaway & Sant'Anna 2021; Sun & Abraham 2021 [M]). Check that the "leaders" move first and the "followers" respond.
   - Use true out-of-sample forecasting (rolling-origin by decade) to test whether lagged "leaders" improve forecasts of "followers" over own lags and AR benchmarks (Diebold-Mariano). Your additive-beats-conjunctive result is already an out-of-sample comparison and the same logic extends to the map.

Lower priority:
- **Local projections (Jordà 2005, AER [M]):** useful for impulse-response shapes, but with 4-5 time points they are unstable.
- **Panel VAR:** works with 3-6 variables, not 58, so use it for a reduced system (fertility, primary completion, GDPpc, tertiary GER, government spending).
- **PC/FCI:** assumes causal sufficiency and faces cycles and feedback here; use PCMCI (Runge et al. 2019, Science Advances [M]) at best.
- **Convergent cross mapping (Sugihara et al. 2012):** needs long time series, so it is poorly suited to 5 decades per country.
- **Synthetic control:** fine for single-country shocks but not for the map.
- **Pre-registration:** register the direction rule and the FDR level before touching a held-out period (for example, the 2015-2020 data).

## 3. Thresholds and functional forms

- **Trow's 15% and 50%.** These are descriptive stage labels from Trow 1973 (elite, mass, universal) [M]. The only formal empirical use I verified is Yu & Delaney 2016 (event-history around the thresholds, 1999-2005). [V] Marginson 2016 (Higher Education, "The worldwide trend to high participation higher education: dynamics of social stratification in inclusive systems") argues that "high participation systems" past roughly 50% have dynamics of their own [M; I did not retrieve it]. I found no study that tests whether 15% is a true structural break (as opposed to a convention).
- **S-curves and logistic diffusion.** Logistic or Gompertz forms are the standard in diffusion work (Griliches 1957-style adoption). Schofer & Meyer describe acceleration after 1960 and global trends over national ones, consistent with sigmoidal world-level diffusion [V]. Clemens 2004 reports a uniform pattern of enrollment growth across countries and a roughly consistent historical pace [V, abstract only]. Specific rate figures were not retrieved.
- **Scaling with income or urbanisation.** I did not verify a published power-law result for enrollment. The usual empirical form is enrollment roughly linear in log GDPpc, capped by saturation at 100% for primary and secondary. It is not "power-law" in the strict sense. Treat any claimed scaling exponent as unverified.
- **Tipping points and dynamical systems.** Spaiser et al. use polynomial ODE systems fit to country panels and find nonlinear regimes [V on the 2017 paper, M on the form]. Their framework is the nearest to your "leaders versus followers," but it models dynamics, not thresholds on enrollment.

**What the evidence supports (my synthesis).** A saturating logistic or log-linear-in-income S-curve, with additive (not conjunctive) enabling factors, fits your own out-of-sample result. A joint "all three conditions necessary" threshold has no published support that I found. 15% is better modelled as a smooth region on the S-curve than as a hard gate. Test a logistic-in-income hazard against a threshold-dummy hazard on a held-out set.

**Not verified:** every [M] item; the specific exponents or rates in Clemens 2004; the Marginson claim; Spaiser 2014 details. Search snippets for several queries returned only link lists.
