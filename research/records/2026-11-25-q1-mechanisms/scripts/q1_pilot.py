#!/usr/bin/env python3
"""Q1 known-truth pilot (design fixed in PRE_REGISTRATION.md, committed before the first run).

Three worlds generate the same observables with different kernels; three rivals with different kernels are
fitted to the same training block with identical budgets (closed-form Gaussian MLE); the winner by held-out
predictive error is compared with the truth. A fourth control pair must score at chance.
"""
import argparse, json, os
import numpy as np

NC, NT = 24, 8
TRAIN = np.zeros((NC, NT), bool); TRAIN[:16, :6] = True
HO = ~TRAIN
WORLDS = ("W1_direct", "W2_selection", "W3_joint")
RIVALS = ("R1", "R2", "R3")


def fe(m):
    rows = np.argwhere(m)
    Z = np.zeros((rows.shape[0], NC + NT))
    Z[np.arange(rows.shape[0]), rows[:, 0]] = 1.0
    Z[np.arange(rows.shape[0]), NC + rows[:, 1]] = 1.0
    return Z[:, 1:]


def make_world(rng, truth, strength):
    c = np.arange(NC)[:, None] * 0.15; t = np.arange(NT)[None, :] * 0.10
    X = 1.0 + 0.6 * rng.standard_normal((NC, NT)) + 0.25 * np.arange(NT)[None, :]
    D = 0.8 * rng.standard_normal((NC, NT)) + 0.5 * X
    P = 0.7 * rng.standard_normal((NC, NT)) - 0.3 * X
    if truth == "W1_direct":                     # schooling causes births
        S = 2.0 + 0.9 * X + 0.9 * rng.standard_normal((NC, NT))
        F = 5.0 - 0.20 * X - strength * S + 0.35 * rng.standard_normal((NC, NT)) + 0.15 * c - 0.10 * t
    elif truth == "W2_selection":                # latent development drives both; no schooling effect
        S = 2.0 + 0.9 * D + 0.5 * rng.standard_normal((NC, NT))
        F = 5.0 - 0.55 * D + 0.35 * rng.standard_normal((NC, NT)) + 0.15 * c - 0.10 * t
    else:                                        # W3 joint choice: price moves both, correlated errors
        e = rng.multivariate_normal([0.0, 0.0], [[1.0, 0.5], [0.5, 1.0]], size=(NC, NT))
        S = 2.0 + 0.9 * X - strength * P + e[..., 0]
        F = 5.0 - 0.30 * X + 0.6 * strength * P + e[..., 1] + 0.15 * c - 0.10 * t
    A = 24.0 + (0.5 * S if truth == "W1_direct" else 0.25 * S) + rng.standard_normal((NC, NT))
    W = 3.0 - 0.25 * S + 0.4 * rng.standard_normal((NC, NT))
    return dict(S=S, F=F, X=X, A=A, W=W, P=P, D=D)


def fit(name, o, m):
    S, F, X, P = o["S"][m], o["F"][m], o["X"][m], o["P"][m]
    Zf = fe(m)
    if name == "R1":                              # F ~ S + X + FE
        Z = np.column_stack([S, X, Zf]); b, *_ = np.linalg.lstsq(Z, F, rcond=None)
        r = F - Z @ b; return dict(b=b, s2=r @ r / len(F))
    if name == "R2":                              # F ~ X + FE and S ~ X + FE
        Z = np.column_stack([X, Zf]); bf, *_ = np.linalg.lstsq(Z, F, rcond=None)
        bs, *_ = np.linalg.lstsq(Z, S, rcond=None); r = F - Z @ bf
        return dict(bf=bf, bs=bs, s2=r @ r / len(F))
    Zs = np.column_stack([P, P * P, Zf]); Zf2 = np.column_stack([P, P * P, Zf])
    bs, *_ = np.linalg.lstsq(Zs, S, rcond=None); bf, *_ = np.linalg.lstsq(Zf2, F, rcond=None)
    rs, rf = S - Zs @ bs, F - Zf2 @ bf
    C = np.cov(rs, rf); return dict(bs=bs, bf=bf, s2=(rf ** 2).mean(), rho=float(C[0, 1] / np.sqrt(C[0, 0] * C[1, 1])))


