"""twoway.py — NEW declared two-way education-economy + endogenous shadow-sector model (Loop 2).

NOT massabm, NOT floorworld, NOT triad, NOT a reproduction. Compact numpy cohort-flow model with:
  education -> economy : Vc_t = Vc0*B0*(1+g)^t * (H_{t-d}/H0)^eps_ec     (complex formal jobs)
  economy -> education : adaptive beliefs on hire probabilities/wages drive completion & college entry
  shadow sector        : provider entry (commercial firms + teacher-tutors), tatonnement price,
                         capacity + class-size dilution, and a positional (competition R_gate) demand term.
See loop2/PRE_DECLARATIONS_L2.md for the fully declared design. All numbers are stylized model output.

Usage: python twoway.py --out ../runs/L2 [--seeds 5]
"""
import argparse
import json
import math
import os
import sys

import numpy as np

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bcommon import write_rows, write_text, m_sd  # noqa: E402

N = 1000
BURN = 15
YEARS = 40
CC = 0.85
ANN = float(sum(0.97 ** k for k in range(40)))
Y_BASIC, Y_DIP, Y_COL = 8.0, 12.0, 16.0

COUNTRIES = {
    'PH-like': dict(s0=0.55, c0=0.25, Vc0=0.060, Vr0=0.180, g=0.020, wc0=2.6, wr0=1.6, sigma=2.0,
                    cost_col=0.60, p_tut0=1.0, cap_cm=0.090, cap_tt=0.040, F_cm=0.060, F_tt=0.020,
                    e_cm=0.15, e_tt=0.30, places_S=0.75, births=0.015, inc_sig=0.80,
                    targets=dict(completion=0.750, tertiary_ger=0.530),
                    target_src=dict(completion='GMR observed 2024', tertiary_ger='GMR observed 2026 (GER)')),
    'HK-like': dict(s0=0.80, c0=0.32, Vc0=0.160, Vr0=0.220, g=0.010, wc0=3.0, wr0=1.8, sigma=2.0,
                    cost_col=0.80, p_tut0=2.5, cap_cm=0.080, cap_tt=0.035, F_cm=0.100, F_tt=0.030,
                    e_cm=0.12, e_tt=0.25, places_S=0.95, births=-0.005, inc_sig=0.70,
                    targets=dict(tutoring_senior_sec=0.85, degree_attainment=0.276, postsec_attainment=0.364),
                    target_src=dict(tutoring_senior_sec='Kwo & Bray 2011 (2010, caveat: not statistically robust)',
                                    degree_attainment='EDB 2025 observed', postsec_attainment='EDB 2025 observed')),
    'KHM-like': dict(s0=0.26, c0=0.12, Vc0=0.025, Vr0=0.080, g=0.030, wc0=2.2, wr0=1.4, sigma=2.0,
                     cost_col=0.40, p_tut0=0.5, cap_cm=0.060, cap_tt=0.050, F_cm=0.040, F_tt=0.010,
                     e_cm=0.08, e_tt=0.40, places_S=0.45, births=0.012, inc_sig=0.90,
                     targets=dict(completion=0.279, formal_share=0.117, university_attainment=0.066),
                     target_src=dict(completion='GMR observed 2023', formal_share='CLFS 2019 observed',
                                     university_attainment='CLFS 2019 observed')),
}

