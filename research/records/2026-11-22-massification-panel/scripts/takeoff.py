#!/usr/bin/env python3
"""Cross-national takeoff test of the triad / surplus-motor boot-up claim. Pre-registered in PROTOCOL_takeoff.md.

Claim tested: tertiary massification 'boots up' only when household means, employer demand (productive
capabilities) and state capacity are ALL present; any one alone, or two, is not enough.

  python takeoff.py fetch          download WDI + ECI into data/ (needs internet)
  python takeoff.py run [--boot 2000 --thr 1000 --workers 20]
Outputs: results/takeoff/{panel.csv, results.json, findings.txt}
"""
import argparse, io, json, os, sys, time, urllib.request
from multiprocessing import Pool
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data"); OUT = os.path.join(HERE, "results", "takeoff")
WDI = {"ter": "SE.TER.ENRR", "sec": "SE.SEC.ENRR", "gdppc": "NY.GDP.PCAP.KD", "agri_va": "NV.AGR.TOTL.ZS",
       "govcons": "NE.CON.GOVT.ZS", "tax": "GC.TAX.TOTL.GD.ZS", "urban": "SP.URB.TOTL.IN.ZS"}
TROW = 15.0          # tertiary GER threshold for 'mass' (Trow 1973)
LAG = 5              # conditions measured 5 years before
YEARS = (1965, 2024)
CASES = ["PHL", "KHM", "HKG", "KOR", "THA", "VNM", "IDN", "MYS", "CHN", "IND"]


# ------------------------------------------------------------------ data
def _get(url, tries=3):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=120) as r:
                return r.read()
        except Exception as e:
            print("  retry", i, url[:90], e, flush=True); time.sleep(3)
    raise RuntimeError("failed " + url)


def fetch():
    os.makedirs(DATA, exist_ok=True)
    for k, code in WDI.items():
        j = json.loads(_get(f"https://api.worldbank.org/v2/country/all/indicator/{code}?format=json&per_page=20000&date={YEARS[0]-10}:{YEARS[1]}"))
        rows = [(d["countryiso3code"], int(d["date"]), d["value"]) for d in j[1] if d["value"] is not None and d["countryiso3code"]]
        json.dump(rows, open(os.path.join(DATA, f"wdi_{k}.json"), "w")); print(k, len(rows), flush=True)
    meta = json.loads(_get("https://api.worldbank.org/v2/country?format=json&per_page=400"))
    json.dump({d["id"]: d["region"]["value"] for d in meta[1]}, open(os.path.join(DATA, "regions.json"), "w"))
    # ECI: Harvard Growth Lab dataverse (Growth Projections & Complexity Rankings), else OWID ranks (1964-2016)
    got = False
    try:
        ds = json.loads(_get("https://dataverse.harvard.edu/api/datasets/:persistentId/?persistentId=doi:10.7910/DVN/XTAQMC"))
        for f in ds["data"]["latestVersion"]["files"]:
            df = f["dataFile"]; name = df.get("filename", "")
            if name.endswith((".csv", ".tab")) or "eci" in name.lower() or "rank" in name.lower():
                raw = _get(f"https://dataverse.harvard.edu/api/access/datafile/{df['id']}?format=original")
                open(os.path.join(DATA, "eci_" + name.replace("/", "_")), "wb").write(raw); print("ECI file", name, len(raw)); got = True
    except Exception as e:
        print("dataverse ECI failed:", e)
    try:
        raw = _get("https://ourworldindata.org/grapher/economic-complexity-rankings.csv?v=1&csvType=full&useColumnShortNames=true")
        open(os.path.join(DATA, "eci_owid_rank.csv"), "wb").write(raw); print("OWID ECI rank", len(raw)); got = True
    except Exception as e:
        print("OWID ECI failed:", e)
    print("ECI obtained" if got else "NO ECI: employer leg will use non-agricultural share of GDP")


def _load_wdi(k):
    p = os.path.join(DATA, f"wdi_{k}.json")
    out = {}
    for iso, y, v in json.load(open(p)):
        out.setdefault(iso, {})[y] = float(v)
    return out


