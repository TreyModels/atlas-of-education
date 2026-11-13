"""China youth-unemployment bulge: fit 2018-2022 (old NBS method), test 2023 H1 (old) and Dec 2023 - Sep 2026 (new method,
students excluded) without refitting, then decompose the bulge by counterfactual.

Run from engine/:  python -m firms.calibrate_china      -> firms/results/{china_fit.json, china_fit.md, *.png}
"""
import itertools, json, math, os, sys, hashlib, platform
import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firms import model as M, data_china as D

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, 'results')
# Bounds widened in the external-review pass (experiments/youth-review/README.md, item 1.2). The previous bounds were
# m_g 0.03-0.50, m_n 0.03-0.42, f_n_ref 0.05-0.38, m_a 0.02-0.6, dr_drop 0-0.3; the previous fit stuck at m_n 0.42,
# f_n_ref 0.38, m_a 0.02, dr_drop 0.30, and m_g 0.03. lam_g stays capped at 1 (a partial-adjustment speed above 1
# overshoots the target); e_prop stays floored at 0 (a negative elasticity to property investment is not admissible).
# f_n_ref is capped at 0.399, not doubled to 0.76: the urn-ball matching needs job-finding below the application rate a
# (a = 0.40, DEFAULTS), so f_n_ref >= a is infeasible (urn_x_from_f raises). A doubled bound is run separately with a = 0.80.
# m_n is capped at 0.449, not doubled to 0.84: the non-graduate wage w_n0 = p_n0 (1 - m_n) must stay above the flow value
# z_n = 0.55 (non-negative bargaining share), so m_n < 1 - z_n/p_n0 = 0.45. The old upper bound 0.42 sat just below this ceiling.
FREE = [  # name, lower, upper, start
    ('m_g', 0.00, 0.50, 0.15), ('m_n', 0.03, 0.449, 0.10), ('f_g_ref', 0.05, 0.38, 0.20), ('f_n_ref', 0.05, 0.399, 0.25),
    ('lam_g', 0.002, 1.0, 0.02), ('zeta', 0.0, 1.0, 0.3), ('m_a', 0.0, 0.6, 0.1), ('sep_scale', 0.2, 2.5, 1.0),
    ('july_g', 0.2, 1.0, 0.7), ('e_prop', 0.0, 1.0, 0.1), ('dr_drop', 0.0, 0.6, 0.02),
]
FIT = (2018, 2022)


def base_ref():
    ym = M.YouthMarket(D)
    return dict(S_ref=ym.p['S_ref'], g_H=ym.p['g_H'], g_N=ym.p['g_N'])


REF = base_ref()


def run(theta=None, **over):
    kw = dict(REF)
    if theta is not None:
        kw.update({n: float(v) for (n, *_), v in zip(FREE, theta)})
    kw.update(over)
    return M.YouthMarket(D, **kw).run()


def obs_pairs(R, y0, y1, method, flags=('v', 'm')):
    out = []
    for i, (y, m) in enumerate(zip(R['year'], R['month'])):
        if y0 <= y <= y1:
            o = D.youth(y, m)
            if o and o[1] == method and o[2] in flags:
                out.append((y, m, o[0], R['rate_old' if method == 'old' else 'rate_new'][i], o[2]))
    return out


def pairs_for(R, window):
    if window == 'early':                                   # 2018-22, old method only
        return obs_pairs(R, *FIT, 'old')
    return obs_pairs(R, 2018, 2026, 'old') + obs_pairs(R, 2023, 2026, 'new')     # whole record, both methods


def resid(theta, window='early', over=None):
    R = run(theta, **(over or {}))
    pr = pairs_for(R, window)
    r = [mod - ob for *_, ob, mod, _ in pr]
    return np.array(r) if all(map(math.isfinite, r)) else np.full(len(pr), 50.0)


def fit(window='early', over=None, nstarts=8, seed=1):
    lo = [f[1] for f in FREE]; hi = [f[2] for f in FREE]
    rng = np.random.default_rng(seed)
    starts = [np.array([f[3] for f in FREE])] + [rng.uniform(lo, hi) for _ in range(nstarts - 1)]
    best = None
    for s in starts:
        try:
            r = least_squares(resid, s, bounds=(lo, hi), diff_step=1e-3, max_nfev=300, args=(window, over))
        except ValueError:
            continue
        if best is None or r.cost < best.cost:
            best = r
    return best


