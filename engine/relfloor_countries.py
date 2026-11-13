"""relfloor for Cambodia, Vietnam and China (v2, 13 Nov 2026).

Same household model as relfloor.py: value of the credential = human capital
(relative premium x ability) + positional (previous-cohort saturation) + relational
(threshold eligibility), against cost, a liquidity constraint and rerouting.

Changes from v1 (5 Nov 2026), following the external review:
  * Seeds are deterministic. v1 seeded with hash(S), which Python randomises per
    process, so v1 runs could not be reproduced exactly.
  * The share of non-completers from the bottom 40% (exit_low) is read in the
    survey year (2014, 2021). v1 read it in 2035, after 11 extrapolated years, and
    that 2035 value was what the DHS comparison in credential_floor_dhs.zip used.
  * Cambodia is tested on lower-secondary completion by wealth quintile
    (UIS CR.2.Q1-Q5, computed from DHS 2014 and 2021-22). This is the model's own
    margin, so it is closer than the DHS Table 2.12 "not in secondary, 12-18" figure.
  * Vietnam gets a second test: the full MICS 2014 quintile profile.
  * China: gaokao registrants are divided by births 18 years earlier.
  * Income growth priors come from WDI real GDP per capita growth 2000-2023
    (CAGR +/- 1 point). The income *level* (mu) stays a free scale parameter,
    because income, cost and subsistence are in stylised units with no observed
    counterpart.
  * Each relational-weight posterior is printed next to its prior, with a
    Kolmogorov-Smirnov test, so readers can see when the data are uninformative.

Sources: inputs/credential_floor_sources.json (each value has a URL, a table
reference and a verification flag).
"""
import json, os, sys
import numpy as np
from multiprocessing import Pool
sys.path.insert(0, os.path.dirname(__file__))
from relfloor import PRIORS, HZ

YEARS = np.arange(1998, 2036)
def yi(y): return int(y - YEARS[0])
STRUCTS = ['M_HC', 'M_POS', 'M_REL']
SIDX = {s: i for i, s in enumerate(STRUCTS)}

# --- sourced data -------------------------------------------------------------
# UIS CR.2 lower-secondary completion, Cambodia, by wealth quintile (poorest..richest)
KHM_Q = {2005: [4.05, 11.58, 18.32, 30.35, 54.18],
         2010: [11.73, 17.82, 30.97, 45.71, 63.38],
         2014: [17.05, 25.13, 37.12, 53.20, 64.53],
         2021: [29.01, 47.56, 54.22, 65.66, 78.87]}
KHM_Q = {k: np.array(v) / 100 for k, v in KHM_Q.items()}
# DHS 2021-22 Table 2.12 secondary NAR, ages 12-18 (definition mismatch; robustness only)
KHM_DHS_NAR = np.array([25.5, 39.9, 43.4, 43.5, 58.7]) / 100
# Vietnam MICS 2014 Table ED.5A, upper-secondary adjusted NAR 15-17, by quintile; total 70.7
VNM_MICS = np.array([40.4, 67.3, 74.3, 85.4, 93.3]) / 100
VNM_MICS_SHAPE = VNM_MICS / VNM_MICS.mean()
# China: gaokao registrants and births 18 years earlier (10,000 persons; NBS, MoE)
CHN_GAOKAO = {2023: 1291, 2024: 1342, 2025: 1335, 2026: 1290}
CHN_BIRTHS = {2005: 1617, 2006: 1584, 2007: 1594, 2008: 1608}
# WDI NY.GDP.PCAP.KD CAGR 2000-2023
WDI_G = {'Cambodia': .0558, 'Vietnam': .0506, 'China': .0776}

def bottom40_share(c_by_q, w=None):
    """Share of non-completers living in the bottom two quintiles.
    w = child weight per quintile (equal by default)."""
    w = np.ones(5) if w is None else np.asarray(w, float)
    nc = (1 - c_by_q) * w
    return float(nc[:2].sum() / nc.sum())

def skew_weights(r):        # poorest quintile has r times the children of the richest
    return np.linspace(r, 1, 5)

OBS_KHM = {yr: {f'w{r}': bottom40_share(KHM_Q[yr], skew_weights(r)) for r in (1, 1.25, 1.5, 2)}
           for yr in (2014, 2021)}

def within(x, lo, hi): return lo <= x <= hi

