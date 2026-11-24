#!/usr/bin/env python3
"""Q3 job 1: known-truth calibration of the actual grouping-multiverse verdict rule.

Extends Sonnet's known_truth_sim.py (committed alongside as scripts/known_truth_sim_orig.py):
- independent seed per replicate;
- BEATS tier (share-level BH at 5% against the random-draw null) added, so all four paper
  verdict tiers are represented;
- strength ladder, minority-only, shared-trend and sign-split regimes;
- Wilson 95% intervals, and a design-size grid (N, T) plus a draw-count axis (R) to separate
  Monte Carlo uncertainty from mechanism/sample-size uncertainty;
- vectorised random-partition statistics (same math as the original loop; a self-test compares
  the two on a few replicates).

Pre-registered in PRE_REGISTRATION.md (committed before this file). Single process, thread caps.
"""
import os
for _v in ("OMP_NUM_THREADS", "OPENBLAS_NUM_THREADS", "MKL_NUM_THREADS"):
    os.environ[_v] = "1"
import json, sys, argparse
import numpy as np
from scipy.stats import chi2
from collections import Counter

REPS_MAIN = 400
REPS_GRID = 200
R_MAIN = 400
N_DEFAULT, T_DEFAULT = 150, 50
CUTS = [2, 3]
NFAM = 4
SEED_BASE = 20261125


def ar1(rng, shape, rho, sd):
    e = rng.normal(size=shape)
    out = np.empty(shape)
    out[..., 0] = e[..., 0]
    for k in range(1, shape[-1]):
        out[..., k] = rho * out[..., k - 1] + np.sqrt(1 - rho ** 2) * e[..., k]
    return sd * out


def make_panel(regime, rng, N, T, b=None):
    tt = np.arange(T, dtype=float)
    common = rng.normal(size=(N, 1))
    L = 0.5 * common + rng.normal(size=(N, NFAM))
    d = rng.normal(size=N)
    ex = ar1(rng, (N, T), 0.6, 1.0)
    ey = ar1(rng, (N, T), 0.6, 1.5)
    if regime == 'D':
        sx, sy = 0.05 * d, 0.05 * d
    else:
        sx, sy = 0.05 * rng.normal(size=N), 0.05 * rng.normal(size=N)
    bb = np.zeros(N)
    if regime == 'U':
        bb[:] = b
    elif regime == 'B':
        bb[L[:, 0] > np.quantile(L[:, 0], 2 / 3)] = b
    elif regime == 'S':
        bb[L[:, 1] > np.median(L[:, 1])] = 0.25
        bb[L[:, 1] <= np.median(L[:, 1])] = -0.25
    x = rng.normal(size=(N, 1)) + sx[:, None] * tt + ex
    y = rng.normal(size=(N, 1)) + sy[:, None] * tt + bb[:, None] * (sx[:, None] * tt + ex) + ey
    return x, y, L


def suff(x, y, spec, T):
    if spec == 'FE':
        X = x - x.mean(1, keepdims=True)
        Y = y - y.mean(1, keepdims=True)
    else:
        tt = np.arange(T, dtype=float)
        A = np.stack([np.ones(T), tt], 1)
        P = A @ np.linalg.solve(A.T @ A, A.T)
        X = x - x @ P
        Y = y - y @ P
    return (X * X).sum(1), (X * Y).sum(1)


def labels_for(L):
    labs, fam = [], []
    for f in range(NFAM):
        for c in CUTS:
            q = np.quantile(L[:, f], np.linspace(0, 1, c + 1)[1:-1])
            lab = np.searchsorted(q, L[:, f])
            labs.append(lab)
            fam.extend([f] * (lab.max() + 1))
    return labs, np.array(fam)


def indicator(lab, N):
    k = lab.max() + 1
    M = np.zeros((N, k))
    M[np.arange(N), lab] = 1.0
    return M


