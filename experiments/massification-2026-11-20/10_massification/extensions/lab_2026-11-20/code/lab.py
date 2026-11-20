"""Lab battery 2026-11-20: 10 predeclared descriptive experiments on secondary/post-secondary
massification across geographic scale and economic structure. Deterministic; data read-only.
Labels: OBSERVED/DERIVED carried from source status. No causal claims."""
import json, hashlib, sys
from pathlib import Path
import numpy as np
import pandas as pd

PKG = Path(__file__).resolve().parents[4]
OUT = PKG / "10_massification/extensions/lab_2026-11-20"
RES = OUT / "results"
D = PKG / "10_massification/data"
R = PKG / "09_relations/data"

def num(s): return pd.to_numeric(s, errors="coerce")

def load():
    uni = pd.read_csv(D/"UNIVERSALIZATION_SERIES.csv")
    uni["value"] = num(uni["value"]); uni["year"] = num(uni["year"])
    tim = pd.read_csv(D/"UNIVERSALIZATION_TIMING.csv")
    base = pd.read_csv(D/"BASELINE_SERIES.csv"); base["value"] = num(base["value"])
    cap = pd.read_csv(D/"STATE_CAPACITY.csv"); cap["value"] = num(cap["value"])
    sch = pd.read_csv(D/"SCHOOL_EXPANSION.csv"); sch["value"] = num(sch["value"])
    wdi = pd.read_csv(R/"panel_wdi_wide.csv")
    eci = pd.read_csv(R/"economic_complexity_panel_30ctys.csv")
    return dict(uni=uni, tim=tim, base=base, cap=cap, sch=sch, wdi=wdi, eci=eci)

def ols(y, X, cluster=None):
    """OLS with optional cluster-robust SE. X includes constant column."""
    y = np.asarray(y, float); X = np.asarray(X, float)
    keep = np.isfinite(y) & np.isfinite(X).all(axis=1)
    y, X = y[keep], X[keep]
    n, k = X.shape
    if n <= k: return dict(beta=None, se=None, n=n, k=k, r2=np.nan, cl=0)
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    resid = y - X @ beta
    XtX_inv = np.linalg.pinv(X.T @ X)
    if cluster is not None:
        cl = np.asarray(cluster)[keep]
        meat = np.zeros((k, k))
        for g in pd.unique(cl):
            m = cl == g
            Xg, rg = X[m], resid[m]
            s = Xg.T @ rg
            meat += np.outer(s, s)
        # small-sample correction G/(G-1)
        G = len(pd.unique(cl))
        corr = G/(G-1) if G > 1 else 1.0
        V = corr * (XtX_inv @ meat @ XtX_inv)
        ncl = G
    else:
        sigma2 = float(resid @ resid) / max(n-k, 1)
        V = sigma2 * XtX_inv
        ncl = 0
    se = np.sqrt(np.clip(np.diag(V), 0, None))
    ss_tot = float(((y - y.mean())**2).sum())
    r2 = 1 - float(resid @ resid)/ss_tot if ss_tot > 0 else np.nan
    return dict(beta=beta, se=se, n=int(n), k=int(k), r2=r2, cl=ncl)

def within(df, cols, gcol="iso3"):
    out = df.copy()
    for c in cols:
        out[c] = out[c] - out.groupby(gcol)[c].transform("mean")
    return out

def between(df, cols, gcol="iso3"):
    g = df.groupby(gcol)[cols].mean().reset_index()
    return g

def fmt(b, se, i=0):
    if b is None: return "NA"
    ci = 1.96*se[i]
    return f"{b[i]:+.4f} (se {se[i]:.4f}, ci [{b[i]-ci:+.4f},{b[i]+ci:+.4f}])"

res_rows = []

def record(exp, estimand, beta, se, n, cl, threshold, verdict, extra=""):
    res_rows.append(dict(experiment=exp, estimand=estimand, estimate=beta, se=se, n=n, clusters=cl,
                         threshold=threshold, verdict=verdict, note=extra))

