"""Porting test for the GPU dose model.

Three questions, in order:
 A. Do the numpy and CUDA implementations of Philox4x32-10 produce the same bits?
 B. Does the bit-exact exp/log agree bit for bit?
 C. For the same seed and the same parameter vector, does the GPU engine give the same answer as the
    numpy reference of the same algorithm (which is the real port check: state variables, then
    aggregates, then the fitted target series)?
 D. Does the new engine reproduce the ORIGINAL serial CPU model (numba model.py) distributionally?
    It cannot reproduce it draw-for-draw: the original consumes one global numpy stream in a
    data-dependent order and visits women in a random permutation, so any parallel rewrite must
    re-key the randomness.  So: many seeds, compare means and standard deviations of the target series.
"""
import json, sys, time, os
import numpy as np
import cupy as cp

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
RES = os.environ.get("RESULTS", "../results")
os.makedirs(RES, exist_ok=True)

import dosecore as dc
from engine import GPUDose, targets_array, distances, make_spec
from ref_numpy import simulate_ref

TEST_SRC = r'''
extern "C" __global__ void k_dump_u(const unsigned long long* wid, const unsigned* aux, int nb,
        unsigned s0, unsigned s1, double* u, unsigned* raw, int n) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;
    double uu[24]; unsigned rr[24];
    draw_uniforms(wid[i], aux[i], s0, s1, nb, uu, rr);
    for (int k = 0; k < nb * 4; k++) { u[(size_t)i * nb * 4 + k] = uu[k]; raw[(size_t)i * nb * 4 + k] = rr[k]; }
}
extern "C" __global__ void k_exp(const double* x, int n, double* e) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;
    e[i] = sy_exp(x[i]);
}
extern "C" __global__ void k_log(const double* x, int n, double* l) {
    int i = blockIdx.x * blockDim.x + threadIdx.x;
    if (i >= n) return;
    l[i] = sy_log(x[i]);
}
'''


def test_rng(n=20000, nb=6):
    src = open(os.path.join(HERE, "kernel.cu")).read() + TEST_SRC
    mod = cp.RawModule(code=src, options=("-fmad=false", "-std=c++11"))
    k = mod.get_function("k_dump_u")
    rng = np.random.default_rng(0)
    wid = rng.integers(0, 10 ** 6, n).astype(np.uint64)
    aux = rng.integers(0, 400, n).astype(np.uint32)
    seed = 12345
    du = cp.zeros((n, nb * 4), cp.float64); dr = cp.zeros((n, nb * 4), cp.uint32)
    k(((n + 127) // 128,), (128,), (cp.asarray(wid), cp.asarray(aux), nb, np.uint32(seed), np.uint32(0),
                                  du, dr, n))
    gu, gr = du.get(), dr.get()
    nu, nr = dc.uniforms(wid, aux, seed, nb)
    return dict(bits_equal=bool((gr == nr).all()), bits_max_diff=int(np.abs(gr.astype(np.int64) - nr).max()),
                u_max_abs_diff=float(np.abs(gu - nu).max()))


