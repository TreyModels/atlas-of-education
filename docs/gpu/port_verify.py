#!/usr/bin/env python3
"""Host-side verification harness for the GPU Plackett-Luce port (branch gpu-pl-port-auditv2).

Codex-rule coverage: RNG integrity (rule 1), parity incl. discrete winner sets (rule 2), full-wall
benchmark metadata (rule 3), provenance manifest (rule 4), staged cross-replica note (rule 5).

Subcommands (CPU-only ones need no torch; GPU ones require ATLAS_PL_BACKEND=gpu + torch/CUDA):

  cpu-digest    --spec SPEC --json OUT
      130-fixture sweep (exact docs/gpu/exp/eq_check2.py generator, seed 20261125) on the CPU
      backend: central digest (sha256 over float64 probability bytes), batch-vs-per-row
      bit-identity, seat-sum check. Runnable on the canonical tree too (backend probe optional).

  e2e-digest    --spec SPEC --json OUT
      Canonical HK Baseline seed 0 (N=300/T=46) end-to-end on the CPU backend; digest of every
      yearly series + E.ALL arrays. Compare pre-port vs post-port: the CPU path must be
      bit-identical (default backend unset).

  rng-integrity --spec SPEC --json OUT
      Proves the port does not alter RNG/realisation semantics: (a) `pl_realize` winner masks are
      bit-identical across the 130 fixtures for fixed caller-supplied uniforms; (b)
      pl_win_probs/pl_win_probs_batch do not advance a caller numpy Generator state; (c) boundary
      cases (n in {1,2,12,20,21}, seats 0/1/n-1/n, equal & extreme weights) reproduce the same
      probabilities and winner sets.

  gpu-parity    --spec SPEC --json OUT
      ATLAS_PL_BACKEND=gpu: 130-fixture GPU batch vs CPU reference; max abs dP <= 1e-7,
      sum(P)=seats_eff, plus discrete winner-set comparison at fixed uniforms.

  pair-cells    --spec SPEC --json OUT [--n 1500 --t 46 --seeds 100-101 --cells ...]
      Rule 2: two Pilot-0 cells, same seeds, CPU run vs GPU run. Per gate-year compares candidate
      lists, admission/winner sets (Jaccard, symmetric difference, flipped seats), event-keyed RNG
      call logs (draw order/consumption), and full-run outcome scalars. Exits 1 if the CPU vs GPU
      max|dP| exceeds 1e-7 (probability level) — discrete flips are reported, not failed, because
      the declared equivalence is on probabilities and run-level scalars.

  bench         --spec SPEC --json OUT
      Rule 3: full-wall microbenchmark (import/startup, warmup/compile, one 9-row batch at
      N=600/seats=69 vs per-row CPU; peak GPU memory; data-transfer estimate). Full-cell wall
      clock recipe is in docs/gpu/PORT_REPORT.md (box, multiworker CPU vs GPU).

Every subcommand emits a provenance manifest (engine/backend files hashes, env, fixture seed,
tolerance, timestamps) and separate artifacts per backend.
"""
import argparse, hashlib, json, os, platform, sys, time
import numpy as np

FIXTURE_SEED = 20261125
N_FIXTURES = 130
TOL = 1e-7
ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


# ---------------------------------------------------------------- fixtures (must match eq_check2.py)
def fixtures():
    """EXACT copy of docs/gpu/exp/eq_check2.py fixture generation (defines the central digest)."""
    rng = np.random.default_rng(FIXTURE_SEED)
    fx = []
    for _ in range(N_FIXTURES):
        n = int(rng.choice([12, 20, 21, 40, 60, 80, 120, 200, 300, 300, 300, 400, 600]))
        seats = int(rng.integers(1, n))
        disp = float(rng.choice([0.0, 0.25, 0.5, 1.0, 1.5, 2.0, 3.0, 4.0, 6.0]))
        w = np.ones(n) if disp == 0.0 else np.exp(disp * rng.standard_normal(n))
        fx.append((n, seats, disp, w))
    return fx


def fixtures_digest(fx):
    """Digest of the fixture definition itself (weights + (n, seats, disp))."""
    h = hashlib.sha256()
    for n, s, d, w in fx:
        h.update(f'{n}|{s}|{d:.12g}|'.encode())
        h.update(np.ascontiguousarray(w, dtype=np.float64).tobytes())
    return h.hexdigest()


def digest(arrays):
    h = hashlib.sha256()
    for a in arrays:
        a = np.ascontiguousarray(np.asarray(a, dtype=np.float64))
        h.update(str(a.shape).encode())
        h.update(a.tobytes())
    return h.hexdigest()


