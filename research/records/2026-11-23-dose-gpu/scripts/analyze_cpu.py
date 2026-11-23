"""Posterior summaries, convergence diagnostics, A-vs-B held-out comparison and tempo/quantum
decomposition for the CPU-original ABC campaign (the headline engine).
usage: analyze_cpu.py --dir results [--what posterior|holdout|decomp|all]
Every section writes its own JSON, so a partial analysis is always usable.
"""
import json, os, sys, argparse, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import model as M
from multiprocessing import Pool

ap = argparse.ArgumentParser()
ap.add_argument("--dir", default="../results"); ap.add_argument("--panel", default="data/panel.json")
ap.add_argument("--procs", type=int, default=6); ap.add_argument("--what", default="all")
ap.add_argument("--nhold", type=int, default=150); ap.add_argument("--ndec", type=int, default=60)
a = ap.parse_args()
D = a.dir
REPORT = ["th_k", "th_f", "kappa", "gam", "lam_s"]
PRETTY = {"th_k": "kin-support loss per full dose of schooling",
          "th_f": "downward money flow per full dose (desired family size)",
          "kappa": "cohort deepening (extra independence at same dose, later cohorts)",
          "gam": "career-first delay added by one unit of independence (years)",
          "lam_s": "marriage-market pickiness per unit of independence"}
GROUP = {"PHL": "EA", "THA": "EA", "CHN": "EA", "IDN": "EA", "VNM": "EA", "KOR": "EA", "MYS": "EA",
         "IND": "SA", "BGD": "SA", "EGY": "ME", "TUR": "ME"}


def wq(x, w, q):
    i = np.argsort(x); c = np.cumsum(w[i]) / w.sum(); return float(np.interp(q, c, x[i]))


def load(scen):
    p = os.path.join(D, f"cpu_fit{scen}.json")
    return json.load(open(p)) if os.path.exists(p) else None


def posterior(fit):
    u = np.array(fit["u"]); w = np.array(fit["w"])
    lo, hi = np.array(fit["lo"]), np.array(fit["hi"]); th = lo + u * (hi - lo)
    out = {}
    for k, n in enumerate(fit["names"]):
        m = float((w * th[:, k]).sum()); sd = float(np.sqrt((w * (th[:, k] - m) ** 2).sum()))
        sd0 = (hi[k] - lo[k]) / np.sqrt(12)
        out[n] = dict(q05=wq(th[:, k], w, .05), q50=wq(th[:, k], w, .5), q95=wq(th[:, k], w, .95),
                      mean=m, sd=sd, prior_sd=sd0, post_over_prior_sd=sd / sd0,
                      truth_prior=(float(lo[k]), float(hi[k])))
    return out, th, w, u


def diagnostics(fit):
    w = np.array(fit["w"]); Dd = np.array(fit["D"]); hist = fit["hist"]
    ess = float(1.0 / np.sum(w ** 2)); n = len(w)
    # drift of the population across rounds: best and median distance, tolerance schedule
    rounds = [dict(round=h["round"], n=h["n"], eps=h["eps"], best=h["best"],
                   median_kept=h["median_kept"], elapsed=h["elapsed"]) for h in hist]
    # is the population concentrated on a few particles?
    top = float(np.sort(w)[::-1][:10].sum())
    # distance vs weight rank: did the tolerance actually bite?
    return dict(kept=n, ess=ess, ess_over_n=ess / n, weight_top10=top,
                best=float(Dd.min()), median=float(np.median(Dd)), tolerance=float(Dd.max()),
                rounds=rounds,
                # simple convergence flag: last tolerance vs second-last best
                last_eps=rounds[-1]["eps"] if rounds else None,
                rounds_completed=len(rounds))


def fhold(f_row, iso, FIT):
    g = GROUP.get(iso); mem = [k for k, c in enumerate(FIT) if GROUP.get(c) == g]
    return float(np.mean([f_row[m] for m in mem])) if g and mem else float(np.mean(f_row))


def particle_sets(fit, n, rng):
    u = np.array(fit["u"]); w = np.array(fit["w"]); idx = rng.choice(len(w), n, p=w)
    P = np.array(fit["lo"]) + u[idx] * (np.array(fit["hi"]) - np.array(fit["lo"]))
    return P, np.array(fit["f"])[idx]


def holdout_job(job):
    scen, P, f_row, seed, iso = job
    pc = PAN["countries"][iso]; f = fhold(f_row, iso, FIT)
    S = M.summaries(M.simulate(pc, P, 0 if scen == "A" else 1, seed, f, nW=24))
    d, _ = M.distance(S, pc)
    errs = {g: [(S[g][int(y)] - v) for y, v in pc[key].items()
                if int(y) <= 2012 and not np.isnan(S[g].get(int(y), np.nan))]
            for g, key in (("tfr", "tfr"), ("asfr", "asfr1519"), ("smam", "smam"), ("m18", "m18"))}
    return dict(scen=scen, iso=iso, D=d, errs=errs,
                tfr_path={int(y): S["tfr"][int(y)] for y in pc["tfr"]})


def decomp_job(job):
    scen, P, f_row, seed, iso = job
    pc = PAN["countries"][iso]; f = fhold(f_row, iso, FIT) if iso not in FIT else f_row[FIT.index(iso)]
    out = M.simulate(pc, P, 0 if scen == "A" else 1, seed, f, nW=24, tmax=2050)
    return scen, iso, out[7]