def test_math():
    src = open(os.path.join(HERE, "kernel.cu")).read() + TEST_SRC
    mod = cp.RawModule(code=src, options=("-fmad=false", "-std=c++11"))
    ke = mod.get_function("k_exp"); kl = mod.get_function("k_log")
    x = np.concatenate([np.linspace(-20, 20, 4000), np.random.default_rng(1).normal(0, 4, 4000)])
    y = np.exp(np.clip(np.linspace(-15, 15, 4000), -700, 700))
    xl = np.concatenate([np.abs(np.random.default_rng(2).normal(0, 3, 4000)) + 1e-6, y])
    de = cp.zeros(x.size, cp.float64); dl = cp.zeros(xl.size, cp.float64)
    grid = lambda n: ((n + 127) // 128,)
    ke(grid(x.size), (128,), (cp.asarray(x), x.size, de))
    kl(grid(xl.size), (128,), (cp.asarray(xl), xl.size, dl))
    ge, gl = de.get(), dl.get()
    return dict(exp_bits_equal=bool((ge == dc.sy_exp(x)).all()),
                exp_max_rel=float(np.max(np.abs(ge - dc.sy_exp(x)) / np.maximum(np.abs(dc.sy_exp(x)), 1e-300))),
                exp_vs_libm=float(np.max(np.abs(ge - np.exp(x)) / np.exp(x))),
                log_bits_equal=bool((gl == dc.sy_log(xl)).all()),
                log_max_abs=float(np.max(np.abs(gl - dc.sy_log(xl)))),
                log_vs_libm=float(np.max(np.abs(gl - np.log(xl)) / np.maximum(np.abs(np.log(xl)), 1e-9))))


def test_equivalence(PAN, params, scen_list, seeds, nW=12, tmax=2012):
    rows = []
    eng = GPUDose(nW=nW, seed=1, max_runs=1, tmax=tmax)
    iso = PAN["FIT"][0]; pc = PAN["countries"][iso]
    fc, gap = 0.0, pc["age_gap"]
    for scen, seed in [(s, sd) for s in scen_list for sd in seeds]:
        prep = make_spec(pc, P, scen, fc, gap, seed, 0)["prep"]
        eng.seed = int(seed)
        eng.load([dict(prep=prep, P=P, fc=fc, gap=gap)])
        gpu = eng.run(scen, use_graph=False)
        gpu["state"] = eng.collect(state=True)["state"]
        ref = simulate_ref(prep, P, scen, seed, fc, gap, nW=nW, tmax=tmax)
        st = {k: int(np.abs(gpu["state"][k].astype(np.int64) - ref["state"][k].astype(np.int64)).max())
              for k in ("st", "par", "afm", "ed", "born", "ex", "mk", "b30", "b35", "afbw", "mav")}
        nst = {k: int((gpu["state"][k].astype(np.int64) != ref["state"][k].astype(np.int64)).sum())
               for k in ("st", "par", "afm", "b30", "b35", "afbw")}
        agg = {}
        for k in ("births", "expo", "sing", "afb_s", "afb_n", "m18n", "m18d", "coh"):
            agg[k] = float(np.abs(gpu[k][0] - ref[k]).max())
        Sg = targets_array(gpu); Sr = targets_array(ref)
        val = lambda z: z[0] if isinstance(z, (list, tuple)) else z
        tgt = {}
        for g in ("tfr", "asfr1519", "smam", "m18"):
            ys = [y for y in Sg[g] if y <= 2012]
            tgt[g] = float(np.nanmax(np.abs(np.array([val(Sg[g][y]) for y in ys]) - np.array([val(Sr[g][y]) for y in ys]))))
        rows.append(dict(scen="AB"[scen], seed=int(seed), state_absmax=st, state_nmismatch=nst,
                         agg_absmax=agg, target_absmax=tgt))
    return rows


def test_vs_original(PAN, nseeds=12, nW=12, tmax=2012, scen=0, fc_list=(-1.2, 0.0, 1.2)):
    """Distributional check against the ORIGINAL numba model.  Identical prepared inputs (the original's
    own prepare), so any difference is the engine: random streams + the marriage-market ordering."""
    import model as M
    rng = np.random.default_rng(11)
    P = M.LO + rng.random(len(M.PN)) * (M.HI - M.LO)      # one random parameter vector
    out = {}
    eng = GPUDose(nW=nW, seed=1, max_runs=len(fc_list), tmax=tmax)
    for iso in ("PHL", "CHN", "EGY"):
        pc = PAN["countries"][iso]
        gap = pc["age_gap"]
        prep_list, cpu = [], []
        for k, fc in enumerate(fc_list):
            PW, PM, wcell, gdp, Zc, dosen = M.prepare(pc, P, np.random.default_rng(500 + k), scen)
            prep = dict(PW=PW, PM=PM, wcell=wcell, gdp=gdp, Zc=Zc, dosen=dosen)
            seeds = [10_000 + 7 * s + k for s in range(nseeds)]
            gpush = []
            for s, seed in enumerate(seeds):
                o = M.simulate(pc, P, scen, seed, fc, nW=nW, tmax=tmax)
                gpush.append(M.summaries(o))
            eng.seed = 1
            eng.load([dict(prep=prep, P=P, fc=fc, gap=gap)] * 1)
            gs = []
            for s, seed in enumerate(seeds):
                eng.seed = int(seed)
                acc = eng.run(scen)
                gs.append(targets_array(acc))
            for kk, g in (("tfr", "tfr"), ("asfr", "asfr1519"), ("smam", "smam")):
                ys = [y for y in range(1980, 2011, 5)]
                ys = [y for y in ys if not np.isnan(np.mean([x[g][y][0] for x in gs]))]
                c = np.array([[x[kk][y] for y in ys] for x in gpush])
                q = np.array([[x[g][y][0] for y in ys] for x in gs])
                out[f"{iso}_{kk}"] = dict(years=ys,
                    cpu_mean=np.nanmean(c, 0).round(4).tolist(), gpu_mean=np.nanmean(q, 0).round(4).tolist(),
                    diff=(np.nanmean(q, 0) - np.nanmean(c, 0)).round(4).tolist(),
                    cpu_sd=np.nanstd(c, 0).round(4).tolist(), gpu_sd=np.nanstd(q, 0).round(4).tolist(),
                    t=float(np.nanmean((np.nanmean(q, 0) - np.nanmean(c, 0)) /
                                       np.sqrt(np.nanvar(c, 0) / nseeds + np.nanvar(q, 0) / nseeds))))
    return out, P.tolist()


def test_graphs(PAN, P):
    """CUDA-graph replay must equal the plain launch sequence."""
    eng = GPUDose(nW=12, seed=9, max_runs=4, tmax=2012)
    specs = []
    for i in range(4):
        iso = PAN["FIT"][i]; pc = PAN["countries"][iso]
        specs.append(make_spec(pc, P, 0, 0.0, pc["age_gap"], 7, i))
    eng.load(specs)
    a = eng.run(0, use_graph=False)
    b = eng.run(0, use_graph=False)
    c = eng.run(0, use_graph=True)
    d = eng.run(0, use_graph=True)
    e = eng.run(0, use_graph=True)
    mx = lambda x, y: float(max(np.abs(x[k] - y[k]).max() for k in ("births", "expo", "sing", "m18n", "coh")))
    return dict(no_graph_repeatable=mx(a, b), graph_vs_plain=mx(a, c), graph_repeatable=mx(d, e))


def bench(PAN, scen=0, nRuns=48, reps=3):
    """Throughput: runs per second, and the CPU-equivalent cost of the same workload."""
    import model as M
    P = M.LO + np.random.default_rng(3).random(len(M.PN)) * (M.HI - M.LO)
    FIT = PAN["FIT"]
    specs = []
    for i in range(nRuns):
        iso = FIT[i % len(FIT)]; pc = PAN["countries"][iso]
        specs.append(make_spec(pc, P, scen, 0.0, pc["age_gap"], 7, i))
    eng = GPUDose(nW=12, seed=5, max_runs=nRuns, tmax=2012)
    eng.load(specs); eng.run(scen)
    t = time.time()
    for _ in range(reps): out = eng.run(scen)
    dt = (time.time() - t) / reps
    S = targets_array(out)
    t2 = time.time()
    for _ in range(reps): eng.load(specs); eng.run(scen)
    dt2 = (time.time() - t2) / reps
    # same workload on one CPU core with the original model
    pc = PAN["countries"][FIT[0]]
    M.simulate(pc, P, scen, 1, 0.0, nW=12)
    t3 = time.time()
    for i in range(4):
        M.simulate(PAN["countries"][FIT[i % len(FIT)]], P, scen, 1 + i, 0.0, nW=12)
    cpu = (time.time() - t3) / 4
    return dict(nRuns=nRuns, gpu_sec=dt, gpu_runs_per_sec=nRuns / dt, load_plus_run_sec=dt2,
                cpu_sec_per_run=cpu, speedup_per_core=cpu / (dt / nRuns),
                gpu_sec_per_param_draw_24runs=dt / nRuns * 24)


if __name__ == "__main__":
    cands = ["../data/panel.json", "data/panel.json", os.path.join(HERE, "..", "..", "..", "data", "panel.json")]
    PAN = json.load(open(next(c for c in cands if os.path.exists(c))))
    import model as M
    rng = np.random.default_rng(4)
    P = M.LO + rng.random(len(M.PN)) * (M.HI - M.LO)
    R = {}
    R["rng"] = test_rng()
    print("RNG:", R["rng"], flush=True)
    R["math"] = test_math()
    print("MATH:", R["math"], flush=True)
    R["equivalence"] = test_equivalence(PAN, P, [0, 1], [1, 2, 3])
    mx = max(max(r["state_absmax"].values()) for r in R["equivalence"])
    print("EQUIV state max |diff| =", mx, flush=True)
    for r in R["equivalence"]:
        print("  scen", r["scen"], "seed", r["seed"], "mismatch", {k: v for k, v in r["state_nmismatch"].items() if v},
              "agg", {k: round(v, 15) for k, v in r["agg_absmax"].items()}, "tgt", {k: round(v, 12) for k, v in r["target_absmax"].items()}, flush=True)
    R["graphs"] = test_graphs(PAN, P)
    print("GRAPHS:", R["graphs"], flush=True)
    R["bench"] = bench(PAN)
    print("BENCH:", R["bench"], flush=True)
    print("running distributional check vs original model ...", flush=True)
    R["dist"], Pt = test_vs_original(PAN, nseeds=12)
    for k, v in R["dist"].items():
        print(" ", k, "diff", v["diff"], "t=", round(v["t"], 2), flush=True)
    OUT = os.path.join(RES, "port_test.json")
    json.dump(R, open(OUT, "w"), indent=1)
    print("wrote", OUT)
