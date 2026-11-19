"""Experiment 1. Given a dataset like the published one, can we tell which explanation produced it?

Each row of results/bank.csv is a pretend dataset: one fitted parameter set of a known explanation, run in one
fresh six-school system, summarised by the same seven patterns (plus the commercial share) that Bray et al. published.
A classifier is trained to name the explanation from those numbers and tested on parameter sets it has never seen
(folds are split by parameter set, so duplicates from resampling cannot leak).

Rule fixed before running: accuracy within 10 points of chance means the published kind of data cannot tell the
explanations apart, however carefully the model is calibrated.
"""
import json
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import GroupKFold
from common import MEASURED, RESULTS, TOL

RNG = np.random.default_rng(20261114)


def fits(df):
    from common import TARGETS, COM_MAX
    z = np.max([np.abs(df[k] - v) / tol for k, (v, tol) in TARGETS.items()]
               + [np.maximum(0, df["com_purchase_share"] - COM_MAX) / 0.05], axis=0)
    return z <= 1


def cv_predict(df, features, labels, n_splits=5, seed=0):
    X = df[features].to_numpy()
    y = df["variant"].map({v: i for i, v in enumerate(labels)}).to_numpy()
    groups = (df["variant"] + "_" + df["group"].astype(str)).to_numpy()
    pred = np.empty_like(y)
    for tr, te in GroupKFold(n_splits).split(X, y, groups):
        clf = RandomForestClassifier(n_estimators=200, min_samples_leaf=5, random_state=seed, n_jobs=1)
        clf.fit(X[tr], y[tr])
        pred[te] = clf.predict(X[te])
    return y, pred, groups


def summarise(y, pred, groups, labels, n_boot=500):
    k = len(labels)
    conf = np.zeros((k, k))
    for a, b in zip(y, pred):
        conf[a, b] += 1
    conf_share = conf / conf.sum(1, keepdims=True)
    acc = float(np.mean(conf_share.diagonal()))            # balanced accuracy: classes weighted equally
    # cluster bootstrap over parameter sets
    ug = np.unique(groups)
    idx = {g: np.flatnonzero(groups == g) for g in ug}
    boots = []
    for _ in range(n_boot):
        take = np.concatenate([idx[g] for g in RNG.choice(ug, len(ug))])
        c = np.zeros((k, k))
        np.add.at(c, (y[take], pred[take]), 1)
        with np.errstate(invalid="ignore"):
            boots.append(np.nanmean((c / c.sum(1, keepdims=True)).diagonal()))
    return {"labels": labels, "chance": 1 / k, "balanced_accuracy": acc,
            "ci90": [float(np.percentile(boots, 5)), float(np.percentile(boots, 95))],
            "confusion_row_share": conf_share.round(4).tolist(), "n_rows": int(len(y)),
            "n_parameter_sets": int(len(ug))}


def main():
    df = pd.read_csv(RESULTS / "bank.csv.gz")
    df["fits"] = fits(df)
    out = {"worlds_per_set": int(df.groupby(["variant", "particle"]).size().iloc[0]),
           "rows": int(len(df)), "fit_share_by_variant": df.groupby("variant")["fits"].mean().round(4).to_dict(),
           "features": MEASURED, "tests": {}}
    X = df.copy()
    for k in MEASURED:                                     # express each pattern in units of its tolerance
        X[k] = X[k] / TOL[k]
    sets = {"three_way": ["thin", "diversion", "favour"], "four_way": ["thin", "diversion", "favour", "full"],
            "thin_vs_favour": ["thin", "favour"], "thin_vs_diversion": ["thin", "diversion"],
            "diversion_vs_favour": ["diversion", "favour"]}
    for subset_name, mask in (("all_rows", np.ones(len(X), bool)), ("rows_that_fit_all_seven", X["fits"].to_numpy())):
        for name, labels in sets.items():
            d = X[mask & X["variant"].isin(labels)]
            y, pred, groups = cv_predict(d, MEASURED, labels)
            out["tests"][f"{name}|{subset_name}"] = summarise(y, pred, groups, labels)
            print(name, subset_name, out["tests"][f"{name}|{subset_name}"]["balanced_accuracy"], flush=True)
    (RESULTS / "recovery.json").write_text(json.dumps(out, indent=1))


if __name__ == "__main__":
    main()
