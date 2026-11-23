"""Host side of the GPU dose model: packs a batch of "runs" (parameter draw x country x country-effect)
onto the Tesla T4 and returns the same aggregate arrays the CPU model produces.

A run is one full simulation of 14 cohorts x 2 urban/rural x 5 wealth quintiles x nW women.
Batching over runs is what buys the order of magnitude: one kernel launch serves every parameter
draw in the batch.
"""
import os
import numpy as np
import cupy as cp
from dosecore import (T0, NT, YR_S, SD, COH, prepare, par_block, D_, IX, LO, HI, dose_vec)

HERE = os.path.dirname(os.path.abspath(__file__))
KERNEL = os.path.join(HERE, "kernel.cu")

K_NAMES = ["k_init", "k_claim", "k_resolve", "k_birth", "k_final"]
BLOCK = 256


def targets_array(acc):
    """The four fitted target series for every run, vectorised.  Mirrors model.py summaries().
    acc: dict with births/expo/sing [n,101,35], afb_s/afb_n [n,101], m18n/m18d [n,80]."""
    r3 = lambda a: a[None] if np.ndim(a) == 2 else a          # (101,35) -> (1,101,35)
    r2 = lambda a: a[None] if np.ndim(a) == 1 else a          # (101,)   -> (1,101)
    births, expo, sing = r3(acc["births"]), r3(acc["expo"]), r3(acc["sing"])
    afb_s, afb_n = r2(acc["afb_s"]), r2(acc["afb_n"])
    m18n, m18d = r2(acc["m18n"]), r2(acc["m18d"])
    n = births.shape[0]
    ys = np.array(YR_S); ti = ys - T0
    with np.errstate(all="ignore"):
        r = births / expo
        valid = (expo[:, ti] > 0).all(-1)
        tfr = np.where(valid, np.nansum(np.where(expo[:, ti] > 0, r[:, ti], 0.0), axis=-1), np.nan)
        asfr = births[:, ti, :5].sum(-1) / expo[:, ti, :5].sum(-1)
        s_a = sing[:, ti] / expo[:, ti]
        ss = s_a[:, :, 30:].mean(-1)
        smam = np.where((ss < .4) & valid, (15 + s_a.sum(-1) - 50 * ss) / (1 - ss), np.nan)
        afb = np.where(afb_n[:, ti] > 0, afb_s[:, ti] / afb_n[:, ti], np.nan)
    m18y = list(range(1975, 2030)); S = {}
    S["tfr"] = dict(zip(ys.tolist(), tfr.T.tolist()))
    S["asfr1519"] = dict(zip(ys.tolist(), asfr.T.tolist()))
    S["smam"] = dict(zip(ys.tolist(), smam.T.tolist()))
    S["afb"] = dict(zip(ys.tolist(), afb.T.tolist()))
    m18 = np.full((n, len(m18y)), np.nan)
    for k, y in enumerate(m18y):
        a0 = y - 1949
        dn = m18d[:, a0:a0 + 5].sum(-1); nu = m18n[:, a0:a0 + 5].sum(-1)
        with np.errstate(all="ignore"):
            m18[:, k] = np.where(dn > 0, nu / dn, np.nan)
    S["m18"] = dict(zip(m18y, m18.T.tolist()))
    return S


def distance_one(S, pc, run):
    """Mean squared standardised error for one run, same averaging as model.distance."""
    parts = {}
    for g, key in (("tfr", "tfr"), ("asfr1519", "asfr1519"), ("smam", "smam"), ("m18", "m18")):
        z = []
        for y, v in pc[key].items():
            y = int(y)
            if y > 2012: continue
            s = S[g].get(y, [np.nan])[run]
            if s is not None and not np.isnan(s): z.append(((s - v) / SD[g]) ** 2)
        if z: parts[g] = float(np.mean(z))
    return (float(np.mean(list(parts.values()))) if parts else np.nan), parts


def distances(S, pcs):
    """[n] distances, one per run, each against its own country's observations."""
    out = np.empty(len(pcs))
    for i, pc in enumerate(pcs):
        out[i], _ = distance_one(S, pc, i)
    return out


