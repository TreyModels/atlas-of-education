"""Experiment #11: cohort-size shock x capacity rule.

ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.
Thresholds and estimands are frozen in ../PRE_DECLARATIONS.md §3.
"""
import toy_engine as eng

EXPERIMENT = "11_cohort_shock"

SIZES = {"down": 96, "neutral": 120, "up": 144}
RULES = ("frozen", "responsive")
ARMS = tuple(f"{s}_{r}" for r in RULES for s in ("neutral", "up", "down"))
CONTROL = {"frozen": "neutral_frozen", "responsive": "neutral_responsive"}


INVESTMENT = 3   # fixed nominal seats per cohort, identical in every arm


def run_seed(seed):
    out = {}
    for rule in RULES:
        for shock, n in SIZES.items():
            arm = f"{shock}_{rule}"
            series = eng.simulate(seed, sizes=[n] * 30,
                                  per_child=(rule == "responsive"),
                                  employer="responsive",
                                  params={"investment_fixed": INVESTMENT})
            m = eng.metrics(series)
            out[arm] = m
    return out


def summarise(per_seed):
    metrics = ["X_M0", "X_M1", "X_M2", "X_M3", "U90", "S_M3_M0",
               "primary_share_h", "lower_share_h", "upper_share_h",
               "floor_ceiling_gap", "primary_total", "upper_total", "applications_total",
               "primary_seats_h", "primary_apps_h"]
    rows = []
    for arm in ARMS:
        for met in metrics:
            xs = [per_seed[s][arm][met] for s in per_seed]
            for stat, fn in (("median", eng.median), ("mean", eng.mean),
                             ("p10", lambda v: eng.quantile(v, 0.10)),
                             ("p90", lambda v: eng.quantile(v, 0.90))):
                rows.append(dict(experiment=EXPERIMENT, level="cell", arm=arm, comparison="level",
                                 window="all", metric=met, statistic=stat, value=fn(xs), n=len(xs)))
        if arm not in CONTROL.values():
            rule = "frozen" if arm.endswith("frozen") else "responsive"
            ctl = CONTROL[rule]
            for met in ("X_M0", "X_M2", "X_M3", "primary_share_h", "lower_share_h",
                        "upper_share_h", "primary_total", "upper_total"):
                diffs = [per_seed[s][arm][met] - per_seed[s][ctl][met] for s in per_seed]
                rows.append(dict(experiment=EXPERIMENT, level="paired_gap", arm=arm,
                                 comparison=f"arm_minus_{ctl}", window="all", metric=met,
                                 statistic="median_gap", value=eng.median(diffs), n=len(diffs)))
                rows.append(dict(experiment=EXPERIMENT, level="paired_gap", arm=arm,
                                 comparison=f"arm_minus_{ctl}", window="all", metric=met,
                                 statistic="share_gt_0", value=sum(d > 0 for d in diffs) / len(diffs),
                                 n=len(diffs)))
                rows.append(dict(experiment=EXPERIMENT, level="paired_gap", arm=arm,
                                 comparison=f"arm_minus_{ctl}", window="all", metric=met,
                                 statistic="share_lt_0", value=sum(d < 0 for d in diffs) / len(diffs),
                                 n=len(diffs)))
    return rows


def thresholds(per_seed):
    seeds = list(per_seed)
    rows = []

    def diffs(arm, ctl, met):
        return [per_seed[s][arm][met] - per_seed[s][ctl][met] for s in seeds]

    d_up_frozen = eng.median(diffs("up_frozen", "neutral_frozen", "X_M0"))
    d_up_resp = eng.median(diffs("up_responsive", "neutral_responsive", "X_M0"))
    d_down_frozen = eng.median(diffs("down_frozen", "neutral_frozen", "X_M0"))

    # Paired difference-in-differences, seed by seed.
    did = [(per_seed[s]["up_frozen"]["X_M0"] - per_seed[s]["neutral_frozen"]["X_M0"])
           - (per_seed[s]["up_responsive"]["X_M0"] - per_seed[s]["neutral_responsive"]["X_M0"])
           for s in seeds]
    did_med = eng.median(did)

    s_up_frozen = eng.median(diffs("up_frozen", "neutral_frozen", "primary_share_h"))
    s_up_resp = eng.median(diffs("up_responsive", "neutral_responsive", "primary_share_h"))

    p1_frozen = d_up_frozen >= 1.0
    p1_resp = abs(d_up_resp) <= 0.5
    p2 = did_med >= 0.75
    p3_frozen = s_up_frozen <= -0.05
    p3_resp = s_up_resp >= -0.02

    verdict = ("SUPPORTED" if (p2 and p1_frozen and p3_frozen)
               else "FALSIFIED" if not p2 else "PARTIAL")

    rows = [
        dict(threshold="P11-1a", metric="median_gap_X_M0_up_frozen", value=d_up_frozen,
             rule=">=+1.0 year (delay under frozen capacity)", met=int(p1_frozen),
             note="paired up minus neutral, frozen capacity"),
        dict(threshold="P11-1b", metric="median_gap_X_M0_up_responsive", value=d_up_resp,
             rule="|gap|<=0.5 year", met=int(p1_resp),
             note="paired up minus neutral, responsive capacity"),
        dict(threshold="P11-2", metric="median_paired_DiD_X_M0", value=did_med,
             rule=">=0.75 year (interaction)", met=int(p2),
             note="paired (up-neutral|frozen) - (up-neutral|responsive)"),
        dict(threshold="P11-3a", metric="median_gap_primary_share_up_frozen", value=s_up_frozen,
             rule="<=-0.05", met=int(p3_frozen), note="completion per child at horizon"),
        dict(threshold="P11-3b", metric="median_gap_primary_share_up_responsive", value=s_up_resp,
             rule=">=-0.02", met=int(p3_resp), note="completion per child at horizon"),
        dict(threshold="SIDE", metric="median_gap_X_M0_down_frozen", value=d_down_frozen,
             rule="descriptive: symmetric down-shock should advance crossings (<=0)",
             met=int(d_down_frozen <= 0), note="secondary, non-decisive"),
        dict(threshold="SIDE", metric="share_did_gt_0", value=sum(1 for d in did if d > 0) / len(did),
             rule="descriptive: share of seeds with a positive paired DiD", met=1,
             note="secondary"),
    ]
    return verdict, rows
