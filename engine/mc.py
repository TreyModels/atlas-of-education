"""mc: the Monte Carlo experiment manager. One place for seeds, parameter draws, matched random numbers across
policies, Sobol sensitivity and structural comparison.

Why one module. Every Monte Carlo in the Atlas answers a variant of four questions, and each used to answer them with
its own seed arithmetic:

  1. Which parameter worlds are plausible?           draw_prior(...)  then  monte_carlo(...)         (+ abc_accept)
  2. Does a policy work, net of simulation noise?    paired_effects(...)  matched seeds, sign claims only when the
                                                     interval excludes zero
  3. Which parameters drive an outcome?              sobol_indices(...)  first-order and total-order, with intervals
  4. Does the answer depend on how the model is built?  compare_structures(...)  same draws, same seeds, rival models

Conventions (do not change them casually; stored results depend on them):

  * A "world" i of a batch draws its simulation noise from seed  100000 * reseed + i  (matched_seeds). Changing
    `reseed` reruns the same parameter worlds with fresh noise, which is how seed noise is measured.
  * Policies are compared on MATCHED random numbers: the baseline and every policy run on the same seed, and the
    effect is the difference within a seed. The Cambodia browser bands (engine/camchild_record.cjs, node) use the same
    rule with seeds 1..30 (APP_SEEDS); that file is JavaScript and cannot import this one.
  * Prior boxes are {name: (low, high, 'lin' | 'log')}, as in childworld.PRIORS.
  * design='random' reproduces the original childworld draws bit for bit (one numpy Generator, one uniform vector per
    parameter in dict order). 'sobol' and 'lhs' are scrambled low-discrepancy designs for sensitivity work.
  * Functions given to run_batch must be defined at module level (they are pickled to worker processes).

Everything here is deterministic for fixed arguments.
"""
import math
import os
from concurrent.futures import ProcessPoolExecutor

import numpy as np

VERSION = '1.0'
APP_SEEDS = tuple(range(1, 31))          # the seeds behind the 30-seed bands in the Cambodia app


# ---------------------------------------------------------------- seeds and generators
def rng(master, stream=None):
    """A numpy Generator. rng(13) is exactly default_rng(13); rng(13, 2) is an independent stream of master 13."""
    if stream is None:
        return np.random.default_rng(master)
    return np.random.default_rng(np.random.SeedSequence([int(master), int(stream)]))


def spawn_seeds(master, n):
    """n statistically independent integer seeds from one master seed (for new experiments)."""
    return [int(s) for s in np.random.SeedSequence(int(master)).generate_state(n, dtype=np.uint64) % (2 ** 31)]


def matched_seeds(n, reseed=0, base=100000):
    """The simulation seed of each of n worlds. Same worlds + same reseed = same noise; new reseed = new noise."""
    return [base * reseed + i for i in range(n)]


# ---------------------------------------------------------------- prior draws
def _scale(u, lo, hi, sc):
    if sc == 'log':
        return np.exp(math.log(lo) + u * (math.log(hi) - math.log(lo)))
    return lo + u * (hi - lo)


def unit_design(d, n, design='random', master=7):
    """n points in the unit cube [0,1)^d. design: 'random' | 'sobol' | 'lhs'."""
    if design == 'random':
        r = rng(master)
        return np.stack([r.random(n) for _ in range(d)], axis=1)
    from scipy.stats import qmc
    if design == 'sobol':
        return qmc.Sobol(d, scramble=True, seed=master).random(n)
    if design == 'lhs':
        return qmc.LatinHypercube(d, seed=master).random(n)
    raise ValueError(f'unknown design {design!r}')


def draw_prior(priors, n, master=7, design='random'):
    """Dict name -> array of n draws from the prior box."""
    keys = list(priors)
    if design == 'random':                       # reproduces childworld.draw(default_rng(master), n, priors)
        r = rng(master)
        return {k: _scale(r.random(n), *priors[k][:2], priors[k][2]) for k in keys}
    U = unit_design(len(keys), n, design, master)
    return {k: _scale(U[:, j], *priors[k][:2], priors[k][2]) for j, k in enumerate(keys)}


