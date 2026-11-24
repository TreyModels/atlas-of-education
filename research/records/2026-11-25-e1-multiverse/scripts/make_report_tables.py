#!/usr/bin/env python3
"""Render the E1 report tables from committed JSON outputs (no analysis here)."""
import json, os, sys
RES = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "results")


def load(name):
    p = os.path.join(RES, name)
    return json.load(open(p)) if os.path.exists(p) else None


S = load("summary_by_R.json"); H = load("split_halves.json"); G = load("group_localisation.json")
P = load("repro400.json")
print("## BH/BY counts by R (four procedures; 272-link family; conservative p)")
print("| R | family | floor 1/(R+1) | floor count | BH cert | BY cert | first rank BH | first rank BY | BY cert (136 parity) |")
print("|---|---|---|---|---|---|---|---|---|")
if S:
    for R in sorted(S["families"], key=lambda z: int(z)):
        fam = S["families"][R]
        for proc in ("up", "down", "flip", "het"):
            f = fam[proc]
            print(f"| {R} | {proc} | {S['floors'][R]:.5f} | {f['n_floor']} | {f['certified_BH']} | "
                  f"{f['certified_BY']} | {f['first_rank_BH']} | {f['first_rank_BY']} | "
                  f"{f.get('certified_BY136')} |")
print()
print("## BY tier changes across R")
if S:
    for proc, d in S["BY_tier_changes"].items():
        for k, v in d.items():
            print(f"- {proc} {k}: gained {v['gained']}, lost {v['lost']}, n at later R {v['n_at_later']}")
print()
print("## Split halves at R =", H.get("R") if H else None)
if H:
    print("up-procedure empirical p rank correlation:", H.get("up_p_rank_correlation"))
    for proc, d in H.get("family_agreement", {}).items():
        print(f"- {proc}: certified A={d['certified_A']} B={d['certified_B']} both={d['certified_both']} "
              f"one-half={d['certified_one_half']} jaccard={d['jaccard']:.3f} BH A/B={d['BH_A']}/{d['BH_B']}")
print()
print("## Group localisation")
if G:
    print(json.dumps(G.get("summary"), indent=1))
    for r in G.get("robust", []):
        print(f"- robust link {r['x']} -> {r['y']}: b={r['b']:.4g} t={r['t']:.2f}, "
              f"top5={r['top5_countries']}, top5 signal share={r['top5_signal_share']:.2f}, "
              f"t without top5={r['t_top5_removed']}, concentrated={r['group_concentrated']}")
print()
print("## R=400 comparison with committed headline")
print(json.dumps(P, indent=1) if P else "unavailable")
