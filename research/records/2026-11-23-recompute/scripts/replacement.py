import os
#!/usr/bin/env python3
"""What did countries share in the years BEFORE they fell below replacement?

Find the year each country's fertility first drops below 2.1 and stays there.
Then look back 5, 10 and 20 years and ask what was already true.
"""
import json, os, gzip
import numpy as np

DATA = os.path.join(os.path.dirname(os.path.abspath(__file__)), "data")


def load(n):
    p = os.path.join(DATA, n + ".json")
    op = open(p) if os.path.exists(p) else gzip.open(p + ".gz")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(op) if r[2] is not None}


meta = json.load(open(os.path.join(DATA, "meta.json")))
REG = {i: m["region"].strip() for i, m in meta.items()
       if m.get("region", "").strip() != "Aggregates" and len(i) == 3}
KEYS = ["lsc", "sec", "ter", "gpi_ter", "u5mr", "gdppc_log", "urban", "flfp",
        "electricity", "life_exp", "wage_emp"]
LAB = {"lsc": "girls+boys finishing lower sec", "sec": "secondary completion",
       "ter": "young people in higher ed", "gpi_ter": "women per man in higher ed",
       "u5mr": "child deaths per 1000", "gdppc_log": "income per person",
       "urban": "% in cities", "flfp": "women in labour force %",
       "electricity": "% homes with power", "life_exp": "life expectancy",
       "wage_emp": "% jobs that are paid"}
S = {k: {kk: vv for kk, vv in load(k).items() if kk[0] in REG} for k in KEYS + ["fertility"]}
F = S["fertility"]


def serial(iso):
    return dict(sorted((y, v) for (i, y), v in F.items() if i == iso))


def cross_year(iso, lvl=2.1):
    s = serial(iso)
    ys = sorted(s)
    for k, y in enumerate(ys):
        if s[y] < lvl:
            nxt = [s[z] for z in ys[k + 1:k + 6]]
            if len(nxt) >= 3 and sum(1 for v in nxt if v < lvl + 0.1) >= max(2, len(nxt) - 1):
                return y
    return None


def at(iso, key, y, tol=3):
    best = None
    for d in range(tol + 1):
        for yy in (y - d, y + d):
            if (iso, yy) in S[key]:
                return S[key][(iso, yy)]
    return None


crossers, stayers = {}, []
for iso in sorted(REG):
    s = serial(iso)
    if len(s) < 20:
        continue
    c = cross_year(iso)
    if c:
        crossers[iso] = c
    elif s and min(s.values()) > 2.4:
        stayers.append(iso)

print(f"{len(crossers)} countries fell below replacement; {len(stayers)} never did\n")
print("=" * 84)
print("THE CLUB, in order of arrival")
print("=" * 84)
by_year = {}
for iso, y in crossers.items():
    by_year.setdefault((y // 10) * 10, []).append(iso)
for dec in sorted(by_year):
    print(f"  {dec}s: " + ", ".join(sorted(by_year[dec])))

print()
print("=" * 84)
print("WHAT THEY LOOKED LIKE 20 / 10 / 5 YEARS BEFORE CROSSING")
print("=" * 84)
print(f"{'':34s}{'20 yrs before':>15}{'10 yrs':>10}{'5 yrs':>9}{'never-crossed':>15}")
for k in KEYS:
    row = []
    for h in (20, 10, 5):
        vals = [at(i, k, c - h) for i, c in crossers.items()]
        vals = [v for v in vals if v is not None]
        row.append(np.median(vals) if vals else float("nan"))
    sv = [at(i, k, 2010) for i in stayers]
    sv = [v for v in sv if v is not None]
    print(f"  {LAB[k]:32s}{row[0]:15.1f}{row[1]:10.1f}{row[2]:9.1f}"
          f"{(np.median(sv) if sv else float('nan')):15.1f}")

print()
print("=" * 84)
print("HOW FAST THINGS WERE MOVING IN THE 10 YEARS BEFORE CROSSING")
print("=" * 84)
for k in KEYS:
    ch = []
    for i, c in crossers.items():
        a, b = at(i, k, c - 10), at(i, k, c)
        if a is not None and b is not None:
            ch.append((k, b - a))
    vals = [v for kk, v in ch if kk == k]
    if vals:
        print(f"  {LAB[k]:32s} median change {np.median(vals):+8.1f}   "
              f"(25th-75th: {np.percentile(vals,25):+.1f} to {np.percentile(vals,75):+.1f})")

print()
print("=" * 84)
print("THE ODD ONES: crossed below replacement while still POOR or UNDER-SCHOOLED")
print("=" * 84)
rows = []
for i, c in crossers.items():
    inc = at(i, "gdppc_log", c)
    ls = at(i, "lsc", c)
    if inc is not None and ls is not None:
        rows.append((i, c, inc, ls))
rows.sort(key=lambda r: r[2])
print("  lowest income at crossing:")
for i, c, inc, ls in rows[:8]:
    print(f"    {i}  crossed {c}  at ${inc:,.0f} per head, lower-secondary {ls:.0f}%")
print("  lowest basic schooling at crossing:")
for i, c, inc, ls in sorted(rows, key=lambda r: r[3])[:8]:
    print(f"    {i}  crossed {c}  with lower-secondary {ls:.0f}%, ${inc:,.0f} per head")

print()
print("=" * 84)
print("HOW MANY HAD EACH CONDITION ALREADY TRUE 10 YEARS BEFORE")
print("=" * 84)
conds = [("income above $5,000", lambda v: v > 5000, "gdppc_log"),
         ("income above $10,000", lambda v: v > 10000, "gdppc_log"),
         ("lower-secondary above 70%", lambda v: v > 70, "lsc"),
         ("lower-secondary above 50%", lambda v: v > 50, "lsc"),
         ("child deaths below 50", lambda v: v < 50, "u5mr"),
         ("city share above 50%", lambda v: v > 50, "urban"),
         ("women outnumber men in higher ed", lambda v: v > 1.0, "gpi_ter"),
         ("electricity above 90%", lambda v: v > 90, "electricity")]
for lab, f, k in conds:
    n = sum(1 for i, c in crossers.items() if (lambda v: v is not None and f(v))(at(i, k, c - 10)))
    tot = sum(1 for i, c in crossers.items() if at(i, k, c - 10) is not None)
    if tot:
        print(f"  {lab:36s} {n:3d} of {tot:3d}   ({100*n/tot:3.0f}%)")
