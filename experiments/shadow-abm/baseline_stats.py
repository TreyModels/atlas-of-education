import json, sys
import numpy as np
from pathlib import Path
R = Path("/Users/treymenefee/code/atlas-of-education/experiments/shadow-abm/src/tutoring_abm/results")
F = Path("/Users/treymenefee/code/atlas-of-education/experiments/shadow-abm/src/fresh_tutoring/source_results")
def wq(x, w, q):
    o = np.argsort(x); c = np.cumsum(w[o]); c /= c[-1]
    return float(np.interp(q, c, x[o]))
for v in ["thin", "diversion", "favour", "full"]:
    p = R / f"posterior_{v}.json"
    if not p.exists():
        p = F / f"posterior_{v}.json"
    d = json.load(open(p))
    print(f"== {v} ({p.parent.name}/{p.name}) free={len(d['free'])} particles={len(d['particles'])}")
    for h in d["history"]:
        print("  gen", h.get("gen"), "eps", round(h.get("eps", 0), 3), "ess", round(h["ess"], 1) if "ess" in h else "-",
              "acc", round(h["accept_rate"], 4) if "accept_rate" in h else "-",
              "fit_share", round(h["fit_share_of_proposals"], 4) if "fit_share_of_proposals" in h else "-",
              "ev", f"{h.get('evidence_eps1', 0):.3g}")
    print("  evidence", d["evidence"])
    P = d["particles"]; w = np.array([x["weight"] for x in P]); w = w / w.sum()
    print("  final ESS from weights", round(1 / np.sum(w ** 2), 1))
    for key in ["withholding_mean", "withholding_among_sellers", "teacher_own_share"]:
        if key in P[0]:
            x = np.array([r[key] for r in P])
            print(f"  {key}: weighted median {wq(x, w, .5):.4f}, p05 {wq(x, w, .05):.4f}, p95 {wq(x, w, .95):.4f}, share<0.01 {np.sum(w*(x<0.01)):.3f}")
    if "nonbuyer_class_instruction" in P[0]:
        x = np.array([r["nonbuyer_class_instruction"] for r in P]); print("  nonbuyer_class_instruction median", round(wq(x, w, .5), 4))
    print("  distance median (weighted)", round(wq(np.array([r["distance"] for r in P]), w, .5), 4), "max", round(max(r["distance"] for r in P), 4))
