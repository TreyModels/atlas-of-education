# Module: Reading models critically

An eight-session module for M.Ed and undergraduate social-science students. No mathematics is assumed. Students learn to read a simulation model the way they would read a policy paper: by asking what was assumed, what was tested, and what would have shown it wrong.

The method is simple. Each session gives students a model whose headline result looked like a finding. They find out for themselves that the result was built in. The exercises are in `teach/EXERCISES.md`. The numbers behind each one were checked against the repository files named there.

Session length is the instructor's choice. The plan below assumes about two hours: 20 minutes of framing, one or two exercises (20 to 40 minutes each), and 30 minutes of discussion. Students need the app running (see `teach/README.md`).

## Overview

| Session | Question | Exercises |
|---|---|---|
| 1 | What is a model for, and what does "illustrative" mean? | 1 |
| 2 | Where do the numbers come from, and how much is luck? | 2, 3 |
| 3 | Which results survive a change of default? | 4, 9 |
| 4 | Can a model win by how it was defined? | 5, 6 |
| 5 | What does it mean for a model to fit? | 7, 11 |
| 6 | Do two trends tell us anything about each other? | 8 |
| 7 | When explanations agree, is that evidence? | 10, 12 |
| 8 | The gate: how to start before building anything | Capstone |

---

## Session 1. What is a model for, and what does "illustrative" mean?

**Question.** If a model cannot be checked against the world, what can it still teach?

**Models used.** China graduate jobs (`#china`). The catalogue (`#catalogue`) for orientation.

**Exercises.** Exercise 1 (does the model beat "same as last year?").

**Before class.** Students read the status table in `REVIEW_STATUS.md` and the three status labels (see `teach/README.md`, "Reading the status labels").

**In class.**
1. Open the catalogue. Ask students to guess which models are calibrated and which illustrative. Then show the table.
2. Exercise 1.
3. Discussion: a ministry asks for a forecast. Why might the simplest rule be the one to beat?

**Readings (choose one or both).**
- Epstein, J. M. (2008). "Why Model?" *Journal of Artificial Societies and Social Simulation* 11(4), 12. Epstein lists reasons to build a model other than prediction. It sets up the idea that a model can be useful without being right.
- Optional: Hyndman, R. J. and Athanasopoulos, G., *Forecasting: Principles and Practice* (free online, OTexts). The section on simple forecasting methods (naive and seasonal naive).

**Hand in.** One paragraph. Choose one status label and say what a reader may and may not conclude from a model carrying it, using the China model as the example.

---

## Session 2. Where do the numbers come from, and how much is luck?

**Question.** When a model gives a cost or an effect, what population and what noise is it measured against?

**Models used.** Cambodia child labour (`#cambodia`).

**Exercises.** Exercise 2 (who is the cost index charging?). Exercise 3 (is the policy effect bigger than the noise?).

**In class.**
1. Exercise 2 first (a short sum, a quick win).
2. Exercise 3. Collect each student's six no-programme rates on the board before anyone moves a lever.
3. Discussion: a study reports that a programme cut child labour by half a point. What else must be reported before you believe it?

**Readings.**
- Cartwright, N. and Hardie, J. (2012). *Evidence-Based Policy: A Practical Guide to Doing It Better*. Oxford University Press. A chapter of the instructor's choice on whether a result that holds in one setting will hold in another.
- Optional background for the instructor: the "Caveats" section of `experiments/camchild-seeds/README.md`.

**Hand in.** A half-page note: "The effect of lever X is smaller than the noise. What would I need to claim it is real?" Use the paired-seed numbers in `experiments/camchild-seeds/README.md` (for example migrant-child support: -0.26 pp, t = -3.5) as the example.

---

## Session 3. Which results survive a change of default?

**Question.** How can a model's headline result depend on a number the author never highlighted?

**Models used.** Angkor: Petri lab (`#petri`) and Elite relocation (`#relocation`).

**Exercises.** Exercise 4 (the coordination multiplier). Exercise 9 (the floor under the water). Both include an instructor demonstration; run them live.

**In class.**
1. Read the model's own question aloud: "When does the court choose another centre?" Ask students what they would need to believe.
2. Exercise 4, then Exercise 9.
3. Discussion: the original paper described a size association. What is the difference between "larger places had more land and water per person" and "larger places are more productive"?

