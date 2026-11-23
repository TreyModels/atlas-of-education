"""Independent numpy implementation of exactly the algorithm in kernel.cu, vectorised over women.
Purpose: the porting test.  Same seed + same parameter vector must give the same answer, because both
consume the same counter-based random numbers and the same bit-exact exp/log.
"""
import numpy as np
from dosecore import (IX, YRS, HUT, uniforms, sy_exp, sy_log)

WPC_OF = lambda nW: 5 * nW
NMAX_OF = lambda nW: int(5 * nW * 1.05 + 0.5) + 1


def simulate_ref(prep, P, scen, seed, fc, gap, nW=12, tmax=2012, coh0=None, gy0=None, cm=None, bcm=0.0, cmref=5.0):
    PW, PM, wcell = prep["PW"], prep["PM"], prep["wcell"]
    PMr = PM.reshape(28, PM.shape[-1])          # per (cohort, urban) cell, men are pooled over wealth
    gdp, Zc, dosen = prep["gdp"], prep["Zc"], prep["dosen"]
    WPC = WPC_OF(nW); WPT = 28 * WPC; nmax = NMAX_OF(nW); MPT = 28 * nmax
    Kc = int(P[IX["Kc"]] + .5); nm = int(5 * nW * P[IX["sexr"]] + .5); ga = int(gap + .5)
    th_k, th_f, gam, lam_s = P[IX["th_k"]], P[IX["th_f"]], P[IX["gam"]], P[IX["lam_s"]]
    Dlo, Dhi, sd_d = P[IX["Dlo"]], P[IX["Dhi"]] + 1.2 * fc, P[IX["sd_d"]]
    c0, phi0, k0, eps = P[IX["c0"]], P[IX["phi0"]], P[IX["k0"]], P[IX["eps"]]
    a0, al_d, al_u = P[IX["a0"]], P[IX["al_d"]], P[IX["al_u"]]
    R0, rho_a, al_m, Rm = P[IX["R0"]], P[IX["rho_a"]], P[IX["al_m"]], P[IX["Rm"]]
    sexr, dsep = P[IX["sexr"]], P[IX["dsep"]]
    Efc = np.exp(fc); K0 = 1. / (1. + np.exp(-(k0 + fc)))
    yrs = YRS

    # ---------------------------------------------------------------- init
    idx = np.arange(WPT, dtype=np.uint64)
    cell = (np.arange(WPT) // WPC); within = np.arange(WPT) % WPC
    c = cell // 2; U = cell % 2; q = within // nW
    u8, _ = uniforms(idx, np.zeros(WPT, np.uint32), seed, 2)
    b = 1930 + 5 * c + (u8[:, 0] * 5.0).astype(np.int64)
    cum = PW[c, U, q]                                        # [WPT, 8]
    ed = (u8[:, 1][:, None] > cum[:, :6]).sum(1).astype(np.int64)
    e = 6 + yrs[ed].astype(np.int64)
    e = e + np.where(ed >= 4, (u8[:, 2] * 3.0).astype(np.int64) - 1, 0)
    ind0 = dosen[ed] * Zc[c]
    if scen == 0:
        ie = ind0.copy()
    else:
        gi = np.clip(b + e - 1925, 0, 125)
        x = np.clip((gdp[gi] - 6.5) / 2.2, 0., 1.4)
        ie = x + .12 * (q - 2) + .10 * U
    mk = e + np.floor(gam * np.maximum(ie, 0.) + .5).astype(np.int64)
    wt = wcell[c, U, q] / nW
    st = np.zeros(WPT, np.int64); par = np.zeros(WPT, np.int64)
    afm = -np.ones(WPT, np.int64); afbw = -np.ones(WPT, np.int64)
    b30 = np.zeros(WPT, np.int64); b35 = np.zeros(WPT, np.int64)

    midx = np.arange(MPT, dtype=np.uint64)
    mcell = (np.arange(MPT) // nmax); jm_ = np.arange(MPT) % nmax
    mc = mcell // 2
    um, _ = uniforms(WPT + midx, np.zeros(MPT, np.uint32), seed, 1)
    mb = 1930 + 5 * mc - ga + (um[:, 0] * 5.0).astype(np.int64)
    med = (um[:, 1][:, None] > PMr[mcell][:, :6]).sum(1).astype(np.int64)
    mexc = 6 + yrs[med].astype(np.int64) + 1
    mav = (jm_ < nm).astype(np.int64)
    mb = np.where(mav == 1, mb, 0); med = np.where(mav == 1, med, 0); mexc = np.where(mav == 1, mexc, 0)

    # ---------------------------------------------------------------- accumulators
    expo = np.zeros(101 * 35); sing = np.zeros(101 * 35); births = np.zeros(101 * 35)
    afb_s = np.zeros(101); afb_n = np.zeros(101)
    m18n = np.zeros(80); m18d = np.zeros(80)

    for t in range(1945, tmax + 1):
        a = t - b
        inwin = (a >= 15) & (a <= 49)
        ti = t - 1950
        if ti < 0: ti += 101
        ai = np.where(inwin, a - 15, 0)
        np.add.at(expo, ti * 35 + ai[inwin], wt[inwin])
        s0 = inwin & (st == 0)
        np.add.at(sing, ti * 35 + ai[s0], wt[s0])

        past = inwin & (a >= e)
        ub, _ = uniforms(idx, np.full(WPT, 1 + (t - 1900), np.uint32), seed, 1)
        ubirth = ub[:, 0]                       # birth uniform is slot 0 of the year stream (round 0)
        ROUNDS = getattr(simulate_ref, "rounds", 2)
        NBLK = (13 + 4 * Kc + 3) // 4
        for rnd in range(ROUNDS):
            u24, raw24 = uniforms(idx, np.full(WPT, 1 + (t - 1900) + (400 if rnd else 0), np.uint32),
                                  seed, NBLK)
            if rnd == 0:
                sep = past & (st == 1) & (u24[:, 1] < dsep)
                st[sep] = 2
                st0 = past & (st == 0) & ~sep
            else:
                st0 = past & (st == 0) & (a >= mk) & (a <= 45)
            Ind = np.where(scen == 0, ind0, np.zeros(WPT))
            if scen != 0:
                x = np.clip((gdp[np.clip(t - 1925, 0, 125)] - 6.5) / 2.2, 0., 1.4)
                Ind = x + .12 * (q - 2) + .10 * U
            K = K0 * sy_exp(-th_k * Ind)
            sh = np.where(a <= 28, 1.0, sy_exp(-.15 * (a - 28).astype(np.float64)))
            parr = 1.0 - sy_exp(-a0 * Efc * K * sh)
            # --- arranged path: the original retries up to 8 times for an eligible man
            claimed = np.full(WPT, -1); is_arr = np.zeros(WPT, bool)
            go_arr = st0 & (u24[:, 2] < parr) if rnd == 0 else np.zeros(WPT, bool)  # one arranged attempt per year
            for k in range(8):
                jm_a = np.floor(u24[:, 3 + k] * nm).astype(np.int64)
                mo = cell * nmax + jm_a
                agem = t - mb[mo]
                lo = np.maximum(mexc[mo], 20)
                ok = go_arr & (claimed < 0) & (mav[mo] == 1) & (agem >= lo) & (agem <= 55)
                claimed = np.where(ok, jm_a, claimed); is_arr = np.where(ok, True, is_arr)
            # --- market: sample up to 3*Kc men to get Kc available-and-eligible ones
            need = st0 & (claimed < 0) & (a >= mk) & (a <= 45)
            s_ = 1.0 + lam_s * Ind
            Rw = R0 + rho_a * (a - mk).astype(np.float64)
            bu = np.full(WPT, -1e9); jb = np.full(WPT, -1); nv = np.zeros(WPT, np.int64)
            for k in range(3 * Kc):
                val = need & (nv < Kc) & (mav[cell * nmax + np.floor(u24[:, 12 + k] * nm).astype(np.int64)] == 1)
                jm_c = np.floor(u24[:, 12 + k] * nm).astype(np.int64)
                moc = cell * nmax + jm_c
                agemc = t - mb[moc]
                loc = np.maximum(mexc[moc], 20)
                val = need & (nv < Kc) & (mav[moc] == 1) & (agemc >= loc) & (agemc <= 55)
                if not val.any(): continue
                nois = np.take_along_axis(u24, (12 + 3 * Kc + np.minimum(nv, Kc - 1))[:, None], axis=1)[:, 0]
                g = (yrs[med[moc]] - yrs[ed]) / 12.0
                uu = -al_d * s_ * np.maximum(-g, 0.) - al_u * np.maximum(g, 0.) + 0.5 * sy_log(nois / (1.0 - nois))
                better = val & (uu > bu)
                bu = np.where(better, uu, bu); jb = np.where(better, jm_c, jb)
                nv = nv + val
            mkt = need & (jb >= 0) & (bu + Rw > 0.0)
            jbs = np.maximum(jb, 0)
            mob = cell * nmax + jbs
            g2 = (yrs[ed] - yrs[med[mob]]) / 12.0
            un2 = u24[:, 12 + 4 * Kc]
            um_acc = -al_m * np.maximum(g2, 0.) + Rm + 0.5 * sy_log(un2 / (1.0 - un2))
            acc = mkt & (um_acc > 0.0)
            claimed = np.where(acc, jb, claimed)
            is_arr = np.where(acc, False, is_arr)
            co = claimed >= 0
            mgid = cell * nmax + np.maximum(claimed, 0)
            key = (((t - 1900) << 39) | (is_arr.astype(np.uint64) << 38)
                   | (raw24[:, 11].astype(np.uint64) << 6) | within.astype(np.uint64)) + np.uint64(1)
            mkey = np.zeros(MPT, np.uint64)
            np.maximum.at(mkey, mgid[co], key[co])
            win = co & (mkey[mgid] == key)
            st[win] = 1; afm[win] = a[win]; mav[mgid[win]] = 0

        # ---- births
        stb = st
        cond = past & ((stb > 0) | (a <= 40))
        phi = 2.0 * sy_exp(-th_f * Ind) - 1.0
        Di = Dlo + (Dhi - Dlo) * .5 * (1.0 + phi)
        cost = c0 * (1 - .9 * K) * (1 + .1 * par)
        S_ = 1.0 / (1.0 + sy_exp(-(Di - par - .5) / sd_d))
        base_h = phi0 * HUT[np.clip(a, 0, 49)] * S_ * sy_exp(-cost)
        hz = np.where(stb == 1, base_h, np.where(stb == 2, base_h * K, eps * HUT[np.clip(a, 0, 49)] * sy_exp(-cost)))
        hz = np.where(cond, hz, 0.0)
        birthed = cond & (hz > 0) & (ubirth < 1.0 - sy_exp(-hz))
        np.add.at(births, ti * 35 + ai[birthed], wt[birthed])
        first = birthed & (par == 0)
        afb_s[ti] += float((wt[first] * a[first]).sum())
        afb_n[ti] += float(wt[first].sum())
        afbw[first] = a[first]
        par[birthed] += 1
        b30[birthed & (a < 30)] += 1
        b35[birthed & (a < 35)] += 1

    # ---------------------------------------------------------------- end of run
    ok18 = (b + 18 <= tmax)
    np.add.at(m18d, b[ok18] - 1925, wt[ok18])
    s18 = ok18 & (afm >= 0) & (afm < 18)
    np.add.at(m18n, b[s18] - 1925, wt[s18])
    coh = np.zeros((14, 7, 8))
    for cc in range(14):
        y0 = 1930 + 5 * cc
        if y0 + 4 + 49 > tmax: continue
        sel = (cell // 2) == cc
        for L in range(7):
            m2 = sel & (ed == L)
            if not m2.any(): continue
            w = wt[m2]; pp = par[m2]
            coh[cc, L, 0] = w.sum(); coh[cc, L, 1] = (w * b30[m2]).sum()
            coh[cc, L, 2] = (w * b35[m2]).sum(); coh[cc, L, 3] = (w * pp).sum()
            coh[cc, L, 4] = w[pp == 0].sum()
            nz = pp > 0
            coh[cc, L, 6] = (w[nz] * afbw[m2][nz]).sum(); coh[cc, L, 7] = w[nz].sum()
            coh[cc, L, 5] = (w * (afm[m2] >= 0)).sum()
    return dict(births=births.reshape(101, 35), expo=expo.reshape(101, 35), sing=sing.reshape(101, 35),
                afb_s=afb_s, afb_n=afb_n, m18n=m18n, m18d=m18d, coh=coh,
                state=dict(st=st, par=par, afm=afm, ed=ed, born=b, ex=e, mk=mk,
                           b30=b30, b35=b35, afbw=afbw, mav=mav))
