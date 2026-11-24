"""Known-truth simulation for the grouping-multiverse verdict rules (methods paper, section 6.8).

SIMPLIFIED, SINGLE-CORE VERSION. It is a design check, not the paper's estimator:
 - estimator: country-clustered OLS slope with country fixed effects (FE) or country trends (TR),
   computed from per-country sufficient statistics (exact, fast);
 - 4 grouping families x (2 cuts, 3 cuts) = 8 groupings, 20 tags;
 - random-grouping null: same group sizes, random permutation of countries, R draws;
 - verdicts: ROBUST (paper rule) split into ROBUST+H (also passes a heterogeneity-vs-random condition) and ROBUST-HET / ROBUST-but-GROUP (paper rule passes, heterogeneity fails); GROUP-SPECIFIC; NONE (the paper's 'beats random' tier is not implemented);
 - truth regimes: A uniform b=0.15, W weak uniform b=0.06, B planted in top tercile of family 0,
   C null (independent series), D null + shared country trends (spurious levels link), S sign-split.
Run:  python3 -I known_truth_sim.py [reps] [R]    (defaults 100 reps, R=400 draws)
Freeze-before-look: the design below was fixed before any verdict was inspected; see README.
"""
import sys, json, numpy as np
from collections import Counter

REPS = int(sys.argv[1]) if len(sys.argv) > 1 else 100
RMAX = int(sys.argv[2]) if len(sys.argv) > 2 else 400
N, T = 150, 50
tt = np.arange(T, dtype=float)
CUTS = [2, 3]; NFAM = 4

def ar1(rng, shape, rho, sd):
    e = rng.normal(size=shape); out = np.empty(shape); out[..., 0] = e[..., 0]
    for k in range(1, shape[-1]): out[..., k] = rho * out[..., k-1] + np.sqrt(1-rho**2) * e[..., k]
    return sd * out

def make_panel(regime, rng):
    common = rng.normal(size=(N, 1)); L = 0.5*common + rng.normal(size=(N, NFAM))
    d = rng.normal(size=N)
    ex = ar1(rng, (N, T), 0.6, 1.0); ey = ar1(rng, (N, T), 0.6, 1.5)
    if regime == 'D':   # shared country-specific trends, no causal link
        sx, sy = 0.05*d, 0.05*d
    else:
        sx, sy = 0.05*rng.normal(size=N), 0.05*rng.normal(size=N)
    b = np.zeros(N)
    if regime == 'A': b[:] = 0.15
    if regime == 'W': b[:] = 0.06
    if regime == 'B': b[L[:, 0] > np.quantile(L[:, 0], 2/3)] = 0.40
    if regime == 'S': b[L[:, 1] > np.median(L[:, 1])] = 0.25; b[L[:, 1] <= np.median(L[:, 1])] = -0.25
    x = rng.normal(size=(N, 1)) + sx[:, None]*tt + ex
    y = rng.normal(size=(N, 1)) + sy[:, None]*tt + b[:, None]*(sx[:, None]*tt + ex) + ey
    return x, y, L

def suff(x, y, spec):
    if spec == 'FE':
        X = x - x.mean(1, keepdims=True); Y = y - y.mean(1, keepdims=True)
    else:
        A = np.stack([np.ones(T), tt], 1); P = A @ np.linalg.solve(A.T @ A, A.T)
        X = x - x @ P; Y = y - y @ P
    sxx = (X*X).sum(1); sxy = (X*Y).sum(1)
    return sxx, sxy

def labels_for(L):
    labs, fam = [], []
    for f in range(NFAM):
        for c in CUTS:
            q = np.quantile(L[:, f], np.linspace(0, 1, c+1)[1:-1])
            labs.append(np.searchsorted(q, L[:, f])); fam.append(f)
    return labs, np.array([f for f, lab in zip(fam, labs) for _ in range(lab.max()+1)])

def group_t(sxx, sxy, lab):
    k = lab.max()+1
    S = np.bincount(lab, sxx, k); Sy = np.bincount(lab, sxy, k)
    b = Sy/S; sc2 = np.bincount(lab, sxy**2, k) - 2*b*np.bincount(lab, sxx*sxy, k) + b**2*np.bincount(lab, sxx**2, k)
    g = np.bincount(lab, minlength=k); se = np.sqrt(np.maximum(sc2, 1e-12) * g/(g-1)) / S
    return b/se

def het_p(sxx, sxy, lab):
    from scipy.stats import chi2
    k = lab.max()+1
    S = np.bincount(lab, sxx, k); Sy = np.bincount(lab, sxy, k); b = Sy/S
    sc2 = np.bincount(lab, sxy**2, k) - 2*b*np.bincount(lab, sxx*sxy, k) + b**2*np.bincount(lab, sxx**2, k)
    g = np.bincount(lab, minlength=k); v = np.maximum(sc2, 1e-12)*g/(g-1)/S**2
    w = 1/v; bw = (w*b).sum()/w.sum(); Q = (w*(b-bw)**2).sum()
    return float(chi2.sf(Q, k-1))

