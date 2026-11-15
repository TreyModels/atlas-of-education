"""Experiment 2. Which things that nobody has measured would tell the explanations apart?

Uses the same pretend datasets as Experiment 1, restricted to those that fit all seven published patterns
(so every row "looks like Siem Reap"). For every other model output it reports
  * AUC for each pair of explanations: the chance that a randomly chosen dataset from one explanation has a
    higher value than one from the other (0.5 = no separation, 1.0 = perfect), shown as max(AUC, 1 - AUC);
  * how much the classifier of Experiment 1 improves when that one output is added to the seven patterns.
It also reads the repo's stored policy runs (results/fresh_check.csv) to ask whether the response to a ban on
teachers tutoring their own pupils separates the explanations.
"""
import json
import numpy as np
import pandas as pd
from scipy.stats import rankdata
from common import ABM, MEASURED, RESULTS, TOL
from recovery import cv_predict, fits, summarise

DERIVED = {
    "instruction_gap_tutoring_vs_not": lambda d: d["instr_tutoring_teacher"] - d["instr_nontutoring_teacher"],
    "purchase_gap_tutoring_vs_not": lambda d: d["buy_tutoring_teacher"] - d["buy_nontutoring_teacher"],
    "coverage_gap_rich_minus_poor": lambda d: d["coverage_q5"] - d["coverage_q1"],
    "participation_gap_rich_minus_poor": lambda d: d["participation_q5"] - d["participation_q1"],
}
SKIP = set(MEASURED) | {"variant", "particle", "group", "world", "converged", "sweeps", "fits",
                        "participation_urban", "participation_rural",
                        # these three are the same patterns counted per pupil rather than per purchase
                        }
PLAIN = {
    "withholding_mean": "share of the curriculum teachers hold back from regular lessons (all teachers)",
    "withholding_among_sellers": "share of the curriculum held back, among teachers who tutor their own pupils",
    "class_instruction": "share of the curriculum delivered in regular lessons",
    "nonbuyer_class_instruction": "regular-lesson coverage received by pupils who buy no tutoring",
    "instr_tutoring_teacher": "regular-lesson coverage in classes whose teacher tutors own pupils",
    "instr_nontutoring_teacher": "regular-lesson coverage in classes whose teacher does not",
    "instruction_gap_tutoring_vs_not": "regular-lesson coverage: tutoring teachers' classes minus other classes",
    "buy_tutoring_teacher": "share of pupil-subjects with tutoring, in classes whose teacher tutors own pupils",
    "buy_nontutoring_teacher": "the same share in classes whose teacher does not",
    "purchase_gap_tutoring_vs_not": "tutoring take-up: tutoring teachers' classes minus other classes",
    "other_given_tutoring_teacher": "share buying from the parallel-class teacher when the own teacher tutors",
    "other_given_nontutoring_teacher": "share buying from the parallel-class teacher when the own teacher does not",
    "coverage": "total curriculum coverage, lessons plus tutoring",
    "coverage_q1": "total coverage, poorest fifth", "coverage_q5": "total coverage, richest fifth",
    "coverage_gap_rich_minus_poor": "total coverage: richest fifth minus poorest fifth",
    "participation_q1": "tutoring participation, poorest fifth", "participation_q5": "tutoring participation, richest fifth",
    "participation_gap_rich_minus_poor": "participation: richest fifth minus poorest fifth",
    "subjects_bought": "number of subjects tutored per pupil",
    "own_share": "share of tutored pupils with any own-teacher tutoring",
    "other_share": "share of tutored pupils with any parallel-teacher tutoring",
    "com_share": "share of tutored pupils with any commercial tutoring",
    "teacher_own_share": "share of teachers who tutor their own pupils",
    "ban_participation": "change in participation when teachers may not tutor own pupils (policy run)",
    "ban_nonbuyer_instr": "change in non-buyers' regular-lesson coverage under that ban (policy run)",
}


def auc(a, b):
    a, b = a[~np.isnan(a)], b[~np.isnan(b)]
    if len(a) == 0 or len(b) == 0:
        return float("nan")
    r = rankdata(np.concatenate([a, b]))
    u = r[:len(a)].sum() - len(a) * (len(a) + 1) / 2
    v = u / (len(a) * len(b))
    return float(max(v, 1 - v))


def main():
    df = pd.read_csv(RESULTS / "bank.csv.gz")
    for k, f in DERIVED.items():
        df[k] = f(df)
    df["fits"] = fits(df)
    d = df[df["fits"]].copy()
    outputs = [c for c in d.columns if c not in SKIP]
    pairs = [("thin", "diversion"), ("thin", "favour"), ("diversion", "favour"), ("thin", "full")]
    table = {}
    for o in outputs:
        row = {f"{a}_vs_{b}": auc(d.loc[d.variant == a, o].to_numpy(), d.loc[d.variant == b, o].to_numpy()) for a, b in pairs}
        row["missing_share"] = float(d[o].isna().mean())
        row["median_by_variant"] = d.groupby("variant")[o].median().round(4).to_dict()
        row["plain"] = PLAIN.get(o, o)
        table[o] = row
    # value added to the classifier (three explanations, rows that fit)
    labels = ["thin", "diversion", "favour"]
    X = d[d.variant.isin(labels)].copy()
    for k in MEASURED:
        X[k] = X[k] / TOL[k]
    y, pred, groups = cv_predict(X, MEASURED, labels)
    base = summarise(y, pred, groups, labels, n_boot=200)["balanced_accuracy"]
    for o in outputs:
        Xo = X.copy()
        Xo[o] = Xo[o].fillna(Xo[o].median())
        y, pred, groups = cv_predict(Xo, MEASURED + [o], labels)
        table[o]["accuracy_with_this_added"] = summarise(y, pred, groups, labels, n_boot=50)["balanced_accuracy"]
        print(o, round(table[o]["accuracy_with_this_added"], 3), flush=True)
    Xall = X.copy()
    for o in outputs:
        Xall[o] = Xall[o].fillna(Xall[o].median())
    y, pred, groups = cv_predict(Xall, MEASURED + outputs, labels)
    all_out = summarise(y, pred, groups, labels, n_boot=200)
    # policy response from the repo's stored runs
    pol = pd.read_csv(ABM / "results" / "fresh_check.csv")
    pol = pol[pol.fit == 1]
    policy = {}
    for o in ("ban_participation", "ban_nonbuyer_instr"):
        policy[o] = {f"{a}_vs_{b}": auc(pol.loc[pol.variant == a, o].to_numpy(), pol.loc[pol.variant == b, o].to_numpy())
                     for a, b in pairs}
        policy[o]["median_by_variant"] = pol.groupby("variant")[o].median().round(4).to_dict()
        policy[o]["plain"] = PLAIN[o]
    out = {"rows_that_fit": int(len(d)), "rows_by_variant": d.variant.value_counts().to_dict(),
           "accuracy_seven_patterns_only": base, "chance": 1 / 3, "accuracy_all_outputs_added": all_out,
           "outputs": table, "policy_response_from_repo_runs": policy}
    (RESULTS / "discriminate.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
