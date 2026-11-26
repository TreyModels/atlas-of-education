#!/usr/bin/env python3
"""Paper C A6 runner (HOST-ONLY; committed BEFORE launch; no run authorized).

Design (A6 prereg, HEAD): 36 cells = S=q0 {0.85,1.0,1.15} x L {0.25,0.45} x supply {A,B,C} x settings {P55,P12};
N=600, T=46; canonical HK gates; treated gate G6->G9 (index 1, kind=contest, share_of cohort, gate-level r by L:
1.2 at L=.25, 1.6 at L=.45, fail from canonical HK gates).
Seeds: FRESH confirmatory block 400-407 only; the runner REJECTS screening 0-7, A5 100-115, the smoke-contaminated
200-207, and pilot 300-307. Host smoke uses ONLY the non-declared seed 900 (--smoke) and is never aggregated.
Pilot (variance only) uses the separate block 300-307 and is invoked with --variance-pilot; pilot rows are never
confirmatory rows. A6 is an ESTIMATION/PRECISION study (pre-declared expectation FAILS vs minima); no confirmation claim.
Outcomes: behavioural only; manipulation-check series (own_share/withheld) recorded but never used as estimands.
"""
import argparse, hashlib, json, os, sys, warnings

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
ENGINE = os.path.join(REPO, 'engine'); SPEC = os.path.join(REPO, 'docs', 'audit', 'canonical_spec.json')
CONFIRM_SEEDS = tuple(range(400, 408)); PILOT_SEEDS = tuple(range(300, 308))
SMOKE_ONLY_SEED = 900   # host smoke must use this non-declared seed; never aggregated
FORBIDDEN = tuple(range(0, 8)) + tuple(range(100, 116)) + tuple(range(200, 208)) + PILOT_SEEDS
Q0S = [0.85, 1.0, 1.15]; LS = [0.25, 0.45]
SUPPLY = {'A': dict(own_ban=0.0, firm_ban=0.0), 'B': dict(own_ban=0.95, firm_ban=0.0), 'C': dict(own_ban=0.0, firm_ban=0.9)}
SETTINGS = {'P55': dict(pay_ratio=0.55, monitoring=0.2, withhold_mode='pay_gap'),
            'P12': dict(pay_ratio=1.2, monitoring=0.5, withhold_mode='pay_gap')}
N, T = 600, 46
FIXED_R = 12.0
L_R = {0.25: 1.2, 0.45: 1.6}

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()
def cid(S, L, sup, st): return f'S{float(S):.2f}|L{float(L):.2f}|{sup}|{st}'
def cells(): return [cid(S, L, sup, st) for S in Q0S for L in LS for sup in SUPPLY for st in SETTINGS]

def params(S, L, sup, st, seed):
    p = json.loads(json.dumps(json.load(open(SPEC))['params']['HK']['primary']))
    p.update(N=N, T=T, seed=seed, q0=float(S)); p.update(SUPPLY[sup]); p.update(SETTINGS[st])
    p['gates'] = json.loads(json.dumps(p['gates']))
    p['gates'][1] = dict(kind='contest', share=float(L), cut0=6.0, r=L_R[float(L)], alpha=0.5, fail='stop',
                         spec=dict(id='A6-G9', label='A6 gate under test'))
    return p

def run_seed(S, L, sup, st, seed):
    warnings.filterwarnings('ignore'); sys.path.insert(0, ENGINE)
    import numpy as np
    from eduengine.core import Engine
    from eduengine.modules.labour import QueueLabour
    from eduengine.modules.schools import PrivateSchools, PublicSchools
    from eduengine.modules.sdg4 import SDG4
    from eduengine.modules.tutoring import TutoringMarket
    E = Engine([PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()], **params(S, L, sup, st, seed)); E.run()
    if getattr(E, 'unfired_events', []): raise RuntimeError(f'unfired events {E.unfired_events}')
    m = E.p['measure_from']; R = E.R
    def mn(k):
        v = np.asarray(R.get(k, []), float); return float(np.nanmean(v[m:])) if v.size else None
    X = E.ALL; sel = (X['cohort'] >= m) & (X['cohort'] <= E.p['T'] - 26)
    if not sel.any(): sel = X['cohort'] >= m
    L9 = np.asarray(X['L9'], float)[sel]; q = np.asarray(X['q'])[sel]; q1 = q == 0
    row = {k: mn(k) for k in ('tut_k12_rate', 'tut_k12_spend', 'tut_g12_rate', 'q5_q1_part_gap_pp', 'q5_q1_spend_gap',
                              'q5_q1_spend_ratio', 'L6_mean', 'L9_mean', 'own_share', 'withheld', 'q_pub')}
    row.update(fixed_R_gap_close=float(np.mean(L9[q1] >= FIXED_R)) if q1.any() else None,
               L9_q1_mean=float(np.nanmean(L9[q1])) if q1.any() else None,
               cid=cid(S, L, sup, st), S=S, L=L, supply=sup, settings=st, seed=seed, N=N, T=T, measure_from=m,
               stage=('smoke' if seed == SMOKE_ONLY_SEED else ('pilot' if seed in PILOT_SEEDS else 'confirmatory')), unfired_events=list(getattr(E, 'unfired_events', [])))
    return row

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('cell', nargs='?'); ap.add_argument('--id')
    ap.add_argument('--seeds', required=True); ap.add_argument('--out-dir', required=True)
    ap.add_argument('--variance-pilot', action='store_true')
    ap.add_argument('--smoke', action='store_true', help='smoke only: single non-declared seed 900, never aggregated')
    a = ap.parse_args()
    seeds = list(range(int(a.seeds.split('-')[0]), int(a.seeds.split('-')[1]) + 1)) if '-' in a.seeds else [int(x) for x in a.seeds.split(',')]
    if a.smoke:
        bad = [s for s in seeds if s != SMOKE_ONLY_SEED]
        if bad: raise SystemExit(f'smoke must use the non-declared seed {SMOKE_ONLY_SEED}; got {bad}')
    elif a.variance_pilot:
        bad = [s for s in seeds if s not in PILOT_SEEDS]
        if bad: raise SystemExit(f'variance pilot must use pilot block {PILOT_SEEDS}; got {bad}')
    else:
        bad = [s for s in seeds if s not in CONFIRM_SEEDS]
        if bad: raise SystemExit(f'A6 estimation run requires fresh block {CONFIRM_SEEDS}; refusing {bad}; forbidden blocks: 0-7, 100-115, 200-207 (smoke-contaminated), 300-307')
    cidv = a.cell or a.id
    if not cidv: raise SystemExit('provide cell id as positional or --id')
    if cidv not in cells(): raise SystemExit(f'unknown A6 cell {cidv}')
    S, L, sup, st = cidv.split('|'); S = S[1:]; L = L[1:]
    os.makedirs(a.out_dir, exist_ok=True)
    fn = os.path.join(a.out_dir, 'ckpt_' + cidv.replace('|', '_') + '.jsonl')
    done = {int(json.loads(l)['seed']) for l in open(fn)} if os.path.exists(fn) else set()
    for sd in seeds:
        if sd in done: continue
        row = run_seed(float(S), float(L), sup, st, sd)
        if a.smoke: row['stage'] = 'smoke'
        with open(fn, 'a') as f: f.write(json.dumps(row) + '\n'); f.flush(); os.fsync(f.fileno())
    print('cell', cidv, 'seeds', seeds, '->', fn)

if __name__ == '__main__':
    main()
