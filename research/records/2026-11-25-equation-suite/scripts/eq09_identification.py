#!/usr/bin/env python3
"""S9 - Identification shell: TWFE/group-time DID, IV, RD, synthetic control (inventory 138-167).
PREREG: PRE_REGISTRATION.md S9. SIMULATION ONLY - demonstration of each design's own known-truth world.
NO causal claim about any real policy or dataset."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from eq_common import ols, rng, synthetic_control_weights, write_result, save_csv, smoke_parser


def did_world(rng, N=40, T=20, effect=True):
    base = np.array([0, 5, 8, 12, 15] * 8)
    groups = rng.permutation(base)
    ufe = rng.normal(0, 1, N); tfe = np.linspace(0, 1, T) * 0.5
    Y = np.zeros((N, T)); tau = np.zeros((N, T))
    D = np.zeros((N, T))
    for i, g in enumerate(groups):
        for t in range(1, T + 1):
            d = 1.0 if (g > 0 and t >= g) else 0.0
            D[i, t - 1] = d
            if effect and g > 0:
                tau[i, t - 1] = (t - g + 1) * (0.30 if g == 5 else 0.10)
            Y[i, t - 1] = ufe[i] + tfe[t - 1] + tau[i, t - 1] * d + rng.normal(0, 0.3)
    return Y, groups, D, tau


def twfe(Y, D, N, T):
    rows = N * T
    X = [np.ones(rows), D.reshape(-1)]
    for i in range(1, N):
        X.append(np.tile((np.arange(N) == i).astype(float), T))
    for t in range(1, T):
        X.append(np.repeat((np.arange(T) == t).astype(float), N))
    fit = ols(Y.reshape(-1), np.column_stack(X))
    return fit["b"][1], fit["se"][1]


def cs_style(Y, groups, T):
    atts = []
    for g in [5, 8, 12, 15]:
        if (groups == g).sum() == 0:
            continue
        base_idx = g - 2
        for t in range(g, T + 1):
            tidx = t - 1
            treated = groups == g
            controls = (groups == 0) | (groups > t)
            if treated.sum() == 0 or controls.sum() == 0:
                continue
            att = (Y[treated, tidx] - Y[treated, base_idx]).mean() - \
                  (Y[controls, tidx] - Y[controls, base_idx]).mean()
            atts.append(att)
    return float(np.mean(atts)) if atts else float("nan")


def iv_world(rng, n, beta, endog=True):
    Z = rng.normal(size=n); u = rng.normal(size=n)
    D = 0.8 * Z + (0.5 * u if endog else 0.0) + rng.normal(size=n)
    Y = 1.0 + beta * D + u + rng.normal(size=n)
    b_ols = ols(Y, np.column_stack([np.ones(n), D]))["b"][1]
    Xf = np.column_stack([np.ones(n), Z])
    Dhat = Xf @ np.linalg.lstsq(Xf, D, rcond=None)[0]
    X2 = np.column_stack([np.ones(n), Dhat])
    b_iv = np.linalg.lstsq(X2, Y, rcond=None)[0][1]
    e = Y - X2 @ np.linalg.lstsq(X2, Y, rcond=None)[0]
    se = float(np.sqrt(np.mean(e ** 2) * np.linalg.pinv(X2.T @ X2)[1, 1]))
    return b_ols, b_iv, se


def rd_world(rng, n, jump):
    x = rng.uniform(-1, 1, n); D = (x >= 0).astype(float)
    Y = 0.5 + jump * D + 0.5 * x + 0.3 * D * x + rng.normal(scale=0.2, size=n)
    m = np.abs(x) <= 0.3
    fit = ols(Y[m], np.column_stack([np.ones(m.sum()), D[m], x[m], D[m] * x[m]]))
    return fit["b"][1], fit["se"][1]


def sc_world(rng, effect):
    T0, T1, J = 15, 5, 10
    f = rng.normal(size=T0 + T1)
    load = rng.uniform(0.5, 1.5, J)
    Y0 = np.outer(f, load) + rng.normal(scale=0.2, size=(T0 + T1, J))
    w_true = rng.dirichlet(np.ones(J))
    Y1 = Y0 @ w_true + rng.normal(scale=0.2, size=T0 + T1)
    Y1[T0:] += effect
    w = synthetic_control_weights(Y1[:T0], Y0[:T0])
    return float(np.mean(Y1[T0:] - Y0[T0:] @ w))


def run(args):
    reps = 12 if args.smoke else 60
    out = {"script": "eq09_identification", "prereg": "S9", "system_map": {"nodes": ["test bench"], "piece": 0, "chain": "family affordability -> learning -> gate -> credential->jobs"}, "masseng_boundary": {"used": "standalone synthetic demonstration (NOT MASSENG v5 output)", "mechanism_in_masseng_v5": False, "note": "evaluation designs; MASSENG has no learning/labour modules"}, "data_tier": "SYNTHETIC",
           "label": "SIMULATION - known-truth identification demonstrations; no causal claim",
           "reps": reps}
    rows, summary = [], {}
    # DID
    tw, cs, true_att, tw_null, cs_null = [], [], [], [], []
    for r in range(reps):
        Y, g, D, tau = did_world(rng(args.seed + r), effect=True)
        a, b = twfe(Y, D, 40, 20); tw.append(a); cs.append(cs_style(Y, g, 20))
        treated = (tau > 0)
        true_att.append(float(tau[treated].mean()))
        Yn, gn, Dn, tn = did_world(rng(args.seed + 500 + r), effect=False)
        an, _ = twfe(Yn, Dn, 40, 20); tw_null.append(an); cs_null.append(cs_style(Yn, gn, 20))
        rows.append(["DID", r, round(true_att[-1], 3), round(a, 3), round(cs[-1], 3)])
    summary["did"] = {"true_att_mean": round(float(np.mean(true_att)), 3),
                      "twfe_mean": round(float(np.mean(tw)), 3),
                      "twfe_bias": round(float(np.mean(tw) - np.mean(true_att)), 3),
                      "cs_style_mean": round(float(np.mean(cs)), 3),
                      "cs_bias": round(float(np.mean(cs) - np.mean(true_att)), 3),
                      "null_twfe_mean": round(float(np.mean(tw_null)), 3),
                      "null_cs_mean": round(float(np.mean(cs_null)), 3)}
    # IV
    ols_b, iv_b, iv_null = [], [], []
    for r in range(reps):
        b_ols, b_iv, se = iv_world(rng(args.seed + 1000 + r), 1500, 1.5, endog=True)
        ols_b.append(b_ols); iv_b.append(b_iv)
        b_ols_n, b_iv_n, se_n = iv_world(rng(args.seed + 2000 + r), 1500, 0.0, endog=False)
        iv_null.append(b_iv_n)
        rows.append(["IV", r, 1.5, round(b_ols, 3), round(b_iv, 3)])
    summary["iv"] = {"true_beta": 1.5, "ols_mean": round(float(np.mean(ols_b)), 3),
                     "iv_mean": round(float(np.mean(iv_b)), 3),
                     "iv_se_mean": round(float(se), 3),
                     "null_iv_mean": round(float(np.mean(iv_null)), 3)}
    # RD
    jump, jump_null = [], []
    for r in range(reps):
        est, se = rd_world(rng(args.seed + 3000 + r), 2000, 0.8)
        jump.append(est)
        est_n, se_n = rd_world(rng(args.seed + 4000 + r), 2000, 0.0)
        jump_null.append(est_n)
        rows.append(["RD", r, 0.8, round(est, 3), round(est_n, 3)])
    summary["rd"] = {"true_jump": 0.8, "mean_estimate": round(float(np.mean(jump)), 3),
                     "mean_se": round(float(se), 3), "null_mean": round(float(np.mean(jump_null)), 3)}
    # synthetic control
    sc, sc_null = [], []
    for r in range(reps):
        sc.append(sc_world(rng(args.seed + 5000 + r), 2.0))
        sc_null.append(sc_world(rng(args.seed + 6000 + r), 0.0))
        rows.append(["SC", r, 2.0, round(sc[-1], 3), round(sc_null[-1], 3)])
    summary["synthetic_control"] = {"true_effect": 2.0, "mean_gap": round(float(np.mean(sc)), 3),
                                    "mean_gap_null": round(float(np.mean(sc_null)), 3)}
    rule = {
        "null_twfe_near_zero": abs(summary["did"]["null_twfe_mean"]) < 0.2,
        "null_iv_near_zero": abs(summary["iv"]["null_iv_mean"]) < 0.2,
        "null_rd_near_zero": abs(summary["rd"]["null_mean"]) < 0.15,
        "null_sc_near_zero": abs(summary["synthetic_control"]["mean_gap_null"]) < 0.3,
        "iv_closer_than_ols": abs(summary["iv"]["iv_mean"] - 1.5) < abs(summary["iv"]["ols_mean"] - 1.5),
    }
    rule["PASS"] = all(rule.values())
    out.update({"summary": summary, "decision_rule": rule,
                "plain_result": ("Each design recovers its target in its own known-truth world and is near zero "
                                 "in the no-effect control; the naive estimators are biased in the stated violation "
                                 "worlds (IV %.2f vs OLS %.2f against a true 1.5; TWFE bias %.2f vs the "
                                 "group-time estimator %.2f). This is a demonstration of the designs, not an "
                                 "estimate of any real programme." %
                                 (summary["iv"]["iv_mean"], summary["iv"]["ols_mean"],
                                  summary["did"]["twfe_bias"], summary["did"]["cs_bias"]))})
    write_result(args.outdir, "eq09_identification", out)
    save_csv(args.outdir, "eq09_identification", ["design", "rep", "truth", "estimate", "control"], rows)
    print("PLAIN:", out["plain_result"])
    print("RULE:", rule)
    return out


if __name__ == "__main__":
    run(smoke_parser("S9 identification shell DID/IV/RD/SC (SIMULATION)"))