# ---------------- E1: 6-country income/urban/services gradient, upper-secondary GER ----------------
def e1(data):
    w = data["wdi"]; six = ["PHL","KHM","HKG","CHN","KOR","JPN"]
    d = w[w.iso3.isin(six) & w.year.between(1995,2024)].copy()
    d["y"] = num(d["SE.SEC.ENRR.UP"]); d["lgdp"] = np.log(num(d["NY.GDP.PCAP.PP.CD"]).clip(lower=1))
    d["urb"] = num(d["SP.URB.TOTL.IN.ZS"]); d["srv"] = num(d["SL.SRV.EMPL.ZS"])
    d = d.dropna(subset=["y","lgdp","urb","srv"])
    d["one"] = 1.0
    # within
    dw = within(d, ["y","lgdp","urb","srv"])
    rw = ols(dw["y"], dw[["one","lgdp","urb","srv"]], cluster=dw["iso3"])
    # between
    db = between(d, ["y","lgdp","urb","srv"]); db["one"] = 1.0
    rb = ols(db["y"], db[["one","lgdp","urb","srv"]], cluster=None)
    verdict = "no association (both CIs include 0)"
    if rw["beta"] is not None and abs(rw["beta"][1]) > 1.96*rw["se"][1]:
        verdict = "within association"
        if rw["beta"][1] >= 3 and abs(rw["beta"][1]) > 1.96*rw["se"][1]: verdict = "strong (>=3 pp per log point)"
    pd.DataFrame([dict(spec="within", coef_lgdp=rw["beta"][1], se=rw["se"][1], ci_lo=rw["beta"][1]-1.96*rw["se"][1], ci_hi=rw["beta"][1]+1.96*rw["se"][1], n=rw["n"], clusters=rw["cl"], r2=rw["r2"]),
                  dict(spec="between", coef_lgdp=rb["beta"][1], se=rb["se"][1], ci_lo=rb["beta"][1]-1.96*rb["se"][1], ci_hi=rb["beta"][1]+1.96*rb["se"][1], n=rb["n"], clusters=rb["cl"], r2=rb["r2"])]).to_csv(RES/"E1_income_gradient.csv", index=False)
    record("E1", "within slope upper-sec GER on log GDP", rw["beta"][1], rw["se"][1], rw["n"], rw["cl"], "CI excl 0 in within & between; strong if >=3", verdict)
    # robustness (post-hoc, clearly labelled; primary threshold unchanged)
    rob = []
    for name, sub, dep in [("all6_upper", d, "y"), ("drop_CHN", d[d.iso3!="CHN"], "y"), ("drop_HKG", d[d.iso3!="HKG"], "y"),
                           ("all6_total_secondary", d.assign(y=num(d["SE.SEC.ENRR"])), "y")]:
        sub = sub.dropna(subset=[dep,"lgdp","urb","srv"]).copy(); sub["one"]=1.0
        sw = within(sub, [dep,"lgdp","urb","srv"])
        rr = ols(sw[dep], sw[["one","lgdp","urb","srv"]], cluster=sw["iso3"])
        if rr["beta"] is not None:
            rob.append(dict(spec=name, coef=rr["beta"][1], se=rr["se"][1], n=rr["n"], clusters=rr["cl"]))
    if rob: pd.DataFrame(rob).to_csv(RES/"E1_robustness.csv", index=False)
    return dict(rw=rw, rb=rb)