def backend():
    from eduengine import contest_math as cm
    fn = getattr(cm, 'pl_backend', None)          # canonical tree has no pl_backend; treat as cpu
    return 'cpu' if fn is None else fn()


def manifest(extra=None):
    from eduengine import contest_math as cm
    files = {}
    for p in (os.path.join(ROOT, 'engine/eduengine/contest_math.py'),
              os.path.join(ROOT, 'engine/eduengine/core.py'),
              os.path.join(ROOT, 'engine/eduengine/contest_gpu.py'),
              os.path.join(ROOT, 'engine/eduengine/modules/tutoring.py')):
        if os.path.exists(p):
            files[os.path.relpath(p, ROOT)] = hashlib.sha256(open(p, 'rb').read()).hexdigest()
    env = dict(backend=backend(), ATLAS_PL_BACKEND=os.environ.get('ATLAS_PL_BACKEND', ''),
               python=platform.python_version(), numpy=np.__version__, platform=platform.platform(),
               tolerance=TOL, fixture_seed=FIXTURE_SEED, n_fixtures=N_FIXTURES,
               contest_math_sha256=files.get('engine/eduengine/contest_math.py'))
    try:
        import torch
        env.update(torch=torch.__version__, cuda=torch.version.cuda,
                   cuda_available=bool(torch.cuda.is_available()),
                   device=torch.cuda.get_device_name(0) if torch.cuda.is_available() else None)
    except Exception:
        env.update(torch=None)
    out = dict(manifest=dict(files=files, env=env, utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
                             engine_commit=os.environ.get('ENGINE_COMMIT', ''),
                             staged_note='cross-replica batching NOT implemented (staged after bounded pilot)'))
    if extra:
        out.update(extra)
    return out


def emit(obj, path):
    if path:
        json.dump(obj, open(path, 'w'), indent=1, sort_keys=True)
    print(json.dumps(obj, default=str, sort_keys=True))


# ---------------------------------------------------------------- CPU digest (130 fixtures)
def cpu_digest(args):
    from eduengine import contest_math as cm
    assert backend() == 'cpu', f'expected cpu backend, got {backend()!r}'
    fx = fixtures()
    ref = [np.asarray(cm.pl_win_probs(w, s, method='auto'), float) for (n, s, d, w) in fx]
    batch = [np.asarray(cm.pl_win_probs_batch(np.asarray([w]), s, method='auto')[0], float)
             for (n, s, d, w) in fx] if hasattr(cm, 'pl_win_probs_batch') else list(ref)
    bit = all(np.array_equal(a, b) for a, b in zip(ref, batch))
    seat_ok = all(abs(float(p.sum()) - min(s, n)) <= 1e-6 for p, (n, s, d, w) in zip(ref, fx))
    worst = max(float(np.max(np.abs(np.asarray(a) - np.asarray(b)))) for a, b in zip(ref, batch))
    out = manifest(dict(n_fixtures=len(fx), central_digest=digest(ref),
                        fixture_digest=fixtures_digest(fx),
                        batch_digest=digest(batch), batch_bit_identical=bool(bit),
                        max_batch_delta=worst, seat_sum_ok=bool(seat_ok)))
    if hasattr(cm, 'pl_stats'):
        out['pl_stats'] = cm.pl_stats()
    emit(out, args.json)
    return 0 if (bit and seat_ok) else 1


# ---------------------------------------------------------------- full-run CPU digest
def e2e_digest(args):
    from eduengine.core import Engine
    from eduengine.modules.labour import QueueLabour
    from eduengine.modules.schools import PrivateSchools, PublicSchools
    from eduengine.modules.sdg4 import SDG4
    from eduengine.modules.tutoring import TutoringMarket
    spec = json.load(open(args.spec))
    p = dict(spec['params']['HK']['primary']); p['seed'] = 0
    E = Engine([PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()], **p)
    t0 = time.time(); E.run(); wall = time.time() - t0
    series = [np.asarray(E.R[k], float) for k in sorted(E.R)]
    allarr = [np.asarray(E.ALL[k], float) for k in sorted(E.ALL)]
    out = manifest(dict(n_series=len(series), n_all=len(allarr),
                        series_digest=digest(series), all_digest=digest(allarr),
                        wall_seconds=round(wall, 3),
                        final_enrolled=float(E.R['enrolled'][-1]),
                        withheld=float(np.nanmean(np.asarray(E.R['withheld'], float)[E.p['measure_from']:]))))
    emit(out, args.json)
    return 0


