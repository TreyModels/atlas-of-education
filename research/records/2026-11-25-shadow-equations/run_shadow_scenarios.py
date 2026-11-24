#!/usr/bin/env python3
"""Run the first-pass shadow-education scenario grid.

Usage
  python run_shadow_scenarios.py --pilot   # N=2,000, 3 seeds
  python run_shadow_scenarios.py --full    # N=20,000, 10 seeds
  python run_shadow_scenarios.py --pilot --out /tmp/x.json
"""
import argparse, json, os, sys
import numpy as np
from dataclasses import asdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from shadow_model import Params, run_scenarios, price_elasticity, SCENARIOS


def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--pilot", action="store_true")
    g.add_argument("--full", action="store_true")
    ap.add_argument("--out", default=None)
    ap.add_argument("--seeds", type=int, default=None)
    args = ap.parse_args()

    if args.full:
        n, seeds = 20000, 10
    else:
        n, seeds = 2000, 3
    if args.seeds:
        seeds = args.seeds

    base = Params(n=n)
    print(f"SIMULATION — first-pass shadow-equation placement. N={n}, seeds={seeds}, scenarios={len(SCENARIOS)}")
    out, deltas, _ = run_scenarios(base, seeds=seeds)
    pe = price_elasticity(base, seeds=seeds)

    print("\nscenario            participation  own_share  learn_gini  admit_gap  tut_gap  earn_gini")
    for name, agg in out.items():
        m = agg
        print(f"{name:18s} {m['tut_participation']['mean']:>13.4f} "
              f"{m['own_share']['mean']:>10.4f} "
              f"{m['learning_gini']['mean']:>10.4f} "
              f"{m['admission_gap_q5_q1']['mean']:>9.4f} "
              f"{m['tut_gap_q5_q1']['mean']:>8.4f} "
              f"{m['earnings_gini']['mean']:>9.4f}")

    print("\npaired deltas vs baseline (mean over seeds)")
    for name, d in deltas.items():
        print(f"{name:18s} participation {d['tut_participation']['mean']:+.4f}  "
              f"own_share {d['own_share']['mean']:+.4f}  "
              f"learn_gini {d['learning_gini']['mean']:+.4f}  "
              f"admit_gap {d['admission_gap_q5_q1']['mean']:+.4f}  "
              f"tut_gap {d['tut_gap_q5_q1']['mean']:+.4f}")
    print(f"\nprice elasticity of participation (own fee, +-10%): {pe:.4f}")

    payload = {
        "label": "SIMULATION — first-pass shadow-equation placement; illustrative parameters, not estimates",
        "config": {"n": n, "seeds": seeds, "scenarios": list(SCENARIOS)},
        "params": asdict(base),
        "scenarios": out,
        "deltas_vs_baseline": deltas,
        "price_elasticity": pe,
        "warnings": [
            "illustrative parameters; no literature verification yet",
            "tutoring fee exogenous; no market clearing (catalogue 83-85 not solved)",
            "contest-success admissions (81) approximated by a score gate; Tullock form deferred",
            "no causal interpretation; simulation only",
        ],
    }
    outpath = args.out or os.path.join(os.path.dirname(os.path.abspath(__file__)), "results_first_pass.json")
    with open(outpath, "w") as f:
        json.dump(payload, f, indent=2)
    print(f"\nwrote {outpath}")


if __name__ == "__main__":
    main()
