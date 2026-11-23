"""Post-fit analysis: posterior summaries, held-out prediction (A vs B), tempo/quantum decomposition.
usage: analyze.py fitA.json fitB.json OUTDIR [--n 150] [--procs 24]"""
import json, sys, argparse, numpy as np
from multiprocessing import Pool
import model as M

ap = argparse.ArgumentParser(); ap.add_argument("fitA"); ap.add_argument("fitB"); ap.add_argument("out")
ap.add_argument("--n", type=int, default=150); ap.add_argument("--procs", type=int, default=24); ap.add_argument("--panel", default="data/panel.json")
args = ap.parse_args()
PAN = json.load(open(args.panel)); FIT, HOLD = PAN["FIT"], PAN["HOLD"]
GROUP = {"PHL": "EA", "THA": "EA", "CHN": "EA", "IDN": "EA", "VNM": "EA", "KOR": "EA", "MYS": "EA", "IND": "SA", "BGD": "SA", "EGY": "ME", "TUR": "ME"}
FITS = {s: json.load(open(f)) for s, f in (("A", args.fitA), ("B", args.fitB))}
DOSEG = [[0, 1], [2], [3], [4], [5, 6]]; DGN = ["none/some primary", "primary", "lower secondary", "upper secondary", "tertiary"]

def wq(x, w, q):
    i = np.argsort(x); c = np.cumsum(w[i]) / w.sum(); return float(np.interp(q, c, x[i]))

def posterior(fit):
    u = np.array(fit["u"]); w = np.array(fit["w"]); th = np.array(fit["lo"]) + u * (np.array(fit["hi"]) - np.array(fit["lo"])); res = {}
    for k, n in enumerate(fit["names"]):
        m = float((w * th[:, k]).sum()); lo, hi = wq(th[:, k], w, .05), wq(th[:, k], w, .95)
        sdp = np.sqrt((w * (th[:, k] - m) ** 2).sum()); sd0 = (fit["hi"][k] - fit["lo"][k]) / np.sqrt(12)
        res[n] = dict(mean=m, q05=lo, q50=wq(th[:, k], w, .5), q95=hi, post_over_prior_sd=float(sdp / sd0))
    return res, th, w

def particle_sets(fit, n, rng):
    u = np.array(fit["u"]); w = np.array(fit["w"]); idx = rng.choice(len(w), n, p=w)
    P = np.array(fit["lo"]) + u[idx] * (np.array(fit["hi"]) - np.array(fit["lo"])); f = np.array(fit["f"])[idx]
    return P, f, idx

def fhold(f_row, iso):
    g = GROUP.get(iso); mem = [k for k, c in enumerate(FIT) if GROUP.get(c) == g]
    return float(np.mean(f_row[mem])) if g and mem else float(np.mean(f_row))

def holdout_job(job):
    scen, P, f_row, seed, iso, oracle = job; pc = PAN["countries"][iso]
    fs = [fhold(f_row, iso)] if not oracle else [-.9, -.3, .3, .9]
    best = None
    for f in fs:
        S = M.summaries(M.simulate(pc, P, 0 if scen == "A" else 1, seed, f, nW=24)); d, parts = M.distance(S, pc)
        if best is None or d < best[0]: best = (d, parts, S, f)
    d, parts, S, f = best
    errs = {}
    for g, key in (("tfr", "tfr"), ("asfr", "asfr1519"), ("smam", "smam"), ("m18", "m18")):
        e = [(S[g][int(y)] - v) for y, v in pc[key].items() if int(y) <= 2012 and not np.isnan(S[g].get(int(y), np.nan))]
        errs[g] = e
    paths = {int(y): S["tfr"][int(y)] for y in pc["tfr"]}
    return dict(scen=scen, iso=iso, D=d, parts=parts, errs=errs, tfr_path=paths, f=f, oracle=oracle)

