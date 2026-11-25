#!/usr/bin/env python3
"""Paper C SCREENING runner — 36-cell orthogonal preregistered grid (screening only; no confirmatory).

SPEC SOURCE (authoritative): docs/audit/PAPER_C_CONFIRMATORY_PREREG.md, FINAL 2026-11-25 —
§1 (design), §8 A1.1/A1.2/A1.7/A1.8 (cells, primaries, contrasts, provenance), §9 A3.1–A3.4 (assertion exemptions,
L bundle, launch manifest). Appendix = the 36-row cell list; this runner generates it in the **appendix row order**.

Cells (36 = 3 S × 2 L × 3 supply × 2 settings):
  S = q0 ∈ {0.85, 1.00, 1.15}                       (school-quality bundle; scales public AND private quality)
  L = G6→G9 contest gate share ∈ {0.25, 0.45}       (share_of='cohort'; gate-level r = 1.2 at L=.25, 1.6 at L=.45;
                                                     the L bundle is fixed jointly by L — no component separation claim)
  supply: A = own_ban 0 / firm_ban 0;  B = own_ban .95 / firm_ban 0;  C = own_ban 0 / firm_ban .9
  settings: P55 = pay_ratio .55, monitoring .2, withhold_mode='pay_gap'
            P12 = pay_ratio 1.2, monitoring .5, withhold_mode='pay_gap'  (prereg Appendix/A3.3; A|P12 is exempt from
                                                                          the binding assertions because its purpose is
                                                                          h=0 under pay_gap. NOTE: a Lead relay message
                                                                          said 'incentive' for P12; the FINAL prereg says
                                                                          pay_gap and A3.3 depends on that. The mode is a
                                                                          top-level constant + manifest field; changing it
                                                                          requires an explicit --p12-incentive override and
                                                                          marks the manifest as a settings override.)
Base: canonical HK params from docs/audit/canonical_spec.json params.HK.primary + canonical gate list, with
gate index 1 (G6→G9) replaced by the contest gate above. N=600, T=46, measure_from=18, seeds 0–7.

Per-run assertions (fail loud, no silent no-op):
  * E.unfired_events == [] (calendar-event validation);
  * EXPOSED arms only (prereg A3.3 + Lead): supply ∈ {A, C} AND settings == P55 → withheld > 1e-3 and own_share > 0.1.
    B (market-only control) and A|P12 (h=0 control) are exempt; their values are still recorded.
  * engine pin: core sha == e111397b…8e71 and spec sha == e5ddef6b… (unless --allow-unpinned, for smoke only).

Outcomes per run (no NaN completion_* fields): K-12 participation/spend; withheld; own_share;
own_share_financial (PROXY: engine lacks contest-only classification, see proxy_flags); Q5−Q1 participation pp gap,
spend gap and spend ratio; own/firm absolute counts+spends as PROXIES (share×attendance / count×price);
by-grade series; realized contest-admission diagnostics per contest gate. All proxy fields carry an explicit flag.

Outputs: per-cell JSONL checkpoints `ckpt_<cellid>.jsonl`, plus `paperC_screening_summary.json` (manifest +
per-cell mean/sd/CI95 over the 8 seeds + all seed rows + invalid-cell report). Screening only:
seeds 100–131 (confirmatory) are rejected by this runner.

Usage (host or box):
  # one cell (smoke or resume a single cell)
  PYTHONPATH=$PWD/engine python papers/shadow-education-contest/code/run_paperC_screening.py cell \
      --id 'S1.00|L0.25|A|P55' --seeds 0-0 --n 60 --out-dir /tmp/paperC_smoke
  # full screening driver (36 cells × seeds 0-7, N=600, T=46)
  PYTHONPATH=$PWD/engine python papers/shadow-education-contest/code/run_paperC_screening.py driver \
      --workers 10 --seeds 0-7 --n 600 --t 46 --out-dir results/paperC_screening
"""
import argparse, hashlib, json, os, subprocess, sys, time, warnings
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, '..', '..', '..'))
ENGINE = os.path.join(REPO, 'engine')
SPEC_PATH = os.path.join(REPO, 'docs', 'audit', 'canonical_spec.json')

