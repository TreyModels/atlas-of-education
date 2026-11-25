#!/usr/bin/env python3
"""
Standalone M1-friendly runner for Paper B (Hong Kong HKDSE & South Korea CSAT)
plus Combined Win-Win Policy Arms (CF4a & CF4b).

Prerequisites:
  - Apply the Tullock `contest` gate additions to `engine/eduengine/core.py`
    and `engine/eduengine/modules/tutoring.py` (see `contest_gate_spec.md`).
  - Run from repository root (`atlas-of-education/`):
      python3 papers/shadow-education-contest/code/run_hk_korea_comparative.py
"""
from __future__ import annotations

import json
import os
import sys
import time
from concurrent.futures import ProcessPoolExecutor
import numpy as np

REPO_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
sys.path.insert(0, os.path.join(REPO_ROOT, "engine"))

from eduengine.core import Engine  # noqa: E402
from eduengine.modules.tutoring import TutoringMarket  # noqa: E402


def make_hk_config(seat_share=0.23, tax_mult=1.0, cap_mult=1.0, wage_comp=0.0):
    """Hong Kong HKDSE: universal free K-12, commercial-only, Grade-12 vertical-tier contest."""
    base_delta_v = 0.85 * (1.0 - wage_comp)
    return dict(
        N=400, T=70, fee_public=0.0, y_median=3.0, y_sigma=0.65,
        urban_share=1.0, subsist=0.15, borrow=0.5,
        p_own=99.0, p_firm=99.0,  # commercial contest-only baseline
        contest_r=1.5, contest_alpha=1.2,
        contest_price=0.12 * tax_mult,
        contest_x0=2.0,
        contest_max_e=4.0 * cap_mult,
        gates=[
            dict(kind="bar", bar=0.0),
            dict(kind="bar", bar=0.0),
            dict(kind="contest", share=seat_share, fail="track", elite_logw=base_delta_v),
            dict(kind="bar", bar=0.0),
        ],
    )


def make_kr_config(seat_share_12=0.12, tax_mult=1.0, cap_mult=1.0, wage_comp=0.0):
    """South Korea CSAT: universal free K-12, stacked G9 + G12 vertical-tier contests."""
    base_delta_v = 1.15 * (1.0 - wage_comp)
    return dict(
        N=400, T=70, fee_public=0.0, y_median=3.0, y_sigma=0.60,
        urban_share=0.85, subsist=0.15, borrow=0.5,
        p_own=99.0, p_firm=99.0,
        contest_r=1.6, contest_alpha=1.25,
        contest_price=0.11 * tax_mult,
        contest_x0=2.0,
        contest_max_e=4.5 * cap_mult,
        gates=[
            dict(kind="bar", bar=0.0),
            dict(kind="contest", share=0.35, fail="track", elite_logw=0.35 * (1.0 - wage_comp)),
            dict(kind="contest", share=seat_share_12, fail="track", elite_logw=base_delta_v),
            dict(kind="bar", bar=0.0),
        ],
    )


def run_one(args):
    regime, arm, cfg, seed = args
    e = Engine(cfg, modules=[TutoringMarket()], seed=seed)
    e.run()
    # Extract steady-state post-burn-in summary (years 35..69)
    hist = e.history[35:]
    tut_k12 = float(np.mean([h.get("tut_k12_rate", h.get("tut_rate", 0.0)) for h in hist]))
    tut_g9 = float(np.mean([h["tut_by_grade"][8] for h in hist if len(h.get("tut_by_grade", [])) > 8]))
    tut_g12 = float(np.mean([h["tut_by_grade"][11] for h in hist if len(h.get("tut_by_grade", [])) > 11]))
    q_rates = np.mean([h["tut_by_q"] for h in hist if "tut_by_q" in h], axis=0)
    spend = float(np.mean([h.get("tut_spend", 0.0) for h in hist]))
    return dict(
        regime=regime, arm=arm, seed=seed,
        k12_rate=tut_k12, g9_rate=tut_g9, g12_rate=tut_g12,
        q5_minus_q1=float(q_rates[4] - q_rates[0]),
        total_spend=spend,
    )


def main():
    t0 = time.time()
    seeds = list(range(30))
    arms = [
        ("HK", "baseline", make_hk_config()),
        ("HK", "CF1a_tax_plus50", make_hk_config(tax_mult=1.5)),
        ("HK", "CF1b_cap_minus50", make_hk_config(cap_mult=0.5)),
        ("HK", "CF2a_seats_028", make_hk_config(seat_share=0.28)),
        ("HK", "CF2b_seats_050", make_hk_config(seat_share=0.50)),
        ("HK", "CF3a_wage_minus30", make_hk_config(wage_comp=0.30)),
        ("HK", "CF3b_wage_minus50", make_hk_config(wage_comp=0.50)),
        ("HK", "CF4a_winwin_wage50_cap50", make_hk_config(wage_comp=0.50, cap_mult=0.5)),
        ("HK", "CF4b_winwin_wage50_seats50", make_hk_config(wage_comp=0.50, seat_share=0.50)),
        ("KR", "baseline", make_kr_config()),
        ("KR", "CF1a_tax_plus50", make_kr_config(tax_mult=1.5)),
        ("KR", "CF1b_cap_minus50", make_kr_config(cap_mult=0.5)),
        ("KR", "CF2a_seats_016", make_kr_config(seat_share_12=0.16)),
        ("KR", "CF2b_seats_040", make_kr_config(seat_share_12=0.40)),
        ("KR", "CF3a_wage_minus30", make_kr_config(wage_comp=0.30)),
        ("KR", "CF3b_wage_minus50", make_kr_config(wage_comp=0.50)),
        ("KR", "CF4a_winwin_wage50_cap50", make_kr_config(wage_comp=0.50, cap_mult=0.5)),
        ("KR", "CF4b_winwin_wage50_seats40", make_kr_config(wage_comp=0.50, seat_share_12=0.40)),
    ]
    jobs = [(reg, arm, cfg, s) for reg, arm, cfg in arms for s in seeds]
    with ProcessPoolExecutor() as ex:
        rows = list(ex.map(run_one, jobs))

    out_dir = os.path.join(os.path.dirname(__file__), "results")
    os.makedirs(out_dir, exist_ok=True)
    out_path = os.path.join(out_dir, "hk_korea_comparative_with_cf4.json")
    with open(out_path, "w") as f:
        json.dump({"elapsed_sec": round(time.time() - t0, 2), "rows": rows}, f, indent=2)
    print(f"Saved {len(rows)} runs to {out_path} in {time.time() - t0:.1f}s")


if __name__ == "__main__":
    main()
