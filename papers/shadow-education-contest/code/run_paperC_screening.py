#!/usr/bin/env python3
"""Paper C SCREENING (frozen 36-cell spec; PREREGISTRATION FINAL; manifest frozen).

Cells: S=q0 {0.85,1.0,1.15} x L (G6->G9 contest share {0.25,0.45}; contest_r fixed by L: 1.2 for .25, 1.6 for .45)
       x supply {A: own_ban0/firm_ban0, B: own_ban .95/firm_ban0, C: own_ban0/firm_ban .9}
       x settings {P55: pay_ratio .55 monitoring .2 pay_gap; P12: pay_ratio 1.2 monitoring .5 pay_gap} = 36 cells.
8 screening seeds (0-7; EXPOSED/exploratory), N=600, canonical HK primary gates otherwise; engine pin 846c9e0.
Assertions: non-market cells (B, C) require withheld>1e-3 and own_share>0.1; A|P12 exempt; failed exposed cell = INVALID.
Outcomes: K-12/G12 participation+spend, own_share_financial proxy (own_share; contamination declared), own/firm grade
  quantities, q_pub, withheld, ptr, teacher_pay, pub_spend, priv_share, elite_share, track_share, L/L6/L9, elite-Q5.
  (completion_primary/upper DROPPED: all-NaN in pilot; not cited.)
Runner: one subprocess per cell, per-seed atomic checkpoints, resume-by-skip, loud failure.
LABEL: PAPER C SCREENING — pre-registered confirmatory screening (engine 846c9e0; frozen spec); not a Pilot.
"""
import argparse, hashlib, json, os, subprocess, sys, time, warnings

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
ENGINE = os.path.join(REPO, 'engine'); SPEC = os.path.join(REPO, 'docs', 'audit', 'canonical_spec.json')
LABEL = 'PAPER C SCREENING — pre-registered confirmatory screening (engine 846c9e0, frozen spec); seeds 0-7 EXPOSED/exploratory'
Q0S = [0.85, 1.0, 1.15]; LS = [0.25, 0.45]
SUPPLY = {'A': dict(own_ban=0.0, firm_ban=0.0), 'B': dict(own_ban=0.95, firm_ban=0.0), 'C': dict(own_ban=0.0, firm_ban=0.9)}
SETTINGS = {'P55': dict(pay_ratio=0.55, monitoring=0.2, withhold_mode='pay_gap'),
            'P12': dict(pay_ratio=1.2, monitoring=0.5, withhold_mode='pay_gap')}
NSEEDS = 8

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def params(q0, L, sup, setting, seed):
    p = json.loads(json.dumps(json.load(open(SPEC))['params']['HK']['primary']))
    p.update(N=600, seed=seed, q0=float(q0))
    p.update(SUPPLY[sup]); p.update(SETTINGS[setting])
    p['gates'] = json.loads(json.dumps(p['gates']))
    p['gates'][1] = dict(kind='contest', share=float(L), cut0=6.0, r=(1.2 if L == 0.25 else 1.6), alpha=0.5,
                         fail='track', spec=dict(id=f'G9-screened', label='gate under test'))
    return p

def run_seed(q0, L, sup, setting, seed):
    warnings.filterwarnings('ignore'); sys.path.insert(0, ENGINE)
    import numpy as np
    from eduengine.core import Engine
    from eduengine.modules.labour import QueueLabour
    from eduengine.modules.schools import PrivateSchools, PublicSchools
    from eduengine.modules.sdg4 import SDG4
    from eduengine.modules.tutoring import TutoringMarket
    p = params(q0, L, sup, setting, seed)
    E = Engine([PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()], **p); E.run()
    if E.unfired_events: raise RuntimeError(f'unfired events {E.unfired_events}')
    if setting == 'P55' and sup in ('A', 'C'):   # exposed arms only (B = own_ban .95 market-only; P12 = no withholding)
        if not (float(np.nanmean(E.R['withheld'])) > 1e-3 and float(np.nanmean(E.R['own_share'])) > 0.1):
            raise RuntimeError(f'NO-OP cell q0={q0} L={L} {sup}/{setting}: withheld/own_share too low')
    m = E.p['measure_from']; R = E.R
    def mn(k):
        v = np.asarray(R.get(k, []), float); return float(np.nanmean(v[m:])) if v.size else None
    X = E.ALL; sel = (X['cohort'] >= m) & (X['cohort'] <= E.p['T'] - 26)
    if not sel.any(): sel = X['cohort'] >= m
    q = np.asarray(X['q'])[sel]; el = np.asarray(X['elite'])[sel]
    row = {k: mn(k) for k in ('tut_k12_rate', 'tut_k12_spend', 'tut_g12_rate', 'own_share', 'firm_price', 'q_pub',
                              'withheld', 'ptr', 'teacher_pay', 'pub_spend', 'priv_share', 'elite_share', 'track_share',
                              'tut_rate', 'contest_e_mean')}
    row['elite_q5_share_pct'] = float(100.0 * np.mean(q[el] == 4)) if el.any() else None
    row['L_mean'] = float(np.nanmean(np.asarray(X['L'], float)[sel])) if 'L' in X else None
    row['L6_mean'] = float(np.nanmean(np.asarray(X['L6'], float)[sel])) if 'L6' in X else None
    row['L9_mean'] = float(np.nanmean(np.asarray(X['L9'], float)[sel])) if 'L9' in X else None
    row.update(q0=q0, L=L, supply=sup, settings=setting, seed=seed)
    return row