# ---------------- E2: structure at crossings ----------------
def e2(data):
    tim = data["tim"]; w = data["wdi"]
    t = tim.copy(); t["cy"] = num(t["crossing_year"]); t = t[t["cy"].notna()]
    rows = []
    for (lvl, thr), g in t.groupby(["level","threshold_pct"]):
        g = g.drop_duplicates("iso3")
        if g.iso3.nunique() < 3: continue
        vals = []
        for _, r in g.iterrows():
            ww = w[(w.iso3==r.iso3) & (w.year==int(r.cy))]
            if len(ww)==0:
                ww = w[(w.iso3==r.iso3) & (w.year.between(int(r.cy)-1, int(r.cy)+1))].head(1)
            if len(ww)==0: continue
            vals.append(dict(iso3=r.iso3, gdp=num(ww["NY.GDP.PCAP.PP.CD"]).iloc[0],
                             urb=num(ww["SP.URB.TOTL.IN.ZS"]).iloc[0], agri=num(ww["SL.AGR.EMPL.ZS"]).iloc[0]))
        v = pd.DataFrame(vals).dropna(subset=["gdp"])
        if len(v) < 3: continue
        lo, hi = v.gdp.quantile(.25), v.gdp.quantile(.75)
        inside = int(((v.gdp>=lo)&(v.gdp<=hi)).sum())
        frac = inside/len(v)
        typical = "structure-typical" if frac >= 4/6 else "not typical"
        rows.append(dict(level=lvl, threshold=thr, n_countries=len(v), inside_iqr=inside, frac=frac,
                         gdp_med=float(v.gdp.median()), gdp_iqr=float(hi-lo),
                         urb_med=float(v.urb.median()) if v.urb.notna().any() else np.nan,
                         agri_med=float(v.agri.median()) if v.agri.notna().any() else np.nan, verdict=typical))
        record("E2", f"crossings inside GDP IQR ({lvl} {thr})", float(frac), np.nan, len(v), len(v), "frac>=4/6", typical)
    df = pd.DataFrame(rows)
    if not df.empty: df.to_csv(RES/"E2_crossing_structure.csv", index=False)
    return df

# ---------------- E3: PHL regional equalization ----------------
def e3(data):
    b = data["base"]
    b = b[b.region.notna() & (b.region!="national") & b.indicator.isin(["education_gini","mean_years_of_schooling"])].copy()
    p = b.pivot_table(index=["region","period"], columns="indicator", values="value", aggfunc="mean").reset_index()
    rows, slopes = [], {}
    for per, g in p.groupby("period"):
        g = g.dropna(subset=["education_gini","mean_years_of_schooling"])
        if len(g) < 5: continue
        X = np.column_stack([np.ones(len(g)), g["mean_years_of_schooling"].values])
        r = ols(g["education_gini"].values, X)
        slopes[str(per)] = dict(slope=r["beta"][1], se=r["se"][1], n=r["n"])
        for _, row in g.iterrows():
            rows.append(dict(region=row.region, period=per, gini=row.education_gini, mys=row.mean_years_of_schooling))
    df = pd.DataFrame(rows)
    df.to_csv(RES/"E3_regional_equalization.csv", index=False)
    periods = sorted(slopes)
    delta = slopes[periods[-1]]["slope"] - slopes[periods[0]]["slope"] if len(periods) >= 2 else np.nan
    # count regions with gini drop >= 0.02
    drops = 0
    if len(periods) >= 2:
        piv = df.pivot_table(index="region", columns="period", values="gini")
        if periods[0] in piv and periods[-1] in piv:
            drops = int((piv[periods[-1]] <= piv[periods[0]] - 0.02).sum())
    for pname, s in slopes.items():
        record("E3", f"Gini~MYS slope ({pname})", s["slope"], s["se"], s["n"], 0, "negative slop & >=10/17 regions improve", "equalizing" if (drops>=10 and all(s["slope"]<0 for s in slopes.values())) else "not established", f"regions improved={drops}")
    return dict(slopes=slopes, delta=delta, drops=drops)

