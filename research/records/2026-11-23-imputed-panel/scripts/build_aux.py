#!/usr/bin/env python3
"""Step 2: assemble the long-run sources on the country x year (1950-2023) grid.

Writes OUT/aux.npz with
  macro_obs / macro_lr  : fertility, life expectancy, under-five mortality, urban share, income per head
                          (observed series, and the same with gaps filled from a long-run source, level-matched)
  education predictors  : Wittgenstein shares by age, Barro-Lee, Lee-Lee enrolment, all on the annual grid
"""
import sys, re, unicodedata
import numpy as np, pandas as pd, pyreadr
from common import *

os.makedirs(OUT, exist_ok=True)
print("countries", NC, flush=True)


def norm(s):
    s = unicodedata.normalize("NFKD", str(s)).encode("ascii", "ignore").decode().lower()
    return re.sub(r"[^a-z]", "", s)


def grid5_to_annual(df, col):
    """df has iso3, year, col on a 5-year grid; linear interpolation within country, no extrapolation"""
    a = np.full((NC, NY), np.nan)
    for iso, g in df.dropna(subset=[col]).groupby("iso3"):
        if iso not in CI:
            continue
        g = g.sort_values("year")
        y = g.year.values.astype(float)
        if len(y) < 2:
            continue
        a[CI[iso]] = np.interp(YEARS, y, g[col].values.astype(float), left=np.nan, right=np.nan)
    return a


# ---------------- UN WPP 2024 (medium variant; history is variant-independent) ----------------
w = pd.read_csv(f"{RAW}/wpp2024_di.csv.gz", usecols=["LocID", "ISO3_code", "Location", "LocTypeName", "Time", "TFR", "LEx", "Q5"], low_memory=False)
w = w[w.LocTypeName == "Country/Area"]
name2iso = {norm(n): i for n, i in zip(w.Location, w.ISO3_code)}
loc2iso = dict(zip(w.LocID, w.ISO3_code))
ALIAS = {"koreasouth": "KOR", "republicofkorea": "KOR", "korearep": "KOR", "korea": "KOR", "vietnam": "VNM", "russia": "RUS",
         "iran": "IRN", "syria": "SYR", "laos": "LAO", "egypt": "EGY", "venezuela": "VEN", "bolivia": "BOL", "tanzania": "TZA",
         "gambia": "GMB", "bahamas": "BAH", "unitedstates": "USA", "unitedstatesofamerica": "USA", "hongkong": "HKG",
         "taiwan": "TWN", "congodemrep": "COD", "democraticrepublicofthecongo": "COD", "congo": "COG", "congorep": "COG",
         "czechia": "CZE", "czechoslovakia": "", "ussr": "", "yugoslavia": "", "turkey": "TUR", "turkiye": "TUR",
         "capeverde": "CPV", "ivorycoast": "CIV", "cotedivoire": "CIV", "burma": "MMR", "myanmarburma": "MMR", "swaziland": "SWZ",
         "yemenrep": "YEM", "kyrgyzstan": "KGZ", "kyrgyzrepublic": "KGZ", "slovakia": "SVK", "macedonia": "MKD", "northmacedonia": "MKD",
         "moldova": "MDA", "brunei": "BRN", "palestine": "PSE", "westbankandgaza": "PSE", "eastgermany": "", "westgermany": "DEU"}
name2iso.update({k: v for k, v in ALIAS.items() if v})
w["iso3"] = w.ISO3_code
macro = {}
for tag, col in (("fertility", "TFR"), ("life_exp", "LEx"), ("u5mr", "Q5")):
    a = np.full((NC, NY), np.nan)
    for iso, g in w[w.Time.between(1950, 2023)].groupby("iso3"):
        if iso in CI:
            a[CI[iso], g.Time.values.astype(int) - 1950] = g[col].values
    macro[tag] = a
