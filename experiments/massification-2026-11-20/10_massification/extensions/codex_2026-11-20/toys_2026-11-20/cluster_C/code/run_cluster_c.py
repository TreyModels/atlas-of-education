"""Run the three Cluster C toys (#7, #8, #9) and evaluate the pre-declared thresholds.

ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.

Writes RESULTS.csv (long format, all cells including failures), code/parameters.json
and a human-readable verdict table on stdout. Thresholds are the constants below,
frozen in PRE_DECLARATIONS.md before this run; they are evaluated mechanically and
never adjusted to the observed numbers.
"""

import csv
import json
import math
import platform
import statistics
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import cluster_c_model as M  # noqa: E402

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
RESULTS = ROOT / "RESULTS.csv"

SEEDS = [20261120 + k for k in range(200)]          # 200 seeds per cell, pre-declared
NSEED = len(SEEDS)
assert NSEED >= 100

# ---- pre-declared thresholds (see PRE_DECLARATIONS.md sections 1–3) --------
T7_FLOOR_GAIN = 10.0        # pp, primary_only vs control
T7_CEIL_GAIN = 2.0          # pp, tertiary_only vs control
T7_MID_GAIN = 3.0           # pp, secondary_only vs control
T7_MID_SEAT_SHARE = 8.33    # pp, 50% of the imposed secondary added-seat share
T7_CEIL_VS_FLOOR = 0.25     # ceiling gain <= 0.25 * floor gain (primary_only)
T7_NO_UNIVERSAL = 50.0      # pp, ceiling share bar for "no ceiling universalization"
T7_UNIVERSAL = 90.0         # pp, universalization bar at any level
T7_BINDING = 0.75           # control utilization required to evaluate own-level claims

T8_INERT_ATT = 2.0          # pp, |attendance gain| at law_e0
T8_INERT_COMP = 1.0         # pp, completion gain at law_e0
T8_BIND_ATT = 10.0          # pp, attendance gain at law_e1
T8_BIND_COMP = 6.0          # pp, completion gain at law_e1
T8_RATIO = 4.0              # gain(e=1) / gain(e=0)
T8_GAP = 8.0                # pp, gain(e=1) - gain(e=0)

T9_ROOMS_PHYS = 30.0        # physical places gain, rooms_only
T9_ROOMS_STAFF = 2.0        # staffed places gain allowed
T9_ROOMS_COMP = 1.0         # pp, completion gain allowed
T9_SPLIT_STAFF = 20.0       # staffed places, split - rooms_only
T9_SPLIT_COMP = 5.0         # pp, split - rooms_only
T9_SPLIT_TEACH = 3.0        # pp, split - teachers_only
T9_COMP_SHARE = 0.70        # teachers_only gain <= 0.70 * split gain
T9_RETENTION = 2.0          # pp, split(high) - split(low)

ROWS = []


def fmt(x):
    return f"{x:.6f}"


def row(experiment, arm, scope, metric, value, sd=None, lo=None, hi=None,
        unit="", status="ok", definition=""):
    ROWS.append({
        "experiment": experiment, "arm": arm, "scope": scope, "metric": metric,
        "value": fmt(value),
        "sd": "" if sd is None else fmt(sd),
        "ci95_low": "" if lo is None else fmt(lo),
        "ci95_high": "" if hi is None else fmt(hi),
        "n_seeds": NSEED, "unit": unit, "status": status,
        "definition": definition, "label": M.LABEL,
    })


def stats(values):
    n = len(values)
    mean = statistics.fmean(values)
    sd = statistics.stdev(values) if n > 1 else 0.0
    half = 1.96 * sd / math.sqrt(n) if n > 1 else 0.0
    return mean, sd, mean - half, mean + half


def paired(ref, arm):
    diffs = [a - b for a, b in zip(arm, ref)]
    mean, sd, lo, hi = stats(diffs)
    pos = sum(1 for d in diffs if d > 1e-12) / len(diffs)
    neg = sum(1 for d in diffs if d < -1e-12) / len(diffs)
    return {"mean": mean, "sd": sd, "lo": lo, "hi": hi, "pos": pos, "neg": neg,
            "diffs": diffs}