def _load_eci():
    """Return {iso: {year: eci}} from the longest-coverage ECI column found; ranks are converted to -rank."""
    import csv
    best, best_n, label = {}, 0, None
    for fn in os.listdir(DATA):
        if not fn.startswith("eci_"):
            continue
        txt = open(os.path.join(DATA, fn), encoding="utf-8", errors="ignore").read()
        delim = "\t" if fn.endswith(".tab") else ","
        rd = list(csv.DictReader(io.StringIO(txt), delimiter=delim))
        if not rd:
            continue
        cols = rd[0].keys()
        isoc = next((c for c in cols if c.lower() in ("code", "iso3", "country_code", "location_code", "iso", "country_iso3_code", "iso3_code")), None)
        yc = next((c for c in cols if c.lower() == "year"), None)
        if not isoc or not yc:
            continue
        for c in cols:
            cl = c.lower()
            if ("eci" in cl or "complexity" in cl or "rank" in cl) and c not in (isoc, yc):
                d = {}
                for r in rd:
                    try:
                        v = float(r[c]); d.setdefault(r[isoc].strip().upper(), {})[int(float(r[yc]))] = (-v if "rank" in cl else v)
                    except Exception:
                        pass
                if "rank" in cl:   # A1: raw ranks shrink with the number of ranked countries; use within-year percentile
                    byy = {}
                    for iso_, yv in d.items():
                        for y_, v_ in yv.items():
                            byy.setdefault(y_, []).append(-v_)
                    d = {iso_: {y_: 1 - (-v_ - 1) / max(len(byy[y_]) - 1, 1) for y_, v_ in yv.items()} for iso_, yv in d.items()}
                n = sum(len(v) for v in d.values())
                yrs = [y for v in d.values() for y in v]
                score = n + (5000 if yrs and min(yrs) < 1990 else 0) + (2000 if "rank" not in cl else 0)
                if score > best_n:
                    best, best_n, label = d, score, f"{fn}:{c}"
    return best, label


def _interp(series, years):
    """Linear interpolation inside observed range only (no extrapolation)."""
    if not series:
        return np.full(len(years), np.nan)
    ys = np.array(sorted(series)); vs = np.array([series[y] for y in ys])
    out = np.interp(years, ys, vs); out[(years < ys[0]) | (years > ys[-1])] = np.nan
    return out


def build_panel():
    W = {k: _load_wdi(k) for k in WDI}
    eci, eci_label = _load_eci()
    regions = json.load(open(os.path.join(DATA, "regions.json")))
    yrs = np.arange(YEARS[0] - LAG, YEARS[1] + 1)
    panel = []
    for iso in W["ter"]:
        if regions.get(iso, "Aggregates") == "Aggregates":
            continue
        ter = _interp(W["ter"].get(iso, {}), yrs)
        cond = dict(H=np.log(_interp(W["gdppc"].get(iso, {}), yrs)),
                    E=_interp(eci.get(iso, {}), yrs) if eci else np.nan * yrs,
                    E_alt=100 - _interp(W["agri_va"].get(iso, {}), yrs),
                    S=_interp(W["govcons"].get(iso, {}), yrs),
                    S_alt=_interp(W["tax"].get(iso, {}), yrs))
        obs_ter = W["ter"].get(iso, {})
        for i, y in enumerate(yrs):
            if y < YEARS[0]:
                continue
            j = i - LAG
            rec = dict(iso=iso, year=int(y), region=regions.get(iso), ter=float(ter[i]), ter_observed=int(y) in obs_ter)
            for k, v in cond.items():
                rec[k] = float(v[j]) if j >= 0 else np.nan
            panel.append(rec)
    return panel, eci_label


def risk_set(panel):
    """Country-years at risk of tertiary takeoff: before the first year GER >= TROW, after a first observation < TROW.
    event = 1 in the first year GER crosses TROW (interpolated series)."""
    by = {}
    for r in panel:
        by.setdefault(r["iso"], []).append(r)
    risk, takeoffs = [], {}
    for iso, rs in by.items():
        rs.sort(key=lambda r: r["year"]); seen_below = False
        for r in rs:
            if not np.isfinite(r["ter"]):
                continue
            if r["ter"] < TROW:
                seen_below = True; risk.append(dict(r, event=0))
            elif seen_below:
                risk.append(dict(r, event=1)); takeoffs[iso] = r["year"]; break
            else:
                break   # already above threshold at first observation: left-censored, excluded
    return risk, takeoffs


