"""Analyse the coupled MASSENG v5 run grid: system ledger, coupling effects, multiverse, reality check.

Reads results/coupling_raw.json (server run), results/bray_check.json, results/channel_decomposition.json and
writes results/summary.json + results/tables.md.

SIMULATION output; no causal claims.  A "seed" is one declared +/-20% parameter-uncertainty draw (MASSENG v5 is
deterministic, so there is no sampling seed).
"""
import gzip
import json
import os

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RESULTS = os.path.join(os.path.dirname(HERE), 'results')


def _load(name):
    """Load a results file, plain JSON or the committed .json.gz (large raw grid)."""
    p = os.path.join(RESULTS, name)
    if os.path.exists(p):
        return json.load(open(p))
    return json.load(gzip.open(p + '.gz', 'rt'))
YEARS = [1970, 1990, 2000, 2010, 2018, 2024]
SYSTEM = ['ger_primary', 'ger_secondary', 'ger_tertiary', 'ner_primary', 'ner_secondary',
          'priv_primary', 'priv_secondary', 'priv_lower_secondary', 'priv_upper_secondary', 'priv_tertiary',
          'trans_lsec_usec', 'S_primary', 'S_secondary', 'S_tertiary', 'edu_share_hh', 'edu_share_bottom30',
          'edu_share_top70', 'hh_share_total_spending', 'pool_share_20_24']
EFFECT = ['ger_primary', 'ger_secondary', 'ger_tertiary', 'ner_secondary', 'S_secondary', 'S_tertiary',
          'edu_share_hh', 'hh_share_total_spending', 'priv_secondary', 'priv_upper_secondary', 'priv_tertiary']


def _v(run, key, year):
    try:
        v = run['ind'][key][run['years'].index(year)]
        return float(v) if v is not None and np.isfinite(v) else None
    except (KeyError, ValueError):
        return None


def _delta(a, b, key, year):
    x, y = _v(a, key, year), _v(b, key, year)
    if x is None or y is None:
        return None
    return round(x - y, 4)


def _pred(**kw):
    def f(g):
        return all(g.get(k) == v for k, v in kw.items())
    return f


def _runs(raw, pred):
    return [r for r in raw['runs'] if 'error' not in r and pred(r['config'])]


def _dropout(run):
    e = np.array(run['flows']['entered_by_decile'], float)
    d = np.array(run['flows']['drops_by_decile'], float)
    return (d / np.maximum(e, 1)).round(4).tolist()


