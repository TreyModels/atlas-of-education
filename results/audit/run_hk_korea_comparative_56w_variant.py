"""Hong Kong (HKDSE) vs South Korea (CSAT) Comparative Tullock Contest Experiment.

Runs all 18 policy arms x 30 matched seeds (540 runs total) against
atlas-of-education branch `research/binding-gate-2026-11-25` (HEAD `68da16e`)
patched with `contest_gate.patch`.

Uses the exact `Engine(modules, **params)` constructor (core.py L73-74) and
`E.R` yearly history dict populated via `E.note(...)`, plus `E.ALL` for cohort
elite-tier tracking.
"""
import json
import os
import sys
import time
import warnings
from concurrent.futures import ProcessPoolExecutor

warnings.filterwarnings("ignore")

ROOT = os.path.dirname(os.path.abspath(__file__))
ENGINE_DIR = os.path.join(ROOT, "engine")
if ENGINE_DIR not in sys.path:
    sys.path.insert(0, ENGINE_DIR)

import numpy as np
from eduengine.core import Engine
from eduengine.modules.labour import QueueLabour
from eduengine.modules.schools import PrivateSchools, PublicSchools
from eduengine.modules.sdg4 import SDG4
from eduengine.modules.tutoring import TutoringMarket

N_SEEDS = 30
SEEDS = list(range(N_SEEDS))


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


def build_arms():
    """Return ordered list of (jurisdiction, arm_id, label, params) for all 18 arms."""
    hk_base = dict(
        N=300,
        T=46,
        measure_from=18,
        y_median=2.2,
        y_sigma=0.65,
        urban_share=1.0,
        subsist=0.35,
        borrow=0.25,
        pay_ratio=1.2,
        monitoring=0.9,
        budget_per_child=0.14,
        fee_public=0.0,
        fee_tertiary=0.25,
        vac0=0.30,
        vac_growth=0.005,
        own_ban=0.95,
        r0=0.04,
        elite_logw=0.50,
        contest_r=1.5,
        contest_alpha=0.25,
        contest_price=0.16,
        contest_x0=1.0,
        contest_max_e=6.0,
        gates=[
            dict(kind="bar", bar=2.0),
            dict(kind="bar", bar=4.0),
            dict(kind="contest", share=0.23, fail="track"),
            dict(kind="bar", bar=10.0),
        ],
    )

    kr_base = dict(
        N=300,
        T=46,
        measure_from=18,
        y_median=2.0,
        y_sigma=0.55,
        urban_share=0.85,
        subsist=0.35,
        borrow=0.25,
        pay_ratio=1.2,
        monitoring=0.9,
        budget_per_child=0.14,
        fee_public=0.0,
        fee_tertiary=0.25,
        vac0=0.28,
        vac_growth=0.005,
        own_ban=0.95,
        r0=0.04,
        elite_logw=0.60,
        contest_r=1.6,
        contest_alpha=0.25,
        contest_price=0.16,
        contest_x0=1.0,
        contest_max_e=6.0,
        gates=[
            dict(kind="bar", bar=2.0),
            dict(kind="contest", share=0.35, fail="track", elite_logw=0.15, set_voc=False),
            dict(kind="contest", share=0.12, fail="track"),
            dict(kind="bar", bar=10.0),
        ],
    )

    specs = []
    for jur, base, s_mod, s_maj, s_label_mod, s_label_maj in [
        ("HK", hk_base, 0.28, 0.50, "S=0.28", "S=0.50"),
        ("KR", kr_base, 0.16, 0.40, "S12=0.16", "S12=0.40"),
    ]:
        arms = [
            ("Baseline", f"Baseline ({'S=0.23' if jur == 'HK' else 'S12=0.12'})", base),
            ("CF1a", "CF1a (+50% tax)", dict(base, contest_price=base["contest_price"] * 1.5)),
            ("CF1b", "CF1b (-50% cap)", dict(base, contest_max_e=base["contest_max_e"] * 0.5)),
            ("CF2a", f"CF2a ({s_label_mod})", _with_g12_share(base, s_mod)),
            ("CF2b", f"CF2b ({s_label_maj})", _with_g12_share(base, s_maj)),
            ("CF3a", "CF3a (dV -30%)", _with_dv_scale(base, 0.70)),
            ("CF3b", "CF3b (dV -50%)", _with_dv_scale(base, 0.50)),
            (
                "CF4a",
                "CF4a (Win-Win: dV -50% + Cap -50%)",
                dict(_with_dv_scale(base, 0.50), contest_max_e=base["contest_max_e"] * 0.5),
            ),
            (
                "CF4b",
                f"CF4b (Win-Win: dV -50% + Seats {s_label_maj})",
                _with_g12_share(_with_dv_scale(base, 0.50), s_maj),
            ),
        ]
        for arm_id, label, prm in arms:
            specs.append((jur, arm_id, label, prm))
    return specs


def _run_single(task):
    jur, arm_id, seed, params = task
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

    X = E.ALL
    sel = (X["cohort"] >= m) & (X["cohort"] <= E.p["T"] - 14) & (X["g"] >= 12)
    el = X["elite"][sel]
    qq = X["q"][sel]
    elite_q5_share = float(np.mean(qq[el] == 4)) if el.any() else float("nan")

    return dict(
        jurisdiction=jur,
        arm_id=arm_id,
        seed=seed,
        k12_spend=k12_spend,
        k12_rate_pct=100.0 * k12_rate,
        g12_pct=100.0 * g12_rate,
        q5_q1_gap_pp=100.0 * float(rq[4] - rq[0]),
        q5_q1_spend_ratio=float(sq[4] / max(sq[0], 1e-9)),
        elite_q5_share_pct=100.0 * elite_q5_share,
        k12_rate_by_q=[float(100.0 * v) for v in rq],
        k12_spend_by_q=[float(v) for v in sq],
        contest_e_mean=contest_e_mean,
    )


