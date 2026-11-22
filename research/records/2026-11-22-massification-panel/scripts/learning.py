#!/usr/bin/env python3
"""APEX v1.2 [A1 2026-11-22: OWID HLO holds only HCI vintages 2010-2020, so L1 adds start year 2010 (2010->2020); gdppc_log already logged, double log removed.]
: learning outcomes (pre-registered 2026-11-22 ~18:30 CST, before any learning data were downloaded).

DOWNLOAD (all public):
  - Our World in Data: harmonized learning outcomes (Altinok, Angrist & Patrinos), long run, 5-yearly.
  - World Bank API, HCI database: HD.HCI.HLOS (harmonized test scores), HD.HCI.LAYS (learning-adjusted years),
    HD.HCI.EYRS (expected years of school), SE.LPV.PRIM (learning poverty).
  - World Bank EdStats (source 12): PISA (LO.PISA.MAT/REA/SCI), TIMSS (LO.TIMSS.MAT4/MAT8/SCI4/SCI8), PIRLS (LO.PIRLS.REA),
    and regional assessments where present (LO.SACMEQ.*, LO.PASEC.*, LO.LLECE.*). Missing codes are logged, not invented.
  SEA-PLM has no API; it is listed as a manual addition.
TESTS (associations only):
  L1 Dilution: 10-year change in harmonized learning ~ 10-year change in secondary GER + initial learning + log GDPpc +
     demographic block (start years 1985-2005, OWID HLO). Pooled and country-FE; clustered SE. Negative = expansion dilutes.
  L2 Quantity vs quality: 'schooling gap' = HD.HCI.EYRS - HD.HCI.LAYS (years of school not converted into learning).
     Association with tertiary GER level and with unemployment among the advanced-educated (credential-inflation signal),
     controlling log GDPpc. Latest year per country.
  L3 Expected vs actual learning (latest HLOS): OLS on log GDPpc, demographic block, secondary GER, urban; residuals listed for Asia.
  L4 PISA within-programme: change in PISA maths vs change in secondary NER between first and last participation (composition test).
Outputs results/learning/{findings.txt, results.json, data/*.json}.
"""
import csv, io, json, os, sys, time, urllib.request
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sweep as S

OUT = os.path.join(S.HERE, "results", "learning"); DD = os.path.join(OUT, "data")
WB = {"hlos": ("HD.HCI.HLOS", None), "lays": ("HD.HCI.LAYS", None), "eyrs": ("HD.HCI.EYRS", None), "lpov": ("SE.LPV.PRIM", None),
      "pisa_mat": ("LO.PISA.MAT", 12), "pisa_rea": ("LO.PISA.REA", 12), "pisa_sci": ("LO.PISA.SCI", 12),
      "timss_mat4": ("LO.TIMSS.MAT4", 12), "timss_mat8": ("LO.TIMSS.MAT8", 12), "timss_sci4": ("LO.TIMSS.SCI4", 12), "timss_sci8": ("LO.TIMSS.SCI8", 12),
      "pirls_rea": ("LO.PIRLS.REA", 12), "sacmeq_rea": ("LO.SACMEQ.REA", 12), "sacmeq_mat": ("LO.SACMEQ.MAT", 12),
      "pasec_mat": ("LO.PASEC.MAT.FI", 12), "pasec_rea": ("LO.PASEC.REA.FI", 12), "llece_mat6": ("LO.LLECE.MAT6", 12), "llece_rea6": ("LO.LLECE.REA6", 12)}
OWID = {"hlo_owid": "https://ourworldindata.org/grapher/average-harmonized-learning-outcome-scores.csv?v=1&csvType=full&useColumnShortNames=true"}
ASIA = S.NE_ASIA | S.SE_ASIA | S.S_ASIA | {"KHM", "PHL"}
import functools
S._series = functools.lru_cache(maxsize=None)(S._series)


def get(url, t=120):
    try:
        return urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=t).read()
    except Exception as e:
        return e


