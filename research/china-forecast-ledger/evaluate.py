"""Rolling-origin evaluation on the new-method series (Dec 2023 onwards).

For every observed month up to Aug 2026 taken as the forecast origin, each model is run using only data up to that
origin, for horizons 1, 3, 6 and 12 months. A pair (origin, horizon) is scored only if the target month was observed.
Each model is compared with naive_same_month on the pairs where BOTH could forecast. Writes results/rolling_origin.json.
"""
import json, math, os
import numpy as np
import sys
import models as M
sys.path.insert(0, os.path.join(M.HERE, '..', '..', 'engine'))
from firms import data_china as D  # noqa: E402  (read-only; used only to describe the old-method series)

HORIZONS = (1, 3, 6, 12)
LAST_ORIGIN = M.idx(2026, 8)
BENCH = 'naive_same_month'


def collect(series, grads):
    """{model: {h: [(origin, target, forecast, observed), ...]}}"""
    out = {m: {h: [] for h in HORIZONS} for m in M.NAMES}
    for o in sorted(i for i in series if i <= LAST_ORIGIN):
        for h in HORIZONS:
            t = o + h
            if t not in series:
                continue
            for m in M.NAMES:
                f = M.forecast(m, series, grads, o, t)
                if f is not None:
                    out[m][h].append((o, t, f, series[t]))
    return out


def compare(rows_m, rows_b):
    b = {(o, t): f for o, t, f, _ in rows_b}
    pairs = [(o, t, f, ob, b[(o, t)]) for o, t, f, ob in rows_m if (o, t) in b]
    n = len(pairs)
    if n == 0:
        return dict(n=0)
    em = np.array([abs(f - ob) for _, _, f, ob, _ in pairs]); eb = np.array([abs(fb - ob) for *_, ob, fb in pairs])
    d = em - eb
    t = float(d.mean() / (d.std(ddof=1) / math.sqrt(n))) if n >= 3 and d.std(ddof=1) > 0 else None
    return dict(n=n, mae=float(em.mean()), naive_mae=float(eb.mean()), mean_diff=float(d.mean()),
                wins=int((d < 0).sum()), ties=int((d == 0).sum()), win_share=float((d < 0).mean()), t=t,
                first_origin=M.label(min(p[0] for p in pairs)), last_origin=M.label(max(p[0] for p in pairs)))


def run():
    series, grads = M.load_observed(), M.load_graduates()
    col = collect(series, grads)
    res = dict(series=dict(first=M.label(min(series)), last=M.label(max(series)), n_observed=len(series),
                           n_calendar_span=max(series) - min(series) + 1,
                           missing=[M.label(i) for i in range(min(series), max(series) + 1) if i not in series]),
               last_origin=M.label(LAST_ORIGIN), horizons=list(HORIZONS), benchmark=BENCH, models={})
    old = [(y, m) for y in range(2018, 2024) for m in range(1, 13) if (D.youth(y, m) or (0, ''))[1] == 'old']
    res['old_method'] = dict(first=f'{old[0][0]}-{old[0][1]:02d}', last=f'{old[-1][0]}-{old[-1][1]:02d}', n=len(old))
    last = max(series)
    cls = {M.class_year(i) for i in series if i - 12 in series and i <= last}
    cls = {c for c in cls if c in grads and c - 1 in grads}
    res['inflow'] = dict(distinct_classes_in_last_fit=len(cls), first_class=min(cls), last_class=max(cls))
    for m in M.NAMES:
        res['models'][m] = dict(n_params=M.MODELS[m]['n_params'], text=M.MODELS[m]['text'], label=M.MODELS[m]['label'], by_horizon={})
        for h in HORIZONS:
            r = compare(col[m][h], col[BENCH][h]); res['models'][m]['by_horizon'][str(h)] = r
    return res


if __name__ == '__main__':
    res = run()
    os.makedirs(os.path.join(M.HERE, 'results'), exist_ok=True)
    json.dump(res, open(os.path.join(M.HERE, 'results', 'rolling_origin.json'), 'w'), indent=1)
    print(res['series'])
    for m, r in res['models'].items():
        for h, v in r['by_horizon'].items():
            if v['n']:
                print(f"{m:18s} h={h:>2s} n={v['n']:2d} MAE {v['mae']:.2f} naive {v['naive_mae']:.2f} diff {v['mean_diff']:+.2f} "
                      f"win {v['wins']}/{v['n']} t {v['t'] if v['t'] is None else round(v['t'], 2)}  origins {v['first_origin']}..{v['last_origin']}")
            else:
                print(f"{m:18s} h={h:>2s} n=0")