class GPUDose:
    def __init__(self, nW=12, seed=1, max_runs=256, tmax=2012):
        self.nW = int(nW); self.seed = int(seed); self.tmax = int(tmax)
        self.WPC = 5 * self.nW; self.WPT = 28 * self.WPC
        self.nmax = int(5 * self.nW * 1.05 + 0.5) + 1
        self.MPT = 28 * self.nmax
        self.max_runs = int(max_runs)
        src = open(KERNEL).read()
        self.mod = cp.RawModule(code=src, options=("-fmad=false", "-std=c++11"))
        self.fn = {k: self.mod.get_function(k) for k in K_NAMES}
        n, W, M = self.max_runs, self.WPT, self.MPT
        I = lambda k: cp.zeros(k, cp.int32); F = lambda k: cp.zeros(k, cp.float64)
        self.w_born = I(n * W); self.w_ed = I(n * W); self.w_ex = I(n * W); self.w_mk = I(n * W)
        self.w_st = I(n * W); self.w_par = I(n * W); self.w_afm = I(n * W); self.w_afbw = I(n * W)
        self.w_b30 = I(n * W); self.w_b35 = I(n * W); self.w_q = I(n * W); self.w_U = I(n * W)
        self.w_claim = I(n * W); self.w_wt = F(n * W); self.w_ind0 = F(n * W)
        self.w_key = cp.zeros(n * W, cp.uint64)
        self.m_born = I(n * M); self.m_edm = I(n * M); self.m_exm = I(n * M); self.m_av = I(n * M)
        self.m_key = cp.zeros(n * M, cp.uint64)
        self.seedv = cp.zeros(n, cp.uint64)
        self.PWc = F(n * 980); self.PMc = F(n * 196); self.wcell = F(n * 140)
        self.Pd = F(n * 25); self.Kci = I(n); self.dosen = F(n * 7); self.Zc = F(n * 14)
        self.gdp = F(n * 126); self.Carr = F(n * 126)
        self.births = F(n * 101 * 35); self.expo = F(n * 101 * 35); self.sing = F(n * 101 * 35)
        self.afb_s = F(n * 101); self.afb_n = F(n * 101)
        self.m18n = F(n * 80); self.m18d = F(n * 80)
        self.coh = F(n * 14 * 7 * 8)
        self.yrs = cp.asarray(np.asarray([0., 3., 6., 9., 12., 14., 16.]), cp.float64)
        from dosecore import HUT
        self.hut = cp.asarray(HUT, cp.float64)
        self.runs = 0
        self.last_tmax = 0
        self.rounds = 2
        self.coh0 = 1930; self.gy0 = 1925; self.my0 = 1925; self.t0 = 1945
        self._graph = None; self._gkey = None

    # ------------------------------------------------------------------ packing
    def load(self, specs):
        """specs: list of dicts with keys prep (from dosecore.prepare), P (full parameter vector),
        fc, gap.  Batches them onto the device."""
        n = len(specs)
        assert n <= self.max_runs, (n, self.max_runs)
        self.runs = n
        PW = np.empty((n, 980)); PM = np.empty((n, 196)); WC = np.empty((n, 140))
        PD = np.empty((n, 25)); KC = np.empty(n, np.int32); DO = np.empty((n, 7))
        ZC = np.empty((n, 14)); GD = np.empty((n, 126)); CM = np.empty((n, 126))
        for i, s in enumerate(specs):
            pr = s["prep"]
            PW[i] = pr["PW"].reshape(-1); PM[i] = pr["PM"].reshape(-1)
            WC[i] = pr["wcell"].reshape(-1); DO[i] = pr["dosen"]
            ZC[i] = pr["Zc"]; GD[i] = pr["gdp"]
            CM[i] = s.get("cm", np.full(126, s.get("cmref", 5.0)))
            PD[i] = par_block(s["P"], s["fc"], s["gap"], s.get("bcm", 0.0), s.get("cmref", 5.0))
            KC[i] = int(s["P"][IX["Kc"]] + .5)
        F = lambda a, t=cp.float64: cp.asarray(np.ascontiguousarray(a), t)
        self.PWc[:n * 980] = F(PW.reshape(-1)).ravel(); self.PMc[:n * 196] = F(PM.reshape(-1)).ravel()
        self.wcell[:n * 140] = F(WC.reshape(-1)).ravel(); self.Pd[:n * 25] = F(PD.reshape(-1)).ravel()
        self.Kci[:n] = cp.asarray(KC); self.dosen[:n * 7] = F(DO.reshape(-1)).ravel()
        self.Zc[:n * 14] = F(ZC.reshape(-1)).ravel(); self.gdp[:n * 126] = F(GD.reshape(-1)).ravel(); self.Carr[:n * 126] = F(CM.reshape(-1)).ravel()
        self.seedv[:n] = cp.asarray(np.full(n, self.seed, np.uint64))   # default: one seed for the batch
        self.births[:n * 3535] = 0; self.expo[:n * 3535] = 0; self.sing[:n * 3535] = 0
        self.afb_s[:n * 101] = 0; self.afb_n[:n * 101] = 0
        self.m18n[:n * 80] = 0; self.m18d[:n * 80] = 0; self.coh[:n * 784] = 0

    # ------------------------------------------------------------------ run
    def _launch(self, scen, tmax):
        """Launch the whole life course.  Called either directly or during CUDA graph capture."""
        n = self.runs; W, M = self.WPT, self.MPT
        nWtot = n * W; nMtot = n * M
        nW, WPC, MPT, nmax = self.nW, self.WPC, self.MPT, self.nmax
        # reset accumulators INSIDE the launch sequence, so a graph replay is a complete fresh run
        self.births[:n * 3535] = 0; self.expo[:n * 3535] = 0; self.sing[:n * 3535] = 0
        self.afb_s[:n * 101] = 0; self.afb_n[:n * 101] = 0
        self.m18n[:n * 80] = 0; self.m18d[:n * 80] = 0; self.coh[:n * 784] = 0
        g1 = ((nWtot + BLOCK - 1) // BLOCK,); g2 = ((nWtot + nMtot + BLOCK - 1) // BLOCK,)
        f = self.fn
        f["k_init"](g2, (BLOCK,), (nW, scen, self.coh0, self.gy0, self.seedv,
            self.PWc, self.PMc, self.wcell, self.dosen, self.Zc, self.gdp, self.Pd, self.yrs,
            WPC, W, MPT, nmax,
            self.w_born, self.w_ed, self.w_ex, self.w_mk, self.w_st, self.w_par, self.w_afm,
            self.w_afbw, self.w_b30, self.w_b35, self.w_q, self.w_U, self.w_claim,
            self.w_wt, self.w_ind0, self.m_born, self.m_edm, self.m_exm, self.m_av, self.m_key,
            nWtot, nMtot))
        claim = f["k_claim"]; resolve = f["k_resolve"]; birth = f["k_birth"]
        for t in range(self.t0, tmax + 1):
            for rnd in range(self.rounds):
                claim(g1, (BLOCK,), (t, rnd, nW, scen, self.gy0, self.seedv,
                    self.PWc, self.PMc, self.wcell, self.dosen, self.Zc, self.gdp, self.Pd, self.Kci,
                    self.yrs, WPC, W, MPT, nmax,
                    self.w_born, self.w_ed, self.w_ex, self.w_mk, self.w_st, self.w_q, self.w_U,
                    self.w_claim, self.w_ind0, self.w_wt, self.expo, self.sing,
                    self.m_born, self.m_edm, self.m_exm, self.m_av, self.m_key, self.w_key, nWtot))
                resolve(g1, (BLOCK,), (t, W, self.w_born, self.w_ex, self.w_st, self.w_afm,
                    self.w_claim, self.w_key, self.m_key, self.m_av, nWtot))
            birth(g1, (BLOCK,), (t, nW, scen, self.gy0, self.seedv,
                self.PWc, self.PMc, self.wcell, self.dosen, self.Zc, self.gdp, self.Pd, self.hut, self.Carr,
                WPC, W, self.w_born, self.w_ed, self.w_ex, self.w_st, self.w_par, self.w_afbw,
                self.w_b30, self.w_b35, self.w_q, self.w_U, self.w_wt, self.w_ind0,
                self.births, self.afb_s, self.afb_n, nWtot))
        f["k_final"](g1, (BLOCK,), (tmax, self.coh0, self.my0, WPC, W, self.w_born, self.w_ed, self.w_afm, self.w_par,
            self.w_afbw, self.w_b30, self.w_b35, self.w_wt, self.m18n, self.m18d, self.coh, nWtot))

    def set_seeds(self, seeds):
        """One RNG seed per run.  Reusing a single seed across parameter draws is deliberate:
        common random numbers make ABC distance comparisons much less noisy."""
        seeds = np.asarray(seeds, dtype=np.uint64).ravel()
        if seeds.size == 1: seeds = np.full(self.runs, seeds[0], np.uint64)
        self.seedv[:self.runs] = cp.asarray(seeds[:self.runs])
        self._gkey = None if False else self._gkey

    def run(self, scen, tmax=None, use_graph=True, seeds=None):
        """Run the batch.  With use_graph the launch sequence is captured once into a CUDA graph and
        replayed, which removes ~0.4 ms of Python/driver overhead per kernel launch (about 200 launches
        per run at tmax=2012)."""
        tmax = self.tmax if tmax is None else int(tmax)
        self.last_tmax = tmax
        if seeds is not None: self.set_seeds(seeds)
        key = (self.runs, tmax, int(scen), self.rounds)
        if use_graph:
            if self._gkey != key:
                self._launch(scen, tmax); cp.cuda.Stream.null.synchronize()   # warm up / compile
                st = cp.cuda.Stream(non_blocking=True)
                with st:
                    st.begin_capture()
                    self._launch(scen, tmax)
                    g = st.end_capture()
                cp.cuda.Stream.null.synchronize()
                self._graph = g; self._gkey = key
            self._graph.launch()
        else:
            self._launch(scen, tmax)
        return self.collect()

    def collect(self, state=False):
        n = self.runs
        out = dict(
            births=self.births[:n * 3535].get().reshape(n, 101, 35),
            expo=self.expo[:n * 3535].get().reshape(n, 101, 35),
            sing=self.sing[:n * 3535].get().reshape(n, 101, 35),
            afb_s=self.afb_s[:n * 101].get().reshape(n, 101),
            afb_n=self.afb_n[:n * 101].get().reshape(n, 101),
            m18n=self.m18n[:n * 80].get().reshape(n, 80),
            m18d=self.m18d[:n * 80].get().reshape(n, 80),
            coh=self.coh[:n * 784].get().reshape(n, 14, 7, 8),
        )
        W = self.WPT
        if state:
            out["state"] = dict(
                st=self.w_st[:n * W].get().reshape(n, W), par=self.w_par[:n * W].get().reshape(n, W),
                afm=self.w_afm[:n * W].get().reshape(n, W), ed=self.w_ed[:n * W].get().reshape(n, W),
                born=self.w_born[:n * W].get().reshape(n, W), ex=self.w_ex[:n * W].get().reshape(n, W),
                mk=self.w_mk[:n * W].get().reshape(n, W), b30=self.w_b30[:n * W].get().reshape(n, W),
                b35=self.w_b35[:n * W].get().reshape(n, W), afbw=self.w_afbw[:n * W].get().reshape(n, W),
                mav=self.m_av[:n * self.MPT].get().reshape(n, self.MPT))
        return out


def make_spec(pc, P, scen, fc, gap, seed_dc, dcidx):
    """One run: parameter vector x country x country-effect, with the host-side imputation done."""
    return dict(prep=prepare(pc, P, scen, seed_dc, dcidx), P=P, fc=fc, gap=gap)
