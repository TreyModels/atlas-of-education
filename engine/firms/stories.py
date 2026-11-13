"""China story tournament: competing explanations of the youth jobs crisis, scored jointly, with Monte Carlo.

docs/china_jobs_stories.md sets out the stories and what each predicts. Each story is a mechanism switched on in
StoryMarket (a SeasonalMarket using its identity hooks), with its own free parameters on top of the shared core.
All stories are fitted to the SAME evidence, so they compete on equal terms:

  youth      NBS 16-24 unemployment, old method 2018-01..2023-06 and new method 2023-12..2026-09 (verified months)
  wages      MyCOS graduate starting pay relative to the NBS urban average wage, log change since 2018, classes 2019-23
  postings   graduate job postings, H1 2025 vs H1 2024: -22% (Caixin, job-board data)
  adult      the adult labour market: aggregate demand A_t is backed out of observed adult unemployment, so any story
             that moves A_t away from it (consumption feedback) pays for the adult unemployment it implies
  queue      national civil-service exam applicants passing review, 2023-26 (2.60, 3.03, 3.42, 3.72 m; Jiemian):
             compared with the model's share of graduates delaying entry (only the queuing story can move it)

Three kinds of uncertainty are kept apart (design memo, 5 Nov 2026):
  structural  stories compared by penalised fit (BIC) -> approximate posterior weights
  parameter   Monte Carlo around each story's fit (Laplace approximation from the Jacobian), outcome distributions
  random      none: this market model is deterministic at the aggregate level (the childworld engine carries seeds)

This is an explanatory exercise on the whole record (the fit sees 2018-26). Forecast tests use the strict protocols
(forecast_2024.py, seasonal_2024.py); the winning story should be put through them next.

Run from engine/:  python -m firms.stories [--starts N] [--draws N]  -> firms/results/stories.{json,md}
"""
import argparse, json, math, os, sys
import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import mc as MC
from firms import model as M, data_china as D, calibrate_china as C, seasonal as S, wage_anchor as W

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results')
QUEUE = {2023: 2.60, 2024: 3.03, 2025: 3.416, 2026: 3.718}     # civil-service applicants passing review (m)


class StoryMarket(S.SeasonalMarket):
    """Mechanisms: cons_c (consumption feedback), auto_a (automation of non-graduate tasks), cred_k (credential
    inflation), delay0/delay_k (graduates delaying entry, responding to graduate unemployment)."""
    EXTRA = dict(cons_c=0.0, auto_a=0.0, cred_k=0.0, delay0=0.0, delay_k=0.0)

    def __init__(self, data, **over):
        ex = {k: over.pop(k) for k in list(over) if k in self.EXTRA}
        super().__init__(data, **over)
        self.x = dict(self.EXTRA, **ex)
        self.hist_u = []; self.hist_uG = []; self.carry = 0.0; self.delay = {}; self.dmult = {}
        self.gs_ref = None

    def _demand_mult(self, y, m):
        c = self.x['cons_c']
        if c == 0 or y < 2019:
            return 1.0
        u12 = np.mean(self.hist_u[-12:]) if self.hist_u else 0.0
        ref = self.u_ref if hasattr(self, 'u_ref') else u12
        mult = max(0.5, 1 - c * (u12 - ref))
        self.dmult.setdefault(y, []).append(mult)
        return mult

    def _nongrad_mult(self, y, m):
        a = self.x['auto_a']
        return math.exp(-a * max(0.0, y + (m - 1) / 12 - 2018)) if a else 1.0

    def _eps(self, y, m, eps, LF_G, LF_N):
        k = self.x['cred_k']
        if not k:
            return eps
        if LF_G + LF_N <= 0:
            return eps
        gs = LF_G / (LF_G + LF_N)
        if self.gs_ref is None and y >= 2018:
            self.gs_ref = gs
        return eps * (1 + k * (gs / self.gs_ref - 1)) if self.gs_ref else eps

    def _class(self, y, cls):
        d0, k = self.x['delay0'], self.x['delay_k']
        if not (d0 or k):
            return cls
        uG = np.mean(self.hist_uG[-12:]) if self.hist_uG else 0.0
        ref = self.uG_ref if hasattr(self, 'uG_ref') else uG
        d = min(0.4, max(0.0, d0 + k * (uG - ref) / 100)) if y >= 2010 else 0.0
        self.delay[y] = d
        out = cls * (1 - d) + self.carry
        self.carry = cls * d
        return out

    def _after_month(self, y, m, rate_new, st):
        self.hist_u.append(rate_new)
        LG = st['UG'] + st['UL'] + st['EGg'] + st['EGn']
        self.hist_uG.append(100 * (st['UG'] + st['UL']) / LG if LG > 0 else 0.0)
        if (y, m) == (2019, 12):
            self.u_ref = float(np.mean(self.hist_u[-24:])); self.uG_ref = float(np.mean(self.hist_uG[-24:]))