def main():
    raw = _load('coupling_raw.json')
    bray = _load('bray_check.json')
    chan = _load('channel_decomposition.json')
    base = raw['baseline_off_pristine']
    off = [r for r in raw['runs'] if r['config'].get('off') and not r['config'].get('capacity')][0]
    off_cap = [r for r in raw['runs'] if r['config'].get('off') and r['config'].get('capacity')][0]
    out = {'meta': raw['meta']}

    # switch-off arm must equal the pristine baseline exactly
    out['switch_off_arm_equals_pristine'] = all(
        _v(off, k, y) == _v(base, k, y) for k in off['ind'] for y in YEARS)

    # ---------------------------------------------------------------- system ledger (off, no tutoring)
    sysled = {k: {y: _v(base, k, y) for y in YEARS} for k in SYSTEM}
    out['system_ledger_off'] = sysled
    out['dropout_baseline'] = _dropout(base)
    out['grads_by_decile_level'] = np.array(base['flows']['grads_by_decile_level']).round(2).tolist()

    # ---------------------------------------------------------------- arm effects, mean over the 3 draws
    ref = off
    specs = [
        ('central_learning_only', _pred(fee=1.0, ban=False, feedback=False, odds_multiplier=1.10,
                                        quality='spend', capacity=False, off=False), ref),
        ('central_learning_plus_financing', _pred(fee=1.0, ban=False, feedback=True, odds_multiplier=1.10,
                                                  quality='spend', capacity=False, off=False), ref),
        ('learning_only_ban_own', _pred(fee=1.0, ban=True, feedback=False, odds_multiplier=1.10,
                                        quality='spend', capacity=False, off=False), ref),
        ('learning_only_fee_low', _pred(fee=0.5, ban=False, feedback=False, odds_multiplier=1.10,
                                        quality='spend', capacity=False, off=False), ref),
        ('learning_only_fee_high', _pred(fee=2.0, ban=False, feedback=False, odds_multiplier=1.10,
                                         quality='spend', capacity=False, off=False), ref),
        ('financing_only', _pred(fee=1.0, ban=False, feedback=True, odds_multiplier=1.0,
                                 quality='spend', capacity=False, off=False), ref),
        ('learning_mult_1.05', _pred(fee=1.0, ban=False, feedback=True, odds_multiplier=1.05,
                                     quality='spend', capacity=False, off=False), ref),
        ('learning_mult_1.20', _pred(fee=1.0, ban=False, feedback=True, odds_multiplier=1.20,
                                     quality='spend', capacity=False, off=False), ref),
        ('quality_teachers', _pred(fee=1.0, ban=False, feedback=True, odds_multiplier=1.10,
                                   quality='teachers', capacity=False, off=False), ref),
        ('limited_places_gate', _pred(fee=1.0, ban=False, feedback=True, odds_multiplier=1.10,
                                      quality='spend', capacity=True, off=False), ref),
        ('limited_places_gate_off', _pred(fee=1.0, ban=False, feedback=True, odds_multiplier=1.10,
                                          quality='spend', capacity=True, off=True), ref),
    ]
    arms = {}
    for name, pred, rf in specs:
        runs = _runs(raw, pred)
        row = {'n_runs': len(runs)}
        for k in EFFECT + ['tut_participation', 'tut_spend_share_gdp', 'tut_participation_gap_q5_q1']:
            for y in (2010, 2024):
                vals = ([_v(r, k, y) for r in runs] if k.startswith('tut_')
                        else [_delta(r, rf, k, y) for r in runs])
                vals = [v for v in vals if v is not None]
                row[f'{k}_{y}'] = round(float(np.mean(vals)), 4) if vals else None
        for y in (2010, 2024):
            d = [[round(a - b, 4) for a, b in zip(_dropout(r), _dropout(base))] for r in runs]
            row[f'dropout_by_decile_{y}'] = ([round(float(np.mean([v[i] for v in d])), 4) for i in range(10)]
                                             if d else None)
        arms[name] = row
    out['arms'] = arms

    # seed spread: central arms, 2010
    spread = {}
    for name, fb in (('central_learning_only', False), ('central_learning_plus_financing', True)):
        vals = {k: [] for k in ('ger_secondary', 'ger_tertiary', 'S_secondary', 'edu_share_hh')}
        part = []
        for s in (0, 1, 2):
            r = [q for q in raw['runs'] if q['config'].get('tag') == f'ON_f1.0_ban0_fb{int(fb)}_s{s}'][0]
            for k in vals:
                vals[k].append(_delta(r, off, k, 2010))
            part.append(_v(r, 'tut_participation', 2010))
        spread[name] = {k: dict(values=v, mean=round(float(np.mean(v)), 4),
                                sd=round(float(np.std(v, ddof=1)), 4)) for k, v in vals.items()}
        spread[name]['tut_participation_2010'] = dict(values=part, mean=round(float(np.mean(part)), 4),
                                                      sd=round(float(np.std(part, ddof=1)), 4))
    out['seed_spread_2010'] = spread

    # ---------------------------------------------------------------- tutoring demand: who buys, where it piles up
    central = [q for q in raw['runs'] if q['config'].get('tag') == 'ON_f1.0_ban0_fb0_s0'][0]
    panel = central['tutoring']['panel']
    tut = {}
    for y in ('2010', '2024'):
        p = panel.get(y)
        if not p:
            continue
        part = np.array(p['part'])          # (10 deciles, 4 levels)
        prob = np.array(p['prob'])          # (10, 4, 4)
        denom = max(part.sum(), 1e-12)
        tut[y] = dict(
            participation_by_decile=part.mean(axis=1).round(3).tolist(),
            participation_by_level=part.mean(axis=0).round(3).tolist(),
            own_share_among_tutored=round(float(prob[..., 1].sum() / denom), 3),
            other_share_among_tutored=round(float(prob[..., 2].sum() / denom), 3),
            commercial_share_among_tutored=round(float(prob[..., 3].sum() / denom), 3),
            spend_per_tutored_pupil_by_decile=(
                (0.03 * (prob[..., 1] * 1.0 + prob[..., 2] * 0.8 + prob[..., 3] * 1.5)
                 / np.maximum(part, 1e-12)).mean(axis=1)).round(4).tolist())
    out['tutoring_demand'] = tut
    out['tutoring_central_params'] = central['params_used']
    out['tutoring_central_b0'] = central['b0_calibrated']

    # ---------------------------------------------------------------- PHL fit consistency (not validation)
    tags = ('OFF', 'OFF_capacity', 'ON_f1.0_ban0_fb0_s0', 'ON_f1.0_ban0_fb1_s0', 'GATE_capacity_s0')
    fit = {}
    for q in raw['runs']:
        if q['config'].get('tag') in tags:
            fit[q['config']['tag']] = q['score']
    fit['baseline_pristine'] = base['score']
    base_ser = base['score']['by_series']
    out['phl_fit_consistency'] = fit
    out['phl_fit_series_delta'] = {}
    for tag, sc in fit.items():
        if tag == 'baseline_pristine':
            continue
        out['phl_fit_series_delta'][tag] = {
            s: (round(sc['by_series'][s]['rmse'] - base_ser[s]['rmse'], 3)
                if sc['by_series'].get(s) and base_ser.get(s)
                and sc['by_series'][s].get('rmse') is not None and base_ser[s].get('rmse') is not None else None)
            for s in base_ser}

    # ---------------------------------------------------------------- reality checks
    out['demand_mix_check_bray'] = {
        'provenance': bray['checker_provenance'], 'n_draws': bray['n_draws'],
        'n_fit_all_seven': bray['n_fit_all_seven'], 'best_max_z': round(bray['best']['max_z'], 3),
        'patterns': {k: dict(target=bray['targets'][k][0], tol=bray['targets'][k][1],
                             best=round(bray['best'][k], 3), z=round(bray['best']['z_' + k], 2))
                     for k in bray['targets']},
    }
    out['channel_decomposition_2010'] = {
        k: {kk: vv[kk]['2010'] for kk in ('ger_secondary', 'ger_tertiary', 'S_secondary', 'edu_share_hh')}
        for k, vv in chan['deltas_vs_baseline'].items()}
    json.dump(out, open(os.path.join(RESULTS, 'summary.json'), 'w'), indent=2)

    # ---------------------------------------------------------------- markdown tables
    def f(x, nd=2):
        return '—' if x is None else (f'{x:.{nd}f}' if isinstance(x, float) else str(x))

    L = ['# Coupled-run summary tables (generated by analyse_results.py)\n',
         'SIMULATION; no causal claims. Baseline = untouched MASSENG v5 R1 PHL fit (`fit_R1.json`), 1940-2024. '
         'A "seed" is a declared ±20% parameter-uncertainty draw; MASSENG v5 is deterministic.\n',
         '## 1. System ledger, tutoring OFF (PHL R1 baseline)\n',
         '| indicator | ' + ' | '.join(str(y) for y in YEARS) + ' |', '|---|' + '---|' * len(YEARS)]
    for k in SYSTEM:
        if k in sysled:
            L.append(f'| {k} | ' + ' | '.join(f(sysled[k][y]) for y in YEARS) + ' |')
    L.append('\n| | d1 | d2 | d3 | d4 | d5 | d6 | d7 | d8 | d9 | d10 |')
    L.append('|---|---|---|---|---|---|---|---|---|---|---|')
    L.append('| dropout per entrant | ' + ' | '.join(f'{v:.3f}' for v in out['dropout_baseline']) + ' |')
    L.append('\n## 2. Coupling effect, by level and by income decile (deltas from baseline; mean over 3 draws)\n')
    L.append('| arm | Δ GER sec 2010 | Δ GER ter 2010 | Δ S_sec 2010 | Δ GER sec 2024 | Δ GER ter 2024 | '
             'Δ S_sec 2024 | Δ edu_share_hh 2010 | tut part 2010 | tut part 2024 |')
    L.append('|---|---|---|---|---|---|---|---|---|---|')
    for name, row in arms.items():
        L.append(f"| {name} | {f(row['ger_secondary_2010'])} | {f(row['ger_tertiary_2010'])} | "
                 f"{f(row['S_secondary_2010'], 4)} | {f(row['ger_secondary_2024'])} | {f(row['ger_tertiary_2024'])} | "
                 f"{f(row['S_secondary_2024'], 4)} | {f(row['edu_share_hh_2010'])} | "
                 f"{f(row['tut_participation_2010'], 3)} | {f(row['tut_participation_2024'], 3)} |")
    L.append('\nDropout-per-entrant *change* by decile (negative = kept in school), central learning-only arm, 2010: '
             + ', '.join(f'{v:+.3f}' for v in (arms['central_learning_only']['dropout_by_decile_2010'] or [])))
    L.append('\nDropout-per-entrant *change* by decile, learning+financing arm, 2010: '
             + ', '.join(f'{v:+.3f}' for v in (arms['central_learning_plus_financing']['dropout_by_decile_2010'] or [])))
    L.append('\n## 3. Seed spread (declared ±20% parameter-uncertainty draws), central arms, 2010\n')
    L.append('| arm | quantity | draw 0 | draw 1 | draw 2 | mean | sd |')
    L.append('|---|---|---|---|---|---|---|')
    for name, sp in spread.items():
        for k, d in sp.items():
            vals = ' | '.join(f'{v:.3f}' if isinstance(v, float) else str(v) for v in d['values'])
            L.append(f"| {name} | {k} | {vals} | {d['mean']:.3f} | {d['sd']:.3f} |")
    L.append('\n## 4. PHL held-out fit consistency (retrospective/inspected; NOT validation)\n')
    L.append('| arm | three-GER RMSE | Δ vs baseline | GER primary | GER secondary | GER tertiary | edu_share_hh |')
    L.append('|---|---|---|---|---|---|---|')
    b3 = base['score']['three_ger_rmse']
    for tag, sc in fit.items():
        s = sc['by_series']

        def rm(k):
            return s[k]['rmse'] if s.get(k) and s[k].get('rmse') is not None else None
        L.append(f'| {tag} | {f(sc["three_ger_rmse"], 3)} | {f((sc["three_ger_rmse"] - b3) if sc["three_ger_rmse"] else None, 3)} | '
                 f'{f(rm("ger_primary"), 3)} | {f(rm("ger_secondary"), 3)} | {f(rm("ger_tertiary"), 3)} | '
                 f'{f(rm("edu_share_hh"), 3)} |')
    L.append('\nPer-series RMSE change vs the matching baseline (negative = closer to observed):\n')
    L.append('| series | baseline RMSE | learning-only Δ | learning+financing Δ | gate Δ (vs gate OFF) |')
    L.append('|---|---|---|---|---|')
    gate = [q for q in raw['runs'] if q['config'].get('tag') == 'GATE_capacity_s0'][0]['score']['by_series']
    for s in base_ser:
        bl = base_ser[s]['rmse']
        if bl is None:
            continue
        d1 = out['phl_fit_series_delta'].get('ON_f1.0_ban0_fb0_s0', {}).get(s)
        d2 = out['phl_fit_series_delta'].get('ON_f1.0_ban0_fb1_s0', {}).get(s)
        d3 = None
        ob = off_cap['score']['by_series'].get(s)
        if ob and ob.get('rmse') is not None and gate.get(s) and gate[s].get('rmse') is not None:
            d3 = round(gate[s]['rmse'] - ob['rmse'], 3)
        L.append(f'| {s} | {f(bl, 3)} | {f(d1, 3)} | {f(d2, 3)} | {f(d3, 3)} |')
    L.append('\n## 5. Bray six-school demand-mix check (Cambodia; NOT PHL validation)\n')
    L.append(f"provenance: {bray['checker_provenance']}\n")
    L.append(f"draws: {bray['n_draws']}; draws fitting all seven patterns within tolerance: "
             f"{bray['n_fit_all_seven']} ({100 * bray['n_fit_all_seven'] / bray['n_draws']:.4f}%); "
             f"best max |z| = {bray['best']['max_z']:.3f}\n")
    L.append('| pattern | target | tolerance | best draw | |z| |')
    L.append('|---|---|---|---|---|')
    for k, d in out['demand_mix_check_bray']['patterns'].items():
        L.append(f"| {k} | {d['target']} | ±{d['tol']} | {d['best']} | {d['z']} |")
    L.append('\n## 6. Tutoring demand in the coupled model (central arm)\n')
    for y, d in tut.items():
        L.append(f"\n**{y}** — participation by level (primary/secondary/upper-secondary/tertiary): "
                 f"{d['participation_by_level']}; by decile: {d['participation_by_decile']}")
        L.append(f"\nprovider mix among tutored: own {d['own_share_among_tutored']}, "
                 f"other {d['other_share_among_tutored']}, commercial {d['commercial_share_among_tutored']}")
    L.append('\n## 7. Channel decomposition at 2010 (from channel_decomposition.py)\n')
    L.append('| arm | Δ GER secondary | Δ GER tertiary | Δ S_secondary | Δ edu_share_hh |')
    L.append('|---|---|---|---|---|')
    for k, d in out['channel_decomposition_2010'].items():
        L.append(f"| {k} | {f(d['ger_secondary'])} | {f(d['ger_tertiary'])} | {f(d['S_secondary'], 4)} | "
                 f"{f(d['edu_share_hh'])} |")
    open(os.path.join(RESULTS, 'tables.md'), 'w').write('\n'.join(L) + '\n')
    print('wrote results/summary.json and results/tables.md')
    print('switch-off arm equals pristine baseline:', out['switch_off_arm_equals_pristine'])
    print('arm run counts:', {k: v['n_runs'] for k, v in arms.items()})


if __name__ == '__main__':
    main()