def verdict(tid, ok, observed, text, extra="", kind="threshold"):
    """ok=True means the pre-declared criterion is met.

    kind="falsifier": ok=True means the falsifier FIRED (i.e. the toy contradicts
    the A10-style reading). Printed as FIRED / not_fired so that "PASS" is never
    shown for a falsifier firing.
    """
    if kind == "falsifier":
        status = "FIRED" if ok else "not_fired"
        shown = "FIRED " if ok else "clear "
    else:
        status = "PASS" if ok else "FAIL"
        shown = "PASS" if ok else "FAIL"
    row("verdicts", "threshold", "all", tid, 1.0 if ok else 0.0, unit="bool",
        status=status,
        definition=f"{text} | observed: {observed}{(' | ' + extra) if extra else ''}")
    print(f"  {shown:5s} {tid}: {observed}")
    return ok


# ==========================================================================
# Experiment 7 — capacity by level
# ==========================================================================
EXP7 = "7_capacity_by_level"


def exp7():
    print("\n[7] capacity by level — 200 seeds x 5 arms")
    per_arm = {}
    for arm in M.ARMS_7:
        per_arm[arm] = [M.level_seed_metrics(M.run_level_capacity(s, arm)) for s in SEEDS]
    ctl = per_arm["control"]

    metrics = ["seats_primary", "seats_secondary", "seats_tertiary",
               "applications_primary", "applications_secondary", "applications_tertiary",
               "completions_primary", "completions_secondary", "completions_tertiary",
               "utilization_primary", "utilization_secondary", "utilization_tertiary",
               "floor_pp", "middle_pp", "ceiling_pp", "floor_minus_ceiling_pp",
               "ceiling_over_floor"]
    for arm, series in per_arm.items():
        for m in metrics:
            mean, sd, lo, hi = stats([r[m] for r in series])
            row(EXP7, arm, "cohort_30", m, mean, sd, lo, hi,
                unit="places" if m.startswith(("seats", "applications", "completions")) else
                ("ratio" if m.startswith(("utilization", "ceiling_over_floor")) else "pp"),
                definition="seed mean at cohort 30; paired draws across arms")
        for bar in M.CROSS_BARS:
            for lvl in M.LEVELS:
                m = f"cross_{lvl}_{int(bar * 100)}"
                vals = [r[m] for r in series]
                mean = statistics.fmean(vals)
                cens = sum(1 for v in vals if v >= M.CENSORED_YEAR) / len(vals)
                status = "censored" if cens > 0.5 else "ok"
                row(EXP7, arm, "crossing", m, mean, unit="cohort", status=status,
                    definition=f"first cohort with {lvl} completion share >= {bar:.2f}; "
                                f"{M.COHORTS + 1}=censored (>30); censored share={cens:.3f}")

    # paired contrasts vs control
    deltas = {}
    for arm in ("primary_only", "secondary_only", "tertiary_only", "all_levels"):
        for lvl in M.LEVELS:
            d = paired([r[f"share_{lvl}_pp"] for r in ctl],
                       [r[f"share_{lvl}_pp"] for r in per_arm[arm]])
            deltas[(arm, lvl)] = d
            row(EXP7, arm, "contrast_vs_control", f"gain_{lvl}_pp", d["mean"], d["sd"],
                d["lo"], d["hi"], unit="pp",
                definition=f"paired {arm} minus control, {lvl} completion share at cohort 30; "
                           f"sign_share+={d['pos']:.3f}")
        d = paired([r["floor_minus_ceiling_pp"] for r in ctl],
                   [r["floor_minus_ceiling_pp"] for r in per_arm[arm]])
        row(EXP7, arm, "contrast_vs_control", "gain_floor_minus_ceiling_pp",
            d["mean"], d["sd"], d["lo"], d["hi"], unit="pp",
            definition="paired change in the floor minus ceiling gap")
        fg = deltas[(arm, "primary")]["mean"]
        row(EXP7, arm, "contrast_vs_control", "ceiling_gain_over_floor_gain",
            (deltas[(arm, "tertiary")]["mean"] / fg) if abs(fg) > 1e-12 else 0.0,
            unit="ratio",
            status="ok" if abs(fg) > 1e-12 else "undefined_no_floor_gain",
            definition="paired mean ceiling gain divided by mean floor gain; "
                       "undefined (reported 0) when the arm does not move the floor")

    # binding precondition
    bind = {lvl: statistics.fmean([r[f"utilization_{lvl}"] for r in ctl])
            for lvl in M.LEVELS}
    for lvl in M.LEVELS:
        row(EXP7, "control", "binding_check", f"control_utilization_{lvl}", bind[lvl],
            unit="ratio", status="binding" if bind[lvl] >= T7_BINDING else "NOT_BINDING",
            definition=f"control completions/seats at cohort 30; binding if >= {T7_BINDING}")

    # level trajectories: seed-mean completion share by cohort, per arm and level
    ceil_curve = {}
    level_curves = {}
    for arm in M.ARMS_7:
        hist_by_seed = [M.run_level_capacity(s, arm) for s in SEEDS]
        level_curves[arm] = [
            [statistics.fmean([h[t][k]["completions"] / M.N for h in hist_by_seed])
             for t in range(M.COHORTS)] for k in range(3)]
        ceil_curve[arm] = level_curves[arm][2]
        row(EXP7, arm, "trajectory", "max_ceiling_share_pp", 100.0 * max(ceil_curve[arm]),
            unit="pp", definition="max over cohorts 1-30 of the seed-mean tertiary share")
        for k in range(3):
            row(EXP7, arm, "trajectory", f"max_{M.LEVELS[k]}_share_pp",
                100.0 * max(level_curves[arm][k]), unit="pp",
                definition=f"max over cohorts 1-30 of the seed-mean {M.LEVELS[k]} share")

    floor_gain = deltas[("primary_only", "primary")]
    ceil_gain_primary = deltas[("primary_only", "tertiary")]
    mid_gain = deltas[("secondary_only", "secondary")]
    ceil_gain_tertiary = deltas[("tertiary_only", "tertiary")]

    t7a = (floor_gain["mean"] >= T7_FLOOR_GAIN) and (floor_gain["lo"] > 0) and \
          bind["primary"] >= T7_BINDING
    verdict("T7a", t7a, f"floor gain {floor_gain['mean']:+.2f} pp "
                        f"[{floor_gain['lo']:+.2f},{floor_gain['hi']:+.2f}] "
                        f"(need >= +{T7_FLOOR_GAIN} pp, CI>0, binding={bind['primary']:.2f})",
            "primary_only raises the floor by >= +10.0 pp, CI excluding 0")
    t7b = (ceil_gain_tertiary["mean"] >= T7_CEIL_GAIN) and (ceil_gain_tertiary["lo"] > 0) and \
          bind["tertiary"] >= T7_BINDING
    verdict("T7b", t7b, f"tertiary_only ceiling gain {ceil_gain_tertiary['mean']:+.2f} pp "
                        f"[{ceil_gain_tertiary['lo']:+.2f},{ceil_gain_tertiary['hi']:+.2f}] "
                        f"(need >= +{T7_CEIL_GAIN}, binding={bind['tertiary']:.2f})",
            "tertiary_only raises the ceiling by >= +2.0 pp")
    t7c = (mid_gain["mean"] >= T7_MID_GAIN) and (mid_gain["mean"] < T7_MID_SEAT_SHARE) and \
          bind["secondary"] >= T7_BINDING
    verdict("T7c", t7c, f"secondary_only middle gain {mid_gain['mean']:+.2f} pp "
                        f"(need in [+{T7_MID_GAIN}, +{T7_MID_SEAT_SHARE}) of a +16.67 pp seat shock; "
                        f"binding={bind['secondary']:.2f})",
            "secondary_only raises the middle by >= +3.0 pp but converts < 50% of added seats")
    t7d = (ceil_gain_primary["mean"] <= T7_CEIL_GAIN) and \
          (ceil_gain_primary["mean"] <= T7_CEIL_VS_FLOOR * floor_gain["mean"])
    verdict("T7d", t7d, f"primary_only ceiling gain {ceil_gain_primary['mean']:+.2f} pp "
                        f"= {ceil_gain_primary['mean'] / floor_gain['mean']:.3f} x floor gain",
            "primary_only: ceiling gain <= +2.0 pp and <= 0.25 x floor gain")
    # T7e is evaluated as literally worded: clause (i) ceiling share < 50 pp anywhere,
    # clause (ii) no arm reaches the 90 pp universalization bar at ANY level.
    max_ceil = max(max(c) for c in ceil_curve.values()) * 100.0
    max_any = max(100.0 * max(level_curves[a][k]) for a in M.ARMS_7 for k in range(3))
    t7e_i = max_ceil < T7_NO_UNIVERSAL
    t7e_ii = max_any < T7_UNIVERSAL
    row(EXP7, "all", "threshold_clause", "T7e_i_ceiling_below_50pp", 1.0 if t7e_i else 0.0,
        unit="bool", status="PASS" if t7e_i else "FAIL",
        definition=f"max seed-mean ceiling share {max_ceil:.2f} pp < {T7_NO_UNIVERSAL:.0f} pp")
    row(EXP7, "all", "threshold_clause", "T7e_ii_no_level_at_90pp", 1.0 if t7e_ii else 0.0,
        unit="bool", status="PASS" if t7e_ii else "FAIL",
        definition=f"max seed-mean share at ANY level {max_any:.2f} pp < {T7_UNIVERSAL:.0f} pp")
    verdict("T7e", t7e_i and t7e_ii,
            f"clause (i) ceiling max {max_ceil:.2f} pp < 50 -> {t7e_i}; "
            f"clause (ii) any-level max {max_any:.2f} pp < 90 -> {t7e_ii}",
            "no arm reaches ceiling share >= 50 pp AND no arm reaches the 90 pp universalization "
            "bar at any level (literal wording; both clauses reported separately)")
    cross_floor = [r["cross_primary_50"] for r in per_arm["primary_only"]]
    floor_obs = sum(1 for v in cross_floor if v < M.CENSORED_YEAR) / len(cross_floor)
    ceil_obs_all = [sum(1 for v in [r["cross_tertiary_50"] for r in per_arm[a]]
                        if v < M.CENSORED_YEAR) / NSEED for a in M.ARMS_7]
    t7f = floor_obs >= 0.5 and max(ceil_obs_all) < 0.5
    verdict("T7f", t7f, f"floor 0.50 crossing observed in {floor_obs:.2f} of seeds; "
                        f"max ceiling-crossing share over arms {max(ceil_obs_all):.2f}",
            "floor crosses 0.50 in primary_only while the ceiling 0.50 crossing is censored everywhere")

    # falsifiers (F7 applicability: see PRE_DECLARATIONS.md deviation #1)
    single = ("primary_only", "secondary_only", "tertiary_only")
    f7_eligible = [a for a in single if deltas[(a, "primary")]["mean"] >= 2.0]
    f7_a = [a for a in f7_eligible
            if deltas[(a, "tertiary")]["mean"] >= deltas[(a, "primary")]["mean"]]
    f7_b = max_ceil >= T7_UNIVERSAL
    verdict("F7", f7_a or f7_b,
            f"floor-moving arms {f7_eligible}; of these, ceiling gain >= floor gain: "
            f"{f7_a or 'none'}; ceiling universalization: {f7_b}",
            "FALSIFIER (fires => contradicts A10): in a single-level arm that moves the floor "
            "(floor gain >= +2 pp), ceiling gain >= floor gain; or ceiling universalization",
            kind="falsifier")
    return per_arm, deltas, bind, ceil_curve


