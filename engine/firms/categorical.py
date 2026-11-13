"""Categorical core of the youth labour market (Tilly, Durable Inequality, 1998).

Tilly's claim is architectural: durable inequality arises when paired, unequal CATEGORIES (citizen/alien, degree/no
degree, insider/outsider) are matched to ORGANIZATIONAL BOUNDARIES (who may enter which position), because the match
solves organizational problems. Four mechanisms do the work:
  exploitation        a category commanding a resource takes part of the value produced by outsiders' effort
  opportunity hoarding a network-bounded category keeps access to a valuable, renewable resource for its members
  emulation           organizations copy categorical distinctions from other organizations, whatever their efficiency
  adaptation          everyday routines (strategies of the subordinate as well as the dominant) that make the categorical
                      system livable, and so lock it in
So here the primitives are categories and positions, not "skilled" and "unskilled" labour. A worker is a cell in
(credential: degree / none) x (network: insider / outsider). In China the insider line is chiefly local urban hukou plus
family connections; in Cambodia it would be patronage networks. A position is a segment with an entry rule:
  sec   secure state / SOE posts: degree required; a fixed, rationed number of openings; a share `hoard` is filled inside
        the insider network before the rest go to an open exam (opportunity hoarding)
  grad  private graduate jobs: degree required by task; free entry of vacancies (as in model.py)
  open  non-graduate jobs: open to all, EXCEPT that a share c_t of employers require a degree, and c_t spreads by
        imitation once degrees are common in the youth labour force (emulation; Dore 1976, Collins 1979)
Exploitation: in open jobs outsiders are paid (1 - ex) w and their outside option is (1 - ex) z (no local entitlements);
the employer keeps the wedge as rent (recorded in a ledger), which makes outsiders cheaper to hire. Adaptation: unemployed graduates may leave the labour force to wait and
prepare for secure posts (exam preparation); the flow depends on their realised chance of a post and on family support,
which differs by category. Waiting is not unemployment in NBS terms, so adaptation moves people out of the measured rate.

The results are not only about inequality. Hoarding and waiting change participation and the measured unemployment
rate; emulation lowers the number of vacancies firms find worth posting (fewer applicants per degree-only vacancy) and so
output; exploitation changes which workers firms hire and therefore who downgrades.

Nesting (a tier-1 test): with the secure segment closed, no waiting, no emulation and ex = 0, this module reproduces
model.YouthMarket to floating-point precision, and splitting any group into insider/outsider categories that no
boundary treats differently changes no aggregate (Tilly's point that categories matter only through boundaries).
"""
import math
import numpy as np
from . import model as M

TILLY_DEFAULTS = dict(
    ins_g=0.5, ins_n=0.5,            # insider share among graduates / non-graduates entering the youth labour force
    # opportunity hoarding in secure posts
    sec_open=0.0,                    # secure openings per year as a share of the 2018-19 graduate entry flow (0 = closed)
    hoard=0.0,                       # share of secure openings filled inside the insider network first
    sec_prem=1.25,                   # secure wage relative to the reference graduate wage (pay scale + security, fixed)
    s_sec=0.004, chi_s=0.2,          # separation from secure posts; application intensity of searching (not waiting) grads
    # adaptation: waiting for secure posts outside the labour force
    wait_max=0.0,                    # max monthly flow from unemployment into waiting (0 = no waiting)
    wait_scale=0.5, wait_quit=1 / 12,  # logistic scale of the waiting decision (value units); monthly exit back to search
    supp_in=1.0, supp_out=0.5,       # share of each category whose family can finance a wait
    z_ins=0.0,                       # extra flow value of unemployment for insiders (family resources)
    # emulation: degree requirements in non-graduate jobs
    em_rate=0.0, em_threshold=0.40, c0=0.02,     # logistic diffusion when the degree share of the LF exceeds threshold
    # exploitation: wage wedge on outsiders in open jobs (share of w - z kept by the employer)
    ex=0.0,
)

GROUPS = [('G_in', True, True), ('G_out', True, False), ('N_in', False, True), ('N_out', False, False)]


def _tiers(types):
    """Group applicant types with equal value to the firm (ties are hired at random among themselves)."""
    idx = sorted([i for i, (x, _) in enumerate(types) if x > 0], key=lambda i: -types[i][1])
    tiers = []
    for i in idx:
        if tiers and abs(types[tiers[-1][0]][1] - types[i][1]) <= 1e-12 * max(1.0, abs(types[i][1])):
            tiers[-1].append(i)
        else:
            tiers.append([i])
    return tiers


