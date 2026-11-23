"""Shared helpers: country list, years, loading the series JSON files."""
import json, os, gzip
import numpy as np
DATA = os.environ.get("ATLAS_DATA", "/root/work/data")
RAW = os.environ.get("ATLAS_RAW", "/root/work/impute/raw")
OUT = os.environ.get("ATLAS_OUT", "/root/work/impute/out")
YEARS = np.arange(1950, 2024)
NY = len(YEARS)
meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = sorted(i for i, m in meta.items() if m.get("region", "").strip() != "Aggregates" and len(i) == 3)
CI = {c: k for k, c in enumerate(REG)}
NC = len(REG)


def load(n, data=None):
    p = os.path.join(data or DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz", "rt")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


def to_panel(d):
    """dict -> (NC, NY) array, NaN where absent, 1950-2023 only"""
    a = np.full((NC, NY), np.nan)
    for (i, y), v in d.items():
        if i in CI and 1950 <= y <= 2023:
            a[CI[i], y - 1950] = v
    return a


def panel_to_rows(a, flag=None, ok=None):
    rows = []
    for i in range(NC):
        for j in range(NY):
            v = a[i, j]
            if np.isfinite(v) and (ok is None or ok[i, j]):
                rows.append([REG[i], int(YEARS[j]), round(float(v), 5)])
    return rows
