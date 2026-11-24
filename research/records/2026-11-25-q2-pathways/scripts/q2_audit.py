#!/usr/bin/env python3
"""Q2 pathway audit: coverage, matching sensitivity, random yardstick, case candidates, dated farming.

Descriptive only. No causal inference. See PRE_REGISTRATION.md (committed before this ran).
"""
import argparse, json, hashlib
from pathlib import Path
import numpy as np
import pandas as pd

FEATURES = ['mean_years_schooling', 'tfr_observed_1950plus', 'gdp_pc_maddison_1990int', 'urban_share_pct']
OUTCOMES = ['mean_years_schooling', 'tfr_observed_1950plus']

def sha256(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()

def load_panel(path):
    d = pd.read_csv(path)
    d['iso3'] = d['iso3'].astype(str)
    return d

def baseline_frame(d, baseline=1980):
    base = d.loc[d.year.eq(baseline), ['iso3'] + FEATURES].set_index('iso3').sort_index().dropna()
    base = base[base['gdp_pc_maddison_1990int'] > 0].copy()
    base['gdp_pc_maddison_1990int'] = np.log(base['gdp_pc_maddison_1990int'])
    return base

def zframe(base):
    sd = base.std(ddof=0)
    return (base - base.mean()) / sd, sd

def pairing_greedy(cost, names):
    n = len(names); chosen, used = [], set()
    for i in range(n):
        for j in range(i + 1, n):
            pass
    order = sorted((cost[i, j], i, j) for i in range(n) for j in range(i + 1, n))
    for dist, i, j in order:
        a, b = names[i], names[j]
        if a not in used and b not in used:
            chosen.append((a, b, float(dist))); used.update((a, b))
    return chosen

def pair_frame(chosen, d, start=1990, end=2010):
    out = pd.DataFrame(chosen, columns=['country_a', 'country_b', 'baseline_distance'])
    lv = {}
    for yr in (1980, start, end):
        lv[yr] = d.loc[d.year.eq(yr), ['iso3'] + OUTCOMES].set_index('iso3')
    for col in OUTCOMES:
        for yr in (1980, start, end):
            out[f'{col}_{yr}_a'] = out.country_a.map(lv[yr][col])
            out[f'{col}_{yr}_b'] = out.country_b.map(lv[yr][col])
        out[f'{col}_change_a'] = out[f'{col}_{end}_a'] - out[f'{col}_{start}_a']
        out[f'{col}_change_b'] = out[f'{col}_{end}_b'] - out[f'{col}_{start}_b']
        out[f'{col}_gap'] = (out[f'{col}_change_a'] - out[f'{col}_change_b']).abs()
    return out

def alt_matchings(base, names, cost_matrix, cost_greedy):
    variants = {}
    variants['greedy_euclid'] = pairing_greedy(cost_greedy, names)
    # Manhattan
    man = np.abs(base.values[:, None, :] - base.values[None, :, :]).sum(-1)
    np.fill_diagonal(man, np.inf)
    variants['greedy_manhattan'] = pairing_greedy(man, names)
    # 3-feature (drop TFR)
    drop = base.drop(columns=['tfr_observed_1950plus'])
    z3 = (drop - drop.mean()) / drop.std(ddof=0)
    c3 = np.linalg.norm(z3.values[:, None, :] - z3.values[None, :, :], axis=-1)
    np.fill_diagonal(c3, np.inf)
    variants['greedy_three_feature'] = pairing_greedy(c3, names)
    # Mahalanobis with regularised covariance
    X = base.values
    cov = np.cov(X, rowvar=False) + 1e-6 * np.eye(X.shape[1])
    inv = np.linalg.pinv(cov)
    dm = np.zeros((len(X), len(X)))
    for i in range(len(X)):
        dv = X[i] - X
        dm[i] = np.einsum('ij,jk,ik->i', dv, inv, dv) ** 0.5
    np.fill_diagonal(dm, np.inf)
    variants['greedy_mahalanobis'] = pairing_greedy(dm, names)
    # Approximate optimal matching: greedy on Mahalanobis, then deterministic 2-opt swaps.
    # (networkx/Hungarian assignment unavailable in the box environment; documented as a deviation.)
    base_pairs = pairing_greedy(dm, names)
    idx = {n: i for i, n in enumerate(names)}
    pairs = [(a, b) for a, b, _ in base_pairs]
    improved = True
    while improved:
        improved = False
        for i in range(len(pairs)):
            for j in range(i + 1, len(pairs)):
                a, b = pairs[i]; c, d = pairs[j]
                cur = dm[idx[a], idx[b]] + dm[idx[c], idx[d]]
                for na, nb, nc, nd in ((a, c, b, d), (a, d, b, c)):
                    newcost = dm[idx[na], idx[nb]] + dm[idx[nc], idx[nd]]
                    if newcost < cur - 1e-12:
                        pairs[i] = (na, nb); pairs[j] = (nc, nd); improved = True
                        break
                if improved:
                    break
            if improved:
                break
    variants['optimal_mahalanobis'] = [(a, b, float(dm[idx[a], idx[b]])) for a, b in pairs]
    return variants

def random_yardstick(d, base, n_draws=1000, seed=71201, start=1990, end=2010):
    rng = np.random.default_rng(seed)
    names = list(base.index)
    # changes from the panel (levels at start and end), keyed by country
    lv0 = d.loc[d.year.eq(start), ['iso3'] + OUTCOMES].set_index('iso3')
    lv1 = d.loc[d.year.eq(end), ['iso3'] + OUTCOMES].set_index('iso3')
    ch = (lv1 - lv0).reindex(names)
    obs = dict(median_schooling_gap=float(np.median(np.abs(ch[OUTCOMES[0]].to_numpy()[:, None] - ch[OUTCOMES[0]].to_numpy()[None, :])[np.triu_indices(len(names), 1)])),
               median_tfr_gap=float(np.median(np.abs(ch[OUTCOMES[1]].to_numpy()[:, None] - ch[OUTCOMES[1]].to_numpy()[None, :])[np.triu_indices(len(names), 1)])))
    obs['n_countries'] = len(names)
    draws = []
    for _ in range(n_draws):
        perm = rng.permutation(len(names))
        sch, tfr = [], []
        for k in range(len(perm) // 2):
            i, j = perm[2 * k], perm[2 * k + 1]
            sch.append(abs(ch.iloc[i][OUTCOMES[0]] - ch.iloc[j][OUTCOMES[0]]))
            tfr.append(abs(ch.iloc[i][OUTCOMES[1]] - ch.iloc[j][OUTCOMES[1]]))
        draws.append(dict(median_schooling_gap=float(np.median(sch)), median_tfr_gap=float(np.median(tfr))))
    rnd = pd.DataFrame(draws)
    return obs, draws, rnd

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--panel', required=True)
    ap.add_argument('--out', required=True)
    ap.add_argument('--agri', default='/root/work/data/emp_agri.json')
    ap.add_argument('--baseline', type=int, default=1980)
    ap.add_argument('--start', type=int, default=1990)
    ap.add_argument('--end', type=int, default=2010)
    a = ap.parse_args()
    outdir = Path(a.out); outdir.mkdir(parents=True, exist_ok=True)
    d = load_panel(a.panel)
    base = baseline_frame(d, a.baseline)
    names = list(base.index)
    print('baseline complete:', len(names))
    z, sd = zframe(base)
    zv = z.values
    cost = np.linalg.norm(zv[:, None, :] - zv[None, :, :], axis=-1)
    np.fill_diagonal(cost, np.inf)
    chosen = pairing_greedy(cost, names)
    df = pair_frame(chosen, d, a.start, a.end)
    df.to_csv(outdir / 'pairs_primary.csv', index=False)
    meta = dict(input_sha256=sha256(a.panel), n_baseline=len(names), n_pairs=len(df),
                unpaired=list(set(names) - set(df.country_a) - set(df.country_b)),
                n_pairs_both_school=float(df['mean_years_schooling_gap'].notna().sum()),
                n_pairs_both_tfr=float(df['tfr_observed_1950plus_gap'].notna().sum()))
    # coverage
    rows = []
    for col in FEATURES + ['effective_fertility', 'child_mortality_per100', 'life_expectancy_years']:
        if col in d.columns:
            at = d.loc[d.year.eq(a.baseline), col]
            rows.append(dict(feature=col, n_1980=int(at.notna().sum()), n_total_countries=int(d.iso3.nunique())))
    pd.DataFrame(rows).to_csv(outdir / 'audit_coverage_features.csv', index=False)
    # full-panel vs matched-sample baseline comparison (in full-panel SD)
    comp = []
    full1980 = d.loc[d.year.eq(a.baseline), ['iso3'] + FEATURES].copy()
    for col in FEATURES:
        voll = full1980[col].dropna()
        if col == 'gdp_pc_maddison_1990int':
            voll = np.log(voll[voll > 0]); sel = base[col]  # base already logged
        else:
            sel = base[col]
        comp.append(dict(feature=col, n_full=int(voll.notna().sum()), n_matched=int(sel.notna().sum()),
                         full_mean=float(voll.mean()), matched_mean=float(sel.mean()),
                         full_sd=float(voll.std(ddof=0)),
                         gap_in_full_sd=float((sel.mean() - voll.mean()) / voll.std(ddof=0))))
    pd.DataFrame(comp).to_csv(outdir / 'audit_selection.csv', index=False)
    # alternatives
    variants = alt_matchings(base, names, cost, cost)
    sens = []
    for label, pairs in variants.items():
        if label.startswith('_') or pairs is None:
            continue
        vdf = pair_frame(pairs, d, a.start, a.end)
        overlap = len(set(map(tuple, vdf[['country_a', 'country_b']].values)) &
                      set(map(tuple, df[['country_a', 'country_b']].values)))
        sens.append(dict(variant=label, n_pairs=len(vdf), overlap_pairs=overlap,
                         overlap_share=round(overlap / len(df), 3),
                         median_baseline_distance=float(vdf.baseline_distance.median()),
                         median_schooling_gap=float(vdf['mean_years_schooling_gap'].median()),
                         median_tfr_gap=float(vdf['tfr_observed_1950plus_gap'].median())))
    pd.DataFrame(sens).to_csv(outdir / 'audit_matching_sensitivity.csv', index=False)
    # random yardstick
    obs, draws, rnd = random_yardstick(d, base, 1000, 71201, a.start, a.end)
    yard = dict(seed=71201, n_draws=len(rnd), observed=obs,
                random_median_schooling_gap_median=float(rnd['median_schooling_gap'].median()),
                random_median_tfr_gap_median=float(rnd['median_tfr_gap'].median()),
                share_random_median_schooling_ge_observed=float((rnd['median_schooling_gap'] >= obs['median_schooling_gap']).mean()),
                share_random_median_tfr_ge_observed=float((rnd['median_tfr_gap'] >= obs['median_tfr_gap']).mean()),
                random_p2_5_schooling=float(rnd['median_schooling_gap'].quantile(.025)),
                random_p97_5_schooling=float(rnd['median_schooling_gap'].quantile(.975)))
    json.dump(yard, open(outdir / 'audit_random_yardstick.json', 'w'), indent=1)
    # standardised summed gap and case candidates
    for col in OUTCOMES:
        df[f'{col}_gap_sd'] = df[f'{col}_gap'] / df[f'{col}_gap'].std(ddof=0)
    df['summed_gap_sd'] = df['mean_years_schooling_gap_sd'] + df['tfr_observed_1950plus_gap_sd']
    df['close'] = df.baseline_distance <= df.baseline_distance.median()
    close = df[df.close].copy(); far = df[~df.close].copy()
    candidates = {}
    candidates['divergent_close'] = close.sort_values('summed_gap_sd', ascending=False).head(3).to_dict('records')
    candidates['convergent_close'] = close.sort_values('summed_gap_sd').head(3).to_dict('records')
    candidates['divergent_distant'] = far.sort_values('summed_gap_sd', ascending=False).head(3).to_dict('records')
    # triad: pair(div close) + nearest baseline neighbour of either member not already paired
    top = close.sort_values('summed_gap_sd', ascending=False).iloc[0]
    used = set(df.country_a) | set(df.country_b)
    cands = []
    for member in (top.country_a, top.country_b):
        dv = np.linalg.norm(zv[names.index(member)][None, :] - zv, axis=1)
        for k in np.argsort(dv):
            if names[k] not in used and names[k] != member:
                cands.append((float(dv[k]), member, names[k])); break
    if cands:
        d0, m0, nb = min(cands)
        trio = [top.country_a, top.country_b, nb]
        candidates['triad'] = dict(members=trio, anchor_pair=[top.country_a, top.country_b],
                                   nearest=[m0, nb], nearest_distance=d0,
                                   noted='triad formed only if the three members are checked together; baseline distances '
                                   'are to the anchor pair members, not a triad-optimal match')
    # half labels by baseline-distance rank (even = A, odd = B), same rule as pairs_with_halves
    halves = {}
    for i, row in df.sort_values('baseline_distance').reset_index(drop=True).iterrows():
        halves[(row.country_a, row.country_b)] = 'A' if i % 2 == 0 else 'B'
    for label, recs in candidates.items():
        if isinstance(recs, list):
            for rec in recs:
                rec['half'] = halves.get((rec['country_a'], rec['country_b']), halves.get((rec['country_b'], rec['country_a'])))
    # holdout halves by baseline-distance rank
    ordered = df.sort_values('baseline_distance').reset_index(drop=True)
    ordered['half'] = ['A' if i % 2 == 0 else 'B' for i in range(len(ordered))]
    ordered.to_csv(outdir / 'pairs_with_halves.csv', index=False)
    # farming employment (dated only, no backcasting)
    farm_note = 'not_loaded'
    farm_rows = []
    try:
        raw = json.load(open(a.agri))
        lut = {}
        for rec in raw:
            if isinstance(rec, list) and len(rec) == 3:
                iso, yr, v = rec
                try: lut[(iso, int(yr))] = float(v)
                except Exception: pass
        farm_note = f'loaded {len(lut)} country-year observations from {a.agri}'
        for rec in candidates['divergent_close'] + candidates['convergent_close'] + candidates['divergent_distant']:
            for side in ('a', 'b'):
                iso = rec[f'country_{side}']
                yrs = sorted(y for (i, y) in lut if i == iso and y >= 1990 and y <= 2010)
                v1990 = lut.get((iso, 1990)); v2010 = lut.get((iso, 2010))
                earliest = (yrs[0], lut[(iso, yrs[0])]) if yrs else (None, None)
                farm_rows.append(dict(country=iso, role=rec.get('summed_gap_sd'), v1990=v1990, v2010=v2010,
                                      first_dated_year=earliest[0], first_dated_value=earliest[1],
                                      change_1990_2010=(None if v1990 is None or v2010 is None else v2010 - v1990),
                                      change_earliest_2010=(None if earliest[0] is None or v2010 is None else v2010 - earliest[1]),
                                      years_used=(str(earliest[0]) + '-' + str(2010)) if earliest[0] and v2010 is not None else 'not dated'))
    except Exception as e:
        farm_note = f'not available: {e}'
    pd.DataFrame(farm_rows).to_csv(outdir / 'audit_farming_dated.csv', index=False)
    json.dump(candidates, open(outdir / 'case_candidates.json', 'w'), indent=1)
    summary = dict(meta=meta, coverage_rows=rows, selection=comp, sensitivity=sens, yardstick=yard,
                   farming=farm_note, candidates=candidates,
                   half_counts=ordered.half.value_counts().to_dict())
    json.dump(summary, open(outdir / 'audit_summary.json', 'w'), indent=1)
    print(json.dumps({k: summary[k] for k in ('meta', 'farming', 'half_counts')}, indent=1))
    print(sens)

if __name__ == '__main__':
    main()
