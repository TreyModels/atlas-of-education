#!/usr/bin/env python3
"""Country-wave / region-wave AGGREGATE layer from harmonized DHS rows (data-team deliverable).

Reads the LOCAL normalized.csv files produced by build_normalized.py (never the raw microdata directly),
reproduces the experiments.R domain specifications E1-E8 as design-based weighted means with Taylor-linearized
(stratified cluster) standard errors, and writes only NON-DISCLOSIVE aggregates:
  aggregate_layer.csv        experiment x country x wave x group: estimate/se/ci, n, design summary, suppression
  coverage_missingness.csv   eligible/complete/missingness/coverage and design feasibility per cell
  join_manifest.json         country(-year) join keys + macro-series link candidates with provenance/permissions
  benchmarks.csv             published-benchmark validation rows (see BENCHMARKS below) vs our estimates

Design: survey design is (stratum, psu, weight); PR person rows use hv005/1e6, IR/WI woman rows use v005/1e6
(never mixed). Domain mean variance: z_i = w_i(y_i-p)/sum(w); PSU totals within strata; var = sum_h n_h/(n_h-1)
* sum_c (z_c - mean_h)^2 (survey's with-replacement Taylor approximation). Suppression: n_complete>=50 and
>=2 PSUs and >=2 strata, otherwise estimate suppressed (n reported only).

RAW AND NORMALIZED MICRODATA STAY LOCAL; only these aggregates are written into the repo.
Usage: python harmonize/aggregate_layer.py --normalized ~/neon-boot/dhs-normalized --outdir harmonize/_out
"""
import argparse, glob, hashlib, json, os, re
import numpy as np
import pandas as pd

SPECS = {
 'E1': dict(record='person', ages=(14, 17), out='attendance', group='wealth'),
 'E2': dict(record='person', ages=(14, 17), out='attendance', group='urban'),
 'E3': dict(record='person', ages=(14, 17), out='attendance', group='sex'),
 'E4': dict(record='woman', ages=(40, 49), out='children_ever_born', group='education'),
 'E5': dict(record='woman', ages=(25, 34), out='early_birth', group='education'),
 # E6 as written in experiments.R wants record_type='woman' + currently_in_school.  The DHS IR/WI recodes have
 # NO current-school item (v716/v717/v731 are occupation/employment, verified in inventory_dhs.py), so E6 is run on
 # PR person rows restricted to women aged 20-24 (person weight) and flagged as a documented deviation.
 'E6': dict(record='person_sex2', ages=(20, 24), out='currently_in_school', group='urban'),
 'E7': dict(record='woman', ages=(25, 34), out='early_union', group='education'),
 'E8': dict(record='woman', ages=(40, 49), out='household_size', group='education'),
}
EDU_BINS = [(0, 5, '0-5'), (6, 11, '6-11'), (12, 99, '12+')]


def edu_recode(s):
    x = pd.to_numeric(s, errors='coerce')
    return np.where(x.isna(), None, np.where(x < 6, '0-5', np.where(x < 12, '6-11', '12+')))


def group_values(df, group, record):
    if group == 'education':
        df = df.copy(); df['education'] = edu_recode(df['school_years']); return df, 'education'
    return df, group


def add_outcomes(df):
    df = df.copy()
    df['early_birth'] = np.where(df['age_first_birth'].notna(), (df['age_first_birth'] < 20).astype(float), np.nan)
    df['early_union'] = np.where(df['age_first_union'].notna(), (df['age_first_union'] < 20).astype(float), np.nan)
    return df