# ------------------------------------------------------------------ models
def logit(X, y, iters=50, ridge=1e-4):
    b = np.zeros(X.shape[1])
    for _ in range(iters):
        p = 1 / (1 + np.exp(-np.clip(X @ b, -30, 30)))
        g = X.T @ (y - p) - ridge * b
        H = (X * (p * (1 - p))[:, None]).T @ X + ridge * np.eye(len(b))
        step = np.linalg.solve(H, g); b += step
        if np.max(np.abs(step)) < 1e-8:
            break
    p = 1 / (1 + np.exp(-np.clip(X @ b, -30, 30)))
    cov = np.linalg.pinv((X * (p * (1 - p))[:, None]).T @ X)
    return b, np.sqrt(np.diag(cov)), p


def design(rows, model, thr, Ekey="E", Skey="S"):
    z = lambda k: np.array([r[k] for r in rows])
    H, E, S = z("H"), z(Ekey), z(Skey)
    h, e, s = (H >= thr[0]).astype(float), (E >= thr[1]).astype(float), (S >= thr[2]).astype(float)
    yr = z("year").astype(float); dec = [(yr >= d) & (yr < d + 10) for d in (1975, 1985, 1995, 2005, 2015)]
    base = [np.ones(len(rows))] + [x.astype(float) for x in dec]
    std = lambda v, k: (v - MU[k]) / SD[k]
    cols = {"H": base + [std(H, "H")],
            "add": base + [std(H, "H"), std(E, Ekey), std(S, Skey)],
            "conj": base + [h * e * s],
            "add_conj": base + [std(H, "H"), std(E, Ekey), std(S, Skey), h * e * s],
            "count": base + [((h + e + s) == k).astype(float) for k in (1, 2, 3)]}[model]
    return np.column_stack(cols)


MU, SD = {}, {}
MODELS = ["H", "add", "conj", "add_conj", "count"]


def cv_logloss(rows, thr, folds=10, seed=0, Ekey="E", Skey="S"):
    isos = sorted({r["iso"] for r in rows}); rng = np.random.default_rng(seed); rng.shuffle(isos)
    fold = {iso: i % folds for i, iso in enumerate(isos)}
    y = np.array([r["event"] for r in rows], float); out = {}
    for m in MODELS:
        X = design(rows, m, thr, Ekey, Skey); ll = np.zeros(len(rows))
        for f in range(folds):
            te = np.array([fold[r["iso"]] == f for r in rows]); tr = ~te
            b, _, _ = logit(X[tr], y[tr])
            p = np.clip(1 / (1 + np.exp(-(X[te] @ b))), 1e-6, 1 - 1e-6)
            ll[te] = -(y[te] * np.log(p) + (1 - y[te]) * np.log(1 - p))
        out[m] = float(ll.mean())
    return out


def _boot(args):
    rows, thr, seed, Ekey, Skey = args
    rng = np.random.default_rng(seed)
    by = {}
    for r in rows:
        by.setdefault(r["iso"], []).append(r)
    isos = list(by); samp = [r for i in rng.choice(len(isos), len(isos)) for r in by[isos[i]]]
    y = np.array([r["event"] for r in samp], float)
    b1, _, _ = logit(design(samp, "add_conj", thr, Ekey, Skey), y)
    b2, _, _ = logit(design(samp, "count", thr, Ekey, Skey), y)
    return float(b1[-1]), float(b2[-1] - b2[-2]), float(b2[-2] - b2[-3])   # conj coef; log-odds jump 2->3; jump 1->2


def _thr_draw(args):
    rows, seed, Ekey, Skey = args
    rng = np.random.default_rng(seed); q = rng.uniform(30, 70, 3)
    thr = [np.nanpercentile([r[k] for r in rows], qq) for k, qq in zip(("H", Ekey, Skey), q)]
    y = np.array([r["event"] for r in rows], float)
    b, se, _ = logit(design(rows, "add_conj", thr, Ekey, Skey), y)
    return float(b[-1]), float(b[-1] / se[-1]), q.tolist()


