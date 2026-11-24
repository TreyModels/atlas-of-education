#!/usr/bin/env python3
"""S5 - Admissions: score bar vs reserved quota vs contest (inventory 81-86).
PREREG: PRE_REGISTRATION.md S5. SIMULATION ONLY; no causal claim."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from eq_common import rng, write_result, save_csv, smoke_parser


def gen(rng, n):
    z = rng.normal(size=n)
    a = 0.3 * z + np.sqrt(1 - 0.09) * rng.normal(size=n)
    score = a + 0.3 * z + rng.normal(scale=0.4, size=n)
    return z, a, score


def admit_bar(score, seats):
    cut = np.sort(score)[::-1][seats - 1]
    return (score >= cut).astype(float)


def admit_quota(z, score, seats, quota_share=0.5, low_group_share=0.4):
    low = z <= np.quantile(z, low_group_share)
    admitted = np.zeros_like(score)
    nq = int(round(seats * quota_share))
    idx_low = np.where(low)[0]
    take = idx_low[np.argsort(score[idx_low])[::-1][:nq]]
    admitted[take] = 1
    idx_other = np.where(~low)[0]
    rest = int(round(seats - admitted.sum()))
    take2 = idx_other[np.argsort(score[idx_other])[::-1][:rest]]
    admitted[take2] = 1
    return admitted


def run(args):
    reps = 15 if args.smoke else 60
    n = 3000 if args.smoke else 12000
    seats = int(0.4 * n)
    out = {"script": "eq04_transitions_gates", "prereg": "S4", "data_tier": "SYNTHETIC",
           "label": "SIMULATION - stipulated admissions DGP; no causal claim",
           "reps": reps, "n": n, "seats": seats}
    rows, summary = [], {}
    for r in range(reps):
        z, a, score = gen(rng(args.seed + r), n)
        q = np.argsort(np.argsort(z)) / (n - 1)
        bar = admit_bar(score, seats)
        quota = admit_quota(z, score, seats)
        quotas = {q: admit_quota(z, score, seats, quota_share=q) for q in (0.4, 0.5, 0.6)}
        # contest: richer pupils value the seat more and exert more effort; rank on score + effort
        value = 1.0 + 0.8 * z
        effort = 0.5 * value
        contest = admit_bar(score + effort, seats)
        for name, adm in [("bar", bar), ("quota", quota), ("contest", contest)]:
            gap = adm[q >= 0.8].mean() - adm[q <= 0.2].mean()
            rows.append([name, r, round(float(adm.mean()), 3), round(float(gap), 4)])
            summary.setdefault(name, []).append(gap)
        for q, adm_q in quotas.items():
            gq = adm_q[q >= 0.8].mean() - adm_q[q <= 0.2].mean()
            summary.setdefault("quota_share_%.1f" % q, []).append(gq)
    summary = {k: {"mean_gap_top_minus_bottom": round(float(np.mean(v)), 4),
                   "ci90": [round(float(np.percentile(v, 5)), 4), round(float(np.percentile(v, 95)), 4)]}
               for k, v in summary.items()}
    rule = {"baseline_gap_positive": summary["bar"]["mean_gap_top_minus_bottom"] > 0,
            "quota_flips_gap_negative": summary["quota"]["mean_gap_top_minus_bottom"] < 0,
            "contest_widens_gap": summary["contest"]["mean_gap_top_minus_bottom"] > summary["bar"]["mean_gap_top_minus_bottom"]}
    rule["PASS"] = all(rule.values())
    mv = {"specs": ["bar", "quota_share_0.4", "quota_share_0.5", "quota_share_0.6", "contest"],
          "estimates": {k: summary[k]["mean_gap_top_minus_bottom"] for k in
                        ["bar", "quota_share_0.4", "quota_share_0.5", "quota_share_0.6", "contest"]}}
    mv["range"] = [min(mv["estimates"].values()), max(mv["estimates"].values())]
    mv["spec_robust"] = len({v > 0 for v in mv["estimates"].values()}) == 1
    out.update({"summary": summary, "multiverse": mv, "decision_rule": rule,
                "system_map": {"nodes": ["stage transitions", "gates"], "piece": 3, "chain": "family affordability -> learning -> gate -> credential->jobs"},
           "masseng_boundary": {"used": "standalone synthetic demonstration (NOT MASSENG v5 output)", "mechanism_in_masseng_v5": True, "note": "standalone synthetic demonstration; not a MASSENG v5 output"},
                "plain_result": ("A score bar admits rich pupils at a higher rate (gap %.3f); a reserved quota "
                                 "flips the gap (%.3f) by construction, and a contest in which richer pupils "
                                 "invest more effort widens it further (%.3f). The quota changes who is admitted, "
                                 "not how much anyone learns — this is a rationing demonstration, not an "
                                 "evaluation of any admissions policy." %
                                 (summary["bar"]["mean_gap_top_minus_bottom"],
                                  summary["quota"]["mean_gap_top_minus_bottom"],
                                  summary["contest"]["mean_gap_top_minus_bottom"]))})
    write_result(args.outdir, "eq04_transitions_gates", out)
    save_csv(args.outdir, "eq04_transitions_gates", ["regime", "rep", "admit_rate", "income_gap"], rows)
    print("PLAIN:", out["plain_result"])
    print("RULE:", rule)
    return out


if __name__ == "__main__":
    run(smoke_parser("S5 admissions bar/quota/contest (SIMULATION)"))
