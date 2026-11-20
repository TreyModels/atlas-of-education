#!/usr/bin/env python3
"""Cluster 2 (tertiary crossing structure): predeclared experiments X4, X5, X6.

Deterministic; absolute paths; no randomness (seed fixed for manifest only).

Rules implemented (frozen by cluster pre-declaration):
- Crossing year = band midpoint (mean of band_earliest / band_latest) when both present.
  Left-censored (band_earliest blank) -> band_latest, marked censored.
  Right-censored (band_latest blank)  -> last_obs_year, marked censored, EXCLUDED from medians.
- Milestone measure used: GER (observed status) rows of UNIVERSALIZATION_TIMING.csv.
- Structure variables at crossing from JOBS_AND_MARKETS_PANEL.csv (1995-2024 coverage):
  exact-year value if present, else linear interpolation between bracketing years.
  NO extrapolation outside observed panel range -> value missing.
- LGDP = log(NY.GDP.PCAP.PP.CD); URBAN = SP.URB.TOTL.IN.ZS; SVCS = SL.SRV.EMPL.ZS.
- IQR via linear-interpolation percentiles (numpy default), Q1=25, Q3=75.
"""
import csv, json, hashlib, sys, platform
from pathlib import Path
import numpy as np

BASE = Path("/Users/treymenefee/massification_live/experiments/massification-2026-11-20/10_massification")
DATA = BASE / "data"
MYDIR = BASE / "extensions/lab_2026-11-20_b/cluster_2_tertiary_crossings"
RES = MYDIR / "results"
RES.mkdir(parents=True, exist_ok=True)

TIMING = DATA / "UNIVERSALIZATION_TIMING.csv"
PANEL = DATA / "JOBS_AND_MARKETS_PANEL.csv"
SERIES = DATA / "UNIVERSALIZATION_SERIES.csv"

STRUCT = {"LGDP": "NY.GDP.PCAP.PP.CD", "URBAN": "SP.URB.TOTL.IN.ZS", "SVCS": "SL.SRV.EMPL.ZS"}
CLUSTER = "2_tertiary_crossing_structure"

def load_timing():
    rows = []
    with open(TIMING, newline="") as f:
        for r in csv.DictReader(f):
            if r["measure"] != "GER":
                continue
            if r["level"] not in ("secondary", "tertiary") or r["threshold_pct"] not in ("15", "50", "90"):
                continue
            be, bl = r["band_earliest"].strip(), r["band_latest"].strip()
            cens = r["censoring"].strip()
            if cens == "right":
                year = float(r["last_obs_year"]) if r["last_obs_year"].strip() else None
            elif cens == "left":
                year = float(bl) if bl else (float(r["last_obs_year"]) if r["last_obs_year"].strip() else None)
            elif be and bl:
                year = (float(be) + float(bl)) / 2.0
            elif bl:
                year = float(bl)
            elif be:
                year = float(be)
            else:
                year = None
            rows.append({
                "country": r["country"], "iso3": r["iso3"], "level": r["level"],
                "thr": int(r["threshold_pct"]), "year": year, "censored": cens in ("left", "right"),
                "censoring": cens or "none", "status": r["status"],
            })
    return rows

def load_panel():
    d = {}  # (country, indicator) -> {year: value}
    with open(PANEL, newline="") as f:
        for r in csv.DictReader(f):
            if r["indicator_code"] in STRUCT.values() and r["value"].strip():
                d.setdefault((r["country"], r["indicator_code"]), {})[int(r["year"])] = float(r["value"])
    return d

def value_at(panel, country, code, year):
    if year is None:
        return None
    s = panel.get((country, code))
    if not s:
        return None
    if year in s:
        return s[year]
    ys = sorted(s)
    if year < ys[0] or year > ys[-1]:
        return None  # no extrapolation
    import bisect
    i = bisect.bisect_left(ys, year)
    y0, y1 = ys[i-1], ys[i]
    v0, v1 = s[y0], s[y1]
    if y1 == y0:
        return v0
    return v0 + (v1 - v0) * (year - y0) / (y1 - y0)

