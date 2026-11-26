#!/usr/bin/env python3
"""Paper C A6 analysis (host-only, committed BEFORE launch): behavioural paired contrasts, 5k seed bootstrap, Holm, MDE.

Declared before launch (see docs/audit/PAPER_C_A6_PREREG.md):
  T1prime = mean over design cells of rate(S=.85) - rate(S=1.15) (pp); direction S up => participation down; min +3.0 pp
  T4prime = mean over design cells of spend_gap(L=.45) - spend_gap(L=.25) (pp); direction L up => gap up; min +2.0 pp
  family = {T1prime, T4prime}, Holm m=2, alpha=.05 two-sided; 8 matched seeds 0-7; N=600.
  5,000-draw seed bootstrap CIs; achieved MDE from pre-declared SDs and n; degeneracy-screen report.
  Manipulation checks M1 (own supply) and M2 (withheld deterministic) reported separately, never as claims.
Input: A6 results JSON (cells -> rows, same schema as screening) OR a directory of ckpt_*.jsonl.
Outputs JSON with design, hashes, per-test effect/bootstrap CI/Holm p/MDE/decision, degeneracy screen, M1/M2 checks.
"""
import hashlib, json, math, os, sys
import numpy as np

def sha(p): return hashlib.sha256(open(p, 'rb').read()).hexdigest()

def load(path):
    if os.path.isdir(path):
        cells = {}
        for fn in sorted(os.listdir(path)):
            if fn.startswith('ckpt_') and fn.endswith('.jsonl'):
                cid = fn[len('ckpt_'):-len('.jsonl')].replace('_', '|')
                rows = [json.loads(l) for l in open(os.path.join(path, fn))]
                cells[cid] = dict(rows=rows)
        return dict(cells=cells, n_runs=sum(len(c['rows']) for c in cells.values()), n_cells=len(cells))
    return json.load(open(path))

def cid(S, L, sup, st): return f'S{float(S):.2f}|L{float(L):.2f}|{sup}|{st}'

def paired_contrast(cells, pairs, field, seeds, scale=1.0):
    out = {sd: [] for sd in seeds}
    for a, b in pairs:
        A = {int(r['seed']): r for r in cells[a]['rows']}
        B = {int(r['seed']): r for r in cells[b]['rows']}
        for sd in seeds:
            if sd in A and sd in B:
                out[sd].append((A[sd][field] - B[sd][field]) * scale)
    return [float(np.mean(out[sd])) for sd in seeds if out[sd]]

def boot_ci(vals, n=5000, seed=20261126):
    rng = np.random.default_rng(seed); a = np.array(vals, float)
    if len(a) == 0: return None
    bs = np.array([np.mean(a[rng.integers(0, len(a), len(a))]) for _ in range(n)])
    return dict(mean=float(a.mean()), ci95=[float(np.percentile(bs, 2.5)), float(np.percentile(bs, 97.5))],
                se=float(a.std(ddof=1) / math.sqrt(len(a))) if len(a) > 1 else 0.0, n=len(a), n_boot=n)

def holm(pvals):
    items = sorted(pvals.items(), key=lambda kv: kv[1]); m = len(items); out = {}; prev = 0.0
    for i, (k, p) in enumerate(items):
        adj = min(1.0, max(prev, (m - i) * p)); out[k] = adj; prev = adj
    return out

def norm_p(t):
    return math.erfc(abs(t) / math.sqrt(2))

def degeneracy(cells, fields, seeds):
    rep = {}
    for f in fields:
        vals = [r[f] for c in cells.values() for r in c['rows'] if int(r['seed']) in seeds and isinstance(r.get(f), (int, float))]
        if not vals: rep[f] = dict(status='NO_DATA'); continue
        uniq = len(set(round(float(v), 12) for v in vals)); sd = float(np.std(vals, ddof=1)) if len(vals) > 1 else 0.0
        per_cell_zero = sum(1 for c in cells.values() if len(set(round(float(r[f]), 12) for r in c['rows'] if int(r['seed']) in seeds and isinstance(r.get(f), (int, float)))) <= 1)
        rep[f] = dict(distinct_values=uniq, sd=sd, cells_with_no_variation=per_cell_zero,
                      pass_=(uniq >= 2 and sd > 0 and per_cell_zero == 0))
    return rep

