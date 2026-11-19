"""Small, dependency-light statistics used by the rigor experiments (numpy + scipy only).

Every function here has a known-answer test in research/tests/test_rigor.py.

Forecast comparison
  mae, mase                 Hyndman & Koehler (2006): scale-free accuracy relative to an in-sample naive forecast.
  diebold_mariano           Diebold & Mariano (1995) test of equal predictive accuracy, with the Harvey, Leybourne &
                            Newbold (1997) small-sample correction and Student-t reference. Loss differentials are
                            serially correlated when horizons overlap, so the long-run variance uses h-1 lags.

Mechanism recovery (identifiability by simulation)
  abc_recovery              Leave-one-out ABC rejection model choice on a reference table of simulated summaries.
                            Each simulated dataset in turn plays "the observed data" (with declared observation noise
                            added); the k nearest other simulations vote for the structure that generated it. The
                            confusion matrix answers: if structure S were true, how often would data of this design
                            point to S? This is the model-recovery check recommended by Wilson & Collins (2019) and the
                            standard response to the fragility of ABC model choice (Robert et al. 2011): judge a design
                            by its confusion matrix, not by one posterior model probability.
"""
from __future__ import annotations

import math

import numpy as np
from scipy import stats as _st


# ------------------------------------------------------------------ forecast accuracy
def mae(err):
    err = np.asarray(err, float)
    return float(np.mean(np.abs(err))) if err.size else float('nan')


def mase(err, insample, m=1):
    """Mean absolute scaled error: MAE of `err` divided by the in-sample MAE of the lag-m naive forecast."""
    y = np.asarray(insample, float)
    if y.size <= m:
        return float('nan')
    scale = np.mean(np.abs(y[m:] - y[:-m]))
    return float(mae(err) / scale) if scale > 0 else float('nan')


def _long_run_var(d, lags):
    d = np.asarray(d, float) - np.mean(d)
    n = d.size
    g0 = float(d @ d) / n
    v = g0
    for k in range(1, lags + 1):
        if k >= n:
            break
        gk = float(d[k:] @ d[:-k]) / n
        v += 2 * gk            # rectangular kernel, as in Diebold & Mariano (1995) for h-step forecasts
    if v <= 0:                 # rectangular kernel can go negative in small samples; fall back to Bartlett
        v = g0 + sum(2 * (1 - k / (lags + 1)) * float(d[k:] @ d[:-k]) / n for k in range(1, min(lags, n - 1) + 1))
    return v


def diebold_mariano(e_model, e_bench, h=1, power=1):
    """Test H0: equal expected loss. Loss = |e|^power. Negative statistic = model more accurate.

    Returns dict(stat, p_two_sided, n, mean_loss_diff, hln=True). Uses the HLN correction
    sqrt((n + 1 - 2h + h(h-1)/n) / n) and a t(n-1) reference distribution.
    """
    e1 = np.asarray(e_model, float); e2 = np.asarray(e_bench, float)
    ok = np.isfinite(e1) & np.isfinite(e2)
    e1, e2 = e1[ok], e2[ok]
    n = e1.size
    if n < 3:
        return dict(stat=None, p_two_sided=None, n=int(n), mean_loss_diff=None, hln=True,
                    note='fewer than 3 paired errors: no test')
    d = np.abs(e1) ** power - np.abs(e2) ** power
    v = _long_run_var(d, max(h - 1, 0))
    if v <= 0:
        return dict(stat=None, p_two_sided=None, n=int(n), mean_loss_diff=float(d.mean()), hln=True,
                    note='zero long-run variance')
    dm = d.mean() / math.sqrt(v / n)
    corr = math.sqrt(max((n + 1 - 2 * h + h * (h - 1) / n) / n, 1e-12))
    stat = float(dm * corr)
    p = float(2 * _st.t.sf(abs(stat), df=n - 1))
    return dict(stat=stat, p_two_sided=p, n=int(n), mean_loss_diff=float(d.mean()), hln=True)


