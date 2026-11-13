"""ABC-SMC (population Monte Carlo) calibration for each mechanism variant.

Distance: the largest standardized deviation across the published patterns (calibrate.distances).
A run fits when every pattern is inside its tolerance band (distance <= 1).

Model evidence: proposals in each generation come from a known mixture density q, so
mean(prior(theta) / q(theta) * 1[distance <= eps]) estimates the prior probability of fitting,
P(distance <= eps | variant). Ratios of these are ABC Bayes factors under the stated uniform priors.
"""
import argparse
import json
from dataclasses import asdict
from multiprocessing import Pool
from pathlib import Path
import numpy as np
from scipy.stats import multivariate_normal
from calibrate import distances, TARGETS
from model import PRIORS, VARIANTS, Params, run


def free_names(variant):
    return [k for k in PRIORS if k not in ("diversion", "favour") or k in VARIANTS[variant]]


def to_params(names, x):
    values = dict(zip(names, x))
    for mech in ("diversion", "favour"):
        values.setdefault(mech, 0.0)
    return Params(**values)


def simulate(args):
    names, x, seed = args
    out = run(to_params(names, x), int(seed))
    z = distances(out)
    return max(z.values()), out, z


def in_prior(names, x):
    lo = np.array([PRIORS[n][0] for n in names]); hi = np.array([PRIORS[n][1] for n in names])
    return np.all((x >= lo) & (x <= hi), axis=-1)


def prior_density(names):
    return 1.0 / np.prod([PRIORS[n][1] - PRIORS[n][0] for n in names])


