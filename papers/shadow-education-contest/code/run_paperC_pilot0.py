#!/usr/bin/env python3
"""Paper C PILOT-0 (REVISED, EXPLORATORY) — supply-form emergence with existing engine switches only.

Corrections applied (engine-core mapping): withholding in canonical HK/KR is already zero because pay_ratio=1.2, so
withholding regimes MUST set pay_ratio<1 (or withhold_mode='incentive') AND own_ban<1; firm_price is an OUTCOME (the
supply inputs are p_firm); S is q0 (public-quality proxy, caps at 1.25); L is NOT varied in Pilot-0 (canonical HK gate
list fixed; L goes to Pilot-1).

Design (96 runs): 3 supply regimes x 2 S proxies (q0 1.0/1.2) x 2 private-supply (p_firm 0.03 low / 0.08 high) x 8 seeds
  regimes: R1 'market_only'   : own_ban=0.95, pay_ratio=0.8, withhold_mode='pay_gap'
           R2 'own_open_gap'  : own_ban=0.0,  pay_ratio=0.8, withhold_mode='pay_gap'
           R3 'own_open_incentive': own_ban=0.0, pay_ratio=1.2, withhold_mode='incentive'
  base params = docs/audit/canonical_spec.json params.HK.primary (canonical HK gate list, unchanged); N=1500;
  T/measure_from from the spec; seed matched.
Outcomes per seed: tut_k12_rate, tut_k12_spend, tut_g12_rate, own_share, tut_own_by_grade, tut_firm_by_grade, q_pub,
withheld, ptr, teacher_pay, pub_spend, priv_share, elite_share, track_share, E.ALL['L'], ['L6'], ['L9'] means,
elite-Q5 share (computed), completion_primary/upper.
Contamination note: own_share/tut_firm_by_grade mix contest-prep with firm tutoring (engine has no clean own-vs-firm
spend split); recorded as-is with this note.
MANIFEST: EXPLORATORY / hypothesis-generating; NOT confirmatory; not a reproduction of any prior run.
"""
import argparse, hashlib, json, os, subprocess, sys, time, warnings

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
ENGINE = os.path.join(REPO, 'engine'); SPEC = os.path.join(REPO, 'docs', 'audit', 'canonical_spec.json')
LABEL = ('PAPER C PILOT-0 (REVISED) — EXPLORATORY / HYPOTHESIS-GENERATING (engine 846c9e0; existing switches only); '
         'NOT confirmatory, NOT a reproduction of any prior run')
REGIMES = [
    ('market_only', dict(own_ban=0.95, pay_ratio=0.8, withhold_mode='pay_gap')),
    ('own_open_gap', dict(own_ban=0.0, pay_ratio=0.8, withhold_mode='pay_gap')),
    ('own_open_incentive', dict(own_ban=0.0, pay_ratio=1.2, withhold_mode='incentive')),
]
Q0S = [1.0, 1.2]; PFIRMS = [0.03, 0.08]; NSEEDS = 8

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def params(regime, q0, p_firm, seed):
    spec = json.load(open(SPEC)); base = json.loads(json.dumps(spec['params']['HK']['primary']))
    p = dict(base); p['seed'] = seed; p['N'] = 1500
    for k, v in dict(REGIMES[[r[0] for r in REGIMES].index(regime)][1]).items(): p[k] = v
    p['q0'] = float(q0); p['p_firm'] = float(p_firm)
    return p

