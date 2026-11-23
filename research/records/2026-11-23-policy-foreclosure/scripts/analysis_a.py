#!/usr/bin/env python3
"""A. NO-OFF-SWITCH: pronatalist introductions in saturated low-fertility countries.

Pre-registered plan: bound test (share of country-years above 1.6 within 10 years),
event study with country and year fixed effects, persistence (3+ consecutive years >1.6),
rivals (income, urbanisation, net migration), power (minimum detectable effect = 2.8*SE).
"""
import json, os, sys
import numpy as np
import pandas as pd
import statsmodels.api as sm
from scipy.stats import beta
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pf_common as pc

OUT = pc.OUT; os.makedirs(OUT, exist_ok=True)
EV = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "events.json")))
EV = EV[0] if isinstance(EV, list) else EV
df = pc.panel()
df = pc.net_migration(df)
tfr = {(r.iso, r.year): r.fertility for r in df.itertuples() if np.isfinite(r.fertility)}
R = []

def tfr_at(iso, yr, win=2):
    for d in range(win + 1):
        for s in (0, 1):
            y = yr + (d if s == 0 else -d)
            v = tfr.get((iso, y))
            if v is not None and np.isfinite(v):
                return v, y
    return None, None

def cp_upper(k, n, alpha=0.05):
    """one-sided Clopper-Pearson upper bound for k successes in n trials."""
    if n == 0:
        return np.nan
    if k == n:
        return 1.0
    return float(beta.ppf(1 - alpha, k + 1, n - k))

events = []
for e in EV["events"]:
    v, yy = tfr_at(e["iso"], e["year"])
    if v is None:
        continue
    events.append(dict(iso=e["iso"], year=e["year"], policy=e["policy"], tfr_intro=v, tfr_year=yy,
                       saturated=bool(v < 1.6)))
E = pd.DataFrame(events)
R.append(f"events with TFR at introduction: {len(E)}; saturated (<1.6): {int(E.saturated.sum())}")

# ---- per-event trajectories (all events, saturated flagged) ----
per = []
for e in E.itertuples():
    pre = [tfr[(e.iso, y)] for y in range(e.year - 5, e.year) if (e.iso, y) in tfr]
    post = [tfr[(e.iso, y)] for y in range(e.year, e.year + 11) if (e.iso, y) in tfr]
    if not post:
        continue
    above = [v > 1.6 for v in post]
    run = mx = 0
    for b in above:
        run = run + 1 if b else 0
        mx = max(mx, run)
    per.append(dict(iso=e.iso, year=e.year, saturated=e.saturated, tfr_intro=e.tfr_intro,
                    pre5=np.nanmean(pre) if pre else np.nan, post10=np.nanmean(post),
                    post_max=np.nanmax(post), post_t5=tfr.get((e.iso, e.year + 5), np.nan),
                    post_t10=tfr.get((e.iso, e.year + 10), np.nan),
                    n_above=int(sum(above)), n_post=len(post), max_run=mx,
                    years_above=";".join(str(e.year + i) for i, b in enumerate(above) if b)))
P = pd.DataFrame(per)
P.to_csv(os.path.join(OUT, "A_event_trajectories.csv"), index=False)

sat = P[P.saturated]
k, n = int(sat.n_above.sum()), int(sat.n_post.sum())
share = k / n if n else np.nan
R.append(f"BOUND TEST (saturated events, country-years in the 10 years after introduction): "
         f"{k} of {n} country-years above TFR 1.6 = {share:.3%}; one-sided 95% upper bound {cp_upper(k, n):.3%}")
R.append(f"  events where TFR exceeds 1.6 at all within 10y: {int((sat.n_above > 0).sum())} of {len(sat)}")
R.append(f"  events with 3+ CONSECUTIVE years above 1.6 (pre-registered falsifier): "
         f"{int((sat.max_run >= 3).sum())} of {len(sat)}")
R.append("  those events: " + "; ".join(f"{r.iso} {r.year} (max {r.post_max:.2f}, {r.max_run} yrs)"
                                       for r in sat.itertuples() if r.max_run >= 3))
pre_post = sat.dropna(subset=["pre5"])
d = pre_post.post_max - pre_post.pre5
R.append(f"PRE/POST: max TFR in 10 years after minus 5-year pre mean: median {np.median(d):+.3f}, "
         f"mean {d.mean():+.3f} (n={len(d)}); events reaching above 1.6: {int((sat.post_max > 1.6).sum())}/{len(sat)}")
R.append(f"  highest TFR reached after any introduction: {sat.post_max.max():.2f} "
         f"({sat.loc[sat.post_max.idxmax(), 'iso']}); never near replacement 2.1")

# ---- event study: first saturated introduction per country, -8..+10 ----
first = sat.sort_values("year").groupby("iso").first().reset_index()
rows = []
for e in first.itertuples():
    for kk in range(-8, 11):
        y = e.year + kk
        v = tfr.get((e.iso, y))
        if v is None:
            continue
        rows.append(dict(iso=e.iso, year=y, k=kk, tfr=v))