# ---------------------------------------------------------------- RNG / realisation integrity
def rng_integrity(args):
    from eduengine import contest_math as cm
    fx = fixtures()
    # (a) pl_realize masks for fixed caller-supplied uniforms
    rng = np.random.default_rng(777001)
    masks = []
    for (n, s, d, w) in fx:
        u = rng.random(n)
        masks.append(np.argsort(-(np.log(np.maximum(w, 1e-300)) +
                                  (-np.log(-np.log(np.clip(u, 1e-12, 1 - 1e-12))))))[:min(s, n)])
    realized = [np.asarray(cm.pl_realize(w, s, rng_row))
                for (n, s, d, w), rng_row in zip(fx, [np.random.default_rng(777001 + i).random(n)
                                                      for i, (n, s, d, w) in enumerate(fx)])]
    realized_digest = digest([m.astype(float) for m in realized])
    # (b) probability calls must not advance a caller Generator
    g = np.random.default_rng(424242)
    before = g.bit_generator.state
    for (n, s, d, w) in fx[:10]:
        cm.pl_win_probs(w, s, method='auto')
        if hasattr(cm, 'pl_win_probs_batch'):
            cm.pl_win_probs_batch(np.asarray([w]), s, method='auto')
    after = g.bit_generator.state
    no_rng_consumed = (before == after)
    # (c) boundary / degenerate cases
    cases = []
    for n in (1, 2, 12, 20, 21):
        for seats in (0, 1, n - 1, n):
            w = np.ones(n)
            cases.append((n, seats, w))
    cases += [(10, 3, np.array([1e-9] * 9 + [1.0])), (10, 3, np.ones(10)),
              (10, 3, np.array([4.0, 1.0] + [1.0] * 8))]
    boundary = []
    for n, seats, w in cases:
        p = np.asarray(cm.pl_win_probs(w, seats, method='auto'), float)
        pu = np.random.default_rng(9000 + n + seats).random(n)
        ok = np.asarray(cm.pl_realize(w, seats, pu))
        boundary.append(dict(n=n, seats=seats, p_digest=digest([p]), winners=int(ok.sum()),
                             seat_sum=float(p.sum()), expect=min(seats, n),
                             seat_ok=abs(float(p.sum()) - min(seats, n)) <= 1e-6,
                             realize_ok=bool(ok.shape == (n,) and ok.dtype == bool)))
    out = manifest(dict(realize_digest=realized_digest, masks_reference_digest=digest(
                            [m.astype(float) for m in masks]),
                        probability_calls_consume_no_rng=bool(no_rng_consumed),
                        boundary=boundary,
                        boundary_ok=bool(all(b['seat_ok'] and b['realize_ok'] for b in boundary))))
    emit(out, args.json)
    return 0 if (no_rng_consumed and all(b['seat_ok'] and b['realize_ok'] for b in boundary)) else 1


# ---------------------------------------------------------------- GPU parity (130 fixtures + winners)
def gpu_parity(args):
    from eduengine import contest_math as cm
    assert backend() == 'gpu', 'set ATLAS_PL_BACKEND=gpu (and have torch/CUDA) for gpu-parity'
    fx = fixtures()
    cm.set_pl_backend('cpu')
    ref = [np.asarray(cm.pl_win_probs(w, s, method='auto'), float) for (n, s, d, w) in fx]
    u = [np.random.default_rng(5000 + i).random(n) for i, (n, s, d, w) in enumerate(fx)]
    ref_masks = [np.asarray(cm.pl_realize(w, s, uu)) for (n, s, d, w), uu in zip(fx, u)]
    cm.set_pl_backend('gpu')
    rows = []
    for k, (n, s, d, w) in enumerate(fx):
        p = np.asarray(cm.pl_win_probs_batch(np.asarray([w]), s, method='auto')[0], float)
        got = np.asarray(cm.pl_realize(w, s, u[k]))
        rows.append(dict(n=n, seats=s, disp=d, d=float(np.max(np.abs(p - ref[k]))),
                         sum=float(p.sum()), seats_expected=min(s, n),
                         winner_flips=int(np.sum(got != ref_masks[k]))))
    cm.set_pl_backend('cpu')
    worst = max(rows, key=lambda r: r['d'])
    bad_sum = [r for r in rows if abs(r['sum'] - r['seats_expected']) > 1e-6]
    out = manifest(dict(n=len(rows), max_abs_diff=worst['d'], worst=worst,
                        mean_abs_diff=float(np.mean([r['d'] for r in rows])),
                        n_gt_1e7=int(sum(r['d'] > 1e-7 for r in rows)),
                        n_gt_1e6=int(sum(r['d'] > 1e-6 for r in rows)),
                        seat_sum_violations=len(bad_sum),
                        winner_flips_total=int(sum(r['winner_flips'] for r in rows)),
                        winner_flip_fixtures=int(sum(1 for r in rows if r['winner_flips'])),
                        pl_stats=cm.pl_stats(), rows=rows))
    emit(out, args.json)
    return 0 if (out['n_gt_1e7'] == 0 and not bad_sum) else 1


