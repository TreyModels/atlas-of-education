"""Triad test: households, employers, state. Same engine and the same enrolment-only targets in PHL, KHM and HKG.

Pre-registered in PROTOCOL_triad.md. Commands (package root, PYTHONPATH=.):
  python scripts/triad.py fit ISO SPEC SEED        one fit (seed 0 = default start)
  python scripts/triad.py score ISO                best start per spec; held-out scores + ensemble + blend
  python scripts/triad.py ident ISO TRUTH REP      one Monte Carlo identification replicate (simulate TRUTH, refit all 4 specs)
  python scripts/triad.py identsum ISO             confusion matrix + parameter recovery
  python scripts/triad.py jobs [fit|ident]         print every job line (feed to xargs -P N)
"""
from __future__ import annotations
import json, sys, time
from pathlib import Path
import numpy as np
from scipy.optimize import least_squares, curve_fit

import masseng.engine_v6_phl as E
from masseng.data import Country, Series
from masseng import calibrate5 as C5

ROOT = Path("outputs/triad")
COUNTRIES = ["PHL", "KHM", "HKG"]
SPLIT = {"PHL": (1995, 2024), "KHM": (2010, 2024), "HKG": (2011, 2024)}   # train <= first; test (first, second]
SPECS = {
    "H":   ["eta", "kappa"],                 # households: income + household cost ("rice")
    "HE":  ["eta", "kappa", "b_e"],          # + employers: non-farm employment share ("formatted workers")
    "HS":  ["eta", "kappa", "b_s"],          # + state: public education effort ("F-16s" / surplus)
    "HES": ["eta", "kappa", "b_e", "b_s"],   # full triad
}
INTERCEPTS = ["a_prim", "a_sec", "a_sec_entry", "a_ter", "a_ter_entry"]
FIXED = dict(c_scale=1.0, eta_x=0.0, mu_basic=-2.5, mu_ter=1.0, nu_basic=0.5, nu_ter=0.5, b_h=0.0, b_p=0.0, b_r=0.0, lam=0.0)
BOUNDS = dict(E.BASE_BOUNDS, b_e=(0.0, 20.0), b_s=(0.0, 20.0))
SERIES = ["ner_primary", "ner_secondary", "ger_tertiary", "ger_primary", "ger_secondary"]
N_SEEDS = 6
N_REPS = 20
NOISE_PP = 1.0

# ---- drivers -----------------------------------------------------------------------------
DRIVER_FILE = Path("countries/triad_drivers.json")
# preference order for each actor; first series found wins (declared before fitting)
EMPLOYER_KEYS = ["nonagri_employment_share", "non_agricultural_employment_share", "nonfarm_share", "formal_share"]
STATE_KEYS = ["gov_edu_spend_gdp", "SE.XPD.TOTL.GD.ZS"]


def _load_driver(c, iso, keys):
    raw = json.loads(DRIVER_FILE.read_text()).get(iso, {}) if DRIVER_FILE.exists() else {}
    for k in keys:
        if k in raw and raw[k].get("points"):
            return k, Series(raw[k]["points"])
        if k in (c.drivers or {}):
            return k, c.drivers[k]
        s = c.wdi(k)
        if s is not None:
            return k, s
    return None, None


class TriadModel(E.Model6PHL):
    def __init__(self, country, params, spec, iso):
        self.tspec = spec
        ek, es = _load_driver(country, iso, EMPLOYER_KEYS)
        sk, ss = _load_driver(country, iso, STATE_KEYS)
        super().__init__(country, params, spec=spec)
        yrs = self.years
        self.Edrv = np.array([es(y) for y in yrs]) if es is not None else np.zeros(len(yrs))
        self.Edrv = self.Edrv / 100.0 if np.nanmax(self.Edrv) > 1.5 else self.Edrv
        self.Sdrv = np.array([ss(y) for y in yrs]) / 10.0 if ss is not None else np.zeros(len(yrs))   # % GDP / 10
        self.driver_info = dict(employer=ek, state=sk,
                                employer_years=[int(es.years[0]), int(es.years[-1])] if es is not None else None,
                                state_years=[int(ss.years[0]), int(ss.years[-1])] if ss is not None else None)
        self.set_params(params)

    def set_params(self, params):
        super().set_params(params)
        for k in ("b_e", "b_s"):
            self.p[k] = float(params.get(k, 0.0)) if (params and k in SPECS[self.tspec]) else 0.0
        return self

    def _base(self, yi, li, S):
        return super()._base(yi, li, S) + self.p["b_e"] * self.Edrv[yi] + self.p["b_s"] * self.Sdrv[yi]