def design_mean_se(d, ycol, group):
    """Design-based domain mean/SE matching survey::svymean on a subset design.

    survey computes domain variance with PSU totals over the FULL design (PSUs with no domain member have a zero
    total), so the stratum PSU counts n_h are the full-design counts, not the domain-only counts:
    z_i = w_i(y_i-p)/sum_domain(w); z_c = sum over the PSU's domain rows; var = sum_h n_h/(n_h-1) *
    sum_c (z_c - mean_{c in h} z_c)^2. This reproduces survey 4.5's Taylor linearization for nest=TRUE designs.
    """
    out = []
    universe = d[['stratum', 'psu']].drop_duplicates()
    counts_h = universe.groupby('stratum').size().to_dict()
    groups = [g for g in d[group].dropna().unique()] if len(d) else []
    for g in sorted(groups, key=lambda z: str(z)):
        s = d[(d[group] == g) & d[ycol].notna()]
        if len(s) == 0:
            continue
        w = s['weight'].to_numpy(float); y = s[ycol].to_numpy(float)
        sw = w.sum()
        if sw <= 0:
            continue
        p = float((w * y).sum() / sw)
        z = w * (y - p) / sw
        zdf = pd.DataFrame({'stratum': s['stratum'].astype(str).to_numpy(),
                            'psu': s['psu'].astype(str).to_numpy(), 'z': z})
        psu_tot = zdf.groupby(['stratum', 'psu'], dropna=False)['z'].sum().reset_index()
        uni = universe.copy()
        uni['stratum'] = uni['stratum'].astype(str); uni['psu'] = uni['psu'].astype(str)
        full = uni.merge(psu_tot, on=['stratum', 'psu'], how='left')
        full['z'] = full['z'].fillna(0.0)
        var = 0.0; n_h_valid = 0; n_lonely = 0
        for h, gg in full.groupby('stratum', dropna=False):
            n_h = len(gg)
            if n_h > 1:
                var += n_h / (n_h - 1) * float(((gg['z'] - gg['z'].mean()) ** 2).sum()); n_h_valid += 1
            else:
                n_lonely += 1
        se = float(np.sqrt(max(var, 0.0)))
        out.append(dict(group=str(g), estimate=p, se=se, n_complete=int(len(s)),
                        weight_sum=float(sw), n_psu=int(psu_tot.shape[0]),
                        n_strata=int(full['stratum'].nunique()), n_strata_df=int(n_h_valid),
                        n_lonely_strata=int(n_lonely),
                        n_psu_domain=int(s[['stratum', 'psu']].drop_duplicates().shape[0])))
    return out


def load_normalized(normalized):
    frames = []
    for p in sorted(glob.glob(os.path.join(normalized, '*', 'normalized_*.csv'))):
        df = pd.read_csv(p)
        df['wave'] = df['wave'].astype(str)
        if len(df) == 0:
            continue
        df['source_file'] = os.path.basename(p)
        frames.append(df)
    return pd.concat(frames, ignore_index=True) if frames else pd.DataFrame()


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def wave_year(wave):
    m = re.match(r'(\d{4})', str(wave))
    return int(m.group(1)) if m else None


BENCHMARKS = [
 # published values reused from the validated prior Cambodia extraction (wt3/dhs research/cambodia-dhs REPORT.md),
 # which cites the public DHS Cambodia 2021-22 Final Report FR377 Table 2.12 (nis.gov.kh PDF). Our measure is the
 # household-schedule CURRENT attendance, not the level-specific NAR, so the match is definitional (+/-tolerance).
 dict(id='B001', country='KH', wave='2021-22', indicator='primary NAR (age 6-11)',
      published=72.8, tolerance_pp=2.5, our_slice=dict(ages=(6, 11), group=None),
      definition_match='definitional: any-level current attendance vs attending-primary NAR',
      citation='DHS Cambodia 2021-22 Final Report FR377 Table 2.12 (public PDF, nis.gov.kh); prior validated extraction wt3/dhs research/cambodia-dhs/REPORT.md'),
 dict(id='B002', country='KH', wave='2021-22', indicator='primary NAR by sex (M/F)',
      published=(72.0, 73.5), tolerance_pp=2.5, our_slice=dict(ages=(6, 11), group='sex'),
      definition_match='definitional', citation='FR377 Table 2.12'),
 dict(id='B003', country='KH', wave='2021-22', indicator='secondary NAR (age 12-18)',
      published=42.0, tolerance_pp=3.0, our_slice=dict(ages=(12, 18), group=None),
      definition_match='NOT MATCHED: attending-secondary NAR vs any-level current attendance; report direction only',
      citation='FR377 Table 2.12'),
 dict(id='B004', country='KH', wave='2021-22', indicator='primary NAR urban / rural',
      published=(75.5, 71.3), tolerance_pp=3.0, our_slice=dict(ages=(6, 11), group='urban'),
      definition_match='definitional', citation='FR377 Table 2.12'),
 # PENDING rows explicitly not filled: no exact public final-report table value retrieved in this environment.
 # They stay PENDING rather than substituting prior-run numbers as published benchmarks.
 dict(id='B005', country='PH', wave='2022', indicator='adolescent attendance 14-17 by wealth', published=None,
      tolerance_pp=None, our_slice=dict(ages=(14, 17), group='wealth'), definition_match='PENDING',
      citation='PENDING: needs Philippines DHS 2022 Final Report FR381 attendance-by-wealth table (public, dhsprogram.com); no exact value retrieved here'),
 dict(id='B006', country='ID', wave='2017', indicator='adolescent attendance 14-17 by wealth', published=None,
      tolerance_pp=None, our_slice=dict(ages=(14, 17), group='wealth'), definition_match='PENDING',
      citation='PENDING: needs Indonesia DHS 2017 Final Report attendance table (public); no exact value retrieved here'),
 dict(id='B007', country='VN', wave='2005', indicator='attendance 14-17 / women outcomes', published=None,
      tolerance_pp=None, our_slice=dict(ages=(14, 17), group=None), definition_match='PENDING',
      citation='PENDING: VN 2005-AIS report tables have different indicator definitions; leave PENDING'),
 dict(id='B008', country='KH/ID/PH/VN', wave='all', indicator='E4-E8 women outcomes', published=None,
      tolerance_pp=None, our_slice=None, definition_match='PENDING',
      citation='PENDING: published CEB/age-at-first-birth/union tables use different age/education bands; only exact matches may be used'),
]