if __name__ == "__main__":
    PAN = json.load(open(a.panel)); FIT, HOLD = PAN["FIT"], PAN["HOLD"]
    A, B = load("A"), load("B")
    R = {}
    if a.what in ("posterior", "all") and A:
        post, _, _, _ = posterior(A)
        R["posterior_A"] = {n: post[n] for n in A["names"]}
        R["diag_A"] = diagnostics(A)
        lines = ["# Scenario A posteriors and convergence diagnostics (CPU original, headline engine)", ""]
        lines.append(f"draws kept {R['diag_A']['kept']}; effective sample size {R['diag_A']['ess']:.0f} "
                     f"({100 * R['diag_A']['ess_over_n']:.0f}% of kept); rounds completed {R['diag_A']['rounds_completed']}")
        lines.append("")
        for h in R["diag_A"]["rounds"]:
            lines.append(f"- round {h['round']}: {h['n']} draws, kept-best {h['best']:.3f}, tolerance {h['eps']:.3f}, {h['elapsed']:.0f}s")
        lines += ["", "| parameter | 5% | median | 95% | posterior sd / prior sd |", "|---|---|---|---|---|"]
        for n in REPORT + [x for x in ("bl_sd", "r_u", "r_q", "pblend") if x in post]:
            d = post[n]; lines.append(f"| {PRETTY.get(n, n)} | {d['q05']:.3f} | {d['q50']:.3f} | {d['q95']:.3f} | {d['post_over_prior_sd']:.2f} |")
        open(os.path.join(D, "summary_A.md"), "w").write("\n".join(lines) + "\n")
        print("\n".join(lines), flush=True)
        json.dump(R, open(os.path.join(D, "analysis_A.json"), "w"), indent=1, default=float)
    if a.what in ("holdout", "all") and A and B:
        rng = np.random.default_rng(11)
        parts = {s: particle_sets(f, a.nhold, rng) for s, f in (("A", A), ("B", B))}
        jobs = [(s, parts[s][0][i], parts[s][1][i], 4000 + i, iso)
                for s in ("A", "B") for i in range(a.nhold) for iso in HOLD]
        pool = Pool(a.procs); res = pool.map(holdout_job, jobs, chunksize=2); pool.close(); pool.join()
        HC = {}
        for s in ("A", "B"):
            HC[s] = {iso: dict(D_mean=float(np.mean([r["D"] for r in res if r["scen"] == s and r["iso"] == iso])),
                              rmse={g: float(np.sqrt(np.mean([e ** 2 for r in res if r["scen"] == s and r["iso"] == iso for e in r["errs"][g]])))
                                    for g in ("tfr", "asfr", "smam", "m18")})
                     for iso in HOLD}
        dA = np.array([HC["A"][i]["D_mean"] for i in HOLD]); dB = np.array([HC["B"][i]["D_mean"] for i in HOLD])
        diff = dA - dB
        boot = [np.mean([rng.choice(diff).item() for _ in range(len(HOLD))]) for _ in range(4000)]
        R["holdout"] = dict(per_country=HC, D_A=dA.tolist(), D_B=dB.tolist(), mean_A=float(dA.mean()), mean_B=float(dB.mean()),
                            diff_mean=float(diff.mean()), diff_ci=[float(np.quantile(boot, .025)), float(np.quantile(boot, .975))],
                            A_better=int((diff < 0).sum()), n=len(HOLD), nhold=a.nhold)
        print(json.dumps({k: v for k, v in R["holdout"].items() if k != "per_country"}, indent=1), flush=True)
        json.dump(R, open(os.path.join(D, "analysis_holdout.json"), "w"), indent=1, default=float)
    if a.what in ("decomp", "all") and A and B:
        rng = np.random.default_rng(12)
        parts = {s: particle_sets(f, a.ndec, rng) for s, f in (("A", A), ("B", B))}
        ALL = FIT + HOLD
        jobs = [(s, parts[s][0][i], parts[s][1][i], 9000 + i, iso)
                for s in ("A", "B") for i in range(a.ndec) for iso in ALL]
        pool = Pool(a.procs); res = pool.map(decomp_job, jobs, chunksize=2); pool.close(); pool.join()
        COHS = M.COH; ref = COHS.index(1940); late = COHS.index(1980); DEC = {}
        for s in ("A", "B"):
            base = 0 if s == "A" else a.ndec * len(ALL)
            for label, isos in (("fit", FIT), ("holdout", HOLD)):
                qn, tm, nm = [], [], []
                for i in range(a.ndec):
                    acc = np.zeros((len(COHS), 8))
                    for k, iso in enumerate(ALL):
                        if iso not in isos: continue
                        r = res[base + i * len(ALL) + k]
                        acc += r[2].sum(0)
                    w = acc[:, 0]
                    with np.errstate(all="ignore"):
                        cf = acc[:, 3] / w; b35 = acc[:, 2] / w; nev = acc[:, 5] / w
                    qn.append(cf[ref] - cf[late]); tm.append((b35[ref] - b35[late]) - (cf[ref] - cf[late]))
                    nm.append(nev[late] - nev[ref])
                qn, tm, nm = np.array(qn), np.array(tm), np.array(nm)
                DEC[f"{s}_{label}"] = dict(
                    quantum_mean=float(np.nanmean(qn)), quantum_q05=float(np.nanquantile(qn, .05)),
                    quantum_q95=float(np.nanquantile(qn, .95)), tempo_mean=float(np.nanmean(tm)),
                    tempo_q05=float(np.nanquantile(tm, .05)), tempo_q95=float(np.nanquantile(tm, .95)),
                    never_married_change=float(np.nanmean(nm)))
        R["decomposition"] = DEC
        print(json.dumps(DEC, indent=1), flush=True)
        json.dump(R, open(os.path.join(D, "analysis_decomp.json"), "w"), indent=1, default=float)
