# "Generative comparative education": methods paper outline

Draft outline, 6 November 2026. Working title: **"Generative comparative education: building, docking and falsifying mechanism models of education systems"**. Target: a methods paper (TODO §14 P2), with the China forecast failure as the empirical spine. This is an outline for Trey to cut, not prose.

**Central claim (one sentence):** Comparative education can be made cumulative if each explanation is built as an executable micro-mechanism inside exact accounting, docked to simpler rivals, confronted jointly with multiple patterns it was not tuned to, and scored under an information set fixed before the outcome is seen — and the value of that standard is shown not when a model succeeds but when it fails in public.

**Secondary claims:** (1) this is Boudon's generative question recovered for comparative education, not a new theory of education; (2) Epstein's generative criterion supplies the epistemology, but the project adds an empirical-credibility test Epstein does not require; (3) the "cocoon" of accounting, docking, pattern-oriented modelling and history matching is what makes an ABM an argument rather than an illustration; (4) the China forecast is the paper's strongest evidence because it is a clean negative result under a declared protocol; (5) the programme is falsifiable at the level of its method, not only its models.

---

## 1. Target journals, fit and word plan

| Journal | Fit | What the paper must become | Risk |
|---|---|---|---|
| **Comparative Education Review** (University of Chicago Press; journal of the Comparative and International Education Society) | The discipline's flagship for comparative method and theory; a paper arguing how comparative education should test explanations belongs here; the Boudon/Epstein lineage fits its readership | Lead with the disciplinary problem and the method; keep code detail in an appendix; one China figure, one Cambodia figure, one falsification table | Reviewers may see ABM as a foreign method; needs the "why not just econometrics" section up front, not in the conclusion |
| **International Journal of Educational Development** (Elsevier) | Best fit for the applied cases (China graduate labour market, Cambodia child labour) and for a method that speaks to policy modellers; higher tolerance for simulation and for country detail | Lead with the two cases and the policy-planning payoff; shorten the ancestry; expand the "what a planner should take from this" section | Methods novelty may be read as technical rather than conceptual; needs the comparative claim stated in the first page |
| **Comparative Education** (Taylor & Francis) | Strong home for the theory lineage (Boudon, positional goods, comparative method) and for a special issue; shorter empirical sections expected | Lead with the theory of comparison: what it means to explain a national pattern generatively; treat cases as illustrations of the method | Less receptive to a forecast-score table; the honest-failure argument may need reframing as a theory of evidence |

**Recommendation:** submit first to **IJED** if the goal is readership among education planners and development economists; to **CER** if the goal is a disciplinary intervention. Prepare the CER version first anyway — the discipline-first framing forces the paper's claim to be about comparative method, which is what makes it more than a project report.

**Two word-count plans** (journal limits to be confirmed against current author guidelines before submission; these are our targets, not quoted journal rules):

| Section | IJED version (~8,500 words excl. references) | CER/CE version (~9,500 words excl. references) |
|---|---:|---:|
| Abstract + keywords | 200 | 200 |
| 1. Introduction: the non-cumulation problem | 1,000 | 1,300 |
| 2. Ancestry: Boudon's generative question | 800 | 1,200 |
| 3. Ancestry: Epstein's standard | 700 | 1,000 |
| 4. The cocoon (four insulations) | 1,900 | 2,200 |
| 5. The protocol: information sets and benchmarks | 1,000 | 1,200 |
| 6. Case 1: China, the honest failure | 1,500 | 1,300 |
| 7. Case 2: Cambodia and the cross-country tests | 1,100 | 900 |
| 8. Falsification conditions | 700 | 900 |
| 9. Objections and replies | 700 | 700 |
| 10. Conclusion: from models to a benchmark platform | 500 | 600 |
| Tables/figures (counted space) | 400 | 400 |
| **Total** | **~8,500** | **~9,500** |
| References | ~1,400 (excluded) | ~1,600 (excluded) |
| Appendix A (repo map) | 400 (online) | 400 (online) |

---

## 2. Abstract (draft, ~190 words)

