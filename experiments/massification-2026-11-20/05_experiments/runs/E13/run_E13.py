"""E13: graduate-supply shock with a matched competitive-labor-market benchmark (reproduction-quality check).
Reuses the October design (experiments8.grad_supply) but writes raw + paired changes itself."""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.environ.get('MASSRUN_EXP', '/tmp/massrun/work/exp'))
from common import run_many, write_rows, write_text, m_sd
from massabm import make_params
from massabm.experiments8 import BASE, SHOCKS, WORLDS, _outcomes

KEYS = ['degree_share', 'd_degree_share', 'diploma_income', 'd_diploma_income', 'degree_income',
        'd_degree_income', 'ratio_dip_to_deg', 'd_ratio', 'formal_rate_diploma', 'd_formal_rate_diploma']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--reps', type=int, default=3)
    ap.add_argument('--N', type=int, default=5000)
    ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    jobs = [((w, sh, r), 'massabm', make_params(seed=20000 + r, N=a.N, tuition_path=tp,
                                                macro_elasticity=0.0, **BASE, **wo))
            for w, wo in WORLDS.items() for sh, tp in SHOCKS.items() for r in range(a.reps)]
    print(f'E13: {len(jobs)} runs reps={a.reps} N={a.N}', flush=True)
    res, elapsed = run_many(jobs, a.workers)
    wall = time.time() - t0
    bad = [t for t, o in res.items() if isinstance(o, dict) and 'error' in o]
    rows = []
    for w in WORLDS:
        for r in range(a.reps):
            if (w, 'no shock', r) not in res or isinstance(res[(w, 'no shock', r)], dict) and 'error' in res[(w, 'no shock', r)]:
                continue
            B = _outcomes(res[(w, 'no shock', r)])
            for sh in SHOCKS:
                k = (w, sh, r)
                o = res.get(k)
                if o is None or (isinstance(o, dict) and 'error' in o):
                    continue
                A = _outcomes(o)
                rows.append(dict(world=w, shock=sh, rep=r,
                                 degree_share=A['degree_share'], d_degree_share=A['degree_share'] - B['degree_share'],
                                 diploma_income=A['basic_income'], d_diploma_income=A['basic_income'] - B['basic_income'],
                                 degree_income=A['degree_income'], d_degree_income=A['degree_income'] - B['degree_income'],
                                 ratio_dip_to_deg=A['basic_income'] / A['degree_income'],
                                 d_ratio=A['basic_income'] / A['degree_income'] - B['basic_income'] / B['degree_income'],
                                 formal_rate_diploma=A['formal_rate_diploma'],
                                 d_formal_rate_diploma=A['formal_rate_diploma'] - B['formal_rate_diploma']))
    write_rows(os.path.join(a.out, 'e13_raw.csv'), list(rows[0].keys()), [[r.get(k) for k in rows[0]] for r in rows])
    summ = []
    for w in WORLDS:
        for sh in SHOCKS:
            R = [r for r in rows if r['world'] == w and r['shock'] == sh]
            if not R:
                summ.append(dict(world=w, shock=sh, n_ok=0)); continue
            row = dict(world=w, shock=sh, n_ok=len(R))
            for k in KEYS:
                row[k], row[k + '_sd'] = m_sd([r[k] for r in R])
            summ.append(row)
    hdr = ['world', 'shock', 'n_ok'] + [x for k in KEYS for x in (k, k + '_sd')]
    write_rows(os.path.join(a.out, 'e13_summary.csv'), hdr, [[r.get(k) for k in hdr] for r in summ])
    L = ['E13 GRADUATE-SUPPLY SHOCK, matched competitive benchmark',
         f'reps={a.reps} N={a.N} wall={wall:.0f}s ok={len(rows)}/{len(jobs)} failed={len(bad)}',
         'No K-12 reform; 1995 tuition shock; labour market 2010-30; paired seeds 20000+r.', '',
         f'  {"world":40s} {"shock":30s} {"d degree":>9s} {"d diploma inc":>15s} {"d degree inc":>13s} {"d dip/deg":>10s} {"d formal|dip":>13s}']
    for r in summ:
        if not r.get('n_ok'):
            L.append(f'  {r["world"]:40s} {r["shock"]:30s} FAILED'); continue
        L.append(f'  {r["world"]:40s} {r["shock"]:30s} {r["d_degree_share"]:+9.3f} '
                 f'{r["d_diploma_income"]:+11.3f}({r["d_diploma_income_sd"]:.3f}) {r["d_degree_income"]:+13.3f} '
                 f'{r["d_ratio"]:+10.3f} {r["d_formal_rate_diploma"]:+9.3f}({r["d_formal_rate_diploma_sd"]:.3f})')
    def G(w, sh, k):
        for r in summ:
            if r['world'] == w and r['shock'] == sh:
                return r.get(k), r.get(k + '_sd', np.nan)
        return np.nan, np.nan
    sw = 'surplus model (slots, floors, ranking)'; cw = 'competitive skill market (CES wages)'
    L += ['', 'PREDECLARED DISCRIMINATION (college half price from 1995):']
    for w in [sw, cw]:
        di, sdi = G(w, 'college half price from 1995', 'd_diploma_income')
        fr, sfr = G(w, 'college half price from 1995', 'd_formal_rate_diploma')
        dr, _ = G(w, 'college half price from 1995', 'd_ratio')
        L.append(f'  {w:40s} Δdiploma income={di:+.4f} (±{sdi:.4f})  Δformal|dip={fr:+.4f} (±{sfr:.4f})  Δratio={dr:+.4f}')
    di_s, _ = G(sw, 'college half price from 1995', 'd_diploma_income')
    di_c, _ = G(cw, 'college half price from 1995', 'd_diploma_income')
    L.append(f'  surplus predicts diploma losers (Δ<0), competitive predicts diploma gainers (Δ>0): observed sign pattern '
             f'{"CONSISTENT" if di_s < 0 < di_c else "NOT CONSISTENT"} -> '
             f'{"SUPPORTS" if di_s < 0 < di_c else "CHALLENGES"} the surplus account'
             f' ({"ratio also usable in both" if True else ""})')
    write_text(os.path.join(a.out, 'findings.txt'), '\n'.join(L) + '\n')
    json.dump(dict(eid='E13', reps=a.reps, N=a.N, wall=wall, runs=len(jobs), ok=len(rows), failed=bad,
                   mean_run=float(np.mean(list(elapsed.values())))), open(os.path.join(a.out, 'run_meta.json'), 'w'), indent=1)
    print(f'wall={wall:.0f}s ok={len(rows)}/{len(jobs)}')


if __name__ == '__main__':
    main()
