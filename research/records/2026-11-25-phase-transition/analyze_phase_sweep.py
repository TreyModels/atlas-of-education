#!/usr/bin/env python3
"""Boundary statistics + phase diagrams for the phase sweep — SIMULATION ONLY.

Pre-registered analysis (PREREGISTRATION_PHASE_SWEEP.md, commit 408aa3e):
  J_edge  = |M_a - M_b| / sigma_med  over axis-adjacent cell pairs, sigma_med = median seed SD of M
  J_max, edge, sharpness = J_max / median(J_edge)
  step-vs-linear: best one-break step fit vs linear fit; Delta R^2
  gate contrast C = mean(J_edge | bar) / mean(J_edge | quota)
  decision rule as declared (J_max >= 4, sharpness >= 2, C >= 2, regressive direction).

Two sources (same pre-registered design, same engine hashes, same seeds):
  --source box    the warm-box quick runs (500+500 = 200 cells x 5 seeds); CSVs pulled by server-runner
  --source local  the local full sweep summary JSON (adds gate-pass/formal-hire quintile read-outs)

Writes results/boundary_stats_<source>.json and results/PHASE_DIAGRAMS_<source>.md. numpy only.
"""
import argparse
import csv
import json
import os
import sys

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, "results")
SIGMA_FLOOR = 0.002
METRIC_ORDER = ["tut_q5_q1_gap", "tut_rate", "q1_liq_share", "q1_gate_fail_share", "gate_fail_share",
                "gate_pass_q_gap", "completion_lower_q_gap", "completion_upper_q_gap",
                "q1_censored_share", "formal_rate", "liq_share", "censored_share"]
GATES = ["bar", "quota"]
STRESS_METRICS = ("tut_q5_q1_gap", "completion_lower_q_gap", "q1_gate_fail_share", "gate_pass_q_gap")


def _num(v):
    if v is None or v == "":
        return None
    try:
        return float(v)
    except ValueError:
        return None


def load_box(box_dir):
    import glob
    cells = []
    files = sorted(glob.glob(os.path.join(box_dir, "*.csv")) +
                   glob.glob(os.path.join(box_dir, "bar_latest", "*.csv")))
    files = [f for f in files if f.endswith("_summary.csv")]
    for fn in files:
        with open(fn, newline="") as f:
            for r in csv.DictReader(f):
                gate = r.get("gate")
                if not gate:
                    continue
                c = {"gate": gate}
                for k, v in r.items():
                    if k == "gate":
                        continue
                    if k in ("x_index", "y_index", "n_seeds"):
                        c[k] = int(float(v))
                    else:
                        c[k] = _num(v)
                for src, dst in (("liq_share_q1", "q1_liq_share"), ("gate_fail_share_q1", "q1_gate_fail_share"),
                                 ("liq_share_q5", "q5_liq_share"), ("gate_fail_share_q5", "q5_gate_fail_share")):
                    if src in c:
                        c[dst] = c[src]
                cells.append(c)
    gates = sorted({c["gate"] for c in cells})
    meta = {"source": "box_quick", "design": {
        "X_vac0_formal_vacancies_per_entrant": sorted({c["x_vac0"] for c in cells}),
        "Y_fee_primary_share_of_median_income": sorted({c["fee_primary"] for c in cells}),
        "gate": gates, "n_cells": len(cells), "seeds": 5, "N": 400, "T": 70, "measure_from": 35,
        "base_world": "formal_loop", "queue_on": True,
        "note": "500 runs per gate on autodl-container-a8f742b5ee-292349c5 (12 workers); engine hashes equal "
                "the committed server run; exits from e.exits only, censored its own category; "
                "bar_binding is an EXPLORATORY post-hoc arm, not part of the pre-registered decision rule"}}
    return meta, cells


def load_local(results_dir):
    with open(os.path.join(results_dir, "phase_sweep_summary.json")) as f:
        d = json.load(f)
    return d["meta"], d["cells"]


def available(cells, metric):
    return sum(1 for c in cells if c.get(metric) is not None) >= 0.9 * len(cells)


def grid(cells, gate, metric):
    cc = [c for c in cells if c["gate"] == gate]
    xs = sorted({c["x_vac0"] for c in cc})
    ys = sorted({c["fee_primary"] for c in cc})
    M = np.full((len(ys), len(xs)), np.nan)
    S = np.full((len(ys), len(xs)), np.nan)
    for c in cc:
        i, j = ys.index(c["fee_primary"]), xs.index(c["x_vac0"])
        if c.get(metric) is not None:
            M[i, j] = c[metric]
        if c.get(f"sd_{metric}") is not None:
            S[i, j] = c[f"sd_{metric}"]
    return xs, ys, M, S


