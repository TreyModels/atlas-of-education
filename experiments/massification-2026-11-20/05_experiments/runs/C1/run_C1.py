"""C1: recovery/identification study across three rival generators + one truth outside the model set.
Predeclared in PRE_DECLARATIONS_C.md."""
import argparse, json, os, sys, time
import numpy as np
sys.path.insert(0, os.environ.get('MASSRUN_EXP', '/tmp/massrun/work/exp'))
from common import write_rows, write_text
from massabm import make_params, run_model
from massabm.summary import cohort_series, year_series
from massabm.model import BASIC
import toy_generators as tg

MOM = tg.MOMENTS
F1 = [dict(mode=('full' if fl == 'adaptive' else ('no_floor' if fl == 'none' else 'full')),
           **({'floor_fixed': dict(elite=4, mid=4, routine=3)} if fl == 'fixed' else {}),
           cost_col=cc) for fl in ('none', 'adaptive', 'fixed') for cc in (0.4, 0.6, 0.8)]
F1_NAMES = [(fl, cc) for fl in ('none', 'adaptive', 'fixed') for cc in (0.4, 0.6, 0.8)]
F3 = [dict(mode='hc_fair_slots', fair_sigma=sg, hc_school=hs) for sg in (0.5, 1.0, 2.0) for hs in (0.03, 0.05, 0.07)]
F3_NAMES = [(sg, hs) for sg in (0.5, 1.0, 2.0) for hs in (0.03, 0.05, 0.07)]
YOO = [dict(t_star=t, beta=b) for t in (-0.5, 0.0, 0.5) for b in (0.15, 0.25, 0.35)]


def mass_moments(S):
    c = cohort_series(S); y = year_series(S)
    e = c['entry']; we = (e >= 1995) & (e <= 2012); wy = (y['year'] >= 2010) & (y['year'] <= 2030)
    form = S['pool_cat'][wy][:, [1, 2, 4], :].sum() / max(S['pool_cat'][wy].sum(), 1)
    tut0 = S['tut'][wy, :, 0].sum(); tut1 = S['tut'][wy, :, 1].sum()
    return dict(completion=float(np.nanmean(c['basic'][we])),
                tertiary=float(np.nanmean(c['degree'][we])),
                premium=float(np.nanmean(y['college_income'][wy]) / np.nanmean(y['basic_income'][wy])),
                formal_share=float(form),
                prep_takeup=float(tut1 / max(tut0, 1e-9)),
                gap_q5_q1=float(np.nanmean(c['basic_q'][we, 4]) - np.nanmean(c['basic_q'][we, 0])))


def run_mass(params, N, seed, reps=2):
    ms = []
    for r in range(reps):
        p = dict(params); p.update(seed=seed + r, N=N)
        ms.append(mass_moments(run_model(make_params(**p))))
    return {k: float(np.mean([m[k] for m in ms])) for k in MOM}


def toy_moments(fn, spec, seed):
    return fn(seed=seed, **spec)


def distort(m, rng, sigma=0.06):
    out = {}
    for k, v in m.items():
        if k == 'gap_q5_q1':
            out[k] = v + rng.normal(0, 0.02)
        else:
            out[k] = v * np.exp(rng.normal(0, sigma))
    return out


def dist(a, b):
    s = 0.0
    for k in MOM:
        scale = max(abs(b[k]), 0.15)
        s += ((a[k] - b[k]) / scale) ** 2
    return float(s)


_N = 2000