def run(nboot, nthr, workers):
    os.makedirs(OUT, exist_ok=True)
    panel, eci_label = build_panel()
    risk, takeoffs = risk_set(panel)
    results = dict(eci_source=eci_label, trow=TROW, lag=LAG)
    for spec, (Ek, Sk) in {"main_ECI_govcons": ("E", "S"), "alt_nonagri_govcons": ("E_alt", "S"), "alt_ECI_tax": ("E", "S_alt")}.items():
        rows = [r for r in risk if all(np.isfinite(r[k]) for k in ("H", Ek, Sk))]
        if len(rows) < 200 or sum(r["event"] for r in rows) < 15:
            results[spec] = dict(skipped=f"too few rows ({len(rows)}) or events"); continue
        for k in ("H", Ek, Sk):
            v = np.array([r[k] for r in rows]); MU[k], SD[k] = float(v.mean()), float(v.std() or 1)
        thr = [float(np.median([r[k] for r in rows])) for k in ("H", Ek, Sk)]
        y = np.array([r["event"] for r in rows], float)
        fits = {}
        for m in MODELS:
            b, se, _ = logit(design(rows, m, thr, Ek, Sk), y)
            fits[m] = dict(coef_tail=b[6:].tolist(), se_tail=se[6:].tolist())
        cv = cv_logloss(rows, thr, Ekey=Ek, Skey=Sk)
        # Ragin-style necessity / sufficiency at median thresholds
        ev = [r for r in rows if r["event"] == 1]
        pres = lambda r, i, k: r[k] >= thr[i]
        necessity = {nm: float(np.mean([pres(r, i, k) for r in ev])) for i, (nm, k) in enumerate((("H", "H"), ("E", Ek), ("S", Sk)))}
        necessity["all3"] = float(np.mean([all(pres(r, i, k) for i, k in enumerate(("H", Ek, Sk))) for r in ev]))
        cnt = np.array([sum(pres(r, i, k) for i, k in enumerate(("H", Ek, Sk))) for r in rows])
        hazard_by_count = {int(c): dict(n=int((cnt == c).sum()), events=int(y[cnt == c].sum()),
                                        rate=float(y[cnt == c].mean()) if (cnt == c).any() else None) for c in range(4)}
        with Pool(workers) as pool:
            boots = pool.map(_boot, [(rows, thr, 7000 + i, Ek, Sk) for i in range(nboot)])
            thrd = pool.map(_thr_draw, [(rows, 9000 + i, Ek, Sk) for i in range(nthr)])
        B = np.array(boots); T = np.array([t[:2] for t in thrd])
        results[spec] = dict(
            n_rows=len(rows), n_countries=len({r["iso"] for r in rows}), n_takeoffs=int(y.sum()), thresholds_median=thr,
            cv_logloss=cv, cv_best=min(cv, key=cv.get), cv_conj_beats_add=cv["add_conj"] < cv["add"],
            fits=fits, necessity_share_of_takeoffs_with_condition_present=necessity, hazard_by_number_of_conditions=hazard_by_count,
            bootstrap=dict(n=nboot, conj_coef_ci90=np.percentile(B[:, 0], [5, 50, 95]).tolist(), share_conj_coef_pos=float((B[:, 0] > 0).mean()),
                           jump_2to3_ci90=np.percentile(B[:, 1], [5, 50, 95]).tolist(), jump_1to2_ci90=np.percentile(B[:, 2], [5, 50, 95]).tolist(),
                           share_accelerating=float((B[:, 1] > B[:, 2]).mean())),
            threshold_mc=dict(n=nthr, share_conj_coef_pos=float((T[:, 0] > 0).mean()), share_conj_z_gt_1_645=float((T[:, 1] > 1.645).mean()),
                              median_conj_coef=float(np.median(T[:, 0]))))
    # case timelines: first year each condition crossed the (main-spec) median threshold, and takeoff year
    main = results.get("main_ECI_govcons", {})
    if "thresholds_median" in main:
        thr = main["thresholds_median"]; cases = {}
        for iso in CASES:
            rs = sorted([r for r in panel if r["iso"] == iso], key=lambda r: r["year"])
            first = lambda k, t: next((r["year"] for r in rs if np.isfinite(r[k]) and r[k] >= t), None)
            last_ter = next((r["ter"] for r in reversed(rs) if np.isfinite(r["ter"])), None)
            cases[iso] = dict(H_cross_year=first("H", thr[0]), E_cross_year=first("E", thr[1]), S_cross_year=first("S", thr[2]),
                              note="cross years are for conditions measured 5 years earlier", takeoff_year=takeoffs.get(iso),
                              latest_ter_ger=last_ter)
        results["cases"] = cases
    # lock-in: after takeoff, does tertiary GER fall >= 25% within 5 years when a condition drops below threshold?
    results["lockin"] = lockin(panel, takeoffs, main.get("thresholds_median"))
    json.dump(results, open(os.path.join(OUT, "results.json"), "w"), indent=2, default=float)
    write_findings(results)


