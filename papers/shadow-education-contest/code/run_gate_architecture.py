#!/usr/bin/env python3
"""NEW-GENERATION Paper A (c): gate-architecture sweep (amended per adjudicator review, prereg A3).

Design (declared NEW; engine pin 846c9e0; not a reconstruction of the Gemini 1,640-run experiment):
  * Gate under test = G6->G9 transition; fail routing PRIMARY = 'track' (matches canonical KR G9-track design),
    declared sensitivity block = 'stop' (contest only, S in {0.25,0.70}, all vac0, both fees) -> 512 runs.
  * Architectures {bar, bar_high, quota, contest} x seat shares S {0.25,0.35,0.45,0.55,0.70}
    x fee regimes {0.19 kept, 0.00 abolished at T0 via year_t event} x vac0 {0.02,0.08,0.25,0.50} x 32 matched seeds.
  * Outcomes: Q5-Q1 K-12 tutoring-participation gap pre (T0-4..T0-1) vs post (T0+1..T0+6);
    gap_delta = post - pre; Delta_cut = gap_delta(fee=0) - gap_delta(fee=0.19) (matched seeds).
  * PRIMARY estimand (pre-declared): H2_contest = Delta_cut(contest, S=.25) - Delta_cut(contest, S=.70) at
    vac0=0.08, fail='track'; uncertainty = PAIRED-SEED bootstrap (5,000 resamples of the 32 matched seeds,
    same seed index for fee0/fee0.19). Secondary: quota H2, per-vac0 Delta_cut curve, H1 (fee=0 gap widening as S
    falls + Spearman monotonicity). bar/bar_high = EXPLORATORY architecture check only (S maps to a bar threshold,
    not a realized seat share); realized admission rates reported per cell. Multiplicity: one pre-stated primary;
    all other contrasts secondary/exploratory. Null/negative H2 is a result; the pre-repair +0.1086 is the
    AUTHOR-REPORTED baseline, not a target.
  * Provenance: fees/archs/shares/vacs/N/T0/T/measure_from/start_year, engine core sha, spec sha, runner sha,
    event_key year_t, per-run event_log, quintile x urban counts, gate applicants/seats/admit rates; per-run
    assertion E.unfired_events == [].
Label: NEW GENERATION — REPRODUCED SIMULATION (engine 846c9e0), NOT a reproduction of the Gemini 1,640-run study.
"""
import argparse, copy, hashlib, json, os, subprocess, sys, time, warnings

HERE = os.path.dirname(os.path.abspath(__file__)); REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
ENGINE = os.path.join(REPO, 'engine'); SPEC = os.path.join(REPO, 'docs', 'audit', 'canonical_spec.json')
LABEL = ('NEW GENERATION — REPRODUCED SIMULATION (engine 846c9e0, frozen spec); '
         'NOT a reproduction of the Gemini-era 1,640-run experiment')
ARCHS = ['bar', 'bar_high', 'quota', 'contest']; SHARES = [0.25, 0.35, 0.45, 0.55, 0.70]
FEES = [0.19, 0.00]; VACS = [0.02, 0.08, 0.25, 0.50]; NSEEDS = 32
T0, T = 12, 20; PRE = list(range(T0 - 4, T0)); POST = list(range(T0 + 1, T0 + 7))
PRIMARY_VAC = 0.08; PRIMARY_ARCH = 'contest'; PRIMARY_LO, PRIMARY_HI = 0.25, 0.70
SENS_ARCH = 'contest'; SENS_SHARES = [0.25, 0.70]

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def gate_for(arch, S, fail):
    if arch == 'bar': return dict(kind='fixed_bar', bar=3.0 + 8.0 * (1.0 - S), fail=fail)
    if arch == 'bar_high': return dict(kind='fixed_bar', bar=6.0 + 8.0 * (1.0 - S), fail=fail)
    if arch == 'quota': return dict(kind='quota', share=S, cut0=6.0, fail=fail)
    if arch == 'contest': return dict(kind='contest', share=S, cut0=6.0, r=0.6, alpha=0.5, fail=fail)
    raise ValueError(arch)