def _cand_one(arg):
    fam, i, ov, N = arg
    try:
        return fam, i, run_mass(ov, N, 33100)
    except Exception as e:
        return fam, i, {'error': repr(e)}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--N', type=int, default=2000)
    ap.add_argument('--out', required=True)
    a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    t0 = time.time()
    from concurrent.futures import ProcessPoolExecutor
    # ---- precompute candidate moment surfaces (2 seeds averaged)
    cand = {}
    seq = []
    for i, ov in enumerate(F1):
        seq.append(('surplus', i, dict(ov)))
    for i, ov in enumerate(F3):
        seq.append(('competitive', i, dict(ov)))
    with ProcessPoolExecutor(max_workers=2) as ex:
        for fam, i, m in ex.map(_cand_one, [(fam, i, ov, a.N) for fam, i, ov in seq]):
            cand.setdefault(fam, {})[i] = m
    for j, ov in enumerate(YOO):
        cand.setdefault('yoo', {})[j] = toy_moments(tg.yoo, ov, 33100)
    # ---- truths
    truths = {}
    truths['G1 surplus/floor'] = run_mass(dict(mode='full', cost_col=0.55), a.N, 33101)
    truths['G2 yoo cutoff'] = toy_moments(tg.yoo, dict(t_star=-0.1, beta=0.22), 33101)
    truths['G3 competitive CES'] = run_mass(dict(mode='hc_fair_slots', fair_sigma=1.0, hc_school=0.05), a.N, 33101)
    truths['G4 outside (random among eligible)'] = toy_moments(tg.random_eligible, dict(), 33101)
    # ---- pseudo-datasets (2 measurement-error draws each) and classification
    rows, conf = [], {t: {f: 0 for f in ('surplus', 'yoo', 'competitive')} for t in truths}
    for tname, tm in truths.items():
        for d in range(2):
            rng = np.random.default_rng(4100 + 17 * d + len(tname))
            dat = distort(tm, rng)
            best = {}
            for fam, grid in cand.items():
                bd, bi = np.inf, None
                for i, m in grid.items():
                    if 'error' in m:
                        continue
                    dd = dist(m, dat)
                    if dd < bd:
                        bd, bi = dd, i
                best[fam] = bd
            pick = min(best, key=best.get)
            conf[tname][pick] += 1
            rows.append(dict(truth=tname, draw=d, pick=pick,
                             d_surplus=best['surplus'], d_yoo=best['yoo'], d_competitive=best['competitive'],
                             margin=float(min(best.values()) and (sorted(best.values())[1] - sorted(best.values())[0])) if len(best) > 1 else np.nan))
    write_rows(os.path.join(a.out, 'c1_confusion.csv'), ['truth', 'draw', 'pick', 'd_surplus', 'd_yoo', 'd_competitive', 'margin'],
               [[r[k] for k in ['truth', 'draw', 'pick', 'd_surplus', 'd_yoo', 'd_competitive', 'margin']] for r in rows])
    # candidate grid moments for audit
    gr = []
    for fam, grid in cand.items():
        for i, m in grid.items():
            gr.append(dict(family=fam, point=i, **{k: m[k] for k in MOM}))
    write_rows(os.path.join(a.out, 'c1_candidate_moments.csv'), ['family', 'point'] + MOM,
               [[r[k] for k in ['family', 'point'] + MOM] for r in gr])
    write_rows(os.path.join(a.out, 'c1_truth_moments.csv'), ['truth'] + MOM,
               [[t] + [truths[t][k] for k in MOM] for t in truths])
    # ---- verdict
    inset = ['G1 surplus/floor', 'G2 yoo cutoff', 'G3 competitive CES']
    mapping = {'G1 surplus/floor': 'surplus', 'G2 yoo cutoff': 'yoo', 'G3 competitive CES': 'competitive'}
    correct = {t: conf[t][mapping[t]] for t in inset}
    rec = sum(1 for t in inset if correct[t] >= 1) / 3
    L = ['C1 RECOVERY / IDENTIFICATION STUDY (cross-cutting)', f'draws=2 measurement-error datasets per truth; wall={time.time() - t0:.0f}s',
         'Candidate families: surplus/floor (massabm full, 3x3 floor x college-cost), Yoo fixed cutoff (3x3 t* x beta),',
         'competitive CES (massabm hc_fair_slots, 3x3 sigma x hc_school). Fitted by minimum weighted distance on six',
         'moments: completion, tertiary share, degree premium, formal share, prep take-up, Q5-Q1 gap.', '',
         'TRUTH MOMENTS (noise-free):', '  ' + '  '.join(f'{k}={truths["G1 surplus/floor"][k]:.3f}' for k in MOM)]
    for t in truths:
        L.append(f'  {t:36s} ' + '  '.join(f'{k}={truths[t][k]:.3f}' for k in MOM))
    L += ['', 'CONFUSION MATRIX (rows = truth, cols = assigned family; 2 noise draws each):',
          f'  {"truth":36s} {"surplus":>8s} {"yoo":>6s} {"competitive":>12s}']
    for t in truths:
        L.append(f'  {t:36s} {conf[t]["surplus"]:8d} {conf[t]["yoo"]:6d} {conf[t]["competitive"]:12d}')
    L += ['', 'DISTANCES PER DRAW (lower = better fit):', f'  {"truth":36s} {"draw":>4s} {"d_surplus":>10s} {"d_yoo":>8s} {"d_comp":>8s} {"pick":>12s}']
    for r in rows:
        L.append(f'  {r["truth"]:36s} {r["draw"]:4d} {r["d_surplus"]:10.3f} {r["d_yoo"]:8.3f} {r["d_competitive"]:8.3f} {r["pick"]:>12s}')
    L += ['', 'PREDECLARED DECISION: a model must recover its own generator better than rivals in >=2 of 3 in-set cases.']
    for t in inset:
        L.append(f'  {t}: recovered {correct[t]}/2 draws -> {"PASS" if correct[t] >= 1 else "FAIL"}')
    L.append(f'  overall recovery share = {rec:.2f} (>=0.67 required) -> {"RECOVERY SUPPORTED" if rec >= 0.67 else "NO IDENTIFICATION on these moments"}')
    g4 = conf['G4 outside (random among eligible)']
    L += ['', 'TRUTH OUTSIDE THE MODEL SET (G4): assigned ' +
          ', '.join(f'{k} {v}/2' for k, v in g4.items()) +
          (' -> the candidates claim a confident identification of a generator that is NOT in their set:'
           ' FORCED IDENTIFICATION, reported as a failure mode.' if max(g4.values()) == 2 else
           ' -> no candidate absorbs it consistently; the miss is visible, which is the honest outcome.')]
    L += ['', 'CAVEAT: six aggregate moments, two noise draws per truth, small candidate grids. This is a pilot-strength',
          'recovery test: it can show that identification is weak, not that it would fail with richer data.']
    write_text(os.path.join(a.out, 'findings.txt'), '\n'.join(L) + '\n')
    json.dump(dict(eid='C1', N=a.N, wall=time.time() - t0, recovery_share=rec,
                   confusion={t: conf[t] for t in conf}), open(os.path.join(a.out, 'run_meta.json'), 'w'), indent=1)
    print('done', time.time() - t0)


if __name__ == '__main__':
    main()
