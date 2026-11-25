#!/usr/bin/env python3
"""P0-03 (external audit) — corrected synthetic population + 100-population parameter recovery.

What this replaces
------------------
The shipped ABC (`docs/audit/gpu_abc_bundle/gpu_bray_abc_and_contest_surface.py:50-54`) built a
degenerate synthetic population:

    n_pupils = 630
    is_g12   = [0]*420 + [1]*210          # 2:1 grade split
    is_urban = [1]*210 + [0]*420          # first 210 pupils are the urban ones
    log_y    ~ N(0,1)  i.i.d. per pupil
    school_gap ~ U(0,1) i.i.d. per pupil

so (a) the G12 x urban cell is EMPTY (every G12 pupil is rural), (b) there are no school
identifiers and no within-school dependence, (c) school quality is unrelated to household income,
(d) the advertised five moments contain only three independent participation moments (overall is
identically (2/3)G9 + (1/3)G12), and the provider-choice parameter delta is analytic
(delta = ln(0.32/0.68) = -0.7537718023763802, EXTERNAL_AUDIT_GPU_2026-11-25.md P0-02). The ABC
therefore cannot identify 5 parameters from 3 independent moments (rank <= 3 < 5).

This script
-----------
1. builds a CORRECTED synthetic population:
   * properly crossed grade x urban cells, including G12-urban (construction guarantees non-empty);
   * explicit school IDs (8 schools, each with both grades) and school-level random effects on
     ability, school quality and household income -> within-school dependence;
   * a positive, non-degenerate income-school-quality relationship (correlation rho_inc_qual);
   * moment sets rich enough to identify the five analytically-reduced parameters
     theta = [b0_eff, b_income, b_school_gap, delta_g12, urban_demand] (delta fixed analytically);
   * the legacy degenerate design is regenerated for the old-vs-new comparison;
2. runs a 100-population-per-configuration ABC recovery experiment (prior draws with common random
   numbers), and reports bias / RMSE / coverage, posterior distributions, and per-population
   Jacobian rank;
3. retains ALL accepted draws and posterior-predictive moments (parquet);
4. compares old vs new on the moments, on identification rank, and on the analytic-delta estimates.

Design choices and their empirical justification are documented in
`docs/audit/SYNTHETIC_DGP_VALIDATION.md` (every structural assumption is labelled ASSUMPTION, not
an estimate; the only data-anchored inputs are the benchmark moment targets of the shipped ABC:
participation 0.73, G9 0.67, G12 0.85, urban-rural gap 0.14, own share 0.68).

Run (host or box):
    OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 OMP_NUM_THREADS=1 \
    /Users/treymenefee/neon-boot/venv/bin/python docs/audit/code/dgp_validation.py \
        --out-dir results/audit --workers 4 --n-pop 100 --n-draws 20000 --seed 20261125
"""
from __future__ import annotations

import argparse
import json
import math
import os
import time
from concurrent.futures import ProcessPoolExecutor
import multiprocessing as mp

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------------------- fixed inputs
# The shipped ABC's benchmark moments (Bray/Cambodia-Asia, as committed at 045a63e). These are the
# only data-anchored numbers in this script; everything else is a labelled design assumption.
BENCH = dict(participation=0.73, g9=0.67, g12=0.85, urban_gap=0.14, own_share=0.68)

# P0-02: provider choice is analytic. P(own | tutoring) = 1/(1+exp(delta)) = 0.68.
DELTA_ANALYTIC = math.log((1.0 - BENCH["own_share"]) / BENCH["own_share"])   # -0.7537718023763802

PARAMS = ["b0_eff", "b_income", "b_school_gap", "delta_g12", "urban_demand"]
PRIOR_LO = np.array([-1.0, 0.0, 0.0, 0.0, -0.5])
PRIOR_HI = np.array([2.5, 2.0, 2.5, 2.5, 1.5])
PRIOR = list(zip(PRIOR_LO.tolist(), PRIOR_HI.tolist()))

# True parameter vectors for the recovery experiment (inside the prior support; two separated regions).
TRUTHS = {
    "A": np.array([0.30, 0.55, 0.70, 1.10, 0.35]),
    "B": np.array([-0.20, 1.10, 0.35, 0.60, 0.90]),
}