# ==========================================================================
# Experiment 8 — enforcement x compulsory law
# ==========================================================================
EXP8 = "8_law_enforcement"


def exp8():
    print("\n[8] enforcement x compulsory law — 200 seeds x 6 cells")
    cells = list(M.LAW_CELLS)
    per_cell = {c: [M.run_law(s, c) for s in SEEDS] for c in cells}
    metrics = ["registration_pp", "attendance_pp", "completion_pp",
               "registration_n", "attendance_n", "completion_n",
               "mean_household_work", "sanction_exposure"]
    for c in cells:
        law, enf = M.LAW_CELLS[c]
        for m in metrics:
            mean, sd, lo, hi = stats([r[m] for r in per_cell[c]])
            row(EXP8, f"{c}", f"law={law},e={enf}", m, mean, sd, lo, hi,
                unit="pp" if m.endswith("_pp") else ("children" if m.endswith("_n") else "units"),
                definition=f"de jure law={law}, declared enforcement={enf}; seed mean")
    deltas = {}
    for c in cells:
        if c == "no_law":
            continue
        for m in ("attendance_pp", "completion_pp", "registration_pp", "mean_household_work"):
            d = paired([r[m] for r in per_cell["no_law"]], [r[m] for r in per_cell[c]])
            deltas[(c, m)] = d
            row(EXP8, c, "contrast_vs_no_law", f"gain_{m}", d["mean"], d["sd"], d["lo"], d["hi"],
                unit="pp" if m.endswith("_pp") else "units",
                definition=f"paired {c} minus no_law; sign_share+={d['pos']:.3f}")

    att0 = deltas[("law_e0", "attendance_pp")]
    cmp0 = deltas[("law_e0", "completion_pp")]
    att5 = deltas[("law_e05", "attendance_pp")]
    att1 = deltas[("law_e1", "attendance_pp")]
    cmp1 = deltas[("law_e1", "completion_pp")]
    work0 = deltas[("law_e0", "mean_household_work")]
    work1 = deltas[("law_e1", "mean_household_work")]

    t8a = abs(att0["mean"]) <= T8_INERT_ATT and cmp0["mean"] <= T8_INERT_COMP
    verdict("T8a", t8a, f"law_e0: attendance {att0['mean']:+.2f} pp "
                        f"[{att0['lo']:+.2f},{att0['hi']:+.2f}], completion {cmp0['mean']:+.2f} pp "
                        f"[{cmp0['lo']:+.2f},{cmp0['hi']:+.2f}] "
                        f"(need |att| <= {T8_INERT_ATT}, comp <= +{T8_INERT_COMP})",
            "paper law is inert in the classroom (equivalence band)")
    t8b = att1["mean"] >= T8_BIND_ATT and cmp1["mean"] >= T8_BIND_COMP
    verdict("T8b", t8b, f"law_e1: attendance {att1['mean']:+.2f} pp, completion {cmp1['mean']:+.2f} pp "
                        f"(need >= +{T8_BIND_ATT} and >= +{T8_BIND_COMP})",
            "enforced law binds: attendance >= +10 pp and completion >= +6 pp")
    monotone = att0["mean"] <= att5["mean"] <= att1["mean"]
    ratio = (att1["mean"] / att0["mean"]) if att0["mean"] > 0 else float("inf")
    gap = att1["mean"] - att0["mean"]
    t8c = monotone and ratio >= T8_RATIO and gap >= T8_GAP
    verdict("T8c", t8c, f"gains e0/e0.5/e1 = {att0['mean']:+.2f}/{att5['mean']:+.2f}/{att1['mean']:+.2f} pp, "
                        f"ratio {ratio:.2f}x, gap {gap:+.2f} pp",
            "enforcement gates the law: monotone in e, gain(e1) >= 4x gain(e0), gap >= +8 pp")
    ratio_work = (work1["mean"] / work0["mean"]) if abs(work0["mean"]) > 1e-12 else float("inf")
    verdict("T8d", ratio_work >= 3.0,
            f"household-work reduction e1/e0 = {ratio_work:.2f}x "
            f"({work0['mean']:+.4f} vs {work1['mean']:+.4f} units)",
            "mechanism-consistency diagnostic: work falls only where attendance rises")
    f8 = abs(att0["mean"]) > T8_INERT_ATT
    verdict("F8", f8, f"law_e0 attendance gain {att0['mean']:+.2f} pp "
                      f"(fires if > {T8_INERT_ATT} pp)",
            "FALSIFIER (fires => enforcement leg redundant): law alone binds", kind="falsifier")

    # built-in null: enforcement without a law
    for c in ("no_law_e05", "no_law_e1"):
        d_att = paired([r["attendance_pp"] for r in per_cell["no_law"]],
                       [r["attendance_pp"] for r in per_cell[c]])
        row(EXP8, c, "built_in_null", "attendance_gain_pp", d_att["mean"], d_att["sd"],
            d_att["lo"], d_att["hi"], unit="pp",
            definition="enforcement without a statute: expected exactly 0 by construction")
    return per_cell, deltas


