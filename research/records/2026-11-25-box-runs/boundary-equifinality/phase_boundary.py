#!/usr/bin/env python3
"""Boundary + equifinality statistics on the pre-registered phase sweeps (SIMULATION ONLY).

Inputs (already pulled from the box, no new runs):
  ~/neon-boot/pulled/phase-sweep-dense/phase_sweep_quick_summary.csv     gate=bar, 10x10, 20 seeds
  ~/neon-boot/pulled/phase-sweep-quota/phase_sweep_quick_summary.csv     gate=quota, 10x10, 5 seeds
Outputs: report JSON + pair CSV + human-readable summary in --out.

Statistics (all pre-declared in PREREGISTRATION_PHASE_SWEEP.md: J_edge, sharpness, C, equifinal pairs):
 - J_max / sharpness: max adjacent-cell jump in a response along the fee axis (Y) at each vacancy
   level (X), normalised by the median absolute level; reported per gate.
 - gate contrast C: same (x,y) cell, bar vs quota, for tutorial Q5-Q1 gap / liq_share / gate_fail_share.
 - equifinal pairs: cell pairs with |d(completion_lower)| < 0.5 pp but |d(liq_share)| > 25 pp or
   |d(tut_rate)| > 20 pp (the auditor's threshold), listed with both cells' axes.
No causal language. Simulation only.
"""
import argparse, csv, json, os, statistics as st

KEEP = ["x_index","x_vac0","y_index","fee_primary","completion_lower","completion_upper",
        "liq_share","gate_fail_share","tut_rate","tut_q5_q1_gap","tut_share_q1","tut_share_q5",
        "completion_lower_q_gap","parity_wealth_lower","formal_rate"]

def load(path, gate):
    rows=[]
    with open(path) as f:
        for r in csv.DictReader(f):
            if r.get("gate")!=gate: continue
            d={}
            for k in KEEP:
                if k in r and r[k]!="":
                    try: d[k]=float(r[k])
                    except ValueError: d[k]=r[k]
            rows.append(d)
    return rows

def jumps(rows, key, axis="fee_primary"):
    """max |adjacent jump| along axis within each level of the other axis, normalised."""
    by={}
    for r in rows:
        other = r["x_index"] if axis=="fee_primary" else r["y_index"]
        by.setdefault(other, []).append(r)
    out=[]
    for o, rs in by.items():
        rs=sorted(rs, key=lambda r: r[axis])
        vals=[(r[axis], r[key]) for r in rs if isinstance(r.get(key),(int,float))]
        for (a0,v0),(a1,v1) in zip(vals, vals[1:]):
            da=abs(a1-a0)
            if da==0: continue
            out.append({"other":o,"from":a0,"to":a1,"delta":v1-v0,"slope":(v1-v0)/da})
    if not out: return None
    j=max(out, key=lambda x: abs(x["delta"]))
    base=st.median([abs(v) for v in [r.get(key) for r in rows] if isinstance(v,(int,float))] or [0]) or 1e-9
    return {"J_max":j["delta"], "at":j, "sharpness":abs(j["delta"])/base, "n_segments":len(out)}

def equifinal(rows):
    pairs=[]
    for i in range(len(rows)):
        for j in range(i+1, len(rows)):
            a,b=rows[i],rows[j]
            if not all(isinstance(a.get(k),(int,float)) and isinstance(b.get(k),(int,float))
                       for k in ("completion_lower","liq_share","tut_rate")): continue
            dcomp=abs(a["completion_lower"]-b["completion_lower"])
            dliq=abs(a["liq_share"]-b["liq_share"])
            dtut=abs(a["tut_rate"]-b["tut_rate"])
            if dcomp<0.005 and (dliq>0.25 or dtut>0.20):
                pairs.append({"x_a":a["x_index"],"y_a":a["y_index"],"x_b":b["x_index"],"y_b":b["y_index"],
                              "d_completion_lower_pp":round(100*dcomp,3),
                              "d_liq_pp":round(100*dliq,2),"d_tut_pp":round(100*dtut,2)})
    pairs.sort(key=lambda p:-(p["d_liq_pp"]+p["d_tut_pp"]))
    return pairs

