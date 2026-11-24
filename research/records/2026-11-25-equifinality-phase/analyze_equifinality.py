#!/usr/bin/env python3
"""analyze_equifinality.py — SIMULATION ONLY (eduengine toy worlds; no empirical/causal claims).

Exhaustive equifinality search over the committed 800-cell / 16,000-run phase sweep, exactly per
`PRE_REGISTRATION.md` (commit 078cc13) in this directory:

  qualifying pair <=> |dGER_sim| < 0.5 pp  AND  (|dliq_share| > 25 pp  OR  |dtut_rate| > 20 pp)

on SEED-MEAN cell values (seeds 0..19), with GER_sim = 1 - never_enrolled_share (declared SIMULATED
participation, not an empirical GER). All differences are in percentage points (100 x share) and absolute
(direction-agnostic); the sign of every d is reported.

Pair families (declared in the prereg):
  * within-gate (PRIMARY):   bar-bar C(400,2) + quota-quota C(400,2) = 159,600 pairs
  * cross-gate (SECONDARY):  bar x quota 400 x 400                   = 160,000 pairs
  together every unordered pair of distinct cells = C(800,2) = 319,600 -> exhaustive over the whole design.

The vectorised counts are cross-checked against an explicit double loop (brute force) on every pair.

Null: 1,000 label-permutation nulls per prereg §7 — within each gate, independently permute each of the three
outcome vectors across the 400 cells (rng = np.random.default_rng(20261125 + k)); report mean/SD/percentiles
and one-sided p = (1 + #{null >= observed}) / 1001, per family and per gate.

Secondary (declared): completion_lower pairing; descriptive phase-boundary diagnostics (J_edge / sharpness /
gate contrast) with NO phase-transition verdict in this record.
"""
import argparse
import csv
import hashlib
import json
import os

import numpy as np

LABEL = "SIMULATION ONLY - eduengine toy worlds; illustrative parameters; no causal/empirical claims"
TOL_GER_PP = 0.5
TOL_LIQ_PP = 25.0
TOL_TUT_PP = 20.0
TOL_CL_PP = 20.0            # secondary (completion_lower), descriptive only
GATES = ["bar", "quota"]
N_PERMS = 1000
NULL_SEED0 = 20261125
_TRI400 = np.triu(np.ones((400, 400), bool), 1)   # upper-triangle mask, reused by the null loop


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


# ------------------------------------------------------------------------------- load & unit checks
def load_cells(summary_json):
    with open(summary_json) as f:
        run = json.load(f)
    by_gate = {g: {} for g in GATES}
    for c in run["cells"]:
        by_gate[c["gate"]][(c["x_index"], c["y_index"])] = c
    cells = {}
    for g in GATES:
        assert len(by_gate[g]) == 400, (g, len(by_gate[g]))
        meta = [by_gate[g][(xi, yi)] for xi in range(20) for yi in range(20)]

        def vec(key):
            return np.array([np.nan if c.get(key) is None else 100.0 * float(c[key]) for c in meta], float)

        cells[g] = dict(meta=meta,
                        ger=vec("ger_sim"),                         # pp: 100*(1 - never_share)
                        liq=vec("liq_share"),                       # pp
                        tut=vec("tut_rate"),                        # pp
                        cl=vec("completion_lower"),                 # pp
                        sd_ger=vec("sd_ger_sim"), sd_liq=vec("sd_liq_share"), sd_tut=vec("sd_tut_rate"))
    return run, cells


def qualify(g_a, l_a, t_a, g_b, l_b, t_b):
    """Explicit pre-registered predicate (strict inequalities), all in pp."""
    return (abs(g_b - g_a) < TOL_GER_PP) and ((abs(l_b - l_a) > TOL_LIQ_PP) or (abs(t_b - t_a) > TOL_TUT_PP))


