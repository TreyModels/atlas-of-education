#!/usr/bin/env python3
"""B. ALTERNATIVES FORECLOSURE: pipeline coverage x non-credentialed livelihoods.

Pre-registered: 10-year-change panel; outcome = change in TFR; regressors = coverage,
coverage x farm share, farm share, log income, urbanisation; country and period fixed
effects, clustered by country. Predicted sign on coverage x farm = POSITIVE (the negative
coverage-fertility association is attenuated where farming livelihoods survive).
Rivals: coverage x log income, coverage x urbanisation. Gradient: bottom vs top third of
farm employment. Random-split null: 400 random splits of the same sizes.
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
    VAL[v] = {(r.iso, r.year): getattr(r, v) for r in df.itertuples()}



R = []


def val(v, iso, y):
    return _num(VAL[v].get((iso, y)))


starts = list(range(1960, 2011, 10))
rows = []
for i in sorted({r.iso for r in df.itertuples()}):
    for s in starts:
        t0, t1 = TFR.get((i, s)), TFR.get((i, s + 10))
        cov, farm, urb = val("sec", i, s), val("emp_agri", i, s), val("urban", i, s)
        lg, cov3 = val("gdppc_log", i, s), val("ter", i, s)
        if any(not np.isfinite(x) for x in (t0, t1, cov, farm, urb, lg, cov3)):
            continue
        rows.append(dict(iso=i, period=s, dtfr=t1 - t0, tfr0=t0, tfr1=t1,
                         pipe=cov / 100, farm=farm / 100, urb=urb / 100, lgdp=lg, pipe3=cov3 / 100))
W = pd.DataFrame(rows)
W.to_csv(os.path.join(OUT, "B_windows.csv"), index=False)
R.append(f"B sample: {len(W)} country-decade windows, {W.iso.nunique()} countries, "
         f"{W.period.nunique()} decades ({', '.join(str(p) for p in sorted(W.period.unique()))})")


def fe_reg(Z, regs, cluster="iso"):
    X = Z[regs].copy()
    Xd = pd.get_dummies(Z[["iso", "period"]].astype(str), drop_first=True, dtype=float)
    X = pd.concat([X.reset_index(drop=True), Xd.reset_index(drop=True)], axis=1)
    m = sm.OLS(Z.dtfr.values, sm.add_constant(X)).fit(cov_type="cluster",
                                                      cov_kwds={"groups": Z[cluster].values})
    return m


Z = W.copy()
Z["covXfarm"] = Z["pipe"] * Z["farm"]
Z["covXlgdp"] = Z["pipe"] * Z["lgdp"]
Z["covXurb"] = Z["pipe"] * Z["urb"]
base = ["pipe", "covXfarm", "farm", "lgdp", "urb"]
m = fe_reg(Z, base)
b_int, se_int = float(m.params["covXfarm"]), float(m.bse["covXfarm"])
b_cov, se_cov = float(m.params["pipe"]), float(m.bse["pipe"])
R.append(f"PRIMARY (secondary completion x farm employment, country+decade FE, clustered): "
         f"coverage effect at farm=0 {b_cov:+.2f} (SE {se_cov:.2f}); interaction {b_int:+.2f} "
         f"(SE {se_int:.2f}, 95% CI {b_int-1.96*se_int:+.2f} to {b_int+1.96*se_int:+.2f}), "
         f"n={int(m.nobs)}")
R.append(f"  pre-registered sign is POSITIVE; observed {'matches' if b_int > 0 else 'does NOT match'} "
         f"(t = {b_int/se_int:+.2f})")
# marginal effect of coverage at low vs high farm (10th/90th percentile)
f10, f90 = np.nanpercentile(Z.farm, 10), np.nanpercentile(Z.farm, 90)
R.append(f"  implied coverage effect at farm 10th pct ({f10:.2f}): {b_cov + b_int*f10:+.2f}; "
         f"at 90th pct ({f90:.2f}): {b_cov + b_int*f90:+.2f}")

# rivals: add coverage x income and coverage x urbanisation
m2 = fe_reg(Z, base + ["covXlgdp", "covXurb"])
R.append(f"RIVALS (add coverage x log income and coverage x urbanisation): interaction "
         f"{float(m2.params['covXfarm']):+.2f} (SE {float(m2.bse['covXfarm']):.2f}); "
         f"coverage x income {float(m2.params['covXlgdp']):+.2f} (SE {float(m2.bse['covXlgdp']):.2f}); "
         f"coverage x urban {float(m2.params['covXurb']):+.2f} (SE {float(m2.bse['covXurb']):.2f})")

# robustness: tertiary coverage
Z["covT_farm"] = Z["pipe3"] * Z["farm"]
m3 = fe_reg(Z, ["pipe3", "covT_farm", "farm", "lgdp", "urb"])
R.append(f"ROBUSTNESS tertiary coverage: interaction {float(m3.params['covT_farm']):+.2f} "
         f"(SE {float(m3.bse['covT_farm']):.2f})")
# robustness: urbanisation as the foreclosure measure (sign should be NEGATIVE if story holds)
m4 = fe_reg(Z, ["pipe", "covXurb", "urb", "farm", "lgdp"])
R.append(f"ROBUSTNESS urbanisation as foreclosure measure: coverage x urban "
         f"{float(m4.params['covXurb']):+.2f} (SE {float(m4.bse['covXurb']):.2f}) — story predicts negative")

# ---- gradient: bottom vs top third of farm employment at first window ----
first_w = W.sort_values("period").groupby("iso").first().reset_index()
q1, q2 = np.nanpercentile(first_w.farm, [33.3, 66.7])
low_iso = set(first_w[first_w.farm <= q1].iso)
high_iso = set(first_w[first_w.farm >= q2].iso)
R.append(f"GRADIENT: foreclosure terciles from each country's first window: low-farm n={len(low_iso)}, "
         f"high-farm n={len(high_iso)} (cut points {q1:.2f}, {q2:.2f})")
Z["high"] = Z.iso.isin(high_iso).astype(float)
Z["covXhigh"] = Z["pipe"] * Z["high"]
m5 = fe_reg(Z, ["pipe", "covXhigh", "covXfarm", "farm", "lgdp", "urb"])
b_gr = float(m5.params["covXhigh"]); se_gr = float(m5.bse["covXhigh"])
R.append(f"  coverage effect in high-farm minus low-farm tercile: {b_gr:+.2f} (SE {se_gr:.2f}); "
         f"story predicts positive (weaker effect where farm survives)")


# ---- random-split null, reusing the grouping-multiverse logic ----
def gradient_coef(labels):
    Zz = Z.copy()
    Zz["high"] = Zz.iso.map(labels).astype(float)
    Zz["covXhigh"] = Zz["pipe"] * Zz["high"]
    try:
        mm = fe_reg(Zz, ["pipe", "covXhigh", "covXfarm", "farm", "lgdp", "urb"])
        return float(mm.params["covXhigh"])
    except Exception:
        return np.nan


countries = sorted(Z.iso.unique())
n_high = len(high_iso)
rng = np.random.default_rng(2026)
null = []
for _ in range(400):
    hi = set(rng.choice(countries, size=n_high, replace=False))
    labs = {c: (1 if c in hi else 0) for c in countries}
    null.append(gradient_coef(labs))
null = np.array([x for x in null if np.isfinite(x)])
pct = float((null < b_gr).mean())
p_emp = float((1 + (null >= b_gr).sum()) / (1 + len(null)))
R.append(f"  RANDOM-SPLIT NULL (400 random splits of the same sized high group): real gradient {b_gr:+.2f} "
         f"is at the {pct:.1%} percentile of the null (null mean {null.mean():+.2f}, sd {null.std():.2f}); "
         f"one-sided empirical p = {p_emp:.3f}")

# ---- levels robustness: TFR end on coverage x farm ----
Z["tfr1"] = Z.tfr1
m6 = fe_reg(Z, ["pipe", "covXfarm", "farm", "lgdp", "urb"])
R.append(f"LEVELS-ROBUSTNESS (TFR at window end): interaction {float(m6.params['covXfarm']):+.2f} "
         f"(SE {float(m6.bse['covXfarm']):.2f})")

out = dict(lines=R, primary=dict(b_cov=b_cov, se_cov=se_cov, b_int=b_int, se_int=se_int, n=int(m.nobs)),
           rivals=dict(b_int=float(m2.params["covXfarm"]), se_int=float(m2.bse["covXfarm"])),
           gradient=dict(b=b_gr, se=se_gr, pct=pct, p_emp=p_emp, null_mean=float(null.mean()),
                         null_sd=float(null.std())))
json.dump(out, open(os.path.join(OUT, "B_results.json"), "w"), indent=1, default=float)
open(os.path.join(OUT, "B_results.txt"), "w").write("\n".join(R) + "\n")
print("\n".join(R))
