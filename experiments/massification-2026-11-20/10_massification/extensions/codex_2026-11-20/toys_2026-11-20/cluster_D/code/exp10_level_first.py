"""Experiment #10: level-first roll-out and crossing order.

ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.
Thresholds and estimands are frozen in ../PRE_DECLARATIONS.md §2.
"""
import toy_engine as eng

EXPERIMENT = "10_level_first"
PV_BUDGET = 40.0
DELTA = 0.97

# Windows in cohort numbers (1-indexed, inclusive).
WINDOWS = {
    "primary_first": {0: (1, 5), 1: (6, 10), 2: (11, 15)},
    "lower_first": {1: (1, 5), 0: (6, 10), 2: (11, 15)},
    "upper_first": {2: (1, 5), 1: (6, 10), 0: (11, 15)},
    "simultaneous": {0: (1, 15), 1: (1, 15), 2: (1, 15)},
}
ARMS = ("control",) + tuple(WINDOWS)
SEQUENTIAL = ("primary_first", "lower_first", "upper_first")


def pv_schedule(windows, pv_budget=PV_BUDGET, delta=DELTA, horizon=30):
    """Equal present value: nominal injection (pv_budget/years)*delta^-t over each window."""
    plan = []
    for t in range(horizon):
        inj = [0.0, 0.0, 0.0]
        for k, (a, b) in windows.items():
            if a <= t + 1 <= b:
                years = b - a + 1
                inj[k] = (pv_budget / years) / (delta ** t)
        plan.append(tuple(inj))
    return plan


def schedule_pv(windows, pv_budget=PV_BUDGET, delta=DELTA, horizon=30):
    plan = pv_schedule(windows, pv_budget, delta, horizon)
    return tuple(round(sum(inj[k] * delta ** t for t, inj in enumerate(plan)), 6) for k in range(3))


def run_seed(seed):
    out = {}
    for arm in ARMS:
        plan = None if arm == "control" else pv_schedule(WINDOWS[arm])
        series = eng.simulate(seed, seats_plan=plan)
        m = eng.metrics(series)
        m["order_ok"] = int(m["X_M0"] <= m["X_M2"] <= m["X_M3"])
        m["order_floor_strict"] = int(m["X_M0"] < m["X_M2"] < m["X_M3"])
        m["prim_universal"] = 1 - m["cens_M1"]
        out[arm] = m
    return out


def summarise(per_seed):
    """Aggregate rows (one per arm/metric) and paired-gap rows vs control."""
    arms = list(ARMS)
    metrics = ["X_M0", "X_M1", "X_M2", "X_M3", "U90",
               "S_M3_M0", "S_M3_M2", "S_M1_M0",
               "primary_share_h", "lower_share_h", "upper_share_h",
               "floor_ceiling_gap", "upper_total", "applications_total",
               "order_ok", "order_floor_strict", "prim_universal"]
    rows = []
    for arm in arms:
        for met in metrics:
            xs = [per_seed[s][arm][met] for s in per_seed]
            rows.append(dict(experiment=EXPERIMENT, level="cell", arm=arm, comparison="level",
                             window="all", metric=met, statistic="median",
                             value=eng.median(xs), n=len(xs)))
            if met not in ("order_ok", "order_floor_strict", "prim_universal"):
                rows.append(dict(experiment=EXPERIMENT, level="cell", arm=arm, comparison="level",
                                 window="all", metric=met, statistic="p10",
                                 value=eng.quantile(xs, 0.10), n=len(xs)))
                rows.append(dict(experiment=EXPERIMENT, level="cell", arm=arm, comparison="level",
                                 window="all", metric=met, statistic="p90",
                                 value=eng.quantile(xs, 0.90), n=len(xs)))
                rows.append(dict(experiment=EXPERIMENT, level="cell", arm=arm, comparison="level",
                                 window="all", metric=met, statistic="mean",
                                 value=eng.mean(xs), n=len(xs)))
        if arm != "control":
            for met in ("X_M0", "X_M1", "X_M2", "X_M3", "U90", "S_M3_M0", "S_M3_M2",
                        "upper_share_h", "primary_share_h", "upper_total", "applications_total"):
                diffs = [per_seed[s][arm][met] - per_seed[s]["control"][met] for s in per_seed]
                rows.append(dict(experiment=EXPERIMENT, level="paired_gap", arm=arm,
                                 comparison="arm_minus_control", window="all", metric=met,
                                 statistic="median_gap", value=eng.median(diffs), n=len(diffs)))
                rows.append(dict(experiment=EXPERIMENT, level="paired_gap", arm=arm,
                                 comparison="arm_minus_control", window="all", metric=met,
                                 statistic="share_gt_0", value=sum(d > 0 for d in diffs) / len(diffs),
                                 n=len(diffs)))
                rows.append(dict(experiment=EXPERIMENT, level="paired_gap", arm=arm,
                                 comparison="arm_minus_control", window="all", metric=met,
                                 statistic="share_eq_0", value=sum(d == 0 for d in diffs) / len(diffs),
                                 n=len(diffs)))
    return rows