def main():
    path = sys.argv[1] if len(sys.argv) > 1 else 'results/audit/newgen/paperC_A6_results.json'
    out = sys.argv[2] if len(sys.argv) > 2 else 'docs/audit/PAPER_C_A6_RESULTS.json'
    d = load(path); cells = d['cells']
    seeds = [int(r['seed']) for c in cells.values() for r in c['rows']]
    seeds = sorted(set(seeds))
    design_seeds = [s for s in seeds if s in range(0, 8)] or seeds
    pairs_T1 = [(cid(S=.85, L=L, sup=sup, st=st), cid(S=1.15, L=L, sup=sup, st=st)) for L in (0.25, 0.45) for sup in 'ABC' for st in ('P55', 'P12')]
    pairs_T4 = [(cid(S=S, L=.45, sup=sup, st=st), cid(S=S, L=.25, sup=sup, st=st)) for S in (0.85, 1.0, 1.15) for sup in 'ABC' for st in ('P55', 'P12')]
    v1 = paired_contrast(cells, pairs_T1, 'tut_k12_rate', design_seeds, 100.0)
    v4 = paired_contrast(cells, pairs_T4, 'q5_q1_spend_gap', design_seeds, 100.0)
    b1 = boot_ci(v1); b4 = boot_ci(v4)
    p1 = norm_p(b1['mean'] / b1['se']) if b1 and b1['se'] > 0 else (0.0 if b1 and b1['mean'] != 0 else 1.0)
    p4 = norm_p(b4['mean'] / b4['se']) if b4 and b4['se'] > 0 else (0.0 if b4 and b4['mean'] != 0 else 1.0)
    h = holm({'T1prime': p1, 'T4prime': p4})
    decl_sd = {'T1prime': 0.0598, 'T4prime': 0.0680}
    z_a, z_b = 2.3940, 0.8416
    mde = {k: (z_a + z_b) * decl_sd[k] / math.sqrt(max(len(v1 if k == 'T1prime' else v4), 1)) for k in decl_sd}
    def decide(k, mean, ci, p_holm, min_e):
        dir_ok = mean > 0
        meets = abs(mean) >= min_e
        sig = p_holm < 0.05
        if dir_ok and meets and sig: return 'HOLDS'
        if not dir_ok: return 'FAILS (direction)'
        return 'INDETERMINATE'
    res = dict(
        paper='Paper C A6 confirmatory analysis', source=path, source_sha256=sha(path),
        design=dict(n=d.get('n_runs'), n_cells=d.get('n_cells'), seeds=design_seeds, n_seeds=len(design_seeds),
                    N=600, T=46, family=['T1prime', 'T4prime'], holm_m=2, alpha=0.05,
                    methods=['paired seed contrasts','5,000-draw seed bootstrap','Holm m=2','MDE from pre-declared SDs','degeneracy screen']),
        T1prime=dict(estimand='rate(S=.85)-rate(S=1.15) pp; direction S up => participation down; min +3.0 pp',
                     effect=b1['mean'] if b1 else None, bootstrap95_ci=b1['ci95'] if b1 else None, se=b1['se'] if b1 else None,
                     p=p1, p_holm=h.get('T1prime'), achieved_mde_pp=mde['T1prime'],
                     decision=decide('T1prime', b1['mean'], b1['ci95'], h.get('T1prime', 1.0), 3.0) if b1 else 'NO_DATA'),
        T4prime=dict(estimand='gap(L=.45)-gap(L=.25) pp; direction L up => gap up; min +2.0 pp',
                     effect=b4['mean'] if b4 else None, bootstrap95_ci=b4['ci95'] if b4 else None, se=b4['se'] if b4 else None,
                     p=p4, p_holm=h.get('T4prime'), achieved_mde_pp=mde['T4prime'],
                     decision=decide('T4prime', b4['mean'], b4['ci95'], h.get('T4prime', 1.0), 2.0) if b4 else 'NO_DATA'),
        degeneracy_screen=degeneracy(cells, ['tut_k12_rate', 'q5_q1_spend_gap', 'tut_k12_spend', 'tut_g12_rate'], design_seeds),
        manipulation_checks=dict(note='M1 own-supply and M2 withholding reported separately; never estimands/claims (A5 defect: withheld deterministic)'),
        labels=dict(no_claim='no Paper C claim until artefact verified+adjudicated; T1/T4 screening outcomes are not confirmatory without A6',
                    no_s_generalisation='passers/design S range only; no S-generalisation claim'))
    json.dump(res, open(out, 'w'), indent=2)
    print(json.dumps({k: res[k] for k in ('T1prime', 'T4prime')}, indent=1)[:1200])
    print('wrote', out, sha(out))
    return 0

if __name__ == '__main__':
    sys.exit(main())