def decomp_job(job):
    scen, P, f_row, seed, iso = job; pc = PAN["countries"][iso]
    f = f_row[FIT.index(iso)] if iso in FIT else fhold(f_row, iso)
    out = M.simulate(pc, P, 0 if scen == "A" else 1, seed, f, nW=24, tmax=2050)
    return scen, iso, out[7]

if __name__ == "__main__":
    rng = np.random.default_rng(7); R = {"posterior": {}}
    for s in "AB":
        R["posterior"][s], _, _ = posterior(FITS[s])
        R.setdefault("in_sample_D", {})[s] = dict(best=float(min(FITS[s]["D"])), median=float(np.median(FITS[s]["D"])), hist=FITS[s]["hist"])
    pool = Pool(args.procs); parts = {s: particle_sets(FITS[s], args.n, rng) for s in "AB"}
    # ---- held-out prediction (and fit countries' in-sample reference with same machinery)
    jobs = []
    for s in "AB":
        P, f, _ = parts[s]
        for i in range(args.n):
            for iso in HOLD: jobs.append((s, P[i], f[i], 1000 + i, iso, False))
    res = pool.map(holdout_job, jobs, chunksize=4)
    # oracle country effect (structural fit, not a prediction) on a smaller subset
    jobs_o = [(s, parts[s][0][i], parts[s][1][i], 5000 + i, iso, True) for s in "AB" for i in range(40) for iso in HOLD]
    res_o = pool.map(holdout_job, jobs_o, chunksize=4)
    H = {}
    for tag, rr in (("predicted", res), ("oracle_f", res_o)):
        H[tag] = {}
        for s in "AB":
            H[tag][s] = {}
            for iso in HOLD:
                x = [r for r in rr if r["scen"] == s and r["iso"] == iso]
                H[tag][s][iso] = dict(D_mean=float(np.mean([r["D"] for r in x])), D_sd=float(np.std([r["D"] for r in x])),
                    rmse={g: float(np.sqrt(np.mean([e ** 2 for r in x for e in r["errs"][g]]))) if any(r["errs"][g] for r in x) else None for g in ("tfr", "asfr", "smam", "m18")},
                    tfr_path_mean={y: float(np.mean([r["tfr_path"][y] for r in x])) for y in x[0]["tfr_path"]})
    R["holdout"] = H
    # paired comparison on predicted D: bootstrap over particles within country, average over countries
    Dm = {s: np.array([[r["D"] for r in res if r["scen"] == s and r["iso"] == iso] for iso in HOLD]) for s in "AB"}   # [country, particle]
    diff = Dm["A"].mean(1) - Dm["B"].mean(1)
    boots = [np.mean([rng.choice(Dm["A"][k], len(Dm["A"][k])).mean() - rng.choice(Dm["B"][k], len(Dm["B"][k])).mean() for k in rng.integers(0, len(HOLD), len(HOLD))]) for _ in range(2000)]
    R["holdout_compare"] = dict(countries=HOLD, D_A=Dm["A"].mean(1).tolist(), D_B=Dm["B"].mean(1).tolist(), mean_D_A=float(Dm["A"].mean()), mean_D_B=float(Dm["B"].mean()),
        diff_A_minus_B=float(diff.mean()), boot_q025=float(np.quantile(boots, .025)), boot_q975=float(np.quantile(boots, .975)),
        countries_A_better=int((diff < 0).sum()))
    # ensemble-mean TFR RMSE
    ens = {}
    for s in "AB":
        e = []
        for iso in HOLD:
            pr = H["predicted"][s][iso]["tfr_path_mean"]; e += [(pr[y] - PAN["countries"][iso]["tfr"][str(y)]) for y in pr]
        ens[s] = float(np.sqrt(np.mean(np.square(e))))
    R["holdout_compare"]["ensemble_tfr_rmse"] = ens
    # ---- in-sample country fit (best particles)
    # ---- decomposition (both scenarios, all countries)
    nd = 60; jobs = [(s, parts[s][0][i], parts[s][1][i], 9000 + i, iso) for s in "AB" for i in range(nd) for iso in FIT + HOLD]
    dres = pool.map(decomp_job, jobs, chunksize=4)
    COHS = M.COH
    def agg(sel):
        acc = np.zeros((len(COHS), 5, 8))
        for _, iso, coh in sel:
            for g, lv in enumerate(DOSEG): acc[:, g, :] += coh[:, lv, :].sum(1)
        return acc
    DEC = {}
    for s in "AB":
        for label, isos in (("fit", FIT), ("holdout", HOLD)):
            per = []
            for i in range(nd):
                sel = [d for (j, d) in zip(jobs, dres) if j[0] == s and j[3] == 9000 + i and d[1] in isos]
                a = agg(sel); w = a[:, :, 0]
                with np.errstate(all="ignore"):
                    cf = a[:, :, 3] / w; b30 = a[:, :, 1] / w; b35 = a[:, :, 2] / w; chl = a[:, :, 4] / w; evm = a[:, :, 5] / w; afb = a[:, :, 6] / a[:, :, 7]
                # national (all dose groups pooled)
                tw = w.sum(1); ncf = (a[:, :, 3].sum(1)) / tw; nb35 = a[:, :, 2].sum(1) / tw; nev = a[:, :, 5].sum(1) / tw; nchl = a[:, :, 4].sum(1) / tw
                per.append(dict(cf=cf, b30=b30, b35=b35, chl=chl, evm=evm, afb=afb, share=w / tw[:, None], ncf=ncf, nb35=nb35, nev=nev, nchl=nchl))
            ref = COHS.index(1940)
            def stat(k, f):
                arr = np.array([f(p) for p in per]); return np.nanmean(arr, 0), np.nanquantile(arr, .05, 0), np.nanquantile(arr, .95, 0)
            out = {}
            for name in ("cf", "b30", "b35", "chl", "evm", "afb", "share"): out[name] = {k: v.tolist() for k, v in zip(("mean", "q05", "q95"), stat(name, lambda p, n=name: p[n]))}
            # decline decomposition relative to the 1940 cohort, by dose group and nationally
            def dec(p, late):
                L = COHS.index(late); res = {}
                for g in range(5):
                    dcf = p["cf"][ref, g] - p["cf"][L, g]; db35 = p["b35"][ref, g] - p["b35"][L, g]
                    res[DGN[g]] = [dcf, db35 - dcf]            # quantum (fewer births by 49), tempo (births postponed beyond 35, still born by 49)
                dcf = p["ncf"][ref] - p["ncf"][L]; db35 = p["nb35"][ref] - p["nb35"][L]; res["national"] = [dcf, db35 - dcf]
                res["national_never_married_change"] = [(1 - p["nev"][L]) - (1 - p["nev"][ref]), 0]
                return res
            out["decomp"] = {}
            for late in (1960, 1970, 1980, 1990):
                dd = [dec(p, late) for p in per]
                out["decomp"][str(late)] = {k: dict(quantum=float(np.nanmean([d[k][0] for d in dd])), tempo=float(np.nanmean([d[k][1] for d in dd])),
                    quantum_q05=float(np.nanquantile([d[k][0] for d in dd], .05)), quantum_q95=float(np.nanquantile([d[k][0] for d in dd], .95)),
                    tempo_q05=float(np.nanquantile([d[k][1] for d in dd], .05)), tempo_q95=float(np.nanquantile([d[k][1] for d in dd], .95))) for k in dd[0]}
            DEC[f"{s}_{label}"] = out
    R["decomposition"] = dict(cohorts=COHS, dose_groups=DGN, results=DEC, reference_cohort=1940)
    json.dump(R, open(f"{args.out}/analysis.json", "w"), indent=1, default=float)
    print("A vs B held-out:", R["holdout_compare"])
