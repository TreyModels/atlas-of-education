"""Shared specification for the GPU dose model: constants, counter-based RNG (Philox4x32-10),
and software exp/log that are bit-identical between numpy (CPU reference) and CUDA.

WHY the software exp/log: the porting test compares the numpy reference against the CUDA kernel
for the same seed and parameter vector.  numpy's libm exp/log and CUDA's device exp/log differ in
the last bit, which can flip a `u < 1-exp(-h)` birth decision.  A tiny Horner implementation with
the same operation order on both sides removes that source of difference entirely, so "did the
port change the model" and "did libm round differently" cannot be confused.
"""
import numpy as np

# ----------------------------------------------------------------------------- model constants
COH = list(range(1930, 2000, 5)); NC = len(COH)
T0, NT, GY0 = 1950, 101, 1925
YRS = np.array([0., 3., 6., 9., 12., 14., 16.])
PRIOR = [
 ("d_pi", .2, .9), ("d_si", 3., 5.), ("d_sc", 6., 8.), ("d_ti", 7.5, 9.5), ("d_tc", 9., 11.),
 ("bl_sd", .02, .25), ("r_u", .03, .35), ("r_q", .08, .35), ("pblend", 0., 1.),
 ("th_k", 0., 5.), ("th_f", 0., 5.), ("kappa", 0., 3.), ("gam", 0., 8.), ("lam_s", 0., 5.),
 ("Dlo", 1.2, 2.6), ("Dhi", 4.5, 8.), ("sd_d", .5, .8), ("c0", .02, 1.0), ("phi0", .5, 1.3),
 ("k0", .5, 3.), ("eps", .01, .05), ("a0", .02, .9), ("al_d", 0., 5.), ("al_u", .2, .8),
 ("R0", .3, 4.5), ("rho_a", .1, .3), ("al_m", 0., 3.), ("Rm", .8, 2.5), ("Kc", 4., 9.),
 ("sexr", .95, 1.05), ("dsep", .01, .03)]
PN = [p[0] for p in PRIOR]; IX = {n: i for i, n in enumerate(PN)}; D_ = len(PN)
LO = np.array([p[1] for p in PRIOR]); HI = np.array([p[2] for p in PRIOR])
HUT = np.interp(np.arange(50), [15, 17, 22, 27, 32, 37, 42, 47, 49],
                [.40, .50, .62, .52, .447, .406, .222, .061, .03])
ZQ = np.array([-1.40, -.64, 0., .64, 1.40])
SD = dict(tfr=.30, asfr=.012, smam=1.0, m18=.04)
YR_S = list(range(1975, 2051))
NPAR = 22   # scalars written into the GPU parameter block


def dose_vec(P):
    d = np.array([0., P[IX["d_pi"]], 1., P[IX["d_si"]], P[IX["d_sc"]], P[IX["d_ti"]], P[IX["d_tc"]]])
    return np.maximum.accumulate(d) / 10.


# ----------------------------------------------------------------------------- Philox4x32-10
_M0 = np.uint32(0xD2511F53); _M1 = np.uint32(0xCD9E8D57)
_W0 = np.uint32(0x9E3779B9); _W1 = np.uint32(0xBB67AE85)
_MASK32 = np.uint64(0xFFFFFFFF)
TWO_M32 = np.float64(1.0) / np.float64(4294967296.0)   # 2**-32, exactly representable


def _mulhilo(a, b):
    p = a.astype(np.uint64) * b.astype(np.uint64)
    return (p >> np.uint64(32)).astype(np.uint32), (p & _MASK32).astype(np.uint32)


def philox(c0, c1, c2, c3, seed0, seed1):
    """Vectorised Philox4x32-10.  Counter = (c0,c1,c2,c3), key = (seed0,seed1).
    Bit-identical to the CUDA implementation in kernel.cu."""
    c0 = np.asarray(c0, dtype=np.uint32).copy(); c1 = np.asarray(c1, dtype=np.uint32).copy()
    c2 = np.asarray(c2, dtype=np.uint32).copy(); c3 = np.asarray(c3, dtype=np.uint32).copy()
    k0 = np.full(c0.shape, np.uint32(seed0 & 0xFFFFFFFF), np.uint32)
    k1 = np.full(c0.shape, np.uint32(seed1 & 0xFFFFFFFF), np.uint32)
    for i in range(10):
        hi0, lo0 = _mulhilo(np.full(c0.shape, _M0, np.uint32), c0)
        hi1, lo1 = _mulhilo(np.full(c0.shape, _M1, np.uint32), c2)
        n0 = hi1 ^ c1 ^ k0; n2 = hi0 ^ c3 ^ k1
        c0, c1, c2, c3 = n0, lo1, n2, lo0
        if i < 9:
            k0 = k0 + _W0; k1 = k1 + _W1
    return c0, c1, c2, c3