def group_t(sxx, sxy, lab):
    k = lab.max() + 1
    S = np.bincount(lab, sxx, k)
    Sy = np.bincount(lab, sxy, k)
    b = Sy / S
    sc2 = np.bincount(lab, sxy ** 2, k) - 2 * b * np.bincount(lab, sxx * sxy, k) + b ** 2 * np.bincount(lab, sxx ** 2, k)
    g = np.bincount(lab, minlength=k)
    se = np.sqrt(np.maximum(sc2, 1e-12) * g / (g - 1)) / S
    return b / se


def het_p(sxx, sxy, lab):
    k = lab.max() + 1
    S = np.bincount(lab, sxx, k)
    Sy = np.bincount(lab, sxy, k)
    b = Sy / S
    sc2 = np.bincount(lab, sxy ** 2, k) - 2 * b * np.bincount(lab, sxx * sxy, k) + b ** 2 * np.bincount(lab, sxx ** 2, k)
    g = np.bincount(lab, minlength=k)
    v = np.maximum(sc2, 1e-12) * g / (g - 1) / S ** 2
    w = 1 / v
    bw = (w * b).sum() / w.sum()
    Q = (w * (b - bw) ** 2).sum()
    return float(chi2.sf(Q, k - 1))


def rand_stats(sxx, sxy, lab, perms):
    """Vectorised group t for R random permutations: perms shape (R, N)."""
    R, N = perms.shape
    M = indicator(lab, N)
    Sp = sxx[perms] @ M
    Syp = sxy[perms] @ M
    b = Syp / Sp
    q2 = (sxy ** 2)[perms] @ M
    q1 = (sxx * sxy)[perms] @ M
    q0 = (sxx ** 2)[perms] @ M
    sc2 = q2 - 2 * b * q1 + b ** 2 * q0
    g = M.sum(0)
    se = np.sqrt(np.maximum(sc2, 1e-12) * g / (g - 1)) / Sp
    return b / se, b, sc2, Sp, g


def rand_het(sxx, sxy, lab, perms):
    tstat, b, sc2, Sp, g = rand_stats(sxx, sxy, lab, perms)
    v = np.maximum(sc2, 1e-12) * g / (g - 1) / Sp ** 2
    w = 1 / np.maximum(v, 1e-300)
    bw = (w * b).sum(1) / w.sum(1)
    Q = (w * (b - bw[:, None]) ** 2).sum(1)
    k = b.shape[1]
    return chi2.sf(Q, k - 1)


def whole_t(sxx, sxy, N):
    return group_t(sxx, sxy, np.zeros(N, int))[0]


def bh(p, q=0.05):
    o = np.argsort(p)
    m = len(p)
    ok = p[o] <= q * (np.arange(1, m + 1) / m)
    keep = np.zeros(m, bool)
    if ok.any():
        keep[o[:np.nonzero(ok)[0].max() + 1]] = True
    return keep


def verdict(x, y, L, rng, R, N, T):
    labs, famtag = labels_for(L)
    ntag = len(famtag)
    st = {s: suff(x, y, s, T) for s in ('FE', 'TR')}
    real = {s: np.concatenate([group_t(*st[s], lab) for lab in labs]) for s in st}
    wt = {s: whole_t(*st[s], N) for s in st}
    het_real = np.mean([het_p(*st['TR'], lab) < 0.05 for lab in labs])
    perms = np.argsort(rng.random((R, N)), 1)
    rnd = {}
    for s in st:
        chunks = [rand_stats(*st[s], lab, perms)[0] for lab in labs]
        rnd[s] = np.concatenate(chunks, 1)
    het_rnd = np.stack([rand_het(*st['TR'], lab, perms) < 0.05 for lab in labs], 1).mean(1)
    tr, fe = rnd['TR'], rnd['FE']
    sgn = np.sign(wt['TR'])
    whole_ok = abs(wt['FE']) > 1.96 and abs(wt['TR']) > 1.96 and np.sign(wt['FE']) == sgn
    sig_same = (real['TR'] * sgn > 1.96)
    share = sig_same.mean()
    famshare = min(sig_same[famtag == f].mean() for f in range(NFAM))
    flip = (real['TR'] * sgn < -1.96).mean()
    flip_rand = ((tr * sgn < -1.96).mean(1)).mean()
    robust = bool(whole_ok and share >= 0.5 and famshare >= 0.25 and flip <= max(0.10, flip_rand + 0.05))
    hetok = bool(het_real <= np.quantile(het_rnd, 0.95))
    null_share = (tr * sgn > 1.96).mean(1)
    p_beats = float((1 + (null_share >= share).sum()) / (R + 1))
    mu = tr.mean(0)
    sd = tr.std(0) + 1e-9
    z = np.sign(wt['TR']) * (real['TR'] - mu) / sd
    p = (1 + (abs(tr) >= abs(real['TR'])).sum(0)) / (R + 1)
    keep = bh(p) & (abs(real['TR']) > 1.96) & (z >= 3) & (abs(wt['FE']) > 1.96) & (
        np.sign(wt['FE']) == np.sign(wt['TR']))
    tags = [int(i) for i in np.nonzero(keep)[0]]
    if robust:
        cat = 'ROBUST+H' if hetok else ('ROBUST-but-GROUP' if tags else 'ROBUST-HET')
    elif tags:
        cat = 'GROUP'
    elif p_beats < 0.05:
        cat = 'BEATS'
    else:
        cat = 'NONE'
    return dict(cat=cat, tags=tags, share=float(share), p_beats=p_beats, het_real=float(het_real))


