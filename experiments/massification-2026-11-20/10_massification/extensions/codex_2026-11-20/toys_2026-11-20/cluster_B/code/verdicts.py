"""Cell means, paired contrasts and predeclared-threshold verdicts for Cluster B.

ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence.

The thresholds evaluated here are the ones written in ../PRE_DECLARATIONS.md
before the run. Nothing in this module may be edited after seeing RESULTS.csv.
"""
import statistics

EXPERIMENTS = ("exp4_visibility_mechanism", "exp5_queue_vs_human_capital",
               "exp6_eligibility_vs_blind_ranking")


def index(rows):
    """values[(arm, metric)][seed] = float, skipping undefined (empty) values."""
    out = {}
    for r in rows:
        v = r["value"]
        if v in ("", None):
            continue
        out.setdefault((r["arm"], r["metric"]), {})[r["seed"]] = float(v)
    return out


def mean_of(values):
    xs = list(values.values())
    return sum(xs) / len(xs) if xs else None


def cell_means(values, experiment_arms, metrics):
    """means[arm][metric] = mean over seeds (None when undefined everywhere)."""
    out = {}
    for arm in experiment_arms:
        out[arm] = {m: mean_of(values.get((arm, m), {})) for m in metrics}
    return out


def paired_diffs(values, metric, arm_a, arm_b, seeds):
    """Per-seed differences a - b on a metric, only where both are defined."""
    va, vb = values.get((arm_a, metric), {}), values.get((arm_b, metric), {})
    return {s: va[s] - vb[s] for s in seeds if s in va and s in vb}


def summarize(diffs):
    if not diffs:
        return {"n": 0, "mean": None, "share_positive": None, "share_negative": None}
    xs = list(diffs.values())
    return {
        "n": len(xs),
        "mean": sum(xs) / len(xs),
        "sd": statistics.pstdev(xs) if len(xs) > 1 else 0.0,
        "share_positive": sum(x > 0 for x in xs) / len(xs),
        "share_negative": sum(x < 0 for x in xs) / len(xs),
        "share_zero": sum(x == 0 for x in xs) / len(xs),
    }


def _verdict(ok, text):
    return {"status": "PASS" if ok else "NOT MET", "statement": text}


def _falsifier(ok, text):
    return {"status": "FALSIFIER TRIGGERED" if ok else "falsifier not triggered",
            "statement": text}


