#!/usr/bin/env python3
"""Step one of PROTOCOL_v5: invert the fitted model for the additive utility shift delta_L(y) that reproduces
observed WDI GER for level L in year y (secondary, tertiary), year by year with earlier shifts kept (sequential
filtering). In each year the secondary shift is solved first, then the tertiary one (tertiary entry in year y
depends on same-year secondary completions, not the reverse).
Usage: python3 scripts/invert_demand5.py ISO SPEC [--from YEAR] [--to YEAR]
Writes outputs/<ISO>/v5/inverted_demand_<SPEC>.json and figures/inverted_demand_<SPEC>.png."""
import argparse, json, os, sys

import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import brentq

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)
import masseng as m
from masseng.engine5 import Model5

LEVELS = {'secondary': (1, 2), 'tertiary': (3,)}
SERIES = {'secondary': ('ger_secondary', 'SE.SEC.ENRR'), 'tertiary': ('ger_tertiary', 'SE.TER.ENRR')}
BOUND = 10.0


class ShiftedModel5(Model5):
    """Model5 with an additive utility shift delta[(level, year_index)] on the base term."""

    def __init__(self, *a, **k):
        self.delta = {}
        super().__init__(*a, **k)

    def _base(self, yi, li, S):
        b = super()._base(yi, li, S)
        for lev, lis in LEVELS.items():
            if li in lis:
                b = b + self.delta.get((lev, yi), 0.0)
        return b


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('iso'); ap.add_argument('spec')
    ap.add_argument('--from', dest='y_from', type=int, default=None)
    ap.add_argument('--to', dest='y_to', type=int, default=2024)
    a = ap.parse_args()
    c = m.Country(a.iso)
    d = os.path.join(ROOT, 'outputs', a.iso, 'v5')
    f = json.load(open(os.path.join(d, f'fit_{a.spec}.json')))
    mod = ShiftedModel5(c, f['params'], spec=f['spec'])
    y0 = a.y_from or c.config['years']['train'][0]
    years = list(mod.years)
    obs = {lev: c.wdi(code).observed() for lev, (_, code) in SERIES.items()}
    delta = {lev: {} for lev in LEVELS}
    flags = {lev: {} for lev in LEVELS}
    for y in range(y0, a.y_to + 1):
        yi = years.index(y)
        for lev in ('secondary', 'tertiary'):
            if y not in obs[lev]:
                continue
            ser, target = SERIES[lev][0], obs[lev][y]

            def gap(x):
                mod.delta[(lev, yi)] = x
                return float(mod.run().ind[ser][yi]) - target
            lo, hi = gap(-BOUND), gap(BOUND)
            if lo * hi > 0:                       # target outside the reachable range: keep the nearer bound
                x = -BOUND if abs(lo) < abs(hi) else BOUND
                flags[lev][y] = 'bracket_failed'
            else:
                x = brentq(gap, -BOUND, BOUND, xtol=1e-3)
            mod.delta[(lev, yi)] = x
            delta[lev][y] = float(x)
        print(y, {lev: round(delta[lev].get(y, float('nan')), 3) for lev in delta}, flush=True)
    # correlations with drivers (levels and first differences, over shared years)
    drv_names = ['premium_tertiary', 'premium_secondary', 'occ_credential_share', 'formal_share']
    drivers = {n: c.drivers[n] for n in drv_names if n in c.drivers}
    corr = {}
    for lev in delta:
        ys = sorted(delta[lev])
        for n, s in drivers.items():
            obsyrs = set(s.observed())
            lo_y, hi_y = min(obsyrs), max(obsyrs)
            sel = [y for y in ys if lo_y <= y <= hi_y]      # no flat extrapolation outside the driver's data
            if len(sel) < 4:
                corr[f'{lev}~{n}'] = dict(n=len(sel), level=None, diff=None); continue
            dv = np.array([delta[lev][y] for y in sel]); xv = np.array([s(y) for y in sel])
            r_l = float(np.corrcoef(dv, xv)[0, 1]) if xv.std() > 0 else None
            r_d = float(np.corrcoef(np.diff(dv), np.diff(xv))[0, 1]) if np.diff(xv).std() > 0 else None
            corr[f'{lev}~{n}'] = dict(n=len(sel), level=r_l, diff=r_d, years=[sel[0], sel[-1]])
    out = dict(spec=a.spec, params=f['params'], delta={lev: {str(y): v for y, v in delta[lev].items()} for lev in delta},
               flags={lev: {str(y): v for y, v in flags[lev].items()} for lev in flags}, correlations=corr)
    json.dump(out, open(os.path.join(d, f'inverted_demand_{a.spec}.json'), 'w'), indent=1, default=float)
    # figure
    os.makedirs(os.path.join(d, 'figures'), exist_ok=True)
    fig, ax = plt.subplots(figsize=(9, 4.4))
    for lev, col in (('secondary', '#0f766e'), ('tertiary', '#c2410c')):
        if delta[lev]:
            ys = sorted(delta[lev])
            ax.plot(ys, [delta[lev][y] for y in ys], '-o', ms=3, color=col, label=f'delta {lev} (left axis)')
    for r in ((1983.5, 1986.5), (1997.5, 1998.5)):
        ax.axvspan(*r, color='#fde68a', alpha=0.5, zorder=0)
    ax.axhline(0, color='#8b949e', lw=0.6)
    ax.set_ylabel('additive utility shift'); ax.set_xlabel('year')
    ax2 = ax.twinx(); ax2.spines['right'].set_visible(True)
    sty = {'premium_tertiary': ('#c2410c', '--'), 'premium_secondary': ('#0f766e', '--'),
           'occ_credential_share': ('#7c3aed', ':'), 'formal_share': ('#6e7781', ':')}
    for n, s in drivers.items():
        o = s.observed(); ys = sorted(o)
        v = np.array([o[y] for y in ys])
        if n in ('occ_credential_share', 'formal_share') and v.max() > 1.5:
            v = v / 100.0
        ax2.plot(ys, v, sty[n][1], color=sty[n][0], lw=1.2, label=f'{n} (right axis)')
    ax2.set_ylabel('driver (premium in log points; shares 0-1)')
    h1, l1 = ax.get_legend_handles_labels(); h2, l2 = ax2.get_legend_handles_labels()
    ax.legend(h1 + h2, l1 + l2, frameon=False, fontsize=7, loc='best')
    ax.set_title(f'{a.iso} {a.spec}: demand shift needed to hit observed GER (shaded: 1984-86, 1998)')
    ax.set_xlim(y0 - 1, a.y_to + 1)
    fig.tight_layout()
    fig.savefig(os.path.join(d, 'figures', f'inverted_demand_{a.spec}.png'), dpi=160)
    print('correlations:')
    for k, v in corr.items():
        print(' ', k, v)


if __name__ == '__main__':
    main()
