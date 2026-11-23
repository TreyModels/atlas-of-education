#!/usr/bin/env python3
"""Shared panel builder for the policy / foreclosure tests (box2: /root/work/data)."""
import json, os
import numpy as np
import pandas as pd

DATA = os.environ.get("PF_DATA", "/root/work/data")
OUT = os.environ.get("PF_OUT", "/root/work/policy_foreclosure/out")
VARS = ["fertility", "sec", "ter", "lsc", "prm_cmp", "emp_agri", "urban",
        "gdppc_log", "flfp", "life_exp", "u5mr", "electricity", "tax"]


def load(v):
    rows = json.load(open(os.path.join(DATA, v + ".json")))
    d = {}
    for i, t, x in rows:
        if x is None:
            continue
        d.setdefault(i, {})[int(t)] = float(x)
    return d


def panel(y0=1960, y1=2023):
    meta = json.load(open(os.path.join(DATA, "meta.json")))
    iso = [k for k, v in meta.items()
           if v.get("region", "").strip() != "Aggregates" and len(k) == 3]
    data = {v: load(v) for v in VARS}
    recs = []
    for i in iso:
        for y in range(y0, y1 + 1):
            r = {"iso": i, "year": y}
            for v in VARS:
                val = data[v].get(i, {}).get(y)
                if v == "gdppc_log" and val is not None:
                    val = np.log(val) if val > 0 else np.nan
                r[v] = val
            recs.append(r)
    df = pd.DataFrame(recs)
    df["region"] = df.iso.map({k: meta[k]["region"].strip() for k in meta})
    return df


def net_migration(df):
    """World Bank net migration and population, cached; returns merged per-1000 series or None."""
    fn = os.path.join(OUT, "net_migration.csv")
    if os.path.exists(fn):
        nm = pd.read_csv(fn)
    else:
        try:
            import urllib.request
            def wb(ind):
                url = (f"https://api.worldbank.org/v2/country/all/indicator/{ind}"
                       f"?format=json&per_page=20000&date=1960:2023")
                j = json.load(urllib.request.urlopen(url, timeout=60))
                rows = [x for x in j[1] if x["value"] is not None]
                return pd.DataFrame([{"iso": x["countryiso3code"], "year": int(x["date"]),
                                      ind: x["value"]} for x in rows])
            m = wb("SM.POP.NETM"); pop = wb("SP.POP.TOTL")
            nm = m.merge(pop, on=["iso", "year"], how="inner")
            nm["netmig_p1000"] = nm["SM.POP.NETM"] / nm["SP.POP.TOTL"] * 1000
            nm = nm[["iso", "year", "netmig_p1000"]]
            nm.to_csv(fn, index=False)
        except Exception as e:
            print("WB migration fetch failed:", e)
            return df
    return df.merge(nm, on=["iso", "year"], how="left")
