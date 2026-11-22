"""A2 rerun (2026-11-22): within-country log-odds lead test with the outcome standardized (fixes the b_xy - b_yx unit mismatch)
and BH/BY q-values from bootstrap p-values (p_lead = max(p_b, p_diff)). Writes results/final/findings_A2.txt and logodds_within_A2.json."""
import json, os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import final_tests as F
t0 = time.time(); r1 = F.test1(int(sys.argv[1]) if len(sys.argv) > 1 else os.cpu_count())
ks = list(r1); pv = np.array([r1[k]["p_lead"] for k in ks]); m = len(pv); o = np.argsort(pv)
for nm, cm in (("q_bh", 1.0), ("q_by", float(np.sum(1.0 / np.arange(1, m + 1))))):
    q = np.minimum.accumulate((pv[o] * m * cm / np.arange(1, m + 1))[::-1])[::-1].clip(max=1)
    for i, j in enumerate(o):
        r1[ks[j]][nm] = float(q[i])
out = os.path.join(F.OUT); os.makedirs(out, exist_ok=True)
json.dump(r1, open(os.path.join(out, "logodds_within_A2.json"), "w"), indent=1, default=float)
lead = sorted([(k, d) for k, d in r1.items() if d["x_leads_within"]], key=lambda kv: kv[1]["p_lead"])
L = [f"A2 WITHIN-COUNTRY LEADS, log-odds, outcome standardized ({round(time.time() - t0)}s)",
     f"{len(lead)} of {m} ordered pairs pass the raw 90% CI rule; {sum(d['q_bh'] < .10 for _, d in lead)} at BH q<0.10; {sum(d['q_by'] < .10 for _, d in lead)} at BY q<0.10.",
     "b = SD of 10-yr change in outcome per SD of predictor; p from 400-draw country-cluster bootstrap (floor 0.0025).", ""]
L += [f"{k:28s} b={d['b_xy']:+.3f} CI({d['ci_xy'][0]:+.3f},{d['ci_xy'][1]:+.3f}) b_rev={d['b_yx']:+.3f} diffCI({d['ci_diff'][0]:+.3f},{d['ci_diff'][1]:+.3f}) q_bh={d['q_bh']:.3f} q_by={d['q_by']:.3f}" for k, d in lead]
open(os.path.join(out, "findings_A2.txt"), "w").write("\n".join(L) + "\n"); print("\n".join(L[:3]))
