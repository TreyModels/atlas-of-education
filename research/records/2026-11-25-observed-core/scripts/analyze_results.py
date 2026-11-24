#!/usr/bin/env python3
"""Summarise the observed-core multiverse results into a machine-readable JSON.

Reads results/predictive.csv, results/transmission.csv, results/verdicts.csv.
No model fitting here; arithmetic on committed outputs only.
"""
import csv, json, os, sys
import numpy as np
from collections import defaultdict

HERE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RES = os.path.join(HERE, "results")


def load(name):
    p = os.path.join(RES, name)
    with open(p) as f:
        return list(csv.DictReader(f))


def fnum(x):
    if x is None or x == "" or x == "None":
        return float("nan")
    return float(x)


def main():
    pred = load("predictive.csv")
    trans = load("transmission.csv")
    verdicts = load("verdicts.csv")

    out = {"cells_total": len(pred), "cells_by_status": {}, "by_outcome_horizon": {},
           "by_split": {}, "transmission": {}, "verdict_counts": {}}

    for r in pred:
        st = r["status"]
        out["cells_by_status"][st] = out["cells_by_status"].get(st, 0) + 1

    # split-level summary
    for split in sorted({r["split"] for r in pred}):
        cells = [r for r in pred if r["split"] == split and r["status"] == "ok"]
        sp = np.array([fnum(r["skill_persist"]) for r in cells])
        st = np.array([fnum(r["skill_trend"]) for r in cells])
        sm = np.array([fnum(r["skill_mean"]) for r in cells])
        out["by_split"][split] = {
            "n_cells_ok": len(cells),
            "median_skill_persist": round(float(np.nanmedian(sp)), 4) if len(sp) else None,
            "median_skill_trend": round(float(np.nanmedian(st)), 4) if len(st) else None,
            "median_skill_mean": round(float(np.nanmedian(sm)), 4) if len(sm) else None,
            "share_cells_beating_persistence": round(float(np.mean(sp > 0)), 3) if len(sp) else None,
        }

    # outcome x horizon: distribution over all splits and over loo only
    for oc in sorted({r["outcome"] for r in pred}):
        for h in sorted({int(r["horizon"]) for r in pred if r["outcome"] == oc}):
            for scope in ("all", "loo"):
                cells = [r for r in pred if r["outcome"] == oc and int(r["horizon"]) == h
                         and r["status"] == "ok" and (scope == "all" or r["split"] == "loo")]
                sp = np.array([fnum(r["skill_persist"]) for r in cells])
                st = np.array([fnum(r["skill_trend"]) for r in cells])
                key = f"{oc}|h{h}|{scope}"
                out["by_outcome_horizon"][key] = {
                    "n_cells": len(cells),
                    "median_n_train": int(np.median([int(r["n_train"]) for r in cells])) if cells else None,
                    "median_n_test": int(np.median([int(r["n_test"]) for r in cells])) if cells else None,
                    "median_skill_persist": round(float(np.nanmedian(sp)), 4) if len(sp) else None,
                    "median_skill_trend": round(float(np.nanmedian(st)), 4) if len(st) else None,
                    "share_beating_persistence": round(float(np.mean(sp > 0)), 3) if len(sp) else None,
                    "share_beating_trend": round(float(np.mean(st > 0)), 3) if len(st) else None,
                }

    # controls/form robustness of beating persistence (LOO only)
    rob = defaultdict(lambda: {"n": 0, "win_p": 0, "win_t": 0})
    for r in pred:
        if r["split"] != "loo" or r["status"] != "ok":
            continue
        k = (r["outcome"], r["horizon"], r["controls"])
        rob[k]["n"] += 1
        rob[k]["win_p"] += int(fnum(r["skill_persist"]) > 0)
        rob[k]["win_t"] += int(fnum(r["skill_trend"]) > 0)
    out["loo_cell_wins"] = [
        {"outcome": k[0], "horizon": int(k[1]), "controls": k[2], "n": v["n"],
         "share_beating_persistence": round(v["win_p"] / v["n"], 3),
         "share_beating_trend": round(v["win_t"] / v["n"], 3)}
        for k, v in sorted(rob.items())
    ]

    # verdict counts
    for v in verdicts:
        out["verdict_counts"][v["verdict"]] = out["verdict_counts"].get(v["verdict"], 0) + 1

    # transmission: per t_id sign robustness across cells
    tr = defaultdict(list)
    for r in trans:
        tr[r["t_id"]].append(r)
    for tid, cells in sorted(tr.items()):
        coefs = np.array([fnum(c["coef"]) for c in cells])
        ses = np.array([fnum(c["se"]) for c in cells])
        ts = np.array([fnum(c["t"]) for c in cells])
        sign = cells[0]["expected_sign"]
        sign_ok = np.array([(c > 0 and sign == "+") or (c < 0 and sign == "-") for c in coefs])
        sig = np.abs(ts) > 1.96
        out["transmission"][tid] = {
            "n_cells": len(cells),
            "expected_sign": sign,
            "median_coef": round(float(np.nanmedian(coefs)), 4),
            "median_se": round(float(np.nanmedian(ses)), 4),
            "share_expected_sign": round(float(np.mean(sign_ok)), 3),
            "share_significant_5pct": round(float(np.mean(sig)), 3),
            "share_expected_sign_and_significant": round(float(np.mean(sign_ok & sig)), 3),
            "cells": [{"h": int(c["h"]), "fe": c["fe"], "extra_control": c["extra_control"],
                       "coef": round(fnum(c["coef"]), 4), "se": round(fnum(c["se"]), 4),
                       "t": round(fnum(c["t"]), 2), "n": int(c["n"]), "n_countries": int(c["n_countries"])}
                      for c in cells],
            "status": ("present_but_mixed" if np.mean(sign_ok) < 1 else "sign_consistent"),
        }
    out["transmission_missing"] = [t for t in ["T1", "T2", "T3", "T4", "T5", "T6", "T7"]
                                   if t not in tr]

    with open(os.path.join(RES, "analysis_summary.json"), "w") as f:
        json.dump(out, f, indent=2, sort_keys=True)
    print(json.dumps({k: out[k] for k in ("cells_total", "cells_by_status", "by_split",
                                          "verdict_counts", "transmission_missing")}, indent=2))
    for tid, v in out["transmission"].items():
        print(f"{tid}: coef {v['median_coef']:+.3f} se {v['median_se']:.3f} "
              f"sign {v['share_expected_sign']:.2f} sig {v['share_significant_5pct']:.2f} "
              f"sign+sig {v['share_expected_sign_and_significant']:.2f}")


if __name__ == "__main__":
    main()
