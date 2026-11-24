#!/usr/bin/env python3
"""X2 analysis — applies the pre-declared hypotheses/thresholds/falsifiers to results_x2.json.

Paired by seed. Material threshold 1 pp (0.01); 90 % seed-bootstrap CI (4,000 draws).
Writes audit_tables/summary_x2.json and prints the pre-declared verdicts. Simulation only.
"""
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "audit_tables")
RNG = np.random.default_rng(20261125)
B = 4000
THR = 0.01  # 1 pp material threshold (pre-declared)
ACC = (0.2, 0.4, 0.8)
BANS = (0.0, 1.0)
GATE_ADJ = [5, 8, 11]   # grades 6/9/12 (1-based)
NON_GATE = [3, 6, 9, 12]  # grades 4/7/10/13 (1-based)
# NOTE: 0-based grade indices; grade g_index+1. Gate-adjacent and non-gate sets overlap only if indices
# collide; they do not (5,8,11 vs 3,6,9,12). Declared in the prereg by grade number.


def boot_ci(d, q=0.90):
    d = np.asarray(d, float)
    bs = np.mean(RNG.choice(d, size=(B, len(d)), replace=True), axis=1)
    return [float(np.quantile(bs, (1 - q) / 2)), float(np.quantile(bs, 1 - (1 - q) / 2))]


def mean_ci(vals):
    v = np.asarray(vals, float)
    return {"mean": float(v.mean()), "ci90": boot_ci(v), "n": int(len(v)),
            "n_pos": int((v > 0).sum()), "n_neg": int((v < 0).sum()),
            "sign_stable": bool((v > 0).all() or (v < 0).all())}


def material(st):
    return bool(abs(st["mean"]) >= THR and (st["ci90"][0] > 0 or st["ci90"][1] < 0))


def material_pos(st):
    return bool(st["mean"] >= THR and st["ci90"][0] > 0)


def material_neg(st):
    return bool(st["mean"] <= -THR and st["ci90"][1] < 0)


def load():
    with open(os.path.join(HERE, "results_x2_EXPLORATORY.json")) as f:
        return json.load(f)


def rowval(r, m):
    x = r["metrics"].get(m)
    return None if x is None else x


def derived(r):
    g = rowval(r, "tut_by_grade")
    q = rowval(r, "tut_by_q")
    out = {"tut_rate": rowval(r, "tut_rate"),
           "gate_adj": float(np.mean([g[i] for i in GATE_ADJ])) if g else None,
           "non_gate": float(np.mean([g[i] for i in NON_GATE])) if g else None,
           "wealth_gap_tut": (q[4] - q[0]) if q else None,
           "own_share": rowval(r, "own_share"),
           "firm_price": rowval(r, "firm_price")}
    for m in ("completion_primary", "completion_lower", "completion_upper", "completion_tertiary",
              "parity_location_lower", "parity_location_upper", "parity_wealth_lower", "parity_wealth_upper",
              "mpl_primary", "q_pub", "formal_share_gdp"):
        out[m] = rowval(r, m)
    for lvl in ("lower", "upper", "tertiary"):
        arr = rowval(r, f"completion_{lvl}_q")
        out[f"wealth_gap_completion_{lvl}"] = (arr[4] - arr[0]) if arr else None
    return out


