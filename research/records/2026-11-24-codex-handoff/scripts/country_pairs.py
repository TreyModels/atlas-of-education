#!/usr/bin/env python3
"""Prospective descriptive matching on baseline only; no causal or significance claims."""
import argparse
import hashlib
import json
from pathlib import Path
import numpy as np
import pandas as pd

FEATURES = ['mean_years_schooling', 'tfr_observed_1950plus', 'gdp_pc_maddison_1990int', 'urban_share_pct']

def match(panel, baseline=1980, start=1990, end=2010):
    if not baseline < start < end:
        raise ValueError('Require baseline < start < end')
    needed = ['iso3', 'year'] + FEATURES
    missing = set(needed) - set(panel.columns)
    if missing:
        raise ValueError(f'Missing columns: {sorted(missing)}')
    if panel.duplicated(['iso3', 'year']).any():
        raise ValueError('Duplicate country-years')
    d = panel.copy()
    d['iso3'] = d['iso3'].astype(str)
    # Pair selection depends only on baseline features, not on outcome availability.
    base = d.loc[d.year.eq(baseline), ['iso3'] + FEATURES].set_index('iso3').sort_index().dropna()
    base = base[base['gdp_pc_maddison_1990int'] > 0].copy()
    if len(base) < 4:
        raise ValueError('At least four complete baseline countries required')
    base['gdp_pc_maddison_1990int'] = np.log(base['gdp_pc_maddison_1990int'])
    sd = base.std(ddof=0)
    if (sd <= 0).any() or not np.isfinite(sd).all():
        raise ValueError('Baseline features must have positive finite variation')
    z = (base - base.mean()) / sd
    iso = z.index.to_numpy(); v = z.to_numpy()
    candidates = []
    for i in range(len(iso)):
        for j in range(i + 1, len(iso)):
            candidates.append((float(np.linalg.norm(v[i] - v[j])), iso[i], iso[j]))
    # Greedy disjoint pairs; no optimal-assignment claim. Deterministic tie break.
    chosen, used = [], set()
    for dist, a, b in sorted(candidates):
        if a not in used and b not in used:
            chosen.append((a, b, dist)); used.update((a, b))
    out = pd.DataFrame(chosen, columns=['country_a', 'country_b', 'baseline_distance'])
    # Future differences are computed AFTER pairs are frozen; no selection on outcomes.
    targets = ['mean_years_schooling', 'tfr_observed_1950plus']
    a = d.loc[d.year.eq(start), ['iso3'] + targets].set_index('iso3')
    b = d.loc[d.year.eq(end), ['iso3'] + targets].set_index('iso3')
    changes = b.reindex(base.index)[targets] - a.reindex(base.index)[targets]
    for column, label in [(targets[0], 'schooling_change'), (targets[1], 'tfr_change')]:
        out[f'{label}_a'] = out.country_a.map(changes[column])
        out[f'{label}_b'] = out.country_b.map(changes[column])
        out[f'{label}_absolute_gap'] = (out[f'{label}_a'] - out[f'{label}_b']).abs()
    return out, {'baseline': baseline, 'outcome_start': start, 'outcome_end': end,
                 'eligible_baseline_countries': len(base), 'pairs': len(out),
                 'unpaired_countries': len(base)-2*len(out),
                 'pairs_with_both_tfr_changes': int(out.tfr_change_absolute_gap.notna().sum()),
                 'pairs_with_both_school_changes': int(out.schooling_change_absolute_gap.notna().sum()),
                 'matching': 'greedy disjoint Euclidean distance on baseline z-scores; GDP logged',
                 'note': 'Descriptive, selected baseline complete cases; no significance test or causal inference.'}

def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--panel', type=Path, required=True)
    ap.add_argument('--out', type=Path, required=True)
    ap.add_argument('--baseline', type=int, default=1980)
    ap.add_argument('--start', type=int, default=1990)
    ap.add_argument('--end', type=int, default=2010)
    args = ap.parse_args()
    out, meta = match(pd.read_csv(args.panel), args.baseline, args.start, args.end)
    meta['input_sha256'] = hashlib.sha256(args.panel.read_bytes()).hexdigest()
    args.out.mkdir(parents=True, exist_ok=True)
    out.to_csv(args.out / 'pairs.csv', index=False, float_format='%.8g')
    (args.out / 'pairs_metadata.json').write_text(json.dumps(meta, indent=2) + '\n')
    print(json.dumps(meta, sort_keys=True))

if __name__ == '__main__':
    main()
