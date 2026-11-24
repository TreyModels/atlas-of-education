#!/usr/bin/env python3
"""Binding-gate experiment analysis (pre-registered in research/binding-gate-2026-11-25 @37cbe3d).

Inputs: per-share CSVs from phase_sweep_binding.py (bar arm + quota arms S in 0.25..0.70).
Outputs: interaction contrast (primary test), monotonicity, per-share table, equifinality count.

H2 (primary): (gap(fee=0.19) - gap(fee=0.00)) at S=0.25  MINUS  same at S=0.70  > 0, seed CIs disjoint.
H1: Spearman rho of mean gap vs S < 0 AND gap(S=0.25)-gap(S=0.70) > 0 with disjoint seed CIs.
SIMULATION ONLY.
"""
import argparse, csv, json, os, statistics as st

def load(path):
    rows = []
    for r in csv.DictReader(open(path)):
        d = {"gate": r["gate"], "share": r.get("share")}
        for k, v in r.items():
            if k in ("gate", "share"): continue
            try: d[k] = float(v) if v != "" else None
            except ValueError: d[k] = v
        rows.append(d)
    return rows

def cell_mean(rows, x, y, key):
    v = [r[key] for r in rows if r["x_index"] == x and r["y_index"] == y and isinstance(r.get(key), (int, float))]
    return st.mean(v) if v else None

def gap_by_fee(rows, fee_lo_y, fee_hi_y, key="tut_q5_q1_gap"):
    """Mean over vacancy levels of (mean at high fee - mean at low fee)."""
    xs = sorted({r["x_index"] for r in rows})
    diffs = []
    for x in xs:
        lo = cell_mean(rows, x, fee_lo_y, key); hi = cell_mean(rows, x, fee_hi_y, key)
        if lo is not None and hi is not None: diffs.append(hi - lo)
    return (st.mean(diffs) if diffs else None), diffs