def uniform_from_bits(x):
    """uint32 -> double in (0,1).  Same expression in CUDA: (x + 0.5) * 2**-32."""
    return (x.astype(np.float64) + 0.5) * TWO_M32


def uniforms(wid, aux, seed, nblocks):
    """[N, 4*nblocks] uniforms for streams keyed on (global stream id, aux)."""
    wid = np.asarray(wid, dtype=np.uint64)
    c0 = (wid & np.uint64(0xFFFFFFFF)).astype(np.uint32)
    c1 = (wid >> np.uint64(32)).astype(np.uint32)
    aux = np.asarray(aux, dtype=np.uint32)
    out = np.empty((wid.shape[0], 4 * nblocks), np.float64)
    raw = np.empty((wid.shape[0], 4 * nblocks), np.uint32)
    for b in range(nblocks):
        o = philox(c0, c1, aux, np.full(wid.shape, np.uint32(b), np.uint32),
                   np.uint32(seed & 0xFFFFFFFF), np.uint32((seed >> 32) & 0xFFFFFFFF))
        for j in range(4):
            raw[:, 4 * b + j] = o[j]
            out[:, 4 * b + j] = uniform_from_bits(o[j])
    return out, raw


# ----------------------------------------------------------------------------- bit-exact exp/log
_LN2HI = 6.93147180369123816490e-01
_LN2LO = 1.90821492927058770002e-10
_INVLN2 = 1.44269504088896338700e+00
_EXPC = [1.0 / 6227020800.0, 1.0 / 479001600.0, 1.0 / 39916800.0, 1.0 / 3628800.0,
         1.0 / 362880.0, 1.0 / 40320.0, 1.0 / 5040.0, 1.0 / 720.0, 1.0 / 120.0,
         1.0 / 24.0, 1.0 / 6.0, 0.5, 1.0, 1.0]     # 1/14! ... 1/1!, 1/0!


def sy_exp(x):
    """exp(x), |x| < 60, by range reduction to +-ln2/2 and a degree-14 Taylor series.
    Operation order matches sy_exp() in kernel.cu exactly."""
    x = np.asarray(x, dtype=np.float64)
    k = np.floor(x * _INVLN2 + 0.5)
    r = (x - k * _LN2HI) - k * _LN2LO
    p = np.full(x.shape, _EXPC[0])
    for c in _EXPC[1:]:
        p = p * r + c
    return np.ldexp(p, k.astype(np.int64))


def sy_log(x):
    """log(x), x > 0.  frexp + atanh series.  Order matches sy_log() in kernel.cu."""
    x = np.asarray(x, dtype=np.float64)
    m, e = np.frexp(x)
    small = m < 0.7071067811865476
    m = np.where(small, m * 2.0, m)
    e = np.where(small, e - 1, e)
    t = (m - 1.0) / (m + 1.0)
    t2 = t * t
    p = np.full(x.shape, 1.0 / 13.0)
    for c in (1.0 / 11.0, 1.0 / 9.0, 1.0 / 7.0, 1.0 / 5.0, 1.0 / 3.0):
        p = p * t2 + c
    logm = 2.0 * t * (1.0 + t2 * p)
    return (e * _LN2HI + e * _LN2LO) + logm


# ----------------------------------------------------------------------------- schooling imputation
def cell_probs(sh, urb, P, noise):
    """Same as model.py cell_probs but taking pre-drawn log-normal noise (so both engines share it)."""
    from scipy.stats import norm
    nC = sh.shape[0]; ru, rq = P[IX["r_u"]], P[IX["r_q"]]
    if ru + rq > .8:
        s = .8 / (ru + rq); ru, rq = ru * s, rq * s
    sw = np.sqrt(1 - ru - rq)
    p = np.clip(sh * np.exp(noise), 1e-6, None); p /= p.sum(1, keepdims=True)
    cut = norm.ppf(np.clip(np.cumsum(p, 1)[:, :-1], 1e-6, 1 - 1e-6))
    zu = (np.array([0., 1.])[None, :] - urb[:, None]) / np.sqrt(urb * (1 - urb))[:, None]
    mu = np.sqrt(ru) * zu[:, :, None] + np.sqrt(rq) * ZQ[None, None, :]
    cum = norm.cdf((cut[:, None, None, :] - mu[..., None]) / sw)
    return np.concatenate([cum, np.ones(cum.shape[:3] + (1,))], axis=3)


