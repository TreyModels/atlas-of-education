#!/usr/bin/env python3
"""QA checks on the real-data run outputs (non-disclosive aggregates only; restricted microdata stays local)."""
import json, sys, os, hashlib
import pandas as pd, numpy as np
base = sys.argv[1] if len(sys.argv) > 1 else 'qa/real_run'
data_path = sys.argv[2] if len(sys.argv) > 2 else os.path.expanduser('~/neon-boot/dhs8_local/normalized_all.csv')
out = {}
est = pd.read_csv(os.path.join(base, 'estimates.csv'), dtype={'wave': str})
stat = pd.read_csv(os.path.join(base, 'status.csv'), dtype={'wave': str})
miss = pd.read_csv(os.path.join(base, 'missingness.csv'), dtype={'wave': str})
man = json.load(open(os.path.join(base, 'manifest.json')))
out['n_estimates'] = int(len(est)); out['n_status'] = int(len(stat)); out['n_missing_rows'] = int(len(miss))
out['status_by_experiment'] = stat.groupby(['experiment', 'status']).size().to_dict() if len(stat) else {}
out['status_non_ok'] = stat[stat.status != 'ok'].groupby(['experiment', 'status']).size().to_dict() if len(stat) else {}
out['estimates_by_experiment'] = est.groupby('experiment').size().to_dict()
out['surveys_by_experiment'] = est.groupby('experiment')['country'].nunique().to_dict()
out['suppressed_by_experiment'] = est[est.suppressed == True].groupby('experiment').size().to_dict()
out['suppression_reasons'] = {}
for reason in ('n<30', 'RSE', 'fewer than 2 PSUs', 'design df', 'non-finite SE'):
    out['suppression_reasons'][reason] = int(est['flags'].astype(str).str.contains(reason, regex=False).sum())
# disclosure rule violations among PUBLISHED cells
pub = est[est.suppressed != True]
viol = dict(
    n_lt_30=int((pub.n_unweighted < 30).sum()),
    n_psu_lt_2=int((pub.n_psu_domain < 2).sum()),
    df_lt_1=int(((pub.design_df.fillna(-1)) < 1).sum()),
    nonfinite=int((~np.isfinite(pub.se)).sum()),
)
out['published_cells'] = int(len(pub)); out['disclosure_violations'] = viol
out['columns_present'] = [c for c in ['n_unweighted','n_weighted','n_psu_domain','n_strata_domain','design_df','rse','suppressed','flags','q_value_bh','externally_benchmarked','not_externally_benchmarked'] if c in est.columns]
out['multiplicity'] = dict(all_exploratory=bool(est.exploratory.all()) if 'exploratory' in est else False,
                           n_q_values=int(est.q_value_bh.notna().sum()) if 'q_value_bh' in est else 0)
out['benchmark'] = dict(manifest_status=man.get('benchmark_status'),
                        n_externally_benchmarked=int((est.externally_benchmarked == True).sum()) if 'externally_benchmarked' in est else None,
                        n_benchmark_pending=int((est.not_externally_benchmarked == True).sum()) if 'not_externally_benchmarked' in est else None)
out['e6_definition'] = man.get('e6_definition')
out['lonely_policy'] = man.get('lonely_psu_policy')
out['weight_provenance'] = man.get('weight_provenance')
out['adapter_metadata_recorded'] = bool(man.get('adapter_metadata') and man['adapter_metadata'] != 'NOT SUPPLIED')
# independent recomputation of unsuppressed weighted domain means from the normalized data
d = pd.read_csv(data_path, dtype={'wave': str})
SPECS = {'E1':('person',14,17,'attendance','wealth',None), 'E2':('person',14,17,'attendance','urban',None),
         'E3':('person',14,17,'attendance','sex',None), 'E4':('woman',40,49,'children_ever_born','education',None),
         'E5':('woman',25,34,'early_birth','education',None), 'E6':('person',20,24,'currently_in_school','urban',2),
         'E7':('woman',25,34,'early_union','education',None), 'E8':('woman',40,49,'household_size','education',None)}
maxdiff = 0.0; ncmp = 0; missing_domains = []
for _, row in pub.iterrows():
    sp = SPECS.get(row.experiment)
    if sp is None: continue
    rtype, lo, hi, outcol, group, sex = sp
    z = d[(d.country == row.country) & (d.wave.astype(str) == str(row.wave)) & (d.record_type == rtype)].copy()
    z = z[pd.to_numeric(z.age, errors='coerce').between(lo, hi)]
    if sex is not None: z = z[pd.to_numeric(z.sex, errors='coerce') == sex]
    afb = pd.to_numeric(z.age_first_birth, errors='coerce'); afb[(afb > 0) & (afb < 10) & (afb != 99)] = np.nan
    afu = pd.to_numeric(z.age_first_union, errors='coerce'); afu[(afu > 0) & (afu < 10) & (afu != 99)] = np.nan
    outc = (afb < 20).astype(float) if outcol == 'early_birth' else \
           (afu < 20).astype(float) if outcol == 'early_union' else pd.to_numeric(z[outcol], errors='coerce')
    grp = (pd.cut(pd.to_numeric(z.school_years, errors='coerce'), [-1, 5, 11, 200], labels=['0-5','6-11','12+'])
           .astype(object) if group == 'education' else pd.to_numeric(z[group], errors='coerce'))
    gs = pd.Series(grp, index=z.index)
    if group == 'education':
        gk = gs.astype(str)
    else:
        gk = gs.map(lambda v: (str(int(v)) if (pd.notna(v) and np.isfinite(float(v))) else 'nan'))
    ok = outc.notna() & gs.notna() & (gk == str(row.group))
    zz = z[ok]; yy = outc[ok]; ww = pd.to_numeric(zz.weight, errors='coerce')
    exp = float(np.sum(yy * ww) / np.sum(ww)) if len(zz) else np.nan
    if not np.isfinite(exp): missing_domains.append((row.experiment, str(row.country), str(row.wave), str(row.group))); continue
    maxdiff = max(maxdiff, abs(float(row.estimate) - exp)); ncmp += 1
out['independent_recompute'] = dict(n_compared=ncmp, max_abs_diff=maxdiff, unmatched=len(missing_domains))
# manifest input hash check
in_sha = man.get('input_sha256', '')
out['manifest_input_sha256'] = in_sha[:16]
out['manifest_has_hashes'] = bool(in_sha and man.get('estimates_sha256'))
def strkeys(o):
    if isinstance(o, dict): return {str(k): strkeys(v) for k, v in o.items()}
    if isinstance(o, list): return [strkeys(v) for v in o]
    return o
json.dump(strkeys(out), open(os.path.join(base, 'qa_summary.json'), 'w'), indent=1, default=str)
print(json.dumps(strkeys(out), indent=1, default=str)[:4500])

# --- diagnosis of tiny independent-recompute differences (top offenders, non-disclosive keys only)