def vg_check(R):
    """External firm-side check, not fitted: graduate vacancies Jan-Jun 2025 vs Jan-Jun 2024 (Caixin, 19 Sep 2025, citing
    job-board data: postings for graduates -22%, job seekers +8%)."""
    v25 = window_mean(R, 'V_g', (2025, 1), (2025, 6)); v24 = window_mean(R, 'V_g', (2024, 1), (2024, 6))
    return 100 * (v25 / v24 - 1)


def stats(pairs):
    if not pairs:
        return dict(n=0)
    e = np.array([mod - ob for *_, ob, mod, _ in pairs]); o = np.array([ob for *_, ob, _, _ in pairs])
    md = np.array([mod for *_, ob, mod, _ in pairs])
    return dict(n=len(e), mae=float(np.abs(e).mean()), rmse=float(np.sqrt((e ** 2).mean())), bias=float(e.mean()),
                corr=float(np.corrcoef(o, md)[0, 1]) if len(e) > 2 else None, obs_mean=float(o.mean()), mod_mean=float(md.mean()))


def window_mean(R, key, a, b):
    """Mean of R[key] over months a..b inclusive, a/b = (year, month)."""
    v = [x for x, y, m in zip(R[key], R['year'], R['month']) if a <= (y, m) <= b]
    return float(np.mean(v))


# ---------------------------------------------------------------- counterfactual switches
def switches(theta, active):
    """Causes in `active` take their historical value; the others are held at their 2018 state."""
    over = {}
    if 'supply' not in active:
        over['grad_supply'] = lambda y: D.graduates(min(y, 2018))
    if 'composition' not in active:
        over['nongrad_supply'] = lambda y: D.nongrad_school_leavers(min(y, 2018))
    if 'demand' not in active:
        ym = M.YouthMarket(D, **dict(REF, **{n: float(v) for (n, *_), v in zip(FREE, theta)}))
        A = ym.A
        over['demand'] = lambda y, m: A.get((y, m), 1.0) if y < 2019 else 1.0
    if 'screening' not in active:
        over['rank'] = 'random'
    if 'sector' not in active:
        over['grad_demand'] = 'flat'
    return over


CAUSES = ['supply', 'composition', 'demand', 'sector', 'screening']
LABEL = dict(supply='Graduate numbers (8.3m in 2019 to 12.7m in 2026)',
             composition='Fewer non-graduate entrants (smaller cohorts, more going to college)',
             demand='Aggregate demand read from adult unemployment',
             sector='Aug-2021 step (unexplained)',   # the dr_drop step: fitted residual, not a sourced shock (review 1.1, 1.6)
             screening='Employers preferring graduates for non-graduate jobs')
EARLY, LATE = ((2018, 1), (2019, 12)), ((2024, 1), (2026, 9))


def outcome(R, key='rate_new'):
    return window_mean(R, key, *LATE) - window_mean(R, key, *EARLY)


def shapley(theta, key='rate_new'):
    cache = {}
    def val(S):
        S = frozenset(S)
        if S not in cache:
            cache[S] = outcome(run(theta, **switches(theta, S)), key)
        return cache[S]
    n = len(CAUSES); phi = {}
    for c in CAUSES:
        tot = 0.0
        for k in range(n):
            for S in itertools.combinations([x for x in CAUSES if x != c], k):
                w = math.factorial(k) * math.factorial(n - k - 1) / math.factorial(n)
                tot += w * (val(set(S) | {c}) - val(S))
        phi[c] = tot
    return phi, val(CAUSES), val(())


