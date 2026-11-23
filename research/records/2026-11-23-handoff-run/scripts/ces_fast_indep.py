#!/usr/bin/env python3
"""Structural estimation of agricultural input substitutability, with recovery.

Boppart et al. posit  Y_a = A_a F(K,L,M,T)  with a nested CES whose elasticity
between labour and capital, and between labour and intermediates, exceeds one.
That elasticity is the parameter the whole mechanism turns on: it is what makes
input intensification (245x in the data) cost-minimising rather than an anomaly.

Model, per country i and year t:

    log(K/L)_it = beta_i + sigma_i * log(w/p)_it + gamma_t + e_it

    beta_i  ~ N(mu_b, tau_b^2)      country intercepts
    sigma_i ~ N(mu_s, tau_s^2)      country-specific substitutability
    gamma_t ~ N(0, 100)             common year effects (absorb shared trends)
    e_it    ~ N(0, s2)

Estimated by Gibbs. mu_s is the headline: the average elasticity. tau_s is what
matters for the theory: whether substitutability is high everywhere, or high only
in some countries.

Then a recovery study: simulate panels with known sigma, run the same estimator,
and report bias and coverage. If the estimator cannot recover a known sigma, its
estimate on real data means nothing.
"""
import json, os, sys
from multiprocessing import Pool
import numpy as np

DATA = "/root/work/data"
NSIM = int(os.environ.get("NSIM", "200"))
NIT = int(os.environ.get("NIT", "4000"))
BURN = NIT // 2


def load(n):
    p = os.path.join(DATA, n + ".json")
    return {(r[0], int(r[1])): float(r[2]) for r in json.load(open(p))}


def build_panel():
    yw = load("pwt_yw"); ls = load("pwt_labsh"); pli = load("pwt_pli")
    kl = load("usda_KperL")
    rows = []
    for (i, t), v in kl.items():
        if v <= 0 or (i, t) not in yw or (i, t) not in ls or (i, t) not in pli:
            continue
        w = yw[(i, t)] * ls[(i, t)]
        p = pli[(i, t)]
        if w <= 0 or p <= 0:
            continue
        rows.append((i, t, np.log(v), np.log(w / p)))
    rows.sort()
    return rows


def pack(rows):
    iso = [r[0] for r in rows]
    ui = {v: n for n, v in enumerate(sorted(set(iso)))}
    gi = np.array([ui[v] for v in iso])
    ty = [r[1] for r in rows]
    ti = {v: n for n, v in enumerate(sorted(set(ty)))}
    gt = np.array([ti[v] for v in ty])
    y = np.array([r[2] for r in rows])
    x = np.array([r[3] for r in rows])
    return gi, gt, y, x, len(ui), len(ti)


def gibbs(gi, gt, y, x, G, T, nit=NIT, burn=BURN, seed=0, xb=0.0, xs=0.5, b0=0.5):
    rng = np.random.default_rng(seed)
    n = len(y)
    cnt = np.bincount(gi, minlength=G).astype(float)
    sx = np.bincount(gi, weights=x, minlength=G)
    sxx = np.bincount(gi, weights=x * x, minlength=G)
    beta = np.full(G, b0); sig = np.full(G, xs)
    gam = np.zeros(T)
    mu_b, mu_s = b0, xs
    tau_b, tau_s = b0, xs
    s2 = 1.0
    keep = np.zeros((nit - burn, 2))
    for it in range(nit):
        r = y - gam[gt]
        sy = np.bincount(gi, weights=r, minlength=G)
        sxy = np.bincount(gi, weights=r * x, minlength=G)
        # joint update of (beta_i, sigma_i) -- vectorised over countries
        A = cnt / s2 + 1.0 / tau_b ** 2
        B = sx / s2
        C = sxx / s2 + 1.0 / tau_s ** 2
        det = A * C - B * B
        r1 = sy / s2 + mu_b / tau_b ** 2
        r2 = sxy / s2 + mu_s / tau_s ** 2
        m1 = (C * r1 - B * r2) / det
        m2 = (-B * r1 + A * r2) / det
        V11 = C / det
        V22 = A / det
        V21 = -B / det
        z1 = rng.normal(0, 1, G); z2 = rng.normal(0, 1, G)
        beta = m1 + np.sqrt(V11) * z1
        sig = m2 + (V21 / np.sqrt(V11)) * z1 + np.sqrt(np.maximum(V22 - V21 ** 2 / V11, 1e-12)) * z2
        # year effects
        resid = y - beta[gi] - sig[gi] * x
        ng = np.bincount(gt, minlength=T).astype(float)
        sg = np.bincount(gt, weights=resid, minlength=T)
        prec = ng / s2 + 1.0 / 100.0
        gam = rng.normal(sg / s2 / prec, 1.0 / np.sqrt(prec))
        # hyperparameters
        mu_b = rng.normal(beta.mean(), np.sqrt(tau_b ** 2 / G + 1e-9))
        mu_s = rng.normal(sig.mean(), np.sqrt(tau_s ** 2 / G + 1e-9))
        tau_b = np.sqrt(1.0 / rng.gamma(0.5 + G / 2.0, 1.0 / (0.5 + 0.5 * ((beta - mu_b) ** 2).sum())))
        tau_s = np.sqrt(1.0 / rng.gamma(0.5 + G / 2.0, 1.0 / (0.5 + 0.5 * ((sig - mu_s) ** 2).sum())))
        rss = ((resid - gam[gt]) ** 2).sum()
        s2 = 1.0 / rng.gamma(0.5 + n / 2.0, 1.0 / (0.5 + rss / 2.0))
        if it >= burn:
            keep[it - burn] = (mu_s, tau_s)
    return keep


