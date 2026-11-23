"""Build the country panel used by the simulation.
Inputs (raw/): World Bank mirror of Barro-Lee (women by age group; both sexes -> men by subtraction),
SMAM, adolescent fertility, TFR, urban share, GDP per head (LEVELS; log taken here), plus the user's
local panel files (married18, primary completion, lower-secondary completion).
Output: data/panel.json with, per country, cohort schooling shares (7 levels), urban share, log GDP path,
and the target series."""
import json, sys, numpy as np
RAW = sys.argv[1]; OUT = sys.argv[2]
wb = json.load(open(f"{RAW}/wb_fetch.json")); D = wb["data"]; FIT, HOLD = wb["FIT"], wb["HOLD"]
tot = json.load(open(f"{RAW}/wb_total.json"))
loc = {k: json.load(open(f"{RAW}/local_{k}.json")) for k in ["married18", "prm_cmp", "lsc"]}
COH = list(range(1930, 2000, 5))   # 5-year birth cohorts, start year

def series(key, iso, src=D):
    return {y: v for i, y, v in src[key] if i == iso}
def lookup(d, y):  # nearest available year
    ks = np.array(sorted(d)); return d[int(ks[np.argmin(abs(ks - y))])]

def cats(iso, sex, age, T):
    """7 ordered schooling levels from Barro-Lee. sex 'FE' direct; 'MA' = (total*popT - fem*popF)/popM."""
    def g(src, k, a, s=""):
        key = f"BAR.{k}.{a}" + (f".{s}" if s else "") + (".ZS" if k != "POP" else "")
        return series(key, iso, src).get(T)
    def vec(src, s, pop_key=None):
        return [g(src, "NOED", age, s), g(src, "PRM.ICMP", age, s), g(src, "PRM.CMPT", age, s),
                g(src, "SEC.ICMP", age, s), g(src, "SEC.CMPT", age, s), g(src, "TER.ICMP", age, s), g(src, "TER.CMPT", age, s)]
    f = vec(D, "FE")
    if sex == "FE": x = f
    else:
        t = vec(tot, "")
        pt = series(f"BAR.POP.{age}", iso, tot).get(T); pf = series(f"BAR.POP.{age}.FE", iso, D).get(T)
        if None in t or None in f or pt is None or pf is None or pt <= pf: return None
        x = [(a * pt - b * pf) / (pt - pf) for a, b in zip(t, f)]
    if None in x: return None
    n, p1, p2, s1, s2, t1, t2 = x
    c = np.clip([n, p1 - p2, p2, s1 - s2, s2, t1 - t2, t2], 0, None)
    return (c / c.sum()).tolist()

def cohort_shares(iso, sex):
    out = {}
    for y0 in COH:
        T = y0 + 30
        c = cats(iso, sex, "2529", T) if T <= 2010 else None
        out[y0] = c
    # 1985: 20-24 group at 2010; re-split tertiary by the 1980 cohort's completion ratio
    if out[1985] is None:
        c = cats(iso, sex, "2024", 2010)
        if c is not None and out[1980] is not None:
            r = out[1980][6] / max(out[1980][5] + out[1980][6], 1e-9); te = c[5] + c[6]
            c[5], c[6] = te * (1 - r), te * r
        out[1985] = c
    # 1990, 1995: extrapolate the last two cohort changes in probit space, damped
    from scipy.stats import norm
    def cum(c): return np.cumsum(c)[:-1]
    a, b = cum(out[1980]), cum(out[1985])
    za, zb = norm.ppf(np.clip(a, 1e-4, 1 - 1e-4)), norm.ppf(np.clip(b, 1e-4, 1 - 1e-4))
    for k, y0 in enumerate([1990, 1995], 1):
        z = zb + 0.7 ** k * (zb - za) * k
        z = np.maximum.accumulate(z[::-1])[::-1]  # keep cum shares ordered (decreasing in level)
        cu = np.sort(norm.cdf(z))
        cc = np.diff(np.concatenate([[0], cu, [1]]))
        out[y0] = np.clip(cc, 0, None).tolist()
    return out

