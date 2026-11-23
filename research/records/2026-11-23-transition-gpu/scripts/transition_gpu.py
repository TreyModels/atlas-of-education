"""Full demographic transition in the GPU dose engine, and the mortality counterfactual.

MODEL EXTENSION, NOT THE PUBLISHED MODEL.  Two additions, both labelled and separately switchable:
  1. cohorts are placed on a configurable base (here 1890-1955, reproductive years 1905-2004) instead of
     the published 1930-1999;
  2. a child-mortality channel: desired births respond to the prevailing child mortality with a coefficient
     estimated from the country-level data (births per woman per point of child mortality per 100),
     measured against the calibration-era child mortality.  With the coefficient at zero the engine is the
     published model bit for bit (trans/test_port.py still passes: state diff 0, targets 0.0).
The historical paths (child mortality, income, urban share, mean schooling) come from un-data's
research/records/2026-11-23-transition/data/long_run_panel.csv.

Constructed inputs (documented assumptions, not data): pre-1930 schooling is built from mean years of
schooling by a normal-latent mapping onto the seven levels, because Barro-Lee starts in 1950; the publisher's
income series (2015 US$ logs) is matched to Maddison 1990-international logs by their mean difference over
1950-2010.
"""
import json, os, sys, time, argparse
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dosecore as dc
from engine import GPUDose, make_spec
from scipy.stats import norm

ap = argparse.ArgumentParser()
ap.add_argument("--panel", default="data/panel.json")
ap.add_argument("--longrun", default="/root/work/transition_gpu/long_run_panel.csv")
ap.add_argument("--out", default="../results/transition.json")
ap.add_argument("--nW", type=int, default=500)
ap.add_argument("--coh0", type=int, default=1890)
ap.add_argument("--gy0", type=int, default=1900)
ap.add_argument("--bcm", type=float, default=0.0067, help="births per woman per point of child mortality/100")
ap.add_argument("--band", type=float, default=0.5, help="fractional sensitivity band on bcm")
ap.add_argument("--cmref", type=float, default=5.0)
ap.add_argument("--scen", default="A", choices=["A","B"], help="individuation (A) or development-only (B)")
ap.add_argument("--force-bcm", type=float, default=None, help="override the coefficient (power check)")
ap.add_argument("--fit", default="/root/work/dose_gpu/results/rej_fitA.json", help="use the weighted posterior medians of this fit as the parameter vector")
ap.add_argument("--tmax", type=int, default=2010)
a = ap.parse_args()
PAN = json.load(open(a.panel))
FIT = PAN["FIT"]
NC = 14; NGY = 126
LEVEL_YEARS = np.array([0., 3., 6., 9., 12., 14., 16.])   # the model's seven schooling levels


def load_longrun(path):
    out = {}
    with open(path) as f:
        hdr = f.readline().strip().split(",")
        ix = {k: i for i, k in enumerate(hdr)}
        for line in f:
            p = line.rstrip("\n").split(",")
            iso = p[ix["iso3"]]; y = int(p[ix["year"]])
            def g(k):
                v = p[ix[k]]
                return float(v) if v not in ("", "NA") else None
            out.setdefault(iso, {})[y] = dict(cm=g("child_mortality_per100"), le=g("life_expectancy_years"),
                                              ef=g("effective_fertility"), mys=g("mean_years_schooling"),
                                              gdp=g("gdp_pc_maddison_1990int"), urb=g("urban_share_pct"))
    return out


def series(d, years, key):
    ys = sorted(y for y in d if d[y][key] is not None)
    if not ys: return None
    v = np.array([d[y][key] for y in ys], float)
    return np.interp(years, ys, v, left=v[0], right=v[-1])


def school_shares(mys):
    """mean years of schooling -> shares of the seven levels, normal latent with sd 3.0 (an assumption)."""
    if mys is None or not np.isfinite(mys): mys = 2.0
    cuts = np.concatenate([[0.], LEVEL_YEARS[1:]]) if False else None
    # level k covers years [LEVEL_YEARS[k], LEVEL_YEARS[k+1]); the last is open-ended
    edges = np.array([0., 3., 6., 9., 12., 14., 16.])
    cdf = norm.cdf((edges - mys) / 3.0)
    sh = np.diff(np.concatenate([[0.], cdf[1:], [1.]]))
    sh = np.clip(sh, 1e-6, None); return sh / sh.sum()


def build_country(iso, LR, ref_gdp_log, cm_override=None):
    d = LR[iso]; years = np.arange(a.gy0, a.gy0 + NGY)
    cm = series(d, years, "cm")
    gdp_m = series(d, years, "gdp")
    urb = series(d, years, "urb")
    mys_s = series(d, years, "mys")
    gdp_log = np.log(np.clip(gdp_m, 1.0, None)) + ref_gdp_log
    shF, shM, urbl = [], [], []
    for c in range(NC):
        y0 = a.coh0 + 5 * c
        i = int(np.clip(y0 + 15 - a.gy0, 0, NGY - 1))
        s = school_shares(mys_s[i] if mys_s is not None else None)
        shF.append(s.tolist()); shM.append(s.tolist())
        urbl.append(float(np.clip((urb[i] if urb is not None else 30.0) / 100.0, 0.03, 0.97)))
    cmv = cm if cm_override is None else np.full(NGY, float(cm_override))
    pc = dict(shF=shF, shM=shM, urban=urbl, gdp=gdp_log.tolist(), age_gap=3.0,
              tfr={}, asfr1519={}, smam={}, m18={}, panel_thresholds={}, region="")
    return pc, cmv


