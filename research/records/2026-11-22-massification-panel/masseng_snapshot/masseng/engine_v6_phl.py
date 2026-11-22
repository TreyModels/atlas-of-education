"""Pre-registered Philippine demand-and-capacity experiment (PROTOCOL_v6_phl.md).

Cleanly extends engine5.py without altering v5 files or outputs:
1. Splits private-sector income slope into nu_basic (basic levels) and nu_ter (tertiary).
2. Uses bounded saturating positional pull g(S) = S / (S + 0.25) in [0, 1) (our modelling adaptation).
3. Supports the 6 nested specs in PROTOCOL_v6_phl.md (P0, P1_con, P1_unc, P2_con, P2_unc, P3_con).
4. Records Q (qualified), L (latent), E (effective), R (admitted), and accessible unfilled seats
   when illustrative declared-capacity clearing is enabled.
"""
from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares

from . import calibrate5 as C5
from .data import Country
from .engine5 import Model5, DEFAULTS as V5_DEFAULTS, PUB, PRIV, LEVEL_NAMES, N_GRADES, _sig, Result
from .array_admissions import clear_two_sector_array

V6_DEFAULTS = dict(
    V5_DEFAULTS,
    nu_basic=0.5,
    nu_ter=0.5,
    s0_sat=0.25,
)

# Level/sector intercepts + cost scale (separate from the 3-5 substantive behavioural dials)
INTERCEPT_FIT = [
    "a_prim", "a_sec", "a_sec_entry", "a_ter", "a_ter_entry",
    "c_scale", "mu_basic", "mu_ter", "nu_basic", "nu_ter",
]

# Pre-registered nested specs (PROTOCOL_v6_phl.md Section 4)
V6_SPECS = {
    "P0": dict(dials=["eta", "eta_x", "kappa"], constrained=True, z=None),
    "P1_con": dict(dials=["b_h", "eta_x", "kappa"], constrained=True, z=None),
    "P1_unc": dict(dials=["b_h", "eta_x", "kappa"], constrained=False, z=None),
    "P2_con": dict(dials=["b_h", "b_p", "eta_x", "kappa"], constrained=True, z=None),
    "P2_unc": dict(dials=["b_h", "b_p", "eta_x", "kappa"], constrained=False, z=None),
    "P3_con": dict(dials=["b_h", "b_p", "eta_x", "kappa", "lam"], constrained=True, z="gS"),
}

BASE_BOUNDS = dict(
    a_prim=(-4.0, 16.0),
    a_sec=(-4.0, 16.0),
    a_sec_entry=(-10.0, 14.0),
    a_ter=(-4.0, 16.0),
    a_ter_entry=(-12.0, 12.0),
    eta=(0.0, 6.0),
    eta_x=(0.0, 4.0),
    kappa=(0.0, 40.0),
    lam=(0.0, 12.0),
    c_scale=(0.05, 8.0),
    mu_basic=(-10.0, 6.0),
    mu_ter=(-8.0, 8.0),
    nu_basic=(-6.0, 8.0),
    nu_ter=(-6.0, 8.0),
)


def spec_bounds(spec: str) -> dict:
    b = dict(BASE_BOUNDS)
    if V6_SPECS[spec]["constrained"]:
        b["b_h"] = (0.0, 12.0)
        b["b_p"] = (0.0, 12.0)
    else:
        b["b_h"] = (-6.0, 12.0)
        b["b_p"] = (-6.0, 12.0)
    return b


def fitted_names_v6(spec: str) -> list[str]:
    return INTERCEPT_FIT + V6_SPECS[spec]["dials"]


