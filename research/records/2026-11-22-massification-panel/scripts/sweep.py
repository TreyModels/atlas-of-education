#!/usr/bin/env python3
"""Wide regression sweep (extreme-bounds / Sala-i-Martin style) with a discovery/confirmation split.
PRE-REGISTERED DESIGN (fixed 2026-11-22 ~16:30 CST, before any data were fetched for it):

Unit: country x start-year t in {1975,1980,...,2010}. Outcome = change over the next 10 years in
  ter = tertiary GER, sec = secondary GER, lsc = lower-secondary completion rate.
Each regression: dY ~ X_t (focus, standardized) + Y_t + decade dummies + up to 2 other predictors at t
  (all pairs from the pool). OLS, country-clustered SEs. Kept if n >= 120 rows and >= 25 countries.
Per (outcome, X): share of regressions with the modal sign, share |t|>1.96 with modal sign,
  Sala-i-Martin CDF(0) (likelihood-weighted normal mass on the modal side), median standardized coef.
Split: countries split once at random (seed 20261122, stratified by region) into DISCOVERY and CONFIRMATION.
  A predictor is ROBUST if CDF(0) >= 0.95 with the same sign in BOTH halves; FRAGILE otherwise.
Groups (focus + base + each single other predictor, all countries in group):
  all, asia (East Asia & Pacific + South Asia), ne_asia, se_asia, s_asia, non_asia,
  early_massifier (tertiary GER >= 15% by 1990), late_massifier (crossed after 1990), not_yet,
  over_complex / under_complex (country-mean ECI percentile minus GDP-pc percentile > +0.15 / < -0.15),
  resource_state (mean natural-resource rents > 10% GDP).
Lead-lag: for each (outcome, X): b1 from dY(t->t+10) ~ X_t + Y_t + decade, b2 from dX(t->t+10) ~ Y_t + X_t + decade.
  'X leads' if b1 significant and b2 not; 'Y leads' the reverse; 'both' / 'neither' otherwise.
Interpretation rule: associations only. Nothing here is causal; it screens candidate mechanisms for the engine.

  python sweep.py fetch      python sweep.py run [--workers 20]
"""
import argparse, csv, io, json, os, sys, time, urllib.request
from itertools import combinations
from multiprocessing import Pool
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "data_sweep"); OUT = os.path.join(HERE, "results", "sweep")
OUTCOMES = {"ter": "SE.TER.ENRR", "sec": "SE.SEC.ENRR", "lsc": "SE.SEC.CMPT.LO.ZS"}
BLOCKS = {
  "schooling": {"pre_ger": "SE.PRE.ENRR", "prm_ner": "SE.PRM.NENR", "prm_cmp": "SE.PRM.CMPT.ZS", "sec_ner": "SE.SEC.NENR",
                "ptr_prm": "SE.PRM.ENRL.TC.ZS", "ptr_sec": "SE.SEC.ENRL.TC.ZS", "edu_xpd_gdp": "SE.XPD.TOTL.GD.ZS",
                "edu_xpd_gov": "SE.XPD.TOTL.GB.ZS", "priv_prm": "SE.PRM.PRIV.ZS", "priv_sec": "SE.SEC.PRIV.ZS",
                "gpi_sec": "SE.ENR.SECO.FM.ZS", "gpi_ter": "SE.ENR.TERT.FM.ZS", "repeat_prm": "SE.PRM.REPT.ZS"},
  "skills": {"hci": "HD.HCI.OVRL", "test_scores": "HD.HCI.HLOS", "lit_adult": "SE.ADT.LITR.ZS", "lab_adv_edu": "SL.TLF.ADVN.ZS",
             "unemp_adv_edu": "SL.UEM.ADVN.ZS", "unemp_basic_edu": "SL.UEM.BASC.ZS"},
  "employment": {"emp_agri": "SL.AGR.EMPL.ZS", "emp_ind": "SL.IND.EMPL.ZS", "emp_srv": "SL.SRV.EMPL.ZS", "wage_emp": "SL.EMP.WORK.ZS",
                 "vuln_emp": "SL.EMP.VULN.ZS", "employers": "SL.EMP.MPYR.ZS", "unemp": "SL.UEM.TOTL.ZS", "unemp_youth": "SL.UEM.1524.ZS",
                 "flfp": "SL.TLF.CACT.FE.ZS", "neet": "SL.UEM.NEET.ZS", "child_work": "SL.TLF.0714.ZS"},
  "economy": {"gdppc_log": "NY.GDP.PCAP.KD", "growth": "NY.GDP.PCAP.KD.ZG", "agri_va": "NV.AGR.TOTL.ZS", "manuf_va": "NV.IND.MANF.ZS",
              "srv_va": "NV.SRV.TOTL.ZS", "exports": "NE.EXP.GNFS.ZS", "fdi": "BX.KLT.DINV.WD.GD.ZS", "remit": "BX.TRF.PWKR.DT.GD.ZS",
              "rents": "NY.GDP.TOTL.RT.ZS", "gini": "SI.POV.GINI", "poverty": "SI.POV.DDAY", "inflation": "FP.CPI.TOTL.ZG",
              "hitech_exp": "TX.VAL.TECH.MF.ZS", "investment": "NE.GDI.TOTL.ZS", "hh_cons": "NE.CON.PRVT.ZS"},
  "state": {"tax": "GC.TAX.TOTL.GD.ZS", "gov_cons": "NE.CON.GOVT.ZS", "gov_xpn": "GC.XPN.TOTL.GD.ZS", "military": "MS.MIL.XPND.GD.ZS",
            "birth_reg": "SP.REG.BRTH.ZS", "electricity": "EG.ELC.ACCS.ZS", "internet": "IT.NET.USER.ZS", "debt_service": "DT.TDS.DECT.GN.ZS",
            "gov_eff": "GE.EST@3", "reg_quality": "RQ.EST@3", "rule_law": "RL.EST@3", "corruption": "CC.EST@3"},
  "demography": {"urban": "SP.URB.TOTL.IN.ZS", "fertility": "SP.DYN.TFRT.IN", "young_share": "SP.POP.0014.TO.ZS", "life_exp": "SP.DYN.LE00.IN",
                 "u5mr": "SH.DYN.MORT", "pop_log": "SP.POP.TOTL"},
}
LOGS = {"gdppc_log", "pop_log"}
STARTS = list(range(1975, 2011, 5)); H = 10
NE_ASIA = {"CHN", "HKG", "MAC", "JPN", "KOR", "PRK", "MNG"}
SE_ASIA = {"BRN", "KHM", "IDN", "LAO", "MYS", "MMR", "PHL", "SGP", "THA", "VNM", "TLS"}
S_ASIA = {"AFG", "BGD", "BTN", "IND", "MDV", "NPL", "PAK", "LKA"}


