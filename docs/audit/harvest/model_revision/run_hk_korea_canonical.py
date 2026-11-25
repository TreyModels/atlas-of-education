#!/usr/bin/env python3
"""Canonical HK/Korea shadow-education contest runner (model-revision 2026-11-25).

SIMULATION only: every number this script writes is stochastic model output, not an empirical estimate.

Implements the pre-registered revision plan (`REVISION_PLAN.md`, incl. amendment 1):

  * canonical spec = the 420-generation parameterisation (N=400, T=70) ported onto the current patched
    `Engine(modules, **params)` / `E.R` engine, with
      - a persistent Korean Grade-9 placement consequence (`elite9`: upper-secondary learning boost and a
        Grade-12 contest effective-input boost; V1), and
      - expected top-K admission probabilities estimated from the gate's own Gumbel-max Plackett-Luce
        mechanism (core.contest_prob / core._fit_contest_prob), used by both household values and effort choice;
  * seat denominators (applicants, seats, applicant:seat ratio, realised admission) recorded per arm and gate;
  * expected-vs-realised admission diagnostics by expected-probability decile and effort quintile
    (recorded by the engine during the scored window, i.e. by the same runs that produce the results);
  * variants: V1 canonical (G9 placement on), V2 G9 contest removed, V3 G9 contest with no lasting
    consequence for winner or loser (the reviewed phantom-prize configuration);
  * 30 matched seeds per arm/variant, paired arm-baseline deltas, seed-level uncertainty.

Usage (from the package root, with ENGINE_ROOT pointing at the directory that contains `eduengine/`):

    python run_hk_korea_canonical.py calibrate --out results/calibration_sweep.json --seeds 10
    python run_hk_korea_canonical.py policy --out results/policy_arms.json --seeds 30 \
        --price-mult <chosen> --alpha-mult <chosen>

Environment: N_WORKERS (default min(56, cpu_count)); ENGINE_ROOT (optional if the engine is 4 levels up).
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor

warnings.filterwarnings("ignore")


def _engine_dir() -> str:
    env = os.environ.get("ENGINE_ROOT")
    if env:
        return env
    here = os.path.dirname(os.path.abspath(__file__))
    for rel in ("engine", "../../../../engine", "../../../engine", "../../engine"):
        cand = os.path.abspath(os.path.join(here, rel))
        if os.path.isdir(os.path.join(cand, "eduengine")):
            return cand
    raise SystemExit("cannot locate engine/ — set ENGINE_ROOT to the directory containing eduengine/")


ENGINE_DIR = _engine_dir()
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)

import numpy as np  # noqa: E402
from eduengine.core import Engine  # noqa: E402
from eduengine.modules.labour import QueueLabour  # noqa: E402
from eduengine.modules.schools import PrivateSchools, PublicSchools  # noqa: E402
from eduengine.modules.sdg4 import SDG4  # noqa: E402
from eduengine.modules.tutoring import TutoringMarket  # noqa: E402

SEEDS = list(range(30))
CALIB_SEEDS = list(range(10))
HOLDOUT_SEEDS = list(range(10, 30))

# ---------------------------------------------------------------- canonical parameterisation (420 generation)
CANON_COMMON = dict(
    N=400,
    T=70,
    measure_from=35,
    subsist=0.15,
    borrow=0.5,
    p_own=99.0,
    p_firm=99.0,
    contest_x0=2.0,
    contest_min_e=0.25,
    g9_consequence=1.0,
    g9_learn_boost=0.20,
    g9_contest_boost=0.35,
    g9_elite_logw=0.0,
)

HK_BASE = dict(
    CANON_COMMON,
    y_median=3.0,
    y_sigma=0.65,
    urban_share=1.0,
    elite_logw=0.85,
    contest_r=1.5,
    contest_alpha=1.2,
    contest_price=0.12,
    contest_max_e=4.0,
    gates=[
        dict(kind="bar", bar=0.0),
        dict(kind="bar", bar=0.0),
        dict(kind="contest", share=0.23, fail="track", elite_logw=0.85),
        dict(kind="bar", bar=0.0),
    ],
)

KR_BASE = dict(
    CANON_COMMON,
    y_median=3.0,
    y_sigma=0.60,
    urban_share=0.85,
    elite_logw=1.15,
    contest_r=1.6,
    contest_alpha=1.25,
    contest_price=0.11,
    contest_max_e=4.5,
    gates=[
        dict(kind="bar", bar=0.0),
        # Korean Grade-9 gate: canonical keeps the 420 design (set_voc default True -> losers tracked vocational);
        # V1 adds the persistent winners' placement consequences via elite9.
        dict(kind="contest", share=0.35, fail="track", elite_logw=0.35),
        dict(kind="contest", share=0.12, fail="track", elite_logw=1.15),
        dict(kind="bar", bar=0.0),
    ],
)


def _with_g12_share(params, share):
    p = dict(params)
    gates = [dict(g) for g in p["gates"]]
    gates[2]["share"] = share
    p["gates"] = gates
    return p


def _with_dv_scale(params, mult):
    p = dict(params)
    p["elite_logw"] = p["elite_logw"] * mult
    gates = [dict(g) for g in p["gates"]]
    for g in gates:
        if "elite_logw" in g:
            g["elite_logw"] = g["elite_logw"] * mult
    p["gates"] = gates
    return p


def build_arms(price_mult=1.0, alpha_mult=1.0, jurisdictions=("HK", "KR")):
    """All 18 policy arms (9 per jurisdiction) of the 540/420 design, on the canonical parameterisation."""
    specs = []
    for jur, base, s_mod, s_maj, s_label_mod, s_label_maj in [
        ("HK", HK_BASE, 0.28, 0.50, "S=0.28", "S=0.50"),
        ("KR", KR_BASE, 0.16, 0.40, "S12=0.16", "S12=0.40"),
    ]:
        if jur not in jurisdictions:
            continue
        base = dict(base, contest_price=base["contest_price"] * price_mult,
                    contest_alpha=base["contest_alpha"] * alpha_mult)
        arms = [
            ("Baseline", f"Baseline ({'S=0.23' if jur == 'HK' else 'S12=0.12'})", base),
            ("CF1a", "CF1a (+50% tax)", dict(base, contest_price=base["contest_price"] * 1.5)),
            ("CF1b", "CF1b (-50% cap)", dict(base, contest_max_e=base["contest_max_e"] * 0.5)),
            ("CF2a", f"CF2a ({s_label_mod})", _with_g12_share(base, s_mod)),
            ("CF2b", f"CF2b ({s_label_maj})", _with_g12_share(base, s_maj)),
            ("CF3a", "CF3a (dV -30%)", _with_dv_scale(base, 0.70)),
            ("CF3b", "CF3b (dV -50%)", _with_dv_scale(base, 0.50)),
            ("CF4a", "CF4a (Win-Win: dV -50% + Cap -50%)",
             dict(_with_dv_scale(base, 0.50), contest_max_e=base["contest_max_e"] * 0.5)),
            ("CF4b", f"CF4b (Win-Win: dV -50% + Seats {s_label_maj})",
             _with_g12_share(_with_dv_scale(base, 0.50), s_maj)),
        ]
        for arm_id, label, prm in arms:
            specs.append((jur, arm_id, label, prm))
    return specs


def build_variants(price_mult=1.0, alpha_mult=1.0):
    """Return (variant, jurisdiction, arm_id, label, params) for V1/V2/V3."""
    specs = []
    for jur, arm_id, label, prm in build_arms(price_mult, alpha_mult, ("HK", "KR")):
        specs.append(("V1_canonical", jur, arm_id, label, prm))
    kr_arms = build_arms(price_mult, alpha_mult, ("KR",))
    for jur, arm_id, label, prm in kr_arms:
        # V2: G9 contest removed -> pass-through bar gate (no G9 tournament, no tracking)
        p2 = dict(prm)
        gates = [dict(g) for g in p2["gates"]]
        gates[1] = dict(kind="bar", bar=0.0)
        p2["gates"] = gates
        specs.append(("V2_g9_removed", jur, arm_id, label, p2))
        # V3: G9 contest present, anticipated premium prices prep, but no realised consequence for winner or loser
        #     (set_voc=False removes the losers' track consequence; g9_consequence=0 removes the placement channel)
        p3 = dict(prm, g9_consequence=0.0)
        gates = [dict(g) for g in p3["gates"]]
        gates[1] = dict(gates[1], set_voc=False)
        p3["gates"] = gates
        specs.append(("V3_g9_no_consequence", jur, arm_id, label, p3))
    return specs


# ---------------------------------------------------------------- single run
def _run_single(task):
    variant, jur, arm_id, seed, params = task
    mods = [PublicSchools(), PrivateSchools(), TutoringMarket(), QueueLabour(), SDG4()]
    E = Engine(mods, **dict(params, seed=seed))
    E.run()

    m = E.p["measure_from"]
    R = E.R
    k12_spend = float(np.mean(R["tut_k12_spend"][m:]))
    k12_rate = float(np.mean(R["tut_k12_rate"][m:]))
    g12_rate = float(np.mean(R["tut_g12_rate"][m:]))
    rq = np.mean(np.array(R["tut_k12_rate_by_q"][m:], float), 0)
    sq = np.mean(np.array(R["tut_k12_spend_by_q"][m:], float), 0)
    contest_e_mean = float(np.mean(R["contest_e_mean"][m:]))
    by_grade = np.mean(np.array(R["tut_by_grade"][m:], float), 0)

    X = E.ALL
    sel = (X["cohort"] >= m) & (X["cohort"] <= E.p["T"] - 14) & (X["g"] >= 12)
    el = X["elite"][sel]
    qq = X["q"][sel]
    elite_q5_share = float(np.mean(qq[el] == 4)) if el.any() else float("nan")
    elite_share = float(np.mean(el))

    # realised return of a non-terminal placement (V1 vs V3 sensitivity; descriptive only, endogenous selection)
    e9 = X["elite9"]
    has_inc = np.isfinite(X["inc"]) & (X["cred"] >= 2)
    g9 = {}
    for tag, mask in (("placed", has_inc & e9), ("not_placed", has_inc & ~e9)):
        if mask.sum() > 0:
            g9[tag] = dict(
                n=int(mask.sum()),
                g12_elite_pct=100.0 * float(np.mean(X["elite"][mask])),
                mean_L=float(np.mean(X["L"][mask])),
                mean_log_wage=float(np.mean(np.log(np.maximum(X["inc"][mask], 1e-3)))),
            )
        else:
            g9[tag] = dict(n=0)
    placed_q5 = float(np.mean(X["q"][e9] == 4)) if e9.any() else float("nan")

    return dict(
        variant=variant,
        jurisdiction=jur,
        arm_id=arm_id,
        seed=seed,
        k12_spend=k12_spend,
        k12_rate_pct=100.0 * k12_rate,
        g12_pct=100.0 * g12_rate,
        q5_q1_gap_pp=100.0 * float(rq[4] - rq[0]),
        q5_q1_spend_ratio=float(sq[4] / max(sq[0], 1e-9)),
        elite_q5_share_pct=100.0 * elite_q5_share,
        elite_share_pct=100.0 * elite_share,
        k12_rate_by_q=[float(100.0 * v) for v in rq],
        k12_spend_by_q=[float(v) for v in sq],
        contest_e_mean=contest_e_mean,
        grade9_tut_pct=float(100.0 * by_grade[8]),
        grade12_tut_pct=float(100.0 * by_grade[11]),
        g9_placement=dict(elite9_share_pct=100.0 * float(np.mean(e9)), placed_q5_pct=placed_q5,
                          g12_elite_pct=g9["placed"]["g12_elite_pct"] if g9["placed"]["n"] else float("nan"),
                          not_placed_g12_elite_pct=g9["not_placed"]["g12_elite_pct"] if g9["not_placed"]["n"] else float("nan"),
                          return_rows=g9),
        contest_calib=_pack_calib(E.contest_calib),
    )


def _pack_calib(calib):
    out = {}
    for m_, C in calib.items():
        out[str(m_)] = {kk: (list(vv) if isinstance(vv, list) else vv) for kk, vv in C.items()}
    return out


# ---------------------------------------------------------------- aggregation helpers
def _stats(vals):
    arr = np.asarray(vals, float)
    arr = arr[np.isfinite(arr)]
    if len(arr) == 0:
        return dict(mean=float("nan"), sd=float("nan"), ci95_lo=float("nan"), ci95_hi=float("nan"), n=0)
    mean = float(np.mean(arr))
    sd = float(np.std(arr, ddof=1)) if len(arr) > 1 else 0.0
    se = sd / np.sqrt(max(len(arr), 1))
    return dict(mean=mean, sd=sd, ci95_lo=mean - 1.96 * se, ci95_hi=mean + 1.96 * se, n=len(arr))


def _agg_calib(rows):
    """Pool the engine's per-gate expected-vs-realised accumulators over runs (sums then ratios)."""
    out = {}
    nlev = 4
    for m_ in range(nlev):
        acc = None
        for r in rows:
            C = r["contest_calib"].get(str(m_))
            if not C:
                continue
            if acc is None:
                acc = {k: (list(v) if isinstance(v, list) else v) for k, v in C.items()}
            else:
                for k, v in C.items():
                    if isinstance(v, list):
                        acc[k] = [a + b for a, b in zip(acc[k], v)]
                    else:
                        acc[k] = acc[k] + v
        if acc is None or acc.get("n_pred", 0) == 0 and acc.get("applicants", 0) == 0:
            out[str(m_)] = None
            continue
        nb = 10
        dec = [
            dict(bin=j,
                 n=int(acc["cnt_bin"][j]),
                 expected=float(acc["exp_bin"][j] / acc["cnt_bin"][j]) if acc["cnt_bin"][j] else float("nan"),
                 realised=float(acc["real_bin"][j] / acc["cnt_bin"][j]) if acc["cnt_bin"][j] else float("nan"))
            for j in range(nb)
        ]
        eff = [
            dict(quintile=j,
                 n=int(acc["cnt_eff"][j]),
                 mean_effort=float(acc["eff_sum"][j] / acc["cnt_eff"][j]) if acc["cnt_eff"][j] else float("nan"),
                 expected=float(acc["exp_eff"][j] / acc["cnt_eff"][j]) if acc["cnt_eff"][j] else float("nan"),
                 realised=float(acc["real_eff"][j] / acc["cnt_eff"][j]) if acc["cnt_eff"][j] else float("nan"))
            for j in range(5)
        ]
        out[str(m_)] = dict(
            n_years=int(acc["n_years"]),
            applicants=int(acc["applicants"]),
            seats=int(acc["seats"]),
            admitted=int(acc["admitted"]),
            applicant_seat_ratio=float(acc["applicants"] / acc["seats"]) if acc["seats"] else float("nan"),
            mean_yearly_ratio=float(acc["ratio_sum"] / acc["n_years"]) if acc["n_years"] else float("nan"),
            realised_admission_rate=float(acc["admitted"] / acc["applicants"]) if acc["applicants"] else float("nan"),
            brier=float(acc["brier"] / acc["n_pred"]) if acc["n_pred"] else float("nan"),
            brier_flat=float(acc["brier_flat"] / acc["n_pred"]) if acc["n_pred"] else float("nan"),
            beta_last=float(acc["beta_last"]),
            cut_last=float(acc["cut_last"]),
            expected_vs_realised_deciles=dec,
            effort_quintiles=eff,
        )
    return out