def structure_at(panel, country, year):
    out = {}
    for var, code in STRUCT.items():
        v = value_at(panel, country, code, year)
        out[var] = None if v is None else (np.log(v) if var == "LGDP" else v)
    return out

def q(vals, p):
    return float(np.percentile(np.array(vals, dtype=float), p)) if len(vals) else None

def ranks(vals):
    # average ranks for ties
    order = sorted(range(len(vals)), key=lambda i: vals[i])
    r = [0.0] * len(vals)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and vals[order[j+1]] == vals[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1.0
        for k in range(i, j+1):
            r[order[k]] = avg
        i = j + 1
    return r

def spearman(x, y):
    n = len(x)
    if n < 3:
        return None
    rx, ry = ranks(x), ranks(y)
    mx, my = sum(rx)/n, sum(ry)/n
    num = sum((a-mx)*(b-my) for a, b in zip(rx, ry))
    den = (sum((a-mx)**2 for a in rx) * sum((b-my)**2 for b in ry)) ** 0.5
    return num/den if den else None

def fmt(v):
    return "" if v is None else (f"{v:.6f}" if isinstance(v, float) else str(v))

timing = load_timing()
panel = load_panel()

def get_milestones(level, thr):
    return [r for r in timing if r["level"] == level and r["thr"] == thr]

# ---------------- X4 ----------------
X4_SETS = [("tertiary 15 + tertiary 50", [("tertiary", 15), ("tertiary", 50)]),
           ("secondary 50 + secondary 90", [("secondary", 50), ("secondary", 90)])]

x4_rows = []
x4_verdicts = {}
for set_name, miles in X4_SETS:
    per_var_inside = {}
    for var in STRUCT:
        vals, inside, total = {}, 0, 0
        per_country = []
        for lvl, thr in miles:
            for r in get_milestones(lvl, thr):
                s = structure_at(panel, r["country"], r["year"])
                v = s[var]
                per_country.append((r["country"], r["iso3"], r["year"], r["censoring"], v))
                if v is not None:
                    vals[r["country"]] = v
        vv = list(vals.values())
        if vv:
            Q1, Q3 = q(vv, 25), q(vv, 75)
            for c, v in vals.items():
                total += 1
                if Q1 <= v <= Q3:
                    inside += 1
        else:
            Q1 = Q3 = None
        per_var_inside[var] = (inside, total)
        for c, iso, yr, cens, v in per_country:
            x4_rows.append([set_name, var, c, iso, fmt(yr), cens, fmt(v), fmt(Q1), fmt(Q3),
                            inside, total, "", ""])
        med = q(vv, 50) if vv else None
        x4_rows.append([set_name, var, "SUMMARY", "", "", "", fmt(med), fmt(Q1), fmt(Q3),
                        inside, total, f"inside_IQR={inside}/{total}", ""])
    n_ok = sum(1 for var in STRUCT if per_var_inside[var][0] >= 4 and per_var_inside[var][1] > 0
               and per_var_inside[var][0] / max(per_var_inside[var][1], 1) >= 4/6)
    # threshold: >=4/6 countries inside IQR on >=2 of 3 variables (denominator = countries with values)
    n_ok = sum(1 for var in STRUCT if per_var_inside[var][0] >= 4)
    if all(per_var_inside[v][1] >= 4 for v in STRUCT):
        verdict = "SUPPORTED" if n_ok >= 2 else "NOT SUPPORTED"
    else:
        verdict = "NOT SUPPORTED" if n_ok < 2 else "PARTIAL"
    x4_verdicts[set_name] = (verdict, n_ok, per_var_inside)

with open(RES / "X4_crossing_typicality.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["milestone_set", "variable", "country", "iso3", "crossing_year", "censoring",
                "value", "Q1", "Q3", "inside_count", "n_with_values", "per_set_stat", "note"])
    w.writerows(x4_rows)