def t_khm_agg(r):     # v1 targets (aggregate completion)
    c = r['c']
    return within(c[yi(2000)], .12, .23) and within(c[yi(2010)], .33, .50) and within(c[yi(2021)], .50, .62)

def t_khm_profile(r):  # aggregate + quintile profile 2014 and 2021, +/-10 points each
    if not t_khm_agg(r): return False
    return all(np.all(np.abs(np.array(r['q'][yi(y)]) - KHM_Q[y]) <= .10) for y in (2014, 2021))

def t_vnm_yl(r):       # v1 targets (Young Lives, completion at 19, mapped to 2013)
    q = r['q'][yi(2013)]
    return within(r['c'][yi(2013)], .50, .66) and within(q[0], .15, .38) and within(q[4], .70, .90)

def t_vnm_mics(r):     # MICS 2014: all five quintile levels +/-8 points
    return bool(np.all(np.abs(np.array(r['q'][yi(2014)]) - VNM_MICS) <= .08))

def t_vnm_yl_shape(r): # Young Lives levels + MICS relative profile (q_i / mean) +/-0.12
    if not t_vnm_yl(r): return False
    q = np.array(r['q'][yi(2014)])
    return bool(q.mean() > 0 and np.all(np.abs(q / q.mean() - VNM_MICS_SHAPE) <= .12))

def t_chn_agg(r):
    c = r['c']
    return within(c[yi(2012)], .25, .36) and within(c[yi(2019)], .42, .54) and within(c[yi(2023)], .54, .66)

def g_band(country): return (WDI_G[country] - .01, WDI_G[country] + .01)

CFG = {
  'Cambodia': dict(L=3, mu=(np.log(.5), np.log(1.4)), g=g_band('Cambodia'), prem='flat',
                   tests={'agg': t_khm_agg, 'profile': t_khm_profile}),
  'Vietnam':  dict(L=3, mu=(np.log(.7), np.log(1.8)), g=g_band('Vietnam'), prem='flat',
                   tests={'yl': t_vnm_yl, 'mics': t_vnm_mics, 'yl_mics_shape': t_vnm_yl_shape}),
  'China':    dict(L=4, mu=(np.log(.8), np.log(2.5)), g=g_band('China'), prem='china',
                   tests={'agg': t_chn_agg}),
}
# v1 growth priors, kept for the comparison run (--v1-priors)
V1_G = {'Cambodia': (.03, .06), 'Vietnam': (.04, .065), 'China': (.05, .09)}

SMOOTH_LIQ = '--smooth-liq' in sys.argv   # robustness: graded rather than hard liquidity threshold

def draw(rng, S, cfg):
    th = {k: rng.uniform(*v) for k, v in PRIORS.items()}
    th['s_liq'] = rng.uniform(0.1, 1.0) if SMOOTH_LIQ else 0.0   # log-income scale of the graded constraint
    th['mu'] = rng.uniform(*cfg['mu']); th['g'] = rng.uniform(*cfg['g'])
    if S == 'M_HC': th['b_pos'] = th['b_rel'] = 0.0
    elif S == 'M_POS': th['b_rel'] = 0.0
    return th

def prem(th, cfg, scen):
    p = np.full(len(YEARS), th['prem0'])
    if cfg['prem'] == 'china' and scen != 'nofall':
        k = (YEARS >= 2018) & (YEARS <= 2023)
        p[YEARS > 2023] = th['prem0'] * 0.8           # 0.75 -> 0.60
        p[k] = th['prem0'] * (1 - 0.2 * (YEARS[k] - 2018) / 5)
    if scen == 'fall':                                  # further 40% by 2035
        k = YEARS >= 2025
        p[k] = p[k] * (1 - 0.4 * (YEARS[k] - 2024) / 11)
    return p

