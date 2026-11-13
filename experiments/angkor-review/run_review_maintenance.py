"""Before/after and isolated-toggle runs for review items 5.4 (canal floor), 5.5 (reshuffle channels)
and 5.6 (elite grain spend). Uses 40 seeds (0-39), the same seeds as experiments/maintenance-repair/run_experiments.py.

Run from the repo root:  python3 experiments/angkor-review/run_review_maintenance.py
"""
from pathlib import Path
import importlib.util, sys, csv, statistics, math
from dataclasses import replace

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
RES = HERE / 'results'
RES.mkdir(exist_ok=True)


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


orig = load('orig_accounted', HERE / 'original/maintenance-repair/accounted.py')
new = load('accounted_v2', HERE / 'model/accounted_v2.py')
SEEDS = range(40)
REGIMES = ('stable', 'maintenance_only', 'reshuffle')


def metrics(h):
    y54 = h[54]['state_population']
    last = h[-1]
    return dict(
        state_final=last['state_population'], refuge_final=last['refuge_population'], total_final=last['total_population'],
        canal_final=last['canal_condition'], shortfall_cum=sum(x['shortfall_kg'] for x in h),
        flight_cum=sum(x['flight'] for x in h), retention=last['state_population'] / y54,
        elite_final=last.get('elite_stock_kg', float('nan')), elite_spent_cum=last.get('elite_spent_kg', float('nan')),
    )


def cell(label, fn, regime, drought, settings_kwargs):
    rows = []
    for seed in SEEDS:
        h = fn(regime, drought, seed, settings_kwargs)
        rows.append(dict(config=label, regime=regime, drought=drought, seed=seed, **metrics(h)))
    return rows


def orig_fn(regime, drought, seed, kw):
    return orig.run(orig.Settings(regime=regime, drought=drought, seed=seed))


def new_fn(regime, drought, seed, kw):
    return new.run(new.Settings(regime=regime, drought=drought, seed=seed, **kw))


# ---------- 0. Regression: flags at old values must reproduce the original bit for bit ----------
max_diff = 0.0
n_checked = 0
for regime in REGIMES:
    for drought in (False, True):
        for seed in SEEDS:
            a = orig.run(orig.Settings(regime=regime, drought=drought, seed=seed))
            b = new.run(new.Settings(regime=regime, drought=drought, seed=seed, canal_floor=.3, elite_spend=0.0, reshuffle_parts='all'))
            for ra, rb in zip(a, b):
                for k in ra:
                    if k in rb:
                        max_diff = max(max_diff, abs(ra[k] - rb[k]))
            n_checked += 1
# Reshuffle with no channel on must equal maintenance_only (the reshuffle code path adds nothing when no channel is on).
eq_diff = 0.0
for drought in (False, True):
    for seed in SEEDS:
        a = new.run(new.Settings(regime='maintenance_only', drought=drought, seed=seed, canal_floor=0, elite_spend=0))
        b = new.run(new.Settings(regime='reshuffle', drought=drought, seed=seed, canal_floor=0, elite_spend=0, reshuffle_parts='none'))
        for ra, rb in zip(a, b):
            for k in ('state_population', 'canal_condition', 'shortfall_kg', 'flight'):
                eq_diff = max(eq_diff, abs(ra[k] - rb[k]))
# Compare the stored accounted runs in experiments/maintenance-repair/runs.csv (engine == accounted).
stored = {}
with (ROOT / 'experiments/maintenance-repair/runs.csv').open() as f:
    for r in csv.DictReader(f):
        if r['engine'] == 'accounted':
            stored[(r['regime'], r['drought'] == 'True', int(r['seed']))] = float(r['state_population'])
stored_diff = 0.0
for regime in REGIMES:
    for drought in (False, True):
        for seed in SEEDS:
            h = orig.run(orig.Settings(regime=regime, drought=drought, seed=seed))
            stored_diff = max(stored_diff, abs(h[-1]['state_population'] - stored[(regime, drought, seed)]))
checks = dict(regression_max_abs_diff=max_diff, regression_runs=n_checked, parts_none_vs_maintenance_only=eq_diff,
              stored_runs_csv_max_abs_diff=stored_diff)
print('CHECKS', checks)

