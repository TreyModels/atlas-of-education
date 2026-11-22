#!/usr/bin/env python3
"""Figures for the report. Usage: make_figures.py ISO VERSION PREFERRED_KEY (e.g. PHL v3 income|trend)."""
import json, os, sys

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
import masseng as m
from masseng import targets as T, calibrate as C
from masseng.engine import Model

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ISO, VERSION, KEY = sys.argv[1], sys.argv[2], sys.argv[3]
OUT = os.path.join(ROOT, 'outputs', ISO, VERSION, 'figures')
os.makedirs(OUT, exist_ok=True)
INK, MUTED, TRAIN, TEST, BM = '#1f2328', '#8b949e', '#2f6db5', '#c2410c', '#6e7781'
plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.titlesize': 10, 'axes.titleweight': 'bold'})

LABEL = {'ger_primary': 'Primary GER', 'ger_secondary': 'Secondary GER', 'ger_tertiary': 'Tertiary GER',
         'ner_primary': 'Primary NER', 'ner_secondary': 'Secondary NER', 'priv_primary': 'Private share, primary',
         'priv_secondary': 'Private share, secondary', 'priv_tertiary': 'Private share, tertiary'}


def load(key):
    d, s = key.split('|')
    return json.load(open(os.path.join(ROOT, 'outputs', ISO, VERSION, f'fit_{d}_{s}.json')))


def run(f, **kw):
    return Model(c, f['params'], supply_rule=f['supply_rule'], demand_form=f['demand_form'],
                 burden_form=f.get('burden_form', 'linear'), split_income=f.get('split_income', False),
                 split_nu=f.get('split_nu', False), **kw
                 ).run(record_deciles=True)


c = m.Country(ISO)
rows = T.build(c)
f = load(KEY)
res = run(f)
lo, hi = c.config['years']['train']
window = [r for r in rows if r['role'] in ('train', 'diagnostic')]

