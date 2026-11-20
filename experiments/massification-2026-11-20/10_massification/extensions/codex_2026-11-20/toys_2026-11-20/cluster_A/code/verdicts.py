"""Evaluate the predeclared thresholds of Cluster A toys #1-#3.

ILLUSTRATIVE TOY - stipulated parameters; not calibrated; not evidence;
no historical test; phase closed; do not cite numbers as estimates.

Reads RESULTS_SUMMARY.json, applies the thresholds predeclared in
../PRE_DECLARATIONS.md mechanically, and writes verdicts.json.

"PASS" means only: the toy's output matches the pattern predeclared for the
toy. It is not evidence about any real education system.
"""

import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LABEL = ("ILLUSTRATIVE TOY - stipulated parameters; not calibrated; not evidence; "
         "no historical test; phase closed; do not cite numbers as estimates.")


def band(value, low, high):
    if value is None:
        return "undefined"
    if value < low:
        return "below"
    if value >= high:
        return "above"
    return "inside"


def main():
    summary_path = HERE.parent / "RESULTS_SUMMARY.json"
    with summary_path.open() as f:
        s = json.load(f)
    a1, a2, a3 = s["exp1"]["agg"], s["exp2"]["agg"], s["exp3"]["agg"]

    # ---- experiment 1 ------------------------------------------------------ #
    a_high = a1["lump.A_high"]
    a_low = a1["lump.A_low"]
    a_diff = a1["lump.A_diff"]
    t1a = a_high >= 1.25
    t1b = a_diff >= 0.25
    exp1 = dict(
        A_high=a_high, A_low=a_low, A_diff=a_diff,
        T1a="PASS" if t1a else "FAIL", T1a_rule="A_high >= 1.25",
        T1b="PASS" if t1b else "FAIL", T1b_rule="A_high - A_low >= 0.25",
        overall="PASS" if (t1a and t1b) else "FAIL",
        falsifier_triggered=bool(a_high <= 1.0 or (a_high < 1.25 and a_diff < 0.25)),
        band=band(a_high, 1.00, 1.25),
        robustness=dict(divisible_A_high=a1["divisible.A_high"],
                        divisible_A_low=a1["divisible.A_low"],
                        divisible_A_diff=a1["divisible.A_diff"]),
        mean_exit_seats_high=a1["lump.mean_exit_seats_high"],
        mean_entry_seats_high=a1["lump.mean_entry_seats_high"],
        share_exit_event_high=a1["lump_F_high_shock_down.share_exit_event"],
        share_entry_event_high=a1["lump_F_high_shock_up.share_entry_event"],
        mean_recovery_ratio_high_down=a1["lump_F_high_shock_down.mean_recovery_ratio"],
    )

    # ---- experiment 2 ------------------------------------------------------ #
    r_high = a2["cap15_F_high_exp30_50.R"]
    r_low = a2["cap15_F_low_exp30_50.R"]
    r_mid = a2["cap15_F_mid_exp30_50.R"]
    exit_share = a2["cap15_F_high_exp30_50.mean_private_exit_event"]
    t2a = r_high < 0.50
    t2b = r_low >= 0.50
    t2c = exit_share >= 0.50
    exp2 = dict(
        R_F_high_30_50=r_high, R_F_low_30_50=r_low, R_F_mid_30_50=r_mid,
        exit_share_F_high_30_50=exit_share,
        net_high=a2["cap15_F_high_exp30_50.mean_net_gain"],
        gross_high=a2["cap15_F_high_exp30_50.mean_gross_gain"],
        R_F_high_38_39=a2["cap15_F_high_exp38_39.R"],
        R_F_low_38_39=a2["cap15_F_low_exp38_39.R"],
        R_cap30_F_high_30_50=a2["cap30_F_high_exp30_50.R"],
        R_cap30_F_low_30_50=a2["cap30_F_low_exp30_50.R"],
        T2a="PASS" if t2a else "FAIL", T2a_rule="R(F_high, 30->50) < 0.50",
        T2b="PASS" if t2b else "FAIL", T2b_rule="R(F_low, 30->50) >= 0.50",
        T2c="PASS" if t2c else "FAIL", T2c_rule="exit share (F_high, 30->50) >= 0.50",
        overall="PASS" if (t2a and t2b and t2c) else "FAIL",
        falsifier_triggered=bool(r_high >= 0.90),
        band=band(r_high, 0.50, 0.90),
    )

    # ---- experiment 3 ------------------------------------------------------ #
    v4t = a3["L4_temp.mean_peak_vacancy"]
    v0t = a3["L0_temp.mean_peak_vacancy"]
    v2t = a3["L2_temp.mean_peak_vacancy"]
    v4p = a3["L4_perm.mean_peak_vacancy"]
    t3a = v4t >= 8.0
    t3b = v4t >= v0t + 4.0
    t3c = v4p < 4.0
    exp3 = dict(
        peak_vacancy={"L0_temp": v0t, "L2_temp": v2t, "L4_temp": v4t,
                      "L0_perm": a3["L0_perm.mean_peak_vacancy"],
                      "L2_perm": a3["L2_perm.mean_peak_vacancy"],
                      "L4_perm": v4p},
        peak_backlog={"L0_temp": a3["L0_temp.mean_peak_backlog"],
                      "L2_temp": a3["L2_temp.mean_peak_backlog"],
                      "L4_temp": a3["L4_temp.mean_peak_backlog"],
                      "L4_perm": a3["L4_perm.mean_peak_backlog"]},
        time_to_steady_state={"L0_temp": a3["L0_temp.mean_time_to_steady_state"],
                              "L2_temp": a3["L2_temp.mean_time_to_steady_state"],
                              "L4_temp": a3["L4_temp.mean_time_to_steady_state"],
                              "L0_perm": a3["L0_perm.mean_time_to_steady_state"],
                              "L2_perm": a3["L2_perm.mean_time_to_steady_state"],
                              "L4_perm": a3["L4_perm.mean_time_to_steady_state"]},
        censored={"L0_temp": a3["L0_temp.mean_censored"],
                  "L2_temp": a3["L2_temp.mean_censored"],
                  "L4_temp": a3["L4_temp.mean_censored"]},
        T3a="PASS" if t3a else "FAIL", T3a_rule="peak vacancy L4 temp >= 8.0",
        T3b="PASS" if t3b else "FAIL", T3b_rule="peak vacancy L4 temp >= L0 temp + 4.0",
        T3c="PASS" if t3c else "FAIL", T3c_rule="peak vacancy L4 perm < 4.0",
        overall="PASS" if (t3a and t3b and t3c) else "FAIL",
        falsifier_triggered=bool(v4t <= v0t + 2.0),
        monotone_temporary=bool(v4t >= v2t >= v0t),
        margin_note="T3a margin = {0:.2f} seats over the declared floor".format(v4t - 8.0),
    )

    out = dict(label=LABEL, seeds=s["seeds"], exp1=exp1, exp2=exp2, exp3=exp3)
    with (HERE.parent / "verdicts.json").open("w") as f:
        json.dump(out, f, indent=2, sort_keys=True)
        f.write("\n")
    print(json.dumps(out, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