def summarise(best, window, over):
    th = best.x
    R = run(th, **over)
    J = best.jac
    sv = np.linalg.svd(J, compute_uv=False)
    try:
        cov = np.linalg.inv(J.T @ J) * (2 * best.cost / max(len(best.fun) - len(th), 1))
        se = np.sqrt(np.clip(np.diag(cov), 0, None))
    except np.linalg.LinAlgError:
        se = np.full(len(th), np.nan)
    h_new_v = obs_pairs(R, 2023, 2026, 'new', flags=('v',))
    held = run(th, **dict(over, **switches(th, set(CAUSES) - {'supply'})))
    return dict(window=window, over={k: (str(v) if isinstance(v, float) and math.isinf(v) else v) for k, v in over.items()},
                params={n: float(v) for (n, *_), v in zip(FREE, th)}, se={n: float(s) for (n, *_), s in zip(FREE, se)},
                condition=float(sv[0] / sv[-1]), jac_singular_values=[float(x) for x in sv],
                fit_early=stats(obs_pairs(R, *FIT, 'old')), holdout_old_2023H1=stats(obs_pairs(R, 2023, 2023, 'old')),
                new_all=stats(obs_pairs(R, 2023, 2026, 'new')), new_verified=stats(h_new_v),
                whole_record=stats(pairs_for(R, 'full')),
                rate_change=outcome(R), grad_u_change=outcome(R, 'u_G'),
                supply_effect=outcome(R) - outcome(held), vg_2025H1_pct=vg_check(R),
                max_abs_balance=float(max(abs(b) for b in R['balance'])),
                max_abs_free_entry_resid=float(max(abs(b) for b in R['resid_n']))), R


def main(quick=False):
    os.makedirs(OUT, exist_ok=True)
    grid = [2.5, 5.0, 10.0, math.inf] if not quick else [5.0]
    profiles = {}
    keep = {}
    for window in ('early', 'full'):
        for sg in grid:
            over = dict(sigma_A=sg)
            best = fit(window, over, nstarts=3 if quick else 6)
            s, R = summarise(best, window, over)
            key = f'{window}|sigma_A={sg}'
            profiles[key] = s; keep[key] = (best.x, R, over)
            print(key, f"cost={best.cost:.1f}", f"fitMAE={s['fit_early']['mae']:.2f}", f"newMAE={s['new_verified']['mae']:.2f}",
                  f"drate={s['rate_change']:+.2f}", f"supply={s['supply_effect']:+.2f}", f"vg={s['vg_2025H1_pct']:+.1f}", flush=True)
    # headline model: whole-record fit at the Card-Lemieux value sigma_A = 5
    th, R, over = keep['full|sigma_A=5.0']
    th_e, R_e, _ = keep['early|sigma_A=5.0']
    res = dict(profiles=profiles, headline='full|sigma_A=5.0', early='early|sigma_A=5.0',
               fixed={k: v for k, v in M.DEFAULTS.items() if k not in [f[0] for f in FREE] and not callable(v)
                      and k not in ('demand', 'grad_supply', 'nongrad_supply')},
               reference=dict(S_ref=REF['S_ref'], g_H=REF['g_H'], g_N=REF['g_N']))
    last = {m: D.youth(2022, m)[0] for m in range(1, 13)}
    res['naive_new_verified'] = stats([(y, m, ob, last[m], f) for y, m, ob, _, f in obs_pairs(R, 2023, 2026, 'new', flags=('v',))])
    res['naive_old_2023H1'] = stats([(y, m, ob, last[m], f) for y, m, ob, _, f in obs_pairs(R, 2023, 2023, 'old')])
    diag = {}
    for name, ov in [('baseline', {}), ('flexible graduate wages (lam_g=1)', dict(lam_g=1.0)),
                     ('young and older graduates perfect substitutes (sigma_A=inf)', dict(sigma_A=math.inf)),
                     ('random hiring (no credential screening)', dict(rank='random')),
                     ('demand flat from 2019', switches(th, set(CAUSES) - {'demand'})),
                     ('graduates held at 2018', switches(th, set(CAUSES) - {'supply'})),
                     ('non-graduate entrants held at 2018', switches(th, set(CAUSES) - {'composition'}))]:
        Rx = run(th, **dict(over, **ov))
        diag[name] = dict(rate_change=outcome(Rx), late_rate=window_mean(Rx, 'rate_new', *LATE),
                          grad_u_change=outcome(Rx, 'u_G'), nongrad_u_change=outcome(Rx, 'u_N'),
                          under_late=window_mean(Rx, 'under', *LATE), grad_share_n_hires_late=window_mean(Rx, 'grad_share_n_hires', *LATE),
                          wage_g_change_pct=100 * (window_mean(Rx, 'w_g', *LATE) / window_mean(Rx, 'w_g', *EARLY) - 1),
                          p_g_change_pct=100 * (window_mean(Rx, 'p_g', *LATE) / window_mean(Rx, 'p_g', *EARLY) - 1))
    res['diagnostics'] = diag
    phi, full, none = shapley(th)
    res['shapley_rate_new'] = dict(contributions=phi, total=full, all_off=none, label=LABEL)
    phiG, fullG, noneG = shapley(th, 'u_G')
    res['shapley_grad_u'] = dict(contributions=phiG, total=fullG, all_off=noneG)
    keys = ('year', 'month', 'rate_old', 'rate_new', 'u_G', 'u_N', 'A', 'under', 'grad_share_n_hires', 'f_g', 'f_n', 'w_g',
            'p_g', 'V_g', 'LF_G', 'LF_N')
    res['series'] = {k: R[k] for k in keys}
    res['series_early_fit'] = {k: R_e[k] for k in ('year', 'month', 'rate_old', 'rate_new')}
    res['manifest'] = dict(python=platform.python_version(), numpy=np.__version__,
                           files={f: hashlib.sha256(open(os.path.join(HERE, f), 'rb').read()).hexdigest()
                                  for f in ('model.py', 'data_china.py', 'calibrate_china.py')})
    json.dump(res, open(os.path.join(OUT, 'china_fit.json'), 'w'), indent=1, default=float)
    plot(res, R, R_e)
    report(res)
    return res