def lockin(panel, takeoffs, thr):
    if not thr:
        return None
    by = {}
    for r in panel:
        by.setdefault(r["iso"], {})[r["year"]] = r
    stats = {"condition_dropped": [0, 0], "no_drop": [0, 0]}
    for iso, t0 in takeoffs.items():
        d = by[iso]
        for y in range(t0 + 1, YEARS[1] - 4):
            if y not in d or y + 5 not in d or not np.isfinite(d[y]["ter"]) or not np.isfinite(d[y + 5]["ter"]):
                continue
            vals = [d[y + 5][k] for k in ("H", "E", "S")]
            if not all(np.isfinite(vals)):
                continue
            dropped = any(v < t for v, t in zip(vals, thr))
            reversal = d[y + 5]["ter"] <= 0.75 * d[y]["ter"]
            key = "condition_dropped" if dropped else "no_drop"
            stats[key][0] += 1; stats[key][1] += int(reversal)
    return {k: dict(country_years=v[0], reversals=v[1], rate=(v[1] / v[0] if v[0] else None)) for k, v in stats.items()}


def write_findings(R):
    L = [f"TAKEOFF TEST. Takeoff = first year tertiary GER crosses {TROW}% (Trow). Conditions measured {LAG} years earlier.",
         f"ECI source: {R.get('eci_source')}", ""]
    for spec in ("main_ECI_govcons", "alt_nonagri_govcons", "alt_ECI_tax"):
        s = R.get(spec, {})
        if "skipped" in s or not s:
            L.append(f"[{spec}] skipped: {s.get('skipped')}"); continue
        L += [f"[{spec}] {s['n_countries']} countries, {s['n_rows']} country-years at risk, {s['n_takeoffs']} takeoffs",
              "  out-of-sample log loss (lower=better, 10-fold by country): " + ", ".join(f"{k}={v:.4f}" for k, v in s["cv_logloss"].items()),
              f"  best = {s['cv_best']}; conjunction adds to additive model out of sample: {s['cv_conj_beats_add']}",
              "  takeoff rate by number of conditions present (0-3): " + ", ".join(f"{k}:{v['events']}/{v['n']}" for k, v in s["hazard_by_number_of_conditions"].items()),
              "  share of takeoffs with condition present: " + ", ".join(f"{k}={v:.0%}" for k, v in s["necessity_share_of_takeoffs_with_condition_present"].items()),
              f"  bootstrap ({s['bootstrap']['n']}): conjunction coef 90% CI {[round(x, 2) for x in s['bootstrap']['conj_coef_ci90']]}, positive in {s['bootstrap']['share_conj_coef_pos']:.0%}",
              f"     log-odds jump 2->3 conditions {[round(x, 2) for x in s['bootstrap']['jump_2to3_ci90']]} vs 1->2 {[round(x, 2) for x in s['bootstrap']['jump_1to2_ci90']]}; accelerating in {s['bootstrap']['share_accelerating']:.0%}",
              f"  threshold Monte Carlo ({s['threshold_mc']['n']} draws, 30th-70th pct): conjunction coef positive in {s['threshold_mc']['share_conj_coef_pos']:.0%}, z>1.645 in {s['threshold_mc']['share_conj_z_gt_1_645']:.0%}", ""]
    if R.get("cases"):
        L.append("Cases (year condition crossed main median threshold, measured 5 yrs earlier; takeoff year):")
        for k, v in R["cases"].items():
            L.append(f"  {k}: H {v['H_cross_year']}  E {v['E_cross_year']}  S {v['S_cross_year']}  takeoff {v['takeoff_year']}  latest tertiary GER {v['latest_ter_ger']}")
    if R.get("lockin"):
        L.append("Lock-in (post-takeoff, tertiary GER falls >=25% within 5 yrs): " + json.dumps(R["lockin"]))
    L += ["", "Read: the boot-up claim predicts (1) add_conj or count beats add out of sample, (2) the 2->3 jump exceeds 1->2,",
          "(3) nearly all takeoffs happen with all three present, (4) few reversals even when a condition later drops."]
    open(os.path.join(OUT, "findings.txt"), "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd")
    ap.add_argument("--boot", type=int, default=2000); ap.add_argument("--thr", type=int, default=1000)
    ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 2))
    a = ap.parse_args()
    fetch() if a.cmd == "fetch" else run(a.boot, a.thr, a.workers)