def edge_stats(xs, ys, M, S):
    sig = np.nanmedian(S)
    sig = max(float(sig) if np.isfinite(sig) else 0.0, SIGMA_FLOOR)
    edges = []
    ny, nx = M.shape
    for i in range(ny):
        for j in range(nx):
            if not np.isfinite(M[i, j]):
                continue
            if j + 1 < nx and np.isfinite(M[i, j + 1]):
                edges.append(dict(axis="X", a=[xs[j], ys[i]], b=[xs[j + 1], ys[i]],
                                  dM=float(M[i, j + 1] - M[i, j])))
            if i + 1 < ny and np.isfinite(M[i + 1, j]):
                edges.append(dict(axis="Y", a=[xs[j], ys[i]], b=[xs[j], ys[i + 1]],
                                  dM=float(M[i + 1, j] - M[i, j])))
    for e in edges:
        e["J"] = abs(e["dM"]) / sig
    Js = np.array([e["J"] for e in edges]) if edges else np.array([])
    med = float(np.median(Js)) if len(Js) else float("nan")
    mx = max(edges, key=lambda e: e["J"]) if edges else None
    return dict(sigma_med=sig, J_max=float(mx["J"]) if mx else None, edge_max=mx,
                sharpness=float(mx["J"] / med) if mx and med > 0 else None, J_median=med, n_edges=len(edges))


def step_vs_linear(seq, coords):
    seq = np.asarray(seq, float); x = np.asarray(coords, float)
    ok = np.isfinite(seq); seq, x = seq[ok], x[ok]
    n = len(seq)
    if n < 4:
        return None
    sst = float(np.sum((seq - seq.mean()) ** 2))
    if sst <= 0:
        return None
    A = np.vstack([x, np.ones(n)]).T
    coef, *_ = np.linalg.lstsq(A, seq, rcond=None)
    r2_lin = 1 - float(np.sum((seq - A @ coef) ** 2)) / sst
    best = None
    for k in range(1, n):
        pred = np.where(np.arange(n) < k, seq[:k].mean(), seq[k:].mean())
        sse = float(np.sum((seq - pred) ** 2))
        if best is None or sse < best[1]:
            best = (k, sse)
    r2_step = 1 - best[1] / sst
    return dict(dR2=float(r2_step - r2_lin), r2_linear=float(r2_lin), r2_step=float(r2_step),
                break_index=int(best[0]), break_coord=float(x[best[0]]) if best[0] < n else None)


def direction_ok(edge):
    if edge is None:
        return None
    if edge["axis"] == "X":      # b is slacker (larger vac0); regressive = higher stress at tighter X = a
        return bool(edge["dM"] < 0)
    return bool(edge["dM"] > 0)  # b is higher fee; regressive = higher stress at lower fee = a


def analyse_gate(cells, gate, metrics):
    out = {}
    for m in metrics:
        xs, ys, M, S = grid(cells, gate, m)
        es = edge_stats(xs, ys, M, S)
        sv = []
        for i, yv in enumerate(ys):
            r = step_vs_linear(M[i, :], xs)
            if r:
                sv.append(dict(axis="X", fixed=yv, **r))
        for j, xv in enumerate(xs):
            r = step_vs_linear(M[:, j], ys)
            if r:
                sv.append(dict(axis="Y", fixed=xv, **r))
        best = max(sv, key=lambda d: d["dR2"]) if sv else None
        out[m] = {**es, "step_best": best, "direction_ok": direction_ok(es["edge_max"]),
                  "range": [float(np.nanmin(M)), float(np.nanmax(M))] if np.isfinite(M).any() else None}
    return out


def ascii_map(xs, ys, M, title, chars=" .:-=+*#%@", decimals=3):
    if not np.isfinite(M).any():
        return f"### {title}\n\n(no data)\n"
    lo, hi = float(np.nanmin(M)), float(np.nanmax(M))
    rng = max(hi - lo, 1e-12)
    out = [f"### {title}", "",
           "rows = primary fee Y (pre-E8 high -> E8 abolition 0 at bottom); cols = vac0 X (severe -> slack)", "```",
           "      " + " ".join(f"{x:>6.3f}" for x in xs)]
    for i in range(len(ys) - 1, -1, -1):
        row = "".join(chars[min(len(chars) - 1, int((M[i, j] - lo) / rng * (len(chars) - 1)))]
                      if np.isfinite(M[i, j]) else "?" for j in range(len(xs)))
        out.append(f"{ys[i]:>5.2f} {row}")
    out += ["```", f"range [{lo:.4f}, {hi:.4f}]", ""]
    return "\n".join(out)


