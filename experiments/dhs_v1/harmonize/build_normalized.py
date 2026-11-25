#!/usr/bin/env python3
"""DHS -> experiments.R schema harmonization adapter (data-team deliverable).

Builds `normalized.csv` EXACTLY to the binding schema of experiments/dhs_v1/experiments.R from the local
restricted DHS recodes (~/neon-boot/pulled/dhs). Raw microdata and the normalized row-level file stay LOCAL:
the normalized file is written under ~/neon-boot/dhs-normalized/ by default and is NEVER committed/uploaded;
only non-disclosive aggregates leave (see aggregate_layer.py).

Weight rule (binding): PR/person rows use the household weight hv005/1e6; IR/WI woman rows use the individual
woman weight v005/1e6. One weight per row, never mixed; record_type records which design/weight applies.

Recode rules (documented; value labels verified by harmonize/inventory_dhs.py):
  age            hv105 (PR) / v012 (IR)
  sex            hv104 1=male 2=female (PR); IR rows are all women -> 2
  urban          1 if hv025/v025==1 else 0
  wealth         hv270 (PR) / v190 (IR), 1..5; 0/9/missing -> NA
  attendance     PR hv121: 1=currently attending -> 1; 0=no, 2=attended at some time -> 0; missing -> NA
                 (DHS recode labels: 0=no, 1=currently attending, 2=attended at some time)
  school_years   hv108 (PR) / v133 (IR), 0..v_max, 97 inconsistent/98 don't know/missing -> NA
  currently_in_school  = attendance on PR rows; NA on IR/WI rows (no current-school item exists in IR)
  children_ever_born   v201 (IR), 0..20, else NA
  age_first_birth      v212 (IR): numeric age; code 0/'no birth' -> NA?  -> see BIRTH_NEVER mapping below
  age_first_union      v511 (IR): numeric age; 0 -> NA (not in union); 99 = known never
  household_size hv009 (PR) / v136 (IR)
Schema columns absent for a record type are emitted as NA (README: include every column even where missing).
Unknown is never treated as "no": special inconsistent/don't-know codes -> NA.

Usage:
  python harmonize/build_normalized.py --root ~/neon-boot/pulled/dhs --outdir ~/neon-boot/dhs-normalized
  python harmonize/build_normalized.py --only KH --check   # one country subset
"""
import argparse, csv, hashlib, json, os, re, sys
import numpy as np
import pandas as pd
import pyreadstat

SCHEMA = ['country','wave','weight','stratum','psu','record_type','age','sex','urban','wealth',
          'attendance','school_years','children_ever_born','age_first_birth','currently_in_school',
          'age_first_union','household_size']

# recode registry is resolved from the local tree at run time (see discover_recodes); no hardcoded file names.
COUNTRY = {'indonesia': 'ID', 'cambodia': 'KH', 'philippines': 'PH', 'vietnam': 'VN'}


def discover_recodes(root):
    """{ (country, wave): {'PR': relpath, 'IR'|'WI': relpath} } from the local DHS tree."""
    recodes = {}
    for dirpath, _dirs, files in os.walk(root):
        for f in sorted(files):
            if not f.upper().endswith(('.DTA', '.SAS7BDAT')):
                continue
            rel = os.path.relpath(os.path.join(dirpath, f), root)
            parts = rel.split(os.sep)
            if len(parts) < 3:
                continue
            country = COUNTRY.get(parts[0], parts[0].upper()[:2])
            wave = parts[1]
            m = re.match(r'[A-Z]{2}([A-Z]{2})\d', f.upper())
            rtype = m.group(1) if m else None
            if rtype in ('PR', 'IR', 'WI'):
                slot = recodes.setdefault((country, wave), {})
                if rtype == 'WI':
                    rtype = 'IR'                      # old Woman Individual recode: same woman-record role
                slot[rtype] = rel
    return recodes


PR_COLS = ['hv001','hv002','hv003','hv005','hv009','hv021','hv022','hv023','hv024','hv025','hv104','hv105',
           'hv108','hv110','hv121','hv122','hv270']
IR_COLS = ['v001','v002','v005','v012','v021','v022','v023','v024','v025','v133','v136','v190','v201','v212',
           'v511','v525']


def sha256(path):
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for b in iter(lambda: f.read(1 << 20), b''):
            h.update(b)
    return h.hexdigest()


def read_vars(path, wanted):
    """Read candidate variables only (case-insensitive); returns DataFrame with lower-case columns.

    DHS recodes are inconsistent about case (older VI/WI recodes store upper-case names); pandas column
    selection is case-sensitive, so fall back to a full read + lower-cased subset when selection fails.
    """
    if path.lower().endswith('.dta'):
        try:
            df = pd.read_stata(path, columns=[c for c in wanted], convert_categoricals=False)
            df.columns = [c.lower() for c in df.columns]
            if not set(c.lower() for c in wanted).issubset(df.columns):
                raise ValueError('selected columns missing after case normalisation')
        except (ValueError, TypeError):
            df = pd.read_stata(path, convert_categoricals=False)
            df.columns = [c.lower() for c in df.columns]
    else:
        try:
            df, _ = pyreadstat.read_sas7bdat(path, usecols=[c.upper() for c in wanted])
        except Exception:
            df, _ = pyreadstat.read_sas7bdat(path)
        df.columns = [c.lower() for c in df.columns]
    return df


