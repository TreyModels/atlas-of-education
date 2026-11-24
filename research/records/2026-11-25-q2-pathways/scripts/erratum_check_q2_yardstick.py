#!/usr/bin/env python3
"""Erratum check — Q2 random-matching yardstick compares the wrong observed statistic.

The committed `results/audit/audit_random_yardstick.json` computes `observed` as the median absolute
1990-2010 gap over ALL pairs of the 105 baseline-complete countries, while each random draw computes the
median over its 52 random pairs. The matched pairs' own medians are different (0.620 schooling, 0.2375
TFR, from `results/audit/pairs_primary.csv`). This script reproduces the committed random yardstick
(seed 71201, 1,000 draws, same algorithm as `scripts/q2_audit.py::random_yardstick`) and reports the share
of random draws whose median is at least as large as (i) the committed all-pairs median and (ii) the
matched-pair median.

Writes `results/audit/erratum_check_q2_yardstick.json`.

Run (needs numpy/pandas, e.g. the project's bundled runtime python):
    python3 scripts/erratum_check_q2_yardstick.py
"""
import json

import numpy as np
import pandas as pd

OUTCOMES = ["mean_years_schooling", "tfr_observed_1950plus"]
FEATURES = ["mean_years_schooling", "tfr_observed_1950plus",
            "gdp_pc_maddison_1990int", "urban_share_pct"]

d = pd.read_csv("data/long_run_panel.csv")
d["iso3"] = d["iso3"].astype(str)
base = d.loc[d.year.eq(1980), ["iso3"] + FEATURES].set_index("iso3").sort_index().dropna()
base = base[base["gdp_pc_maddison_1990int"] > 0].copy()
base["gdp_pc_maddison_1990int"] = np.log(base["gdp_pc_maddison_1990int"])
names = list(base.index)

lv0 = d.loc[d.year.eq(1990), ["iso3"] + OUTCOMES].set_index("iso3")
lv1 = d.loc[d.year.eq(2010), ["iso3"] + OUTCOMES].set_index("iso3")
ch = (lv1 - lv0).reindex(names)


def all_pairs_median(col):
    a = ch[col].to_numpy()
    m = np.abs(a[:, None] - a[None, :])
    return float(np.median(m[np.triu_indices(len(a), 1)]))


observed_all_pairs = {c: all_pairs_median(c) for c in OUTCOMES}

rng = np.random.default_rng(71201)
sch, tfr = [], []
for _ in range(1000):
    perm = rng.permutation(len(names))
    s, t = [], []
    for k in range(len(perm) // 2):
        i, j = perm[2 * k], perm[2 * k + 1]
        s.append(abs(ch.iloc[i][OUTCOMES[0]] - ch.iloc[j][OUTCOMES[0]]))
        t.append(abs(ch.iloc[i][OUTCOMES[1]] - ch.iloc[j][OUTCOMES[1]]))
    sch.append(float(np.median(s)))
    tfr.append(float(np.median(t)))
sch = np.array(sch)
tfr = np.array(tfr)

# matched-pair medians from the committed primary pair table
pairs = pd.read_csv("results/audit/pairs_primary.csv")
matched_medians = {
    OUTCOMES[0]: float(pairs["mean_years_schooling_gap"].median()),
    OUTCOMES[1]: float(pairs["tfr_observed_1950plus_gap"].median()),
}

committed = json.load(open("results/audit/audit_random_yardstick.json"))
out = {
    "question": ("Does the committed random-yardstick comparison use the matched-pair observed medians?"),
    "answer": ("NO — the committed 'observed' statistics (0.820 / 0.7715) are medians over all "
               "5,460 unordered pairs of the 105 countries, while the random draws use their 52 pairs. "
               "The matched-pair medians are 0.620 / 0.2375; against those the shares are 96.1% / 100.0%, "
               "i.e. the matched pairs are LESS divergent than random pairing (direction of the paper's "
               "point survives; the magnitude and the 'central honest null' sentence do not)."),
    "seed": 71201,
    "n_draws": 1000,
    "n_countries": len(names),
    "all_pairs_observed": {k: round(v, 4) for k, v in observed_all_pairs.items()},
    "matched_pair_observed": {k: round(v, 4) for k, v in matched_medians.items()},
    "random_draw_median_of_medians": {
        "schooling": round(float(np.median(sch)), 4),
        "tfr": round(float(np.median(tfr)), 4),
    },
    "share_random_median_ge_all_pairs_observed": {
        "schooling": round(float((sch >= observed_all_pairs[OUTCOMES[0]]).mean()), 4),
        "tfr": round(float((tfr >= observed_all_pairs[OUTCOMES[1]]).mean()), 4),
    },
    "share_random_median_ge_matched_pair_observed": {
        "schooling": round(float((sch >= matched_medians[OUTCOMES[0]]).mean()), 4),
        "tfr": round(float((tfr >= matched_medians[OUTCOMES[1]]).mean()), 4),
    },
    "committed_json": {
        "observed": committed["observed"],
        "share_random_median_schooling_ge_observed": committed["share_random_median_schooling_ge_observed"],
        "share_random_median_tfr_ge_observed": committed["share_random_median_tfr_ge_observed"],
    },
    "reproduction": ("python3 scripts/erratum_check_q2_yardstick.py (this record; reads "
                     "data/long_run_panel.csv and results/audit/pairs_primary.csv; same algorithm and "
                     "seed as scripts/q2_audit.py)"),
}
assert abs(out["all_pairs_observed"][OUTCOMES[0]] - 0.8200) < 5e-4
assert abs(out["all_pairs_observed"][OUTCOMES[1]] - 0.7715) < 5e-4
assert abs(out["share_random_median_ge_all_pairs_observed"]["schooling"] - 0.524) < 5e-4
assert abs(out["share_random_median_ge_all_pairs_observed"]["tfr"] - 0.503) < 5e-4
json.dump(out, open("results/audit/erratum_check_q2_yardstick.json", "w"), indent=1)
print(json.dumps(out, indent=1))