**Readings.**
- Klassen, Ortman, Lobo and Evans (2022). "Provisioning an Early City: Spatial Equilibrium in the Agricultural Economy at Angkor, Cambodia." *Journal of Archaeological Method and Theory* 29: 763-794. Read the introduction and discussion; for the scaling table, see `experiments/angkor-review/README.md` section 5.1 for what the review says about it.
- Hall, Penny and Hamilton (2018), *PLOS ONE*, https://doi.org/10.1371/journal.pone.0203962 (the link is on `public/research/relocation.html`). It documents continued settlement at Koh Ker after the royal court left, which is the empirical constraint the relocation model is asked to respect.

**Hand in.** Two columns on one page. Left: three results the Angkor models showed before the review. Right: what each one depended on.

---

## Session 4. Can a model win by how it was defined?

**Question.** When one strategy wins a race, was the race fair?

**Models used.** Out of Africa, "Coast or herds?" (the page `public/research/out-of-africa.html` and the separate repository).

**Exercises.** Exercise 5 (can the mixed strategy lose?). Exercise 6 (rank by total, or by area?).

**In class.**
1. Students read the Atlas page's sentence "The mixed strategy is the most likely in both chronologies" before seeing any table. Take a quick vote on whether they believe it.
2. Exercise 5, then Exercise 6 (spreadsheet).
3. Discussion: the standalone page was corrected, but the Atlas copy was not. What does that tell you about how corrections travel?

**Readings.**
- Grimm, V. et al. (2005). "Pattern-oriented modeling of agent-based complex systems: lessons from ecology." *Science* 310: 987-991. The idea of testing a model against several patterns at once, which is what the shadow education and Out of Africa models try to do.
- Epstein (2008) again, the list of reasons to model other than prediction.

**Hand in.** The spreadsheet from Exercise 6, with one sentence explaining the change in ranking, and one sentence rewriting the Out of Africa page's headline sentence so that it is true.

---

## Session 5. What does it mean for a model to fit?

**Question.** A model matches the past. Does that tell us it understands the present?

**Models used.** China graduate jobs (`#china`) and its stored fit (`engine/firms/results/china_fit.md`).

**Exercises.** Exercise 7 (the unexplained step in August 2021). Exercise 11 (parameters on the wall). Students will also recall Exercise 1.

**In class.**
1. Ask: how many numbers did the model fit? (Eleven.) How many data points did it fit? (60 months in the early window.) What does the ratio suggest?
2. Exercises 7 and 11.
3. Discussion: the model was labelled "fitted + free residual". Where in the model is the free residual?

**Readings.**
- Grimm et al. (2005), for contrast with a model that has to match several independent patterns.
- Read `research/china-forecast-ledger/README.md`, sections "Puzzle", "Fact check" and "Results" (about three pages). It shows how the same question is handled when the benchmark is chosen first and a loss is reported first.

**Hand in.** A short comparison of the 2021 events (the tutoring restrictions and the property downturn) as possible explanations for the step. For each, write one observation outside the model that would support or weaken it.

---

## Session 6. Do two trends tell us anything about each other?

**Question.** Fertility and life expectancy both fall for sixty years. Does one explain the other?

**Models used.** Fertility collapse lab (`public/research/fertility.html`).

**Exercises.** Exercise 8 (two lines going down).

**In class.**
1. Draw the two invented lines from step 4 of the exercise on the board before any data are shown.
2. Run the Korea snippet live. Then read the first table of `experiments/fertility-trend-check/README.md`.
3. Discussion: what would a convincing test of "development lowers fertility" look like? (Look for events: a sudden change in one series that is not shared by the other.)

**Readings.**
- Granger, C. W. J. and Newbold, P. (1974). "Spurious regressions in econometrics." *Journal of Econometrics* 2: 111-120. This is technical; assign it to the instructor, or ask students to read only the introduction and conclusion.
- The lab page itself: the four-act summary and "claims held vs ruled out".

**Hand in.** Choose two time series from a statistical yearbook (for example, school enrolment and mobile phone subscriptions in one country). Explain in 150 words why they correlate, and why that tells you nothing about cause.

---

## Session 7. When explanations agree, is that evidence?

**Question.** If three explanations make the same prediction, or if the data cannot separate them, what have we learned?

