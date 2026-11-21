"""Item 2 — re-verify the decisive test (§8.2) and name what has two peaks.

Inputs: coexistence_*.csv (annual district metrics, model state), cohorts_*.csv
(cohort early-leaving), panel_*.csv (pupil records), PARAMETERS.csv (thresholds).

Checks
  B1  every coexistence row satisfies its own arithmetic
  B2  the four criteria are re-evaluated cell by cell (district x cohort entry
      year, candidate years entry+9..entry+11) with the *declared* thresholds,
      mirroring the declared rule: a cell passes iff all four hold in one year
  B3  per-arm/per-seed cell counts and the global verdict recomputed from B2 and
      compared with RUNS.json
  B4  criterion (b) early leaving recomputed from pupil records (exact)
  B5  the three candidate "two-peaked" objects are measured separately:
      tutoring expenditure, applications per selective place, years completed
"""
import math
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import common as C


def f(x):
    return float("nan") if x is None or str(x).strip() == "" else float(x)


def i(x):
    return int(float(x))


def cmp(actual, expected):
    """|actual - expected|; 0 when both are undefined (empty denominator)."""
    a, e = f(actual), (float("nan") if expected is None else float(expected))
    if math.isnan(a) and math.isnan(e):
        return 0.0
    if math.isnan(a) or math.isnan(e):
        return 1.0
    return abs(a - e) / max(1.0, abs(e))


THR_KEYS = {"unused": "coexistence_unused_share",
            "early": "coexistence_early_leave_share",
            "qpp": "coexistence_qualified_per_place",
            "ratio": "coexistence_gate_catchup_ratio",
            "gshare": "coexistence_gate_household_share"}


# ---------------------------------------------------------------------------
def check_arithmetic():
    bad = []
    n = 0
    for arm in C.ARMS:
        for r in C.coex_rows(arm):
            offers, dec = i(r["ordinary_secondary_offers"]), i(r["offers_declined"])
            app, qual = i(r["selective_applicants"]), i(r["selective_qualified"])
            places, adm = i(r["selective_places"]), i(r["selective_admitted"])
            away = i(r["selective_turned_away"])
            gh, gh_app = f(r["gate_hours_lower_final"]), i(r["lower_final_applicants"])
            ch, n_non = f(r["catchup_hours_total"]), i(r["non_selective_pupils"])
            ghh = i(r["gate_tutoring_households"])
            tests = {
                "unused": cmp(r["unused_accessible_share"], dec / offers if offers else None),
                "qpp": cmp(r["qualified_per_place"], qual / places if places else None),
                "gate_per_app": cmp(r["gate_hours_per_applicant"], gh / gh_app if gh_app else None),
                "catchup_per_non": cmp(r["catchup_hours_per_nonselective"], ch / n_non if n_non else None),
                "ratio": cmp(r["gate_to_catchup_ratio"],
                             (gh / gh_app) / (ch / n_non) if (gh_app and n_non and ch) else None),
                # the delivered column divides by the *tutoring-log* applicant count
                # (lower_final_applicants), not by the gate-log selective_applicants
                "gshare": cmp(r["gate_household_share"], ghh / gh_app if gh_app else None),
                "turned_away": away - (qual - adm),
                "admitted_le_places": max(0, adm - places),
                "qualified_le_applicants": max(0, qual - app),
            }
            for k, v in tests.items():
                n += 1
                if v is None:
                    continue
                if not (v == v) or v > C.TOL_IDENTITY:
                    bad.append((arm, int(r["seed"]), int(r["year"]), k, v))
    return dict(item="B1 coexistence arithmetic", n_values=n, n_violations=len(bad),
                tolerance=C.TOL_IDENTITY,
                verdict="PASS" if not bad else "FAIL"), bad


# ---------------------------------------------------------------------------
def evaluate_cells(cx_rows, coh_rows, P, arm):
    """Mirror of coexistence_verdict() in code/coevolve_v0.py."""
    thr = {k: float(P[v]) for k, v in THR_KEYS.items()}
    cx = {(int(r["seed"]), int(r["year"])): r for r in cx_rows}
    cells = []
    for r in coh_rows:
        seed, c = int(r["seed"]), int(r["cohort_entry_year"])
        early = f(r["left_secondary_early_share"])
        best = None
        for t in (c + 9, c + 10, c + 11):
            if not (0 <= t <= int(P["years"]) - 1):
                continue
            x = cx.get((seed, t))
            if x is None:
                continue
            a = f(x["unused_accessible_share"]) >= thr["unused"]
            bb = early >= thr["early"]
            cc = (f(x["qualified_per_place"]) >= thr["qpp"]) and i(x["selective_turned_away"]) > 0
            dd = ((f(x["gate_to_catchup_ratio"]) >= thr["ratio"])
                  and (f(x["gate_household_share"]) >= thr["gshare"]))
            rec = dict(seed=seed, cohort=c, year=t, a=a, b=bb, c=cc, d=dd,
                       all_four=(a and bb and cc and dd),
                       unused=f(x["unused_accessible_share"]), early=early,
                       qpp=f(x["qualified_per_place"]),
                       turned_away=i(x["selective_turned_away"]),
                       ratio=f(x["gate_to_catchup_ratio"]),
                       gshare=f(x["gate_household_share"]))
            if best is None or (rec["all_four"] and not best["all_four"]):
                best = rec
            if rec["all_four"]:
                break
        if best is not None:
            cells.append(best)
    return cells