REGIMES = {
    'R1_demand_led': dict(eps_ec=0.0, d_ec=0, feedback=1, schooling='endo', shadow='endogenous'),
    'R2_education_led': dict(eps_ec=0.6, d_ec=5, feedback=1, schooling='endo', shadow='endogenous'),
    'R3_complementary': dict(eps_ec=0.3, d_ec=3, feedback=1, schooling='endo', shadow='endogenous'),
    'R4_frozen_schooling': dict(eps_ec=0.3, d_ec=3, feedback=1, schooling='frozen', shadow='endogenous'),
    'R5_frozen_returns': dict(eps_ec=0.3, d_ec=3, feedback=0, schooling='endo', shadow='endogenous'),
    'R6_fixed_supply': dict(eps_ec=0.3, d_ec=3, feedback=1, schooling='endo', shadow='fixed_supply'),
    'R7_no_tutoring': dict(eps_ec=0.3, d_ec=3, feedback=1, schooling='endo', shadow='off'),
    'R8_edled_frozen': dict(eps_ec=0.6, d_ec=5, feedback=1, schooling='frozen', shadow='endogenous'),
    'R9_demand_led_frozen': dict(eps_ec=0.0, d_ec=0, feedback=1, schooling='frozen', shadow='endogenous'),
    'R10_frozen_economy': dict(eps_ec=0.3, d_ec=3, feedback=0, schooling='endo', shadow='endogenous',
                                freeze_economy=True),
}


def sig(x):
    return 1.0 / (1.0 + np.exp(-np.clip(x, -30, 30)))


def feasible_share(cost, inc_sig):
    """P(household income >= 2 x annual college cost) under declared lognormal(median 1, sigma=inc_sig)."""
    x = math.log(max(2.0 * cost, 1e-6))
    return float(0.5 * math.erfc((x - 0.0) / (inc_sig * math.sqrt(2.0))))