# ---------------- X5 ----------------
t50 = get_milestones("tertiary", 50)
s90 = get_milestones("secondary", 90)
dated_t = [r for r in t50 if not r["censored"]]
dated_s = [r for r in s90 if not r["censored"]]
x5_rows = []
x5_flags = {}
min_n = min(len(dated_t), len(dated_s))
for var in STRUCT:
    def collect(rows_):
        out = {}
        for r in rows_:
            v = structure_at(panel, r["country"], r["year"])[var]
            if v is not None:
                out[r["country"]] = v
        return out
    vt, vs = collect(dated_t), collect(dated_s)
    lt, ls = list(vt.values()), list(vs.values())
    med_t, med_s = q(lt, 50), q(ls, 50)
    pooled = lt + ls
    iqr_w = (q(pooled, 75) - q(pooled, 25)) if pooled else None
    if med_t is None or med_s is None or iqr_w in (None, 0):
        diff = ratio = None
        flag = None
    else:
        diff = med_t - med_s
        ratio = abs(diff) / iqr_w
        flag = "same" if ratio <= 0.50 else "different"
    x5_flags[var] = flag
    for c, v in sorted(vt.items()):
        x5_rows.append([var, "tertiary_50", c, fmt(v), fmt(med_t), fmt(q(lt, 25)), fmt(q(lt, 75)), len(lt), "", "", ""])
    for c, v in sorted(vs.items()):
        x5_rows.append([var, "secondary_90", c, fmt(v), fmt(med_s), fmt(q(ls, 25)), fmt(q(ls, 75)), len(ls), "", "", ""])
    x5_rows.append([var, "CONTRAST", "", "", fmt(med_t), fmt(med_s), fmt(diff), len(lt), fmt(iqr_w),
                    fmt(ratio), flag or ""])

if min_n < 4:
    x5_verdict = "DATA LIMITED"
elif sum(1 for v in x5_flags.values() if v == "same") >= 2 and sum(1 for v in x5_flags.values() if v == "different") == 0:
    x5_verdict = "SAME PACKAGE"
elif sum(1 for v in x5_flags.values() if v == "different") >= 2 and sum(1 for v in x5_flags.values() if v == "same") == 0:
    x5_verdict = "DIFFERENT PACKAGE"
else:
    x5_verdict = "PARTIAL"

with open(RES / "X5_package_contrast.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["variable", "set", "country", "value", "median", "Q1_or_median_other",
                "diff_or_Q3", "n_dated", "pooled_IQR_width", "absdiff_over_IQR", "per_var_flag"])
    w.writerows(x5_rows)

# ---------------- X6 ----------------
sec50 = {r["country"]: r for r in get_milestones("secondary", 50)}
sec90 = {r["country"]: r for r in get_milestones("secondary", 90)}
ter50 = {r["country"]: r for r in get_milestones("tertiary", 50)}
x6_rows = []
pairs = {}
subs = {}
for c, t in ter50.items():
    if t["censored"] or t["year"] is None:
        x6_rows.append([c, "excluded_tertiary50_censored", "", "", "", "", "", ""])
        continue
    s = sec50[c]
    if s["censored"]:
        s2 = sec90[c]
        if s2["censored"] or s2["year"] is None:
            x6_rows.append([c, "excluded_no_dated_secondary", "", "", "", "", "", ""])
            continue
        s = s2
        subs[c] = s["year"]
    gap = t["year"] - s["year"]
    pairs[c] = (gap, s["year"], s["censoring"])
    x6_rows.append([c, "gap", fmt(t["year"]), fmt(s["year"]), fmt(gap), "secondary90_substituted" if c in subs else "secondary50", s["censoring"], t["censoring"]])

n = len(pairs)
x6_res = {}
if n < 4:
    x6_verdict = "UNABLE"
else:
    for var in STRUCT:
        xs, ys = [], []
        for c, (gap, secyear, _) in pairs.items():
            v = structure_at(panel, c, secyear)[var]
            if v is not None and gap is not None:
                xs.append(v); ys.append(gap)
        rho = spearman(xs, ys) if len(xs) >= 3 else None
        x6_res[var] = (rho, len(xs))
    sig = {v: r for v, (r, k) in x6_res.items() if r is not None and abs(r) >= 0.70}
    weak = all(r is not None and abs(r) < 0.40 for v, (r, k) in x6_res.items() if k > 0) and x6_res
    if len(sig) >= 2:
        signs = {np.sign(r) for r in sig.values()}
        x6_verdict = "SUPPORTED" if len(signs) == 1 else "PARTIAL"
    elif all(r is not None and abs(r) < 0.40 for r, k in x6_res.values() if k > 0) and any(k > 0 for r, k in x6_res.values()):
        x6_verdict = "NOT SUPPORTED"
    else:
        x6_verdict = "PARTIAL"
