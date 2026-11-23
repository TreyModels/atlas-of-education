#!/usr/bin/env python3
"""Tests designed to kill the marriage-timing edges.

For each marriage-timing edge that survives country trends, run:
  1. permutation: shuffle the sparse series across years within each country
     (keeps each country's level and distribution, destroys the true timing),
     200 draws; report the share of draws whose |b| is at least the actual |b|;
  2. country jackknife: drop one country at a time, report the range of b;
  3. sample-selection check for schooling -> fertility: is the edge on the
     country-years where marriage data exist the same as on the whole panel?

Reuses edge_marriage.py (which reuses full_matrix_trends.py's estimator).
"""
import json
import numpy as np
from edge_marriage import S, build_rows, fit, CTRL, grid10, survey10

RNG = np.random.default_rng(20261123)
EDGES = [("smam_f", "fertility", "grid10"),
         ("smam_gap", "fertility", "grid10"),
         ("nevermar_f_4549", "fertility", "grid10"),
         ("coresid_60plus", "fertility", "grid10"),
         ("sec", "smam_f", "survey10"),
         ("sec", "nevermar_f_4549", "survey10"),
         ("sec", "smam_gap", "survey10")]
NPERM = 200


def actual(x, y, mode):
    rows = build_rows(x, y, mode)
    return fit(rows, True, x, y), rows


def permute_sparse(name):
    """Return a copy of S[name] with values shuffled across years within country."""
    byc = {}
    for (i, t), v in S[name].items():
        byc.setdefault(i, []).append((t, v))
    out = {}
    for i, lst in byc.items():
        lst = sorted(lst)
        vals = [v for _, v in lst]
        RNG.shuffle(vals)
        for (t, _), v in zip(lst, vals):
            out[(i, t)] = v
    return out


def perm_p(x, y, mode, base, nperm=NPERM):
    if base is None:
        return None
    obs = abs(base["b"])
    null = []
    old = None
    for _ in range(nperm):
        # shuffle the sparse side: x for grid10 edges, y for survey10 edges
        target = x if mode == "grid10" else y
        old = S[target]
        S[target] = permute_sparse(target)
        try:
            r = fit(build_rows(x, y, mode), True, x, y)
        finally:
            S[target] = old
        if r is not None:
            null.append(abs(r["b"]))
    if not null:
        return dict(n=0)
    null = np.array(null)
    return dict(n=len(null), p=float((null >= obs).mean()),
                q05=float(np.percentile(null, 5)),
                q50=float(np.percentile(null, 50)),
                q95=float(np.percentile(null, 95)),
                obs=obs)


def jackknife(x, y, mode, rows):
    if not rows:
        return None
    bs = []
    countries = sorted({r[0] for r in rows})
    for c in countries:
        r = fit([r2 for r2 in rows if r2[0] != c], True, x, y)
        if r is not None:
            bs.append(r["b"])
    if len(bs) < 5:
        return dict(n=len(bs))
    bs = np.array(bs)
    return dict(n=len(bs), min=float(bs.min()), max=float(bs.max()),
                q05=float(np.percentile(bs, 5)),
                q50=float(np.percentile(bs, 50)),
                q95=float(np.percentile(bs, 95)),
                share_same_sign=float((np.sign(bs) == np.sign(np.median(bs))).mean()))


def selection_check():
    """sec -> fertility on the whole panel vs on the marriage-data subsample."""
    full = fit(build_rows("sec", "fertility", "grid10"), True, "sec", "fertility")
    rows = [r for r in build_rows("sec", "fertility", "grid10")
            if (r[0], r[1]) in S["smam_f"]]
    sub = fit(rows, True, "sec", "fertility")
    rows2 = [r for r in build_rows("sec", "fertility", "grid10")
             if (r[0], r[1]) in S["nevermar_f_4549"]]
    sub2 = fit(rows2, True, "sec", "fertility")
    return dict(full=full, marriage_smam_sample=sub,
                marriage_nevermar_sample=sub2)


