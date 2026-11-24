#!/usr/bin/env python3
"""Dense-grid boundary/equifinality statistics, PRE-REGISTERED metric (v2, clean).

Metric (PREREGISTRATION_PHASE_SWEEP_DENSE + AMENDMENT_01):
  J(pair) = |Δ response| / median(seed SD of the two cells)   [both axes; SD>1e-9 required]
  sharpness = J_max / median(J_edge), J_edge = pairs whose *varying* coordinate is at a grid boundary
  SIGNATURE: sharpness>=2 AND J_max>=4 AND interior AND gate contrast C>0.05
  PARTIAL:   sharpness>=1 or J_max>=2 ; ABSENT otherwise.
SIMULATION ONLY.
"""
import argparse, csv, json, os, statistics as st

RESP = ["tut_q5_q1_gap", "gate_fail_share", "liq_share", "tut_rate", "completion_lower_q_gap"]
SD = {"tut_q5_q1_gap": "sd_tut_q5_q1_gap", "gate_fail_share": "sd_gate_fail_share",
      "liq_share": "sd_liq_share", "tut_rate": "sd_tut_rate",
      "completion_lower_q_gap": "sd_completion_lower_q_gap"}

def load(path, gate):
    rows = []
    for r in csv.DictReader(open(path)):
        if r.get("gate") != gate: continue
        d = {}
        for k, v in r.items():
            try: d[k] = float(v) if v != "" else None
            except ValueError: d[k] = v
        rows.append(d)
    return rows

def jstats(rows, resp):
    """All adjacent pairs along both axes; J normalised by seed SD; edge = varying coord at boundary."""
    xs = sorted({r["x_index"] for r in rows}); ys = sorted({r["y_index"] for r in rows})
    xmin, xmax, ymin, ymax = xs[0], xs[-1], ys[0], ys[-1]
    pairs = []
    # along X: fixed y, adjacent x
    for y in ys:
        rs = sorted([r for r in rows if r["y_index"] == y], key=lambda r: r["x_index"])
        for a, b in zip(rs, rs[1:]):
            va, vb = a.get(resp), b.get(resp)
            if not isinstance(va, (int, float)) or not isinstance(vb, (int, float)): continue
            sds = [s for s in (a.get(SD[resp]), b.get(SD[resp])) if isinstance(s, (int, float)) and s > 1e-9]
            if not sds: continue
            sd = st.median(sds)
            pairs.append({"axis": "X", "J": abs(vb - va) / sd, "delta": vb - va, "fixed": y,
                          "from": a["x_index"], "to": b["x_index"],
                          "edge": a["x_index"] in (xmin, xmax) or b["x_index"] in (xmin, xmax)})
    # along Y: fixed x, adjacent y
    for x in xs:
        rs = sorted([r for r in rows if r["x_index"] == x], key=lambda r: r["y_index"])
        for a, b in zip(rs, rs[1:]):
            va, vb = a.get(resp), b.get(resp)
            if not isinstance(va, (int, float)) or not isinstance(vb, (int, float)): continue
            sds = [s for s in (a.get(SD[resp]), b.get(SD[resp])) if isinstance(s, (int, float)) and s > 1e-9]
            if not sds: continue
            sd = st.median(sds)
            pairs.append({"axis": "Y", "J": abs(vb - va) / sd, "delta": vb - va, "fixed": x,
                          "from": a["y_index"], "to": b["y_index"],
                          "edge": a["y_index"] in (ymin, ymax) or b["y_index"] in (ymin, ymax)})
    if not pairs: return None
    jm = max(pairs, key=lambda p: p["J"])
    edge = [p["J"] for p in pairs if p["edge"]]
    jedge = st.median(edge) if edge else None
    sharp = (jm["J"] / jedge) if jedge and jedge > 0 else None
    return {"J_max": jm["J"], "at": jm, "J_edge_median": jedge, "sharpness": sharp,
            "n_pairs": len(pairs),
            "J_max_X": max([p["J"] for p in pairs if p["axis"] == "X"], default=None),
            "J_max_Y": max([p["J"] for p in pairs if p["axis"] == "Y"], default=None),
            "J_max_X_interior": max([p["J"] for p in pairs if p["axis"] == "X" and not p["edge"]], default=None),
            "J_max_Y_interior": max([p["J"] for p in pairs if p["axis"] == "Y" and not p["edge"]], default=None)}

def equifinal(rows):
    out = []
    for i in range(len(rows)):
        for j in range(i + 1, len(rows)):
            a, b = rows[i], rows[j]
            if not all(isinstance(a.get(k), (int, float)) and isinstance(b.get(k), (int, float))
                       for k in ("completion_lower", "liq_share", "tut_rate")): continue
            dc = abs(a["completion_lower"] - b["completion_lower"])
            dl = abs(a["liq_share"] - b["liq_share"]); dt = abs(a["tut_rate"] - b["tut_rate"])
            if dc < 0.005 and (dl > 0.25 or dt > 0.20):
                out.append({"x_a": a["x_index"], "y_a": a["y_index"], "x_b": b["x_index"], "y_b": b["y_index"],
                            "d_completion_pp": round(100 * dc, 3), "d_liq_pp": round(100 * dl, 2),
                            "d_tut_pp": round(100 * dt, 2)})
    out.sort(key=lambda p: -(p["d_liq_pp"] + p["d_tut_pp"]))
    return out