class Model6PHL(Model5):
    """Subclass of Model5 preserving exact cohort/target accounting while implementing PROTOCOL_v6_phl.md."""

    def __init__(self, country: Country, params=None, spec: str = "P2_con", switches=None, annual_market: bool = False):
        # Initialize parent with R1 placeholder, then apply v6_phl spec rules
        super().__init__(country, params=None, spec="R1", switches=switches, annual_market=annual_market)
        self.v6_spec = spec
        self.zsrc = V6_SPECS[spec]["z"]
        self.set_params(params or {})

    def set_params(self, params):
        self.p = dict(V6_DEFAULTS)
        if params:
            self.p.update({k: v for k, v in params.items() if k in V6_DEFAULTS})
        allowed = set(V6_SPECS[self.v6_spec]["dials"])
        for k in ("b_h", "b_p", "b_r", "lam", "eta"):
            if k not in allowed:
                self.p[k] = 0.0
        return self

    def _g(self, s_val: float) -> float:
        s0 = float(self.p.get("s0_sat", 0.25))
        return float(s_val / (s_val + s0))

    def _base(self, yi, li, S):
        p = self.p
        return (
            p["b_h"] * self.prem[yi, li]
            + p["b_p"] * self._g(S[li])
            + p["eta"] * self.lngdp[yi]
            + p["eta_x"] * self.lnmult[yi]
        )

    def _v(self, yi, li, S):
        p = self.p
        z = self._g(S[li]) if self.zsrc == "gS" else 0.0
        k = p["kappa"] * np.exp(-p["lam"] * z)
        cost = p["c_scale"] * self.direct[yi, li, :][None, :] + self.forgone[yi, li]
        burden = (cost - self.transfer[yi, :, li][:, None]).clip(0.0) / self.mult[yi][:, None]
        v = -k * np.log1p(burden)
        if li == 3:
            v[:, PRIV] += p["mu_ter"] + p["nu_ter"] * (self.lngdp[yi] + self.lnmult[yi])
        else:
            v[:, PRIV] += p["mu_basic"] + p["nu_basic"] * (self.lngdp[yi] + self.lnmult[yi])
        return v

    def _entry_prob(self, yi, li, base, V, S, latent=False):
        if not latent:
            return _sig(base + np.logaddexp(V[li][:, PUB], V[li][:, PRIV]))
        p = self.p
        z = self._g(S[li]) if self.zsrc == "gS" else 0.0
        k = p["kappa"] * np.exp(-p["lam"] * z)
        free_burden = np.maximum(self.forgone[yi, li] / self.mult[yi], 0.0)
        free = np.repeat((-k * np.log1p(free_burden))[:, None], 2, axis=1)
        if li == 3:
            free[:, PRIV] += p["mu_ter"] + p["nu_ter"] * (self.lngdp[yi] + self.lnmult[yi])
        else:
            free[:, PRIV] += p["mu_basic"] + p["nu_basic"] * (self.lngdp[yi] + self.lnmult[yi])
        best = np.maximum(V[li], free)
        return _sig(base + np.logaddexp(best[:, PUB], best[:, PRIV]))


def fit_v6_phl(country: Country, train: list[dict], spec: str, start: dict | None = None, max_nfev: int = 250, ftol: float = 1e-7) -> dict:
    assert all(r["role"] == "train" for r in train), "fit_v6_phl() received non-training rows"
    names = fitted_names_v6(spec)
    bounds = spec_bounds(spec)
    base = dict(V6_DEFAULTS)
    if start:
        base.update({k: v for k, v in start.items() if k in base})
    model = Model6PHL(country, base, spec=spec)
    lo = np.array([bounds[n][0] for n in names], dtype=float)
    hi = np.array([bounds[n][1] for n in names], dtype=float)
    x0 = np.array([np.clip(base[n], bounds[n][0], bounds[n][1]) for n in names], dtype=float)
    obs = np.array([r["value"] for r in train], dtype=float)
    scale = np.array([
        10.0 if r["series"].startswith("edu_share") else (100.0 if r.get("transform") == "index_2016" else 1.0)
        for r in train
    ], dtype=float)
    w = C5._w(train) * scale

    def resid(x):
        prm = dict(base)
        prm.update(dict(zip(names, x)))
        res = model.set_params(prm).run()
        return np.nan_to_num((C5._pred(res, train) - obs) * w, nan=50.0)

    sol = least_squares(resid, x0, bounds=(lo, hi), x_scale="jac", max_nfev=max_nfev, diff_step=1e-3, ftol=ftol, xtol=ftol)
    prm = dict(base)
    prm.update(dict(zip(names, sol.x)))
    at_bounds = [
        n for n, v in zip(names, sol.x)
        if abs(v - bounds[n][0]) < 1e-3 or abs(v - bounds[n][1]) < 1e-3
    ]
    dials_at_bounds = [n for n in V6_SPECS[spec]["dials"] if n in at_bounds]
    return dict(
        params=prm,
        fitted=names,
        substantive_dials=V6_SPECS[spec]["dials"],
        intercepts=INTERCEPT_FIT,
        cost=float(sol.cost),
        nfev=int(sol.nfev),
        status=int(sol.status),
        message=str(sol.message),
        spec=spec,
        constrained=V6_SPECS[spec]["constrained"],
        at_bounds=at_bounds,
        dials_at_bounds=dials_at_bounds,
    )


def score_v6_phl(country: Country, fit_obj: dict, rows: list[dict]):
    res = Model6PHL(country, fit_obj["params"], spec=fit_obj["spec"]).run(record_deciles=True)
    test = [r for r in rows if r["role"] == "test"]
    window = [r for r in rows if r["role"] in ("train", "diagnostic") and r["year"] <= country.config["years"]["train"][1]]
    pred = C5._pred(res, test)
    bm = C5.benchmarks(window, test)
    table = {}
    for s in sorted({r["series"] for r in test}):
        idx = [i for i, r in enumerate(test) if r["series"] == s]
        o = np.array([test[i]["value"] for i in idx])
        def _rmse(p):
            p = np.asarray(p, float)
            m = ~np.isnan(p)
            return float(np.sqrt(np.mean((p[m] - o[m]) ** 2))) if m.any() else np.nan
        table[s] = dict(
            n=len(idx),
            model=_rmse(pred[idx]),
            persistence=_rmse(bm[idx, 0]),
            trend=_rmse(bm[idx, 1]),
            obs=o.tolist(),
            pred=pred[idx].tolist(),
            years=[test[i]["year"] for i in idx],
        )
    return res, table
