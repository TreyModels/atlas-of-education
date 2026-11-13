"""ABC-SMC calibration for each mechanism variant, scored across K calibration worlds (calibrate.score_worlds).

Distance D(theta) = 7th smallest of the 10 per-world max-z values; a set fits when D <= 1 (>= 7 of 10 worlds fit).

Population steps per generation:
  1. propose from a mixture of the previous (weighted) particles, accept D <= eps (importance weights prior/q);
  2. resample by importance weights, then `mh_sweeps` random-walk Metropolis moves that target
     prior(theta) * 1[D(theta) <= eps] (rejuvenation; this is the fix for weight degeneracy).
Evidence: importance-sampling estimate of P(D <= 1 | variant) under the uniform prior, from a fresh batch
drawn from the final mixture. ESS diagnostics are logged per generation: importance ESS before the move step
and the number of distinct particles after it.
"""
import argparse
import json
from multiprocessing import Pool
from pathlib import Path
import numpy as np
from scipy.stats import multivariate_normal
from calibrate import CAL_WORLDS, FIT_RANK, K_WORLDS, score_worlds
from model import PRIORS, VARIANTS, Params


def free_names(variant):
    return [k for k in PRIORS if k not in ("diversion", "favour") or k in VARIANTS[variant]]


def to_params(names, x):
    values = dict(zip(names, x))
    for mech in ("diversion", "favour"):
        values.setdefault(mech, 0.0)
    return Params(**values)


def simulate(args):
    names, x = args
    D, mean_out, zs = score_worlds(to_params(names, x))
    return D, mean_out, zs


def in_prior(names, x):
    lo = np.array([PRIORS[n][0] for n in names]); hi = np.array([PRIORS[n][1] for n in names])
    return np.all((x >= lo) & (x <= hi), axis=-1)


def prior_density(names):
    return 1.0 / np.prod([PRIORS[n][1] - PRIORS[n][0] for n in names])


def resample_move(names, pool, X, D, O, Z, w, eps, cov, rng, sweeps):
    """Resample by importance weights, then Metropolis moves with target prior * 1[D <= eps]."""
    n, dim = X.shape
    idx = rng.choice(n, size=n, p=w)
    X, D = X[idx].copy(), D[idx].copy()
    O = [O[i] for i in idx]; Z = [Z[i] for i in idx]
    prop_cov = (2.38 ** 2 / dim) * cov
    accepted = 0
    for _ in range(sweeps):
        cand = X + rng.multivariate_normal(np.zeros(dim), prop_cov, size=n)
        ok = np.flatnonzero(in_prior(names, cand))
        res = pool.map(simulate, [(names, cand[i]) for i in ok], chunksize=10) if len(ok) else []
        for j, i in enumerate(ok):
            d, o, z = res[j]
            if d <= eps:
                X[i], D[i], O[i], Z[i] = cand[i], d, o, z
                accepted += 1
    return X, D, O, Z, accepted / (n * sweeps) if sweeps else 1.0