def slice_tables(cells, metrics, gate):
    """E8-abolition slice (fee=0) and baseline-X slice, per gate."""
    cc = [c for c in cells if c["gate"] == gate]
    xs = sorted({c["x_vac0"] for c in cc}); ys = sorted({c["fee_primary"] for c in cc})
    md = []
    md.append(f"#### {gate}: E8-abolition slice (fee_primary = 0.0), X severe -> slack")
    display = {"x_vac0": "vac0", "fee_primary": "fee"}
    hdr = ["x_vac0", "x_vac_per_gate_pass"] + [m for m in metrics if m in ("liq_share", "q1_liq_share",
           "tut_rate", "tut_q5_q1_gap", "completion_lower", "completion_lower_q_gap", "formal_rate")]
    md.append("| " + " | ".join(hdr) + " |")
    md.append("|" + "---|" * len(hdr))
    for x in xs:
        c = next(c for c in cc if c["x_vac0"] == x and c["fee_primary"] == 0.0)
        md.append("| " + " | ".join(f"{c.get(k):.3f}" if isinstance(c.get(k), float) else str(c.get(k))
                                    for k in hdr) + " |")
    mid = xs[len(xs) // 2]
    md.append("")
    md.append(f"#### {gate}: fee slice at vac0 = {mid:.3f}, fee .00 (E8) -> .18 (pre-abolition)")
    hdr2 = ["fee_primary", "liq_share", "q1_liq_share", "tut_rate", "tut_q5_q1_gap", "completion_lower",
            "completion_lower_q_gap", "formal_rate"]
    md.append("| " + " | ".join(hdr2) + " |")
    md.append("|" + "---|" * len(hdr2))
    for y in ys:
        c = next(c for c in cc if c["x_vac0"] == mid and c["fee_primary"] == y)
        md.append("| " + " | ".join(f"{c.get(k):.3f}" if isinstance(c.get(k), float) else str(c.get(k))
                                    for k in hdr2) + " |")
    md.append("")
    return "\n".join(md)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--source", choices=["box", "local"], default="box")
    ap.add_argument("--box-dir", default="/Users/treymenefee/neon-boot/pulled/phase-sweep-quick")
    ap.add_argument("--results-dir", default=RES)
    ap.add_argument("--out-tag", default=None)
    a = ap.parse_args()

    if a.source == "box":
        meta, cells = load_box(a.box_dir)
    else:
        meta, cells = load_local(a.results_dir)
    tag = a.out_tag or a.source
    metrics = [m for m in METRIC_ORDER if available(cells, m)]

    stats = {"label": "SIMULATION ONLY - boundary statistics; no causal/empirical claims",
             "preregistration": "PREREGISTRATION_PHASE_SWEEP.md (commit 408aa3e, before any run)",
             "source": tag, "sigma_floor": SIGMA_FLOOR, "design": meta.get("design", meta),
             "metrics_available": metrics, "by_gate": {}}
    gates_present = sorted({c["gate"] for c in cells})
    for g in gates_present:
        stats["by_gate"][g] = analyse_gate(cells, g, metrics)

    verdict = {}
    for metric in STRESS_METRICS:
        if "bar" not in stats["by_gate"] or "quota" not in stats["by_gate"]:
            verdict[metric] = {"pre_registered_gate_pair_not_both_present": True}
            continue
        if metric not in metrics:
            verdict[metric] = {"unavailable_in_source": True}
            continue
        b, q = stats["by_gate"]["bar"][metric], stats["by_gate"]["quota"][metric]
        C = (b["J_median"] / q["J_median"]) if q["J_median"] and q["J_median"] > 0 else None
        ok = dict(J_max_ge_4=b["J_max"] is not None and b["J_max"] >= 4,
                  sharpness_ge_2=b["sharpness"] is not None and b["sharpness"] >= 2,
                  gate_contrast_ge_2=C is not None and C >= 2,
                  regressive_direction=bool(b["direction_ok"]))
        verdict[metric] = {"clauses": ok, "gate_contrast_C": C, "present": all(ok.values()),
                           "J_max_bar": b["J_max"], "sharpness_bar": b["sharpness"],
                           "edge_max_bar": b["edge_max"], "direction_ok_bar": b["direction_ok"],
                           "J_max_quota": q["J_max"], "sharpness_quota": q["sharpness"],
                           "step_best_bar": b["step_best"], "step_best_quota": q["step_best"]}
    stats["decision"] = verdict

    with open(os.path.join(a.results_dir, f"boundary_stats_{tag}.json"), "w") as f:
        json.dump(stats, f, indent=1)

    md = ["# Phase diagrams — SIMULATION ONLY", "",
          f"Source: **{tag}**. eduengine toy worlds; illustrative parameters; no causal or empirical claims.",
          "Rows = primary-fee Y (`.00` = E8 abolition at the bottom); columns = vac0 X (severe left -> slack right).", ""]
    for g in gates_present:
        for m in ("tut_q5_q1_gap", "q1_liq_share", "gate_fail_share", "completion_lower_q_gap"):
            if m in metrics:
                xs, ys, M, _S = grid(cells, g, m)
                md.append(ascii_map(xs, ys, M, f"{g} — {m}"))
        md.append(slice_tables(cells, metrics, g))
    with open(os.path.join(a.results_dir, f"PHASE_DIAGRAMS_{tag}.md"), "w") as f:
        f.write("\n".join(md))
    print(json.dumps({k: {kk: vv for kk, vv in v.items() if kk in
                          ("present", "J_max_bar", "sharpness_bar", "gate_contrast_C",
                           "direction_ok_bar", "J_max_quota", "sharpness_quota")}
                      for k, v in verdict.items()}, indent=1))


if __name__ == "__main__":
    main()