def _rank_value(types, rank):
    """types: list of (x_i, J_i). Expected value of one vacancy under ranking by value or random choice."""
    if not any(x > 0 for x, _ in types):
        return 0.0
    tiers = _tiers(types) if rank == 'value' else [[i for i, (x, _) in enumerate(types) if x > 0]]
    v, surv = 0.0, 1.0
    for t in tiers:
        X = sum(types[i][0] for i in t)
        v += surv * (1 - math.exp(-X)) * sum(types[i][0] * types[i][1] for i in t) / X
        surv *= math.exp(-X)
    return v


def _rank_hires(V, types, rank):
    """Hires of each type per V vacancies (same order as `types`)."""
    out = [0.0] * len(types)
    if V <= 0 or not any(x > 0 for x, _ in types):
        return out
    tiers = _tiers(types) if rank == 'value' else [[i for i, (x, _) in enumerate(types) if x > 0]]
    surv = 1.0
    for t in tiers:
        X = sum(types[i][0] for i in t)
        h = V * surv * (1 - math.exp(-X))
        for i in t:
            out[i] = h * types[i][0] / X
        surv *= math.exp(-X)
    return out


class CategoricalMarket(M.YouthMarket):
    def __init__(self, data, **over):
        tk = {k: over.pop(k) for k in list(over) if k in TILLY_DEFAULTS}
        super().__init__(data, **over)
        self.t = dict(TILLY_DEFAULTS, **tk)

    def run(self):
        if not hasattr(self, 't'):                 # reference pass from the parent's __init__
            return M.YouthMarket.run(self)
        p, D, T = self.p, self.data, self.t
        a, r = p['a'], p['r']
        G = p['grad_supply'] or D.graduates
        NL = p['nongrad_supply'] or D.nongrad_school_leavers
        p = dict(p); p['s_g'] *= p['sep_scale']; p['s_n'] *= p['sep_scale']; p['s_gn'] *= p['sep_scale']
        dg, dn, dgn = r + p['s_g'] + p['age_g'], r + p['s_n'] + p['age_n'], r + p['s_gn'] + p['age_g']
        dsec = r + T['s_sec'] + p['age_g']
        w_g0 = p['p_g0'] * (1 - p['m_g']); w_n0 = p['p_n0'] * (1 - p['m_n'])
        om_g = (w_g0 - p['z_g']) / (p['p_g0'] - p['z_g']); om_n = (w_n0 - p['z_n']) / (p['p_n0'] - p['z_n'])
        kap_g = (1 - math.exp(-M.urn_x_from_f(p['f_g_ref'], a))) * (p['p_g0'] - w_g0) / dg
        kap_n = (1 - math.exp(-M.urn_x_from_f(p['f_n_ref'], a))) * (p['p_n0'] - w_n0) / dn
        SG_ref, SN_ref = p['S_ref']
        w_sec = T['sec_prem'] * w_g0
        sec_per_month = T['sec_open'] * p['psi_g'] * 0.5 * (G(2018) + G(2019)) / 12
        names = [g[0] for g in GROUPS]; deg = {g[0]: g[1] for g in GROUPS}; ins = {g[0]: g[2] for g in GROUPS}
        dgroups = [k for k in names if deg[k]]; ngroups = [k for k in names if not deg[k]]
        U = {k: 0.0 for k in names}; W = {k: 0.0 for k in dgroups}
        Eg = {k: 0.0 for k in dgroups}; Es = {k: 0.0 for k in dgroups}; Eo = {k: 0.0 for k in names}
        S_un = S_sig = 0.0; pending = 0.0
        w_g, w_n = w_g0, w_n0
        c = 0.0                                  # share of non-graduate vacancies requiring a degree
        qsec = {k: 0.05 for k in dgroups}
        hist_G, hist_N = [], []
        share_g = {'G_in': T['ins_g'], 'G_out': 1 - T['ins_g']}
        share_n = {'N_in': T['ins_n'], 'N_out': 1 - T['ins_n']}
        keys = ('year', 'month', 'rate_old', 'rate_new', 'slack', 'LF_G', 'LF_N', 'f_g', 'p_g', 'p_n', 'w_g', 'w_n', 'V_g',
                'V_n', 'A', 'u_G', 'u_N', 'under', 'grad_share_n_hires', 'resid_n', 'balance', 'c_req', 'waiting',
                'sec_hires', 'sec_ins_share', 'rent_exploit', 'rent_hoard', 'output') + tuple(
                f'u_{k}' for k in names) + tuple(f'w_{k}' for k in names) + tuple(f'E_sec_{k}' for k in dgroups)
        out = {k: [] for k in keys}
        t_ref = p['ref_years'][0] + 0.5 * (p['ref_years'][1] - p['ref_years'][0]) + 0.5
        for y, m in M._months(p['start'], p['end']):
            tt = y + (m - 0.5) / 12 - t_ref
            A = self.A_at(y, m)
            lfg = sum(U[k] + Eg[k] + Eo[k] + Es[k] for k in dgroups); lfn = sum(U[k] + Eo[k] for k in ngroups)
            hist_G.append(lfg); hist_N.append(lfn)
            LF_G = float(np.mean(hist_G[-12:])); LF_N = float(np.mean(hist_N[-12:]))
            warm = (y, m) < p['warm_until']
            sig = math.inf if warm else p['sigma_A']
            Dg = 1.0
            if p['grad_demand'] == 'observed' and not warm:
                Dg = D.property_index(y, m) ** p['e_prop'] * (1 - p['dr_drop'] * ((y, m) >= (2021, 8)))
                if p['grad_shift'] is not None:
                    Dg *= p['grad_shift'](y, m)
            p_g = Dg * A * p['p_g0'] * M.ces_relative(max(LF_G, 1e-9), SG_ref * math.exp(p['g_H'] * tt), sig)
            p_n = A * p['p_n0'] * M.ces_relative(max(LF_N, 1e-9), SN_ref * math.exp(p['g_N'] * tt), sig)
            lg, ln = (1.0, 1.0) if warm else (p['lam_g'], p['lam_n'])
            w_g += lg * (p['z_g'] + om_g * (p_g - p['z_g']) - w_g)
            w_n += ln * (p['z_n'] + om_n * (p_n - p['z_n']) - w_n)
            # exploitation: outsiders in open jobs are paid less than the bargained wage; the employer keeps the wedge
            # outsiders' outside option is worse (no local entitlements), which is what lets the wedge stick
            wo = {k: (w_n if ins[k] else (1 - T['ex']) * w_n) for k in names}
            z = {k: ((p['z_g'] if deg[k] else p['z_n']) * (1 if ins[k] else 1 - T['ex'])) + (T['z_ins'] if ins[k] else 0.0)
                 for k in names}
            J_g = (p_g - w_g) / dg
            Jo = {k: ((p_n * (1 + p['eps']) - wo[k]) / dgn if deg[k] else (p_n - wo[k]) / dn) for k in names}
            if m == 9:
                S_un, S_sig = p['psi_g'] * G(y + 1), 0.0
            searching = m >= 9 or m <= 6
            stud = p['zeta'] * S_un if searching else 0.0
            # ---- 1. secure posts: rationed openings, hoarded share to insiders first, then an open exam
            hS = {k: 0.0 for k in dgroups}; hS_W = {k: 0.0 for k in dgroups}
            if sec_per_month > 0:
                app = {k: W[k] + T['chi_s'] * U[k] for k in dgroups}
                O = sec_per_month
                O_h = T['hoard'] * O
                ins_app = sum(app[k] for k in dgroups if ins[k])
                h_ins = O_h * (1 - math.exp(-ins_app / O_h)) if O_h > 0 and ins_app > 0 else 0.0
                for k in dgroups:
                    if ins[k] and ins_app > 0:
                        hS[k] += h_ins * app[k] / ins_app
                O_o = O - h_ins
                rest = {k: app[k] - hS[k] for k in dgroups}
                tot = sum(rest.values())
                h_open = O_o * (1 - math.exp(-tot / O_o)) if O_o > 0 and tot > 0 else 0.0
                for k in dgroups:
                    if tot > 0:
                        hS[k] += h_open * rest[k] / tot
                for k in dgroups:                          # split each group's secure hires between waiters and searchers
                    if app[k] > 0:
                        hS_W[k] = hS[k] * W[k] / app[k]
                    qsec[k] = 0.7 * qsec[k] + 0.3 * (hS[k] / app[k] if app[k] > 0 else 0.0)
            hS_U = {k: hS[k] - hS_W[k] for k in dgroups}
            # ---- 2. private graduate jobs (free entry, closed form as in model.py)
            UGav = {k: U[k] - hS_U[k] for k in dgroups}
            Ueff = sum(UGav.values()) + p['chi'] * sum(Eo[k] for k in dgroups) + stud
            kg = kap_g * A
            if J_g > kg and Ueff > 0:
                x = -math.log(1 - kg / J_g)
                f_g = a * (1 - math.exp(-x)) / x
                V_g = a * Ueff / x
            else:
                f_g, V_g = 0.0, 0.0
            hG_U = {k: f_g * UGav[k] for k in dgroups}
            hG_O = {k: f_g * p['chi'] * Eo[k] for k in dgroups}
            hG_S = f_g * stud
            # ---- 3. downgrading decision and adaptation (waiting) for unemployed graduates
            phi, wflow = {}, {k: 0.0 for k in dgroups}
            for k in dgroups:
                dz = (dg * z[k] + f_g * w_g) / (dg + f_g)                          # reservation value rU
                phi[k] = 1 / (1 + math.exp(-((wo[k] - p['d']) - dz) / (p['nu'] * p['p_n0'])))
                if T['wait_max'] > 0 and sec_per_month > 0:
                    gain = qsec[k] * (w_sec - dz) / dsec - f_g * (w_g - dz) / dg
                    supp = T['supp_in'] if ins[k] else T['supp_out']
                    wflow[k] = T['wait_max'] * supp / (1 + math.exp(-gain / T['wait_scale']))
            # ---- 4. non-graduate jobs: ranking (or random), a share c requiring a degree (emulation)
            Gapp = {k: phi[k] * (UGav[k] - hG_U[k]) * (1 - wflow[k]) for k in dgroups}
            UNt = sum(U[k] for k in ngroups); Gt = sum(Gapp.values())
            kn = kap_n * A
            hO = {k: 0.0 for k in names}; V_n = 0.0; resid = 0.0
            if UNt + Gt > 0:
                base = UNt if UNt > 0 else Gt
                openfrac = 1 - c

                def types(xb):
                    xs = {}
                    for k in dgroups:
                        xs[k] = xb * Gapp[k] / base
                    for k in ngroups:
                        xs[k] = (xb * U[k] / base / openfrac) if openfrac > 1e-12 else 0.0
                    return xs

                def value(xb):
                    xs = types(xb)
                    v_open = _rank_value([(xs[k], Jo[k]) for k in names], p['rank'])
                    if c <= 0:
                        return v_open
                    v_req = _rank_value([(xs[k], Jo[k]) for k in dgroups], p['rank'])
                    return openfrac * v_open + c * v_req
                if value(200.0) > kn:
                    lo, hi = 1e-12, 200.0
                    for _ in range(100):
                        mid = math.sqrt(lo * hi)
                        if value(mid) > kn:
                            hi = mid
                        else:
                            lo = mid
                    xb = math.sqrt(lo * hi)
                    resid = value(xb) - kn
                    V_n = a * base / xb
                    xs = types(xb)
                    ho = _rank_hires(V_n * openfrac, [(xs[k], Jo[k]) for k in names], p['rank'])
                    for k, h in zip(names, ho):
                        hO[k] += h
                    if c > 0:
                        hr = _rank_hires(V_n * c, [(xs[k], Jo[k]) for k in dgroups], p['rank'])
                        for k, h in zip(dgroups, hr):
                            hO[k] += h
            # emulation: degree requirements spread as degrees become the norm in the youth labour force
            if T['em_rate'] > 0 and not warm:
                sG = lfg / (lfg + lfn) if lfg + lfn > 0 else 0.0
                c = min(max(c + T['em_rate'] * (c + T['c0']) * (1 - c) * (sG - T['em_threshold']), 0.0), 0.99)
            # ---- 5. entry
            infl = {k: 0.0 for k in names}; signed = {k: 0.0 for k in dgroups}
            if m == 7:
                cls = p['psi_g'] * G(y)
                for k in dgroups:
                    signed[k] = S_sig * share_g[k]
                pending = cls - S_sig
                S_un = S_sig = 0.0
            if m >= 7 and pending > 0:
                tot_in = pending * (p['july_g'] if m == 7 else (1 - p['july_g']) / 5)
                for k in dgroups:
                    infl[k] = tot_in * share_g[k]
            nin = p['psi_n'] * NL(y) * (p['july_n'] if m == 7 else (1 - p['july_n']) / 11)
            for k in ngroups:
                infl[k] = nin * share_n[k]
            # ---- 6. stocks
            stock = lambda: (sum(U.values()) + sum(W.values()) + sum(Eg.values()) + sum(Es.values()) + sum(Eo.values()))
            before = stock()
            age_out = sum(p['age_g'] * (U[k] + W[k] + Eg[k] + Es[k] + Eo[k]) for k in dgroups) + \
                sum(p['age_n'] * (U[k] + Eo[k]) for k in ngroups)
            for k in dgroups:
                u, wt, eg, es, eo = U[k], W[k], Eg[k], Es[k], Eo[k]
                to_wait = wflow[k] * (UGav[k] - hG_U[k])
                hOk = hO[k]
                U[k] = u + infl[k] - hS_U[k] - hG_U[k] - hOk - to_wait + T['wait_quit'] * wt + p['s_g'] * eg \
                    + p['s_gn'] * eo + T['s_sec'] * es - p['age_g'] * u
                W[k] = wt + to_wait - hS_W[k] - T['wait_quit'] * wt - p['age_g'] * wt
                Eg[k] = eg + hG_U[k] + hG_O[k] + signed[k] - p['s_g'] * eg - p['age_g'] * eg
                Es[k] = es + hS[k] - T['s_sec'] * es - p['age_g'] * es
                Eo[k] = eo + hOk - hG_O[k] - p['s_gn'] * eo - p['age_g'] * eo
            for k in ngroups:
                u, eo = U[k], Eo[k]
                U[k] = u + infl[k] - hO[k] + p['s_n'] * eo - p['age_n'] * u
                Eo[k] = eo + hO[k] - p['s_n'] * eo - p['age_n'] * eo
            if searching:
                S_un -= hG_S; S_sig += hG_S
            balance = stock() - (before + sum(infl.values()) - age_out) - sum(signed.values())
            # ---- 7. observation and ledger
            Ut = sum(U.values()); Wt = sum(W.values())
            LF = sum(U.values()) + sum(Eg.values()) + sum(Es.values()) + sum(Eo.values())
            su = p['zeta'] * S_un if searching else 0.0
            LG = sum(U[k] + Eg[k] + Es[k] + Eo[k] for k in dgroups); LN = sum(U[k] + Eo[k] for k in ngroups)
            hGn = sum(hO[k] for k in dgroups); hNn = sum(hO[k] for k in ngroups)
            Eemp_g = sum(Eg[k] + Es[k] + Eo[k] for k in dgroups)
            rec = dict(year=y, month=m, rate_new=100 * Ut / LF if LF > 0 else float('nan'),
                       rate_old=100 * (Ut + su) / (LF + su) if LF > 0 else float('nan'),
                       slack=100 * (Ut + Wt) / (LF + Wt) if LF > 0 else float('nan'),
                       LF_G=LG, LF_N=LN, f_g=f_g, p_g=p_g, p_n=p_n, w_g=w_g, w_n=w_n, V_g=V_g, V_n=V_n, A=A,
                       u_G=100 * sum(U[k] for k in dgroups) / LG if LG > 0 else 0.0,
                       u_N=100 * sum(U[k] for k in ngroups) / LN if LN > 0 else 0.0,
                       under=100 * sum(Eo[k] for k in dgroups) / Eemp_g if Eemp_g > 0 else 0.0,
                       grad_share_n_hires=hGn / (hGn + hNn) if hGn + hNn > 0 else 0.0, resid_n=resid, balance=balance,
                       c_req=c, waiting=Wt, sec_hires=sum(hS.values()),
                       sec_ins_share=(hS['G_in'] / sum(hS.values())) if sum(hS.values()) > 0 else float('nan'),
                       rent_exploit=sum((w_n - wo[k]) * Eo[k] for k in names),
                       rent_hoard=sum((w_sec - w_g) * Es[k] for k in dgroups),
                       output=p_g * sum(Eg.values()) + p_g * sum(Es.values())
                       + p_n * (1 + p['eps']) * sum(Eo[k] for k in dgroups) + p_n * sum(Eo[k] for k in ngroups))
            for k in names:
                lfk = U[k] + Eo[k] + (Eg[k] + Es[k] if deg[k] else 0.0)
                rec[f'u_{k}'] = 100 * U[k] / lfk if lfk > 0 else 0.0
                emp = Eo[k] + (Eg[k] + Es[k] if deg[k] else 0.0)
                rec[f'w_{k}'] = ((wo[k] * Eo[k] + (w_g * Eg[k] + w_sec * Es[k] if deg[k] else 0.0)) / emp) if emp > 0 else 0.0
            for k in dgroups:
                rec[f'E_sec_{k}'] = Es[k]
            for kk in keys:
                out[kk].append(rec[kk])
        self.R = out
        return out
