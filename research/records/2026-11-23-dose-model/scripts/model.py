"""Individual-level life-course simulation: schooling dose, kin support, marriage market, births.
Scenario 0 = A (dose individuation + cohort deepening); scenario 1 = B (income lowers fertility directly; dose has no
individuation effect). Everything outside the 'independence index' is shared between A and B."""
import numpy as np
from numba import njit
from scipy.stats import norm

COH = list(range(1930, 2000, 5)); NC = len(COH)
T0, NT, GY0 = 1950, 101, 1925          # calendar index 0 = 1950; gdp array starts 1925
YRS = np.array([0., 3., 6., 9., 12., 14., 16.])   # years of schooling per level (levels: none, prim-incomplete, prim, sec-inc, sec, ter-inc, ter)
# (name, low, high). Priors are uniform on these ranges.
PRIOR = [
 ("d_pi", .2, .9), ("d_si", 3., 5.), ("d_sc", 6., 8.), ("d_ti", 7.5, 9.5), ("d_tc", 9., 11.),     # dose weights (primary complete = 1)
 ("bl_sd", .02, .25), ("r_u", .03, .35), ("r_q", .08, .35), ("pblend", 0., 1.),                    # imputation uncertainty
 ("th_k", 0., 5.), ("th_f", 0., 5.), ("kappa", 0., 3.), ("gam", 0., 8.), ("lam_s", 0., 5.),         # individuation strengths
 ("Dlo", 1.2, 2.6), ("Dhi", 4.5, 8.), ("sd_d", .5, .8), ("c0", .02, 1.0), ("phi0", .5, 1.3), ("k0", .5, 3.), ("eps", .01, .05),
 ("a0", .02, .9), ("al_d", 0., 5.), ("al_u", .2, .8), ("R0", .3, 4.5), ("rho_a", .1, .3), ("al_m", 0., 3.), ("Rm", .8, 2.5),
 ("Kc", 4., 9.), ("sexr", .95, 1.05), ("dsep", .01, .03)]
PN = [p[0] for p in PRIOR]; IX = {n: i for i, n in enumerate(PN)}
LO = np.array([p[1] for p in PRIOR]); HI = np.array([p[2] for p in PRIOR])
HUT = np.interp(np.arange(50), [15, 17, 22, 27, 32, 37, 42, 47, 49], [.40, .50, .62, .52, .447, .406, .222, .061, .03])
ZQ = np.array([-1.40, -.64, 0., .64, 1.40])

def dose_vec(P):
    d = np.array([0., P[IX["d_pi"]], 1., P[IX["d_si"]], P[IX["d_sc"]], P[IX["d_ti"]], P[IX["d_tc"]]])
    return np.maximum.accumulate(d) / 10.

def cell_probs(sh, urb, P, rng):
    """Impute cell-level schooling distributions from national Barro-Lee shares by cohort.
    Latent schooling L = sqrt(r_u)*urban + sqrt(r_q)*wealth + within; cut-points from the national shares, with
    log-normal measurement noise (bl_sd) on the shares. Returns cumulative probs [nC,2,5,7]."""
    nC = sh.shape[0]; ru, rq = P[IX["r_u"]], P[IX["r_q"]]
    if ru + rq > .8: s = .8 / (ru + rq); ru, rq = ru * s, rq * s
    sw = np.sqrt(1 - ru - rq)
    p = np.clip(sh * np.exp(rng.normal(0, P[IX["bl_sd"]], sh.shape)), 1e-6, None); p /= p.sum(1, keepdims=True)
    cut = norm.ppf(np.clip(np.cumsum(p, 1)[:, :-1], 1e-6, 1 - 1e-6))                  # [nC,6]
    zu = (np.array([0., 1.])[None, :] - urb[:, None]) / np.sqrt(urb * (1 - urb))[:, None]  # [nC,2]
    mu = np.sqrt(ru) * zu[:, :, None] + np.sqrt(rq) * ZQ[None, None, :]                 # [nC,2,5]
    cum = norm.cdf((cut[:, None, None, :] - mu[..., None]) / sw)
    return np.concatenate([cum, np.ones(cum.shape[:3] + (1,))], axis=3)

