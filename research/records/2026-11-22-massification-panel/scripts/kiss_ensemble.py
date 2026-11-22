"""KISS enrolment experiment: Philippines, many-model (Page) + blended-forecast (Silver) versions.

Pre-registered in PROTOCOL_kiss_phl.md. Targets are enrolment only (no private shares, no spending).
Commands (run from package root, PYTHONPATH=.):
  python scripts/kiss_ensemble.py fit K1 3     # one fit = one spec x one start (seed 0 = default start)
  python scripts/kiss_ensemble.py score        # picks best start per spec, scores everything held-out
  python scripts/kiss_ensemble.py mc K1 300    # Monte Carlo uncertainty band for one spec
  python scripts/kiss_ensemble.py all          # everything, sequentially (slow: ~40 fits)
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares, curve_fit

import masseng.engine_v6_phl as E
from masseng.data import Country
from masseng import calibrate5 as C5

OUT = Path("outputs/PHL/kiss"); (OUT / "fits").mkdir(parents=True, exist_ok=True)

# ---- pre-registered specs -------------------------------------------------------------
INTERCEPTS = ["a_prim", "a_sec", "a_sec_entry", "a_ter", "a_ter_entry"]
SPECS = {
    "K0": ["eta", "kappa"],            # income growth + household cost
    "K1": ["eta", "kappa", "b_p"],     # + bounded positional pull (lagged saturation)
    "K2": ["eta", "kappa", "b_h"],     # + measured returns (b_h >= 0)
}
for k, d in SPECS.items():
    E.V6_SPECS[k] = dict(dials=d, constrained=True, z=None)
FIXED = dict(c_scale=1.0, eta_x=0.0, mu_basic=-2.5, mu_ter=1.0, nu_basic=0.5, nu_ter=0.5)
BOUNDS = dict(E.BASE_BOUNDS, b_h=(0.0, 12.0), b_p=(0.0, 12.0))
TRAIN_SERIES = {"ger_primary", "ger_secondary", "ger_tertiary", "ner_primary"}
PRIMARY = ["ner_primary", "ner_secondary", "ger_tertiary"]      # selection metric
REPORT = PRIMARY + ["ger_primary", "ger_secondary"]
CAPS = dict(ner_primary=100, ner_secondary=100, ger_tertiary=100, ger_primary=130, ger_secondary=130)
N_SEEDS = 10


def _rows():
    c = Country("PHL"); rows = C5.build_rows(c)
    train = [r for r in rows if r["role"] == "train" and r["series"] in TRAIN_SERIES]
    test = [r for r in rows if r["role"] == "test" and r["series"] in REPORT]
    window = [r for r in rows if r["role"] in ("train", "diagnostic") and r["year"] <= c.config["years"]["train"][1]]
    return c, train, test, window


def _names(spec):
    return INTERCEPTS + SPECS[spec]


def _params(spec, x):
    p = dict(E.V6_DEFAULTS); p.update(FIXED); p.update(dict(zip(_names(spec), x))); return p


def _resid_fn(c, spec, rows):
    m = E.Model6PHL(c, dict(E.V6_DEFAULTS, **FIXED), spec=spec)
    obs = np.array([r["value"] for r in rows]); w = C5._w(rows)
    def f(x):
        return np.nan_to_num((C5._pred(m.set_params(_params(spec, x)).run(), rows) - obs) * w, nan=50.0)
    return f


def cmd_fit(spec, seed):
    c, train, _, _ = _rows()
    names = _names(spec)
    lo = np.array([BOUNDS[n][0] for n in names]); hi = np.array([BOUNDS[n][1] for n in names])
    if seed == 0:
        base = dict(E.V6_DEFAULTS, **FIXED)
        x0 = np.clip([base[n] for n in names], lo, hi)
    else:
        x0 = np.random.default_rng(7000 + seed).uniform(lo, hi)
    t = time.time()
    sol = least_squares(_resid_fn(c, spec, train), x0, bounds=(lo, hi), x_scale="jac",
                        diff_step=1e-3, max_nfev=300, ftol=1e-7, xtol=1e-7)
    at = [n for n, v in zip(names, sol.x) if min(abs(v - BOUNDS[n][0]), abs(v - BOUNDS[n][1])) < 1e-2]
    out = dict(spec=spec, seed=seed, x=sol.x.tolist(), names=names, params=_params(spec, sol.x),
               cost=float(sol.cost), nfev=int(sol.nfev), status=int(sol.status), message=str(sol.message),
               hit_nfev_cap=bool(sol.nfev >= 300), at_bounds=at,
               dials_at_bounds=[n for n in SPECS[spec] if n in at], seconds=round(time.time() - t, 1))
    (OUT / "fits" / f"{spec}_seed{seed:02d}.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"FIT {spec} seed{seed}: cost={out['cost']:.3f} nfev={out['nfev']} dials_at_bounds={out['dials_at_bounds']} ({out['seconds']}s)", flush=True)


def _best(spec):
    fs = [json.loads(p.read_text()) for p in (OUT / "fits").glob(f"{spec}_seed*.json")]
    if not fs:
        return None, []
    fs.sort(key=lambda f: f["cost"])
    return fs[0], fs


def _logistic_preds(window, test):
    """Rival 'diffusion' model: one logistic S-curve per series, fitted on the training window only."""
    out = np.full(len(test), np.nan); info = {}
    for s in REPORT:
        h = sorted((r["year"], r["value"]) for r in window if r["series"] == s)
        if len(h) < 4:
            info[s] = "too few training points"; continue
        t = np.array([a for a, _ in h], float); y = np.array([b for _, b in h], float)
        cap = CAPS[s]
        f = lambda tt, L, k, t0: L / (1 + np.exp(-k * (tt - t0)))
        try:
            p, _ = curve_fit(f, t, y, p0=[min(cap, y.max() * 1.2), 0.05, t.mean()],
                             bounds=([y.max() * 0.9, 0.0, 1900], [cap, 1.0, 2100]), maxfev=20000)
            info[s] = dict(L=float(p[0]), k=float(p[1]), t0=float(p[2]))
            for i, r in enumerate(test):
                if r["series"] == s:
                    out[i] = f(r["year"], *p)
        except Exception as e:  # report, do not hide
            info[s] = f"fit failed: {e}"
    return out, info


def _rmse(p, o):
    p = np.asarray(p, float); o = np.asarray(o, float); m = np.isfinite(p) & np.isfinite(o)
    return float(np.sqrt(np.mean((p[m] - o[m]) ** 2))) if m.any() else None


def cmd_score():
    c, train, test, window = _rows()
    obs = np.array([r["value"] for r in test])
    preds, fitinfo = {}, {}
    for spec in SPECS:
        best, fs = _best(spec)
        if best is None:
            continue
        res = E.Model6PHL(c, best["params"], spec=spec).run()
        preds[spec] = np.asarray(C5._pred(res, test), float)
        fitinfo[spec] = dict(best_seed=best["seed"], train_cost=best["cost"], starts=len(fs),
                             start_costs=sorted(round(f["cost"], 3) for f in fs),
                             dials={n: best["params"][n] for n in SPECS[spec]},
                             dials_at_bounds=best["dials_at_bounds"], hit_nfev_cap=best["hit_nfev_cap"])
    bm = C5.benchmarks(window, test)
    preds["persistence"], preds["trend"] = bm[:, 0], bm[:, 1]
    preds["logistic"], loginfo = _logistic_preds(window, test)
    members = [k for k in ("K0", "K1", "K2", "logistic") if k in preds]
    preds["page_ensemble"] = np.nanmean(np.vstack([preds[k] for k in members]), axis=0)
    preds["silver_blend"] = 0.5 * preds["persistence"] + 0.5 * preds["page_ensemble"]

    sel = [i for i, r in enumerate(test) if r["series"] in PRIMARY]
    table = {}
    for name, p in preds.items():
        table[name] = dict(primary_rmse=_rmse(p[sel], obs[sel]),
                           by_series={s: _rmse(p[[i for i, r in enumerate(test) if r["series"] == s]],
                                               obs[[i for i, r in enumerate(test) if r["series"] == s]]) for s in REPORT})
    ranked = sorted([k for k in table if table[k]["primary_rmse"] is not None], key=lambda k: table[k]["primary_rmse"])
    out = dict(protocol="PROTOCOL_kiss_phl.md", status="retrospective, inspected; not blind",
               primary_metric="held-out RMSE pooled over " + ", ".join(PRIMARY),
               page_ensemble_members=members, silver_blend="0.5*persistence + 0.5*page_ensemble (weights fixed in advance)",
               ranking=ranked, table=table, fits=fitinfo, logistic=loginfo,
               beats_persistence={k: table[k]["primary_rmse"] < table["persistence"]["primary_rmse"] for k in ranked})
    (OUT / "scores.json").write_text(json.dumps(out, indent=2) + "\n")
    print("RANKING (primary RMSE):")
    for k in ranked:
        bs = table[k]["by_series"]
        print(f"  {k:14s} {table[k]['primary_rmse']:6.2f} | " + " ".join(f"{s}={bs[s]:.1f}" if bs[s] is not None else f"{s}=na" for s in REPORT))
    for k, v in fitinfo.items():
        print(f"  {k}: starts={v['starts']} best_seed={v['best_seed']} cost={v['train_cost']:.2f} dials={ {a: round(b, 3) for a, b in v['dials'].items()} } at_bounds={v['dials_at_bounds']}")
    _figure(c, test, preds)


def _figure(c, test, preds):
    import matplotlib; matplotlib.use("Agg"); import matplotlib.pyplot as plt
    fig, axes = plt.subplots(1, 3, figsize=(13, 4))
    style = dict(persistence=("#999999", ":"), trend=("#999999", "--"), logistic=("#8c6d31", "-."),
                 K0=("#1f77b4", "-"), K1=("#2ca02c", "-"), K2=("#9467bd", "-"),
                 page_ensemble=("#d62728", "-"), silver_blend=("#000000", "-"))
    for ax, s in zip(axes, PRIMARY):
        idx = [i for i, r in enumerate(test) if r["series"] == s]
        yrs = [test[i]["year"] for i in idx]
        ax.scatter(yrs, [test[i]["value"] for i in idx], color="#222222", s=16, zorder=5, label="observed")
        for k, (col, ls) in style.items():
            if k in preds:
                ax.plot(yrs, preds[k][idx], color=col, ls=ls, lw=1.6 if k in ("page_ensemble", "silver_blend") else 1.0, label=k)
        ax.set_title(s); ax.spines[["top", "right"]].set_visible(False)
    axes[0].legend(frameon=False, fontsize=7)
    fig.suptitle("Philippines KISS run: held-out years (not blind)")
    fig.tight_layout(); fig.savefig(OUT / "fig_kiss_heldout.png", dpi=150)


def cmd_mc(spec, n):
    """Monte Carlo band: draw parameters from the Gauss-Newton covariance at the best fit; re-run the model."""
    c, train, test, _ = _rows()
    best, _ = _best(spec)
    names, x = best["names"], np.array(best["x"])
    f = _resid_fn(c, spec, train)
    r0 = f(x); J = np.zeros((len(r0), len(x)))
    for j in range(len(x)):
        h = 1e-3 * max(1.0, abs(x[j])); xx = x.copy(); xx[j] += h; J[:, j] = (f(xx) - r0) / h
    dof = max(len(r0) - len(x), 1); s2 = float(r0 @ r0) / dof
    cov = np.linalg.pinv(J.T @ J) * s2
    lo = np.array([BOUNDS[k][0] for k in names]); hi = np.array([BOUNDS[k][1] for k in names])
    rng = np.random.default_rng(42)
    draws = np.clip(rng.multivariate_normal(x, cov, size=n, check_valid="ignore"), lo, hi)
    m = E.Model6PHL(c, best["params"], spec=spec)
    P = np.array([C5._pred(m.set_params(_params(spec, d)).run(), test) for d in draws], float)
    q05, q50, q95 = np.nanpercentile(P, [5, 50, 95], axis=0)
    obs = np.array([r["value"] for r in test])
    cover = {}
    for s in REPORT:
        idx = [i for i, r in enumerate(test) if r["series"] == s]
        cover[s] = float(np.mean((obs[idx] >= q05[idx]) & (obs[idx] <= q95[idx])))
    out = dict(spec=spec, draws=n, method="Gauss-Newton covariance at best fit; draws clipped to bounds",
               note="Parameter uncertainty only; ignores model-structure uncertainty, so bands are too narrow if the model is wrong.",
               coverage_90pct_band=cover, param_sd={k: float(np.sqrt(max(cov[i, i], 0))) for i, k in enumerate(names)},
               band=[dict(series=r["series"], year=r["year"], obs=r["value"], q05=float(a), q50=float(b), q95=float(cc))
                     for r, a, b, cc in zip(test, q05, q50, q95)])
    (OUT / f"mc_{spec}.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"MC {spec}: 90% band coverage of held-out obs: " + ", ".join(f"{k}={v:.0%}" for k, v in cover.items()))


if __name__ == "__main__":
    a = sys.argv[1:]
    if a[0] == "fit":
        cmd_fit(a[1], int(a[2]))
    elif a[0] == "score":
        cmd_score()
    elif a[0] == "mc":
        cmd_mc(a[1], int(a[2]) if len(a) > 2 else 300)
    elif a[0] == "all":
        for s in SPECS:
            for seed in range(N_SEEDS):
                cmd_fit(s, seed)
        cmd_score()
        for s in SPECS:
            cmd_mc(s, 300)