def run_sim(arg):
    true_s, seed = arg
    rng = np.random.default_rng(seed)
    rows = PANEL
    gi, gt, y0, x, G, T = PACKED
    beta = rng.normal(1.0, 0.8, G)
    sig = rng.normal(true_s, 0.4, G)
    gam = rng.normal(0, 0.3, T)
    y = beta[gi] + sig[gi] * x + gam[gt] + rng.normal(0, 0.35, len(y0))
    k = gibbs(gi, gt, y, x, G, T, nit=NIT, burn=BURN, seed=seed * 7 + 1)
    post = k[:, 0]
    return true_s, post.mean(), np.percentile(post, 2.5), np.percentile(post, 97.5)


if __name__ == "__main__":
    rows = build_panel()
    gi, gt, y, x, G, T = pack(rows)
    PANEL = rows; PACKED = (gi, gt, y, x, G, T)
    print(f"panel: {len(rows)} country-years, {G} countries, {T} years", flush=True)

    print("\nfitting the real data (4 chains):", flush=True)
    with Pool(4) as p:
        chains = p.starmap(gibbs, [(gi, gt, y, x, G, T, NIT, BURN, s) for s in range(4)])
    allc = np.vstack(chains)
    mus, taus = allc[:, 0], allc[:, 1]
    print(f"  mu_sigma (average elasticity) : {mus.mean():+.3f}  "
          f"95% CrI [{np.percentile(mus,2.5):+.3f}, {np.percentile(mus,97.5):+.3f}]")
    print(f"  tau_sigma  (SD across countries): {taus.mean():.3f}  "
          f"95% CrI [{np.percentile(taus,2.5):.3f}, {np.percentile(taus,97.5):.3f}]")
    print(f"  P(mu_sigma > 1) = {100*np.mean(mus>1):.1f}%   "
          f"P(mu_sigma > 0) = {100*np.mean(mus>0):.1f}%")
    rhat = np.abs(chains[0][:, 0].mean() - chains[1][:, 0].mean())
    print(f"  between-chain spread in the mean: {rhat:.4f}")

    print(f"\nrecovery study: {NSIM} simulations per true value", flush=True)
    jobs = [(s, 1000 + 100000 * si + k) for si, s in enumerate((0.0, 0.5, 1.0, 1.5)) for k in range(NSIM)]
    with Pool(28) as p:
        res = p.map(run_sim, jobs, chunksize=2)
    print(f"{'true sigma':>11s}{'mean est':>10s}{'bias':>8s}{'coverage':>10s}")
    for s in (0.0, 0.5, 1.0, 1.5):
        r = [x for x in res if x[0] == s]
        est = np.array([x[1] for x in r])
        cov = np.mean([x[2] <= s <= x[3] for x in r])
        print(f"{s:>11.1f}{est.mean():>10.3f}{est.mean()-s:>+8.3f}{100*cov:>9.1f}%")