# ------------------------------------------------------------------------------- pair search
def pair_mask(G1, L1, T1, G2, L2, T2):
    """Boolean matrix[i, j] = qualify(cell i of set 1, cell j of set 2)."""
    dG = np.abs(G1[:, None] - G2[None, :])
    dL = np.abs(L1[:, None] - L2[None, :])
    dT = np.abs(T1[:, None] - T2[None, :])
    return (dG < TOL_GER_PP) & ((dL > TOL_LIQ_PP) | (dT > TOL_TUT_PP))


def all_pairs(cells):
    """Exhaustive pair search; returns counts and the full qualifying-pair list (with signs)."""
    out = {"within_bar": 0, "within_quota": 0, "cross": 0, "pairs": []}
    for g in GATES:
        v = cells[g]
        ok = ~np.isnan(v["ger"]) & ~np.isnan(v["liq"]) & ~np.isnan(v["tut"])
        okm = ok[:, None] & ok[None, :]
        with np.errstate(invalid="ignore"):
            m = okm & pair_mask(v["ger"], v["liq"], v["tut"], v["ger"], v["liq"], v["tut"])
        m &= np.triu(np.ones_like(m, bool), 1)
        out[f"within_{g}"] = int(m.sum())
        for i, j in np.argwhere(m):
            out["pairs"].append(dict(fam=f"within_{g}", i=int(i), j=int(j),
                                     dger=float(v["ger"][j] - v["ger"][i]),
                                     dliq=float(v["liq"][j] - v["liq"][i]),
                                     dtut=float(v["tut"][j] - v["tut"][i])))
    b, q = cells["bar"], cells["quota"]
    okb = ~np.isnan(b["ger"]) & ~np.isnan(b["liq"]) & ~np.isnan(b["tut"])
    okq = ~np.isnan(q["ger"]) & ~np.isnan(q["liq"]) & ~np.isnan(q["tut"])
    with np.errstate(invalid="ignore"):
        m = (okb[:, None] & okq[None, :]) & pair_mask(b["ger"], b["liq"], b["tut"],
                                                      q["ger"], q["liq"], q["tut"])
    out["cross"] = int(m.sum())
    for i, j in np.argwhere(m):
        out["pairs"].append(dict(fam="cross", i=int(i), j=int(j),
                                 dger=float(q["ger"][j] - b["ger"][i]),
                                 dliq=float(q["liq"][j] - b["liq"][i]),
                                 dtut=float(q["tut"][j] - b["tut"][i])))
    return out


def brute_force_counts(cells):
    """Explicit double loop over every pair — validity cross-check for the vectorised counts."""
    counts = {"within_bar": 0, "within_quota": 0, "cross": 0}
    for g in GATES:
        v = cells[g]
        n = len(v["ger"])
        ok = ~np.isnan(v["ger"]) & ~np.isnan(v["liq"]) & ~np.isnan(v["tut"])
        for i in range(n):
            if not ok[i]:
                continue
            for j in range(i + 1, n):
                if ok[j] and qualify(v["ger"][i], v["liq"][i], v["tut"][i],
                                     v["ger"][j], v["liq"][j], v["tut"][j]):
                    counts[f"within_{g}"] += 1
    b, q = cells["bar"], cells["quota"]
    okb = ~np.isnan(b["ger"]) & ~np.isnan(b["liq"]) & ~np.isnan(b["tut"])
    okq = ~np.isnan(q["ger"]) & ~np.isnan(q["liq"]) & ~np.isnan(q["tut"])
    for i in range(len(b["ger"])):
        if not okb[i]:
            continue
        for j in range(len(q["ger"])):
            if okq[j] and qualify(b["ger"][i], b["liq"][i], b["tut"][i],
                                  q["ger"][j], q["liq"][j], q["tut"][j]):
                counts["cross"] += 1
    return counts


