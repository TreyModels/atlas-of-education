#!/usr/bin/env python3
"""B2. Foreclosure interaction, expanded-sample robustness.

Same pre-registered model as analysis_b.py but: windows start 1970..2010, and the sample
only requires the core variables (TFR at both ends, coverage, farm share); the controls are
included where available. Coverage and farm share are expressed in 10-percentage-point /
10-share units so the coefficients are readable. Reported as a robustness/power check.
"""
import json, os, sys
import numpy as np
import pandas as pd
import statsmodels.api as sm
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import pf_common as pc

OUT = pc.OUT; os.makedirs(OUT, exist_ok=True)


def _num(x):
    try:
        return float(x)
    except Exception:
        return np.nan


df = pc.panel()
TFR = {(r.iso, r.year): _num(r.fertility) for r in df.itertuples()}
VAL = {}
for v in ("sec", "ter", "emp_agri", "urban", "gdppc_log"):
    VAL[v] = {(r.iso, r.year): _num(getattr(r, v)) for r in df.itertuples()}
R = []

starts = list(range(1970, 2011, 10))
rows = []
for i in sorted({r.iso for r in df.itertuples()}):
    for s in starts:
        t0, t1 = TFR.get((i, s), np.nan), TFR.get((i, s + 10), np.nan)
        cov, farm = VAL["sec"].get((i, s), np.nan), VAL["emp_agri"].get((i, s), np.nan)
        if not all(np.isfinite(x) for x in (t0, t1, cov, farm)):
            continue
        rows.append(dict(iso=i, period=s, dtfr=t1 - t0, tfr1=t1,
                         cov=cov, farm=farm, urb=VAL["urban"].get((i, s), np.nan),
                         lgdp=VAL["gdppc_log"].get((i, s), np.nan)))
W = pd.DataFrame(rows)
R.append(f"B2 expanded sample: {len(W)} country-decade windows, {W.iso.nunique()} countries, "
         f"decades {sorted(W.period.unique())}")


def fe_reg(Z, regs):
    Z = Z.dropna(subset=regs + ["dtfr"])
    X = Z[regs].copy()
    Xd = pd.get_dummies(Z[["iso", "period"]].astype(str), drop_first=True, dtype=float)
    X = pd.concat([X.reset_index(drop=True), Xd.reset_index(drop=True)], axis=1)
    m = sm.OLS(Z.dtfr.values, sm.add_constant(X)).fit(cov_type="cluster",
                                                      cov_kwds={"groups": Z.iso.values})
    return m, len(Z)


Z = W.copy()
Z["cov10"] = Z["cov"] / 10.0      # one unit = 10 percentage points
Z["farm10"] = Z.farm / 10.0    # one unit = 10 share points
Z["covXfarm"] = Z["cov10"] * Z["farm10"]
Z["covXlgdp"] = Z["cov10"] * Z["lgdp"]
Z["covXurb"] = Z["cov10"] * Z["urb"]
core = ["cov10", "covXfarm", "farm10"]
m, n = fe_reg(Z, core)
bi, sei = float(m.params["covXfarm"]), float(m.bse["covXfarm"])
R.append(f"B2 PRIMARY (core, no controls): coverage/10pp {float(m.params['cov10']):+.2f} "
         f"(SE {float(m.bse['cov10']):.2f}); interaction per 10pp coverage x 10pp farm "
         f"{bi:+.2f} (SE {sei:.2f}, 95% CI {bi-1.96*sei:+.2f} to {bi+1.96*sei:+.2f}), n={n}")
m2, n2 = fe_reg(Z, core + ["lgdp", "urb"])
R.append(f"B2 with income+urban controls: interaction {float(m2.params['covXfarm']):+.2f} "
         f"(SE {float(m2.bse['covXfarm']):.2f}), n={n2}")
m3, n3 = fe_reg(Z, core + ["lgdp", "urb", "covXlgdp", "covXurb"])
R.append(f"B2 RIVALS (coverage x income, coverage x urban added): farm interaction "
         f"{float(m3.params['covXfarm']):+.2f} (SE {float(m3.bse['covXfarm']):.2f}); "
         f"x income {float(m3.params['covXlgdp']):+.2f} (SE {float(m3.bse['covXlgdp']):.2f}); "
         f"x urban {float(m3.params['covXurb']):+.2f} (SE {float(m3.bse['covXurb']):.2f}), n={n3}")

# gradient + random-split null
first_w = W.sort_values("period").groupby("iso").first().reset_index()
q1, q2 = np.nanpercentile(first_w.farm, [33.3, 66.7])
high_iso = set(first_w[first_w.farm >= q2].iso)
Z["high"] = Z.iso.isin(high_iso).astype(float)
Z["covXhigh"] = Z["cov10"] * Z["high"]
m4, n4 = fe_reg(Z, core + ["high", "covXhigh"])
bg, seg = float(m4.params["covXhigh"]), float(m4.bse["covXhigh"])
R.append(f"B2 GRADIENT: coverage effect high-farm minus low-farm third: {bg:+.2f} (SE {seg:.2f}), "
         f"n={n4}; story predicts positive")
countries = sorted(Z.iso.unique()); n_high = len(high_iso)
rng = np.random.default_rng(2026)
null = []
for _ in range(400):
    hi = set(rng.choice(countries, size=n_high, replace=False))
    Zz = Z.copy(); Zz["high"] = Zz.iso.isin(hi).astype(float)
    Zz["covXhigh"] = Zz["cov10"] * Zz["high"]
    try:
        mm, _ = fe_reg(Zz, core + ["high", "covXhigh"])
        null.append(float(mm.params["covXhigh"]))
    except Exception:
        pass
null = np.array(null)
pct = float((null < bg).mean())
R.append(f"B2 random-split null (400 splits): real gradient at {pct:.1%} percentile, "
         f"null mean {null.mean():+.2f} (sd {null.std():.2f})")
json.dump(dict(lines=R), open(os.path.join(OUT, "B2_results.json"), "w"), indent=1, default=float)
open(os.path.join(OUT, "B2_results.txt"), "w").write("\n".join(R) + "\n")
print("\n".join(R))