def as_rows(D):
    """{name: array} -> list of {name: float}."""
    n = len(next(iter(D.values())))
    return [{k: float(v[i]) for k, v in D.items()} for i in range(n)]


# ---------------------------------------------------------------- running
def _call(job):
    fn, args = job
    return fn(*args)


def run_batch(fn, arg_tuples, workers=None, chunksize=None):
    """[fn(*a) for a in arg_tuples], in order, across processes. workers=1 runs in this process (for tests)."""
    arg_tuples = list(arg_tuples)
    if workers == 1 or len(arg_tuples) < 2:
        return [fn(*a) for a in arg_tuples]
    cs = chunksize or max(1, len(arg_tuples) // (4 * (workers or os.cpu_count() or 1)))
    with ProcessPoolExecutor(max_workers=workers) as ex:
        return list(ex.map(_call, [(fn, a) for a in arg_tuples], chunksize=cs))


def monte_carlo(sim, thetas, seeds, workers=None):
    """sim(theta, seed) -> dict of outputs. Returns the list of outputs, one per world, in order."""
    return run_batch(sim, list(zip(thetas, seeds)), workers)


def provenance(**kw):
    import scipy
    return dict(mc_version=VERSION, numpy=np.__version__, scipy=scipy.__version__, **kw)


# ---------------------------------------------------------------- policies on matched random numbers
def summarize(x, z=1.96):
    """Mean, spread and a sign claim for a set of paired differences (one per seed)."""
    x = np.asarray(x, float)
    n = len(x)
    se = float(x.std(ddof=1) / math.sqrt(n)) if n > 1 else float('nan')
    m = float(x.mean())
    lo, hi = m - z * se, m + z * se
    return dict(n=n, mean=m, sd=float(x.std(ddof=1)) if n > 1 else float('nan'), se=se, lo=lo, hi=hi,
                p05=float(np.percentile(x, 5)), p50=float(np.percentile(x, 50)), p95=float(np.percentile(x, 95)),
                share_lower=float((x < 0).mean()), share_higher=float((x > 0).mean()),
                sign=('lower' if hi < 0 else 'higher' if lo > 0 else 'none'))


def paired_effects(sim, policies, seeds, outcome, workers=None):
    """Effect of each policy on `outcome`, on matched random numbers.

    sim(seed, policy_dict) -> anything;  outcome(result) -> float.  The baseline is policy {} on the same seed.
    Returns {policy_name: summarize(effect per seed)} and the raw per-seed effects under key '_raw'.
    A sign is claimed ('lower' / 'higher') only when the 95% interval over seeds excludes zero; otherwise 'none'.
    """
    names = list(policies)
    jobs = [(sim, s, {}) for s in seeds] + [(sim, s, policies[n]) for n in names for s in seeds]
    vals = run_batch(_outcome_of, [(outcome, *j) for j in jobs], workers)
    k = len(seeds)
    base = np.array(vals[:k])
    raw = {n: np.array(vals[k * (1 + i):k * (2 + i)]) - base for i, n in enumerate(names)}
    out = {n: summarize(raw[n]) for n in names}
    out['_raw'] = {n: raw[n].tolist() for n in names}
    out['_baseline'] = base.tolist()
    return out


def _outcome_of(outcome, sim, seed, policy):
    return float(outcome(sim(seed, policy)))


# ---------------------------------------------------------------- Sobol sensitivity (Saltelli 2010, Jansen total)
def sobol_indices(f, priors, n=1024, master=0, boot=200, workers=None, vectorized=False):
    """First-order (S1) and total-order (ST) Sobol indices of a scalar output.

    f(theta_dict) -> float for one world (run in parallel), or, if vectorized=True, f({name: array}) -> array.
    Cost: n * (d + 2) evaluations. Use a FIXED simulation seed inside f, otherwise noise is counted as variance
    that no parameter explains. n should be a power of two. Intervals are bootstrap 5-95%.
    """
    keys = list(priors)
    d = len(keys)
    U = unit_design(2 * d, n, 'sobol', master)
    A, B = U[:, :d], U[:, d:]
    mats = [A, B] + [np.where(np.arange(d) == i, B, A) for i in range(d)]

    def evaluate(M):
        D = {k: _scale(M[:, j], *priors[k][:2], priors[k][2]) for j, k in enumerate(keys)}
        if vectorized:
            return np.asarray(f(D), float)
        return np.array(run_batch(f, [(t,) for t in as_rows(D)], workers), float)

    Y = [evaluate(M) for M in mats]
    yA, yB, yAB = Y[0], Y[1], Y[2:]

    def est(idx):
        a, b = yA[idx], yB[idx]
        var = np.var(np.concatenate([a, b]), ddof=1)
        if var <= 0:
            return np.zeros(d), np.zeros(d)
        s1 = np.array([np.mean(b * (ab[idx] - a)) / var for ab in yAB])
        st = np.array([0.5 * np.mean((a - ab[idx]) ** 2) / var for ab in yAB])
        return s1, st

    s1, st = est(np.arange(n))
    r = rng(master, 1)
    bs = [est(r.integers(0, n, n)) for _ in range(boot)]
    b1, bt = np.array([b[0] for b in bs]), np.array([b[1] for b in bs])
    return {k: dict(S1=float(s1[i]), S1_lo=float(np.percentile(b1[:, i], 5)), S1_hi=float(np.percentile(b1[:, i], 95)),
                    ST=float(st[i]), ST_lo=float(np.percentile(bt[:, i], 5)), ST_hi=float(np.percentile(bt[:, i], 95)))
            for i, k in enumerate(keys)}, dict(evaluations=n * (d + 2), n=n, boot=boot)


def stiff_directions(indices, threshold=0.05):
    """Parameters whose total-order index exceeds the threshold, biggest first (the 'stiff' directions)."""
    return [k for k, v in sorted(indices.items(), key=lambda kv: -kv[1]['ST']) if v['ST'] >= threshold]


# ---------------------------------------------------------------- structural comparison
def compare_structures(models, thetas, seeds, keys, workers=None):
    """Run rival model structures on the SAME parameter draws and the SAME seeds.

    models: {name: sim(theta, seed) -> dict}.  For each output key reports, per structure, the mean over worlds, and for
    every pair the mean difference with its interval (paired by world), the share of worlds where the first is higher,
    and the rank correlation across worlds (do the structures agree about WHICH worlds are high?).  `between_share` is the
    share of output variance that sits between structures rather than between worlds: near 0 means the conclusion does
    not depend on the structure.
    """
    from scipy.stats import spearmanr
    outs = {n: monte_carlo(m, thetas, seeds, workers) for n, m in models.items()}
    names = list(models)
    res = {}
    for k in keys:
        M = np.array([[o[k] for o in outs[n]] for n in names])           # structures x worlds
        pairs = {}
        for i in range(len(names)):
            for j in range(i + 1, len(names)):
                diff = M[i] - M[j]
                s = summarize(diff)
                s['share_first_higher'] = float((diff > 0).mean())
                s['spearman'] = float(spearmanr(M[i], M[j])[0]) if M.shape[1] > 2 else float('nan')
                pairs[f'{names[i]} - {names[j]}'] = s
        tot = float(M.var())
        between = float(M.mean(axis=1).var())
        res[k] = dict(means={n: float(M[i].mean()) for i, n in enumerate(names)}, pairs=pairs,
                      between_share=between / tot if tot > 0 else 0.0)
    return res


# ---------------------------------------------------------------- approximate Bayesian computation
def abc_accept(outputs, targets, tol):
    """Boolean mask of worlds within tol[key] of targets[key] on every key. outputs: {key: array}."""
    ok = np.ones(len(next(iter(outputs.values()))), bool)
    for k, t in targets.items():
        ok &= np.abs(np.asarray(outputs[k]) - t) <= tol[k]
    return ok