for k, d in SPECS.items():
    E.V6_SPECS[k] = dict(dials=[x for x in d if x in ("eta", "kappa")], constrained=True, z=None)
    # eta must not be zeroed by the parent; kappa is always active


def _rows(iso):
    c = Country(iso)
    tr_end, te_end = SPLIT[iso]
    rows = C5.build_rows(c)
    keep = [dict(r) for r in rows if r["series"] in SERIES and r.get("transform") is None]
    for r in keep:
        r["role"] = "train" if r["year"] <= tr_end else ("test" if r["year"] <= te_end else "out")
    train = [r for r in keep if r["role"] == "train"]
    test = [r for r in keep if r["role"] == "test"]
    # primary metric: NER where the series has held-out data, else GER of that level; tertiary is GER
    prim = []
    for lev in ("primary", "secondary"):
        prim.append(f"ner_{lev}" if any(r["series"] == f"ner_{lev}" for r in test) else f"ger_{lev}")
    prim.append("ger_tertiary")
    return c, train, test, prim


def _names(spec):
    return INTERCEPTS + SPECS[spec]


def _params(spec, x):
    p = dict(E.V6_DEFAULTS); p.update(FIXED); p.update(dict(zip(_names(spec), x))); return p


def _model(c, iso, spec, params=None):
    return TriadModel(c, params or _params(spec, [dict(E.V6_DEFAULTS, **FIXED).get(n, 0.0) for n in _names(spec)]), spec, iso)


def _fit(c, iso, spec, rows, x0):
    names = _names(spec)
    lo = np.array([BOUNDS[n][0] for n in names]); hi = np.array([BOUNDS[n][1] for n in names])
    m = _model(c, iso, spec)
    obs = np.array([r["value"] for r in rows]); w = C5._w(rows)
    def f(x):
        return np.nan_to_num((C5._pred(m.set_params(_params(spec, x)).run(), rows) - obs) * w, nan=50.0)
    sol = least_squares(f, np.clip(x0, lo, hi), bounds=(lo, hi), x_scale="jac", diff_step=1e-3,
                        max_nfev=300, ftol=1e-7, xtol=1e-7)
    at = [n for n, v in zip(names, sol.x) if min(abs(v - BOUNDS[n][0]), abs(v - BOUNDS[n][1])) < 1e-2]
    return sol, at, m


def _x0(spec, seed):
    names = _names(spec)
    if seed == 0:
        base = dict(E.V6_DEFAULTS, **FIXED); base.update(b_e=0.0, b_s=0.0)
        return np.array([base.get(n, 0.0) for n in names], float)
    lo = np.array([BOUNDS[n][0] for n in names]); hi = np.array([BOUNDS[n][1] for n in names])
    return np.random.default_rng(9000 + seed).uniform(lo, hi)