def run_seed(regime, q0, p_firm, seed):
    warnings.filterwarnings('ignore'); sys.path.insert(0, ENGINE)
    import numpy as np
    from eduengine.core import Engine
    from eduengine.modules.labour import QueueLabour
    from eduengine.modules.schools import PrivateSchools, PublicSchools
    from eduengine.modules.sdg4 import SDG4
    from eduengine.modules.tutoring import TutoringMarket
    E = Engine([PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()],
               **params(regime, q0, p_firm, seed)); E.run()
    if getattr(E, 'unfired_events', []): raise RuntimeError(f'unfired events {E.unfired_events}')
    m = E.p['measure_from']; R = E.R
    def mn(k):
        v = np.asarray(R.get(k, []), float); return float(np.nanmean(v[m:])) if v.size else float('nan')
    X = E.ALL; sel = (X['cohort'] >= m) & (X['cohort'] <= E.p['T'] - 26)
    if not sel.any(): sel = X['cohort'] >= m
    q = np.asarray(X['q'])[sel]; el = np.asarray(X['elite'])[sel]
    d = {k: mn(k) for k in ('tut_k12_rate', 'tut_k12_spend', 'tut_g12_rate', 'own_share', 'firm_price', 'q_pub',
                            'withheld', 'ptr', 'teacher_pay', 'pub_spend', 'priv_share', 'elite_share', 'track_share',
                            'completion_primary', 'completion_upper', 'contest_e_mean', 'tut_rate')}
    d['elite_q5_share_pct'] = float(100.0 * np.mean(q[el] == 4)) if el.any() else float('nan')
    d['tut_own_by_grade_last'] = float(np.mean(np.asarray(R.get('tut_own_by_grade', [[np.nan]]), float)[m:], 0)[-1]) if 'tut_own_by_grade' in R else float('nan')
    d['tut_firm_by_grade_last'] = float(np.mean(np.asarray(R.get('tut_firm_by_grade', [[np.nan]]), float)[m:], 0)[-1]) if 'tut_firm_by_grade' in R else float('nan')
    d['L_mean'] = float(np.nanmean(np.asarray(X['L'], float)[sel])) if 'L' in X else float('nan')
    d['L6_mean'] = float(np.nanmean(np.asarray(X['L6'], float)[sel])) if 'L6' in X else float('nan')
    d['L9_mean'] = float(np.nanmean(np.asarray(X['L9'], float)[sel])) if 'L9' in X else float('nan')
    d['cohorts'] = int(sel.sum())
    return d

def np_mean(v):
    return sum(v) / max(len(v), 1)

def run_cell(regime, q0, p_firm, seeds, out_dir):
    warnings.filterwarnings('ignore'); os.makedirs(out_dir, exist_ok=True)
    tag = f'{regime}_q{q0:.2f}_pf{p_firm:.3f}'
    ck = os.path.join(out_dir, f'ckpt_{tag}.jsonl'); done = set()
    if os.path.exists(ck):
        for line in open(ck):
            try: done.add(int(json.loads(line)['seed']))
            except Exception: pass
    rows_this = []
    for sd in seeds:
        if sd in done: continue
        row = run_seed(regime, q0, p_firm, sd)
        row.update(regime=regime, q0=q0, p_firm=p_firm, seed=sd)
        rows_this.append(row)
        with open(ck, 'a') as f:
            f.write(json.dumps(row) + '\n'); f.flush(); os.fsync(f.fileno())
    # binding assertion (Lead sanity check): non-market regimes MUST show withholding AND own-teacher tutoring
    all_rows = rows_this + [json.loads(l) for l in open(ck)]
    if regime != 'market_only':
        h = float(np_mean([r['withheld'] for r in all_rows]))
        os_ = float(np_mean([r['own_share'] for r in all_rows]))
        if h <= 1e-6 or os_ <= 1e-6:
            raise RuntimeError(f'NO-OP regime {tag}: withheld={h} own_share={os_} — withholding mechanism did not bind')
    return tag