MOMENTS = ("k12_spend", "k12_rate_pct", "g12_pct", "q5_q1_gap_pp", "q5_q1_spend_ratio",
           "elite_q5_share_pct", "elite_share_pct", "contest_e_mean", "grade9_tut_pct", "grade12_tut_pct")


def _summarise(rows, base_rows):
    base_by_seed = {r["seed"]: r for r in base_rows}
    out = {}
    for key in MOMENTS:
        out[key] = _stats([r[key] for r in rows])
    out["n_seeds"] = len(rows)
    deltas = {}
    for key in ("g12_pct", "q5_q1_gap_pp", "q5_q1_spend_ratio", "elite_q5_share_pct", "k12_rate_pct"):
        d = [r[key] - base_by_seed[r["seed"]][key] for r in rows if r["seed"] in base_by_seed]
        deltas[key] = _stats(d)
    out["delta_vs_baseline_paired"] = deltas
    out["contest_calib"] = _agg_calib(rows)
    return out


def _spend_index(rows, base_rows):
    base_by_seed = {r["seed"]: r for r in base_rows}
    paired = [100.0 * r["k12_spend"] / base_by_seed[r["seed"]]["k12_spend"] for r in rows if r["seed"] in base_by_seed]
    return _stats(paired)


# ---------------------------------------------------------------- executables
def _run_tasks(tasks, workers):
    workers = max(1, min(int(workers), 56, os.cpu_count() or 1))
    print(f"running {len(tasks)} simulations on {workers} workers (nice -n 10 expected from the shell)", flush=True)
    with ProcessPoolExecutor(max_workers=workers) as ex:
        rows = list(ex.map(_run_single, tasks, chunksize=1))
    return rows