def plot(res, R, R_e):
    import matplotlib; matplotlib.use('Agg')
    import matplotlib.pyplot as plt
    t = np.array(R['year']) + (np.array(R['month']) - 0.5) / 12
    sel = t >= 2017.5
    fig, ax = plt.subplots(figsize=(10, 4.6), dpi=150)
    te = t
    old_e = np.where(te < 2023.5, np.array(R_e['rate_old']), np.nan); new_e = np.where(te >= 2023.9, np.array(R_e['rate_new']), np.nan)
    old_f = np.where(t < 2023.5, np.array(R['rate_old']), np.nan); new_f = np.where(t >= 2023.9, np.array(R['rate_new']), np.nan)
    ax.axvspan(2018, 2023, color='#eef2f7', zorder=0, label='early-fit window (2018-22)')
    ax.plot(t[sel], old_f[sel], color='#2563eb', lw=1.6, label='whole-record fit, old method')
    ax.plot(t[sel], new_f[sel], color='#ea580c', lw=1.6, label='whole-record fit, new method')
    ax.plot(t[sel], old_e[sel], color='#2563eb', lw=1, ls='--', label='2018-22 fit, extrapolated (old)')
    ax.plot(t[sel], new_e[sel], color='#ea580c', lw=1, ls='--', label='2018-22 fit, forecast (new)')
    for meth, col in (('old', '#1e3a8a'), ('new', '#9a3412')):
        pts = [(y + (m - 0.5) / 12, D.youth(y, m)[0], D.youth(y, m)[2]) for y in range(2018, 2027) for m in range(1, 13)
               if D.youth(y, m) and D.youth(y, m)[1] == meth]
        for flag, mk in (('v', 'o'), ('m', 'x')):
            q = [(a, b) for a, b, f in pts if f == flag]
            if q:
                ax.scatter(*zip(*q), s=14, color=col, marker=mk, zorder=3,
                           label=f'NBS {meth} method' + (' (from memory, unverified)' if flag == 'm' else ''))
    ax.set_ylabel('urban unemployment, ages 16-24 (%)'); ax.set_xlim(2017.5, 2026.9); ax.grid(alpha=.3)
    ax.legend(fontsize=7, loc='upper left', ncol=2, frameon=False)
    ax.set_title('China youth unemployment: firm-side model vs NBS (sigma_A = 5)', fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, 'china_fit.png')); plt.close(fig)
    # decomposition bar
    sh = res['shapley_rate_new']
    fig, ax = plt.subplots(figsize=(7, 3.2), dpi=150)
    names = CAUSES; vals = [sh['contributions'][c] for c in names]
    ax.barh([LABEL[c] for c in names][::-1], vals[::-1], color=['#2563eb', '#16a34a', '#a855f7', '#ea580c'][::-1])
    ax.axvline(0, color='k', lw=.6); ax.set_xlabel('percentage points of the rise, 2018-19 to 2024-26 (model, new method)')
    for i, v in enumerate(vals[::-1]):
        ax.text(v, i, f' {v:+.1f}', va='center', fontsize=8)
    ax.set_title(f"Shapley decomposition of the modelled rise ({sh['total']:+.1f} pp)", fontsize=9)
    fig.tight_layout(); fig.savefig(os.path.join(OUT, 'china_shapley.png')); plt.close(fig)