# ---------------- UN WUP 2025 revision, share urban, national definitions ----------------
u = pd.read_csv(f"{RAW}/wup_urban.csv", header=0)
u = u[u.ISO3_Code.notna()]
a = np.full((NC, NY), np.nan)
for _, r in u.iterrows():
    if r.ISO3_Code in CI:
        for y in range(1950, 2024):
            v = r.get(f"{y}.0")
            if v is not None and pd.notna(v):
                a[CI[r.ISO3_Code], y - 1950] = float(v)
macro["urban"] = a
# ---------------- income: PWT 10.x, then Maddison 2023 ----------------
p = pd.read_excel("/root/work/pwt.xlsx", sheet_name="Data", usecols=["countrycode", "year", "rgdpna", "pop"])
p["pc"] = p.rgdpna / p["pop"]
pw = np.full((NC, NY), np.nan)
for iso, g in p[p.year.between(1950, 2023)].groupby("countrycode"):
    if iso in CI:
        pw[CI[iso], g.year.values - 1950] = g.pc.values
m = pd.read_csv(f"{RAW}/mpd_Full_data.csv")
mp = np.full((NC, NY), np.nan)
for iso, g in m[m.year.between(1950, 2023)].groupby("countrycode"):
    if iso in CI:
        mp[CI[iso], g.year.values - 1950] = g.gdppc.values
print("PWT countries", int(np.isfinite(pw).any(1).sum()), "Maddison countries", int(np.isfinite(mp).any(1).sum()), flush=True)

obs = {k: to_panel(load(k)) for k in ("fertility", "life_exp", "u5mr", "urban", "gdppc_log")}
src = {"fertility": [macro["fertility"]], "life_exp": [macro["life_exp"]], "u5mr": [macro["u5mr"]],
       "urban": [macro["urban"]], "gdppc_log": [pw, mp]}
LOGSCALE = {"gdppc_log": True, "u5mr": True}


def splice(o, sources, logscale):
    """fill gaps in the observed series from the long-run sources, matching level by the median country difference
    over the overlap (in logs for ratios); returns filled array and flag (1 = long-run source)"""
    f = o.copy(); flag = np.zeros(o.shape, int)
    tr = (lambda x: np.log(np.maximum(x, 1e-6))) if logscale else (lambda x: x)
    itr = np.exp if logscale else (lambda x: x)
    for i in range(NC):
        for s in sources:
            miss = ~np.isfinite(f[i]) & np.isfinite(s[i])
            ov = np.isfinite(o[i]) & np.isfinite(s[i])
            if miss.any() and ov.sum() >= 5:
                off = np.median(tr(o[i][ov]) - tr(s[i][ov]))
                f[i, miss] = itr(tr(s[i][miss]) + off); flag[i, miss] = 1
    return f, flag


macro_lr, macro_flag = {}, {}
for k in obs:
    macro_lr[k], macro_flag[k] = splice(obs[k], src[k], LOGSCALE.get(k, False))
    print(f"{k:10s} observed share {np.isfinite(obs[k]).mean():.3f} -> after long-run fill {np.isfinite(macro_lr[k]).mean():.3f}", flush=True)
# level agreement check of sources with observed (overlap correlation of within-country changes) is in validate.py

# ---------------- Wittgenstein Centre WCDE v3 (population by age, sex, education) ----------------
d = list(pyreadr.read_r(f"{RAW}/wcde_pop-age-sex-edattain.rds").values())[0]
d = d[d.education.isin(["No Education", "Incomplete Primary", "Primary", "Lower Secondary", "Upper Secondary", "Post Secondary"])]
d["iso3"] = d.country_code.astype(int).map(loc2iso)
d = d[d.iso3.isin(CI)]
d = d.groupby(["iso3", "year", "age", "education"], as_index=False)["pop"].sum()
piv = d.pivot_table(index=["iso3", "year", "age"], columns="education", values="pop").reset_index()
tot = piv[["No Education", "Incomplete Primary", "Primary", "Lower Secondary", "Upper Secondary", "Post Secondary"]].sum(1)
piv["nos"] = piv["No Education"] / tot
piv["ls"] = (piv["Lower Secondary"] + piv["Upper Secondary"] + piv["Post Secondary"]) / tot
piv["us"] = (piv["Upper Secondary"] + piv["Post Secondary"]) / tot
piv["ps"] = piv["Post Secondary"] / tot
piv["pr"] = 1 - (piv["No Education"] + piv["Incomplete Primary"]) / tot
piv["year"] = piv.year.astype(int)
aux = {}
for age, tag in (("15--19", "15"), ("20--24", "20"), ("25--29", "25")):
    g = piv[piv.age == age]
    for c in ("nos", "ls", "us", "ps", "pr"):
        aux[f"wc_{c}{tag}"] = grid5_to_annual(g.rename(columns={}), c)