# ---- figure 1: fit and test, with naive benchmarks
series = [s for s in LABEL if any(r['series'] == s for r in rows)]
n = len(series)
fig, axes = plt.subplots(2, (n + 1) // 2, figsize=(4.0 * ((n + 1) // 2), 6.4))
for ax, s in zip(axes.flat, series):
    ax.axvspan(c.config['years']['test'][0] - 0.5, c.config['years']['test'][1] + 0.5, color='#f6f8fa', zorder=0)
    ax.plot(res.years, res.ind[s], color=INK, lw=1.6, label='model')
    for role, col, lab in (('train', TRAIN, 'fitted on'), ('test', TEST, 'held out'), ('diagnostic', MUTED, 'not used')):
        pts = sorted((r['year'], r['value']) for r in rows if r['series'] == s and r['role'] == role)
        if pts:
            ax.plot(*zip(*pts), 'o', color=col, ms=3.2, label=lab, zorder=3)
    hist = sorted((r['year'], r['value']) for r in window if r['series'] == s)
    if len(hist) >= 3:
        yy = np.arange(hi, c.config['years']['test'][1] + 1)
        b = np.polyfit([h[0] for h in hist], [h[1] for h in hist], 1)
        ax.plot(yy, np.polyval(b, yy), ':', color=BM, lw=1, label='naive: trend')
        ax.plot(yy, np.full(len(yy), hist[-1][1]), '--', color=BM, lw=1, label='naive: last value')
    ax.set_title(LABEL[s])
    ax.set_xlim(c.config['years']['train'][0] - 3, c.config['years']['test'][1] + 1)
for ax in axes.flat[n:]:
    ax.axis('off')
axes.flat[0].legend(frameon=False, fontsize=7, loc='lower left')
fig.suptitle(f"{c.config['country']}: model fitted on {lo}–{hi} (blue), tested on later years (orange, shaded)",
             x=0.01, ha='left', fontsize=11, fontweight='bold')
fig.tight_layout()
fig.savefig(os.path.join(OUT, 'fit_and_test.png'), dpi=160)
plt.close(fig)

# ---- figure 2: demand rivals (if available)
riv = {}
rs = 'fiscal' if ISO == 'PHL' else f['supply_rule']   # PHL demand rivals were fitted with S1
for k in (f'income|{rs}', f'trend|{rs}', f'none|{rs}'):
    p = os.path.join(ROOT, 'outputs', ISO, VERSION, 'fit_' + k.replace('|', '_') + '.json')
    if os.path.exists(p):
        riv[k.split('|')[0]] = run(json.load(open(p)))
if len(riv) > 1:
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    col = {'income': INK, 'trend': '#7c3aed', 'none': '#0f766e'}
    lab = {'income': 'D1 demand follows national income', 'trend': 'D2 smooth diffusion trend', 'none': 'D3 no demand growth'}
    for ax, s in zip(axes, ('ger_secondary', 'ger_tertiary')):
        for yr in ((1983.5, 1986.5), (1997.5, 1999.5), (2019.5, 2020.5)):
            ax.axvspan(*yr, color='#fde68a', alpha=0.45, zorder=0)
        for k, r in riv.items():
            ax.plot(r.years, r.ind[s], color=col[k], lw=1.4, label=lab[k])
        pts = sorted((r['year'], r['value']) for r in rows if r['series'] == s)
        ax.plot(*zip(*pts), 'o', color=MUTED, ms=3, label='WDI')
        ax.set_title(LABEL[s] + ' under the three demand rivals')
        ax.set_xlim(1968, 2025)
    axes[0].legend(frameon=False, fontsize=7)
    fig.text(0.01, 0.01, 'Yellow bands: falls in GDP per head (1984–86, 1998–99, 2020).', fontsize=7, color=MUTED)
    fig.tight_layout(rect=(0, 0.04, 1, 1))
    fig.savefig(os.path.join(OUT, 'demand_rivals.png'), dpi=160)
    plt.close(fig)

# ---- figure 3: participation by income decile
yr = 2019 if ISO == 'PHL' else 2012
dp = res.extra['deciles'].get(yr)
if dp:
    fig, ax = plt.subplots(figsize=(6.2, 3.6))
    for lev, colr in (('primary', '#2f6db5'), ('secondary', '#0f766e'), ('tertiary', '#c2410c')):
        if dp.get(lev):
            ax.plot(range(1, 11), np.minimum(dp[lev], 130), '-o', color=colr, ms=3, label=f'model, {lev}')
    tg = c.config.get('targets', {})
    g = tg.get('income_gradient_2019') or tg.get('income_gradient_2012')
    if g:
        for lev, colr in (('primary', '#2f6db5'), ('secondary', '#0f766e'), ('tertiary', '#c2410c')):
            if lev in g:
                ax.plot([1, 10], [g[lev]['poorest'], g[lev]['richest']], 's', color=colr, mfc='white', ms=6)
    ax.set_xlabel('income decile (1 = poorest)')
    ax.set_ylabel('participation, % of decile\'s official-age population')
    ax.set_title(f'Participation by income decile, {yr} (squares: survey poorest and richest)')
    ax.legend(frameon=False, fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'deciles.png'), dpi=160)
    plt.close(fig)

# ---- figure 4 (PHL): K-12 transition, tertiary
if ISO == 'PHL':
    ched = c.config['targets']['ched_tertiary']
    yrs = list(res.years)
    base = res.ind['enrol_tertiary'][yrs.index(2016)]
    fig, axes = plt.subplots(1, 2, figsize=(10, 3.6))
    ax = axes[0]
    ax.plot(res.years, res.ind['ger_tertiary'], color=INK, lw=1.6, label='model')
    pts = sorted((r['year'], r['value']) for r in rows if r['series'] == 'ger_tertiary' and r['year'] >= 2008)
    ax.plot(*zip(*pts), 'o', color=TEST, ms=3.5, label='WDI (held out)')
    ax.set_xlim(2008, 2025); ax.set_title('Tertiary GER through the K-12 transition'); ax.legend(frameon=False, fontsize=7)
    ax = axes[1]
    cy = [int(k[:4]) + 1 for k in ched]
    ax.plot(cy, [ched[k]['total'] / ched['2015-16']['total'] for k in ched], 's-', color=TEST, ms=4,
            label='CHED headcount (held out)')
    ax.plot(range(2014, 2025), [res.ind['enrol_tertiary'][yrs.index(y)] / base for y in range(2014, 2025)],
            color=INK, lw=1.6, label='model enrolment')
    ax.axhline(1, color=MUTED, lw=0.6)
    ax.set_title('Tertiary enrolment, index (AY2015-16 = 1)'); ax.legend(frameon=False, fontsize=7)
    fig.tight_layout()
    fig.savefig(os.path.join(OUT, 'k12_transition.png'), dpi=160)
    plt.close(fig)
print('figures in', OUT)