# ------------------------------------------------------------------------------- null
def _stats(arr, observed, n_perms):
    a = np.asarray(arr, float)
    o = float(observed)
    return dict(observed=o, null_mean=float(a.mean()), null_sd=float(a.std(ddof=1)),
                null_p2_5=float(np.percentile(a, 2.5)), null_p50=float(np.percentile(a, 50)),
                null_p97_5=float(np.percentile(a, 97.5)),
                null_min=float(a.min()), null_max=float(a.max()),
                ratio_obs_over_nullmean=(o / a.mean()) if a.mean() > 0 else None,
                p_one_sided=float((1.0 + np.sum(a >= o)) / (n_perms + 1.0)))


def null_distribution(cells, obs, n_perms=N_PERMS):
    """Prereg §7: label-permutation nulls, independent permutation of each outcome vector within each gate."""
    keys = ("within_bar", "within_quota", "within_gate_combined", "cross", "all_pairs")
    acc = {k: np.zeros(n_perms, int) for k in keys}
    for k in range(n_perms):
        rng = np.random.default_rng(NULL_SEED0 + k)
        perm = {}
        for g in GATES:
            perm[g] = dict(ger=rng.permutation(cells[g]["ger"]),
                           liq=rng.permutation(cells[g]["liq"]),
                           tut=rng.permutation(cells[g]["tut"]))
        nb = int(pair_mask(perm["bar"]["ger"], perm["bar"]["liq"], perm["bar"]["tut"],
                           perm["bar"]["ger"], perm["bar"]["liq"], perm["bar"]["tut"])[_TRI400].sum())
        nq = int(pair_mask(perm["quota"]["ger"], perm["quota"]["liq"], perm["quota"]["tut"],
                           perm["quota"]["ger"], perm["quota"]["liq"], perm["quota"]["tut"])[_TRI400].sum())
        nc = int(pair_mask(perm["bar"]["ger"], perm["bar"]["liq"], perm["bar"]["tut"],
                           perm["quota"]["ger"], perm["quota"]["liq"], perm["quota"]["tut"]).sum())
        acc["within_bar"][k] = nb
        acc["within_quota"][k] = nq
        acc["within_gate_combined"][k] = nb + nq
        acc["cross"][k] = nc
        acc["all_pairs"][k] = nb + nq + nc
    return {k: _stats(acc[k], obs[k], n_perms) for k in keys}


# ------------------------------------------------------------------------------- helpers
def cell_meta(cells, gate, i):
    c = cells[gate]["meta"][i]
    return dict(gate=gate, x_index=c["x_index"], x_vac0=c["x_vac0"], y_index=c["y_index"],
                fee_primary=c["fee_primary"])


