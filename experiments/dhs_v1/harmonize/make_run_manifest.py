#!/usr/bin/env python3
"""Pinning artifacts for the DHS execution harness (data-team follow-up; no new analysis).

Writes, from the LOCAL normalized files and the committed availability matrix only:
  _out/singleton_ledger.csv           full 28-file strata scan: file,country,wave,record_type,stratum,n_psu,n_rows
  _out/run_map.csv                    file -> country/wave/record_type -> candidate & feasible experiments
  _out/normalized_output_hashes.csv   local normalized files: path, sha256, bytes, rows (pin for the run manifest)
Raw/normalized microdata stay local; these files contain only design/file metadata and hashes.
"""
import glob, hashlib, os
import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, '_out')
NORM = os.path.expanduser('~/neon-boot/dhs-normalized')
EXPS = ['E1','E2','E3','E4','E5','E6','E7','E8']


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def main():
    files = sorted(glob.glob(os.path.join(NORM, '*', 'normalized_*.csv')))
    avail = pd.read_csv(os.path.join(OUT, 'availability_E1_E8.csv'))
    avail['wave'] = avail['wave'].astype(str)
    led, runs, hashes = [], [], []
    for path in files:
        fn = os.path.basename(path)
        d = pd.read_csv(path, usecols=['country', 'wave', 'record_type'] + ['stratum', 'psu', 'weight'])
        country, wave = str(d['country'].iloc[0]), str(d['wave'].iloc[0])
        rtype = str(d['record_type'].iloc[0])
        # --- full strata scan (every stratum, so QA can reconcile per-file counts)
        g = d.groupby('stratum', dropna=False).agg(n_psu=('psu', 'nunique'), n_rows=('weight', 'size')).reset_index()
        for _, r in g.iterrows():
            led.append(dict(file=fn, country=country, wave=wave, record_type=rtype,
                            stratum=str(r['stratum']), n_psu=int(r['n_psu']), n_rows=int(r['n_rows']),
                            singleton_psu=int(int(r['n_psu']) == 1)))
        # --- run map: record-type candidates + feasibility from the verified matrix
        candidate = ['E1', 'E2', 'E3', 'E6'] if rtype == 'person' else ['E4', 'E5', 'E7', 'E8']
        row = avail[(avail.country == country) & (avail.wave == wave)]
        feas = []
        if len(row):
            for e in candidate:
                v = str(row.iloc[0][e])
                if v.startswith('FEASIBLE'):
                    feas.append(e)
        runs.append(dict(file=fn, country=country, wave=wave, record_type=rtype,
                         experiments_candidate=';'.join(candidate), experiments_feasible=';'.join(feas)))
        hashes.append(dict(file=fn, path='~/neon-boot/dhs-normalized/' + os.path.relpath(path, NORM),
                           sha256=sha256(path), bytes=os.path.getsize(path), rows=int(len(d))))
    pd.DataFrame(led).to_csv(os.path.join(OUT, 'singleton_ledger.csv'), index=False)
    pd.DataFrame(runs).to_csv(os.path.join(OUT, 'run_map.csv'), index=False)
    pd.DataFrame(hashes).to_csv(os.path.join(OUT, 'normalized_output_hashes.csv'), index=False)
    n_single = int(pd.DataFrame(led)['singleton_psu'].sum())
    print(f"files={len(files)} strata_rows={len(led)} singleton_strata={n_single} "
          f"run_map_rows={len(runs)} hashes={len(hashes)}")
    print(pd.DataFrame(led)[pd.DataFrame(led)['singleton_psu'] == 1].groupby('file').size().to_string())


if __name__ == '__main__':
    main()