Comparative education explains national patterns with theories that rarely run, which makes rival explanations hard to separate and failures hard to see. This paper sets out a method — generative comparative education — for turning such explanations into executable models and testing them against data they were not tuned to. It recovers the demand for generative explanation from Boudon's (1974) analysis of educational expansion and inequality, and the epistemic standard from Epstein's agent-based generative social science, and it adds a discipline for empirical credibility: stock-flow consistency, docking, pattern-oriented modelling and history matching, inside an explicit information-set protocol. The method is shown through its failures and partial successes: a China graduate-labour model that fits history and loses to a naive forecast (1.09 against 0.89 points), a Cambodia child-labour model whose policy directions are robust while its level is not calibrated, and a cross-country model of school exit that reproduces two national patterns and fails a third. The paper states what would falsify the programme and argues that public, benchmarked model failure is a comparative-education method, not an embarrassment.

**Keywords:** comparative education; generative social science; agent-based models; educational expansion; causal mechanisms; model verification; China; Cambodia.

---

## 3. Section-by-section outline with the central claim of each

### 1. Introduction: why comparative education does not accumulate (~1,000–1,300 words)

**Central claim:** The field's explanatory debates recur because rival explanations are verbal and therefore underdetermined; their predictions are not written down, so the same evidence can be narrated by several theories, and a theory that would fail cannot be identified. The fix is not more data or more theory but a public specification of mechanism plus a test that the mechanism did not see.