def wilson(k, n, z=1.96):
    if n == 0:
        return (float('nan'), float('nan'))
    p = k / n
    den = 1 + z * z / n
    c = (p + z * z / (2 * n)) / den
    h = z * np.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return (float(max(0.0, c - h)), float(min(1.0, c + h)))


def summarise(cats, regime, planted=4):
    n = len(cats)
    cnt = Counter(cats)
    out = dict(reps=n, counts=dict(cnt))
    def rate(c):
        return cnt[c] / n
    for c in ('ROBUST+H', 'ROBUST-HET', 'ROBUST-but-GROUP', 'GROUP', 'BEATS', 'NONE'):
        out[c + '_rate'] = rate(c)
        out[c + '_ci'] = wilson(cnt[c], n)
    if regime in ('C', 'D'):
        fp = sum(cnt[c] for c in cnt if c != 'NONE')
        out['false_positive_rate'] = fp / n
        out['false_positive_ci'] = wilson(fp, n)
    if regime == 'U':
        out['false_negative_rate'] = rate('NONE')
        out['false_negative_ci'] = wilson(cnt['NONE'], n)
        out['correct_robust_rate'] = (cnt['ROBUST+H'] + cnt['ROBUST-but-GROUP']) / n
        out['correct_robust_ci'] = wilson(cnt['ROBUST+H'] + cnt['ROBUST-but-GROUP'], n)
    if regime == 'B':
        hit = sum(1 for c in cats if c in ('GROUP', 'ROBUST-but-GROUP'))
        # localisation measured separately from the per-rep tags
        out['false_robust_everywhere_rate'] = (cnt['ROBUST+H'] + cnt['ROBUST-HET']) / n
        out['false_robust_everywhere_ci'] = wilson(cnt['ROBUST+H'] + cnt['ROBUST-HET'], n)
    return out


def run_cell(regime, b, N, T, reps, R, seed_base):
    cats = []
    loc_hits = 0
    for rep in range(reps):
        rng = np.random.default_rng(seed_base + 1000 * rep)
        x, y, L = make_panel(regime, rng, N, T, b)
        v = verdict(x, y, L, rng, R, N, T)
        cats.append(v['cat'])
        if regime == 'B':
            if v['cat'] in ('GROUP', 'ROBUST-but-GROUP') and 4 in v['tags']:
                loc_hits += 1
    out = summarise(cats, regime)
    out.update(N=N, T=T, R=R, b=b, seed_base=seed_base)
    if regime == 'B':
        out['planted_tag_flagged'] = loc_hits
        out['planted_tag_flagged_rate'] = loc_hits / reps
        out['planted_tag_flagged_ci'] = wilson(loc_hits, reps)
    return out


