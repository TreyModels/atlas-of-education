"""Create ledger.csv: frozen forecasts for Oct 2026 - Mar 2027 from every model, using data through the last month in
data/observed.csv (Sep 2026), plus the repo's earlier frozen blind forecast under its original freeze date.

The ledger is append-only. This script refuses to run if ledger.csv already exists.
"""
import csv, json, os, sys
import models as M

LEDGER = os.path.join(M.HERE, 'ledger.csv')
FROZEN = '2026-11-14'
TARGETS = [M.idx(2026, 10) + k for k in range(6)]      # Oct 2026 .. Mar 2027
BLIND = os.path.join(M.HERE, '..', '..', 'engine', 'firms', 'results', 'blind_forecast_2026_11.json')
SEAS = os.path.join(M.HERE, '..', '..', 'engine', 'firms', 'results', 'seasonal_2024.json')
FIELDS = ['model', 'target_month', 'forecast', 'data_cutoff', 'date_frozen', 'horizon', 'n_params', 'note']


def rows():
    series, grads = M.load_observed(), M.load_graduates()
    cutoff = max(series)
    out = []
    for name in M.NAMES:
        for t in TARGETS:
            f = M.forecast(name, series, grads, cutoff, t)
            if f is None:
                raise RuntimeError(f'{name} could not forecast {M.label(t)}')
            out.append(dict(model=name, target_month=M.label(t), forecast=f'{f:.2f}', data_cutoff=M.label(cutoff), date_frozen=FROZEN,
                            horizon=t - cutoff, n_params=M.MODELS[name]['n_params'],
                            note=M.MODELS[name]['label'] + ('; reference month last year not observed, linearly interpolated'
                                                            if name not in ('naive_last', 'seasonal_profile') and (t - 12) not in series else '')))
    blind = json.load(open(BLIND))
    npar = len(json.load(open(SEAS))['rows']['spread11']['params'])
    for k, v in blind['forecasts'].items():
        y, m = map(int, k.split('-'))
        out.append(dict(model='blind_seasonal_2024_spread11', target_month=k, forecast=f"{v['model']:.2f}", data_cutoff='2024-12',
                        date_frozen=blind['written'], horizon='', n_params=npar,
                        note='existing engine model, frozen 5 Nov 2026 on data to Dec 2024 (new-method fit window Dec 2023-Dec 2024)'))
        out.append(dict(model='blind_naive_2024', target_month=k, forecast=f"{v['naive']:.2f}", data_cutoff='2024-12',
                        date_frozen=blind['written'], horizon='', n_params=0, note='its own benchmark: same month of 2024'))
    return out


if __name__ == '__main__':
    if os.path.exists(LEDGER):
        sys.exit('ledger.csv exists; the ledger is append-only and is not regenerated')
    r = rows()
    with open(LEDGER, 'w', newline='') as f:
        w = csv.DictWriter(f, FIELDS); w.writeheader(); w.writerows(r)
    print(len(r), 'rows written')