def evaluate(rows, seeds):
    values = index(rows)
    result = {}

    # ---------------- Experiment 4 ----------------
    e4 = "exp4_visibility_mechanism"
    e4_arms = [f"{m}:v{v:.1f}" for m in ("human_capital", "signaling") for v in (0.0, 0.5, 1.0)]
    e4_metrics = ["applications", "admissions", "public_admissions", "private_admissions",
                  "graduate_hires", "applicant_hires", "output_true_hires", "output_valued_hires",
                  "rejected_count", "rejected_skill"]
    cm4 = cell_means(values, e4_arms, e4_metrics)

    def m4(arm, metric):
        return cm4[arm][metric]

    def d(metric, a, b):
        return summarize(paired_diffs(values, metric, a, b, seeds))

    hc0, hc5, hc1 = "human_capital:v0.0", "human_capital:v0.5", "human_capital:v1.0"
    sg0, sg5, sg1 = "signaling:v0.0", "signaling:v0.5", "signaling:v1.0"

    hc_true_delta = d("output_true_hires", hc1, hc0)
    sg_true_delta = d("output_true_hires", sg1, sg0)
    hc_val_delta = d("output_valued_hires", hc1, hc0)
    sg_val_delta = d("output_valued_hires", sg1, sg0)

    t41_pattern = (
        hc_true_delta["mean"] is not None and hc_true_delta["mean"] >= 0.05
        and m4(hc5, "output_true_hires") >= m4(hc0, "output_true_hires") - 0.01
        and m4(hc1, "output_true_hires") >= m4(hc5, "output_true_hires") - 0.01
        and sg_true_delta["mean"] is not None and sg_true_delta["mean"] <= -0.05
        and m4(sg5, "output_true_hires") <= m4(sg0, "output_true_hires") + 0.01
        and m4(sg1, "output_true_hires") <= m4(sg5, "output_true_hires") + 0.01
    )
    t42_pattern = (
        hc_val_delta["mean"] is not None and hc_val_delta["mean"] >= 0.05
        and m4(hc5, "output_valued_hires") >= m4(hc0, "output_valued_hires") - 0.01
        and m4(hc1, "output_valued_hires") >= m4(hc5, "output_valued_hires") - 0.01
        and sg_val_delta["mean"] is not None and sg_val_delta["mean"] <= -0.05
        and m4(sg5, "output_valued_hires") <= m4(sg0, "output_valued_hires") + 0.01
        and m4(sg1, "output_valued_hires") <= m4(sg5, "output_valued_hires") + 0.01
    )

    def composition_leg(v):
        hc_a, sg_a = f"human_capital:v{v:.1f}", f"signaling:v{v:.1f}"
        rc_gap = abs(m4(hc_a, "rejected_count") - m4(sg_a, "rejected_count"))
        rs_hc, rs_sg = m4(hc_a, "rejected_skill"), m4(sg_a, "rejected_skill")
        rs_gap = None if (rs_hc is None or rs_sg is None) else abs(rs_hc - rs_sg)
        gh_gap = abs(m4(hc_a, "graduate_hires") - m4(sg_a, "graduate_hires"))
        return {"v": v, "rejected_count_gap": rc_gap, "rejected_skill_gap": rs_gap,
                "graduate_hires_gap": gh_gap,
                "met": (rc_gap >= 10 or (rs_gap is not None and rs_gap >= 0.10))
                       and gh_gap >= 10}

    comp = [composition_leg(v) for v in (0.5, 1.0)]
    pairing = {
        "applications_equal_at_v0": abs(m4(hc0, "applications") - m4(sg0, "applications")) < 1e-9,
        "admissions_equal_at_v0": abs(m4(hc0, "admissions") - m4(sg0, "admissions")) < 1e-9,
        "rejected_count_equal_at_v0": abs(m4(hc0, "rejected_count") - m4(sg0, "rejected_count")) < 1e-9,
        "graduate_hires_equal_at_v0": abs(m4(hc0, "graduate_hires") - m4(sg0, "graduate_hires")) < 1e-9,
        "valued_output_equal_at_v0": abs(m4(hc0, "output_valued_hires") - m4(sg0, "output_valued_hires")) < 1e-9,
        "rejected_skill_equal_at_v0": None,
        "rejected_skill_at_v0_note":
            "Not a pairing test: at v=0 the two markets are structurally identical (counts above are equal), but "
            "the human-capital rule adds +1.0 true skill to every graduate by definition, so the rejected set's "
            "MEAN TRUE SKILL necessarily differs between mechanisms (0.688 vs 0.496). Recorded for transparency.",
    }
    coincide = True
    coincide_detail = []
    for v in (0.0, 0.5, 1.0):
        hc_a, sg_a = f"human_capital:v{v:.1f}", f"signaling:v{v:.1f}"
        dt = abs(m4(hc_a, "output_true_hires") - m4(sg_a, "output_true_hires"))
        dv = abs(m4(hc_a, "output_valued_hires") - m4(sg_a, "output_valued_hires"))
        dr = abs(m4(hc_a, "rejected_count") - m4(sg_a, "rejected_count"))
        dg = abs(m4(hc_a, "graduate_hires") - m4(sg_a, "graduate_hires"))
        same = dt < 0.02 and dv < 0.02 and dr < 0.5 and dg < 0.5
        coincide = coincide and same
        coincide_detail.append({"v": v, "output_true_gap": dt, "output_valued_gap": dv,
                                "rejected_count_gap": dr, "graduate_hires_gap": dg,
                                "signatures_coincide": same})

    result[e4] = {
        "label": "ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence",
        "cells": cm4,
        "paired_contrasts": {
            "hc_true_v1_minus_v0": hc_true_delta,
            "sg_true_v1_minus_v0": sg_true_delta,
            "hc_valued_v1_minus_v0": hc_val_delta,
            "sg_valued_v1_minus_v0": sg_val_delta,
            "hc_true_v05_minus_v0": d("output_true_hires", hc5, hc0),
            "sg_true_v05_minus_v0": d("output_true_hires", sg5, sg0),
            "hc_true_v1_minus_v05": d("output_true_hires", hc1, hc5),
            "sg_true_v1_minus_v05": d("output_true_hires", sg1, sg5),
            "hc_valued_v05_minus_v0": d("output_valued_hires", hc5, hc0),
            "hc_valued_v1_minus_v05": d("output_valued_hires", hc1, hc5),
            "sg_valued_v05_minus_v0": d("output_valued_hires", sg5, sg0),
            "sg_valued_v1_minus_v05": d("output_valued_hires", sg1, sg5),
            "hc_applications_v1_minus_v0": d("applications", hc1, hc0),
            "sg_applications_v1_minus_v0": d("applications", sg1, sg0),
        },
        "verdicts": [
            dict(_verdict(t41_pattern,
                          "T4.1 TRUE-output sign pattern: HC output among hires rises with v by >= +0.05 and is "
                          "monotone non-decreasing; signalling output among hires falls with v by >= -0.05 and is "
                          "monotone non-increasing."), id="T4.1"),
            dict(_verdict(t42_pattern,
                          "T4.2 EMPLOYER-VALUED output sign pattern (v*skill + (1-v)*credential): same rise/fall "
                          "pattern with the same margins."), id="T4.2"),
            dict(_verdict(all(c["met"] for c in comp),
                          "T4.3 Rejected-applicant composition differs at v in {0.5,1}: rejected-count gap >= 10 or "
                          "rejected-skill gap >= 0.10, and graduate-hire gap >= 10."), id="T4.3"),
        ],
        "composition_legs": comp,
        "pairing_diagnostics_v0": pairing,
        "falsifier": dict(_falsifier(coincide,
                                     "F4: signatures coincide at ALL v (output true and valued gaps < 0.02, "
                                     "rejected counts equal, graduate hires equal)."),
                          detail=coincide_detail),
    }

    # ---------------- Experiment 5 ----------------
    e5 = "exp5_queue_vs_human_capital"
    e5_arms = ["skill_upgrade:fixed_jobs", "skill_upgrade:responsive_jobs",
               "rank_upgrade:fixed_jobs", "rank_upgrade:responsive_jobs",
               "reference_no_treatment:fixed_jobs", "reference_no_treatment:responsive_jobs"]
    e5_metrics = ["older_group_hires", "treated_group_hires", "total_hires",
                  "output_hires", "population_mean_skill", "job_count"]
    cm5 = cell_means(values, e5_arms, e5_metrics)

    def m5(arm, metric):
        return cm5[arm][metric]

    sk_f, rk_f = "skill_upgrade:fixed_jobs", "rank_upgrade:fixed_jobs"
    sk_r, rk_r = "skill_upgrade:responsive_jobs", "rank_upgrade:responsive_jobs"
    bl_f, bl_r = "reference_no_treatment:fixed_jobs", "reference_no_treatment:responsive_jobs"

    t51 = (m5(rk_f, "older_group_hires") <= m5(bl_f, "older_group_hires") - 1.0
           and m5(rk_f, "older_group_hires") <= m5(sk_f, "older_group_hires") - 1.0)
    t52 = m5(rk_f, "output_hires") <= m5(bl_f, "output_hires") - 0.05
    t53 = m5(sk_f, "output_hires") >= m5(bl_f, "output_hires") + 0.05
    gap_fixed = m5(rk_f, "output_hires") - m5(sk_f, "output_hires")
    gap_resp = m5(rk_r, "output_hires") - m5(sk_r, "output_hires")
    t54 = abs(gap_resp) <= 0.05
    # decomposition diagnostic: full absorption makes hires = population, so the
    # residual output gap is the stipulated +1 skill on 20 people.
    pop_gap = m5(rk_r, "population_mean_skill") - m5(sk_r, "population_mean_skill")
    alloc_gap_resp = gap_resp - pop_gap
    older_gap_resp = m5(rk_r, "older_group_hires") - m5(sk_r, "older_group_hires")
    t55 = abs(older_gap_resp) <= 1.0

    result[e5] = {
        "label": "ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence",
        "cells": cm5,
        "paired_contrasts": {
            "rank_fixed_minus_reference_fixed_output": d("output_hires", rk_f, bl_f),
            "skill_fixed_minus_reference_fixed_output": d("output_hires", sk_f, bl_f),
            "rank_fixed_minus_skill_fixed_output": d("output_hires", rk_f, sk_f),
            "rank_fixed_minus_reference_fixed_older_hires": d("older_group_hires", rk_f, bl_f),
            "rank_fixed_minus_skill_fixed_older_hires": d("older_group_hires", rk_f, sk_f),
            "rank_resp_minus_skill_resp_output": d("output_hires", rk_r, sk_r),
            "rank_resp_minus_skill_resp_older_hires": d("older_group_hires", rk_r, sk_r),
        },
        "gaps": {"output_gap_fixed": gap_fixed, "output_gap_responsive": gap_resp,
                 "population_mean_gap_responsive": pop_gap,
                 "allocation_component_responsive": alloc_gap_resp,
                 "older_hire_gap_responsive": older_gap_resp,
                 "output_gap_attenuation_share":
                     None if gap_fixed == 0 else 1 - abs(gap_resp) / abs(gap_fixed)},
        "verdicts": [
            dict(_verdict(t51, "T5.1 Rank allocation lowers hires of the fixed older-diploma group: rank/fixed <= "
                               "reference/fixed - 1.0 and rank/fixed <= skill/fixed - 1.0."), id="T5.1"),
            dict(_verdict(t52, "T5.2 Rank allocation lowers output among hires: rank/fixed <= reference/fixed - 0.05."),
                 id="T5.2"),
            dict(_verdict(t53, "T5.3 Skill upgrade raises output among hires: skill/fixed >= reference/fixed + 0.05."),
                 id="T5.3"),
            dict(_verdict(t54, "T5.4 The fixed-jobs output separation DISAPPEARS under responsive jobs: "
                               "|output(rank,responsive) - output(skill,responsive)| <= 0.05."), id="T5.4"),
        ],
        "diagnostics": [
            dict(_verdict(t55, "D5.5 (diagnostic) Older-diploma hire separation disappears under responsive jobs: "
                               "|older(rank,responsive) - older(skill,responsive)| <= 1.0."), id="D5.5"),
            dict(_verdict(abs(alloc_gap_resp) <= 0.05,
                          "D5.6 (diagnostic) Allocation-induced output gap under responsive jobs (total gap minus "
                          "the stipulated population skill gap) <= 0.05 in absolute value."), id="D5.6"),
        ],
    }

    # ---------------- Experiment 6 ----------------
    e6 = "exp6_eligibility_vs_blind_ranking"
    e6_arms = []
    for c in (45, 25):
        for vis in ("visible_credential", "blind_ranking"):
            for gate in ("gate_repealed", "gate_retained"):
                e6_arms.append(f"c{c}:{vis}:{gate}")
    e6_metrics = ["uncred_offers", "cred_offers", "total_offers", "uncred_offer_rate",
                  "offer_skill_mean", "vacancies", "eligible_count"]
    cm6 = cell_means(values, e6_arms, e6_metrics)

    def rate(c, vis, gate):
        return cm6[f"c{c}:{vis}:{gate}"]["uncred_offer_rate"]

    v_ret = rate(45, "visible_credential", "gate_retained")
    v_rep = rate(45, "visible_credential", "gate_repealed")
    b_ret = rate(45, "blind_ranking", "gate_retained")
    b_rep = rate(45, "blind_ranking", "gate_repealed")
    t61 = (v_rep - v_ret >= 0.15) and (v_rep >= 0.25)
    t62 = b_ret <= 0.05
    t63 = b_rep >= 0.25
    t64 = (b_rep > 0) and (v_rep >= 0.75 * b_rep)
    rates = [v_ret, v_rep, b_ret, b_rep]
    coincide6 = (max(rates) - min(rates)) <= 0.01

    sens = {}
    for c in (25,):
        s_ret = rate(c, "visible_credential", "gate_retained")
        s_rep = rate(c, "visible_credential", "gate_repealed")
        s_b_ret = rate(c, "blind_ranking", "gate_retained")
        s_b_rep = rate(c, "blind_ranking", "gate_repealed")
        sens[f"c{c}"] = {
            "rates": {"visible_gate_retained": s_ret, "visible_gate_repealed": s_rep,
                      "blind_gate_retained": s_b_ret, "blind_gate_repealed": s_b_rep},
            "gate_alone_raises_by": s_rep - s_ret,
            "blind_alone_rate": s_b_ret,
            "both_rate": s_b_rep,
            "repeal_reaches_75pct_of_both": (s_b_rep > 0) and (s_rep >= 0.75 * s_b_rep),
        }

    result[e6] = {
        "label": "ILLUSTRATIVE TOY — stipulated parameters; not calibrated; not evidence",
        "cells": cm6,
        "paired_contrasts": {
            "visible_repealed_minus_visible_retained": d("uncred_offer_rate",
                                                         "c45:visible_credential:gate_repealed",
                                                         "c45:visible_credential:gate_retained"),
            "blind_repealed_minus_blind_retained": d("uncred_offer_rate",
                                                     "c45:blind_ranking:gate_repealed",
                                                     "c45:blind_ranking:gate_retained"),
            "both_minus_visible_repealed": d("uncred_offer_rate",
                                             "c45:blind_ranking:gate_repealed",
                                             "c45:visible_credential:gate_repealed"),
        },
        "main_rates": {"visible_gate_retained": v_ret, "visible_gate_repealed": v_rep,
                       "blind_gate_retained": b_ret, "blind_gate_repealed": b_rep},
        "sensitivity_c25": sens,
        "verdicts": [
            dict(_verdict(t61, "T6.1 Gate repeal alone raises the uncredentialed offer rate by >= 0.15 and to the "
                               "declared high level (>= 0.25) when the credential is visible at ranking."), id="T6.1"),
            dict(_verdict(t62, "T6.2 Blind ranking alone (gate retained) leaves the uncredentialed offer rate at the "
                               "low level (<= 0.05)."), id="T6.2"),
            dict(_verdict(t63, "T6.3 Both levers together (blind ranking + gate repealed) reach the declared high "
                               "level (>= 0.25)."), id="T6.3"),
            dict(_verdict(t64, "T6.4 Repeal is a sufficient lever: rate(visible,repealed) >= 0.75 * "
                               "rate(blind,repealed)."), id="T6.4"),
        ],
        "falsifier": dict(_falsifier(coincide6,
                                     "F6: no effect of either lever - all four main uncredentialed offer rates equal "
                                     "within 0.01."),
                          rates=dict(zip(["visible_gate_retained", "visible_gate_repealed",
                                          "blind_gate_retained", "blind_gate_repealed"], rates))),
    }
    return result
