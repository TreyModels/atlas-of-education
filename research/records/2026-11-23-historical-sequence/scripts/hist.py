"""Quantify the schooling vs structural-change sequence for four historical cases from the project's own
long-run panel (mean years of schooling and urban share, 1750-2024).  See DEFINITIONS.md."""
import csv, json
import numpy as np
SRC = "/root/work/transition/out/long_run_panel.csv"
rows = list(csv.DictReader(open(SRC)))
data = {}
for r in rows:
    iso = r["iso3"]
    if iso not in ("GBR", "FRA", "USA", "DEU"): continue
    y = int(r["year"])
    def g(k):
        v = r.get(k, "")
        try: return float(v)
        except Exception: return np.nan
    data.setdefault(iso, {})[y] = dict(sch=g("mean_years_schooling"), urb=g("urban_share_pct"),
                                       cm=g("child_mortality_per100"), tfr=g("effective_fertility"))

def takeoff(series, threshold, horizon=30):
    """First year whose rise over the next `horizon` years is at least `threshold` and not reversed."""
    ys = sorted(y for y in series if np.isfinite(series[y]))
    out = None
    for i, y in enumerate(ys):
        fut = [yy for yy in ys if y <= yy <= y + horizon]
        if not fut or fut[-1] < y + horizon - 5: continue
        vals = [series[yy] for yy in fut if np.isfinite(series[yy])]
        if len(vals) < 5: continue
        rise = vals[-1] - vals[0]
        if rise >= threshold and min(vals[vals.index(vals[0]):]) >= vals[0] - 0.15 * max(rise, 1e-9):
            out = int(y); break
    return out

res = {}
for iso, d in data.items():
    sch = {y: v["sch"] for y, v in d.items()}
    urb = {y: v["urb"] for y, v in d.items()}
    s1 = takeoff(sch, 1.0)     # +1 year of schooling within 30 years
    s2 = takeoff(sch, 2.0)     # a sharper +2 years
    u1 = takeoff(urb, 10.0)    # +10 percentage points of urban share within 30 years
    u2 = takeoff(urb, 20.0)
    res[iso] = dict(sch_plus1=s1, sch_plus2=s2, urb_plus10=u1, urb_plus20=u2,
                    sch_1800=round(sch.get(1800, float("nan")), 2) if 1800 in sch else None,
                    sch_1850=round(sch.get(1850, float("nan")), 2) if 1850 in sch else None,
                    sch_1900=round(sch.get(1900, float("nan")), 2) if 1900 in sch else None,
                    urb_1800=round(urb.get(1800, float("nan")), 1) if 1800 in urb else None,
                    urb_1850=round(urb.get(1850, float("nan")), 1) if 1850 in urb else None,
                    urb_1900=round(urb.get(1900, float("nan")), 1) if 1900 in urb else None)
print("case | schooling +1yr within 30y | +2yr | urban +10pp | urban +20pp | lead (schooling yr - urban yr)")
for iso, r in res.items():
    lead = (r["sch_plus1"] - r["urb_plus20"]) if r["sch_plus1"] and r["urb_plus20"] else None
    print("%s | %s | %s | %s | %s | %s" % (iso, r["sch_plus1"], r["sch_plus2"], r["urb_plus10"], r["urb_plus20"], lead))
print("\nlevels:")
for iso, r in res.items():
    print(" ", iso, {k: r[k] for k in ("sch_1800","sch_1850","sch_1900","urb_1800","urb_1850","urb_1900")})
json.dump(res, open("/root/work/hist_seq/sequence_from_panel.json", "w"), indent=1)
