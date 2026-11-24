"""EXP-2: Test whether standard 10-year macro regressions blur distinct micro DGPs (Macro Wall),
and evaluate which micro observables separate the DGPs while passing Q1's zero-signal control.
"""
import argparse, json
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import cross_val_score

def main(inp, out_csv):
    df = pd.DataFrame(json.load(open(inp)))
    # 1. Macro summary by DGP x Arm
    rows = []
    for (dgp, arm, seed), g in df.groupby(["dgp", "arm", "seed"]):
        pre = g[g["t"] < 10]
        post = g[g["t"] >= 10]
        rows.append({
            "dgp": dgp, "arm": arm, "seed": seed,
            "d_ger": post["ger"].mean() - pre["ger"].mean(),
            "d_cl_total": post["cl_total"].mean() - pre["cl_total"].mean(),
            "d_study_work": post["study_work"].mean() - pre["study_work"].mean(),
            "d_hidden_work": post["hidden_work"].mean() - pre["hidden_work"].mean(),
            "d_tutoring": post["tutoring"].mean() - pre["tutoring"].mean(),
            "enrolled_hrs_p90": post["enrolled_work_hrs_p90"].mean(),
            "hidden_to_sw": post["hidden_to_sw_ratio"].mean(),
            "tutor_inc_corr": post["tutor_income_corr"].mean(),
            "mean_learn": post["mean_learn"].mean(),
        })
    sdf = pd.DataFrame(rows)
    sdf.to_csv(out_csv, index=False)

    # 2. Macro-only vs Micro-signature classification across the 3 single-mechanism DGPs
    sub = sdf[sdf["dgp"].isin(["DGP_POVERTY", "DGP_SCHOOL_PUSH", "DGP_CROWDING_TUTOR"]) & (sdf["arm"] == "tuition_only")]
    if len(sub) >= 9:
        macro_acc = cross_val_score(LogisticRegression(), sub[["d_ger", "d_cl_total"]], sub["dgp"], cv=3).mean()
        micro_acc = cross_val_score(
            LogisticRegression(),
            sub[["enrolled_hrs_p90", "hidden_to_sw", "tutor_inc_corr", "mean_learn"]],
            sub["dgp"], cv=3
        ).mean()
        print(f"3-DGP discrimination | Macro-only accuracy: {macro_acc:.3f} | Micro-signature accuracy: {micro_acc:.3f}")

    # 3. Print counterfactual arm table
    summary = sdf.groupby(["dgp", "arm"])[["d_ger", "d_study_work", "d_hidden_work", "d_tutoring"]].mean()
    print(summary.to_string())

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--inp", default="results/exp1_abm.json")
    ap.add_argument("--out", default="results/exp2_macro_wall.csv")
    args = ap.parse_args()
    main(args.inp, args.out)