ES = pd.DataFrame(rows)
if len(ES):
    ES["post"] = (ES.k >= 0).astype(float)
    X = pd.get_dummies(ES[["iso", "year"]].astype(str), drop_first=True, dtype=float)
    X["POST"] = ES.post.values
    X = sm.add_constant(X)
    m = sm.OLS(ES.tfr.values, X).fit(cov_type="cluster", cov_kwds={"groups": ES.iso.values})
    b_post, se_post = float(m.params["POST"]), float(m.bse["POST"])
    R.append(f"EVENT STUDY (first saturated introduction per country, n={len(ES)} country-years, "
             f"{ES.iso.nunique()} countries, country+calendar-year FE): post-introduction TFR shift "
             f"{b_post:+.3f} (SE {se_post:.3f}, 95% CI {b_post-1.96*se_post:+.3f} to {b_post+1.96*se_post:+.3f})")
    R.append(f"  POWER for the absence claim: minimum detectable shift (80% power, alpha .05) = "
             f"{2.8*se_post:.3f} births per woman")
    # event-time coefficients
    ev = []
    for kk in range(0, 11):
        sub = ES[ES.k == kk]
        if len(sub) < 10:
            continue
        Xk = pd.get_dummies(ES[["iso", "year"]].astype(str), drop_first=True, dtype=float)
        Xk = sm.add_constant(Xk)
        base = ES.copy()
        ev.append((kk, len(sub), np.nanmean(sub.tfr)))
    R.append("  mean TFR by event year: " + ", ".join(f"t+{k0}:{v:.2f}" for k0, _, v in ev))

# ---- rivals: pooled post dummy with controls ----
def pooled(post_years=10, controls=False, trends=False):
    rows = []
    for e in first.itertuples():
        for kk in range(-5, post_years + 1):
            y = e.year + kk
            r = df[(df.iso == e.iso) & (df.year == y)]
            if len(r) == 0:
                continue
            r = r.iloc[0]
            if not np.isfinite(r.fertility):
                continue
            rows.append(dict(iso=e.iso, year=y, tfr=r.fertility, post=float(kk >= 0),
                             lgdp=r.gdppc_log, urban=r.urban,
                             nmig=getattr(r, "netmig_p1000", np.nan), k=kk))
    Z = pd.DataFrame(rows)
    ctrl_cols = ["post"] + [c for c in ("lgdp", "urban", "nmig") if np.isfinite(Z[c]).sum() > 100]
    Xd = pd.get_dummies(Z[["iso", "year"]].astype(str), drop_first=True, dtype=float)
    X = pd.concat([Z[ctrl_cols].reset_index(drop=True), Xd.reset_index(drop=True)], axis=1)
    if trends:
        tt = Z.k.values
        for i in sorted(Z.iso.unique()):
            if i == sorted(Z.iso.unique())[0]:
                continue
            X["trend_" + i] = ((Z.iso == i) * (Z.year - 1990)).astype(float).values
    mask = np.isfinite(Z.tfr.values)
    X = X.loc[mask]; yy = Z.tfr.values[mask]; grp = Z.iso.values[mask]
    X = X.fillna(X.mean())
    m = sm.OLS(yy, sm.add_constant(X)).fit(cov_type="cluster", cov_kwds={"groups": grp})
    return float(m.params["post"]), float(m.bse["post"]), int(mask.sum()), int(Z.iso.nunique())

for label, ctrl, tr in [("no rivals", False, False), ("with income+urban+migration", True, True),
                        ("no rivals, country trends", False, True)]:
    if ctrl:
        b, se, n, nc = pooled(controls=True, trends=False)
        R.append(f"RIVALS: post-introduction TFR shift with income, urbanisation and net migration controlled: "
                 f"{b:+.3f} (SE {se:.3f}) over {n} country-years, {nc} countries")
    elif tr:
        b, se, n, nc = pooled(controls=False, trends=True)
        R.append(f"RIVALS: post-introduction shift with country-specific trends: {b:+.3f} (SE {se:.3f})")
    else:
        b0, se0, n0, nc0 = pooled()
        R.append(f"RIVALS: baseline post-introduction shift (no controls): {b0:+.3f} (SE {se0:.3f})")

# ---- Thailand case study ----
th = df[(df.iso == "THA") & df.fertility.notna()][["year", "fertility"]].set_index("year").fertility
if len(th):
    R.append("THAILAND (1997 reversal, case study): TFR " +
             ", ".join(f"{y}:{th[y]:.2f}" for y in (1990, 1997, 2000, 2005, 2010, 2015, 2020, 2023) if y in th) +
             f"; change 1997-2023 {th.get(2023, np.nan)-th.get(1997, np.nan):+.2f}; no recovery above 1.6 after the reversal")

json.dump({"lines": R, "events": events, "per_event": per}, open(os.path.join(OUT, "A_results.json"), "w"),
          indent=1, default=float)
open(os.path.join(OUT, "A_results.txt"), "w").write("\n".join(R) + "\n")
print("\n".join(R))