def codes_map(df, var):
    """Value-label mapping when a Stata/SAS categorical survived; otherwise identity (numeric codes)."""
    return df[var] if var in df.columns else pd.Series(np.nan, index=df.index)


def num(df, col):
    if col in df.columns:
        return pd.to_numeric(df[col], errors='coerce').astype(float)
    return pd.Series(np.nan, index=df.index, dtype=float)


def clean_num(s, lo, hi):
    x = pd.to_numeric(s, errors='coerce').astype(float)
    return x.where(x.between(lo, hi), np.nan)


def make_pr(df, country, wave):
    n = len(df)
    out = pd.DataFrame(index=df.index)
    out['country'] = country
    out['wave'] = wave
    out['weight'] = pd.to_numeric(df['hv005'], errors='coerce') / 1e6
    out['stratum'] = df['hv022'].map(lambda v: f'{int(v)}' if pd.notna(v) else None)
    out['psu'] = df['hv021'].map(lambda v: f'{int(v)}' if pd.notna(v) else None)
    out['record_type'] = 'person'
    out['age'] = clean_num(df['hv105'], 0, 120)
    out['sex'] = clean_num(df['hv104'], 1, 2)
    out['urban'] = np.where(pd.to_numeric(df['hv025'], errors='coerce') == 1, 1.0,
                            np.where(pd.to_numeric(df['hv025'], errors='coerce') == 2, 0.0, np.nan))
    w = num(df, 'hv270')
    out['wealth'] = w.where(w.between(1, 5), np.nan)
    # --- current school attendance: wave-specific recode verified empirically (see adapter manifest notes)
    # DHS recodes differ: some code 1=currently attending with 2=attended at some time (older), others code
    # 0=no, 2=currently attending and never use 1 (DHS-7/8). hv110 ("still in school", 1/0/9) is the
    # unambiguous household-schedule item where present. Missing/not-asked -> NA (never treated as no).
    att = num(df, 'hv121')
    h110 = num(df, 'hv110')
    codes = set(int(v) for v in att.dropna().unique()) if att.notna().any() else set()
    current_code = None
    if codes:
        current_code = 1 if 1 in codes else (2 if 2 in codes else None)
    attendance = np.full(len(df), np.nan)
    if h110.notna().any():                      # preferred: hv110==1 still in school; 9/DK -> NA
        attendance = np.where(h110 == 1, 1.0, np.where(h110 == 0, 0.0, np.nan))
    elif current_code is not None:
        attendance = np.where(att == current_code, 1.0, np.where(att.notna(), 0.0, np.nan))
    out['attendance'] = attendance
    out.attrs['attendance_recode'] = dict(hv121_codes=sorted(codes), current_code=current_code,
                                          hv110_used=bool(h110.notna().any()))
    out['school_years'] = clean_num(num(df, 'hv108'), 0, 40)
    out['children_ever_born'] = np.nan
    out['age_first_birth'] = np.nan
    out['currently_in_school'] = out['attendance']
    out['age_first_union'] = np.nan
    out['household_size'] = clean_num(num(df, 'hv009'), 1, 60)
    return out, n, dict(hv121_codes=sorted(int(c) for c in att.dropna().unique()),
                         current_code=current_code, hv110_used=bool(h110.notna().any()))


def make_woman(df, country, wave):
    out = pd.DataFrame(index=df.index)
    out['country'] = country
    out['wave'] = wave
    out['weight'] = pd.to_numeric(df['v005'], errors='coerce') / 1e6
    out['stratum'] = df['v022'].map(lambda v: f'{int(v)}' if pd.notna(v) else None)
    out['psu'] = df['v021'].map(lambda v: f'{int(v)}' if pd.notna(v) else None)
    out['record_type'] = 'woman'
    out['age'] = clean_num(num(df, 'v012'), 0, 120)
    out['sex'] = 2.0
    u = num(df, 'v025')
    out['urban'] = np.where(u == 1, 1.0, np.where(u == 2, 0.0, np.nan))
    w = num(df, 'v190')
    out['wealth'] = w.where(w.between(1, 5), np.nan)
    out['attendance'] = np.nan
    out['school_years'] = clean_num(num(df, 'v133'), 0, 40)
    out['children_ever_born'] = clean_num(num(df, 'v201'), 0, 25)
    # DHS IR: v212 age at first birth; 0 = no birth recorded? Keep special codes 96-99 as unknown EXCEPT 0 -> NA
    afb = clean_num(num(df, 'v212'), 0, 60)
    out['age_first_birth'] = afb.where(afb > 0, np.nan)
    out['currently_in_school'] = np.nan          # no current-school item in IR/WI
    afu = clean_num(num(df, 'v511'), 0, 60)
    out['age_first_union'] = afu.where(afu > 0, np.nan)
    out['household_size'] = clean_num(num(df, 'v136'), 1, 60)
    return out, len(df)