def report(res):
    L = []
    P = lambda s='': L.append(s)
    P('# China youth bulge: firm-side model results'); P()
    P('Generated by `python -m firms.calibrate_china`. Two fitting windows: "early" = 2018-01..2022-12 (old NBS method, 60 '
      'months; everything later is out of sample) and "full" = every observed month 2018-01..2026-09 under both methods. '
      'The method switch is an observation equation (searching final-year students leave numerator and denominator), '
      'never a fitted level shift. Each row fixes the CES elasticity sigma_A and fits the other nine parameters.'); P()
    P('| Window, sigma_A | MAE 2018-22 | MAE 2023 H1 (old) | MAE new method (verified) | Modelled rise, pp | of which graduate supply | Grad vacancies 2025H1 y/y (obs -22%) |')
    P('|---|---:|---:|---:|---:|---:|---:|')
    for k, s in res['profiles'].items():
        P(f"| {k} | {s['fit_early']['mae']:.2f} | {s['holdout_old_2023H1']['mae']:.2f} | {s['new_verified']['mae']:.2f} | "
          f"{s['rate_change']:+.2f} | {s['supply_effect']:+.2f} | {s['vg_2025H1_pct']:+.1f}% |")
    P(); P(f"Naive benchmark (same calendar month of 2022): MAE 2023 H1 {res['naive_old_2023H1']['mae']:.2f}; "
           f"new-method verified {res['naive_new_verified']['mae']:.2f}."); P()
    h = res['profiles'][res['headline']]
    P(f"## Headline model: {res['headline']}"); P()
    P('| Parameter | Estimate | s.e. (local) |'); P('|---|---:|---:|')
    for k, v in h['params'].items():
        P(f"| {k} | {v:.4f} | {h['se'][k]:.4f} |")
    P(); P(f"Jacobian condition number {h['condition']:.0f}."); P()
    sh = res['shapley_rate_new']
    P(f"## Decomposition of the modelled rise ({sh['total']:+.2f} pp; all four causes held at 2018: {sh['all_off']:+.2f} pp)"); P()
    for c, v in sh['contributions'].items():
        P(f"- {LABEL[c]}: {v:+.2f} pp")
    shg = res['shapley_grad_u']
    P(); P(f"Graduate unemployment rate, same decomposition (total {shg['total']:+.2f} pp): " +
           '; '.join(f"{c} {v:+.2f}" for c, v in shg['contributions'].items())); P()
    P('## Mechanism diagnostics (headline parameters; model new-method rate, 2018-19 to 2024-26)'); P()
    P('| Variant | Δ youth rate | late rate | Δ grad u | Δ non-grad u | grads downgraded (late, %) | grad share of non-grad hires | Δ grad wage % | Δ grad productivity % |')
    P('|---|---:|---:|---:|---:|---:|---:|---:|---:|')
    for k, d in res['diagnostics'].items():
        P(f"| {k} | {d['rate_change']:+.2f} | {d['late_rate']:.1f} | {d['grad_u_change']:+.2f} | {d['nongrad_u_change']:+.2f} | "
          f"{d['under_late']:.1f} | {d['grad_share_n_hires_late']:.2f} | {d['wage_g_change_pct']:+.1f} | {d['p_g_change_pct']:+.1f} |")
    P(); P(f"Accounting: max |stock balance residual| {h['max_abs_balance']:.2e}; max |free-entry residual| {h['max_abs_free_entry_resid']:.2e}.")
    open(os.path.join(OUT, 'china_fit.md'), 'w').write('\n'.join(L) + '\n')


if __name__ == '__main__':
    r = main(quick='--quick' in sys.argv)
    print(open(os.path.join(OUT, 'china_fit.md')).read())