# ---------------- E4: city-state vs large-country shape ----------------
def e4(data):
    tim = data["tim"]; w = data["wdi"]
    t = tim.copy(); t["cy"] = num(t["crossing_year"]); t = t[t["cy"].notna()]
    def cross(iso, level, thr):
        x = t[(t.iso3==iso) & (t.level==str(level)) & (num(t.threshold_pct)==thr) & t.cy.notna()]
        return float(x.cy.iloc[0]) if len(x) else np.nan
    rows = []
    for iso in ["HKG","CHN","PHL","KHM"]:
        lo = cross(iso,"lower secondary",90); te = cross(iso,"tertiary",50)
        ww = w[(w.iso3==iso) & w.year.between(1995,2024)].sort_values("year")
        g = num(ww["SE.SEC.ENRR"]).diff().dropna()
        vol = float(g.std()) if len(g) >= 5 else np.nan
        rows.append(dict(iso3=iso, lower_cross=lo, tertiary_cross=te,
                         duration=(te-lo) if np.isfinite(lo) and np.isfinite(te) else np.nan, volatility=vol))
    df = pd.DataFrame(rows); df.to_csv(RES/"E4_scale_shape.csv", index=False)
    hk = df[df.iso3=="HKG"]; large = df[df.iso3!="HKG"]
    d_ratio = large.duration.median()/hk.duration.iloc[0] if np.isfinite(hk.duration.iloc[0]) and hk.duration.iloc[0] else np.nan
    v_ratio = large.volatility.median()/hk.volatility.iloc[0] if np.isfinite(hk.volatility.iloc[0]) and hk.volatility.iloc[0] else np.nan
    verdict_d = ("city-state faster" if np.isfinite(d_ratio) and d_ratio >= 1.5 else
                 ("no clear difference" if np.isfinite(d_ratio) else "insufficient dated crossings"))
    verdict_v = ("city-state smoother" if np.isfinite(v_ratio) and v_ratio >= 2 else
                 ("large countries smoother" if np.isfinite(v_ratio) and v_ratio <= 0.5 else
                  ("no clear difference" if np.isfinite(v_ratio) else "insufficient")))
    record("E4", "duration ratio large/HKG", float(d_ratio) if np.isfinite(d_ratio) else np.nan, np.nan, len(df), 1, ">=1.5 city-state faster", verdict_d)
    record("E4", "volatility ratio large/HKG", float(v_ratio) if np.isfinite(v_ratio) else np.nan, np.nan, len(df), 1, ">=2 city-state smoother; <=0.5 large smoother", verdict_v)
    return df

