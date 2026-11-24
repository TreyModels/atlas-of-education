"""H4: out-of-seed tie-breaker test on measured observables, with controls and placebos."""
import numpy as np
from scipy import stats

import measure
import model

SEED_K = lambda k: 20261125 + 100 * int(k)  # noqa: E731
CAL_BLOCK = list(range(0, 20))
HELDOUT_BLOCK = list(range(20, 80))
REPL_BLOCK = list(range(80, 140))
CHANCE = 1.0 / float(len(model.WORLDS))
ALPHA = 0.05


def _rng(seed):
    # Paired design: the survey RNG depends only on the seed, not on the world label, so the
    # s=0 labels are identical and s=1 worlds are compared on the same survey draws.
    return np.random.default_rng(int(seed) + 992_631)


def build_unit(world, s, seed, nuisance, ban=0.0):
    res = model.run_unit(world, s, seed, ban=ban, **nuisance)
    ys = model.year_stats(res)
    post = {k: v[model.SHOCK_YEAR + 5:] for k, v in res.items()}  # t = 15..24
    meas = measure.survey_unit(post, _rng(seed))
    tb = measure.tiebreakers(meas)
    theta = model.theta_of(world, s)
    return {
        "world": world if s == 1 else "Z", "s": s, "seed": seed,
        "T1": tb["T1"], "T2": tb["T2"], "T3": tb["T3"], "T4": tb["T4"],
        "theta": [theta["w_pov"], theta["w_push"], theta["w_tutor"], theta["div"]],
        "d_ger": float(ys["ger"][15:].mean() - ys["ger"][:10].mean()),
        "d_cl": float(ys["cl_observed"][15:].mean() - ys["cl_observed"][:10].mean()),
    }


def build_block(block, nuisances, s=1, worlds=model.WORLDS, seed_log=None):
    units = []
    for k in block:
        seed = SEED_K(k)
        for w in worlds:
            units.append(build_unit(w, s, seed, nuisances[w]))
        if seed_log is not None and (k + 1) % 10 == 0:
            seed_log.append({"stage": "h4_units", "block": block[0], "s": s, "seeds_done": k + 1})
    return units


def _stack(units, key):
    return np.array([u[key] for u in units], dtype=np.float64)


def _labels(units):
    return np.array([u["world"] for u in units])


def _finite_mask(X):
    return np.all(np.isfinite(X), axis=1)


def classify(train, test, key, worlds=tuple(model.WORLDS)):
    Xtr = _stack(train, key)
    Xte = _stack(test, key)
    mtr = _finite_mask(Xtr)
    mte = _finite_mask(Xte)
    Xtr, ytr = Xtr[mtr], _labels(train)[mtr]
    Xte, yte = Xte[mte], _labels(test)[mte]
    if len(Xtr) < len(worlds) * 2 or len(Xte) == 0:
        return {"accuracy": float("nan"), "n_train": int(len(Xtr)), "n_test": int(len(Xte)),
                "per_world_recall": {}, "valid": False}
    mu = Xtr.mean(axis=0)
    sd = Xtr.std(axis=0)
    sd[sd == 0] = 1.0
    Ztr, Zte = (Xtr - mu) / sd, (Xte - mu) / sd
    cents = {w: Ztr[ytr == w].mean(axis=0) for w in worlds}
    dist = np.column_stack([np.linalg.norm(Zte - cents[w], axis=1) for w in worlds])
    pred = np.array(worlds)[np.argmin(dist, axis=1)]
    acc = float(np.mean(pred == yte))
    recall = {w: float(np.mean(pred[yte == w] == w)) for w in worlds}
    p = float(stats.binomtest(int(np.sum(pred == yte)), len(yte), CHANCE,
                              alternative="greater").pvalue)
    return {"accuracy": acc, "n_train": int(len(Xtr)), "n_test": int(len(Xte)),
            "per_world_recall": recall, "binom_p_one_sided": p, "valid": True}


def chance_band(n):
    se = np.sqrt(CHANCE * (1.0 - CHANCE) / n)
    return [float(CHANCE - 1.96 * se), float(CHANCE + 1.96 * se)]


def admissibility(train, key, threshold=0.90):
    """R^2 of each feature component on the known DGP weights + macro moments (calibration only)."""
    X = _stack(train, key)
    ok = _finite_mask(X)
    W = np.array([u["theta"] for u in train], dtype=np.float64)[ok]
    macro = np.array([[u["d_ger"], u["d_cl"]] for u in train], dtype=np.float64)[ok]
    X = X[ok]
    A = np.column_stack([np.ones(len(X)), W, macro])
    r2s = []
    for j in range(X.shape[1]):
        y = X[:, j]
        beta, *_ = np.linalg.lstsq(A, y, rcond=None)
        resid = y - A @ beta
        sst = np.sum((y - y.mean()) ** 2)
        r2s.append(float(1.0 - np.sum(resid ** 2) / sst) if sst > 0 else 0.0)
    worst = max(r2s)
    return {"r2_per_component": r2s, "max_r2": worst,
            "rejected": bool(worst > threshold), "threshold": threshold}