def contrast(bar, quota, key="tut_q5_q1_gap"):
    q = {(r["x_index"], r["y_index"]): r for r in quota}
    d = [(r[key] - q[(r["x_index"], r["y_index"])][key]) for r in bar
         if (r["x_index"], r["y_index"]) in q and isinstance(r.get(key), (int, float))
         and isinstance(q[(r["x_index"], r["y_index"])].get(key), (int, float))]
    return {"n": len(d), "median_abs": st.median([abs(x) for x in d]) if d else None,
            "max_abs": max((abs(x) for x in d), default=None)}

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--bar", required=True); ap.add_argument("--quota", required=True); ap.add_argument("--out", required=True)
    a = ap.parse_args(); os.makedirs(a.out, exist_ok=True)
    bar, quota = load(a.bar, "bar"), load(a.quota, "quota")
    res = {"label": "SIMULATION ONLY - eduengine toy worlds", "n_cells": {"bar": len(bar), "quota": len(quota)},
           "metric": "J=|d|/median(seed SD), both axes; sharpness=J_max/median(J_edge); edge=varying coord at boundary",
           "stats": {}, "gate_contrast": {}, "equifinal": {}}
    for g, rows in (("bar", bar), ("quota", quota)):
        for r in RESP:
            s = jstats(rows, r)
            if s: res["stats"][f"{g}:{r}"] = s
    C = contrast(bar, quota)["median_abs"] or 0
    res["gate_contrast"]["tut_q5_q1_gap"] = contrast(bar, quota)
    eqs = equifinal(bar) + equifinal(quota)
    res["equifinal"] = {"n_pairs": len(eqs), "top20": eqs[:20]}
    verdicts = {}
    for g in ("bar", "quota"):
        lst = []
        for r in ("tut_q5_q1_gap", "gate_fail_share"):
            s = res["stats"].get(f"{g}:{r}")
            if not s: continue
            # interior candidate = best jump not on an edge
            interior_best = max([v for v in (s["J_max_X_interior"], s["J_max_Y_interior"]) if v is not None], default=0.0)
            jm = s["J_max"]
            sh = s["sharpness"] or 0
            use_j, use_sh = (interior_best, sh) if interior_best >= 1 else (jm, sh)
            if use_sh >= 2 and use_j >= 4 and C > 0.05: v = "SIGNATURE"
            elif use_sh >= 1 or use_j >= 2: v = "PARTIAL"
            else: v = "ABSENT"
            lst.append({"response": r, "verdict": v, "J_max": round(jm, 3), "sharpness": round(sh, 3),
                        "J_max_interior": round(interior_best, 3), "edge_median_J": round(s["J_edge_median"], 3) if s["J_edge_median"] else None,
                        "argmax_axis": s["at"]["axis"], "argmax_from": s["at"]["from"], "argmax_to": s["at"]["to"],
                        "argmax_on_edge": s["at"]["edge"]})
        verdicts[g] = lst
    res["verdict"] = {"cells": verdicts, "gate_contrast_median_abs_tut_gap": C,
                      "rule": "SIGNATURE: interior J>=4 AND sharpness>=2 AND C>0.05; PARTIAL: sharpness>=1 or J>=2"}
    json.dump(res, open(os.path.join(a.out, "dense_boundary_equifinality.json"), "w"), indent=1)
    L = ["# Dense-grid boundary + equifinality, pre-registered metric (SIMULATION ONLY)", "",
         f"cells: bar {len(bar)}, quota {len(quota)}; {res['metric']}", "", "## Verdict"]
    for g, lst in verdicts.items():
        for c in lst:
            L.append(f"- **{g} / {c['response']}**: **{c['verdict']}** — J_max {c['J_max']} (interior {c['J_max_interior']}) "
                     f"at {c['argmax_axis']} axis {c['argmax_from']}→{c['argmax_to']} "
                     f"{'(edge)' if c['argmax_on_edge'] else '(interior)'}; sharpness {c['sharpness']}")
    L += ["", f"- gate contrast (bar vs quota) median |Δtut Q5−Q1 gap| = {C:.4f} (SIGNATURE needs > 0.05)", "",
          "## J_max by axis (interior only)"]
    for k, s in res["stats"].items():
        L.append(f"- {k}: X interior {s['J_max_X_interior']}, Y interior {s['J_max_Y_interior']}, "
                 f"global {s['J_max']:.2f} ({'edge' if s['at']['edge'] else 'interior'})")
    L += ["", f"## Equifinal pairs: **{len(eqs)}**"]
    for p in eqs[:6]:
        L.append(f"- ({p['x_a']},{p['y_a']}) vs ({p['x_b']},{p['y_b']}): Δcompletion {p['d_completion_pp']} pp, "
                 f"Δliq {p['d_liq_pp']} pp, Δtut {p['d_tut_pp']} pp")
    open(os.path.join(a.out, "SUMMARY.md"), "w").write("\n".join(L) + "\n")
    print("\n".join(L))

if __name__ == "__main__":
    main()