**Models used.** Shadow education lab (`public/research/shadow-education.html`) and the credential floor (`#credentials`, `public/reference/credential-floor.md`).

**Exercises.** Exercise 10 (three explanations, one code base). Exercise 12 (the cliff in the credential floor, and the seed that changes).

**In class.**
1. Exercise 10, then Exercise 12. The two end on the same point: a result can be a product of the model's structure, not of the world.
2. Discussion: list the three explanations of shadow education from the lab page. Which published evidence would separate them?

**Readings.**
- Bray, M. (1999). *The Shadow Education System: Private Tutoring and Its Implications for Planners*. Paris: UNESCO International Institute for Educational Planning. Background on the phenomenon the model tries to explain.
- Boudon, R. (1974). *Education, Opportunity, and Social Inequality: Changing Prospects in Western Society*. New York: Wiley. Primary and secondary effects of social origin on educational choice.
- Optional: Collins, R. (1979). *The Credential Society*. New York: Academic Press; and Dore, R. (1976). *The Diploma Disease*. London: Allen and Unwin.

**Hand in.** One page. Choose two rival explanations of why students stay in school or buy tutoring. State what each predicts that the other does not. Say whether any data you know of would show that.

---

## Session 8. The gate, and the capstone workshop

**Question.** Before anyone builds a model, what must be in place?

**Models used.** None. The reading is `research/GATE.md` and `research/PUZZLE_LOG.md`.

**In class.**
1. Read the gate table aloud: fact check, two rivals, the separating observation, small or recoverable, a benchmark, owned. Ask students which gate each of the twelve exercises would have failed.
2. Read the first row of `research/PUZZLE_LOG.md` (the unmarried-adults survey in China) as a worked example of the three-line format.
3. Peer review: students swap capstone drafts and answer the three questions below.

**Readings.** `research/GATE.md`. `research/PUZZLE_LOG.md`, first row only. `research/china-forecast-ledger/README.md`, first sentence of "Results" (a loss reported first).

**Hand in.** The capstone (below).

---

## Capstone assignment: the gate

Students do the first three gates from `research/GATE.md` on a topic of their own. They do not build a model.

**Task.** Take one chart from the news or from an international agency report on a comparative education or development topic. Write about 800 words in four parts.

1. **The fact.** State in one sentence what the chart shows: who, what, where, when, in which units. Then find a second, independent source (a different organisation, not a copy of the first). Report whether the two agree. If they disagree, say so first, because that is the finding.
2. **Two rival explanations.** One plain sentence each. An explanation with no rival is only a description. The explanations must be different in kind, not two strengths of the same cause.
3. **The separating observation.** Name something that could be measured, where the two rivals predict different results. Write it down as if before collecting any data. Say where such data might exist.
4. **A benchmark.** In two sentences: what simple rule (last year's value, no change, chance) would any model of this have to beat?

**Hand in** the four parts, and a three-line row in the format of `research/PUZZLE_LOG.md` (fact, rivals, separating observation).

**Assessment guide.**

| Criterion | What good work shows |
|---|---|
| Fact check | A second source that is really independent. Disagreement reported, not hidden. |
| Rivals | Two explanations with different consequences, not synonyms. |
| Separating observation | Specific and measurable. It could in principle come out against one rival. |
| Benchmark | A rule needing no parameters. |
| Plain language | No term left unexplained. |

**Peer review questions (session 8).** (1) Would the second source disagree if the first source were wrong? (2) Could the separating observation come out for both rivals? (3) What would the author need to assume to build a model of this?

---

## Optional extension

The review found results that restate the model's own rules (item 5.7 in `experiments/angkor-review/README.md`; proposed rewording in `experiments/angkor-review/TEXT_CHANGES.json`). One example: in `experiments/learning-round2/RESULTS.md`, finding 1 says that funding maintenance before ritual lowers the drought food gap, and now adds that "the ordering is set by the model rule, so this is an assumption-driven result, not a finding." Students can be asked to find, in that file and in `experiments/frontier-allocation/RESULTS.md` (section "Changing priorities after conquest"), the sentence where the model's own rule is stated, and to say whether the headline sentence would still be interesting without it. The two `learning` folders carry a warning that they were produced with the old coordination multiplier and water floor and have not been rerun. Treat all of these as historical.