def prepare(pc, P, scen, seed_dc, dcidx, gy0=None):
    """Host-side preparation (numpy, shared by GPU and reference).  Deterministic from (seed, draw id).
    Returns the flat arrays the kernels need for one (parameter draw, country) pair."""
    dosen = dose_vec(P)
    shF = np.array(pc["shF"], dtype=np.float64); shM = np.array(pc["shM"], dtype=np.float64)
    urb = np.array(pc["urban"], dtype=np.float64)
    for sh in (shF, shM):
        for k, y0 in enumerate(COH):
            thr = pc["panel_thresholds"].get(str(y0))
            if thr and y0 >= 1985:
                ge2, ge3 = sh[k, 2:].sum(), sh[k, 3:].sum(); w = P[IX["pblend"]]
                n2 = ge2 if thr[0] is None else (1 - w) * ge2 + w * thr[0]
                n3 = ge3 if thr[1] is None else (1 - w) * ge3 + w * thr[1]
                n3 = min(n3, n2); g0, g1, g2 = 1 - n2, n2 - n3, n3
                a, b, c_ = sh[k, :2].sum(), sh[k, 2], sh[k, 3:].sum()
                sh[k, :2] *= g0 / max(a, 1e-9); sh[k, 2] = g1 if b > 0 else sh[k, 2]
                sh[k, 3:] *= g2 / max(c_, 1e-9); sh[k] /= sh[k].sum()
    # two independent log-normal noise draws, keyed on (seed, draw, country)
    nz, _ = uniforms(np.array([dcidx * 2, dcidx * 2 + 1], dtype=np.uint64), np.uint32(0), seed_dc, 25)
    nF = nz[0, :NC * 7].reshape(NC, 7)
    nM = nz[1, :NC * 7].reshape(NC, 7)
    PW = cell_probs(shF, urb, P, nF * P[IX["bl_sd"]])
    PMa = cell_probs(shM, urb, P, nM * P[IX["bl_sd"]])
    PM = np.zeros((NC, 2, 7))
    for c in range(NC):
        for U in (0, 1):
            pr = np.diff(np.hstack([np.zeros((5, 1)), PMa[c, U]]), axis=1).mean(0); PM[c, U] = np.cumsum(pr)
    wcell = np.zeros((NC, 2, 5))
    for c in range(NC):
        wcell[c, 1, :] = urb[c] / 5; wcell[c, 0, :] = (1 - urb[c]) / 5
    gdp = np.array(pc["gdp"], dtype=np.float64)
    z = np.zeros(NC)
    for c, y0 in enumerate(COH):
        md = (shF[c] * dosen).sum()
        z[c] = .5 * (gdp[int(y0 + 22) - (GY0 if gy0 is None else gy0)] - 7.) / 1.5 + .5 * (md - .35) / .25
    Zc = np.exp(P[IX["kappa"]] * z) if scen == 0 else np.ones(NC)
    return dict(PW=PW.astype(np.float64), PM=PM.astype(np.float64), wcell=wcell, gdp=gdp,
                Zc=Zc.astype(np.float64), dosen=dosen.astype(np.float64))


def par_block(P, fc, gap, bcm=0.0, cmref=5.0):
    """The 25 scalars per run; order must match P_* indices in kernel.cu.
    bcm/cmref drive the child-mortality channel of the transition extension; bcm=0 makes it a no-op."""
    return np.array([P[IX["th_k"]], P[IX["th_f"]], P[IX["gam"]], P[IX["lam_s"]], P[IX["Dlo"]],
                     P[IX["Dhi"]] + 1.2 * fc, P[IX["sd_d"]], P[IX["c0"]], P[IX["phi0"]], P[IX["k0"]],
                     P[IX["eps"]], P[IX["a0"]], P[IX["al_d"]], P[IX["al_u"]], P[IX["R0"]],
                     P[IX["rho_a"]], P[IX["al_m"]], P[IX["Rm"]], P[IX["sexr"]], P[IX["dsep"]],
                     fc, np.exp(fc), float(gap), float(bcm), float(cmref)], dtype=np.float64)