def contrast(bar, quota, key):
    q={(r["x_index"],r["y_index"]):r for r in quota}
    out=[]
    for r in bar:
        o=q.get((r["x_index"],r["y_index"]))
        if o and isinstance(r.get(key),(int,float)) and isinstance(o.get(key),(int,float)):
            out.append({"x":r["x_index"],"y":r["y_index"],"bar":r[key],"quota":o[key],"diff":r[key]-o[key]})
    return out

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("--bar", default=os.path.expanduser("~/neon-boot/pulled/phase-sweep-dense/phase_sweep_quick_summary.csv"))
    ap.add_argument("--quota", default=os.path.expanduser("~/neon-boot/pulled/phase-sweep-quota/phase_sweep_quick_summary.csv"))
    ap.add_argument("--out", required=True)
    a=ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    bar=load(a.bar,"bar"); quota=load(a.quota,"quota")
    resp=["tut_q5_q1_gap","liq_share","gate_fail_share","tut_rate","completion_lower","completion_lower_q_gap"]
    res={"label":"SIMULATION ONLY - eduengine toy worlds; illustrative; no causal claims",
         "n_cells_bar":len(bar),"n_cells_quota":len(quota),
         "boundary":{}, "gate_contrast":{}, "equifinal":{}}
    for k in resp:
        res["boundary"][f"bar:{k}"]=jumps(bar,k)
        res["boundary"][f"quota:{k}"]=jumps(quota,k)
    for k in ["tut_q5_q1_gap","liq_share","gate_fail_share"]:
        c=contrast(bar,quota,k); res["gate_contrast"][k]={
            "n_cells":len(c),
            "median_abs_diff":st.median([abs(x["diff"]) for x in c]) if c else None,
            "max_abs_diff":max((abs(x["diff"]) for x in c), default=None)}
    eqs=equifinal(bar)+equifinal(quota)
    res["equifinal"]={"n_pairs":len(eqs),"thresholds":{"d_completion_lower_pp":0.5,"d_liq_pp":25,"d_tut_pp":20},
                      "top20":eqs[:20]}
    json.dump(res, open(os.path.join(a.out,"boundary_equifinality.json"),"w"), indent=1)
    with open(os.path.join(a.out,"equifinal_pairs.csv"),"w",newline="") as f:
        w=csv.DictWriter(f, fieldnames=list(eqs[0].keys())) if eqs else None
        if w: w.writeheader(); w.writerows(eqs)
    # readable summary
    L=["# Phase-diagram boundary + equifinality (SIMULATION ONLY)","",
       f"cells: bar {len(bar)} (20 seeds), quota {len(quota)} (5 seeds)","",
       "## Sharpest adjacent-cell jump along the fee (liquidity) axis, per response"]
    for k in resp:
        for g in ("bar","quota"):
            j=res["boundary"][f"{g}:{k}"]
            if j: L.append(f"- **{g} / {k}**: J_max = {j['J_max']:+.4f} at x={j['at']['other']} "
                                f"({j['at']['from']:.2f}->{j['at']['to']:.2f}), sharpness = {j['sharpness']:.2f}")
    L+=["","## Gate contrast (same cell, bar vs quota)"]
    for k,v in res["gate_contrast"].items():
        if v["n_cells"]: L.append(f"- {k}: median |diff| = {v['median_abs_diff']:.4f}, max |diff| = {v['max_abs_diff']:.4f} over {v['n_cells']} cells")
    L+=["","## Equifinal pairs (same completion level, different liquidity/tutoring)",
        f"- total pairs meeting thresholds: **{len(eqs)}**"]
    for p in eqs[:5]:
        L.append(f"- completion_lower within {p['d_completion_lower_pp']} pp but Δliq {p['d_liq_pp']} pp / Δtut {p['d_tut_pp']} pp: "
                 f"(x{p['x_a']},y{p['y_a']}) vs (x{p['x_b']},y{p['y_b']})")
    open(os.path.join(a.out,"SUMMARY.md"),"w").write("\n".join(L)+"\n")
    print("\n".join(L))

if __name__=="__main__": main()