def spearman(xs, ys):
    n = len(xs)
    def rank(v):
        s = sorted(range(n), key=lambda i: v[i])
        r = [0]*n
        for pos, i in enumerate(s): r[i] = pos + 1
        return r
    rx, ry = rank(xs), rank(ys)
    mx, my = st.mean(rx), st.mean(ry)
    num = sum((a-mx)*(b-my) for a, b in zip(rx, ry))
    den = (sum((a-mx)**2 for a in rx) * sum((b-my)**2 for b in ry)) ** 0.5
    return num/den if den else None

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="dir containing share_* subdirs with CSVs")
    ap.add_argument("--out", required=True)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    shares = {}
    for name in sorted(os.listdir(a.root)):
        p = os.path.join(a.root, name, "phase_sweep_quick_summary.csv")
        if os.path.exists(p): shares[name] = load(p)
    res = {"label": "SIMULATION ONLY - eduengine toy worlds", "arms": {}, "H2_primary": {}, "H1": {}}
    per_share = {}
    for name, rows in shares.items():
        # fee levels: y index last = 0.19, index 0 = 0.0
        ys = sorted({r["y_index"] for r in rows})
        lo_y, hi_y = ys[0], ys[-1]
        fee_lo = next((r["fee_primary"] for r in rows if r["y_index"] == lo_y), None)
        fee_hi = next((r["fee_primary"] for r in rows if r["y_index"] == hi_y), None)
        gap, diffs = gap_by_fee(rows, lo_y, hi_y)
        gatefail_gap, _ = gap_by_fee(rows, lo_y, hi_y, "gate_fail_share")
        tut_mean = st.mean([r["tut_q5_q1_gap"] for r in rows if isinstance(r.get("tut_q5_q1_gap"), (int, float))])
        per_share[name] = {"n_rows": len(rows), "fee_lo": fee_lo, "fee_hi": fee_hi,
                           "mean_tut_gap": tut_mean, "E8_gap_effect": gap, "E8_gatefail_effect": gatefail_gap,
                           "per_vac_level": diffs}
    res["arms"] = per_share
    # H2: quota arms with share parsed from dir name
    quota = {}
    for name, d in per_share.items():
        if name.startswith("share_"):
            try: S = float(name.split("_")[1])
            except ValueError: continue
            quota[S] = d
    if len(quota) >= 2:
        Ss = sorted(quota)
        lo_name, hi_name = f"share_{Ss[0]}", f"share_{Ss[-1]}"
        d1 = quota[Ss[0]]["E8_gap_effect"]; d2 = quota[Ss[-1]]["E8_gap_effect"]
        inter = (d1 - d2) if (d1 is not None and d2 is not None) else None
        # crude CI from per-vac-level dispersion
        def mean_sd(v): return (st.mean(v), st.stdev(v) / len(v) ** 0.5) if len(v) > 1 else (v[0], 0.0) if v else (None, None)
        m1, s1 = mean_sd(quota[Ss[0]]["per_vac_level"]); m2, s2 = mean_sd(quota[Ss[-1]]["per_vac_level"])
        se = (s1 ** 2 + s2 ** 2) ** 0.5 if (s1 is not None and s2 is not None) else None
        res["H2_primary"] = {"S_lo": Ss[0], "S_hi": Ss[-1], "E8_effect_at_S_lo": m1, "E8_effect_at_S_hi": m2,
                             "interaction": inter, "se_approx": se,
                             "ci95": [inter - 1.96*se, inter + 1.96*se] if (inter is not None and se) else None,
                             "verdict": ("SUPPORTED" if (inter is not None and se and inter > 1.96*se)
                                         else "UNDERPOWERED" if (inter is not None and inter > 0) else "NOT SUPPORTED")}
        means = [quota[S]["mean_tut_gap"] for S in Ss]
        rho = spearman(Ss, means)
        diff = (quota[Ss[0]]["mean_tut_gap"] - quota[Ss[-1]]["mean_tut_gap"]) if all(m is not None for m in means) else None
        res["H1"] = {"shares": Ss, "mean_tut_gap_by_share": means, "spearman_rho": rho,
                     "gap_low_share_minus_high_share": diff,
                     "verdict": ("SUPPORTED" if (rho is not None and rho < 0 and diff is not None and diff > 0) else "NOT SUPPORTED")}
    json.dump(res, open(os.path.join(a.out, "binding_gate_analysis.json"), "w"), indent=1)
    L = ["# Binding-gate experiment (SIMULATION ONLY)", "",
         "## Per-arm summary", "| arm | rows | mean Q5-Q1 tut gap | E8 gap effect (fee .19 vs .00) | E8 gate-fail effect |",
         "|---|---|---|---|---|"]
    for k, d in per_share.items():
        L.append(f"| {k} | {d['n_rows']} | {d['mean_tut_gap']:.4f} | {d['E8_gap_effect']:+.4f} | {d['E8_gatefail_effect']:+.4f} |")
    if res.get("H2_primary"):
        h = res["H2_primary"]
        L += ["", "## H2 (primary, pre-registered)", f"- interaction = E8 effect at S={h['S_lo']} minus S={h['S_hi']}: "
              f"**{h['interaction']:+.4f}** (se≈{h['se_approx']:.4f}, 95% CI {h['ci95']})", f"- verdict: **{h['verdict']}**"]
    if res.get("H1"):
        h = res["H1"]
        L += ["", "## H1", f"- mean tut gap by share: " + ", ".join(f"S={s}: {m:.4f}" for s, m in zip(h["shares"], h["mean_tut_gap_by_share"])),
              f"- Spearman rho {h['spearman_rho']:+.3f}; gap(S_lo)-gap(S_hi) {h['gap_low_share_minus_high_share']:+.4f}", f"- verdict: **{h['verdict']}**"]
    open(os.path.join(a.out, "SUMMARY.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    main()
