"""Layer 2 (frozen accounting/outcomes dashboard) for the v6 gate+jobs prototype.

Measurement only: this module receives the raw arrays produced by the behavioural core and returns a fixed set of
outcomes and accounting identities. It never sees a structural switch, never runs a model, and never changes which
arrays are produced -- so the same dashboard is applied to every swapped model, which is what lets us say which
equation block moves which outcome. All quantities are simulation, not estimates.
"""
from __future__ import annotations

import numpy as np

QUINTILES = ((0, 1), (2, 3), (4, 5), (6, 7), (8, 9))


def _gini(x):
    x = np.sort(np.asarray(x, float))
    x = x[np.isfinite(x)]
    n = len(x)
    s = x.sum()
    if n == 0 or s <= 0:
        return float("nan")
    idx = np.arange(1, n + 1)
    return float(2.0 * np.sum(idx * x) / (n * s) - (n + 1) / n)


def _by_quintile(values, decile, weights=None, reduce="mean"):
    out = []
    values = np.asarray(values, float)
    for lo, hi in QUINTILES:
        m = (decile >= lo) & (decile <= hi)
        v = values[m]
        if reduce == "mean":
            out.append(float(np.nanmean(v)) if np.isfinite(v).any() else float("nan"))
        else:
            out.append(float(np.nansum(v)))
    return out


def _ols_slope(x, y):
    m = np.isfinite(x) & np.isfinite(y)
    if m.sum() < 10:
        return float("nan")
    x, y = x[m], y[m]
    x = x - x.mean()
    return float((x * (y - y.mean())).sum() / max((x * x).sum(), 1e-12))


def outcomes(d: dict) -> dict:
    """Turn raw arrays into the frozen dashboard. No structural switches are read here."""
    n = d["n"]
    decile = np.asarray(d["decile"])
    income = np.asarray(d["income"], float)
    ability = np.asarray(d["ability"], float)
    cred = np.asarray(d["cred"], int)
    prep = np.asarray(d["prep"], float)
    prep_any = (prep > 0).any(axis=1)
    spend_share = np.asarray(d["prep_spend"], float)          # prep outlay as a share of household income
    spend_units = spend_share * income                       # prep outlay in mean-income units
    learning = np.asarray(d["learning"], float)
    admitted = np.asarray(d["admitted"], bool)
    state = np.asarray(d["state"], int)
    formal = np.asarray(d["formal"], float)      # expected formal-work share per cell (fractional mass, in [0,1])
    pay = np.asarray(d["pay"], float)
    queue = np.asarray(d["queue_years"], float)
    hidden_income = np.asarray(d["hidden_income"], float)
    eligible = state >= 0                        # reached the gate (was in a school state at that level)
    with np.errstate(invalid="ignore"):
        mean_learning = np.nanmean(learning, axis=1) if learning.size else np.full(n, np.nan)

    out = {
        "n": int(n),
        "ger": [float(x) if np.isfinite(x) else None for x in d.get("ger", [])],
        "q_public": [float(x) if np.isfinite(x) else None for x in d.get("q_pub", [])],
        "mean_learning": float(np.nanmean(mean_learning)),
        "prep_participation": float(prep_any.mean()),
        "prep_participation_by_gate": [float(np.mean(prep[:, g] > 0)) for g in range(prep.shape[1])],
        "prep_spend_share_mean": float(np.nanmean(spend_share)),
        "prep_spend_units_mean": float(np.nanmean(spend_units)),
        "prep_spend_share_by_quintile": _by_quintile(spend_share, decile),
        "prep_participation_by_quintile": _by_quintile(prep_any.astype(float), decile),
        # Dang-2007-style income elasticity of tutoring expenditure (mean-income units, buyers only)
        "prep_income_elasticity": _ols_slope(np.log(income[prep_any]), np.log(spend_units[prep_any]))
        if (prep_any & (spend_units > 0)).sum() > 10 else float("nan"),
        "credential_shares": [float(np.mean(cred == c)) for c in range(4)],
        "admission_rate": [float(admitted[:, g].sum() / max(eligible[:, g].sum(), 1)) for g in range(admitted.shape[1])],
        "admission_by_quintile": [_by_quintile(admitted[:, g].astype(float), decile) for g in range(admitted.shape[1])],
        "pushout_by_quintile": [_by_quintile((eligible[:, g] & ~admitted[:, g]).astype(float), decile)
                                for g in range(admitted.shape[1])],
        "admission_ability_correlation": [
            float(np.corrcoef(ability[eligible[:, g]], admitted[eligible[:, g], g])[0, 1])
            if eligible[:, g].sum() > 2 else float("nan") for g in range(admitted.shape[1])],
        "state_shares_by_quintile": {
            name: _by_quintile((state[:, 0] == i).astype(float), decile)
            for i, name in enumerate(("school_only", "study_and_work", "visible_work_only", "hidden_work"))},
        "hidden_work_income_mean": float(np.nanmean(hidden_income)),
        "formal_share": float(np.nanmean(formal.astype(float))),
        "formal_share_by_credential": [float(np.mean(formal[cred == c])) if (cred == c).any() else float("nan")
                                       for c in range(4)],
        "formal_share_by_quintile": _by_quintile(formal.astype(float), decile),
        "mean_pay": float(np.nanmean(pay)),
        "pay_by_quintile": _by_quintile(pay, decile),
        "pay_by_credential": [float(np.nanmean(pay[cred == c])) if (cred == c).any() else float("nan")
                              for c in range(4)],
        "pay_gini": _gini(pay),
        "queue_share": float(np.nanmean((queue > 0).astype(float))),
        "queue_share_by_quintile": _by_quintile((queue > 0).astype(float), decile),
    }
    # credential shares by income quintile (five groups)
    out["credential_shares_by_quintile"] = [
        [float(np.mean(cred[(decile >= lo) & (decile <= hi)] == c)) for c in range(4)] for lo, hi in QUINTILES]
    return out