# ---- prereg constants (do not edit without a new prereg; Appendix/A3) ------------------------------------------
S_VALUES = (0.85, 1.00, 1.15)
L_VALUES = (0.25, 0.45)
SUPPLIES = {'A': dict(own_ban=0.0, firm_ban=0.0),
            'B': dict(own_ban=0.95, firm_ban=0.0),
            'C': dict(own_ban=0.0, firm_ban=0.9)}
SETTINGS = {'P55': dict(pay_ratio=0.55, monitoring=0.2, withhold_mode='pay_gap'),
            'P12': dict(pay_ratio=1.2, monitoring=0.5, withhold_mode='pay_gap')}
SETTING_ORDER = ('P55', 'P12')
SUPPLY_ORDER = ('A', 'B', 'C')
L_R = {0.25: 1.2, 0.45: 1.6}            # contest_r fixed by L (gate-level r)
DEFAULT_N, DEFAULT_T = 600, 46
SCREENING_SEEDS = tuple(range(0, 8))
CONFIRMATORY_SEEDS = frozenset(range(100, 132))
ENGINE_COMMIT = '846c9e0'
EXPECTED_CORE_SHA = 'e111397bd8a50f94e82bb77715f236ee3d5c0bf863a23d84afdf1c6c71fa8e71'
EXPECTED_SPEC_SHA = 'e5ddef6b4ecd04a0e96f480b43a97f0567bed7654ec032c1779c9e20f6beb755'
LABEL = ('PAPER C SCREENING (36-cell preregistered grid; seeds 0-7 exploratory; N=600/T=46; engine pin 846c9e0) '
         '— screening only, NOT confirmatory')


def sha256(path):
    return hashlib.sha256(open(path, 'rb').read()).hexdigest()


def cell_ids():
    """36 cell ids in the Appendix row order: S, then L, then (A,B,C for P55), then (A,B,C for P12)."""
    ids = []
    for s in S_VALUES:
        for l in L_VALUES:
            for setting in SETTING_ORDER:
                for supply in SUPPLY_ORDER:
                    ids.append(f'S{s:.2f}|L{l:.2f}|{supply}|{setting}')
    assert len(ids) == 36, len(ids)
    return ids


def parse_cell(cid):
    s_, l_, supply, setting = cid.split('|')
    s = float(s_[1:]); l = float(l_[1:])
    if round(s, 2) not in [round(x, 2) for x in S_VALUES]:
        raise ValueError(f'cell {cid}: S must be one of {S_VALUES}')
    if round(l, 2) not in [round(x, 2) for x in L_VALUES]:
        raise ValueError(f'cell {cid}: L must be one of {L_VALUES}')
    if supply not in SUPPLIES or setting not in SETTINGS:
        raise ValueError(f'cell {cid}: unknown supply/setting')
    return s, l, supply, setting