def download():
    os.makedirs(DD, exist_ok=True); log = {}
    for k, (code, src) in WB.items():
        url = f"https://api.worldbank.org/v2/country/all/indicator/{code}?format=json&per_page=20000&date=1960:2024" + (f"&source={src}" if src else "")
        raw = get(url)
        try:
            j = json.loads(raw); rows = [(d["countryiso3code"] or d["country"]["id"], int(d["date"]), d["value"]) for d in j[1] if d["value"] is not None]
        except Exception as e:
            rows = []; log[k] = f"failed: {str(raw)[:120] if isinstance(raw, Exception) else repr(e)}"
        json.dump(rows, open(os.path.join(DD, f"{k}.json"), "w")); log.setdefault(k, len(rows))
    for k, url in OWID.items():
        raw = get(url)
        if isinstance(raw, Exception):
            log[k] = f"failed: {raw}"; continue
        txt = raw.decode("utf-8", "ignore"); rd = list(csv.DictReader(io.StringIO(txt)))
        col = [c for c in rd[0] if c not in ("entity", "code", "year", "Entity", "Code", "Year")][0] if rd else None
        rows = [(r.get("code") or r.get("Code"), int(r.get("year") or r.get("Year")), float(r[col])) for r in rd if col and r.get(col) not in ("", None) and (r.get("code") or r.get("Code"))]
        json.dump(rows, open(os.path.join(DD, f"{k}.json"), "w")); open(os.path.join(DD, f"{k}.csv"), "w").write(txt); log[k] = len(rows)
    return log


def ser(k):
    p = os.path.join(DD, f"{k}.json"); out = {}
    if os.path.exists(p):
        for iso, y, v in json.load(open(p)):
            out.setdefault(iso, {})[y] = float(v)
    return out


def near(s, y, w=3):
    for d in range(w + 1):
        for yy in (y - d, y + d):
            if s and yy in s:
                return s[yy]
    return np.nan


def latest(s):
    return (max(s), s[max(s)]) if s else (None, np.nan)


def ols(X, y, g=None):
    r = S.ols_cluster(X, y, g if g is not None else np.arange(len(y)))
    return None if r is None else (r[0], r[1])


def demo(iso, y):
    vals = [near(S._series(k).get(iso), y) for k in ("fertility", "u5mr", "young_share")] + [-near(S._series("life_exp").get(iso), y)]
    return vals


