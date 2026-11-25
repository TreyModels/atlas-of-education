#!/usr/bin/env python3
"""NEW-GENERATION Paper A (c): gate-architecture sweep >=5,000 runs (prereg GATE2_PREREGISTRATION.md §2(c)).

Design (declared NEW; not a reconstruction of Gemini's undocumented parameterisation):
  gate architectures at the G6->G9 transition: bar, bar_high, quota, contest  (gate 0 = primary completion bar,
  gate 2 = G12 contest, gate 3 = tertiary bar are held fixed); seat share S in {0.25,0.35,0.45,0.55,0.70} for the
  share-based architectures (quota/contest) and the corresponding bar quantile for the bar architectures;
  fee regimes {0.19 (kept), 0.00 (abolished at t0)}; formal-vacancy vac0 in {0.02,0.08,0.25,0.50};
  seeds 0..31 per cell -> 4 x 5 x 2 x 4 x 32 = 5,120 runs.
  Outcome: Q5-Q1 K-12 tutoring-participation gap (pp), pre (t0-4..t0-1) vs post (t0+1..t0+4);
  Delta_cut = gap_delta(fee abolished) - gap_delta(fee kept); H2 = mean Delta_cut at S=0.25 minus S=0.70 (contest/quota).
  Runner: per-cell subprocess, per-seed atomic checkpoints, resume by skip, arm failure raises (loud).
Label: NEW GENERATION — REPRODUCED SIMULATION (repaired engine 98baf6b, frozen spec), NOT a reproduction of the
Gemini 1,640-run experiment.
"""
import argparse, hashlib, json, os, subprocess, sys, time, warnings

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
ENGINE = os.path.join(REPO, 'engine'); SPEC = os.path.join(REPO, 'docs', 'audit', 'canonical_spec.json')
LABEL = ('NEW GENERATION — REPRODUCED SIMULATION (repaired engine 98baf6b, frozen spec); '
         'NOT a reproduction of the Gemini-era 1,640-run experiment')
ARCHS = ['bar', 'bar_high', 'quota', 'contest']; SHARES = [0.25, 0.35, 0.45, 0.55, 0.70]
FEES = [0.19, 0.00]; VACS = [0.02, 0.08, 0.25, 0.50]; NSEEDS = 32
T0 = 12; T = T0 + 8; PRE = list(range(T0 - 4, T0)); POST = list(range(T0 + 1, T0 + 5))

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def gate_for(arch, S):
    """Gate at the G6->G9 transition for architecture/seat share S. Bar thresholds calibrated to S via the
    pre-registered engine quantile rule (declared in the prereg appendix as NEW)."""
    if arch == 'bar':
        return dict(kind='fixed_bar', bar=3.0 + 8.0 * (1.0 - S), fail='stop')
    if arch == 'bar_high':
        return dict(kind='fixed_bar', bar=6.0 + 8.0 * (1.0 - S), fail='stop')
    if arch == 'quota':
        return dict(kind='quota', share=S, cut0=6.0, fail='stop')
    if arch == 'contest':
        return dict(kind='contest', share=S, cut0=6.0, r=0.6, alpha=0.5, fail='stop')
    raise ValueError(arch)

def params(arch, S, fee, vac0):
    spec = json.load(open(SPEC))
    base = json.loads(json.dumps(spec['params']['KR']['primary']))
    p = dict(base)
    p.update(N=300, T=T, measure_from=4, vac0=float(vac0), fee_public=float(fee),
             gates=[dict(kind='fixed_bar', bar=2.0, spec=dict(id='G6', label='primary completion')),
                    dict(gate_for(arch, S), spec=dict(id=f'G9-{arch}-{S}', label='gate architecture under test')),
                    dict(kind='contest', share=0.12, fail='track', spec=dict(id='G12', label='university gate')),
                    dict(kind='fixed_bar', bar=10.0, spec=dict(id='TER', label='tertiary completion'))])
    if fee == 0.0:
        p['events'] = [dict(year=T0, set=dict(fee_public=0.0), label='fee abolition')]
    return p

def gap(E):
    import numpy as np
    rq = np.array(E.R['tut_k12_rate_by_q'], float)
    pre = 100.0 * float(np.mean(rq[PRE, 4] - rq[PRE, 0]))
    post = 100.0 * float(np.mean(rq[POST, 4] - rq[POST, 0]))
    return pre, post, post - pre

def run_cell(arch, S, fee, vac0, seeds, out_dir):
    warnings.filterwarnings('ignore')
    os.makedirs(out_dir, exist_ok=True)
    sys.path.insert(0, ENGINE)
    import numpy as np
    from eduengine.core import Engine
    from eduengine.modules.labour import QueueLabour
    from eduengine.modules.schools import PrivateSchools, PublicSchools
    from eduengine.modules.sdg4 import SDG4
    from eduengine.modules.tutoring import TutoringMarket
    p = params(arch, S, fee, vac0)
    tag = f"{arch}_{S:.2f}_{fee:.2f}_{vac0:.2f}"
    ckpt = os.path.join(out_dir, f'ckpt_{tag}.jsonl')
    done = set()
    if os.path.exists(ckpt):
        for line in open(ckpt):
            try: done.add(int(json.loads(line)['seed']))
            except Exception: pass
    for sd in seeds:
        if sd in done: continue
        mods = [PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()]
        E = Engine(mods, **dict(p, seed=sd)); E.run()
        unfired = list(getattr(E, 'unfired_events', []))
        if unfired:
            raise RuntimeError(f'unfired calendar events in cell {tag}: {unfired}')
        pre, post, d = gap(E)
        row = dict(arch=arch, S=S, fee=fee, vac0=vac0, seed=sd, gap_pre=pre, gap_post=post, gap_delta=d,
                   contest_e_mean=float(np.mean(E.R['contest_e_mean'][E.p['measure_from']:])),
                   k12_spend=float(np.mean(E.R['tut_k12_spend'][E.p['measure_from']:])))
        with open(ckpt, 'a') as f:
            f.write(json.dumps(row) + '\n'); f.flush(); os.fsync(f.fileno())
    return tag