Content: the recurring "bar has moved" problem (credential expansion that does not equalize opportunity — the book's chapter 1 argument, TODO §R); three symptoms (untestable rivalries, post-hoc mechanism lists, forecasts that are never scored); what would count as progress; the paper's plan. Introduce the Atlas as the working example, not the subject. State the paper's own scope: method, not a new theory of education; examples, not a survey.

### 2. Ancestry I: Boudon's generative question (~800–1,200 words)

**Central claim:** Boudon (1974) already asked the question this paper formalises — how do micro-level educational decisions and institutional rules generate a macro distribution of opportunity, and why can expansion leave inequality intact? The paper inherits the question and the insistence on mechanisms; it adds executability, exact accounting and data confrontation.

Content: Boudon's *Education, Opportunity, and Social Inequality: Changing Prospects in Western Society* (New York: Wiley, 1974; ISBN 0471091057); his distinction between inequality of educational opportunity and inequality of social opportunity; the result usually called the Boudon effect (educational expansion need not equalise social opportunity because the value of a credential is positional); the generative structure of his argument (micro decisions → distribution). What Boudon did not have: a computer, a stock-flow ledger, and a held-out test. Be precise: we are not claiming Boudon built a model; we are claiming he specified a mechanism whose execution was analytically intractable. Contrast with the field's later turn to large-scale assessment and cross-national regression, which improved measurement while leaving mechanism underdetermined.

### 3. Ancestry II: Epstein's standard (~700–1,000 words)

**Central claim:** Epstein's generative criterion ("to explain a macro regularity is to grow it from a micro-specification") supplies the epistemology, but it is a criterion of *generative sufficiency*, not of empirical credibility; the paper's contribution is to add the credibility test that generative social science often leaves implicit.

Content: Epstein (1999, *Complexity* 4(5): 41–60) and Epstein (2006, *Generative Social Science*, Princeton UP); the generative maxim commonly compressed as "if you didn't grow it, you didn't explain it"; Epstein's (2008, "Why Model?", *JASSS* 11(4): 12) distinction between explanation and prediction, and the sixteen reasons to model. The paper's two-part standard: **generative adequacy** (the model generates the target pattern from plausible micro rules — necessary, not sufficient) and **out-of-sample credibility** (it generates patterns it was not tuned to, scored under a protocol fixed in advance — the part ABM practice often omits). This section must say plainly that a model that fits history has not thereby explained it.

### 4. The cocoon: four insulations and the uncertainty layers (~1,900–2,200 words)

**Central claim:** An ABM becomes an argument only when it is insulated from four standard objections — that it violates accounting, that it is a one-off whose results depend on implementation, that a single pattern can always be fitted, and that calibration is unconstrained. The four insulations are stock-flow consistency, docking, pattern-oriented modelling and history matching; uncertainty is then handled in four declared layers.

**4.1 Stock-flow consistency.** Central claim: identities are the part of a social model that can be beyond dispute, and an identity violation is a bug, not a finding. Content: people and money ledgers; every person in exactly one state; every payment with payer and payee. Evidence from the repo: firm-side stock balance residual **1.42e-14**, free-entry residual **8.88e-16** (`docs/china_fit.md`); the planning kernel's **1,000** random conservation cases and invalid-input tests (`planning/test_kernel.cjs`); camchild spending identity, `cash = amount × eligible × years` (`tests/test_camchild.cjs`); the reconstructed-cohort closure **<1e-9** (`engine/tests.py`). Cite Godley & Lavoie (2007) for the stock-flow-consistent accounting tradition.

**4.2 Docking.** Central claim: a new model must reproduce its predecessor as a special case, or its added mechanisms are not identified against the simpler account. Content: docking as the ABM analogue of nesting. Evidence: `categorical.py` nests `model.py` to **1e-10**; the seasonal model nests the base model to **1e-9** (`engine/firms/test_firms.py`); browser–Python parity worst difference **1.29e-7** (`tests/js_parity.mjs`); the Python twin of the Cambodia world reproduces every household choice with worst numeric difference **0.0e+00** (`tests/camchild_parity.py`). Cite Axtell, Axelrod, Epstein & Cohen (1996) on aligning simulation models.

**4.3 Pattern-oriented modelling.** Central claim: one pattern can be fitted by many structures; several patterns jointly constrain. Content: Grimm et al. (2005) pattern-oriented modelling; the project's use of multiple weak patterns. Evidence: the floorworld test of eight patterns in four countries (`docs/education_and_formalization.md` — demand-led S2 passes all eight in **14.7%** of 6,000 draws, human-capital S1 in **10.3%**, hybrid S5 in **0.7%**); the childworld use of two country numbers to separate four-state patterns (`docs/asia_school_work.md`); the round-8 floor test's six arms (`related/massification_project/results/round8_mechanisms_and_ledger_fix/floor_test/findings.txt`). Also state the failure mode: adding patterns until the model passes is not POM; the pattern set must be fixed before fitting.

**4.4 History matching.** Central claim: calibration should rule out regions of parameter space that are inconsistent with evidence, not search for a single best fit; the output of a calibration is a set of not-ruled-out worlds, and the object to report is what that set still cannot say. Content: Craig et al. (2001) Bayesian history matching; the project's practical equivalents: ABC tolerance matching in `engine/mc.py` and `childworld_mc.py`; the strict information sets in `forecast_strict.py`; the parameter-valley profiling still to be done on the tournament winner (TODO P2). Introduce the project's **facts register** convention (`docs/facts_register.md`): every number an engine is scored against is labelled **calibration / test / diagnostic / input**, and a headline number must say which it is. This is the paper's most transferable institutional device: a register that prevents fit statistics being reported as evidence.

**4.5 Uncertainty in four layers.** Central claim: simulation noise, parameter uncertainty, structural uncertainty and measurement uncertainty are different things and must not be reported as one band. Evidence: `engine/mc.py` and `engine/test_mc.py` (15 tests: Ishigami Sobol indices within **0.04** of analytic values, additive shares **0.9 / 0.1**, matched seeds cancel a common shock exactly, parallel equals serial, no sign claim when the interval includes zero); childworld Sobol stiff directions (`engine/results/childworld_sobol.md`: value of state D total-order **0.80** for the neither-share; value of school **0.41** for child-labourers-in-school); the Angkor lab's explicit distinction between 10th–90th percentile bands and bootstrap intervals (`worlds/angkor/reference/monte_carlo_lab/README.md`); the "three kinds of uncertainty" framing in the cocoon memo. Say what a seed band is not: it is not a confidence interval about the world.

### 5. The protocol: information sets, benchmarks and pre-registration (~1,000–1,200 words)

**Central claim:** A forecast or evaluation is informative only if (a) the model's information set is fixed at a date, (b) the benchmark is a naive rule using the same information, (c) the scoring rule is written down before the outcome is seen, and (d) the code is tested for leaks from the test period into the fit. Otherwise "the model failed" and "the model was never asked" are indistinguishable.

Content: the Dec 2022 and Dec 2024 cutoffs (`firms/forecast_strict.py`, `forecast_2024.py`); the leak tests — `demand_leak_check() == 0.0` and `stories_strict.leak_check() == 0.0`, plus the deliberately non-vacuous companion test that perturbing pre-cutoff observations *does* move the residuals (`engine/firms/test_firms.py`); the naive benchmarks (same month of 2022: **1.71**; same month of 2024: **0.89**); the blind forecast frozen 5 November 2026 (Oct **17.3**, Nov **16.9**, Dec **16.7**) scored only when NBS releases arrive and never refit first (`engine/firms/results/blind_forecast_2026_11.md`); the Atlas engine's protocol recorded before the search (`engine/tune_protocol.json`) and enforced by `engine/test_validation.py` (test rows cannot select parameters; unverified rows are diagnostic only); the rule that a fact moves from test to calibration only with a dated register entry. Also report the honest limitation: the "strict" China tests were run after the test-period errors had been seen, so they are not blind; only the Oct–Dec 2026 forecast is.

### 6. Case 1: China, the honest failure (~1,300–1,500 words)

**Central claim:** The China graduate-labour model is the paper's best evidence for the method because it is a well-specified failure: an explanatory model that fits the historical record loses to a naive forecast under a declared protocol, and the loss is diagnostic rather than mysterious.

Content (all numbers from the 6 November 2026 refit, in the repo result files): whole-record fit **1.27 pts** (a fit statistic; `RUN_REPORT.md`, `docs/facts_register.md`); whole-record modelled rise **+5.18 pts** with Shapley shares sector **+3.84**, supply **+1.47**, composition **−0.10**, demand **−0.04** (`docs/china_fit.md`); fitted to 2018–22 only: **5.54** vs naive **1.61** (`RUN_REPORT.md`); strict Dec 2022: **5.54** vs **1.61**; Tilly strict **5.84 / 5.49** vs **1.61** (`docs/UPDATE_2026_11_05.md`); Dec 2024 same-definition: **1.71** vs **0.89**; spread-out entry: **0.77** vs **0.89**, winning **12 of 19** months (`engine/firms/results/seasonal_2024.md`); tournament winner under the strict protocol: **1.09** vs **0.89**, bias **−0.41**, postings **−89%** vs **−22%**, **2 of 16** parameters at bounds (`engine/firms/results/stories_strict.md`); required-demand inversion: the model needs graduate demand **6–15% below 2022** by 2025–26, contradicted by the adult labour market (`firms/results/demand_inversion.md`). The ablation shows no single culprit: mechanisms are individually large and offsetting; the 2018–24 path pins their sum, not each. Report the "what would change the verdict" list: profiling the flat valley with `mc.py`; an independent graduate-demand series; a participation/NEET margin; a better wage benchmark. The lesson for the field: a fit statistic is not a test, and a model that cannot be beaten by its own forecast should say so.

### 7. Case 2: Cambodia and the cross-country tests (~900–1,100 words)

**Central claim:** The method's second use is to separate claims the data support from claims only the calibration supports. In Cambodia the policy *directions* are robust across a calibration ridge while the *level* of child labour is not calibrated; in the cross-country model, two national patterns are reproduced and a third is a clean failure.

Content: Cambodia — 30-seed bands, schools-as-protection **−6.36 to −7.55 pts** across five calibrations, cash **−1.97 to −3.68**, factory-only ban **−0.40 to −1.01**, child labour stays **13.9–14.4%** against **10.7%** in the 2012 survey (`engine/results/camchild_ridge.md`); the partial-ban increase and Basu–Van hysteresis are not reproduced; the UIS-vs-census observation equation (17.6% vs ~8.4%) is a measurement-layer problem, not a modelling failure (`docs/cambodia_observation_equation.md`). Cross-country — four states; value of state D separates dropout-without-work at AUC **0.89**; India is a clean failure: **31% [8–68]** school-and-work predicted vs **0.4%** observed, and the model reaches India only in a corner at 3× tolerance; the first-round Kyrgyz "pass" is withdrawn after the source figure was found not to exist (`docs/asia_school_work.md`, `docs/CHANGES_evidence_lane_2026_11_05.md`). The relational-floor test: history does not discriminate between structures, but the *composition of exits* does — human capital predicts about **50%** of exits from the bottom 40%, the relational floor above **85%** (Philippines: **52% vs 94%**; Cambodia **65% vs 98%**) (`docs/relational_floor_test.md`, `docs/relational_floor_countries.md`). The lesson: report which observable would discriminate, even when the current data cannot.

### 8. Falsification conditions (~700–900 words)

**Central claim:** The programme is falsifiable at two levels: each model has stated failure conditions, and the method itself has conditions under which it should be abandoned. Both should be specified before the next evaluation, not after.

Content: a table with three columns — *claim*, *what would falsify it*, *where the test lives / would live*.

| Claim | What would falsify it | Where |
|---|---|---|
| Exact accounting improves inference rather than decorating it | Rival models with no ledger forecast or explain as well under the same protocol | comparative benchmark still to build |
| Docking identifies mechanisms | A docked model's added mechanism changes a target it was not supposed to touch; or the simpler model forecasts better | `engine/firms/test_firms.py`; seasonal vs base |
| Patterns jointly constrain structures | A structure fitted on one pattern generalises to the others no better than chance | floorworld eight-pattern test; childworld country tests |
| The relational floor is a real mechanism | In FIES/APIS household data, exits from the bottom 40% come out near the human-capital prediction (~50%) rather than >85% | the decisive test, not yet run (`docs/relational_floor_test.md` §Data) |
| Spread-out entry is the China seasonal mechanism | The blind Oct–Dec 2026 forecast loses; or an 11-month entry rule fails on independent entry-timing data | `firms.blind_forecast --score`, never refit first |
| The method is cumulative | Rival teams using the same protocol cannot reproduce the stored results from the public repo | `python run_all.py`; `RUN_REPORT.md` |
| The method is not just model-fitting | Under a pre-declared protocol, the models fail more often than they succeed — and the failures are informative | already true for China; report it |

Also state: a programme that only ever produces failures is not vindicated either; the paper's claim is that both outcomes must be reportable, not that failure is success. The weak point is that the method has not yet produced a decisive out-of-sample success; the blind forecast and the valley profile are the two chances.

### 9. Objections and replies (~700 words)

**Central claim:** The standard objections have specific answers, and the answers are themselves testable.

- *"ABMs are storytelling with dials."* Reply: only if they lack identities, docking, fixed pattern sets and held-out tests; the cocoon is the response, and the paper shows it being enforced.
- *"This is curve-fitting."* Reply: the facts register separates calibration from test; the China failure is the proof that the model is not fitted to the test.
- *"Simulation uncertainty is not empirical uncertainty."* Reply: agreed; the paper reports them separately and says what each cannot support.
- *"Why not just econometrics?"* Reply: identification and generative explanation answer different questions; the project uses reduced-form evidence as targets and constraints, and the two should be complementary, not rival.
- *"Why China and Cambodia?"* Reply: chosen for contrasting mechanisms (credential queue vs child-labour protection), not representativeness; the method is the claim, the cases are demonstrations.
- *"Does it scale?"* Reply: the Angkor challenge template (`worlds/angkor/01_MESSAGE_TO_ATLAS_AI.md`) is the proposed scaling path; it is not yet tested.
- *"Who reviews a model?"* Reply: reviewers run it; the repo's `run_all.py`, `RUN_REPORT.md` and verification note are the review protocol, and a benchmark platform should treat reproducibility as a submission requirement.

### 10. Conclusion: from models to a comparative benchmark platform (~500–600 words)

**Central claim:** The method scales only if models become public objects with model cards, declared struts, fixed protocols, stored results and scored blind forecasts — a benchmark platform for comparative education. The paper's contribution is the standard, not the Atlas specifically.

Content: the Angkor handoff's proposed common world contract (`worlds/angkor/02_ENGINEERING_HANDOFF.md`) and challenge template; what a submission would have to contain (model card, struts with provenance and ranges, intervention schema, observables, validation targets, run manifest with hashes and seeds); the two-track future (empirical models vs teaching toys, never confused); the invitation to rival teams. Close on the honest sentence: the programme's strongest result so far is a forecast that failed in public, and that is the standard the next paper will be held to.

---

## 4. Figures and tables plan

1. **Table 1** — the four insulations and what each rules out (with the repo test that enforces it).
2. **Table 2** — the four uncertainty layers (simulation / parameter / structural / measurement) and how each is reported.
3. **Figure 1** — China: observed vs strict-protocol forecast vs naive benchmark, Dec 2022 and Dec 2024 cutoffs on one pair of panels, with the test-period errors shown, not hidden.
4. **Table 3** — the falsification table from §8, including "not yet tested".
5. **Table 4** — the facts-register excerpt (calibration / test / diagnostic / input).
6. **Box 1** — what a "generative explanation" is and is not (Boudon + Epstein in plain language).
7. **Appendix A** — repository map and one-command reproduction; **Appendix B** — test inventory (92 Python unit tests, 30 Planning Lab tests, 26 Cambodia tests, 21 child-labour-simulator tests, round-8 stored and rerun, parity checks); **Appendix C** — data licences and attribution (from `LICENSES.md`).

---

## 5. What the paper must not claim

- Not that agent-based models are more credible than econometric estimates; not that a simulation band is a confidence interval.
- Not that the China model explains China; it fails its own forecast test.
- Not that the Cambodia model estimates policy effects; the protection magnitudes are placeholders and the level is not calibrated.
- Not that the relational floor is established; the decisive household-data test has not been run.
- Not that "the Atlas" is a validated platform; it is a collection of tested worlds with one ledger still missing.
- Not novelty against a literature that has not been read: the prior-work search is now done and its map is in `related/prior_work_annotated.md` (23 entries, five claimed gaps G1–G5, and what would refute each). Cite it before claiming a gap; until the gaps have been checked against the entries, position as "we formalise a standard implicit in several traditions", not "no one has done this".

---

## 6. Literature to cite (verified; links/DOIs where available)

**Ancestry and standard**
- Boudon, R. (1974). *Education, Opportunity, and Social Inequality: Changing Prospects in Western Society*. New York: Wiley. ISBN 978-0471091059.
- Epstein, J. M. (1999). "Agent-based computational models and generative social science." *Complexity* 4(5), 41–60. https://doi.org/10.1002/(SICI)1099-0526(199905/06)4:5<41::AID-CPLX9>3.0.CO;2-F
- Epstein, J. M. (2006). *Generative Social Science: Studies in Agent-Based Computational Modeling*. Princeton University Press. https://doi.org/10.1515/9781400842872
- Epstein, J. M. (2008). "Why Model?" *Journal of Artificial Societies and Social Simulation* 11(4), 12. https://www.jasss.org/11/4/12.html

**Method components**
- Godley, W. & Lavoie, M. (2007). *Monetary Economics: An Integrated Approach to Credit, Money, Income, Production and Wealth*. Basingstoke: Palgrave Macmillan.
- Axtell, R., Axelrod, R., Epstein, J. M. & Cohen, M. D. (1996). "Aligning simulation models: A case study and results." *Computational and Mathematical Organization Theory* 1(2), 123–141. https://doi.org/10.1007/BF01299065
- Grimm, V., Revilla, E., Berger, U., Jeltsch, F., Mooij, W. M., Railsback, S. F., Thulke, H.-H., Weiner, J., Wiegand, T. & DeAngelis, D. L. (2005). "Pattern-oriented modeling of agent-based complex systems: lessons from ecology." *Science* 310(5750), 987–991. https://doi.org/10.1126/science.1116681
- Craig, P. S., Goldstein, M., Rougier, J. C. & Seheult, A. H. (2001). "Bayesian forecasting for complex systems using computer simulators." *Journal of the American Statistical Association* 96(454), 717–729. https://doi.org/10.1198/016214501753168370

**Substantive literature the cases rest on**
- Tilly, C. (1998). *Durable Inequality*. Berkeley: University of California Press. And Tilly, C. (2005). *Identities, Boundaries, and Social Ties*. Boulder, CO: Paradigm Publishers.
- Dore, R. (1976). *The Diploma Disease: Education, Qualification and Development*. London: Allen & Unwin.
- Collins, R. (1979). *The Credential Society*. New York: Academic Press (reissued Columbia University Press, 2019, https://doi.org/10.7312/coll19234).
- Thurow, L. C. (1975). *Generating Inequality*. New York: Basic Books (Palgrave edition https://doi.org/10.1007/978-1-349-15723-5).
- Hirsch, F. (1976). *Social Limits to Growth*. Cambridge, MA: Harvard University Press. https://doi.org/10.4159/harvard.9780674497900
- Raftery, A. E. & Hout, M. (1993). "Maximally maintained inequality: expansion, reform, and opportunity in Irish education, 1921–75." *Sociology of Education* 66(1). https://doi.org/10.2307/2112784
- Todd, P. E. & Wolpin, K. I. (2006). "Assessing the impact of a school subsidy program in Mexico: using a social experiment to validate a dynamic behavioral model of child schooling and fertility." *American Economic Review* 96(5), 1384–1417. https://doi.org/10.1257/aer.96.5.1384
- Basu, K. & Van, P. H. (1998). "The economics of child labor." *American Economic Review* 88(3), 412–427.
- Nordtveit, B. H. (2010). "Schools as agencies of protection in Namibia and Swaziland: can they prevent dropout and child labor in the context of HIV/AIDS and poverty?" *Comparative Education Review* 54(2), 223–242. https://doi.org/10.1086/651261
- Nordtveit, B. H. (2016). *Schools as Protection? Reinventing Education in Contexts of Adversity*. Cham: Springer. https://doi.org/10.1007/978-3-319-25651-1
- Altinok, N., Angrist, N. & Patrinos, H. A. (2018). *Global Data Set on Education Quality (1965–2015)*. Policy Research Working Paper 8314, World Bank. https://doi.org/10.1596/1813-9450-8314
- Menefee, T. & Nordtveit, B. (2026). *Massification and Its Mechanisms: Credential Pipelines, Compression Technology, and the Formal Economy Threshold*. Working paper, revised October 2026; in this repository at `related/massification_project/paper/Massification_and_Its_Mechanisms.md`.

**Data/measurement sources** (cite at the country level in the cases, not in the methods argument): NBS monthly urban unemployment releases; MoE graduating-class and tertiary-entrant bulletins; UNESCO UIS out-of-school rates; Cambodia NIS 2019 census attendance and the 2012 Child Labour Survey; UNICEF Innocenti 2024 India child-labour/schooling report; ILO/UNICEF child-labour estimates. Exact links are in `engine/firms/data_china.py`, `docs/asia_school_work.md`, `docs/cambodia_observation_equation.md`, `docs/input_audit_supplied.md` and `docs/CHANGES_evidence_lane_2026_11_05.md`.

---

## 7. Open decisions before drafting

1. **Co-authorship.** Is this paper Trey alone, or Trey + Bjørn (the massification paper is joint; the methods paper overlaps it)? Decide before the ancestry sections, because Boudon→Epstein→cocoon is the shared argument.
2. **Journal order.** IJED first for reach, CER first for the discipline. This changes the introduction's first 500 words, nothing else.
3. **Prior-work search (TODO A7).** Done 6 November 2026: `related/prior_work_annotated.md` (23 entries, gaps G1–G5, refutation conditions). Read it before drafting the introduction; the novelty claim must be stated against those entries, not against the empty set.
4. **The decisive test.** The paper is much stronger with one out-of-sample success. Candidates: the blind Oct–Dec 2026 China forecast; the valley profile on the tournament winner; the FIES/APIS test of exit composition. At least one should be reported, pass or fail.
5. **Anonymised data/participant material.** None used; the paper can say so in the data-availability statement.
