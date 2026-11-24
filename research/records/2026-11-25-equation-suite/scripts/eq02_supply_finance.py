#!/usr/bin/env python3
"""S7 - Education finance, benefit incidence, cost-benefit (inventory 106-122).
PREREG: PRE_REGISTRATION.md S7. SIMULATION ONLY; no causal claim."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from eq_common import rng, write_result, save_csv, smoke_parser


def gini(x):
    x = np.sort(np.asarray(x, float)); n = len(x); c = np.cumsum(x)
    return float((2 * np.sum(np.arange(1, n + 1) * x) / (n * c[-1])) - (n + 1) / n)


def concentration(benefit, income):
    """Concentration index of benefits ranked by income (positive = pro-rich)."""
    b = np.asarray(benefit, float); y = np.asarray(income, float)
    order = np.argsort(y)
    b = b[order]
    rank = (np.arange(1, len(b) + 1) / len(b))
    return float(2 * np.cov(b, rank, bias=True)[0, 1] / b.mean()) if b.mean() > 0 else 0.0


def irr(cashflows, lo=-0.9, hi=1.0, iters=200):
    def npv(r):
        return sum(cf / (1 + r) ** t for t, cf in enumerate(cashflows))
    for _ in range(iters):
        mid = (lo + hi) / 2
        if npv(mid) > 0:
            lo = mid
        else:
            hi = mid
    return (lo + hi) / 2


def run(args):
    n = 20000 if args.smoke else 100000
    reps = 10 if args.smoke else 40
    out = {"script": "eq02_supply_finance", "prereg": "S2", "data_tier": "SYNTHETIC",
           "label": "SIMULATION - stipulated income/enrolment DGP; arithmetic policy scenarios",
           "n": n, "reps": reps}
    unit_cost = 1.0
    rows, summary = [], {}
    for scen in ["universal", "means_tested", "quota"]:
        cis, npvs, irrs, bi = [], [], [], None
        for r in range(reps):
            rng_ = rng(args.seed + 100 * ["universal", "means_tested", "quota"].index(scen) + r)
            logy = rng_.normal(size=n)
            y = np.exp(logy)
            q = np.argsort(np.argsort(y)) / (n - 1)
            p_enr = 1 / (1 + np.exp(-(-1.2 + 1.4 * logy + 0.4 * (rng_.random(n) < 0.5))))
            enr = (rng_.random(n) < p_enr).astype(float)
            if scen == "universal":
                benefit = enr * unit_cost
            elif scen == "means_tested":
                benefit = enr * unit_cost * (q <= 0.4)
            else:
                seats = int(enr.sum() * 0.4)
                admitted = np.zeros(n)
                for grp, share in [(q <= 0.4, 0.5), (q > 0.4, 0.5)]:
                    idx = np.where(grp)[0]
                    take = idx[np.argsort(-y[idx])[: int(round(seats * share))]]
                    admitted[take] = 1
                benefit = admitted * unit_cost
            cis.append(concentration(benefit, y))
            bi = np.array([benefit[q >= 0.8].sum(), benefit[(q > 0.6) & (q < 0.8)].sum(),
                           benefit[(q > 0.4) & (q <= 0.6)].sum(), benefit[(q > 0.2) & (q <= 0.4)].sum(),
                           benefit[q <= 0.2].sum()])
            bi = bi / bi.sum()
            cash = [-unit_cost] + [0.25] * 30
            npvs.append(sum(cf / (1.05) ** t for t, cf in enumerate(cash)))
            irrs.append(irr(cash))
            rows.append([scen, r, round(cis[-1], 4), round(npvs[-1], 3), round(irrs[-1], 4),
                         round(float(bi[0]), 3), round(float(bi[-1]), 3)])
        summary[scen] = {"mean_concentration_index": round(float(np.mean(cis)), 4),
                         "ci90": [round(float(np.percentile(cis, 5)), 4), round(float(np.percentile(cis, 95)), 4)],
                         "benefit_share_top_quintile": round(float(np.mean([row[5] for row in rows if row[0] == scen])), 3),
                         "benefit_share_bottom_quintile": round(float(np.mean([row[6] for row in rows if row[0] == scen])), 3),
                         "npv_at_5pct": round(float(np.mean(npvs)), 3),
                         "irr_mean": round(float(np.mean(irrs)), 4)}
    rule = {"universal_more_pro_rich_than_means_tested":
                summary["universal"]["mean_concentration_index"] > summary["means_tested"]["mean_concentration_index"],
            "npv_positive_at_5pct": summary["universal"]["npv_at_5pct"] > 0,
            "irr_above_5pct": summary["universal"]["irr_mean"] > 0.05}
    rule["PASS"] = all(rule.values())
    mv = {"specs": ["universal", "means_tested", "quota"],
          "estimates": {k: summary[k]["mean_concentration_index"] for k in
                        ["universal", "means_tested", "quota"]}}
    mv["range"] = [min(mv["estimates"].values()), max(mv["estimates"].values())]
    mv["spec_robust"] = len({v > 0 for v in mv["estimates"].values()}) == 1
    mv["discount_sensitivity"] = {"npv_5pct": summary["universal"]["npv_at_5pct"]}
    out.update({"summary": summary, "multiverse": mv, "decision_rule": rule,
                "system_map": {"nodes": ["schools-state", "dashboard"], "piece": 1, "chain": "family affordability -> learning -> gate -> credential->jobs"},
           "masseng_boundary": {"used": "standalone synthetic demonstration (NOT MASSENG v5 output)", "mechanism_in_masseng_v5": True, "note": "standalone synthetic demonstration; not a MASSENG v5 output"},
                "plain_result": ("A universal per-student subsidy is pro-rich in this model (concentration index "
                                 "%.3f vs %.3f for means-testing) because enrolment rises with income; the "
                                 "investment arithmetic gives a positive NPV at 5%% and an IRR of %.1f%%. These are "
                                 "arithmetic consequences of the stated assumptions, not policy estimates." %
                                 (summary["universal"]["mean_concentration_index"],
                                  summary["means_tested"]["mean_concentration_index"],
                                  100 * summary["universal"]["irr_mean"]))})
    write_result(args.outdir, "eq02_supply_finance", out)
    save_csv(args.outdir, "eq02_supply_finance",
             ["scenario", "rep", "concentration_index", "npv_5pct", "irr", "benefit_top_q", "benefit_bottom_q"], rows)
    print("PLAIN:", out["plain_result"])
    print("RULE:", rule)
    return out


if __name__ == "__main__":
    run(smoke_parser("S7 education finance / benefit incidence (SIMULATION)"))
