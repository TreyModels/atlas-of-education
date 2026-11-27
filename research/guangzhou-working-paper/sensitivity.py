"""Exploratory Spearman and partial rank correlations; not causal effects.
PRCC assumes monotone responses. All other 31 sampled inputs are controlled.
HS_TEACH_SD is tied to TEACH_SD, not a separately sampled dimension.
"""
import csv
import json
from pathlib import Path
import numpy as np

ROOT = Path(__file__).resolve().parent

def ranks(x):
    order = np.argsort(x, kind='stable')
    result = np.empty(len(x), float)
    values, starts, counts = np.unique(x[order], return_index=True, return_counts=True)
    for start, count in zip(starts, counts):
        result[order[start:start+count]] = start + (count-1)/2
    return result

def analyze():
    rows = list(csv.DictReader((ROOT/'draws.csv').open()))
    names = list(json.loads((ROOT/'ranges.json').read_text()))
    x = np.column_stack([ranks(np.array([float(r[k]) for r in rows])) for k in names])
    x = (x-x.mean(0))/x.std(0)
    results = []
    for outcome in ('T', 'Sstar', 'delta_T', 'delta_T_ban'):
        y = np.array([float(r['T'])-float(r['T_before' if outcome=='delta_T' else 'T_noban']) if outcome.startswith('delta_') else float(r[outcome]) for r in rows])
        y = ranks(y); y = (y-y.mean())/y.std()
        for j, name in enumerate(names):
            controls = np.column_stack([np.ones(len(x)), np.delete(x,j,axis=1)])
            rx = x[:,j]-controls@np.linalg.lstsq(controls,x[:,j],rcond=None)[0]
            ry = y-controls@np.linalg.lstsq(controls,y,rcond=None)[0]
            results.append(dict(outcome=outcome, parameter=name, spearman=float(x[:,j]@y/len(y)), prcc=float(np.corrcoef(rx,ry)[0,1]), n=len(y)))
    with (ROOT/'sensitivity.csv').open('w',newline='') as f:
        writer=csv.DictWriter(f,fieldnames=results[0]);writer.writeheader();writer.writerows(results)
    lines=['# Rank sensitivity diagnostics','', 'All 32 independently sampled inputs; 1,024 settings, one synthetic cohort per setting. PRCC controls the ranks of the other 31 inputs. Coefficients describe this assumed input distribution; they are neither causal effects nor variance shares. Nonmonotonicity, interactions and cohort noise can weaken or distort rankings. No inferential p-values are reported. TEACH_SD also controls HS_TEACH_SD.','']
    for outcome in ('T','Sstar','delta_T','delta_T_ban'):
        lines += ['## '+outcome,'','| Input | Spearman | PRCC |','|---|---:|---:|']
        for r in sorted([r for r in results if r['outcome']==outcome],key=lambda r:abs(r['prcc']),reverse=True):
            lines.append('| {} | {:+.3f} | {:+.3f} |'.format(r['parameter'],r['spearman'],r['prcc']))
        lines.append('')
    (ROOT/'SENSITIVITY.md').write_text('\n'.join(lines))
    for outcome in ('T','Sstar','delta_T','delta_T_ban'):
        print(outcome, sorted([r for r in results if r['outcome']==outcome],key=lambda r:abs(r['prcc']),reverse=True)[:5])

if __name__=='__main__': analyze()