def sim(th, cfg, scen='base', n=2000, seed=0):
    rng = np.random.default_rng(seed)
    logy0 = rng.normal(th['mu'], 0.7, n)
    ab = 0.3 * (logy0 - logy0.mean()) / 0.7 + np.sqrt(1 - 0.09) * rng.normal(size=n)
    q = np.searchsorted(np.quantile(logy0, [.2, .4, .6, .8]), logy0)
    pm = prem(th, cfg, scen); s_prev = 0.3
    c_ = th['direct'] + th['forgo']; out = {'c': [], 'q': [], 'exit_low': [], 'q3': []}
    for t, yr in enumerate(YEARS):
        y = np.exp(logy0) * (1 + th['g']) ** (yr - 1998)
        R = HZ * (pm[t] * np.exp(th['gamma'] * ab) + th['b_pos'] * s_prev + th['b_rel'])
        want = R - cfg['L'] * c_ + rng.logistic(0, th['sig'], n) > 0
        thresh = th['y_sub'] + th['kappa'] * c_
        if th.get('s_liq', 0) > 0:   # P(finance) rises smoothly with log income around the threshold
            pf = th['p_fin'] + (1 - th['p_fin']) / (1 + np.exp(-(np.log(y) - np.log(thresh)) / th['s_liq']))
            fin = rng.random(n) < pf
        else:
            fin = (y >= thresh) | (rng.random(n) < th['p_fin'])
        stay = want & fin; s_prev = stay.mean(); ex = ~stay
        out['c'].append(stay.mean()); out['q'].append([stay[q == i].mean() for i in range(5)])
        out['exit_low'].append((ex & (q <= 1)).sum() / max(ex.sum(), 1))
        out['q3'].append(stay[q >= 2].mean())
    return {k: np.array(v) for k, v in out.items()}

def work(args):
    country, S, chunk, nd, gmode = args
    cfg = dict(CFG[country])
    if gmode == 'v1': cfg['g'] = V1_G[country]
    rng = np.random.default_rng([2026, list(CFG).index(country), SIDX[S], chunk])
    acc = []
    for i in range(nd):
        seed = (chunk * nd + i) * 7 + SIDX[S]
        th = draw(rng, S, cfg); r = sim(th, cfg, 'base', 1500, seed)
        passed = [k for k, t in cfg['tests'].items() if t(r)]
        if not passed: continue
        rb = sim(th, cfg, 'base', 4000, seed)
        rn = sim(th, cfg, 'nofall', 4000, seed)
        rf = sim(th, cfg, 'fall', 4000, seed)
        acc.append({'th': th, 'pass': passed,
             'exit_low_2014': float(rb['exit_low'][yi(2014)]),
             'exit_low_2021': float(rb['exit_low'][yi(2021)]),
             'exit_low_2035': float(rb['exit_low'][-1]),
             'fall35_q3': float(rf['q3'][-1] - rf['q3'][yi(2024)]),
             'cn_resp': float(rb['c'][yi(2023)] / rn['c'][yi(2023)] - 1),
             'cn_2024_26': float(rb['c'][yi(2026)] / rb['c'][yi(2024)] - 1),
             'c_end': float(rb['c'][yi(2024)]),
             'q_2014': [float(v) for v in rb['q'][yi(2014)]],
             'q_2021': [float(v) for v in rb['q'][yi(2021)]]})
    return country, S, acc

def pct(v): return [round(float(np.percentile(v, p)), 3) for p in (5, 50, 95)]

def ks_uniform(x, lo, hi):
    """KS statistic and asymptotic p-value of sample x against U(lo, hi)."""
    x = np.sort((np.asarray(x) - lo) / (hi - lo)); n = len(x)
    ecdf_hi = np.arange(1, n + 1) / n; ecdf_lo = np.arange(0, n) / n
    D = float(max(np.max(ecdf_hi - x), np.max(x - ecdf_lo)))
    lam = (np.sqrt(n) + 0.12 + 0.11 / np.sqrt(n)) * D
    p = float(np.clip(2 * sum((-1) ** (k - 1) * np.exp(-2 * k * k * lam * lam) for k in range(1, 101)), 0, 1))
    return round(D, 3), round(p, 4)