# ---------------- E5: structure and tertiary expansion (30 countries) ----------------
def e5(data):
    w = data["wdi"]; eci = data["eci"]
    d = w.merge(eci[["iso3","year","eci_hs92","eci_sitc"]], on=["iso3","year"], how="left")
    d = d[d.year.between(1995,2024)].copy()
    d["y"] = num(d["SE.TER.ENRR"]); d["lgdp"] = np.log(num(d["NY.GDP.PCAP.PP.CD"]).clip(lower=1))
    d["urb"] = num(d["SP.URB.TOTL.IN.ZS"]); d["srv"] = num(d["SL.SRV.EMPL.ZS"]); d["eci"] = num(d["eci_hs92"])
    d = d.dropna(subset=["y","lgdp","urb","srv"])
    d["one"] = 1.0
    dw = within(d, ["y","lgdp","urb","srv"]); dw["eci"] = d["eci"].fillna(0)
    rw = ols(dw["y"], dw[["one","lgdp","urb","srv","eci"]], cluster=dw["iso3"])
    db = between(d, ["y","lgdp","urb","srv"]); db["eci"] = d.groupby("iso3")["eci"].mean().fillna(0).values; db["one"] = 1.0
    rb = ols(db["y"], db[["one","lgdp","urb","srv","eci"]], cluster=None)
    pd.DataFrame([dict(spec="within", coef_srv=rw["beta"][4], se=rw["se"][4], coef_lgdp=rw["beta"][1], coef_urb=rw["beta"][3], n=rw["n"], clusters=rw["cl"]),
                  dict(spec="between", coef_srv=rb["beta"][4], se=rb["se"][4], coef_lgdp=rb["beta"][1], coef_urb=rb["beta"][3], n=rb["n"], clusters=rb["cl"])]).to_csv(RES/"E5_tertiary_structure.csv", index=False)
    verdict = "association" if abs(rw["beta"][4]) > 1.96*rw["se"][4] else "no within association"
    record("E5", "within slope tertiary GER on services share", rw["beta"][4], rw["se"][4], rw["n"], rw["cl"], "CI excl 0 and sign stable", verdict)
    # robustness: drop log GDP (collinearity) and urban-only
    rob = []
    for name, cols in [("within_no_lgdp", ["one","urb","srv"]), ("within_no_urb", ["one","lgdp","srv"])]:
        cl = list(dict.fromkeys(cols + ["iso3"])); sw = within(d, [c for c in cols if c!="one"])
        rr = ols(sw["y"], sw[cols], cluster=sw["iso3"])
        if rr["beta"] is not None:
            rob.append(dict(spec=name, coef_srv=rr["beta"][2] if "urb" in cols else rr["beta"][2], se=rr["se"][2], n=rr["n"], clusters=rr["cl"]))
    if rob:
        rdf = pd.DataFrame(rob); rdf.to_csv(RES/"E5_robustness.csv", index=False)
        signs = set(np.sign(rdf.coef_srv.dropna())) | {np.sign(rw["beta"][4])}
        record("E5", "services slope sign stability across specs", float("nan"), np.nan, rw["n"], rw["cl"], "sign stable", "not robust (sign unstable)" if len(signs) > 1 else "association", "; ".join(f"{r.spec}={r.coef_srv:+.2f}" for r in rdf.itertuples()))
    return dict(rw=rw, rb=rb)

# ---------------- E6: formalisation and upper-secondary completion ----------------
def e6(data):
    uni = data["uni"]; w = data["wdi"]
    c = uni[(uni.indicator=="completion_upper_secondary")].copy()
    c = c.groupby(["iso3","year"])["value"].mean().reset_index(name="comp")
    m = c.merge(w[["iso3","year","SL.EMP.WORK.ZS"]], on=["iso3","year"]).copy()
    m["wage"] = num(m["SL.EMP.WORK.ZS"]); m = m.dropna(subset=["comp","wage"]).sort_values(["iso3","year"])
    out = []
    for lag in [0,5]:
        mm = m.copy(); mm["wage_l"] = mm.groupby("iso3")["wage"].shift(lag)
        mm = mm.dropna(subset=["wage_l","comp"])
        dw = within(mm, ["comp","wage_l"])
        r = np.corrcoef(dw["comp"], dw["wage_l"])[0,1] if len(mm) > 5 else np.nan
        out.append(dict(lag=lag, within_r=r, n=len(mm), clusters=mm.iso3.nunique()))
        record("E6", f"within corr completion~wage lag{lag}", r, np.nan, len(mm), mm.iso3.nunique(), "|r|>=0.4 at lag5", "association" if (lag==5 and np.isfinite(r) and abs(r)>=0.4) else "not established")
    pd.DataFrame(out).to_csv(RES/"E6_formalisation_completion.csv", index=False)
    return out