def _write(payload, out_path):
    os.makedirs(os.path.dirname(os.path.abspath(out_path)), exist_ok=True)
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=1)
    print(f"wrote {out_path}", flush=True)


def _base_meta(args, elapsed, n_runs):
    return dict(
        label="SIMULATION — stochastic model output, not empirical estimates; no causal claims",
        script=os.path.basename(__file__),
        generated_at=time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        engine_root=ENGINE_DIR,
        mode=args.mode,
        price_mult=args.price_mult,
        alpha_mult=args.alpha_mult,
        n_runs=n_runs,
        elapsed_seconds=round(elapsed, 2),
        workers=min(int(args.workers), 56, os.cpu_count() or 1),
        cpu_cap="nice -n 10, max_workers<=56 (<=70% of 80 cores)",
        canonical_spec="420 generation: N=400, T=70, y_median 3.0, subsist .15, borrow .5, contest_alpha 1.2/1.25, "
                        "contest_price .12/.11, contest_max_e 4.0/4.5, elite_logw .85/1.15, bar gates 0/0/0, "
                        "contest-only tutoring (p_own=p_firm=99), G9 placement consequences (V1)",
        python=sys.version.split()[0],
        numpy=np.__version__,
    )


def mode_calibrate(args):
    """Declared calibration sweep: 6x3 grid on KR baseline, calibration seeds 0-9 (amendment 1)."""
    t0 = time.time()
    price_mults = [0.25, 0.5, 0.75, 1.0, 1.5, 2.0]
    alpha_mults = [0.85, 1.0, 1.15]
    seeds = list(range(args.seeds))
    tasks = []
    keys = []
    for pm in price_mults:
        for am in alpha_mults:
            specs = build_arms(pm, am, ("KR",))
            prm = [s[3] for s in specs if s[1] == "Baseline"][0]
            keys.append((pm, am))
            for sd in seeds:
                tasks.append(("V1_canonical", "KR", "Baseline", sd, prm))
    rows = _run_tasks(tasks, args.workers)
    by_cfg = {}
    for i, (pm, am) in enumerate(keys):
        chunk = rows[i * len(seeds):(i + 1) * len(seeds)]
        part = _stats([r["k12_rate_pct"] for r in chunk])
        gap = _stats([r["q5_q1_gap_pp"] for r in chunk])
        ratio = _stats([r["q5_q1_spend_ratio"] for r in chunk])
        e5 = _stats([r["elite_q5_share_pct"] for r in chunk])
        S = ((part["mean"] - 76.5) / 2.8) ** 2 + ((gap["mean"] - 32.1) / 3.0) ** 2
        by_cfg[f"price_x{pm:.2f}__alpha_x{am:.2f}"] = dict(
            price_mult=pm, alpha_mult=am, S=float(S),
            participation=part, gap=gap, spend_ratio=ratio, elite_q5_share=e5,
        )
    # selection rule (fixed in amendment 1)
    untuned = by_cfg["price_x1.00__alpha_x1.00"]
    keep_untuned = (75.7 <= untuned["participation"]["mean"] <= 78.5) and abs(untuned["gap"]["mean"] - 32.1) <= 3.0
    if keep_untuned:
        chosen = (1.0, 1.0)
        chosen_key = "price_x1.00__alpha_x1.00"
        reason = "untuned 420 port inside both training tolerances; kept for parsimony (plan §5.1)"
    else:
        chosen_key = min(by_cfg, key=lambda k: by_cfg[k]["S"])
        chosen = (by_cfg[chosen_key]["price_mult"], by_cfg[chosen_key]["alpha_mult"])
        reason = "untuned port outside training tolerance; minimum-S grid point (amendment 1)"
    best = by_cfg[chosen_key]
    payload = dict(
        metadata=_base_meta(args, time.time() - t0, len(rows)),
        calibration_seeds=seeds,
        grid=dict(price_mults=price_mults, alpha_mults=alpha_mults,
                  score="S = ((part-76.5)/2.8)^2 + ((gap-32.1)/3.0)^2",
                  training_moments=dict(participation_target_pct=76.5, participation_band=[75.7, 78.5],
                                        gap_target_pp=32.1, gap_tol_pp=3.0),
                  heldout_moments=dict(kr_spend_ratio=3.4, kr_spend_tol=0.5,
                                       hk_grade9_participation_pct=53.8, hk_grade12_participation_pct=71.8,
                                       hk_tol_pp=5.0)),
        configs=by_cfg,
        selection=dict(chosen_price_mult=chosen[0], chosen_alpha_mult=chosen[1], chosen_key=chosen_key,
                       reason=reason, untuned_inside_tolerance=bool(keep_untuned),
                       achieved_training=dict(participation=best["participation"], gap=best["gap"])),
        seeds=rows,
    )
    _write(payload, args.out)
    print(f"\n=== calibration grid (training moments, seeds {seeds[0]}-{seeds[-1]}) ===")
    print(f"{'config':28s} | {'participation':>14s} | {'gap pp':>14s} | {'ratio':>12s} | {'S':>8s}")
    for key, d in sorted(by_cfg.items(), key=lambda kv: kv[1]["S"]):
        print(f"{key:28s} | {d['participation']['mean']:8.2f}±{d['participation']['sd']:4.2f} | "
              f"{d['gap']['mean']:8.2f}±{d['gap']['sd']:4.2f} | {d['spend_ratio']['mean']:6.2f}±{d['spend_ratio']['sd']:4.2f} | "
              f"{d['S']:8.3f}")
    print(f"\nchosen: price x{chosen[0]} alpha x{chosen[1]}  ({reason})")


