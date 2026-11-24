#!/usr/bin/env python3
"""Read-only report: corrected exit-reason decomposition for combo 0 and combo 143.

Derived report only; never modifies the results JSON. Summarises, per combo (mean over seeds):
  - overall started_liquidity_share / started_choice_share
  - per wealth quintile q1..q5: liquidity / choice / never / censored / other_terminal / started_share
  - urban / rural: same categories
  - population sizes and a few attainment metrics for context
Usage: python report_decomp.py --in results_multiverse_fixed1440.json --out decomp_report.json
"""
import argparse
import json
import os

CATS = ("liquidity", "choice", "never", "censored", "other_terminal", "started_share")


def mean(xs):
    xs = [x for x in xs if x is not None]
    return float(sum(xs) / len(xs)) if xs else None


def combo_report(rows, ci):
    rs = [r for r in rows if r["combo_index"] == ci]
    seeds = sorted(r["seed"] for r in rs)
    out = {"combo_index": ci, "combo": rs[0]["combo"], "n_seeds": len(seeds),
           "seeds": [seeds[0], seeds[-1]]}
    g = rs[0]["groups"]
    out["overall"] = {
        "started_liquidity_share": mean([r["groups"].get("started_liquidity_share") for r in rs]),
        "started_choice_share": mean([r["groups"].get("started_choice_share") for r in rs]),
        "n_population": mean([r["groups"].get("n_population") for r in rs]),
        "n_exits": mean([r["groups"].get("n_exits") for r in rs]),
        "n_censored": mean([r["groups"].get("n_censored") for r in rs]),
    }
    for quint in ("q1", "q2", "q3", "q4", "q5"):
        out[quint] = {c: mean([(r["groups"].get(quint) or {}).get(c) for r in rs]) for c in CATS}
        out[quint]["n"] = mean([(r["groups"].get(quint) or {}).get("n") for r in rs])
    for grp in ("urban", "rural"):
        out[grp] = {c: mean([(r["groups"].get(grp) or {}).get(c) for r in rs]) for c in CATS}
        out[grp]["n"] = mean([(r["groups"].get(grp) or {}).get("n") for r in rs])
    out["metrics"] = {k: mean([r["metrics"].get(k) for r in rs]) for k in
                      ("completion_primary", "completion_lower", "completion_upper",
                       "completion_tertiary", "tut_rate", "formal_rate")}
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--in", dest="inp", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    d = json.load(open(a.inp))
    rows = d["rows"]
    cls = [c for c in rows[0]["combo"]]
    axes = d["design"]["axes"]
    names = list(axes.keys())
    rep = {"source": os.path.abspath(a.inp), "label": d.get("label"),
           "driver_sha256": d["code_sha256"].get("run_edsystem_multiverse.py"),
           "runs": len(rows), "elapsed_s": d.get("elapsed_s"),
           "notes": "Exit shares partition the full measured child population (exits from e.exits + "
                    "survivors censored at horizon). Mean over seeds; derived report, results unmodified."}
    for ci in (0, 143):
        out = combo_report(rows, ci)
        out["combo_named"] = dict(zip(names, out["combo"]))
        rep[f"combo_{ci}"] = out
    with open(a.out, "w") as f:
        json.dump(rep, f, indent=1)
    # human-readable headline
    def pct(x):
        return f"{100*x:.1f}%" if x is not None else "n/a"
    print("CORRECTED EXIT DECOMPOSITION (mean over seeds)")
    for ci in (0, 143):
        c = rep[f"combo_{ci}"]
        print(f"\ncombo {ci}: {c['combo_named']}  seeds {c['seeds'][0]}..{c['seeds'][1]} (n={c['n_seeds']})")
        o = c["overall"]
        print(f"  started: liquidity {pct(o['started_liquidity_share'])}  choice {pct(o['started_choice_share'])}")
        print(f"  population {o['n_population']:.0f} = exits {o['n_exits']:.0f} + censored {o['n_censored']:.0f}")
        for q in ("q1", "q2", "q3", "q4", "q5"):
            g = c[q]
            print(f"  {q}: liq {pct(g['liquidity'])} choice {pct(g['choice'])} never {pct(g['never'])} "
                  f"censored {pct(g['censored'])} other {pct(g['other_terminal'])} started {pct(g['started_share'])}")
        for grp in ("urban", "rural"):
            g = c[grp]
            print(f"  {grp}: liq {pct(g['liquidity'])} choice {pct(g['choice'])} never {pct(g['never'])} "
                  f"censored {pct(g['censored'])} other {pct(g['other_terminal'])}")
        m = c["metrics"]
        fm = lambda k: f"{m[k]:.3f}" if m.get(k) is not None else "n/a"
        print(f"  attainment: lower {fm('completion_lower')} upper {fm('completion_upper')} "
              f"tertiary {fm('completion_tertiary')} tut_rate {fm('tut_rate')}")


if __name__ == "__main__":
    main()