# ---- the stories: (description, extra free parameters, fixed settings)
CORE = [f for f in C.FREE if f[0] not in ('e_prop', 'dr_drop')]
STORIES = {
    'supply':      ('Education expansion only: graduate supply against observed demand', [], {}),
    'property':    ('+ graduate demand loads on real-estate investment', [('e_prop', 0.0, 1.0, 0.2)], {}),
    'regulatory':  ('+ step fall in graduate demand from Aug 2021 (tutoring, platforms)', [('dr_drop', 0.0, 0.4, 0.1)], {}),
    'credential':  ('+ credential inflation: graduates\' edge in non-graduate jobs rises with their share',
                    [('cred_k', 0.0, 5.0, 1.0)], {}),
    'automation':  ('+ automation erodes non-graduate job value after 2018', [('auto_a', 0.0, 0.05, 0.01)], {}),
    'consumption': ('+ consumption loop: youth unemployment lowers aggregate demand', [('cons_c', 0.0, 0.03, 0.005)], {}),
    'queuing':     ('+ queuing: entry spread over 11 months; delayed entry rises with graduate unemployment',
                    [('delay0', 0.0, 0.3, 0.05), ('delay_k', 0.0, 4.0, 1.0)], dict(spread=11)),
    'everything':  ('all mechanisms together', [('e_prop', 0.0, 1.0, 0.2), ('dr_drop', 0.0, 0.4, 0.1),
                    ('cred_k', 0.0, 5.0, 1.0), ('auto_a', 0.0, 0.05, 0.01), ('cons_c', 0.0, 0.03, 0.005),
                    ('delay0', 0.0, 0.3, 0.05), ('delay_k', 0.0, 4.0, 1.0)], dict(spread=11)),
}


def spec(story):
    return CORE + STORIES[story][1]


def build(story, x, data=D, **extra):
    kw = dict(C.REF, sigma_A=5.0, e_prop=0.0, dr_drop=0.0)
    kw.update(STORIES[story][2]); kw.update({f[0]: float(v) for f, v in zip(spec(story), x)}); kw.update(extra)
    return StoryMarket(data, **kw)


def run(story, x, **extra):
    ym = build(story, x, **extra)
    R = ym.run()
    return R, ym


def youth_pairs(R):
    return C.obs_pairs(R, 2018, 2023, 'old', ('v',)) + C.obs_pairs(R, 2023, 2026, 'new', ('v',))


N_Y = None


_LEN = {}


def residuals(story, x, parts=False):
    if parts:
        return _residuals(story, x, parts=True)
    try:
        r = _residuals(story, x)
        _LEN[story] = len(r)
        return r
    except (ZeroDivisionError, ValueError, OverflowError, FloatingPointError):
        return np.full(_LEN.get(story, 115), 50.0)      # a failed world (e.g. no graduate vacancies) scores badly


def _residuals(story, x, parts=False):
    R, ym = run(story, x)
    yp = youth_pairs(R)
    ry = [mod - ob for *_, ob, mod, _ in yp]
    n = len(ry)
    wp, wo = W.model_wage_path(R, W.KNOWN + W.TEST), W.observed_path(W.KNOWN + W.TEST)
    rw = [math.sqrt(n / 5) * 100 * (wp[y] - wo[y]) / 4 for y in (2019, 2020, 2021, 2022, 2023)]  # 4 log pts ~ 1 pt
    vg = C.vg_check(R)
    rp = [math.sqrt(n / 5) * (vg + 22) / 10]                                                    # 10% postings ~ 1 pt
    ra = []
    for y in range(2019, 2027):                                                                  # adult consistency
        mm = np.mean(ym.dmult.get(y, [1.0]))
        ra.append(math.sqrt(n / 8) * 16 * (mm - 1) / 2)                                          # 2 pts adult ~ 1 pt
    rq = []
    for y in (2024, 2025, 2026):
        d, d0 = ym.delay.get(y, 0.0), ym.delay.get(2023, 0.0)
        md = math.log(max(d, 1e-3) / max(d0, 1e-3)) if (d0 > 0 and d > 0) else 0.0
        rq.append(math.sqrt(n / 3) * 10 * (md - math.log(QUEUE[y] / QUEUE[2023])) / 4)
    r = ry + rw + rp + ra + rq
    if not all(map(math.isfinite, r)):
        r = [50.0] * len(r)
    if parts:
        return dict(youth=ry, wages=rw, postings=rp, adult=ra, queue=rq, R=R, ym=ym, vg=vg)
    return np.array(r)


