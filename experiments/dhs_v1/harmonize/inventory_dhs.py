#!/usr/bin/env python3
"""DHS local raw-data inventory + availability verifier (data-team deliverable).

Reads ONLY metadata and the candidate schema variables from the local restricted DHS recodes under
~/neon-boot/pulled/dhs (raw microdata never committed/uploaded). Writes non-disclosive metadata:
  availability_matrix.csv  one row per (country, wave, recode, variable): present/coding/non-missing/n
  catalog.json             per file: path (relative), sha256, bytes, format, rows, recode, weight/strata/psu vars
  value_codes.json         observed value codes/labels for the recodes-critical variables (attendance, wealth,
                           education years, CEB, age-first-birth/union, current-school)
Usage: python harmonize/inventory_dhs.py [--root ~/neon-boot/pulled/dhs] [--outdir harmonize/_out]
"""
import argparse, hashlib, json, os, re, sys
from collections import OrderedDict

import numpy as np
import pyreadstat

SCHEMA = ['country','wave','weight','stratum','psu','record_type','age','sex','urban','wealth',
          'attendance','school_years','children_ever_born','age_first_birth','currently_in_school',
          'age_first_union','household_size']
PR_VARS = ['hv001','hv002','hv005','hv009','hv021','hv022','hv023','hv024','hv025','hv104','hv105',
           'hv108','hv110','hv121','hv122','hv270','hv271']
IR_VARS = ['v001','v002','v005','v012','v021','v022','v023','v024','v025','v133','v136','v149',
           'v190','v201','v212','v511','v525','v701','v702','v715','v716','v717','v731']
KEY_VARS = ['hv110','hv121','hv122','hv270','hv271','hv108','hv009','hv005','hv021','hv022','hv023','hv024','hv025',
            'hv104','hv105','v005','v021','v022','v023','v024','v025','v012','v133','v136','v190','v201',
            'v212','v511','v525','v716','v717','v731']
COUNTRY = {'indonesia':'ID','cambodia':'KH','philippines':'PH','vietnam':'VN'}


def sha256(path):
    h = hashlib.sha256()
    with open(path,'rb') as f:
        for b in iter(lambda: f.read(1<<20), b''):
            h.update(b)
    return h.hexdigest()


def recode_type(name):
    n = name.upper()
    for t in ('PR','IR','WI','HH','BR','KR','CR','MR','GE','MM'):
        if re.search(r'(^|[A-Z])'+t+r'\d', n) or n.startswith(t):
            return {'PR':'PR','IR':'IR','WI':'WI','HH':'HH','BR':'BR'}.get(t, t)
    m = re.search(r'([A-Z]{2})([A-Z]{2})\d', n)
    return m.group(2) if m else 'UNK'


def read_meta(path, cols):
    """Return (n_rows, columns, value_labels, column_labels) without loading the full file."""
    if path.lower().endswith('.dta'):
        _df, meta = pyreadstat.read_dta(path, metadataonly=True)
        return (meta.number_rows, [c.lower() for c in meta.column_names],
                meta.variable_value_labels, meta.column_names_to_labels)
    # SAS7BDAT: no metadata-only API; row_limit=0 returns metadata without the data rows
    try:
        _df, meta = pyreadstat.read_sas7bdat(path, row_limit=0)
    except Exception:
        _df, meta = pyreadstat.read_sas7bdat(path, row_limit=5)
    return (getattr(meta, 'number_rows', -1), [c.lower() for c in meta.column_names],
            getattr(meta, 'variable_value_labels', {}) or {}, getattr(meta, 'column_names_to_labels', {}) or {})