def check_cells(P):
    runs = C.read_json("RUNS.json")
    delivered = {}
    for r in runs["runs"]:
        delivered[(r["arm"], r["seed"])] = bool(r["metrics"]["coexistence_all_four"])
    rows = []
    mismatch = []
    per_arm = {}
    for arm in C.ARMS:
        cx = C.coex_rows(arm)
        coh = C.cohort_rows(arm)
        for seed in C.SEEDS:
            cells = evaluate_cells([r for r in cx if i(r["seed"]) == seed],
                                   [r for r in coh if i(r["seed"]) == seed], P, arm)
            n_ok = sum(1 for c in cells if c["all_four"])
            per_arm[(arm, seed)] = dict(n_cells=len(cells), n_all_four=n_ok)
            if bool(n_ok) != delivered.get((arm, seed)):
                mismatch.append((arm, seed, n_ok, delivered.get((arm, seed))))
            for c in cells:
                rows.append(dict(arm=arm, **c))
    base = [k for k in per_arm if k[0] == "baseline"]
    base_ok = all(per_arm[k]["n_all_four"] > 0 for k in base)
    return dict(item="B2 four-criteria cell evaluation (declared thresholds)",
                n_cells=len(rows), n_cells_arms_seeds=len(per_arm),
                baseline_cells_all_four=[per_arm[k]["n_all_four"] for k in base],
                baseline_cells_total=[per_arm[k]["n_cells"] for k in base],
                baseline_any_all_four=base_ok,
                verdict_rule="COEXISTENT iff at least one baseline district x cohort cell has all four",
                n_verdict_mismatches=len(mismatch),
                verdict="PASS" if (not mismatch and base_ok) else "FAIL"), rows, per_arm, mismatch


def check_early_from_panel():
    bad = []
    n = 0
    worst = 0.0
    for arm in C.ARMS:
        panel = C.Panel(arm)
        for seed in C.SEEDS:
            rs = panel.seed_rows(seed)
            for r in [x for x in C.cohort_rows(arm) if i(x["seed"]) == seed]:
                c = i(r["cohort_entry_year"])
                d = [x for x in rs if x["_entry"] == c]
                ent = [x for x in d if x["_attended_secondary"]]
                val = (sum(1 for x in ent if x["_completed_lower_year"] < 0) / len(ent)
                       if ent else float("nan"))
                n += 1
                diff = abs(val - f(r["left_secondary_early_share"]))
                worst = max(worst, diff)
                if diff > C.TOL_EXACT:
                    bad.append((arm, seed, c, f(r["left_secondary_early_share"]), val))
    return dict(item="B4 early-leaving (criterion b) from pupil records", n_values=n,
                max_abs_diff=worst, n_disagreements=len(bad), tolerance=C.TOL_EXACT,
                verdict="PASS" if not bad else "FAIL"), bad


