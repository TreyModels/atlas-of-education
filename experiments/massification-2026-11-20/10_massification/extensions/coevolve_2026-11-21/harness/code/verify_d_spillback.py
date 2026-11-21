"""Item 4 — re-verify the SPILLBACK experiment (§9) from the delivered tables.

The declared criterion: a spillback is present iff the treated-village
younger-cohort primary-persistence gain is >= 5 pp *relative to the
control-cohort-adjusted baseline*; falsifier: gain < 5 pp or negative.

The delivered table defines the control group by `panel["village"] !=
treated_village`, where `village` is a label ("v5", "town") and
`treated_village` is an integer.  The harness therefore recomputes the contrast
under four explicit control definitions and reports every one:

  D1 delivered   control = every row (the str/int comparison never excludes)
  D2 pure        control = non-treated villages only (town excluded)
  D3 excl-treated control = all rows except the treated village (town included)
  D4 vs baseline same villages/cohorts, spillback arm minus baseline arm

No threshold is changed.
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


def persistence(rows):
    sel = [r for r in rows if r["_years_attended"] > 0]
    if not sel:
        return float("nan"), 0
    return sum(1 for r in sel if r["_completed_primary_year"] >= 0) / len(sel), len(sel)


def masks(entry, y0):
    return (entry >= y0 + 3), ((entry >= 6) and entry < (y0 + 3))


def did(panel, seed, y0, tv, definition):
    young, old = masks(0, y0)
    rows = panel.seed_rows(seed)
    vlab = "v%d" % tv

    def group(rows_, grp):
        if grp == "treated":
            sel = [r for r in rows_ if r["village"] == vlab]
        elif definition == "delivered":
            sel = list(rows_)
        elif definition == "pure":
            sel = [r for r in rows_ if r["village"].startswith("v") and r["village"] != vlab]
        elif definition == "excl_treated":
            sel = [r for r in rows_ if r["village"] != vlab]
        else:
            raise ValueError(definition)
        return sel

    out = {}
    for grp in ("treated", "control"):
        for name, is_young in (("young", True), ("old", False)):
            sel = [r for r in group(rows, grp)
                   if masks(r["_entry"], y0)[0 if is_young else 1]]
            p, n = persistence(sel)
            out[(grp, name)] = (p, n)
    gain = ((out[("treated", "young")][0] - out[("treated", "old")][0])
            - (out[("control", "young")][0] - out[("control", "old")][0]))
    return out, gain


def main():
    P = C.params()
    y0 = int(P["spillback_year"])
    thr = float(P["spillback_gain_pp"])
    runs = C.read_json("RUNS.json")
    delivered = {r["seed"]: r["metrics"].get("spillback_did_pp")
                 for r in runs["runs"] if r["arm"] == "spillback"}
    deliv_tbl = C.read_csv("spillback_SPILLBACK.csv")
    sp = C.Panel("spillback")
    base = C.Panel("baseline")
    tv_by_seed = {}
    for r in deliv_tbl:
        tv_by_seed[i(r["seed"])] = i(r["treated_village"])

    # reproduce the delivered table from the panel
    tbl_bad = []
    for r in deliv_tbl:
        seed, grp, grpname = i(r["seed"]), r["group"], r["villages"]
        tv = tv_by_seed[seed]
        rows = [x for x in sp.seed_rows(seed)
                if masks(x["_entry"], y0)[0 if grp == "younger_cohorts" else 1]]
        if grpname == "treated_village":
            sel = [x for x in rows if x["village"] == "v%d" % tv]
        else:
            sel = list(rows)  # the delivered str/int comparison never excludes a row
        p, n = persistence(sel)
        if n != i(r["n_children"]) or abs(p - f(r["primary_persistence"])) > C.TOL_EXACT:
            tbl_bad.append((seed, grp, grpname, n, i(r["n_children"]), p, f(r["primary_persistence"])))

    results = []
    mism = []
    for seed in C.SEEDS:
        tv = tv_by_seed[seed]
        out_d, g_d = did(sp, seed, y0, tv, "delivered")
        out_p, g_p = did(sp, seed, y0, tv, "pure")
        out_e, g_e = did(sp, seed, y0, tv, "excl_treated")
        # D4: same treated village and cohorts, baseline arm instead of control villages
        bo = {}
        for grp in ("treated", "control"):
            for name, is_young in (("young", True), ("old", False)):
                sel = [r for r in base.seed_rows(seed)
                       if masks(r["_entry"], y0)[0 if is_young else 1]
                       and (r["village"] == "v%d" % tv if grp == "treated" else True)]
                bo[(grp, name)] = persistence(sel)[0]
        g_b = ((out_d[("treated", "young")][0] - out_d[("treated", "old")][0])
               - (bo[("control", "young")] - bo[("control", "old")]))
        results.append(dict(seed=seed, treated_village=tv,
                            did_delivered=g_d, did_pure=g_p, did_excl_treated=g_e,
                            did_vs_baseline=g_b, delivered_value=delivered[seed],
                            n_treated_young=out_d[("treated", "young")][1],
                            n_control_young=out_d[("control", "young")][1],
                            p_treated_young=out_d[("treated", "young")][0],
                            p_treated_old=out_d[("treated", "old")][0],
                            p_control_young=out_d[("control", "young")][0],
                            p_control_old=out_d[("control", "old")][0]))
        if delivered[seed] is not None and abs(g_d - delivered[seed]) > 1e-9:
            mism.append((seed, "delivered_did", g_d, delivered[seed]))

    def verdict(key):
        vals = [r[key] for r in results]
        return ("SPILLBACK-PRESENT" if all(v >= thr for v in vals) else "NO-SPILLBACK",
                sum(1 for v in vals if v >= thr), [round(v * 100, 2) for v in vals])

    v_del, n_del, pp_del = verdict("did_delivered")
    v_pure, n_pure, pp_pure = verdict("did_pure")
    v_base, n_base, pp_base = verdict("did_vs_baseline")

    # district-wide effect of the response-(b) switch in the spillback arm
    district = []
    for seed in C.SEEDS:
        tv = tv_by_seed[seed]
        for grp in ("young", "old"):
            m = masks(0, y0)[0 if grp == "young" else 1]
            sel_b = [r for r in base.seed_rows(seed) if masks(r["_entry"], y0)[0 if grp == "young" else 1]
                     and r["village"].startswith("v") and r["village"] != "v%d" % tv]
            sel_s = [r for r in sp.seed_rows(seed) if masks(r["_entry"], y0)[0 if grp == "young" else 1]
                     and r["village"].startswith("v") and r["village"] != "v%d" % tv]
            district.append(dict(seed=seed, group=grp,
                                 baseline=persistence(sel_b)[0],
                                 spillback=persistence(sel_s)[0]))

    checks = [
        dict(item="D1 delivered spillback table reproduced from panel",
             n_rows=len(deliv_tbl), n_disagreements=len(tbl_bad), tolerance=C.TOL_EXACT,
             verdict="PASS" if not tbl_bad else "FAIL"),
        dict(item="D2 DiD recomputed (delivered control definition)",
             per_seed_pp=pp_del, n_seeds_ge_threshold=n_del,
             mean_pp=round(sum(pp_del) / 3, 3),
             delivered_run_values=[round(x * 100, 4) for x in delivered.values()],
             n_value_mismatches=len(mism),
             verdict="PASS" if not mism else "FAIL"),
        dict(item="D3 verdict under each control definition",
             delivered=dict(verdict=v_del, seeds_clearing=n_del, pp=pp_del),
             pure_villages=dict(verdict=v_pure, seeds_clearing=n_pure, pp=pp_pure),
             excl_treated=dict(verdict=verdict("did_excl_treated")[0],
                               seeds_clearing=verdict("did_excl_treated")[1],
                               pp=verdict("did_excl_treated")[2]),
             vs_baseline_arm=dict(verdict=v_base, seeds_clearing=n_base, pp=pp_base),
             threshold_pp=thr * 100,
             rule="present iff every paired seed >= 5 pp (code: all(...))",
             verdict=("PASS-CONSISTENT" if v_del == v_pure == v_base == "NO-SPILLBACK" else "FAIL")),
        dict(item="D4 response-(b) switch moves persistence district-wide",
             control_village_primary_persistence=district,
             verdict="DESCRIPTIVE"),
    ]

    C.write_csv("D_spillback.csv",
                ["seed", "treated_village", "did_delivered_pp", "did_pure_pp",
                 "did_excl_treated_pp", "did_vs_baseline_pp", "delivered_run_value",
                 "n_treated_young", "n_control_young", "p_treated_young",
                 "p_treated_old", "p_control_young", "p_control_old"],
                [[r["seed"], r["treated_village"]] +
                 ["%.6f" % (r[k] * 100) for k in ("did_delivered", "did_pure",
                                                  "did_excl_treated", "did_vs_baseline")] +
                 ["%.6f" % r["delivered_value"], r["n_treated_young"], r["n_control_young"],
                  "%.6g" % r["p_treated_young"], "%.6g" % r["p_treated_old"],
                  "%.6g" % r["p_control_young"], "%.6g" % r["p_control_old"]]
                 for r in results])
    C.write_csv("D_district_switch.csv",
                ["seed", "group", "baseline_persistence", "spillback_persistence"],
                [[d["seed"], d["group"], "%.6g" % d["baseline"], "%.6g" % d["spillback"]]
                 for d in district])
    C.write_json("D_summary.json", {"label": "SIMULATED", "checks": checks,
                                    "rows": [{k: (None if isinstance(v, float) and v != v else v)
                                              for k, v in r.items()} for r in results],
                                    "delivered_table_mismatches": tbl_bad})
    for c in checks:
        print("%-58s %s" % (c["item"], c.get("verdict")))
        for k, v in c.items():
            if k not in ("item", "verdict"):
                print("    %-40s %s" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