# ---------------- E7: state capacity around crossings ----------------
def e7(data):
    cap = data["cap"]; tim = data["tim"]
    def z(s):
        sd = s.std()
        return (s - s.mean())/sd if sd and np.isfinite(sd) else s*0
    cap = cap.copy(); cap["z"] = cap.groupby("indicator")["value"].transform(lambda s: z(num(s)))
    dim = cap.groupby(["iso3","year","dimension"])["z"].mean().reset_index()
    t = tim.copy(); t["cy"] = num(t["crossing_year"]); t = t[t["cy"].notna()]
    t = t[t.level=="lower secondary"].drop_duplicates("iso3")
    rows = []
    for _, r in t.iterrows():
        for dname in ["fiscal","delivery_capacity","enforcement"]:
            dd = dim[(dim.iso3==r.iso3) & (dim.dimension==dname)]
            pre = dd[dd.year.between(r.cy-5, r.cy-1)]["z"].mean(); post = dd[dd.year.between(r.cy+1, r.cy+5)]["z"].mean()
            if np.isfinite(pre) and np.isfinite(post): rows.append(dict(iso3=r.iso3, dimension=dname, delta=post-pre))
    df = pd.DataFrame(rows); df.to_csv(RES/"E7_capacity_around_crossings.csv", index=False)
    if not df.empty:
        s = df.groupby("dimension")["delta"].mean()
        n_dims = int((s.abs() >= 0.25).sum())
        verdict = "capacity-linked" if n_dims >= 2 else ("not established" if len(s) >= 2 else "DATA LIMITED (only %d dimension with coverage)" % len(s))
        record("E7", "capacity delta around lower-sec crossing (SD units)", float(s.mean()), np.nan, len(df), df.iso3.nunique(), ">=0.25 SD in >=2/3 dims", verdict, "; ".join(f"{k}={v:+.2f}" for k,v in s.items()))
    return df

# ---------------- E8: PHL infrastructure strain ----------------
def e8(data):
    w = data["wdi"]
    d = w[w.iso3=="PHL"][["year","SE.SEC.ENRL.TC.ZS","SE.SEC.ENRR"]].copy()
    d["ptrs"] = num(d["SE.SEC.ENRL.TC.ZS"]); d["ger"] = num(d["SE.SEC.ENRR"])
    d = d.dropna().sort_values("year")
    d["dptr"] = d.ptrs.diff(); d["dger"] = d.ger.diff()
    dd = d.dropna(subset=["dptr","dger"]); dd["one"] = 1.0
    r = ols(dd["dptr"], dd[["one","dger"]])
    pd.DataFrame([dict(coef=float(r["beta"][1]) if r["beta"] is not None else np.nan, se=float(r["se"][1]) if r["se"] is not None else np.nan, n=r["n"])]).to_csv(RES/"E8_phl_strain.csv", index=False)
    verdict = "strain" if (r["beta"] is not None and r["beta"][1] > 1.0) else "no strain"
    record("E8", "PHL dPTR on dGER", float(r["beta"][1]) if r["beta"] is not None else np.nan, float(r["se"][1]) if r["se"] is not None else np.nan, r["n"], 1, ">1.0", verdict)
    return r

# ---------------- E9: remittances, spending and enrolment growth ----------------
def e9(data):
    w = data["wdi"]; six = ["PHL","KHM","HKG","CHN","KOR","JPN"]
    w = w[w.iso3.isin(six)]
    out = []
    specs = [("spend","SE.XPD.TOTL.GD.ZS"), ("ger_sec_growth","SE.SEC.ENRR"), ("ger_ter_growth","SE.TER.ENRR")]
    for name, col in specs:
        d = w[["iso3","year","BX.TRF.PWKR.DT.GD.ZS",col]].copy()
        d = d.rename(columns={col:"y"}); d["y"] = num(d["y"]); d["remit_l"] = num(d.groupby("iso3")["BX.TRF.PWKR.DT.GD.ZS"].shift(1))
        if "growth" in name: d["y"] = np.log(d["y"].clip(lower=1)).groupby(d["iso3"]).diff()
        d["lgdp"] = np.log(num(w["NY.GDP.PCAP.PP.CD"]).clip(lower=1))
        d = d.dropna(subset=["y","remit_l"]); d["one"] = 1.0
        dw = within(d, ["y","remit_l","lgdp"])
        r = ols(dw["y"], dw[["one","remit_l","lgdp"]], cluster=dw["iso3"])
        out.append(dict(spec=name, coef=float(r["beta"][1]) if r["beta"] is not None else np.nan, se=float(r["se"][1]) if r["beta"] is not None else np.nan, n=r["n"]))
        if r["beta"] is not None:
            record("E9", f"remittance assoc: {name}", float(r["beta"][1]), float(r["se"][1]), r["n"], r["cl"], "CI excl 0 & sign consistent", "association" if abs(r["beta"][1]) > 1.96*r["se"][1] else "no association")
    pd.DataFrame(out).to_csv(RES/"E9_remittances.csv", index=False)
    return out