# ---------- 1. Before (original) and after (new defaults) ----------
rows = []
for regime in REGIMES:
    for drought in (False, True):
        rows += cell('before:original', orig_fn, regime, drought, {})
        rows += cell('after:new defaults (canal_floor=0, elite_spend=0.1 relief)', new_fn, regime, drought, {})

# ---------- 2. 5.4 canal floor, isolated (elite_spend=0, all reshuffle parts) ----------
for floor in (0.3, 0.0):
    for regime in REGIMES:
        for drought in (False, True):
            rows += cell(f'5.4 canal_floor={floor}', new_fn, regime, drought,
                         dict(canal_floor=floor, elite_spend=0.0, reshuffle_parts='all'))

# ---------- 3. 5.5 reshuffle channels, one at a time, isolated (canal_floor=0, elite_spend=0) ----------
base = dict(canal_floor=0.0, elite_spend=0.0)
for parts in ('none', 'extraction', 'relief', 'trust', 'grievance', 'all'):
    for drought in (False, True):
        rows += cell(f'5.5 reshuffle parts={parts}', new_fn, 'reshuffle', drought, dict(base, reshuffle_parts=parts))
for drop in ('extraction', 'relief', 'trust', 'grievance'):
    keep = ','.join(p for p in ('extraction', 'relief', 'trust', 'grievance') if p != drop)
    for drought in (False, True):
        rows += cell(f'5.5 leave-out {drop} (parts={keep})', new_fn, 'reshuffle', drought, dict(base, reshuffle_parts=keep))

# ---------- 4. 5.6 elite grain spend (canal_floor=0, all reshuffle parts) ----------
for s in (0.0, 0.1, 0.3):
    for use in ('relief', 'service'):
        for regime in REGIMES:
            for drought in (False, True):
                rows += cell(f'5.6 elite_spend={s} use={use}', new_fn, regime, drought,
                             dict(canal_floor=0.0, elite_spend=s, elite_use=use, reshuffle_parts='all'))

csv_path = RES / 'maintenance-runs.csv'
keys = list(rows[0].keys())
with csv_path.open('w') as f:
    w = csv.DictWriter(f, fieldnames=keys)
    w.writeheader(); w.writerows(rows)


def mean_sd(xs):
    m = statistics.fmean(xs)
    sd = statistics.stdev(xs) if len(xs) > 1 else 0.
    s = sorted(xs)
    q = lambda p: s[min(len(s) - 1, int(p * (len(s) - 1) + .5))]
    return m, sd, q(.1), q(.9)


def fmt(xs, d=1):
    if any(math.isnan(x) for x in xs):
        return 'n/a'
    m, sd, lo, hi = mean_sd(xs)
    return f'{m:.{d}f} ± {sd:.{d}f} [{lo:.{d}f}, {hi:.{d}f}]'


configs = []
for r in rows:
    if r['config'] not in configs:
        configs.append(r['config'])
md = ['| Config | Regime | Drought | State pop. final (x1) | Retention (final / year 54) | Share of seeds with retention < 0.5 | Refuge final | Canal final | Cum. shortfall (kg) | Cum. flight | Elite stock final (kg) |',
      '|---|---|---|---|---|---|---|---|---|---|---|']
for cfg in configs:
    for regime in REGIMES:
        for drought in (False, True):
            g = [r for r in rows if r['config'] == cfg and r['regime'] == regime and r['drought'] == drought]
            if not g:
                continue
            collapse = sum(1 for r in g if r['retention'] < .5) / len(g)
            md.append(f"| {cfg} | {regime} | {'drought' if drought else 'stable'} | {fmt([r['state_final'] for r in g],0)} | "
                      f"{fmt([r['retention'] for r in g],3)} | {collapse:.2f} | {fmt([r['refuge_final'] for r in g],0)} | "
                      f"{fmt([r['canal_final'] for r in g],3)} | {fmt([r['shortfall_cum'] for r in g],0)} | "
                      f"{fmt([r['flight_cum'] for r in g],0)} | {fmt([r['elite_final'] for r in g],0)} |")
(RES / 'maintenance-summary.md').write_text('\n'.join(md) + '\n')
(RES / 'maintenance-checks.json').write_text(__import__('json').dumps(checks, indent=2))
print('\n'.join(md))
print('rows', len(rows), 'configs', len(configs))