def params_for(cid, n, t, seed, p12_incentive=False):
    s, l, supply, setting = parse_cell(cid)
    spec = json.load(open(SPEC_PATH))
    p = json.loads(json.dumps(spec['params']['HK']['primary']))
    p.update(N=int(n), T=int(t), seed=int(seed), measure_from=min(int(spec['params']['HK']['primary'].get('measure_from', 18)), int(t) // 2))
    p['q0'] = float(s)
    p.update(SUPPLIES[supply])
    p.update(SETTINGS[setting])
    if setting == 'P12' and p12_incentive:
        p['withhold_mode'] = 'incentive'
    gates = json.loads(json.dumps(p['gates']))
    gates[1] = dict(kind='contest', share=float(l), share_of='cohort', r=float(L_R[round(l, 2)]), fail='stop')
    p['gates'] = gates
    return p


def _mean_series(R, key, m):
    import numpy as np
    return float(np.nanmean(np.asarray(R[key], float)[m:]))


def run_seed(cid, seed, n, t, p12_incentive=False, allow_unpinned=False):
    warnings.filterwarnings('ignore')
    sys.path.insert(0, ENGINE)
    import numpy as np
    from eduengine.core import Engine
    from eduengine.modules.labour import QueueLabour
    from eduengine.modules.schools import PrivateSchools, PublicSchools
    from eduengine.modules.sdg4 import SDG4
    from eduengine.modules.tutoring import TutoringMarket

    core_sha = sha256(os.path.join(ENGINE, 'eduengine', 'core.py'))
    spec_sha = sha256(SPEC_PATH)
    if not allow_unpinned:
        assert core_sha == EXPECTED_CORE_SHA, f'engine core sha {core_sha} != canonical pin {EXPECTED_CORE_SHA}'
        assert spec_sha == EXPECTED_SPEC_SHA, f'spec sha {spec_sha} != canonical {EXPECTED_SPEC_SHA}'

    p = params_for(cid, n, t, seed, p12_incentive=p12_incentive)
    t0 = time.time()
    E = Engine([PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()], **p)
    E.run()
    wall = time.time() - t0
    if getattr(E, 'unfired_events', []):
        raise RuntimeError(f'{cid} seed {seed}: unfired calendar events {E.unfired_events}')
    s_, l, supply, setting = parse_cell(cid)
    if supply in ('A', 'C') and setting == 'P55':       # exposed arms only (prereg A3.3 + Lead)
        h = _mean_series(E.R, 'withheld', E.p['measure_from'])
        own = _mean_series(E.R, 'own_share', E.p['measure_from'])
        if not (h > 1e-3):
            raise RuntimeError(f'INVALID exposed arm {cid} seed {seed}: withheld={h!r} <= 1e-3 (no withholding)')
        if not (own > 0.1):
            raise RuntimeError(f'INVALID exposed arm {cid} seed {seed}: own_share={own!r} <= 0.1 (no own-teacher supply)')

    R = E.R; m = int(E.p['measure_from'])
    rate_q = np.nanmean(np.asarray(R['tut_k12_rate_by_q'], float)[m:], axis=0)
    spend_q = np.nanmean(np.asarray(R['tut_k12_spend_by_q'], float)[m:], axis=0)
    att = np.asarray(R['att_by_grade'], float)[m:]                 # years x grades (same index as tut_own_by_grade)
    own_by = np.asarray(R['tut_own_by_grade'], float)[m:]
    firm_by = np.asarray(R['tut_firm_by_grade'], float)[m:]
    k12 = slice(0, min(12, att.shape[1]))                         # primary+lower+upper grades = 0..11
    own_cnt = np.sum(own_by[:, k12] * att[:, k12], axis=1)
    firm_cnt = np.sum(firm_by[:, k12] * att[:, k12], axis=1)
    fp = np.asarray(R['firm_price'], float)[m:]
    p_own = float(E.p['p_own'])
    own_cnt_m = float(np.nanmean(own_cnt)); firm_cnt_m = float(np.nanmean(firm_cnt))
    contests = list(getattr(E, 'contest_gates', []))
    cont = {}
    for m_, gt in contests:
        cont[str(m_)] = dict(
            admit_rate=float(np.nanmean(np.asarray(R['contest_admit_rate'], float)[m:, m_])),
            candidates=float(np.nanmean(np.asarray(R['contest_candidates'], float)[m:, m_])),
            seats=float(np.nanmean(np.asarray(R['contest_seats'], float)[m:, m_])),
            expected_p_mean=float(np.nanmean(np.asarray(R['contest_expected_p_mean'], float)[m:, m_])))
    row = dict(
        cid=cid, S=s_, L=l, supply=supply, settings=setting, seed=int(seed), N=int(n), T=int(t),
        measure_from=m, wall_seconds=round(wall, 4),
        # primary/secondary outcomes (screening)
        tut_k12_rate=_mean_series(R, 'tut_k12_rate', m),
        tut_k12_spend=_mean_series(R, 'tut_k12_spend', m),
        tut_rate=_mean_series(R, 'tut_rate', m),
        withheld=_mean_series(R, 'withheld', m),
        own_share=_mean_series(R, 'own_share', m),
        own_share_financial_proxy=float(own_cnt_m / max(own_cnt_m + firm_cnt_m, 1e-12)),
        q5_q1_part_gap_pp=float(100.0 * (rate_q[4] - rate_q[0])),
        q5_q1_spend_gap=float(spend_q[4] - spend_q[0]),
        q5_q1_spend_ratio=float(spend_q[4] / max(spend_q[0], 1e-9)),
        own_count_proxy_k12=own_cnt_m,
        firm_count_proxy_k12=firm_cnt_m,
        own_spend_proxy_k12=own_cnt_m * p_own,
        firm_spend_proxy_k12=firm_cnt_m * float(np.nanmean(fp)),
        tut_by_grade=[float(x) for x in np.nanmean(np.asarray(R['tut_by_grade'], float)[m:], axis=0)],
        tut_own_by_grade=[float(x) for x in np.nanmean(own_by, axis=0)],
        tut_firm_by_grade=[float(x) for x in np.nanmean(firm_by, axis=0)],
        q_pub=_mean_series(R, 'q_pub', m), ptr=_mean_series(R, 'ptr', m),
        teacher_pay=_mean_series(R, 'teacher_pay', m), priv_share=_mean_series(R, 'priv_share', m),
        firm_price=float(np.nanmean(fp)),
        contest_admission_by_gate=cont,
        unfired_events=list(getattr(E, 'unfired_events', [])),
        assertions=dict(exposed=(supply in ('A', 'C') and setting == 'P55'), checked=True),
        params={k: p[k] for k in ('N', 'T', 'measure_from', 'seed', 'q0', 'own_ban', 'firm_ban', 'pay_ratio',
                                  'monitoring', 'withhold_mode', 'contest_r')},
        gate=p['gates'][1],
        proxy_flags=dict(
            own_share_financial='PROXY: own/(own+firm) from per-grade shares; engine has no contest-only '
                                'classification, so firm series includes contest-prep pupils (declared contamination)',
            absolute_counts='PROXY: per-grade tutoring share x attending pupils (grades 0-11), mean over window',
            absolute_spends='PROXY: own count x p_own; firm count x mean firm_price (firm series contaminated)'),
        engine=dict(commit=ENGINE_COMMIT, core_sha=core_sha, spec_sha=spec_sha),
    )
    return row


# ---------------------------------------------------------------- cell + driver
def _ckpt_path(out_dir, cid):
    return os.path.join(out_dir, 'ckpt_' + cid.replace('|', '_') + '.jsonl')


def run_cell(cid, seeds, n, t, out_dir, p12_incentive=False, allow_unpinned=False):
    os.makedirs(out_dir, exist_ok=True)
    ck = _ckpt_path(out_dir, cid)
    done = set()
    if os.path.exists(ck):
        for line in open(ck):
            try:
                done.add(int(json.loads(line)['seed']))
            except Exception:
                pass
    for sd in seeds:
        if sd in done:
            continue
        row = run_seed(cid, sd, n, t, p12_incentive=p12_incentive, allow_unpinned=allow_unpinned)
        with open(ck, 'a') as f:
            f.write(json.dumps(row) + '\n'); f.flush(); os.fsync(f.fileno())
    return ck


def _read_cell(out_dir, cid):
    ck = _ckpt_path(out_dir, cid)
    if not os.path.exists(ck):
        return []
    rows = []
    for line in open(ck):
        try:
            rows.append(json.loads(line))
        except Exception:
            pass
    return rows


def _stat(v):
    import numpy as np
    a = np.asarray([x for x in v if isinstance(x, (int, float)) and (x == x)], float)
    if a.size == 0:
        return dict(mean=None, sd=None, ci95_lo=None, ci95_hi=None, n=0)
    mean = float(a.mean()); sd = float(a.std(ddof=1)) if a.size > 1 else 0.0
    se = sd / (a.size ** 0.5)
    return dict(mean=mean, sd=sd, ci95_lo=mean - 1.96 * se, ci95_hi=mean + 1.96 * se, n=int(a.size))


METRICS = ('tut_k12_rate', 'tut_k12_spend', 'tut_rate', 'withheld', 'own_share', 'own_share_financial_proxy',
           'q5_q1_part_gap_pp', 'q5_q1_spend_gap', 'q5_q1_spend_ratio', 'own_count_proxy_k12',
           'firm_count_proxy_k12', 'own_spend_proxy_k12', 'firm_spend_proxy_k12', 'q_pub', 'ptr',
           'teacher_pay', 'priv_share', 'firm_price')


def _engine_file_hashes():
    files = {}
    for rel in ('core.py', 'rng.py', 'contest_math.py', 'planning.py', 'modules/labour.py',
                'modules/schools.py', 'modules/sdg4.py', 'modules/tutoring.py', 'modules/state.py'):
        fp = os.path.join(ENGINE, 'eduengine', rel)
        if os.path.exists(fp):
            files['engine/eduengine/' + rel] = sha256(fp)
    return files


def _manifest(ids, seeds, n, t, workers, out_dir, p12_incentive, runner_sha, analysis_commit=''):
    core_sha = sha256(os.path.join(ENGINE, 'eduengine', 'core.py'))
    return dict(label=LABEL, status='SCREENING-ONLY', prereg='docs/audit/PAPER_C_CONFIRMATORY_PREREG.md',
                engine_commit=ENGINE_COMMIT, core_sha256=core_sha, spec_sha256=sha256(SPEC_PATH),
                engine_file_sha256=_engine_file_hashes(),
                runner_sha256=runner_sha, analysis_commit=analysis_commit or None,
                fail_routing='cell assertion/failure aborts that cell (nonzero); driver records INVALID cells, '
                             'preserves checkpoints, writes summary, exits 2 if any invalid; no silent drop',
                cells=ids, n_cells=len(ids), seeds=list(seeds), n=int(n), t=int(t), workers=workers,
                settings=dict(P55=SETTINGS['P55'], P12=dict(SETTINGS['P12'], withhold_mode=(
                    'incentive' if p12_incentive else SETTINGS['P12']['withhold_mode']))),
                settings_note=('prereg Appendix/A3.3 define P12 withhold_mode=pay_gap; --p12-incentive overrides to '
                               'incentive and marks this manifest as a SETTINGS OVERRIDE'),
                p12_incentive_override=bool(p12_incentive),
                supplies=SUPPLIES, L_values=list(L_VALUES), L_r=L_R, S_values=list(S_VALUES),
                seeds_rule='0-7 exploratory/screening; confirmatory 100-131 rejected by this runner',
                assertions='exposed arms (supply A/C & P55): withheld>1e-3 and own_share>0.1; B and A|P12 exempt; '
                           'E.unfired_events==[] every run',
                proxy_flags='own_share_financial, absolute counts/spends are PROXIES (see per-row proxy_flags)',
                started_utc=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), out_dir=os.path.abspath(out_dir))


def driver(args):
    for sd in args.seeds:
        if sd in CONFIRMATORY_SEEDS:
            raise SystemExit(f'screening runner refuses confirmatory seeds (got {sd}); use 0-7 only')
    ids = cell_ids()
    if args.cells:
        requested = [c for c in args.cells.split(',') if c]
        missing = [c for c in requested if c not in ids]
        if missing:
            raise SystemExit(f'unknown/non-preregistered cells: {missing}')
        ids = [c for c in ids if c in requested]          # keep appendix order
        if not args.allow_subset:
            raise SystemExit('subset selection requires --allow-subset (screening must run all 36 cells; '
                             'no post-hoc cells)')
    runner_sha = sha256(os.path.abspath(__file__))
    os.makedirs(args.out_dir, exist_ok=True)
    t_start = time.time()
    failures = {}

    def launch(cid):
        r = subprocess.run([sys.executable, os.path.abspath(__file__), 'cell', '--id', cid,
                            '--seeds', f'{args.seeds[0]}-{args.seeds[-1]}', '--n', str(args.n), '--t', str(args.t),
                            '--out-dir', args.out_dir] + (['--p12-incentive'] if args.p12_incentive else []) +
                           (['--allow-unpinned'] if args.allow_unpinned else []),
                           capture_output=True, text=True,
                           env=dict(os.environ, PYTHONPATH=ENGINE, OPENBLAS_NUM_THREADS='1',
                                    MKL_NUM_THREADS='1', OMP_NUM_THREADS='1'))
        if r.returncode != 0:
            failures[cid] = (r.stderr or r.stdout)[-1500:]
        return cid
    with ThreadPoolExecutor(max_workers=max(1, int(args.workers))) as ex:
        list(ex.map(launch, ids))
    wall = time.time() - t_start

    # aggregate: per-cell stats over the requested seeds; incomplete/invalid cells reported, never dropped
    summary = {}
    invalid = []
    for cid in ids:
        rows = _read_cell(args.out_dir, cid)
        seeds_got = sorted({int(r['seed']) for r in rows})
        if cid in failures:
            invalid.append(dict(cid=cid, reason='cell failed', stderr=failures[cid]))
            continue
        if seeds_got != list(args.seeds):
            invalid.append(dict(cid=cid, reason=f'incomplete seeds {seeds_got} != {list(args.seeds)}'))
        summary[cid] = dict(seed_stats={k: _stat([r[k] for r in rows]) for k in METRICS if rows and k in rows[0]},
                            n_seeds=len(seeds_got), rows=rows)
    payload = dict(
        manifest=_manifest(ids, list(args.seeds), args.n, args.t, args.workers, args.out_dir,
                           args.p12_incentive, runner_sha, args.analysis_commit),
        wall_seconds=round(wall, 2),
        n_cells=len(ids), n_runs=sum(len(v['rows']) for v in summary.values()),
        invalid_cells=invalid, cells=summary,
        checkpoint_sha256={cid: sha256(_ckpt_path(args.out_dir, cid))
                           for cid in ids if os.path.exists(_ckpt_path(args.out_dir, cid))})
    out = os.path.join(args.out_dir, 'paperC_screening_summary.json')
    tmp = out + '.tmp'
    json.dump(payload, open(tmp, 'w'), indent=1, default=float)
    os.replace(tmp, out)
    print(f'wrote {out} sha256={sha256(out)} runs={payload["n_runs"]} invalid={len(invalid)} wall={wall:.1f}s')
    if invalid:
        print('INVALID cells:', json.dumps([v['cid'] for v in invalid]))
        return 2
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    sub = ap.add_subparsers(dest='cmd', required=True)
    c = sub.add_parser('cell'); c.add_argument('--id', required=True); c.add_argument('--seeds', default='0-7')
    c.add_argument('--n', type=int, default=DEFAULT_N); c.add_argument('--t', type=int, default=DEFAULT_T)
    c.add_argument('--out-dir', required=True); c.add_argument('--p12-incentive', action='store_true')
    c.add_argument('--allow-unpinned', action='store_true')
    d = sub.add_parser('driver'); d.add_argument('--workers', type=int, default=10)
    d.add_argument('--seeds', default='0-7'); d.add_argument('--n', type=int, default=DEFAULT_N)
    d.add_argument('--t', type=int, default=DEFAULT_T); d.add_argument('--out-dir', required=True)
    d.add_argument('--cells', default=None); d.add_argument('--allow-subset', action='store_true')
    d.add_argument('--p12-incentive', action='store_true'); d.add_argument('--allow-unpinned', action='store_true')
    d.add_argument('--analysis-commit', default='')
    a = ap.parse_args()
    if a.cmd == 'driver':
        a.seeds = list(range(int(a.seeds.split('-')[0]), int(a.seeds.split('-')[1]) + 1)) if '-' in a.seeds else \
                  [int(x) for x in a.seeds.split(',')]
        return driver(a)
    seeds = list(range(int(a.seeds.split('-')[0]), int(a.seeds.split('-')[1]) + 1)) if '-' in a.seeds else \
            [int(x) for x in a.seeds.split(',')]
    if any(s in CONFIRMATORY_SEEDS for s in seeds):
        raise SystemExit('screening runner refuses confirmatory seeds (100-131); use 0-7 only')
    ck = run_cell(a.id, seeds, a.n, a.t, a.out_dir, p12_incentive=a.p12_incentive, allow_unpinned=a.allow_unpinned)
    print(f'checkpoint {ck} sha256={sha256(ck)}')
    return 0


if __name__ == '__main__':
    sys.exit(main())