def run_country(name, cfg, regime, seed, tut_shift=0.0):
    rng = np.random.default_rng(seed)
    r = REGIMES[regime]
    eps_ec, d_ec, fb = r['eps_ec'], r['d_ec'], r['feedback']
    schooling, shadow = r['schooling'], r['shadow']
    freeze_econ = bool(r.get('freeze_economy', False))
    g = cfg['g']
    # provider counts per 1000 births (initial)
    n_cm, n_tt = 2.0, 6.0
    # beliefs (adaptive) and reference returns
    qc_b, qr_b, wc_b, wr_b = 0.6, 0.3, cfg['wc0'], cfg['wr0']
    H0 = 0.55 * Y_BASIC + 0.35 * Y_DIP + 0.10 * Y_COL   # initial human-capital index (declared)
    ret_S_ref = ret_C_ref = None
    Qd_hist, Qs_hist = [], []
    p_tut = cfg['p_tut0']
    fea = feasible_share(cfg['cost_col'], cfg['inc_sig'])
    # reference beliefs captured at the end of burn-in (used by the frozen-returns arm)
    qc_ref = qr_ref = wc_ref = wr_ref = 0.0
    Vc_frozen = Vr_frozen = None
    # annual cohort record: (basic, diploma, college, formal complex, formal routine)
    cohorts = []

    def H_of(cohorts):
        tot = sum(c[0] + c[1] + c[2] for c in cohorts)
        yrs = sum(c[0] * Y_BASIC + c[1] * Y_DIP + c[2] * Y_COL for c in cohorts)
        return yrs / max(tot, 1e-9)

    def step(t, s_t, c_t, burn=False):
        nonlocal qc_b, qr_b, wc_b, wr_b, H0, ret_S_ref, ret_C_ref, p_tut, n_cm, n_tt
        nonlocal qc_ref, qr_ref, wc_ref, wr_ref, Vc_frozen, Vr_frozen
        Bt = N * (1 + cfg['births']) ** float(t)
        B0 = N
        H = H_of(cohorts) if cohorts else H0
        lagH = H_of(cohorts[:-d_ec]) if (d_ec > 0 and len(cohorts) > d_ec) else H
        # declared stochastic demand shocks (multiplicative lognormal, sd 0.06) -> seed dispersion
        shock = math.exp(0.06 * float(rng.standard_normal()))
        Vc = cfg['Vc0'] * B0 * (1 + g) ** max(t, 0) * (max(lagH, 1e-9) / max(H0, 1e-9)) ** eps_ec * shock
        Vr = cfg['Vr0'] * B0 * (1 + g) ** max(t, 0) * shock
        if freeze_econ and Vc_frozen is not None:
            Vc, Vr = Vc_frozen, Vr_frozen
        # pipeline (declared 4/4-year lags): secondary completions at t from births at t-16 and s at t-4
        if burn:
            S_t = cfg['s0'] * Bt
            C_ent = cfg['c0'] * S_t
            C_t = CC * cfg['c0'] * cfg['s0'] * Bt
            D_t = (1 - cfg['c0']) * S_t
            X_t = (1 - cfg['s0']) * Bt
        else:
            S_t = s_t * N * (1 + cfg['births']) ** (t - 16)
            C_ent = c_t * S_t
            C_t = CC * c_t * N * (1 + cfg['births']) ** (t - 20)
            D_t = (1 - c_t) * S_t
            X_t = (1 - s_t) * N * (1 + cfg['births']) ** (t - 20)
        # hiring
        comp = min(C_t, Vc)
        left_col = max(C_t - comp, 0.0)
        rout_D = min(D_t, Vr)
        rout_C = min(left_col, max(Vr - rout_D, 0.0))
        rout = rout_D + rout_C
        inf = max(C_t + D_t + X_t - comp - rout, 0.0)
        cohorts.append([X_t, D_t, C_t, comp, rout])
        if len(cohorts) > 40:
            cohorts.pop(0)
        # observed probabilities and wages
        qc = comp / max(C_t, 1e-9)
        qr = rout_D / max(D_t, 1e-9)
        wc = np.clip(cfg['wc0'] * (Vc / max(C_t, 1e-9)) ** (1 / cfg['sigma']), 1.0, 4 * cfg['wc0'])
        wr = np.clip(cfg['wr0'] * (Vr / max(D_t, 1e-9)) ** (1 / cfg['sigma']), 1.0, 3 * cfg['wr0'])
        if not burn:
            lam = 0.7
            qc_b = lam * qc_b + (1 - lam) * qc
            qr_b = lam * qr_b + (1 - lam) * qr
            wc_b = lam * wc_b + (1 - lam) * wc
            wr_b = lam * wr_b + (1 - lam) * wr
            if fb == 0 and ret_S_ref is not None:
                qc_b, qr_b, wc_b, wr_b = qc_ref, qr_ref, wc_ref, wr_ref
        ret_S = (qr_b * wr_b + (1 - qr_b) * 1.0 - 1.0) * ANN
        ret_C = (CC * (qc_b * wc_b + (1 - qc_b) * 1.0) - (qr_b * wr_b + (1 - qr_b) * 1.0)) * ANN - 4 * cfg['cost_col']
        if burn:
            ret_S_ref, ret_C_ref = ret_S, ret_C
            qc_ref, qr_ref, wc_ref, wr_ref = qc_b, qr_b, wc_b, wr_b
        # positional competition
        R_S = Bt / max(cfg['places_S'] * B0, 1e-9)
        R_C = (C_ent + 1e-9) / max(Vc, 1e-9)
        # tutoring demand (positional + returns - price), realized through capacity
        T_S = sig(-1.0 + tut_shift + 0.9 * math.log1p(max(ret_S, 0.0)) + 0.7 * math.log(max(R_S, 1e-6))
                  - 1.1 * (p_tut / max(ret_S + 2.0, 0.5)))
        T_C = sig(-1.6 + tut_shift + 0.9 * math.log1p(max(ret_C, 0.0)) + 0.8 * math.log(max(R_C, 1e-6))
                  - 1.1 * (p_tut / max(ret_C + 2.0, 0.5)))
        Qd = Bt * T_S + C_ent * T_C
        Qs = (n_cm * cfg['cap_cm'] + n_tt * cfg['cap_tt']) * B0
        util = min(1.0, Qs / max(Qd, 1e-9)) if Qd > 0 else 1.0
        take_S = T_S * util
        take_C = T_C * util
        quality = (min(1.0, Qs / max(Qd, 1e-9))) ** 0.3 if Qd > 0 else 1.0
        # price tatonnement
        gap = (Qd - Qs) / max(Qs, 1e-9)
        p_tut = float(np.clip(p_tut * (1 + 0.15 * np.clip(gap, -0.5, 0.5)),
                              0.2 * cfg['p_tut0'], 5.0 * cfg['p_tut0']))
        # provider entry / exit (profit sign from last year's utilisation and price)
        if shadow == 'endogenous' and not burn and t > 1:
            utilisation = util
            pi_cm = p_tut * cfg['cap_cm'] * utilisation - cfg['F_cm']
            pi_tt = p_tut * cfg['cap_tt'] * utilisation - cfg['F_tt']
            n_cm = float(np.clip(n_cm * (1 + cfg['e_cm'] * np.tanh(pi_cm / max(cfg['F_cm'], 1e-6))), 0.2, 40.0))
            n_tt = float(np.clip(n_tt * (1 + cfg['e_tt'] * np.tanh(pi_tt / max(cfg['F_tt'], 1e-6))), 0.5, 120.0))
        Qd_hist.append(Qd); Qs_hist.append(Qs)
        return dict(S_t=S_t, C_t=C_t, D_t=D_t, X_t=X_t, comp=comp, rout=rout, inf=inf,
                    Vc=Vc, Vr=Vr, H=H, qc=qc, qr=qr, wc=wc, wr=wr,
                    take_S=take_S, take_C=take_C, price=p_tut, n_cm=n_cm, n_tt=n_tt,
                    quality=quality, Qd=Qd, Qs=Qs, R_S=R_S, R_C=R_C,
                    ret_S=ret_S, ret_C=ret_C, s_t=s_t, c_t=c_t)

    # ---------------- burn-in (schooling fixed; jobs grow; beliefs adapt)
    for t in range(-BURN, 0):
        step(t, cfg['s0'], cfg['c0'], burn=True)
    # ---------------- horizon: reference H and previous-year state from the burn-in
    H0 = H_of(cohorts)
    # frozen-economy arm: hold vacancies at their t=0 values for the whole horizon
    Bt0 = N
    H0_for_jobs = H0
    Vc_frozen = cfg['Vc0'] * Bt0 * (max(H0_for_jobs, 1e-9) / max(H0_for_jobs, 1e-9)) ** eps_ec
    Vr_frozen = cfg['Vr0'] * Bt0
    prev_ret_S, prev_ret_C = ret_S_ref, ret_C_ref
    prev_take_S, prev_take_C = 0.0, 0.0
    series = []
    for t in range(0, YEARS):
        if schooling == 'frozen':
            s_t, c_t = cfg['s0'], cfg['c0']
        else:
            # economy -> education: completion and college entry respond to expected returns
            s_t = sig(math.log(cfg['s0'] / (1 - cfg['s0'])) + 2.5 * (prev_ret_S - ret_S_ref) / ANN
                      + 0.8 * prev_take_S + 0.15 * float(rng.standard_normal()))
            logit_c = math.log(cfg['c0'] / (1 - cfg['c0'])) + 2.5 * (prev_ret_C - ret_C_ref) / ANN + 0.8 * prev_take_C \
                + 0.15 * float(rng.standard_normal())
            c_t = float(np.clip(sig(logit_c) * fea, 0.01, 0.98))
            s_t = float(np.clip(s_t, 0.05, 0.98))
        out = step(t, s_t, c_t, burn=False)
        series.append(out)
        prev_ret_S, prev_ret_C = out['ret_S'], out['ret_C']
        prev_take_S, prev_take_C = out['take_S'], out['take_C']
    return series