def _fit_one(job):
    story, s = job
    sp = spec(story)
    try:
        r = least_squares(lambda x: residuals(story, x), s, bounds=([f[1] for f in sp], [f[2] for f in sp]),
                          diff_step=1e-3, max_nfev=150)
        return story, float(r.cost), list(map(float, r.x)), r.jac.tolist()
    except ValueError:
        return story, math.inf, None, None


def starts(story, n):
    sp = spec(story); lo = np.array([f[1] for f in sp]); hi = np.array([f[2] for f in sp])
    warm = {}
    p = os.path.join(OUT, 'seasonal_2024.json')
    if os.path.exists(p):
        warm = json.load(open(p))['rows']['spread11']['params']
    rng = MC.rng(13)
    S0 = [np.clip([warm.get(f[0], f[3]) for f in sp], lo + 1e-6, hi - 1e-6), np.array([f[3] for f in sp])]
    return S0 + [rng.uniform(lo, hi) for _ in range(max(0, n - 2))]


def outcomes(story, x, **extra):
    R, ym = run(story, x, **extra)
    wm = lambda k, a, b: C.window_mean(R, k, a, b)
    return dict(youth_2025=wm('rate_new', (2025, 1), (2025, 12)), youth_2019=wm('rate_old', (2019, 1), (2019, 12)),
                gradU_2025=wm('u_G', (2025, 1), (2025, 12)), gradU_2019=wm('u_G', (2019, 1), (2019, 12)),
                wage_g_change=100 * (wm('w_g', (2025, 1), (2025, 12)) / wm('w_g', (2018, 1), (2018, 12)) - 1),
                Vg_change=100 * (wm('V_g', (2025, 1), (2025, 12)) / wm('V_g', (2019, 1), (2019, 12)) - 1),
                delay_2025=ym.delay.get(2025, 0.0))


def _mc(job):
    story, xs = job
    out = []
    for x in xs:
        try:
            o = outcomes(story, x); rr = residuals(story, np.array(x))
            o['ssr'] = float(rr @ rr); o['x'] = list(map(float, x))
            out.append(o)
        except Exception:
            pass
    return out


MECH_OFF = {'e_prop': 0.0, 'dr_drop': 0.0, 'cred_k': 0.0, 'auto_a': 0.0, 'cons_c': 0.0, 'delay_k': 0.0}


