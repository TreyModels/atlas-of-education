# Shadow education: can the three explanations be told apart?

Written by `make_readme.py` from `results/*.json`. Do not edit by hand; rerun the scripts.

**Status: not identified.** Inside this model the three explanations are, for practical purposes, one explanation. The model has to be redesigned before it can support a paper about rival explanations.

## Puzzle
In six Siem Reap schools most pupils pay for extra lessons, and most buy them from their own teacher (Bray et al. 2016, 2018). Why the own teacher?

## Fact check
The targets are seven published patterns from one study of six schools (overall, Grade 9 and Grade 12 participation, the urban–rural gap, the own-teacher and other-teacher shares, and the share of teachers who tutor), plus a small commercial share. There is no second, independent source for these patterns in the repo, and no pupil-level data. Gate 1 is therefore only half met.

## Rival explanations
- **Thin:** the timetable is too short for the curriculum, so everyone needs more hours.
- **Diversion:** teachers hold back content in regular lessons and sell it in paid ones.
- **Favour:** buying from your own teacher brings a benefit of its own (marks, goodwill).

The tutoring model is imported unchanged from `experiments/shadow-abm/src/tutoring_abm/model.py`.

## The test, fixed before running
Take every fitted parameter set of each explanation, run it in fresh six-school systems, and summarise each run with the same published patterns. Each run is a pretend dataset whose true explanation is known. Train a classifier to name the explanation and test it on parameter sets it has not seen. **Rule:** accuracy within 10 points of chance means this kind of data cannot tell the explanations apart.

## Result 1: “favour” is the same model as “thin”
In the code a pupil's three options are worth `b + favour` (own teacher), `b − other_cost` (other teacher) and `b − commercial_cost`. Adding favour is therefore the same as raising the base demand and both costs by the same amount. `equivalence.py` rewrites each of the 116 distinct fitted favour parameter sets as a thin parameter set and compares every model output in 3 school systems, with no policy and under each of the four policy levers. The largest difference in any output is 6.7e-16, which is rounding error. 32 of the 116 rewritten sets fall outside the ranges allowed for the thin variant. Those ranges are the only thing that separates the two variants, so their different fit rates in the repo's calibration reflect the allowed ranges, not different behaviour.

In plain words: the model has no observable consequence of favour that thin does not also have.

## Result 2: the published patterns barely identify the explanation
24,000 pretend datasets (30 fresh school systems for each of 200 fitted parameter sets per variant). Accuracy is balanced across explanations; brackets are 90% intervals from resampling parameter sets.

| Task | Chance | Accuracy, all datasets | Accuracy, datasets that fit all seven patterns |
|---|---|---|---|
| Name one of three explanations | 33% | 45% (41%–49%) | 41% (36%–46%) |
| Name one of four (adds diversion + favour together) | 25% | 32% (28%–34%) | 29% (26%–31%) |
| Thin vs favour (the same model: a placebo) | 50% | 62% (55%–68%) | 62% (57%–67%) |
| Thin vs diversion | 50% | 56% (51%–62%) | 52% (46%–57%) |
| Diversion vs favour | 50% | 60% (55%–66%) | 59% (54%–64%) |

By the rule, three-way accuracy is above the 10-point band on all datasets (45% against 33%) and within it on datasets that fit all seven patterns (41%). The placebo row shows how to read this: thin and favour are the same model, yet the classifier separates them 62% of the time, because the two calibrations settled in different corners of the allowed ranges. Any accuracy at or below that level is an artefact of the ranges. Thin against diversion scores 52%, below the placebo.

## Result 3: nothing else the model produces separates them either
Among the 9,311 datasets that fit all seven patterns, each other model output was scored by how well it separates pairs of explanations (AUC: 0.50 is no separation, 1.00 is perfect) and by how much it improves the three-way classifier (which scores 41% on the seven patterns alone).

| Output nobody has measured | Thin vs diversion | Diversion vs favour | Thin vs favour | Three-way accuracy if added |
|---|---|---|---|---|
| share of the curriculum teachers hold back from regular lessons (all teachers) | 0.68 | 0.68 | 0.50 | 50% |
| share of the curriculum held back, among teachers who tutor their own pupils | 0.68 | 0.68 | 0.50 | 50% |
| regular-lesson coverage: tutoring teachers' classes minus other classes | 0.59 | 0.60 | 0.51 | 43% |
| regular-lesson coverage in classes whose teacher does not | 0.55 | 0.50 | 0.56 | 40% |
| total coverage, richest fifth | 0.55 | 0.51 | 0.56 | 41% |
| total curriculum coverage, lessons plus tutoring | 0.54 | 0.51 | 0.56 | 41% |

With every model output added at once, three-way accuracy is 49% (45%–54%). The only output with any signal is withholding itself, and the median fitted diversion dataset has withholding of 0.000: most diversion settings that fit the data do not withhold, and then they behave exactly like thin.

Policy response does not help. From the repo's stored runs, the change in participation under a ban on teachers tutoring their own pupils separates thin from diversion with AUC 0.56 and diversion from favour with AUC 0.53.

## What this means
1. The planned paper, “what data would tell the three explanations apart”, cannot be written from this model. Inside it, no data would.
2. The finding itself is worth a short section in the methods paper: a model advertised as three rival explanations was one explanation with three labels, and a recovery test plus one line of algebra showed it.
3. To make the explanations rivals, each needs a consequence the others lack. Candidates to build and then test:
   - **Favour:** school-assessed marks rise for pupils who buy from their own teacher, while externally marked exam scores do not. That needs marks in the model and both kinds of score in the data.
   - **Diversion:** content covered in regular lessons is lower in tutoring teachers' classes than in the same teacher's classes in a subject or year where tutoring is not sold. That needs a within-teacher comparison.
   - **Thin:** take-up tracks timetabled hours against curriculum load across subjects and grades, whoever the teacher is.
4. The pupil-level survey behind Bray et al. may already hold some of this. Asking for it is the next step, before any more modelling.

## Limits
- The pretend datasets come from parameter sets fitted to the published patterns, so the test asks whether the explanations differ in the region that fits Siem Reap, not everywhere.
- The repo's fitted sets for diversion and favour stopped just short of the fitting tolerance; restricting to datasets that fit all seven patterns handles this.
- Each pretend dataset is one six-school system with exact choice probabilities; a real survey adds sampling error, which can only make separation harder.
- The classifier is a random forest with 200 trees; a different classifier could score a few points differently.

## Rerun
```sh
python3 equivalence.py        # under a minute
python3 simulate_bank.py 30   # about five minutes, one core
python3 recovery.py           # about two minutes
python3 discriminate.py       # about four minutes
python3 make_readme.py
```
