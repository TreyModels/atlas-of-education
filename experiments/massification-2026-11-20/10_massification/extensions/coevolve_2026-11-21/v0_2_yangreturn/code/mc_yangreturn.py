#!/usr/bin/env python3
"""Parameter Monte Carlo for the v0.2 return-side Yang wiring (CRN; paired seeds; deterministic).

Contract: ../PRE_DECLARATIONS.md (sha256 recorded before run). Runs the copied simulator; the frozen
v0 and v0.1 extensions are only read (for the identity guard).
"""
import argparse, importlib.util, json, os, sys
import numpy as np
import pandas as pd
from multiprocessing import Pool

HERE = os.path.dirname(os.path.abspath(__file__))
EXT = os.path.dirname(HERE)
BASE = os.path.dirname(EXT)          # coevolve_2026-11-21
V0 = os.path.join(BASE, "code", "coevolve_v0.py")
V02 = os.path.join(HERE, "coevolve_v0_2_yangreturn.py")
OUT = os.path.join(EXT, "results")
SIZES = [200000, 500000, 1000000, 2000000]
SEEDS = [0, 1]
DESIGNS = ["none", "yang", "yang_endog"]
DRAW_SEED = 20261121
DRAWS = 150
LABEL = "SIMULATED"

def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m

def draw_params(n, seed=DRAW_SEED):
    rng = np.random.default_rng(seed)
    out = []
    for k in range(n):
        variant = int(rng.integers(0, 3))
        out.append({
            "draw": k,
            "b": float(rng.uniform(100.0, 160.0)),
            "anchorD": float(rng.uniform(400.0, 600.0)),
            "mapping": ["linear", "proportional", "convex"][variant],
            "mapping_index": variant,
            "convex_scale": float(rng.uniform(100.0, 400.0)),
            "premium_mult": float(rng.uniform(0.85, 1.15)),
            "beta_mult": float(rng.uniform(0.7, 1.3)),
            "travel_mult": float(rng.uniform(0.5, 1.5)),
            "child_wage_mult": float(rng.uniform(0.85, 1.15)),
        })
    return out

_MOD = None
_P = None

def _init():
    global _MOD, _P
    _MOD = load("v02_worker", V02)
    _P = _MOD.params_as_lists()

def _run_cell(task):
    """task = (draw, size, seed, design). Returns metrics."""
    d, N, seed, design = task
    cfg = {
        "city_N": float(N), "b": d["b"], "anchorD": d["anchorD"],
        "mapping": d["mapping"], "convex_scale": d["convex_scale"],
        "alpha": 1.0, "premium_mult": d["premium_mult"], "beta_mult": d["beta_mult"],
        "travel_mult": d["travel_mult"], "child_wage_mult": d["child_wage_mult"],
    }
    _MOD.YANG.update(cfg)
    sim = _MOD.run_one(design, int(seed), _P)
    coh = _MOD.cohort_table(sim, _P)
    comp = float(coh["completed_upper_by_age_20"].mean()) * 100.0
    left = float(coh["left_secondary_early_share"].mean()) * 100.0
    cx = _MOD.coexistence_series(sim, _P)
    years = cx["year"] if "year" in cx.columns else cx.iloc[:, 1]
    cx = cx[(years >= 6) & (years <= 17)]
    def m(col):
        v = cx[col].astype(float)
        v = v[~np.isnan(v)]
        return float(v.mean()) if len(v) else float("nan")
    return {
        "draw": d["draw"], "size": N, "seed": seed, "design": design,
        "completion": comp, "leaving": left,
        "unused_accessible_share": m("unused_accessible_share"),
        "qualified_per_place": m("qualified_per_place"),
        "gate_household_share": m("gate_household_share"),
    }

def identity_guard():
    v0 = load("v0_guard", V0); v2 = load("v02_guard", V02)
    P0 = v0.params_as_lists(); P2 = v2.params_as_lists()
    s0 = v0.run_one("baseline", 20261121, P0)
    s2 = v2.run_one("baseline", 20261121, P2)
    p0 = v0.build_panel(s0, "baseline", 20261121); p2 = v2.build_panel(s2, "baseline", 20261121)
    y0 = v0.build_pupilyear(s0, "baseline", 20261121); y2 = v2.build_pupilyear(s2, "baseline", 20261121)
    ok = p0.equals(p2) and y0.equals(y2)
    return {"pass": bool(ok), "panel_equal": bool(p0.equals(p2)), "pupilyear_equal": bool(y0.equals(y2)),
            "note": "arm 'baseline' with default YANG declarations; alpha*g = 0"}

def quantile(a, q):
    a = np.sort(np.asarray(a, dtype=float)); a = a[~np.isnan(a)]
    if len(a) == 0: return None
    return float(np.quantile(a, q))

def stats(a):
    a = np.asarray(a, dtype=float); a = a[~np.isnan(a)]
    return {"mean": float(a.mean()), "median": float(np.median(a)), "p5": quantile(a, 0.05),
            "p95": quantile(a, 0.95), "min": float(a.min()), "max": float(a.max())}

