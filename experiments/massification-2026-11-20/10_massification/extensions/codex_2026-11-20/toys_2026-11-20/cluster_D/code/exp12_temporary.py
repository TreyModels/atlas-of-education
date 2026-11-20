"""Experiment #12: temporary expansion with expectations.

ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.
Thresholds and estimands are frozen in ../PRE_DECLARATIONS.md §4.
The temporary lease is 12 upper-secondary seats in cohorts 2-4 only; the investment rule is
switched off so the lease is the sole capacity variation; starting conditions are a
mid-transition state (near-universal primary/lower-secondary, elite upper-secondary).
"""
import toy_engine as eng

EXPERIMENT = "12_temporary"

SEAT0 = (108, 100, 12)
PARAMS = {
    "seat0": SEAT0,
    "investment_fixed": 0,
    "warm_stage": True,
    "init_readers": 0.758,
    "init_formal_share": 0.40,
    "init_skill_stock": 0.35,
    "belief_memory": 0.70,
    "placement_reference": 12.0,
}
LEASE = [(0, 0, 12) if t == 1 else ((0, 0, -12) if t == 4 else (0, 0, 0)) for t in range(30)]
FEE_PLAN = {t: {2: 0.0} for t in (1, 2, 3)}
EMPLOYERS = ("frozen", "responsive")
TREATMENTS = ("control", "supply_only", "fee_waiver", "placement_info")
ARMS = tuple(f"{t}_{e}" for e in EMPLOYERS for t in TREATMENTS)
WINDOWS = {"PRE": (0, 1), "DURING": (1, 4), "POST": (4, 7), "DECAY": (15, 20)}
QUANTS = ("upper_apps", "total_apps", "hires", "grad_hires", "upper_comple", "poor_upper")


def _arm_config(arm):
    treatment, emp = arm.rsplit("_", 1)
    plan = None if treatment == "control" else LEASE
    fee = FEE_PLAN if treatment == "fee_waiver" else None
    info = treatment == "placement_info"
    return plan, fee, info, emp


def run_seed(seed):
    out = {}
    for arm in ARMS:
        plan, fee, info, emp = _arm_config(arm)
        series = eng.simulate(seed, seats_plan=plan, fee_plan=fee, info=info,
                              employer=emp, params=PARAMS)
        m = eng.metrics(series)
        for w, (a, b) in WINDOWS.items():
            rows = series[a:b]
            m[f"{w}_upper_apps"] = eng.mean([r["applications"][2] for r in rows])
            m[f"{w}_total_apps"] = eng.mean([sum(r["applications"]) for r in rows])
            m[f"{w}_hires"] = eng.mean([r["hires"] for r in rows])
            m[f"{w}_grad_hires"] = eng.mean([r["grad_hires"] for r in rows])
            m[f"{w}_upper_comple"] = eng.mean([r["completions"][2] for r in rows])
            m[f"{w}_poor_upper"] = eng.mean([(r["poor_upper"] / r["completions"][2])
                                             if r["completions"][2] else 0.0 for r in rows])
        out[arm] = m
    return out


def summarise(per_seed):
    rows = []
    for arm in ARMS:
        for w in WINDOWS:
            for q in QUANTS:
                xs = [per_seed[s][arm][f"{w}_{q}"] for s in per_seed]
                for stat, fn in (("median", eng.median), ("mean", eng.mean),
                                 ("p10", lambda v: eng.quantile(v, 0.10)),
                                 ("p90", lambda v: eng.quantile(v, 0.90))):
                    rows.append(dict(experiment=EXPERIMENT, level="cell", arm=arm,
                                     comparison="level", window=w, metric=q, statistic=stat,
                                     value=fn(xs), n=len(xs)))
        emp = arm.rsplit("_", 1)[1]
        ctl = f"control_{emp}"
        if arm != ctl:
            for w in WINDOWS:
                for q in QUANTS:
                    diffs = [per_seed[s][arm][f"{w}_{q}"] - per_seed[s][ctl][f"{w}_{q}"]
                             for s in per_seed]
                    rel = []
                    for s in per_seed:
                        base = per_seed[s][ctl][f"{w}_{q}"]
                        rel.append((per_seed[s][arm][f"{w}_{q}"] - base) / base if base else 0.0)
                    rows.append(dict(experiment=EXPERIMENT, level="paired_gap", arm=arm,
                                     comparison=f"arm_minus_{ctl}", window=w, metric=q,
                                     statistic="median_gap", value=eng.median(diffs), n=len(diffs)))
                    rows.append(dict(experiment=EXPERIMENT, level="paired_gap", arm=arm,
                                     comparison=f"arm_minus_{ctl}", window=w, metric=q,
                                     statistic="median_rel_gap", value=eng.median(rel), n=len(rel)))
                    rows.append(dict(experiment=EXPERIMENT, level="paired_gap", arm=arm,
                                     comparison=f"arm_minus_{ctl}", window=w, metric=q,
                                     statistic="share_gt_0", value=sum(d > 0 for d in diffs) / len(diffs),
                                     n=len(diffs)))
    return rows