def stats(v):
    import numpy as np
    a = np.array(v, float); n = len(a); m = float(a.mean()); sa = float(a.std(ddof=1)) if n > 1 else 0.0
    se = sa / np.sqrt(max(n, 1))
    return dict(mean=m, sd=sa, ci95_lo=m - 1.96 * se, ci95_hi=m + 1.96 * se, n=n)

def driver(seeds, workers, out_dir):
    from concurrent.futures import ThreadPoolExecutor
    from collections import defaultdict
    os.makedirs(out_dir, exist_ok=True)
    cells = [(a, S, f, v) for a in ARCHS for S in SHARES for f in FEES for v in VACS]
    t0 = time.time()
    def launch(c):
        a, S, f, v = c
        r = subprocess.run([sys.executable, os.path.abspath(__file__), 'cell', a, str(S), str(f), str(v),
                            f'{seeds[0]}-{seeds[-1]}', out_dir], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONPATH=ENGINE, OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1',
                                    OMP_NUM_THREADS='1'))
        if r.returncode != 0:
            raise RuntimeError(f'cell {c} failed rc={r.returncode}: {r.stderr[-1000:]}')
        return c
    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(launch, cells))
    wall = time.time() - t0
    rows = []
    for a, S, f, v in cells:
        tag = f"{a}_{S:.2f}_{f:.2f}_{v:.2f}"
        rows.extend(json.loads(l) for l in open(os.path.join(out_dir, f'ckpt_{tag}.jsonl')))
    # cell means and H1/H2
    cells_out = {}
    for r in rows:
        key = (r['arch'], r['S'], r['fee'], r['vac0'])
        cells_out.setdefault(key, []).append(r)
    summary = {}
    for (a, S, f, v), rr in cells_out.items():
        summary.setdefault(a, {}).setdefault(str(S), {})[f'{f:.2f}_{v:.2f}'] = {m: stats([x[m] for x in rr]) for m in
                                                                               ('gap_pre', 'gap_post', 'gap_delta')}
    # Delta_cut by (arch,S,vac): fee0 delta - fee0.19 delta (matched cells, independent seeds)
    dcut = {}
    for a in ARCHS:
        for S in SHARES:
            for v in VACS:
                k0 = (a, S, 0.0, v); k1 = (a, S, 0.19, v)
                if k0 in cells_out and k1 in cells_out:
                    d0 = float(np.mean([x['gap_delta'] for x in cells_out[k0]]))
                    d1 = float(np.mean([x['gap_delta'] for x in cells_out[k1]]))
                    dcut[f'{a}|{S}|{v}'] = d0 - d1
    def h2(arch):
        a = [dcut[f'{arch}|0.25|{v}'] for v in VACS if f'{arch}|0.25|{v}' in dcut]
        b = [dcut[f'{arch}|0.70|{v}'] for v in VACS if f'{arch}|0.70|{v}' in dcut]
        return float(np.mean(a) - np.mean(b)) if a and b else None
    payload = dict(label=LABEL,
                   metadata=dict(generation='NEW GENERATION', spec=sha(SPEC), engine_commit='846c9e0',
                                 unfired_events_asserted=True,
                                 engine_core_sha256=sha(os.path.join(ENGINE, 'eduengine', 'core.py')),
                                 runner_sha256=sha(os.path.abspath(__file__)), seeds=list(seeds),
                                 n_seeds=len(seeds), n_cells=len(cells), total_runs=len(rows), workers=workers,
                                 elapsed_seconds=round(wall, 2), T0=T0, T=T,
                                 env='py3.10.8 numpy2.2.6; BLAS/OMP=1; nice 10',
                                 preregistration='docs/audit/GATE2_PREREGISTRATION.md'),
                   cells={f'{a}|{S}|{f}|{v}': summary[a][str(S)][f'{f:.2f}_{v:.2f}'] for a in ARCHS for S in SHARES for f in FEES for v in VACS if a in summary},
                   delta_cut=dcut, H2={a: h2(a) for a in ARCHS})
    path = os.path.join(out_dir, 'gate_architecture_results.json')
    json.dump(payload, open(path, 'w'), indent=2)
    print('wrote', path, 'sha', sha(path), 'runs', len(rows), 'wall', round(wall, 1))
    return 0

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'cell':
        a, S, f, v, ss, out = sys.argv[2:8]
        run_cell(a, float(S), float(f), float(v), [int(x) for x in ss.split('-')] if '-' in ss else [int(ss)], out)
        return 0
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', default=f'0-{NSEEDS - 1}'); ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--out-dir', default=os.path.join(REPO, 'results', 'newgen_gate'))
    ap.add_argument('--fees', default='0.19,0.00', help='comma list of fee regimes; use 0.19 for the fee-free subset')
    a = ap.parse_args()
    global FEES
    FEES = [float(x) for x in a.fees.split(',')]
    return driver([int(x) for x in a.seeds.split('-')] if '-' in a.seeds else [int(a.seeds)], a.workers, a.out_dir)

if __name__ == '__main__':
    sys.exit(main())
