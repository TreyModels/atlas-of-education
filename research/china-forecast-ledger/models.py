"""Small forecasters for the China youth unemployment rate (new NBS method, 16-24 excluding students).

Every forecaster has at most 4 estimated numbers. Each is called through forecast(), which first throws away every
observation after the forecast origin (and every graduating-class size not yet announced at the origin), so a forecast can
not use later data by construction.

Months are integers: idx = 12 * year + (month - 1). Gaps inside the observed span (Mar and Apr 2026 are not in the data
file) are filled by straight-line interpolation between the neighbouring observed months, and only when a model needs to
read a month that is missing. Forecasts are always scored against real observations only.
"""
import csv, math, os
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OBSERVED = os.path.join(HERE, 'data', 'observed.csv')
GRADUATES = os.path.join(HERE, 'data', 'graduates.csv')
K_DRIFT = 6          # seasonal_drift: number of year-on-year changes averaged (fixed in advance)
N_HARMONICS = 2      # seasonal_profile: harmonics in the seasonal shape (fixed in advance)


def idx(y, m):
    return 12 * y + (m - 1)


def ym(i):
    return divmod(i, 12)[0], divmod(i, 12)[1] + 1


def label(i):
    y, m = ym(i)
    return f'{y}-{m:02d}'


def load_observed(path=OBSERVED):
    s = {}
    with open(path, newline='') as f:
        for r in csv.DictReader(f):
            k = idx(int(r['year']), int(r['month']))
            if k in s:
                raise ValueError(f'duplicate month in {path}: {label(k)}')
            s[k] = float(r['rate'])
    return s


def load_graduates(path=GRADUATES):
    with open(path, newline='') as f:
        return {int(r['year']): float(r['millions']) for r in csv.DictReader(f)}


def known_grads(grads, origin):
    """Class of year c is treated as announced from December of year c-1 (assumption; see README Limits)."""
    return {c: g for c, g in grads.items() if idx(c - 1, 12) <= origin}


def cut(series, origin):
    return {i: v for i, v in series.items() if i <= origin}


def fill(series):
    """Linear interpolation across internal gaps only; nothing before the first or after the last observation."""
    if not series:
        return {}
    ks = sorted(series); out = dict(series)
    for a, b in zip(ks, ks[1:]):
        for i in range(a + 1, b):
            out[i] = series[a] + (series[b] - series[a]) * (i - a) / (b - a)
    return out


def class_year(i):
    """Graduating class that matters for calendar month i: the class of that year from July, otherwise last year's."""
    y, m = ym(i)
    return y if m >= 7 else y - 1


# ---------------------------------------------------------------- the forecasters
def naive_same_month(s, g, origin, target):
    return s.get(target - 12)


def naive_last(s, g, origin, target):
    ks = [i for i in s if i <= origin]
    return s[max(ks)] if ks else None


def seasonal_drift(s, g, origin, target):
    base = s.get(target - 12)
    d = [s[i] - s[i - 12] for i in sorted(s) if i - 12 in s]
    if base is None or len(d) < 3:
        return None
    return base + float(np.mean(d[-K_DRIFT:]))


def _harm(m, h):
    cols = [1.0]
    for j in range(1, h + 1):
        cols += [math.cos(2 * math.pi * j * m / 12), math.sin(2 * math.pi * j * m / 12)]
    return cols


def seasonal_profile(s, g, origin, target):
    ks = sorted(s)
    if len(ks) < 12:
        return None
    X = np.array([_harm(ym(i)[1], N_HARMONICS) for i in ks]); y = np.array([s[i] for i in ks])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    prof = lambda i: float(np.dot(_harm(ym(i)[1], N_HARMONICS)[1:], beta[1:]))   # seasonal shape, no level
    win = [i for i in range(origin - 11, origin + 1) if i in s]
    if len(win) < 8:
        return None
    level = float(np.mean([s[i] - prof(i) for i in win]))
    return level + prof(target)


def _growth(g, c):
    return 100 * (g[c] / g[c - 1] - 1) if c in g and c - 1 in g else None


def graduate_inflow(s, g, origin, target):
    base = s.get(target - 12)
    xt = _growth(g, class_year(target))
    if base is None or xt is None:
        return None
    xs, ys = [], []
    for i in sorted(s):
        if i - 12 in s and _growth(g, class_year(i)) is not None:
            xs.append(_growth(g, class_year(i))); ys.append(s[i] - s[i - 12])
    if len(ys) < 6:
        return None
    xs, ys = np.array(xs), np.array(ys)
    if np.ptp(xs) < 1e-9:
        return base + float(ys.mean())
    b, a = np.polyfit(xs, ys, 1)
    return base + float(a + b * xt)


MODELS = {
    'naive_same_month': dict(fn=naive_same_month, n_params=0, label='Same month last year',
        text='The forecast is the rate for the same calendar month a year earlier. Nothing is estimated. This is the benchmark.'),
    'naive_last': dict(fn=naive_last, n_params=0, label='Last value',
        text='The forecast is the most recent observed rate, whatever month is being forecast. Nothing is estimated.'),
    'seasonal_drift': dict(fn=seasonal_drift, n_params=1, label='Same month plus recent drift',
        text=f'Same month a year earlier, plus the average year-on-year change over the last {K_DRIFT} months. '
             f'One number is estimated (the average change); the window of {K_DRIFT} is fixed in advance.'),
    'seasonal_profile': dict(fn=seasonal_profile, n_params=2 * N_HARMONICS, label='Level plus smooth seasonal shape',
        text=f'A smooth yearly shape ({N_HARMONICS} sine-cosine pairs, so {2 * N_HARMONICS} estimated numbers, fitted to all data up to the '
             f'origin) added to a level set by the average of the last 12 months with the shape removed. The level is set by a rule, '
             f'not fitted. A free 12-month profile would be 11 numbers, so it is shrunk to {N_HARMONICS} pairs.'),
    'graduate_inflow': dict(fn=graduate_inflow, n_params=2, label='Same month plus graduate-cohort shift',
        text='Same month a year earlier, plus a shift that depends on how much bigger the graduating class is than the year before '
             '(percent growth). Two numbers are estimated: a constant shift and a slope on cohort growth, by least squares on '
             'past year-on-year changes. A class counts as known from December of the year before it graduates.'),
}
NAMES = list(MODELS)


def forecast(model, series, grads, origin, target):
    """Forecast for month `target` using only data up to month `origin`. Returns None if the model cannot be fitted."""
    s = fill(cut(series, origin))
    g = known_grads(grads, origin)
    if target <= origin:
        raise ValueError('target must be after the origin')
    v = MODELS[model]['fn'](s, g, origin, target)
    return None if v is None else float(v)