def write_csv(path, rows, fieldnames):
    with open(path, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fieldnames, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow(r)


def composition(rows):
    if not rows:
        return dict(n=0)
    return dict(n=len(rows),
                x_differs_only=int(sum(1 for r in rows if r["x_differs"] and not r["y_differs"])),
                y_differs_only=int(sum(1 for r in rows if r["y_differs"] and not r["x_differs"])),
                both_differ=int(sum(1 for r in rows if r["x_differs"] and r["y_differs"])),
                mean_abs_dger_pp=float(np.mean([r["abs_dger_pp"] for r in rows])),
                mean_abs_dliq_pp=float(np.mean([r["abs_dliq_pp"] for r in rows])),
                mean_abs_dtut_pp=float(np.mean([r["abs_dtut_pp"] for r in rows])),
                share_via_liq_only=float(np.mean([(r["abs_dliq_pp"] > TOL_LIQ_PP) and
                                                  not (r["abs_dtut_pp"] > TOL_TUT_PP) for r in rows])),
                share_via_tut_only=float(np.mean([(r["abs_dtut_pp"] > TOL_TUT_PP) and
                                                  not (r["abs_dliq_pp"] > TOL_LIQ_PP) for r in rows])),
                share_via_both=float(np.mean([(r["abs_dtut_pp"] > TOL_TUT_PP) and
                                              (r["abs_dliq_pp"] > TOL_LIQ_PP) for r in rows])))


def phase_diagnostics(cells):
    """Cheap, descriptive-only grid-edge statistics (J_edge / sharpness / gate contrast). No verdict."""
    def edges(v, metric, sd_metric):
        M = v[metric].reshape(20, 20)
        S = v[sd_metric].reshape(20, 20)
        sd_med = float(np.nanmedian(S))
        js = []
        for xi in range(20):
            for yi in range(20):
                for dx, dy in ((1, 0), (0, 1)):
                    xj, yj = xi + dx, yi + dy
                    if xj < 20 and yj < 20 and np.isfinite(M[xi, yi]) and np.isfinite(M[xj, yj]):
                        js.append(abs(M[xj, yj] - M[xi, yi]) / sd_med if sd_med > 0 else np.nan)
        js = np.asarray([j for j in js if np.isfinite(j)], float)
        if len(js) == 0:
            return None
        return dict(sd_med_pp=sd_med, mean_J_edge=float(js.mean()), median_J_edge=float(np.median(js)),
                    J_max=float(js.max()), sharpness=float(js.max() / max(np.median(js), 1e-12)),
                    n_edges=int(len(js)))
    out = {}
    for metric, sd_metric in (("ger", "sd_ger"), ("liq", "sd_liq"), ("tut", "sd_tut")):
        out[metric] = {g: edges(cells[g], metric, sd_metric) for g in GATES}
        eb, eq = out[metric]["bar"], out[metric]["quota"]
        out[metric]["gate_contrast_mean_J"] = (eb["mean_J_edge"] / eq["mean_J_edge"]
                                               if eb and eq and eq["mean_J_edge"] > 0 else None)
    return out


# ------------------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description="Exhaustive equifinality analysis (SIMULATION ONLY)")
    ap.add_argument("--run-json", required=True, help="phase_sweep_full_summary.json from the box run")
    ap.add_argument("--runs-csv", default=None, help="phase_sweep_full_runs.csv (hashed, not re-analysed)")
    ap.add_argument("--out", required=True)
    ap.add_argument("--n-perms", type=int, default=N_PERMS)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)

    run, cells = load_cells(a.run_json)
    design = run["design"]
    n_missing = {g: int(np.sum(np.isnan(cells[g]["ger"]) | np.isnan(cells[g]["liq"]) |
                               np.isnan(cells[g]["tut"]))) for g in GATES}

    # ---- validity (prereg §9) ------------------------------------------------------------------
    n_pairs_within = sum(400 * 399 // 2 for _ in GATES)
    n_pairs_cross = 400 * 400
    n_pairs_total = design["n_cells"] * (design["n_cells"] - 1) // 2
    assert n_pairs_total == n_pairs_within + n_pairs_cross == 319600, (n_pairs_total, n_pairs_within)
    for g in GATES:
        c0 = cells[g]["meta"][0]
        tot = sum((c0.get(f"{k}_share") or 0.0) for k in
                  ("liq", "gate_fail", "finished", "never", "no_seat", "not_admitted", "choice", "censored"))
        assert abs(tot - 1.0) <= 1e-6, (g, tot)

    ap_ = all_pairs(cells)
    obs = {"within_bar": ap_["within_bar"], "within_quota": ap_["within_quota"], "cross": ap_["cross"],
           "within_gate_combined": ap_["within_bar"] + ap_["within_quota"]}
    obs["all_pairs"] = obs["within_bar"] + obs["within_quota"] + obs["cross"]
    bf = brute_force_counts(cells)
    assert bf["within_bar"] == obs["within_bar"], (bf, obs)
    assert bf["within_quota"] == obs["within_quota"], (bf, obs)
    assert bf["cross"] == obs["cross"], (bf, obs)

    nulls = null_distribution(cells, obs, n_perms=a.n_perms)

    # ---- full qualifying-pair tables -----------------------------------------------------------
    pairs = []
    for p in ap_["pairs"]:
        if p["fam"] == "cross":
            ma, mb = cell_meta(cells, "bar", p["i"]), cell_meta(cells, "quota", p["j"])
        else:
            g = p["fam"].replace("within_", "")
            ma, mb = cell_meta(cells, g, p["i"]), cell_meta(cells, g, p["j"])
        row = dict(family=p["fam"],
                   gate_a=ma["gate"], x_a=ma["x_index"], x_vac0_a=ma["x_vac0"], y_a=ma["y_index"],
                   fee_a=ma["fee_primary"],
                   gate_b=mb["gate"], x_b=mb["x_index"], x_vac0_b=mb["x_vac0"], y_b=mb["y_index"],
                   fee_b=mb["fee_primary"],
                   ger_a=float(cells[ma["gate"]]["ger"][p["i"]]),
                   ger_b=float(cells[mb["gate"]]["ger"][p["j"]]),
                   liq_a=float(cells[ma["gate"]]["liq"][p["i"]]),
                   liq_b=float(cells[mb["gate"]]["liq"][p["j"]]),
                   tut_a=float(cells[ma["gate"]]["tut"][p["i"]]),
                   tut_b=float(cells[mb["gate"]]["tut"][p["j"]]),
                   dger_pp=p["dger"], dliq_pp=p["dliq"], dtut_pp=p["dtut"],
                   abs_dger_pp=abs(p["dger"]), abs_dliq_pp=abs(p["dliq"]), abs_dtut_pp=abs(p["dtut"]),
                   score_pp=abs(p["dliq"]) + abs(p["dtut"]),
                   x_differs=int(ma["x_index"] != mb["x_index"]),
                   y_differs=int(ma["y_index"] != mb["y_index"]))
        pairs.append(row)
    primary = sorted([r for r in pairs if r["family"] != "cross"], key=lambda r: -r["score_pp"])
    cross = sorted([r for r in pairs if r["family"] == "cross"], key=lambda r: -r["score_pp"])

    pair_cols = ["family", "gate_a", "x_a", "x_vac0_a", "y_a", "fee_a", "ger_a", "liq_a", "tut_a",
                 "gate_b", "x_b", "x_vac0_b", "y_b", "fee_b", "ger_b", "liq_b", "tut_b",
                 "dger_pp", "dliq_pp", "dtut_pp", "abs_dger_pp", "abs_dliq_pp", "abs_dtut_pp", "score_pp",
                 "x_differs", "y_differs"]
    write_csv(os.path.join(a.out, "equifinality_pairs.csv"), sorted(pairs, key=lambda r: (r["family"],
                                                                                          -r["score_pp"])),
              pair_cols)
    write_csv(os.path.join(a.out, "equifinality_top50.csv"), primary[:50], pair_cols)
    write_csv(os.path.join(a.out, "equifinality_top50_crossgate.csv"), cross[:50], pair_cols)

    # distinct cells / max degree in the PRIMARY family
    deg = {}
    for r in primary:
        for key in ((r["gate_a"], r["x_a"], r["y_a"]), (r["gate_b"], r["x_b"], r["y_b"])):
            deg[key] = deg.get(key, 0) + 1
    max_deg = max(deg.values()) if deg else 0
    max_deg_cells = [dict(gate=k[0], x_index=k[1], y_index=k[2], degree=v)
                     for k, v in sorted(deg.items(), key=lambda kv: -kv[1])[:5] if v == max_deg]

    # ---- secondary: completion_lower (descriptive) ---------------------------------------------
    cl_pairs = []
    for g in GATES:
        v = cells[g]
        ok = ~np.isnan(v["ger"]) & ~np.isnan(v["cl"])
        okm = ok[:, None] & ok[None, :]
        dG = np.abs(v["ger"][:, None] - v["ger"][None, :])
        dCL = np.abs(v["cl"][:, None] - v["cl"][None, :])
        with np.errstate(invalid="ignore"):
            m = okm & (dG < TOL_GER_PP) & (dCL > TOL_CL_PP)
        m &= np.triu(np.ones_like(m, bool), 1)
        for i, j in np.argwhere(m):
            ma, mb = cell_meta(cells, g, int(i)), cell_meta(cells, g, int(j))
            cl_pairs.append(dict(family=f"within_{g}", gate_a=g, x_a=ma["x_index"], x_vac0_a=ma["x_vac0"],
                                 y_a=ma["y_index"], fee_a=ma["fee_primary"], gate_b=g,
                                 x_b=mb["x_index"], x_vac0_b=mb["x_vac0"], y_b=mb["y_index"],
                                 fee_b=mb["fee_primary"],
                                 dger_pp=float(v["ger"][j] - v["ger"][i]),
                                 abs_dger_pp=float(abs(v["ger"][j] - v["ger"][i])),
                                 dcl_pp=float(v["cl"][j] - v["cl"][i]),
                                 abs_dcl_pp=float(abs(v["cl"][j] - v["cl"][i])),
                                 score_pp=float(abs(v["cl"][j] - v["cl"][i]))))
    cl_pairs.sort(key=lambda r: -r["score_pp"])
    write_csv(os.path.join(a.out, "equifinality_completion_lower_pairs.csv"), cl_pairs,
              ["family", "gate_a", "x_a", "x_vac0_a", "y_a", "fee_a", "gate_b", "x_b", "x_vac0_b", "y_b",
               "fee_b", "dger_pp", "abs_dger_pp", "dcl_pp", "abs_dcl_pp", "score_pp"])

    # ---- pre-registered reading rule (prereg §7) -----------------------------------------------
    comb = nulls["within_gate_combined"]
    within_obs = obs["within_gate_combined"]
    if within_obs <= comb["null_p97_5"]:
        verdict = ("NO EVIDENCE OF EQUIFINALITY BEYOND CHANCE: observed within-gate qualifying pairs "
                   f"{within_obs} <= null 97.5th percentile {comb['null_p97_5']:.1f} "
                   f"(null mean {comb['null_mean']:.2f}, null max {comb['null_max']:.0f}, "
                   f"one-sided p={comb['p_one_sided']:.3f})")
    else:
        ratio = (within_obs / comb["null_mean"]) if comb["null_mean"] > 0 else float("nan")
        verdict = ("EXCESS EQUIFINALITY: observed within-gate qualifying pairs "
                   f"{within_obs} > null 97.5th percentile {comb['null_p97_5']:.1f} "
                   f"(null mean {comb['null_mean']:.2f}, ratio {ratio:.2f}, "
                   f"one-sided p={comb['p_one_sided']:.3f})")

    report = {
        "label": LABEL,
        "prereg": "research/records/2026-11-25-equifinality-phase/PRE_REGISTRATION.md (commit 078cc13)",
        "inputs": {"run_json": os.path.abspath(a.run_json), "run_json_sha256": sha256(a.run_json),
                   "runs_csv": os.path.abspath(a.runs_csv) if a.runs_csv else None,
                   "runs_csv_sha256": (sha256(a.runs_csv) if a.runs_csv and os.path.exists(a.runs_csv)
                                       else None),
                   "analysis_script_sha256": sha256(os.path.abspath(__file__)),
                   "engine_code_sha256": run.get("code_sha256")},
        "design_check": {"n_cells": design["n_cells"],
                         "gates": design.get("gates", design.get("gate")),
                         "seeds": design["seeds"], "runs": design["runs"],
                         "runs_ok": design.get("runs_ok"), "runs_failed": design.get("runs_failed"),
                         "N": design["N"], "T": design["T"], "measure_from": design["measure_from"],
                         "x_levels": design["axes"]["X_vac0_formal_vacancies_per_entrant"],
                         "y_levels": design["axes"]["Y_fee_primary_share_of_median_income"],
                         "contest_gate": design.get("contest_gate")},
        "definition": {"ger_sim": "1 - never_enrolled_share (declared SIMULATED participation, not empirical GER)",
                       "tol_ger_pp": TOL_GER_PP, "tol_liq_pp": TOL_LIQ_PP, "tol_tut_pp": TOL_TUT_PP,
                       "pp": "100 x share; d on seed-mean cell values; absolute d, sign reported",
                       "families": {"within_gate_primary": "bar-bar and quota-quota pairs (159,600)",
                                    "cross_gate_secondary": "bar x quota pairs (160,000)",
                                    "total_pairs": "C(800,2) = 319,600 (exhaustive)"}},
        "counts": {"within_bar": obs["within_bar"], "within_quota": obs["within_quota"],
                   "within_gate_total": within_obs, "cross_gate": obs["cross"],
                   "all_pairs_total": obs["all_pairs"],
                   "pairs_examined": {"within_gate": n_pairs_within, "cross_gate": n_pairs_cross,
                                      "total": n_pairs_total},
                   "cells_with_missing_primary": n_missing,
                   "distinct_cells_in_primary_pairs": len(deg),
                   "max_degree": max_deg, "max_degree_cells": max_deg_cells},
        "null_1000_perms": {**{k: nulls[k] for k in nulls},
                            "n_perms": a.n_perms,
                            "scheme": "within each gate, independently permute the 3 outcome vectors across "
                                      "the 400 cells; rng=default_rng(20261125+k); same thresholds"},
        "verdict_primary": verdict,
        "pair_composition_primary": composition(primary),
        "pair_composition_cross_gate": composition(cross),
        "top50_primary": primary[:50],
        "top10_cross_gate": cross[:10],
        "completion_lower_secondary": {"tol_ger_pp": TOL_GER_PP, "tol_cl_pp": TOL_CL_PP,
                                       "n_pairs": len(cl_pairs),
                                       "n_by_gate": {g: sum(1 for r in cl_pairs if r["gate_a"] == g)
                                                     for g in GATES},
                                       "top10": cl_pairs[:10]},
        "phase_boundary_diagnostics_descriptive": phase_diagnostics(cells),
        "phase_boundary_note": "descriptive only; NO phase-transition verdict in this record "
                               "(that is the sibling phase-transition workstream's decision rule)",
        "validity": {"brute_force_matches_vectorised": True, "brute_force_counts": bf,
                     "n_cells_missing_primary": n_missing},
    }
    with open(os.path.join(a.out, "equifinality_null.json"), "w") as f:
        json.dump({"label": LABEL, "n_perms": a.n_perms,
                   **{k: nulls[k] for k in nulls}}, f, indent=1)
    with open(os.path.join(a.out, "equifinality_report.json"), "w") as f:
        json.dump(report, f, indent=1, default=str)
    with open(os.path.join(a.out, "analysis_manifest.json"), "w") as f:
        json.dump({"label": LABEL, "prereg": report["prereg"],
                   "analysis_script": os.path.abspath(__file__),
                   "analysis_script_sha256": report["inputs"]["analysis_script_sha256"],
                   "inputs": {k: v for k, v in report["inputs"].items() if k != "engine_code_sha256"},
                   "outputs": sorted(fn for fn in os.listdir(a.out) if fn.endswith((".csv", ".json")))},
                  f, indent=1)
    print(json.dumps({"label": LABEL, "counts": report["counts"], "verdict": verdict,
                      "null_within_gate_combined": comb, "null_cross_gate": nulls["cross"],
                      "null_within_bar": nulls["within_bar"], "null_within_quota": nulls["within_quota"],
                      "completion_lower_pairs": len(cl_pairs),
                      "out_dir": os.path.abspath(a.out)}, indent=1, default=str))


if __name__ == "__main__":
    main()