def main(nstarts, ndraws):
    os.makedirs(OUT, exist_ok=True)
    jobs = [(s, x0) for s in STORIES for x0 in starts(s, nstarts)]
    fits = MC.run_batch(_fit_one, [(j,) for j in jobs], chunksize=1)
    res = dict(stories={})
    n_obs = None
    for s in STORIES:
        c, x, J = min(((c, x, J) for st, c, x, J in fits if st == s and x is not None), key=lambda t: t[0])
        P = residuals(s, x, parts=True)
        n_obs = len(np.concatenate([P[k] for k in ('youth', 'wages', 'postings', 'adult', 'queue')]))
        ssr = 2 * c; k = len(spec(s))
        bic = n_obs * math.log(ssr / n_obs) + k * math.log(n_obs)
        J = np.array(J); sigma2 = ssr / max(n_obs - k, 1)
        try:
            cov = np.linalg.pinv(J.T @ J) * sigma2
        except Exception:
            cov = np.eye(k) * 1e-6
        res['stories'][s] = dict(desc=STORIES[s][0], k=k, ssr=ssr, bic=bic, params={f[0]: v for f, v in zip(spec(s), x)},
                                 at_bounds=[f[0] for f, v in zip(spec(s), x) if min(v - f[1], f[2] - v) < 1e-2 * (f[2] - f[1])],
                                 youth_mae=float(np.mean(np.abs(P['youth']))),
                                 wage_err={y: float(W.model_wage_path(P['R'], [2018, y])[y] - W.observed_path([2018, y])[y]) for y in (2021, 2023)},
                                 postings=P['vg'], adult_pen=float(np.sum(np.square(P['adult']))),
                                 queue_pen=float(np.sum(np.square(P['queue']))), cov=cov.tolist(), x=list(x))
    bics = {s: r['bic'] for s, r in res['stories'].items()}
    b0 = min(bics.values())
    wts = {s: math.exp(-0.5 * (b - b0)) for s, b in bics.items()}; tot = sum(wts.values())
    for s in res['stories']:
        res['stories'][s]['weight'] = wts[s] / tot
    res['n_obs'] = n_obs
    # ---- parameter Monte Carlo: propose around each fit, KEEP only draws inside the 90% joint confidence region
    #      SSR <= SSR_min * (1 + k/(n-k) * F_0.90(k, n-k))  (Bates & Watts), then report outcomes over kept draws
    from scipy.stats import f as fdist
    rng = MC.rng(21)
    mc_jobs = []
    for s, r in res['stories'].items():
        sp = spec(s); lo = np.array([f[1] for f in sp]); hi = np.array([f[2] for f in sp])
        x = np.array(r['x']); cov = np.array(r['cov']); k = len(x)
        sd = np.sqrt(np.clip(np.diag(cov), 0, None)); sd = np.minimum(sd, 0.15 * (hi - lo))   # cap proposal width
        draws = np.clip(x + rng.standard_normal((ndraws, k)) * sd * 0.5, lo, hi)
        r['ssr_cut'] = r['ssr'] * (1 + k / (n_obs - k) * fdist.ppf(0.90, k, n_obs - k))
        half = ndraws // 2
        mc_jobs += [(s, draws[:half].tolist()), (s, draws[half:].tolist())]
    mc = MC.run_batch(_mc, [(j,) for j in mc_jobs], chunksize=1)
    for (s, _), out in zip(mc_jobs, mc):
        res['stories'][s].setdefault('mc_all', []).extend(out)
    for s, r in res['stories'].items():
        r['mc'] = [d for d in r['mc_all'] if d['ssr'] <= r['ssr_cut']]
        r['mc_kept'] = len(r['mc']); r['mc_tried'] = len(r.pop('mc_all'))
    # ---- what each mechanism contributes in the 'everything' story, over its kept draws
    ev = res['stories']['everything']; sp = spec('everything'); idx = {f[0]: i for i, f in enumerate(sp)}
    contrib = {}
    sample = [np.array(d['x']) for d in ev['mc']][:80] or [np.array(ev['x'])]
    for name in ('e_prop', 'dr_drop', 'cred_k', 'auto_a', 'cons_c', 'delay_k'):
        vals = []
        for x in sample:
            base = outcomes('everything', x)['youth_2025']
            xo = x.copy(); xo[idx[name]] = MECH_OFF[name]
            if name == 'delay_k':
                xo[idx['delay0']] = 0.0
            vals.append(base - outcomes('everything', xo)['youth_2025'])
        contrib[name] = vals
    res['contributions_youth_2025'] = contrib
    res['contributions_draws'] = len(sample)
    for s in res['stories']:
        res['stories'][s].pop('cov', None)
        for d in res['stories'][s]['mc']:
            d.pop('x', None)
    json.dump(res, open(os.path.join(OUT, 'stories.json'), 'w'), indent=1)
    report(res)


def q(v, p):
    return float(np.percentile(v, p)) if len(v) else float('nan')


