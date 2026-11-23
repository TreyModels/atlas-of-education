# SFI scaling-law and modelling scan for the Networked Domus theory

Worker `novelty-review`, branch `research/sfi-scan-2026-11-23`, 23 November 2026. Task-23. Literature scan only.
`[verified URL]` = a search result pointed at the work itself or its record; `[unverified]` = standard citation not
URL-confirmed today. Scope: the Santa Fe Institute scaling tradition and the complexity/ABM modelling traditions it
anchors, read against what the Networked Domus manuscripts actually claim. This does not restate the project's own
scaling or mechanism records; it extends them.

**The theory, in its own terms (from the Domus corpus).** The cooperative nest and the domus are one architecture
that scales by capturing other lineages; everything since the Neolithic is that architecture scaling. It makes
three quantitative moves: (a) settlement scaling — infrastructure sublinear, socioeconomic terms superlinear, with
monument construction near 7/6 and household productivity near 1/6 in the pre-Hispanic Basin of Mexico; (b) an
inhibition/specialisation formalism borrowed from Yang et al. — functional diversity grows sublinearly with system
size, governed by an inhibition parameter (θ) and a specialisation parameter (γ), with cities as the logarithmic
outlier; (c) the credential ratchet — once θ passes a critical value, adding scale adds almost no new functional
diversity, and credential categories proliferate faster than the real exits they open. The theory explicitly says
the θ/γ frame is a *diagnostic frame until a model is fitted to credential data*.

## Action table

| Source | Claim | Exponent / model | Relevance to Networked Domus | Testable prediction for us | Data needed |
|---|---|---|---|---|---|
| Bettencourt, Lobo, Strumsky & West 2007 PNAS, "Growth, innovation, scaling, and the pace of life in cities" [verified URL: pnas.org/doi/10.1073/pnas.0610172104] | Socioeconomic output superlinear, infrastructure sublinear | β ≈ 1.15 (1.01–1.27); infrastructure ≈ 0.85 (0.78–0.92); per-capita ≈ size^0.15 | The domus's superlinear/sublinear split is exactly this claim generalised to settlement | If the architecture is general, the same exponents should appear in archaeological settlements (Ortman) and in firm/organisational data | City-level output/wages/patents/infrastructure — **missing** |
| Bettencourt 2013 Science, "The origins of scaling in cities" [verified URL: science.org/doi/10.1126/science.1235823] | A network-based derivation of the exponents | β from network density and path length | Supplies the mechanism (network returns) the theory calls "pipework" | Network access/credential gates should predict who captures the superlinear return | City network data — missing |
| Bettencourt & West 2010 Nature, "A unified theory of urban living" [verified URL: nature.com/articles/467912a] | Cities as the leading edge of the scaling regime | review/synthesis | Theoretical anchor for "the city is the terminal node" | High-θ systems converge on similar functional distributions regardless of starting culture | Cross-country occupational/credential categories |
| Ortman, Cabaniss, Sturm & Bettencourt 2014 PLOS ONE, "The pre-history of urban scaling" [verified URL: journals.plos.org/plosone, pone.0087902]; 2015 Science Advances [unverified] | Settlement scaling in pre-Hispanic Basin of Mexico | area exponents 2/3–5/6; monuments ≈ 7/6; household productivity ≈ 1/6 | **The single most useful SFI result for the theory's deep-time claim** | Pre-modern settlements should show the same split without wheels, draft animals or fossil fuel | Archaeological settlement survey data (Ortman-type) — new pull, but small |
| Yang, Holehouse, Youn, Arroyo, Redner & West 2026 PNAS, "Scaling laws for function diversity and specialization across socioeconomic and biological complex systems" (arXiv 2208.06487) [verified URL: arxiv.org/html/2208.06487v2; LSE pnas.2509729123.pdf] | Functional diversity scales sublinearly with size; θ = inhibition between categories, γ = specialisation | sublinear diversity; cities logarithmic outlier; generalised Yule-Simon family | **The theory's quantitative core for the credential ratchet** | Estimate θ and γ on occupational/credential categories; θ should rise with development; diversity should flatten logarithmically at high credential density | Occupation categories at 2–3 digit depth (ILOSTAT now 1-digit only — our binding constraint); credential counts (not held) |
| Holehouse, Redner, Yang, Krapivsky, Arroyo, West, Kempes & Youn 2025, "A generative model of function growth…" [verified URL: arxiv.org/abs/2509.14468] | Generative model of category growth by novelty + preferential attachment | Yule-Simon style | Explains category proliferation without real functional gain | Credential counts should grow faster than distinct functions; both follow the model's shape | Credential/occupation time series |
| Firm/organisation scaling: company scaling studies (Chalmers fulltext [verified URL: research.chalmers.se]; Kobayashi et al. 2021 Entropy [verified URL]) | Sales ~ employees^≈1; overhead ~ employees^≈0.85 | ≈1 and ≈0.85 | If the domus is an organisation, its overhead should scale like infrastructure | Administrative/enforcement cost should scale sublinearly with population while surplus scales superlinearly | Firm/agency microdata — missing |
| Arthur 1999 Science, "Complexity and the economy" [verified URL: science.org/doi/10.1126/science.284.5411.107]; W. B. Arthur SFI page [verified URL: sites.santafe.edu/~wbarthur] | Increasing returns, path dependence, lock-in | qualitative/complexity economics | Formal language for the ratchet and for "the dominant category absorbs investment" | Early institutional choices should predict later occupational concentration | Historical occupation/institution series |
| Epstein & Axtell 1996, *Growing Artificial Societies* (Sugarscape) [verified URL: mitpress.mit.edu] | Agent-based societies can generate macro patterns from micro rules | ABM | Methodological ancestor of our dose/ABM work | Our ABM should reproduce occupational diversity scaling as an emergent property, not an assumption | none beyond our ABM |
| Laland, Odling-Smee & Feldman niche-construction literature (BBS) [verified URL: cambridge.org/core BBS] | Organisms construct the niche that then selects on them | evolutionary model | The domus is a constructed niche; "capture" is niche construction with other lineages | Niche-construction intensity should predict domestication depth and path dependence | Archaeological/energy-throughput proxies |
| Tainter 1988, *The Collapse of Complex Societies* [verified URL: Zenon record]; Scheffer et al. 2009 Nature early-warning signals [verified URL: Crossref doi 10.1038/nature08227] | Marginal returns to complexity decline; critical transitions have early-warning signatures | diminishing returns; rising variance/autocorrelation before transition | Formal language for "terminal enclosure" and its failure mode | Before a fertility or institutional transition, variance and autocorrelation should rise | Panel with long country series; feasible in principle |
| Structural change beyond Boppart: Herrendorf, Rogerson & Valentinyi 2014 [unverified URL]; Ngai & Pissarides 2007 [unverified]; Acemoglu & Restrepo 2018/2019 on automation [verified URL: aeaweb AER 10.1257/aer.20160696; JEP 33.2.3] | Sectoral labour reallocation and mechanisation displace/reinstate labour | structural-change models; task-based automation | Explains the agricultural-transition/labour-release side of the domus | Farm-input and mechanisation changes should move labour out of agriculture before they move births (our input-price work already found the birth link null) | Our panel has agri_va, emp_agri, wage_emp — testable now |
| Cultural evolution: Boyd & Richerson dual inheritance [unverified]; Henrich & McElreath [unverified] | Cumulative culture, transmission biases, path dependence | cultural-evolution models | Explains why the domus package converges across unconnected regions | Independent domestication centres should converge on similar institutional sequences | Domestication/institution timelines |