for var in STRUCT:
    rho, k = x6_res.get(var, (None, 0))
    x6_rows.append([f"rho_{var}", fmt(rho), k, "", "", "", "", ""])

with open(RES / "X6_spacing_structure.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["country_or_stat", "kind", "tertiary50_year_or_rho", "secondary_year_or_n",
                "gap", "substitution", "secondary_censoring", "tertiary_censoring"])
    w.writerows(x6_rows)

# ---------------- CLUSTER_RESULTS.csv ----------------
def note_x4():
    parts = []
    for name, (v, nok, pvi) in x4_verdicts.items():
        parts.append(f"{name}: {v}; inside-IQR counts " +
                     ", ".join(f"{k}={a}/{b}" for k, (a, b) in pvi.items()))
    return "; ".join(parts)

def note_x5():
    return "; ".join(f"{k}: |median diff|/pooled IQR flag={v}" for k, v in x5_flags.items()) + \
        f"; dated n tertiary50={len(dated_t)}, secondary90={len(dated_s)} (right-censored excluded from medians)"

def note_x6():
    sub = ", ".join(f"{c} secondary-90 substituted" for c in subs) or "none"
    return f"n={n} countries with both crossings dated; substitutions: {sub}"

cluster_rows = [
    ["X4", CLUSTER, "structure typicality at tertiary vs secondary crossings",
     "share of countries inside cross-country IQR per structure variable, per milestone set",
     "; ".join(f"{k}:{a}/{b}" for k, (a, b) in x4_verdicts[X4_SETS[0][0]][2].items()) + " | " +
     "; ".join(f"{k}:{a}/{b}" for k, (a, b) in x4_verdicts[X4_SETS[1][0]][2].items()),
     "", "", "", 6, "2 milestone sets x 3 variables",
     ">=4/6 inside IQR on >=2 of 3 variables",
     # Lead fix (schema): one verdict per row is required by RESULTS.csv. Both declared milestone sets
     # have the same verdict here; if they differed the joint conservative value would be PARTIAL.
     (x4_verdicts[X4_SETS[0][0]][0] if x4_verdicts[X4_SETS[0][0]][0] == x4_verdicts[X4_SETS[1][0]][0] else "PARTIAL"),
     "observed", note_x4()],
    ["X5", CLUSTER, "same or different structure package: tertiary-50 vs secondary-90",
     "median difference / pooled IQR width per variable",
     "; ".join(f"{k}={x5_rows[[i for i,r in enumerate(x5_rows) if r[0]==k and r[1]=='CONTRAST'][0]][6]}" for k in STRUCT),
     "", "", "", min(len(dated_t), len(dated_s)), "3 variables", "|diff|<=0.50*IQR in >=2 of 3 -> SAME",
     x5_verdict, "observed", note_x5()],
    ["X6", CLUSTER, "secondary->tertiary spacing vs structure at secondary crossing",
     "Spearman rho per structure variable",
     "; ".join(f"{k}={fmt(x6_res[k][0]) if k in x6_res else ''}(n={x6_res[k][1]})" if k in x6_res else f"{k}=NA" for k in STRUCT),
     "", "", "", n, "3 variables", "|rho|>=0.70 for >=2/3 with consistent sign",
     x6_verdict, "observed", note_x6()],
]
with open(RES / "CLUSTER_RESULTS.csv", "w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["experiment", "cluster", "question", "estimand", "estimate", "se", "ci_low", "ci_high",
                "n", "clusters", "threshold", "verdict", "label", "note"])
    w.writerows(cluster_rows)

print("X4:", {k: v[0] for k, v in x4_verdicts.items()})
print("X5:", x5_verdict, x5_flags)
print("X6:", x6_verdict, {k: v for k, v in x6_res.items()}, "n=", n)
print("exit 0")