def ranks(x):
    order = np.argsort(x, kind="mergesort"); r = np.empty(len(x)); r[order] = np.arange(1, len(x)+1)
    # average ties
    xs = np.asarray(x); uniq, inv, cnt = np.unique(xs, return_inverse=True, return_counts=True)
    if np.any(cnt > 1):
        sums = np.zeros(len(uniq)); np.add.at(sums, inv, r); avg = sums / cnt; r = avg[inv]
    return r

def spearman(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = ~(np.isnan(x) | np.isnan(y))
    if m.sum() < 3: return None
    rx, ry = ranks(x[m]), ranks(y[m])
    if np.std(rx) == 0 or np.std(ry) == 0: return None
    return float(np.corrcoef(rx, ry)[0, 1])

def pearson2(x, y):
    x = np.asarray(x, float); y = np.asarray(y, float)
    m = ~(np.isnan(x) | np.isnan(y))
    if m.sum() < 3 or np.std(x[m]) == 0: return None
    return float(np.corrcoef(x[m], y[m])[0, 1] ** 2)

def aggregate(cells, draws_list):
    df = pd.DataFrame(cells)
    by = {}
    for design in ("yang", "yang_endog"):
        by[design] = {}
        for N in SIZES:
            sub = df[(df.design == design) & (df["size"] == N)]
            base = df[(df.design == "none") & (df["size"] == N)]
            # pair seeds within draw
            piv = sub.pivot_table(index="draw", columns="seed", values=["completion", "leaving"], aggfunc="first")
            pivb = base.pivot_table(index="draw", columns="seed", values=["completion", "leaving"], aggfunc="first")
            comp_gap = (piv["completion"].mean(axis=1) - pivb["completion"].mean(axis=1)).to_numpy()
            leav_gap = (piv["leaving"].mean(axis=1) - pivb["leaving"].mean(axis=1)).to_numpy()
            by[design][N] = {"completion_gap": stats(comp_gap), "leaving_gap": stats(leav_gap),
                             "completion_gap_arr": comp_gap, "leaving_gap_arr": leav_gap}
        # per-draw counts and pooled gaps
        counts = np.zeros(len(draws_list), int)
        for k, d in enumerate(draws_list):
            n = 0
            for N in SIZES:
                arr = by[design][N]["completion_gap_arr"]
                if abs(arr[k]) >= 0.5:
                    n += 1
            counts[k] = n
        by[design]["count_any"] = counts
        by[design]["robust_active"] = (counts >= 3)
        pooled = np.nanmean(np.vstack([by[design][N]["completion_gap_arr"] for N in SIZES]), axis=0)
        pooled_l = np.nanmean(np.vstack([by[design][N]["leaving_gap_arr"] for N in SIZES]), axis=0)
        by[design]["pooled_completion"] = pooled
        by[design]["pooled_leaving"] = pooled_l
    # coexistence metrics by design/size (mean over years/seeds)
    coex = {}
    for design in ("none", "yang", "yang_endog"):
        coex[design] = {}
        for N in SIZES:
            sub = df[(df.design == design) & (df["size"] == N)]
            coex[design][N] = {c: float(np.nanmean(sub[c].to_numpy())) for c in
                               ("unused_accessible_share", "qualified_per_place", "gate_household_share")}
    # sensitivity + variance (completion, primary yang)
    gap = by["yang"]["pooled_completion"]
    params = ["b", "anchorD", "mapping_index", "convex_scale", "premium_mult", "beta_mult", "travel_mult", "child_wage_mult"]
    table = []
    for p in params:
        x = [d[p] for d in draws_list]
        rho_c = spearman(x, gap); rho_l = spearman(x, by["yang"]["pooled_leaving"])
        r2 = pearson2(x, gap)
        table.append({"param": p, "spearman_completion": rho_c, "spearman_leaving": rho_l, "r2_completion": r2})
    r2sum = sum((r["r2_completion"] or 0.0) for r in table)
    for r in table:
        r["variance_share"] = (r["r2_completion"] or 0.0) / r2sum if r2sum else None
    top3 = sorted(table, key=lambda r: -abs(r["spearman_completion"] or 0.0))[:3]
    # boundary contingency (Yang-toy inert definition, declared)
    yang_toy_inert = [(d["premium_mult"] <= 0.95 and d["child_wage_mult"] >= 1.05) for d in draws_list]
    co_inert = ~by["yang"]["robust_active"]
    cont = {"yang_toy_inert_and_co_inert": int(sum(a and b for a, b in zip(yang_toy_inert, co_inert))),
            "yang_toy_inert_and_co_active": int(sum(a and (not b) for a, b in zip(yang_toy_inert, co_inert))),
            "yang_toy_active_and_co_inert": int(sum((not a) and b for a, b in zip(yang_toy_inert, co_inert))),
            "yang_toy_active_and_co_active": int(sum((not a) and (not b) for a, b in zip(yang_toy_inert, co_inert)))}
    out = {
        "label": LABEL, "n_draws": len(draws_list), "draw_seed": DRAW_SEED,
        "sizes": SIZES, "seeds": SEEDS, "designs": DESIGNS,
        "robust_active_share_yang": float(np.mean(by["yang"]["robust_active"])),
        "robust_active_share_yang_endog": float(np.mean(by["yang_endog"]["robust_active"])),
        "inert_share_yang": float(np.mean(~by["yang"]["robust_active"])),
        "by_size": {str(N): {design: {"completion_gap": {k: v for k, v in by[design][N]["completion_gap"].items() if k != "arr"},
                                        "leaving_gap": {k: v for k, v in by[design][N]["leaving_gap"].items()}}
                              for design in ("yang", "yang_endog")} for N in SIZES},
        "pooled": {design: {"completion_gap": stats(by[design]["pooled_completion"]),
                            "leaving_gap": stats(by[design]["pooled_leaving"])}
                   for design in ("yang", "yang_endog")},
        "coexistence": coex,
        "sensitivity": {"table": table, "top3": top3},
        "boundary_contingency": cont,
        "identity_guard": identity_guard(),
    }
    return out, by, df

def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--draws", type=int, default=DRAWS)
    ap.add_argument("--outdir", default=OUT)
    ap.add_argument("--tag", default="mc")
    ap.add_argument("--workers", type=int, default=6)
    ap.add_argument("--identity-only", action="store_true")
    args = ap.parse_args(argv)
    os.makedirs(args.outdir, exist_ok=True)
    if args.identity_only:
        print(json.dumps(identity_guard(), indent=2)); return 0
    draws_list = draw_params(args.draws)
    tasks = []
    for d in draws_list:
        for N in SIZES:
            for s in SEEDS:
                for design in DESIGNS:
                    tasks.append((d, N, s, design))
    t0 = __import__("time").time()
    with Pool(args.workers, initializer=_init) as pool:
        cells = pool.map(_run_cell, tasks, chunksize=8)
    runtime = __import__("time").time() - t0
    out, by, df = aggregate(cells, draws_list)
    out["runtime_seconds"] = None  # runtime only in console log (determinism)
    out["n_runs"] = len(cells)
    out["workers"] = args.workers
    with open(os.path.join(args.outdir, "%s_results.json" % args.tag), "w") as fh:
        json.dump(out, fh, indent=2, sort_keys=True); fh.write("\n")
    # per-draw CSV
    rows = []
    for k, d in enumerate(draws_list):
        r = {p: d[p] for p in ("draw", "b", "anchorD", "mapping", "convex_scale", "premium_mult", "beta_mult", "travel_mult", "child_wage_mult")}
        for design in ("yang", "yang_endog"):
            r["count_%s" % design] = int(by[design]["count_any"][k])
            r["robust_%s" % design] = bool(by[design]["robust_active"][k])
            r["pooled_completion_gap_%s" % design] = float(by[design]["pooled_completion"][k])
            r["pooled_leaving_gap_%s" % design] = float(by[design]["pooled_leaving"][k])
        for N in SIZES:
            r["completion_gap_yang_%d" % N] = float(by["yang"][N]["completion_gap_arr"][k])
            r["leaving_gap_yang_%d" % N] = float(by["yang"][N]["leaving_gap_arr"][k])
        r["yang_toy_inert"] = bool(d["premium_mult"] <= 0.95 and d["child_wage_mult"] >= 1.05)
        r["coevolve_inert_yang"] = bool(not by["yang"]["robust_active"][k])
        rows.append(r)
    pd.DataFrame(rows).to_csv(os.path.join(args.outdir, "%s_per_draw.csv" % args.tag), index=False, float_format="%.10g")
    log = []
    log.append("v0.2 MC: %d draws x 2 seeds x %d sizes x 3 designs = %d runs; workers=%d; runtime=%.1fs"
               % (args.draws, len(SIZES), out["n_runs"], args.workers, runtime))
    log.append("identity guard: %s" % ("PASS" if out["identity_guard"]["pass"] else "FAIL"))
    log.append("robust-ACTIVE share: yang %.4f | yang_endog %.4f | inert(yang) %.4f"
               % (out["robust_active_share_yang"], out["robust_active_share_yang_endog"], out["inert_share_yang"]))
    for design in ("yang", "yang_endog"):
        g = out["pooled"][design]["completion_gap"]
        log.append("%s pooled completion gap: mean %+.4f median %+.4f p5 %+.4f p95 %+.4f"
                   % (design, g["mean"], g["median"], g["p5"], g["p95"]))
    log.append("top3: %s" % json.dumps(out["sensitivity"]["top3"]))
    log.append("boundary contingency: %s" % json.dumps(out["boundary_contingency"]))
    with open(os.path.join(args.outdir, "%s_console.log" % args.tag), "w") as fh:
        fh.write("\n".join(log) + "\n")
    print("\n".join(log))
    return 0

if __name__ == "__main__":
    sys.exit(main())