# Structural design assumptions (documented + sensitivity in the report; NOT estimates).
DESIGN = dict(
    n_schools=32,                # 16 urban + 16 rural; every school contains both grades
    rho_inc_qual=0.50,           # corr(household log income, school quality): positive SES gradient
    school_quality_sd=1.0,
    within_school_share=0.55,    # variance share of the school random effect for income/ability
    school_gap_sd=0.45,          # school-level part of the "school_gap" covariate (resources)
    school_gap_idio_sd=0.25,     # within-school part (kept non-degenerate)
    ability_sd=1.0,
)

TOL_CROSSED = dict(cell=0.05, inc_q=0.05, qual_t=0.05, own=0.03, overall=0.05, g9=0.05, g12=0.05,
                   urban_gap=0.04)
TOL_LEGACY = dict(overall=0.05, g9=0.05, g12=0.05, urban_gap=0.04, own=0.06)


# --------------------------------------------------------------------------------------- population
def make_population(kind, n_per_cell, rng, design=DESIGN):
    """Return a dict of per-pupil arrays and school metadata.

    Corrected design ('crossed'):
      * 8 schools, 4 urban / 4 rural, each school teaches BOTH grades;
      * every grade x urban cell is populated through multiple schools (construction invariant);
      * school random effects (quality q_s, ability a_s, income m_s) with
            corr(log_y, q_s) = rho_inc_qual  (positive, non-degenerate);
      * school_gap = school-level resource gap + idiosyncratic pupil noise.
    Legacy design ('legacy'): exact shipped construction (420 G9 + 210 G12, 210 urban first, no
    school IDs, i.i.d. covariates) so the old-vs-new comparison is apples-to-apples.
    """
    if kind == "crossed":
        ns = int(design["n_schools"])
        urban_school = np.array([True] * (ns // 2) + [False] * (ns - ns // 2))
        q_s = rng.normal(0.0, design["school_quality_sd"], size=ns)          # school quality
        a_s = rng.normal(0.0, 1.0, size=ns)                                   # school ability effect
        # Income loading: school quality raises mean log income (positive SES-school gradient).
        # We build log_y = rho*quality_z + sqrt(1-rho^2)*idio so that Var(log_y)=1 and
        # corr(log_y, quality) = rho exactly (in expectation).
        rho = float(design["rho_inc_qual"])
        grades, urbans, schools, ys, gaps, abilities = [], [], [], [], [], []
        per_cell = int(n_per_cell)
        for g12 in (0, 1):
            for urb in (0, 1):
                pool = np.flatnonzero(urban_school == bool(urb))
                # spread each cell evenly over the schools of its urban type -> cell x school crossed
                sids = np.repeat(pool, int(math.ceil(per_cell / len(pool))))[:per_cell]
                n = len(sids)
                q = q_s[sids]
                idio = rng.standard_normal(n)
                log_y = rho * q + math.sqrt(max(1.0 - rho ** 2, 0.0)) * idio
                gap_s = rng.normal(0.0, design["school_gap_sd"], size=ns)[sids]
                gap = gap_s + rng.normal(0.0, design["school_gap_idio_sd"], size=n)
                abil = a_s[sids] + rng.normal(0.0, design["ability_sd"], size=n)
                grades.append(np.full(n, g12))
                urbans.append(np.full(n, urb))
                schools.append(sids)
                ys.append(log_y)
                gaps.append(gap)
                abilities.append(abil)
        pop = dict(
            kind=kind,
            grade_g12=np.concatenate(grades).astype(np.int8),
            urban=np.concatenate(urbans).astype(np.int8),
            school_id=np.concatenate(schools).astype(np.int16),
            log_y=np.concatenate(ys),
            school_gap=np.concatenate(gaps),
            ability=np.concatenate(abilities),
            school_quality=q_s[np.concatenate(schools)],
            n_schools=ns,
        )
    elif kind == "legacy":
        n = 630
        pop = dict(
            kind=kind,
            grade_g12=np.concatenate([np.zeros(420, np.int8), np.ones(210, np.int8)]),
            urban=np.concatenate([np.ones(210, np.int8), np.zeros(420, np.int8)]),
            school_id=np.full(n, -1, np.int16),          # NO school identifiers
            log_y=rng.standard_normal(n),
            school_gap=rng.random(n),                    # U(0,1) i.i.d. per pupil
            ability=rng.standard_normal(n),
            school_quality=np.full(n, np.nan),
            n_schools=0,
        )
    else:
        raise ValueError(kind)
    pop["n"] = int(len(pop["log_y"]))
    return pop


def participation(pop, theta):
    """P(any paid tutoring) for each draw in ``theta`` (B,5) -> (B, n) array.

    With V_none = 0, V_own = V, V_other = V + delta and delta analytic, the 3-option softmax
    collapses to a logistic: p_any = sigmoid(V + ln(1+exp(delta))).  This is an exact identity of
    the shipped utility specification, not an approximation.
    """
    theta = np.atleast_2d(np.asarray(theta, float))
    c = math.log1p(math.exp(DELTA_ANALYTIC))
    b0, bi, bg, dg, ud = theta.T
    V = (b0[:, None]
         + bi[:, None] * pop["log_y"][None, :]
         + bg[:, None] * pop["school_gap"][None, :]
         + dg[:, None] * pop["grade_g12"][None, :]
         + ud[:, None] * pop["urban"][None, :])
    return 1.0 / (1.0 + np.exp(-(V + c)))


def _group_means(p, groups, counts, moment_names, out_cols):
    """p: (B,n); groups: list of index arrays -> append group means to out."""
    B = p.shape[0]
    for g, name in zip(groups, moment_names):
        if len(g) == 0:
            out_cols.append(np.full(B, np.nan))
        else:
            out_cols.append(p[:, g].mean(axis=1))


def moments(pop, theta, moment_set):
    """Moment vector(s) for a population.

    moment_set 'crossed' (12 moments, used for recovery):
       4 grade x urban cell participation means; 4 within-population income-quartile means;
       3 school-quality-tercile means; own-teacher share (analytic).
    moment_set 'legacy' (the shipped 5 advertised moments):
       overall, G9, G12, urban-rural contrast (first 210 vs last 420, as shipped), own share.
    """
    theta = np.atleast_2d(np.asarray(theta, float))
    p = participation(pop, theta)
    B = p.shape[0]
    own = np.full(B, 1.0 / (1.0 + math.exp(DELTA_ANALYTIC)))
    cols, names = [], []
    if moment_set == "crossed":
        g12 = pop["grade_g12"].astype(bool)
        urb = pop["urban"].astype(bool)
        cells = [("part_g9_rural", ~g12 & ~urb), ("part_g9_urban", ~g12 & urb),
                 ("part_g12_rural", g12 & ~urb), ("part_g12_urban", g12 & urb)]
        for nm, mask in cells:
            idx = np.flatnonzero(mask)
            cols.append(p[:, idx].mean(axis=1) if len(idx) else np.full(B, np.nan))
            names.append(nm)
        # income quartiles (within population) and school-quality terciles (school-level q)
        qb = np.quantile(pop["log_y"], [0.25, 0.5, 0.75])
        inc_q = np.searchsorted(qb, pop["log_y"])
        for j in range(4):
            idx = np.flatnonzero(inc_q == j)
            cols.append(p[:, idx].mean(axis=1) if len(idx) else np.full(B, np.nan))
            names.append(f"part_inc_q{j + 1}")
        sq = pop["school_quality"]
        if np.all(np.isfinite(sq)):
            tb = np.quantile(sq, [1 / 3, 2 / 3])
            tq = np.searchsorted(tb, sq)
            for j in range(3):
                idx = np.flatnonzero(tq == j)
                cols.append(p[:, idx].mean(axis=1) if len(idx) else np.full(B, np.nan))
                names.append(f"part_qual_t{j + 1}")
        else:  # legacy design has no school quality -> these moments do not exist
            for j in range(3):
                cols.append(np.full(B, np.nan))
                names.append(f"part_qual_t{j + 1}")
        # within-school school-gap quartiles (idiosyncratic resource variation identifies b_school_gap)
        gq = np.quantile(pop["school_gap"], [0.25, 0.5, 0.75])
        gapq = np.searchsorted(gq, pop["school_gap"])
        for j in range(4):
            idx = np.flatnonzero(gapq == j)
            cols.append(p[:, idx].mean(axis=1) if len(idx) else np.full(B, np.nan))
            names.append(f"part_gap_q{j + 1}")
        cols.append(own)
        names.append("own_share")
    elif moment_set == "legacy":
        g9 = pop["grade_g12"] == 0
        g12 = pop["grade_g12"] == 1
        urban_first210 = np.zeros(pop["n"], bool)
        urban_first210[:210] = True            # shipped construction: the first 210 are urban
        cols += [p.mean(axis=1), p[:, np.flatnonzero(g9)].mean(axis=1),
                 p[:, np.flatnonzero(g12)].mean(axis=1),
                 p[:, np.flatnonzero(urban_first210)].mean(axis=1)
                 - p[:, np.flatnonzero(~urban_first210)].mean(axis=1),
                 own]
        names += ["part_overall", "part_g9", "part_g12", "urban_gap", "own_share"]
    else:
        raise ValueError(moment_set)
    return np.column_stack(cols), names


def moment_targets(moment_set, truth, seed, n_per_cell=4000):
    """Benchmark targets: moments at ``truth`` on a large fresh population (approximate expectation)."""
    rng = np.random.default_rng(seed + 991)
    pop = make_population("crossed", n_per_cell, rng)
    m, names = moments(pop, truth, moment_set)
    return m[0], names, pop


def moment_group_sizes(pop, moment_set):
    """Number of pupils behind each moment (for sample-size-aware ABC tolerances)."""
    n = pop["n"]
    if moment_set == "crossed":
        g12 = pop["grade_g12"].astype(bool); urb = pop["urban"].astype(bool)
        cells = [~g12 & ~urb, ~g12 & urb, g12 & ~urb, g12 & urb]
        sizes = [int(m.sum()) for m in cells]
        qb = np.quantile(pop["log_y"], [0.25, 0.5, 0.75])
        inc_q = np.searchsorted(qb, pop["log_y"])
        sizes += [int((inc_q == j).sum()) for j in range(4)]
        sq = pop["school_quality"]
        if np.all(np.isfinite(sq)):
            tb = np.quantile(sq, [1 / 3, 2 / 3])
            tq = np.searchsorted(tb, sq)
            sizes += [int((tq == j).sum()) for j in range(3)]
        else:
            sizes += [1, 1, 1]
        gq = np.quantile(pop["school_gap"], [0.25, 0.5, 0.75])
        gapq = np.searchsorted(gq, pop["school_gap"])
        sizes += [int((gapq == j).sum()) for j in range(4)]
        sizes += [n]
        return np.array(sizes, float)
    if moment_set == "legacy":
        return np.array([n, int((pop["grade_g12"] == 0).sum()), int((pop["grade_g12"] == 1).sum()),
                         min(210, n), n], float)
    raise ValueError(moment_set)


def tolerances_for(names, sizes, probs):
    """ABC tolerances: floor of the benchmark tolerance, widened to 2.5 finite-sample SE.

    Targets are benchmark moments; a population of n pupils estimates them with sampling error
    sqrt(p(1-p)/n_g).  With a fixed 0.05 tolerance the n=50 configuration would accept almost no
    prior draw for pure sampling-noise reasons (not because the model is wrong), so the tolerance is
    the larger of the benchmark tolerance and 2.5 SE.  The same rule is used for every configuration.
    """
    base = []
    for nm in names:
        if nm == "own_share":
            base.append(0.03)
        elif nm == "urban_gap":
            base.append(0.04)
        else:
            base.append(0.05)
    base = np.array(base, float)
    p = np.clip(np.asarray(probs, float), 1e-6, 1 - 1e-6)
    se = np.sqrt(p * (1 - p) / np.maximum(sizes, 1.0))
    return np.maximum(base, 2.5 * se)


# --------------------------------------------------------------------------------------- one population
def recover_one(job):
    """Run the ABC recovery for one (configuration, population) unit. Returns a serialisable dict."""
    cfg_id, pop_id, kind, truth_name, n_per_cell, moment_set, n_draws, seed, prior_lo, prior_hi = job
    truth = TRUTHS[truth_name]
    rng = np.random.default_rng(seed)
    # Targets: common across populations of a configuration (benchmark moments; computed once per
    # call is cheap enough and keeps the function pure).
    target, names, target_pop = moment_targets(moment_set, truth, seed=seed)
    pop = make_population(kind, n_per_cell, rng)
    m_obs, _ = moments(pop, truth, moment_set)
    m_obs = m_obs[0]
    sizes = moment_group_sizes(pop, moment_set)
    tols = tolerances_for(names, sizes, m_obs)

    # Prior draws with common random numbers (same U matrix for every population of a config).
    prng = np.random.default_rng(seed + 7001)
    U = prng.random((n_draws, len(PARAMS)))
    draws = prior_lo + U * (prior_hi - prior_lo)

    m_draws = np.empty((n_draws, len(names)), float)
    chunk = 4000
    for lo in range(0, n_draws, chunk):
        m_draws[lo:lo + chunk], _ = moments(pop, draws[lo:lo + chunk], moment_set)

    z = np.nanmax(np.abs(m_draws - m_obs[None, :]) / tols[None, :], axis=1)
    acc = z <= 1.0
    escalation = 0
    while int(acc.sum()) == 0 and escalation < 2:      # documented fallback: widen x2, x4
        escalation += 1
        tols = tols * 2.0
        z = np.nanmax(np.abs(m_draws - m_obs[None, :]) / tols[None, :], axis=1)
        acc = z <= 1.0
    n_acc = int(acc.sum())
    post = draws[acc]
    post_mom = m_draws[acc]

    # posterior predictive on a fresh population from the same distribution (accepted draws only)
    pred = np.empty((0, len(names)), float)
    if n_acc:
        fresh = make_population(kind, n_per_cell, np.random.default_rng(seed + 31))
        pred, _ = moments(fresh, post[: min(n_acc, 500)], moment_set)

    # ---------------------------------------------------------------- identification diagnostics
    # Numerical Jacobian of the moment map at truth, on this population's covariates.
    base, _ = moments(pop, truth[None, :], moment_set)
    J = np.zeros((len(names), len(PARAMS)))
    for j in range(len(PARAMS)):
        h = 1e-5
        tp = truth.copy(); tp[j] += h
        tm = truth.copy(); tm[j] -= h
        mp, _ = moments(pop, tp[None, :], moment_set)
        mm, _ = moments(pop, tm[None, :], moment_set)
        J[:, j] = (mp[0] - mm[0]) / (2 * h)
    sv = np.linalg.svd(J, compute_uv=False)
    rank = int(np.sum(sv > max(sv[0], 1e-300) * 1e-8)) if len(sv) else 0
    # independent moment count: remove exact linear redundancies in the observed moment vector
    sv_m = np.linalg.svd(np.column_stack([m_obs, np.ones_like(m_obs)]), compute_uv=False)

    # posterior summary
    if n_acc >= 2:
        mean = post.mean(0)
        sd = post.std(0, ddof=1)
        q025, q975 = np.percentile(post, [2.5, 97.5], axis=0)
    else:
        mean = np.full(5, np.nan); sd = np.full(5, np.nan)
        q025 = np.full(5, np.nan); q975 = np.full(5, np.nan)

    return dict(
        config=cfg_id, pop_id=pop_id, kind=kind, truth_name=truth_name, n_per_cell=n_per_cell,
        n_pupils=pop["n"], moment_set=moment_set, n_draws=n_draws,
        truth=truth, post_mean=mean, post_sd=sd, q025=q025, q975=q975,
        n_accepted=n_acc, accept_rate=n_acc / n_draws, tol_escalation=escalation,
        m_obs=np.asarray(m_obs), moment_names=names, tols=tols,
        jac_rank=rank, jac_sv=sv, jac_sv_moments=sv_m,
        g12_urban_cell=int(np.sum((pop["grade_g12"] == 1) & (pop["urban"] == 1))),
        n_schools=pop["n_schools"],
        school_icc_income=_icc(pop),
        accepted_theta=post, accepted_moments=post_mom,
        posterior_predictive=pred,
        target=np.asarray(target),
    )


def _icc(pop):
    """Within-school intraclass correlation of household log income (0 for the legacy design)."""
    sid = pop["school_id"]
    if pop["n_schools"] <= 0:
        return float("nan")
    ok = sid >= 0
    y = pop["log_y"][ok]
    g = sid[ok]
    schools = np.unique(g)
    n = len(y)
    if len(schools) < 2 or n <= len(schools):
        return float("nan")
    grand = y.mean()
    ss_between = sum(len(y[g == s]) * (y[g == s].mean() - grand) ** 2 for s in schools)
    ss_total = float(np.sum((y - grand) ** 2))
    k = len(schools)
    ms_between = ss_between / max(k - 1, 1)
    ms_within = (ss_total - ss_between) / max(n - k, 1)
    n_bar = n / k
    denom = ms_between + (n_bar - 1) * ms_within
    return float((ms_between - ms_within) / denom) if denom > 0 else 0.0


# --------------------------------------------------------------------------------------- driver
def build_jobs(n_pop, n_draws, seed, workers):
    """Configurations: two truths, two sample sizes, crossed design + legacy degenerate contrast."""
    # Configurations: sample-size ladder on the corrected design (weak -> usable identification),
    # a second truth region, and the legacy degenerate design as the contrast.
    configs = [
        dict(id="NEW-crossed-n100-truthA", kind="crossed", truth="A", n_per_cell=100,
             moment_set="crossed", n_pop=n_pop),
        dict(id="NEW-crossed-n400-truthA", kind="crossed", truth="A", n_per_cell=400,
             moment_set="crossed", n_pop=n_pop),
        dict(id="NEW-crossed-n1000-truthA", kind="crossed", truth="A", n_per_cell=1000,
             moment_set="crossed", n_pop=n_pop),
        dict(id="NEW-crossed-n400-truthB", kind="crossed", truth="B", n_per_cell=400,
             moment_set="crossed", n_pop=n_pop),
        dict(id="OLD-degenerate-truthA", kind="legacy", truth="A", n_per_cell=0,
             moment_set="legacy", n_pop=n_pop),
    ]
    jobs = []
    for ci, cfg in enumerate(configs):
        for p in range(cfg["n_pop"]):
            jobs.append((cfg["id"], p, cfg["kind"], cfg["truth"], cfg["n_per_cell"],
                         cfg["moment_set"], n_draws,
                         seed + 100000 * ci + 17 * p + 3,
                         PRIOR_LO.copy(), PRIOR_HI.copy()))
    return configs, jobs


def summarise(results, configs):
    """Recovery metrics per configuration, plus old-vs-new moment/rank comparison."""
    rows, met_rows, acc_rows, pred_rows, rank_rows = [], [], [], [], []
    for r in results:
        for j, pname in enumerate(PARAMS):
            t = r["truth"][j]
            rows.append(dict(config=r["config"], pop_id=r["pop_id"], param=pname,
                             truth=t, post_mean=r["post_mean"][j], post_sd=r["post_sd"][j],
                             q025=r["q025"][j], q975=r["q975"][j],
                             bias=r["post_mean"][j] - t,
                             covered=bool(r["q025"][j] <= t <= r["q975"][j]) if np.isfinite(r["q025"][j]) else False,
                             n_accepted=r["n_accepted"], accept_rate=r["accept_rate"],
                             tol_escalation=r["tol_escalation"],
                             jac_rank=r["jac_rank"], n_schools=r["n_schools"],
                             g12_urban_cell=r["g12_urban_cell"], moment_set=r["moment_set"]))
        met_rows.append(dict(config=r["config"], pop_id=r["pop_id"],
                             m_obs=tuple(r["m_obs"]), target=tuple(r["target"]),
                             moment_names=tuple(r["moment_names"])))
        rank_rows.append(dict(config=r["config"], pop_id=r["pop_id"], jac_rank=r["jac_rank"],
                              min_sv=float(r["jac_sv"][-1]), max_sv=float(r["jac_sv"][0]),
                              n_moments=len(r["moment_names"]),
                              school_icc_income=r["school_icc_income"],
                              n_schools=r["n_schools"], g12_urban_cell=r["g12_urban_cell"]))
        for k in range(len(r["accepted_theta"])):
            acc_rows.append(dict(config=r["config"], pop_id=r["pop_id"],
                                 **{("theta_" + p): float(r["accepted_theta"][k, j])
                                    for j, p in enumerate(PARAMS)},
                                 max_z=float("nan")))
        for k in range(len(r["posterior_predictive"])):
            pred_rows.append(dict(config=r["config"], pop_id=r["pop_id"],
                                  **{("ppc_" + nm): float(r["posterior_predictive"][k, j])
                                     for j, nm in enumerate(r["moment_names"])}))

    per_param = pd.DataFrame(rows)
    summary = {}
    for cfg in configs:
        cid = cfg["id"]
        sub = per_param[per_param.config == cid]
        entry = dict(n_pop=int(sub.pop_id.nunique()),
                     mean_n_accepted=float(sub.n_accepted.mean()),
                     mean_accept_rate=float(sub.accept_rate.mean()),
                     jac_rank_mean=float(sub.jac_rank.mean()),
                     jac_rank_min=int(sub.jac_rank.min()),
                     jac_rank_max=int(sub.jac_rank.max()),
                     g12_urban_cell_mean=float(sub.g12_urban_cell.mean()),
                     n_schools_mean=float(sub.n_schools.mean()),
                     params={})
        for pname in PARAMS:
            pp = sub[sub.param == pname]
            bias = pp.bias.to_numpy(float)
            rmse = float(np.sqrt(np.nanmean(bias ** 2)))
            entry["params"][pname] = dict(
                truth_A=_truth_for(cid, pname),
                bias_mean=float(np.nanmean(bias)), rmse=rmse,
                rmse_rel=rmse / max(abs(_truth_for(cid, pname)), 1e-9),
                coverage95=float(np.nanmean(pp.covered.to_numpy(bool))),
                post_sd_mean=float(np.nanmean(pp.post_sd)),
            )
        summary[cid] = entry

    # analytic delta comparison (old shipped estimates vs the analytic value)
    delta_note = dict(
        analytic_delta=DELTA_ANALYTIC,
        shipped_7param_delta=-0.8241,
        shipped_6param_delta=-0.6682,
        shipped_7param_error=abs(-0.8241 - DELTA_ANALYTIC),
        shipped_6param_error=abs(-0.6682 - DELTA_ANALYTIC),
    )
    return dict(per_param=per_param,
                moments=pd.DataFrame(met_rows),
                accepted=pd.DataFrame(acc_rows),
                predictive=pd.DataFrame(pred_rows),
                rank=pd.DataFrame(rank_rows),
                summary=summary, delta_note=delta_note)


def _truth_for(cid, pname):
    for tname, arr in TRUTHS.items():
        if tname in cid:
            return float(arr[PARAMS.index(pname)])
    return float("nan")


def old_vs_new_comparison(summary, moments_df, rank_df):
    """Compact old-vs-new table: moments, G12xurban, school count, rank, analytic delta error."""
    out = {}
    for cid in summary:
        sub = moments_df[moments_df.config == cid]
        rk = rank_df[rank_df.config == cid]
        names = list(sub.moment_names.iloc[0])
        obs = np.array([np.mean([row[i] for row in sub.m_obs]) for i in range(len(names))])
        tgt = np.array([np.mean([row[i] for row in sub.target]) for i in range(len(names))])
        out[cid] = dict(
            moments={nm: dict(observed=float(o), target=float(t)) for nm, o, t in zip(names, obs, tgt)},
            g12_urban_cell_mean=float(rk.g12_urban_cell.mean()),
            n_schools_mean=float(rk.n_schools.mean()),
            school_icc_income_mean=float(np.nanmean(rk.school_icc_income)),
            jac_rank_mean=float(rk.jac_rank.mean()),
            jac_rank_min=int(rk.jac_rank.min()),
            jac_rank_max=int(rk.jac_rank.max()),
            n_moments=int(rk.n_moments.iloc[0]),
        )
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out-dir", default="results/audit")
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--n-pop", type=int, default=100)
    ap.add_argument("--n-draws", type=int, default=20000)
    ap.add_argument("--seed", type=int, default=20261125)
    args = ap.parse_args()
    os.makedirs(args.out_dir, exist_ok=True)
    t0 = time.time()
    configs, jobs = build_jobs(args.n_pop, args.n_draws, args.seed, args.workers)

    ctx = mp.get_context("fork")
    with ProcessPoolExecutor(max_workers=args.workers, mp_context=ctx) as ex:
        results = list(ex.map(recover_one, jobs, chunksize=1))

    # -------- acceptance guards (P0-03): the corrected design must satisfy the stated invariants
    new_res = [r for r in results if r["kind"] == "crossed"]
    assert new_res, "no corrected-design populations"
    assert all(r["g12_urban_cell"] > 0 for r in new_res), "G12 x urban cell empty in the corrected design"
    assert all(r["n_schools"] > 0 for r in new_res), "no school identifiers in the corrected design"
    assert len([r for r in results if r["kind"] == "legacy"]) == args.n_pop, "legacy contrast incomplete"
    assert all(len(r["accepted_theta"]) > 0 for r in results), "some population retained no accepted draws"

    out = summarise(results, configs)
    out["old_vs_new"] = old_vs_new_comparison(out["summary"], out["moments"], out["rank"])

    # -------- persist everything (ALL accepted draws + posterior predictive + diagnostics)
    out["per_param"].to_parquet(os.path.join(args.out_dir, "dgp_recovery_samples.parquet"), index=False)
    out["accepted"].to_parquet(os.path.join(args.out_dir, "dgp_accepted_draws.parquet"), index=False)
    out["predictive"].to_parquet(os.path.join(args.out_dir, "dgp_posterior_predictive.parquet"), index=False)
    out["rank"].to_parquet(os.path.join(args.out_dir, "dgp_rank_diagnostics.parquet"), index=False)
    out["moments"].to_parquet(os.path.join(args.out_dir, "dgp_moment_recovery.parquet"), index=False)

    meta = dict(
        p0="P0-03 corrected synthetic DGP + 100-population parameter recovery",
        date_utc=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        runtime_sec=round(time.time() - t0, 2),
        workers=args.workers, n_pop_per_config=args.n_pop, n_draws=args.n_draws, seed=args.seed,
        params=PARAMS, prior=list(PRIOR), truths={k: v.tolist() for k, v in TRUTHS.items()},
        delta_analytic=DELTA_ANALYTIC, delta_note=out["delta_note"],
        design_assumptions=DESIGN, benchmark_moments=BENCH,
        configs=[{k: v for k, v in c.items()} for c in configs],
        summary=out["summary"], old_vs_new=out["old_vs_new"],
        artifacts=["dgp_recovery_samples.parquet", "dgp_accepted_draws.parquet",
                   "dgp_posterior_predictive.parquet", "dgp_rank_diagnostics.parquet",
                   "dgp_moment_recovery.parquet"],
    )
    with open(os.path.join(args.out_dir, "dgp_validation_summary.json"), "w") as f:
        json.dump(meta, f, indent=2, default=float)

    print(json.dumps({k: meta[k] for k in ("runtime_sec", "delta_analytic")}, indent=2))
    for cid, ent in out["summary"].items():
        line = [f"{cid}: n={ent['n_pop']} rank={ent['jac_rank_min']}..{ent['jac_rank_max']} "
                f"accept={ent['mean_n_accepted']:.1f}"]
        for pname in PARAMS:
            e = ent["params"][pname]
            line.append(f"{pname}: bias={e['bias_mean']:+.3f} rmse={e['rmse']:.3f} cov={e['coverage95']:.2f}")
        print("  " + " | ".join(line))


if __name__ == "__main__":
    main()
