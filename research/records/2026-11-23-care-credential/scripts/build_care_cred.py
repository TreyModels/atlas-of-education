"""Care-work loop and credential inflation: build the country panel and run the pre-registered tests.

Pre-registration: research/records/2026-11-23-care-credential/PREREGISTRATION.md (committed first).
Measures: care share = female employment in ISIC P+Q over total female employment; credentialed-jobs share =
female employment in ISCO 1+2; credential-occupation gap = female tertiary attainment minus credentialed-jobs
share; outcome = total fertility. Placebos: male care share, manufacturing share.
"""
import csv, glob, json, os, sys
import numpy as np
RAW = "/root/work/care_cred/raw"
OUT = "/root/work/care_cred"

def read_ilo(path):
    rd = list(csv.reader(open(path)))
    hdr = rd[0]; i = {k: n for n, k in enumerate(hdr)}
    rows = [r for r in rd[1:] if len(r) >= 9]
    out = {}
    for r in rows:
        iso, sex, age, eco = r[i["REF_AREA"]], r[i["SEX"]], r[i["AGE"]], r[i["ECO"]]
        if age not in ("AGE_YTHADULT_YGE15", "AGE_AGGREGATE_YGE15"): continue
        try: v = float(r[i["OBS_VALUE"]])
        except Exception: continue
        out.setdefault(iso, {})[(sex, eco, age)] = v
    return out

def age_pref(keys, sex, eco):
    for a in ("AGE_YTHADULT_YGE15", "AGE_AGGREGATE_YGE15"):
        if (sex, eco, a) in keys: return keys[(sex, eco, a)]
    return None

eco_files = sorted(glob.glob(f"{RAW}/ilo_eco_*.csv"))
ocu_files = sorted(glob.glob(f"{RAW}/ilo_ocu_*.csv"))
rows = []
for f in eco_files:
    year = int(f.split("_")[-1].split(".")[0])
    D = read_ilo(f)
    for iso, keys in D.items():
        tf = age_pref(keys, "SEX_F", "ECO_ISIC4_TOTAL"); tm = age_pref(keys, "SEX_M", "ECO_ISIC4_TOTAL")
        pf = age_pref(keys, "SEX_F", "ECO_ISIC4_P"); qf = age_pref(keys, "SEX_F", "ECO_ISIC4_Q")
        pm = age_pref(keys, "SEX_M", "ECO_ISIC4_P"); qm = age_pref(keys, "SEX_M", "ECO_ISIC4_Q")
        cf = age_pref(keys, "SEX_F", "ECO_ISIC4_C")
        if not tf or not pf or not qf: continue
        rows.append(dict(iso=iso, year=year, care_f=100 * (pf + qf) / tf,
                         care_m=(100 * (pm + qm) / tm) if (tm and pm and qm) else np.nan,
                         manuf_f=(100 * cf / tf) if cf else np.nan, emp_f=tf, emp_m=tm))
print("ILO ECO observations:", len(rows), "from", len(eco_files), "year files", flush=True)

# occupations: credentialed jobs = ISCO 1+2 share of female employment
ocu = {}
for f in ocu_files:
    year = int(f.split("_")[-1].split(".")[0])
    rd = list(csv.reader(open(f)))
    hdr = rd[0]; i = {k: n for n, k in enumerate(hdr)}
    for r in rd[1:]:
        if len(r) < 9: continue
        iso, sex, age, ocu_c = r[i["REF_AREA"]], r[i["SEX"]], r[i["AGE"]], r[i["OCU"]]
        if sex != "SEX_F": continue
        if age not in ("AGE_YTHADULT_YGE15", "AGE_AGGREGATE_YGE15"): continue
        try: v = float(r[i["OBS_VALUE"]])
        except Exception: continue
        ocu.setdefault((iso, year), {})[ocu_c] = v
def ocu_share(keys, codes):
    tot = keys.get("OCU_ISCO08_TOTAL") or keys.get("OCU_ISCO88_TOTAL")
    if not tot: return np.nan
    s = 0.0
    for c in codes:
        v = keys.get(c)
        if v is None: return np.nan
        s += v
    return 100 * s / tot
for (iso, year), keys in ocu.items():
    sh = ocu_share(keys, ["OCU_ISCO08_1", "OCU_ISCO08_2"])
    if np.isnan(sh): sh = ocu_share(keys, ["OCU_ISCO88_1", "OCU_ISCO88_2"])
    if np.isnan(sh): continue
    for r in rows:
        if r["iso"] == iso and r["year"] == year: r["isco12_f"] = sh
print("with ISCO share:", sum(1 for r in rows if "isco12_f" in r), flush=True)

# World Bank series
wdi = json.load(open(f"{RAW}/wdi.json"))
def series(key):
    d = {}
    for iso, y, v in wdi.get(key, []):
        try: d[(iso, int(y))] = float(v)
        except Exception: pass
    return d
S = {k: series(k) for k in ("tfr", "flfp", "edu_upsec_f", "edu_ter_f", "gdp_pc", "urban")}
print("WDI sizes:", {k: len(v) for k, v in S.items()}, flush=True)
def near(key, iso, year, tol=2):
    for dt in range(0, tol + 1):
        for y in ((year - dt, year + dt) if dt else (year,)):
            if (iso, y) in S[key]: return S[key][(iso, y)], y
    return None, None
for r in rows:
    for k in S:
        v, y = near(k, r["iso"], r["year"])
        r[k] = v if v is not None else np.nan
        r[f"{k}_year"] = y
# cross-section: latest year per country with a care share and a fertility value
best = {}
for r in rows:
    if not np.isfinite(r.get("tfr", np.nan)): continue
    if r["iso"] not in best or r["year"] > best[r["iso"]]["year"]: best[r["iso"]] = r
cs = list(best.values())
print("cross-section countries:", len(cs), flush=True)
with open(f"{OUT}/panel_cross_section.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=sorted({k for r in cs for k in r})); w.writeheader(); w.writerows(cs)
with open(f"{OUT}/panel_all.csv", "w", newline="") as f:
    w = csv.DictWriter(f, fieldnames=sorted({k for r in rows for k in r})); w.writeheader(); w.writerows(rows)
json.dump(dict(n_obs=len(rows), n_cross=len(cs), years=sorted({r["year"] for r in rows})),
          open(f"{OUT}/coverage.json", "w"), indent=1)
print("wrote panels", flush=True)