def smc(variant, pool, n_particles, max_gen, seed, log, evidence_n=2000, mh_sweeps=2):
    names = free_names(variant)
    dim = len(names)
    rng = np.random.default_rng(seed)
    lo = np.array([PRIORS[n][0] for n in names]); hi = np.array([PRIORS[n][1] for n in names])
    history = []
    n0 = n_particles * 10
    X = lo + (hi - lo) * rng.random((n0, dim))
    res = pool.map(simulate, [(names, x) for x in X], chunksize=10)
    D = np.array([r[0] for r in res])
    order = np.argsort(D)[:n_particles]
    particles, dist = X[order], D[order]
    O = [res[i][1] for i in order]; Z = [res[i][2] for i in order]
    weights = np.full(n_particles, 1 / n_particles)
    eps = float(dist.max())
    history.append({"gen": 0, "eps": eps, "proposed": n0, "fit_share_of_proposals": float((D <= 1).mean())})
    log(f"{variant} gen0 eps={eps:.3f} prior fit share={np.mean(D <= 1):.5f}")
    for gen in range(1, max_gen + 1):
        eps_new = max(1.0, float(np.quantile(dist, 0.5)))
        cov = 2 * np.cov(particles.T, aweights=weights) + 1e-9 * np.eye(dim)
        kern = multivariate_normal(mean=np.zeros(dim), cov=cov)
        acc_x, acc_d, acc_o, acc_z, acc_q, props, proposed = [], [], [], [], [], [], 0
        while len(acc_x) < n_particles:
            batch = max(200, 2 * (n_particles - len(acc_x)))
            idx = rng.choice(n_particles, size=batch, p=weights)
            cand = particles[idx] + rng.multivariate_normal(np.zeros(dim), cov, size=batch)
            cand = cand[in_prior(names, cand)]
            if not len(cand):
                continue
            res = pool.map(simulate, [(names, x) for x in cand], chunksize=10)
            proposed += len(cand)
            q = np.array([np.sum(weights * kern.pdf(c - particles)) for c in cand])
            for x, qq, (d, o, z) in zip(cand, q, res):
                props.append((qq, d))
                if d <= eps_new:
                    acc_x.append(x); acc_d.append(d); acc_o.append(o); acc_z.append(z); acc_q.append(qq)
        test_idx = rng.choice(n_particles, size=20000, p=weights)
        test = particles[test_idx] + rng.multivariate_normal(np.zeros(dim), cov, size=20000)
        inside = in_prior(names, test).mean()
        m = n_particles
        X_new = np.array(acc_x[:m]); D_new = np.array(acc_d[:m]); O_new = acc_o[:m]; Z_new = acc_z[:m]
        w = prior_density(names) / (np.array(acc_q[:m]) / inside)
        w = w / w.sum()
        ess_imp = float(1 / np.sum(w ** 2))
        qs = np.array([p[0] for p in props]) / inside
        fits = np.array([p[1] <= 1 for p in props])
        ev_diag = float(np.mean(prior_density(names) / qs * fits) * inside) if len(qs) else 0.0
        particles, dist, O, Z, mh_acc = resample_move(names, pool, X_new, D_new, O_new, Z_new, w, eps_new,
                                                       cov, rng, mh_sweeps)
        weights = np.full(m, 1 / m)
        unique = len({tuple(np.round(x, 12)) for x in particles})
        eps = eps_new
        history.append({"gen": gen, "eps": eps_new, "proposed": proposed, "accept_rate": n_particles / proposed,
                        "ess_importance": ess_imp, "unique_after_move": unique, "mh_acceptance": mh_acc,
                        "evidence_diag": ev_diag, "fit_share_of_proposals": float(fits.mean())})
        log(f"{variant} gen{gen} eps={eps_new:.3f} proposed={proposed} acc={n_particles/proposed:.3f} "
            f"ess_importance={ess_imp:.1f} unique_after_move={unique} mh_acc={mh_acc:.3f} fit={fits.mean():.3f}")
        if eps_new <= 1.0:
            break
    # dedicated evidence stage at eps = 1: importance sampling from the final mixture
    cov = 2 * np.cov(particles.T, aweights=weights) + 1e-9 * np.eye(dim)
    kern = multivariate_normal(mean=np.zeros(dim), cov=cov)
    idx = rng.choice(n_particles, size=evidence_n, p=weights)
    cand = particles[idx] + rng.multivariate_normal(np.zeros(dim), cov, size=evidence_n)
    test = particles[rng.choice(n_particles, size=50000, p=weights)] + rng.multivariate_normal(np.zeros(dim), cov, size=50000)
    inside = in_prior(names, test).mean()
    keep = in_prior(names, cand); cand = cand[keep]
    res = pool.map(simulate, [(names, x) for x in cand], chunksize=10)
    q = np.array([np.sum(weights * kern.pdf(c - particles)) for c in cand]) / inside
    fits = np.array([r[0] <= 1 for r in res])
    terms = np.zeros(evidence_n); terms[np.flatnonzero(keep)] = prior_density(names) / q * fits
    boot = [rng.choice(terms, evidence_n).mean() for _ in range(2000)]
    evidence = {"estimate": float(terms.mean()), "ci90": [float(np.quantile(boot, .05)), float(np.quantile(boot, .95))],
                "proposals": evidence_n, "fit_share": float(fits.mean()), "final_eps": float(eps),
                "worlds_per_set": K_WORLDS}
    log(f"{variant} evidence at eps=1: {evidence}")
    return names, particles, weights, history, dist, O, Z, evidence


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--particles", type=int, default=400)
    ap.add_argument("--gens", type=int, default=16)
    ap.add_argument("--seed", type=int, default=20261109)
    ap.add_argument("--out", type=Path, default=Path("results"))
    ap.add_argument("--procs", type=int, default=2)
    ap.add_argument("--mh-sweeps", type=int, default=3)
    ap.add_argument("--variants", nargs="*", default=list(VARIANTS))
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    logf = (a.out / "smc_log.txt").open("a")

    def log(msg):
        print(msg, flush=True); logf.write(msg + "\n"); logf.flush()

    with Pool(a.procs) as pool:
        for j, variant in enumerate(a.variants):
            names, X, W, hist, D, O, Z, evidence = smc(variant, pool, a.particles, a.gens, a.seed + j, log,
                                                       mh_sweeps=a.mh_sweeps)
            rows = []
            for x, d, o, z, w in zip(X, D, O, Z, W):
                rows.append({"variant": variant, "weight": float(w), "worlds": CAL_WORLDS, "distance": float(d),
                             "fit_worlds": int(np.sum(np.asarray(z) <= 1)), "world_max_z": [float(v) for v in z],
                             **{n: float(v) for n, v in zip(names, x)}, **o})
            (a.out / f"posterior_{variant}.json").write_text(json.dumps({
                "variant": variant, "free": names, "calibration_worlds": CAL_WORLDS, "fit_rank": FIT_RANK,
                "history": hist, "evidence": evidence, "particles": rows}, indent=1))


if __name__ == "__main__":
    main()