def heterogeneity():
    """Does the schooling -> fertility edge differ by marriage regime?

    Countries split by their earliest observed share never married at 45-49
    (above/below the median).  This is a split sample, not a control: marriage
    age is on the causal path and is never put in the regression.
    """
    reg = {}
    for (i, t), v in S["nevermar_f_4549"].items():
        reg[i] = min(reg.get(i, 1e9), t)  # first survey year per country
    first = {i: v for i, v in {i: S["nevermar_f_4549"][(i, t)]
                               for i, t in [(i, min(t2 for (i2, t2) in S["nevermar_f_4549"] if i2 == i))
                                            for i in reg]}.items()}
    vals = sorted(first.values())
    cut = vals[len(vals) // 2]
    low = {i for i, v in first.items() if v <= cut}
    rows = build_rows("sec", "fertility", "grid10")
    out = {}
    for name, keep in (("low_never_married", low), ("high_never_married", set(first) - low)):
        sub = [r for r in rows if r[0] in keep]
        out[name] = fit(sub, True, "sec", "fertility")
    return dict(cut=cut, groups=out, n_low=len(low), n_high=len(first) - len(low))


def log_income_check():
    """Re-run the headline edges with income genuinely logged (session rule)."""
    old = {k: v for k, v in S["gdppc_log"].items()}
    S["gdppc_log"] = {k: np.log(max(v, 1.0)) for k, v in old.items()}
    out = {}
    try:
        for x, y, mode in EDGES:
            if x in S and y in S:
                r = (grid10 if mode == "grid10" else survey10)(x, y, True)
                out[f"{x}->{y}"] = r
    finally:
        S["gdppc_log"] = old
    return out


if __name__ == "__main__":
    out = {}
    print("=== permutation + jackknife falsifiers (all with country trends) ===")
    for x, y, mode in EDGES:
        if x not in S or y not in S:
            print(f"{x} -> {y}: missing series")
            continue
        base, rows = actual(x, y, mode)
        if base is None:
            print(f"{x} -> {y}: not estimable")
            continue
        pp = perm_p(x, y, mode, base)
        jk = jackknife(x, y, mode, rows)
        rec = dict(actual=base, permutations=pp, jackknife=jk, mode=mode)
        out[f"{x}->{y}"] = rec
        print(f"{x:16s} -> {y:16s} b={base['b']:+.4f} (se {base['se']:.4f}, n={base['n']}, "
              f"{base['nc']} countries)")
        print(f"    permutation p={pp.get('p'):.3f} null |b| q05={pp.get('q05'):.4f} "
              f"median={pp.get('q50'):.4f} q95={pp.get('q95'):.4f} "
              f"actual|b|={pp.get('obs'):.4f} (draws={pp.get('n')})")
        print(f"    jackknife: drop-one-country b range {jk.get('min'):+.4f} to "
              f"{jk.get('max'):+.4f}; same sign in {jk.get('share_same_sign'):.0%} of drops")
    out["selection_check"] = selection_check()
    out["heterogeneity"] = heterogeneity()
    out["log_income"] = log_income_check()
    print("\n=== sample-selection check: sec -> fertility (country trends) ===")
    for k, v in out["selection_check"].items():
        if v is None:
            print(f"  {k}: not estimable")
        else:
            print(f"  {k:26s} b={v['b']:+.4f} se={v['se']:.4f} n={v['n']} "
                  f"countries={v['nc']}")
    print("\n=== heterogeneity: sec -> fertility by marriage regime (country trends) ===")
    h = out["heterogeneity"]
    print(f"  split at never-married 45-49 = {h['cut']:.1f}% (low group {h['n_low']} "
          f"countries, high group {h['n_high']})")
    for k, v in h["groups"].items():
        print(f"  {k:20s} " + (f"b={v['b']:+.4f} se={v['se']:.4f} n={v['n']} "
                               f"countries={v['nc']}" if v else "not estimable"))
    print("\n=== income logged (session rule) vs levels, country trends ===")
    for k, v in out["log_income"].items():
        base = out.get(k, {}).get("actual") if k in out else None
        print(f"  {k:34s} " + (f"b={v['b']:+.4f} se={v['se']:.4f} n={v['n']}" if v else "not estimable"))
    json.dump(out, open("/root/work/undata/results_falsifiers.json", "w"), indent=1)
    print("\nwrote /root/work/undata/results_falsifiers.json")