def _stats(vals):
    arr = np.array(vals, float)
    mean = float(np.nanmean(arr))
    sd = float(np.nanstd(arr, ddof=1)) if len(arr) > 1 else 0.0
    se = sd / np.sqrt(max(len(arr), 1))
    return dict(mean=mean, sd=sd, ci95_lo=mean - 1.96 * se, ci95_hi=mean + 1.96 * se)


def main():
    t0 = time.time()
    specs = build_arms()
    tasks = []
    label_map = {}
    for jur, arm_id, label, params in specs:
        label_map[(jur, arm_id)] = label
        for s in SEEDS:
            tasks.append((jur, arm_id, s, params))

    workers = 56
    print(f"Running {len(tasks)} simulations ({len(specs)} arms x {N_SEEDS} seeds) on {workers} workers...")
    with ProcessPoolExecutor(max_workers=workers) as ex:
        raw_results = list(ex.map(_run_single, tasks, chunksize=4))

    # Group by (jurisdiction, arm_id) sorted by seed
    grouped = {}
    for row in raw_results:
        grouped.setdefault((row["jurisdiction"], row["arm_id"]), []).append(row)
    for key in grouped:
        grouped[key].sort(key=lambda r: r["seed"])

    summary = {"HK": {}, "KR": {}}
    for jur in ("HK", "KR"):
        base_rows = grouped[(jur, "Baseline")]
        base_spend_mean = float(np.mean([r["k12_spend"] for r in base_rows]))
        base_by_seed = {r["seed"]: r for r in base_rows}

        for _, arm_id, label, _ in [s for s in specs if s[0] == jur]:
            rows = grouped[(jur, arm_id)]
            spend_idx_seeds = [100.0 * r["k12_spend"] / base_by_seed[r["seed"]]["k12_spend"] for r in rows]
            spend_idx_agg = 100.0 * float(np.mean([r["k12_spend"] for r in rows])) / base_spend_mean
            g12_vals = [r["g12_pct"] for r in rows]
            gap_vals = [r["q5_q1_gap_pp"] for r in rows]
            ratio_vals = [r["q5_q1_spend_ratio"] for r in rows]
            elite_vals = [r["elite_q5_share_pct"] for r in rows]
            k12_rate_vals = [r["k12_rate_pct"] for r in rows]
            k12_spend_vals = [r["k12_spend"] for r in rows]

            summary[jur][arm_id] = dict(
                label=label,
                n_seeds=len(rows),
                total_spend_index=round(spend_idx_agg, 2),
                total_spend_index_seed_stats=_stats(spend_idx_seeds),
                g12_pct=_stats(g12_vals),
                q5_q1_gap_pp=_stats(gap_vals),
                q5_q1_spend_ratio=_stats(ratio_vals),
                elite_q5_share_pct=_stats(elite_vals),
                k12_rate_pct=_stats(k12_rate_vals),
                k12_spend_raw=_stats(k12_spend_vals),
                delta_vs_baseline=dict(
                    total_spend_index_pts=round(spend_idx_agg - 100.0, 2),
                    g12_pp=_stats([r["g12_pct"] - base_by_seed[r["seed"]]["g12_pct"] for r in rows]),
                    q5_q1_gap_pp=_stats([r["q5_q1_gap_pp"] - base_by_seed[r["seed"]]["q5_q1_gap_pp"] for r in rows]),
                    q5_q1_spend_ratio=_stats(
                        [r["q5_q1_spend_ratio"] - base_by_seed[r["seed"]]["q5_q1_spend_ratio"] for r in rows]
                    ),
                    elite_q5_share_pp=_stats(
                        [r["elite_q5_share_pct"] - base_by_seed[r["seed"]]["elite_q5_share_pct"] for r in rows]
                    ),
                ),
            )

    elapsed = time.time() - t0
    payload = dict(
        metadata=dict(
            repo="https://github.com/TreyModels/atlas-of-education.git",
            branch="research/binding-gate-2026-11-25",
            base_commit="68da16e",
            n_arms=len(specs),
            n_seeds=N_SEEDS,
            total_runs=len(raw_results),
            elapsed_seconds=round(elapsed, 2),
            history_api="E.R (core.py L99; populated via E.note(...))",
        ),
        summary=summary,
        seeds=raw_results,
    )

    out_path = os.path.join(ROOT, "hk_korea_comparative_with_cf4.json")
    with open(out_path, "w") as f:
        json.dump(payload, f, indent=2)

    print(f"\nCompleted {len(raw_results)} runs in {elapsed:.1f}s -> {out_path}\n")
    for jur in ("HK", "KR"):
        print(f"=== {jur} (30 matched seeds) ===")
        print(f"{'Arm':6s} | {'Label':38s} | {'SpendIdx':8s} | {'G12 %':7s} | {'Q5-Q1 Gap':9s} | {'Q5/Q1 Ratio':11s} | {'Elite Q5 %':10s}")
        print("-" * 105)
        for arm_id, d in summary[jur].items():
            print(
                f"{arm_id:6s} | {d['label']:38s} | {d['total_spend_index']:8.1f} | "
                f"{d['g12_pct']['mean']:6.1f}% | {d['q5_q1_gap_pp']['mean']:7.1f}pp | "
                f"{d['q5_q1_spend_ratio']['mean']:10.2f}x | {d['elite_q5_share_pct']['mean']:9.1f}%"
            )
        print()


if __name__ == "__main__":
    main()
