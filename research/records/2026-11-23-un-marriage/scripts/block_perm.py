#!/usr/bin/env python3
"""Block (circular-shift) permutation falsifier.

The within-country *year shuffle* used in falsify.py re-assigns the sparse
series' values to survey years at random.  That destroys the serial structure of
the series, so the null distribution of the coefficient is much too narrow and
the test rejects far too easily (it is anti-conservative).  This script repeats
the same test with a **circular shift within each country**: the country's values
keep their order and spacing, only their alignment to the calendar years is
rotated.  This preserves the country's serial correlation and level while
breaking the link between the marriage series and the outcome years, which is the
right null for "is the timing informative?".

Reported for the edges where the two permutation schemes disagree.
"""
import json
import numpy as np
from edge_marriage import S, build_rows, fit

RNG = np.random.default_rng(20261124)
EDGES = [("nevermar_f_4549", "fertility", "grid10"),
         ("smam_f", "fertility", "grid10"),
         ("smam_gap", "fertility", "grid10"),
         ("coresid_60plus", "fertility", "grid10")]
NPERM = {"nevermar_f_4549": 200, "smam_f": 200, "smam_gap": 100, "coresid_60plus": 100}


def circ_shift(name):
    byc = {}
    for (i, t), v in S[name].items():
        byc.setdefault(i, []).append((t, v))
    out = {}
    for i, lst in sorted(byc.items()):
        lst.sort()
        vals = [v for _, v in lst]
        if len(vals) > 1:
            k = int(RNG.integers(1, len(vals)))
            vals = list(np.roll(np.array(vals), k))
        for (t, _), v in zip(lst, vals):
            out[(i, t)] = float(v)
    return out


def run(x, y, mode, nperm):
    base = fit(build_rows(x, y, mode), True, x, y)
    if base is None:
        return None
    obs = abs(base["b"])
    null = []
    for _ in range(nperm):
        old = S[x]
        S[x] = circ_shift(x)
        try:
            r = fit(build_rows(x, y, mode), True, x, y)
        finally:
            S[x] = old
        if r is not None:
            null.append(abs(r["b"]))
    null = np.array(null)
    return dict(actual=base, n=nperm, p_circ=float((null >= obs).mean()),
                q05=float(np.percentile(null, 5)),
                q50=float(np.percentile(null, 50)),
                q95=float(np.percentile(null, 95)), obs=obs)


if __name__ == "__main__":
    out = {}
    for x, y, mode in EDGES:
        if x not in S:
            print(f"{x}: missing")
            continue
        r = run(x, y, mode, NPERM[x])
        if r is None:
            print(f"{x}: not estimable")
            continue
        out[f"{x}->{y}"] = r
        a = r["actual"]
        print(f"{x:16s} -> {y}  b={a['b']:+.4f} se={a['se']:.4f} n={a['n']} "
              f"countries={a['nc']}")
        print(f"    circular-shift permutation p={r['p_circ']:.3f} "
              f"(draws={r['n']}; null |b| q05={r['q05']:.4f} median={r['q50']:.4f} "
              f"q95={r['q95']:.4f}; actual |b|={r['obs']:.4f})")
    json.dump(out, open("/root/work/undata/results_block_perm.json", "w"), indent=1)
    print("wrote /root/work/undata/results_block_perm.json")
