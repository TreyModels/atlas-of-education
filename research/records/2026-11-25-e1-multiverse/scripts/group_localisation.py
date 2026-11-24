#!/usr/bin/env python3
"""E1 group-localisation diagnostic.

For the 'robust everywhere' links and for every link certified under BY at the largest R, ask whether the
signal is concentrated in a minority of countries. Leave-one-country-out pooled estimates on the full panel
(trend specification) are computed with the unchanged estimator (gm_core.fit_edge); then the top-5 countries
are removed jointly and the estimate is re-computed. A link is 'group-concentrated' if excluding its top 5
countries flips significance (|t| < 1.96) or changes |b| by more than 50%.
"""
import os, sys, json, csv
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import gm_core as g

OUT = os.environ.get("GM_OUT", "/root/work/e1/out")
RES = os.path.join(ROOT, "results")
summary = json.load(open(os.path.join(RES, "summary_by_R.json")))
Rmax = summary["available_R"]
robust = [tuple(x) for x in summary["robust_everywhere"]]
# BY-certified links at Rmax, from the per-link csv
verdict = list(csv.DictReader(open(os.path.join(RES, "verdict_by_R.csv"))))
by_links = []
for row in verdict:
    for proc in ("up", "down", "flip", "het"):
        k = f"certBY_{proc}_R{Rmax}"
        if row.get(k) == "1":
            by_links.append((row["x"], row["y"]))
by_links = sorted(set(by_links))

PAIR_IDX = {(x, y): i for i, (x, y) in enumerate(g.PAIRS)}
ALL = np.ones(g.C, bool)
ISO = list(g.ISOS)


def fit_on(mem):
    return None


def link_stats(x, y):
    pi = PAIR_IDX[(x, y)]
    spec = 2 * pi + 1  # trend specification
    E = g.EDGES[spec]
    base = g.fit_edge(E, ALL)
    if base is None:
        return None
    b0, se0 = base[0], base[1]
    t0 = b0 / se0
    loo = []
    for c, iso in enumerate(ISO):
        mem = ALL.copy(); mem[c] = False
        r = g.fit_edge(E, mem)
        if r is None:
            continue
        loo.append((iso, r[0], r[0] / r[1] if r[1] > 0 else np.nan))
    if not loo:
        return None
    loo.sort(key=lambda z: -abs(b0 - z[1]))
    top5 = [z[0] for z in loo[:5]]
    mem = ALL.copy()
    for iso in top5:
        mem[ISO.index(iso)] = False
    r5 = g.fit_edge(E, mem)
    t5 = (r5[0] / r5[1]) if (r5 is not None and r5[1] > 0) else np.nan
    b5 = r5[0] if r5 is not None else np.nan
    ts = np.array([z[2] for z in loo], float)
    deltas = np.array([abs(b0 - z[1]) for z in loo], float)
    order = np.argsort(-deltas)
    top10_share = float(deltas[order][:10].sum() / max(deltas.sum(), 1e-12))
    top5_share = float(deltas[order][:5].sum() / max(deltas.sum(), 1e-12))
    flip = bool(np.isfinite(t5) and (np.sign(t5) != np.sign(t0) or abs(t5) < 1.96))
    change = float(abs(b5 - b0) / max(abs(b0), 1e-12)) if np.isfinite(b5) else np.nan
    return dict(x=x, y=y, b=b0, se=se0, t=t0, t_top5_removed=t5 if np.isfinite(t5) else None,
                n_excl_below_1_96=int(np.nansum(np.abs(ts) < 1.96) - 1) if np.isfinite(ts).all() else 0,
                min_abs_t=float(np.nanmin(np.abs(ts))), max_abs_delta_b=float(np.nanmax(deltas)),
                top5_countries=top5, top5_signal_share=top5_share, top10_signal_share=top10_share,
                flips_when_top5_removed=flip, rel_change_b_top5=change,
                group_concentrated=bool(flip or (np.isfinite(change) and change > 0.5)))


res = dict(R=Rmax, robust_links=robust, by_certified_links=by_links,
           robust=[], by=[])
for x, y in robust:
    st = link_stats(x, y)
    if st:
        res["robust"].append(st)
seen = set((r["x"], r["y"]) for r in res["robust"])
for x, y in by_links:
    if (x, y) in seen:
        continue
    st = link_stats(x, y)
    if st:
        st["by_certified"] = True
        res["by"].append(st)
allst = res["robust"] + res["by"]
res["summary"] = dict(n_robust=len(res["robust"]),
                      n_robust_group_concentrated=sum(1 for r in res["robust"] if r["group_concentrated"]),
                      n_by_links=len(by_links),
                      n_by_group_concentrated=sum(1 for r in allst if r["group_concentrated"]),
                      n_by_checked=len(allst))
json.dump(res, open(os.path.join(RES, "group_localisation.json"), "w"), indent=1, default=float)
with open(os.path.join(RES, "group_localisation.csv"), "w", newline="") as fh:
    w = csv.writer(fh)
    w.writerow(["set", "x", "y", "b", "se", "t", "t_top5_removed", "min_abs_t",
                "max_abs_delta_b", "top5_countries", "top5_signal_share", "top10_signal_share",
                "flips_when_top5_removed", "rel_change_b_top5", "group_concentrated"])
    for tag, lst in (("robust", res["robust"]), ("by", res["by"])):
        for r in lst:
            w.writerow([tag, r["x"], r["y"], r["b"], r["se"], r["t"], r["t_top5_removed"],
                        r["min_abs_t"], r["max_abs_delta_b"], ";".join(r["top5_countries"]),
                        r["top5_signal_share"], r["top10_signal_share"],
                        int(r["flips_when_top5_removed"]), r["rel_change_b_top5"],
                        int(r["group_concentrated"])])
print(json.dumps(res["summary"], indent=1))