# ---------------------------------------------------------------------------
# B5 — what has two peaks: three separate objects
# ---------------------------------------------------------------------------
def two_peaks():
    P = C.Panel("baseline")
    yc = {}
    for r in P.rows:
        yc[r["_yc"]] = yc.get(r["_yc"], 0) + 1
    n = len(P.rows)
    top = sorted(yc.items(), key=lambda kv: -kv[1])
    yc_rows = [dict(object="years_completed", bucket=k, count=v, share=v / n)
               for k, v in sorted(yc.items())]

    gate = [r["_gate_hours"] for r in P.rows]
    catch = [r["_catchup_hours"] for r in P.rows]
    def dist(v):
        c = {}
        for x in v:
            k = round(x, 1)
            c[k] = c.get(k, 0) + 1
        return sorted(c.items())
    tut_rows = ([dict(object="gate_tutoring_hours_per_pupil", bucket=k, count=v,
                      share=v / len(gate)) for k, v in dist(gate)] +
                [dict(object="catchup_tutoring_hours_per_pupil", bucket=k, count=v,
                      share=v / len(catch)) for k, v in dist(catch)])

    # applications per selective place by year (baseline, mean over seeds)
    by = {}
    for r in C.coex_rows("baseline"):
        by.setdefault(i(r["year"]), []).append(f(r["qualified_per_place"]))
    series = [(t, sum(v) / len(v)) for t, v in sorted(by.items())]
    vals = [v for _, v in series]
    peaks = [(series[k][0], vals[k]) for k in range(1, len(vals) - 1)
             if vals[k] > vals[k - 1] and vals[k] > vals[k + 1]]
    # prominence: a peak counts only if it exceeds both neighbours by >= 0.15
    prominent = [(t, v) for t, v in peaks
                 if v - max(dict(series)[t - 1], dict(series)[t + 1]) >= 0.15]
    qpp_rows = [dict(object="applications_per_selective_place", bucket=t, count="",
                     share="", value=v) for t, v in series]

    measured = dict(
        years_completed_top_buckets=[dict(years=k, count=v, share=v / n) for k, v in top[:4]],
        years_completed_n_modes=len([1 for k, v in yc.items()
                                     if v > 0.05 * n]),
        gate_zero_share=sum(1 for x in gate if x == 0) / len(gate),
        gate_dose_modes=[k for k, v in dist(gate) if k > 0 and v > 0.01 * len(gate)],
        catchup_zero_share=sum(1 for x in catch if x == 0) / len(catch),
        catchup_dose_modes=[k for k, v in dist(catch) if k > 0 and v > 0.05 * len(catch)],
        qpp_min=min(vals), qpp_max=max(vals), qpp_first=vals[0], qpp_last=vals[-1],
        qpp_local_maxima=[(t, round(v, 3)) for t, v in peaks],
        qpp_prominent_maxima=[(t, round(v, 3)) for t, v in prominent],
    )
    return measured, yc_rows, tut_rows, qpp_rows


# ---------------------------------------------------------------------------
def main():
    P = C.params()
    checks = []
    c1, b1 = check_arithmetic()
    checks.append(c1)
    c2, cells, per_arm, mismatch = check_cells(P)
    checks.append(c2)
    c4, b4 = check_early_from_panel()
    checks.append(c4)
    measured, yc_rows, tut_rows, qpp_rows = two_peaks()
    checks.append(dict(item="B5 what has two peaks (measured separately)",
                       **measured, verdict="DESCRIPTIVE"))

    C.write_csv("B_coexistence_cells.csv",
                ["arm", "seed", "cohort_entry_year", "year_evaluated", "a_unused",
                 "b_early_leaving", "c_oversubscribed", "d_tutoring_concentrated",
                 "all_four", "unused_share", "early_leave_share", "qualified_per_place",
                 "turned_away", "gate_to_catchup_ratio", "gate_household_share"],
                [[c["arm"], c["seed"], c["cohort"], c["year"], int(c["a"]), int(c["b"]),
                  int(c["c"]), int(c["d"]), int(c["all_four"]),
                  "%.10g" % c["unused"], "%.10g" % c["early"], "%.10g" % c["qpp"],
                  c["turned_away"], "%.10g" % c["ratio"], "%.10g" % c["gshare"]]
                 for c in cells])
    C.write_csv("B_cell_counts.csv", ["arm", "seed", "n_cells", "n_all_four"],
                [[a, s, v["n_cells"], v["n_all_four"]] for (a, s), v in sorted(per_arm.items())])
    C.write_csv("B_two_peaks.csv", ["object", "bucket", "count", "share", "value"],
                [[r["object"], r["bucket"], r["count"],
                  ("%.6g" % r["share"]) if r.get("share") not in ("", None) else "",
                  ("%.6g" % r["value"]) if r.get("value") not in ("", None) else ""]
                 for r in (yc_rows + tut_rows + qpp_rows)])
    if b1 or b4 or mismatch:
        C.write_csv("B_disagreements.csv", ["arm", "seed", "key", "what", "a", "b"],
                    [[x[0], x[1], x[2], x[3], x[4], ""] for x in b1] +
                    [[x[0], x[1], x[2], "early_leaving", x[3], x[4]] for x in b4] +
                    [[x[0], x[1], "", "verdict", x[2], x[3]] for x in mismatch])
    C.write_json("B_summary.json", {"label": "SIMULATED", "checks": checks,
                                    "thresholds": {k: float(P[v]) for k, v in THR_KEYS.items()},
                                    "cells": {("%s|%d" % k): v for k, v in per_arm.items()}})
    for c in checks:
        print("%-60s %s" % (c["item"], c.get("verdict")))
        for k, v in c.items():
            if k not in ("item", "verdict"):
                print("    %-40s %s" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