## Ranked reading list (top 10)

1. **Yang et al. 2026 PNAS** (arXiv 2208.06487) — the θ/γ formalism the theory depends on; read for the exact model,
   the systems covered, and what "cities are the outlier" means quantitatively.
2. **Ortman et al. 2014 PLOS ONE and 2015 Science Advances** — settlement scaling in an ancient society; the only
   SFI result that directly tests the domus architecture in deep time.
3. **Bettencourt et al. 2007 PNAS** — the canonical urban scaling exponents and their ranges.
4. **Bettencourt 2013 Science** — the network derivation; why the exponents take these values.
5. **Holehouse et al. 2025 arXiv** — the generative model of function growth; the mechanism behind category
   proliferation.
6. **Bettencourt & West 2010 Nature** — the synthesis that the theory's "scaling regime" language comes from.
7. **Arthur 1999 Science** — increasing returns and lock-in; the economics behind the ratchet.
8. **Tainter 1988** — diminishing returns to complexity; the collapse side of "terminal enclosure".
9. **Scheffer et al. 2009 Nature** — early-warning indicators; how one would test an approaching transition.
10. **Epstein & Axtell 1996** — the ABM tradition our dose model belongs to.

## The three SFI ideas most likely to be new to this project

1. **Estimating θ and γ rather than invoking them.** The theory uses the diversity/specialisation formalism
   diagnostically, and the manuscript is explicit that it has not been fitted. Nobody in the project has yet
   estimated an inhibition or specialisation parameter on occupation or credential categories. That is the single
   most direct quantitative test the theory offers — and the binding constraint is category depth (ILOSTAT is now
   1-digit; 2–3 digit is needed, and credential counts are not held).
2. **Settlement scaling as a deep-time test that does not need modern city output data.** Ortman's archaeological
   scaling (area, monuments, household productivity) is a way to test the superlinear/sublinear split on a
   civilisation with no wheels or fossil fuel. It is the only feasible route to the theory's strongest empirical
   claim; it needs a small, public survey dataset rather than new country-level measurement.
3. **Collapse and tipping-point formalism for "terminal enclosure".** Scheffer's early-warning signatures (rising
   variance and autocorrelation before a critical transition) and Tainter's diminishing returns give the theory
   testable predictions about failure, not just about scaling. Our long country panels could carry at least a
   demonstration on fertility or institutional transitions.

## What this scan does NOT support

The "universal scaling law" reading is influential but contested: exponents vary with boundary definitions,
indicator construction and regime; the urban scaling result is robust in direction far more than in precise value
(the theory's own manuscript says this). Tainter's collapse thesis is influential rather than established. The
Yang formalism is new and has few independent replications. Saying "the domus obeys a scaling law" is a research
programme, not a finding, until θ and γ are estimated.

## (1) Fertility

The SFI material bears on fertility only indirectly, through collapse/tipping-point dynamics and through the
structural-change/mechanisation literature. Our own level-versus-volatility and survival results remain the core;
nothing in the SFI canon gives a better country-level fertility test than what we have already run.

## (2) Massification

The relevant SFI material is the functional-diversity formalism (occupational/credential categories vs system
size), settlement scaling, and the organisational-scaling results. The credential-ratchet prediction — credential
categories proliferate while distinct functions do not — is testable only with credential counts plus 2–3 digit
occupation categories, neither of which we currently hold at depth; that is the honest data gap.

*Verification caveat: web_search only. Items marked `[unverified]` need a publisher check before a paper;
"influential" and "evidenced" are kept apart throughout.*