def main():
    t0 = time.time(); log = json.load(open(os.path.join(OUT, 'dl_log.json'))) if '--cached' in sys.argv else download()
    json.dump(log, open(os.path.join(OUT, 'dl_log.json'), 'w')); res = {"download": log}
    hlo = ser("hlo_owid"); sec = S._series("sec"); gdp = S._series("gdppc_log"); urb = S._series("urban"); ter = S._series("ter")
    hlos = ser("hlos"); lays = ser("lays"); eyrs = ser("eyrs"); une = S._series("unemp_adv_edu"); secner = S._series("sec_ner"); pisa = ser("pisa_mat")
    # L1 dilution
    R = []
    for c, s in hlo.items():
        for t in (1985, 1990, 1995, 2000, 2005, 2010):
            l0, l1 = near(s, t, 2), near(s, t + 10, 2); e0, e1 = near(sec.get(c), t), near(sec.get(c), t + 10)
            g0 = near(gdp.get(c), t); d = demo(c, t)
            if np.isfinite([l0, l1, e0, e1, g0] + d).all() and g0 > 0:
                R.append((c, t, l1 - l0, e1 - e0, l0, g0, *d))
    if len(R) >= 40:
        A = np.array([r[2:] for r in R], float); iso = np.array([r[0] for r in R])
        dem = A[:, 4:]; dz = (dem - dem.mean(0)) / dem.std(0); dpc = dz.mean(1)
        z = lambda v: (v - v.mean()) / (v.std() or 1)
        X = np.column_stack([np.ones(len(A)), z(A[:, 1]), z(A[:, 2]), z(A[:, 3]), z(dpc)])
        r = ols(X, A[:, 0], iso)
        fe = None
        if r is not None:
            Xw = X[:, 1:].copy(); yw = A[:, 0].copy()
            for c in np.unique(iso):
                s_ = iso == c; Xw[s_] -= Xw[s_].mean(0); yw[s_] -= yw[s_].mean()
            keep = np.array([(iso == c).sum() > 1 for c in iso])
            if keep.sum() > 30:
                rf = ols(np.column_stack([np.ones(keep.sum()), Xw[keep]]), yw[keep], iso[keep]); fe = None if rf is None else dict(b=float(rf[0][1]), se=float(rf[1]))
        res["L1"] = dict(n=len(A), countries=int(len(np.unique(iso))), pooled_b_dSecGER=float(r[0][1]) if r else None, pooled_se=float(r[1]) if r else None,
                         fe=fe, note="standardized change in secondary GER; outcome = change in harmonized score points")
    else:
        res["L1"] = dict(skipped=f"n={len(R)}")
    # L2 quantity vs quality
    rows = []
    for c in set(eyrs) & set(lays):
        ye, e = latest(eyrs[c]); yl, l = latest(lays[c])
        g = near(gdp.get(c), ye); tr_ = near(ter.get(c), ye); u = near(une.get(c), ye, 5)
        if np.isfinite([e, l, g]).all() and g > 0:
            rows.append((c, e - l, g, tr_, u))
    if len(rows) > 40:
        A = np.array([r[1:] for r in rows], float); iso = np.array([r[0] for r in rows])
        out = {"n": len(A), "mean_gap_years": float(np.nanmean(A[:, 0]))}
        for j, nm in ((2, "ter_ger"), (3, "unemp_adv_edu")):
            m = np.isfinite(A[:, j]) & np.isfinite(A[:, 0])
            if m.sum() > 30:
                X = np.column_stack([np.ones(m.sum()), (A[m, j] - A[m, j].mean()) / A[m, j].std(), (A[m, 1] - A[m, 1].mean()) / A[m, 1].std()])
                r = ols(X, A[m, 0]); out[f"gap_on_{nm}"] = dict(b=float(r[0][1]), se=float(r[1]), n=int(m.sum())) if r else None
        out["asia"] = {r[0]: round(r[1], 2) for r in rows if r[0] in ASIA}
        res["L2"] = out
    # L3 expected vs actual learning
    rows = []
    for c, s in hlos.items():
        y, v = latest(s); g = near(gdp.get(c), y); e = near(sec.get(c), y); u = near(urb.get(c), y); d = demo(c, y)
        if np.isfinite([v, g, e, u] + d).all() and g > 0:
            rows.append((c, v, g, e, u, *d))
    if len(rows) > 40:
        A = np.array([r[1:] for r in rows], float); iso = [r[0] for r in rows]
        dem = A[:, 4:]; dpc = ((dem - dem.mean(0)) / dem.std(0)).mean(1)
        X = np.column_stack([np.ones(len(A)), A[:, 1], A[:, 2], A[:, 3], dpc]); b, *_ = np.linalg.lstsq(X, A[:, 0], rcond=None); pred = X @ b
        r2 = 1 - ((A[:, 0] - pred) ** 2).sum() / ((A[:, 0] - A[:, 0].mean()) ** 2).sum()
        res["L3"] = dict(n=len(A), r2=float(r2), asia={c: dict(actual=round(float(A[i, 0])), expected=round(float(pred[i])), resid=round(float(A[i, 0] - pred[i])))
                                                          for i, c in enumerate(iso) if c in ASIA})
    # L4 PISA composition
    rows = []
    for c, s in pisa.items():
        ys = sorted(s)
        if len(ys) >= 2:
            a, b2 = ys[0], ys[-1]; n0, n1 = near(secner.get(c), a), near(secner.get(c), b2)
            if np.isfinite([n0, n1]).all():
                rows.append((c, s[b2] - s[a], n1 - n0, b2 - a))
    if len(rows) > 15:
        A = np.array([r[1:] for r in rows], float)
        X = np.column_stack([np.ones(len(A)), (A[:, 1] - A[:, 1].mean()) / A[:, 1].std(), A[:, 2]]); r = ols(X, A[:, 0])
        res["L4"] = dict(n=len(A), b_dSecNER_std=float(r[0][1]) if r else None, se=float(r[1]) if r else None,
                         asia={x[0]: dict(dPISA=round(x[1], 1), dSecNER=round(x[2], 1), years=int(x[3])) for x in rows if x[0] in ASIA | {"HKG", "MAC", "SGP"}})
    json.dump(res, open(os.path.join(OUT, "results.json"), "w"), indent=1, default=float)
    L = [f"APEX v1.2 LEARNING OUTCOMES ({round(time.time() - t0)}s)", "", f"Downloads (rows or error): {json.dumps(log)}", ""]
    for k in ("L1", "L2", "L3", "L4"):
        L.append(f"{k}: {json.dumps(res.get(k), default=float)[:2500]}"); L.append("")
    L += ["SEA-PLM (2019/2024) has no API: add manually from the SEA-PLM regional reports.", "Associations only."]
    open(os.path.join(OUT, "findings.txt"), "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    main()