def pred(name, f, o, m):
    S, X, P = o["S"][m], o["X"][m], o["P"][m]
    if name == "R1": return np.column_stack([S, X, fe(m)]) @ f["b"]
    if name == "R2": return np.column_stack([X, fe(m)]) @ f["bf"]
    return np.column_stack([P, P * P, fe(m)]) @ f["bf"]


def implied_gradient(name, f, o):
    """Model-implied dF/dS (the statistic the micro measurement would estimate)."""
    if name == "R1": return float(f["b"][0])                       # direct coefficient
    if name == "R2": return float(f["bf"][0] / f["bs"][0])         # through X
    return float(f["bf"][1] / f["bs"][0])                          # through price^2 / price


def true_gradient(o, m):
    S, F = o["S"][m], o["F"][m]
    x = S - S.mean(); return float((x * (F - F.mean())).mean() / (x * x).mean())


def n_params(name, m):
    nfe = m.sum() and (NC + NT - 1)
    return {"R1": 2 + nfe, "R2": 2 + 2 * nfe, "R3": 4 + 2 * nfe}[name]


def bic_score(name, fit_, obs, m):
    """-2 logL + k log n, Gaussian, with the rival's own residual variance: a fair-complexity comparison."""
    r = obs["F"][m] - pred(name, fit_, obs, m)
    n = r.size
    return float(n * np.log(fit_["s2"]) + n_params(name, m) * np.log(n))


def run_block(reps, strengths, seed_dgp, seed_fit, truth_list, tag):
    out = {}
    for st in strengths:
        table = {w: {r: 0 for r in RIVALS} for w in truth_list}
        bic_tab = {w: {r: 0 for r in RIVALS} for w in truth_list}
        grad = {w: {r: 0 for r in RIVALS} for w in truth_list}
        for rep in range(reps):
            rng = np.random.default_rng([seed_dgp, int(round(st * 1000)), rep])
            for truth in truth_list:
                o = make_world(rng, truth, st)
                # fitting seed independence: rivals fitted in a seeded, rival-specific order
                order = np.random.default_rng([seed_fit, int(round(st * 1000)), rep]).permutation(list(RIVALS))
                fits = {n: fit(n, o, TRAIN) for n in order}
                mse = {n: float(((pred(n, fits[n], o, HO) - o["F"][HO]) ** 2).mean()) for n in RIVALS}
                table[truth][min(mse, key=mse.get)] += 1
                bic = {n: bic_score(n, fits[n], o, HO) for n in RIVALS}
                bic_tab[truth][min(bic, key=bic.get)] += 1
                gt = true_gradient(o, HO)
                gd = {n: abs(implied_gradient(n, fits[n], o) - gt) for n in RIVALS}
                grad[truth][min(gd, key=gd.get)] += 1
        out[str(st)] = dict(mse_recovery={w: {r: table[w][r] / reps for r in RIVALS} for w in truth_list},
                            bic_recovery={w: {r: bic_tab[w][r] / reps for r in RIVALS} for w in truth_list},
                            gradient_recovery={w: {r: grad[w][r] / reps for r in RIVALS} for w in truth_list})
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--reps", type=int, default=40)
    ap.add_argument("--out", default="results"); a = ap.parse_args()
    os.makedirs(a.out, exist_ok=True)
    strengths = (0.10, 0.25, 0.45)
    main_res = run_block(a.reps, strengths, 20261125, 777001, WORLDS, "main")
    # control 1: zero-signal (strength 0 -> worlds become identical in F|S content): must be ~chance
    zero = run_block(a.reps, (0.0,), 20261125, 777001, WORLDS, "zero")
    res = dict(reps=a.reps, strengths=list(strengths), main=main_res, zero_signal_control=zero)
    json.dump(res, open(f"{a.out}/pilot_recovery.json", "w"), indent=1)
    print(json.dumps(res, indent=1))


if __name__ == "__main__":
    main()