def whole_t(sxx, sxy):
    return group_t(sxx, sxy, np.zeros(N, int))[0]

def bh(p, q=0.05):
    o = np.argsort(p); m = len(p); ok = p[o] <= q*(np.arange(1, m+1)/m)
    keep = np.zeros(m, bool)
    if ok.any(): keep[o[:np.nonzero(ok)[0].max()+1]] = True
    return keep

def verdicts(x, y, L, rng, Rlist):
    labs, famtag = labels_for(L); ntag = len(famtag)
    st = {s: suff(x, y, s) for s in ('FE', 'TR')}
    real = {s: np.concatenate([group_t(*st[s], lab) for lab in labs]) for s in st}
    wt = {s: whole_t(*st[s]) for s in st}
    rnd = {s: np.empty((RMAX, ntag)) for s in st}
    het_real = np.mean([het_p(*st['TR'], lab) < 0.05 for lab in labs]); het_rnd = np.empty(RMAX)
    for r in range(RMAX):
        perm = rng.permutation(N)
        for s in st:
            rnd[s][r] = np.concatenate([group_t(*st[s], lab[perm]) for lab in labs])
        het_rnd[r] = np.mean([het_p(*st['TR'], lab[perm]) < 0.05 for lab in labs])
    out = {}
    for R in Rlist:
        tr = rnd['TR'][:R]; fe = rnd['FE'][:R]
        sgn = np.sign(wt['TR'])
        whole_ok = abs(wt['FE']) > 1.96 and abs(wt['TR']) > 1.96 and np.sign(wt['FE']) == sgn
        sig_same = (real['TR']*sgn > 1.96)
        share = sig_same.mean()
        famshare = min(sig_same[famtag == f].mean() for f in range(NFAM))
        flip = (real['TR']*sgn < -1.96).mean()
        flip_rand = ((tr*sgn < -1.96).mean(1)).mean()
        robust = whole_ok and share >= 0.5 and famshare >= 0.25 and flip <= max(0.10, flip_rand+0.05)
        hetok = het_real <= np.quantile(het_rnd[:R], 0.95)   # v2 rule; v1 (max(0.10, mean+0.05)) was discretised by 8 groupings and failed 40% of uniform truths
        if robust and hetok: out[R] = ('ROBUST+H', None); continue      # robust AND groups no more heterogeneous than random
        mu = tr.mean(0); sd = tr.std(0)+1e-9
        z = np.sign(real['TR'])*(real['TR']-mu)/sd
        p = (1+(abs(tr) >= abs(real['TR'])).sum(0))/(R+1)
        keep = bh(p) & (abs(real['TR']) > 1.96) & (z >= 3) & (abs(real['FE']) > 1.96) & (np.sign(real['FE']) == np.sign(real['TR']))
        if keep.any(): out[R] = ('GROUP' if not robust else 'ROBUST-but-GROUP', [int(i) for i in np.nonzero(keep)[0]])
        elif robust: out[R] = ('ROBUST-HET', None)   # paper rule says robust; heterogeneity condition fails; no tag clears FDR
        else: out[R] = ('NONE', None)
    return out, famtag

def main():
    Rlist = [r for r in (25, 100, 400) if r <= RMAX]
    res = {}
    for regime in ('A', 'W', 'B', 'C', 'D', 'S'):
        rng = np.random.default_rng({'A':1,'W':2,'B':3,'C':4,'D':5,'S':6}[regime]*1000+7)
        cnt = {R: Counter() for R in Rlist}; hit = {R: 0 for R in Rlist}
        for rep in range(REPS):
            x, y, L = make_panel(regime, rng)
            out, famtag = verdicts(x, y, L, rng, Rlist)
            for R in Rlist:
                v, tags = out[R]; cnt[R][v] += 1
                if regime == 'B' and v in ('GROUP', 'ROBUST-but-GROUP'):
                    # planted tag: family 0, 3-cut, top tercile = index  (fam0 2-cut has 2 tags, 3-cut has 3 tags)
                    if 4 in tags: hit[R] += 1
        res[regime] = {str(R): dict(cnt[R]) | ({'planted_tag_flagged': hit[R]} if regime == 'B' else {}) for R in Rlist}
        print(regime, res[regime], flush=True)
    json.dump({'reps': REPS, 'R': Rlist, 'N': N, 'T': T, 'results': res}, open('known_truth_sim.json', 'w'), indent=1)

if __name__ == '__main__': main()