def thresholds(per_seed):
    """Pre-declared P10-1..P10-3. Returns (verdict, rows)."""
    seeds = list(per_seed)
    rows = []

    def med(arm, met):
        return eng.median([per_seed[s][arm][met] for s in seeds])

    def paired(arm, met):
        return [per_seed[s][arm][met] - per_seed[s]["control"][met] for s in seeds]

    share_order = {a: eng.mean([per_seed[s][a]["order_ok"] for s in seeds]) for a in SEQUENTIAL}
    p1_met = min(share_order.values()) >= 0.90

    s_prim = med("primary_first", "S_M3_M0")
    s_sim = med("simultaneous", "S_M3_M0")
    d_pair = eng.median([per_seed[s]["primary_first"]["S_M3_M0"] - per_seed[s]["simultaneous"]["S_M3_M0"]
                         for s in seeds])
    p2_a = s_prim >= 2.0
    p2_b = s_sim <= 1.0
    p2_c = d_pair >= 2.0
    p2_met = p2_a and p2_b and p2_c

    # P10-3 compares each sequential arm with the SIMULTANEOUS arm (as declared in §2),
    # not with the no-injection control.
    band = {a: abs(eng.median([per_seed[s][a]["X_M3"] - per_seed[s]["simultaneous"]["X_M3"]
                               for s in seeds])) for a in SEQUENTIAL}
    p3_met = max(band.values()) >= 1.0

    verdict = ("SUPPORTED" if all([p1_met, p2_met, p3_met])
               else "FALSIFIED" if (not p1_met and not p3_met) else "PARTIAL")

    rows = [
        dict(threshold="P10-1", metric="share_order_non_decreasing", value=min(share_order.values()),
             rule=">=0.90 in every sequential arm", met=int(p1_met),
             note=";".join(f"{a}={share_order[a]:.3f}" for a in SEQUENTIAL)),
        dict(threshold="P10-2a", metric="median_S_primary_first", value=s_prim,
             rule=">=2.0 years", met=int(p2_a), note="floor-to-ceiling spacing, primary_first"),
        dict(threshold="P10-2b", metric="median_S_simultaneous", value=s_sim,
             rule="<=1.0 year", met=int(p2_b), note="compression under simultaneous expansion"),
        dict(threshold="P10-2c", metric="median_paired_S_diff", value=d_pair,
             rule=">=2.0 years", met=int(p2_c), note="primary_first minus simultaneous, paired"),
        dict(threshold="P10-3", metric="max_median_abs_gap_X_M3", value=max(band.values()),
             rule=">=1.0 year for at least one sequential arm", met=int(p3_met),
             note=";".join(f"{a}={band[a]:.2f}" for a in SEQUENTIAL)),
        dict(threshold="INTERVAL", metric="S_primary_first_in_2_12", value=s_prim,
             rule="declared interval [2,12] years (secondary, non-decisive)",
             met=int(2.0 <= s_prim <= 12.0), note="interval prediction, not a decision rule"),
    ]

    # Sub-checks reported for every arm so partial failures are visible.
    for a in SEQUENTIAL:
        gaps = [per_seed[s][a]["X_M2"] - per_seed[s][a]["X_M0"] for s in seeds]
        rows.append(dict(threshold="SIDE", metric=f"median_gap_M0_M2_{a}", value=eng.median(gaps),
                         rule="descriptive: consecutive level take-off gap >=1 year (secondary)",
                         met=int(eng.median(gaps) >= 1.0), note="secondary, non-decisive"))
    # Uncensored-only version of the P10-3 band (secondary diagnostic, not decisive):
    # drops seeds where either side's ceiling take-off was never reached (sentinel 31).
    for a in SEQUENTIAL:
        vals = [abs(per_seed[s][a]["X_M3"] - per_seed[s]["simultaneous"]["X_M3"])
                for s in seeds
                if not per_seed[s][a]["cens_M3"] and not per_seed[s]["simultaneous"]["cens_M3"]]
        rows.append(dict(threshold="SIDE", metric=f"median_abs_gap_X_M3_uncensored_{a}",
                         value=(eng.median(vals) if vals else float("nan")),
                         rule="descriptive: P10-3 restricted to seeds with both ceilings reached",
                         met=int(bool(vals) and eng.median(vals) >= 1.0),
                         note=f"n_uncensored={len(vals)}"))
    for a in ARMS:
        rows.append(dict(threshold="SIDE", metric=f"censored_U90_{a}",
                         value=eng.mean([per_seed[s][a]["cens_U90"] for s in seeds]),
                         rule="descriptive: share of seeds where ceiling universal (90%) never reached",
                         met=1, note="A10-mirror diagnostic; not a decision rule"))
    return verdict, rows