# ==========================================================================
# Experiment 9 — buildings vs teachers at equal budget
# ==========================================================================
EXP9 = "9_buildings_vs_teachers"


def exp9():
    print("\n[9] buildings vs teachers at equal budget — 200 seeds x 8 cells")
    cells = [(a, r) for a in M.ALLOC for r in M.RETENTION]
    per_cell = {(a, r): [M.run_budget(s, a, r) for s in SEEDS] for a, r in cells}
    metrics = ["physical_places", "admissions_staffed", "completions_n", "completion_pp",
               "ptr_declared", "ptr_effective", "teacher_load", "budget_spent"]
    for (a, r) in cells:
        for m in metrics:
            mean, sd, lo, hi = stats([x[m] for x in per_cell[(a, r)]])
            row(EXP9, f"{a}__retention_{r}", f"alloc={a},pi={M.RETENTION[r]}", m,
                mean, sd, lo, hi,
                unit="pp" if m.endswith("_pp") else ("places" if "places" in m or "staffed" in m
                                                     else ("ratio" if m.startswith("ptr") or "load" in m
                                                           else "children")),
                definition=f"{a} at retention pi={M.RETENTION[r]}; rooms+{M.ALLOC[a][0]*M.ROOM_COST}"
                            f"+posts {M.ALLOC[a][1]*M.TEACHER_COST} = {M.BUDGET}")

    deltas = {}
    for r in M.RETENTION:
        base = per_cell[("baseline", r)]
        for a in ("rooms_only", "teachers_only", "split"):
            for m in ("admissions_staffed", "completion_pp", "physical_places",
                      "ptr_declared", "ptr_effective"):
                d = paired([x[m] for x in base], [x[m] for x in per_cell[(a, r)]])
                deltas[(a, r, m)] = d
                row(EXP9, f"{a}__retention_{r}", "contrast_vs_baseline", f"gain_{m}",
                    d["mean"], d["sd"], d["lo"], d["hi"], unit="pp" if m.endswith("_pp") else "places",
                    definition=f"paired {a} minus baseline at pi={M.RETENTION[r]}")
        for a in ("rooms_only", "teachers_only"):
            for m in ("admissions_staffed", "completion_pp", "physical_places"):
                d = paired([x[m] for x in per_cell[(a, r)]], [x[m] for x in per_cell[("split", r)]])
                deltas[("split_minus_" + a, r, m)] = d
                row(EXP9, f"split__retention_{r}", f"contrast_vs_{a}", f"gain_{m}",
                    d["mean"], d["sd"], d["lo"], d["hi"],
                    unit="pp" if m.endswith("_pp") else "places",
                    definition=f"paired split minus {a} at pi={M.RETENTION[r]}")
    for a in ("baseline", "rooms_only", "teachers_only", "split"):
        d = paired([x["completion_pp"] for x in per_cell[(a, "low")]],
                   [x["completion_pp"] for x in per_cell[(a, "high")]])
        deltas[(a, "retention", "completion_pp")] = d
        row(EXP9, f"{a}__retention_delta", "retention_high_minus_low", "gain_completion_pp",
            d["mean"], d["sd"], d["lo"], d["hi"], unit="pp",
            definition="paired high-retention minus low-retention completion; teacher-constrained "
                       "arms should gain, rooms_only should not")

    ok_all = True
    for r in M.RETENTION:
        phys = deltas[("rooms_only", r, "physical_places")]["mean"]
        staff = deltas[("rooms_only", r, "admissions_staffed")]["mean"]
        comp = deltas[("rooms_only", r, "completion_pp")]["mean"]
        ok = (phys >= T9_ROOMS_PHYS) and (staff <= T9_ROOMS_STAFF) and (comp <= T9_ROOMS_COMP)
        ok_all = ok_all and ok
        verdict(f"T9a[{r}]", ok, f"rooms_only pi={M.RETENTION[r]}: physical {phys:+.0f}, "
                                 f"staffed {staff:+.2f}, completion {comp:+.2f} pp",
                "rooms without staff: physical >= +30 but staffed <= +2 and completion <= +1 pp")
    ok_b = True
    for r in M.RETENTION:
        staff = deltas[("split_minus_rooms_only", r, "admissions_staffed")]["mean"]
        comp = deltas[("split_minus_rooms_only", r, "completion_pp")]["mean"]
        ok = staff >= T9_SPLIT_STAFF and comp >= T9_SPLIT_COMP
        ok_b = ok_b and ok
        verdict(f"T9b[{r}]", ok, f"split - rooms_only pi={M.RETENTION[r]}: staffed {staff:+.2f}, "
                                 f"completion {comp:+.2f} pp",
                "split dominates rooms at equal budget: staffed >= +20, completion >= +5 pp")
    ok_c = True
    for r in M.RETENTION:
        d_teach = deltas[("split_minus_teachers_only", r, "completion_pp")]["mean"]
        g_split = deltas[("split", r, "completion_pp")]["mean"]
        g_teach = deltas[("teachers_only", r, "completion_pp")]["mean"]
        share = (g_teach / g_split) if g_split > 0 else float("inf")
        ok = d_teach >= T9_SPLIT_TEACH and share <= T9_COMP_SHARE
        ok_c = ok_c and ok
        verdict(f"T9c[{r}]", ok, f"split - teachers_only pi={M.RETENTION[r]}: completion "
                                 f"{d_teach:+.2f} pp; teachers/split gain share {share:.2f}",
                "composition matters: split - teachers_only >= +3 pp and teachers' gain <= 70% of split's")
    d_split = deltas[("split", "retention", "completion_pp")]["mean"]
    d_teach = deltas[("teachers_only", "retention", "completion_pp")]["mean"]
    d_base = deltas[("baseline", "retention", "completion_pp")]["mean"]
    d_rooms = deltas[("rooms_only", "retention", "completion_pp")]["mean"]
    t9d = (d_split >= T9_RETENTION and abs(d_teach) <= T9_RETENTION
           and d_base >= T9_RETENTION and d_rooms >= T9_RETENTION)
    verdict("T9d", t9d, f"retention gain: split {d_split:+.2f}, teachers_only {d_teach:+.2f}, "
                        f"baseline {d_base:+.2f}, rooms_only {d_rooms:+.2f} pp",
            "retention binds only where teachers bind: split (+), teachers_only (0), teacher-constrained "
            "arms (+)")
    f9 = False
    for r in M.RETENTION:
        if deltas[("rooms_only", r, "completion_pp")]["mean"] > T9_ROOMS_COMP:
            f9 = True
    verdict("F9", f9, f"rooms_only completion gain > {T9_ROOMS_COMP} pp in any retention cell: {f9}",
            "FALSIFIER (fires => rooms alone produce completions): composition irrelevant",
            kind="falsifier")
    return per_cell, deltas