# ---------------- E10: replication of E1 in 30 countries ----------------
def e10(data, e1res):
    w = data["wdi"]
    d = w[w.year.between(1995,2024)].copy()
    d["y"] = num(d["SE.SEC.ENRR.UP"]); d["lgdp"] = np.log(num(d["NY.GDP.PCAP.PP.CD"]).clip(lower=1))
    d["urb"] = num(d["SP.URB.TOTL.IN.ZS"]); d["srv"] = num(d["SL.SRV.EMPL.ZS"])
    d = d.dropna(subset=["y","lgdp","urb","srv"]); d["one"] = 1.0
    r = ols(d["y"], d[["one","lgdp","urb","srv"]], cluster=d["iso3"])
    db = between(d, ["y","lgdp","urb","srv"]); db["one"] = 1.0
    rb = ols(db["y"], db[["one","lgdp","urb","srv"]])
    e1w = e1res["rw"]["beta"][1] if e1res["rw"]["beta"] is not None else np.nan
    ci_lo = rb["beta"][1]-1.96*rb["se"][1]; ci_hi = rb["beta"][1]+1.96*rb["se"][1]
    verdict = "replicates" if ci_lo <= e1w <= ci_hi and np.sign(e1w)==np.sign(rb["beta"][1]) else "does not replicate"
    pd.DataFrame([dict(spec="pooled", coef_lgdp=rb["beta"][1], se=rb["se"][1], ci_lo=ci_lo, ci_hi=ci_hi, n=rb["n"], clusters=0),
                  dict(spec="E1_within", coef_lgdp=e1w, se=np.nan, ci_lo=np.nan, ci_hi=np.nan, n=e1res["rw"]["n"], clusters=e1res["rw"]["cl"])]).to_csv(RES/"E10_replication.csv", index=False)
    record("E10", "E1 within slope inside 30-country CI", rb["beta"][1], rb["se"][1], rb["n"], 0, "inside CI and same sign", verdict, f"E1={e1w:+.3f}, 30cty CI=[{ci_lo:+.3f},{ci_hi:+.3f}]")
    return rb

def main():
    data = load()
    RES.mkdir(parents=True, exist_ok=True)
    e1r = e1(data); e2(data); e3(data); e4(data); e5(data); e6(data); e7(data); e8(data); e9(data); e10(data, e1r)
    summ = pd.DataFrame(res_rows)
    summ.to_csv(RES/"SUMMARY.csv", index=False)
    # manifest
    files = {}
    for p in [D/"UNIVERSALIZATION_SERIES.csv", D/"UNIVERSALIZATION_TIMING.csv", D/"BASELINE_SERIES.csv",
              D/"STATE_CAPACITY.csv", D/"SCHOOL_EXPANSION.csv", R/"panel_wdi_wide.csv", R/"economic_complexity_panel_30ctys.csv"]:
        files[str(p.relative_to(PKG))] = hashlib.sha256(p.read_bytes()).hexdigest()
    codeh = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    man = dict(experiments=10, outputs=sorted(p.name for p in RES.glob("*.csv")), data_hashes=files,
               code_sha256=codeh, seeds="deterministic (no RNG)", label="OBSERVED/DERIVED from source status; descriptive only")
    (OUT/"RUN_MANIFEST.json").write_text(json.dumps(man, indent=2))
    print(summ.to_string(index=False))
    print("\nwrote", OUT)

if __name__ == "__main__":
    main()
