#!/usr/bin/env python3
"""Paper C CONFIRMATORY (A5 16-seed interim) — aggregate per-cell checkpoints, seeds 100-115 only.

Writes paperC_confirmatory.json (screening-schema-compatible summary), SHA256SUMS, CONFIRM_RESULTS_DONE.
A5 rule: exactly 16 matched seeds 100-115; 116-131 excluded; no outcome-based selection.
"""
import hashlib, json, os, sys

D = sys.argv[1] if len(sys.argv) > 1 else '/root/work/paperC/confirm_final'
SEEDS = list(range(100, 116))
EXCLUDED = list(range(116, 132))
REPO = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', '..'))
RUNNER = os.path.join(REPO, 'papers', 'shadow-education-contest', 'code', 'run_paperC_screening.py')
SPEC = os.path.join(REPO, 'docs', 'audit', 'canonical_spec.json')

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

META = {'cid', 'S', 'L', 'supply', 'settings', 'seed', 'N', 'T', 'measure_from', 'wall_seconds', 'unfired_events',
        'assertions', 'params', 'gate', 'proxy_flags', 'engine', 'tut_by_grade', 'tut_own_by_grade', 'tut_firm_by_grade',
        'contest_admission_by_gate'}

def stat(vals):
    import numpy as np
    a = np.array(vals, float); n = len(a)
    if n == 0: return None
    m = float(np.nanmean(a)); sd = float(np.nanstd(a, ddof=1)) if n > 1 else 0.0
    se = sd / np.sqrt(max(n, 1))
    return dict(mean=m, sd=sd, ci95_lo=m - 1.96 * se, ci95_hi=m + 1.96 * se, n=n)

cells, allrows, invalid = {}, [], []
for fn in sorted(os.listdir(D)):
    if not (fn.startswith('ckpt_') and fn.endswith('.jsonl')): continue
    cid = '_'.join(fn[len('ckpt_'):-len('.jsonl')].split('_'))
    cid = fn[len('ckpt_'):-len('.jsonl')].replace('_', '|')
    rows = [json.loads(l) for l in open(os.path.join(D, fn))]
    rows = [r for r in rows if int(r['seed']) in SEEDS]
    rows.sort(key=lambda r: r['seed'])
    if len(rows) < 16: invalid.append(dict(cell=cid, reason=f'only {len(rows)}/16 seeds'))
    metrics = {}
    for r in rows:
        for k, v in r.items():
            if k in META: continue
            if isinstance(v, (int, float)) and v is not None: metrics.setdefault(k, []).append(v)
    ss = {k: stat(v) for k, v in metrics.items()}
    cells[cid] = dict(seed_stats=ss, n_seeds=len(rows), rows=rows)
    allrows.extend(rows)

summary = {cid: {k: v for k, v in c['seed_stats'].items()} for cid, c in cells.items()}
payload = dict(
    label='PAPER C CONFIRMATORY — A5 16-SEED INTERIM (frozen 6 passers; seeds 100-115; N=1500/T=46; engine 846c9e0)',
    manifest=dict(status='CONFIRMATORY A5 INTERIM', stage='confirmatory', prereg='docs/audit/PAPER_C_CONFIRMATORY_PREREG.md',
                  prereg_sha256='445ec423c03ffdc8521a820694a72662cabbe342331dc1c8a839023e00053a8d',
                  a4='docs/audit/PAPER_C_A4_P12_CLARIFICATION.md', a4_sha256='8c967eabe5d007485ec1fe4a4a28735beeeabeee40c064eb67996c731fcc1ea3',
                  a5='docs/audit/PAPER_C_A5_SEED_TRUNCATION.md', a5_sha256='365155965423b4f9171b5ad69a87dd0ef11c0710b5216190d043beebfb16bf99',
                  a5_adjudication='1c51f17', passers_sha256='b64a69f0391d0089b535b6e43cfd2a55680f6c812159c3f0e37efc6ba95b99e7',
                  screening_source_sha256='6bcc29a50d41dc2c63a5959c0b023eb203c5bf1bd0cd04ffaee908a5ebb5b6d4',
                  runner='papers/shadow-education-contest/code/run_paperC_screening.py', runner_sha256=sha(RUNNER),
                  engine_commit='846c9e0', core_sha256='e111397bd8a50f94e82bb77715f236ee3d5c0bf863a23d84afdf1c6c71fa8e71',
                  spec_sha256=sha(SPEC), cells=sorted(cells), n_cells=len(cells), seeds=SEEDS, n_seeds=16,
                  excluded_seeds=EXCLUDED, n=1500, t=46, holm_family=['T2', 'T3'], holm_m=2, alpha=0.05,
                  t1_t4_status='screening failures; not confirmatorily tested',
                  p12_mode='pay_gap (no-withholding control, A4)', gate=dict(index=1, kind='contest', share_of='cohort', r_by_L={'0.25': 1.2, '0.45': 1.6}, fail='stop'),
                  precision='A5 interim: 16 matched seeds; SE = sqrt(2) x the 32-seed plan; no full-precision claim',
                  assertions='exposed arms A/C & P55: withheld>1e-3, own_share>0.1; B and A|P12 exempt; unfired_events==[] per run',
                  no_s_generalisation='all passers S=0.85; no S-generalisation claim'),
    wall_seconds=None, n_cells=len(cells), n_runs=len(allrows), invalid_cells=invalid,
    cells=cells, summary=summary,
    checkpoint_sha256={fn: sha(os.path.join(D, fn)) for fn in sorted(os.listdir(D)) if fn.startswith('ckpt_') and fn.endswith('.jsonl')},
)
OUT = os.path.join(D, 'paperC_confirmatory.json')
json.dump(payload, open(OUT, 'w'), indent=2)
with open(os.path.join(D, 'SHA256SUMS'), 'w') as f:
    for fn in sorted(os.listdir(D)):
        p = os.path.join(D, fn)
        if os.path.isfile(p) and fn != 'SHA256SUMS': f.write(f'{sha(p)}  {fn}\n')
open(os.path.join(D, 'CONFIRM_RESULTS_DONE'), 'w').write('done\n')
print(json.dumps(dict(n_runs=payload['n_runs'], n_cells=payload['n_cells'], invalid=invalid, sha=sha(OUT)), indent=1))