def count_nonmissing(path, cols):
    """Non-missing counts for available candidate columns (restricted data stay in memory only)."""
    cols = [c for c in cols]
    try:
        if path.lower().endswith('.dta'):
            import pandas as pd
            df = pd.read_stata(path, columns=cols, convert_categoricals=False)
        else:
            # SAS7BDAT column names are upper-case; pyreadstat matches case-sensitively
            df, _ = pyreadstat.read_sas7bdat(path, usecols=[c.upper() for c in cols])
            df.columns = [c.lower() for c in df.columns]
    except Exception as exc:
        return {}, f'read_failed: {type(exc).__name__}: {exc}'
    out = {}
    for c in df.columns:
        s = df[c]
        out[c.lower()] = dict(n=int(len(s)), nonmissing=int(s.notna().sum()),
                              distinct=int(s.dropna().nunique()),
                              obs_codes=[float(x) for x in sorted(s.dropna().unique())[:8]])
    return out, None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=os.path.expanduser('~/neon-boot/pulled/dhs'))
    ap.add_argument('--outdir', default=os.path.join(os.path.dirname(os.path.abspath(__file__)), '_out'))
    args = ap.parse_args()
    os.makedirs(args.outdir, exist_ok=True)
    rows, catalog = [], []
    codes = {}
    for dirpath, _dirs, files in os.walk(args.root):
        for f in sorted(files):
            if not f.upper().endswith(('.DTA', '.SAS7BDAT')):
                continue
            path = os.path.join(dirpath, f)
            rel = os.path.relpath(path, args.root)
            parts = rel.split(os.sep)
            country = COUNTRY.get(parts[0], parts[0].upper()[:2])
            wave = parts[1] if len(parts) > 1 else '?'
            rtype = recode_type(f)
            cand = PR_VARS if rtype == 'PR' else IR_VARS if rtype in ('IR', 'WI') else []
            try:
                nrows, columns, vlabels, clabels = read_meta(path, cand)
            except Exception as exc:
                catalog.append(dict(country=country, wave=wave, recode=rtype, file=rel,
                                    sha256=sha256(path), bytes=os.path.getsize(path),
                                    status=f'metadata_error: {type(exc).__name__}: {exc}'))
                continue
            cols_sub = [c for c in cand if c in columns]
            counts, err = count_nonmissing(path, cols_sub) if cand else ({}, None)
            catalog.append(dict(country=country, wave=wave, recode=rtype, file=rel,
                                sha256=sha256(path), bytes=os.path.getsize(path),
                                format='dta' if path.lower().endswith('.dta') else 'sas7bdat',
                                n_rows=int(nrows) if nrows is not None else None,
                                n_columns=len(columns), variables_checked=len(cols_sub), read_error=err))
            for c in cand:
                info = counts.get(c, {})
                vl = {str(k): str(v) for k, v in (vlabels.get(c, {}) or {}).items()}
                rows.append(dict(country=country, wave=wave, recode=rtype, file=rel, variable=c,
                                 present=int(c in columns),
                                 variable_label=(clabels.get(c) or '') if isinstance(clabels, dict) else '',
                                 nonmissing=info.get('nonmissing'), n=info.get('n'),
                                 distinct=info.get('distinct'),
                                 observed_codes=(';'.join(str(x) for x in info.get('obs_codes', [])) if info else ''),
                                 value_labels=(';'.join(f'{k}={v}' for k, v in list(vl.items())[:12]) if vl else '')))
            for c in KEY_VARS:
                if c in cols_sub and c in vlabels and vlabels[c]:
                    codes.setdefault(f'{country}/{wave}/{rtype}/{c}', {str(k): str(v) for k, v in vlabels[c].items()})
    # csv
    import csv
    fields = list(rows[0].keys()) if rows else ['country']
    with open(os.path.join(args.outdir, 'availability_matrix.csv'), 'w', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        for r in rows:
            w.writerow(r)
    json.dump(dict(root=os.path.expanduser(args.root),
                   generated_by='harmonize/inventory_dhs.py',
                   raw_microdata_local_only=True,
                   files=sorted(catalog, key=lambda x: (x['country'], x['wave'], x['file']))),
              open(os.path.join(args.outdir, 'catalog.json'), 'w'), indent=1)
    json.dump(codes, open(os.path.join(args.outdir, 'value_codes.json'), 'w'), indent=1)
    print(f'wrote {len(rows)} variable rows, {len(catalog)} files -> {args.outdir}')


if __name__ == '__main__':
    main()
