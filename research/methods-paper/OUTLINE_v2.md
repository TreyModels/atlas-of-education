# Methods paper outline, v2

14 November 2026. Replaces `docs/engine/methods_paper_outline.md` (v1, 6 November 2026) as the working outline; v1 is untouched. This is an outline for Trey to cut, not prose for the paper. Supporting files in this folder: `REFERENCES_VERIFIED.md` (every citation checked, with status) and `NOVELTY.md` (what is and is not new).

Working title (proposal; v1's title can stay if preferred): **"Explaining education systems with executable models: a testing protocol for comparative education, after analytical sociology"**.

---

## What changed from v1 and why

1. **Ancestry rebuilt.** v1 ran Boudon, then Epstein, as if the generative argument had no sociological successor. Analytical sociology (Hedström; Manzo) has argued it for twenty years and has built executable Boudon-type and educational-choice models (Manzo 2011, 2013). v2 adds a section on that lineage and repositions the contribution as a translation and testing-practice paper for comparative and international education, not a recovery of Boudon. Basis: `NOVELTY.md` §1, §3.
2. **Empirical spine corrected.** v1 called the China forecast a "clean negative result" and "a forecast that failed in public". The strict China tests were run after the test-period errors had been seen, so they are not blind (`engine/firms/results/seasonal_2024.md` item 4; `stories_strict.md` item 5). v2 says so plainly. The only blind test is the frozen Oct-Dec 2026 forecast, not yet scored.
3. **Seasonal numbers corrected.** In `seasonal_2024.md` the variant selected on training fit (spread8) has test error 0.99 against naive 0.89 and loses, although item 1 of that file's prose says it beats naive. The variant v1 cited (spread11, 0.77, 12 of 19 months, paired t -0.77) was not the pre-selected one and is not distinguishable from naive. v2 uses these figures and flags the prose error.
4. **Core demonstration changed.** v2 makes three things the core: the frozen forecast ledger (rolling-origin small models plus forecasts frozen before the data arrive), the recovery/identification tests (can the data tell rival explanations apart?), and the facts-register and audit record of what the method caught in the repo's own models. The old China model becomes a documented, non-blind negative case. Results from `research/` are marked "to be inserted"; no numbers from them are in this outline.
5. **Numbers updated for the 14 Nov 2026 review** (`REVIEW_STATUS.md`). Part 5 of this file lists each number, its v1 and v2 values, the repo file it comes from, and which could not be traced. The relational-floor "85% against 50%" discriminator is withdrawn; the "+22.8 pp no waiting" figure is replaced by +12.2.
6. **Docking demoted from identification to verification.** The shadow-education review found that the three rival explanations share one `model.py`, so their policy agreement is not independent evidence. Docking shows implementation consistency; recovery tests are what bear on identification.
7. **"History matching" claim narrowed.** The repo uses ABC-style tolerance matching, not emulator-based history matching.
8. **"What the paper must not claim" extended** (Part 7), including the claims v1 would have drawn reviewers' objections for.
9. **Journal note** rewritten with trade-offs and adding JASSS and *Sociological Methods & Research* (Part 6).

---

## Part 1. Central claim and secondary claims

**Central claim (one sentence).** Rival explanations of education-system patterns can be made more testable if each is written as an executable mechanism model, checked against a simpler predecessor, tested for whether the available data could tell it apart from its rivals before it is used to adjudicate between them, and scored under an information set fixed before the outcome is seen, with failures recorded in a public ledger.

**Secondary claims** (each should survive a reviewer who knows Hedström and Manzo):
1. The generative programme is not new to sociology; analytical sociology has already built executable Boudon-type and educational-choice models. The paper brings the programme and its validation tools into comparative and international education, whose recurring rival-explanation disputes (credential expansion, shadow education, school-to-work) are of the same kind.
2. The added contribution is a set of auditable practices: a facts register separating calibration from test numbers, docking as routine verification, recovery tests, and a frozen forecast ledger that records losses.
3. The practices are shown on the repo's models, including what they caught: errors in the models' own earlier verdicts.
4. The paper is a practice-and-protocol paper. It does not claim a validated model of any education system.

---

## Part 2. Section plan

Word targets are ours, not journal rules. Part 6 explains why journal limits are not quoted.

| Section | Content | Approx. words (ours) |
|---|---|---:|
| Abstract, keywords | | 200 |
| 1. Introduction: rival explanations that never get separated | the problem in comparative education | 1,000 |
| 2. Lineage: Boudon, analytical sociology, Epstein | new section; see below | 1,400 |
| 3. What is added: a protocol for education models | positioning against section 2 | 800 |
| 4. The practices and their limits | facts register, docking, patterns, ABC, accounting | 1,500 |
| 5. The protocol: information sets, blind versus non-blind | the taxonomy of tests | 1,000 |
| 6. Demonstration A: the China forecast ledger | ledger plus the old model's non-blind record | 1,500 |
| 7. Demonstration B: can the data tell explanations apart? | shadow education; credential floor | 1,600 |
| 8. Short case: Cambodia and the measurement layer | | 700 |
| 9. Falsification conditions | | 600 |
| 10. Objections and replies | | 700 |
| 11. Conclusion | | 500 |
| Tables/figures | | 400 |

(Total about 12,000 as listed, which is long for most of the journals in Part 6; cutting options are: shorten paper §4 to a table, fold §8 into §7, or move the Cambodia case to an appendix. Decide after the target journal is chosen.)

---

## Part 3. Section-by-section

### 1. Introduction: rival explanations that never get separated

**Claim:** Comparative education's explanatory disputes recur because rival explanations are verbal; the same evidence can be narrated by several of them, and a failed forecast is rarely scored. A written, executable specification plus a test the model did not see makes disagreement more specific.
Content: the credential-expansion puzzle (expansion that does not equalise opportunity; v1 cites the book's chapter 1, `TODO §R`, not traced); three symptoms (untestable rivalries, post-hoc mechanism lists, unscored forecasts); the paper's scope: practice, not a new theory of education; cite the author's 2012 conference paper on complex adaptive systems in comparative education and say what is different now (executable models, protocol, forecast ledger). Do not open with "no one has done this".

### 2. Lineage: Boudon, analytical sociology, Epstein (new section)

**Claim:** The programme of explaining a social pattern by specifying and running the mechanism that generates it has a sociological lineage that educational research should recognise: Boudon (1974) on educational opportunity; Breen and Goldthorpe (1997) on a formal rational-action model of educational differentials; Hedström and Swedberg (1998), Hedström (2005), Hedström and Ylikoski (2010) and Hedström and Bearman (2009) on mechanism-based explanation and analytical sociology; Manzo on executable versions; Epstein (1999, 2006, 2008) from complexity science.
Content, in order:
- **Boudon (1974):** primary and secondary effects and the positional-value argument, as the field's generative question. Check the attributions against the book before drafting (`REFERENCES_VERIFIED.md` §C). Note Boudon's own "generating models" writing (1979, unchecked).
- **Breen and Goldthorpe (1997):** the formal rational-action model: families weigh costs, benefits and perceived chances; class differences arise from resources and constraints. A mathematical model, not a simulation.
- **Analytical sociology:** the mechanism-based explanation argument (Hedström 2005 ch. 2; Hedström and Ylikoski 2010) and its endorsement of simulation of interacting agents; Hedström and Manzo (2015) as the programme statement for ABM; Keuschnigg, Lovsjö and Hedström on the relation to computational social science (contents unread).
- **Manzo:** (2013) an agent-based model of educational choice with peer influence, built on Breen and Goldthorpe and tested against French survey data; (2011) an agent-based treatment of Boudon's relative-deprivation model (not about schooling); (2009) multi-agent simulation of school choice in France and Italy; (2022) on agent-based models and causal inference. State what each does in one sentence each (paraphrase from `REFERENCES_VERIFIED.md` §A5).
- **Other education ABMs:** Maroulis et al. (2010, 2014, 2016) on complex-systems and school-choice models; Salgado et al. (2014) setting an ABM beside a multilevel model; Reardon et al. (2016); Leoni (2021).
- **Epstein:** the generative criterion and "Why model?" (explanation is not prediction).
Say plainly: v1 treated Epstein as the epistemology and added "an empirical-credibility test Epstein does not require". The analytical-sociology work already treats empirical confrontation as part of the programme (Manzo 2013 compares simulations to survey data). The paper's addition is narrower; see section 3.

### 3. What is added: a protocol for education models

**Claim:** Given section 2, the defensible contribution is (a) taking the programme into comparative and international education and testing it on cross-national cases; (b) a set of practices that make a model's claims auditable; (c) a record of failures, including the paper's own.
Content: a table with three columns: practice, where it comes from (cite the origin), what the paper adds. Entries: facts register (no direct origin found; claim as practice); docking (Axtell et al. 1996); exact accounting (Godley and Lavoie 2007); pattern-oriented modelling (Grimm et al. 2005); ABC calibration (Beaumont et al. 2002; Thiele et al. 2014); history matching (Craig et al. 2001; Andrianakis et al. 2015; used here only if implemented); frozen-information forecast ledger (standard forecasting practice; novelty only in application); recovery test (see section 7). State which of these are new in education and which are not new at all.

### 4. The practices and their limits

Keep each subsection short; Table 1 can carry most of it.

**4.1 Exact accounting.** Identities as part of a model that cannot be disputed; a violation is a bug. Repo evidence: stock-balance residual 1.42e-14 and free-entry residual 8.88e-16 (`docs/engine/china_fit.md`, line 58). Other v1 evidence (planning-kernel 1,000 random cases, camchild identity, reconstructed-cohort closure under 1e-9) could not be traced: `planning/test_kernel.cjs` and `tests/test_camchild.cjs` are not in this checkout, `engine/tests.py` is. Do not cite them until located.

**4.2 Docking: verification, not identification.** The new model reproduces its predecessor as a special case (`engine/firms/test_firms.py`: seasonal nests base to 1e-9, per v1; recheck). Add the lesson from `experiments/shadow-abm/README.md`: three explanations sharing one `model.py` (only 6 of about 215 lines differ) agree on policy because they share code; that agreement is not independent evidence. Docking must be paired with recovery tests.

**4.3 Pattern-oriented modelling.** Several weak patterns jointly constrain structures; the pattern set must be fixed before fitting. v1's floorworld eight-pattern result (S2 14.7%, S1 10.3%, S5 0.7% of 6,000 draws) is in `docs/engine/education_and_formalization.md`; it is not in the 14 Nov review's list and was not rechecked here, and the credential-floor review found that a hard liquidity threshold can make a verdict an artefact of the model form. Treat it as unreviewed and say so, or drop it.

**4.4 Calibration and what it can claim.** ABC-style tolerance matching (`engine/mc.py`, `childworld_mc.py`); cite Beaumont et al. and Thiele et al. Do not call it history matching unless emulator-based implausibility is implemented. Report what the not-ruled-out set cannot say. The shadow-education numbers (Part 5, row 13) show how thin that set can be.

**4.5 The facts register** (`docs/engine/facts_register.md`). Labels: calibration / test / diagnostic / input / blind test. Add a label that v1 lacked: **"test, not blind"** versus **"blind"**. In the current register the Jan 2025-Sep 2026 rows are labelled "Test" and carry the note that test-period errors had been seen; the register's own heading should distinguish them. Show the register catching real problems (paper §6, §7 and Part 5).

**4.6 Uncertainty in four layers** (simulation / parameter / structural / measurement), as v1; evidence `engine/mc.py`, `engine/test_mc.py`, `engine/results/childworld_sobol.md`. Add the `experiments/camchild-seeds` result as an example of "seed spread as the yardstick": five of 13 single-lever settings move the national child-labour rate by less than the reference seed spread (0.46 pp).

### 5. The protocol: information sets, and which tests were blind

**Claim:** A test counts as evidence of the kind readers assume only if the information set is fixed at a date, the benchmark is a naive rule on the same information, the scoring rule is written before the outcome is seen, the code is leak-tested, and the choice of model was made before the test months were seen. Tests that fail the last condition are reported as pseudo out-of-sample.

**Table 2: every China test, labelled.** (This table is the honest core of v1's section 5.)

| Test | Fitted to | Scored on | Blind? | Result | Source |
|---|---|---|---|---|---|
| Early-fit strict, Dec 2022 cutoff | old-method 2018-22 | 2023 H1 old method; new-method Dec 2023-Sep 2026 (32 months) | **No.** Run after the test-period errors had been seen (v1 §5 states this for the strict China tests) | 5.54 against naive 1.61 | `docs/engine/UPDATE_2026_11_05.md` line 19; `experiments/youth-review/README.md` §1.7 |
| Tilly strict | same | same | No | 5.84 (unemployment only), 5.49 or 5.57 (with wages; files disagree, see Part 5, row 5) against 1.61 | `engine/firms/results/tilly_strict.md`; `UPDATE_2026_11_05.md` line 21 |
| Dec 2024 base model | data to Dec 2024 | Jan 2025-Sep 2026 (19 months) | No: the test months were already published when the test was run | 1.71 against naive 0.89 | `engine/firms/results/forecast_2024.md` |
| Dec 2024 seasonal variants (five) | same | same | No: the candidate mechanisms came from `forecast_2024.md`, which had shown test-period seasonal errors | see Table 3 | `seasonal_2024.md` item 4 |
| Tournament winner (16 parameters), Dec 2024 cutoff | same | same | No: mechanism set and 11-month spread chosen after test months seen | 1.09 against 0.89; 8 of 19 months won; t +0.89 | `engine/firms/results/stories_strict.md` |
| **Frozen forecast, 5 Nov 2026** | data to Dec 2024; model spread11 | Oct, Nov, Dec 2026 | **Yes for the outcome months**, but the model choice (spread11) was made after seeing data to Sep 2026; the forecast does not test that choice | model 17.3, 16.9, 16.7; naive 17.1, 16.1, 15.7; scoring pending | `engine/firms/results/blind_forecast_2026_11.md` |
| **Rolling-origin ledger of small models** | data to each origin | later months, horizons 1, 3, 6, 12 | Partly: rule fixed before results; the origins span months already observed, so the retrospective rows are not blind; only ledger entries frozen before release are | **to be inserted** from `research/china-forecast-ledger/` | |

**Table 3: the Dec 2024 seasonal variants (`engine/firms/results/seasonal_2024.md`).** Report all five, in the order of the file, with the selection rule stated.

| Variant | Fit new 2024 (selection criterion) | Test MAE | Months beating naive | Mean difference to naive | Paired t |
|---|---:|---:|---:|---:|---:|
| base | 0.91 | 1.71 | 5/19 | +0.81 | +4.72 |
| duration | 0.80 | 1.19 | 7/19 | +0.30 | +1.69 |
| **spread8 (selected on training fit)** | 0.62 | 0.99 | 7/19 | +0.10 | +0.66 |
| spread11 | 0.65 | 0.77 | 12/19 | -0.12 | -0.77 |
| duration + spread11 | 0.67 | 0.71 | 11/19 | -0.19 | -1.14 |
| Naive, same month of 2024 | | 0.89 | | | |

Text for the paper: the variant chosen by the declared rule loses to naive (0.99 against 0.89); two later-looking variants have lower test error than naive but neither difference is distinguishable from zero (19 monthly errors, which are serially correlated, so the paired t is optimistic); and none of this is blind. `seasonal_2024.md` item 1 says spread8 is "the first China specification ... to beat the naive benchmark"; that sentence is wrong by the file's own table, and item 2's "0.62-0.70" are training-fit numbers, not test numbers. These should be corrected in the source file by the owner (I did not edit it).

### 6. Demonstration A: the China forecast ledger

**Claim:** The honest China story is a layered one: the original model's pseudo out-of-sample record (a documented, non-blind loss), a simpler rival (the lake null), and a ledger of small models whose forecasts are frozen before data arrive.
Content:
- **The old model's record (non-blind).** Fit statistics (in sample): whole-record MAE 1.86 on disk, 1.76 after widened bounds; 1.27 is the in-sample "new MAE", which `facts_register.md` line 24 and line 75 call the "whole-record error" (the files disagree; see Part 5, row 1). Modelled rise +5.18 on disk, +5.06 widened. Strict early fit 5.54 against naive 1.61 (32 months). Tournament winner 1.09 against 0.89 with bias -0.41; graduate postings -89% modelled against -22% observed; 2 of 16 parameters at bounds; 6 starts only (`stories_strict.md`). The ablation shows large offsetting mechanisms: the 2018-24 path pins their sum, not each (`stories_strict.md` item 3b). Required-demand inversion: the model needs graduate demand 6-15% below 2022 by 2025-26 (`engine/firms/results/demand_inversion.md`; v1 figure, rechecked only for the file's existence).
- **What the review changed.** The Aug-2021 step carries most of the rise and is unexplained (Shapley relabelled; `experiments/youth-review/README.md` §1.1, §1.6); a data-sized step fits worse in sample and does not reproduce the observed postings fall; `lam_g` is weakly identified; a four-parameter lake null beats the 11-parameter model on the verified new-method months (2.88 against 5.54) and both lose to naive (1.61) (`youth-review` §1.8). Status: "fitted + free residual" (`REVIEW_STATUS.md`).
- **The ledger.** Rival small models (zero to four estimated numbers) against `naive_same_month`, rolling origins, horizons 1, 3, 6, 12, a public CSV of frozen forecasts. **Results to be inserted** from `research/china-forecast-ledger/`. State in the text what the rule was and that it was fixed before results; state the number of origin-target pairs beside every number; do not report a comparison without its n.
- **The frozen forecast.** The 5 Nov 2026 forecast: how it was frozen (data to Dec 2024; spread11), the scoring rule (`python -m firms.blind_forecast --score`, no refit first), and that it will be scored when releases arrive. If scored before submission, insert the result, pass or fail.
- **Lesson stated carefully.** A fit statistic is not a test; a model that loses a pseudo out-of-sample test to a naive rule should say so; the ledger is the mechanism that would have made that loss visible earlier.

### 7. Demonstration B: can the data tell rival explanations apart?

**Claim:** Before a model is used to adjudicate between explanations, the paper asks whether data of the kind available could distinguish the explanations at all (a recovery or identification test). Two cases.

**7.1 Shadow education: three explanations of tutoring.** Existing state (`experiments/shadow-abm/README.md`, 14 Nov 2026): after recalibration, the pair fit rate on 20 fresh worlds per particle is 37-44% (old posteriors on the same seeds 17-19%); only 1-7% of particles fit at least 70% of fresh worlds (old 0-1%); favour-variant importance ESS 121 of 200; at tolerance 1, 0-4% of proposals fit; evidence ratios at tolerance 1 rest on a handful of fitting proposals (thin 2.5e-7, full 7.9e-9, favour 2.1e-8, diversion 0). Policy agreement across variants comes from shared code (6 of about 215 lines differ) and is not independent evidence. Status: "illustrative". **Recovery test results to be inserted** from `research/shadow-education/` (does simulated data from one explanation get identified correctly? which observables separate them?). Do not draw a conclusion about tutoring in the paper from the ABM.

**7.2 Credential floor: four structures including Breen-Goldthorpe.** Existing state (`public/reference/credential-floor.md`, v2.1, 14 Nov 2026): the earlier rejection of the relational floor came from a hard liquidity threshold, which makes a completion cliff by wealth that fits no quintile profile; with a graded constraint all three structures (human capital, positional, relational) fit Cambodia's and Vietnam's full quintile profiles, and the relational-weight posterior equals its prior (Cambodia 0.38 [0.04, 0.75]; Vietnam 0.36 [0.03, 0.75]); the profile-fitted structures predict 57-58% of Cambodian non-completers from the bottom 40%, inside the observed 55-64%. Projections to 2035 change sign with the form of the constraint and must not be quoted. China is explained by no structure (every structure predicts a 3-11% rise in college entry against registrants falling 5.3% per birth). Status: "illustrative". **Four-structure test with Breen-Goldthorpe: results to be inserted** from `research/credential-floor/`. Lesson, stated as a lesson about method: a verdict that looks like evidence about a mechanism can come from a modelling choice (the liquidity form); the recovery test and the robustness variant are what exposed it. The v1 discriminator (human capital predicts about 50% of exits from the bottom 40%, relational above 85%) is withdrawn: under the graded constraint the structures give similar predictions once each fits the wealth profile (`credential-floor.md`, "Reading" items 1-2).

### 8. Short case: Cambodia and the measurement layer (can be an appendix)

**Claim:** the method separates what the data support from what only a calibration supports.
Content: 30-seed bands; schools-as-protection effect -6.36 to -7.55 pts across five calibrations; child labour stays 13.9-14.4% against 10.7% in the 2012 survey (`engine/results/camchild_ridge.md`); the level is not calibrated and the cost index is illustrative with a known defect (`cst()` charges every child in a region, `REVIEW_STATUS.md` problem 6); five of 13 single-lever settings move the national rate by less than seed spread, and closing the Thai route leaves the national rate unchanged while teen work away from home falls by 10.0 pp (`experiments/camchild-seeds/README.md`); the UIS-versus-census observation equation is a measurement-layer problem (`docs/engine/cambodia_observation_equation.md`). Do not mix numbers from `camchild_ridge.md` and `camchild-seeds`: they use different scenario definitions (see Part 5, row 14). Status: "calibrated (out-of-school rates) + illustrative costs".

### 9. Falsification conditions

Table: claim, what would falsify it, where the test lives.

| Claim | What would falsify it | Where |
|---|---|---|
| The ledger practice reveals model losses earlier than ad hoc evaluation | Ledger forecasts frozen before release do not differ in verdict from the retrospective rows | `research/china-forecast-ledger/` (to be inserted) |
| Small, explainable models can be scored against naive on the China series | Naive wins at all horizons with large n (likely outcome per the interim README; do not pre-judge in the text) | same |
| Recovery tests are informative | The recovery test passes for variants that later prove indistinguishable on real data, or fails for variants that real data separate | `research/shadow-education/`, `research/credential-floor/` (to be inserted) |
| Docking catches implementation errors | An implementation error is found in a docked model that docking should have caught | `engine/firms/test_firms.py` |
| The facts register prevents fit statistics being reported as evidence | The register's labels are found misapplied in published numbers | `docs/engine/facts_register.md` |
| Spread-out entry is the China seasonal mechanism | The frozen Oct-Dec 2026 forecast loses to naive; or independent entry-timing data contradict an 11-month spread | `engine/firms/blind_forecast.py --score` |
| Method is reproducible | An outside team cannot reproduce the stored results from the repo | `scripts/check-all.sh` (14 Nov review) |

State the weak point: the method has not yet produced a decisive blind success; the scored frozen forecast and the ledger are the first chances, and a loss there is a result to report, not a reason to redraft.

### 10. Objections and replies

Keep v1's list (storytelling with dials; curve-fitting; simulation versus empirical uncertainty; why not econometrics; why these cases; scaling; who reviews), updating where numbers changed, and add:
- **"This is analytical sociology."** Reply: the generative argument and the use of simulation are; the paper says so in section 2. What it adds is described in section 3.
- **"Manzo already built an educational-choice ABM."** Reply: yes, and the paper builds on that line; it differs in testing practice and in its cross-national comparative cases.
- **"A negative result with a non-blind test is not evidence."** Reply: agreed; Table 2 labels each test and the paper's argument does not rest on the non-blind ones.
- **"Your three explanations share code."** Reply: agreed; policy agreement is not claimed as evidence; the recovery test is the response.
- **"ABMs lack empirical credibility."** Reply: cite Fagiolo et al. (2007, 2019) and Bruch and Atwell (2015) and state which of their recommendations the paper follows and which it does not.

### 11. Conclusion

From models to a record of what was tested. Close on the claim the evidence can carry: a collection of small, public, tested models and a ledger that scores their forecasts, including their failures. v1's closing sentence ("a forecast that failed in public") is withdrawn.

---

## Part 4. Figures and tables

1. Table 1: practices, origins, additions (section 3).
2. Table 2: every China test with blind/not-blind label (section 5).
3. Table 3: the Dec 2024 variants (section 5).
4. Figure 1: China, observed against model forecasts and the naive benchmark, the non-blind tests clearly labelled as such; ledger panel to be inserted.
5. Table 4: recovery-test results, shadow education and credential floor (to be inserted).
6. Table 5: falsification conditions (section 9).
7. Table 6: facts-register excerpt.
8. Appendix A: repo map; Appendix B: test inventory (only what can be located; see Part 5, row 15); Appendix C: data licences (`LICENSES.md` per v1, not located in this checkout; check).

---

## Part 5. Number-by-number update table (what the 14 Nov review superseded)

Paths are relative to the repository root. "Not traced" means I could not find the number in a file in this checkout.

| # | Quantity | v1 value | v2 value | Source file(s) | Notes |
|---|---|---|---|---|---|
| 1 | China fit, "whole-record" | 1.27 pts | Do not headline. 1.27 is the in-sample "new MAE" for the on-disk full fit; whole-record MAE is 1.86 (on disk) and 1.76 (widened bounds). | `experiments/youth-review/README.md` §1.2 table; `docs/engine/facts_register.md` lines 24, 75 | Files disagree on what 1.27 is: the facts register calls it the whole-record error, the review table lists it under "New MAE". `RUN_REPORT.md` (cited by v1) is not in this checkout. Either way it is a fit statistic. |
| 2 | Modelled rise | +5.18 | +5.18 on disk, +5.06 widened; "about +5 pp survives refits" | `youth-review` §1.2; `REVIEW_STATUS.md` | |
| 3 | Shapley shares of the rise | sector +3.84, supply +1.47, composition -0.10, demand -0.04 (of +5.18) | Same on disk, but "sector" is now "Aug-2021 step (unexplained)". Widened: step +3.33, supply +1.91, composition -0.18, demand 0.00 (of +5.06). | `youth-review` §1.1, §1.6; `docs/engine/china_fit.md` | Shares hold other parameters fixed. With the step at data size (0.02-0.07) the rise stays about +5, so the rise is not identified as step-driven. |
| 4 | Early-fit strict (fit 2018-22) | 5.54 against naive 1.61 | Same; n = 32 verified months. The site export gives 5.50 against 1.71 with n = 24 (stale). | `docs/engine/UPDATE_2026_11_05.md` line 19; `youth-review` §1.7 | v1 §5 quotes naive 1.71 for "same month of 2022" and §6 quotes 1.61; 1.71 is the pre-input-fix value. Use 1.61. |
| 5 | Tilly strict | 5.84 / 5.49 against 1.61 | 5.84 (unemployment only); with wages 5.49 (`tilly_strict.md`) or 5.57 (`UPDATE_2026_11_05.md` line 21). | `engine/firms/results/tilly_strict.md`; `docs/engine/UPDATE_2026_11_05.md` | Files disagree (5.49 against 5.57). Check which is current; do not quote either until resolved. |
| 6 | "+22.8 pp no waiting" | cited in `facts_register` (v1 does not use it) | +12.2 pp measured-rate counterfactual; with waiting +5.1; broad measure +9.5; the counterfactual also changes flows, so it is not pure accounting | `youth-review` §1.4; `docs/engine/facts_register.md` line 41 | The +22.8 is not reproduced. |
| 7 | Dec 2024 base model | 1.71 against naive 0.89 | Same | `forecast_2024.md`; `seasonal_2024.md` | |
| 8 | Spread-out entry | "0.77 against 0.89, winning 12 of 19 months" | See Table 3: the selected variant (spread8) is 0.99, loses; spread11 0.77 (12/19; t -0.77) not pre-selected; none distinguishable from naive; not blind | `seasonal_2024.md` | Prose of `seasonal_2024.md` items 1-2 contradicts its own tables. |
| 9 | Tournament winner | 1.09 against 0.89; bias -0.41; postings -89% against -22%; 2 of 16 at bounds | Same, plus: 8 of 19 months won, t +0.89; 6 starts only; mechanism set chosen after the test months were seen | `stories_strict.md` | |
| 10 | Lake null | not in v1 | Four-parameter lake null 2.88 on verified months; categorical early fit 5.54; naive 1.61; whole-record MAE 2.88 | `youth-review` §1.8 | The categorical model is not shown to beat a plain null out of sample. |
| 11 | Relational-floor discriminator | human capital about 50% of exits from the bottom 40%, relational above 85%; Philippines 52% against 94%; Cambodia 65% against 98% | Withdrawn. Hard-threshold model: Cambodia relational 85% [69, 97] against observed 55-64%, but that model fits no quintile profile. Graded constraint: relational 67% [57, 80]; profile-fitted 58% [54, 61]; all structures fit the profile; weights equal priors. | `public/reference/credential-floor.md` v2.1; v1 sources `docs/engine/relational_floor_test.md`, `docs/engine/relational_floor_countries.md` | The two `docs/engine/` files still carry v1 numbers (52/94; 65/98) and disagree with `public/reference/credential-floor.md`. The Philippines case was not re-run under the graded constraint in any file I read. |
| 12 | Credential-floor projections | "persists, not intensifies" | Not to be quoted: the Q3+ completion response to a 40% premium fall changes sign with the constraint (relational ~0 hard, +10 graded; human capital -12 hard, -6 graded). | `credential-floor.md` "Reading" item 3 | |
| 13 | Shadow education | not in v1's text | Fresh-world pair fit 37-44% (old 17-19%); 1-7% of particles fit 70% of fresh worlds; ESS 121/200; tolerance-1 acceptance 0-4%; policy agreement from shared code (6 of about 215 lines); median withholding 0%, above 1% in 21% of diversion worlds. Status "illustrative". | `experiments/shadow-abm/README.md` | The task brief said the shadow-education verdict is superseded; v1 does not state one, so there is no v1 number to replace. |
| 14 | Cambodia | schools-as-protection -6.36 to -7.55 pts; cash -1.97 to -3.68; ban -0.40 to -1.01; level 13.9-14.4% against 10.7% | Level and ridge numbers unchanged (`camchild_ridge.md`). New: seed-spread study (50 seeds) with different scenario definitions: cash -4.82 pp at half-max; protection -2.20; ban -0.32; five of 13 levers within seed spread (0.46 pp). Status "calibrated (out-of-school rates) + illustrative costs". | `engine/results/camchild_ridge.md`; `experiments/camchild-seeds/README.md`; `REVIEW_STATUS.md` | Different scenario definitions between the two files; do not set their numbers side by side without stating the definitions. Cost index not usable (`cst()` defect). |
| 15 | Accounting and test inventory | 1.42e-14, 8.88e-16; 1,000 planning-kernel cases; camchild identity; 1e-9 closure; 92 / 30 / 26 / 21 tests; parity 1.29e-7, 0.0e+00 | Residuals 1.42e-14 and 8.88e-16 confirmed (`docs/engine/china_fit.md` line 58). The test counts, the parity figures and four test files (`planning/test_kernel.cjs`, `tests/test_camchild.cjs`, `tests/js_parity.mjs`, `tests/camchild_parity.py`) are not in this checkout. | | Not traced; recheck before using. `engine/tests.py`, `test_mc.py`, `test_validation.py`, `engine/firms/test_firms.py` exist. |
| 16 | Floorworld eight patterns | S2 14.7%, S1 10.3%, S5 0.7% | Unchanged in `docs/engine/education_and_formalization.md`; not covered by the review | | Unreviewed; see paper §4.3. |
| 17 | Blind forecast | Oct 17.3, Nov 16.9, Dec 16.7; naive 17.1, 16.1, 15.7 | Same (v1 gave only the model); scoring pending | `engine/firms/results/blind_forecast_2026_11.md` | |
| 18 | India school-and-work | 31% [8-68] against 0.4% observed; passes only at 3x tolerance | Not rechecked in this pass | `docs/engine/asia_school_work.md` lines 76-77 | |
| 19 | Required demand inversion | 6-15% below 2022 by 2025-26 | Not rechecked beyond file existence | `engine/firms/results/demand_inversion.md` | |
| 20 | Prior-work map | 23 entries, gaps G1-G5 | Not traced | `related/prior_work_annotated.md` absent from this checkout | |
| 21 | Massification paper | cited | Not traced | `related/massification_project/...` absent | |

---

## Part 6. Target-journal note

I did not verify word limits, scope statements or review times and quote none. Check each journal's current author guidelines before choosing. The trade-offs below are my judgment, not verified facts about the journals.

| Journal | Case for | Case against |
|---|---|---|
| ***Comparative Education Review*** | The field's disciplinary venue (v1 notes it is the Comparative and International Education Society's journal); a paper about how comparative education tests explanations belongs here; Nordtveit (2010) appeared in it. | A protocol-and-ledger paper with results still to come may read as a project report; a methods paper from outside the usual qualitative-historical or econometric mix may meet hostile reviewers; the scored ledger entries need to be in before it is persuasive. |
| ***Comparative Education*** | Receptive to theory-of-comparison arguments; the lineage section (Boudon, Breen and Goldthorpe, analytical sociology) is at home here. | Less likely to value a forecast table; the negative-result framing needs rewriting as an argument about evidence. |
| ***International Journal of Educational Development*** | Applied cases (China graduate labour market, Cambodia child labour) and planners; likely more tolerant of country detail. | Methods novelty may be read as technical; the lineage section must be short. |
| ***Compare*** | Broad comparative and international readership. | Not examined; fit unknown. Look at recent method papers before deciding. |
| ***JASSS*** | Where several of the ABM precedents (Maroulis, Salgado, Reardon, Epstein 2008) appeared; reviewers will know validation, ODD and docking; reproducibility norms fit the repo; simulation reviewers will evaluate the protocol on its merits. | Readers are modellers, not comparativists, so the "bring it to comparative education" claim carries less weight there; the contribution would be judged as a validation-practice paper and compared with Fagiolo et al. and Bruch and Atwell, who have more empirical depth. |
| ***Sociological Methods & Research*** | Published the Hedström and Manzo special issue and Bruch and Atwell; the right audience for "tests for ABMs of educational inequality"; strong on ABM credibility. | Wants methodological advance and an empirical demonstration that is not a non-blind loss; the education-field framing counts for little; likely to ask for a formal treatment of the test protocol. |

Recommendation: (1) If the paper can include at least one blind or recovery result by submission, and the aim is the comparative-education readership, *Comparative Education Review* with the section 2-3 framing is the natural first choice, as v1 judged. (2) If the ledger and recovery results are thin, a shorter JASSS or SMR version centred on sections 4, 5, 7 may be easier to defend, since those readers can assess the protocol directly. (3) Whichever is chosen, the first 500 words differ; the evidence and Table 2 should not.

---

## Part 7. What the paper must not claim (v1 list kept and extended)

From v1, unchanged:
- That agent-based models are more credible than econometric estimates; that a simulation band is a confidence interval.
- That the China model explains China.
- That the Cambodia model estimates policy effects; the protection magnitudes are placeholders and the level is not calibrated.
- That "the Atlas" is a validated platform.
- Novelty against a literature that has not been read.

Changed:
- v1: "Not that the relational floor is established; the decisive household-data test has not been run." v2: not that the relational floor is established, **and not that it is rejected**; the earlier rejection was an artefact of a hard liquidity threshold, and the data do not discriminate it (`credential-floor.md`).

Added:
- That Boudon's question is "recovered" for comparative education, or that Epstein's standard is the epistemology and the paper adds credibility to it (see `NOVELTY.md` §3).
- That the China forecast "failed in public", or that the strict tests were blind. Only the Oct-Dec 2026 forecast, and ledger entries frozen before release, are blind.
- That the spread-out-entry mechanism has been shown to beat naive. The selected variant lost; the others are not distinguishable from naive on 19 correlated months.
- That the 1.27 figure is an out-of-sample result, or an unambiguous "whole-record" error.
- That agreement among rival variants of a model is evidence for a policy conclusion when they share code.
- That docking identifies mechanisms.
- That the project does history matching in the emulator-and-implausibility sense unless it does.
- That the cocoon is new. Its parts are cited in section 3.
- That "comparative education can be made cumulative" has been shown; the evidence so far is that models were downgraded on review.
- Policy projections from the credential-floor model, whose sign depends on the form of the liquidity constraint.
- Any claim from the `research/` folders before their results are inserted and checked.

---

## Part 8. Open decisions

1. Co-authorship (as v1): sole-authored, or with Bjorn Nordtveit. The lineage section is shared with the massification paper.
2. Whether to wait for scored Oct-Dec 2026 releases and the `research/` results before drafting section 6-7. The paper is stronger with them; the outline works if they are pending as long as the paper is framed as a protocol.
3. Which source-file fixes to make first (none made here): `seasonal_2024.md` prose (items 1-2), `facts_register.md` role labels and the +22.8 sentence, `docs/engine/relational_floor_*.md` (v1 numbers), the 5.49 / 5.57 mismatch. I edited none of them.
4. Locate the files v1 cites that are absent here (`RUN_REPORT.md`, `related/`, several `tests/` files, `worlds/angkor/`, `LICENSES.md`), or drop the citations.
5. Read Hedström (2005), Manzo (2013, 2022) and Breen and Goldthorpe (1997) in full and revise section 2 accordingly.
6. Check the comparative-education journals for existing simulation work; revise the "taking it into the field" claim to match what is found.
