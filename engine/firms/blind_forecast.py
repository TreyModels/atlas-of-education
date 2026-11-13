"""Freeze a blind forecast for future NBS releases (written 5 Nov 2026; do not regenerate after Oct 2026 data appear).

Model: seasonal_2024 variant 'spread11' with the parameters stored in results/seasonal_2024.json, data frozen at
Dec 2024 and the same prespecified input rules. Benchmark: same calendar month of 2024 (new definition).
`python -m firms.blind_forecast` writes results/blind_forecast_2026_11.{json,md} only if they do not exist;
`python -m firms.blind_forecast --score` scores whatever new verified months data_china.py now holds.
"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from firms import seasonal_2024 as S, forecast_2024 as F4, data_china as D, calibrate_china as C

OUT = S.OUT
PATH = os.path.join(OUT, 'blind_forecast_2026_11.json')
FIRST = (2026, 10)


def make():
    if os.path.exists(PATH):
        print('blind forecast already frozen:', PATH); return json.load(open(PATH))
    res = json.load(open(os.path.join(OUT, 'seasonal_2024.json')))['rows']['spread11']
    x = [res['params'][f[0]] for f in C.FREE + S.VARIANTS['spread11']['extra']]
    R = S.run(x, 'spread11'); nf = F4.naive('same_month_2024')
    rows = {f"{y}-{m:02d}": dict(model=round(r, 2), naive=nf(y, m))
            for y, m, r in zip(R['year'], R['month'], R['rate_new']) if (y, m) >= FIRST and y <= 2027}
    out = dict(written='2026-11-05', model='seasonal_2024 spread11, data frozen Dec 2024', forecasts=rows)
    json.dump(out, open(PATH, 'w'), indent=1)
    L = ['# Blind forecast, frozen 5 November 2026', '', 'NBS urban surveyed unemployment, 16-24 excluding students (%). '
         'Model: `seasonal_2024` spread11, data frozen at Dec 2024. Score with `python -m firms.blind_forecast --score` '
         'as releases arrive; never refit before scoring.', '', '| Month | Model | Naive (same month 2024) |', '|---|---:|---:|']
    L += [f"| {k} | {v['model']:.1f} | {v['naive']:.1f} |" for k, v in rows.items()]
    open(PATH.replace('.json', '.md'), 'w').write('\n'.join(L) + '\n')
    return out


def score():
    f = json.load(open(PATH))['forecasts']; pr = []
    for k, v in f.items():
        y, m = map(int, k.split('-')); o = D.youth(y, m)
        if o and o[1] == 'new' and o[2] == 'v':
            pr.append((k, o[0], v['model'], v['naive']))
    if not pr:
        print('no verified months yet'); return
    em = sum(abs(a - b) for _, b, a, _ in pr) / len(pr); en = sum(abs(c - b) for _, b, _, c in pr) / len(pr)
    print(f"{len(pr)} months: model MAE {em:.2f}, naive {en:.2f}")


if __name__ == '__main__':
    score() if '--score' in sys.argv else make()