def our_benchmark_value(d, b):
    """Compute the matched descriptive slice for a benchmark from the normalized PR person rows."""
    if b['published'] is None or b['our_slice'] is None:
        return None
    sp = b['our_slice']
    dw = d[(d['country'] == b['country']) & (d['wave'].astype(str) == b['wave']) & (d['record_type'] == 'person')].copy()
    age = pd.to_numeric(dw['age'], errors='coerce')
    dw = dw[age.between(sp['ages'][0], sp['ages'][1])]
    if sp['group'] is None:
        dw = dw[dw['attendance'].notna()]
        return float(np.average(dw['attendance'], weights=dw['weight'])) if len(dw) else None
    g = sp['group']
    dw = dw[dw[g].notna() & dw['attendance'].notna()]
    out = {}
    for val, sub in dw.groupby(g):
        out[str(int(val)) if float(val).is_integer() else str(val)] = float(np.average(sub['attendance'], weights=sub['weight']))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--normalized', default=os.path.expanduser('~/neon-boot/dhs-normalized'))
    ap.add_argument('--outdir', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '_out'))
    ap.add_argument('--macro-root', default=os.path.expanduser('~/neon-boot/wt2/dhseco/research/records/2026-11-24-dhs-api-ecological/data'))
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    d = load_normalized(args.normalized)
    if d.empty:
        raise SystemExit(f'no normalized files under {args.normalized}; run build_normalized.py first')
    d = add_outcomes(d)
    rows, coverage = [], []
    for key, sp in SPECS.items():
        for (country, wave), dw in d.groupby(['country', 'wave']):
            rec = dw[dw['record_type'] == ('person' if sp['record'] in ('person', 'person_sex2') else 'woman')]
            if sp['record'] == 'person_sex2':
                rec = rec[pd.to_numeric(rec['sex'], errors='coerce') == 2]
            rec, gcol = group_values(rec, sp['group'], sp['record'])
            age = pd.to_numeric(rec['age'], errors='coerce')
            in_domain = age.between(sp['ages'][0], sp['ages'][1])
            rec = rec[in_domain].copy()
            if len(rec) == 0:
                coverage.append(dict(experiment=key, country=country, wave=wave, record_type=sp['record'],
                                     n_domain=0, n_complete=0, outcome_missing_pct=None, group_missing_pct=None,
                                     status='NO_ROWS'))
                continue
            out_missing = float(rec[sp['out']].isna().mean()) if sp['out'] in rec else 1.0
            grp_missing = float(rec[gcol].isna().mean()) if gcol in rec else 1.0
            complete = rec[rec[sp['out']].notna() & rec[gcol].notna()]
            status = 'OK'
            if out_missing >= 0.999:
                status = 'BLOCKED_OUTCOME_VARIABLE_MISSING'
            elif grp_missing >= 0.999:
                status = 'BLOCKED_GROUP_VARIABLE_MISSING'
            coverage.append(dict(experiment=key, country=country, wave=wave, record_type=sp['record'],
                                 n_domain=int(len(rec)), n_complete=int(len(complete)),
                                 outcome_missing_pct=round(100 * out_missing, 2),
                                 group_missing_pct=round(100 * grp_missing, 2),
                                 n_psu=int(complete['psu'].nunique()) if len(complete) else 0,
                                 n_strata=int(complete['stratum'].nunique()) if len(complete) else 0,
                                 weight_sum=float(complete['weight'].sum()) if len(complete) else 0.0,
                                 status=status))
            if status != 'OK':
                continue
            for r in design_mean_se(rec, sp['out'], gcol):
                suppressed = not (r['n_complete'] >= 50 and r['n_psu'] >= 2 and r['n_strata_df'] >= 2)
                rows.append(dict(experiment=key, country=country, wave=wave, record_type=sp['record'],
                                 outcome=sp['out'], group_var=gcol, group=r['group'],
                                 estimate=(None if suppressed else round(r['estimate'], 6)),
                                 se=(None if suppressed else round(r['se'], 6)),
                                 ci_lo=(None if suppressed else round(r['estimate'] - 1.96 * r['se'], 6)),
                                 ci_hi=(None if suppressed else round(r['estimate'] + 1.96 * r['se'], 6)),
                                 n_complete=r['n_complete'], n_domain=int(len(rec)),
                                 n_psu=r['n_psu_domain'], n_strata=r['n_strata'], n_strata_df=r['n_strata_df'],
                                 weight_sum=round(r['weight_sum'], 6), suppressed=int(suppressed),
                                 suppression_reason=('' if not suppressed else
                                                     'n<50 or <2 PSUs or <2 strata with >=2 PSUs'),
                                 srs_se=round(float(pd.Series(rec.loc[rec[gcol] == r['group'], sp['out']]).std()
                                                    / np.sqrt(max(1, r['n_complete']))), 6) if r['n_complete'] > 1 else None,
                                 source_files=';'.join(sorted(rec['source_file'].unique()))))
    agg = pd.DataFrame(rows); cov = pd.DataFrame(coverage)
    agg.to_csv(os.path.join(args.outdir, 'aggregate_layer.csv'), index=False)
    cov.to_csv(os.path.join(args.outdir, 'coverage_missingness.csv'), index=False)

    # --- benchmark table ------------------------------------------------------
    bench_rows = []
    for b in BENCHMARKS:
        ours = our_benchmark_value(d, b)
        bench_rows.append(dict(benchmark_id=b['id'], country=b['country'], wave=b['wave'], indicator=b['indicator'],
                               published=str(b['published']), our_estimate=str(ours),
                               tolerance_pp=b['tolerance_pp'], definition_match=b['definition_match'],
                               citation=b['citation'],
                               status=('PENDING' if b['published'] is None else 'AVAILABLE')))
    pd.DataFrame(bench_rows).to_csv(os.path.join(args.outdir, 'benchmarks.csv'), index=False)

    # --- join manifest (country-year keys; subnational explicitly blocked) ---
    years = sorted({(c, str(w), wave_year(w)) for c, w in d[['country', 'wave']].drop_duplicates().itertuples(index=False)},
                   key=lambda x: (x[0], x[1]))
    macro_files = sorted(glob.glob(os.path.join(args.macro_root, 'panel_edu2_*.csv')))
    macro_index = []
    for f in macro_files:
        try:
            m = pd.read_csv(f, usecols=['indicator', 'country', 'year', 'survey', 'value'])
        except Exception:
            continue
        for c in ['KH', 'ID', 'PH', 'VN']:
            sub = m[m['country'] == c]
            if len(sub):
                macro_index.append(dict(file=os.path.basename(f), indicator=sub['indicator'].iloc[0],
                                        country=c, years=sorted(int(y) for y in sub['year'].dropna().unique()),
                                        n_rows=int(len(sub)), provenance='public DHS API aggregate (M6)',
                                        permission='public aggregate; no restricted microdata'))
    manifest = dict(
        generated_by='harmonize/aggregate_layer.py',
        schema='experiments/dhs_v1/experiments.R',
        raw_microdata='local only (~/neon-boot/pulled/dhs); never committed/uploaded',
        normalized_microdata='local only (~/neon-boot/dhs-normalized); never committed/uploaded',
        country_year_keys=[dict(country=c, wave=w, year=y) for c, w, y in years],
        subnational='BLOCKED: DHS regions/clusters are survey-specific; cluster GPS displaced (DHS terms) and no '
                    'genuine compatible admin-unit join key exists in the harmonized schema. No subnational-year '
                    'link is claimed.',
        macro_link_candidates=macro_index,
        macro_spine_declared_not_local=[
            dict(id='M1', name='imputed lead-lag matrix', path='origin/research/imputed-matrix-2026-11-23@5e4602b',
                 status='DECLARED-NOT-LOCAL: committed result CSVs are the durable record; not fetched in this lane'),
            dict(id='M3', name='marriage-extended matrix', path='origin/research/matrix-marriage-2026-11-23@559a4e9',
                 status='DECLARED-NOT-LOCAL'),
        ],
        linkage_rules=dict(
            timing='link only same or earlier survey year; all cross-sectional links are descriptive, not causal',
            geography='country-year only; region-year BLOCKED',
            missingness='aggregate cells carry n_complete/n_domain and suppression flags; macro joins must carry the '
                        'DHS survey year and are ambiguous where wave spans two calendar years (e.g. 2021-22)',
            permissions='DHS microdata restricted (local only); DHS API panels are public aggregates; matrix M1/M3 '
                        'are committed country-year aggregates, placebos show 21.7% wrong-country significance (not causal)'),
    )
    json.dump(manifest, open(os.path.join(args.outdir, 'join_manifest.json'), 'w'), indent=1)
    print(f'wrote aggregate_layer.csv ({len(agg)} rows), coverage_missingness.csv ({len(cov)} rows), '
          f'benchmarks.csv ({len(bench_rows)}), join_manifest.json')


if __name__ == '__main__':
    main()