def prepare(pc, P, rng, scen):
    """Country panel + parameter vector -> arrays for the kernel."""
    dosen = dose_vec(P)
    shF = np.array(pc["shF"]); shM = np.array(pc["shM"]); urb = np.array(pc["urban"])
    for sh in (shF, shM):   # blend youngest cohorts toward the panel's completion rates (uncertain weight)
        for k, y0 in enumerate(COH):
            thr = pc["panel_thresholds"].get(str(y0))
            if thr and y0 >= 1985:
                ge2, ge3 = sh[k, 2:].sum(), sh[k, 3:].sum(); w = P[IX["pblend"]]
                n2 = ge2 if thr[0] is None else (1 - w) * ge2 + w * thr[0]; n3 = ge3 if thr[1] is None else (1 - w) * ge3 + w * thr[1]
                n3 = min(n3, n2); g0, g1, g2 = 1 - n2, n2 - n3, n3
                a, b, c_ = sh[k, :2].sum(), sh[k, 2], sh[k, 3:].sum()
                sh[k, :2] *= g0 / max(a, 1e-9); sh[k, 2] = g1 if b > 0 else sh[k, 2]; sh[k, 3:] *= g2 / max(c_, 1e-9)
                sh[k] /= sh[k].sum()
    PW = cell_probs(shF, urb, P, rng)
    PMa = cell_probs(shM, urb, P, rng)           # men: marginalise over wealth quintiles
    PM = np.zeros((NC, 2, 7))
    for c in range(NC):
        for U in (0, 1):
            pm = np.diff(np.concatenate([[0], PMa[c, U]], axis=0), axis=0) if False else None
            pr = np.diff(np.hstack([np.zeros((5, 1)), PMa[c, U]]), axis=1).mean(0); PM[c, U] = np.cumsum(pr)
    wcell = np.zeros((NC, 2, 5))
    for c in range(NC): wcell[c, 1, :] = urb[c] / 5; wcell[c, 0, :] = (1 - urb[c]) / 5
    gdp = np.array(pc["gdp"]); y_at = lambda y: gdp[int(y) - GY0]
    z = np.zeros(NC)
    for c, y0 in enumerate(COH):
        md = (shF[c] * dosen).sum()
        z[c] = .5 * (y_at(y0 + 22) - 7.) / 1.5 + .5 * (md - .35) / .25
    Zc = np.exp(P[IX["kappa"]] * z) if scen == 0 else np.ones(NC)
    return PW, PM, wcell, gdp, Zc, dosen

@njit(cache=True)
def _samp(cum):
    r = np.random.random(); e = 0
    while e < 6 and r > cum[e]: e += 1
    return e

@njit(cache=True)
def _logit_noise():
    u = np.random.random() * .999998 + 1e-6
    return .5 * np.log(u / (1 - u))

