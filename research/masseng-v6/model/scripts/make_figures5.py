#!/usr/bin/env python3
"""Regenerate PHL v5 figures only from final fit and score files."""
import json
import os
from pathlib import Path

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

from masseng.data import Country
from masseng.engine5 import Model5

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / 'outputs' / 'PHL' / 'v5'
FIG = OUT / 'figures'
FIG.mkdir(parents=True, exist_ok=True)
SCORES = json.loads((OUT / 'scores.json').read_text())
WINNER = SCORES['winner_by_preregistered_rule']
C = Country('PHL')
FITS = {s: json.loads((OUT / f'fit_{s}.json').read_text()) for s in sorted(SCORES['rivals'])}
RESULTS = {s: Model5(C, f['params'], spec=s).run(record_deciles=True) for s, f in FITS.items()}
YEARS = list(RESULTS[WINNER].years)
INK, MUTED, TRAIN, TEST = '#1f2328', '#8b949e', '#2f6db5', '#c2410c'
COLOURS = {'R0': '#6e7781', 'R1': '#1f2328', 'R2': '#7c3aed', 'R3': '#0f766e', 'R4': '#b45309', 'R5': '#be123c'}
LABELS = {
    'ger_primary': 'Primary GER (%)', 'ger_secondary': 'Secondary GER (%)',
    'ger_tertiary': 'Tertiary GER (%)', 'enrol_tertiary': 'CHED tertiary headcount index (2016 = 1)',
    'edu_share_hh': 'Household education spending share (%)',
    'hh_share_total_spending': 'Household share of total education spending (%)',
}
plt.rcParams.update({'font.size': 9, 'axes.spines.top': False, 'axes.spines.right': False,
                     'axes.titlesize': 10, 'axes.titleweight': 'bold'})


def curve(spec, series):
    r = RESULTS[spec]
    values = r.ind[series]
    if series == 'enrol_tertiary':
        base = float(values[YEARS.index(2016)])
        return [float(v) / base for v in values]
    return values


fig, axes = plt.subplots(2, 3, figsize=(13, 7))
for ax, series in zip(axes.flat, LABELS):
    ax.axvspan(1995.5, 2024.5, color='#f6f8fa', zorder=0)
    ax.plot(YEARS, curve(WINNER, series), color=INK, lw=1.5, label=f'{WINNER} model')
    table = SCORES['rivals'][WINNER]['series_losses'].get(series)
    if table:
        ax.plot(table['years'], table['obs'], 'o', color=TEST, ms=3.5, label='held-out observation')
    ax.set_title(LABELS[series])
    ax.set_xlim(1970 if series.startswith('ger_') else 1988, 2025)
axes.flat[0].legend(frameon=False, fontsize=8)
fig.suptitle(f'Philippines v5: {WINNER}; orange observations were not used in fitting', x=.01, ha='left', fontsize=12, fontweight='bold')
fig.text(.01, .01, 'Retrospective inspected test; not blind. The post-1995 enrolment series were not fitted. CHED values are indexed to 2016.', fontsize=8, color=MUTED)
fig.tight_layout(rect=(0, .035, 1, 1))
fig.savefig(FIG / 'fit_and_test.png', dpi=160)
plt.close(fig)

fig, axes = plt.subplots(1, 2, figsize=(11, 4))
for ax, series in zip(axes, ('ger_secondary', 'ger_tertiary')):
    for spec in sorted(RESULTS):
        ax.plot(YEARS, curve(spec, series), color=COLOURS[spec], lw=1.25, label=spec)
    table = SCORES['rivals'][WINNER]['series_losses'][series]
    ax.plot(table['years'], table['obs'], 'o', color=MUTED, ms=2.8, label='observed')
    ax.set_title(LABELS[series])
    ax.set_xlim(1968, 2025)
axes[0].legend(frameon=False, fontsize=7, ncol=2)
fig.suptitle('Pre-registered demand rivals: losses and selection are in scores.json', x=.01, ha='left', fontsize=11, fontweight='bold')
fig.tight_layout()
fig.savefig(FIG / 'demand_rivals.png', dpi=160)
plt.close(fig)
print(f'figures regenerated from {WINNER} and final rival outputs in {FIG}')