def holm(pvals):
    """Holm step-down; returns adjusted p-values in the original order."""
    order = np.argsort(pvals)
    m = len(pvals)
    adj = np.empty(m)
    running = 0.0
    for rank, i in enumerate(order):
        val = (m - rank) * pvals[i]
        running = max(running, val)
        adj[i] = min(1.0, running)
    return adj


def label_permutation(train, test, key, n_perm=100, rng_seed=20261124):
    rng = np.random.default_rng(rng_seed)
    obs = classify(train, test, key)
    if not obs["valid"]:
        return {"observed": obs, "permutation_acc": [], "p_perm": float("nan")}
    Xtr = _stack(train, key)
    ytr = _labels(train)
    mtr = _finite_mask(Xtr)
    Xtr, ytr = Xtr[mtr], ytr[mtr]
    mu, sd = Xtr.mean(axis=0), Xtr.std(axis=0)
    sd[sd == 0] = 1.0
    Ztr = (Xtr - mu) / sd
    Xte = _stack(test, key)
    yte = _labels(test)
    mte = _finite_mask(Xte)
    Zte = (Xte[mte] - mu) / sd
    worlds = np.array(list(model.WORLDS))
    accs = []
    for _ in range(n_perm):
        perm = rng.permutation(ytr)
        cents = {w: Ztr[perm == w].mean(axis=0) for w in worlds}
        dist = np.column_stack([np.linalg.norm(Zte - cents[w], axis=1) for w in worlds])
        pred = worlds[np.argmin(dist, axis=1)]
        accs.append(float(np.mean(pred == yte[mte])))
    accs = np.array(accs)
    return {"observed_accuracy": obs["accuracy"], "permutation_median": float(np.median(accs)),
            "permutation_p95": float(np.quantile(accs, 0.95)),
            "p_perm": float((np.sum(accs >= obs["accuracy"]) + 1) / (n_perm + 1))}


def algebraic_equivalence(heldout_block, nuisance, seed_log=None):
    """ban=1.8 vs ban=2.0 are algebraically identical in the kernel (threshold rule)."""
    units = []
    diffs = []
    for k in heldout_block:
        seed = SEED_K(k)
        a = model.run_unit("P", 1, seed, ban=1.8, **nuisance)
        b = model.run_unit("P", 1, seed, ban=2.0, **nuisance)
        if k == heldout_block[0]:
            for key in a:
                diffs.append(float(np.max(np.abs(a[key].astype(np.float64)
                                            - b[key].astype(np.float64)))))
        for ban_val, res in ((1.8, a), (2.0, b)):
            post = {key: v[model.SHOCK_YEAR + 5:] for key, v in res.items()}
            tb = measure.tiebreakers(measure.survey_unit(post, _rng(seed)))
            units.append({"world": f"ban{ban_val}", "T1": tb["T1"], "T2": tb["T2"],
                          "T3": tb["T3"], "T4": tb["T4"]})
    bin_acc = {}
    for key in ("T1", "T2", "T3", "T4"):
        X = _stack(units, key)
        y = np.array([u["world"] for u in units])
        ok = _finite_mask(X)
        X, y = X[ok], y[ok]
        mu, sd = X.mean(0), X.std(0)
        sd[sd == 0] = 1
        Z = (X - mu) / sd
        cent = {w: Z[y == w].mean(0) for w in ("ban1.8", "ban2.0")}
        pred = np.where(np.linalg.norm(Z - cent["ban1.8"], axis=1)
                        <= np.linalg.norm(Z - cent["ban2.0"], axis=1), "ban1.8", "ban2.0")
        bin_acc[key] = float(np.mean(pred == y))
    n = 2 * len(heldout_block)
    band = [0.5 - 1.96 * np.sqrt(0.25 / n), 0.5 + 1.96 * np.sqrt(0.25 / n)]
    return {"note": "ban=1.8 and ban=2.0 are algebraically identical (kernel threshold rule)",
            "max_abs_kernel_diff": max(diffs) if diffs else None,
            "accuracies": bin_acc, "n": n, "chance_band_95": band,
            "within_band": {k: bool(band[0] <= v <= band[1]) for k, v in bin_acc.items()},
            "pass": bool(all(band[0] <= v <= band[1] for v in bin_acc.values()))}