def summarise(a, nd, country, S):
    d = {'accepted': len(a), 'rate': len(a) / nd}
    if len(a) < 5: return d
    for k in ['exit_low_2014', 'exit_low_2021', 'exit_low_2035', 'fall35_q3', 'cn_resp',
              'cn_2024_26', 'c_end']:
        d[k] = pct([x[k] for x in a])
    for yr in (2014, 2021):
        Q = np.array([x[f'q_{yr}'] for x in a])
        d[f'q_profile_{yr}'] = [pct(Q[:, i]) for i in range(5)]
    for k in ['b_rel', 'b_pos', 'gamma', 'prem0', 'g', 's_liq']:
        d['post_' + k] = pct([x['th'][k] for x in a])
    if S == 'M_REL':
        lo, hi = PRIORS['b_rel']
        D, p = ks_uniform([x['th']['b_rel'] for x in a], lo, hi)
        post = d['post_b_rel']
        d['b_rel_vs_prior'] = {
            'prior': [round(lo + f * (hi - lo), 3) for f in (.05, .5, .95)],
            'posterior': post,
            'width_ratio_90': round((post[2] - post[0]) / (0.9 * (hi - lo)), 3),
            'ks_D': D, 'ks_p': p,
            'verdict': 'posterior ~ prior (data uninformative)' if (p > 0.01 or D < 0.1)
                       else 'posterior differs from prior'}
    if country == 'Cambodia':
        for yr in (2014, 2021):
            v = np.array([x[f'exit_low_{yr}'] for x in a]); obs = OBS_KHM[yr]
            lo_o, hi_o = min(obs.values()), max(obs.values())
            d[f'exit_low_{yr}_vs_obs'] = {
                'observed_range': [round(lo_o, 3), round(hi_o, 3)],
                'share_draws_in_observed_range': round(float(np.mean((v >= lo_o) & (v <= hi_o))), 3),
                'share_draws_within_5pts': round(float(np.mean((v >= lo_o - .05) & (v <= hi_o + .05))), 3)}
    return d

def chn_cohort():
    out = {}
    for yr, g in CHN_GAOKAO.items():
        b = CHN_BIRTHS.get(yr - 18)
        if b: out[yr] = {'registrants_10k': g, 'births_10k': b, 'ratio': round(g / b, 4)}
    r24, r26 = out[2024]['ratio'], out[2026]['ratio']
    return {'by_year': out,
            'raw_change_2024_26': round(CHN_GAOKAO[2026] / CHN_GAOKAO[2024] - 1, 4),
            'cohort_adjusted_change_2024_26': round(r26 / r24 - 1, 4),
            'note': 'Registrants include repeaters and vocational-track (spring) candidates; '
                    'births are NBS sample-survey estimates; no mortality or migration adjustment.'}

def run(nd, gmode='sourced', chunks=8):
    jobs = [(c, S, i, nd // chunks, gmode) for c in CFG for S in STRUCTS for i in range(chunks)]
    res = {}
    with Pool(os.cpu_count()) as p:
        for c, S, acc in p.imap_unordered(work, jobs):
            res.setdefault(c, {}).setdefault(S, []).extend(acc)
    out = {'meta': {'draws_per_country_structure': nd, 'growth_priors': gmode,
                    'growth_bands': {c: list(V1_G[c] if gmode == 'v1' else CFG[c]['g']) for c in CFG},
                    'observed_khm_exit_low': {str(k): {kk: round(vv, 3) for kk, vv in v.items()}
                                              for k, v in OBS_KHM.items()},
                    'observed_khm_dhs_nar_2021_equal_weights': round(bottom40_share(KHM_DHS_NAR), 3),
                    'china_cohort': chn_cohort()}}
    for c in CFG:
        out[c] = {}
        for test in CFG[c]['tests']:
            out[c][test] = {S: summarise([x for x in res[c][S] if test in x['pass']], nd, c, S)
                            for S in STRUCTS}
    return out

if __name__ == '__main__':
    nd = int(sys.argv[1]) if len(sys.argv) > 1 else 24000
    gmode = 'v1' if '--v1-priors' in sys.argv else 'sourced'
    out = run(nd, gmode)
    here = os.path.dirname(__file__)
    os.makedirs(os.path.join(here, 'results'), exist_ok=True)
    fn = 'relfloor_countries_v2.json' if gmode == 'sourced' else 'relfloor_countries_v2_v1priors.json'
    if SMOOTH_LIQ: fn = fn.replace('.json', '_smoothliq.json')
    json.dump(out, open(os.path.join(here, 'results', fn), 'w'), indent=1)
    print(json.dumps(out['meta'], indent=1))
    for c in CFG:
        for test, block in out[c].items():
            print(f'== {c} [{test}]')
            for S, d in block.items():
                keep = {k: d[k] for k in d if k in ('accepted', 'exit_low_2021', 'exit_low_2035',
                        'fall35_q3', 'cn_resp', 'cn_2024_26', 'b_rel_vs_prior', 'exit_low_2021_vs_obs', 'q_profile_2021', 'q_profile_2014')}
                print(' ', S, json.dumps(keep))