def params(arch, S, fee, vac0, fail='track'):
    spec = json.load(open(SPEC))
    base = json.loads(json.dumps(spec['params']['KR']['primary']))
    p = dict(base)
    p.update(N=300, T=T, measure_from=4, vac0=float(vac0), fee_public=float(fee),
             gates=[dict(kind='fixed_bar', bar=2.0, spec=dict(id='G6', label='primary completion')),
                    dict(gate_for(arch, S, fail), spec=dict(id=f'G9-{arch}-{S}-{fail}', label='gate architecture under test')),
                    dict(kind='contest', share=0.12, fail='track', spec=dict(id='G12', label='university gate')),
                    dict(kind='fixed_bar', bar=10.0, spec=dict(id='TER', label='tertiary completion'))])
    if fee == 0.0:
        p['events'] = [dict(year_t=T0, set=dict(fee_public=0.0), label='fee abolition')]
    return p

def gap(E):
    import numpy as np
    rq = np.array(E.R['tut_k12_rate_by_q'], float)
    pre = 100.0 * float(np.mean(rq[PRE, 4] - rq[PRE, 0]))
    post = 100.0 * float(np.mean(rq[POST, 4] - rq[POST, 0]))
    return pre, post, post - pre

def design_diag(E):
    """Quintile x urban counts and gate applicants/seats/admit rates for the gate under test (level index 1)."""
    import numpy as np
    X = E.ALL; m = E.p['measure_from']
    sel = (X['cohort'] >= m) & (X['cohort'] <= E.p['T'] - 14)
    q = np.asarray(X['q'])[sel]; urban = np.asarray(X['urban'])[sel]
    cells = {f'q{j}_u{int(u)}': int(np.sum((q == j) & (urban == u))) for j in range(5) for u in (0, 1)}
    def ser(name):
        v = np.asarray(E.R.get(name, []), float)
        return float(np.mean(v[m:])) if v.ndim == 2 else (float(np.mean(v[m:])) if v.size else None)
    return dict(cells=cells, contest_candidates=ser('contest_candidates'), contest_seats=ser('contest_seats'),
                contest_admitted=ser('contest_admitted'), contest_applicant_seat_ratio=ser('contest_applicant_seat_ratio'),
                contest_admit_rate=ser('contest_admit_rate'))

def run_cell(arch, S, fee, vac0, fail, seeds, out_dir):
    warnings.filterwarnings('ignore'); os.makedirs(out_dir, exist_ok=True)
    sys.path.insert(0, ENGINE)
    import numpy as np
    from eduengine.core import Engine
    from eduengine.modules.labour import QueueLabour
    from eduengine.modules.schools import PrivateSchools, PublicSchools
    from eduengine.modules.sdg4 import SDG4
    from eduengine.modules.tutoring import TutoringMarket
    p = params(arch, S, fee, vac0, fail)
    tag = f"{arch}_{S:.2f}_{fee:.2f}_{vac0:.2f}_{fail}"
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
        if E.unfired_events:
            raise RuntimeError(f'unfired calendar events in cell {tag}: {E.unfired_events}')
        pre, post, d = gap(E)
        g = copy.deepcopy(E.p['gates'][1])
        row = dict(arch=arch, S=S, fee=fee, vac0=vac0, fail=fail, seed=sd,
                   gap_pre=pre, gap_post=post, gap_delta=d,
                   gate_spec={k: g.get(k) for k in ('kind', 'share', 'bar', 'cut0', 'r', 'alpha', 'fail')},
                   event_log=list(E.event_log),
                   contest_e_mean=float(np.mean(E.R['contest_e_mean'][E.p['measure_from']:])),
                   k12_spend=float(np.mean(E.R['tut_k12_spend'][E.p['measure_from']:])),
                   design=design_diag(E))
        with open(ckpt, 'a') as f:
            f.write(json.dumps(row) + '\n'); f.flush(); os.fsync(f.fileno())
    return tag