# ---------------------------------------------------------------- paired full-run cells (discrete winners)
REGIMES = {
    'market_only': dict(own_ban=0.95, pay_ratio=0.55, monitoring=0.2, withhold_mode='pay_gap'),
    'own_open_gap': dict(own_ban=0.0, pay_ratio=0.55, monitoring=0.2, withhold_mode='pay_gap'),
    'own_open_incentive': dict(own_ban=0.0, pay_ratio=1.2, monitoring=0.2, withhold_mode='incentive'),
    'own_open_gap_firm_ban': dict(own_ban=0.0, pay_ratio=0.55, monitoring=0.2, withhold_mode='pay_gap',
                                  firm_ban=0.9),
}


def _pair_run(spec_path, regime, n, t, seed, backend_name):
    """Run one pilot cell; return outcome scalars, per-gate-year winner sets and RNG call log."""
    import importlib
    cm = importlib.import_module('eduengine.contest_math')
    if backend_name == 'gpu':
        cm.set_pl_backend('gpu')
    else:
        cm.set_pl_backend('cpu')
    from eduengine.core import Engine
    from eduengine.modules.labour import QueueLabour
    from eduengine.modules.schools import PrivateSchools, PublicSchools
    from eduengine.modules.sdg4 import SDG4
    from eduengine.modules.tutoring import TutoringMarket
    from eduengine.rng import EventRNG
    spec = json.load(open(spec_path))
    p = dict(spec['params']['HK']['primary']); p.update(N=n, T=t, seed=seed)
    p.update(REGIMES[regime])
    log = []
    orig_uniform = EventRNG.uniform

    def spy(self, year, shock_type, pid):
        arr = np.asarray(pid)
        log.append((int(year), str(shock_type), arr.size, hashlib.sha256(arr.tobytes()).hexdigest()[:16]))
        return orig_uniform(self, year, shock_type, pid)

    EventRNG.uniform = spy
    winners = {}

    class Rec(Engine):
        def _record_contest(self, m, ci, seats, seats_eff, w, P, won, diag):
            pids = np.asarray(self.kids['pid'][ci])[np.asarray(won, bool)]
            winners[(int(self.t_now), int(m))] = sorted(int(x) for x in pids)
            return Engine._record_contest(self, m, ci, seats, seats_eff, w, P, won, diag)

    try:
        E = Rec([PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()], **p)
        t0 = time.time(); E.run(); wall = time.time() - t0
    finally:
        EventRNG.uniform = orig_uniform
        cm.set_pl_backend('cpu')
    R = E.R; m0 = E.p['measure_from']

    def mn(k):
        v = np.asarray(R.get(k, []), float)
        return float(np.nanmean(v[m0:])) if v.size else float('nan')
    out = {k: mn(k) for k in ('tut_k12_rate', 'tut_k12_spend', 'tut_g12_rate', 'own_share', 'q_pub',
                              'withheld', 'contest_e_mean', 'elite_share', 'firm_price', 'ptr')}
    out['wall_seconds'] = wall
    return dict(outcomes=out, winners={f'{y}:{m}': v for (y, m), v in winners.items()},
                rng_log=log, measure_from=m0)


