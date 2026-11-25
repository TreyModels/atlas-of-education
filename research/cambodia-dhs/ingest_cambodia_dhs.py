#!/usr/bin/env python3
"""Cambodia DHS PR attendance / out-of-school extraction (pre-registered).

Reads the DHS PR recodes (KHPR42/51/61/73/82) with pyreadstat, computes weighted
attendance/out-of-school by age group, sex, residence and region, and writes
derived aggregates. Raw microdata are NOT committed (DHS terms).

Definitions (see PRE_REGISTRATION.md):
  current attendance = HV121==1 OR (HV121==2 AND HV122>0)
  upper bound        = HV121 in {1,2}
  out-of-school      = 1 - current attendance
"""
import hashlib, json, os, sys
import numpy as np
import pandas as pd
import pyreadstat

BASE = os.path.expanduser("~/neon-boot/pulled/dhs/cambodia")
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "results")
os.makedirs(OUT, exist_ok=True)
WAVES = {
    "2000":    ("KHPR42SD", "KHPR42FL.SAS7BDAT"),
    "2005":    ("KHPR51SD", "KHPR51FL.SAS7BDAT"),
    "2010":    ("KHPR61SD", "KHPR61FL.SAS7BDAT"),
    "2014":    ("KHPR73SD", "KHPR73FL.SAS7BDAT"),
    "2021-22": ("KHPR82SD", "KHPR82FL.SAS7BDAT"),
}
COLS = ["HV001","HV002","HV021","HV022","HV024","HV025","HV005",
        "HV104","HV105","HV121","HV122"]

def sha256(p):
    h = hashlib.sha256()
    with open(p, "rb") as f:
        for b in iter(lambda: f.read(1 << 20), b""):
            h.update(b)
    return h.hexdigest()

def taylor(df, ycol, by):
    """Weighted proportion + Taylor-linearized SE (PSU within strata)."""
    rows = []
    grouped = df.groupby(by, dropna=False) if by else [((), df)]
    for key, g in grouped:
        w = g["w"].to_numpy(float); y = g[ycol].to_numpy(float)
        sw = w.sum()
        if sw <= 0 or len(g) == 0:
            continue
        p = float((w * y).sum() / sw)
        z = w * (y - p) / sw
        cl = (pd.DataFrame({"h": g["HV022"].to_numpy(), "c": g["HV021"].to_numpy(), "z": z})
                .groupby(["h", "c"], dropna=False)["z"].sum())
        var = 0.0
        for _, gg in cl.groupby(level=0):
            n = len(gg)
            if n > 1:
                var += n / (n - 1) * float(((gg - gg.mean()) ** 2).sum())
        se = float(np.sqrt(var))
        rec = dict(zip(by, key if isinstance(key, tuple) else (key,)))
        rec.update(n=len(g), pct=round(100 * p, 3), se=round(100 * se, 3),
                   ci_lo=round(100 * (p - 1.96 * se), 2), ci_hi=round(100 * (p + 1.96 * se), 2))
        rows.append(rec)
    return rows

def load_wave(wave, folder, fname):
    path = os.path.join(BASE, wave, folder, fname)
    df, meta = pyreadstat.read_sas7bdat(path, usecols=[c for c in COLS if c in COLS])
    have = set(df.columns)
    for c in COLS:
        if c not in have:
            df[c] = np.nan
    df["w"] = df["HV005"] / 1e6
    df = df[(df["HV105"] >= 6) & (df["HV105"] <= 17)].copy()
    df["age_group"] = pd.cut(df["HV105"], [5, 11, 14, 17],
                             labels=["6-11", "12-14", "15-17"])
    df["att_current"] = ((df["HV121"] == 1) | ((df["HV121"] == 2) & (df["HV122"].fillna(0) > 0))).astype(float)
    df["att_any"] = df["HV121"].isin([1, 2]).astype(float)
    df["sex"] = df["HV104"].map({1: "Male", 2: "Female"})
    df["res"] = df["HV025"].map({1: "Urban", 2: "Rural"})
    df["reg"] = np.where(df["HV024"] == 12, "Phnom Penh", "Other")
    df["wave"] = wave
    cat = dict(wave=wave, path=path, sha256=sha256(path), n_rows=int(len(df)),
               n_age_6_17=int(len(df)),
               hv121_values=sorted([float(x) for x in df["HV121"].dropna().unique()]),
               missing_hv121=int(df["HV121"].isna().sum()),
               missing_hv122=int(df["HV122"].isna().sum()),
               weight_sum=float(df["w"].sum()))
    return df, cat

def main():
    frames, catalog = [], []
    for wave, (folder, fname) in WAVES.items():
        print(f"reading {wave} ...", flush=True)
        df, cat = load_wave(wave, folder, fname)
        frames.append(df); catalog.append(cat)
        print(f"  {wave}: {len(df)} members aged 6-17", flush=True)
    allw = pd.concat(frames, ignore_index=True)

    # write catalog
    with open(os.path.join(OUT, "catalog.json"), "w") as f:
        json.dump({"waves": catalog, "definition":
                   "current = HV121==1 OR (HV121==2 AND HV122>0)",
                   "note": "raw microdata not committed; derived aggregates only"}, f, indent=2)

    # national by wave x age group, both variants
    rows = []
    for variant, col in [("current", "att_current"), ("any_current_year", "att_any")]:
        for r in taylor(allw, col, ["wave", "age_group"]):
            r["variant"] = variant; rows.append(r)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "attendance_by_wave.csv"), index=False)

    # 2021-22 by age x sex x residence x region
    d22 = allw[allw.wave == "2021-22"]
    rows = []
    for variant, col in [("current", "att_current"), ("any_current_year", "att_any")]:
        for r in taylor(d22, col, ["age_group", "sex", "res", "reg"]):
            r["variant"] = variant; rows.append(r)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "attendance_2021_22_by_sex_residence.csv"), index=False)

    # all waves by age x sex
    rows = []
    for variant, col in [("current", "att_current"), ("any_current_year", "att_any")]:
        for r in taylor(allw, col, ["wave", "age_group", "sex"]):
            r["variant"] = variant; rows.append(r)
    pd.DataFrame(rows).to_csv(os.path.join(OUT, "attendance_by_wave_sex.csv"), index=False)

    print("\n=== national, current attendance variant, by wave/age ===")
    df = pd.read_csv(os.path.join(OUT, "attendance_by_wave.csv"))
    print(df[df.variant == "current"].pivot(index="wave", columns="age_group", values="pct").to_string())
    print("\n=== 2021-22 by age x residence (current) ===")
    d = pd.read_csv(os.path.join(OUT, "attendance_2021_22_by_sex_residence.csv"))
    print(d[(d.variant == "current") & (d.sex == "Male")].pivot_table(
        index="age_group", columns="res", values="pct", aggfunc="mean").to_string())
    print("\nwrote", OUT)

if __name__ == "__main__":
    main()
