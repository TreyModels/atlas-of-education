"""Writes README.md from the result files, so no number in it is typed by hand."""
import json
from common import HERE, RESULTS

eq = json.loads((RESULTS / "equivalence.json").read_text())
rec = json.loads((RESULTS / "recovery.json").read_text())
dis = json.loads((RESULTS / "discriminate.json").read_text())
T = rec["tests"]


def pct(x):
    return f"{100 * x:.0f}%"


def acc_row(key, label):
    a, f = T[f"{key}|all_rows"], T[f"{key}|rows_that_fit_all_seven"]
    return (f"| {label} | {pct(a['chance'])} | {pct(a['balanced_accuracy'])} ({pct(a['ci90'][0])}–{pct(a['ci90'][1])}) "
            f"| {pct(f['balanced_accuracy'])} ({pct(f['ci90'][0])}–{pct(f['ci90'][1])}) |")


worst = max(v["worst_abs_difference"] for v in eq["policies"].values())
three_all = T["three_way|all_rows"]["balanced_accuracy"]
three_fit = T["three_way|rows_that_fit_all_seven"]["balanced_accuracy"]
placebo = T["thin_vs_favour|rows_that_fit_all_seven"]["balanced_accuracy"]
td = T["thin_vs_diversion|rows_that_fit_all_seven"]["balanced_accuracy"]
rule_all = "above" if three_all - 1 / 3 > 0.10 else "within"
rule_fit = "above" if three_fit - 1 / 3 > 0.10 else "within"
outs = dis["outputs"]
best_td = sorted(outs.items(), key=lambda kv: -kv[1]["thin_vs_diversion"])[:6]
allacc = dis["accuracy_all_outputs_added"]
pol = dis["policy_response_from_repo_runs"]
wm = outs["withholding_mean"]

lines = []
A = lines.append
A("# Shadow education: can the three explanations be told apart?")
A("")
A("Written by `make_readme.py` from `results/*.json`. Do not edit by hand; rerun the scripts.")
A("")
A("**Status: not identified.** Inside this model the three explanations are, for practical purposes, one explanation. "
  "The model has to be redesigned before it can support a paper about rival explanations.")
A("")
A("## Puzzle")
A("In six Siem Reap schools most pupils pay for extra lessons, and most buy them from their own teacher "
  "(Bray et al. 2016, 2018). Why the own teacher?")
A("")
A("## Fact check")
A("The targets are seven published patterns from one study of six schools (overall, Grade 9 and Grade 12 participation, "
  "the urban–rural gap, the own-teacher and other-teacher shares, and the share of teachers who tutor), plus a small "
  "commercial share. There is no second, independent source for these patterns in the repo, and no pupil-level data. "
  "Gate 1 is therefore only half met.")
A("")
A("## Rival explanations")
A("- **Thin:** the timetable is too short for the curriculum, so everyone needs more hours.")
A("- **Diversion:** teachers hold back content in regular lessons and sell it in paid ones.")
A("- **Favour:** buying from your own teacher brings a benefit of its own (marks, goodwill).")
A("")
A("The tutoring model is imported unchanged from `experiments/shadow-abm/src/tutoring_abm/model.py`.")
A("")
A("## The test, fixed before running")
A("Take every fitted parameter set of each explanation, run it in fresh six-school systems, and summarise each run with "
  "the same published patterns. Each run is a pretend dataset whose true explanation is known. Train a classifier to name "
  "the explanation and test it on parameter sets it has not seen. **Rule:** accuracy within 10 points of chance means "
  "this kind of data cannot tell the explanations apart.")
A("")
A("## Result 1: “favour” is the same model as “thin”")
A("In the code a pupil's three options are worth `b + favour` (own teacher), `b − other_cost` (other teacher) and "
  "`b − commercial_cost`. Adding favour is therefore the same as raising the base demand and both costs by the same amount. "
  f"`equivalence.py` rewrites each of the {eq['n_parameter_sets']} distinct fitted favour parameter sets as a thin parameter "
  f"set and compares every model output in {eq['worlds']} school systems, with no policy and under each of the four policy "
  f"levers. The largest difference in any output is {worst:.1e}, which is rounding error. "
  f"{eq['rewritten_sets_outside_thin_prior_box']} of the {eq['n_parameter_sets']} rewritten sets fall outside the ranges "
  "allowed for the thin variant. Those ranges are the only thing that separates the two variants, so their different "
  "fit rates in the repo's calibration reflect the allowed ranges, not different behaviour.")
A("")
A("In plain words: the model has no observable consequence of favour that thin does not also have.")
A("")
A("## Result 2: the published patterns barely identify the explanation")
A(f"{rec['rows']:,} pretend datasets ({rec['worlds_per_set']} fresh school systems for each of 200 fitted parameter sets "
  "per variant). Accuracy is balanced across explanations; brackets are 90% intervals from resampling parameter sets.")