# ------------------------------------------------------------------ mechanism recovery
def abc_recovery(X, labels, noise_sd, k=None, accept_frac=0.02, rng=None, mask_obs=None, reps=1):
    """Leave-one-out ABC rejection model choice.

    X          (n, p) noiseless simulated summaries (one row per simulated dataset)
    labels     length-n structure labels
    noise_sd   length-p observation-error SDs added to the pseudo-observed row only (declared assumptions)
    k          neighbours per vote (default: max(5, accept_frac * n))
    mask_obs   optional boolean length-n: which rows may play "observed" (e.g. only rows near real data)
    reps       independent noise draws per pseudo-observed row

    Distances use summaries standardised by their pooled SD plus noise SD, so a summary measured with large error
    carries less weight. Returns dict(labels, confusion (true x predicted counts), accuracy, chance, per_true_recall,
    mean_posterior_true (average vote share for the true structure)).
    """
    X = np.asarray(X, float); labels = np.asarray(labels)
    noise_sd = np.asarray(noise_sd, float)
    n, p = X.shape
    if noise_sd.shape != (p,):
        raise ValueError('noise_sd must have one entry per summary')
    keep = np.all(np.isfinite(X), axis=1)
    X, labels = X[keep], labels[keep]
    mask_obs = np.ones(len(X), bool) if mask_obs is None else np.asarray(mask_obs, bool)[keep]
    n = len(X)
    rng = np.random.default_rng(0) if rng is None else rng
    uniq = sorted(set(labels.tolist()))
    idx = {s: i for i, s in enumerate(uniq)}
    k = int(k or max(5, round(accept_frac * n)))
    scale = np.sqrt(X.std(axis=0) ** 2 + noise_sd ** 2)
    scale[scale == 0] = 1.0
    Z = X / scale
    conf = np.zeros((len(uniq), len(uniq)), int)
    post_true = []
    for i in np.flatnonzero(mask_obs):
        for _ in range(reps):
            obs = (X[i] + rng.normal(0, noise_sd)) / scale
            dist = np.sqrt(((Z - obs) ** 2).sum(axis=1))
            dist[i] = np.inf                     # leave the generating simulation out
            nn = np.argpartition(dist, k)[:k]
            votes = np.bincount([idx[s] for s in labels[nn]], minlength=len(uniq)) / k
            pred = int(np.argmax(votes))
            conf[idx[labels[i]], pred] += 1
            post_true.append(votes[idx[labels[i]]])
    total = conf.sum()
    recall = {s: (float(conf[i, i] / conf[i].sum()) if conf[i].sum() else None) for s, i in idx.items()}
    return dict(labels=uniq, confusion=conf.tolist(), accuracy=float(np.trace(conf) / total) if total else None,
                chance=1 / len(uniq), per_true_recall=recall, k=k, n_reference=int(n),
                n_pseudo_observed=int(total), mean_posterior_true=float(np.mean(post_true)) if post_true else None)


def paired_summary(diffs):
    """Mean, SD, standard error, t and a 95% interval for paired (common-random-number) differences."""
    d = np.asarray([x for x in diffs if x is not None and np.isfinite(x)], float)
    n = d.size
    if n < 2:
        return dict(n=int(n), mean=float(d.mean()) if n else None)
    se = d.std(ddof=1) / math.sqrt(n)
    q = _st.t.ppf(0.975, n - 1)
    return dict(n=int(n), mean=float(d.mean()), sd=float(d.std(ddof=1)), se=float(se),
                t=float(d.mean() / se) if se > 0 else None, ci95=[float(d.mean() - q * se), float(d.mean() + q * se)],
                share_negative=float(np.mean(d < 0)), share_positive=float(np.mean(d > 0)))


def r2_ols(y, x):
    """R^2 and OLS slope t-statistic (classical SE) of y on [1, x]. Used for the spurious-regression null."""
    y = np.asarray(y, float); x = np.asarray(x, float)
    X = np.column_stack([np.ones_like(x), x])
    beta, *_ = np.linalg.lstsq(X, y, rcond=None)
    e = y - X @ beta
    sst = float(((y - y.mean()) ** 2).sum())
    r2 = 1 - float(e @ e) / sst if sst > 0 else float('nan')
    s2 = float(e @ e) / max(len(y) - 2, 1)
    var_b = s2 * np.linalg.pinv(X.T @ X)[1, 1]
    t = float(beta[1] / math.sqrt(var_b)) if var_b > 0 else float('nan')
    return r2, t, float(beta[1])