def mode_policy(args):
    """Full rerun: V1 18 arms + V2/V3 KR 9 arms each, matched seeds, seat accounting, diagnostics."""
    t0 = time.time()
    seeds = list(range(args.seeds))
    specs = build_variants(args.price_mult, args.alpha_mult)
    tasks = []
    for variant, jur, arm_id, label, prm in specs:
        for sd in seeds:
            tasks.append((variant, jur, arm_id, sd, prm))
    rows = _run_tasks(tasks, args.workers)

    grouped = {}
    for r in rows:
        grouped.setdefault((r["variant"], r["jurisdiction"], r["arm_id"]), []).append(r)
    for key in grouped:
        grouped[key].sort(key=lambda r: r["seed"])

    summary = {}
    for variant in sorted({s[0] for s in specs}):
        summary[variant] = {}
        for jur in sorted({s[1] for s in specs if s[0] == variant}):
            base_rows = grouped.get((variant, jur, "Baseline"), [])
            summary[variant][jur] = {}
            for _, jur2, arm_id, label, _ in [s for s in specs if s[0] == variant and s[1] == jur]:
                rws = grouped[(variant, jur, arm_id)]
                d = _summarise(rws, base_rows)
                d["label"] = label
                d["total_spend_index"] = _spend_index(rws, base_rows)
                summary[variant][jur][arm_id] = d

    # held-out moments: seeds 10-29 only (never used for calibration selection)
    holdout = {}
    for variant in summary:
        holdout[variant] = {}
        for jur in summary[variant]:
            holdout[variant][jur] = {}
            for arm_id in ("Baseline",):
                rws = [r for r in grouped[(variant, jur, arm_id)] if r["seed"] in HOLDOUT_SEEDS]
                holdout[variant][jur][arm_id] = {
                    k: _stats([r[k] for r in rws]) for k in
                    ("k12_rate_pct", "q5_q1_gap_pp", "q5_q1_spend_ratio", "grade9_tut_pct", "grade12_tut_pct",
                     "elite_q5_share_pct")
                }

    # pre-stated CF4 criterion, unchanged from the 540 reproduction
    cf4 = {}
    for variant in summary:
        if not summary[variant].get("HK") or not summary[variant].get("KR"):
            continue
        cf4[variant] = {}
        for arm_id in ("CF4a", "CF4b"):
            res = {}
            ok_all = True
            for jur in ("HK", "KR"):
                b = summary[variant][jur]["Baseline"]
                a = summary[variant][jur][arm_id]
                spend_ok = a["total_spend_index"]["mean"] < 80.0
                equity_ok = a["elite_q5_share_pct"]["mean"] < b["elite_q5_share_pct"]["mean"]
                res[jur] = dict(spend_index=a["total_spend_index"]["mean"], spend_ok=bool(spend_ok),
                                elite_q5=a["elite_q5_share_pct"]["mean"],
                                baseline_elite_q5=b["elite_q5_share_pct"]["mean"], equity_ok=bool(equity_ok))
                ok_all = ok_all and spend_ok and equity_ok
            res["win_win_both_jurisdictions"] = bool(ok_all)
            cf4[variant][arm_id] = res

    payload = dict(
        metadata=_base_meta(args, time.time() - t0, len(rows)),
        variants=dict(
            V1_canonical="G9 contest + persistent placement consequences (elite9 learn & G12 contest boost)",
            V2_g9_removed="no G9 contest (pass-through bar gate)",
            V3_g9_no_consequence="G9 contest prices prep but has no realised consequence for winner or loser "
                                 "(reviewed phantom-prize configuration; set_voc=False, g9_consequence=0)",
        ),
        summary=summary,
        cf4_criterion_pre_stated=cf4,
        heldout_moments_seeds_10_29=holdout,
        seeds=rows,
    )
    _write(payload, args.out)

    print()
    for variant in summary:
        for jur in summary[variant]:
            print(f"=== {variant} / {jur} ({len(seeds)} matched seeds) ===")
            print(f"{'Arm':8s} | {'SpendIdx':>9s} | {'G12 %':>7s} | {'Q5-Q1 gap':>9s} | {'Q5/Q1 x':>8s} | {'EliteQ5 %':>9s} | {'K12 %':>7s}")
            for arm_id, d in summary[variant][jur].items():
                print(f"{arm_id:8s} | {d['total_spend_index']['mean']:9.1f} | {d['g12_pct']['mean']:6.1f}% | "
                      f"{d['q5_q1_gap_pp']['mean']:8.1f} | {d['q5_q1_spend_ratio']['mean']:8.2f} | "
                      f"{d['elite_q5_share_pct']['mean']:8.1f}% | {d['k12_rate_pct']['mean']:6.1f}%")
            print()
    print("CF4 pre-stated criterion (spend index < 80 AND elite Q5 below baseline, both jurisdictions):")
    for variant in cf4:
        for arm_id in ("CF4a", "CF4b"):
            print(f"  {variant:28s} {arm_id}: {cf4[variant][arm_id]['win_win_both_jurisdictions']}  "
                  f"HK spend {cf4[variant][arm_id]['HK']['spend_index']:.2f} / "
                  f"elite {cf4[variant][arm_id]['HK']['elite_q5']:.2f} | "
                  f"KR spend {cf4[variant][arm_id]['KR']['spend_index']:.2f} / "
                  f"elite {cf4[variant][arm_id]['KR']['elite_q5']:.2f}")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=("calibrate", "policy"))
    ap.add_argument("--out", required=True)
    ap.add_argument("--seeds", type=int, default=30)
    ap.add_argument("--workers", type=int, default=int(os.environ.get("N_WORKERS", min(56, os.cpu_count() or 1))))
    ap.add_argument("--price-mult", type=float, default=1.0)
    ap.add_argument("--alpha-mult", type=float, default=1.0)
    args = ap.parse_args()
    if args.mode == "calibrate":
        mode_calibrate(args)
    else:
        mode_policy(args)


if __name__ == "__main__":
    main()