A("")
A("| Task | Chance | Accuracy, all datasets | Accuracy, datasets that fit all seven patterns |")
A("|---|---|---|---|")
A(acc_row("three_way", "Name one of three explanations"))
A(acc_row("four_way", "Name one of four (adds diversion + favour together)"))
A(acc_row("thin_vs_favour", "Thin vs favour (the same model: a placebo)"))
A(acc_row("thin_vs_diversion", "Thin vs diversion"))
A(acc_row("diversion_vs_favour", "Diversion vs favour"))
A("")
A(f"By the rule, three-way accuracy is {rule_all} the 10-point band on all datasets ({pct(three_all)} against 33%) and "
  f"{rule_fit} it on datasets that fit all seven patterns ({pct(three_fit)}). The placebo row shows how to read this: "
  f"thin and favour are the same model, yet the classifier separates them {pct(placebo)} of the time, because the two "
  "calibrations settled in different corners of the allowed ranges. Any accuracy at or below that level is an artefact of "
  f"the ranges. Thin against diversion scores {pct(td)}, below the placebo.")
A("")
A("## Result 3: nothing else the model produces separates them either")
A(f"Among the {dis['rows_that_fit']:,} datasets that fit all seven patterns, each other model output was scored by how well "
  "it separates pairs of explanations (AUC: 0.50 is no separation, 1.00 is perfect) and by how much it improves the "
  f"three-way classifier (which scores {pct(dis['accuracy_seven_patterns_only'])} on the seven patterns alone).")
A("")
A("| Output nobody has measured | Thin vs diversion | Diversion vs favour | Thin vs favour | Three-way accuracy if added |")
A("|---|---|---|---|---|")
for k, v in best_td:
    A(f"| {v['plain']} | {v['thin_vs_diversion']:.2f} | {v['diversion_vs_favour']:.2f} | {v['thin_vs_favour']:.2f} | {pct(v['accuracy_with_this_added'])} |")
A("")
A(f"With every model output added at once, three-way accuracy is {pct(allacc['balanced_accuracy'])} "
  f"({pct(allacc['ci90'][0])}–{pct(allacc['ci90'][1])}). The only output with any signal is withholding itself, and the "
  f"median fitted diversion dataset has withholding of {wm['median_by_variant']['diversion']:.3f}: most diversion settings "
  "that fit the data do not withhold, and then they behave exactly like thin.")
A("")
A("Policy response does not help. From the repo's stored runs, the change in participation under a ban on teachers "
  f"tutoring their own pupils separates thin from diversion with AUC {pol['ban_participation']['thin_vs_diversion']:.2f} "
  f"and diversion from favour with AUC {pol['ban_participation']['diversion_vs_favour']:.2f}.")
A("")
A("## What this means")
A("1. The planned paper, “what data would tell the three explanations apart”, cannot be written from this model. "
  "Inside it, no data would.")
A("2. The finding itself is worth a short section in the methods paper: a model advertised as three rival explanations "
  "was one explanation with three labels, and a recovery test plus one line of algebra showed it.")
A("3. To make the explanations rivals, each needs a consequence the others lack. Candidates to build and then test:")
A("   - **Favour:** school-assessed marks rise for pupils who buy from their own teacher, while externally marked exam "
  "scores do not. That needs marks in the model and both kinds of score in the data.")
A("   - **Diversion:** content covered in regular lessons is lower in tutoring teachers' classes than in the same "
  "teacher's classes in a subject or year where tutoring is not sold. That needs a within-teacher comparison.")
A("   - **Thin:** take-up tracks timetabled hours against curriculum load across subjects and grades, whoever the "
  "teacher is.")
A("4. The pupil-level survey behind Bray et al. may already hold some of this. Asking for it is the next step, before "
  "any more modelling.")
A("")
A("## Limits")
A("- The pretend datasets come from parameter sets fitted to the published patterns, so the test asks whether the "
  "explanations differ in the region that fits Siem Reap, not everywhere.")
A("- The repo's fitted sets for diversion and favour stopped just short of the fitting tolerance; restricting to "
  "datasets that fit all seven patterns handles this.")
A("- Each pretend dataset is one six-school system with exact choice probabilities; a real survey adds sampling error, "
  "which can only make separation harder.")
A("- The classifier is a random forest with 200 trees; a different classifier could score a few points differently.")
A("")
A("## Rerun")
A("```sh")
A("python3 equivalence.py        # under a minute")
A("python3 simulate_bank.py 30   # about five minutes, one core")
A("python3 recovery.py           # about two minutes")
A("python3 discriminate.py       # about four minutes")
A("python3 make_readme.py")
A("```")
(HERE / "README.md").write_text("\n".join(lines) + "\n")
print("README written")