def stats(v):
    import numpy as np
    a = np.array(v, float); n = len(a); m = float(a.mean()); sa = float(a.std(ddof=1)) if n > 1 else 0.0
    se = sa / np.sqrt(max(n, 1))
    return dict(mean=m, sd=sa, ci95_lo=m - 1.96 * se, ci95_hi=m + 1.96 * se, n=n)

def dcut_for(cells, arch, S, vac, fail):
    """Paired-seed Delta_cut = mean over seeds of [gap_delta(fee0,seed) - gap_delta(fee0.19,seed)]."""
    k0 = (arch, S, 0.0, vac, fail); k1 = (arch, S, 0.19, vac, fail)
    if k0 not in cells or k1 not in cells: return None
    a = {r['seed']: r['gap_delta'] for r in cells[k0]}; b = {r['seed']: r['gap_delta'] for r in cells[k1]}
    common = sorted(set(a) & set(b))
    vals = [a[s] - b[s] for s in common]
    return dict(values=vals, seeds=common, mean=float(sum(vals) / len(vals)) if vals else None)

def paired_boot(vals, n=5000, seed=20261125):
    import numpy as np
    if not vals: return None
    rng = np.random.default_rng(seed); a = np.array(vals, float)
    bs = np.array([np.mean(a[rng.integers(0, len(a), len(a))]) for _ in range(n)])
    return dict(mean=float(a.mean()), ci95_lo=float(np.percentile(bs, 2.5)), ci95_hi=float(np.percentile(bs, 97.5)),
                half_width=float((np.percentile(bs, 97.5) - np.percentile(bs, 2.5)) / 2.0), n_boot=n)

def spearman(x, y):
    import numpy as np
    x = np.asarray(x, float); y = np.asarray(y, float)
    rx = np.argsort(np.argsort(x)); ry = np.argsort(np.argsort(y))
    return float(np.corrcoef(rx, ry)[0, 1])


def h1_bootstrap(cells_rows, arch=PRIMARY_ARCH, vac=PRIMARY_VAC, n_boot=5000, seed=20261125):
    """Seed-resampled 95% CI for H1 = gap_delta(fee=0,S=.25) - gap_delta(fee=0,S=.70) (secondary statistic)."""
    import numpy as np
    k_lo = (arch, 0.25, 0.0, vac, 'track'); k_hi = (arch, 0.70, 0.0, vac, 'track')
    if k_lo not in cells_rows or k_hi not in cells_rows: return None
    lo = {r['seed']: r['gap_delta'] for r in cells_rows[k_lo]}
    hi = {r['seed']: r['gap_delta'] for r in cells_rows[k_hi]}
    common = sorted(set(lo) & set(hi))
    if not common: return None
    rng = np.random.default_rng(seed)
    vals = []
    for _ in range(n_boot):
        pick = rng.integers(0, len(common), len(common))
        vals.append(float(np.mean([lo[common[i]] - hi[common[i]] for i in pick])))
    a = np.array(vals)
    return dict(mean=float(np.mean([lo[s] - hi[s] for s in common])),
                ci95_lo=float(np.percentile(a, 2.5)), ci95_hi=float(np.percentile(a, 97.5)),
                half_width=float((np.percentile(a, 97.5) - np.percentile(a, 2.5)) / 2.0), n_boot=n_boot)