# cohort back-projection: the 25-29 age group ten years later was 15-19 now; only while the later year is observed history (<=2020)
for c in ("nos", "ls", "us", "ps", "pr"):
    a25 = aux[f"wc_{c}25"]
    full = grid5_to_annual(piv[piv.age == "25--29"], c)  # to 2023 grid; need up to 2033: recompute on wider grid
    g = piv[piv.age == "25--29"]
    wide = np.full((NC, 2100 - 1950 + 1), np.nan)
    yy = np.arange(1950, 2101)
    for iso, gg in g.groupby("iso3"):
        gg = gg.sort_values("year"); wide[CI[iso]] = np.interp(yy, gg.year.values, gg[c].values)
    co = np.full((NC, NY), np.nan)
    for j, y in enumerate(YEARS):
        if y + 10 <= 2020:
            co[:, j] = wide[:, y + 10 - 1950]
    aux[f"wc_co_{c}"] = co
# ---------------- Barro-Lee v3 (1950-2015, 5-yearly, both sexes, by age) ----------------
b = pd.read_csv(f"{RAW}/BL_v3_MF.csv")
b = b[(b.agefrom == 15) & (b.ageto == 24)].rename(columns={"WBcode": "iso3"})
for c in ("yr_sch", "lp", "ls", "lh"):
    aux[f"bl_{c}"] = grid5_to_annual(b, c)
b2 = pd.read_csv(f"{RAW}/BL_v3_MF.csv")
b2 = b2[(b2.agefrom == 25) & (b2.ageto == 34)].rename(columns={"WBcode": "iso3"})
aux["bl_ysch2534_lead10"] = np.full((NC, NY), np.nan)
tmp = grid5_to_annual(b2, "yr_sch")
for j, y in enumerate(YEARS):  # cohort back-projection: age 25-34 ten years later
    if y + 10 <= 2015:
        aux["bl_ysch2534_lead10"][:, j] = tmp[:, j + 10]
# ---------------- Lee-Lee 2016 enrolment ratios (1820-2010, 5-yearly) ----------------
ll = pd.read_csv(f"{RAW}/ll_enroll.csv", header=None, skiprows=8, names=["Country", "Year", "pri", "sec", "ter", "Region"])
ll["Country"] = ll.Country.ffill()
ll = ll[pd.to_numeric(ll.Year, errors="coerce").notna()].copy()
ll["year"] = ll.Year.astype(float).astype(int)
ll["iso3"] = ll.Country.map(lambda s: name2iso.get(norm(s), ALIAS.get(norm(s), "")))
unm = sorted(set(ll.Country[ll.iso3 == ""]))
print("Lee-Lee unmatched names:", unm, flush=True)
for c in ("pri", "sec", "ter"):
    aux[f"ll_{c}"] = grid5_to_annual(ll[ll.iso3 != ""], c)
for k, v in aux.items():
    print(f"  {k:20s} cells {np.isfinite(v).mean():.3f}", flush=True)
np.savez_compressed(f"{OUT}/aux.npz", **{f"obs_{k}": v for k, v in obs.items()}, **{f"lr_{k}": v for k, v in macro_lr.items()},
                    **{f"flag_{k}": v for k, v in macro_flag.items()}, **{f"x_{k}": v for k, v in aux.items()})
print("saved")
