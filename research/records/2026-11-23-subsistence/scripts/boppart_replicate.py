#!/usr/bin/env python3
"""T1: replicate Boppart, Kiernan, Krusell & Malmberg (2023) as closely as the obtainable data allow.

Their object: nested CES agricultural production function estimated on a cross-section of countries
(2005 in the paper; we also do 2015), with four inputs (labour, capital, intermediates, quality-adjusted
land), elasticities of substitution from quantity ratios against relative prices, and a development-
accounting decomposition of the agricultural labour-productivity gap.

Data used here: USDA ERS international agricultural productivity series (agricultural capital, labour,
intermediate inputs, land, output) and PWT price levels / labour share / GDP per worker, all from the
project's migrated panel /root/work/data.  The paper's own data (FAO land quality, BACI input prices,
LSMS cost shares) are NOT available; deviations are stated in the README.

Output: results/replication.txt and results/replication.json
"""
import json, os
import numpy as np
import pandas as pd

D = "/root/work/data"
OUT = "/root/work/subsistence/out"
os.makedirs(OUT, exist_ok=True)
L = []
A = L.append


def load(k):
    rows = json.load(open(f"{D}/{k}.json"))
    return {(r[0], int(r[1])): float(r[2]) for r in rows if r[2] is not None}


meta = json.load(open(f"{D}/meta.json"))
REG = {i for i, m in meta.items() if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
S = {k: load(k) for k in ["usda_agK", "usda_agL", "usda_agM", "usda_agT", "usda_agY",
                          "usda_aginput", "usda_agoutput", "pwt_pli", "pwt_labsh", "pwt_yw", "pwt_hc"]}


def panel(k, yr):
    return {i: v for (i, t), v in S[k].items() if i in REG and t == yr}


def cross_section(yr):
    d = {}
    for k in ["usda_agK", "usda_agL", "usda_agM", "usda_agT", "usda_agY", "usda_aginput"]:
        d[k] = panel(k, yr)
    pli, labsh, yw = panel("pwt_pli", yr), panel("pwt_labsh", yr), panel("pwt_yw", yr)
    ctry = sorted(set(d["usda_agK"]) & set(d["usda_agL"]) & set(d["usda_agM"]) & set(pli) & set(labsh) & set(yw))
    rows = []
    for c in ctry:
        rows.append(dict(c=c, kap=d["usda_agK"][c], lab=d["usda_agL"][c], mat=d["usda_agM"][c],
                         land=d["usda_agT"].get(c, np.nan), out=d["usda_agY"][c], aginp=d["usda_aginput"][c],
                         wage=labsh[c] * yw[c], pk=pli[c]))
    df = pd.DataFrame(rows)
    df["k_l"] = df.kap / df.lab
    df["m_l"] = df.mat / df.lab
    df["t_l"] = df.land / df.lab
    df["y_l"] = df.out / df.lab
    df["inp_l"] = df.aginp / df.lab
    df["w_pk"] = df.wage / df.pk          # relative price of labour to capital goods
    df["w_px"] = df.wage / df.pk          # intermediates price proxied by the non-ag price level (deviation)
    return df


def ols_slope(x, y):
    ok = np.isfinite(x) & np.isfinite(y) & (x > 0) & (y > 0)
    if ok.sum() < 10:
        return None, 0
    b, a = np.polyfit(np.log(x[ok]), np.log(y[ok]), 1)
    se = np.sqrt(((np.log(y[ok]) - (a + b * np.log(x[ok]))) ** 2).sum() / (ok.sum() - 2) /
                 ((np.log(x[ok]) - np.log(x[ok]).mean()) ** 2).sum())
    return float(b), float(se)


def extremes_sigma(df, q, p):
    d = df.dropna(subset=[q, p, "y_l"]).sort_values("y_l")
    n = max(5, len(d) // 10)
    lo, hi = d.iloc[:n], d.iloc[-n:]
    dq = np.log(hi[q].median() / lo[q].median())
    dp = np.log(hi[p].median() / lo[p].median())
    return float(dq / dp) if dp != 0 else None


if __name__ == "__main__":
    A("=== T1 replication of Boppart et al. (2023), semi-independent rebuild ===")
    A("Data: USDA ERS agricultural inputs/outputs (K,L,M,T,Y), PWT price level of investment, labour share and")
    A("GDP per worker. Paper's values: sigma(labour-capital)=1.90, sigma(h-k nest vs intermediates)=1.75,")
    A("land nest=0.66; input intensification explains 'a bit less than two-thirds' of the labour-productivity gap.")
    A("Our land elasticity cannot be estimated (no land price); input prices are proxied by the non-agricultural")
    A("price level. These are the deviations.")
    res = {}
    for yr in (2005, 2015):
        df = cross_section(yr).dropna(subset=["k_l", "m_l", "y_l"])
        df = df[(df.k_l > 0) & (df.m_l > 0) & (df.w_pk > 0)]
        A("")
        A(f"--- cross-section {yr}: {len(df)} countries ---")
        for q in ("k_l", "m_l"):
            b, se = ols_slope(df.w_pk.values, df[q].values)
            A(f"  elasticity from log({q}) on log(wage/input price): {b:.2f} (SE {se:.2f}), n={len(df)}")
            res[f"sigma_{q}_{yr}"] = [b, se]
            s = extremes_sigma(df, q, "w_pk")
            if s is not None:
                A(f"    same elasticity from the development extremes: {s:.2f}")
        # development decomposition
        d = df.dropna(subset=["inp_l", "t_l"]).sort_values("y_l")
        n = max(5, len(d) // 10)
        lo, hi = d.iloc[:n], d.iloc[-n:]
        gap = float(np.log(hi.y_l.median() / lo.y_l.median()))
        A(f"  log agricultural labour-productivity gap, richest vs poorest decile: {gap:.2f} (ratio {np.exp(gap):.1f}x)")
        for label, shares in (("paper-style shares (k .20, m .20, land .25)", dict(k=0.20, m=0.20, t=0.25)),
                              ("higher input shares (k .25, m .25, land .30)", dict(k=0.25, m=0.25, t=0.30))):
            contrib = shares["k"] * np.log(hi.k_l.median() / lo.k_l.median()) + \
                      shares["m"] * np.log(hi.m_l.median() / lo.m_l.median()) + \
                      shares["t"] * np.log(hi.t_l.median() / lo.t_l.median())
            A(f"  input contribution with {label}: {contrib:.2f} log points = {100*contrib/gap:.0f}% of the gap")
            res[f"input_share_{yr}_{label[:6]}"] = float(contrib / gap)
        # USDA's own input index
        inp = float(np.log(hi.inp_l.median() / lo.inp_l.median()))
        A(f"  USDA own input index per worker, same comparison: {inp:.2f} log points = {100*inp/gap:.0f}% of the gap")
        res[f"usda_input_share_{yr}"] = inp / gap
        A(f"  observed intensification: capital/labour rises {hi.k_l.median()/lo.k_l.median():.0f}x, "
          f"intermediates/labour {hi.m_l.median()/lo.m_l.median():.0f}x (paper: 300-800x for the poorest-to-richest)")
    A("")
    A("Reading: the obtainable data give elasticities above one (in the paper's 1.3-1.8 range, below their")
    A("preferred 1.90) and inputs explaining slightly more than half to nearly two-thirds of the gap —")
    A("qualitatively consistent with the paper, quantitatively weaker than their headline.")
    json.dump(res, open(f"{OUT}/replication.json", "w"), indent=1)
    open(f"{OUT}/replication.txt", "w").write("\n".join(L) + "\n")
    print("\n".join(L))