def driver(seeds, workers, out_dir, include_sensitivity=True):
    from concurrent.futures import ThreadPoolExecutor
    os.makedirs(out_dir, exist_ok=True)
    cells = [(a, S, f, v, 'track') for a in ARCHS for S in SHARES for f in FEES for v in VACS]
    if include_sensitivity:
        cells += [(SENS_ARCH, S, f, v, 'stop') for S in SENS_SHARES for f in FEES for v in VACS]
    t0 = time.time()
    def launch(c):
        a, S, f, v, fail = c
        r = subprocess.run([sys.executable, os.path.abspath(__file__), 'cell', a, str(S), str(f), str(v), fail,
                            f'{seeds[0]}-{seeds[-1]}', out_dir], capture_output=True, text=True,
                           env=dict(os.environ, PYTHONPATH=ENGINE, OPENBLAS_NUM_THREADS='1', MKL_NUM_THREADS='1', OMP_NUM_THREADS='1'))
        if r.returncode != 0:
            raise RuntimeError(f'cell {c} failed rc={r.returncode}: {r.stderr[-1200:]}')
        return c
    with ThreadPoolExecutor(max_workers=workers) as ex:
        list(ex.map(launch, cells))
    wall = time.time() - t0
    rows = []
    for c in cells:
        a, S, f, v, fail = c
        tag = f"{a}_{S:.2f}_{f:.2f}_{v:.2f}_{fail}"
        rows.extend(json.loads(l) for l in open(os.path.join(out_dir, f'ckpt_{tag}.jsonl')))
    cells_rows = {}
    for r in rows:
        cells_rows.setdefault((r['arch'], r['S'], r['fee'], r['vac0'], r['fail']), []).append(r)
    summary = {}
    for (a, S, f, v, fail), rr in cells_rows.items():
        summary.setdefault(fail, {}).setdefault(a, {}).setdefault(str(S), {})[f'{f:.2f}_{v:.2f}'] = {
            m: stats([x[m] for x in rr]) for m in ('gap_pre', 'gap_post', 'gap_delta')}
    # primary H2 (contest, vac0=.08, track)
    def h2(arch, fail='track', vac=PRIMARY_VAC):
        d_lo = dcut_for(cells_rows, arch, PRIMARY_LO, vac, fail)
        d_hi = dcut_for(cells_rows, arch, PRIMARY_HI, vac, fail)
        if d_lo is None or d_hi is None: return None
        if d_lo['seeds'] != d_hi['seeds']:
            raise RuntimeError(f'paired-seed mismatch in {arch}/{vac}/{fail}: {d_lo["seeds"]} vs {d_hi["seeds"]}')
        vals = [lo - hi for lo, hi in zip(d_lo['values'], d_hi['values'])]
        return dict(mean=float(np.mean(vals)), stats=stats(vals), paired_bootstrap=paired_boot(vals),
                    dcut_lo=paired_boot(d_lo['values']), dcut_hi=paired_boot(d_hi['values']))
    primary = h2(PRIMARY_ARCH, 'track')
    secondary = {'quota_H2': h2('quota', 'track'),
                 'contest_H2_stop_sensitivity': h2('contest', 'stop'),
                 'contest_vac0_curve': {}}
    for v in VACS:
        r = h2('contest', 'track', vac=v)
        secondary['contest_vac0_curve'][f'{v:.2f}'] = r
    # H1: fee=0 gap widening as S falls (contest, track, vac0=.08) + Spearman across shares
    h1 = None
    if all((PRIMARY_ARCH, S, 0.0, PRIMARY_VAC, 'track') in cells_rows for S in SHARES):
        gd = {S: float(np.mean([r['gap_delta'] for r in cells_rows[(PRIMARY_ARCH, S, 0.0, PRIMARY_VAC, 'track')]])) for S in SHARES}
        h1 = dict(gap_delta_fee0_by_share={f'{S:.2f}': gd[S] for S in SHARES},
                  H1_S025_minus_S070=gd[0.25] - gd[0.70],
                  spearman_gapdelta_vs_share=spearman(SHARES, [gd[S] for S in SHARES]),
                  h1_seed_bootstrap=h1_bootstrap(cells_rows),
                  note='H1 = fee=0 gap_delta(S=.25) - gap_delta(S=.70); negative Spearman means gap widens as seats shrink; bootstrap resamples seeds (not a proper paired bootstrap for the H1 delta — point + Spearman are the declared minimum)')
    exploratory = {a: {f'{S:.2f}': {f'{f:.2f}_{v:.2f}': {'gap_delta': summary['track'][a].get(str(S), {}).get(f'{f:.2f}_{v:.2f}', {}).get('gap_delta', {})}
                                    for f in FEES for v in VACS} for S in SHARES} for a in ('bar', 'bar_high')}
    # realized admission / design diagnostics per cell (mean over runs)
    design = {}
    for (a, S, f, v, fail), rr in cells_rows.items():
        design[f'{a}|{S}|{f}|{v}|{fail}'] = {
            'admit_rate': stats([x['design']['contest_admit_rate'] for x in rr if x['design']['contest_admit_rate'] is not None]),
            'applicant_seat_ratio': stats([x['design']['contest_applicant_seat_ratio'] for x in rr if x['design']['contest_applicant_seat_ratio'] is not None]),
            'quintile_urban_cells': rr[0]['design']['cells'] if rr else None,
            'gate_spec': rr[0]['gate_spec'] if rr else None}
    payload = dict(label=LABEL,
                   metadata=dict(generation='NEW GENERATION', engine_commit='846c9e0',
                                 engine_core_sha256=sha(os.path.join(ENGINE, 'eduengine', 'core.py')),
                                 spec_sha256=sha(SPEC), runner_sha256=sha(os.path.abspath(__file__)),
                                 archs=ARCHS, shares=SHARES, fees=FEES, vacs=VACS, N=300, T0=T0, T=T,
                                 measure_from=4, start_year=0, event_key='year_t',
                                 seeds=list(seeds), n_seeds=len(seeds), n_cells=len(cells), total_runs=len(rows),
                                 workers=workers, elapsed_seconds=round(wall, 2), unfired_events_asserted=True,
                                 fail_routing=dict(primary='track', sensitivity='stop (contest only, S .25/.70, all vac0, both fees)'),
                                 primary_estimand=f'H2_contest(vac0={PRIMARY_VAC}, fail=track) = Delta_cut(S=.25)-Delta_cut(S=.70); paired-seed bootstrap 95% CI',
                                 mde_proxy='bootstrap 95% CI half-width of the primary H2 (reported); 32 matched seeds',
                                 multiplicity='one pre-stated primary (contest H2 at vac0=.08); quota H2, vac0 curve, H1 secondary; bar/bar_high exploratory',
                                 baseline_note='pre-repair +0.1086 is AUTHOR-REPORTED baseline, not a target',
                                 design_check_note='quintile x urban counts use cohorts measure_from..T-14 (partial cohorts expected); reported as a design check only, NOT an estimation population',
                                 achieved_mde_proxy='primary_H2 paired-seed bootstrap 95% CI half-width (see primary_H2_contest.paired_bootstrap.half_width); a |H2| below it is inconclusive-or-null, not evidence of no effect'),
                   primary_H2_contest=primary, secondary=secondary, H1=h1, exploratory_bar_archs=exploratory,
                   cells=summary, design_diagnostics=design)
    path = os.path.join(out_dir, 'gate_architecture_results.json')
    json.dump(payload, open(path, 'w'), indent=2)
    print('wrote', path, 'sha', sha(path), 'runs', len(rows), 'wall', round(wall, 1))
    return 0

def main():
    if len(sys.argv) > 1 and sys.argv[1] == 'cell':
        a, S, f, v, fail, ss, out = sys.argv[2:9]
        seeds = (list(range(int(ss.split('-')[0]), int(ss.split('-')[1]) + 1)) if '-' in ss else [int(ss)])
        run_cell(a, float(S), float(f), float(v), fail, seeds, out)
        return 0
    ap = argparse.ArgumentParser()
    ap.add_argument('--seeds', default=f'0-{NSEEDS - 1}'); ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--out-dir', default=os.path.join(REPO, 'results', 'newgen_gate'))
    ap.add_argument('--fees', default='0.19,0.00')
    ap.add_argument('--no-sensitivity', action='store_true')
    a = ap.parse_args()
    global FEES
    FEES = [float(x) for x in a.fees.split(',')]
    seeds = (list(range(int(a.seeds.split('-')[0]), int(a.seeds.split('-')[1]) + 1)) if '-' in a.seeds
             else [int(x) for x in a.seeds.split(',')])
    return driver(seeds, a.workers, a.out_dir, include_sensitivity=not a.no_sensitivity)

if __name__ == '__main__':
    sys.exit(main())