if __name__ == "__main__":
    LR = load_longrun(a.longrun)
    # parameter vector: weighted posterior medians of the fitted scenario-A population, so the transition
    # run uses the model as fitted to the observed data rather than a half-prior guess.
    P = (dc.LO + dc.HI) / 2
    if os.path.exists(a.fit):
        fit = json.load(open(a.fit))
        u = np.array(fit["u"]); w = np.array(fit["w"]); lo = np.array(fit["lo"]); hi = np.array(fit["hi"])
        th = lo + u * (hi - lo)
        for k, n in enumerate(fit["names"]):
            i = np.argsort(th[:, k]); c = np.cumsum(w[i]) / w.sum()
            P[dc.IX[n]] = float(np.interp(.5, c, th[i, k]))
        print("parameter vector: posterior medians from", a.fit, flush=True)
    else:
        print("parameter vector: prior midpoints (no fit file)", flush=True)
    # rescale Maddison logs to the published income scale using the overlap 1950-2010
    offs = []
    for iso in FIT:
        d = LR[iso]; yrs = [y for y in range(1950, 2011) if y in d and d[y]["gdp"]]
        if not yrs: continue
        madd = np.array([np.log(d[y]["gdp"]) for y in yrs])
        pubb = np.array([PAN["countries"][iso]["gdp"][y - 1925] for y in yrs])
        offs.append(np.mean(pubb - madd))
    ref_off = float(np.mean(offs)) if offs else 0.0
    print("income-scale offset (published log minus Maddison log):", round(ref_off, 3), flush=True)
    countries, specs, meta = [], [], []
    for iso in FIT:
        pc, cm = build_country(iso, LR, ref_off)
        cm_pre = float(np.mean([LR[iso][y]["cm"] for y in range(1800, 1851) if y in LR[iso] and LR[iso][y]["cm"]]))
        countries.append(iso)
        for arm, cmv in (("history", cm), ("frozen", np.full(NGY, cm_pre))):
            for bc, tag in ((a.bcm * (1 - a.band), "lo"), (a.bcm, "mid"), (a.bcm * (1 + a.band), "hi")):
                if a.force_bcm is not None: bc, tag = a.force_bcm, "forced"
                specs.append(dict(prep=dc.prepare(pc, P, 0 if a.scen == "A" else 1, 1234, len(specs), gy0=a.gy0), P=P, fc=0.0,
                                  gap=3.0, cm=cmv.tolist(), bcm=bc, cmref=a.cmref))
                meta.append(dict(iso=iso, arm=arm, band=tag, bcm=bc, cm_pre=cm_pre))
    print("runs:", len(specs), "women per run:", 28 * 5 * a.nW, "total women:", len(specs) * 28 * 5 * a.nW, flush=True)
    eng = GPUDose(nW=a.nW, seed=7, max_runs=len(specs), tmax=a.tmax)
    eng.coh0 = a.coh0; eng.gy0 = a.gy0; eng.my0 = a.coh0; eng.t0 = a.gy0 + 15
    t0 = time.time(); eng.load(specs); acc = eng.run(0 if a.scen == "A" else 1); wall = time.time() - t0
    coh = acc["coh"]                                     # [run, 14, 7, 8]
    births, expo = acc["births"], acc["expo"]            # [run, 101, 35]
    with np.errstate(all="ignore"):
        rr = births / expo
        tfr_year = np.where((expo > 0).all(-1), np.nansum(np.where(expo > 0, rr, 0.0), axis=-1), np.nan)
    years_abs = list(range(1950, 1951 + 100))
    women = len(specs) * 28 * 5 * a.nW
    res = dict(tfr_years=years_abs,
               tfr=[[[None if np.isnan(v) else float(v) for v in tfr_year[i]] for i in range(acc["births"].shape[0])]][0],
               scen=a.scen, coh0=a.coh0, gy0=a.gy0, tmax=a.tmax, nW=a.nW, women=women, runs=len(specs),
               woman_years=women * 35, wall_sec=wall, throughput_women_per_sec=women / wall,
               cohorts=[a.coh0 + 5 * c for c in range(NC)], meta=meta,
               rows=[])
    for i, m in enumerate(meta):
        w = coh[i][:, :, 0].sum(); births = coh[i][:, :, 3].sum(); nev = coh[i][:, :, 4].sum()
        by30 = coh[i][:, :, 1].sum()
        wc = coh[i][:, :, 0].sum(1)                     # weight by cohort
        cf = coh[i][:, :, 3].sum(1) / np.maximum(wc, 1e-9)
        c30 = coh[i][:, :, 1].sum(1) / np.maximum(wc, 1e-9)
        cnv = coh[i][:, :, 4].sum(1) / np.maximum(wc, 1e-9)
        res["rows"].append(dict(iso=m["iso"], arm=m["arm"], band=m["band"], bcm=m["bcm"],
                                births_by_49=float(births / max(w, 1e-9)),
                                births_by_30=float(by30 / max(w, 1e-9)),
                                childless=float(nev / max(w, 1e-9)),
                                cohort_fertility=cf.tolist(), cohort_births_by_30=c30.tolist(),
                                cohort_childless=cnv.tolist(), cm_pre=m["cm_pre"]))
    json.dump(res, open(a.out, "w"), indent=1)
    print("wall %.2fs, %.0f women/s, %.2fM women, %.0fM woman-years" % (wall, women / wall, women / 1e6, women * 35 / 1e6), flush=True)
    print("wrote", a.out, flush=True)