def thresholds(per_seed):
    seeds = list(per_seed)
    rows = []

    def gap(arm, w, q):
        ctl = "control_" + arm.rsplit("_", 1)[1]
        return [per_seed[s][arm][f"{w}_{q}"] - per_seed[s][ctl][f"{w}_{q}"] for s in seeds]

    def rel_gap(arm, w, q):
        ctl = "control_" + arm.rsplit("_", 1)[1]
        out = []
        for s in seeds:
            base = per_seed[s][ctl][f"{w}_{q}"]
            out.append((per_seed[s][arm][f"{w}_{q}"] - base) / base if base else 0.0)
        return out

    # P12-1: information arm raises applications, not hires, under frozen jobs.
    rel_post_info = eng.median(rel_gap("placement_info_frozen", "POST", "upper_apps"))
    hires_post_info = eng.median(gap("placement_info_frozen", "POST", "hires"))
    p1_apps = rel_post_info >= 0.05
    p1_hires = abs(hires_post_info) <= 1.0

    # P12-2: temporary hire gain under responsive employers, decaying.
    during_h = eng.median(gap("supply_only_responsive", "DURING", "hires"))
    post_h = eng.median(gap("supply_only_responsive", "POST", "hires"))
    p2_a = during_h >= 2.0
    p2_b = post_h <= 0.5 * during_h if during_h > 0 else post_h <= 0.0

    # P12-3: persistence with decay, at least one treatment arm, applications.
    pers = {}
    for arm in ARMS:
        if arm.startswith("control"):
            continue
        post = eng.median(rel_gap(arm, "POST", "upper_apps"))
        decay = eng.median(rel_gap(arm, "DECAY", "upper_apps"))
        ok = post >= 0.02 and (decay <= 0.5 * post if post > 0 else False)
        pers[arm] = (post, decay, ok)
    p3 = any(v[2] for v in pers.values())

    verdict = ("SUPPORTED" if (p2_a and p2_b and p3)
               else "FALSIFIED" if not p3 else "PARTIAL")

    rows = [
        dict(threshold="P12-1a", metric="median_rel_gap_POST_upper_apps_placement_info_frozen",
             value=rel_post_info, rule=">=+0.05", met=int(p1_apps),
             note="applications up with information (fixed jobs)"),
        dict(threshold="P12-1b", metric="median_gap_POST_hires_placement_info_frozen",
             value=hires_post_info, rule="|gap|<=1.0 person", met=int(p1_hires),
             note="total hires flat; frozen-posts total is 40 by construction"),
        dict(threshold="P12-2a", metric="median_gap_DURING_hires_supply_only_responsive",
             value=during_h, rule=">=+2.0 persons", met=int(p2_a),
             note="temporary hire gain under responsive employers"),
        dict(threshold="P12-2b", metric="median_gap_POST_hires_supply_only_responsive",
             value=post_h, rule="<=50% of DURING gap", met=int(p2_b),
             note="decay of the hire gain after the lease ends"),
        dict(threshold="P12-3", metric="max_arm_POST_rel_gap_with_decay", value=p3,
             rule="at least one arm: POST>=+2% and DECAY<=50% of POST", met=int(p3),
             note=";".join(f"{a}:post={v[0]:.3f},decay={v[1]:.3f}" for a, v in pers.items())),
    ]
    for arm, (post, decay, ok) in pers.items():
        rows.append(dict(threshold="SIDE", metric=f"rel_gap_POST_upper_apps_{arm}", value=post,
                         rule="descriptive", met=int(post >= 0.02), note=f"decay={decay:.4f}"))
    for arm in ("supply_only_frozen", "fee_waiver_frozen", "supply_only_responsive",
                "fee_waiver_responsive"):
        rows.append(dict(threshold="SIDE", metric=f"median_gap_DURING_poor_upper_{arm}",
                         value=eng.median(gap(arm, "DURING", "poor_upper")),
                         rule="descriptive: fee waiver should shift composition, not seats", met=1,
                         note="poor share of upper-secondary completers"))
    return verdict, rows
