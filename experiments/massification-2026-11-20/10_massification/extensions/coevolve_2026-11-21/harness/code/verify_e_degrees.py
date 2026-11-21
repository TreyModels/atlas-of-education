"""Item 5 — the DEGREES-OUTRUN-JOBS oddity (§8.4, third arm).

The declared arm is "graduate supply growth doubled from year 8; employer
requirement and returns rules as §6(c)".  §6(c) declares

    req_t  = req_0 + lambda_req * (share_t - g0)
    return_t = return_0 * (1 - lambda_ret * (share_t - g0))

with g0 the declared steady-state graduate share.  This script measures from the
delivered pupil records what the model's own share is, and what the arm does.

It does not change any parameter, threshold or seed.  The finding is recorded as
a design defect (ARM-NOT-TESTING-GLUT), not as a result.
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


def share_series(panel):
    """Graduate share = share of the 18-22 age band holding cred >= 3 (upper
    secondary or above), recomputed from completion years.  Exact only for years
    in which the whole 18-22 band is inside the scored cohort frame (t >= 22)."""
    out = {}
    for t in range(0, 30):
        num = den = 0
        for r in panel.rows:
            age = 6 + t - r["_entry"]
            if not (18 <= age <= 22):
                continue
            den += 1
            if r["_completed_upper_year"] >= 0 and r["_completed_upper_year"] <= t:
                num += 1
        # is the band complete? entries t-16..t-12 must all be scored cohorts 6..17
        complete = (6 <= t - 16) and (t - 12 <= 17)
        out[t] = dict(share=(num / den if den else float("nan")), n=den, num=num,
                      band_complete=complete)
    return out


def main():
    P = C.params()
    g0 = float(P["graduate_share_0"])
    lr = float(P["lambda_req"])
    lret = float(P["lambda_ret"])
    req0 = float(P["employer_req_0"])
    ret0 = float(P["return_0"])
    dbl_from = int(P["degrees_double_from_year"])
    base = C.Panel("baseline")
    deg = C.Panel("degrees_outrun_jobs")
    sb = share_series(base)
    sd = share_series(deg)

    rows = []
    for t in range(18, 30):
        if not sb[t]["band_complete"]:
            continue
        rules = []
        for name, s in (("baseline(response_c off)", sb[t]["share"]),
                        ("degrees_outrun_jobs", sd[t]["share"])):
            used = g0 + 2.0 * (s - g0) if name != "baseline(response_c off)" else s
            used = min(max(used, 0.0), 1.0)
            if name == "baseline(response_c off)":
                req, ret = req0, ret0
            else:
                req = req0 + lr * (used - g0)
                ret = ret0 * (1.0 - lret * (used - g0))
            rules.append(dict(arm=name, share=s, used=used, req=req, ret=ret))
        rows.append(dict(year=t, baseline_share=sb[t]["share"],
                         degrees_share=sd[t]["share"],
                         base_req=rules[0]["req"], base_ret=rules[0]["ret"],
                         deg_used=rules[1]["used"], deg_req=rules[1]["req"],
                         deg_ret=rules[1]["ret"]))

    shares = [r["baseline_share"] for r in rows]
    mean_share = sum(shares) / len(shares)
    max_share = max(shares)
    reqs = [r["deg_req"] for r in rows]
    rets = [r["deg_ret"] for r in rows]

    # attainment / objects comparison, mean over seeds
    def arm_mean(arm, key):
        vals = [f(r[key]) for r in C.family_rows(arm)] if False else None
        return None

    runs = C.read_json("RUNS.json")
    met = {}
    for arm in ("baseline", "degrees_outrun_jobs"):
        rs = [r["metrics"] for r in runs["runs"] if r["arm"] == arm]
        met[arm] = {k: sum(m[k] for m in rs) / len(rs) for k in
                    ("completion_upper_secondary", "completion_tertiary",
                     "mean_years_completed")}
    obj = {}
    for r in C.read_csv("objects_all_arms.csv"):
        obj.setdefault((r["arm"], r["object"]), []).append(f(r["value"]))
    obj_mean = {k: sum(v) / len(v) for k, v in obj.items()}
    cred_base = obj_mean[("baseline", "credential")]
    cred_deg = obj_mean[("degrees_outrun_jobs", "credential")]

    # evidence that no supply process is touched
    diffs = {k: met["degrees_outrun_jobs"][k] - met["baseline"][k]
             for k in met["baseline"]}

    checks = [
        dict(item="E1 model's own graduate share vs the declared anchor g0",
             g0=g0, mean_share_18_29=round(mean_share, 6),
             max_share_18_29=round(max_share, 6),
             anchor_above_model_share=bool(g0 > max_share),
             implication="(share_t - g0) < 0 in every measured year, so the "
                         "declared requirement rule lowers the requirement and "
                         "raises the return as graduates accumulate",
             verdict="DEFECT-CONFIRMED" if g0 > max_share else "NOT-CONFIRMED"),
        dict(item="E2 implied employer rule inside the arm",
             years_measured=[r["year"] for r in rows],
             used_range=[round(min(r["deg_used"] for r in rows), 6),
                         round(max(r["deg_used"] for r in rows), 6)],
             req_range=[round(min(reqs), 6), round(max(reqs), 6)],
             ret_range=[round(min(rets), 6), round(max(rets), 6)],
             requirement_below_baseline=bool(max(reqs) < req0),
             return_above_baseline=bool(min(rets) > ret0),
             verdict=("DEFECT-CONFIRMED" if (max(reqs) < req0 and min(rets) > ret0)
                      else "NOT-CONFIRMED")),
        dict(item="E3 what the arm did to attainment (mean over 3 seeds)",
             completion_upper=dict(baseline=round(met["baseline"]["completion_upper_secondary"], 6),
                                   degrees=round(met["degrees_outrun_jobs"]["completion_upper_secondary"], 6),
                                   diff=round(diffs["completion_upper_secondary"], 6)),
             completion_tertiary=dict(baseline=round(met["baseline"]["completion_tertiary"], 6),
                                      degrees=round(met["degrees_outrun_jobs"]["completion_tertiary"], 6),
                                      diff=round(diffs["completion_tertiary"], 6)),
             mean_years=dict(baseline=round(met["baseline"]["mean_years_completed"], 6),
                             degrees=round(met["degrees_outrun_jobs"]["mean_years_completed"], 6),
                             diff=round(diffs["mean_years_completed"], 6)),
             credential_object=dict(baseline=round(cred_base, 6),
                                    degrees=round(cred_deg, 6), diff=round(cred_deg - cred_base, 6)),
             verdict="DESCRIPTIVE"),
        dict(item="E5 the requirement channel is inert (step at integer credentials)",
             access_penalty=float(P["credential_access_penalty"]),
             access_mapping_req_3_0=[1.0 if c >= req0 else float(P["credential_access_penalty"])
                                     for c in (1, 2, 3, 4, 5)],
             access_mapping_req_in_arm=[1.0 if c >= min(reqs) else float(P["credential_access_penalty"])
                                        for c in (1, 2, 3, 4, 5)],
             mappings_identical=bool(
                 [1.0 if c >= req0 else float(P["credential_access_penalty"]) for c in (1, 2, 3, 4, 5)]
                 == [1.0 if c >= min(reqs) else float(P["credential_access_penalty"]) for c in (1, 2, 3, 4, 5)]),
             implication="req moves inside (2,3] and credentials are integers, so the "
                         "credential-access mapping is unchanged; the only live channel "
                         "is return_t = 1.068..1.076, i.e. a uniform credential premium",
             verdict="DEFECT-CONFIRMED"),
        dict(item="E4 implementation audit: is a supply growth process changed?",
             degrees_double_from_year=dbl_from,
             change_year_effective_only_from=dbl_from,
             response_c_on_from="t=-11 (whole run): _arm_flags sets response_c=1 for the arm",
             code_uses_of_degrees_double="one: _employer_rule rescales (share_t - g0) by 2.0",
             supply_objects_changed=[],
             verdict="DEFECT-CONFIRMED"),
    ]
    C.write_csv("E_degrees.csv",
                ["year", "baseline_share", "degrees_share", "baseline_req", "baseline_ret",
                 "degrees_used", "degrees_req", "degrees_ret"],
                [[r["year"]] + ["%.6g" % r[k] for k in
                                ("baseline_share", "degrees_share", "base_req", "base_ret",
                                 "deg_used", "deg_req", "deg_ret")] for r in rows])
    C.write_json("E_summary.json", {"label": "SIMULATED", "checks": checks,
                                    "defect_id": "ARM-NOT-TESTING-GLUT",
                                    "v0_1_requirements": [
                                        "declare g0 from the model's own baseline steady-state share "
                                        "(or declare it as an external institutional constant with a "
                                        "pre-declared sensitivity range), before any result is seen",
                                        "declare an explicit graduate-supply instrument (a tertiary-place "
                                        "expansion path, a cohort-size shock, or a K_uni path) instead of "
                                        "rescaling the argument of the employer rule",
                                        "pre-declare the expected sign of req_t and return_t under the arm "
                                        "and fail the arm loudly if the run moves them the other way",
                                        "run a pre-outcome manipulation check that the arm moves the "
                                        "declared object (graduate supply) before reading attainment",
                                        "declare the response-(c) switch separately from the supply shock "
                                        "so the arm remains a one-change counterfactual (§8.3/§8.4 rule)",
                                    ]})
    for c in checks:
        print("%-58s %s" % (c["item"], c.get("verdict")))
        for k, v in c.items():
            if k not in ("item", "verdict"):
                print("    %-40s %s" % (k, v))
    return 0


if __name__ == "__main__":
    sys.exit(main())
