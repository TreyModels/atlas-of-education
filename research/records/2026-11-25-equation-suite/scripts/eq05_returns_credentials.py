#!/usr/bin/env python3
"""S1 - Mincer returns, ability bias, IV (inventory 42-56). PREREG: PRE_REGISTRATION.md S1.
SIMULATION ONLY. No causal claim about any real economy; the DGP is stipulated."""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
from eq_common import ols, rng, write_result, save_csv, smoke_parser


def two_sls(y, S, Z, X_exog):
    """2SLS for y = b*S + X_exog*c + e with instrument Z. SEs homoskedastic 2SLS."""
    X = np.column_stack([S] + ([X_exog] if X_exog is not None else []))
    Zf = np.column_stack([Z] + ([X_exog] if X_exog is not None else []))
    Xhat = Zf @ np.linalg.lstsq(Zf, X, rcond=None)[0]
    b = np.linalg.lstsq(Xhat, y, rcond=None)[0]
    e = y - X @ b
    sigma2 = float(np.mean(e ** 2))
    cov = sigma2 * np.linalg.pinv(Xhat.T @ Xhat)
    se = np.sqrt(np.maximum(np.diag(cov), 0.0))
    return b[0], se[0]


def one_rep(rng, n, ability_bias):
    a = rng.normal(size=n)
    v = rng.normal(size=n)
    Z = rng.normal(size=n)
    X = rng.uniform(0, 40, n)
    S = 10.0 + (2.2 if ability_bias else 0.0) * a + 1.5 * v + 1.0 * Z
    lw = 1.0 + 0.09 * S + 0.12 * a + 0.04 * X - 0.0005 * X ** 2 + rng.normal(scale=0.3, size=n)
    ols_naive = ols(lw, np.column_stack([np.ones(n), S]))["b"][1]
    ols_oracle = ols(lw, np.column_stack([np.ones(n), S, a]))["b"][1]
    b_iv, se_iv = two_sls(lw, S, Z, None)
    # experience profile with the schooling coefficient recovered by oracle OLS
    Xq = np.column_stack([np.ones(n), S, a, X, X ** 2])
    prof = ols(lw, Xq)["b"]
    mret10 = prof[3] + 2 * prof[4] * 10
    return {"ols_naive": ols_naive, "ols_oracle": ols_oracle,
            "iv": b_iv, "iv_se": se_iv,
            "exact_pct_iv": 100.0 * (np.exp(b_iv) - 1.0),
            "mret_exp10": mret10}


def run(args):
    reps = 40 if args.smoke else 120
    n = 800 if args.smoke else 4000
    out = {"script": "eq05_returns_credentials", "prereg": "S5", "data_tier": "SYNTHETIC",
           "label": "SIMULATION - stipulated Mincer DGP; no causal claim",
           "truth": 0.09, "reps": reps, "n": n}
    rows, summary = [], {}
    for world, bias in [("ability_bias", True), ("null_no_ability_bias", False)]:
        b_naive, b_or, b_iv, cover_iv, cover_naive = [], [], [], 0, 0
        exact, mret = [], []
        for r in range(reps):
            d = one_rep(rng(args.seed + 1000 * (1 if bias else 2) + r), n, bias)
            b_naive.append(d["ols_naive"] - 0.09)
            b_or.append(d["ols_oracle"] - 0.09)
            b_iv.append(d["iv"] - 0.09)
            cover_iv += int(abs(d["iv"] - 0.09) <= 1.96 * d["iv_se"])
            cover_naive += int(abs(d["ols_naive"] - 0.09) <= 1.96 * 0.0 + 1.96 * 0.02)
            exact.append(d["exact_pct_iv"])
            mret.append(d["mret_exp10"])
            rows.append([world, r, round(d["ols_naive"], 4), round(d["ols_oracle"], 4),
                         round(d["iv"], 4), round(d["exact_pct_iv"], 2), round(d["mret_exp10"], 4)])
        summary[world] = {
            "mean_bias_ols_naive": round(float(np.mean(b_naive)), 4),
            "mean_bias_ols_oracle": round(float(np.mean(b_or)), 4),
            "mean_bias_2sls": round(float(np.mean(b_iv)), 4),
            "ols_naive_abs_bias_gt_0.01_share": round(float(np.mean(np.abs(b_naive) > 0.01)), 2),
            "exact_pct_mean": round(float(np.mean(exact)), 2),
            "marginal_return_experience_10_mean": round(float(np.mean(mret)), 4),
        }
    # pre-declared decision rule
    bias_s, null_s = summary["ability_bias"], summary["null_no_ability_bias"]
    rule = {
        "bias_world_naive_biased": bias_s["mean_bias_ols_naive"] > 0.01,
        "bias_world_iv_bias_smaller": abs(bias_s["mean_bias_2sls"]) < bias_s["mean_bias_ols_naive"],
        "null_world_naive_close": abs(null_s["mean_bias_ols_naive"]) <= 0.01,
        "null_world_iv_close": abs(null_s["mean_bias_2sls"]) <= 0.02,
    }
    rule["PASS"] = all(rule.values())
    mv = {"specs": ["ols_no_controls", "ols_with_ability_oracle", "2sls"],
          "estimates": {"ols_no_controls": round(0.09 + bias_s["mean_bias_ols_naive"], 4),
                        "ols_with_ability_oracle": round(0.09 + bias_s["mean_bias_ols_oracle"], 4),
                        "2sls": round(0.09 + bias_s["mean_bias_2sls"], 4)}}
    mv["range"] = [min(mv["estimates"].values()), max(mv["estimates"].values())]
    mv["spec_robust"] = all(v > 0 for v in mv["estimates"].values())
    out.update({"summary": summary, "multiverse": mv, "decision_rule": rule,
                "system_map": {"nodes": ["jobs-credentials"], "piece": 4, "chain": "family affordability -> learning -> gate -> credential->jobs"},
           "masseng_boundary": {"used": "standalone synthetic demonstration (NOT MASSENG v5 output)", "mechanism_in_masseng_v5": False, "note": "standalone synthetic demonstration; not a MASSENG v5 output"},
                "plain_result": ("Under the stipulated ability-bias DGP the naive regression overstates the return "
                                 "(mean bias %.3f) while 2SLS is much closer (mean bias %.3f); with no ability bias "
                                 "both recover the 9%% return. This is a demonstration of the estimator, not an "
                                 "estimate of any real return." %
                                 (bias_s["mean_bias_ols_naive"], bias_s["mean_bias_2sls"]))})
    write_result(args.outdir, "eq01_returns", out)
    save_csv(args.outdir, "eq01_returns",
             ["world", "rep", "ols_naive", "ols_oracle", "iv", "exact_pct_iv", "mret_exp10"], rows)
    print("PLAIN:", out["plain_result"])
    print("RULE:", rule)
    return out


if __name__ == "__main__":
    run(smoke_parser("S1 Mincer returns / ability bias / IV (SIMULATION)"))