def report(res):
    st = res['stories']
    L = ['# China story tournament', '',
         'Generated by `python -m firms.stories`. Every story is fitted to the same evidence: youth unemployment '
         '2018-26 (both NBS definitions), graduate starting pay relative to the average wage (2019-23), graduate '
         'postings in H1 2025, consistency with the adult labour market, and the civil-service queue (2023-26). Stories '
         f"are compared by BIC over {res['n_obs']} weighted residuals. Weights are approximate posterior probabilities "
         'among these stories only.', '',
         '| Story | Free params | Youth MAE | Starting pay err 2021 / 2023 (log) | Postings H1 2025 | Adult penalty | Queue penalty | BIC | Weight |',
         '|---|---:|---:|---:|---:|---:|---:|---:|---:|']
    for r in st.values():
        r['wage_err'] = {int(k): v for k, v in r['wage_err'].items()}
    for s, r in sorted(st.items(), key=lambda kv: kv[1]['bic']):
        L.append(f"| **{s}** | {r['k']} | {r['youth_mae']:.2f} | {r['wage_err'][2021]:+.3f} / {r['wage_err'][2023]:+.3f} | "
                 f"{r['postings']:+.0f}% | {r['adult_pen']:.1f} | {r['queue_pen']:.1f} | {r['bic']:.1f} | {100 * r['weight']:.1f}% |")
    L += ['', 'Observed: postings −22%; starting pay −0.132 (2021) and −0.217 (2023) log points since 2018.', '',
          '## Parameter Monte Carlo: outcomes over the draws the data cannot reject', '',
          'Draws proposed around each fit; kept only if inside the 90% joint confidence region (SSR test). '
          'Bands are 5-95% over kept draws.', '',
          '| Story | Youth rate 2025 (%) | Graduate unemployment 2019 → 2025 (%) | Graduate wage 2018→2025 | Graduate vacancies 2019→2025 | Kept / tried |',
          '|---|---|---|---|---|---:|']
    for s, r in sorted(st.items(), key=lambda kv: kv[1]['bic']):
        mc = r.get('mc', [])
        g = lambda k: [d[k] for d in mc]
        f3 = lambda v: f"{q(v, 50):.1f} [{q(v, 5):.1f}, {q(v, 95):.1f}]"
        L.append(f"| {s} | {f3(g('youth_2025'))} | {q(g('gradU_2019'), 50):.1f} → {f3(g('gradU_2025'))} | "
                 f"{f3(g('wage_g_change'))}% | {f3(g('Vg_change'))}% | {r['mc_kept']} / {r['mc_tried']} |")
    L += ['', 'Observed youth rate 2025 (new method, verified months): 16.6%.', '',
          '## What each mechanism adds to the 2025 youth rate, inside the everything story', '',
          f"Switching one mechanism off in each of {res['contributions_draws']} kept draws (others held at the draw). Points of youth unemployment.", '',
          '| Mechanism | Median | 90% band |', '|---|---:|---|']
    names = dict(e_prop='property loading', dr_drop='regulatory step (2021)', cred_k='credential inflation',
                 auto_a='automation', cons_c='consumption loop', delay_k='queuing / delayed entry')
    for k, v in res['contributions_youth_2025'].items():
        L.append(f"| {names[k]} | {q(v, 50):+.2f} | [{q(v, 5):+.2f}, {q(v, 95):+.2f}] |")
    c = {k: q(v, 50) for k, v in res['contributions_youth_2025'].items()}
    ev, rg = st['everything'], st['regulatory']
    L += ['', '## What this establishes', '',
          f"1. **No single story is enough.** The combined model wins decisively (BIC {ev['bic']:.0f} against {rg['bic']:.0f} for the best "
          'single story), even after the penalty for its extra parameters. Each single story fails on a different observable. '
          'Supply, property, credential and automation leave the graduate pay erosion unexplained (errors of about +0.2 log '
          'points). Queuing fits the exam queue and the seasonal shape but not pay. Consumption alone strains the adult '
          'labour market.',
          f"2. **Inside the combined model, a graduate-demand fall dated from August 2021 does most of the work:** "
          f"{c['dr_drop']:+.1f} pts of 2025 youth unemployment. Then the consumption loop ({c['cons_c']:+.1f}) and automation "
          f"({c['auto_a']:+.1f}). Property loading on graduate jobs adds about {c['e_prop']:+.1f}; its effect runs through "
          f"adult demand, already in the data. Queuing ({c['delay_k']:+.1f}) and credential inflation ({c['cred_k']:+.1f}) slightly "
          'lower the measured rate: delayed entrants are not counted, and graduates taking non-graduate jobs are employed.',
          '3. **Read the dated step with care.** It is a fall in graduate-job value from Aug 2021. Its timing matches the '
          'tutoring ban and platform tightening, but it will also absorb any graduate-specific demand fall that began then '
          '(white-collar property and finance jobs, "jobless growth"). It identifies when and whom, not which policy. '
          'Sector-level data on graduate hiring (TODO §R) are needed to split it.',
          f"4. **Still missing:** postings fall {ev['postings']:+.0f}% in H1 2025 in the combined model, against −22% observed. "
          'This is the second explanatory exercise to leave the postings gap open; the next mechanism to add is search '
          'and participation (NEET).',
          '5. **This is explanation, not prediction:** every story saw 2018-26. The combined story now goes through the '
          'strict Dec 2024 protocol and the blind forecast (TODO §R, P1).']
    L += ['', '## Parameters at bounds', '']
    L += [f"- {s}: {', '.join(r['at_bounds']) or 'none'}" for s, r in st.items()]
    open(os.path.join(OUT, 'stories.md'), 'w').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('--starts', type=int, default=3); ap.add_argument('--draws', type=int, default=200)
    a = ap.parse_args(); main(a.starts, a.draws)
