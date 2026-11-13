"""Whole-record China fit with Tilly's mechanisms switched on (secure posts, hoarding, waiting, emulation,
exploitation), freeing the waiting and emulation rates alongside the model.py parameters.

Run from engine/:  python -m firms.tilly_fit   -> firms/results/tilly_fit.{json,md}
Question tested: does adaptation (waiting outside the labour force for hoarded posts) let the model match the bulge
without the implausible 31% fall in graduate-job productivity the model.py fit needed?
"""
import json, math, os, sys
import numpy as np
from scipy.optimize import least_squares

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firms import categorical as C, calibrate_china as K, data_china as D

HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'results')
FIXED = dict(sec_open=0.10, hoard=0.4, ins_g=0.5, ins_n=0.5, ex=0.2, sigma_A=5.0)
FREE = K.FREE + [('wait_max', 0.0, 0.3, 0.05), ('em_rate', 0.0, 2.0, 0.3)]


def run(th, **over):
    kw = dict(K.REF, **FIXED)
    kw.update({n: float(v) for (n, *_), v in zip(FREE, th)}); kw.update(over)
    return C.CategoricalMarket(D, **kw).run()


def resid(th):
    R = run(th)
    pr = K.pairs_for(R, 'full')
    r = [mod - ob for *_, ob, mod, _ in pr]
    return np.array(r) if all(map(math.isfinite, r)) else np.full(len(pr), 50.0)


def main():
    lo = [f[1] for f in FREE]; hi = [f[2] for f in FREE]
    prev = json.load(open(os.path.join(OUT, 'china_fit.json')))['profiles']['full|sigma_A=5.0']['params']
    starts = [np.array([prev.get(f[0], f[3]) for f in FREE])]
    starts[0] = np.clip(starts[0], np.array(lo) + 1e-6, np.array(hi) - 1e-6)
    rng = np.random.default_rng(3)
    starts += [rng.uniform(lo, hi) for _ in range(3)]
    best = None
    for s in starts:
        try:
            r = least_squares(resid, s, bounds=(lo, hi), diff_step=1e-3, max_nfev=300)
        except ValueError:
            continue
        if best is None or r.cost < best.cost:
            best = r
    th = best.x; R = run(th)
    st = lambda pr: K.stats(pr)
    E, L = K.EARLY, K.LATE
    m = lambda R, k, w: K.window_mean(R, k, *w)
    res = dict(params={n: float(v) for (n, *_), v in zip(FREE, th)}, fixed=FIXED, cost=float(best.cost),
               whole_record=st(K.pairs_for(R, 'full')), new_verified=st(K.obs_pairs(R, 2023, 2026, 'new', flags=('v',))),
               holdout_old_2023H1=st(K.obs_pairs(R, 2023, 2023, 'old')),
               rate_change=m(R, 'rate_new', L) - m(R, 'rate_new', E), slack_change=m(R, 'slack', L) - m(R, 'slack', E),
               waiting_late=m(R, 'waiting', L), c_req_late=m(R, 'c_req', L),
               p_g_change_pct=100 * (m(R, 'p_g', L) / m(R, 'p_g', E) - 1), w_g_change_pct=100 * (m(R, 'w_g', L) / m(R, 'w_g', E) - 1),
               vg_2025H1_pct=K.vg_check(R), uG_in=m(R, 'u_G_in', L), uG_out=m(R, 'u_G_out', L),
               sec_ins_share=m(R, 'sec_ins_share', L), max_balance=float(max(abs(b) for b in R['balance'])))
    for name, ov in (('no waiting', dict(wait_max=0.0)), ('no hoarding', dict(hoard=0.0)), ('no emulation', dict(em_rate=0.0)),
                     ('graduates held at 2018', dict(grad_supply=lambda y: D.graduates(min(y, 2018)))),
                     ('no graduate-demand step', dict(grad_demand='flat'))):
        Rx = run(th, **ov)
        res[f'cf: {name}'] = dict(rate_change=m(Rx, 'rate_new', L) - m(Rx, 'rate_new', E),
                                  slack_change=m(Rx, 'slack', L) - m(Rx, 'slack', E))
    res['series'] = {k: R[k] for k in ('year', 'month', 'rate_old', 'rate_new', 'slack', 'waiting', 'c_req')}
    json.dump(res, open(os.path.join(OUT, 'tilly_fit.json'), 'w'), indent=1, default=float)
    print(json.dumps({k: v for k, v in res.items() if k != 'series'}, indent=1, default=float))


if __name__ == '__main__':
    main()