def driver(workers, out_dir, seeds):
    from concurrent.futures import ThreadPoolExecutor
    os.makedirs(out_dir, exist_ok=True)
    cells = [(r[0], q0, pf) for r in REGIMES for q0 in Q0S for pf in PFIRMS]
    t0 = time.time()
    def launch(c):
        r = subprocess.run([sys.executable, os.path.abspath(__file__), 'cell', c[0], str(c[1]), str(c[2]),
                            f'{seeds[0]}-{seeds[-1]}', out_dir], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONPATH=ENGINE, OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', OMP_NUM_THREADS='1'))
        if r.returncode != 0: raise RuntimeError(f'cell {c} failed rc={r.returncode}: {r.stderr[-1500:]}')
        return c
    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(launch, cells))
    wall = time.time() - t0
    rows = []
    for c in cells:
        tag = f'{c[0]}_q{float(c[1]):.2f}_pf{float(c[2]):.3f}'
        p = os.path.join(out_dir, f'ckpt_{tag}.jsonl')
        if os.path.exists(p): rows.extend(json.loads(l) for l in open(p))
    def stat(v):
        import numpy as np
        a = np.array(v, float); n = len(a); mu = float(np.nanmean(a)); sd = float(np.nanstd(a, ddof=1)) if n > 1 else 0.0
        se = sd / np.sqrt(max(n, 1))
        return dict(mean=mu, sd=sd, ci95_lo=mu - 1.96 * se, ci95_hi=mu + 1.96 * se, n=n)
    metrics = ['tut_k12_rate', 'tut_k12_spend', 'tut_g12_rate', 'own_share', 'firm_price', 'q_pub', 'withheld', 'ptr',
               'teacher_pay', 'pub_spend', 'priv_share', 'elite_share', 'track_share', 'completion_primary',
               'completion_upper', 'contest_e_mean', 'tut_rate', 'elite_q5_share_pct', 'tut_own_by_grade_last',
               'tut_firm_by_grade_last', 'L_mean', 'L6_mean', 'L9_mean']
    summary = {}
    for r in rows:
        key = f"{r['regime']}|q0={r['q0']}|p_firm={r['p_firm']}"
        summary.setdefault(key, []).append(r)
    summary = {k: {m: stat([r[m] for r in rr]) for m in metrics if m in rr[0]} for k, rr in summary.items()}
    payload = dict(label=LABEL,
                   manifest=dict(status='EXPLORATORY', generation='PAPER C PILOT-0 REVISED', engine_commit='846c9e0',
                                 engine_core_sha256=sha(os.path.join(ENGINE, 'eduengine', 'core.py')),
                                 spec_sha256=sha(SPEC), runner_sha256=sha(os.path.abspath(__file__)),
                                 base='params.HK.primary (canonical HK gate list fixed); N=1500',
                                 regimes={r[0]: r[1] for r in REGIMES}, q0_proxy=Q0S, p_firm=PFIRMS,
                                 seeds=list(seeds), n_seeds=len(seeds), cells=len(cells), runs=len(rows),
                                 workers=workers, wall_seconds=round(wall, 2),
                                 withholding_note='pay_ratio<1 or incentive mode required to make h>0; regimes set explicitly',
                                 contamination_note='own_share/tut_firm_by_grade mix contest-prep with firm tutoring; no clean own-vs-firm spend split — recorded as-is',
                                 note='EXPLORATORY / hypothesis-generating; no confirmatory claim; L varied in Pilot-1'),
                   summary=summary)
    path = os.path.join(out_dir, 'paperC_pilot0_results.json'); json.dump(payload, open(path, 'w'), indent=2)
    print('wrote', path, 'sha', sha(path), 'runs', len(rows), 'wall', round(wall, 1)); return 0

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'cell':
        r, q0, pf, ss, out = sys.argv[2:7]
        seeds = list(range(int(ss.split('-')[0]), int(ss.split('-')[1]) + 1)) if '-' in ss else [int(ss)]
        run_cell(r, float(q0), float(pf), seeds, out); return 0
    ap = argparse.ArgumentParser(); ap.add_argument('--workers', type=int, default=2)
    ap.add_argument('--seeds', default=f'0-{NSEEDS-1}')
    ap.add_argument('--out-dir', default=os.path.join(REPO, 'results', 'paperC_pilot0'))
    a = ap.parse_args()
    seeds = list(range(int(a.seeds.split('-')[0]), int(a.seeds.split('-')[1]) + 1)) if '-' in a.seeds else [int(x) for x in a.seeds.split(',')]
    return driver(a.workers, a.out_dir, seeds)

if __name__ == '__main__':
    sys.exit(main())