def selftest():
    """Compare vectorised random statistics with the original loop implementation."""
    rng = np.random.default_rng(7)
    x, y, L = make_panel('U', rng, 120, 40, 0.15)
    labs, _ = labels_for(L)
    st = {s: suff(x, y, s, 40) for s in ('FE', 'TR')}
    perms = np.argsort(rng.random((50, 120)), 1)
    lab = labs[0]
    vt, _, _, _, _ = rand_stats(*st['TR'], lab, perms)
    loop = np.stack([group_t(*st['TR'], lab[np.argsort(perm)]) for perm in perms])
    d = np.nanmax(np.abs(vt - loop))
    vh = rand_het(*st['TR'], lab, perms)
    lh = np.array([het_p(*st['TR'], lab[np.argsort(perm)]) for perm in perms])
    dh = np.nanmax(np.abs(vh - lh))
    print(json.dumps({'selftest_group_t_max_abs_diff': float(d), 'selftest_het_max_abs_diff': float(dh)}))
    return d < 1e-8 and dh < 1e-8


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--out', default='results/calibration.json')
    ap.add_argument('--quick', action='store_true', help='smaller reps for a smoke test')
    args = ap.parse_args()
    if args.selftest:
        ok = selftest()
        print('SELFTEST_PASS' if ok else 'SELFTEST_FAIL')
        return 0 if ok else 1
    reps_main = 40 if args.quick else REPS_MAIN
    reps_grid = 20 if args.quick else REPS_GRID
    out = dict(design=dict(N=N_DEFAULT, T=T_DEFAULT, cuts=CUTS, R=R_MAIN, regimes_reps=reps_main,
                           grid_reps=reps_grid, seed_base=SEED_BASE), main={}, strength_ladder={}, design_grid={}, R_axis={})
    # main regimes: C null, U uniform strong, B minority, D shared trend, S sign split
    specs = [('C', None, 'null'), ('U', 0.15, 'uniform strong'), ('B', 0.40, 'minority top third fam0'),
             ('D', None, 'shared country trends, no effect'), ('S', None, 'sign-split +/-0.25')]
    for reg, b, label in specs:
        cell = run_cell(reg, b, N_DEFAULT, T_DEFAULT, reps_main, R_MAIN, SEED_BASE)
        cell['label'] = label
        out['main'][reg] = cell
        print(reg, label, json.dumps({k: cell[k] for k in cell if k.endswith('_rate') or k.endswith('_flagged_rate') or k == 'reps'}), flush=True)
    # strength ladder (uniform)
    for b in (0.02, 0.04, 0.06, 0.10, 0.15, 0.25):
        cell = run_cell('U', b, N_DEFAULT, T_DEFAULT, reps_main, R_MAIN, SEED_BASE + 500000 + int(b * 1000))
        out['strength_ladder'][str(b)] = cell
        print('ladder', b, cell['correct_robust_rate'], cell['false_negative_rate'], flush=True)
    # design grid: N x T for C, U(0.06), B(0.40)
    for reg, b in (('C', None), ('U', 0.06), ('B', 0.40)):
        for (N, T) in [(80, 50), (150, 30), (150, 50), (150, 60), (220, 50)]:
            cell = run_cell(reg, b, N, T, reps_grid, R_MAIN, SEED_BASE + 900000 + N * 10 + T)
            out['design_grid'][f"{reg}_N{N}_T{T}"] = cell
            print('grid', reg, N, T, cell.get('false_positive_rate', cell.get('correct_robust_rate')), flush=True)
    # draw-count axis R for C and U(0.06)
    for reg, b in (('C', None), ('U', 0.06)):
        for R in (100, 400):
            cell = run_cell(reg, b, N_DEFAULT, T_DEFAULT, reps_grid, R, SEED_BASE + 700000 + R)
            out['R_axis'][f"{reg}_R{R}"] = cell
            print('Raxis', reg, R, cell.get('false_positive_rate', cell.get('correct_robust_rate')), flush=True)
    os.makedirs(os.path.dirname(args.out) or '.', exist_ok=True)
    json.dump(out, open(args.out, 'w'), indent=1, default=float)
    print('WROTE', args.out)
    return 0


if __name__ == '__main__':
    sys.exit(main())