@njit(cache=True)
def run_country(seed, scen, nW, tmax, PW, PM, wcell, gdp, Zc, dosen, yrs, hut, P, fc, gap_age):
    np.random.seed(seed)
    nC = PW.shape[0]
    births = np.zeros((NT, 35)); expo = np.zeros((NT, 35)); sing = np.zeros((NT, 35))
    m18n = np.zeros(80); m18d = np.zeros(80); afb_s = np.zeros(NT); afb_n = np.zeros(NT)
    coh = np.zeros((nC, 7, 8))
    th_k, th_f, gam, lam_s = P[9], P[10], P[12], P[13]
    Dlo, Dhi, sd_d, c0, phi0, k0, eps = P[14], P[15] + 1.2 * fc, P[16], P[17], P[18], P[19], P[20]
    a0, al_d, al_u, R0, rho_a, al_m, Rm, Kc, sexr, dsep = P[21], P[22], P[23], P[24], P[25], P[26], P[27], int(P[28] + .5), P[29], P[30]
    K0 = 1. / (1. + np.exp(-(k0 + fc)))
    ga = int(gap_age + .5)
    for c in range(nC):
        y0 = 1930 + 5 * c
        for U in range(2):
            nw = 5 * nW
            b = np.empty(nw, np.int64); ed = np.empty(nw, np.int64); ex = np.empty(nw, np.int64); mk = np.empty(nw, np.int64)
            st = np.zeros(nw, np.int64); par = np.zeros(nw, np.int64); afm = -np.ones(nw, np.int64); afbw = -np.ones(nw, np.int64)
            b30 = np.zeros(nw); b35 = np.zeros(nw); wt = np.empty(nw); qq = np.empty(nw, np.int64); ind0 = np.empty(nw)
            for q in range(5):
                for k in range(nW):
                    i = q * nW + k
                    b[i] = y0 + np.random.randint(0, 5); ed[i] = _samp(PW[c, U, q]); qq[i] = q; wt[i] = wcell[c, U, q] / nW
                    e = int(6 + yrs[ed[i]]);
                    if ed[i] >= 4: e += np.random.randint(-1, 2)
                    ex[i] = e; ind0[i] = dosen[ed[i]] * Zc[c]
                    if scen == 0: ie = ind0[i]
                    else:
                        ie = max(0., min(1.4, (gdp[min(max(b[i] + e - 1925, 0), 125)] - 6.5) / 2.2)) + .12 * (q - 2) + .10 * U
                    mk[i] = e + int(gam * max(ie, 0.) + .5)
            nm = int(5 * nW * sexr + .5)
            bm = np.empty(nm, np.int64); edm = np.empty(nm, np.int64); exm = np.empty(nm, np.int64); av = np.ones(nm, np.bool_)
            for j in range(nm):
                bm[j] = y0 - ga + np.random.randint(0, 5); edm[j] = _samp(PM[c, U]); exm[j] = int(6 + yrs[edm[j]]) + 1
            for t in range(y0 + 15, min(y0 + 4 + 49, tmax) + 1):
                perm = np.random.permutation(nw)
                for ii in range(nw):
                    i = perm[ii]; a = t - b[i]
                    if a < 15 or a > 49: continue
                    w = wt[i]; ti = t - T0; ai = a - 15
                    expo[ti, ai] += w
                    if st[i] == 0: sing[ti, ai] += w
                    if a < ex[i]: continue
                    if scen == 0: Ind = ind0[i]
                    else: Ind = max(0., min(1.4, (gdp[t - 1925] - 6.5) / 2.2)) + .12 * (qq[i] - 2) + .10 * U
                    K = K0 * np.exp(-th_k * Ind)
                    if st[i] == 0:
                        j = -1
                        sh = 1. if a <= 28 else np.exp(-.15 * (a - 28))
                        if np.random.random() < 1 - np.exp(-a0 * np.exp(fc) * K * sh):
                            for _ in range(8):
                                jj = np.random.randint(0, nm)
                                if av[jj] and t - bm[jj] >= max(exm[jj], 20) and t - bm[jj] <= 55: j = jj; break
                        if j < 0 and a >= mk[i] and a <= 45:
                            s = 1. + lam_s * Ind; Rw = R0 + rho_a * (a - mk[i]); bu = -1e9; nv = 0
                            for _ in range(3 * Kc):
                                jj = np.random.randint(0, nm)
                                if not (av[jj] and t - bm[jj] >= max(exm[jj], 20) and t - bm[jj] <= 55): continue
                                nv += 1
                                g = (yrs[edm[jj]] - yrs[ed[i]]) / 12.
                                u = -al_d * s * max(-g, 0.) - al_u * max(g, 0.) + _logit_noise()
                                if u > bu: bu = u; jb = jj
                                if nv >= Kc: break
                            if nv > 0 and bu + Rw > 0:
                                um = -al_m * max((yrs[ed[i]] - yrs[edm[jb]]) / 12., 0.) + Rm + _logit_noise()
                                if um > 0: j = jb
                        if j >= 0:
                            st[i] = 1; av[j] = False; afm[i] = a
                    elif st[i] == 1 and np.random.random() < dsep: st[i] = 2
                    # births
                    hz = 0.
                    if st[i] > 0 or a <= 40:
                        phi = 2. * np.exp(-th_f * Ind) - 1.
                        Di = Dlo + (Dhi - Dlo) * .5 * (1. + phi)
                        cost = c0 * (1 - .9 * K) * (1 + .1 * par[i])
                        S = 1. / (1. + np.exp(-(Di - par[i] - .5) / sd_d))
                        if st[i] == 1: hz = phi0 * hut[a] * S * np.exp(-cost)
                        elif st[i] == 2: hz = phi0 * hut[a] * S * np.exp(-cost) * K
                        else: hz = eps * hut[a] * np.exp(-cost)
                    if hz > 0 and np.random.random() < 1 - np.exp(-hz):
                        births[ti, ai] += w
                        if par[i] == 0: afb_s[ti] += w * a; afb_n[ti] += w; afbw[i] = a
                        par[i] += 1
                        if a < 30: b30[i] += 1
                        if a < 35: b35[i] += 1
            for i in range(nw):
                if b[i] + 18 <= tmax:
                    m18d[b[i] - 1925] += wt[i]
                    if afm[i] >= 0 and afm[i] < 18: m18n[b[i] - 1925] += wt[i]
                if y0 + 4 + 49 <= tmax:
                    s_ = coh[c, ed[i]]; w = wt[i]
                    s_[0] += w; s_[1] += w * b30[i]; s_[2] += w * b35[i]; s_[3] += w * par[i]
                    if par[i] == 0: s_[4] += w
                    else: s_[6] += w * afbw[i]; s_[7] += w
                    if afm[i] >= 0: s_[5] += w
    return births, expo, sing, m18n, m18d, afb_s, afb_n, coh