def smc(variant, pool, n_particles, max_gen, seed, log, evidence_n=4000):
    names = free_names(variant)
    dim = len(names)
    rng = np.random.default_rng(seed)
    lo = np.array([PRIORS[n][0] for n in names]); hi = np.array([PRIORS[n][1] for n in names])
    seed_counter = seed * 10_000_000
    history = []
    # generation 0: prior
    n0 = n_particles * 10
    X = lo + (hi - lo) * rng.random((n0, dim))
    seeds = seed_counter + np.arange(n0); seed_counter += n0
    res = pool.map(simulate, [(names, x, s) for x, s in zip(X, seeds)], chunksize=50)
    D = np.array([r[0] for r in res])
    Q = np.full(n0, prior_density(names))                  # proposal density = prior
    order = np.argsort(D)[:n_particles]
    particles, dist, weights = X[order], D[order], np.full(n_particles, 1 / n_particles)
    eps = dist.max()
    history.append({"gen": 0, "eps": float(eps), "proposed": n0, "evidence_eps1": float((D <= 1).mean())})
    log(f"{variant} gen0 eps={eps:.3f} prior fit share={np.mean(D <= 1):.5f}")
    all_props = []  # (x, q, d, out, z, seed) for evidence at eps=1 and posterior extraction
    for gen in range(1, max_gen + 1):
        eps_new = max(1.0, float(np.quantile(dist, 0.5)))
        cov = 2 * np.cov(particles.T, aweights=weights) + 1e-9 * np.eye(dim)
        kern = multivariate_normal(mean=np.zeros(dim), cov=cov)
        accepted_x, accepted_d, accepted_q, proposed = [], [], [], 0
        gen_props = []
        while len(accepted_x) < n_particles:
            batch = max(200, 2 * (n_particles - len(accepted_x)))
            idx = rng.choice(n_particles, size=batch, p=weights)
            cand = particles[idx] + rng.multivariate_normal(np.zeros(dim), cov, size=batch)
            cand = cand[in_prior(names, cand)]
            if not len(cand):
                continue
            seeds = seed_counter + np.arange(len(cand)); seed_counter += len(cand)
            res = pool.map(simulate, [(names, x, s) for x, s in zip(cand, seeds)], chunksize=25)
            proposed += len(cand)
            # mixture proposal density, including truncation to the prior box (normalizer estimated)
            q = np.array([np.sum(weights * kern.pdf(c - particles)) for c in cand])
            for x, s, qq, (d, out, z) in zip(cand, seeds, q, res):
                gen_props.append((x, qq, d, out, z, int(s)))
                if d <= eps_new:
                    accepted_x.append(x); accepted_d.append(d); accepted_q.append(qq)
        # truncation normalizer: share of kernel mass inside the prior box (Monte Carlo)
        test_idx = rng.choice(n_particles, size=20000, p=weights)
        test = particles[test_idx] + rng.multivariate_normal(np.zeros(dim), cov, size=20000)
        inside = in_prior(names, test).mean()
        X_new = np.array(accepted_x[:n_particles]); D_new = np.array(accepted_d[:n_particles])
        q_new = np.array(accepted_q[:n_particles]) / inside
        w = prior_density(names) / q_new
        weights = w / w.sum(); particles, dist = X_new, D_new
        # evidence estimate at eps=1 from this generation's proposals
        qs = np.array([g[1] for g in gen_props]) / inside
        fits = np.array([g[2] <= 1 for g in gen_props])
        ev = float(np.mean(prior_density(names) / qs * fits) * inside) if len(qs) else 0.0
        ess = 1 / np.sum(weights ** 2)
        history.append({"gen": gen, "eps": eps_new, "proposed": proposed, "accept_rate": n_particles / proposed,
                        "ess": float(ess), "evidence_eps1": ev, "fit_share_of_proposals": float(fits.mean())})
        log(f"{variant} gen{gen} eps={eps_new:.3f} proposed={proposed} acc={n_particles/proposed:.3f} "
            f"ess={ess:.0f} fit={fits.mean():.3f} evidence={ev:.3g}")
        all_props = gen_props
        if eps_new <= 1.0:
            break
    # final posterior sample: last generation's accepted particles, with weights
    final = [(x, d, out, z, s) for (x, q, d, out, z, s) in all_props if d <= eps_new][:n_particles]
    # dedicated evidence stage at eps = 1: a large proposal batch from the final mixture
    cov = 2 * np.cov(particles.T, aweights=weights) + 1e-9 * np.eye(dim)
    kern = multivariate_normal(mean=np.zeros(dim), cov=cov)
    idx = rng.choice(n_particles, size=evidence_n, p=weights)
    cand = particles[idx] + rng.multivariate_normal(np.zeros(dim), cov, size=evidence_n)
    test = particles[rng.choice(n_particles, size=50000, p=weights)] + rng.multivariate_normal(np.zeros(dim), cov, size=50000)
    inside = in_prior(names, test).mean()
    keep = in_prior(names, cand); cand = cand[keep]
    seeds = seed_counter + np.arange(len(cand))
    res = pool.map(simulate, [(names, x, s) for x, s in zip(cand, seeds)], chunksize=25)
    q = np.array([np.sum(weights * kern.pdf(c - particles)) for c in cand]) / inside
    fits = np.array([r[0] <= 1 for r in res])
    terms = np.zeros(evidence_n); terms[np.flatnonzero(keep)] = prior_density(names) / q * fits
    boot = [rng.choice(terms, evidence_n).mean() for _ in range(2000)]
    evidence = {"estimate": float(terms.mean()), "ci90": [float(np.quantile(boot, .05)), float(np.quantile(boot, .95))],
                "proposals": evidence_n, "fit_share": float(fits.mean()), "final_eps": float(eps_new)}
    log(f"{variant} evidence at eps=1: {evidence}")
    return names, particles, weights, history, final, evidence


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--particles", type=int, default=400)
    ap.add_argument("--gens", type=int, default=16)
    ap.add_argument("--seed", type=int, default=20261109)
    ap.add_argument("--out", type=Path, default=Path("results"))
    ap.add_argument("--procs", type=int, default=2)
    ap.add_argument("--variants", nargs="*", default=list(VARIANTS))
    a = ap.parse_args()
    a.out.mkdir(parents=True, exist_ok=True)
    logf = (a.out / "smc_log.txt").open("a")

    def log(msg):
        print(msg, flush=True); logf.write(msg + "\n"); logf.flush()

    with Pool(a.procs) as pool:
        for j, variant in enumerate(a.variants):
            names, X, W, hist, final, evidence = smc(variant, pool, a.particles, a.gens, a.seed + j, log)
            rows = []
            for (x, d, out, z, s), w in zip(final, W):
                rows.append({"variant": variant, "weight": float(w), "seed": s, "distance": float(d),
                             **{n: float(v) for n, v in zip(names, x)}, **out})
            (a.out / f"posterior_{variant}.json").write_text(json.dumps({
                "variant": variant, "free": names, "history": hist, "evidence": evidence, "particles": rows}, indent=1))


if __name__ == "__main__":
    main()