def main():
    banner = ("=" * 78) + "\n" + M.LABEL + "\n" + ("=" * 78)
    print(banner)
    t0 = time.time()
    exp7()
    exp8()
    exp9()
    elapsed = time.time() - t0

    with RESULTS.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(ROWS[0]))
        writer.writeheader()
        writer.writerows(ROWS)
    params = {
        "label": M.LABEL,
        "python": platform.python_version(),
        "seeds": {"first": SEEDS[0], "last": SEEDS[-1], "n_per_cell": NSEED},
        "experiment_7": {
            "N": M.N, "cohorts": M.COHORTS, "fee": M.FEE, "base_seats": M.BASE_SEATS,
            "gate": M.GATE, "apt_w": M.APT_W, "stock_w": M.STOCK_W,
            "cash_group": M.CASH_GROUP, "cash_draw": M.CASH_DRAW,
            "seat_ramp": M.SEAT_RAMP, "stock_keep": M.STOCK_KEEP,
            "stock_feed": M.STOCK_FEED, "arms": M.ARMS_7,
            "shock": "level capacity doubled (m=2), phased over 4 cohorts, permanent",
        },
        "experiment_8": {
            "N": M.N, "att_threshold": M.ATT_THRESHOLD,
            "comp_threshold": M.COMP_THRESHOLD, "comp_base": M.COMP_BASE,
            "delta_norm": M.DELTA_NORM, "enf_coef": M.ENF_COEF,
            "reg_threshold": M.REG_THRESHOLD, "reg_norm": M.REG_NORM,
            "reg_enf": M.REG_ENF, "work_retain": M.WORK_RETAIN, "cells": M.LAW_CELLS,
        },
        "experiment_9": {
            "N": M.N, "budget": M.BUDGET, "room_cost": M.ROOM_COST,
            "teacher_cost": M.TEACHER_COST, "teacher_capacity": M.TEACHER_CAPACITY,
            "base_rooms": M.BASE_ROOMS, "base_posts": M.BASE_POSTS,
            "q_base": M.Q_BASE, "q_floor": M.Q_FLOOR, "q_slope": M.Q_SLOPE,
            "retention": M.RETENTION, "alloc": M.ALLOC,
        },
        "thresholds": {
            "T7_FLOOR_GAIN": T7_FLOOR_GAIN, "T7_CEIL_GAIN": T7_CEIL_GAIN,
            "T7_MID_GAIN": T7_MID_GAIN, "T7_MID_SEAT_SHARE": T7_MID_SEAT_SHARE,
            "T7_CEIL_VS_FLOOR": T7_CEIL_VS_FLOOR, "T7_NO_UNIVERSAL": T7_NO_UNIVERSAL,
            "T7_UNIVERSAL": T7_UNIVERSAL, "T7_BINDING": T7_BINDING,
            "T8_INERT_ATT": T8_INERT_ATT, "T8_INERT_COMP": T8_INERT_COMP,
            "T8_BIND_ATT": T8_BIND_ATT, "T8_BIND_COMP": T8_BIND_COMP,
            "T8_RATIO": T8_RATIO, "T8_GAP": T8_GAP,
            "T9_ROOMS_PHYS": T9_ROOMS_PHYS, "T9_ROOMS_STAFF": T9_ROOMS_STAFF,
            "T9_ROOMS_COMP": T9_ROOMS_COMP, "T9_SPLIT_STAFF": T9_SPLIT_STAFF,
            "T9_SPLIT_COMP": T9_SPLIT_COMP, "T9_SPLIT_TEACH": T9_SPLIT_TEACH,
            "T9_COMP_SHARE": T9_COMP_SHARE, "T9_RETENTION": T9_RETENTION,
        },
        "elapsed_seconds": round(elapsed, 2),
    }
    (HERE / "parameters.json").write_text(json.dumps(params, indent=2) + "\n")
    print(f"\nwrote {RESULTS} ({len(ROWS)} rows) in {elapsed:.1f}s")


if __name__ == "__main__":
    main()