panel = {"FIT": FIT, "HOLD": HOLD, "cohorts": COH, "countries": {}}
for iso in FIT + HOLD:
    F, M = cohort_shares(iso, "FE"), cohort_shares(iso, "MA")
    # male shares: fall back to female shares shifted if Barro-Lee male unavailable
    shF = [F[y] for y in COH]
    shM = [M[y] if M[y] is not None else None for y in COH]
    if any(m is None for m in shM):
        for k in range(len(shM)):
            if shM[k] is None: shM[k] = shM[k - 1] if k > 0 and shM[k - 1] is not None else shF[k]
    urb = series("SP.URB.TOTL.IN.ZS", iso)
    uc = []
    for y0 in COH:
        yy = y0 + 2.5 + 22
        if yy < 1960:  # back-cast linearly from first five years, floor 3%
            sl = (urb[1965] - urb[1960]) / 5; v = urb[1960] + sl * (yy - 1960)
        else: v = lookup(urb, min(yy, 2023))
        uc.append(float(np.clip(v / 100, 0.03, 0.97)))
    g = series("NY.GDP.PCAP.KD", iso); yrs = sorted(g); lg = {y: np.log(g[y]) for y in yrs}
    gr = np.clip((lg[yrs[-1]] - lg[yrs[-16]]) / 15, 0.005, 0.04)
    gdp = []
    for y in range(1925, 2051):
        if y < yrs[0]: gdp.append(lg[yrs[0]] - 0.012 * (yrs[0] - y))
        elif y > yrs[-1]: gdp.append(lg[yrs[-1]] + gr * (y - yrs[-1]))
        else: gdp.append(lg[y])
    smf, smm = series("SP.DYN.SMAM.FE", iso), series("SP.DYN.SMAM.MA", iso)
    common = [y for y in smf if y in smm]
    gap = float(np.clip(np.mean([smm[y] - smf[y] for y in common]), 1.0, 6.0)) if common else 3.0
    tf = series("SP.DYN.TFRT.IN", iso); adr = series("SP.ADO.TFRT", iso)
    m18 = {int(y): v for i, y, v in loc["married18"] if i == iso}
    # panel completion rates for the youngest cohorts (check / blend): primary completion at ~age 13, lower sec at ~age 16
    pc = {int(y): v for i, y, v in loc["prm_cmp"] if i == iso}; lc = {int(y): v for i, y, v in loc["lsc"] if i == iso}
    pan_thr = {}
    for y0 in [1985, 1990, 1995]:
        a = pc.get(y0 + 2 + 13); b = lc.get(y0 + 2 + 16)
        pan_thr[y0] = [None if a is None else min(a / 100, 1.0), None if b is None else min(b / 100, 1.0)]
    panel["countries"][iso] = dict(
        shF=shF, shM=shM, urban=uc, gdp=[float(x) for x in gdp], age_gap=gap,
        tfr={y: tf[y] for y in range(1980, 2011, 5) if y in tf}, asfr1519={y: adr[y] / 1000 for y in range(1980, 2011, 5) if y in adr},
        smam={y: v for y, v in smf.items() if 1975 <= y <= 2015}, m18={y: v / 100 for y, v in m18.items() if y >= 1990},
        panel_thresholds=pan_thr, region=json.load(open(f"{RAW}/local_meta.json")).get(iso, {}).get("region", "").strip())
json.dump(panel, open(OUT, "w"))
for iso, p in panel["countries"].items():
    print(iso, p["region"], "tfr", len(p["tfr"]), "smam", len(p["smam"]), "m18", len(p["m18"]), "gap", round(p["age_gap"], 1),
          "F1980", np.round(p["shF"][10], 2).tolist(), "M1980", np.round(p["shM"][10], 2).tolist())
