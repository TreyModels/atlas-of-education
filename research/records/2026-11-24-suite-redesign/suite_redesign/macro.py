"""H1: country-decade panel, FE regression with country-clustered SE, and the slope-overlap test."""
import numpy as np
from scipy import stats

import model

N_COUNTRIES = 24
SIGMA_Y = (0.45, 0.55, 0.65)
SIGMA_A = (0.15, 0.20, 0.25)
H1_SEED_BASE = 20270101


def country_nuisance(c):
    return {"sigma_y": SIGMA_Y[c % 3], "sigma_a": SIGMA_A[(c // 3) % 3]}


def build_panel(world, s=1.0, countries=N_COUNTRIES, years=model.YEARS):
    """Rows: (country, decade, D_cl_observed, D_GER) over 10-year changes, t=10..24."""
    rows = []
    for c in range(countries):
        res = model.run_unit(world, s, H1_SEED_BASE + 100 * c, years=years,
                             **country_nuisance(c))
        ys = model.year_stats(res)
        for t in range(model.SHOCK_YEAR, years):
            dec = 1 if t < 15 else (2 if t < 20 else 3)
            rows.append((c, dec, ys["cl_observed"][t] - ys["cl_observed"][t - 10],
                         ys["ger"][t] - ys["ger"][t - 10]))
    return np.array(rows, dtype=np.float64)


def _design(panel, world_dummies=False):
    """[const, (wS, wC), decade d2, d3, D_GER, (D_GER*wS, D_GER*wC)]."""
    C = panel[:, 0].astype(int)
    dec = panel[:, 1].astype(int)
    dger = panel[:, 3]
    cols = [np.ones(len(panel)), (dec == 2).astype(float), (dec == 3).astype(float), dger]
    return np.column_stack(cols), C


def _design_pooled(panels):
    parts = []
    for w, panel in panels.items():
        X, C = _design(panel)
        X = np.column_stack([
            X[:, 0], np.full(len(X), 1.0 if w == "S" else 0.0),
            np.full(len(X), 1.0 if w == "C" else 0.0),
            X[:, 1], X[:, 2], X[:, 3],
            X[:, 3] * (1.0 if w == "S" else 0.0), X[:, 3] * (1.0 if w == "C" else 0.0),
        ])
        parts.append((X, C, panel[:, 2]))
    X = np.vstack([p[0] for p in parts])
    C = np.concatenate([p[1] for p in parts])
    y = np.concatenate([p[2] for p in parts])
    return X, y, C


def ols_cluster(y, X, groups):
    """OLS with country-clustered sandwich covariance (finite-sample adjusted)."""
    n, k = X.shape
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ beta
    XtX_inv = np.linalg.inv(X.T @ X)
    meat = np.zeros((k, k))
    ug = np.unique(groups)
    for g in ug:
        m = groups == g
        s = X[m].T @ e[m]
        meat += np.outer(s, s)
    G = len(ug)
    scale = (G / (G - 1.0)) * ((n - 1.0) / (n - k))
    V = XtX_inv @ meat @ XtX_inv * scale
    return beta, V


def wald_p(beta, V, idx):
    b = beta[idx]
    VV = V[np.ix_(idx, idx)]
    stat = float(b @ np.linalg.solve(VV, b))
    return stat, float(stats.chi2.sf(stat, len(idx)))


def bootstrap_slopes(panels, n_boot=400, rng_seed=20261124):
    """Country-level cluster bootstrap (same resample across worlds; paired design)."""
    rng = np.random.default_rng(rng_seed)
    out = {w: [] for w in panels}
    for _ in range(n_boot):
        countries = rng.integers(0, N_COUNTRIES, size=N_COUNTRIES)
        mapping = {c: np.where(countries == c)[0] for c in range(N_COUNTRIES)}
        for w, panel in panels.items():
            idx = []
            for old, new_idxs in mapping.items():
                rows = np.where(panel[:, 0].astype(int) == old)[0]
                for j, ni in enumerate(new_idxs):
                    block = panel[rows].copy()
                    block[:, 0] = ni  # relabel resampled country
                    idx.append(block)
            boot = np.vstack(idx)
            X, C = _design(boot)
            beta, _ = ols_cluster(boot[:, 2], X, C)
            out[w].append(float(beta[3]))
    return {w: np.array(v) for w, v in out.items()}


def overlap(ci_a, ci_b):
    lo = max(ci_a[0], ci_b[0])
    hi = min(ci_a[1], ci_b[1])
    union = max(ci_a[1], ci_b[1]) - min(ci_a[0], ci_b[0])
    return float(max(0.0, hi - lo) / union) if union > 0 else 0.0


def run_h1(seed_log):
    panels = {}
    slopes = {}
    for w in model.WORLDS:
        panel = build_panel(w, 1.0)
        panels[w] = panel
        X, C = _design(panel)
        beta, V = ols_cluster(panel[:, 2], X, C)
        slopes[w] = {"beta": float(beta[3]), "se": float(np.sqrt(V[3, 3])),
                     "n_rows": int(len(panel)), "n_countries": N_COUNTRIES}
        seed_log.append({"stage": "h1_panel", "world": w, "rows": int(len(panel))})

    Xp, yp, Cp = _design_pooled(panels)
    beta_p, V_p = ols_cluster(yp, Xp, Cp)
    stat, p_joint = wald_p(beta_p, V_p, [6, 7])

    boot = bootstrap_slopes(panels)
    ci = {w: [float(np.quantile(boot[w], 0.025)), float(np.quantile(boot[w], 0.975))]
          for w in panels}
    overlaps = {}
    for a in model.WORLDS:
        for b in model.WORLDS:
            if a < b:
                overlaps[f"{a}-{b}"] = overlap(ci[a], ci[b])

    wall = bool(p_joint > 0.05 and all(v >= 0.75 for v in overlaps.values()))
    return {
        "design": {"countries": N_COUNTRIES, "years": model.YEARS,
                   "nuisance_grid": {"sigma_y": SIGMA_Y, "sigma_a": SIGMA_A},
                   "seed_base": H1_SEED_BASE, "batch_layout": model.LAYOUT,
                   "outcome": "D_cl_observed on D_GER, decade FE, country-clustered SE"},
        "slopes": slopes,
        "boot_ci95": ci,
        "pair_overlap": overlaps,
        "joint_interaction": {"wald_chi2": stat, "df": 2, "p": p_joint},
        "decision_rule": "cannot separate iff joint p>0.05 and all pairwise overlaps >= 0.75",
        "verdict": "cannot separate (wall holds in this redesign)" if wall else "separable",
        "verdict_code": "cannot_separate" if wall else "separable",
        "label": "SIMULATION",
    }