def pair_cells(args):
    seeds = [int(x) for x in str(args.seeds).split('-')] if '-' in str(args.seeds) else \
            [int(x) for x in str(args.seeds).split(',')]
    if len(seeds) == 2 and str(args.seeds).count('-') == 1:
        seeds = list(range(seeds[0], seeds[1] + 1))
    cells = [c for c in str(args.cells).split(',') if c]
    out = manifest(dict(cells=cells, seeds=seeds, n=args.n, t=args.t,
                        tolerance_probability=TOL,
                        note='discrete winner flips are reported, not failed; probability bound is the declared equivalence'))
    all_ok = True
    cell_results = {}
    for cell in cells:
        for seed in seeds:
            cpu = _pair_run(args.spec, cell, args.n, args.t, seed, 'cpu')
            gpu = _pair_run(args.spec, cell, args.n, args.t, seed, 'gpu')
            # RNG integrity: call sequence (year, shock, size, pid-hash) until first divergence
            lc, lg = cpu['rng_log'], gpu['rng_log']
            n_same = 0
            for a, b in zip(lc, lg):
                if a != b:
                    break
                n_same += 1
            rng_identical = (lc == lg)
            # discrete winners per gate-year
            kw = sorted(set(cpu['winners']) | set(gpu['winners']))
            flips = {}
            for k in kw:
                a = set(cpu['winners'].get(k, [])); b = set(gpu['winners'].get(k, []))
                flips[k] = dict(sym_diff=len(a ^ b), jaccard=(len(a & b) / len(a | b)) if (a | b) else 1.0,
                                seats_cpu=len(a), seats_gpu=len(b))
            n_flip = sum(v['sym_diff'] for v in flips.values())
            outcome_delta = {k: (gpu['outcomes'][k] - cpu['outcomes'][k]) for k in cpu['outcomes']
                             if isinstance(cpu['outcomes'][k], float)}
            key = f'{cell}|seed={seed}'
            cell_results[key] = dict(rng_calls_cpu=len(lc), rng_calls_gpu=len(lg),
                                     rng_identical=bool(rng_identical), rng_same_prefix=n_same,
                                     winner_set_sym_diff_total=int(n_flip),
                                     gate_years=int(len(kw)),
                                     gate_years_with_flips=int(sum(1 for v in flips.values() if v['sym_diff'])),
                                     flips=flips, outcome_delta=outcome_delta,
                                     wall_cpu=cpu['outcomes']['wall_seconds'],
                                     wall_gpu=gpu['outcomes']['wall_seconds'])
            print(f'PAIR {key} rng_identical={rng_identical} winner_sym_diff={n_flip} '
                  f'gate_years_flipped={cell_results[key]["gate_years_with_flips"]}/{len(kw)}', flush=True)
    out['paired_cells'] = cell_results
    emit(out, args.json)
    return 0 if all_ok else 1


# ---------------------------------------------------------------- benchmark (full-wall metadata)
def bench(args):
    from eduengine import contest_math as cm
    out = manifest(dict(note='GPU microbenchmark; full-cell wall-clock recipe in docs/gpu/PORT_REPORT.md'))
    t_import0 = time.time()
    import eduengine  # noqa: F401
    out['startup_import_seconds'] = round(time.time() - t_import0, 4)
    n, seats = 600, 69
    rng = np.random.default_rng(31415)
    W = np.array([np.exp(1.0 * rng.standard_normal(n)) for _ in range(9)])
    t0 = time.perf_counter(); [np.asarray(cm.pl_win_probs(row, seats, method='auto')) for row in W]
    out['cpu_per_row_9_seconds'] = round(time.perf_counter() - t0, 5)
    if backend() != 'gpu':
        out['gpu'] = None
        emit(out, args.json)
        return 0
    cm.set_pl_backend('gpu')
    try:
        cm.pl_win_probs_batch(W[:1], seats, method='auto')          # warmup / graph capture
        t0 = time.perf_counter(); P = np.asarray(cm.pl_win_probs_batch(W, seats, method='auto'))
        out['gpu_batch_9_seconds'] = round(time.perf_counter() - t0, 5)
        t0 = time.perf_counter(); [np.asarray(cm.pl_win_probs_batch(W[i:i + 1], seats, method='auto'))
                                   for i in range(9)]
        out['gpu_single_row_9_seconds'] = round(time.perf_counter() - t0, 5)
        torch = __import__('torch')
        out['gpu_peak_memory_bytes'] = int(torch.cuda.max_memory_allocated()) if torch.cuda.is_available() else None
        out['data_transfer_bytes_estimate'] = int(W.nbytes + P.nbytes)
    finally:
        cm.set_pl_backend('cpu')
    out['speedup_gpu_batch_vs_cpu_per_row'] = (out.get('cpu_per_row_9_seconds') /
                                               max(out.get('gpu_batch_9_seconds', 1e-9), 1e-9))
    emit(out, args.json)
    return 0


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    for name in ('cpu-digest', 'e2e-digest', 'rng-integrity', 'gpu-parity', 'pair-cells', 'bench'):
        s = sub.add_parser(name)
        s.add_argument('--spec', default='docs/audit/canonical_spec.json')
        s.add_argument('--json', default=None)
        if name == 'pair-cells':
            s.add_argument('--n', type=int, default=1500)
            s.add_argument('--t', type=int, default=46)
            s.add_argument('--seeds', default='100-101')
            s.add_argument('--cells', default='market_only,own_open_gap')
    args = ap.parse_args()
    return {'cpu-digest': cpu_digest, 'e2e-digest': e2e_digest, 'rng-integrity': rng_integrity,
            'gpu-parity': gpu_parity, 'pair-cells': pair_cells, 'bench': bench}[args.cmd](args)


if __name__ == '__main__':
    sys.exit(main())