def _get(url, tries=4):
    for i in range(tries):
        try:
            with urllib.request.urlopen(urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"}), timeout=180) as r:
                return r.read()
        except Exception as e:
            print("  retry", i, url[:100], e, flush=True); time.sleep(4)
    return None


def fetch():
    os.makedirs(DATA, exist_ok=True)
    allvars = dict(OUTCOMES); [allvars.update(b) for b in BLOCKS.values()]
    for k, code in allvars.items():
        fn = os.path.join(DATA, f"{k}.json")
        if os.path.exists(fn):
            continue
        c, src = (code.split("@") + [None])[:2]
        url = f"https://api.worldbank.org/v2/country/all/indicator/{c}?format=json&per_page=20000&date=1960:2024" + (f"&source={src}" if src else "")
        raw = _get(url)
        try:
            j = json.loads(raw); rows = [(d["countryiso3code"], int(d["date"]), d["value"]) for d in j[1] if d["value"] is not None and d["countryiso3code"]]
        except Exception as e:
            print("FAILED", k, code, e); rows = []
        json.dump(rows, open(fn, "w")); print(f"{k:16s} {code:22s} {len(rows)}", flush=True)
    meta = json.loads(_get("https://api.worldbank.org/v2/country?format=json&per_page=400"))
    json.dump({d["id"]: dict(region=d["region"]["value"], income=d["incomeLevel"]["value"]) for d in meta[1]},
              open(os.path.join(DATA, "meta.json"), "w"))
    eci_src = os.path.join(HERE, "data", "eci_owid_rank.csv")   # reuse takeoff download (OEC ranks 1964-2016)
    if os.path.exists(eci_src):
        rd = list(csv.DictReader(open(eci_src)))
        col = [c for c in rd[0] if "eci" in c.lower()][0]
        byy = {}
        for r in rd:
            if r[col]:
                byy.setdefault(int(r["year"]), []).append((r["code"], float(r[col])))
        rows = [(iso, y, 1 - (rk - 1) / max(len(v) - 1, 1)) for y, v in byy.items() for iso, rk in v]
        json.dump(rows, open(os.path.join(DATA, "eci_pct.json"), "w")); print("eci_pct", len(rows))


def _series(k):
    out = {}
    for iso, y, v in json.load(open(os.path.join(DATA, f"{k}.json"))):
        out.setdefault(iso, {})[y] = float(v)
    return out


def _near(s, y, w=2):
    """value at year y, else nearest within +-w years (no interpolation beyond that)."""
    if s is None:
        return np.nan
    for d in range(w + 1):
        for yy in (y - d, y + d):
            if yy in s:
                return s[yy]
    return np.nan


def build():
    meta = json.load(open(os.path.join(DATA, "meta.json")))
    preds = {}
    for b in BLOCKS.values():
        preds.update(b)
    names = [k for k in preds if os.path.getsize(os.path.join(DATA, f"{k}.json")) > 50]
    if os.path.exists(os.path.join(DATA, "eci_pct.json")):
        names.append("eci_pct")
    S = {k: _series(k) for k in names}; Y = {o: _series(o) for o in OUTCOMES}
    isos = [i for i, m in meta.items() if m["region"] != "Aggregates"]
    rows = []
    for iso in isos:
        for t in STARTS:
            r = dict(iso=iso, t=t, region=meta[iso]["region"])
            for o in OUTCOMES:
                y0, y1 = _near(Y[o].get(iso), t), _near(Y[o].get(iso), t + H)
                r[f"{o}_0"], r[f"d_{o}"] = y0, y1 - y0
            for k in names:
                v = _near(S[k].get(iso), t)
                r[k] = np.log(v) if (k in LOGS and v > 0) else v
                v1 = _near(S[k].get(iso), t + H)
                r[f"dx_{k}"] = (np.log(v1) if (k in LOGS and v1 > 0) else v1) - r[k]
            rows.append(r)
    return rows, names, meta


def groups(rows, names, meta):
    by = {}
    for r in rows:
        by.setdefault(r["iso"], []).append(r)
    ter = _series("ter"); g = {}
    asia_regions = {"East Asia & Pacific", "South Asia"}
    for iso, rs in by.items():
        reg = rs[0]["region"]; tags = ["all"]
        tags.append("asia" if reg in asia_regions else "non_asia")
        if iso in NE_ASIA: tags.append("ne_asia")
        if iso in SE_ASIA: tags.append("se_asia")
        if iso in S_ASIA: tags.append("s_asia")
        tser = ter.get(iso, {}); cross = min([y for y, v in tser.items() if v >= 15] or [9999])
        tags.append("early_massifier" if cross <= 1990 else ("late_massifier" if cross < 9999 else "not_yet"))
        rents = [r["rents"] for r in rs if "rents" in r and np.isfinite(r["rents"])]
        if rents and np.mean(rents) > 10: tags.append("resource_state")
        g[iso] = tags
    # complexity mismatch: country mean ECI percentile minus GDP-pc percentile (cross-section of country means)
    if "eci_pct" in names:
        m_e = {i: np.nanmean([r["eci_pct"] for r in rs]) for i, rs in by.items()}
        m_g = {i: np.nanmean([r["gdppc_log"] for r in rs]) for i, rs in by.items()}
        ok = [i for i in by if np.isfinite(m_e[i]) and np.isfinite(m_g[i])]
        gr = {i: k / max(len(ok) - 1, 1) for k, i in enumerate(sorted(ok, key=lambda i: m_g[i]))}
        er = {i: k / max(len(ok) - 1, 1) for k, i in enumerate(sorted(ok, key=lambda i: m_e[i]))}
        for i in ok:
            d = er[i] - gr[i]
            if d > 0.15: g[i].append("over_complex")
            if d < -0.15: g[i].append("under_complex")
    return g


def ols_cluster(X, y, cl):
    XtX = X.T @ X
    try:
        inv = np.linalg.inv(XtX)
    except np.linalg.LinAlgError:
        return None
    b = inv @ (X.T @ y); e = y - X @ b
    u, idx = np.unique(cl, return_inverse=True)
    S = np.zeros((len(u), X.shape[1])); np.add.at(S, idx, X * e[:, None])
    G = len(u); n, k = X.shape
    V = inv @ (S.T @ S) @ inv * (G / max(G - 1, 1)) * ((n - 1) / max(n - k, 1))
    ll = -0.5 * n * np.log(max(e @ e / n, 1e-12))
    return b, np.sqrt(max(V[1, 1], 1e-18)), ll


# globals for workers
P = None


def _prep(rows, names):
    A = {k: np.array([r.get(k, np.nan) for r in rows], float) for k in names}
    for o in OUTCOMES:
        A[f"{o}_0"] = np.array([r[f"{o}_0"] for r in rows], float); A[f"d_{o}"] = np.array([r[f"d_{o}"] for r in rows], float)
    for k in names:
        A[f"dx_{k}"] = np.array([r[f"dx_{k}"] for r in rows], float)
    iso = np.array([r["iso"] for r in rows]); t = np.array([r["t"] for r in rows])
    dec = np.column_stack([(t >= d) & (t < d + 10) for d in (1985, 1995, 2005)]).astype(float)
    return dict(A=A, iso=iso, dec=dec)


def _z(v, m):
    s = v[m].std(); return (v - v[m].mean()) / (s if s > 0 else 1)


def _reg(o, x, extras, mask_rows):
    A = P["A"]; y = A[f"d_{o}"]
    cols = [x, f"{o}_0"] + list(extras)
    m = mask_rows & np.isfinite(y)
    for c in cols:
        m &= np.isfinite(A[c])
    n = int(m.sum())
    if n < 120 or len(np.unique(P["iso"][m])) < 25:
        return None
    X = np.column_stack([np.ones(n), _z(A[x], m)[m]] + [_z(A[c], m)[m] for c in cols[1:]] + [P["dec"][m]])
    r = ols_cluster(X, y[m], P["iso"][m])
    return None if r is None else (r[0][1], r[1], r[2], n)


def _summ(res):
    res = [r for r in res if r is not None]
    if len(res) < 5:
        return None
    b = np.array([r[0] for r in res]); se = np.array([r[1] for r in res]); ll = np.array([r[2] for r in res])
    sign = 1.0 if np.median(b) >= 0 else -1.0
    w = np.exp(ll - ll.max()); w /= w.sum()
    from math import erf, sqrt
    cdf = float(np.sum(w * np.array([0.5 * (1 + erf(sign * bi / (si * sqrt(2)))) for bi, si in zip(b, se)])))
    return dict(n_regs=len(res), median_coef=float(np.median(b)), modal_sign=int(sign), share_modal_sign=float(np.mean(np.sign(b) == sign)),
                share_sig_modal=float(np.mean((np.abs(b / se) > 1.96) & (np.sign(b) == sign))), cdf0=cdf, median_n=int(np.median([r[3] for r in res])))


def _job_full(args):
    o, x, pool, half = args
    m = P["half_mask"][half]
    return (o, x, half, _summ([_reg(o, x, ex, m) for ex in combinations([p for p in pool if p != x], 2)]))


def _job_group(args):
    o, x, pool, gname = args
    m = P["group_mask"][gname]
    return (o, x, gname, _summ([_reg(o, x, (ex,), m) for ex in pool if ex != x] + [_reg(o, x, (), m)]))


def _job_leadlag(args):
    o, x = args
    A = P["A"]; m0 = np.ones(len(P["iso"]), bool)
    r1 = _reg(o, x, (), m0)
    # reverse: dX ~ Y_t + X_t
    y = A[f"dx_{x}"]; m = m0 & np.isfinite(y) & np.isfinite(A[f"{o}_0"]) & np.isfinite(A[x]); n = int(m.sum())
    r2 = None
    if n >= 120 and len(np.unique(P["iso"][m])) >= 25:
        X = np.column_stack([np.ones(n), _z(A[f"{o}_0"], m)[m], _z(A[x], m)[m], P["dec"][m]])
        rr = ols_cluster(X, y[m], P["iso"][m]); r2 = None if rr is None else (rr[0][1], rr[1])
    s1 = r1 is not None and abs(r1[0] / r1[1]) > 1.96; s2 = r2 is not None and abs(r2[0] / r2[1]) > 1.96
    verdict = "x_leads" if s1 and not s2 else "y_leads" if s2 and not s1 else "both" if s1 and s2 else "neither"
    return (o, x, dict(b_x_to_dy=None if r1 is None else float(r1[0]), t1=None if r1 is None else float(r1[0] / r1[1]),
                        b_y_to_dx=None if r2 is None else float(r2[0]), t2=None if r2 is None else float(r2[0] / r2[1]), verdict=verdict))


def _init(p):
    global P
    P = p


def run(workers):
    os.makedirs(OUT, exist_ok=True)
    rows, names, meta = build()
    g = groups(rows, names, meta)
    p = _prep(rows, names)
    iso = p["iso"]; regions = {i: meta[i]["region"] for i in set(iso)}
    rng = np.random.default_rng(20261122); half = {}
    for reg in sorted(set(regions.values())):
        cs = sorted(i for i in set(iso) if regions[i] == reg); rng.shuffle(cs)
        for k, c in enumerate(cs):
            half[c] = "discovery" if k % 2 == 0 else "confirmation"
    p["half_mask"] = {h: np.array([half[i] == h for i in iso]) for h in ("discovery", "confirmation")}
    gnames = ["all", "asia", "ne_asia", "se_asia", "s_asia", "non_asia", "early_massifier", "late_massifier", "not_yet", "over_complex", "under_complex", "resource_state"]
    p["group_mask"] = {gn: np.array([gn in g.get(i, []) for i in iso]) for gn in gnames}
    # usable predictors: >= 300 non-missing rows
    pool = [k for k in names if np.isfinite(p["A"][k]).sum() >= 300]
    t0 = time.time()
    with Pool(workers, initializer=_init, initargs=(p,)) as pl:
        full = pl.map(_job_full, [(o, x, pool, h) for o in OUTCOMES for x in pool for h in ("discovery", "confirmation")], chunksize=1)
        grp = pl.map(_job_group, [(o, x, pool, gn) for o in OUTCOMES for x in pool for gn in gnames], chunksize=4)
        ll = pl.map(_job_leadlag, [(o, x) for o in OUTCOMES for x in pool], chunksize=8)
    block_of = {k: b for b, d in BLOCKS.items() for k in d}; block_of["eci_pct"] = "economy"
    F = {}
    for o, x, h, s in full:
        F.setdefault((o, x), {})[h] = s
    table = []
    for (o, x), d in F.items():
        a, b = d.get("discovery"), d.get("confirmation")
        robust = bool(a and b and a["cdf0"] >= 0.95 and b["cdf0"] >= 0.95 and a["modal_sign"] == b["modal_sign"])
        table.append(dict(outcome=o, var=x, block=block_of.get(x), robust=robust,
                          disc_sign=a and a["modal_sign"], disc_cdf0=a and round(a["cdf0"], 3), disc_coef=a and round(a["median_coef"], 3), disc_regs=a and a["n_regs"],
                          conf_sign=b and b["modal_sign"], conf_cdf0=b and round(b["cdf0"], 3), conf_coef=b and round(b["median_coef"], 3), conf_regs=b and b["n_regs"]))
    G = {}
    for o, x, gn, s in grp:
        if s:
            G.setdefault(gn, []).append(dict(outcome=o, var=x, block=block_of.get(x), **{k: (round(v, 3) if isinstance(v, float) else v) for k, v in s.items()}))
    LL = [dict(outcome=o, var=x, block=block_of.get(x), **d) for o, x, d in ll]
    json.dump(dict(pool=pool, groups_membership={k: sorted(i for i in g if k in g[i]) for k in gnames}, full=table, by_group=G, leadlag=LL,
                   seconds=round(time.time() - t0)), open(os.path.join(OUT, "results.json"), "w"), indent=1, default=float)
    with open(os.path.join(OUT, "robust_table.csv"), "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0])); w.writeheader(); w.writerows(table)
    findings(table, G, LL, pool, g)


def findings(table, G, LL, pool, g):
    L = [f"WIDE SWEEP: {len(pool)} predictors, outcomes = 10-yr change in tertiary GER (ter), secondary GER (sec), lower-sec completion (lsc).",
         "ROBUST = Sala-i-Martin CDF(0) >= 0.95, same sign, in BOTH the discovery and confirmation halves of countries.", ""]
    for o in OUTCOMES:
        rob = sorted([r for r in table if r["outcome"] == o and r["robust"]], key=lambda r: -abs(r["disc_coef"] or 0))
        L.append(f"[{o}] robust predictors ({len(rob)} of {sum(1 for r in table if r['outcome'] == o)}):")
        for r in rob[:20]:
            L.append(f"   {'+' if r['disc_sign'] > 0 else '-'} {r['var']:16s} ({r['block']:10s}) coef disc {r['disc_coef']:+.2f} / conf {r['conf_coef']:+.2f}  cdf {r['disc_cdf0']}/{r['conf_cdf0']}")
        frag = [r for r in table if r["outcome"] == o and not r["robust"] and r["disc_cdf0"] and r["disc_cdf0"] >= 0.95]
        L.append(f"   discovery-only (failed to replicate): " + ", ".join(sorted(r["var"] for r in frag)[:25]))
        L.append("")
    for gn in ("asia", "se_asia", "ne_asia", "s_asia", "early_massifier", "late_massifier", "over_complex", "under_complex", "resource_state"):
        rs = G.get(gn, [])
        n_c = sum(1 for i in g if gn in g[i])
        L.append(f"<{gn}> ({n_c} countries) strongest stable associations (cdf0 >= 0.95, sign stable in >= 90% of specs):")
        for o in OUTCOMES:
            top = sorted([r for r in rs if r["outcome"] == o and r["cdf0"] >= 0.95 and r["share_modal_sign"] >= 0.9], key=lambda r: -abs(r["median_coef"]))[:8]
            L.append(f"   {o}: " + ", ".join(f"{'+' if r['modal_sign'] > 0 else '-'}{r['var']}({r['median_coef']:+.1f})" for r in top))
        L.append("")
    L.append("LEAD-LAG (all countries): which moves first?")
    for o in OUTCOMES:
        xs = [r for r in LL if r["outcome"] == o and r["verdict"] == "x_leads"]
        ys = [r for r in LL if r["outcome"] == o and r["verdict"] == "y_leads"]
        L.append(f"   {o}: X leads enrolment: " + ", ".join(sorted(r["var"] for r in xs)))
        L.append(f"   {o}: enrolment leads X:  " + ", ".join(sorted(r["var"] for r in ys)))
    L += ["", "Associations only. Group results are not split-validated (groups are small); treat them as hypotheses."]
    open(os.path.join(OUT, "findings.txt"), "w").write("\n".join(L) + "\n"); print("\n".join(L))


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument("cmd"); ap.add_argument("--workers", type=int, default=max(1, (os.cpu_count() or 2) - 1))
    a = ap.parse_args()
    fetch() if a.cmd == "fetch" else run(a.workers)