def summarise(series):
    def arr(k):
        return np.array([s[k] for s in series], float)
    tot = arr('C_t') + arr('D_t') + arr('X_t')
    formal = arr('comp') + arr('rout')
    return dict(
        completion=arr('s_t'), college_entry=arr('c_t'),
        degree_share=arr('C_t') / np.maximum(tot, 1e-9),
        formal_share=formal / np.maximum(tot, 1e-9),
        complex_jobs=arr('comp'), complex_vac=arr('Vc'),
        complex_share=arr('comp') / np.maximum(formal, 1e-9),
        H=arr('H'), qc=arr('qc'), qr=arr('qr'), wc=arr('wc'), wr=arr('wr'),
        take_S=arr('take_S'), take_C=arr('take_C'), price=arr('price'),
        n_cm=arr('n_cm'), n_tt=arr('n_tt'), Qd=arr('Qd'), Qs=arr('Qs'),
        R_S=arr('R_S'), R_C=arr('R_C'), ret_S=arr('ret_S'), ret_C=arr('ret_C'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', required=True)
    ap.add_argument('--seeds', type=int, default=5)
    ap.add_argument('--calibrate', type=int, default=1,
                    help='1 = calibrate the common shadow-demand shift to HK senior-sec take-up 0.85; '
                         '0 = uncalibrated (shift=0) for the sensitivity table')
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    seeds = list(range(a.seeds))
    # ---- declared calibration of ONE household-demand parameter (common demand shift) to the one
    # verified shadow-education target: HK senior-secondary take-up 0.85 (Kwo & Bray 2011, caveat).
    hk = COUNTRIES['HK-like']
    def hk_take(shift):
        vals = []
        for sd_ in seeds:
            Sp = run_country('HK-like', hk, 'R3_complementary', sd_, tut_shift=shift)
            vals.append(float(np.mean([x['take_S'] for x in Sp[-5:]])))
        return float(np.mean(vals)), float(np.std(vals))
    if a.calibrate:
        lo, hi = -4.0, 4.0
        for _ in range(24):
            mid = (lo + hi) / 2
            v, _ = hk_take(mid)
            if v < 0.85:
                lo = mid
            else:
                hi = mid
        tut_shift = (lo + hi) / 2
    else:
        tut_shift = 0.0
    hk_take_val = hk_take(tut_shift)[0]
    print(f'calibrated demand shift = {tut_shift:.4f}; HK senior-sec take-up (y40) = {hk_take_val:.3f}', flush=True)
    rows, refs = [], []
    failures = []
    for cname, cfg in COUNTRIES.items():
        for regime in REGIMES:
            for seed in seeds:
                try:
                    S = run_country(cname, cfg, regime, seed, tut_shift=tut_shift)
                    sm = summarise(S)
                    for t in range(YEARS):
                        rows.append(dict(country=cname, regime=regime, seed=seed, year=t,
                                         completion=float(sm['completion'][t]),
                                         college_entry=float(sm['college_entry'][t]),
                                         degree_share=float(sm['degree_share'][t]),
                                         formal_share=float(sm['formal_share'][t]),
                                         complex_jobs=float(sm['complex_jobs'][t]),
                                         complex_vac=float(sm['complex_vac'][t]),
                                         complex_share=float(sm['complex_share'][t]),
                                         H=float(sm['H'][t]), qc=float(sm['qc'][t]), qr=float(sm['qr'][t]),
                                         wc=float(sm['wc'][t]), wr=float(sm['wr'][t]),
                                         take_S=float(sm['take_S'][t]), take_C=float(sm['take_C'][t]),
                                         price=float(sm['price'][t]),
                                         n_cm=float(sm['n_cm'][t]), n_tt=float(sm['n_tt'][t]),
                                         R_S=float(sm['R_S'][t]), R_C=float(sm['R_C'][t]),
                                         ret_S=float(sm['ret_S'][t]), ret_C=float(sm['ret_C'][t]),
                                         spend_per_pupil=float(sm['price'][t] * sm['take_C'][t])))
                    if not all(np.isfinite([sm['completion'][t] for t in range(YEARS)])):
                        failures.append(dict(country=cname, regime=regime, seed=seed, why='nonfinite'))
                except Exception as e:  # noqa: BLE001
                    failures.append(dict(country=cname, regime=regime, seed=seed, why=repr(e)))
    hdr = ['country', 'regime', 'seed', 'year', 'completion', 'college_entry', 'degree_share',
           'formal_share', 'complex_jobs', 'complex_vac', 'complex_share', 'H', 'qc', 'qr', 'wc', 'wr',
           'take_S', 'take_C', 'price', 'n_cm', 'n_tt', 'R_S', 'R_C', 'ret_S', 'ret_C', 'spend_per_pupil']
    write_rows(os.path.join(a.out, 'l2_raw.csv'), hdr, [[r[k] for k in hdr] for r in rows])

    # ---------------- checkpoints and decomposition
    cps = []
    keys = ['completion', 'college_entry', 'degree_share', 'formal_share', 'complex_share',
            'take_S', 'take_C', 'price', 'n_cm', 'n_tt', 'R_C', 'H']
    for cname in COUNTRIES:
        for regime in REGIMES:
            for yr in [10, 20, 30, 40]:
                R = [r for r in rows if r['country'] == cname and r['regime'] == regime
                     and r['year'] == yr - 1]
                row = dict(country=cname, regime=regime, year=yr, n=len(R))
                for k in keys:
                    row[k], row[k + '_sd'] = m_sd([x[k] for x in R])
                cps.append(row)
    hdr2 = ['country', 'regime', 'year', 'n'] + [x for k in keys for x in (k, k + '_sd')]
    write_rows(os.path.join(a.out, 'l2_checkpoints.csv'), hdr2, [[r[k] for k in hdr2] for r in cps])

    def get(cname, regime, yr, k):
        R = [r for r in rows if r['country'] == cname and r['regime'] == regime and r['year'] == yr - 1]
        return float(np.mean([r[k] for r in R])), float(np.std([r[k] for r in R]))

    # direction decomposition + target misses
    out = {}
    L = ['LOOP 2 — BIDIRECTIONAL EDUCATION-ECONOMY + ENDOGENOUS SHADOW SECTOR (NEW declared module)',
         f'countries={list(COUNTRIES)} regimes={list(REGIMES)} seeds={seeds} horizon={YEARS}y burn-in={BURN}y',
         'twoway.py; see PRE_DECLARATIONS_L2.md. All numbers are stylized model output, not country estimates.',
         f'failed trajectories: {len(failures)}', '',
         'DIRECTION DECOMPOSITION AT YEAR 40 (sd across seeds in brackets) and 20/40 checkpoints:']
    for cname in COUNTRIES:
        cfg = COUNTRIES[cname]
        comp_endo, comp_endo_sd = get(cname, 'R3_complementary', 40, 'complex_share')
        comp_froz, _ = get(cname, 'R4_frozen_schooling', 40, 'complex_share')
        comp_edlead, comp_edlead_sd = get(cname, 'R2_education_led', 40, 'complex_share')
        comp_edlead_froz, comp_edlead_froz_sd = get(cname, 'R8_edled_frozen', 40, 'complex_share')
        deg_on, deg_on_sd = get(cname, 'R3_complementary', 40, 'degree_share')
        deg_off, deg_off_sd = get(cname, 'R5_frozen_returns', 40, 'degree_share')
        ed_dir = comp_edlead - comp_edlead_froz
        ec_dir = deg_on - deg_off
        ed_sd = math.sqrt(comp_edlead_sd ** 2 + comp_edlead_froz_sd ** 2)
        ec_sd = math.sqrt(deg_on_sd ** 2 + deg_off_sd ** 2)
        big_ed = ed_dir > 2 * ed_sd
        big_ec = ec_dir > 2 * ec_sd
        if big_ed and big_ec:
            verdict = 'complementary'
        elif big_ed and ed_dir >= ec_dir:
            verdict = 'education-led'
        elif big_ec and ec_dir >= ed_dir:
            verdict = 'demand-led'
        else:
            verdict = 'neither identified at this N/sd'
        tS, tS_sd = get(cname, 'R3_complementary', 40, 'take_S')
        tC, tC_sd = get(cname, 'R3_complementary', 40, 'take_C')
        price, _ = get(cname, 'R3_complementary', 40, 'price')
        ncm, _ = get(cname, 'R3_complementary', 40, 'n_cm')
        ntt, _ = get(cname, 'R3_complementary', 40, 'n_tt')
        comp_jobs, _ = get(cname, 'R3_complementary', 40, 'complex_jobs')
        form_sh, form_sd = get(cname, 'R3_complementary', 40, 'formal_share')
        # generated vs supplied formal/complex jobs (predeclared decomposition)
        jobs_supplied, _ = get(cname, 'R1_demand_led', 40, 'complex_jobs')
        jobs_supplied_f, _ = get(cname, 'R9_demand_led_frozen', 40, 'complex_jobs')
        jobs_generated, _ = get(cname, 'R2_education_led', 40, 'complex_jobs')
        jobs_generated_f, _ = get(cname, 'R8_edled_frozen', 40, 'complex_jobs')
        supplied_jobs = jobs_supplied - jobs_supplied_f
        generated_jobs = jobs_generated - jobs_generated_f
        out[cname] = dict(ed_dir=ed_dir, ec_dir=ec_dir, ed_sd=ed_sd, ec_sd=ec_sd, verdict=verdict,
                          supplied_jobs=supplied_jobs, generated_jobs=generated_jobs,
                          complex_share_y40=comp_endo, formal_share_y40=form_sh,
                          take_S_y40=tS, take_C_y40=tC, price_y40=price, n_cm=ncm, n_tt=ntt,
                          complex_jobs_y40=comp_jobs)
        L.append(f'  {cname}: ed_dir(complex share, ed-led vs frozen) = {ed_dir:+.4f} (2sd {2 * ed_sd:.4f}); '
                 f'ec_dir(degree share, returns on vs off) = {ec_dir:+.4f} (2sd {2 * ec_sd:.4f})')
        L.append(f'    -> direction verdict: {verdict}')
        L.append(f'    y40: complex-job share {comp_endo:.3f} (sd {comp_endo_sd:.3f}), formal share {form_sh:.3f} '
                 f'(sd {form_sd:.3f}), complex jobs/cohort {comp_jobs:.1f}')
        L.append(f'    generated-vs-supplied complex jobs/cohort: supplied-by-demand {supplied_jobs:+.2f}; '
                 f'generated-by-schooling {generated_jobs:+.2f}')
        L.append(f'    y40 shadow: take-up S {tS:.3f} (sd {tS_sd:.3f}), C {tC:.3f} (sd {tC_sd:.3f}), '
                 f'price {price:.2f}, providers commercial {ncm:.1f} / teacher {ntt:.1f}, '
                 f'spend/pupil {price * tC:.2f}')

    # target misses
    L += ['', 'TARGET MISSES (model y40 vs observed literature/data targets; targets are NOT fitted):']
    for cname, cfg in COUNTRIES.items():
        o = out[cname]
        tg = cfg['targets']
        if 'completion' in tg:
            c, _ = get(cname, 'R3_complementary', 40, 'completion')
            L.append(f'  {cname}: upper-secondary completion model {c:.3f} vs target {tg["completion"]:.3f} '
                     f'-> miss {c - tg["completion"]:+.3f}')
        if 'formal_share' in tg:
            L.append(f'  {cname}: formal-job share model {o["formal_share_y40"]:.3f} vs target '
                     f'{tg["formal_share"]:.3f} -> miss {o["formal_share_y40"] - tg["formal_share"]:+.3f}')
        if 'tutoring_senior_sec' in tg:
            L.append(f'  {cname}: senior-secondary tutoring take-up model {o["take_S_y40"]:.3f} vs target '
                     f'{tg["tutoring_senior_sec"]:.3f} (Kwo & Bray 2011, caveat) -> miss '
                     f'{o["take_S_y40"] - tg["tutoring_senior_sec"]:+.3f}')
        if 'degree_attainment' in tg:
            L.append(f'  {cname}: degree attainment proxy (degree share of new entrants) {o["complex_share_y40"]:.3f} '
                     f'vs post-sec attainment target {tg["postsec_attainment"]:.3f} (degree 0.276) -> proxy miss')
        if 'university_attainment' in tg:
            L.append(f'  {cname}: university attainment proxy (complex-job share) '
                     f'{o["complex_share_y40"]:.3f} vs target {tg["university_attainment"]:.3f} -> miss '
                     f'{o["complex_share_y40"] - tg["university_attainment"]:+.3f}')
    # positional test: take-up at high vs low college-gate competition (within R3)
    L += ['', 'POSITIONAL RESPONSE TEST (R3, within-trajectory): tutoring take-up when college-gate competition '
              'R_C is above vs below its 40-year median:']
    for cname in COUNTRIES:
        R = [r for r in rows if r['country'] == cname and r['regime'] == 'R3_complementary']
        med = float(np.median([r['R_C'] for r in R]))
        hi = [r['take_C'] for r in R if r['R_C'] > med]
        lo = [r['take_C'] for r in R if r['R_C'] <= med]
        mhi, mlo = float(np.mean(hi)), float(np.mean(lo))
        sd = float(np.std([r['take_C'] for r in R]))
        L.append(f'  {cname}: take-up_C high-R_C {mhi:.3f} vs low-R_C {mlo:.3f} -> delta {mhi - mlo:+.3f} '
                 f'(2sd of take-up {2 * sd:.3f}) -> {"POSITIONAL RESPONSE" if (mhi - mlo) > 2 * sd else "not distinguishable"}')
    # shadow-sector industry: fixed supply vs endogenous entry
    L += ['', 'SHADOW SECTOR AS INDUSTRY (R3 vs R6 fixed supply, y40):']
    for cname in COUNTRIES:
        tS_e, _ = get(cname, 'R3_complementary', 40, 'take_S')
        tS_f, _ = get(cname, 'R6_fixed_supply', 40, 'take_S')
        p_e, _ = get(cname, 'R3_complementary', 40, 'price')
        p_f, _ = get(cname, 'R6_fixed_supply', 40, 'price')
        c_e, _ = get(cname, 'R3_complementary', 40, 'complex_share')
        c_f, _ = get(cname, 'R6_fixed_supply', 40, 'complex_share')
        L.append(f'  {cname}: take-up S endo {tS_e:.3f} vs fixed supply {tS_f:.3f}; price {p_e:.2f} vs {p_f:.2f}; '
                 f'complex share {c_e:.3f} vs {c_f:.3f}')
    write_text(os.path.join(a.out, 'findings.txt'), '\n'.join(L) + '\n')
    json.dump(dict(module='twoway.py (NEW; not massabm/floorworld/triad/paper reproduction)',
                   countries=list(COUNTRIES), regimes=list(REGIMES), seeds=seeds, years=YEARS, burn_in=BURN,
                   failures=failures, direction=out,
                   target_sources={c: COUNTRIES[c]['target_src'] for c in COUNTRIES}),
              open(os.path.join(a.out, 'run_meta.json'), 'w'), indent=1)
    print(f'L2 done: {len(rows)} rows, {len(failures)} failures')
    print('\n'.join(L[:60]))


if __name__ == '__main__':
    main()