def cmd_fit(iso, spec, seed):
    c, train, _, _ = _rows(iso)
    t = time.time()
    sol, at, m = _fit(c, iso, spec, train, _x0(spec, seed))
    out = dict(iso=iso, spec=spec, seed=seed, names=_names(spec), x=sol.x.tolist(), params=_params(spec, sol.x),
               cost=float(sol.cost), n_train=len(train), nfev=int(sol.nfev), status=int(sol.status),
               hit_nfev_cap=bool(sol.nfev >= 300), at_bounds=at, dials_at_bounds=[n for n in SPECS[spec] if n in at],
               drivers=m.driver_info, seconds=round(time.time() - t, 1))
    d = ROOT / iso / "fits"; d.mkdir(parents=True, exist_ok=True)
    (d / f"{spec}_seed{seed:02d}.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"FIT {iso} {spec} seed{seed}: cost={out['cost']:.3f} dials_at_bounds={out['dials_at_bounds']} ({out['seconds']}s)", flush=True)


def _best(iso, spec):
    fs = sorted((json.loads(p.read_text()) for p in (ROOT / iso / "fits").glob(f"{spec}_seed*.json")), key=lambda f: f["cost"])
    return (fs[0] if fs else None), fs


def _rmse(p, o):
    p = np.asarray(p, float); o = np.asarray(o, float); k = np.isfinite(p) & np.isfinite(o)
    return float(np.sqrt(np.mean((p[k] - o[k]) ** 2))) if k.any() else None


def _logistic(train, test, cap=110.0):
    out = np.full(len(test), np.nan)
    for s in SERIES:
        h = sorted((r["year"], r["value"]) for r in train if r["series"] == s)
        if len(h) < 4:
            continue
        t = np.array([a for a, _ in h], float); y = np.array([b for _, b in h], float)
        f = lambda tt, L, k, t0: L / (1 + np.exp(-k * (tt - t0)))
        try:
            p, _ = curve_fit(f, t, y, p0=[min(cap, y.max() * 1.2), 0.05, t.mean()],
                             bounds=([y.max() * 0.9, 0.0, 1900], [max(cap, y.max() * 0.9 + 1e-6), 1.0, 2100]), maxfev=20000)
            for i, r in enumerate(test):
                if r["series"] == s:
                    out[i] = f(r["year"], *p)
        except Exception:
            pass
    return out


def _bench(train, test):
    """Persistence = last training value; trend = linear fit over training values of that series."""
    out = np.full((len(test), 2), np.nan)
    for i, r in enumerate(test):
        h = sorted((q["year"], q["value"]) for q in train if q["series"] == r["series"])
        if not h:
            continue
        out[i, 0] = h[-1][1]
        if len(h) >= 3:
            out[i, 1] = float(np.polyval(np.polyfit([a for a, _ in h], [b for _, b in h], 1), r["year"]))
    return out


def cmd_score(iso):
    c, train, test, prim = _rows(iso)
    obs = np.array([r["value"] for r in test])
    preds, info = {}, {}
    for spec in SPECS:
        b, fs = _best(iso, spec)
        if b is None:
            continue
        m = _model(c, iso, spec, b["params"])
        preds[spec] = np.asarray(C5._pred(m.run(), test), float)
        info[spec] = dict(best_seed=b["seed"], train_cost=b["cost"], n_train=b["n_train"], starts=len(fs),
                          start_costs=sorted(round(f["cost"], 3) for f in fs),
                          dials={n: b["params"].get(n) for n in SPECS[spec]}, dials_at_bounds=b["dials_at_bounds"],
                          aic=2 * b["n_train"] * 0 + b["n_train"] * np.log(2 * b["cost"] / b["n_train"]) + 2 * len(b["names"]),
                          drivers=b["drivers"])
    bm = _bench(train, test)
    preds["persistence"], preds["trend"] = bm[:, 0], bm[:, 1]
    preds["logistic"] = _logistic(train, test)
    members = [k for k in ("H", "HE", "HS", "HES", "logistic") if k in preds]
    preds["page_ensemble"] = np.nanmean(np.vstack([preds[k] for k in members]), axis=0)
    preds["silver_blend"] = 0.5 * preds["persistence"] + 0.5 * preds["page_ensemble"]
    sel = [i for i, r in enumerate(test) if r["series"] in prim]
    table = {k: dict(primary_rmse=_rmse(p[sel], obs[sel]),
                     by_series={s: _rmse(p[[i for i, r in enumerate(test) if r["series"] == s]],
                                         obs[[i for i, r in enumerate(test) if r["series"] == s]]) for s in SERIES})
             for k, p in preds.items()}
    ranked = sorted([k for k in table if table[k]["primary_rmse"] is not None], key=lambda k: table[k]["primary_rmse"])
    best_naive = min(table["persistence"]["primary_rmse"], table["trend"]["primary_rmse"] or 1e9)
    actor_verdict = {}
    for spec, actor in (("HE", "employer"), ("HS", "state")):
        if spec in table and "H" in table:
            actor_verdict[actor] = dict(
                improves_on_H=table[spec]["primary_rmse"] < table["H"]["primary_rmse"],
                beats_logistic=table[spec]["primary_rmse"] < (table["logistic"]["primary_rmse"] or 1e9),
                dial_off_bound=not info[spec]["dials_at_bounds"],
                supported=bool(table[spec]["primary_rmse"] < table["H"]["primary_rmse"]
                               and table[spec]["primary_rmse"] < (table["logistic"]["primary_rmse"] or 1e9)
                               and not info[spec]["dials_at_bounds"]))
    out = dict(iso=iso, split=SPLIT[iso], primary_series=prim, n_test_primary=len(sel), ranking=ranked, table=table,
               fits=info, page_ensemble_members=members, best_naive_rmse=best_naive,
               beats_naive={k: table[k]["primary_rmse"] < best_naive for k in ranked}, actor_verdict=actor_verdict)
    (ROOT / iso).mkdir(parents=True, exist_ok=True)
    (ROOT / iso / "scores.json").write_text(json.dumps(out, indent=2, default=float) + "\n")
    print(f"== {iso} primary={prim} n_test={len(sel)}")
    for k in ranked:
        print(f"  {k:14s} {table[k]['primary_rmse']:6.2f}")
    for k, v in info.items():
        print(f"  {k}: cost={v['train_cost']:.2f} dials={ {a: round(b, 3) for a, b in v['dials'].items()} } at_bounds={v['dials_at_bounds']} drivers={v['drivers']}")
    print("  actors:", actor_verdict)


def cmd_ident(iso, truth, rep):
    """Simulate training data from TRUTH's fitted parameters (+ noise), refit all specs; record winner by AIC."""
    c, train, _, _ = _rows(iso)
    b, _ = _best(iso, truth)
    m = _model(c, iso, truth, b["params"])
    synth = np.asarray(C5._pred(m.run(), train), float)
    rng = np.random.default_rng(100000 + 1000 * list(SPECS).index(truth) + rep)
    rows = []
    for r, v in zip(train, synth):
        q = dict(r); q["value"] = float(v + rng.normal(0, NOISE_PP)); rows.append(q)
    res = {}
    for spec in SPECS:
        bs, _ = _best(iso, spec)
        sol, at, _ = _fit(c, iso, spec, rows, np.array(bs["x"]))   # start at that spec's real-data fit
        n = len(rows)
        res[spec] = dict(cost=float(sol.cost), k=len(sol.x), aic=n * np.log(2 * sol.cost / n) + 2 * len(sol.x),
                         dials={nm: float(v) for nm, v in zip(_names(spec), sol.x) if nm in SPECS[spec]}, at_bounds=at)
    winner = min(res, key=lambda s: res[s]["aic"])
    d = ROOT / iso / "ident"; d.mkdir(parents=True, exist_ok=True)
    (d / f"{truth}_rep{rep:02d}.json").write_text(json.dumps(dict(truth=truth, rep=rep, winner=winner, truth_dials=
        {k: b["params"][k] for k in SPECS[truth]}, fits=res), indent=2) + "\n")
    print(f"IDENT {iso} truth={truth} rep{rep}: winner={winner}", flush=True)


def cmd_identsum(iso):
    d = ROOT / iso / "ident"
    conf = {t: {s: 0 for s in SPECS} for t in SPECS}
    rec = {}
    for p in d.glob("*.json"):
        j = json.loads(p.read_text())
        conf[j["truth"]][j["winner"]] += 1
        for k, tv in j["truth_dials"].items():
            rec.setdefault((j["truth"], k), []).append((tv, j["fits"][j["truth"]]["dials"][k], k in j["fits"][j["truth"]]["at_bounds"]))
    recovery = {}
    for (t, k), v in rec.items():
        tv = v[0][0]; est = np.array([e for _, e, _ in v]); hits = sum(h for *_, h in v)
        within = None if abs(tv) < 1e-6 else float(np.mean(np.abs(est - tv) <= 0.25 * abs(tv)))
        lab = ("boundary-censored / not cleanly identified" if hits / len(v) > 0.2 or abs(tv - BOUNDS[k][0]) < 1e-2 or abs(tv - BOUNDS[k][1]) < 1e-2
               else ("identified (software diagnostic)" if within is not None and within >= 0.8 else "not identified"))
        recovery[f"{t}:{k}"] = dict(truth=tv, median=float(np.median(est)), within_25pct=within, bound_hits=hits, n=len(v), label=lab)
    out = dict(iso=iso, rule="winner = lowest AIC on simulated training data; rows = truth, cols = chosen", confusion=conf, recovery=recovery)
    (ROOT / iso / "identification.json").write_text(json.dumps(out, indent=2) + "\n")
    print(f"== {iso} confusion (truth -> chosen):")
    for t in SPECS:
        print(f"  {t:4s}", conf[t])
    for k, v in recovery.items():
        print(f"  {k:10s} truth={v['truth']:.3f} med={v['median']:.3f} within25={v['within_25pct']} hits={v['bound_hits']}/{v['n']} -> {v['label']}")


def cmd_jobs(kind):
    for iso in COUNTRIES:
        for spec in SPECS:
            if kind == "fit":
                for s in range(N_SEEDS):
                    print(f"fit {iso} {spec} {s}")
            else:
                for r in range(N_REPS):
                    print(f"ident {iso} {spec} {r}")


if __name__ == "__main__":
    a = sys.argv[1:]
    {"fit": lambda: cmd_fit(a[1], a[2], int(a[3])), "score": lambda: cmd_score(a[1]),
     "ident": lambda: cmd_ident(a[1], a[2], int(a[3])), "identsum": lambda: cmd_identsum(a[1]),
     "jobs": lambda: cmd_jobs(a[1])}[a[0]]()