def run_cell(q0, L, sup, setting, seeds, out_dir):
    warnings.filterwarnings('ignore'); os.makedirs(out_dir, exist_ok=True)
    tag = f'S{q0:.2f}_L{L:.2f}_{sup}_{setting}'
    ck = os.path.join(out_dir, f'ckpt_{tag}.jsonl'); done = set()
    if os.path.exists(ck):
        for line in open(ck):
            try: done.add(int(json.loads(line)['seed']))
            except Exception: pass
    for sd in seeds:
        if sd in done: continue
        row = run_seed(q0, L, sup, setting, sd)
        with open(ck, 'a') as f:
            f.write(json.dumps(row) + '\n'); f.flush(); os.fsync(f.fileno())
    return tag

def driver(workers, out_dir, seeds):
    from concurrent.futures import ThreadPoolExecutor
    os.makedirs(out_dir, exist_ok=True)
    cells = [(q0, L, sup, st) for q0 in Q0S for L in LS for sup in SUPPLY for st in SETTINGS]
    t0 = time.time()
    def launch(c):
        q0, L, sup, st = c
        r = subprocess.run([sys.executable, os.path.abspath(__file__), 'cell', str(q0), str(L), sup, st,
                            f'{seeds[0]}-{seeds[-1]}', out_dir], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONPATH=ENGINE, OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', OMP_NUM_THREADS='1'))
        if r.returncode != 0: raise RuntimeError(f'cell {c} failed rc={r.returncode}: {r.stderr[-1500:]}')
        return c
    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(launch, cells))
    wall = time.time() - t0
    rows = []
    for c in cells:
        tag = f'S{c[0]:.2f}_L{c[1]:.2f}_{c[2]}_{c[3]}'
        rows.extend(json.loads(l) for l in open(os.path.join(out_dir, f'ckpt_{tag}.jsonl')))
    def stat(v):
        import numpy as np
        a = np.array([x for x in v if x is not None], float); n = len(a)
        if n == 0: return None
        mu = float(np.nanmean(a)); sd = float(np.nanstd(a, ddof=1)) if n > 1 else 0.0; se = sd / np.sqrt(max(n, 1))
        return dict(mean=mu, sd=sd, ci95_lo=mu - 1.96 * se, ci95_hi=mu + 1.96 * se, n=n)
    metrics = ['tut_k12_rate', 'tut_k12_spend', 'tut_g12_rate', 'own_share', 'firm_price', 'q_pub', 'withheld', 'ptr',
               'teacher_pay', 'pub_spend', 'priv_share', 'elite_share', 'track_share', 'tut_rate', 'contest_e_mean',
               'elite_q5_share_pct', 'L_mean', 'L6_mean', 'L9_mean']
    summary = {}
    for r in rows:
        key = f"S{r['q0']:.2f}|L{r['L']:.2f}|{r['supply']}|{r['settings']}"
        summary.setdefault(key, []).append(r)
    summary = {k: {m: stat([x[m] for x in rr]) for m in metrics if m in rr[0]} for k, rr in summary.items()}
    payload = dict(label=LABEL,
                   manifest=dict(status='PRE-REGISTERED SCREENING', generation='PAPER C', engine_commit='846c9e0',
                                 engine_core_sha256=sha(os.path.join(ENGINE, 'eduengine', 'core.py')),
                                 spec_sha256=sha(SPEC), runner_sha256=sha(os.path.abspath(__file__)),
                                 cells=len(cells), seeds=list(seeds), n_seeds=len(seeds), N=600, runs=len(rows),
                                 workers=workers, wall_seconds=round(wall, 2),
                                 assertions='non-market cells require withheld>1e-3 and own_share>0.1; A|P12 exempt; failed exposed cell = INVALID',
                                 dropped_fields='completion_primary/upper dropped (all-NaN in pilot; not cited)',
                                 contamination='own_share mixes contest-prep with firm tutoring; q0 scales public+private quality',
                                 prereg='docs/audit/PAPER_C_CONFIRMATORY_PREREG.md (FINAL)',
                                 launch_manifest='docs/audit/PAPER_C_LAUNCH_MANIFEST.json (FROZEN)'),
                   summary=summary)
    path = os.path.join(out_dir, 'paperC_screening_results.json'); json.dump(payload, open(path, 'w'), indent=2)
    print('wrote', path, 'sha', sha(path), 'runs', len(rows), 'wall', round(wall, 1)); return 0

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'cell':
        q0, L, sup, st, ss, out = sys.argv[2:8]
        seeds = list(range(int(ss.split('-')[0]), int(ss.split('-')[1]) + 1)) if '-' in ss else [int(ss)]
        run_cell(float(q0), float(L), sup, st, seeds, out); return 0
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=10)
    ap.add_argument('--seeds', default=f'0-{NSEEDS-1}'); ap.add_argument('--out-dir', default=os.path.join(REPO, 'results', 'paperC_screening'))
    a = ap.parse_args()
    seeds = list(range(int(a.seeds.split('-')[0]), int(a.seeds.split('-')[1]) + 1)) if '-' in a.seeds else [int(x) for x in a.seeds.split(',')]
    return driver(a.workers, a.out_dir, seeds)

if __name__ == '__main__':
    sys.exit(main())