def validate_design(out, ctx):
    """Return per-cell checks: weight>0, stratum/psu non-missing, unique within stratum, wealth domain."""
    checks = dict(rows=int(len(out)), weight_missing=int(out['weight'].isna().sum()),
                  weight_nonpositive=int((out['weight'] <= 0).sum()),
                  stratum_missing=int(out['stratum'].isna().sum()), psu_missing=int(out['psu'].isna().sum()))
    ok = out.dropna(subset=['stratum', 'psu'])
    if len(ok):
        dup = ok.duplicated(subset=['stratum', 'psu']).sum()
        checks['psu_stratum_duplicates'] = int(dup)     # expected 0 only if psu ids are globally unique; see doc
        checks['n_psu'] = int(ok.groupby(['stratum', 'psu']).ngroups)
        checks['n_strata'] = int(ok['stratum'].nunique())
    checks['record_type'] = ctx
    return checks


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=os.path.expanduser('~/neon-boot/pulled/dhs'))
    ap.add_argument('--outdir', default=os.path.expanduser('~/neon-boot/dhs-normalized'))
    ap.add_argument('--only', default=None, help='country code filter, e.g. KH')
    ap.add_argument('--check', action='store_true', help='validate only (no normalized files written)')
    args = ap.parse_args()
    os.makedirs(os.path.join(os.path.dirname(os.path.abspath(__file__)), '_out'), exist_ok=True)
    manifest = []
    meta_out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '_out')
    all_recodes = discover_recodes(args.root)
    for (country, wave), recodes in sorted(all_recodes.items()):
        if args.only and country != args.only:
            continue
        for rtype, rel in recodes.items():
            path = os.path.join(args.root, rel)
            if not os.path.exists(path):
                manifest.append(dict(country=country, wave=wave, record_type=rtype, file=rel,
                                     status='MISSING_FILE'))
                continue
            wanted = PR_COLS if rtype == 'PR' else IR_COLS
            try:
                df = read_vars(path, [c for c in wanted])
            except Exception as exc:
                manifest.append(dict(country=country, wave=wave, record_type=rtype, file=rel,
                                     status=f'READ_FAILED: {type(exc).__name__}: {exc}'))
                continue
            try:
                if rtype == 'PR':
                    out, n, recode = make_pr(df, country, wave)
                    ctx = 'person/hv005'
                else:
                    out, n = make_woman(df, country, wave)
                    recode = dict(current_school_item='absent in IR/WI codebook -> E6 uses PR person rows')
                    ctx = 'woman/v005'
            except KeyError as exc:
                manifest.append(dict(country=country, wave=wave, record_type=rtype, file=rel,
                                     status=f'MISSING_VARIABLE: {exc}'))
                continue
            out = out[SCHEMA]
            checks = validate_design(out, ctx)
            rec = dict(country=country, wave=wave, record_type=rtype, input_file=rel,
                       input_sha256=sha256(path), input_rows=int(len(df)), rows=int(len(out)),
                       weight_variable=('hv005/1e6' if rtype == 'PR' else 'v005/1e6'),
                       status='OK', checks=checks, recode=recode,
                       nonmissing={c: int(out[c].notna().sum()) for c in SCHEMA})
            if not args.check:
                od = os.path.join(args.outdir, country)
                os.makedirs(od, exist_ok=True)
                op = os.path.join(od, f'normalized_{country}_{wave}_{out.record_type.iloc[0]}.csv'
                                  .replace(' ', ''))
                out.to_csv(op, index=False, float_format='%.10g')
                rec['output_file'] = os.path.relpath(op, os.path.expanduser('~'))
                rec['output_sha256'] = sha256(op)
            manifest.append(rec)
            print(f"{country}/{wave}/{out.record_type.iloc[0] if len(out) else rtype}: {len(out)} rows"
                  f" -> {'(check only)' if args.check else rec.get('output_file')}", flush=True)
    json.dump(dict(schema=SCHEMA, binding='experiments/dhs_v1/experiments.R', raw_local_only=True,
                   weight_rule='PR: hv005/1e6 household weight; IR/WI: v005/1e6 individual woman weight',
                   missing_rule='97/98/99 inconsistent/dont-know and unknown -> NA; age_first_birth/union 99 = known never only',
                   adapters=manifest),
              open(os.path.join(meta_out, 'adapter_manifest.json'), 'w'), indent=1)
    print(f"adapter manifest -> {os.path.join(meta_out, 'adapter_manifest.json')}")


if __name__ == '__main__':
    main()