# ------------------------------------------------------------------ summaries and distance
SD = dict(tfr=.30, asfr=.012, smam=1.0, m18=.04)
YR_S = range(1975, 2051)
def summaries(out):
    births, expo, sing, m18n, m18d, afb_s, afb_n, coh = out
    S = {}
    with np.errstate(all="ignore"):
        r = births / expo
        S["tfr"] = {t: float(np.nansum(r[t - T0]) if (expo[t - T0] > 0).all() else np.nan) for t in YR_S}
        S["asfr"] = {t: float(births[t - T0, :5].sum() / expo[t - T0, :5].sum()) for t in YR_S}
        sm = {}
        for t in YR_S:
            if not (expo[t - T0] > 0).all(): sm[t] = np.nan; continue
            s_a = sing[t - T0] / expo[t - T0]; ss = s_a[30:].mean()
            sm[t] = float((15 + s_a.sum() - 50 * ss) / (1 - ss)) if ss < .4 else np.nan
        S["smam"] = sm
        S["m18"] = {t: float(m18n[t - 24 - 1925:t - 19 - 1925].sum() / m18d[t - 24 - 1925:t - 19 - 1925].sum()) for t in range(1975, 2030)
                    if m18d[t - 24 - 1925:t - 19 - 1925].sum() > 0}
        S["afb"] = {t: float(afb_s[t - T0] / afb_n[t - T0]) if afb_n[t - T0] > 0 else np.nan for t in YR_S}
    return S

def distance(S, pc):
    """Mean squared standardised error, averaging the four target groups equally."""
    parts = {}
    for g, key in (("tfr", "tfr"), ("asfr", "asfr1519"), ("smam", "smam"), ("m18", "m18")):
        obs = pc[key]; z = []
        for y, v in obs.items():
            y = int(y); s = S[g].get(y, np.nan)
            if y <= (2012 if g != "m18" else 2012) and not np.isnan(s): z.append(((s - v) / SD[g]) ** 2)
        if z: parts[g] = float(np.mean(z))
    return float(np.mean(list(parts.values()))) if parts else np.nan, parts

def simulate(pc, P, scen, seed, fc, nW=14, tmax=2012, rng=None):
    rng = rng or np.random.default_rng(seed)
    PW, PM, wcell, gdp, Zc, dosen = prepare(pc, P, rng, scen)
    return run_country(seed, scen, nW, tmax, PW, PM, wcell, gdp, Zc, dosen, YRS, HUT, P, fc, pc["age_gap"])

def simulate_many(pc, P, scen, seed, fcs, nW=14, tmax=2012):
    """Prepare once, run for several country effects (common random numbers)."""
    PW, PM, wcell, gdp, Zc, dosen = prepare(pc, P, np.random.default_rng(seed), scen)
    return [run_country(seed, scen, nW, tmax, PW, PM, wcell, gdp, Zc, dosen, YRS, HUT, P, f, pc["age_gap"]) for f in fcs]