def main():
    os.makedirs(OUT, exist_ok=True)
    d = load()
    rows = d["rows"]
    idx = {(r["gate"], r["rural_firm_access"], r["own_ban"], r["seed"]): derived(r) for r in rows}
    seeds = list(range(20))
    metrics = ["tut_rate", "gate_adj", "non_gate", "wealth_gap_tut", "own_share",
               "completion_primary", "completion_lower", "completion_upper", "completion_tertiary",
               "parity_location_lower", "parity_location_upper",
               "wealth_gap_completion_lower", "wealth_gap_completion_upper", "wealth_gap_completion_tertiary",
               "mpl_primary", "q_pub", "formal_share_gdp"]
    summary = {"label": "X2 gate/tutoring inequality factorial — pre-declared analysis",
               "runs": len(rows), "elapsed_s": d["elapsed_s"],
               "threshold_pp": THR, "gate_adjacent_grades_1based": [6, 9, 12],
               "non_gate_grades_1based": [4, 7, 10, 13],
               "surfaces": {}, "paired_contrasts": {}, "hypotheses": {}}

    # full factorial surface (mean over 20 seeds + CI over seeds)
    surf = {}
    for gate in ("bar", "quota"):
        for a in ACC:
            for ban in BANS:
                vals = {m: [idx[(gate, a, ban, s)][m] for s in seeds] for m in metrics}
                surf[f"{gate}|access{a}|ban{ban:g}"] = {m: mean_ci([v for v in vs if v is not None])
                                                       for m, vs in vals.items()}
    summary["surfaces"] = surf

    def paired_contrast(k1, k2, label):
        """k1,k2 are (gate,access,ban) tuples; paired over seeds."""
        out = {}
        for m in metrics:
            diffs = [idx[k1 + (s,)][m] - idx[k2 + (s,)][m] for s in seeds
                     if idx[k1 + (s,)][m] is not None and idx[k2 + (s,)][m] is not None]
            out[m] = mean_ci(diffs) if diffs else {"status": "insufficient"}
        summary["paired_contrasts"][label] = out
        return out

    # quota - bar, by access and ban
    qb = {}
    for ban in BANS:
        for a in ACC:
            qb[f"access{a}|ban{ban:g}"] = paired_contrast(("quota", a, ban), ("bar", a, ban),
                                                          f"quota_minus_bar|access{a}|ban{ban:g}")
    # ban on - off, by gate and access
    for gate in ("bar", "quota"):
        for a in ACC:
            paired_contrast((gate, a, 1.0), (gate, a, 0.0), f"ban1_minus_ban0|{gate}|access{a}")
    # access 0.8 - 0.2, by gate and ban
    for gate in ("bar", "quota"):
        for ban in BANS:
            paired_contrast((gate, 0.8, ban), (gate, 0.2, ban), f"access0.8_minus_0.2|{gate}|ban{ban:g}")

    # ---------------- pre-declared hypotheses ----------------
    H = {}
    # H1: quota raises overall + gate-adjacent tutoring at ban=0, >=2/3 access levels both material positive
    rows_h1 = []
    for a in ACC:
        c = qb[f"access{a}|ban0"]
        rows_h1.append({"access": a,
                        "tut_rate": c["tut_rate"], "gate_adj": c["gate_adj"],
                        "tut_rate_material_pos": material_pos(c["tut_rate"]),
                        "gate_adj_material_pos": material_pos(c["gate_adj"])})
    ok_both = [r for r in rows_h1 if r["tut_rate_material_pos"] and r["gate_adj_material_pos"]]
    any_neg = any(material_neg(qb[f"access{a}|ban0"]["tut_rate"]) or material_neg(qb[f"access{a}|ban0"]["gate_adj"]) for a in ACC)
    H["H1_gate_prep"] = {"supported": bool(len(ok_both) >= 2 and not any_neg),
                         "falsifier_confirmed": bool(len(ok_both) <= 1 or any_neg),
                         "per_access": rows_h1, "n_access_both_material_pos": len(ok_both),
                         "rule": "both tut_rate and gate-adjacent tutoring material-positive (>=1pp, 90% CI excludes 0) in >=2/3 access levels at ban=0"}
    # H1b: ban reduces tutoring, >=2/3 access levels both gates
    rows_h1b = []
    for gate in ("bar", "quota"):
        for a in ACC:
            c = summary["paired_contrasts"][f"ban1_minus_ban0|{gate}|access{a}"]
            rows_h1b.append({"gate": gate, "access": a, "tut_rate": c["tut_rate"],
                             "material_neg": material_neg(c["tut_rate"])})
    for gate in ("bar", "quota"):
        n = sum(1 for r in rows_h1b if r["gate"] == gate and r["material_neg"])
        H.setdefault("H1b_ban", {})[gate] = {"n_access_material_neg": n, "supported": bool(n >= 2)}
    H["H1b_ban"]["supported"] = bool(H["H1b_ban"]["bar"]["supported"] and H["H1b_ban"]["quota"]["supported"])
    H["H1b_ban"]["falsifier_confirmed"] = not H["H1b_ban"]["supported"]
    H["H1b_ban"]["per_cell"] = rows_h1b
    # H2: quota widens top-bottom tutoring gap (ban=0), >=2/3 access levels
    rows_h2 = [{"access": a, "quota_minus_bar_wealth_gap_tut": qb[f"access{a}|ban0"]["wealth_gap_tut"],
                "material_pos": material_pos(qb[f"access{a}|ban0"]["wealth_gap_tut"])} for a in ACC]
    n_h2 = sum(1 for r in rows_h2 if r["material_pos"])
    any_neg_h2 = any(material_neg(qb[f"access{a}|ban0"]["wealth_gap_tut"]) for a in ACC)
    H["H2_wealth_gap_widening"] = {"supported": bool(n_h2 >= 2 and not any_neg_h2),
                                    "falsifier_confirmed": bool(n_h2 <= 1 or any_neg_h2),
                                    "per_access": rows_h2, "n_material_pos": n_h2,
                                    "rule": "top-bottom tutoring gap quota-bar material-positive in >=2/3 access levels at ban=0"}
    # H3: access 0.8 vs 0.2 reduces wealth gap, both gates (ban=0)
    rows_h3 = []
    for gate in ("bar", "quota"):
        c = summary["paired_contrasts"][f"access0.8_minus_0.2|{gate}|ban0"]
        rows_h3.append({"gate": gate, "gap_diff": c["wealth_gap_tut"],
                        "material_neg": material_neg(c["wealth_gap_tut"])})
    H["H3_access_gradient"] = {"supported": bool(all(r["material_neg"] for r in rows_h3)),
                                "falsifier_confirmed": bool(not all(r["material_neg"] for r in rows_h3)),
                                "per_gate": rows_h3,
                                "rule": "wealth tutoring gap (access0.8 - access0.2) material-negative in BOTH gates at ban=0"}
    # gate-specificity DiD (quota-bar on gate-adjacent minus non-gate), ban=0
    did = {}
    for a in ACC:
        g = qb[f"access{a}|ban0"]["gate_adj"]; n = qb[f"access{a}|ban0"]["non_gate"]
        dm = g["mean"] - n["mean"]
        # bootstrap on the paired difference of paired differences
        diffs = [(idx[("quota", a, 0.0, s)]["gate_adj"] - idx[("quota", a, 0.0, s)]["non_gate"])
                 - (idx[("bar", a, 0.0, s)]["gate_adj"] - idx[("bar", a, 0.0, s)]["non_gate"])
                 for s in seeds]
        st = mean_ci(diffs)
        st["material_pos"] = material_pos(st)
        did[f"access{a}"] = st
    H["gate_specificity_DiD"] = {"per_access": did,
                                  "material_pos_count": sum(1 for v in did.values() if v["material_pos"]),
                                  "interpretation": "if material-positive, the quota tutoring response is gate-concentrated (gate arithmetic); if not, it is broader"}
    summary["hypotheses"] = H
    with open(os.path.join(OUT, "summary_x2.json"), "w") as f:
        json.dump(summary, f, indent=1)
    print(json.dumps({"H1": {"supported": H["H1_gate_prep"]["supported"],
                             "falsifier_confirmed": H["H1_gate_prep"]["falsifier_confirmed"],
                             "n_access_both_material_pos": H["H1_gate_prep"]["n_access_both_material_pos"],
                             "per_access": [{"access": r["access"], "tut_rate": round(r["tut_rate"]["mean"], 4),
                                             "gate_adj": round(r["gate_adj"]["mean"], 4),
                                             "pos": (r["tut_rate_material_pos"], r["gate_adj_material_pos"])}
                                            for r in rows_h1]},
                      "H1b": {"supported": H["H1b_ban"]["supported"]},
                      "H2": {"supported": H["H2_wealth_gap_widening"]["supported"],
                             "falsifier_confirmed": H["H2_wealth_gap_widening"]["falsifier_confirmed"],
                             "n_material_pos": H["H2_wealth_gap_widening"]["n_material_pos"],
                             "per_access": [{"access": r["access"], "gap_diff": round(r["quota_minus_bar_wealth_gap_tut"]["mean"], 4),
                                             "pos": r["material_pos"]} for r in rows_h2]},
                      "H3": {"supported": H["H3_access_gradient"]["supported"],
                             "per_gate": [{"gate": r["gate"], "gap_diff": round(r["gap_diff"]["mean"], 4),
                                           "neg": r["material_neg"]} for r in rows_h3]},
                      "DiD": {"material_pos_count": H["gate_specificity_DiD"]["material_pos_count"],
                              "per_access": {k: round(v["mean"], 4) for k, v in did.items()}}}, indent=1))


if __name__ == "__main__":
    main()