def run_h4(calibration, heldout, replication, s0_units, nuisance_by_world, seed_log):
    results = {}
    for key in ("T1", "T2", "T3", "T4"):
        results[key] = {
            "admissibility": admissibility(calibration, key),
            "heldout": classify(calibration, heldout, key),
            "replication": classify(calibration, replication, key),
            "label_permutation": label_permutation(calibration, heldout, key),
        }
    # macro-only control (matched moments should not identify the world)
    class _U(dict):
        pass

    for u in calibration + heldout:
        pass
    macro_cal = [{"world": u["world"], "M": np.array([u["d_ger"], u["d_cl"]], float)}
                 for u in calibration]
    macro_ho = [{"world": u["world"], "M": np.array([u["d_ger"], u["d_cl"]], float)}
                for u in heldout]
    # reuse classify machinery by exposing M as a feature vector
    def classify_vectors(train_v, test_v):
        Xtr = np.array([u["M"] for u in train_v])
        ytr = np.array([u["world"] for u in train_v])
        Xte = np.array([u["M"] for u in test_v])
        yte = np.array([u["world"] for u in test_v])
        mu, sd = Xtr.mean(0), Xtr.std(0)
        sd[sd == 0] = 1
        Ztr, Zte = (Xtr - mu) / sd, (Xte - mu) / sd
        worlds = np.array(["P", "S", "C"])
        cents = {w: Ztr[ytr == w].mean(0) for w in worlds}
        pred = worlds[np.argmin(np.column_stack(
            [np.linalg.norm(Zte - cents[w], axis=1) for w in worlds]), axis=1)]
        return float(np.mean(pred == yte))

    macro_acc = classify_vectors(macro_cal, macro_ho)

    s0_cal = [u for u in s0_units["calibration"]]
    s0_ho = [u for u in s0_units["heldout"]]
    s0_acc = classify(s0_cal, s0_ho, "T1")
    # For s=0 the labels are the same model; the classifier must fall to chance on every T.
    s0_all = {k: classify(s0_cal, s0_ho, k) for k in ("T1", "T2", "T3", "T4")}

    pvals = np.array([results[k]["heldout"]["binom_p_one_sided"] for k in results])
    adj = holm(pvals)
    band = chance_band(results["T1"]["heldout"]["n_test"] if results["T1"]["heldout"]["valid"] else 180)
    rejected = [k for k in results if results[k]["admissibility"]["rejected"]]
    eligible = [k for k in results if not results[k]["admissibility"]["rejected"]]
    separators = []
    for key, p_adj in zip(results, adj):
        ho = results[key]["heldout"]
        rep = results[key]["replication"]
        is_eligible = key not in rejected
        beats = bool(is_eligible and ho["valid"] and ho["accuracy"] > band[1] and p_adj < ALPHA)
        survives = bool(is_eligible and rep["valid"] and rep["accuracy"] > band[1])
        results[key]["holm_adjusted_p"] = float(p_adj)
        results[key]["eligible_for_confirmatory_test"] = bool(is_eligible)
        results[key]["beats_chance_heldout"] = beats
        results[key]["survives_replication"] = survives
        if beats and survives:
            separators.append(key)

    placebo = {
        "s0_control": {"accuracy": s0_acc.get("accuracy"), "chance_band": band,
                       "within_band": bool(s0_acc.get("valid")
                                           and band[0] <= s0_acc["accuracy"] <= band[1]),
                       "all_tiebreakers": s0_all},
        "macro_only_control_accuracy": macro_acc,
        "label_permutation": {k: results[k]["label_permutation"] for k in results},
    }
    algebraic = algebraic_equivalence(HELDOUT_BLOCK, nuisance_by_world["P"], seed_log)
    invalid = (not placebo["s0_control"]["within_band"]) or (not algebraic["pass"])
    if invalid:
        verdict_code, verdict = "cannot_test", "cannot test (a pre-registered control failed)"
    elif not eligible:
        verdict_code = "cannot_test"
        verdict = ("cannot test (F3): every tie-breaker was rejected by the admissibility gate as a "
                   "transform of the DGP weights (max R^2: "
                   + ", ".join(f"{k}={results[k]['admissibility']['max_r2']:.3f}" for k in rejected) + ")")
    elif separators:
        verdict_code, verdict = "separates", f"separates (tie-breakers: {separators})"
    else:
        verdict_code, verdict = "cannot_separate", "cannot separate (no tie-breaker beats chance after Holm)"

    return {
        "units": {"calibration": len(calibration), "heldout": len(heldout),
                  "replication": len(replication)},
        "seeds": {"calibration": [SEED_K(CAL_BLOCK[0]), SEED_K(CAL_BLOCK[-1])],
                  "heldout": [SEED_K(HELDOUT_BLOCK[0]), SEED_K(HELDOUT_BLOCK[-1])],
                  "replication": [SEED_K(REPL_BLOCK[0]), SEED_K(REPL_BLOCK[-1])]},
        "batch_layout": model.LAYOUT,
        "chance_band_95": band,
        "tiebreakers": results,
        "holms_adjusted_p": {k: float(v) for k, v in zip(results, adj)},
        "separators": separators,
        "rejected_by_admissibility_gate": rejected,
        "eligible_for_confirmatory_test": eligible,
        "f3_all_rejected": bool(not eligible),
        "placebos": placebo,
        "algebraic_equivalence_placebo": algebraic,
        "verdict": verdict, "verdict_code": verdict_code,
        "label": "SIMULATION",
    }
